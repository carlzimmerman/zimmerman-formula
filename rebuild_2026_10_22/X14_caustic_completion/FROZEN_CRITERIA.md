# X14_caustic_completion: are caustics generic for v3s's khronon dust, and is there a caustic-free completion with no new scale? FROZEN CRITERIA

Written and committed (with `ASSUMPTION_LEDGER.md` and `LITERATURE_MAP.md`) before any lane script exists and before any
derivation result. Rules: `rebuild_2026_10_22/BRIEF.md`, `doors_push_2026_10_22/BRIEF.md`. κ = ½ is FITTED. Footings canonical
a₀ = 9.3603e-11 m/s² and alt a₀ = 1.1312e-10 m/s², never pooled. No dark-matter particle. Never "theory closed"; nothing here
says the data favour the framework. This is a theory-consistency lane: no data comparison. Small jobs only:
`OMP_NUM_THREADS=1 nice -n 15`, < 1 GB RSS, minutes; the heavy queue and every other lane untouched; no downloads.

## 0. What was read, and the not-blind statement

Read before freezing: `rebuild_2026_10_22/BRIEF.md`; `covariant_push_2026_10_22/V3_FULL_PICTURE.md` (§1, §2, §4.7, §6);
the READMEs of X8, X10, X12, O1, X6, X3 (and X3's B1-S / B2-S code in `x3_switched_stiffness.py`), S4 (μ_K bound), Q7 (BS25's
DBI K), C5_health; the reviews `v3s_soft_side_caustics_2026_10_23` and `v3_constraint_algebra_2026_10_23`. The literature
look-ups of `LITERATURE_MAP.md` (PROVISIONAL).

**Not blind.** I know the record's results: X8/X10 fold (soft lobes at t₀ + 0.4 to 2.7 Gyr; the wake line behind a MW-mass
mass at t_i + 3.9–4.4 Gyr), X12 is not validated, C5's IR band for β > 0, X3 E2's β window estimate. Before freezing I made
these back-of-envelope scoping estimates (no script, not used as results):
- a test stream past a MW-mass point mass at b ≈ 25 kpc, V ≈ 70 km/s: the khronon's k-independent self term ω_p² = Kρ(M − 1)
  of the AQUAL phantom times the Newtonian Danby–Camm focusing time gives ω_p τ_f ≈ V/(2v_K(b)) ≈ 0.35;
- the stiffness sound speed L★√(Kρ/2) of the phantom at ~100 kpc is ~0.03 km/s (Mach ~10³);
- C1 needs β ≳ 1e-6 to make a ~70 km/s wind subsonic at x ≈ 0.1, and C5's IR band allows β ≲ 1e-5 at μ_K = 0.1 Mpc⁻¹;
- √M μ_K ℓ ≈ 0.02 at μ_K = 0.1 Mpc⁻¹, ℓ ≈ 100 kpc.
These estimates shaped which numbers §4 computes. Thresholds below are structural (signs, exponents, existence of a window),
not tuned to them.

## 1. Definitions

- **v3s's khronon fluid** (X3 B2-S; V3_FULL_PICTURE §2): velocity v = −∇σ (exactly irrotational), charge
  ρ_τ = D·P + ρ_d with ρ_d = −μ_K²Ξ/K (K ≡ 4πG), force −∇φ + ∇Ξ, hold law Kρ_τ = ∇·[(1 − μ(x))∇Ξ] − μ_K²Ξ, x = |∇Ξ|/a₀,
  μ = x/(1+x), switched stiffness −(γ_L/2)[max(D·P, 0)]², γ_L = K L★²/2. The PN Lagrangian is X3's `L1` (B2-S).
