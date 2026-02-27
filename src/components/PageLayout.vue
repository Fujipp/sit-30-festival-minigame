<template>
  <!-- Shared layout: SIT Festival Template background + corner icons (bleed off edges) -->
  <div class="fixed inset-0 w-screen h-screen overflow-hidden">
    <!-- Background -->
    <div
      class="absolute inset-0 bg-cover bg-center"
      style="background-image: url('/img/SIT Festival Template.png')"
    ></div>

    <!-- SIT_30.png — top-left, bleeds slightly off top -->
    <img
      src="/img/icon/SIT_30.png"
      alt="SIT 30"
      class="absolute z-10 pointer-events-none"
      style="top: -10px; left: 20px; height: 140px"
    />

    <!-- GOOSE.png — bottom-left, bleeds off left edge -->
    <img
      src="/img/icon/GOOSE.png"
      alt="Goose"
      class="absolute z-10 pointer-events-none"
      style="bottom: 0; left: -10px; height: 200px"
    />

    <!-- SIT.png — bottom-right, bleeds off right edge -->
    <img
      src="/img/icon/SIT.png"
      alt="SIT"
      class="absolute z-10 pointer-events-none"
      style="bottom: 10px; right: -10px; height: 140px"
    />

    <!-- Page content -->
    <div class="relative z-20 w-full h-full">
      <slot />
    </div>
  </div>
</template>

<script setup>
// Shared layout used by LevelView, BoardView, QuestionView
</script>
