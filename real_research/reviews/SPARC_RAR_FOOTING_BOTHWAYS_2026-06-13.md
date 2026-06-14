# The both-ways footing check on the SPARC RAR a0 — and a self-correction (2026-06-13)

*Verifying the standing "a0=9.36e-11 is within ~0.3% of optimal under unweighted dex-scatter" claim
on the REAL 175 SPARC rotation curves (data/sparc_data/*_rotmod.dat, Lelli+2016), per the project's #1
working rule: test on the framework's own footing, verify a favorable claim as hard as an unfavorable
one, and report the convention-robust truth in BOTH directions. Script:
`reviews/sparc_rar_footing_bothways.py`, deterministic, no synthetic data, 175 galaxies / 2807 points
after the standard err/V<0.1 cut.*

## What the data actually says (unweighted rms dex-scatter, McGaugh interpolating RAR)

| Footing (Υ_disk) | unweighted-dex-OPTIMAL a0 | a0=9.36e-11 offset from optimal | scatter penalty of 9.36e-11 |
|---|---|---|---|
| 0.50 (McGaugh standard) | 1.128e-10 | **−17.0%** (low) | +0.0030 dex (+2.1%) |
| 0.60 (midpoint) | 9.275e-11 | **+0.9%** | +0.0000 dex (+0.0%) |
| 0.70 (framework's stated footing) | 7.777e-11 | **+20.4%** (high) | +0.0027 dex (+1.9%) |

The RAR scatter floor is ~0.143–0.147 dex at every footing (consistent with McGaugh's ~0.13).

## The honest read (both ways — and a correction to the earlier note)

**1. The "a0 is ~20% too low" claim is NOT robust — it is the McGaugh-Υ=0.50 footing artifact.**
Raising the stellar M/L from 0.50 to 0.70 raises g_bar and moves the unweighted-dex optimum DOWN from
1.13e-10 to 7.78e-11 — a **36.7% swing from M/L alone**. The optimum **brackets** 9.36e-11: it sits
*above* the framework value at Υ=0.50 and *below* it at Υ=0.70. The sign of the "deficit" flips inside
the standard M/L range, so "20% too low" is not a property of the equation — it is a property of the
convention. 9.36e-11 is **convention-compatible** with the SPARC RAR magnitude.

**2. SELF-CORRECTION (favorable claim verified, found overstated): the "within 0.3% of optimal at
Υ=0.70" framing was wrong.** At Υ=0.70 the optimum is 7.78e-11 and 9.36e-11 is +20% *high*, not 0.3%
away. The near-exact coincidence (+0.9%, zero scatter penalty) lands specifically at **Υ≈0.60**, not
0.70. The earlier memory note conflated "there exists a footing where 9.36e-11 is near-optimal" (TRUE,
at Υ≈0.60) with "the framework's own Υ=0.70 lands on it" (FALSE — that footing undershoots). Banked as
a correction, exactly as the working rule requires: a manufactured-precision win is penalized as hard
as a reflexive kill.

**3. The genuinely robust, convention-independent statement (stronger than the original note):** the
data does **not convict** 9.36e-11 (no robust deficit — the optimum brackets it, sign-flipping with
M/L) and does **not uniquely select** it (no robust win — the χ² is flat-bottomed, penalty ≤2% / ≤0.003
dex across the whole Υ∈[0.5,0.7] range, and the optimum itself swings 37% with M/L). The SPARC RAR
magnitude is **consistent with but non-diagnostic of** the framework a0. This is the same conclusion the
honest anchor (`reviews/sparc_rar_honest.py`) reaches from the H0-hostage side: a0 ~ cH0 to an O(1/6)
coefficient that the z=0 magnitude alone cannot resolve.

**4. SELF-CORRECTION (added 2026-06-13 PM — the analysis above used the WRONG interpolation; both-ways cuts
both ways).** Sections 1–3 fit the RAR with **McGaugh's** ν, which is NOT the framework's interpolation. On the
framework's OWN de Sitter–Unruh derived ν, **g_obs = √(g_bar² + g_bar·a0)**, the picture at Υ=0.70 is *friendlier*
to the framework, not a deficit:

| interpolation @ Υ=0.70 | optimal a0 | 9.36e-11 offset | scatter penalty |
|---|---|---|---|
| McGaugh ν (used in §1–3) | 7.78e-11 | **+20% (high)** | +1.9% |
| simple ν | 7.54e-11 | +24% (high) | +2.4% |
| **framework dS–Unruh ν (the right one)** | **1.03e-10** | **−9% (BELOW optimal)** | **+0.51%** |

So under the framework's own interpolation, 9.36e-11 is within **~0.5% of optimal scatter** (the published
paper's "within 0.3% of optimal scatter" is **DEFENSIBLE**, not overstated — my AM reading that called it
overstated was itself the artifact: it used McGaugh's ν). The optimal a0 + the penalty depend on BOTH the M/L
AND the interpolation; across {McGaugh, simple, dS-Unruh}×{Υ=0.5,0.7} the optimum spans ~7.5e-11…1.8e-10 and
the penalty is ≤~2% worst case (≤0.5% on the framework's ν). **The convention-robust truth is unchanged in
spirit — small penalty everywhere, non-diagnostic — but the honest framing is "9.36e-11 is within ~0.5% of
optimal on the framework's own ν," NOT "+20% high." Neither a "~20% too low" (McGaugh-Υ=0.5) NOR a "~20% too
high" (McGaugh-Υ=0.7) deficit is robust; both are interpolation/M-L artifacts. Do not manufacture a deficit
from the wrong ν.**

## Caveats kept both ways
- This is a0 MAGNITUDE at z=0 only. It does NOT test a0(z) (the one distinctive claim — untestable on
  disk), and does NOT single out Z (the coefficient is H0-hostage; any H0∈67–73 makes cH0/Z fit).
- A higher M/L is itself a framework CHOICE, not a free win. The honest statement is magnitude
  *compatibility* across conventions, never that 9.36e-11 is data-selected.
- Independent spot-checks (this run): optimum 1.128e-10 @ Υ=0.50 reproduces sparc_rar_honest.py's
  1.129e-10; 175/2807 galaxies/points; scatter floor 0.143–0.147 dex.

## Disposition
No verdict change to the framework's empirical standing — the SPARC anchor remains "solid real-data
MOND phenomenology, coefficient unresolved." What changed is the PRECISION of the both-ways footing
statement: the deficit is a footing artifact (correct), but so was the "0.3% at Υ=0.70" win — the
truthful version is the **bracket + flat-bottom**: convention-compatible, non-diagnostic, both ways.
Quarantine held (Z never asserted from this fit; the coefficient stays H0-hostage).
