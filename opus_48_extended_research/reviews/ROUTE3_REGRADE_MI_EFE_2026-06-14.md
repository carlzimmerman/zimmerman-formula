# REGRADE — Route 3 [corrected_discrimination]: the framework's OWN dS-Unruh MI-EFE wide-binary gamma

*Opus 4.8 (1M) adversarial regrade, 2026-06-14. Scripts (reproducible, numpy/scipy only):
`/tmp/mi_regrade.py`, `/tmp/mi_eom_solve.py`, `/tmp/mi_scalar_vmi.py`, `/tmp/mi_vs_mg.py`,
`/tmp/discriminator_decomp.py`, `/tmp/final_verify.py`. Anchored on banked
`real_research/reviews/toe_law/mi_f4_widebinary_efe.py`, `MI_COUPLING_FAMILY.md`,
`efe_clinch_framework.py`, and the sibling routes `PURE_MI_WIDEBINARY_GAMMA_ROUTE1` (1.137) and
`WB_EFE_DERIVATION` (1.324 AQUAL). a0/Z never asserted derived.*

## Bottom line

Route 3 got the **right idea** (use the dS-Unruh MI, expose that 1.32 is AQUAL modified gravity) but
the **wrong number** and an **oversold discriminator**. Three findings:

1. **No simple-mu/AQUAL was smuggled INTO the framework value** — the framework column genuinely uses
   the dS-Unruh mu. (a) passes.
2. **The framework-MI gamma is WRONG: route3 says 1.168 (central ~1.18); the correct value is 1.137.**
   The error is a real MI mistake — route3 evaluated mu at the Newtonian field `e=2.298` instead of at
   the true total worldline acceleration `x_op = nu(e)*e = 2.753`. In modified inertia mu is a function
   of the actual acceleration |a|, not of g_ext/a0. (c) FAILS for route3; route1's 1.137 is correct.
3. **The "hidden discriminator" is largely wishful.** The claimed 0.25 gap is a conflation of three
   effects; the clean, shape-and-a0-controlled MI-vs-MG gap is only 0.03–0.08, inside the systematics.
   And the literature says MI-EFE for wide binaries is **time-nonlocal and possibly STRONGER** than
   AQUAL — contradicting route3's "MI one-sided weaker." (d) is overstated.

## (a) Did route3 smuggle simple-mu/AQUAL into the framework value? NO.

