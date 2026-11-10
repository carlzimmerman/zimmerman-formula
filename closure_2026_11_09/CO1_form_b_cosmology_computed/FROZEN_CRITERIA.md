# CO1 FROZEN CRITERIA: form B's cosmology rows, computed instead of carried (the decision's open item 8)

Committed alone, before any CO1 script exists and before any CO1 number is computed.
TEST lane, quarantined. Adopts nothing, relabels nothing, registers nothing. Footings canonical (a0 9.3603e-11) and alt
(1.1312e-10 m/s^2), graded separately, never pooled. Kappa = 1/2 FITTED; not theory closed. Cold dark energy; no particle.
A fail is reported as a fail, first, in plain words. Nothing here can turn form B into a pass: its open items 1 to 7 stand.

## 1. What is graded

The owner's decision of 2026-11-09 (`closure_2026_11_09/OWNER_DECISION_2026-11-09_FINAL_FORM_B.md`) lists the cosmology rows
of form B as "pass, carried from the cold reference; the 1-halo redistribution is NOT EVALUATED" (open item 8). This lane
computes those rows for form B itself.

- **Linear content of form B:** baryons, photons, neutrinos, the cold component (pressureless, sound speed zero) and a
  vacuum term, under GR. Under B the a0 law is not a force, so nothing but GR acts on the perturbations at any epoch
  (CMB3's open corner A1, a0 at z 1100, does not arise). The parameter set is F1A's B2 cold best fit per footing
  (`closure_2026_11_07/F1A_primary_cmb_audit/parts/fit_B2_<footing>_cold.json`): fitted there on raw Planck PR4 CamSpec and
  ACT DR6 spectra with the footing's own h. No LCDM parameter file is read.
- **Nonlinear content of form B:** its stated dynamics (collisionless cold component and baryons under Newtonian gravity)
  are the record's S0 PM run. Its closure says the cold component around condensed baryons sits as the law's phantom. The
  gap between the two is the 1-halo redistribution: the same mass, laid out differently inside each halo.

## 2. Linear rows (per footing)

**C1. Primary CMB (re-run).** F1A's stored B2 cold best fit is replayed through F1A's own likelihood
(`f1a.PA(f1a.camb_theory(**pars), stored nuisances)`, executed read-only). Statistic: Delta_cal = PA chi^2 - chi2_cal, with
chi2_cal as stored in F1A's `parts/cal.json`. Line (QX15 L1's): Delta_cal <= 9 PASS.

**C2. CMB lensing, linear.** PR4 bandpowers through `cfg917_lib` (conservative L 8 to 400, CMB-marginalised covariance), as
QX3 iter2 loads them. Theory: CLASS at the B2 best fit with its own A_s and tau (other settings as QX3 iter2's `run_class`).
Lines: shape chi^2 with the amplitude refitted <= 18.48 (the record's line), and |A - 1| <= 2 sigma_A, A the data's
amplitude relative to the prediction. Reported: chi^2 at A = 1. Disclosure: F1A's fit has no low-L data, so tau and with it
A_s are weakly held; the amplitude line tests the primary fit's own A_s.

**C3. Growth rate, linear.** DESI DR1 f sigma8 ratio rows as CE2 transcribed them (BGS 0.295, LRG1 0.510, LRG2 0.706, LRG3
0.919; ShapeFit and ShapeFit + BAO panels, errors symmetrised), multiplied by DESI's fiducial f sigma8(z). The fiducial is
used only as the unit the ratios were published in (CLASS at h 0.6736, omega_b 0.02237, omega_cdm 0.1200, n_s 0.9649,
A_s 2.083e-9, one 0.06 eV neutrino; transcribed from memory and flagged as such). Form B: f(z) sigma8(z) from CLASS at the
B2 best fit. Line: every bin within 2 err on both panels. Reported: chi^2 per panel and sigma8.

## 3. The layout whose redistribution is evaluated (z = 0)

Machinery: CFG556's halo model, library part executed read-only (engine spectrum, sigma(M), mass function, bias, NFW with
its c(M), turnaround at Delta_ta 11.81, `baryon_cum`, `U_of`, `spectra_ta`, `spectra_std`). Units Msun/h, Mpc/h. FB is the
engine's baryon fraction (0.1571, cold-to-baryon ratio 5.364 against F1A's 5.41; used so that mass is conserved against S0).
For a reference halo (M200m = M, NFW M_L(<r), turnaround mass M_ta at r_ta, M200c at R200c):

