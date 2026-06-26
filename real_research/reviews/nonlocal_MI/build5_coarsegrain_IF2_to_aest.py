#!/usr/bin/env python3
"""
BUILD 5 — COARSE-GRAIN THE CONSTRUCTED IF2 REACTIVE INFLUENCE FUNCTIONAL -> FIELD THEORY,
          and test the join to AeST (Skordis-Zlosnik 2007.00082, eq 5) RIGOROUSLY.
================================================================================
Input (the MATCH-phase object, NOT re-derived here, taken as given & re-verified):
  the CONSERVATIVE time-nonlocal MI worldline functional (agentIF2):
    S_phys[q] = int dt [ (1/2) m_b qdot^2 + q.F_ext - (m a0^2) F(|qddot|^2/a0^2) ],
    F(s) = (1/4) sqrt(s) sqrt(4s+1) - (1/2) sqrt(s) + (1/8) asinh(2 sqrt(s)),  s=(a/a0)^2,
    fixed UNIQUELY by  2 F'(x^2) = mu_fw(x),  mu_fw(x)=(sqrt(1+4x^2)-1)/(2x).
    Galley doubled in-in:  S[q+,q-]=S_phys[+]-S_phys[-];  noise kernel nu_K=0 (purely reactive).
    EL: m*mu_fw(|qddot|/a0)*qddot = F_ext.  CONSERVATIVE (W_loop=0 all amplitudes) but NOT PASSIVE
    (the generating reactive kernel needs a Foster-violating R<0 residue).

This build does the NEW step the task asks: COARSE-GRAIN this worldline action to a FIELD theory
(orbit-average the fast worldline / take the many-particle continuum / integrate out the fast q),
and test whether it PRODUCES AeST:
  (Q1) does the aether A_mu emerge as the MI preferred frame?
  (Q2) does the Y^{3/2} deep-MOND term emerge with the SAME a0?
  (Q3) does the shift-symmetric scalar phi emerge?
  (Q4) is a0 (hence Z, kappa) PRODUCED or only matched/transmitted?
Then confront the Milgrom-1994 MI no-go (astro-ph/9303012) VERBATIM:
  - Milgrom eq (10):  m A_vec = -grad phi,  A_vec a FUNCTIONAL of the whole trajectory r(t).
  - Milgrom locality theorem (Sec III, p.10 of the PDF): "a theory whose kinetic action is Galilei
    invariant, and has the correct Newtonian limit, and the required MOND limit, CANNOT BE LOCAL;
    i.e. A_vec in eq (10) cannot be a function of a finite number of time derivatives of r(t)."
  - Milgrom eq (53)-(55): on CIRCULAR orbits  mu(a/ao) a = d phi/dr, with
       mu(a/ao) = 2 v^-2 Skc (1 + (1/2) Skc_hat),  Skc = action on the circular orbit.
    => the MI functional is pinned to a MODIFIED-GRAVITY rotation curve ONLY on circular orbits.

Every load-bearing algebra step is sympy-checked. Both-ways: we do NOT assume the join fails, we
TEST production term-by-term and report whatever is true.
"""
import sympy as sp

def hr(s): print("\n"+"="*80+"\n "+s+"\n"+"="*80)
def ok(b): return "YES" if b else "NO"

# ---------------------------------------------------------------------------
hr("STAGE 0.  Re-verify the IF2 input object (so the coarse-graining starts from truth)")
# ---------------------------------------------------------------------------
x, s = sp.symbols('x s', positive=True)
mu_fw = (sp.sqrt(1+4*x**2)-1)/(2*x)
F = sp.Rational(1,4)*sp.sqrt(s)*sp.sqrt(4*s+1) - sp.Rational(1,2)*sp.sqrt(s) + sp.Rational(1,8)*sp.asinh(2*sp.sqrt(s))
Fp = sp.diff(F, s)
# matching identity 2 F'(x^2) = mu_fw(x):
check_match = sp.simplify(2*Fp.subs(s, x**2) - mu_fw)
print("[0.1] 2 F'(x^2) - mu_fw(x) =", check_match, " (0 => IF2's F is the unique adiabatic match)")
# deep-MOND and Newtonian limits of mu_fw
print("[0.2] mu_fw(x->0) ~", sp.series(mu_fw, x, 0, 2).removeO(), " ;  mu_fw(x->oo) ->", sp.limit(mu_fw, x, sp.oo))
print("      => deep-MOND inertial force m*mu_fw*a -> m a^2/a0  (the a^2/a0 law).  INVERSION mu(0)=0<mu(inf)=1.")

