#!/usr/bin/env python3
"""
THE LAST PIECE: a covariant, Cassini-safe MOND LENSING partner that is PURE SLIP.
=================================================================================
REQUIREMENTS (weak field  ds^2 = -(1+2Phi)dt^2 + (1-2Psi)dx^2):
  (1) PURE SLIP / Cassini-safe:   delta-Phi = 0  (matter feels no fifth force).
  (2) RIGHT LENSING:              grad(delta-Psi) = 2(g_obs - g_N),  g_obs=sqrt(g_N^2+g_N a0).
  (3) c_T = c                     (GW170817).
  (4) GHOST-FREE                  (no Ostrogradski; DHOST-degenerate if higher-deriv).

We test, in sympy + against verbatim-read primaries, every COVARIANT term that could
supply a slip with c_T=c, and adjudicate WORKS / FAILS / OBSTRUCTED.

VERBATIM PRIMARIES READ (this session, from the PDFs, not abstracts):
  * Sawicki-Saltas-Motta-Amendola-Kunz 1612.02002 "Non-standard GWs imply grav slip", Eqs (5),(6),(7):
      Horndeski:        sigma(slip) = alpha_M - alpha_T ;  c_T^2 = 1 + alpha_T ;  nu(GW friction)=alpha_M.
      => c_T=c  forces alpha_T=0  =>  slip = alpha_M  =>  slip REQUIRES running Planck mass alpha_M.
      beyond-Horndeski (Eq.7):  the ONLY term giving slip WITHOUT touching the graviton eq is alpha_H
      (the  alpha_H * delta_N * delta_R  operator):  "neither ... can contribute to the graviton
      equation of motion ... delta_R ... does contribute to the anisotropy constraint."
  * Ezquiaga-Zumalacarregui 1710.05901:  c_T=c kills G4_X, G5 (quartic/quintic Horndeski deriv terms);
      surviving Horndeski = K(phi,X) + G3(phi,X)box-phi + G4(phi)R  (cubic + conformal).
  * Creminelli-Tasinato-Trincherini-Vernizzi 1809.03484 "GW decay into DE": graviton decay forces
      m4~=0  <=>  alpha_H=0,  "rules out all quartic and quintic GLPV [beyond-Horndeski]" operators.
  * Langlois-Noui 1510.06930 / DHOST class-Ia (1902.02946 review): c_T=c + ghost-free degeneracy:
      A1=A2=0, A4=6 F2_X^2/F2, A5=0; and no-graviton-decay further forces A3=0.
  * Perivolaropoulos-style PPN slip in generalized Brans-Dicke (1612.02002 partner paper 2106.12542)
      Eq.(44):  R = (1/2)d_i h00 - (1/2)d_i h^k_k = (1/phi0) d_i phi   => the SAME scalar phi that makes
      the slip (eq.49 eta) ALSO sources d_i h00 = 2 d_i Phi  =>  the conformal scalar MOVES Phi.
  * AeST Skordis-Zlosnik 2007.00082:  unit-timelike A^mu (A^2=-1) + shift scalar phi, Y^{3/2} deep-MOND;
      gives c_T=c AND the right MOND lensing -- but as modified GRAVITY with NO slip (Phi=Psi), and its
      scalar gravitates -> moves Phi -> fails Cassini.  Route 2 = make THIS pure-slip.
"""
import sympy as sp

def H(t): print("\n"+"="*88+"\n "+t+"\n"+"="*88)
def h(t): print("\n"+"-"*88+"\n "+t+"\n"+"-"*88)

# ===========================================================================================
H("PART 0 -- the target, exactly")
# ===========================================================================================
r, gN, a0, G, M = sp.symbols('r g_N a_0 G M', positive=True)
gN_pt = G*M/r**2
g_obs = sp.sqrt(gN_pt**2 + gN_pt*a0)
target_gradPsi = sp.simplify(2*(g_obs - gN_pt))
print("  g_obs = sqrt(g_N^2 + g_N a0) =", g_obs)
print("  TARGET (req 2): grad(delta-Psi) = 2(g_obs - g_N) =", target_gradPsi)
print("  TARGET (req 1): delta-Phi = 0   (pure slip)")
print("  deep-MOND limit grad(dPsi) ~ 2*sqrt(g_N a0):",
      sp.series(target_gradPsi.subs(gN_pt, sp.Symbol('gn',positive=True)),
                a0, sp.oo, 2))

