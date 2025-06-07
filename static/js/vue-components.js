// Vue 3 Components for Missiora 3-view interface

const HeaderView = {
  props: ['userData'],
  template: `
    <header class="gradient-header px-6 py-4 text-white">
      <div class="max-w-7xl mx-auto flex justify-between items-center">
        <h1 class="text-2xl font-bold tracking-wider">MISSIORA</h1>
        
        <div v-if="userData" class="glass-pill">
          <div class="user-data-items">
            <span class="user-name">{{ userData.name || 'Solopreneur' }}</span>
            <span class="user-goal">🎯 {{ userData.currentGoal || 'Set Your Goal' }}</span>
            <span class="user-location">📍 {{ userData.location || 'Location' }}</span>
            <span class="user-timeline">🕒 {{ userData.timeline || 'Q1 2025' }}</span>
            <span class="user-balance">💰 €{{ userData.balance || '0' }}</span>
          </div>
        </div>
        
        <div class="avatar-circle">
          {{ getInitials(userData?.name) }}
        </div>
      </div>
    </header>
  `,
  methods: {
    getInitials(name) {
      if (!name) return 'S'
      return name.split(' ').map(n => n[0]).join('').toUpperCase().substring(0, 2)
    }
  }
}

const IdentityView = {
  emits: ['save', 'update-header'],
  data() {
    return {
      identity: {
        name: '',
        archetype: '',
        mood: '',
        region: '',
        field: '',
        selfTitle: ''
      },
      showOrchestrator: false,
      orchestratorMessages: [],
      orchestratorInput: '',
      isOrchestratorTyping: false
    }
  },
  template: `
    <div class="max-w-4xl mx-auto px-6 py-8">
      <div class="glass-card p-8">
        <h2 class="text-3xl font-bold text-gray-800 mb-2">Define Your Identity</h2>
        <p class="text-gray-600 mb-8">Discover your authentic self and entrepreneurial archetype</p>
        
        <!-- Orchestrator Helper -->
        <div v-if="showOrchestrator" class="mb-8 orchestrator-card">
          <div class="orchestrator-header">
            <h3 class="orchestrator-title">🧠 Identity Orchestrator</h3>
            <button @click="showOrchestrator = false" class="close-orchestrator">×</button>
          </div>
          
          <div class="orchestrator-messages">
            <div v-for="message in orchestratorMessages" :key="message.id" 
                 :class="['message-bubble', message.type === 'user' ? 'user-message' : 'ai-message']">
              <div class="message-content">{{ message.content }}</div>
            </div>
            <div v-if="isOrchestratorTyping" class="ai-message">
              <div class="typing-indicator">
                <span>🤖 Thinking</span>
                <div class="typing-dots">
                  <span></span><span></span><span></span>
                </div>
              </div>
            </div>
          </div>
          
          <div class="orchestrator-input">
            <input 
              v-model="orchestratorInput" 
              @keyup.enter="sendToOrchestrator"
              placeholder="Tell me about yourself, your dreams, your challenges..."
              class="flex-1 input-field"
              :disabled="isOrchestratorTyping"
            />
            <button @click="sendToOrchestrator" 
                    :disabled="isOrchestratorTyping || !orchestratorInput.trim()" 
                    class="btn-primary">
              {{ isOrchestratorTyping ? '...' : 'Send' }}
            </button>
          </div>
        </div>
        
        <form @submit.prevent="saveIdentity" class="space-y-6">
          <div class="form-group">
            <label class="form-label">Your Name</label>
            <input v-model="identity.name" 
                   placeholder="Enter your full name" 
                   class="input-field" />
          </div>
          
          <div class="form-group">
            <label class="form-label">Entrepreneurial Archetype</label>
            <select v-model="identity.archetype" class="input-field">
              <option value="">Select your archetype</option>
              <option value="builder">Builder - Create and construct</option>
              <option value="guide">Guide - Teach and mentor</option>
              <option value="rebel">Rebel - Disrupt and innovate</option>
              <option value="creator">Creator - Design and imagine</option>
              <option value="connector">Connector - Network and unite</option>
            </select>
          </div>
          
          <div class="form-group">
            <label class="form-label">Current Mood & Energy</label>
            <textarea v-model="identity.mood" 
                      placeholder="How are you feeling about your entrepreneurial journey right now?"
                      class="input-field textarea-field"></textarea>
          </div>
          
          <div class="form-group">
            <label class="form-label">Region/Location</label>
            <input v-model="identity.region" 
                   placeholder="Where are you based? (e.g., Berlin, Germany)" 
                   class="input-field" />
          </div>
          
          <div class="form-group">
            <label class="form-label">Industry/Field</label>
            <input v-model="identity.field" 
                   placeholder="What industry or field do you work in?" 
                   class="input-field" />
          </div>
          
          <div class="form-group">
            <label class="form-label">Professional Title</label>
            <input v-model="identity.selfTitle" 
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
  `,
  async mounted() {
    await this.loadIdentity()
  },
  methods: {
    async loadIdentity() {
      try {
        const response = await fetch('/api/identity')
        if (response.ok) {
          const data = await response.json()
          Object.assign(this.identity, data)
        }
      } catch (error) {
        console.log('No existing identity data')
      }
    },
    
    async saveIdentity() {
      try {
        const response = await fetch('/api/identity', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(this.identity)
        })
        
        if (response.ok) {
          this.$emit('save', this.identity)
          this.$emit('update-header', {
            name: this.identity.name,
            location: this.identity.region
          })
        }
      } catch (error) {
        console.error('Failed to save identity:', error)
      }
    },
    
    toggleOrchestrator() {
      this.showOrchestrator = !this.showOrchestrator
      if (this.showOrchestrator && this.orchestratorMessages.length === 0) {
        this.orchestratorMessages.push({
          id: 1,
          type: 'ai',
          content: 'Hello! I\'m here to help you discover your authentic entrepreneurial identity. What drives you? What are you passionate about creating? Tell me about your dreams and what makes you unique.'
        })
      }
    },
    
    async sendToOrchestrator() {
      if (!this.orchestratorInput.trim() || this.isOrchestratorTyping) return
      
      const userMessage = this.orchestratorInput.trim()
      this.orchestratorMessages.push({
        id: Date.now(),
        type: 'user',
        content: userMessage
      })
      
      this.orchestratorInput = ''
      this.isOrchestratorTyping = true
      
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
          this.orchestratorMessages.push({
            id: Date.now() + 1,
            type: 'ai',
            content: data.reply || 'I understand. Take your time to reflect on what truly matters to you in your entrepreneurial journey.'
          })
        } else {
          throw new Error('Chat service unavailable')
        }
      } catch (error) {
        this.orchestratorMessages.push({
          id: Date.now() + 1,
          type: 'ai',
          content: 'I understand. Take your time to reflect on what truly matters to you in your entrepreneurial journey. What aspects of your identity feel most authentic to you?'
        })
      } finally {
        this.isOrchestratorTyping = false
        await this.$nextTick()
        this.scrollOrchestratorToBottom()
      }
    },
    
    scrollOrchestratorToBottom() {
      const container = document.querySelector('.orchestrator-messages')
      if (container) {
        container.scrollTop = container.scrollHeight
      }
    }
  }
}

