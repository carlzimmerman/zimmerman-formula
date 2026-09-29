#!/usr/bin/env python3
"""j01_conventions_and_target.py -- lane J (membrane route): fix the conventions, verify them from first principles, and
state exactly what the puzzle asks of a membrane.  G = c = 1 throughout (hbar not used).

CONVENTION (the brief's, verified below, not assumed):
  * Heaviside four-form:  L = -F^2/(2 4!),  F = E vol_4  =>  T_ab = -(E^2/2) g_ab,  rho = E^2/2  (check A2)
  * Lambda = 8 pi rho,  H^2 = Lambda/3 = 8 pi rho/3 = 4 pi E^2/3                                   (check A1)
  * membrane  S = -sigma Int sqrt(-h) + e Int A3   =>  Gauss jump DeltaE = e                      (check A3)
  * wall between E_out = E and E_in = E - e:  Delta P = rho_out - rho_in = e E - e^2/2 = e (E - e/2)   (check A4)
  * Israel (O(4) bounce, G = 1): the two sides' extrinsic curvatures satisfy A - B = 4 pi sigma,
    1/R^2 = H_in^2 + A^2 = H_out^2 + B^2  =>  A, B = DeltaP/(3 sigma) +- 2 pi sigma                (checks A5-A6)
  A, B are the wall's proper accelerations relative to the geodesics of the inner / outer vacuum (agents/I_adversarial_audit a01);
  their mean is DeltaP/(3 sigma) EXACTLY.
TARGET: a0 = H_Lambda/Z, Z = sqrt(32 pi/3)  <=>  G rho = 4 a0^2  <=>  a0 = E/(2 sqrt 2) (rho = E^2/2).
Readings of "the wall's acceleration is a0":  mean, A, or B;  H_Lambda = H_out or H_in (declared, all reported).

Exit 0 = every check (including the controls that MUST detect a wrong convention) held.
"""
import sys, math, itertools
import sympy as sp
import mpmath as mp

mp.mp.dps = 40
ok = []
def chk(name, cond):
    ok.append(bool(cond)); print(("PASS " if cond else "FAIL ") + name)

# --------------------------------------------------------------------------------------------------------------- helpers
def einstein(g, x):
    n = len(x); gi = g.inv()
    Gam = [[[sum(gi[i, l] * (sp.diff(g[l, j], x[k]) + sp.diff(g[l, k], x[j]) - sp.diff(g[j, k], x[l])) for l in range(n)) / 2
             for k in range(n)] for j in range(n)] for i in range(n)]
    def Riem(i, j, k, l):
        return (sp.diff(Gam[i][j][l], x[k]) - sp.diff(Gam[i][j][k], x[l])
                + sum(Gam[i][k][m] * Gam[m][j][l] - Gam[i][l][m] * Gam[m][j][k] for m in range(n)))
    Ric = sp.Matrix(n, n, lambda j, l: sp.simplify(sum(Riem(i, j, i, l) for i in range(n))))
    Rs = sp.simplify(sum(gi[j, l] * Ric[j, l] for j in range(n) for l in range(n)))
    G = (Ric - Rs * g / 2).applyfunc(sp.simplify)
    return G, Ric, Rs

print("== A. conventions verified from first principles ==")
# ------------------------------------------------------------------------------------------- A1: S^4(L): 3 H^2 = 8 pi rho
Ls = sp.symbols('L', positive=True)
chi, th, ph, ps = sp.symbols('chi theta phi psi')
g4 = sp.diag(Ls**2, Ls**2 * sp.sin(chi)**2, Ls**2 * sp.sin(chi)**2 * sp.sin(th)**2,
             Ls**2 * sp.sin(chi)**2 * sp.sin(th)**2 * sp.sin(ph)**2)
G4, Ric4, R4 = einstein(g4, [chi, th, ph, ps])
chk("A1a Euclidean de Sitter S^4(L): G_ab = -(3/L^2) g_ab (Einstein tensor computed from the metric)",
    sp.simplify(G4 + 3 * g4 / Ls**2) == sp.zeros(4, 4))
