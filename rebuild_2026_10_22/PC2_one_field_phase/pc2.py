#!/usr/bin/env python3
"""PC2_one_field_phase: one field, two phases, derived switch. FROZEN_CRITERIA.md committed alone first.
Run: PYTHONHASHSEED=0 OMP_NUM_THREADS=1 nice -n 19 python3 pc2.py     twin: PC2_MUTATE=1 (hbar x 2, K1 must fail, exit 1)
kappa = 1/2 FITTED; cold dark energy, never a particle; the cold sector stays retired; not theory closed;
nothing here says the data favour the framework."""
import csv, glob, json, math, os, sys
import numpy as np
import sympy as sp

MUT = os.environ.get("PC2_MUTATE") == "1"; TAG = "_MUTATE" if MUT else ""
HERE = os.path.dirname(os.path.abspath(__file__)); RB = os.path.dirname(HERE); INP = os.path.join(RB, "CRG1_clean_room_regrade", "inputs")
OUT = open(os.path.join(HERE, f"pc2{TAG}.out"), "w"); RES = dict(lane="PC2_one_field_phase", mutate=MUT, checks={}, settings="kappa = 1/2 FITTED; cold dark energy never a particle; retired sector stays retired; not theory closed")


def P(*a):
    s = " ".join(str(x) for x in a); print(s); OUT.write(s + "\n")


def check(k, ok, val, thr):
    RES["checks"][k] = dict(ok=bool(ok), value=val, threshold=thr); P(f"  [{'PASS' if ok else 'FAIL'}] {k}: {val} | {thr}")


G, MS, PC, C = 6.67430e-11, 1.98847e30, 3.0856775814913673e16, 299792458.0
KPC, MPC = PC * 1e3, PC * 1e6
HBAR = 1.054571817e-34 * (2.0 if MUT else 1.0); KB = 1.380649e-23; EV = 1.602176634e-19; AMU = 1.66053906660e-27
A0 = dict(canonical=9.3603e-11, alt=1.1312e-10); ZETA32 = 2.612375; ZETA3 = 1.2020569; W = (12.19, 12.39); TOLW = 0.12; TQ = 0.3; T_MID = 12.3
GYR = 3.15576e16; ev_kg = EV / C ** 2; KM = 1e3
SC = json.load(open(os.path.join(INP, "scalars.json"))); BG = {}
for b, q in SC["backgrounds"].items():
    p = q["params"]; h = p["h"]; H0 = 100 * h * 1e3 / MPC; BG[b] = dict(h=h, H0=H0, rhoc=3 * H0 ** 2 / (8 * math.pi * G), a=q["em1_map_a"], b=q["em1_map_b"], wb=p["omega_b"], wc=p["omega_cdm"])
Bn = list(BG); bA = BG[Bn[0]]; Unit = MS / PC ** 3 / KM ** 3     # Q unit: Msun/pc^3/(km/s)^3
WX = 0.1197; rho_x0 = WX * 3 * (100e3 / MPC) ** 2 / (8 * math.pi * G)


def R200(lM, B): return (3 * 10 ** lM * MS / (800 * math.pi * B["rhoc"])) ** (1 / 3)
def V200(lM, B): return math.sqrt(G * 10 ** lM * MS / R200(lM, B))
def rho_flat(V, r): return V ** 2 / (4 * math.pi * G * r ** 2)
def Qflat(V, r): return rho_flat(V, r) / (V / math.sqrt(2)) ** 3
def Qc(m_kg): return ZETA32 * m_kg ** 4 / ((2 * math.pi) ** 1.5 * HBAR ** 3)
def m_of_Qc(Q): return (Q * (2 * math.pi) ** 1.5 * HBAR ** 3 / ZETA32) ** 0.25
def lQ(Q): return math.log10(Q / Unit)
def QM(lM, B, f=1.0): return Qflat(V200(lM, B), f * R200(lM, B))
def lM_of_Q(Q, B, f=1.0):
    # Q(M) proportional to 1/M at fixed f
    return 12.0 + math.log10(QM(12.0, B, f) / Q)
def lands(l, s):
    t = max(TOLW, s); return W[0] - t <= l <= W[1] + t
def miss(l): return l - W[1] if l > W[1] else (l - W[0] if l < W[0] else 0.0)


P("PC2_one_field_phase" + (" [MUTATE: hbar x 2, control output]" if MUT else "") + ": criteria f2beb77a4a; kappa = 1/2 FITTED; retired sector stays retired; not theory closed")
# ------------------------------------------------- inputs: SPARC
T = {}
for l in open(os.path.join(INP, "sparc", "SPARC_Lelli2016c.mrt")):
    t = l.split()
    if len(t) == 19:
        try: T[t[0]] = dict(Inc=float(t[5]), L=float(t[7]), MHI=float(t[13]), Vf=float(t[15]), Q=int(t[17]))
        except ValueError: pass
