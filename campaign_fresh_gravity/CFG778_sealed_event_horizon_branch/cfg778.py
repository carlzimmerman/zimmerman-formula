"""CFG778 -- seal the event-horizon a0 branch (a0 ∝ 1/R_E) for the November ALMA releases.
Criteria: FROZEN_CRITERIA.md (committed alone first, 041eb8c24).  CFG571 predict imported read-only.
Run: python3 cfg778.py  (CFG778_MUTATE=1: Omega_Lambda -> 0, the branch must be flagged undefined).  Seconds.
kappa = 1/2 FITTED; not theory closed.
"""
import hashlib
import json
import math
import os
import sys

import numpy as np
from scipy import integrate

MUT = os.environ.get("CFG778_MUTATE") == "1"
HERE = os.path.dirname(os.path.abspath(__file__))
SUF = "_MUTATE" if MUT else ""
OUT = []


def P(s=""):
    print(s, flush=True)
    OUT.append(str(s))


FAILS = []


def check(name, ok, d):
    P(f"  [{'PASS' if ok else 'FAIL'}] {name}: {d}")
    if not ok:
        FAILS.append(name)


OM = 0.308
OL = 0.0 if MUT else 1 - OM
h = 0.70
c = 2.99792458e5                     # km/s
H0 = 100 * h                         # km/s/Mpc
E = lambda a: math.sqrt(OM / a ** 3 + OL)


def R_E(a):
    """c a int_a^inf da'/(a'^2 H(a'))  [Mpc]"""
    f = lambda lna: math.exp(-lna) / E(math.exp(lna))          # da/(a^2 E) = dlna / (a E)
    val, err = integrate.quad(f, math.log(a), 60.0, limit=500, epsrel=1e-12)
    tail_ok = f(60.0) * 1e3 < 1e-12 * max(val, 1e-300)
    return c / H0 * a * val, tail_ok


P("CFG778  event-horizon a0 branch" + ("  [MUTATE: Omega_Lambda = 0]" if MUT else ""))
RE0, ok0 = R_E(1.0)
if MUT:
    bounded = ok0 and RE0 < 1e6
    P(f"  EdS: R_E(0) = {RE0:.3e} Mpc, tail converged: {ok0}")
    P(f"  M1 tooth: branch {'FINITE (DID NOT BITE)' if bounded else 'UNDEFINED -> flagged (bites)'}")
    open(os.path.join(HERE, f"cfg778{SUF}.out"), "w").write("\n".join(OUT) + "\n")
    sys.exit(1)

P(f"\nK1  R_E(0) = {RE0:.2f} Mpc; c/H0 = {c / H0:.2f}; c/H_inf = {c / (H0 * math.sqrt(OL)):.2f}")
k1a = c / H0 <= RE0 <= c / (H0 * math.sqrt(OL))
errs = []
for z in (0.0, 1.0, 2.0):
    a = 1 / (1 + z)
    d = 1e-5
    dR = (R_E(a * math.exp(d))[0] - R_E(a * math.exp(-d))[0]) / (2 * d)
    errs.append(abs(dR - (R_E(a)[0] - c / (H0 * E(a)))) / R_E(a)[0])
check("K1 c/H0 <= R_E(0) <= c/H_inf and dR_E/dlna = R_E - c/H", k1a and max(errs) < 1e-6, f"max rel {max(errs):.1e}")

rE = lambda z: RE0 / R_E(1 / (1 + z))[0]
CC = {1.5: 1.3070, 2.0: 1.4399}                 # astra's REPORT.md, E-CCBH column (quoted)
rEC = lambda z: float(np.interp(z, [1.5, 2.0], [CC[1.5], CC[2.0]]))
P("\nbranch ratios a0(z)/a0(0):")
for z in (0.5, 1.0, 1.419, 1.5, 1.997, 2.0):
    P(f"  z {z:5.3f}: E (constant Lambda) {rE(z):.4f}" + (f"; E-CCBH (astra) {rEC(z):.4f}" if 1.4 <= z <= 2.0 else ""))

