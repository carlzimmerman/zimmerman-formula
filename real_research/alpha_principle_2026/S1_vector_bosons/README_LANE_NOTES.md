# S1 lane notes (added after an independent re-run; no result changed)

* **Registered versus enforced checks.** The pre-registration lists checks D1-D7 for the mode-sum stage. After development smoke tests the lane re-registered its stage
  (Amendment 3, written before the final scripts s1_3 and s1_4 ran) and the final scripts enforce the RE-REGISTERED checks E1-E7 and C1-C4, not D1-D7. The thresholds of E1, E3 and E4
  were set after seeing scratch numbers (disclosed in Amendments 3 and 4); the pre-registered no-electric-instability expectation (E7) failed on the first run of s1_4 and was
  re-registered post hoc (Amendment 4; the first run is kept as `s1_4_vector_uv_and_current_FIRSTRUN.out`). Read the S1 result as: what the final scripts enforce, not what D1-D7 originally demanded.
* **Trailing 'exit N' lines.** Several committed `.out` files in this and other lanes end with a line `exit N` appended by the shell wrapper that saved them; a fresh run of the script does not write it.
  `s1_3_modesum_validation.out` and its `_MUTATE.out` were regenerated from fresh runs (stdout only). Other lanes' `.out` files were left as saved.
* No PDFs, caches or usernames are stored in this lane.
