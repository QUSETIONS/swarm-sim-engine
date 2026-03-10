<template>
  <div class="step-container">
    <h3 class="step-title">Step 1: Define Target & Assets</h3>
    <div class="form-group">
      <label class="glow-label">Audit Target Requirement:</label>
      <textarea v-model="requirement" class="cyber-input" rows="4"></textarea>
    </div>
    <div class="form-group">
      <label class="glow-label">Upload Target Blueprint (Doc/Code):</label>
      <div class="file-wrapper">
        <input type="file" @change="onFileChange" class="cyber-file" />
      </div>
    </div>
    <button @click="submit" :disabled="loading" class="primary-btn glow-btn btn-block">
      {{ loading ? 'Extracting Ontology...' : 'Upload & Generate Ontology' }}
    </button>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { generateOntology } from '../api/graph'

const emit = defineEmits(['next'])
const requirement = ref('Predict how discussion evolves')
const file = ref<File | null>(null)
const loading = ref(false)

const onFileChange = (e: any) => {
  file.value = e.target.files[0]
}

const submit = async () => {
  if (!file.value) return alert('Select a file')
  loading.value = true
  try {
    const res = await generateOntology([file.value], requirement.value)
    emit('next', {
      projectId: res.data.data.project_id,
      ontology: res.data.data.ontology
    })
  } catch (err) {
    alert('Error generating ontology')
  } finally {
    loading.value = false
  }
}
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

.form-group {
  margin-bottom: 1.5rem;
}

.glow-label {
  display: block;
  margin-bottom: 0.5rem;
  color: var(--text-main);
  font-weight: 500;
  font-size: 1rem;
}

.cyber-input {
  width: 100%;
  background: rgba(11, 15, 25, 0.7);
  border: 1px solid var(--panel-border);
  color: var(--primary-color);
  padding: 12px;
  border-radius: 6px;
  font-family: monospace;
  font-size: 1rem;
  transition: all 0.3s ease;
  resize: vertical;
}

.cyber-input:focus {
  outline: none;
  border-color: var(--primary-color);
  box-shadow: 0 0 10px rgba(23, 224, 137, 0.2);
}

.file-wrapper {
  background: rgba(255, 255, 255, 0.02);
  border: 1px dashed var(--panel-border);
  border-radius: 6px;
  padding: 1rem;
  text-align: center;
  transition: all 0.3s ease;
}

.file-wrapper:hover {
  border-color: var(--primary-color);
  background: rgba(23, 224, 137, 0.05);
}

.cyber-file {
  color: var(--text-muted);
}
.cyber-file::file-selector-button {
  background: transparent;
  border: 1px solid var(--primary-color);
  color: var(--primary-color);
  padding: 6px 16px;
  border-radius: 4px;
  cursor: pointer;
  margin-right: 15px;
  transition: all 0.3s ease;
}
.cyber-file::file-selector-button:hover {
  background: var(--primary-color);
  color: var(--bg-color);
}

.btn-block {
  width: 100%;
  margin-top: 1rem;
  padding: 14px;
}
</style>
