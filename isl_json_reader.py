from common import *
import json

def read_json(isl_json_path):
    moves = []
    with open(isl_json_path) as f:
        isl_json = json.load(f)
        for isl_move in isl_json:
            match isl_move["typ"]:
                case "PointCut":
                    move = Move("pcut", {"block_id": isl_move["blockId"], "point": [isl_move["point"]["x"], isl_move["point"]["y"]]})
                case "Color":
                    move = Move("color", {"block_id": isl_move["blockId"], "color": [isl_move["color"]["r"], isl_move["color"]["g"], isl_move["color"]["b"], isl_move["color"]["a"]]})
                case "Merge":
                    move = Move("merge", {"block_id0": isl_move["blockId1"], "block_id1": isl_move["blockId2"]})
                case "VerticalCut":
                    move = Move("lcut", {"block_id": isl_move["blockId"], "orientation": "vertical", "offset": isl_move["lineNumber"]})
                case "HorizontalCut":
                    move = Move("lcut", {"block_id": isl_move["blockId"], "orientation": "horizontal", "offset": isl_move["lineNumber"]})
                case "Swap":
                    move = Move("merge", {"block_id0": isl_move["blockId1"], "block_id1": isl_move["blockId2"]})
            moves.append(move)
    return moves

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", type=str)
    args = parser.parse_args()
    moves = read_json(args.input)
    print(moves)
