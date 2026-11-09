# SS1 (self-shielded late conversion): FROZEN CRITERIA, committed alone before any script or number

TEST lane, quarantined. Owner decision `closure_2026_11_09/OWNER_DECISION_2026-11-09_SS1_LAUNCH.md`. kappa = 1/2 FITTED;
not theory closed. Adopts nothing. No dark-matter particle is adopted: the component is the record's test object, graded as
HY1 / BG1 / PJ1 / WD1 / XF1 graded theirs. Footings canonical (a0 9.3603e-11 m/s^2) and alt (1.1312e-10), the record's
kappa = 1/2 values as PJ1 / WD1 carry them, graded separately and never pooled. The outside text is not in the repo and
nothing from it is committed; its constants are frozen ONCE below as numbers, and its printed claims are used only as
hand-estimate comparisons.

## 0. Question

The CMB-era clustering component (omega_chi/omega_b = R, F1's value per footing: F1A R_B2 5.4096 canonical / 5.4123 alt)
is pressureless dust before z_dec = 0.55. After z_dec it converts to free dark radiation at a bare rate Gamma0, but the
conversion mediator is reabsorbed where the component's own column is large, so big halos keep their share and small halos
and the field drain. Under ONE gate rule for every system, does this pass every gate the record grades?

## 1. The construction, frozen once

- z_dec = 0.55. Before z_dec: cold, pressureless, the record's cold component of amount R omega_b (the CMB lanes' value).
- Bare rate Gamma0 = 0.820 / Gyr. Conversion time budget tau_tot = 4.49 (field retention exp(-4.49) = 1.12 %), frozen as
  given; Gamma0 x (lookback time to z 0.55 on each footing) is reported beside it. tau(z) = Gamma0 [t(z) - t(z_dec)].
- Escape probability P_esc = 1 / (1 + x^2), x = Sigma / Sigma_gate, Sigma_gate = 0.042 g/cm^2 = 2.01e8 Msun/kpc^2.
  Effective local rate Gamma0 P_esc.
- Column: Sigma(r) = sqrt( max(R500^2 - r^2, 0) * rhobar_chi(<0.25 R500) * rho_chi(r) ), component densities only,
  R500 the pre-conversion halo's (held fixed while it drains), the densities the CURRENT (draining) ones.
- Other outside constants (reported, used only in the Sigma_gate derivation check and the Bullet drag estimate): mediator
  speed 0.0632 c, sigma_phi_chi/m 1.40 cm^2/g, Gamma_psi 4.20 / Myr, R_abs 1.68e-4 kpc^3 Msun^-1 Myr^-1 (Gamma_psi / R_abs =
  2.5e4 Msun/kpc^3). The script searches products of integer and half-integer powers (-1 .. +1) of
  {sigma/m, v_med, Gamma_psi, R_abs, Gamma0, c} with the dimension of a column and prints every one within 10 % of 0.042
  g/cm^2. "Reproduces" iff one lies within 2 %; otherwise "NOT REPRODUCED from the stated constants" and 0.042 is used as
  given (frozen).

**The one gate rule (primary): self-consistent radial peeling.** Each system's pre-conversion component profile rho_chi0(r)
on a log radial grid (300 shells, 1e-3 R500 to R200). Every shell obeys d rho_chi(r)/d tau = - rho_chi(r) P_esc(x(r, tau)),
with x(r, tau) from the column above recomputed at every step (rhobar_chi(<0.25 R500, tau) from the current shells). Shells
at r >= R500 have Sigma = 0 and drain at the bare rate. Integrated with an implicit (backward-Euler, sub-stepped) scheme
from tau 0 to tau_tot; convergence printed (2x steps changes no retained mass by > 1e-4).
- **Members** (Coma UDGs inside Coma; nothing else in this lane is a member): the mediator from a member must cross its own
  column and the host's: Sigma_member = Sigma_own + Sigma_host(d, tau), the host draining under the same rule.
- **Reduced reading (reported):** the outside text's own ODE dx/dtau = -x/(1+x^2), solved exactly from
  ln(x/x0) + (x^2 - x0^2)/2 = -tau, applied to every system with the system column
  x0 = R500 rhobar_chi(<0.25 R500) / Sigma_gate (the column at r = 0 with rho -> rhobar), retention f = x(tau_tot)/x0.
- **Frozen-Da reading (disclosed bracket only):** f = exp(-4.49 / (1 + x0^2)). Never grades.
- The drained mass leaves; the retained profile is NOT adiabatically re-expanded for the lost mass (disclosed; it can only
  make the retained component less concentrated than graded).

