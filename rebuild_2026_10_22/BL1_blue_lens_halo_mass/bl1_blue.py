#!/usr/bin/env python3
"""BL1_blue_lens_halo_mass (criteria c64f9be055): S2's forward model (read-only, its own text up to its K2 block) with route E halos at EM1's M200 and FC1's core rule.
    PYTHONHASHSEED=0 OMP_NUM_THREADS=1 nice -n 15 python3 bl1_blue.py [--mutate]   kappa = 1/2 FITTED; footings never pooled; not theory closed."""
import json, math, os, sys
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"): os.environ[_v] = "1"
import numpy as np
from scipy.optimize import brentq, minimize_scalar
BHERE = os.path.dirname(os.path.abspath(__file__)); REB = os.path.dirname(BHERE); S2 = os.path.join(REB, "S2_v3_lowg_lensing", "s2_v3_lowg_lensing.py")
MUTB = "--mutate" in sys.argv; sys.argv = [S2]
T = open(S2).read(); CUT = "# ---- K2: forward model of an isolated point mass"; assert T.count(CUT) == 1
N = {"__file__": S2, "__name__": "s2_ro"}; exec(compile(T[:T.index(CUT)], S2, "exec"), N)
AQ, RG, LMG, LRT, CENTRAL, cell, model_g, DAT, H_NAT, zl, WW, MEMB, a0u, Gpc, FOOTS = (N[k] for k in ("AQ", "RGRID_PC", "LMG", "LRT", "CENTRAL", "cell", "model_g", "DAT", "H_NAT", "zl", "WW", "MEMB", "a0u", "Gpc", "FOOTS"))
OUT = []
def P(s): print(s, flush=True); OUT.append(str(s))
EM1J = json.load(open(os.path.join(REB, "EM1_emergent_dust_law", "em1_emergent_results.json")))["rows"]["A_c2b_refit"]["R1"]; BA, BB = EM1J["a"], EM1J["b"]
HB = json.load(open(os.path.join(REB, "F3_growth_audit", "f3_growth_audit_results.json")))["K2"]["A_c2b_refit"]["params"]["h"]
X43J = json.load(open(os.path.join(REB, "X43_collapse_core_floor", "x43_collapse_core_results.json")))
SCT = sorted((math.log10(float(k)), math.log10(v[0])) for k, v in X43J["sigma_coll_table"].items()); SC_LM, SC_LS = np.array([a for a, _ in SCT]), np.array([b for _, b in SCT])
def sigma_coll(M):
    l = math.log10(M)
    if l < SC_LM[0]: s = (SC_LS[1] - SC_LS[0]) / (SC_LM[1] - SC_LM[0]); return 10 ** (SC_LS[0] + s * (l - SC_LM[0]))
    if l > SC_LM[-1]: s = (SC_LS[-1] - SC_LS[-2]) / (SC_LM[-1] - SC_LM[-2]); return 10 ** (SC_LS[-1] + s * (l - SC_LM[-1]))
    return 10 ** float(np.interp(l, SC_LM, SC_LS))
CE = json.load(open(os.path.join(REB, "CE1_converged_eta_grade", "ce1_results.json")))["eta"]; ETAV = [CE[str(e)]["med"] for e in (12, 13, 14)]
NOM, NH, NWB = 0.2976016, 0.6856427, 0.0223081; NOB = NWB / NH ** 2; FC = (NOM - NOB) / NOM
def eta_conv(M): return float(np.interp(math.log10(M), [12, 13, 14], ETAV))
def B(x): x = np.asarray(x, float); return 4 * (np.arcsinh(x) - x / np.sqrt(1 + x * x))
SAT = {"n": 0}
def solve_r0(M, R, S):                                            # X38 A1's compact root, as X53; saturation counted
    lm = lambda lr: math.log(math.pi * S * math.exp(2 * lr) * float(B(R / math.exp(lr))))
    pk = minimize_scalar(lambda lr: -lm(lr), bounds=(math.log(R * 1e-6), math.log(R * 1e3)), method="bounded", options={"xatol": 1e-10}); lpk = float(pk.x)
    if lm(lpk) < math.log(M): SAT["n"] += 1; return math.exp(lpk)
    return math.exp(brentq(lambda lr: lm(lr) - math.log(M), math.log(R * 1e-7), lpk, xtol=1e-14))
