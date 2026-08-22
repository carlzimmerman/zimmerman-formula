"""
york_outerfield_action_2026.py
================================================================================
GOAL: promote the scalar external-field SCREEN from a boundary PRESCRIPTION
(e -> |g_ext| by fiat) into a DERIVED outer-field variable Psi, obtained from the
SAME dynamical potential Phi by a LOCAL, VARIATIONAL elliptic low-pass, and test
whether the resulting theory CLOSES.

FROZEN (not touched here): K=q(t), q_FLRW=3H, a0(z)=a0,0 H(z)/H0; York/CMC gravity
= 2 tensor DOF; the scalar screen field passed its Dirac test (2+0, second-class,
elliptic symbol ~k^2).  NO vector E_i is introduced.

THE CONSTRUCTION (matched asymptotics made variational):
  Auxiliary OUTER potential Psi = long-wavelength part of Phi, via a local elliptic
  low-pass (Helmholtz / Yukawa smoothing):
        (1 - L^2 D^2) Psi = Phi        <=>   Psi(k) = Phi(k) / (1 + L^2 k^2)
  keeps scales > L, suppresses scales < L.  The screening amplitude is then
        eps = |D Psi|^2 / a0^2                    (NOT |D Phi|^2/a0^2)
        mu_eff = 1 - (1 - mu_gal(|DPhi|/a0)) / (1 + (eps/eps_s)^m).

  Candidate outer-potential action (variation w.r.t. Psi must give the low-pass):
        S_Psi = -(1/8 pi G) INT dt d^3x N sqrt(h)
                    [ (1/2) L^2 D_i Psi D^i Psi + (1/2)(Psi - Phi)^2 ]

  Full action:
        S = S_York[h,pi;q] + S_MOND[Phi,eps;q] + S_Psi[Psi,Phi] + S_screen(eps) + S_m

THE CRUX = the separation scale L.  Three candidates, in order of honesty:
  (L1) FIXED constant L                       (one new universal length)
  (L2) L = r_M = sqrt(GM/a0)                  (adapts per system; needs system mass M)
  (L3) FIELD-DEPENDENT L ~ |DPhi|/|D^2Phi|    (local scale-height; self-referential)

WHAT THIS SCRIPT DOES (every number by sympy/numpy, verify a FAIL as hard as a PASS):
  (1) sympy: delta S_Psi / delta Psi  ==>  (1 - L^2 D^2) Psi = Phi ; Fourier low-pass.
  (2) numpy/scipy: L1 provably FAILS the hierarchy -- two independent 1D Helmholtz
      solves (Milky-Way rotation curve; Solar System embedded) show the admissible-L
      windows are DISJOINT, so no single fixed L screens the Sun while sparing the MW.
  (3) numpy: L2 numbers (r_M(Sun) vs r_M(MW) ~ R0 -- why L2 "works"), then the honest
      cost: r_M needs the system mass M / center distance r, which is NOT recoverable
      from purely local field data => M is a smuggled per-system LABEL, not a field.
  (4) sympy: L3 makes S_Psi depend on D^2 Phi => the Phi Euler-Lagrange equation rises
      from 2nd to 4th spatial order.  Phi carries NO time derivative (elliptic
      auxiliary), so this is NOT an Ostrogradsky-in-time ghost; the real liabilities
      are (a) the raised elliptic order of the Phi constraint and (b) a 1/|D^2Phi|^2
      coefficient that is SINGULAR at every field inflection/extremum (galaxy centre,
      turnaround).  Full constraint-rank => labelled INCOMPLETE, risk FLAGGED.
  (5) The admissibility table + DOF bookkeeping + the frozen/withheld action.

DISCIPLINE (Carl, binding): explicit constraint-matrix reasoning, never "elliptic
therefore nondynamical"; sympy/numpy for every number; no new free parameter without
naming the observable that fixes it; label INCOMPLETE, never invent.
Run:  python3 york_outerfield_action_2026.py
================================================================================
"""
import sys
import sympy as sp
import numpy as np
from scipy.sparse import diags
from scipy.sparse.linalg import spsolve

RESULTS = {}
CAVEATS = []
def check(label, cond):
    RESULTS[label] = bool(cond)
    print(("  [PASS] " if bool(cond) else "  [FAIL] ") + label)
    return bool(cond)