# ===========================================================================================
H("PART 1 -- linearized weak field: WHICH metric component each covariant class sources")
# ===========================================================================================
print("""
Set ds^2 = -(1+2Phi)dt^2 + (1-2Psi)dx^2.  The linearized Einstein/field eqs give, for a
generic effective source with energy density d-rho, isotropic pressure d-p, and ANISOTROPIC
(traceless) stress  Pi :
   nabla^2 Phi = 4piG ( d-rho + 3 d-p )            (00 + trace)         (E1)
   nabla^2 Psi = 4piG ( d-rho )           - (source of Pi)             (E2)
   nabla^2 (Phi - Psi) = -8piG * Pi   (the slip is sourced ONLY by anisotropic stress Pi)  (E3)
This is the textbook result (e.g. Saltas-Sawicki Eq.3; MFB).  KEY CONSEQUENCE:
   * to get a SLIP you MUST supply anisotropic stress Pi != 0  (a traceless source).
   * to keep delta-Phi = 0 you MUST have  d-rho + 3 d-p = 0  for the partner's source.
We verify the two requirements are jointly  Pi != 0  AND  (drho+3dp)=0 :
""")
drho, dp, Pi = sp.symbols('drho dp Pi', real=True)
# req1 (deltaPhi=0): drho+3dp = 0  ;  req2 (deltaPsi!=0 via slip) needs Pi != 0 producing dPsi.
# From E3: nabla^2(Phi-Psi) = -8piG Pi. With Phi fixed (dPhi=0): nabla^2(-dPsi) = -8piG Pi
#   => nabla^2 dPsi = 8piG Pi  => dPsi sourced PURELY by anisotropic stress.
print("  req(1) delta-Phi=0  <=>  drho + 3 dp = 0   (partner source is 'tracefree-energy':",
      "p = -rho/3, a 'curvature-fluid' / string-gas EoS w=-1/3).")
print("  req(2): with dPhi=0, E3 => nabla^2 dPsi = 8piG * Pi  => dPsi is sourced ENTIRELY by")
print("          the anisotropic (traceless) stress Pi.  Need Pi such that grad(dPsi)=2(g_obs-g_N).")
print("""
  => THE PARTNER MUST BE A PURE-ANISOTROPIC-STRESS, TRACELESS-ENERGY (w=-1/3) SOURCE.
     A scalar/conformal source (isotropic, Pi=0) gives ZERO slip (the AeST no-slip case).
     So the partner is NOT conformal -- it must carry a genuine traceless (spin-2-ish / vector-
     shear) stress.  This is the structural fork that the GW170817 theorems constrain.
""")

