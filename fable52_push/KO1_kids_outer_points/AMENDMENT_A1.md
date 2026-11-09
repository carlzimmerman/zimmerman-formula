# KO1 AMENDMENT A1 (post hoc: written after the first run, whose numbers have been seen)

Committed alone, before `ko1.py` is changed or re-run. It changes one known-answer check's expectation and one reported
item's background. It changes no statistic, cut, gate, line or label rule.

## What happened

The first run (`ko1_run1_KA5_fail.out`, `.json`, kept) passed KA1, KA2, KA3, KA4, the numerics and coverage checks and the
cross-shear null, and failed KA5. By the frozen rule its label is NO VERDICT.

## 1. KA5: the check was wrong, not the pair finder

- As frozen, KA5 plants synthetic objects around 4,000 lenses (1,000 real hosts and 3,000 controls) and expects each lens to
  be affected only by the object planted for it.
- As implemented, all 4,000 objects go into one pool. An object planted for one lens can lie inside another picked lens's
  range and qualify as its host. The run shows it: 285 host-free lenses flipped against 241 planted on host-free lenses, 44
  more than expected. Hand estimate of the cross-talk: 4 objects per square degree, discs of 0.1 to 0.3 square degrees, about
  half heavy enough, about a quarter inside the window, so roughly 5 % of the 900 host-free lenses picked, about 45.
- **Replacement.** The expectation is computed by brute force over all 4,000 x 4,000 (lens, synthetic object) pairs with the
  frozen host definition (mass threshold, projected radius, no window), independently of the tree: the expected minimum
  distance is the smaller of the value before planting and the smallest |Delta chi| of the qualifying synthetic objects. The
  check passes if the tree-based finder returns exactly that array (1e-6 Mpc) and, separately, if every lens with its own
  planted host at 50 Mpc has a minimum distance of at most 50 Mpc. This is a stricter test of the finder than the frozen one.

## 2. R4: the chance level is not flat

- R4 as frozen takes the pair count at 300 to 500 Mpc as the chance level. The pool has finite depth, so chance pairs thin
  out with |Delta chi|, and the excess at 100 to 300 Mpc is overstated (the first run's "share inside 230 Mpc 0.77, inside
  115 Mpc 0.22" disagrees with CFG502's measured pair scatter of about 115 Mpc for that reason).
- **Replacement.** The chance histogram is the same scan with the lenses' sky positions shuffled among lenses (seed 52),
  each lens keeping its chi, mass and radius. R4 stays a reported item.

## 3. What has been seen (so nothing below can be called blind)

Primary, first run, canonical / alt: A_hf 1.098 +- 0.154 / 0.999 +- 0.141 on 40,667 host-free lenses (outer-weight share
0.290; cut Delta 0.3 dex, W 230 Mpc chosen by the frozen rule); W10 stack 1.707 +- 0.086 / 1.553 +- 0.078; hosted
2.009 +- 0.107 / 1.828 +- 0.098; hosted minus host-free +0.912 +- 0.186 / +0.830 +- 0.169; two-phase exterior 0.056 / 0.051
(share) and 0.463 / 0.422 (cap); mass-scatter factor 1.274; label by the frozen table on both runs of the rule: LAW LEVEL
HOLDS. Reported items seen: the isolation shells, the type, mass and redshift subsets (host-free late types -0.19 +- 0.39,
early types 1.34 +- 0.18, canonical), the host-count trend, the four settings, near / far sources, and the published tables
(GAMA isolated 0.97 +- 0.28 against KiDS-bright isolated 1.50 +- 0.08; hot-gas variant 0.47 +- 0.04).

## 4. Extras, declared here before they are computed (`ko1_extra.py`; reported only, no label rests on them)

The reported subsets show a split the pooled statistic hides: the host-free outer signal is carried by early-type, massive
lenses, and host-free late types show none. Because this was seen after the freeze it cannot be a gate. What will be
computed, and what each reading would say, is fixed now:

- **E1, profiles.** g_obs / law in all 15 bins for host-free lenses (all, late, early), for W30 (all, late, early) and for
  hosted lenses by type. Three windows: outer (bins 0 to 3), middle (bins 4 to 6, g_bar 9.7e-15 to 5.3e-14) and inner (bins 7
  to 12, g_bar 5.3e-14 to 1.6e-12, the window in which the record measured blue lenses on the law).
  - If the missing outer signal of late types is an artefact of badly placed lenses (photo-z outliers), their inner
    amplitude is low too.
  - If the law is the lens's own field, late types sit at 1 in all three windows.
  - The two-phase reading puts them at 1 inside the wall and at or below the two-phase exterior outside it.
- **E2, stricter and looser hosts.** Delta = 0.0 and -0.3 dex at W 230 Mpc (pooled and by type), with the outer-weight
  share and the mass-scatter factor for each. If the amplitude keeps falling as the cut tightens, the frozen cut has not
  reached the lens's own field.
- **E3, the type split with its joint error.** Early minus late for the host-free set and for W30, by joint jackknife, and
  the same with each type's own mass-scatter factor.
- **E4, late types by redshift half and by mass half** (host-free), to see whether one corner carries the result.

kappa = 1/2 FITTED; not theory closed. Adopts nothing.
