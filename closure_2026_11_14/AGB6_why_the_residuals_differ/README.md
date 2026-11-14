# AGB6 — why the claim's residuals and the Pantheon+ ones differ for the same supernovae

2026-11-14. Plan: `PLAN.md` (committed alone before the chain was run). **A diagnosis, not a blind test; no frozen
verdict word.** Adopts nothing, edits no ledger, grades no part of this repository's framework.

## Answer
**Nothing is wrong with the older residuals. The age slope is in every uncorrected set of magnitudes for these
supernovae, raw Pantheon+ included. It goes away at one step only: the Pantheon+ release's own "bias correction",
which carries a host-mass term of 0.08 mag.**

Same 196 supernovae, same ages (the claim's), same fit (line in age inside 8 redshift bins, the claim's weights),
A in units of the published 0.030 mag/Gyr:

| set of magnitudes | no mass step | mass step free |
|---|---|---|
| C, the claim's own residuals | +0.83 ± 0.21 | +0.72 ± 0.26 |
| M, the SDSS-II table's MLCS2k2 modulus | +0.88 ± 0.18 | +0.74 ± 0.22 |
| S, the SDSS-II table's SALT2 modulus (its coefficients) | +0.74 ± 0.18 | +0.58 ± 0.22 |
| S′, the same fit, coefficients free | +0.65 ± 0.22 | +0.52 ± 0.25 |
| P′, Pantheon+ fit, the SDSS-II coefficients | +0.85 ± 0.18 | +0.64 ± 0.21 |
| P, Pantheon+ fit, coefficients free | +0.64 ± 0.22 | +0.49 ± 0.24 |
| Pc, Pantheon+ fit, the release's coefficients, nothing else | +0.64 ± 0.18 | +0.47 ± 0.21 |
| **Pb, Pantheon+ as published** | **+0.20 ± 0.19** | +0.30 ± 0.22 |

| step | change in A (no mass step) | carries slope? |
|---|---|---|
| C → S, the claim's analysis against the survey's SALT2 modulus | +0.09 ± 0.10 | no |
| C → M, against the survey's MLCS2k2 modulus | −0.05 ± 0.12 | no |
| S → S′, fixed against free coefficients | +0.09 ± 0.11 | no |
| S′ → P, the light-curve fit itself, coefficients free | +0.01 ± 0.05 | no |
| S → P′, the light-curve fit itself, coefficients fixed | −0.11 ± 0.05 | yes, the other way (2.2σ) |
| C → P, the claim's residuals against raw Pantheon+ | +0.19 ± 0.14 | no |
| P → Pc, free against the release's coefficients | +0.01 ± 0.11 | no |
| **Pc → Pb, the release's bias correction** | **+0.44 ± 0.07** | **yes (6.0σ)** |

- The release's construction was recovered exactly from its own table: m_b_corr = mB + 0.1475 x1 − 3.0922 c −
  biasCor_m_b − 0.0524, with no separate host step (rms 0.0000 mag). **The host dependence sits inside the bias
  correction**: its mean is +0.022 mag for low-mass SDSS hosts and −0.054 for the others.
- On these supernovae the bias correction trends with host age at −0.0157 ± 0.0026 mag/Gyr, which is 0.52 of the
  published slope; with a plain mass step taken out it still trends at 0.25 ± 0.10 of it.
- With a mass step allowed in the fit, the same step is smaller (0.17 ± 0.09) and every set sits between 0.3 and
  0.75: the sets no longer differ by more than their errors.
- Equal weights give the same picture (raw 0.50 ± 0.23, published 0.05 ± 0.21; the bias-correction step 0.52 ± 0.09).
- Each of the claim's tables separately: table 1 (161) repeats it; the 35 supernovae that are only in table 2 are
  too few to say anything.
- The two light-curve fits differ slightly with host age (Pantheon+ colours redder by 0.0015 ± 0.0005 per Gyr),
  which makes the Pantheon+ fit carry a little more slope at fixed coefficients, not less.
- Dropping the five supernovae where the two residuals differ most changes nothing (0.84, 0.66).

## Two corrections this makes to AGB5's write-up
1. AGB5's first post hoc found the difference between the claim's residuals and the Pantheon+ ones trending with
   age at 4 to 5σ. **That was an artefact of the comparison.** There the Pantheon+ stretch and colour coefficients
   were fitted on these supernovae before the age term, which hands part of the age trend to stretch (the two are
   correlated at −0.44). Fitted jointly, or with the release's own coefficients, raw Pantheon+ carries 0.64 and the
   difference from the claim's residuals is 0.19 ± 0.14.
