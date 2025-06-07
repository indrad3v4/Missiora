"""
Advanced UX Migration Script for Missiora
Creates beautiful Vue 3 interface with orchestrator integration
"""

import os
import shutil
import subprocess
import json
import textwrap
from pathlib import Path

def ensure_directory(path):
    """Create directory if it doesn't exist"""
    Path(path).mkdir(parents=True, exist_ok=True)

def write_file(filepath, content):
    """Write content to file, creating directories if needed"""
    ensure_directory(os.path.dirname(filepath))
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

def main():
    print("🚀 Starting Advanced UX Migration...")
    
    # Create Vue project structure
    vue_src = Path("static/src")
    components_dir = vue_src / "components"
    assets_dir = vue_src / "assets"
    
    ensure_directory(str(components_dir))
    ensure_directory(str(assets_dir))
    
    # 1. Create enhanced package.json for Vue build
    package_json = {
        "name": "missiora-ui",
        "version": "1.0.0",
        "scripts": {
            "dev": "vite",
            "build": "vite build",
            "preview": "vite preview"
        },
        "dependencies": {
            "vue": "^3.3.4",
            "@vueuse/core": "^10.5.0",
            "pinia": "^2.1.7"
        },
        "devDependencies": {
            "@vitejs/plugin-vue": "^4.4.0",
            "vite": "^4.4.9",
            "tailwindcss": "^3.3.3",
            "autoprefixer": "^10.4.16",
            "postcss": "^8.4.31"
        }
    }
    
    write_file("static/package.json", json.dumps(package_json, indent=2))
    
    # 2. Create Vite config
    vite_config = textwrap.dedent("""
        import { defineConfig } from 'vite'
        import vue from '@vitejs/plugin-vue'
        
        export default defineConfig({
          plugins: [vue()],
          build: {
            outDir: '../dist',
            rollupOptions: {
              input: 'src/main.js'
            }
          },
          server: {
            proxy: {
              '/api': 'http://localhost:5000'
            }
          }
        })
    """)
    write_file("static/vite.config.js", vite_config)
    
    # 3. Create Tailwind config
    tailwind_config = textwrap.dedent("""
        module.exports = {
          content: ['./src/**/*.{vue,js,ts}', '../templates/**/*.html'],
          theme: {
            extend: {
              colors: {
                primary: {
                  50: '#ecfdf5',
                  500: '#10b981',
                  600: '#059669',
                  700: '#047857'
                },
                secondary: {
                  50: '#eff6ff',
                  500: '#3b82f6',
                  600: '#2563eb'
                }
              },
              animation: {
                'pulse-slow': 'pulse 3s infinite',
                'bounce-gentle': 'bounce 2s infinite'
              }
            }
          },
          plugins: []
        }
    """)
    write_file("static/tailwind.config.js", tailwind_config)
    
    # 4. Create main Vue app entry point
    main_js = textwrap.dedent("""
        import { createApp } from 'vue'
        import { createPinia } from 'pinia'
        import App from './App.vue'
        import './assets/style.css'
        
        const app = createApp(App)
        app.use(createPinia())
        app.mount('#app')
    """)
    write_file("static/src/main.js", main_js)
    
    # 5. Create CSS with Tailwind
    style_css = textwrap.dedent("""
        @tailwind base;
        @tailwind components;
        @tailwind utilities;
        
        @layer components {
          .gradient-header {
            background: linear-gradient(135deg, #10b981 0%, #3b82f6 100%);
          }
          
          .glass-card {
            @apply bg-white/80 backdrop-blur-lg border border-white/20 rounded-2xl shadow-xl;
          }
          
          .input-field {
            @apply w-full px-4 py-3 border-2 border-gray-200 rounded-xl focus:border-primary-500 focus:outline-none transition-colors duration-200;
          }
          
          .btn-primary {
            @apply bg-gradient-to-r from-primary-500 to-secondary-500 text-white px-6 py-3 rounded-xl font-semibold hover:shadow-lg transform hover:-translate-y-0.5 transition-all duration-200;
          }
          
          .btn-secondary {
            @apply bg-gray-600 text-white px-6 py-3 rounded-xl font-semibold hover:bg-gray-700 transition-colors duration-200;
          }
          
          .milestone-card {
            @apply p-6 border-2 border-gray-200 rounded-2xl cursor-pointer transition-all duration-300 hover:shadow-lg;
          }
          
          .milestone-card.active {
            @apply border-primary-500 bg-primary-50 shadow-lg;
          }
          
          .milestone-card.completed {
            @apply border-green-500 bg-green-50;
          }
          
          .milestone-icon {
            @apply w-12 h-12 rounded-full flex items-center justify-center text-white font-bold text-lg;
          }
          
          .milestone-icon.active {
            @apply bg-primary-500;
          }
          
          .milestone-icon.completed {
            @apply bg-green-500;
          }
          
          .milestone-icon.pending {
            @apply bg-gray-400;
          }
        }
    """)
    write_file("static/src/assets/style.css", style_css)
    
    # 6. Create main App.vue with advanced layout
    app_vue = textwrap.dedent("""
        <template>
          <div id="app" class="min-h-screen bg-gradient-to-br from-gray-50 to-gray-100">
            <HeaderComponent :user-data="userData" />
            
            <main class="pb-24">
              <transition name="fade" mode="out-in">
                <component :is="currentView" 
                  @identity-saved="handleIdentitySaved"
                  @mission-saved="handleMissionSaved"
                  @update-header="updateHeaderData"
                />
              </transition>
            </main>
            
            <FooterNav 
              :active-tab="activeTab" 
              @tab-change="changeTab"
            />
          </div>
        </template>
        
        <script setup>
        import { ref, computed, onMounted } from 'vue'
        import HeaderComponent from './components/HeaderComponent.vue'
        import FooterNav from './components/FooterNav.vue'
        import IdentityView from './components/IdentityView.vue'
        import MissionView from './components/MissionView.vue'
        import RoadmapView from './components/RoadmapView.vue'
        
        const activeTab = ref('Identity')
        const userData = ref({
          name: 'Solopreneur',
          goal: 'Set Your Goal',
          location: 'Location',
          quarter: 'Q1 2025',
          balance: 0
        })
        
        const views = {
          Identity: IdentityView,
          Mission: MissionView,
          Roadmap: RoadmapView
        }
        
        const currentView = computed(() => views[activeTab.value])
        
        onMounted(async () => {
          await loadUserData()
        })
        
        async function loadUserData() {
          try {
            const response = await fetch('/api/user-data')
            if (response.ok) {
              const data = await response.json()
              userData.value = { ...userData.value, ...data }
            }
          } catch (error) {
            console.log('Using default user data')
          }
        }
        
        function updateHeaderData(newData) {
          userData.value = { ...userData.value, ...newData }
        }
        
        function changeTab(tab) {
          activeTab.value = tab
        }
        
        function handleIdentitySaved(data) {
          updateHeaderData({
            name: data.name,
            location: data.region
          })
          setTimeout(() => changeTab('Mission'), 1000)
        }
        
        function handleMissionSaved(data) {
          updateHeaderData({
            goal: data.goal
          })
          setTimeout(() => changeTab('Roadmap'), 1000)
        }
        </script>
        
        <style>
        .fade-enter-active,
        .fade-leave-active {
          transition: opacity 0.3s ease;
        }
        
        .fade-enter-from,
        .fade-leave-to {
          opacity: 0;
        }
        </style>
    """)
    write_file("static/src/App.vue", app_vue)
    
    # 7. Create enhanced HeaderComponent
    header_component = textwrap.dedent("""
        <template>
          <header class="gradient-header text-white px-6 py-4">
            <div class="max-w-7xl mx-auto flex justify-between items-center">
              <h1 class="text-2xl font-bold tracking-wider">MISSIORA</h1>
              
              <div v-if="userData" class="glass-card px-4 py-2 text-sm">
                <div class="flex items-center space-x-4">
                  <span class="font-medium">{{ userData.name }}</span>
                  <span class="flex items-center">
                    <span class="mr-1">🎯</span>
                    {{ userData.goal }}
                  </span>
                  <span class="flex items-center">
                    <span class="mr-1">📍</span>
                    {{ userData.location }}
                  </span>
                  <span class="flex items-center">
                    <span class="mr-1">🕒</span>
                    {{ userData.quarter }}
                  </span>
                  <span class="flex items-center">
                    <span class="mr-1">💰</span>
                    €{{ userData.balance }}
                  </span>
                </div>
              </div>
              
              <div class="w-12 h-12 bg-white/20 rounded-full flex items-center justify-center">
                <span class="font-bold text-lg">{{ initials }}</span>
              </div>
            </div>
          </header>
        </template>
        
        <script setup>
        import { computed } from 'vue'
        
        const props = defineProps({
          userData: {
            type: Object,
            default: () => ({})
          }
        })
        
        const initials = computed(() => {
          if (!props.userData.name) return 'S'
          return props.userData.name
            .split(' ')
            .map(n => n[0])
            .join('')
            .toUpperCase()
            .substring(0, 2)
        })
        </script>
    """)
    write_file("static/src/components/HeaderComponent.vue", header_component)
    
    # 8. Create FooterNav component
    footer_nav = textwrap.dedent("""
        <template>
          <nav class="fixed bottom-0 left-0 right-0 bg-white border-t border-gray-200 px-6 py-4">
            <div class="max-w-7xl mx-auto flex justify-center space-x-8">
              <button
                v-for="tab in tabs"
                :key="tab"
                @click="$emit('tab-change', tab)"
                :class="[
                  'px-8 py-3 rounded-xl font-semibold transition-all duration-200',
                  activeTab === tab 
                    ? 'bg-gradient-to-r from-primary-500 to-secondary-500 text-white shadow-lg transform -translate-y-1' 
                    : 'text-gray-600 hover:text-gray-800 hover:bg-gray-100'
                ]"
              >
                {{ tab }}
              </button>
            </div>
          </nav>
        </template>
        
        <script setup>
        defineProps({
          activeTab: String
        })
        
        defineEmits(['tab-change'])
        
        const tabs = ['Identity', 'Mission', 'Roadmap']
        </script>
    """)
    write_file("static/src/components/FooterNav.vue", footer_nav)
    
    # 9. Create enhanced IdentityView with orchestrator
    identity_view = textwrap.dedent("""
        <template>
          <div class="max-w-4xl mx-auto px-6 py-8">
            <div class="glass-card p-8">
              <h2 class="text-3xl font-bold text-gray-800 mb-2">Define Your Identity</h2>
              <p class="text-gray-600 mb-8">Discover your authentic self and entrepreneurial archetype</p>
              
              <!-- Orchestrator Helper -->
              <div v-if="showOrchestrator" class="mb-8 p-6 bg-blue-50 border border-blue-200 rounded-xl">
                <div class="flex justify-between items-center mb-4">
                  <h3 class="text-lg font-semibold text-blue-800">🧠 Identity Orchestrator</h3>
                  <button @click="showOrchestrator = false" class="text-blue-600 hover:text-blue-800">×</button>
                </div>
                <div class="space-y-4">
                  <div v-for="message in orchestratorMessages" :key="message.id" 
                       :class="['p-3 rounded-lg', message.type === 'user' ? 'bg-blue-100 ml-8' : 'bg-white mr-8']">
                    {{ message.content }}
                  </div>
                  <div class="flex gap-2">
                    <input 
                      v-model="orchestratorInput" 
                      @keyup.enter="sendToOrchestrator"
                      placeholder="Tell me about yourself..."
                      class="flex-1 input-field"
                    />
                    <button @click="sendToOrchestrator" class="btn-primary">Send</button>
                  </div>
                </div>
              </div>
              
              <form @submit.prevent="saveIdentity" class="space-y-6">
                <div>
                  <label class="block text-sm font-semibold text-gray-700 mb-2">Your Name</label>
                  <input v-model="identity.name" 
                         placeholder="Enter your full name" 
                         class="input-field" />
                </div>
                
                <div>
                  <label class="block text-sm font-semibold text-gray-700 mb-2">Entrepreneurial Archetype</label>
                  <select v-model="identity.archetype" class="input-field">
                    <option value="">Select your archetype</option>
                    <option value="builder">Builder - Create and construct</option>
                    <option value="guide">Guide - Teach and mentor</option>
                    <option value="rebel">Rebel - Disrupt and innovate</option>
                    <option value="creator">Creator - Design and imagine</option>
                    <option value="connector">Connector - Network and unite</option>
                  </select>
                </div>
                
                <div>
                  <label class="block text-sm font-semibold text-gray-700 mb-2">Current Mood & Energy</label>
                  <textarea v-model="identity.mood" 
                            placeholder="How are you feeling about your entrepreneurial journey right now?"
                            class="input-field h-24 resize-none"></textarea>
                </div>
                
                <div>
                  <label class="block text-sm font-semibold text-gray-700 mb-2">Region/Location</label>
                  <input v-model="identity.region" 
                         placeholder="Where are you based? (e.g., Berlin, Germany)" 
                         class="input-field" />
                </div>
                
                <div>
                  <label class="block text-sm font-semibold text-gray-700 mb-2">Industry/Field</label>
                  <input v-model="identity.field" 
                         placeholder="What industry or field do you work in?" 
                         class="input-field" />
                </div>
                
                <div>
                  <label class="block text-sm font-semibold text-gray-700 mb-2">Professional Title</label>
                  <input v-model="identity.title" 
                         placeholder="How do you describe yourself professionally?" 
                         class="input-field" />
                </div>
                
                <div class="flex gap-4 pt-4">
                  <button type="submit" class="btn-primary flex-1">
                    Save Identity & Continue
                  </button>
                  <button type="button" @click="toggleOrchestrator" class="btn-secondary">
                    {{ showOrchestrator ? 'Hide' : 'Get' }} AI Guidance
                  </button>
                </div>
              </form>
            </div>
          </div>
        </template>
        
        <script setup>
        import { ref, onMounted } from 'vue'
        
        const emit = defineEmits(['identity-saved', 'update-header'])
        
        const identity = ref({
          name: '',
          archetype: '',
          mood: '',
          region: '',
          field: '',
          title: ''
        })
        
        const showOrchestrator = ref(false)
        const orchestratorMessages = ref([])
        const orchestratorInput = ref('')
        
        onMounted(async () => {
          await loadIdentity()
        })
        
        async function loadIdentity() {
          try {
            const response = await fetch('/api/identity')
            if (response.ok) {
              const data = await response.json()
              Object.assign(identity.value, data)
            }
          } catch (error) {
            console.log('No existing identity data')
          }
        }
        
        async function saveIdentity() {
          try {
            const response = await fetch('/api/identity', {
              method: 'POST',
              headers: { 'Content-Type': 'application/json' },
              body: JSON.stringify(identity.value)
            })
            
            if (response.ok) {
              emit('identity-saved', identity.value)
              emit('update-header', {
                name: identity.value.name,
                location: identity.value.region
              })
            }
          } catch (error) {
            console.error('Failed to save identity:', error)
          }
        }
        
        function toggleOrchestrator() {
          showOrchestrator.value = !showOrchestrator.value
          if (showOrchestrator.value && orchestratorMessages.value.length === 0) {
            orchestratorMessages.value.push({
              id: 1,
              type: 'ai',
              content: 'Hello! I\'m here to help you discover your authentic entrepreneurial identity. What drives you? What are you passionate about creating?'
            })
          }
        }
        
        async function sendToOrchestrator() {
          if (!orchestratorInput.value.trim()) return
          
          const userMessage = orchestratorInput.value.trim()
          orchestratorMessages.value.push({
            id: Date.now(),
            type: 'user',
            content: userMessage
          })
          
          orchestratorInput.value = ''
          
          try {
            const response = await fetch('/api/chat', {
              method: 'POST',
              headers: { 'Content-Type': 'application/json' },
              body: JSON.stringify({
                user_message: userMessage,
                context: 'identity_discovery'
              })
            })
            
            if (response.ok) {
              const data = await response.json()
              orchestratorMessages.value.push({
                id: Date.now(),
                type: 'ai',
                content: data.reply
              })
            }
          } catch (error) {
            orchestratorMessages.value.push({
              id: Date.now(),
              type: 'ai',
              content: 'I understand. Take your time to reflect on what truly matters to you in your entrepreneurial journey.'
            })
          }
        }
        </script>
    """)
    write_file("static/src/components/IdentityView.vue", identity_view)
    
    # 10. Create enhanced MissionView
    mission_view = textwrap.dedent("""
        <template>
          <div class="max-w-4xl mx-auto px-6 py-8">
            <div class="glass-card p-8">
              <h2 class="text-3xl font-bold text-gray-800 mb-2">Build Your Mission</h2>
              <p class="text-gray-600 mb-8">Define your highest goal and authentic mission</p>
              
              <!-- Enhanced Orchestrator Chat -->
              <div v-if="showChat" class="mb-8 glass-card p-6">
                <div class="flex justify-between items-center mb-4">
                  <h3 class="text-lg font-semibold text-gray-800">🧠 Mission Orchestrator</h3>
                  <button @click="showChat = false" class="text-gray-600 hover:text-gray-800 text-xl">×</button>
                </div>
                
                <div class="h-64 overflow-y-auto mb-4 space-y-3">
                  <div v-for="msg in chatMessages" :key="msg.id" 
                       :class="['p-4 rounded-xl', msg.role === 'user' ? 'bg-blue-100 ml-8' : 'bg-gray-100 mr-8']">
                    <div class="font-medium mb-1" v-if="msg.role === 'assistant'">🤖 Orchestrator</div>
                    {{ msg.content }}
                  </div>
                  <div v-if="isTyping" class="bg-gray-100 mr-8 p-4 rounded-xl">
                    <div class="flex items-center space-x-2">
                      <div class="animate-pulse">🤖 Orchestrator is thinking...</div>
                    </div>
                  </div>
                </div>
                
                <div class="flex gap-2">
                  <input 
                    v-model="chatInput" 
                    @keyup.enter="sendChatMessage"
                    placeholder="What's your highest aspiration?"
                    class="flex-1 input-field"
                    :disabled="isTyping"
                  />
                  <button @click="sendChatMessage" :disabled="isTyping || !chatInput.trim()" 
                          class="btn-primary">
                    {{ isTyping ? '...' : 'Send' }}
                  </button>
                </div>
              </div>
              
              <form @submit.prevent="saveMission" class="space-y-6">
                <div>
                  <label class="block text-sm font-semibold text-gray-700 mb-2">Mission Statement</label>
                  <textarea v-model="mission.statement" 
                            placeholder="What is your core mission? What change do you want to create in the world?"
                            class="input-field h-32 resize-none"></textarea>
                </div>
                
                <div>
                  <label class="block text-sm font-semibold text-gray-700 mb-2">Highest Goal</label>
                  <input v-model="mission.goal" 
                         placeholder="What do you ultimately want to achieve? Be specific and ambitious."
                         class="input-field" />
                </div>
                
                <div>
                  <label class="block text-sm font-semibold text-gray-700 mb-2">Emotional Blocks & Fears</label>
                  <textarea v-model="mission.blocks" 
                            placeholder="What fears, doubts, or limiting beliefs hold you back?"
                            class="input-field h-24 resize-none"></textarea>
                </div>
                
                <div class="flex gap-4 pt-4">
                  <button type="submit" class="btn-primary flex-1">
                    Save Mission & Generate Roadmap
                  </button>
                  <button type="button" @click="toggleChat" class="btn-secondary">
                    {{ showChat ? 'Hide' : 'Chat with' }} Orchestrator
                  </button>
                </div>
              </form>
            </div>
          </div>
        </template>
        
        <script setup>
        import { ref, onMounted, nextTick } from 'vue'
        
        const emit = defineEmits(['mission-saved', 'update-header'])
        
        const mission = ref({
          statement: '',
          goal: '',
          blocks: ''
        })
        
        const showChat = ref(false)
        const chatMessages = ref([])
        const chatInput = ref('')
        const isTyping = ref(false)
        
        onMounted(async () => {
          await loadMission()
        })
        
        async function loadMission() {
          try {
            const response = await fetch('/api/mission')
            if (response.ok) {
              const data = await response.json()
              Object.assign(mission.value, data)
            }
          } catch (error) {
            console.log('No existing mission data')
          }
        }
        
        async function saveMission() {
          try {
            const response = await fetch('/api/mission', {
              method: 'POST',
              headers: { 'Content-Type': 'application/json' },
              body: JSON.stringify(mission.value)
            })
            
            if (response.ok) {
              emit('mission-saved', mission.value)
              emit('update-header', {
                goal: mission.value.goal
              })
            }
          } catch (error) {
            console.error('Failed to save mission:', error)
          }
        }
        
        function toggleChat() {
          showChat.value = !showChat.value
          if (showChat.value && chatMessages.value.length === 0) {
            chatMessages.value.push({
              id: 1,
              role: 'assistant',
              content: 'Welcome! I\'m here to help you clarify your highest goal and mission. What impact do you want to make? What legacy do you want to leave?'
            })
          }
        }
        
        async function sendChatMessage() {
          if (!chatInput.value.trim() || isTyping.value) return
          
          const userMsg = chatInput.value.trim()
          chatMessages.value.push({
            id: Date.now(),
            role: 'user',
            content: userMsg
          })
          
          chatInput.value = ''
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
              chatMessages.value.push({
                id: Date.now(),
                role: 'assistant',
                content: data.reply
              })
            }
          } catch (error) {
            chatMessages.value.push({
              id: Date.now(),
              role: 'assistant',
              content: 'I understand your vision. Let\'s explore what specific outcomes would make you feel most fulfilled and aligned with your purpose.'
            })
          } finally {
            isTyping.value = false
          }
        }
        </script>
    """)
    write_file("static/src/components/MissionView.vue", mission_view)
    
    # 11. Create beautiful RoadmapView with lifeline design
    roadmap_view = textwrap.dedent("""
        <template>
          <div class="max-w-4xl mx-auto px-6 py-8">
            <div class="glass-card p-8">
              <h2 class="text-3xl font-bold text-gray-800 mb-2">Your Roadmap</h2>
              <p class="text-gray-600 mb-8">Let's follow your roadmap to the highest goal.</p>
              
              <!-- Lifeline Visual -->
              <div class="relative">
                <div class="absolute left-8 top-0 bottom-0 w-1 bg-gradient-to-b from-primary-500 to-secondary-500"></div>
                
                <div class="space-y-6">
                  <div v-for="(milestone, index) in milestones" :key="milestone.id"
                       class="relative flex items-start space-x-6">
                    
                    <!-- Milestone Icon -->
                    <div :class="[
                      'milestone-icon relative z-10',
                      milestone.status === 'active' ? 'active' : 
                      milestone.status === 'completed' ? 'completed' : 'pending'
                    ]">
                      <i v-if="milestone.status === 'completed'" class="fas fa-check"></i>
                      <i v-else-if="milestone.status === 'active'" class="fas fa-target"></i>
                      <span v-else>{{ index + 1 }}</span>
                    </div>
                    
                    <!-- Milestone Content -->
                    <div :class="[
                      'milestone-card flex-1',
                      milestone.status === 'active' ? 'active' : 
                      milestone.status === 'completed' ? 'completed' : ''
                    ]" @click="selectMilestone(milestone)">
                      
                      <div class="flex justify-between items-start mb-3">
                        <h3 class="text-xl font-semibold text-gray-800">{{ milestone.title }}</h3>
                        <span :class="[
                          'px-3 py-1 rounded-full text-xs font-medium',
                          milestone.status === 'active' ? 'bg-primary-100 text-primary-700' :
                          milestone.status === 'completed' ? 'bg-green-100 text-green-700' :
                          'bg-gray-100 text-gray-700'
                        ]">
                          {{ milestone.status }}
                        </span>
                      </div>
                      
                      <p class="text-gray-600 mb-4">{{ milestone.description }}</p>
                      
                      <!-- AI Suggestion (for active milestone) -->
                      <div v-if="milestone.status === 'active' && milestone.suggestion" 
                           class="bg-yellow-50 border border-yellow-200 rounded-xl p-4">
                        <h4 class="font-semibold text-yellow-800 mb-2">💡 AI Suggestion</h4>
                        <p class="text-yellow-700 mb-3">{{ milestone.suggestion.idea }}</p>
                        <div class="flex space-x-4 text-sm">
                          <span class="text-yellow-600">💰 Cost: {{ milestone.suggestion.cost }}</span>
                          <span class="text-yellow-600">📈 ROI: {{ milestone.suggestion.roi }}</span>
                        </div>
                      </div>
                      
                      <!-- Action Buttons -->
                      <div v-if="milestone.status === 'active'" class="flex gap-3 mt-4">
                        <button @click.stop="completeMilestone(milestone.id)" 
                                class="btn-primary">
                          Mark Complete
                        </button>
                        <button @click.stop="chatWithOrchestrator(milestone)" 
                                class="btn-secondary">
                          Get Guidance
                        </button>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
              
              <!-- Progress Summary -->
              <div class="mt-12 p-6 bg-gray-50 rounded-xl">
                <h3 class="text-lg font-semibold mb-4">Progress Summary</h3>
                <div class="flex justify-between text-sm text-gray-600">
                  <span>{{ completedCount }} of {{ milestones.length }} milestones completed</span>
                  <span>{{ Math.round((completedCount / milestones.length) * 100) }}% complete</span>
                </div>
                <div class="mt-2 bg-gray-200 rounded-full h-2">
                  <div class="bg-gradient-to-r from-primary-500 to-secondary-500 h-2 rounded-full transition-all duration-500"
                       :style="{ width: (completedCount / milestones.length) * 100 + '%' }"></div>
                </div>
              </div>
            </div>
          </div>
        </template>
        
        <script setup>
        import { ref, computed, onMounted } from 'vue'
        
        const milestones = ref([])
        const selectedMilestone = ref(null)
        
        const completedCount = computed(() => 
          milestones.value.filter(m => m.status === 'completed').length
        )
        
        onMounted(async () => {
          await loadMilestones()
        })
        
        async function loadMilestones() {
          try {
            const response = await fetch('/api/milestones')
            if (response.ok) {
              const data = await response.json()
              milestones.value = data.map(m => ({
                ...m,
                suggestion: m.code === 'design_first_offer' ? {
                  idea: 'Automate Courier Service Platform',
                  cost: '€80 initial investment',
                  roi: '€500 revenue in 2 weeks'
                } : null
              }))
            }
          } catch (error) {
            console.error('Failed to load milestones:', error)
          }
        }
        
        function selectMilestone(milestone) {
          selectedMilestone.value = milestone
        }
        
        async function completeMilestone(milestoneId) {
          try {
            const response = await fetch(`/api/milestones/${milestoneId}/complete`, {
              method: 'POST'
            })
            
            if (response.ok) {
              await loadMilestones()
            }
          } catch (error) {
            console.error('Failed to complete milestone:', error)
          }
        }
        
        function chatWithOrchestrator(milestone) {
          // Navigate to chat with context
          window.location.href = `/narrative-chat?context=milestone&id=${milestone.id}`
        }
        </script>
        
        <style scoped>
        .fas {
          font-family: "Font Awesome 5 Free";
          font-weight: 900;
        }
        </style>
    """)
    write_file("static/src/components/RoadmapView.vue", roadmap_view)
    
    # 12. Update templates/index.html to use new build
    index_html = textwrap.dedent("""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Missiora - AI Agency for Solopreneurs</title>
            <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
            <link href="{{ url_for('static', filename='dist/assets/index.css') }}" rel="stylesheet">
        </head>
        <body>
            <div id="app">
                <div class="min-h-screen flex items-center justify-center bg-gradient-to-br from-primary-500 to-secondary-500">
                    <div class="text-white text-center">
                        <div class="animate-spin w-8 h-8 border-4 border-white border-t-transparent rounded-full mx-auto mb-4"></div>
                        <p class="text-lg">Loading Missiora...</p>
                    </div>
                </div>
            </div>
            <script src="{{ url_for('static', filename='dist/assets/index.js') }}"></script>
        </body>
        </html>
    """)
    write_file("templates/index.html", index_html)
    
    # 13. Build the Vue application
    print("📦 Installing dependencies...")
    os.chdir("static")
    
    # Install dependencies
    subprocess.run(["npm", "install"], check=True)
    
    # Build for production
    print("🔨 Building Vue application...")
    subprocess.run(["npm", "run", "build"], check=True)
    
    os.chdir("..")
    
    print("✅ Advanced UX Migration completed!")
    print("\n🎯 What's new:")
    print("• Beautiful gradient header with real-time user data")
    print("• Glass-morphism design with Tailwind CSS")
    print("• Enhanced orchestrator integration in Identity & Mission")
    print("• Lifeline roadmap visualization with AI suggestions")
    print("• Smooth transitions and micro-interactions")
    print("• Responsive design for all devices")
    print("\n🚀 Ready to launch!")

if __name__ == "__main__":
    main()