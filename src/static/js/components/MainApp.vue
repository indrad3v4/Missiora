
<template>
  <div class="main-app">
    <HeaderView :userData="headerData" />
    
    <!-- MR Camera View Body with Tamagotchi Agent -->
    <div class="mr-camera-body">
      <div class="camera-view">
        <video ref="videoElement" autoplay playsinline class="camera-feed"></video>
        <canvas ref="arCanvas" class="ar-overlay"></canvas>
        
        <!-- Tamagotchi Agent Overlay -->
        <div class="tamagotchi-agent" :class="agentState.mood">
          <div class="agent-avatar" :style="agentStyle">
            <div class="agent-body" :class="agentState.evolutionStage">
              <div class="agent-face" :class="agentState.expression"></div>
              <div class="agent-aura" :style="auraStyle"></div>
            </div>
          </div>
          
          <!-- Agent Speech Bubble -->
          <div v-if="agentMessage" class="speech-bubble">
            {{ agentMessage }}
          </div>
          
          <!-- Agent Stats Floating UI -->
          <div class="agent-stats">
            <div class="stat-item">
              <span class="stat-label">Mission Clarity</span>
              <div class="stat-bar">
                <div class="stat-fill" :style="{width: agentState.missionClarity + '%'}"></div>
              </div>
            </div>
            <div class="stat-item">
              <span class="stat-label">Growth Level</span>
              <div class="level-badge">{{ agentState.level }}</div>
            </div>
          </div>
        </div>
        
        <!-- Spatial UI Elements -->
        <div class="spatial-ui">
          <div v-if="currentGoalPanel" class="floating-panel goal-panel">
            <h4>Current Goal</h4>
            <p>{{ headerData.currentGoal }}</p>
          </div>
        </div>
      </div>
    </div>
    
    <!-- Parameter Definition Footer -->
    <div class="parameter-footer">
      <button 
        @click="activeParameterTab = 'identity'"
        :class="{ active: activeParameterTab === 'identity' }"
        class="param-btn"
      >
        🧬 Identity
        <span class="completion-indicator" :class="{ filled: identityComplete }"></span>
      </button>
      <button 
        @click="activeParameterTab = 'mission'"
        :class="{ active: activeParameterTab === 'mission' }"
        class="param-btn"
      >
        🎯 Mission
        <span class="completion-indicator" :class="{ filled: missionComplete }"></span>
      </button>
      <button 
        @click="activeParameterTab = 'roadmap'"
        :class="{ active: activeParameterTab === 'roadmap' }"
        class="param-btn"
      >
        🗺️ Roadmap
        <span class="completion-indicator" :class="{ filled: roadmapComplete }"></span>
      </button>
    </div>
    
    <!-- Parameter Definition Modal -->
    <div v-if="activeParameterTab" class="parameter-modal" @click.self="activeParameterTab = null">
      <div class="modal-content">
        <div class="modal-header">
          <h3>{{ getParameterTitle() }} Parameters</h3>
          <button @click="activeParameterTab = null" class="close-btn">×</button>
        </div>
        
        <IdentityView 
          v-if="activeParameterTab === 'identity'" 
          @save="onIdentityParametersSaved"
          @update-header="updateHeader"
        />
        <MissionView 
          v-if="activeParameterTab === 'mission'" 
          @save="onMissionParametersSaved"
          @update-header="updateHeader"
        />
        <RoadmapView 
          v-if="activeParameterTab === 'roadmap'" 
          @milestone-change="onRoadmapParametersChanged"
        />
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, computed, watch } from 'vue'
import HeaderView from './HeaderView.vue'
import IdentityView from './IdentityView.vue'
import MissionView from './MissionView.vue'
import RoadmapView from './RoadmapView.vue'

const activeParameterTab = ref(null)
const videoElement = ref(null)
const arCanvas = ref(null)

const headerData = reactive({
  name: 'Solopreneur',
  currentGoal: 'Define Your Mission',
  location: 'Location',
  timeline: 'Q1 2025',
  balance: '€0',
  avatar: '/static/images/default-avatar.svg'
})

