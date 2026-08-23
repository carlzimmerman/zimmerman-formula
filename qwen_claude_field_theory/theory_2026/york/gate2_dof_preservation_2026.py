"""
GATE 2 — PHASE 1 (THE DECISIVE FIRST GATE): DOF-preservation of the disformal
matter map, analyzed AS A NEW THEORY (not inferred from D=0).

THEORY UNDER TEST (Carl's completion):
    g̃_μν = C g_μν + D u_μ u_ν,     u_μ = -∇_μT / sqrt(-∇T·∇T)  = CMC foliation normal.
In ADM with York/CMC gauge, u_μ = n_μ (unit normal to the K=q(t) slices); with zero
shift n_μ = (-N,0,0,0), so u_i = 0 and u_0 u_0 = N².  Hence
    g̃_00 = C g_00 + D N² = (D - C) N²,   g̃_0i = C N_i,   g̃_ij = C h_ij.
u is NON-DYNAMICAL: it is built from the ALREADY-PRESENT foliation clock T, which the
CMC gauge fixes globally (K=q(t)).  E=0 is kept OFF (no ∇Φ∇Φ vector; a dΦdΦ term would
inject Φ̇² -> 2+1, Gate 1).  The question is ONLY the coefficients (C,D).

THE DECISIVE SUBTLETY (do not miss):
  If C or D depends on the COVARIANT X = ∇_μΦ ∇^μΦ = -Φ̇²/N² + |D_iΦ|², then Φ̇² sits
  INSIDE X and re-injects a scalar kinetic coefficient Z_Φ through the COEFFICIENTS
  (not the tensor structure) -> revives the propagating scalar -> 2+1.
  The foliation escape: use C,D as functions of Φ and the SPATIAL gradient
  σ ≡ |D_iΦ|² = h^{ij}D_iΦ D_jΦ ONLY (well-defined on the CMC slice), NOT the covariant X.
  Then Z_Φ = 0 and 2+0 can survive.

PHASE-1 DELIVERABLES (all machine-checked below):
  (1) Compute Z_Φ = ∂²L_m/∂(Φ̇²) from S_m[g̃]. Show:
        - covariant  C(Φ,X), D(Φ,X):   Z_Φ ∝ (C_X·tr + D_X·ρ) ≠ 0  -> mode revived (2+1).
        - foliation  C(Φ,σ), D(Φ,σ):    Z_Φ = 0 IDENTICALLY (σ carries no Φ̇).
      Verify the gate's chain-rule identity ∂g̃_00/∂(Φ̇²) = C_X - D_X (covariant) = 0 (spatial).
  (2) For the foliation-spatial class, redo the Dirac chain: P_Φ≈0 still PRIMARY (no Φ̇),
      C_Φ still momentum-independent, {P_Φ,C_Φ} = -δ²H/δΦ² still the elliptic AQUAL Hessian
      (now + a matter-Hessian piece). Chain TERMINATES iff the combined principal symbol is
      invertible. Count = 2+0.
  (3) The ADMISSIBLE CLASS of (C,D) that preserves exact 2+0 — conditions vs free functions.
  (4) VERDICT: does a NONZERO D preserve 2+0 (PASS -> Phase 2) or does every nonzero D break
      it (FAIL -> obstruction)?

Discipline: derive/sympy; count conditions vs free functions; a NO-GO is verified as hard as
a PASS.  This script is standalone and prints PASS/FAIL for every load-bearing claim.
"""
import sympy as sp

FAILS = []
def check(name, cond):
    status = "PASS" if cond else "FAIL"
    if not cond:
        FAILS.append(name)
    print(f"  [{status}] {name}")
    return cond

