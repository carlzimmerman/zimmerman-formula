# SC2_clone_rule_on_spec_lenses: FROZEN CRITERIA (committed alone, before any number from this lane)

**Question.** SI3's AMENDMENT A2 found that drawing a lens and then applying the veto skews the iso-random clones to high z and massive lenses, on KiDS's photo-z samples. P2, SI1 and SI2 build their hole term by the same rule. SI2's headline is LENSING TENSION GONE ON CLEAN LENSES, which gate G8 rests on. With per-lens clones, do SI1's and SI2's frozen classes change, and does P2's verdict?

**What is already known to me.** The committed tables of P2, SI1 and SI2, including P2's S3 lens/I weight line (1.052 to 1.376 by bin, 1.05 to 1.07 in O2) and its acceptances (0.450 on S3, 0.708 on S1). SI3's A2 result on KiDS. No S1 weight ratio, no z or mass skew on these samples, and no per-lens number exists yet.

## Rules
- **Old rule (frozen in P2).** `make_iso`: draw a lens from the sample with replacement, draw a uniform position in a GAMA box, keep the point if it meets the edge margin and the veto. S3: I3, 4 N points. S1: I1, 2 N points.
- **New rule (SI3 A2's design, no free parameter).** Every lens in the sample gets exactly its accepted clones, each carrying that lens's own z and lg M★: 4 per lens on S3 and 2 per lens on S1, the same totals as frozen. The positions, edge margin and veto are P2's own functions. Seed 20261031 + 4. Draws stop at 100,000 per lens, and any lens left short is printed.
- **Unchanged:** lens stacks, plain randoms R (P2's draws, same stream, because they have no veto), estimator, 36-patch jackknife, Hartlap, models, rungs, neighbour terms (recomputed by P2's own code for the new I points), statistic, classes and SI2's combined reading.

## Execution
All three lanes' text runs by asserted string replacement, never re-coded, and the only change to the physics is that block in P2's text. Nothing is written into P2, SI1 or SI2. The runs:
- **old:** frozen catalogues and P2's existing measurement cache. This is the check that the machinery reproduces the record.
- **new:** per-lens clones, the same counts. This is the graded comparison, and it is a fresh measurement of every centre.
- **k20 (reported):** per-lens clones, 20 per lens on both samples. A new realisation of I has its own noise: in Δχ² it is about 2D/√(k + 1), so about 1.15 D on S1 and 0.9 D on S3 at the frozen counts. A class flip could be that noise and not the rule. k20 cuts it to about 0.44 D.
- **MUTATE:** see below.

## Frozen outputs, in this order
**1. K_H3-style weight ratios, old rule first, then new.** Source weight per centre, (Σ WW_L / N_L) / (Σ WW_I / N_I), averaged over the range's bins, for in, O1 and O2, on S3 and S1. Also lens/R, and the mean z and mean lg M★ of the clones against the lenses.

**2. Regrade table, each footing, each of S3 and S1, never pooled.** Lines: all lenses R0 (SI1's frozen grade, with inner and outer); blue R0; red R0; red R2; all lenses R2 (SI2's frozen lines). Each with χ²(law), p, χ²(route E), p, Δχ² = χ²(route E) − χ²(law), D and class, old against new. Classes as SI1 froze them: NOT POWERED, LAW PREFERRED, ROUTE E PREFERRED, NEITHER. The raw L − R line is reported as in SI2.

**3. SI2's combined reading** (canonical, all lenses at R2), by SI2's own text, old against new: LENSING TENSION GONE ON CLEAN LENSES, TENSION REMAINS, or MIXED.

**4. P2's verdict** per footing and the lane line, old against new, with A_in, A_O1, A_O2 at cases (a) and (b) and S.

**5. Noise, reported.** I's own noise in Δχ² per line, from two halves of I with the covariance fixed: half A, half B, and half the jackknife error of their difference, on all lenses at R0 and R2.

**Reading rule.** A class is CHANGED if its string on the new run differs from old. Any change goes at the top of the README, and that includes a change k20 doesn't support. For each change the README says what k20 reads and how large the shift is against the noise. Nothing else is called a change.

## Checks (a failure in K1 stops the comparison; a failure in K2 to K5 makes the new column NO READING)
- **K1, old rule reproduces the record.** SI2's committed χ²(law), χ²(route E), Δχ², D, p and class on every line, both samples, both footings, and its combined reading. SI1's committed all, inner and outer lines and classes. P2's committed verdicts, S3 Δ, sigma, model (a) and (b), amplitudes, and its two weight lines. |d| ≤ 1e-9.
- **K2, the clone rule.** On the new run every lens has exactly its count, and every clone's z and lg M★ equal its lens's exactly. Every point meets the edge margin. P2's brute-force veto on 200 points per sample finds 0 violations.
- **K3, only I changed.** Per-centre WG, WW of lenses and R equal the old run's within 1e-9, relative to the largest. The raw L − R lines equal the old run's within 1e-9.
- **K4, nulls on the new I.** Cross-shear of Δ (P2's K4 statistic) and half A − half B of I, each p ≥ 0.001, on S3 and S1.
- **K5, weight ratio.** New rule's O2 ratio within 0.10 of 1 on S3 and S1, SI3's K_H3 limit.
- **MUTATE (separate outputs, canonical only).** Every lens's clones take the z and lg M★ of lenses from the top half of the sample's z. K2 and K5 must fail, χ²(route E) must change on every line of the all-lens R0 and R2 rows, and the run must print NO READING and exit 1.

## What this cannot show
- Whether I is right beyond this one flaw. Per-lens clones match z and mass. They do not place clones on the lens's own footprint or match colour. SI2's disclosure stands: its hole term for red and blue lenses is the sample's full stack.
- Neighbours fainter than r 19.8 are in neither model, as in SI1. R2 stays an open choice, as in SI2.
- SI1's reported variants (M★ ± 0.2, cut at R200, shift scan), SI2's reported sensitivity tables, and AS1, which runs SI2's text, are not regraded here. Their I is the old one.
- It says nothing about KiDS's photometric samples, which are SI3's.
- A preference compares two members of this record only.

## Resources
One thread, `nice -n 15`, under about 2 GB, at most two processes at once. If this costs much more than about 90 minutes of CPU, I stop and report what I have. Nothing outside this lane is written except scratch work files.

κ = ½ FITTED. Footings never pooled. Cold dark energy is a gravitating field component, never a particle. The theory stays open. Nothing here says the data favour the framework.