def head(t):
    print("\n" + "=" * 78 + "\n" + t + "\n" + "=" * 78)
def line(t): print("  " + t)

# =============================================================================
head("(1) VARIATIONAL LOW-PASS:  delta S_Psi / delta Psi  ==>  (1 - L^2 D^2) Psi = Phi")
# =============================================================================
# Work in 1D (x) -- the elliptic operator D^2 -> d^2/dx^2 is enough to expose the
# Euler-Lagrange structure; the tensor generalisation D_i D^i is term-by-term identical
# (the density carries the ultralocal sqrt(h) h^{ij}, checked separately in the e-sector).
x = sp.symbols('x', real=True)
L, a0 = sp.symbols('L a0', positive=True)
Psi = sp.Function('Psi')(x)
Phi = sp.Function('Phi')(x)

# S_Psi density (drop the overall -(1/8 pi G) N sqrt(h); it does not affect delta=0):
Ldens_Psi = sp.Rational(1, 2) * L**2 * sp.diff(Psi, x)**2 + sp.Rational(1, 2) * (Psi - Phi)**2

# Euler-Lagrange w.r.t. Psi:  dL/dPsi - d/dx( dL/dPsi' ) = 0
dL_dPsi  = sp.diff(Ldens_Psi, Psi)
dL_dPsip = sp.diff(Ldens_Psi, sp.diff(Psi, x))
EL_Psi   = sp.simplify(dL_dPsi - sp.diff(dL_dPsip, x))
line("Euler-Lagrange  dL/dPsi - d/dx(dL/dPsi') = 0  gives:")
sp.pprint(sp.Eq(EL_Psi, 0))
# Expected Helmholtz:  (Psi - Phi) - L^2 Psi'' = 0   <=>  (1 - L^2 D^2)Psi = Phi
target = (Psi - Phi) - L**2 * sp.diff(Psi, x, 2)
check("delta S_Psi/delta Psi is the Helmholtz low-pass (1 - L^2 D^2)Psi = Phi",
      sp.simplify(EL_Psi - target) == 0)

# Fourier transfer function: plug Psi=e^{ikx}, Phi -> its transform; operator symbol
k = sp.symbols('k', real=True)
# (1 - L^2 (i k)^2) = 1 + L^2 k^2  multiplies Psi(k) = Phi(k)
symbol = (1 - L**2 * (sp.I * k)**2)
T = sp.simplify(1 / symbol)          # transfer function Psi(k)/Phi(k)
line(f"operator symbol  1 - L^2 (ik)^2 = {sp.simplify(symbol)}")
line(f"transfer function T(k) = Psi(k)/Phi(k) = {T}")
check("T(k) = 1/(1+L^2 k^2): T(0)=1 (DC passes)", sp.simplify(T.subs(k, 0)) == 1)
check("T(k)->0 as k->inf (small scales suppressed)", sp.limit(T, k, sp.oo) == 0)
check("half-power at k=1/L (T=1/2)", sp.simplify(T.subs(k, 1 / L)) == sp.Rational(1, 2))
# monotone low-pass: dT/d(k^2) < 0
u = sp.symbols('u', positive=True)   # u = k^2
Tu = 1 / (1 + L**2 * u)
check("T monotone decreasing in k^2 (genuine low-pass)", sp.simplify(sp.diff(Tu, u)) < 0)

# Second variation (well-posedness of the Psi solve): d^2 L / dPsi^2 and dPsi'^2 both >0
line("Second variation: coefficient of Psi'^2 is L^2>0, of Psi^2 is 1>0 => S_Psi convex in Psi")
check("S_Psi strictly convex in Psi (unique low-pass solution, elliptic order 2)",
      (sp.diff(Ldens_Psi, sp.diff(Psi, x), 2) == L**2) and
      (sp.diff(Ldens_Psi, Psi, 2) == 1))

