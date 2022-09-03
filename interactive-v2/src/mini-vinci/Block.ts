import { Point } from "./Point";
import { RGBA } from "./Color";

export type Size = Point;
export enum BlockType {
  SimpleBlockType,
  ComplexBlockType,
}
export type Block = SimpleBlock | ComplexBlock;

export class SimpleBlock {
  typ: BlockType;

  id: string;

  bottomLeft: Point;

  topRight: Point;

  size: Size;

  color: RGBA;

  constructor(id: string, bottomLeft: Point, topRight: Point, color: RGBA) {
    this.typ = BlockType.SimpleBlockType;
    this.id = id;
    this.bottomLeft = bottomLeft;
    this.topRight = topRight;
    this.size = topRight.getDiff(bottomLeft);
    this.color = color;
    if (
      this.bottomLeft.px > this.topRight.px ||
      this.bottomLeft.py > this.topRight.py
    ) {
      throw Error("Invalid Block");
    }

    if (this.size.getScalarSize() == 0) {
      throw new Error("Block size cannot be 0!");
    }
  }

  getChildren() {
    return [this];
  }
}

export class ComplexBlock {
  typ: BlockType;

  id: string;

  bottomLeft: Point;

  topRight: Point;

  size: Size;

  subBlocks: SimpleBlock[];

  constructor(
    id: string,
    bottomLeft: Point,
    topRight: Point,
    subBlocks: SimpleBlock[]
  ) {
    this.typ = BlockType.ComplexBlockType;
    this.id = id;
    this.bottomLeft = bottomLeft;
    this.topRight = topRight;
    this.size = topRight.getDiff(bottomLeft);
    this.subBlocks = subBlocks;

    if (this.size.getScalarSize() == 0) {
      throw new Error("Block size cannot be 0!");
    }
  }

  getChildren() {
    return this.subBlocks;
  }

  offsetChildren(newBottomLeft: Point) {
    let newChildren: SimpleBlock[] = [];
    this.subBlocks.forEach((block) => {
      newChildren.push(
        new SimpleBlock(
          "child",
          block.bottomLeft.add(newBottomLeft).subtract(this.bottomLeft),
          block.topRight.add(newBottomLeft).subtract(this.bottomLeft),
          block.color
        )
      );
    });
    return newChildren;
  }
}
