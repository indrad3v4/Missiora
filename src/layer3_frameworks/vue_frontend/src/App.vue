<script>
import { ref, onMounted } from 'vue'
import { useUserStore } from '@/stores/user.js'
import IdentityCard from '@/components/IdentityCard.vue'
import MissionCard from '@/components/MissionCard.vue'
import RoadmapCard from '@/components/RoadmapCard.vue'
import ChatWidget from '@/components/ChatWidget.vue'

export default {
  name: 'App',
  components: {
    IdentityCard,
    MissionCard,
    RoadmapCard,
    ChatWidget
  },
  setup() {
    const userStore = useUserStore()
    const activeTab = ref('home')
    const messages = ref([])

    onMounted(async () => {
      await userStore.fetchUserData()
    })

    const setActiveTab = (tab) => {
      activeTab.value = tab
    }

    const handleIdentityUpdate = async (newIdentity) => {
      try {
        await userStore.updateIdentity(newIdentity)
      } catch (error) {
        console.error('Failed to update identity:', error)
      }
    }

    const handleMissionUpdate = async (newMission) => {
      try {
        await userStore.updateMission(newMission)
      } catch (error) {
        console.error('Failed to update mission:', error)
      }
    }

    const handleRoadmapUpdate = async (newRoadmap) => {
      try {
        await userStore.updateRoadmap(newRoadmap)
      } catch (error) {
        console.error('Failed to update roadmap:', error)
      }
    }

    const handleSendMessage = async (message) => {
      try {
        const response = await fetch('/api/agent/interact', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({ message })
        })

        if (response.ok) {
          const data = await response.json()
          messages.value.push({
            content: message,
            isUser: true,
            timestamp: new Date()
          })
          messages.value.push({
            content: data.response,
            isUser: false,
            timestamp: new Date()
          })
          
          // Trigger lip-sync animation
          window.dispatchEvent(new CustomEvent('agent-response'))
        }
      } catch (error) {
        console.error('Failed to send message:', error)
      }
    }

    return {
      userStore,
      activeTab,
      messages,
      setActiveTab,
      handleIdentityUpdate,
      handleMissionUpdate,
      handleRoadmapUpdate,
      handleSendMessage
    }
  }
}
</script>