rhoE = sp.symbols('rho_E', positive=True)
Hh = sp.symbols('H', positive=True)
# G_ab = 8 pi T_ab with T_ab = -rho g_ab  (vacuum energy):  -3 H^2 = -8 pi rho
sol = sp.solve(sp.Eq(-3 * Hh**2, -8 * sp.pi * rhoE), Hh)
chk("A1b vacuum energy rho gives H^2 = 8 pi rho / 3  (Lambda = 8 pi rho, H^2 = Lambda/3)", sp.simplify(sol[0]**2 - 8 * sp.pi * rhoE / 3) == 0)

# ------------------------------------------------------------------------------------------- A2: four-form stress tensor
E = sp.symbols('E', real=True)
eta = sp.diag(-1, 1, 1, 1)
from sympy import LeviCivita
def Fdown(a, b, c, d):        # F_{abcd} = E * eps_{abcd},  eps_{0123} = +1 (flat, sqrt(-g) = 1)
    return E * LeviCivita(a, b, c, d)
idx = range(4)
def Fup(a, b, c, d):
    return eta[a, a] * eta[b, b] * eta[c, c] * eta[d, d] * Fdown(a, b, c, d)
F2 = sum(Fdown(a, b, c, d) * Fup(a, b, c, d) for a in idx for b in idx for c in idx for d in idx)
Tab = sp.zeros(4, 4)
for m in idx:
    for n_ in idx:
        # T_mn = (1/3!) F_{m abc} F_n^{abc} - (1/(2 4!)) g_mn F^2   (from L = -F^2/(2 4!))
        s1 = sum(Fdown(m, a, b, c) * (eta[a, a] * eta[b, b] * eta[c, c]) * Fdown(n_, a, b, c) for a in idx for b in idx for c in idx)
        Tab[m, n_] = sp.Rational(1, 6) * s1 - sp.Rational(1, 48) * eta[m, n_] * F2
chk("A2 four-form F = E vol: F^2 = -24 E^2 and T_ab = -(E^2/2) g_ab, i.e. energy density T_00 = E^2/2 (rho = E^2/2), pressure -E^2/2",
    sp.simplify(F2 + 24 * E**2) == 0 and sp.simplify(Tab + (E**2 / 2) * eta) == sp.zeros(4, 4))

# ------------------------------------------------------------------------------------------- A3: Gauss jump = e
z, e_, a_ = sp.symbols('z e a')
af = sp.Function('a')
# reduced action for A_{012}(z) = a(z):  L = -F^2/(2 4!) = +(a')^2/2   (F^2 = -24 a'^2);   membrane term e * a(0) delta(z)
Lag = sp.Rational(1, 2) * sp.diff(af(z), z)**2 + e_ * sp.DiracDelta(z) * af(z)
from sympy.calculus.euler import euler_equations
eq = euler_equations(Lag, af(z), z)[0]
# EL: d/dz(a') = e delta(z)  =>  jump of a' = e ; E = a'
rhs = sp.simplify(sp.Eq(eq.lhs, 0))
# check: eq is  e delta - a'' = 0
chk("A3 membrane -sigma*Area + e*Int A3 with L = -F^2/(2 4!): Euler-Lagrange gives E'(z) = e delta(z), i.e. Gauss jump DeltaE = e",
    sp.simplify(eq.lhs - (e_ * sp.DiracDelta(z) - sp.diff(af(z), z, 2))) == 0)

# ------------------------------------------------------------------------------------------- A4: Delta P = e (E - e/2)
Es, es, ss = sp.symbols('E e sigma', positive=True)
DP = Es**2 / 2 - (Es - es)**2 / 2
chk("A4 pressure jump rho_out - rho_in = e E - e^2/2 = e * (mean of the two side fields)  (Lorentz force on a charged sheet)",
    sp.simplify(DP - (es * Es - es**2 / 2)) == 0 and sp.simplify(DP - es * (Es + (Es - es)) / 2) == 0)

# ------------------------------------------------------------------------------------------- A5: Israel from the O(4) Einstein equations
xi = sp.symbols('xi')
rho = sp.Function('rho')
gO4 = sp.diag(1, rho(xi)**2, rho(xi)**2 * sp.sin(chi)**2, rho(xi)**2 * sp.sin(chi)**2 * sp.sin(th)**2)
GO, _, _ = einstein(gO4, [xi, chi, th, ph])
GOm = (gO4.inv() * GO).applyfunc(sp.simplify)            # G^a_b
rp, rpp = sp.diff(rho(xi), xi), sp.diff(rho(xi), xi, 2)
Gxixi = 3 * (rp**2 - 1) / rho(xi)**2
Gtan = 2 * rpp / rho(xi) + (rp**2 - 1) / rho(xi)**2
chk("A5a O(4) metric ds^2 = d xi^2 + rho(xi)^2 dOmega_3^2: G^xi_xi = 3(rho'^2 - 1)/rho^2 (constraint) and G^i_j = [2 rho''/rho + (rho'^2 - 1)/rho^2] delta^i_j",
    sp.simplify(GOm[0, 0] - Gxixi) == 0 and all(sp.simplify(GOm[i, i] - Gtan) == 0 for i in (1, 2, 3))
    and all(sp.simplify(GOm[i, j]) == 0 for i in range(4) for j in range(4) if i != j))