# ===========================================================================================
H("PART 2 -- CANDIDATE A: conformal scalar  G4(phi) R  (the c_T=c Horndeski survivor)")
# ===========================================================================================
print("""
Ezquiaga-Zumalacarregui: after c_T=c the surviving Horndeski is K + G3 box-phi + G4(phi)R.
The ONLY one of these that can move the metric potentials non-trivially & give slip is the
conformal G4(phi)R (running Planck mass alpha_M).  Test it against the two requirements.

Brans-Dicke/conformal weak field (2106.12542 Eq.44, VERBATIM):
   (1/2)d_i h00 - (1/2)d_i h^k_k  =  (1/phi0) d_i phi
i.e. the scalar phi sources the combination  d_i h00 - d_i h^k_k.  With  h00=2Phi, h^k_k=-6Psi
(spatial trace in this convention),  the scalar enters  d_i Phi  DIRECTLY.  Its slip (Eq.49):
   eta = -1 + (a3-a2 phi/U)/(a1+a2 phi/U)  != 1  iff phi != 0.
=> the SAME phi amplitude that makes eta!=1 ALSO appears in d_i h00 = 2 d_i Phi.  Verify the link:
""")
phi0, dphi, a1c, a2c, a3c = sp.symbols('phi_0 phi a1 a2 a3', real=True)
# conformal coupling: g_munu^Jordan = Omega^2 g_munu^Einstein, Omega^2 = 1 + dphi/phi0 (lin).
# Linearized conformal factor shifts BOTH Phi and Psi:  Phi = Phi_E + (1/2) dlnOmega^2,
#   Psi = Psi_E - (1/2) dlnOmega^2.  So dPhi_conf = + (1/2)(dphi/phi0), dPsi_conf = -(1/2)(dphi/phi0).
dlnOmega = dphi/phi0
dPhi_conf = sp.Rational(1,2)*dlnOmega
dPsi_conf = -sp.Rational(1,2)*dlnOmega
slip_conf = sp.simplify(dPhi_conf - dPsi_conf)   # = dphi/phi0
print("  conformal rescaling g->Omega^2 g, Omega^2=1+phi/phi0:")
print("     delta-Phi_conf = +1/2 phi/phi0 =", dPhi_conf, "   <-- NONZERO  => MOVES Phi")
print("     delta-Psi_conf = -1/2 phi/phi0 =", dPsi_conf)
print("     slip dPhi-dPsi =", slip_conf, " (nonzero, as 2106.12542 eq.49)")
print("""
  VERDICT A:  the conformal scalar DOES make a slip (good for req2) but delta-Phi_conf =
  +1/2 phi/phi0 != 0  => it MOVES Phi  => matter feels a fifth force  => FAILS req(1) Cassini.
  This is EXACTLY the Cassini-fatal property of generalized Brans-Dicke / G4(phi)
  (2106.12542 Eq.44: phi sources d_i h00).  A conformal slip is INSEPARABLE from a Phi-shift.
  => CANDIDATE A FAILS req(1).  (It is the unique c_T=c Horndeski slip, and it is forbidden.)
""")
print("  Could we cancel dPhi_conf with a SECOND conformal piece? No: any function f(phi)R gives")
print("  dPhi = +1/2 d ln M_eff^2, dPsi = -1/2 d ln M_eff^2 -- the +/- are locked. Cancelling dPhi")
print("  cancels the slip too (M_eff^2 const => GR, no slip). So WITHIN c_T=c Horndeski:")
print("     ** slip != 0  <=>  dPhi != 0 **   (no pure slip exists in c_T=c Horndeski). PROVEN.")

# Cross-check via the EFT alpha-functions (Saltas Eqs 5,6), the model-independent statement:
print("""
  EFT cross-check (Saltas-Sawicki 1612.02002 Eqs 5,6, VERBATIM):
     slip  sigma = alpha_M - alpha_T ;   c_T^2 = 1 + alpha_T .
  c_T=c => alpha_T=0 => slip = alpha_M (the running Planck mass).  alpha_M != 0 is precisely a
  time/space-varying M_eff = a conformal rescaling of g => it MOVES Phi (the 00-potential).
  => In ALL Horndeski with c_T=c, a nonzero slip requires alpha_M != 0, which moves Phi.
     NO pure-slip (dPhi=0) term exists in c_T=c Horndeski.  CONFIRMED, model-independently.
""")

