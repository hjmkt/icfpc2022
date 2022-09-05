import { Block, Frame, Interpreter, Painter, VinciCanvas } from "./mini-vinci";
import { calcScore, getCurrentSpec } from "./problems";
import { RGBA } from "./mini-vinci/Color";

let currentCanvas: VinciCanvas | null = null;
let currentFrame: Frame | null = null;
let currentGlobalId = 0;

export function getCurrentGlobalId(): number {
    return currentGlobalId;
}

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

export function runCode(
    islText: string,
    resetRange: boolean,
    isV2CostMode: boolean
): void {
    const interpreter = new Interpreter(isV2CostMode);
    const interpretedStructure = interpreter.run(islText, getCurrentSpec());
    currentGlobalId = interpreter.topLevelIdCounter;

    const painter = new Painter();
    currentCanvas = interpretedStructure.canvas;
    const renderedData = painter.draw(interpretedStructure.canvas);
    currentFrame = renderedData;

    const canvas = document.getElementById("leftCanvas") as HTMLCanvasElement;
    drawCanvas(canvas, renderedData);

    const overlayCanvas = document.getElementById(
        "rightCanvasOverlay"
    ) as HTMLCanvasElement;
    drawCanvas(overlayCanvas, renderedData);

    calcScore(interpretedStructure.cost, renderedData);

    if (resetRange) {
        const lines = calcLines(islText);
        const range = document.getElementById("range") as HTMLInputElement;
        range.min = String(0);
        range.max = String(lines);
        range.value = range.max;
        (document.getElementById("timestamp") as HTMLDivElement).innerText =
            range.max;
    }
}

export function calcLines(text: string): number {
    const result = text.match(/\n/g);
    return result === null ? 1 : result.length + 1;
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

export function untilLine(text: string, line: number): string {
    let result = "";
    const lines = text.split(/\n/);

    for (let i = 1; i <= Math.min(line, lines.length); i++) {
        const line = lines[i - 1] as string;
        result = result + line + "\n";
    }

    return result;
}

export function queryLeftCanvasPixel(x: number, y: number): RGBA {
    if (currentFrame === null) {
        return { r: 0, g: 0, b: 0, a: 0 };
    }
    x = Math.max(0, Math.min(399, Math.floor(x)));
    y = Math.max(0, Math.min(399, Math.floor(y)));
    const item = currentFrame[y * 400 + x];
    return item ? item : { r: 0, g: 0, b: 0, a: 0 };
}
