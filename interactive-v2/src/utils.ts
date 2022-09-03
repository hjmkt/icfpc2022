import { Block, Frame, Interpreter, Painter, VinciCanvas } from "./mini-vinci";
import { calcScore } from "./problems";

let currentCanvas: VinciCanvas | null = null;

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

export function runCode(islText: string): void {
    const interpreter = new Interpreter();
    const interpretedStructure = interpreter.run(islText);

    const painter = new Painter();
    currentCanvas = interpretedStructure.canvas;
    const renderedData = painter.draw(interpretedStructure.canvas);

    const canvas = document.getElementById("leftCanvas") as HTMLCanvasElement;
    drawCanvas(canvas, renderedData);

    calcScore(interpretedStructure.cost, renderedData);
}

export function getPointerBlocks(x: number, y: number): Block[] {
    if (currentCanvas == null) {
        return [];
    }

    let result: Block[] = [];
    currentCanvas.blocks.forEach((block) => {
        if (
            x >= block.bottomLeft.px &&
            x < block.topRight.px &&
            y >= block.bottomLeft.py &&
            y < block.topRight.py
        ) {
            result.push(block);
        }
    });
    return result;
}
