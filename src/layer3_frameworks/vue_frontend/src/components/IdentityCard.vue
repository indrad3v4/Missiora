<script setup>
import { ref, onMounted } from 'vue'

const identityData = ref(null)
const isLoading = ref(true)
const error = ref(null)

onMounted(async () => {
  try {
    const response = await fetch('/api/identity')
    if (response.ok) {
      identityData.value = await response.json()
    } else {
      error.value = 'Failed to load identity data'
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
      <h1 class="text-2xl font-bold text-zinc-900 dark:text-zinc-100 mb-2">Your Identity</h1>
      <p class="text-zinc-600 dark:text-zinc-400">Discover and define your authentic entrepreneurial self</p>
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

    <!-- Identity Content -->
    <div v-else class="space-y-6">
      <!-- Progress Overview -->
      <div class="bg-white/60 dark:bg-zinc-800/60 backdrop-blur-sm rounded-xl border border-amber-200/50 dark:border-zinc-700/50 p-6">
        <div class="flex items-center justify-between mb-4">
          <h2 class="text-lg font-semibold text-zinc-900 dark:text-zinc-100">Identity Discovery Progress</h2>
          <span class="text-2xl font-bold text-amber-600 dark:text-amber-400">{{ completionPercentage }}%</span>
        </div>
        <div class="w-full bg-zinc-200 dark:bg-zinc-700 rounded-full h-3">
          <div class="bg-gradient-to-r from-amber-400 to-orange-500 h-3 rounded-full transition-all duration-500" 
               :style="{ width: completionPercentage + '%' }"></div>
        </div>
      </div>

      <!-- Identity Cards Grid -->
      <div class="grid md:grid-cols-2 gap-6">
        <!-- Core Values -->
        <div class="bg-white/60 dark:bg-zinc-800/60 backdrop-blur-sm rounded-xl border border-amber-200/50 dark:border-zinc-700/50 p-6">
          <div class="flex items-center gap-3 mb-4">
            <div class="w-10 h-10 bg-amber-100 dark:bg-amber-900/30 rounded-lg flex items-center justify-center">
              <svg class="w-5 h-5 text-amber-600 dark:text-amber-400" fill="currentColor" viewBox="0 0 20 20">
                <path d="M3.172 5.172a4 4 0 015.656 0L10 6.343l1.172-1.171a4 4 0 115.656 5.656L10 17.657l-6.828-6.829a4 4 0 010-5.656z"/>
              </svg>
            </div>
            <h3 class="text-lg font-semibold text-zinc-900 dark:text-zinc-100">Core Values</h3>
          </div>
          <p class="text-zinc-600 dark:text-zinc-400 text-sm mb-4">
            What principles guide your decisions and define who you are?
          </p>
          <div class="space-y-2">
            <div class="flex items-center justify-between text-sm">
              <span class="text-zinc-700 dark:text-zinc-300">Discovered</span>
              <span class="text-amber-600 dark:text-amber-400 font-medium">0/5</span>
            </div>
            <button class="w-full text-left text-sm text-amber-600 dark:text-amber-400 hover:text-amber-700 dark:hover:text-amber-300 transition-colors">
              + Start values discovery
            </button>
          </div>
        </div>

        <!-- Strengths -->
        <div class="bg-white/60 dark:bg-zinc-800/60 backdrop-blur-sm rounded-xl border border-amber-200/50 dark:border-zinc-700/50 p-6">
          <div class="flex items-center gap-3 mb-4">
            <div class="w-10 h-10 bg-green-100 dark:bg-green-900/30 rounded-lg flex items-center justify-center">
              <svg class="w-5 h-5 text-green-600 dark:text-green-400" fill="currentColor" viewBox="0 0 20 20">
                <path d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/>
              </svg>
            </div>
            <h3 class="text-lg font-semibold text-zinc-900 dark:text-zinc-100">Strengths</h3>
          </div>
          <p class="text-zinc-600 dark:text-zinc-400 text-sm mb-4">
            Your natural talents and acquired skills that set you apart.
          </p>
          <div class="space-y-2">
            <div class="flex items-center justify-between text-sm">
              <span class="text-zinc-700 dark:text-zinc-300">Identified</span>
              <span class="text-green-600 dark:text-green-400 font-medium">0/8</span>
            </div>
            <button class="w-full text-left text-sm text-green-600 dark:text-green-400 hover:text-green-700 dark:hover:text-green-300 transition-colors">
              + Explore your strengths
            </button>
          </div>
        </div>

        <!-- Passions -->
        <div class="bg-white/60 dark:bg-zinc-800/60 backdrop-blur-sm rounded-xl border border-amber-200/50 dark:border-zinc-700/50 p-6">
          <div class="flex items-center gap-3 mb-4">
            <div class="w-10 h-10 bg-purple-100 dark:bg-purple-900/30 rounded-lg flex items-center justify-center">
              <svg class="w-5 h-5 text-purple-600 dark:text-purple-400" fill="currentColor" viewBox="0 0 20 20">
                <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z"/>
              </svg>
            </div>
            <h3 class="text-lg font-semibold text-zinc-900 dark:text-zinc-100">Passions</h3>
          </div>
          <p class="text-zinc-600 dark:text-zinc-400 text-sm mb-4">
            What energizes you and makes time fly when you're doing it?
          </p>
          <div class="space-y-2">
            <div class="flex items-center justify-between text-sm">
              <span class="text-zinc-700 dark:text-zinc-300">Explored</span>
              <span class="text-purple-600 dark:text-purple-400 font-medium">0/3</span>
            </div>
            <button class="w-full text-left text-sm text-purple-600 dark:text-purple-400 hover:text-purple-700 dark:hover:text-purple-300 transition-colors">
              + Discover your passions
            </button>
          </div>
        </div>

        <!-- Life Experiences -->
        <div class="bg-white/60 dark:bg-zinc-800/60 backdrop-blur-sm rounded-xl border border-amber-200/50 dark:border-zinc-700/50 p-6">
          <div class="flex items-center gap-3 mb-4">
            <div class="w-10 h-10 bg-blue-100 dark:bg-blue-900/30 rounded-lg flex items-center justify-center">
              <svg class="w-5 h-5 text-blue-600 dark:text-blue-400" fill="currentColor" viewBox="0 0 20 20">
                <path d="M13 6a3 3 0 11-6 0 3 3 0 016 0zM18 8a2 2 0 11-4 0 2 2 0 014 0zM14 15a4 4 0 00-8 0v3h8v-3z"/>
              </svg>
            </div>
            <h3 class="text-lg font-semibold text-zinc-900 dark:text-zinc-100">Life Experiences</h3>
          </div>
          <p class="text-zinc-600 dark:text-zinc-400 text-sm mb-4">
            Key moments and experiences that shaped your entrepreneurial journey.
          </p>
          <div class="space-y-2">
            <div class="flex items-center justify-between text-sm">
              <span class="text-zinc-700 dark:text-zinc-300">Captured</span>
              <span class="text-blue-600 dark:text-blue-400 font-medium">0/5</span>
            </div>
            <button class="w-full text-left text-sm text-blue-600 dark:text-blue-400 hover:text-blue-700 dark:hover:text-blue-300 transition-colors">
              + Share your story
            </button>
          </div>
        </div>
      </div>

      <!-- Get Started Section -->
      <div class="bg-gradient-to-r from-amber-500 to-orange-500 rounded-xl p-6 text-white">
        <div class="flex items-center gap-4">
          <div class="w-12 h-12 bg-white/20 rounded-lg flex items-center justify-center">
            <svg class="w-6 h-6" fill="currentColor" viewBox="0 0 20 20">
              <path d="M10 2L3 7v11a1 1 0 001 1h12a1 1 0 001-1V7l-7-5zM9 10a1 1 0 112 0v3a1 1 0 11-2 0v-3z"/>
            </svg>
          </div>
          <div class="flex-1">
            <h3 class="text-lg font-semibold mb-1">Ready to Begin Your Identity Journey?</h3>
            <p class="text-sm opacity-90">Start with a simple conversation about what makes you unique.</p>
          </div>
          <button class="bg-white/20 hover:bg-white/30 px-4 py-2 rounded-lg text-sm font-medium transition-colors">
            Start Now
          </button>
        </div>
      </div>
    </div>
  </div>
</template>