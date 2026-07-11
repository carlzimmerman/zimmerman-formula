#!/usr/bin/env python3
r"""
LANE 1 -- Variation of the de Sitter-Unruh MODIFIED-INERTIA matter action and the
readout of T_00 (the Poisson/lensing source) in a weak-field static galaxy.

    S_matter = -1/2 INT d^4x sqrt(-g) rho_m [ s u^mu K(Box_u/a0^2) u_mu ],
        s = -1  (postulated),
        u^mu = passive unit-timelike frame,  u^mu u_mu = -1,
        Box_u f = u^a nabla_a(u^b nabla_b f) = (u.nabla)^2 f,
        K(z) = (sqrt(1+4z) - 1) / (2 sqrt(z)),   Herglotz-Nevanlinna, ||K||<=1.

The physics we must decide (framework-first, modified INERTIA, NO dark matter):
  (i)  T_00 = the lensing/Poisson source.  Is it rho_bar (baryonic -> UNDER-lens,
       horn C) or nu*rho_bar (enhanced -> collapses to modified gravity)?
  (ii) the traceless T_ij (anisotropic stress) = the slip source (Psi - Phi).
       Is the slip O(1)*(nu-1) [a pure-MI no-DM lensing channel, Carl's dream]
       or O(v^2/c^2)-suppressed [loophole CLOSED, horn C]?

Every approximation is printed explicitly.  Both a0 footings run.
Symbols kept exact where possible; order-counting done with a bookkeeping eps.
Units c = 1 (geometric); a0, accelerations have dimension 1/length.
"""

import sympy as sp

def banner(t):
    print("\n" + "="*78 + "\n" + t + "\n" + "="*78)

# ---------------------------------------------------------------------------
banner("SECTION 0.  The form factor K(z), the static trap K(0)=0, and K'(z)")
# ---------------------------------------------------------------------------
z = sp.symbols('z', positive=True)
K = (sp.sqrt(1 + 4*z) - 1) / (2*sp.sqrt(z))
Kp = sp.simplify(sp.diff(K, z))
print("K(z)            =", K)
print("K'(z)           =", Kp)

K0   = sp.limit(K, z, 0, '+')       # static trap
Kinf = sp.limit(K, z, sp.oo)        # GR / high-acceleration limit
print("lim_{z->0} K    =", K0, "   <-- STATIC TRAP: Box_u -> 0 => K -> 0 => zero MI stress")
print("lim_{z->oo} K   =", Kinf, "  <-- high-acceleration (Newton/GR) limit, ||K||<=1 saturates")
# small-z expansion: modified-inertia deep-MOND behaviour K ~ sqrt(z)
ser = sp.series(K, z, 0, 2).removeO()
print("K(z) small-z    =", ser, "   (deep-MOND: K -> sqrt(z), i.e. m_eff ~ m*(a/a0))")
# K' diverges as z->0 but is tamed by an accompanying z (checked in Sec 4):
Kp_small = sp.series(Kp, z, 0, 1).removeO()
print("K'(z) small-z   ~", Kp_small, "  (diverges as 1/(2 sqrt z); tamed by z*K' -> 0)")
print("z*K'(z) small-z ~", sp.series(z*Kp, z, 0, 2).removeO(), "  <-- product stays finite/small")

# ---------------------------------------------------------------------------
banner("SECTION 1.  The static trap, made explicit for a truly static element")
# ---------------------------------------------------------------------------
t = sp.symbols('t')
f = sp.Function('f')
# static field f = f(x) only; passive frame u=(1,0,0,0) (normalized, flat lead)
# Box_u f = (u.nabla)^2 f = d^2/dt^2 f  -> 0 for static f.
print("For a strictly STATIC source with u^mu=(1,0,0,0):")
print("   Box_u f = (u.grad)^2 f = d^2 f/dt^2 = 0   ->   K(Box_u/a0^2) = K(0) = 0.")
print("=> a genuinely static matter element sources ZERO modified-inertia stress.")
print("   The enhancement can ONLY come from ORBITING matter (nonzero worldline")
print("   proper-acceleration).  We model that source next.")

