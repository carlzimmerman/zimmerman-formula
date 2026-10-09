# The Crispy Fried Chicken Status Board

*Where the theory stands, as of 9 October 2026, in one picture.*

The theory makes one claim: the acceleration scale where galaxies stop obeying Newton, a₀, is set by the density of dark energy.

```
a₀ = κ · c · √(G ρ_Λ),   κ = ½   →   a₀ = 9.36 × 10⁻¹¹ m/s²
```

The ½ is **fitted** to galaxy rotation curves, not derived. A cold component with the amount of mass usually attributed to dark matter (Ω_c h² ≈ 0.12) is still required; no dark-matter particle is added.

![Status board: every test of the theory as a coloured tile](img/status_board.png)

## How to read it

Each tile is one test. The colour restates a verdict recorded in [`campaign_fresh_gravity/STANDING_2026-09-29.md`](../campaign_fresh_gravity/STANDING_2026-09-29.md), and the lane IDs on each tile point to the scripts that produced it. Every verdict comes from a committed script with pass/fail rules frozen *before* the data were read, plus a control that is deliberately broken and must fail.

| colour | meaning |
|---|---|
| 🟩 **pass** | the theory meets the test within the stated errors |
| 🟨 **conditional** | passes, but only under a stated assumption that is not yet proved |
| 🟦 **not decidable yet** | today's data cannot tell the theory from its rival |
| 🟥 **fails** | the theory misses the test, and audits from the raw data confirm the miss |
| ⬜ **open** | not yet answered, or waiting on data |

## Column 1 · The relativistic theory (the "chassis")

This is the full field theory underneath the law: general relativity plus a preferred time direction (a "khronon"). It has to behave like Einstein's gravity wherever Einstein's gravity has been tested.

- **Passes:**
  - gravitational waves travel at exactly light speed;
  - realistic matter keeps the equations well behaved;
  - binary pulsars, with a 490,000× margin;
  - solar-system tests;
  - matter is exactly conserved (G9).
- **Conditional:**
  - well-posedness, in two forms (high-frequency and full nonlinear);
  - strong coupling;
  - structural order (G0): no runaway "ghost" mode, but solvability in the strongly nonlinear regime is unproved;
  - **black holes.** EHT shadows and LIGO ringdowns are matched to better than one part in 10⁹. A *moving* black hole keeps a hidden, Planck-scale defect on its innermost horizon. A 2019 paper's standard would count that as fatal; the owner's reading of it is still pending.

- **Fails, for the ungated chassis only: zero-field nonlinear dependence (G5/G10).** This 1-D test runs the bare relativistic chassis with the law switched on everywhere, including the smooth, expanding cosmic background, where the field is near zero. In that setting the sensitivity to tiny perturbations does not level off at the larger perturbation on the finest grid (N = 2047, CFG358, a knife-edge call). **It does not test candidate B, your live model:** there the law is switched off outside bound halos, so it never acts on that background. Candidate B's full action does not exist yet, so for B this is untested, not passed. This sits alongside the ungated chassis's growth failure in Column 3.

## Column 2 · Galaxies and clusters

- **Passes:**
  - rotation curves (SPARC, 0.10 dex scatter);
  - a₀ measured locally with MeerKAT, 0.9–1.3 × 10⁻¹⁰ (PAPER40);
  - clusters, including the Bullet Cluster, which needs the cold mass;
  - Andromeda's and the Local Volume's dwarfs;
  - the Milky Way's vertical force: round cold energy beats MOND's flattened phantom disc in 32 of 32 cells (CFG516). This separates the theory from MOND, and Gaia DR4 tests it directly.
