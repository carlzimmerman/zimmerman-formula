# NC2: cosmology of born-clumped cold dark energy. FAIL: K1 (R2) and K2 (R6) both triggered, both footings, every clump mass

Kappa = 1/2 FITTED; not theory closed. Adopts nothing. TEST lane (FRAMEWORK_CANDIDATE_2, lane NC2). Criteria:
FROZEN_CRITERIA.md (b1ed7d2541), pushed alone before any script.

Scripts:
- nc2_g1.py: G1 primary CMB, built by a subagent; 95 s per footing, peak RSS 0.79 GB.
- nc2_g2g4.py: G2 lensing, G4 mu distortion and the implied b; 10 s, 0.41 GB.
- nc2_g3.py: G3 forest, built by a subagent; 69 s, 0.33 GB.

Outputs are each script's .json / .out plus the MUTATE twins, and parts/ (G1 per-footing logs).

Lanes used read-only: the QX15 grader and fits, QX3 iter2's PR4 machinery, GL1's corrected kernel and P1D3's DESI DR1
loader. Name: cold dark energy, never dark matter; no particle. NC1's clump spectrum had not landed when the gates ran,
so the frozen M_cl brackets are used.

**Label: FAIL.**
- **K1 (R2):** the primary CMB tolerates a large-scale bias of only |b - 1| <= 1.4e-3 / 3.3e-3. A peaks-born clump
  population implies b = 45-1866 at recombination. The Poisson and compensated clump fields also miss by 12-17 orders of
  magnitude in Delta chi^2.
- **K2 (R6):** the DESI DR1 forest 1D power excludes the clumps at the mean abundance on both brackets
  (Delta chi^2_Asimov 1.7-2.4e5). The fraction of the component it allows in clumps is 0.25-0.28 %.
- The mean component alone passes CMB lensing, as expected.

## Gate x reading x M_cl (canonical / alt; the two agree to the digits shown unless both are given)

| Gate | Reading | M_cl 1e13 (r_cl 4.14 Mpc) | 1e14 (8.93 Mpc) | 1e15 (19.2 Mpc) |
|---|---|---|---|---|
| G1 primary CMB (QX15 PA, Delta vs 3741.08 / 3741.15) | Z, bias b | b 1.2: +4.10e4 / +4.08e4; 1.5: +5.57e5; 2.0: +6.35e6; all **FAIL**. Tolerated b 0.99670-1.00142 (canonical), 0.99671-1.00143 (alt) | (Z is M_cl-free) | |
| | P (Poisson clumps) | +8.2e13 **FAIL** | +6.8e15 **FAIL** | +3.6e17 **FAIL** |
| | C (compensated, k^4 tail) | +1.3e12 **FAIL** | +1.35e15 **FAIL** | +2.3e17 **FAIL** |
| Implied b at z_rec (Sheth-Tormen peaks, k 0.05) | | nu 1.07, b_L 0.07, **b 45** | nu 1.67, b_L 0.74, **b 453** | nu 2.89, b_L 3.04, **b 1866** |
| G2 CMB lensing L <= 400 | (a) mean component | chi^2 8.56 / 8.56 **PASS** | | |
| | (b) clumps' Poisson power, corrected kernel (n = 4) | chi^2 10.67 (+2.11) **PASS** | 84.4 (+75.9) **FAIL** | 248.3 (+239.8) **FAIL** |
| G3 forest DESI DR1 P1D, z 2.2-4.4, Asimov Delta chi^2 | (i) linear + clumps | 1.66e5 **FAIL**; tolerated f_in 0.0028 | 2.40e5 **FAIL**; f_in 0.0026 | 2.42e5 **FAIL**; f_in 0.0025 |
| | (ii) inter-clump, baryons alone | 2.30e5 **FAIL** | 2.30e5 **FAIL** | 2.30e5 **FAIL** |
| | (iii) post-freeze: profile cut at 0.1 Mpc | 1.29e12 **FAIL**; f_in 0.0014 | 1.29e14 **FAIL**; f_in 0.00042 | 1.29e16 **FAIL**; f_in 0.00013 |
| G4 mu (adiabatic window; upper bound) | P / C | 2.87e-2 > 9e-5 | 1.34e-2 | 6.1e-3 |

## What it means

- **The CMB needs the cold component to trace the adiabatic mode to about 0.1 %.**
  - Z gives the tolerated range. In CAMB's convention it is a fully correlated CDI with S/zeta about 0.01-0.02, which is
    Planck's CDI scale.
  - A population that sits at future cluster nodes from birth carries the late linear field's modulation at birth. At
    k 0.05 that is b_L delta_L0, which is 600 times the cold component's adiabatic contrast at recombination.
  - A component made of discrete cluster-mass clumps also carries Poisson noise. On CMB scales it exceeds zeta's power by
    1e3-1e8 (P), and still by 4-3e5 at k 0.01-0.05 when compensated (C at 1e14).
  - This is the same physics that closed the primordial-black-hole door (PB1-PB4): cluster-mass primordial objects are
    shot-noise isocurvature.
  - Even M_cl 1e13 with a k^4-compensated tail fails G1 by 1e12.