SIGA = {f: a0u(f) / (2 * math.pi * Gpc) for f in FOOTS}
ZT = float(np.average(np.minimum(zl, 1.0), weights=WW.sum(1))); RHOM0 = 2.775e11 * NH ** 2 * NOM / 1e18; DTA = 5.55
STATE = dict(mode="law", prof="E", dlm=0.0, hf=0.5 if MUTB else 1.0); TAB = {}; LAW_TABLE = N["table"]; META = {}
def halo(foot, Ms, Mc, Mb_tot, dlm, prof):
    M200 = 10 ** (BA + BB * (math.log10(Ms + Mc) - 10) + dlm); R200 = (3 * M200 / (4 * math.pi * 200 * 2.775e11 * HB ** 2 / 1e18)) ** (1 / 3)
    Mt = M200 / FC; S = max(SIGA[foot], FC * eta_conv(Mt) * sigma_coll(Mt)); r0 = solve_r0(M200, R200, S)
    rta = (3 * (M200 + Mb_tot) / (4 * math.pi * DTA * RHOM0)) ** (1 / 3) / (1 + ZT); rc = rta if prof == "E" else R200
    return math.pi * S * r0 ** 2 * B(np.minimum(RG, max(rc, R200)) / r0), dict(M200=M200, R200=R200, S=S, r0=r0, rta=rta)
def table(foot, h, yk, fhot, dcold, dMs):
    if STATE["mode"] == "law": return LAW_TABLE(foot, h, yk, fhot, dcold, dMs)
    key = (foot, h, fhot, dcold, round(dMs, 8), STATE["prof"], round(STATE["dlm"], 6), STATE["hf"])
    if key in TAB: return TAB[key]
    tab = np.empty((len(LMG), len(LRT)))
    for gi, lm in enumerate(LMG):
        lm70 = lm - 2 * math.log10(0.70 / h); Ms = 10 ** (lm + dMs); Mc = 10 ** (lm + (-0.69 * lm70 + 6.63) + dcold); Mh_ = fhot * 10 ** lm
        Mb = Ms + Mc + Mh_ * np.minimum(1.0, (RG / 1e5) ** 3); Mh, _ = halo(foot, Ms, Mc, Ms + Mc + Mh_, STATE["dlm"], STATE["prof"])
        tab[gi] = np.log(AQ.delta_sigma(np.exp(LRT) * 1e6, RG, Mb + STATE["hf"] * Mh, "const"))
    TAB[key] = tab; return tab
N["table"] = table
CFG = dict(CENTRAL, ye="zero"); CFG25 = dict(CFG, split="ur25"); RES = dict(fc=FC, z_ta=ZT, a=BA, b=BB, k={}, foot={}); ok = True; S2J = json.load(open(os.path.join(REB, "S2_v3_lowg_lensing", "s2_v3_lowg_lensing_results.json")))
P(f"BL1 blue lenses, route E at EM1's M200, FC1's rule; f_c {FC:.5f}; z_ta {ZT:.3f}; EM1 a {BA} b {BB}; kappa = 1/2 FITTED; footings never pooled; not theory closed" + (" [MUTATE halo x 0.5]" if MUTB else ""))
d = 0.0
if not MUTB:
    lad = S2J["ladder"] if "ladder" in S2J else S2J.get("LADDER", S2J)
    for foot in FOOTS:
        for k in N["CLS"]:
            a = cell(foot, k, CFG); ref = None
            for lk, row in (lad[foot].items() if foot in lad else []):
                if lk.startswith("L4"): ref = row[k]["A"]
            if ref is None: raise SystemExit("NOT DECIDED: S2 L4 not found in results")
            d = max(d, abs(a["A"] - ref)); RES["k"].setdefault("law", {}).setdefault(foot, {})[k] = dict(A=a["A"], sA=a["sA"], chi2=a["chi2_15_A1"], cls=a["cls"])
    k1 = d <= 1e-6; ok &= k1; P(f"K1 S2's L4 reproduced (blue/red/all, both footings): max |d| {d:.1e}: {'PASS' if k1 else 'FAIL'}"); RES["k"]["K1"] = bool(k1)
    k2 = 0.0; k3 = 0.0
    for lM in (11.5, 12.0, 13.0):
        M = 10 ** lM; R = (3 * M / (4 * math.pi * 200 * 2.775e11 * HB ** 2 / 1e18)) ** (1 / 3); r0 = solve_r0(M, R, 150.0); k2 = max(k2, abs(math.pi * 150.0 * r0 ** 2 * float(B(R / r0)) / M - 1))
    k3 = abs(math.pi * 106.85 * solve_r0(1e12, 2e5, 106.85) ** 2 * float(B(2e5 / solve_r0(1e12, 2e5, 106.85))) / 1e12 - 1)
    ok &= k2 <= 1e-8 and k3 <= 1e-6; P(f"K2 M_h(R200) = M200 max {k2:.1e}; K3 solve at S 106.85, M 1e12 {k3:.1e}: {'PASS' if k2 <= 1e-8 and k3 <= 1e-6 else 'FAIL'}"); RES["k"]["K2"] = k2; RES["k"]["K3"] = k3
STATE["mode"] = "E"
def run(foot, k, prof, dlm, cfg=CFG):
    STATE.update(prof=prof, dlm=dlm); return cell(foot, k, cfg)