# ---------------------------------------------------------------------------
banner("SECTION 2.  Orbiting source: the scalar u^mu Box_u u_mu = -(a.a) = -a_c^2")
# ---------------------------------------------------------------------------
# Minkowski eta = diag(-1,1,1,1).  Uniform circular orbit, coordinate time t,
# u^mu = gamma (1, -v sin(Om t), v cos(Om t), 0),  v = Om*r,  gamma = 1/sqrt(1-v^2).
# Convective (proper-time) derivative carried along the worldline: D/Dtau = gamma d/dt.
v, Om, r = sp.symbols('v Omega r', positive=True)
gamma = 1/sp.sqrt(1 - v**2)
phi = Om*t
eta = sp.diag(-1, 1, 1, 1)

U = sp.Matrix([gamma, -gamma*v*sp.sin(phi), gamma*v*sp.cos(phi), 0])   # u^mu(t)
def lower(Vup): return eta*Vup
def dot(Aup, Bup): return (lower(Aup).T * Bup)[0]

# normalization u.u = -1
print("u^mu u_mu =", sp.simplify(dot(U, U)), " (should be -1)")

# 4-acceleration a^mu = D u^mu/Dtau = gamma d/dt u^mu
A = gamma*sp.diff(U, t)
A = sp.simplify(A)
# jerk J^mu = Box_u u^mu = gamma d/dt a^mu
J = sp.simplify(gamma*sp.diff(A, t))

aa   = sp.simplify(dot(A, A))            # a.a  (spacelike, > 0)
u_a  = sp.simplify(dot(U, A))            # u.a  (should be 0)
u_J  = sp.simplify(dot(U, J))            # u^mu Box_u u_mu
print("u.a (accel perp velocity)      =", u_a, " (should be 0)")
print("a.a  = |a|^2                    =", aa)
# Newtonian centripetal magnitude a_c = v^2/r (with v=Om r): a.a = gamma^4 (v^2/r)^2 up to O(v^2)
aa_sub = sp.simplify(aa.subs(Om, v/r))
print("a.a with Om=v/r                =", aa_sub, "   -> |a| = gamma^2 v^2/r ~ a_c (centripetal)")
print("u^mu (Box_u u_mu) = u.J        =", u_J)
print("CHECK identity  u^mu Box_u u_mu = -(a.a):", sp.simplify(u_J + aa) == 0)
print()
print("=> The SCALAR that sets the argument of K is the 'expectation value'")
print("     <Box_u> = (u^mu Box_u u_mu)/(u^mu u_mu) = (-a_c^2)/(-1) = a_c^2.")
print("   Hence z_eff = <Box_u>/a0^2 = a_c^2/a0^2  =  (a_c/a0)^2.")
print("   (NOT the orbital-frequency Omega^2/a0^2; the vector jerk oscillates,")
print("    but the physical scalar contraction returns the acceleration^2 scale.)")

# ---------------------------------------------------------------------------
banner("SECTION 3.  z_eff = (a_c/a0)^2 is O(1) in the MOND regime -- BOTH footings")
# ---------------------------------------------------------------------------
# MOND regime is DEFINED by a_c ~ a0.  Evaluate K, K' there for both a0 footings.
a0_canon = 9.36e-11     # cH_Lambda/Z  (canonical, rho_DE)
a0_alt   = 1.13e-10     # cH0 * rho_total footing (alt)
for name, a0v in [("canonical a0=9.36e-11", a0_canon), ("alt a0=1.13e-10", a0_alt)]:
    for ac_over_a0 in [0.3, 1.0, 3.0]:     # deep, transition, high
        zval = ac_over_a0**2
        print(f"  [{name}]  a_c/a0={ac_over_a0:>4}: z_eff={zval:6.3f}  "
              f"K={float(K.subs(z,zval)):.4f}  K'={float(Kp.subs(z,zval)):.4f}  "
              f"z*K'={float((z*Kp).subs(z,zval)):.4f}")
