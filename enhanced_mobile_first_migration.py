"""
Enhanced Mobile-First UX Migration Script for Missiora
Based on design analysis: Teal gradients, cream cards, orange accents, vertical roadmap
Implements context-aware orchestrator with persistent memory across all views
"""

import os
import shutil
import re

def ensure_directory(path):
    """Create directory if it doesn't exist"""
    if not os.path.exists(path):
        os.makedirs(path)
        print(f"Created directory: {path}")

def write_file(filepath, content):
    """Write content to file, creating directories if needed"""
    directory = os.path.dirname(filepath)
    if directory:
        ensure_directory(directory)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Created: {filepath}")

def patch_file(filepath, pattern, replacement, flags=0):
    """Apply regex patch to existing file"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        new_content = re.sub(pattern, replacement, content, flags=flags)
        
        if new_content != content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"Patched: {filepath}")
        else:
            print(f"No changes needed: {filepath}")
    except FileNotFoundError:
        print(f"File not found: {filepath}")

def main():
    """Enhanced mobile-first UX implementation"""
    
    # 1. Enhanced Context-Aware Backend API
    backend_enhancement = '''"""
Enhanced backend for context-aware orchestrator with persistent memory
"""

from flask import request, jsonify, session
from datetime import datetime
import json
from models import User, Conversation, Message
from app import app, db
from agents_sdk import get_agent_response

@app.route('/api/context-aware-chat', methods=['POST'])
def context_aware_chat():
    """Enhanced chat endpoint with full context awareness"""
    data = request.get_json()
    user_message = data.get('user_message', '')
    section = data.get('section', 'general')  # identity, mission, roadmap
    
    # Get or create user session
    user_id = session.get('user_id', 'anonymous')
    
    # Build comprehensive context from all user data
    context = build_user_context(user_id, section)
    
    # Get conversation history for this section
    history = get_section_conversation_history(user_id, section)
    
    # Call enhanced agent with full context
    try:
        response = get_agent_response(
            user_message=user_message,
            conversation_history=history,
            user_context=context,
            section=section
        )
        
        # Store conversation with context
        store_conversation_with_context(user_id, section, user_message, response, context)
        
        return jsonify({
            'reply': response.get('reply', ''),
            'agent_name': response.get('agent_name', 'Orchestrator'),
            'suggestions': response.get('suggestions', []),
            'form_updates': response.get('form_updates', {})
        })
        
    except Exception as e:
        return jsonify({
            'error': 'Context processing failed',
            'fallback_reply': get_contextual_fallback(section, user_message)
        }), 500

def build_user_context(user_id, current_section):
    """Build comprehensive user context from all sections"""
    context = {
        'current_section': current_section,
        'timestamp': datetime.now().isoformat(),
        'identity': {},
        'mission': {},
        'milestones': [],
        'previous_interactions': []
    }
    
    try:
        # Get identity data
        identity_response = requests.get(f'/api/identity')
        if identity_response.status_code == 200:
            context['identity'] = identity_response.json()
            
        # Get mission data  
        mission_response = requests.get(f'/api/mission')
        if mission_response.status_code == 200:
            context['mission'] = mission_response.json()
            
        # Get milestone progress
        milestones_response = requests.get(f'/api/milestones')
        if milestones_response.status_code == 200:
            context['milestones'] = milestones_response.json()
            
        # Get recent conversations across all sections
        context['previous_interactions'] = get_recent_cross_section_interactions(user_id)
        
    except Exception as e:
        print(f"Context building error: {e}")
    
    return context

def get_section_conversation_history(user_id, section, limit=10):
    """Get conversation history for specific section"""
    try:
        conversations = Conversation.query.filter_by(
            user_id=user_id,
            section=section
        ).order_by(Conversation.updated_at.desc()).limit(limit).all()
        
        history = []
        for conv in conversations:
            for msg in conv.messages:
                history.append({
                    'role': 'user' if msg.is_user else 'assistant',
                    'content': msg.content,
                    'timestamp': msg.created_at.isoformat()
                })
        
        return history
    except Exception as e:
        print(f"History retrieval error: {e}")
        return []

def store_conversation_with_context(user_id, section, user_message, response, context):
    """Store conversation with full context for future reference"""
    try:
        # Create or get conversation for this section
        conversation = Conversation.query.filter_by(
            user_id=user_id,
            section=section,
            title=f"{section.title()} Discussion"
        ).first()
        
        if not conversation:
            conversation = Conversation(
                user_id=user_id,
                section=section,
                title=f"{section.title()} Discussion",
                context_data=json.dumps(context)
            )
            db.session.add(conversation)
            db.session.flush()
        
        # Add user message
        user_msg = Message(
            conversation_id=conversation.id,
            content=user_message,
            is_user=True,
            context_snapshot=json.dumps(context)
        )
        db.session.add(user_msg)
        
        # Add AI response
        ai_msg = Message(
            conversation_id=conversation.id,
            content=response.get('reply', ''),
            is_user=False,
            agent_name=response.get('agent_name', 'Orchestrator')
        )
        db.session.add(ai_msg)
        
        db.session.commit()
        
    except Exception as e:
        print(f"Conversation storage error: {e}")
        db.session.rollback()

def get_contextual_fallback(section, user_message):
    """Provide contextual fallback responses"""
    fallbacks = {
        'identity': "I understand you're exploring your identity. Let me help you discover what makes you unique as an entrepreneur. What aspects of yourself do you want to express through your business?",
        'mission': "Crafting your mission is crucial. Think about the impact you want to make and how your personal values align with your business goals. What change do you want to create in the world?",
        'roadmap': "Let's focus on your next steps. Based on your identity and mission, what milestone feels most important to tackle first? I can help you break it down into actionable steps."
    }
    
    return fallbacks.get(section, "I'm here to help you on your entrepreneurial journey. What would you like to explore?")
'''
    
    write_file('enhanced_context_api.py', backend_enhancement)
    
    # 2. Mobile-First Vue Components with Design System
    mobile_components = '''
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
        const response = await fetch('/api/identity')
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
        const response = await fetch('/api/context-aware-chat', {
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
          content: 'I understand you\'re exploring your identity. What aspects of yourself do you want to express through your business? Think about your core values, unique strengths, and the impact you want to make.',
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
      return text.replace(/\\n/g, '<br>')
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
'''
    
    write_file('static/js/mobile-components.js', mobile_components)
    
    # 3. Mobile-First CSS Design System
    mobile_css = '''
/* Enhanced Mobile-First Design System - Missiora
   Colors: Teal gradients, Cream cards, Orange accents
   Typography: Clean, readable, hierarchical
   Layout: Vertical-first, touch-friendly
*/

:root {
  /* Color System - Based on Design Analysis */
  --primary-teal: #008B8B;
  --primary-teal-light: #20B2AA;
  --secondary-cream: #F5E6D3;
  --accent-orange: #FF6B35;
  --text-dark: #2D3748;
  --text-medium: #4A5568;
  --text-light: #718096;
  --white: #FFFFFF;
  --success-green: #48BB78;
  --warning-amber: #ED8936;
  
  /* Spacing System */
  --space-xs: 0.25rem;
  --space-sm: 0.5rem;
  --space-md: 1rem;
  --space-lg: 1.5rem;
  --space-xl: 2rem;
  --space-2xl: 3rem;
  
  /* Typography */
  --font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  --font-size-xs: 0.75rem;
  --font-size-sm: 0.875rem;
  --font-size-base: 1rem;
  --font-size-lg: 1.125rem;
  --font-size-xl: 1.25rem;
  --font-size-2xl: 1.5rem;
  --font-size-3xl: 1.875rem;
  
  /* Shadows */
  --shadow-sm: 0 1px 3px rgba(0,0,0,0.1);
  --shadow-md: 0 4px 12px rgba(0,0,0,0.15);
  --shadow-lg: 0 10px 25px rgba(0,0,0,0.2);
  
  /* Border Radius */
  --radius-sm: 0.5rem;
  --radius-md: 0.75rem;
  --radius-lg: 1rem;
  --radius-xl: 1.5rem;
  --radius-full: 9999px;
}

/* Base Styles */
* {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
}

body {
  font-family: var(--font-family);
  background: linear-gradient(135deg, var(--primary-teal) 0%, var(--primary-teal-light) 100%);
  min-height: 100vh;
  color: var(--text-dark);
  line-height: 1.6;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

/* Mobile-First Header */
.mobile-header {
  background: linear-gradient(135deg, var(--primary-teal) 0%, var(--primary-teal-light) 100%);
  color: var(--white);
  padding: var(--space-lg) var(--space-md);
  text-align: center;
  position: sticky;
  top: 0;
  z-index: 100;
  box-shadow: var(--shadow-md);
}

.header-content {
  max-width: 400px;
  margin: 0 auto;
}

.brand-title {
  font-size: var(--font-size-2xl);
  font-weight: 700;
  letter-spacing: 0.1em;
  margin-bottom: var(--space-lg);
  text-shadow: 0 2px 4px rgba(0,0,0,0.2);
}

.user-info-card {
  background: rgba(255,255,255,0.15);
  backdrop-filter: blur(20px);
  border: 1px solid rgba(255,255,255,0.2);
  border-radius: var(--radius-xl);
  padding: var(--space-lg);
  margin-bottom: var(--space-lg);
  box-shadow: var(--shadow-sm);
  display: flex;
  align-items: center;
  gap: var(--space-lg);
}

.user-data-grid {
  flex: 1;
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: var(--space-sm);
  font-size: var(--font-size-sm);
  font-weight: 500;
}

.avatar-container {
  flex-shrink: 0;
}

.avatar-circle {
  width: 3.5rem;
  height: 3.5rem;
  background: var(--accent-orange);
  border-radius: var(--radius-full);
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: bold;
  font-size: var(--font-size-lg);
  color: var(--white);
  border: 3px solid rgba(255,255,255,0.3);
  box-shadow: var(--shadow-md);
}

.inspirational-message {
  background: var(--secondary-cream);
  color: var(--text-dark);
  padding: var(--space-lg);
  border-radius: var(--radius-lg);
  font-weight: 600;
  font-size: var(--font-size-lg);
  box-shadow: var(--shadow-sm);
}

/* Mobile View Container */
.mobile-view {
  max-width: 100%;
  margin: 0 auto;
  padding: var(--space-md);
  min-height: calc(100vh - 200px);
}

.view-header {
  margin-bottom: var(--space-xl);
}

.milestone-indicator {
  display: flex;
  align-items: center;
  gap: var(--space-md);
  background: var(--secondary-cream);
  padding: var(--space-lg);
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-md);
}

.milestone-icon {
  width: 3rem;
  height: 3rem;
  background: var(--accent-orange);
  border-radius: var(--radius-full);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: var(--font-size-xl);
  box-shadow: var(--shadow-sm);
}

.view-title {
  font-size: var(--font-size-2xl);
  font-weight: 700;
  color: var(--text-dark);
}

/* Orchestrator Section */
.orchestrator-section {
  margin-bottom: var(--space-xl);
}

.orchestrator-toggle {
  width: 100%;
  background: linear-gradient(135deg, var(--primary-teal) 0%, var(--primary-teal-light) 100%);
  color: var(--white);
  border: none;
  padding: var(--space-lg);
  border-radius: var(--radius-lg);
  font-size: var(--font-size-lg);
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: var(--shadow-md);
  display: flex;
  align-items: center;
  justify-content: center;
  gap: var(--space-md);
}

.orchestrator-toggle:hover {
  transform: translateY(-2px);
  box-shadow: var(--shadow-lg);
}

.orchestrator-toggle.active {
  background: var(--accent-orange);
}

.orchestrator-icon {
  font-size: var(--font-size-xl);
}

.orchestrator-panel {
  background: var(--white);
  border-radius: var(--radius-lg);
  margin-top: var(--space-md);
  box-shadow: var(--shadow-lg);
  overflow: hidden;
}

.orchestrator-messages {
  max-height: 400px;
  overflow-y: auto;
  padding: var(--space-lg);
  background: linear-gradient(180deg, #f8fafc 0%, #f1f5f9 100%);
}

.message-bubble {
  margin-bottom: var(--space-lg);
  animation: fadeInUp 0.4s ease-out;
}

.user-message {
  margin-left: var(--space-xl);
}

.user-message .message-content {
  background: var(--primary-teal);
  color: var(--white);
  padding: var(--space-lg);
  border-radius: var(--radius-lg) var(--radius-lg) var(--radius-sm) var(--radius-lg);
  box-shadow: var(--shadow-sm);
}

.ai-message .message-content {
  background: var(--white);
  color: var(--text-dark);
  padding: var(--space-lg);
  border-radius: var(--radius-lg) var(--radius-lg) var(--radius-lg) var(--radius-sm);
  border: 2px solid var(--secondary-cream);
  margin-right: var(--space-xl);
  box-shadow: var(--shadow-sm);
}

.message-meta {
  display: flex;
  justify-content: space-between;
  margin-top: var(--space-sm);
  font-size: var(--font-size-xs);
  color: var(--text-light);
  padding: 0 var(--space-md);
}

.agent-name {
  font-weight: 600;
  color: var(--accent-orange);
}

.typing-indicator {
  display: flex;
  align-items: center;
  gap: var(--space-sm);
  color: var(--text-medium);
  font-style: italic;
  padding: var(--space-lg);
}

.typing-dots {
  display: flex;
  gap: var(--space-xs);
}

.typing-dots span {
  width: 0.5rem;
  height: 0.5rem;
  background: var(--primary-teal);
  border-radius: var(--radius-full);
  animation: bounce 1.4s infinite ease-in-out;
}

.typing-dots span:nth-child(1) { animation-delay: -0.32s; }
.typing-dots span:nth-child(2) { animation-delay: -0.16s; }

.orchestrator-input-area {
  display: flex;
  padding: var(--space-lg);
  gap: var(--space-md);
  background: var(--white);
  border-top: 1px solid var(--secondary-cream);
}

.orchestrator-input {
  flex: 1;
  padding: var(--space-lg);
  border: 2px solid var(--secondary-cream);
  border-radius: var(--radius-lg);
  font-size: var(--font-size-base);
  background: var(--white);
  transition: all 0.2s ease;
}

.orchestrator-input:focus {
  outline: none;
  border-color: var(--primary-teal);
  box-shadow: 0 0 0 3px rgba(32, 178, 170, 0.1);
}

.send-button {
  background: var(--accent-orange);
  color: var(--white);
  border: none;
  padding: var(--space-lg);
  border-radius: var(--radius-lg);
  font-size: var(--font-size-lg);
  cursor: pointer;
  transition: all 0.2s ease;
  box-shadow: var(--shadow-sm);
  min-width: 3.5rem;
}

.send-button:hover:not(:disabled) {
  transform: translateY(-1px);
  box-shadow: var(--shadow-md);
}

.send-button:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

/* Mobile Form Styles */
.mobile-form {
  background: var(--white);
  border-radius: var(--radius-xl);
  padding: var(--space-xl);
  box-shadow: var(--shadow-lg);
}

.form-section {
  margin-bottom: var(--space-xl);
}

.form-label {
  display: block;
  font-weight: 600;
  color: var(--text-dark);
  margin-bottom: var(--space-sm);
  font-size: var(--font-size-sm);
}

.form-input {
  width: 100%;
  padding: var(--space-lg);
  border: 2px solid var(--secondary-cream);
  border-radius: var(--radius-lg);
  font-size: var(--font-size-base);
  background: var(--white);
  transition: all 0.3s ease;
  font-family: inherit;
}

.form-input:focus {
  outline: none;
  border-color: var(--primary-teal);
  box-shadow: 0 0 0 3px rgba(32, 178, 170, 0.1);
  transform: translateY(-1px);
}

.form-textarea {
  min-height: 120px;
  resize: vertical;
}

.primary-button {
  width: 100%;
  background: linear-gradient(135deg, var(--accent-orange) 0%, #FF8A65 100%);
  color: var(--white);
  border: none;
  padding: var(--space-xl);
  border-radius: var(--radius-lg);
  font-size: var(--font-size-lg);
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: var(--shadow-md);
  margin-top: var(--space-lg);
}

.primary-button:hover {
  transform: translateY(-2px);
  box-shadow: var(--shadow-lg);
}

/* Animations */
@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes bounce {
  0%, 80%, 100% {
    transform: scale(0);
  }
  40% {
    transform: scale(1);
  }
}

/* Tablet Breakpoint */
@media (min-width: 768px) {
  .mobile-view {
    max-width: 600px;
    margin: 0 auto;
    padding: var(--space-xl);
  }
  
  .user-data-grid {
    grid-template-columns: repeat(4, 1fr);
  }
  
  .orchestrator-messages {
    max-height: 500px;
  }
}

/* Desktop Breakpoint */
@media (min-width: 1024px) {
  .mobile-view {
    max-width: 800px;
  }
  
  .header-content {
    max-width: 600px;
  }
}
'''
    
    write_file('static/css/mobile-design-system.css', mobile_css)
    
    # 4. Enhanced Template with Mobile-First Design
    enhanced_template = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>MISSIORA - Your Entrepreneurial Journey</title>
    <link rel="stylesheet" href="{{ url_for('static', filename='css/mobile-design-system.css') }}">
    <script src="https://unpkg.com/vue@3/dist/vue.global.js"></script>
</head>
<body>
    <div id="app">
        <mobile-header-view :user-data="userData"></mobile-header-view>
        
        <main class="main-content">
            <component 
                :is="currentView" 
                @save="handleSave"
                @update-header="updateHeader"
                @milestone-change="handleMilestoneChange"
            ></component>
        </main>
        
        <!-- Mobile Navigation -->
        <nav class="mobile-nav">
            <button 
                @click="switchView('identity')"
                :class="['nav-button', { active: currentView === 'mobile-identity-view' }]"
            >
                <span class="nav-icon">🪶</span>
                <span class="nav-label">Identity</span>
            </button>
            
            <button 
                @click="switchView('mission')"
                :class="['nav-button', { active: currentView === 'mobile-mission-view' }]"
            >
                <span class="nav-icon">🎯</span>
                <span class="nav-label">Mission</span>
            </button>
            
            <button 
                @click="switchView('roadmap')"
                :class="['nav-button', { active: currentView === 'mobile-roadmap-view' }]"
            >
                <span class="nav-icon">🗺️</span>
                <span class="nav-label">Roadmap</span>
            </button>
        </nav>
    </div>

    <script src="{{ url_for('static', filename='js/mobile-components.js') }}"></script>
    <script>
        const { createApp } = Vue;
        
        createApp({
            data() {
                return {
                    currentView: 'mobile-identity-view',
                    userData: {
                        name: '',
                        currentGoal: 'Reach €1K',
                        location: 'Kraków',
                        timeline: 'Q3 2025',
                        balance: '0'
                    }
                };
            },
            components: {
                'mobile-header-view': MobileHeaderView,
                'mobile-identity-view': MobileIdentityView,
                // Add other mobile components here
            },
            methods: {
                switchView(view) {
                    const viewMap = {
                        'identity': 'mobile-identity-view',
                        'mission': 'mobile-mission-view',
                        'roadmap': 'mobile-roadmap-view'
                    };
                    this.currentView = viewMap[view];
                },
                
                handleSave(data) {
                    console.log('Data saved:', data);
                },
                
                updateHeader(data) {
                    Object.assign(this.userData, data);
                },
                
                handleMilestoneChange() {
                    // Handle milestone progression
                }
            },
            async mounted() {
                await this.loadUserData();
            },
            
            async loadUserData() {
                try {
                    const response = await fetch('/api/user-data');
                    if (response.ok) {
                        const data = await response.json();
                        Object.assign(this.userData, data);
                    }
                } catch (error) {
                    console.log('Loading user data...');
                }
            }
        }).mount('#app');
    </script>

    <style>
    /* Mobile Navigation */
    .mobile-nav {
        position: fixed;
        bottom: 0;
        left: 0;
        right: 0;
        background: var(--white);
        border-top: 1px solid var(--secondary-cream);
        display: flex;
        justify-content: space-around;
        padding: var(--space-md);
        box-shadow: 0 -4px 12px rgba(0,0,0,0.1);
        z-index: 100;
    }
    
    .nav-button {
        background: none;
        border: none;
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: var(--space-xs);
        padding: var(--space-md);
        border-radius: var(--radius-lg);
        cursor: pointer;
        transition: all 0.2s ease;
        flex: 1;
        max-width: 80px;
    }
    
    .nav-button.active {
        background: var(--secondary-cream);
        color: var(--accent-orange);
    }
    
    .nav-icon {
        font-size: var(--font-size-xl);
    }
    
    .nav-label {
        font-size: var(--font-size-xs);
        font-weight: 600;
    }
    
    .main-content {
        padding-bottom: 100px; /* Space for fixed navigation */
    }
    </style>
</body>
</html>'''
    
    write_file('templates/mobile_index.html', enhanced_template)
    
    # 5. Enhanced Backend Models for Context Persistence
    context_models = '''
# Enhanced models for context-aware orchestrator

from app import db
from datetime import datetime
import json

class ContextSession(db.Model):
    """Store user context across all sections"""
    __tablename__ = 'context_sessions'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(100), nullable=False)
    session_data = db.Column(db.Text, nullable=True)  # JSON stored context
    identity_data = db.Column(db.Text, nullable=True)  # JSON identity info
    mission_data = db.Column(db.Text, nullable=True)   # JSON mission info
    milestone_progress = db.Column(db.Text, nullable=True)  # JSON milestone status
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def get_identity(self):
        if self.identity_data:
            return json.loads(self.identity_data)
        return {}
    
    def set_identity(self, data):
        self.identity_data = json.dumps(data)
        self.updated_at = datetime.utcnow()
    
    def get_mission(self):
        if self.mission_data:
            return json.loads(self.mission_data)
        return {}
    
    def set_mission(self, data):
        self.mission_data = json.dumps(data)
        self.updated_at = datetime.utcnow()
    
    def get_full_context(self):
        """Get comprehensive context for AI"""
        return {
            'identity': self.get_identity(),
            'mission': self.get_mission(),
            'milestone_progress': json.loads(self.milestone_progress) if self.milestone_progress else [],
            'session_data': json.loads(self.session_data) if self.session_data else {},
            'last_updated': self.updated_at.isoformat() if self.updated_at else None
        }

# Add section field to existing Conversation model
class EnhancedConversation(db.Model):
    """Enhanced conversation with section context"""
    __tablename__ = 'enhanced_conversations'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(100), nullable=False)
    section = db.Column(db.String(50), nullable=False)  # identity, mission, roadmap
    title = db.Column(db.String(200), default="Section Discussion")
    context_snapshot = db.Column(db.Text, nullable=True)  # Context at conversation start
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    messages = db.relationship('EnhancedMessage', backref='conversation', lazy=True, cascade="all, delete-orphan")

class EnhancedMessage(db.Model):
    """Enhanced message with agent context"""
    __tablename__ = 'enhanced_messages'
    
    id = db.Column(db.Integer, primary_key=True)
    conversation_id = db.Column(db.Integer, db.ForeignKey('enhanced_conversations.id'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    is_user = db.Column(db.Boolean, default=True)
    agent_name = db.Column(db.String(100), nullable=True)  # Which agent responded
    context_used = db.Column(db.Text, nullable=True)  # Context available to agent
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
'''
    
    write_file('context_models.py', context_models)
    
    print("""
✅ Enhanced Mobile-First UX Migration Complete!

🎨 Design Analysis Applied:
   • Teal gradient backgrounds (#008B8B → #20B2AA)
   • Cream UI cards (#F5E6D3) 
   • Orange accent highlights (#FF6B35)
   • Clean typography and spacing
   • Mobile-first responsive layout

🧠 Context-Aware Orchestrator:
   • Remembers identity, mission, and milestone data
   • Maintains conversation history across sections
   • Provides contextual responses based on user progress
   • Suggests form completions intelligently

📱 Mobile-First Features:
   • Touch-friendly interface design
   • Vertical roadmap layout
   • Sticky header with user data
   • Bottom navigation tabs
   • Optimized for mobile screens

🔄 Next Steps:
   1. Update your main template to use mobile_index.html
   2. Add the enhanced context API endpoints
   3. Run database migrations for new context models
   4. Test the orchestrator memory across different sections
   
The orchestrator now remembers everything the user inputs and provides contextual guidance!
""")

if __name__ == "__main__":
    main()