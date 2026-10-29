#!/usr/bin/env python3
"""IN1_ic1613_inclination: is IC 1613's two-tracer failure consistent with one (near face-on) inclination?
Frozen criteria f4d9ab5eea (committed alone). Inputs: X1's sigma and r_h; LITTLE THINGS masses and HI V_rot as parsed by RT1 (66c45c5082).

kappa = 1/2 FITTED; footings never pooled; not theory closed; nothing here says the data favour the framework.
Run:  PYTHONHASHSEED=0 python3 -I in1_ic1613_inclination.py      (IN1_MUTATE=1 twin)
"""
import os, sys, json, math, hashlib
import numpy as np

MUT = os.environ.get("IN1_MUTATE", "0") == "1"; TAG = "_MUTATE" if MUT else ""
HERE = os.path.dirname(os.path.abspath(__file__)); REB = os.path.dirname(HERE)
G, MSUN, PC = 6.67430e-11, 1.98847e30, 3.0856775814913673e16
KPC = 1e3 * PC; A0 = {"canonical": 9.3603e-11, "alt": 1.1312e-10}
OUT = []
def P(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); OUT.append(s)
nu = lambda y: 0.5 + math.sqrt(0.25 + 1.0 / y)
P(f"IN1_ic1613_inclination (criteria f4d9ab5eea){'  [MUTATE: sin/cos swapped]' if MUT else ''}; kappa = 1/2 FITTED; not theory closed")
RT = json.load(open(os.path.join(REB, "RT1_lt_rotation_regrade", "rt1_lt_rotation_regrade_results.json")))
SIG, RH, LMS_X1 = 10.8, 1439.78, 8.28                     # X1 row (b = 1 for IC 1613)
MS, MG = 2.88e7, 5.93e7                                     # Oh+15 Table 2 (RT1 parse)
VROT48, RMAX, I0 = 16.9, 2.71, 48.0
VST = 13.0                                                  # UNGC vAmp (FD1's K term)
r12 = 4 / 3 * RH * PC

def vsq_disc(i_deg, q):
    i = math.radians(i_deg); c2, s2 = math.cos(i) ** 2, math.sin(i) ** 2
    if MUT: c2, s2 = s2, c2
    sR2 = SIG ** 2 / (q * q * c2 + s2)
    return sR2 * (2 + q * q)
def E_sigma(i_deg, q, a0, spherical=False, mb_half=None, vrot=VST):
    v2 = 3 * SIG ** 2 if spherical else vsq_disc(i_deg, q) + vrot ** 2
    gobs = v2 * 1e6 / r12
    mbh = (0.5 * MS + 0.5 * MG) if mb_half is None else mb_half
    gN = G * mbh * MSUN / r12 ** 2
    return math.log10(gobs) - math.log10(nu(gN / a0) * gN)
def E_HI(i_deg, a0):
    V = VROT48 * math.sin(math.radians(I0)) / math.sin(math.radians(i_deg))
    gobs = (V * 1e3) ** 2 / (RMAX * KPC); gN = G * (MS + MG) * MSUN / (RMAX * KPC) ** 2
    return math.log10(gobs) - math.log10(nu(gN / a0) * gN)

checks = {}
e0 = E_sigma(48, 1.0, A0["canonical"], spherical=True, mb_half=0.5 * 10 ** LMS_X1, vrot=0.0)
checks["K0"] = abs(e0 - (-0.535162)) < 0.01
e0b = E_HI(48, A0["canonical"]); checks["K0b"] = abs(e0b - RT["lg"]["canonical"]["IC 1613"]["MSED"]["E"]) < 0.001
checks["K1"] = all(abs(vsq_disc(i, 1.0) / (3 * SIG ** 2) - 1) < 1e-12 for i in np.arange(10, 60.01, 0.5))
ss = [E_sigma(i, 0.6, A0["canonical"]) for i in (60, 40, 20)]
checks["K2"] = ss[0] < ss[1] < ss[2]
P(f"  K0 spherical, X1 baryons, i 48: E {e0:+.4f} (HO3 -0.5352): {'PASS' if checks['K0'] else 'FAIL'};  K0b HI at 48: {e0b:+.4f} (RT1): {'PASS' if checks['K0b'] else 'FAIL'}")
P(f"  K1 isotropic disc = spherical: {'PASS' if checks['K1'] else 'FAIL'};  K2 E_sigma rises toward face-on (q 0.6): {'PASS' if checks['K2'] else 'FAIL'}")
IS = np.round(np.arange(10.0, 60.001, 0.5), 1)
RES = dict(criteria="f4d9ab5eea", mutate=MUT, footings={})
def interval(mask):
    xs = IS[mask]; return [float(xs.min()), float(xs.max())] if len(xs) else None
for f, a0 in A0.items():
    out = {}
    eh = np.array([E_HI(i, a0) for i in IS]); ih = np.abs(eh / 0.075) < 2
    for q in (0.6, 0.4, 0.8):
        es = np.array([E_sigma(i, q, a0) for i in IS]); isg = np.abs(es / 0.0792) < 2
        both = ih & isg
        lit = {f"i{x}": dict(E_sigma=float(E_sigma(x, q, a0)), E_HI=float(E_HI(x, a0))) for x in (48, 39, 20, 15)}
        I = interval(both)
        v = ("INCLINATION RESOLVES IC 1613" if I and I[1] >= 15 and I[0] <= 48 else
             ("INCLINATION RESOLVES ONLY IF i < 15" if I else "INCLINATION DOES NOT RESOLVE IC 1613"))
        out[f"q{q}"] = dict(I_sigma=interval(isg), I_HI=interval(ih), I_both=I, lit=lit, verdict=v)
        P(f"\n  [{f}] q_sigma {q}: I_sigma {interval(isg)}  I_HI {interval(ih)}  both {I} -> {v}")
        P("     " + "; ".join(f"i {x}: E_sigma {lit[f'i{x}']['E_sigma']:+.3f}, E_HI {lit[f'i{x}']['E_HI']:+.3f}" for x in (48, 39, 20, 15)))
    RES["footings"][f] = out
RES["checks"] = checks; RES["verdict"] = {f: RES["footings"][f]["q0.6"]["verdict"] for f in A0}
P(f"\n=== VERDICT (q 0.6): canonical {RES['verdict']['canonical']}; alt {RES['verdict']['alt']}")
fn = os.path.join(HERE, f"in1_ic1613_inclination_results{TAG}.json")
json.dump(RES, open(fn, "w"), indent=1, default=float)
P(f"checks {sum(checks.values())}/{len(checks)}; results sha256 {hashlib.sha256(open(fn, 'rb').read()).hexdigest()}")
open(os.path.join(HERE, f"in1_ic1613_inclination{TAG}.out"), "w").write("\n".join(OUT) + "\n")
sys.exit(0 if all(checks.values()) else 1)
