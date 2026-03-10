export const W = 40, H = 30;

export function getGround(x: number, y: number): number {
    if (x === 0 || y === 0 || x === W - 1 || y === H - 1) return 7; // River/Border
    if (y === 15) return 4; // Road
    if (x === 20) return 4; // Road
    return 3; // Grass
}

export function generateMapData() {
    const data = [];
    for (let y = 0; y < H; y++) {
        const row = [];
        for (let x = 0; x < W; x++) {
            row.push(getGround(x, y));
        }
        data.push(row);
    }
    return data;
}

export const LANDMARKS = {
    Plaza: { x: 400, y: 300 },
    Cafe: { x: 100, y: 100 },
    Library: { x: 700, y: 100 },
    Park: { x: 400, y: 500 },
    Home: { x: 100, y: 500 }
};
