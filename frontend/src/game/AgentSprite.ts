import Phaser from 'phaser';
import { PICO8_COLORS } from './palette';

export const SPRITE_CONFIG = {
    frameWidth: 16,
    frameHeight: 24,
};

export function generateAgentSprite(scene: Phaser.Scene, key: string, color: number): void {
    const fw = SPRITE_CONFIG.frameWidth;
    const fh = SPRITE_CONFIG.frameHeight;
    const graphics = scene.make.graphics({ x: 0, y: 0 });

    // Draw 4 directions (simplified)
    for (let i = 0; i < 4; i++) {
        const x = i * fw;
        const y = 0;

        // Body
        graphics.fillStyle(color);
        graphics.fillRect(x + 4, y + 8, 8, 8);
        // Head
        graphics.fillStyle(PICO8_COLORS.peach);
        graphics.fillRect(x + 5, y + 2, 6, 6);
        // Eyes
        graphics.fillStyle(0x000000);
        graphics.fillRect(x + 6, y + 4, 1, 1);
        graphics.fillRect(x + 9, y + 4, 1, 1);
    }

    graphics.generateTexture(key, 4 * fw, fh);
    graphics.destroy();

    const texture = scene.textures.get(key);
    for (let i = 0; i < 4; i++) {
        texture.add(i, 0, i * fw, 0, fw, fh);
    }
}