const MissionView = {
  emits: ['save', 'update-header'],
  data() {
    return {
      mission: {
        statement: '',
        goal: '',
        blocks: ''
      },
      showChat: false,
      messages: [],
      userInput: '',
      isTyping: false
    }
  },
  template: `
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
  `,
  async mounted() {
    try {
      const response = await fetch('/api/mission')
      if (response.ok) {
        const data = await response.json()
        Object.assign(this.mission, data)
      }
    } catch (error) {
      console.log('No existing mission data')
    }
  },
  methods: {
    toggleChat() {
      this.showChat = !this.showChat
      if (this.showChat && this.messages.length === 0) {
        this.messages.push({
          id: 1,
          role: 'agent',
          content: "Welcome! I'm here to help you discover and refine your highest goal. What drives you as a solopreneur? What impact do you want to make?"
        })
      }
    },
    async sendMessage() {
      if (!this.userInput.trim() || this.isTyping) return
      
      const userMsg = this.userInput.trim()
      this.messages.push({
        id: Date.now(),
        role: 'user',
        content: userMsg
      })
      
      this.userInput = ''
      this.isTyping = true
      
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
          this.messages.push({
            id: Date.now(),
            role: 'agent',
            content: data.reply || 'I understand your perspective. Could you tell me more about what success looks like for you?'
          })
        } else {
          throw new Error('Chat service unavailable')
        }
      } catch (error) {
        this.messages.push({
          id: Date.now(),
          role: 'agent',
          content: "I understand your goal. Let me help you refine it further. What specific outcome would make you feel most fulfilled?"
        })
      } finally {
        this.isTyping = false
        await this.$nextTick()
        if (this.$refs.chatMessages) {
          this.$refs.chatMessages.scrollTop = this.$refs.chatMessages.scrollHeight
        }
      }
    },
    async saveMission() {
      try {
        const response = await fetch('/api/mission', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(this.mission)
        })
        
        if (response.ok) {
          this.$emit('save', this.mission)
          this.$emit('update-header', {
            currentGoal: this.mission.goal
          })
          alert('Mission saved successfully!')
        }
      } catch (error) {
        console.error('Failed to save mission:', error)
        alert('Failed to save mission')
      }
    }
  }
}

