# FRZ6R AMENDMENT A1 (2026-11-13): a relative bite rule for twin TW1, added as a reported reading; the as-frozen rule stays first

Committed alone, while the main run is live and before any graded number from it has been read. The frozen criteria
(4314f23c90) are not changed. Every label is first computed and reported with the frozen rules.

## Why

I ran the whole pipeline once as a throwaway test in scratch space, outside this folder: N = 48 (dx about 0.42 Mpc/h, eight times
coarser than the frozen N = 384; 18 % of gas pixels floored), 3 seeds. Those numbers are not results and are not used. On that
test the frozen TW1 rule did not bite on either footing (anchor-bin Delta chi^2: TW1 0.22 / 0.15 against J2 0.0005 / 0.0017
for canonical / alt), because of its absolute floor: section 7 requires |A_TW1 - A_J2| >= max(0.25 A_J2, 1.0). When the split's
own A is many orders of magnitude below 1, a twin can change A by a factor of several hundred and still fail the floor of 1.0.
The floor was meant to stop noise from counting as a bite. It does not test whether the boundary is implemented.

## Added reading (reported beside the frozen word, never replacing it)

TW1 bites (A1 rule) if both hold, at the anchors over all seeds:
- the change is large relative to the case: A_TW1 / A_J2 >= 1.25 or <= 0.8;
- the change is resolved against seed noise: |A_TW1 - A_J2| > 2 sqrt(SE_A(TW1)^2 + SE_A(J2)^2), where SE_A is the delete-one
  jackknife over the seed index of the anchor statistic A (the formula of section 5, applied to A).

The labels are then recomputed with this TW1 rule and everything else frozen. They are reported as "A1 reading". The frozen
TW2 rule is unchanged.

## Order in RESULT_BLIND.md

The as-frozen labels come first. The A1 reading follows, marked as an amendment reading.

kappa = 1/2 FITTED; not theory closed. Adopts nothing.
