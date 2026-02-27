<template>
  <RouterView />
</template>

<script setup>
import { onBeforeUnmount, onMounted } from 'vue'

let audioCtx = null

const getAudioCtx = async () => {
  const AudioCtx = window.AudioContext || window.webkitAudioContext
  if (!AudioCtx) return null
  if (!audioCtx) audioCtx = new AudioCtx()
  if (audioCtx.state === 'suspended') {
    try {
      await audioCtx.resume()
    } catch {
      return null
    }
  }
  return audioCtx
}

const playTone = async ({ freq, duration, gain, type }) => {
  const ctx = await getAudioCtx()
  if (!ctx || ctx.state !== 'running') return

  const osc = ctx.createOscillator()
  const vol = ctx.createGain()
  osc.type = type
  osc.frequency.value = freq
  vol.gain.value = 0.0001

  osc.connect(vol)
  vol.connect(ctx.destination)

  const now = ctx.currentTime
  vol.gain.exponentialRampToValueAtTime(gain, now + 0.01)
  vol.gain.exponentialRampToValueAtTime(0.0001, now + duration)
  osc.start(now)
  osc.stop(now + duration + 0.01)
}

const isButtonEvent = (event) => {
  const el = event.target instanceof Element ? event.target : null
  const btn = el?.closest('button')
  if (!btn || btn.disabled) return null
  return btn
}

const onHover = async (event) => {
  const btn = isButtonEvent(event)
  if (!btn) return

  const from = event.relatedTarget instanceof Element ? event.relatedTarget.closest('button') : null
  if (from === btn) return

  if (!audioCtx || audioCtx.state !== 'running') return
  playTone({ freq: 520, duration: 0.055, gain: 0.012, type: 'triangle' })
}

const onClick = (event) => {
  const btn = isButtonEvent(event)
  if (!btn) return
  playTone({ freq: 660, duration: 0.085, gain: 0.03, type: 'sine' })
}

onMounted(() => {
  document.addEventListener('mouseover', onHover, true)
  document.addEventListener('click', onClick, true)
})

onBeforeUnmount(() => {
  document.removeEventListener('mouseover', onHover, true)
  document.removeEventListener('click', onClick, true)
})
</script>
