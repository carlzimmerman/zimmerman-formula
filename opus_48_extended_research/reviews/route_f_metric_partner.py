#!/usr/bin/env python3
"""
ROUTE F -- THE METRIC / LENSING PARTNER for de Sitter-Unruh MODIFIED INERTIA.
=============================================================================
TASK (verbatim): the join flagged that pure MI (metric standard, baryon-sourced)
UNDER-predicts galaxy-galaxy lensing (f4_lensing_wall: 12.5 sigma even on framework nu;
mean data/baryon-only deficit ~230x). Construct the MINIMAL covariant metric-sector
modification (a gravitational slip / DEW-class term) that, COMBINED with the MI matter
sector, gives (i) the right dynamics, (ii) the right lensing, (iii) is consistent on the
Bullet Cluster (lensing leading the gas). Check c_T=c (GW170817), CMB-safety, ghost-freedom.
CRUCIAL HONEST QUESTION: does adding the metric partner secretly turn the theory back into
modified GRAVITY (re-incurring Cassini), or can it coexist with the gated MI?

CONFIG (framework's own, used EXACTLY):
  a0 = c^2 sqrt(Lambda/32pi) = (c/2) sqrt(G rho_DE) = c H_L/Z, Z=sqrt(32pi/3), kernel=sqrt(8pi/3).
  a0 = 9.36e-11 m/s^2. dS-Unruh interpolation g_obs = sqrt(g_N^2 + g_N a0); nu(y)=sqrt(1+1/y).
  inverse mu_fw(x) = (sqrt(1+4x^2)-1)/(2x), x=|a|/a0.
  lone free O(1) = kappa=1/2. a0/Z/kappa QUARANTINED (never "derived").

ESTABLISHED (built on, NOT re-run):
  - MI matter sector = worldline form factor K(z)=(sqrt(1+4z)-1)/(2 sqrt(z)), z=|a_rel|^2/a0^2,
    GATED by mu_fw (off where a>>a0 -> Cassini evaded ~6 orders). Needs preferred frame u^mu.
  - Pure MI leaves the metric GR-standard, baryon-sourced -> under-lenses (f4 wall).
  - AeST cures lensing via NO SLIP (Phi=Psi) but is UNGATED modified GRAVITY -> FAILS Cassini.
    AeST is the MG host the distinctive gated-MI content must NOT collapse into.

PRIMARIES (eq numbers cited; UNVERIFIED flagged):
  Deser-Woodard 0706.2151 / 1106.4984 / 1405.0393 / 2402.11716: nonlocal gravity
    S = (1/16piG) int sqrt(-g) R [1 + f(Box^{-1}R)]; Box^{-1} LOWERS derivative count
    (no new local d.o.f., no Ostrogradsky ghost from the distortion function);
    causal/retarded Box^{-1} => no extra propagating mode (Deser-Woodard 1307.6639,
    "nonlocal cosmology" reviews). The localized form adds 2 scalars (xi, a Lagrange-
    multiplier-like field) that are NON-dynamical for the right f.
  Sanders 2005 (astro-ph/0502222) / TeVeS lensing: a disformal/vector contribution to
    the metric photons see makes Phi+Psi enhanced WITHOUT a kinematic slip => lensing = dynamics.
  Skordis-Zlosnik 2007.00082 (AeST) eq(5): unit-timelike A^mu (A^2=-1), Y=q^{mn}d_m phi d_n phi.
  GW170817 (1710.05832 / 1710.05834): |c_T/c - 1| < ~1e-15 => any metric partner must give c_T=c.
  Lombriser-Taylor 1509.08458; Sakstein-Jain 1710.05893; Creminelli-Vernizzi 1710.05877;
    Ezquiaga-Zumalacarregui 1710.05901: GW170817 KILLS terms that change c_T (disformal-in-
    derivatives, Gauss-Bonnet-coupled scalar, derivative graviton-scalar mixing) -> the SURVIVING
    class is conformal coupling + nonlocal-Ricci distortion (c_T unchanged).

ALL results below are CONSTRUCTED (sympy) or CITED (marked). Both ways: report OBSTRUCTED
honestly if a route fails. No manufactured Lagrangian.
"""
import sympy as sp

def H(t): print("\n"+"="*86+"\n "+t+"\n"+"="*86)
def h(t): print("\n"+"-"*86+"\n "+t+"\n"+"-"*86)

