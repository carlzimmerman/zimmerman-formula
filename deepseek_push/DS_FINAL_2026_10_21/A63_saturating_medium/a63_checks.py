#!/usr/bin/env python3
"""
A63_saturating_medium -- WHAT MEDIUM PRODUCES THE SATURATING VACUUM TERM,
and does nature pick n=1 or n=2?

Run:  python3 a63_checks.py               (31/31 PASS, exit 0)
      python3 a63_checks.py --mutate      (the identified medium is replaced by a
                                           saturating dielectric: the identification
                                           checks must FAIL, 24/31)
      python3 a63_checks.py --mutate-n2   (replaced by the n=2 element: 23/31)

Deterministic. stdlib + numpy + sympy. No network. <= 60 s.

Units: algebra in units of a0 (a0 = 1) where convenient; SI numbers use
a0 = 9.36e-11 m s^-2 (BRIEF section 4, canonical footing).

The one structural choice: the identified medium is the one-sided
single-occupancy (Langmuir) gate driven by an activity.  --mutate replaces it
with the centrosymmetric saturating dielectric A = C tanh(g/g_c), which is the
nearest rival in the same "response saturates" class.
"""
import sys
import json
import math
import numpy as np
import sympy as sp

# Which medium is "the identified one"?  langmuir (default) | tanh | n2
MEDIUM = "langmuir"
if "--mutate-n2" in sys.argv:
    MEDIUM = "n2"
elif "--mutate" in sys.argv:
    MEDIUM = "tanh"
MUTATE = MEDIUM != "langmuir"

# ---------------------------------------------------------------------------
# Constants (BRIEF section 4)
# ---------------------------------------------------------------------------
A0 = 9.36e-11                  # m s^-2
C_LIGHT = 2.99792458e8         # m s^-1
KPC = 3.0856775814913673e19    # m
AU = 1.495978707e11            # m
G_NEWT = 6.67430e-11           # m^3 kg^-1 s^-2
MSUN = 1.98892e30              # kg

CHECKS = []


def ck(cid, ok, value, threshold, note=""):
    ok = bool(ok)
    CHECKS.append({"id": cid, "pass": ok, "value": float(value),
                   "threshold": float(threshold), "note": note})
    tail = f"  # {note}" if note else ""
    print(f"{cid} {'PASS' if ok else 'FAIL'} {value} {threshold}{tail}")


# ---------------------------------------------------------------------------
# Symbols
# ---------------------------------------------------------------------------
g, a0, A, u, K, th, s, C, x, gn, E = sp.symbols(
    'g a0 A u K theta s C x g_N E', positive=True)
U = sp.symbols('U', positive=True)
c2, c3 = sp.symbols('c_2 c_3', real=True)
Nmax = sp.symbols('N_max', positive=True)


# ---------------------------------------------------------------------------
# The identified medium.
#   Langmuir (default): theta = g/(g+a0), A = a0 theta
#   --mutate:           A = a0 tanh(g/a0)  (centrosymmetric dielectric, C = g_c)
#   --mutate-n2:        A = (a0/2) th,  4x(1-th) = th(2-th)   (self-depleting)
# ---------------------------------------------------------------------------
def isotherm(xv):
    """theta as a function of the reduced drive x = g/a0.

    langmuir : th = x/(1+x)                    the one-sided lattice
    tanh     : th = tanh(x)                     the centrosymmetric dielectric
    n2       : 4x(1-th) = th(2-th)              the self-depleting element
    """
    if MEDIUM == "tanh":
        return math.tanh(xv)
    if MEDIUM == "n2":
        b = 2.0 + 4.0 * xv
        return 8.0 * xv / (b + math.sqrt(b * b - 16.0 * xv))   # stable form
    return xv / (1.0 + xv)


def resp(gv, a0v=A0):
    """A(g), the medium's share of the field.  Capacity a0, except n=2 (a0/2)."""
    cap = a0v / 2.0 if MEDIUM == "n2" else a0v
    return cap * isotherm(gv / a0v)


def gN_of(gv, a0v=A0):
    return gv - resp(gv, a0v)


def resp_n2(gv, a0v=A0):
    ah = a0v / 2.0
    return 2.0 * gv * ah / (gv + ah + math.sqrt(gv * gv + ah * ah))


def gN_n2(gv, a0v=A0):
    return gv - resp_n2(gv, a0v)


def g_from_gN_n1(y, a0v=A0):
    return (y * a0v / 2.0) * (1.0 + math.sqrt(1.0 + 4.0 / y))


def g_from_gN_n2(y, a0v=A0):
    return a0v * math.sqrt(y * y + y)


def skew_binomial(thv, ns=1.0):
    """skew of delta-theta for N_s independent binomial gates, fraction units."""
    return (1.0 - 2.0 * thv) / math.sqrt(ns * thv * (1.0 - thv))


# ===========================================================================
# K1 -- the identity: A = a0 theta, gN = g theta, 1/A = 1/g + 1/a0
# ===========================================================================
A_can = a0 * g / (g + a0)
th_can = g / (g + a0)
gN_can = g - A_can
k1 = [
    sp.simplify(A_can - a0 * th_can),
    sp.simplify(gN_can - g * th_can),
    sp.simplify(A_can + gN_can - g),
    sp.simplify(1 / A_can - (1 / g + 1 / a0)),
    sp.simplify(g - (a0 + g) * th_can),
]
ck("K1", all(sp.simplify(r) == 0 for r in k1),
   max(abs(float(r)) for r in k1), 1e-30,
   "A=a0*th, gN=g*th, A+gN=g, 1/A=1/g+1/a0, g=(a0+g)*th (sympy remainders)")

