import {Interpreter, Painter} from "./mini-vinci";
import * as ace from "brace";
import "brace/theme/solarized_light";
import {drawCanvas} from "./utils";
import {setupOverlay} from "./canvasOverlay";
import {calcScore, changeProblem} from "./problems";

const editor = ace.edit("isl");
editor.setTheme("ace/theme/solarized_light")

const runButton = document.getElementById("runButton") as HTMLButtonElement;
runButton.addEventListener("click", () => {
    const islText  = editor.getValue();

    const interpreter = new Interpreter();
    const interpretedStructure = interpreter.run(islText);

    const painter = new Painter();
    const renderedData = painter.draw(interpretedStructure.canvas);

    const canvas = document.getElementById("leftCanvas") as HTMLCanvasElement;
    drawCanvas(canvas, renderedData);

    calcScore(interpretedStructure.cost, renderedData);
});

const problemSelector = document.getElementById("problem") as HTMLSelectElement;
problemSelector?.addEventListener("change", () => {
    changeProblem(problemSelector.value);
});

document.addEventListener("DOMContentLoaded", () => {
   const numProblems = 25;
    for (let i = 1; i <= numProblems; i++) {
        const option = document.createElement("option");
        option.innerText = `${i}`;
        problemSelector.appendChild(option);
    }
    changeProblem("1");

    setupOverlay();
});