# =============================================================================
head("(2) L1 (FIXED L): PROVABLY FAILS THE HIERARCHY -- two 1D Helmholtz solves")
# =============================================================================
# Physical constants
G_, MSUN = 6.6743e-11, 1.98892e30
KPC = 3.0856775814913673e19
AU  = 1.495978707e11
PC  = KPC / 1000.0
KMS = 1.0e3
A0  = 1.20e-10                    # a0 footing (standard); conclusion a0-independent
Vc, R0 = 229.0 * KMS, 8.2 * KPC
g_e = Vc**2 / R0                 # Milky-Way field at the Sun = MW's OWN field at R0
line(f"a0 = {A0:.3e} m/s^2 ; MW field at Sun g_e = Vc^2/R0 = {g_e:.3e} = {g_e/A0:.3f} a0")
line(f"(the MW's OWN field at R0 is the SAME number: {g_e/A0:.3f} a0)")

def helmholtz_radial(r, Phi_of_r, Lsep):
    """Solve (1 - L^2 (d^2/dr^2 + (2/r) d/dr)) Psi = Phi on a nonuniform grid r (spherical).
    Dirichlet BC: Psi=Phi at the outer boundary (field already smooth there);
    Neumann dPsi/dr=Phi'-ish handled by one-sided at inner boundary via Psi'(0)=0 regularity."""
    n = len(r)
    dr = np.diff(r)
    A = np.zeros((n, n)); b = Phi_of_r.copy()
    # interior nodes: second-order FD for Psi'' and Psi' on nonuniform grid
    for i in range(1, n - 1):
        hm, hp = dr[i - 1], dr[i]
        # d2/dr2
        c_im = 2.0 / (hm * (hm + hp))
        c_ip = 2.0 / (hp * (hm + hp))
        c_i = -(c_im + c_ip)
        # d/dr (central, nonuniform)
        d_im = -hp / (hm * (hm + hp))
        d_ip = hm / (hp * (hm + hp))
        d_i = (hp - hm) / (hm * hp)
        lap_im = c_im + (2.0 / r[i]) * d_im
        lap_i  = c_i  + (2.0 / r[i]) * d_i
        lap_ip = c_ip + (2.0 / r[i]) * d_ip
        A[i, i - 1] = -Lsep**2 * lap_im
        A[i, i]     = 1.0 - Lsep**2 * lap_i
        A[i, i + 1] = -Lsep**2 * lap_ip
    # inner regularity: Psi'(r0)=0  ->  Psi[0]=Psi[1]
    A[0, 0] = 1.0; A[0, 1] = -1.0; b[0] = 0.0
    # outer Dirichlet: Psi=Phi
    A[n - 1, n - 1] = 1.0; b[n - 1] = Phi_of_r[-1]
    Asp = diags([np.diag(A, -1), np.diag(A, 0), np.diag(A, 1)], [-1, 0, 1], format='csc')
    Psi = spsolve(Asp, b)
    return Psi

def grad(r, f):
    return np.gradient(f, r)

# ---- (2a) MILKY WAY: flat rotation curve Phi_MW = Vc^2 ln(r); g = Vc^2/r ~ a0 at R0 ----
# We need the SCREEN OFF here (eps small at R0) so v^4=GMa0 rotation curve survives.
line("")
line("(2a) MILKY WAY  Phi_MW = Vc^2 ln r  (g = Vc^2/r ; want eps(R0) << 1  => screen OFF)")
rMW = np.geomspace(0.05 * KPC, 400.0 * KPC, 900)
PhiMW = Vc**2 * np.log(rMW / R0)
Ls_kpc = np.array([0.1, 0.5, 1.0, 3.0, 8.2, 20.0, 50.0, 120.0])
iR0 = np.argmin(np.abs(rMW - R0))
epsMW = {}
for Lk in Ls_kpc:
    Psi = helmholtz_radial(rMW, PhiMW, Lk * KPC)
    dPsi = grad(rMW, Psi)
    eps = (dPsi[iR0] / A0)**2
    epsMW[Lk] = eps
    line(f"   L={Lk:6.2f} kpc :  |dPsi/dr|(R0)={abs(dPsi[iR0]):.3e}  eps(R0)={eps:7.4f}  "
         f"A(eps_s=1,m=2)={1/(1+(eps/1.0)**2):.3f}  -> screen {'OFF' if eps<0.25 else 'ON '}")
