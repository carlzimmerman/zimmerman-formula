#!/usr/bin/env python3
"""x02: dimensionless numbers of the extended thermodynamics at the exact a0-points, with the pre-declared closed-form
scan (A6) against six decoy Z' values.  L = 1 (lengths in the de Sitter radius), G = c = 1.
Points: P1 f-norm BH horizon kappa_b = a0; P2 f-norm cosmological horizon kappa_c = a0; P3 flat probe hole r_s = 1/(2 a0);
P4 formal SdS object at r = r_s (a cosmological horizon with M<0); P5 BH-norm existence check."""
import mpmath as mp
from fractions import Fraction
import sys
mp.mp.dps = 50
PASS = FAIL = CO = CB = 0


def chk(n, c, d=""):
    global PASS, FAIL
    if c: PASS += 1; print("  ok  ", n, d)
    else: FAIL += 1; print("  FAIL", n, d)


def ctrl(n, c, d=""):
    global CO, CB
    if not c: CO += 1; print("  ctrl-ok ", n, d)
    else: CB += 1; print("  CTRL-BAD", n, d)


pi = mp.pi
Zt = mp.sqrt(32 * pi / 3)
DECOYS = {"2pi": 2 * pi, "6": mp.mpf(6), "5.5": mp.mpf('5.5'), "6.5": mp.mpf('6.5'), "sqrt(8pi/3)": mp.sqrt(8 * pi / 3), "1.05Z": mp.mpf('1.05') * Zt}


def pair_from_x(x): return (-x + mp.sqrt(4 - 3 * x ** 2)) / 2
def pair_from_y(y): return (-y + mp.sqrt(4 - 3 * y ** 2)) / 2   # same quadratic: x^2 + x y + y^2 = 1


def points(Zp):
    K = 1 / Zp
    out = {}
    # P1
    x = (mp.sqrt(K ** 2 + 3) - K) / 3
    y = pair_from_x(x)
    M = x * (1 - x ** 2) / 2
    out["P1"] = dict(
        x=x, y=y, mu=M / (1 / (3 * mp.sqrt(3))),
        V_over_VdS=x ** 3, V_over_Veff=x ** 3 / (y ** 3 - x ** 3),
        PV_over_M=-x ** 2 / (1 - x ** 2), TS_over_M=(1 - 3 * x ** 2) / (2 * (1 - x ** 2)), U_over_M=1 / (1 - x ** 2),
        G_over_M=(1 + x ** 2) / (2 * (1 - x ** 2)), F_over_M=(1 + 3 * x ** 2) / (2 * (1 - x ** 2)),
        CP_over_S=-2 * (1 - 3 * x ** 2) / (1 + 3 * x ** 2), S_over_SdS=x ** 2, T_over_TdS=(1 - 3 * x ** 2) / (2 * x),
        Stot_over_SdS=1 - x * y, Tc_over_Tb=((3 * y ** 2 - 1) / (2 * y)) / ((1 - 3 * x ** 2) / (2 * x)),
        R_iso=(y ** 3 - x ** 3) ** (mp.mpf(1) / 3) / mp.sqrt(x ** 2 + y ** 2),
        dG_pair=(x * (1 + x ** 2) - y * (1 + y ** 2) + 2) / 4)
    # P2
    y = (K + mp.sqrt(K ** 2 + 3)) / 3
    x = pair_from_y(y)
    M = y * (1 - y ** 2) / 2
    out["P2"] = dict(
        x=x, y=y, mu=M / (1 / (3 * mp.sqrt(3))),
        V_over_VdS=y ** 3, V_over_Veff=y ** 3 / (y ** 3 - x ** 3),
        PV_over_M=-y ** 2 / (1 - y ** 2), TS_over_M=(3 * y ** 2 - 1) / (2 * (1 - y ** 2)),
        G_over_M=-(1 + y ** 2) / (2 * (1 - y ** 2)),
        CP_over_S=2 * (3 * y ** 2 - 1) / (3 * y ** 2 + 1), S_over_SdS=y ** 2, T_over_TdS=(3 * y ** 2 - 1) / (2 * y),
        Stot_over_SdS=1 - x * y, Tb_over_Tc=((1 - 3 * x ** 2) / (2 * x)) / ((3 * y ** 2 - 1) / (2 * y)),
        R_iso=(y ** 3 - x ** 3) ** (mp.mpf(1) / 3) / mp.sqrt(x ** 2 + y ** 2),
        dG_pair=(x * (1 + x ** 2) - y * (1 + y ** 2) + 2) / 4)
    # P3 flat probe r_s = Z'/2 (units L), s = r^2
    r = Zp / 2
    s = r ** 2
    out["P3"] = dict(
        V_over_VdS=r ** 3, PV_over_M=-s, TS_over_M=mp.mpf(1) / 2, U_over_M=1 + s, G_over_M=mp.mpf(1) / 2, F_over_M=mp.mpf(1) / 2,
        CP_over_S=mp.mpf(-2), S_over_SdS=s, T_over_TdS=1 / (2 * r))
    # P4 formal SdS at r = r_s: cosmological-horizon formulas with y = r_s, M < 0
    y = Zp / 2
    M = y * (1 - y ** 2) / 2
    out["P4"] = dict(
        M_over_L=M, V_over_VdS=y ** 3, PV_over_M=-y ** 2 / (1 - y ** 2), TS_over_M=(3 * y ** 2 - 1) / (2 * (1 - y ** 2)),
        G_over_M=-(1 + y ** 2) / (2 * (1 - y ** 2)), CP_over_S=2 * (3 * y ** 2 - 1) / (3 * y ** 2 + 1),
        S_over_SdS=y ** 2, T_over_TdS=(3 * y ** 2 - 1) / (2 * y), kappa_over_a0=(3 * y ** 2 - 1) / (2 * y) * Zp)
    return out


