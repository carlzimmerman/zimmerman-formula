# The fine-structure-constant chain: status as of 2026-09-28

*Every line below points to a committed script or a cited source. Nothing here is a derivation of alpha. alpha stays an INPUT; kappa = 1/2 stays FITTED; the SM mass and coupling sector stays walled. Lane M (red team) has reported; lane K (literature audit) was still running.*

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
| C | holographic, species, emergence | inequalities, or alpha traded for a count N; the fermion-only emergence toy misses by ~1.9x, but that figure is misleading: the proper SM chain leaves 1/alpha_em ~ 107 at the species cutoff (not 0), and hypercharge emergence would need ~8.6 extra unit-Y Dirac fermions near 1 TeV (lane M, m4); either way it needs the walled masses |
| D | look-elsewhere bar | (no derivation proposed) the standard any candidate must clear |
| E | dilaton / attractors | freedom moves into the gauge kinetic function B_F(phi); Lambda and kappa never enter; for the fitted-exponent families tested, a dark-energy-tied alpha needs w ~ -1 (this is NOT general: lane E's own B3 allows 1+w up to ~0.25 at zeta < 6.5e-8) |
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
* **Post-hoc observation: VOID.** Lane A's remark that alpha(m_P) ~ 1/132 puts the required minimal-object size within 0.6% of Z was produced by a bug (b_Y = 3/5 b_1 instead of 5/3 b_1). Corrected: 1/alpha_em(m_P) = 104.94 (lanes B and F had it right), required k = 5.12, and Z = 5.7888 is 12-13% away. Found by the red team (lane M), fixed in lane A's script with a disclosed amendment. The remark was repeated in lane D's commit message (1d23899e6) and in earlier status text; it should be disregarded.
* Several lanes read only abstracts of some papers or recalled others; each lane's report labels which.
* Agents disclosed their own slips in amendments (thresholds loosened after seeing numbers in E; script bugs in A; hand-derivation slips in F; an unregistered check removed in H; a post-hoc stellar scan in I).
* Verification note: mutation-control invocation differs by lane (positional `MUTATE` for A, B, D, E, G, H, I, J; `--mutate` for AH scripts and lane F/C); every real run exits 0 and every control exits 1 when invoked correctly.

## Pending at time of writing

* Lane K: literature audit of published derivation claims through the lane-D checker.

## Red-team results (lane M, committed with this update)

Lane M attacked every negative result. Bottom line: the closures are SOUND; it found one real bug and several over-statements. It re-ran all lane A-G, D and AH1/AH5/AH6 scripts clean (AH2 and AH4 were not re-run by it).

* **Bug (lane A), fixed:** the hypercharge running coefficient (above). It created a spurious positive hint; it never closed a branch.
* **Lane B:** a universal gravity coefficient gives an interacting fixed point for U(1)_Y only if f > 0 and for SU(2), SU(3) only if f < 0, never both; lane B's f >= 0 restriction is harmless. Any truncation would need f_g to 0.18% for 1e-3.
* **Lane C:** see the corrected row above. Making the cutoff self-consistent shifts the result by 0.6%.
* **dS gauge structure:** the MacDowell-Mansouri coupling is ~ (16/3) G Lambda ~ 1e-121; it cannot supply alpha.
* **Lane D:** an independent enumerator reproduces D's E1(12) counts exactly and E2(6) to 7e-5. The bar is right. It is one-sided by design (a leading-order derivation cannot clear miss <= 5e-10 unless it declares its own effective precision).
* **Lean AH3:** `no_alpha_from_obs` follows from its own hypothesis, so it adds essentially no physics beyond stating the premise; the premise (rate depends on e only through eE/H^2) is a leading-order statement.
* **Untestable here:** a supersymmetric completion fixing the 6D coupling ratio (Salam-Sezgin keeps a flat modulus per the search summary; the link to the coupling is recalled).

### The red team's five under-tested branches (all rated LOW plausibility)

1. Joint over-determination: score (alpha_Y, alpha_2, alpha_3) together, not alpha alone (candidate map: lane F's S^2 relations alpha_SU2 = 3 l_P^2/R^2, alpha_U1 = N^2 l_P^2/(2 R^2)).
2. Emergence with a forced tower spectrum (the 2/(3 pi) coefficient is forced): compute 1/alpha_Y at Lambda_sp = M_red/sqrt(N) for one declared anomaly-fixed tower.
3. Graviton-inherited gauge coefficient: check whether the SO(10) kinetic coefficient is tied to G*Lambda (then it fails by ~121 orders) or free.
4. Holographic count: N^2 = c' S_dS gives 1/alpha = 12 pi c', so c' = 3.635 would be needed; enumerate the geometrically forced c'.
5. Charged fermions in dS_2, massless and massive: does sigma/H depend on alpha only through ln(mu_R/H)?
