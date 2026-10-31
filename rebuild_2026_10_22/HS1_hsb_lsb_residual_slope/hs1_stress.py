#!/usr/bin/env python3
"""HS1 POST-RESULT, reported only: is the tilt real? Partial regressions at fixed V_flat and mass, narrower bins, other surface densities, stricter samples, outliers, free Upsilon per galaxy, contraction, and the S each galaxy would need.
    python3 hs1_stress.py   kappa = 1/2 FITTED; footings never pooled; not theory closed."""
import json, math, os, sys
FHERE2 = os.path.dirname(os.path.abspath(__file__)); _T = open(os.path.join(FHERE2, "hs1_slope.py")).read(); __file__ = os.path.join(FHERE2, "hs1_slope.py"); exec(compile(_T[:_T.index('Pn(f"HS1: slope')], "hs1_head", "exec"))
HERE = FHERE2; OUTL.clear(); X39S = open(os.path.join(FRB, "X39_baryonic_contraction", "x39_contraction.py")).read(); SGN = 1
exec(compile(X39S[X39S.index("def contract(r, Mb, M0, F, gnedin=None):"):X39S.index('P("\\n=== checks")')], "x39_contract", "exec"))
from scipy.stats import spearmanr
TA = "A_c2b_refit"; SD = {}; RE = {}
for l in open(MRT):
    p = l.split()
    if len(p) < 18: continue
    try: SD[p[0]] = float(p[12]); RE[p[0]] = float(p[9])
    except ValueError: pass
GF = dict(N1=m_route(S1, TA), F=m_route(0.0, TA, SIG["canonical"]), law=m_law("canonical")); I5 = iu_of(0.50); QS = sel(60, 120)
def arrays(gf, qs=QS, iu=I5, fac=2.0):
    R = []
    for q in qs:
        d = delta(q, gf, iu, fac)
        if d is None or SB.get(q["name"], 0) <= 0: continue
        t = TAB[q["name"]]; R.append(dict(name=q["name"], d=d, sb=math.log10(SB[q["name"]]), sd=math.log10(max(SD.get(q["name"], 0), 1e-3)), vf=math.log10(t["vf"]), mb=q["lMb"], rd=math.log10(t["rd"]), inc=t["inc"], Q=t["Q"]))
    return R
def fit2(R, *ks):
    y = np.array([r["d"] for r in R]); X = np.column_stack([np.ones(len(R))] + [[r[k] for r in R] for k in ks]); c = np.linalg.lstsq(X, y, rcond=None)[0]; rng = np.random.default_rng(1); B_ = []
    for _ in range(4000):
        k = rng.integers(0, len(R), len(R)); B_.append(np.linalg.lstsq(X[k], y[k], rcond=None)[0][1])
    return float(c[1]), float((np.percentile(B_, 84) - np.percentile(B_, 16)) / 2)
Pn("HS1 stress, POST-RESULT, reported only; kappa = 1/2 FITTED; footings never pooled; not theory closed")
Res = {}
for nm in ("N1", "F", "law"):
    R = arrays(GF[nm]); o = {}; Pn(f"{nm}: delta at 2 R_d, Upsilon 0.50, n {len(R)}")
    for lab, ks in (("lg SBeff", ("sb",)), ("lg SBeff at fixed lg V_flat", ("sb", "vf")), ("lg SBeff at fixed lg M_b", ("sb", "mb")), ("lg SBdisk", ("sd",)), ("lg SBdisk at fixed lg V_flat", ("sd", "vf"))):
        b, s = fit2(R, *ks); o[lab] = (b, s); Pn(f"  slope on {lab}: {b:+.4f} +- {s:.4f} ({b / s:+.2f} sigma)")
    for lab, f_ in (("V_flat 60-90", lambda r: r["vf"] < math.log10(90)), ("V_flat 90-120", lambda r: r["vf"] >= math.log10(90)), ("Q = 1", lambda r: r["Q"] == 1), ("Inc 45-80", lambda r: 45 <= r["inc"] <= 80)):
        K = [r for r in R if f_(r)]; b, s = fit2(K, "sb"); rho = spearmanr([r["sb"] for r in K], [r["d"] for r in K]); o[lab] = (b, s, len(K)); Pn(f"  {lab}, n {len(K)}: {b:+.4f} +- {s:.4f} ({b / s:+.2f} sigma), Spearman {rho[0]:+.3f}, p {rho[1]:.1e}")
    Ks = sorted(R, key=lambda r: abs(r["d"]))[:-5]; b, s = fit2(Ks, "sb"); Pn(f"  dropping the 5 largest |delta|: {b:+.4f} +- {s:.4f} ({b / s:+.2f} sigma)"); o["drop5"] = (b, s)
    lb = [float(np.polyfit([r["sb"] for j, r in enumerate(R) if j != i], [r["d"] for j, r in enumerate(R) if j != i], 1)[0]) for i in range(len(R))]; Pn(f"  leave one out: slope from {min(lb):+.4f} to {max(lb):+.4f}"); Res[nm] = o
