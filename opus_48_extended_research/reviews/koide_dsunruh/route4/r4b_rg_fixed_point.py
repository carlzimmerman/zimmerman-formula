#!/usr/bin/env python3
"""
ROUTE 4 (b) -- RG FIXED POINT in the FLAVOR (Yukawa) sector.

QUESTION: Does the renormalization-group flow of the charged-lepton Yukawa couplings
have a FIXED POINT (UV or IR) at which the sqrt-mass vector sits at 45deg (r=sqrt2,
Q=2/3)? This is genuinely distinct from the dead dS-Unruh IR loop (that was a single-mass
QED-like self-energy; this is the flavor-space flow of the 3 Yukawas together) and from a
static potential (4a).

DEFINITION (2/3-free): the SM/2HDM lepton-Yukawa beta functions. For the charged leptons,
y_e, y_mu, y_tau, the one-loop RGE is
    dy_i/dt = y_i/(16pi^2) * [ a*Tr(stuff) + b*y_i^2 + (gauge) ]
with FLAVOR-DIAGONAL structure -- the leptonic Yukawas are multiplicatively renormalized
(no off-diagonal mixing in the charged-lepton sector at leading order; the only flavor
non-universality is the y_i^2 self term). So:
    d(ln y_i)/dt = (1/16pi^2)[ C(t) + b*y_i^2 ]
with C(t) FLAVOR-UNIVERSAL (top-Yukawa traces, gauge). Key structural fact: the COMMON
piece C(t) RESCALES all y_i by the same factor -> it does NOT move the SHAPE (the ratios
y_i/y_j, hence r). Only the b*y_i^2 term is flavor-dependent. For LEPTONS, y_i^2 ~ 1e-4
(tau) down to 1e-11 (e): utterly negligible. So the lepton sqrt-mass shape r is
RG-INVARIANT to enormous precision -> the RG flow has NO fixed point that MOVES r to sqrt2;
r is frozen at its IR/boundary value, whatever it is. The RGE cannot CREATE the 45deg.

We verify this quantitatively (the shape barely runs), and we check the only place a flow
COULD pin a shape: a strongly-coupled fixed point where y_tau^2 ~ O(1) (a 2HDM/4th-family/
composite scenario). There, does the IR-attractive ratio land at r=sqrt2? We test the
Pendleton-Ross / quasi-fixed-point structure.
"""
import sympy as sp
import mpmath as mp
mp.mp.dps = 40

print("="*80)
print("ROUTE 4(b) -- RG FIXED POINT of the lepton-Yukawa flow at r=sqrt2 ?")
print("="*80)

# ---------------------------------------------------------------------------
# [1] The shape is RG-frozen for leptons: d(ln y_i)/dt has a flavor-universal part that
#     cancels in ratios, and a flavor-dependent y_i^2 part that is ~1e-4..1e-11.
# ---------------------------------------------------------------------------
print("\n[1] Does the lepton-Yukawa shape (the ratios, hence r) run at all?")
# SM lepton Yukawa: y_l = sqrt(2) m_l / v, v=246 GeV.
v_ev = mp.mpf('246.0e9')  # eV
m = {'e': mp.mpf('510998.95'), 'mu': mp.mpf('105658375.5'), 'tau': mp.mpf('1776860000.0')}  # eV
y = {k: mp.sqrt(2)*mv/v_ev for k, mv in m.items()}
print("    SM lepton Yukawas: y_e=%.3e  y_mu=%.3e  y_tau=%.3e" % (y['e'], y['mu'], y['tau']))
print("    flavor-dependent RGE term ~ y_i^2:  y_tau^2=%.3e  y_e^2=%.3e" % (y['tau']**2, y['e']**2))
print("    => the SHAPE-MOVING term is <= 1e-4 (tau); the e,mu shape coords are frozen to")
print("       ~1e-11. The flavor-universal gauge/top part RESCALES all y_i equally and")
print("       CANCELS in the ratios -> r is RG-invariant. The flow CANNOT move r to sqrt2.")

# Quantify shape running over the full SM range t = ln(mu) from M_Z to M_Planck.
# d(ln Q)/dt: Q=p2/p1^2 with p_i^? ... here the 'mass' shape is in sqrt-mass = sqrt(y) up to scale.
# The change in r over 30+ decades of running, driven by the y_i^2 splitting, is computed:
# d ln(y_tau/y_e)/dt = (b/16pi^2)(y_tau^2 - y_e^2). With b ~ 3/2 (2HDM-ish O(1)):
b = mp.mpf('1.5')
drun = b/(16*mp.pi**2)*(y['tau']**2 - y['e']**2)
t_range = mp.log(mp.mpf('1.22e28')/mp.mpf('9.1e10'))  # ln(M_Pl/M_Z) ~ 39
total_shape_run = drun * t_range
print("    ln(y_tau/y_e) RG change over M_Z->M_Planck ~ %.3e (utterly negligible)" % total_shape_run)
print("    => the lepton 45deg, IF present in the IR, is NOT produced by running; it is a")
print("       BOUNDARY condition. The RGE is shape-inert for leptons. NO fixed-point creation.")

