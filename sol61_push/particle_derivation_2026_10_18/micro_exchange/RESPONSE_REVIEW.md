# Focused independent audit of the response derivation

Scope: `../micro_response/DERIVATION.md` section 1 threshold contact and
gravitational susceptibility, sections 2–3 static host response/operator
comparison, and sections 4–5 critical three-body branch, scale window and
baryon phase source. The separate nodal-ring branch and the whole research
program are outside this review. No response-lane file was edited by this
reviewer. Main `MICRO_EXCHANGE.md` is preserved unchanged.

Initial audited response SHA-256:
`5cf4501ab0bf58f2e32838fea79ab9df74a05b41fba686e3599ebd2052bad39d`.

Normalized claim: the specified scalar actions yield the displayed stable
finite-density compressibility in their stated regimes. Changing the
separate host quartic to lambda=2 yields a positive three-body interaction
and a fractional-power phase pressure on its allowed density branch; it
does not supply the required gradient branch or a direct baryon phase
source while retaining the original source-free charge current.

Initial primary verdict: **correct only after a stated restriction**. The
main formulas pass; the literal claim that the *exact relativistic*
positive-density branch requires `X_NR>0` must instead read `S>0`. The
positive-X statement is exact for the leading NR constrained Legendre
problem, and is inherited by the full theory only where the omitted
relativistic corrections are small relative to the retained X invariant.

The smallest explicit counterexample to unqualified exact-X wording is a
flat metric, positive small coordinate detuning mu, and constant phase
gradient obeying

\[
 |\nabla\pi|^2=2m\mu+\frac{\mu^2}{2},\qquad
 X_{\rm NR}=\mu-\frac{|\nabla\pi|^2}{2m}
          =-\frac{\mu^2}{4m}<0,
\]

whereas

\[
 S=(m+\mu)^2-|\nabla\pi|^2-m^2=\frac{\mu^2}{2}>0.
\]

For mu sufficiently small relative to m and M this is a valid positive
density of the exact tuned polynomial model. It occupies a narrow
cancellation region: the discarded term `mu^2/(2m)` is comparable to
`X_NR`. Thus it does not rescue a controlled, gradient-dominated negative-X
MOND branch. The additional ordering is that the omitted relativistic
terms in S are much smaller than `m|X_NR|`, whenever an X-sign conclusion
is drawn from the leading NR action. This restriction supplements the
small individual frequency/gradient ratios; cancellation must be checked.

Independent reconstruction and obligation matrix:

| Obligation | Check and status |
|---|---|
| Threshold/RWA distinction | Passed: the negative-frequency source term is `delta k=-g_c^2/[8m^2 M(M+2m)]`; the complete threshold contact is `g2=lambda_rep/(2m^2)` |
| NR density susceptibility | Passed at positive dilute n0 with the stated source/detuning elimination and Born contact regime: differentiating the quantum-pressure chemical potential gives `m^2/[g2+k^2/(4mn0)]` |
| Jeans closure | Passed: Poisson substitution gives the displayed denominator and its unstable long-wave limit; no stable infinite homogeneous k→0 limit is inferred |
| Canonical host lapse response | Passed: the fixed-coordinate-frequency lapse action gives explicit `2 omega^2 I` plus `q^T K^-1 q`; including the seagull recovers `(rho+p)/cs^2` |
| Host phase/amplitude gaps | Passed: the determinant at k=0 has one Goldstone root and amplitude eigenvalues of `[[A+4omega^2,B],[B,D]]`; static Hessian eigenvalues alone are not the gaps |
| Material P operator | Passed: `P_L=-ik delta rho/k^2` converts finite compressibility to a k² restoring kernel, rather than a local constant P² tether; this is a nonlocal density representation |
| Analytic cubic obstruction | Passed at tree level on the specified isotropic, unpolarized, nonsingular static-amplitude branch; no all-loop/gapless exclusion is claimed |
| Tuned mediator expansion | Passed: independent cubic stationarity expansion gives `chi=-2I/M+3I²/(2M³)+23I³/(4M⁵)` and `Veff=m²I+epsilon I²+I³/M²+23I⁴/(8M⁴)` |
| Exact density branch | Passed for S: U'' is strictly positive; stationarity forces chi=-x≤0; I(x) is increasing and `S(x)=3x²/4+2x³/M>0` for x>0 |
| NR three-body coefficient and pressure | Passed for the controlled truncation: `g3=3/(8m³M²)` and the constrained maximum over n≥0 gives `P=2X^(3/2)/(3sqrt(g3))` for X>0 and vacuum for X≤0 |
| Residual quartic | Passed: coexistence `nt=-3g2/(4g3)`, `Xt=-3g2²/(16g3)` and spinodal `ns=-g2/(2g3)`, `Xs=-g2²/(4g3)` are correct in the NR truncation |
| Three-body scale window | Passed with the extra noncancellation qualification above: `I≫(2/3)|epsilon|M²` suppresses quartic chemical potential, `I≪min(M²,mM)` controls mediator/NR density scales, `k²≪8mX` suppresses quantum pressure |
| Original attractive branch | Passed as a diagnostic, not a controlled precision value: original epsilon=-m/M gives NR coexistence `I=mM/2`, `X=-m/8`, so increasing M/m alone does not produce a parametric NR limit |
| Baryon Ward obstruction | Passed: for the phase convention used, `-g_b pi rho_b` gives `-dot n+div(n grad pi/m)=g_b rho_b`; this is a source for the original charge current, which cannot remain a source-free two-form dual without a compensating sector |
| Conserved-current derivative coupling | Passed for the displayed coupling: integration by parts makes a conserved stationary baryon current supply no local phase source; general shift-invariant metric couplings remain outside that restriction |

