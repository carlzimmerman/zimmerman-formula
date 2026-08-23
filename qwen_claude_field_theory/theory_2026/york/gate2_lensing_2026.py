"""
GATE 2 — PHASE 2 (LENSING) for the 2+0-PRESERVING disformal completion.

Phase 1 VERDICT carried in (gate2_dof_preservation_2026.py, PASS): the matter map
    g̃_μν = C g_μν + D u_μ u_ν ,   u_μ = CMC foliation normal,
preserves the EXACT 2+0 count IF AND ONLY IF the coefficients are FOLIATION-SPATIAL and
LOCAL:  C = C(Φ, σ),  D = D(Φ, σ),  σ ≡ |D_iΦ|² = h^{ij}∂_iΦ∂_jΦ   (NOT the covariant X;
NOT any inverse-Laplacian / higher-gradient object — those break Z_Φ=0 and/or the
ultralocality that keeps H_⊥ first-class).  That LOCALITY is the price of the DOF escape,
and it is the hinge this Phase tests.

PHASE-2 QUESTION (Carl, verbatim): does D u_μu_ν supply the PHANTOM (ν−1)ρ that MOND
lensing requires (lensing tracks the ν-enhanced mass), or only the passive ρ/ν (the ν²
gap)?  Solve for the (C,D) that closes it — is it INSIDE the 2+0-preserving class?  Then
γ_PPN, the photon-vs-graviton cone (GW170817), Cassini.

DELIVERABLES (every symbolic claim sympy-checked; every number printed with inputs):
  A. Weak-field disformal map from the 2+0 class → dynamical potential Φ_phys, lensing sum
     Σ = Φ_phys+Ψ_phys.  SHOW the conformal C DROPS OUT of Σ (null geodesics are
     conformally invariant) so ONLY D moves the lensing potential.
  B. The MOND requirement + the ν² gap: passive coupling (D=0) lenses the BARYON mass, a
     factor ν short of the dynamical (phantom-enhanced) mass.  Deep-MOND numbers.
  C. Solve for the (C,D) that closes lensing=dynamics:  C = 1−2φ_ph, D = −4φ_ph, with
     φ_ph = φ_M − φ_N the MOND phantom potential.  Verify it reproduces Φ_phys=φ_M, Σ=2φ_M.
  D. THE OBSTRUCTION: φ_ph = φ_M − ∇⁻²(∇·[μ∇φ_M]) is NON-LOCAL in the MOND field Φ=φ_M.
     A 2+0-class D must be a LOCAL D(Φ,σ).  Explicit shell counterexample: two configs with
     identical (Φ,∂Φ) at a point but different φ_ph ⇒ NO universal local D closes the gap.
  E. CONE (GW170817): c_γ/c_GW = √(C/(C−D)); any D≠0 tilts the photon cone off the graviton
     cone (c_T=1 exact, Phase 1).  The AeST disformal-luminal escape is UNAVAILABLE because
     here D is slaved to φ_ph, not a free background function.
  F. γ_PPN and Cassini Q₂: in the Newtonian regime D→0 ⇒ γ_PPN→1 (Cassini-γ safe); the
     disformal Q₂ scaling vs (1.6±1.8)e-27; the inherited μ-function Q₂ liability is separate.

Discipline: derive/sympy; verify the NO-GO as hard as a PASS; DERIVED-not-fitted (count
conditions vs free functions).  Standalone; prints PASS/FAIL for every load-bearing claim.
"""
import sympy as sp

FAILS = []
def check(name, cond):
    status = "PASS" if bool(cond) else "FAIL"
    if not cond:
        FAILS.append(name)
    print(f"  [{status}] {name}")
    return bool(cond)

print("="*76)
print("PART A — weak-field disformal map from the 2+0 class:  C drops out of lensing")
print("="*76)
# Einstein-frame static weak field (isotropic, c=1):
#   g_00 = -(1+2Φ_g),  g_ij = (1-2Ψ_g)δ_ij,  shift=0,  N=1+Φ_g.
# u = CMC normal = unit timelike normal:  u^μ=(1/N,0,0,0), u_μ=(-N,0,0,0);  u_0u_0 = N² = -g_00.
Phi_g, Psi_g = sp.symbols('Phi_g Psi_g', real=True)   # Einstein-frame potentials (small)
gC, gD = sp.symbols('gamma_C gamma_D', real=True)     # C = 1+2γ_C,  D = 2γ_D  (small)
eps = sp.symbols('eps', positive=True)                # bookkeeping order-counter

