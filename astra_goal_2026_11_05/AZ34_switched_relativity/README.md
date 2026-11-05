# UNDECIDED full relativity claims; scoped identities and estimates survive

Kappa = 1/2 FITTED; not theory closed. This audit does not change the scoped
adoption. Criteria were committed alone as825835993f. The post-result mapped
quadrature diagnostic was frozen separately as ea24dbeba4; it does not erase
the original quadrature failures. Both footings remain separate throughout.

## Six claims

| Claim | Result and limit |
|---|---|
| Binary pulsars | NO VERDICT full radiation. Conservative arithmetic survives; P3's propagating background-gradient mode prevents carrying C8's no-channel assertion. |
| Leaf problem | UNDECIDED existence and regularity. Strict convexity supports conditional uniqueness, but the energy fails to control H(div). |
| Causality | NO VERDICT gauge-invariant retarded response. Criterion B requires a globally regular timelike khronon; an elliptic equation alone does not settle criterion A. |
| Strong coupling | PASS scoped estimate, both footings. Full nonlinear/interface EFT remains open. |
| G9 | PASS matter-shell identity. The off-shell-zero claim is false. |
| Static black holes | PASS reduced static response, both footings; full finite-cap and moving/rotating solutions remain open. |

The exact leaf witness and conservation derivation are in
`STRUCTURAL_AUDIT.md`. Main structural checks15/17 and mutant13/17 retain
the two original quadrature failures. The mapped diagnostic passes unchanged
tolerances. Inverting the switch separately fails principal sound-speed
positivity and the original witness's uniform energy bound. Invariant G9
and GR checks correctly remain valid for either switch orientation.

## Corrected strong-coupling estimates

`coupling.py` uses corrected local u=GM/(c^2 L^2), retains W's cubic and
checks positive background divergence. Over the declared CQ7 intervals,
the largest loop estimates are0.0001181147 canonical and0.00009804985 alt,
below the inherited0.01 line. The corrected90pc Eot-Wash known answer agrees
with1.312e-3 within0.0241%; float64 and50-digit evaluations agree to1.23e-15.
The double-pulsar leakage estimates are at most3.444e-18 and3.100e-18.
These are mixing estimates, not a full binary radiation calculation.

The inherited free inputs remain explicit: Qbar-1=1e-6, mu_K^-1=100kpc,
external x_e=1,2,3, and longitudinal/transverse response brackets. The
screening length is FITTED. CQ7's interval itself retains the unswitched
satellite-solver caveat. Inverted-switch backgrounds are NOT EVALUABLE
on shell by reusing the main background: the positive-branch stiffness
that supported it has been removed.

## Static black-hole calculation

All30 members per footing pass: four benchmark masses, three lengths per
footing, four capped charges where applicable and screened p(2M)=0.
All60 coarse/fine pairs pass. Maximum coefficient changes are2.0436e-7
canonical and2.0419e-7 alt, against1e-3. Maximum physical shifts are2.4324e-11
and2.9393e-11, below P3's PROVISIONAL0.01 comparison floor. The24pc known
response reproduces exactly; Schwarzschild observables agree within1.78e-15.

D.P=N(p'+2p/r) is evaluated on512/1024 radial points from2.00001M to50M,
with positive minima8.2334e-7/8.2071e-7. The screened identity
D.P=(1-N)/(sigma N) is checked independently; capped limiting members have
p=1 and D.P=2N/r. This p=1 truncation does not resolve the full finite-a_hat
cap gap. Charges and benchmark masses are illustrative/free. This is a
stationary reduced calculation, not an EHT likelihood or binary ringdown fit.

The inverted switch removes a nonzero stiffness Euler term on these main
members; its residual is recorded separately. Their observables cannot be
called inverted-switch on-shell predictions. The production run peaks below
120MB RSS, single threaded. Source hashes and per-case checkpoints are saved.

## GR control

`gr_control.py` computes all256 linearized Riemann components of an arbitrary
pure gauge perturbation h_ab=partial_a xi_b+partial_b xi_a, with
xi_0=f(t)g(x,y,z). Its lapse is time dependent and satisfies a spatial
Poisson identity, but every curvature component vanishes. Superposing it
on a TT wave F(t-x) leaves the nonzero tidal field unchanged. All six exact
checks pass. This demonstrates why a lapse/constraint equation alone cannot
establish physical acausality; it does not solve v3s's sourced response.

## Reproduction

Run from the repository root, with OMP_NUM_THREADS=1 and PYTHONHASHSEED=0:

```sh
python3 -B astra_goal_2026_11_05/AZ34_switched_relativity/structural.py
python3 -B astra_goal_2026_11_05/AZ34_switched_relativity/structural.py --mutate
python3 -B astra_goal_2026_11_05/AZ34_switched_relativity/quadrature_diagnostic.py
python3 -B astra_goal_2026_11_05/AZ34_switched_relativity/coupling.py
python3 -B astra_goal_2026_11_05/AZ34_switched_relativity/gr_control.py
python3 -B astra_goal_2026_11_05/AZ34_switched_relativity/black_holes.py --resume
python3 -B astra_goal_2026_11_05/AZ34_switched_relativity/report.py
```

Structural exits1,1 are expected and preserve the failed numerical gates.
Coupling and GR scripts each write separate main/mutant records. On a fresh
BH output directory omit `--resume`; existing checkpoints require it and
must match every input hash. SIGTERM stops between atomic cases. The
initial serialization bug and full rerun are documented in
`IMPLEMENTATION_NOTES.md`. No old P3 output is overwritten.

The next calculations are the separately frozen nonlinear-existence,
moving-source, PN, interior, and full constrained-response lanes. A small
static correction is not a proof of full dynamical health.

## Board integration

The six cards now use `BOARD_CLAIMS.json`, backed by calculation commit
c869c20b96. The source/provenance, adoption-scope, red-tile and LW1 form guards
remain enforced. The baseline integration test failed21/27 checks before
editing; the new board passes27/27. All37 generator selftest mutants are
caught. The explicit off-shell-claim mutant and the generator's stripped-
source mutant both exit1. The rendered image was inspected; notes and both
vertical-force badges fit within their tiles.

```sh
MPLCONFIGDIR=/tmp/az34_mpl python3 -B explainers/make_status_board.py --selftest
MPLCONFIGDIR=/tmp/az34_mpl python3 -B explainers/make_status_board.py --mutate
MPLCONFIGDIR=/tmp/az34_mpl python3 -B astra_goal_2026_11_05/AZ34_switched_relativity/board_check.py --output board_main.json
MPLCONFIGDIR=/tmp/az34_mpl python3 -B astra_goal_2026_11_05/AZ34_switched_relativity/board_check.py --mutate --output board_mutate.json
MPLCONFIGDIR=/tmp/az34_mpl python3 -B explainers/make_status_board.py
```

Expected exits0,1,0,1,0. Nothing here certifies the action's remaining
nonlinear, moving-source or cosmological questions.
