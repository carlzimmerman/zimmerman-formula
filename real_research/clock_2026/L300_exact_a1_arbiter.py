"""L300 -- THE A=1 ARBITER, EXACT: the cold-cosmic-mean carrier in the full 5-field Minkowski matrix with
EXACT rational parameters and 150-dps root extraction.  L290's a = 1 claim was conditioning-limited at 60
dps (det at the polyroots' claimed minima ~ 1e29-1e44); L291b's FRW tangent (numeric mixed partials) agreed
with the '131' to 2% but its own finite-difference conditioning at 1e6-scale entries is unfixed.  THIS lane
settles both with the exact polynomial: the 5x5 matrix at exactly rational (dust, clock, switch) parameters,
the determinant as an exact rational polynomial in W = omega^2, its roots at 150 dps with residual checks.
The predictions: (i) if the growing family is PHYSICS it persists at 150 dps with |det|/scale < 1e-30 at the
roots and scales ~ k^2-ish across k = 0.01/0.1/1 per Mpc; (ii) if it is conditioning/Jeans-swindle noise the
150-dps roots collapse to the bare dust branch (omega ~ +-sqrt(4 pi G rho) ~ 0.68 H0, k-independent) and the
growing '131' family vanishes: the L291b arbiter is then an artifact and the carrier's z ~ 0 face is ordinary
cold-Jeans dust (the CDM-class linear growth the brief requires)."""
import math, time, json, os
import sympy as sp
import mpmath as mp
T0 = time.time(); print("L300 -- the exact a = 1 arbiter (rational 5x5, 150-dps roots)\n")
t, x, y, z = sp.symbols('t x y z', real=True); X = [t, x, y, z]
eps = sp.symbols('epsilon', positive=True)
KB, c1, c2, c3, c4, Q0, beta, xi, Cc, G1, G2 = sp.symbols('K_B c_1 c_2 c_3 c_4 Q_0 beta xi C G_1 G_2', real=True)
c14 = sp.Symbol('c14', real=True)
Psi, Phi, Tf, P, Xc = [sp.Function(n)(t, x) for n in ("Psi", "Phi", "T", "P", "chi")]
Nf = 1 + eps * Psi; af = 1 - eps * Phi
g = sp.diag(-Nf ** 2, af ** 2, af ** 2, af ** 2); ginv = g.inv(); sqrtg = Nf * af ** 3
Gam = [[[sp.simplify(sum(ginv[l, s] * (sp.diff(g[s, m], X[n]) + sp.diff(g[s, n], X[m]) - sp.diff(g[m, n], X[s])) for s in range(4)) / 2) for n in range(4)] for m in range(4)] for l in range(4)]
Ric = sp.zeros(4, 4)
for m in range(4):
    for n in range(4):
        Ric[m, n] = sum(sp.diff(Gam[l][m][n], X[l]) - sp.diff(Gam[l][m][l], X[n]) + sum(Gam[l][l][s] * Gam[s][m][n] - Gam[l][n][s] * Gam[s][m][l] for s in range(4)) for l in range(4))
R = sum(ginv[m, n] * Ric[m, n] for m in range(4) for n in range(4))
tau = t + eps * Tf; dtau = [sp.diff(tau, v) for v in X]
Xinv = -sum(ginv[m, n] * dtau[m] * dtau[n] for m in range(4) for n in range(4))
n_dn = [-dtau[m] / sp.sqrt(Xinv) for m in range(4)]; n_up = [sum(ginv[m, n] * n_dn[n] for n in range(4)) for m in range(4)]
Dn = [[sp.diff(n_dn[n], X[m]) - sum(Gam[l][m][n] * n_dn[l] for l in range(4)) for n in range(4)] for m in range(4)]
Dn_up = [[sum(ginv[m, a_] * ginv[n, b_] * Dn[a_][b_] for a_ in range(4) for b_ in range(4)) for n in range(4)] for m in range(4)]
T1 = sum(Dn[m][n] * Dn_up[m][n] for m in range(4) for n in range(4)); divn = sum(ginv[m, n] * Dn[m][n] for m in range(4) for n in range(4)); T2 = divn ** 2
T3 = sum(Dn[m][n] * Dn_up[n][m] for m in range(4) for n in range(4))
J_dn = [sum(n_up[nu] * Dn[nu][m] for nu in range(4)) for m in range(4)]; J_up = [sum(ginv[m, n] * J_dn[n] for n in range(4)) for m in range(4)]
T4 = sum(J_dn[m] * J_up[m] for m in range(4))
phi = Q0 * t + eps * P; dphi = [sp.diff(phi, v) for v in X]
Jdphi = sum(J_up[m] * dphi[m] for m in range(4)); Q = sum(n_up[m] * dphi[m] for m in range(4))
Y = sum((ginv[m, n] + n_up[m] * n_up[n]) * dphi[m] * dphi[n] for m in range(4) for n in range(4))
chi = Cc * t + eps * Xc; dchi = [sp.diff(chi, v) for v in X]
Xchi = -sum(ginv[m, n] * dchi[m] * dchi[n] for m in range(4) for n in range(4)); dX = Xchi - Cc ** 2
JF = sp.Function('Jfunc'); FW = sp.Function('Fw'); FCH = sp.Function('Fch')
Lbr = R - c1 * T1 - c2 * T2 - c3 * T3 + c4 * T4 + 2 * (2 - KB) * Jdphi - (2 - KB) * beta * Y - (G1 * dX + G2 * dX ** 2 / 2)
L = sqrtg * Lbr
L2 = sp.expand(sp.diff(L, eps, 2).subs(eps, 0) / 2)
fields = [Psi, Phi, Tf, P, Xc]
def EL(Lag, f):
    e = sp.diff(Lag, f)
    for d_ in Lag.atoms(sp.Derivative):
        if d_.expr == f:
            vars_ = []
            for v_, cnt in d_.variable_count: vars_ += [v_] * cnt
            e += (-1) ** len(vars_) * sp.diff(sp.diff(Lag, d_), *vars_)
    return sp.expand(e)
