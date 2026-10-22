# D9b_A33_multiplier FROZEN CRITERIA (written before any script or number of this lane)

Open row 12′ of `doors_push_2026_10_22/D9_uv_parent/MAP.md`: DSF-21's master action A33
(`deepseek_push/DS_FINAL_2026_10_21/A33_master_action/MASTER_ACTION.md` §1) **plus a Lagrange multiplier λ enforcing the Gauss
identity D_iP^i = ρ_c − ρ̄ as a field equation** (A66 "Route A", `A66_dof_repair/report.md` §2; A66's checks A2/A3 are stubs per
its erratum; A68 B9 computed only the {H_i, D·P} bracket and explicitly did not check Route A). κ = ½ is FITTED (κ = Z/4π is a
postulate; Z = 5.78881). Footings a₀ = 9.36e-11 (canonical) / 1.13e-10 m/s² (alt), never pooled. Cold energy, no particle
species. Not "theory closed". Nothing here says the data favour the framework over ΛCDM. Anything true by construction is flagged.

## 0. The theory under test (declared before computing)

A33's ADM Lagrangian (K = 4πG, c = 1) with clock term written ξ P^iD_i ln N (A33: ξ = 1, its K5) and the cold medium's rest-mass
coupling to the lapse written with weight m_c (A33 §1 and §3.4: T^c minimally coupled and conserved ⇒ m_c = 1), plus

  L_λ / (N√h) = λ (D_iP^i − (ρ_c − ρ̄)) ,  ς = 1 (A33 §7.3: the only consistent partition).

- **Literal member M_lit:** ξ = 1, m_c = 1 (A33 exactly as written + λ).
- **Law-preserving members:** whatever (ξ, m_c) the static computation (L1) shows reproduces g_N = g²/(g+a₀). If they form a
  family related by a field redefinition of λ, that family is one theory **M\*** and is the object of the verdict.

## 1. Scope

Linear perturbations per Fourier mode (scalar sector), H = 0 for the Dirac count, frozen-coefficient FRW for well-posedness,
static spherical cold branch for the law, high-k principal symbol for the cone (round-2 §4's principal Lagrangian, extended by
the medium and λ). The medium is the fluid reduction of A33's Vlasov sector (fixed dispersion σ_c² = a₀L★, A20), irrotational for
the scalar sector; its 2 vortical modes are counted separately. No full nonlinear bracket algebra; {H_⊥, H_⊥} first-classness is
inherited from A54/A68 (as A68 did).

## 2. Checks (script `d9b_a33_multiplier.py`, sympy + numpy, exact rationals where possible)