const RoadmapView = {
  emits: ['milestone-change'],
  data() {
    return {
      milestones: [],
      selectedMilestone: null
    }
  },
  template: `
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
  `,
  async mounted() {
    await this.loadMilestones()
  },
  methods: {
    async loadMilestones() {
      try {
        const response = await fetch('/api/milestones')
        if (response.ok) {
          this.milestones = await response.json()
          // Add sample suggestions for demo
          this.milestones.forEach(m => {
            if (m.code === 'design_first_offer') {
              m.suggestions = {
                idea: 'Automate Courier Service',
                cost: '€80',
                roi: '€500 in 2 weeks'
              }
            }
          })
          
          // Auto-select first active or incomplete milestone
          const activeOrNext = this.milestones.find(m => m.active || (!m.completed && !m.active))
          if (activeOrNext) {
            this.selectedMilestone = activeOrNext
          }
        }
      } catch (error) {
        console.error('Failed to load milestones:', error)
      }
    },
    selectMilestone(milestone) {
      this.selectedMilestone = milestone
    },
    canActivate(milestone) {
      // Can activate if previous milestones are completed
      const currentIndex = this.milestones.findIndex(m => m.id === milestone.id)
      if (currentIndex === 0) return true
      
      const previousMilestone = this.milestones[currentIndex - 1]
      return previousMilestone && previousMilestone.completed
    },
    async completeMilestone(milestoneId) {
      try {
        const response = await fetch(`/api/milestones/${milestoneId}/complete`, {
          method: 'POST'
        })
        
        if (response.ok) {
          await this.loadMilestones()
          this.$emit('milestone-change')
        }
      } catch (error) {
        console.error('Failed to complete milestone:', error)
      }
    },
    async activateMilestone(milestoneId) {
      try {
        const response = await fetch(`/api/milestones/${milestoneId}/activate`, {
          method: 'POST'
        })
        
        if (response.ok) {
          await this.loadMilestones()
          this.$emit('milestone-change')
        }
      } catch (error) {
        console.error('Failed to activate milestone:', error)
      }
    }
  }
}

const MainApp = {
  components: {
    HeaderView,
    IdentityView,
    MissionView,
    RoadmapView
  },
  data() {
    return {
      activeTab: 'identity',
      headerData: {
        name: 'Solopreneur',
        currentGoal: 'Set Goal',
        location: 'Location',
        timeline: 'Q1 2025',
        balance: '€0'
      }
    }
  },
  template: `
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
  `,
  async mounted() {
    await this.loadUserData()
  },
  methods: {
    async loadUserData() {
      try {
        const response = await fetch('/api/user-data')
        if (response.ok) {
          const userData = await response.json()
          Object.assign(this.headerData, userData)
        }
      } catch (error) {
        console.log('Loading default user data')
      }
    },
    updateHeader(data) {
      Object.assign(this.headerData, data)
    },
    onIdentitySaved(identityData) {
      if (identityData.name && identityData.archetype) {
        setTimeout(() => {
          this.activeTab = 'mission'
        }, 1000)
      }
    },
    onMissionSaved(missionData) {
      if (missionData.statement && missionData.goal) {
        setTimeout(() => {
          this.activeTab = 'roadmap'
        }, 1000)
      }
    },
    onMilestoneChange() {
      this.loadUserData()
    }
  }
}

export { MainApp, HeaderView, IdentityView, MissionView, RoadmapView }