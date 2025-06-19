<template>
  <div class="flex-1 flex items-center justify-center p-6">
    <div class="w-full max-w-md bg-white/90 backdrop-blur-sm rounded-2xl shadow-lg border border-amber-300/50 p-6">
      <div class="flex items-center justify-between mb-4">
        <h2 class="text-xl font-bold text-amber-900">Identity</h2>
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
          <label class="block text-sm font-medium text-amber-800 mb-1">Name</label>
          <input 
            v-model="formData.name"
            type="text" 
            class="w-full px-3 py-2 border border-amber-300 rounded-lg focus:ring-2 focus:ring-amber-500 focus:border-transparent"
            placeholder="Your name"
          />
        </div>

        <div>
          <label class="block text-sm font-medium text-amber-800 mb-1">Archetype</label>
          <select 
            v-model="formData.archetype"
            class="w-full px-3 py-2 border border-amber-300 rounded-lg focus:ring-2 focus:ring-amber-500 focus:border-transparent"
          >
            <option value="">Select archetype</option>
            <option value="Visionary">Visionary</option>
            <option value="Builder">Builder</option>
            <option value="Connector">Connector</option>
            <option value="Optimizer">Optimizer</option>
          </select>
        </div>

        <div>
          <label class="block text-sm font-medium text-amber-800 mb-1">Current Mood</label>
          <input 
            v-model="formData.mood"
            type="text" 
            class="w-full px-3 py-2 border border-amber-300 rounded-lg focus:ring-2 focus:ring-amber-500 focus:border-transparent"
            placeholder="How are you feeling today?"
          />
        </div>

        <div>
          <label class="block text-sm font-medium text-amber-800 mb-1">Region</label>
          <input 
            v-model="formData.region"
            type="text" 
            class="w-full px-3 py-2 border border-amber-300 rounded-lg focus:ring-2 focus:ring-amber-500 focus:border-transparent"
            placeholder="Your location"
          />
        </div>

        <div>
          <label class="block text-sm font-medium text-amber-800 mb-1">Field</label>
          <input 
            v-model="formData.field"
            type="text" 
            class="w-full px-3 py-2 border border-amber-300 rounded-lg focus:ring-2 focus:ring-amber-500 focus:border-transparent"
            placeholder="Your area of expertise"
          />
        </div>

        <div>
          <label class="block text-sm font-medium text-amber-800 mb-1">Self Title</label>
          <input 
            v-model="formData.self_title"
            type="text" 
            class="w-full px-3 py-2 border border-amber-300 rounded-lg focus:ring-2 focus:ring-amber-500 focus:border-transparent"
            placeholder="How do you describe yourself?"
          />
        </div>

        <div>
          <label class="block text-sm font-medium text-amber-800 mb-1">Bio</label>
          <textarea 
            v-model="formData.bio"
            rows="3"
            class="w-full px-3 py-2 border border-amber-300 rounded-lg focus:ring-2 focus:ring-amber-500 focus:border-transparent resize-none"
            placeholder="Tell us about yourself..."
          ></textarea>
        </div>

        <div class="flex gap-3 pt-4">
          <button 
            type="submit"
            :disabled="isLoading"
            class="flex-1 bg-amber-500 text-white py-2 px-4 rounded-lg font-medium hover:bg-amber-600 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {{ isLoading ? 'Saving...' : 'Save Identity' }}
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script>
import { ref, watch } from 'vue'

export default {
  name: 'IdentityCard',
  props: {
    identity: {
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
      name: '',
      archetype: '',
      mood: '',
      region: '',
      field: '',
      self_title: '',
      bio: ''
    })

    // Watch for prop changes and update form
    watch(() => props.identity, (newIdentity) => {
      if (newIdentity) {
        formData.value = { ...formData.value, ...newIdentity }
      }
    }, { immediate: true, deep: true })

    const handleSubmit = async () => {
      isLoading.value = true
      try {
        await emit('update', formData.value)
      } catch (error) {
        console.error('Failed to update identity:', error)
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