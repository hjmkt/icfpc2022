import * as ace from "brace";
import "brace/theme/solarized_light";
import { runCode, untilLine } from "./utils";
import { setGrid, setTool, setupOverlay } from "./canvasOverlay";
import { changeProblem, getCurrentSpec } from "./problems";
import { parseAndDownloadIsl, parseIsl } from "./parser";
import axios from "axios";

const commandStorageKey = "icfpc2022-interactive-v2-command";

const editor = ace.edit("isl");
editor.setTheme("ace/theme/solarized_light");

const runButton = document.getElementById("runButton") as HTMLButtonElement;
runButton.addEventListener("click", () => {
    const spec = getCurrentSpec();
    runCode(editor.getValue(), true, !!spec.sourcePngJSON);
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
    overlay.style.opacity = "75%";
});
overlayButton.addEventListener("mouseup", () => {
    const overlay = document.getElementById(
        "rightCanvasOverlay"
    ) as HTMLCanvasElement;
    overlay.style.opacity = "0%";
});

const range = document.getElementById("range") as HTMLInputElement;
range.addEventListener("input", () => {
    (document.getElementById("timestamp") as HTMLDivElement).innerText =
        range.value;

    const code = untilLine(editor.getValue(), Number(range.value));

    const spec = getCurrentSpec();

    runCode(code, false, !!spec.sourcePngJSON);
});

const pixelate = document.getElementById("pixelate") as HTMLSelectElement;
pixelate.addEventListener("change", () => {
    const factor = Number(pixelate.value);
    changeProblem(problemSelector.value, factor).then(() => {
        const spec = getCurrentSpec();
        runCode(editor.getValue(), true, !!spec.sourcePngJSON);
    });
});

const problemSelector = document.getElementById("problem") as HTMLSelectElement;
problemSelector?.addEventListener("change", () => {
    const factor = Number(pixelate.value);
    changeProblem(problemSelector.value, factor).then(() => {
        const spec = getCurrentSpec();
        runCode("", true, !!spec.sourcePngJSON);
    });
});

const tool = document.getElementById("tool") as HTMLSelectElement;
tool.addEventListener("change", () => {
    setTool(tool.value);
});

const commandRunButton = document.getElementById(
    "commandRun"
) as HTMLButtonElement;
commandRunButton.addEventListener("click", () => {
    const command = (document.getElementById("command") as HTMLInputElement)
        .value;

    localStorage.setItem(commandStorageKey, command);

    const isl = parseIsl(editor.getValue());
    axios.post("/api/actions/command", {
        command,
        isl,
    });
});

const grid = document.getElementById("grid") as HTMLSelectElement;
grid.addEventListener("change", () => {
    const value = Number(grid.value);
    setGrid(value);
});

document.addEventListener("DOMContentLoaded", () => {
    const overlay = document.getElementById(
        "rightCanvasOverlay"
    ) as HTMLCanvasElement;
    overlay.style.opacity = "0%";

    const numProblems = 40;
    for (let i = 1; i <= numProblems; i++) {
        const option = document.createElement("option");
        option.innerText = `${i}`;
        problemSelector.appendChild(option);
    }
    changeProblem("1", 1).then(() => {
        const spec = getCurrentSpec();
        runCode("", true, !!spec.sourcePngJSON);
    });

    setupOverlay(editor);

    const command = localStorage.getItem(commandStorageKey);
    if (command) {
        (document.getElementById("command") as HTMLInputElement).value =
            command;
    }
});