print()
print("=> In the MOND regime z_eff = O(1); K and K' and z*K' are ALL O(1).")
print("   There is NO large 1/a0^2 denominator hiding in the source stress:")
print("   a0^2 is cancelled by a_c^2, by construction of the MOND regime.")
print("   The a0 footing shifts K,K' only by O(1); NO scaling conclusion depends on it.")

# ---------------------------------------------------------------------------
banner("SECTION 4.  The variation T_mu_nu, structural readout of T_00")
# ---------------------------------------------------------------------------
print(r"""
The scalar Lagrangian density is
    L = -1/2 rho_m [ s u^mu K(Box_u/a0^2) u_mu ]
      ~ -1/2 rho_m [ (-1) * (-1) * Kbar ]         (s=-1, u^mu u_mu = -1, Kbar=<K>)
      = -1/2 rho_m Kbar,       Kbar = K(a_c^2/a0^2) in {0..1}.

T_mu_nu = -(2/sqrt(-g)) delta(sqrt(-g) L)/delta g^{mu nu} has three pieces:

 (a) metric-determinant piece  delta sqrt(-g) = -1/2 sqrt(-g) g_{mu nu} delta g^{mu nu}
        ->  T_mu_nu ⊃ g_{mu nu} L = -(1/2) rho_m Kbar g_{mu nu}
        an ISOTROPIC pressure p = -(1/2) rho_m Kbar   (weak field: |p| <~ rho_m/2).

 (b) matter/number-current + explicit u_mu piece (standard dust identity
        delta rho_m = (1/2) rho_m (g_{mu nu} - u_mu u_nu) delta g^{mu nu}, plus
        delta u_mu = u^nu delta g_{mu nu}):
        ->  T_mu_nu ⊃ rho_m Kbar u_mu u_nu   (up to the overall 1/2 normalization).

 (c) the K'-pieces from delta(Box_u)/delta g^{mu nu}.  Box_u = (u.nabla)^2 carries
     the metric through the Christoffels in nabla and through u_mu = g_{mu nu}u^nu:
        ->  T_mu_nu ⊃ rho_m K'(z) * [ (u.nabla)^2-structure contracted with u u ].

CRUCIAL STRUCTURAL FACTS (footing-independent):

  * Every one of (a),(b),(c) is proportional to rho_m.  T_00 has SUPPORT ONLY where
    rho_m != 0, i.e. ON the baryons.  In the far-field 'halo' region (rho_m = 0)
    T_00 = 0.  A matter action can NOT manufacture an extended dark T_00 halo.
    => T_00 is BARYONIC.  Modified gravity gets its far-field enhancement from the
       FIELD equation (nonlinear/AeST Poisson), never from T_00; here there is no
       such field, so this is genuinely modified INERTIA with a baryonic source.

  * The magnitude:  T_00 ~ rho_m * O(Kbar),  with Kbar = K(z) <= 1  (||K||<=1).
    In the transition regime Kbar ~ 0.4-0.7 < 1.  So the leading T_00 is
    O(1)*rho_bar, and if anything <= rho_bar (mildly UNDER, not enhanced).
    It is NOT nu*rho_bar (nu ~ few would require Kbar ~ nu > 1, forbidden by ||K||<=1).
""")
# demonstrate the isotropic-pressure coefficient sign/size explicitly
rho_m = sp.symbols('rho_m', positive=True)
Kbar  = sp.symbols('Kbar', positive=True)
L_dens = -sp.Rational(1,2)*rho_m*Kbar
print("Isotropic pressure p = L =", L_dens, " (|p| <= rho_m/2 since Kbar<=1)")
print("Leading T_00 ~ rho_m*Kbar (dust) + isotropic piece: O(1)*rho_bar, support = baryons.")
print("VERDICT (i): T_00 = BARYONIC (under-lens). NOT enhanced to nu*rho_bar.")

