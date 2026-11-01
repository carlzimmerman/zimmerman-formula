# TD1_threshold_derivation: T LOCATED, NOT DERIVED. Every a₀-free attempt lands more than 1 dex above T, and the action needs a seed number and a separate mass term. The T question stops here

Criteria `FROZEN_CRITERIA.md` + `ASSUMPTION_LEDGER.md` (7f011a08bc, alone first); no amendment. Owner decision `OWNER_DECISION_2026-11-01_T_ONLY.md` (25c68146ab). Script `td1_threshold.py`; `td1_threshold.out`, `td1_threshold_results.json`; twin `*_MUTATE.*`. κ = ½ FITTED, unused. No a₀ enters, so the footings coincide by construction, which is not a test. Cold dark energy is a gravitating field component, never a particle. Not theory closed. Nothing here says the data favour the framework. Not blind.

## Verdict (frozen rule): **T LOCATED, NOT DERIVED**

Target W = [12.19, 12.39], log M☉, background `A_c2b_refit` (`B_cfg886_bg` for spread).

| Attempt | Primary | Other rows | Spread | Label |
|---|---|---|---|---|
| **A1** turned-around mass, σ(M) = δ_ta = 1.0624 | **13.942** | B 13.882; δ_ta × 0.993 13.957 | 0.061 | **MISS**, +1.55 above W's upper edge |
| **A2** Astra's clock (CFG763), turned around τ ago | **13.843** at 1.20 Gyr | 0.72 Gyr 13.885; 3.47 Gyr 13.605; B 13.542–13.824 | 0.343 | **CHOICE-DEPENDENT** |
| **A3** action with Θ and s(Σ) removed | | | | **NO LINK** |

A2's label comes from the frozen spread rule. It isn't near a landing: the lowest of its six rows is 13.542, 1.15 dex above W.

Reported, deciding nothing: A1b, the collapsed mass σ(M*) = 1.6865, is 12.861 (B 12.779), 0.39 to 0.47 above W's upper edge. A1c, M_ta × f_coll, is 13.895. Neither lands, so there's no clue to record.

## A3, the action
With the step and the a₀ term removed, L = −½(∇χ)² − ½ξθχ² − ¼λχ⁴ on the exact EdS top hat:
- **(a) Mass.** N = √(3ξ t_coll/2π) × 2.39628. The integral holds no M. Mass enters only through the collapse epoch.
- **(b) Numbers.** ξ, the seed and λ. ρ_DE can at most set ξ's scale, H_Λ = 0.0573 /Gyr. The seed stays free. W then needs N₀ between 1.182 and 1.254, growth of about × 3.4, so the seed would be set to within 7.5 %.
- **(c) After virialisation.** θ averages to zero, the tachyonic mass goes, and λχ⁴ alone gives w = 1/3, not w = 0. Requirement R5 then needs a separate mass term, which is a new number.
- **(d) Dimensions.** Newtonian pressureless collapse has no c, and G with H(t) makes no mass, so the only scale is P(k)'s, through σ(M, z) = number. With c, the Hubble mass is lg 23.05, 10.7 dex away. Other scales need ħ, baryon rates or a₀, which this attempt excludes.

**Missing piece, named:** a seed number, and a term that holds the condensate cold once θ averages to zero.

**One thing A3 gets right, post-result:** the sign. Later-collapsing, more massive systems reach larger N, so a threshold selects high mass. This changes no label, since the threshold takes the free seed to place it.

**Limits of A3.** θ of the matter flow stands in for the aether's θ_u, which isn't solved. The top hat holds for M below about M*. The rows follow a region's own collapse; R, the smoothing scale that would make this a basin key, stays posited. The NO LINK label is my reading of (a)–(d) against the frozen definition, written into the script, not computed.

## What this leaves
With no a₀, no baryon rates and no ħ, T can only be a member of the σ(M, z) = number family. DT1's epochs and this lane's δ_ta, δ_c rows all sit well above it: to reach W, σ must be about 2.0 to 2.15, and nothing in collapse statistics selects that. COOL1 shows baryon rates can land only by choice, and with no link. The crossover with a₀ is excluded by the owner's 10-31 rule, and CSM1 shows its consistent form fails lensing by +415 anyway.

**Stop rule fires.** No fourth attempt. Only the owner can reopen this, for a new forced kernel that's a₀-free. T goes into the flagship whitepaper as located from data, with this statement of what it would take.

This does not touch PAPER64's split as a description: T stays a located number there, canonical only. FG1 grades it.

## Expectation against result
Verdict and labels as expected. Numbers: A1 13.94 against my 13.5 ± 0.4, just above that range. A1b 12.86, inside my 12.5–13.0. A2 13.54–13.89 against my 13.2–13.5, above it. I set A2's primary and rule before seeing any of this; the misses are larger than I expected.

## Checks and twin
K1 z_f 0.944, 0.886, DT1's. K2 σ₈ 0.8275 vs 0.8274, 0.8172 vs 0.8172. K3 δ_ta 1.06241, δ_c 1.68647. K4 I 2.396280 on both grids. K5 0.26 GB. Rerun: JSON and output byte-identical.
MUTATE (turnaround at η = π/2): K3 fails at δ_ta 0.34081, exit 1, as frozen. Its verdict line doesn't change, since A1 misses at any δ_ta on either side of this range: the twin bites on the check, not the label.
