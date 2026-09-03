# The coherence fork: f08–f10 (2026-09-03)

Three scripts asking the question the whole programme had assumed away: **not "what extra mass is there?" but
"which KIND of modification is on the table?"** All three are committed and runnable; two end in negative results
and one opens a fork that stays open.

## What was asked

Every one of the ~130 hunt items assumed the modification is a function of the local field, `nu(g_bar/a_0)` — the
**modified-gravity** arm, operative in this repository since 2026-08-08. The liability table then says that
assumption fails outside rotating discs. f08–f10 ask whether the arm itself was the wrong choice.

## f08 — let the data pick the kernel's argument. **Result stands; second half WITHDRAWN.**

Fixes the disc relation empirically and asks which local variable, used as the kernel's argument, also lands the
15 liability rows on it. Candidates: acceleration, radius in MOND units, dispersion, density, dynamical time, mixed.

- **STANDS:** no single-variable argument collapses both regimes. Each either keeps the disc relation tight
  (0.176 dex) and leaves the liability rows off it (median −0.106, rms 0.377 dex), or accommodates the rows only by
  loosening the discs — and the discs' tightness is the framework's entire empirical basis.
- **WITHDRAWN:** the "second variable absorbs the residual" finding (slope −0.343). Its mutation control FAILED —
  a single shuffle of 15 rows returned −0.232. Do not cite it.

## f09 — the pattern nobody read. **1.7 sigma. A hint, not a result.**

Every system the framework fits is **rotation-supported**; every system it misses is **pressure-supported**, across
eleven decades of mass. That matters because Milgrom proved (1994; 2011, arXiv:1111.1611) modified **inertia** and
modified **gravity** agree exactly for circular orbits in the deep-MOND limit and differ for every other orbit.

Matched pair, the only version that is not confounded: rotating dwarf irregulars vs the eight classical dwarf
spheroidals at the **same internal acceleration** and the **same baryonic mass**, both sides through the framework's
own kernel, both footings, the dwarf spheroidals given the more favourable of the two prescriptions.

| population | median residual | scatter | N |
|---|---|---|---|
| rotating, matched acceleration | +0.013 dex | 0.175 | 105 |
| pressure-supported (classical dwarf spheroidals) | +0.228 dex | 0.349 | 8 |

Separation **+0.215 dex, 1.73 sigma** (canonical; +0.205 alt). **Quote it at that strength, never higher.**

Three failures recorded in the file rather than hidden:
- **A1 FAILS its 3-sigma bar.** Only eight classical dwarf spheroidals exist. No analysis choice pushes this past 2 sigma.
- **A3 FAILS.** Matching on mass as well as acceleration *degrades the control*: only 5 rotating galaxies overlap and
  they sit at −0.205 dex, off the kernel themselves. The separation appears to grow only because the control gets worse.
- **A6.** The sign of the residual tracks which branch of the external-field prescription was used — isolated branch all
  positive, external-field branch all negative. Part of the scatter is the prescription, not the data.

Also withdrawn: a pooled coherence correlation across all systems. It was out-ranked by velocity scale (r=+0.52 vs
−0.45) **and** circular, because the disc dispersion was derived from the same kinetic energy that defines the deficit.

## f10 — the cheapest route to deciding the fork. **SHUT.**

In modified gravity an isolated binary feels a **central** force depending on separation alone, so it cannot know the
orbit's eccentricity; a trajectory-dependent modification must. That looked like a one-sided, parameter-free falsifier
on Gaia DR4, using the projected angle between separation and relative velocity — a quantity Gaia measures directly.

**It does not work.** 12000 vectorised two-body MOND orbit integrations per case:

| eccentricity law | gravity | slope of velocity ratio vs projection angle |
|---|---|---|
| thermal | modified | −0.476 ± 0.067 |
| thermal | Newtonian | −0.916 ± 0.110 |
| uniform | modified | +0.211 ± 0.016 |
| uniform | Newtonian | +0.119 ± 0.014 |

The force is blind to eccentricity; **the observable is not.** Projection and orbital-phase sampling reintroduce the
eccentricity distribution at full strength, and the predicted slope **reverses sign** between a thermal and a uniform
population. Subtracting the Newtonian slope at matched eccentricities half-rescues it — the residual slope's sign is
robust, its magnitude differs by a factor 4.8 — and an exclusion needs the magnitude.

**Do not preregister this.** It would have looked clean and produced a confident December number that was measuring
the unknown eccentricity distribution of wide binaries rather than the form of gravity. The frozen Amendment 10 band
is untouched; this file adds nothing to it.

## Standing after f08–f10

- The modified-gravity arm is **not established as the right arm**. The rotation/pressure split is a real structural
  pattern with a real theorem behind it, and the repository has tested only one arm since 2026-08-08.
- The fork is **OPEN and currently undecidable** with anything cheap. The cheapest route is shut (f10) and the
  matched-pair evidence is sample-size-limited at 1.7 sigma (f09).
- Nothing here rescues clusters. The f04–f07 no-go chain still forbids supplying the cluster residual with any dark
  component, hot, cold or mixed.
- Dark matter explains the rotation/pressure pattern equally well and this work does not separate the two.
