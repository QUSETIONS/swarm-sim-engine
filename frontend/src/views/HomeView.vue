<template>
  <div class="home">
    <div class="hero-content glass-panel">
      <div class="badge">v2.0 Beta</div>
      <h2 class="title">Swarm-Sim <span class="highlight">Engine MVP</span></h2>
      <p class="subtitle">
        国内首个开源的代码漏洞挖掘多智能体系统内核。
        基于 Multi-Agent 架构，让漏洞挖掘触手可及。
      </p>
      
      <div class="features">
        <div class="feature-item">
          <i class="icon">🤖</i>
          <span>角色化 SOP</span>
        </div>
        <div class="feature-item">
          <i class="icon">🕸️</i>
          <span>GraphRAG</span>
        </div>
        <div class="feature-item">
          <i class="icon">⚡</i>
          <span>沙箱 PoC 执行</span>
        </div>
      </div>

      <router-link to="/process" class="cta-link">
        <button class="primary-btn glow-btn">
          Initialize Swarm <span class="arrow">→</span>
        </button>
      </router-link>
    </div>
  </div>
</template>

<style scoped>
.home {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 70vh;
  padding: 2rem;
}

.hero-content {
  text-align: center;
  padding: 4rem 3rem;
  max-width: 800px;
  width: 100%;
  position: relative;
  overflow: hidden;
  border-top: 1px solid rgba(23, 224, 137, 0.3);
}

.hero-content::before {
  content: "";
  position: absolute;
  top: -50%; left: -50%;
  width: 200%; height: 200%;
  background: radial-gradient(circle, rgba(23, 224, 137, 0.05) 0%, transparent 50%);
  animation: rotate 20s linear infinite;
  z-index: -1;
}

@keyframes rotate {
  100% { transform: rotate(360deg); }
}

.badge {
  display: inline-block;
  padding: 4px 12px;
  border-radius: 20px;
  background: rgba(23, 224, 137, 0.1);
  color: #17e089;
  font-size: 0.85rem;
  font-weight: 600;
  letter-spacing: 1px;
  margin-bottom: 1.5rem;
  border: 1px solid rgba(23, 224, 137, 0.2);
}

.title {
  font-size: 3.5rem;
  font-weight: 800;
  margin-bottom: 1rem;
  line-height: 1.2;
}

.highlight {
  color: var(--primary-color);
  text-shadow: 0 0 20px rgba(23, 224, 137, 0.3);
}

.subtitle {
  font-size: 1.1rem;
  color: var(--text-muted);
  max-width: 600px;
  margin: 0 auto 3rem;
  line-height: 1.6;
}

.features {
  display: flex;
  justify-content: center;
  gap: 2rem;
  margin-bottom: 3rem;
}

.feature-item {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.95rem;
  color: var(--text-main);
  background: rgba(255,255,255,0.03);
  padding: 8px 16px;
  border-radius: 8px;
  border: 1px solid rgba(255,255,255,0.05);
}

.cta-link {
  text-decoration: none;
}

.glow-btn {
  padding: 16px 40px;
  font-size: 1.1rem;
  letter-spacing: 2px;
  border-width: 2px;
  background: rgba(23, 224, 137, 0.1);
}

.glow-btn .arrow {
  display: inline-block;
  transition: transform 0.3s ease;
  margin-left: 8px;
}

.glow-btn:hover .arrow {
  transform: translateX(5px);
}
</style>
