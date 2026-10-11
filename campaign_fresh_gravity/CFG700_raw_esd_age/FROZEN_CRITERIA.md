# CFG700 FROZEN CRITERIA — the early-type age signal on RAW lensing only

(owner chat, after the owner's 10-10 rule "raw data vs framework-native only"). Committed alone before any number.

Why: CFG585–589 scored ε against CFG529's environment term, which is ΛCDM-built (halofit two-halo, HOD satellites,
Moster/Behroozi SHMR) — an inherited ingredient under the 10-10 rule. This lane re-tests the core claim with no model.

Claim: at identical stellar mass, older (redder) early types carry MORE lensing signal than younger ones. A law that
computes gravity from the present baryons alone predicts no difference (same M*, same stellar-mass-based gas estimate).

Sample: CFG589's mass-stratified f30 early-type tertiles (colour residual thirds inside each of ten log M* bins; built by
executing cfg585_age.py's head unedited, exactly as CFG589). OLD = top tertile, YOUNG = bottom tertile.

Statistic (model-free): raw ESD(R) of each group from `esd_loo` (per-lens pair sums WG/WW, 15 bins; no comps, no
environment, no law, no κ, no footing). Amplitude
  A_b = log10( Σ_k w_k ESD_old,k / Σ_k w_k ESD_young,k ),  w_k = 1/σ_k² of the ALL-f30-early raw ESD (jackknife diagonal),
over band b ∈ {K9 (bins 6–14, PRIMARY), K-in (12–14), K-mid (9–11), K-out (6–8)}.
Errors: 50-patch jackknife of A_b (joint LOO of both groups). PRIMARY significance = empirical Z: A_b divided by the
standard deviation of A_b over 200 random OLD/YOUNG relabellings within the ten mass bins (seed 700).
Verdict (K9): AGE SIGNAL ON RAW DATA iff A > 0 and empirical Z ≥ 2; NONE iff |Z| < 1; else WEAK.
Report-only: A in K-in/K-mid/K-out (ACE P2 radial shape), jackknife Z, and the ratio of empirical to jackknife σ.

Controls: C1 OLD/YOUNG median log M* agree within 0.02 dex; C2 median lens z reported, agree within 0.02 (else the
verdict is flagged: Σ_crit weighting differs); C3 OLD+MID+YOUNG pair sums reproduce the all-early raw ESD to 1e-10
(estimator closure); C4 the null distribution's mean |A| < its σ/3 (no relabelling bias).
MUTATE (CFG700_MUTATE=1): the OLD group's pair sums WG × 0.8 → A must drop by log10(0.8) = −0.0969 to 1e-6 (linearity).

No law, footing or κ enters. Interpretation (what it means for the framework) is separate from the verdict.
