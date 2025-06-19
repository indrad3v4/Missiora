<template>
  <div class="flex-1 flex items-center justify-center p-6">
    <div class="w-full max-w-md bg-white/90 backdrop-blur-sm rounded-2xl shadow-lg border border-amber-300/50 p-6">
      <div class="flex items-center justify-between mb-4">
        <h2 class="text-xl font-bold text-amber-900">Roadmap</h2>
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

      <div class="space-y-4">
        <div>
          <label class="block text-sm font-medium text-amber-800 mb-1">Roadmap Title</label>
          <input 
            v-model="formData.title"
            type="text" 
            class="w-full px-3 py-2 border border-amber-300 rounded-lg focus:ring-2 focus:ring-amber-500 focus:border-transparent"
            placeholder="Your roadmap title"
          />
        </div>

        <div>
          <label class="block text-sm font-medium text-amber-800 mb-1">Description</label>
          <textarea 
            v-model="formData.description"
            rows="3"
            class="w-full px-3 py-2 border border-amber-300 rounded-lg focus:ring-2 focus:ring-amber-500 focus:border-transparent resize-none"
            placeholder="Describe your roadmap..."
          ></textarea>
        </div>

        <!-- Milestones List -->
        <div v-if="roadmap.milestones && roadmap.milestones.length > 0">
          <h3 class="text-sm font-medium text-amber-800 mb-2">Milestones</h3>
          <div class="space-y-2">
            <div 
              v-for="milestone in roadmap.milestones" 
              :key="milestone.id"
              class="flex items-center gap-3 p-3 bg-amber-50 rounded-lg"
            >
              <div class="flex-shrink-0">
                <div 
                  :class="[
                    'w-4 h-4 rounded-full border-2',
                    milestone.completed 
                      ? 'bg-green-500 border-green-500' 
                      : milestone.active 
                        ? 'bg-amber-500 border-amber-500' 
                        : 'bg-white border-amber-300'
                  ]"
                ></div>
              </div>
              <div class="flex-1">
                <h4 class="text-sm font-medium text-amber-900">{{ milestone.title }}</h4>
                <p class="text-xs text-amber-700">{{ milestone.description }}</p>
              </div>
              <div class="text-xs text-amber-600">
                {{ milestone.completed ? 'Complete' : milestone.active ? 'Active' : 'Pending' }}
              </div>
            </div>
          </div>
        </div>

        <div class="flex gap-3 pt-4">
          <button 
            @click="handleSubmit"
            :disabled="isLoading"
            class="flex-1 bg-amber-500 text-white py-2 px-4 rounded-lg font-medium hover:bg-amber-600 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {{ isLoading ? 'Saving...' : 'Save Roadmap' }}
          </button>
          <button 
            @click="generateRoadmap"
            :disabled="isLoading"
            class="bg-green-500 text-white py-2 px-4 rounded-lg font-medium hover:bg-green-600 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
          >
            Generate
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, watch } from 'vue'

export default {
  name: 'RoadmapCard',
  props: {
    roadmap: {
      type: Object,
      default: () => ({ milestones: [] })
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
      title: '',
      description: '',
      milestones: []
    })

    // Watch for prop changes and update form
    watch(() => props.roadmap, (newRoadmap) => {
      if (newRoadmap) {
        formData.value = { ...formData.value, ...newRoadmap }
      }
    }, { immediate: true, deep: true })

    const handleSubmit = async () => {
      isLoading.value = true
      try {
        await emit('update', formData.value)
      } catch (error) {
        console.error('Failed to update roadmap:', error)
      } finally {
        isLoading.value = false
      }
    }

    const generateRoadmap = async () => {
      isLoading.value = true
      try {
        const response = await fetch('/api/roadmap/generate', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          }
        })

        if (response.ok) {
          const generatedRoadmap = await response.json()
          formData.value = { ...formData.value, ...generatedRoadmap }
          await emit('update', formData.value)
        }
      } catch (error) {
        console.error('Failed to generate roadmap:', error)
      } finally {
        isLoading.value = false
      }
    }

    return {
      formData,
      isLoading,
      handleSubmit,
      generateRoadmap
    }
  }
}
</script>