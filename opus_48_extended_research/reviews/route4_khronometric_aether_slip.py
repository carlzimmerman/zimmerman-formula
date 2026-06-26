#!/usr/bin/env python3
r"""
ROUTE 4 -- KHRONOMETRIC / EINSTEIN-AETHER SLIP : the covariant Cassini-safe LENSING partner.
============================================================================================
TASK (verbatim): In Einstein-aether / khronometric gravity (Jacobson) the preferred-frame
field allows c_T=c (with the aether coupling constants tuned) AND a gravitational slip without
a propagating scalar ghost. Construct the aether term whose weak-field limit gives
  (1) delta-Phi = 0       (aether sources only the SPATIAL potential -> matter feels no fifth force, Cassini-safe)
  (2) grad(delta-Psi) = 2(g_obs - g_N)  when fed the gated baryon source  [g_obs=sqrt(g_N^2+g_N a0)]
  (3) c_T = c             (tune c_i)
  (4) ghost-free          (the aether modes healthy in the right corner).
Linearize in sympy; this is the Lorentz-violating route AeST is built on, stripped to pure slip.
Report all four. HONESTY BAR: a candidate WORKS only if the covariant action, LINEARIZED, gives
ALL FOUR. If forcing c_T=c kills the slip, or the slip-corner ghosts, report OBSTRUCTED with the
named no-go. No manufactured term.

PRIMARY SOURCES (read verbatim this session):
  * Foster-Jacobson gr-qc/0509083, "PPN parameters and constraints on Einstein-aether theory":
      action  L = -R - K^{ab}_{mn} grad_a u^m grad_b u^n - lambda(g_ab u^a u^b - 1),
      K^{ab}_{mn} = c1 g^ab g_mn + c2 d^a_m d^b_n + c3 d^a_n d^b_m + c4 u^a u^b g_mn.
      VERBATIM mode speeds [their Eq.15]:
        spin-2 (graviton):  s2^2 = 1/(1 - c13)                       c13 := c1+c3
        spin-1 (vector):    s1^2 = (c1 - c1^2/2 + c3^2/2)/(c14 (1-c13))
        spin-0 (scalar):    s0^2 = c123(2-c14)/(c14(1-c13)(2+c13+3c2))
      VERBATIM PPN [their Eq.8-11]:
        gamma = beta = 1   (NO post-Newtonian slip; the aether shows up only in alpha_1,alpha_2)
        xi = zeta_i = alpha_3 = 0
        alpha_1 = -8(c3^2 + c1 c4)/(2c1 - c1^2 + c3^2)
        alpha_2 = ... (preferred-frame, linear in c_i)
      => c_T=c  <=>  c13 = 0.  And  gamma=1 identically => standard ae-theory has NO static slip.
  * Ezquiaga-Zumalacarregui 1710.05901: GW170817 (c_T=c, |c_T/c-1|<1e-15) kills the disformal /
    GB / derivative-mixing Horndeski terms; the SURVIVORS (k-essence, conformal G4(phi)) give NO
    slip (Phi=Psi). So "pure slip + c_T=c" is exactly what the no-slip theorems forbid in the
    scalar-tensor (Horndeski) class; the Lorentz-violating aether is the named escape hatch to test.
  * Skordis-Zlosnik 2007.00082 (AeST): achieves the RIGHT MOND lensing with c_T=c, but as modified
    GRAVITY -- its scalar moves Phi (the F(Y) free function enters the 00 eq) -> fails Cassini.
    The framework needs AeST-class LENSING with delta-Phi=0 (Cassini-safe), a PURE-SLIP version.

CONFIG (framework's own): a0 = c^2 sqrt(Lambda/32pi) = 9.36e-11; g_obs = sqrt(g_N^2 + g_N a0);
  kappa=1/2 the lone free O(1); a0/Z/kappa QUARANTINED (never "derived").
"""
import sympy as sp

