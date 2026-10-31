# NF1_no_floor_rule: FROZEN CRITERIA (committed alone, before any script or graded number)

**Question.** ET1 and ET2 measure the S = ρ₀r₀ that SPARC asks for below 150 km/s: 69, 103, 143 M☉/pc² with M200 (ET1) and 70, 108, 158 free (ET2), a rise with ρ about +0.56 to +0.60. Against that, a flat floor reads MIXED. FC1's collapse branch, continued below its crossing with η held flat, gives about 48, 69, 94 at those bins' masses by hand. That runs parallel to the need at about 0.65 of it. So: does route E need the floor at all? Does the SPARC line pass with the collapse branch alone?

**Why it matters.** The floor is the only place a₀ enters route E. With no floor the two footings coincide on SPARC, X78's alt failure stops applying to route E, and a₀ = κc√(Gρ_Λ) plays no role in the cold sector at all. That would be a change to the theory's headline, so a pass would be an open question for the owner. It would not be a result to adopt.

**Already known to me (not blind).** The hand numbers above; ET1, ET2, FC1, LS1 tables. I have not run this rule through any grader. The record has no graded no-floor rule at this S; EM1's NFW and DC14 fits were cusped and fail the Υ leg (0.36, 0.47).

## Rule
X74's grader with FC1's conversions (commit 061b2e2a1a), CE1's median η, X73 PRIMARY, f★ 0.034. Replace S = max(Σ_a0, f_c η Σ_coll) with S = f_c η(M_t) Σ_coll(M_t), M_t = M/f_c, at every mass:
- **N0 (primary):** η flat below 10¹², the grader's own interpolation. No extrapolation of η.
- **N1:** below 10¹², η × 10^(s (12 − lg M_t)), s = 1.25 × ½ log₁₀(8.05/5.72) = 0.0928: CE1's c-equivalent trend over 10¹²–10¹⁴.
- **N2:** the same with s = 1.25 × log₁₀(8.05/5.92) = 0.1668: the trend over 10¹²–10¹³.

N1 and N2 extrapolate a native trend to masses no zoom has reached. X80 will measure them. Neither s is fitted to SPARC.

## Frozen labels (from the SPARC line, EM1's `line`: rms ≤ 0.110 and median Υ in [0.50, 0.80], both backgrounds)
- **FLOOR NOT NEEDED:** N0 passes.
- **TREND-DEPENDENT:** N0 fails, N1 or N2 passes.
- **FLOOR NEEDED:** all three fail.

A pass here is a SPARC statement only. It does not grade dwarfs, lensing perturbers or the RAR's tightness.

## Reported
- rms and Υ against FC1 (0.0687 / 0.0700, Υ 0.51 / 0.50) and the law.
- By V_flat (LS1's bins, Υ 0.50): n, median Υ, ΔV, and S_rule against ET1's and ET2's intervals.
- S_rule at lg M200 = 8, 9, 10, 11.

## Checks (any failure makes the verdict NOT DECIDED)
- **K1:** with the floor restored the run reproduces FC1's SPARC rms and Υ and all cluster predictions, both footings, |d| ≤ 1e-9.
- **K2:** under N0, canonical and alt SPARC rms and Υ are identical, |d| ≤ 1e-9. If not, a₀ enters somewhere I have not understood.
- **K3:** clusters and groups under N0 against FC1: max |ΔZ| printed. It should be 0, since the floor is off there. A nonzero value is reported, and the affected keys listed.
- **MUTATE:** S × 0.5 under N0 raises median Υ on both backgrounds.

## What this cannot show
- It does not measure low-mass S. Zooms stop at 10¹²; X80 is queued.
- Zooms make cusps (X81), and the core shape here is chosen. So this is not "collapse alone explains SPARC": the shape is still imposed.
- EM1's M200 at low mass is an extrapolated fit. ET1's mutation shows the low-mass S depends on it, though ET2's free fit does not.
- It leaves unexamined why rotation curves follow a tight RAR with a scale near a₀ if a₀ has no role. That coincidence would then need an account.
- Dwarf and perturber limits (PC1's ceiling, IC 1613, J0946, ultra-faints) are not graded and would change.

κ = ½ FITTED. Footings never pooled. Cold dark energy is a gravitating field component, never a particle. Not theory closed. Nothing here says the data favour the framework.
