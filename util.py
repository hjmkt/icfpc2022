from common import *

def move_to_isl(move):
    match move.move_type:
        case "pcut":
            block_id = move.options["block_id"]
            (offset_x, offset_y) = move.options["point"]
            return f"cut[{block_id}][{offset_x},{offset_y}]"
        case "lcut":
            block_id = move.options["block_id"]
            orientation = move.options["orientation"]
            offset = move.options["offset"]
            return f"cut[{block_id}][{'X' if orientation=='vertical' else 'Y'}][{offset}]"
        case "color":
            block_id = move.options["block_id"]
            color = move.options["color"]
            return f"color[{block_id}][{color[0]},{color[1]},{color[2]},{color[3]}]"
        case "swap":
            block_id0 = move.options["block_id0"]
            block_id1 = move.options["block_id1"]
            return f"swap[{block_id0}][{block_id1}]"
        case "merge":
            block_id0 = move.options["block_id0"]
            block_id1 = move.options["block_id1"]
            return f"merge[{block_id0}][{block_id1}]"

def moves_to_isl(moves):
    isl = []
    for move in moves:
        isl.append(move_to_isl(move))
    return "\n".join(isl)