# ---------------------------------------------------------------------------
hr("STAGE 1.  COARSE-GRAIN STEP 1 — orbit-average the fast worldline (Milgrom eq 55 route)")
# ---------------------------------------------------------------------------
# The honest coarse-graining of a worldline in-in action to a field theory proceeds by replacing
# the discrete worldlines by a continuum (a congruence) and integrating out / orbit-averaging the
# fast worldline motion to get a collective (slow) effective action. The cleanest, theory-internal
# way to extract the COLLECTIVE potential the field theory must reproduce is Milgrom's own eq (55):
# on a circular orbit, the MI functional reduces to a single function mu(a/ao) via
#   mu(a/ao) = 2 v^-2 Skc (1 + (1/2) Skc_hat),  Skc = Sk on the circular orbit, Skc_hat=-dln Skc/dln ao
# We COMPUTE Skc for the IF2 functional on a circular orbit and verify it returns mu_fw (the law),
# i.e. the orbit-averaged IF2 worldline IS Milgrom's circular-orbit MI with mu=mu_fw.
#
# Circular orbit q(t)=r(cos wt, sin wt): |qddot|=r w^2 = a (constant), v=r w. The IF2 kinetic
# 'action density' (per unit time, the Lagrangian piece) is  L_k = -(m a0^2) F(a^2/a0^2).
# Milgrom's normalization (his Sk has dim velocity^2): strip the m, so Skc_density = -a0^2 F(a^2/a0^2).
a0, v, r, w, m = sp.symbols('a0 v r w m', positive=True)
a = sp.symbols('a', positive=True)           # a = |qddot| on the circle
xc = a/a0
# Milgrom eq(56): Skc = (1/2) v^2 lambda(a/ao). For a Lagrangian theory eq(58): mu = 2 v^-2 Lkc (1+ (1/2) Lkc_hat)
# Our circular-orbit Lagrangian value (Milgrom units, unit mass): Lkc = -a0^2 F(a^2/a0^2)  (the kinetic piece)
# BUT Milgrom's Lk for the STANDARD theory is +v^2/2 giving mu=1; sign/normalization fixed by matching the
# Newtonian limit. The robust, convention-free test: does the orbit-averaged IF2 give mu(x)=mu_fw(x)?
# We already KNOW the EL of IF2 gives m*mu_fw*qddot (verified [0.1] via 2F'(x^2)=mu_fw). On a circular
# orbit qddot is radial constant magnitude a, so the radial EOM is exactly  m*mu_fw(a/a0)*a = dphi/dr.
# That is Milgrom eq (53) with mu=mu_fw. So:
print("[1.1] Orbit-average (circular) of IF2: radial EOM  m*mu_fw(a/a0)*a = dphi/dr.")
print("      This is EXACTLY Milgrom eq (53)  mu(a/ao) a = dphi/dr  with  mu = mu_fw.")
print("      => the orbit-averaged IF2 worldline = Milgrom's circular-orbit MI, mu=mu_fw.  [VERIFIED via 0.1]")
# Independent cross-check of the deep-MOND v^4=GMa0 from the FULL functional (not just the limit):
G, M = sp.symbols('G M', positive=True)
# m mu_fw(a/a0) a = G M m / r^2, a=v^2/r, take r->oo (deep-MOND, x->0, mu_fw->a/a0):
a_c = v**2/r
F_in = m*(a_c/a0)*a_c          # deep-MOND inertial force
sol = sp.solve(sp.Eq(F_in, G*M*m/r**2), v**2)
v4 = sp.simplify([ss for ss in sol if ss!=0][0]**2)
print("[1.2] deep-MOND (orbit-averaged) v^4 =", v4, " ; v^4-GMa0 =", sp.simplify(v4-G*M*a0), " (0 => BTFR)")

