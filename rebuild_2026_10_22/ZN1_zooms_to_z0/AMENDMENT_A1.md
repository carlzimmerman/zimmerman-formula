# ZN1 AMENDMENT A1 (committed alone, before any ZN1 snapshot has been analysed; the runs are unaffected)

Two changes to the grade. Both come from checks run on 10-31 on other rules, in `../NZ1_zoom_core_radius/`. No ZN1 number exists.

1. **All 15 shear keys read their measured value on the run's own C\* template.** G-OUT-Mall and G-OUT-M1..M3 have been reading X7's fixed A_CAL and s_CAL, computed on an older template, while their predictions and the other 11 keys' measured values use the current one. Here A comes from the run's `M_all|OUTER` and `M_terc|OUTER`, and s_CAL is scaled by the same ratio. See `../NZ1_zoom_core_radius/nz1_one_template.out`.

2. **Gas scale.** X-COP's gate uses X-COP's gas. One rule shouldn't use two gas scales for the same physical quantity. So the shear keys are graded with eRASS1's Mgas500 raised by SM1's matched +0.111 dex, **and** on eRASS1's own gas. The verdict classes in `FROZEN_CRITERIA.md` are read on X-COP's scale. **[GAS-SCALE-DEPENDENT]** is appended if eRASS1's own gas gives a different class. SM1's offset comes from five massive clusters, none in the lensing sample, so its application across the lensing sample's mass range is an extrapolation, disclosed.

Everything else in `FROZEN_CRITERIA.md` stands. K3 (the harness reproduces MA1's predictions) is unaffected, since it compares predictions.

κ = ½ FITTED. Not theory closed.
