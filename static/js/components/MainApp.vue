<template>
  <div class="main-app">
    <HeaderView :userData="headerData" />
    
    <div class="content-area">
      <IdentityView 
        v-if="activeTab === 'identity'" 
        @save="onIdentitySaved"
        @update-header="updateHeader"
      />
      <MissionView 
        v-if="activeTab === 'mission'" 
        @save="onMissionSaved"
        @update-header="updateHeader"
      />
      <RoadmapView 
        v-if="activeTab === 'roadmap'" 
        @milestone-change="onMilestoneChange"
      />
    </div>
    
    <div class="footer-nav">
      <button 
        @click="activeTab = 'identity'"
        :class="{ active: activeTab === 'identity' }"
        class="nav-btn"
      >
        Identity
      </button>
      <button 
        @click="activeTab = 'mission'"
        :class="{ active: activeTab === 'mission' }"
        class="nav-btn"
      >
        Mission
      </button>
      <button 
        @click="activeTab = 'roadmap'"
        :class="{ active: activeTab === 'roadmap' }"
        class="nav-btn"
      >
        Roadmap
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import HeaderView from './HeaderView.vue'
import IdentityView from './IdentityView.vue'
import MissionView from './MissionView.vue'
import RoadmapView from './RoadmapView.vue'

const activeTab = ref('identity')
const headerData = reactive({
  name: 'Solopreneur',
  currentGoal: 'Set Goal',
  location: 'Location',
  timeline: 'Q1 2025',
  balance: '€0'
})

onMounted(() => {
  loadUserData()
})

async function loadUserData() {
  try {
    const response = await fetch('/api/user-data')
    if (response.ok) {
      const userData = await response.json()
      Object.assign(headerData, userData)
    }
  } catch (error) {
    console.log('Loading default user data')
  }
}

function updateHeader(data) {
  Object.assign(headerData, data)
}

function onIdentitySaved(identityData) {
  if (identityData.name && identityData.archetype) {
    setTimeout(() => {
      activeTab.value = 'mission'
    }, 1000)
  }
}

function onMissionSaved(missionData) {
  if (missionData.statement && missionData.goal) {
    setTimeout(() => {
      activeTab.value = 'roadmap'
    }, 1000)
  }
}

function onMilestoneChange() {
  loadUserData()
}
</script>

<style scoped>
.main-app {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  background: #f9fafb;
}

.content-area {
  flex: 1;
  min-height: 0;
  overflow-y: auto;
}

.footer-nav {
  background: white;
  padding: 1rem 2rem;
  display: flex;
  justify-content: center;
  gap: 1rem;
  border-top: 1px solid #e5e7eb;
  box-shadow: 0 -4px 20px rgba(0,0,0,0.1);
  position: sticky;
  bottom: 0;
}

.nav-btn {
  padding: 1rem 2rem;
  border: none;
  border-radius: 8px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
  background: #f3f4f6;
  color: #6b7280;
  min-width: 120px;
}

.nav-btn.active {
  background: linear-gradient(135deg, #4ade80 0%, #22d3ee 100%);
  color: white;
  transform: translateY(-2px);
}

.nav-btn:hover:not(.active) {
  background: #e5e7eb;
  transform: translateY(-1px);
}

@media (max-width: 768px) {
  .footer-nav {
    padding: 0.75rem 1rem;
    gap: 0.5rem;
  }
  
  .nav-btn {
    padding: 0.75rem 1rem;
    font-size: 0.9rem;
    min-width: 100px;
  }
}
</style>