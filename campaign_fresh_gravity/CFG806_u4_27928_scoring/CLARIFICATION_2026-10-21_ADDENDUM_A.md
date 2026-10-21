# CFG806 clarification, addendum A (2026-10-21; before any U4_27928 data; nothing frozen edited)

**MUTATE continuum.** The same reading as CFG809 addendum A §2 applies here. In MUTATE, the continuum for the shifted window
excludes channels within ±600 km/s of the true z = 1.4193, because those channels are not line-free.

CFG942 checked this on MOCK U4-a before applying it (90bdb0153). In the shifted window, the 2R_e circle reads −16.0σ with the
true-line channels in the continuum, and −1.8σ without them. So the old reading over-subtracted and made the control easier to
pass.

**MUTATE decision.** It is G1's selection-aware S/N (A-U13). That value reads −0.3 on MOCK, so G1 fails and the control bites.
The literal S/N (8.6 on pure noise) is printed and never decides. If a selection-aware null shows the same continuum-selection
bias as CFG809 addendum B describes, the same null-calibrated statistic applies here.

κ = ½ fitted; footings never pooled; cold energy mass required; not theory closed.
