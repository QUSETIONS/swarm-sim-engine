import Phaser from 'phaser'
import { LANDMARKS } from './town-map'

export class TownManager {
    private scene: Phaser.Scene
    private agentSprites: Record<string, Phaser.GameObjects.Sprite> = {}
    private thoughtBubbles: Record<string, { bg: Phaser.GameObjects.Rectangle, text: Phaser.GameObjects.Text }> = {}

    constructor(scene: Phaser.Scene) {
        this.scene = scene
    }

    public registerAgent(uuid: string, sprite: Phaser.GameObjects.Sprite) {
        this.agentSprites[uuid] = sprite
    }

    public getAgent(uuid: string) {
        return this.agentSprites[uuid]
    }

    public updateAgentFromLog(entry: any) {
        const id = entry.agent_id
        const sprite = this.agentSprites[id]
        if (!sprite) return

        // Thought Bubble Logic
        if (entry.thought && !this.thoughtBubbles[id]) {
            this.showThought(id, entry.thought)
        }

        // Movement Logic
        this.moveAgent(id, entry.metadata?.location)
    }

    private showThought(id: string, thought: string) {
        const sprite = this.agentSprites[id]
        const container = sprite.parentContainer
        if (!container) return

        const bg = this.scene.add.rectangle(0, -45, 160, 40, 0xffffff, 0.9).setOrigin(0.5).setStrokeStyle(1, 0x333333)
        const text = this.scene.add.text(0, -45, thought, {
            fontSize: '10px', color: '#000', fontFamily: 'Arial', wordWrap: { width: 140 }
        }).setOrigin(0.5)

        container.add([bg, text])
        this.thoughtBubbles[id] = { bg, text }

        this.scene.time.delayedCall(4000, () => {
            bg.destroy()
            text.destroy()
            delete this.thoughtBubbles[id]
        })
    }

    private moveAgent(id: string, locationKey?: string) {
        const sprite = this.agentSprites[id]
        const target = sprite.parentContainer || sprite

        let tx = sprite.x + (Math.random() - 0.5) * 40
        let ty = sprite.y + (Math.random() - 0.5) * 40

        if (locationKey && LANDMARKS[locationKey as keyof typeof LANDMARKS]) {
            const lm = LANDMARKS[locationKey as keyof typeof LANDMARKS]
            tx = lm.x + (Math.random() - 0.5) * 20
            ty = lm.y + (Math.random() - 0.5) * 20
        }

        this.scene.tweens.add({
            targets: target,
            x: Phaser.Math.Clamp(tx, 50, 750),
            y: Phaser.Math.Clamp(ty, 50, 550),
            duration: 1500
        })
    }
}
