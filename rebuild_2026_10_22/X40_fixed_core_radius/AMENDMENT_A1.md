# X40 AMENDMENT A1 (POST-RESULT, check code only)

RUN1 (`_RUN1` files, kept) failed K1's fixed-r_c normalisation check. The check interpolated M_h at r_ta between grid
points (RM does not contain r_ta) and compared that with the fair share at 1e-10. The halo function itself is exact at r_ta
by construction, and it is constant beyond r_ta. The check now evaluates the normalisation at r_ta exactly and at the grid
end. Model, calibration and every graded number are unchanged; the rerun reproduces RUN1's grades. The duplicated "K0"
label is the X38 machinery's K0 (EM1 + X30 bands) plus this lane's K0 (X38 SD reproduced); both are reported.
