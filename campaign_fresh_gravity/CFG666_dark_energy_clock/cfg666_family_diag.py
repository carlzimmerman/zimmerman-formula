#!/usr/bin/env python3
"""CFG666 post-hoc diagnostic (no verdict weight): for which true scale a_true = kappa_true c sqrt(G rho_DE) would the clock's
uniform-dilution shape pass the frozen gates, and what settling time would a cosmic-rate clock (rate H_Lambda) then need?"""
import os, sys, io, json, math, contextlib
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); LANES = os.path.dirname(HERE); sys.path.insert(0, LANES)
with contextlib.redirect_stdout(io.StringIO()):
    import CFG4_common as C4, CFG7_common as C7
    g4, _ = C4.exec_slices(os.path.join(LANES, "CFG4_galaxy_law.py"), [(None, 'banner("K  CONTROLS')], name="cfg4_galaxy_ro")
C = 2.99792458e8; G = 6.67430e-11; MPC = 3.0857e22; GYR = 3.15576e16
H0 = 67.4e3 / MPC; OL = 0.685; HL = H0 * math.sqrt(OL); RHO = 3 * H0 ** 2 * OL / (8 * math.pi * G)
T_UNIV = 13.8
iu = int(np.argmin(np.abs(g4["UPS"] - 0.61)))
gb, go, ok, ww = g4["GB"][:, iu], g4["GO"][:, iu], g4["OK"][:, iu], g4["WW"][:, iu]
m = ok & (gb > 0); gb, go, w = gb[m], go[m], ww[m]
nu = lambda y: np.asarray(C7.nu_mono(np.asarray(y, float)), float)
def st(pred):
    r = np.log10(go) - np.log10(pred); return float(np.sqrt(np.sum(w * r * r) / w.sum())), float(np.sum(w * r) / w.sum())
out = {}
for foot in ("canonical", "alt"):
    a0 = C7.A0_SI[foot]; rl, _ = st(nu(gb / a0) * gb); keff = a0 / (C * math.sqrt(G * RHO))
    rows = []
    for ratio in np.geomspace(1.0001, 6.0, 40):          # a_true / a0_eff
        at = ratio * a0; f = math.sqrt(1 / ratio)
        rc, bc = st((1 + f * (nu(gb / at) - 1)) * gb)
        ok_ = (rc - rl <= 0.01) and abs(bc) <= 0.03
        tb = -math.log(1 - f) / HL / GYR if f < 1 else float("inf")
        rows.append(dict(ratio=float(ratio), kappa_true=float(keff * ratio), f=f, d_rms=rc - rl, bias=bc, shape_ok=bool(ok_), t_b_Gyr=tb))
    okr = [r for r in rows if r["shape_ok"]]
    mx = max(okr, key=lambda r: r["ratio"]) if okr else None
    out[foot] = dict(rows=rows, max_allowed=mx)
    print(f"[{foot}] law rms {rl:.4f}; shape passes the frozen gates up to a_true/a0 = {mx['ratio']:.3f} (kappa_true {mx['kappa_true']:.3f}, "
          f"f {mx['f']:.3f}); a cosmic-rate clock would then need t_b = {mx['t_b_Gyr']:.1f} Gyr (universe {T_UNIV} Gyr)" if mx else f"[{foot}] no ratio passes")
    for r in rows[::6]:
        print(f"   a_true/a0 {r['ratio']:.3f}: d_rms {r['d_rms']:+.4f} bias {r['bias']:+.4f} pass {r['shape_ok']}  t_b {r['t_b_Gyr']:.1f} Gyr")
json.dump(out, open(os.path.join(HERE, "cfg666_family_diag.json"), "w"), indent=1)
