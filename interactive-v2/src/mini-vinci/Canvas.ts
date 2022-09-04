import { Block, ComplexBlock, SimpleBlock } from "./Block";
import { RGBA } from "./Color";
import { Point } from "./Point";

export type Color = RGBA;

export interface CanvasSpec {
    width: number;
    height: number;
    blocks: BlockSpec[];
    sourcePngJSON?: string;
}

export interface BlockSpec {
    blockId: string;
    bottomLeft: [number, number];
    topRight: [number, number];
    color: [number, number, number, number];
    source?: [number, number, number, number][];
}

export class Canvas {
    width: number;

    height: number;

    // backgroundColor: Color;

    blocks: Map<string, Block>;

    constructor({ width, height, blocks }: CanvasSpec) {
        this.width = width;
        this.height = height;

        // this.backgroundColor = backgroundColor;
        this.blocks = new Map();
        blocks.forEach((block) => {
            if (block.source === undefined || block.source.length === 0) {
                this.blocks.set(
                    block.blockId,
                    new SimpleBlock(
                        block.blockId,
                        new Point(block.bottomLeft),
                        new Point(block.topRight),
                        {
                            r: block.color[0],
                            g: block.color[1],
                            b: block.color[2],
                            a: block.color[3],
                        }
                    )
                );
            } else {
                const subBlocks: SimpleBlock[] = [];
                let idx = 0;
                for (let y = 399; y >= 0; y--) {
                    for (let x = 0; x < 400; x++) {
                        const color = block.source[idx++];
                        if (!color) continue;
                        const pixel = new SimpleBlock(
                            "pixel",
                            new Point([x, y]),
                            new Point([x + 1, y + 1]),
                            {
                                r: color[0],
                                g: color[1],
                                b: color[2],
                                a: color[3],
                            }
                        );
                        subBlocks.push(pixel);
                    }
                }
                this.blocks.set(
                    block.blockId,
                    new ComplexBlock(
                        block.blockId,
                        new Point(block.bottomLeft),
                        new Point(block.topRight),
                        subBlocks
                    )
                );
            }
        });
    }

    get size(): Point {
        return new Point([this.width, this.height]);
    }

    simplify(): SimpleBlock[] {
        let simplifiedBlocks: SimpleBlock[] = [];
        this.blocks.forEach((value) => {
            simplifiedBlocks = simplifiedBlocks.concat(value.getChildren());
        });
        return simplifiedBlocks;
    }
}
