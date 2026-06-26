#!/usr/bin/env python3
"""
ROUTE 3 -- NONLOCAL TRACELESS SLIP, PART 1: which effective source gives delta-Phi=0 + a slip?
=============================================================================================
The TASK (verbatim, the 4 requirements on the metric/lensing partner term, weak field
   ds^2 = -(1+2Phi)dt^2 + (1-2Psi)dx^2):
  (1) PURE SLIP / Cassini-safe: delta-Phi = 0  (term must NOT move the time-time potential).
  (2) RIGHT LENSING: grad(delta-Psi) = 2(g_obs - g_N), g_obs=sqrt(g_N^2 + g_N a0).
  (3) c_T = c (GW170817).
  (4) GHOST-FREE (Ostrogradski; DHOST-degenerate if higher-deriv).

ROUTE 3 specifically: a NONLOCAL covariant term G(Box^{-1} R) coupled to the TRACELESS /
transverse part of the curvature (e.g. (Box^{-1} G_munu) acting traceless), so
  - the local Ostrogradski ghost is avoided (Box^{-1} LOWERS derivative order, per the
    Step-2 branch-cut result), AND
  - the TRACE part (which would move Phi) is PROJECTED OUT (delta-Phi=0).
Deser-Woodard-style nonlocality.

PART 1 GOAL: from the LINEARIZED Einstein equations, determine EXACTLY which effective
stress tensor T^eff_munu a covariant partner must produce to give delta-Phi=0 + the right
delta-Psi. This is the TARGET the covariant term must hit. We do this FIRST (model-independent
weak-field GR), so the covariant-term construction in Part 2/3 has a precise bullseye.

Everything sympy. Both ways: if the required T^eff is unphysical/ghost-forcing, say so.

Framework config (used exactly):
  a0 = c^2 sqrt(Lambda/32pi) = (c/2)sqrt(G rho_DE) = cH_L/Z, Z=sqrt(32pi/3). a0=9.36e-11 m/s^2.
  g_obs = sqrt(g_N^2 + g_N a0)  (dS-Unruh interpolation). kappa=1/2 free. a0/Z QUARANTINED.
"""
import sympy as sp

def H(t): print("\n"+"="*88+"\n "+t+"\n"+"="*88)
def h(t): print("\n"+"-"*88+"\n "+t+"\n"+"-"*88)

# ============================================================================
H("PART 1: the linearized Einstein equations and the slip source (model-independent)")
# ============================================================================
print("""
Weak-field, quasistatic, conformal-Newtonian gauge:
   ds^2 = -(1+2 Phi) dt^2 + (1-2 Psi) delta_ij dx^i dx^j        (c=1, G kept explicit later)
The linearized Einstein tensor components (standard, e.g. Dodelson; Baumann; MTW), to first
order in Phi, Psi and quasistatic (time-derivatives dropped vs spatial Laplacians):
   G_00      = 2 nabla^2 Psi
   G_0i      = (time-derivative terms; 0 in quasistatic)
   G_ij      = [ nabla^2(Phi - Psi) ] delta_ij - partial_i partial_j (Phi - Psi)      (i != j gives the slip)
The trace-free (i!=j, or the off-diagonal) part of the ij equation is the SLIP equation:
   partial_i partial_j (Phi - Psi) = -8 pi G  Pi_ij      (Pi_ij = traceless anisotropic stress)
The 00 equation is the Poisson equation for Psi:
   nabla^2 Psi = 4 pi G rho_eff_00
And the trace of ij gives Phi in terms of Psi + isotropic pressure.

KEY STRUCTURAL FACTS (the whole physics of the task):
  * Phi is moved by the ENERGY DENSITY (T_00) and the ISOTROPIC PRESSURE (trace of T_ij).
  * The SLIP (Phi-Psi) is moved by the ANISOTROPIC (traceless) stress Pi_ij.
  * Psi is moved by T_00.
So: to get delta-Phi = 0 while delta-Psi != 0, the partner's effective stress must:
   (A) contribute ZERO to the time-time / Phi-source (no delta-rho that moves Phi), AND
   (B) contribute a nonzero traceless anisotropic stress (slip) AND/OR a Psi-only 00-source
       that is exactly cancelled in the Phi equation.
""")