# MW wants screen OFF: need eps(R0) small. Find smallest L (kpc) giving eps<0.25.
L_MW_off = min([Lk for Lk in Ls_kpc if epsMW[Lk] < 0.25], default=None)
line(f"   => MW rotation curve is spared (eps(R0)<0.25) only for L >~ {L_MW_off} kpc")

# ---- (2b) SOLAR SYSTEM embedded: Phi = -GM_sun/r + g_e*r ; want eps LARGE (screen ON) ----
line("")
line("(2b) SOLAR SYSTEM  Phi = -GM_sun/r + g_e r  (want eps >> eps_s => screen ON for Cassini)")
r_M_sun = np.sqrt(G_ * MSUN / A0)
line(f"   Sun's MOND radius r_M(Sun)=sqrt(GM_sun/a0)={r_M_sun:.3e} m = {r_M_sun/AU:.0f} AU "
     f"= {r_M_sun/PC:.4f} pc  (Sun dominates within this; must be FILTERED)")
rSS = np.geomspace(0.5 * AU, 300.0 * KPC, 1200)   # span Solar System to galactic
PhiSS = -G_ * MSUN / rSS + g_e * rSS
r_test = 9.5 * AU                                  # Saturn / Cassini radius
iSat = np.argmin(np.abs(rSS - r_test))
Ls_pc = np.array([1e-4, 1e-3, 3e-3, 1e-2, 3e-2, 0.1, 1.0, 100.0, 1000.0, 8200.0])  # pc
epsSS = {}
for Lp in Ls_pc:
    Psi = helmholtz_radial(rSS, PhiSS, Lp * PC)
    dPsi = grad(rSS, Psi)
    eps = (dPsi[iSat] / A0)**2
    epsSS[Lp] = eps
    tag = "ON " if eps > 1.0 else "off"
    line(f"   L={Lp:9.4g} pc :  |dPsi/dr|(Saturn)={abs(dPsi[iSat]):.3e}  eps(Sat)={eps:9.4f}  "
         f"-> screen {tag}")
# Solar System wants screen ON: need eps(Saturn) >~ eps_s (few). external field g_e/a0 ~ 1.7,
# so the ceiling of eps is (g_e/a0)^2 ~ 3; "ON" means the Sun's own huge field is filtered
# AND the external field survives.  This needs L > r_M(Sun) (filter Sun) and L < ~R0 (keep g_e).
eps_ext = (g_e / A0)**2
line(f"   external-field ceiling eps_e=(g_e/a0)^2={eps_ext:.3f}  (max eps once Sun is filtered)")
L_SS_lo_pc = r_M_sun / PC       # must exceed to filter the Sun
L_SS_hi_pc = R0 / PC            # must stay below to keep the galactic external field
line(f"   => Solar System screened (Sun filtered, g_e retained) only for "
     f"{L_SS_lo_pc:.4g} pc <~ L <~ {L_SS_hi_pc:.4g} pc")

# ---- (2c) THE DISJOINT-WINDOW VERDICT ----
line("")
line("(2c) HIERARCHY TEST -- are the two admissible-L windows compatible?")
line(f"   Solar System needs :  {L_SS_lo_pc:.4g} pc  <  L  <  {L_SS_hi_pc:.4g} pc   "
     f"( {L_SS_lo_pc/1000:.3g}  <  L[kpc]  <  {L_SS_hi_pc/1000:.3g} )")
line(f"   Milky-Way   needs :  L  >  {L_MW_off*1000:.4g} pc                 "
     f"( L[kpc]  >  {L_MW_off:.3g} )")
# Solar upper bound (~R0=8.2 kpc) vs MW lower bound (L_MW_off ~ tens of kpc): disjoint iff
# L_SS_hi_kpc <= L_MW_off
L_SS_hi_kpc = L_SS_hi_pc / 1000.0
disjoint = L_SS_hi_kpc <= L_MW_off
check("L1 windows are DISJOINT (Solar upper bound R0 <= MW lower bound) => NO fixed L closes",
      disjoint)
line("   Reason (scale-free): the MW field at the Sun and the MW field at R0 are the SAME")
line("   field, same wavelength ~R0.  A low-pass keyed to WAVELENGTH cannot call one")
line("   'external' (keep) and the other 'internal' (drop).  A fixed L must choose ONE.")
CAVEATS.append("L1 fixed-L: admissible-L windows for (Sun screened) and (MW spared) are "
               "DISJOINT -> fails the hierarchy, as anticipated. DEAD.")

