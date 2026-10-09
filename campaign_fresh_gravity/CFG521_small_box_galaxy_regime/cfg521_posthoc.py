#!/usr/bin/env python3
"""CFG521 post-hoc (NOT gating; added after the frozen verdict, 2026-10-09):
(1) P/P_S0 vs k at z = 0 out to k = 8 for every box, incl. CFG518's L = 200 runs vs CFG359 S0 (beyond CFG518's k <= 1 cut);
(2) z-growth of the high-k deficit (L = 50 DC-can); (3) L = 50 DC-can z = 0 catchment-mass breakdown by f_ret class, recomputed
from the saved z = 0 positions with the engine's own in_cover (checks the engine diagnostic)."""
import os, sys, json, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); EXT = os.path.abspath(os.path.join(HERE, "..", "..", "..", "_external_data"))
W = os.path.join(EXT, "cfg521_work"); L_ = []
def P(s=""): print(s); L_.append(s)
ld = lambda p: json.load(open(p))
KS = (0.5, 1, 1.5, 2, 3, 4, 6, 8)
def curve(a, b, n="z0"):
    s, s0 = a["snap"][n], b["snap"][n]; k = np.array(s["k"]); r = np.array(s["P"]) / np.interp(k, s0["k"], s0["P"])
    return " ".join(f"{k[np.argmin(abs(k - x))]:.2f}:{r[np.argmin(abs(k - x))]:.3f}" for x in KS if x <= k.max() * 1.01)
P("(1) P/P_S0 at z = 0 (k h/Mpc : ratio)")
S0_200 = ld(os.path.join(EXT, "cfg359_work", "cfg359_S0_FLAT_canonical_N256.json"))
for nm, f in (("L200 census can (CFG518)", "cfg518_RES_TA_MIXA_MASSCONS_fretcensus_FLAT_canonical_N256.json"),
              ("L200 K1 f_ret=1 (CFG518)", "cfg518_RES_TA_MIXA_MASSCONS_fretone_FLAT_canonical_N256.json"),
              ("L200 MUTATE (CFG518)", "cfg518_RES_TA_NOCOMP_MIXA_MASSCONS_fretcensus_FLAT_canonical_N256.json")):
    P(f"  {nm:28s} {curve(ld(os.path.join(EXT, 'cfg518_work', f)), S0_200)}")
for Lb in (100, 50, 25):
    s0 = ld(os.path.join(W, f"cfg521_S0_TA_MIXA_MASSCONS_fretcensus_FLAT_canonical_N256_L{Lb}.json"))
    for nm, t in (("census can", "_MIXA_MASSCONS_fretcensus_FLAT_canonical"), ("census alt", "_MIXA_MASSCONS_fretcensus_FLAT_alt"),
                  ("K1 f_ret=1", "_MIXA_MASSCONS_fretone_FLAT_canonical"), ("MUTATE", "_NOCOMP_MIXA_MASSCONS_fretcensus_FLAT_canonical")):
        p = os.path.join(W, f"cfg521_RES_TA{t}_N256_L{Lb}.json")
        if os.path.exists(p): P(f"  L{Lb} {nm:23s} {curve(ld(p), s0)}")
P("\n(2) L50 census can, P/P_S0 by snapshot")
a = ld(os.path.join(W, "cfg521_RES_TA_MIXA_MASSCONS_fretcensus_FLAT_canonical_N256_L50.json"))
s0 = ld(os.path.join(W, "cfg521_S0_TA_MIXA_MASSCONS_fretcensus_FLAT_canonical_N256_L50.json"))
for n in ("z1", "z0.5", "z0"): P(f"  {n:5s} {curve(a, s0, n)}")
os.environ.update(CFG521_L="50", CFG521_RMIN=str(2 * 50 / 256), CFG521_THREADS="2"); sys.path.insert(0, HERE)
import cfg521_pm as E
d = np.load(os.path.join(W, "cfg521_RES_TA_MIXA_MASSCONS_fretcensus_FLAT_canonical_N256_L50_z0.npz"))
m = E.Mesh(256); delta = m.deposit(d["pos"].astype(np.float64)); D = E.dta_table()["D"][0]
cm, ff = E.in_cover(m, delta, D, 1.0, 1.0, "FLAT", "canonical", want_fret=True)
rho = 1 + delta; c = rho * cm
P(f"\n(3) L50 census can z = 0: catchments hold {c.sum() / rho.sum():.3f} of box mass in {cm.mean():.3f} of the volume")
for lo, hi in ((0, 0.2), (0.2, 0.55), (0.55, 1.01)):
    s = (ff >= lo) & (ff < hi) & cm; P(f"  f_ret in [{lo:.2f}, {hi:.2f}): {(rho * s).sum() / c.sum():.3f} of catchment mass")
P(f"  catchment mass-weighted mean f_ret {(ff * c).sum() / c.sum():.3f} (engine diagnostic: {a['snap']['z0']['fret_mass_mean_catch']:.3f})")
open(os.path.join(HERE, "cfg521_posthoc.out"), "w").write("\n".join(L_) + "\n")
