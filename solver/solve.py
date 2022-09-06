import argparse
import isl_json_reader
import adjust
import solve_with_rect_fill

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--problem", type=int)
    parser.add_argument("-s", "--seed", type=int)
    parser.add_argument("-t", "--token", type=str)
    parser.add_argument("-r", "--resume", type=str)
    args = parser.parse_args()
    if args.resume is not None:
        resume_moves = isl_json_reader.read_json(args.resume)
    else:
        resume_moves = []

    moves = solve_with_rect_fill.solve(
        args.problem, args.seed, args.token, resume_moves
    )
    adjusted_moves = adjust.adjust(args.problem, args.seed, args.token, moves)
