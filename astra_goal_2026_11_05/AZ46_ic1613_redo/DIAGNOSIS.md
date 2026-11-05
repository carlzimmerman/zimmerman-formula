# Preliminary diagnosis complete; new cube test not yet frozen

Kappa=1/2 FITTED; not theory closed. This is the investigation required
before lane12's new criteria, under diagnostic-plan commit e282c8c2dc.
It does not amend FN4a or change its recorded failures.

The independent map/ring calculation reproduces the two old numbers:
HI mass3.034577678e7Msun with the old Gaussian-area rounding, and drift-
corrected velocity20.849205635km/s. Raw FITS decoding matches an independent
astropy section exactly, and32/64-row sums agree within the predeclared
1e-10 relative line. The two old ring-velocity comparisons agree exactly.
All4 computational checks now pass. Runtime0.23s; peak RSS189MB.

## Flux: weighting and benchmark provenance matter

The local primary-beam-corrected natural-weighted moment map integrates
to262.8614461Jy km/s under the original1.1331 beam-area convention. Its
HISTORY explicitly records PBCOR; adding another primary-beam correction
to this map would double-correct it. Using the exact Gaussian area gives
262.8637577Jy km/s: an8.8e-6 fractional effect. Keeping signed rather
than positive-only pixels changes the mass by only0.0154%. These effects
cannot explain a28.4% deficit relative to the Oh gas-table conversion.

The natural beam is13.19112x10.98504arcsec, while the robust cube uses
7.69068x6.47604arcsec. Each must use its own beam. The original engine
hardcodes the natural beam, so its unexecuted robust option would need
an explicit beam correction before being used as a new resolution test.

Hunter2012 Table4 quotes robust-weighted log(MHI)=7.53. The local natural
map mass is10.44% below that value. Their sectionIV.1 reports an11% mean
absolute natural/robust mass difference across the sample, often with
robust higher. That makes weighting a plausible contribution, not an
object-specific uncertainty or proof that IC1613 agrees. Do not convert
this population average into a new acceptance tolerance. The robust
moment map is listed publicly but is not among the local files.
[Source](https://arxiv.org/html/1208.5834)

Oh2015 Table2 instead gives Mgas5.93e7Msun; sectionIII.2 scales HI
profiles by1.4 for helium/metals. Its implied HI mass is4.235714e7Msun.
The table-to-map gap is therefore reproduced, but its full origin is
NOT IDENTIFIED. A near-factor1.4 coincidence is not evidence of helium
double counting. Recovering the exact published radial profile and
integration/calibration provenance remains necessary.
[Source](https://arxiv.org/html/1502.01281)

## Drift: different derivative and velocity-field estimators

The saved mask and original moment maps give Vrot16.096784010km/s at
Rmax798.539464arcsec. The old sm3/finite-difference derivative raises
this to20.849205635. Applying the analytical Eq4 shape from Oh2015 to
the SAME q=Sigma*sigma^2 profile, fitted in log q within Rmax, instead
gives18.880258635km/s. This fit choice was stated before executing it;
it is not the paper's unreleased numerical fit. Its log-q RMS residual
is0.592, and two fixed initializations converge to the same objective.

Thus smoothing the derivative materially changes the result, but does
not reproduce16.9. Oh's principal rotation curves use bulk velocity
fields, whereas this pipeline fits the intensity-weighted moment1 map.
The absence of that bulk field and numerical profile leaves a substantive
comparison gap. The new18.88 value is an exploratory diagnostic, not a
new PASS based on proximity to the old2km/s threshold.
[Source, sectionsIII.1.1–III.1.2](https://arxiv.org/html/1502.01281)

## Preserved failed check and reproduction

The first diagnostic script accidentally required bitwise equality for
chunk sums rather than the plan's1e-10 relative tolerance. The positive
sum differed by3.7e-9 on a1.918e7 total, about2e-16 relative. That initial
failure is preserved in diagnosis_first_check_failure.json. The check
was corrected to the already stated line; no physical result changed.

Run with the existing Python environment providing numpy/scipy/astropy:

    python astra_goal_2026_11_05/AZ46_ic1613_redo/diagnose.py

diagnosis.json contains profiles, fit parameters, beam/HISTORY evidence,
checks and input hashes. This preliminary step uses the old saved mask,
explicitly hashed; the new cube test still requires its own independently
prepared masks, correct natural/robust beams, known answers, mutations,
both footings and numerical resolution pairs. No new lane12 physical
verdict has been issued, and no missing product was downloaded.
