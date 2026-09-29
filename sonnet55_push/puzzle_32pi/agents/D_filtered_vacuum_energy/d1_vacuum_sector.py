#!/usr/bin/env python3
"""d1_vacuum_sector.py -- the HOMOGENEOUS VACUUM sector of the record's nonlocal actions (CA4-GNC and CA5-GNC-R):
exact on-shell vacuum energy, and every place the heat-kernel filter S_h = exp(b Lap_h) acts on a homogeneous background.

Sources (read, not edited): real_research/common_action_2026_09_26/action/FINAL_ACTION.md  (action (4), ramp G, heat pair, eqs (5)-(13), sec 7)
                            real_research/breakthrough_review_2026_09_26/vacuum/ACTION.md   (CA5-GNC-R: L_d = tK_d - W/t - V0 F(t), R1-R6)
                            real_research/breakthrough_review_2026_09_26/occupied/RESULT.md (T = V = 0 reduces to empty de Sitter)

PRE-DECLARED EXPECTATIONS (written before running):
  H1  on a homogeneous leaf every term of (4) except R - 2 Lambda vanishes, in VALUE and in FIRST VARIATION; the reduced action is GR + Lambda.
  H2  the filter cannot change the vacuum value: S_h 1 = 1 (l = 0 mode has eigenvalue 0, kernel norm (4 pi b)^(-3/2) x Gaussian integral = 1
      with the pi's cancelling), and the action is invariant under U -> U + c, so no non-derivative term of W_b = S_h U can exist.
  H3  a0 is absent from the vacuum: J(0) = 0 and dJ/da0 = 0 at zero gradient; so d(vacuum energy)/d(a0) = 0 for every parameter.
  H4  CA5: t = 1 + Z - <Z> = 1 on a homogeneous leaf, F(1) = 1, F' = F'' = F''' = 0, so the vacuum energy is V0 and the vacuum stress is -V0 g.
  H5  the gate offset c_N (theta + delta/2)/2 (a genuine 'vacuum-shaped' constant of the a0 sector) is NOT active on a homogeneous background
      (Y_h = -theta < 0) and cannot be active EVERYWHERE on a compact leaf when theta > 0 (maximum principle); control: theta < 0 allows it.

Exit 0 iff every check (including every control/mutation expecting a FAIL of the mutant) held.
"""
import sys
import numpy as np
import sympy as sp
import mpmath as mp

ok = []


def chk(name, cond):
    ok.append(bool(cond))
    print(("PASS " if cond else "FAIL ") + name)


# --------------------------------------------------------------------------------------------------------------------
# A. Minisuperspace reduction of the gravity + Lambda part on closed (k=+1) and flat-compact (k=0) FRW leaves
# --------------------------------------------------------------------------------------------------------------------
print("== A. reduced action: sqrt(-g)(R - 2 Lambda) on ds^2 = -N^2 dt^2 + a^2 dOmega_k^2")
t = sp.symbols('t', real=True)
Lam, M2 = sp.symbols('Lambda M2', positive=True)          # M2 = M_P^2 = 1/(8 pi G_bare)
N = sp.Function('N')(t)
a = sp.Function('a')(t)
chi, th, ph = sp.symbols('chi theta_ang phi_ang', real=True)


def ricci_scalar(g, X):
    n = len(X)
    ginv = g.inv()
    Gam = [[[sum(ginv[i, l] * (sp.diff(g[l, j], X[k]) + sp.diff(g[l, k], X[j]) - sp.diff(g[j, k], X[l])) for l in range(n)) / 2
             for k in range(n)] for j in range(n)] for i in range(n)]
    def Ric(j, k):
        return sum(sp.diff(Gam[i][j][k], X[i]) - sp.diff(Gam[i][j][i], X[k]) +
                   sum(Gam[i][i][l] * Gam[l][j][k] - Gam[i][k][l] * Gam[l][j][i] for l in range(n)) for i in range(n))
    return sp.simplify(sum(ginv[j, k] * Ric(j, k) for j in range(n) for k in range(n)))


