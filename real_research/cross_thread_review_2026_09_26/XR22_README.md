# XR22 — the chain's law for wide binaries, and what the frozen Gaia DR4 pre-registration can say about it

The question: what does the derivation chain's current law predict for wide binaries, and does the frozen Gaia DR4
pre-registration (data release 2026-12-02) still test it?

At z = 0 the chain's law is FP7's two-field AQUAL with J_P2 and a heat filter of length ξ, applied to both the source and
the output (FP7 A1b: the double filter is forced). FP14 leaves ξ as the gravity core's one knob, bounded to
[0.0243 / 0.0268 pc, ~100 pc]. FP17 finds no screening without it. Wide binaries at 1–30 kAU straddle ξ: 5 kAU is 0.024 pc.

Scripts (each writes its own `.out`, `_MUTATE.out`, `_results[_MUTATE].json`):
- `XR22_force_law.py`: the force law, solved in 3-D, with its controls.
- `XR22_prereg_statistic.py`: the force law put through the pre-registration's own estimator.
- `XR22_common.py`: the shared solvers and the read-only access to the pre-registration's machinery.

Nothing outside this folder was written. `prep_2026/gaia_dr4_prep/` was only read: its pipeline is exec'd from source, and
no bytecode is written. **κ = ½ stays fitted (Z = 5.7888). ξ is a free knob that no chain link fixes.**

## The answer

**1. Per pair, the chain boosts a wide binary only beyond s ≈ 2ξ.**
- At the Solar-System floor (ξ = 0.0243 pc = 5.0 kAU, canonical), γ_v rises from 1.001 at 3 kAU to 1.026 at 10 kAU and
  1.060 at 20 kAU. It saturates at 1.064 (alt floor: 1.083).
- The saturated value is the chain's unfiltered external-field-effect (EFE) tensor, averaged over directions:
  B∥ = 1.297, B⊥ = 1.101, sphere average 1.131 (canonical, at the pre-registration's primary field 1.778 × 10⁻¹⁰ m s⁻²).
- The half-way point sits at s½ = 2.2–2.4 ξ for 1–2 M☉, nearly mass-independent.
- The frozen record's banked "framework-as-MG" number 1.1389 is √B∥ of this same law: the parallel direction only (K1).

**2. Under the frozen statistic the chain predicts a ceiling, not a point.**
- **γ̂ = 1.0725 (canonical) / 1.0900 (alt) at the floor.** It falls to 1.040 / 1.0525 at ξ = 0.05 pc, 1.0125 / 1.015 at
  0.1 pc, and 1.000 for ξ ≥ 0.3 pc.
- The two estimator paths agree to one grid step (0.0025–0.005). The nuisance κ stays inside the frozen window
  (0.984–1.000).

**3. Where it lands.**
- At the canonical floor, 1.0725 is 2.6 σ_tot above Newton and 3.2 σ_tot below Arm A's floor (1.1614). That is the row
  "1.056–1.084: Arm A disfavored; Newton disfavored at 2–3 σ_tot".
- At the alt floor, 1.0900 falls in the row "1.084–1.101: Arm B killed from above".
- For ξ = 0.04–0.10 pc it falls in "1.007–1.056"; for ξ ≥ 0.15 pc it is Newton-side.

**4. The frozen pre-registration tests the chain only partly.**
- **It can kill the chain from above.** A DR4 γ̂ more than 3 σ_tot above the chain's ceiling (≳ 1.157 canonical,
  ≳ 1.174 alt) excludes it at every allowed ξ. An Arm-A-band result would do that.
- **It cannot confirm the chain or fix ξ.**
  - A Newtonian result only bounds ξ from below: ξ > 0.036 pc (canonical) or > 0.047 pc (alt) at 2 σ_tot. In the
    infinite-N limit, where only σ_sys = 0.02 remains, the bound is 0.050 / 0.060 pc. Either way the chain stays alive,
    because ξ can grow.
  - A result between 1.00 and 1.07 maps onto a broad range of ξ.
- **The frozen rows carry no reading for this law.** Arm A has no filter. Arm B is a different structure (carrier plus
  biharmonic cone, ξ ≥ 4 pc).
