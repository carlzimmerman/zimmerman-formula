#!/usr/bin/env python3
"""G3 -- embedding of U(1)_Y in a simple group: what is forced (a ratio) and what is not (the coupling). Pre-registered E1-E4.
Run: python3 g3_gut_embedding_ratios.py [MUTATE]   (MUTATE: drop u^c from the 10, an INCOMPLETE SU(5) multiplet; the 3/8 checks must FAIL; exits 1. See Amendment 1: the original "drop the whole 10" mutation was ill-designed because 5bar alone is complete)"""
import sys
import sympy as sp

MUT = len(sys.argv) > 1 and sys.argv[1] == "MUTATE"
checks = []
def chk(name, ok, info=""):
    checks.append((name, bool(ok)))
    print(f"[{'PASS' if ok else 'FAIL'}] {name} {info}")
R = sp.Rational

# ---------- fields: (name, colour dim, SU(2) dim, Y)  -- left-handed Weyl, Q = T3 + Y
dbar = ("dc", 3, 1, R(1, 3)); Lf = ("L", 1, 2, -R(1, 2))                       # 5bar
Qf = ("Q", 3, 2, R(1, 6)); uc = ("uc", 3, 1, -R(2, 3)); ec = ("ec", 1, 1, R(1, 1))   # 10
nuc = ("nuc", 1, 1, R(0, 1))                                                    # singlet (16 of SO(10))
five = [("d5", 3, 1, -R(1, 3)), ("l5", 1, 2, R(1, 2))]                          # 5 of SU(5) (E6 vector-like 10 = 5 + 5bar)
fivebar = [dbar, Lf]

def trace_T3sq(fs):
    # SU(2) multiplet of dim d has T3 eigenvalues -(d-1)/2 ... (d-1)/2 ; multiplicity = colour dim
    tot = 0
    for _, c, d, _y in fs:
        tot += c*sum((R(d - 1, 2) - i)**2 for i in range(d))
    return tot
def trace_Ysq(fs):
    return sum(c*d*y**2 for _, c, d, y in fs)
def trace_Qsq(fs):
    tot = 0
    for _, c, d, y in fs:
        tot += c*sum((R(d - 1, 2) - i + y)**2 for i in range(d))
    return tot
def trace_T3Y(fs):
    return sum(c*sum((R(d - 1, 2) - i)*y for i in range(d)) for _, c, d, y in fs)
def sin2(fs):
    return trace_T3sq(fs)/trace_Qsq(fs)

tenplet = [Qf, uc, ec]
gen_SU5 = fivebar + ([Qf, ec] if MUT else tenplet)             # 5bar + 10   (MUTATE: u^c removed -> incomplete multiplet)
gen_SO10 = gen_SU5 + [nuc]                                     # 16
ten_vl = five + fivebar                                        # E6: 27 = 16 + 10 + 1 ; 10 -> 5 + 5bar
gen_E6 = gen_SO10 + ten_vl + [nuc]

print("      Tr T3^2 / Tr Y^2 / Tr Q^2 for the SU(5) generation:", trace_T3sq(gen_SU5), trace_Ysq(gen_SU5), trace_Qsq(gen_SU5))
chk("E1a SU(5) (5bar+10): Tr T3 Y = 0 and Tr Q^2 = Tr T3^2 + Tr Y^2", trace_T3Y(gen_SU5) == 0 and trace_Qsq(gen_SU5) == trace_T3sq(gen_SU5) + trace_Ysq(gen_SU5))
chk("E1b SU(5): Tr Y^2/Tr T3^2 = 5/3, sin^2 theta_W = Tr T3^2/Tr Q^2 = 3/8", sin2(gen_SU5) == R(3, 8), f"sin^2={sin2(gen_SU5)}")
chk("E1c SO(10) 16: sin^2 = 3/8", sin2(gen_SO10) == R(3, 8), f"sin^2={sin2(gen_SO10)}")
chk("E1d E6 27: sin^2 = 3/8", sin2(gen_E6) == R(3, 8), f"sin^2={sin2(gen_E6)}")
# the coupling relation itself: single coupling g => g_Y^2 Tr Y^2 = g_2^2 Tr T3^2
g2s, gYs = sp.symbols("g2s gYs", positive=True)
gY_sq = sp.solve(sp.Eq(gYs*trace_Ysq(gen_SU5), g2s*trace_T3sq(gen_SU5)), gYs)[0]
chk("E1e g_Y^2 = (3/5) g_2^2 (GUT normalization factor 5/3 in alpha_1)", sp.simplify(gY_sq - R(3, 5)*g2s) == 0, f"g_Y^2 = {gY_sq} g_2^2")
print("      NOTE: this fixes g_Y/g_2 (ratio). The common value g_GUT is not touched by any trace.")

