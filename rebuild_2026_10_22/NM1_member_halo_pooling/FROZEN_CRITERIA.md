# NM1_member_halo_pooling — FROZEN CRITERIA (committed alone, before any script or graded number)

Written 2026-10-25 (the owner said "keep trying"). κ = ½ FITTED. Footings canonical / alt, scored separately, never
pooled. Cold dark energy (w ≈ 0, clumping, a gravitating field component; not matter, never a particle). Nothing here says
the data favour the framework or ΛCDM. Not "theory closed".

## 0. Hypothesis NM (nested member halos)

X38's a₀-cored halos (Burkert, ρ₀r₀ = Σ_a0 = a₀/(2πG)) pass SPARC, the cluster OUTER bands and the dwarf cap (CD1), but
fail heavy cluster cores (X38/X39: MID T3 Z +4.3/+3.8, MID KT slope +3.1/+3.0, MGAS T3 OUTER +5.4/+4.9). X40b found no
single-halo rule that raises the cluster core surface density.

**Unexamined structural point:** the Σ_a0 cap (CD1: g_h ≤ 0.2545 a₀ for any r₀) holds **per halo**. A cluster is
assembled from galaxies that each carry their own a₀-cored halo. Collisionless material stripped from member halos keeps
following its hosts' orbits, so the members' cold dark energy traces the cluster galaxy distribution, not the smooth
cored cluster halo. Superposed halos can exceed a single halo's cap.

**NM, no new constant:**
1. The cluster's cold dark energy total stays X30/X38's fair share M_fair = 5.364 M_b,tot.
2. The member share is M_mem = R × M★,cl, where M★,cl = M_b,tot/6 (X30's convention: M_b = 1.2 × gas, so stars are
   M_b/6). R is the cold-dark-energy-to-baryon ratio of galaxies from X38's own halo relation
   log M200 = a + b(log M_b − 10) (EM1 background A: a = 11.18, b = 0.9), averaged over a cluster stellar mass function
   (Schechter, log M* = 10.9, α = −1.2, 10⁸–10¹³ M☉): R = ⟨10^a (m/10¹⁰)^b⟩_φ / ⟨m⟩_φ. Capped so M_mem ≤ M_fair.
3. The members' cold dark energy is distributed like cluster galaxies: an NFW number-density profile with c_g = 2.9
   (literature cluster-galaxy concentration, from memory, PROVISIONAL), scaled to r_200 ≈ the turnaround-limited radius
   X30 uses (`rta`), normalised to M_mem within rta.
4. The rest, M_fair − M_mem, forms one Σ_a0 Burkert halo exactly as X38 (`solve_r0`, compact root).
5. SPARC is unchanged (isolated galaxies carry no member population), so X38's SPARC pass stands by construction. That is
   stated, not regraded.

## 1. Grading (X38's cluster cells, unchanged)

The same 15 cells as X38's `grade_clusters`: MID T1–T3 and slope, OUTER all / T1–T3 / slope, OUTER M-all / M1–M3, INNER
all and M-all, both h (0.672, 0.686). A cell passes if |Z| ≤ 2 for both h.

| class | rule (per footing; the lane verdict needs both footings to agree, else UNDECIDED) |
|---|---|
| NM PASSES CLUSTERS | every cell passes |
| NM IMPROVES | no cell that passes in X38 now fails, and the summed |Z| of X38's failing cells falls by ≥ 50% |
| NM FAILS | anything else |

Reported only:
- c_g = 2.0 / 4.0;
- α = −1.0 / −1.4;
- EM1 background B (a = 11.2);
- the member fraction M_mem/M_fair;
- each cell's change from X38.

## 2. Checks

- **K0** With M_mem = 0 the script reproduces X38's cluster predictions (`x38_sd_halos_results.json`) for every cell to
  1e-6 (canonical and alt, h 0.672).
- **K1** The NFW member profile integrates to M_mem at rta to 1e-8. The Schechter averages are checked against
  quadrature on two grids, agreeing to 1e-6.
- **K2** Peak RSS < 2 GB, one thread.
- **MUTATE=1** (separate outputs): place the member share in the Burkert halo instead (c_g → ∞ is replaced by "no
  nesting"). The predictions must equal K0's X38 values, so a MUTATE run that does not reproduce X38 exits 0 (failure),
  and one that does exits 1.

## 3. Disclosed

- **Hand pre-flight (before freezing).** R ≈ 15 gives M_mem ≈ 0.47 M_fair. An NFW with c = 2.9 encloses about 26% of
  its mass inside 0.3 r_200, against about 10% for the cored halo, so at most about 1.8× in the core. The X40b
  requirement is 3–5×.
- A member share proportional to M_b has no KT dependence, so the MID KT slope cell is expected to stay hard. This is
  written now, not found later.
- Stripping is modelled as "traces the galaxies". Dynamical friction and tidal heating are not modelled.
- c_g and the Schechter parameters are literature values from memory (PROVISIONAL), not fitted. Variants are reported.
