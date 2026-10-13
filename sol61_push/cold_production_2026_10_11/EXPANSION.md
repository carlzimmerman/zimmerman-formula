# Survival after expansion in a finite quantum model

2026-10-11. Base inspected: `defe92ee8af8400c34fa1c50a5c27e265f66563e`.
Continuation of [the production mechanism](REPORT.md). This calculation
tests a specific missing implication: whether dilution and detuning can
prevent complete reconversion to the source. It is not a continuum or
cosmological abundance calculation.

## Hamiltonian and background

Keep a parent at zero momentum and three daughter pairs at opposite
comoving momenta. Write k_j=m u q_j, with u=0.001 and q_j=0.7,1,1.4.
Set M=2m sqrt(1+u^2), omega_j(a)=sqrt(m^2+k_j^2/a^2). Retain the
same resonant conversion interaction as in the preceding report:

\[
 H=M N_b+\sum_j\omega_j(a)(N_{j,+}+N_{j,-})
 +\sum_jg_j(a)(b a_j^\dagger c_j^\dagger+b^\dagger a_j c_j).
\]

The mode-normalization dependence is
g_j(a)=g_* a^(-3/2) omega_*/omega_j(a), with omega_*=M/2.
This follows from adiabatic free-field normalization in comoving volume.
The rotating-wave and adiabatic approximations are stipulated reductions;
the full covariant field theory has not been simulated.

The invariant N=N_b+sum_j n_j, with N_{j,+}=N_{j,-}=n_j, remains conserved.
The basis is all nonnegative tuples (n_1,n_2,n_3) with sum n_j<=N.
Its dimension is binomial(N+3,3); this is the full invariant sector of the
declared mode Hamiltonian, not an occupation cutoff within that sector.
Each link adding one pair to mode j has coefficient
g_j(n_j+1)sqrt(N-sum n_j).

Use x=m u^2 t, eta=g_*/(m u^2)=0.08 and h=H(a=1)/(m u^2)=0.03.
An imposed radiation-dominated background has
a^2=0.25+2 h x. The origin a=0.5 is the start of the calculation, not the
big bang. No cold daughters are initially occupied. These dimensionless
parameters are test inputs; the background is not solved from the parent,
daughters and visible matter through the Friedmann equation.

Subtract the invariant M N and divide by m u^2. In this reduced Hamiltonian,

\[
 K(x)=\sum_j\delta_j(a)n_j+\sum_j\gamma_j(a)T_j,
 \quad\delta_j=\frac{2(q_j^2/a^2-1)}{
 \sqrt{1+u^2q_j^2/a^2}+\sqrt{1+u^2}},
\]

where gamma_j=eta a^(-3/2) sqrt(1+u^2)/sqrt(1+u^2q_j^2/a^2).
The rationalized expression for delta avoids cancellation near resonance.
The source crosses the resonance of pair j at a=q_j.

## Energy accounting includes expansion

For the finite unitary equation i dpsi/dx=K(x)psi,

\[
 \frac{d\langle K\rangle}{dx}=\langle K'(x)\rangle.
\]

The derivative contains both the redshifting free-particle energy and the
changing interaction energy. In physical units the former is
-2H sum_j (k_j^2/a^2)/omega_j times the mean pair number in each mode.
Ignoring the derivative of g_j would miss part of the work. The script
integrates the complete work alongside the state and checks it against
the Hamiltonian expectation. This is conservation with explicit work in
the reduced model, not a computed full-field cosmological stress tensor.

## A bound on all future reconversion

This finite-dimensional model permits more than a visual plateau argument.
Define n=sum_j n_j, d=2/(sqrt(1+u^2)+1)>0. Then

\[
 K(x)=-d n+R(x),\qquad
 R=\sum_j r_j(a)n_j+\sum_j\gamma_j(a)T_j,
 \quad r_j=\frac{2q_j^2/a^2}{\sqrt{1+u^2q_j^2/a^2}+1}.
\]

Each r_j and gamma_j is positive and decreases to zero as a increases.
For gamma, d log(gamma)/d log(a)=-3/2+v_j^2<-1/2. All matrices have
finite norm. Let C_j bound ||T_j||; the maximum absolute row sum suffices
because T_j is symmetric. Since ||n_j||=N,

\[
 B(A)=N\sum_jr_j(A)+\sum_j\gamma_j(A)C_j
 \quad\Longrightarrow\quad
 \|R(A)\|\le B(A),\quad
 \int_{x(A)}^\infty\|R'(x)\|dx\le B(A).
\]