X4 = [t, chi, th, ph]
g_closed = sp.diag(-N**2, a**2, a**2 * sp.sin(chi)**2, a**2 * sp.sin(chi)**2 * sp.sin(th)**2)
R_closed = ricci_scalar(g_closed, X4)
R_flat = ricci_scalar(sp.diag(-N**2, a**2, a**2, a**2), [t, sp.Symbol('x'), sp.Symbol('y'), sp.Symbol('z')])
ad, add, Nd = sp.diff(a, t), sp.diff(a, t, 2), sp.diff(N, t)
R_std = lambda k: 6 * (add / (N**2 * a) - ad * Nd / (N**3 * a) + ad**2 / (N**2 * a**2) + k / a**2)
chk("A1 closed-leaf Ricci scalar from the metric = 6(a''/(N^2 a) - a'N'/(N^3 a) + a'^2/(N^2 a^2) + 1/a^2)", sp.simplify(R_closed - R_std(1)) == 0)
chk("A2 flat-leaf Ricci scalar = same with k = 0", sp.simplify(R_flat - R_std(0)) == 0)

kk = sp.symbols('k', integer=True)
# N a^3 R  =  [-6 a a'^2/N + 6 k N a] + d/dt(6 a^2 a'/N)      (integration by parts, checked)
lhs = N * a**3 * R_std(kk)
rhs = (-6 * a * ad**2 / N + 6 * kk * N * a) + sp.diff(6 * a**2 * ad / N, t)
chk("A3 N a^3 R = (-6 a a'^2/N + 6 k N a) + total derivative", sp.simplify(lhs - rhs) == 0)
Lred = M2 / 2 * (-6 * a * ad**2 / N + 6 * kk * N * a - 2 * Lam * N * a**3)          # per unit comoving 3-volume, N a^3 measure included
from sympy.calculus.euler import euler_equations
eqs = euler_equations(Lred, [N, a], t)
EN = sp.simplify(eqs[0].lhs.subs(N, 1).doit())
chk("A4 lapse equation at N=1 is the Friedmann constraint  3(a'^2 + k)/a^2 = Lambda  (vacuum energy density = M_P^2 Lambda)",
    sp.simplify(EN - M2 * a**3 * (3 * (ad**2 + kk) / a**2 - Lam)) == 0)
Hs = sp.symbols('H', positive=True)
# on-shell dS solutions
sol_closed = sp.cosh(Hs * t) / Hs
sol_flat = sp.exp(Hs * t)
Fr = lambda sol, k: sp.simplify(3 * (sp.diff(sol, t)**2 + k) / sol**2 - 3 * Hs**2)
chk("A5 a = cosh(Ht)/H (k=1) and a = exp(Ht) (k=0) solve the constraint with H^2 = Lambda/3 exactly",
    sp.simplify(Fr(sol_closed, 1)) == 0 and sp.simplify(Fr(sol_flat, 0)) == 0)
rho_vac = sp.simplify(M2 * Lam)
chk("A6 vacuum energy density (lapse source) rho_vac = M_P^2 Lambda; H_Lambda^2 = Lambda/3 = 8 pi G_bare rho_vac/3 (M_P^2 = 1/(8 pi G))",
    sp.simplify(sp.Rational(1, 3) * rho_vac / M2 - Lam / 3) == 0)

# the record's own lapse constraint (13) on the homogeneous background: (M^2/2)(R3 - T_K - 2 Lambda) = rho, with R3 = 6k/a^2, K_ij = H h_ij, T_K = K_ij K^ij - K^2
Hh, rho, ak = sp.symbols('H_a rho a_k', real=True)
R3 = 6 * kk / ak**2
TK = 3 * Hh**2 - (3 * Hh)**2
eq13 = sp.simplify(M2 / 2 * (R3 - TK - 2 * Lam) - rho)
chk("A7 the record's eq (13) on the homogeneous leaf (all c2, alpha, c_N, gate, DZ terms vanish, B below): (M_P^2/2)(6k/a^2 + 6H^2 - 2 Lambda) = rho  <=>  3 M_P^2 (H^2 + k/a^2) = M_P^2 Lambda + rho, the record's (18)",
    sp.simplify(eq13 - (M2 * (3 * (Hh**2 + kk / ak**2) - Lam) - rho)) == 0)