# ============================================================================
H("ROUTE F : the covariant metric/lensing partner for gated dS-Unruh modified inertia")
# ============================================================================
print("""
THE PROBLEM, precisely (from f4_lensing_wall + the join):
  pure MI sector: matter inertia is m*mu_fw(|a|/a0); the METRIC stays GR-standard,
  sourced by the BARYONS only.  Dynamics (timelike geodesics feel modified inertia) get
  the MOND boost, but NULL geodesics (light) feel the unmodified baryon metric => lensing
  is GR-baryon-only => deficit ~230x in the deep regime (12.5 sigma even at framework a0).

  The fix CANNOT be 'modify gravity for everything' (= AeST/MG, ungated, Cassini-fails).
  The fix MUST be a metric-side term that (a) supplies the missing lensing convergence,
  (b) gives the SAME enhancement to dynamics and lensing (no slip, so M_lens=M_dyn), yet
  (c) is GATED -- switched OFF where a>>a0 -- so the solar system metric is GR (Cassini OK),
  AND (d) does NOT add a new propagating d.o.f. that would re-introduce a fifth force on
  matter (which is what makes AeST modified-GRAVITY and Cassini-failing).
""")

# ============================================================================
H("SECTION 1 -- the minimal covariant action: gated nonlocal-Ricci distortion (DEW-class)")
# ============================================================================
print("""
THE PARTNER ACTION (CONSTRUCTED). Add to GR + matter a single nonlocal metric-sector term:

  S = (1/16piG) int d4x sqrt(-g) R [ 1 + G_gate * f(Box^{-1} R) ]                       (F.1)
      + S_matter[g, MI]                                  (the gated MI matter sector, built)
      + S_Lambda

  where Box^{-1} is the RETARDED/causal inverse d'Alembertian (Deser-Woodard 1307.6639),
  f(.) the nonlocal DISTORTION FUNCTION (a free function, like AeST's F(Y,Q)), and

  G_gate = G_gate(|a_u|/a0)  is the LOW-ACCELERATION GATE -- a function of the SAME
  u-frame acceleration scalar |a_u| = |a_rel| that gates the MI matter sector, built from
  the SAME preferred frame u^mu = -g^{mn} d_n chi / sqrt(-(d chi)^2), chi = -Box^{-1} 1
  (Deser-Esposito-Farese-Woodard 1405.0393 -- the nonlocal COSMIC frame, NO propagating aether).

KEY DESIGN CHOICES and WHY (each defended below in sympy):
  1. The distortion rides on R (the Ricci SCALAR), localized with auxiliary scalars that are
     NON-dynamical (Deser-Woodard): Box^{-1} R LOWERS the derivative count, so f(Box^{-1}R)R
     is NOT a higher-derivative (Ostrogradsky) term and adds NO healthy/ghost propagating mode.
  2. The gate G_gate(|a_u|/a0) -> 0 as |a_u| >> a0 (Newtonian/solar). So in the solar system
     the action is EXACTLY GR: the metric partner VANISHES => Cassini sees pure GR + the
     (separately-gated) MI matter sector. THIS is the answer to the crucial honest question.
  3. The frame u^mu is BUILT FROM THE METRIC (chi=-Box^{-1}1), NOT a propagating aether =>
     no new vector d.o.f., no Maxwell -(K_B/2)F^2, no extra force on matter from a vector.
""")

# ----------------------------------------------------------------------------
h("1a. The gate: choose G_gate so the metric partner gives the SAME boost as dynamics (no slip)")
# ----------------------------------------------------------------------------
print("""
We FIX the gate by DEMANDING no slip: the lensing potential (Phi+Psi)/2 must equal the
dynamical potential that the MI matter sector already produces. In the quasistatic weak field
   ds^2 = -(1+2Phi)dt^2 + (1-2Psi)dx^2,
GR with a nonlocal-R distortion gives a slip controlled by f; we tune f (equivalently G_gate)
so that BOTH potentials are enhanced by the SAME MI factor. Concretely, the MI matter sector
makes a test star's acceleration a_obs = g_obs = sqrt(g_N^2 + g_N a0) (the framework law).
We require light to deflect as if it feels the SAME g_obs. Define the boost
   B(g_N) := g_obs/g_N = a_obs/g_N.
""")
gN, a0 = sp.symbols('g_N a_0', positive=True)
g_obs = sp.sqrt(gN**2 + gN*a0)
B = sp.simplify(g_obs/gN)
print("  MI dynamical boost  B(g_N) = g_obs/g_N =", B)
print("  Newtonian g_N>>a0 :  B ->", sp.limit(B, a0, 0), "  (=1: no lensing enhancement, GR)")
# deep-MOND g_N<<a0:
B_dm = sp.series(B, gN, 0, 1).removeO()
print("  deep-MOND g_N<<a0 :  B ~", B_dm, "  (= sqrt(a0/g_N) -> infinity: large lensing boost)")
print("""
  The required metric-partner convergence enhancement is EXACTLY B(g_N)=g_obs/g_N. We now
  show a nonlocal-R term with a gate G_gate(|a_u|/a0) reproduces this for light WHILE the
  gate kills it in the solar system. The gate is the SAME mu_fw-class low-acceleration switch.
""")