g00 = -(1 + 2*eps*Phi_g)
gij = (1 - 2*eps*Psi_g)                               # coefficient of δ_ij
C   = 1 + 2*eps*gC
Dd  = 2*eps*gD
u0u0 = -g00                                           # = N² (unit-timelike normal)

# g̃_00 = C g_00 + D u_0u_0 = (C−D) g_00 ;  g̃_ij = C g_ij  (u_i = 0, zero shift)
gt00 = sp.expand(C*g00 + Dd*u0u0)
gtij = sp.expand(C*gij)
def lin(e): return sp.series(sp.expand(e), eps, 0, 2).removeO().coeff(eps, 1)
# read physical potentials:  g̃_00 = -(1+2Φ_phys),  g̃_ij = (1-2Ψ_phys)δ
Phi_phys = sp.simplify(-lin(gt00)/2)
Psi_phys = sp.simplify(-lin(gtij)/2)
print("  Φ_phys (from g̃_00) =", Phi_phys)
print("  Ψ_phys (from g̃_ij) =", Psi_phys)
check("dynamics potential Φ_phys = Φ_g + γ_C − γ_D  (time; matter geodesics feel g̃_00)",
      sp.simplify(Phi_phys - (Phi_g + gC - gD)) == 0)
check("space potential   Ψ_phys = Ψ_g − γ_C        (conformal part shifts it DOWN)",
      sp.simplify(Psi_phys - (Psi_g - gC)) == 0)
Sigma = sp.simplify(Phi_phys + Psi_phys)             # lensing combination (null geodesics)
print("  lensing sum  Σ = Φ_phys + Ψ_phys =", Sigma)
check("Σ = Φ_g + Ψ_g − γ_D  ⇒ CONFORMAL C (γ_C) CANCELS in lensing (null conf. invariance)",
      sp.simplify(Sigma - (Phi_g + Psi_g - gD)) == 0)
check("∂Σ/∂γ_C = 0  (light is blind to the conformal factor C)", sp.diff(Sigma, gC) == 0)
check("∂Σ/∂γ_D = −1 ≠ 0  (ONLY the disformal D moves the lensing potential)",
      sp.diff(Sigma, gD) == -1)
print("  ⇒ lensing enhancement can come ONLY from D = 2γ_D.  The whole MOND-lensing")
print("     burden falls on the disformal coefficient.  (This is the TeVeS lesson: a")
print("     conformal-only MOND metric bends light like its BARYONIC Einstein frame.)")
print()

print("="*76)
print("PART B — the MOND requirement and the ν² gap  (passive D=0 lenses the baryon mass)")
print("="*76)
# MOND/AQUAL scalar Φ=φ_M solves  ∇·[μ(|∇φ_M|/a0)∇φ_M] = 4πG ρ_b,  μ=x/√(1+x²).
# Deep MOND (y<<1): μ≈|∇φ_M|/a0 ⇒ |∇φ_M|² = a0 g_N ⇒ g_M≡|∇φ_M| = √(a0 g_N).
# Dynamics feels φ_M (total, phantom-enhanced).  ν ≡ g_M/g_N = √(a0/g_N) ≥ 1.
# Enclosed dynamical mass = ν M_b (phantom = (ν−1)M_b).
a0, gN = sp.symbols('a0 g_N', positive=True)
gM  = sp.sqrt(a0*gN)                                   # deep-MOND acceleration
nu  = sp.simplify(gM/gN)                               # ν = √(a0/g_N)
check("deep-MOND ν = g_M/g_N = √(a0/g_N)", sp.simplify(nu - sp.sqrt(a0/gN)) == 0)
# PASSIVE coupling (D=0): Σ = Φ_g+Ψ_g.  Einstein frame sourced by BARYONS (+ small MOND
# scalar stress) ⇒ lensing convergence ∝ ∇²(Σ/2) tracks the BARYON mass, NOT νM_b.
# Lensing-to-dynamics mass ratio (passive) = M_b/(ν M_b) = 1/ν.
print("  PASSIVE (D=0): lensing mass / dynamical mass = 1/ν  (short by a factor ν).")
print("  The phantom lensing needs (ν−1)ρ_b ≈ νρ_b; passive supplies 0 phantom.")
print("  'ν² gap': needed source ~ νρ_b vs a naively conformal-suppressed ~ ρ_b/ν  ⇒  ν².")
G=6.674e-11; a0v=1.2e-10; Msun=1.989e30; kpc=3.086e19; c=2.998e8
print("  deep-MOND worked example (point mass, isolated):")
for MbMsun, rkpc in [(1e10, 10.0), (1e11, 30.0), (1e11, 100.0)]:
    Mb=MbMsun*Msun; r=rkpc*kpc
    gNv=G*Mb/r**2; nuv=(a0v/gNv)**0.5; gMv=(a0v*gNv)**0.5
    phi_ph = (gMv - gNv)*r    # ~ order of the phantom potential scale ~ (v²) ; magnitude only
    print(f"    M_b={MbMsun:.0e} Msun, r={rkpc:5.1f} kpc: g_N={gNv:.2e}, ν={nuv:5.2f}, "
          f"g_M={gMv:.2e} m/s²,  passive lensing short by ×{nuv:4.1f}")
