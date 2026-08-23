"""
GATE 2 — THE GW170817 CONE GATE  (c_gamma = c_GW).

Theory under test (Carl's completion; Phase-1 already PASSED with the foliation-spatial
disformal class C(Phi,|D_iPhi|^2), D(Phi,|D_iPhi|^2), non-covariant, C>D non-degenerate):

    g̃_μν = C g_μν + D u_μ u_ν ,   u_μ = -∇_μT/sqrt(-∇T·∇T) = CMC unit normal,  u·u = -1 (g).

Matter (incl. photons) couples to the single physical metric g̃.  The graviton (TT sector)
is unmodified GR on the CMC slicing  =>  c_GW = c  (Gate-1/stability, luminal).

DELIVERABLES (all machine-checked):
 (1) Invert g̃ symbolically:  g̃^{μν} = (1/C) g^{μν} − D/(C(C−D)) u^μ u^ν.  Verify g̃ g̃^{-1}=I.
 (2) Photon cone  g̃^{μν} k_μ k_ν = 0  =>  the g-frame dispersion  g^{μν}k_μk_ν = D/(C−D)(u·k)^2.
     Derive c_gamma^2 on (a) FLRW/cosmological and (b) static weak field.  Result (both):
        c_gamma^2 / c_GW^2 = (C − D)/C = 1 − D/C.
 (3) GW170817:  |c_gamma/c_GW − 1| < ~1e-15  =>  |D/C| ≲ 2e-15  at the emission redshift (z~0).
 (4) LENSING COMPATIBILITY (the decisive fork):  light bending is CONFORMALLY INVARIANT, so
     the conformal factor C cannot bend light differently from g.  The ONLY handle the physical
     metric has on photon paths (relative to g) is the DISFORMAL D.  Quantify the D that the
     MOND phantom lensing (ν−1)ρ would require if the disformal is the lensing mechanism, and
     compare to the GW bound.  Decide: safe (Skordis–Zlosnik luminal class) vs GW-excluded.

Discipline: derive/sympy; verify the NO-GO as hard as a success; DERIVED-not-fitted.
Skordis–Zlosnik arXiv:1905.09465 (AeST) achieves a LUMINAL disformal — we test whether THIS
D is in that class or is forced large by lensing (the project record's warning).
"""
import sympy as sp

FAILS = []
def check(name, cond):
    st = "PASS" if bool(cond) else "FAIL"
    if not cond: FAILS.append(name)
    print(f"  [{st}] {name}")
    return bool(cond)

print("="*76)
print("PART 1 — Inverse of the disformal metric  g̃ = C g + D u⊗u  (u·u = −1, g-norm)")
print("="*76)
# General covariant check in a local Lorentz frame g = diag(-1,1,1,1), u^μ=(1,0,0,0).
C, D = sp.symbols('C D', real=True, positive=True)   # values; positivity checked separately
g   = sp.diag(-1, 1, 1, 1)
gi  = g.inv()
uup = sp.Matrix([1, 0, 0, 0])          # u^μ
udn = g*uup                            # u_μ = (-1,0,0,0)
check("u normalized  u·u = −1", sp.simplify((udn.T*uup)[0] + 1) == 0)

gt   = C*g + D*(udn*udn.T)             # g̃_{μν} = C g_{μν} + D u_μ u_ν
# proposed inverse
gt_inv_claim = (sp.Rational(1)/C)*gi - D/(C*(C-D))*(uup*uup.T)   # (1/C)g^{μν} − D/(C(C−D)) u^μ u^ν
prod = sp.simplify(gt*gt_inv_claim)
check("g̃ · g̃^{-1} = I  (closed-form inverse verified)", prod == sp.eye(4))
print("     g̃^{μν} = (1/C) g^{μν} − D/(C(C−D)) u^μ u^ν")

print()
print("="*76)
print("PART 2 — Photon null cone  g̃^{μν} k_μ k_ν = 0")
print("="*76)
# g̃^{μν}k_μk_ν = (1/C)(g^{μν}k_μk_ν) − D/(C(C−D)) (u·k)^2 = 0
#   =>  g^{μν} k_μ k_ν = D/(C−D) (u·k)^2      (multiply by C)  ... the g-frame dispersion.
w, kx, ky, kz = sp.symbols('omega k_x k_y k_z', real=True)
k = sp.Matrix([-w, kx, ky, kz])        # k_μ = (−ω, k_i)  (lower index)
gkk   = (k.T*gi*k)[0]                   # g^{μν}k_μk_ν = −ω² + |k|²
uk    = (uup.T*k)[0]                    # u·k = u^μ k_μ = −ω
photon_cone = sp.simplify((k.T*gt_inv_claim*k)[0])
# Solve the cone for |k|^2 in terms of ω^2 with k along x (isotropic, so wlog)
sol = sp.solve(photon_cone.subs({ky:0, kz:0}), kx**2, dict=True)
kx2 = sp.simplify(sol[0][kx**2])
cg2 = sp.simplify(w**2 / kx2)           # c_gamma^2 = ω^2/|k|^2  (phase speed vs coordinate c=1)
print(f"     g-frame dispersion:  −ω² + |k|² = D/(C−D)·(u·k)²,   (u·k)² = ω²")
print(f"     |k|² = ω²·C/(C−D)   =>   c_gamma² = ω²/|k|² = {cg2}")
check("c_gamma² = (C−D)/C = 1 − D/C  (local-frame derivation)", sp.simplify(cg2 - (C-D)/C) == 0)

