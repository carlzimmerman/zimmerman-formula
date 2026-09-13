# L232 robustness audit

`L232` pooled all radii, so long rotation curves contributed more weight than
short ones.  This independent audit keeps the same fixed cosmological scales,
the same fixed mass-to-light ratios, and the same four parameter-free integer
families, but first computes one RMS residual per galaxy and then averages
those residuals equally.  A 1000-draw galaxy bootstrap measures how often each
integer wins under resampling.

Run:

```bash
python3 fable_independent_2026/L232_robustness_audit.py
python3 -m unittest -v fable_independent_2026/test_L232_robustness_audit.py
```

This is a robustness check, not a likelihood: published covariance,
inclination, distance, and mass-to-light uncertainties are not yet
marginalised.  A surviving `n=2` preference would strengthen the discrete
prediction; a change of winner would show that L232's pooled-point result is
aggregation-sensitive.  Neither result derives the integer from the action,
and neither addresses the relativistic scalar/PPN/FLRW gates.
