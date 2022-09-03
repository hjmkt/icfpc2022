import * as ace from "brace";
import "brace/theme/solarized_light";
import { runCode } from "./utils";
import { setupOverlay } from "./canvasOverlay";
import { changeProblem } from "./problems";
import {parseAndDownloadIsl} from "./parser";

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
    runCode("");

    setupOverlay();
});