# ---------------------------------------------------------------------------
# [2] Strong-coupling quasi-fixed point: the ONLY way an RG flow pins a SHAPE is if a
#     coupling is O(1) and IR-attractive (Pendleton-Ross/Hill). Test: 3 Yukawas with a
#     COMMON flavor-universal driver D(t) and self-terms; the IR-attractive ratio.
#     beta_i = y_i ( -G(t) + y_i^2 )  (schematic: gauge pulls down, self pushes up).
#     Fixed ratio: y_i^2 = G for ALL i with y_i != 0 -> y_i EQUAL -> r=0 (DEMOCRATIC),
#     OR some y_i=0 -> hierarchical, r large. There is NO attractor at a generic 45deg.
# ---------------------------------------------------------------------------
print("\n[2] Strong-coupling quasi-fixed-point (Pendleton-Ross/Hill): where is the shape pinned?")
yt = sp.symbols('y0 y1 y2', positive=True)
G = sp.symbols('G', positive=True)   # flavor-universal driver (gauge/top), >0
# beta_i = y_i(-G + y_i^2); fixed point y_i^2=G (nonzero) or y_i=0.
print("    beta_i = y_i(-G + y_i^2).  Nonzero fixed point: y_i^2=G for every active i.")
print("    => all active Yukawas EQUAL at the FP -> sqrt-mass vector DEMOCRATIC -> r=0.")
print("    A 45deg (r=sqrt2) would need the three y_i pinned at a SPECIFIC non-equal ratio.")
print("    No flavor-universal driver can do that (it pins them equal or to 0). To pin a")
print("    non-trivial ratio you need a FLAVOR-STRUCTURED beta (off-diagonal/texture) -- which")
print("    is exactly an input texture, i.e. you put the answer in. (Same wall as 4a.)")

# ---------------------------------------------------------------------------
# [3] Could a flavor-STRUCTURED fixed point (e.g. an S3-symmetric Yukawaon RGE a la Sumino)
#     land at r=sqrt2 WITHOUT inputting 2/3? Sumino's own construction: the fixed point of
#     his S3 Yukawaon flow is the DEMOCRATIC point (3x3 democratic matrix), eigenvalues
#     (3,0,0)-ish -> Q -> 1 (max breaking) in the symmetric limit, NOT 2/3. Sumino must add
#     an EXPLICIT S3-breaking + a tuned correction to reach the observed masses; the 2/3 is
#     an INPUT (he fits it), not an output of the fixed point. Verify the democratic-matrix
#     eigenvalue Koide value:
# ---------------------------------------------------------------------------
print("\n[3] S3 Yukawaon (Sumino-class) fixed point = DEMOCRATIC matrix. Its Koide value:")
# Democratic 3x3 mass matrix M_dem = c*(all ones). Eigenvalues: (3c,0,0).
Mdem = sp.Matrix([[1,1,1],[1,1,1],[1,1,1]])
eig = Mdem.eigenvals()
print("    democratic matrix eigenvalues:", eig, " = (3,0,0)")
masses = [3,0,0]
sm = sum(masses); ss = sum(sp.sqrt(sp.Integer(x)) for x in masses)
Qdem = sp.nsimplify(sm/ss**2)
print("    Koide Q of (3,0,0): p2/p1^2 with sqrt-masses (sqrt3,0,0):")
sqrt_masses = [sp.sqrt(sp.Integer(x)) for x in masses]
p1d = sum(sqrt_masses); p2d = sum(x**2 for x in sqrt_masses)
Qd = sp.nsimplify(p2d/p1d**2)
print("    Q_dem =", Qd, " (=1, MAXIMAL breaking)  -> r^2 =", sp.nsimplify(6*Qd-2), " (NOT sqrt2)")
print("    => the S3-symmetric (democratic) fixed point gives Q=1, r=2, NOT 2/3/sqrt2.")
print("       The 2/3 must be reached by a TUNED departure from the FP (Sumino fits it).")

print("""
[VERDICT 4b] The RG flow does NOT non-circularly land r=sqrt2:
  - For real leptons the shape is RG-FROZEN (y_i^2 <= 1e-4); running cannot create 45deg.
  - The only shape-pinning fixed point of a flavor-UNIVERSAL flow is the DEMOCRATIC one
    (r=0), or hierarchical (some y=0); neither is r=sqrt2.
  - The S3 Yukawaon (Sumino-class) symmetric fixed point is the DEMOCRATIC matrix -> Q=1,
    r=2 (max breaking), NOT 2/3. Reaching 2/3 requires a TUNED S3-breaking that fits the
    masses = inputs 2/3. No clean RG fixed point at the 45deg shape.
""")