# ===========================================================================
# K2 -- W is the integral of the isotherm: K W'(u) = g
# ===========================================================================
# The closed form is fixed by the fundamental theorem (avoid sympy's branch cut
# at U > a0): d/du of the candidate must equal the integrand and W(0)=W'(0)=0.
KW_target = a0 ** 2 * (-u / a0 - sp.log(1 - u / a0))
r_deriv = sp.simplify(sp.diff(KW_target, u) - a0 * u / (a0 - u))
r_w0 = sp.simplify(KW_target.subs(u, 0))
r_dw0 = sp.simplify(sp.diff(KW_target, u).subs(u, 0))
# numerical quadrature cross-check at three points (a0 = 1)
quad = []
for uv in (0.3, 0.7, 0.95):
    xs_ = np.linspace(0.0, uv, 200001)
    fs = np.where(xs_ < 1.0, xs_ / (1.0 - xs_), 0.0)
    val = float(np.trapz(fs, xs_))
    quad.append(abs(val - (-uv - math.log(1.0 - uv))))
r_quad = max(quad)
ck("K2", r_deriv == 0 and r_w0 == 0 and r_dw0 == 0 and r_quad < 1e-9,
   float(r_quad), 1e-9,
   "K W = int_0^u a0 U/(a0-U) dU = a0^2[-u/a0-ln(1-u/a0)]; W(0)=W'(0)=0; "
   "quadrature agrees to 1e-9")

# ===========================================================================
# K3 -- the converse: the log form IMPLIES the law (one condition, not two)
# ===========================================================================
Wform = a0 ** 2 * (-A / a0 - sp.log(1 - A / a0))
gsol = sp.solve(sp.Eq(a0 * A / (a0 - A), g), A)[0]
r3 = sp.simplify(g - a0 * A / (a0 - A))
ck("K3", sp.simplify(sp.diff(Wform, A) - a0 * A / (a0 - A)) == 0,
   float(abs(sp.simplify(sp.diff(Wform, A) - a0 * A / (a0 - A)))), 1e-30,
   "g = K W'(u) with u=A inverts to A=a0 g/(g+a0) and gN=g^2/(g+a0): "
   "the log W and the law are ONE condition")

# ===========================================================================
# K4 -- W's expansion: coefficient of u^n is 1/n (in units a0 = 1)
# ===========================================================================
t = sp.symbols('t', positive=True)
Wser = sp.series(-t - sp.log(1 - t), t, 0, 8).removeO().expand()
coeffs = [sp.nsimplify(Wser.coeff(t, n)) for n in range(2, 8)]
targets = [sp.Rational(1, n) for n in range(2, 8)]
worst = max(abs(float(c - tg)) for c, tg in zip(coeffs, targets))
ck("K4", worst < 1e-25, worst, 1e-25,
   "K W/a0^2 = sum_{n>=2} u^n/(n a0^n): coefficients 1/2,1/3,1/4,1/5,1/6,1/7")

# ===========================================================================
# K5 -- the n=2 potential differs first at u^4, by a factor 2
# ===========================================================================
W2 = sp.integrate(A * (a0 - A) / (a0 - 2 * A), A)
W2ser = sp.series(W2, A, 0, 6).removeO().expand()
W1ser = sp.series(a0 ** 2 * (-A / a0 - sp.log(1 - A / a0)), A, 0, 6).removeO().expand()
cw1 = [sp.simplify(W1ser.coeff(A, n)) for n in range(2, 6)]
cw2 = [sp.simplify(W2ser.coeff(A, n)) for n in range(2, 6)]
# ratios cw2/cw1 must be 1,1,2,4
ratios = [sp.simplify(cw2[i] / cw1[i]) for i in range(4)]
k5_ratio4 = float(ratios[2])
k5_ratio5 = float(ratios[3])
ck("K5", abs(k5_ratio4 - 2) < 1e-12 and abs(k5_ratio5 - 4) < 1e-12,
   k5_ratio4, 1e-12,
   "W_n2/W_n1 = 1,1,2,4 at u^2..u^5: the n=2 potential is NOT 'only u^2' -- "
   "it agrees through u^3 and differs first at u^4 (factor 2)")

# ===========================================================================
# K6 -- tanh dielectric: c2 = 0 exactly, c3 = -1/3, deep exponent 3
# ===========================================================================
xs = sp.symbols('xs', positive=True)
tanh_ser = sp.series(sp.tanh(xs), xs, 0, 6).removeO().expand()
c2_tanh = sp.simplify(tanh_ser.coeff(xs, 2))
c3_tanh = sp.simplify(tanh_ser.coeff(xs, 3))
# deep law with C = g_c: gN = gc(x - tanh x) -> gc x^3/3
gN_tanh = sp.series(xs - sp.tanh(xs), xs, 0, 6).removeO().expand()
lead_tanh = sp.simplify(gN_tanh.coeff(xs, 3))
# numeric log-log slope at small x
xv = 1e-4
val1 = (xv - math.tanh(xv))
xv2 = 1e-5
val2 = (xv2 - math.tanh(xv2))
slope_tanh = (math.log(val2) - math.log(val1)) / (math.log(xv2) - math.log(xv))
ck("K6", c2_tanh == 0 and abs(float(c3_tanh) + sp.Rational(1, 3)) < 1e-15
   and abs(slope_tanh - 3) < 1e-3,
   slope_tanh, 1e-3,
   "tanh: c2=0 (odd), c3=-1/3; gN=gc x^3/3, deep exponent 3 -- no g^2 term, "
   "no MOND")

