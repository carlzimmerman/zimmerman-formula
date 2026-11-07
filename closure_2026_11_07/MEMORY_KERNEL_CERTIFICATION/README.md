# Memory-kernel and remaining-gap certification, 2026-11-07

**Premise update, 2026-11-07:** the numerical web thresholds inherited from SV5/FA3 require the Limber-kernel reread. The integral theorems and counterexamples remain valid. See the [latest certification](../LEAN_LATEST_CERTIFICATION/README.md) for the premise hold.

**The unrestricted positive-kernel comparison across epochs is refuted.**
Positivity alone does not relate a web response at an earlier cosmic time to
host response today. Continuous integral comparisons are proved under explicit
source-ordering assumptions; the cross-epoch bound is proved for nonincreasing
kernels. EW2's normalized H-inf analytic chain is also proved. This is a
self-review of mathematical statements, not an observational regrade or a
certification of the full covariant theory. Kappa = 1/2 FITTED; not theory closed.

Base checkpoint: `cca79181a44a551ab359a62e3b2a021ceacecec1`. Inputs are FA3's
`FROZEN_CRITERIA.md`, `fa3.py`, `fa3.json`, `fa3.out`, `RESULT.md`, EW2's README
section 5, and SV1's Lean shell-bound statement. Exact hashes before and after
verification are recorded in `verification.json`. No original lane result,
frozen criterion, paper, or physical label is changed by this follow-up.

## 1. Memory: the claim and its obstruction

FA3 defines memory by a causal lag integral

```
M_k[W](t) = integral from 0 to t of k(s) W(t-s) ds.
```

It grades hosts at today's age T, while the web is evaluated at earlier ages t.
The frozen script reports T = 14.0656 Gyr and, for the latest web epoch z=0.25,
t = 10.916 Gyr, about 0.776 T. Positivity gives no lower bound on
`integral_0^t k / integral_0^T k`: a kernel can put most of its mass after t.
Even exact source alignment and constant source magnitudes do not fix this.

`DelayedKernel.lean` supplies a fully normalized counterexample. With today's
age normalized to 1, set

```
k_delay(s) = 100 max(0, min(s - 4/5, 1 - s)),
k_positive(s) = (999/1000) k_delay(s) + (1/1000) exp(-s).
```

Lean proves that k_positive is continuous, strictly positive, integrable on
positive lags, and has total causal mass 1. Its mass by today is at least
0.999, but its mass by age 0.8 is at most 0.001. Thus constant aligned source
histories have host response above 0.816 and early response below 0.005.
The delayed component alone contributes exactly zero up to age 0.8, for
**any scalar or vector source history**, not just a constant one.

This refutes the comparison asserted for arbitrary positive kernels from the
recorded premises. It does not establish a new candidate passing W1 or any
other observational gate. The exponential-family numerical FAIL remains a
numerical result in FA3's record; nothing here changes that label.

## 2. What survives for continuous kernels

`MemoryKernel.lean` proves, over arbitrary measure spaces:

* Nonnegative shared weights preserve an almost-everywhere source ordering
  `web(s) >= c host(s)`, provided the weighted sources are integrable.
* A bounded scalar or vector source bounds its memory response by the source
  cap times the kernel's mass.
* A lower bound on projection onto a fixed unit vector bounds the norm of
  the vector integral from below. A magnitude-only comparison is insufficient:
  opposite directions can cancel. The file includes a two-atom counterexample.
* For a kernel nonincreasing on [0,T], with 0 < t <= T,
  `t integral_0^T k <= T integral_0^t k`. With k nonnegative and t >= 3T/4,
  the earlier mass is at least three quarters of today's mass.
* The exponential relaxation kernel is nonincreasing. A continuous-kernel
  gate theorem composes the age bound with explicitly supplied response
  inequalities: `0.033 host <= mass_today`, `mass_early <= web`,
  `host >= 0.816`, and `web <= 0.005` are incompatible.

Integrability, common kernel, epoch comparison, and directional projection are
part of the theorem statements. The measure can be restricted to a causal lag
interval. No continuity of a general kernel is needed for the order theorem;
its explicit integrability hypotheses are the relevant condition.

FA3 stores mass-weighted mean cosines and magnitude ratios, not uniform
pointwise projection certificates. A mean cosine near 1 is not a pointwise
lower bound in the direction required by the vector theorem. The present
proof does not promote those summaries into that missing hypothesis. The
unrestricted cross-epoch route is closed by counterexample; the decreasing-
kernel route remains conditional on the actual source projection bounds.

## 3. H-inf: the integral gap

`HInf.lean` proves the analytic chain on the normalized radial interval [1/2,1].
For a continuous potential f whose derivative is at least s >= 0,