# ---- CFG571 import
src = open(os.path.join(HERE, "..", "CFG571_prereg_proprietary_alma", "cfg571_prereg.py")).read()
head = src.split("# ---- controls ----")[0]
ns = {"__file__": os.path.join(HERE, "..", "CFG571_prereg_proprietary_alma", "cfg571_prereg.py"), "__name__": "cfg571_import"}
argv0 = sys.argv
sys.argv = [argv0[0]]
exec(compile(head, "cfg571_head", "exec"), ns)
sys.argv = argv0
stored = json.load(open(os.path.join(HERE, "..", "CFG571_prereg_proprietary_alma", "cfg571_prereg_results.json")))["results"]["GS4_24110"]
bh = json.load(open(os.path.join(HERE, "..", "CFG775_bh_horizon_dark_energy", "cfg775_results.json")))["numbers"]["B2"]["8.0"]["r_BH"]
r_bh = lambda z: float(np.interp(z, [float(k) for k in bh], list(bh.values())))
ns["MODELS"] = {"E": rE, "E-CCBH": rEC, "F-flat": lambda z: 1.0, "F-DESI": ns["r_desi"], "BH-k3": r_bh, "R-H": ns["r_H"]}
pred = ns["predict"]

worst = 0.0
SEAL = {"ratios": {"E": {"1.41933": rE(1.41933), "1.997": rE(1.997)}, "E-CCBH": {"1.41933": rEC(1.41933), "1.997": rEC(1.997)}},
        "GS4_24110": {}, "U4_27928": {}}
P("\nGS4_24110 (z 1.997, R 7.39 kpc, V_c 206): required log M_gas (Rg = Rd), canon / alt")
for lm in (10.89, 10.76):
    pr = pred(7.39, 206.0, 1.997, 10 ** lm, 7.39 / 1.678)
    for m in ("F-flat", "F-DESI", "R-H"):
        for fn in ns["FOOT"]:
            worst = max(worst, abs(pr[(fn, m)]["logVbar2R_G"] - stored[str(lm)][f"{fn}|{m}"]["logVbar2R_G"]))
    SEAL["GS4_24110"][str(lm)] = {f"{a}|{b}": d for (a, b), d in pr.items()}
    P(f"  logM* {lm}: " + "; ".join(f"{m} {ns['fmt'](pr[('canon 9.36e-11', m)]['logMgas_Rg=Rd'])}/{ns['fmt'](pr[('alt 1.13e-10', m)]['logMgas_Rg=Rd'])}" for m in ns["MODELS"]))
check("K2 F-flat / F-DESI / R-H reproduce CFG571's stored GS4_24110 logMbar,req", worst <= 1e-3, f"max |d| {worst:.1e} dex")
z = 1.41933
from scipy.integrate import quad
dc = 2.99792458e5 / 70.0 * quad(lambda x: 1 / math.sqrt(0.3 * (1 + x) ** 3 + 0.7), 0, z)[0] * 1e3
Re = 0.49 / 206264.806 * dc / (1 + z)
P(f"\nU4_27928 (z {z}, R = 2 Re = {2 * Re:.2f} kpc): required log M_gas canon/alt by V_c")
for Vc in (150, 175, 200, 225, 250, 275, 300):
    pr = pred(2 * Re, float(Vc), z, 10 ** 10.74, Re / 1.678)
    SEAL["U4_27928"][str(Vc)] = {f"{a}|{b}": d for (a, b), d in pr.items()}
    P(f"  V_c {Vc}: " + "; ".join(f"{m} {ns['fmt'](pr[('canon 9.36e-11', m)]['logMgas_Rg=Rd'])}/{ns['fmt'](pr[('alt 1.13e-10', m)]['logMgas_Rg=Rd'])}" for m in ns["MODELS"]))

blob = json.dumps(SEAL, sort_keys=True, default=str).encode()
sha = hashlib.sha256(blob).hexdigest()
open(os.path.join(HERE, "SEALED_EVENT_HORIZON.json"), "wb").write(blob)
P(f"\nSEALED_EVENT_HORIZON.json sha256 = {sha}")
P("FAILS: " + (str(FAILS) if FAILS else "none"))
open(os.path.join(HERE, "cfg778.out"), "w").write("\n".join(OUT) + "\n")
sys.exit(1 if FAILS else 0)