- To score the chain as the chain, an amendment would be needed. It would register the ceiling (1.0725 / 1.0900 at the
  primary field), its ξ reading, and, for ξ, a separation-resolved statistic. **The author decides.** Nothing was
  filed here.

**5. DR4's precision on ξ.**
- **The frozen number is a poor ξ-meter.** At the floor, dγ̂/d ln ξ = −0.036 (canonical), so σ(ln ξ) ≈ 0.8 with σ_tot
  (0.54 with σ_fit alone): ξ to about a factor of 2. Above ~0.1 pc it gives a lower bound only.
- **So DR4, scored as frozen, cannot fix ξ the way κ is fitted.**
- **A separation-resolved statistic could**, if ξ is small. Take the median ṽ in bins of s_proj at N = 30,000, counting
  statistical error only:

  | ξ | σ(ln ξ), canonical | σ(ln ξ), alt |
  |---|---|---|
  | ≤ 0.04 pc | 0.20 | 0.15–0.16 |
  | 0.05 pc | 0.23 | 0.17 |
  | 0.07 pc | 0.32 | 0.24 |
  | 0.10 pc | 0.54 | 0.44 |

- **Which separations discriminate ξ best:** s_proj = 5–30 kAU carries 91% of the information. The 7–15 kAU bins carry
  66% of it at the floor, and the weight moves to 20–30 kAU as ξ grows.
- **The systematic to beat:** hidden triples also inflate v at wide separations. They could mimic the transition.

**6. BDEF's Riemann-coupled Galileon (FP17's variant): an ESTIMATE, not adopted.**
- Its static-gradient c_T and its stability are open (FP17).
- It is carried in FP17's own spherical reduction onto the unfiltered EFE response. The reduction is ambiguous around
  the Galactic field: two readings × two stiffnesses bracket it.
- **γ̂ spans 1.000–1.085** (canonical) for k^(1/4) ∈ [104, 407] kpc. The heat filter spans 1.000–1.0725, so the ranges
  overlap and **the frozen number cannot tell them apart.**
- Its screening radius grows as M^(1/3); the heat filter's transition is mass-independent. Even so, at matched γ̂ a
  separation × mass resolved statistic separates them by **at most 0.85 σ** at N = 30,000.
- **DR4 does not separate the heat filter from the Galileon.**
- FP17's own r_E (0.035–0.087 pc) is reproduced exactly in FP17's convention (the Galactic field fed to P2 as Newtonian).
  In FP7's convention (the field as observed) it is 6–12% larger. Flagged for FP17's owner, not edited.

