#!/usr/bin/env python3
# CFG181 referee main: independent re-derivation of CFG174 Q1-Q4 from the frozen question (no repo import; no CFG174 script read).
# MUTATE=k (1..7): control; exits 1 iff the control bites (the load-bearing line flips to FAIL).  Main exits 0 with a class line.
import os, sys, json, math
sys.dont_write_bytecode = True
import numpy as np, sympy as sp
from CFG181_common import *
HERE = os.path.dirname(os.path.abspath(__file__))
MUT = int(os.environ.get("MUTATE", "0"))
H, OL = 0.674, 0.685            # primary cosmology for Q1/Q4
T0 = 13.79 * GYR                 # as the frozen question states
HQ3, OMQ3 = 0.6766, 0.3111       # Q3 cosmology
out = {"MUTATE": MUT}; lines = []
def P(s=""): print(s); lines.append(s)

# ---------- README targets (read, not blind)
T = dict(SigA=106.9, SigB=129.2, swept=365.0, RA=0.293, RB=0.354, f=[(0.1, 1.00), (1, 0.83), (10, 0.18), (30, 0.064)], slope=-0.87,
         q3={0.85: -0.33, 1.5: -0.51, 2.5: -0.72}, q3v={0.85: -0.08, 1.5: -0.13, 2.5: -0.18}, Hz={0.85: 0.21, 1.5: 0.37, 2.5: 0.57},
         q4A={14: 2.06, 14.5: 1.40, 15: 0.95}, q4B={14: 2.49, 14.5: 1.69, 15: 1.15})

# ---------- symbolic identities
r, Mb, a0s, Gs = sp.symbols("r M_b a0 G", positive=True)
gN = Gs * Mb / r**2
Mc = r**2 * sp.sqrt(gN**2 + a0s * gN) / Gs - Mb          # M_c = g r^2/G - M_b with g = sqrt(gN^2 + a0 gN)
Mc_ser = sp.simplify(sp.series(Mc, r, 0, 3).removeO())
sym_ok = sp.simplify(Mc_ser - a0s * r**2 / (2 * Gs)) == 0
rho_s, ts, cs, ks = sp.symbols("rho_L t c kappa", positive=True)
Rsym = sp.simplify((a0s / (2 * sp.pi * Gs)) / (rho_s * cs * ts)); R_has_Mb = Mb in Rsym.free_symbols
P(f"[sympy] small-r limit of M_c(<r) = {Mc_ser}  (== a0 r^2/(2G): {sym_ok});  R symbolic = {Rsym};  contains M_b: {R_has_Mb}")
out["sympy_ok"] = bool(sym_ok and not R_has_Mb)

# ---------- Q1
a0f = 1.0; t0 = T0; ucol = 1.0; colfac = 1.0; u = C
if MUT == 1: t0 = 1.0 * GYR
if MUT == 2: colfac = 0.25            # shell surface density M_c/(4 pi r^2) = a0/(8 pi G)
if MUT == 3: u = 370e3
if MUT == 4: a0f = 0.1
if MUT == 5: colfac = 4.0
def Q1(a0):
    S = Sigma_P2(a0 * a0f) * colfac; sw = swept(H, OL, t0, u); return S, sw, S / sw
SA, sw, RA = Q1(A0_A); SB, _, RB = Q1(A0_B)
LO, HI = 0.1, 1.0
q1_pass = (LO <= RA <= HI)
umin = RA * C
kappa_chk = A0_A / (C * math.sqrt(G * rho_L(H, OL)))
P(f"[Q1] cosmology H0={H*100:.1f}, OL={OL}; t0={t0/GYR:.2f} Gyr; u={u/1e3:.0f} km/s; check kappa=a0/(c sqrt(G rho_L)) = {kappa_chk:.4f}")
P(f"[Q1] Sigma_M A/B = {SA:.2f}/{SB:.2f} Msun/pc^2; swept = {sw:.2f}; R A/B = {RA:.4f}/{RB:.4f}; u_min/c = {umin/C:.4f}; pass line 0.1<=R<=1: {q1_pass}")
R_alt_formula = 0.5 / (2 * math.pi * (t0) * math.sqrt(G * rho_L(H, OL)))
P(f"[Q1] R via kappa/(2 pi t0 sqrt(G rho_L)) with kappa=1/2: {R_alt_formula:.4f} (footing-A a0 is the CHARTER value, kappa_eff = {kappa_chk:.4f})")
out["Q1"] = dict(SigA=SA, SigB=SB, swept=sw, RA=RA, RB=RB, pass_line=bool(q1_pass), u_over_c=umin / C, kappa_eff=kappa_chk)
# hand check with the Q3 cosmology
out["Q1_swept_at_Q3_cosmology"] = swept(HQ3, 0.6889, T0)

