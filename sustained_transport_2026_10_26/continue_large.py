import argparse,json
from pathlib import Path
from evolve import run
p=argparse.ArgumentParser();p.add_argument('--output',required=True);a=p.parse_args()
run(json.loads(Path('sustained_transport_2026_10_26/continue_large_config.json').read_text()),a.output)
