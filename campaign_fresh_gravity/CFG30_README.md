# CFG30 — binary galaxies under candidate B, refereed

Script: `CFG30_binary_galaxies_referee.py`, about 75 s.
- Outputs: `.out` and `_results.json`.
- MUTATE control: `_MUTATE.out` and `_MUTATE_results.json`. Every velocity difference is halved, and the headline H3 fails (A = 0.58 / 0.55, rc = 1).
- The main run exits 1. Two load-bearing checks fail: the control C3 (marginally) and H4. Both are reported as run.

κ = ½ is fitted. Both footings are used.

## Question

The failures summary listed binary galaxies as candidate B's largest unscored risk (B1). Isolated 2MRS major pairs move 1.8–1.9× faster than Milgrom's isolated deep-MOND two-body law predicts at d3 > 5 r_p (`hunt_2026/h48_h69b_relative_isolation.py`), while ΛCDM's abundance-matched halos land on their own prediction.

Candidate B drops the external field for top-level systems, so its prediction for an isolated pair *is* that two-body law. But the September estimator assumed circular orbits. In B's logarithmic two-body potential, an L* pair at 100–500 kpc has a circular period of about 3–18 Gyr. Unless something removes orbital energy (dynamical friction), such pairs are not virialised. They are still on the timing argument's orbit (Kahn & Woltjer 1959): they separated with the Hubble flow, turned around, and are falling back. In a log potential that infall is fast.

This lane asks whether the pairs are really too fast for B, or whether the circular-orbit assumption made them look so.

## Method

Both laws go through one machinery; between the two orbit models only the pair's speed changes.
- **Sample, estimator and projection prior:** h48b's own, exec'd read-only (2MRS major pairs with d3 > 5 r_p, N = 1830; Gaussian pairs plus uniform interlopers; the 3-D separation log-uniform in [r_p, 20 r_p] with the random-orientation kernel).
- **Circular:** h48b's prediction, unchanged. B uses the deep-MOND two-body circular speed; ΛCDM uses Moster+13 halos as NFW.
- **Timing:** the radial timing orbit from the Big Bang in each law's own two-body force plus Λ, on the first approach, with the speed at each 3-D separation fixed by r(t0) = r.
  - B: r̈ = −v_c²/r + Ω_Λ H₀² r.
  - ΛCDM: the halos as point masses (the classic Kahn–Woltjer form), with NFW as a variant.
  - The prior is truncated at the separation turning around today.
- **Cosmology:** CFG7's Planck 2018 (t0 = 13.80 Gyr).

## Disclosures

- **Before the script was written**, a scratch run looked at the separation tertiles: the dispersion falls 238 → 196 → 170 km/s. H2 confirms this and is marked as seen. The timing speed was also estimated by hand (v ≈ 2 v_c at 140 kpc).
- **The MUTATE run was executed first.** It exposed two numerical bugs in the controls. Both were fixed with the declared tolerances unchanged:
  - C2b: the quadrature table was too coarse just below today's turnaround radius. It is now denser there.
  - C2c: the general-potential solver lost the potential difference to rounding right next to the apocentre. It now uses the interpolant's exact local form there.
- **Added after the MUTATE run, reported only:**
  - R0: H3 divided by the estimator bias that C3 measured;
  - R7: the ΛCDM columns and the trend significance.

## Results

**Controls.**

| control | result |
|---|---|
| C1 | h48b's committed amplitudes reproduced: 1.886 / 1.800 / 0.949 (committed 1.89 / 1.80 / 0.95), N = 1830 |
| C2a | the analytic Λ = 0 limits reproduced to 2e-14 |
| C2b | the ODE lands on the table to 3e-12; the shooter matches the quadrature to 4.5e-4 |
| C2c | the general solver matches Kepler to 3e-4 |
| C2d | **the Local Group's first-approach speeds reproduce FP11's full two-body integration of the plain P2 law to 0.3–0.4%**, both footings |
| C3 | **FAILED, marginally.** The Gaussian estimator reads the timing model's own velocity distribution 5.5% high (mean of five mocks 1.055; the declared tolerance was 0.05). R0 corrects H3 for it. |

**Hypotheses.** A is the amplitude the data require (1 = the prediction is right).

