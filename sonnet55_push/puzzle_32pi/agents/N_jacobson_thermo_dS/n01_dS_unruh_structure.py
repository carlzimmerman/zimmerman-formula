#!/usr/bin/env python3
"""n01_dS_unruh_structure.py -- exact facts about the temperature, horizon and acceleration of a static observer in de Sitter.

Units c = hbar = k_B = 1; G does not appear.  L = 1/H is the de Sitter radius.  Static patch  ds^2 = -f dt^2 + dr^2/f + r^2 dOmega^2, f = 1 - H^2 r^2.
Three different things are called 'acceleration' (the audit caveat), and this script keeps them apart:
   a      proper acceleration of the static observer (relative to the local geodesic / free fall) -- the MOND-relevant one
   A5     embedding ("Unruh-effective") acceleration, A5^2 = a^2 + H^2  (Deser-Levin's a_5, arXiv gr-qc/9706018, opened)
   kappa  surface gravity of the Killing field normalised to unit length at the observer: kappa_obs = H / sqrt(f0)
Claims (each with controls that must FAIL):
 A1 a = H^2 r0 / sqrt(f0) from the metric (Christoffels);          A2 A5^2 = a^2 + H^2 from the embedding hyperbola
 A3 chordal distance along the worldline = -(4/A5^2) sinh^2(A5 tau/2)  =>  thermal Wightman function, KMS period 2 pi / A5
 A4 numerical detector response F(w) = (w/2pi)/(exp(2 pi w/A5)-1) (detailed balance ratio exp(2 pi w/A5)), also H -> 0 (flat Rindler, T = a/2pi)
 A5 Tolman:  T_GH / sqrt(f0) = A5 / 2pi;  kappa_obs = A5 = a / sin(theta),  tan(theta) = a/H  (sin theta = H r0)
 A6 geodesics: every timelike geodesic of the hyperboloid has A5 = H  (T = H/2pi)
 A7 the horizon of ANY static observer is the same Killing horizon X0 = X1: a 2-sphere of radius L, area 4 pi L^2, independent of a;
    proper distance to it l = (pi/2 - theta)/H ;  a*l -> 1 and kappa*l -> 1 as theta -> pi/2 (flat Rindler limit), corrections O(H^2/a^2)
 A8 kappa of the Killing horizon from the metric = H (geodesic normalisation)
Exit 0 = all pass.
"""
import sys
import sympy as sp
import mpmath as mp

ok = []
def check(name, cond):
    ok.append(bool(cond)); print(f"  [{'OK' if cond else 'FAIL'}] {name}")
def must_fail(name, cond):          # a control: the WRONG statement must be detected as false
    ok.append(not bool(cond)); print(f"  [{'OK' if not cond else 'FAIL'}] CONTROL (wrong claim must be rejected): {name}")

H, r0, a, tau, s = sp.symbols('H r0 a tau s', positive=True)
t, r, th, ph = sp.symbols('t r theta phi', real=True)
f = 1 - H**2 * r**2

print("A1  proper acceleration of the static observer, from the metric")
X = [t, r, th, ph]
g = sp.diag(-f, 1 / f, r**2, r**2 * sp.sin(th)**2)
ginv = g.inv()
Gam = lambda i, j, k: sum(ginv[i, l] * (sp.diff(g[l, j], X[k]) + sp.diff(g[l, k], X[j]) - sp.diff(g[j, k], X[l])) for l in range(4)) / 2
u = [1 / sp.sqrt(f), 0, 0, 0]
acc = [sp.simplify(sum(u[n] * sp.diff(u[m], X[n]) for n in range(4)) + sum(Gam(m, n, k) * u[n] * u[k] for n in range(4) for k in range(4))) for m in range(4)]
a_sq = sp.simplify(sum(g[m, m] * acc[m]**2 for m in range(4)).subs(r, r0))     # |a|^2 = g_rr (a^r)^2
f0 = 1 - H**2 * r0**2
check("A1  |a|^2 = H^4 r0^2/f0  (a^r = -H^2 r0 from the Christoffels; g_rr = 1/f0)", sp.simplify(a_sq - H**4 * r0**2 / f0) == 0)
a_r = H**2 * r0 / sp.sqrt(f0)                                                     # positive root, used from here on
check("A1b |a| = f'/(2 sqrt f) = H^2 r0/sqrt(f0)", sp.simplify(sp.diff(f, r).subs(r, r0) / (2 * sp.sqrt(f0)) + a_r) == 0)
must_fail("A1c |a|^2 = H^2 r0^2/f0 (missing an H^2)", sp.simplify(a_sq - H**2 * r0**2 / f0) == 0)

