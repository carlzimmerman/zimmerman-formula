#!/usr/bin/env python3
"""CFG374 analysis: frozen decision (CFG361 cuts) per T and footing, plus POST-FREEZE combined scorecard rows (labelled, not scored):
(i) CMB-lensing proxy: P ratio at k = 0.05-0.2 h/Mpc at z = 1 and 0.5 (upper bound on A_lens - 1; higher z contributes ~1);
(ii) KiDS isolated-lens effect of the reservoir compensation: fractional change of enclosed lensing mass at r = 0.1, 0.3, 1, 3 Mpc for
     lenses with M_b = 1e10.5 / 1e11 Msun (excess = phantom inside 0.4 r_ta minus the local cold share, smeared over a Gaussian R_c = 3 Mpc/h).
S0 = CFG359 256^3 JSON read-only.  Frozen: FROZEN_CRITERIA.md (396ed0c5a)."""
import os, json, math
import numpy as np
from scipy.special import erf
HERE = os.path.dirname(os.path.abspath(__file__)); W = os.path.abspath(os.path.join(HERE, "..", "..", "..", "_external_data", "cfg374_work"))
W9 = os.path.abspath(os.path.join(HERE, "..", "..", "..", "_external_data", "cfg359_work"))
LOG, OUT = [], {"lane": "CFG374", "frozen": "396ed0c5a", "runs": {}}
def P(s=""): print(s); LOG.append(s)
r0 = json.load(open(os.path.join(W9, "cfg359_S0_FLAT_canonical_N256.json")))["snap"]
def ratios(s, zn):
    k, p = np.array(s[zn]["k"]), np.array(s[zn]["P"]); k0, p0 = np.array(r0[zn]["k"]), np.array(r0[zn]["P"]); m = k <= 1
    pr = p[m] / np.interp(k[m], k0, p0)
    return dict(s8=s[zn]["sigma8"] / r0[zn]["sigma8"], pdev=float(np.max(np.abs(pr - 1))), P=[float(np.interp(x, k[m], pr)) for x in (0.1, 0.3, 1.0)],
                lens=float(np.mean(pr[(k[m] >= 0.05) & (k[m] <= 0.2)])))
def cat(r):
    ds = abs(r["s8"] - 1)
    if ds > 0.20: return "FAIL"
    if ds <= 0.05 and r["pdev"] <= 0.10: return "GROWTH OK"
    return "TENSION"
P("CFG374 -- RES R_c = 3 Mpc/h with the phantom sourced by pressure-filtered baryons; ratios to S0 (CFG359) at z = 0")
verd = {}
for T in ("MIXA", "MIXB"):
    for f in ("canonical", "alt"):
        p = os.path.join(W, f"cfg374_RES_Rc3_{T}_FLAT_{f}_N256.json")
        if not os.path.exists(p):
            P(f"  {T} {f}: MISSING"); continue
        s = json.load(open(p))["snap"]; z0 = ratios(s, "z0"); z1 = ratios(s, "z1"); zh = ratios(s, "z0.5")
        c = cat(z0); verd[(T, f)] = c
        OUT["runs"][f"{T}|{f}"] = dict(z0=z0, z05=zh, z1=z1, verdict=c, overdraw=s["z0"].get("overdraw_mass_frac"))
        P(f"  {T} K {f:9s}: s8 {z0['s8']:.4f}  max|P-1| k<=1 {z0['pdev']:.3f}  P@0.1/0.3/1 {z0['P'][0]:.3f}/{z0['P'][1]:.3f}/{z0['P'][2]:.3f}  "
          f"(z0.5 s8 {zh['s8']:.4f}, z1 {z1['s8']:.4f}) -> {c}")
for T, lab in (("MIXA", "LANE VERDICT (primary)"), ("MIXB", "conservative")):
    vs = [verd.get((T, f)) for f in ("canonical", "alt")]
    if None in vs: v = "INCOMPLETE"
    elif "FAIL" in vs: v = "FAIL"
    elif all(x == "GROWTH OK" for x in vs): v = "GROWTH OK"
    else: v = "TENSION"
    OUT[f"verdict_{T}"] = v; P(f"  {T}: {v}  [{lab}]")