# free Upsilon per galaxy
Pn("Free Upsilon per galaxy (the SPARC line's own fit): how does the fitted Upsilon run with lg SBeff, and what tilt is left?")
for nm in ("N1", "F", "law"):
    U_, X_, D_, W_ = [], [], [], []
    for q in QS:
        if SB.get(q["name"], 0) <= 0: continue
        if nm == "law": g = m_law("canonical"); LG = np.log10(np.maximum(np.column_stack([g(q, i) for i in range(len(UPS))]), 1e-300))
        else: gh_ = gh_S(q, S1 if nm == "N1" else 0.0, TA, None if nm == "N1" else SIG["canonical"]); LG = np.log10(np.maximum(q["GB"] + gh_[:, None], 1e-300))
        w, s_, iu = fit_one(q, LG); d = delta(q, GF[nm], iu, 2.0)
        if d is None: continue
        U_.append(float(UPS[iu])); X_.append(math.log10(SB[q["name"]])); D_.append(d)
    U_, X_, D_ = np.array(U_), np.array(X_), np.array(D_); p = spearmanr(X_, U_); edge = float(np.mean((U_ <= 0.301) | (U_ >= 1.199))); bu = float(np.polyfit(X_, np.log10(U_), 1)[0]); Pn(f"  {nm}: median Upsilon {np.median(U_):.2f}; d lg Upsilon / d lg SBeff {bu:+.3f} per dex (Upsilon x {10 ** bu:.2f} per dex), Spearman {p[0]:+.3f}, p {p[1]:.1e}; at the grid's edge {edge:.0%}; tilt left at each galaxy's best Upsilon {float(np.polyfit(X_, D_, 1)[0]):+.4f}, rms {float(np.sqrt(np.mean(D_ ** 2))):.3f}"); Res[f"freeU_{nm}"] = dict(bu=bu, rho=p[0], p=p[1], medU=float(np.median(U_)), edge=edge)
# contraction at N1's S, Upsilon 0.50, strength f
bg = BGS[TA]; rc = 3 * (100 * bg["h"] * 1e3 / MPCE) ** 2 / (8 * math.pi * GE)
def gh_con(q, f_):
    M = 10 ** (bg["a"] + bg["b"] * (q["lMb"] - 10)); Mk = M * MSUNE; R200 = (3 * Mk / (4 * math.pi * 200 * rc)) ** (1 / 3); c = Srule(M, S1, TA); r0 = solve_r0(Mk, R200, c); Rm = q["Rm"]; rg = np.geomspace(Rm[0] * 0.05, R200, 300); M0 = math.pi * c * r0 ** 2 * B(rg / r0); U = 0.50
    Mbk = np.maximum.accumulate(np.maximum(q["GB"][:, I5] * Rm ** 2 / GE, 0.0)); Mtot = max(float(Mbk[-1]), (U * q["meta"]["L36"] + 1.33 * q["meta"]["MHI"]) * 1e9 * MSUNE); Mbg = np.where(rg < Rm[0], Mbk[0] * (rg / Rm[0]) ** 2, np.interp(np.log(rg), np.log(Rm), Mbk)); o_ = rg > Rm[-1]
    if o_.any(): t_ = np.clip(np.log(rg[o_] / Rm[-1]) / math.log(3.0), 0, 1); Mbg[o_] = np.exp(np.log(max(Mbk[-1], 1e-300)) * (1 - t_) + np.log(Mtot) * t_)
    Mbg = np.maximum.accumulate(Mbg); Mf, _, _ = contract(rg, Mbg, M0, Mtot / Mk); Mu = M0 + f_ * (Mf - M0); return GE * np.interp(np.log(Rm), np.log(rg), Mu) / Rm ** 2
