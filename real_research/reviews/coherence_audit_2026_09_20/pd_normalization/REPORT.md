# PD01–PD03: exact normalization audit, 2026-09-20

**Primary verdict: incomplete, with the smallest missing implication identified.**
The claim audited is that the theory's static metric channel count and the two
half-identities independently determine \(\kappa=a_0/s=1/2\), where
\(s=c\sqrt{G\rho_\Lambda}\) and \(u_\Lambda=c^2\rho_\Lambda\).
The valid response algebra has now been reconstructed and compiled in Lean.
It gives \(\kappa=1/(n\lambda)\), where \(\lambda\) is the per-channel
linear response in the already fixed vacuum units. The raw PD argument does
not derive \(\lambda=1\) or an equivalent action coefficient.

This audit starts from the raw PD scripts and original Lean file at commit
`3aaed026d55f65b38733316cb63c432290a339e1`. Those inputs match HEAD and were
unchanged. The repository was already dirty. All audit writes are in this
directory; no original source or status board was changed. No cosmological
fit, ΛCDM requirement, or external-source theorem is used in the result below.

## Exact claims and dependencies

| Step | Raw source locator | Status and exact scope |
|---|---|---|
| Vacuum units leave a response slope | `fable_independent_2026/L230_one_number.py:53–79` | Passed: \(\mu(Y)\sim bY\) and the stipulated spherical Poisson equation give \(a_0=s/b\). |
| OR response has slope equal to count | `deepseek_push/PD01_polarization_count.py:21–28,89–118` | Passed **if** \(p(Y)/Y\to1\). Generally the slope is \(n\lambda\), not \(n\). |
| Saturation forces OR composition | `deepseek_push/PD01_polarization_count.py:133–144` | Failed: the normalized mean also saturates at one. Excluding an unnormalized sum does not select OR among normalized laws. |
| The scalar metric symbol has rank two | `deepseek_push/PD01_polarization_count.py:164–224`; `PD02_polarization_count.py:55–88` | Passed for the stated static, scalar, two-potential ansatz, \(d\ge2\), and nonzero spatial frequency. |
| That rank is a count of equal, independently engaging vacuum-energy shares | `PD01_polarization_count.py:257–284,360–374`; `PD03_two_halves.py:16–20,119–138` | Not established. A response-space dimension supplies neither a kinetic quadratic form nor an energy partition nor an OR law. |
| Horizon lapse yields the half | `deepseek_push/PD03_two_halves.py:78–101` | The substitution is exact for its defined potential. Its interpretation as an exact relativistic kinetic-energy matching is not proved. |
| Equilibrium half fixes the vacuum normalization | `deepseek_push/PD03_two_halves.py:102–114` | Not addressed by this source: the equilibrium relation is restated, not derived. Even granting it for every \(a_0\), it does not determine \(a_0/s\). |
| Quarter-energy matching selects the coefficient | `deepseek_push/PD03_two_halves.py:129–138` | Conditional: this is an additional quantitative matching axiom, algebraically equivalent to \(\kappa^2=1/4\). |
| Numerical check independently validates the coefficient | `deepseek_push/PD03_two_halves.py:143–172` | Failed as independent evidence: line 150 sets `a0 = s / 2` before evaluating the identity. |

The dependency graph is therefore

\[
\text{stipulated spherical flux law}+\mu(Y)/Y\to b
\Longrightarrow a_0=s/b,
\]
\[
\text{OR law}+p(Y)/Y\to\lambda+\text{count }n
\Longrightarrow b=n\lambda
\Longrightarrow\kappa=1/(n\lambda).
\]

The count theorem supplies \(n=2\) only after identifying its mathematical
channels with the OR channels. The extra input \(\lambda=1\) remains even
after that identification is granted. Counting physical degrees of freedom,
counting scalar potential equations, and partitioning energy are distinct
operations. The audited code computes the middle one.

## A constructive counterfamily and its action

For every \(\lambda>0\), use two identical formal channels

\[
p_\lambda(Y)=\frac{\lambda Y}{1+\lambda Y},\qquad
\mu_\lambda(Y)=1-(1-p_\lambda(Y))^2
              =1-(1+\lambda Y)^{-2},\qquad Y\ge0.
\]

