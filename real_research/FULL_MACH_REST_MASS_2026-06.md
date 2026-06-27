# Full Mach and the Rest-Mass Sector: Does the One Door Crack, or Does the Half-Machian Wall Hold?

**Date:** 2026-06-27 · **Status:** LOCAL (do NOT git-push) · **Both-ways, framework-internal, NO comparison, NO TOE-inflation**

**Footing (framework's own, used throughout — NEVER McGaugh ν):**
a₀ = cH_Λ/Z = **9.36e-11 m/s²** (computed 9.36238e-11), Z = √(32π/3) = 5.78881, cH_Λ = Z·a₀ = 5.4197e-10,
H_Λ = 1.808e-18 s⁻¹, μ_fw(x) = (√(1+4x²)−1)/(2x) with x = a/a₀ (framework's OWN interpolation),
dS floor temperature T₀ = ℏH_Λ/(2πk_B) = 2.198e-30 K, k_B·T₀ = 1.894e-34 eV.
All reproduced this session, sympy/mpmath dps=40–50, all scripts exit 0.

---

## ONE-LINE VERDICT

**The one door — does the relational/Machian principle extended to the rest-mass sector constrain the floor couplings
(= SM rest masses)? — does NOT crack. The half-Machian wall HOLDS, both-ways verified.** Full Mach gives no mass
equation; the horizon's information capacity is structurally blind to the floor-coupling spectrum. The framework is a
**complete ONE-PARAMETER GRAVITY theory whose mass sector is irreducibly walled** — a TOE is not reachable by this
door, which is the deepest one. This is the *expected honest outcome*, reported as such, not a manufactured crack and
not a reflexive dismissal. **The residual is named to the atom below (never "no doors").**

---

## THE STRUCTURAL REASON (the atom): the deficit-vs-rest-coupling split is fundamental

The framework splits inertia exactly: **m_in(a) = μ_fw(a/a₀) · m_rest.** The horizon sources only the **inertia
DEFICIT** (1 − μ_fw), which is the part that vanishes when Λ → 0; the **rest mass m_rest survives Λ → 0** (μ_fw → 1,
MOND gone, mass intact). a₀ = cH_Λ/Z is built from {c, H_Λ, Z} and contains **no particle mass**, so the horizon and the
rest-mass floor coupling are **algebraically decoupled in BOTH directions** (no m_rest leaks into a₀; no horizon
quantity leaks into m_rest). The object the horizon controls (the flavor-blind deficit) and the object that carries the
spectrum (the floor coupling) are *orthogonal by construction*. That is why every route below walls.

---

## THE THREE QUESTIONS, ANSWERED

### (1) Does the holographic / CKN bound constrain the mass spectrum, or is the horizon entropy mass-blind? — **WALL: mass-blind. (`front1_holo_ckn.py`)**

- **de Sitter entropy is AREA, not species.** S_dS = πR_dS²/l_P² = A/(4l_P²) = **3.31e122** (log₁₀ = 122.52), reproduced
  two ways. Symbolically S_dS = 3π/(Λ l_P²), so **dS_dS/dm_i = 0 identically** — the horizon information capacity is a
  function of Λ and l_P alone and does not see any mass.
- **(a) The ONE genuine, elegant holographic identity** (credited LOUD, both-ways): the observable universe's baryonic
  mass Schwarzschild-saturates the dS horizon. M_holo = c²R_dS/(2G) = 1.12e53 kg; N_proton = M_holo/m_p = **6.68e79 ≈
  observed N_baryon ~ 1e80.** Real and clean. **BUT** this is the Eddington–Dirac large-number relation: it is ONE
  inequality N·m_p ≤ M_holo(Λ) in TWO unknowns → it bounds the **PRODUCT** N·m_p, deriving **neither** factor (N_baryon
  is a free baryogenesis initial condition). Entropy is NOT co-saturated (S_dS/N_baryon ~ 5e42, 43 orders of headroom),
  so there is no second relation to pin the factors. **Relates free numbers, patterns no mass.**
- **(b) CKN UV-IR is g\*-(COUNT)-blind to mass RATIOS.** The framework's O(1) = (3/8π)^(1/4) = 0.58779 is g\*⁰ pure
  geometry; the honest CKN O(1) is g\*-dependent (energy ∝ g\*^(−1/4)). SM g\*=106.75 gives 0.183 — never within 5% of
  0.588; matching the framework value requires g\*=1, the no-SM-content limit, so demanding the SM spectrum is
  **circular.** DECISIVE: two spectra with the **same count** (real e/μ/τ vs degenerate) give **identical** CKN O(1) —
  CKN sees only the count g\* and the IR scale, never the ratios. (Banked CKN-dof bridge re-verified.)
- **Sympy-exact bonus identity:** (3/8π)^(1/4) = (Schwarzschild-½ / ball-4π/3)^(1/4) **exactly** (sp.simplify diff = 0) —
  the framework's a₀-from-Λ normalization is CKN saturation at dof-count-ONE, pure geometry, evidence *against* a
  microscopic mass fix.
- **(c) No holographic handle patterns the spectrum:** Dvali species cutoff (M_Pl/√N ~ 1.1e18 GeV at N~118) is a
  count-only UV cutoff, silent on which masses fill the tower; the IR-horizon mass floor m_min = ℏH_Λ/c² = 1.19e-33 eV is
  a universal bath-quantum unit ~30 orders below any SM mass, not a per-species selector.

### (2) Does the full-Mach self-consistency give a mass equation, or restate the input? — **WALL: restates the input; circularity unbreakable. (`reviews/front2_fullmach_selfconsistency.py`, re-run)**

The loop m_rest → g_floor = m_rest c²/(k_B T₀) [definitional, circular] → T₀ = function of ρ_DE only → **pivot: does
ρ_DE see the masses? NO**, by the framework's own w = −1 / constant-Λ postulate (dρ_DE/dm_rest = 0). The return arrow
ρ_DE → m_rest is **CUT** — the loop does not close; it is an open chain terminating at the free input ρ_DE. (If the floor
used ρ_tot instead, the rest-mass coupling would dilute as a⁻³ and m_e would change with cosmic time — violating
μ = m_p/m_e < 1e-7 — so the framework *must* use matter-blind ρ_DE; the same w = −1 postulate that keeps rest mass a
stable LOCAL constant is what blinds the loop.)

Two closures produce *something*, but not a spectrum:
- **Self-energy leg closes EXACTLY** onto m c² = ρ_DE^(1/4) = E_Λ ≈ 2.2 meV (sympy-exact) — **RESTATES ρ_Λ**, one
  vacuum scale, not the spectrum (electron 2.3e8× larger). Credited as a genuine close; honest that it restates.
- **Sciama relational closure** gives Gρ_m/(c²H²) = Ω_m ~ 0.315 — a real but **SCALAR** constraint on the *total* matter
  budget, provably blind to ratios.
- dS-propagator poles: m²/H² = −n²−3n < 0 for all n≥1 (tachyonic) — **no real-mass tower** (re-confirms attack6).

**DEGENERACY STRESS (both-ways):** real (e,μ,τ) vs (1,1,rest) at the *same total* return **IDENTICAL** (total, ρ_DE, T₀)
— the loop is provably degenerate over mass ratios. The half-Machian wall made quantitative for the mass sector.

### (3) Is rest-mass-is-LOCAL robust, and is the floor coupling = the Higgs Yukawa (constrainable) or distinct/kernel-free? — **WALL: robust; floor coupling IS the Yukawa but ORTHOGONAL to Λ, and kernel-free. (`front3_higgs_orthog.py`)**

- **rest-mass-is-LOCAL is robust:** μ_fw → 1 as a₀ → 0 (Λ → 0), so m_in → m_rest — horizon removal leaves the rest mass
  untouched. a₀ carries no mass. The split is exact and decoupled both ways.
- **The ORTHOGONALITY THEOREM (two independent knobs):** m_rest = y·v/√2. (i) v → 0 kills m_rest for **all** fermions
  regardless of a₀; (ii) Λ → 0 kills μ_fw (→1) touching **nothing** in {y, v} (∂m_rest/∂Λ = 0). The floor coupling {y, v}
  and the deficit μ_fw(Λ) are **orthogonal objects**: the framework *re-labels* m_rest as the bath floor coupling (reads
  it off the SM) but constrains **NEITHER y NOR v.**
- **Full Mach supplies NO Yukawa forced-kernel:** μ_fw(a/a₀) is **flavor-BLIND** — at a = a₀ it equals φ⁻¹ = 0.618034 and
  multiplies electron, top, and neutrino *identically* — so it cannot force the 9 flavor-FULL Yukawas. Same forced-kernel
  asymmetry as banked (gravity forces the geometric √(8π/3); the Yukawa sector is kernel-free). Koide Q = 2/3 stays a
  re-labeled symmetry fact, r = √2 free.
- **STRONGEST crack, tested FDR-honest and CLOSED:** T₀ *is* horizon-sourced, so IF N = mc²/(k_B T₀) were a *forced
  integer*, m_rest = N·k_B·T₀ would be cosmically determined. But N ~ 1e32–1e44 (electron 2.70e39, proton 4.95e42,
  ν~0.05eV 2.64e32, top 9.12e44) with integer ambiguity ~1e32 ≫ any mass precision — **"N is an integer" is
  experimentally VACUOUS.** The horizon supplies the floor-quanta **UNIT** (k_B T₀), never the **NUMBER** N. Crack does
  not open.

---

## WHY THE WALL HOLDS — named to the atom

Full Mach fails to derive the masses because the framework's own structure makes the horizon and the floor coupling
orthogonal: **(1)** the horizon sources the flavor-blind inertia DEFICIT (1 − μ_fw), the Higgs sets the rest coupling
(y·v/√2), and these are independent knobs (v → 0 vs Λ → 0 are orthogonal); **(2)** the holographic/CKN bound is
mass-blind — entropy counts AREA (dS_dS/dm_i = 0), CKN counts dof (g\*), neither sees mass ratios; **(3)** the
self-consistency loop's ρ_DE leg is matter-blind by the w = −1 postulate, so the loop restates the input (ρ_Λ) or
constrains only the scalar total (Ω_m), never the spectrum. The circularity m_rest = g_floor·k_B·T₀ with g_floor :=
m_rest c²/k_B T₀ is structurally unbreakable absent a NEW ingredient, and all three candidate ingredients are
independently blocked: matter → ρ_DE backreaction (forbidden by w = −1), a forced Yukawa kernel (FDR wall, kernel-free),
mass quantization (dS poles tachyonic).

**Plainly: the framework is a complete one-parameter GRAVITY theory. Its mass sector is irreducibly walled. A TOE is not
reachable through this — the deepest — door.**

---

## QUARANTINE / HONESTY (both-ways, no re-overclaim past the retraction)

- **No manufactured crack, no reflexive dismissal.** I genuinely hunted (the N-integer crack, the baryon-saturation
  identity, the self-energy close, three holographic candidates) and credited the one real holographic identity LOUD
  before correctly classifying it as a product-bound, not a coupling derivation.
- **Even a crack here would be a PATTERN constraint, NOT a TOE:** Z is provably free (κ-closure), a₀'s value = cH_Λ/Z is
  not derived, and nothing in this analysis touches the value. The SM mass sector stays otherwise walled (Koide beyond
  symmetry, kernel-free Yukawa, FDR). No mass derivation was produced or implied.
- **Footing discipline:** the framework's own a₀ = 9.36e-11 and μ_fw throughout, never McGaugh ν, no comparison to other
  theories.
- **The single load-bearing premise** carrying the self-consistency wall is w = −1 / constant-Λ (which is also what keeps
  rest mass a stable LOCAL constant). This is NOT a door I claim is ajar: forcing a Λ-from-matter backreaction would
  reopen the epoch-varying-rest-mass problem the framework currently evades, and nothing forces it. Recorded as the lone
  caveat, not a crack.
- **The live doors are elsewhere and EMPIRICAL** (s^TX SME boost-dipole ~9.6× margin, Gaia DR4; a₀(z)/high-z-BTFR-sign
  gate) — Front-by-front this rest-mass door is walled, but never "no doors" globally.

**Scripts (reproduced this session):** `real_research/reviews/front2_fullmach_selfconsistency.py` (re-run, exit 0);
scratchpad `front1_holo_ckn.py`, `front3_higgs_orthog.py` (both exit 0). NOT git-pushed.