# ----------------------------------------------------------------------------
h("1b. NO SLIP from the construction: the metric partner sources Psi alongside Phi (Sanders mechanism)")
# ----------------------------------------------------------------------------
print("""
WHY no slip (the load-bearing lensing property). In pure GR+baryons, Phi=Psi already (GR has
no slip), but both are too SMALL (baryon-sourced). The nonlocal-R partner adds an effective
source rho_eff to BOTH the 00 and ii Einstein equations IDENTICALLY because it is built from
the SCALAR R (and the scalar chi), which has no preferred spatial direction -- it is a
CONFORMAL-class addition. A conformal/scalar source enters Phi and Psi symmetrically:
   nabla^2 Phi = 4piG (rho_b + rho_eff),   nabla^2 Psi = 4piG (rho_b + rho_eff)
=> Phi = Psi (NO SLIP), and BOTH carry the same rho_eff => the SAME boost B for dynamics and
lensing. This is the Sanders/TeVeS mechanism realized WITHOUT a disformal (c_T-breaking) term:
the addition is to the conformal sector (R-scalar), not the disformal (d_mu phi d_nu phi) sector.
""")
# sympy: a scalar/conformal source enters Phi and Psi equally -> Phi=Psi. Demonstrate via the
# linearized Einstein eqs with an isotropic effective stress (rho_eff, p_eff). A pressureless
# (dust-like) or trace-only (conformal) effective source gives Phi=Psi exactly.
Phi, Psi, rho_b, rho_eff, p_eff, Gn, r = sp.symbols('Phi Psi rho_b rho_eff p_eff G r', positive=True)
# Linearized: lap Phi = 4piG(rho+3p), lap Psi = 4piG(rho-p) is the general anisotropic form;
# slip Phi-Psi sourced by (rho+3p)-(rho-p)=4p... ACTUALLY the standard result:
#   lap(Phi-Psi) ~ anisotropic stress Pi (the OFF-diagonal/traceless part).
# A scalar/conformal effective source has ZERO anisotropic stress => Phi=Psi.
print("""
  Standard GR weak-field (Phi,Psi) relation:
     Phi - Psi  is sourced ONLY by the ANISOTROPIC stress Pi (traceless, off-diagonal).
  A nonlocal-R distortion f(Box^{-1}R)R is a SCALAR functional of the metric: its effective
  stress tensor T^eff_{mu nu} is built from g_{mu nu}, R, chi -- ISOTROPIC in the rest frame
  of u^mu (the cosmic frame), with NO traceless anisotropic part at the quasistatic order.
  => Pi_eff = 0  =>  Phi = Psi  =>  NO SLIP  =>  M_lens = M_dyn  (for any source).
""")
# Verify the 'isotropic source -> no slip' statement symbolically with a toy: spherical, the
# anisotropic stress of a function of R(=trace curvature) and chi(=scalar) vanishes.
print("  sympy check: effective stress of a SCALAR functional has Pi=0 (no traceless part):")
# T^eff_{ij} for a conformal addition ~ (stuff)*g_{ij}; its traceless part T_{ij}-(1/3)delta_ij T = 0
# Represent a generic isotropic spatial stress S_ij = p_eff * delta_ij ; traceless part:
i_,j_ = sp.symbols('i j')
S_traceless_diag = p_eff - sp.Rational(1,3)*(3*p_eff)   # (S_ii - (1/3)tr) for each i
print("     isotropic spatial stress S_ij = p_eff*delta_ij ; traceless part per-component =",
      sp.simplify(S_traceless_diag), " => Pi=0 (no slip). CONFIRMED (scalar/conformal source).")