## 2. Pre-conversion halos (primary framework-native; brackets disclosed)

- **Primary (the record's KD1 P3 / QX3 G3 capture convention, no LCDM fitting formula):** a system with baryons M_b,sys
  sits at z_dec in a halo whose component mass is M_chi0 = f_cap R M_b,sys, f_cap = 0.76 (X22, QX3 iter2 FCAP), total
  M200 = M_b,sys + M_chi0, profile a singular isothermal sphere (the self-similar collapse profile) truncated at R200, where
  the mean density inside R200 is 200 rho_crit(z_dec) on the footing background (QX15 main h; Omega_m = omega_b (1 + R) / h^2;
  flat with Lambda). R500 = R200 sqrt(200/500) (exact for the SIS). The component is the fraction M_chi0/M200 of the density
  at every radius.
- M_b,sys per class (the record's own conventions, as WD1 / KD1): SPARC M_b(<last point); KiDS the QX5 loader's lens M_b;
  X-COP GB1's Mb_last; groups GB1's gas inside R500 x (1 + f*), f* 0 and 1; Coma UDGs and dSphs M*; MW 6e10 Msun; Bullet
  DB1's per-subcluster gas + stars; Coma's host the law-implied baryons from S1's hydrostatic field (WD1 G5 construction).
- **Bracket B1 (concentration):** NFW at z_dec with the Duffy et al. 2008 full-sample c200(M, z) =
  5.71 (M200 / 2e12 h^-1 Msun)^-0.084 (1 + z)^-0.47 (an LCDM-calibrated fitting formula: disclosed bracket, never grades).
- **Bracket B2 (halo mass of galaxy-scale systems):** for KiDS lenses, SPARC, the Coma UDGs, dSphs and the MW, M200 from
  inverting the Moster, Naab & White 2013 stellar-to-halo relation at z_dec (their eqs. 2, 11-14 with their best-fit
  parameters) at the system's stellar mass (KiDS: the loader's M_b taken as M*), component M_chi0 = M200 R / (1 + R)
  (an abundance-matching relation, LCDM-calibrated: disclosed bracket, never grades). Groups, X-COP and the Bullet keep the
  primary (their halos are baryon-complete). The label is printed under B1, under B2 and under B1 + B2.

## 3. Cosmic mean (background, growth, lensing)

The cosmic surviving share S(tau) = mass-weighted retention over the Press-Schechter collapsed fraction at z_dec on the
footing's CLASS linear power (cold component + baryons, QX15 main theta), halos 1e6 - 1e16 Msun (40 mass nodes, each a
primary SIS system with M_b,sys = M200 / (1 + f_cap R), its retention from the radial peeling at each tau), and the
uncollapsed remainder draining at the bare rate. Sheth-Tormen collapsed fraction reported as a bracket. The converted mass
goes into dark radiation (w = 1/3) with d(rho_dr a^4)/dt = a^4 Gamma0 <P_esc> rho_chi (energy conservation).

## 4. Gates (both footings; the record's lines; per-bin shape where the record grades one)

1. **KiDS isolated lenses** (QX5 lensing() loader, 59 Brouwer+2021 points, WD1 G2 construction; line QX7 iter_4
   FROZEN_CRITERIA.md:26): PASS iff |shift| <= 0.05 dex at every point. Reported: the shift at the points nearest
   0.3, 1 and 1.5 Mpc per stellar-mass bin; retained component inside 200 kpc vs F2's ~0.9 M_b; KX1's per-bin joint-budget
   line (E_b + 2 sigma_tot at 100-300 kpc) beside each bin.