The framework's isolated law `g_obs = sqrt(g_N^2 + g_N a0) = g_N nu(y)`, `nu(y)=sqrt(1+1/y)`, inverts
to the MI inertia `mu(x) = (sqrt(1+4x^2)-1)/(2x)` — verified an exact inverse companion (max err 1.4e-14).
This is NOT simple-mu `x/(1+x)` and NOT standard/F4 `x/sqrt(1+x^2)`. Route3 used this dS-Unruh mu for the
framework column and put simple-mu only in the labeled normal-MOND comparison column. Clean on (a).
(One nuance: the dS-Unruh mu is algebraically Milgrom-99's F1 with x->2x, consistent with `MI_COUPLING_FAMILY.md`.)

## (b)/(c) Is the framework-MI gamma correct? NO — route3 used the wrong operating point.

I recomputed three independent ways (analytic inertia tensor; **direct 2D vector-EOM `fsolve` of
mu(|a|/a0)a_vec=F_vec**; scalar vector-MI of the banked mi_f4 prescription). All three agree:

| estimator | CORRECT (mu at x_op=2.753) | route3 (mu at e=2.298) |
|---|---|---|
| transverse 1/mu | **1.198** | 1.241 (WRONG) |
| longitudinal 1/[mu(1+L)] | **1.016** | 1.023 (WRONG) |
| 3D isotropic (2T+1L)/3 | **1.137** | 1.168 (WRONG) |

The clean identity `1/mu(x_op) = nu(e) = 1.198` is the transverse boost — machine-verified. Route3's
1.241/1.023/1.168 are reproduced EXACTLY by mis-evaluating mu at `e` (the Newtonian field) instead of
at the boosted total acceleration `x_op`. In MI the star in the MW field actually accelerates at
`a = nu(e)*g_ext`, so `x_op = nu(e)*e = 2.753` is the operating point; `e` is the force, not the accel.
**Route3 is internally inconsistent**: it lists "scalar vector-MI = 1.198" (correct, = nu(e)) AND
"transverse = 1.241" (wrong) — these must be the same number.

**Correct framework dS-Unruh MI cap: gamma_cap = 1.137 (3D isotropic), 1.11 (2D-projected) – 1.198
(pure-transverse). Central 1.137, NOT 1.168, NOT ~1.18.** This matches the sibling route1 doc. The
direct gamma(s) curve (M_tot=1.5 Msun) rises from ~1.05 (s=3 kAU) to the cap by s~6–7 kAU, matching
Chae's 2–5 kAU onset.

## (d) Does MI-vs-MG really open a hidden discriminator? Mostly NO — it is oversold.

The 1.32 AQUAL headline is confirmed: simple-mu, mu at the field e=2.298, orbit-avg = **1.324**. That
IS modified-gravity machinery, so route3's headline claim ("1.32 = AQUAL MG, framework MI is different")
is directionally right.

BUT route3's claimed **0.25 hidden discriminator** (framework-MI 1.168 vs std-MOND-AQUAL 1.421)
decomposes into THREE independent pieces — only ONE of which is the MI-vs-MG realization difference:

| piece (each held-others-fixed) | size |
|---|---|
| MI-vs-MG (simple-mu shape, a0_F) | **+0.084** |
| interpolation shape (dS-Unruh vs simple-mu) | **+0.103** ← dominant |
| a0 (framework 9.36 vs standard 1.2e-10) | **+0.097** |
| total (= route3's 0.25/0.28 gap) | +0.284 |

The **clean, shape-AND-a0-controlled** MI-vs-MG gap (the only honest discriminator) is **0.031** for the
dS-Unruh shape (MI 1.137 vs same-shape AQUAL 1.168) or **0.084** for simple-mu. That is **comparable to
or below** the interpolation/a0 systematics — it does NOT cleanly clear the floor. Route3's both_ways
section partly admits this ("collapses to 0.056 under same shape") but it (i) used the inflated 1.168,
(ii) blended a0 + shape + realization into one "discriminator," and (iii) understated that the dominant
0.10 piece is interpolation, exactly the banked-rule "interp dominates."

**Literature contradiction (this is the sharpest catch):** route3 asserts "MI predicts a one-sided
WEAKER galactic-field EFE than AQUAL, never stronger." Milgrom 2310.14334 and Scholarpedia say the
opposite for this regime: MI predicts a *much weaker* effect in the **inner Solar System** but
**possibly a STRONGER** external-field effect on **wide binaries**, and the MI-EFE is **time-nonlocal**
— "the kinetic acceleration depends not only on position but on characteristics of the full orbit
(frequency ratios, eccentricity)," and "the quasi-static approximation may not be valid for bound
orbits." Both route1's 1.137 and route3's 1.168 are **quasi-static-tensor approximations of a quantity
the framework cannot actually compute without a full trajectory kernel** — the banked mi_f4 script flags
exactly this ("true MI evaluates the kernel on the full helical trajectory"). So the "MI is weaker"
sign is NOT robust, and the MI-vs-MG number itself carries an uncontrolled time-nonlocality systematic
that likely exceeds the 0.03–0.08 quasi-static gap. The discriminator is real in principle but
not delivered, and its sign is literature-contested.

## Data confrontation (corrected MI number)

| model | gamma | vs Chae 1.60 (+.17/-.14) | vs Saad-Ting 1.12 |
|---|---|---|---|
| framework MI **corrected 1.137** | 1.137 | **-3.3 sigma** | +0.1 sigma (consistent) |
| route3 MI 1.168 | 1.168 | -3.1 sigma | +0.4 sigma |
| MI transverse 1.198 | 1.198 | -2.9 sigma | +0.6 sigma |
| simple-mu AQUAL 1.324 (NOT framework) | 1.324 | -2.0 sigma | +1.2 sigma |

The corrected (lower) cap makes the Chae tension slightly WORSE (-3.3 vs route3's -3.1 sigma) and the
Saad-Ting agreement essentially unchanged (consistent). The field's own 1.60-vs-1.12 split
(systematics-dominated, Δγ~0.44) still swamps the framework-vs-Newton signal. Direction of route3's data
story holds; magnitudes shift down ~0.03 because the MI cap was inflated.

## (e) Both ways — corrected

- **Framework-vs-Newton (the winnable axis):** gap-to-Newton = **0.137**, not route3's 0.17 (and not the
  banked 0.32 = simple-mu). The Newton clinch SURVIVES at well-controlled systematics but is THINNER:
  DR4 SNR ~3.6 sigma (well-ctrl) / ~2.2 sigma (realistic), DOWN from the banked 5–8 sigma and slightly
  below route3's 3–5 sigma. Fragile to the Saad-Ting deprojection.
- **No manufactured win from "MI is special":** the hidden discriminator is NOT clean — 0.10 of the 0.25
  is interpolation, 0.10 is a0, only 0.03–0.08 is genuine MI-vs-MG, and the MI-vs-MG sign is
  literature-contested (Milgrom: MI may be STRONGER for WBs) and quasi-static-approximation-limited.
  Route3 oversold this.
- **No lazy "MI=MG so 1.32 stands":** MI and MG genuinely differ (different mu-argument: field e vs
  boosted x_op), and 1.32 is genuinely the AQUAL/MG value — the framework's own MI is genuinely lower
  (1.137). The published 1.20–1.32 band IS normal-MOND-contaminated, as route3 correctly diagnosed.
- **Interp/estimator spread at fixed a0 (1.11–1.20, plus shape pushing to 1.04 std-MI or 1.32 simple-MI)
  still exceeds the a0-only MOND gap (~0.04–0.06)** — interpolation dominates, per the banked rule.

## NET regrade

Route 3's *framing* is sound and corrects a real error (1.32 = AQUAL MG, not the framework's MI), but its
*number is wrong* (1.137, not 1.168 — wrong MI operating point) and its *discriminator is oversold* (the
clean MI-vs-MG gap is 0.03–0.08, not 0.25; and Milgrom says MI may be STRONGER, not one-sided weaker, for
wide binaries — both numbers are quasi-static approximations of a time-nonlocal quantity). Verdict
skeleton (clean-ish vs Newton, MOND-/realization-degenerate, ~3 sigma below the pro-MOND camp, consistent
with the Newton camp) SURVIVES but the Newton clinch is thinner (0.137 gap, ~2–4 sigma DR4) and the
"hidden discriminator" should be downgraded from "0.25, opens a real test" to "0.03–0.08 quasi-static,
sign-contested, not delivered." a0/Z never asserted derived.

Sources: Milgrom, "MOND as manifestation of modified inertia" (arXiv 2310.14334); Scholarpedia, "The MOND
paradigm of modified dynamics."