E = [EL(L2, f) for f in fields]
w, k = sp.symbols('omega k', positive=True)
amps = sp.symbols('A_Psi A_Phi A_T A_P A_chi'); ex = sp.exp(sp.I * (k * x - w * t))
sub = {f: A * ex for f, A in zip(fields, amps)}
M = sp.zeros(5, 5)
for i, e in enumerate(E):
    ee = sp.expand(sp.simplify(e.subs(sub).doit() / ex))
    for j, A in enumerate(amps): M[i, j] = sp.simplify(ee.coeff(A))
M = M.subs({c1: KB, c3: -KB, c4: c14 - KB})
print(f"    matrix built ({time.time()-T0:.0f} s)")
# ---- exact rational parameters (the a = 1 cold-cosmic-mean state, C = 1)
R_ = sp.Rational
c14n = R_(25, 10 ** 6)
NUM = {KB: R_(1, 5), c14: c14n, c2: c14n / (1 - 2 * c14n), beta: (R_(2) - R_(1, 5)) / (2 - c14n), xi: 0, Q0: 0}
       # the deep-MOND cold point (beta = beta0: J_Y - beta = 0), khronometric equal-speed corner, no well (Q0 = 0), no healing (xi = 0)
p1 = R_(93, 100)                                     # rho16/2 at a = 1 (16 pi G rho = 6 Om_m = 1.86)
A10 = 10 ** 10
g2 = p1 * (A10 - 1) / 2
MPC = 3.0856775814913673e22; H0 = 67.4e3 / MPC; C_ = 2.99792458e8
mp.mp.dps = 150
OUT = {}
for kMpc in (0.01, 0.1, 1.0):
    kk = kMpc * (C_ / H0) / MPC                                   # k in H0/c units at a = 1 (H(a) = 1)
    kQ = R_(str(kk))
    Mn = M.subs(NUM).subs({Cc: 1, G1: -p1, G2: -g2})
    W = sp.Symbol('W', real=True)
    dn = sp.expand(Mn.subs(k, kQ).subs(w ** 2, W).det(method="berkowitz"))
    pW = sp.Poly(dn, W)
    cf = [mp.mpf(R_(c_).p) / mp.mpf(R_(c_).q) for c_ in pW.all_coeffs()]
    while cf and cf[0] == 0: cf = cf[1:]
    roots = mp.polyroots(cf, maxsteps=5000, extraprec=2000)
    grow = sorted([float(mp.re(-r_)) for r_ in roots if mp.re(r_) < 0 and abs(mp.im(r_)) < 1e-12 * abs(r_)], reverse=True)
    # residual check at the claim: |det|/poly_scale at each root
    res = [mp.log10(abs(dn.subs(W, r_)) / abs(cf[0]) + mp.mpf('1e-200')) for r_ in roots]
    OUT[str(kMpc)] = dict(growth=float(grow[0]) if grow else 0.0, roots=[mp.nstr(r_, 6) for r_ in roots],
                          log10_residual=[float(r_) for r_ in res])
    print(f"    k = {kMpc} /Mpc (k_tilde = {float(kQ):.4g} H0/c): growing family: {[f'{g_:.6g}' for g_ in grow]} H0; "
          f"roots {[mp.nstr(r_, 5) for r_ in roots]}; log10|det|/scale at roots: {[f'{float(r_):.1f}' for r_ in res]}", flush=True)
m1 = OUT['0.1']['growth']; m01 = OUT['0.01']['growth']; m1k = OUT['1.0']['growth']
check_ok = m1 < 1.0 and m01 < 1.0 and m1k < 1.5
print(f"\n    the dust's own Jeans reference: omega = sqrt(4 pi G rho) = sqrt(1.5 Om_m) = {math.sqrt(1.5 * 0.31):.3f} H0 (k-independent)")
print(f"    L290's conditioning-limited '131' at k = 0.1; L291b's numeric tangent: 128; this exact extraction: {m1:.6g}")
print(f"    [{'PASS' if check_ok else 'FAIL'}] L300 [FINDING] the exact a = 1 arbiter: the growing family of the"
      f" cold cosmic-mean carrier at 150 dps is {m1:.6g} H0 at k = 0.1 /Mpc (L290: 131, L291b FRW: 128) with "
      f"log10|det|/scale {OUT['0.1']['log10_residual'][0]:.0f} at the root: [the family persists => PHYSICS, the "
      f"carrier dies at z ~ 0; the family collapses => conditioning artifact, the carrier's z ~ 0 face is ordinary "
      f"cold-Jeans dust]")
json.dump(OUT, open(os.path.splitext(os.path.abspath(__file__))[0] + "_results.json", "w"), indent=1, default=str)
print(f"\nL300 COMPLETE ({time.time()-T0:.0f} s)")
import sys; sys.exit(0 if check_ok else 1)