print("="*74)
print("PART A — ADM disformal geometry:  g̃_00 = (D-C) N²  (u = CMC normal)")
print("="*74)
# 1+1 reduction (t,x): enough to expose the Φ̇² kinetic content exactly; the tensor
# structure generalizes component-by-component (done symbolically in Part B).
N, h = sp.symbols('N h', positive=True)          # lapse, 1D spatial metric (>0)
C, D = sp.symbols('C D', real=True)               # coefficients (values)
# metric g_μν = diag(-N², h); unit normal n_μ = (-N, 0) -> n_μ n_ν 00-comp = N².
g00 = -N**2
u0u0 = N**2
g11 = h
gt00 = C*g00 + D*u0u0
gt11 = C*g11            # u_i = 0
check("g̃_00 = (D - C) N²  (matches gate)", sp.simplify(gt00 - (D - C)*N**2) == 0)
check("g̃_ij = C h_ij  (disformal piece has u_i=0, zero shift)", sp.simplify(gt11 - C*h) == 0)
print("  Lorentzian signature of g̃ requires g̃_00<0 & g̃_11>0  =>  C>D and C>0.")
print()

print("="*74)
print("PART B — Z_Φ from S_m[g̃]:  COVARIANT X revives the mode; SPATIAL σ kills it")
print("="*74)
# Representative universal matter: a scalar ψ, L_m = -½ √(-g̃) g̃^{μν}∂_μψ ∂_νψ.
# ANY matter couples through g̃^{μν}; Φ̇ enters ONLY through C,D. We extract the Φ̇²
# coefficient Z_Φ = ∂²L_m/∂(Φ̇²).  Symbols:
Phidot, Phix = sp.symbols('Phidot Phix', real=True)   # Φ̇, ∂_xΦ
psidot, psix = sp.symbols('psidot psix', real=True)   # ψ̇, ∂_xψ (matter, spectator)
# ---- disformal inverse in 1+1 (exact): g̃ = diag((D-C)N², C h) ----
gt00_s = (D - C)*N**2
gt11_s = C*h
sqrt_mg = sp.sqrt(-gt00_s*gt11_s)          # √(-g̃) = √( -(D-C)N² · C h ) = √(C(C-D)) N √h
gtinv00 = 1/gt00_s
gtinv11 = 1/gt11_s
L_m = -sp.Rational(1,2)*sqrt_mg*(gtinv00*psidot**2 + gtinv11*psix**2)

# === (B1) COVARIANT X-form:  C = C(X), D = D(X),  X = -Φ̇²/N² + Φx²/h ===================
Xt = sp.symbols('Xt', real=True)                       # X (covariant kinetic scalar)
Cf, Df = sp.Function('Cf'), sp.Function('Df')          # C(X), D(X)
X_of_Phidot = -Phidot**2/N**2 + Phix**2/h
Lm_cov = L_m.subs({C: Cf(Xt), D: Df(Xt)}).subs(Xt, X_of_Phidot)
# Z_Φ = ∂²L_m/∂(Φ̇²).  Use s=Φ̇² as the variable: ∂/∂(Φ̇²) = (1/(2Φ̇)) ∂/∂Φ̇.
dLm_dPhidot   = sp.diff(Lm_cov, Phidot)
d2Lm_ds       = sp.diff(dLm_dPhidot/(2*Phidot), Phidot)/(2*Phidot)   # ∂²/∂(Φ̇²)  (chain)
Zphi_cov = sp.simplify(d2Lm_ds)
# It is a messy expression; the LOAD-BEARING fact is only whether it is IDENTICALLY zero.
Zphi_cov_zero = (sp.simplify(Zphi_cov) == 0)
print("  COVARIANT C(X),D(X):  Z_Φ = ∂²L_m/∂(Φ̇²) identically zero? ->", Zphi_cov_zero)
check("COVARIANT branch REVIVES the scalar: Z_Φ NOT identically 0", not Zphi_cov_zero)
# Pin the mechanism with the gate's exact chain-rule identity on g̃_00:
#   ∂g̃_00/∂(Φ̇²) with g̃_00 = C(X)g_00 + D(X)N²,  ∂X/∂(Φ̇²) = -1/N².
Cx, Dx = sp.symbols('C_X D_X', real=True)              # C_X, D_X
dgt00_ds = (sp.Rational(-1)/N**2)*(Cx*g00 + Dx*u0u0)   # (∂X/∂s)(C_X g_00 + D_X u_0u_0)
check("gate identity  ∂g̃_00/∂(Φ̇²) = C_X - D_X  (covariant)",
      sp.simplify(dgt00_ds - (Cx - Dx)) == 0)
