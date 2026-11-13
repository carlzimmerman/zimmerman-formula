# EUC12 (COMMON STELLAR-MASS SCALE, EUCLID vs SLACS): RESULT

2026-11-12. FROZEN_CRITERIA bdaf5dcd26 (alone) → scripts and runs 339a88bf39 → this file. TEST lane. κ = ½ FITTED;
not theory closed. No outcome here is a pass of the theory. No amendment was made.

## Verdict

**Construction A (DESI DR1 CIGALE), primary class θ_E < 1.3″: NO VERDICT / NO VERDICT** (canonical / alt).
Δb_common = **−0.087 [−0.241, +0.122] / −0.084 [−0.240, +0.123]**. Also NO VERDICT for all of P and for θ_E ≥ 1.3″,
on both footings, and under construction B (Legacy Surveys W1 and z). No word is SAME STARS: the 95 % intervals are
about ±0.18 dex wide, so the ±0.10 band cannot hold them at this N. No word is EUCLID NEEDS MORE: every central
value is at or below zero.

Plainly: on one mass scale and one dispersion fitter, Euclid's typical lens galaxies do not need measurably more
stars than SLACS's. The central values say they need the same or slightly less, but the data cannot tell the
difference from ±0.15 dex.

## What the two mass catalogues do

The suspected scale difference between the catalogues is not there. Against CIGALE (Chabrier, so both δ carry the
≈ 0.24 dex IMF constant):
- δ_E (ECLIPSE Salpeter, spec-z rescaled) θ_E < 1.3″: **+0.235 [+0.176, +0.352]** (N 22); all P +0.222
  [+0.167, +0.297] (N 33; +0.245 without the spec-z rescaling); θ_E ≥ 1.3″ +0.167 [+0.065, +0.313] (N 11).
- δ_S (Auger Salpeter): **+0.258 [+0.214, +0.296]** (N 27); restricted to the lenses with own-fitter σ +0.284 (N 11).
- δ_E − δ_S: **−0.023 [−0.097, +0.113]** (θ_E < 1.3″), −0.036 [−0.108, +0.050] (all P), −0.091 [−0.198, +0.055] (≥ 1.3″).
- Construction B (one E-MILES W1 recipe for both): δ_E − δ_S −0.049 [−0.108, +0.020] (θ_E < 1.3″), −0.077
  (all P); z band −0.007 and −0.020.
Both constructions agree that ECLIPSE (Prospector) and Auger 2009 sit on the same scale to within about 0.05 dex.

## Where the gap went: the dispersion scale

b_dyn, law S, β = 0 (canonical / alt):
- Euclid P, EUC5R DESI fits: θ_E < 1.3″ **+0.129 / +0.127** (N 23); all P +0.202 / +0.197 (N 35); ≥ 1.3″ +0.259 / +0.253 (N 12).
- SLACS, EUC5R's own fitter on SDSS spectra at DESI noise: **+0.193 / +0.187** (N 28); as observed +0.193 / +0.188.
- SLACS, published σ, same 28: +0.162 / +0.154; all 79 with Salpeter mass: +0.152 / +0.146.

So the earlier Euclid-over-SLACS gap came from the SLACS side. Read with the same fitter, SLACS lenses need about
+0.19 on these conventions, not +0.08. On the catalogue scales, the typical Euclid class is already about 0.06 dex
below SLACS.

Contradiction with the brief: I cannot reproduce "SLACS dynamics about +0.085". EUC5R's own machinery, with Auger's
Salpeter masses, Re(V), n = 4, a 1.5″ fibre and 1.5″ seeing, gives +0.15 from the published σ. My per-lens b agrees
with EUC5R's K-sanity ratios (b ≈ −2 log ratio + 0.01, correlation 0.999), so the difference lies in conventions:
probably the +0.085 used a different mass normalisation (the A55/A85 Fs × Mass route?). That is unverified, and it
is the thing to check before anyone quotes the SLACS dynamical number again.

