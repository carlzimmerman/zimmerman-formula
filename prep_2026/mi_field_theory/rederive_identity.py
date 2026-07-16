#!/usr/bin/env python3
r"""
INDEPENDENT RE-DERIVATION OF THE TWO LOAD-BEARING KINEMATIC FACTS OF THE
de Sitter-Unruh MODIFIED-INERTIA ACTION (Zimmerman framework).
================================================================================
Framework action (MI_COMPLETION_WRITTEN_2026-07.md Sec 2, line 20):

    S_matter = -(1/2) INT sqrt(-g) rho_m [ s u^mu K(Box_u/a0^2) u_mu ],
    K(z) = (sqrt(1+4z)-1)/(2 sqrt z),   Box_u f = u^a grad_a(u^b grad_b f),
    s = -1 (POSTULATE), a0 = c H_Lambda / Z = 9.36e-11 m/s^2 (canonical, rho_DE),
    ALT footing rho_total/cH0 -> 1.13e-10.   Own interpolation nu(y)=sqrt(1+1/y).

This script re-derives, from scratch and WITHOUT trusting any banked result:

  [I]   THE FIRST-MOMENT IDENTITY   u_mu Box_u u^mu = -|a|^2 .
        Question the task poses: is it WORLDLINE-GENERAL, or does it secretly
        need circularity?  Answer, established three independent ways:
          (A) flat space, FULLY GENERAL worldline, OFF-shell master identity;
          (B) GENERAL curved metric (arbitrary g_ab(x)), FULLY GENERAL worldline,
              off-shell master identity -- pure metric compatibility, no orbit shape;
          (C) a CONCRETE curved, non-geodesic, NON-circular worldline
              (static Schwarzschild observer) evaluated in closed form.
        Verdict printed: worldline-general (unit norm + metric compatibility only;
        NO circularity, NO geodesy, NO Killing vector).

  [II]  THE FIRST-MOMENT CLOSURE     K(Box_u/a0^2) -> K(a^2/a0^2) = mu_fw(|a|/a0),
        and the exact inversion of the circular balance to g_obs = nu(y) g_bar.
        PLUS the honesty check: the moment expansion is UNCONTROLLED beyond n=1
        (the literal helix channel differs at O(1)), so the reduction is the exact
        FIRST moment and nothing more -- the higher-moment/off-circular closure is
        genuinely FREE. We reproduce the divergence of the moments independently.

RULES honored: verify a WIN as hard as a DEFICIT; both a0 footings where a scale
enters; reason from the framework's own premises; every load-bearing step is a
sympy check with NO hard-coded booleans; exit 0 iff every check passes.
"""
import sympy as sp
import numpy as np

PASS = True
def check(name, cond):
    global PASS
    ok = bool(cond)
    print(f"   [{'PASS' if ok else 'FAIL'}] {name}")
    if not ok:
        PASS = False

C_LIGHT = 2.99792458e8
A0_DE, A0_TOT = 9.36e-11, 1.13e-10
FOOTINGS = [("rho_DE canonical cH_Lambda/Z", A0_DE), ("rho_total/cH0 alt", A0_TOT)]

# =====================================================================================
print("#"*100)
print("# [I.A] FLAT SPACE, FULLY GENERAL WORLDLINE -- the OFF-SHELL master identity")
print("#"*100)
# u^mu(tau) are ARBITRARY functions of proper time -- NOT a helix, NOT circular, NOT
# constrained. eta = diag(-1,1,1,1). a^mu = du/dtau, Box_u u^mu = d^2u/dtau^2 (flat: the
# directional derivative along u reduces to d/dtau on a worldline-supported field).
tau = sp.symbols('tau', real=True)
uf   = [sp.Function(f'u{i}')(tau) for i in range(4)]
eta  = sp.diag(-1, 1, 1, 1)
dot_e = lambda p, q: sum(eta[i, i]*p[i]*q[i] for i in range(4))
u_v  = sp.Matrix(uf)
a_v  = u_v.diff(tau)          # a^mu = Du^mu/dtau  (flat)
box_u_v = a_v.diff(tau)       # Box_u u^mu = D^2 u^mu / dtau^2 (flat)

# MASTER OFF-SHELL IDENTITY (no constraint imposed):
#     d/dtau (u.a)  ==  a.a + u.(Box_u u)
master_flat = sp.simplify(sp.diff(dot_e(u_v, a_v), tau) - (dot_e(a_v, a_v) + dot_e(u_v, box_u_v)))
check("OFF-SHELL: d/dtau(u.a) = a.a + u.(Box_u u) for ARBITRARY worldline (flat)",
      master_flat == 0)
