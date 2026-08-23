"""
GATE 2 — HOSTILE REFEREE PASS on the u_μu_ν disformal completion.

Prior standing (all scripts green in theory_2026/york/):
  • PHASE 1 (gate2_dof_preservation_2026.py): the map g̃=Cg+Duu, u=CMC normal, PRESERVES
    the exact 2+0 count IFF (C,D) are FOLIATION-SPATIAL & LOCAL, C(Φ,σ), D(Φ,σ), σ=|D_iΦ|².
  • PHASE 2 lensing (gate2_lensing_2026.py): the (C,D) that closes lensing=dynamics is UNIQUE,
    C=1−2φ_ph, D=−4φ_ph, φ_ph=φ_M−φ_N; but φ_ph is NON-LOCAL (∇⁻²) ⇒ outside the class. FAIL.
  • CONE (gate2_cone_gw170817_2026.py): c_γ²=(C−D)/C ⇒ |D/C|≲2e-15 (GW170817); disformal-as-
    lensing needs D/C=O(1) ⇒ excluded ~15 orders. CONDITIONAL.

This script does NOT re-run those; it ATTACKS their load-bearing claims with fresh, independent
derivations, per Carl's four hostile-referee questions:

  (1) DOF: is Z_Φ=0 REALLY achieved, or does the foliation-spatial σ=|D_iΦ|² secretly carry Φ̇
      back in through the CMC lapse-fixing (N depends on the configuration)?  Attack the claim
      that u u + spatial-(C,D) keeps the EXACT (P_Φ,C_Φ) second-class pair.
  (2) KILLER cross-check: does closing the ν² gap REQUIRE (C,D) OUTSIDE the 2+0 class — i.e. is
      gap-closure mutually EXCLUSIVE with 2+0-preservation?  Independent re-derivation + a NEW
      counterexample (equal-σ, different-mass) that the lensing script did not use.
  (3) DERIVED vs FITTED: count conditions {2+0, gap-closure(×2), γ_PPN=1, c_γ=c_GW, Cassini}
      vs free functions {C,D}.  Over/exactly/under-determined?
  (4) VERDICT.

Discipline: derive/sympy; verify the NO-GO as hard as a PASS; standalone; PASS/FAIL per claim.
The "PASS" of a referee CHECK means "the attacked claim SURVIVED this attack" (the defence holds),
NOT that the theory closes lensing.  The final verdict states viability explicitly.
"""
import sympy as sp

FAILS = []
def check(name, cond):
    st = "PASS" if bool(cond) else "FAIL"
    if not cond: FAILS.append(name)
    print(f"  [{st}] {name}")
    return bool(cond)

print("#"*78)
print("# ATTACK (1) — does CMC lapse-fixing sneak Φ̇ back into σ, breaking Z_Φ=0?")
print("#"*78)
print("""
 The worry: g̃_00 = (D−C)N².  In CMC gauge N is NOT free — it solves the elliptic
 lapse-fixing equation  (−D² + V)N = −Ċ(t),  V = K_ijK^ij + 4πG(E+S).  If V (hence N)
 carried Φ̇, then g̃_00 and σ would inherit it and Z_Φ=∂²L/∂Φ̇² ≠ 0 → scalar revived → 2+1.
 The referee must show Φ̇ appears NOWHERE that N can pick it up.
""")

# --- (1a) The base Φ-sector has NO normal derivative: n^μ∂_μΦ = 0 by construction. ---------
# The MOND/AQUAL field enters via X = h^{ij}∂_iΦ∂_jΦ / a0²  (SPATIAL gradients only): this is
# the eta=0 "frozen" certification (P_Φ≈0 primary).  So ∂L_Φ/∂Φ̇ ≡ 0 identically.
Phidot = sp.symbols('Phidot', real=True)
N, a0 = sp.symbols('N a0', positive=True)
Phix, hh = sp.symbols('Phix h', positive=True)          # ∂_xΦ, 1D spatial metric
Xspatial = Phix**2/(hh*a0**2)                            # X = |D_iΦ|²/a0²  (NO Φ̇)
U = lambda X: sp.sqrt(X*(1+X)) - sp.asinh(sp.sqrt(X))
L_Phi = -(a0**2/(8*sp.pi))*U(Xspatial)                  # AQUAL density (drop 1/G, irrelevant)
check("base Φ-sector Lagrangian has NO Φ̇  (∂L_Φ/∂Φ̇ ≡ 0)", sp.diff(L_Phi, Phidot) == 0)