# ===========================================================================
# K7 -- Langevin dielectric: c2 = 0, c3 = -1/15, deep exponent 3
# ===========================================================================
L = sp.coth(xs) - 1 / xs
Lser = sp.series(3 * L, xs, 0, 6).removeO().expand()
c2_lan = sp.simplify(Lser.coeff(xs, 2))
c3_lan = sp.simplify(Lser.coeff(xs, 3))
gN_lan = sp.series(3 * L - xs, xs, 0, 6).removeO().expand()
lead_lan = sp.simplify(-gN_lan.coeff(xs, 3))
ck("K7", c2_lan == 0 and abs(float(c3_lan) + sp.Rational(1, 15)) < 1e-15
   and abs(float(lead_lan) - sp.Rational(1, 15)) < 1e-15,
   float(c3_lan), 1e-15,
   "Langevin: 3L = x - x^3/15 + ...; c2=0, c3=-1/15; gN = gc x^3/15, "
   "deep exponent 3")

# ===========================================================================
# K8 -- the admissibility theorem: ONE number c2 fixes affinity AND capacity
#       C = s = -c2 a0.  The Langmuir c2 = -1 gives C = a0.
# ===========================================================================
f = xs + c2 * xs ** 2 + c3 * xs ** 3
A_gen = C * f.subs(xs, g / s)
gN_gen = sp.series(g - A_gen, g, 0, 3).removeO().expand()
lin = sp.simplify(gN_gen.coeff(g, 1))
quad = sp.simplify(gN_gen.coeff(g, 2))
# impose lin = 0 -> C = s ; then quad = 1/a0 -> s = -c2 a0
s_sol = sp.solve(sp.Eq(quad.subs(C, s), 1 / a0), s)[0]
k8_ok = (sp.simplify(lin.subs(C, s)) == 0
         and sp.simplify(s_sol + c2 * a0) == 0)
 # the Langmuir (c2 = -1) must give s = a0
s_lang = float(sp.simplify(s_sol.subs(c2, -1) / a0))
ck("K8", bool(k8_ok) and abs(s_lang - 1) < 1e-15, s_lang, 1e-30,
   "general saturating medium: no linear term => C=s; deep coefficient => "
   "s=C=-c2*a0 (Langmuir c2=-1 => a0).  Capacity is NOT free")

# ===========================================================================
# K9 -- the biased (non-centrosymmetric) tanh: the strongest dielectric rival.
#       Matches the deep limit exactly, but capacity <= a0/2 and R <= 2/3.
# ===========================================================================
w = sp.symbols('w', positive=True)
Ec, P = sp.symbols('E_c P', positive=True)
A_bt = P * (sp.tanh(xs / Ec + w) - sp.tanh(w))
c1_bt = sp.simplify(sp.diff(A_bt, xs).subs(xs, 0))
c2_bt = sp.simplify(sp.diff(A_bt, xs, 2).subs(xs, 0) / 2)
P_sol = sp.solve(sp.Eq(c1_bt, 1), P)[0]
Ec_sol = sp.solve(sp.Eq(sp.simplify(c2_bt.subs(P, P_sol)), -1 / a0), Ec)[0]
uu = sp.symbols('uu', positive=True)
# x -> oo : tanh -> 1, so A_inf = P (1 - tanh w) with P = E_c cosh^2 w
Ainf_expr = sp.simplify((P_sol * (1 - sp.tanh(w))).subs(Ec, Ec_sol))
Ainf_u = sp.simplify(Ainf_expr.subs(w, sp.atanh(uu)))
cap_max = float(sp.simplify((Ainf_u / a0).subs(uu, 1)))
c3_bt = sp.simplify(sp.diff(A_bt, xs, 3).subs(xs, 0) / 6)
c3_bt = sp.simplify(c3_bt.subs(P, P_sol).subs(Ec, Ec_sol))   # sequential!
R_bt = sp.simplify(c3_bt * 1 / ((-1 / a0) ** 2))
R_bt_u = sp.simplify(R_bt.subs(w, sp.atanh(uu)))
R_max = float(sp.simplify(R_bt_u.subs(uu, 1)))
ck("K9", abs(cap_max - 0.5) < 1e-12 and abs(R_max - 2.0 / 3.0) < 1e-12,
   cap_max, 1e-12,
   "biased tanh (c2=-1/a0 forced, exact deep limit): capacity = a0*u/(1+u) "
   "<= a0/2, R = 1-1/(3u^2) <= 2/3 < 1 -- cannot reach capacity a0")

# ===========================================================================
# K10 -- Born-Infeld: caps the DRIVE, anti-screens at every field, exponent 1
# ===========================================================================
gBI = gn / sp.sqrt(1 + gn ** 2 / E ** 2)
ABI = sp.simplify(gBI - gn)          # 1/sqrt(1+z) - 1 < 0 for all z > 0
gBI_series = sp.series(gBI, gn, 0, 5).removeO().expand()
ABI_series = sp.series(ABI, gn, 0, 5).removeO().expand()
lead_g_BI = sp.simplify(gBI_series.coeff(gn, 1))       # = 1 : Newtonian
lead_A_BI = sp.simplify(ABI_series.coeff(gn, 3))       # = -1/(2E^2): cubic, no g^2
cap_BI = sp.limit(gBI, gn, sp.oo)
k10_val = float(ABI.subs({gn: a0, E: a0}) / a0)
# max relative deviation from the law over gN/a0 in [1e-3, 10], with E_max = a0
mx_bi = 0.0
for ly in np.linspace(math.log(1e-3), math.log(10.0), 20000):
    gnv = math.exp(ly)
    gb = gnv / math.sqrt(1.0 + gnv ** 2)
    gl = (gnv / 2.0) * (1.0 + math.sqrt(1.0 + 4.0 / gnv))
    mx_bi = max(mx_bi, abs(gb - gl) / gl)
