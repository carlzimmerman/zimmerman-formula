# CRG1: resolution of the x62 flag. Spec agent's note, not given to the implementer.

**The flag.** `FG1_final_grade/x62_x43copy_law_a2.out` line 15 and `x62_x43copy_on_shpS9_L7.082_T12.3_B.out` line 15 read "K0 rule forced to Sigma_a0 reproduces X38: SPARC 0.0541 (0.0795), OUTER 0.999 (0.697): FAIL". The `on` file also has "X30 OUTER / MID 0.7801 / 1.6387: FAIL" on line 5.

**Resolution: harness mode, not a grader fault.** Two separate causes.

1. **K0x38.** In `X43_collapse_core_floor/x43_collapse_core.py`, `sig_core(f, tag, M, rule=False)` returns `(s, False)` (`if not rule: return s, False`). LEE1's harness (`LEE1_look_elsewhere/lee1.py`, `run_x43`) passes that second value as the `above` flag to `LF_G` and `LF_M`. In mode `law`, `_combine` returns the law regardless. In mode `on`, `above = False` selects the law branch too. So the check computes the law's SPARC and cluster numbers, in both files, and compares them with X38's a0-floor halo numbers (0.0795, 0.697). The check isn't testing what its label says. In mode `off` the same line passes, 0.0795 and 0.697 (`x62_x43copy_off_a2.out` line 15), which is the real test of X38's halos through this harness. The 0.0541 equals EM1's law rms (lines 5 of the same files), which confirms that it is the law branch.

2. **K0's X30 half, `on` file only.** The tag ends in `_B`, so `budget_edit()` puts GS1's gas tail and the native Omega ratio in X30's `prep`. That moves the C* denominator and so X30's KT_all OUTER and MID, which K0 pins at the pre-tail 0.716 and 1.668. `NZ1_zoom_core_radius/nz1_one_template.out` lines 3 and 4 show the same move: f* 0.20, no tail, KT_all 0.7160; f* 0.20, tail to r_ta, KT_all 0.7801. An expected consequence of the edit. `law_a2` has no `_B`, and its X30 half passes.

**Effect on FG1's graded cells: none found.**
- `fg1_harness.py` computes its own `k0` from LEE1's K0a, K0b, K0c, K2a, K2b, which don't use these lines.
- C3's K and X come from ZN4, not from the `_B` X43 cluster row, so the shifted C* doesn't reach them. C3's S and G don't read C* either. The `_B` edit changes only X30's cluster path.
- C4's K does read this harness's cluster row, from `law_a2`, with no tail and f* 0.20. Its X7 outer template matches its C* at that setting (M_all 0.9291 against X7 0.9291, `nz1_one_template.out` line 3), so the old-template defect found on 10-31 doesn't act on that row.

**What remains true.** These two checks print FAIL in harness modes by construction and carry no information there, and `x43_collapse_core.py`'s `exit 1` follows from them. FG1's `fg1_read.py` asserts this diagnosis as `K0-diagnosis`. That's a good guard against the pattern changing, but it reads literals from the same outputs, so it isn't independent evidence. CRG1's rebuild doesn't reproduce these checks. It has its own.

**Limit of this note.** It rests on reading the code and logs. I did not rerun any harness.
