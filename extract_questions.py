#!/usr/bin/env python3
"""
Improved extractor: parse options/answer from the prompt text using ●​ bullet marker.
"""
import fitz
import json
import re
import os
from collections import OrderedDict

OUT_JSON = "src/data/questions.json"
IMG_DIR  = "public/img/questions"
IMG_WEB  = "/img/questions"

os.makedirs(IMG_DIR, exist_ok=True)

BULLET = "●"  # the bullet character used in PDFs

def split_choices(raw):
    """
    Split raw text into choices using ●​ as delimiter.
    Returns list of raw choice strings.
    """
    # Split on bullet followed by optional zero-width spaces then A/B/C/D
    parts = re.split(r"●[\u200b\s]*", raw)
    return [p.strip() for p in parts if p.strip()]

def parse_choice_item(item):
    """
    Parse 'A ✅ font-weight: bold;' → (letter, text, is_correct)
    """
    correct = "✅" in item or "☑" in item
    item = item.replace("✅", "").replace("☑", "").strip()
    m = re.match(r"^([A-D])\s+(.*)", item, re.DOTALL)
    if m:
        return m.group(1), m.group(2).strip(), correct
    return None, item, correct

def parse_question_block(raw_text, level, q_num, q_images):
    lines = [l for l in raw_text.splitlines() if l.strip()]
    if not lines:
        return None

    # First line: "QN — Title + optional question body"
    header_line = lines[0]
    header_line = re.sub(r"^Q\d+\s*[—–\-]\s*", "", header_line).strip()

    # Everything after the header line is body+choices (as individual lines or merged)
    body_raw = " ".join(lines[1:])

    # --- Split body into: question prompt vs choices ---
    # Choices start at first ● marker
    bullet_pos = body_raw.find(BULLET)
    if bullet_pos >= 0:
        prompt_part = body_raw[:bullet_pos].strip()
        choices_raw = body_raw[bullet_pos:]
    else:
        prompt_part = body_raw.strip()
        choices_raw = ""

    # Parse choices
    choice_items = split_choices(choices_raw)
    options = ["", "", "", ""]
    answer_text = ""
    letter_map = {"A": 0, "B": 1, "C": 2, "D": 3}

    for item in choice_items:
        letter, text, correct = parse_choice_item(item)
        if letter in letter_map:
            options[letter_map[letter]] = text
            if correct:
                answer_text = text

    return {
        "id": f"L{level}Q{q_num:02d}",
        "title": header_line,
        "prompt": prompt_part if prompt_part else None,
        "image": q_images.get(q_num),
        "options": options,
        "answer": answer_text,
    }

def collect_question_images(doc, level, max_q):
    """
    Map images to question numbers by document reading order.
    We assign each image block to the latest seen question header (Qxx) before it.
    This handles layouts where an image for a question appears on the next page.
    """
    image_map = OrderedDict()
    current_q = None

    for page in doc:
        # Gather Q header positions on this page.
        headers = []
        page_dict = page.get_text("dict")
        for block in page_dict.get("blocks", []):
            if block.get("type") != 0:
                continue
            for line in block.get("lines", []):
                text = "".join(span.get("text", "") for span in line.get("spans", [])).strip()
                m = re.match(r"Q(\d{1,2})\s*[—–\-]", text)
                if not m:
                    continue
                q_num = int(m.group(1))
                if 1 <= q_num <= max_q:
                    headers.append((line.get("bbox", [0, 0, 0, 0])[1], q_num))

        headers.sort(key=lambda x: x[0])

        # Gather all image occurrences with y-position.
        image_occurrences = []
        for img_info in page.get_images(full=True):
            xref = img_info[0]
            try:
                base = doc.extract_image(xref)
            except Exception:
                continue
            img_bytes = base.get("image", b"")
            if len(img_bytes) < 2000:
                continue

            rects = page.get_image_rects(xref)
            if not rects:
                continue

            for rect in rects:
                image_occurrences.append((rect.y0, xref, img_bytes, base.get("ext", "png")))

        image_occurrences.sort(key=lambda item: item[0])

        for img_y, _, img_bytes, ext in image_occurrences:
            target_q = current_q

            if headers:
                first_header_y = headers[0][0]
                if img_y >= first_header_y - 120:
                    target_q = min(headers, key=lambda item: abs(item[0] - img_y))[1]

            if target_q is None or target_q in image_map:
                continue

            ext = (ext or "png").lower()
            if ext in {"jpx", "jpeg2000"}:
                ext = "png"

            fname = f"level{level}_q{target_q:02d}.{ext}"
            fpath = os.path.join(IMG_DIR, fname)
            with open(fpath, "wb") as f:
                f.write(img_bytes)
            image_map[target_q] = f"{IMG_WEB}/{fname}"
            print(f"  [IMG] Q{target_q:02d} → {fname}")

        if headers:
            current_q = headers[-1][1]

    return dict(image_map)

def extract_level(level, max_q):
    pdf_path = f"Question/Level{level}.pdf"
    if not os.path.exists(pdf_path):
        print(f"  [SKIP] {pdf_path}")
        return []

    doc = fitz.open(pdf_path)
    print(f"\n── Level {level}: {len(doc)} pages ──")

    # --- Collect images mapped by question header flow ---
    q_images = collect_question_images(doc, level, max_q)

    # --- Collect all text then split by question header ---
    full_text = "\n".join(page.get_text("text") for page in doc)
    parts = re.split(r"(?=Q\d{1,2}\s*[—–\-])", full_text)

    questions = []
    for part in parts:
        m = re.match(r"Q(\d+)\s*[—–\-]", part)
        if not m:
            continue
        q_num = int(m.group(1))
        if q_num < 1 or q_num > max_q:
            continue
        q = parse_question_block(part.strip(), level, q_num, q_images)
        if q:
            questions.append(q)
            correct_flag = "✅" if q["answer"] else "❌ MISSING"
            print(f"  Q{q_num:02d} {correct_flag}  {q['title'][:50]}")

    doc.close()
    return questions


# ── main ──────────────────────────────────────────────
level_config = {1: 20, 2: 20, 3: 20, 4: 20, 5: 10}
output = {}

for level, max_q in level_config.items():
    qs = extract_level(level, max_q)
    output[f"level{level}"] = qs
    missing = [q for q in qs if not q["answer"]]
    print(f"  => {len(qs)} questions | {len(missing)} missing answers")

with open(OUT_JSON, "w", encoding="utf-8") as f:
    json.dump(output, f, ensure_ascii=False, indent=2)

total = sum(len(v) for v in output.values())
print(f"\n✅ Done! {total} questions → {OUT_JSON}")