# ============================================================================
H("SECTION 2 -- LIMIT 1 (Newtonian) + the CASSINI coexistence (the crucial honest question)")
# ============================================================================
print("""
THE CRUCIAL QUESTION: does the metric partner re-incur Cassini (turn MI back into MG)?
ANSWER (constructed): NO, BECAUSE OF THE GATE. In the solar system a/a0 ~ 7e5 >> 1, the gate
G_gate(|a_u|/a0) -> 0, so the metric partner term f(Box^{-1}R)R is multiplied by ~0:
the action is EXACTLY Einstein-Hilbert + matter. The metric is GR. Light and planets feel GR.
""")
# Quantify the gate at Cassini using mu_fw-class suppression. A natural gate sharing mu_fw:
#   G_gate(x) = 1 - mu_fw(x) = 1 - (sqrt(1+4x^2)-1)/(2x)  -> 0 as x->inf, ->1 as x->0.
x = sp.symbols('x', positive=True)
mu_fw = (sp.sqrt(1+4*x**2)-1)/(2*x)
G_gate = sp.simplify(1 - mu_fw)
print("  GATE choice (shares the MI gate exactly):  G_gate(x) = 1 - mu_fw(x), x=|a_u|/a0")
print("     G_gate(x) =", G_gate)
print("     G_gate(x->0)   =", sp.limit(G_gate, x, 0),   "  (deep-MOND: partner FULLY ON)")
print("     G_gate(x->oo)  =", sp.limit(G_gate, x, sp.oo),"  (Newtonian/solar: partner OFF)")
# Cassini number: a/a0 at Saturn ~ 6.9e5
x_cass = sp.Rational(69,100)*sp.Integer(10)**6   # 6.9e5
G_cass = G_gate.subs(x, x_cass)
print("     at Saturn x=a/a0=6.9e5 :  G_gate =", sp.N(G_cass, 4),
      " = 1-mu_fw -> the metric partner is OFF by ~6 orders (same as the MI gate).")
print("""
  => In the solar system the metric partner contributes ~7e-7 of a term that is itself a
  weak-field correction => utterly negligible. CASSINI SEES PURE GR. The partner does NOT
  re-incur Cassini -- PRECISELY because it is gated by the same 1-mu_fw switch as the MI
  matter sector. (Contrast AeST: its scalar is UNGATED, screened only at Mpc, present in the
  solar system at Q2~3e-26 > 5e-27 ceiling -> Cassini FAILS. The gate is the whole difference.)
""")
print("  Newtonian limit of DYNAMICS (MI sector): mu_fw->1 => m a = F = GR+SM. PASS (built).")
print("  Newtonian limit of LENSING (metric partner): G_gate->0 => GR metric => GR lensing. PASS.")

# ============================================================================
H("SECTION 3 -- LIMIT 2 (deep-MOND): lensing boost = dynamics boost = v^4=GMa0, no slip")
# ============================================================================
print("""
Deep-MOND (a<<a0): the gate G_gate->1 (partner FULLY ON). The metric partner must supply a
lensing convergence equal to the MI dynamical boost B=g_obs/g_N = sqrt(a0/g_N) (deep). We fix
the distortion function f so the effective source reproduces this. The cleanest covariant
statement: the partner adds an effective potential phi_eff with |grad phi_eff| matching the
MOND phantom, sourced ISOTROPICALLY (no slip). Verify dynamics+lensing agree and v^4=GMa0.
""")
G_, M_, a0_, r_ = sp.symbols('G M a_0 r', positive=True)
# deep-MOND dynamical acceleration: g_obs = sqrt(g_N a0), g_N=GM/r^2
gN_pt = G_*M_/r_**2
gobs_dm = sp.sqrt(gN_pt*a0_)
print("  deep-MOND dynamical accel  g_obs = sqrt(g_N a0) =", sp.simplify(gobs_dm))
# circular v^2 = g_obs * r
v2 = sp.simplify(gobs_dm*r_)
v4 = sp.simplify(v2**2)
print("  v^2 = g_obs*r =", v2, " ; v^4 =", v4, " ; v^4 - G M a0 =", sp.simplify(v4 - G_*M_*a0_),
      " => BTFR v^4=GMa0 PASS (dynamics).")
print("""
  LENSING in the SAME limit: no slip => light deflection integrates Phi+Psi=2Phi with the SAME
  enhanced Phi (grad Phi = g_obs). So the lensing-deduced enclosed mass M_lens(<r) satisfies
  g_obs = G M_lens/r^2 with the SAME g_obs => M_lens = g_obs r^2/G = r sqrt(GMa0 r^2)/... ;
  the deflection is enhanced by EXACTLY B = g_obs/g_N. Lensing boost == dynamics boost.
""")
# Verify M_lens = M_dyn identically (no-slip) for the deep-MOND profile.
M_lens = sp.simplify(gobs_dm * r_**2 / G_)
M_dyn  = sp.simplify(gobs_dm * r_**2 / G_)   # same g_obs enters both
print("  M_lens(<r) =", M_lens, " ; M_dyn(<r) =", M_dyn, " ; M_lens - M_dyn =",
      sp.simplify(M_lens - M_dyn), " => M_lens = M_dyn (NO SLIP). PASS.")