# vacuum: G^a_b = -8 pi rho_E delta^a_b  =>  rho'^2 = 1 - H^2 rho^2
Hv2 = sp.symbols('H2', positive=True)
cons = sp.solve(sp.Eq(Gxixi, -3 * Hv2), rp**2)[0]
chk("A5b vacuum constraint: rho'^2 = 1 - H^2 rho^2 with 3 H^2 = 8 pi rho_E", sp.simplify(cons - (1 - Hv2 * rho(xi)**2)) == 0)
# wall: T^i_j = -sigma delta(xi - xi0) delta^i_j (tangential; energy density sigma, tension sigma).  Tangential Einstein equation
# 2 rho''/rho + ... = -8 pi rho_E - 8 pi sigma delta  =>  integrate across the wall:  2 [rho']/rho = -8 pi sigma
coef_rpp = sp.diff(Gtan, rpp)                                 # = 2/rho
jump_rp = sp.simplify(-8 * sp.pi * ss / coef_rpp)             # [rho'] = rho'_out - rho'_in
chk("A5c Israel jump: [rho'] = rho'_out - rho'_in = -4 pi sigma rho  (so the extrinsic curvatures K = rho'/rho obey  K_in - K_out = 4 pi sigma)",
    sp.simplify(jump_rp + 4 * sp.pi * ss * rho(xi)) == 0)

# ------------------------------------------------------------------------------------------- A6: A, B and the mean
Aa, Bb = sp.symbols('A B', real=True)
Hi2 = sp.Rational(8, 3) * sp.pi * (Es - es)**2 / 2
Ho2 = sp.Rational(8, 3) * sp.pi * Es**2 / 2
sols = sp.solve([sp.Eq(Aa - Bb, 4 * sp.pi * ss), sp.Eq(Aa**2 - Bb**2, Ho2 - Hi2)], [Aa, Bb], dict=True)[0]
DPs = es * Es - es**2 / 2
chk("A6 solving A - B = 4 pi sigma, A^2 - B^2 = H_out^2 - H_in^2:  A = DP/(3 sigma) + 2 pi sigma, B = DP/(3 sigma) - 2 pi sigma, mean = DP/(3 sigma)  (all sigma)",
    sp.simplify(sols[Aa] - (DPs / (3 * ss) + 2 * sp.pi * ss)) == 0 and sp.simplify(sols[Bb] - (DPs / (3 * ss) - 2 * sp.pi * ss)) == 0)

# independent numerical solve of the junction for the radius (root-find on R, not using the closed form)
def R_numeric(Ev, ev, sv):
    Ev, ev, sv = mp.mpf(Ev), mp.mpf(ev), mp.mpf(sv)
    hi2 = (8 * mp.pi / 3) * (Ev - ev)**2 / 2; ho2 = (8 * mp.pi / 3) * Ev**2 / 2
    def f(u):                     # u = 1/R^2 ; A>0 branch for the inner cap; B may be of either sign
        A_ = mp.sqrt(u - hi2)
        rhs = A_ - 4 * mp.pi * sv           # = B (signed)
        return rhs**2 - (u - ho2)
    # B^2 = u - ho2 with B = A - 4 pi sigma  (sign of B free) -> solve quadratic-in-sqrt by bracketing
    lo = max(hi2, ho2) + mp.mpf(10)**(-30)
    us = [lo * (1 + mp.mpf(k) / 50)**2 for k in range(0, 4000, 1)]
    prev = f(us[0]); root = None
    for u in us[1:]:
        cur = f(u)
        if prev * cur <= 0:
            root = mp.findroot(f, (u * mp.mpf('0.999'), u), solver='anderson'); break
        prev = cur
    return root
