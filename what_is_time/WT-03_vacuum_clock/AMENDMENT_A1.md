# WT-03 — AMENDMENT A1 (appended after the frozen run; criteria c9ea722b6 are not edited)

Written 2026-10-21 after `wt03.py` (main and MUTATE) had run. Nothing here changes a frozen rule, threshold or verdict. Items 1–3
come from a coordinator note (WT-01 record map) received after the run; item 4 discloses the post-hoc script.

## 1. Branch A — the unimodular law (record, added; IDENTITY)

The record carries two a0(z) branches. They are reported separately and never pooled.
- **Branch A** (`campaign_fresh_gravity/CFG6_README.md`, 3409d12da, lines 27–30 and 284–286; XR20 T1, CFG43, XR30): a0 reads the
  Henneaux–Teitelboim integration constant, so it is **exactly flat for any dark-energy history**. CFG6's recommendation is
  "Keep A as the framework's prediction" (pre-registered 0.00 dex at z ≈ 2.5).
- Under Branch A, d ln a0/dt ≡ 0. The vacuum clock has **no direction and no rate**, whatever CFG689's band does. This is an
  identity, not a measurement; it carries no verdict weight, and nothing in §§5–7 of the criteria applies to it (no NEC demand
  arises, because a0 does not read ρ_DE(z)).
- **The tracking reading** (owner rule 2026-10-06; the CFG689 band as presented in THEORY_CANONICAL draft §3.8) with CFG911's three
  readings ε / −p / V is the lane's main analysis, as frozen.

## 2. The rival a0 ∝ H(z) is not viable (record, added)

`fable_independent_2026/L37_RECOMBINATION.md` (f64b01921) and HANDOFF_CONTRACT A34: the ρ_total (rival) footing tilts n_s at
recombination by **27σ** (only A_s and n_s marginalised in that lane). The rival is used here **only** as the MUTATE control and
as a comparison drift in (e). It is not treated as a viable branch.

## 3. The −p reading vs the stage-17 pressure law (record, added; scope note)

HANDOFF_CONTRACT A34: the stage-17 pressure law a0² = κ²G(−p_Q) and the ρ_Λ reading differ by 167–490× at z = 1100 and
coincide only at z = 0. This lane's −p reading uses −p_DE reconstructed from CFG689's ρ_DE(z) over z ≤ 2.33 only; it says nothing
about z = 1100.

## 4. Post-hoc script `wt03_posthoc.py` (written after the run; reported only, no verdict weight)

Prompted by two things in the frozen run: the 68% RISE of segment 0.7–1.0 at ρ_adj = −0.5 sat within Monte-Carlo noise of the
line (p_rise 0.84149 vs 0.8413), and K1b flagged "APPROXIMATION OFF" at z 1.0/1.5/2.33. Contents:
- PH0: code equality with the frozen run (same seed, same draws).
- PH1: the ρ_adj at which segment 0.7–1.0 stops being RISE_68.
- PH2: net intervals [0, 0.4] and [0, 0.7], which are not in the frozen set.
- PH3: the correlations APPROX-G omitted, fitted to the stored joint quantiles `sqrtX_q`, and the segment flags under the fit.
- PH4: the same ε segment classifier on CFG689's committed bracket modes (θ* modes reported only: CFG689's K9 failed as frozen).

The frozen verdict is the one in the README's verdict table. Every post-hoc number is labelled POST HOC.
