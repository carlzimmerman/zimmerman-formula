#!/usr/bin/env python3
"""HS1 POST-RESULT, reported only: could the zooms' own scatter in S at fixed mass supply the tilt if S ranked with surface brightness? And does the tilt survive on gas-dominated galaxies, where Upsilon hardly matters?
    python3 hs1_scatter.py   kappa = 1/2 FITTED; footings never pooled; not theory closed."""
import json, math, os, sys
FHERE2 = os.path.dirname(os.path.abspath(__file__)); _T = open(os.path.join(FHERE2, "hs1_slope.py")).read(); __file__ = os.path.join(FHERE2, "hs1_slope.py"); exec(compile(_T[:_T.index('Pn(f"HS1: slope')], "hs1_head", "exec"))
HERE = FHERE2; OUTL.clear(); TA = "A_c2b_refit"; I5 = iu_of(0.50); QS = sel(60, 120); bg = BGS[TA]; rc = 3 * (100 * bg["h"] * 1e3 / MPCE) ** 2 / (8 * math.pi * GE)
XJ = json.load(open(os.path.join(FRB, "X77_direct_core_surface_density", "x77_results.json")))["summary"]; SC = {k: float(np.std(np.log10(XJ[k]["per_seed"]), ddof=1)) for k in ("1e+12_ng64", "1e+13_ng48", "1e+14_ng48")}
Pn("HS1 scatter, POST-RESULT, reported only; kappa = 1/2 FITTED; footings never pooled; not theory closed"); Pn("zooms' scatter of lg eta at fixed mass (X77, per seed): " + ", ".join(f"{k} {v:.3f} dex (n {len(XJ[k]['per_seed'])})" for k, v in SC.items())); SIGN = SC["1e+12_ng64"]
def row(gf, qs): 
    X, Y = [], []
    for q in qs:
        d = delta(q, gf, I5, 2.0)
        if d is None or SB.get(q["name"], 0) <= 0: continue
        X.append(math.log10(SB[q["name"]])); Y.append(d)
    X, Y = np.array(X), np.array(Y); return slope(X, Y), boot(X, Y, 4000), float(Y.mean()), float(np.sqrt(np.mean(Y ** 2))), len(X), float(X.std(ddof=1))
LB = {q["name"]: math.log10(SB[q["name"]]) for q in QS if SB.get(q["name"], 0) > 0}; mu_, sd_ = float(np.mean(list(LB.values()))), float(np.std(list(LB.values()), ddof=1)); Pn(f"lg SBeff in the sample: mean {mu_:.2f}, sd {sd_:.2f} dex; to flatten +0.315 per dex needs sd(lg S) at rank correlation 1 of {0.315 * sd_:.3f} dex")
def m_rank(sig, r):
    C = {}
    def f(q, iu):
        if q["name"] not in C:
            M = 10 ** (bg["a"] + bg["b"] * (q["lMb"] - 10)); Mk = M * MSUNE; R200 = (3 * Mk / (4 * math.pi * 200 * rc)) ** (1 / 3); c = Srule(M, S1, TA) * 10 ** (sig * r * (LB.get(q["name"], mu_) - mu_) / sd_); r0 = solve_r0(Mk, R200, c); C[q["name"]] = GE * math.pi * c * r0 ** 2 * B(q["Rm"] / r0) / q["Rm"] ** 2
        return q["GB"][:, iu] + C[q["name"]]
    return f
Res = dict(scatter=SC, sb_sd=sd_)
for sig, r in ((SIGN, 0.5), (SIGN, 1.0), (2 * SIGN, 1.0)):
    b, s, m, rm, n, _ = row(m_rank(sig, r), QS); Pn(f"  N1 with lg S shifted by {sig:.3f} dex x r {r:.1f} x z(lg SBeff): slope {b:+.4f} +- {s:.4f} ({b / s:+.2f} sigma), mean delta {m:+.3f}, rms {rm:.3f}, n {n}"); Res[f"rank_{sig:.3f}_{r}"] = dict(b=b, s=s, mean=m, rms=rm)
for lab, f_ in (("gas-dominated (1.33 M_HI > 0.5 L36)", lambda q: 1.33 * q["meta"]["MHI"] > 0.5 * q["meta"]["L36"]), ("star-dominated", lambda q: 1.33 * q["meta"]["MHI"] <= 0.5 * q["meta"]["L36"])):
    K = [q for q in QS if f_(q)]; o = {}
    for nm, gf in (("N1", m_route(S1, TA)), ("F", m_route(0.0, TA, SIG["canonical"])), ("law", m_law("canonical"))):
        b, s, m, rm, n, sx = row(gf, K); o[nm] = dict(b=b, s=s, mean=m, rms=rm, n=n, sx=sx); Pn(f"  {lab}, {nm}: n {n}, sd lg SBeff {sx:.2f}: slope {b:+.4f} +- {s:.4f} ({b / s:+.2f} sigma), mean delta {m:+.3f}, rms {rm:.3f}")
    Res[lab] = o
json.dump(Res, open(os.path.join(HERE, "hs1_scatter.json"), "w"), indent=1, default=float); open(os.path.join(HERE, "hs1_scatter.out"), "w").write("\n".join(OUTL) + "\n")
