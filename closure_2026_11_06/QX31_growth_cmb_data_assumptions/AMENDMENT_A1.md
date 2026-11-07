# QX31 Amendment A1 (POST-RESULT, disclosed): K1 reference values

Kappa = 1/2 FITTED; not theory closed.

- **As frozen, K1 FAILS.** The criteria compared this lane's FFP10 chi^2 with 8.3724 (CMB-marged) and 8.7094 (PS1). Those
  are CFG917's reproductions of the Planck package's own unit tests, which are evaluated at the package's test cosmology
  through CAMB. They are not FFP10's spectrum through the binning rule. The lane gives 8.8634 and 9.3140.
- **K1' (added after the first run).** The value on record for FFP10 through this rule is QX3 iter2's K1: 8.863447
  (iter2.json, K1_ffp10_chi2; QX3 iter2's frozen criteria also cite 8.86). This lane reproduces it to 1e-6, so K1' PASSES.
  PS1 at FFP10 (9.3140) has no value on record and is reported only.
- **The units check is unaffected.** K2 (F_PS1 = sum M^XY C^XY_FFP10 + M^PP X_FFP10, max relative deviation 1.33e-4)
  passes as frozen. It matches CFG917 K3b'(i), which got <= 1.3e-4.
- **No statistic, variant, line or label changed.** The code change adds the K1' print and the "direction" wording on
  PARTIAL labels; the numbers are unchanged. The first run's output (before the K1' print) gave the same numbers.
