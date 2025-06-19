<script setup>
import { ref, onMounted } from 'vue'

const roadmapData = ref(null)
const milestones = ref([])
const isLoading = ref(true)
const error = ref(null)

onMounted(async () => {
  try {
    const [roadmapResponse, milestonesResponse] = await Promise.all([
      fetch('/api/roadmap'),
      fetch('/api/milestones')
    ])
    
    if (roadmapResponse.ok) {
      roadmapData.value = await roadmapResponse.json()
    }
    
    if (milestonesResponse.ok) {
      milestones.value = await milestonesResponse.json()
    } else {
      error.value = 'Failed to load roadmap data'
    }
  } catch (e) {
    error.value = 'Network error'
  } finally {
    isLoading.value = false
  }
})

const completionPercentage = ref(25)

const getMilestoneIcon = (index) => {
  const icons = ['🚀', '📊', '💡', '🎯', '📈', '🏆']
  return icons[index % icons.length]
}

const getMilestoneStatus = (milestone) => {
  if (milestone.completed) return 'completed'
  if (milestone.active) return 'active'
  return 'pending'
}
</script>

<template>
  <div class="max-w-4xl mx-auto">
    <div class="mb-6">
      <h1 class="text-2xl font-bold text-zinc-900 dark:text-zinc-100 mb-2">Your Roadmap</h1>
      <p class="text-zinc-600 dark:text-zinc-400">Track your progress and plan your next steps toward entrepreneurial success</p>
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

    <!-- Roadmap Content -->
    <div v-else class="space-y-6">
      <!-- Progress Overview -->
      <div class="bg-white/60 dark:bg-zinc-800/60 backdrop-blur-sm rounded-xl border border-amber-200/50 dark:border-zinc-700/50 p-6">
        <div class="flex items-center justify-between mb-4">
          <h2 class="text-lg font-semibold text-zinc-900 dark:text-zinc-100">Overall Progress</h2>
          <span class="text-2xl font-bold text-amber-600 dark:text-amber-400">{{ completionPercentage }}%</span>
        </div>
        <div class="w-full bg-zinc-200 dark:bg-zinc-700 rounded-full h-3 mb-4">
          <div class="bg-gradient-to-r from-amber-400 to-orange-500 h-3 rounded-full transition-all duration-500" 
               :style="{ width: completionPercentage + '%' }"></div>
        </div>
        <div class="grid grid-cols-3 gap-4 text-center">
          <div>
            <div class="text-2xl font-bold text-green-600 dark:text-green-400">2</div>
            <div class="text-sm text-zinc-600 dark:text-zinc-400">Completed</div>
          </div>
          <div>
            <div class="text-2xl font-bold text-amber-600 dark:text-amber-400">1</div>
            <div class="text-sm text-zinc-600 dark:text-zinc-400">In Progress</div>
          </div>
          <div>
            <div class="text-2xl font-bold text-zinc-400 dark:text-zinc-500">5</div>
            <div class="text-sm text-zinc-600 dark:text-zinc-400">Upcoming</div>
          </div>
        </div>
      </div>

      <!-- Timeline -->
      <div class="bg-white/60 dark:bg-zinc-800/60 backdrop-blur-sm rounded-xl border border-amber-200/50 dark:border-zinc-700/50 p-6">
        <h2 class="text-lg font-semibold text-zinc-900 dark:text-zinc-100 mb-6">Milestone Timeline</h2>
        
        <div class="space-y-4">
          <!-- Sample milestones when API data is empty -->
          <div v-if="!milestones || milestones.length === 0">
            <!-- Milestone 1 - Completed -->
            <div class="flex items-start gap-4 p-4 bg-green-50 dark:bg-green-900/20 rounded-lg border border-green-200 dark:border-green-700">
              <div class="w-10 h-10 bg-green-500 rounded-full flex items-center justify-center text-white font-bold">
                ✓
              </div>
              <div class="flex-1">
                <h3 class="font-semibold text-zinc-900 dark:text-zinc-100">Foundation Setup</h3>
                <p class="text-sm text-zinc-600 dark:text-zinc-400 mb-2">Complete identity discovery and define core values</p>
                <div class="flex items-center gap-4 text-xs text-zinc-500 dark:text-zinc-400">
                  <span class="bg-green-100 dark:bg-green-900/30 text-green-800 dark:text-green-200 px-2 py-1 rounded">Completed</span>
                  <span>Due: Week 1</span>
                </div>
              </div>
            </div>

            <!-- Milestone 2 - Completed -->
            <div class="flex items-start gap-4 p-4 bg-green-50 dark:bg-green-900/20 rounded-lg border border-green-200 dark:border-green-700">
              <div class="w-10 h-10 bg-green-500 rounded-full flex items-center justify-center text-white font-bold">
                ✓
              </div>
              <div class="flex-1">
                <h3 class="font-semibold text-zinc-900 dark:text-zinc-100">Mission Development</h3>
                <p class="text-sm text-zinc-600 dark:text-zinc-400 mb-2">Craft purpose and vision statements</p>
                <div class="flex items-center gap-4 text-xs text-zinc-500 dark:text-zinc-400">
                  <span class="bg-green-100 dark:bg-green-900/30 text-green-800 dark:text-green-200 px-2 py-1 rounded">Completed</span>
                  <span>Due: Week 2</span>
                </div>
              </div>
            </div>

            <!-- Milestone 3 - Active -->
            <div class="flex items-start gap-4 p-4 bg-amber-50 dark:bg-amber-900/20 rounded-lg border border-amber-200 dark:border-amber-700">
              <div class="w-10 h-10 bg-amber-500 rounded-full flex items-center justify-center text-white font-bold">
                3
              </div>
              <div class="flex-1">
                <h3 class="font-semibold text-zinc-900 dark:text-zinc-100">Market Research</h3>
                <p class="text-sm text-zinc-600 dark:text-zinc-400 mb-2">Validate your idea and understand your target market</p>
                <div class="flex items-center gap-4 text-xs text-zinc-500 dark:text-zinc-400">
                  <span class="bg-amber-100 dark:bg-amber-900/30 text-amber-800 dark:text-amber-200 px-2 py-1 rounded">In Progress</span>
                  <span>Due: Week 4</span>
                </div>
                <div class="mt-3">
                  <div class="w-full bg-zinc-200 dark:bg-zinc-700 rounded-full h-2">
                    <div class="bg-amber-500 h-2 rounded-full" style="width: 60%"></div>
                  </div>
                  <div class="text-xs text-amber-600 dark:text-amber-400 mt-1">60% complete</div>
                </div>
              </div>
            </div>

            <!-- Milestone 4 - Pending -->
            <div class="flex items-start gap-4 p-4 bg-zinc-50 dark:bg-zinc-800/50 rounded-lg border border-zinc-200 dark:border-zinc-700">
              <div class="w-10 h-10 bg-zinc-300 dark:bg-zinc-600 rounded-full flex items-center justify-center text-zinc-600 dark:text-zinc-300 font-bold">
                4
              </div>
              <div class="flex-1">
                <h3 class="font-semibold text-zinc-600 dark:text-zinc-300">Business Plan</h3>
                <p class="text-sm text-zinc-500 dark:text-zinc-400 mb-2">Create a comprehensive business plan and financial projections</p>
                <div class="flex items-center gap-4 text-xs text-zinc-500 dark:text-zinc-400">
                  <span class="bg-zinc-200 dark:bg-zinc-700 text-zinc-600 dark:text-zinc-300 px-2 py-1 rounded">Pending</span>
                  <span>Due: Week 6</span>
                </div>
              </div>
            </div>

            <!-- Milestone 5 - Pending -->
            <div class="flex items-start gap-4 p-4 bg-zinc-50 dark:bg-zinc-800/50 rounded-lg border border-zinc-200 dark:border-zinc-700">
              <div class="w-10 h-10 bg-zinc-300 dark:bg-zinc-600 rounded-full flex items-center justify-center text-zinc-600 dark:text-zinc-300 font-bold">
                5
              </div>
              <div class="flex-1">
                <h3 class="font-semibold text-zinc-600 dark:text-zinc-300">MVP Development</h3>
                <p class="text-sm text-zinc-500 dark:text-zinc-400 mb-2">Build and test your minimum viable product</p>
                <div class="flex items-center gap-4 text-xs text-zinc-500 dark:text-zinc-400">
                  <span class="bg-zinc-200 dark:bg-zinc-700 text-zinc-600 dark:text-zinc-300 px-2 py-1 rounded">Pending</span>
                  <span>Due: Week 10</span>
                </div>
              </div>
            </div>
          </div>

          <!-- API milestones when available -->
          <div v-else v-for="(milestone, index) in milestones" :key="milestone.id" 
               :class="[
                 'flex items-start gap-4 p-4 rounded-lg border',
                 getMilestoneStatus(milestone) === 'completed' ? 'bg-green-50 dark:bg-green-900/20 border-green-200 dark:border-green-700' :
                 getMilestoneStatus(milestone) === 'active' ? 'bg-amber-50 dark:bg-amber-900/20 border-amber-200 dark:border-amber-700' :
                 'bg-zinc-50 dark:bg-zinc-800/50 border-zinc-200 dark:border-zinc-700'
               ]">
            <div :class="[
              'w-10 h-10 rounded-full flex items-center justify-center font-bold',
              getMilestoneStatus(milestone) === 'completed' ? 'bg-green-500 text-white' :
              getMilestoneStatus(milestone) === 'active' ? 'bg-amber-500 text-white' :
              'bg-zinc-300 dark:bg-zinc-600 text-zinc-600 dark:text-zinc-300'
            ]">
              {{ getMilestoneStatus(milestone) === 'completed' ? '✓' : index + 1 }}
            </div>
            <div class="flex-1">
              <h3 :class="[
                'font-semibold',
                getMilestoneStatus(milestone) === 'pending' ? 'text-zinc-600 dark:text-zinc-300' : 'text-zinc-900 dark:text-zinc-100'
              ]">{{ milestone.title }}</h3>
              <p :class="[
                'text-sm mb-2',
                getMilestoneStatus(milestone) === 'pending' ? 'text-zinc-500 dark:text-zinc-400' : 'text-zinc-600 dark:text-zinc-400'
              ]">{{ milestone.description }}</p>
              <div class="flex items-center gap-4 text-xs text-zinc-500 dark:text-zinc-400">
                <span :class="[
                  'px-2 py-1 rounded',
                  getMilestoneStatus(milestone) === 'completed' ? 'bg-green-100 dark:bg-green-900/30 text-green-800 dark:text-green-200' :
                  getMilestoneStatus(milestone) === 'active' ? 'bg-amber-100 dark:bg-amber-900/30 text-amber-800 dark:text-amber-200' :
                  'bg-zinc-200 dark:bg-zinc-700 text-zinc-600 dark:text-zinc-300'
                ]">
                  {{ getMilestoneStatus(milestone) === 'completed' ? 'Completed' : 
                     getMilestoneStatus(milestone) === 'active' ? 'In Progress' : 'Pending' }}
                </span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Next Actions -->
      <div class="bg-gradient-to-r from-amber-500 to-orange-500 rounded-xl p-6 text-white">
        <div class="flex items-center gap-4">
          <div class="w-12 h-12 bg-white/20 rounded-lg flex items-center justify-center">
            <svg class="w-6 h-6" fill="currentColor" viewBox="0 0 20 20">
              <path d="M13 6a3 3 0 11-6 0 3 3 0 016 0zM18 8a2 2 0 11-4 0 2 2 0 014 0zM14 15a4 4 0 00-8 0v3h8v-3z"/>
            </svg>
          </div>
          <div class="flex-1">
            <h3 class="text-lg font-semibold mb-1">Ready for Your Next Milestone?</h3>
            <p class="text-sm opacity-90">Continue with market research to validate your business idea.</p>
          </div>
          <button class="bg-white/20 hover:bg-white/30 px-4 py-2 rounded-lg text-sm font-medium transition-colors">
            Continue
          </button>
        </div>
      </div>
    </div>
  </div>
</template>