S = []
for f in sorted(glob.glob(os.path.join(INP, "sparc", "rotmod", "*_rotmod.dat"))):
    n = os.path.basename(f).replace("_rotmod.dat", "")
    if n not in T: continue
    a = np.loadtxt(f, comments="#", ndmin=2); t = T[n]; Rm = a[:, 0] * KPC
    gb = (np.sign(a[:, 3]) * a[:, 3] ** 2 + 0.5 * a[:, 4] ** 2 + 0.7 * a[:, 5] ** 2) * 1e6 / Rm
    S.append(dict(name=n, r=Rm[-1], V=a[-1, 1] * 1e3, gmax=float(np.max(gb)), lMb=math.log10((0.5 * t["L"] + 1.33 * t["MHI"]) * 1e9), **t))
sel = [g for g in S if g["Q"] <= 2 and g["Inc"] >= 30 and g["Vf"] > 0]
BINS = [(20, 60), (60, 100), (100, 150), (150, 200), (200, 250), (250, 400)]
MC = json.load(open(os.path.join(RB, "MC1_minimal_cold_requirement", "mc1_results.json")))["footings"]

# ------------------------------------------------- checks
Tc = 2 * math.pi * HBAR ** 2 / (4.002602 * AMU * KB) * (145.0 / (4.002602 * AMU) / ZETA32) ** (2 / 3)
check("K1", abs(Tc - 3.13) <= 0.02, f"ideal Bose T_c of 4He {Tc:.3f} K", "3.13 within 0.02 K")
Nat = SC["native"]; OBn = Nat["wb"] / Nat["h"] ** 2; RR = 1 + (Nat["Om"] - OBn) / OBn; rcn = 3 * (100 * Nat["h"] * 1e3 / MPC) ** 2 / (8 * math.pi * G)
nu = lambda y: 0.5 + math.sqrt(0.25 + 1 / y)
def Z1(edge, a0):
    lo, hi = 6.0, 17.0
    fun = lambda l: math.log(nu(G * 10 ** l * MS / ((3 * RR * 10 ** l * MS / (4 * math.pi * edge * rcn)) ** (1 / 3)) ** 2 / a0)) - math.log(RR)
    for _ in range(200):
        c = 0.5 * (lo + hi)
        if fun(lo) * fun(c) <= 0: hi = c
        else: lo = c
    return 0.5 * (lo + hi) + math.log10(RR)
z1 = {f: {str(e): Z1(e, A0[f]) for e in (200, 500)} for f in A0}
DT = json.load(open(os.path.join(RB, "DT1_threshold_tournament", "dt1_tournament_results.json")))["candidates"]
check("K2", max(abs(z1[f]["200"] - DT["G (R200)"]["logT"][f]) for f in A0) <= 0.05, f"Z1 R200 {z1['canonical']['200']:.3f}, {z1['alt']['200']:.3f} vs DT1 {DT['G (R200)']['logT']['canonical']:.3f}, {DT['G (R200)']['logT']['alt']:.3f}", "0.05 dex")
xc = MC["canonical"]["xcop"]
check("K3", xc["table"]["0.1"]["n"] == 7 and abs(xc["table"]["0.1"]["GN"] / 6.73 - 1) < 1e-3, f"MC1 JSON X-COP x 0.1 Gamma_N {xc['table']['0.1']['GN']:.4f}, n 7", "README 6.73 within rounding; values read from JSON unchanged")
r1090 = rho_x0 * 1091 ** 3 / (MS / PC ** 3)
check("K4", abs(r1090 / 43 - 1) <= 0.02, f"rho_x(z 1090) {r1090:.2f} Msun/pc^3", "43 within 2 %")
v2 = V200(12.0, bA); r2 = R200(12.0, bA); vh = (10 * G * 1e12 * MS * bA["H0"]) ** (1 / 3)
check("K5", abs(v2 / vh - 1) < 1e-10 and abs(r2 / (vh / (10 * bA["H0"])) - 1) < 1e-10, f"V200 {v2 / 1e3:.2f} km/s R200 {r2 / KPC:.1f} kpc", "(10 G H M)^(1/3), V/(10H)")
Xs, cc, ms = sp.symbols("X c m", positive=True); Xn = sp.Symbol("X", negative=True); Pp = cc * Xs ** sp.Rational(3, 2); n_ = sp.diff(Pp, Xs); cs2 = sp.simplify(n_ / (ms * sp.diff(n_, Xs)))
Pn = cc * Xn * sp.sqrt(-Xn); nn = sp.diff(Pn, Xn); cs2n = sp.simplify(nn / (ms * sp.diff(nn, Xn)))
check("K6", sp.simplify(cs2 - 2 * Xs / ms) == 0 and sp.simplify(cs2n - 2 * Xn / ms) == 0, f"X>0 {cs2}; X<0 {cs2n}", "2X/m, CFG122")