print("""
   => This is pure Leibniz: it used NOTHING about the orbit (not circular, not geodesic,
      not periodic). On the constraint surface u.u = -1 (const), d/dtau(u.u)=2 u.a = 0,
      so u.a = 0 and d/dtau(u.a)=0, hence  u.(Box_u u) = -|a|^2.  Worldline-general.""")

# =====================================================================================
print("#"*100)
print("# [I.B] GENERAL CURVED METRIC, GENERAL WORLDLINE -- metric compatibility does it all")
print("#"*100)
# Arbitrary 2D Lorentzian metric g_ab(x^0,x^1) (2D suffices to exhibit every Christoffel
# structure; the argument is dimension-blind). Arbitrary worldline x^a(tau). We build the
# covariant derivative ALONG the curve, D V^a/dtau = dV^a/dtau + Gamma^a_bc u^b V^c, and
# verify the SAME off-shell master identity -- now with a NONTRIVIAL connection.
x0, x1 = sp.symbols('x0 x1', real=True)
coords = [x0, x1]
# generic symmetric metric with coordinate dependence (kept invertible & Lorentzian generically)
g00 = sp.Function('g00')(x0, x1)
g01 = sp.Function('g01')(x0, x1)
g11 = sp.Function('g11')(x0, x1)
g   = sp.Matrix([[g00, g01], [g01, g11]])
ginv = g.inv()
# Christoffels Gamma^a_bc = 1/2 g^ad (d_b g_dc + d_c g_db - d_d g_bc)
def christoffel(a, b, c):
    s = 0
    for d in range(2):
        s += ginv[a, d]*(sp.diff(g[d, c], coords[b]) + sp.diff(g[d, b], coords[c]) - sp.diff(g[b, c], coords[d]))
    return sp.Rational(1, 2)*s
Gam = [[[sp.simplify(christoffel(a, b, c)) for c in range(2)] for b in range(2)] for a in range(2)]

# arbitrary worldline
X = [sp.Function('X0')(tau), sp.Function('X1')(tau)]
u = [sp.diff(X[a], tau) for a in range(2)]           # u^a = dx^a/dtau

def covD(V):
    """D V^a/dtau along the worldline = dV^a/dtau + Gamma^a_bc u^b V^c, evaluated on x=X(tau)."""
    out = []
    for a in range(2):
        term = sp.diff(V[a], tau)
        for b in range(2):
            for c in range(2):
                Gsub = Gam[a][b][c].subs({x0: X[0], x1: X[1]}, simultaneous=True)
                term += Gsub*u[b]*V[c]
        out.append(term)
    return out

def gdot(P, Q):
    """g_ab P^a Q^b evaluated on the worldline."""
    gsub = g.subs({x0: X[0], x1: X[1]}, simultaneous=True)
    return sum(gsub[a, b]*P[a]*Q[b] for a in range(2) for b in range(2))

a_cov   = covD(u)          # a^a = D u^a/dtau (proper acceleration, curved)
box_cov = covD(a_cov)      # Box_u u^a = D a^a/dtau  = u^c nabla_c(u^b nabla_b u^a)

lhs = sp.diff(gdot(u, a_cov), tau)
rhs = gdot(a_cov, a_cov) + gdot(u, box_cov)
master_curved = sp.simplify(lhs - rhs)
check("OFF-SHELL curved: d/dtau(u.a) = a.a + u.(Box_u u), ARBITRARY g_ab(x) & worldline",
      master_curved == 0)
print("""
   => The ONLY inputs were (i) the product rule and (ii) metric compatibility built into
      Gamma (nabla g = 0). No circularity, no geodesy, no symmetry of g. On-shell u.u=-1
      => u.a=0 => u.(Box_u u) = -|a|^2 in ANY spacetime, for ANY timelike worldline.
      This is the derivational backbone of the RAR in the framework, re-derived from scratch.""")