ck("K10", lead_g_BI == 1
   and sp.simplify(lead_A_BI + 1 / (2 * E ** 2)) == 0 and cap_BI == E
   and k10_val < 0 and abs(mx_bi - 0.9689) < 1e-3,
   k10_val, 1e-12,
   "BI: g=gN/sqrt(1+gN^2/E^2); g linear in gN (Newtonian, no g^2 term), "
   "A=-gN^3/(2E^2) NEGATIVE everywhere, g->E: -0.2929a0 at gN=a0")

# ===========================================================================
# K11 -- BI has the opposite topology: it caps g, the theory caps A
# ===========================================================================
gn_big = 1e3 * A0
g_BI_big = gn_big / math.sqrt(1 + (gn_big / A0) ** 2)
A_th_big = resp(1e9 * A0, A0)          # theory at huge drive
k11_bi = g_BI_big / A0                  # -> 1 (=E/a0), g is capped
k11_th = A_th_big / A0                  # -> 1, A is capped (g is not)
g_th_big = 1e9 * A0
ck("K11", abs(k11_bi - 1) < 1e-5 and abs(k11_th - 1) < 1e-6
   and g_th_big / A0 > 1e8,
   k11_bi, 1e-5,
   "at gN=1e3 a0: BI g=0.9999995 E (g capped); theory at g=1e9 a0 still has "
   "g=1e9 a0 and A=0.999999 a0 (A capped) -- opposite topology")

# ===========================================================================
# K12 -- mass action with LINEAR adsorption gives the Langmuir isotherm
# ===========================================================================
ka, kd = sp.symbols('k_a k_d', positive=True)
th_sol = sp.solve(sp.Eq(ka * g * (1 - th), kd * th), th)[0]
r12 = sp.simplify(th_sol - g / (g + kd / ka))
ck("K12", r12 == 0, float(abs(r12)), 1e-30,
   "k_a g (1-th) = k_d th  =>  th = g/(g+s), s=k_d/k_a: one occupant, "
   "adsorption linear in the drive")

# ===========================================================================
# K13 -- the grand-canonical route gives the same isotherm
# ===========================================================================
z = sp.symbols('z', positive=True)
th_gc = z / (1 + z)
r13 = sp.simplify(th_gc.subs(z, g / a0) - g / (g + a0))
ck("K13", r13 == 0, float(abs(r13)), 1e-30,
   "Z=1+z, th=z/(1+z), activity z=g/a0 => same th: equilibrium and kinetic "
   "routes agree")

# ===========================================================================
# K14 -- capacity per site: q = a0/N_s; the SITE's saturation field is a0
# ===========================================================================
Ns, q = sp.symbols('N_s q', positive=True)
C_tot = Ns * q
q_sol = sp.solve(sp.Eq(C_tot, a0), q)[0]
law_site = sp.simplify((Ns * q_sol) * (g / (g + a0)) - a0 * g / (g + a0))
k14_val = float(sp.simplify((q_sol / a0).subs(Ns, 100)))
ck("K14", law_site == 0 and sp.simplify(q_sol * Ns - a0) == 0
   and abs(k14_val * 100 - 1) < 1e-15,
   k14_val, 1e-30,
   "capacity per site q = a0/N_s (not predicted, fixes the gate density); "
   "affinity s = a0 = the site's own half-occupancy field; C/s = 1")

# ===========================================================================
# K15 -- multi-occupancy (BET/ladder): capacity N_max a0, gN < 0 at small g
# ===========================================================================
th_lad = (z + 2 * z ** 2) / (1 + z + z ** 2)     # N_max = 2, U = 0
gN_lad = sp.series(g - 2 * a0 * th_lad.subs(z, g / a0), g, 0, 2).removeO()
lin_lad = sp.simplify(gN_lad.coeff(g, 1))
k15_val = float(gN_lad.subs(g, sp.Rational(1, 1000) * a0) / a0)
ck("K15", lin_lad == -1, k15_val, 1e-4,
   "two occupants per site: linear coefficient 1-N_max = -1 => gN = -g at "
   "small g (anti-gravity); gN(1e-3 a0)/a0 = -9.99e-4 -- excluded")

# ===========================================================================
# K16 -- a thermal two-level gate with LINEAR coupling fails at g = 0
# ===========================================================================
lam, kT = sp.symbols('lambda kT', positive=True)
th_F = 1 / (1 + sp.exp(-lam * g / kT))
k16_val = float(sp.limit(th_F, g, 0))
# no real pole for the Fermi gate; the Langmuir has one at g = -a0
fermi_pole = sp.solve(sp.Eq(sp.denom(sp.together(th_F)), 0), g)
k16_nopole = all(sp.im(p) != 0 for p in fermi_pole)
ck("K16", abs(k16_val - 0.5) < 1e-15 and k16_nopole,
   k16_val, 1e-12,
   "Fermi gate (linear coupling H=-lam g sigma_z): A(0)=a0/2 != 0 and no "
   "real pole; the Langmuir has A(0)=0 and a pole at g=-a0")

