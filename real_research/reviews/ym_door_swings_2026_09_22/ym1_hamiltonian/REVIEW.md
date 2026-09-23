# Independent adversarial review (2026-09-22)

Two fresh reviewers were each told to find errors. Neither saw the other's
report. Both reran the scripts from scratch copies, and neither edited any
file.

## Reviewer 1: Hamiltonian proof §§2–6, the tree bounds and `verify.py`

**Verdict: Theorem 1 and the X_d table are proven, modulo fixable
presentation gaps. Nothing fatal.**

The reviewer tried to construct a configuration in which compatible
polymers fail to factorise, and could not. It checked independently that
every polymer is counted by the slot-labelled tree, that the label factor
is 16, that each edge contributes 1/c, and that K* = 6⁶/7⁷ and A ≤ G² hold.
The contact dichotomy is exhaustive, #edges ≤ 4m holds, the use of μ_b is
legitimate, the (C2) inclusion–exclusion is exact, and the constants
recompute as λ_*/C_F = 6.21372×10⁻⁴/(d−1) and X = 131.02 / 185.29 / 226.93.

| gap flagged | resolution |
|---|---|
| Ueltschi's hypotheses |1+ζ| ≤ 1 and ∫d|μ_b|e^a < ∞ not stated | stated in §6 |
| "each slot carries at most one edge" left implicit | stated in §5 |
| (C1)–(C3) attributed to (4) without the derivation | derivation (6.3) written out |
| Γ_{0t} sum only sketched | marked-path argument written out in §7 |
| rounding 131.1 vs 131.02; "below 0.04" marginally false; `REVIEW.md` missing; grid rows sit on κ_B ≈ K* | "rounded up" stated; 0.041; this file; grid rows marked NOT CERTIFIED in `verify.py` and §9 |

## Reviewer 2: Hamiltonian §7 with (F3)/(F4), and the Euclidean proof

**Verdict: both sound, nothing fatal.**

For (A), the reviewer checked the boundary factorisation with an entangled
ψ, the bounds ext ≤ ℓ, the three error terms (including the need for the
3K weighting), the Cauchy step and the absence of circularity. It
reproduced κ = 0.7695 K* and κ_B = 0.9412 K*.

For (B), it checked the TV lemma, the influence bound (the common factor
from the other plaquettes is absorbed into the reference measure ν), the
time-slice distance and the transfer-matrix facts. It also confirmed that
SZZ's normalisation converts to β_W = N² β_SZZ.

| gap flagged | resolution |
|---|---|
| Γ_{0t} path argument should cite κ < K*, not κ_B | rewritten; κ suffices, κ_B is a valid overbound |
| Euclidean statement must require β > 0 | added |
| Föllmer's ¼ and the definition of δ_i missing | added |
| "temporal gauge" wording loose for periodic time | rewritten: integrate all temporal links, which gives P_G |
| register correction overstated SZZ: the threshold is explicit, the rate is not, and it degrades with N | softened in PROOF.md, `ym2_continuum/REPORT.md` and README |

## Residual scope (unchanged by the review)

- Only the finite-volume, volume-uniform statement is proved. I15's
  infinite-volume GNS statement keeps its non-explicit Yarotsky
  threshold.
- `verify.py` checks arithmetic. The constants 16, 8 and 4m come from the
  analytic proof.
- The D = 2 exact cross-check in the Euclidean file cannot fail at these
  couplings. It is a sanity check, not a sharp test.
