#!/usr/bin/env python3
"""CN1 POST-RESULT, reported only: virial energy to undo Blumenthal contraction in SPARC's collapse-branch galaxies at Upsilon 0.50, against each galaxy's supernova energy (BE1's budget).
kappa = 1/2 FITTED; footings never pooled; not theory closed."""
import json, math, os, sys
FH = os.path.dirname(os.path.abspath(__file__)); FR = os.path.dirname(FH)
LSD = os.path.join(FR, "LS1_lstar_analogs"); S = open(os.path.join(LSD, "ls1_analogs.py")).read(); __file__ = os.path.join(LSD, "ls1_analogs.py")
exec(compile(S[:S.index('P("LS1 SPARC')], "ls1_head", "exec")); HERE = FH
X39S = open(os.path.join(FR, "X39_baryonic_contraction", "x39_contraction.py")).read(); SGN = 1
exec(compile(X39S[X39S.index("def contract(r, Mb, M0, F, gnedin=None):"):X39S.index('P("\\n=== checks")')], "x39_contract", "exec"))
CE = json.load(open(os.path.join(FR, "CE1_converged_eta_grade", "ce1_results.json")))["eta"]; ETAV = [CE[str(e)]["med"] for e in (12, 13, 14)]; FC = (lambda om, ob: (om - ob) / om)(0.2976016, 0.0223081 / 0.6856427 ** 2)
ERG = 1e-7; R = {}
def W(rg, Mb, Mc):
    dM = np.diff(Mc); rm = 0.5 * (rg[1:] + rg[:-1]); return -GE * float(np.sum(0.5 * (Mb[1:] + Mb[:-1] + Mc[1:] + Mc[:-1]) * dM / rm))
print(f"CN1 energy to undo contraction, Upsilon 0.50, f_c {FC:.5f}; kappa = 1/2 FITTED; not theory closed")
for foot in ("canonical", "alt"):
    bg = BGS[TAG]; rc = 3 * (100 * bg["h"] * 1e3 / MPCE) ** 2 / (8 * math.pi * GE); rows = []
    for q in GALS:
        M2 = 10 ** (bg["a"] + bg["b"] * (q["lMb"] - 10)); Mt = M2 / FC; sc = FC * float(np.interp(math.log10(Mt), [12, 13, 14], ETAV)) * sigma_coll(TAG, Mt)[0] * MSUNE / PC2
        if sc <= SIG[foot]: continue
        Mk = M2 * MSUNE; R200 = (3 * Mk / (4 * math.pi * 200 * rc)) ** (1 / 3); r0 = solve_r0(Mk, R200, sc); Rm = q["Rm"]; rg = np.geomspace(Rm[0] * 0.05, R200, 600); M0 = math.pi * sc * r0 ** 2 * B(rg / r0)
        Mbk = np.maximum.accumulate(np.maximum(q["GB"][:, I05] * Rm ** 2 / GE, 0.0)); Mtot = max(float(Mbk[-1]), (0.5 * q["meta"]["L36"] + 1.33 * q["meta"]["MHI"]) * 1e9 * MSUNE)
        Mbg = np.where(rg < Rm[0], Mbk[0] * (rg / Rm[0]) ** 2, np.interp(np.log(rg), np.log(Rm), Mbk)); o_ = rg > Rm[-1]
        if o_.any():
            t_ = np.clip(np.log(rg[o_] / Rm[-1]) / math.log(3.0), 0, 1); Mbg[o_] = np.exp(np.log(max(Mbk[-1], 1e-300)) * (1 - t_) + np.log(Mtot) * t_)
        Mbg = np.maximum.accumulate(Mbg); Mf, _, _ = contract(rg, Mbg, M0, Mtot / Mk); Eq = max(0.0, (W(rg, Mbg, M0) - W(rg, Mbg, Mf)) / 2); Es = (0.5 * q["meta"]["L36"] * 1e9 / 100.0) * 1e51 * ERG; vf = TAB.get(q["name"], {}).get("vf", float("nan"))
        rows.append(dict(name=q["name"], vf=vf, lM200=math.log10(M2), eps=Eq / Es, Ereq_erg=Eq / ERG, Esn_erg=Es / ERG))
    e = np.array([r["eps"] for r in rows]); v = np.array([r["vf"] for r in rows]); out = dict(n=len(rows), median=float(np.median(e)), p16=float(np.percentile(e, 16)), p84=float(np.percentile(e, 84)), max=float(e.max()), frac_gt1=float(np.mean(e > 1)), bins={})
    print(f"  [{foot}] active {len(rows)}: eps median {out['median']:.3f} [{out['p16']:.3f}, {out['p84']:.3f}], max {out['max']:.3f}, frac > 1 {out['frac_gt1']:.2f}")
    for lo, hi in ((100, 150), (150, 200), (200, 250), (250, 400)):
        m = (v >= lo) & (v < hi)
        if m.sum(): out["bins"][f"{lo}-{hi}"] = dict(n=int(m.sum()), median=float(np.median(e[m]))); print(f"    V_flat {lo}-{hi}: n {int(m.sum())}, eps median {np.median(e[m]):.3f}")
    R[foot] = dict(out, rows=rows)
json.dump(R, open(os.path.join(FH, "cn1_energy.json"), "w"), indent=1, default=float)
