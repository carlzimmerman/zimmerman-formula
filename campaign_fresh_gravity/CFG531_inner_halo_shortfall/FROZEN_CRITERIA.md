# CFG531 FROZEN CRITERIA: is the KiDS inner-bin deficit the same shortfall as the SLUGGS centrals' residual?

Written 2026-10-09, before any CFG531 script was written or any CFG531 number computed. Inputs inspected so far are committed
results only: the CFG529 JSON model vectors and README, the CFG528/528b JSON offsets and README, CFG509's README, CFG468's JSON.

Standing settings: a0 = kappa c sqrt(G rho_DE), kappa = 1/2 FITTED. Footings 9.3603e-11 (canonical) and 1.1312e-10 (alt) are
scored separately and NEVER pooled. Kernel nu_mono = 1/(1 - exp(-sqrt y)) with the record's monotone splice. Candidate B (the law
inside bound halos; phantom = settled cold energy; census edge at >~ 500 kpc). The cold energy's mass is still required. No knob is
fitted. Not "theory closed". Compute: nice 10, <= 4 threads, no PM runs, nothing downloaded.

The owner asked "are you sure?". The hypothesis under test is adversarial: KiDS (law-type profiles short in the inner 9 bins once
satellites are stripped, CFG529) and SLUGGS centrals (+0.07 to +0.14 dex in sigma_los after the joint best case, CFG528b) are the
same thing, namely the law + baryons under-predicting mass at ~10-100 kpc around massive galaxies.

## 1. The common quantity

