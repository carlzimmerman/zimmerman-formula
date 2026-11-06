# QX12 iter_3 frozen criteria: an isothermal sector in contact with the sea, sound speed fixed by galaxies alone

Frozen before any iter_3 script or number (iter_1 8ea6100c3f and iter_2 6241f3ab3b are on the record). Kappa = 1/2
FITTED; not theory closed. Adopts nothing. TEST lane: COLD DARK ENERGY, no particle, no LCDM inputs.

## The sector

Today it is isothermal: p_X = c_s0^2 rho_X, barotropic. It gravitates as a source of the a0 law (as in QX10), is pulled
by g_tot, and is in hydrostatic equilibrium in each host. Early it is cold through the QX7 clock switch:
c_s(z) = c_s0 S(z), with S -> 0 for z > 10. The switch is assumed, not graded here, and growth is owed. One constant
today: c_s0.

Profile (QX10 iter_2's machinery, isothermal version), with H(r) = integral from r to r_ta of g_tot:
rho_X(r) = A exp(H(r)/c_s0^2).
- Open contact: A = rho_sea = the cosmic mean sector density today (omega_d = 0.1196). The retained mass is
  M_open.
- Capture cap: a system cannot hold more than it captured, M_cap = f_cap R M_b,tot (f_cap 0.76, R 5.562, QX10's
  convention). Retained = min(M_open, M_cap); if M_cap < M_open, A is scaled down so the mass is M_cap.
- Self-consistent: damped Picard on M_X(<r), with the law on (QX10 solver form). If it does not converge in 4000
  iterations, the system is labelled NOEQ (collapse) for that c_s0.
- Lensing measures the excess over the sea, so KiDS uses M_X - (4 pi/3) rho_sea r^3.
- r_ta: QX10's rule. Hosts: QX10's (SPARC G5 list as exponential discs, KiDS point masses, ellipticals, X-COP and
  groups from measured baryon profiles).

## Constant fixed by non-cluster data only

c_s0 grid: 60 log-spaced values from 100 to 6000 km/s. Galaxy gates, QX10's lines:
- G5: M_X(<R_opt)/M_b <= 0.3
- G6: |KiDS mean shift| <= 0.05 dex
- G7: |ellipticals mean shift| <= 0.15 dex

Per footing, c_min = the smallest grid c_s0 at which G5, G6 and G7 all pass, and pass at every larger grid value
(retention falls with c_s0, Lean `iso_ratio`). This is the most retention galaxies allow.

## Prediction (graded at c_min, per footing)

- X-COP: the HO1 line (|mean| <= 0.05, rms <= 0.10) on log(M_obs / M_law(M_b + M_X)).
- Groups: QX5's mean-band rule over the two stellar allowances. QX10's strict count (>= 16/20) is reported.
- PASS: X-COP and the groups band both pass on both footings at c_min.
- FAIL otherwise. Say which way it misses. Retention falls monotonically with c_s0, so an under-prediction at c_min
  kills the whole isothermal class: no larger c_s0 helps.
- The full c_s0 scan of X-COP and groups is reported as context only. If some c_s0 > c_min passes both, that is
  CLUSTER-SET (a FAIL by the no-tuning rule) and a lead.

## Known answers

- KA1: no baryons, Newtonian, c_s0 large: the open profile is uniform at rho_sea to 1e-6.
- KA2: c_s0 -> 6000 km/s returns the plain law in galaxies (|shifts| <= 0.02).
- KA3: setting R = 0 (no sector) returns the QX2 X-COP baseline (+0.4675 / +0.4345).

## MUTATE (separate outputs)

- M1: c_s0 = 30 km/s (below the grid) must fail a galaxy gate.
- M2: M_cap -> 0 must return KA3's numbers.
