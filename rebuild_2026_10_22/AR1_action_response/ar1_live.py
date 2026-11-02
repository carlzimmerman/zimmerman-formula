#!/usr/bin/env python3
"""AR1 live validation: DR8's dr8_live.py, unchanged, at another mass, by replacing its setup and softening from ar1_setup.json. SIGTERM -> checkpoint, exit 75, --resume. Runs under runs/ here.
    python3 ar1_live.py TAG dr8_live-arguments...   kappa = 1/2 FITTED, unused; not theory closed."""
import json, os, sys
sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__)); RB = os.path.dirname(HERE); sys.path.insert(0, os.path.join(RB, "DR8_pressure_core_response")); import dr8_ic as IC, dr8_live as DL
TAG = sys.argv[1]; S = json.load(open(os.path.join(HERE, "ar1_setup.json")))[TAG]; IC.setup = lambda tag=None: dict(S); DL.EPS = S["eps"]
sys.exit(DL.main(sys.argv[2:]))
