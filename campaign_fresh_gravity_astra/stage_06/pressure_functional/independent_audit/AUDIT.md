# Independent audit of PF1

Worker: `/root/proof_precision`, actual Astra agent. Review date: 2026-09-27.
Only the new candidate `DERIVATION.md` and `ancestry.json` were read for this
assignment. The candidate's actual SHA256 matches its ancestry record:
`102dee0743c300c38781846828a38a72e52701be648dd39931f0d2b332676cd1`.
The earlier campaign, FGF-019 and FGF-020 narratives are not proof premises and
were not consulted. No literature search, numerical experiment or rank test
was performed. This is an independent exact proof reconstruction, not a
duplicate scientific run or an acceptance of an actual instrument model.

**Primary verdict: proved as written**, under the explicitly declared
nonnegative-profile and off-target-rank assumptions, with the mathematical
typing made precise below. No counterexample was found to that conditional
lemma. The result does not by itself establish globally strictly positive
profiles when the baseline has unchanged zeros, and does not establish that
any real pressure map satisfies the kernel or rank premises.

## 1. Normalized claim and hypotheses

Let I be the finite radial interval, x0 an interior point, and m finite.
The observations are real linear functionals

    L_i(p)=integral_I K_i(x)p(x)dx.

These integrals must be well-defined for p0. Kernels are measurable, with
finite uniform essential bounds on a fixed neighborhood U of x0 and on the
selected compensation supports. This is the usual meaning of the candidate's
bounded-kernel integral model; boundedness does not mean that a bound may
diverge as the support shrinks. No assertion is needed about a kernel's
irrelevant point values on a measure-zero set.

The baseline p0 is smooth, p0>=0 on I, and is bounded below by positive
constants eta_U and eta_J on U and on the compact off-target set J. The
distance from J to x0 is positive. Interpret smooth test functions supported
in J as ambient smooth functions with compact support contained in J
(or in its interior under the usual C_c^infinity notation). Define their
linear space X_J. If J has no nonzero such test functions, the independence
assumption cannot hold for m>=1. Thus the phrase “compact J” presents a
notation issue to specify, not an unproved source of test functions.

The exact rank premise is independence of L_1,...,L_m restricted to X_J.
It implies independence of the whole observation list, but the converse need
not hold. Independence near x0 and independence on J are generally
incomparable: neither implies the other. A globally dependent list may first
be reduced, but that operation alone does not establish independence on J.

The conclusion is that there are smooth nonnegative p_delta with identical
L_i values, p_delta→p0 uniformly, and p_delta'(x0) tending to either infinity
or minus infinity, according to a fixed chosen sign. The profiles are strictly
positive on the supports where they change. If p0 is globally strictly
positive, then every sufficiently small p_delta is also globally strictly
positive. With a baseline zero elsewhere, that zero persists.

## 2. Reconstruct the functional-rank step

Define T:X_J→R^m by T(h)=(L_1(h),...,L_m(h)). Its image is a linear subspace.
If image(T) were proper, finite-dimensional linear algebra supplies a nonzero
row vector w with w dot T(h)=0 for every h in X_J. Equivalently,

    sum_i w_i (L_i restricted to X_J)=0,

contradicting the stated independence. Therefore T is onto R^m. Choose h_j
with T(h_j)=e_j. This even permits an identity compensation matrix; choosing
any basis of measurement vectors instead gives the candidate's invertible A.
No approximation, numerical singular-value cutoff, completeness theorem,
or infinite-dimensional inverse-function theorem is needed.

Signed h_j are allowed. Requiring h_j>=0 would be an additional restriction
and is not supplied by independence. The candidate correctly does not require
it. The selected finite family has bounded sup norms because its members are
smooth with compact support. The inverse A is fixed before delta varies.
An ill-conditioned A can make the constants very large, but cannot destroy
the existence statement as delta→0. It matters greatly for a finite-resolution
or noisy application and is not quantified by this exact rank premise.

## 3. Independent local construction and all exponents

A concrete permitted bump is

    phi(t)=e t exp[-1/(1-4t²)] for |t|<1/2, and 0 otherwise.