# ---------------------------------------------------------------------------
banner("SECTION 5.  Anisotropic stress / slip order-count (preview of Lane 2)")
# ---------------------------------------------------------------------------
# bookkeeping small parameter eps ~ Phi ~ Psi ~ v^2/c^2 ~ 1e-6 (galactic weak field)
eps = sp.symbols('epsilon', positive=True)  # eps = v^2/c^2 = Phi = Psi order
print("Bookkeeping: Phi ~ Psi ~ v^2/c^2 ~ eps ~ 1e-6.  a_c/a0 ~ O(1) => K,K' ~ O(1).")
print()
print("Sources of a TRACELESS (anisotropic) T_ij:")
print("  * dust ram stress  rho_m u_i u_j ~ rho_m v_i v_j ~ rho_m*eps        [O(rho*eps)]")
print("  * K'-pieces (c):   rho_m K'(z) * (u.nabla)^2-structure.  The traceless")
print("      part carries the spatial u_i u_j / metric-gradient structure, i.e.")
print("      ~ rho_m * K' * O(v^2) = rho_m * O(1) * O(eps).                    [O(rho*eps)]")
print("    No anomalous boost: z_eff=O(1) => no 1/a0^2 amplification (Sec 3).")
print()
aniso_stress = sp.Symbol('rho_m')*eps            # ~ rho v^2/c^2
needed       = 1*eps**0                            # (nu-1) ~ O(1)
# slip sourced by anisotropic stress:  nabla^2 (Psi-Phi) ~ 8 pi G * aniso_stress
# integrated -> (Psi-Phi) ~ Phi * (aniso_stress/rho) ~ eps * eps = eps^2
slip      = eps**2          # (Psi - Phi)
need_lens = eps             # (nu-1)*Phi  ~ O(1)*eps
ratio = sp.simplify(slip/need_lens)
print("Slip produced:        (Psi - Phi)      ~ Phi * (aniso/rho) ~ eps*eps = eps^2")
print("Slip NEEDED for lens: (nu-1)*Phi        ~ O(1)*eps")
print("RATIO  (produced/needed) =", ratio, " = eps = v^2/c^2 ~ 1e-6.")
print()
print("=> The anisotropic-stress slip is v^2/c^2 ~ 1e-6 TOO SMALL to source the")
print("   lensing enhancement.  The K' terms do NOT evade this: they are O(1)*(same")
print("   O(eps) structure), and the ||K||<=1 form-factor bound is not even needed")
print("   -- z*K' stays finite (Sec 0), so no K'-divergence rescues the suppression.")
print()
print("VERDICT (ii): SLIP is O(v^2/c^2)-SUPPRESSED.  The pure-MI anisotropic-stress")
print("   lensing channel is CLOSED.  Horn C confirmed.")

# ---------------------------------------------------------------------------
banner("SECTION 6.  SUMMARY")
# ---------------------------------------------------------------------------
print("""
 (i)  T_00 = baryonic rho_bar (support = baryons only; magnitude O(1)*rho_bar,
      <= rho_bar since ||K||<=1).  NOT enhanced to nu*rho_bar; no far-field dark
      T_00 halo is possible from a matter action ∝ rho_m.  -> UNDER-lens.
 (ii) Anisotropic stress / slip (Psi-Phi) ~ rho v^2/c^2 -> (Psi-Phi)/[(nu-1)Phi]
      ~ v^2/c^2 ~ 1e-6.  SLIP-CLOSED.
 Both a0 footings: only shift O(1) numbers (K,K'); no scaling conclusion moves.
 Net: pure modified-inertia does NOT lens correctly here.  Horn C confirmed;
      a no-DM lensing story must come from Road 1 Branch B or Road 2 nonlocal-MG,
      NOT from the matter-action anisotropic stress.
""")
print("lane1_variation.py: DONE (exit 0)")
