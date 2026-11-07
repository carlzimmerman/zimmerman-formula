# LD1 FROZEN CRITERIA: can a cold component that decays late pass the CMB wall without sitting in discs? (2026-11-06)

Frozen before any script. TEST lane: adopts nothing. Kappa = 1/2 FITTED. Not theory closed.

**Why.** ALL_GATES_NOGO_2026_11_06.md: the CMB needs a cold early component, and KD1 shows such a component is captured
everywhere (f_cap 4.11 x baryons), against SPARC's allowance f <= 0.326 canonical / (alt from kd1.json).

A component that decays to dark radiation late keeps the early universe cold. Discs today then hold only its surviving
share. No lane on the record grades this class. Here it is cold dark energy decaying to dark radiation (CLASS `dcdm -> dr`).
It is not a particle claim.

## Setting, fixed before grading (per footing, never pooled)

- **Background:** omega_b, n_s, tau and the initial omega_dcdm are QX15's main theta for the footing, exactly as KD1
  uses them.
- **h:** re-solved so that 100 theta_s equals its value in the non-decaying model at QX15's h. The primary CMB fixes
  theta_s; decay shifts late distances.
- **Lifetime: the longest SPARC allows.** The surviving share today S = rho_dcdm(0) / [rho_dcdm(z_hi)(1+z_hi)^-3] must
  satisfy f_cap x S <= SPARC_f_max. Here f_cap and SPARC_f_max are kd1.json's `uniform_f_diag` values: canonical 4.111 and
  0.3257, giving S_max = 0.0792; alt values read from the same file.
  - Gamma_dcdm is solved so that S = S_max: the most favourable lifetime for the CMB that discs allow.
  - Assumption, stated: the captured share decays in place with the same lifetime, so disc content today = f_cap x S.

## Gates

- **D1 (primary).** CMB-lensing shape: KD1's G9a statistic (QX3 PR4 machinery, A_s refit), chi^2 <= 18.48.
- **D2 (reported, not graded).** The A_s fixed at QX15's value; the chi^2 and the required amplitude change.
- **D3 (reported).** Clusters at z = 0 hold only f_cap x S <= 0.33. So this class does NOT carry the cluster step, and a
  separate ingredient would still be needed. Stated, not graded.
- **NOT EVALUATED.** The primary TT/TE/EE likelihood with decay (late ISW, the shifted h) is not rerun here. A D1 PASS is
  therefore "passes CMB lensing at fixed theta_s" only.

## Known answer and twin

- **KA:** Gamma = 0 at QX15's h reproduces kd1.json's G9a chi2_mu_inf (8.5599 canonical / 8.5604 alt) to 1e-3.
- **MUTATE:** lifetime 0.2 Gyr (decayed by z ~ 20). D1 must FAIL.

**Label:** D1 PASS on both footings means "the CMB wall has a late-decay escape (lensing level)". Otherwise FAIL, with the
margin.
