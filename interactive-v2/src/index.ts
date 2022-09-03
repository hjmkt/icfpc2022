import {Frame, Interpreter, Painter, SimilarityChecker} from "./mini-vinci";

const runButton = document.getElementById("runButton");
runButton?.addEventListener("click", () => {
    const isl = document.getElementById("isl") as HTMLTextAreaElement;
    const islText  = isl.value;

    const interpreter = new Interpreter();
    const interpretedStructure = interpreter.run(islText);

    const painter = new Painter();
    const renderedData = painter.draw(interpretedStructure.canvas);

    const canvas = document.getElementById("leftCanvas") as HTMLCanvasElement;
    drawCanvas(canvas, renderedData);
});

const problemSelector = document.getElementById("problem") as HTMLSelectElement;
problemSelector?.addEventListener("change", () => {
    changeProblem(problemSelector.value);
});

document.addEventListener("DOMContentLoaded", () => {
   changeProblem("1");
});

function changeProblem(id: string): void {
    fetch(`/${id}.json`).then(response => {
        response.json().then(data => {
            const rightCanvas = document.getElementById("rightCanvas") as HTMLCanvasElement;
            drawCanvas(rightCanvas, SimilarityChecker.dataToFrame(data));
        })
    });
}

function drawCanvas(canvas: HTMLCanvasElement, frame: Frame): void {
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
