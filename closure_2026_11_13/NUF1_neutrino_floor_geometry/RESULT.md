# NUF1 — RESULT: the neutrino-mass floor against DESI DR2 BAO + the compressed CMB prior (geometry only)

2026-11-13. Criteria `FROZEN_CRITERIA.md`, committed alone before any real-data number (84c613b81a). No amendment.
A test of flat ΛCDM on its own terms. It adopts nothing and edits no ledger.

## Verdict
**FLOOR DISFAVOURED / FRAGILE** (all four known-answer checks pass).
- Primary (all DR2 BAO bins + DESI's compressed CMB prior): best-fit effective mass **m = −0.145 eV**, 68 % interval
  **[−0.228, −0.060] eV** (Δχ² = 1), 95 % [−0.312, +0.051] eV. At the normal-ordering floor 0.059 eV, **Δχ² = 4.38**
  (2.1σ); at the inverted floor 0.10 eV, Δχ² = 6.59 (2.6σ).
- FRAGILE: dropping LRG2 (Δχ² 2.82) or replacing the Lyα BAO pair with the Lyα AP pair (Δχ² 3.56) turns the word into
  FLOOR ALLOWED. Dropping LRG1 (5.43) or keeping only z > 0.6 (6.48) leaves it DISFAVOURED.
- The geometry alone puts flat ΛCDM's preferred neutrino mass below the laboratory floor, at about 2σ, not 3σ. DESI's
  3.0σ (arXiv:2503.14744, −0.101 +0.047/−0.056 eV) uses the full CMB likelihood with lensing, which this lane leaves out
  by design. Our central value is more negative than DESI's and our interval about 1.6 times wider.

## Fits (profile χ² over θ*, ω_b, ω_bc; three degenerate states; extrapolation at fixed θ*, ω_b, ω_bc)
| run | best m [eV] | 68 % | 95 % | χ²_min | Δχ²(0.059) | Δχ²(0.10) | word (NO floor) |
|---|---|---|---|---|---|---|---|
| **primary** | **−0.145** | [−0.228, −0.060] | [−0.312, +0.051] | 10.70 | **4.38** (2.09σ) | 6.59 (2.57σ) | **FLOOR DISFAVOURED** |
| ctl: drop LRG1 | −0.171 | [−0.257, −0.084] | [−0.344, +0.027] | 5.94 | 5.43 (2.33σ) | 7.78 (2.79σ) | FLOOR DISFAVOURED |
| ctl: drop LRG2 | −0.114 | [−0.201, −0.022] | [−0.287, +0.088] | 6.04 | 2.82 (1.68σ) | 4.58 (2.14σ) | FLOOR ALLOWED |
| ctl: Lyα AP pair replaces Lyα BAO | −0.129 | [−0.212, −0.042] | [−0.296, +0.069] | 13.52 | 3.56 (1.89σ) | 5.62 (2.37σ) | FLOOR ALLOWED |
| ctl: z > 0.6 only | −0.202 | [−0.294, −0.110] | [−0.388, −0.010] | 4.83 | 6.48 (2.55σ) | 8.87 (2.98σ) | FLOOR DISFAVOURED |

σ columns are √Δχ² (one parameter). The best fit never sits at a grid edge. The profile at m = 0 lies Δχ² = 2.39 above
the minimum (primary).

## Known-answer checks
| check | ours | published (TeX source) | tolerance | outcome |
|---|---|---|---|---|
| K1 BAO-only ΛCDM | Ω_m 0.2971, h r_d 101.56 Mpc | 0.2975 ± 0.0086, 101.54 ± 0.73 (arXiv:2503.14738) | 0.003, 0.3 Mpc | PASS |
| K2 as briefed (ΛCDM values for DESI + compressed prior) | — | not quoted by the paper | — | DROPPED |
| K2A Δχ²(w0wa − ΛCDM), DESI + compressed prior | −8.24 (w0 −0.45, wa −1.64) | −8.0 (Table `tab:dchisq`) | ± 1.0 | PASS |
| K2B DESI + BBN + θ* | Ω_m 0.2964, H0 68.50 | 0.2967 ± 0.0045, 68.45 ± 0.47 | 0.5σ | PASS |
| K3 mutation twin (BAO = model at 0.06 eV) | m 0.0600, 68 % [−0.050, +0.145], χ²_min ≈ 0 | 0.06 | 0.005 eV | PASS (exit 3) |

K2A's w0, wa sit close to DESI's posterior means for the same combination (−0.43 ± 0.22, −1.72 ± 0.64), which
checks the compressed prior's numbers and units directly.

## Reported only (no frozen word)
| run | best m [eV] | 68 % | Δχ²(0.059) | Δχ²(0.10) | reading |
|---|---|---|---|---|---|
| w0, wa also free (PPF; grid 0.02 eV) | +0.027 | [−0.159, +0.153] | 0.06 | 0.31 | floor allowed |
| ω_bc prior sd × 2 | −0.137 | [−0.275, +0.028] | 1.45 | 2.22 | floor allowed |
| extrapolation at fixed h (not θ*) | −0.149 | [−0.234, −0.062] | 4.45 | 6.67 | as primary |
| θ* mean 0.0104110 (Eq. `thetastar_prior`) not the printed 0.01041 | −0.141 | [−0.224, −0.055] | 4.18 | 6.35 | as primary |

- **w0wa free:** yes, the floor becomes allowed: Δχ²(0.059) = 0.06 and Δχ²(0.10) = 0.31, best fit +0.027 eV (95 % −0.348 to +0.265), χ²_min 7.20 against 10.70 for ΛCDM (−3.5 for two more parameters). At the floor
  w0 = −0.46, wa = −1.60, the DESI quadrant. The mass and the dark-energy evolution trade against each other along
  one degeneracy; for m > 0.33 eV wa runs into its prior edge (−3).
- **Widened ω_bc prior:** the neutrino information here comes almost entirely from the CMB's ω_bc; doubling its sd
  drops the floor's Δχ² from 4.38 to 1.45.
- **Convention and rounding:** the fixed-h extrapolation and the four-figure θ* mean each move Δχ²(0.059) by less than
  0.2; neither changes the word.
- **One massive state vs three degenerate (observation, not a frozen row):** K2A's ΛCDM fit at 0.06 eV with one massive
  state (DESI's fixed-mass convention) has χ² = 15.58; the primary profile at 0.06 eV with three degenerate states has
  15.13. Against the primary minimum that is Δχ² ≈ 4.9 at 0.06 eV instead of 4.4. The real normal-ordering spectrum at
  the floor is closer to one heavy state, so the degenerate choice frozen here (following arXiv:2407.10965) is the
  milder one, by about 0.5 in Δχ².
- **Shape:** the profile's slope dips over |m| < 0.01 eV (second differences ±0.13 against a typical 0.03). It comes
  from CAMB's small-mass response mirrored by the extrapolation (h_eff is smooth across it; the twin shows the same);
  the floor values are read at the floor itself and the minimum sits at −0.145, so neither is affected.

## What this lane cannot say
- It leaves out CMB lensing, the ISW effect, the damping tail and the full CMB likelihood: it is weaker than DESI's
  analysis by construction and cannot confirm or refute the 3.0σ.
- It is the same BAO-against-CMB mismatch (low h r_d from BAO against the CMB's ω_bc and θ*) that drives the
  evolving-dark-energy hint, not a second, independent anomaly; the w0wa row shows the two trade against each other.
- A negative effective mass is a statement about ΛCDM's fit, not a measured physical mass.
- It says nothing about whether the repository's own framework is favoured; canonical and alt a0 footings do not
  enter. Nothing is adopted; no ledger is edited.
- The compressed prior is DESI's (CamSpec, ΛCDM-marginalised early-universe compression), taken as printed. The
  2503.14744 prior built for the effective-mass model is shown only as a figure there, so it is not used.

## Reproduce
`cd closure_2026_11_13/NUF1_neutrino_floor_geometry && python3 nuf1_run.py primary > nuf1_primary.out` (about 9 min,
CAMB 1.6.6, numpy 1.26.4, scipy 1.14.1), then `python3 nuf1_collect.py`. Every other row is the same command with its
mode name.
