# CL4_cluster_energy_budget: FROZEN CRITERIA (committed before any script or number)

Lane-ID note: frozen as CL1_cluster_energy_budget (first commit below), renamed CL4 because CL1_combined_threshold_budget already exists. Criteria unchanged.

**Question.** CE1's converged cusp is too dense in cluster cores (η 17.67 at 1e13, 16.91 at 1e14; limit 14.3, G-IN-Mall).
BE1 left clusters untested. Is there enough energy, from any named source, to soften them? Budget only: no mechanism.

**Required energy.** BE1's formula, read-only: E_req = (W(η 14.3) − W(η_conv))/2 for the smooth core, at M200 = 1e13 and 1e14,
canonical and alt, f★ 0.034 and 0.0615. c_f 4 (η 10.82) is reported too.

**Sources (each the whole budget, coupling 1):**
- **SN:** E = (M★/100 Msun) 1e51 erg.
- **AGN:** E = 0.1 M_BH c², with M_BH = 0.005 M★ (a ceiling: all stars treated as bulge).
- **INFALL:** E = M★ V200² (order-of-magnitude orbital energy of the stars' host galaxies, gravity only).

Masses: M★ = f★ M_gas (X73's definition), M_gas = 0.10 M200 at both masses. The 0.10, 0.005, 0.1 and 1/100 are assumed
round values from memory, PROVISIONAL, not measured here.

**Output.** ε_req = E_req / E for each source, mass, footing and f★.

**Classes per source (worst mass, worst f★, canonical):**
- **EXCLUDED:** ε_req > 1.
- **AMPLE:** ε_req ≤ 0.01.
- **SUFFICIENT IF COUPLED:** otherwise.

**Checks.**
- **K1:** target η = η_conv gives E_req = 0.
- **K2:** BE1's canonical median at the same loader is reproduced from its committed `be1_results.json`.
- **MUTATE:** M_gas × 0.01 must multiply every ε_req by 100 (within 1%).

**Scope.** Energy only. A pass names a candidate source; it shows no coupling, and CM1 shows coupling can be far below 1.
κ = ½ FITTED. Not theory closed. Cold dark energy is a gravitating field component, never a particle.
