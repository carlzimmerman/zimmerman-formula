#!/usr/bin/env python3
"""CFG491 Step 1 -- the numbers behind the differentiator matrix that are computed here (not quoted from other lanes):
 (1) the lensing edge: framework r_edge = r_M / ln(1 + f_ret f_b/(1-f_b)) vs LCDM splashback vs MOND's EFE radius r_M/e;
 (2) a0(z) = kappa c sqrt(G rho_DE(z)) under the on-disk DESI DR2 w0wa chains vs flat (MOND) vs a0 ~ H(z);
 (3) the scaling exponents d log r / d log M_b that separate the three edge laws.
Inputs flagged (U) are recalled from the literature, not read from a file on disk. kappa = 1/2 FITTED; both footings."""
import os, sys, io, json, math, contextlib
import numpy as np
from scipy.optimize import brentq
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.dirname(HERE))
with contextlib.redirect_stdout(io.StringIO()):
    import CFG4_common as C
G, MSUN, KPC = 6.674e-11, 1.989e30, 3.0857e19
H, OM = 0.7, 0.315                                              # (U) Planck-like; LCDM comparator only
RHOC = 3 * (H * 100 * 1e3 / 3.0857e22) ** 2 / (8 * math.pi * G); RHOM = OM * RHOC
FB = 1.0 / (1.0 + 5.364)                                        # CFG462's f_b (Omega_c/Omega_b = 5.364)
A0 = C.A0
OUT, L = {}, []
def P(s=""): print(s); L.append(s)

def moster(lMh):
    Mh = 10 ** lMh; M1 = 10 ** 11.590
    return math.log10(2 * 0.0351 * Mh / ((Mh / M1) ** -1.376 + (Mh / M1) ** 0.608))
def inv_moster(lMs): return brentq(lambda x: moster(x) - lMs, 9.0, 15.5)

P("(1) LENSING EDGE: framework r_edge vs LCDM splashback vs MOND EFE radius (kpc)")
P(f"   f_b = {FB:.6f}; framework edge at f_ret = 1: {1/math.log(1/(1-FB)):.4f} r_M")
P("   LCDM: M_h = Moster+13^-1(M*), R200m with Omega_m 0.315 (U); R_sp/R200m = 0.54(1+0.53 Om)(1+1.36 exp(-Gamma/3.04)) (More+15, U), Gamma 0.5..3")
P("   MOND: no edge in isolation; QUMOND EFE turns the field Newtonian-like beyond r_EFE = r_M / e, e = 0.02..0.05 (Chae's field range; CFG8 median 0.043-0.049)")
rows = []
for lMs in (9.5, 10.0, 10.5, 11.0, 11.3):
    Mb = 10 ** lMs * (1.5 if lMs < 10.25 else 1.2)              # rough gas share: stated, not fitted
    lMh = inv_moster(lMs); Mh = 10 ** lMh
    R200m = (3 * Mh * MSUN / (4 * math.pi * 200 * RHOM)) ** (1 / 3) / KPC
    sp = [0.54 * (1 + 0.53 * OM) * (1 + 1.36 * math.exp(-g / 3.04)) * R200m for g in (3.0, 0.5)]
    fret_lcdm = Mb / (FB * Mh)                                  # the LCDM-equivalent retention (same total mass)
    for foot in ("canonical", "alt"):
        rM = math.sqrt(G * Mb * MSUN / A0[foot]) / KPC
        ed = {f: rM / math.log(1 + f * FB / (1 - FB)) for f in (1.0, 0.3, 0.1, 0.07)}
        ed_l = rM / math.log(1 + min(fret_lcdm, 1.0) * FB / (1 - FB))
        row = dict(lMs=lMs, lMb=math.log10(Mb), lMh=lMh, footing=foot, r_M=rM, edge=ed, edge_fret_lcdm=ed_l, fret_lcdm=fret_lcdm,
                   R200m=R200m, Rsp=sp, rEFE=[rM / 0.05, rM / 0.02])
        rows.append(row)
        P(f"   log M* {lMs:4.1f} [{foot:9s}] r_M {rM:6.1f} | edge f_ret=1 {ed[1.0]:6.0f}, 0.3 {ed[0.3]:6.0f}, 0.1 {ed[0.1]:6.0f}, 0.07 {ed[0.07]:6.0f};"
          f" at LCDM-equal retention {fret_lcdm:.3f}: {ed_l:6.0f} | LCDM log M_h {lMh:5.2f}, R200m {R200m:5.0f}, R_sp {sp[0]:4.0f}-{sp[1]:4.0f}"
          f" | MOND r_EFE {rM/0.05:5.0f}-{rM/0.02:5.0f}")