- **Conditional: the Milky Way's ultra-faint dwarfs.** They move about 2× faster than the law predicts (3.8σ at the generous end), and every data-side explanation fails. Post-reionisation cold accretion onto these fossils (CFG344) removes the offset, but only in a narrow window and with ΛCDM-calibrated assembly assumed.
- **Conditional: Local Group timing.** The earlier 13.5σ miss came mostly from treating the orbit as radial with measurement errors only. With Andromeda's sideways motion it drops to about 2–3σ, and a derived shared cold-energy supply between the two galaxies removes most of the rest. About 4σ remains on the old straight-line statistic (CFG522).
- **Footing-dependent: lensing around isolated galaxies (KiDS).** In a validated neighbourhood model the zero-knob edge falls short in the inner 50–190 kpc (CFG529). On the alt footing an allowed 0.1 dex heavier stellar mass closes it; on canonical none does (CFG531). The deficit sits in the most massive, early-type lenses.
- **Tension: the four central ellipticals (SLUGGS).** With each galaxy's measured globular-cluster profile and orbits, the gap is about +0.07 dex on average, 2.8–3.5σ statistical only (CFG528b). Heavier stars, hot gas and the cold-energy edge all fail to close it. It is not a foreground effect.
- **Not decidable yet (DR4): the Milky Way's outer slope.** At census baryons the law fits the speeds, but Gaia's 15–27 kpc decline is 3–5σ steeper than the law (CFG532b). A standard dark-matter halo fails the same test (3.4σ). The result rests on a disputed distance scale, and Cepheids stay flat. In external galaxies seen through their gas, the law predicts outer slopes with no bias (153 SPARC galaxies, CFG533), so the tension is specific to the Milky Way: how we measure it from inside, or its current disturbance. DR4 fixes the distance scale.

## Column 3 · Cosmology, and does a₀ change over cosmic time?

The theory's sharpest prediction is that **a₀ stays constant**. Its main rival has a₀ growing with the expansion rate, H(z).

![a₀ against redshift: flat line versus the a₀ ∝ H(z) rival](img/a0z_chart.png)

- **Not decidable yet: a₀ over time.** The two lines separate at redshift 2–5. At those redshifts, though, the uncertainty in how much gas each galaxy holds is larger than the gap between the lines (the "calibration wall", PAPER38). No public data set can settle this today.
- **Open: Gaia DR4 wide binaries** (data release 2 December 2026). This test is pre-registered and frozen: PAPER35 predicts exactly Newtonian behaviour.
- **Conditional: structure growth, candidate B.** Simulated in a universe-in-a-box (CFG361 onward), switching the law on everywhere makes structure 15–17% too clumpy. The fix has no hand-set numbers: the extra gravity is cold energy that each halo can spend only once, drawn from its own surroundings. Large-scale growth passes in every run, including two 512³ realisations, and with cold energy placed where real, gas-stripped galaxies put it (CFG518; PAPER45 v2.1). Once halo cores were resolved, the bookkeeping turned out to rob them (CFG521, CFG526). A rebuilt engine that draws only from each halo's outer reservoir now makes halos match the law's own profile at every resolution (CFG527). Whether small-scale clumpiness converges is being settled by a fixed-box resolution study (CFG530, running). The condition: cold energy is bookkeeping, not simulated particles, and its settling is not derived from an action.
- **Fails: structure growth, chassis alone.** Without B's switch, all matter feels the MOND boost and structure grows about 7× too fast, which CMB lensing rules out. This variant is dead; candidate B is the live one.

## Column 4 · The deep "why"

- **Open:**
  - why κ = ½ (twelve derivation attempts, none successful);
  - what sets the amount of cold mass;
  - how "ownership" (which system carries the extra pull) arises from an action.
- **Conditional: quantum stability (G12).** It needs new physics below about 10⁹ GeV, as every theory of this family does.

## The bottom line

The law wins where it is cleanest: rotation curves, MeerKAT, clusters, and every local test of gravity. It separates from MOND on the Milky Way's vertical force. Structure growth has a fix with no hand-set numbers on large scales, and halos now match the law's profile; small-scale convergence is being settled. The pattern in the misses is massive, settled galaxies: central ellipticals, massive isolated lenses (on canonical), and the Milky Way's outer slope (shared with dark-matter halos, and resting on a disputed distance scale). Three things stay open: why κ = ½, what sets the cold energy's amount, and ρ_Λ. The two tests that could change the picture are **Gaia DR4** (2 December 2026) and **a₀ at redshift ~2.5**.

---

κ = ½ is fitted, not derived. The cold mass is still required; no dark-matter particle is added. The board is generated by [`campaign_fresh_gravity/closure_map/status_picture_2026_10_03.py`](../campaign_fresh_gravity/closure_map/status_picture_2026_10_03.py), and the a₀ chart by [`chart_a0z_one.py`](../campaign_fresh_gravity/CHART_a0z_rar_z0_5_2026-10-01/chart_a0z_one.py).
