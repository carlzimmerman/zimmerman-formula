#!/usr/bin/env python3
"""SN1: what S do the LG dwarfs need? X49's data path; criteria FROZEN_CRITERIA.md. python3 sn1.py [--mutate]"""
import csv, json, math, os, sys, time
import numpy as np
from scipy.optimize import brentq, minimize_scalar
T0 = time.time(); MUT = "--mutate" in sys.argv; KS = 0.5 if MUT else 1.0; TAG = "_MUTATE" if MUT else ""
HERE = os.path.dirname(os.path.abspath(__file__)); REB = os.path.dirname(HERE); REPO = os.path.dirname(REB); OUT = []
def P(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); OUT.append(s)
G, MSUN, PC, MPC = 6.67430e-11, 1.98847e30, 3.0856775814913673e16, 3.0856775814913673e22
U = MSUN / PC ** 2; A0 = {"canonical": 9.3603e-11, "alt": 1.1312e-10}; FEET = tuple(A0)
CLS = ("MW ultra-faint", "bright M31", "M31 others", "MW classical", "LG field"); BMAX = 2.1907
def BB(x): x = np.asarray(x, float); return np.log1p(x * x) + 2 * np.log1p(x) - 2 * np.arctan(x)
def BS(x): x = np.asarray(x, float); return 4 * (np.arcsinh(x) - x / np.sqrt(1 + x * x))
def solve_r0(M, R, Sig, B):
    lm = lambda lr: math.log(math.pi * Sig * math.exp(2 * lr) * float(B(R / math.exp(lr))))
    lpk = float(minimize_scalar(lambda lr: -lm(lr), bounds=(math.log(R * 1e-6), math.log(R * 1e3)), method="bounded", options={"xatol": 1e-10}).x)
    if lm(lpk) < math.log(M): return math.exp(lpk)
    return math.exp(brentq(lambda lr: lm(lr) - math.log(M), math.log(R * 1e-7), lpk, xtol=1e-14))
EM = json.load(open(os.path.join(REB, "EM1_emergent_dust_law", "em1_emergent_results.json")))["rows"]["A_c2b_refit"]["R1"]
h = json.load(open(os.path.join(REB, "F3_growth_audit", "f3_growth_audit_results.json")))["K2"]["A_c2b_refit"]["params"]["h"]
RHOC = 3 * (100 * h * 1e3 / MPC) ** 2 / (8 * math.pi * G)
ARR = list(csv.DictReader(open(os.path.join(REPO, "campaign_fresh_gravity", "CFG257_ufd_kinematics_scoping", "arroyo_polonio2026_tableA1.csv"))))
AF = {r["lvd_name"]: float(r["sig_free"]) / float(r["sig_f0"]) for r in ARR}; MF = float(np.median(list(AF.values())))
X1 = list(csv.DictReader(open(os.path.join(REB, "X1_hosted_recount", "x1_per_system.csv"))))
def systems(f, fair=False):
    out = []
    for r in X1:
        if r["footing"] != f or r["cls"] not in CLS: continue
        mv = float(r["M_V"]) if r["M_V"] not in ("", None) else None
        b = AF.get(r["name"], MF if (mv is not None and mv > -7.7) else 1.0)
        sc = float(r["sigma"]) * b; r12 = 4 / 3 * float(r["rh_pc"]) * PC; Mb = 10 ** float(r["logMstar"])
        gobs = 3 * (sc * 1e3) ** 2 / r12; gN = G * (Mb / 2) * MSUN / r12 ** 2
        M200 = (6.364 * Mb if fair else 10 ** (EM["a"] + EM["b"] * (math.log10(Mb) - 10))) * MSUN
        out.append(dict(name=r["name"], cls=r["cls"], r12=r12, gobs=gobs, gN=gN, M200=M200, R200=(3 * M200 / (4 * math.pi * 200 * RHOC)) ** (1 / 3), s=float(r["sdMC[Newton]"]), lm=float(r["logMstar"])))
    return out
def Eof(q, Spc, B):
    Sig = KS * Spc * U; r0 = solve_r0(q["M200"], q["R200"], Sig, B)
    Mh = math.pi * Sig * r0 ** 2 * float(B(min(q["r12"], q["R200"]) / r0)); return math.log10(q["gobs"] / (q["gN"] + G * Mh / q["r12"] ** 2))