```
s/128 <= integral from 1/2 to 1 of |f(u)| u^2 du.
```

The proof splits at u=3/4. The sign there selects a quarter-interval on which
|f| has a linear lower bound. It does not assume that f crosses zero inside
the interval.

For a monotone potential, Lean also proves the missing absolute-variation
step: if signed weighted integrals are increments of D and |D| <= delta,
the weighted absolute integral is at most 4 delta. The proof handles potentials
of one sign separately and uses the intermediate value theorem only in the
crossing case. A small signed integral alone would not justify this step.

The final theorem `normalized_Hinf_of_mass_derivative` assumes

```
f'(u) >= 1-eps,    |D(u)| <= delta,
D'(u) = (mu R)^2 f(u) u^2,    eps < 1, delta >= 0,
```

with the continuity and differentiability stated in Lean. It proves

```
(mu R)^2 <= 512 delta / (1-eps).
```

The primitive relation follows by the fundamental theorem of calculus rather
than being assumed as an integral identity in this final theorem.

`LawBand.lean` proves the adjacent simple-mu algebra. With
`m_a(g) = g^2/(a+g)`, a>0, reference>0, and 0<=eps<1, a field in
`[(1-eps) reference, (1+eps) reference]` satisfies
`|m_a(g)/m_a(reference)-1| <= 2eps+eps^2`. It also proves the phantom cap
`0 <= g-m_a(g) < a` for g>=0.

For R>0, G>0 and constant M_b>0, the physical dictionary is
u=r/R, f(u)=R Phi(Ru)/(G M_b), and
D(u)=-(M_eff(Ru)-M_b)/M_b. The sign in D gives the positive derivative used
in the formal theorem. The spherical static mass equation and constant M_b
supply that equation; the field error band supplies delta. Applying the
certificate to numerical solver outputs still requires those physical
identifications and hypotheses. The dimensional change of variables and the
full field equations are not formalized here. No numerical approximation to
eps=10^0.05-1 or the quoted 12.3 bound is newly certified.

## 4. Signed-shell scope

`SignedShell.lean` proves an exact rational obstruction to extending SV1's
finite-sum algebra to inward radial components. For a=1, weights 0.99 and
0.01 and radial fields 1 and -50, the mean is 0.49, the signed flux is positive,
and `flux < mean^2/(1+mean)`. This reverses the inequality needed by that
extension. The witness obeys G=|g| but is not a constructed solution of the
AQUAL PDE. SV1's existing theorem with nonnegative radial components remains
unchanged; a source-realizability theorem is a separate obligation.

## 5. Coverage, verification and next obligations

| Obligation | Result |
|---|---|
| Continuous positive-kernel order comparison | Proved under explicit integrability and source ordering |
| Vector cancellation control | Proved under a directional cone hypothesis; magnitude-only route refuted |
| Arbitrary positive kernels across unequal ages | Refuted, including normalized strictly positive integrable kernels |
| Decreasing kernels / exponential relaxation across ages | Age theorem proved; physical projection inputs remain conditional |
| H-inf lower integral, absolute variation, FTC, coefficient 512 | Proved in normalized variables under the stated first-order equations |
| Simple-mu mass band and source cap | Proved for the stated positive domain |
| Signed extension of finite-shell algebra | Refuted; physical PDE realizability not settled |
| Full covariant variations, numerical convergence, all-scale empirical bounds | Not addressed by these proofs |

The five files contain 48 newly kernel-checked theorems. Printed axiom lists
must contain only `propext`, `Classical.choice`, and `Quot.sound`. The
counterexamples are proved propositions, not failed proof attempts. The
previous 107-theorem certificate is preserved; this verifier checks that all
of its source hashes remain unchanged without recompiling them.

Reproduce with a built dependency tree in this repository:

```sh
python3 closure_2026_11_07/MEMORY_KERNEL_CERTIFICATION/verify.py
```

Or pass `--library-project /absolute/path/to/matching/lean_2026` to reuse a
prebuilt Mathlib tree. The verifier requires identical toolchain and dependency
manifest hashes, checks every expected theorem's axiom report, and records
source/log hashes. Numerical and historical source files are hashed for
provenance; they are not rerun or promoted to exact physical theorems.

Continuation checkpoint: obtain spatially pointwise projections (with error
bounds) for the actual web histories if the decreasing-kernel physical
exclusion is needed; otherwise do not assert that universal result. For H-inf,
formalize the physical normalization and its derivation from the spherical
static equations before calling the entire action-to-bound chain certified.
Full covariant calculus and empirical all-scale coverage remain separate open
routes. No manuscript integration or adoption is implied.

Self-proofreading covered the new Lean files and this report. Existing claims
were left intact, with the earlier gap report linked to this continuation.