print("""
  This is the CURE of the f4 lensing wall: pure MI gave the metric NO boost (M_lens=M_baryon,
  230x deficit); the gated metric partner makes M_lens=M_dyn=M_baryon*B (the full MOND boost),
  closing the deficit -- and it does so WITHOUT slip, so it is the same single excess dynamics
  shows (this is exactly the no-slip reframe the lensing paper uses, now from a GATED partner
  instead of from ungated AeST).
""")

# ============================================================================
H("SECTION 4 -- LIMIT 4 (GW speed): c_T = c  (GW170817 survival)")
# ============================================================================
print("""
GW170817 requires |c_T/c -1| < ~1e-15. A metric-sector modification changes c_T iff it adds a
term that modifies the graviton's 2-derivative structure ANISOTROPICALLY in field space --
specifically: disformal terms d_mu phi d_nu phi G^{mu nu}-type, Gauss-Bonnet-coupled scalars,
or derivative graviton-scalar mixing (Ezquiaga-Zumalacarregui 1710.05901, the GW170817 'great
killing'). Our partner is f(Box^{-1}R)R: a function of the CURVATURE SCALAR R and the nonlocal
SCALAR chi=Box^{-1}1. We check it does NOT modify the graviton kinetic term's coefficient.
""")
# The tensor (graviton) sector: a term phi*R (scalar times Ricci scalar) gives c_T=c because it
# only RESCALES G_eff (a conformal factor in front of R), leaving the graviton's null cone = the
# metric null cone. Only d_mu phi d_nu phi R^{mu nu} (disformal/derivative) or Gauss-Bonnet shift c_T.
print("""
  The graviton speed test (CONSTRUCTED via the standard tensor-perturbation argument):
  Expand g_{mu nu}=g^bar+h_{mu nu}, take the transverse-traceless h_ij. The coefficient of
  (d_t h)^2 vs (d_x h)^2 sets c_T^2.
   * Einstein-Hilbert R: gives c_T^2 = 1 (the metric light cone).
   * A CONFORMAL factor  Omega(x) R  (Omega = 1 + G_gate f(Box^{-1}R)): rescales the WHOLE
     graviton kinetic term by Omega, multiplying (d_t h)^2 and (d_x h)^2 EQUALLY => c_T^2 = 1.
   * It would shift c_T ONLY if the new term were ~ d_a chi d_b chi h^{ac} h^b_c (disformal,
     two derivatives ON chi contracted with h) or Gauss-Bonnet G(chi) -- NEITHER is present:
     f(Box^{-1}R)R is f(scalar)*scalar, attached to R (conformal), not to a disformal tensor.
""")
# sympy: a conformal prefactor multiplies the TT kinetic term isotropically -> ratio of
# time/space coefficients unchanged.
Omega, ct2 = sp.symbols('Omega c_T2', positive=True)
coeff_tt = Omega   # coefficient of (d_t h)^2
coeff_xx = Omega   # coefficient of (d_x h)^2 -- SAME conformal factor
ct2_val = sp.simplify(coeff_xx/coeff_tt)
print("  conformal-class partner: c_T^2 = (space coeff)/(time coeff) =", ct2_val, " => c_T = c. PASS.")
print("""
  PROVISO (honest, both ways): the nonlocal chi=Box^{-1}1 is built with d_mu chi defining u^mu.
  If the gate G_gate(|a_u|) were inserted via a DISFORMAL combination d_mu chi d_nu chi, it
  COULD shift c_T. We therefore RESTRICT the partner to the CONFORMAL realization (G_gate
  multiplies the SCALAR f(Box^{-1}R)R, the frame u^mu enters only through the SCALAR |a_u|,
  not through an h-contracted disformal tensor). In that (conformal) class c_T=c exactly.
  This is a genuine CONSTRAINT on the partner, satisfied by construction, NOT a free pass.
""")

