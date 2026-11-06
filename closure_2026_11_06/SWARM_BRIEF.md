# Closure swarm, 2026-11-06: shared rules for lanes QX1-QX9

Goal (owner, 11-06): every gate gets a final label from ONE consistent action and mechanism. Every equation is
written in order and its algebraic steps are certified in Lean. Iterate on mechanisms (mutate, regrade) until each
gate passes, or until the lane proves that no member of a stated class can pass.

Rules, binding on every lane:
- Freeze criteria and commit them alone before any graded number. Tolerances come from real measurement errors.
  Every lane needs a MUTATE control, and it must bite.
- An iteration may change the MECHANISM: a new term in the action, a new field equation consequence. Each
  iteration gets its own frozen criteria file (QXn/iter_k/), so failures stay on the record. No knob scans; no
  constant tuned to a gate.
- Any candidate mechanism must keep the existing passes: SPARC/RAR, Cassini/PPN, c_T, galaxy lensing, Solar
  System. Recheck them on the candidate's own equations before calling anything a pass.
- No dark-matter particle. No LCDM inputs (no Planck parameters, no LCDM background). Raw data or
  framework-native only. Use both footings and never pool them. kappa = 1/2 FITTED; never write 'theory closed'.
- Retired or frozen items (route E cold sector, v3s variants) may be reopened as TEST lanes. Nothing is adopted;
  the owner adopts.
- Never edit astra_goal_2026_11_05/. Commit with explicit paths only (git commit -- paths). Push via a temp
  detached worktree (merge origin/main, push HEAD:main, retry on reject). Never rewrite history.
- Compute: nice -n 15, at most 2 threads, checkpointed parts. If the load average is above 40, wait.
- Lean: fable_independent_2026/lean_2026 (mathlib, lake). New files QX*_*.lean, each with a _MUTATE twin.
  0 sorry, standard axioms only, and the .out saved.