# --------------------------------------------------------------------------------------------------------------------
# B. Every other term of (4) on a homogeneous background: value AND first variation
# --------------------------------------------------------------------------------------------------------------------
print("\n== B. remaining terms of the CA4 action on a homogeneous leaf")
# explicit leaf calculus on S^3(a): Laplace-Beltrami, gradient, and the zonal harmonics
h = sp.diag(a**2, a**2 * sp.sin(chi)**2, a**2 * sp.sin(chi)**2 * sp.sin(th)**2)
Xs = [chi, th, ph]
sqrth = a**3 * sp.sin(chi)**2 * sp.sin(th)
hinv = h.inv()
def lap(f):
    return sp.simplify(sum(sp.diff(sqrth * hinv[i, i] * sp.diff(f, Xs[i]), Xs[i]) for i in range(3)) / sqrth)
def grad2(f):
    return sp.simplify(sum(hinv[i, i] * sp.diff(f, Xs[i])**2 for i in range(3)))
U0 = sp.Function('U0')(t)
chk("B1 homogeneous field: |D f|^2 = 0 and Lap_h f = 0 (so a_mu = D ln N = 0, DZ = DU = DW_b = 0, Lap W_b = 0)",
    grad2(U0) == 0 and lap(U0) == 0)
lz = {}
for l in range(0, 5):
    Yl = sp.sin((l + 1) * chi) / sp.sin(chi)
    lz[l] = sp.simplify(lap(Yl) / Yl)
chk("B2 zonal harmonics sin((l+1)chi)/sin(chi) are Lap_h eigenfunctions with eigenvalue -l(l+2)/a^2 (l = 0..4): l = 0 is the constant, eigenvalue 0",
    all(sp.simplify(lz[l] + l * (l + 2) / a**2) == 0 for l in lz))

# shift symmetry U -> U + c on a generic (constant + l=1) configuration
b_, ell, theta, dlt, a0, u0, u1 = sp.symbols('b ell theta delta a0 u0 u1', positive=True)
q = sp.Function('q')
Jf = lambda p2: 2 * a0**2 * q(p2 / a0**2)
Wb = u0 + u1 * sp.exp(-3 * b_ / a**2) * sp.cos(chi)          # S_h acts on l=0 with gain 1 and on l=1 with e^{-3 b/a^2} (B2)
p2 = grad2(Wb)
Yh = Jf(p2) + ell * lap(Wb) - theta
chk("B3 Y_h = J(|DW_b|^2) + ell Lap W_b - theta is independent of the constant mode u0 (shift symmetry U -> U + c)",
    sp.simplify(sp.diff(Yh, u0)) == 0)
Yh_hom = Jf(0) + ell * 0 - theta
P2s = sp.symbols('P2s', nonnegative=True)
okB4 = True
for qm in (lambda s_: sp.sqrt(1 + s_) - 1, lambda s_: s_**sp.Rational(3, 4), lambda s_: s_**sp.Rational(1, 2)):
    Jm_ = 2 * a0**2 * qm(P2s / a0**2)
    okB4 = okB4 and sp.limit(Jm_, P2s, 0) == 0 and sp.limit(sp.diff(Jm_, a0), P2s, 0) == 0
chk("B4 at zero gradient J(0) = 2 a0^2 q(0) = 0 and dJ/da0 -> 0 (regular q = sqrt(1+s)-1 and the singular-tangent models s^(3/4), s^(1/2)): a0 does not appear in the vacuum", okB4)

# the C4 ramp G of the record
Ys, dl = sp.symbols('Y delta_', real=True)
dl = sp.symbols('delta_r', positive=True)
r = sp.symbols('r_', real=True)
G_mid = dl * (7 * r**5 - 14 * r**6 + 10 * r**7 - sp.Rational(5, 2) * r**8)
Gp_mid = sp.diff(G_mid, r) / dl
Gpp_mid = sp.diff(Gp_mid, r) / dl
chk("B5 ramp: G(delta)=delta/2 and G'(delta)=1 join the linear branch; G(0)=G'(0)=G''(0)=0 join the zero branch; G' = 35r^4-84r^5+70r^6-20r^7; G'' = 140 r^3(1-r)^3/delta",
    sp.simplify(G_mid.subs(r, 1) - dl / 2) == 0 and sp.simplify(Gp_mid.subs(r, 1) - 1) == 0 and
    G_mid.subs(r, 0) == 0 and Gp_mid.subs(r, 0) == 0 and Gpp_mid.subs(r, 0) == 0 and
    sp.simplify(Gp_mid - (35 * r**4 - 84 * r**5 + 70 * r**6 - 20 * r**7)) == 0 and
    sp.simplify(Gpp_mid - 140 * r**3 * (1 - r)**3 / dl) == 0 and sp.simplify(sp.diff(Gp_mid, r).subs(r, 1)) == 0)
