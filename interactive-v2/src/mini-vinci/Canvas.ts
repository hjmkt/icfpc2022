import { Block, SimpleBlock } from "./Block";
import { RGBA } from "./Color";
import { Point } from "./Point";

export type Color = RGBA;

export interface CanvasSpec {
    width: number;
    height: number;
    blocks: BlockSpec[];
}

export interface BlockSpec {
    blockId: string;
    bottomLeft: [number, number];
    topRight: [number, number];
    color: [number, number, number, number];
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