# ------------------------------------------------- gate 1
P("\n== GATE 1: switch landing; W [12.19, 12.39], tolerance max(0.12, spread); canonical graded, alt reported")
rows = {}
def rowadd(k, vals, zero=True, note=""):
    sp_ = (max(vals["A"], vals["B"]) - min(vals["A"], vals["B"])) if "B" in vals else 0.0
    rows[k] = dict(primary=vals["A"], spread=sp_, miss=miss(vals["A"]), lands=lands(vals["A"], sp_), zero_constant=zero, note=note, alt=vals.get("alt"))
    P(f"  {k}: log M {vals['A']:.3f}" + (f" (B {vals['B']:.3f})" if "B" in vals else "") + (f" alt {vals['alt']:.3f}" if vals.get("alt") is not None else "") + f" | miss {rows[k]['miss']:+.3f} {'LANDS' if rows[k]['lands'] else 'MISS'} {note}")
rowadd("Z1 share R200", dict(A=z1["canonical"]["200"], alt=z1["alt"]["200"]), note="DT1 G reproduced")
rowadd("Z1 share R500", dict(A=z1["canonical"]["500"], alt=z1["alt"]["500"]))
# Z2 g200 = a0 : g200 ~ M^(1/3)
def Z2(a0, B): return 12 + 3 * math.log10(a0 / (G * 1e12 * MS / R200(12.0, B) ** 2))
rowadd("Z2 g200=a0", dict(A=Z2(A0["canonical"], BG[Bn[0]]), B=Z2(A0["canonical"], BG[Bn[1]]), alt=Z2(A0["alt"], BG[Bn[0]])))
# Z3 peak gbar = a0
srt = sorted(sel, key=lambda g: g["lMb"])
def Z3(a0, B):
    lm = np.array([g["lMb"] for g in srt]); lg = np.log10([g["gmax"] / a0 for g in srt]); w = 21; med = np.array([np.median(lg[i:i + w]) for i in range(len(lg) - w)]); mid = np.array([np.median(lm[i:i + w]) for i in range(len(lg) - w)])
    i = int(np.argmax(med >= 0)); return (B["a"] + B["b"] * (float(mid[i]) - 10), float(mid[i]), float(np.median([g["Vf"] for g in srt[i:i + w]])))
z3 = {f: Z3(A0[f], BG[Bn[0]]) for f in A0}; rowadd("Z3 peak g_b=a0", dict(A=z3["canonical"][0], B=Z3(A0["canonical"], BG[Bn[1]])[0], alt=z3["alt"][0]), note=f"log Mb {z3['canonical'][1]:.2f}, V_flat {z3['canonical'][2]:.0f}; acceleration key, X60's class")
rowadd("Z4 X43 crossover, native c_f", dict(A=DT["C"]["logT"]["canonical"], alt=DT["C"]["logT"]["alt"]), note="READ DT1 C")
rowadd("Z4b CSM1 corrected, L 3.75", dict(A=11.223), note="READ CSM1")
hbarc = 1.973269804e-7  # eV m
rho_de = (1 - Nat["Om"]) * rcn; rho_de_ev4 = rho_de * C ** 2 / EV * hbarc ** 3
mZ5 = rho_de_ev4 ** 0.25
MPl = 2.435e27; a0ev = {f: A0[f] / C * (HBAR / EV) for f in A0}; mZ6 = {f: math.sqrt(a0ev[f] * MPl) for f in A0}
def lM_deg(m_ev, B, f=1.0): return lM_of_Q(Qc(m_ev * ev_kg), B, f)
rowadd("Z5 m=rho_DE^(1/4)", dict(A=lM_deg(mZ5, BG[Bn[0]]), B=lM_deg(mZ5, BG[Bn[1]])), note=f"m {mZ5:.3e} eV")
rowadd("Z6 m=Lambda_BK(alpha 1)", dict(A=lM_deg(mZ6["canonical"], BG[Bn[0]]), B=lM_deg(mZ6["canonical"], BG[Bn[1]]), alt=lM_deg(mZ6["alt"], BG[Bn[0]])), note=f"m {mZ6['canonical']:.3e} eV")
def lM_R(R, B): return math.log10(800 * math.pi * B["rhoc"] * R ** 3 / 3 / MS)
for lab, mu in (("v3s mu_K 0.1", 0.1), ("forest 56.6", 56.6), ("crossing 2.04e4", 2.04e4), ("BBN 1.24e8", 1.24e8)):
    rowadd(f"Z7 pi/mu=R200, {lab}", dict(A=lM_R(math.pi / mu * MPC, BG[Bn[0]]), B=lM_R(math.pi / mu * MPC, BG[Bn[1]])), note="floor or ceiling on mu, READ BOLTZ1, v3s")