2. **Groups** (GB1's Lovisari 20, GB1 G3 line, WD1 G4 construction): PASS iff >= 16/20 within 2 sigma at f* = 0 AND
   f* = 1. Reported: retention vs pre-conversion R500, and the median residual against the record's +0.19..+0.45 dex step.
3. **X-COP** (GB1 G2 / WD1 G3): PASS iff |mean| <= 0.05, rms <= 0.10 AND every graded r/R500 bin (0-0.25, 0.25-0.5,
   0.5-0.75, 0.75-1, 1-2; >= 3 points) within 0.10 dex (NA2 shape). Reported: retained component over the dynamical mass
   per TR1 bin beside TR1's falling fraction (D canonical 0.71, 0.66, 0.58, 0.46, 0.32) and TR1's own SHAPE statistic
   (RMS <= 0.10, max |SHAPE_b| <= 0.15) read for the retained component as tracer.
4. **Coma UDGs inside the mediator bath** (GB1 G5 rows, WD1 G5 construction with Coma's retained component in the external
   field): REPORTED, not graded (UA1: NOT A TEST); the reading against 2 sigma_U is printed.
5. **SPARC and gas-rich low-density discs** (QX8 exact-field parts, WD1 G1 / G1b): PASS iff rms <= law-only + 0.010 and
   |mean| <= 0.05 (all, and the v_flat >= 250 tail), AND the median retained component inside the last measured radius
   <= F2's allowance (KD1 SPARC_f_max: 0.3257 canonical, 0.1937 alt). AGC 114905 and Malin 1 chi^2 reported.
6. **Background, bare cosmological constant** (DESI DR2 BAO table and Pantheon+ STAT+SYS shape as CFG681 carries them):
   h re-solved so that D_M(z*) (z* from the CLASS reference) equals the no-conversion reference's (theta_s held: r_s is
   untouched, everything before z_dec is unchanged), r_d from the CLASS reference, Omega_Lambda from flatness today.
   PASS iff chi^2_BAO(fixed r_d) + chi^2_SN(M profiled) of SS1 minus the no-conversion reference's <= 4. Reported: the
   h shift, D_M and D_H shifts in % at the DESI redshifts, the r_d-profiled (CFG681 raw-shape) reading, and theta_s's
   shift if h is NOT re-solved. **Bracket, a separate sector (named as such, never grades):** the outside text's
   compensation, the conversion product carrying w = -0.85 instead of radiation; same statistic printed.
7. **CMB.** (a) Primary peaks: by construction unchanged before z_dec; verified by printing omega_b, omega_chi, N_eff at
   z > z_dec (identical), r_s (identical) and D_M(z*) (held). Late ISW NOT EVALUATED (as LD1). (b) **CMB lensing, graded:**
   the record's PR4 machinery (QX3 iter2 / CFG917 data, A_s refit) through GL1's corrected Limber kernel (limber4 as
   WD1 / PJ1 carry it) on the SS1 background, with the ratio R(k, z) of the lensing source (rho_b delta_b + rho_chi
   delta_chi) from the record's two-fluid growth ODE with the time-gated cosmic S(tau): PASS iff chi^2 <= 18.48 (LD1 / KD1
   G9a line).
8. **Forest and growth.** Forest (NC2 G3 band on DESI DR1 P1D, WD1 G9 machinery): z 2.2-4.4 > z_dec, so the ratio is 1 by
   construction; graded PASS iff Delta chi^2 <= 4 (verified at R = 1 identically). Growth: fsigma8 ratios on the DESI DR1
   rows (z 0.295, 0.51, 0.706, 0.919) under CE2's rule as WD1 / PJ1 carry it (each ratio within 2 sigma of both readings,
   and <= 1.001): PASS iff every row passes.
9. **Bullet** (DB1 / UX6 child as WD1 G6 runs it): the retained component is pressureless and collisionless, so it rides on
   the galaxies (DB1 on = "gal"); mediator drag: momentum-transfer rate per unit retained mass ~ Gamma0 <P_esc> (no
   absorption-driven cross-section on the component), Gamma0/Gamma_psi = 1.95e-4 reported. Amount = each subcluster's
   retained component from the radial peeling. PASS iff DB1's label is PASS.
10. **Cassini / Solar System** (GB1 G8 / KT16 via g_ss, WD1 G10): the MW's retained component density at 8.2 kpc as a
    uniform background; PASS iff GB1's line.

**Label.** PASS on a footing iff gates 1, 2, 3, 5, 6, 7(b), 8, 9 and 10 all PASS (4 reported per UA1; 7(a) a
verification). Otherwise **FAIL**, naming the first failing gate in the order 1-10, with the full table. NO VERDICT only if a
known answer fails (stop, grade nothing) or a graded gate is NOT EVALUABLE (missing input named).

## 5. Hand estimates, frozen before any number (primary SIS halos)

- Pre-conversion system column x0 ~ R500 / 135 kpc: clusters (M_b 1.5e14) x0 ~ 7, retention ~0.9, ~3.7 M_b retained
  (KD1's uniform X-COP need is 4.18 / 3.78); groups (M_b 1.5e13) x0 ~ 3.4, retention ~0.55, ~2.3 M_b (need 3.46 at f* 0,
  1.23 at f* 1); KiDS top bin (M_b 2e11) x0 ~ 0.8, retention ~0.02; SPARC discs retention ~0.01-0.02 (<< 0.33).