def closed_form(val, tol=mp.mpf('1e-9')):
    """(p/q) pi^a sqrt3^b with |p|<=64, q<=64, a in -2..2, b in 0,1 ; returns first hit description or None"""
    if abs(val) < mp.mpf('1e-30'):
        return "0"
    for a in (0, 1, -1, 2, -2):
        for b in (0, 1):
            ratio = val / (pi ** a * mp.sqrt(3) ** b)
            fr = Fraction(float(ratio)).limit_denominator(64)
            if fr.numerator == 0 or abs(fr.numerator) > 64: continue
            if abs(ratio - mp.mpf(fr.numerator) / fr.denominator) < tol * abs(ratio):
                return f"({fr.numerator}/{fr.denominator}) pi^{a} sqrt3^{b}"
    return None


print("== cross-check against lane L's published numbers (README of L, not re-run here) ==")
P = points(Zt)
p1, p2 = P["P1"], P["P2"]
chk("P1: r_b/L = 0.522632, r_c/L = 0.630391, M/M_N = 0.986952", abs(p1["x"] - mp.mpf('0.522632')) < 1e-6 and abs(p1["y"] - mp.mpf('0.630391')) < 1e-6 and abs(p1["mu"] - mp.mpf('0.986952')) < 1e-6,
    f"x={mp.nstr(p1['x'],9)} y={mp.nstr(p1['y'],9)} mu={mp.nstr(p1['mu'],9)}")
chk("P2: r_c/L = 0.637797?, mu = 0.982984 (kappa_c = a0)", abs(p2["mu"] - mp.mpf('0.982984')) < 1e-6 and abs(p2["y"] - mp.mpf('0.637797')) < 1e-6,
    f"y={mp.nstr(p2['y'],9)} mu={mp.nstr(p2['mu'],9)}")
chk("exact P1 closed form x_b = (sqrt(1+32 pi)-1)/sqrt(96 pi)", abs(p1["x"] - (mp.sqrt(1 + 32 * pi) - 1) / mp.sqrt(96 * pi)) < 1e-40)
chk("P1: S_b/S_dS = 0.273145, S_tot/S_dS = 0.670537, T_c/T_b = 0.882376",
    abs(p1["S_over_SdS"] - mp.mpf('0.273145')) < 1e-6 and abs(p1["Stot_over_SdS"] - mp.mpf('0.670537')) < 1e-6 and abs(p1["Tc_over_Tb"] - mp.mpf('0.882376')) < 1e-6)

print("\n== A5 table (puzzle Z = sqrt(32 pi/3)) ==")
for pt in ("P1", "P2", "P3", "P4"):
    print(f"  {pt}:")
    for k, v in P[pt].items():
        print(f"     {k:14s} = {mp.nstr(v, 14)}")

print("\n== identities of the flat probe (P3): exact, and they restate rho_L r_s^2 = 1 ==")
p3 = P["P3"]
chk("P3: PV/M = -8 pi/3, U/M = 1 + 8 pi/3, S/S_dS = V/V_dS^(2/3) = 8 pi/3, TS/M = F/M = G/M = 1/2 (Smarr of Schwarzschild)",
    abs(p3["PV_over_M"] + 8 * pi / 3) < 1e-40 and abs(p3["U_over_M"] - (1 + 8 * pi / 3)) < 1e-40 and abs(p3["S_over_SdS"] - 8 * pi / 3) < 1e-40 and p3["TS_over_M"] == mp.mpf(1) / 2)