The second inequality follows term by term by monotonicity, not by assuming
an oscillatory integral cancels. Energy expectation therefore has a finite
limit E_inf, with |E_inf-E(A)|<=B(A). Because R tends to zero,
mean n has a limit and E_inf=-d mean n_inf. Combining these statements gives

\[
 \boxed{\left|\frac{\langle n\rangle_\infty}{N}
      -\frac{\langle n\rangle_A}{N}\right|
      \le\frac{2B(A)}{dN}.}
\]

This is an analytic bound for the stipulated finite Hamiltonian and its
indefinitely expanding background. After the endpoint it only requires that
a remains monotone and tends to infinity with the same mode-normalization
law; it does not require radiation domination to persist forever.
A positive lower bound would establish
surviving production in that model even after all later inverse conversions.
It says nothing about the omitted continuum, collapse or gravitational
clustering. Its evaluation on a numerical state inherits the integrator's
error; the calculation is not an interval-arithmetic proof certificate.

## Scope of the proposed test

[expansion.py](expansion.py) originally specified N=4 and 8, three pair modes,
and a in [0.5,16], with a tighter N=4 repeat and a zero-coupling control. That
run hit its 180-second cap before returning scientific results. Its timeout
manifest is retained under `expansion_run`; no production verdict comes from it.
[expansion_v2.py](expansion_v2.py) reduces the endpoint to a=8, leaving all
other physical inputs and checks unchanged, with a new 150-second cap. This
resource-driven revision was made before any conversion output was available.
Norm,
expansion work and the future-return bound are recorded. Its result record
is authoritative for execution success and numerical values; a timeout is
not a physical rejection. The contract fixes these inputs before execution.

The revised run completed and passed 16/16 checks. At a=8:

| Source quanta N | Converted fraction | Bound on any future fraction change | Lower bound on limiting fraction |
|---:|---:|---:|---:|
| 4 | 0.95617571 | 0.15152576 | 0.80464994 |
| 8 | 0.96144097 | 0.16188583 | 0.79955514 |

These lower bounds use numerical endpoint states and the exact finite-model
inequality. They are conditional on numerical accuracy, not rigorous interval
enclosures. Reporting about 79% as a surviving fraction leaves a much larger
margin than the observed numerical errors but does not upgrade the computation
to a formal proof certificate. Fractions count converted source quanta, each
giving one pair, rather than a ratio to the initially empty daughter population.

The largest norm error is 1.20e-6, and the largest reduced-energy/work
discrepancy is 9.06e-6. Tightening the N=4 tolerances changes the endpoint
fraction by 3.65e-7 and reduces both conservation discrepancies. The
zero-coupling control produces exactly zero daughters. The
[result](expansion_run_v2/results.json) and
[manifest](expansion_run_v2/manifest.json) preserve all snapshots and checks.
The manifest validator passed. The original timeout is retained rather than
counted as a rejection or a successful run.

At the endpoint, every retained mode has p/m <= 1.75e-4 and subsequently
redshifts further. This guarantees small kinetic pressure in these retained
modes. It does not prove that hotter modes in the untruncated theory remain
empty. The three pairs also do not constitute an isotropic halo.

In particular, the modes are selected cold modes. No calculation here
demonstrates that the full action suppresses every omitted hotter mode.
The finite occupation is also far below the cosmological occupation screen
in the first report. Resolving these two issues, and imposing the source
energy and Hubble rate self-consistently, is necessary before applying the
construction to the repository's cold component. Even that would leave
the galaxy-law and vacuum-normalization mechanisms unresolved.

Self-review verdict: **conditional on the specified finite-mode Hamiltonian,
expanding background and numerical endpoint accuracy**, permanent nonzero
daughter production follows. The analytic proof uses finite matrix norms;
its bound is not uniform under adding arbitrary high-momentum modes and must
not be extrapolated to the field continuum.

The next discriminating calculation should start from the one-field potential,
not add more tuned cold modes. With X homogeneous and Y initially linearized,
the exact classical background and linear fluctuation equations are

\[
 \ddot X+3H\dot X+\lambda(X^2-f^2)X=0,\qquad
 \ddot Y_k+3H\dot Y_k+
 [k^2/a^2+m^2+\lambda(X^2-f^2)]Y_k=0.
\]

A mode-instability analysis of this source will test whether the fastest
growth actually lies in the cold band or whether omitted hot modes dominate.
It must then include quantum initial fluctuations, renormalized backreaction,
and the source's contribution to expansion. The displayed linear equations
cannot by themselves calculate depletion or the final abundance.