P("  compare CFG372 single-phase: 1e6 K s8 1.009/1.011, P 7.6/8.9% (GROWTH OK); 1e4 K 1.029/1.035, P 24/30% (TENSION)")
P("  compare CFG366 R_c = 3 (no gas filter): s8 1.034 / 1.040, P(k=1) 1.29 / 1.35 (TENSION); CFG361 T5: 1.205 / 1.257 (FAIL)")

P("\nPOST-FREEZE combined scorecard (reported, not scored)")
for key, r in OUT["runs"].items():
    P(f"  (i) CMB-lensing proxy {key}: mean P ratio k 0.05-0.2: z1 {r['z1']['lens']:.3f}, z0.5 {r['z05']['lens']:.3f}, z0 {r['z0']['lens']:.3f}"
      f"  -> A_lens - 1 <~ {r['z05']['lens'] - 1:+.3f} (Planck/ACT allow a few %)")
# (ii) KiDS: reservoir compensation around an isolated lens
G = 4.30091e-9; H = 0.674; RC = 3.0 / H; A0 = {"canonical": 9.3603e-11, "alt": 1.1312e-10}
MPC = 3.0857e22; MSUN = 1.989e30
def nu(y): return 1.0 / (1.0 - np.exp(-np.sqrt(np.maximum(y, 1e-14))))
def frac_gauss(r):                                   # enclosed fraction of a 3D Gaussian of width RC
    x = r / (math.sqrt(2) * RC); return erf(x) - 2 * x * np.exp(-x * x) / math.sqrt(math.pi)
rho_m = 0.315 * 3 * (67.4 / 3.0857e19)**2 / (8 * math.pi * 6.674e-11) / MSUN * MPC**3
for foot, a0 in A0.items():
    for Mb in (10**10.5, 10**11):
        a0u = a0 * (3.15576e16 / 3.0857e19)**0 ; g = lambda r: G * Mb / r**2               # (km/s)^2/Mpc
        a0c = a0 / 1e3 * MPC / 1e3                                                         # a0 in (km/s)^2/Mpc
        r = np.geomspace(1e-3, 30, 4000); Mph = Mb * (nu(g(r) / a0c) - 1.0)
        # r_ta: mean enclosed (Mb + Mph) density = 11.8 rho_m (CFG354 K4 z = 0 value)
        rta = r[np.argmin(np.abs((Mb + Mph) / (4 / 3 * math.pi * r**3) - 11.806 * rho_m))]; rcut = 0.4 * rta
        Mex = max(float(np.interp(rcut, r, Mph)) - 5.364 * Mb, 0.0)
        row = []
        for R in (0.1, 0.3, 1.0, 3.0):
            Mlaw = Mb + float(np.interp(min(R, rcut), r, Mph)); dM = Mex * float(frac_gauss(R))
            row.append((R, -dM / Mlaw))
        OUT.setdefault("kids", {})[f"{foot}|{math.log10(Mb):.1f}"] = dict(r_ta=float(rta), M_excess=Mex, frac=row)
        P(f"  (ii) KiDS {foot:9s} M_b 1e{math.log10(Mb):.1f}: r_ta {rta:.2f} Mpc, excess {Mex:.2e} Msun; enclosed-mass change at r = "
          + ", ".join(f"{R:g} Mpc {x:+.2%}" for R, x in row))
P("  (iii) SPARC: the compensation inside 0.1 Mpc is the (ii) r = 0.1 row -- rotation curves are unchanged at that level.")
open(os.path.join(HERE, "cfg374_analysis.out"), "w").write("\n".join(LOG) + "\n")
json.dump(OUT, open(os.path.join(HERE, "cfg374_results.json"), "w"), indent=1)