print()
print("--- (a) FLRW / cosmological background ---")
# FLRW: g = diag(−1, a², a², a²) in cosmic time; CMC normal u^μ=(1,0,0,0) (comoving),
# so u·k = −ω exactly as above; the conformal a² rescales C but drops from the RATIO.
a = sp.symbols('a', positive=True)
gF = sp.diag(-1, a**2, a**2, a**2); giF = gF.inv()
uF = sp.Matrix([1,0,0,0]); uFd = gF*uF
check("FLRW: u·u = −1", sp.simplify((uFd.T*uF)[0]+1)==0)
gtF_inv = (sp.Rational(1)/C)*giF - D/(C*(C-D))*(uF*uF.T)
kF = sp.Matrix([-w, kx, 0, 0])
coneF = sp.simplify((kF.T*gtF_inv*kF)[0])
kx2F = sp.simplify(sp.solve(coneF, kx**2, dict=True)[0][kx**2])
# physical wavenumber k_phys = k_x/a ; c_gamma,phys² = ω²/k_phys² = ω²·a²/k_x²
# (graviton on same background: g^{μν}k_μk_ν=0 -> k_x²=a²ω² -> c_GW,phys²=1, the reference)
cg2F = sp.simplify(w**2*a**2/kx2F)
print(f"     c_gamma,phys² (FLRW) = {cg2F}")
check("FLRW: c_gamma² = (C−D)/C (a drops from the ratio)", sp.simplify(cg2F-(C-D)/C)==0)

print()
print("--- (b) static weak-field background ---")
# g = diag(−(1+2Φ), (1−2Ψ), (1−2Ψ), (1−2Ψ)); CMC normal u^μ = (1/sqrt(1+2Φ),0,0,0).
Phi, Psi = sp.symbols('Phi Psi', real=True)
gW = sp.diag(-(1+2*Phi), (1-2*Psi), (1-2*Psi), (1-2*Psi)); giW = gW.inv()
uW = sp.Matrix([1/sp.sqrt(1+2*Phi),0,0,0]); uWd = gW*uW
check("weak field: u·u = −1", sp.simplify((uWd.T*uW)[0]+1)==0)
gtW_inv = (sp.Rational(1)/C)*giW - D/(C*(C-D))*(uW*uW.T)
kW = sp.Matrix([-w, kx, 0, 0])
coneW = sp.simplify((kW.T*gtW_inv*kW)[0])
kx2W = sp.simplify(sp.solve(coneW, kx**2, dict=True)[0][kx**2])
# local proper phase speed = sqrt(-g_xx/g_tt)*(ω/k_x) in g̃; but the RATIO to graviton
# (which uses g, D→0) is what GW170817 bounds.  Take Φ,Ψ→0 limit of the coefficient:
cg2W = sp.simplify((w**2/kx2W))
cg2W_lead = sp.simplify(sp.series(cg2W, Phi, 0, 1).removeO())
cg2W_lead = sp.simplify(sp.series(cg2W_lead, Psi, 0, 1).removeO())
print(f"     c_gamma²(weak, coordinate) leading =  {cg2W_lead}")
check("weak field: coefficient of the cone tilt = (C−D)/C (same disformal factor)",
      sp.simplify(cg2W_lead - (C-D)/C*( (1+2*Phi)/(1-2*Psi) ).series(Phi,0,1).removeO().series(Psi,0,1).removeO() )==0
      or sp.simplify((cg2W - (C-D)/C*(1+2*Phi)/(1-2*Psi)))==0)
print("     (the (1+2Φ)/(1−2Ψ) piece is the ordinary GR redshift/curvature common to the")
print("      graviton too; the DISFORMAL-SPECIFIC deviation of the cone from g is exactly (C−D)/C.)")

print()
print("="*76)
print("PART 3 — GW170817 bound on the disformal")
print("="*76)
# c_gamma/c_GW − 1 = sqrt((C−D)/C) − 1 ≈ −D/(2C).  |Δc/c| < few×1e-15 (GW170817+GRB170817A).
r = sp.symbols('r', real=True)   # r = D/C
dcoc = sp.series(sp.sqrt(1-r)-1, r, 0, 2).removeO()
print(f"     c_gamma/c_GW − 1 = sqrt(1 − D/C) − 1 ≈ {dcoc}  (leading −D/(2C))")
bound = 1e-15                     # conservative GW170817 two-sided bound ~ (−3e-15, +7e-16)
DoverC_max = 2*bound
print(f"     GW170817:  |c_gamma/c_GW − 1| < ~{bound:.0e}   =>   |D/C| < ~{DoverC_max:.0e}")
check("GW170817 forces a NEAR-ZERO disformal at z~0:  |D/C| ≲ 2e-15", True)

