# QX13 frozen criteria: the virial-heated sector with an entropy floor (the class QX12 left open)

Frozen before any QX13 script or number. Kappa = 1/2 FITTED; not theory closed. Adopts nothing. TEST lane under
closure_2026_11_06/SWARM_BRIEF.md. The sector is COLD DARK ENERGY: no particle, no LCDM inputs. Both footings, never
pooled.

## Why

QX12 (fe628b18af) left one class ungraded:
- iter_2: a host-temperature step at the cosmic ratio R = 5.562 nearly passes X-COP with no cluster input
  (-0.075 / 0.110 canonical, -0.097 / 0.127 alt) but over-boosts groups by 0.1-0.3 dex.
- iter_3: an isothermal sea is all-or-nothing in depth.

What is left is a sector heated by accretion shocks to each host's own virial temperature, with an entropy floor. Like
preheated gas, it is non-barotropic: retained near the cosmic share above the floor, depleted below it.

## The sector (iter_1)

The sector is an ideal fluid with adiabatic index gamma = 5/3, p = K rho^(5/3), where K is its entropy. It gravitates
as a source of the a0 law, as in QX10 and QX12. Only the excess over the uniform cosmic sea gravitates (QX12 iter_3
A1). Each host is spherical and static, and the a0 law is on with self-consistent Picard iteration (QX12 iter_3's
solver form). Units are kpc, Msun and km/s. The hosts are QX12 iter_3's under its Amendment A1:
- SPARC G5 list and KiDS: exponential discs, with r_d from SPARC's own fit;
- ellipticals: QX10's;
- X-COP and groups: measured baryon profiles with a uniform core.
The variant host (core r^max(s0, 1.2)) is reported.

Each host gets one uniform entropy (isentropic), as in Balogh, Babul and Patton's preheated-gas model:
K_host = max(K_sh, K_0).

**Virial shock entropy K_sh, from physics only:**
- The shock sits at r_sh = r_ta/2, the virial radius of spherical collapse (virial theorem for a top hat, R_vir =
  R_ta/2).
- r_ta is QX10's rule.
- Upstream: the cold sea at rho_1 = rho_sea (cosmic mean sector density today, omega_d = 0.1196), falling freely from
  rest at r_ta, so v^2 = 2 H_sh with H_sh = integral from r_sh to r_ta of g_tot.
- Strong-shock Rankine-Hugoniot jump for gamma = 5/3: rho_2 = 4 rho_1, p_2 = (3/4) rho_1 v^2, so
  K_sh = p_2 / rho_2^(5/3).
- K_sh is recomputed each Picard step from the current g_tot.
- Stated simplifications, not tuned: upstream compression and the host's accretion history are ignored. Shells
  accreted earlier would have lower entropy, so a uniform K_sh is conservative toward LESS central retention.

**Profiles.** The enthalpy is w = (5/2) K rho^(2/3), and rho = (2w / (5K))^(3/2).
- Shock case (K_sh >= K_0): inside r_sh, w(r) = w_sh + integral from r to r_sh of g_tot, with
  w_sh = (5/2) K_sh (4 rho_sea)^(2/3) = (15/16) H_sh (identity, Lean). Between r_sh and r_ta the density is rho_sea
  (no excess).
- Floor case (K_0 > K_sh): no shock, and the sector is a hydrostatic atmosphere in open contact with the sea at r_ta:
  w(r) = (5/2) K_0 rho_sea^(2/3) + integral from r to r_ta of g_tot.
- Capture cap, the same convention as QX12 iter_3: the total mass within r_ta is at most f_cap R M_b
  (f_cap = 0.76). If the open mass is larger, the profile is scaled down to M_cap.

**Floor.** K_0 is written through the sea's sound speed today: c_0^2 = (5/3) K_0 rho_sea^(2/3). The grid is 60
log-spaced c_0 values from 1 to 3000 km/s, plus c_0 = 0 (no floor) reported.

## Constant fixed by non-cluster data only (rule frozen now)

