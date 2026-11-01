#!/usr/bin/env python3
"""UR3 Part B: Milky Way, RG1/GD3's grader, halo term contracted. FROZEN_CRITERIA.md. Spherical baryons BY HAND. kappa = 1/2 FITTED, unused; not theory closed."""
import json, math, os, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE); from ur3_common import *
RGD = os.path.join(RB, "RG1_native_n_regrade"); s = open(os.path.join(RGD, "rg1_mw.py")).read(); s = s[:s.index("OUT = dict(K2=k2")].replace("HERE = os.path.dirname(os.path.abspath(__file__))", f"HERE = {RGD!r}")
_G0 = G; _bs = Bs; ns = {"__file__": os.path.join(RGD, "rg1_mw.py"), "__name__": "m"}; exec(compile(s, "rg1_head", "exec"), ns); g = ns["g"]; grade, CELLS, classify, BGS, SM, MCM = ns["grade"], ns["CELLS"], ns["classify"], ns["BGS"], ns["SM"], ns["MCM"]
OUT = []
def P(x): print(x, flush=True); OUT.append(x)
R0, BR_R, BR_K, BR_E5, OR, OV, OE, KZU, LINE_KZ, LINE_OU, vE, eE, KZ_BR, KZ_BR_E, Lb = g["R0"], g["BR_R"], g["BR_K"], g["BR_E5"], g["OR"], g["OV"], g["OE"], g["KZU"], g["LINE_KZ"], g["LINE_OU"], g["vE"], g["eE"], g["KZ_BR"], g["KZ_BR_E"], g["L"]
def g2(bar, tag, mode, d=0.0, mut=1.0):
    M, R2, S, r0 = halo(math.log10(bar["Mb"]), tag, d); rp = np.r_[R0, np.asarray(OR, float)]; vp = np.r_[bar["vc_R0"], np.asarray(bar["vou"], float)]; o = np.argsort(rp); rp, vp = rp[o], vp[o]; rp, ui = np.unique(rp, return_index=True); Mp = np.maximum.accumulate(vp[ui] ** 2 * rp / _G0)
    rg = np.geomspace(0.1, R2, 700); Mbg = np.where(rg < rp[0], Mp[0] * rg / rp[0], np.exp(np.interp(np.log(rg), np.log(np.r_[rp, R2]), np.log(np.r_[Mp, max(bar["Mb"], Mp[-1])])))); Mbg = np.maximum.accumulate(Mbg) * mut
    Mg = Mc(rg, Mbg, M, R2, S, r0, mode); gh = lambda r: _G0 * np.interp(np.log(np.asarray(r, float)), np.log(rg), Mg) / np.asarray(r, float) ** 2
    rk = np.hypot(BR_R, 1.1); K = bar["K"] + gh(rk) * 1.1 / rk / KZU; r00 = math.hypot(R0, 1.1); K0 = bar["K_R0"] + float(gh(r00)) * 1.1 / r00 / KZU; vc = math.sqrt(bar["vc_R0"] ** 2 + R0 * float(gh(R0))); vo = np.sqrt(bar["vou"] ** 2 + OR * gh(OR)); cK = float(np.sum(((K - BR_K) / BR_E5) ** 2)); cO = float(np.sum(((vo - OV) / OE) ** 2))
    D = max(cK / LINE_KZ, abs(vc - vE) / (2 * eE), cO / LINE_OU, abs(K0 - KZ_BR) / (2 * KZ_BR_E))
    return dict(Sig_ratio=1.0, lgM200=math.log10(M), r0=r0, sat=False, vc_R0=vc, K_R0=K0, chi2_Kz=cK, chi2_Ou=cO, L1=bool(abs(vc - Lb.VC_BRIEF) <= Lb.VC_BRIEF_LINE and abs(vc - vE) <= 2 * eE), L2a=bool(cK <= LINE_KZ), L2b=bool(abs(K0 - KZ_BR) <= 2 * KZ_BR_E), L3=bool(cO <= LINE_OU), D=D, dvc=vc - bar["vc_R0"], dK=K0 - bar["K_R0"], Qr0=float(np.interp(math.log(R0), np.log(rg), Mg) / np.interp(math.log(R0), np.log(rg), math.pi * S * r0 ** 2 * Bs(rg / r0))))
