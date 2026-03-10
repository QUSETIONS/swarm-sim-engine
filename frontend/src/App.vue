<template>
  <div class="app-container">
    <header>
      <h1>Swarm Simulation MVP</h1>
    </header>
    <main>
      <router-view />
    </main>
  </div>
</template>

<style>
:root {
  --bg-color: #0b0f19;
  --panel-bg: rgba(22, 27, 34, 0.6);
  --panel-border: rgba(255, 255, 255, 0.08);
  --primary-color: #17e089;
  --primary-hover: #12b870;
  --text-main: #e6edf3;
  --text-muted: #8b949e;
  --accent-cyan: #29adff;
  --font-body: 'Inter', system-ui, sans-serif;
  --font-heading: 'Space Grotesk', system-ui, sans-serif;
}

body {
  font-family: var(--font-body);
  margin: 0;
  padding: 0;
  background-color: var(--bg-color);
  color: var(--text-main);
  background-image: radial-gradient(circle at top right, rgba(23, 224, 137, 0.05) 0%, transparent 40%),
                    radial-gradient(circle at bottom left, rgba(41, 173, 255, 0.05) 0%, transparent 40%);
  background-attachment: fixed;
  min-height: 100vh;
}

.app-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

header {
  margin-bottom: 30px;
  padding-bottom: 15px;
  border-bottom: 1px solid var(--panel-border);
  display: flex;
  align-items: center;
}

h1, h2, h3, h4, h5 {
  font-family: var(--font-heading);
  margin: 0;
}

header h1 {
  background: linear-gradient(90deg, #17e089, #29adff);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  font-weight: 700;
  letter-spacing: -0.5px;
}

/* Global Utility Classes */
.glass-panel {
  background: var(--panel-bg);
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
  border: 1px solid var(--panel-border);
  border-radius: 12px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
}

.primary-btn {
  font-family: var(--font-heading);
  background: transparent;
  color: var(--primary-color);
  border: 2px solid var(--primary-color);
  padding: 10px 24px;
  border-radius: 6px;
  cursor: pointer;
  font-size: 16px;
  font-weight: 600;
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
  text-transform: uppercase;
  letter-spacing: 1px;
}

.primary-btn:hover {
  background: var(--primary-color);
  color: var(--bg-color);
  box-shadow: 0 0 15px rgba(23, 224, 137, 0.4);
  transform: translateY(-2px);
}
</style>

