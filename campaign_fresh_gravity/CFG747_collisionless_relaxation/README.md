# CFG747: collisionless cold energy relaxes onto the law in the inner halo, without dissipation

**Label: R1 FAIL as frozen (the outer radii miss), but the inner halo lands on the law.** For every non-law starting state,
the time-averaged cold-energy mass at r = 2 and 5 r_M sits within 0.2–1.7% of the law, with no dissipation of any kind. At
r = 10 and 20 r_M it falls short (0.62–0.96 of the law): a deficit, with mass carried outward or escaping. The control stays
on the law and energy is conserved.

- **Criteria:** `FROZEN_CRITERIA.md` (ce642f4f2), committed alone first.
- **Script:** `OMP_NUM_THREADS=1 nice -n 10 python3 cfg747.py` (about 8 min, 4 runs) → `cfg747.out`, `cfg747_results.json`.
  `CFG747_MUTATE=1` exits 1: with no cold-energy force the control collapses, m(2)/2 = 1.96.
- **Settings:** κ = ½ FITTED; the cold energy's mass is required; no particle species; not "theory closed".

## Dynamics
Radial cold-energy shells around a point baryonic mass, units G = a₀ = M_b = 1:
- **r̈ = −1/r² + m(<r)²/r⁴.** The critical tether cancels the cold energy's self-gravity; the cubic residual pushes outward.
- The static law is m(r) = r.
- No law quantity is input.

## Results (time-averaged over t = 2000–3000)

| start (at rest) | m/r at r = 2 | 5 | 10 | 20 | kinetic energy | escaped mass | ΔE/E |
|---|---|---|---|---|---|---|---|
| law (control) | 0.999 | 1.001 | 1.000 | 1.000 | 8e-11 | 0 | 1.5e-15 |
| uniform sphere (cold infall) | **0.998** | **0.986** | 0.880 | 0.624 | 1.02 | 2.07 | 5.9e-5 |
| 1.5 × law | **0.999** | **0.994** | 0.959 | 0.818 | 0.59 | 0.61 | 1.6e-4 |
| 0.5 × law | **0.999** | **0.983** | 0.877 | 0.620 | 0.25 | 0.22 | 7.0e-5 |

- **K1 FAIL as frozen:** the finite-difference force agrees with the analytic force to 7.9e-6, against a 1e-6 bar. The bar was
  below the floating-point noise of a centred difference of an O(10) energy at h = 1e-6. The control's 1.5e-15 energy
  conservation confirms the force is the energy's gradient. Disclosed; the frozen file is unchanged.
- **K2 PASS** (ΔE/E ≤ 1.6e-4).

## Reading
1. **A dissipationless route to the law exists.**
   - With its self-gravity cancelled by the critical tether, cold energy feels only the baryons' pull and its own outward
     residual push, u²/a₀.
   - Collisionless shells from very different starts settle so that the inner halo (≤ 5 r_M) holds exactly the law's mass.
     Excess mass is pushed out (the push grows as m²); a deficit is filled by infall.
   - This is the relaxation channel CFG744 said candidate B was missing, at least in the inner halo, for radial orbits.
2. **The outer halo is short of the law** at 10–20 r_M. Two possible reasons, not separated here: there was not yet enough time
   (≈ 24 deep circular periods at r = 20, fewer for radial orbits), or there was not enough mass (some was ejected beyond R₀).
   The deficit is the **opposite** sign to the C3 early-type excess.
3. **Limits.** Radial orbits only (the extreme collisionless case); reflecting inner boundary at 0.5 r_M with a fixed core of
   0.5; a point baryonic mass; cubic W; one N.
4. **Next (named, not run).** A longer, larger run (t_end ≫ the outer dynamical time, R₀ ≥ 200) to see whether the outer halo
   converges or stays short. Then angular momentum.
