#!/usr/bin/env python3
"""CN1 frozen output 1: median Upsilon and dV by V_flat with Blumenthal contraction on collapse-branch galaxies, at R = 1 and down the R grid. kappa = 1/2 FITTED; footings never pooled; not theory closed."""
import json, math, os, sys
FH = os.path.dirname(os.path.abspath(__file__)); FR = os.path.dirname(FH)
LSD = os.path.join(FR, "LS1_lstar_analogs"); S = open(os.path.join(LSD, "ls1_analogs.py")).read(); __file__ = os.path.join(LSD, "ls1_analogs.py")
exec(compile(S[:S.index('P("LS1 SPARC')], "ls1_head", "exec")); HERE = FH
X39S = open(os.path.join(FR, "X39_baryonic_contraction", "x39_contraction.py")).read(); SGN = 1
exec(compile(X39S[X39S.index("def contract(r, Mb, M0, F, gnedin=None):"):X39S.index('P("\\n=== checks")')], "x39_contract", "exec"))
CE = json.load(open(os.path.join(FR, "CE1_converged_eta_grade", "ce1_results.json")))["eta"]; ETAV = [CE[str(e)]["med"] for e in (12, 13, 14)]; FC = (lambda om, ob: (om - ob) / om)(0.2976016, 0.0223081 / 0.6856427 ** 2)
bg = BGS[TAG]; rc = 3 * (100 * bg["h"] * 1e3 / MPCE) ** 2 / (8 * math.pi * GE)
def gh_of(q, foot, R_):
    M2 = 10 ** (bg["a"] + bg["b"] * (q["lMb"] - 10)); Mt = M2 / FC; sc = FC * float(np.interp(math.log10(Mt), [12, 13, 14], ETAV)) * sigma_coll(TAG, Mt)[0] * MSUNE / PC2; Mk = M2 * MSUNE; R200 = (3 * Mk / (4 * math.pi * 200 * rc)) ** (1 / 3); Rm = q["Rm"]
    if sc <= SIG[foot]:
        s = SIG[foot]; r0 = solve_r0(Mk, R200, s); return np.tile((GE * math.pi * s * r0 ** 2 * B(Rm / r0) / Rm ** 2)[:, None], (1, len(UPS))), False
    si = R_ * sc; r0 = solve_r0(Mk, R200, si); rg = np.geomspace(Rm[0] * 0.05, R200, 300); M0 = math.pi * si * r0 ** 2 * B(rg / r0); gh = np.zeros((len(Rm), len(UPS)))
    for iu, U in enumerate(UPS):
        Mbk = np.maximum.accumulate(np.maximum(q["GB"][:, iu] * Rm ** 2 / GE, 0.0)); Mtot = max(float(Mbk[-1]), (U * q["meta"]["L36"] + 1.33 * q["meta"]["MHI"]) * 1e9 * MSUNE)
        Mbg = np.where(rg < Rm[0], Mbk[0] * (rg / Rm[0]) ** 2, np.interp(np.log(rg), np.log(Rm), Mbk)); o_ = rg > Rm[-1]
        if o_.any():
            t_ = np.clip(np.log(rg[o_] / Rm[-1]) / math.log(3.0), 0, 1); Mbg[o_] = np.exp(np.log(max(Mbk[-1], 1e-300)) * (1 - t_) + np.log(Mtot) * t_)
        Mbg = np.maximum.accumulate(Mbg); Mf, _, _ = contract(rg, Mbg, M0, Mtot / Mk); gh[:, iu] = GE * np.interp(np.log(Rm), np.log(rg), Mf) / Rm ** 2
    return gh, True
BINS = ((20, 60), (60, 100), (100, 150), (150, 200), (200, 250), (250, 400)); R = {}
print("CN1 by V_flat: median Upsilon / dV at Upsilon 0.50 (2-4 R_d), Blumenthal on collapse-branch galaxies; kappa = 1/2 FITTED; not theory closed")
for foot in ("canonical", "alt"):
    R[foot] = {}
    for R_ in (1.0, 0.8, 0.6, 0.4, 0.3):
        row = {}
        for lo, hi in BINS:
            U, D, na = [], [], 0
            for q in sel(lo, hi):
                gh, ac = gh_of(q, foot, R_); na += ac; _, _, iu = fit_one(q, np.log10(np.maximum(q["GB"] + gh, 1e-300))); U.append(UPS[iu]); d = dv(q, gh[:, I05])
                if d is not None: D.append(d)
            row[f"{lo}-{hi}"] = dict(n=len(U), active=na, U=float(np.median(U)), dV=float(np.median(D)))
        R[foot][f"{R_:.1f}"] = row
        print(f"  [{foot}] R {R_:.1f}: " + "; ".join(f"{k} {v['U']:.2f}/{v['dV']:+.1f}" for k, v in row.items()), flush=True)
json.dump(R, open(os.path.join(FH, "cn1_bins.json"), "w"), indent=1); open(os.path.join(FH, "cn1_bins.out"), "w").write(json.dumps(R, indent=0))