- So the galaxy and cluster rows may survive on the PRIMARY halos; under bracket B2 the top KiDS bins sit in ~1e13 halos,
  x0 ~ 2.8, retention ~0.4, ~15 M_b of component around a 2e11 lens: KiDS FAILS by > 0.5 dex there (the orchestrator's K1).
- Cosmic S today ~0.06-0.08 (field 1.1 % + halos above ~1e13 at z 0.55); ~92 % of the component becomes dark radiation
  at z < 0.55, Omega_dr(0) ~ 0.15-0.2. Background: BAO FAILS by >> 4 in chi^2 with a bare Lambda (K2; the outside text
  itself reports 4.8 sigma). CMB lensing: the source drops by ~90 % at z < 0.55 only; the shape change is smaller than LD1's
  (decay mostly at z < 2); expect chi^2 between the baseline 8.56 and LD1's 46, side of the 18.48 line unknown (K3).
- Coma UDGs: own SIS halos ~14 kpc, b ~ 2-3 at r_h even fully bathed: shortfall stays ~+0.9 to +1.1 dex.
- Forest PASS by construction; growth fsigma8 at z 0.3 down several % (outside text: -3.4 %), likely inside CE2's 2 sigma.
- Hits recorded as HE-a (KiDS primary PASS, B2 FAIL), HE-b (BAO FAIL), HE-c (X-COP amount within 0.1 dex of the need),
  HE-d (lensing below LD1's 46).

## 6. Known answers (a KA FAIL stops grading)

- KA1 peeling (orchestrator's numbers, outside equations): reduced ODE x0 1.35 -> 0.028, 1.80 -> 0.056, 3.20 -> 0.506
  (each to 0.001); frozen 1.80 -> 0.347 (to 0.001).
- KA2 the radial PDE's central shell of a uniform-density (top-hat) sphere equals the reduced ODE at the same x0 to 1e-4.
- KA3 component -> 0 reproduces the record's law-only numbers on gates 1, 2, 3, 4, 5 to 1e-6 (WD1 KA4: QX8 SPARC rms,
  KiDS shift 0, GB1 L0 X-COP, groups, UDGs).
- KA4 LD1 replay: ld1.py's run() at LD1's Gamma and h reproduces its D1 chi^2 (46.3 / 53.0) to 0.05; and the lane's
  two-fluid + limber4 ratio method at uniform decay (gate off, LD1's Gamma, QX15 h held, decay from z_hi) agrees with
  CLASS's own dcdm lensing chi^2 to within 15 % of (chi^2 - baseline). If this validation fails, gate 7(b) is NO VERDICT
  (not graded on the ratio method).
- KA5 baseline lensing chi^2 8.5599 / 8.5604 at R = 1 (KD1 / PJ1); forest Delta chi^2 0 at R = 1.
- KA6 Bullet: the law alone reproduces DB1 K1 (WD1's check).
- KA7 background: Gamma0 -> 0 returns the reference h to 1e-5 and the reference BAO + SN chi^2 to 1e-6.

## 7. MUTATE (separate *_MUTATE outputs; must bite)

- M1 Sigma_gate x 3 and M2 Sigma_gate / 3: the cluster / group retention and at least one graded gate status or the
  cosmic S(0) must move (printed per gate); "BITES" iff the gate-status vector or the label differs from the main run on
  each footing for at least one of M1, M2; otherwise NO BITE, disclosed.
- M3 z_dec = 2 (gate as frozen): gate 7(b) must FAIL, as LD1 did.
- M4 gate off (P_esc = 1 everywhere, the LD1 class with the frozen time budget): gate 3 must FAIL (clusters keep 1.1 %).

## 8. Lean

The outside text's four "theorems" are restated in the lane's words in RESULT.md with a true / false verdict each (Theorem 2's
bound and Theorem 4's ratio are already known wrong as written). Correct versions of the true ones are written as Lean
statements in `ss1_lean/SS1.lean`, compiled with `lake env lean <abs path>` from the record's Lean tree only if that
environment builds; otherwise left as statements, disclosed. Lean adds no gate.

## 9. Operational

One thread, nice 10, RSS < 1 GB except the record's own CLASS runs and the DB1 Bullet child (peak recorded); preemptible
(SIGTERM checkpoints in parts/); `df -h` before each child, stop under 2 GiB free. Read-only use of every other lane's files.
Outputs: ss1.py (+ ss1_cosmo.py, ss1_bullet.py), ss1.json / ss1.out, ss1_MUTATE.json / .out, parts/, ss1_lean/, RESULT.md.
Explicit-path commits; push via a sparse temporary worktree of origin/main.
