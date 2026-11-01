# TD1_threshold_derivation: FROZEN CRITERIA, committed alone before any script or number of this lane

**Question.** Can the switch threshold T be derived with no a₀ and no fitted constant? Three attempts, then this question stops. Owner decision: `OWNER_DECISION_2026-11-01_T_ONLY.md`.

**Not blind.** T, its window and the classic nonlinear mass near 10^12.5–13 M☉ are all known to me. A landing is weak evidence on its own, which is why the link test below is required.

## Target
W = [12.19, 12.39] in log M☉, COOL1's window: LEE1's lower edge and BS1's Local Group basin, width 0.20 dex. T is an M200c mass summed over a basin, z = 0. The upper edge is one object's margin. T has a target on canonical only.

## Already excluded, not rerun
DT1 A–G; COOL1 (cooling, NO LINK); CF1 and X58 (own-mass crossover); J1, X19 (potential depth); T from L (PAPER64 v1.1 withdrawn; CSM1: consistent crossover 11.22, lensing +415; refit L 2.51 fails groups +2.62). The crossover η Σ_coll = a₀/2πG uses a₀, which the owner's 10-31 rule removed from the cold sector. It isn't an available derivation.

## The three attempts
All on EM1's record background `A_c2b_refit`, with `B_cfg886_bg` reported for spread. σ(M) as DT1 builds it, M total mass. No a₀ enters, so the footings coincide by construction, which is not a test.

**A1, turned-around mass (the field variable).** BASIN_FIELD_EQUATION_CANDIDATE's selector is θ < 0, turned around. Its native mass: σ(M_ta, z = 0) = δ_ta, with δ_ta from the exact Einstein-de Sitter parametric solution, the same convention as the record's δ_c = 1.686. **Primary row: M_ta directly.**
Reported beside it, never deciding:
- A1b, the collapsed mass: σ(M*) = 1.686.
- A1c, M_ta × f_coll, the mass inside M200 halos, f_coll = erfc[(δ_c − δ_ta)/√(2(S(10⁹) − S(M_ta)))].
- δ_ta × 0.993, a low-Ω_m size check on the EdS value.

**A2, Astra's clock.** CFG763's formation clock, first-order rate τ. A basin holds a halo if it turned around at least τ ago: D(z_ta) = δ_ta/σ(M), lookback(z_ta) = τ. τ from CFG763's canonical table: 0.72 and 1.20 Gyr (lower bounds), 3.47 Gyr (upper bound). **Primary row: 1.20 Gyr**, nominal ages, with the other two setting the spread. Disclosed: that clock was fitted on baryon ages in tidal dwarfs and old discs for a different medium, and here it's applied to a basin. That's a transfer with no derived bridge.

**A3, the action (analytic plus one integral).** Does the candidate action produce a mass threshold once its posits are removed? Remove the step Θ(θ) and s(Σ), which carries a₀. Keep L = −½(∇χ)² − ½ ξ θ χ² − ¼ λ χ⁴, the lowest-order coupling to the flow's expansion, tachyonic for θ < 0. Compute the growth exponent N = ∫ √(ξ|θ|) dt from turnaround to collapse on the exact EdS solution, and how N depends on M. State:
- (a) whether M enters other than through the collapse epoch;
- (b) how many numbers ξ, the seed amplitude and the required N add, and which, if any, ρ_DE fixes;
- (c) what happens to χ once the halo virialises and θ averages to zero;
- (d) a dimensional statement: with {G, c, H(t), ρ_DE, P(k), pure numbers} and no baryon rates or a₀, is every mass scale in gravity-only collapse a member of the family σ(M, z) = number?

## Frozen labels
**Threshold, per attempt A1, A2:**
- **LANDS:** primary row in W and input spread ≤ 0.20 dex.
- **CHOICE-DEPENDENT:** spread > 0.20 dex, whether or not the primary lands. COOL1's rule.
- **MISS:** primary outside W and spread ≤ 0.20 dex.

**Link, A3:**
- **LINK:** A3 gives a term with the right sign, surviving virialisation, and adding no number that ρ_DE doesn't fix.
- **NO LINK:** otherwise. The missing piece is named.

**Lane verdict:**
- **T DERIVED** only if A1 or A2 LANDS **and** LINK. C3 is then regraded at that T by LEE1's harness, and nothing else.
- **T LANDS WITHOUT A MECHANISM** if a threshold LANDS with NO LINK. Not a derivation.
- **T LOCATED, NOT DERIVED** otherwise.

A reported row landing in W, such as A1b, is a clue and changes no label.

## Stop rule, frozen
After this lane reports, the T question stops under any verdict but T DERIVED. No fourth attempt. No other δ, z, τ, smoothing scale or definition of mass. A clue from a reported row is recorded in the whitepaper's open problems and is not chased. Only the owner can reopen it, and only for a new forced kernel that's a₀-free. Any verdict goes into the flagship whitepaper as it stands.

**Expectation on record.** T LOCATED, NOT DERIVED. A1 near 13.5 ± 0.4, MISS. A1b near 12.5–13.0. A2 near 13.2–13.5. A3 NO LINK: mass enters only through the epoch, and a seed number stays free.

**What a pass wouldn't mean.** C3 is expected to fail the cluster keys and IC 1613 at any T. T DERIVED wouldn't make the theory pass.

## Checks and twin
K1 machinery reproduces DT1: z_f(10¹²) 0.944, z_f(10^12.3) 0.886, within 0.005. K2 σ₈ from the same σ(M) route equals EM1's within 0.01. K3 δ_ta from the parametric solution equals 1.0624 within 0.001, δ_c equals 1.6865 within 0.001. K4 the growth integral on a second grid agrees within 10⁻⁴. K5 peak RSS < 1 GB. Rerun byte-identical JSON.
MUTATE (`TD1_MUTATE=1`, separate outputs): turnaround taken at η = π/2 instead of π; K3 must fail, exit 1.

One thread, nice 15, under 1 GB, no downloads. `PYTHONHASHSEED=0 OMP_NUM_THREADS=1 nice -n 15 python3 -I td1_threshold.py`.

κ = ½ FITTED, unused here; T LOCATED. Cold dark energy is a gravitating field component, never a particle. No ΛCDM inputs. Not theory closed. Nothing here says the data favour the framework.
