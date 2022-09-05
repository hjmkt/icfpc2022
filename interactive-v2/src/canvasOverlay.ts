import Konva from "konva";
import * as ace from "brace";
import { isV2ScoreMode, queryPixel } from "./problems";
import {
    getCurrentGlobalId,
    getPointerBlocks,
    queryLeftCanvasPixel,
    runCode,
} from "./utils";

const width = 812;
const height = 802;

let lineColor: (color: string) => void;
let curTool = "Inspect";
let targetBlock = "";
let targetX = 0;
let targetY = 0;
let targetX2 = -1;
let targetY2 = -1;
let prevR = 0;
let prevG = 0;
let prevB = 0;
let prevA = 0;
let currentGrid = 1;

export function setTool(toolName: string) {
    curTool = toolName;
    targetBlock = "";
    targetX2 = -1;
    targetY2 = -1;
    switch (toolName) {
        case "HLine Cut":
        case "VLine Cut":
        case "Point Cut":
        case "Color":
        case "Swap":
        case "Merge":
        case "CCM(左下)":
        case "CCM(右下)":
        case "CCM(右上)":
        case "CCM(左上)":
        case "矩形":
        case "CCCM(中央)":
            lineColor("red");
            break;
        default:
            lineColor("gray");
            toolName = "Inspect";
            break;
    }

    (document.getElementById("tool") as HTMLSelectElement).value = toolName;
}

function isContMode(): boolean {
    const check = document.getElementById("contCheck") as HTMLInputElement;
    return Boolean(check.checked);
}

export function setGrid(value: number) {
    currentGrid = value;
}

function applyGrid(pos: { x: number; y: number }): { x: number; y: number } {
    return {
        x: Math.floor(pos.x / currentGrid) * currentGrid,
        y: Math.floor((pos.y + 2) / currentGrid) * currentGrid - 2,
    };
}

