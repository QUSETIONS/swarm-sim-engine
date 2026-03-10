import Phaser from 'phaser';
import { PICO8_COLORS } from './palette';

const TILE_SIZE = 32;

export function generateTileset(scene: Phaser.Scene): void {
    const graphics = scene.make.graphics({ x: 0, y: 0 });
    const tilesPerRow = 10;
    const rows = 8;
    const width = tilesPerRow * TILE_SIZE;
    const height = rows * TILE_SIZE;

    graphics.clear();

    const drawAt = (tileX: number, tileY: number, drawFn: () => void) => {
        graphics.save();
        graphics.translateCanvas(tileX * TILE_SIZE, tileY * TILE_SIZE);
        drawFn();
        graphics.restore();
    };

    // 0: Light floor
    drawAt(0, 0, () => {
        graphics.fillStyle(PICO8_COLORS.lightGray);
        graphics.fillRect(0, 0, TILE_SIZE, TILE_SIZE);
    });
    // 3: Grass
    drawAt(3, 0, () => {
        graphics.fillStyle(PICO8_COLORS.darkGreen);
        graphics.fillRect(0, 0, TILE_SIZE, TILE_SIZE);
        graphics.fillStyle(PICO8_COLORS.green);
        graphics.fillRect(4, 4, 2, 2);
    });
    // 4: Road
    drawAt(4, 0, () => {
        graphics.fillStyle(PICO8_COLORS.darkGray);
        graphics.fillRect(0, 0, TILE_SIZE, TILE_SIZE);
    });
    // 7: Water
    drawAt(7, 0, () => {
        graphics.fillStyle(PICO8_COLORS.blue);
        graphics.fillRect(0, 0, TILE_SIZE, TILE_SIZE);
    });

    graphics.generateTexture('tileset', width, height);
    graphics.destroy();
}
