import {drawCanvas} from "./utils";
import {Frame, SimilarityChecker} from "./mini-vinci";
import {RGBA} from "./mini-vinci/Color";

let currentFrame: Frame | null = null;

export function changeProblem(id: string): void {
    fetch(`/${id}.json`).then(response => {
        response.json().then(data => {
            const rightCanvas = document.getElementById("rightCanvas") as HTMLCanvasElement;
            currentFrame = SimilarityChecker.dataToFrame(data);
            drawCanvas(rightCanvas, currentFrame);
        })
    });
}

export function queryPixel(x: number, y: number): RGBA {
    if (currentFrame === null) {
        return { r: 0, g: 0, b: 0, a: 0 };
    }
    x = Math.max(0, Math.min(399, Math.floor(x)));
    y = Math.max(0, Math.min(399, Math.floor(y)));
    const item = currentFrame[y * 400 + x];
    return item ? item : { r: 0, g: 0, b: 0, a: 0 };
}

export function calcScore(instructionCost: number, renderedData: Frame): string {
    if (currentFrame === null) {
        return "";
    }
    const similarity = SimilarityChecker.imageDiff(currentFrame, renderedData);
    const text = `cost = ${instructionCost}\n` +
        `similarity = ${similarity}\n` +
        `total = ${instructionCost + similarity}`;
    (document.getElementById("leftCanvasText") as HTMLDivElement).innerText = text;
    return text;
}
