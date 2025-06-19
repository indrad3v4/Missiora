<script setup>
import { ref, onMounted } from 'vue'

const emit = defineEmits(['switch-tab'])
const message = ref('')
const messages = ref([])
const isLoading = ref(false)
const messageCount = ref(0)
const showLoginPrompt = ref(false)

onMounted(async () => {
  // Check auth status and message count
  try {
    const response = await fetch('/api/auth/status')
    if (response.ok) {
      const data = await response.json()
      messageCount.value = data.message_count || 0
      showLoginPrompt.value = messageCount.value >= 10 && !data.authenticated
    }
  } catch (e) {
    console.error('Failed to check auth status:', e)
  }
})

const sendMessage = async () => {
  if (!message.value.trim() || isLoading.value) return

  const userMessage = message.value.trim()
  message.value = ''
  
  // Add user message to chat
  messages.value.push({
    content: userMessage,
    isUser: true,
    timestamp: new Date()
  })

  isLoading.value = true

  try {
    const response = await fetch('/api/agent/interact', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ message: userMessage })
    })

    if (response.ok) {
      const data = await response.json()
      messages.value.push({
        content: data.response || 'I received your message.',
        isUser: false,
        timestamp: new Date()
      })
      
      messageCount.value++
      if (messageCount.value >= 10) {
        showLoginPrompt.value = true
      }
    } else {
      throw new Error('Failed to get response')
    }
  } catch (e) {
    messages.value.push({
      content: 'Sorry, I encountered an error. Please try again.',
      isUser: false,
      timestamp: new Date(),
      isError: true
    })
  } finally {
    isLoading.value = false
  }
}

const handleKeydown = (event) => {
  if (event.key === 'Enter' && !event.shiftKey) {
    event.preventDefault()
    sendMessage()
  }
}
</script>

<template>
  <div class="max-w-2xl mx-auto w-full">
    <!-- Login Prompt Banner -->
    <div v-if="showLoginPrompt" class="mb-6 p-4 bg-amber-100 dark:bg-amber-900/30 border border-amber-200 dark:border-amber-700 rounded-lg">
      <div class="flex items-center gap-3">
        <svg class="w-5 h-5 text-amber-600 dark:text-amber-400" fill="currentColor" viewBox="0 0 20 20">
          <path d="M10 2L3 7v11a1 1 0 001 1h12a1 1 0 001-1V7l-7-5zM9 10a1 1 0 112 0v3a1 1 0 11-2 0v-3z"/>
        </svg>
        <div>
          <p class="text-sm font-medium text-amber-800 dark:text-amber-200">Ready for more personalized guidance?</p>
          <p class="text-xs text-amber-600 dark:text-amber-300">Create an account to continue your journey with unlimited conversations.</p>
        </div>
      </div>
    </div>

    <!-- Initial Chat Bubble -->
    <div v-if="messages.length === 0" class="text-center mb-8">
      <div class="inline-block bg-white/60 dark:bg-zinc-800/60 backdrop-blur-sm p-8 rounded-2xl shadow-lg border border-amber-200/50 dark:border-zinc-700/50">
        <div class="mb-4">
          <div class="w-12 h-12 mx-auto bg-gradient-to-br from-amber-400 to-orange-400 rounded-full flex items-center justify-center shadow-lg">
            <svg class="w-6 h-6 text-white" fill="currentColor" viewBox="0 0 20 20">
              <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z"/>
            </svg>
          </div>
        </div>
        <h2 class="text-2xl font-semibold text-zinc-900 dark:text-zinc-100 mb-3">
          What lights you up today?
        </h2>
        <p class="text-zinc-600 dark:text-zinc-400 text-sm">
          Share what excites you, and I'll help you turn it into actionable steps toward your entrepreneurial goals.
        </p>
      </div>
    </div>

    <!-- Chat Messages -->
    <div v-if="messages.length > 0" class="space-y-4 mb-6 max-h-96 overflow-y-auto">
      <div v-for="(msg, index) in messages" :key="index" 
           :class="[
             'flex',
             msg.isUser ? 'justify-end' : 'justify-start'
           ]">
        <div :class="[
          'max-w-xs sm:max-w-md p-3 rounded-lg',
          msg.isUser 
            ? 'bg-amber-500 text-white' 
            : msg.isError 
              ? 'bg-red-100 dark:bg-red-900/30 text-red-800 dark:text-red-200'
              : 'bg-white dark:bg-zinc-800 text-zinc-900 dark:text-zinc-100 shadow-sm border border-zinc-200 dark:border-zinc-700'
        ]">
          <p class="text-sm whitespace-pre-wrap">{{ msg.content }}</p>
          <p class="text-xs opacity-70 mt-1">
            {{ new Date(msg.timestamp).toLocaleTimeString() }}
          </p>
        </div>
      </div>
    </div>

    <!-- Input Area -->
    <div class="bg-white/60 dark:bg-zinc-800/60 backdrop-blur-sm rounded-xl border border-amber-200/50 dark:border-zinc-700/50 p-4">
      <div class="flex gap-3">
        <textarea
          v-model="message"
          @keydown="handleKeydown"
          :disabled="isLoading"
          placeholder="Share what's on your mind..."
          class="flex-1 resize-none border-0 bg-transparent text-zinc-900 dark:text-zinc-100 placeholder-zinc-500 dark:placeholder-zinc-400 focus:outline-none text-sm"
          rows="1"
        ></textarea>
        <button
          @click="sendMessage"
          :disabled="!message.trim() || isLoading"
          :class="[
            'px-4 py-2 rounded-lg text-sm font-medium transition-colors duration-200',
            message.trim() && !isLoading
              ? 'bg-amber-500 hover:bg-amber-600 text-white'
              : 'bg-zinc-200 dark:bg-zinc-700 text-zinc-400 dark:text-zinc-500 cursor-not-allowed'
          ]"
        >
          <svg v-if="isLoading" class="w-4 h-4 animate-spin" fill="none" viewBox="0 0 24 24">
            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
            <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
          </svg>
          <span v-else>Send</span>
        </button>
      </div>
      <div class="flex justify-between items-center mt-3 text-xs text-zinc-500 dark:text-zinc-400">
        <span>Press Enter to send, Shift+Enter for new line</span>
        <span v-if="!showLoginPrompt">{{ messageCount }}/10 messages</span>
      </div>
    </div>
  </div>
</template>