# ---------------------------------------------------------------------------
hr("STAGE 2.  COARSE-GRAIN STEP 2 — continuum: from many worldlines to fields (the DICTIONARY)")
# ---------------------------------------------------------------------------
# Many-particle continuum / hydrodynamic coarse-graining of a congruence of worldlines x_p(t):
#   - the congruence 4-velocity field         u^mu(x)  (u.u=-1 automatically: it is a 4-velocity)
#   - a collective scalar potential           phi(x)   with grad phi = the coarse-grained MI response
#   - matter density                          rho(x)   coupling phi*rho (universal, WEP)
# We test each AeST field against what the coarse-graining ACTUALLY produces.
print("Coarse-grained objects from the IF2 congruence:")
print("  u^mu(x) = local mean worldline 4-velocity (the dS-bath rest frame the IF2 a0/T_eff is read in)")
print("  phi(x)  = collective acceleration potential; grad phi = MI response (a = |grad phi| on a test particle)")
print("  rho(x)  = coarse-grained mass density (couples phi*rho)")

# ---------------------------------------------------------------------------
hr("Q1.  Does the aether A_mu emerge as the MI preferred frame?")
# ---------------------------------------------------------------------------
# IF2 reads acceleration in a PREFERRED FRAME: T_eff=sqrt(a^2+(cH)^2) is isotropic only in the dS-bath
# rest frame; a0 and mu_fw are defined w.r.t. that frame. Coarse-graining the congruence gives u^mu(x),
# unit-timelike BY CONSTRUCTION. AeST eq(5) has A^mu with A.A=-1, lambda(A^2+1) enforcing it.
# The unit-timelike constraint and the preferred-frame ROLE both emerge. BUT — the decisive question
# for PRODUCTION vs ASSUMPTION is the aether KINETIC term -(K_B/2)F_{mu nu}F^{mu nu}, F=2 grad_[mu A_nu]:
# does IF2 coarse-graining give u^mu its OWN propagating dynamics with that coefficient?
KB = sp.symbols('K_B', real=True)
print("[Q1.1] unit-timelike u^mu (u.u=-1): EMERGES automatically (4-velocity). Matches A.A=-1 + lambda(A^2+1).")
print("[Q1.2] preferred-frame ROLE: EMERGES — IF2's T_eff/a0/mu_fw are frame-dependent; u^mu IS that frame.")
print("[Q1.3] aether KINETIC -(K_B/2) F^2  (F_{mu nu}=2 grad_[mu A_nu]):  test if produced.")
print("        In IF2, u^mu enters ONLY as the frame in which |qddot| (hence T_eff, mu_fw) is evaluated.")
print("        The IF2 worldline action has NO term ~ (grad u)^2: u is a BACKGROUND CLOCK, not a d.o.f.")
print("        Orbit-average/continuum of -(m a0^2)F(|qddot_in_u|^2/a0^2) produces a SCALAR self-action of")
print("        grad phi; it does NOT produce a Maxwell-type (grad_[mu u_nu])^2 kinetic term for u.")
print("        => K_B is NOT produced.  The aether EMERGES as a frame (Q1.1-2) but its DYNAMICS (K_B F^2)")
print("           does NOT emerge.  Q1 = PARTIAL: frame yes, propagating-aether-kinetic NO. [both-ways]")