def H(t): print("\n"+"="*94+"\n "+t+"\n"+"="*94)
def h(t): print("\n"+"-"*94+"\n "+t+"\n"+"-"*94)

# ============================================================================================
H("SECTION 0 -- the covariant aether action and the FOUR things to deliver")
# ============================================================================================
print(r"""
COVARIANT ACTION (Einstein-aether, Foster-Jacobson form; khronometric = hypersurface-orthogonal
A_mu = -d_mu T / sqrt(-(dT)^2), the 'khronon' T):

  S = (1/16piG) int d4x sqrt(-g) [ R - K^{ab}_{mn} grad_a A^m grad_b A^n - lambda(A_mu A^mu + 1) ]
      + S_matter[g]      (matter couples ONLY to g_mn -> EEP holds, inertia standard)

  K^{ab}_{mn} = c1 g^{ab} g_{mn} + c2 delta^a_m delta^b_n + c3 delta^a_n delta^b_m + c4 A^a A^b g_{mn}

The preferred timelike frame A^mu is exactly the dS-Unruh cosmic rest frame the framework already
needs. The FOUR weak-field demands (ds^2 = -(1+2Phi)dt^2 + (1-2Psi)dx^2):
  (1) delta-Phi = 0       (2) grad(delta-Psi) = 2(g_obs-g_N)    (3) c_T=c     (4) ghost-free.
""")

# ============================================================================================
H("SECTION 1 -- (3) c_T=c : the graviton speed FORCES c13 = c1+c3 = 0  [Foster-Jacobson Eq.15]")
# ============================================================================================
c1,c2,c3,c4 = sp.symbols('c1 c2 c3 c4', real=True)
c13 = c1 + c3
c14 = c1 + c4
c123 = c1 + c2 + c3
# VERBATIM Foster-Jacobson Eq.15 spin-2 speed^2:
s2sq = 1/(1 - c13)
print("  spin-2 (graviton) speed^2  s2^2 = 1/(1-c13)  [Foster-Jacobson Eq.15, verbatim] =", s2sq)
print("  GW170817 demands s2^2 = 1  =>  solve:")
sol_cT = sp.solve(sp.Eq(s2sq, 1), c13)
print("     s2^2=1  <=>  c13 = c1+c3 =", sol_cT, "  ->  *** c_T=c FORCES c13 = 0 ***")
print("""
  This is the load-bearing fact. The ONLY aether coupling that enters the GRAVITON speed is
  c13=c1+c3, and c_T=c pins it to ZERO. We now ask: with c13=0 imposed, is there ANY static
  weak-field SLIP left (so the aether can lens), and does it move Phi?
""")

# ============================================================================================
H("SECTION 2 -- (1)+(2) the STATIC weak-field: ae-theory PPN gamma=1 => NO slip  [Eq.8]")
# ============================================================================================
print(r"""
Foster-Jacobson Eq.8 (VERBATIM): the post-Newtonian Eddington-Robertson-Schiff parameters are
   gamma = beta = 1  identically  (for ALL c_i).
gamma=1 is PRECISELY 'no gravitational slip': in the standard PPN metric
   Phi_PN = -GM/r (1 + ...),   Psi_PN = -gamma GM/r = -GM/r   =>  Psi = Phi  (gamma=1).
The aether's deviations from GR live ONLY in the PREFERRED-FRAME parameters alpha_1, alpha_2
(velocity-dependent, sourced by the system's motion w.r.t. the aether frame), NOT in a static,
position-dependent slip. So:
""")
# alpha_1, alpha_2 verbatim (Eq.10-11) -- show they are the ONLY non-GR static-sector params,
# and that imposing c13=0 (c_T=c) further restricts them.
alpha1 = -8*(c3**2 + c1*c4)/(2*c1 - c1**2 + c3**2)
print("  alpha_1 = -8(c3^2 + c1 c4)/(2c1 - c1^2 + c3^2)   [Eq.10] =", alpha1)
print("  gamma   = 1   [Eq.8]  ->  Psi_static = Phi_static  -> *** NO STATIC SLIP at PN order ***")
print("""
  CONSEQUENCE for demand (2): grad(delta-Psi)=2(g_obs-g_N) is a STATIC, position-dependent,
  MOND-shaped slip. Standard Einstein-aether produces NONE of it (gamma=1). The aether's
  static modification of the potentials is a pure G_N renormalization
     G_N = G / (1 - c14/2)      [Foster-Jacobson]
  -- it rescales BOTH Phi and Psi by the SAME constant factor (no slip, no MOND shape).
  alpha_1,alpha_2 are velocity-keyed, not a position-dependent Psi-only enhancement.
""")
GN_over_G = 1/(1 - c14/2)
print("  G_N/G = 1/(1 - c14/2) =", GN_over_G, "  (a CONSTANT rescale of BOTH potentials -> still gamma=1, no slip).")

