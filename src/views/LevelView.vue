<template>
  <div class="level-screen">
    <div class="level-overlay"></div>

    <button type="button" class="icon-button icon-top-left" @click="router.push('/')">
      <img class="icon-image" src="/img/icon/SIT_30.png" alt="SIT 30" />
    </button>
    <img class="icon icon-bottom-left" src="/img/icon/GOOSE.png" alt="Goose" />
    <img class="icon icon-bottom-right" src="/img/icon/SIT.png" alt="SIT" />

    <div class="level-content">
      <h1 class="level-title">SELECT LEVEL</h1>
      <div class="level-grid">
        <button
          v-for="l in 5"
          :key="l"
          type="button"
          @click="onSelect(l)"
          class="level-button"
        >
          LEVEL {{ l }}
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router'
import { useGameStore } from '../stores/gameStore.js'
import questionsData from '../data/questions.json'

const router = useRouter()
const game = useGameStore()

const onSelect = (level) => {
  game.selectLevel(level, questionsData)
  router.push('/board')
}
</script>

<style scoped>
.level-screen {
  position: fixed;
  inset: 0;
  width: 100vw;
  height: 100vh;
  overflow-x: hidden;
  overflow-y: auto;
  scrollbar-gutter: stable;
  background: center / cover no-repeat url('/img/SIT Festival Template.png');
}

.level-overlay {
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

.icon-top-left {
  top: 0.7rem;
  left: 1rem;
  width: clamp(9rem, 18vw, 19rem);
}

.icon-button {
  position: absolute;
  z-index: 9999;
  background: none;
  border: none;
  padding: 0;
  cursor: pointer;
}

.icon-button .icon-image {
  width: 100%;
  height: auto;
  display: block;
}

.icon-bottom-left {
  bottom: 0;
  left: 0.4rem;
  width: clamp(3.4rem, 8vw, 5rem);
}

.icon-bottom-right {
  right: -0.4rem;
  bottom: 0.4rem;
  width: clamp(8rem, 20vw, 15rem);
}

.level-content {
  position: relative;
  z-index: 3;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: clamp(1.2rem, 2.2vh, 1.9rem);
  width: 100%;
  height: 100%;
  padding: clamp(3.5rem, 6vh, 4.5rem) clamp(0.75rem, 3vw, 1.4rem) clamp(1.5rem, 4vh, 2.1rem);
}

.level-title {
  margin: 0;
  font-family: 'Outfit', 'Sarabun', sans-serif;
  font-size: clamp(1.7rem, 4.2vw, 3.5rem);
  font-weight: 800;
  letter-spacing: 0.14em;
  color: #eef7ff;
  text-shadow: 0 2px 16px rgba(16, 82, 154, 0.75);
}

.level-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(130px, 1fr));
  gap: clamp(0.6rem, 1.5vw, 1rem);
  width: 100%;
  max-width: min(960px, 85vw);
  margin-inline: auto;
}

.level-button {
  width: 100%;
  padding: clamp(0.75rem, 1.5vw, 1rem) clamp(0.9rem, 2vw, 1.15rem);
  border-radius: 1rem;
  border: 1px solid rgba(255, 255, 255, 0.4);
  color: #ffffff;
  font-family: 'Outfit', 'Sarabun', sans-serif;
  font-size: clamp(0.95rem, 2.5vw, 1.25rem);
  font-weight: 700;
  letter-spacing: 0.08em;
  background: linear-gradient(135deg, rgba(255, 255, 255, 0.28), rgba(130, 182, 227, 0.16));
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
  box-shadow:
    0 10px 28px rgba(6, 28, 58, 0.34),
    inset 0 1px 0 rgba(255, 255, 255, 0.45),
    inset 0 -8px 22px rgba(16, 82, 154, 0.14);
  transition: transform 0.2s ease, box-shadow 0.2s ease, border-color 0.2s ease;
}

.level-button:hover {
  transform: translateY(-2px) scale(1.02);
  border-color: rgba(255, 255, 255, 0.65);
  box-shadow:
    0 12px 30px rgba(6, 28, 58, 0.4),
    inset 0 1px 0 rgba(255, 255, 255, 0.55),
    inset 0 -8px 26px rgba(16, 82, 154, 0.22);
}

.level-button:active {
  transform: translateY(1px) scale(0.98);
}


@media (max-width: 1024px) {
  .level-content {
    padding-top: 3.7rem;
    gap: 1rem;
  }
  .level-title {
    font-size: clamp(1.5rem, 5vw, 2.8rem);
  }
}

@media (max-width: 768px) {
  .level-content {
    padding: 3.2rem 0.9rem 1.4rem;
    justify-content: flex-start;
  }
  .level-grid {
    max-width: min(520px, 100%);
  }
  .level-title {
    letter-spacing: 0.08em;
  }
}

@media (max-width: 520px) {
  .level-content {
    padding-top: 2.8rem;
    gap: 0.85rem;
  }
  .level-grid {
    gap: 0.5rem;
  }
  .level-button {
    font-size: 0.9rem;
  }
}
</style>
