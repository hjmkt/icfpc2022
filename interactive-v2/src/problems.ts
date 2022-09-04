import { drawCanvas, runCode } from "./utils";
import { Frame, SimilarityChecker } from "./mini-vinci";
import { RGBA } from "./mini-vinci/Color";
import { BlockSpec, CanvasSpec } from "./mini-vinci/Canvas";

let currentFrame: Frame | null = null;
let currentSpec: CanvasSpec | null = null;

export async function changeProblem(id: string): Promise<void> {
    const response = await fetch(`/${id}.json`);
    const data = await response.json();
    const rightCanvas = document.getElementById(
        "rightCanvas"
    ) as HTMLCanvasElement;
    currentFrame = SimilarityChecker.dataToFrame(data);
    drawCanvas(rightCanvas, currentFrame);

    if (Number(id) <= 25) {
        currentSpec = {
            width: 400,
            height: 400,
            blocks: [
                {
                    blockId: "0",
                    bottomLeft: [0, 0],
                    topRight: [400, 400],
                    color: [255, 255, 255, 255],
                },
            ],
        };
        runCode("", true, false);
        return;
    }

    const response2 = await fetch(`/${id}.initial.json`);
    currentSpec = await response2.json();

    if (Number(id) >= 36 && currentSpec && currentSpec.sourcePngJSON) {
        const source = await fetch(`/${id}.source.json`);
        const sourceJson = await source.json();
        (currentSpec.blocks[0] as BlockSpec).source = sourceJson; // 36-40前提の決めうち
    }

    runCode("", true, Number(id) >= 36);
}

export function isV2ScoreMode(): boolean {
    const spec = getCurrentSpec();
    return !!spec.sourcePngJSON;
}

export function getCurrentSpec(): CanvasSpec {
    if (currentSpec) return currentSpec;
    return {
        width: 400,
        height: 400,
        blocks: [
            {
                blockId: "0",
                bottomLeft: [0, 0],
                topRight: [400, 400],
                color: [255, 255, 255, 255],
            },
        ],
    };
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

export function calcScore(
    instructionCost: number,
    renderedData: Frame
): string {
    if (currentFrame === null) {
        return "";
    }
    const similarity = SimilarityChecker.imageDiff(currentFrame, renderedData);
    let text =
        `cost = ${instructionCost}\n` +
        `similarity = ${similarity}\n` +
        `total = ${instructionCost + similarity}`;

    if (isV2ScoreMode()) {
        text += `\n(final v2 score mode)`;
    } else {
        text += `\n(base score mode)`;
    }

    (document.getElementById("costText") as HTMLDivElement).innerText = text;
    return text;
}
