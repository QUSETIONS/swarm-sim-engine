<template>
  <div class="step-container">
    <h3 class="step-title">Step 4: Audit Report (Town Daily)</h3>
    <div class="form-group text-center" v-if="!report">
      <button @click="generate" :disabled="loading" class="primary-btn glow-btn btn-block">
        {{ loading ? 'Compiling Report...' : 'Generate Daily Executive Report' }}
      </button>
    </div>
    <div v-else>
      <TownDaily :reportData="report" />
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, defineProps } from 'vue'
import { generateReport } from '../api/report'
import TownDaily from './TownDaily.vue'

const props = defineProps<{ simulationId: string }>()
const loading = ref(false)
const report = ref<any>(null)
const message = ref('')
const reply = ref('')

const generate = async () => {
  loading.value = true
  try {
    const res = await generateReport(props.simulationId)
    report.value = res.data.data
  } catch (err) {
    alert('Error generating report')
  } finally {
    loading.value = false
  }
}

const askAgent = async () => {
  const res = await interviewAgent('1', message.value)
  reply.value = res.data.data.response
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

.text-center {
  text-align: center;
}

.btn-block {
  width: 100%;
  max-width: 400px;
  margin: 2rem auto;
  padding: 14px;
}
</style>