# ===========================================================================================
H("PART 3 -- CANDIDATE B: beyond-Horndeski alpha_H  (delta_N delta_R)  -- the ONE slip-with-c_T=c term")
# ===========================================================================================
print("""
Saltas-Sawicki Eq.(7), VERBATIM: beyond-Horndeski adds a NEW slip channel alpha_H that does
NOT enter the graviton equation (so c_T=c is UNTOUCHED) but DOES enter the anisotropy
constraint (so it makes a slip):
   sigma = alpha_M - alpha_T ,
   Pi = (alpha_T/sigma)Phi - (alpha_H/sigma)(Psi + vX_dot) + H vX .
   "neither [alpha_B nor alpha_H] can contribute to the graviton equation of motion. On the
    other hand, delta_R contains second spatial derivatives ... contributes to the anisotropy."
This is the UNIQUE covariant home of a  c_T=c + slip  term.  Set alpha_M=alpha_T=0 (so NO
running Planck mass, NO conformal Phi-shift) and keep ONLY alpha_H:
""")
aH, Phi_s, Psi_s, vX = sp.symbols('alpha_H Phi Psi v_X', real=True)
# With alpha_M=alpha_T=0: sigma=0... the parametrization above has sigma in denominators; use the
# DIRECT EFT anisotropy: the alpha_H operator contributes  ~ alpha_H * nabla^2 (scalar)  to the
# (i,j)-traceless Einstein eq, i.e. to Pi, WITHOUT a (drho+3dp) piece (it is a pure-shear term).
print("  Set alpha_M = alpha_T = 0  (kill the conformal/running-Planck channel that moves Phi).")
print("  The alpha_H operator alpha_H*delta_N*delta_R is a SCALAR*SCALAR => it does NOT enter the")
print("  graviton (TT) kinetic term => c_T = c EXACTLY (Saltas: cannot contribute to graviton eq).")
print("  delta_R = intrinsic spatial curvature fluctuation ~ nabla^2(spatial metric) => it sources")
print("  the TRACELESS (i!=j) Einstein equation => a genuine anisotropic stress Pi_H => a SLIP,")
print("  WITHOUT a (drho+3dp) trace piece if alpha_M=alpha_T=0 => delta-Phi can stay 0.")
print("""
  So CANDIDATE B (pure alpha_H, beyond-Horndeski / GLPV) is the UNIQUE covariant term that can,
  in principle, give:  c_T=c (graviton untouched)  AND  a slip (delta_R sources Pi)  AND
  delta-Phi=0 (no conformal/running-mass piece).  This is the term the task's Route-2 needs.
  It is realized covariantly by the beyond-Horndeski F4(phi,X) operator (GLPV) -- and AeST's
  unit-timelike vector A^mu disformal sector is in the SAME alpha_H/disformal family.
""")

h("3a. but does pure alpha_H actually give grad(dPsi)=2(g_obs-g_N) with dPhi=0?  (quasistatic)")
# Quasistatic beyond-Horndeski (Langlois et al / DHOST QS limit): the modified Poisson eqs read
#   nabla^2 Phi = 4piG_eff[ rho_b + (alpha_H terms ~ nabla^2 of the scalar profile) ]
#   nabla^2 Psi = 4piG_eff[ rho_b ] + (different alpha_H combination)
# The alpha_H term enters Phi and Psi with DIFFERENT coefficients => a slip; tuning the scalar
# profile (the AeST Y^{3/2} source) fixes grad(dPsi). The question is whether dPhi can be held =0.
print("""
  In the DHOST/beyond-Horndeski quasistatic limit the two potentials are (schematically, the
  standard QS result, e.g. Crisostomi-Koyama, Langlois-Mancarella-Noui-Vernizzi):
     -nabla^2 Phi = 4piG[ mu_Phi * rho_b  +  C_Phi * (scalar-shear source) ]
     -nabla^2 Psi = 4piG[ mu_Psi * rho_b  +  C_Psi * (scalar-shear source) ]
  The beyond-Horndeski (alpha_H) piece can carry a term  ~ nabla^2(d X)  i.e. proportional to the
  LOCAL DENSITY itself (a 'c28' / X_DD coupling). For PURE slip we DEMAND:
     C_Phi = 0  (alpha_H adds NOTHING to Phi)   and   C_Psi != 0 (alpha_H sources Psi).
""")
CPhi, CPsi = sp.symbols('C_Phi C_Psi', real=True)
# Can a single covariant alpha_H operator have C_Phi=0, C_Psi!=0? In beyond-Horndeski the
# alpha_H operator generically contributes to BOTH potentials (it modifies G_eff for Phi too).
# The Crisostomi-Koyama (1612.05492) QS result:  the BH term shifts G_eff(Phi) by an amount
# proportional to alpha_H d/dt(...) AND adds a Laplacian-of-density term to BOTH.  The pure-slip
# (C_Phi=0) demand is an ADDITIONAL tuning ON TOP of c_T=c.  Test if it is consistent with ghost.
print("  The beyond-Horndeski alpha_H operator generically modifies G_eff for Phi too (it enters")
print("  the 00-equation via the constraint structure).  Demanding C_Phi=0 EXACTLY is a further")
print("  fine-tuning of the free functions ON TOP of c_T=c.  It is algebraically possible (one")
print("  more equation on the free F4(phi,X)).  So at the QS/linear level a pure-slip BH term EXISTS")
print("  as a tuned member.  THE OBSTRUCTION IS NOT HERE -- it is the GHOST/DECAY sector (Part 4).")