Both channels start at zero and saturate at one. Their OR response is
normalized, positive and monotone, and its slope is \(2\lambda\).
Consequently \(\kappa=1/(2\lambda)\). The exact rational witness
\(\lambda=2\) has two identical OR channels and \(\kappa=1/4\).
It violates only the additional unit-slope premise, demonstrating that the
other listed response properties do not entail that premise. It is not a
counterexample to the correctly stated theorem that *assumes* unit slope.
Here \(\lambda\) is dimensionless: it introduces no independent dimensionful
input beyond \(s\). Fixing the physical unit \(s\) makes the numerical
susceptibility measurable; it does not set that susceptibility to one.

Even a local variational quasistatic completion and ellipticity leave this
freedom. Put \(X=|\nabla\Phi|^2/s^2\), and define

\[
F_\lambda(Y^2)=Y^2-\frac{2}{\lambda^2}
 \left[\log(1+\lambda Y)+\frac1{1+\lambda Y}-1\right].
\]

Then \(F_\lambda(0)=0\), \(F_{\lambda,X}=\mu_\lambda\),
\(F_\lambda(Y^2)\sim(4\lambda/3)Y^3\) at the origin, and
\(F_\lambda(Y^2)/Y^2\to1\) at infinity. Varying

\[
I[\Phi]=\int\left[-\frac{s^2}{8\pi G}F_\lambda(X)
                  -\rho_b\Phi\right]d^3x
\]

with compactly supported variations gives exactly
\(\nabla\cdot(\mu_\lambda\nabla\Phi)=4\pi G\rho_b\).
The source coupling and high-gradient Newtonian coefficient are the same
for every \(\lambda\). For \(t=\lambda Y>0\), the transverse and
longitudinal eigenvalues of the flux Jacobian are

\[
\mu_\lambda=\frac{t(t+2)}{(1+t)^2}>0,\qquad
\mu_\lambda+Y\mu_\lambda'=\frac{t(t^2+3t+4)}{(1+t)^3}>0.
\]

The equation is strictly elliptic away from \(g=0\), where its expected
deep-response degeneracy occurs. These factorizations give a uniform
argument, not a finite parameter scan. The exact computation verifies the
identities and signs. An additive constant vacuum term does not constrain
\(\lambda\) in this static variational problem.

**Scope:** this is a formal two-channel response with a consistent effective
single-potential action. It is not a covariant two-field or metric completion,
does not derive a vacuum stress tensor, and does not prove full-theory health.
It decisively shows that OR algebra, normalization, local action existence,
and quasistatic ellipticity are insufficient to select the coefficient.
The physical bridge between the two-potential carrier and the response law
still has to be supplied by the theory.

## What the geometric and half arguments establish

Directly tracing the linearized Ricci tensor gives

\[
R_{00}=\Delta\Phi,\quad
\delta^{ij}R_{ij}=2(d-1)\Delta\Psi-\Delta\Phi,
\]
\[
G_{00}=(d-1)\Delta\Psi,\qquad
G_{kk}=(d-1)\Delta[\Phi-(d-2)\Psi].
\]

In coordinates \((\Delta\Psi,\Delta(\Phi-\Psi))\), the coefficient
matrix is

\[
M_d=\begin{pmatrix}d-1&0\\(d-1)(3-d)&d-1\end{pmatrix},
\qquad\det M_d=(d-1)^2.
\]

This proves the scalar-symbol result for all integers \(d\ge2\); it fails
at \(d=1\), where the matrix vanishes. Boundary conditions and zero modes
are separate from this symbol rank. No radial assumption is needed for
the trace formulas. PD01's comment at lines 169–172 about an off-diagonal
sum entering a general-field trace is incorrect: contraction with
\(\delta^{ij}\) already removes off-diagonal terms.

PD02's executable formulas at lines 84–88 are correct. Its docstring
lines 12–25 and concluding text at lines 188–201 retain incompatible earlier
coefficients. At \(d=2\), its header predicts \(G_{00}=3\Delta\Psi/2\)
instead of \(\Delta\Psi\). The code's unique vanishing of the
\(\Psi\)-coefficient at \(d=3\) is correct in the chosen slip basis;
it is not invariant diagonalizability. The change of basis
\(q=\Phi-(d-2)\Psi\) diagonalizes the two displayed equations for every
\(d\ge2\).

Ordinary spatial parity sends each of the two scalar potentials to itself
at the reflected point. It does not exchange them. Thus the positive
quadratic form \(K=\operatorname{diag}(1,4)\) is parity invariant and has
unequal weights. Even imposing an actual channel-exchange symmetry permits
\(K=\left(\begin{smallmatrix}A&B\\B&A\end{smallmatrix}\right)\), with
an undetermined overall coefficient. Rank and parity cannot fix the
normalization used by PD03.