Pn("N1 with Blumenthal at strength f (Mu = M0 + f (Mf - M0)), Upsilon 0.50: does a baryon-driven response remove the tilt?")
for f_ in (0.0, 0.25, 0.5, 0.75, 1.0):
    C_ = {}
    def gf(q, iu):
        if q["name"] not in C_: C_[q["name"]] = gh_con(q, f_)
        return q["GB"][:, iu] + C_[q["name"]]
    R = arrays(gf); b, s = fit2(R, "sb"); d = np.array([r["d"] for r in R]); Pn(f"  f {f_:.2f}: slope {b:+.4f} +- {s:.4f} ({b / s:+.2f} sigma); mean delta {d.mean():+.3f}, rms {float(np.sqrt(np.mean(d ** 2))):.3f}"); Res[f"contract_{f_}"] = dict(b=b, s=s, mean=float(d.mean()), rms=float(np.sqrt(np.mean(d ** 2))))
# the S each galaxy needs at 2 R_d
Pn("The S each galaxy needs to match V_obs at 2 R_d, Upsilon 0.50, same M200 and R200:")
rows = []; none = 0
for q in QS:
    t = TAB[q["name"]]; Rk = q["Rm"] / KPC; ok = q["OK"][:, I5]; R2 = 2 * t["rd"]
    if SB.get(q["name"], 0) <= 0 or ok.sum() < 2 or not (Rk[ok].min() <= R2 <= Rk[ok].max()): continue
    Rm_ = R2 * KPC; V2 = float(np.interp(math.log(R2), np.log(Rk[ok]), q["Vobs"][ok])) * 1e3; gb = float(np.interp(math.log(R2), np.log(Rk[ok]), q["GB"][ok, I5])); Mn = (V2 ** 2 / Rm_ - gb) * Rm_ ** 2 / GE
    if Mn <= 0: none += 1; continue
    M = 10 ** (bg["a"] + bg["b"] * (q["lMb"] - 10)); Mk = M * MSUNE; R200 = (3 * Mk / (4 * math.pi * 200 * rc)) ** (1 / 3); un = MSUNE / PC2; f = lambda S_: math.pi * S_ * solve_r0(Mk, R200, S_) ** 2 * float(B(Rm_ / solve_r0(Mk, R200, S_))) - Mn; lo, hi = 1.0 * un, 5000.0 * un
    if f(lo) > 0 or f(hi) < 0: rows.append((math.log10(SB[q["name"]]), None, Srule(M, S1, TA) / un)); continue
    for _ in range(50):
        mid = math.sqrt(lo * hi); (lo, hi) = (mid, hi) if f(mid) < 0 else (lo, mid)
    rows.append((math.log10(SB[q["name"]]), math.log10(lo / un), Srule(M, S1, TA) / un))
G = [r for r in rows if r[1] is not None]; x_, y_ = np.array([r[0] for r in G]), np.array([r[1] for r in G]); b_ = float(np.polyfit(x_, y_, 1)[0]); P_ = spearmanr(x_, y_); rng = np.random.default_rng(1); bb = [float(np.polyfit(x_[k], y_[k], 1)[0]) for k in (rng.integers(0, len(x_), len(x_)) for _ in range(4000))]; Pn(f"  solved {len(G)}, off the 1-5000 range {len(rows) - len(G)}, baryons alone already enough {none}; d lg S_need / d lg SBeff {b_:+.3f} +- {(np.percentile(bb, 84) - np.percentile(bb, 16)) / 2:.3f} per dex, Spearman {P_[0]:+.3f}, p {P_[1]:.1e}; S_need median {10 ** np.median(y_):.0f}, 16-84 % {10 ** np.percentile(y_, 16):.0f}-{10 ** np.percentile(y_, 84):.0f} Msun/pc^2; rule N1 median {np.median([r[2] for r in G]):.0f}; scatter of lg S_need {y_.std():.2f} dex")
Res["S_need"] = dict(n=len(G), slope=b_, rho=P_[0], p=P_[1], scatter=float(y_.std()), med=float(10 ** np.median(y_)))
json.dump(Res, open(os.path.join(HERE, "hs1_stress.json"), "w"), indent=1, default=float); open(os.path.join(HERE, "hs1_stress.out"), "w").write("\n".join(OUTL) + "\n")
