
// Enhanced Mobile-First Vue Components - Missiora Design System
// Colors: Teal gradients (#008B8B, #20B2AA), Cream cards (#F5E6D3), Orange accents (#FF6B35)

const MobileHeaderView = {
  props: ['userData'],
  template: `
    <header class="mobile-header">
      <div class="header-content">
        <h1 class="brand-title">MISSIORA</h1>
        
        <div v-if="userData" class="user-info-card">
          <div class="user-data-grid">
            <span class="user-name">{{ userData.name || 'Solopreneur' }}</span>
            <span class="user-goal">🎯 {{ userData.currentGoal || 'Reach €1K' }}</span>
            <span class="user-location">📍 {{ userData.location || 'Kraków' }}</span>
            <span class="user-timeline">🕒 {{ userData.timeline || 'Q3 2025' }}</span>
          </div>
          
          <div class="avatar-container">
            <div class="avatar-circle">
              {{ getInitials(userData?.name) }}
            </div>
          </div>
        </div>
        
        <div class="inspirational-message">
          Let's follow your roadmap to the highest goal.
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

const MobileIdentityView = {
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
      isOrchestratorTyping: false,
      contextData: {}
    }
  },
  template: `
    <div class="mobile-view">
      <div class="view-header">
        <div class="milestone-indicator">
          <div class="milestone-icon identity-icon">🪶</div>
          <h2 class="view-title">Define Identity</h2>
        </div>
      </div>
      
      <!-- Context-Aware Orchestrator -->
      <div class="orchestrator-section">
        <button 
          @click="toggleOrchestrator" 
          class="orchestrator-toggle"
          :class="{ active: showOrchestrator }"
        >
          <span class="orchestrator-icon">🧠</span>
          <span>{{ showOrchestrator ? 'Hide' : 'Get' }} AI Guidance</span>
        </button>
        
        <div v-if="showOrchestrator" class="orchestrator-panel">
          <div class="orchestrator-messages">
            <div v-for="message in orchestratorMessages" :key="message.id" 
                 :class="['message-bubble', message.type === 'user' ? 'user-message' : 'ai-message']">
              <div class="message-content" v-html="formatMessage(message.content)"></div>
              <div class="message-meta">
                <span class="message-time">{{ formatTime(message.timestamp) }}</span>
                <span v-if="message.agent_name" class="agent-name">{{ message.agent_name }}</span>
              </div>
            </div>
            
            <div v-if="isOrchestratorTyping" class="ai-message">
              <div class="typing-indicator">
                <span>🤖 Analyzing your context...</span>
                <div class="typing-dots">
                  <span></span><span></span><span></span>
                </div>
              </div>
            </div>
          </div>
          
          <div class="orchestrator-input-area">
            <input 
              v-model="orchestratorInput" 
              @keyup.enter="sendToOrchestrator"
              placeholder="Share your entrepreneurial story, challenges, dreams..."
              class="orchestrator-input"
              :disabled="isOrchestratorTyping"
            />
            <button 
              @click="sendToOrchestrator" 
              :disabled="isOrchestratorTyping || !orchestratorInput.trim()" 
              class="send-button"
            >
              <span v-if="isOrchestratorTyping">⏳</span>
              <span v-else>🚀</span>
            </button>
          </div>
        </div>
      </div>
      
      <!-- Identity Form -->
      <form @submit.prevent="saveIdentity" class="mobile-form">
        <div class="form-section">
          <label class="form-label">Your Name</label>
          <input 
            v-model="identity.name" 
            placeholder="Enter your full name"
            class="form-input"
            @input="updateContext"
          />
        </div>
        
        <div class="form-section">
          <label class="form-label">Entrepreneurial Archetype</label>
          <select v-model="identity.archetype" class="form-input" @change="updateContext">
            <option value="">Select your archetype</option>
            <option value="builder">Builder - Create and construct</option>
            <option value="guide">Guide - Teach and mentor</option>
            <option value="rebel">Rebel - Disrupt and innovate</option>
            <option value="creator">Creator - Design and imagine</option>
            <option value="connector">Connector - Network and unite</option>
          </select>
        </div>
        
        <div class="form-section">
          <label class="form-label">Current Mood & Energy</label>
          <textarea 
            v-model="identity.mood" 
            placeholder="How are you feeling about your entrepreneurial journey?"
            class="form-input form-textarea"
            @input="updateContext"
          ></textarea>
        </div>
        
        <div class="form-section">
          <label class="form-label">Location</label>
          <input 
            v-model="identity.region" 
            placeholder="Where are you based? (e.g., Kraków, Poland)"
            class="form-input"
            @input="updateContext"
          />
        </div>
        
        <div class="form-section">
          <label class="form-label">Industry/Field</label>
          <input 
            v-model="identity.field" 
            placeholder="What industry do you work in?"
            class="form-input"
            @input="updateContext"
          />
        </div>
        
        <div class="form-section">
          <label class="form-label">Professional Title</label>
          <input 
            v-model="identity.selfTitle" 
            placeholder="How do you describe yourself professionally?"
            class="form-input"
            @input="updateContext"
          />
        </div>
        
        <button type="submit" class="primary-button">
          Save Identity & Continue 🚀
        </button>
      </form>
    </div>
  `,
  async mounted() {
    await this.loadIdentity()
    await this.loadContextData()
    this.initializeOrchestrator()
  },
  methods: {
    async loadIdentity() {
      try {
        const response = await fetch('/api/dev/identity')
        if (response.ok) {
          const data = await response.json()
          Object.assign(this.identity, data)
          this.updateContext()
        }
      } catch (error) {
        console.log('Loading identity data...')
      }
    },
    
    async loadContextData() {
      try {
        const response = await fetch('/api/user-context')
        if (response.ok) {
          this.contextData = await response.json()
        }
      } catch (error) {
        console.log('Loading context...')
      }
    },
    
    updateContext() {
      this.contextData.identity = { ...this.identity }
      this.contextData.lastUpdated = new Date().toISOString()
    },
    
    initializeOrchestrator() {
      // Initialize with context-aware greeting
      this.orchestratorMessages.push({
        id: 1,
        type: 'ai',
        content: this.getContextualGreeting(),
        timestamp: new Date(),
        agent_name: 'Identity Orchestrator'
      })
    },
    
    getContextualGreeting() {
      const hasData = this.identity.name || this.identity.archetype || this.identity.field
      
      if (hasData) {
        return `Hello${this.identity.name ? ' ' + this.identity.name : ''}! I can see you've started defining your identity${this.identity.archetype ? ' as a ' + this.identity.archetype : ''}. Let's dive deeper into what makes you unique as an entrepreneur. What aspects of your identity feel most authentic to you right now?`
      } else {
        return `Welcome to your identity discovery journey! I'm here to help you uncover what makes you uniquely positioned as an entrepreneur. Let's start with what drives you - what's the story behind your entrepreneurial ambitions?`
      }
    },
    
    toggleOrchestrator() {
      this.showOrchestrator = !this.showOrchestrator
      if (this.showOrchestrator && this.orchestratorMessages.length === 0) {
        this.initializeOrchestrator()
      }
    },
    
    async sendToOrchestrator() {
      if (!this.orchestratorInput.trim() || this.isOrchestratorTyping) return
      
      const userMessage = this.orchestratorInput.trim()
      this.orchestratorMessages.push({
        id: Date.now(),
        type: 'user',
        content: userMessage,
        timestamp: new Date()
      })
      
      this.orchestratorInput = ''
      this.isOrchestratorTyping = true
      
      try {
        const response = await fetch('/api/dev/context-aware-chat', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            user_message: userMessage,
            section: 'identity',
            current_data: this.identity,
            context: this.contextData
          })
        })
        
        if (response.ok) {
          const data = await response.json()
          this.orchestratorMessages.push({
            id: Date.now() + 1,
            type: 'ai',
            content: data.reply || 'I understand. Let me help you explore this further.',
            timestamp: new Date(),
            agent_name: data.agent_name || 'Identity Orchestrator'
          })
          
          // Apply any form updates suggested by the AI
          if (data.form_updates) {
            Object.assign(this.identity, data.form_updates)
            this.updateContext()
          }
          
        } else {
          throw new Error('Context service unavailable')
        }
      } catch (error) {
        this.orchestratorMessages.push({
          id: Date.now() + 1,
          type: 'ai',
          content: 'I understand you're exploring your identity. What aspects of yourself do you want to express through your business? Think about your core values, unique strengths, and the impact you want to make.',
          timestamp: new Date(),
          agent_name: 'Identity Orchestrator'
        })
      } finally {
        this.isOrchestratorTyping = false
        await this.$nextTick()
        this.scrollToBottom()
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
          
          // Show success and guide to next step
          this.orchestratorMessages.push({
            id: Date.now(),
            type: 'ai',
            content: `Excellent! Your identity is saved. Now let's move to defining your mission - the "why" behind your entrepreneurial journey. Head to the Mission tab when you're ready!`,
            timestamp: new Date(),
            agent_name: 'Identity Orchestrator'
          })
        }
      } catch (error) {
        console.error('Failed to save identity:', error)
      }
    },
    
    formatMessage(text) {
      return text.replace(/\n/g, '<br>')
    },
    
    formatTime(timestamp) {
      return new Date(timestamp).toLocaleTimeString('en-US', { 
        hour: '2-digit', 
        minute: '2-digit' 
      })
    },
    
    scrollToBottom() {
      const container = document.querySelector('.orchestrator-messages')
      if (container) {
        container.scrollTop = container.scrollHeight
      }
    }
  }
}