GRID = np.round(np.arange(-0.4, 0.8001, 0.05), 3)
def delta(foot, k, cfg=CFG):
    As, ss = [], []
    for dl in GRID:
        a = run(foot, k, "E", float(dl), cfg); As.append(a["A"]); ss.append(a["sA"])
    As, ss = np.array(As), np.array(ss)
    def cross(t):
        y = As - t; idx = np.where(np.sign(y[:-1]) * np.sign(y[1:]) <= 0)[0]
        return float(GRID[idx[0]] + (GRID[idx[0] + 1] - GRID[idx[0]]) * y[idx[0]] / (y[idx[0]] - y[idx[0] + 1])) if idx.size else None
    # A falls as M200 rises; the 2 sigma range of Delta runs from A + 2s = 1 to A - 2s = 1
    return dict(d=cross(1.0), lo=cross_s(As, ss, -2), hi=cross_s(As, ss, 2), s1lo=cross_s(As, ss, -1), s1hi=cross_s(As, ss, 1), A=As.tolist(), s=ss.tolist())
def cross_s(As, ss, n):
    y = As + (-n) * ss - 1; idx = np.where(np.sign(y[:-1]) * np.sign(y[1:]) <= 0)[0]
    return float(GRID[idx[0]] + (GRID[idx[0] + 1] - GRID[idx[0]]) * y[idx[0]] / (y[idx[0]] - y[idx[0] + 1])) if idx.size else None
for foot in FOOTS:
    F = {}
    for k in N["CLS"]:
        a = run(foot, k, "E", 0.0); t = run(foot, k, "T", 0.0); F[k] = dict(A=a["A"], sA=a["sA"], cls=a["cls"], chi2=a["chi2_15_A1"], A_T=t["A"], sA_T=t["sA"], chi2_T=t["chi2_15_A1"])
        P(f"  [{foot} {k}] E: A {a['A']:.3f} +- {a['sA']:.3f} [{a['cls']}], chi2(15) {a['chi2_15_A1']:.1f}; T: A {t['A']:.3f} +- {t['sA']:.3f}, chi2 {t['chi2_15_A1']:.1f}" + ("" if MUTB else f"; law A {RES['k']['law'][foot][k]['A']:.3f} chi2 {RES['k']['law'][foot][k]['chi2']:.1f}"))
    if not MUTB:
        for k in N["CLS"]:
            F[k]["D"] = delta(foot, k); D = F[k]["D"]; P(f"    Delta_{k}: {D['d']} (1 sigma {D['s1lo']}, {D['s1hi']}; 2 sigma {D['lo']}, {D['hi']})")
        a25 = {k: run(foot, k, "E", 0.0, CFG25) for k in ("blue", "red")}; F["ur25"] = {k: dict(A=v["A"], sA=v["sA"], cls=v["cls"]) for k, v in a25.items()}; P(f"    u-r 2.5 split: blue A {a25['blue']['A']:.3f} +- {a25['blue']['sA']:.3f}; red A {a25['red']['A']:.3f} +- {a25['red']['sA']:.3f}")
        cl = F["blue"]["cls"]; g = {"consistent": "BLUE CONSISTENT", "between": "BLUE BETWEEN", "short": "BLUE SHORT", "over": "BLUE OVER"}[cl]
        def has0(D):                                                   # "lo" is the A + 2 sigma = 1 crossing (upper Delta), "hi" the A - 2 sigma = 1 crossing (lower Delta); None = off the grid
            if D["d"] is None: return False
            return (D["hi"] is None or D["hi"] <= 0) and (D["lo"] is None or D["lo"] >= 0)
        b0, r0_ = has0(F["blue"]["D"]), has0(F["red"]["D"]); c = "COLOUR SPLIT" if b0 and not r0_ else "GAP IN BOTH" if not b0 and not r0_ else "NO GAP" if b0 and r0_ else "OTHER"
        if not ok: g = "NOT DECIDED (" + g + ")"; c = "NOT DECIDED (" + c + ")"
        F["grade"] = g; F["colour"] = c; P(f"  GRADE [{foot}]: {g}; colour reading: {c}")
    RES["foot"][foot] = F
if MUTB:
    B0 = json.load(open(os.path.join(BHERE, "bl1_results.json")))["foot"]["canonical"]["blue"]["A"]; A1 = RES["foot"]["canonical"]["blue"]["A"]
    P(f"MUTATE halo x 0.5: blue A {B0:.3f} -> {A1:.3f}: {'PASS' if A1 > B0 else 'FAIL'}")
tag = "_MUTATE" if MUTB else ""
RES["saturated_solves"] = SAT["n"]; P(f"saturated r0 solves: {SAT['n']}")
json.dump(RES, open(os.path.join(BHERE, f"bl1_results{tag}.json"), "w"), indent=1, default=float); open(os.path.join(BHERE, f"bl1{tag}.out"), "w").write("\n".join(OUT) + "\n")