P("  READ, not redone: TD1 A1 13.942, A2 13.542-13.885, A3 NO LINK; COOL1 10.876; DT1 A 12.09/12.43 is external c_f, a reference only")
der = [k for k, v in rows.items() if v["lands"] and v["zero_constant"]]
smallest = min(rows, key=lambda k: abs(rows[k]["miss"]))
P(f"  zero-constant rows landing: {der or 'NONE'}; smallest miss {smallest} {rows[smallest]['miss']:+.3f}")
RES["gate1"] = dict(rows=rows, landing=der, smallest=smallest)
Tb = {}
for lab, f in (("R200", 1.0), ("0.1 R200", 0.1)):
    q = QM(T_MID, bA, f); m = m_of_Qc(q) / ev_kg; lo, hi = m_of_Qc(QM(W[1], bA, f)) / ev_kg, m_of_Qc(QM(W[0], bA, f)) / ev_kg
    Tb[lab] = dict(m_eV=m, lo=lo, hi=hi, lQ=lQ(q)); P(f"  C1 FIT, NOT DERIVED, degeneracy at {lab}: m {m:.3f} eV [{lo:.3f}, {hi:.3f}] across W; log Q_c {lQ(q):.2f}; V200(T) {V200(T_MID, bA) / 1e3:.0f} km/s; window in m is {100 * (hi / lo - 1):.0f} %")
sig = V200(T_MID, bA) / math.sqrt(2); mC2 = HBAR / (sig * R200(T_MID, bA)) / ev_kg; muC3 = math.pi / (R200(T_MID, bA) / MPC)
P(f"  C2 FIT: hbar/(m sigma)=R200: m {mC2:.3e} eV. C3 FIT: pi/mu=R200: mu {muC3:.2f}/Mpc, against BOLTZ1's forest floor 56.6 (x{56.6 / muC3:.1f}), BBN floor 1.24e8 (x{1.24e8 / muC3:.1e})")
RES["gate1"].update(C1=Tb, C2_m_eV=mC2, C3_mu=muC3, Z5_m_eV=mZ5, Z6_m_eV=mZ6)
# V_flat place
lb = 10 + (np.array([W[0], W[1]]) - bA["a"]) / bA["b"]
inW = [g["Vf"] for g in S if lb[0] - 0.2 <= g["lMb"] <= lb[1] + 0.2 and g["Vf"] > 0]
above = [g for g in S if bA["a"] + bA["b"] * (g["lMb"] - 10) > T_MID]
vT = (G * 10 ** ((lb[0] + lb[1]) / 2) * MS * A0["canonical"]) ** 0.25 / 1e3
P(f"  V_flat place: T maps to log M_b {lb[0]:.2f}-{lb[1]:.2f}; law's flat speed there {vT:.0f} km/s; SPARC median V_flat within +-0.2 of it {np.median(inW):.0f} (n {len(inW)}); SPARC above T {len(above)} of {len(S)}; V200(T) {V200(T_MID, bA) / 1e3:.0f}, so V_flat/V200 = {vT * 1e3 / V200(T_MID, bA):.2f}")
RES["gate1"]["Vflat"] = dict(vT=vT, med=float(np.median(inW)), above=len(above), total=len(S))

