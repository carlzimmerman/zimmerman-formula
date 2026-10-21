#!/usr/bin/env python3
"""AG4e: seal the frozen S2 action's own n=1 (simple) law's ALMA gas predictions (GS4_24110, U4_27928) before 11-06 / 11-28.
AG4d's method: CFG571's head executed read-only (as CFG778 does) with the kernel swapped to nu1 = (1 + sqrt(1 + 4/y))/2.
Criteria: FROZEN_CRITERIA.md (committed alone, before this script).  No gate (owner's direct go).
Run: python3 ag4e.py      AG4E_MUTATE=1: kernel nu = 1, F-DESI vs R-H must collapse (exit 1 = bites); nothing sealed.
kappa = 1/2 fitted; footings never pooled; cold-energy mass required; not theory closed."""
import hashlib, json, math, os, sys
import numpy as np
from scipy.integrate import quad

HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
CFGD = os.path.join(REPO, "campaign_fresh_gravity"); ARG = os.path.join(REPO, "argon_push")
MUT = os.environ.get("AG4E_MUTATE") == "1"; TAG = "_MUTATE" if MUT else ""
OUT = []
def P(s=""):
    print(s, flush=True); OUT.append(str(s))
FAILS = []
def check(name, ok, d=""):
    P(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f": {d}" if d else "")); (None if ok else FAILS.append(name)); return ok
def finish(code):
    open(os.path.join(HERE, f"ag4e{TAG}.out"), "w").write("\n".join(OUT) + "\n"); sys.exit(code)

P("AG4e: n=1 (simple) ALMA gas predictions (CFG571 code path, kernel nu1 = (1 + sqrt(1 + 4/y))/2)" + ("   *** MUTATE: nu = 1 ***" if MUT else ""))
P("kappa = 1/2 fitted; footings never pooled; cold-energy mass required; not theory closed.")

# ---- CFG571 head, read-only (as CFG778)
P571 = os.path.join(CFGD, "CFG571_prereg_proprietary_alma", "cfg571_prereg.py")
head = open(P571).read().split("# ---- controls ----")[0]
ns = {"__file__": P571, "__name__": "cfg571_import"}
argv0 = sys.argv; sys.argv = [argv0[0]]; exec(compile(head, "cfg571_head", "exec"), ns); sys.argv = argv0
NU_MONO = ns["NU"]
stored571 = json.load(open(os.path.join(CFGD, "CFG571_prereg_proprietary_alma", "cfg571_prereg_results.json")))["results"]
seal778 = json.load(open(os.path.join(CFGD, "CFG778_sealed_event_horizon_branch", "SEALED_EVENT_HORIZON.json")))
bh = json.load(open(os.path.join(CFGD, "CFG775_bh_horizon_dark_energy", "cfg775_results.json")))["numbers"]["B2"]["8.0"]["r_BH"]
r_bh = lambda z: float(np.interp(z, [float(k) for k in bh], list(bh.values())))
ZK = {1.41933: "1.41933", 1.997: "1.997"}
def tab(name):
    def f(z):
        k = min(ZK, key=lambda q: abs(q - z)); assert abs(k - z) < 1e-6, z
        return float(seal778["ratios"][name][ZK[k]])
    return f
ns["MODELS"] = {"E": tab("E"), "E-CCBH": tab("E-CCBH"), "F-flat": lambda z: 1.0, "F-DESI": ns["r_desi"], "BH-k3": r_bh, "R-H": ns["r_H"],
                "L-fb(RAR-eq)": ns["r_fb"]}
z4 = 1.41933
dc = 2.99792458e5 / 70.0 * quad(lambda x: 1 / math.sqrt(0.3 * (1 + x) ** 3 + 0.7), 0, z4)[0] * 1e3; Re = 0.49 / 206264.806 * dc / (1 + z4)
VCS = (150, 175, 200, 225, 250, 275, 300)


def grid(nu):
    ns["NU"] = nu; out = {"GS4_24110": {}, "U4_27928": {}}
    for lm in (10.89, 10.76):
        pr = ns["predict"](7.39, 206.0, 1.997, 10 ** lm, 7.39 / 1.678); out["GS4_24110"][str(lm)] = {f"{a}|{b}": d for (a, b), d in pr.items()}
    for Vc in VCS:
        pr = ns["predict"](2 * Re, float(Vc), z4, 10 ** 10.74, Re / 1.678); out["U4_27928"][str(Vc)] = {f"{a}|{b}": d for (a, b), d in pr.items()}
    return out


NU1 = lambda y: 0.5 * (1 + np.sqrt(1 + 4 / np.asarray(y, float)))
NU2 = lambda y: np.sqrt(1 + 1 / np.asarray(y, float))
NEWT = lambda y: np.ones_like(np.asarray(y, float))

# ---- controls
P("\nControls")
gm = grid(NU_MONO); worst = 0.0; n_cmp = 0
for tgt, keys in (("GS4_24110", ("10.89", "10.76")), ("U4_27928", tuple(str(v) for v in VCS))):
    for k in keys:
        for key, d in gm[tgt][k].items():
            m = key.split("|", 1)[1]
            for ref in ((stored571[tgt][k] if m in ("F-DESI", "F-flat", "R-H", "L-fb(RAR-eq)") else None),
                        (seal778[tgt][k] if m in ("E", "E-CCBH", "F-flat", "F-DESI", "BH-k3", "R-H") else None)):
                if ref is not None and key in ref:
                    worst = max(worst, abs(d["logVbar2R_G"] - ref[key]["logVbar2R_G"])); n_cmp += 1
