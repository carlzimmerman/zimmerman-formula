# So what is T and L, exactly?

*Plain-language explainer, 2026-10-27; updated the same night with CL2, CL3 and the held-out tests. κ = ½ is fitted; the theory is not closed. Nothing here says the data favour the
framework over ΛCDM.*

## The picture in one paragraph

The galaxy law, g_N = g²/(g + a₀), with a₀ tied to dark energy, describes isolated galaxies on its own. Groups and
clusters of galaxies need extra gravitating mass. In this framework that mass is **cold dark energy**: a gravitating, slowly
moving (w ≈ 0) component paired with dark energy. It is not a particle and not "dark matter". So the theory has to answer
two questions:

1. **Where** does cold dark energy collect into halos, and where does it stay away?
2. **How concentrated** are the halos it forms?

**T** answers the first question and **L** answers the second.

## T: the switch threshold (*where* cold dark energy switches on)

**What it is.** A mass. A system heavier than about **T ≈ 10^12.3 M☉** (roughly 2 × 10^12 suns of total mass, about the
scale of a small group of galaxies) carries a cold dark energy halo. A lighter, isolated system, such as a single galaxy
up to Milky Way size, follows the law on its own baryons. Satellite galaxies sit inside their host's halo, so they feel it
too.

**Why we think it exists.**
- **KiDS lenses need T to be high.** The weak-lensing signal of isolated galaxies is fit by the law with *no* halo, so T
  must sit above them. Their mass bins reach log M200 ≈ 12.05.
- **Groups need T to be lower than their own mass.** Groups need halos; their log M200 runs 12.0–13.7, with a median of
  12.76.
- **The window.** The data allow a narrow window, log T ≈ 12.2–12.5 (CF2). At T = 12.1 the lensing fails.

**What T is *not*.**
- **It is not fixed by core concentration.** Lane CF1 showed that tying T to the concentration number makes lensing and
  groups contradict each other.
- **It is not any simple native scale tried so far.** Lane DT1 ran a pre-registered tournament: formation epochs,
  self-similar collapse, the galaxy-mass-function knee, and "where the law alone supplies the fair share". Every candidate
  missed the window. T is **located by data, not yet derived**.

**The clue.** The one formula that lands at the window is X43's *core-floor crossover*: the mass where an infall halo's
core surface density reaches the galaxy floor a₀/(2πG). It lands there when the concentration number is about 4. The value
4 is exactly L (below).

## L: the concentration level (*how concentrated* the halos are)

**What it is.** A single number, about **L ≈ 4**. It sets how tightly cold dark energy is packed into the core of a halo,
through the infall factor η = (4/(3B(1))) L^{5/4} ≈ 15, which multiplies the collapse surface density.

**What sets its mass dependence.** The framework's own collisionless zoom simulations (X48). They give a concentration
that **falls with mass**: about 6.4 / 4.5 / 4.0 at 10^12 / 10^13 / 10^14 M☉, once scaled to L = 4 at cluster mass. Groups
come out about 10–15 % more concentrated than clusters. That is exactly what lane CL1 found the data need, and the mass
slope is native, not tuned.

**What is not yet native.** The *level* itself. The zooms put the absolute concentration about 1.5–2× too high, and they
are not converged. Higher-resolution runs (ng 64) are in progress. Until they converge, L = 4 is an external number. It is
the same value the record has carried since X43.

## Why they matter together

| lane | what is set | result (canonical footing) |
|---|---|---|
| CL1 | T and one constant c_f | everything passes except one line, at 0.1–0.2σ |
| CL2 | T = 10^12.3; L = 4 with the native slope | **every graded line passes** at L = 4 with the steeper native slopes; the NFW-fit slope fails (FRAGILE) |
| CL3 | T computed *from* L (the crossover at L) | **every graded line passes** at L = 3.75 and 3.9, so one number does both jobs |

The cluster halo budget behind these lanes uses no free choice. It is the fair share of cold dark energy for the gas
X-COP actually measures, out to the turnaround radius (GS1).

## Then we tested it on data it had never seen, and it failed

| held-out test | result |
|---|---|
| Local Group dwarfs one by one (HO3) | fails: about 0.25 dex of extra scatter; Leo T and Phoenix sit above the law |
| SLUGGS central ellipticals (HO2) | fails: still under-predicted, 1 of 4 clears |
| the Milky Way (HO2) | fails: it needs a halo, which would need T below 10^11.9, while lensing needs T above 10^12.15 |
| X-COP clusters one by one (HO1) | fails: the mean is right, the shape wrong (cores too light, outskirts too heavy) |
| hot-gas groups (HO1) | fails: the predicted sign is opposite to the data |

So T and L, as a sharp mass switch plus one concentration level, **describe** the lines they were built from. They are
not yet the mechanism. The failures point the same way: a switch keyed on environment or gas state rather than mass, and
a different halo shape.

## The honest scorecard

- **Located by data, not derived:** L ≈ 3.75–3.9, with T following from it through the crossover (CL3). This holds only
  for the steeper native slope.
- **Native:** the mass slope of concentration (from zooms), the cluster gas budget (measured), the core floor a₀/(2πG),
  and the background (BAO + BBN, no CMB).
- **Still open:**
  - why L ≈ 4 (converged zooms);
  - why the switch is the core-floor crossover (the physics of condensation);
  - the alternative a₀ footing, which fails SPARC and the Milky Way ultra-faint dwarfs regardless of T and L.
- **Margins are thin.** Groups pass at Z +1.99 against a limit of 2.00.

## Where to look

Lane folders under `rebuild_2026_10_22/`:
- `CF1_cf_window_map`
- `CF2_decoupled_threshold_map`
- `GS1_measured_gas_outskirts`
- `CL1_combined_threshold_budget`
- `CL2_native_cf_slope`
- `CL3_one_number`
- `DT1_threshold_tournament`
- `X43_collapse_core_floor`
- `X48_native_cf_zoom`

The question paper is PAPER63, DOI 10.5281/zenodo.23708507.