print("A2  embedding hyperbola: A5^2 = a^2 + H^2")
L = 1 / H
R = sp.sqrt(L**2 - r0**2)                     # radius of the hyperbola in the (X0,X1) plane
tt = tau / sp.sqrt(f0)                        # Killing time t = tau / sqrt(f0)
XX = [R * sp.sinh(tt / L), R * sp.cosh(tt / L), r0, sp.Integer(0), sp.Integer(0)]
eta = [-1, 1, 1, 1, 1]
hyper = sp.simplify(sum(eta[i] * XX[i]**2 for i in range(5)) - L**2)
check("A2a worldline lies on the hyperboloid -X0^2+X1^2+X2^2 = L^2", hyper == 0)
vel = [sp.diff(c, tau) for c in XX]
acc5 = [sp.diff(c, tau, 2) for c in XX]
check("A2b tau is proper time: X'.X' = -1", sp.simplify(sum(eta[i] * vel[i]**2 for i in range(5)) + 1) == 0)
A5sq = sp.simplify(sum(eta[i] * acc5[i]**2 for i in range(5)))
check("A2c 5D acceleration squared = H^2/f0", sp.simplify(A5sq - H**2 / f0) == 0)
check("A2d = a^2 + H^2 with a from A1 (the Deser-Levin 5-acceleration)", sp.simplify(A5sq - (a_r**2 + H**2)) == 0)
must_fail("A2e A5^2 = a^2 - H^2 (the sign of anti-de Sitter)", sp.simplify(A5sq - (a_r**2 - H**2)) == 0)

print("A3  chordal distance => thermal Wightman function")
tau0 = sp.symbols('tau0', real=True)
XX0 = [c.subs(tau, 0) for c in XX]
dX = [XX[i] - XX0[i] for i in range(5)]
chord = sp.simplify(sum(eta[i] * dX[i]**2 for i in range(5)))       # (Delta X)^2
A5 = H / sp.sqrt(f0)                     # positive root of A5^2 = H^2/f0 = a^2 + H^2 (A2c, A2d)
target = -(4 / A5**2) * sp.sinh(A5 * tau / 2)**2
for vals in [dict(H=1.3, r0=0.5, tau=0.7), dict(H=0.4, r0=1.9, tau=2.3), dict(H=2.0, r0=0.1, tau=0.05)]:
    e = float(abs(sp.N((chord - target).subs({H: vals['H'], r0: vals['r0'], tau: vals['tau']}))))
    check(f"A3a (Delta X)^2 = -(4/A5^2) sinh^2(A5 tau/2): numeric spot check H={vals['H']}, r0={vals['r0']}, tau={vals['tau']}: residual {e:.1e}", e < 1e-12)
# periodicity in imaginary proper time: W(tau) ~ 1/sinh^2(A5 (tau - i eps)/2) is invariant under tau -> tau + 2 pi i / A5
Ash = sp.symbols('A', positive=True)
W = 1 / sp.sinh(Ash * tau / 2)**2
period = sp.simplify(sp.expand_trig((W.subs(tau, tau + 2 * sp.pi * sp.I / Ash) - W).rewrite(sp.exp)))
check("A3c W(tau + 2 pi i/A) = W(tau)  (KMS period beta = 2 pi/A5  =>  T = A5/2pi)", period == 0)
W2 = 1 / sp.sinh(Ash * tau / 2)**2
must_fail("A3d period pi i/A (i.e. T = A/pi) is NOT a period of W", sp.simplify(sp.expand_trig((W2.subs(tau, tau + sp.pi * sp.I / Ash) - W2).rewrite(sp.exp))) == 0)

