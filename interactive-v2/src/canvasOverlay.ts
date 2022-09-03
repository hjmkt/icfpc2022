import Konva from "konva";
import {queryPixel} from "./problems";

const width = 812;
const height = 802;

export function setupOverlay() {
    const stage = new Konva.Stage({
        container: "canvas-overlay",
        width: width,
        height: height
    });

    const leftLayer = new Konva.Layer({
        x: 1,
        y: 1,
    });

    const leftCanvas = new Konva.Rect({
        x: 0,
        y: 0,
        width: 400,
        height: 400,
        // fill: "red",
        // opacity: 0.5,
    });

    leftLayer.add(leftCanvas);

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

    const vline1 = new Konva.Line({
        points: [200, 0, 200, 399],
        stroke: "white",
        strokeWidth: 1
    });
    const vline2 = new Konva.Line({
        points: [200, 0, 200, 399],
        stroke: "gray",
        strokeWidth: 1,
        dash: [5]
    })
    const hline1 = new Konva.Line({
        points: [0, 200, 400, 200],
        stroke: "white",
        strokeWidth: 1
    });
    const hline2 = new Konva.Line({
        points: [0, 200, 400, 200],
        stroke: "gray",
        strokeWidth: 1,
        dash: [5]
    });
    rightLayer.add(vline1);
    rightLayer.add(vline2);
    rightLayer.add(hline1);
    rightLayer.add(hline2);

    rightCanvas.on("pointermove", () => {
        const pos = rightCanvas.getRelativePointerPosition();
        const x = Math.max(0, Math.min(399, Math.floor(pos.x) + 1));
        const y = Math.max(0, Math.min(399, Math.floor(pos.y) + 1));
        const vPoints = [x, 0, x, 400];
        vline1.points(vPoints);
        vline2.points(vPoints);
        const hPoints = [0, y, 400, y];
        hline1.points(hPoints);
        hline2.points(hPoints);

        const {r, g, b, a} = queryPixel(x, y);
        const text = `point = [${x}, ${y}], color = [${r}, ${g}, ${b}, ${a}]`;
        (document.getElementById("rightCanvasText") as HTMLDivElement).innerText = text;
    });

    rightCanvas.on("pointerdown", () => {
        const pos = rightCanvas.getRelativePointerPosition();
        const x = Math.max(0, Math.min(399, Math.floor(pos.x) + 1));
        const y = Math.max(0, Math.min(399, Math.floor(pos.y) + 1));
        const {r, g, b, a} = queryPixel(x, y);
        console.log(`[${x}, ${y}]`);
        console.log(`[${r}, ${g}, ${b}, ${a}]`);
    });

    rightCanvas.on("pointerenter", () => {
        vline1.show();
        vline2.show();
        hline1.show();
        hline2.show();
    });

    rightCanvas.on("pointerleave", () => {
        vline1.hide();
        vline2.hide();
        hline1.hide();
        hline2.hide();
    });

    stage.add(leftLayer);
    stage.add(rightLayer);
}
