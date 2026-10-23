# Z2_satellite_systematics AMENDMENT A1 (POST-RESULT; append-only; reported-only lines, no verdict line or check changed)

Written after the scored run had printed every frozen number and class. Nothing in `FROZEN_CRITERIA.md` is changed.
The script gained an `A1` section at its end and extra per-system columns (orbit-MC and host-bracket q, pericentre
interval). A rerun with the cached prediction tables reproduced every pre-A1 output line exactly.

1. **Is the clean subset's drop a host-field selection?** The C1 cut (q < 0.5 at pericentre) keeps distant satellites,
   which sit in weak host fields. v3 static and AQUAL + EFE residuals rise with the host field (frozen V3: TRACKS HOST
   FIELD), so the clean subset's lower median could be selection, not systematics. For each flavor and subset, the drop
   of the median central residual is compared with the drop expected from the full sample's own regression on log x_e
   (and on log x_e + M_V), with a 2000-resample bootstrap. Reported only.
2. **Orbit robustness of the clean subset.** The clean subset recomputed with the E_lo and E_hi host masses (central
   orbits) and with the 84th-percentile q of the 300-draw orbit MC. Reported only.
3. **Host-field slope at fixed luminosity.** d/d log x_e at fixed M_V of the data, log(g_obs/g_bar), and of each
   flavor's own central prediction, bootstrap sd. This restates the frozen V3 proxy rows (M_V control) as data vs
   prediction. Reported only.