# ------------------------------------------------- gate 2
P("\n== GATE 2: log Q = log10[rho/sigma^3], Msun/pc^3/(km/s)^3; sigma = V_c/sqrt2; tolerance 0.3 dex")
G2 = {}
for foot in A0:
    a0 = A0[foot]; x = MC[foot]["xcop"]; law = {}
    for lo_, hi_ in BINS:
        q = [lQ(Qflat(g["V"], g["r"])) for g in sel if lo_ <= g["Vf"] < hi_]; law[f"SPARC outer {lo_}-{hi_}"] = (float(np.median(q)), float(np.percentile(q, 16)), float(np.percentile(q, 84)), len(q))
    Vk = (G * 10 ** 10.5 * MS * a0) ** 0.25; Qk = lQ(Qflat(Vk, 310 * KPC)); Qk1 = lQ(Qflat(Vk, 100 * KPC)); law["KiDS logM* 10.5, r 0.31 Mpc"] = (Qk, Qk, Qk, 1)
    LT = [lQ(Qflat(float(r["V_kms"]) * 1e3, float(r["Rmax_kpc"]) * KPC)) for r in csv.DictReader(open(os.path.join(INP, "little_things", "oh2015_table2.csv"))) if r["V_kms"].strip() and r["Rmax_kpc"].strip()]
    law["LITTLE THINGS last point"] = (float(np.median(LT)), float(np.percentile(LT, 16)), float(np.percentile(LT, 84)), len(LT))
    cold_tot, cold_N = {}, {}
    tb = x["table"]; xs = ["0.1", "0.2", "0.3", "0.5", "0.7"]
    for i, k in enumerate(xs):
        r = tb[k]["r"] * KPC; Vc = math.sqrt(G * tb[k]["mh"] * MS / r); s = Vc / math.sqrt(2)
        cold_tot[f"X-COP x {k}, flat-rule rho_tot"] = lQ(rho_flat(Vc, r) / s ** 3)
    for xx, rr, rh in zip(x["rho"]["N"]["x"], x["rho"]["N"]["r_kpc"], x["rho"]["N"]["rho_Mspc3"]):
        kk = f"{xx:g}"
        if rh > 0 and kk in tb: cold_N[f"X-COP shell to x {kk}, rho_x N"] = math.log10(rh / (math.sqrt(G * tb[kk]["mh"] * MS / (tb[kk]["r"] * KPC) / 2) / 1e3) ** 3)
    B_ = MC[foot]["bullet"]
    for lab, m_ in zip(("main", "sub"), np.array(B_["need"]) + np.array(B_["law"])):
        Vc = math.sqrt(G * m_ * MS / (300 * KPC)); cold_tot[f"Bullet {lab} M300"] = lQ(Qflat(Vc, 300 * KPC))
    d = {}
    for r in csv.DictReader(open(os.path.join(INP, "dwarfs", "x1_per_system_inputs.csv"))):
        if r["footing"] == foot and r["sigma"] and r["rh_pc"]:
            s = float(r["sigma"]) * 1e3; rr = float(r["rh_pc"]) * PC; d.setdefault(r["cls"], []).append(lQ(s ** 2 / (2 * math.pi * G * rr ** 2) / s ** 3))
    dw = {k: float(np.median(v)) for k, v in d.items() if len(v) > 3}
    lawv = {k: v[0] for k, v in law.items() if "250-400" not in k}
    L0 = min(lawv.values()); Lk = min(lawv, key=lawv.get); Ct = max(cold_tot.values()); Ck = max(cold_tot, key=cold_tot.get); CN = max(cold_N.values()); CNk = max(cold_N, key=cold_N.get)
    gap = L0 - Ct; gapN = L0 - CN; sparconly = min(v for k, v in lawv.items() if "SPARC" in k)
    lab = lambda g: "SEPARATED" if g > TQ else ("NOT SEPARATED" if g < -TQ else "MARGINAL")
    G2[foot] = dict(law=law, cold_tot=cold_tot, cold_N=cold_N, dwarfs=dw, gap_tot=gap, gap_N=gapN, label_tot=lab(gap), label_N=lab(gapN), low_law=Lk, top_cold=Ck, top_cold_N=CNk, gap_tot_noKiDS=sparconly - Ct, gap_N_noKiDS=sparconly - CN, Q_kids_100kpc=Qk1)
    P(f" {foot}"); [P(f"  law  {k}: {v[0]:+.2f} [{v[1]:+.2f}, {v[2]:+.2f}] n {v[3]}") for k, v in law.items()]; P(f"  KiDS at 0.1 Mpc, reported: {Qk1:+.2f}")
    [P(f"  cold {k}: {v:+.2f}") for k, v in cold_tot.items()]; [P(f"  cold {k}: {v:+.2f}") for k, v in cold_N.items()]; P("  dwarfs: " + ", ".join(f"{k} {v:+.2f}" for k, v in dw.items()))
    P(f"  LABEL rho_tot: gap {gap:+.2f} ({Lk} vs {Ck}) {lab(gap)}; rho_x N: gap {gapN:+.2f} {lab(gapN)}. SPARC-only, reported: {sparconly - Ct:+.2f}, {sparconly - CN:+.2f}")
RES["gate2"] = G2
z_on = 3e4; v0 = C / z_on; Qbg_warm = rho_x0 / v0 ** 3; g2c = G2["canonical"]; Qd = {k: v[0] for k, v in g2c["law"].items() if "SPARC" in k}
vcold = 6e3 / 4; Qbg_forest = rho_x0 / vcold ** 3
zreq = {k: C / (rho_x0 / (10 ** v * Unit)) ** (1 / 3) for k, v in Qd.items()}
P(f"\n FRW: rho_x0 {rho_x0 / (MS / PC ** 3):.3e} Msun/pc^3. Warmest field non-relativistic at z 3e4: v0 {v0 / 1e3:.2f} km/s, log Q_bg {lQ(Qbg_warm):+.2f}. X22's c_s 6 km/s at z 3 (forest, a warning only): log Q_bg {lQ(Qbg_forest):+.2f}")
P("  z_nr needed for Q_bg >= Q of each law class, Liouville: " + ", ".join(f"{k.split()[-1]} {v:.2e}" for k, v in zreq.items()) + f"; dwarfs' largest {max(g2c['dwarfs'].values()):+.2f} needs z_nr {C / (rho_x0 / (10 ** max(g2c['dwarfs'].values()) * Unit)) ** (1 / 3):.2e}")
RES["frw"] = dict(lQ_warm=lQ(Qbg_warm), lQ_forest=lQ(Qbg_forest), znr_needed=zreq)

