# CFG32 — the X-ray ellipticals under candidate B, refereed

Script: `CFG32_xray_ellipticals_under_b.py`, under a second.
- Outputs: `.out` and `_results.json`.
- MUTATE control: `_MUTATE.out` and `_MUTATE_results.json`. Every g_obs is halved, and H1 fails (rc = 1).
- The main run exits 1: the headline H1 (that the failure survives at > 2σ) failed. That is reported as run.

κ = ½ is fitted. Both footings are used.

## Question

The failures summary carried the X-ray ellipticals as liability B4, never scored under candidate B and never given a significance. Seven X-ray-bright early-type galaxies (Humphrey+2006, ApJ 646, 899: NGC 720, 1407, 4125, 4261, 4472, 4649, 6482) need a median 1.69× (canonical) / 1.57× (alt) more boost than the law gives over 5–70 kpc. That was computed with stars only, at a Kroupa population M/L (`hunt_2026/h10_h18_xray_hse.py`).

**What candidate B predicts here is the law itself.**
- T5 makes galaxies phantom-dominated. The "max(phantom, cosmic share)" rule is for baryon-complete clusters.
- Ownership gives no external field: isolated and top-level galaxies obey the law, and accreted ones (NGC 4472 and 4649 are Virgo members) obey the isolated law of their infall baryons.

So B changes little. What this lane adds is the referee h10 never had:
- h10 used the paper's best-fit NFW + stars model, not the deprojected data.
- It omitted the hot gas.
- It fixed the IMF at Kroupa, which is uncertain for massive ellipticals.

## Method (declared before the first run)

h10's data and mass model are exec'd read-only.
- **Offset:** a point's offset is log[(g_obs/g_bar)/ν]. A galaxy's offset is the median over its five radii, since those are not independent. The sample offset is the mean of the seven, with the galaxy-to-galaxy error std/√7.
- **Systematic floor,** computed by re-running the pipeline:
  - the IMF: Kroupa → Salpeter, Humphrey's own population values;
  - the radial range: all radii → r ≤ 40 kpc, where the fitted model is least extrapolated.
- **Hot gas:** it cannot be added, because the repository has no gas profiles. Instead, the gas each galaxy would need to null its offset is reported.

## Results

**C1 (control):** h10's committed numbers are reproduced (1.689 / 0.2493 canonical; 1.571 / 0.2421 alt).

| | canonical | alt | verdict |
|---|---|---|---|
| H1 (headline): the failure survives at > 2σ | **+0.280 ± 0.165 dex → 1.70σ** (a factor 1.91) | **+0.254 ± 0.161 → 1.58σ** (1.79) | **FAIL**: not established at 2σ |
| H2: the shortfall grows toward low acceleration | slope negative in **7 of 7** galaxies | | PASS: the missing mass is extended |
| H3: the max rule applied at each radius | over-predicts at 10 kpc by 2.4–5.5× in **6 of 7**; under-predicts at 70 kpc in 7 of 7 | | PASS: not an escape |

The error budget: galaxy-to-galaxy 0.084 dex; IMF 0.126; radial range 0.065; floor 0.142.

**Per-galaxy offsets (canonical, dex).**

| galaxy | Kroupa | Salpeter | hot gas needed inside 70 kpc to null it (M_gas/M_*) |
|---|---|---|---|
| NGC 720 | +0.57 | +0.46 | 12.0 |
| NGC 1407 | +0.27 | +0.15 | 4.7 |
| NGC 4125 | +0.04 | −0.09 | 1.2 |
| NGC 4261 | +0.03 | −0.08 | 2.5 |
| NGC 4472 | +0.34 | +0.20 | 9.3 |
| NGC 4649 | +0.55 | +0.42 | 15.5 |
| NGC 6482 | +0.15 | +0.02 | 1.6 |

**Reported (sample means).**

| variant | canonical | alt |
|---|---|---|
| Kroupa | +0.280 | +0.254 |
| Salpeter | +0.154 (1.45σ) | +0.130 (1.26σ) |
| Humphrey's fitted M/L | +0.347 | +0.319 |
| r ≤ 40 kpc | +0.215 | +0.193 |
| P2 kernel | +0.331 | +0.307 |

## Standing

**B4 is a large shortfall but not an established failure: a factor ~1.8–1.9 in acceleration at 1.6–1.7σ.** The significance is limited by seven galaxies and the IMF, not by the size of the offset.

Two findings sharpen it:
- **The missing mass is extended.** The shortfall grows outward in all seven galaxies, which is what a missing mass component looks like, not a wrong M/L.
- **It is carried by a few galaxies.** Three galaxies carry it: NGC 720, NGC 4649 and NGC 4472. Hot gas would have to be 9–15× their stellar mass inside 70 kpc to close it, which is not plausible for X-ray atmospheres. Four sit near zero.

B's cluster rule (the cosmic share applied at each radius) is not an escape: it over-predicts the inner regions several-fold.

**What decides it:** the deprojected gas density and temperature profiles, which carry the hot-gas mass and avoid the fitted-model extrapolation. Humphrey+2006 (and later deeper work on some of these galaxies) publish them. They are not yet in the repository, and fetching them needs the owner's go.

Nothing here says the theory is closed.