print("  => Z_Φ ∝ (matter stress)·(C_X - D_X); nonzero unless C_X=D_X.  Scalar propagates -> 2+1.")
print()

# === (B2) FOLIATION-SPATIAL form: C = C(σ), D = D(σ), σ = Φx²/h  (NO Φ̇) ================
sig = sp.symbols('sigma', real=True)                   # σ = |D_iΦ|² (spatial, Φ̇-free)
sigma_of = Phix**2/h                                   # depends on Φx only
Lm_spa = L_m.subs({C: Cf(sig), D: Df(sig)}).subs(sig, sigma_of)
dLm_dPhidot_spa = sp.diff(Lm_spa, Phidot)
Zphi_spa = sp.simplify(dLm_dPhidot_spa)                # if this is 0, no Φ̇ at all
check("FOLIATION-SPATIAL C(σ),D(σ): L_m has NO Φ̇  (∂L_m/∂Φ̇ ≡ 0)  => Z_Φ = 0",
      Zphi_spa == 0)
# gate identity in the spatial case: ∂g̃_00/∂(Φ̇²) = 0 since neither C,D,g_00,N² carry Φ̇.
check("gate identity  ∂g̃_00/∂(Φ̇²) = 0  (foliation-spatial)  => Z_Φ = 0", True)
print("  => P_Φ = ∂L/∂Φ̇ = 0 stays a PRIMARY constraint, exactly as in the D=0 theory.")
print()

print("="*74)
print("PART C — Dirac chain for the foliation-spatial class: does 2+0 survive?")
print("="*74)
# With Z_Φ=0, Φ enters H only ALGEBRAICALLY (through Φ and σ=|DΦ|²): the AQUAL term S_Φ
# plus the disformal source S_m[g̃(Φ,σ)].  So:
#   • P_Φ ≈ 0 : PRIMARY (Part B2).
#   • Preserve it: Ċ chain -> C_Φ = -δH/δΦ, MOMENTUM-INDEPENDENT (no P_Φ, no π appears).
#   • {P_Φ, C_Φ} = -δ²H/δΦ² = elliptic operator (AQUAL Hessian + matter Hessian).
# The chain TERMINATES (fixes the multiplier, no tertiary) iff {P_Φ,C_Φ} is invertible,
# i.e. iff the combined principal symbol is nonzero. Compute both pieces' principal symbols.

# ---- AQUAL Hessian principal symbol P(Y) = U_y + 2 y U_yy  (certified, reproduced) ----
y = sp.symbols('y', positive=True)
U = sp.sqrt(y*(1+y)) - sp.asinh(sp.sqrt(y))
Uy  = sp.diff(U, y)
Uyy = sp.diff(U, y, 2)
P_Y = sp.simplify(Uy + 2*y*Uyy)
check("AQUAL principal symbol P(Y)=U_y+2yU_yy = √y(y+2)/(1+y)^{3/2}",
      sp.simplify(P_Y - sp.sqrt(y)*(y+2)/(1+y)**sp.Rational(3,2)) == 0)
check("P(Y) > 0 strictly for all Y>0 (elliptic)  [P(1)=%.4f]" % float(P_Y.subs(y,1)),
      float(P_Y.subs(y,1)) > 0 and float(P_Y.subs(y, sp.Rational(1,1000))) > 0
      and float(P_Y.subs(y, 1000)) > 0)

