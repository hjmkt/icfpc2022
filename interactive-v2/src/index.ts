import * as ace from "brace";
import "brace/theme/solarized_light";
import { runCode, untilLine } from "./utils";
import { setTool, setupOverlay } from "./canvasOverlay";
import { changeProblem } from "./problems";
import { parseAndDownloadIsl } from "./parser";

const editor = ace.edit("isl");
editor.setTheme("ace/theme/solarized_light");

const runButton = document.getElementById("runButton") as HTMLButtonElement;
runButton.addEventListener("click", () => {
    runCode(editor.getValue());
});

const jsonButton = document.getElementById("jsonButton") as HTMLButtonElement;
jsonButton.addEventListener("click", () => {
    parseAndDownloadIsl(editor.getValue());
});

const overlayButton = document.getElementById("overlay") as HTMLButtonElement;
overlayButton.addEventListener("mousedown", () => {
    const overlay = document.getElementById(
        "rightCanvasOverlay"
    ) as HTMLCanvasElement;
    overlay.style.display = "block";
});
overlayButton.addEventListener("mouseup", () => {
    const overlay = document.getElementById(
        "rightCanvasOverlay"
    ) as HTMLCanvasElement;
    overlay.style.display = "none";
});

const range = document.getElementById("range") as HTMLInputElement;
range.addEventListener("input", () => {
    (document.getElementById("timestamp") as HTMLDivElement).innerText =
        range.value;

    const code = untilLine(editor.getValue(), Number(range.value));
    runCode(code, false);
});

const problemSelector = document.getElementById("problem") as HTMLSelectElement;
problemSelector?.addEventListener("change", () => {
    changeProblem(problemSelector.value).then(() => {
        runCode("");
    });
});

const tool = document.getElementById("tool") as HTMLSelectElement;
tool.addEventListener("change", () => {
    setTool(tool.value);
});

document.addEventListener("DOMContentLoaded", () => {
    const numProblems = 35;
    for (let i = 1; i <= numProblems; i++) {
        const option = document.createElement("option");
        option.innerText = `${i}`;
        problemSelector.appendChild(option);
    }
    changeProblem("1").then(() => {
        runCode("");
    });

    setupOverlay(editor);
});