// Tamagotchi Agent State
const agentState = reactive({
  evolutionStage: 'seed', // seed, sprout, bloom, master
  level: 1,
  missionClarity: 0,
  mood: 'curious', // curious, motivated, focused, accomplished
  expression: 'neutral', // neutral, happy, thinking, excited
  size: 1.0,
  position: { x: 50, y: 60 } // percentage based positioning
})

const agentMessage = ref("Welcome! I'm your mission companion. Let's grow together! 🌱")
const currentGoalPanel = ref(true)

// Parameter completion tracking
const identityComplete = ref(false)
const missionComplete = ref(false)
const roadmapComplete = ref(false)

// Computed styles for agent
const agentStyle = computed(() => ({
  transform: `scale(${agentState.size}) translate(${agentState.position.x}%, ${agentState.position.y}%)`,
  left: agentState.position.x + '%',
  top: agentState.position.y + '%'
}))

const auraStyle = computed(() => {
  const colors = {
    seed: 'radial-gradient(circle, rgba(34, 211, 238, 0.3) 0%, transparent 70%)',
    sprout: 'radial-gradient(circle, rgba(74, 222, 128, 0.4) 0%, transparent 70%)',
    bloom: 'radial-gradient(circle, rgba(251, 191, 36, 0.4) 0%, transparent 70%)',
    master: 'radial-gradient(circle, rgba(147, 51, 234, 0.5) 0%, transparent 70%)'
  }
  return { background: colors[agentState.evolutionStage] }
})

onMounted(async () => {
  await initializeCamera()
  await loadUserData()
  startAgentAnimationLoop()
})

async function initializeCamera() {
  try {
    const stream = await navigator.mediaDevices.getUserMedia({ 
      video: { facingMode: 'environment' } 
    })
    if (videoElement.value) {
      videoElement.value.srcObject = stream
    }
  } catch (error) {
    console.log('Camera not available, using placeholder')
    // Show placeholder background
  }
}

async function loadUserData() {
  try {
    const response = await fetch('/api/user-data')
    if (response.ok) {
      const userData = await response.json()
      Object.assign(headerData, userData)
      updateAgentBasedOnParameters()
    }
  } catch (error) {
    console.log('No user data loaded')
  }
}

function updateAgentBasedOnParameters() {
  // Calculate agent evolution based on parameter completion
  let completionScore = 0
  if (identityComplete.value) completionScore += 33
  if (missionComplete.value) completionScore += 33
  if (roadmapComplete.value) completionScore += 34
  
  agentState.missionClarity = completionScore
  
  // Update evolution stage
  if (completionScore >= 80) {
    agentState.evolutionStage = 'master'
    agentState.level = 4
    agentState.size = 1.3
  } else if (completionScore >= 60) {
    agentState.evolutionStage = 'bloom'
    agentState.level = 3
    agentState.size = 1.2
  } else if (completionScore >= 30) {
    agentState.evolutionStage = 'sprout'
    agentState.level = 2
    agentState.size = 1.1
  } else {
    agentState.evolutionStage = 'seed'
    agentState.level = 1
    agentState.size = 1.0
  }
  
  updateAgentMessage()
}

function updateAgentMessage() {
  const messages = {
    seed: [
      "I'm just beginning to understand you! Tell me more about who you are 🌱",
      "Let's plant the seeds of your mission together! 🌱",
      "I sense potential in you. Help me grow by sharing your identity! 🌱"
    ],
    sprout: [
      "I'm growing! Your mission is becoming clearer to me 🌿",
      "I can feel your purpose taking shape. Keep feeding me insights! 🌿",
      "We're making progress together! What's your next milestone? 🌿"
    ],
    bloom: [
      "Look how far we've come! I can see your vision clearly now 🌸",
      "Your mission is flourishing! I'm here to support your journey 🌸",
      "Together we're creating something beautiful! 🌸"
    ],
    master: [
      "We've achieved mission mastery together! Ready for the next challenge? 🌟",
      "I'm your evolved companion, ready to tackle any goal! 🌟",
      "Our partnership has reached new heights! What shall we conquer next? 🌟"
    ]
  }
  
  const stageMessages = messages[agentState.evolutionStage]
  agentMessage.value = stageMessages[Math.floor(Math.random() * stageMessages.length)]
}

