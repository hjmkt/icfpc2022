import {Parser} from "./mini-vinci/Parser";
import {Program} from "./mini-vinci/Program";
import {InstructionType} from "./mini-vinci/Instruction";

export function parseAndDownloadIsl(code: string): void {
    const parser = new Parser();
    const program = parser.parse(code).result as Program;

    const result: any = [];

    program.instructions.forEach(inst => {
        switch (inst.typ) {
            case InstructionType.NopInstructionType:
                result.push({
                    typ: "Nop"
                });
                break;
            case InstructionType.CommentInstructionType:
                result.push({
                    typ: "Comment",
                    comment: inst.comment,
                });
                break;
            case InstructionType.ColorInstructionType:
                result.push({
                    typ: "Color",
                    blockId: inst.blockId,
                    color: { r: inst.color.r, g: inst.color.g, b: inst.color.b, a: inst.color.a }
                });
                break;
            case InstructionType.PointCutInstructionType:
                result.push({
                    typ: "PointCut",
                    blockId: inst.blockId,
                    point: {x: inst.point.px, y: inst.point.py}
                });
                break;
            case InstructionType.VerticalCutInstructionType:
                result.push({
                    typ: "VerticalCut",
                    blockId: inst.blockId,
                    lineNumber: inst.lineNumber
                });
                break;
            case InstructionType.HorizontalCutInstructionType:
                result.push({
                    typ: "HorizontalCut",
                    blockId: inst.blockId,
                    lineNumber: inst.lineNumber
                });
                break;
            case InstructionType.SwapInstructionType:
                result.push({
                    typ: "Swap",
                    blockId1: inst.blockId1,
                    blockId2: inst.blockId2,
                });
                break;
            case InstructionType.MergeInstructionType:
                result.push({
                    typ: "Merge",
                    blockId1: inst.blockId1,
                    blockId2: inst.blockId2,
                });
                break;
        }
    });

    const json = JSON.stringify(result, null, 4);
    const blob = new Blob([json], { type: "application/json"});

    const link = document.createElement("a");
    document.body.appendChild(link);
    link.href = window.URL.createObjectURL(blob);
    link.download = "isl.json";
    link.click();
    document.body.removeChild(link);
}
