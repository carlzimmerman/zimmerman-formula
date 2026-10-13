# CFG741 — can P-wave heating be the two-sector selector? (frozen criteria, committed alone; order-of-magnitude lane)

Block CFG740–749. Written before any CFG741 number. κ = ½ fitted; both footings; the cold energy's mass is required; no
particle species; not theory closed.

## Why
CFG699 left a two-sector picture:
- a fast polarization field P makes the law's phantom in galaxies;
- a separate cold component C carries the cosmic mass (Ω_C/Ω_b ≈ 5.3), clusters (CFG624: about 3 M_b missing at 0.8 R500),
  the Bullet and the CMB.

C must stay mostly **out** of galaxies (SPARC needs no extra mass) but **in** clusters. CFG696 showed that P relaxes by
radiating its excess energy. The candidate selector: that radiated energy heats C and evicts it from galaxies, but not from
clusters.

## Tests
- **T1 (sympy). Energy radiated.** In the D-form (CFG694), with D = g_N fixed by Gauss, H[P] − H[0] = ∫[W_nl(P) − g_N·P] d³x,
  with W_nl = (4πG)²P³/(3a₀). At the minimum u = √(a₀g_N); for a point mass M_b in the deep regime:
  - E_rad = |ΔH| = (2/3) M_b V_f² ln Λ, with V_f⁴ = G M_b a₀ and Λ = R_out/R_in.
  - PASS iff sympy confirms. A relaxation from P = 0 radiates exactly |ΔH| (CFG696 A2: energy lost = |E_static|).
- **T2. Heating budget.** To keep C unbound inside the galaxy's baryonic region, C's dispersion must reach ~V_f:
  E_need = (3/2)(C/b) M_b V_f², where C/b is the system's cold-to-baryon mass ratio in its catchment.
  - Q = E_rad/E_need = (4/9) ln Λ / (C/b).
  - Evaluate Q for ln Λ ∈ {2, 4, 6} with **galaxies** at C/b = 5.3 (cosmic) and at C/b = 10 (galaxies' missing baryons raise it),
    and **clusters** at C/b = 5.3.
- **Selector viable iff Q ≥ 1 for galaxies AND Q < 1 for clusters, for some ln Λ ≤ 6.** Otherwise CLOSED.
- **T3 (reported). Scale-freeness.** Show symbolically that Q has no dependence on M_b or a₀. Any difference between galaxies
  and clusters can then come only from C/b and ln Λ.

## Verdict
VIABLE / CLOSED by the T2 rule. **Not claimed:** a coupling between P waves and C. It is assumed perfect (100% absorption),
which makes CLOSED a strong result.

## MUTATE (`CFG741_MUTATE=1`, exit 1 iff it bites)
Doubling W_nl's coefficient changes the u at the minimum but must leave |ΔH| ∝ M_b V_f² ln Λ with coefficient 2/3 only if
evaluated at the matched a₀. Check instead that with a **quadratic** W_nl (not SI) the energy is not ∝ ln Λ (T1 fails).
