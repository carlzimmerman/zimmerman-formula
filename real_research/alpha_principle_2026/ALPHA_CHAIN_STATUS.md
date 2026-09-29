# The fine-structure-constant chain: status as of 2026-09-28

*Every line below points to a committed script or a cited source. Nothing here is a derivation of alpha. alpha stays an INPUT; kappa = 1/2 stays FITTED; the SM mass and coupling sector stays walled. Lanes K (literature audit) and M (red team) were still running when this was written; see the last section.*

## The question

Can the programme's own structure force alpha = e^2/(4 pi eps0 hbar c) = 1/137.035999177 (Thomson limit; alpha runs) with no free parameter and no choice made after seeing the target?

## The chain, in order (each link is checked; each ends without a forced value)

| # | Link | Where | What it establishes |
|---|---|---|---|
| 1 | Dimensional obstruction | `real_research/alpha_schwinger_2026/ah5_dimensional_obstruction.py` (4dc1a546a) | From (c, G, Lambda) no dimensionless number exists. Adding hbar gives exactly one, x = Lambda G hbar/c^3 = 2.85e-122. alpha is an independent second group once a charge exists. The a0 chain has neither hbar nor a charge, so it cannot output alpha. |
| 2 | Horizon Schwinger/Unruh rate | `ah1_schwinger_ds2.py` (5db88bfc2), Lean `fable_independent_2026/lean_2026/AH3_alpha_nogo.lean` (86f3c7a9a) | The pair-production factor depends on e only through lambda = eE/H^2, so alpha is a free direction. Machine-checked (ten theorems, standard axioms, controls fail). |
| 3 | Horizon induced current | `ah2_induced_current_ds2.py` (5823f6bfe, dS_2 toy), `ah4_induced_current_ds4.py` (0c72bfdec, dS_4 scalar) | The current carries e^2, but sigma/H = alpha x G(m/H) with G mass-dependent; no conductivity tie fixes alpha. dS_4: heavy fields fall as a power (~0.124/mu^2); the ln(m/H) term is the one-loop running of e, so alpha enters as the measured low-energy input. |
| 4 | Charge quantization by geometry | `ah6_kaluza_klein.py` (e39f0bfcc) | KK gives alpha_n = 4 n^2 l_P^2/R^2 (derived by computer algebra). alpha = 1/137.036 needs R = 23.41 l_P; carrier mass 5.2e17 GeV; the electron is 1e-21 of the minimum graviphoton-charged mass. Alpha is traded for the modulus R. |
| 5 | Ten independent routes | `real_research/alpha_principle_2026/` lanes A-J (a628e8a66, 1d23899e6, 190cb6920) | See the table below. |
| 6 | The bar | lane D `D_calibration_bar/` | Any candidate must clear P < 1e-3 after look-elsewhere, miss <= 5e-10, zero fitted reals, scale stated. |

## Where each route ends (the residual freedom)

| Lane | Route | Ends at |
|---|---|---|
| A | WGC, Dirac + extremality, RN-dS | inequalities, alpha-free relations, or alpha re-expressed as the size of the minimal magnetic extremal object (r = 1/(2 sqrt(alpha)) l_P); integer fits automatic (n ~ 3.5e61) |
| B | RG / asymptotic safety | truncation-dependent bounds; SM charged content gives alpha^-1 ~ 75-77; needs a Planck-scale alpha^-1 ~ 105 |
| C | holographic, species, emergence | inequalities, or alpha traded for a count N; emergence misses by ~1.9x and needs the walled masses |
| D | look-elsewhere bar | (no derivation proposed) the standard any candidate must clear |
| E | dilaton / attractors | freedom moves into the gauge kinetic function B_F(phi); Lambda and kappa never enter; a Lambda-tied alpha must be static (w = -1) |
| F | KK stabilization, light charged states | R ~ 1e30 l_P from Casimir + Lambda (needs ~115 decades of tuning to reach 23.4); Freund-Rubin adds a free 6D ratio and a tuned Lambda_6 |
| G | topology, anomalies, GUT embedding | integers, charge ratios, coupling ratios; overall coupling free |
| H | string / heterotic | alpha traded for the string scale / dilaton and threshold constants; convention of the O(1) coefficient unresolved |
| I | selection, consistency bounds | bands (hundreds to thousands of times wider than 1e-3), not a point; HH-weight extremum is a scheme choice |
| J | emergent photon from a condensate | alpha^-1 = (N_eff/3 pi) ln(Lambda^2/mu^2) + const; N_eff and Lambda/mu not derived; the repo's dark-fluid order parameter cannot supply them |

**Common finding.** Every route fixes integers, ratios or inequalities, or moves the freedom into one of: a modulus (radion, dilaton, string scale), a dimensionful scale or cutoff ratio, the charged spectrum, or a gauge kinetic function. These are the same non-derivable objects seen from different sides.

## What a derivation would have to supply

A principle that (i) forces one of those objects to a NUMBER without a choice made after seeing the target, (ii) states the scale at which alpha is meant, (iii) reaches the measured value at the level the bar requires (a few 1e-10, or a stated predicted precision), and (iv) does not need the walled charged-mass spectrum, or derives it. Nothing in the record does this.

## Caveats and open items

* dS_2 results (AH1-AH3) are a two-dimensional toy (e has mass dimension); only the structural statements (rate depends on eE; tie arithmetic) carry to 4D. AH4 is the dS_4 scalar only.
* Untested: fermions and backreaction in dS, higher-derivative corrections, string-tower emergence, de Sitter quantum break-time with charged species, full FRG results beyond published truncations, moduli stabilization in an explicit string model.
* **Unreconciled:** the repo's earlier bound zeta < 4e-9 (SM bridge review, 2026-06-17) is NOT reproduced by lane E (its bound is ~6.5e-8 under stated definitions; the old review does not define zeta).
* **Post-hoc observation, not a lead:** lane A noticed after seeing its numbers that alpha(m_P) ~ 1/132 puts the required minimal-object size within 0.6% of Z = 2 sqrt(8 pi/3). Under lane D's rule that precision allows about 3 alternatives; the lane tried far more; it is not evidence.
* Several lanes read only abstracts of some papers or recalled others; each lane's report labels which.
* Agents disclosed their own slips in amendments (thresholds loosened after seeing numbers in E; script bugs in A; hand-derivation slips in F; an unregistered check removed in H; a post-hoc stellar scan in I).
* Verification note: mutation-control invocation differs by lane (positional `MUTATE` for A, B, D, E, G, H, I, J; `--mutate` for AH scripts and lane F/C); every real run exits 0 and every control exits 1 when invoked correctly.

## Pending at time of writing

* Lane K: literature audit of published derivation claims through the lane-D checker.
* Lane M: red team of the negative results, with a ranked list of under-tested branches.
