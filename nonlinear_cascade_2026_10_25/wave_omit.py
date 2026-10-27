import argparse
from cc_wave_checked import run
p=argparse.ArgumentParser();p.add_argument("--output",required=True);args=p.parse_args();run({'q': 80.0, 'dt_Myr': 0.005, 'duration_Myr': 100.0, 'wall_seconds': 300, 'wave_h_kpc': 2.0, 'omit_inertia': True, 'g2_override': None},args.output)
