#!/usr/bin/env python3
"""CL5 POST-RESULT control, reported only: the frozen STATIC has no moved gas at a_f, so each cycled run also carries extra central mass (contraction). Here the same M_f sits at a_f with no bursts.
    python3 cl5_control.py NAME_OF_CYCLED_RUN; kappa = 1/2 FITTED; not theory closed."""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); T = open(os.path.join(HERE, "cl5_cycles.py")).read(); name = sys.argv[1]; Q = json.load(open(os.path.join(HERE, f"cl5_run_{name}.json")))
old = 'if N == 0: Mf, bind, el = 0.0, "none", 0.0'; assert T.count(old) == 1; T = T.replace(old, f'if N == 0: Mf, bind, el = {Q["Mf"]!r}, "control", 0.0')
NS = {"__file__": os.path.join(HERE, "cl5_cycles.py"), "__name__": "cl5_ro"}; exec(compile(T, "cl5_cycles", "exec"), NS)
NS["RUNS"][f"CTRL_{name}"] = (Q["mass"], Q["a_f"], 0, 0.0); NS["run"](f"CTRL_{name}")
