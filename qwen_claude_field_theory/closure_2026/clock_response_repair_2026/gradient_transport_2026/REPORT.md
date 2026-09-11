# A spatial clock gradient requires a transport budget

Base a91f22e94. Full relativistic MOND closure remains **OPEN**. This is a
necessary-current calculation for the same reconstructed action, not a solved
galaxy, a new phenomenological force law, or an observational exclusion.

## Exact action and scope

Retain the previous covariant gravitational density

\[
\sqrt{-g}\{M^2(\mathcal R-2\Lambda)/2+P(X,\tau)+sW(Y,\tau)
 -V(\tau)+\gamma X\Box\chi\}.
\]

Here s=sqrt(-grad(tau)^2), n=-grad(tau)/s, Q=n.grad(chi),
X=-grad(chi)^2, Y=Q^2-X. At a fixed cosmological time,

\[
P=-\frac U2\log\frac{U-2dX}{U-2dq^2}+3\gamma qH(X-q^2),
\quad W=U+2d\ell(\sqrt{1+Y/\ell}-1)-2\gamma q^2\dot q,
\quad V=U.
\]

The background functions are the same imported ones; no coefficient is fitted
here. Define B=U/(2d)=q^2(1+m) and ell=q^2 m/2. In particular
P_X=P_X0+3 gamma q H, with P_X0=d B/(B-X), and
W_Y=d/sqrt(1+Y/ell). This use of B is not the earlier scalar kinetic Bhat.

Use zero shift and retain general radial metric A,R. At the instant under
investigation assume chi_t=q is spatially uniform, giving Q=q/N and Q_r=-Q N_r/N.
This is a restriction on the branch, not a gauge identity. The metric, matter
constraints and long-time evolution have not been solved in this package.

## The current is derived, not set to zero

The already unrestricted action variation gives the ADM-improved scalar
current j and density p_chi with partial_t p_chi+partial_r j=0. Substituting
the above branch only after variation yields

\[
\widehat j\equiv\frac{Aj}{2NR^2}
 =-C_0u+\gamma\mathcal B,\qquad u=\chi_r,
\]
\[
C_0=P_{X0}-\frac{W_Y}{N},\qquad
\mathcal B=(2QK_r-3qH)u+X\frac{N_r}{N}-\frac{2R_rY}{R},
\quad Y=u^2/A^2.
\]

`derive.py` checks this against the original varied radial current, not against
a guessed Poisson equation. It imports the 36 original action identities and
checks six new exact symbolic identities. The boundary-improved ADM convention
must also be used for p_chi; it cannot be mixed with the unimproved covariant
local current when evaluating charge inside a finite sphere.

For regular fields, center flux zero, and sufficient differentiability,

\[
j(t,r)=-\partial_t\int_0^r p_\chi(t,s)\,ds.
\]

**Regularity does not imply j=0.** Zero current is used below only as a
separately labelled control. Even a metric that looks static need not have
stationary scalar charge, since this action has explicit clock dependence.

## Uniform constitutive sign theorem

For every N>0, q>0, d>0, 0<m<=2, 0<=Y<=Q^2, and B-X>0,

\[
\boxed{C_0>0.}
\]

The X>=0 range is the timelike chi domain together with its null boundary;
it is not a claim that spacelike chi is forbidden by the action.

Proof: multiplying C0 by the positive factor (B-X)N z/(dB), where
z=sqrt(1+Y/ell), gives

\[
F(z)=Nz-1+\frac{q^2/N^2-\ell(z^2-1)}B.
\]

Let t=sqrt(1+Q^2/ell)>1, so 1<=z<=t. This quadratic is concave and its
exact difference from its endpoint chord is

\[
F(z)-\frac{(t-z)F(1)+(z-1)F(t)}{t-1}
 =\frac\ell B(z-1)(t-z)\ge0.
\]

Both endpoints are strictly positive. Write a=q^2/B=1/(1+m)>=1/3:

\[
N^2F(1)=N^3-N^2+a
 =(N-2/3)^2(N+1/3)+a-4/27>0.
\]

At the other endpoint,

\[
F(t)=Nt-1=\sqrt{N^2+2/m}-1>0.
\]

Thus F and C0 are positive. This proof handles Y=0, X=0 and m=2; it
does not exchange a singular m->0 limit with a field equation. Positivity
alone is not a uniform positive lower bound over all allowed N,m.

Consequently gamma=0 AND j=0 imply u=0 in this branch. This is a statement
about the zero-cubic-coupling control, not an exclusion of the actual nonzero
gamma action. A numerical counterexample at m=10,N=.5,X=0 has
C0/d=-0.490711985, demonstrating why the parameter restriction matters.

## Actual nonzero coupling: a necessary transport inequality

At any point where C0>=delta>=0 the exact current identity gives

\[
\boxed{\delta|u|\le|\gamma\mathcal B|+|\widehat j|.}
\]

