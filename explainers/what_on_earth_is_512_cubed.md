# What on earth is 512³ all about?

*The universe-in-a-box simulations, what the number means, and why going from 256³ to 512³ mattered.*

## A universe in a box

To test whether the law can build the cosmic web we see (galaxies, groups, clusters and the filaments between them), we simulate a chunk of the universe on a computer.

- **The box:** a cube 200 Mpc/h on a side, about **one billion light-years** across. It's big enough to hold thousands of galaxy groups and clusters.
- **The start:** a nearly smooth universe at redshift 49, about 50 million years after the Big Bang. The tiny ripples in it are the ones the cosmic microwave background shows.
- **The run:** gravity acts for 13.7 billion years, in 150 time steps, up to today.
- **The test:** how clumpy is the result? We compare it with the same box run with ordinary Newtonian gravity.

The method is called *particle-mesh* (PM). Matter is represented by particles. Each step, their mass is spread onto a grid of cells, gravity is solved on that grid with fast Fourier transforms, and the particles are moved.

## So what does "512³" mean?

It's the size of that grid, and the number of particles.

| | 256³ | **512³** |
|---|---|---|
| cells per side | 256 | 512 |
| particles | 256 × 256 × 256 ≈ **17 million** | 512 × 512 × 512 ≈ **134 million** |
| size of one cell | ~3.8 million light-years | **~1.9 million light-years** |
| memory | a few GB | **~35 GB** |
| run time on the Mac | ~20–40 minutes | **~2.5–4 hours** |

Going from 256³ to 512³ halves the cell size in each direction, so you get 8× the particles. It's like a photo with twice the pixels across: the overall picture is the same, but small things become sharp.

## Why the extra sharpness mattered

The law adds extra gravity, the "phantom", around matter. In the simulations, that phantom builds **too much small-scale structure**: about 15% too much clumping on scales of a few million light-years, against an allowed 10%.

The worry was that this could be a blurry-photo artefact. An earlier check had hinted that the excess *grows* as the grid gets sharper. So we ran the same setup at 512³:

| rule | 256³ | **512³** |
|---|---|---|
| law switched on everywhere (best rule so far) | +15.3% too clumpy | **+17.4%** |

It got slightly *worse* with sharper detail. So the problem is real, and the cheaper 256³ runs were if anything a little too kind.

## The fix being tested at 512³

Two other results pointed at a cure:

1. **The excess comes from halo outskirts.** Most of it sits in the outer parts of groups and clusters, between about half the turnaround radius and the turnaround radius itself.
2. **KiDS lensing allows it.** Galaxy-lensing data (KiDS-1000) only need the law to reach about **0.3–0.5 of the turnaround radius**, once nearby galaxies' lensing is modelled honestly.

So we confined the law to 0.4 of the turnaround radius around each halo and re-ran at 512³:

| 512³ run | overall clumpiness | small-scale excess | verdict |
|---|---|---|---|
| law on everywhere | +2.3% | +17.4% | too clumpy |
| **law confined to ~0.4 turnaround radius** | **+0.5%** | **+8.0%** | **passes** *(canonical footing; the second footing is still running)* |

The same fix at 256³ also passes in three different random universes, so it isn't a fluke of one simulated sky.

## Why 0.4? The "supply edge" idea

The confinement radius might not be a new knob at all. In the working model, the phantom must be filled by real **cold fluid**, and each halo only has so much of it. The phantom's mass grows outward, so it runs out of cold fluid at a radius:

r_supply = r_t / ln(1 + f_ret / 5.364)

- r_t is the MOND radius.
- f_ret is the fraction of its original baryons the halo kept, measured by baryon censuses.

For the halos that matter, that edge lands at about **0.25–0.5 of the turnaround radius**. That's the same window lensing allows and growth needs. This hypothesis is timestamped on Zenodo: **PAPER45, DOI 10.5281/zenodo.23219295**. The next 512³ runs set each halo's radius from its own supply edge, with nothing tuned.

## The honest caveats

- **Not all in yet:** the second footing (a₀ = 1.13 × 10⁻¹⁰) at 512³ is still running.
- **Lensing:** the KiDS window depends on how strongly nearby galaxies contribute to the lensing signal. That's modelled freely, without an outside prior.
- **Bookkeeping:** in these runs the cold fluid isn't moved around particle by particle. The reservoir rule is gravity-level bookkeeping.
- **Not covered:** none of this derives κ = ½, the cold fluid's amount, or the dark-energy density.

## In one line

512³ is the "high-definition" version of the universe-in-a-box test. It showed that the clumping problem is real, and it is now testing whether letting the law stop where the cold fluid runs out fixes it.