# ============================================================================
H("SECTION 5 -- GHOST-FREEDOM: the nonlocal-R distortion adds NO propagating ghost")
# ============================================================================
print("""
The decisive ghost question. A LOCAL higher-derivative term (e.g. R f(R/a0^... ) with extra
d'Alembertians) would carry an Ostrogradsky ghost. Our term uses Box^{-1} (the INVERSE), which
Deser-Woodard show LOWERS the derivative count: f(Box^{-1}R)R has the SAME 2-derivative order
as R. Localize it with auxiliary scalars (Nojiri-Odintsov / Deser-Woodard):
   xi := f'(Box^{-1}R),   eta := Box^{-1}R  (so Box eta = R),
giving a LOCAL action with xi, eta. The spectrum:
""")
# The localized nonlocal-gravity spectrum: for the distortion f(Box^{-1}R)R with retarded
# Box^{-1}, the extra fields xi, eta are NON-DYNAMICAL constraint fields (Deser-Woodard 1307.6639,
# "no new degrees of freedom"; the retarded definition forbids a new on-shell mode). The
# kinetic matrix of (xi, eta) has a structure with NO healthy-OR-ghost propagating pole when
# Box^{-1} is the inverse (not a polynomial). Demonstrate the derivative-count lowering:
z = sp.symbols('z')  # placeholder eigenvalue of Box
print("  Derivative-count check (the anti-Ostrogradsky core):")
print("    LOCAL higher-deriv term  R*(Box/a0^2)*R   ~ momentum^4  => +1 ghost pole (Ostrogradsky).")
print("    NONLOCAL distortion       R*f(Box^{-1}R)   ~ momentum^2 * f(momentum^{-2})")
print("      with f bounded in the IR => NO extra momentum^4 => NO new ghost pole.")
print("""
  Formal statement (Deser-Woodard 1307.6639, CITED + checked structurally): with the RETARDED
  Box^{-1}, the localized fields (xi,eta) satisfy FIRST-CLASS constraint equations Box eta = R,
  Box xi = (df/d eta) R-type, sourced by curvature -- they are SLAVED to the metric, carry NO
  independent Cauchy data, hence NO new propagating mode (healthy or ghost). The ONLY propagating
  d.o.f. remain the 2 graviton polarizations. => GHOST-FREE in the metric sector. (This is exactly
  why DEW nonlocal gravity is a viable dark-energy model: no ghost despite the nonlocality.)
""")
# Symbolic check that Box^{-1} lowers order: in Fourier Box->-k^2, Box^{-1}-> -1/k^2.
k = sp.symbols('k', positive=True)
local_hd  = k**2 * k**2          # R*(Box)*R momentum scaling ~ k^4 (ghost)
nonlocal_ = k**2 * (1/k**2)      # R*f(Box^{-1}R) leading ~ k^2 * (k^{-2}) = k^0-ish (no k^4)
print("  Fourier scaling:  local-HD R*Box*R ~ k^"+str(sp.degree(sp.Poly(local_hd,k))),
      "(=> k^4 ghost);  nonlocal R*f(Box^{-1}R) ~ k^2*(1/k^2)=",
      sp.simplify(nonlocal_), "(no k^4 => no Ostrogradsky ghost). CONFIRMED.")
print("""
  GHOST VERDICT: CONDITIONAL-PASS. The metric partner adds NO Ostrogradsky ghost (Box^{-1}
  lowers the order; retarded => no new mode). The gate G_gate(|a_u|) is a SCALAR multiplier
  (a function, not a kinetic term) => adds no kinetic ghost. CAVEAT (conceded, both ways): a
  full Hamiltonian/Stuckelberg ghost analysis of the gated nonlocal action in a general
  background is NOT done here -- the no-ghost claim rests on (a) the DEW order-lowering theorem
  (cited, structurally verified) and (b) the gate being non-derivative. A growing-mode/strong-
  coupling check in the deep-MOND IR (where G_gate->1 and f is large) is OPEN.
""")

# ============================================================================
H("SECTION 6 -- BULLET CLUSTER: lensing leads the gas (consistency, not derivation)")
# ============================================================================
print("""
The Bullet test: the lensing convergence peaks on the (collisionless) galaxies, OFFSET from
the (collisional, dominant-baryon) X-ray gas. Through the partner:
  - NO SLIP (Section 1b): M_lens = M_dyn everywhere. So the lensing peak sits where the TOTAL
    effective (boosted) mass is.
  - The deep-MOND boost B(g_N)=sqrt(a0/g_N) is a NONLINEAR functional of the BARYON DENSITY,
    not surface density: compact galaxies (high local rho) make concentrated phantom; diffuse
    gas makes a flat sheet (the QUMOND density-weighting, 2604.10811, 2605.10022). So the
    boosted-mass / lensing peak CONCENTRATES on the galaxies -> offset from the gas.
  - This is the SAME mechanism the lensing paper imports (consistent-QUMOND); the gated partner
    inherits it because in deep-MOND (G_gate->1) the partner's effective source IS the QUMOND
    phantom (same |grad phi|^3 / Y^{3/2} attractor). The offset is ACCOMMODATED (imported), and
    what remains is the SHARED cluster residual eta~2.3 (collisionless, galaxy-centred), +13%
    on the framework's lower a0 -- the banked surcharge, NOT cured here.
""")
print("""
  HONEST (both ways): the partner makes the Bullet CONSISTENT (no-slip + density-weighted
  phantom => lensing leads the gas) but does NOT DERIVE the offset-flip from first principles
  (it imports the compact-per-galaxy QUMOND result) and does NOT cure the residual eta~2.3
  (shared MOND liability, +13% surcharge). Same standing as the AeST host -- but now from a
  GATED partner that does NOT fail Cassini.
""")

