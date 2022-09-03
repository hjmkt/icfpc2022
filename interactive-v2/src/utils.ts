import {Frame} from "./mini-vinci";

export function drawCanvas(canvas: HTMLCanvasElement, frame: Frame): void {
    const context = canvas.getContext("2d");
    if (context === null) return;

    const width = 400;
    const height = 400;

    const imageData = context.createImageData(width, height);
    let idx = 0;
    for (let y = 0; y < height; y++) {
        for (let x = 0; x < width; x++) {
            const rgba = frame[y * width + x];
            if (!rgba) continue;
            imageData.data[idx++] = rgba.r;
            imageData.data[idx++] = rgba.g;
            imageData.data[idx++] = rgba.b;
            imageData.data[idx++] = rgba.a;
        }
    }
    context.putImageData(imageData, 0, 0);
}