# =====================================================================================
print("#"*100)
print("# [I.C] CONCRETE curved, NON-geodesic, NON-circular check: static Schwarzschild observer")
print("#"*100)
# A static observer sits still at fixed r: manifestly NOT circular, NOT freely falling.
# If the identity needed circularity it would fail here. It does not.
M, r, th = sp.symbols('M r theta', positive=True)
t, rr, tht, ph = sp.symbols('t r_c theta_c phi_c', real=True)
f = 1 - 2*M/r
gS = sp.diag(-f, 1/f, r**2, r**2*sp.sin(th)**2)     # Schwarzschild (t,r,theta,phi)
coordsS = [t, rr, tht, ph]
gS_c = gS.subs({r: rr, th: tht})
gSinv = gS_c.inv()
def christ_S(a, b, c):
    s = 0
    for d in range(4):
        s += gSinv[a, d]*(sp.diff(gS_c[d, c], coordsS[b]) + sp.diff(gS_c[d, b], coordsS[c]) - sp.diff(gS_c[b, c], coordsS[d]))
    return sp.simplify(sp.Rational(1, 2)*s)

# static unit observer: u^mu = (1/sqrt(f), 0,0,0), with u.u = -f*(u^t)^2 = -1
uS = [1/sp.sqrt(f.subs(r, rr)), 0, 0, 0]
uu = sp.simplify(sum(gS_c[i, j]*uS[i]*uS[j] for i in range(4) for j in range(4)))
check("static Schwarzschild observer is unit-timelike (u.u = -1)", sp.simplify(uu + 1) == 0)

# a^mu = u^c nabla_c u^mu = u^t(d_t u^mu=0) + Gamma^mu_ct u^c u^t = Gamma^mu_tt (u^t)^2
a_S = []
for mu in range(4):
    term = 0
    for c in range(4):
        term += christ_S(mu, c, 0)*uS[c]*uS[0]     # only u^t=uS[0] nonzero
    a_S.append(sp.simplify(term))
# Box_u u^mu = u^c nabla_c a^mu = Gamma^mu_c d u^c a^d  (a static, d_t a=0)
box_S = []
for mu in range(4):
    term = 0
    for c in range(4):
        for d in range(4):
            term += christ_S(mu, c, d)*uS[c]*a_S[d]
    box_S.append(sp.simplify(term))
uBu_S  = sp.simplify(sum(gS_c[i, j]*uS[i]*box_S[j] for i in range(4) for j in range(4)))
amag2_S = sp.simplify(sum(gS_c[i, j]*a_S[i]*a_S[j] for i in range(4) for j in range(4)))
check("Schwarzschild: |a|^2 = (M/r^2)^2 / f  (known surface-gravity magnitude^2)",
      sp.simplify(amag2_S - (M/rr**2)**2/f.subs(r, rr)) == 0)
check("Schwarzschild static observer: u.(Box_u u) = -|a|^2 EXACTLY (curved, non-circular)",
      sp.simplify(uBu_S + amag2_S) == 0)
print(f"   closed form: u.Box_u u = {uBu_S},   -|a|^2 = {-amag2_S}")
print("""
   VERDICT [I]: u_mu Box_u u^mu = -|a|^2 is WORLDLINE-GENERAL. Inputs = unit norm + metric
   compatibility ONLY. It does NOT need circularity, geodesy, periodicity, or any spacetime
   symmetry. The <Box_u>_u first spectral moment is +|a|^2 for every timelike worldline.""")

# =====================================================================================
print("#"*100)
print("# [II] THE FIRST-MOMENT CLOSURE: K(a^2/a0^2)=mu_fw and the exact g_obs=nu(y) g_bar")
print("#"*100)
z, xx, y = sp.symbols('z x y', positive=True)
K   = (sp.sqrt(1 + 4*z) - 1)/(2*sp.sqrt(z))     # published kernel
mu  = (sp.sqrt(1 + 4*xx**2) - 1)/(2*xx)         # inertia dressing mu_fw(x), x=a/a0
nu  = sp.sqrt(1 + 1/y)                           # framework's OWN nu(y), y=g_bar/a0

check("K(0+) = 0 (deep-MOND: DC/time part drops)", sp.limit(K, z, 0, '+') == 0)
check("K(+oo) = 1 (Newtonian UV limit)", sp.limit(K, z, sp.oo) == 1)
check("first-moment substitution z=x^2 gives K(x^2) = mu_fw(x) exactly",
      sp.simplify(K.subs(z, xx**2) - mu) == 0)

# circular balance mu_fw(x)*x = y inverts EXACTLY to x = y*nu(y) => g_obs = nu(y) g_bar
step_x2 = sp.simplify((y*nu)**2 - (y**2 + y))                       # x^2 = y^2+y
collapse = sp.simplify((sp.sqrt(sp.factor(1 + 4*(y**2 + y))) - 1)/2 - y)  # sqrt((2y+1)^2)=2y+1
check("x^2 = y^2 + y  at  x = y*nu(y)  (the nested radical collapses)", step_x2 == 0)
check("mu_fw(y*nu)*(y*nu) - y = 0 exactly  =>  g_obs = nu(y) g_bar at EVERY radius", collapse == 0)