worst = 0; nsolved = 0
for (Ev, ev, sv) in [(1, 0.3, 0.1), (1, 0.05, 0.01), (1, 0.6, 0.2), (1, 1.0, 0.05)]:
    u = R_numeric(Ev, ev, sv)
    if u is None:
        continue
    nsolved += 1
    DPn = mp.mpf(ev) * Ev - mp.mpf(ev)**2 / 2
    ho2 = (8 * mp.pi / 3) * Ev**2 / 2
    u_closed = ho2 + (DPn / (3 * sv) - 2 * mp.pi * sv)**2
    worst = max(worst, abs(u - u_closed) / u_closed)
print("   A6n: %d of 4 cases had a bracketed root" % nsolved)
chk("A6n independent numerical root-find of the Israel junction reproduces 1/R^2 = H_out^2 + (DeltaP/(3 sigma) - 2 pi sigma)^2 (all solved cases, rel err < 1e-12; needs >= 3 solved)", nsolved >= 3 and worst < 1e-12)

# literature cross-checks of the two coefficients that matter (supergravity domain-wall review hep-th/9604090, kappa = 8 pi G = 1):
#  (i) reflection-symmetric wall: acceleration on both sides = sigma/4 = 2 pi G sigma;  (ii) extreme Type I wall (Minkowski|AdS): the AdS fiducial
#  observers accelerate at chi = sigma/2 = 4 pi G sigma, sigma_ext = 2 chi.   Both are the same A - B = 4 pi G sigma.
G_ = sp.symbols('G', positive=True)
sig = sp.symbols('sigma', positive=True)
kap8 = 8 * sp.pi * G_
accel_sym = (4 * sp.pi * G_ * sig) / 2           # A = -B = half of the jump
chk("A6L literature (opened: hep-th/9604090): with kappa = 8 pi G = 1, the symmetric-wall acceleration 2 pi G sigma = sigma/4 and the extreme-wall AdS acceleration 4 pi G sigma = sigma/2 = chi both follow from A - B = 4 pi G sigma",
    sp.simplify(accel_sym.subs(G_, 1 / (8 * sp.pi)) - sig / 4) == 0 and sp.simplify((4 * sp.pi * G_ * sig).subs(G_, 1 / (8 * sp.pi)) - sig / 2) == 0)

# ------------------------------------------------------------------------------------------- B. the TARGET, in membrane variables
print("\n== B. what the puzzle asks of a membrane ==")
Z = mp.sqrt(32 * mp.pi / 3)
kap_s, x_, s_ = sp.symbols('kappa x s', positive=True)
# units E = 1: x = e/E, s = sigma/E
DPx = x_ - x_**2 / 2
Hout_s = sp.sqrt(4 * sp.pi / 3)
mean_s = DPx / (3 * s_)
# puzzle:  a0 = kappa c sqrt(G rho) with rho = E^2/2  ->  a0 = kappa E/sqrt(2)
a0_s = kap_s / sp.sqrt(2)
chk("B1 a0 = kappa sqrt(G rho_Lambda), rho = E^2/2  =>  a0/H_out = kappa sqrt(3/(8 pi)) = 1/Z at kappa = 1/2 (Z = sqrt(32 pi/3)); a0 = E/(2 sqrt 2)",
    sp.simplify(a0_s / Hout_s - kap_s * sp.sqrt(3 / (8 * sp.pi))) == 0 and abs(mp.sqrt(3 / (8 * mp.pi)) / 2 - 1 / Z) < mp.mpf(10)**(-30))
# probe limit x, s -> 0 with k = e/sigma = x/s fixed
k_s = sp.symbols('k', positive=True)
mean_probe = sp.limit((mean_s.subs(x_, k_s * s_)) , s_, 0)
kstar = sp.solve(sp.Eq(mean_probe, a0_s), k_s)[0]
chk("B2 probe limit (x, s -> 0, k = e/sigma fixed): mean acceleration -> k E/3; a0 = E/(2 sqrt2) needs k* = 3 kappa/sqrt2 = 3/(2 sqrt 2) = 1.0607 at kappa = 1/2",
    sp.simplify(kstar - 3 * kap_s / sp.sqrt(2)) == 0 and abs(float(kstar.subs(kap_s, sp.Rational(1, 2))) - 3 / (2 * math.sqrt(2))) < 1e-15)