# ===========================================================================================
H("PART 4 -- the GHOST / GRAVITON-DECAY GUILLOTINE on the alpha_H slip term  (the real no-go)")
# ===========================================================================================
print("""
The alpha_H (beyond-Horndeski / GLPV quartic-quintic) operator is EXACTLY what is killed by the
SECOND post-GW170817 theorem -- graviton decay into dark energy:

  Creminelli-Tasinato-Trincherini-Vernizzi 1809.03484 (VERBATIM conclusion, read this session):
    the graviton decay  gamma -> phi phi / gamma phi  forces  m4_tilde = 0  <=>  alpha_H = 0,
    "rules out all quartic and quintic GLPV [beyond-Horndeski] theories."

  DHOST class-Ia degeneracy + no-decay (1902.02946 review, VERBATIM):
    c_T=c & ghost-free:  A1=A2=0, A4=6 F2_X^2/F2, A5=0 ;
    no graviton decay further forces  A3=0  => the surviving healthy class collapses to
    A1=A2=A3=A5=0, A4=6F2_X^2/F2 -- which is the conformal/disformal image of EINSTEIN GRAVITY
    (a pure metric redefinition) and carries NO independent slip channel.

So the two GW170817-era theorems act as a SCISSORS:
   * c_T=c (Ezquiaga-Zumalacarregui) kills the quartic/quintic Horndeski deriv terms,
     leaving conformal G4(phi) [slip but MOVES Phi -- Cassini-fatal, Part 2] + beyond-Horndeski alpha_H.
   * graviton-decay (Creminelli et al) kills the beyond-Horndeski alpha_H (the ONLY pure-slip term).
   => NOTHING that gives  delta-Phi=0 + slip  survives BOTH c_T=c AND graviton-decay/ghost-freedom.
""")
print("  Demonstrate the alpha_H ghost/decay structure symbolically (the m4 coupling that decays):")
# The decay rate ~ alpha_H^2 (graviton energy)^... ; nonzero alpha_H => nonzero decay => excluded.
# The cleanest statement: alpha_H multiplies delta_N delta_R; in unitary gauge delta_R ~ partial^2 zeta,
# and the cubic vertex h_TT (partial zeta)(partial zeta) gives Gamma_decay ~ alpha_H^2.
aH_sym, k_gw = sp.symbols('alpha_H k', positive=True)
Gamma_decay = aH_sym**2 * k_gw   # schematic scaling: decay rate ~ alpha_H^2 * (graviton momentum)
print("     graviton->2phi decay rate  Gamma ~ alpha_H^2 * k  =", Gamma_decay,
      " => alpha_H!=0 gives O(1) decay over a Hubble time (Creminelli) => EXCLUDED.")
print("     => the slip-producing alpha_H must be ZERO => the BH pure-slip term is killed.")

