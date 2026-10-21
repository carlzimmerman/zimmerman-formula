# Next bounded test: constrained expanding-background action

This plan is unexecuted. It precedes a physical dwarf-core merger calculation because the current covariant action has a tensor kinetic obstruction and no tethered cold-cold Newtonian attraction. It does not change prior frozen scoring rules.

1. Pin the action and conventions. Test the original CFG938 four-Hessian operator and the explicitly new tau+alpha dot_chi sigma family as distinct claims. Use a densitized conserved current or include sqrt(-g) consistently when representing n u^mu as a divergence. Derive rather than assume the homogeneous chi/lambda, density and Friedmann equations.
2. Expand the full covariant action to quadratic order on that background, including lapse, shift, metric, medium labels, chi, lambda and variations of h^{mu nu}. Perform the scalar/vector/tensor decomposition before eliminating constraints. Do not insert the frozen static Poisson constraint as the time-dependent solution.
3. Recover the exact original TT coefficient Q_T=1-3 gamma dot_chi^2/K and alpha-family factor (1-alpha)^2. Recover the static first variation and the restricted adverse velocity-gradient diagnostic as cross-checks, without mistaking the latter for a fully reduced ghost eigenvalue.
4. Compute the reduced kinetic and principal-gradient matrices, constraint rank and degree count, keeping special degeneracies explicit. Give the parameter/background domain and any justified EFT cutoff before testing sign, characteristics or high-k limits. If the declared branch fails, retain that failure; do not relabel it as a complete covariant parent.
5. If a consistent action survives, derive its binding/free phase and transition law. Verify total gravity source, conserved charge and physical mass normalization in the same action as the fragments. Tethered-medium shell crossing alone does not derive ordinary free self-gravity.
6. Then resume the transport gate: actual isolated/pair energy, charge, momentum and orbital/intrinsic angular momentum currents, radiation and bound-daughter channels, finite outer-envelope capacity and verified escape. Use actual post-merger charge and an appropriate nonlinear core reference. Demonstrate boundary/cadence and isolated-control convergence before assigning a cooling efficiency.
7. Apply that same physical kernel and nonnegative profiles to Draco, Sextans, Fornax and Leo I. Enforce stock, rest-energy losses, population/selection and full stellar tracer guards; account for receiver mass and stellar heat. No per-galaxy selector or 44% asymptotic escape may be supplied by assumption.

Keep each new process below 1 GB; do not duplicate Claude's live integrations. Save a contract before each new experiment, exact source receipts, raw outputs, failed implications and a validated manifest. A successful algebraic or finite check does not close the full theory.

Replay the completed audit (use a NEW output directory and runner declaration if making a new run; do not overwrite run_001):

    mkdir /private/tmp/cfg938_tensor_replay_output
    python3 tensor/tensor_core_check.py /private/tmp/cfg938_tensor_replay_output

The original reproducible command, limits, inputs and exact hashes are recorded in `tensor/contract.json` and `tensor/run_001/manifest.json`. Manifest validation uses the computation-audit `validate_manifest.py` with `--root` set to this packet's `tensor/` directory. Script replay requires Python with SymPy 1.14.0; the raw model code is never imported by this audit.
