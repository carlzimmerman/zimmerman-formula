# FS21: PRE-REGISTRATION of the neutrino mass-splitting ratio claim (frozen 2026-11-11; never edit, only append dated readings)

**The claim, as first written.** `zimmerman-formula/ai_slop/research/MASTER_VERIFICATION_TABLE.md` line 96 and
`ai_slop/ORIGINAL_README.md` line 212, both first committed 2026-06-01:
"Delta m^2_atm / Delta m^2_sol = Z^2 = 33.5", listed there as measured 32.6 (2.8 % off), test "JUNO, DUNE".
Z^2 = 32 pi / 3 = 33.510321638...

**Why freeze now.** The June files use two definitions of the atmospheric splitting (Delta m^2_31 in `DEEP_STRUCTURE.py`,
Delta m^2_32 in `GAPS_AND_NEXT_STEPS.py`; the table's 32.6 matches the 32 form). They differ by exactly 1.000 in the ratio, about
3 %, and JUNO will resolve that. The choice must be fixed before the data can make it.

**Disclosure: numbers seen before freezing** (NuFIT 6.0 as transcribed in `targets/pmns_2025.py`, provisional; JUNO 59-day
Delta m^2_21 = 7.50 +- 0.12; normal ordering). With Delta m^2_21 combined to 7.497 +- 0.101 (inverse-variance, approximate):
- |Dm31|/Dm21 = 33.80 +- 0.56 (IC19, no SK atmospheric; Dm3l 2.534) and 33.52 +- 0.53 (IC24, with it; Dm3l 2.513).
- |Dm32|/Dm21 = 32.80 and 32.52.
So the 31 form sits at 0.5 and 0.0 sigma from Z^2 and the 32 form at 1.3 and 1.9 sigma. **The 31 form is chosen as primary AFTER
seeing that it fits.** That is a post hoc choice and is charged as one extra trial below. (My chat message of 2026-11-11 had the
two NuFIT variants swapped; the assignment above follows the committed table.)

## The two frozen claims
- **C31 (primary):** R31 = |Delta m^2_31| / Delta m^2_21 = 32 pi / 3.
- **C32 (carried):** R32 = |Delta m^2_32| / Delta m^2_21 = 32 pi / 3.
R31 - R32 = +1 in normal ordering and -1 in inverted ordering, exactly. No third definition, no added constant, no running or
"correction" factor may be introduced later. The ordering is whatever is measured; neither claim assumes it.
Not registered: the June table's "m3/m2 = Z". It equals C31 only if the lightest mass is zero, which is not measurable soon and
conflicts with FS16's 2.24 meV assumption.

## Data rule
- Variants, never pooled: (a) each variant of the latest NuFIT release; (b) JUNO alone, once one JUNO analysis reports both
  Delta m^2_21 and |Delta m^2_31| or |Delta m^2_32|.
- If a source quotes only one atmospheric splitting, convert with |Dm31| = |Dm32| + Dm21 (normal) or |Dm32| - Dm21 (inverted).
- sigma_R by quadrature of the fractional errors (asymmetric errors averaged), unless the source gives the ratio or a correlation.
- Transcribed values are PROVISIONAL until checked against the source table; each reading names its source.

## Reading rule (per claim, per variant)
pull = (R - 32 pi/3) / sigma_R; precision p = sigma_R / R.
- |pull| <= 2: CONSISTENT. 2 < |pull| <= 3: TENSION. |pull| > 3: EXCLUDED.
- A reading is DECISIVE when p <= 1.0 %.
- **KILLED:** every available variant is EXCLUDED. A killed claim stays killed.
- **SURVIVED (DECISIVE):** p <= 1.0 % and every variant CONSISTENT.
- Otherwise OPEN, with the variant readings listed.
- **Final reading:** the first JUNO-alone result with p <= 0.5 %. At that precision C31 and C32 are 6 sigma apart, so at most one
  can survive.

## What a survival is worth (frozen now, so it cannot be inflated later)
- **This test can kill the claim. It cannot certify it.** The atomos gate needs a surplus of at least 10 bits. Supply at
  precision p is log2(1/(2p)): 6.6 bits at 0.5 %. Cost is log2(2 x 46) = 6.5 bits: two definitions times the 46 claims with an
  error column in the June table. Surplus about 0. A survivor is labelled **CURIOSITY (SURVIVED A PRE-REGISTERED TEST)**.
- **Forward value.** The status-at-freeze run computes, from the posteriors above, the chance that the final central value lands
  within 2 sigma_final of Z^2 if Z^2 has nothing to do with it (sigma_final/R = 0.4 %). A pass is worth at most the inverse of
  that chance as a likelihood ratio.
- No mechanism is offered. A survival does not support the framework's gravity sector, and a kill does not damage it.

## Hand estimate (mine, at freeze)
C32 is KILLED at the final reading. C31: about a one-in-three chance of surviving whether or not Z^2 means anything.