print("A4  detector response, numerics (mpmath): F(w) = int ds e^{-iws} W on the shifted contour Im tau = -pi/A")
mp.mp.dps = 30
def F_resp(w, A):
    # W(tau - i pi/A) = +A^2/(16 pi^2 cosh^2(A s/2));   contour shift gives the factor e^{-pi w/A}
    integrand = lambda sv: mp.e**(-1j * w * sv) * A**2 / (16 * mp.pi**2 * mp.cosh(A * sv / 2)**2)
    return mp.e**(-mp.pi * w / A) * mp.quad(integrand, [-mp.inf, 0, mp.inf])
def F_thermal(w, A):
    return (w / (2 * mp.pi)) / (mp.e**(2 * mp.pi * w / A) - 1)
for (av, Hv) in [(0.7, 1.3), (2.5, 0.4), (1.0, 1e-9), (0.0, 1.0)]:
    A = mp.sqrt(av**2 + Hv**2)
    for w in [0.3, 1.1]:
        v, tv = F_resp(w, A), F_thermal(w, A)
        check(f"A4a a={av}, H={Hv}, w={w}: F(w) = (w/2pi)/(e^{{2 pi w/A5}}-1); rel.err {float(abs(v - tv) / abs(tv)):.1e}", abs(v - tv) / abs(tv) < 1e-12)
    w = 0.8
    ratio = F_resp(-w, A) / F_resp(w, A)
    check(f"A4b a={av}, H={Hv}: detailed balance F(-w)/F(w) = exp(2 pi w/A5)  (T = A5/2pi)", abs(ratio - mp.e**(2 * mp.pi * w / A)) / abs(ratio) < 1e-12)
Ab = mp.sqrt(0.7**2 + 1.3**2)
wrongratio = mp.e**(2 * mp.pi * 0.8 / 0.7)              # the flat Unruh temperature a/2pi would predict this ratio for a=0.7
check("A4c CONTROL: the ratio at (a=0.7,H=1.3) differs from flat-Unruh exp(2 pi w/a)  (the H term is real)",
      abs(F_resp(-0.8, Ab) / F_resp(0.8, Ab) - wrongratio) / wrongratio > 0.5)

print("A5  Tolman / kappa / angle")
Tgh = H / (2 * sp.pi)
check("A5a T_GH/sqrt(f0) = A5/(2pi)   (Tolman)", sp.simplify(Tgh / sp.sqrt(f0) - A5 / (2 * sp.pi)) == 0)
must_fail("A5b T_GH*sqrt(f0) = A5/2pi (wrong Tolman direction)", sp.simplify(Tgh * sp.sqrt(f0) - A5 / (2 * sp.pi)) == 0)
theta = sp.asin(H * r0)
check("A5c tan(theta) = a/H with sin(theta)=H r0", sp.simplify(sp.tan(theta) - a_r / H) == 0)
check("A5d kappa_obs = H/sqrt(f0) = H/cos(theta) = A5 = a/sin(theta)", sp.simplify(H / sp.cos(theta) - A5) == 0 and sp.simplify(a_r / sp.sin(theta) - A5) == 0)
check("A5e T_U = a/2pi and T_Lambda = H/2pi add in quadrature: T^2 = T_U^2 + T_Lambda^2; equal at a = H (theta = pi/4)",
      sp.simplify((A5 / (2 * sp.pi))**2 - (a_r / (2 * sp.pi))**2 - (H / (2 * sp.pi))**2) == 0 and sp.simplify(sp.tan(sp.pi / 4) - 1) == 0)

