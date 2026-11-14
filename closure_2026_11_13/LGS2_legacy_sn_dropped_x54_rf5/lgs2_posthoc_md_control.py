"""LGS2 POST HOC (written after the X54 des_only numbers; not in FROZEN_CRITERIA.md; no label attached):
the size control for X54's M-D model. The frozen control (rand197) ran M-C only. M-D's class changed for des_only, so this
runs the same rand197 draw (seed 20261113) through both models, to see whether the loss of any 197 supernovae moves M-D.
M-C in this run must reproduce the frozen rand197 M-C exactly (same code, same draw): a reproducibility check.
It executes the frozen harness lgs2_run.py with three exact substitutions (models, output name, run dir), nothing else.

usage: python3 -I -B lgs2_posthoc_md_control.py          (writes lgs2_posthoc_x54_rand197_CD.{out,json})
kappa = 1/2 FITTED; not theory closed.
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "lgs2_run.py")


def sub(text, old, new):
    assert text.count(old) == 1, f"expected exactly one occurrence of: {old!r} (found {text.count(old)})"
    return text.replace(old, new)


t = open(SRC).read()
t = sub(t, 'LGS_MODELS=("C",) if SAMPLE == "rand197" else ("C", "D")', 'LGS_MODELS=("C", "D")')
t = sub(t, 'out = os.path.join(HERE, f"lgs2_x54_{SAMPLE}")', 'out = os.path.join(HERE, f"lgs2_posthoc_x54_{SAMPLE}_CD")')
t = sub(t, 'LGS_RUNS=os.path.join(X54_BUILD, f"runs_{SAMPLE}")', 'LGS_RUNS=os.path.join(X54_BUILD, f"runs_posthoc_{SAMPLE}")')
sys.argv = [SRC, "x54", "rand197"]
exec(compile(t, SRC, "exec"), {"__name__": "__main__", "__file__": SRC})