p4 = P["P4"]
chk("P4: kappa_c/a0 = 8 pi - 1 exactly, T_c/T_dS = (8 pi - 1)/Z", abs(p4["kappa_over_a0"] - (8 * pi - 1)) < 1e-40)
chk("P4: M/L = (Z/4)(1 - 8 pi/3) < 0 (a negative-mass 'SdS': the puzzle horizon is a cosmological horizon of a naked-singularity spacetime)",
    p4["M_over_L"] < 0 and abs(p4["M_over_L"] - (Zt / 4) * (1 - 8 * pi / 3)) < 1e-40)
ctrl("mutation: P4 kappa_c = a0 (i.e. the puzzle object is an ordinary cosmological horizon of surface gravity a0)", abs(p4["kappa_over_a0"] - 1) < 1e-6)

print("\n== A6 closed-form scan: puzzle vs decoys (tolerance 1e-9, family (p/q) pi^a sqrt3^b) ==")
allpts = {"puzzle": points(Zt)}
for nm, zz in DECOYS.items(): allpts[nm] = points(zz)
# planted control: the scan must find 7 pi/24 and reject e
chk("scan control: recovers planted 7 pi/24", closed_form(7 * pi / 24) is not None)
ctrl("scan control: does not 'find' e", closed_form(mp.e) is not None)
ctrl("scan control: does not 'find' sqrt(1+32 pi)", closed_form(mp.sqrt(1 + 32 * pi)) is not None)
hits_true = {}
for pt in ("P1", "P2", "P3", "P4"):
    for k in P[pt]:
        h = closed_form(allpts["puzzle"][pt][k])
        hd = {nm: closed_form(allpts[nm][pt][k]) for nm in DECOYS}
        nd = sum(v is not None for v in hd.values())
        if h is not None:
            hits_true[(pt, k)] = (h, nd)
n_total = sum(len(P[pt]) for pt in P)
print(f"   quantities tested at the puzzle point: {n_total}; closed-form hits: {len(hits_true)}")
for (pt, k), (h, nd) in hits_true.items():
    print(f"     {pt} {k:14s} = {h}   (same test hits {nd}/6 decoy points)")
p12_hits = [(pt, k) for (pt, k) in hits_true if pt in ("P1", "P2")]
chk("P1/P2 (the genuine SdS a0-points): zero closed-form hits among the tested quantities", len(p12_hits) == 0, f"{len(p12_hits)} hits")
# hits at P3 are identities of construction; require each to also appear at the decoy points where the family reaches
disc = [(pt, k) for (pt, k), (h, nd) in hits_true.items() if nd == 0]
print(f"   hits absent at ALL decoys (would count under the A6 rule): {disc}")
# P3/P4 hits must be identities: PV_over_M = -s etc.  Tag them
for (pt, k), (h, nd) in hits_true.items():
    pass
# decoy hit rate on P1/P2: spurious rate calibration
tot = 0; hitsd = 0; defn = 0
for nm in DECOYS:
    for pt in ("P1", "P2"):
        for k in allpts[nm][pt]:
            if k == "T_over_TdS":
                # T/T_dS = 1/Z' by DEFINITION of the point: closed form at decoys with rational or 1/(2 pi) Z' (identity of construction)
                defn += closed_form(allpts[nm][pt][k]) is not None
                continue
            tot += 1
            hitsd += closed_form(allpts[nm][pt][k]) is not None
print(f"   spurious-hit calibration (definitional T/T_dS = 1/Z' excluded; it hits {defn} decoy points by construction): {hitsd} hits in {tot} decoy tests on P1/P2")
chk("decoy P1/P2 spurious hits are essentially absent (<= 1)", hitsd <= 1)

print("\n== P5: Bousso-Hawking normalisation existence check for kappa = a0 = H/Z ==")
Zf = float(Zt)
import numpy as np
mus = np.linspace(1e-6, 1 - 1e-9, 200001)
LNAR = 1 / (3 * np.sqrt(3))
Mv = mus * LNAR
def roots(M):
    c = np.roots([-1.0, 0.0, 1.0, -2 * M])  # -r^3 + r - 2M = 0
    rr = np.sort(c[np.isreal(c)].real)
    rr = rr[rr > 0]
    return rr
xs_list, ys_list = [], []
for mu_ in mus[::400]:
    rr = roots(mu_ * LNAR)
    xs_list.append(rr[0]); ys_list.append(rr[1])
xs_a, ys_a = np.array(xs_list), np.array(ys_list)
M_a = mus[::400] * LNAR
rstar = np.cbrt(M_a)                       # r*^3 = M L^2
fstar = 1 - 2 * M_a / rstar - rstar ** 2   # = 1 - 3 M^(2/3)
kb_f = (1 - 3 * xs_a ** 2) / (2 * xs_a)
kc_f = (3 * ys_a ** 2 - 1) / (2 * ys_a)
kb_BH = kb_f / np.sqrt(fstar); kc_BH = kc_f / np.sqrt(fstar)
chk("BH-norm: kappa_b >= sqrt(3) H on the whole family (min %.6f); kappa_c >= H (min %.6f) => no horizon has kappa = H/Z = %.4f" % (kb_BH.min(), kc_BH.min(), 1 / Zf),
    kb_BH.min() >= np.sqrt(3) - 1e-3 and kc_BH.min() >= 1 - 1e-3 and min(kb_BH.min(), kc_BH.min()) > 1 / Zf)
