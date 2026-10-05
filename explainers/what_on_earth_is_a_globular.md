# What on earth is a globular?

*Globular clusters, and why the faint, distant ones matter for the law.*

## A ball of very old stars

A **globular cluster** is a tight, round swarm of roughly 10⁴ to 10⁶ stars, bound together by their own gravity. The Milky Way has about 150 of them, scattered through its halo.

- **Old:** they are among the oldest objects in the Galaxy, about 12–13 billion years.
- **Simple:** all the stars in one cluster formed at about the same time from the same gas.
- **No dark matter:** studies of their stellar motions find no sign of it. They appear to be pure stars.

That last point is what makes them useful. A globular is a clean, dark-matter-free laboratory for gravity.

## Why most globulars test nothing

Most globulars are dense, so the gravity between their stars is far stronger than a₀ (9.4 × 10⁻¹¹ m/s²). Above a₀ your law gives back Newton exactly, so these clusters agree with every theory.

The interesting ones are the **faint, puffy, distant globulars** far out in the halo:

| cluster | distance from the Milky Way's centre (approx.) | stars with measured speeds |
|---|---|---|
| NGC 2419 | about 90 kpc | 183 |
| Palomar 3 | about 90 kpc | 22 |
| Palomar 4 | about 110 kpc | 23 |
| Palomar 14 | about 70 kpc | 16 |

These clusters are so spread out that the gravity inside them drops below a₀. There your law **boosts** gravity, and it predicts that their stars move faster than Newton says.

## The law versus Newton, in one number

Measure how fast the stars move (the velocity dispersion σ). Then ask what mass-to-light ratio, M/L, the cluster's stars would need to explain it: how much mass per unit of starlight.

- Real old stars have M/L ≈ **1.3–2.2**, from stellar-population models.
- **Newton** (no boost) needs M/L ≈ **2.1 ± 0.4**, right in that range.
- **Your law** needs M/L ≈ **0.8 ± 0.15**. That is too little mass per star, because the boost makes the predicted speeds too high.

So **the law over-predicts the outer globulars' speeds by about 1.8×**, at 4.6σ (canonical footing) or 4.9σ (alt). The record for this is `hunt_2026/h93_outer_halo_globulars`. It reproduces Baumgardt+2005, Jordi+2009 and Frank+2012 using the repository's own kernel.

**It is not yet decisive.** A 0.3 dex uncertainty in the stars' M/L spans the whole gap. Palomar 3 even sits comfortably on the law. Also, the cluster with the most data (NGC 2419) has the smallest boost, while the one with the biggest boost (Palomar 14) has only 16 stars. That is why the published literature never settled it.

> **Update (deep audit, 5 Oct 2026):**
> - **The tension is smaller than first quoted.** Scored with the published measurement errors, the over-prediction is about **3.2–3.5σ**, not 4.6σ. Most of it comes from Palomar 4.
> - **Palomar 14's input is unsettled:** 0.71 km/s is used, against the 0.38 km/s in Jordi et al. (2009).
> - **Palomar 3:** unresolved binary stars *could* explain its high speed spread, but only marginally once outlier clipping is included. The source of its measurement isn't named in the data on disk.
> - **What would settle all of it:** individual-star, repeat-epoch velocities.
> - Details: `campaign_fresh_gravity/AUDIT_GLOBULARS_2026-10-05/`.

## Why this matters next to the ultra-faint dwarfs

| system | dark matter? | what the law predicts | what is measured |
|---|---|---|---|
| Ultra-faint dwarf galaxies | the cold component is expected | too slow | about **2× faster** (3.8σ) |
| Outer-halo globulars | none | too fast | about **1.8× slower** |

Both are faint, low-acceleration systems orbiting the Milky Way, and the law misses them **in opposite directions.**

That pattern is informative. If the law itself were simply wrong at low acceleration, both kinds of system would miss the same way. Instead it looks like:

- the **globulars** behave closer to Newton than the law allows;
- the **dwarfs** carry *extra* mass beyond their stars, which fits a cold component that the globulars lack.

## How the framework could match the globulars

1. **Ownership (your own rule, PAPER35).** Only the *outermost* bound system carries the MOND boost. Inside the Milky Way, wide binaries come out exactly Newtonian; that is the pre-registered Gaia DR4 prediction. If a globular counts as *owned* by the Milky Way in the same way, its inside should be plain Newtonian, and that matches the data.
   - **The catch:** the dwarf audit treated satellite galaxies as carrying their own boost. The theory then needs a clear rule for why a dwarf galaxy (which collapsed on its own, with its own cold mass) is a top-level system while a globular (a star cluster that formed inside the host) is not. Making the dwarfs Newtonian too would make their failure worse.
2. **Lower M/L.** Over billions of years, globulars lose many of their low-mass stars through internal encounters. That makes their true M/L lower than standard models assume, which lowers the predicted speeds. The 0.3 dex uncertainty already spans the gap. Measured mass functions per cluster would pin this down.
3. **A stronger external pull.** With the formula used, the Milky Way's field trims the boost by only 7–15% for Palomar 3 and 4, and it dominates only for Palomar 14. The full field-equation version could be stronger. It is the least likely to close the gap alone.

## Bottom line

Globulars are your law's cleanest dark-matter-free test at low acceleration. Today they lean against the boost at about 4.6σ, inside a mass-to-light systematic large enough to hide it. Read alongside the dwarfs, they point to one question that candidate B must answer: **which systems own their boost, and which are owned by their host?**

---

κ = ½ is fitted, not derived. The cold mass is still required; no dark-matter particle is added. The numbers come from the committed lane `hunt_2026/h93_outer_halo_globulars.py`; the dwarf numbers come from `campaign_fresh_gravity/AUDIT_UFD_2026-10-03/`. See also [the Crispy Fried Chicken Status Board](crispy_fried_chicken_status_board.md).