export function setupOverlay(editor: ace.Editor) {
    const stage = new Konva.Stage({
        container: "canvas-overlay",
        width: width,
        height: height,
    });

    const inspectLayer = new Konva.Layer({
        x: 1,
        y: 1,
    });
    inspectLayer.hide();

    const leftLayer = new Konva.Layer({
        x: 1,
        y: 1,
    });

    const fadeOut = new Konva.Rect({
        x: 0,
        y: 0,
        width: 400,
        height: 400,
    });
    inspectLayer.add(fadeOut);

    const strokeWidth = 2;
    const targetBlock1 = new Konva.Rect({
        x: strokeWidth / 2,
        y: strokeWidth / 2,
        width: 400 - strokeWidth,
        height: 400 - strokeWidth,
        stroke: "white",
        strokeWidth: strokeWidth,
    });
    const targetBlock2 = new Konva.Rect({
        x: strokeWidth / 2,
        y: strokeWidth / 2,
        width: 400 - strokeWidth,
        height: 400 - strokeWidth,
        stroke: "red",
        strokeWidth: strokeWidth,
        dash: [10, 5],
    });
    inspectLayer.add(targetBlock1);
    inspectLayer.add(targetBlock2);

    function updateTargetBlock(
        x: number,
        y: number,
        width: number,
        height: number
    ) {
        targetBlock1.x(x + strokeWidth / 2);
        targetBlock1.y(400 - (y + strokeWidth / 2) - (height - strokeWidth));
        targetBlock1.width(width - strokeWidth);
        targetBlock1.height(height - strokeWidth);
        targetBlock2.x(targetBlock1.x());
        targetBlock2.y(targetBlock1.y());
        targetBlock2.width(targetBlock1.width());
        targetBlock2.height(targetBlock1.height());
    }

    const leftCanvas = new Konva.Rect({
        x: 0,
        y: 0,
        width: 400,
        height: 400,
        // fill: "red",
        // opacity: 0.5,
    });

    leftLayer.add(leftCanvas);

    const leftVLine1 = new Konva.Line({
        points: [200, 0, 200, 399],
        stroke: "white",
        strokeWidth: 1,
    });
    const leftVLine2 = new Konva.Line({
        points: [200, 0, 200, 399],
        stroke: "gray",
        strokeWidth: 1,
        dash: [5],
    });
    const leftHLine1 = new Konva.Line({
        points: [0, 200, 400, 200],
        stroke: "white",
        strokeWidth: 1,
    });
    const leftHLine2 = new Konva.Line({
        points: [0, 200, 400, 200],
        stroke: "gray",
        strokeWidth: 1,
        dash: [5],
    });
    leftLayer.add(leftVLine1);
    leftLayer.add(leftVLine2);
    leftLayer.add(leftHLine1);
    leftLayer.add(leftHLine2);

    const rightLayer = new Konva.Layer({
        x: 411,
        y: 1,
    });

    const rightCanvas = new Konva.Rect({
        x: 0,
        y: 0,
        width: 400,
        height: 400,
        // fill: "red",
        // opacity: 0.5,
    });

    rightLayer.add(rightCanvas);

    const rightVLine1 = new Konva.Line({
        points: [200, 0, 200, 399],
        stroke: "white",
        strokeWidth: 1,
    });
    const rightVLine2 = new Konva.Line({
        points: [200, 0, 200, 399],
        stroke: "gray",
        strokeWidth: 1,
        dash: [5],
    });
    const rightHLine1 = new Konva.Line({
        points: [0, 200, 400, 200],
        stroke: "white",
        strokeWidth: 1,
    });
    const rightHLine2 = new Konva.Line({
        points: [0, 200, 400, 200],
        stroke: "gray",
        strokeWidth: 1,
        dash: [5],
    });
    rightLayer.add(rightVLine1);
    rightLayer.add(rightVLine2);
    rightLayer.add(rightHLine1);
    rightLayer.add(rightHLine2);

    function updateLines(pos: { x: number; y: number }) {
        const x = Math.max(0, Math.min(399, Math.floor(pos.x)));
        const y = Math.max(0, Math.min(399, Math.floor(pos.y) + 1));
        const vPoints = [x, 0, x, 400];
        rightVLine1.points(vPoints);
        rightVLine2.points(vPoints);
        leftVLine1.points(vPoints);
        leftVLine2.points(vPoints);
        const hPoints = [0, y, 400, y];
        rightHLine1.points(hPoints);
        rightHLine2.points(hPoints);
        leftHLine1.points(hPoints);
        leftHLine2.points(hPoints);

        const { r, g, b, a } = queryPixel(x, y);
        const text = `point = [${x}, ${
            400 - y - 1
        }], color = [${r}, ${g}, ${b}, ${a}]`;
        (
            document.getElementById("rightCanvasText") as HTMLDivElement
        ).innerText = text;
    }

    lineColor = (color: string) => {
        rightHLine2.stroke(color);
        leftHLine2.stroke(color);
        rightVLine2.stroke(color);
        leftVLine2.stroke(color);
    };

    function lineVisible(visible: boolean) {
        if (visible) {
            rightVLine1.show();
            rightVLine2.show();
            leftVLine1.show();
            leftVLine2.show();
            rightHLine1.show();
            rightHLine2.show();
            leftHLine1.show();
            leftHLine2.show();
        } else {
            rightVLine1.hide();
            rightVLine2.hide();
            leftVLine1.hide();
            leftVLine2.hide();
            rightHLine1.hide();
            rightHLine2.hide();
            leftHLine1.hide();
            leftHLine2.hide();
        }
    }

    function queryPointerBlocks(pos: { x: number; y: number }) {
        const x = Math.max(0, Math.min(399, Math.floor(pos.x)));
        const y = 399 - Math.max(0, Math.min(399, Math.floor(pos.y) + 1));

        let { r, g, b, a } = queryLeftCanvasPixel(x, 399 - y);
        let right = queryPixel(x, 399 - y);
        let rDiff = (r - right.r) * (r - right.r);
        let gDiff = (g - right.g) * (g - right.g);
        let bDiff = (b - right.b) * (b - right.b);
        // let aDiff = (a - right.a) * (a - right.a);
        let diff = Math.sqrt(rDiff + gDiff + bDiff) / Math.sqrt(255 * 255 * 3);
        diff = Math.round(10000 - diff * 100 * 100) / 100;

        const blocks = getPointerBlocks(x, y);
        const first = blocks[0];
        if (first) {
            let text =
                `${first.typ === 0 ? "SimpleBlock" : "ComplexBlock"}(id = ${
                    first.id
                })\n` +
                `bottomLeft = [${first.bottomLeft.px}, ${first.bottomLeft.py}]\n` +
                `topRight = [${first.topRight.px}, ${first.topRight.py}]\n` +
                `size = [${first.size.px}, ${first.size.py}]\n` +
                `color = [${r}, ${g}, ${b}, ${a}] (similarity ${diff}%)`;

            updateTargetBlock(
                first.bottomLeft.px,
                first.bottomLeft.py,
                first.size.px,
                first.size.py
            );
            inspectLayer.show();
            (
                document.getElementById("leftCanvasText") as HTMLDivElement
            ).innerText = text;
        }
    }

    rightCanvas.on("pointermove", () => {
        const pos = applyGrid(rightCanvas.getRelativePointerPosition());
        updateLines(pos);
    });

    leftCanvas.on("pointermove", () => {
        const pos = applyGrid(leftCanvas.getRelativePointerPosition());
        updateLines(pos);

        queryPointerBlocks(pos);
    });

    leftCanvas.on("pointerleave", () => {
        inspectLayer.hide();
        lineVisible(false);
    });
    leftCanvas.on("pointerenter", () => {
        lineVisible(true);
    });
    rightCanvas.on("pointerleave", () => {
        lineVisible(false);
    });
    rightCanvas.on("pointerenter", () => {
        lineVisible(true);
    });

    rightCanvas.on("pointerdown", () => {
        const pos = applyGrid(rightCanvas.getRelativePointerPosition());
        const x = Math.max(0, Math.min(399, Math.floor(pos.x)));
        const y = Math.max(0, Math.min(399, Math.floor(pos.y) + 1));
        const { r, g, b, a } = queryPixel(x, y);
        console.log(`[${x}, ${y}]`);
        console.log(`[${r}, ${g}, ${b}, ${a}]`);

        const ccmCommon = (part: number) => {
            const { r, g, b, a } = queryPixel(x, y);
            const id = getCurrentGlobalId();

            let move =
                `cut[${targetBlock}][${targetX},${targetY}]\n` +
                `color[${targetBlock}.${part}][${r},${g},${b},${a}]\n` +
                `merge[${targetBlock}.0][${targetBlock}.3]\n` +
                `merge[${targetBlock}.1][${targetBlock}.2]\n` +
                `merge[${id + 1}][${id + 2}]\n`;

            editor.setValue(editor.getValue() + move);
            if (!isContMode()) {
                setTool("Inspect");
            } else {
                targetBlock = "";
            }
            runCode(editor.getValue(), true, isV2ScoreMode());
        };

        switch (curTool) {
            case "Color":
                if (targetBlock !== "") {
                    const { r, g, b, a } = queryPixel(x, y);
                    const move = `color[${targetBlock}][${r},${g},${b},${a}]\n`;
                    editor.setValue(editor.getValue() + move);
                    if (!isContMode()) {
                        setTool("Inspect");
                    } else {
                        targetBlock = "";
                    }
                    runCode(editor.getValue(), true, isV2ScoreMode());
                }
                break;
            case "矩形":
                if (targetBlock !== "" && targetY2 >= 0 && targetX2 >= 0) {
                    const { r, g, b, a } = queryPixel(x, y);
                    const id = getCurrentGlobalId();

                    let move = `cut[${targetBlock}][${targetX},${targetY}]\n`;

                    if (targetX < targetX2 && targetY >= targetY2) {
                        // 右下
                        move +=
                            `color[${targetBlock}.1][${r},${g},${b},${a}]\n` +
                            `cut[${targetBlock}.1][${targetX2},${targetY2}]\n` +
                            `color[${targetBlock}.1.0][${prevR},${prevG},${prevB},${prevA}]\n` +
                            `color[${targetBlock}.1.1][${prevR},${prevG},${prevB},${prevA}]\n` +
                            `color[${targetBlock}.1.2][${prevR},${prevG},${prevB},${prevA}]\n` +
                            `merge[${targetBlock}.1.0][${targetBlock}.1.3]\n` +
                            `merge[${targetBlock}.1.1][${targetBlock}.1.2]\n` +
                            `merge[${id + 1}][${id + 2}]\n` +
                            `merge[${targetBlock}.0][${targetBlock}.3]\n` +
                            `merge[${id + 3}][${targetBlock}.2]\n` +
                            `merge[${id + 4}][${id + 5}]\n`;
                    } else if (targetX >= targetX2 && targetY >= targetY2) {
                        // 左下
                        move +=
                            `color[${targetBlock}.0][${r},${g},${b},${a}]\n` +
                            `cut[${targetBlock}.0][${targetX2},${targetY2}]\n` +
                            `color[${targetBlock}.0.0][${prevR},${prevG},${prevB},${prevA}]\n` +
                            `color[${targetBlock}.0.1][${prevR},${prevG},${prevB},${prevA}]\n` +
                            `color[${targetBlock}.0.3][${prevR},${prevG},${prevB},${prevA}]\n` +
                            `merge[${targetBlock}.0.0][${targetBlock}.0.3]\n` +
                            `merge[${targetBlock}.0.1][${targetBlock}.0.2]\n` +
                            `merge[${id + 1}][${id + 2}]\n` +
                            `merge[${targetBlock}.1][${targetBlock}.2]\n` +
                            `merge[${id + 3}][${targetBlock}.3]\n` +
                            `merge[${id + 4}][${id + 5}]\n`;
                    } else if (targetX < targetX2 && targetY < targetY2) {
                        // 右上
                        move +=
                            `color[${targetBlock}.2][${r},${g},${b},${a}]\n` +
                            `cut[${targetBlock}.2][${targetX2},${targetY2}]\n` +
                            `color[${targetBlock}.2.2][${prevR},${prevG},${prevB},${prevA}]\n` +
                            `color[${targetBlock}.2.1][${prevR},${prevG},${prevB},${prevA}]\n` +
                            `color[${targetBlock}.2.3][${prevR},${prevG},${prevB},${prevA}]\n` +
                            `merge[${targetBlock}.2.0][${targetBlock}.2.3]\n` +
                            `merge[${targetBlock}.2.1][${targetBlock}.2.2]\n` +
                            `merge[${id + 1}][${id + 2}]\n` +
                            `merge[${targetBlock}.0][${targetBlock}.3]\n` +
                            `merge[${id + 3}][${targetBlock}.1]\n` +
                            `merge[${id + 4}][${id + 5}]\n`;
                    } else if (targetX >= targetX2 && targetY < targetY2) {
                        // 左上
                        move +=
                            `color[${targetBlock}.3][${r},${g},${b},${a}]\n` +
                            `cut[${targetBlock}.3][${targetX2},${targetY2}]\n` +
                            `color[${targetBlock}.3.0][${prevR},${prevG},${prevB},${prevA}]\n` +
                            `color[${targetBlock}.3.2][${prevR},${prevG},${prevB},${prevA}]\n` +
                            `color[${targetBlock}.3.3][${prevR},${prevG},${prevB},${prevA}]\n` +
                            `merge[${targetBlock}.3.0][${targetBlock}.3.3]\n` +
                            `merge[${targetBlock}.3.1][${targetBlock}.3.2]\n` +
                            `merge[${id + 1}][${id + 2}]\n` +
                            `merge[${targetBlock}.1][${targetBlock}.2]\n` +
                            `merge[${id + 3}][${targetBlock}.0]\n` +
                            `merge[${id + 4}][${id + 5}]\n`;
                    }

                    editor.setValue(editor.getValue() + move);
                    if (!isContMode()) {
                        setTool("Inspect");
                    } else {
                        targetBlock = "";
                        targetX2 = -1;
                        targetY2 = -1;
                    }
                    runCode(editor.getValue(), true, isV2ScoreMode());
                }
                break;
            case "CCM(左下)":
                if (targetBlock !== "") {
                    ccmCommon(0);
                }
                break;
            case "CCM(右下)":
                if (targetBlock !== "") {
                    ccmCommon(1);
                }
                break;
            case "CCM(右上)":
                if (targetBlock !== "") {
                    ccmCommon(2);
                }
                break;
            case "CCM(左上)":
                if (targetBlock !== "") {
                    ccmCommon(3);
                }
                break;
            case "CCCM(中央)":
                if (targetBlock !== "" && targetY2 >= 0 && targetX2 >= 0) {
                    const { r, g, b, a } = queryPixel(x, y);
                    const id = getCurrentGlobalId();
                    let move =
                        `cut[${targetBlock}][${targetX},${targetY}]\n` +
                        `cut[${targetBlock}.1][${targetX2},${targetY2}]\n` +
                        `color[${targetBlock}.1.3][${r},${g},${b},${a}]\n` +
                        `merge[${targetBlock}.1.0][${targetBlock}.1.3]\n` +
                        `merge[${targetBlock}.1.1][${targetBlock}.1.2]\n` +
                        `merge[${id + 1}][${id + 2}]\n` +
                        `merge[${targetBlock}.0][${targetBlock}.3]\n` +
                        `merge[${id + 3}][${targetBlock}.2]\n` +
                        `merge[${id + 4}][${id + 5}]\n`;

                    editor.setValue(editor.getValue() + move);
                    if (!isContMode()) {
                        setTool("Inspect");
                    } else {
                        targetBlock = "";
                        targetX2 = -1;
                        targetY2 = -1;
                    }
                    runCode(editor.getValue(), true, isV2ScoreMode());
                }
                break;
        }
    });

    leftCanvas.on("pointerdown", () => {
        const pos = applyGrid(leftCanvas.getRelativePointerPosition());
        const x = Math.max(0, Math.min(399, Math.floor(pos.x)));
        const y = 399 - Math.max(0, Math.min(399, Math.floor(pos.y) + 1));
        const blocks = getPointerBlocks(x, y);
        const first = blocks[0];
        if (first == null) {
            return;
        }

        switch (curTool) {
            case "HLine Cut": {
                const move = `cut[${first.id}][y][${y}]\n`;
                editor.setValue(editor.getValue() + move);
                if (!isContMode()) setTool("Inspect");
                runCode(editor.getValue(), true, isV2ScoreMode());
                break;
            }
            case "VLine Cut": {
                const move = `cut[${first.id}][x][${x}]\n`;
                editor.setValue(editor.getValue() + move);
                if (!isContMode()) setTool("Inspect");
                runCode(editor.getValue(), true, isV2ScoreMode());
                break;
            }
            case "Point Cut": {
                const move = `cut[${first.id}][${x},${y}]\n`;
                editor.setValue(editor.getValue() + move);
                if (!isContMode()) setTool("Inspect");
                runCode(editor.getValue(), true, isV2ScoreMode());
                break;
            }
            case "Color": {
                if (targetBlock === "") {
                    targetBlock = first.id;
                }
                break;
            }
            case "Swap": {
                if (targetBlock === "") {
                    targetBlock = first.id;
                } else {
                    const move = `swap[${targetBlock}][${first.id}]\n`;
                    editor.setValue(editor.getValue() + move);
                    if (!isContMode()) {
                        setTool("Inspect");
                    } else {
                        targetBlock = "";
                    }
                    runCode(editor.getValue(), true, isV2ScoreMode());
                }
                break;
            }
            case "Merge": {
                if (targetBlock === "") {
                    targetBlock = first.id;
                } else {
                    const move = `merge[${targetBlock}][${first.id}]\n`;
                    editor.setValue(editor.getValue() + move);
                    if (!isContMode()) {
                        setTool("Inspect");
                    } else {
                        targetBlock = "";
                    }
                    runCode(editor.getValue(), true, isV2ScoreMode());
                }
                break;
            }
            case "CCM(左下)":
            case "CCM(右下)":
            case "CCM(右上)":
            case "CCM(左上)": {
                if (targetBlock === "") {
                    targetBlock = first.id;
                    targetX = x;
                    targetY = y;
                }
                break;
            }
            case "矩形":
            case "CCCM(中央)":
                if (targetBlock === "") {
                    targetBlock = first.id;
                    targetX = x;
                    targetY = y;
                } else if (targetX2 < 0 && targetY2 < 0) {
                    targetX2 = x;
                    targetY2 = y;
                    let { r, g, b, a } = queryLeftCanvasPixel(x, 399 - y); // 場所によってyの意味が違うので補正(後で整理)
                    prevR = r;
                    prevG = g;
                    prevB = b;
                    prevA = a;
                }
                break;
            default:
                console.log(first.id);
                return;
        }
    });

    stage.add(inspectLayer);
    stage.add(leftLayer);
    stage.add(rightLayer);
}