LS = np.round(np.arange(0.5, 3.5001, 0.01), 2)
def table(Q, B): return np.array([[Eof(q, 10 ** l, B) for l in LS] for q in Q])          # systems x grid
def boot_setup(Q, seed=20261031, n=2000):
    rng = np.random.default_rng(seed); idx = {};
    for c in CLS:
        I = np.array([i for i, q in enumerate(Q) if q["cls"] == c]); idx[c] = (I, rng.integers(0, len(I), (n, len(I))), rng.standard_normal((n, len(I))))
    return idx
def clsZ(E, Q, idx):
    """E: per-system vector -> {class: (median, sd, Z)}"""
    s = np.array([q["s"] for q in Q]); o = {}
    for c, (I, ix, nz) in idx.items():
        m = float(np.median(E[I])); sd = float(np.std(np.median(E[I][ix] + s[I][ix] * nz, axis=1))); o[c] = (m, sd, m / sd)
    return o
def interpE(T, lgS):                                                                      # lgS per system
    i = np.clip(np.floor((lgS - LS[0]) / 0.01).astype(int), 0, len(LS) - 2); w = (lgS - LS[i]) / 0.01
    k = np.arange(T.shape[0]); return T[k, i] * (1 - w) + T[k, i + 1] * w
def spearman(x, y):
    a = np.argsort(np.argsort(x)).astype(float); b = np.argsort(np.argsort(y)).astype(float); a -= a.mean(); b -= b.mean(); return float((a * b).sum() / math.sqrt((a ** 2).sum() * (b ** 2).sum()))