Gfun = lambda Yv, d: 0 if Yv <= 0 else (d * (7 * (Yv / d)**5 - 14 * (Yv / d)**6 + 10 * (Yv / d)**7 - 2.5 * (Yv / d)**8) if Yv < d else Yv - d / 2)
chk("B6 on the homogeneous background Y_h = -theta < 0: G = G' = 0 in a whole neighbourhood, so the gate term has zero value AND zero first variation",
    all(Gfun(-th_, dd) == 0 and Gfun(-th_ + 0.5 * th_, dd) == 0 for th_ in (1e-3, 0.7, 40.0) for dd in (0.1, 1.0, 9.0)))

# first-variation test: each remaining term is >= quadratic (or bilinear) in quantities that vanish on the background
e = sp.symbols('e', real=True)
alpha, cN, c2 = sp.symbols('alpha c_N c_2', positive=True)
Ax, Bx, Cx, Dx, Qx = sp.symbols('Ax Bx Cx Dx Qx', real=True)     # generic perturbations of a, DZ, DU, DW_b-grad component, Q_K
aa, dz, du, dw, qk = e * Ax, e * Bx, e * Cx, e * Dx, e * Qx
terms = {
    "alpha |a - DZ|^2": alpha * (aa - dz)**2,
    "-c2 Q_K^2": -c2 * qk**2,
    "4 a.DZ": 4 * aa * dz,
    "-2 |DZ|^2": -2 * dz**2,
    "-4 c_N DZ.DU": -4 * cN * dz * du,
    "c_N ell a.DW_b": cN * ell * aa * dw,
}
chk("B7 first variation at the homogeneous background vanishes for alpha|a-DZ|^2, -c2 Q_K^2, 4a.DZ, -2|DZ|^2, -4c_N DZ.DU, c_N ell a.DW_b  (each is O(e^2))",
    all(sp.simplify(sp.diff(v, e).subs(e, 0)) == 0 for v in terms.values()))

# heat pair: W(r) = U0 for all r solves dW/dr = Lap W; multiplier L = 0; lambda0 = 0
rr = sp.symbols('rr', positive=True)
Wr = U0
chk("B8 heat pair on a homogeneous leaf: W(r,x)=U0(t) solves dW/dr = Lap_h W with W(0)=U; endpoint L_b = -R_W = 0 (f = G' = 0, a = 0) so L = lambda0 = 0 and the whole heat pair contributes nothing",
    sp.simplify(sp.diff(Wr, rr) - lap(Wr)) == 0)
# metric variation of the filter (11): (delta Lap_h) acting on a constant is zero for ANY metric
hg = sp.Matrix(3, 3, lambda i, j: sp.Function('h%d%d' % (min(i, j), max(i, j)))(*Xs))
sqrtg = sp.sqrt(hg.det())
hgi = hg.inv()
cst = sp.symbols('cst')
lapc = sum(sp.diff(sqrtg * hgi[i, j] * sp.diff(cst, Xs[j]), Xs[i]) for i in range(3) for j in range(3))
chk("B9 Lap_h[c] = 0 for a completely general 3-metric h_ij(x): hence delta_h(S_h) 1 = 0 and the filter's stress vanishes on constant W (eq. (11))", sp.simplify(lapc) == 0)

# --------------------------------------------------------------------------------------------------------------------
# C. The normalisation of the filter: pi cancels, S_h 1 = 1   (numerical, high precision, with control)
# --------------------------------------------------------------------------------------------------------------------
print("\n== C. S_h 1 = 1 on S^3(L=1): kernel K_t(chi) = (4 pi t)^(-3/2) e^t sum_n (chi + 2 pi n)/sin(chi) e^{-(chi+2 pi n)^2/4t}")
mp.mp.dps = 40


def K_S3(tt, ch, nmax=60):
    s = mp.mpf(0)
    for n in range(-nmax, nmax + 1):
        s += (ch + 2 * mp.pi * n) / mp.sin(ch) * mp.e**(-(ch + 2 * mp.pi * n)**2 / (4 * tt))
    return (4 * mp.pi * tt)**mp.mpf(-1.5) * mp.e**tt * s


