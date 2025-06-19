import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export const useUserStore = defineStore('user', () => {
  // State
  const identity = ref({})
  const mission = ref({})
  const roadmap = ref({ milestones: [] })
  const isLoading = ref(false)
  const error = ref(null)

  // Computed
  const identityCompletion = computed(() => {
    const fields = [identity.value.name, identity.value.archetype, identity.value.mood, 
                   identity.value.region, identity.value.field, identity.value.self_title]
    const completed = fields.filter(field => field && field.trim()).length
    return Math.round((completed / fields.length) * 100)
  })

  const missionCompletion = computed(() => {
    const fields = [mission.value.statement, mission.value.goal, mission.value.blocks]
    const completed = fields.filter(field => field && field.trim()).length
    return Math.round((completed / fields.length) * 100)
  })

  const roadmapCompletion = computed(() => {
    const totalMilestones = roadmap.value.milestones?.length || 0
    if (totalMilestones === 0) return 0
    const completedMilestones = roadmap.value.milestones.filter(m => m.completed).length
    return Math.round((completedMilestones / totalMilestones) * 100)
  })

  const isProfileComplete = computed(() => {
    return identityCompletion.value >= 80 && missionCompletion.value >= 80
  })

  // Actions
  async function fetchUserData() {
    isLoading.value = true
    error.value = null
    
    try {
      const [identityRes, missionRes, roadmapRes] = await Promise.all([
        fetch('/api/identity'),
        fetch('/api/mission'),
        fetch('/api/roadmap')
      ])

      if (identityRes.ok) {
        identity.value = await identityRes.json()
      }
      if (missionRes.ok) {
        mission.value = await missionRes.json()
      }
      if (roadmapRes.ok) {
        const roadmapData = await roadmapRes.json()
        roadmap.value = {
          title: roadmapData.title,
          description: roadmapData.description,
          milestones: roadmapData.milestones || []
        }
      }
    } catch (err) {
      error.value = 'Failed to load user data'
      console.error('Error fetching user data:', err)
    } finally {
      isLoading.value = false
    }
  }

  async function updateIdentity(newIdentity) {
    isLoading.value = true
    try {
      const response = await fetch('/api/identity', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(newIdentity)
      })

      if (response.ok) {
        const updated = await response.json()
        identity.value = { ...identity.value, ...updated }
      } else {
        throw new Error('Failed to update identity')
      }
    } catch (err) {
      error.value = 'Failed to update identity'
      throw err
    } finally {
      isLoading.value = false
    }
  }

  async function updateMission(newMission) {
    isLoading.value = true
    try {
      const response = await fetch('/api/mission', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(newMission)
      })

      if (response.ok) {
        const updated = await response.json()
        mission.value = { ...mission.value, ...updated }
      } else {
        throw new Error('Failed to update mission')
      }
    } catch (err) {
      error.value = 'Failed to update mission'
      throw err
    } finally {
      isLoading.value = false
    }
  }

  async function updateRoadmap(newRoadmap) {
    isLoading.value = true
    try {
      const response = await fetch('/api/roadmap', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(newRoadmap)
      })

      if (response.ok) {
        const updated = await response.json()
        roadmap.value = { ...roadmap.value, ...updated }
      } else {
        throw new Error('Failed to update roadmap')
      }
    } catch (err) {
      error.value = 'Failed to update roadmap'
      throw err
    } finally {
      isLoading.value = false
    }
  }

  return {
    // State
    identity,
    mission,
    roadmap,
    isLoading,
    error,
    
    // Computed
    identityCompletion,
    missionCompletion,
    roadmapCompletion,
    isProfileComplete,
    
    // Actions
    fetchUserData,
    updateIdentity,
    updateMission,
    updateRoadmap
  }
})