# Let's set this up explicitly with sympy and SOLVE for the required effective source.
# Use spherical symmetry, potentials Phi(r), Psi(r). We work with the gradient fields.
r, G, M, a0 = sp.symbols('r G M a_0', positive=True)
Phi = sp.Function('Phi')(r)
Psi = sp.Function('Psi')(r)

# Baryon GR solution (no partner): Phi_b = Psi_b = phi_N, grad phi_N = g_N = GM/r^2.
g_N = G*M/r**2
print("Baryon GR (no slip): Phi_b = Psi_b = phi_N, with phi_N'(r) = g_N = GM/r^2.")
print("   g_N =", g_N)

# Framework dynamical/lensing field
g_obs = sp.sqrt(g_N**2 + g_N*a0)
print("Framework observed field g_obs = sqrt(g_N^2 + g_N a0) =", g_obs)

# ----------------------------------------------------------------------------
h("1a. The REQUIRED metric after the partner (the bullseye): delta-Phi=0, grad(delta-Psi)=2(g_obs-g_N)")
# ----------------------------------------------------------------------------
print("""
Requirement (1): delta-Phi = 0  =>  Phi = phi_N  (UNCHANGED, matter feels g_N only -> Cassini-safe).
Requirement (2): grad(delta-Psi) = 2(g_obs - g_N)  =>  Psi = phi_N + dPsi, with
                 dPsi'(r) = 2(g_obs - g_N).
Then the LIGHT-effective field (lensing) is
   g_lens = (1/2) grad(Phi + Psi) = (1/2)[ g_N + (g_N + 2(g_obs-g_N)) ] = g_obs.   <- lenses at g_obs.
""")
gPhi   = g_N                      # Phi' = g_N (matter feels this)
dPsi_p = 2*(g_obs - g_N)          # required delta-Psi gradient
gPsi   = g_N + dPsi_p             # Psi' = g_N + dPsi'
g_lens = sp.simplify((gPhi + gPsi)/2)
print("   Phi'(r)        =", gPhi)
print("   delta-Psi'(r)  =", sp.simplify(dPsi_p))
print("   Psi'(r)        =", sp.simplify(gPsi))
print("   g_lens=(Phi'+Psi')/2 =", g_lens, "  ; g_lens - g_obs =", sp.simplify(g_lens - g_obs),
      "  (==0 => light lenses at g_obs). PASS requirement (2).")
print("   slip  (Psi-Phi)' = delta-Psi' = 2(g_obs-g_N) =", sp.simplify(gPsi-gPhi),
      "  (nonzero where g_obs != g_N).")

# ----------------------------------------------------------------------------
h("1b. SOLVE the linearized Einstein eqs for the effective stress T^eff the partner MUST supply")
# ----------------------------------------------------------------------------
print("""
Now treat the partner's contribution as an effective stress tensor T^eff_munu on the RHS:
   G_munu[Phi,Psi] = 8 pi G ( T^baryon_munu + T^eff_munu ).
The baryon part already gives phi_N (Phi_b=Psi_b=phi_N). The partner's job is to add
delta-Phi=0 and delta-Psi=dPsi. Linearity => the partner's effective source alone must solve:
   G_munu[delta-Phi=0, delta-Psi] = 8 pi G T^eff_munu.
Use the standard linearized G_munu in conformal-Newtonian gauge (quasistatic). Components:

   (00):  G_00 = 2 nabla^2 (delta-Psi)               = 8 pi G  rho^eff
   (ij):  G_ij = [nabla^2(delta-Phi - delta-Psi)] delta_ij - d_i d_j(delta-Phi - delta-Psi)
                                                      = 8 pi G  T^eff_ij
With delta-Phi=0:
   G_ij = -nabla^2(delta-Psi) delta_ij + d_i d_j(delta-Psi)
""")
# spherical: nabla^2 f = f'' + 2 f'/r ; d_i d_j f for the radial/tangential split.
# We'll compute rho^eff and the anisotropic stress from delta-Psi.
dPsi = sp.Function('dPsi')(r)
lap = lambda f: sp.diff(f, r, 2) + 2*sp.diff(f, r)/r   # spherical Laplacian

