# IC28 constant-tensor construction checkpoint

Full theory **OPEN**. The report's local checks are not a cosmology PASS.
This is a distinct action branch, not IC26 with reinterpreted outputs.

## Surviving result from one action

Setting v=v0 in the explicitly specified phase action gives H_qR=H_RR=0,
H_SR=-v0 and constant physical tensor kinetic coupling. The independently
derived linear potentials satisfy Phi=Psi on the active homogeneous pin.
The compatibility equation is satisfied on the H_RR=0 branch, which the old
nondegenerate Legendre transformation excluded.

The same actual varied witness has H_physical=1.03149697657,
a=.0131578947368, scalar principal speed squared .00906008396237,
and lapse Schur M=-3 in model units. The two fluid modes are retained.
All sampled kinetic matrices are positive; actual local auxiliary brackets
have computed rank4 at k²=0,.001,1,100,1e12. This is not a nonlinear DOF count.
The primordial clock remains a counted physical scalar candidate.

## The two executed continuation attempts

1. Explicit exponential D(S): both step grids stop near
   Q=.00022110012526. The last lapse Schur magnitudes are about8.4e-8
   and4.7e-8, with charge errors below4e-15. This is evidence of approach
   to a lapse degeneration, not successful cosmology.
2. Integrated D(S) with M=-3 held by actual coefficient jets: both grids
   reach the declared positive-z floor near Q=.01547848. The last z
   values are about8e-7; D is about1.8e5 and a about1.4e-8.
   Charge errors remain below1.3e-13. No zero-field continuation is claimed.

The initial large step once jumped to negative z in a diagnostic probe.
That probe was not a valid continuation of the positive-z reconstruction.
A regression test now rejects nonpositive z before division, and the
integrator limits its step using the actual z velocity. The bounded recorded
runs use this guard and retain its stopping reason; no negative-z result
is used as a physical counterexample.

The exact auxiliary equation explains the new obligation:

    D=-Aq/(2z)-2E4 z².

If z tends to0 while A and nonzero q remain finite, D diverges and
a is asymptotic to -Az/(2q), tending to0. This is a conditional algebraic
limiting statement; the finite guard runs do not prove the entire limit.

Full Euler spectra are not globally stable certificates. For the integrated
trial, an initial k²=.001 root is approximately +80.9120 in T-time, and
positive real parts are not discarded. Their finite-time physical effects
still need integration; no all-scale stability PASS is made.

## Next constructive move

KEEP the constant tensor coupling and its no-slip identity.
The lapse drift is Sdot=[3Qdot(rhoH+pH)-C qdot]/M. At the same initial
state, increasing |M| slows that drift without altering the leading no-slip
or kinetic identities. A read-only local diagnostic at M=-1000 gives
Sdot=.01163260223 and zdot=-.9719875002, compared with Sdot=3.877534077
and zdot=-60.27335544 at M=-3. Genuine-jet residuals remain below4e-40
in that40-digit calculation. This is only a local distinct-action diagnostic,
NOT an integrated history. Its exact command is recorded in run_index.json.

The next bounded evolution should first test that slower-clock integrated
potential, then vary A(S) jointly with D(S) if the positive-z boundary remains.
The no-slip derivation is independent of those coefficient choices.
The proposed constant-z design equation is in IC28_CONSTANT_TENSOR.md.
Do not pool different choices into a single completed theory.

Beyond this: same-function off-trajectory matter, full nonlinear constraints,
static/pin-off MOND matching, measured G and PPN, physical causality and
interaction scales, and actual galaxy/cluster/CMB evidence remain required.
No empirical fit, novelty certification, Lean proof or peer review is claimed.