# ---------- E2: Pati-Salam, independent couplings
g4, gL, gR = sp.symbols("g4 gL gR", positive=True)
T15 = sp.diag(1, 1, 1, -3)/(2*sp.sqrt(6))
chk("E2a SU(4) generator T15 = diag(1,1,1,-3)/(2 sqrt6) has Tr_4 T15^2 = 1/2 (canonical)", sp.simplify((T15**2).trace() - R(1, 2)) == 0)
# (B-L)/2 on (q,q,q,l) = (1/6,1/6,1/6,-1/2) = c*T15 ; c:
c_BL = sp.simplify((R(1, 6))/T15[0, 0])
chk("E2b (B-L)/2 = sqrt(2/3) T15", sp.simplify(c_BL - sp.sqrt(R(2, 3))) == 0)
gY_ps = sp.sqrt(1/(1/gR**2 + R(2, 3)/g4**2))
sin2_ps = sp.simplify(gY_ps**2/(gL**2 + gY_ps**2))
print("      Pati-Salam sin^2 theta_W (independent couplings) =", sin2_ps)
chk("E2c Pati-Salam at g4 = gL = gR gives 3/8", sp.simplify(sin2_ps.subs({g4: sp.Symbol("g", positive=True), gL: sp.Symbol("g", positive=True), gR: sp.Symbol("g", positive=True)}) - R(3, 8)) == 0)
val_a = sin2_ps.subs({g4: 1, gL: 1, gR: 1}); val_b = sin2_ps.subs({g4: 2, gL: 1, gR: 1}); val_c = sin2_ps.subs({g4: 1, gL: 1, gR: 3})
chk("E2d without imposing equal couplings the ratio is free (3 distinct values at 3 coupling ratios)", len({sp.nsimplify(val_a), sp.nsimplify(val_b), sp.nsimplify(val_c)}) == 3, f"{[float(v) for v in (val_a, val_b, val_c)]}")
chk("E2e sin^2 theta_W is homogeneous of degree 0 in (g4,gL,gR): the overall coupling scale drops out", sp.simplify(sin2_ps.subs({g4: sp.Symbol('l', positive=True)*g4, gL: sp.Symbol('l', positive=True)*gL, gR: sp.Symbol('l', positive=True)*gR}) - sin2_ps) == 0)

# ---------- E3: one-loop b_i from field content
def b_sm():
    ngen = 3
    # SU(3): -11 + 2/3 * sum_Weyl T ; T=1/2 per (anti)triplet: per gen Q(2 triplets), U, D
    b3 = -11 + R(2, 3)*ngen*(2*R(1, 2) + R(1, 2) + R(1, 2))
    b2 = -R(22, 3) + R(2, 3)*ngen*(3*R(1, 2) + R(1, 2)) + R(1, 3)*R(1, 2)
    sumY2 = sum(c*d*y**2 for _, c, d, y in [Qf, uc, dbar, Lf, ec])
    b1 = R(3, 5)*(R(2, 3)*ngen*sumY2 + R(1, 3)*2*R(1, 4))
    return (b1, b2, b3)
def b_mssm():
    ngen = 3
    sumY2 = sum(c*d*y**2 for _, c, d, y in [Qf, uc, dbar, Lf, ec])
    b3 = -9 + ngen*(2*R(1, 2) + R(1, 2) + R(1, 2))
    b2 = -6 + ngen*(3*R(1, 2) + R(1, 2)) + 2*R(1, 2)
    b1 = R(3, 5)*(ngen*sumY2 + 2*2*R(1, 4))
    return (b1, b2, b3)
chk("E3a SM  b = (41/10, -19/6, -7)", b_sm() == (R(41, 10), -R(19, 6), -7), str(b_sm()))
chk("E3b MSSM b = (33/5, 1, -3)", b_mssm() == (R(33, 5), 1, -3), str(b_mssm()))
print("      NOTE: b_i are rational numbers fixed by representation content; they fix the SLOPES d alpha^-1/d ln mu, never an additive constant.")

# ---------- E4: alpha_em relation at unification
a1i, a2i, aGi = sp.symbols("a1i a2i aGi", positive=True)
alpha_em_inv = R(5, 3)*a1i + a2i
at_unif = sp.simplify(alpha_em_inv.subs({a1i: aGi, a2i: aGi}))
chk("E4a alpha_em^-1 = (5/3) alpha_1^-1 + alpha_2^-1 -> (8/3) alpha_G^-1 : alpha_em(M_G) = (3/8) alpha_G", sp.simplify(at_unif - R(8, 3)*aGi) == 0)
chk("E4b sin^2 theta_W = alpha_em/alpha_2 = (5/3 alpha_1^-1 + alpha_2^-1)^-1 / alpha_2 -> 3/8 at unification", sp.simplify((1/alpha_em_inv.subs({a1i: aGi, a2i: aGi}))*aGi - R(3, 8)) == 0)
print("      scale statement: these hold at M_G (~1e16 GeV, model-dependent); not at the Thomson limit.")

nfail = sum(1 for _, ok in checks if not ok)
print(f"\nSUMMARY: {len(checks)-nfail}/{len(checks)} checks pass" + (" [MUTATE]" if MUT else ""))
sys.exit(1 if nfail else 0)
