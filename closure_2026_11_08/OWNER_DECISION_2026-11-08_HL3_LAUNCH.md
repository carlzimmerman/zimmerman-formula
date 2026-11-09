# Owner decision 2026-11-08: lane HL3 (lensing-leg shape of the cluster residual) launched, downloads approved

Given in the orchestrator session ("Theory completion") on 2026-11-08 after XF1 was launched. The orchestrator's synthesis
had read the hot-leg no-go as resting on hydrostatic masses, with the inner-bin shape never checked on a lensing-only mass
profile. Owner's words (verbatim) to the question "May the HL3 lane download the public X-COP, CLASH and LoCuSS cluster
profiles?": "Yes, download them".

Correction recorded here: the synthesis' statement that the X-COP per-cluster profiles were never downloaded and the
inner-bin shape was audited only as a class mean was WRONG. The 12 X-COP per-cluster hydrostatic, gas and stellar profiles
are on disk (`real_research/data/xcop/`) and NA2 (d) graded the shape per r/R500 bin as a cluster median. The CLASH lensing
RAR points (Tian+2020, 84 points, 20 clusters, 14.3-600 kpc) are also on disk. What the record lacks is the per-bin
residual on the LENSING leg set beside the hydrostatic leg; HL3 grades that, and the downloads extend the lensing leg
from 600 kpc to R500 (Umetsu+2016 profiles, Donahue+2014 gas), with LoCuSS as a conditional second sample.

Scope
- Lane HL3 only; a grading lane of the adopted law, not a mechanism lane. It adopts nothing; the owner adopts.
- Downloads: data files only, under `_external_data/hl3/`, untracked, logged with sha256 in the lane's FETCH_LOG.md,
  no absolute home paths, nothing downloaded is executed, under 200 MB.
- Criteria frozen and pushed alone first: closure_2026_11_08/HL3_lensing_leg_shape/FROZEN_CRITERIA.md (ef4595f390).
- Folds into PAPER70 v1.9 (or the next version). Both footings separately. kappa = 1/2 FITTED.
