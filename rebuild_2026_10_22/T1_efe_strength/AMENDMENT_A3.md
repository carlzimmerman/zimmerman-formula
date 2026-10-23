# T1_efe_strength AMENDMENT A3 (POST-RESULT; append-only; reported-only lines, no verdict line or check changed)

Written after the scored run had printed every frozen number and class. Nothing above is changed.

1. **Satellite tracking controlled for log y₀.** The frozen tracking slope (residual vs log x_e) is positive at every ε.
   Satellites far from their host are also the brighter ones, so a selection effect could make that trend. The partial
   OLS slope on log x_e with log y₀ as a second regressor (same central data; 4000 bootstrap resamples, seed 20261026)
   tests this. Reported only.
2. **Absolute fields.** The Coma UDGs' median total host field (dmean) times their ε_95 gives the largest absolute field
   their AQUAL EFE may act with. P2's 95 % lower bound and F2's (S²-scaled) upper bound in absolute x_e are printed
   beside it, so that the S1-vs-P2 tension can be read in field units as well as in ε units. Reported only.
3. The assembly was re-run with the committed stage files (`T1_SKIP_STAGES=1`); no stage was recomputed.