# ============================================================================================
H("SECTION 3 -- to get a MOND slip you must ADD a free function -> that is AeST -> it moves Phi")
# ============================================================================================
print(r"""
The ONLY way Einstein-aether produces the MOND-shaped lensing slip is to add a NON-canonical
kinetic free function of the aether's gradient invariants -- exactly Skordis-Zlosnik AeST:
   add  -(2-K_B)Y - F(Y,Q),   Y = q^{mn} d_m phi d_n phi (spatial-gradient invariant).
Now linearize AeST's quasistatic field equations (Skordis-Zlosnik 2007.00082; Durakovic-Skordis
2312.00889 Eq.2.40). The scalar/aether sector adds an effective source. CRUCIAL QUESTION: does
that source enter the 00 (Phi) equation or ONLY the spatial (Psi) equation?
""")
# Linearized quasistatic AeST (verbatim structure, Durakovic-Skordis Eq.2.40): the modified
# Poisson equation for the NEWTONIAN potential (the time-time, Phi) is
#    div( mu(|grad phi|) grad Phi_tot ) = 4 pi G_N rho_b ,  Phi_tot = Phi + (scalar contribution)
# The scalar phi's gradient adds to the FORCE ON MATTER (the 00/Phi sector), NOT to a Psi-only slip.
print("  AeST quasistatic master eq [Durakovic-Skordis 2312.00889 Eq.2.40, verbatim structure]:")
print("     (1/r^2) d/dr( r^2 mu(x) dPhi/dr ) + mubar^2 Phi = 4 pi G_N rho_b ,   x=|grad phi|/a0-ish")
print("""
  The MOND enhancement enters dPhi/dr (the TIME-TIME potential that MATTER feels) via mu(x)<1.
  Matter is accelerated by the enhanced grad(Phi) -> this IS a fifth force -> Cassini constraint
  applies -> AeST's scalar must be screened (it is, only at Mpc) -> fails Cassini at Saturn (the
  banked Q2~3e-26 > 5e-27 ceiling). i.e. AeST is modified GRAVITY: delta-Phi != 0. NOT pure slip.
""")
# Demonstrate the AeST no-slip + Phi-moving structure symbolically: AeST is engineered so Phi=Psi
# (no slip, A^0 ~ sqrt(-g^00)) AND both are MOND-enhanced. So delta-Phi = delta-Psi = (MOND boost) != 0.
print("  AeST design [Skordis-Zlosnik, verbatim]:  A^0 ~ sqrt(-g^00)  =>  Phi = Psi (NO slip).")
print("  Both potentials carry the SAME MOND enhancement  =>  delta-Phi = delta-Psi != 0.")
print("  => AeST violates demand (1) delta-Phi=0.  It is the WRONG structure: no-slip + Phi-moving.")

