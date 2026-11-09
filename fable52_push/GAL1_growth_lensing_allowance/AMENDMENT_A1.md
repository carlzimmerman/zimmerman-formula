# GAL1 amendment A1 (committed alone, before any GAL1 script exists or any graded number)

**What changes: KA1's tolerance, and the precision of the lensing line. Nothing else.**

- **Reason.** While writing the script I read the record's full-precision row in closure_2026_11_06/SV5_growth_mechanism/
  sv5_t0.json: sigma_A,rel = 0.024061596724788335, A_X0 = 1.021028693246012. The frozen KA1 compares the recomputed values
  with the 4-decimal print (0.0241, 1.0210) within 1e-3 relative. 0.0240616 is 1.6e-3 from 0.0241 in relative terms,
  inside the print's own rounding, so KA1 as frozen would fail on rounding alone and not on any defect.
- **KA1, amended.** The recomputed A_X0 and sigma_A,rel must equal sv5_t0.json's full-precision values within 1e-6
  relative (same machinery, same files, so they should agree to rounding error), and X0's PR4 chi^2 must equal iter2.json's
  chi2_min 8.570880970083943 within 1e-3 relative (unchanged).
- **Lensing line, stated at full precision.** The graded 2 sigma line is |r_eff - 1| <= 2 x sigma_A,rel with the
  recomputed full-precision sigma_A,rel (0.048123 if KA1 passes; the criteria's "0.0482" was the rounded figure). The
  reported 3 sigma line is 1 + 3 sigma_A,rel (1.072185). The direct-only check under M-POT (z_on 1089, 3 sigma) therefore
  expects f = q / (1.5 + q), q = sqrt(1.072185) - 1 = 0.035464, f = 0.02309, against SWT1's 0.0231 (from WL1's rounded
  1.072): the 0.5 % tolerance is unchanged.
- Rows, gates, histories, labels, MUTATE arms and the hand estimates are unchanged. No GAL1 number exists yet: the only
  numbers read are the record's own (sv5_t0.json) and a CLASS timing run that printed the reference's PR4 chi^2 (8.5708)
  and A (1.02103), which are the record's values.

kappa = 1/2 FITTED; not theory closed. Adopts nothing.
