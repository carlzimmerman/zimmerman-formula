# M5_equilibrium_law: frozen criteria (committed alone, with the assumption ledger, before any script or number)

Question: can the galaxy law be the **equilibrium (attractor)** of a cold-energy medium that **self-gravitates normally
everywhere** (no hold, no cancellation), with the medium's total profile equal to the law's phantom density, so that it
clumps, binds and grows like dust where equilibrium is not reached? κ = ½ FITTED. Footings canonical 9.3603e-11 / alt
1.1312e-10 m s⁻², never pooled. Cold energy is a medium of real rest mass, never a particle. No new fitted constant:
anything new must be built from a₀, G, c, Λ, L★. Observables from an action. Not "theory closed". Nothing here may say
the data favour the framework.

**Blindness disclosure.** Not blind. Before freezing I read: THEORY_V3_DRAFT rows U1, O1, PH1, TM1, Y1, Z1/ZT, V1;
Z2's README table (ISO / MOND / V3S clean medians and slopes); P4's T1 numbers (0.054 / 0.054 dex) and T5 (TDGs);
F1's A_MID table; F3's verdict table; CFG660 (field-aligned stress: law = exact spherical equilibrium, isotropic
EXCLUDED, NOT KINETIC, ILL-POSED along the field); CFG638 (bath fluid equations); CFG121 (dipolar door, scoped no-go);
CFG122 (superfluid door, scoped no-go); CFG870 / CFG876 (cored component; universal floor BROKEN). Rows R1, R3, R5
re-use verified pipelines whose numbers I have seen. Rows R2, R4, R6 and checks S2, S4–S6, N1 are new and unseen.

Before freezing I worked out (by hand, not yet checked) the expected shape of S2 (uniqueness forces a density-blind stress)
and S5 (deep-regime cancellation). They are stated here as hypotheses H1–H3 so that a wrong expectation is visible.

## 0. Candidates (each: action, equilibrium + uniqueness, linear stability, relaxation time, far-from-equilibrium limit)

- **(a) acceleration-dependent equation of state / stress.** Medium stress Π(ρ_c, ∇Φ) (isotropic or field-aligned);
  hydrostatic balance ∂_jΠ_ij = ρ_c ∂_iΦ with ∇²Φ = 4πG(ρ_b + ρ_c).
- **(b) internal polarisation relaxing to align with the field** (mass self-gravitates; the polarisation exerts the
  internal force). Two sub-cases: polarisation per unit mass (P = ρ_c p) and per unit volume; and the BLT reading where
  the polarisation charge also gravitates.
- **(c) entropy / temperature attractor**: isothermal (or locally thermal) medium with a bath tied to a₀ (CFG638), or a
  local temperature σ²(g).