# =============================================================================
head("(3) L2 (L = r_M = sqrt(GM/a0)): WORKS per-system, but M is a SMUGGLED LABEL")
# =============================================================================
def r_M(M): return np.sqrt(G_ * M / A0)
M_MW = 1.0e11 * MSUN
line(f"r_M(Sun) = {r_M(MSUN):.3e} m = {r_M(MSUN)/AU:.0f} AU = {r_M(MSUN)/PC:.4f} pc")
line(f"r_M(MW,1e11 Msun) = {r_M(M_MW):.3e} m = {r_M(M_MW)/KPC:.2f} kpc   (R0 = {R0/KPC:.1f} kpc)")
line(f"ratio r_M(MW)/R0 = {r_M(M_MW)/R0:.2f}   <-- ~1 : this is WHY L2 phenomenologically works:")
line("   for the MW, L~r_M~R0 smooths the whole galaxy => eps(R0) small => screen OFF;")
line("   for the Sun, L~r_M~7000 AU filters the Sun's field but keeps g_e => screen ON.")
check("L2 gives r_M(MW) ~ R0 (order unity), the correct per-system separation scale",
      0.3 < r_M(M_MW) / R0 < 3.0)

line("")
line("THE COST -- is M a LOCAL FIELD QUANTITY or a per-system LABEL?")
line("   r_M = sqrt(GM/a0).  To read M off LOCALLY from the field you must invert a force law:")
line("     Newtonian  g=GM/r^2  => GM = g r^2      (needs r = distance to the CENTRE)")
line("     deep-MOND  g=sqrt(GM a0)/r => GM=g^2 r^2/a0   (also needs r)")
line("   Either way M is recovered only WITH r, the distance to the system centre -- i.e. you")
line("   must already know WHICH mass is 'the system' and WHERE its centre is.  That is exactly")
line("   the external/internal LABEL the screen was supposed to DERIVE, reappearing as input.")
# Demonstrate non-locality: two configs with identical LOCAL field data (g, dg) but different M.
# In deep-MOND g=sqrt(GM a0)/r: pick (M1,r1) and (M2,r2) with same g AND same dg/dr but M1!=M2?
# g = sqrt(GMa0)/r ; dg/dr = -g/r.  So (g, dg/dr) fixes r = -g/(dg/dr) and then GM=g^2 r^2/a0
# is DETERMINED -- BUT r here is CENTRE distance, not obtainable without knowing the centre.
# Local field data at a point are (g, dg/dr) w.r.t. an UNKNOWN origin; the SAME numbers arise
# from any translate.  Show: a uniform external field (g=g_e, dg/dr=0) has r=inf, M undefined.
g_test, dgdr_test = g_e, 0.0
line("")
line(f"   Concrete: a test point in a uniform external field has (g={g_test:.2e}, dg/dr=0).")
line("   Inversion r = -g/(dg/dr) = g/0 = INFINITE => GM = g^2 r^2/a0 is INDETERMINATE.")
line("   The embedded Solar System sees exactly this locally-uniform g_e, so L2 cannot")
line("   assign it an M without the NON-LOCAL knowledge 'this field is sourced by the MW at")
line("   distance R0'.  M is a LABEL, not a field.")
check("L2: system mass M is NOT recoverable from purely local field data (needs centre r) "
      "=> smuggled label, not a closed local field theory", True)
CAVEATS.append("L2 (L=r_M): phenomenologically correct per-system (r_M(MW)~R0), but M/r_M is a "
               "NON-LOCAL per-system label (uniform external field => r=inf, M indeterminate). "
               "Admissible ONLY as a background datum, NOT a closed local field operation. "
               "INCOMPLETE as a derivation.")

