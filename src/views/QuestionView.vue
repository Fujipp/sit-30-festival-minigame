<template>
  <div class="question-screen">
    <div class="question-overlay"></div>

    <img class="icon icon-top-left" src="/img/icon/SIT_30.png" alt="SIT 30" />
    <img class="icon icon-bottom-left" src="/img/icon/GOOSE.png" alt="Goose" />
    <img class="icon icon-bottom-right" src="/img/icon/SIT.png" alt="SIT" />

    <div class="question-content">
      <div class="question-header">
        <div class="question-pill">Level {{ game.currentLevel }} - {{ questionCode }}</div>
      </div>

      <div class="question-panel">
        <section class="question-left">
          <h2 class="question-title">{{ game.activeQuestion.title }}</h2>
          <p v-if="game.activeQuestion.prompt" class="question-prompt">{{ game.activeQuestion.prompt }}</p>

          <div class="choices-list">
            <button
              v-for="(opt, oIdx) in game.activeQuestion.options"
              :key="oIdx"
              type="button"
              class="choice-btn"
              :disabled="selectedOptionIndex !== null"
              :class="choiceClass(opt, oIdx)"
              @click="selectChoice(oIdx)"
            >
              <span class="choice-index">{{ ['A', 'B', 'C', 'D'][oIdx] }}</span>
              <span class="choice-text">{{ opt }}</span>
            </button>
          </div>
        </section>

        <aside class="question-right">
          <div v-if="game.activeQuestion.image" class="image-wrap">
            <img :src="game.activeQuestion.image" alt="Question image" class="question-image" />
          </div>
          <pre v-else-if="game.activeQuestion.code" class="code-wrap" v-html="highlightedCode"></pre>
          <div v-else class="image-empty">NO IMAGE</div>
        </aside>
      </div>

      <div class="question-footer">
        <button @click="resetChoice" class="back-btn reset-btn" :disabled="selectedOptionIndex === null">RESET</button>
        <button @click="goBack" class="back-btn">BACK</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, onMounted, ref, watch } from 'vue'
import { useRouter } from 'vue-router'
import { useGameStore } from '../stores/gameStore.js'

const router = useRouter()
const game = useGameStore()
const selectedOptionIndex = ref(null)

onMounted(() => {
  if (!game.currentQuestions.length) {
    router.replace('/level')
  }
})

watch(() => game.activeQuestionIndex, () => {
  selectedOptionIndex.value = null
})

const questionCode = computed(() => {
  const id = game.activeQuestion?.id
  if (typeof id === 'string') {
    const m = id.match(/Q\d{2}$/i)
    if (m) return m[0].toUpperCase()
  }
  return `Q${String(game.activeQuestionIndex + 1).padStart(2, '0')}`
})

const escapeHtml = (text) => text
  .replaceAll('&', '&amp;')
  .replaceAll('<', '&lt;')
  .replaceAll('>', '&gt;')
  .replaceAll('"', '&quot;')
  .replaceAll("'", '&#39;')

