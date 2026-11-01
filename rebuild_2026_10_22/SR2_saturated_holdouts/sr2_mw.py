#!/usr/bin/env python3
"""UR3 Part B: Milky Way, RG1/GD3's grader, halo term contracted. FROZEN_CRITERIA.md. Spherical baryons BY HAND. kappa = 1/2 FITTED, unused; not theory closed."""
import json, math, os, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE); from sr2_common import *
RGD = os.path.join(RB, "RG1_native_n_regrade"); s = open(os.path.join(RGD, "rg1_mw.py")).read(); s = s[:s.index("OUT = dict(K2=k2")].replace("HERE = os.path.dirname(os.path.abspath(__file__))", f"HERE = {RGD!r}")
_G0 = G; _bs = Bs; ns = {"__file__": os.path.join(RGD, "rg1_mw.py"), "__name__": "m"}; exec(compile(s, "rg1_head", "exec"), ns); g = ns["g"]; grade, CELLS, classify, BGS, SM, MCM = ns["grade"], ns["CELLS"], ns["classify"], ns["BGS"], ns["SM"], ns["MCM"]
OUT = []
def P(x): print(x, flush=True); OUT.append(x)
R0, BR_R, BR_K, BR_E5, OR, OV, OE, KZU, LINE_KZ, LINE_OU, vE, eE, KZ_BR, KZ_BR_E, Lb = g["R0"], g["BR_R"], g["BR_K"], g["BR_E5"], g["OR"], g["OV"], g["OE"], g["KZU"], g["LINE_KZ"], g["LINE_OU"], g["vE"], g["eE"], g["KZ_BR"], g["KZ_BR_E"], g["L"]
def g2(bar, tag, mode, d=0.0, mut=1.0):
    M, R2, S, r0 = halo(math.log10(bar["Mb"]), tag, d); rp = np.r_[R0, np.asarray(OR, float)]; vp = np.r_[bar["vc_R0"], np.asarray(bar["vou"], float)]; o = np.argsort(rp); rp, vp = rp[o], vp[o]; rp, ui = np.unique(rp, return_index=True); Mp = np.maximum.accumulate(vp[ui] ** 2 * rp / _G0)
    rg = np.geomspace(0.1, R2, 700); Mbg = np.where(rg < rp[0], Mp[0] * rg / rp[0], np.exp(np.interp(np.log(rg), np.log(np.r_[rp, R2]), np.log(np.r_[Mp, max(bar["Mb"], Mp[-1])])))); Mbg = np.maximum.accumulate(Mbg) * mut
    M0_ = math.pi * S * r0 ** 2 * Bs(rg / r0); Mg = sat_contract(rg, Mbg, Mbg * max(0.0, 1 - g["Mgas"] / bar["Mb"]), M0_, float(Mbg[-1] / M0_[-1])); gh = lambda r: _G0 * np.interp(np.log(np.asarray(r, float)), np.log(rg), Mg) / np.asarray(r, float) ** 2
    rk = np.hypot(BR_R, 1.1); K = bar["K"] + gh(rk) * 1.1 / rk / KZU; r00 = math.hypot(R0, 1.1); K0 = bar["K_R0"] + float(gh(r00)) * 1.1 / r00 / KZU; vc = math.sqrt(bar["vc_R0"] ** 2 + R0 * float(gh(R0))); vo = np.sqrt(bar["vou"] ** 2 + OR * gh(OR)); cK = float(np.sum(((K - BR_K) / BR_E5) ** 2)); cO = float(np.sum(((vo - OV) / OE) ** 2))
    D = max(cK / LINE_KZ, abs(vc - vE) / (2 * eE), cO / LINE_OU, abs(K0 - KZ_BR) / (2 * KZ_BR_E))
    return dict(Sig_ratio=1.0, lgM200=math.log10(M), r0=r0, sat=False, vc_R0=vc, K_R0=K0, chi2_Kz=cK, chi2_Ou=cO, L1=bool(abs(vc - Lb.VC_BRIEF) <= Lb.VC_BRIEF_LINE and abs(vc - vE) <= 2 * eE), L2a=bool(cK <= LINE_KZ), L2b=bool(abs(K0 - KZ_BR) <= 2 * KZ_BR_E), L3=bool(cO <= LINE_OU), D=D, dvc=vc - bar["vc_R0"], dK=K0 - bar["K_R0"], Qr0=float(np.interp(math.log(R0), np.log(rg), Mg) / np.interp(math.log(R0), np.log(rg), math.pi * S * r0 ** 2 * Bs(rg / r0))))
RES = dict(rows={}); P(f"Eilers {vE} +- {eE}; K_z(R0) {KZ_BR} +- {KZ_BR_E}")
SAT["on"] = False; m = g2(MCM, "A_c2b_refit", "x"); RES["K1"] = [m["vc_R0"], m["K_R0"]]; P(f"K1 denominator off McMillan V_c {m['vc_R0']:.1f} K_z {m['K_R0']:.1f} (UR3 251.2, 81.2)"); SAT["on"] = True
for t in T["S"]:
    for d in (0.0, -0.05, 0.10):
        m = g2(MCM, t, "x", d); rows = [g2(c["bar"], t, "x", d) for c in CELLS]; c = classify(rows); RES["rows"][f"{t}|{d:+.2f}"] = dict(cls=c["cls"], best=c["best"], inprior=c["best_in_prior"], n_all=c["n_all"], Rd=c["passing_Rd"], mcm=[m["vc_R0"], m["K_R0"], m["chi2_Kz"], m["chi2_Ou"]], counts={l: sum(r[l] for r in rows) for l in ("L1", "L2a", "L2b", "L3")})
        P(f"{t[:1]} d{d:+.2f} McM V_c {m['vc_R0']:.1f} K_z {m['K_R0']:.1f} chi2Kz {m['chi2_Kz']:.1f} chi2Ou {m['chi2_Ou']:.1f} Q {m['Qr0']:.2f} | box {c['cls']} all4 {c['n_all']} Rd {c['passing_Rd']} best D {c['best']['D']:.2f} Vc {c['best']['vc_R0']:.0f} K {c['best']['K_R0']:.1f} inprior D {c['best_in_prior'] and round(c['best_in_prior']['D'], 2)}")
SAT["ms"] = 0.1; m = g2(MCM, "A_c2b_refit", "x"); P(f"MUTATE M* x 0.1 McMillan V_c {m['vc_R0']:.1f} K_z {m['K_R0']:.1f}"); SAT["ms"] = 1.0
json.dump(RES, open(os.path.join(HERE, "sr2_mw.json"), "w"), indent=1, default=float); open(os.path.join(HERE, "sr2_mw.out"), "w").write("\n".join(OUT) + "\n")
