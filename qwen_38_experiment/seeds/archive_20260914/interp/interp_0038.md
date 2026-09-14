# interp_0038 -- the recombination off-switch X bounds the PMNS solar angle

Seed 0038 is a random collision. Read charitably, all three bullets point at ONE
dimensionless number X that both bullets share:

   * bullet 1 (duality): a duality that "exchanges the off-switch at recombination"
    (the ionization / radiation->matter transition at z_rec) has a value that BOUNDS
    the PMNS solar mixing angle sin^2(theta_12) ~= 0.307.
   * bullet 2 (renorm): the beat between m_W/m_Z = 0.8814 and its dual renormalizes
    into the two-footing fork {a0 = 9.3619e-11, a0 = 1.1279e-10 m/s^2}.
   * wildcard: the single number BOTH bullets share, if true, is X ~= 0.307.

## Hypothesis (one sentence)
X = 0.307 is the recombination off-switch duality value, and it is simultaneously
(a) the PMNS solar mixing sin^2(theta_12), and (b) the renormalization image of the
m_W/m_Z beat into the a0 two-footing fork; i.e. X_rec ~= X_beat ~= 0.307 within the
kappa-scale tolerance.

## Exact quantities
- X_pmns = sin^2(theta_12) ~= 0.307 (PMNS solar mixing; seed value).
- X_rec  = recombination off-switch duality = z_rec / z_eq, z_rec = 1089.7,
           z_eq = 3384 (Planck 2018) -> 0.322. Flag convention: z_rec, z_eq vary ~5%
           by dataset; alternative off-switch T_rec/T_eq ~= 0.49 is a competing def.
- X_beat = two-way beat m_Z/m_W - m_W/m_Z = 1/0.8814 - 0.8814 = 1.1345 - 0.8814 = 0.253;
           renorm target = footing ratio R = 1.1279e-10 / 9.3619e-11 = 1.2048.
- footings: a0 = 9.3619e-11 and 1.1279e-10 m/s^2 (dimensional steps use BOTH).

## Exact test
1. Collapse: |X_rec - X_pmns| = |0.322 - 0.307| = 0.015 < tol = 0.043 (kappa fit
   uncertainty 0.551 +/- 0.043).
2. Bullet-2 bridge: a fixed, pre-declared renorm map r(beat) sends the beat 0.253 (or
   m_Z/m_W = 1.1345) onto a footing value or onto X within 2 sig figs; record which.
   This is the loose link -- flag it honestly, do not dress it up.
3. Dimensional checks run on BOTH footings.

## Kill conditions (any one => REFUTED / NULL / DISCARD)
- X_rec != 0.307 beyond tol = 0.043 (esp. if the off-switch resolves to T_rec/T_eq
   ~= 0.49 or z_rec alone, which fail).
- No pre-declared renorm map sends the m_W/m_Z beat to a footing or to X within 2 sig
   figs -> bullet 2 is NULL.
- The "duality" is a pure unit/normalization artifact -> CONVENTION, not a hit.
- X = 0.307 is itself a pure CONVENTION match (normalization artifact).
- X collapses onto kappa = 1/2 (fitted 0.551 +/- 0.043) -- do NOT count that as a hit.

## What it is NOT
A hypothesis, not a derivation. X ~= 0.307 is NOT claimed derived; if the numbers
collapse it is a coincidence to be chased, not a proof. Do not count kappa = 1/2 here.