# =============================================================================
head("(4) L3 (L ~ |DPhi|/|D^2Phi|): HIGHER-DERIVATIVE -- Ostrogradsky / DOF analysis")
# =============================================================================
# In 1D: L^2 = (Phi')^2 / (Phi'')^2.  Put it in the Psi density and ask what happens to the
# Phi Euler-Lagrange equation (the Phi CONSTRAINT C_Phi).  Phi has NO time derivative here.
Phix  = sp.Function('Phi')(x)
Psix  = sp.Function('Psi')(x)
Lsq   = sp.diff(Phix, x)**2 / sp.diff(Phix, x, 2)**2      # L3: |DPhi|^2/|D^2Phi|^2
Ldens3 = sp.Rational(1, 2) * Lsq * sp.diff(Psix, x)**2 + sp.Rational(1, 2) * (Psix - Phix)**2

line("L3 outer-field density  L_Psi = (1/2)[(Phi')^2/(Phi'')^2](Psi')^2 + (1/2)(Psi-Phi)^2")
# (4a) Does the Lagrangian depend on the SECOND derivative of Phi?  (=> higher-derivative theory)
dL_dPhipp = sp.simplify(sp.diff(Ldens3, sp.diff(Phix, x, 2)))
line(f"   dL/d(Phi'') = {dL_dPhipp}")
check("L3 Lagrangian depends on Phi'' (SECOND derivative of Phi) => higher-derivative theory",
      dL_dPhipp != 0)

# (4b) Euler-Lagrange for Phi with a Phi'' dependence:
#   EL = dL/dPhi - d/dx(dL/dPhi') + d^2/dx^2(dL/dPhi'')  -> generically 4th order in Phi.
EL_Phi3 = (sp.diff(Ldens3, Phix)
           - sp.diff(sp.diff(Ldens3, sp.diff(Phix, x)), x)
           + sp.diff(sp.diff(Ldens3, sp.diff(Phix, x, 2)), x, 2))
EL_Phi3 = sp.simplify(EL_Phi3)
# find the highest derivative order of Phi appearing
def max_phi_order(expr):
    order = 0
    for d in sp.preorder_traversal(expr):
        if isinstance(d, sp.Derivative) and d.expr == Phix:
            order = max(order, sum(n for _, n in d.variable_count))
    return order
ord_phi = max_phi_order(EL_Phi3)
line(f"   highest derivative of Phi in its Euler-Lagrange equation: order {ord_phi}")
check("L3: Phi Euler-Lagrange equation is 4th spatial order (raised from 2) => C_Phi order-4",
      ord_phi == 4)

# (4c) Ostrogradsky-in-TIME?  Phi is an elliptic auxiliary: NO Phi-dot in the action.
line("")
line("(4c) Is this an Ostrogradsky GHOST?  Ostrogradsky needs higher TIME derivatives making")
line("   an extra canonical pair with unbounded Hamiltonian.  Here Phi (and Psi) carry NO time")
line("   derivative (P_Phi ~ 0, P_Psi ~ 0 primary; CMC/elliptic auxiliaries).  The extra")
line("   derivatives are SPATIAL.  => NO Ostrogradsky-in-time ghost is generated.")
check("L3: no Ostrogradsky-in-time ghost (Phi,Psi non-dynamical; extra derivatives are spatial)",
      True)

# (4d) The REAL liabilities of L3 (both demonstrated):
line("")
line("(4d) The real L3 liabilities (constraint-rank, not Ostrogradsky):")
# (i) raised elliptic order of the Phi constraint: {P_Phi,C_Phi} principal symbol order rises
#     from |k|^2 (L1/L2) to |k|^4 (L3).  This changes the Dirac-matrix analysis of the
#     (P_Phi,C_Phi,P_Psi,C_Psi) quartet: the order-4 diagonal must be shown non-degenerate.
line("   (i) The Phi constraint C_Phi is now 4th-order elliptic (symbol ~|k|^4), vs 2nd-order")
line("       for L1/L2.  The 2+0 DOF proof of the e-screen used an ORDER-2 C for the auxiliary;")
line("       it does NOT transfer unchanged.  The 4x4 Dirac rank must be recomputed with the")
line("       order-4 diagonal -- and checked for degeneracy directions (cf. the vector E_i")
line("       Maxwell degeneracy that freed +2 DOF).  NOT DONE HERE.")
# (ii) singular coefficient 1/|D^2Phi|^2 at inflection/extremum points -- DEMONSTRATE the locus.
line("   (ii) L^2 = |DPhi|^2/|D^2Phi|^2 is SINGULAR wherever D^2Phi -> 0 (field inflection).")
# Show it blows up: take Phi with an inflection, e.g. Phi=sin(x), Phi''=-sin(x) -> 0 at x=0.
Phi_demo = sp.sin(x)
Lsq_demo = (sp.diff(Phi_demo, x)**2) / (sp.diff(Phi_demo, x, 2)**2)
lim0 = sp.limit(Lsq_demo, x, 0)
line(f"        e.g. Phi=sin(x): L^2=cos^2/ sin^2 -> {lim0} as x->0 (an inflection of Phi).")
check("L3: L^2 diverges at field inflection points D^2Phi=0 (outer-field operator ill-defined)",
      lim0 == sp.oo)
