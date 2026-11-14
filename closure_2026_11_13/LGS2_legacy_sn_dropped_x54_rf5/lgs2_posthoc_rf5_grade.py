"""LGS2 POST HOC (written after the runs; not in FROZEN_CRITERIA.md): RF5's grader with one reporting line guarded.

Why. As frozen, RF5's own grader stops with "math domain error" on the des_only sample: the khronon cell K0.03, which in
the committed run and in LGS2's full run ends in a CLASS stiff-solver failure (UNDETERMINED), in des_only runs on and stops
(no fall on a fresh Jacobian, 29 failed CLASS runs) at Omega_DE = -0.55, h = 0.45, plik 1.2e5. The grader's a0 readout,
a0_canonical = 0.5 c sqrt(G rho_crit Omega_DE), then takes the square root of a negative number. That line is a report
(per-cell a0), read by no gate. The guard below sets it to None when Omega_DE <= 0; nothing else changes.
The frozen harness lgs2_run.py is executed with two exact substitutions: the output name (lgs2_posthoc_rf5_<sample>) and
this guard on RF5's text. Run on both samples; the full output must equal the frozen full grade (a check of the wrapper).

usage: python3 -I -B lgs2_posthoc_rf5_grade.py <full|des_only>
kappa = 1/2 FITTED; not theory closed.
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "lgs2_run.py")


def sub(text, old, new):
    assert text.count(old) == 1, f"expected exactly one occurrence of: {old!r} (found {text.count(old)})"
    return text.replace(old, new)


def guard(t_rf5):
    return sub(t_rf5, 'if r["Omega_DE"] == r["Omega_DE"] else None',
               'if (r["Omega_DE"] == r["Omega_DE"] and r["Omega_DE"] > 0) else None')


t = open(SRC).read()
t = sub(t, 'LGS_OUT=os.path.join(HERE, f"lgs2_rf5_{SAMPLE}")', 'LGS_OUT=os.path.join(HERE, f"lgs2_posthoc_rf5_{SAMPLE}")')
t = sub(t, 'exec(compile(t, SRC, "exec"), g)', 'exec(compile(LGS_POSTHOC_GUARD(t), SRC, "exec"), g)')
sample = sys.argv[1]
assert sample in ("full", "des_only")
sys.argv = [SRC, "rf5", sample, "grade"]
exec(compile(t, SRC, "exec"), {"__name__": "__main__", "__file__": SRC, "LGS_POSTHOC_GUARD": guard})
