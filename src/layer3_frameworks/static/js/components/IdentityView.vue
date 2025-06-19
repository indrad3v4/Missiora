<template>
  <div class="identity-view">
    <div class="content-card">
      <h2>Define Your Identity</h2>
      <form @submit.prevent="saveIdentity" class="identity-form">
        <div class="form-group">
          <label>Your Name</label>
          <input v-model="identity.name" placeholder="Enter your name" class="form-input" />
        </div>
        
        <div class="form-group">
          <label>Archetype</label>
          <select v-model="identity.archetype" class="form-select">
            <option value="">Select your archetype</option>
            <option value="creator">Creator</option>
            <option value="builder">Builder</option>
            <option value="consultant">Consultant</option>
            <option value="teacher">Teacher</option>
            <option value="innovator">Innovator</option>
          </select>
        </div>
        
        <div class="form-group">
          <label>Current Mood</label>
          <textarea v-model="identity.mood" placeholder="How are you feeling about your journey?" class="form-textarea"></textarea>
        </div>
        
        <div class="form-group">
          <label>Region/Location</label>
          <input v-model="identity.region" placeholder="Where are you based?" class="form-input" />
        </div>
        
        <div class="form-group">
          <label>Field/Industry</label>
          <input v-model="identity.field" placeholder="What industry do you work in?" class="form-input" />
        </div>
        
        <div class="form-group">
          <label>Self-Title</label>
          <input v-model="identity.selfTitle" placeholder="How do you describe yourself?" class="form-input" />
        </div>
        
        <button type="submit" class="save-btn">Save Identity</button>
      </form>
    </div>
  </div>
</template>

<script setup>
import { reactive, onMounted } from 'vue'

const identity = reactive({
  name: '',
  archetype: '',
  mood: '',
  region: '',
  field: '',
  selfTitle: ''
})

const emit = defineEmits(['save', 'update-header'])

onMounted(async () => {
  try {
    const response = await fetch('/api/identity')
    if (response.ok) {
      const data = await response.json()
      Object.assign(identity, data)
    }
  } catch (error) {
    console.log('No existing identity data')
  }
})

async function saveIdentity() {
  try {
    const response = await fetch('/api/identity', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(identity)
    })
    
    if (response.ok) {
      emit('save', identity)
      emit('update-header', {
        name: identity.name,
        location: identity.region
      })
      alert('Identity saved successfully!')
    }
  } catch (error) {
    console.error('Failed to save identity:', error)
    alert('Failed to save identity')
  }
}
</script>

<style scoped>
.identity-view {
  padding: 2rem;
  max-width: 600px;
  margin: 0 auto;
}

.content-card {
  background: white;
  border-radius: 12px;
  padding: 2rem;
  box-shadow: 0 4px 20px rgba(0,0,0,0.1);
}

.identity-form {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.form-group label {
  font-weight: 600;
  color: #374151;
}

.form-input, .form-select, .form-textarea {
  padding: 0.75rem;
  border: 2px solid #e5e7eb;
  border-radius: 8px;
  font-size: 1rem;
  transition: border-color 0.2s;
}

.form-input:focus, .form-select:focus, .form-textarea:focus {
  outline: none;
  border-color: #22d3ee;
}

.form-textarea {
  min-height: 100px;
  resize: vertical;
}

.save-btn {
  background: linear-gradient(135deg, #4ade80 0%, #22d3ee 100%);
  color: white;
  padding: 1rem 2rem;
  border: none;
  border-radius: 8px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: transform 0.2s;
}

.save-btn:hover {
  transform: translateY(-2px);
}
</style>