"""p16: WHY do gas-dominated and star-dominated SPARC galaxies want different a0?  (diagnostic, not a derivation)

Lane V (agents/V_evidence_for_the_coefficient, v02 section S) found late types (T >= 8) prefer a lower a0 than early types
(T <= 5): ratio 1.46 in the cleanest published-style fit, 2.3 with Upsilon free, for every interpolating function. The July note
(real_research/papers/WHICH_A0_POPULATION_SPLIT_2026.md) found ~1.8 by gas fraction. Neither tested a cause. This script does.

Baseline (lane V's cleanest): RAR IF, Upsilon_disk fixed 0.5 (bulge 0.7), Q <= 2, i >= 30 deg, sigma_int 0.11 dex, profile in a0.
Each diagnostic changes ONE thing and reports a0(gas class), a0(star class) and their ratio. A cause 'closes' the split if the ratio
falls inside 1 +- its 2-sigma statistical error (independent-points errors, which understate the true error; stated, not hidden).

  D0 baseline, two class definitions (Hubble type; gas fraction at the last point)
  D1 same-regime comparison: only points in a common g_bar window (low, mid) -- does the split survive at matched acceleration?
  D2 pressure support: V_c^2 = V_obs^2 + sigma^2 R/R_g (exponential gas disc, R_g = R_HI/3.5), sigma = 6 / 8 / 10 km/s
  D3 distances: only TRGB / Cepheid (f_D = 2, 3) galaxies
  D4 inclination >= 50 deg
  D5 outer half of each curve only (beam smearing, inner non-circular motions)
  D6 Upsilon needed: star-class a0 at Upsilon_disk 0.5-0.9 (what Upsilon makes it agree with the gas class?)
  D7 gas needed: gas-class a0 with gas mass x 0.6-1.4 (what gas scale makes it agree with the star class?)

Run: python3 p16_gas_star_split_cause.py   |  MUTATE=1: class labels shuffled (seeded); the split must vanish and check A must fail
"""
import math, os, sys
import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "agents", "V_evidence_for_the_coefficient"))
import v_common as V

MUTATE = os.environ.get("MUTATE") == "1"
res = []
def check(n, ok): res.append(bool(ok)); print(("PASS  " if ok else "FAIL  ") + n)

# R_HI from the SPARC table (column 15), for the pressure-support correction
RHI = {}
for ln in open(os.path.join(V.DATA, "SPARC_Lelli2016c.mrt")):
    p = ln.split()
    if len(p) >= 18 and p[1].lstrip("-").isdigit() and p[4].isdigit():
        try: RHI[p[0]] = float(p[14])
        except ValueError: pass

gals = [g for g in V.load_sparc() if g["Q"] is not None and g["Q"] <= 2 and g["inc"] >= 30]
for g in gals:                                   # gas fraction at the last point, Upsilon 0.5/0.7
    vb2 = g["Vgas"][-1] ** 2 + 0.5 * g["Vdisk"][-1] ** 2 + 0.7 * g["Vbul"][-1] ** 2
    g["fgas"] = g["Vgas"][-1] ** 2 / vb2 if vb2 > 0 else np.nan
if MUTATE:
    rng = np.random.default_rng(16)
    T = rng.permutation([g["T"] for g in gals]); F = rng.permutation([g["fgas"] for g in gals])
    for g, t, f in zip(gals, T, F): g["T"], g["fgas"] = int(t), float(f)
GAS = lambda g: g["T"] >= 8
STAR = lambda g: g["T"] <= 5
A0S = np.exp(np.linspace(math.log(0.3e-10), math.log(3.0e-10), 91))
SIG = 0.11

def fit(gs, ufixed=0.5):
    if len(gs) < 4: return (np.nan, np.nan, len(gs))
    a, s = V.parabola_min(A0S, V.Profile(gs, V.IF_rar, ufixed=ufixed).scan(A0S, SIG), k=8)
    return a, s, len(gs)

def split(name, gs_gas, gs_star, ug=0.5, us=0.5):
    a1, s1, n1 = fit(gs_gas, ug); a2, s2, n2 = fit(gs_star, us)
    r = a2 / a1; sr = math.hypot(s1, s2)
    closed = abs(math.log(r)) < 2 * sr
    print(f"  {name:46s} gas {a1*1e10:6.3f} (n {n1:3d})  star {a2*1e10:6.3f} (n {n2:3d})  ratio {r:5.2f} +- {sr*r:4.2f}  {'CLOSES' if closed else 'stays'}")
    return dict(gas=a1, star=a2, ratio=r, sig_ln=sr, closed=closed)

def sub(g, m):                                   # keep only points where mask m is True
    h = dict(g)
    for k in ("Rm", "Vobs", "eV", "Vgas", "Vdisk", "Vbul"): h[k] = g[k][m]
    return h