# ------------------------------------------------- gate 3
P("\n== GATE 3: abundance; thermal relic of C1's mass, g = 1 (g = 2 reported), z_nr against 3e4")
G3 = {}
for lab, q in Tb.items():
    m = q["m_eV"]; n = rho_x0 * C ** 2 / EV / m      # 1/m^3
    for g_ in (1, 2):
        Tx = (n * math.pi ** 2 / (ZETA3 * g_)) ** (1 / 3) * hbarc; z = m / (3.15 * Tx) - 1; Tr = Tx / (2.7255 * 8.617333e-5)
        G3[f"{lab} g{g_}"] = dict(Tx_eV=Tx, Tx_over_Tgamma=Tr, znr=z, x3e4=3e4 / z); P(f"  {lab}, m {m:.3f} eV, g {g_}: T_x today {Tx / 8.617333e-5:.2f} K ({Tr:.2f} T_gamma), z_nr {z:.2e}, short of 3e4 by x{3e4 / z:.2f}")
RES["gate3"] = G3
P("  Non-thermal: abundance is an integration constant (BOLTZ1 G16): not interlocked, counted +1. Then Q_bg is unbounded above, so FRW is degenerate, see FRW line.")

# ------------------------------------------------- gate 4
P("\n== GATE 4: mass reading. M_ph(R200)/M_b against 5.35; EM1 R200")
G4 = {}
for foot in A0:
    for Vf in (60, 100, 150, 200, 250, 300):
        Mb = (Vf * 1e3) ** 4 / (G * A0[foot]) / MS; lM = bA["a"] + bA["b"] * (math.log10(Mb) - 10); Rv = R200(lM, bA); Mph = (Vf * 1e3) ** 2 * Rv / G / MS - Mb; cs = 10 ** lM * (1 - 1 / RR)
        G4[f"{foot} {Vf}"] = dict(lMb=math.log10(Mb), lM200=lM, Mph_over_Mb=Mph / Mb, Mph_over_share_EM1=Mph / cs); P(f"  {foot} V {Vf}: log Mb {math.log10(Mb):.2f}, EM1 log M200 {lM:.2f}, R200 {Rv / KPC:.0f} kpc, M_ph/M_b {Mph / Mb:.1f}, M_ph/(EM1 cold share) {Mph / cs:.2f}")
RES["gate4"] = G4

# ------------------------------------------------- gate 5
P("\n== GATE 5: thermalisation against the Bullet; s = sigma_x/m_x; N = Q/Q_c")
tH = 1 / bA["H0"]
S_sub_gcm2 = MC["canonical"]["bullet"]["need"][1] * MS / (math.pi * (300 * KPC) ** 2) * 0.1
s_tau1 = 1 / S_sub_gcm2; s_lit = 1.25
Qcmax = 10 ** max(g2c["cold_tot"].values()) * Unit   # lowest Q_c that keeps every cold row out of the degenerate side
Qcmax_N = 10 ** max(g2c["cold_N"].values()) * Unit
G5 = {}
def smin(V, r, Qc_):
    N = max(Qflat(V, r) / Qc_, 1.0); rho = rho_flat(V, r) * 1e-3  # g/cm^3 (kg/m^3 x 1e-3)
    return 1 / (N * rho * (V * 100) * tH), N
rows5 = dict(Rlast_200_250=(225e3, g2c and float(np.median([g["r"] for g in sel if 200 <= g["Vf"] < 250]))), Rlast_100_150=(125e3, float(np.median([g["r"] for g in sel if 100 <= g["Vf"] < 150]))), KiDS_31=((G * 10 ** 10.5 * MS * A0["canonical"]) ** 0.25, 310 * KPC), KiDS_100=((G * 10 ** 10.5 * MS * A0["canonical"]) ** 0.25, 100 * KPC))
for k, (V, r) in rows5.items():
    a = smin(V, r, Qcmax); b = smin(V, r, Qcmax_N); G5[k] = dict(smin_tot=a[0], N_tot=a[1], smin_N=b[0], N_N=b[1], over_tau1_tot=a[0] / s_tau1, over_lit_tot=a[0] / s_lit, over_tau1_N=b[0] / s_tau1, over_lit_N=b[0] / s_lit)
    P(f"  {k}: rho {rho_flat(V, r) / (MS / PC ** 3):.2e} Msun/pc^3, s_min {a[0]:.2f} cm^2/g (N {a[1]:.1f}, Q_c at top cold rho_tot); {b[0]:.2f} (N {b[1]:.1f}, Q_c at top rho_x N)")
P(f"  Bullet: Sigma_sub cold need in 300 kpc {S_sub_gcm2:.3f} g/cm^2: s_max(tau 1) {s_tau1:.2f} cm^2/g; PROVISIONAL Randall+ 1.25 cm^2/g")
P("  FRW rate at s_min(R_last 200-250), warmest z_nr 3e4, Bose N_bg = Q_bg/Q_c floored at 1: Gamma/H")
def Hz(z): return bA["H0"] * math.sqrt((bA["wb"] + bA["wc"]) / bA["h"] ** 2 * (1 + z) ** 3 + 4.15e-5 / bA["h"] ** 2 * (1 + z) ** 4 + 0.7)
sv = G5["Rlast_200_250"]["smin_tot"]; G5["frw"] = {}
for z in (0, 3, 20, 100, 1090, 1e4, 3e4):
    rho = rho_x0 * (1 + z) ** 3 * 1e-3; v = v0 * (1 + z) * 100; Nb = max(Qbg_warm / Qcmax, 1.0); g = sv * rho * v * Nb / Hz(z); G5["frw"][str(z)] = g; P(f"   z {z:g}: Gamma/H {g:.2e} (N_bg {Nb:.2f})")