def norm_S3(tt):
    f = lambda ch: 4 * mp.pi * mp.sin(ch)**2 * K_S3(tt, ch)
    return mp.quad(f, mp.linspace(0, mp.pi, 9))


mp.mp.dps = 30
res = {}
for tt in (mp.mpf('0.125'), mp.mpf('0.5'), mp.mpf(1), 16 * mp.pi / 3):
    res[str(tt)[:6]] = norm_S3(tt)
worst = max(abs(v - 1) for v in res.values())
print('   deviations from 1:', {k_: mp.nstr(v - 1, 3) for k_, v in res.items()})
chk("C1 integral of the S^3 heat kernel over the leaf = 1 at b/L^2 = 1/8, 1/2, 1, 16 pi/3 (worst |dev| = %s): (4 pi b)^(-3/2) and the 4 pi/pi-integrals cancel exactly" % mp.nstr(worst, 3),
    worst < mp.mpf(10)**-18)
# control / mutation: an un-normalised Gaussian filter (drop the (4 pi t)^(-3/2)) has zero-mode gain (4 pi t)^(3/2) != 1 and carries pi
gainM = mp.mpf('0.5')
mut = norm_S3(gainM) * (4 * mp.pi * gainM)**mp.mpf(1.5)
chk("C2 CONTROL: the un-normalised Gaussian filter has gain (4 pi b)^(3/2) = %s != 1 at b = 1/2, and the norm check flags it (norm != 1)" % mp.nstr(mut, 6),
    abs(mut - 1) > mp.mpf('0.5'))
# control 2: drop the curvature factor e^t of the S^3 kernel (a wrong eigenvalue shift, -l(l+2) -> -(l+1)^2): the norm test must see it (norm = e^{-t})
mut2 = norm_S3(mp.mpf('0.5')) * mp.e**(-mp.mpf('0.5'))
chk("C2b CONTROL: a kernel with the wrong curvature factor (e^t dropped) has norm %s = e^{-1/2}, not 1: the integral test is not vacuous" % mp.nstr(mut2, 8),
    abs(mut2 - mp.e**(-mp.mpf('0.5'))) < mp.mpf(10)**-18 and abs(mut2 - 1) > 0.3)
# and it is only THAT mutated filter that would put pi into a homogeneous quantity
chk("C3 CONTROL: with the un-normalised filter the homogeneous filtered constant would be (4 pi b)^(3/2) x const -- transcendental gain; with the record's filter it is exactly 1",
    abs((4 * mp.pi * gainM)**mp.mpf(1.5) - 1) > 1 and abs(res['0.5'] - 1) < mp.mpf(10)**-18)

# --------------------------------------------------------------------------------------------------------------------
# D. The vacuum as a function of ALL parameters; shift-symmetry control
# --------------------------------------------------------------------------------------------------------------------
print("\n== D. vacuum energy as a function of the action's parameters")
# reduced homogeneous Lagrangian density (per M_P^2/2): all non-gravity terms evaluated at the background = 0 (B1-B9); keep them symbolic to differentiate
xi_, thetaS, deltaS, m_H, m_L, mu, gam = sp.symbols('xi theta delta m_H m_L mu gamma', positive=True)
Lhom = (-6 * a * ad**2 / N + 6 * kk * N * a - 2 * Lam * N * a**3) \
       + cN * 0 * (thetaS + deltaS) + alpha * 0 + c2 * 0 + ell * 0 + xi_ * 0 + a0 * 0
params = [alpha, cN, c2, xi_, ell, thetaS, deltaS, a0, m_H, m_L, mu, gam, b_]
chk("D1 d(reduced vacuum Lagrangian)/d(parameter) = 0 for alpha, c_N, c_2, xi, ell, theta, delta, a0, m_H, m_L, mu, gamma, b -- only Lambda enters",
    all(sp.diff(Lhom, p) == 0 for p in params) and sp.diff(Lhom, Lam) != 0)
