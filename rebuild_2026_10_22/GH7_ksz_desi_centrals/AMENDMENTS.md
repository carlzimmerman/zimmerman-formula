# GH7 amendments (committed after the power gate and before T̂ is computed)

1. **The frozen mock's R looks too high.** The measured P(k) at k ≲ 0.02 h/Mpc is inflated (2.7e5 at k = 0.002 and 1.6e5 at
   k = 0.011, in (Mpc/h)³), most likely survey-window and n(z) leakage. This gives the mock rms v_true 418 km/s and R = 1.263.
   The frozen class stays computed at R = 1.263. Every amplitude and class is **also** reported at the context value
   R = 0.724 (r 0.64 from arXiv:2604.19745, σ_v 300 km/s, data rms v_rec 265 km/s). A class that differs between the two is
   labelled **R-LIMITED**, which is not a result.
2. **Gate.** Frozen R: G1 S 10.26, G2 S 4.89, both pass. Context R: G1 S 5.88 passes, G2 S 2.80 fails. **Extent is claimed only if
   the extent class is the same at both R values.**
3. **K5's frozen text is wrong.** The injection that gives A = 1 is −τ T R v_rec/c, not v_rec/R. The corrected form is used.
4. **p values.** 200 shuffles cannot reach p < 0.003. 200 set the covariance as frozen; 2000 more set σ(A) and p.
5. **Memory.** `gh7_vel.py` peaked at 4.3 GB, above the frozen 3 GB.

6. **Positive control, added after T̂ and before any README (the result was A(1.8) ≪ 1 at both R).** A shortfall this large is as likely a broken
   pipeline as absent gas. The same pipeline stacks all BGS galaxies above log M★ 10.5, 11 and 11.25 (no central cut, z 0.1–0.5), where
   arXiv:2604.19745 reports kSZ detections on DESI DR2 × ACT DR6. **Rule: if the best of these three matched-filter A/σ is below 4, the BELOW class is
   VOID (pipeline not validated). Only if at least one reaches 4 does the MW-mass shortfall stand.** The filter uses the k = 1.8 shape.