# ---------- Q2 (numerical, from the kernel, then analytic)
def fnum(x, M=1e11):
    Mk = M * MSUN; a0 = A0_A
    rr = x * math.sqrt(G * Mk / a0); g = float(nu_p2(G * Mk / rr**2 / a0)) * G * Mk / rr**2
    Mc_ = g * rr**2 / G - Mk; return Mc_ / (Mk * x**2 / 2)
fs = {x: fnum(x) for x in (0.1, 1, 10, 30)}
slope = math.log(fnum(30) / fnum(3)) / math.log(10)
fslope = {x: (math.log(fnum(x * 1.001)) - math.log(fnum(x / 1.001))) / (2 * math.log(1.001)) for x in (30, 100, 1000)}
P(f"[Q2] f(x)=M_c/(M_c small-r asymptote): " + ", ".join(f"x={x}: {v:.4f}" for x, v in fs.items()) + f"; chord slope 3-30 = {slope:.4f}; local slopes {', '.join(f'x={x}:{v:.3f}' for x,v in fslope.items())}")
P(f"[Q2] fraction of the SWEPT column (R*f): " + ", ".join(f"x={x}: {RA*v:.4f}" for x, v in fs.items()))
out["Q2"] = dict(f=fs, slope=slope, local_slopes=fslope, f_swept={x: RA * v for x, v in fs.items()})

# ---------- Q3
q3 = {}
for z in (0.85, 1.5, 2.5):
    ratio = t_of_z(HQ3, 1 - OMQ3, z) / age_flat(HQ3, 1 - OMQ3)
    if MUT == 6: ratio = E_of_z(OMQ3, z)              # sign control: the H(z) reading in the accumulation slot
    dex = math.log10(ratio); q3[z] = dict(dex=dex, vel=dex / 4, Hdex=math.log10(E_of_z(OMQ3, z)))
P(f"[Q3] t0(Q3 cosmology)={age_flat(HQ3,1-OMQ3)/GYR:.3f} Gyr; " + "; ".join(f"z={z}: dex {v['dex']:+.3f}, vel {v['vel']:+.3f}, a0~H {v['Hdex']:+.3f}" for z, v in q3.items()))
q3_falls = q3[1.5]["dex"] < 0
out["Q3"] = q3; out["Q3_falls_line"] = bool(q3_falls)

# ---------- Q4
def Q4(a0, mut7=False, colf=1.0):
    S = to_msunpc2(a0 / (2 * math.pi * G)) * colf * 1e12       # Msun / Mpc^2
    res = {}; sw_res = {}
    rc = rho_crit(H); rc_msun_mpc3 = rc / MSUN * MPC**3
    for lm in (14, 14.5, 15):
        M = 10**lm; R = r500(M, H) / MPC                           # Mpc
        area = math.pi * R**2
        if mut7:                                                    # mass ~ R^3 at fixed value at 1e14: M-proportional
            R14 = r500(1e14, H) / MPC; mass = S * math.pi * R14**2 * (M / 1e14)
        else: mass = S * area
        need = 0.85 * M; res[lm] = mass / need
        sw_res[lm] = to_msunpc2(rho_L(H, OL) * C * T0) * 1e12 * area / need
    return res, sw_res
q4A, swA = Q4(A0_A, MUT == 7); q4B, _ = Q4(A0_B, MUT == 7)
slope4 = (math.log10(q4A[15]) - math.log10(q4A[14])) / 1.0
label = {lm: (0.5 <= q4A[lm] <= 2.0) for lm in q4A}
q4_pass = all(label.values()); scaling_line = abs(slope4 + 1 / 3) <= 0.02
P(f"[Q4] A ratio (column mass / 0.85 M500): " + ", ".join(f"{lm}:{v:.3f}" for lm, v in q4A.items()) + "; B: " + ", ".join(f"{lm}:{v:.3f}" for lm, v in q4B.items()))
P(f"[Q4] swept-column ratio: " + ", ".join(f"{lm}:{v:.2f}" for lm, v in swA.items()) + f"; exponent d log ratio/d logM = {slope4:.4f} (line: -1/3 +- 0.02: {scaling_line}); factor-2 line per mass {label}; overall pass {q4_pass}")
out["Q4"] = dict(A=q4A, B=q4B, swept=swA, slope=slope4, label=label, pass_line=bool(q4_pass), scaling_line=bool(scaling_line))

