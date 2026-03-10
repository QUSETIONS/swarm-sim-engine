<template>
  <div ref="phaserContainer" class="phaser-container" :class="{ 'telemetry-filter': telemetryMode }"></div>
</template>

<script setup lang="ts">
import { onMounted, onUnmounted, ref, watch } from 'vue'
import Phaser from 'phaser'
import { generateTileset } from '../game/tileset-generator'
import { generateAgentSprite } from '../game/AgentSprite'
import { generateMapData } from '../game/town-map'
import { TownManager } from '../game/TownManager'
import { connectSimulationLogStream, closeSimulationLogStream } from '../api/simulation'

const emit = defineEmits(['selectAgent'])
const props = defineProps<{ simulationId?: string, telemetryMode?: boolean }>()
const phaserContainer = ref<HTMLElement | null>(null)
let game: Phaser.Game | null = null
let townManager: TownManager | null = null
let wsListener: any = null

onMounted(() => {
  const config: Phaser.Types.Core.GameConfig = {
    type: Phaser.AUTO,
    parent: phaserContainer.value!,
    width: 800,
    height: 600,
    pixelArt: true,
    scene: {
      preload,
      create
    }
  }

  game = new Phaser.Game(config)
})

onUnmounted(() => {
  if (game) game.destroy(true)
  if (wsListener) closeSimulationLogStream(wsListener)
})

function preload(this: Phaser.Scene) {
  generateTileset(this)
}

function create(this: Phaser.Scene) {
  const mapData = generateMapData()
  const map = this.make.tilemap({ data: mapData, tileWidth: 32, tileHeight: 32 })
  const tileset = map.addTilesetImage('tileset')
  if (!tileset) return
  map.createLayer(0, tileset, 0, 0)

  townManager = new TownManager(this)

  if (props.simulationId) {
    startPolling(this)
  }
}

async function startPolling(scene: Phaser.Scene) {
  // Initial agent creation if missing (Simplified for Audit Fix)
  if (Object.keys((townManager as any).agentSprites).length === 0) {
    const mockAgents = [
      { uuid: "1", name: "Alice", color: 0xff004d },
      { uuid: "2", name: "Bob", color: 0x29adff }
    ]
    mockAgents.forEach(a => {
      generateAgentSprite(scene, `agent_${a.uuid}`, a.color)
      const sprite = scene.add.sprite(0, 0, `agent_${a.uuid}`).setScale(2)
      sprite.setInteractive({ useHandCursor: true })
      sprite.on('pointerdown', () => emit('selectAgent', a))
      
      const label = scene.add.text(0, 25, a.name, { fontSize: '12px', color: '#fff' }).setOrigin(0.5)
      scene.add.container(400, 300, [sprite, label])
      
      townManager?.registerAgent(a.uuid, sprite)
    })
  }

  if (!props.simulationId || !townManager) return

  wsListener = (logEntry: any) => {
    // Process new log entries via TownManager
    townManager?.updateAgentFromLog(logEntry)
  }

  connectSimulationLogStream(props.simulationId, wsListener)
}
</script>

<style scoped>
.phaser-container {
  width: 800px;
  height: 600px;
  margin: 0 auto;
  border: 4px solid #333;
  border-radius: 8px;
}
.telemetry-filter {
  filter: invert(0.9) hue-rotate(180deg) brightness(1.2) contrast(1.5);
  border-color: #17e089;
  box-shadow: 0 0 15px rgba(23, 224, 137, 0.4);
}
</style>