# ===========================================================================
# K17 -- analytic structure: n=1 pole at -a0, n=2 branch points at +-i a0/2
# ===========================================================================
A_n2_sym = g + a0 / 2 - sp.sqrt(g ** 2 + a0 ** 2 / 4)
gr = sp.Symbol('g_r', real=True)          # real axis: where the pole is
gz = sp.Symbol('g_z')                     # unrestricted: where the branch pts are
pole1 = sp.solve(sp.Eq(sp.denom(A_can).subs(g, gr), 0), gr)
branch = sp.solve(sp.Eq(gz ** 2 + a0 ** 2 / 4, 0), gz)
k17_pole = [complex(sp.N(p.subs(a0, 1))) for p in pole1]
k17_branch = [complex(sp.N(b.subs(a0, 1))) for b in branch]
ck("K17", abs(k17_pole[0].real + 1) < 1e-12 and abs(k17_pole[0].imag) < 1e-15
   and len(k17_branch) == 2
   and all(abs(abs(b.imag) - 0.5) < 1e-12 and abs(b.real) < 1e-15
           for b in k17_branch),
   abs(k17_branch[0].imag), 1e-12,
   "n=1: pole at g=-a0 (positive-mixture/Stieltjes class); n=2: branch points "
   "+-i a0/2 (no positive mixture of two-state gates)")

# ===========================================================================
# K18 -- the skew of the occupancy noise: (1-2 theta)/sqrt(N_s theta(1-theta))
# ===========================================================================
# binomial third moment of the fraction: mu3 = th(1-th)(1-2th)/N_s^2,
# sigma^3 = [th(1-th)/N_s]^{3/2}
thv = sp.symbols('theta_v', positive=True)
mu3 = thv * (1 - thv) * (1 - 2 * thv) / Ns ** 2
sig3 = (thv * (1 - thv) / Ns) ** sp.Rational(3, 2)
skew_sym = sp.simplify(mu3 / sig3)
skew_target = (1 - 2 * thv) / sp.sqrt(Ns * thv * (1 - thv))
r18 = sp.simplify(skew_sym - skew_target)
# values at g = a0/2, with theta taken FROM THE MEDIUM (not from the formula)
g_half = 0.5 * A0
th1_half = isotherm(g_half / A0)                 # medium's occupancy
th2_half = 2 * resp_n2(g_half, A0) / A0
sk1_half = skew_binomial(th1_half)
sk2_half = skew_binomial(th2_half)
ck("K18", r18 == 0 and abs(sk1_half - 0.70710678) < 1e-6
   and abs(sk2_half + 0.34831) < 1e-4,
   sk1_half, 1e-6,
   "skew = (1-2th)/sqrt(N_s th(1-th)) exactly; at g=a0/2: n1=+0.707107, "
   "n2=-0.348327 (opposite signs)")

# ===========================================================================
# K19 -- the flip: theta=1/2 at g=a0 (n=1) and g=3a0/8 (n=2)
# ===========================================================================
g_flip1 = sp.solve(sp.Eq(g / (g + a0), sp.Rational(1, 2)), g)[0]
# n=2: 4x(1-th)=th(2-th) at th=1/2  ->  4x/2 = 3/4
x_flip2 = sp.solve(sp.Eq(4 * x * (1 - sp.Rational(1, 2)),
                         sp.Rational(1, 2) * (2 - sp.Rational(1, 2))), x)[0]
k19_ratio = float(g_flip1 / a0 / x_flip2)
# the flip is located FROM THE MEDIUM: bisect theta(g) = 1/2
lo, hi = 0.05, 4.0
for _ in range(200):
    mid = 0.5 * (lo + hi)
    if isotherm(mid) < 0.5:
        lo = mid
    else:
        hi = mid
flip_med = 0.5 * (lo + hi)
# and the n=2 flip from the closed form
lo, hi = 0.30, 0.45
for _ in range(200):
    mid = 0.5 * (lo + hi)
    thm = 2 * resp_n2(mid * A0, A0) / A0
    if thm < 0.5:
        lo = mid
    else:
        hi = mid
ck("K19", abs(k19_ratio - 8.0 / 3.0) < 1e-12 and abs(0.5 * (lo + hi) - 0.375) < 1e-12
   and abs(flip_med - 1.0) < 1e-10,
   flip_med, 1e-10,
   "skew zero at g=a0 (n1, from the medium) and g=3a0/8=0.375a0 (n2); "
   "ratio 8/3=2.667")

# ===========================================================================
# K20 -- opposite signs on the whole window (0.375, 1) a0
# ===========================================================================
window = [0.40, 0.50, 0.65, 0.80, 0.95]
sgn_ok = True
worst_win = 1e9
for xv_ in window:
    gv = xv_ * A0
    s1 = skew_binomial(isotherm(xv_))          # from the medium
    s2 = skew_binomial(2 * resp_n2(gv, A0) / A0)
    if not (s1 > 0 > s2):
        sgn_ok = False
    worst_win = min(worst_win, abs(s1), abs(s2))
ck("K20", sgn_ok, worst_win, 1e-12,
   "on g/a0 in (0.375,1): n1 skew > 0 > n2 skew at every probe "
   "(min |skew| over the window = %.4f)" % worst_win)

