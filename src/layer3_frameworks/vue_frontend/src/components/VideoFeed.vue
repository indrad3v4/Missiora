<template>
  <div class="absolute top-4 right-4 w-32 h-24 bg-black/20 rounded-lg overflow-hidden border border-amber-300/50">
    <!-- Video Element -->
    <video 
      ref="videoElement"
      class="w-full h-full object-cover"
      autoplay
      muted
      playsinline
    ></video>
    
    <!-- Avatar Overlay -->
    <div class="absolute inset-0 flex items-center justify-center">
      <div 
        :class="[
          'w-16 h-20 rounded-full transition-all duration-300',
          isListening ? 'animate-pulse-slow' : ''
        ]"
      >
        <!-- Tamagotchi Avatar SVG -->
        <svg viewBox="0 0 64 80" class="w-full h-full">
          <!-- Body -->
          <ellipse 
            cx="32" cy="50" rx="24" ry="28" 
            :fill="isListening ? 'rgba(34, 197, 94, 0.8)' : 'rgba(34, 197, 94, 0.6)'"
            stroke="rgba(34, 197, 94, 0.9)" 
            stroke-width="2"
          />
          
          <!-- Eyes -->
          <circle cx="26" cy="35" r="2" fill="#065f46" />
          <circle cx="38" cy="35" r="2" fill="#065f46" />
          
          <!-- Mouth -->
          <path 
            d="M 28 45 Q 32 48 36 45" 
            stroke="#065f46" 
            stroke-width="2" 
            fill="none" 
            stroke-linecap="round"
            :class="{ 'animate-pulse': isListening }"
          />
          
          <!-- Lotus Symbol -->
          <g transform="translate(32, 55)">
            <circle r="4" fill="rgba(6, 95, 70, 0.3)" />
            <path 
              d="M -2 -1 Q 0 -3 2 -1 Q 0 1 -2 -1 Z" 
              fill="#065f46" 
              opacity="0.6"
            />
          </g>
        </svg>
      </div>
    </div>

    <!-- Permission Request -->
    <div v-if="showPermissionRequest" class="absolute inset-0 bg-black/50 flex items-center justify-center">
      <button 
        @click="requestCameraPermission"
        class="bg-amber-500 text-white px-3 py-1 rounded text-xs hover:bg-amber-600 transition-colors"
      >
        Enable Camera
      </button>
    </div>

    <!-- Error State -->
    <div v-if="error" class="absolute inset-0 bg-red-500/20 flex items-center justify-center">
      <div class="text-xs text-red-800 text-center p-2">
        Camera not available
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted, onUnmounted } from 'vue'

export default {
  name: 'VideoFeed',
  setup() {
    const videoElement = ref(null)
    const showPermissionRequest = ref(false)
    const isListening = ref(false)
    const error = ref(false)
    let stream = null

    const requestCameraPermission = async () => {
      try {
        stream = await navigator.mediaDevices.getUserMedia({ 
          video: { 
            width: 320, 
            height: 240,
            facingMode: 'user'
          }, 
          audio: false 
        })
        
        if (videoElement.value) {
          videoElement.value.srcObject = stream
        }
        
        showPermissionRequest.value = false
        error.value = false
      } catch (err) {
        console.error('Camera permission denied:', err)
        error.value = true
        showPermissionRequest.value = false
      }
    }

    const startListening = () => {
      isListening.value = true
      // Simulate lip-sync animation
      setTimeout(() => {
        isListening.value = false
      }, 2000)
    }

    onMounted(async () => {
      // Check if camera is available
      if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
        showPermissionRequest.value = true
        
        // Auto-request permission after a short delay
        setTimeout(() => {
          requestCameraPermission()
        }, 1000)
      } else {
        error.value = true
      }

      // Listen for agent responses to trigger lip-sync
      window.addEventListener('agent-response', startListening)
    })

    onUnmounted(() => {
      if (stream) {
        stream.getTracks().forEach(track => track.stop())
      }
      window.removeEventListener('agent-response', startListening)
    })

    return {
      videoElement,
      showPermissionRequest,
      isListening,
      error,
      requestCameraPermission
    }
  }
}
</script>