## Brackets and variants (Δb_common, θ_E < 1.3″, construction A, canonical / alt)

- SLACS σ as observed −0.087 / −0.084 (word unchanged); published σ −0.055 / −0.050 [≈ −0.21, +0.17].
- Euclid seeing 0.9 / 1.3″: −0.093 / −0.080 (canonical); SLACS seeing 1.2 / 1.8″: −0.086 / −0.090.
- Construction B W1: −0.114 [−0.271, +0.070] / −0.110 [−0.271, +0.072]; B z: −0.072 / −0.068 [−0.23, +0.13].
- Per-lens form, median(b + δ) on lenses that have both: E +0.411 (N 22), S +0.374 (N 11), difference
  **+0.037 / +0.039**. The decomposed and per-lens forms differ by about 0.12 dex. That spread comes from which
  subsets enter and from medians of sums. Both are inside NO VERDICT; neither form is robust enough to pick a side.
- Newton twin (both sides, a₀ → 0): −0.096. The statistic barely depends on the law, as expected, because both
  samples sit at similar accelerations.

## Reading, not a gate: EUC10 Part B on the common scale

Lensing at catalogued source redshifts, Euclid minus SLACS (canonical / alt), moved by δ_E(P) +0.222 and δ_S +0.258:
- AGEL DR2: from +0.156 / +0.150 to **+0.120 / +0.114**.
- DESI SLF IV: from +0.216 / +0.212 to **+0.180 / +0.176**.
The common scale removes only about 0.04 dex. The lensing population gap stays. The dynamics gap does not show up on
the same fitter. Those two statements pull against each other, and this lane does not resolve them.

## Samples

Euclid matched (A) 33 of 35 P lenses (by TARGETID): median z 0.428 against 0.428, log M★ 11.548 against 11.575,
θ_E 1.082″ against 1.098″. The matched set is P to within noise. SLACS: 28 of 79 Auger lenses with Salpeter mass are in
DESI DR1 (27 with LOGM), 11 of them also among the own-fitter 28. B: all 35 P and 71 of 79 SLACS have a Tractor
object within 1.5″. CIGALE CHI2 median 2.1 (Euclid) and 2.3 (SLACS); LOGM_ERR median 0.09. The spec-z rescaling moves
ECLIPSE masses by a median −0.014 dex (range −0.215 to +0.389).

## Known answers and mutation (all pass)

K1 Chabrier − Salpeter δ_S −0.240 (target −0.25 ± 0.02); K2 shifted positions 0 of 79; K3 Euclid Z identical, SLACS
median |ΔZ| 0.0003, Euclid positions all within 0.24″; K4 J3 0.9659 (N 72); K5 P medians +0.2018 / +0.1972, per-lens
within 1.4e-5 dex; K6 cancellation 0.00000; K7 E-MILES M/L_V 3.822 against table 3.865. Mutation twin (shift +0.20 on
the Euclid common masses): Δ moves by −0.200 on both footings and exits 1.

## Caveats

- The samples sit at different redshifts (Euclid ≈ 0.43, SLACS ≈ 0.2), so any redshift-dependent bias of CIGALE or of
  the B recipe does not cancel. B's bands are top-hat approximations with a single-burst age clock.
- Arc light is in the photometry on both sides.
- The SLACS model (n = 4, Re(V)) and the Euclid model (catalogue Sérsic) are measured differently.
- Legacy Surveys photometry was fetched from the Data Lab TAP (114 cones, manifest under
  `_external_data/euc12_common_mass_scale/`). The licence line in the manifest is PROVISIONAL.
- Favourable or not, these readings await an independent re-grade.

## Files

`FROZEN_CRITERIA.md`; `euc12_common.py`; `euc12_cigale.py` (one chunked pass; `euc12_cigale_rows.csv`, `.out`);
`euc12_fetch_ls.py` (`.out`); `euc12.py` (`euc12.out`, `euc12_results.json`, `euc12_euclid.csv`, `euc12_slacs.csv`;
`*_MUTATE_shift.*`, exit 1).