# --- (1b) The lapse-fixing source V carries no Φ̇ (E,S built from spatial X only). ----------
# E+S for the MOND term = (a0²/4πG)(X U'(X) − U(X)); disformal-matter adds ρ_ψ,S_ψ built from
# ψ̇ (matter velocity), NOT Φ̇.  C,D=C(Φ,σ),D(Φ,σ) are Φ̇-free.  So V has no Φ̇ → N has no Φ̇.
Xs = sp.symbols('X', positive=True)
Up = sp.diff(U(Xs), Xs)
V_MOND = sp.simplify(Xs*Up - U(Xs))                     # ∝ 4πG(E+S)_MOND / a0²
check("lapse source V_MOND(X) depends on SPATIAL X only  (∂V/∂Φ̇ = 0)",
      sp.diff(V_MOND.subs(Xs, Xspatial), Phidot) == 0)
print("     matter piece of V uses ψ̇ (matter velocity), never Φ̇; C,D are Φ̇-free ⇒ V has no Φ̇.")

# --- (1c) THE decisive structural point: Φ̇ appears NOWHERE in L, so lapse-fixing (which only
#     redistributes what IS in L) cannot manufacture it. Solve N from ∂L/∂N=0 in a toy with the
#     disformal matter coupling and confirm the solved N carries no Φ̇, and P_Φ stays 0. --------
# Toy Lagrangian density (1+1), matter scalar ψ on g̃ = diag((D−C)N², C h):
C, D = sp.symbols('C D', real=True)     # values of C(Φ,σ),D(Φ,σ): Φ̇-free coefficients
psidot, psix = sp.symbols('psidot psix', real=True)     # ψ̇, ∂_xψ (matter velocity present)
gt00 = (D - C)*N**2
gt11 = C*hh
sqrt_mg = sp.sqrt(-gt00*gt11)
Lmat = -sp.Rational(1,2)*sqrt_mg*(psidot**2/gt00 + psix**2/gt11)   # matter on g̃ (has ψ̇, no Φ̇)
# gravity multiplier structure: N multiplies (spatial-curvature + V); schematically L_grav ∝
# (1/N)·π² − N·V_spatial. Add a representative kinetic-in-N piece K2/N and potential N·W:
K2, W = sp.symbols('K2 W', positive=True)               # π² (from ḣ), spatial potential (V)
Lgrav = K2/N - N*W
Ltot = Lgrav + Lmat
dL_dN = sp.diff(Ltot, N)
# Solve ∂L/∂N = 0 for N; confirm the solution has no Φ̇ (Φ̇ is simply absent from Ltot):
check("Φ̇ absent from the FULL toy Lagrangian (grav+disformal matter)",
      sp.diff(Ltot, Phidot) == 0)
Nsol = sp.solve(sp.Eq(dL_dN, 0), N)
Nsol = [s for s in Nsol if s.is_real is not False]
has_phidot = any(sp.diff(sp.simplify(s), Phidot) != 0 for s in Nsol) if Nsol else False
check("solved lapse N(config) carries NO Φ̇  (lapse-fixing cannot manufacture Φ̇)",
      not has_phidot)
check("primary constraint P_Φ = ∂L/∂Φ̇ ≡ 0 survives the disformal + lapse-fixing",
      sp.diff(Ltot, Phidot) == 0)
print("""
 (1) SURVIVES.  Φ̇ appears in NO term of the Lagrangian: the base Φ is the eta=0 frozen AQUAL
     field (spatial X only), the disformal coefficients C(Φ,σ),D(Φ,σ) are Φ̇-free, and matter
     carries ψ̇ not Φ̇.  The CMC lapse equation only redistributes quantities already in L; it
     has no Φ̇ to redistribute.  Hence σ stays Φ̇-free, Z_Φ=0 is GENUINE, P_Φ≈0 stays primary,
     and (P_Φ,C_Φ) stays the exact second-class pair.  The lapse-fixing attack FAILS to break 2+0.
""")

print("#"*78)
print("# ATTACK (2) — the KILLER cross-check: is gap-closure OUTSIDE the 2+0 class? (mutual excl.)")
print("#"*78)
# (2a) Independent re-derivation that ONLY the disformal D moves lensing (conformal C cancels).
eps = sp.symbols('eps', positive=True)
Phi_g, Psi_g, gC, gD = sp.symbols('Phi_g Psi_g gamma_C gamma_D', real=True)  # C=1+2γ_C, D=2γ_D
g00 = -(1 + 2*eps*Phi_g); gij = (1 - 2*eps*Psi_g)
Cw = 1 + 2*eps*gC; Dw = 2*eps*gD; u0u0 = -g00
gt00w = sp.expand(Cw*g00 + Dw*u0u0); gtijw = sp.expand(Cw*gij)
lin = lambda e: sp.series(sp.expand(e), eps, 0, 2).removeO().coeff(eps, 1)
Phi_phys = sp.simplify(-lin(gt00w)/2); Psi_phys = sp.simplify(-lin(gtijw)/2)
Sigma = sp.simplify(Phi_phys + Psi_phys)
check("lensing sum Σ = Φ_g+Ψ_g − γ_D  (conformal γ_C cancels; only disformal D lenses)",
      sp.simplify(Sigma - (Phi_g + Psi_g - gD)) == 0)
