<template>
  <div class="flex-1 flex items-center justify-center p-6">
    <div class="w-full max-w-md bg-white/90 backdrop-blur-sm rounded-2xl shadow-lg border border-amber-300/50 p-6">
      <div class="flex items-center justify-between mb-4">
        <h2 class="text-xl font-bold text-amber-900">Mission</h2>
        <div class="flex items-center gap-2">
          <div class="w-12 h-2 bg-amber-200 rounded-full overflow-hidden">
            <div 
              class="h-full bg-green-500 transition-all duration-300"
              :style="{ width: `${completion}%` }"
            ></div>
          </div>
          <span class="text-sm text-amber-700">{{ completion }}%</span>
        </div>
      </div>

      <form @submit.prevent="handleSubmit" class="space-y-4">
        <div>
          <label class="block text-sm font-medium text-amber-800 mb-1">Mission Statement</label>
          <textarea 
            v-model="formData.statement"
            rows="4"
            class="w-full px-3 py-2 border border-amber-300 rounded-lg focus:ring-2 focus:ring-amber-500 focus:border-transparent resize-none"
            placeholder="What is your core mission and purpose?"
          ></textarea>
        </div>

        <div>
          <label class="block text-sm font-medium text-amber-800 mb-1">Primary Goal</label>
          <input 
            v-model="formData.goal"
            type="text" 
            class="w-full px-3 py-2 border border-amber-300 rounded-lg focus:ring-2 focus:ring-amber-500 focus:border-transparent"
            placeholder="e.g., Reach €1K MRR"
          />
        </div>

        <div>
          <label class="block text-sm font-medium text-amber-800 mb-1">Current Blocks</label>
          <textarea 
            v-model="formData.blocks"
            rows="3"
            class="w-full px-3 py-2 border border-amber-300 rounded-lg focus:ring-2 focus:ring-amber-500 focus:border-transparent resize-none"
            placeholder="What obstacles are you facing?"
          ></textarea>
        </div>

        <div class="flex gap-3 pt-4">
          <button 
            type="submit"
            :disabled="isLoading"
            class="flex-1 bg-amber-500 text-white py-2 px-4 rounded-lg font-medium hover:bg-amber-600 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {{ isLoading ? 'Saving...' : 'Save Mission' }}
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script>
import { ref, watch } from 'vue'

export default {
  name: 'MissionCard',
  props: {
    mission: {
      type: Object,
      default: () => ({})
    },
    completion: {
      type: Number,
      default: 0
    }
  },
  emits: ['update'],
  setup(props, { emit }) {
    const isLoading = ref(false)
    const formData = ref({
      statement: '',
      goal: '',
      blocks: ''
    })

    // Watch for prop changes and update form
    watch(() => props.mission, (newMission) => {
      if (newMission) {
        formData.value = { ...formData.value, ...newMission }
      }
    }, { immediate: true, deep: true })

    const handleSubmit = async () => {
      isLoading.value = true
      try {
        await emit('update', formData.value)
      } catch (error) {
        console.error('Failed to update mission:', error)
      } finally {
        isLoading.value = false
      }
    }

    return {
      formData,
      isLoading,
      handleSubmit
    }
  }
}
</script>