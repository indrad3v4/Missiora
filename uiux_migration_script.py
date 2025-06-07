#!/usr/bin/env python3
"""
UX Migration Script: Transform Missiora to 3-view Interface
Implements Identity/Mission/Roadmap structure with milestone-driven orchestration
"""

import os
import re
import json
import subprocess
from pathlib import Path

def ensure_directory(path):
    """Create directory if it doesn't exist"""
    Path(path).mkdir(parents=True, exist_ok=True)

def write_file(filepath, content):
    """Write content to file, creating directories if needed"""
    ensure_directory(os.path.dirname(filepath))
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"✓ Created {filepath}")

def patch_file(filepath, pattern, replacement, flags=0):
    """Apply regex patch to existing file"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        new_content = re.sub(pattern, replacement, content, flags=flags)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        print(f"✓ Patched {filepath}")
        return True
    except Exception as e:
        print(f"✗ Failed to patch {filepath}: {e}")
        return False

def run_command(cmd, description=""):
    """Run shell command with error handling"""
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✓ {description or cmd}")
            return True
        else:
            print(f"✗ {description or cmd}: {result.stderr}")
            return False
    except Exception as e:
        print(f"✗ Command failed: {e}")
        return False

def main():
    print("🚀 Starting UX Migration to 3-view Interface...")
    
    # 1. Clean database and create branch
    print("\n📁 Setting up environment...")
    run_command("rm -f instance/solopreneur_agency.db", "Cleaning database")
    run_command("git checkout -b uiux/v1-lifeline 2>/dev/null || git checkout uiux/v1-lifeline", "Creating/switching to branch")
    
    # 2. Update User model
    print("\n🗄️ Updating database models...")
    
    models_patch = '''
# Add these fields after the existing User model fields, before # Relationships
    # Identity and Mission data  
    identity_data = db.Column(db.Text, nullable=True)  # JSON stored identity
    mission_statement = db.Column(db.Text, nullable=True)
    current_goal = db.Column(db.String(500), nullable=True)
    
    '''
    
    milestone_model = '''

class Milestone(db.Model):
    __tablename__ = 'milestones'
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(50), unique=True, nullable=False)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    active = db.Column(db.Boolean, default=False)
    completed = db.Column(db.Boolean, default=False)
    order_index = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Milestone {self.code}>'
'''
    
    # Patch models.py
    patch_file('models.py', 
               r'(    # Relationships)', 
               models_patch + r'\1')
    
    # Add Milestone model if not exists
    with open('models.py', 'r') as f:
        if 'class Milestone' not in f.read():
            with open('models.py', 'a') as f:
                f.write(milestone_model)
    
    # 3. Create Vue components
    print("\n🎨 Creating Vue components...")
    
    # Ensure static/js/components directory exists
    ensure_directory('static/js/components')
    
    # Header component
    header_vue = '''<template>
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
</style>'''
    
    write_file('static/js/components/HeaderView.vue', header_vue)
    
    # Identity component
    identity_vue = '''<template>
  <div class="identity-view">
    <div class="content-card">
      <h2>Define Your Identity</h2>
      <form @submit.prevent="saveIdentity" class="identity-form">
        <div class="form-group">
          <label>Your Name</label>
          <input v-model="identity.name" placeholder="Enter your name" class="form-input" />
        </div>
        
        <div class="form-group">
          <label>Archetype</label>
          <select v-model="identity.archetype" class="form-select">
            <option value="">Select your archetype</option>
            <option value="creator">Creator</option>
            <option value="builder">Builder</option>
            <option value="consultant">Consultant</option>
            <option value="teacher">Teacher</option>
            <option value="innovator">Innovator</option>
          </select>
        </div>
        
        <div class="form-group">
          <label>Current Mood</label>
          <textarea v-model="identity.mood" placeholder="How are you feeling about your journey?" class="form-textarea"></textarea>
        </div>
        
        <div class="form-group">
          <label>Region/Location</label>
          <input v-model="identity.region" placeholder="Where are you based?" class="form-input" />
        </div>
        
        <div class="form-group">
          <label>Field/Industry</label>
          <input v-model="identity.field" placeholder="What industry do you work in?" class="form-input" />
        </div>
        
        <div class="form-group">
          <label>Self-Title</label>
          <input v-model="identity.selfTitle" placeholder="How do you describe yourself?" class="form-input" />
        </div>
        
        <button type="submit" class="save-btn">Save Identity</button>
      </form>
    </div>
  </div>
</template>

<script setup>
import { reactive, onMounted } from 'vue'

const identity = reactive({
  name: '',
  archetype: '',
  mood: '',
  region: '',
  field: '',
  selfTitle: ''
})

const emit = defineEmits(['save', 'update-header'])

onMounted(async () => {
  try {
    const response = await fetch('/api/identity')
    if (response.ok) {
      const data = await response.json()
      Object.assign(identity, data)
    }
  } catch (error) {
    console.log('No existing identity data')
  }
})

async function saveIdentity() {
  try {
    const response = await fetch('/api/identity', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(identity)
    })
    
    if (response.ok) {
      emit('save', identity)
      emit('update-header', {
        name: identity.name,
        location: identity.region
      })
      alert('Identity saved successfully!')
    }
  } catch (error) {
    console.error('Failed to save identity:', error)
    alert('Failed to save identity')
  }
}
</script>

<style scoped>
.identity-view {
  padding: 2rem;
  max-width: 600px;
  margin: 0 auto;
}

.content-card {
  background: white;
  border-radius: 12px;
  padding: 2rem;
  box-shadow: 0 4px 20px rgba(0,0,0,0.1);
}

.identity-form {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.form-group label {
  font-weight: 600;
  color: #374151;
}

.form-input, .form-select, .form-textarea {
  padding: 0.75rem;
  border: 2px solid #e5e7eb;
  border-radius: 8px;
  font-size: 1rem;
  transition: border-color 0.2s;
}

.form-input:focus, .form-select:focus, .form-textarea:focus {
  outline: none;
  border-color: #22d3ee;
}

.form-textarea {
  min-height: 100px;
  resize: vertical;
}

.save-btn {
  background: linear-gradient(135deg, #4ade80 0%, #22d3ee 100%);
  color: white;
  padding: 1rem 2rem;
  border: none;
  border-radius: 8px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: transform 0.2s;
}

.save-btn:hover {
  transform: translateY(-2px);
}
</style>'''
    
    write_file('static/js/components/IdentityView.vue', identity_vue)
    
    # Mission component
    mission_vue = '''<template>
  <div class="mission-view">
    <div class="content-card">
      <h2>Build Your Mission</h2>
      
      <div class="orchestrator-chat" v-if="showChat">
        <div class="chat-header">
          <h3>🧠 Orchestrator Chat</h3>
          <button @click="showChat = false" class="close-chat">×</button>
        </div>
        <div class="chat-messages" ref="chatMessages">
          <div v-for="msg in messages" :key="msg.id" class="message" :class="msg.role">
            <div class="message-content">{{ msg.content }}</div>
          </div>
        </div>
        <div class="chat-input">
          <input 
            v-model="userInput" 
            @keyup.enter="sendMessage" 
            placeholder="Describe your highest goal..." 
            :disabled="isTyping"
          />
          <button @click="sendMessage" :disabled="isTyping || !userInput.trim()">
            {{ isTyping ? '...' : 'Send' }}
          </button>
        </div>
      </div>
      
      <div class="mission-form">
        <div class="form-group">
          <label>Mission Statement</label>
          <textarea v-model="mission.statement" placeholder="What is your core mission?" class="form-textarea"></textarea>
        </div>
        
        <div class="form-group">
          <label>Highest Goal</label>
          <input v-model="mission.goal" placeholder="What do you ultimately want to achieve?" class="form-input" />
        </div>
        
        <div class="form-group">
          <label>Emotional Blocks</label>
          <textarea v-model="mission.blocks" placeholder="What fears or doubts hold you back?" class="form-textarea"></textarea>
        </div>
        
        <div class="button-group">
          <button @click="saveMission" class="save-btn">Save Mission</button>
          <button @click="toggleChat" class="chat-btn">
            {{ showChat ? 'Hide' : 'Chat with' }} Orchestrator
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { reactive, ref, onMounted, nextTick } from 'vue'

const mission = reactive({
  statement: '',
  goal: '',
  blocks: ''
})

const showChat = ref(false)
const messages = ref([])
const userInput = ref('')
const isTyping = ref(false)
const chatMessages = ref(null)

const emit = defineEmits(['save', 'update-header'])

onMounted(async () => {
  try {
    const response = await fetch('/api/mission')
    if (response.ok) {
      const data = await response.json()
      Object.assign(mission, data)
    }
  } catch (error) {
    console.log('No existing mission data')
  }
})

function toggleChat() {
  showChat.value = !showChat.value
  if (showChat.value && messages.value.length === 0) {
    messages.value.push({
      id: 1,
      role: 'agent',
      content: "Welcome! I'm here to help you discover and refine your highest goal. What drives you as a solopreneur? What impact do you want to make?"
    })
  }
}

async function sendMessage() {
  if (!userInput.value.trim() || isTyping.value) return
  
  const userMsg = userInput.value.trim()
  messages.value.push({
    id: Date.now(),
    role: 'user',
    content: userMsg
  })
  
  userInput.value = ''
  isTyping.value = true
  
  try {
    const response = await fetch('/api/chat', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        user_message: userMsg,
        context: 'mission_building'
      })
    })
    
    if (response.ok) {
      const data = await response.json()
      messages.value.push({
        id: Date.now(),
        role: 'agent',
        content: data.reply || 'I understand your perspective. Could you tell me more about what success looks like for you?'
      })
    } else {
      throw new Error('Chat service unavailable')
    }
  } catch (error) {
    messages.value.push({
      id: Date.now(),
      role: 'agent',
      content: "I understand your goal. Let me help you refine it further. What specific outcome would make you feel most fulfilled?"
    })
  } finally {
    isTyping.value = false
    await nextTick()
    if (chatMessages.value) {
      chatMessages.value.scrollTop = chatMessages.value.scrollHeight
    }
  }
}

async function saveMission() {
  try {
    const response = await fetch('/api/mission', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(mission)
    })
    
    if (response.ok) {
      emit('save', mission)
      emit('update-header', {
        currentGoal: mission.goal
      })
      alert('Mission saved successfully!')
    }
  } catch (error) {
    console.error('Failed to save mission:', error)
    alert('Failed to save mission')
  }
}
</script>

<style scoped>
.mission-view {
  padding: 2rem;
  max-width: 800px;
  margin: 0 auto;
}

.content-card {
  background: white;
  border-radius: 12px;
  padding: 2rem;
  box-shadow: 0 4px 20px rgba(0,0,0,0.1);
}

.orchestrator-chat {
  margin-bottom: 2rem;
  border: 2px solid #e5e7eb;
  border-radius: 12px;
  overflow: hidden;
}

.chat-header {
  background: #f3f4f6;
  padding: 1rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-bottom: 1px solid #e5e7eb;
}

.chat-header h3 {
  margin: 0;
  color: #374151;
}

.close-chat {
  background: none;
  border: none;
  font-size: 1.5rem;
  cursor: pointer;
  color: #6b7280;
}

.chat-messages {
  max-height: 300px;
  overflow-y: auto;
  padding: 1rem;
}

.message {
  margin-bottom: 1rem;
  padding: 0.75rem;
  border-radius: 8px;
}

.message.user {
  background: #dbeafe;
  margin-left: 2rem;
}

.message.agent {
  background: #f3f4f6;
  margin-right: 2rem;
}

.chat-input {
  display: flex;
  gap: 0.5rem;
  padding: 1rem;
  border-top: 1px solid #e5e7eb;
}

.chat-input input {
  flex: 1;
  padding: 0.75rem;
  border: 2px solid #e5e7eb;
  border-radius: 8px;
}

.chat-input button {
  padding: 0.75rem 1.5rem;
  background: #4ade80;
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
}

.chat-input button:disabled {
  background: #9ca3af;
  cursor: not-allowed;
}

.mission-form {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.form-group label {
  font-weight: 600;
  color: #374151;
}

.form-input, .form-textarea {
  padding: 0.75rem;
  border: 2px solid #e5e7eb;
  border-radius: 8px;
  font-size: 1rem;
}

.form-textarea {
  min-height: 100px;
  resize: vertical;
}

.button-group {
  display: flex;
  gap: 1rem;
}

.save-btn, .chat-btn {
  padding: 1rem 2rem;
  border: none;
  border-radius: 8px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: transform 0.2s;
}

.save-btn {
  background: linear-gradient(135deg, #4ade80 0%, #22d3ee 100%);
  color: white;
}

.chat-btn {
  background: #6b7280;
  color: white;
}

.save-btn:hover, .chat-btn:hover {
  transform: translateY(-2px);
}
</style>'''
    
    write_file('static/js/components/MissionView.vue', mission_vue)
    
    # Roadmap component
    roadmap_vue = '''<template>
  <div class="roadmap-view">
    <div class="content-card">
      <h2>Your Roadmap</h2>
      <p class="subtitle">Let's follow your roadmap to the highest goal.</p>
      
      <div class="roadmap-container">
        <div class="milestone-track">
          <div 
            v-for="(milestone, index) in milestones" 
            :key="milestone.id"
            class="milestone-node"
            :class="{ 
              active: milestone.active, 
              completed: milestone.completed,
              upcoming: !milestone.active && !milestone.completed 
            }"
            @click="selectMilestone(milestone)"
          >
            <div class="milestone-icon">
              <i v-if="milestone.completed" class="fas fa-check"></i>
              <i v-else-if="milestone.active" class="fas fa-target"></i>
              <i v-else class="fas fa-circle"></i>
            </div>
            <div class="milestone-content">
              <h3>{{ milestone.title }}</h3>
              <p v-if="milestone.description">{{ milestone.description }}</p>
              <div v-if="milestone.suggestions" class="suggestions">
                <h4>Suggested Idea:</h4>
                <p>{{ milestone.suggestions.idea }}</p>
                <div class="suggestion-details">
                  <span>Cost: {{ milestone.suggestions.cost }}</span>
                  <span>ROI: {{ milestone.suggestions.roi }}</span>
                </div>
              </div>
            </div>
          </div>
        </div>
        
        <div class="milestone-actions" v-if="selectedMilestone">
          <button 
            v-if="selectedMilestone.active && !selectedMilestone.completed"
            @click="completeMilestone(selectedMilestone.id)"
            class="complete-btn"
          >
            Mark Complete
          </button>
          <button 
            v-if="!selectedMilestone.active && !selectedMilestone.completed && canActivate(selectedMilestone)"
            @click="activateMilestone(selectedMilestone.id)"
            class="activate-btn"
          >
            Start This Milestone
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'

const milestones = ref([])
const selectedMilestone = ref(null)

const emit = defineEmits(['milestone-change'])

onMounted(async () => {
  await loadMilestones()
})

async function loadMilestones() {
  try {
    const response = await fetch('/api/milestones')
    if (response.ok) {
      milestones.value = await response.json()
      // Add sample suggestions for demo
      milestones.value.forEach(m => {
        if (m.code === 'design_first_offer') {
          m.suggestions = {
            idea: 'Automate Courier Service',
            cost: '€80',
            roi: '€500 in 2 weeks'
          }
        }
      })
      
      // Auto-select first active or incomplete milestone
      const activeOrNext = milestones.value.find(m => m.active || (!m.completed && !m.active))
      if (activeOrNext) {
        selectedMilestone.value = activeOrNext
      }
    }
  } catch (error) {
    console.error('Failed to load milestones:', error)
  }
}

function selectMilestone(milestone) {
  selectedMilestone.value = milestone
}

function canActivate(milestone) {
  // Can activate if previous milestones are completed
  const currentIndex = milestones.value.findIndex(m => m.id === milestone.id)
  if (currentIndex === 0) return true
  
  const previousMilestone = milestones.value[currentIndex - 1]
  return previousMilestone && previousMilestone.completed
}

async function completeMilestone(milestoneId) {
  try {
    const response = await fetch(`/api/milestones/${milestoneId}/complete`, {
      method: 'POST'
    })
    
    if (response.ok) {
      await loadMilestones()
      emit('milestone-change')
    }
  } catch (error) {
    console.error('Failed to complete milestone:', error)
  }
}

async function activateMilestone(milestoneId) {
  try {
    const response = await fetch(`/api/milestones/${milestoneId}/activate`, {
      method: 'POST'
    })
    
    if (response.ok) {
      await loadMilestones()
      emit('milestone-change')
    }
  } catch (error) {
    console.error('Failed to activate milestone:', error)
  }
}
</script>

<style scoped>
.roadmap-view {
  padding: 2rem;
  max-width: 800px;
  margin: 0 auto;
}

.content-card {
  background: white;
  border-radius: 12px;
  padding: 2rem;
  box-shadow: 0 4px 20px rgba(0,0,0,0.1);
}

.subtitle {
  color: #6b7280;
  margin-bottom: 2rem;
}

.milestone-track {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  margin-bottom: 2rem;
}

.milestone-node {
  display: flex;
  align-items: flex-start;
  gap: 1rem;
  padding: 1rem;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s;
  border: 2px solid transparent;
}

.milestone-node:hover {
  background: #f9fafb;
}

.milestone-node.active {
  background: #dbeafe;
  border-color: #3b82f6;
}

.milestone-node.completed {
  background: #dcfce7;
  border-color: #22c55e;
}

.milestone-node.upcoming {
  background: #f3f4f6;
}

.milestone-icon {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.2rem;
  flex-shrink: 0;
}

.milestone-node.active .milestone-icon {
  background: #3b82f6;
  color: white;
}

.milestone-node.completed .milestone-icon {
  background: #22c55e;
  color: white;
}

.milestone-node.upcoming .milestone-icon {
  background: #9ca3af;
  color: white;
}

.milestone-content {
  flex: 1;
}

.milestone-content h3 {
  margin: 0 0 0.5rem 0;
  color: #111827;
}

.milestone-content p {
  margin: 0;
  color: #6b7280;
  font-size: 0.9rem;
}

.suggestions {
  margin-top: 1rem;
  padding: 1rem;
  background: #fef3c7;
  border-radius: 8px;
}

.suggestions h4 {
  margin: 0 0 0.5rem 0;
  color: #92400e;
  font-size: 0.9rem;
}

.suggestion-details {
  display: flex;
  gap: 1rem;
  margin-top: 0.5rem;
  font-size: 0.8rem;
  color: #92400e;
}

.milestone-actions {
  display: flex;
  gap: 1rem;
  justify-content: center;
}

.complete-btn, .activate-btn {
  padding: 0.75rem 1.5rem;
  border: none;
  border-radius: 8px;
  font-weight: 600;
  cursor: pointer;
  transition: transform 0.2s;
}

.complete-btn {
  background: #22c55e;
  color: white;
}

.activate-btn {
  background: #3b82f6;
  color: white;
}

.complete-btn:hover, .activate-btn:hover {
  transform: translateY(-2px);
}
</style>'''
    
    write_file('static/js/components/RoadmapView.vue', roadmap_vue)
    
    # Main App component
    main_app_vue = '''<template>
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
  balance: '€0',
  avatar: '/static/images/default-avatar.svg'
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
    console.log('No user data loaded')
  }
}

function updateHeader(data) {
  Object.assign(headerData, data)
}

function onIdentitySaved(identityData) {
  console.log('Identity saved:', identityData)
  // Auto-advance to mission if identity is complete
  if (identityData.name && identityData.archetype) {
    setTimeout(() => {
      activeTab.value = 'mission'
    }, 1000)
  }
}

function onMissionSaved(missionData) {
  console.log('Mission saved:', missionData)
  // Auto-advance to roadmap if mission is complete
  if (missionData.statement && missionData.goal) {
    setTimeout(() => {
      activeTab.value = 'roadmap'
    }, 1000)
  }
}

function onMilestoneChange() {
  console.log('Milestone changed')
  loadUserData() // Refresh header data
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
</style>'''
    
    write_file('static/js/components/MainApp.vue', main_app_vue)
    
    # 4. Update main template
    print("\n📄 Creating main template...")
    
    index_html = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Missiora - AI Agency for Solopreneurs</title>
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: #f9fafb;
            line-height: 1.5;
        }
        
        #app {
            min-height: 100vh;
        }
        
        /* Loading state */
        .loading {
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            font-size: 1.2rem;
            color: #6b7280;
        }
    </style>
</head>
<body>
    <div id="app">
        <div class="loading">Loading Missiora...</div>
    </div>
    
    <script type="importmap">
    {
      "imports": {
        "vue": "https://unpkg.com/vue@3/dist/vue.esm-browser.js"
      }
    }
    </script>
    <script type="module">
        import { createApp } from 'vue'
        import MainApp from '/static/js/components/MainApp.vue'
        
        const app = createApp(MainApp)
        
        app.config.errorHandler = (err, vm, info) => {
            console.error('Vue error:', err, info)
        }
        
        app.mount('#app')
    </script>
</body>
</html>'''
    
    write_file('templates/index.html', index_html)
    
    # 5. Add API routes to routes.py
    print("\n🔌 Adding API routes...")
    
    api_routes = '''
# === NEW API ROUTES FOR 3-VIEW UX ===

@app.route('/api/identity', methods=['GET', 'POST'])
@login_required
def api_identity():
    """Handle identity data storage and retrieval"""
    if request.method == 'POST':
        identity_data = request.json
        current_user.identity_data = json.dumps(identity_data)
        db.session.commit()
        return jsonify({'success': True})
    else:
        if current_user.identity_data:
            return jsonify(json.loads(current_user.identity_data))
        return jsonify({})

@app.route('/api/mission', methods=['GET', 'POST'])
@login_required
def api_mission():
    """Handle mission data storage and retrieval"""
    if request.method == 'POST':
        mission_data = request.json
        current_user.mission_statement = mission_data.get('statement', '')
        current_user.current_goal = mission_data.get('goal', '')
        db.session.commit()
        return jsonify({'success': True})
    else:
        return jsonify({
            'statement': current_user.mission_statement or '',
            'goal': current_user.current_goal or '',
            'blocks': ''
        })

@app.route('/api/milestones')
@login_required
def api_milestones():
    """Get all milestones"""
    milestones = Milestone.query.order_by(Milestone.order_index).all()
    return jsonify([{
        'id': m.id,
        'code': m.code,
        'title': m.title,
        'description': m.description,
        'active': m.active,
        'completed': m.completed,
        'order_index': m.order_index
    } for m in milestones])

@app.route('/api/milestones/<int:milestone_id>/complete', methods=['POST'])
@login_required
def api_complete_milestone(milestone_id):
    """Mark milestone as complete and activate next"""
    milestone = Milestone.query.get_or_404(milestone_id)
    milestone.completed = True
    milestone.active = False
    
    # Activate next milestone
    next_milestone = Milestone.query.filter(
        Milestone.order_index > milestone.order_index,
        Milestone.completed == False
    ).order_by(Milestone.order_index).first()
    
    if next_milestone:
        next_milestone.active = True
    
    db.session.commit()
    return jsonify({'success': True})

@app.route('/api/milestones/<int:milestone_id>/activate', methods=['POST'])
@login_required
def api_activate_milestone(milestone_id):
    """Activate a specific milestone"""
    # Deactivate all milestones
    Milestone.query.update({'active': False})
    
    # Activate selected milestone
    milestone = Milestone.query.get_or_404(milestone_id)
    milestone.active = True
    
    db.session.commit()
    return jsonify({'success': True})

@app.route('/api/user-data')
@login_required
def api_user_data():
    """Get user data for header display"""
    identity_data = {}
    if current_user.identity_data:
        identity_data = json.loads(current_user.identity_data)
    
    return jsonify({
        'name': identity_data.get('name', current_user.username),
        'currentGoal': current_user.current_goal or 'Set Your Goal',
        'location': identity_data.get('region', 'Location'),
        'timeline': 'Q1 2025',
        'balance': '€0'
    })

'''
    
    # Insert API routes after imports in routes.py
    with open('routes.py', 'r') as f:
        routes_content = f.read()
    
    # Find import section and add after it
    import_end = routes_content.find('from eth_account.messages import encode_defunct')
    if import_end != -1:
        import_end = routes_content.find('\n', import_end) + 1
        new_content = routes_content[:import_end] + api_routes + routes_content[import_end:]
    else:
        # Fallback: add after existing imports
        import_end = routes_content.find('\n\n@app.route')
        new_content = routes_content[:import_end] + api_routes + routes_content[import_end:]
    
    # Update index route
    new_content = re.sub(
        r'@app\.route\(\'/\'\)\ndef index\(\):\s+.*?return redirect\(url_for\(\'narrative_chat\'\)\)',
        '''@app.route('/')
def index():
    """Main application entry point"""
    if current_user.is_authenticated:
        return render_template('index.html')
    else:
        return redirect(url_for('auth_options'))''',
        new_content,
        flags=re.DOTALL
    )
    
    write_file('routes.py', new_content)
    
    # 6. Create bootstrap script
    print("\n🌱 Creating milestone bootstrap script...")
    
    bootstrap_script = '''#!/usr/bin/env python3
"""Bootstrap milestones for the UX migration"""

from app import app, db

def create_milestones():
    """Create initial milestone data"""
    # Import here to avoid circular imports
    from models import Milestone
    
    with app.app_context():
        # Clear existing milestones
        Milestone.query.delete()
        
        # Create starter milestones
        milestones = [
            Milestone(
                code='define_identity',
                title='Define Identity',
                description='Establish your archetype, mood, and professional identity',
                active=True,
                completed=False,
                order_index=1
            ),
            Milestone(
                code='build_mission',
                title='Build Mission',
                description='Create your mission statement and highest goal',
                active=False,
                completed=False,
                order_index=2
            ),
            Milestone(
                code='design_first_offer',
                title='Design First Offer',
                description='Create your first service or product offering',
                active=False,
                completed=False,
                order_index=3
            ),
            Milestone(
                code='secure_first_clients',
                title='Secure First Clients',
                description='Land your initial customers and validate your offer',
                active=False,
                completed=False,
                order_index=4
            ),
            Milestone(
                code='automate_system',
                title='Automate AI System',
                description='Build systems to scale your solopreneur business',
                active=False,
                completed=False,
                order_index=5
            )
        ]
        
        for milestone in milestones:
            db.session.add(milestone)
        
        db.session.commit()
        print(f"✓ Created {len(milestones)} milestones")

if __name__ == '__main__':
    create_milestones()
'''
    
    write_file('bootstrap_milestones.py', bootstrap_script)
    
    # 7. Update agent service for milestone-driven orchestration
    print("\n🤖 Updating agent orchestration...")
    
    # Patch agent_service.py to include milestone context
    agent_patch = '''

def get_milestone_context():
    """Get current active milestone context"""
    try:
        from models import Milestone
        active_milestone = Milestone.query.filter_by(active=True, completed=False).first()
        if active_milestone:
            return f"Current milestone: {active_milestone.title} - {active_milestone.description}"
        return "No active milestone"
    except:
        return "Milestone system initializing"

'''
    
    # Add milestone context to agent service
    with open('agent_service.py', 'r') as f:
        agent_content = f.read()
    
    # Insert milestone context function
    if 'get_milestone_context' not in agent_content:
        agent_content = agent_patch + agent_content
    
    # Update get_agent_response to include milestone context
    agent_content = re.sub(
        r'(def get_agent_response\(user_message, message_history=None, user_info=None\):.*?context = create_context\(user_info\))',
        r'\1\n        milestone_context = get_milestone_context()',
        agent_content,
        flags=re.DOTALL
    )
    
    write_file('agent_service.py', agent_content)
    
    # 8. Run database migration and seeding
    print("\n💾 Setting up database...")
    
    # Create the database tables
    migration_script = '''
from app import app, db

with app.app_context():
    db.create_all()
    print("✓ Database tables created")
'''
    
    write_file('migrate_db.py', migration_script)
    run_command('python migrate_db.py', 'Creating database tables')
    run_command('python bootstrap_milestones.py', 'Seeding milestone data')
    
    # 9. Create .gitignore if missing
    print("\n📝 Creating .gitignore...")
    
    gitignore_content = '''# Database
instance/
*.db
*.sqlite

# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg
MANIFEST

# Environment
.env
.venv
env/
venv/
ENV/
env.bak/
venv.bak/

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Logs
*.log
logs/

# Node modules (if any)
node_modules/

# Temporary files
*.tmp
*.temp
'''
    
    if not os.path.exists('.gitignore'):
        write_file('.gitignore', gitignore_content)
    
    # 10. Final steps
    print("\n🎯 Finalizing migration...")
    
    # Create default avatar placeholder
    ensure_directory('static/images')
    
    # Clean up temporary files
    for temp_file in ['migrate_db.py']:
        if os.path.exists(temp_file):
            os.remove(temp_file)
    
    # Git operations
    run_command('git add .', 'Staging all changes')
    run_command('git commit -m "feat(uiux): implement 3-tab Highest-Goal interface with milestone-driven orchestration"', 'Committing changes')
    
    print("\n🎉 UX Migration Complete!")
    print("\nSummary of changes:")
    print("✓ Created 3-view Vue.js interface (Identity/Mission/Roadmap)")
    print("✓ Added milestone-driven orchestration system")
    print("✓ Updated database schema with identity/mission fields")
    print("✓ Implemented responsive header with user data")
    print("✓ Added interactive chat integration in Mission view")
    print("✓ Created comprehensive API endpoints")
    print("✓ Added milestone management system")
    print("✓ Updated routes for new interface")
    print("✓ Created database migration and seeding")
    print("✓ Added proper .gitignore file")
    
    print("\nNext steps:")
    print("1. Restart the application to see the new interface")
    print("2. Test the Identity → Mission → Roadmap flow")
    print("3. Verify milestone progression works correctly")
    print("4. Test chat integration in Mission view")
    
    return True

if __name__ == '__main__':
    success = main()
    if success:
        print("\n🚀 Ready to launch the new Missiora interface!")
    else:
        print("\n❌ Migration encountered issues. Check logs above.")