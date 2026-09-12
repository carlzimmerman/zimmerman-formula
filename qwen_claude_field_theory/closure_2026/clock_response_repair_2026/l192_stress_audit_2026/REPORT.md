# L192: metric stress does not become exact dust at the reported roots

All ten inverse-metric variations confirm the proposed stress tensor of the frozen gamma0 action. At every one of the20 tested cases, its invariant transverse pressure is nonzero. Thus the reported sound-speed proxy zero does not imply exact dust stress.

At the first L192 transverse root, a=1 and Yt=0.00025242369831450766, faithful use of L192's Q=qbar gives

    L = 0.0002763569145371649,
    L/U = 0.0303992605990881,
    L/T00 = 0.00277085534289249,
    L192 transverse proxy cs^2 = 8.86e-17.

Using the recorded physical Q at that unchanged root gives L=0.00015264998924072876 and L/U=0.0167914988164802. The latter point is no longer a zero of L192's proxy; its value is -4.08613e-5. Neither evaluation adjusts the root or replaces the reference state in P.

## Derivation from all metric components

Signature is(-+++), and

    X=-g^{ab} chi_a chi_b,
    s=sqrt(-g^{ab} tau_a tau_b),
    Y=-X+(g^{ab} tau_a chi_b)^2/s^2,
    action density=sqrt(-g)[P(X,tau)-V(tau)+s W(Y,tau)].

Vary each independent symmetric component of the inverse metric before specializing to Minkowski space, tau=s0*t and chi=Q*t+b*x. Off-diagonal variations change both symmetric entries and therefore carry multiplicity2. With L=P-V+s0 W and Y=b^2, the exact result is

    T00 = 2 PX Q^2-P+V,
    T0x = Tx0 = 2 PX Q b,
    Txx = L+2(PX-s0 WY)b^2,
    Tyy = Tzz = L,

with every remaining off-diagonal component zero. The scalar action and its volume factor are both varied; holding s or the projected gradient fixed during metric variation would give a different and incorrect tensor.

The mixed tensor T^a_b has transverse spacelike eigenvectors in the y and z directions with eigenvalue L. These eigenvalues are invariant under changes of frame. Exact dust T_ab=rho*u_a*u_b has three zero spacelike eigenvalues, so L!=0 is sufficient to exclude exact dust at a tested point. Nonzero Txx-Tyy in the clock frame alone would not suffice because T0x also need not vanish.

There is an additional exact identity. Define the numerator of L192's transverse proxy by

    N_T = 2 PX(1-2 Q^2 WY/W)-2 s0 WY.

Then

    det[(T^a_b-L delta^a_b) restricted to(t,x)] = -s0*b^2*W*N_T.

At N_T=0, a third mixed-tensor eigenvalue equals L. The stress can therefore resemble a boosted perfect fluid with nonzero pressure rather than dust. The calculation does not assume or establish a physical sound-speed formula from this stress identity; the independent principal-symbol audit addresses that different question.

## Fixed reference state and numerical evaluations

The gamma0 limit of the existing action is used exactly:

    P = -U/2 log[(U-2dX)/(U-2d qbar^2)],
    V = U,
    W = U+2d ell(sqrt(1+Y/ell)-1).

The denominator always uses the original qbar coefficient history. Independently reintegrating the same coefficient IVP and directly evaluating these expressions agrees with the authoritative constitutive jet evaluator. Changing the denominator to the physical Q would change the action's additive P value and hence its stress.

The source's first coefficient state is qbar=10/11, U=1/110, d=1/200, ell=5/121. Its physical scalar rate is Q=0.90783215058, rather than qbar=0.90909090909. Both choices are evaluated at each unchanged source Yt and Yl; five positive-root epochs times two roots times two Q choices gives20 cases.

| Epoch a | L/U at recorded Yt, Q=qbar | L/U at same Yt, physical Q |
| --- | ---: | ---: |
| 1.000000 | 0.0303993 | 0.0167915 |
| 0.750137 | 0.0693705 | 0.0387435 |
| 0.562705 | 0.169230 | 0.0958255 |
| 0.422105 | 0.407427 | 0.202965 |
| 0.316637 | 0.117076 | -0.331089 |

All20 transverse eigenvalues are resolved away from zero under the stated1e-9 threshold on abs(L/U). The source-faithful proxy zeros are reproduced independently to better than1e-10. The source's displayed physical logarithm margin is reproduced using physical Q, which confirms the qbar/physical-Q distinction.

These are frozen local evaluations. The input physical background was generated with gamma=1e-6; stress is evaluated at gamma=0 as requested. No claim is made that these inherited field values with added spatial gradient solve the gamma0 Einstein, scalar, or clock equations.

## Checks and exact run records

Five unit tests passed: all ten metric directions and symmetric multiplicities; the repeated-eigenvalue/proxy identity; reference-state preservation; finite differences of the complete explicit metric-dependent density; and domain rejection. There are39 additional source, jet, proxy-root and numerical consistency checks.

Finite differences of all ten components at the first Yt reproduce the symbolic stress for both Q choices. The maximum scaled error decreases from2.57e-10 at metric step1e-5 to3.69e-12 or less at step1e-6.

Fresh evidence is in run_002/result.json and run_002/manifest.json. The bounded run started2026-09-12T15:11:07.160763+00:00, ran1.843717seconds and exited0. The five-test suite within that run completed in approximately0.3seconds; the exact timing is in stderr.txt. Manifest validation with --root exited0, verifying current source inputs and result/log hashes. The verdict now branches on the computed nonzero-pressure result rather than being an unconditional output string.

Executed scientific command from repository root:

~~~bash
python3 -B -m unittest discover -s qwen_claude_field_theory/closure_2026/clock_response_repair_2026/l192_stress_audit_2026 -p "test_*.py" -v && python3 -B qwen_claude_field_theory/closure_2026/clock_response_repair_2026/l192_stress_audit_2026/stress_audit.py --result-file qwen_claude_field_theory/closure_2026/clock_response_repair_2026/l192_stress_audit_2026/run_002/result.json
~~~

The exact expanded bounded-run argv, resource limits, repository state, software versions, and seven input hashes are stored in the manifest. Run through computation-audit/scripts/run_experiment.py with contract.json, timeout120seconds, CPU cap100seconds and cooperative numerical thread cap1.

Validation command:

~~~bash
python3.11 /Users/carlzimmerman/.codex/plugins/cache/openai-curated-remote/mathbox/3.0.0/skills/computation-audit/scripts/validate_manifest.py qwen_claude_field_theory/closure_2026/clock_response_repair_2026/l192_stress_audit_2026/run_002/manifest.json --root /Users/carlzimmerman/new_physics/zimmerman-formula
~~~

The initial run_001 exited0, but is historical after the verdict-output repair. Its original source is retained as run_001/source_at_run.py and matches its recorded source SHA256 exactly. Its manifest still points to the original now-modified source path and must not be presented as current-input-fresh evidence. No manifest was edited to conceal that distinction.

Used computation-audit and verification-before-completion workflows. This report is a bounded stress obstruction to the asserted exact-dust interpretation, not a full-theory no-go, attractor calculation, observational result, or proof of the complete constrained principal system. No source coefficients, root values, reference normalization, or other agents' files were changed; no Git mutation was performed.