For the lapse convention \(f(r)=1+2\Phi(r)/c^2=1-r^2/R^2\),
\(\Phi(R)=-c^2/2\) follows from \(f(R)=0\). This is an exact metric
identity. The source then uses the nonrelativistic expression \(mv^2/2\)
at \(v=c\) to interpret it, without deriving a relativistic energy or a
matching action. That interpretation supplies no additional equation for
\(a_0\). Likewise, granting \(\sigma^2=\sqrt{GM_ba_0}/2\) leaves
\(a_0\) arbitrary: for any positive \(a_0\), the right-hand side defines
the corresponding \(\sigma^2\).

The precise normalization issue in PD03 can be displayed without disputing
either half. If the action-to-energy conversion is
\(\eta a_0^2/G\) and the recruited vacuum fraction is \(f\chi\), then

\[
\eta a_0^2/G=f\chi u_\Lambda
\quad\Longleftrightarrow\quad
\kappa^2=f\chi/\eta.
\]

PD03 sets \(f=\chi=1/2\) and \(\eta=1\). A coefficient fixed by a
derived action would be new information; a selected matching condition is
a new axiom. With \(s^2=Gu_\Lambda\), its actual condition satisfies

\[
a_0^2/G=u_\Lambda/4\quad\Longleftrightarrow\quad\kappa^2=1/4,
\]

now certified in Lean. Positivity then gives \(\kappa=1/2\). This is a
legitimate conditional model definition, but the algebraic rewriting alone
does not eliminate the unexplained dimensionless input. The two routes
also do not share a count-dependent law: unit-rate OR gives \(1/n\),
whereas a one-of-\(n\) kinetic-half energy rule gives \(1/\sqrt{2n}\).
They agree at \(n=2\); agreement there is not proof of a common mechanism.

## Verification, provenance, and concrete progress

The bounded exact run verified **20 exact identities**, including the
all-dimension symbol, counterfamily, action derivative and ellipticity
factorizations. The AST audit found literal `True` as the tested condition
in 8/17 PD01 checks, 2/6 PD02 checks, and 9/12 PD03 checks. These include
many interpretive steps; their PASS counts do not certify those steps.

The original `PD02_channel_count.lean` fails compilation in the installed
Lean 4.34.0-rc2 environment. Its failures include a mathematical locality
issue: \(Y\ne0\) does not imply \(1+Y\ne0\) (original line 115).
The replacement handles denominator nonvanishing *eventually near zero*.
`PDNormalization.lean` compiles with the original five mathematical results
reconstructed, plus:

- `or_slope_general`: the universal slope is \(n\lambda\);
- `rate_family_slope`: rational channels realize each real slope;
- `two_channels_need_not_have_slope_two`: the explicit two-channel rate-2
  response cannot have slope 2;
- `kappa_normalization`: the free rate survives MOND matching;
- `quarter_matching_iff`: the exact PD03 matching equivalence.

The printed theorem dependencies contain only `propext`, `Classical.choice`,
and `Quot.sound`, with no `sorryAx`. Compiler logs retain harmless tactic
suggestions; there are no compilation errors in the reconstruction.

Reproducibility records are `exact_run/manifest.json` and
`lean_run/manifest.json`. They pin source and execution hashes before and
after, base commit, dirty state, actual command, versions, elapsed times,
limits, and result hashes. The Python run has a 30-second wall limit; the
Lean verification has a 90-second wall limit and per-compilation 50-second
limits. No randomness is used. Cooperative library thread cap: one.
The pinned Lake manifest records Mathlib's dependency revision; every
installed compiled dependency is not individually hashed.

Direct regeneration commands from the repository root are:

```sh
python3 real_research/reviews/coherence_audit_2026_09_20/pd_normalization/check_pd_normalization.py real_research/reviews/coherence_audit_2026_09_20/pd_normalization/recheck.json
```

From `fable_independent_2026/lean_2026`, compile with:

```sh
lake env lean ../../real_research/reviews/coherence_audit_2026_09_20/pd_normalization/PDNormalization.lean
```

The strongest next step is now narrow and testable: derive the response
from a specified action with matter coupling and vacuum normalization
already fixed, then calculate \(\lim_{Y\to0^+}p(Y)/Y\). Under the OR
identification, proving that quantity equals one closes this coefficient
gap. Proving another value makes a different prediction. Neither an
additional channel recount nor another substitution of \(a_0=s/2\)
addresses it. No claim of full theory closure or global novelty follows
from the present bounded result.