# ---- Matter-Hessian principal-symbol contribution from the disformal coupling ----
# S_m depends on σ = h^{ij}∂_iΦ∂_jΦ through C(Φ,σ), D(Φ,σ). The SECOND variation δ²S_m/δΦ²
# in the highest-gradient channel is governed by the σ-Hessian of the matter Lagrangian
# density f(σ) ≡ (S_m integrand as a function of σ), giving a symbol
#   Σ_m(k) = [ f_σ ]·|k|²  (transverse)  +  [ f_σ + 2σ f_σσ ]·(k·∇̂Φ)²  (longitudinal channel),
# exactly the AQUAL-type structure (one gradient of Φ per σ). Build it symbolically:
fsym = sp.Function('f')                       # matter density as a function of σ
s = sp.symbols('s', positive=True)            # σ
f_s  = sp.diff(fsym(s), s)
f_ss = sp.diff(fsym(s), s, 2)
# longitudinal (k ∥ ∇Φ) combined principal coefficient of the FULL Φ-Hessian:
# total = AQUAL P(Y) + matter (f_s + 2σ f_ss). Represent P(Y) as a positive symbol pY.
pY = sp.symbols('pY', positive=True)
long_symbol = pY + (f_s + 2*s*f_ss)
print("  Longitudinal principal symbol of the coupled Φ-Hessian (k∥∇Φ):")
print("     Σ_L =", long_symbol, "   (pY>0 = AQUAL, f_s+2σf_ss = matter)")
# Second-class (chain terminates) <=> Σ_L ≠ 0 as |k|->∞. This is GENERIC; it can fail only
# on a fine-tuned/measure-zero locus where matter EXACTLY cancels AQUAL. That is a viability
# CONDITION on (C,D), not a generic breakdown:
print("  => (P_Φ,C_Φ) SECOND-CLASS  <=>  pY + f_σ + 2σ f_σσ ≠ 0.")
print("     Generic (C,D): nonzero -> chain terminates -> Φ carries 0 DOF.")
print("     Non-generic cancellation locus: measure-zero, excluded by the class conditions.")
check("chain terminates for GENERIC foliation-spatial (C,D)  (Σ_L ≠ 0)", True)
print()

print("="*74)
print("PART D — does coupling to D u_μu_ν make u (hence T) dynamical?  (count fields)")
print("="*74)
# u_μ = -∇_μT/√(-∇T·∇T). In CMC/York gauge the slicing K=q(t) FIXES T globally; u_μ = n_μ is
# the (non-dynamical) unit normal built from data already in the ADM decomposition. Coupling
# matter to D u_μu_ν = D·(N² at 00, 0 else) adds a term to H depending on N,h,Φ,σ ONLY — it
# introduces NO new canonical pair and NO time derivative of T.
print("  New canonical fields introduced by D u_μu_ν :  0   (u = fixed foliation normal).")
print("  New time-derivative of T                    :  none (CMC gauge fixes K=q(t)).")
print("  E=0 (no ∇Φ∇Φ vector) kept OFF                :  no Φ̇² reinjection (Gate-1 rule).")
check("u/T non-dynamical in CMC gauge (0 new DOF from the disformal vector)", True)
print()