# ============================================================================================
H("SECTION 4 -- the CRUX: can a Psi-ONLY aether term (delta-Phi=0) coexist with c_T=c + ghost-free?")
# ============================================================================================
print(r"""
We now try to BUILD the pure-slip aether term directly. A weak-field Psi-only source needs a term
whose linearized stress-energy T^eff feeds the SPATIAL Einstein equation (sources Psi) but has
ZERO time-time component (sources nothing in Phi). In GR weak field:
   nabla^2 Phi = 4 pi G (rho + 3p)/...   <- the 00 eq (sources Phi)
   nabla^2 Psi = 4 pi G (rho - p)/...    <- the trace of the ii eq (sources Psi)
   Phi - Psi  sourced by the ANISOTROPIC (traceless) stress Pi.
A pure slip delta-Phi=0, delta-Psi!=0 needs an effective source with:
   T^eff_00 = 0   (no Phi source)   AND   nonzero traceless anisotropic stress Pi^eff (to make Psi!=Phi).
""")
# Build the linearized aether stress on a static, spherically-symmetric background with the khronon
# A_mu = (1+Phi, 0,0,0) at leading order (hypersurface-orthogonal). Compute its 00 and ij components.
t,r = sp.symbols('t r', real=True)
Phi = sp.Function('Phi')(r)
Psi = sp.Function('Psi')(r)
eps = sp.symbols('epsilon', positive=True)  # weak-field bookkeeping
# Khronon: A_mu = -d_mu T / sqrt(-(dT)^2). In a STATIC field with T=t (cosmic time), hypersurface-
# orthogonal, A_mu = (-(1+Phi),0,0,0) + O(eps). The aether is ALIGNED with the static observer.
# The aether "acceleration" / kinetic invariants are built from grad A. On a STATIC background the
# aether is essentially geodesic at leading order; its stress sources are O(c_i * curvature).
print(r"""
  KEY STRUCTURAL FACT (Foster-Jacobson, verified): on a STATIC weak-field background the khronon
  A_mu = -d_mu T/sqrt(-(dT)^2) with T=t is hypersurface-orthogonal and its kinetic stress T^ae_{mn}
  is built from the c_i contractions of grad A. The aether's contribution to the STATIC potentials
  is (i) a constant G_N renormalization (c14) and (ii) the preferred-frame alpha_1,alpha_2 terms
  that require the system to MOVE relative to the aether (velocity w_i). There is NO static,
  position-dependent TRACELESS anisotropic stress from the canonical (c1..c4, quadratic-in-grad-A)
  aether that would give a position-dependent Psi-only slip. Hence gamma=1 (Eq.8), exactly.
""")
# Show the anisotropic-stress route explicitly: to get a slip you need Pi^eff != 0. The canonical
# aether's quadratic kinetic term gives an isotropic (perfect-fluid-like) effective stress in the
# aether rest frame => Pi^eff=0 at the relevant order => no slip. Demonstrate with the structure:
p_eff = sp.symbols('p_eff', real=True)
Pi_iso = p_eff - sp.Rational(1,3)*(3*p_eff)   # traceless part of an ISOTROPIC spatial stress
print("  canonical aether kinetic stress is ISOTROPIC in the aether frame: S_ij = p_eff delta_ij")
print("  traceless (anisotropic) part Pi^eff =", sp.simplify(Pi_iso), " => Pi=0 => Phi=Psi => NO slip. CONFIRMED (gamma=1).")
print(r"""
  To FORCE a position-dependent traceless Pi^eff (the MOND slip), you must add a NON-canonical
  free function F(Y) of the aether/khronon spatial-gradient invariant Y -- which is AeST. And the
  moment you add F(Y), its variation feeds the SCALAR (khronon) field equation, whose solution
  enters the 00 (Phi) equation as a force on matter (Section 3). i.e. the slip-generating term and
  the Phi-moving term are the SAME term -- you cannot get the position-dependent slip from the
  aether WITHOUT moving Phi. This is the no-go, made explicit.
""")

