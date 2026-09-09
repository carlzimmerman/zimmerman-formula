# IC37–39: evidence review, constructive variant, and next gate

Full original gravity goal **OPEN**. This is mathematical self-review, not an
independent referee or Lean certificate. Base c23c1d7ec34f32b1c982648a27ae25ce88243115.
Concurrent commits b349cb0f3 and 01c2a0514 supplied Claude/Fable's L44, and
97186208f supplied L45/L49 during this run. Working files of those lanes were
not edited. Input hashes, not temporal ordering of commit messages, govern
which calculations used which sources.

## What changed mathematically

1. **IC37:** analytic differentiation and local high-precision ODE Taylor
   recurrence replace unstable high-order derivatives of float64 fits.
   Choosing the two unused initial clock rates can cancel the quadratic and
   cubic boundary residuals to numerical precision. Neither chosen branch
   cancels the quartic residual. The old exponentially flat pin activation
   still fails this necessary bounded-response test for these selected data,
   conditional on the numerical nonzero-jet evidence and stated regularity.
2. **IC38:** an exact function-level elimination criterion removes the lapse
   boundary constants altogether. On its regular determinant domain, TWO
   differential residuals must vanish as functions. A hand-solved counterexample
   shows why keeping only the first would falsely certify compatibility.
3. **IC39:** a new explicit pin-potential variant turns on as x^4, leaving the
   exponential MOND primitive unchanged. A quartic source then admits a finite
   second multiplier response, provided the lower jets vanish exactly. The
   new pin potential is varied before constraints are imposed, and its pinned
   q/z Schur coefficient is independently recomputed. The price is a C3/not-C4
   activation and an unproved exact-root/matching certificate.

This is a constructive change in the obstruction, NOT completion of the theory.
No failed construction or inconvenient output was removed.

## Numerical results, in the code's dimensionless normalization

After solving the actual lapse equation and matching E=E_r=0 at r=2:

| initial clock rates | E_rr | E_rrr | E_rrrr |
|---|---:|---:|---:|
| U0=U1=0 | 2.5637063003e7 | 8.7203586832e9 | 3.9551407872e11 |
| IC36 U1=-2.64003824557, U0=0 | -2.6293841967e4 | -1.3734899996e8 | -4.9609271492e9 |
| select U1=-2.63810520446, U0=0 | about 2.76e-33 | -1.2822185025e8 | -4.4991100169e9 |
| select U1=6.60495166651, U0=0 | about 6.33e-33 | -1.6728090577e9 | -7.0417971660e11 |
| joint negative branch | about 4.76e-43 | about -7.31e-40 | -1.1529842694e9 |
| joint positive branch | about 3.52e-43 | about -2.78e-40 | -4.6840486219e11 |

The joint negative branch has

    U0=-0.024569822448770560055189567877390905071374214282622,
    U1=-2.5425647701326657979323182304426915663638892064619.

The joint positive branch has

    U0=0.049997879816162768977345635978832286049939235839415,
    U1=6.5714508508935263539735046750709712493534055587717.

Both were selected by actual computed residuals and Jacobians; the searches
took 12 and 13 float root evaluations, followed by high-precision refinement.
The substantial nonzero jets agree between 50- and 80-digit evaluations.
Near-zero values vary with rounding and are NOT exact zeros or interval bounds.
The actual boundary determinant is approximately 249750.58657147188263, with
computed rank 2. This is a response matrix, NOT a Poisson-bracket matrix.

IC38 independently recovers those lapse boundary constants. Its baseline
R2(2)=52583.4562140433. For the two joint branches R2 and R2' are tiny, but
R2''=-2364853.48738731 and -960731990.204022, respectively, stable under the
precision change. Thus a zero first compatibility residual at the face does
not certify a common solution throughout the collar.

For IC39's eta4 and exact satisfaction of the four lower-jet conditions, the
conditional limits ell_tt(2+) are approximately 0.00158812197295783 and
0.645181442277073. The output explicitly reports unresolved lower jets and
`exact_zero_jet_certificate=false`; it does not divide numerical leakage by
eta4 and declare it finite. eta4's fourth endpoint derivatives are +6144 and
-6144 versus zero on the adjacent constant plateaus, so the C4 failure is real.

## Exact statements versus computational evidence

**Interface lemma:** with E=W_tt and initial w=wc, ell=ell_t=0, finite S and
bounded ell_tt require E=O(eta). For the old exponential switch a first nonzero
finite Taylor jet violates this. All-zero jets are not sufficient for smooth
nonanalytic E; exp[-1/(2x)] is the explicit counterexample.

**Operator theorem:** for real C2 coefficients and sources on an open interval
with c2 and det(M) nowhere zero, IC38's R1=R2=0 as FUNCTIONS is necessary and
sufficient for a common C2 lapse-acceleration solution. The proof is direct
elimination, differentiation and substitution. No division by b1 is used.
Singular det(M) is undecided. SymPy verifies the generic identities and tests
include compatible, incompatible and singular manufactured pairs. Verdict for
this restricted theorem: proved as written by the supplied elementary proof,
with self-review; no machine-checked Lean proof.

**Variant lemma:** if x=a delta+o(delta), a>0, S->S0, and
E=E4 delta^4/24+o(delta^4), then eta4 yields
ell_tt -> -E4 b^4/[24 exp(S0) a^4]. This is an exact conditional asymptotic
statement. Existence of exact field data satisfying its hypotheses is missing.

**Field numerics:** computationally verified only in the stated local,
fixed-coefficient domain and precision range. No interval enclosure, analytic
continuation radius, full nonlinear solution or general initial-data exclusion.
Dependency chain: IC29/30 action -> IC32 coefficient -> IC33 physical flows ->
IC35 first-preservation ODE -> IC37 sources -> IC38 elimination / IC39 variant.