g["MODE"].update(m="native", t="A_c2b_refit"); k3 = grade(MCM, "canonical", 0, BGS["A_c2b_refit"], 0, SM); P(f"UR3 Part B, Milky Way; K3 RG1's own path, McMillan: V_c {k3['vc_R0']:.2f} K_z {k3['K_R0']:.2f} (RG1 202.8, 67.9)")
RES = dict(K3={k: k3[k] for k in ("vc_R0", "K_R0")}, rows={}); P(f"Eilers {vE} +- {eE}; K_z(R0) {KZ_BR} +- {KZ_BR_E}; lines chi2_Kz {LINE_KZ:.2f}, chi2_Ou {LINE_OU:.2f}")
for t in T["S"]:
    for lab, d in (("d0", 0.0), ("d+0.10", 0.10)):
        for mo in ("off", "blum", "gnedin"):
            m = g2(MCM, t, mo, d); rows = [g2(c["bar"], t, mo, d) for c in CELLS]; c = classify(rows); c["mcmillan"] = {k: m[k] for k in ("vc_R0", "K_R0", "chi2_Kz", "chi2_Ou", "L1", "L2a", "L2b", "L3", "lgM200", "Qr0")}; c["counts"] = {l: sum(r[l] for r in rows) for l in ("L1", "L2a", "L2b", "L3")}; RES["rows"][f"{t}|{lab}|{mo}"] = c
            P(f"{t[:1]} {lab:7s} {mo:7s} McM V_c {m['vc_R0']:.1f} K_z {m['K_R0']:.1f} chi2Kz {m['chi2_Kz']:.1f} chi2Ou {m['chi2_Ou']:.1f} L {int(m['L1'])}{int(m['L2a'])}{int(m['L2b'])}{int(m['L3'])} lgM {m['lgM200']:.2f} Q(R0) {m['Qr0']:.2f} | box {c['cls']} counts {c['counts']} all4 {c['n_all']} Rd {c['passing_Rd']} best D {c['best']['D']:.2f} inprior D {c['best_in_prior'] and c['best_in_prior']['D']}")
m = g2(MCM, "A_c2b_refit", "blum", 0.0, 2.0); RES["MUTATE"] = {k: m[k] for k in ("vc_R0", "K_R0")}; P(f"MUTATE M_b x 2 in response, McMillan: V_c {m['vc_R0']:.1f} K_z {m['K_R0']:.1f}")
_r = np.geomspace(0.1, 300, 2000); P(f"K4 contraction identity, M_b 0: {float(np.max(np.abs(contract(_r, np.zeros_like(_r), 1e8 * _r, 0.0)[0] / (1e8 * _r) - 1)[5:-5])):.1e}")
json.dump(RES, open(os.path.join(HERE, "ur3_mw.json"), "w"), indent=1, default=float); open(os.path.join(HERE, "ur3_mw.out"), "w").write("\n".join(OUT) + "\n")
# Stress, reported after the result (a win is checked as hard as a fail): spherical baryons by hand, and in-prior cells.
def st(mode, mut, t="A_c2b_refit"):
    rows = [g2(c["bar"], t, mode, 0.0, mut) for c in CELLS]; c = classify(rows); ip = [(CELLS[i], r) for i, r in enumerate(rows) if CELLS[i]["tag_Rd_IN"] and CELLS[i]["tag_Mstar_IN"] and all(r[l] for l in ("L1", "L2a", "L2b", "L3"))]
    P(f"stress {mode} M_b x {mut}: {c['cls']} all4 {c['n_all']} in-prior all4 {len(ip)} best inprior D {c['best_in_prior'] and round(c['best_in_prior']['D'], 2)}; " + "; ".join(f"Rd {a['R_d']:.2f} M* {a['Mstar']:.2e} Vc {r['vc_R0']:.0f} K {r['K_R0']:.1f} Q {r['Qr0']:.2f}" for a, r in ip[:4]))
for mo in ("blum", "gnedin"):
    for mu in (0.7, 0.85, 1.0, 1.15): st(mo, mu)
# Stress 2, reported after the result: start the response from LC1's measured zoom shape, NFW c 12.95 at 1e12, instead of the hand-chosen smooth core.
import ur3_common as _U
_Mc0 = Mc
def _McN(rg, Mbg, M, R, S, r0, mode):
    c = 12.95; mu = lambda x: np.log1p(x) - x / (1 + x); M0 = M * mu(rg / (R / c)) / mu(c)
    if mode == "off": return M0
    return contract(rg, Mbg, M0, float(Mbg[-1] / M0[-1]), gnedin=(0.85, 0.8, rg[-1]) if mode == "gnedin" else None)[0]
_M, _R, _S, _r = halo(math.log10(MCM["Mb"]), "A_c2b_refit"); _x = np.array([R0]); P(f"start mass at R0: smooth core {float(math.pi * _S * _r ** 2 * Bs(R0 / _r)):.3e}, r0 {_r:.2f} kpc, S {_S / 1e6:.1f} Msun/pc2; NFW c 12.95 {float(_McN(_x, _x, _M, _R, 0, 0, 'off')[0]):.3e}, M200 {_M:.3e}")
Mc = _McN
for mo in ("off", "blum", "gnedin"):
    m = g2(MCM, "A_c2b_refit", mo); rows = [g2(c["bar"], "A_c2b_refit", mo) for c in CELLS]; c = classify(rows); P(f"NFW start {mo}: McM V_c {m['vc_R0']:.1f} K_z {m['K_R0']:.1f} | box {c['cls']} all4 {c['n_all']} best D {c['best']['D']:.2f} Vc {c['best']['vc_R0']:.0f} K {c['best']['K_R0']:.1f}"); RES["rows"][f"NFWstart|{mo}"] = dict(cls=c["cls"], best=c["best"], mcm=[m["vc_R0"], m["K_R0"]])
Mc = _Mc0; json.dump(RES, open(os.path.join(HERE, "ur3_mw.json"), "w"), indent=1, default=float); open(os.path.join(HERE, "ur3_mw.out"), "w").write("\n".join(OUT) + "\n")