**7. A blind spot of the frozen estimator (flagged for the pre-registration's owner, read-only).**
- The anchored κ absorbs any boost that is the same at every acceleration. The ξ → 0 linear kernel (y-flat) returns
  γ̂ ≈ 1.00 with κ = 1.06–1.09: "systematic-limited, no verdict".
- The chain's filtered law is not y-flat, so its numbers are unaffected. Any law with a boost in the anchor bins
  (log y ≥ 0.5) would be.

## The per-pair curve, γ_v(s) = √⟨B⟩ (M = 1 M☉, the pre-registration's primary field)

The orientation average is over the field direction. The last column is 120 kAU, where every row except ξ = 0.2 pc has
saturated.

| law | ξ or k | 3 | 5 | 7 | 10 | 15 | 20 | 30 | 60 | 120 kAU |
|---|---|---|---|---|---|---|---|---|---|---|
| heat filter, canonical | floor 0.0243 pc | 1.0012 | 1.0049 | 1.0117 | 1.0261 | 1.0486 | 1.0595 | 1.0630 | 1.0635 | 1.0637 |
| heat filter, canonical | 0.05 pc | 1.0001 | 1.0007 | 1.0018 | 1.0048 | 1.0138 | 1.0259 | 1.0486 | 1.0634 | 1.0636 |
| heat filter, canonical | 0.10 pc | 1.0000 | 1.0001 | 1.0002 | 1.0007 | 1.0022 | 1.0049 | 1.0138 | 1.0487 | 1.0635 |
| heat filter, canonical | 0.20 pc | 1.0000 | 1.0000 | 1.0000 | 1.0001 | 1.0003 | 1.0007 | 1.0022 | 1.0138 | 1.0487 |
| heat filter, alt | floor 0.0268 pc | 1.0012 | 1.0050 | 1.0123 | 1.0285 | 1.0574 | 1.0748 | 1.0824 | 1.0831 | 1.0833 |
| Galileon, canonical (estimate) | k^(1/4) = 104 kpc, FP17 reading | 1.000–1.004 | 1.002–1.016 | 1.006–1.034 | 1.015–1.055 | 1.037–1.063 | 1.054–1.064 | 1.063–1.064 | 1.064 | 1.064 |

Each of the Galileon's cells spans the two stiffnesses (μ_T, μ_L); lane 2's `.out` has all readings, k and masses. At
2 M☉ the heat filter's curve sits lower by at most 0.004 (at 15 kAU). Parallel and perpendicular split and flip:
- perpendicular is larger up to s ≈ 20 kAU (the filter suppresses the parallel direction most);
- parallel is larger from 30 kAU on (the unfiltered tensor). At the canonical floor the flip falls between 20 and 30 kAU.

The sample-level projected split (Amendment 2(e)) nearly cancels: +0.0025 (canonical), +0.07 σ at N = 30,000.

## γ̂ under the frozen statistic (PHYS path; REG in brackets where it differs)

| ξ [pc] | canonical γ̂ | (γ̂ − 1)/σ_tot | alt γ̂ | (γ̂ − 1)/σ_tot |
|---|---|---|---|---|
| floor (0.0243 / 0.0268) | **1.0725** | 2.59 | **1.0900** | 3.21 |
| 0.03 | 1.0650 | 2.32 | 1.0875 (1.0850) | 3.12 |
| 0.04 | 1.0500 | 1.79 | 1.0675 (1.0650) | 2.41 |
| 0.05 | 1.0400 (1.0375) | 1.43 | 1.0525 (1.0475) | 1.87 |
| 0.07 | 1.0250 (1.0200) | 0.89 | 1.0300 (1.0275) | 1.07 |
| 0.10 | 1.0125 (1.0075) | 0.45 | 1.0150 (1.0125) | 0.54 |
| 0.15 | 1.0050 (1.0025) | 0.18 | 1.0050 | 0.18 |
| 0.20 | 1.0025 (1.0000) | 0.09 | 1.0025 | 0.09 |
| ≥ 0.3 (to 100) | 1.0000 | 0 | 1.0000 | 0 |

The ceiling depends on the Galactic field (REG path, canonical floor):
- 1.0725 at the pre-registration's primary field, 1.778 × 10⁻¹⁰ m s⁻²;
- 1.0575 at its alt field, 2.078 × 10⁻¹⁰;
- 1.0500 at the chain's own field, 2.32 × 10⁻¹⁰ (FP7).

The pre-registration's primary field decides, as its own text says.

**Two paths from force law to γ̂**, both through the frozen estimator's functions:
- **REG** is the path Amendments 11–12 register for coherence-length arms (g03y / L47), mirrored line by line. It
  reproduces Amendment 11(b)'s 1.0450 / 1.0300 exactly.
- **PHYS** uses the same population and model. Each pair is boosted at its true mass, true 3-D separation (1.5–120 kAU)
  and its own angle to an isotropic field direction.

## Checks

| script | main | MUTATE |
|---|---|---|
| `XR22_force_law.py` | 19/21, **0 load-bearing failures, rc = 0**. The two FAILs are reported hypotheses, kept as run: H3 (the nonlinear correction reaches −31% of B − 1 where B − 1 ≈ 10⁻³, at 3 kAU) and H4 (the perpendicular boost alone overshoots its unfiltered value near s ~ 2–4 ξ, so it is not monotone in ξ). | 4/6, **rc = 1**. The output leg of the double filter is dropped: K4 (3-D linear response 1.0949 vs the chain's kernel 1.0520) and K5 (3-D vs the independent 2-D solver, off by up to 1.7 × 10⁻²) fail. |
| `XR22_prereg_statistic.py` | 12/16, **0 load-bearing failures, rc = 0**. FAILs are reported hypotheses, kept as run: H1 (the floor γ̂ 1.0725 lies above the declared [1.007, 1.056]); H3 (the alt floor 1.0900 exceeds 1.084); H4 (a floor-ξ outcome is separable from Newton at 2 σ_tot); H10 (the split is +0.0025, not parallel-dominant). | 8/16, **rc = 1**. The filter is moved to ξ = 0 in the prediction path: L1 (the separation ratio 1.03 vs < 0.25) and L2 (γ̂ flat in ξ) fail. |

**Controls reproduced exactly.**
- The frozen section 1.1 numbers y_extN = 1.4647 / 1.1513, from the frozen pipeline's own function.
- The banked 1.1389 = √B∥.
- FP7's stiffnesses at 2.32 × 10⁻¹⁰ (0.4501, 4.507, 49.64).
- Amendment 11(b)'s 1.0450 / 1.0300 and g03h's 1.0325 / 1.0400 through the registered path. The cached estimator is
  bit-identical to the direct call.
- The frozen gate's own inject-1.00 recovery, 0.9850 ± 0.0137 (κ 1.0070) / 0.9900 ± 0.0125 (κ 1.0043), with seed
  20261216 and the 3,000,000-pair master.
- The population mirror is bit-identical to the frozen generator.

**Analytic limits.**
- **Deep-MOND two-body.** An independent 2-D FEM solver with μ = x reproduces Milgrom's exact force
  s F = (2/3)[M^1.5 − m₁^1.5 − m₂^1.5]:
  - ratio 1.0034 at ξ/s = 0.05 (1.0046 at q = 0.3);
  - 1.0014 at 0.025;
  - 1.0007 after Richardson extrapolation.
- **EFE-dominated linear regime.** The Schwinger kernel equals the analytic anisotropic-Coulomb tensor to 2 × 10⁻¹⁵ and
  quadrature to 4 × 10⁻¹¹. The 3-D solver's linear response extrapolates to it to 9 × 10⁻⁶ and 1.2 × 10⁻⁴.
- **ξ → 0.** The frozen record's P2 numbers above.

**Convergence.**
- 3-D vs the independent 2-D free-space solver, in the nonlinear regime at the floors: ≤ 1.4 × 10⁻⁶ in B.
- Refining h from ξ/2.5 to ξ/3.5, or growing the box from a 9 to a 13.5 r_M margin: ≤ 5.2 × 10⁻⁵.
- All 3,540 production solves converged (|R| < 10⁻⁸). Momentum is conserved to 2.6 × 10⁻⁷.
- Angular interpolation: ≤ 3.9 × 10⁻⁴. The nonlinear correction at ξ = 0.3 pc: 1.2 × 10⁻⁶, so the exact linear kernel is
  used above it.

## Pre-declaration and disclosures

- **Hypotheses were written into each docstring before that script's first full run.** They are reported checks and fall
  as they fall. Only controls and the prediction-path checks (L1, L2) are load-bearing.
- **Exploratory runs, disclosed.**
  - A one-point solver prototype and a linear-kernel preview informed lane 1's H1–H3 and H5.
  - A development dry run of each lane (`XR22_DRYRUN=1`: the linear kernel standing in for every solve; outputs outside
    the repository) exercised the bookkeeping before the full runs.
  - Lane 1's dry run showed that H4 fails for the perpendicular orientation. H4 was kept as declared. **H4b**, on the
    orientation average, was added after that dry run and is labelled as such.
  - Lane 2's dry run showed the estimator's linear-grade response (≈ 1.0775 at the floor) after its hypotheses were
    written. None was changed, and H1, H3, H4 and H10 fell as written.
- **Two lane-2 runs were stopped and repeated.**
  - The first MUTATE run crashed on a printout (a division by zero when the boost does not depend on ξ). The crash was a
    code fault, not a check result. The guard was fixed and MUTATE rerun.
  - Then V0's printout was relabelled; the physics was unchanged. MUTATE and main were rerun in that order.
  - Lane 1's MUTATE ran before a one-line change (the worker-count setting), which its path never reaches.
  - A function (not used by lane 1) was added to `XR22_common.py` while lane 1's main run was in progress.
- **Grades.**
  - Nonlinear two-body 3-D solves for ξ ≤ 0.2 pc; the exact linear kernel above.
  - The ξ → 0 row (V0) is the linear kernel only. It is **not** the unfiltered law's γ̂: that law returns to Newton at
    high y, and the Solar System excludes it (FP7 A4). Its γ̂ ≈ 1.00 comes from κ absorbing a y-flat boost.
  - The Galileon is an estimate in FP17's spherical reduction, not a solve of its field equation.
- **Mass ratio.** The force tables are equal-mass. A q = 0.3 pair has up to 10.5% less B − 1 when its separation is
  parallel to the field, and ≤ 0.2% less when perpendicular (K7b). Its effect on γ̂ was not put through the estimator; a
  rough scaling from K7b's rows (an estimate, not a computed number) puts it at −0.001 to −0.002, below the 0.0025 grid
  step. It runs against the chain.
- **Mirrored conventions.** The REG path's conventions are mirrored, not repaired: the 3-point orientation rule, clipping
  to 1–2 M☉ and 3–30 kAU, r₃d rebuilt from the noisy M_obs, and velocity scaling at fixed orbit. PHYS repairs all but
  the last. The Galactic field direction is isotropic per pair.
- **Budget.** Lane 1 used 3 single-threaded workers (≤ 4 threads, ~8 GB). A development run that pushed the combined
  total past 12 GB was stopped.
- **Not computed.**
  - Self-consistent orbits.
  - Contamination by hidden triples.
  - ν_mono. The chain's FP7 root carries J_P2, so P2 is scored.
  - The Galileon's own field equation.

## How it was computed

**The law.**

    g = g_N + S∇φ,  ∇·[μ_s(|∇φ|/a₀)∇φ] = 4πG Sρ,  μ_s(x) = x/(1 − 2x),  S = e^{ξ²∇²/2}

- The Galaxy is the scalar's uniform background gradient x_e, with μ_s(x_e)x_e = η, the P2 inversion of the observed
  field.
- FP13's separator drops out locally. Its yield switch is max(0, 2q) = 0 today, and its band-pass leg L(0) = 2.88 Mpc
  moves a pair's force by ~10⁻²². Both were checked in FP13's committed results.
- FP14's α_c renormalises G by ≤ 1.6 × 10⁻⁹. The pair is quasi-static (retardation 8 × 10⁻⁷).

**Solvers.**
1. The exact double-filtered linear response, by the Schwinger integral.
2. A 3-D periodic pseudo-spectral Newton–Krylov solver on the convex energy. The preconditioner is the far-field operator,
   inverted by FFT. A barrier line search keeps |∇φ| < a₀/2, and a linear image correction removes the periodic images.
3. An independent axisymmetric free-space P1-FEM Newton solver.

**The plug-in.** The 3-D solver takes a pluggable screening term c(r)G(|∇φ|) (K8), per the coordinator's request.

**Production.** 3,540 solves:
- M = 0.6–2.5 M☉, s = 1.5–120 kAU, θ = 0/45/90°;
- ξ = the floor to 0.2 pc, both footings;
- the registered grid at the other two Galactic fields.

## Reproduction

From the repository root, in this order:
```
MUTATE=1 python3 real_research/cross_thread_review_2026_09_26/XR22_force_law.py
python3 real_research/cross_thread_review_2026_09_26/XR22_force_law.py
MUTATE=1 python3 real_research/cross_thread_review_2026_09_26/XR22_prereg_statistic.py
python3 real_research/cross_thread_review_2026_09_26/XR22_prereg_statistic.py
```
Wall time on 3–4 single-threaded workers:

| run | wall time |
|---|---|
| lane 1 MUTATE | 3 min |
| lane 1 main | 36 min (production 33 min) |
| lane 2 MUTATE | 7.5 min |
| lane 2 main | 8 min |

The whole lane takes about 55 min. Peak memory is about 8 GB for lane 1 with 3 workers (about 10 GB with 4) and 5 GB for
lane 2; run them one at a time. `XR22_NPROC` sets lane 1's worker count (default 4).