| id | test | PASS line |
|---|---|---|
| C1 | control: linear Dirac algorithm (generic code) on A68's H = 0 scalar action without medium | 1 scalar DOF (A68 D4/D5) |
| C2 | A33 + irrotational medium, no λ | scalar DOF computed; reported (expected count 2 is NOT a pass line; pass = algorithm terminates, rank stable over 3 random rational parameter draws) |
| C3 | M_lit and M\* (+ λ, π_λ) | per-mode dims, #first-class, #second-class, DOF reported; PASS = identical over 3 draws and identical for M_lit, M\*. Field-theory count stated as 26 + 2 (λ) + medium, with the computed number of second-class constraints the multiplier chain adds |
| C4 | DOF accounting vs A68 (26 / 8 FC / 5) | reported: does the multiplier remove the 5th (mixed conformal / P_L) mode, the medium sound, or a combination? PASS = the difference (no-λ minus λ) equals an integer ≥ 0 computed both from Dirac and from deg det of the EL operator |
| L1 | static spherical cold branch, γ → 0: law holds iff s ≡ ξ + m_c = 1 | sympy residual of the law exactly 0 at s = 1; M_lit (s = 2) deviation reported at g = a₀/3 (compare A33 K5's −0.55a₀) both footings |
| L2 | the law-preserving member's static cold equations equal AQUAL with μ(x) = x/(1+x) (L49) | symbolic residual 0 |
| L3 | members with ξ + m_c = 1 are related by λ → λ + cΦ (identity, flagged by construction) | symbolic residual 0 |
| T1 | **D-T test.** Low-k medium dispersion of M\*: is the medium's linear self-gravity term (−Kρ̄) present? c₂ ≡ 1 − (coefficient of −Kρ̄ in ω²)/1 computed | c₂ computed; **c₂ = 1 ⇒ D-T applies** |
| T2 | D-T hypotheses (CFG941 DERIVATION §1.3) checked one by one against M\*: (H1) cold static medium, (H2) always-on tether force F(u), (H3) phantom = own mass, g = g_N + u, (H4) law with deep limit. Each tied to a computed item | each hypothesis marked MET / NOT MET with the item |
| T3 | EdS growth exponent of M\* (medium + baryons, Ω_c/Ω_b = 5.3643) from the derived equations | reproduce CFG941 K3 0.60954 to 1e-4 if D-T applies; value reported either way |
| N1 | **NG1 test.** M\*'s enforced identity gives ρ_c = ρ̄ + ρ_ph with ρ_ph = AQUAL L49's phantom (L2). AG6C S0.4 (`argon_push/AG6C_relativistic_completion/ag6c_s0_saddle_results.json`, external labelled input) min ρ_ph/ρ̄ per fiducial and footing | NG1 bites iff min (1 + ρ_ph/ρ̄) < 0 at any fiducial |
| V1 | principal cone of M\* on a static background with u ∈ [0, a₀), any angle: speeds of all polarizations; is the A33 mode with ω²/k² = (γ/η)Δ, Δ = 1 + 4ηu²/K sin²θ…, still present? does a factor a₀/(a₀ − u) appear? | sup v² over u ∈ [0, a₀) and angle finite; formula reported; numbers both footings at L★ = 24 pc and 1 kpc, η = γ |
| F1 | FRW frozen-coefficient Hadamard test of M\* (comoving, H > 0): max Re s over the root set of the EL determinant at k → ∞, scaled by k² | max Re s / k² → 0 (≤ 1e-6 relative at the two largest k) ⇒ well posed; ∝ k² ⇒ WT-02-type ill-posed |
| F2 | the equation fixing λ on a leaf is elliptic with positive coefficient on FRW | coefficient of k²λ computed, > 0 for η > 0, ρ_c ≥ 0 |

`D9B_A33_MULTIPLIER COMPLETE: N/M checks PASS.`; exit 0 iff all pass. MUTATE (`D9B_MUTATE=1`): put WT-02/CFG938 S1d's expansion term
into the constraint (D·P → D·P − 3H Ṗ-potential/c², the non-intrinsic operator). F1 must FAIL. Outputs `*_MUTATE.out`,
`*_results_MUTATE.json`.

Constants (sources): G = 6.674e-11, c = 2.998e8, pc = 3.0857e16 m; ρ̄_c = Ω_c ρ_crit with Ω_c = 0.264, H₀ = 67.4 km/s/Mpc
(Planck 2018, standard); Ω_c/Ω_b = 5.3643 (A33 coefficient table row 9); L★ ∈ {24 pc (A20), 1 kpc}; η = γ = KL★²/2 for numbers
only (A68 D13: η/γ is unfixed — every number at η ≠ γ scales as stated in the README). No fitting, no scan toward a target.

## 3. What each outcome means (verdict rule, frozen)

- **EXCLUDED (named theorem)** — if L1 shows M_lit fails the law AND, for M\*, T1 gives c₂ = 1 with all four T2 hypotheses MET
  (⇒ D-T: no linear self-gravity, growth a^n with n < 1, hover/EFE of CFG941), OR N1 shows NG1 bites. Name every theorem that
  bites. Lane verdict word: **SCOPED NO-GO**.
- **VIABLE PARENT CANDIDATE** — M\* reproduces the law (L1/L2), T1 gives c₂ ≠ 1 or a T2 hypothesis NOT MET, N1 does not bite,
  V1 finite and ≤ 1 at η ≥ γ, F1/F2 well posed, and the C-count has no extra ghost. Lane verdict word: **CRISP FINDING**.
- **UNDECIDED** — anything else (e.g. law preserved and D-T evaded but NG1 needs a solve this lane cannot do, or F1 ambiguous).
  Lane verdict word: **NOTHING NEW** or **SCOPED NO-GO** with the open item named.
- V1 and F1 are reported regardless; a healthy cone or FRW does not rescue a parent excluded by D-T or NG1, and an unhealthy one
  excludes independently (named).
