#!/usr/bin/env python3
"""NZ1 reported line 2: SPARC by V_flat under r0 from the zooms (collapse branch; floor keeps its budget r0), against FC1's table. LS1's and FC1's machinery; canonical and alt.
    python3 nz1_bins.py   kappa = 1/2 FITTED; footings never pooled; not theory closed."""
import json, math, os, sys
FHERE = os.path.dirname(os.path.abspath(__file__)); FRB = os.path.dirname(FHERE)
CE = json.load(open(os.path.join(FRB, "CE1_converged_eta_grade", "ce1_results.json")))["eta"]; ETAV = [CE[str(e)]["med"] for e in (12, 13, 14)]
FC = (lambda om, ob: (om - ob) / om)(0.2976016, 0.0223081 / 0.6856427 ** 2)
LSD = os.path.join(FRB, "LS1_lstar_analogs"); S = open(os.path.join(LSD, "ls1_analogs.py")).read(); __file__ = os.path.join(LSD, "ls1_analogs.py")
exec(compile(S[:S.index('P("LS1 SPARC')], "ls1_head", "exec")); HERE = FHERE
assert abs(float(B(1.0)) - 0.69707) < 1e-4
from scipy.optimize import brentq as _bq
def M200(q, tag=TAG): b = BGS[tag]; return 10 ** (b["a"] + b["b"] * (q["lMb"] - 10))
def eta_conv(M): return float(np.interp(math.log10(M), [12, 13, 14], ETAV))
def gh(q, f, zoom=True):
    bg = BGS[TAG]; rc = 3 * (100 * bg["h"] * 1e3 / MPCE) ** 2 / (8 * math.pi * GE); M = M200(q); R200 = (3 * M * MSUNE / (4 * math.pi * 200 * rc)) ** (1 / 3); Mt = M / FC
    e = eta_conv(Mt); Sc = sigma_coll(TAG, Mt)[0]; sc = FC * e * Sc * MSUNE / PC2; s = max(SIG[f], sc)
    if zoom and sc > SIG[f]: a = _bq(lambda a_: 4 / 3 * a_ * a_ / float(B(a_)) - e, 1.01, 1e4, xtol=1e-12); r0 = math.sqrt(3 * (Mt / 2) / (4 * math.pi * Sc)) * 3.0857e16 / a
    else: r0 = solve_r0(M * MSUNE, R200, s)
    return GE * math.pi * s * r0 ** 2 * B(q["Rm"] / r0) / q["Rm"] ** 2
BINS = ((20, 60), (60, 100), (100, 150), (150, 200), (200, 250), (250, 400)); FJ = json.load(open(os.path.join(FRB, "FC1_cold_share_native_eta", "fc1_ls1.json"))); R = {}; OUT = []
def PR(s): print(s, flush=True); OUT.append(s)
PR(f"NZ1 SPARC by V_flat, f_c {FC:.5f}; eta table {ETAV}; dV at Upsilon 0.50, 2-4 R_d; FC1 in brackets; kappa = 1/2 FITTED; not theory closed")
for f in ("canonical", "alt"):
    R[f] = {}
    for lo, hi in BINS:
        qs = sel(lo, hi); U, D, N = [], [], 0
        for q in qs:
            g_ = gh(q, f); _, _, iu = fit_one(q, np.log10(np.maximum(q["GB"] + g_[:, None], 1e-300))); U.append(UPS[iu]); d = dv(q, g_)
            if d is not None: D.append(d)
        k = f"{lo}-{hi}"; c = FJ[f][k]; R[f][k] = dict(n=len(qs), U=float(np.median(U)), dV=float(np.median(D)), U_FC1=c["U"], dV_FC1=c["dV"])
        PR(f"  {f} {k}: n {len(qs)} U {np.median(U):.2f} ({c['U']:.2f}) dV {np.median(D):+.1f} ({c['dV']:+.1f})")
d = max(abs(float(np.median([dv(q, gh(q, 'canonical', zoom=False)) for q in sel(250, 400) if dv(q, gh(q, 'canonical', zoom=False)) is not None])) - FJ["canonical"]["250-400"]["dV"]), 0.0)
PR(f"K budget r0 reproduces FC1's 250-400 dV: |d| {d:.1e}: {'PASS' if d <= 1e-6 else 'FAIL'}")
json.dump(R, open(os.path.join(FHERE, "nz1_bins.json"), "w"), indent=1); open(os.path.join(FHERE, "nz1_bins.out"), "w").write("\n".join(OUT) + "\n"); sys.exit(0 if d <= 1e-6 else 1)
