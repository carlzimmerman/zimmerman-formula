# CFG452 FROZEN CRITERIA: T15/T16 settling budget with a0(z) = kappa c sqrt(G rho_DE(z)) (moving target)

Frozen before any CFG452 script exists. kappa = 1/2 is FITTED. Both a0 footings (canonical 9.3603e-11, alt 1.1312e-10, the
z = 0 values) are reported separately, never pooled. a0 TRACKS dark energy: flat a0 is only the w = -1 case. No dark-matter
particle; the cold fluid's mass is still required. Read-only on deepseek_push, CFG450 and CFG451.

## Why
CFG451 put T15/T16 on the framework's a0 but held a0 fixed over the 10.3 Gyr since z = 2. In the framework a0(t) follows
rho_DE(t), so the kernel supply S(<R) = 1/(exp(r_t/R) - 1), r_t = sqrt(G M_b / a0(t)), is a moving target.

## Model (declared, the minimal extension of T15's f_law)
- Relaxation toward the moving target: dM/dt = Gamma (S(t) M_b - M), M = 0 at z = 2, Gamma = lambda sqrt(4 pi G rho)
  constant (rho held as in T15/T16). Today: M/M_b = Gamma * integral_{t(z=2)}^{t0} S(t) exp(-Gamma (t0 - t)) dt.
  With S constant this is exactly T15's f_law * S (control C1).
- a0(z) = a0_footing * r(z), with r(z) = the p13c DESI DR2 chain median of sqrt(rho_DE(z)/rho_DE0)
  (sonnet55_push/puzzle_32pi/p13c_desi_dr2_chains_a0z.csv, 5c037358f). **Primary: DESI+CMB+Pantheon+** (the record's CPL
  curve). Reported separately: Union3, DESY5, DESI+CMB (no SN), and the Pantheon+ q16 and q84 curves as a band.
- Time to z: flat LCDM background (Omega_m 0.30, H0 70) gives the fractional-time map u(z) = (t - t(z=2))/(t0 - t(z=2));
  tau is held at T15/T16's 10.3 Gyr. Only the weighting shape is taken from the background.
- Held, as CFG451: lambda 0.028, tau, rho_R500 1.55e-24, the MW deficits (V 188/200/230; M_b 7e10 and 1e11), the
  group/cluster M_b and R500 conventions, the CFG450 footing-matched deficits, T12's lambda range [0.029, 0.066].
- T16's lambda_max: the lambda at which the moving-target settled mass equals the deficit x (bisection; the budget is
  infeasible if x exceeds the lambda -> infinity limit, which is today's S).

## Verdict items (per footing, per DE curve; same definitions as CFG451)
V1 clusters M_cold/M_b < 0 at b = 0 and 0.3 (overdraft stands); V2 groups b = 0.3 sign (knife-edge if |.| < 0.15);
V3 the MW-30 infeasibility speed (M_b 7e10); V4 floor 0.028 / cluster upper lambda_max (>= 1.5 STANDS, 1.0-1.5 WEAKENED,
< 1.0 BREAKS); V5 the three-way intersection, MW M_b 7e10 (frozen) and T16-verbatim (both M_b).
- **Headline decision:** relative to CFG451 (flat a0), does the primary DE curve change V1 or V4's class on either footing?
  YES -> "a0(z) MATTERS"; NO -> "a0(z) DOES NOT CHANGE THE BUDGET'S VERDICT" (shifts reported).

## Controls
- **C1:** with r(z) = 1 (w = -1), every number equals CFG451's committed cfg451_results.json to 1e-6.
- **C2:** the p13c medians read in are 0.8779 at z = 2 and 0.827 / 0.782 / 0.798 at z = 2.5 (Pantheon+ / Union3 / DESY5),
  to 1e-3.
- **MUTATE (CFG452_MUTATE=1):** plant r(z) = 0.5 for all z > 0 (a0 halved in the past). The cluster b = 0 M_cold/M_b must
  rise by more than 0.1 relative to flat on both footings (the integral must see the history). Outputs go to *_MUTATE files.

A failed control is reported and kept, never silently fixed.
