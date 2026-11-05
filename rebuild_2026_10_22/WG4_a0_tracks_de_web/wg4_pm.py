#!/usr/bin/env python3
"""WG4 engine (FROZEN_CRITERIA.md, 6f8cd8bbd1): WG2's engine (imported read only) with a0 tracking dark energy.
a0 rules: DE = a0_foot sqrt(rho_DE(z)/rho_DE0) with DESI DR2 CPL (-0.838, -0.62) via a0kit.rho_de_ratio; NATLOW = the native CFG689
band's lower 68 % edge (1, 0.76, 0.71, 0.33 at z 0, 1, 1.5, 2.33), held beyond. Backgrounds B2D / B1D = WG2's B2 / B1 with CPL dark
energy in place of Lambda; their ICs are B2's / B1's (dark energy is under 1e-4 of the matter at z_on 50 either way).
Usage: python3 wg4_pm.py run RULE A0RULE BG AS N NSTEP ZON FOOT   (writes runs/<tag>.json here)
       python3 wg4_pm.py checks                                  (WG2's K1, K2 and K9; runs/checks.json)
       WG2_MUTATE=1 halves the Poisson factor in the imported engine (K1 must FAIL).
kappa = 1/2 FITTED; the cold sector stays retired; not theory closed."""
import os, sys, json, math
HERE = os.path.dirname(os.path.abspath(__file__)); REB = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(REB, "WG2_bare_law_web_lensing")); import wg2_pm as B   # read only
import numpy as np
A0K = B.a0kit
B.RUNS = os.path.join(HERE, "runs")
W0, WA = -0.838, -0.62
NAT_Z = [0.0, 1.0, 1.5, 2.33]; NAT_LOW = [1.00, 0.76, 0.71, 0.33]
_base_background, _base_a0, _base_ics = B.background, B.a0_code, B.class_ics

def background(bg, w0=W0, wa=WA):
    if bg in ("B2D", "B1D"):
        om = (B.OMB + B.OFLD) if bg == "B2D" else B.OMB
        ode = 1 - om - B.OMR
        return (lambda a: math.sqrt(B.OMR / a ** 4 + om / a ** 3 + ode * float(A0K.rho_de_ratio(1 / a - 1, w0, wa)))), B.OMB
    return _base_background(bg)

def a0_code(a, a0rule, foot, E):
    base = B.A0[foot] / B.ACC_UNIT; z = 1 / a - 1
    if a0rule == "DE": return base * math.sqrt(float(A0K.rho_de_ratio(z, W0, WA)))
    if a0rule == "NATLOW": return base * float(np.interp(z, NAT_Z, NAT_LOW))
    return _base_a0(a, a0rule, foot, E)

def class_ics(bg, z_on):
    return _base_ics({"B2D": "B2", "B1D": "B1"}.get(bg, bg), z_on)

B.background, B.a0_code, B.class_ics = background, a0_code, class_ics   # WG2's run() now uses these

def checks():
    out = dict(B.checks())
    ea = abs(a0_code(1 / 3, "DE", "canonical", None) / (B.A0["canonical"] / B.ACC_UNIT) - float(A0K.a0_of_z(2.0, W0, WA, 1.0)))
    E2, _ = background("B2D"); eb = abs(E2(1.0) - 1.0)
    Ed, _ = background("B2D", -1.0, 0.0); Eb, _ = _base_background("B2")
    ec = max(abs(Ed(1 / (1 + z)) / Eb(1 / (1 + z)) - 1) for z in (0.0, 1.0, 10.0, 50.0))
    out["K9"] = dict(a0_DE_z2=ea, E0=eb, lambda_limit=ec, pass_=bool(ea < 1e-9 and eb < 1e-9 and ec < 1e-12))
    print(f"K9: a0 DE at z 2 vs a0kit {ea:.1e}; E(0) - 1 {eb:.1e}; w=-1 limit vs B2 {ec:.1e} -> {'PASS' if out['K9']['pass_'] else 'FAIL'}")
    os.makedirs(B.RUNS, exist_ok=True); json.dump(out, open(os.path.join(B.RUNS, f"checks{B.SUF}.json"), "w"), indent=1)
    return out

if __name__ == "__main__":
    if sys.argv[1] == "checks":
        checks()
    else:
        _, _, rule, a0r, bg, As, N, ns, zon, foot = sys.argv
        B.run(rule, a0r, bg, float(As), int(N), int(ns), float(zon), foot)