Hence a finite spatial gradient cannot be justified merely by proposing its
profile. The cubic term or the time derivative of enclosed scalar charge must
supply this budget. It concerns scalar charge, not baryon non-conservation.

A concrete bound for 0<m<=.1 and .99<=N<=1.01 is C0>=d/2. To check it,
split the timelike interval at Y=Q^2/2. Below that point X/B>=2/5 because
2N^2(1+m)<5/2. Therefore P_X0>=5d/3 and W_Y/N<=100d/99, leaving
C0>=65d/99>d/2. Above it N sqrt(1+Y/ell)>=sqrt(1/m)>=sqrt(10)>2;
P_X0>=d and W_Y/N<d/2 again give C0>d/2.

For the local controls A=1,R=r,K_r=H, all admissible zero-current roots satisfy

\[
|u|\le\frac{2|\gamma|}{d}
 \left(|2QH-3qH|Q+Q^2|N_r/N|+2Q^2/r\right).
\]

This is a uniform root bound, independent of whether the numerical search
misses roots. With geometry bounded independently of gamma and d bounded
away from zero, such zero-current gradients are O(gamma). Neither condition
may be silently dropped in a singular/nonperturbative limit.

## Computed controls and what they do not prove

`scan.py` evaluates 4,207 admissible points from the declared broad sign grid.
The analytic argument, not the number of samples, proves the sign theorem.
It also brackets local current roots for 36 choices of lapse (.99,1,1.01),
radius (.1,1,10), and N_r/N (0,1e-6,.001,.01), using the actual gamma=1e-6
background. Every bracketed root is checked against the current residual and
the analytic bound. A separate 60-digit calculation uses exact background
constants and a different root algorithm. Finite bracketing is not exhaustive.
The largest bracketed |u| is 1.97617e-7; the largest absolute disagreement
between the two root calculations is 1.05880e-22 in these units.

For N=1,r=1,N_r/N=.01 the small root is u=1.6528770430e-7. In contrast,
the deliberately finite test gradient u=.1Q=.09090909 requires
widehat(j)=-.00413056424 in these code units. The cubic contribution supplies
only about 1.2353e-5 of C0|u|; it does not balance this profile without flux.
The hypothetical finite profile is **not** asserted to solve metric constraints.
This comparison measures a required transport term, not a predicted galaxy
force, a decay time, or an observational likelihood.

There is no local a0, no empirical fit, no measured-G calibration, no extra
dark-particle population, and no MOND target imposed on these equations.

## Lean scope, verification, and next calculation

`Transport.lean` formalizes the endpoint cubic positivity, positivity above
an endpoint chord, and the absolute-value transport inequality. The map from
the covariant action and constitutive square roots into those hypotheses is
derived analytically here and checked symbolically outside Lean. Compilation
does not formalize the PDE, Dirac closure, gravity phenomenology or the entire
sign theorem end-to-end. These certificates must not be advertised as a
Lean-certified law of nature.

The initial Lean invocation failed because the umbrella Mathlib.Tactic import
requested an unavailable compiled dependency. Restricting the import to the
already available Linarith module resolved that environment issue without
changing a theorem. Final commands, input hashes, versions, exits and raw output
are recorded in run_001/manifest.json and run_001/stdout.txt. All four top-level
jobs returned exit 0, including all eight nested prior pressure-branch jobs.
All three new Lean lemmas compile with only propext, Classical.choice and
Quot.sound reported. The manifest validator with current-input hash checking
also returned 0. These are computation/proof checks, not a theory PASS.

Fable commits 7a9f6df2f and 93845f387 arrived during this work. Their three
changed files are confined to fable_independent_2026; no input of this
calculation was changed. Their cosmology conclusions were not re-audited here.

Self-audit: the current restriction, timelike domain, positive logarithmic
denominator, background range and nonzero-flux alternative are explicit.
The finite root search is labelled non-exhaustive; no sampled sign is used as
a universal proof. No independent agent or external novelty audit was performed.
Mathematical proofreading covered only this package, with no changes to other
research or to the action.

**Next unavoidable calculation:** evolve the nonzero current and metric
constraints together with supported matter, or construct a controlled slowly
evolving boundary solution that supplies the required enclosed-charge rate.
This budget is a check on that solution, not a substitute. The pre-existing
finite-time evolution convergence failure remains unresolved. Spatially varying
chi_t, spacelike chi, other cosmological m, and singular geometric limits lie
outside this theorem and require their own stability/constraint analysis.

Credit Carl Zimmerman for the primordial-clock and persistent-transport
intuition, including the paddle/swirl analogy. Brian Keating's video
https://www.youtube.com/watch?v=HRnselv8Y6E was user-supplied motivation;
no video theorem or endorsement is claimed. Mathbox research/computation audit
guided the distinction between a source budget and a constructed solution.