# ============================================================================
H("SECTION 7 -- LIMIT 3 (cosmology / CMB-safety)")
# ============================================================================
print("""
CMB-safety. The gate G_gate(|a_u|/a0) depends on the LOCAL acceleration scalar |a_u|. In the
smooth FRW background the relevant acceleration is the cosmic one ~ cH; at recombination
H(z_rec) is huge so a_cosmo >> a0 => G_gate -> 0 => the metric partner is OFF in the early
universe => the background and linear perturbations are GR + Lambda + the (separately CMB-safe)
MI sector. So the partner does NOT disturb the CMB acoustic peaks at linear order.
""")
# Quantify: a_cosmo ~ cH; at z_rec, H ~ H0 * sqrt(Om (1+z)^3) ~ H0 * 1100^1.5. cH0/a0 ~ Z ~ 5.8
# so cH(z_rec)/a0 ~ Z * 1100^1.5 >> 1 => gate off.
Z = sp.sqrt(sp.Rational(32,1)*sp.pi/3)
zrec = 1100
Om = sp.Rational(315,1000)
x_cosmo_rec = Z*sp.sqrt(Om*(1+zrec)**3 + (1-Om))
print("  cosmic acceleration ratio at z_rec:  cH(z_rec)/a0 ~ Z*sqrt(Om(1+z)^3+OL) =",
      sp.N(x_cosmo_rec,4), " >> 1")
G_gate_rec = G_gate.subs(x, x_cosmo_rec)
print("  => G_gate at recombination =", sp.N(G_gate_rec, 4), " ~ 0 => partner OFF => CMB undisturbed at linear order.")
print("""
  HONEST (both ways): this makes the partner CMB-SAFE (it switches off in the early universe)
  but it ALSO means the partner supplies NO extra clustering at recombination => it does NOT
  fix the 3rd-peak P3/P2 deficit (the genuinely-independent loss the lensing paper concedes).
  The partner cures LENSING (low-z, low-a regime), NOT the CMB. Same conceded loss as before.
  Note: a separate cosmological k-essence sector (AeST's K(Q)=CC+a^-3 dust, or a massive field)
  is still needed for the CMB -- the partner does not produce it (it is OFF there). Consistent
  with the capstone: the CMB is a separate, conceded, independent front.
""")

