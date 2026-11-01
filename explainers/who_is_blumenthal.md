# Who is the Blumenthal guy, and what was his deal?

*The person behind the formula that keeps breaking route E's spirals. As of 1 November 2026.*

## The short version

George R. Blumenthal is a theoretical astrophysicist who spent his career at UC Santa Cruz. He helped build the cold dark matter picture of galaxy formation in the 1980s, then wrote down a short formula for what happens to a dark halo when ordinary gas falls into its middle. He later ran the university.

He comes up here because of that formula. It's what "Blumenthal" means in UR1, UR2, NR3 and the rest.

## The person

- **Training:** B.S. at the University of Wisconsin–Milwaukee, Ph.D. in physics at UC San Diego.
- **Career:** joined UC Santa Cruz's astronomy and astrophysics faculty in 1972. His work ranged over gamma ray bursts, compact X-ray sources, active galactic nuclei and cosmology.
- **The famous paper:** Blumenthal, Faber, Primack and Rees, "Formation of galaxies and large-scale structure with cold dark matter," *Nature* 311, 517 (1984). It's one of the founding papers of the standard picture.
- **Administration:** acting chancellor of UC Santa Cruz from 2006, named chancellor in 2007, stepped down in 2019. He then directed Berkeley's Center for Studies in Higher Education until 2023.

So the man whose name sits in your code is a physicist turned university leader, not someone who works on modified gravity.

## The formula

The paper that matters here came two years later: Blumenthal, Faber, Flores and Primack (1986), on the contraction of dark halos as baryons fall in.

**The problem.** Gas cools and sinks to the middle of a halo, forming a disc. That adds gravity at the centre, so the halo's own material gets pulled inward. How far?

**The idea.** If the gas settles slowly compared with an orbit, each orbit adjusts gently, and the orbit's angular momentum stays the same. For a circular orbit, angular momentum squared is proportional to r M(<r). So that product stays fixed:

```
r_i M_i(r_i) = r_f [ M_i(r_i) + M_b(r_f) ]
```

A shell starting at radius r_i with mass M_i inside it ends at r_f, where it now also encloses baryons M_b. Solve it shell by shell and you have the new halo.

**Why it caught on.** It's a few lines of algebra, has no free number, and gives an answer without running a simulation.

**What it assumes:** spherical symmetry, circular orbits, slow change, and shells that don't cross. None is exactly true. Gnedin and collaborators (2004) relaxed the circular orbits by using an orbit-averaged radius, and found the original tends to overestimate contraction in the inner regions. That's "Gnedin" in your lanes.

## Why he came up in your work

**1. The physics is the same for any cold collisionless component.** Blumenthal wrote it about dark matter particles. Your cold dark energy is a gravitating field, never a particle, but in the dust limit it falls along the same paths (DR2 checks this). So his formula applies to route E's halos even though his picture and yours differ about what the halos are. There's an irony there: a founder of the framework you reject supplies the equation that's giving yours the most trouble.

**2. It's the source of the pinch.** Put the formula on version N and spirals get too dense in the middle, leaving less room for stars:

| | No response | Blumenthal |
|---|---|---|
| Υ, SPARC median (A / B) | 0.75 / 0.76 | **0.35 / 0.36** (line 0.50–0.80) |
| Υ at 150–200, 200–250 km/s | 0.57, 0.62 | **0.30, 0.36** |
| Tilt (line 0.15) | +0.59 | +0.17 |

The 0.30 is the grid's floor; the audit reads the true value as about 0.28. UR2 then showed that making halos lighter to compensate runs into blue lensing: δ −0.30 needed, −0.10 allowed. That's the "pinch."

**3. It also has a good side.** UR1 found one nice thing: the same formula, run in both directions, pushes cold material inward in discs and outward in cluster cores, with the crossover at the cosmic ratio and no new number. So the sign of the galaxy and cluster asks comes from one rule. The size is wrong.

**4. Everyone wants him to be wrong, and so far he mostly isn't.** The obvious escape is "that's a crude 1986 formula, real halos won't do this." LC1 tested it: a disc grown live in a simulated zoom gave f_Q 0.872 [0.54, 1.07], close to the formula. The class is BLUMENTHAL HOLDS. So today's doors (Noether flux, phase-space cap, thin disc, fountains, rotation) were all ways of arguing with him, and none got Υ, tilt and LITTLE THINGS to pass together.

**NR4 and RM2 state the requirement plainly:** the response has to be nearly switched off at L★ masses (f about 0–0.2), where gravity alone gives about 0.87.

## Where he could still lose

- **Cores.** LC1's halos are cusps. Blumenthal's circular-orbit assumption is weakest in a pressure-supported core, and route E's core is chosen by hand. DR8's live test on a cored halo is still running. This is the one open route where the formula itself may be the wrong tool.
- **Things gravity doesn't do.** Gas blowing out rapidly isn't adiabatic. The computed channels here don't reach the need at a real coupling (CM1, DR9), but that's the family of processes that would have to do it.
- **Fluid behaviour.** HB1 is testing a cold component with pressure, where shells aren't the right picture. It has its own objections.

## Caveats

The biographical facts come from public sources (Wikipedia, UCSC and Berkeley pages), and they differ slightly on when his chancellorship started. The 1986 paper's details are as described in later papers; I didn't read the original or check its journal reference. None of this says anything about what he thinks of your work, since he hasn't, as far as I know, seen it.

κ = ½ FITTED, unused in these rows. Cold dark energy is a gravitating field component, never a particle. Not theory closed. Nothing here says the data favour the framework.

## Sources
- [George R. Blumenthal, Wikipedia](https://en.wikipedia.org/wiki/George_R._Blumenthal)
- [UCSC Magazine, "A chancellor looks back"](https://magazine.ucsc.edu/2019/03/a-chancellor-looks-back/)
- [Berkeley CSHE profile](https://cshe.berkeley.edu/people/george-blumenthal)
- [Gnedin et al., contraction of halos in response to baryons](https://arxiv.org/abs/astro-ph/0510539)
- Repo: `rebuild_2026_10_22/` lanes X39, UR1, UR2, NR3, NR4, LC1, DR2