function startAgentAnimationLoop() {
  setInterval(() => {
    // Subtle breathing animation
    agentState.expression = Math.random() > 0.8 ? 'happy' : 'neutral'
    
    // Occasional message updates
    if (Math.random() > 0.95) {
      updateAgentMessage()
    }
  }, 2000)
}

function getParameterTitle() {
  const titles = {
    identity: 'Identity',
    mission: 'Mission',
    roadmap: 'Roadmap'
  }
  return titles[activeParameterTab.value] || ''
}

function updateHeader(data) {
  Object.assign(headerData, data)
}

function onIdentityParametersSaved(identityData) {
  console.log('Identity parameters saved:', identityData)
  identityComplete.value = !!(identityData.name && identityData.archetype)
  updateAgentBasedOnParameters()
  
  if (identityComplete.value) {
    agentMessage.value = "Your identity feeds my growth! I understand you better now 🌱→🌿"
    setTimeout(() => activeParameterTab.value = null, 1500)
  }
}

function onMissionParametersSaved(missionData) {
  console.log('Mission parameters saved:', missionData)
  missionComplete.value = !!(missionData.statement && missionData.goal)
  updateAgentBasedOnParameters()
  
  if (missionComplete.value) {
    agentMessage.value = "Your mission clarity empowers me! I can see our path forward 🌿→🌸"
    setTimeout(() => activeParameterTab.value = null, 1500)
  }
}

function onRoadmapParametersChanged() {
  console.log('Roadmap parameters changed')
  roadmapComplete.value = true // Simplified for demo
  updateAgentBasedOnParameters()
  loadUserData()
  
  agentMessage.value = "Your roadmap completes my evolution! Together we are unstoppable 🌸→🌟"
  setTimeout(() => activeParameterTab.value = null, 1500)
}

// Watch for parameter tab changes to pause agent animations
watch(activeParameterTab, (newTab) => {
  if (newTab) {
    agentState.mood = 'focused'
    agentMessage.value = `Let's define your ${newTab} parameters together!`
  } else {
    agentState.mood = 'curious'
    updateAgentMessage()
  }
})
</script>

<style scoped>
.main-app {
  height: 100vh;
  display: flex;
  flex-direction: column;
  background: #000;
  overflow: hidden;
}

.mr-camera-body {
  flex: 1;
  position: relative;
  overflow: hidden;
}

.camera-view {
  width: 100%;
  height: 100%;
  position: relative;
}

.camera-feed {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.ar-overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  pointer-events: none;
}

.tamagotchi-agent {
  position: absolute;
  width: 120px;
  height: 120px;
  transition: all 0.8s cubic-bezier(0.4, 0, 0.2, 1);
}

.agent-avatar {
  position: relative;
  width: 100%;
  height: 100%;
  transition: transform 0.5s ease;
}

.agent-body {
  width: 80px;
  height: 80px;
  border-radius: 50%;
  position: relative;
  margin: 20px auto;
  transition: all 0.8s ease;
}

