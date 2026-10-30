# Brief for Argon: where route E stands and what to do next (2026-10-30)

This replaces ARGON_BRIEF_2026-10-29 and the status I gave you earlier. **That status was wrong in three places:**
- It presented X77's η as a native pass. X81 and CE1 showed that pass came from the resolution cut.
- It said clusters pass with the native branch. They don't: two core keys fail.
- It said GH2 had no result. It does.

Please discard anything you built on those three points.

## 1. Rules for your answer

**Standing rules**
- κ = ½ is FITTED. Never say "theory closed" or that the data favour the framework.
- Footings are never pooled: canonical a₀ = 9.3603e-11 m/s² (Σ_a0 = a₀/2πG = 106.85 M☉/pc²); alt a₀ = 1.1312e-10 m/s² (129.13 M☉/pc²).
- The name is "cold dark energy": a gravitating w ≈ 0 field component, never "cold dark matter" and never a particle.
- No ΛCDM inputs anywhere: no Planck 5.364, no f_b = 0.157, no borrowed c(M), no ΛCDM background.
- Criteria are frozen and committed alone before any script or number. A fail gets checked as hard as a win.

**What I can't use, based on your last rounds**
- A number back-solved from its target.
- Inputs chosen to reach a result. State where each input comes from.
- A closed-form result without a numerical check. Your r⁻⁹ᐟ⁴ boost came from 16/3 where the integral gives 8/3.
- Lean over integers or trivial algebra presented as physics certification.
- "Final theory", "Nobel" or "proves" language.
- Any idea in the closed list (section 5) unless you name what is new about it.

If you have no new mechanism or data for a question, say so. That is a useful answer.

## 2. The theory under test

