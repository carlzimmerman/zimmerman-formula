# LAM1_spin_lens_split: STOPPED AT STAGE 0, NOT EVALUABLE. The rebuilt B21 isolation keeps 554,316 lenses against B21's 259,383 (+114 %), outside K0's 15 %. Even if it had matched, the spectroscopic red sample can detect only a gap of 4 or more in A

Criteria: `FROZEN_CRITERIA.md` (5ed7fac28a), alone first, **not blind**. Amendments A1-A7 in `AMENDMENTS.md` (aea5d1532e, d8c3fbcf2e) were written before any count. Files: `STAGE0.md`, `lam1_stage0.py`, `lam1_stage0.out`, `lam1_stage0.json`. Idea from arXiv 2610.40789, not its network. kappa = 1/2 FITTED. Footings never pooled. Not theory closed. Nothing here says the data favour the framework. Reinstates nothing.

| gate | result | frozen outcome |
|---|---|---|
| F1 training | DynPop Qual >= 1: 6063, of which 5811 have an SDSS fibre spectrum within 1"; 514 slow | PASS; DynPop kept (> 3000) |
| K0 isolation rebuild | 554,316 isolated (comoving sphere), +1.137 vs 259,383; physical sphere 422,562, +0.629 | **FAIL: F2 NOT EVALUABLE, lane stops** |
| F2 power, canonical | sigma(dA) 1.400 (sys 0.136) vs dA_rot/3 = 2.291 | not evaluable; power alone passes |
| F2 power, alt | sigma(dA) 1.277 (sys 0.125) vs dA_rot/3 = 1.643 | not evaluable; power alone passes |

Application sample: 10,570 red isolated lenses with an SDSS DR17 spectrum (KiDS-N only; spec-z median 0.30). PROXY f_slow 0.066 (Sersic masses), 0.104 as a row (Petrosian masses). Wave 2 (the 17.7 GB shear catalogue) is not needed and was not fetched.

## Reading
- **The stop is the reconstruction, not the physics.** My version of B21's sphere is twice as permissive as theirs. Plausible causes, none tested: B21's distance convention (flat Lambda-CDM; physical or comoving not stated), satellites drawn from a catalogue other than the masked bright sample, the flux-scale step that needs GAaP r (absent from the public files), or edge handling. Tuning the rule until it hits 259,383 would be fitting to the target, so it is not done here.
- **The power result says more.** F2's power line passes only because H-rot is extreme: all of the 0.45 excess sitting in 6.6 % of red lenses gives dA_rot = 6.8, so A_slow would be about 7.8. KINEMATIC needs dA >= 4.2 canonical or 3.8 alt to clear 3 sigma. Any realistic split, such as slow rotators carrying twice the fast excess, is about 0.5-1 in dA and sits inside 1 sigma. With 694 slow lenses, this sample cannot answer the question CFG849 posed, even with a perfect isolation match.
- **What would.** A shear stack over the photo-z sample with the estimator applied photometrically. E3 would reject that, because without spectra the estimator is photometry. Or about 10x more spectroscopic red lenses, from DESI BGS over KiDS. Neither is in reach here.
- **F1 is a real asset.** 5811 MaNGA galaxies have both a stellar lambda_Re and an SDSS fibre spectrum, including 514 slow rotators. That is enough to test the paper's core idea on stellar absorption lines (stage 1, E1-E3) without any lensing. That test would be a new lane with its own criteria, not this one.