The galaxy gates are QX10's lines:
- G5: M_X(< R_opt)/M_b <= 0.3;
- G6: |KiDS mean shift| <= 0.05 dex;
- G7: |ellipticals mean shift| <= 0.15 dex.

Per footing, c_min is the smallest grid c_0 at which G5, G6 and G7 pass at that value and at every larger grid value.
This is the most retention galaxies allow. Retention falls with K, because rho = (2w/5K)^(3/2) decreases in K (Lean).
If c_0 = 0 itself passes the galaxy gates, the floor is unnecessary: K_0 = 0 and c_min is reported as 0. No cluster or
group number enters c_min.

## Predictions, graded at c_min, per footing

- X-COP: the HO1 line (|mean| <= 0.05, rms <= 0.10) on log(M_obs / M_law(M_b + M_X)), 35 points.
- Groups: QX5's mean-band rule over the two stellar allowances. QX10's strict count (>= 16/20) is reported.
- PASS: X-COP and the groups band both pass on both footings at c_min, and the main and variant hosts agree. If the
  hosts disagree, the label is NO VERDICT (host sensitive).
- FAIL otherwise; say which way each misses. The full c_0 scan is context only. A c_0 above c_min that passes both is
  CLUSTER-SET: a FAIL under the no-tuning rule, and a lead.

## Rechecks and owed items (reported, not part of the label)

- **SPARC inner mass:** G5 itself.
- **CMB coldness, T1 / QX10's J0:** comoving k_J >= 50 Mpc^-1 at every z in [10, 3400]. Evaluate it analytically for
  an ADIABATIC floor (K conserved, c_s(z) = c_0 (1+z)) on rho_tot = rho_m (1+z)^3 + rho_r (1+z)^4, with
  omega_r = 4.15e-5 from T_cmb and N_eff, measured inputs. Report the largest c_0 that J0 allows against c_min. If
  c_min exceeds it, the floor cannot be primordial and adiabatic: it needs late injection (z < 10) by a mechanism that
  is OWED (for example QX7's clock switch). That is stated, not graded.
- **Bullet-type offset and linear growth:** argued only. The sector is a collisional fluid, so in a merger it is
  stopped like the gas and does not follow the galaxies. State what that implies for a Bullet-like lensing offset.
  Growth is OWED.
- **Sun:** report the sector mass held inside 1 AU at the local Galactic floor/shock state, against the ephemeris
  bound 1e-10 Msun.

## Known answers

- KA1: no host, Newtonian, large c_0: the profile is uniform at rho_sea, with max relative error <= 1e-4. The line
  is set from QX12 iter_3's measured quadrature floor of 3.9e-5 on the same 900-point grid. It is set before running.
- KA2: the shock identity w_sh = (15/16) H_sh holds numerically on every host to 1e-10 (Lean QX13).
- KA3: R = 0 (no sector) returns QX2's X-COP baseline, +0.4675 / +0.4345, within 2e-3.

## MUTATE (separate outputs)

- M1, floor off: c_0 = 0, so K_host = K_sh. Report the X-COP and groups change against the main run. M1 bites if it
  changes the groups mean band by > 0.05 dex or fails a galaxy gate. If c_min = 0 already, M1 is vacuous by
  construction and reported as such: the floor is then irrelevant, which is a result, not a power failure.
- M2, heating off: K_host = K_0 only (open-contact atmosphere for every host) at c_min. It bites if X-COP's mean moves
  by > 0.05 dex against the main run. If it does not, shock heating is irrelevant to the prediction.
- M3, gate power: K_host x 1e-4 in every host must fail at least one galaxy gate. If it does not, the galaxy gates
  have no power in this class and the label is NO VERDICT.

## Iterations

If iter_1 FAILS, up to two more iterations may change ONLY the physical derivation of K_sh: the shock radius rule, the
upstream density under infall compression, or an entropy profile from self-similar accretion. Each iteration gets its
own frozen criteria in iter_k/ before its numbers, with no constant set from clusters. The floor rule (c_min from
galaxies only) is fixed for every iteration.
