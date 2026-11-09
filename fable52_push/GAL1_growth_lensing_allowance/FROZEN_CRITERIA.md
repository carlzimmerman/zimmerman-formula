# GAL1 frozen criteria: what growth and CMB lensing allow for the volume law-on regions fill, as a history f(z)

Frozen before any GAL1 script exists and before any graded GAL1 number. TEST lane, quarantined: it relabels nothing in the
record, is not registered, and edits neither fable52_push/README.md nor PAPER70. Both footings (canonical a0 9.3603e-11, alt
1.1312e-10 m/s^2), graded separately, never pooled. One thread, under 1 GB, minutes. No downloads; every data row below is
already on disk in the record.

## 0. The question and what it rests on

SWT1 T2 (fable52_push/SWT1_switch_theorems): law-on regions act on long waves as low-permittivity inclusions, so linear
gravity is boosted by q_C (Maxwell-Garnett; Lean bound q_C <= (3/2) f / (1 - f) for volume filling f). It compared q_C at
one epoch (z 1) with one line, WL1's 0.0354. That line is SV5 iter_1's W1 rule, |r - 1| <= 3 sigma_A,rel with
sigma_A,rel = 0.0241 (SV5 T0.4, the PR4 amplitude error of the record's reference X0), read as r = (1 + q)^2 <= 1.072. It
counts only the direct boost of the potential at one epoch.

The boost acts on linear gravity at every epoch at which the regions exist, so it also changes growth. GAL1 solves the
linear growth equation with G_eff(z) = G (1 + q(z)) in the record's background, forms f sigma8, S8 and the CMB-lensing
power, and turns each probe into a 2 sigma allowance on constant f.

## 1. Background and growth (frozen)

- Background: the record's reference, QX3 iter2's run_class (read-only) at its worst corner, omega_b 0.0215, omega_d
  0.11958060485606123, H0 65, n_s 0.95, A_s 2e-9, tau 0.06, N_ur 3.046 (the background of SV5 T0.4, QX3 iter3's M and
  SWT1). H(z) is taken from CLASS.
- Growth ODE, ' = d / d ln a, for the clustering matter (baryons + cold component):
  delta'' + (2 + d ln H / d ln a) delta' - (3/2) Omega_cl(a) (1 + q(a)) delta = 0,
  Omega_cl(a) = ((omega_b + omega_d) / h^2) a^-3 (H0 / H)^2.
  Initial conditions at z 30 on CLASS's growing mode: delta = D_CLASS(30), delta' = f_CLASS(30) D_CLASS(30). The reference
  is the same ODE with q = 0. Every history below has q = 0 above z 6, so the start at z 30 does not cut any boost.
- Outputs, all as ratios to the reference (scale-independent boost, so no k dependence enters):
  - sigma8 ratio s(z) = D_q(z) / D(z); S8 ratio = s(0) (Omega_m is unchanged).
  - f sigma8 ratio Rf(z) = D_q'(z) / D'(z), with D' from the ODE state (no spline).
  - Lensing-potential ratio R(z) = (1 + q(z)) D_q(z) / D(z). The (1 + q) is the direct boost of the potential that SWT1
    graded; D_q / D is the growth that SWT1 did not.

## 2. CMB-lensing power (frozen formula)

Standard Limber kernel, the one in cfg917_lib.limber_X (the record's own):

  C_L^phiphi = (4 / (L + 1/2)^4) (3/2 Omega_m H0^2 / c^2)^2 integral_0^chi* dchi [(1 + z) (chi* - chi) / chi*]^2 P_lin(k, z) R(z)^2,
  k = (L + 1/2) / chi.

- The boosted-to-reference ratio is S(L) = C_L(R) / C_L(1); the prefactor cancels. P_lin(k, z) from CLASS pk_lin for
  z <= 20; above z 20, P(k, 20) (D(z) / D(20))^2 from CLASS's growth factor. chi from CLASS, chi* at z 1089.
- I do NOT use QX3 iter2's limber_ratio. Its weight per dz is ((chi* - chi) / (chi chi*))^2 (1 + z)^2 / (H chi^2), which
  differs from the standard kernel above by a factor chi^-4. That factor cancels for a z-independent ratio and does not
  cancel for a z-dependent one. A reported check computes S(L) both ways for one history. It relabels nothing.
- The boosted spectrum is S(L) X0, X0 = CLASS's lensing spectrum for the reference (QX3 iter2 X_of). The effective
  amplitude change is r_eff = A(X0) / A(S X0), with A the record's PR4 best-amplitude rule (QX3 iter2 best_amp_chi2 on
  cfg917_lib's PR4 CMB-marginalised conservative bandpowers, L 8-400). For S = c constant, r_eff = c exactly.
- Reported beside r_eff: S(L) at L 100, 200, 400, its mean over L 100-400, and the PR4 shape chi^2 with the amplitude
  refitted (record's line 18.48; X0 8.57).

## 3. Histories (frozen)

- **Readings L, C, NC, NL (SWT1).** q(z) = SWT1's q_tot = q_C + |q_ff| from swt1.py's `compensated` on its own radii tables
  (swt1.py's definitions executed read-only up to `RES = dict(`), on z = 0, 0.25, 0.5, 0.75, 1, 1.5, 2, 3, both footings.
  q is linear in z between grid points and 0 above z 3 (switched on at z 3, the earliest constant-f bracket). f(z) is
  reported beside q(z). For C (filling over 0.30) SWT1's q_C is a lower bound, so a FAIL of C stands and a PASS would not.
  SWT1 uses the z 0 stellar mass function at every z, which over-counts hosts at z 2-3 (disclosed, as SWT1 did).
  Reported: the same readings extended to z 4 and 6 (q = 0 above 6).
- **Constant f, switched on at z_on = 3, 1.5, 0.5.** q = (3/2) f / (1 - f) (the insulating Maxwell-Garnett value, SWT1's
  Lean bound, the form that turned 0.0354 into f <= 0.0231), a step at z_on, constant below it. These histories do not
  depend on a0, so their allowances are the same on both footings.

## 4. Data rows frozen (only rows the record carries)

| probe | row used | where in the record | 2 sigma line (graded) |
|---|---|---|---|
| CMB lensing | Planck PR4 lensing amplitude of the reference X0: A_X0 = 1.0210, sigma_A,rel = 0.0241 (conservative bins L 8-400, CMB-marginalised covariance) | SV5 T0.4 (sv5_t0.out), cfg917_lib PR4 files; replayed here as KA1 | the record's rule on the change (SV5 W1, WL1) at 2 sigma instead of 3: \|r_eff - 1\| <= 2 sigma_A,rel = 0.0482 |
| f sigma8 | DESI DR1 Table 9 ratios as CE2 transcribed them, errors symmetrised: BGS z 0.295: 0.80 +- 0.20 / 0.84 +- 0.19; LRG1 0.510: 1.09 +- 0.13 / 1.16 +- 0.13; LRG2 0.706: 1.05 +- 0.12 / 1.04 +- 0.101; LRG3 0.919: 0.96 +- 0.105 / 0.997 +- 0.092 (ShapeFit / ShapeFit + BAO) | closure_2026_11_07/CE2_late_heated_window ce2.py and FROZEN_CRITERIA (L181 / G045 / CFG508 transcription) | every bin, both panels: \|Rf - r\| <= 2 err |
| S8 | KiDS-1000 S8 = 0.759 +- 0.0225 | SS4 (closure_2026_11_09/SS4_late_pressure_halves) CS line | on the change: \|s(0) - 1\| <= 2 x 0.0225 / 0.759 = 0.0593 |

Reported, not graded:
- Lensing at 3 sigma (1 + 3 x 0.0241, the WL1 / SWT1 line), so the move from 0.0231 can be split into "2 sigma instead of
  3" and "growth added".
- Lensing centred on the data instead of the reference: |A(S X0) - 1| <= 2 / sqrt(b(S X0)) (the boosted template's own
  fitted amplitude and error; for flat S this is r_eff <= A_X0 + 2 sigma_A,abs, about 1.070).
- CE2's suppression-only rule Rf <= 1.001. It was written for lanes that suppress growth; any positive boost breaks it, so
  it is not a 2 sigma allowance. Its allowance is reported.
- Shear-equivalent S8: KiDS cosmic shear sees the boosted potential, so (1 + q(z)) s(z) at z 0.3 and 0.5 against the same
  0.0593 band. The record's S8 rule uses sigma8 only; the graded S8 row follows the record and is the more lenient one.
- CMB3's A_phi scan (closure_2026_11_07/CMB3, +2.4-2.8 in chi^2 at A_phi 0.95 / 1.05, +10-11 at 0.90 / 1.10): sigma
  about 0.031 by my own quadratic interpolation, so a 2 sigma band of about 0.062 on the lensing power. Not graded because
  the error is my interpolation of a four-point scan.

## 5. Allowances and grades (frozen)

- For each graded probe and each z_on: f_max = the largest f in (0, 0.5) at which the probe passes its line, by bisection
  on f (the statistics are monotonic in f for q >= 0; checked on a grid of 11 values and stated). If it still passes at
  0.5, the allowance is reported as > 0.5.
- **Tightest allowance** f_tight = min over the three graded probes and the three z_on.
- Each reading is graded PASS or FAIL on each probe; a reading PASSES overall iff it passes all three graded probes.

## 6. Labels, per footing

- **ALLOWANCE CONFIRMED** iff 0.0231 / 1.5 <= f_tight <= 1.5 x 0.0231 (0.01540 to 0.03465), AND L and C fail, AND NC and
  NL pass.
- Otherwise **ALLOWANCE TIGHTER** if f_tight < 0.01540, **ALLOWANCE LOOSER** if f_tight > 0.03465, with the number and the
  readings that change side. If f_tight is inside the band but a reading changes side: TIGHTER if NC or NL fails, LOOSER
  if L or C passes.
- **NO VERDICT** if any known answer fails, or if a frozen row cannot be read from disk.

## 7. Known answers (each must pass, else NO VERDICT)

- KA1, the record's lensing row replays: A_X0 = 1.0210 and sigma_A,rel = 0.0241 (sv5_t0.out, 4 decimals) within 1e-3
  relative, and X0's PR4 chi^2 equals iter2.json's 8.5709 within 1e-3 relative.
- KA2, G_eff = G reproduces the record's growth: my D(z) / D(0), f(z) and f sigma8(z) = f D sigma8(0) against CLASS's
  scale_independent_growth_factor, scale_independent_growth_factor_f and f x sigma(8/h Mpc, z), at z 0, 0.295, 0.51,
  0.706, 0.919, 1.5, 2, 3: max relative difference <= 2e-3.
- KA3, matter-era growth index: Einstein-de Sitter background (Omega_cl = 1, d ln H / d ln a = -3/2) through the same ODE
  function, constant q in {0, 0.05, 0.3, -0.2}, started off the growing mode; the late slope d ln delta / d ln a equals
  p = (-1 + sqrt(1 + 24 (1 + q))) / 4 within 1e-6.
- KA4, lensing kernel: (a) R = c constant gives S(L) = c^2 within 1e-10 (closed form); (b) my absolute Limber X_L for the
  reference equals CLASS's X0 within 2 % at L 100, 200, 300, 400 (checks the kernel's chi powers and prefactor); (c) an
  independent quadrature, cfg917_lib.limber_X on its own z grid, gives the same S(L) at L 100, 200, 400 within 1e-3 for
  the constant-f history f 0.02, z_on 1.5.

## 8. MUTATE twins (separate outputs; each must bite)

- **M-SIGN** (gal1_MUTATE_sign.*): q -> -q in the growth and the potential. Bites iff growth drops for every positive-q
  history: s(0) < 1, Rf < 1 at all four DESI bins and r_eff < 1.
- **M-POT** (gal1_MUTATE_potonly.*): the boost on the potential only, growth left at the reference (R = 1 + q, D_q = D).
  Bites iff Rf = s = 1 exactly and the lensing allowance at z_on 3 is looser than the main run's by more than 1 %. Its
  check: with the boost on at every z (z_on 1089), the 3 sigma lensing allowance reproduces SWT1's 0.0231 within 0.5 %.

## 9. Hand estimates made before freezing (disclosed)

- Without growth, the 2 sigma line alone gives (1 + q)^2 <= 1.0482, q <= 0.0238, f <= 0.0156: a factor 1.48 below 0.0231,
  just inside the band.
- With growth, a matter-era boost raises D by roughly (3/5) q per e-fold times Omega_m^0.55, so with z_on 3 I expect
  D_q(0) / D about 1 + 0.5 q and r_eff about (1 + q)^2 (1 + 0.5 q)^2 at the lensing redshifts. That would put the
  lensing allowance near 0.010-0.012, below the band: I expect **ALLOWANCE TIGHTER**, and NC (q 0.012-0.020) may cross
  the 2 sigma line. f sigma8 and S8 I expect to be loose (allowances of order 0.1 or more). These are guesses. They do not
  enter the gates, and the gates are not changed to match them.

## Files (planned)

gal1.py -> gal1.json, gal1.out; gal1.py --mutate sign -> gal1_MUTATE_sign.json / .out; gal1.py --mutate potonly ->
gal1_MUTATE_potonly.json / .out; RESULT.md (label first, one table).

kappa = 1/2 FITTED; not theory closed. Adopts nothing.