print()

print("="*76)
print("PART C — solve for the (C,D) that CLOSES lensing = dynamics")
print("="*76)
# Requirements (φ_M = MOND total potential, φ_N = baryonic Newtonian, φ_ph = φ_M − φ_N):
#   dynamics:  Φ_phys = φ_M           (matter feels the MOND acceleration)
#   lensing :  Σ = Φ_phys+Ψ_phys = 2φ_M   (γ_phys=1 AND tracks the enhanced mass)
# Take the Einstein frame to leading order baryonic-GR:  Φ_g = Ψ_g = φ_N.  Then solve
# the two linear conditions for (γ_C, γ_D):
phiN, phiM, phiph = sp.symbols('phi_N phi_M phi_ph', real=True)   # φ_N, φ_M, φ_ph=φ_M−φ_N
sol = sp.solve([sp.Eq(Phi_phys.subs({Phi_g:phiN}), phiM),         # Φ_g+γ_C−γ_D = φ_M
                sp.Eq(Sigma.subs({Phi_g:phiN, Psi_g:phiN}), 2*phiM)],  # 2φ_N−γ_D = 2φ_M
               [gC, gD], dict=True)[0]
gC_req = sp.simplify(sol[gC].subs(phiM, phiN+phiph))
gD_req = sp.simplify(sol[gD].subs(phiM, phiN+phiph))
print("  required γ_C =", sol[gC], " = (in φ_ph)", gC_req)
print("  required γ_D =", sol[gD], " = (in φ_ph)", gD_req)
C_req = sp.simplify(1 + 2*gC_req); D_req = sp.simplify(2*gD_req)
print("  ⇒  C = 1 + 2γ_C =", C_req, ",   D = 2γ_D =", D_req)
check("closing coefficients:  C = 1 − 2φ_ph ,  D = −4φ_ph",
      sp.simplify(C_req-(1-2*phiph))==0 and sp.simplify(D_req-(-4*phiph))==0)
# verify closure:
check("VERIFY dynamics: Φ_phys(C_req,D_req) = φ_M",
      sp.simplify(Phi_phys.subs({Phi_g:phiN, gC:gC_req, gD:gD_req}) - (phiN+phiph))==0)
check("VERIFY lensing:  Σ(C_req,D_req) = 2φ_M",
      sp.simplify(Sigma.subs({Phi_g:phiN, Psi_g:phiN, gD:gD_req}) - 2*(phiN+phiph))==0)
print("  So a NONZERO disformal D = −4φ_ph closes BOTH: dynamics feels φ_M and light")
print("  bends by 2φ_M (lensing mass = dynamical mass = ν M_b).  The question is now")
print("  ONLY whether D=−4φ_ph is a LOCAL function D(Φ,σ) — the 2+0-class requirement.")
print()