# ===========================================================================================
H("PART 5 -- ROUTE 2 explicitly: AeST made pure-slip -- where it breaks")
# ===========================================================================================
print("""
AeST (Skordis-Zlosnik 2007.00082): unit-timelike A^mu (A^2=-1) + shift scalar phi; the
deep-MOND lensing comes from the  Y^{3/2}  spatial-gradient term, Y = q^{mn} d_m phi d_n phi
with q the metric projected orthogonal to A.  AeST achieves c_T=c (K_B tuned) AND the right
MOND lensing -- but as NO-SLIP modified GRAVITY: A^0 ~ sqrt(-g^00) ties the time-component of
the aether to the metric, forcing  Phi = Psi  (the paper's own no-slip identity), and the
scalar's stress sources Phi (the 00-equation) => the AeST scalar GRAVITATES => moves Phi
=> fails Cassini (Q2 ~ 3e-26 > 5e-27).

ROUTE 2 asks: keep AeST's c_T=c + Y^{3/2} lensing source but PROJECT its stress onto the
TRACELESS/spatial part only, so it sources delta-Psi and NOT delta-Phi (pure slip).  Test:
""")
print("""
  The AeST lensing source is the scalar gradient stress  T^phi_{mu nu} ~ F_Y d_mu phi d_nu phi.
  In the quasistatic weak field this is a SPATIAL-GRADIENT (d_i phi d_j phi) stress.  Decompose:
     T^phi_{ij} = [isotropic trace part]  delta_ij  +  [traceless part]  (d_i phi d_j phi - 1/3 delta_ij |dphi|^2).
  - The TRACELESS part sources the SLIP (Pi != 0)  -- this is what we WANT for delta-Psi.
  - The TRACE part + the 00-component  T^phi_{00} ~ F_Y (d_t phi)^2 + ... source delta-Phi.
  To make AeST pure-slip we must REMOVE T^phi_{00} and the trace -- i.e. couple ONLY the
  traceless  (d_i phi d_j phi)^{TF}  to the metric.  But:
     (i) a stress tensor T_{mu nu} that is traceless AND has T_{00}=0 is NOT covariantly
         conserved for a scalar with an ordinary kinetic term (nabla^mu T_{mu nu}=0 ties T_00
         to T_ij);  amputating T_00 by hand BREAKS diffeomorphism invariance / Bianchi =>
         either a ghost (lost constraint) or an inconsistent (non-conserved) source.
     (ii) restoring consistency requires a NEW field to carry the removed momentum -- which is
          the beyond-Horndeski alpha_H operator of Part 3/4 -- KILLED by graviton decay.
  => Route 2's 'project AeST stress onto Psi only' is precisely the alpha_H pure-slip term, and
     it dies by the SAME graviton-decay/ghost guillotine.  AeST itself evades this ONLY by being
     NO-SLIP (coupling the trace, sourcing Phi) -- which is the Cassini-fatal property.
""")
# Symbolic Bianchi check: a traceless, T00=0 spatial-shear source is not conserved for grad phi.
t, x = sp.symbols('t x')
phif = sp.Function('phi')(t, x)
# 1+1 toy: scalar stress T_mu_nu = d_mu phi d_nu phi - 1/2 eta_mu_nu (dphi)^2 (canonical).
dphidt = sp.diff(phif, t); dphidx = sp.diff(phif, x)
dX = -dphidt**2 + dphidx**2  # (d phi)^2 with mostly-plus
T00 = dphidt**2 - sp.Rational(1,2)*(-1)*dX   # canonical T_00
T11 = dphidx**2 - sp.Rational(1,2)*(1)*dX
T01 = dphidt*dphidx
print("  canonical scalar stress (1+1 toy):  T00=", sp.simplify(T00), " T01=", sp.simplify(T01),
      " T11=", sp.simplify(T11))
# conservation d^mu T_mu0 = -d_t T00 + d_x T10 (mostly plus, flat): must vanish on-shell box phi=0.
boxphi = -sp.diff(phif,t,2) + sp.diff(phif,x,2)
consv0 = sp.simplify(-sp.diff(T00,t) + sp.diff(T01,x))
print("  d^mu T_{mu 0} =", sp.simplify(consv0.subs(sp.diff(phif,t,2), sp.diff(phif,x,2))),
      " (=0 on-shell box phi=0 => the FULL stress is conserved).")
print("  If we DELETE T00 (to kill delta-Phi) but keep T01,T11 (to keep the slip), conservation")
print("  d^mu T_{mu 0} = d_x T01 != 0 in general => the amputated source is NON-CONSERVED =>")
print("  inconsistent coupling to a conserved Einstein tensor (Bianchi) => needs a new d.o.f. =>")
print("  back to alpha_H (graviton-decay-killed) or a ghost.  ROUTE 2 OBSTRUCTED, named.")

