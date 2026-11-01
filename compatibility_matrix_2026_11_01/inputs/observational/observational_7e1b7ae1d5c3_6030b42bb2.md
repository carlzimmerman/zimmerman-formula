# DR6_outer_key_projection: NO VERDICT as frozen, because the MUTATE line failed (0.16 against 0.5). The measured numbers read NO SUPPLY [BREAKS OTHERS] [CEILING INSUFFICIENT]: a native two-halo term doesn't close G-OUT-M3 on measured gas

Criteria: `FROZEN_CRITERIA.md` (bbf9dbc511), committed alone first. `dr6_pk.py`, `dr6_inject.py`, `dr6_grade.py`, `dr6_amp.py`, `dr6_post.py`; outputs `dr6_pk.out`, `dr6_pk.json`, `dr6.out`, `dr6_results.json`, `dr6_amp.out`, `dr6_amp.json`, `dr6_post.out`, `dr6_post_x10.out`. κ = ½ FITTED, unused. Cold dark energy, never a particle. Not theory closed. Nothing here says the data favour the framework. Not blind.

**The door was half closed already.** GC1 (09280e4b66) showed the term beyond r_ta projects as a flat sheet. This lane adds the native P(k), ZN4's chain and the part inside r_ta.

## Why there is no frozen verdict
MUTATE (C2 sign flipped) moved G-OUT-M3 by +0.16, C2 itself −0.13. The frozen line was 0.5, so by my own rule: no verdict. The line was set from my expectation of a large term, and that expectation was wrong. The move is opposite in sign and about equal in size, and the post-result ×10 run below is close to linear in the band, so the term does reach the keys. That reading is post-result and doesn't restore a verdict. All other checks pass: K1 |d| 0, K2 σ₈ 0.8260, r_d 147.13862, K3 ratio 1.0004, K4 b(ν=1) 1.00002, K5 0.0001.

## Requirement and supply: gas +0.005, worst and best h
G-OUT-M3 needs pred +0.284 (+27 %) at f★ 0.034, h 0.672; +0.217 (+21 %) at its easiest cell (f★ 0.0615, h 0.686).

| variant | G-OUT-M3 Z, f★ 0.034 (h 0.672 / 0.686) | f★ 0.0615 | supply fraction | keys |
|---|---|---|---|---|
| ZN4, no term | +4.41 / +4.07 | +4.13 / +3.81 | | 12 of 15, 12 of 15 |
| C1, beyond r_ta | +4.41 / +4.07 | +4.13 / +3.81 | 0.000 | 12, 12 |
| C3, up to the linear density only where the model is below it | +4.46 / +4.12 | +4.18 / +3.86 | **−0.020 to −0.027** | **11**, 12; G-OUT-M2 goes over, +2.00 / +2.09 at f★ 0.034 |
| C2, ceiling, double counts | +4.28 / +3.94 | +4.00 / +3.68 | +0.055 to +0.073 | 12, 12 |

G-OUT-Mall: C1 −0.02, C3 −0.05 to −0.07, C2 +0.17 to +0.23. G-MID-T3 doesn't move usefully: +2.17 → +2.19 under C2. X-COP unchanged by construction. Groups and SPARC weren't given the term.

**Direct amplitude, M3 median** (z 0.30, lg M₂₀₀ 14.44, ν 2.38, b 3.78), no exclusion, RF5's P(k): ΔΣ_2h 1.29, 1.44, 1.60 M☉/pc² at R = 1.42, 2, 3 Mpc. For scale, ZN4's shape gives about 41.5, 25.8, 14.6 at those radii (a side calculation, not the grader's number), so even with no exclusion the term is 3–11 %, against +27 %. The grader's C2 gives about +1.5 % because removing ξ inside R₂₀₀ takes out most of the signal.

**The expectation on record was wrong in two ways.** I expected C2 to clear M3: it supplies 6–7 %. I expected C3 to supply something: it has the wrong sign. Mass added beyond about 3 Mpc sits outside the band and lowers ΔΣ there.

## The questions asked
- **Do the shear keys contain it?** Yes. X7's stacks are cluster minus random, and neither X2 nor X7 models or removes a two-halo term. So prediction and data must both carry it; nothing has been subtracted. (The "2h" in X7's array comments is the two h cells.)
- **Other keys.** The term scales the wrong way with mass. At ×10 (post-result, not a rule): G-OUT-M1 pred 0.315 → 0.790, G-OUT-M3 1.040 → 1.198, M3 still +3.07, and G-MID-T2, G-MID-T3 fail. A bias of 1.5 to 3.8 can't overcome the low-mass bins' smaller one-halo signal. The data's shortfall grows with mass; this term's relative share falls with it.
- **Double count.** Yes inside about 2.5 R₂₀₀, no beyond. ρ_model/ρ_lin for M3's median: 2.57 at 1.5 R₂₀₀, 1.75 at 2, 0.63 at 3, 0.33 at 5, 0.27 at 0.9 r_ta. The band's neighbourhood is already above the linear expectation. Further out the model is below it, and C3 fills that (median 41 % of the total budget added), but that mass doesn't help the band.
- **The sphere.** The standard zoom is RS **1.5** q_M. RS 2.0 was only VB1's run B. x_edge is about 7 R₂₀₀.

## Correction to my own criteria
The criteria argued GC1's reason fails on this chain because of the tail's thin shell. For M3 that's mostly untrue: x_edge R₂₀₀ < r_ta in 12 of 109 clusters at this x_edge (approximate, one x_edge), so most M3 clusters take the zoom's shape cut at r_ta, with no tail. GC1's conclusion stands anyway, as the numbers show.

## Corrections to the outside claim
ZN4 on +0.005 is 12 of 15: G-MID-T3, G-OUT-M3, G-OUT-Mall. 14 of 15 is OP2. The band is 1.42–3 Mpc physical, about 1.1–2.4 R₂₀₀ for M3's median, not 2.18–3.17 R₅₀₀.

## Limits
- Linear ξ, no native nonlinear model. Peak-background bias is standard, with native inputs only. The zooms' own P(k) stays EM1's Background A, a Λ refit.
- RF5's cell is a window, on compressed plik-lite, not a pass.
- OP2 not graded. By arithmetic the ceiling's −0.13 takes +2.39 to about +2.26, still failing, and it double counts.
- `dr6_post.py`'s ΔΣ scale is a median-cluster estimate.