It is smooth, its support [-1/2,1/2] is compactly contained in (-1,1),
and phi'(0)=1. Fix any 0<alpha<1 and
finite b≠0, independent of delta. Choose delta small enough that
[x0-delta,x0+delta] lies in U and misses J. Let

    u_delta=b delta^alpha phi((x-x0)/delta),
    v(delta)=T_local(u_delta)=(L_i(u_delta))_i,
    c(delta)=A^(-1)v(delta),
    p_delta=p0+u_delta-sum_j c_j(delta)h_j.

Here T_local merely denotes the same observation vector applied to the local
bump; it is not restricted to X_J. The two support regions are disjoint.
Changing variables x=x0+delta t gives, with fixed M_i=ess sup_U |K_i|,

    |v_i(delta)| <= |b| M_i ||phi||_1 delta^(alpha+1).    (A1)

The extra factor delta is the integration Jacobian, not a derivative factor.
With any fixed compatible finite-dimensional norm,

    ||c(delta)|| <= ||A^(-1)|| ||v(delta)||
                    = O(delta^(alpha+1)),
    ||sum_j c_j h_j||_infinity = O(delta^(alpha+1)).       (A2)

Meanwhile ||u_delta||_infinity=|b| ||phi||_infinity delta^alpha.
Thus ||p_delta-p0||_infinity=O(delta^alpha), and linearity gives exactly

    L(p_delta)-L(p0)=v-Ac=0.                              (A3)

No approximate cancellation is being promoted to equality.

For positivity, choose delta so that
|b| ||phi||_infinity delta^alpha<eta_U/2 and the compensation sup norm is
less than eta_J/2. Then p_delta>=eta_U/2 on the local changed support and
p_delta>=eta_J/2 on the compensation support. Everywhere else p_delta=p0>=0.
The smoothness follows from finite sums and a smooth rescaled compact bump.
There is no uniform bound on its higher derivatives, and none is assumed.

Since the h_j vanish in an entire neighborhood of x0,

    p_delta'(x0)-p0'(x0)=b delta^(alpha-1).                (A4)

The exponent is negative. This diverges to +infinity for b>0 and to
−infinity for b<0. Positivity does not restrict either sign once delta is
sufficiently small. The exponents are mutually compatible: for instance,
alpha=1/2 and delta_n=n^(-2) give a derivative change b n, local sup change
O(n^(-1)), and compensation/measurement change O(n^(-3)). This is an exact
sequence description, not a numerical test.

Thus the candidate's rank, positivity, uniform-convergence and derivative
claims all follow. The first implication requiring an external physical
input is applicability of the observation model and allowed profile class.

## 4. Finite-tolerance variant

Without any rank premise, keep only p_delta=p0+u_delta. The same local
positivity argument works, and (A1) implies that, for each fixed epsilon_i>0,
eventually

    |L_i(p_delta)-L_i(p0)|<epsilon_i for every i.

Because m is finite, one delta can satisfy all inequalities. Derivative
divergence and uniform convergence are unchanged. This proves the finite-box
claim without a covariance model. More generally it works for any acceptance
region containing an open neighborhood of L(p0), but no such extension is
needed for the candidate statement.

“Positive fixed error box around the baseline” is important: zero-width
coordinates are exact constraints, one-sided regions may place the baseline
on their boundary, and tolerances shrinking with delta require a separate
rate comparison. The stated proof does not cover those cases. It likewise
does not cover a measurement family or beam resolution that changes as delta
shrinks. None of these variants refutes the candidate's fixed finite box.

## 5. Counterexample attempts and limits of necessity

**Dropping off-target rank breaks this compensation construction.** Take
I=(-2,2), x0=0, J contained in (1,3/2), p0=1, and one bounded kernel
K=1 on (-1/2,1/2) and zero on J. Every compensation function supported in J
has zero measurement. Choose instead a smooth bump phi=(1+t)theta(t), where
theta is even, nonnegative, supported in (-1,1), and theta(0)=1. Then
phi'(0)=1 and integral phi>0. Its local observation change is nonzero for
b≠0, so no J-supported compensation can cancel it. This shows why the
candidate needs its stated rank premise for its chosen construction. It does
not prove that exact non-identification is impossible without that premise:
the odd bump in section 3 has zero integral in this particular example.
The premise is sufficient, not claimed necessary for every possible method.

