#!/usr/bin/env python3
"""LS1 POST-RESULT, reported only: the a0 law on the same statistics, and Upsilon / dV by V_flat at c_f 4 and at CE1's converged eta(M).
kappa = 1/2 FITTED; footings never pooled; not theory closed."""
import sys, json, math, os
S = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "ls1_analogs.py")).read()
exec(compile(S[:S.index('P("LS1 SPARC')], "ls1_head", "exec"))
EMNS = NS
LAW = EMNS["LAW"]; A0 = EMNS["A0"]
print("LAW type", type(LAW), "A0", A0)
CE = dict(zip((12., 13., 14.), (25.94, 17.67, 16.91)))
def M200(q, tag=TAG): b = BGS[tag]; return 10 ** (b["a"] + b["b"] * (q["lMb"] - 10))
def halo_eta(q, f, eta, tag=TAG):
    bg = BGS[tag]; rc = 3 * (100 * bg["h"] * 1e3 / MPCE) ** 2 / (8 * math.pi * GE); M = M200(q)
    R200 = (3 * M * MSUNE / (4 * math.pi * 200 * rc)) ** (1 / 3); s = max(SIG[f], eta * sigma_coll(tag, M)[0] * MSUNE / PC2)
    r0 = solve_r0(M * MSUNE, R200, s); return GE * math.pi * s * r0 ** 2 * B(q["Rm"] / r0) / q["Rm"] ** 2
def eta_ce(q): return float(np.interp(math.log10(M200(q)), [12, 13, 14], [25.94, 17.67, 16.91]))
def ev(gh_fn):
    out = {}
    for lo, hi in ((20, 60), (60, 100), (100, 150), (150, 200), (200, 250), (250, 400)):
        U, D = [], []
        for q in sel(lo, hi):
            gh = gh_fn(q); _, _, iu = fit_one(q, np.log10(np.maximum(q["GB"] + gh[:, None], 1e-300))); U.append(UPS[iu]); d = dv(q, gh)
            if d is not None: D.append(d)
        out[f"{lo}-{hi}"] = (len(U), round(float(np.median(U)), 2), round(float(np.median(D)), 1))
    return out
R = {}
for f in ("canonical", "alt"):
    R[f] = dict(c4=ev(lambda q: halo_eta(q, f, eta_of(4.0))), converged=ev(lambda q: halo_eta(q, f, eta_ce(q))))
    a0 = A0[f]
    def lawgh(q):
        gb = q["GB"][:, I05]; y = gb / a0; nu = 0.5 + np.sqrt(0.25 + 1 / np.maximum(y, 1e-30)); return gb * (nu - 1)
    # the law's boost depends on Upsilon, so fit with the full grid
    def ev_law():
        out = {}
        for lo, hi in ((20, 60), (60, 100), (100, 150), (150, 200), (200, 250), (250, 400)):
            U, D = [], []
            for q in sel(lo, hi):
                G = q["GB"]; y = G / a0; g = G * (0.5 + np.sqrt(0.25 + 1 / np.maximum(y, 1e-30)))
                _, _, iu = fit_one(q, np.log10(np.maximum(g, 1e-300))); U.append(UPS[iu]); d = dv(q, lawgh(q))
                if d is not None: D.append(d)
            out[f"{lo}-{hi}"] = (len(U), round(float(np.median(U)), 2), round(float(np.median(D)), 1))
        return out
    R[f]["law_simple_nu"] = ev_law()
    print(f); [print(" ", k, v) for k, v in R[f].items()]
json.dump(R, open(os.path.join(HERE, "ls1_posthoc.json"), "w"), indent=1)