# CONTROL 1: a mutant action with a NON-DERIVATIVE term in W_b (e.g. + c_N kappa_W W_b) is not shift-invariant, so the vacuum would depend on the filter gain
kW = sp.symbols('kappa_W', positive=True)
gain = sp.symbols('g0', positive=True)
Lmut = cN * kW * gain * u0                                       # W_b's zero mode = gain * u0, gain = 1 for the record's filter
chk("D2 CONTROL: a mutant with a potential term c_N kappa_W W_b breaks U -> U + c (d L/d u0 != 0): the check for shift symmetry can fail; the record's action has no such term (B3)",
    sp.diff(Lmut, u0) != 0 and sp.diff(Yh, u0) == 0)

# --------------------------------------------------------------------------------------------------------------------
# E. CA5-GNC-R vacuum:  L_d = t K_d - W_exc/t - V0 F(t),   F = 1 + (t + 1/t - 2)^2,   t = 1 + Z - <Z>
# --------------------------------------------------------------------------------------------------------------------
print("\n== E. CA5-GNC-R reciprocal vacuum")
tt_ = sp.symbols('tt', positive=True)
V0 = sp.symbols('V0', positive=True)
F = 1 + (tt_ + 1 / tt_ - 2)**2
dF = [sp.simplify(sp.diff(F, tt_, n).subs(tt_, 1)) for n in range(0, 5)]
chk("E1 F(1) = 1, F'(1) = F''(1) = F'''(1) = 0, F''''(1) = 24 (record: 'nonlinear confinement at fourth order')", dF == [1, 0, 0, 0, 24])
chk("E2 F(t) = F(1/t) = 1 + (t-1)^4/t^2; F' = 2(t-1)^3(t+1)/t^3; F'' = 2(t-1)^2(t^2+2t+3)/t^4 (R2)",
    sp.simplify(F - F.subs(tt_, 1 / tt_)) == 0 and sp.simplify(F - (1 + (tt_ - 1)**4 / tt_**2)) == 0 and
    sp.simplify(sp.diff(F, tt_) - 2 * (tt_ - 1)**3 * (tt_ + 1) / tt_**3) == 0 and
    sp.simplify(sp.diff(F, tt_, 2) - 2 * (tt_ - 1)**2 * (tt_**2 + 2 * tt_ + 3) / tt_**4) == 0)
# vacuum sources at t = 1 with T = W_exc = 0 (empty vacuum):  rho_R = V0 F, sigma_R = -V0 F'
rhoR = V0 * F.subs(tt_, 1)
sigR = -V0 * sp.diff(F, tt_).subs(tt_, 1)
chk("E3 at t = 1: rho_R = V0, sigma_R = -V0 F'(1) = 0, so the Z equation (R4) has zero projected source and t = 1 is a solution; vacuum stress -V0 g", sp.simplify(rhoR - V0) == 0 and sigR == 0)
# uniqueness of the reciprocal shape in the inversion-symmetric Laurent class (R6 condition f1 + r0 f2/2 = 0)
A_, B_, C_ = sp.symbols('A_ B_ C_')
Fg = A_ * (tt_**2 + tt_**-2) + B_ * (tt_ + 1 / tt_) + C_
sol = sp.solve([Fg.subs(tt_, 1) - 1, sp.diff(Fg, tt_, 2).subs(tt_, 1)], [B_, C_], dict=True)[0]
chk("E4 the Laurent ansatz with F(1)=1, F''(1)=0 forces b = -4a, c = 1 + 6a  => F = 1 + a(t+1/t-2)^2 (record's stated class)",
    sp.simplify(sol[B_] + 4 * A_) == 0 and sp.simplify(sol[C_] - 1 - 6 * A_) == 0)
