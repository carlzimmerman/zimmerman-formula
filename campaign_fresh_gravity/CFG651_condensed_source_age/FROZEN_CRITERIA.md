# CFG651 FROZEN CRITERIA — does THEORY v2's condensed-source rule (A5) predict the early-type AGE SIGNAL?

Committed alone, before any CFG651 script or number. **POST-HOC MECHANISM TEST, NOT A BLIND PREDICTION**: the age signal
has already been seen (CFG585 K9 D +0.94/+0.86, CFG586, CFG631, CFG700 raw-ESD A = +0.166, Z_emp 2.33). This lane asks
whether A5 ("the law's phantom is sourced only by condensed baryons, stars + cold gas"), with no new constant, produces
a signal of that sign and size. κ = ½ is FITTED. Footings canonical (9.36e-11) / alt (1.13e-10), never pooled.
"Cold energy" throughout; its mass is still required. Not theory closed. No ΛCDM or standard-MOND yardstick in a verdict.

## 1. What A5 can change at fixed stellar mass (stated before computing)
The CFG531 / CFG585 law profile already uses the record's condensed source: M_gal = M*(1 + f_cold(M*)),
f_cold = 10^(−0.69 log M* + 6.63) (CFG634 T6a), a function of M* only, so OLD and YOUNG at the same M* get the same
source. Under A5 the only age lever is a colour-dependent condensed (cold-gas) fraction; hot gas is not a source and,
per the census (A9, CFG515), galaxy-scale hosts (log M_ta < 12.5) retain no hot gas at all (f_ret = f_c = 0.10, CFG640).

## 2. Predicted-D derivation (three routes, no new constant)
Per lens i, a condensed-source shift Δf_i (in units of M*_i) changes the law's point mass M_p = M_gal + M*·Δf. Per group g
of the CFG529/531 machinery and per tertile T, Δf_T,g = plain mean of Δf_i over lenses in T ∩ g. The own law profile is
rebuilt with CFG531's `law_vecs` (unedited) at 10^dl − 1 = Δf_T,g, both footings, kernel ν_mono.
- **R2 (PRIMARY, measured proxy on disk):** LePhare SFR_BEST (log SFR) → sSFR S_i = 10^(SFR_BEST − log M*). Inside each of
  CFG700's ten f30-early mass bins, f_cold,i = f_cold(M*_i) · S_i / ⟨S⟩_bin (missing SFR, −99 → the bin median S). The
  normalisation keeps the record's mean cold gas per bin (no constant enters; only the measured SFR rank/ratio).
  Δf_i = f_cold,i − f_cold(M*_i).
- **R1 (census / assembly-epoch bound, CFG515 + CFG640):** per group, f_ret from `fret_census(M_gal)`; OLD converts its
  retained hot share at the largest assembly-epoch bracket χ_age,max = max chi_age in `cfg640_split.json`; YOUNG none:
  Δf_OLD,g = (f_ret,g − 0.10) χ_age,max (M_gal,g/0.10)/M*_g, Δf_YOUNG,g = 0. (Favourable to A5 by construction.)
- **R3 (ceilings, report only):** R3a all of each bin's record cold gas in OLD (Δf = +2 f_cold), none in YOUNG (Δf = −f_cold);
  R3b phase ceiling: OLD sources all census-retained baryons (χ = 1), YOUNG condensed only.

## 3. Statistics and comparison rule
- **PRIMARY (framework-native, raw-data comparison): A_pred** = log10(Σ_k w_k own'_OLD,k / Σ_k w_k own'_YOUNG,k) over K9
  (bins 6–14) with CFG700's masks (ten-bin stratified tertiles) and weights (w = 1/σ² of the all-early raw ESD); own' = the
  stacked LAW own profile (CFG529 construction A own_rec path, SHMR "moster" stripping mix as CFG531 uses; no environment
  term). Compared with CFG700's measured A = +0.1658, σ = 0.0712 (empirical null sd, K9).
- **SECONDARY: D_pred = ε_pred,OLD − ε_pred,YOUNG** with ε_pred = wvec · Δown (the CFG531 GLS weight vector of each tertile's
  K9 fit; CFG585 masks), construction A, compared with CFG585 D(K9) +0.9411 ± 0.3544 (canonical) / +0.8619 ± 0.3241 (alt).
  The CFG531 covariance contains an SHMR term: labelled context. CFG631 D(K9) +0.928/+0.850 ± 0.33/0.30 reported only.
- **Rule (per footing, per statistic; primary decides):**
  - CONSISTENT iff prediction > 0 and |pred − meas| ≤ 2σ;
  - FAILS iff prediction < −0.1σ (wrong sign) or |pred − meas| > 3σ;
  - TENSION otherwise (this includes a near-zero prediction lying 2–3σ below the measurement).
  - Mechanism label (independent of the class): A5 ACCOUNTS FOR the signal if pred ≥ meas/2; DOES NOT ACCOUNT if pred < meas/4.
  - The lane verdict is stated per footing; if the footings differ both are reported, never averaged.
- **Ceiling reading (R3):** if even R3's increment over the equal-source baseline is below meas − 2σ on a footing, record
  "A5 CANNOT PRODUCE the signal on that footing by any condensed-fraction allocation within the record's cold gas and census".

## 4. MUTATE (CFG651_MUTATE=1 writes *_MUTATE outputs)
- **M1 all-baryon source (candidate B / S-all):** source = census-retained baryons, independent of phase ⇒ the condensed
  re-allocation leaves the source unchanged: A_pred,S-all − A_base and D_pred,S-all must be 0 to 1e-6 (the age term comes
  only from A5). A_base = the equal-source law A (composition only) is reported.
- **M2 shuffled ages:** 200 within-mass-bin label shuffles (CFG700's `tertiles(rng)`, seed 651), R2 increment via the
  linearised per-group derivative table: |mean| < sd/3 required, and the real-label increment's rank reported.
- **M3 linearity:** linear (derivative table, Δf = ±0.05) vs exact R2 increment agree within 10% (or 1e-4 absolute).

## 5. Controls
C1 CFG700 measured A(K9) reproduced to 1e-4; C2 CFG585 D(A, canonical, K9) +0.9411 reproduced to 1e-3; C3 SFR coverage in
f30 early ≥ 98%; C4 OLD/YOUNG median log M* within 0.02 dex. Resource: one process, nice 10, ≤ 1.5 GB; no downloads.

## 6. What a result means
A FAIL or "does not account" says A5 (with the census and the on-disk proxy) gives no age term of the observed sign/size;
the age signal then stays unexplained by THEORY v2 (open problem 4), and the LePhare-mass-bias nuisance (CFG700) stays open.
A CONSISTENT result would be a post-hoc mechanism, not a confirmation.