**epsilon = Delta M(<r) / M_pred(<r)**, the fractional extra enclosed mass over the framework prediction (law + baryons; the lens's
or galaxy's OWN profile only, environment excluded), measured in a radial band.

- **KiDS (deprojection method, declared):** in a band of bins, the model is `m(eps) = E + (1 + eps) * own`, where E is the CFG529
  f30-matched environment (stacked) and own the stacked law-type own profile (with the f30 stripping mix). eps is the GLS estimate
  `eps = (o^T W r) / (o^T W o)`, `sigma_eps = (o^T W o)^-1/2`, with `r = d - E - own`, `o = own` (moster SHMR) and
  `W = (C/hart(n_band) + delta delta^T)^-1`, delta = model(behroozi) - model(moster) (CFG529's chi2c, unchanged). Delta Sigma is
  linear in the enclosed-mass profile, so eps is EXACTLY Delta M(<r)/M_pred(<r) when the extra mass is proportional to the predicted
  own profile over the radii that feed the band; for any other shape it is an approximation, tested by MU2 below.
- **SLUGGS:** the per-galaxy offset o_i = mean over the outer GC bins of log10(sigma_obs / sigma_pred). The Jeans equation is linear
  in g, so a uniform mass excess g -> (1 + eps) g gives sigma -> sqrt(1 + eps) sigma exactly. Hence
  `eps_i = 10^(2 o_i) - 1`, `sigma_eps_i = 2 ln10 10^(2 o_i) sigma_i` (sigma_i = CFG466's GC bootstrap, statistical only).
  The class value uses the class mean offset and CFG528b's class error. Exact under the same template (tested by MU5).
- **Radii.** KiDS: per band the stack-weighted mean R and the 16-84 % weighted range of the lens-by-lens R (f30 weights); r/r_M =
  sqrt(a0/g) at the band's g-bin edges (footing-dependent; r_M = sqrt(G M_b/a0)). SLUGGS: the outer-bin R range and mean per galaxy,
  r_M from the row's stellar mass (K0 JAM-law calibrated, stars only; declared).
- **Mass.** KiDS: f30 log M* tertiles (by lens count). SLUGGS: the four centrals' log M* (from the CFG331 table on disk).

### KiDS bands (CFG377 bin order, bin 0 outermost; f30 sample, 57,265 lenses)
- **K-in:** bins 12-14 (CFG377 mean R about 46-81 kpc).
- **K-mid:** bins 9-11 (about 107-189 kpc).
- **K-out:** bins 6-8 (about 251-443 kpc).
- **K9:** bins 6-14 together (the CFG529 "inner 9").
- Per-bin eps is reported (no verdict weight).

### Primary own profile
LAW_RTA (law + baryon point mass to r_ta,law), constructions A (CFG503 sharp) and B (CFG504 smooth), both with the measured f30
leakage (CFG529's EC30). Reason: in candidate B the census edge sits at >~ 500 kpc, so inside 445 kpc the law-type profiles coincide
(CFG529's CENSUS and LAW_RTA vectors are equal in bins 8-14). CENSUS is reported for the base fit.

### SLUGGS rows
- **Primary:** J, the CFG528b joint best case (R-own, heaviest admissible IMF, D x 1.1, most favourable +-2 sigma tracer edges),
  taken from `cfg528b_measured_tracers_results.json`.
- **Reported:** M own and M K0 (measured tracers), the three-galaxy class without NGC 4374, and the four-galaxy class with a 0.05 dex
  per-galaxy systematic added in quadrature (CFG466's headroom).

## 2. Question 1: SAME SHORTFALL? (per footing)
- **KiDS shortfall significant (KS):** eps(K9) > 0 at >= 3 sigma in BOTH constructions.
- **SLUGGS shortfall significant (SS):** eps(J class mean) > 0 at >= 2 sigma (statistical).
- **Overlap statements (reported, they set the label, not the verdict):**
  - kpc: does the K-in band's 16-84 % R range overlap the SLUGGS outer-bin range?
  - r/r_M: does any KiDS inner-9 bin's r/r_M range overlap the SLUGGS outer bins' r/r_M range?
  - M*: does the f30 95th-percentile log M* reach the lowest SLUGGS central's log M*?
  - Environment: f30 lenses are isolated; the SLUGGS four are group/cluster centrals (M87, NGC 5846) or group-dominant. This is
    stated in every verdict line.
- **Amplitude agreement (AG):** |eps(K-in) - eps(J class)| <= 2 sigma_comb (quadrature), in both constructions. K-in is the band
  that overlaps the SLUGGS radii in kpc.
- **Radius agreement (RG):** the KiDS shortfall must be present where SLUGGS measures it: eps(K-in) > 0 at >= 2 sigma in both
  constructions.

## 3. Question 2: alternatives (each killed or confirmed before any shortfall claim; per footing)

### (a) Stellar-mass scale / IMF, in the validated f30 environment
- **Shifts:** M* -> M* 10^delta for delta in {0.05, 0.10, 0.15, 0.20, 0.25, 0.30, 0.40}. M_gal' = M_gal + M*(10^delta - 1); the gas
  part is unchanged. The model is evaluated at the data's fixed physical radii (the measured bins were built with the original M_gal).
- **IMF rising with mass (recalled, PROVISIONAL; Cappellari/Conroy-style):** delta(log M*) = 0.25 clip((log M* - 10.3)/1.0, 0, 1).
  IMF1 applies it to all f30 lenses; IMF2 to early types only (typ = 1).
- **Allowed:** delta <= 0.15 uniform; IMF1; IMF2. delta = 0.20 is the "edge". Larger values are reported only.
- **Environment held fixed** (CFG529's validated E and stripping weights) in the primary. Reported variant: E and the stripping
  weights re-evaluated at log M* + delta (delta = 0.15, 0.20).
- **Construction B:** the shift enters additively, own_B(delta) = own_B(0) + [own_A(delta) - own_A(0)] (declared approximation:
  the transition window only acts beyond r_ta).
- **delta_close:** the delta at which eps(K9) = 0, by linear interpolation on the grid (reported).
- **EXPLAINED BY (a)** if an allowed shift gives, in both constructions, eps(K9) within 2 sigma of 0 AND the inner-9 chi2 of the law
  p > 0.01.
- **Same shift on SLUGGS:** M* x 10^delta on the JAM-law ceiling, row M own (measured tracers): the offset change and the inner JAM
  excess eps_in (CFG528 rule: admissible if eps_in <= 0.06 dex). Reported per galaxy.

### (b) The LCDM-built stripping / satellite term
- **S-off:** own mix at f = 0 (no truncation); E unchanged.
- **S-half:** own mix at f/2.
- **S-502:** CFG502's first-principles environment (E_W30, HOD f, no stripping, linear two-halo) with unstripped own profiles
  (construction A geometry).
- **Reported:** zero leakage (E and own at f = 0, CFG529's T4 setting).
- **DEPENDS ON (b)** if S-off or S-502 makes eps(K9) consistent with 0 (|Z| < 2) in both constructions (S-502: construction A only).
  The LCDM chi2 on f30 of each variant environment is reported, so a variant that LCDM itself rejects is visible.

### (c) Early vs late type
- eps per band for early (typ = 1) and late (typ = 0) f30 lenses separately (data, covariance, own and E stacked with each class's
  weights; colour-blind E, as CFG529).
- **CARRIED BY EARLY TYPES** if eps(K9, early) > 0 at >= 3 sigma and |Z(K9, late)| < 2 (both constructions); CARRIED BY LATE TYPES
  in the mirror case; BOTH if both >= 2 sigma; the class difference is reported with its Z (jackknife covariance of the difference).
- SLUGGS centrals are all early types: if CARRIED BY EARLY TYPES, the comparison is class-matched; it is the record's early/late
  split (CFG505/509), not a new effect. If CARRIED BY LATE TYPES, the two data sets are different galaxies -> DIFFERENT.

### (d) Kernel (report, never adopt)
- nu_simple and nu_standard (CFG468 definitions), a0 rescaled per footing by CFG468's SPARC-fitted ratio a0(kernel)/a0(nu_mono)
  (T-free primary, T-fix reported). Rebuild LAW_RTA (construction A; B additive as in (a)); SLUGGS row M own with the kernel swapped in
  both the JAM calibration and the field (the offset change is added to J, declared approximation).
- Reported: eps(K9), eps(K-in), SLUGGS class eps, and CFG468's SPARC status (Delta chi2; SPARC-PASS needs <= 4 in both treatments).
- **"Kernel removes both"** only if both eps are within 2 sigma of 0 AND the kernel is SPARC-PASS. Report only.

## 4. Question 3: derived mechanism (no knobs)
Statement to test (an analytic fact, written before any run): in candidate B the dynamical mass inside r is
M_law(<r) = nu(G M_b(<r)/(r^2 a0)) M_b(<r), which increases with M_b(<r) and cannot exceed its value for M_b(<r) = M_b(total). So any
redistribution of a FIXED baryon mass (adiabatic-contraction analogue, extended vs point stars, the round rule on a spherical
distribution) can only lower the prediction at r relative to the point-mass law. The census edge only removes mass where it binds
(CFG528 item 3). The KiDS own profile already uses a point mass, i.e. the maximal-contraction limit.

Computed checks (both footings):
- **M-a (contraction bound):** SLUGGS: the stars collapsed to a point (the maximal contraction limit) instead of the Hernquist profile;
  the eps it supplies in the outer GC bins. KiDS: 0 by construction (already a point).
- **M-b (extended baryons / round rule):** KiDS: a Hernquist distribution with the same mass at a = 3 kpc (declared scale, sign check
  only) changes eps(K-in) by how much, and with what sign.
- **M-c (census edge):** the fraction of the K-in and SLUGGS radii inside r_edge (if all inside: the census adds nothing).
- **MECHANISM FOUND** only if a derived (non-template) process supplies >= 50 % of the required eps in K-in AND in the SLUGGS class, on
  both footings. Otherwise **NONE**.
- **Template (not derived, reported):** missing hot CGM baryons in the phantom source. The required extra baryon mass inside the K-in
  radii equals (10^delta_close - 1) M* (from (a)), and for SLUGGS CFG528's gas multipliers. Compared with recalled, PROVISIONAL hot-CGM
  scales; labelled TEMPLATE, never "found".

## 5. Verdict (per footing; if the footings differ the label is FOOTING-DEPENDENT with both given)
In order:
1. If not KS: **NOT DIAGNOSTIC** if |eps(K-in) - eps(J)| <= 2 sigma_comb, else **DIFFERENT**.
2. If KS and EXPLAINED BY (a): **EXPLAINED BY (a)** (with the SLUGGS admissibility of the same shift stated).
3. If KS and DEPENDS ON (b): **EXPLAINED BY (b)**.
4. If KS and (c) reads CARRIED BY LATE TYPES: **DIFFERENT** (different galaxy class).
5. If KS and the kernel removes both (d): **EXPLAINED BY (d)** (report only; the kernel is not adopted).
6. If KS, SS, RG and AG: **SHARED SHORTFALL**, with the overlap label (kpc / r/r_M / M* / environment) and the (c) reading.
7. If KS and SS but not (RG and AG): **DIFFERENT**.
8. If KS and not SS: **DIFFERENT** (SLUGGS no longer significant).
Mechanism: **FOUND** / **NONE** per section 4.

## 6. Controls (load-bearing)
- **K1:** the CFG529 machinery (exec'd read-only up to its controls block) reproduces CFG529's committed f30 LAW_RTA and LCDM chi2 and
  inner-9 chi2 for A and B, both footings, within 0.01.
- **K2:** the rebuilt LAW_RTA own tables at delta = 0 (full, tr_moster_W30, tr_behroozi_W30) equal CFG503's committed tables for the
  f30 groups to 1e-9 relative; the kernel path with nu_mono equals them too.
- **K3:** the CFG528b machinery (exec'd read-only) reproduces its committed row M own offsets to 1e-6.
- **K4:** the SLUGGS kernel swap with nu_mono itself reproduces row M own exactly.

## 7. MUTATE (CFG531_MUTATE=1, separate outputs)
- **MU1 (must recover):** mock d = E + 1.4 own (no noise): eps = 0.400 in every band, both constructions and footings, to 1e-6.
- **MU2 (method test, must recover):** a non-proportional extra mass, Delta M(<r) = 0.3 M_gal (r / 50 kpc) for r <= r_ta,law (an
  isothermal r^-2 shell), projected exactly per group; recovered eps per band vs the true stack-weighted Delta M(<R)/M_law(<R) in that
  band. PASS if |recovered - true| <= 0.25 true + 0.02 in K-in, K-mid and K9 (K-out reported).
- **MU3 (must fail to show a split):** type labels shuffled within each (M_gal, z) group (seed 531): the early-late eps(K9) difference
  must have |Z| < 2.5 in both constructions and footings.
- **MU4 (must fail to detect):** mock d = the model itself (eps = 0): KS must read false.
- **MU5 (must recover):** SLUGGS g -> 1.5 g in row M own: every offset drops by 0.5 log10 1.5 to 1e-6, and the eps mapping returns
  0.5 (relative to the unscaled g) to 1e-6.

## 8. Outputs
`cfg531_kids.py` (KiDS: base, a, b, c, d, MU1-MU4) and `cfg531_sluggs.py` (SLUGGS: common quantity, a, d, mechanism checks, MU5),
`cfg531_verdict.py` (joins the two JSONs, applies section 5). Each writes `.out` / `_results.json`, and `_MUTATE.*` under
CFG531_MUTATE=1. README after the runs. Frozen text is never edited; departures are dated disclosures in the README.