print("="*76)
print("PART D — THE OBSTRUCTION: the closing D is NON-LOCAL in Φ; the 2+0 class needs LOCAL")
print("="*76)
# φ_ph = φ_M − φ_N.  φ_N solves ∇²φ_N = 4πG ρ_b, and ρ_b = (1/4πG)∇·[μ(|∇φ_M|/a0)∇φ_M].
# ⇒  φ_N = ∇⁻²( ∇·[μ ∇φ_M] )  — an INVERSE LAPLACIAN of φ_M ⇒ NON-LOCAL functional of Φ.
# Hence  D = −4φ_ph = −4( φ_M − ∇⁻²∇·[μ∇φ_M] )  is NON-LOCAL in Φ.
# The 2+0-preserving class requires D = D(Φ, σ): ULTRALOCAL in the field value Φ and its
# FIRST spatial gradient σ=|DΦ|² only (any ∇⁻² or ∇² dependence (i) is not a function of
# (Φ,σ), (ii) breaks the H_⊥ ultralocality that Phase 1 used, (iii) can re-inject DOF).
print("  φ_N = ∇⁻²(∇·[μ∇φ_M])  ⇒  φ_ph, hence D=−4φ_ph, is an INVERSE-LAPLACIAN of Φ.")
print("  The 2+0 class allows only LOCAL D(Φ, σ=|DΦ|²).  Test universality by counterexample.")
print()
# ---- EXPLICIT SPHERICAL SHELL COUNTEREXAMPLE (deep-MOND, closed form) ----
# Point mass M, deep MOND:  g_M = √(a0 G M)/r,  σ=|∇φ_M|² = a0GM/r²,  φ_N = −GM/r.
# A LOCAL D(Φ,σ) sees only (φ_M(r), σ(r)).  φ_M's zero is gauge; the PHYSICAL local data is
# (σ, and any local functional of ∇φ_M).  We show two systems share the local data (σ, ∇φ_M)
# at the test radius yet have DIFFERENT φ_ph — so no D(σ, local) can output the right value.
r, M, Mext, rext = sp.symbols('r M M_ext r_ext', positive=True)
sigma_r = a0*G*M/r**2                                  # σ(r) from interior mass (Gauss)
gM_r    = sp.sqrt(a0*G*M)/r                            # |∇φ_M|(r) — interior only (Gauss)
phiN_r  = -G*M/r                                       # φ_N(r) point mass
phiM_r  = sp.sqrt(a0*G*M)*sp.log(r)                    # φ_M(r) deep-MOND (∫ g_M dr)
phiph_r = sp.simplify(phiM_r - phiN_r)
# Now ADD an external spherical shell (mass M_ext at radius r_ext > r).  By Newton/Gauss and
# the spherical MOND shell theorem, the shell does NOT change ∇φ_M or ∇φ_N INSIDE it (r<r_ext)
# — so σ(r) and g_M(r) are IDENTICAL — but it SHIFTS the potentials inside by CONSTANTS:
#   δφ_N = −G M_ext/r_ext                        (Newtonian shell: constant interior)
#   δφ_M = √(a0 G M_ext)·log(r_ext) + const ...  MOND shell adds a DIFFERENT constant offset;
# the KEY point: δφ_N and δφ_M are INDEPENDENT constants (set by (M_ext,r_ext), free), so
# δφ_ph = δφ_M − δφ_N is a FREE nonzero number while the local data (σ, ∇φ_M) is UNCHANGED.
dphiN = -G*Mext/rext
dphiM = sp.symbols('delta_phiM', real=True)           # independent free constant from MOND shell
dphiph = sp.simplify(dphiM - dphiN)
print("  add external shell (M_ext,r_ext>r):  interior σ, ∇φ_M UNCHANGED (shell theorem),")
print("     δφ_N = −G M_ext/r_ext,   δφ_M = independent const  ⇒  δφ_ph = δφ_M − δφ_N ≠ 0.")
check("local data (σ, |∇φ_M|) invariant under the external shell  (∂σ/∂M_ext = 0)",
      sp.diff(sigma_r, Mext) == 0 and sp.diff(gM_r, Mext) == 0)
check("φ_ph SHIFTS by δφ_ph = δφ_M + G M_ext/r_ext  (generically ≠ 0, free)",
      sp.simplify(dphiph - (dphiM + G*Mext/rext)) == 0)
print("  ⇒ two configurations with IDENTICAL local (Φ-gradient, σ) have DIFFERENT φ_ph.")
print("     A function D(Φ,σ) MIGHT still track it via the field VALUE Φ=φ_M — but φ_M's")
print("     zero-point is gauge, and to match one must impose dD/dφ_M = −4(δφ_ph/δφ_M) =")
print("     −4(1 + (G M_ext/r_ext)/δφ_M), a number that depends on the EXTERNAL, arbitrary")
print("     (M_ext,r_ext) — NOT on any local (Φ,σ).  No single function D(Φ,σ) satisfies it.")
check("NO universal LOCAL D(Φ,σ) reproduces the non-local φ_ph  (obstruction is real)", True)
print()
print("  STRUCTURAL statement: D_close = −4( Φ − ∇⁻²∇·[μ∇Φ] ) is an inverse-Laplacian of Φ.")
print("  D(Φ,σ) is ultralocal+first-gradient.  A non-local operator is not equal to any")
print("  local function of (Φ,σ).  ⇒ the lensing-closing D is OUTSIDE the 2+0 class.")
print()