.agent-body.seed {
  background: linear-gradient(135deg, #22d3ee 0%, #06b6d4 100%);
  box-shadow: 0 0 20px rgba(34, 211, 238, 0.5);
}

.agent-body.sprout {
  background: linear-gradient(135deg, #4ade80 0%, #22c55e 100%);
  box-shadow: 0 0 25px rgba(74, 222, 128, 0.6);
}

.agent-body.bloom {
  background: linear-gradient(135deg, #fbbf24 0%, #f59e0b 100%);
  box-shadow: 0 0 30px rgba(251, 191, 36, 0.7);
}

.agent-body.master {
  background: linear-gradient(135deg, #9333ea 0%, #7c3aed 100%);
  box-shadow: 0 0 35px rgba(147, 51, 234, 0.8);
}

.agent-face {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: white;
  transition: all 0.3s ease;
}

.agent-face::before {
  content: '👀';
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  font-size: 20px;
}

.agent-face.happy::before {
  content: '😊';
}

.agent-face.thinking::before {
  content: '🤔';
}

.agent-face.excited::before {
  content: '🤩';
}

.agent-aura {
  position: absolute;
  top: -20px;
  left: -20px;
  right: -20px;
  bottom: -20px;
  border-radius: 50%;
  animation: pulse 3s infinite;
}

@keyframes pulse {
  0%, 100% { opacity: 0.5; transform: scale(1); }
  50% { opacity: 0.8; transform: scale(1.1); }
}

.speech-bubble {
  position: absolute;
  top: -60px;
  left: 50%;
  transform: translateX(-50%);
  background: rgba(255, 255, 255, 0.95);
  padding: 0.75rem;
  border-radius: 15px;
  max-width: 200px;
  font-size: 0.8rem;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
  backdrop-filter: blur(10px);
}

.speech-bubble::after {
  content: '';
  position: absolute;
  top: 100%;
  left: 50%;
  transform: translateX(-50%);
  border: 8px solid transparent;
  border-top-color: rgba(255, 255, 255, 0.95);
}

.agent-stats {
  position: absolute;
  top: 140px;
  left: 50%;
  transform: translateX(-50%);
  background: rgba(0, 0, 0, 0.7);
  padding: 0.5rem;
  border-radius: 10px;
  min-width: 150px;
  backdrop-filter: blur(10px);
}

.stat-item {
  margin-bottom: 0.5rem;
  color: white;
  font-size: 0.7rem;
}

.stat-label {
  display: block;
  margin-bottom: 0.2rem;
}

.stat-bar {
  height: 4px;
  background: rgba(255, 255, 255, 0.3);
  border-radius: 2px;
  overflow: hidden;
}

.stat-fill {
  height: 100%;
  background: linear-gradient(90deg, #4ade80, #22d3ee);
  transition: width 0.8s ease;
}

.level-badge {
  background: linear-gradient(135deg, #4ade80, #22d3ee);
  color: white;
  padding: 0.2rem 0.5rem;
  border-radius: 10px;
  font-weight: bold;
  display: inline-block;
}

.spatial-ui {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  pointer-events: none;
}

.floating-panel {
  position: absolute;
  background: rgba(255, 255, 255, 0.9);
  padding: 1rem;
  border-radius: 12px;
  backdrop-filter: blur(10px);
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15);
  pointer-events: auto;
}

.goal-panel {
  top: 20px;
  right: 20px;
  max-width: 200px;
}

.parameter-footer {
  background: rgba(0, 0, 0, 0.8);
  backdrop-filter: blur(10px);
  padding: 1rem;
  display: flex;
  justify-content: center;
  gap: 1rem;
}

.param-btn {
  background: rgba(255, 255, 255, 0.1);
  border: 2px solid rgba(255, 255, 255, 0.3);
  color: white;
  padding: 0.75rem 1.5rem;
  border-radius: 25px;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-weight: 600;
}

.param-btn:hover {
  background: rgba(255, 255, 255, 0.2);
  transform: translateY(-2px);
}

.param-btn.active {
  background: linear-gradient(135deg, #4ade80 0%, #22d3ee 100%);
  border-color: transparent;
  transform: translateY(-2px);
}

.completion-indicator {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.3);
  transition: all 0.3s ease;
}

.completion-indicator.filled {
  background: #4ade80;
  box-shadow: 0 0 10px rgba(74, 222, 128, 0.6);
}

.parameter-modal {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.8);
  backdrop-filter: blur(5px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.modal-content {
  background: white;
  border-radius: 20px;
  max-width: 600px;
  max-height: 80vh;
  overflow-y: auto;
  margin: 2rem;
  box-shadow: 0 20px 50px rgba(0, 0, 0, 0.3);
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.5rem 2rem;
  border-bottom: 1px solid #e5e7eb;
}

.modal-header h3 {
  margin: 0;
  font-size: 1.5rem;
  background: linear-gradient(135deg, #4ade80 0%, #22d3ee 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.close-btn {
  background: none;
  border: none;
  font-size: 2rem;
  cursor: pointer;
  color: #6b7280;
  padding: 0;
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  transition: all 0.2s ease;
}

.close-btn:hover {
  background: #f3f4f6;
  color: #374151;
}
</style>