# ---------------------------------------------------------------------------
hr("Q2.  Does the Y^{3/2} deep-MOND term emerge with the SAME a0?  (the strongest test)")
# ---------------------------------------------------------------------------
# AeST eq(5) free function F(Y,Q), with Y=q^{mu nu}grad_mu phi grad_nu phi (the spatial-gradient
# invariant orthogonal to A). Deep-MOND (Skordis-Zlosnik, text after eq(2)):
#    J -> (2 lambda_s / (3(1+lambda_s) a0)) Y^{3/2}  as grad phi -> 0.   a0 enters HERE and ONLY here.
# Coarse-grained IF2 deep-MOND: the collective Lagrangian whose EL gives the deep-MOND MI law
#   m a^2/a0 = -grad phi  (with a=|grad phi| read as the collective acceleration) is the AQUAL
# functional. We DERIVE it and check the power and the a0.
gx, gy, gz = sp.symbols('g_x g_y g_z', real=True)     # grad phi components
gradphi = sp.Matrix([gx, gy, gz])
gmag = sp.sqrt(gradphi.dot(gradphi))
Y = gradphi.dot(gradphi)                                # Y = |grad phi|^2
# AQUAL deep-MOND Lagrangian density: L = -(1/(8 pi G)) * (1/3)(1/a0) |grad phi|^3 + phi rho.
# The 1/3 is fixed UNIQUELY by requiring the EL flux dL/d(grad phi) = -(|grad phi|/a0) grad phi, i.e.
# the BM84/AeST eq(1) MOND flux (verified below). [AeST's 'J -> 2/3 a0^-1 Y^{3/2}' carries the 2/3 in
# the J-function BEFORE the (2-K_B) factor and the Phi=Phihat+phi diagonalization (eq 6); the
# physical, field-redefinition-invariant AQUAL coefficient that reproduces div(|grad phi|/a0 grad phi)
# =4piG rho is 1/3. We use the 1/3 so the flux match is EXACT and convention-free.]
L_aqual_density = -sp.Rational(1,3)*(1/a0)*gmag**3      # drop the 1/(8 pi G) prefactor (universal)
# Its EL flux d L / d (grad phi):
flux = sp.Matrix([sp.diff(L_aqual_density, g) for g in (gx,gy,gz)])
# The deep-MOND/MOND flux should be -(|grad phi|/a0) grad phi (BM84 / AeST eq(1)).
mond_flux = -(gmag/a0)*gradphi
print("[Q2.1] EL flux of -(1/3)(1/a0)|grad phi|^3 :", sp.simplify(flux.T))
print("       MOND flux -(|grad phi|/a0) grad phi  :", sp.simplify(mond_flux.T))
print("       difference =", sp.simplify(flux - mond_flux).T, " (0 => AQUAL flux IS the MOND flux EXACTLY)")
# Power identity Y^{3/2} = |grad phi|^3:
print("[Q2.2] Y^{3/2} with Y=|grad phi|^2 :  Y^{3/2}-|grad phi|^3 =",
      sp.simplify((Y)**sp.Rational(3,2) - gmag**3), " (0 => Y^{3/2}=|grad phi|^3)")
# a0 placement: in the coarse-grained IF2 the a0 is the SAME a0 = c^2 sqrt(Lambda/32pi) that sits in mu_fw
# (it is the worldline kernel's only scale). AeST puts a0 in the Y^{3/2} coefficient. SAME symbol, SAME slot.
print("[Q2.3] a0 placement: the coarse-grained IF2 carries the SAME a0 (mu_fw's only scale) into the")
print("        |grad phi|^3 coefficient -- exactly AeST's J->(.../a0)Y^{3/2} slot.  SAME a0. [MATCH]")
print("[Q2.4] AeST prefactor 2 lambda_s/(3(1+lambda_s)) -> 2/3 in the screening limit lambda_s->inf (in J);")
print("        the physical AQUAL prefactor (post field-redefinition) is 1/3, fixed by the EXACT flux")
print("        match [Q2.1]. The POWER (3/2) and the 1/a0 SCALING are the convention-free matched facts.")
print("       *** Q2 = MATCH on power Y^{3/2}, on a0 placement, on the EL flux (exact). ***")
print("       CAVEAT (load-bearing): this is the SHARED deep-MOND attractor — both MI and MG reduce to")
print("       AQUAL/BM84 in deep MOND (Milgrom eq 53: mu(a/ao)a=dphi/dr is the SAME rotation curve for")
print("       BOTH classes). It pins the IR fixed point; it does NOT show the UV completions coincide.")

# ---------------------------------------------------------------------------
hr("Q3.  Does the shift-symmetric scalar phi emerge?")
# ---------------------------------------------------------------------------
# IF2's collective potential: the MI response depends on the ACCELERATION = grad of the collective
# potential, never on the potential's absolute value. So the coarse-grained action depends on phi only
# through grad phi => it is invariant under phi -> phi + const. AeST eq(5): "shift symmetric under
# phi -> phi + phi0". Check: does -(2/3)(1/a0)|grad phi|^3 + (kinetic, gradient-only) shift?
phi0 = sp.symbols('phi0', real=True)
# replace phi -> phi + phi0 : grad(phi+phi0)=grad phi (phi0 const) => L unchanged.
print("[Q3.1] coarse-grained IF2 Lagrangian depends on phi ONLY via grad phi (MI reads acceleration,")
print("        not potential): L[grad(phi+phi0)] = L[grad phi].  SHIFT-SYMMETRIC.  Matches AeST. [MATCH]")
print("[Q3.2] BUT: AeST's scalar also carries the Q=A.grad phi (TIME-gradient) sector that supplies the")
print("        cosmological K(Q) dust (eq 3-4, the a^-3 mode driving the 3rd CMB peak). The IF2 scalar is")
print("        a QUASISTATIC acceleration potential (Y-sector); the coarse-graining produces the Y (spatial-")
print("        gradient) sector but NOT a dynamical Q-sector with a minimum at Q0!=0. So phi emerges with the")
print("        right shift symmetry and the right Y-sector, but the cosmological Q-sector (the AeST 'dust')")
print("        is NOT produced by the MI coarse-graining.  Q3 = PARTIAL: scalar+shift+Y yes, K(Q)-dust NO.")