- v_vir = sqrt(G M200c / R200c). v_stiff = 265.8 / 288.1 km/s (PD1 A1). nu is PD1's and ONE1's form: nu(y) = 1/2 +
  sqrt(1/4 + 1/y).
- **Galaxy regime, v_vir <= v_stiff (ONE1's galaxy rule in its own, Lagrangian, scope).** Cold mass (1 - FB) M_ta. Condensed
  baryons M_b = (1 - FB) M_ta / X at the centre, X = PD1's printed share (59.486 / 59.503). Cold enclosed mass
  M_b [m(x) - 1] with m(x) = 1/2 + sqrt(1/4 + x^2), x = r / r_M, r_M = sqrt(G M_b / a0), up to x_t^2 = X (X + 1); X M_b
  beyond. The uncondensed baryons FB M_ta - M_b follow the reference shape M_L(<r) / M_ta.
- **Group and cluster regime, v_vir > v_stiff (PD1 A1 / A2's rule in the R200c scope).** M_b,sys = FB M200c; share =
  (1 - FB) M200c. Baryons inside R200c: `baryon_cum` (CFG556's declared stars and beta-model gas) normalised to M_b,sys at
  R200c. Core: f_core share in the reference halo's own NFW shape truncated at R200c, f_core = pre [1 - (v_stiff /
  v_vir)^2], pre = 1/2. Phantom: W M_b(<r) [nu(G M_b(<r) / r^2 a0) - 1], W = 1.5 v_vir^2 / (1.5 v_vir^2 + (15 km/s)^2),
  source frozen at M_b,sys beyond R200c, capped at E = (1 - f_core) share (constant beyond the radius where it reaches E).
  If it has not reached E at r_ta, the remainder is isothermal (M proportional to r) out to r_ta. The reference's matter
  between R200c and r_ta stays where the reference has it.
- **Comparison layout "Rb" (the cold reference with the same baryons):** baryons exactly as above; the cold component in the
  reference NFW shape (galaxy regime: (M_ta - M_b) M_L(<r) / M_ta; cluster regime: (1 - FB) M_L inside R200c, the reference
  outside).
- Every layout holds M_ta inside r_ta. Spectra with CFG556's turnaround-scope formulas: R_tot = 1 + (P_B - P_Lta) / P_std,
  R_bar = 1 + (P_Rb - P_Lta) / P_std, **R_cold = R_tot / R_bar**: the change made by re-laying the cold component alone.
- Held in z: the z = 0 ratios are used at every z (CFG592's "held"). a0 is constant.

**Inherited ingredients, flagged (owner's rule of 10-10):** the halo list (Tinker 2008 mass function, Tinker 2010 bias,
Duffy 2008 c(M)) and CFG556's declared baryon shapes (Moster 2013 stars, beta-model gas) are not framework-native. They are
calibrated on runs of collisionless matter under Newtonian gravity, which is form B's own stated dynamics and S0's; that is
why they are used, and it is not a claim that the data favour anything. They enter only the ratio R; the base spectrum is
the record's own S0 PM run. Brackets below show how far R moves when they are changed.

## 4. Redistribution rows (per footing)

**C4. CMB lensing with the redistribution.** S(L) = [integral of w(z)^2 P_lin((L + 1/2) / chi, z) R_cold(k) over z <= 3,
plus the same integral without R above z 3] / [the integral without R], standard Limber kernel (the form GAL1 and cfg917
use), linear CLASS spectrum of C2. X(L) S(L) is graded with the record's PR4 amplitude rule: r_eff = A(X) / A(S X).
Lines: |r_eff - 1| <= 2 sigma_A,rel (C2's) and the shape chi^2 of S X <= 18.48.

**C5. Raw KiDS-1000 xi+-.** CFG592's native machinery, library part executed unchanged (data, published covariance, n(z),
published cuts, support cut f >= 0.9 on the S0 spectrum, nuisances, fit, `klass`), on CFG596's S0 run (L100 N1024, nodes z
0, 0.5, 1). Models: S0 x R_tot (form B) and S0 x R_bar (the cold reference with the same baryons).
Statistic: **d_cold = chi^2(S0 x R_tot) - chi^2(S0 x R_bar)**. Robustness set as CFG596: widen2, noIA, fade, DESI
distances. Label by `klass(d_cold, robust, N_kept >= 10)`: EXCLUDED (d >= 9 and every robust variant >= 9), TENSION
(d >= 4), CONSISTENT (d < 4 and every robust variant < 9), otherwise NOT DIAGNOSTIC.
Tooth, printed beside the label: the data replaced by form B's own prediction at the Rb best-fit nuisances and refitted
with S0 x R_bar; the redistribution is VISIBLE to KiDS if that chi^2_min >= 9 (CFG596's T-OWN rule), NOT VISIBLE otherwise.
Reported: absolute chi^2 and p for S0, S0 x R_bar, S0 x R_tot; DES Y3 through the same path (CFG596 found DES not
diagnostic); the S0 engine's sigma8 0.811 beside C3's sigma8.

## 5. Label (per footing)

- **ROWS HOLD:** C1, C2, C3, C4 PASS and C5 CONSISTENT.
- **ROWS HOLD, REDISTRIBUTION IN TENSION:** C1 to C4 PASS and C5 TENSION.
- **REDISTRIBUTION EXCLUDED:** C5 EXCLUDED or C4 FAIL.
- **LINEAR ROW FAILS:** any of C1, C2, C3 fails; the row is named.
- NO VERDICT if a known answer fails or a mutation arm does not bite; C5 NOT DIAGNOSTIC is reported as that.
The label always carries the words "with an inherited halo list". The forest row is not recomputed; it stays carried.

## 6. Brackets (reported, never graded)

Core prefactor 1 and 0. Regime boundary at M200m 1e13 Msun/h instead of v_stiff. Galaxy rule in the virial scope (cold
(1 - FB) M200m, X unchanged). Gas core radius 0.2 R200c instead of 0.1. Press-Schechter mass function with the Mo-White
bias in place of Tinker. c(M) x 0.7 and x 1.3. nu(y) = 1 / (1 - exp(-sqrt(y))) (CFG556's kernel) in place of the simple
form. KiDS amplitude: the S0 spectrum scaled by (sigma8 of C3 / 0.811)^2.

## 7. Known answers

- KA1: the executed CFG556 machinery reproduces its committed primary table (R at k 1: 1.716 / 1.885; sigma8 ratio
  1.0402 / 1.0463) to 1e-3.
- KA2: nulls. Layout Rb with the reference's own baryons gives R = 1 to 1e-6; the cluster rule with pre = 1 / (1 -
  (v_stiff / v_vir)^2) (all of the share in the core) and W = 0 gives R_cold = 1 to 1e-6 in the cluster regime.
- KA3: every layout is non-decreasing and ends at M_ta (1e-9).
- KA4: the executed shear machinery reproduces CFG596's S0 rows: KiDS N_kept 104, chi^2 144.26; DES 52, 68.64 (0.01).
- KA5: the PR4 row of the record's reference X0: chi^2 8.5708, A 1.0210287 (as GAL1's KA1).
- KA6: C1's replay equals F1A's stored PA chi^2 to 0.1 (3740.157 / 3740.301).
- KA7: m(x_t) = 1 + X at x_t^2 = X (X + 1) to 1e-12.

## 8. MUTATE

- M1 (C5 has teeth): CFG556's candidate-B primary layout in place of form B's; chi^2(S0 x R) - chi^2(S0) must be >= 9 on
  KiDS, canonical (CFG596 measured +68.73 with the PM's own boost).
- M2 (C4 has teeth): R_cold = 1.10 flat at z <= 3 must break C4's amplitude line.
- M3 (C1 has teeth): F1A's stored baryons-only best fit replayed must give Delta_cal > 25.
- M4 (the layout responds): the cluster rule moved to the Lagrangian scope (share (1 - FB) M_ta) must raise R_cold at
  k = 1 h/Mpc by at least 0.10 over the primary.

## 9. Disclosures

- Seen before the freeze: F1A's, QX15's, CMB3's and GAL1's results (C1 and the PR4 reference row are known to pass for the
  cold reference; C1 is a re-run). CFG556's table (candidate B +0.72 / +0.88 at k 1; its r200m-scope bracket -0.081 /
  -0.047). CFG596's S0 chi^2 (144.26, p 0.014) and its EXCLUDED label for candidate B. PD1's, ONE1's and RB1's criteria;
  PD1's results. No CO1 number exists.
- Hand estimate (unverified, written before any code): the cluster rule puts about half the share in the reference's own
  NFW and caps the phantom near 0.7 R200c, so |R_cold - 1| should stay below about 0.1 at k <= 1; the galaxy regime adds
  little there. Expected: C4 PASS with |r_eff - 1| below 0.01; C5 CONSISTENT or TENSION; the sign of d_cold not known.
- What a ROWS HOLD label would and would not say: the cosmology rows survive counting the layout, for this layout, with an
  inherited halo list. It would not say the layout is derived (open item 1), and it is not evidence for the framework: a
  cold component of the fitted amount gives the cold-component spectra.