OUT["edge"] = rows
# scaling exponents between log M* 10.0 and 11.0
def pick(lMs, foot): return [r for r in rows if r["lMs"] == lMs and r["footing"] == foot][0]
for foot in ("canonical", "alt"):
    a, b = pick(10.0, foot), pick(11.0, foot); dl = b["lMb"] - a["lMb"]
    s_fw = math.log10(b["edge"][0.1] / a["edge"][0.1]) / dl
    s_fw_l = math.log10(b["edge_fret_lcdm"] / a["edge_fret_lcdm"]) / dl
    s_l = math.log10(b["R200m"] / a["R200m"]) / dl
    P(f"   [{foot}] d log r / d log M_b over log M* 10->11: framework (fixed f_ret) {s_fw:.2f}; framework with LCDM-equal retention {s_fw_l:.2f};"
      f" LCDM R200m/R_sp {s_l:.2f}; MOND r_EFE (fixed e) 0.50")
    OUT.setdefault("scaling", {})[foot] = dict(framework_fixed_fret=s_fw, framework_lcdm_retention=s_fw_l, lcdm=s_l, mond_fixed_e=0.5)

P("\n(2) a0(z): framework a0 ~ sqrt(rho_DE(z)) with the on-disk DESI DR2 w0wa chains (weighted medians of w0, wa); MOND flat; rival a0 ~ H(z)")
CH = os.path.abspath(os.path.join(HERE, "..", "..", "..", "_external_data", "desi_dr2_chains"))
def rde(z, w0, wa):
    a = 1 / (1 + z); return a ** (-3 * (1 + w0 + wa)) * np.exp(-3 * wa * (1 - a))
def Hz(z, w0, wa, om=OM): return np.sqrt(om * (1 + z) ** 3 + (1 - om) * rde(z, w0, wa))
OUT["a0z"] = {}
for nm in ("desy5", "pantheonplus", "union3"):
    p = os.path.join(CH, nm, "chain.1.txt")
    if not os.path.exists(p):
        P(f"   {nm}: chain not on disk"); continue
    hdr = open(p).readline().lstrip("#").split(); iw, i0, ia = hdr.index("weight"), hdr.index("w"), hdr.index("wa")
    x = np.vstack([np.loadtxt(os.path.join(CH, nm, f"chain.{k}.txt"))[:, [iw, i0, ia]] for k in range(1, 5)])
    x = x[int(0.3 * len(x)):]
    wt = x[:, 0]; o = np.argsort(x[:, 1]); w0 = x[o, 1][np.searchsorted(np.cumsum(wt[o]), 0.5 * wt.sum())]
    o = np.argsort(x[:, 2]); wa = x[o, 2][np.searchsorted(np.cumsum(wt[o]), 0.5 * wt.sum())]
    zs = np.array([0.5, 1.0, 1.5, 2.0, 2.5])
    ratio = np.sqrt(rde(zs, w0, wa))
    # posterior spread of log a0(z=2.5)/a0(0)
    sub = x[np.random.default_rng(1).choice(len(x), 4000, p=wt / wt.sum())]
    d25 = 0.5 * np.log10(rde(2.5, sub[:, 1], sub[:, 2]))
    OUT["a0z"][nm] = dict(w0=float(w0), wa=float(wa), z=zs.tolist(), dlog_a0=np.log10(ratio).tolist(),
                          dlog_a0_z25_16_84=[float(np.percentile(d25, 16)), float(np.percentile(d25, 84))],
                          dlog_H_z25=float(np.log10(Hz(2.5, -1, 0))))
    P(f"   DESI+CMB+{nm:12s}: w0 {w0:+.3f}, wa {wa:+.3f} -> d log a0 at z = 0.5/1/1.5/2/2.5: "
      + " ".join(f"{v:+.3f}" for v in np.log10(ratio)) + f" dex (z 2.5 68%: {np.percentile(d25,16):+.3f}..{np.percentile(d25,84):+.3f});"
      f" rival a0 ~ H(z) at z 2.5: {np.log10(Hz(2.5, -1, 0)):+.3f} dex; MOND 0")
P("   calibration wall at z 2-2.5 (PAPER38/CFG213-229): >= 0.3 dex per galaxy; the DE-tracking shift is ~0.1 dex or less.")
json.dump(OUT, open(os.path.join(HERE, "cfg491_matrix_numbers_results.json"), "w"), indent=1, default=float)
open(os.path.join(HERE, "cfg491_matrix_numbers.out"), "w").write("\n".join(L) + "\n")
