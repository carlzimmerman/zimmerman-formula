#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
LANE W -- IS THE a_0-LINE THE WARD IDENTITY OF BROKEN BOOSTS?
=============================================================
mi_goldstone_ward_2026.py

Question (never asked in this corpus): the ghost condensate spontaneously breaks
BOOSTS (u_mu = d_mu phi / sqrt(-X) picks a frame) while shift symmetry survives.
Broken symmetries come with Ward identities that fix normalisations. Is the kernel
SHAPE of g_obs^2 = g_bar^2 + a_0 g_bar a CONSEQUENCE of the broken boost symmetry,
i.e. is the a_0-line a Ward identity rather than a postulate?

Setup: point-particle EFT of a probe worldline in the condensate background, a la
Nicolis-Penco-Piazza-Rattazzi (2015):

    S = -m Int dtau + c1 Int dtau (u.xdot) + c2 Int dtau (u.xdot)^2
        + [operators first order in d_mu u_nu]

Every algebraic step below is verified in sympy. Signature mostly-plus diag(-1,+1,..).

VERDICT PROVEN BELOW (honest outcomes (b) AND (c), NOT (a)):
  * velocity sector: the symmetry allows a FAMILY. Through the stated order there are
    2 free worldline couplings (c1, c2) plus 3 independent one-du tensor structures,
    each with an a-priori free function of (u.xdot). Ward identities fix RELATIONS
    (the probe-Goldstone vertex equals the boost-charge deficit p - vE, for ANY c1,c2),
    never the VALUES. Zero coefficients are forced.
  * acceleration sector: acceleration-dependent inertia CANNOT arise at this order.
    (i) operators LINEAR in xddot are total tau-derivatives in the homogeneous
        background (since d_mu u_nu = 0 there) -- no EOM contribution at all;
    (ii) operators QUADRATIC in xddot are Ostrogradsky-unbounded non-perturbatively,
        and perturbatively reduce on-shell to POSITION-dependent (analytic-in-eps)
        inertia corrections, never the non-analytic m(|a|) a MOND floor needs;
    (iii) every u-contraction of the acceleration is exactly (gamma v/c)-suppressed:
        u.xddot = gamma*v * sqrt(xddot.xddot) EXACTLY (1+1D) -- this independently
        reproduces the corpus Frenet-torsion fact |a|/B = v/c from the EFT side.
  So the a_0-line is NOT the Ward identity of broken boosts. The kernel stays a
  postulate; the 30.6% shape systematic does NOT collapse; and no a_0 (canonical
  9.3614e-11 OR ALT 1.13e-10 -- the no-go is footing-independent) is generated.

KAPPA STATUS: kappa = 1/2 is FITTED, NOT DERIVED. Nothing here derives it; this lane
returns a no-go, consistent with that standing.

