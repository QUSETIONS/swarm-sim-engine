<template>
  <div class="process-view">
    <div class="stepper-wrapper glass-panel">
      <div class="steps-nav">
        <div class="step" :class="{ active: currentStep >= 1 }">
          <div class="circle">1</div><span class="label">Upload Data</span>
        </div>
        <div class="connector" :class="{ active: currentStep >= 2 }"></div>
        <div class="step" :class="{ active: currentStep >= 2 }">
          <div class="circle">2</div><span class="label">Knowledge Graph</span>
        </div>
        <div class="connector" :class="{ active: currentStep >= 3 }"></div>
        <div class="step" :class="{ active: currentStep >= 3 }">
          <div class="circle">3</div><span class="label">Agent Simulation</span>
        </div>
        <div class="connector" :class="{ active: currentStep >= 4 }"></div>
        <div class="step" :class="{ active: currentStep >= 4 }">
          <div class="circle">4</div><span class="label">Audit Report</span>
        </div>
      </div>
    </div>
    
    <div class="step-content glass-panel">
      <transition name="fade-slide" mode="out-in">
        <div :key="currentStep" class="step-wrapper">
          <StepUpload v-if="currentStep === 1" @next="onUploadDone" />
          <StepGraph v-if="currentStep === 2" :projectId="projectId" :ontology="ontology" @next="onGraphDone" />
          
          <div v-if="currentStep === 3" class="sim-wrapper">
            <StepSimulation :simulationId="simulationId" :projectId="projectId" :graphId="graphId" :entities="entities" @next="onSimulationDone" />
            <div style="margin-top: 20px; display: flex; gap: 20px;">
              <div style="flex: 2;">
                <div style="display:flex; justify-content:space-between; align-items:center;">
                  <h4 :class="{ 'telemetry-text': telemetryMode }">{{ telemetryMode ? 'Telemetry View (Hacker Mode)' : '小镇全景 (Town View)' }}</h4>
                  <label class="switch">
                    <input type="checkbox" v-model="telemetryMode">
                    <span class="slider round"></span>
                  </label>
                </div>
                <TownViewport :simulationId="simulationId" :telemetryMode="telemetryMode" @selectAgent="onSelectAgent" />
              </div>
              <div style="flex: 1;">
                <SocialFeed :simulationId="simulationId" :telemetryMode="telemetryMode" />
              </div>
            </div>
            
            <AgentInterviewModal 
              v-if="selectedAgent" 
              :agent="selectedAgent" 
              @close="selectedAgent = null" 
            />
          </div>

          <StepReport v-if="currentStep === 4" :simulationId="simulationId" />
        </div>
      </transition>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import StepUpload from '../components/StepUpload.vue'
import StepGraph from '../components/StepGraph.vue'
import StepSimulation from '../components/StepSimulation.vue'
import StepReport from '../components/StepReport.vue'
import TownViewport from '../components/TownViewport.vue'
import SocialFeed from '../components/SocialFeed.vue'
import AgentInterviewModal from '../components/AgentInterviewModal.vue'

const currentStep = ref(1)
const projectId = ref('')
const ontology = ref<any>(null)
const simulationId = ref('sim_demo_1')
const graphId = ref('')
const entities = ref<any[]>([])
const selectedAgent = ref<any | null>(null)
const telemetryMode = ref(false)

const onUploadDone = (data: any) => {
  projectId.value = data.projectId
  ontology.value = data.ontology
  currentStep.value = 2
}
const onGraphDone = (data: any) => {
  graphId.value = data.graphId
  // Mock entity extraction complete
  entities.value = [{ uuid: "1", name: "Alice", summary: "student" }, { uuid: "2", name: "Bob", summary: "teacher" }]
  currentStep.value = 3
}
const onSimulationDone = () => {
  currentStep.value = 4
}
const onSelectAgent = (agent: any) => {
  selectedAgent.value = agent
}
</script>

<style scoped>
.stepper-wrapper {
  margin-bottom: 2rem;
  padding: 1.5rem 2rem;
}

.steps-nav {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.step {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.5rem;
  color: var(--text-muted);
  transition: all 0.3s ease;
  flex: 1;
}

.step.active {
  color: var(--primary-color);
}

.circle {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  background: var(--bg-color);
  border: 2px solid var(--panel-border);
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
  transition: all 0.3s ease;
  font-family: var(--font-heading);
}

.step.active .circle {
  border-color: var(--primary-color);
  background: rgba(23, 224, 137, 0.1);
  box-shadow: 0 0 10px rgba(23, 224, 137, 0.4);
}

.label {
  font-size: 0.9rem;
  font-weight: 500;
  letter-spacing: 0.5px;
}

.connector {
  flex: 2;
  height: 2px;
  background: var(--panel-border);
  margin-bottom: 20px;
  position: relative;
  transition: all 0.5s ease;
}

.connector.active::after {
  content: '';
  position: absolute;
  top: 0; left: 0; bottom: 0;
  width: 100%;
  background: linear-gradient(90deg, var(--primary-color), var(--accent-cyan));
  box-shadow: 0 0 5px var(--primary-color);
}

.step-content {
  padding: 2.5rem;
  min-height: 400px;
  position: relative;
  transition: all 0.4s ease;
}

/* Toggle Switch Styles */
.switch {
  position: relative;
  display: inline-block;
  width: 50px;
  height: 24px;
}
.switch input { 
  opacity: 0;
  width: 0;
  height: 0;
}
.slider {
  position: absolute;
  cursor: pointer;
  top: 0; left: 0; right: 0; bottom: 0;
  background-color: #ccc;
  transition: .4s;
}
.slider:before {
  position: absolute;
  content: "";
  height: 16px;
  width: 16px;
  left: 4px;
  bottom: 4px;
  background-color: white;
  transition: .4s;
}
input:checked + .slider {
  background-color: #17e089;
}
input:checked + .slider:before {
  transform: translateX(26px);
}
.slider.round {
  border-radius: 34px;
}
.slider.round:before {
  border-radius: 50%;
}
.telemetry-text {
  color: #17e089;
  text-shadow: 0 0 5px #17e089;
}

/* Step Transitions */
.step-wrapper {
  width: 100%;
}

.fade-slide-enter-active,
.fade-slide-leave-active {
  transition: all 0.4s cubic-bezier(0.25, 0.8, 0.25, 1);
}

.fade-slide-enter-from {
  opacity: 0;
  transform: translateX(30px);
}

.fade-slide-leave-to {
  opacity: 0;
  transform: translateX(-30px);
}
</style>
