# Independent audit: FGF046

Normalized claim: for every fixed smooth positive hydrostatic signed-Q
background on the specified regular interval, and each exact compact C1,1
polynomial datum with L/N^3<R/2, the author constructs a positive C1 solution
of both forced isothermal fluid equations on the declared cone for
T_N=min(tau,1/(8M),R/(4S_N))>0. Spatial gradients are Lipschitz, local
uniqueness holds among positive C1 competitors, and the physical germ is
independent of auxiliary extension. T_N>=c_* N^-4 for sufficiently large N.
A buffered interior restart holds under all bounds in author (20), including
a uniform Lipschitz-gradient bound. The energy identity includes moving
boundary terms. The pinned FGF045 obstruction applies only to continuations
covering its stipulated cone and satisfying its large-N gates.

Primary verdict: **proved as written**.

The verdict concerns that precise local construction and higher-norm gate.
It neither removes the higher norm nor classifies an earlier endpoint.

## Provenance and authoritative revision

Reviewer: /root/fgf046_reviewer. The independent derivation was frozen at
2026-10-06T02:41:30.584086+00:00, SHA256
c29434e8abbabc2034833a1d4936cb804fef6467fd51c31d42c964bbb88c2d62.
The accompanying DERIVATION_FROZEN.json pins task, contract and all old
ancestry. Only that material was read before freezing. No new root proof
was read during this review. AUTHOR_EXPOSURE.json records first exposure
to the author-declared final bundle; no pre-freeze author draft was read.

Authoritative proof:
deepseek_push/astra_spawn_ideas/fresh_gravity_followups/results/FGF-046/fgf046_run_001/DERIVATION.md,
SHA256 60fe268cf837456527205f8f3a8337646c5cc8eaf6560446d2ec0b3805a075e1.
Author result.json:
8ed09eb44ace4214dffe87a7c396a43a8b12a80c5b751c7a1495dee785b610f1.
REPORT.md and input_sha256.json were also read and checked against that result.
The reviewer did not edit any author bytes.

The independent proof used a slightly smaller time coefficient 1/(16P) and
a different harmless gradient-Lipschitz envelope. It independently found the
same C0 contraction plus derivative-interpolation mechanism and the same
need to retain the higher norm in its proved continuation gate. Agreement is
not itself proof; the specific checks below supply the review evidence.

## Dependency graph

1. Smooth regular hydrostatic Q background and exact C1,1 datum [task and
   pinned ancestry; domain/convention leaf].
2. Invertible invariant transformation [internal algebra, (2)-(3)].
3. Elementary ODE iteration and flow Jacobian [internal construction, (8)-(9)].
4. Uniform amplitude, gradient, gradient-Lipschitz estimates [internal scalar
   integral estimates, (10)-(12)].
5. Uniform contraction [internal estimate, (14)] plus derivative interpolation
   and time-integrated limit [(15), internal analysis] -> actual C1 solution.
6. Exponential inversion [internal algebra] -> positivity and both fluid PDEs.
7. Intrinsic cone-speed bootstrap + difference transport [internal estimates,
   (17)-(18), Section 6] -> physical localization and extension independence.
8. Buffered endpoint modulus + cutoff restart [internal construction,
   (20)-(23)] -> sufficient continuation with all stated norms retained.
9. Product-rule energy and hydrostatic control [internal algebra, (24)-(27)].
10. Constructed germ + separately pinned FGF045 theorem under its own gates
    [old internal theorem] -> conditional no-continuation-through-upper-time.

No circular dependence is present: local existence does not use FGF045's
upper obstruction; that theorem is used only after existence and uniqueness.
There are no external theorem or numerical-computation leaves.

## Obligation matrix

| Obligation | Result | Evidence |
|---|---|---|
| Exact unsmoothed data and exceptional joins | passed | f and f' match continuously at +/-1; f'' need not; Lip f'=8 |
| Actual initial norm dependence | passed | M0=O(N^4), H0=O(N^7); (5)-(6) retain both |
| Positive sound speed and full pressure | passed | c>0 permits inversion; both speed families and pressure remain |
| Forced linear iterate exists | passed | Bounded speeds and spatial Lipschitz coefficient give concatenated integral contractions |
| Flow differentiability without C2 data | passed | C1 coefficient gives variational integral equation; exact C1,1 datum suffices |
| Uniform derivative modulus | passed | Pair-characteristic quotient bounds Lip p by (11) |
| Quantitative induction | passed | MT<=1/8 closes both M and H bounds with strict margin |
| Uniform C0 contraction | passed | Difference forcing uses preceding gradient; ratio <=1/8 |
| Genuine C1 limit | passed | (15) gives spatial derivative Cauchy convergence; PDE gives time derivative convergence |
| Initial trace and positivity | passed | All iterates have identical trace; exponential reconstruction and (16) |
| Local time lower bound | passed | (19) bounds all entries of the minimum below by c_*N^-4 |
| Backward characteristics stay regular | passed | Strict intrinsic speed margin c and moving-cone first-contact argument |
| C1 competitor uniqueness | passed | Integral difference inequality iterated to factorial remainder |
| Auxiliary extension independence | passed | Same physical speed bootstrap and same data/force on K0 |
| Sufficient endpoint continuation | passed | (20) supplies spatial modulus; (21) supplies time modulus; trace and restart preserve C1 |
| Positive spatial buffer | passed | J inside I, intermediate I', cutoff neighborhood and explicit delta-time gate |
| Energy and correct signs at boundaries | passed | Pressure and force work cancel; Reynolds terms have signs b'E(b)-a'E(a) |
| Exact hydrostatic control | passed | v=0,n=rho solves both equations; local uniqueness identifies it |
| Same-branch FGF045 corollary | passed under its explicitly stated gates | Existence supplies a germ; only cone-covering continuations face the upper obstruction |
| First-gradient-only continuation | not addressed | Author explicitly retains K_* |
| Shock or earliest endpoint classification | not addressed | Explicitly disclaimed |
| Coupled gravity or evolving-H closure | out of scope | Source residual and branch separation retained |

