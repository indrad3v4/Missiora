<template>
  <div class="roadmap-view">
    <div class="content-card">
      <h2>Your Roadmap</h2>
      <p class="subtitle">Let's follow your roadmap to the highest goal.</p>
      
      <div class="roadmap-container">
        <div class="milestone-track">
          <div 
            v-for="(milestone, index) in milestones" 
            :key="milestone.id"
            class="milestone-node"
            :class="{ 
              active: milestone.active, 
              completed: milestone.completed,
              upcoming: !milestone.active && !milestone.completed 
            }"
            @click="selectMilestone(milestone)"
          >
            <div class="milestone-icon">
              <i v-if="milestone.completed" class="fas fa-check"></i>
              <i v-else-if="milestone.active" class="fas fa-target"></i>
              <i v-else class="fas fa-circle"></i>
            </div>
            <div class="milestone-content">
              <h3>{{ milestone.title }}</h3>
              <p v-if="milestone.description">{{ milestone.description }}</p>
              <div v-if="milestone.suggestions" class="suggestions">
                <h4>Suggested Idea:</h4>
                <p>{{ milestone.suggestions.idea }}</p>
                <div class="suggestion-details">
                  <span>Cost: {{ milestone.suggestions.cost }}</span>
                  <span>ROI: {{ milestone.suggestions.roi }}</span>
                </div>
              </div>
            </div>
          </div>
        </div>
        
        <div class="milestone-actions" v-if="selectedMilestone">
          <button 
            v-if="selectedMilestone.active && !selectedMilestone.completed"
            @click="completeMilestone(selectedMilestone.id)"
            class="complete-btn"
          >
            Mark Complete
          </button>
          <button 
            v-if="!selectedMilestone.active && !selectedMilestone.completed && canActivate(selectedMilestone)"
            @click="activateMilestone(selectedMilestone.id)"
            class="activate-btn"
          >
            Start This Milestone
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'

const milestones = ref([])
const selectedMilestone = ref(null)

const emit = defineEmits(['milestone-change'])

onMounted(async () => {
  await loadMilestones()
})

async function loadMilestones() {
  try {
    const response = await fetch('/api/milestones')
    if (response.ok) {
      milestones.value = await response.json()
      // Add sample suggestions for demo
      milestones.value.forEach(m => {
        if (m.code === 'design_first_offer') {
          m.suggestions = {
            idea: 'Automate Courier Service',
            cost: '€80',
            roi: '€500 in 2 weeks'
          }
        }
      })
      
      // Auto-select first active or incomplete milestone
      const activeOrNext = milestones.value.find(m => m.active || (!m.completed && !m.active))
      if (activeOrNext) {
        selectedMilestone.value = activeOrNext
      }
    }
  } catch (error) {
    console.error('Failed to load milestones:', error)
  }
}

function selectMilestone(milestone) {
  selectedMilestone.value = milestone
}

function canActivate(milestone) {
  // Can activate if previous milestones are completed
  const currentIndex = milestones.value.findIndex(m => m.id === milestone.id)
  if (currentIndex === 0) return true
  
  const previousMilestone = milestones.value[currentIndex - 1]
  return previousMilestone && previousMilestone.completed
}

async function completeMilestone(milestoneId) {
  try {
    const response = await fetch(`/api/milestones/${milestoneId}/complete`, {
      method: 'POST'
    })
    
    if (response.ok) {
      await loadMilestones()
      emit('milestone-change')
    }
  } catch (error) {
    console.error('Failed to complete milestone:', error)
  }
}

async function activateMilestone(milestoneId) {
  try {
    const response = await fetch(`/api/milestones/${milestoneId}/activate`, {
      method: 'POST'
    })
    
    if (response.ok) {
      await loadMilestones()
      emit('milestone-change')
    }
  } catch (error) {
    console.error('Failed to activate milestone:', error)
  }
}
</script>

<style scoped>
.roadmap-view {
  padding: 2rem;
  max-width: 800px;
  margin: 0 auto;
}

.content-card {
  background: white;
  border-radius: 12px;
  padding: 2rem;
  box-shadow: 0 4px 20px rgba(0,0,0,0.1);
}

.subtitle {
  color: #6b7280;
  margin-bottom: 2rem;
}

.milestone-track {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  margin-bottom: 2rem;
}

.milestone-node {
  display: flex;
  align-items: flex-start;
  gap: 1rem;
  padding: 1rem;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s;
  border: 2px solid transparent;
}

.milestone-node:hover {
  background: #f9fafb;
}

.milestone-node.active {
  background: #dbeafe;
  border-color: #3b82f6;
}

.milestone-node.completed {
  background: #dcfce7;
  border-color: #22c55e;
}

.milestone-node.upcoming {
  background: #f3f4f6;
}

.milestone-icon {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.2rem;
  flex-shrink: 0;
}

.milestone-node.active .milestone-icon {
  background: #3b82f6;
  color: white;
}

.milestone-node.completed .milestone-icon {
  background: #22c55e;
  color: white;
}

.milestone-node.upcoming .milestone-icon {
  background: #9ca3af;
  color: white;
}

.milestone-content {
  flex: 1;
}

.milestone-content h3 {
  margin: 0 0 0.5rem 0;
  color: #111827;
}

.milestone-content p {
  margin: 0;
  color: #6b7280;
  font-size: 0.9rem;
}

.suggestions {
  margin-top: 1rem;
  padding: 1rem;
  background: #fef3c7;
  border-radius: 8px;
}

.suggestions h4 {
  margin: 0 0 0.5rem 0;
  color: #92400e;
  font-size: 0.9rem;
}

.suggestion-details {
  display: flex;
  gap: 1rem;
  margin-top: 0.5rem;
  font-size: 0.8rem;
  color: #92400e;
}

.milestone-actions {
  display: flex;
  gap: 1rem;
  justify-content: center;
}

.complete-btn, .activate-btn {
  padding: 0.75rem 1.5rem;
  border: none;
  border-radius: 8px;
  font-weight: 600;
  cursor: pointer;
  transition: transform 0.2s;
}

.complete-btn {
  background: #22c55e;
  color: white;
}

.activate-btn {
  background: #3b82f6;
  color: white;
}

.complete-btn:hover, .activate-btn:hover {
  transform: translateY(-2px);
}
</style>