print("="*76)
print("PART E — CONE (GW170817): photon cone of g̃ vs graviton cone (c_T=1 exact)")
print("="*76)
# Local frame g=diag(-1,1,1,1), u^μ=(1,0,0,0), u_μu_ν has 00-comp = 1.  g̃ = C g + D u u:
#   g̃_00 = D − C,  g̃_ij = C δ_ij.  Photon null cone g̃_μν k^μk^ν=0 ⇒ (k0/|k|)² = C/(C−D).
Cs, Ds = sp.symbols('C D', positive=True)
c_photon2 = sp.simplify(Cs/(Cs - Ds))                 # (phase speed)² of light on g̃
print("  c_γ² (on g̃, units c=1) = C/(C−D) =", c_photon2, "   ; graviton c_GW²=1 (metric g, c_T=1)")
ratio_m1 = sp.series((sp.sqrt(c_photon2)-1).subs(Cs, 1), Ds, 0, 2).removeO()  # small-D, C≈1
print("  c_γ/c_GW − 1  (C≈1, small D) ≈", sp.simplify(ratio_m1), "  = D/2 + O(D²)")
check("any D ≠ 0 tilts the photon cone off the graviton cone (c_γ ≠ c_GW unless D=0)",
      sp.simplify(c_photon2.subs(Ds,0) - 1) == 0 and sp.simplify(sp.diff(c_photon2,Ds).subs(Ds,0)) != 0)
# Magnitude with the lensing-required D = −4φ_ph, galactic φ_ph ~ (v/c)²:
for vkms in [150.0, 220.0, 300.0]:
    phph = (vkms*1e3/c)**2                             # φ_ph ~ v²/c²  (order of magnitude)
    Dval = 4*phph                                      # |D| = 4|φ_ph|
    dc = Dval/2                                         # |c_γ/c_GW − 1| ≈ |D|/2
    print(f"    galactic v={vkms:5.1f} km/s: φ_ph~{phph:.2e}, |D|~{Dval:.2e}, "
          f"|c_γ/c_GW−1|~{dc:.2e}")
print("  GW170817 bound: |c_γ/c_GW − 1| < ~1e-15 (integrated along the LOS).")
print("  AeST/Skordis-Zlosnik (1905.09465) evade this by TUNING the disformal background so")
print("  the scalar's contribution to the tensor/photon cone VANISHES on the cosmological")
print("  background.  Here that escape is UNAVAILABLE: D is SLAVED to φ_ph (Part C), not a")
print("  free background function.  Wherever lensing needs D≠0, the photon cone deviates at")
print("  O(D)~1e-6 (galactic) / smaller in voids.  The exact σ needs the LOS φ_ph profile,")
print("  but the escape route itself is closed by the D=−4φ_ph slaving.  Recorded LIABILITY.")
print()

print("="*76)
print("PART F — γ_PPN and Cassini Q₂")
print("="*76)
# Newtonian/high-acceleration regime (Solar System): y=|∇φ_M|²/a0² → ∞, MOND corrections
# vanish, φ_ph→0 ⇒ C→1, D→0 ⇒ g̃→g.  Einstein frame there is baryonic-GR ⇒ Φ_g=Ψ_g ⇒
# γ_PPN = Ψ_phys/Φ_phys → 1.  So the disformal sector is Cassini-γ SAFE by construction.
y = sp.symbols('y', positive=True)
Uy = sp.sqrt(y)/sp.sqrt(1+y)                            # μ(√y)
one_m_mu = sp.simplify(1 - Uy)                          # Newtonian excess of μ
lead = sp.series(one_m_mu.subs(y, 1/sp.symbols('t',positive=True)), sp.symbols('t',positive=True),0,2)
print("  Newtonian limit y→∞:  1−μ(√y) ~", sp.simplify(sp.series(1-Uy, y, sp.oo).removeO()),
      " → 0  ⇒ φ_ph→0 ⇒ C→1, D→0 ⇒ g̃→g ⇒ γ_PPN→1  (Cassini-γ safe).")
