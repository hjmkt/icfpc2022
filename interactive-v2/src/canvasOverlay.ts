import Konva from "konva";
import * as ace from "brace";
import { queryPixel } from "./problems";
import { getPointerBlocks, runCode } from "./utils";
import { ComplexBlock, SimpleBlock } from "./mini-vinci/Block";

const width = 812;
const height = 802;

let lineColor: (color: string) => void;
let curTool = "Inspect";
let targetBlock = "";

export function setTool(toolName: string) {
    curTool = toolName;
    targetBlock = "";
    switch (toolName) {
        case "HLine Cut":
        case "VLine Cut":
        case "Point Cut":
        case "Color":
        case "Swap":
        case "Merge":
        case "Cont Swap":
            lineColor("red");
            break;
        default:
            lineColor("gray");
            toolName = "Inspect";
            break;
    }

    (document.getElementById("tool") as HTMLSelectElement).value = toolName;
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
        const x = Math.max(0, Math.min(399, Math.floor(pos.x) ));
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
        const text = `point = [${x}, ${400 - y - 1}], color = [${r}, ${g}, ${b}, ${a}]`;
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

        const blocks = getPointerBlocks(x, y);
        const first = blocks[0];
        if (first) {
            let text =
                `${first.typ === 0 ? "SimpleBlock" : "ComplexBlock"}(id = ${
                    first.id
                })\n` +
                `bottomLeft = [${first.bottomLeft.px}, ${first.bottomLeft.py}]\n` +
                `topRight = [${first.topRight.px}, ${first.topRight.py}]\n` +
                `size = [${first.size.px}, ${first.size.py}]`;

            if (first.typ === 0) {
                const block = first as SimpleBlock;
                // simple
                updateTargetBlock(
                    block.bottomLeft.px,
                    block.bottomLeft.py,
                    block.size.px,
                    block.size.py
                );
            } else {
                // complex
                const block = first as ComplexBlock;
                updateTargetBlock(
                    block.bottomLeft.px,
                    block.bottomLeft.py,
                    block.size.px,
                    block.size.py
                );
            }
            inspectLayer.show();
            (
                document.getElementById("leftCanvasText") as HTMLDivElement
            ).innerText = text;
        }
    }

    rightCanvas.on("pointermove", () => {
        const pos = rightCanvas.getRelativePointerPosition();
        updateLines(pos);
    });

    leftCanvas.on("pointermove", () => {
        const pos = leftCanvas.getRelativePointerPosition();
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
        const pos = rightCanvas.getRelativePointerPosition();
        const x = Math.max(0, Math.min(399, Math.floor(pos.x)));
        const y = Math.max(0, Math.min(399, Math.floor(pos.y) + 1));
        const { r, g, b, a } = queryPixel(x, y);
        console.log(`[${x}, ${y}]`);
        console.log(`[${r}, ${g}, ${b}, ${a}]`);

        switch (curTool) {
            case "Color":
                if (targetBlock !== "") {
                    const { r, g, b, a } = queryPixel(x, y);
                    const move = `color[${targetBlock}][${r},${g},${b},${a}]\n`;
                    editor.setValue(editor.getValue() + move);
                    setTool("Inspect");
                    runCode(editor.getValue());
                }
                break;
        }
    });

    leftCanvas.on("pointerdown", () => {
        const pos = leftCanvas.getRelativePointerPosition();
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
                setTool("Inspect");
                runCode(editor.getValue());
                break;
            }
            case "VLine Cut": {
                const move = `cut[${first.id}][x][${x}]\n`;
                editor.setValue(editor.getValue() + move);
                setTool("Inspect");
                runCode(editor.getValue());
                break;
            }
            case "Point Cut": {
                const move = `cut[${first.id}][${x},${y}]\n`;
                editor.setValue(editor.getValue() + move);
                setTool("Inspect");
                runCode(editor.getValue());
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
                    setTool("Inspect");
                    runCode(editor.getValue());
                }
                break;
            }
            case "Cont Swap":
            {
                if (targetBlock === "") {
                    targetBlock = first.id;
                } else {
                    const move = `swap[${targetBlock}][${first.id}]\n`;
                    editor.setValue(editor.getValue() + move);
                    runCode(editor.getValue());
                    targetBlock = "";
                }
                break;
            }
            case "Merge": {
                if (targetBlock === "") {
                    targetBlock = first.id;
                } else {
                    const move = `merge[${targetBlock}][${first.id}]\n`;
                    editor.setValue(editor.getValue() + move);
                    setTool("Inspect");
                    runCode(editor.getValue());
                }
                break;
            }
            default:
                console.log(first.id);
                return;
        }
    });

    stage.add(inspectLayer);
    stage.add(leftLayer);
    stage.add(rightLayer);
}