RES = dict(frozen="FROZEN_CRITERIA.md", mutate=MUT, footings={}); ET1 = [(9.97, 52, 85), (10.59, 81, 124), (11.13, 118, 200)]
RG1 = json.load(open(os.path.join(REB, "RG1_native_n_regrade", "rg1_p1_native_smooth.json")))["classes"]; X49 = json.load(open(os.path.join(REB, "X49_dwarfs_route_e_floor", "x49_dwarfs_results.json")))["footings"]
sys.path.insert(0, os.path.join(REB, "RG1_native_n_regrade")); os.environ.pop("RG1_MUTATE", None); import rg1_lib as L
for f in FEET:
    Q = systems(f); idx = boot_setup(Q); F = RES["footings"][f] = {}; lM = np.log10([q["M200"] / MSUN for q in Q]); SA = A0[f] / (2 * math.pi * G) / U
    P(f"\n=== [{f}] N {len(Q)}; Sigma_a0 {SA:.1f}")
    if not MUT:
        Ek = np.array([Eof(q, SA, BB) for q in Q]); d1 = max(abs(float(np.median(Ek[idx[c][0]])) - X49[f]["classes"][c]["median"]) for c in CLS)
        Ek = np.array([Eof(q, L.S_nat(q["M200"] / MSUN), BS) for q in Q]); d2 = max(abs(float(np.median(Ek[idx[c][0]])) - RG1[f][c]["median"]) for c in CLS)
        xp = minimize_scalar(lambda x: -float(BS(x)) * math.pi / x ** 2, bounds=(.1, 30), method="bounded").x; d3 = abs(-(-float(BS(xp)) * math.pi / xp ** 2) * 1 - BMAX) if False else abs(math.pi * float(BS(xp)) / xp ** 2 - BMAX)
        F["K"] = dict(K1=d1, K2=d2, K3=d3); P(f"K1 X49 |d| {d1:.2e} {'PASS' if d1 < 1e-3 else 'FAIL'}; K2 RG1 |d| {d2:.2e} {'PASS' if d2 < 1e-3 else 'FAIL'}; K3 bound |d| {d3:.2e} {'PASS' if d3 < 1e-3 else 'FAIL'}")
    T = table(Q, BS); TB = table(Q, BB)
    # S_need by class
    F["S_need"] = {}
    for nm, TT in (("smooth", T), ("burkert", TB)):
        F["S_need"][nm] = {}
        for c in CLS:
            I = idx[c][0]; md = np.median(TT[I], axis=0); j = np.where(md <= 0)[0]
            sn = None if len(j) == 0 else float(10 ** (LS[j[0]] - 0.01 * md[j[0]] / (md[j[0]] - md[j[0] - 1]) * 0) if j[0] == 0 else 10 ** np.interp(0, [md[j[0]], md[j[0] - 1]], [LS[j[0]], LS[j[0] - 1]]))
            F["S_need"][nm][c] = dict(S_need=sn, lgM200=float(np.median(lM[I])), E_at_3000=float(md[-1]))
        P(f"S_need {nm}: " + "; ".join(f"{c} {v['S_need'] and round(v['S_need'],1)} (lgM {v['lgM200']:.2f}, E@3000 {v['E_at_3000']:+.2f})" for c, v in F["S_need"][nm].items()))
    # capped
    Mneed = np.array([(q["gobs"] - q["gN"]) * q["r12"] ** 2 / G for q in Q]); M2 = np.array([q["M200"] for q in Q])
    F["capped"] = {c: [int((Mneed[idx[c][0]] > M2[idx[c][0]]).sum()), len(idx[c][0])] for c in CLS}; P("M_need > M200:", F["capped"])
    # V1
    def scan(TT):
        out = []
        for l in LS:
            E = interpE(TT, np.full(len(Q), l)); z = clsZ(E, Q, idx); out.append((float(l), max(abs(v[2]) for v in z.values()), {c: z[c] for c in CLS}))
        return out
    sc = scan(T); ok = [x[0] for x in sc if x[1] < 2]; best = min(sc, key=lambda x: x[1])
    F["V1"] = dict(verdict="ONE S ADMITTED" if ok else "NO ONE S", range=[10 ** ok[0], 10 ** ok[-1]] if ok else None, best_S=10 ** best[0], best_maxZ=best[1], best_Z={c: best[2][c][2] for c in CLS}, sigma_a0_inside=bool(ok and 10 ** ok[0] <= SA <= 10 ** ok[-1]))
    P(f"V1 {F['V1']['verdict']}; range {F['V1']['range']}; best S {10**best[0]:.1f} max|Z| {best[1]:.2f}; Z", {c[:8]: round(v, 2) for c, v in F['V1']['best_Z'].items()}, "Sigma_a0 inside", F["V1"]["sigma_a0_inside"])
    sb = scan(TB); okb = [x[0] for x in sb if x[1] < 2]; bb = min(sb, key=lambda x: x[1]); F["V1_burkert"] = dict(range=[10 ** okb[0], 10 ** okb[-1]] if okb else None, best_S=10 ** bb[0], best_maxZ=bb[1]); P("V1 Burkert (reported):", F["V1_burkert"])
    # V2
    PS = np.round(np.arange(-0.6, 0.6001, 0.01), 2); adm = []
    for p in PS:
        for l9 in LS:
            E = interpE(T, np.clip(l9 + p * (lM - 9), 0.5, 3.5)); z = clsZ(E, Q, idx)
            if max(abs(v[2]) for v in z.values()) < 2: adm.append((float(p), float(l9)))
    A = np.array(adm) if adm else np.zeros((0, 2)); F["V2"] = dict(n=len(adm))
    if len(adm):
        F["V2"].update(p_range=[float(A[:, 0].min()), float(A[:, 0].max())], S9_range=[float(10 ** A[:, 1].min()), float(10 ** A[:, 1].max())])
    a24 = A[np.isclose(A[:, 0], 0.24)] if len(adm) else A
    F["V2"]["verdict"] = "COLLAPSE SLOPE ADMITTED" if len(a24) else "COLLAPSE SLOPE EXCLUDED"
    if len(a24): F["V2"]["S9_at_024"] = [float(10 ** a24[:, 1].min()), float(10 ** a24[:, 1].max())]; F["V2"]["over_rule"] = [x / 29.4 for x in F["V2"]["S9_at_024"]]
    elif len(adm): F["V2"]["nearest_p"] = float(A[np.argmin(abs(A[:, 0] - 0.24)), 0])
    # best at p = 0.24 regardless
    bz = min(((max(abs(v[2]) for v in clsZ(interpE(T, np.clip(l9 + 0.24 * (lM - 9), .5, 3.5)), Q, idx).values()), float(l9)) for l9 in LS)); F["V2"]["p024_best"] = dict(maxZ=bz[0], S9=10 ** bz[1])
    P("V2", F["V2"])
    # V3
    def inb(p, l9, b): v = 10 ** (l9 + p * (b[0] - 9)); return b[1] <= v <= b[2]
    allj = [(p, l) for p, l in adm if all(inb(p, l, b) for b in ET1)]; low = [(p, l) for p, l in adm if all(inb(p, l, b) for b in ET1[:2])]
    F["V3"] = dict(verdict="CURVE JOINS" if allj else "JOINS LOW BINS ONLY" if low else "NO JOIN", n_all=len(allj), n_low=len(low))
    if len(adm):
        # nearest approach: S of admitted members at each band centre
        F["V3"]["adm_S_at_bins"] = {str(b[0]): [float((10 ** (A[:, 1] + A[:, 0] * (b[0] - 9))).min()), float((10 ** (A[:, 1] + A[:, 0] * (b[0] - 9))).max())] for b in ET1}
        if allj: F["V3"]["members"] = dict(p=[min(x[0] for x in allj), max(x[0] for x in allj)], S9=[10 ** min(x[1] for x in allj), 10 ** max(x[1] for x in allj)])
    P("V3", F["V3"])
    # V4
    Smin = np.log10(np.maximum(Mneed, 1e-300) / np.array([q["r12"] for q in Q]) ** 2 / BMAX / U / KS); neg = int((Mneed <= 0).sum()); Smin = np.where(Mneed > 0, Smin, -2.0)
    z = {c: clsZ(Smin, Q, {c: idx[c]})[c] for c in CLS}; hi = min(z[c][0] + 2 * z[c][1] for c in CLS); lo = max(z[c][0] - 2 * z[c][1] for c in CLS)
    F["V4"] = dict(verdict="ONE S_min" if lo <= hi else "S_min VARIES", cls={c: dict(S_min=10 ** z[c][0], dex_sd=z[c][1]) for c in CLS}, band=[10 ** lo, 10 ** hi], n_nonpositive=neg,
                   rho_r12=spearman(np.array([q["r12"] for q in Q]), Smin), rho_Mstar=spearman(np.array([q["lm"] for q in Q]), Smin), rho_gN=spearman(np.array([q["gN"] for q in Q]), Smin))
    P("V4", F["V4"])
    # field vs satellites reported + fair share
    Qf = systems(f, True); idf = boot_setup(Qf); Tf = table(Qf, BS); o = {}
    for l, n in ((math.log10(29.4), "S 29.4"), (math.log10(SA), "Sigma_a0"), (F["V1"]["best_S"] and math.log10(F["V1"]["best_S"]), "V1 best")):
        o[n] = {c: round(v[2], 2) for c, v in clsZ(interpE(Tf, np.full(len(Qf), l)), Qf, idf).items()}
    F["fair_share_Z"] = o; P("fair-share Z:", o)
    z = clsZ(interpE(T, np.full(len(Q), math.log10(SA))), Q, idx); F["smooth_at_sigma_a0"] = {c: dict(E=v[0], Z=v[2]) for c, v in z.items()}; P("smooth core at Sigma_a0:", {c[:8]: (round(v[0], 3), round(v[2], 2)) for c, v in z.items()})
V = {f: {k: RES["footings"][f][k]["verdict"] for k in ("V1", "V2", "V3", "V4")} for f in FEET}
RES["verdicts"] = {k: V["canonical"][k] if V["canonical"][k] == V["alt"][k] else f"UNDECIDED {V['canonical'][k]} / {V['alt'][k]}" for k in V["canonical"]}
P("\n=== VERDICTS", RES["verdicts"]); P(f"runtime {time.time()-T0:.0f} s")
open(os.path.join(HERE, f"sn1{TAG}.out"), "w").write("\n".join(OUT) + "\n"); json.dump(RES, open(os.path.join(HERE, f"sn1_results{TAG}.json"), "w"), indent=1, default=float)
