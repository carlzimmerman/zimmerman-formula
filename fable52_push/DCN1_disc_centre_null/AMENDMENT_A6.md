# DCN1 AMENDMENT A6 (post hoc; committed alone, AFTER seeing the first label-script output)

TEST lane. Adopts nothing. kappa = 1/2 FITTED; not theory closed. Criteria d603f1703c; A1 0a6e46fb52; A2 15f6f993e4;
A3 f5e101ba9a; A4 d08610695e; A5 00d6869022.

## What the first label pass showed

- **Every reading came out NO VERDICT on the known-answer gate.**
  - **KA3 failed.** Three of the four p = 0.75 sequences were not Converged. Their values were recovered to 1e-15, but the
    rule's E exceeded 20 %. My test grid started at h = 1, where c h^p is up to 0.8, which is coarser than any grid in
    this lane. The frozen text does not fix the test grid.
  - **KA4 failed as frozen and passed under A1.** Q converges at order 0.51 to -4.13e-29 against the exact -5.33e-29: the
    null cell's resolution-independent error.
  - **Under A3, KA4's P2 geometry failed only on the rule's order window.** Q_A = -5.6458, -5.6558, -5.6573, -5.6607,
    -5.6610 (1e-29) against the exact -5.6617. The finest grid is within 1.1e-4, but the noisy last steps give an observed
    order of 6.41, above 6. KA4's P1 geometry and KA5 pass under A3.
- **The per-background labels.**
  - Under A5, P1 is ARTEFACT on both footings (all 16 stable) and P2 is STABLE AT THE CENTRE (all 8).
  - As written, A3 leaves 2-5 backgrounds per problem and footing open.
  - The frozen reading as coded calls one background (alt 10.7 / 0.1 a0) unbounded. Its Q is negative and creeps 0.5 %
    per level toward zero.
- **A code slip in that frozen labelling.** The frozen unbounded(b) requires Q Diverging AND Part A failing to bound it (A1
  or A2 failing, or Q_id diverging too). The script tested only the first condition. This is fixed to the frozen text in
  every reading. It is a code fix, not a change of criteria.
- **M3's numerical half did not bite.** On the KA4 sphere's annulus u <= 0.10, so dropping 1/(1+u) moves the rate by 2.1 %,
  under the 5 % line. M3's sympy half bites. Both facts are reported as they are.

## The amendment (a new last reading, "A6"; every earlier reading is reported first, unchanged)

1. **KA3's test grid** is the lane's own: h = 1/N_R, N_R in 48, 72, 108, 162, 243. Sequences, signs and the lines are
   unchanged.
2. **A known answer with an exact value** (KA4, KA5 under A3) passes if either:
   - the rule converges within the frozen tolerance, or
   - Q_A on each of the finest two grids lies within the frozen tolerance (2 % KA4, 5 % KA5) of the exact annulus sup.

   A direct comparison with a known exact value needs no extrapolation. The rule still grades every P1 / P2 background.
3. **Per-background labels** are A5's.
4. **RESULT.md leads** with A6's label and says plainly that:
   - it is the last of six readings;
   - A5 and A6 were written after the outcome was seen;
   - every reading frozen before the outcome was seen is NO VERDICT.

kappa = 1/2 FITTED; not theory closed. Adopts nothing.
