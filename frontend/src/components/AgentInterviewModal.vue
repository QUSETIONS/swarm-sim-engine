<template>
  <div v-if="agent" class="agent-interview-modal">
    <div class="modal-content">
      <div class="modal-header">
        <h3>采访: {{ agent.name }}</h3>
        <button @click="$emit('close')" class="close-btn">&times;</button>
      </div>
      <div class="chat-history" ref="chatHistory">
        <div v-for="(msg, i) in messages" :key="i" :class="['message', msg.role]">
          <span class="sender">{{ msg.role === 'user' ? '你' : agent.name }}:</span>
          <p>{{ msg.text }}</p>
        </div>
        <div v-if="loading" class="loading">正在思考...</div>
      </div>
      <div class="input-area">
        <input 
          v-model="input" 
          @keyup.enter="sendMessage" 
          placeholder="问点什么吧..." 
          :disabled="loading"
        />
        <button @click="sendMessage" :disabled="loading || !input.trim()">发送</button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, watch, nextTick } from 'vue'
import axios from 'axios'

const props = defineProps<{ agent: any | null }>()
const emit = defineEmits(['close'])

const input = ref('')
const messages = ref<{ role: 'user' | 'agent', text: string }[]>([])
const loading = ref(false)
const chatHistory = ref<HTMLElement | null>(null)

watch(() => props.agent, () => {
  messages.value = []
  if (props.agent) {
    messages.value.push({ role: 'agent', text: `你好，我是 ${props.agent.name}。有什么想聊聊的吗？` })
  }
})

const sendMessage = async () => {
  if (!input.value.trim() || loading.value) return
  
  const text = input.value
  messages.value.push({ role: 'user', text })
  input.value = ''
  loading.value = True
  
  await nextTick()
  scrollToBottom()

  try {
    const res = await axios.post('/api/simulation/interview', {
      agent_id: props.agent.uuid,
      question: text
    })
    messages.value.push({ role: 'agent', text: res.data.data.response })
  } catch (e) {
    messages.value.push({ role: 'agent', text: '抱歉，我现在有点忙，稍后再说吧。' })
  } finally {
    loading.value = false
    await nextTick()
    scrollToBottom()
  }
}

const scrollToBottom = () => {
  if (chatHistory.value) {
    chatHistory.value.scrollTop = chatHistory.value.scrollHeight
  }
}
</script>

<style scoped>
.agent-interview-modal {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  background: rgba(0,0,0,0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}
.modal-content {
  background: white;
  width: 400px;
  height: 500px;
  border-radius: 12px;
  display: flex;
  flex-direction: column;
  overflow: hidden;
  box-shadow: 0 10px 25px rgba(0,0,0,0.2);
}
.modal-header {
  padding: 15px;
  background: #f8f9fa;
  border-bottom: 1px solid #eee;
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.chat-history {
  flex: 1;
  padding: 15px;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
  gap: 10px;
}
.message {
  max-width: 80%;
  padding: 8px 12px;
  border-radius: 8px;
}
.message.user {
  align-self: flex-end;
  background: #007bff;
  color: white;
}
.message.agent {
  align-self: flex-start;
  background: #e9ecef;
  color: #333;
}
.sender {
  font-size: 10px;
  margin-bottom: 2px;
  display: block;
}
.input-area {
  padding: 15px;
  border-top: 1px solid #eee;
  display: flex;
  gap: 10px;
}
.input-area input {
  flex: 1;
  padding: 8px;
  border: 1px solid #ddd;
  border-radius: 4px;
}
.close-btn {
  background: none;
  border: none;
  font-size: 24px;
  cursor: pointer;
}
</style>