def gbar05(g):
    return (np.sign(g["Vgas"]) * g["Vgas"] ** 2 + 0.5 * g["Vdisk"] ** 2 + 0.7 * g["Vbul"] ** 2) * 1e6 / g["Rm"]

print(f"sample: {len(gals)} galaxies (Q<=2, i>=30); gas class T>=8: {sum(map(GAS, gals))}; star class T<=5: {sum(map(STAR, gals))}" + ("   *** MUTATE: labels shuffled ***" if MUTATE else ""))
out = {}
print("\nD0 baseline")
out["D0"] = split("Hubble type (T>=8 vs T<=5)", [g for g in gals if GAS(g)], [g for g in gals if STAR(g)])
out["D0f"] = split("gas fraction at last point (>0.5 vs <0.3)", [g for g in gals if g["fgas"] > 0.5], [g for g in gals if g["fgas"] < 0.3])

print("\nD1 matched acceleration window (only points with g_bar inside it, Upsilon 0.5)")
for lab, lo, hi in (("low  g_bar 1e-12..2e-11", 1e-12, 2e-11), ("mid  g_bar 2e-11..1e-10", 2e-11, 1e-10)):
    win = lambda g: sub(g, (gbar05(g) > lo) & (gbar05(g) < hi))
    gg = [w for w in (win(g) for g in gals if GAS(g)) if len(w["Rm"]) >= 2]
    ss = [w for w in (win(g) for g in gals if STAR(g)) if len(w["Rm"]) >= 2]
    out["D1 " + lab[:3].strip()] = split(lab, gg, ss)

print("\nD2 pressure support (asymmetric drift), all galaxies corrected")
for sig in (6.0, 8.0, 10.0):
    def ad(g, s=sig):
        h = dict(g); Rg = max(RHI.get(g["name"], 0) / 3.5, 0.5) * V.kpc
        h["Vobs"] = np.sqrt(g["Vobs"] ** 2 + s ** 2 * g["Rm"] / Rg); return h
    out[f"D2 {sig:.0f}"] = split(f"sigma_HI = {sig:.0f} km/s", [ad(g) for g in gals if GAS(g)], [ad(g) for g in gals if STAR(g)])

print("\nD3-D5 data-quality cuts")
out["D3"] = split("TRGB/Cepheid distances only (f_D 2,3)", [g for g in gals if GAS(g) and g["fD"] in (2, 3)], [g for g in gals if STAR(g) and g["fD"] in (2, 3)])
out["D4"] = split("inclination >= 50 deg", [g for g in gals if GAS(g) and g["inc"] >= 50], [g for g in gals if STAR(g) and g["inc"] >= 50])
outer = lambda g: sub(g, np.arange(len(g["Rm"])) >= len(g["Rm"]) // 2)
out["D5"] = split("outer half of each curve", [outer(g) for g in gals if GAS(g)], [outer(g) for g in gals if STAR(g)])

print("\nD6 Upsilon the star class would need (gas class fixed at 0.5)")
d6 = {}
for u in (0.5, 0.6, 0.7, 0.8, 0.9):
    d6[u] = split(f"star Upsilon_disk = {u}", [g for g in gals if GAS(g)], [g for g in gals if STAR(g)], 0.5, u)
print("\nD7 gas mass the gas class would need (star class at Upsilon 0.5)")
d7 = {}
for e in (0.6, 0.8, 1.0, 1.2, 1.4):
    d7[e] = split(f"gas mass x {e}", [V.transform(g, gas_scale=e) for g in gals if GAS(g)], [g for g in gals if STAR(g)])

print()
D0 = out["D0"]
check(f"A the split is real in this sample: star/gas a0 ratio {D0['ratio']:.2f}, more than 2 sigma from 1 (both class definitions)",
      not D0["closed"] and D0["ratio"] > 1 and not out["D0f"]["closed"] and out["D0f"]["ratio"] > 1)
closers = [k for k in ("D1 low", "D1 mid", "D2 6", "D2 8", "D2 10", "D3", "D4", "D5") if out[k]["closed"]]
print(f"   single-cause diagnostics that close it: {closers or 'none'}")
u_close = [u for u, d in d6.items() if d["closed"]]
e_close = [e for e, d in d7.items() if d["closed"]]
print(f"   Upsilon_disk values (star class) that close it: {u_close}; gas scales (gas class) that close it: {e_close}")
check("B the record's 'Upsilon uplift' reading: some star-class Upsilon in 0.6-0.9 closes the split", len([u for u in u_close if u >= 0.6]) > 0)
check("C a gas-mass rescaling alone needs > 20% (no factor in 0.8-1.2 except 1.0 closes it)", not any(d7[e]["closed"] for e in (0.8, 1.2)))
print(f"\n{sum(res)}/{len(res)} pass" + ("  (MUTATE)" if MUTATE else ""))
sys.exit(0 if all(res) else 1)
