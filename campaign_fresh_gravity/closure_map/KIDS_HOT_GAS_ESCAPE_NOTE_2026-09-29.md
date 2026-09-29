# KiDS split: can X-ray data test B's hot-gas escape? (data note, 2026-09-29; no lane number)

**Why.** The KiDS early/late split is B's one specific failure relative to the colour-split ΛCDM (CFG61, CFG88, CFG95, CFG96).
- **CFG61's escape:** early-type lenses carry extra baryons, Δf × M*, at the M* node. Δf = 0.25 is acceptable (p > 0.0027), and about 1 is the best fit.
- **So the gas must lie within the smallest 1-halo lensing radius,** about 50 kpc for early types. The split is spread over all seven 1-halo bins, and the innermost two are at about 2.7–2.8σ each (CFG88).

**Source of every number below:** `kids_hot_gas_escape_note.py` (log: `.out`). The orchestrator agreed to record this as a note, not a lane.

## 1. Measured: the eROSITA stacks

The data are eRASS:4, from Zhang et al. 2025, A&A 693, A197 (arXiv:2411.19945), Table 3, read from the arXiv HTML on 2026-09-29. The luminosity is 0.5–2 keV, within R500c.

| log M* | quiescent (QU), erg/s | star-forming (SF), erg/s | QU − SF |
|---|---|---|---|
| 10.5–11.0 (medians 10.8 / 10.7) | (1.1 ± 0.4) × 10⁴⁰ | (0.80 ± 0.50) × 10⁴⁰ | +0.3 ± 0.64 × 10⁴⁰ (0.5σ) |
| 11.0–11.25 | (6.2 ± 0.8) × 10⁴⁰ | (2.3 ± 1.5) × 10⁴⁰ | +3.9 ± 1.7 × 10⁴⁰ (2.3σ) |

- **In the KiDS early-type mass range** (the isolated-lens sample stops at log M* 11.0), the paper finds no significant QU–SF difference.
- **What is measured and what is modelled:**
  - The luminosities are measured stacks, after modelled subtractions of X-ray binaries (Aird+2017), unresolved AGN and satellites.
  - Internally, masked luminosity minus the modelled part equals the CGM luminosity to within 5%.
  - The paper series gives no gas masses, temperatures, densities or metallicities.
- **The radii differ.** The stacks integrate within R500c, which is not tabulated (about 200 kpc for these halos). The early-type lensing radii are about 50–270 kpc.
- **The selection differs.** The stacks are SDSS centrals split by star formation. The KiDS classes are split by colour (u − r > 2.0).

## 2. An estimate, not a result: bremsstrahlung only

The escape's extra gas is placed in its X-ray-faintest geometry, uniform inside radius R. Metal lines are omitted, which makes this a lower bound at a given temperature.
- **Δf = 0.25 within 50 kpc:** 2 × 10³⁸ erg/s at 0.1 keV to 1 × 10⁴⁰ at 0.3 keV. That is below the quiescent 2σ bound (1.9 × 10⁴⁰) at every temperature.
- **Δf = 1 within 50 kpc:** 3 × 10³⁹ at 0.1 keV to 1.7 × 10⁴¹ at 0.3 keV. That is above the bound for T ≥ 0.15 keV.
- **Metal lines would raise all of these,** by a factor that needs a plasma emissivity model.
- **Temperature:** gas in hydrostatic equilibrium in B's potential at these masses would sit near kT ≈ 0.10–0.13 keV (flat v_c 179 km/s; script row 2b). This too is an estimate.

## 3. Measured context: CFG57's X-ray profiles

- **The sample:** the seven X-ray-covered SLUGGS early types, log M* 11.15–11.62, mostly group or cluster centrals.
- **The measurement:** they hold M_gas(<20 kpc)/M* = 0.002–0.03. M87 has the most, at 0.03.
- **Why it is only context:** this is a more massive, X-ray-selected population, at a smaller radius than the escape needs.

## Reading

- **No quiescent excess in the KiDS mass range.** At log M* 10.5–11.0 the eROSITA stacks show none.
- **But band-only data cannot close the escape.** By the bremsstrahlung estimate, metal-poor gas at kT ≈ 0.1 keV would stay below the stacks' sensitivity at Δf = 0.25–1 within 50 kpc.
- **The escape is untested for metal-enriched gas.** Closing it needs an APEC emissivity model for Z = 0.1–1 Z☉ and T = 0.1–0.3 keV. pyatomdb downloads about 95 MB of AtomDB line and continuum files on first use, and that download needs the owner's approval. atomdb.org did not resolve from this machine on 2026-09-29.
- **Measured hot gas is far below what the escape needs.** Around massive, X-ray-bright early types it is 0.2–3% of M* within 20 kpc, against the 25–100% the escape needs, though for a different population and radius.

κ = ½ stays fitted. Nothing here says the data favour either model, or that the theory is closed.