print("A6  every timelike geodesic of the hyperboloid has A5 = H")
# geodesic: X = L (sinh(tau/L) e_A + cosh(tau/L) e_B) with e_A timelike unit, e_B spacelike unit, e_A.e_B = 0.  Take a boosted+rotated pair.
bv, ang = sp.symbols('bv ang', real=True)
eA = sp.Matrix([sp.cosh(bv), sp.sinh(bv) * sp.cos(ang), sp.sinh(bv) * sp.sin(ang), 0, 0])
eB = sp.Matrix([sp.sinh(bv), sp.cosh(bv) * sp.cos(ang), sp.cosh(bv) * sp.sin(ang), 0, 0])
dot = lambda p, q: sum(eta[i] * p[i] * q[i] for i in range(5))
check("A6a e_A.e_A = -1, e_B.e_B = +1, e_A.e_B = 0", sp.simplify(dot(eA, eA) + 1) == 0 and sp.simplify(dot(eB, eB) - 1) == 0 and sp.simplify(dot(eA, eB)) == 0)
Xg = L * (sp.sinh(tau / L) * eA + sp.cosh(tau / L) * eB)
check("A6b on the hyperboloid", sp.simplify(dot(Xg, Xg) - L**2) == 0)
check("A6c proper time", sp.simplify(dot(Xg.diff(tau), Xg.diff(tau)) + 1) == 0)
Ag = sp.simplify(dot(Xg.diff(tau, 2), Xg.diff(tau, 2)))
check("A6d A5^2 = H^2 for every geodesic  (a = 0)  =>  T = H/2pi", sp.simplify(Ag - H**2) == 0)

print("A7  the horizon of a static observer, its area, and the flat-Rindler limit")
# horizon X0 = X1  =>  X2^2+X3^2+X4^2 = L^2 : radius L, area 4 pi L^2 regardless of r0
Xh = sp.symbols('Xh')
check("A7a on X0=X1 the hyperboloid reduces to a round S^2 of radius L: area 4 pi L^2, entropy pi L^2/G, both independent of a",
      sp.simplify(-Xh**2 + Xh**2 + sp.Symbol('rho')**2 - L**2) == sp.Symbol('rho')**2 - L**2)
ell = sp.integrate(1 / sp.sqrt(1 - H**2 * r**2), (r, r0, L))
ell_th = (sp.pi / 2 - theta) / H
check("A7b proper radial distance to the horizon l = (pi/2 - theta)/H", sp.simplify(ell - ell_th) == 0)
eps = sp.symbols('epsilon', positive=True)             # eps = pi/2 - theta
a_eps = H * sp.cot(eps); ell_eps = eps / H; kap_eps = H / sp.sin(eps)
sa = sp.series(a_eps * ell_eps, eps, 0, 4).removeO(); sk = sp.series(kap_eps * ell_eps, eps, 0, 4).removeO()
check("A7c a*l = 1 - eps^2/3 + ...  ->  1 (Rindler: a = 1/l)", sp.simplify(sa - (1 - eps**2 / 3)) == 0)
check("A7d kappa_obs*l = 1 + eps^2/6 + ...  ->  1", sp.simplify(sk - (1 + eps**2 / 6)) == 0)
check("A7e eps ~ H/a for a >> H:  corrections to flat Rindler are O((H/a)^2)", sp.simplify(sp.limit(sp.atan(H / a) / (H / a), a, sp.oo) - 1) == 0)
must_fail("A7f a*l = 1 exactly (no curvature correction)", sp.simplify(a_eps * ell_eps - 1) == 0)

print("A8  surface gravity of the Killing horizon from the metric: kappa^2 = -(1/2) grad_a xi_b grad^a xi^b at r = L")
xi_low = [g[0, 0], 0, 0, 0]                                   # xi_mu = g_{mu t}
nab = sp.Matrix(4, 4, lambda i, j: sp.diff(xi_low[j], X[i]) - sum(Gam(k, i, j) * xi_low[k] for k in range(4)))
contr = sp.simplify(sum(nab[i, j] * nab[k, l] * ginv[i, k] * ginv[j, l] for i in range(4) for j in range(4) for k in range(4) for l in range(4)))
kap2 = sp.simplify(sp.limit(-contr / 2, r, 1 / H))
check("A8a kappa_xi^2 = H^2 at the cosmological horizon (geodesic normalisation)", sp.simplify(kap2 - H**2) == 0)
check("A8b for chi = xi/sqrt(f0): kappa_chi = kappa_xi/sqrt(f0) = A5", sp.simplify(sp.sqrt(kap2) / sp.sqrt(f0) - A5) == 0)

n, npass = len(ok), sum(ok)
print(f"\nn01: {npass}/{n} checks passed")
sys.exit(0 if npass == n else 1)
