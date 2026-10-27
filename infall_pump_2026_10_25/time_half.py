import argparse,json
from pathlib import Path
from evolve import run
ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);args=ap.parse_args()
run(json.loads(Path('infall_pump_2026_10_25/time_half_config.json').read_text()),args.output)