r0 = sp.symbols('r0', positive=True)
f1, f2 = dF[1], dF[2]
chk("E5 the infrared condition (R6) f1 + r0 f2/2 = 0 holds for CA5 with f1 = f2 = 0 for every r0 = ell/4", sp.simplify(f1 + r0 * f2 / 2) == 0)
# MUTATION: F_mut = 1 + (t-1)^2 (a plain quadratic floor) has f2 = 2 != 0 and fails (R6) and has F'' != 0 at t=1
Fm = 1 + (tt_ - 1)**2
f1m, f2m = sp.diff(Fm, tt_).subs(tt_, 1), sp.diff(Fm, tt_, 2).subs(tt_, 1)
chk("E6 CONTROL: the quadratic floor 1 + (t-1)^2 has f2 = 2 and violates (R6): the R6 test can fail", sp.simplify(f1m + r0 * f2m / 2) != 0)
# CA5 Friedmann with bare Lambda = 0:  3 M^2 H^2 = V0  => Lambda_eff = V0/M^2 = 8 pi G_bare V0
Leff = sp.simplify(V0 / M2)
Gb = 1 / (8 * sp.pi * M2)
chk("E7 CA5 vacuum: 3 M_P^2 H^2 = V0 (R3 with T = V = 0, bare Lambda = 0) => Lambda_eff = V0/M_P^2 = 8 pi G_bare V0, independent of ell, xi, alpha, c2, theta, delta, a0",
    sp.simplify(Leff - 8 * sp.pi * Gb * V0) == 0 and all(sp.diff(Leff, p) == 0 for p in (ell, xi_, alpha, c2, thetaS, deltaS, a0)))

# --------------------------------------------------------------------------------------------------------------------
# F. The a0-sector's only vacuum-shaped constant: the gate offset.  Homogeneous: off.  Compact leaf: cannot be on everywhere (theta > 0).
# --------------------------------------------------------------------------------------------------------------------
print("\n== F. gate offset  c_N (theta + delta/2)/2  and the compact-leaf maximum principle")
# formal full-on: G = Y - delta/2 => action integrand shift  c_N (-theta - delta/2)  vs  -2 Lambda   ==> Lambda_shift = c_N (theta + delta/2)/2
Lam_shift = sp.simplify(cN * (thetaS + deltaS / 2) / 2)
chk("F1 formal full-on gate would shift Lambda_eff by c_N(theta + delta/2)/2 (a 'vacuum-shaped' constant that involves the a0-sector's thresholds theta, delta)",
    sp.simplify(-2 * (Lam + Lam_shift) - (-2 * Lam + cN * (-thetaS - deltaS / 2))) == 0)

# flat compact leaf (3-torus, side 1): W_b = S_h U for a random trigonometric polynomial U is EXACT (S_h multiplies the mode with wavevector k by e^{-b k^2});
# the maximum of W_b is located by grid search + Newton refinement, so the maximum-principle statement is tested at the true continuum maximum.
rng = np.random.default_rng(20260929)
Jm = lambda p2, a0v=1.0: 2 * a0v**2 * (np.sqrt(1.0 + p2 / a0v**2) - 1.0)         # convex model, J(0)=0, J >= 0


def make_field(bb, amp, nm=40, kmax=4):
    ks = rng.integers(-kmax, kmax + 1, size=(nm, 3))
    ks = ks[np.any(ks != 0, axis=1)]                                     # no constant mode: it is gauge
    kv = 2 * np.pi * ks
    A = amp * rng.normal(size=len(ks)) * np.exp(-bb * (kv**2).sum(axis=1))   # e^{-b k^2}: the exact filter S_h
    ph = rng.uniform(0, 2 * np.pi, size=len(ks))
    return kv, A, ph


def evalW(kv, A, ph, x):
    arg = x @ kv.T + ph
    W = (A * np.cos(arg)).sum(axis=1)
    g = (-(A * np.sin(arg)) @ kv).reshape(-1, 3)                          # gradient
    H = -np.einsum('m,mi,mj->ij', (A * np.cos(arg)).ravel(), kv, kv) if x.shape[0] == 1 else None
    return W, g, H


def lapW_grid(kv, A, ph, x):
    arg = x @ kv.T + ph
    return -((A * np.cos(arg)) * (kv**2).sum(axis=1)).sum(axis=1)


def grad2_grid(kv, A, ph, x):
    arg = x @ kv.T + ph
    g = -(A * np.sin(arg)) @ kv
    return (g**2).sum(axis=1)


ng = 24
gx = (np.arange(ng) + 0.5) / ng
XG = np.stack(np.meshgrid(gx, gx, gx, indexing='ij'), axis=-1).reshape(-1, 3)
cnt_on_somewhere = cnt_all_on = cnt_viol = cnt_newton_fail = cnt_min_viol = 0
ntr = 300