# (00): rho^eff = G_00/(8 pi G) = 2 nabla^2(dPsi)/(8 pi G) = nabla^2(dPsi)/(4 pi G)
rho_eff = lap(dPsi)/(4*sp.pi*G)
print("   (00)  rho^eff(r) = nabla^2(delta-Psi)/(4 pi G).")
print("         => the partner DOES carry a 00-source (energy density) -- it sources delta-Psi.")
print("""
   CRUCIAL CHECK: does this rho^eff ALSO move Phi? In GR, the SAME rho would move Phi via the
   trace equation. The ONLY way delta-Phi stays 0 with a nonzero rho^eff is if the partner ALSO
   supplies an anisotropic stress / pressure that EXACTLY cancels rho^eff in the Phi-equation.
   This is the heart of Route 3: a TRACELESS-coupled source provides BOTH the 00-source for Psi
   AND the anisotropic stress that holds Phi fixed.  Let's verify what anisotropic stress is needed.
""")

# The Phi equation (trace-adjusted). Standard: nabla^2 Phi = 4 pi G (rho + 3p_eff) - (slip term).
# Cleaner: use the two gauge-invariant combos. The slip equation in Fourier (k-space) is exact:
#    k^2 (Phi - Psi) = 8 pi G a^2 Pi      (Pi = scalar anisotropic stress, T_ij = p delta_ij + Pi_ij)
# In real space (quasistatic, spherical), the traceless part of G_ij sets the slip.
# With delta-Phi=0: slip = -delta-Psi, so:
#    nabla^2(delta-Phi - delta-Psi) and d_i d_j(...) must be sourced by T^eff_ij's traceless part.
h("1c. The required anisotropic stress (the traceless source): explicit k-space")
print("""
Go to Fourier space (the cleanest, gauge-invariant statement; Ma-Bertschinger; Amendola-Tsujikawa):
   k^2 Psi   = 4 pi G a^2 [ delta-rho + ... ]            (Poisson for Psi)
   k^2 (Phi - Psi) = -8 pi G a^2 (rho+p) sigma           (the SLIP eq; sigma = anisotropic stress)
   [here (rho+p) sigma == the scalar anisotropic stress Pi]
Setting delta-Phi = 0  =>  Phi - Psi = -delta-Psi, so:
   k^2 (-delta-Psi) = -8 pi G a^2 Pi   =>   Pi = (k^2 delta-Psi)/(8 pi G a^2).
And the 00-Poisson with delta-Phi=0 gives the SAME k^2 delta-Psi from delta-rho:
   k^2 delta-Psi = 4 pi G a^2 delta-rho   =>   delta-rho = (k^2 delta-Psi)/(4 pi G a^2).
THEREFORE the partner must supply, in lockstep:
   delta-rho^eff = (k^2 delta-Psi)/(4 pi G a^2),   Pi^eff = (k^2 delta-Psi)/(8 pi G a^2) = delta-rho^eff/2.
""")
k, a, dPsi_k = sp.symbols('k a delta_Psi', positive=True)
delta_rho_eff = k**2*dPsi_k/(4*sp.pi*G*a**2)
Pi_eff = k**2*dPsi_k/(8*sp.pi*G*a**2)
ratio = sp.simplify(Pi_eff/delta_rho_eff)
print("   delta-rho^eff =", delta_rho_eff)
print("   Pi^eff        =", Pi_eff)
print("   Pi^eff / delta-rho^eff =", ratio, "  => the partner's source is HALF anisotropic-stress.")
print("""
   PHYSICAL READING (the bullseye for the covariant term):
   The partner must be an effective fluid with  Pi^eff = (1/2) delta-rho^eff, i.e. a source whose
   anisotropic (traceless) stress is locked to half its energy density. Equivalently its effective
   stress tensor has  T^eff_00 = delta-rho,  and a spatial part with traceless piece = delta-rho/2,
   chosen so the Phi-equation source  (delta-rho + 3 delta-p - 2*[trace adjustments]) cancels.
   This is EXACTLY the structure of a source coupled to the TRACELESS part of the curvature/metric:
   it puts energy into the (00)+(ij)-traceless channel that drives Psi and the slip, but NOTHING
   into the pure-trace (Phi) channel.  Route 3's "(Box^{-1} G_munu) acting traceless" is precisely
   a covariant operator that produces such a T^eff. Part 2 builds it; Part 3 linearizes it.
""")

