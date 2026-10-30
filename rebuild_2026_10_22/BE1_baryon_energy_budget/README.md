# BE1_baryon_energy_budget: SN ENERGY SUFFICIENT IF COUPLED (both footings). About 2 % of each galaxy's supernova energy would soften the converged cusp to the SPARC limit

Criteria: `FROZEN_CRITERIA.md` (6304ce4bb0), committed before any script or number. Script `be1_energy.py` execs X74
read-only (X76's loader), with CE1's median c_f table. Outputs: `be1.out`, `be1_results.json` (per galaxy), MUTATE files.
The `x74_*` files here are by-products of that read-only exec.

**What is compared.** For each SPARC galaxy:
- the virial energy needed to turn its converged-cusp core (CE1 η) into the core SPARC allows (η 21.2);
- its supernova energy, (0.5 L[3.6] / 100 M☉) × 10⁵¹ erg.

## Result
| footing | target | active galaxies | ε_req median [16–84 %] | max | ε_req > 1 | Spearman with M200 | class |
|---|---|---|---|---|---|---|---|
| canonical | **η 21.2 (primary)** | 74/175 | **0.017** [0.006, 0.023] | 0.040 | 0 % | +0.59 | **SUFFICIENT IF COUPLED** |
| canonical | η 10.82 (c_f 4, reported) | 74/175 | 0.035 [0.006, 0.083] | 0.119 | 0 % | +0.98 | SUFFICIENT IF COUPLED |
| alt | η 21.2 | 56/175 | 0.018 [0.011, 0.024] | 0.040 | 0 % | +0.39 | SUFFICIENT IF COUPLED |
| alt | η 10.82 | 56/175 | 0.032 [0.012, 0.064] | 0.084 | 0 % | +0.97 | SUFFICIENT IF COUPLED |

- **Checks:**
  - K1: W from M dM/r matches W from ½∫ρΦ dV to 1e-8.
  - K2: E_req = 0 at η_t = η_conv.
  - MUTATE: E_SN × 0.01 gives ε × 100.000000.
- **The class sits just above AMPLE (≤ 0.01).** A galaxy's own supernovae carry about 50× the energy its core needs. Even
  the full step to the c_f 4 rule needs at most 12 %.
- **The required share rises with halo mass** (Spearman +0.6 to +1.0). The most massive SPARC halos need the most.

## Reading (a necessary condition only)
Energy does not forbid a stellar origin for SPARC cores: a percent-level coupling would suffice. This does **not** show
that stars make the cores. Three things are open:
- **The coupling mechanism** (it must act on the cold dark energy through gravity alone, e.g. repeated potential
  fluctuations). It is untested, and its efficiency is not derived here.
- **Clusters.** CE1 shows the cluster cores are also too dense (G-MID-T3, G-IN-Mall). Supernovae in a cluster are far too
  weak against cluster binding energies. This lane did not test them, and a separate energy source (e.g. the central
  black hole) would be a new assumption.
- **The inputs.** The SN numbers (one per 100 M☉, 10⁵¹ erg) are PROVISIONAL, quoted from memory. M★ = 0.5 L[3.6] is the
  Υ in route E's M_b. Virial energy ignores the baryons' own potential.

κ = ½ FITTED. Footings never pooled. Not theory closed. Nothing here says the data favour the framework. Cold dark energy
is a gravitating field component, never a particle.
