# Verified checkpoint: fixed-history criticality and a sourced response system

Continues `196f84653`. No action functions or fitted parameters were changed.
This checkpoint follows Carl Zimmerman's primordial-clock direction; it does
not derive the fitted one-half acceleration-scale coefficient. **Complete
relativistic MOND theory: OPEN.**

## Strongest new result

For the actual fixed canonical future reference history
\(\gamma=10^{-6}, M^2=1, a(0)=1,m(0)=1/10,v(0)=1/2\),

\[
\boxed{G>\gamma Hq/5>0,\qquad K>(1411/2500)B_0>0.}
\]

The proof combines an invariant region of the prescribed ODE with an exact
positive-polynomial bound. It rules out reaching the proposed **full FLRW
principal** critical point \(G=0\) at a finite regular future epoch on this
history. It does not exclude past epochs, spatially nonlinear branches,
other initial data, finite-wavelength instabilities, or a zero gap at an
infinite-time endpoint. Four Lean statements certify the pointwise rational
algebra; the action variation and invariant-region ODE proof remain outside
Lean and are independently audited. See `history/REPORT.md`.

This is stronger than another finite scan: the three numerical epoch checks
only test the code-to-model map, not the absence of a future crossing.

## Additional completed work and honest limits

- `adm/`: a different-gauge derivation of the full quadratic action, including
  explicit background residuals and exact agreement with the previously
  existing source-free finite-wavelength constraint and kinetic coefficients.
  This is an independent cross-check, not a newly discovered free system.
- `probe.py` and `PROBE.md`: a conserved matter probe, varied constraints,
  explicit canonical forcing and separate expressions for both physical
  potentials. The numerical forced evolution is **not yet run**. It is a
  formal signed linear probe, not a galaxy or CMB calculation.

The critical branch is therefore not available simply by waiting for the
fixed future background to reach it. The next executable step is the forced
response integration already specified in `PROBE.md`, with constraint-compatible
initial data. No reconstruction of new coefficient histories is needed or
authorized by this result. An unchanged-action nonlinear galaxy calculation
and the remaining cosmological/PPN/constraint gates are still required.

## Verification

`verify.py` executes the new Python/Lean work and relevant existing action,
background and metric-response regressions, with two workers and a 90-second
limit per child. `run_001/checks/summary.json` records exact commands, working
directories, exit codes, hashes and printed Lean axiom sets; `COMMANDS.md`
records the reproducible runner invocation. `FILES.md` is the exact inventory.
No success flag means a complete gravity theory.

The combined run completed successfully: eight Python jobs and two Lean
compilations exited 0. All eleven printed theorem axiom sets use only
`propext`, `Classical.choice`, and `Quot.sound`; four of these statements
are new. The deliberate assertion negative control exited 1 as required.
All three current provenance manifests validate. The new Lean file emits
one harmless tactic-style linter warning; no proof error or sorry is present.
The already-hashed source is retained unchanged.

The research/computation-audit skills caused us to reuse existing finite-k
work, separate formal algebra from physical implications, and obtain an
independent check of the invariant-region proof before publication. Prose and
formula self-review covered only this checkpoint's new files.
