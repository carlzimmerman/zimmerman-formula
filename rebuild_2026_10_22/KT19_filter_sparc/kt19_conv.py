#!/usr/bin/env python3
"""KT19 resolution check (added after the result, disclosed): filter rms at smoothing grid n = 3000 against the run's 1500. kappa = 1/2 FITTED; not theory closed."""
import os, sys
os.environ["KT19_N"] = "3000"; HERE = os.path.dirname(os.path.abspath(__file__))
src = open(os.path.join(HERE, "kt19.py")).read().split("# checks")[0]; ns = {"__file__": os.path.join(HERE, "kt19.py"), "__name__": "kt19conv"}; exec(src, ns)
out = []
for foot, a0 in ns["A0"].items():
    fl = ns["run"](a0, filt=True, cache={}); out.append(f"{foot} n=3000 filter rms {fl['rms']:.4f} median {fl['med']:+.4f} inner {fl['med_inner']:+.4f}")
print("\n".join(out)); open(os.path.join(HERE, "kt19_conv.out"), "w").write("\n".join(out) + "\n")