## What Claude's new work contributes, and what it does not

L44 was rerun unchanged: 76 printed PASS entries, exit 0. Its independently
reconstructed pinned q/z Schur coefficient agrees with the new variant's
direct variation. The escape from that particular transition-ghost mechanism
belongs to IC20, not to the later finite-multiplier work. Preserve this
structural invariant; do not move the activation onto kinetic terms.

The pass count is not a proof count. L44-D3 contains `or True`; F6 checks
assigned mode-count arithmetic and documentary text; finite samples do not
establish uniform theorems. These limitations do not invalidate the separate
symbolic Schur identity. Neither L44 nor this turn supplies a full scalar
Dirac/propagator certificate. L44's finite-order activation suggestion is
credited in the new variant. No superluminal-clock relaxation is adopted.

The newer L49 belongs to a different deposited action and uses a different
kernel. `l49_kernel_scope_audit.py` extracts and executes its actual pure
kernel functions and constants, without importing its empirical pipeline.
At gN/a0=1 it returns g/a0=1.5819767068693262, whereas the requested exact
mu(y)=1-exp(-y) gives 1.349976485401124. Substituting L49's value into the
requested equation leaves residual 0.25677236872889897; the independently
root-solved value leaves about -1.44e-15. At gN/a0=100 L49 adds a saturated
0.6476; the exact requested kernel does not. Its quoted overshoot/fractions
must therefore NOT be transferred unchanged to IC29/30/39.

Additionally, L49-N9 tests only a small algebraic S_eff and then claims CMB
and growth recovery; it does not calculate CMB spectra or establish equality
of the full coupled perturbation systems. N8's BBN check is literal True, and
the script always exits 0 even when scientific checks fail. Its code explicitly
inputs Planck Omega_c h^2, rather than inferring it under the modified theory.
These are reasons to retain its mechanisms as leads, not accept its claim of
an otherwise complete theory or a universal CMB exclusion. L45/L49 raw-data
inferences were NOT reanalysed in this turn. Their full empirical script was
not run; only the recorded kernel scope calculation was run. No claim here
validates or refutes their empirical fits.

## Executed checks and scope

| job | child exit | runner exit | interpretation |
|---|---:|---:|---|
| IC37 analytic source audit | 0 | 0 | independently compiled flow and finite kicks agree |
| IC37 float diagnostic | 2 | 1 | scoped identities pass; derivative-fit weakness preserved; full theory OPEN |
| IC37 high-precision study | 2 | 1 | both constructive root branches recorded; full theory OPEN |
| IC38 functional study | 2 | 1 | exact identities and numerical obstruction retained; full theory OPEN |
| closure regression suite | 0 | 0 | 440 tests, 323.158 seconds inside unittest |
| IC39 variant | 2 | 1 | seven scoped checks true; conditional gate only |
| IC39 focused tests | 0 | 0 | 3 tests pass |
| unchanged Claude/Fable L44 | 0 | 0 | 76 printed PASS entries with the caveats above |
| L49 kernel scope audit | 0 | 0 | different constitutive laws demonstrated |
| L49 scope tests | 0 | 0 | 2 tests pass |

All ten manifests validated against the current repository with exit 0.
Hashes remained unchanged through each run. All jobs are terminal. The full
440-test suite was collected before the five later focused tests existed;
445 distinct tests passed across the three test jobs, not a claimed single
445-test discovery. Resource limits: 600 wall seconds per main job (60 for
the L49 scope jobs), 2 MiB logs, one cooperative numerical-library thread.
No hard memory, CPU-time or affinity cap. Exact argv, input hashes, software,
runtime, raw outputs and status are in the manifests and run_index.json.

Test-first failures were observed for missing IC38 module, numeric reducer and
coefficient export, for missing IC39 module, and for missing L49 scope module.
Manufactured ODE, constraint-pair and activation tests later passed. Additional
precision/consumer tests strengthen the audit; not every scientific identity
was independently invented test-first. The historical IC37 float failures
remain reproducible, and no old evidence was overwritten. Lean and lake were
not found on PATH; there is no formal proof artifact to claim.

Mathbox computation-audit enforced input/output provenance and scope separation;
proof-audit and proofread-math were self-review of the IC37–39 derivations and
this report. No separate mathematical-token typo repair was needed.

## Unavoidable next construction calculation

Pursue IC39 without importing unproved success from the old activation:

1. Certify an exact nearby solution of the two initial-data selection equations
   (not merely a tiny Newton residual) and its regular first-preservation ODE.
2. Construct the inactive-side unpinned response and a common finite interface
   expansion; evolve or preserve through the next time order with the actual
   eta4 derivatives. Reject distributional sources or a new hidden mode.
3. Continue the functional Dirac chain and full scalar/vector/tensor stability,
   including rank-changing, homogeneous and zero-field sectors. A positive
   pinned Schur coefficient is not a substitute for this calculation.

Original gates still needing full certificates: same-action global MOND/GR
recovery and measured G; independent lensing and full PPN beta/gamma/alpha_i;
two tensor gravitational DOF plus only an explicitly healthy clock; ordinary
matter Ward identity on the complete system; physical tensor light cone;
ghost/gradient/strong-coupling/causality control; expanding cosmology and its
galaxy matching; controlled k=0/y=0; and empirical galaxy, binary, cluster and
pre-recombination/CMB tests. The vacuum-scale coefficient one half remains an
input. No requirement has been lowered to manufacture a PASS.