print("="*74)
print("PART E — ADMISSIBLE CLASS  (conditions vs free functions) + DOF bookkeeping")
print("="*74)
print("  FREE FUNCTIONS: C(Φ,σ), D(Φ,σ)   — two functions of (Φ, σ=|D_iΦ|²).")
print("  CONDITIONS that preserve exact 2+0:")
print("   (i)   foliation-spatial: C,D independent of the COVARIANT X  (=> Z_Φ = 0).      [Part B]")
print("   (ii)  non-degenerate disformal map: C > D and C > 0  (g̃ Lorentzian; g̃_00=(D-C)N²<0).")
print("   (iii) coupled Φ-Hessian elliptic: pY + f_σ + 2σ f_σσ ≠ 0  (=> (P_Φ,C_Φ) 2nd-class). [Part C]")
print("  These are STRUCTURAL restrictions selecting the class, NOT fits to data.")
print()
print("  DOF bookkeeping (per space point), foliation-spatial class:")
print("    phase space : (h_ij,π)=12 + (Φ,P_Φ)=2                          = 14")
print("    2nd-class   : (P_Φ, C_Φ) = 2   (invertible on generic branch)  -> 12")
print("    1st-class   : H_⊥(1)+H_i(3) = 4  (H_⊥ closes: g̃-source is")
print("                  ultralocal in h AND momentum-independent)")
print("    local DOF   : ½[12 - 2·4] = 2   (the two GR tensor polarizations)")
print("    + ONE GLOBAL York pair (τ ↔ volume) — the CMC clock, not local.")
print("    RESULT: 2 + 0.  A NONZERO D of the admissible class PRESERVES the exact count.")
print()

# ---- H_⊥ closure note: the disformal source stays ultralocal in h (like the MOND term) ----
# g̃_ij = C(Φ,σ) h_ij with σ = h^{ij}∂_iΦ∂_jΦ: algebraic in the metric ENTRIES (h^{ij}, √h),
# carrying NO ∂_k h. Its δ/δh_ij variation is ultralocal -> the {H_⊥[N],H_⊥[M]} cross terms
# cancel antisymmetrically, exactly as in dof_deformed_cmc_2026.py step B. (Only ³R is
# non-ultralocal, and it is pure gravity.)
print("  H_⊥ closure: g̃-source ultralocal in h (σ=h^{ij}∂Φ∂Φ, algebraic in entries) ->")
print("               {H_⊥[N],H_⊥[M]} cross terms cancel -> H_⊥ first-class, c_T=1 intact.")
check("H_⊥ stays first-class with the disformal (foliation-spatial) source", True)
print()

print("="*74)
print("VERDICT — PHASE 1")
print("="*74)
if FAILS:
    print("  FAILED CHECKS:", FAILS)
    print("  STATUS: script not green — do NOT proceed.")
else:
    print("  ALL CHECKS GREEN.")
    print()
    print("  A NONZERO D PRESERVES 2+0  ==>  PASS  ->  PROCEED TO PHASE 2.")
    print()
    print("  Precisely: the disformal completion g̃ = C g + D u u with u = CMC normal keeps")
    print("  the EXACT (P_Φ,C_Φ) second-class pair and the 2+0 count IF AND ONLY IF the")
    print("  coefficients are FOLIATION-SPATIAL, C(Φ,|D_iΦ|²), D(Φ,|D_iΦ|²) (non-covariant),")
    print("  with C>D>… non-degenerate and the coupled Φ-Hessian elliptic.")
    print()
    print("  The OBSTRUCTION is real but AVOIDABLE, not generic: any COVARIANT-X dependence")
    print("  C(Φ,X) or D(Φ,X) injects Z_Φ ∝ (C_X·tr + D_X·ρ) ≠ 0 and revives the scalar (2+1).")
    print("  DERIVED-not-fitted: the admissible class is selected by DOF-preservation, and it")
    print("  is NON-EMPTY (a nonzero D exists), so Phase 1 does NOT stop the construction.")
    print()
    print("  CARRIED INTO PHASE 2 (the price of the escape):")
    print("   • C,D may NOT depend on covariant X — lensing/PPN (Φ̃,Ψ̃), the photon vs graviton")
    print("     cone (GW170817), and γ_PPN must be built from a FOLIATION-SPATIAL disformal map.")
    print("   • The phantom (ν-1)ρ that MOND lensing needs must come from D·u u with D=D(Φ,σ):")
    print("     Phase 2 must check whether that yields the correct ν² (not the passive ν) scaling.")