check("K1 nu_mono reproduces CFG571 + CFG778 sealed logMbar,req", worst <= 1e-9 and n_cmp > 0, f"max |d| {worst:.1e} dex over {n_cmp} entries")
y = np.logspace(-6, 4, 401); g1k = NU1(y) * y
check("K2 nu1: g^2/(g+1) = y to 1e-12; nu1(1e-4) = 100.50125", np.max(np.abs(g1k ** 2 / (g1k + 1) - y) / y) < 1e-12 and abs(float(NU1(1e-4)) - 100.50125) < 1e-5)

if MUT:
    gn = grid(NEWT)
    col = all(abs(gn["GS4_24110"][lm][f"{fn}|R-H"]["logVbar2R_G"] - gn["GS4_24110"][lm][f"{fn}|F-DESI"]["logVbar2R_G"]) < 0.01
              for lm in ("10.89", "10.76") for fn in ns["FOOT"])
    P(f"MUTATE (nu = 1): F-DESI vs R-H separation collapses -> {'control BITES (exit 1, nothing sealed)' if col else 'DID NOT BITE (recorded)'}")
    finish(1 if col else 0)
if FAILS:
    P("controls failed; nothing sealed"); finish(1)

g1 = grid(NU1); g2 = grid(NU2)
rep = json.load(open(os.path.join(ARG, "AG4d_n2_alma_seal", "ag4d_results.json")))["n1_simple_reported"]
k3 = max(abs(g1[t][k][key]["logVbar2R_G"] - rep[t][k][key]["logVbar2R_G"]) for t in g1 for k in g1[t] for key in g1[t][k])
check("K3 nu1 grid equals AG4d's reported n=1 grid", k3 == 0.0, f"max |d| {k3:.1e}")
if FAILS:
    P("controls failed; nothing sealed"); finish(1)
fmt = ns["fmt"]; BR = list(ns["MODELS"])
P("\nGS4_24110 (z 1.997, R 7.39 kpc, V_c 206): required total log M_gas, Rg = Rd (Rg = 1.5Rd), canon / alt")
for lm in ("10.89", "10.76"):
    P(f"  log M* {lm}:")
    for m in BR:
        c = lambda gg, fn, s: fmt(gg["GS4_24110"][lm][f"{fn}|{m}"][f"logMgas_{s}"])
        P(f"    {m:13s} n=1 {c(g1, 'canon 9.36e-11', 'Rg=Rd')}({c(g1, 'canon 9.36e-11', 'Rg=1.5Rd')}) / {c(g1, 'alt 1.13e-10', 'Rg=Rd')}({c(g1, 'alt 1.13e-10', 'Rg=1.5Rd')})"
          f"   | sealed nu_mono {c(gm, 'canon 9.36e-11', 'Rg=Rd')} / {c(gm, 'alt 1.13e-10', 'Rg=Rd')}   | sealed n=2 (AG4d) {c(g2, 'canon 9.36e-11', 'Rg=Rd')} / {c(g2, 'alt 1.13e-10', 'Rg=Rd')}")
P(f"\nU4_27928 (z {z4}, R = 2 Re = {2 * Re:.2f} kpc, log M* 10.74): n=1 required total log M_gas (Rg = Rd), canon/alt, by V_c")
for Vc in VCS:
    P(f"  V_c {Vc}: " + "; ".join(f"{m} {fmt(g1['U4_27928'][str(Vc)][f'canon 9.36e-11|{m}']['logMgas_Rg=Rd'])}/{fmt(g1['U4_27928'][str(Vc)][f'alt 1.13e-10|{m}']['logMgas_Rg=Rd'])}" for m in BR))

SEAL = {"law": "n=1 simple (frozen S2 rest state), g_N = g^2/(g + a0), nu1 = (1 + sqrt(1 + 4/y))/2", "code": "CFG571 head (read-only) with NU = nu1",
        "ratios": {m: {"1.41933": ns["MODELS"][m](1.41933), "1.997": ns["MODELS"][m](1.997)} for m in BR},
        "GS4_24110": g1["GS4_24110"], "U4_27928": g1["U4_27928"]}
blob = json.dumps(SEAL, sort_keys=True, default=str).encode(); sha = hashlib.sha256(blob).hexdigest()
open(os.path.join(HERE, "SEALED_N1.json"), "wb").write(blob)
open(os.path.join(HERE, "PREDICTIONS_HASH.txt"), "w").write(f"{sha}  SEALED_N1.json\n")
json.dump({"nu_mono": gm, "n1_sealed": g1, "n2_sealed_AG4d": g2, "sha256": sha}, open(os.path.join(HERE, "ag4e_results.json"), "w"), indent=1, default=str)
P(f"\nSEALED_N1.json sha256 = {sha}")
P("FAILS: none")
finish(0)