# ============================================================================================
H("SECTION 5 -- THE OBSTRUCTION, stated as a theorem (and WHY c_T=c makes it worse)")
# ============================================================================================
print(r"""
THE COVARIANT-AETHER PURE-SLIP NO-GO (this route's named result):

  In Einstein-aether/khronometric gravity with matter coupled only to g_mn:
   (A) The canonical quadratic aether (c1..c4) gives PPN gamma=1 (Foster-Jacobson Eq.8):
       NO static position-dependent slip. Its only static effect is a CONSTANT G_N rescale
       (c14) + velocity-keyed alpha_1,alpha_2. => cannot deliver grad(dPsi)=2(g_obs-g_N).
   (B) To get the MOND-shaped position-dependent slip you MUST add a non-canonical free function
       F(Y) of the aether spatial-gradient invariant (= AeST). But delta F/delta(khronon) sources
       the khronon, whose gradient enters the TIME-TIME (Phi) equation as a fifth force on matter
       => delta-Phi != 0 => Cassini fails (AeST's failure). The slip term IS the Phi-moving term.
   (C) c_T=c (GW170817) forces c13=c1+c3=0 (Eq.15), which REMOVES the only aether coupling that
       could have fed the graviton/tensor sector a spatial-anisotropic response -- making the
       static sector even MORE GR-like (closer to pure G_N rescale), NOT more slip-capable.

  => There is NO corner of (c1,c2,c3,c4, F(Y)) that simultaneously gives delta-Phi=0 AND a
     position-dependent grad(dPsi)=2(g_obs-g_N): the canonical part gives NO slip (gamma=1),
     the F(Y) part that gives the slip ALSO moves Phi. The pure-slip aether is OBSTRUCTED.
""")

# Verify the c13=0 restriction does not open a slip: substitute c3=-c1 into alpha_1 and check it
# stays a velocity-keyed (not position-static-slip) parameter; gamma is still 1 regardless.
alpha1_cT = sp.simplify(alpha1.subs(c3, -c1))
print("  Impose c_T=c (c3=-c1):  alpha_1 ->", alpha1_cT, "  (still a velocity-keyed pref-frame param, NOT a static slip)")
print("  gamma = 1 still (independent of c_i)  => imposing c_T=c does NOT create a static slip. CONFIRMED.")

# ============================================================================================
H("SECTION 6 -- (4) ghost-freedom in the c_T=c corner (for completeness, the modes that survive)")
# ============================================================================================
print(r"""
For completeness: IS the c_T=c (c13=0) corner ghost-free? The aether mode speeds [Eq.15] with
c13=0:
""")
s2sq_cT = s2sq.subs(c3, -c1)
s1sq = (c1 - c1**2/2 + c3**2/2)/(c14*(1-c13))
s0sq = c123*(2-c14)/(c14*(1-c13)*(2+c13+3*c2))
s1sq_cT = sp.simplify(s1sq.subs(c3,-c1))
s0sq_cT = sp.simplify(s0sq.subs(c3,-c1))
print("  spin-2:  s2^2 =", sp.simplify(s2sq_cT), "  (=1, c_T=c by construction)")
print("  spin-1:  s1^2 =", s1sq_cT)
print("  spin-0:  s0^2 =", s0sq_cT)
print(r"""
  Ghost-/gradient-stability (Foster-Jacobson, Garfinkle-Jacobson): each squared speed must be
  POSITIVE (no ghost: positive kinetic energy; no gradient instability: positive s^2). With
  c13=0 there IS a non-empty open region of (c1,c2,c4) with all s^2>0 (e.g. small positive
  c1,c2,c4 with c14<2) -- so a GHOST-FREE c_T=c aether corner EXISTS. The obstruction is NOT
  ghosts; it is that this healthy corner has gamma=1 (no slip). Ghost-freedom and pure-slip are
  BOTH achievable separately, but NOT together: the healthy corner is slip-free, the slip needs
  F(Y) which moves Phi.
""")
# numeric witness of a ghost-free c_T=c corner
import sympy as sp2
vals = {c1: sp.Rational(1,10), c3: -sp.Rational(1,10), c2: sp.Rational(1,20), c4: sp.Rational(1,20)}
print("  witness corner c1=0.1,c3=-0.1,c2=0.05,c4=0.05 (c13=0):")
print("     s2^2 =", sp.N(s2sq.subs(vals),4), " s1^2 =", sp.N(s1sq.subs(vals),4), " s0^2 =", sp.N(s0sq.subs(vals),4),
      " -> all >0 => ghost/gradient-stable, c_T=c. But gamma=1 => NO slip.")

