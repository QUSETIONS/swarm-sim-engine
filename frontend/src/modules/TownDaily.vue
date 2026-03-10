<template>
  <div class="newspaper-container">
    <div class="paper">
      <div class="masthead">
        <h1>小镇日报 (Town Daily)</h1>
        <div class="edition">第 {{ edition }} 期 | {{ date }}</div>
      </div>
      
      <div class="main-story">
        <h2>头条：小镇的觉醒与纽带</h2>
        <div class="content">
          <p>在最近的一次社会推演中，我们观察到居民们展现出了前所未有的社交活力。特别是 {{ topAgent }}，在广场上的活跃程度引起了广泛关注。</p>
          <img src="https://via.placeholder.com/400x200?text=Agent+Town+Action" alt="Simulation Snapshot" />
        </div>
      </div>
      
      <div class="side-bar">
        <h3>热门动态</h3>
        <ul>
          <li v-for="(m, i) in topMoments" :key="i">
            <strong>{{ m.user }}:</strong> {{ m.text }}
          </li>
        </ul>
      </div>
      
      <div class="footer">
        "每一个像素都有它的故事。"
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'

const edition = ref(1)
const date = ref(new Date().toLocaleDateString())
const topAgent = ref("Alice")
const topMoments = ref([
  { user: "Alice", text: "今天在广场散步，感觉模拟的世界也充满了阳光呢。" },
  { user: "Bob", text: "刚结束了一场深度讨论，大家的观点都很有启发。" }
])
</script>

<style scoped>
.newspaper-container {
  padding: 40px;
  background: #fdfaf0;
  min-height: 80vh;
  display: flex;
  justify-content: center;
}
.paper {
  max-width: 800px;
  background: #fff;
  border: 1px solid #ddd;
  box-shadow: 5px 5px 15px rgba(0,0,0,0.1);
  padding: 40px;
  font-family: 'Georgia', serif;
  color: #333;
}
.masthead {
  border-bottom: 4px double #333;
  text-align: center;
  margin-bottom: 20px;
}
.masthead h1 {
  font-size: 48px;
  margin: 0;
  text-transform: uppercase;
}
.edition {
  font-size: 14px;
  padding: 5px 0;
}
.main-story h2 {
  font-size: 28px;
  text-decoration: underline;
}
.content {
  line-height: 1.6;
}
.side-bar {
  margin-top: 30px;
  border-top: 1px solid #333;
  padding-top: 10px;
}
.side-bar h3 {
  font-size: 18px;
}
.side-bar ul {
  list-style: none;
  padding: 0;
}
.side-bar li {
  margin-bottom: 10px;
  font-style: italic;
}
.footer {
  margin-top: 40px;
  border-top: 1px solid #eee;
  text-align: center;
  font-size: 12px;
  color: #888;
}
</style>
