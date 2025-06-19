<template>
  <div class="header-bar">
    <div class="brand">MISSIORA</div>
    <div class="user-info" v-if="userData">
      <div class="info-pill">
        <span class="name">{{ userData.name || 'Solopreneur' }}</span>
        <span class="goal">🎯 {{ userData.currentGoal || 'Set Goal' }}</span>
        <span class="location">📍 {{ userData.location || 'Location' }}</span>
        <span class="timeline">🕒 {{ userData.timeline || 'Q1 2025' }}</span>
        <span class="balance">💰 {{ userData.balance || '€0' }}</span>
      </div>
      <div class="avatar">
        <img :src="userData.avatar || '/static/images/default-avatar.svg'" alt="Avatar" />
      </div>
    </div>
  </div>
</template>

<script setup>
import { defineProps } from 'vue'
defineProps({
  userData: {
    type: Object,
    default: () => ({})
  }
})
</script>

<style scoped>
.header-bar {
  background: linear-gradient(135deg, #4ade80 0%, #22d3ee 100%);
  padding: 1rem 2rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
  color: white;
}

.brand {
  font-size: 1.5rem;
  font-weight: bold;
  letter-spacing: 2px;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.info-pill {
  background: rgba(255,255,255,0.2);
  padding: 0.5rem 1rem;
  border-radius: 25px;
  display: flex;
  gap: 1rem;
  backdrop-filter: blur(10px);
}

.info-pill span {
  font-size: 0.9rem;
}

.avatar {
  width: 50px;
  height: 50px;
  border-radius: 50%;
  overflow: hidden;
  border: 3px solid rgba(255,255,255,0.3);
}

.avatar img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

@media (max-width: 768px) {
  .info-pill {
    flex-direction: column;
    gap: 0.5rem;
  }
  
  .info-pill span {
    font-size: 0.8rem;
  }
}
</style>