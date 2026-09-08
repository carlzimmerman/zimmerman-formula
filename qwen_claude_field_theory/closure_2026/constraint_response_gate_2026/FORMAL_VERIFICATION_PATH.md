# What the user-linked fluid formalizations can contribute

Checked 2026-09-08. Source question: does OpenAI's NavierStokesAndEuler
repository supply a gravity mechanism, or a useful verification method?
Classification: **adjacent verification method only**. No gravity theorem
is imported and no novelty claim depends on these sources.

The inspected repository revision was
`8937a8f4cbc7abaab5e9e97d1cc7f5d2319d9538`. Its README describes Lean
formalizations of forced Navier-Stokes breakdown and unforced Euler blowup.
Those equations, forcing classes and solution spaces are not the constrained
MOND action in this directory. The metadata labels review self-assessed.
This inspection did not install dependencies, build Lean, independently check
its full proof dependency graph, or establish acceptance of a Clay solution.
[README](https://github.com/openai/NavierStokesAndEuler/blob/8937a8f4cbc7abaab5e9e97d1cc7f5d2319d9538/README.md),
[metadata](https://github.com/openai/NavierStokesAndEuler/blob/8937a8f4cbc7abaab5e9e97d1cc7f5d2319d9538/formalization.yaml).

The directly useful pattern is separating a trusted mathematical challenge
from its proposed proof. Comparator checks the statement and permitted
axioms, with optional independent kernel checking, subject to its documented
trust and sandbox assumptions. Even its documentation warns that poorly
specified definition holes can allow formally correct but unintended answers.
This targets our actual problem: a finite toy matrix can be correct while
failing to certify the intended nonlinear field theory.
[Comparator specification](https://github.com/leanprover/comparator/blob/master/README.md),
[project checking instructions](https://github.com/openai/NavierStokesAndEuler/blob/8937a8f4cbc7abaab5e9e97d1cc7f5d2319d9538/ComparatorChallenges/README.md).

The NS reference statement explicitly includes forcing and a prescribed
solution class. That is a useful reminder to keep the exact hypotheses:
periodic is not synonymous with mean zero, a finite-time norm estimate is
not global control, and a conserved signed external stress is not automatically
healthy physical matter. Fluid blowup does not prove clock caustics or MOND
instability without a derived equivalence of the equations and admissible data.
[Reference definitions](https://github.com/openai/NavierStokesAndEuler/blob/8937a8f4cbc7abaab5e9e97d1cc7f5d2319d9538/ComparatorChallenges/NavierStokes.lean).

## An efficient next formalization target

Freeze the following mathematical challenge independently of its proof:

> For the explicit scalar quadratic action obtained from S0+DeltaS_b in
> DECISION.md on its Lambda=0 canonical stiff FLRW member, m>0 and finite K_s>=1,
> with the specified smooth compact mean-zero signed stress, spatial-decay
> inverse Laplacian and zero-past retarded boundary conditions, prove that
> the background-covariant Ward identity holds and that the orthonormal
> electric Weyl response at t=3/2, (x,y,z)=(3,0,0) is nonzero outside the
> physical metric light cone, with the displayed strict lower bound.

Four separate dependencies must remain visible:

1. Full action -> this quadratic action (already checked symbolically here;
   its nonlinear covariant/constraint completion is not thereby certified).
2. Quadratic variation -> retarded equation and reconstructed metric.
3. Compact-support Green identity and positivity -> exterior Weyl bound.
4. Signed external probe -> an admissible dynamical matter experiment
   (**OPEN**, and deliberately NOT an assumption concealed in the theorem).

The positive-Lambda member, with its different prescribed tau_Lambda(T),
also needs its own retarded calculation; no theorem about Lambda=0 alone
is silently promoted to that fixed-parameter physical theory.

Small algebraic identities can be formalized first, but they must be called
algebraic lemmas, not a formal proof of the whole gravity target. No Lean or
Lake executable was found on this task's PATH; no new unchecked Lean artifact
or installation was added merely to display a formal-proof label.

Search scope: the linked repo's README, metadata, reference statements,
checking configuration and immediate submission interfaces; Comparator's
primary documentation. No general fluid or gravity literature search, full
fluid-proof audit, or global novelty search was performed. Only this original
summary and links are retained; no third-party source cache was created.
