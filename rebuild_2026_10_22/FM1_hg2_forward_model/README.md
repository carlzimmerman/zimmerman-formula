# FM1_hg2_forward_model: HG2's negative sign is a conditioning artefact; the statistic cannot see a hot-gas excess

Criteria: `FROZEN_CRITERIA.md` (9c9d980ba0, committed alone, before any script or number); no amendment.
Machinery: GA1's committed script, executed read-only.

κ = ½ FITTED. Not "theory closed". Nothing here says the data favour the framework.

## Verdict (frozen): **CONDITIONING EXPLAINS THE SIGN** (canonical and alt)

**Method.** The base picture is observed the way HG2 observes data:
- model pulls are g_pred × lognormal scatter;
- the scatter s_int is data-driven: 0.356 dex canonical, 0.368 alt, from 1.4826 × MAD of the residuals; the FAINT arm
  alone gives 0.365, so the scatter is not set by the bright arm;
- σ is inverted from HG2's estimator;
- the groups are binned on that σ;
- the statistic is D_stat, over 2000 realisations.

| variant | D_mod median [95 %] canonical | q(D_mod ≤ D_meas = −0.362) | class |
|---|---|---|---|
| **PRIMARY s_int 0.356** | **−0.492 [−0.656, −0.316]** | **0.934** | **EXPLAINS** |
| FAINT-only s 0.365 | −0.500 [−0.657, −0.327] | 0.945 | EXPLAINS |
| 0.5 s_int | −0.217 [−0.494, +0.057] | 0.129 | EXPLAINS |
| 1.5 s_int | −0.599 [−0.727, −0.452] | 0.998 | PARTLY |

- Alt: PRIMARY −0.523, q 0.967, EXPLAINS.
- **Check K1:** binning on the *observed* σ with no scatter reproduces HO1/GA1's D_pred (+0.3059 / +0.2821) exactly.

The old positive "prediction" came from mixing a model pull with a binning on the observed pull.

## Verified as hard as a failure (post-result diagnostic, labelled, NOT graded)

`fm1_post_plant_diagnostic.py` / `.out` / `.json` plant an extra pull in the BRIGHT arm of the model:

| planted BRIGHT excess | D_mod median [95 %] (canonical) | q | measured D |
|---|---|---|---|
| 0.0 dex | −0.492 [−0.656, −0.316] | 0.934 | consistent |
| +0.2 dex | −0.452 [−0.655, −0.217] | 0.793 | consistent |
| +0.4 dex | −0.417 [−0.708, −0.092] | 0.649 | consistent |
| −0.2 dex | −0.537 [−0.675, −0.393] | 0.988 | excluded |

The alt footing gives the same pattern.

**So HG2's statistic, read through a forward model, is nearly blind to a hot-gas excess.**
- A +0.4 dex excess in the X-ray-bright groups still yields a negative D consistent with the data.
- The measured sign therefore **neither refutes the base picture nor supports a hot-atmosphere selector**: it is
  NOT DIAGNOSTIC of the mechanism.
- It mildly disfavours a *deficit* in the bright groups (−0.2 dex is excluded).

## Consequence for the record

**HG2's "wrong sign" (HO1(b), GT1, DS1, GA1, DY1, AP1) is withdrawn as a failure of the theory.** It was a comparison
of an un-forward-modelled prediction with a statistic that conditions on the observed pull.

The group sign is reclassified from "open tension" to **not diagnostic as measured**. A diagnostic version would bin on
a pull-independent quantity: X-ray temperature, stellar mass, or richness.

## Checks: 4/4

- **K0:** GA1's D reproduced.
- **K1:** HO1/GA1's D_pred reproduced exactly with observed binning.
- **K2:** s_int > 0, and the realisations are seeded.
- **K3:** peak RSS 0.67 GB.
- **Rerun:** byte-identical.
- **MUTATE twin** (s_int = 0):
  - It exits 1, but by a crash, not by K2 (disclosed). With zero scatter the model σ of the two arms never share a bin,
    so every D_mod is undefined and the percentile call fails.
  - The same fact shows as the "noise-free model-binned D = nan" line in the graded run. Without scatter, the arms do
    not overlap in σ at all: **the overlap HG2 bins on is created by scatter.**