| | canonical | alt | verdict |
|---|---|---|---|
| H1: circular orbits, most favourable baryons (Υ_K = 1.0, +0.3 mag, doubled xGASS gas at upper limits) | **1.511 ± 0.040** (12.9σ above 1) | 1.443 ± 0.038 (11.7σ) | PASS: baryons cannot close the circular gap |
| H2: circular profile, inner − outer tertile | B +0.75 (**6.5σ**); ΛCDM +0.31 (**5.4σ**) | | PASS (seen before): the circular model fails the data's profile **for both laws** |
| H3 (headline): B's timing orbits, h48b's baryons | **1.116 ± 0.028** | **1.047 ± 0.026** | PASS: in [0.80, 1.25] |
| R0: H3 ÷ the estimator bias | 1.058 | 0.993 | |
| H4: timing profile (inner / middle / outer) | 1.04 / 1.09 / 1.39: **−4.2σ** | −4.1σ | **FAIL**: the timing speeds fall too steeply with separation |
| H5: ΛCDM halos under the same timing | **0.463 ± 0.014** | | PASS: ΛCDM over-predicts under timing orbits |

**Reported rows** (B, canonical, timing unless stated).

| row | result |
|---|---|
| R1 projection geometry | radial-orbit projection 1.05 (ΛCDM 0.47); geometry-consistent circular 2.16 (ΛCDM 1.06) |
| R2 steeper companion density (n ∝ r⁻³) | 1.04 (ΛCDM 0.42) |
| R3 later branches | outgoing after the first pericentre 1.11; second approach 1.38 |
| R4 growing mass (M ∝ t) | 1.20 / 1.13 |
| R5 baryons under timing | most favourable 0.84 / 0.79 (B over-predicts); realistic (Υ_K = 0.6 + detected gas) 1.09 / 1.02, against 1.85 / 1.76 circular |
| R6 **the Local Group** | the same timing gives MW–M31 −175 / −191 km/s at the nominal baryons, **1.60× / 1.75× the measured −109.3 ± 4.4**. It would need M_b = 7.1 / 5.8e10 against 1.75e11. This is FP11 T4, reproduced. |
| R7 mass tertiles (log M_b 10.93 / 11.20 / 11.39) | B timing 0.96 / 1.06 / 1.33 (**+5.3σ**); B circular +4.1σ; ΛCDM circular 1.17 / 0.91 / 0.85 (**−4.7σ**); ΛCDM timing −8.5σ. The pair speeds rise with mass faster than B's M^¼ and slower than ΛCDM's abundance matching. |
| R8 isolation scan F = 2 / 3 / 5 / 8 | timing 1.22 / 1.13 / 1.12 / 1.02; ΛCDM timing 0.55–0.40; circular 1.76–1.89 |
| R9 ALFALFA dwarf pairs (h47, N = 53) | circular 1.12 ± 0.29 (reproduced); timing 1.13 ± 0.17 / 1.05 ± 0.15; ΛCDM timing 1.24 ± 0.19. The fitted interloper fraction shifts between shapes (0.26 → 0.19), so this sample cannot separate the orbit models. |
| R10 ΛCDM halos as NFW under timing | 0.52 |

## Standing

**B1 is not an established amplitude failure of candidate B.** It was one only under circular orbits:
- with circular orbits, even the most generous baryons leave the pairs 1.4–1.5× too fast (12–13σ);
- but the circular model fails the data's own separation profile for both laws (6.5σ and 5.4σ);
- under B's own timing orbits, the mean amplitude is 1.05–1.12 (0.99–1.06 after the estimator's bias);
- ΛCDM's halos under the same timing orbits over-predict (0.46).

Each law fits the mean in one orbit model and fails it in the other. **Which orbits apply is B's to specify, not a knob:**
- If B's dark density exerts no dynamical friction on a pair (T5's identity read literally: the dark density is the law's phantom, slaved to the baryons), timing orbits apply.
- If its cold component acts as a free medium, friction virialises the pairs and B1 stands at H1's level.

**The timing reading is not a clean pass.** Three tensions remain:
- **The separation profile (H4, 4.2σ).** The timing speeds fall too steeply with separation. The outer tertile has the most interlopers (27%).
- **The mass trend (R7, 5.3σ).** The pair speeds rise faster than B's M^¼. A mass-dependent Υ_K would reduce this. ΛCDM misses the same trend by 4.7σ in the other direction.
- **The Local Group (R6).** The same timing makes MW–M31 approach 1.6–1.75× too fast, as FP11 found.

**Binary galaxies do not currently discriminate B from ΛCDM.** The data sit between the two laws' simple orbit models, on the profile and the mass trend alike. Deciding it needs an orbit distribution derived from each law's own assembly history (N-body grade), and a statement from B on dynamical friction.

Nothing here says the theory is closed.