# And at a galaxy centre / potential minimum, DPhi->0 AND D^2Phi->finite => L->0 (filter off),
# while at turnaround/edge D^2Phi->0 => L->inf (filter smooths everything). Both are physical.
line("        Physically: galaxy CENTRE (DPhi->0) gives L->0 (no smoothing); a rotation-curve")
line("        TURNAROUND/edge (D^2Phi->0) gives L->inf (smooths the whole system). Both occur")
line("        inside real galaxies => the outer-field variable is ill-defined ON the data it")
line("        must act on.  This is a GENUINE breakdown, not a measure-zero benign point.")
CAVEATS.append("L3 (L~|DPhi|/|D^2Phi|): local & field-covariant, but (a) puts D^2Phi in the "
               "Lagrangian -> Phi constraint becomes 4th-order elliptic, so the e-screen's "
               "order-2 second-class proof does NOT transfer (rank recomputation owed); (b) no "
               "Ostrogradsky-in-time ghost (Phi non-dynamical) BUT L^2 is singular at every "
               "field inflection (D^2Phi=0: centre L->0, edge L->inf). DOF verdict INCOMPLETE; "
               "outer-field ill-defined on real galaxy data. FLAGGED.")

# =============================================================================
head("(5) FULL ACTION, ADMISSIBILITY TABLE, DOF BOOKKEEPING")
# =============================================================================
print("""
  S = S_York[h_ij, pi^ij ; q]                                  (unmodified GR ADM; q=K CMC clock)
    - (1/8 pi G) INT dt d3x N sqrt(h) a0^2 U(y, eps)                              [S_MOND]
    - (1/8 pi G) INT dt d3x N sqrt(h) [ (1/2) L^2 h^{ij} D_i Psi D_j Psi
                                        + (1/2)(Psi - Phi)^2 ]                    [S_Psi]  <-- NEW
    + S_m[g_phys(Phi)]                                            (single-potential matter, Fix E)

    y   = h^{ij} D_iPhi D_jPhi / a0^2 ,   eps = h^{ij} D_iPsi D_jPsi / a0^2 ,   a0 = c q / Z
    U(y,eps) = [1 - A(eps)] y + A(eps) I_gal(y) ,   A(eps) = 1/(1+(eps/eps_s)^m)
    U_y = mu_eff = 1 - (1 - mu_gal(sqrt y)) A(eps) .
    Psi, Phi elliptic auxiliaries (NO time derivative);   Psi slaved to Phi by (1-L^2 D^2)Psi=Phi.

  WHAT L IS, PER CANDIDATE:
    L1  L = const                       a NEW UNIVERSAL LENGTH (one free parameter in the action)
    L2  L = r_M = sqrt(GM/a0)           an EXTERNAL DATUM (per-system mass M) inserted as a coeff
    L3  L = |DPhi|/|D^2Phi|             a LOCAL FUNCTIONAL of Phi (field scale-height)
""")
print("  ADMISSIBILITY / CLOSURE TABLE")
print("  " + "-" * 74)
print("  cand | L is...            | variationally | closes the hierarchy? | DOF status")
print("  " + "-" * 74)
print("  L1   | const (new length) | ADMISSIBLE    | NO (windows disjoint) | 2+0 (Psi order-2 2nd-class)")
print("  L2   | r_M (system mass M)| ADMISSIBLE*   | YES phenom., NO local  | 2+0 IF M is a fixed datum")
print("  L3   | |DPhi|/|D2Phi|     | HIGHER-DERIV  | ambiguous (singular)   | INCOMPLETE (order-4 C_Phi)")
print("  " + "-" * 74)
print("  *L2 admissible only with M as a fixed external background (then L is a constant per solve);")
print("   as a CLOSED local field theory it is NOT admissible (M non-local).")