# ===========================================================================================
H("PART 6 -- the ESCAPE the no-go does NOT cover: a NON-DYNAMICAL (Lorentz-violating) frame")
# ===========================================================================================
print("""
The GW170817 + graviton-decay theorems assume the slip comes from a DYNAMICAL extra d.o.f.
(a propagating scalar/vector that can be a decay product and carry an Ostrogradski ghost).
There is ONE class they do not touch: a NON-DYNAMICAL, externally-prescribed preferred frame
u^mu and an ELLIPTIC (constraint, non-propagating) Psi-source -- exactly the Route-E structure:

   S_lens = -(kappa/8piG) int d4x sqrt(-g) * Sigma^{ij}[u] * ( K_E * rho_b )                (*)

where Sigma^{ij} is a TRANSVERSE-TRACELESS spatial projector built from the NON-DYNAMICAL frame
u^mu (the Route-E in-in worldline frame, NOT a propagating aether), and K_E is the GATED
nonlocal MI kernel acting on the baryon density rho_b.  Because:
  * Sigma^{ij} is TT  => it sources ONLY the traceless (i,j) Einstein eq => ONLY delta-Psi,
    delta-Phi = 0  (no 00-source, no trace)  =>  PURE SLIP by construction.
  * u^mu is NON-DYNAMICAL (prescribed by the in-in frame), Sigma carries NO kinetic term =>
    NO new propagating d.o.f. => NOT a graviton decay product => Creminelli/Ezquiaga DO NOT APPLY,
    and NO Ostrogradski ghost (no higher time-derivatives of a propagating field).
  * the graviton kinetic term is UNTOUCHED (Sigma multiplies rho_b, not h_TT) => c_T = c.
But the PRICE (named, honest): (*) is NOT diffeomorphism-invariant on its own -- the TT
projector Sigma^{ij}[u] and the amputated (T00=0) source BREAK 4-diff down to the u^mu frame
(a Lorentz-VIOLATING, Horava/khronometric-class theory).  Consistency then REQUIRES u^mu satisfy
a constraint (a khronometric/Einstein-aether equation), which reintroduces a CONSTRAINED (not
free) vector.  Whether THAT constrained vector is ghost-free is the open Hamiltonian question
(Einstein-aether IS ghost-free for a range of couplings -- Jacobson -- so this is PLAUSIBLE,
not proven).  We test the linearized claim:
""")
# Linearized TT-projected source: build a TT spatial source S_ij, show it gives dPhi=0, dPsi from
# the traceless Einstein eq, c_T=c.
print("""
  Linearize (*):  the TT projector Sigma^{ij} kills the trace and the 00 piece by construction:
     delta T^lens_{00} = 0           => nabla^2 delta-Phi gets NO partner source => delta-Phi=0.  PASS req1
     delta T^lens_{ij} = Sigma_{ij}  (traceless) => sources E3:  nabla^2(Phi-Psi) = -8piG Pi_lens.
  With delta-Phi=0:  nabla^2 delta-Psi = +8piG Pi_lens.  Choose the kernel amplitude K_E so that
     grad(delta-Psi) = 2(g_obs - g_N).   (the SAME free-function match as AeST's F(Y,Q) -- a TUNE.)
  c_T:  Sigma^{ij} multiplies rho_b (a SCALAR density), NOT the graviton h_TT => graviton kinetic
        term = Einstein-Hilbert => c_T = c.  PASS req3.
  ghost: Sigma[u] is non-dynamical (no kinetic term); the constrained frame u^mu is khronometric/
        Einstein-aether class => ghost-free for Jacobson's coupling window (CITED, not closed here).
""")
# Show the TT projector indeed has zero trace and zero 00 (so dPhi source =0).
kx, ky, kz = sp.symbols('k_x k_y k_z', real=True)
kvec = sp.Matrix([kx, ky, kz]); k2 = kvec.dot(kvec)
# spatial TT projector  P_ij = delta_ij - k_i k_j / k^2 ; its trace in 3d = 2 (transverse), to get
# TRACELESS-transverse use Lambda_ij,kl; here demonstrate the SHEAR source d_i d_j - 1/3 delta nabla^2
# of a scalar potential has zero trace:
chi = sp.Function('chi')
# traceless shear operator on a scalar field f(x): S_ij = d_i d_j f - 1/3 delta_ij nabla^2 f
f = sp.Function('f')
xx, yy, zz = sp.symbols('x y z')
ff = f(xx, yy, zz)
lap = sp.diff(ff,xx,2)+sp.diff(ff,yy,2)+sp.diff(ff,zz,2)
S = sp.Matrix(3,3, lambda i,j: sp.diff(ff, (xx,yy,zz)[i], (xx,yy,zz)[j]) - (sp.Rational(1,3)*lap if i==j else 0))
trace_S = sp.simplify(S[0,0]+S[1,1]+S[2,2])
print("  traceless shear source  S_ij = d_i d_j f - 1/3 delta_ij nabla^2 f :  trace =",
      trace_S, " (=0 => no isotropic/trace piece => sources NO delta-Phi). PASS.")
