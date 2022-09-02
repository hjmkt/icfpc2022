class Canvas:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.pixels = [[[255, 255, 255, 255] for _ in range(width)] for _ in range(height)]
        self.blocks = {str(0): SimpleBlock(width, height, [255, 255, 255, 255], str(0))}
        self.coord_to_block_id = [[str(0) for _ in range(width)] for _ in range(height)]
        self.global_id = 0

    def exec_move(self, move):
        match move.move_type:
            case "pcut":
                block_id = move.options["block_id"]
                (offset_x, offset_y) = move.options["point"]
                block = self.blocks[block_id]
                # TODO
                sub_blocks = [
                    SimpleBlock(block.x, block.y, x-block.x, y-block.y, block.color, f"{block.block_id}.0"),
                    SimpleBlock(block.x+offset_x, block.y, block.width-offset_x, y-block.y, block.color, f"{block.block_id}.1"),
                    SimpleBlock(block.x+offset_x, block.y+offset_y, block.width-offset_x, block.height-offset_y, block.color, f"{block.block_id}.2"),
                    SimpleBlock(block.x, block.y+offset_y, x-block.x, block.height-offset_y, block.color, f"{block.block_id}.3"),
                ]
                for sub_block in sub_blocks:
                    self.blocks[sub_block.block_id] = sub_block
                    for y in range(sub_block.y, sub_block.y+sub_block.height):
                        for x in range(sub_block.x, sub_block.x+sub_block.width):
                            self.coord_to_block_id = sub_block.block_id
                self.blocks.pop(block.block_id)
            case "lcut":
                block_id = move.options["block_id"]
                orientation = move.options["orientation"]
                offset = move.options["offset"]
                if orientation == "vertical":
                    offset_x = offset
                    sub_blocks = [
                        SimpleBlock(block.x, block.y, x-block.x, y-block.y, block.color, f"{block.block_id}.0"),
                        SimpleBlock(block.x+offset_x, block.y, block.width-offset_x, y-block.y, block.color, f"{block.block_id}.1"),
                    ]
                else: # horizontal
                    offset_y = offset
                    sub_blocks = [
                        SimpleBlock(block.x, block.y, x-block.x, y-block.y, block.color, f"{block.block_id}.0"),
                        SimpleBlock(block.x, block.y+offset_y, x-block.x, block.height-offset_y, block.color, f"{block.block_id}.1"),
                    ]
                for sub_block in sub_blocks:
                    self.blocks[sub_block.block_id] = sub_block
                    for y in range(sub_block.y, sub_block.y+sub_block.height):
                        for x in range(sub_block.x, sub_block.x+sub_block.width):
                            self.coord_to_block_id = sub_block.block_id
                self.blocks.pop(block.block_id)
            case "color":
                block_id = move.options["block_id"]
                color = move.options["color"]
                block = self.blocks[block_id]
                block.color = color
                for y in range(block.y, block.y+block.height):
                    for x in range(block.x, block.x+block.width):
                        self.pixels[y][x] = color
            case "swap":
                block_id0 = move.options["block_id0"]
                block_id1 = move.options["block_id1"]
                block0 = self.blocks[block_id0]
                block1 = self.blocks[block_id1]
                block0.x, block1.x = block1.x, block0.x
                block0.y, block1.y = block1.y, block0.y
                block0.width, block1.width = block1.width, block0.width
                block0.height, block1.height = block1.height, block0.height
                for y in range(block0.y, block0.y+block0.height):
                    for x in range(block0.x, block0.x+block0.width):
                        self.pixels[y][x] = block0.color
                for y in range(block1.y, block1.y+block1.height):
                    for x in range(block1.x, block1.x+block1.width):
                        self.pixels[y][x] = block1.color
            case "merge":
                block_id0 = move.options["block_id0"]
                block_id1 = move.options["block_id1"]
                block0 = self.blocks[block_id0]
                block1 = self.blocks[block_id1]
                if block0.y==block1.y and max(block0.x, block1.x)-min(block0.x, block1.x)==block0.width+block1.width and block0.height==block1.height:
                    block = SimpleBlock(min(block0.x, block1.x), block0.y, block0.width+block1.width, block0.height)
                elif block0.x==block1.x and max(block0.y, block1.y)-min(block0.y, block1.y)==block0.height+block1.height and block0.width==block1.width:
                    block = SimpleBlock(block0.x, min(block0.y, block1.y), block0.width, block0.height+block1.height)
                else:
                    assert False, "invalid merge"
                self.blocks.pop(block_id0)
                self.blocks.pop(block_id1)
                self.global_id += 1
                block.block_id = self.global_id
                self.blocks[block.block_id] = block

class SimpleBlock:
    def __init__(self, x, y, width, height, color, block_id):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.block_id = block_id

class ComplexBlock:
    def __init__(self, x, y, width, height, block_id, child_blocks):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.block_id = block_id
        self.child_blocks = child_blocks

class Move:
    def __init__(self, move_type, options):
        self.move_type = move_type
        self.options = options
