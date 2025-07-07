<template>
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
</style>