- **Caustic**: finite-time blow-up of the khronon's second derivatives ∂²σ from smooth data. Either J = det(∂x/∂q) → 0
  (shell crossing, pressureless elements) or a gradient catastrophe of the characteristics (a shock) where a pressure acts.
  Both end the single-valued smooth khronon (Babichev 2016's notion for k-essence).
- **Generic**: occurs for an open set of smooth initial data, including data in the regime of X8/X10 (relative speed
  w ∈ [68.75, 74.8] km/s, MW-mass 6e10 M☉, fold locations r ∈ {11, 33, 73, 91, 156} kpc from the mass), not only for
  symmetric or fine-tuned data.
- **Completion**: a modification of v3s (action term, field content or solution concept) proposed in the literature to
  prevent or continue the caustics of pressureless scalar dust, k-essence or projectable-HL dust.
- **New scale**: any constant not already in v3s, dimensionful or dimensionless (a dimensionless coefficient sets a scale,
  e.g. c√β). v3s's constants: κ (a₀), L★ (γ_L), μ_K (free, ≤ 0.1 Mpc⁻¹ by S4, BS cap 10 Mpc⁻¹), the postulated J_x, c, G.
  No constant is fitted here; a new constant's allowed range is reported from the checks, never chosen.

## 2. The frozen class list (from `LITERATURE_MAP.md`) and each class's representative

| class | representative used in step 2 |
|---|---|
| C1 K² / (□φ)² (mimetic γ, ghost condensate, projectable-HL λ ≠ 1, khronon β) | PN Lagrangian term −(B/(2K))(∇²σ)², B = βc²/(2 + 3β) (record form, X3 E2 / C5); β > 0 ghost-free (C5) |
| C2 higher-spatial-curvature potential (Mukohyama's higher codimension) | Poisson ∇²φ − sℓ_*²∇⁴φ = Kρ, both signs s = ±1 |
| C3 native K(Q) pressure | v3s's μ_K term as it is (χ = k²/(KM_θ + Θγ_Lk²) + μ_K²/K); k ≪ μ_K barotropic limit p = Kρ²/(2μ_K²) |
| C4 DBI / BI; de Rham–Motohashi caustic-free set | BS25 K = (2μ²/λ_D)[1 − √(1 − λ_D(Q − 1)²)]; the condition c_s² = K′/(QK″) = 1 + αX with X ∝ Q² |
| C5 complex scalar (Madelung) | Bernoulli gains the quantum potential Q_ν = −(ν²/2)∇²√ρ/√ρ, ρ = \|Ψ\|² (ν = ℏ/m); field content of BR17 for P4 |
| C6 imperfect-DM deformation f(Y/X², Z/X³) | its PN content: an acceleration-dependent constraint function (the same variable as v3s's Y = \|∇Ξ\|²/c⁴), and Landau-frame vorticity |
| C7 vector / aether promotion | record (C5, v4) and literature (DOF, c₁₃); no new derivation |
| C8 multi-stream / kinetic | record (O1 K6, K11) and literature; no new derivation |
| C9 adhesion / vanishing viscosity | sticky merger of two khronon elements with charges m₁, m₂ (charge and momentum conserved) |

**Stop rule:** this list is frozen. No class is added after step 2 starts. No constant is fitted. No data comparison.

## 3. Step 2: checks per class (sympy unless stated)

- **P1 static limit.** The class's contribution to the static field equations on v3s's static branch (khronon at rest,
  Ξ = φ + C, K = ∇·n = 0) is zero → PASS (AQUAL and the a₀-line unchanged). Zero only as the new constant → 0 →
  PASS-WITH-BOUND. Otherwise FAIL.
- **P2 Solar-System screening.** C6/X3-D2's static screened solution is unchanged (same test as P1 for the screened
  equations). Preferred-frame (moving-Sun, PPN α₁, α₂) effects are not part of this pass and are reported as not checked.
- **P3 dispersion, both sides of D·P = 0.** X3's linear system (`disp_switched`, copied with provenance) extended by the
  class's representative. Check **R0** first: X3's B1-S ω² reproduced on Θ = 1 and Θ = 0 (residual 0). Report ω²(k) for
  Θ = 1, 0, the large-k exponent n (ω² ∝ kⁿ) and its coefficient sign for ρ_τ > 0 and ρ_τ < 0, and any (M_θ − 1) factor.
- **P4 DOF.** Number of ω² roots of the scalar determinant + 2 tensor modes, for classes inside the PN system; the
  completion's full field content at all energies otherwise (record/literature). PASS iff 3.
- **P5 GW speed.** The class's operator on unitary-gauge Minkowski with a TT perturbation (h₊, h× of t, z) contributes no
  term quadratic in h → PASS. A class that changes the tensor sector passes only with a bound (c_T → c at k → 0 within
  \|c_T/c − 1\| ≤ 1e-15) → PASS-WITH-BOUND.
- **P6 well-posedness and health.** (a) No Hadamard growth: −ω² bounded above uniformly in k on both sides, both signs of
  ρ_τ (X3's standard). (b) No ghost (C5's kinetic sign). (c) An IR gradient band is tolerated only if its maximum rate is
  ≤ H₀ (native H₀ = 67.2 km/s/Mpc, the lower end, conservative) at some S4-allowed μ_K ∈ {0.03, 0.1} Mpc⁻¹; for C1 the band
  is C5's ω² = −βc²k²/(2 + 3β) for aH ≪ k ≪ μ_K, maximum rate taken at k = μ_K (C5's own estimate form) → PASS-WITH-BOUND.
  (d) Representability: the class must allow both signs of ρ_τ and its zero crossing (v3s's charge is sign-indefinite:
  X8 soft lobes, H4 saddles, X3's interface). FAIL if it needs ρ_τ ≥ 0 or is singular at ρ_τ = 0.
- **FT fold test** (uses P3 and the step-3 models):
  - **FT-FAIL** if the class leaves n = 0 (a k-independent restoring term) on either side or for either sign; or its pressure
    stays finite as J → 0 (linearly degenerate), so the step-3 sheet fold is not prevented; or it acts only at
    k² ≲ M_θμ_K² with √M_θ μ_K ℓ < 1 at the fold locations for S4-allowed μ_K.
  - **FT-COND** if n = 2 (pressure / acoustic) on both sides for both signs: the fold is removed only for subsonic
    compression (c_class ≥ w at the fold locations); supersonic compression in a genuinely nonlinear field gives a gradient
    catastrophe (A11). It counts as removing the fold iff the subsonic condition holds at all five fold locations, with the
    conservative bracket M_θ − 1 = x, at a value of the class's constant that also passes P6(c), on both footings.
  - **FT-PASS-LIT** if n ≥ 4 (dispersive) on both sides for both signs: removal of the finite-time singularity rests on the
    literature (BR17), not shown here.
  - **FT-PASS-CONSTRUCT** for C8 and C9 (continuation by construction).
- **SC scale.** List the class's new constants and the range the checks allow; say how each could be fixed (a derivation
  from v3s's own quantities, or nothing). Never fitted.

## 4. Step 3: the analytic folds from v3s's own equations (sympy; numbers where stated)

- **F1 planar reduction (μ_K = 0).** From X3's `L1`: (a) the inverse hold flux 𝒰(y) = a₀y/(a₀ − \|y\|), \|y\| < a₀, inverts
  u(1 − μ(\|u\|/a₀)) = y (residual 0); (b) 𝒰′(y) = (1 + \|𝒰\|/a₀)² = M_L (residual 0); (c) before the first crossing each
  label obeys ẍ = −K[Σ_b(<x) − Σ_b,tot/2] − K S(q) + 𝒰(K S(q)) (+ the stiffness term on Θ = 1), consistent with the EL
  equations of `L1` and Gauss's law (residual 0); (d) J̈ = −Kρ_b(x)J + Kρ_τ0(q)(M_L(q) − 1) on Θ = 0 (residual 0).
- **F2 a cold stream crossing a sheet (the 1D point mass).** Closed form, checked against the explicit trajectory map:
  zero charge (the mimetic limit, X-D2): J = 1 − KΣ_bτ/\|w\|, fold at τ_f = \|w\|/(KΣ_b) < τ_turn = 2τ_f for every
  \|w\| < ∞ and Σ_b > 0. Charged: the exact fold condition; ρ_τ0 < 0 folds for every initial datum.
- **F3 phase mixing of held oscillations (planar).** Exact ξ̈ = −K[Σ_b(<q + ξ) − Σ_b(<q)]; linear J(q, t) and the fold time
  bound for ∂_qω ≠ 0 (Dawson-type).
- **F4 spherical shells.** Exact shell equation r̈ = −G(M_b + m)/r² + 𝒰(Gm/r²) from the spherical hold law and Poisson
  (residual 0). (a) m = 0: r → 0 at t_ff = (π/2)√(q³/(2GM_b)) (closed form); (b) m < 0: reaches r = 0 or the flux cap with a
  diverging inward force within t ≤ t_ff (comparison); (c) m > 0: a wall at r_w = √(Gm/a₀) excludes hoop collapse; the
  held shells' radial frequency ω²(q) is derived, and shell crossing by phase mixing follows iff dω/dq ≠ 0.
- **F5 pressure.** (a) Genuine nonlinearity (p″(τ_s) ≠ 0 in mass coordinates) for the stiffness p = (γ_L/2)ρ², the K(Q)
  limit p = Kρ²/(2μ_K²), an isothermal p = c²ρ; linear degeneracy of the Chaplygin p = −A/ρ. (b) The cold-fold depth reached
  before a γ = 2 pressure acts: J_* = 1/(1 + 𝓜²) (energy integral). (c) Numbers, both footings: 𝓜 = w/c₀, c₀² = γ_Lρ_ph,
  ρ_ph the AQUAL phantom of a 6e10 M☉ point mass at the five fold locations, L★ = 21.682 / 22.849 pc, w = 68.75 and
  74.8 km/s. (d) K(Q): in P3's χ, ω² → Kρ_τ(M_θ − 1) independent of μ_K for k² ≫ M_θμ_K² (sympy limit); numbers
  q_K = √M_θ μ_K ℓ with M_θ = (1 + x)² (upper bracket), ℓ ∈ {11, 156} kpc, μ_K ∈ {0.1 (S4), 10 (BS cap)} Mpc⁻¹; and the
  condition under which the K(Q) pressure could prevent a fold, stated.

## 5. Frozen verdicts

**(i) Caustics in v3s's khronon dust.**
- **CAUSTICS GENERIC (shown analytically)** iff all of: F1 (a)–(d) residual 0; F2's zero-charge fold holds for all
  \|w\| < ∞, Σ_b > 0; soft labels (ρ_τ0 < 0) fold for every initial datum (F2) and soft spherical shells collapse in finite
  time (F4b); stiff labels fold either by F2's condition or by phase mixing (F3, F4c) for an open set of data; F5(a) finds
  the stiffness and K(Q) pressures genuinely nonlinear and F5(c) gives 𝓜 ≥ 10 at every fold location on both footings;
  F5(d) gives q_K < 1 at μ_K = 0.1 Mpc⁻¹ on both footings.
- **NOT GENERIC** iff a native term (self term, stiffness, K(Q)) is shown to prevent both J → 0 and gradient blow-up for
  every datum in the X8/X10 regime.
- **UNDECIDED** otherwise.

**(ii) Completions.** A class "removes the fold" iff its FT is PASS-LIT, PASS-CONSTRUCT, or COND with the §3 window met.
It is "compatible" iff P1, P2, P4, P5, P6 are PASS or PASS-WITH-BOUND.
- **A ZERO-CONSTANT COMPLETION EXISTS (name it)** iff some class with no new constant (SC empty) removes the fold and is
  compatible.
- **EVERY COMPLETION NEEDS A NEW SCALE** iff no zero-constant class qualifies, but at least one class with a new constant
  removes the fold and is compatible for some value of that constant.
- **NO COMPLETION COMPATIBLE WITH v3s's PASSES** iff no class removes the fold and is compatible, at any value of its
  constants.
- **UNDECIDED** iff a check needed for one of these lines cannot be completed.

## 6. Checks, MUTATE, outputs

- Checks with explicit pass lines: R0 (X3 B1-S reproduced), R1 (X3 B2-S c² reproduced), F1a–F1d, F2, F3, F4a–F4c, F5a–F5d,
  and per class P1–P6 / FT / SC. The script exits 0 iff every check that is required to pass passes.
- **MUTATE** (`X14_MUTATE=1`), all at once: (m1) 𝒰(y) → y (MOND removed from the self term) — F1b must FAIL; (m2) β → −β
  (B < 0) — C1's P6(a) must FAIL; (m3) the sheet's impulse sign flipped (repulsive sheet) — F2 must FAIL; (m4) C1's term
  removed (B = 0) — C1's FT must FAIL (n = 0 on Θ = 0). Each of these four must fail.
- Outputs: `x14_caustic_completion.out`, `x14_caustic_completion_results.json` and their `_MUTATE` twins. README with the
  verdicts, derivations (JSON keys), every amendment labelled PRE-RESULT or POST-RESULT, and "what this does not show".
- Git: pathspec commits of this lane only; never push; no rebase or amend.