RES["gate5"] = G5; RES["gate5_bullet"] = dict(sigma_gcm2=S_sub_gcm2, s_tau1=s_tau1, s_lit=s_lit)


# ------------------------------------------------- A1, POST-HOC rows; no frozen label moves
P("\n== POST-HOC (A1)")
PH = {}
from astropy.io import fits
DX = os.path.join(os.path.dirname(RB), "real_research", "data", "xcop"); inner = {}
for n in sorted(os.listdir(DX)):
    p_ = os.path.join(DX, n)
    if not (os.path.isdir(p_) and os.path.exists(os.path.join(p_, f"{n}_mstar.fits"))): continue
    with fits.open(os.path.join(p_, f"{n}_hydro_mass.fits")) as h: hm = h[1].data.copy(); r5 = h[1].header["R500"]
    with fits.open(os.path.join(p_, f"{n}_fgas_profile.fits")) as h: ga = h[1].data.copy(); rg5 = h[1].header["R500"]
    with fits.open(os.path.join(p_, f"{n}_mstar.fits")) as h: st = h[2].data.copy()
    li = lambda rr, mm, t: float(10 ** np.interp(np.log10(t), np.log10(rr), np.log10(mm))) if rr[0] <= t <= rr[-1] else float("nan")
    for x_ in (0.03, 0.05, 0.07, 0.1):
        t = x_ * r5; mh, mg, ms_ = li(hm["RADIUS"], hm["M_FORW"], t), li(ga["RADIUS"] * rg5, ga["MGAS"], t), li(st["RADIUS"], st["MSTAR"], t)
        if not np.all(np.isfinite([mh, mg, ms_])): continue
        Rm = t * KPC; Vc = math.sqrt(G * mh * MS / Rm); gb = G * (mg + ms_) * MS / Rm ** 2; a0 = A0["canonical"]; law_ = gb * nu(gb / a0)
        inner.setdefault(x_, []).append((lQ(Qflat(Vc, Rm)), G * mh * MS / Rm ** 2 / law_, t))
PH["xcop_inner"] = {str(k): dict(n=len(v), lQ=float(np.median([a[0] for a in v])), obs_over_law=float(np.median([a[1] for a in v])), r_kpc=float(np.median([a[2] for a in v]))) for k, v in inner.items()}
for k, v in PH["xcop_inner"].items(): P(f"  X-COP x {k}: n {v['n']}, r {v['r_kpc']:.0f} kpc, log Q {v['lQ']:+.2f}, observed/law inside {v['obs_over_law']:.2f}")
PH["kids"] = {}
for lm in (10.1, 10.5, 10.9):
    for rk in (100, 310, 1000):
        for foot in A0: PH["kids"][f"{foot} {lm} {rk}"] = lQ(Qflat((G * 10 ** lm * MS * A0[foot]) ** 0.25, rk * KPC))
    P(f"  KiDS log M* {lm}, canonical, r 0.1, 0.31, 1 Mpc: " + ", ".join(f"{PH['kids'][f'canonical {lm} {rk}']:+.2f}" for rk in (100, 310, 1000)))
top = max(g2c["cold_tot"].values()); lowk = g2c["law"]["KiDS logM* 10.5, r 0.31 Mpc"][0]; midQ = 0.5 * (top + lowk) ; PH["gap_mid"] = midQ; PH["gap_lM"] = lM_of_Q(10 ** midQ * Unit, bA); PH["gap_m_eV"] = m_of_Qc(10 ** midQ * Unit) / ev_kg
P(f"  Gate-2 gap midpoint log Q {midQ:+.2f}: at R200 that is log M {PH['gap_lM']:.2f}, m {PH['gap_m_eV']:.2f} eV. R200(T) {R200(T_MID, bA) / KPC:.0f} kpc vs lens radius 310 kpc; V200(T) {V200(T_MID, bA) / 1e3:.0f} vs lens V {((G * 10 ** 10.5 * MS * A0['canonical']) ** 0.25) / 1e3:.0f}: the lens row IS nearly the T row, so this landing is not independent")
PH["relic"] = {}
for lab, q in Tb.items():
    v_ = 3.15 * G3[f"{lab} g1"]["Tx_eV"] / q["m_eV"] * C; PH["relic"][lab] = lQ(rho_x0 / v_ ** 3); P(f"  thermal relic {lab}: v0 {v_ / 1e3:.0f} km/s, log Q_bg {PH['relic'][lab]:+.2f}; below SPARC 200-250's {Qd['SPARC outer 200-250']:+.2f} by {Qd['SPARC outer 200-250'] - PH['relic'][lab]:.2f} dex; a fixed occupancy relic cannot reach disc Q")