# the target as a locus in the (x, s) plane, exact (mean reading, H_ref = H_out):  DeltaP/(3 sigma) = E/(2 sqrt2)
locus = sp.simplify(sp.solve(sp.Eq(mean_s, a0_s.subs(kap_s, sp.Rational(1, 2))), s_)[0])
chk("B3 exact target locus (mean reading, all x): sigma/E = (2 sqrt2/3)(x - x^2/2), i.e. DeltaP/(3 sigma) = sqrt(rho)/2 with NO pi anywhere",
    sp.simplify(locus - 2 * sp.sqrt(2) / 3 * (x_ - x_**2 / 2)) == 0 and not locus.has(sp.pi))
# the puzzle in Lagrangian variables: a_mean^2 = (2 e^2 rho/(9 sigma^2)) (1 - x/2)^2, a0^2 = G rho/4  =>  e^2/(G sigma^2) = 9/8 (probe)
rho_s, e2, sg2 = sp.symbols('rho e2 sg2', positive=True)
lhs = (2 * e2 * rho_s / (9 * sg2))                     # probe: (e E / (3 sigma))^2 with E^2 = 2 rho
chk("B4 puzzle in Lagrangian form: (eE/(3 sigma))^2 = G rho/4 with E^2 = 2 rho  <=>  e^2/(G sigma^2) = 9/8   (pi-free); equivalently 4 pi G sigma^2/e^2 = 32 pi/9 = Z^2/3",
    sp.simplify(sp.solve(sp.Eq(lhs, rho_s / 4), e2)[0] / sg2 - sp.Rational(9, 8)) == 0
    and abs(4 * mp.pi / (mp.mpf(9) / 8) - Z**2 / 3) < mp.mpf(10)**(-30))

# kappa -> k*  table
print("   kappa readings and the probe ratio k* = e/sigma they need (Heaviside, rho = E^2/2, Gauss jump e):")
kap_table = [("framework kappa=1/2 (Z=5.789)", mp.mpf(1) / 2),
             ("forced kernel kappa=1 (Z=2.894)", mp.mpf(1)),
             ("Milgrom  c H/(2 pi)  (Z=2 pi)", mp.sqrt(8 * mp.pi / 3) / (2 * mp.pi)),
             ("Verlinde c H/6       (Z=6)", mp.sqrt(8 * mp.pi / 3) / 6),
             ("Nariai-shell 3 sqrt3 (Z=5.196)", mp.sqrt(8 * mp.pi / 3) / (3 * mp.sqrt(3)))]
for nm, kv in kap_table:
    print("     %-34s kappa=%.4f  a0/H=%.5f  k*=3kappa/sqrt2=%.5f" % (nm, kv, kv * mp.sqrt(3 / (8 * mp.pi)), 3 * kv / mp.sqrt(2)))

# ------------------------------------------------------------------------------------------- C. CONTROLS: wrong conventions must shift k* and be detected
print("\n== C. controls: wrong conventions ==")
# general convention: rho = rf E^2, Gauss jump DeltaE = jf e, Israel A - B = cf pi sigma (cf = 4 is right), Heaviside standard (rf, jf, cf) = (1/2, 1, 4)
rf, jf, cf = sp.symbols('rf jf cf', positive=True)
def kstar_general(rfv, jfv, cfv, kap):
    Eq_ = sp.symbols('Eq', positive=True); ee, sg = sp.symbols('ee sg', positive=True)
    DPg = rfv * (Eq_**2 - (Eq_ - jfv * ee)**2)
    Ho2g = sp.Rational(8, 3) * sp.pi * rfv * Eq_**2
    Hi2g = sp.Rational(8, 3) * sp.pi * rfv * (Eq_ - jfv * ee)**2
    # A - B = cf pi sigma, A^2 - B^2 = Ho2 - Hi2  =>  mean = (Ho2-Hi2)/(2 cf pi sigma)
    mean = (Ho2g - Hi2g) / (2 * cfv * sp.pi * sg)
    target = kap * sp.sqrt(3 / (8 * sp.pi)) * sp.sqrt(Ho2g)
    mean_p = sp.limit(mean.subs(ee, sp.Symbol('kk', positive=True) * sg), sg, 0)
    return sp.simplify(sp.solve(sp.Eq(mean_p, target), sp.Symbol('kk', positive=True))[0])
