# icfpc2022

Team sonna_baka_na's repository

# Requirements

- Python 3.10
- Node.js & npm

# Setup

```bash
pip install -r requirements.txt
```

# Usage

## Run solver

solution will be exported as "isl_p{PROBLEM_ID}_{SCORE}.txt" (auto submission was enabled when API token was specified, during the contest)
Up to 256 is mostly used for NUM_OF_INITIAL_SEEDS during the contest.

```bash
# run solver with rect-fill strategy
python solver/solve_with_rect_fill.py -p PROBLEM_ID -s NUM_OF_INITIAL_SEEDS [-r EXISTING_JSON_TO_OPTIMIZE] [-t API_TOKEN]

# adjust positions of existing cut moves
python solver/adjust.py -p PROBLEM_ID -s NUM_OF_INITIAL_SEEDS -r EXISTING_JSON_TO_OPTIMIZE [-t API_TOKEN]

# run solver with rect-fill strategy, then adjust positions of cut moves
python solver/solve.py -p PROBLEM_ID -s NUM_OF_INITIAL_SEEDS [-r EXISTING_JSON_TO_OPTIMIZE] [-t API_TOKEN]
```


## Run interactive UI

```
cd interactive-v2
npm install
npm start
```

