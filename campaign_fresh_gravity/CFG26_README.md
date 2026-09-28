# CFG26 — the infall from the peak's own surroundings (aborted before its main run)

Script: `CFG26_constrained_infall.py`.
- **Record:** the first (MUTATE) run's log, `CFG26_constrained_infall_MUTATE_aborted.out`.
- **No main run was made. No result is claimed.**

## What it tried

CFG25 found that spherical infall around a *power-law* seed misses KiDS's outer signal for standard halos too. This lane swapped the seed for the constrained mean linear profile around a region that turns around at z = 0.25 (`CFG7_common.ics_constrained`): the linear-theory expectation of a peak's own surroundings. It then scored a standard halo and the framework's FG016-type profile on KiDS.

## Why it was stopped

The first run passed its controls:
- the fitter reproduces BASE and CFG21;
- the zero-velocity radius matches the top-hat one to 0.1%;
- the guard is 0.

But the seed is unphysical for this purpose.
- **The mean profile is flat inside the region.** The conditional mean of δ(<q) given δ(<R) is nearly constant for q < R, so the seed's inner slope is only 0.054–0.068. The region collapses like a top hat.
- **So there is no halo at z = 0.25.** M200m is 1–4% of M_ta, splashback sits at 0.04–0.06 r_ta, and each run takes about 12 s against 70–600 s for FG016's seeds.
- **The framework profile inherits it.** The law inside that tiny caustic gives χ² about 350 on KiDS.
- **The underdense variant fails.** t_env = −1 makes the mean overdensity negative at large q, and the seed construction returns NaN.

The routine's fix is a steeper inner slope (`eps_in`). That reintroduces a scanned choice (FG016's accretion-rate grid), so the lane could no longer give a decisive yes/no. It was stopped before any main run.

**Lesson for later lanes:** `ics_constrained` without `eps_in` does not produce a galaxy halo.

## Standing

Nothing changes: CFG25's reading stands. What the KiDS outer profile needs is a realistic model of the lens's surroundings, N-body-grade, for both models. A spherical engine with a different seed cannot supply it without a new choice.