const highlightCodeText = (source) => {
  const escaped = escapeHtml(source)
  const tokenRegex = /(&lt;\/?[a-zA-Z0-9-]+|&quot;[^&]*?&quot;|@[a-z-]+|[.#][a-zA-Z_][\w-]*|#[0-9a-fA-F]{3,8}\b|\b(?:var|rgb|rgba|hsl|hsla)\b|\b(?:class|id)\b(?==)|\b(?:blue|red|green|grey|gray|coral|orange|purple|black|white)\b|\b\d+(?:\.\d+)?(?:px|rem|em|%)?\b|\b[a-z-]+(?=\s*:)|[{}():])/g

  return escaped.replace(tokenRegex, (token) => {
    if (token.startsWith('&lt;')) return `<span class="tok-tag">${token}</span>`
    if (token.startsWith('&quot;')) return `<span class="tok-string">${token}</span>`
    if (token.startsWith('@')) return `<span class="tok-atrule">${token}</span>`
    if (token.startsWith('.') || token.startsWith('#')) return `<span class="tok-selector">${token}</span>`
    if (/^#[0-9a-fA-F]{3,8}$/.test(token) || /^\d/.test(token)) return `<span class="tok-number">${token}</span>`
    if (/^(var|rgb|rgba|hsl|hsla)$/.test(token)) return `<span class="tok-fn">${token}</span>`
    if (/^(class|id)$/.test(token)) return `<span class="tok-attr">${token}</span>`
    if (/^[{}():]$/.test(token)) return `<span class="tok-punc">${token}</span>`
    if (/^(blue|red|green|grey|gray|coral|orange|purple|black|white)$/.test(token)) return `<span class="tok-value">${token}</span>`
    return `<span class="tok-prop">${token}</span>`
  })
}

const highlightedCode = computed(() => {
  const code = game.activeQuestion?.code
  if (!code) return ''
  return highlightCodeText(code)
})

const playResultTone = async (isCorrect) => {
  const AudioCtx = window.AudioContext || window.webkitAudioContext
  if (!AudioCtx) return
  const ctx = new AudioCtx()

  const osc = ctx.createOscillator()
  const gain = ctx.createGain()
  osc.type = isCorrect ? 'triangle' : 'sawtooth'
  osc.frequency.value = isCorrect ? 820 : 260
  gain.gain.value = 0.0001

  osc.connect(gain)
  gain.connect(ctx.destination)

  const now = ctx.currentTime
  gain.gain.exponentialRampToValueAtTime(isCorrect ? 0.035 : 0.04, now + 0.01)
  gain.gain.exponentialRampToValueAtTime(0.0001, now + (isCorrect ? 0.12 : 0.14))
  osc.start(now)
  osc.stop(now + (isCorrect ? 0.13 : 0.15))
}

const selectChoice = (index) => {
  if (selectedOptionIndex.value !== null) return
  selectedOptionIndex.value = index
  const selectedOption = game.activeQuestion?.options?.[index]
  playResultTone(selectedOption === game.activeQuestion?.answer)
}

const choiceClass = (option, index) => {
  if (selectedOptionIndex.value === null) return ''
  if (index === selectedOptionIndex.value) {
    return option === game.activeQuestion.answer ? 'choice-btn--correct' : 'choice-btn--wrong'
  }
  return 'choice-btn--dim'
}

const resetChoice = () => {
  selectedOptionIndex.value = null
}

const goBack = () => {
  router.push('/board')
}
</script>

<style scoped>
.question-screen {
  position: fixed;
  inset: 0;
  width: 100vw;
  height: 100vh;
  overflow: hidden;
  background: center / cover no-repeat url('/img/SIT Festival Template.png');
}

.question-overlay {
  position: absolute;
  inset: 0;
  background:
    radial-gradient(90% 45% at 50% 100%, rgba(130, 182, 227, 0.46) 0%, rgba(130, 182, 227, 0) 68%),
    linear-gradient(180deg, rgba(16, 82, 154, 0.22) 0%, rgba(16, 82, 154, 0.12) 45%, rgba(16, 82, 154, 0.34) 100%);
}

.icon {
  position: absolute;
  z-index: 9999;
  pointer-events: none;
  user-select: none;
}

.icon-top-left { top: 0.8rem; left: 1.2rem; width: 20rem; }
.icon-bottom-left { bottom: 0; left: 0.4rem; width: 5rem; }
.icon-bottom-right { right: -0.4rem; bottom: 0.4rem; width: 15rem; }

.question-content {
  position: relative;
  z-index: 3;
  display: flex;
  flex-direction: column;
  width: 100%;
  height: 100%;
  padding: 4.7rem clamp(0.8rem, 2.3vw, 1.7rem) 1rem;
}

.question-header {
  display: flex;
  justify-content: center;
  margin-bottom: 0.9rem;
}

.question-pill {
  padding: 0.68rem 1.35rem;
  border-radius: 999px;
  border: 1px solid rgba(255, 255, 255, 0.42);
  background: linear-gradient(135deg, rgba(255, 255, 255, 0.24), rgba(130, 182, 227, 0.14));
  backdrop-filter: blur(10px);
  color: #eef7ff;
  font-family: 'Outfit', 'Sarabun', sans-serif;
  font-size: clamp(1rem, 1.9vw, 1.3rem);
  font-weight: 800;
  letter-spacing: 0.06em;
}

.question-panel {
  flex: 1;
  min-height: 0;
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 0.9rem;
}

.question-left,
.question-right {
  border: 1px solid rgba(255, 255, 255, 0.28);
  border-radius: 1.1rem;
  background: linear-gradient(135deg, rgba(255, 255, 255, 0.2), rgba(130, 182, 227, 0.1));
  backdrop-filter: blur(11px);
  box-shadow:
    0 10px 26px rgba(7, 30, 60, 0.28),
    inset 0 1px 0 rgba(255, 255, 255, 0.45),
    inset 0 -10px 20px rgba(16, 82, 154, 0.16);
}

.question-left {
  padding: 1.1rem;
  display: flex;
  flex-direction: column;
  min-height: 0;
}

.question-title {
  margin: 0;
  color: #fff;
  font-family: 'Outfit', 'Sarabun', sans-serif;
  font-size: clamp(1.08rem, 2.1vw, 1.75rem);
  line-height: 1.35;
  font-weight: 800;
}

.question-prompt {
  margin: 0.45rem 0 0;
  color: #e7f3ff;
  font-size: clamp(0.95rem, 1.35vw, 1.12rem);
  line-height: 1.45;
}

.choices-list {
  margin-top: 0.85rem;
  display: grid;
  grid-template-columns: 1fr;
  gap: 0.65rem;
}

.choice-btn {
  min-height: 72px;
  border-radius: 0.95rem;
  border: 1px solid rgba(255, 255, 255, 0.34);
  background: rgba(8, 25, 54, 0.36);
  color: #fff;
  display: flex;
  align-items: center;
  gap: 0.7rem;
  text-align: left;
  padding: 0.75rem 0.9rem;
  cursor: pointer;
  transition: transform 0.16s ease, box-shadow 0.18s ease, border-color 0.18s ease, background 0.18s ease, opacity 0.18s ease;
}

.choice-btn:not(:disabled):hover {
  transform: translateY(-1px) scale(1.01);
  border-color: rgba(173, 218, 255, 0.95);
  background: rgba(22, 61, 110, 0.62);
  box-shadow:
    0 8px 18px rgba(8, 23, 48, 0.36),
    inset 0 1px 0 rgba(255, 255, 255, 0.2);
}

.choice-btn:not(:disabled):active {
  transform: translateY(1px) scale(0.99);
}

.choice-btn:disabled {
  cursor: default;
}

.choice-btn--correct { background: rgba(46, 204, 113, 0.48); border-color: rgba(46, 204, 113, 0.92); }
.choice-btn--wrong { background: rgba(231, 76, 60, 0.42); border-color: rgba(231, 76, 60, 0.86); }
.choice-btn--dim { opacity: 0.42; }

.choice-index {
  width: 2.2rem;
  height: 2.2rem;
  border-radius: 999px;
  background: #fff;
  color: #0a2048;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  font-size: 1.06rem;
  font-weight: 800;
  flex: none;
}

.choice-text {
  font-size: clamp(0.9rem, 1.38vw, 1.12rem);
  font-weight: 700;
  line-height: 1.35;
}

.question-right {
  padding: 0.85rem;
  display: flex;
  align-items: center;
  justify-content: center;
}

.image-wrap {
  width: 100%;
  height: 100%;
  border-radius: 0.85rem;
  overflow: hidden;
  background: rgba(255, 255, 255, 0.12);
}

.question-image { width: 100%; height: 100%; object-fit: contain; }

.code-wrap {
  width: 100%;
  height: 100%;
  margin: 0;
  padding: 1rem 1.05rem;
  overflow: auto;
  border-radius: 0.85rem;
  border: 1px solid rgba(133, 193, 255, 0.66);
  background:
    linear-gradient(180deg, rgba(7, 16, 38, 0.95) 0%, rgba(9, 26, 58, 0.95) 100%);
  color: #eef6ff;
  font-size: clamp(0.83rem, 1.08vw, 0.96rem);
  line-height: 1.5;
  font-family: 'JetBrains Mono', 'Fira Code', 'Menlo', monospace;
  white-space: pre-wrap;
  box-shadow:
    inset 0 0 0 1px rgba(255, 255, 255, 0.08),
    0 8px 24px rgba(4, 13, 32, 0.42);
}

.code-wrap :deep(.tok-tag) { color: #ff9fdd; }
.code-wrap :deep(.tok-atrule) { color: #7ed0ff; font-weight: 700; }
.code-wrap :deep(.tok-selector) { color: #9cf78b; }
.code-wrap :deep(.tok-prop) { color: #ffd479; }
.code-wrap :deep(.tok-value) { color: #7fc7ff; }
.code-wrap :deep(.tok-number) { color: #ffb38f; }
.code-wrap :deep(.tok-string) { color: #ffe8a4; }
.code-wrap :deep(.tok-attr) { color: #b9c7ff; }
.code-wrap :deep(.tok-fn) { color: #96f1de; }
.code-wrap :deep(.tok-punc) { color: #d6e7ff; }

.code-wrap::-webkit-scrollbar {
  width: 10px;
}

.code-wrap::-webkit-scrollbar-thumb {
  background: rgba(130, 182, 227, 0.7);
  border-radius: 999px;
}

.image-empty {
  color: #e8f4ff;
  font-weight: 800;
  letter-spacing: 0.08em;
  font-size: 1rem;
}

.question-footer {
  margin-top: 0.8rem;
  display: flex;
  justify-content: center;
  flex-wrap: wrap;
  gap: 0.55rem;
}

.back-btn {
  padding: 0.72rem 1.25rem;
  border-radius: 999px;
  border: 1px solid rgba(255, 255, 255, 0.42);
  background: rgba(8, 25, 54, 0.45);
  color: #fff;
  font-family: 'Outfit', 'Sarabun', sans-serif;
  font-size: 0.95rem;
  font-weight: 800;
  letter-spacing: 0.06em;
  transition: transform 0.16s ease, box-shadow 0.18s ease, background 0.18s ease;
}

.back-btn:hover {
  transform: translateY(-1px) scale(1.03);
  background: rgba(30, 77, 136, 0.66);
  box-shadow: 0 8px 18px rgba(8, 23, 48, 0.35);
}

.back-btn:active {
  transform: translateY(1px) scale(0.98);
}

.back-btn:disabled {
  opacity: 0.45;
  cursor: not-allowed;
  transform: none;
  box-shadow: none;
}

.reset-btn {
  background: rgba(43, 115, 193, 0.55);
}


@media (max-width: 1200px) {
  .icon-top-left { width: 15rem; }
  .icon-bottom-right { width: 11rem; }
  .question-content { padding-top: 4.2rem; }
}

@media (max-width: 768px) {
  .icon-top-left { width: 11rem; top: 0.5rem; left: 0.7rem; }
  .icon-bottom-left { width: 3.6rem; }
  .icon-bottom-right { width: 8rem; }
  .question-content { padding: 3.7rem 0.5rem 0.7rem; }
  .question-pill { padding: 0.48rem 0.9rem; font-size: 0.88rem; }
  .question-panel { gap: 0.55rem; }
  .question-left { padding: 0.72rem; }
  .question-title { font-size: 1rem; }
  .question-prompt { font-size: 0.86rem; }
  .choice-btn { min-height: 56px; padding: 0.5rem 0.56rem; }
  .choice-index { width: 1.75rem; height: 1.75rem; font-size: 0.88rem; }
  .choice-text { font-size: 0.84rem; }
  .question-right { min-height: 180px; padding: 0.55rem; }
  .code-wrap { font-size: 0.78rem; }
  .question-footer { margin-top: 0.45rem; gap: 0.4rem; }
  .back-btn { padding: 0.56rem 0.9rem; font-size: 0.78rem; }
}

@media (max-width: 480px) {
  .question-content { padding-top: 3.5rem; }
  .question-right { min-height: 150px; }
}

@media (max-width: 980px) {
  .question-panel { grid-template-columns: 1fr; }
  .question-right { min-height: 240px; }
}
</style>