ctrl("mutation: BH-norm horizon with kappa < H exists", kc_BH.min() < 1 - 1e-3)
chk("f-norm: kappa_b spans (0, inf) and kappa_c spans (0, 1] on the family (so kappa = H/Z is attained once on each)",
    kb_f.min() < 1 / Zf < kb_f.max() and kc_f.min() < 1 / Zf < kc_f.max())
# dimensionless potential ratios are normalisation independent if (M, T, PV) are rescaled by the same factor
Nf = np.sqrt(fstar)
TS_over_M_f = (kb_f / (2 * np.pi)) * np.pi * xs_a ** 2 / M_a
TS_over_M_BH = (kb_BH / (2 * np.pi)) * np.pi * xs_a ** 2 / (M_a / Nf)
chk("TS/M is unchanged when M and T are both rescaled by the normalisation (identity, not a result)", np.allclose(TS_over_M_f, TS_over_M_BH, rtol=1e-12))

# first law in the BH normalisation: with E = M/N(M) the first law dE = T_BH dS does NOT hold (N depends on M); dM = T_f dS does
def Mx(x): return x * (1 - x ** 2) / 2
def Nx(x): return mp.sqrt(1 - 3 * Mx(x) ** (mp.mpf(2) / 3))
def Tf(x): return (1 - 3 * x ** 2) / (4 * pi * x)
for xv in (mp.mpf('0.2'), mp.mpf('0.4'), mp.mpf('0.52')):
    dM = mp.diff(Mx, xv); dS = 2 * pi * xv
    dE = mp.diff(lambda z: Mx(z) / Nx(z), xv)
    lhsf = dM - Tf(xv) * dS
    lhsBH = dE - (Tf(xv) / Nx(xv)) * dS
    chk(f"x = {float(xv)}: f-norm first law dM = T dS holds; BH-norm dE = T_BH dS with E = M/N fails (residual {mp.nstr(lhsBH / (dE), 3)} of dE)",
        abs(lhsf) < 1e-15 and abs(lhsBH / dE) > 1e-3)

print("\n== structure: every P1/P2 number is a generic function of K = kappa/H (no feature at K = 1/Z) ==")
import sympy as sp
Ks = sp.symbols('K', positive=True)
sK = sp.sqrt(Ks ** 2 + 3)
xK = (sK - Ks) / 3
yK = (sK + Ks) / 3
forms = {
    "P1 C_P/S": -2 * (1 - 3 * xK ** 2) / (1 + 3 * xK ** 2),
    "P2 C_P/S": 2 * (3 * yK ** 2 - 1) / (3 * yK ** 2 + 1),
    "P1 PV/M": -xK ** 2 / (1 - xK ** 2),
    "P1 TS/M": (1 - 3 * xK ** 2) / (2 * (1 - xK ** 2)),
    "P1 G/M": (1 + xK ** 2) / (2 * (1 - xK ** 2)),
}
for k, v in forms.items():
    print(f"   {k:10s} = {sp.simplify(v)}")
chk("C_P/S at kappa_b = K equals -2K/sqrt(K^2+3) and at kappa_c = K equals +2K/sqrt(K^2+3) for EVERY K (so at K = 1/Z: -/+ 2/sqrt(1+32 pi) = -/+0.19849)",
    sp.simplify(forms["P1 C_P/S"] + 2 * Ks / sK) == 0 and sp.simplify(forms["P2 C_P/S"] - 2 * Ks / sK) == 0
    and abs(float((2 * Ks / sK).subs(Ks, 1 / sp.sqrt(32 * sp.pi / 3))) - 2 / float(sp.sqrt(1 + 32 * sp.pi))) < 1e-12)
chk("the G/M = 1/2 - PV/M and TS/M = 1/2 + PV/M identities hold at P1 (Smarr; not a result)",
    sp.simplify(forms["P1 G/M"] - (sp.Rational(1, 2) - forms["P1 PV/M"])) == 0 and sp.simplify(forms["P1 TS/M"] - (sp.Rational(1, 2) + forms["P1 PV/M"])) == 0)
print(f"\n== TOTAL: {PASS} pass, {FAIL} fail; controls rejected {CO}, not rejected {CB} ==")
sys.exit(0 if FAIL == 0 and CB == 0 else 1)
