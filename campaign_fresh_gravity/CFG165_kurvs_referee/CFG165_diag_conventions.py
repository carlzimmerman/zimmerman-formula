#!/usr/bin/env python3
"""CFG165 POST-COMPARISON diagnostic (written AFTER opening CFG140/141/160 source; NOT part of the frozen main): isolate which of my
declared conventions produces the residual 0.003 dex offset to CFG160.  Labelled: two conventions swapped one at a time and together.
ZF_REPO=<repo> python3 CFG165_diag_conventions.py > CFG165_diag_conventions.out"""
import sys, math
sys.dont_write_bytecode = True
import numpy as np
import CFG165_referee_kurvs_p4 as M
P = lambda *a: print(*a, flush=True)
AS = M.load_sparc_anchor()
targets = {"P4 primary": (0.1441, -0.0060, 0.0439, 0.0443), "alpha x0.6": (0.0580, -0.0917, 0.0446, 0.0459),
           "alpha x1.4": (0.2107, 0.0601, 0.0456, 0.0454), "Re=2Reff": (0.0662, -0.0837, 0.0459, 0.0470)}
kw = {"P4 primary": {}, "alpha x0.6": dict(scale=0.6), "alpha x1.4": dict(scale=1.4), "Re=2Reff": dict(Refac=2.0, Refac_anchor=2.0)}


def cell_own(S, sp, mu):
    po = M.per_object(S, sp, mu, 0.0, "canonical")
    out = {}
    for law in ("flat", "H"):
        m, e, _ = M.pool(po["d_" + law], po["e_" + law])
        pa = M.per_object(AS, sp, None, 0.0, "canonical", anchor=True)
        am, ae, _ = M.pool(pa["d_" + law], pa["e_" + law])          # the anchor pooled with the SAME law's own weights
        out[law] = (m - am, math.hypot(e, ae))
    return out


for label, col, own in (("mine (inc_sfr, flat anchor for both)", "inc_sfr_deg", False), ("inc_star only", "inc_star_deg", False),
                        ("own-law anchor only", "inc_sfr_deg", True), ("inc_star + own-law anchor", "inc_star_deg", True)):
    S = M.load_kurvs(inc_col=col)
    P(f"\n{label}")
    for nm, k in kw.items():
        sp = M.spec("P4", **k)
        if own:
            r = cell_own(S, sp, 0.67)
            f, h = r["flat"], r["H"]
            df, sf, dh, sh = f[0], f[1], h[0], h[1]
        else:
            c = M.cell(S, AS, sp, 0.67, 0.0, "canonical")
            df, sf, dh, sh = c["flat"]["dprime"], c["flat"]["sigma"], c["H"]["dprime"], c["H"]["sigma"]
        t = targets[nm]
        P(f"  {nm:12s} flat {df:+.4f}+-{sf:.4f} (CFG160 {t[0]:+.4f}+-{t[2]:.4f}; diff {df-t[0]:+.4f})   rival {dh:+.4f}+-{sh:.4f} (CFG160 {t[1]:+.4f}+-{t[3]:.4f}; diff {dh-t[1]:+.4f})")

# ---- counts and the full sensitivity table with the inclination column that CFG140 uses (inc_star_deg)
S = M.load_kurvs(inc_col="inc_star_deg")
P("\nWith inc_star_deg (CFG140's column): ladder, sensitivity rows, grid counts")
for nm in ("P0", "P1", "P2", "P3", "P4"):
    c = M.cell(S, AS, M.SP[nm], 0.67, 0.0, "canonical")
    P(f"  {nm}: flat {c['flat']['dprime']:+.3f}+-{c['flat']['sigma']:.3f} ({c['flat']['z']:+.2f}s) rival {c['H']['dprime']:+.3f}+-{c['H']['sigma']:.3f} ({c['H']['z']:+.2f}s)")
for mu in M.MUS:
    c = M.cell(S, AS, M.SP["P4"], mu, 0.0, "canonical")
    P(f"  mu={mu}: flat {c['flat']['dprime']:+.3f}+-{c['flat']['sigma']:.3f} ({c['flat']['z']:+.2f}s) rival {c['H']['dprime']:+.3f}+-{c['H']['sigma']:.3f} ({c['H']['z']:+.2f}s)")
for name, sp in (("P4", M.SP["P4"]), ("x0.6", M.spec("P4", scale=0.6)), ("x1.4", M.spec("P4", scale=1.4)), ("Re2", M.spec("P4", Refac=2.0, Refac_anchor=2.0)), ("P2", M.SP["P2"]), ("P3", M.SP["P3"])):
    cn = {"flat": [0, 0, 0], "H": [0, 0, 0]}
    for mu in M.MUS:
        for dl in M.DELS:
            for ft in M.FOOTS:
                c = M.cell(S, AS, sp, mu, dl, ft)
                for law in ("flat", "H"):
                    z = c[law]["z"]
                    cn[law][0 if z > 2 else (2 if z < -2 else 1)] += 1
    P(f"  {name:5s} counts [>+2s, within, <-2s]: flat {cn['flat']}  rival {cn['H']}")
c = M.cell(S, AS, M.SP["P4"], 0.67, 0.0, "canonical")
po = c["po"]
P("  per galaxy Dflat P4: " + ", ".join(f"{n_}:{d:+.2f}" for n_, d in zip(S.name, po["d_flat"])))
