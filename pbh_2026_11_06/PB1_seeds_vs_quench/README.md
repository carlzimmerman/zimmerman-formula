# PB1_seeds_vs_quench: PBHs break EB1b's quench only at f ~ 1, M_p 1e6-1e7 Msun

Criteria 3b174fddd7, committed alone before any script or number. Kappa = 1/2 FITTED. Not theory closed.
Conditional on WG2's R1 rule, which fails the CMB-lensing shape (WG2-WG6). Adopts nothing.

**A PBH population is a MASS component that must be paid for.** f = Omega_PBH / Omega_b. The PBH mass is added on
top of B2, in E(a), in the background acceleration and in the clustering mass. At f = 1 that adds Omega 0.049,
as much mass as all the baryons. This lane maps what is NEEDED. Whether such an f is allowed is PB2's question.

## Label (as frozen): QUENCH BROKEN, at the edge of the grid
All checks and controls pass (below). The primary is R1, e(z) median, z_on 50, xi 1, eta_f 1, eps 0.1.

| footing | G_i QSO1 (non-trivial cells) | G_ii galaxy (1e10, 3 sigma, z >= 3) | both gates |
|---|---|---|---|
| canonical | M_p 1e7 at any f >= 1e-10; M_p 1e5-1e6 only at f = 1 | M_p 1e6, 1e7 at f = 1; 1e8 at f >= 0.1; 1e9 at f >= 1e-4 | (1e6, 1), (1e7, 1) |
| alt | same | same | (1e6, 1), (1e7, 1) |
| R0 control | M_p 1e6, 1e7 at f = 1 only | M_p 1e8, 1e9 at f = 1 only | none |

**What the label means.** The quench is broken only where the PBH mass equals the whole baryon mass (f = 1), with
M_p 1e6-1e7 Msun. At f = 0.1 no cell passes both gates in the primary. The boundary lies between f 0.1 and 1, on
the grid's last column.

## Minimal (M_p, f) needed under R1 (both footings agree)
- **(i) QSO1 by z 7.0451, headline mass 10^7.7.** This is set by mechanism (a).
  - A lone point seed binds only about 5.6 M_p of baryons by z 7, about 1 M_p under R0. So Eddington growth is
    supply-limited, and M_BH(z 7) is about 6.6 M_p.
  - The seed must already be about QSO1 / 6.6: M_p >= ~8e6 for 10^7.7, ~1.2e6 for 10^6.9 (interpolated between
    grid points; 1e7 passes 7.7, 1e6 fails 6.9 at 6.6e6).
  - f can be as small as 1e-10, so one rare seed is enough. In this route the PBH is the hole; nothing grows.
  - Smaller seeds (1e5-1e6) pass only at f = 1. There the BH swallows a whole early-collapsing 5-sigma Poisson
    clump (eta_f = 1, the maximal supply). With eta_f 0.1 they fail.
- **(ii) Galaxy-mass collapse by z 3.** This is set by mechanism (b), Poisson isocurvature. It needs roughly
  f M_p >= 1e6-1e7 Msun with N >= 10.
  - 1e10 3-sigma z_coll: 4.4 / 4.8 (canonical / alt) at (1e6, 1); 7.2 / 7.6 at (1e7, 1); 4.5 / 4.9 at (1e8, 0.1);
    2.3 / 2.5 (fail) at (1e7, 0.1).
  - The (a) route counts only for M_p 1e9, f >= 1e-4: one seed binds 1.8e10 by z 3.
  - The law matters here. R0 needs M_p >= 1e8 at f = 1; R1 reaches M_p 1e6 at f = 1.

Which mechanism dominates: **(a) for QSO1, (b) for galaxies.** They meet only at f ~ 1.

## Variants (reported)
| variant | effect on the both-gates region |
|---|---|
| p05 (weakest field) | adds (1e5, 1) and (1e7, 0.1) |
| ZON_REL (boost from z 1000) | adds down to (1e4, 1) on alt, (1e5, 1), (1e7, 0.1) |
| p95, NOPRESS, PBH-EFE, host 3 sigma | unchanged |
| eta_f 0.1 | G_i shrinks to M_p 1e6-1e7 at f = 1 |
| eps 0.2 | drops M_p 1e5 from G_i |
| planted e = 0 (MU1) | G_i down to M_p 1e3 / 1e2 (canonical / alt), G_ii at every M_p 1e1-1e9 with f down to 1e-10-1e-4; 26 / 38 both-gate cells. The quench, not the seeds, is what blocks. |

## Checks and controls (all PASS)
- **KA1** f = 0 reproduces EB1b's canonical/alt p05 and median tables. The collapse pattern is identical, max
  |d ln(1+z)| 1.5e-4 (tolerance 1e-3).
- **KA2** seed-effect scaling: delta_m = f (1 + 3y/2) to 5e-12.
- **KA3** white noise: sigma^2 N = 0.99965.
- **KA4** EdS shell: 1.0641 / 1.6876 against 1.0624 / 1.6865.
- **MU1** e = 0 reproduces EB1's isolated sphere to 6.8e-5, and (a) bound mass is >= with e(z) everywhere,
  strictly larger in some cells.
- **MU2** e = 1e3 matches R0 to 0.14 %, and the G_ii map is identical.
- **MU3** no drag gives more bound mass at z 100 (drag bites). Release (Gamma_d = H) is at z 886.
- **PB1_MUTATE=1** (P_iso x 0): KA3 FAILS, exit 1.

## Verifying the win (post-run diagnostics, no label change)
- **The PBHs' own field.** The ambient field from the iso mode (rms field of an 8e10 fluctuation at z 50) is 0.09
  and 0.27 of WG2's e_web at (1e6, 1) and (1e7, 1). So e_web, not the PBHs, sets the quench in the passing cells.
  The field exceeds e_web only at (1e9, 1), at 2.6.
- **Baryons lag the PBHs.** At z 50, delta_b / delta_p is 0.39 at f = 1 and 0.07 at f = 0.1. The nonlinear shell
  treats the PBH + baryon mixture as one fluid with mass-weighted contrast and velocity, which is an approximation.
  The excess mass is right; the baryon fraction of the first collapse is overstated.
- **Poisson amplitude.** At (1e6, 1), sigma_iso(1e10, z 50) = 0.021 against the adiabatic 5.3e-4, so the
  isocurvature mode is 40 times the Silk-damped baryon field.

## Limits
- Spherical and monochromatic. No PBH accretion feedback, gas heating or mergers.
- The scalar EFE ansatz.
- e(z) is a 12.5 h^-1 Mpc mesh lower bound.
- QSO1 growth uses maximal supply (eta_f 1).
- (b) is used only at N >= 10. The k cut at the PBH separation removes up to ~25 % of the variance at N = 10, which
  is conservative.
- The single-fluid mixture is used in the nonlinear stage.
- No abundance gate: n_p is reported per cell.
- R1 is a rule, not the action.

## Files
- `FROZEN_CRITERIA.md`
- `pb1.py` (imports EB1 / EB1b read-only). Run with `python3 pb1.py`: ~6 min, one thread.
- `pb1.out`, `pb1_results.json`
- `pb1_MUTATE.out`, `pb1_results_MUTATE.json`