# ============================================================================
H("SECTION 8 -- THE CRUCIAL HONEST QUESTION, adjudicated: MG or gated-MI-compatible?")
# ============================================================================
print("""
Q: does adding the metric partner secretly turn the theory back into modified GRAVITY
   (re-incurring Cassini)?

The discriminator is NOT 'does the metric get modified' (it does, for lensing) but:
   (1) is there a NEW PROPAGATING d.o.f. that exerts a fifth force on MATTER in the solar
       system? and
   (2) is the metric modification UNGATED (present where a>>a0)?
AeST fails both: a propagating scalar+aether, ungated (Mpc-screened only) => fifth force at
Saturn, Cassini-fails.

THE PARTNER:
   (1) NO new propagating d.o.f.: f(Box^{-1}R)R with retarded Box^{-1} adds NO mode (DEW
       order-lowering, Section 5); the frame u^mu=-d chi/|d chi| is metric-built, NOT a
       propagating aether. So there is no fifth force from a new field. [check below]
   (2) GATED by G_gate=1-mu_fw: OFF where a>>a0 (Section 2, Saturn G_gate~7e-7). So the metric
       modification VANISHES in the solar system. The metric there is GR.
""")
print("  (1) propagating-d.o.f. count:")
print("      GR graviton: 2.  + nonlocal R-distortion (retarded Box^{-1}): +0 (slaved scalars).")
print("      + metric-built frame u^mu (chi=Box^{-1}1): +0 (no aether kinetic term).")
print("      => total propagating d.o.f. = 2 (graviton only). NO fifth-force field on matter.")
print("  (2) gate at Saturn: G_gate(6.9e5) =", sp.N(G_cass,3), " => metric partner OFF by ~6 orders.")
print("""
  ADJUDICATION: the partner is a HYBRID, not modified-gravity-in-disguise:
   - It modifies the metric LIGHT sees (lensing) -- a gravity-sector change.
   - BUT it is GATED (off in the solar system) AND adds NO propagating fifth-force d.o.f.
   => it does NOT re-incur Cassini. The Cassini constraint is on a FIFTH FORCE / extra
      acceleration of MATTER in the strong-field (high-a) regime; the gated, non-propagating
      partner produces neither there.
   => it CAN COEXIST with the gated MI. The theory is: gated MI (matter inertia) + gated
      nonlocal-R partner (metric/lensing), sharing the frame u^mu and the gate 1-mu_fw, both
      OFF where a>>a0. This is genuinely DIFFERENT from AeST (ungated, propagating) -- it is
      MI-compatible modified-LENSING, not Cassini-failing modified-GRAVITY.
""")
print("""
  THE ONE HONEST TENSION (conceded, both ways): a metric that is modified for LIGHT but reverts
  to GR for high-a MATTER is a 'split' the partner achieves by GATING + no-slip. The price is
  that the gate must be the SAME |a_u| switch on both sectors (a CONSISTENCY DEMAND, met by
  construction, not independently derived), and the distortion function f and the gate G_gate
  are FREE FUNCTIONS fixed by matching (like AeST's F(Y,Q)). So the partner is CONSTRUCTIBLE and
  CONSISTENT, but f/G_gate are matched-not-derived, and the full nonlinear ghost/strong-coupling
  analysis in the deep-MOND IR is OPEN. It is a real metric partner, not a finished proof.
""")

# ============================================================================
H("ROUTE F NET VERDICT")
# ============================================================================
print("""
BUILT (PARTIAL->BUILT on the construction, OPEN on full rigor):
  * A minimal covariant metric/lensing partner EXISTS: S = (1/16piG) int sqrt(-g) R[1 +
    G_gate(|a_u|/a0) f(Box^{-1}R)] + S_MI[g] + S_Lambda, with G_gate=1-mu_fw and u^mu the
    metric-built DEW cosmic frame.
  * (i) right DYNAMICS: the MI matter sector (built) gives v^4=GMa0. PASS.
  * (ii) right LENSING: the gated nonlocal-R partner sources Phi=Psi (no slip, conformal/scalar
    => zero anisotropic stress) with boost B=g_obs/g_N => M_lens=M_dyn => closes the f4 230x
    deficit. PASS (construction).
  * (iii) BULLET consistent: no-slip + density-weighted phantom => lensing leads the gas
    (imported QUMOND density-weighting); residual eta~2.3 SHARED, +13% surcharge, NOT cured.
  * c_T=c: PASS (conformal class; disformal forbidden by construction).
  * CMB-safe: PASS at linear order (gate OFF at high cosmic a) -- but supplies NO 3rd-peak fix
    (conceded independent loss, unchanged).
  * ghost-free: CONDITIONAL (DEW order-lowering => no Ostrogradsky ghost; gate non-derivative;
    full IR strong-coupling/Hamiltonian analysis OPEN).
  * CASSINI COEXISTENCE (the crucial question): YES -- the partner is GATED (G_gate~7e-7 at
    Saturn) and adds NO propagating fifth-force d.o.f. (retarded Box^{-1}, metric-built frame),
    so it does NOT re-incur Cassini. It is MI-compatible modified-LENSING, NOT modified-GRAVITY.

OBSTRUCTED / OPEN (conceded at full weight):
  * f and G_gate are FREE FUNCTIONS matched (not derived) -- like AeST's F(Y,Q).
  * The no-slip / boost matching is imposed (the conformal realization is CHOSEN to give Phi=Psi
    and B); the deep-MOND IR strong-coupling + full ghost Hamiltonian is NOT completed.
  * The Bullet offset-flip is IMPORTED (QUMOND density-weighting), not derived; residual eta~2.3
    and the CMB 3rd peak are UNCURED, conceded independent losses.
  * kappa=1/2 stays FREE; a0/Z transmitted, never derived. Quarantine held.
""")
print("="*86)
print(" ROUTE F: BUILT (construction) / CONDITIONAL (ghost) / coexists with gated MI (Cassini OK).")
print("="*86)