Two notation clarifications were sent to the author alongside the physical
restriction. Section 3's `K_g W'_rem` is correct if prime means d/du; for
`p=|P|` the derivative is instead `W_rem,p=u²/(a0-u)`. The derivative variable
should be explicit. The gas formula is correct with F a number density in
velocity space and E=v²/2+Phi_N the *specific* energy; using total particle
energy adds a mass in the chain rule. Neither clarification changes the core
response or branch results.

The label “spacelike” should not be inferred just from `X_NR<0`: the full
massive phase covector may still be timelike with squared frequency norm
between zero and m². The actual obstruction concerns S<0 positive density
and the controlled gradient-dominated negative-X_NR branch.

Evidence: read `../micro_response/check_response.py` and the run-002 output;
the finite assertions match the corresponding Hessians, source, determinant
and critical-branch formulas. Executed the documented runner-v2 validator
for `../micro_response/run_002/manifest.json` at the repository root; result
was `valid evidence record (run status: completed)`. The four finite host
masses/five momenta do not certify all states. No repeat numerical experiment
was required. External primary-paper attribution was not independently
re-authenticated in this focused internal proof audit.

Provenance: separate reviewer from the response author, with shared model
and project context. The displayed phase, thermodynamic, branch and source
algebra was independently reconstructed. The author was sent the explicit
counterexample and minimal scope corrections. This does not constitute an
independent full-theory review or observational evidence.

## Final correction checked

The author preserved the initial bytes as `DERIVATION_PRE_REVIEW.md`; its
SHA-256 matches the initial audited hash above. The intermediate correction
had SHA-256
`01f7dc68a5bd1093e9d63d63cc5c234e5ec1ff4d5deac4f30c7eedeb5ea7e828`.
The final checked response note is SHA-256
`2ba9a12c97fc2c3d237bbb963b22486ff0ad066fafd3404b6d35063d290423c8`.

Re-read the changed summary, gas convention, W derivative, exact-S branch
and NR remainder paragraphs, plus the branch conclusion in section 5.
The explicit counterexample is retained. The text now requires
`|S-2mX_NR|≪2m|X_NR|` for the leading-X sign test, states the stationary
phase assumption when writing the remainder as `mu_NR²`, and gives the
generic time-dependent replacement. It also distinguishes the required
gradient-dominated negative-X regime from the causal type of the full
massive phase covector. Both notation clarifications are present.

Final normalized-claim verdict: **proved as written**, within the stated
coherent-background, static-probe, contact/detuning, dilute/NR and
nonsingular or explicitly tuned-critical domains. No remaining actionable
correctness issue was found in this assigned scope. This pass supports the
explicit susceptibility and restricted critical construction and their
obstruction conclusions; it does not establish a full theory, a formation
state or a matched baryonic fifth force. No new numerical result is inferred
from these prose/domain corrections; prior code and evidence were unchanged.
