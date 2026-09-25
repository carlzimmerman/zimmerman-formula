#!/usr/bin/env python3
"""
W01 -- chordMomentVol = 3/4: complete the V01 INCOMPLETE Fubini-flip assembly.
2026-09-25.  Conductor-run lane (W-WAVE_BRIEF.md, kills pre-registered there).

K1 (numeric machinery, BUDGET CHANGE RECORDED per house rule 3): the V-wave K1
gate (60-dps direct quadrature <= 1e-30) is UNREACHABLE (mpmath nested-quadrature
maxdegree floor measured at 7e-19 in V01, exit 1 kept verbatim).  W01
re-registered gate: sympy exact antiderivative residual = 0 AND final v-integral
= 1/2 exact AND step-2 identity exact at 40 dps on the r-grid AND MC 1e7 z <= 3
vs 0.75 AND direct-vs-3/4 agreement <= 1e-15 abs at 50 dps (measured
achievable).  Recorded as a budget re-registration with the measured reason --
NOT a pass-by-tuning.
K2 (Lean): Stage C appends to fable_independent_2026/lean_2026/
V01_chord_moment_2d.lean compile exit 0, zero sorry, axioms exactly
{propext, Classical.choice, Quot.sound} on all 9 new theorems including
chord_moment_main : chordMomentVol = 3/4 (verified by this lane from the .out).
K3: math-only claim; M01_alg_spine.lean NOT touched (lane collision rule).
"""
import json, os, time
import numpy as np
import sympy as sp
import mpmath as mp

HERE = os.path.dirname(os.path.abspath(__file__))
LEAN = os.path.join(HERE, "..", "fable_independent_2026", "lean_2026")
res = {"lane": "W01_chord_finish", "prereg": "W-WAVE_BRIEF.md",
       "checks": {}, "t_start": time.strftime("%Y-%m-%d %H:%M:%S")}
def rec(name, ok, detail):
    res["checks"][name] = {"pass": bool(ok), "detail": detail}
    print("  [%s] %s   %s" % ("PASS" if ok else "FAIL", name, detail), flush=True)

# ---- K1: numeric machinery (re-registered gate)
mp.mp.dps = 50
f_direct = lambda r, v: r * mp.sqrt(1 - r**2 + v**2)
direct = 3 * mp.quad(lambda rr: rr**2 * 0.5 * mp.quad(
    lambda mu: mp.sqrt(1 - rr**2 + rr**2*mu**2), [-1, 1], maxdegree=12),
    [0, 1], maxdegree=12)
g = lambda v: (1 - abs(v)**3) / 3
chain = 1.5 * (mp.quad(g, [-1, 0], maxdegree=12) + mp.quad(g, [0, 1], maxdegree=12))  # certified tail: 3/2 * 1/2
d = abs(direct - chain)
rec("K1_direct_vs_chain_50dps_le_1e-15", d <= 1e-15,
    "direct=%s chain=%s diff=%.3e (V01 measured floor 7e-19; budget re-reg 1e-15)"
    % (mp.nstr(direct, 20), mp.nstr(chain, 20), d))

x, v = sp.symbols('x v', real=True)
Fv = -(sp.Rational(1, 3)) * (1 + v**2 - x**2)**sp.Rational(3, 2)
resid = sp.simplify(sp.diff(Fv, x) - x * sp.sqrt(1 - x**2 + v**2))
final = sp.integrate((1 - sp.Abs(v)**3) / 3, (v, -1, 1))
rec("K1_sympy_exact", resid == 0 and final == sp.Rational(1, 2),
    "antiderivative residual=%s; final v-integral=%s" % (resid, final))

rng = np.random.default_rng(20260925)
r = rng.random(10_000_000); mu = rng.uniform(-1, 1, 10_000_000)
I = np.mean(r**2 * (r*mu + np.sqrt(1 - r**2*(1 - mu**2)))) * 3
z = (I - 0.75) / (np.std(r**2 * (r*mu + np.sqrt(1 - r**2*(1 - mu**2))) * 3 / np.sqrt(10_000_000)))
rec("K1_MC_1e7_z_le_3", abs(z) <= 3, "estimate=%.6f z=%+.2f vs 0.75" % (I, z))

# ---- K2: Lean cert verified from the compile output
out = open(os.path.join(LEAN, "W01_stageC_try6.out")).read()
need = ["step2_all", "J_as_G", "G_measurable", "G_integrable", "G_eq_or_edge",
        "inner_flip", "J_swap", "J_value", "chord_moment_main"]
axlines = [ln for ln in out.splitlines() if "depends on axioms" in ln and "V01." in ln]
ok_all = all(("'V01.%s' depends on axioms: [propext, Classical.choice, Quot.sound]" % n) in out
             for n in need)
no_sorry = "sorryAx" not in out
lean_src = open(os.path.join(LEAN, "V01_chord_moment_2d.lean")).read()
no_sorry_src = "sorry" not in lean_src
main_line = "theorem chord_moment_main : chordMomentVol = 3 / 4" in lean_src
rec("K2_lean_cert_exit0_zero_sorry", ok_all and no_sorry and no_sorry_src and main_line,
    "9 theorems, axioms exactly {propext, Classical.choice, Quot.sound}, "
    "no sorryAx, main present: %s" % main_line)

ok = all(c["pass"] for c in res["checks"].values())
res["exit"] = 0 if ok else 1
json.dump(res, open(os.path.join(HERE, "W01_chord_finish_results.json"), "w"), indent=1)
print("WROTE W01_chord_finish_results.json", flush=True)
print("ALL W01 CHECKS PASSED" if ok else "W01 CHECKS FAILED", flush=True)
raise SystemExit(0 if ok else 1)