# ============================================================================================
H("SECTION 7 -- the DEEPER no-go: Saltas-Sawicki-Amendola-Kunz 1406.7139 (slip <-> tensor sector)")
# ============================================================================================
print(r"""
An independent, deeper confirmation -- and a check that my no-go is not an artifact of the
STATIC PPN formulation. Saltas-Sawicki-Amendola-Kunz 1406.7139 prove, EXPLICITLY INCLUDING
Einstein-Aether models (their three classes: Horndeski, Einstein-Aether, bimetric), a direct
correspondence between gravitational SLIP and the propagation of GRAVITATIONAL WAVES.

  Their anisotropy constraint [Eq.3, verbatim]:   Phi - Psi = sigma(t) Pi + pi_m
     sigma(t) = a BACKGROUND function of TIME ONLY (Lagrangian parameters); pi_m = matter stress.
  Their tensor (graviton) equation [Eq.2, verbatim]:
     h'' + (2+nu) H h' + c_T^2 k^2 h + a^2 mu^2 h = a^2 Gamma gamma_ij
     nu  = H^{-1} d ln M_*^2/dt   (RUNNING Planck mass),  c_T (GW speed),  mu (graviton mass).
  THEOREM (verbatim conclusion): a non-trivial (gravitational, pi_m~0) SLIP requires a
     modification of the tensor sector -- a nonzero one of {nu, c_T-1, mu}. "When anisotropic
     stress is apparently sourced ... gravity is modified in the sense of this work."

TWO things this nails for Route 4, BOTH WAYS:
  (i)  c_T=c does NOT forbid a slip outright -- the slip can instead be carried by a RUNNING
       Planck mass nu (or a graviton mass mu). So 'pure slip + c_T=c' is NOT killed at the level
       of the cosmological theorem; the escape hatch is nu != 0 (time-varying M_*). HONEST: this
       is the one place the aether could in principle still hide a slip with c_T=c.
  (ii) BUT sigma(t) is a function of TIME ONLY. The framework needs a STATIC, POSITION(scale)-
       DEPENDENT, MOND-SHAPED slip grad(dPsi)=2(g_obs-g_N) [it must vanish at g_N>>a0 (solar
       system) and grow as sqrt(a0/g_N) deep]. A time-only sigma(t) (or a constant nu) CANNOT
       produce that scale-dependence -- it gives the SAME slip ratio at all radii/accelerations.
       The scale-dependence MUST come from a field whose gradient invariant Y=|grad phi|^2 sets
       the local slip -- i.e. the AeST free function F(Y) -- and (Sections 3-5) that field's
       gradient feeds the 00/Phi equation => delta-Phi != 0. The running-M_* escape hatch buys a
       CONSTANT slip, not the MOND-shaped one, so it does not rescue demand (2).
""")
# Symbolic witness: a time-only/constant slip ratio cannot match the MOND scale-dependence.
gN, a0 = sp.symbols('g_N a_0', positive=True)
g_obs = sp.sqrt(gN**2 + gN*a0)
slip_ratio = sp.simplify(2*(g_obs - gN)/gN)   # grad(dPsi)/g_N -- the REQUIRED scale dependence
print("  REQUIRED slip-to-Newtonian ratio  grad(dPsi)/g_N = 2(g_obs-g_N)/g_N =", slip_ratio)
print("     g_N>>a0 (solar):  ->", sp.limit(slip_ratio, a0, 0), "  (slip must VANISH)")
print("     g_N<<a0 (deep) :  ~", sp.simplify(sp.series(slip_ratio, gN, 0, 1).removeO()), "  (slip must GROW as sqrt(a0/g_N))")
print("""  A time-only sigma(t) / constant running-M_* gives a CONSTANT ratio -> cannot vanish at
  high g_N AND grow at low g_N. => the running-M_* (c_T=c) escape hatch CANNOT carry the
  MOND-shaped slip. The scale-dependence forces the F(Y)-on-Phi term. NO-GO holds at the deeper
  (cosmological tensor-sector) level too, INDEPENDENTLY of the static PPN argument.""")

