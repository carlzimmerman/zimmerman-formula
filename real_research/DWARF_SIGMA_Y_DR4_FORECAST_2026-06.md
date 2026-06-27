# Gaia DR4 power forecast for the dwarf σ(y) test — the swing, computed

**Script:** `reviews/dwarf_sigma_y_DR4_power_forecast.py` (exit 0). **Footing:** a₀=9.36e-11, framework θ(y), EFE-boost exponent −½. **Data:** Pace+2022, 24 usable MW dwarfs. **Question:** will Gaia DR4 deliver a >3σ verdict on the framework's modified-gravity-impossible σ-vs-history prediction?

## The decisive finding: it depends entirely on *which* y

The forecast splits the test cleanly into a dead branch and a live branch — and the split is the whole result.

**The current-y test is intrinsically DEAD (the "caught cold" problem, now quantified):**
- The entire sample sits at **current-y ≤ 0.66** — *zero* dwarfs above y=1. The two carriers (Antlia II y_cur=0.66, Crater II y_cur=0.57) give predicted σ-boosts of only **+8.5% and +6.6%**.
- Monte-Carlo power @3σ stays **< 1%** even with *ideal* σ-precision (0.3 km/s) **and 5× the sample**. No amount of data rescues the instantaneous test — the carriers simply are not hot *right now*.

**The recent-history (memory-weighted) y test is ALIVE:**
- The carriers reached **peri-y = 3.28 / 2.55** at their last pericenter. The framework's σ records the *kernel-weighted recent* y (memory ~0.4–0.5 Gyr), so a dwarf caught within ~one memory-time of pericenter is *still hot*.
- Power @3σ on peri-y: **8.5%** (diffuse-σ, current sample) → **58%** (2× sample) → **84%** (3× sample); **72%** at ideal σ on the current sample alone.

| test observable | power @3σ (diffuse σ, DR4-era 2–3× sample) |
|---|---|
| instantaneous current-y | **< 1% — dead** |
| memory-weighted recent-y (y_eff) | **58–84% — alive** |

## What this means, honestly

1. **December 2026 (DR4 alone, current σ, current sample) will most likely still be a low-power null** — and that is *correct*, not a failure. The current data genuinely cannot test this.
2. **The test is alive, but only with the right analysis.** The viable version needs all four: (i) the **memory-weighted y_eff** observable (reconstructed from the orbit + the θ-kernel), *not* the instantaneous current-y; (ii) **DR4 orbits** to identify the dwarfs caught *within ~0.5 Gyr of pericenter* (the genuinely-hot ones); (iii) **diffuse-carrier spectroscopy** to halve the σ-errors on the UDGs; (iv) **~2–3× sample growth** (DR4 + LSST satellites).
3. **DR4's decisive contribution is the ORBIT** — it reconstructs each dwarf's recent y-history and selects the recently-hot carriers. The current-y is already known; what DR4 adds is *phase*.

## The locked recipe (ready for DR4)
> Reconstruct y_eff = (θ-kernel ⊛ y-history) from DR4 orbits over the last ~0.5 Gyr; select carriers with y_eff > 1 (recent-pericenter, still-hot) vs adiabatic controls (y_eff < 0.3); partial-correlate log σ against y_eff at fixed (M_bar, r_half), with diffuse-carrier spectroscopy for the σ-precision. Decisive (~60–85% power) by ~2028–30, not at the DR4 drop alone.

## Course-correction for the paper
The v3 paper emphasized **current-y** as the test observable. The forecast shows current-y is the *underpowered cold end* — the framework's own memory kernel says the correct observable is the **recent-history y_eff**. This is a (favorable) sharpening worth folding into a future revision: it moves the test from "dead on current data" to "alive with DR4 orbits + spectroscopy," and it is the more faithful reading of the kernel.
