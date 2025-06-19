<script setup>
import { ref, onMounted } from 'vue'
import ChatWidget from './components/ChatWidget.vue'
import IdentityCard from './components/IdentityCard.vue'
import MissionCard from './components/MissionCard.vue'
import RoadmapCard from './components/RoadmapCard.vue'

const auth = ref(null)
const error = ref(null)
const activeTab = ref('chat')
const userName = ref('Indradeva')
const userGoal = ref('Reach €1K')
const userLocation = ref('Kraków')
const userTimeline = ref('Q3 2025')

onMounted(async () => {
  try {
    const response = await fetch('/api/auth/status')
    if (response.ok) {
      auth.value = await response.json()
    }
  } catch (e) {
    error.value = 'Network error'
  }
})

const setActiveTab = (tab) => {
  activeTab.value = tab
}
</script>

<template>
  <div class="min-h-screen flex flex-col bg-gradient-to-br from-amber-50 via-orange-50 to-yellow-50 dark:from-zinc-900 dark:via-zinc-800 dark:to-zinc-900 text-zinc-800 dark:text-zinc-100">
    <!-- Header / Avatar panel -->
    <header class="p-6 flex items-center gap-4 bg-white/40 dark:bg-zinc-800/40 backdrop-blur-sm border-b border-amber-200/50 dark:border-zinc-700/50">
      <div class="relative">
        <div class="w-16 h-16 rounded-full bg-gradient-to-br from-amber-200 to-amber-300 dark:from-amber-500 dark:to-amber-600 flex items-center justify-center ring-2 ring-amber-400/50 shadow-lg">
          <div class="w-12 h-12 rounded-full bg-gradient-to-br from-emerald-200 to-emerald-300 dark:from-emerald-400 dark:to-emerald-500 flex items-center justify-center">
            <svg class="w-6 h-6 text-emerald-700 dark:text-emerald-200" fill="currentColor" viewBox="0 0 20 20">
              <path d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/>
            </svg>
          </div>
        </div>
        <div class="absolute -bottom-1 -right-1 w-5 h-5 bg-green-400 rounded-full border-2 border-white dark:border-zinc-800"></div>
      </div>
      <div class="flex-1">
        <h1 class="font-semibold text-xl text-zinc-900 dark:text-zinc-100">{{ userName }}</h1>
        <div class="flex items-center gap-4 text-sm text-zinc-600 dark:text-zinc-400 mt-1">
          <div class="flex items-center gap-1">
            <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
              <path d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/>
            </svg>
            {{ userGoal }}
          </div>
          <div class="flex items-center gap-1">
            <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
              <path d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z"/>
              <path d="M15 11a3 3 0 11-6 0 3 3 0 016 0z"/>
            </svg>
            {{ userLocation }}
          </div>
          <div class="flex items-center gap-1">
            <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
              <path d="M10 18a8 8 0 100-16 8 8 0 000 16zm1-12a1 1 0 10-2 0v4a1 1 0 00.293.707l2.828 2.829a1 1 0 101.415-1.415L11 9.586V6z"/>
            </svg>
            {{ userTimeline }}
          </div>
        </div>
      </div>
      <div class="flex items-center gap-2">
        <div class="w-2 h-2 bg-green-400 rounded-full animate-pulse"></div>
        <span class="text-xs text-zinc-500 dark:text-zinc-400">Online</span>
      </div>
    </header>

    <!-- Main Content Area -->
    <main class="flex-1 p-6">
      <!-- Chat View (Default) -->
      <div v-if="activeTab === 'chat'" class="h-full flex items-center justify-center">
        <ChatWidget @switch-tab="setActiveTab" />
      </div>

      <!-- Identity Tab -->
      <div v-else-if="activeTab === 'identity'" class="h-full">
        <IdentityCard />
      </div>

      <!-- Mission Tab -->
      <div v-else-if="activeTab === 'mission'" class="h-full">
        <MissionCard />
      </div>

      <!-- Roadmap Tab -->
      <div v-else-if="activeTab === 'roadmap'" class="h-full">
        <RoadmapCard />
      </div>
    </main>

    <!-- Bottom Navigation -->
    <nav class="border-t border-amber-200/50 dark:border-zinc-700/50 bg-white/60 dark:bg-zinc-800/60 backdrop-blur-sm">
      <div class="flex">
        <button 
          @click="setActiveTab('identity')"
          :class="[
            'flex-1 py-4 px-2 text-center transition-colors duration-200 flex flex-col items-center gap-1',
            activeTab === 'identity' ? 'text-amber-600 dark:text-amber-400 bg-amber-50/50 dark:bg-amber-900/20' : 'text-zinc-600 dark:text-zinc-400 hover:text-amber-500 dark:hover:text-amber-300'
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
            'flex-1 py-4 px-2 text-center transition-colors duration-200 flex flex-col items-center gap-1',
            activeTab === 'mission' ? 'text-amber-600 dark:text-amber-400 bg-amber-50/50 dark:bg-amber-900/20' : 'text-zinc-600 dark:text-zinc-400 hover:text-amber-500 dark:hover:text-amber-300'
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
            'flex-1 py-4 px-2 text-center transition-colors duration-200 flex flex-col items-center gap-1',
            activeTab === 'roadmap' ? 'text-amber-600 dark:text-amber-400 bg-amber-50/50 dark:bg-amber-900/20' : 'text-zinc-600 dark:text-zinc-400 hover:text-amber-500 dark:hover:text-amber-300'
          ]"
        >
          <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
            <path d="M9 17V7m0 10a2 2 0 01-2 2H5a2 2 0 01-2-2V7a2 2 0 012-2h2a2 2 0 012 2m0 10a2 2 0 002 2h2a2 2 0 002-2M9 7a2 2 0 012-2h2a2 2 0 012 2v10a2 2 0 01-2 2H9V7z"/>
          </svg>
          <span class="text-xs font-medium">Roadmap</span>
        </button>

        <button 
          @click="setActiveTab('chat')"
          :class="[
            'flex-1 py-4 px-2 text-center transition-colors duration-200 flex flex-col items-center gap-1',
            activeTab === 'chat' ? 'text-amber-600 dark:text-amber-400 bg-amber-50/50 dark:bg-amber-900/20' : 'text-zinc-600 dark:text-zinc-400 hover:text-amber-500 dark:hover:text-amber-300'
          ]"
        >
          <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
            <path d="M2 5a2 2 0 012-2h7a2 2 0 012 2v4a2 2 0 01-2 2H9l-3 3v-3H4a2 2 0 01-2-2V5z"/>
            <path d="M15 7v2a4 4 0 01-4 4H9.828l-1.766 1.767c.28.149.599.233.938.233h2l3 3v-3h2a2 2 0 002-2V9a2 2 0 00-2-2h-1z"/>
          </svg>
          <span class="text-xs font-medium">Chat</span>
        </button>
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