# numeric ring residual across 8 decades, both footings (footing enters only via y):
ys   = np.logspace(-4, 4, 400)
mu_n = lambda q: (np.sqrt(1 + 4*q**2) - 1)/(2*q)
nu_n = lambda q: np.sqrt(1 + 1/q)
res  = np.abs(mu_n(ys*nu_n(ys))*(ys*nu_n(ys))/ys - 1.0)
print(f"   numeric ring residual over y in [1e-4,1e4]: max = {res.max():.2e}")
check("ring law is algebraic (residual < 1e-12: no radius mixing, no field equation)",
      res.max() < 1e-12)

# g_obs = sqrt(g_bar^2 + g_bar a0) identity (framework's stated RAR form), both footings:
for lab, a0 in FOOTINGS:
    gb = np.logspace(-13, -8, 200)
    g_from_nu = nu_n(gb/a0)*gb
    g_rar     = np.sqrt(gb**2 + gb*a0)
    rel = np.max(np.abs(g_from_nu/g_rar - 1))
    check(f"[{lab}] nu(y)*g_bar == sqrt(g_bar^2+g_bar a0) to <1e-12", rel < 1e-12)

# =====================================================================================
print("#"*100)
print("# [II.b] HONESTY: the moment expansion is UNCONTROLLED beyond n=1 (closure is FREE)")
print("#"*100)
# On the exact helix u=(g, g v cos w t, g v sin w t, 0) [c=1], compute u.(Box_u)^n u and
# compare to the prescription (a^2)^n (u.u). They agree ONLY at n=1 (the first moment); the
# ratio blows up like (1/v^2)^{n-1}, so the reduction is the exact FIRST moment and no more.
vv, om = sp.symbols('v omega', positive=True)
gam = 1/sp.sqrt(1 - vv**2)
u_h = sp.Matrix([gam, gam*vv*sp.cos(om*tau), gam*vv*sp.sin(om*tau), 0])
check("helix is unit-timelike (u.u=-1)", sp.simplify(dot_e(list(u_h), list(u_h)) + 1) == 0)
amag2_h = sp.simplify(dot_e(list(u_h.diff(tau)), list(u_h.diff(tau))))
print("   moment table  u.(Box_u)^n u  vs  prescription (a^2)^n (u.u):")
ratios = {}
for n in (1, 2, 3):
    exact_n = sp.simplify(dot_e(list(u_h), list(u_h.diff(tau, 2*n))))
    presc_n = sp.simplify((amag2_h)**n * dot_e(list(u_h), list(u_h)))
    ratios[n] = sp.simplify(exact_n/presc_n)
    print(f"     n={n}: exact={exact_n},  ratio exact/prescription = {ratios[n]}")
check("n=1 moment ratio = 1 (first-moment closure is EXACT)", sp.simplify(ratios[1] - 1) == 0)
check("n=2 moment ratio = 1 - 1/v^2 (i.e. -1/(gamma^2 v^2): diverges as v->0 => uncontrolled)",
      sp.simplify(ratios[2] - (1 - 1/vv**2)) == 0)
# literal frequency channel |K(-w^2)| = 1 (no MOND) -- the reduction is a genuine CHOICE:
Kn = sp.lambdify(z, K, 'numpy')
w_gal = C_LIGHT/1.5e5
Klit = abs(complex(Kn(complex(-(w_gal**2), 1.0))))
print(f"   literal channel at galactic w=c/v: |K(-w^2+i0)| = {Klit:.9f}  vs  K(1)={float(Kn(1.0)):.4f}")
check("literal frequency closure gives |K|~1 (NO MOND) => the O(1) closure choice is real, not cosmetic",
      abs(Klit - 1) < 1e-3)
print("""
   => The prescription K(Box_u/a0^2) -> K(|a|^2/a0^2) is the EXACT first spectral moment
      (n=1) and provably NOT the literal operator (which differs at O(1) and gives no MOND).
      On a circle every first-moment closure coincides (|a| constant); off circles the
      time-weighting of |a(tau)|^2 is FREE. This is the theory's genuine open structure --
      re-derived here, not asserted: the RAR is derived, the off-circular closure is not.""")

print("="*100)
print(f" REDERIVE_IDENTITY RESULT: {'ALL CHECKS PASS' if PASS else 'A CHECK FAILED'}")
print("="*100)
import sys
sys.exit(0 if PASS else 1)
