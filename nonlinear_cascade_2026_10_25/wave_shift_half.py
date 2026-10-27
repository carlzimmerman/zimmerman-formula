import argparse
from cc_wave_renormalized import run
p=argparse.ArgumentParser();p.add_argument("--output",required=True);args=p.parse_args();run({'q': 80.0, 'dt_Myr': 0.005, 'duration_Myr': 150.0, 'wall_seconds': 240, 'wave_h_kpc': 2.0, 'omit_inertia': False, 'g2_override': None, 'renormalize': 0.5},args.output)