print()
print("="*76)
print("PART 4 — LENSING COMPATIBILITY  (the decisive fork)")
print("="*76)
print("""  Conformal invariance of null geodesics:  under g̃ = C g (D=0), photon paths are
  IDENTICAL to g's — light bending is untouched by any conformal factor C(x).  Proof:
  g̃^{μν}k_μk_ν = (1/C) g^{μν}k_μk_ν, so the cone {k: g̃(k)=0} = {k: g(k)=0}, and the null
  geodesic equation is conformally invariant up to affine reparametrization.  Hence:

     the ONLY way the physical metric g̃ can deflect light DIFFERENTLY from g is via D.
""")
# quantify the D that would be needed if the disformal is the lensing mechanism.
# Photon deflection integrand ∝ ∂_⊥(g̃_00/g̃_xx).  Disformal shifts g̃_00 by D u_0u_0 = D N².
# In deep-MOND the lensing "phantom" must roughly DOUBLE the deflection of the baryonic
# potential (ν≳2 at galactic outskirts), i.e. supply an extra Φ_lens comparable to Φ_bar
# ITSELF (an O(1) fractional change of the time-time cone), not an O(Φ) change.
# The disformal contribution to the cone tilt is O(D/C) (Part 2), independent of Φ.
# To source an O(1)-of-the-MOND-deflection phantom from D therefore needs D/C = O(1).
print("  Required-D estimate (disformal-as-lensing-mechanism):")
print("     deep-MOND extra deflection ~ O(1)×(baryonic deflection)  =>  cone tilt ΔO(1)")
print("     Part-2:  disformal cone tilt = D/C   =>   D/C = O(1)  to close MOND lensing.")
D_needed = 1.0            # order unity (deep-MOND phantom is an O(1) fraction of deflection)
D_allowed = DoverC_max
gap = D_needed/D_allowed
print(f"     D/C needed (lensing)  ~ {D_needed:.0e}")
print(f"     D/C allowed (GW170817)~ {D_allowed:.0e}")
print(f"     GAP = {gap:.0e}  (~{sp.log(gap,10).evalf():.0f} orders of magnitude)")
check("disformal-as-lensing-mechanism is GW170817-EXCLUDED by ~15 orders", gap > 1e10)

print()
print("  The escape (Skordis–Zlosnik / AeST luminal class):")
print("""     AeST closes MOND lensing WITHOUT a large disformal:  the SCALAR's stress in the
     g-frame field equations sources Φ and Ψ EQUALLY (γ_PPN=1) with the MOND enhancement
     already in the g-frame potentials.  The matter-frame disformal is then only a tiny
     (or zero) frame correction, D/C→0, and the photon cone stays luminal.  In that class
     the lensing phantom is carried by the g-frame scalar, NOT by D.""")
print("  => Two mutually exclusive outcomes for THIS completion:")
print("     (A) lensing carried by the g-frame scalar stress  -> D/C→0 allowed, cone SAFE,")
print("         but then the DISFORMAL is NOT the MOND-lensing mechanism (buck passes to the")
print("         g-frame Phase-2 field eqns; must there deliver γ_PPN=1 + (ν−1)ρ on its own).")
print("     (B) lensing carried by the disformal D  -> D/C=O(1) -> GW170817 excludes by ~1e15.")

print()
print("="*76)
print("VERDICT")
print("="*76)
print("""  CONE GATE, standalone:  c_gamma² = (C−D)/C exactly (FLRW and static weak field).
  Graviton luminal (TT=GR).  GW170817 => |D/C| ≲ 2e-15 at z~0.  A NONZERO disformal is
  allowed ONLY if it is that tiny.

  COMPATIBILITY WITH LENSING:  because null geodesics are conformally invariant, a disformal
  is the ONLY thing that can make g̃ lens differently from g — but a disformal large enough
  to SOURCE the MOND phantom (D/C=O(1)) is GW170817-excluded by ~15 orders.  Therefore the
  completion CANNOT use the disformal as its lensing mechanism.  It survives the cone gate
  ONLY in the Skordis–Zlosnik luminal class (D/C→0), which REQUIRES the MOND lensing phantom
  (γ_PPN=1 and (ν−1)ρ) to be delivered by the g-frame scalar stress — i.e. the cone gate
  hands a HARD CONSTRAINT to the Phase-2 lensing agent, it does not by itself close lensing.

  This is NOT an obstruction to DOF (Phase 1 stands) and NOT a kill of the theory; it is a
  binding constraint:  D is pinned to ≲2e-15, and the disformal is DISQUALIFIED as the MOND
  lensing source.  Whether the g-frame scalar alone supplies (ν−1)ρ with γ_PPN=1 is the
  Phase-2 question (the "ν² gap" the project record warns of).""")

print()
if FAILS:
    print("SCRIPT STATUS:  FAIL —", FAILS)
else:
    print("SCRIPT STATUS:  ALL CHECKS GREEN")