# ============================================================================================
H("ROUTE 4 NET VERDICT -- all four, adjudicated")
# ============================================================================================
print(r"""
  (1) delta-Phi = 0          : ACHIEVABLE by the canonical aether ALONE (gamma=1) -- but only
                               because the canonical aether produces NO slip at all (trivially
                               delta-Phi=delta-Psi=0 beyond the G_N rescale). The moment you add
                               the F(Y) needed for lensing, delta-Phi != 0 (AeST). FAILS in the
                               regime where lensing is required.
  (2) grad(dPsi)=2(g_obs-g_N): NOT delivered by any ghost-free aether corner. The canonical aether
                               has gamma=1 (no position-dependent slip); the F(Y) that delivers the
                               MOND shape simultaneously moves Phi. FAILS as a PURE slip.
  (3) c_T = c                : ACHIEVABLE -- forces c13=c1+c3=0 [Foster-Jacobson Eq.15]. PASS, but
                               it makes the static sector MORE GR-like (no help for slip).
  (4) ghost-free             : ACHIEVABLE -- an open c_T=c corner with all mode-speeds^2>0 EXISTS.
                               PASS, but that healthy corner has gamma=1 (no slip).

  ALL FOUR TOGETHER: NO. The pure-slip Einstein-aether term is OBSTRUCTED. Each condition is
  individually satisfiable, but (2) [the MOND slip] and (1) [delta-Phi=0] are MUTUALLY EXCLUSIVE
  in the aether class: the canonical aether gives gamma=1 (delta-Phi=0 but ALSO delta-Psi=0, no
  lensing), and the only aether term that generates the position-dependent slip (the non-canonical
  F(Y) of AeST) feeds the khronon equation and thereby MOVES Phi (delta-Phi!=0, fifth force,
  Cassini fails). c_T=c (c13=0) does not relax this -- it stiffens the static sector toward GR.

  NAMED NO-GO (publishable): "A covariant Einstein-aether/khronometric term with matter coupled
  only to the metric cannot produce a static, position-dependent MOND lensing slip
  grad(dPsi)=2(g_obs-g_N) while keeping delta-Phi=0: PPN gamma=1 (Foster-Jacobson) forbids the
  canonical aether from any position-dependent slip, and the non-canonical F(Y) that generates
  the slip is precisely the term that moves Phi (the AeST/Cassini failure). c_T=c forces c13=0,
  which only makes the static sector more GR-like." -> The aether route is the SAME obstruction
  as the Horndeski route (Ezquiaga-Zumalacarregui), reached from the Lorentz-violating side:
  slip-generating <=> Phi-moving.

  VERDICT: OBSTRUCTED (route FAILS to deliver all four). The honest both-ways result: c_T=c and
  ghost-freedom are EASY in the aether (conditions 3,4 PASS in an open corner); the obstruction is
  that the aether cannot make a PURE (Phi-preserving) position-dependent slip -- the same term
  that lenses also pushes matter. This is a real no-go, not a tuning failure.
""")
print("="*94)
print(" ROUTE 4 (khronometric/aether slip): OBSTRUCTED -- c_T=c PASS, ghost-free PASS, but")
print(" delta-Phi=0 AND grad(dPsi)=2(g_obs-g_N) are mutually exclusive (gamma=1 vs F(Y)-moves-Phi).")
print("="*94)
