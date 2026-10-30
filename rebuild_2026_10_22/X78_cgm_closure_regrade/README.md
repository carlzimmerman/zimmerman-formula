# X78_cgm_closure_regrade

> **Superseded in part by GH1_matched_lensing_satellites (10-29).** KiDS lensing around these *same* G09 hosts wants Δ = +0.17 [+0.05, +0.28], not +0.78. The satellite number is a method systematic of this measurement (likely pair weighting toward rich hosts, interlopers, velocity bias), not a halo-mass need. Satellite-based needs/fails in this lane are overstated; the lensing lines stand.

> **Lane-ID collision.** A peer session's `X78_footing_upsilon_floor` holds the X78 id. This lane (04848505f2) is
> different. Cite it by its full name, `X78_cgm_closure_regrade`.

**Question.** A full regrade, with the gas gravitating, of the CGM route from X77_cgm_budget.
- **Halos:** route E fair-share halos (smooth core, self-consistent r_ta).
- **Gas:** Zhang+24's measured hot CGM (β 0.43, M_hot(<R_vir) = 1.84 M★), cut at **their own closure radius,
  3 R_vir**. The cut is not tuned here.
- **Law:** given the same baryons.
- **Data:** KiDS lensing (X53 harness) and GAMA satellites (X75 frozen measurement), bins 3–4 (log M★ 10.6–11.0).
- Criteria were frozen first (04848505f2).

## Verdict: CGM-CLOSURE HALOS FAIL on satellites, both footings

| canonical (alt similar) | route E + CGM to 3 R_vir | law + same CGM |
|---|---|---|
| lensing χ², bins 3–4 (30 pts, block-diagonal, 2h) | **140.6** | 757.8 |
| lensing Δ(H2H − L2H), bins 3–4 | **−617** (HALOS) | — |
| σ_sat bins 3–4, km/s (measured 151 ± 9, 188 ± 9) | 115, 138 | 167, 196 |
| satellites χ², bins 3–4 | **44.4 ✗** | 3.7 |

**Edges and cuts (reported):**

| | lensing H2H b3–4 | lensing L2H b3–4 | sat χ² H | sat χ² L |
|---|---|---|---|---|
| central, cut 2 R_vir | 203 | 298 | 110 | 0.6 |
| **central, cut 3 R_vir** | **141** | 758 | **44** | 3.7 |
| central, cut 5 R_vir | 676 | 1914 | 0.2 | 13.5 |
| generous (f_b + 1σ, β − 1σ), 3 R_vir | 560 | 2325 | 0.4 | 39 |
| tight (f_b − 1σ, β + 1σ), 3 R_vir | 447 | 99 | 224 | 23 |
| *X53 baseline: F2 baryons (0.5 M★ hot), SPARC halos, bins 3–4* | *385* | *95* | | |

## What it shows

1. **With Zhang's CGM cut at their closure radius, route E's lensing improves sharply.**
   - Bins 3–4 χ² is 141, against 385 for SPARC halos in X53.
   - It beats the law given the same gas by 617.
   - It still trails the law with F2's small hot gas (95 in X53), and 141 on 30 points is not a good fit.
2. **The same halos under-predict satellites by about 20 %** (χ² 44). Satellites need the gas out to ~5 R_vir, and
   then lensing is badly overshot (676).
3. **The law has the mirror-image problem.**
   - With F2's small hot gas it fits lensing (X53) but under-predicts satellites (X75).
   - With Zhang's CGM it fits satellites (χ² 0.6–3.7) but overshoots lensing (299–758).
4. **So no single baryon budget fits both probes, in either model.** Lensing (KiDS, isolated lenses) and satellites
   (GAMA, centrals including group centrals) want masses about 0.3–0.4 dex apart at the same M★, whatever the gravity
   model.
   - That points to a sample or systematic difference between the probes, not to the model.
   - X75 A1 already found that poor-group hosts lower the satellite need by ~0.15 dex.
   - **A matched sample is needed before either probe can be used to set or exclude a galaxy mass rule:** B21-style
     isolated hosts with spectroscopic satellites, or KiDS lensing of GAMA centrals.
5. **A caution for the law reading.** If galaxies really hold Zhang-level hot gas out to ~3 R_vir, the isolated law
   overshoots KiDS lensing by Δχ² of hundreds. The law's lensing pass assumes little CGM beyond 100 kpc.

κ = ½ FITTED; c_f EXTERNAL; footings never pooled; cold dark energy is a gravitating field component, never a particle;
not theory closed; nothing here says the data favour the framework.

## Checks (4/4)

- **K1:** the reimplemented fair-share lensing reproduces X76's H2H χ² (−1e-16).
- **K2:** the law stack reproduces X53's L2H (6e-12).
- **K3:** the CGM normalisation at R_vir is exact.
- **MUTATE:** a cut at 1 R_vir lowers σ_sat(H) in bins 3–4 (67/80 vs 115/138).
- **Disclosed fix:** the first run reported "FOOTINGS DISAGREE" because it compared verdict strings that contained the
  χ² values. It now compares the class and the failing line. Both footings fail the same line (satellites); no number
  changed.
- Runtime ~2.5 min, one thread.

## Files

- `FROZEN_CRITERIA.md`
- `x78_regrade.py` with `x78_regrade.out` and `x78_regrade_results.json`

Run:

    PYTHONHASHSEED=0 OMP_NUM_THREADS=1 nice -n 15 python3 x78_regrade.py