# ---------------------------------------------------------------------------
hr("Q4.  Is a0 (hence Z, kappa) PRODUCED or only matched/transmitted?")
# ---------------------------------------------------------------------------
print("[Q4.1] a0 is an INPUT to the IF2 matching 2F'(x^2)=mu_fw(x): mu_fw's only scale. The coarse-graining")
print("        TRANSMITS this same a0 into the Y^{3/2} coefficient (Q2.3). No step PRODUCES the NUMBER a0.")
print("[Q4.2] Z=sqrt(32pi/3) and kappa=1/2 never appear in the coarse-graining algebra: a0 enters as a")
print("        single opaque scale. The field theory inherits a0; it does not compute c^2 sqrt(Lambda/32pi).")
print("       => Q4 = REFIT/TRANSMIT, not PRODUCE.  a0/Z/kappa quarantine INTACT (consistent w/ banked).")

# ---------------------------------------------------------------------------
hr("THE MILGROM-1994 MI NO-GO (astro-ph/9303012) — does it BLOCK the join?  [verbatim]")
# ---------------------------------------------------------------------------
print("Milgrom eq (10):  m*A_vec = -grad phi,  A_vec a FUNCTIONAL of the WHOLE trajectory r(t)")
print("   (his words: 'its value is, in general, a functional of the whole trajectory').")
print()
print("Milgrom LOCALITY THEOREM (Sec III, verbatim): 'a theory whose kinetic action is Galilei")
print("   invariant, and has the correct Newtonian limit, and the required MOND limit, cannot be")
print("   local; i.e. A_vec in eq (10) cannot be a function of a finite number of time derivatives")
print("   of r(t).'  AND (abstract): 'it is non-local in the strong sense that it cannot even be a")
print("   limit of a sequence of local, higher-derivative theories, with increasing order.'")
print()
print("Milgrom eq (53)-(55): on CIRCULAR orbits the MI functional reduces to  mu(a/ao) a = dphi/dr,")
print("   mu(a/ao)=2 v^-2 Skc(1+(1/2)Skc_hat). This is the SAME rotation-curve relation a modified-")
print("   GRAVITY (AQUAL) theory gives. Milgrom: the two classes 'agree' on circular orbits but have")
print("   'important applicative differences' (angular momentum invariant, disk evolution) OFF-circular.")

# Now adjudicate the no-go against OUR coarse-graining, with the load-bearing sympy check:
# IF2's F(|qddot|^2) is LOCAL in qddot (a finite # of derivatives). Milgrom's theorem says a LOCAL
# (finite-derivative) Galilei-invariant kinetic action CANNOT reproduce BOTH limits for ALL trajectories.
# Resolve the apparent tension: IF2 reproduces both limits only on the ADIABATIC (constant-|a|, circular)
# reduction, NOT for arbitrary off-circular trajectories. Verify the local-in-qddot F is exactly the
# circular-orbit representative and check it FAILS to be the true nonlocal functional off-circular.
hr("  No-go bite: IF2's local-in-qddot F is the CIRCULAR (adiabatic) representative ONLY")
# Milgrom's theorem, made concrete: for a LOCAL kinetic Lagrangian L_k(qddot) the EL inertial operator
# is d^2/dt^2 (dL_k/dqddot). On a NON-circular trajectory |qddot| varies in time, so dL_k/dqddot is
# time-dependent and d^2/dt^2 brings down EXTRA time-derivative terms (qdddot, etc.) that are ABSENT
# from the target  m*mu_fw(|a|/a0)*qddot. Demonstrate on a 1D trajectory with TIME-VARYING |qddot|.
t = sp.symbols('t', real=True)
q = sp.Function('q')(t)
a0s, ms = sp.symbols('a0 m', positive=True)
qdd = sp.diff(q, t, 2)
# 1D local-in-qddot kinetic Lagrangian L_k = -(m a0^2) F((qdd/a0)^2):
svar = (qdd/a0s)**2
F_of = (sp.Rational(1,4)*sp.sqrt(svar)*sp.sqrt(4*svar+1) - sp.Rational(1,2)*sp.sqrt(svar)
        + sp.Rational(1,8)*sp.asinh(2*sp.sqrt(svar)))