**Global strict positivity is not automatic.** A baseline may be positive on
U and J but vanish on an untouched open subinterval. Every constructed
p_delta has that same zero. This refutes only the shorthand claim of globally
strict positivity from the weaker p0>=0 hypothesis, not the candidate's
explicit “nonnegative” conclusion. Add global p0>0 if that stronger wording
is intended; a global positive lower bound is unnecessary because changes
occur only on the two already controlled supports.

**The allowed observation class matters.** If an exact observation is the
derivative itself, L(p)=p'(x0), no such derivative-changing exact null family
can exist. That distributional functional is not an integral against a
bounded ordinary kernel and lies outside PF1. This is a scope counterexample
to replacing the finite bounded-kernel premise with arbitrary finite linear
measurements, not a counterexample to PF1.

No tested counterexample satisfies all normalized PF1 premises. There are
no failed computational attempts: the checks here are exact arguments and
explicit counterexamples to deliberately altered premises.

## 6. What a real map application still needs

The conditional theorem requires authenticating all of the following for the
same physical perturbations:

* The actual measured quantities must be finitely many fixed linear pressure
  functionals, with units, projection, beam, annulus weights, mask and any
  additive backgrounds represented consistently. A reconstructed pressure
  profile produced by an inversion with priors is not automatically the raw
  observation operator.
* Kernel bounds must hold on the local and compensation supports. The text
  correctly excludes unaudited raw tangent singularities. An integrable
  singular kernel would need a different estimate; failure of the bounded-
  kernel premise is not by itself proof of derivative identification.
* Off-target rank must hold for the full retained measurement vector on a
  region where the baseline pressure has a positive margin. Global rank,
  finite-bin rank or near-target rank alone does not establish it. Finite
  numerical ranks also need a tolerance/conditioning interpretation.
* The perturbations must remain in the physically admissible class. The proof
  provides no uniform gradient/curvature bound, equilibrium equation, same
  X-ray signal, monotonicity requirement, boundary flux, composition or
  electron-to-total pressure conversion. Any independently justified extra
  restrictions must be imposed jointly before drawing an observational result.

The target is a point derivative. A fixed-resolution averaged gradient is a
different functional; it cannot silently inherit the unbounded pointwise
claim. Likewise monotonicity or another named restriction does not by itself
prove a finite derivative bound: one must show that the actual restricted
class excludes the relevant construction or satisfies a quantitative bound.

Restoration by P_*/L_* rescales the derivative but does not supply physical
admissibility. The Q/R/M and two a-normalization bridge in the candidate is
properly conditional; no step of this functional proof selects a gravity law,
provides hydrostatic consistency or tests the user's filtered-MONO framework.

## 7. Obligation matrix, remaining gap and provenance

| Obligation | Audit result |
|---|---|
| Independence on J implies a fixed invertible measurement matrix | passed, exact finite-dimensional annihilator argument |
| Test functions exist on the specified support | conditional exactly on stated functional independence and an explicit test-space interpretation |
| Local observation exponent alpha+1 | passed under fixed local kernel bound and measurable integrals |
| Compensation exponent alpha+1 | passed because A and h_j are fixed, finite and bounded |
| Uniform convergence and support-wise strict positivity | passed; global nonnegativity retained |
| Global strict positivity from merely nonnegative baseline | not implied; counterexample given |
| Point derivative exponent alpha−1 and either sign | passed for fixed b≠0 and 0<alpha<1 |
| Finite positive tolerance without rank | passed for a fixed box centered at the baseline with every width positive |
| Actual beam/map kernels, rank and admissibility | not addressed by available candidate evidence |
| Gravity-theory exclusion or complete pressure explanation | out of scope |

The smallest remaining implication is authentication of the real observation
operator and its off-target rank on an admissible positive-pressure support.
The next discriminating check is to compare the actual finite operator's
restricted response space with the desired point or finite-resolution
gradient, retaining extra spatial/boundary modes and independently justified
regularity constraints. A full-rank chosen finite basis alone does not defeat
this continuum conditional proof.

This is proof-only evidence. Source-byte verification and artifact generation
were performed, but no numerical experiment, measured rank, tolerance scan,
CAS proof or computation manifest is claimed. Exact source and output hashes
and actual proof-only metadata are supplied in `result.json`. The ancestry
links establish the candidate's recorded origin, not audited truth of its
earlier scientific parents. The review is attached to PF1 and makes no theory-
completion claim.