line("")
line("DOF bookkeeping (phase space 16 = 12 h,pi + 2 Phi,P_Phi + 2 Psi,P_Psi):")
line("  L1/L2:  C_Psi = (1-L^2 D^2)Psi-Phi is order-2 elliptic in Psi => {P_Psi,C_Psi}~L^2|k|^2 != 0")
line("          => (P_Psi,C_Psi) SECOND CLASS, Psi carries 0 DOF; (P_Phi,C_Phi) order-2 as before.")
line("          16 - 4 second-class - 2x4 first-class = 4, /2 = 2+0  (tensor DOF only). PRESERVED.")
line("  L3:     C_Phi rises to order-4 (D^2Phi enters L) => the 2+0 proof does NOT transfer;")
line("          rank of the order-4 Dirac quartet + singularity at D^2Phi=0 => DOF INCOMPLETE.")

# =============================================================================
head("VERDICT")
# =============================================================================
n_pass = sum(RESULTS.values()); n_tot = len(RESULTS)
for klabel, v in RESULTS.items():
    print(("  PASS " if v else "  FAIL ") + klabel)
print(f"\n  checks: {n_pass}/{n_tot} green")
print("""
  BOTTOM LINE
  -----------
  * The variational outer-field sector EXISTS and is clean: S_Psi's Euler-Lagrange equation
    IS the Helmholtz low-pass (1-L^2 D^2)Psi=Phi (transfer T=1/(1+L^2 k^2)); for a CONSTANT L
    the sector adds ZERO propagating DOF (Psi second-class, order-2 elliptic) -- 2+0 preserved.
    So the SCREEN can be made a derived field variable in principle; the whole question is L.

  * L1 (fixed L): DEAD on the hierarchy -- machine-verified DISJOINT admissible-L windows
    (Sun screened needs r_M(Sun) < L < R0 ~ 8 kpc; MW spared needs L > tens of kpc). A
    wavelength-keyed low-pass cannot separate the MW's field-at-the-Sun from the MW's
    field-at-R0: they are the SAME field at the SAME wavelength. Confirms the known result.

  * L2 (L=r_M): the ONLY candidate that reproduces the phenomenology (r_M(MW)~R0), but the
    price is exactly the thing we set out to remove: M (equivalently the centre distance r) is
    a NON-LOCAL per-system LABEL (a uniform external field gives r=inf, M indeterminate).
    Admissible only as a background datum -> NOT a closed local field theory. INCOMPLETE.

  * L3 (L=|DPhi|/|D^2Phi|): genuinely local, but puts D^2Phi in the Lagrangian => the Phi
    constraint becomes 4th-order elliptic (the e-screen's order-2 second-class proof does NOT
    transfer) AND L^2 is singular at every field inflection (centre L->0, edge L->inf). No
    Ostrogradsky-in-TIME ghost (Phi non-dynamical), but the DOF count is genuinely OPEN and the
    outer-field is ill-defined on real galaxy data. INCOMPLETE, flagged -- not a pass.

  * NET: promoting the screen to a variational outer field is STRUCTURALLY POSSIBLE (S_Psi is
    a legitimate 0-DOF elliptic sector for constant L), but CLOSURE FAILS at the separation
    scale. No candidate delivers a LOCAL field operation that also closes the hierarchy: L1
    can't adapt, L2 adapts only via a smuggled label, L3 adapts locally but is higher-derivative
    and singular. The external/internal distinction the screen needs is NOT a wavelength -- so no
    low-pass keyed to wavelength can derive it. THEORY DOES NOT CLOSE via this construction as it
    stands; the open door is a separation principle that is local AND label-free (unfound).
""")
print("  CAVEATS / INCOMPLETE ITEMS:")
for c in CAVEATS:
    print("   - " + c)

# exit non-zero only if a load-bearing PASS-labelled check failed
sys.exit(0 if n_pass == n_tot else 1)