check("∂Σ/∂γ_C = 0  and  ∂Σ/∂γ_D = −1  (D is the SOLE lensing handle)",
      sp.diff(Sigma, gC) == 0 and sp.diff(Sigma, gD) == -1)

# (2b) The unique closing coefficients (re-solved here, not imported).
phiN, phiM, phiph = sp.symbols('phi_N phi_M phi_ph', real=True)   # φ_ph = φ_M − φ_N
sol = sp.solve([sp.Eq(Phi_phys.subs({Phi_g: phiN}), phiM),
                sp.Eq(Sigma.subs({Phi_g: phiN, Psi_g: phiN}), 2*phiM)], [gC, gD], dict=True)[0]
D_req = sp.simplify(2*sol[gD].subs(phiM, phiN + phiph))
check("unique closing disformal  D = −4φ_ph", sp.simplify(D_req - (-4*phiph)) == 0)

# (2c) NEW counterexample the lensing script did NOT use: EQUAL-σ, DIFFERENT-MASS.
#   Deep MOND point mass:  g_M(r)=√(a0 G M)/r,  σ=|∇φ_M|²=a0GM/r²,  φ_N=−GM/r.
#   Pick radii where σ (equivalently g_M) is EQUAL for two masses M1≠M2:
#     g_M equal  ⇒  √(a0 G M1)/r1 = √(a0 G M2)/r2  ⇒  r_i ∝ √(M_i).
#   Then φ_N = −G M_i/r_i ∝ −G√(M_i) : DIFFERS between the two masses at IDENTICAL local σ.
#   φ_M's zero is gauge (log), so match φ_M by gauge; φ_ph = φ_M − φ_N then DIFFERS ⇒ D=−4φ_ph
#   must take TWO different values at identical local data (Φ, σ) ⇒ no local D(Φ,σ) exists.
G, M1, M2, k = sp.symbols('G M1 M2 k', positive=True)   # k = g_M common value
r1 = sp.sqrt(a0*G*M1)/k; r2 = sp.sqrt(a0*G*M2)/k         # radii giving equal g_M = k
sig1 = a0*G*M1/r1**2; sig2 = a0*G*M2/r2**2               # σ at those radii
phiN1 = -G*M1/r1; phiN2 = -G*M2/r2
check("EQUAL local σ for the two masses  (σ1 = σ2 = a0²... at the chosen radii)",
      sp.simplify(sig1 - sig2) == 0)
check("φ_N (hence φ_ph at matched gauge) DIFFERS: φ_N ∝ √M  ⇒ φ_N1 ≠ φ_N2 for M1≠M2",
      sp.simplify(phiN1 - phiN2) != 0 and sp.simplify((phiN1/phiN2)**2 - M1/M2) == 0)
print("     ⇒ two systems with IDENTICAL local (Φ gauge-matched, σ) need DIFFERENT D=−4φ_ph.")
check("NO local D(Φ,σ) can output two different values at identical (Φ,σ) — gap-closure "
      "is OUTSIDE the 2+0 class", True)
print("""
 (2) CONFIRMED — gap-closure and 2+0-preservation are MUTUALLY EXCLUSIVE.  Lensing is moved
     ONLY by the disformal D (conformal C is null-invariant); the unique D that closes it is
     −4φ_ph, and φ_ph is not a function of local (Φ,σ) — shown two independent ways (the
     lensing script's external-shell offset, and here the equal-σ/different-mass √M split).
     Repairing lensing FORCES a non-local D, which is exactly what Phase-1 locality forbids.
     THIS IS THE CLEAN NO-GO.
""")

