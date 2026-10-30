# CL5_agn_gas_cycles: FROZEN CRITERIA (committed alone, before any script or number)

**Question.** CE1's converged cusps are too dense in cluster cores (η 17.67 at 1e13, 16.91 at 1e14; limit 14.3, G-IN-Mall).
CL4 found only the black hole has the energy (ε 0.075 at coupling 1), with no mechanism. LS1 suggests η(M) high at 1e12
and lower at 1e13–1e14. Two questions:
- **Part A:** can black-hole-powered gas cycles soften a formed cluster cusp by gravity alone, within that energy?
- **Part B:** if the cusps were softened exactly to the limits, would the grade then pass?

## Part A: dynamics (CM1's harness, read-only)

**Machinery.** CM1's cold-halo ICs (Eddington DF, N = 200000, seed 1), shell self-gravity, kick-drift-kick, EPS, η
estimator on [x_c(500th), 1]. Units G = M200 = R200 = 1. dt = 1 Myr. Period and ramps below. All R at 10 Gyr against a STATIC of the same
ICs.

**Halos.** NFW c with η = 16.91 (1e14) and 17.67 (1e13) at x_c 0.001 (CE1 medians, ng 48).

**Baryons (units of M200; PROVISIONAL round values, as CL4).**
- Total gas M_g = 0.10, Hernquist scale a_g = 0.20 R200.
- Stars M★ = 0.0615 M_g (X73's f★ definition, the larger graded f★), static, Hernquist a = 0.05 R200.
- Moved gas M_f, Hernquist scale a_f, taken out of the static gas (static gas = M_g − M_f at a_g). In each burst it goes a_f → 8 a_f with
  a cosine ramp over 50 Myr out (about the sound-crossing limit of a cluster core; 5 Myr would be unphysical), returning over 400 Myr. N bursts in 10 Gyr, equally spaced.

**Energy and mass caps on M_f in every burst (the smaller wins).**
- Energy: E_lift(M_f) ≤ ε_c E_AGN / N, with E_AGN = 0.1 M_BH c², M_BH = 0.005 M★ (CL4's ceiling). E_lift is the work to expand M_f from
  a_f to 8 a_f in the static baryons + initial NFW + its own self-energy (CM1's e_lift form).
- Gas: M_f ≤ 2 M_g,H(< 2.414 a_f), so its half-mass content does not exceed the gas already within that radius.

**Runs.**
| mass | a_f | N | ε_c | role |
|---|---|---|---|---|
| 1e14 | 0.05 | 10 | 1 | ceiling |
| 1e14 | 0.05 | 10 | 0.3 | map |
| 1e14 | 0.05 | 10 | 0.05 | **realistic coupling** (AGN feedback models; PROVISIONAL, from memory) |
| 1e14 | 0.05 | 3 | 1 | low cadence |
| 1e14 | 0.05 | 40 | 1 | high cadence |
| 1e14 | 0.02 | 10 | 1 | inner gas |
| 1e14 | a_f = a_g, M_f = M_g | 10 | no cap | BOUND (sensitivity; unphysical) |
| 1e13 | 0.05 | 10 | 1 | ceiling |
| 1e13 | 0.05 | 10 | 0.05 | realistic coupling |
| each mass | none | none | none | STATIC |

**Needed.** R = η/η_STATIC ≤ 14.3/16.91 = 0.846 (1e14), ≤ 14.3/17.67 = 0.809 (1e13).

**Verdict (canonical; route E is above the floor here, so alt has the same dynamics).**
- **REACHES AT REALISTIC COUPLING:** both ε_c 0.05 runs reach.
- **CEILING ONLY:** not that, and at both masses at least one run with ε_c > 0.05 reaches.
- **NOT REACHED AT CEILING:** at either mass, no capped run reaches.
- **NOT DECIDED:** any check fails.
Report which cap binds in each run.

**Checks.**
- **K1:** t = 0 particle η within 5 % of analytic NFW at the same x_c; STATIC drifts ≤ 3 %.
- **K2:** work balance < 1 % in every run.
- **K3:** Σ lift ≤ ε_c E_AGN in every capped run; M_f within the gas cap.
- **MUTATE (monotonic):** at 1e14, a_f 0.05, N 10: R does not fall as ε_c falls, within 0.03. BOUND must move R by > 0.03, else NOT DECIDED.

## Part B: what softening to the limits would buy (X74 grader unchanged, CE1's route)

**Table.** η = 21.2 / 14.3 / 14.3 at 1e12 / 1e13 / 1e14 (BE1's SPARC limit, CL4's cluster limit; c_f-equivalent via CE1's cf()). This is a stipulated target, not a prediction.
f★ 0.034 and 0.0615, canonical and alt.

**Verdict per footing and f★.**
- **TARGET PASSES:** no failing cluster key, SPARC line passes, groups consistent.
- **TARGET BREAKS: lines.** Otherwise.

**Reported, not graded.** LS1's Υ and ΔV by V_flat at the target table.

**Checks.** K4: the grader at CE1's own median table reproduces CE1's committed SPARC rms and Υ. MUTATE: 1e12 η × 0.5 must raise canonical SPARC median Υ.

## Scope
Prescribed gas histories at ceilings, spherical, one seed, formed halo at t = 0; no gas physics is simulated. ng 48 cluster η until A4 finishes: if A4 moves them, the needed R moves.
A reach is existence at that coupling, not a derivation. The mechanism is a new assumption and cannot lower η at 1e13–1e14 without also acting in lower-mass black-hole hosts, which this lane does not test.
κ = ½ FITTED. Footings never pooled. Not theory closed. Nothing here says the data favour the framework. Cold dark energy is a gravitating field component, never a particle.