# ---------- reproduction table (only for the unmutated run)
def within(v, t, tol, rel=True): return abs(v - t) <= (tol * abs(t) if rel else tol)
rows = []
def add(name, mine, tgt, ok): rows.append((name, mine, tgt, bool(ok)))
if MUT == 0:
    add("Sigma_M A", SA, T["SigA"], within(SA, T["SigA"], .006)); add("Sigma_M B", SB, T["SigB"], within(SB, T["SigB"], .015))
    add("swept col", sw, T["swept"], within(sw, T["swept"], .015))
    add("R A", RA, T["RA"], abs(RA - T["RA"]) <= .004); add("R B", RB, T["RB"], abs(RB - T["RB"]) <= .005)
    add("u_min/c", umin / C, T["RA"], abs(umin / C - T["RA"]) <= .004)
    for x, v in T["f"]: add(f"f({x})", fs[x], v, abs(fs[x] - v) <= .005)
    add("slope 3-30", slope, T["slope"], abs(slope - T["slope"]) <= .01)
    for z in q3:
        add(f"Q3 dex z={z}", q3[z]["dex"], T["q3"][z], abs(q3[z]["dex"] - T["q3"][z]) <= .01)
        add(f"Q3 vel z={z}", q3[z]["vel"], T["q3v"][z], abs(q3[z]["vel"] - T["q3v"][z]) <= .005)
        add(f"a0~H dex z={z}", q3[z]["Hdex"], T["Hz"][z], abs(q3[z]["Hdex"] - T["Hz"][z]) <= .01)
    for lm in q4A:
        add(f"Q4 A {lm}", q4A[lm], T["q4A"][lm], within(q4A[lm], T["q4A"][lm], .03)); add(f"Q4 B {lm}", q4B[lm], T["q4B"][lm], within(q4B[lm], T["q4B"][lm], .03))
    add("Q4 label FAIL at 14 only", float(label[14]), 0.0, (not label[14]) and label[14.5] and label[15])
    add("Q4 swept band in [2.8,7.4]", min(swA.values()), 2.8, all(2.8 <= v <= 7.4 for v in swA.values()))
    add("sympy M_c limit + R mass-free", float(out["sympy_ok"]), 1.0, out["sympy_ok"])
    P(""); P("reproduction table (mine vs README target; README numbers are targets read, not blind)")
    for n, m, t_, ok in rows: P(f"  {n:28s} mine {m:10.4f}  README {t_:8.3f}  {'OK' if ok else 'OUT OF TOLERANCE'}")
    bad = [n for n, m, t_, ok in rows if not ok]
    q1bad = [n for n in bad if n.startswith(("Sigma", "swept", "R ", "u_min", "Q3", "a0~H"))]
    cls = "REPRODUCES" if not bad else ("DISAGREES" if any(abs(m - t_) > 0.05 * abs(t_) and n.startswith(("R ", "Q3 dex")) for n, m, t_, ok in rows if not ok) else "PARTIAL")
    P(f"CLASS: {cls}; rows out of tolerance: {bad}")
    out["class"] = cls; out["rows"] = rows; out["bad"] = bad
    tgt = f"{HERE}/CFG181_main"
else:
    lines_map = {1: ("Q1 pass line", q1_pass), 2: ("Q1 pass line", q1_pass), 3: ("Q1 pass line", q1_pass), 4: ("Q1 pass line", q1_pass),
                 5: ("Q1 pass line", q1_pass), 6: ("Q3 falls-with-z line", q3_falls), 7: ("Q4 wrong-scaling line", scaling_line)}
    nm, val = lines_map[MUT]
    bites = not val
    P(f"[MUTATE {MUT}] load-bearing line '{nm}' = {val} -> control {'BITES (flips to FAIL)' if bites else 'DOES NOT BITE'}")
    out["control_bites"] = bool(bites); out["line"] = nm
    tgt = f"{HERE}/CFG181_MUTATE_{MUT}"
open(tgt + ".out", "w").write("\n".join(lines) + "\n")
json.dump(out, open(tgt + ("_results.json" if MUT else "_results.json"), "w"), indent=1, default=float)
if MUT: sys.exit(1 if out["control_bites"] else 0)
sys.exit(0)