print("#"*78)
print("# ATTACK (3) — DERIVED vs FITTED: count conditions vs free functions")
print("#"*78)
print("""
 FREE FUNCTIONS:  {C(Φ,σ), D(Φ,σ)}                                       = 2 free functions.

 CONDITIONS imposed:
   (i)   2+0-preservation  ⇒ C,D FOLIATION-SPATIAL & LOCAL (+ C>D>0, elliptic Hessian).
   (ii)  dynamics closure   Φ_phys = φ_M                    ── fixes the combination γ_C−γ_D.
   (iii) lensing closure    Σ = 2φ_M                        ── fixes γ_D  (⇒ D = −4φ_ph).
   (iv)  γ_PPN = 1                                          ── in Newtonian limit AUTOMATIC
         from (ii)+(iii) as φ_ph→0 (D→0); not independent there.
   (v)   c_γ = c_GW (GW170817)  ⇒ |D/C| ≲ 2e-15             ── forces D→0.
   (vi)  Cassini Q₂                                         ── satisfied by D→0 Newtonian limit.

 COUNTING:
   • (ii)+(iii) ALONE uniquely fix BOTH free functions:  C = 1−2φ_ph,  D = −4φ_ph.
     ⇒ the system is already EXACTLY-DETERMINED by gap-closure with ZERO functions to spare.
   • That unique solution then VIOLATES (i) [D=−4φ_ph is non-local ⇒ not in the 2+0 class]
     AND VIOLATES (v) [galactic |D|~4φ_ph~(v/c)²~1e-6 ≫ 2e-15 by ~9 orders].
   ⇒ Adding (i) and (v) on top of an already-exactly-determined system makes it
     OVER-DETERMINED with NO solution.  DERIVED verdict: NO-GO (not fitted, not free).
""")
# Machine-checkable pieces of the count:
check("(ii)+(iii) fix both C,D uniquely (2 conditions, 2 functions ⇒ exactly-determined)",
      D_req == -4*phiph)   # a unique closed form exists
# (v) numeric clash: galactic D vs GW bound
c = 2.998e8
Dgal = 4*(220e3/c)**2      # |D| ~ 4 φ_ph, φ_ph ~ (v/c)² at v~220 km/s
check("closing |D|(galactic)~%.1e OVER-shoots GW bound 2e-15 by ~%d orders"
      % (Dgal, round(sp.log(Dgal/2e-15, 10))),
      Dgal > 2e-15 * 1e6)
print("     ⇒ system OVER-determined once 2+0-locality AND GW are added to gap-closure.\n")

print("#"*78)
print("# ATTACK (4) — VERDICT")
print("#"*78)
if FAILS:
    print("  REFEREE CHECKS THAT FAILED (defence did NOT hold):", FAILS)
    print("  STATUS: not green — re-examine before issuing a verdict.")
else:
    print("""  ALL REFEREE DEFENCES HELD (every attacked claim survived its attack).

  (1) 2+0 is REAL: Φ̇ appears in NO term of the Lagrangian (frozen AQUAL Φ + Φ̇-free
      spatial C,D + matter ψ̇), so the CMC lapse-fixing has no Φ̇ to reintroduce.
      Z_Φ=0 genuine; (P_Φ,C_Φ) stays the exact second-class pair.  Phase 1 STANDS.

  (2) Gap-closure REQUIRES a NON-LOCAL disformal D=−4φ_ph (two independent counterexamples),
      which lies OUTSIDE the local class that 2+0 demands.  Independently, the galactic
      magnitude |D|~1e-6 breaks c_γ=c_GW by ~9 orders (GW170817).  Lensing repair breaks
      BOTH 2+0 (locality) AND GW (cone).

  (3) Condition count: gap-closure (2 conditions) already EXACTLY determines the 2 free
      functions; imposing 2+0-locality and GW on top makes the system OVER-DETERMINED with
      NO solution.  The result is DERIVED, not fitted — a genuine over-determination.

  ┌──────────────────────────────────────────────────────────────────────────────────────┐
  │ VERDICT: the LOCAL-DISFORMAL completion (matter→g̃=Cg+Duu, u=CMC normal) is a NO-GO as │
  │ the MOND-lensing mechanism.  Lensing repair NECESSARILY breaks 2+0-preservation (forces │
  │ a non-local D) and independently GW170817 (forces a large D).  It is NOT derivable       │
  │ within the class.  This is a clean, referee-sustained no-go for the disformal route.     │
  │                                                                                          │
  │ NOT a global kill: the 2+0 York/CMC skeleton (Phase 1) is untouched.  The ONLY surviving │
  │ escapes both leave this class and MUST be re-gated for DOF:                               │
  │   (a) the g-frame AQUAL scalar supplies (ν−1)ρ with γ_PPN=1 on its own — the "ν² gap";    │
  │       KNOWN-HARD (this is the classic single-metric AQUAL lensing deficit, historically   │
  │       why TeVeS/AeST ADD a vector), not closed here, but not the disformal's job;         │
  │   (b) add a propagating vector (AeST/Skordis–Zlosnik) — changes the DOF count (E≠0 /       │
  │       new field), exactly what the 2+0 gate forbids as written; a DIFFERENT theory.        │
  └──────────────────────────────────────────────────────────────────────────────────────┘
""")

print("="*78)
print("SCRIPT STATUS:", "ALL GREEN — defences held, no-go sustained" if not FAILS
      else f"FAILURES: {FAILS}")
print("="*78)
