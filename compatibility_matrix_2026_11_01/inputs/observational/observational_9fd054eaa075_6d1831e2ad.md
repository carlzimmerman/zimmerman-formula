# DR7_fragments: BITES, FAILS [NOISE-LIMITED]. The phase-space cap on the response itself, no new number, lifts Υ from 0.35 to 0.41 and worsens the tilt. It acts only inside about 0.6 r_h

Criteria: `FROZEN_CRITERIA.md` (d2c8868a77), committed alone first. `dr7_cap.py`, `dr7.py`, `dr7_tail_add.py`, `dr7_checks.py`, `dr7_read.py`, `dr7.out`, `dr7_results.json`, `dr7_{MEDIAN,LOW,HIGH,MUTATE}_results.json`. UR1's path, read only. κ = ½ FITTED, unused here. No a₀ in the cold sector. Cold dark energy, never a particle. Not theory closed. Nothing here says the data favour the framework. **Not blind:** UR1, UR2, NR3, LC1, PS1, PS2 and RM1's result files were read. The door came from an outside text received as fragments; this tests the fragment "a Lynden-Bell / Liouville cap on ρ_f/σ_f³ limiting contraction", with the rule written here, not by that text.

## Was it tested before?
PS1 and PS2 capped the initial core only, on the rule with the floor, with no response in the path. UR1, UR2, NR3, LC1 and OP3 have no cap. RM1 names a phase-space cap as one proposal behind a fitted envelope. So this exact case was open.

## Canonical, f★ 0.034, EM1, Blumenthal
| Input ρ₁₀, ρ₁₁ | Cap | Υ A/B | rms A | tilt A | Υ by V_flat | Groups Z | LT A | keys | X-COP |
|---|---|---|---|---|---|---|---|---|---|
| MEDIAN | off (NR3) | 0.35/0.36 | 0.0670 | +0.17 | 0.49, 0.53, 0.46, 0.30, 0.36, 0.47 | +1.50 | +0.116 | 14 | −0.097, 0.146 |
| **MEDIAN** | **on** | **0.41/0.41** | **0.0693** | **+0.21** | **0.54, 0.58, 0.46, 0.31, 0.40, 0.52** | **+1.50** | **+0.116** | **14** | **−0.097, 0.146** |
| MEDIAN | on, Q₀ cold-only (reported) | 0.40/0.40 | 0.0691 | +0.20 | 0.53, 0.57, 0.46, 0.31, 0.39, 0.52 | +1.50 | +0.116 | | |
| LOW | on | 0.55/0.56 | 0.0675 | +0.53 | 1.00, 0.91, 0.65, 0.34, 0.40, 0.52 | +1.50 | +0.173 | | |
| HIGH | on | 0.30/0.30 | 0.0751 | −0.06 | 0.30, 0.30, 0.32, 0.31, 0.40, 0.52 | +1.50 | +0.061 | | |

FAIRTA + cap (reported): Υ 0.83/0.84, rms 0.1227, tilt +0.67, groups +5.46, LT +0.525: unchanged from dead.

## Frozen label
**BITES, FAILS [NOISE-LIMITED].** Υ moves 0.06. PRIMARY fails the line (Υ), tilt and LITTLE THINGS; keys miss G-IN-Mall −2.05. [NOISE-LIMITED] because LOW reaches the line, but fails tilt and LITTLE THINGS there, and HIGH clears tilt and LITTLE THINGS at Υ's grid floor. A band run reaching a line isn't a pass. My expectation (Υ 0.36–0.45, tilt holds or worsens, line fails) held.

## How this reads
- **The cap is real where Blumenthal is wrong and small where the fit needs it.** On a test core uncapped Blumenthal exceeds Q₀ by ×2148 at its cusp, because circular orbits cusp a core by construction. On SPARC every call binds, but the capped core ends at a median 0.63 r_h (p90 1.8), and the held-back mass rejoins just outside it: M/M_c at r_h has median 1.000.
- **So M_f/M_0 at r₀ doesn't move:** 1.51, 1.41, 1.65, 1.92, 1.91, 1.98 with and without the cap. LITTLE THINGS, groups, keys and X-COP read outer or integrated mass and are unchanged. Only inner rotation-curve points feel it, which is why rms gets slightly worse.
- **The miss stays at 150–250 km/s:** 0.31, 0.40 against the 0.50 line. It lands near RM1's I0.75 at δ 0 (0.40, +0.22) with no free strength. RM1's 180 cells, evaluated read only on its files, show none clearing; its own reader's verdict isn't committed here.
- **Clusters:** expansion lowers Q, so the cap is nearly inert; with BCG the 0.05 Mpc response goes 0.74 to 0.73.

## Limits
Q is a proxy for f, so this is not the Liouville theorem itself. Isotropic. Q₀ inherits the hand-chosen Burkert and η. M_c is still Blumenthal outside the capped core: the cap truncates its cusp, it isn't a solution for the true orbit response. No live test with a core: LC1 starts from the zoom's own profile. Keys ran on UR1's gas inputs, without GS4's +0.005, as frozen; the row fails before that matters. KiDS, Local Group and MW not run.

## Checks
K1 cap off vs NR3 MEDIAN: |d| 0. K2 independent Q, capped/Q₀ 1.000, uncapped 2148. K3 identity 4.5e-14. K4 grid × 2, 6.9e-6, though M/M_c at r_h is 1 in that case, so it tests little. K5 M ≤ M_c, edge 9.8e-13, fixed point 1.0e-4. MUTATE ρ_lim × 0.1: Υ 1.20, bites. Reader rerun byte-identical.

**Implementation departures, made after the freeze, disclosed.**
1. The criteria said 12 damped steps. The test case showed 1.3e-2 at 12, against K5's 10⁻³, before any graded number, so the loop runs to 10⁻⁴, at most 200 steps. Same fixed point.
2. K5's monotonic line: min dM is −1.26e33 kg, roundoff from a large stand-in in the cumulative sum, about 6e-13 of a cluster's mass. It was seen on the graded output, and the reader then given a tolerance of 2e34 kg (10⁴ M☉). Written strictly, K5 would have failed on this roundoff. The verdict doesn't rest on it, but the tolerance was set after the fact.

κ = ½ FITTED. Not theory closed.