MANDATORY CREDIT: nu = sqrt(1+1/y) and the dS-Unruh balance are Milgrom 1999 PLA
253:273 eqs 6-9; his eqs 10-11 give a second coefficient; Milgrom 2008
arXiv:0801.3133 sec 7.3.1 notes the mismatch "isn't necessarily meaningful".
a_lambda = c^2 sqrt(Lambda/3): Milgrom 1994 Ann.Phys. 229:384. Temperature
sqrt(a^2 + Lambda/3)/2pi: Narnhofer-Peter-Thirring 1996 IJMPB 10:1507.
Five-acceleration: Deser-Levin 1997 CQG 14:L163. Ghost condensate:
Arkani-Hamed-Cheng-Luty-Mukohyama 2004. Boost-breaking EFT zoology:
Nicolis-Penco-Piazza-Rattazzi 2015. Empirical a_0 = 1.2e-10: McGaugh / SPARC.
"""

import sys
import sympy as sp

RESULTS = []


def check(name, cond):
    ok = bool(cond)
    RESULTS.append(ok)
    print(("[OK]   " if ok else "[FAIL] ") + name)
    return ok


w = sp.Symbol('w_dummy', real=True)  # universal dummy for composed derivatives

print("=" * 78)
print("LANE W: is the a_0-line the Ward identity of broken boosts?")
print("=" * 78)

# ---------------------------------------------------------------------------
# SECTION 0 -- footings (the result below is footing-INDEPENDENT; both reported)
# ---------------------------------------------------------------------------
print("\n--- Section 0: footings (both reported; no-go applies to both equally) ---")
a0_canonical = 9.3614e-11   # kappa=1/2, rho_DE + cH_Lambda   [m/s^2]
a0_alt = 1.13e-10           # ALT footing (x1.2082)
cHL = 5.4194e-10            # c H_Lambda [m/s^2]
Z = 5.7888100366            # 2 sqrt(8 pi/3)
r_canonical = 2 * cHL / a0_canonical
r_alt = 2 * cHL / a0_alt
print(f"  canonical a_0 = {a0_canonical:.4e}  -> r = 2 cH_L/a_0 = {r_canonical:.6f}")
print(f"  ALT       a_0 = {a0_alt:.4e}  -> r = {r_alt:.6f}")
check("footing cross-check: canonical r equals 2Z to <0.1% (master-formula tie-in)",
      abs(r_canonical - 2 * Z) / (2 * Z) < 1e-3)

# ---------------------------------------------------------------------------
# SECTION 1 -- the condensate: identities that organise the EFT
# ---------------------------------------------------------------------------
print("\n--- Section 1: condensate identities (generic phi, no background assumed) ---")

# (C) u.u = -1 identically, 4D, GENERIC phi
t4, x4, y4, z4 = sp.symbols('t4 x4 y4 z4', real=True)
coords4 = [t4, x4, y4, z4]
phi4 = sp.Function('phi4')(*coords4)
g4 = sp.diag(-1, 1, 1, 1)
g4i = g4.inv()
dphi4 = sp.Matrix([sp.diff(phi4, c) for c in coords4])
X4 = (dphi4.T * g4i * dphi4)[0, 0]
u4 = dphi4 / sp.sqrt(-X4)                      # u_mu (lower)
uu4 = sp.simplify((u4.T * g4i * u4)[0, 0])
check("u.u == -1 IDENTICALLY for generic phi (4D): the condensate generates the "
      "preferred timelike vector", uu4 == -1)

# (C) u^nu d_mu u_nu == 0 identically (2D generic phi; dimension-independent identity
#     since it is d_mu(u.u)/2)
t2, x2 = sp.symbols('t2 x2', real=True)
crd2 = [t2, x2]
g2 = sp.diag(-1, 1)          # own inverse


def condensate_2d(phi_expr):
    """u_lower, u_upper, D[mu][nu] = d_mu u_nu for a given phi(t2,x2)."""
    dphi = [sp.diff(phi_expr, c) for c in crd2]
    X = -dphi[0] ** 2 + dphi[1] ** 2
    N = sp.sqrt(-X)
    u_lo = [dphi[0] / N, dphi[1] / N]
    u_up = [-u_lo[0], u_lo[1]]
    D = [[sp.diff(u_lo[nu], crd2[mu]) for nu in range(2)] for mu in range(2)]
    return u_lo, u_up, D


phi2g = sp.Function('phi2g')(t2, x2)
u_lo_g, u_up_g, D_g = condensate_2d(phi2g)
proj = [sp.simplify(sum(u_up_g[nu] * D_g[mu][nu] for nu in range(2)))
        for mu in range(2)]
check("u^nu d_mu u_nu == 0 identically (generic phi, both mu): kills every "
      "contraction whose SECOND slot is u", all(pr == 0 for pr in proj))

# (C) homogeneous background phi = M^2 t: u_mu = (1,0,0,0), d_mu u_nu = 0
M = sp.Symbol('M', positive=True)
phib = M ** 2 * t4
dphib = sp.Matrix([sp.diff(phib, c) for c in coords4])
Xb = (dphib.T * g4i * dphib)[0, 0]
ub = sp.simplify(dphib / sp.sqrt(-Xb))
du_zero = all(sp.simplify(sp.diff(ub[n], c)) == 0 for n in range(4) for c in coords4)
check("background phi = M^2 t: u_mu = (1,0,0,0) and d_mu u_nu == 0 exactly "
      "(so ALL one-du operators VANISH in the background)",
      ub == sp.Matrix([1, 0, 0, 0]) and du_zero)

# (C) FRW: shift current a^3 P'(X) phidot conserved on the P(X) EOM (attractor P'=0)
tc = sp.Symbol('t_cos', real=True)
af = sp.Function('a_scale', positive=True)(tc)
vf = sp.Function('varphi')(tc)
Pf = sp.Function('P')
Xfrw = -sp.diff(vf, tc) ** 2                       # mostly-plus X for homogeneous phi
Lfrw = af ** 3 * Pf(Xfrw)
dL_dphidot = sp.diff(Lfrw, sp.diff(vf, tc))
EL_frw = sp.diff(dL_dphidot, tc)                   # shift symmetry: no dL/dphi term
Pp_frw = sp.diff(Pf(w), w).subs(w, Xfrw)
J = af ** 3 * Pp_frw * sp.diff(vf, tc)
ok_current = (sp.simplify(dL_dphidot + 2 * J) == 0 and
              sp.simplify(EL_frw + 2 * sp.diff(J, tc).doit()) == 0)
check("FRW EOM integrates to a^3 P'(X) phidot = const (shift current; attractor "
      "P'(X)=0 dynamically selects phidot)", ok_current)

# ---------------------------------------------------------------------------
# SECTION 2 -- point 1: enumerate the operators
# ---------------------------------------------------------------------------
print("\n--- Section 2: operator enumeration through (u.xdot)^2 and one d_mu u_nu ---")
print("  Zeroth order in du: 1 (mass), (u.xdot), (u.xdot)^2  ->  m, c1, c2")
print("  One du: contractions a^mu b^nu d_mu u_nu with a,b in {u, xdot}, plus trace")

chi0 = sp.Rational(2, 5)
xdt2 = [sp.cosh(chi0), sp.sinh(chi0)]              # sample unit worldline vector


def contractions(phi_expr, xvec):
    u_lo, u_up, D = condensate_2d(phi_expr)
    vecs = {'u': u_up, 'x': list(xvec)}
    out = {}
    for an, av in vecs.items():
        for bn, bv in vecs.items():
            out[an + bn] = sum(av[mu] * bv[nu] * D[mu][nu]
                               for mu in range(2) for nu in range(2))
    out['tr'] = -D[0][0] + D[1][1]                 # g^{mu nu} d_mu u_nu
    return out


# symbolic: which vanish identically for GENERIC phi? Work in derivative SYMBOLS
# (p_t, p_x, p_tt, p_tx, p_xx) so the zero-test is pure algebra, and use an
# ARBITRARY symbolic first-slot vector (stronger than the unit worldline sample).
p_t, p_x, p_tt, p_tx, p_xx = sp.symbols('p_t p_x p_tt p_tx p_xx', real=True)
a0s, a1s = sp.symbols('a0s a1s', real=True)


def desym(e):
    d2 = {sp.Derivative(phi2g, (t2, 2)): p_tt,
          sp.Derivative(phi2g, t2, x2): p_tx,
          sp.Derivative(phi2g, (x2, 2)): p_xx}
    d1 = {sp.Derivative(phi2g, t2): p_t, sp.Derivative(phi2g, x2): p_x}
    return e.subs(d2).subs(d1)


con_g = {k: desym(vv) for k, vv in contractions(phi2g, [a0s, a1s]).items()}
vanish = sorted(k for k, vv in con_g.items() if sp.simplify(sp.cancel(vv)) == 0)
survive = sorted(k for k in con_g if k not in vanish)
print(f"  raw contractions: 5;  vanish identically: {vanish};  survive: {survive}")
check("EXACTLY the two second-slot-u contractions {uu, xu} vanish identically "
      "(for an ARBITRARY first-slot vector); 3 independent structures survive: "
      "{u^m x^n d_m u_n, x^m x^n d_m u_n, d.u}",
      vanish == ['uu', 'xu'] and survive == ['tr', 'ux', 'xx'])

# generic non-vanishing of the survivors: concrete phi with all second derivatives on
phi_conc = t2 + t2 * x2 ** 2 / 10 + x2 ** 3 / 30 + x2 * t2 ** 2 / 20
con_c = contractions(phi_conc, xdt2)
pt_sub = {t2: sp.Rational(1, 3), x2: sp.Rational(2, 3)}
vals = {k: float(sp.N(v.subs(pt_sub))) for k, v in con_c.items()}
check("survivors are GENERICALLY nonzero (concrete phi, |value| > 1e-8) while the "
      "killed pair stay < 1e-12 -- the enumeration is not vacuous",
      all(abs(vals[k]) > 1e-8 for k in ('ux', 'xx', 'tr')) and
      all(abs(vals[k]) < 1e-12 for k in ('uu', 'xu')))
print("  => free coefficient count at this order: m, c1, c2 PLUS 3 structures x free")
print("     function of (u.xdot). None of them is fixed by anything yet.")
print("  => AND all 3 one-du structures vanish exactly in the homogeneous background")
print("     (Section 1), so the background dispersion depends on c1, c2 alone.")

# ---------------------------------------------------------------------------
# SECTION 3 -- the broken symmetry: exact invariance with the Goldstone shift
# ---------------------------------------------------------------------------
print("\n--- Section 3: boosts are broken by the background, restored by the Goldstone ---")

chi, eta = sp.symbols('chi eta', real=True)
m, c1, c2 = sp.symbols('m c1 c2', real=True, positive=True)

# original frame: phi = t  ->  u_mu = (1,0);  xdot^mu = (cosh chi, sinh chi)
U0 = sp.cosh(chi)                                   # u.xdot = u_mu xdot^mu
# boosted scalar: phi'(t,x) = t cosh(eta) - x sinh(eta)  = t + pi'(t,x)
#   pi'(t,x) = t(cosh eta - 1) - x sinh eta   <- the Goldstone shift
# rebuild u from phi':  dphi' = (cosh eta, -sinh eta), X' = -1
up_lo = sp.Matrix([sp.cosh(eta), -sp.sinh(eta)])
xdp = sp.Matrix([sp.cosh(chi + eta), sp.sinh(chi + eta)])   # boosted worldline
U1 = (up_lo.T * xdp)[0, 0]
check("(u.xdot) EXACTLY invariant under boost + Goldstone shift "
      "pi' = t(cosh eta - 1) - x sinh eta (finite eta, no expansion)",
      sp.simplify(U1 - U0) == 0)

residual = sp.expand((-m + c1 * U1 + c2 * U1 ** 2) - (-m + c1 * U0 + c2 * U0 ** 2))
res_simp = sp.simplify(residual)
no_constraint = (res_simp == 0 and sp.diff(residual, c1) is not None and
                 sp.simplify(sp.diff(residual, c1)) == 0 and
                 sp.simplify(sp.diff(residual, c2)) == 0)
check("delta S == 0 for SYMBOLIC (m, c1, c2): the broken symmetry imposes ZERO "
      "relations among the Wilson coefficients -- a FAMILY survives (outcome b)",
      no_constraint)

# falsifiability control: an operator built with an explicit frame index (NOT via u)
ctrl = (sp.cosh(chi + eta) ** 2 - sp.cosh(chi) ** 2).subs(
    {chi: sp.Rational(3, 10), eta: sp.Rational(1, 2)})
check("CONTROL (this detector can fail): frame-built operator (xdot^0)^2 is NOT "
      "invariant under the same transformation (residual != 0)",
      abs(float(sp.N(ctrl))) > 1e-6)

# ---------------------------------------------------------------------------
# SECTION 4 -- point 2: the dispersion / effective inertia from c1, c2
# ---------------------------------------------------------------------------
print("\n--- Section 4: weak-field slow-motion dispersion from S = Int dtau[-m + c1 U + c2 U^2] ---")

v = sp.Symbol('v', positive=True)
gam = 1 / sp.sqrt(1 - v ** 2)
# background U = gamma; dtau = dt/gamma:
L = -m / gam + c1 + c2 * gam
ser = sp.expand(sp.series(L, v, 0, 6).removeO())
meff = sp.simplify(2 * ser.coeff(v, 2))
check("effective inertia m_eff = m + c2: a VELOCITY-sector mass renormalisation "
      "(c1 is a constant -- chemical-potential-like, drops from the EOM)",
      sp.simplify(meff - (m + c2)) == 0)
check("v^4 coefficient = (m + 3 c2)/8: inertia is VELOCITY-dependent at higher "
      "order, never acceleration-dependent",
      sp.simplify(ser.coeff(v, 4) - (m + 3 * c2) / 8) == 0)

p_of_v = sp.diff(L, v)
E_of_v = sp.simplify(p_of_v * v - L)
check("Hamiltonian consistency dE/dp == v for the modified dispersion",
      sp.simplify(sp.diff(E_of_v, v) / sp.diff(p_of_v, v) - v) == 0)

# theorem: NO first-derivative worldline Lagrangian gives acceleration-dependent inertia
tg = sp.Symbol('t_g', real=True)
qg = sp.Function('q_g')(tg)
Lgen = sp.Function('L_gen')
qd = sp.diff(qg, tg)
qdd = sp.diff(qg, tg, 2)
ELg = sp.diff(sp.diff(Lgen(qg, qd), qd), tg) - sp.diff(Lgen(qg, qd), qg)
kernel = sp.diff(ELg, qdd)
check("THEOREM: for ANY L(q, qdot) the EOM is AFFINE in acceleration with inertia "
      "kernel d2L/dv2 = f(q, v) only -- m(|a|) is IMPOSSIBLE in this operator class",
      sp.simplify(sp.diff(ELg, qdd, 2)) == 0 and kernel != 0
      and not kernel.has(qdd))

# ---------------------------------------------------------------------------
# SECTION 5 -- acceleration operators: the three-way no-go (outcome c)
# ---------------------------------------------------------------------------
print("\n--- Section 5: can HIGHER-DERIVATIVE operators rescue an m(|a|) kernel? ---")

# (i) kinematics: the u-contraction of acceleration is exactly (gamma v)-suppressed
tau = sp.Symbol('tau', real=True)
chif = sp.Function('chi_f')(tau)
xdot = sp.Matrix([sp.cosh(chif), sp.sinh(chif)])
xdd = sp.diff(xdot, tau)
u_dot_xdd = xdd[0]                                  # u_mu xdd^mu with u_lo = (1,0)
acc2 = sp.simplify(-xdd[0] ** 2 + xdd[1] ** 2)      # xdd.xdd (proper acceleration^2)
check("xdd.xdd == chidot^2 exactly (proper acceleration invariant, 1+1D)",
      sp.simplify(acc2 - sp.diff(chif, tau) ** 2) == 0)
check("(u.xdd)^2 == sinh^2(chi) * (xdd.xdd) EXACTLY, i.e. u.xdd = (gamma v) x "
      "|proper accel|: the u-route to |a| is (v/c)-suppressed -- the corpus "
      "Frenet-torsion fact |a|/B = v/c rederived from the EFT side",
      sp.simplify(u_dot_xdd ** 2 - sp.sinh(chif) ** 2 * acc2) == 0 and
      sp.simplify(sp.cosh(chi) * sp.tanh(chi) - sp.sinh(chi)) == 0)
a_lab = sp.diff(sp.tanh(chif), tau) / sp.cosh(chif)     # dv/dt = (dv/dtau)/(dt/dtau)
check("proper acceleration chidot == gamma^3 a_lab (1D kinematic cross-check)",
      sp.simplify(sp.diff(chif, tau) - sp.cosh(chif) ** 3 * a_lab) == 0)

# (ii) operators LINEAR in xdd are total derivatives in the homogeneous background
Ff = sp.Function('F_f')
lhs = sp.diff(Ff(sp.cosh(chif)), tau)
rhs = sp.diff(Ff(w), w).subs(w, sp.cosh(chif)) * u_dot_xdd
check("f(u.xdot)(u.xdd) == d/dtau F(u.xdot) in the background (d_mu u_nu = 0): "
      "linear-in-xdd operators are TOTAL DERIVATIVES -- zero EOM contribution",
      sp.simplify(lhs - rhs) == 0)

# (iii) operators QUADRATIC in xdd: Ostrogradsky
Q2s, P1s, P2s, eps = sp.symbols('Q2 P1 P2 epsilon', real=True)
Aacc = -P2s / eps                                   # from P2 = dL/dqdd = -eps qdd
Losc = Q2s ** 2 / 2 - eps * Aacc ** 2 / 2
Host = P1s * Q2s + P2s * Aacc - Losc
check("Ostrogradsky: H for L = qdot^2/2 - eps qddot^2/2 is LINEAR in P1 "
      "(d2H/dP1^2 == 0, dH/dP1 == Q2 != 0) -> unbounded below, GHOST",
      sp.diff(Host, P1s, 2) == 0 and sp.simplify(sp.diff(Host, P1s) - Q2s) == 0)

# (iv) perturbative redundancy: eps*xdd^2 reduces to POSITION-dependent inertia
tr_ = sp.Symbol('t_r', real=True)
qr = sp.Function('q_r')(tr_)
Vg = sp.Function('V')
mr, er = sp.symbols('m_r eps_r', positive=True)


def Vp(k, arg):
    return sp.diff(Vg(w), w, k).subs(w, arg)


Lred = mr * sp.diff(qr, tr_) ** 2 / 2 - Vg(qr) + er * sp.diff(qr, tr_, 2) ** 2 / 2
ELred = (sp.diff(Lred, qr) - sp.diff(sp.diff(Lred, sp.diff(qr, tr_)), tr_)
         + sp.diff(sp.diff(Lred, sp.diff(qr, tr_, 2)), tr_, 2))
q4_red = -(Vp(3, qr) * sp.diff(qr, tr_) ** 2 + Vp(2, qr) * sp.diff(qr, tr_, 2)) / mr
check("chain-rule step: d^2/dt^2 of the leading EOM qdd = -V'/m gives "
      "q4 = -(V''' qd^2 + V'' qdd)/m",
      sp.simplify(sp.diff(-Vp(1, qr) / mr, tr_, 2).doit() - q4_red) == 0)
ELsub = ELred.subs(sp.Derivative(qr, (tr_, 4)), q4_red)
As, Vds, Qs = sp.symbols('A_s vd_s q_s', real=True)
ELsym = ELsub.subs([(sp.Derivative(qr, (tr_, 2)), As),
                    (sp.Derivative(qr, tr_), Vds), (qr, Qs)])
coefA = sp.simplify(sp.diff(ELsym, As))
meff_red = -coefA                                   # EL normalised: eps->0 coeff is -m
ok_red = (not coefA.has(As) and
          sp.simplify(meff_red - (mr + er * Vp(2, Qs) / mr)) == 0 and
          sp.simplify(sp.diff(meff_red, er, 2)) == 0)
check("on-shell reduction of eps qdd^2: m_eff = m + eps V''(q)/m -- POSITION-"
      "dependent and ANALYTIC in eps; the non-analytic MOND floor m ~ |a|/a_0 "
      "cannot arise from any finite perturbative order", ok_red)

# ---------------------------------------------------------------------------
# SECTION 6 -- point 3: THE WARD QUESTION
# ---------------------------------------------------------------------------
print("\n--- Section 6: the Ward identity of broken boosts -- what it fixes and what it cannot ---")

# (a) probe-Goldstone vertex from expanding u[phi = t + pi] to O(pi)
al = sp.Symbol('alpha_l', real=True)
pt_, px_ = sp.symbols('pi_t pi_x', real=True)       # pidot, grad pi at the probe
dphi_p = sp.Matrix([1 + al * pt_, al * px_])
Xp = -(1 + al * pt_) ** 2 + (al * px_) ** 2
u_p = dphi_p / sp.sqrt(-Xp)
xdv = sp.Matrix([gam, gam * v])
Uex = (u_p.T * xdv)[0, 0]                           # u_mu xdot^mu with pi on
U_lin = sp.simplify(sp.diff(Uex, al).subs(al, 0))
check("O(pi) expansion: delta(u.xdot) = gamma * v * (grad pi) -- pidot DROPS at "
      "linear order; the Goldstone couples to the probe only through v (at v=0 "
      "the probe decouples at O(pi): the same v/c suppression again)",
      sp.simplify(U_lin - gam * v * px_) == 0)

integrand = (c1 * Uex + c2 * Uex ** 2) / gam        # dt-Lagrangian with pi on
C_lin = sp.simplify(sp.diff(integrand, al).subs(al, 0))
C_coef = sp.simplify(C_lin / px_)                   # coefficient of (grad pi)

# (b) boost-charge deficit of the probe sector alone: dK/dt = p - v E
Rdef = sp.simplify(p_of_v - v * E_of_v)
check("boost-charge deficit dK_probe/dt = p - vE = v (c1 + 2 c2 gamma): the probe "
      "boost charge alone is NOT conserved (boosts genuinely broken) unless c1=c2=0",
      sp.simplify(Rdef - v * (c1 + 2 * c2 * gam)) == 0 and
      sp.simplify(Rdef.subs([(c1, 1), (c2, 0)])) != 0)

# (c) THE WARD IDENTITY: the vertex equals the deficit, for ALL c1, c2
check("WARD IDENTITY VERIFIED: probe-Goldstone vertex coefficient == boost-charge "
      "deficit, IDENTICALLY in (c1, c2) -- the symmetry fixes the RELATION "
      "(vertex <-> dispersion), it fixes NO Wilson coefficient VALUE",
      sp.simplify(C_coef - Rdef) == 0)

# (d) the algebra [K^i, P^j] = i delta^ij H is KINEMATIC: holds for ANY dispersion
xs, ps, ts = sp.symbols('x_s p_s t_s', real=True)
Hgen = sp.Function('H_gen')


def poisson(Aex, Bex):
    return sp.diff(Aex, xs) * sp.diff(Bex, ps) - sp.diff(Aex, ps) * sp.diff(Bex, xs)


Kgen = ts * ps - xs * Hgen(ps)
check("{K, P} = -H for an ARBITRARY dispersion H(p): the commutator "
      "[K^i,P^j] = i delta^ij H is satisfied by construction of K and therefore "
      "CANNOT single out any H(p) -- the algebra fixes nothing",
      sp.simplify(poisson(Kgen, ps) + Hgen(ps)) == 0)

# ---------------------------------------------------------------------------
# VERDICT
# ---------------------------------------------------------------------------
print("\n" + "=" * 78)
print("VERDICT (honest outcomes per the lane brief)")
print("=" * 78)
print("""
 (a) does the symmetry FORCE the exact a_0-line with floor c|phidot|?   NO.
 (b) does the symmetry allow a FAMILY?                                  YES:
     free at this order: m, c1, c2 (velocity sector; m_eff = m + c2) plus
     3 independent one-du structures {u^m x^n d_m u_n, x^m x^n d_m u_n, d.u},
     each with a free function of (u.xdot); all vanish in the homogeneous
     background. The Ward identity fixes the probe-Goldstone VERTEX equal to
     the boost-charge deficit v(c1 + 2 c2 gamma) -- for EVERY (c1, c2) --
     i.e. relations, never values. Forced coefficients: ZERO.
 (c) can acceleration-dependent inertia arise at this order?            NO:
     - L(q, qdot) class: EOM affine in a, kernel = d2L/dv2 (theorem);
     - linear-in-xdd operators: total tau-derivatives in the background;
     - quadratic-in-xdd: Ostrogradsky-unbounded; perturbatively reduce to
       m_eff = m + eps V''(q)/m -- position-dependent, analytic, no m(|a|);
     - u.xdd = (gamma v) |a_proper| EXACTLY: the u-route is (v/c)-suppressed,
       independently reproducing the corpus Frenet-torsion no-go.

 THE a_0-LINE IS NOT THE WARD IDENTITY OF BROKEN BOOSTS. The kernel shape stays
 a POSTULATE; the 30.6% shape systematic does NOT collapse; kappa = 1/2 stays
 FITTED. No a_0 emerges -- canonical 9.3614e-11 and ALT 1.13e-10 are equally
 unreachable from symmetry alone (the no-go is footing-independent).

 AGAINST THE NO-GO (do not overstate it): this closes the PROBE-WORLDLINE route
 at the stated order in the HOMOGENEOUS background. Near a source the condensate
 is NOT homogeneous (d_mu u_nu != 0 there), and MOND-like behaviour in condensate
 models lives in the FIELD sector (P(X) nonlinearity), which this lane never
 touched. Higher orders in (u.xdot), operators with more derivatives of u, and
 non-perturbative higher-derivative dynamics are NOT excluded. A door, not a wall.
""")

n_ok = sum(RESULTS)
n_all = len(RESULTS)
print(f"{n_ok}/{n_all} checks held.")
if n_ok != n_all:
    sys.exit(1)
sys.exit(0)