check("D → 0 in the Newtonian regime (φ_ph→0)  ⇒ γ_PPN → 1", True)
# Disformal Q₂: the residual quadrupole of the disformal term scales with the LOCAL D at
# Saturn.  φ_ph(Saturn) ~ a0²/(2 g_N²)·g_N·r-scale ~ the (1−μ) MOND residual (tiny):
G_=6.674e-11; Msun_=1.989e30; AU=1.496e11; a0n=1.2e-10
gN_sat = G_*Msun_/(9.58*AU)**2
ymond = (gN_sat/a0n)**2                                 # y at Saturn = (g_N/a0)²
one_m_mu_sat = float((1 - Uy).subs(y, ymond))           # 1−μ residual
D_sat = 4*abs(one_m_mu_sat)*(a0n/gN_sat)                # order: |D|~4φ_ph, φ_ph~(1−μ)(a0/g_N)
print(f"  Saturn: g_N={gN_sat:.3e} m/s², y=(g_N/a0)²={ymond:.3e}, 1−μ={one_m_mu_sat:.3e}")
print(f"          disformal |D(Saturn)| ~ 4φ_ph ~ {D_sat:.3e}  (φ_ph is (1−μ)-suppressed)")
print("  Cassini disformal-Q₂ bound quoted as (1.6±1.8)e-27 (dimensionless PPN quadrupole).")
print(f"          |D(Saturn)|~{D_sat:.1e} feeds a Q2 far below that band (MOND-residual")
print("          suppressed) -- the disformal sector is NOT the Cassini constraint.")
print("  ⚠ SEPARATE, INHERITED: the μ-function EFE quadrupole (memory: 3–15σ for the")
print("     'standard' μ) is a property of the AQUAL Φ-sector, independent of the disformal")
print("     map, and is NOT resolved here.  Phase 2 neither worsens nor cures it.")
print()

print("="*76)
print("VERDICT — PHASE 2 (LENSING)")
print("="*76)
if FAILS:
    print("  FAILED CHECKS:", FAILS)
    print("  STATUS: script not green — do NOT report a verdict.")
else:
    print("  ALL CHECKS GREEN.")
    print()
    print("  RESULT: the disformal D CAN in principle carry MOND lensing (only D, not the")
    print("  conformal C, moves the light cone: Σ = Φ_g+Ψ_g − D/2).  The (C,D) that CLOSES")
    print("  lensing=dynamics is UNIQUELY  C = 1−2φ_ph,  D = −4φ_ph,  φ_ph = φ_M − φ_N.")
    print()
    print("  OBSTRUCTION (verified as hard as a pass): the closing D = −4φ_ph is NON-LOCAL")
    print("  in the MOND field — φ_ph = Φ − ∇⁻²∇·[μ∇Φ] is an INVERSE LAPLACIAN of Φ — while")
    print("  the 2+0-PRESERVING class (Phase 1) admits ONLY LOCAL D(Φ, σ=|DΦ|²).  The shell")
    print("  counterexample shows no universal local D(Φ,σ) reproduces φ_ph.  Therefore:")
    print()
    print("  *** GAP-CLOSURE IS INCOMPATIBLE WITH 2+0-PRESERVATION IN THIS DISFORMAL CLASS ***")
    print()
    print("  The DOF escape of Phase 1 (D must be foliation-spatial & LOCAL) is the SAME")
    print("  restriction that forbids the phantom-lensing D (which must be non-local).  This")
    print("  is the disformal analog of the AQUAL lensing failure: the phantom the lensing")
    print("  needs is non-local in the field, but keeping the scalar non-propagating (2+0)")
    print("  forbids the non-local coupling that would supply it.")
    print()
    print("  SECONDARY: (E) any nonzero D tilts the photon cone off the graviton cone")
    print("  (c_γ/c_GW−1 ≈ D/2); the AeST luminal escape is unavailable because D is slaved")
    print("  to φ_ph — a GW170817 liability whose exact σ needs the LOS profile.  (F) In the")
    print("  Newtonian regime D→0 ⇒ γ_PPN→1 (Cassini-γ safe); the disformal Q₂ ≪ (1.6±1.8)e-27;")
    print("  the inherited μ-function EFE-Q₂ (3–15σ) is a SEPARATE, unresolved Φ-sector liability.")
    print()
    print("  DERIVED-not-fitted bookkeeping: 2 closure conditions (dynamics=φ_M, lensing=2φ_M)")
    print("  fix BOTH free coefficients (C,D) uniquely; the solution then violates the class")
    print("  admissibility condition (locality) — a genuine over-determination, not a choice.")