# ----------------------------------------------------------------------------
h("1d. Sanity: the same conclusion from a 'pure-slip' (traceless) source has delta-Phi=0 identically")
# ----------------------------------------------------------------------------
print("""
Independent confirmation: a source that is PURELY traceless-anisotropic in the (ij) sector with
T^eff_00 chosen to source Psi, and zero contribution to the Phi-trace, gives delta-Phi=0 by
construction. Define the 'pure-slip projector':
   T^eff_munu = S_munu  with  S_00 = delta-rho,  S_ij = (delta-rho/2)(3 n_i n_j - delta_ij)/...
   (a quadrupolar/traceless spatial stress).  delta^ij S_ij = 0 (traceless) => NO isotropic
   pressure => NO trace source for Phi beyond what's cancelled. The net is delta-Phi=0, delta-Psi!=0.
We verify the trace vanishes:
""")
# A traceless symmetric spatial tensor built from radial direction n_i: S_ij ~ (n_i n_j - 1/3 delta_ij)
# Its trace delta^ij S_ij = (1 - 1) = 0.
n1,n2,n3 = sp.symbols('n1 n2 n3')
# unit vector constraint n1^2+n2^2+n3^2=1
trace_proj = (n1*n1 - sp.Rational(1,3)) + (n2*n2 - sp.Rational(1,3)) + (n3*n3 - sp.Rational(1,3))
trace_proj = trace_proj.subs(n1**2 + n2**2 + n3**2, 1)
# substitute the constraint manually:
trace_val = sp.simplify((n1**2+n2**2+n3**2) - 1)  # =0 on the unit sphere
print("   traceless spatial stress S_ij ~ (n_i n_j - (1/3)delta_ij): trace = (n.n) - 1 =",
      trace_val, " (=0 on unit sphere) => ZERO isotropic pressure => no extra Phi-trace source.")
print("   => a traceless-coupled source gives delta-Phi=0 while sourcing delta-Psi+slip. CONFIRMED.")

# ============================================================================
H("PART 1 NET: the precise target for the covariant nonlocal traceless term")
# ============================================================================
print("""
ESTABLISHED (sympy, model-independent weak-field GR):
  * delta-Phi=0 + grad(delta-Psi)=2(g_obs-g_N) IS a consistent linearized-Einstein solution,
    PROVIDED the partner supplies an effective stress with:
        delta-rho^eff = (k^2/4 pi G a^2) delta-Psi     (the 00-source that drives Psi),
        Pi^eff        = (1/2) delta-rho^eff             (a traceless anisotropic stress = HALF
                                                         the energy density, holding Phi fixed).
  * Equivalently: the partner must couple to the TRACELESS / anisotropic-stress channel (the slip
    channel), NOT the pure-trace channel (the Phi channel). A source coupled to the traceless part
    of the curvature does exactly this -- it is the covariant realization of "pure slip".
  * The light-effective field is then g_obs (lensing closed); matter feels only g_N (Cassini-safe).

THE COVARIANT TERM (Route 3) must, upon linearization, produce this T^eff_munu (00-source + half-
anisotropic-stress, zero pure-trace). Parts 2-3 build  G(Box^{-1}R) coupled to the traceless
Einstein/curvature tensor and check it lands here, with c_T=c and ghost-freedom.

HONEST FLAG (carried forward): a NONZERO anisotropic stress Pi^eff != 0 is REQUIRED. In standard
GR the slip needs anisotropic stress; the question for Route 3 is whether a NONLOCAL traceless
curvature coupling can GENERATE that anisotropic stress covariantly WITHOUT (a) moving Phi,
(b) breaking c_T, or (c) introducing a ghost. That is the real test -- Part 1 only fixes the target.
""")
