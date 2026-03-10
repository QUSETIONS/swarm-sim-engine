<template>
  <div class="step-container">
    <h3 class="step-title">Step 2: Initialize Knowledge Graph</h3>
    <div class="form-group">
      <h4 class="glow-label">Extracted Ontology Entities:</h4>
      <pre class="code-pre">{{ ontology }}</pre>
    </div>
    <button @click="build" :disabled="loading" class="primary-btn glow-btn btn-block">
      {{ loading ? 'Constructing Edges...' : 'Confirm & Build Semantic Graph' }}
    </button>
  </div>
</template>

<script setup lang="ts">
import { ref, defineProps, defineEmits } from 'vue'
import { buildGraph } from '../api/graph'

const props = defineProps<{ projectId: string, ontology: any }>()
const emit = defineEmits(['next'])
const loading = ref(false)

const build = async () => {
  loading.value = true
  try {
    const res = await buildGraph(props.projectId)
    // mock wait for async task
    setTimeout(() => {
      emit('next', { graphId: 'mock_graph_id' })
    }, 1000)
  } catch (err) {
    alert('Error building graph')
    loading.value = false
  }
}
</script>

<style scoped>
.step-container {
  max-width: 800px;
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
  color: var(--accent-cyan);
  margin-bottom: 1rem;
  font-size: 1.1rem;
}

.code-pre {
  background: #0d1117;
  color: var(--primary-color);
  border: 1px solid var(--panel-border);
  padding: 1.5rem;
  border-radius: 8px;
  font-family: 'Fira Code', monospace;
  overflow-x: auto;
  min-height: 200px;
  max-height: 400px;
  box-shadow: inset 0 0 15px rgba(0,0,0,0.5);
  transition: all 0.3s;
}

.code-pre:hover {
  border-color: var(--accent-cyan);
}

.btn-block {
  width: 100%;
  margin-top: 2rem;
  padding: 14px;
}
</style>