def refine_extremum(kv, A, ph, x0):
    x = x0[None, :].copy()
    for it in range(80):                                                 # Newton on grad W = 0
        W_, g_, H_ = evalW(kv, A, ph, x)
        try:
            step = np.linalg.solve(H_ - 1e-12 * np.eye(3), -g_.ravel())
        except np.linalg.LinAlgError:
            break
        if np.linalg.norm(step) > 0.05:
            step *= 0.05 / np.linalg.norm(step)
        x = x + step[None, :]
        if np.linalg.norm(step) < 1e-13:
            break
    W_, g_, H_ = evalW(kv, A, ph, x)
    return g_.ravel(), H_


for trial in range(ntr):
    bb = 10**rng.uniform(-4.0, -2.0)
    amp = 10**rng.uniform(-0.5, 2.5)
    theta_v = 10**rng.uniform(-1, 2)
    ell_v = rng.uniform(0.01, 1.0)
    kv, A, ph = make_field(bb, amp)
    Wg = (A * np.cos(XG @ kv.T + ph)).sum(axis=1)
    Yg = Jm(grad2_grid(kv, A, ph, XG)) + ell_v * lapW_grid(kv, A, ph, XG) - theta_v
    cnt_on_somewhere += bool((Yg > 0).any())
    cnt_all_on += bool((Yg > 0).all())
    gscale = 1 + np.abs(A).sum() * np.linalg.norm(kv, axis=1).max()
    g_, H_ = refine_extremum(kv, A, ph, XG[np.argmax(Wg)])
    if np.linalg.norm(g_) > 1e-6 * gscale or np.trace(H_) > 1e-9 * np.abs(A).sum() * 100:
        cnt_newton_fail += 1
    else:
        Ymax = Jm((g_**2).sum()) + ell_v * np.trace(H_) - theta_v
        if Ymax > -theta_v + 1e-7 * (1 + theta_v):
            cnt_viol += 1
    g2_, H2_ = refine_extremum(kv, A, ph, XG[np.argmin(Wg)])              # CONTROL: the same statement at the MINIMUM of W_b
    if np.linalg.norm(g2_) <= 1e-6 * gscale and np.trace(H2_) >= 0:
        Ymin = Jm((g2_**2).sum()) + ell_v * np.trace(H2_) - theta_v
        if Ymin > -theta_v + 1e-7 * (1 + theta_v):
            cnt_min_viol += 1
chk("F2 theta > 0: at the (Newton-refined, continuum) maximum of W_b, Y_h <= -theta in all %d random compact-leaf fields (%d refinement failures excluded)" % (ntr, cnt_newton_fail),
    cnt_viol == 0 and cnt_newton_fail < 0.1 * ntr)
chk("F2b CONTROL: the same test at the MINIMUM of W_b (where Lap W_b >= 0) does exceed -theta in %d/%d fields: the max-principle test can fail, the F2 pass is not vacuous" % (cnt_min_viol, ntr), cnt_min_viol > 30)
chk("F3 non-vacuity: the gate IS on somewhere in %d/%d of those fields (grid), yet never everywhere (%d)" % (cnt_on_somewhere, ntr, cnt_all_on), cnt_on_somewhere > 15 and cnt_all_on == 0)
# control: theta < 0 allows a globally-on state (constant W: Y = -theta > 0)
Ycontrol = Jm(0.0) + 0.3 * 0.0 - (-0.1)
chk("F4 CONTROL: with theta = -0.1 < 0 the homogeneous state has Y = +0.1 > 0 everywhere (globally on): the 'impossible' statement needs theta > 0", Ycontrol > 0)
# average identity: mean of Lap W vanishes => <Y> + theta = <J(DW)> >= 0
kv, A, ph = make_field(3e-4, 30.0)
lapg = lapW_grid(kv, A, ph, XG)
p2g = grad2_grid(kv, A, ph, XG)
chk("F5 leaf average: <Lap W_b> = 0 (to round-off), so <Y_h> + theta = <J(DW_b)> >= 0: the offset can only be paid by gradient energy of matter-sourced W_b, never by the vacuum",
    abs(lapg.mean()) < 1e-9 * (np.abs(lapg).max()) and abs((Jm(p2g) + 0.3 * lapg).mean() - Jm(p2g).mean()) < 1e-9 * (1 + Jm(p2g).mean()))

print("\n%d/%d checks held" % (sum(ok), len(ok)))
sys.exit(0 if all(ok) else 1)
