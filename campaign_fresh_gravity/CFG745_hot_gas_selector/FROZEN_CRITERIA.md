# CFG745 — a hot-gas selector: cold mass retained in proportion to hot gas (frozen criteria, committed alone)

Block CFG740–749. Written before any CFG745 number. κ = ½ fitted; both footings, never pooled; the cold energy's mass is
required; no particle species; not theory closed.

## Why
CFG741/742 closed the energy and velocity routes. A threshold in mass needs a new scale (the only mass scale in {G, a₀, c} is
c⁴/Ga₀ ~ 10²³·⁶ M☉). A **dimensionless** baryon-state variable needs none. The candidate is the hot-gas fraction of a system's
baryons, f_hot. **Selector H:** the separate cold component C retained in a bound system is C = k · M_hot.

## Inputs (committed lanes; one declared bracket)
- X-COP (CFG624 G2, 12 clusters, ~0.8 R500): per-cluster M_hse, M_b, M_NCE (ν_mono). Converted to simple μ (the construction's
  law, CFG695) by the ratio ν_simple/ν_mono at each cluster's g_b/a₀ at r = 1000 kpc (audit `results.json`).
  - Missing mass resid = (M_hse − M_NCE,simple)/M_b.
- Cluster hot fraction **f_hot,cl ∈ [0.85, 0.95]** (declared bracket; X-COP's gas/star split is not committed).
- Groups (Tian+26, CFG543 addendum): f_hot = 0.08 of M_bar (median). NCE offset +0.010 dex, Z +0.31, so σ = 0.032 dex (CFG624
  G4b, canonical).
- Massive early types (CFG531/CFG580): extra mass needed 0.8 M* (canonical) / 0.55 M* (alt) inside ~100 kpc. eROSITA envelope
  for gas at kT 0.10–0.13 keV: allowed gas = f_bound × required, f_bound = 1.86/1.07 (Z = 0.1), 1.12/0.64 (Z = 0.3), 0.62/0.36
  (Z = 1) (CFG580).

## Tests
- **H1. Calibrate.** k = median over clusters of resid/f_hot,cl, both footings, at both bracket ends.
- **H2. Groups.** Δ_pred = log10(1 + k · 0.08/ν_g), at ν_g = 1.6 and 3.7 (y = 1 and 0.1).
  - PASS iff Δ_pred ≤ 2σ = 0.064 at both ends; TENSION at one end; FAIL at neither.
- **H3. Early types.** M_hot,req = (required extra)/k.
  - **NOT EXCLUDED** iff M_hot,req ≤ the eROSITA-allowed gas for some Z at kT 0.10–0.13 keV, on both footings; else EXCLUDED.
  - Any NOT EXCLUDED is labelled "hot-gas mass unmeasured".
- **H4 (reported, structural).**
  - Galaxies: f_hot ≈ 0 ⇒ C ≈ 0 (SPARC unchanged).
  - Bullet: C is collisionless and retained at formation, so it follows the galaxies, not the stripped gas.
  - CMB: C is cold.
  - Shear (D2): C is reduced in groups. Not scored.

## Verdict
- **SELECTOR CONSISTENT** iff H2 is not FAIL and H3 is NOT EXCLUDED, on both footings at both bracket ends. Otherwise
  INCONSISTENT.
- k is a new constant. With L*, the full construction then has two (CFG679 R1 allows one per candidate), so it is flagged
  "two constants".
- No mechanism for C ∝ M_hot is claimed.

## MUTATE (`CFG745_MUTATE=1`, exit 1 iff it bites)
C = k·M_b (no state dependence) with the same calibration (f_hot,cl → 1). The group shift must then exceed 2σ at ν_g = 3.7,
i.e. a state-blind selector fails groups.
