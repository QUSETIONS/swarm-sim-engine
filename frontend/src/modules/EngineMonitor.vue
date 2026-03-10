<template>
  <div class="step-container">
    <h3 class="step-title">Step 3: Run Simulation Engine</h3>
    <div class="form-group text-center">
      <p class="glow-label">Ontology Entities Extracted: <span class="highlight">{{ entities.length }}</span></p>
    </div>
    <button v-if="!isRunning" @click="start" :disabled="loading" class="primary-btn glow-btn btn-block">
      {{ loading ? 'Booting Swarm Intelligence...' : 'Initialize Swarm Agents' }}
    </button>
    <button v-else @click="finish" class="primary-btn glow-btn btn-block" style="background: var(--accent-pink)">
      End Simulation &amp; Generate Report
    </button>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { startSimulation } from '../api/simulation'

const props = defineProps<{ simulationId: string, projectId: string, graphId: string, entities: any[] }>()
const emit = defineEmits(['next'])
const loading = ref(false)
const isRunning = ref(false)

const start = async () => {
  loading.value = true
  try {
    await startSimulation(props.simulationId)
    isRunning.value = true
    loading.value = false
  } catch (err) {
    alert('Error starting simulation')
    loading.value = false
  }
}

const finish = () => {
  emit('next')
}
</script>

<style scoped>
.step-container {
  max-width: 600px;
  margin: 0 auto;
}

.step-title {
  color: var(--primary-color);
  margin-bottom: 2rem;
  text-align: center;
  font-size: 1.8rem;
  letter-spacing: 1px;
}

.glow-label {
  color: var(--text-main);
  font-size: 1.2rem;
}

.highlight {
  color: var(--accent-cyan);
  font-weight: 700;
  text-shadow: 0 0 10px rgba(41, 173, 255, 0.4);
}

.text-center {
  text-align: center;
}

.btn-block {
  width: 100%;
  margin-top: 2rem;
  padding: 14px;
}
</style>
