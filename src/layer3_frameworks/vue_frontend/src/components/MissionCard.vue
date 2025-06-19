<script setup>
import { ref, onMounted } from 'vue'

const missionData = ref(null)
const isLoading = ref(true)
const error = ref(null)

onMounted(async () => {
  try {
    const response = await fetch('/api/mission')
    if (response.ok) {
      missionData.value = await response.json()
    } else {
      error.value = 'Failed to load mission data'
    }
  } catch (e) {
    error.value = 'Network error'
  } finally {
    isLoading.value = false
  }
})

const completionPercentage = ref(0)
</script>

<template>
  <div class="max-w-4xl mx-auto">
    <div class="mb-6">
      <h1 class="text-2xl font-bold text-zinc-900 dark:text-zinc-100 mb-2">Your Mission</h1>
      <p class="text-zinc-600 dark:text-zinc-400">Define your purpose and create a meaningful business vision</p>
    </div>

    <!-- Loading State -->
    <div v-if="isLoading" class="flex items-center justify-center py-12">
      <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-amber-500"></div>
    </div>

    <!-- Error State -->
    <div v-else-if="error" class="bg-red-50 dark:bg-red-900/30 border border-red-200 dark:border-red-700 rounded-lg p-6">
      <div class="flex items-center gap-3">
        <svg class="w-5 h-5 text-red-500" fill="currentColor" viewBox="0 0 20 20">
          <path d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z"/>
        </svg>
        <span class="text-red-800 dark:text-red-200">{{ error }}</span>
      </div>
    </div>

    <!-- Mission Content -->
    <div v-else class="space-y-6">
      <!-- Progress Overview -->
      <div class="bg-white/60 dark:bg-zinc-800/60 backdrop-blur-sm rounded-xl border border-amber-200/50 dark:border-zinc-700/50 p-6">
        <div class="flex items-center justify-between mb-4">
          <h2 class="text-lg font-semibold text-zinc-900 dark:text-zinc-100">Mission Development Progress</h2>
          <span class="text-2xl font-bold text-amber-600 dark:text-amber-400">{{ completionPercentage }}%</span>
        </div>
        <div class="w-full bg-zinc-200 dark:bg-zinc-700 rounded-full h-3">
          <div class="bg-gradient-to-r from-amber-400 to-orange-500 h-3 rounded-full transition-all duration-500" 
               :style="{ width: completionPercentage + '%' }"></div>
        </div>
      </div>

      <!-- Mission Components Grid -->
      <div class="grid md:grid-cols-2 gap-6">
        <!-- Purpose Statement -->
        <div class="bg-white/60 dark:bg-zinc-800/60 backdrop-blur-sm rounded-xl border border-amber-200/50 dark:border-zinc-700/50 p-6">
          <div class="flex items-center gap-3 mb-4">
            <div class="w-10 h-10 bg-blue-100 dark:bg-blue-900/30 rounded-lg flex items-center justify-center">
              <svg class="w-5 h-5 text-blue-600 dark:text-blue-400" fill="currentColor" viewBox="0 0 20 20">
                <path d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/>
              </svg>
            </div>
            <h3 class="text-lg font-semibold text-zinc-900 dark:text-zinc-100">Purpose Statement</h3>
          </div>
          <p class="text-zinc-600 dark:text-zinc-400 text-sm mb-4">
            Why does your business exist? What change do you want to create?
          </p>
          <div class="space-y-3">
            <div class="p-3 bg-zinc-50 dark:bg-zinc-700/50 rounded-lg border border-zinc-200 dark:border-zinc-600">
              <p class="text-sm text-zinc-700 dark:text-zinc-300 italic">
                "Your purpose statement will appear here once you've defined it..."
              </p>
            </div>
            <button class="w-full text-left text-sm text-blue-600 dark:text-blue-400 hover:text-blue-700 dark:hover:text-blue-300 transition-colors">
              + Define your purpose
            </button>
          </div>
        </div>

        <!-- Vision Statement -->
        <div class="bg-white/60 dark:bg-zinc-800/60 backdrop-blur-sm rounded-xl border border-amber-200/50 dark:border-zinc-700/50 p-6">
          <div class="flex items-center gap-3 mb-4">
            <div class="w-10 h-10 bg-purple-100 dark:bg-purple-900/30 rounded-lg flex items-center justify-center">
              <svg class="w-5 h-5 text-purple-600 dark:text-purple-400" fill="currentColor" viewBox="0 0 20 20">
                <path d="M10 12a2 2 0 100-4 2 2 0 000 4z"/>
                <path d="M10 1C4.477 1 0 5.477 0 11s4.477 10 10 10 10-4.477 10-10S15.523 1 10 1zM2 11a8 8 0 1116 0 8 8 0 01-16 0z"/>
              </svg>
            </div>
            <h3 class="text-lg font-semibold text-zinc-900 dark:text-zinc-100">Vision Statement</h3>
          </div>
          <p class="text-zinc-600 dark:text-zinc-400 text-sm mb-4">
            What does success look like? Where do you see your business in 5 years?
          </p>
          <div class="space-y-3">
            <div class="p-3 bg-zinc-50 dark:bg-zinc-700/50 rounded-lg border border-zinc-200 dark:border-zinc-600">
              <p class="text-sm text-zinc-700 dark:text-zinc-300 italic">
                "Your vision statement will appear here once you've crafted it..."
              </p>
            </div>
            <button class="w-full text-left text-sm text-purple-600 dark:text-purple-400 hover:text-purple-700 dark:hover:text-purple-300 transition-colors">
              + Craft your vision
            </button>
          </div>
        </div>

        <!-- Target Audience -->
        <div class="bg-white/60 dark:bg-zinc-800/60 backdrop-blur-sm rounded-xl border border-amber-200/50 dark:border-zinc-700/50 p-6">
          <div class="flex items-center gap-3 mb-4">
            <div class="w-10 h-10 bg-green-100 dark:bg-green-900/30 rounded-lg flex items-center justify-center">
              <svg class="w-5 h-5 text-green-600 dark:text-green-400" fill="currentColor" viewBox="0 0 20 20">
                <path d="M13 6a3 3 0 11-6 0 3 3 0 016 0zM18 8a2 2 0 11-4 0 2 2 0 014 0zM14 15a4 4 0 00-8 0v3h8v-3z"/>
              </svg>
            </div>
            <h3 class="text-lg font-semibold text-zinc-900 dark:text-zinc-100">Target Audience</h3>
          </div>
          <p class="text-zinc-600 dark:text-zinc-400 text-sm mb-4">
            Who are you serving? What problems are you solving for them?
          </p>
          <div class="space-y-2">
            <div class="flex items-center justify-between text-sm">
              <span class="text-zinc-700 dark:text-zinc-300">Defined segments</span>
              <span class="text-green-600 dark:text-green-400 font-medium">0/3</span>
            </div>
            <button class="w-full text-left text-sm text-green-600 dark:text-green-400 hover:text-green-700 dark:hover:text-green-300 transition-colors">
              + Define your audience
            </button>
          </div>
        </div>

        <!-- Value Proposition -->
        <div class="bg-white/60 dark:bg-zinc-800/60 backdrop-blur-sm rounded-xl border border-amber-200/50 dark:border-zinc-700/50 p-6">
          <div class="flex items-center gap-3 mb-4">
            <div class="w-10 h-10 bg-amber-100 dark:bg-amber-900/30 rounded-lg flex items-center justify-center">
              <svg class="w-5 h-5 text-amber-600 dark:text-amber-400" fill="currentColor" viewBox="0 0 20 20">
                <path d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/>
              </svg>
            </div>
            <h3 class="text-lg font-semibold text-zinc-900 dark:text-zinc-100">Value Proposition</h3>
          </div>
          <p class="text-zinc-600 dark:text-zinc-400 text-sm mb-4">
            What unique value do you provide? Why should customers choose you?
          </p>
          <div class="space-y-2">
            <div class="flex items-center justify-between text-sm">
              <span class="text-zinc-700 dark:text-zinc-300">Components defined</span>
              <span class="text-amber-600 dark:text-amber-400 font-medium">0/4</span>
            </div>
            <button class="w-full text-left text-sm text-amber-600 dark:text-amber-400 hover:text-amber-700 dark:hover:text-amber-300 transition-colors">
              + Build your value prop
            </button>
          </div>
        </div>
      </div>

      <!-- Current Mission Summary -->
      <div class="bg-gradient-to-r from-blue-500 to-purple-500 rounded-xl p-6 text-white">
        <div class="flex items-start gap-4">
          <div class="w-12 h-12 bg-white/20 rounded-lg flex items-center justify-center flex-shrink-0">
            <svg class="w-6 h-6" fill="currentColor" viewBox="0 0 20 20">
              <path d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/>
            </svg>
          </div>
          <div class="flex-1">
            <h3 class="text-lg font-semibold mb-2">Your Mission Draft</h3>
            <p class="text-sm opacity-90 mb-4">
              As you complete each section, your mission statement will take shape here. This will become the guiding principle for all your business decisions.
            </p>
            <div class="bg-white/10 rounded-lg p-4">
              <p class="text-sm italic">
                "To [purpose] for [target audience] by [unique approach] so that [desired outcome]"
              </p>
            </div>
          </div>
        </div>
      </div>

      <!-- Get Started Section -->
      <div class="bg-gradient-to-r from-amber-500 to-orange-500 rounded-xl p-6 text-white">
        <div class="flex items-center gap-4">
          <div class="w-12 h-12 bg-white/20 rounded-lg flex items-center justify-center">
            <svg class="w-6 h-6" fill="currentColor" viewBox="0 0 20 20">
              <path d="M13 6a3 3 0 11-6 0 3 3 0 016 0zM18 8a2 2 0 11-4 0 2 2 0 014 0zM14 15a4 4 0 00-8 0v3h8v-3z"/>
            </svg>
          </div>
          <div class="flex-1">
            <h3 class="text-lg font-semibold mb-1">Ready to Define Your Mission?</h3>
            <p class="text-sm opacity-90">Let's start by exploring your purpose and the impact you want to make.</p>
          </div>
          <button class="bg-white/20 hover:bg-white/30 px-4 py-2 rounded-lg text-sm font-medium transition-colors">
            Begin Mission
          </button>
        </div>
      </div>
    </div>
  </div>
</template>