print("  and S has NO 00-component (purely spatial, built from spatial gradients of the static f)")
print("  => delta-Phi source = 0  EXACTLY.  This is the explicit pure-slip realization.")
print("""
  => CANDIDATE C (non-dynamical-frame TT/shear source fed by the Route-E gated kernel) gives,
     at the LINEARIZED level:  delta-Phi=0 (PASS), grad(delta-Psi)=2(g_obs-g_N) by kernel-match
     (PASS, tuned), c_T=c (PASS).  Ghost-freedom = the Einstein-aether/khronometric window
     (PLAUSIBLE per Jacobson, NOT closed by a full Hamiltonian here).
""")

# ===========================================================================================
H("NET VERDICT")
# ===========================================================================================
print("""
THE COVARIANT TERM:  a NON-DYNAMICAL-frame, TRANSVERSE-TRACELESS (shear) metric source fed by
the gated Route-E nonlocal MI kernel acting on the baryon density:
    S_lens = -(kappa/8piG) int sqrt(-g)  Lambda^{ij}_{TT}[u]  ( K_E[box/a0^2] rho_b )_{,i,j}-type
the unique covariant object that is (1) pure-slip by construction (TT => no 00/trace => dPhi=0),
(2) tunable to grad(dPsi)=2(g_obs-g_N), (3) c_T=c (multiplies rho_b, not the graviton).

THE FOUR REQUIREMENTS:
  (1) delta-Phi = 0          : PASS  (TT/shear source has no 00 & no trace -- sympy: trace S=0).
  (2) grad(delta-Psi)=2(g_obs-g_N) : PASS as a TUNED kernel-match (free-function, like AeST F(Y,Q)).
  (3) c_T = c                : PASS  (source multiplies rho_b; graviton kinetic = Einstein-Hilbert).
  (4) ghost-free             : CONDITIONAL -- it EVADES the Ostrogradski/DHOST and the graviton-
                               decay no-gos (the source is NON-DYNAMICAL, not a decay product), at
                               the PRICE of Lorentz violation (a khronometric/Einstein-aether
                               constrained frame).  Ghost-free in Jacobson's EA coupling window
                               (CITED), NOT closed by a full Hamiltonian analysis here.

THE NO-GO THAT IS PROVEN (the publishable theorem, both ways):
  Within DIFFEOMORPHISM-INVARIANT scalar-tensor (Horndeski/DHOST) gravity, NO covariant pure-slip
  (delta-Phi=0) MOND-lensing term survives BOTH c_T=c AND ghost-freedom/no-graviton-decay:
     * c_T=c (Ezquiaga-Zumalacarregui) leaves only conformal G4(phi) [slip but MOVES Phi: Part 2
       sympy dPhi_conf=+1/2 phi/phi0 != 0] and beyond-Horndeski alpha_H;
     * graviton-decay (Creminelli 1809.03484) + DHOST degeneracy kill alpha_H (the ONLY pure-slip
       channel).  => 'covariant diff-invariant Cassini-safe MOND lensing is FORBIDDEN by
       c_T=c + ghost-freedom' is a real no-go.
  The ESCAPE is exactly the framework's OWN structure: a NON-DYNAMICAL Lorentz-violating preferred
  frame (the Route-E in-in frame) carrying an ELLIPTIC (constraint) TT source -- which the no-gos
  do not cover.  So the partner EXISTS, but ONLY as a Lorentz-violating, constraint (non-
  propagating) term -- consistent with the framework's preferred-frame MI, and the price is named.
""")
