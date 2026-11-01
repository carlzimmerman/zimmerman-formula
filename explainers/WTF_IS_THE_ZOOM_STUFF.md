# Wtf is this zoom stuff about anyways?

**Short version.** A zoom is a computer experiment that lets cold dark energy collapse under its own gravity, so we can see what shape of halo it makes. We run them so the halo shape comes out of the framework itself, not from a number borrowed elsewhere.

κ = ½ FITTED. Not theory closed. Nothing here says the data favour the framework.

## Why we need them

The theory has two parts:
1. The law, g_N = g²/(g + a₀), which acts on visible matter.
2. Halos of cold dark energy: a gravitating field component, never a particle.

The law says nothing about what a halo looks like. To predict a rotation curve or a lensing signal, you need the halo's mass and how that mass is spread out, above all how dense its centre is.

For a long time that came from c_f = 4, a concentration value taken from outside the framework. It worked, but it was an input, and the standing rule is raw data or framework-native only. So the question became: **if this fluid collapses on the framework's own background, what halo does it actually make?** You can't work that out on paper, because collapse is too messy. You have to run it.

## What one run does

1. **Set up a patch of the early universe.** Take a sphere of particles, slightly lumpy, using the record's own power spectrum and background. Its centre is forced to be a density peak that will grow into a halo of the mass we asked for.
2. **Let gravity act.** Every particle pulls on every other, in small time steps, about 1,000 to 1,900 of them. The particles are tracers of the fluid, not real objects.
3. **Measure the result.** Find the centre and read off the density profile: how much mass sits inside each radius.

Then repeat with a different random lump pattern (a "seed"), usually nine times per mass, because individual halos differ a lot. Masses run from 10⁸ M☉ (dwarf) to 10¹⁵ M☉ (big cluster).

**The name is loose.** In most astrophysics a "zoom" means re-running one region at high resolution inside a big simulated universe. Ours are isolated spheres with nothing outside them. That's a real limit: see below.

## The knobs you keep seeing

| Term | Meaning |
|---|---|
| **ng** | Grid size per side used to lay down particles. Higher means finer. ng 38 / 48 / 64 / 80 is 12,149 / 24,405 / 57,777 / 113,009 particles. ng 80 is the top so far. |
| **seed** | Which random lump pattern. Each grid draws its own field, so "seed 1 at ng 48" and "seed 1 at ng 64" are **different halos**. |
| **ε** | Softening: gravity is smoothed below this distance so particles don't scatter wildly. Nothing inside about 3ε can be trusted. |
| **z_f** | The halo's formation epoch. Early runs stop here. |
| **z = 0** | Today. ZN1 onward carry the runs on to here, which is what you compare with today's clusters. |
| **c_f** | Formation concentration: how centrally packed the halo is, read from where the density slope hits −2. |
| **η** | The strength of the core: how dense the centre is, relative to the density of collapse at that mass. |

## What's in them and what isn't

**In:** gravity between particles, plus the background's Λ term.

**Not in:**
- the a₀ law (the runs use Newtonian gravity between particles)
- gas, stars, feedback, or a central galaxy's pull
- anything outside the sphere: neighbours, later infall from beyond it

So a zoom tells you what the cold sector does **alone**. Gas is added afterwards in the grading step, and it doesn't push back on the halo. If baryons reshape halos in reality, these runs can't show it.

## What they've told us

| Lane | Question | Answer |
|---|---|---|
| **X48** (to ng 80) | Does collapse give c_f ≈ 4? | **No.** c_f is about 7–10, above the window [3.3, 4.6]. At 10¹², ng 80 gives 7.43 against 7.74 at ng 64, so it's converged there. |
| **X48 A5** | Does the old c_f rule, with its floor, pass SPARC on that value? | **No**: SPARC SETTLED FAIL, Υ 0.48. The floor rule was removed on 10-31 anyway. |
| **X81** | Are the "cores" in the zooms real? | **No.** They are NFW cusps seen through the resolution cut. Early η values depended on where the fit started, which is a numerical choice. |
| **X80** | Does the a₀ floor emerge at dwarf masses? | **No**: FLOOR BY HAND. But native version N, with no floor, passes SPARC's line. |
| **NR1** | Does that still pass with 10¹² at ng 80? | **Yes, conditionally**: Υ 0.72 / 0.75. Only if 10¹⁰ and 10¹¹ don't drop too. If they drop by the same factor, it fails at Υ 0.88 / 0.89. |
| **ZN3, ZN4** | Do native cluster shapes at z = 0 fit, with no fitted parameter? | **Only on X-COP's gas scale**: 15 of 15 keys and X-COP, at ng 80. On the measured gas scale (+0.005 ± 0.017, not +0.111): 12 of 15, G-OUT-M3 +4.41. |
| **OP1** | Do low-mass shapes fix the dwarfs? | **No.** 10⁸ and 10⁹ are self-similar and still fail all five Local Group classes. The miss is in mass, not shape. |

The biggest lesson: **the shape no longer looks like the main problem.** Resolution didn't rescue clusters or dwarfs. In both, what's missing is how much mass the halo has, so the mass rule is the pressure point.

## Traps, each of which has already caught us

- **Scatter is huge.** At ng 48, c_f ran from 2.3 to 13.4 at one mass. One seed means nothing, so compare medians with their bands.
- **"Same seed, higher ng" isn't a resolution test,** since the field is redrawn. X81's T1 made this mistake and could never have decided anything.
- **A trend can vanish.** "c falls with mass" appeared at ng 48 and didn't hold at ng 64.
- **The centre can be an artefact.** Anything inside about 3ε reflects the setup, not physics.
- **A pass can rest on something else.** ZN3's clean pass rested on a gas offset that was later measured to be about zero.

## Still open

- **NR2** is running: nine ng 80 seeds at each of 10¹⁰ and 10¹¹. It decides whether NR1's pass survives.
- Nothing past ng 80 has been tested.
- There are still no neighbours, no gas response and no feedback in any run.
- A thin closing shell near turnaround, needed to close the mass budget in the grader, isn't physical (ZN3's limits).

## Where to look

- Engine: `rebuild_2026_10_22/X48_native_cf_zoom/x48_zoom.py`
- Results: the `README.md` in `X48_native_cf_zoom`, `X80_low_mass_floor_emergence`, `X81_core_convergence`, `ZN1_zooms_to_z0`, `ZN3_native_shape_at_1e15`, `ZN4_cluster_resolution`, `NR1_native_n_ng80`, `OP1_one_profile_dwarfs` (all under `rebuild_2026_10_22/`), plus `X48_native_cf_zoom/A5_RESULT.md`
