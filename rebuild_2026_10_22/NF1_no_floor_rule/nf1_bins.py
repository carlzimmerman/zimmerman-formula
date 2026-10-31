#!/usr/bin/env python3
"""NF1 reported: LS1's table by V_flat at Upsilon 0.50 with no floor, against ET1 and ET2's S; S_rule at lg M200 8-11. kappa = 1/2 FITTED; not theory closed."""
import json, math, os, sys
FHERE = os.path.dirname(os.path.abspath(__file__)); FRB = os.path.dirname(FHERE)
CE = json.load(open(os.path.join(FRB, "CE1_converged_eta_grade", "ce1_results.json")))["eta"]; ETAV = [CE[str(e)]["med"] for e in (12, 13, 14)]; FC = (lambda om, ob: (om - ob) / om)(0.2976016, 0.0223081 / 0.6856427 ** 2)
LSD = os.path.join(FRB, "LS1_lstar_analogs"); S = open(os.path.join(LSD, "ls1_analogs.py")).read(); __file__ = os.path.join(LSD, "ls1_analogs.py")
exec(compile(S[:S.index('P("LS1 SPARC')], "ls1_head", "exec")); HERE = FHERE
S1 = 1.25 * 0.5 * math.log10(8.05 / 5.72); S2 = 1.25 * math.log10(8.05 / 5.92); VAR = dict(N0=0.0, N1=S1, N2=S2)
def Srule(M, s): Mt = M / FC; return FC * float(np.interp(math.log10(Mt), [12, 13, 14], ETAV)) * 10 ** (s * max(0.0, 12 - math.log10(Mt))) * sigma_coll(TAG, Mt)[0] * MSUNE / PC2
def gh(q, s):
    bg = BGS[TAG]; rc = 3 * (100 * bg["h"] * 1e3 / MPCE) ** 2 / (8 * math.pi * GE); M = 10 ** (bg["a"] + bg["b"] * (q["lMb"] - 10)); R200 = (3 * M * MSUNE / (4 * math.pi * 200 * rc)) ** (1 / 3); c = Srule(M, s); r0 = solve_r0(M * MSUNE, R200, c); return GE * math.pi * c * r0 ** 2 * B(q["Rm"] / r0) / q["Rm"] ** 2
BINS = ((20, 60), (60, 100), (100, 150), (150, 200), (200, 250), (250, 400)); ET = json.load(open(os.path.join(FRB, "ET1_core_strength_needed", "et1_results.json")))["ups"]["0.50"]["bins"]; R = {}; OUT = []
def Pn(s): print(s, flush=True); OUT.append(s)
Pn(f"NF1 by V_flat, Upsilon 0.50; f_c {FC:.5f}; s N1 {S1:.4f} N2 {S2:.4f}; footings coincide with no floor; kappa = 1/2 FITTED; not theory closed")
ET2F = os.path.join(FRB, "ET2_free_core_low_mass", "et2_results.json"); ET2 = json.load(open(ET2F)) if os.path.exists(ET2F) else None
for nm, s in VAR.items():
    R[nm] = {}
    for lo, hi in BINS:
        qs = sel(lo, hi); U, D = [], []
        for q in qs:
            g = gh(q, s); _, _, iu = fit_one(q, np.log10(np.maximum(q["GB"] + g[:, None], 1e-300))); U.append(UPS[iu]); d = dv(q, g)
            if d is not None: D.append(d)
        k = f"{lo}-{hi}"; e = ET[k]; Sr = Srule(10 ** e["lgM"], s) / (MSUNE / PC2); ins = e["ci"][0] <= Sr <= e["ci"][1]; R[nm][k] = dict(n=len(qs), U=float(np.median(U)), dV=float(np.median(D)), S_rule=Sr, ET1=e["med"], ET1_ci=e["ci"], inside=bool(ins), lgM=e["lgM"])
        Pn(f"  {nm} {k}: n {len(qs)} U {np.median(U):.2f} dV {np.median(D):+.1f}; S_rule {Sr:.0f} vs ET1 {e['med']:.0f} [{e['ci'][0]:.0f},{e['ci'][1]:.0f}] {'inside' if ins else 'outside'}")
    R[nm]["S_at"] = {f"{l}": Srule(10 ** l, s) / (MSUNE / PC2) for l in (8, 9, 10, 11)}; Pn(f"  {nm} S_rule at lg M200 8/9/10/11: " + " / ".join(f"{v:.1f}" for v in R[nm]["S_at"].values()))
json.dump(R, open(os.path.join(HERE, "nf1_bins.json"), "w"), indent=1, default=float); open(os.path.join(HERE, "nf1_bins.out"), "w").write("\n".join(OUT) + "\n")