# ===========================================================================
# K21 -- the excluded candidate: rotation-curve curvature / max split
# ===========================================================================
def nu1(yv):
    return (1.0 + math.sqrt(1.0 + 4.0 / yv)) / 2.0


def nu2(yv):
    return math.sqrt(1.0 + 1.0 / yv)


mx, ymax = 0.0, 0.0
for yv in np.logspace(-4, 2, 200000):
    r = (nu1(yv) - nu2(yv)) / nu2(yv)
    if r > mx:
        mx, ymax = r, yv


def curv(fn, yv, h=1e-4):
    ly = math.log(yv)
    lp = math.log(fn(math.exp(ly + h)))
    l0 = math.log(fn(yv))
    lm = math.log(fn(math.exp(ly - h)))
    return (lp - 2 * l0 + lm) / h ** 2


c1_knee = curv(nu1, 0.5)
c2_knee = curv(nu2, 0.5)
ck("K21", abs(mx - (2 / math.sqrt(3) - 1)) < 2e-5 and abs(ymax - 0.5) < 1e-3,
   mx, 2e-5,
   "max (g1-g2)/g2 = 2/sqrt3-1 = 0.1547005 at gN=a0/2; d2ln(nu)/d(lny)^2 at "
   "the knee 0.0741 (n1) vs 0.1111 (n2) -- a rotation-curve fit, excluded")

# ===========================================================================
# K22 -- the mean-field non-rotation-curve route: wide binaries at 10 kAU
# ===========================================================================
wb = {}
for M, sv in [(1.0, 10.0), (2.0, 10.0), (1.5, 20.0)]:
    r = sv * 1000.0 * AU
    gNw = G_NEWT * M * MSUN / r ** 2
    yv = gNw / A0
    g1 = g_from_gN_n1(yv)
    g2 = g_from_gN_n2(yv)
    wb[(M, sv)] = (yv, math.sqrt(g1 / g2) - 1.0, math.sqrt(g1 * r), math.sqrt(g2 * r))
k22 = wb[(1.0, 10.0)][1]
ck("K22", 0.070 < k22 < 0.078, k22, 1e-3,
   "wide binary 1 Msun at 10 kAU: y=gN/a0=0.634, v(n1)/v(n2)-1 = 7.40% "
   "(7.03% at 1.5 Msun/10 kAU) -- the knee, no rotation curve")

# ===========================================================================
# K23 -- the medium fingerprint R = c3 c1 / c2^2: +1, 0, and divergent
# ===========================================================================
def series_coeffs(expr, var, n):
    ser = sp.series(expr, var, 0, n + 1).removeO().expand()
    return [sp.simplify(ser.coeff(var, k)) for k in range(1, n + 1)]

cA1 = series_coeffs(A_can, g, 3)
cA2 = series_coeffs(A_n2_sym, g, 3)
R1 = sp.simplify(cA1[2] * cA1[0] / cA1[1] ** 2)
R2 = sp.simplify(cA2[2] * cA2[0] / cA2[1] ** 2)
# R from the MEDIUM itself (isotherm switched by --mutate / --mutate-n2)
if MEDIUM == "tanh":
    A_med_sym = a0 * sp.tanh(g / a0)
elif MEDIUM == "n2":
    A_med_sym = A_n2_sym
else:
    A_med_sym = A_can
cMed = series_coeffs(A_med_sym, g, 3)
if sp.simplify(cMed[1]) == 0:
    R_med = float('inf')
else:
    R_med = float(sp.simplify(cMed[2] * cMed[0] / cMed[1] ** 2))
ck("K23", R1 == 1 and R2 == 0 and abs(R_med - 1.0) < 1e-12, R_med, 1e-12,
   "R = c3*c1/c2^2 (Miller-delta analogue) from the medium: Langmuir +1, "
   "n=2 0, centrosymmetric dielectric divergent")

# ===========================================================================
# K24 -- homogeneity: both laws are degree 1 in (g, a0)
# ===========================================================================
lam_h = sp.symbols('lambda_h', positive=True)
sc = {a0: lam_h * a0, g: lam_h * g}
r24a = sp.simplify(lam_h * A_can - A_can.subs(sc, simultaneous=True))
r24b = sp.simplify(lam_h * gN_can - gN_can.subs(sc, simultaneous=True))
ck("K24", r24a == 0 and r24b == 0,
   float(abs(r24a) + abs(r24b)), 1e-30,
   "A and gN are homogeneous of degree 1 in (g,a0): a0 is the only scale")

# ===========================================================================
# K25 -- the saturated anomaly: A_inf = a0 (n1) vs a0/2 (n2); at gN=a0 the
#        anomaly is 0.618a0 vs 0.414a0 (49% apart)
# ===========================================================================
Ainf1 = float(sp.limit(A_can, g, sp.oo) / a0)
Ainf2 = float(sp.limit(A_n2_sym, g, sp.oo) / a0)
a_y1 = g_from_gN_n1(1.0) / A0 - 1.0
a_y2 = g_from_gN_n2(1.0) / A0 - 1.0
ck("K25", abs(Ainf1 - 1) < 1e-12 and abs(Ainf2 - 0.5) < 1e-12,
   Ainf2, 1e-12,
   "capacity A_inf: a0 (n1) vs a0/2 (n2), factor 2; at gN=a0 anomaly "
   "0.61803a0 vs 0.41421a0")