Qc_use = 10 ** midQ * Unit; PH["frw"] = {}
for lab, Qtop in (("Q_bg = SPARC 200-250", Qd["SPARC outer 200-250"]), ("Q_bg = SPARC 20-60", Qd["SPARC outer 20-60"]), ("Q_bg = largest dwarf class", max(g2c["dwarfs"].values()))):
    Qb = 10 ** Qtop * Unit; v_ = (rho_x0 / Qb) ** (1 / 3); Nb = Qb / Qc_use
    for slab, s_ in (("s_min R_last 200-250", smin(*rows5["Rlast_200_250"], Qc_use)[0]), ("s_max Randall 1.25", 1.25)):
        vals = {z: s_ * rho_x0 * (1 + z) ** 3 * 1e-3 * v_ * 100 * (1 + z) * Nb / Hz(z) for z in (0.0, 3.0, 20.0, 100.0, 1090.0, 1e4)}
        zc = [z for z, g_ in vals.items() if g_ >= 1]; PH["frw"][f"{lab} | {slab}"] = dict(v0_kms=v_ / 1e3, N_bg=Nb, s=s_, rates={str(k): v for k, v in vals.items()}, thermal_by=max(zc) if zc else None)
        P(f"  FRW, {lab}: v0 {v_ / 1e3:.3f} km/s, N_bg {Nb:.1e}; {slab} s {s_:.3f}: Gamma/H " + ", ".join(f"z{z:g} {g_:.1e}" for z, g_ in vals.items()))
PH["pincer"] = {}
rho_d = MC["canonical"]["P2"]["disc_rho_Rlast"]["200-250"] * MS / PC ** 3
for frac in (0.6, 0.8):
    for Vf in (125e3, 225e3):
        cs = frac * Vf; rd = rho_flat(Vf, float(np.median([g["r"] for g in sel if abs(g["Vf"] - Vf / 1e3) < 25]))); nn_ = {}
        for lab, pw in (("n=1/2, P=K rho^3", 2), ("n=1, P=K rho^2", 1)):
            K = cs ** 2 / ((pw + 1) * rd ** pw); rw = ((1 / 3) * C ** 2 / K) ** (1 / pw); z = (rw / rho_x0) ** (1 / 3) - 1; nn_[lab] = z
            w_rec = K * (rho_x0 * 1091 ** 3) ** pw / C ** 2; PH["pincer"][f"{lab} c_s {frac} V, V {Vf / 1e3:.0f}"] = dict(z_w13=z, w_1090=w_rec, short_of_3e4=3e4 / z)
            P(f"  pincer {lab}, c_s {frac} V at V {Vf / 1e3:.0f}: w=1/3 at z {z:.0f}, short of 3e4 by x{3e4 / z:.0f}; w(z 1090) {w_rec:.2e}")
RES["posthoc"] = PH

# ------------------------------------------------- gate 6
P("\n== GATE 6: law's non-cluster rows, RQ2 results/law.json")
L = json.load(open(os.path.join(RB, "RQ2_framework_acceptance", "results", "law.json")))["footings"]; G6 = {}
for foot in A0:
    rr = L[foot]["rows"]; nb = sorted(k for k in rr if not k.startswith("B")); f_ = [k for k in nb if rr[k]["label"] == "FAIL"]; p_ = [k for k in nb if rr[k]["label"] == "PASS"]; ot = [k for k in nb if rr[k]["label"] not in ("PASS", "FAIL", "NOT COMPUTABLE", "READ", "OPEN DATA")]
    G6[foot] = dict(fail=f_, n_pass=len(p_), other=ot); P(f"  {foot}: non-B rows FAIL {len(f_)}: {f_}; PASS {len(p_)}; other {ot}")
RES["gate6"] = G6

# ------------------------------------------------- gate 7
P("\n== GATE 7: L = (2 Lambda (2m)^(3/2)/3) X sqrt|X| - alpha Lambda theta rho_b/M_Pl (CFG122's form), X = mu - m Phi + theta_dot - (grad theta)^2/(2m)")
P(f"  c_s^2 = {cs2} at X>0 (healthy, no MOND); {cs2n} at X<0 (the law-carrying branch), negative: gradient instability, CFG122 G5.1; rate at 1 kpc read 0.22 /Myr at m 1 eV. Transition stability and growth through it: NOT COMPUTED, no form survives.")

RES["verdict"] = dict(gate1="DERIVED" if der else "KILLED AT GATE 1 AS A DERIVATION", gate2=G2["canonical"]["label_tot"], gate2_N=G2["canonical"]["label_N"])
P("\nVERDICT: " + json.dumps(RES["verdict"], sort_keys=True))
fail = [k for k, v in RES["checks"].items() if not v["ok"]]; P(f"checks failed: {fail or 'none'}")
json.dump(RES, open(os.path.join(HERE, f"pc2{TAG}_results.json"), "w"), indent=1, sort_keys=True, default=float); OUT.close()
sys.exit(1 if fail else 0)
