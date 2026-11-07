# EW2 iter_2 frozen criteria: AeST's dust branch on the linear web (SV5 target), primary CMB, KiDS hosts

Kappa = 1/2 FITTED; not theory closed. Committed with ../FROZEN_CRITERIA.md before any script or number. Both footings,
never pooled. Machinery reused read-only: SV5 (sv5_common.py loaders: QX3 iter3 corner background, CLASS P_lin, PR4
lensing likelihood I2; sv5_iter1.json's law-on response B_W(k, z) per footing), QX5 loaders (KiDS lensing points LE),
QX10's G6 line.

## Class A_mu

AeST with dust/mass scale mu (physical, Mpc^-1), any F in SZ's family including v4's capped F. The scalar's own scale
splits the web (iter_1): comoving k < k_sw(z) = mu/(1+z) is the dust branch (law off: Jcal is absent at linear order and
the field's gradient is suppressed by (k/a mu)^2 there); k >= k_sw is the Jeans-type band, where the field's static
equation is the a0 law (C1) and, at linear order with F_Y(0) = 0, there is no Newtonian restoring term (C7 runaway).
Response used (generous to AeST: the band is given the law's nonlinear response, not C7's linear runaway):

  B(k, z) = 1 for k < k_sw(z);  B(k, z) = B_W(k, z) (SV5 iter_1, same footing) for k >= k_sw(z).
  Floor variant (reported): B = nu_min(z)^2 (SV5's Lean bound per z) in the band.

Dust amount: AeST's I0 is an initial datum (C2 K2, FITTED). The web field is SV5's target (the dust reference times
A_X0), so W1 grades the GAIN of the law on the web only; the amount is NOT a prediction (reported NOT EVALUABLE).

Projection exactly as SV5's project(): sqrt(B) per z interpolated in ln k on the solver grid (held outside the box
shells and outside z in [0.25, 50]), then Rr(k_i, z_j) = 1 where k_i < mu/(1+z_j); S = I2.limber_ratio; A_S from
I2.best_amp_chi2(X0 S); r = A_X0/A_S; Delta chi^2 = chi2(X0 S) - c0.

## Gates (per footing)

- W1 (SV5 lensing amplitude line): |r - 1| <= 3 sigma_A,rel (sigma_A,rel from SV5's T0.4, about 0.024).
- W2 (shape): Delta chi^2 <= I2.DCHI2_LINE (4).
- QX15 primary CMB: not rerun (needs C7's patched CLASS). Graded by the record's computed result: C7 (patched CLASS
  3.3.4, gauge-checked) finds every BBN-compatible small-K_B lambda_s = infinity configuration, v4 included, runs away at
  linear order (P/P_ref 1e2-1e41 by k <= 10 h/Mpc, chi^2 1.2e3 to infinite) -> FAIL [C7 read]. Reported with it: the band
  edge at last scattering, k_sw(z* = 1090) = mu/1091, against the acoustic range k 0.005-0.3 Mpc^-1.
- G6 KiDS (QX10 line): the static spherical v4 solve (iter_1 equations, Delta = 0 primary) on each KiDS mass bin of QX5's
  LE list (Brouwer+21 isolated, log Mb 9.4, 10.45, 10.7, 10.9) as a Hernquist profile with a_h = 3 kpc (H2's galaxy-guard
  form); each LE point at r = sqrt(G Mb/gbar); shift_i = log10(g_law(r_i)/g_AeST(r_i)); G6 = mean over LE points.
  PASS iff |G6| <= 0.05 dex and g_AeST > 0 at every LE radius. Zero-point envelope (reported only, a free constant if it
  is what passes): one universal Delta in [-8, 2] step 0.25.

## Members graded and the class map (no member adopted; this is a map, not a fit)

- Declared members: mu in {0.0156, 0.1, 0.3, 0.5, 0.7, 1.0, 1.58, 2.0, 3.0, 10, 56.6, 2.04e4, 1.24e8} Mpc^-1 (iter_1).
- Map: 61 log-spaced mu over [1e-3, 1e9] Mpc^-1 (0.2 dex). mu_w = the smallest map value from which W1 and W2 pass at
  every larger map value; mu_h = the largest map value up to which G6 passes at every smaller map value. Resolution
  0.2 dex, stated.
- Hosts at mu > 1e3 Mpc^-1 (numerically infeasible: > 3e3 radians of oscillation inside R_ref) are graded by the bound
  H-inf, derived in the README before use: in the spherical static form with M_b constant on [R/2, R], a solution with
  |g/g_law - 1| <= eps on [R/2, R] needs (mu R)^2 <= 512 delta/(1 - eps), delta = 2 eps + eps^2. At eps = 10^0.05 - 1 this
  is mu R <= 12.3; a member above it fails the 0.05 dex line pointwise on that octave. Labelled "FAIL [bound]".

## Label

Per footing. NO-GO FOR CLASS A_mu (web + KiDS) if no map member passes W1, W2 and G6 together, on both footings
(Lean T4 for the window statement mu_h < mu_w). PASS for the members that pass all three (QX15 still graded separately).
FAIL otherwise. The amount (I0) is labelled NOT EVALUABLE as a prediction in every case.

## Known-answer checks

- KA1: mu = 1e12 (every mode dust): r = 1 and Delta chi^2 = 0 to 1e-6.
- KA2: mu = 1e-8 (every mode in the band): r equals SV5 iter_1's r (74.7 / 89.4) to 1e-3 relative.
- KA3: the host solver reproduces H2's galaxy guard (Hernquist 1e11 Msun, a_h 3 kpc, canonical, Delta = 0): g/g_law - 1
  at 1 Mpc = +0.090 (mu 0.1), -0.163 (0.3), -1.749 (1.0), each to +-0.005; max |dev| at r <= 200 kpc = 0.003, 0.016,
  0.086, each to +-0.002.
- KA4: mu = 1e-6: |G6| <= 1e-4.
- KA5: halving the solver's max step changes G6 by <= 1e-3 at mu = 0.3 and mu = 10.
If KA1-KA4 fail, the iteration is NOT EVALUABLE.

## MUTATE (separate outputs *_MUTATE)

K2 -> 0 (mu = 0: no dust branch, no static mass term). W1 must FAIL at every member (r = SV5's) and G6 must be 0 to
1e-4. Bites iff the main run's W1 passes for at least one member.