# ===========================================================================
# K26 -- the adsorption exponent must be exactly 1
# ===========================================================================
def slope_alpha(al, x1=1e-4, x2=1e-5):
    def gNa(xv):
        return 1.0 * (xv - xv ** al / (1.0 + xv ** al))   # a0 = 1
    return (math.log(abs(gNa(x2))) - math.log(abs(gNa(x1)))) / (math.log(x2) - math.log(x1))


sl = {al: slope_alpha(al) for al in (0.5, 1.0, 2.0)}
ck("K26", abs(sl[1.0] - 2) < 1e-3 and abs(sl[2.0] - 1) < 1e-3
   and abs(sl[0.5] - 0.5) < 1e-2, sl[1.0], 1e-3,
   "theta=x^a/(1+x^a): deep exponent 2 only at a=1 (a=2 -> 1, linear; "
   "a=1/2 -> 0.5 with gN<0): the drive must enter the RATE linearly")

# ===========================================================================
# K27 -- the identified medium reproduces BOTH the law and K W'(u) = g
#        (W is checked through its derivative, i.e. the equation of state)
# ===========================================================================
worst_law = 0.0
for xv_ in np.logspace(-3, 3, 400):
    gv = xv_ * A0
    worst_law = max(worst_law, abs(gN_of(gv, A0) - gv ** 2 / (gv + A0)) / (gv ** 2 / (gv + A0)))


def g_of_u(uv, a0v=A0):
    """invert the medium's response A(g) = uv by bisection"""
    lo, hi = 0.0, 1e7 * a0v
    for _ in range(200):
        mid = 0.5 * (lo + hi)
        if resp(mid, a0v) < uv:
            lo = mid
        else:
            hi = mid
    return 0.5 * (lo + hi)


worst_W = 0.0
for xv_ in (0.1, 0.5, 0.9):
    uv = xv_ * A0
    g_med = g_of_u(uv)
    g_W = a0_val = A0 * uv / (A0 - uv)          # K W'(u) for the log form
    worst_W = max(worst_W, abs(g_med - g_W) / g_W)
ck("K27", worst_law < 1e-12 and worst_W < 1e-8, worst_W, 1e-8,
   "the identified medium reproduces gN=g^2/(g+a0) to %.1e and K W'(u)=g to "
   "%.1e (u/a0=0.1,0.5,0.9): the law and the log W are one equation of state"
   % (worst_law, worst_W))

# ===========================================================================
# K28 -- the medium's half-occupancy drive IS a0 (affinity = capacity)
# ===========================================================================
k28_th = isotherm(1.0)
k28_A = resp(1e6 * A0, A0) / A0
ck("K28", abs(k28_th - 0.5) < 1e-12 and abs(k28_A - 1.0) < 1e-5,
   k28_th, 1e-12,
   "the medium at g=a0 is exactly half occupied (theta=1/2) and saturates at "
   "A=a0: the affinity and the capacity are the same number")

# ===========================================================================
# K29 -- n=2 has the SAME c2 as the Langmuir but HALF the capacity: it
#        violates C = -c2 a0 by exactly the factor 2 (the depletion lam=1)
# ===========================================================================
cA2_2 = series_coeffs(A_n2_sym, g, 2)
c2_n2 = sp.simplify(cA2_2[1] * 2)            # A''(0) = 2 c2
cap_n2 = float(sp.limit(A_n2_sym, g, sp.oo) / a0)
k29_ratio = cap_n2 / 1.0                     # C/( -c2 a0 ) with -c2 a0 = 1
ck("K29", abs(float(sp.simplify(c2_n2 * a0 / -2)) - 1) < 1e-15
   and abs(k29_ratio - 0.5) < 1e-15, k29_ratio, 1e-15,
   "n=2: c2=-1/a0 exactly as the Langmuir, but capacity a0/2 not a0 -- it "
   "violates C=-c2*a0 by the factor 2 (A35's lambda=1 depletion)")

# ===========================================================================
# K30 -- the skew's statistical price: N(3 sigma) = 54 / (s_true phi^3)^2
# ===========================================================================
phi_list = (0.3, 0.5, 0.7)
k30 = {phi: 54.0 / (0.70710678 * phi ** 3) ** 2 for phi in phi_list}
# A2's normalisation: 0.03 dex occupancy at g=a0 against a 0.06 dex total
phi_a2 = 0.03 / math.sqrt(0.03 ** 2 + 0.06 ** 2)
k30_a2 = 54.0 / (0.70710678 * phi_a2 ** 3) ** 2
ck("K30", abs(k30[0.5] - 6912) < 5 and abs(k30[0.3] - 148148) < 200
   and 9000 < k30_a2 < 15000, k30_a2, 1e-9,
   "skew N(3sigma): phi=0.5 -> 6912 points, phi=0.3 -> 1.48e5, phi=0.7 -> 918; "
   "0.03 dex occupancy on a 0.06 dex background gives phi=0.447, N=1.35e4")

# ===========================================================================
# K31 -- the skew table quoted in the report (N_s = 1), 9 points, both laws
# ===========================================================================
table_n1 = [2.84605, 1.78885, 1.02062, 0.70711, 0.28868, 0.0, -0.40825, -0.70711, -1.15470]
table_n2 = [1.66413, 0.75718, 0.0, -0.34831, -0.85851, -1.24301, -1.83194, -2.29423, -3.02869]
ks = [0.10, 0.20, 0.375, 0.50, 0.75, 1.00, 1.50, 2.00, 3.00]
worst_tab = 0.0
for xv_, t1, t2 in zip(ks, table_n1, table_n2):
    gv = xv_ * A0
    s1 = skew_binomial(isotherm(xv_))
    s2 = skew_binomial(2 * resp_n2(gv, A0) / A0)
    worst_tab = max(worst_tab, abs(s1 - t1), abs(s2 - t2))
