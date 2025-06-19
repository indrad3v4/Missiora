<template>
  <div class="absolute bottom-32 left-8 right-8">
    <!-- Chat Messages -->
    <div v-if="messages.length > 0" class="mb-4 max-h-48 overflow-y-auto space-y-2">
      <div 
        v-for="(message, index) in messages" 
        :key="index"
        :class="[
          'flex',
          message.isUser ? 'justify-end' : 'justify-start'
        ]"
      >
        <div 
          :class="[
            'max-w-xs p-3 rounded-lg text-sm',
            message.isUser 
              ? 'bg-amber-500 text-white' 
              : 'bg-white/90 text-amber-900 border border-amber-300'
          ]"
        >
          {{ message.content }}
        </div>
      </div>
    </div>

    <!-- Chat Bubble or Input -->
    <div v-if="!isInputVisible" @click="showInput" class="cursor-pointer">
      <div class="relative bg-amber-200/90 backdrop-blur-sm rounded-2xl p-4 shadow-lg border border-amber-300/50 transform transition-transform hover:scale-105">
        <div class="absolute bottom-0 left-8 w-0 h-0 border-l-8 border-r-8 border-t-8 border-l-transparent border-r-transparent border-t-amber-200/90 transform translate-y-full"></div>
        <p class="text-amber-900 font-medium text-lg">
          What lights you up today?
        </p>
      </div>
    </div>

    <!-- Input Area -->
    <div v-else class="bg-white/90 backdrop-blur-sm rounded-2xl border border-amber-300/50 p-4 shadow-lg">
      <div class="flex gap-3">
        <textarea
          ref="messageInput"
          v-model="currentMessage"
          @keydown="handleKeydown"
          :disabled="isLoading"
          placeholder="Share what's on your mind..."
          class="flex-1 resize-none border-0 bg-transparent text-amber-900 placeholder-amber-600 focus:outline-none text-sm"
          rows="1"
        ></textarea>
        <button
          @click="sendMessage"
          :disabled="!currentMessage.trim() || isLoading"
          :class="[
            'px-4 py-2 rounded-lg text-sm font-medium transition-colors duration-200',
            currentMessage.trim() && !isLoading
              ? 'bg-amber-500 hover:bg-amber-600 text-white'
              : 'bg-amber-200 text-amber-500 cursor-not-allowed'
          ]"
        >
          <svg v-if="isLoading" class="w-4 h-4 animate-spin" fill="none" viewBox="0 0 24 24">
            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
            <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
          </svg>
          <span v-else>Send</span>
        </button>
      </div>
      <div class="flex justify-between items-center mt-3 text-xs text-amber-600">
        <span>Press Enter to send, Shift+Enter for new line</span>
        <button @click="hideInput" class="text-amber-500 hover:text-amber-700">Close</button>
      </div>
    </div>

    <!-- Video Feed Component -->
    <VideoFeed v-if="isInputVisible" />
  </div>
</template>

<script>
import { ref, nextTick } from 'vue'
import VideoFeed from './VideoFeed.vue'

export default {
  name: 'ChatWidget',
  components: {
    VideoFeed
  },
  props: {
    messages: {
      type: Array,
      default: () => []
    }
  },
  emits: ['send'],
  setup(props, { emit }) {
    const currentMessage = ref('')
    const isInputVisible = ref(false)
    const isLoading = ref(false)
    const messageInput = ref(null)

    const showInput = async () => {
      isInputVisible.value = true
      await nextTick()
      messageInput.value?.focus()
    }

    const hideInput = () => {
      isInputVisible.value = false
      currentMessage.value = ''
    }

    const sendMessage = async () => {
      if (!currentMessage.value.trim() || isLoading.value) return

      const message = currentMessage.value.trim()
      currentMessage.value = ''
      isLoading.value = true

      try {
        await emit('send', message)
      } catch (error) {
        console.error('Failed to send message:', error)
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

    return {
      currentMessage,
      isInputVisible,
      isLoading,
      messageInput,
      showInput,
      hideInput,
      sendMessage,
      handleKeydown
    }
  }
}
</script>