<template>
  <div class="home-screen">
    <div class="home-overlay"></div>
    <div class="home-content">
      <button
        type="button"
        @click="router.push('/level')"
        class="start-button"
      >
        START
      </button>
    </div>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router'
const router = useRouter()
</script>

<style scoped>
.home-screen {
  position: fixed;
  inset: 0;
  width: 100vw;
  height: 100vh;
  background: center / cover no-repeat url('/img/21.png');
}

.home-overlay {
  position: absolute;
  inset: 0;
  background:
    radial-gradient(120% 60% at 50% 100%, rgba(130, 182, 227, 0.5) 0%, rgba(130, 182, 227, 0) 65%),
    linear-gradient(to top, rgba(16, 82, 154, 0.68) 0%, rgba(16, 82, 154, 0.12) 50%, rgba(16, 82, 154, 0.28) 100%);
}

.home-content {
  position: relative;
  z-index: 1;
  display: flex;
  align-items: flex-end;
  justify-content: center;
  width: 100%;
  height: 100%;
  padding: 0 1rem max(2rem, 6vh);
}

.start-button {
  min-width: 265px;
  padding: 1.2rem 3.4rem;
  border-radius: 999px;
  border: 1px solid rgba(255, 255, 255, 0.45);
  background: linear-gradient(135deg, rgba(255, 255, 255, 0.33), rgba(130, 182, 227, 0.2));
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
  color: #ffffff;
  font-family: 'Outfit', 'Sarabun', sans-serif;
  font-weight: 800;
  letter-spacing: 0.18em;
  font-size: clamp(1.25rem, 3.1vw, 1.75rem);
  text-shadow: 0 1px 10px rgba(16, 82, 154, 0.8);
  box-shadow:
    0 10px 30px rgba(8, 33, 67, 0.45),
    inset 0 1px 0 rgba(255, 255, 255, 0.5),
    inset 0 -10px 30px rgba(16, 82, 154, 0.2);
  transition: transform 0.2s ease, box-shadow 0.2s ease, background 0.2s ease;
  animation: float-in 0.55s ease-out;
}

.start-button:hover {
  transform: translateY(-2px) scale(1.03);
  box-shadow:
    0 14px 35px rgba(8, 33, 67, 0.52),
    inset 0 1px 0 rgba(255, 255, 255, 0.6),
    inset 0 -14px 36px rgba(16, 82, 154, 0.26);
  background: linear-gradient(135deg, rgba(255, 255, 255, 0.4), rgba(130, 182, 227, 0.26));
}

.start-button:active {
  transform: translateY(1px) scale(0.99);
}

@keyframes float-in {
  0% {
    opacity: 0;
    transform: translateY(18px) scale(0.95);
  }
  100% {
    opacity: 1;
    transform: translateY(0) scale(1);
  }
}

@media (max-width: 640px) {
  .home-content {
    padding-bottom: max(1.5rem, 5vh);
  }

  .start-button {
    min-width: 220px;
    padding: 1rem 2.8rem;
    letter-spacing: 0.14em;
  }
}
</style>