**Route E, the current flagship.** Gravity is plain Newtonian. The a₀ law g = ν(g_N/a₀) g_N is emergent rather than fundamental. Each halo is cold dark energy with a cored profile:
- Core rule: ρ₀r₀ = max(Σ_a0, η Σ_coll(M)), with shape ρ = ρ₀(1+x²)^(−3/2), x = r/r₀. The shape is chosen, not derived.
- η = (4/(3 B_S(1))) c_f^(5/4), B_S(1) = 0.69707, derived from r⁻⁹ᐟ⁴ self-similar infall. η = 10.82 at c_f = 4, and c_f = 4 is an external input.
- Σ_coll(M), M☉/pc²: 3.83 at 10¹¹, 6.84 at 10¹², 11.95 at 10¹³, 20.48 at 10¹⁴, 34.71 at 10¹⁵ (X43, from the record's own P(k)). z_f: 1.137, 0.944, 0.751, 0.562, 0.385.
- Halo mass: fair share of the baryons inside the self-consistent turnaround radius (R_nat = 5.27), for clusters and for the galaxy lensing test; SPARC uses EM1's M200 relation.
- **Related line:** PAPER64's basin switch (a halo only above T ≈ 10^12.3 M☉ in basin mass) has a data-located T and no derived mechanism. CSM1 found no consistent single L. It is not the current flagship, but it is on record.

**Grader (X74):** SPARC line (median Υ ≥ 0.50, both backgrounds), 15 cluster keys with |Z| ≤ 2 in two h cells, groups. Plus separate tests: Milky Way (Eilers v_c = 229.1 ± 4.6 km/s, K_z, Ou), KiDS lensing bins 3–4, tSZ.

## 3. Results, best current numbers

### 3a. Core strength by configuration (canonical, cluster masses at ng 48)

| Configuration | η at 10¹² / 10¹³ / 10¹⁴ | SPARC Υ | Clusters | Grader |
|---|---|---|---|---|
| External c_f = 4 (X73) | 10.82 at all | passes | pass | **PASS**, fragile at s16 slope |
| Native at the ε cut (X77) | 20.83 / 13.79 / 14.39 | passes | knife edge | superseded by CE1 |
| **Converged native (X81/CE1)** | **25.94 / 17.67 / 16.91** | **0.48 FAIL** | **G-MID-T3 Z −2.30, G-IN-Mall Z −2.55, both too dense** | **FAIL** |
| Supernova softening only (SH1) | R 0.573–0.817 at 10¹², clusters native | 0.52–0.55 | same two keys fail | FAIL |
| Softening at all masses, R 0.685 (SH1) | 17.77 / 12.10 / 11.59 | 0.54 | pass | PASS, but cluster softening is assumed |
| Stipulated (CL5 Part B) | 21.2 / 14.3 / 14.3 | 0.52 | pass at f★ 0.034; G-IN-Mall OVER at 0.0615 | conditional |

- X81 finding: native zoom "cores" are NFW cusps seen through the softening cut. Their cusp fit gives the converged η. Removing the cut raises η 18–28 %.
- Alt fails the SPARC line in every row (Υ 0.41–0.47). X78 traces this to the a₀ law itself (law Υ 0.44); an Υ floor of 0.50 needs a₀ ≤ 9.95e-11.
- X76: letting c_f scatter per galaxy from native values worsens SPARC (P_line 0.001).

### 3b. Milky Way look-alikes (LS1, frozen; 18 SPARC galaxies, V_flat 200–250, Q ≤ 2, Inc ≥ 30)
Frozen at c_f = 4: SYSTEMATIC L★ DEFICIT on both footings: median Υ 0.71 / 0.65, ΔV at Υ 0.50 over 2–4 R_d −34.7 / −25.7 km/s. Control at V_flat 100–150: −6.4 / −0.8.

Canonical median Υ, ΔV at Υ 0.50 (columns after c_f 4 are reported post-result):

| V_flat | n | c_f 4 | η 21.2 / 14.3 / 14.3 | converged native | a₀ law |
|---|---|---|---|---|---|
| 100–150 | 23 | 0.74, −6.4 | 0.74, −6.4 | 0.71, −5.6 | 0.65, −6.8 |
| 150–200 | 25 | 0.58, −12.6 | 0.55, −6.4 | 0.49, +1.3 | 0.44, +5.2 |
| 200–250 | 18 | 0.71, −34.7 | 0.61, −18.6 | 0.57, −7.8 | 0.54, −12.5 |
| 250–400 | 10 | 0.82, −65.5 | 0.77, −57.9 | 0.73, −51.0 | 0.70, −40.0 |

**This is the new core tension.** The full SPARC sample needs η(10¹²) ≤ 21.2, yet the L★ analogs want more. The conflict is inside SPARC at 10¹². Softening clusters can't touch it. The 250–400 row is short for every model, so a fixed Υ 0.50 may be wrong there.

### 3c. Milky Way proper (X79, GD3)
| Halo | Best in-prior v_c | McMillan v_c | All four tests? |
|---|---|---|---|
| c_f 4 | 202.5 | 193.8 | no |
| X77 η | 209.1 | 200.1 | only R_d 1.93 kpc, outside Licquia & Newman |
| Converged η (×1.245) | 216.0 | 207.3 | no, about −2.8σ in priors |

Raising η further breaks K_z and the outer curve (η × 2 falls to V+K ONLY). Softening lowers v_c (SH1).

### 3d. KiDS lensing and the gas (GH1–GH7, X76, X78, TL1)
| Gas cut k (R_vir) | Route E χ² (canonical / alt) | Law χ² (canonical / alt) |
|---|---|---|
| 1, measured | 437.9 / 433.9 | **66.2 / 80.8** |
| 2 | 203.3 / 216.4 | 298.3 / 429.9 |
| 3, Zhang's closure | **140.6** / 178.3 | 757.8 / 1028.3 |
| 5 | 675.7 / 681.3 | 1913.7 / 2472.8 |

KiDS bins 3–4 flip at k* = 1.82 / 1.66. Alt law's best is 73.3 at F2's 0.5 M★ hot gas.

- **G09 centrals:** 50–300 kpc can't discriminate.
- **Satellites:** GH1 finds +0.78 is a method systematic; matched-host lensing gives Δ = +0.17 [+0.05, +0.28].
- **Softening:** doesn't change the lensing, which is a halo-mass deficit (SH1).
- **TL1, frozen:** r⁻⁹ᐟ⁴ tail outside r_f, fixed M(<r_ta), inner core identical: best 189.8 / 229.0: NO IMPROVEMENT. The mass moves past the window (300 kpc ΔΣ 8.67 → 6.99). A continuous variant reaches 121.9 only at post-hoc k = 4.5, beyond turnaround, with SPARC ungraded.

**Direct gas evidence**
- **GH5 (ACT y × 206k DESI centrals):** no tSZ detection (null p 0.41). Empirical errors, already corrected by 1.4 from eight null stacks: A(k=3) = −0.07 ± 0.39, 2.7σ from 1; A(k=1.8) ≈ 0.07 ± 0.5 (scaled), 1.8σ; A(k=1) = 0.39 ± 1.2, so even Zhang's gas inside R_vir isn't seen. Do not divide these again. Star-forming lenses stack negative, likely CIB over-subtraction; passive is the tier to trust. tSZ can't see cool gas.
- **GH4 (88k KiDS lenses):** NOT DECIDED (Δχ² +3.9 vs threshold 4).
- **GH7 (kSZ, sees any temperature):** VOID. Positive control S/N 3.81 < 4. A(1.8) 0.04 ± 0.08 frozen R, 0.07 ± 0.14 context R, with shuffle σ, is not a usable limit until the pipeline is validated.
- **GH6 (FRBs):** non-diagnostic; on the order of 1500–8000 FRBs are needed.

### 3e. Softening: can baryons do it by gravity alone?
- **BE1:** SPARC needs 1.7 % of supernova energy if it couples.
- **CM1:** measured gas, 40 cycles: R 0.932, need 0.817; 0.4 % of lift energy reaches the cold component.
- **CM2/CM3:** reaches only at coupling 1 with rare large bursts: 10 bursts R 0.573, 20 bursts 0.685. Coupling 0.3 misses (0.894, 0.956). Robust to seed and baryon fraction at coupling 1. Cadence and coupling aren't derived.
- **CL4 (clusters, to η 14.3, provisional inputs):** supernovae excluded (ε 6.71), infall excluded (10.5), black hole sufficient if coupled (0.075).
- **CL5, frozen:** black-hole-capped gas cycles at 10¹³ and 10¹⁴: NOT REACHED AT CEILING. Against a fairer post-result same-gas control, R is 0.91–0.95 with no build-up, against 0.81–0.85 needed. Even moving all the gas at 3× the black-hole energy gives 0.918. Spherical, prescribed histories, one seed.
- **BH1:** a peer lane on the same question with other geometries is still running; no result yet.

### 3f. The floor and dwarfs
- **Status:** Σ_a0 is empirical, not derived, and κ isn't derived.
- **X65–X67, X47:** local mechanisms all fail.
- **PC1:** floor halos have a ceiling, g ≤ 0.2545 a₀ (M₃D(<r) ≤ 1.599 Σ r²). J0946's dark perturber exceeds it (R 31/26 at 0.3 kpc).
- **MF1:** H₂ cooling gives lg M_f ≈ 6.0–6.6, near PC1's window, but canonical is NOT DIAGNOSTIC and M_f is not derived. Alt is z-dependent.
- **IC 1613:** fails, and the inclination rescue failed too.

## 4. Runs in progress
- **X48 A4:** 18 ng 64 zooms at 10¹³ and 10¹⁴, unfinished. Every cluster η above is ng 48 until they finish; A4 can move them. Automatic follow-ups: X72, X74, CE1_A4, then A5.
- **X80:** 24 zooms at 10¹⁰ and 10¹¹, queued behind A5. Your earlier formula is on record as an outside prediction, reported and not graded: R canonical 0.80 / 0.50, alt 0.66 / 0.41 at 10¹¹ / 10¹⁰, using c_f ∝ 1+z_f. X80's fit is cut-dependent, so a converged value needs reporting too. Its frozen ρ₀r₀ of 134.9 at 10¹² is the cut value.
- **PAPER65:** draft only. Nothing is deposited without the owner's go.

## 5. Closed: do not re-propose without something new
| Idea | Why closed |
|---|---|
| Adiabatic contraction for the MW or clusters | X39: SPARC Υ 0.39 canonical, 0.32 alt; clusters move +0.08 against +1.0 needed. Your 224 km/s used back-solved V_bar, f_b 0.157 and the cut 135 M☉/pc². |
| r⁻⁹ᐟ⁴ tail for lensing | TL1, and GC3/GX1 on clusters: fixes X-COP or lensing, not both. |
| Reshaping at fixed mass | X68: zero-sum, no root. |
| Correlated matter beyond r_ta | Under 1 M☉/pc² at 2 Mpc; wrong sign outside R. |
| Gated AQUAL pulls, tethers, phase-space and pressure floors, phantom tracking | X65–X67, X47, PS1/PS2, X65_X67_POSTMORTEM. |
| Soft floor, split Burkert, cored NFW | X69, X70_soft_floor_x0. |
| Cluster gas cycles at the black-hole cap | CL5. |
| Supernovae or infall for cluster cores | CL4. |
| Potential, σ, or acceleration keys for a switch | J1, X19: satellites are shallower than the Sun. |
| "κ derived" from 32π, DSF-21, SIS ratio | Restatements or posits. |
| c_f from (Δ_vir/Δ_ta)^(1/3) × 2 | Evaluates to 8.3, not 4. |

**Open in principle:** cool, unshocked gas beyond R_vir has mass for lensing and no tSZ signal. It has no quantitative test: your 0.40 cool fraction and R_sh 1.2 were chosen, and the same gas should appear in absorption lines. It doesn't fix route E's shape gap by itself.

## 6. The questions, in priority order

**Q1. The 10¹² tension.** The full SPARC sample needs η ≤ 21.2 and the L★ analogs want about 26. Which is it: a sample effect, a baryon-model effect (Υ varying with mass or bulge, disc thickness), real halo scatter that X76's result already limits, or a sign route E's mass dependence is wrong? Name one test on SPARC data.

**Q2. The missing mass at 100–500 kpc.** Rearranging doesn't work. Where could extra mass come from without a fit? Give the expected mass, its source, and a test on data that exists now, separate from k. Or argue that the deficit means halos aren't the answer at these masses.

**Q3. Clusters.** What lowers converged η by about 20 % at 10¹³–10¹⁴ besides gas cycles? Consider non-spherical or merger-driven effects, or a reason the zoom cusp isn't the right initial condition. Give the energy and a frozen pass condition. BH1 may close the black-hole route.

**Q4. Should route E stay the flagship?** The three failures are all at about 10¹²: L★ analogs, the Milky Way, and KiDS. Does that point to one cause? Compare with the alternatives on record: the a₀ law with a basin switch, or a law plus halos only in some systems. Say what result would make you drop route E.

**Q5. The floor.** Is there any route to Σ_a0 that isn't closed above, with a predicted R at 10¹⁰ and 10¹¹ before X80 lands?

**Q6. Best decisive tests.** Rank up to three measurements or analyses with existing public data that would best separate the options. State the expected signal for each theory and the sample size. Include how GH7's positive control or a cool-gas test could be made to work, if you think either is worth it.

## 7. Format for your reply
For each question:
1. The answer in plain words, or "no new idea".
2. Every input, with its source: measured, native, or assumed.
3. The derivation, with a numerical check of any closed form.
4. Frozen pass and fail conditions before any result, both footings.
5. What it would break elsewhere: SPARC, clusters, MW, KiDS.

At most three proposed lanes, ranked. Scripts are welcome if they read inputs rather than hard-code targets. I can't assume your scripts ran correctly: every number you give gets recomputed here.