half = sp.Rational(1, 2)
k_std = kstar_general(half, 1, 4, half)
k_m1 = kstar_general(half, half, 4, half)               # Gauss jump e/2
k_m2 = kstar_general(sp.Integer(1), 1, 4, half)         # rho = E^2 (no 1/2)
k_m3 = kstar_general(half, 1, 8, half)                  # Israel 8 pi sigma
kG = kstar_general(1 / (8 * sp.pi), 4 * sp.pi, 4, half)  # Gaussian units: rho = E^2/(8 pi), Gauss jump 4 pi e_G
print("   k*(standard) = %s = %.6f ;  Gauss jump e/2: %s = %.6f ;  rho = E^2: %s = %.6f ;  Israel 8 pi sigma: %s = %.6f ;  Gaussian e_G: %s = %.6f" %
      (k_std, float(k_std), k_m1, float(k_m1), k_m2, float(k_m2), k_m3, float(k_m3), k_m3 * 0 + kG, float(kG)))
chk("C0 general-convention machinery reproduces the standard k* = 3/(2 sqrt 2) for (rho, Gauss, Israel) = (E^2/2, e, 4 pi sigma)", sp.simplify(k_std - 3 / (2 * sp.sqrt(2))) == 0)
chk("C1 CONTROL (Gauss jump e/2): k* doubles to 3/sqrt2 (the kappa = 1 value) -- detected", sp.simplify(k_m1 - 3 / sp.sqrt(2)) == 0 and abs(float(k_m1) - float(k_std)) > 0.1)
chk("C2 CONTROL (rho = E^2, no 1/2): k* becomes 3/4 -- detected", sp.simplify(k_m2 - sp.Rational(3, 4)) == 0 and abs(float(k_m2) - float(k_std)) > 0.1)
chk("C3 CONTROL (Israel 8 pi sigma): k* doubles -- detected", sp.simplify(k_m3 - 3 / sp.sqrt(2)) == 0)
chk("C4 unit change to Gaussian charge e_G = e/sqrt(4 pi): k*_G = 3 kappa/sqrt(8 pi) = k*/sqrt(4 pi) (pi-content changes with the unit, as it must)",
    sp.simplify(kG - 3 * half / sp.sqrt(8 * sp.pi)) == 0 and sp.simplify(kG - k_std / sp.sqrt(4 * sp.pi)) == 0)
# physical a/H in terms of the coupling ratio, for the two units: a/H = k/(2 sqrt(3 pi)) (Heaviside) = k_G/sqrt3 (Gaussian): the physical content is unit-independent
kk = sp.symbols('kk', positive=True)
aH_HL = kk / (2 * sp.sqrt(3 * sp.pi))
# (Gaussian k_G = k/sqrt(4 pi)  =>  a/H = k_G * sqrt(4 pi)/(2 sqrt(3 pi)) = k_G/sqrt3)
chk("C5 covariance: a/H = k/(2 sqrt(3 pi)) [Heaviside] = k_G/sqrt3 [Gaussian, k_G = k/sqrt(4 pi)]: a principle transcribed consistently gives the same a/H; transcribed inconsistently it is off by sqrt(4 pi)",
    sp.simplify(aH_HL - (kk / sp.sqrt(4 * sp.pi)) / sp.sqrt(3)) == 0)

# --------------------------------------------------------------------------------------------------------- D. numerics at the target
print("\n== D. numerical sanity at the target (independent of the algebra above) ==")
Ev = mp.mpf(1); Hn = mp.sqrt((8 * mp.pi / 3) * Ev**2 / 2)
kstar_v = 3 / (2 * mp.sqrt(2))
prev_err = None
for sv in [mp.mpf('1e-3'), mp.mpf('1e-5'), mp.mpf('1e-7')]:
    ev = kstar_v * sv
    dP = ev * Ev - ev**2 / 2
    mean = dP / (3 * sv)
    print("   sigma=%.0e  mean=%.8f  H/Z=%.8f   A=%.8f  B=%.8f" % (sv, mean, Hn / Z, mean + 2 * mp.pi * sv, mean - 2 * mp.pi * sv))
chk("D1 at e/sigma = 3/(2 sqrt2) the mean wall acceleration -> H/Z as sigma -> 0 (rel err < 1e-6 at sigma = 1e-7)", abs(mean / (Hn / Z) - 1) < 1e-6)
print("\n%d/%d" % (sum(ok), len(ok)))
sys.exit(0 if all(ok) else 1)