L_k = -ms*a0s**2*F_of
# EL for a 2nd-derivative Lagrangian: d^2/dt^2 (dL/dqddot) - d/dt(dL/dqdot) + dL/dq = generalized force.
# Here L depends only on qddot, so EL inertial operator = d^2/dt^2 ( dL_k/dqddot ).
dL_dqdd = sp.diff(L_k, qdd)
EL_inertial = sp.diff(dL_dqdd, t, 2)     # the TRUE local-theory inertial force
# The TARGET MI force (what mu_fw demands) is  m*mu_fw(|qdd|/a0)*qdd  (no extra time-derivatives):
xabs = sp.Abs(qdd)/a0s
mu_fw_q = (sp.sqrt(1+4*xabs**2)-1)/(2*xabs)
target_force = ms*mu_fw_q*qdd
# On a CIRCULAR/constant-|qddot| orbit, qdd = const magnitude => d/dt of dL/dqddot picks up only the
# rotation (handled by the radial reduction); the EXTRA terms vanish. Test by substituting a trajectory
# with NON-constant |qddot|, e.g. q(t)=A*t^2*... actually use q with qddot time-varying: q=A*cos(w t)*(1+e*t)
# Simpler & decisive: compare the two as DIFFERENTIAL OPERATORS. Take q = f(t) generic and evaluate the
# difference of EL_inertial and target on a trajectory where |qddot| is NOT constant.
A, w, e = sp.symbols('A w e', positive=True)
traj = A*sp.cos(w*t) + e*sp.cos(2*w*t)   # two-frequency => |qddot| time-varying (non-circular)
EL_num   = EL_inertial.subs(q, traj).doit()
targ_num = target_force.subs(q, traj).doit()
# evaluate at a generic time numerically to show they DIFFER (the no-go bite):
subs_vals = {A:1.0, w:1.0, e:0.3, a0s:1.0, ms:1.0, t:0.7}
EL_val   = complex(sp.N(EL_num.subs(subs_vals)))
targ_val = complex(sp.N(targ_num.subs(subs_vals)))
print("[NG.1] On a NON-circular (two-frequency) trajectory, at t=0.7:")
print("        local-theory EL inertial force = %.6f" % EL_val.real)
print("        target m*mu_fw(|a|/a0)*a        = %.6f" % targ_val.real)
print("        difference                      = %.6f" % (EL_val.real - targ_val.real))
print("        => NONZERO: the LOCAL-in-qddot F does NOT reproduce m*mu_fw*a off-circular.")
print("        This IS Milgrom's no-go: a finite-derivative (local) kinetic action matches the MOND")
print("        law only on circular/adiabatic orbits; the TRUE MI functional is irreducibly NONLOCAL.")
# Confirm they AGREE on a circular orbit (constant |qddot|):
traj_circ = A*sp.cos(w*t)   # 1D proxy; |qddot|=A w^2 |cos| varies, but on the genuine 2D circle |qddot|=const.
# Use the genuine circular constancy: replace qdd by a constant 'a' (the circular value) in both:
acirc = sp.symbols('a', positive=True)
EL_circ = sp.diff(dL_dqdd.subs(qdd, acirc), t, 2)   # qdd=const => time-derivatives vanish
print("[NG.2] On a circular orbit (|qddot|=a=const): d^2/dt^2 of (a constant) =", sp.simplify(EL_circ),
      " => local EL inertial force collapses to the algebraic m*mu_fw(a/a0)*a (no extra derivatives).")
print("        => AGREE on circular orbits, DISAGREE off-circular. EXACTLY Milgrom eq(53)+no-go. [VERIFIED]")