ck("K31", worst_tab < 1e-4, worst_tab, 1e-4,
   "the report's skew table reproduces on all 9 points for both laws")

# ---------------------------------------------------------------------------
ntot = len(CHECKS)
npass = sum(1 for c in CHECKS if c["pass"])
print()
print(f"A63 COMPLETE: {npass}/{ntot} checks PASS.")

results = {
    "lane": "A63_saturating_medium",
    "mutated": MUTATE,
    "medium": MEDIUM,
    "status": (
        "MEDIUM: a one-sided, hard-core, single-occupancy lattice driven by an "
        "ACTIVITY (mass action, adsorption linear in the drive) -- the Langmuir "
        "gate.  It is the only candidate that reproduces BOTH gN=g^2/(g+a0) and "
        "W=(a0^2/K)[-u/a0-ln(1-u/a0)] (and the two are one condition, not two).  "
        "EXCLUDED: tanh and Langevin dielectrics (c2=0 -> gN prop g^3, exponent "
        "3); Born-Infeld (caps the drive, anti-screens, exponent 1); biased "
        "tanh (capacity <= a0/2); multi-occupancy ladders (gN<0); linear-"
        "coupling thermal gates (A(0)=a0/2).  DISCRIMINATOR: the sign of the "
        "occupancy-noise skew at fixed gN -- +0.7071 (n=1) vs -0.3483 (n=2) at "
        "g=a0/2, zero at g=a0 vs 3a0/8, opposite signs on (0.375,1)a0."
    ),
    "checks": CHECKS,
    "numbers": {
        "c2_langmuir": -1.0,
        "c3_langmuir": 1.0,
        "R_langmuir": float(R1),
        "R_n2": float(R2),
        "c2_tanh": float(c2_tanh),
        "c3_tanh": float(c3_tanh),
        "c2_langevin": float(c2_lan),
        "c3_langevin": float(c3_lan),
        "deep_exponent_tanh": slope_tanh,
        "deep_exponent_langevin": 3.0,
        "deep_exponent_BI": 1.0,
        "admissibility_s_over_a0_langmuir": s_lang,
        "admissibility_law": "C = s = -c2*a0",
        "capacity_biased_tanh_max_over_a0": cap_max,
        "R_biased_tanh_max": R_max,
        "A_inf_n1_over_a0": Ainf1,
        "A_inf_n2_over_a0": Ainf2,
        "BI_anomaly_at_gN_a0_over_a0": k10_val,
        "BI_max_rel_dev_from_law": mx_bi,
        "BI_cap_g_over_E_at_gN_1e3a0": k11_bi,
        "skew_n1_at_half_a0": sk1_half,
        "skew_n2_at_half_a0": sk2_half,
        "skew_n1_at_a0": 0.0,
        "skew_n2_at_a0": skew_binomial(2 * resp_n2(A0, A0) / A0),
        "skew_flip_n1_over_a0": float(g_flip1 / a0),
        "skew_flip_n2_over_a0": float(x_flip2),
        "skew_flip_ratio": k19_ratio,
        "skew_window_min_abs": worst_win,
        "max_split_g_rel": mx,
        "max_split_y": ymax,
        "curvature_knee_n1": c1_knee,
        "curvature_knee_n2": c2_knee,
        "wide_binary_M1_s10kAU_y": wb[(1.0, 10.0)][0],
        "wide_binary_M1_s10kAU_dv_rel": wb[(1.0, 10.0)][1],
        "wide_binary_M2_s10kAU_dv_rel": wb[(2.0, 10.0)][1],
        "wide_binary_M1p5_s20kAU_dv_rel": wb[(1.5, 20.0)][1],
        "anomaly_at_gN_a0_n1": a_y1,
        "anomaly_at_gN_a0_n2": a_y2,
        "capacity_per_site_over_a0_at_Ns100": k14_val,
        "W_coeff_ratio_u4": k5_ratio4,
        "W_coeff_ratio_u5": k5_ratio5,
        "tanh_deep_coefficient_over_gc": float(lead_tanh),
        "skew_N3sigma_phi050": k30[0.5],
        "skew_N3sigma_phi030": k30[0.3],
        "skew_N3sigma_phi070": k30[0.7],
        "skew_N3sigma_A2_normalisation": k30_a2,
        "skew_window_gN_over_a0": [0.10227, 0.5],
        "skew_window_g_over_a0": [0.375, 1.0],
    },
    "constants_used": [
        "a0 = 9.36e-11 m s^-2 (BRIEF s4, canonical footing)",
        "c = 2.99792458e8 m s^-1",
        "1 pc = 3.0856775814913673e16 m; kpc = 3.0856775814913673e19 m",
        "1 AU = 1.495978707e11 m",
        "G = 6.67430e-11 m^3 kg^-1 s^-2",
        "M_sun = 1.98892e30 kg",
    ],
}
outname = "a63_results.json"
if MEDIUM == "tanh":
    outname = "a63_results_MUTATE.json"
elif MEDIUM == "n2":
    outname = "a63_results_MUTATE_n2.json"
with open(outname, "w") as fh:
    json.dump(results, fh, indent=2)

sys.exit(0 if npass == ntot else 1)