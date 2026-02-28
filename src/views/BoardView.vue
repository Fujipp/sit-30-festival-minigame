<template>
  <div class="board-screen">
    <div class="board-overlay"></div>

    <img class="icon icon-top-left" src="/img/icon/SIT_30.png" alt="SIT 30" />
    <img class="icon icon-bottom-left" src="/img/icon/GOOSE.png" alt="Goose" />
    <img class="icon icon-bottom-right" src="/img/icon/SIT.png" alt="SIT" />

    <div class="board-content">
      <div class="board-header">
        <h1 class="board-title">LEVEL {{ game.currentLevel }} QUESTIONS</h1>
      </div>

      <div class="question-grid">
        <button
          v-for="(q, index) in game.currentQuestions"
          :key="q.id"
          type="button"
          class="question-button"
          @click="onOpen(index)"
        >
          {{ toQuestionLabel(index, q.id) }}
        </button>
      </div>

      <div class="board-footer">
        <button type="button" class="board-back" @click="router.push('/level')">BACK</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useGameStore } from '../stores/gameStore.js'

const router = useRouter()
const game = useGameStore()

onMounted(() => {
  if (!game.currentQuestions.length) {
    router.replace('/level')
  }
})

const onOpen = (index) => {
  game.openQuestion(index)
  router.push('/question')
}

const toQuestionLabel = (index, id) => {
  if (typeof id === 'string') {
    const qCode = id.match(/Q\d{2}$/i)
    if (qCode) return qCode[0].toUpperCase()
  }
  return `Q${String(index + 1).padStart(2, '0')}`
}
</script>

<style scoped>
.board-screen {
  position: fixed;
  inset: 0;
  width: 100vw;
  height: 100vh;
  overflow: hidden;
  background: center / cover no-repeat url('/img/SIT Festival Template.png');
}

.board-overlay {
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

.board-content {
  position: relative;
  z-index: 3;
  display: flex;
  flex-direction: column;
  width: 100%;
  height: 100%;
  padding: 4.7rem clamp(0.8rem, 2.2vw, 1.6rem) 1.1rem;
}

.board-header {
  display: flex;
  justify-content: center;
  align-items: center;
  margin-bottom: 1.2rem;
}

.board-title {
  margin: 0;
  text-align: center;
  color: #edf6ff;
  text-shadow: 0 2px 16px rgba(16, 82, 154, 0.7);
  font-family: 'Outfit', 'Sarabun', sans-serif;
  font-size: clamp(1.15rem, 3vw, 2rem);
  letter-spacing: 0.08em;
  font-weight: 800;
}

.question-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(170px, 1fr));
  gap: clamp(0.75rem, 1.15vw, 1rem);
  width: 100%;
  margin: 0;
  padding: 0.25rem 0.2rem;
  align-content: start;
  flex: 1;
}

.question-button {
  min-height: clamp(86px, 10.5vw, 118px);
  border-radius: 1.05rem;
  border: 1px solid rgba(255, 255, 255, 0.36);
  color: #ffffff;
  font-family: 'Outfit', 'Sarabun', sans-serif;
  font-size: clamp(1.18rem, 2.4vw, 1.68rem);
  font-weight: 800;
  letter-spacing: 0.07em;
  background: linear-gradient(135deg, rgba(255, 255, 255, 0.29), rgba(130, 182, 227, 0.18));
  backdrop-filter: blur(11px);
  -webkit-backdrop-filter: blur(11px);
  box-shadow:
    0 9px 24px rgba(6, 28, 58, 0.29),
    inset 0 1px 0 rgba(255, 255, 255, 0.46),
    inset 0 -8px 20px rgba(16, 82, 154, 0.16);
  transition: transform 0.2s ease, box-shadow 0.2s ease, border-color 0.2s ease;
}

.question-button:hover {
  transform: translateY(-2px) scale(1.02);
  border-color: rgba(255, 255, 255, 0.6);
  box-shadow:
    0 12px 28px rgba(6, 28, 58, 0.4),
    inset 0 1px 0 rgba(255, 255, 255, 0.58),
    inset 0 -9px 22px rgba(16, 82, 154, 0.22);
}

.board-footer {
  display: flex;
  justify-content: center;
  margin-top: auto;
  padding-top: 1rem;
}

.board-back {
  padding: 0.62rem 1.25rem;
  border-radius: 999px;
  border: 1px solid rgba(255, 255, 255, 0.46);
  color: #ffffff;
  background: linear-gradient(135deg, rgba(255, 255, 255, 0.26), rgba(130, 182, 227, 0.14));
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
  font-family: 'Outfit', 'Sarabun', sans-serif;
  font-size: 0.92rem;
  font-weight: 700;
  letter-spacing: 0.08em;
  box-shadow: 0 8px 22px rgba(7, 30, 60, 0.3);
}


@media (max-width: 1024px) {
  .icon-top-left { width: 15rem; }
  .icon-bottom-right { width: 11rem; }
  .board-content { padding-top: 4.2rem; }
  .question-button { min-height: 78px; }
}

@media (max-width: 768px) {
  .icon-top-left { width: 11rem; top: 0.5rem; left: 0.7rem; }
  .icon-bottom-left { width: 3.6rem; }
  .icon-bottom-right { width: 8rem; }
  .board-content { padding: 3.7rem 0.55rem 0.8rem; }
  .board-title { font-size: 1.05rem; }
  .question-grid { gap: 0.52rem; }
  .question-button { min-height: 68px; font-size: 0.98rem; }
}

@media (max-width: 480px) {
  .question-grid { grid-template-columns: repeat(2, minmax(0, 1fr)); }
  .board-back { font-size: 0.75rem; padding: 0.45rem 0.78rem; }
}

@media (max-width: 900px) {
  .board-content { padding-top: 4.4rem; }
  .question-grid { grid-template-columns: repeat(auto-fit, minmax(140px, 1fr)); }
}

@media (max-width: 640px) {
  .board-content { padding-top: 4.1rem; }
  .board-header { margin-bottom: 0.85rem; }
  .board-back { font-size: 0.82rem; padding: 0.5rem 0.9rem; }
  .question-grid { grid-template-columns: repeat(2, minmax(0, 1fr)); }
}
</style>