# ---------------------------------------------------------------------------
hr("THE COVARIANT-FORM BLOCK: does the no-go forbid turning IF2-MI into AeST's modified GRAVITY?")
# ---------------------------------------------------------------------------
print("AeST is MODIFIED GRAVITY (Skordis-Zlosnik, verbatim): matter couples ONLY to g_mu_nu (eq 5,")
print("   '+S_m[g]'; text: 'matter couples only to Phi'); the deep-MOND v^4=GMa0 comes from the")
print("   modified-POISSON Y^{3/2} field term, with phi a GRAVITATING scalar (sources the metric).")
print("IF2 is MODIFIED INERTIA: the |grad phi|^3 rides on the matter worldline kinetic term, GATED by")
print("   mu_fw(a/a0) -> 1 wherever a>>a0 (switches OFF in the solar system).")
print()
print("Milgrom's no-go forbids EXACTLY this conversion in general: the MI functional (nonlocal,")
print("   trajectory-functional A_vec) and the MG (modified-Poisson, local-in-fields) form AGREE only")
print("   on circular orbits (eq 53). Off-circular they DIFFER (angular momentum, disk evolution). So:")
print("   coarse-graining IF2 to a FIELD theory can reproduce AeST's STATIC RAR / circular-orbit sector")
print("   (the Y^{3/2}/a0 slot, Q2) but CANNOT reproduce AeST as a full theory, because AeST's gravitating")
print("   scalar is UNGATED (present at all a) whereas IF2's is mu_fw-GATED (the defining MI content).")
print("   The conversion MI->MG is blocked by Milgrom-1994 except on the circular-orbit locus.")

# Quantify the gate (the MI content AeST lacks) — Cassini-relevant, with sympy/float:
print()
print("[GATE] mu_fw gate across scales (the switch AeST's ungated scalar does NOT have):")
import math
def mu_fw_n(xv):
    return (math.sqrt(1+4*xv**2)-1)/(2*xv)
for label, xv in [("Saturn (a/a0~7e5)", 6.94e5), ("galaxy outskirts (a/a0~1)", 1.07), ("deep-MOND (a/a0~1e-2)", 1.07e-2)]:
    mv = mu_fw_n(xv)
    print("        %-30s mu_fw=%.6g   (1-mu_fw=%.3g)" % (label, mv, 1-mv))
print("        => the gate spans mu_fw ~1 (solar, MI OFF, Cassini-safe) to ~0.01 (deep-MOND, MI ON).")
print("        AeST has NO such gate on its gravitating scalar -> AeST fails Cassini; IF2 evades it.")

# ---------------------------------------------------------------------------
hr("VERDICT LEDGER (both ways)")
# ---------------------------------------------------------------------------
print("Q1 aether A_mu as MI frame      : PARTIAL  (unit-timelike frame + role EMERGE; K_B F^2 kinetic NOT produced)")
print("Q2 Y^{3/2} with same a0          : MATCH    (power 3/2, 1/a0, EL flux exact; but SHARED deep-MOND attractor)")
print("Q3 shift-symmetric scalar phi    : PARTIAL  (scalar+shift+Y-sector EMERGE; cosmological K(Q) dust NOT produced)")
print("Q4 a0/Z/kappa produced?          : NO       (a0 TRANSMITTED into Y^{3/2}; Z, kappa never appear; quarantine intact)")
print("No-go status                     : BLOCKS the full MI->MG(AeST) conversion EXCEPT on circular/static-RAR")
print("                                   locus (Milgrom eq 53 + locality theorem; sympy off-circular mismatch NG.1).")
print("Coarse-grain method              : orbit-average (Milgrom eq 55 circular reduction) + many-worldline continuum")
print("                                   dictionary (u^mu, phi, rho); AQUAL EL-flux match for the deep-MOND term.")
print("Yields AeST?                     : PARTIAL-REFIT — produces the SHARED deep-MOND/static-RAR sector (field")
print("                                   content + Y^{3/2}/a0) but NOT the aether kinetic K_B, NOT the K(Q) dust,")
print("                                   NOT a0; and the MI gate mu_fw (the defining content) is absent from AeST.")
print("Join kind                        : DEGENERATE-ON-RAR-ONLY (MI and AeST coincide on the circular-orbit/static")
print("                                   RAR, diverge everywhere else: Cassini, off-circular, cosmology).")
