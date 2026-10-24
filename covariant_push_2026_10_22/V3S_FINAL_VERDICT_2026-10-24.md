# v3s: final verdict (2026-10-24)

This document closes the v3s investigation. The theory is frozen as stated below. Every thread now has a final status: it
passes, it fails with a named mechanism, or it waits on dated data. No further lanes are opened on the v3s family unless a
new forced kernel appears; data due on fixed dates (§5) is scored against the sealed predictions as it arrives.

Freezing the investigation does not mean the theory passes; §3 says where it fails. κ = ½ FITTED. Footings 9.3603e-11 /
1.1312e-10 m/s², never pooled. No dark-matter particle. Nothing here says the data favour the framework. Full derivations,
equations and Lean names: `V3_FULL_PICTURE.md`. Every explanation the record has tried: `rebuild_2026_10_22/X0_explanation_map/MAP.md`.

## 1. The frozen theory

    S = (c³/16πG) ∫ √−g [ R − 2 J_x(Y) + 2 K(Q) ]  −  (γ_L/2) ∫ √−g [max(D_i P^i, 0)]²  +  S_m[g, matter]

    J_x = Λ − 2a₀²[y − ln(1 + y)],  y = √Y/a₀      (static limit: AQUAL, μ(x) = x/(1 + x))
    K(Q) = μ_K²(Q − 1)²,  μ_K < 0.1 Mpc⁻¹            (isolated-galaxy lensing bound, S4)
    γ_L = K L★²/2,  L★ ≥ 21.7 / 22.9 pc              (outer globulars, D10)
    a₀ = κ c √(G ρ_Λ) = c² √(Λ/32π),  κ = ½ FITTED

**Inputs:** κ (fitted), L★ (a lower bound only), the cold-dust abundance (an initial condition), and μ_K (bounded above
only). The β K² caustic completion (C1) is **not** part of the frozen theory; its status is in §4.

## 2. What passes (each result reproduced by the coordinator; Lean where named)

| test | result | evidence |
|---|---|---|
| The a₀-line and RAR form | forced: slope 1, intercept 0 | LEAN `EQB_A0LINE_uniqueness` |
| SPARC RAR | rms 0.054 / 0.054 dex, one Υ per galaxy, EFE solved for 109 (χ² line fails: conditional) | P4 |
| MeerKAT a₀ | +0.032 dex from SPARC's, same recipe | P4 |
| Isolated groups, isolated LG dwarfs | +0.010 / −0.010 dex; +0.06 / +0.02 ± 0.08 dex | P4, X1 |
| Tidal dwarfs, DF2/DF4 | Newtonian in their host, as predicted | U1 |
| Solar System (screened) | all 24 Cassini cells pass by 4.8e7–5.1e9 (the unscreened law fails) | C6, E2 |
| Gravitational waves, binary pulsars | c_T = c; ≤ 3.2e-14 of the double pulsar's precision | C8, P3 |
| Static black holes, neutron stars | shifts ≤ 2.9e-11 | P3 |
| Constraint algebra; saddle health | closes with 3 DOF; switched stiffness well-posed and statics unchanged (qualifiers in V3_FULL_PICTURE §4.7) | Codex review, X3, LEAN `switched_*` |

## 3. What fails, with the mechanism

**The one mechanism.** v3s has one cold field, and kinematics fix it to be the field that carries the law (α ≡ 1; X6,
LEAN `coupling_one_is_law`). It cannot be weightless in isolated galaxies, weigh in clusters and hosts, and grow like dust
from z ≈ 1100 all at once. A separate dust that does those things double-counts in galaxies: it is CDM under another name.

