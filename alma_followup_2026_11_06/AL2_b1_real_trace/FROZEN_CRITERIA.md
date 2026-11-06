# AL2: trace the row-B I0 collapse on the real spw25 cutout. FROZEN CRITERIA, before the stream, any script or number

Follows AL1 (cb2a36ca23): I0 = 0 is an absorbing state of cfg942 lm_fit; the -172 km/s start offset alone did not reproduce it on smooth MOCKs.
Committed alone, with the owner's approval file, before the cube is streamed. Diagnosis only: **no V_c from any modified fit is computed or
printed**, nothing is scored, no scorecard row, prediction or frozen file changes. κ = ½ FITTED; one disc excludes no model; not theory closed.

## Steps (`al2_trace.py`; outputs `al2_trace.out/.json`)
- **R0 (identity)** cutout sha256 begins 61f147499c28123e (the release cutout). If not, STOP: report and do nothing else.
- **R1 (reproduce)** the frozen `ac1_score.measure()` (G1-3D, no injection) on the cutout gives both fits with I0 = 0 and params equal to
  `ac1_score_RELEASE.json` to 1e-6 relative. If not, report NOT REPRODUCED and continue with R2-R4 as information.
- **R2 (trace)** in this process only, wrap `C.lm_fit` to log every accepted step (iteration, cost, all 9 parameters, lam) for each of the six
  trial fits. Report the first step at which I0 = 0, the cost just before and after it, the start cost and the zero-model cost sum (D/sigma)^2.
- **R3 (start decomposition)** for the frozen start p0 of each branch: cost(p0), cost(zero model), and the cost with one start component
  replaced at a time by a data-derived value (I0 from the 3D-mask flux through the injection formula F bp / sum exp; vsys from the 3D centroid;
  PA from the moment-1 gradient as frozen; h, rt, s0 unchanged). Costs only; no fit is run from a changed start.
- **R4 (data facts)** inside the fit cylinder (r <= 1", |v| <= 600): continuum residual (median over line-free channels, in sigma); lag-1
  channel autocorrelation of off-source spectra; ratio of the frozen I0 start to the flux-implied I0; fraction of fit voxels with |D| > 4 sigma
  outside the 3D mask.
- **Trigger call:** named only if R2 shows the collapsing step and R3 shows which start component makes cost(p0) exceed cost(zero model)
  (or the step's clip), with the others changing it by less than that one. Otherwise TRIGGER UNRESOLVED.
- **MUTATE (`AL2_MUTATE=1`)** R1 with a synthetic 2x scaling of the cube's data (cost function check: zero-model cost must scale x4, and the
  trace must change). Bites iff the zero-model cost ratio is 4 to 1e-6.

## After
- Cutout deleted after the outputs are written. Any repair stays a proposal for an owner-filed scorer addendum.