<template>
  <div class="h-screen bg-gradient-to-br from-amber-100 via-orange-100 to-yellow-200 overflow-hidden">
    <!-- Header Card -->
    <div class="absolute top-6 left-6 right-6 z-10">
      <div class="bg-gradient-to-r from-amber-200/80 to-green-200/80 backdrop-blur-sm rounded-2xl p-4 shadow-lg border border-amber-300/50">
        <div class="flex items-center gap-2 mb-2">
          <div class="w-6 h-6 bg-green-400 rounded-full flex items-center justify-center">
            <svg class="w-4 h-4 text-white" fill="currentColor" viewBox="0 0 20 20">
              <path d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/>
            </svg>
          </div>
          <h1 class="font-bold text-xl text-amber-900">
            {{ userStore.identity.name || 'Set up your profile' }}
          </h1>
        </div>
        <div class="space-y-1 text-sm">
          <div class="flex items-center gap-2 text-amber-800">
            <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
              <path d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/>
            </svg>
            <span>{{ userStore.mission.goal || 'Set your goal' }}</span>
          </div>
          <div class="flex items-center gap-2 text-amber-800">
            <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
              <path d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z"/>
              <path d="M15 11a3 3 0 11-6 0 3 3 0 016 0z"/>
            </svg>
            <span>{{ userStore.identity.region || 'Location' }}</span>
          </div>
          <div class="flex items-center gap-2 text-amber-800">
            <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
              <path d="M10 18a8 8 0 100-16 8 8 0 000 16zm1-12a1 1 0 10-2 0v4a1 1 0 00.293.707l2.828 2.829a1 1 0 101.415-1.415L11 9.586V6z"/>
            </svg>
            <span>Q3 2025</span>
          </div>
        </div>
      </div>
    </div>

    <!-- Main Content Area -->
    <main class="h-full flex flex-col pt-32 pb-32">
      <!-- Identity Card -->
      <IdentityCard 
        v-if="activeTab === 'identity'" 
        :identity="userStore.identity"
        :completion="userStore.identityCompletion"
        @update="handleIdentityUpdate"
      />
      
      <!-- Mission Card -->
      <MissionCard 
        v-else-if="activeTab === 'mission'" 
        :mission="userStore.mission"
        :completion="userStore.missionCompletion"
        @update="handleMissionUpdate"
      />
      
      <!-- Roadmap Card -->
      <RoadmapCard 
        v-else-if="activeTab === 'roadmap'" 
        :roadmap="userStore.roadmap"
        :completion="userStore.roadmapCompletion"
        @update="handleRoadmapUpdate"
      />
      
      <!-- Default: Tamagotchi AI Character -->
      <div v-else class="flex-1 flex items-center justify-center relative">
        <!-- Tamagotchi AI Character -->
        <div class="relative animate-float">
          <!-- Glowing base -->
          <div class="absolute bottom-0 left-1/2 transform -translate-x-1/2 w-24 h-8 bg-gradient-to-r from-emerald-400/30 to-green-400/30 rounded-full blur-lg animate-pulse-slow"></div>
          
          <!-- AI Character Body -->
          <div class="relative w-32 h-40 bg-gradient-to-b from-emerald-200/80 to-green-300/80 rounded-full animate-glow backdrop-blur-sm border-2 border-emerald-300/50 shadow-2xl">
            <!-- Character Face -->
            <div class="absolute top-8 left-1/2 transform -translate-x-1/2">
              <!-- Eyes -->
              <div class="flex gap-4 mb-2">
                <div class="w-3 h-1 bg-emerald-800 rounded-full"></div>
                <div class="w-3 h-1 bg-emerald-800 rounded-full"></div>
              </div>
              <!-- Smile -->
              <div class="w-6 h-3 border-b-2 border-emerald-800 rounded-full"></div>
            </div>
            
            <!-- Lotus Symbol in Body -->
            <div class="absolute top-16 left-1/2 transform -translate-x-1/2">
              <svg class="w-8 h-8 text-emerald-600/60" fill="currentColor" viewBox="0 0 24 24">
                <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-2 15l-5-5 1.41-1.41L10 14.17l7.59-7.59L19 8l-9 9z"/>
              </svg>
            </div>
            
            <!-- Arms -->
            <div class="absolute top-20 -left-4 w-8 h-12 bg-gradient-to-b from-emerald-200/60 to-green-300/60 rounded-full transform -rotate-12"></div>
            <div class="absolute top-20 -right-4 w-8 h-12 bg-gradient-to-b from-emerald-200/60 to-green-300/60 rounded-full transform rotate-12"></div>
          </div>
        </div>

        <!-- Chat Widget -->
        <ChatWidget 
          :messages="messages"
          @send="handleSendMessage"
        />
      </div>
    </main>

    <!-- Bottom Navigation -->
    <nav class="absolute bottom-0 left-6 right-6 mb-6">
      <div class="bg-amber-200/80 backdrop-blur-sm rounded-2xl p-2 shadow-lg border border-amber-300/50">
        <div class="flex justify-around">
          <button 
            @click="setActiveTab('identity')"
            :class="[
              'flex-1 py-3 px-4 text-center transition-all duration-200 flex flex-col items-center gap-1 rounded-xl',
              activeTab === 'identity' ? 'bg-amber-300/50 text-amber-900' : 'text-amber-800 hover:bg-amber-300/30'
            ]"
          >
            <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
              <path d="M10 9a3 3 0 100-6 3 3 0 000 6zm-7 9a7 7 0 1114 0H3z"/>
            </svg>
            <span class="text-xs font-medium">Identity</span>
          </button>
          
          <button 
            @click="setActiveTab('mission')"
            :class="[
              'flex-1 py-3 px-4 text-center transition-all duration-200 flex flex-col items-center gap-1 rounded-xl',
              activeTab === 'mission' ? 'bg-amber-300/50 text-amber-900' : 'text-amber-800 hover:bg-amber-300/30'
            ]"
          >
            <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
              <path d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/>
            </svg>
            <span class="text-xs font-medium">Mission</span>
          </button>
          
          <button 
            @click="setActiveTab('roadmap')"
            :class="[
              'flex-1 py-3 px-4 text-center transition-all duration-200 flex flex-col items-center gap-1 rounded-xl',
              activeTab === 'roadmap' ? 'bg-amber-300/50 text-amber-900' : 'text-amber-800 hover:bg-amber-300/30'
            ]"
          >
            <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
              <path d="M9 17V7m0 10a2 2 0 01-2 2H5a2 2 0 01-2-2V7a2 2 0 012-2h2a2 2 0 012 2m0 10a2 2 0 002 2h2a2 2 0 002-2M9 7a2 2 0 012-2h2a2 2 0 012 2v10a2 2 0 01-2 2H9V7z"/>
            </svg>
            <span class="text-xs font-medium">Roadmap</span>
          </button>
        </div>
      </div>
    </nav>
  </div>
</template>

<style>
/* Global styles */
body {
  font-family: system-ui, -apple-system, sans-serif;
}

/* Custom scrollbar */
::-webkit-scrollbar {
  width: 6px;
}

::-webkit-scrollbar-track {
  background: transparent;
}

::-webkit-scrollbar-thumb {
  background: rgba(251, 191, 36, 0.3);
  border-radius: 3px;
}

::-webkit-scrollbar-thumb:hover {
  background: rgba(251, 191, 36, 0.5);
}
</style>