## Decisive reconstruction and adverse checks

The potentially fragile step is derivative preservation, not the C0
contraction. Along two frozen-flow curves, p solves p'=-v_x^k p-g_e'.
The quotient of the difference by curve distance has a coefficient bounded
by 2M: one M comes from the p equation and one from differentiation of the
curve distance. The remaining term is bounded by H sup|p|+G2. This derives
(11) directly from Lipschitz data; assigning a continuous second derivative
to f would have been invalid but is unnecessary here. With MT<=1/8,
exp(2MT)[H0+TG2+THM] <= (4/3)(H/4+H/8)=H/2.
Thus the higher norm really is uniformly bounded throughout iteration even
though its initial value grows as N^7.

For h=u^k-u^j, the remainder between h_x and a forward quotient of length
a is at most H a because Lip(h_x)<=2H. This gives
||h_x||<=2||h||/a+H a and the displayed square-root bound. The estimate is
valid on the whole auxiliary line, so no boundary loss occurs when choosing
a. Uniform convergence of the continuous derivatives makes u_x jointly
continuous. The PDE then gives uniform convergence of u_t. No compactness
subsequence, weak-derivative identification alone, or implicit C2 theorem is
substituted for the classical solution.

A large H does not impose an extra inverse-H lifespan restriction: its
recurrence is linear in H times T M, and H was chosen proportional to its
actual initial value. It enters derivative-convergence constants but not the
contraction factor. This explains the valid N^-4 lower time despite the N^7
second-derivative scale. The c_* formula is dimensionally consistent: the
norm and force terms entering m_bar all have units inverse time, and s_bar
has units speed. Floors tau^-1 and (tau d)^-1 handle zero-norm controls.

The physical cone uses a speed determined by physical initial and force
bounds, not the exterior cutoff values. Its bootstrap does not assume the
solution stays hydrostatic outside the bump. While its speed inequality
holds, backward characteristics remain in the cone, and integration improves
the inequality by margin c, excluding first contact. The same argument
holds for each extension before comparing solutions. This makes Section 6
stronger than merely asserting global auxiliary uniqueness; it genuinely
removes exterior information from the physical conclusion.

For continuation, a uniform spatial Lipschitz bound alone is not mislabeled
a spacetime trace theorem. The author first bounds the characteristic
variation of p by P_*^2+G_K1, then controls its shift at fixed position by
K_* times characteristic displacement. This is exactly the missing temporal
modulus and is valid on I' using the collar. The terminal function and its
spatial derivative converge uniformly; cutoff extension bounds (22) follow
by the product rule. The restarted PDE supplies the matching time derivative
at t_*. The construction extends an interior J, without claiming lateral
boundary data or continuation on an entire unbuffered cone.

The zero-velocity control tests pressure-force cancellation instead of
setting those terms to zero. The relative-energy flux has no asserted sign;
only its density is nonnegative. On the shrinking cone a'=S_N,b'=-S_N,
so the boundary-motion contribution is -S_N(E(b)+E(a)), as stated.

## Source, command, and packaging checks

All eight task ancestry pins match their actual bytes. The original FGF045
root overstatement remains visible and is superseded by its explicit scope
correction; the FGF046 proof respects that correction. No external source
lookup, imported existence theorem, network access, installation, service,
commit, or mathematical executable run was used.

Administrative commands read the task/contracts/pinned ancestry, wrote only
the assigned independent-audit directory, read the final author bundle, and
used Python hashlib/json to check metadata. The checks found no missing
required result fields, all embedded author input/output hashes match, and
input_sha256.json equals the embedded mapping exactly. The frozen reviewer
proof hash and all its frozen input hashes also match. These are provenance
checks, not numerical verification of PDE existence.

Both author and reviewer initially read old source text before checking its
pins. The pins all matched before author proof development and before the
reviewer freeze; no source mismatch was silently accepted. This ordering
exception is disclosed and does not change which source bytes the proofs use.

## Remaining implication and strongest safe conclusion

No missing implication was found inside the author's normalized theorem.
The strongest safe conclusion is directly constructed local positive C1
fluid evolution, locally unique on the regular causal patch, with a proved
N^-4 guaranteed lower time and a sufficient buffered higher-norm restart.
The old upper-time obstruction now applies to every admissible continuation
of this nonempty germ. It still does not force a first-gradient singularity
at an arbitrary earlier endpoint.

The smallest optional strengthening is to derive, on the needed buffered
moving domain, a bound for the spatial Lipschitz-gradient norm from specified
lower norms. That estimate and its domain bookkeeping must precede any
first-gradient endpoint classification. Coupled-field evolution remains a
separate physical obligation, because frozen fields still have C(n-rho).
No additional computation is needed to accept the presently scoped theorem.

Final proofreading self-review covered the new independent files in full:
no routine edits, no mathematical-token changes, and no unresolved notation
issues identified. The frozen derivation was preserved byte-for-byte. These
are Markdown artifacts; no LaTeX build applies.