- **The forest excludes the clumps two ways, and they bracket the truth.**
  - In (i), the component's own small-scale adiabatic power is gone outside the clumps. At k > 1/r_cl the matter power
    drops to about f_b^2 (r ~ 0.03-0.05), while the clumps' shot noise adds power at intermediate k.
  - In (ii), sightlines between clumps see gas that grew on baryons alone from z 1090 (D ∝ a^0.29), so r ~ 1e-8 to 1e-7.
  - The NC3-motivated profile cut at 0.1 Mpc, (iii), makes the shot noise dominant (r up to 1e6) and fails harder.
  - The forest allows at most 0.13-0.28 % of the component in clumps.
- **CMB lensing** passes for the mean component (chi^2 8.56), as the candidate said (R1). The clumps' Poisson power fails
  it at 1e14-1e15 through the corrected kernel; 1e13 passes (+2.11).
- **mu (G4) does not count toward the label.**
  - The adiabatic-window bound treats the clump power as adiabatic, and true CDI heats photons only through potentials, so
    it is an upper bound.
  - It lies above the FIRAS line by 70-320 times. 65 % of it comes from k < 50, against the candidate's "null below k 50".
  - The rule written in the frozen criteria would call this a FAIL. Here it is reported as not decisive, a post-freeze
    reading, disclosed. The label is FAIL without it.

## Known answers and MUTATE

- **KA1:** the QX15 grader at each footing's main fit gives chi^2_PA 3741.081 / 3741.147, within 5e-13 of QX15. **PASS.**
- **KA2:** GL1's kernel reproduces record arithmetic at n = 0 (0.0 difference) and gives S = 1 at R = 1. The shape row is
  1.005 / 1.006 / 1 / 0.991 / 0.984 / 0.980, against GL1 to 4.6e-4. **PASS.**
- **KA3:** P1D3's md5 and 755 bins are reproduced. f_in 0 gives r = 1 and Delta chi^2 0. **PASS.**
- **KA4** (reported): C_10 iso / ad is 1.913 against (2 f_c)^2 2.849, a ratio of 0.67, inside the factor 1.5. **PASS.**
- **M1 (R19):** a flat CDI at Delta^2_S(0.05) = 0.018 gives Delta 1.2e17 and FAILS. **BITES.**
- **M2:** a uniform component reproduces QX15 (G1), the mean lensing (G2b = G2a, mu 0) and r = 1 (G3). **OK.**
- **M3:** collapsed clumps (r_cl x 0.1) give G3 (i) Delta chi^2 2.1e10-5.4e10 and FAIL. **BITES.**

## Decisions and disclosures

- **G1, Z.** CAMB "initial_vector" (1, a, 0, 0, 0). In that mode CAMB's adiabatic sign is reversed. With
  delta_cdm(1090, 0.05) of -15.58 (adiabatic) and +2.13 (CDI), b = 1 - 0.137 a.
- **G1, P and C.** Lensed adiabatic plus unlensed isocurvature: iso lensing is neglected, irrelevant at these sizes. No refit
  ran, because no Delta fell in 4-200. Linear theory is far outside its range at these amplitudes; the numbers only mark the
  result as astronomically FAIL.
- **Implied b** = 1 + b_L delta_cdm(z 0)/delta_cdm(z_rec) at k 0.05 (ratio 614, synchronous gauge). It comes from a
  transfer-only CLASS run at each footing's QX15 fit.
- **G3.**
  - Abundance: the clump abundance uses each footing's QX15 R (5.409 / 5.411). The candidate quotes R 5.562 (QX12); the
    difference does not change any label.
  - Bracket (ii) growth: exponent with f = f_b. The ungraded p = 1 reading gives the same Delta chi^2.
  - Lambda's late suppression is ignored, and the whole sightline is taken as inter-clump.
  - Statistic: the full DESI covariance (stat + syst). The flux model is a linear 1D matter-power proxy; saturation is
    not modelled. P1D2 showed saturation can hide a few-% effect at z > 4; it cannot hide 1e5 in Delta chi^2.
- **G3 label** follows the frozen rule's FAIL line: a FAIL needs both brackets to fail, and both do. Bracket (iii) was
  added after the freeze at the requesting session's request (NC3 input) and is not part of the label.
- **Memory.** G1's peak RSS was 0.79 GB, under the 1 GB line.

Kappa = 1/2 FITTED; not theory closed.