- **(d) own: explicit relaxation drift** toward a baryon-defined target (the record's settling class, CFG541/544/638)
  written as the attractor it is.
- **(e) own: collisionless relaxation** of a dust medium around baryons (no internal force).
- **(f) own: (a) regularised by a stiffness built from L★** (a Bohm-type gradient pressure with D = L★^{3/2} a₀^{1/2},
  or a compressional c² = g L★). Constructed here to test whether an allowed scale can cure (a)'s dynamics.

Hypotheses (expectations, frozen so they can be wrong): **H1** exact equilibrium for every baryon profile forces a
stress whose along-field part does not respond to ρ_c; **H2** in the deep regime (g ≪ a₀) that stress is minus the
gravitational Maxwell stress, so the medium's nonlinear self-gravity cancels (the hold returns); **H3** any along-field
stiffness c∥² trades law error against convective amplification with product of order ln(density contrast).

## 1. Checks (the script exits 0 only if all pass; implementation / identity / reproduction checks, not verdicts)

| id | check | line |
|---|---|---|
| S1 | sympy, 3D, generic quartic Φ(x,y,z): Π_ij = (1/4πG)[χ ∂_iΦ∂_jΦ − K(s) δ_ij], s = \|∇Φ\|², K′(s) = χ/2, χ = 1 − μ(√s/a₀), μ = x/(1+x), satisfies ∂_jΠ_ij − ρ_ph ∂_iΦ = 0 with ρ_ph = ∇·(χ∇Φ)/4πG (= AQUAL phantom) | residual ≤ 1e-12 at 20 random points (exact symbolic where feasible) |
| S2 | sympy, spherical jets (r, g, g′, g″ independent): field-aligned Π with P∥ = A(ρ,g), P⊥ = B(ρ,g); requiring radial balance on the law for every baryon profile forces ∂A/∂ρ = 0 and ∂B/∂ρ = 0 and fixes A_g, B − A uniquely; the 3D analogue with A(ρ,s)δ + B(ρ,s)∂Φ∂Φ forces A_ρ = B_ρ = 0, B = χ/4πG, A = −K/4πG + const | exact |
| S3 | sympy: the spherical balance with S2's stress integrates exactly to μ(g/a₀) g = G M_b/r² + C/r², C = 0 by regularity (unique equilibrium) | exact |
| S4 | sympy: Lagrangian (Cowling) perturbation of a medium supported by a ρ-blind stress has principal part ξ̈ = g ∂ξ (first order in space) → s² = i k g (|Re s| ∝ √k, Hadamard ill-posed); with an added compressional c²: s² = −c²k² + i k g | exact |
| S5 | sympy: force density on the medium = ∂_jΠ_ij − ρ_c ∂_iΦ = (ρ_ph[Φ] − ρ_c)∂_iΦ = (ρ_b − ∇·(μ∇Φ)/4πG)∂_iΦ (identity); with the peculiar potential on FRW the medium's per-mass force is −[(ρ̄ − δρ_b)/(ρ̄ + δρ_c)]∇δΦ + O(g/a₀) | exact |
| S6 | sympy: linearised on FRW (peculiar Φ, Π quadratic in ∇δΦ), δ̈ + 2Hδ̇ = 4πGρ̄δ (dust) | exact |
| N1 | spherical top-hat in EdS: dust control gives linear δ at collapse 1.686 ± 0.01 | as stated |
| N2 | 1D operators on a Dirichlet interval (finite differences, N = 200/400/800): L = c²∂² + g∂ has max Re s ≤ 1e-6 ω_ref (stable control); L = g∂ has max Re s growing with N (ill-posed) | as stated |
| P4a | own SPARC loader + algebraic AQUAL law (μ = x/(1+x)), per-galaxy Υ on P4's grid and rms rule, reproduces P4's iso_perUps rms and median Υ, both footings | ≤ 2e-4 dex; Υ median equal |
| P4c | numerical integration of S3's ODE (g′ from the stress balance) on each SPARC galaxy's own baryons at its fitted Υ equals the algebraic law | max \|Δ log g\| ≤ 1e-5 dex |
| Z2a | from Z2's committed per-system CSV (read-only): clean (C1–C4) plain median of Delta_ISO and Delta_MOND, both footings | within 0.05 of Z2's bootstrap medians (+0.465 / +0.424; +0.693 / +0.711) |
| Z2b | predicted host-field slope (OLS on log x_e with M_V, 45 systems, canonical) of a flavor = slope of (Delta_V3D − Delta_flavor); data slope = slope of Delta_V3D | MOND −0.76 ± 0.05, V3S −0.55 ± 0.05, data −0.05 ± 0.05 |

`--mutate` plants: **M1** stress built with the standard μ = x/√(1+x²) while ρ_ph uses x/(1+x) → S1 must fail; **M2**
anisotropy dropped (isotropic P∥ = P⊥) → S3 must fail; **M3** the deep factor applied to the background force in N1 →
dust control fails; **M4** SPARC law with standard μ → P4a must fail; **M5** Delta_ISO shifted by +0.10 → Z2a must fail.
MUTATE must exit non-zero; outputs written with `_MUTATE` names.

## 2. Rows and frozen class rules (both footings where a₀ enters; a row's class is the worse footing)

- **R1 SPARC tightness, assuming equilibrium reached.** If S1–S3 hold, the equilibrium is AQUAL on the baryons and the
  row is P4a's rms. PASS if rms ≤ 0.110 dex and median Υ in 0.50–0.80 (P4's line); else CONDITIONAL (P4's own rule).
- **R2 attractor / relaxation check per SPARC galaxy (new).** At each galaxy's fitted Υ: phantom profile ρ_c(r) from the
  law; an along-field stiffness with support fraction δ (= |p′|/ρ_c g) shifts the law by Δ log g from ΔM = δ M_c; δ★ is the
  largest uniform δ with weighted rms(Δ log g) ≤ ε, ε = 0.02 dex (primary) and 0.054 dex (reported). Convective
  amplification ln A = TV(ln ρ_c)/(2δ★) (WKB, S4's s² = −c²k² + ikg); relaxation time t_rel = ∫dr/c to r_last vs
  t_dyn = r_last/V_last and 1/H₀ (H₀ 67.9). **PASS** (attractor) if ln A ≤ 3 and t_rel ≤ min(10 t_dyn, 1/H₀) in ≥ 90 % of
  galaxies; **FAIL** if ln A > 10 in ≥ 50 %; else MARGINAL. Reported alongside: fraction of points with ρ_ph < 0 (a real
  medium cannot be negative), M_c(r_last)/M_b against 5.36 (ΛCDM-processed abundance, reported only), and the L★-Bohm
  variant's peak local growth rate (g²/D)^{1/3} × t_dyn.
- **R3 satellites (Z2's data).** Equilibrium relaxed inside the host → AQUAL + EFE (Z2's MOND flavor); medium kept from
  before infall, not re-relaxed → isolated AQUAL (ISO). Excess PASS if the clean median is within 2 sd of 0 and the
  M_V-controlled predicted slope is within 2 sd of the data's; else FAIL (ROBUST/NOT ROBUST as Z2).
- **R4 growth.** Linear: from S6 (σ₈/σ₈,dust = 1 exactly) → PASS at linear order. Nonlinear clumping (the premise
  "clumps and binds like dust"): N1 with the S5 deep-regime force; PASS if linear δ at collapse is within 10 % of 1.686;
  FAIL if > 1.3 × 1.686 or no collapse by a = 1e3 a_i·(collapse time of dust × 10).
- **R5 cluster terciles.** Derivable only if the cluster equilibrium is AQUAL (S1); then the row is F1's AQUAL A_MID
  (read, not recomputed): FAIL if F1's primary A_MID Z > +3 on both footings.
- **R6 TDGs.** Relaxed in host field → P4 T5 (FAIL as P4); medium-free (no capture) → U1 native PASS; the row is
  CONDITIONAL on the capture history unless the dynamics decides it.
- **(c) BTFR line.** A universal bath σ gives V_flat² = 2σ² for every galaxy; FAIL if the rms of log V_flat about its
  mean (SPARC, Vflat > 0) exceeds 3× the rms of the BTFR residual log(V_flat⁴/(G M_b a₀))/4 at the fitted Υ.

## 3. Verdict rules (per candidate)

- **VIABLE**: no new constant; unique baryon-fixed equilibrium (S2/S3 or equivalent); R2 PASS; R1, R3, R4, R6 PASS
  (R5 if derivable).
- **NO-GO**: a theorem (S-check) blocks (i) uniqueness, (ii) attractor / well-posedness, or (iii) dust-like clumping, with
  no allowed-scale escape (f tested); the block is named.
- **CONDITIONAL**: otherwise, with each postulate or hidden constant named.

Compute: `OMP_NUM_THREADS=1 nice -n 15`, < 1 GB, minutes. No downloads. Commits by explicit pathspec, this lane only.
Never push.
