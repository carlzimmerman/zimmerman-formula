# Same-target precision correction, before corrected-challenge numbers

The frozen challenge is the sole L satisfying the **actual X43 canonical background-A** core crossover at logM12.3. The first numeric implementation supplied by the independent bounds calculation used displayed a0=9.3603e-11 and yielded L=2.5090595510216196. Actual X43 imports FP0 a0=9.360324825027975e-11. Therefore the same target requires

L_actual = 2.5090595510216196 * (9.360324825027975e-11 / 9.3603e-11)^(4/5)
         = 2.5090648745652686.

At the old value U(12.3)/actualfloor=.99999734784546. The relative error in L was2.12ppm. Run006 is retained as implementation precision-error history, not the authoritative frozen-target challenge. Root and bounds agent independently confirmed the correction and root explicitly required the rerun before its results. Run007 uses the corrected value, full17digit tag, identical single-L model, zero new fitted numbers and no threshold scan. This amendment does not modify prior pinned criteria or artifacts.
