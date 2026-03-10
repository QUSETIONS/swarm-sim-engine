<template>
  <div class="social-feed" :class="{ 'cyber-feed': cyberMode }">
    <h3>{{ cyberMode ? 'Agent Activity Stream' : '小镇朋友圈 (Social Feed)' }}</h3>
    <div v-if="moments.length === 0" class="empty">等待动态中...</div>
    <transition-group name="feed-list" tag="div" class="feed-container">
      <div v-for="(moment, i) in moments" :key="moment.timestamp + moment.agent_name + i" class="moment-card">
        <div class="header">
          <span class="name">{{ moment.agent_name }}</span>
          <span class="emotion">{{ moment.emotion }}</span>
        </div>
        <div class="content">{{ moment.content }}</div>
        <div class="footer">{{ moment.timestamp }}</div>
      </div>
    </transition-group>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'
import { connectSimulationLogStream, closeSimulationLogStream } from '../api/simulation'

const props = defineProps<{ simulationId?: string, cyberMode?: boolean }>()
const moments = ref<any[]>([])
let wsListener: any = null

onMounted(() => {
  if (props.simulationId) {
    wsListener = (logEntry: any) => {
      // We only care about entries that have an action or content
      if (logEntry.content || logEntry.action) {
        const newMoment = {
          agent_name: logEntry.agent_id || "System",
          content: logEntry.content || `[Action: ${logEntry.action}]`,
          emotion: logEntry.emotion || "🤖",
          timestamp: new Date().toLocaleTimeString()
        }
        moments.value.unshift(newMoment)
        // Keep only the latest 10
        if (moments.value.length > 10) {
          moments.value.pop()
        }
      }
    }
    connectSimulationLogStream(props.simulationId, wsListener)
  }
})

onUnmounted(() => {
  if (wsListener) {
    closeSimulationLogStream(wsListener)
  }
})
</script>

<style scoped>
.social-feed {
  max-width: 500px;
  background: #f0f2f5;
  padding: 15px;
  border-radius: 8px;
}
.moment-card {
  background: white;
  margin-bottom: 15px;
  padding: 10px;
  border-radius: 4px;
}
.header { display: flex; justify-content: space-between; margin-bottom: 5px; }
.name { font-weight: bold; color: #1a73e8; }
.content { font-size: 14px; line-height: 1.4; color: #333; }
.footer { font-size: 11px; color: #999; margin-top: 5px; }

/* Cyber Theme Overrides */
.cyber-feed {
  background: #0d1117;
  border: 1px solid #17e089;
  color: #17e089;
  box-shadow: 0 0 10px rgba(23, 224, 137, 0.2);
}
.cyber-feed h3 { color: #17e089; }
.cyber-feed .empty { color: #17e089; }
.cyber-feed .moment-card {
  background: #161b22;
  border: 1px solid #30363d;
}
.cyber-feed .name { color: #17e089; font-family: monospace; }
.cyber-feed .content { color: #c9d1d9; font-family: monospace; }
.cyber-feed .footer { color: #666; font-family: monospace; }

/* Transition Group Animations */
.feed-container {
  position: relative;
}
.feed-list-enter-active,
.feed-list-leave-active {
  transition: all 0.5s cubic-bezier(0.4, 0, 0.2, 1);
}
.feed-list-enter-from {
  opacity: 0;
  transform: translateY(-20px) scale(0.95);
}
.feed-list-leave-to {
  opacity: 0;
  transform: translateX(30px);
}
.feed-list-move {
  transition: transform 0.5s ease;
}
</style>