2. AGB5's verdict said the slope "is in the older residuals and largely absent from the modern ones". The first
   half is right; the second is wrong as worded. It is absent from the **published** Pantheon+ magnitudes and
   present in the raw ones.

## What it means for a correction to published distances
The published slope was measured on residuals with no host correction, and there it holds. The releases' own host
corrections have already taken most of it out. A correction applied on top of published distances should use what
is left in them:

| slope left in the published distances | A |
|---|---|
| Pantheon+ (this lane, set Pb) | +0.20 ± 0.19 |
| DES Dovekie (AGB3, fit U on the published moduli) | +0.23 ± 0.06 |
| the same with noise in the star-formation ages allowed for (reliability 0.64) | +0.35 ± 0.09 |

Used as the prior on the amplitude in AGB1's cosmology fit (`agb6_today.py`; arithmetic on committed grids; no
frozen word):

| slope left | template | sample | q0 | Δχ² against q0 = 0 | reads | Δχ² never |
|---|---|---|---|---|---|---|
| DES, 0.23 ± 0.06 | cosmic average | whole | −0.25 | 7.80 | ACCELERATING TODAY | 102.9 |
| | cosmic average | DES alone | −0.42 | 6.21 | ACCELERATING TODAY | 74.2 |
| | sample's own drift | whole | −0.26 | 8.80 | ACCELERATING TODAY | 131.7 |
| | sample's own drift | DES alone | −0.54 | 10.42 | ACCELERATING TODAY | 95.9 |
| DES, noise allowed, 0.35 ± 0.09 | cosmic average | whole | −0.18 | 3.59 | SIGN NOT SETTLED | 73.0 |
| | cosmic average | DES alone | −0.34 | 3.86 | SIGN NOT SETTLED | 60.7 |
| | sample's own drift | whole | −0.21 | 4.98 | ACCELERATING TODAY | 113.0 |
| | sample's own drift | DES alone | −0.52 | 9.76 | ACCELERATING TODAY | 94.1 |
| Pantheon+, 0.20 ± 0.19 | cosmic average | whole | −0.23 | 3.74 | SIGN NOT SETTLED | 55.9 |
| | sample's own drift | whole | −0.28 | 6.16 | ACCELERATING TODAY | 103.7 |
| published slope in full, 1.00 ± 0.13 | cosmic average | whole | +0.13 | 1.61 | SIGN NOT SETTLED | 32.7 |

With the slope that is actually left in the DES distances, the expansion is accelerating today in all four
variants. Allowing for noise in the ages, it is accelerating with the sample's own age drift and falls just short of
the line (3.6, 3.9 against 4) with the cosmic-average template. The published slope in full is the only case that
moves the best fit to q0 > 0, and it double counts what the surveys have already corrected.

## Limits
- A diagnosis on 196 supernovae at z < 0.4, written after AGB5's numbers were known. Eight sets and nine steps
  were compared; only the bias-correction step is far beyond 2σ.
- The amplitudes depend on the weights at the level of their errors (raw Pantheon+: 0.64 with the claim's weights,
  0.50 with equal weights, 0.40 with Pantheon+'s own in AGB5, 0.30 with the SDSS table's ages in AGB4).
- The sets are relatives of the claim's residuals, not their exact construction, which is not public.
- That the Pantheon+ bias correction removes an age trend does not say it removes it for the right reason; it was
  built from a dust model fitted per host-mass group. What it does to the slope is measured here; whether age or
  dust is the cause is not.
- The DES leftover (0.23 ± 0.06) rests on photometric star-formation ages and a simple age model (AGB3).
- In the extension script one line reads "Pcb → Pb … CARRIES SLOPE" with a change of 0.000 ± 0.000: the two sets
  are identical by construction and the flag is a division of rounding errors.

## Files
`PLAN.md`; `agb6_chain.py`, `agb6_chain.{json,out}` (the planned chain); `agb6_published_step.py`, `.json`, `.out`
(the published step broken down; written after the chain, same rule); `agb6_today.py`, `.json`, `.out` (closing
arithmetic).

Commits (local / origin): plan 7e34c74eb3 / 5be3f06fb4; chain script 07e874a997 / 7f94fb058f; result abf5f977dc /
e232dd0940. The correction note in AGB5's README: e9b1a0de9b / b744311d58.

kappa = 1/2 FITTED; not theory closed.