| failure | numbers | lanes | status |
|---|---|---|---|
| **Cluster cores** | 1.5–1.7 × the law in 0.3–1 Mpc; Z 4.5–5.5 all-source, 4.1–5.0 selection-corrected; no excess in the lightest third | F1, X2, X7, X11, X13 | FAIL (data robust; no μ_K fixes it, S4) |
| **Linear growth / CMB** | σ₈/σ₈,dust 0.003–0.005 at galaxy-allowed μ_K; nonlinear J_x does not restore it (ρ_NL ≈ −0.05, converged 128³–384³) | F3, X4, L1 | FAIL (512³ production pending, §5) |
| **No radiation era** | stiff a⁻⁶ partner; BBN needs μ_K ≥ 1.84e8 h/Mpc | Q6, Q7 | FAIL for the literal K |
| **Hosted dwarfs** | hosted ⇒ Newtonian (T3); six hosted sets disagree at ≥ 5σ (Antlia II 24σ, MW ultra-faints 12.6σ, …) | U1, X1 | FAIL |
| **Milky Way disc** | K_z(1.1 kpc) 92–97 vs 66.4 ± 2.2; outer slope excluded (Z −3.9 to −4.6) | P4, S3, X5 | FAIL (generic to the μ-law family) |
| **Caustics** | the single-stream khronon folds generically (analytic, X14; self-consistent axisymmetric, peer review cc727f275c); no completion without a new constant | X8, X10, X14 | STRUCTURAL GAP (§4) |

Three of these (clusters, the CMB's third peak, the Milky Way joint fit) are generic to every MOND-class theory: no
rule-compatible framework in the literature claims a clean pass (MAP §1).

## 4. The caustic completion (β K², C1): final status

| test | result | lane |
|---|---|---|
| Unique survivor of nine completion classes | yes; window β ∈ [2.0e-6 / 2.2e-6, 1.0e-5] at μ_K = 0.1 Mpc⁻¹ | X14 |
| Preferred-frame PPN | PASS: α₁ = α₂ = 0 at PPN order for every β; residuals ≤ 3.6e-10 | X15 |
| Binary pulsars | PASS on a condition: |s₁ − s₂| < 7e-7 (J0737), strong-field sensitivity uncomputed | X16 |
| Galaxy/cluster selector | NO (WRONG SIGN): inert in statics, wrong mass ordering in motion | X17 |
| Galaxy dynamics | works only for motion slower than c_A (160–770 km/s at the window top) | X15, X17 |
| Linear growth on forest scales | overshoots at k ≳ 1–3 h/Mpc for every β (linear) | X17 |
| Forest after saturation | **UNDECIDED** under the frozen rule: the linear khronon ODE breaks X14's flux cap at early times (last at z ≈ 200–500, even at β = 0), so it is outside its own validity. Ignoring the cap, the forest fails in 80/80 cells and no β puts both σ₈ and the forest inside the lines. Deciding it needs a nonlinear code started from a cap-consistent state | X18 (71e86472ea / c9832d656f; coordinator rerun in progress, 96 min) |

C1 cures a health problem. It does not touch the mechanism in §3. Every test that could be graded passes or is conditional; the one test X18 could not grade (the forest) fails in every cell once the cap is ignored.

## 5. What can still change the verdict (dated, sealed in advance)

| data | date | sealed prediction |
|---|---|---|
| ALMA U4 / GS4 | 2026-11-06 / 11-28 | addendum F |
| Gaia DR4: wide binaries, MW | 2026-12-02 | `SEALED_V3_MW_DR4.json` (S3), C6 |
| L1 512³ production (only rung KiDS can score) | in the compute queue | the converged ladder says ρ_NL ≈ −0.05: it does not restore growth |

## 6. The verdict

- **As a galaxy-scale law, v3s is complete and passes:** the a₀-line, SPARC, isolated systems and Solar-System screening,
  with a well-posed covariant action.
- **As a theory of gravity and cosmology, v3s fails:** clusters, growth/CMB, the radiation era, hosted dwarfs and the Milky
  Way disc. Most of these follow from one mechanism (α ≡ 1, one field).
- **What a successor needs:** a gravitating cold sector that clusters like dust from z ≈ 1100, weighs in hosts and clusters,
  and adds nothing in isolated galaxies. That needs a selector between galaxy and cluster scales. Nothing in the record
  provides one: density-keyed pressure is excluded by the μ-pincer, and C1's acceleration-keyed sound speed is inert in
  statics (X17).
