# Both exponential branches: continuation of the existing audit

**Claim audited:** the existing C-H/K scalar completion remains healthy with
either exact exponential law in its stated small-alpha parameter window.
**Verdict: refuted for the displayed frozen scalar block.** This is a failure
of this completion in that window, not a no-go for either law or another action.

The user explicitly requested exploration of both branches on 2026-09-26.
The earlier EXP reduction in
[recipe_followup_check.py](../../closure_resume_2026_09_26/recipe_followup_check.py)
is retained as prior work. The new calculation extends that comparison to RAR
and checks the filter crossing explicitly. It does not restart the earlier
construction campaign.

Use t=g_N/a0 and x=g/a0 consistently:

| Branch | Definition | Dimensionless phantom acceleration h |
|---|---|---|
| RAR | x=t/(1-exp(-sqrt(t))) | t/(exp(sqrt(t))-1) |
| EXP | t=x(1-exp(-x)) | x exp(-x) |

The RAR definition matches equation (4) of McGaugh, Lelli and Schombert,
[arXiv:1609.05917v1](https://arxiv.org/pdf/1609.05917v1), checked on
2026-09-26 (PDF title, author list, v1 marking and equation inspected).
This source supplies the fitted constitutive expression, not a relativistic
action or a derivation of a0 from vacuum energy. The primary source was read
online; no new local source cache was created.

The corresponding longitudinal coefficients are, with z=sqrt(t),

\[
C_{L,\mathrm{RAR}}=
\frac{e^z(1-z/2)-1}{(e^z-1)^2},\qquad
C_{L,\mathrm{EXP}}=\frac{1-x}{e^x+x-1}.
\]

Both have a negative interval. They cannot be replaced by L340's positive-slope
`nu_mono` and still be called the same exact constitutive law. A spherical
inverse also does not identify nonspherical AQUAL and QUMOND equations.

Independent elimination of lapse, shift and auxiliary from the existing
real-time frozen block yields, for B=c2>0 and k>0 on its regular branch,

\[
L_{\rm red}=\frac{2(2+3B)}B\dot\psi^2
 -2k^2\frac{N}{D}\psi^2,
\quad D=\alpha+(\alpha+2)C,
\quad N=2-\alpha(1+C),
\quad \frac{c_s^2}{c^2}=\frac{BN}{(2+3B)D}.
\]

For -1<C<0 and the small positive alpha window, N>0. Consequently D must be
positive, requiring alpha > -2C/(1+C). Equality is singular and is excluded.

| Exact witness | C_L | Required alpha in the unsuppressed limit |
|---|---:|---:|
| RAR, t=9 | -0.03031581176 | >0.06252718592 |
| EXP, x=2 | -0.11920292202 | >0.27067056647 |

The latter is also the maximum EXP threshold on x>1: the threshold is
2(x-1)exp(-x), whose maximum occurs at x=2. No global optimum is claimed for
the RAR witness. Both are far above L340's stated alpha ceiling 3.2e-9;
that empirical ceiling is an inherited conditional input, not rederived here.

With the frozen heat factor C=C0 exp(-(k xi)^2), a coefficient satisfying
C0 < -alpha/(alpha+2) gives a finite singular crossing

\[
(k\xi)_*=\sqrt{\log\frac{-(\alpha+2)C_0}{\alpha}}.
\]

At alpha=3.2e-9 the two witnesses give 4.093553 (RAR) and 4.257503 (EXP).
At the crossing N=4/(alpha+2)>0, so numerator cancellation cannot regularize
this reduced expression. Explicit nonzero-k samples on its low-k side have
negative squared speed. The UV filter does not remove that lower-k interval.
This conclusion is conditional on the displayed frozen coefficient model and
the available background/wavelength domain; it is not a full curved-background
instability theorem.

Raising alpha is not a finished repair. The same block changes the static
response to (1+C)/(1-alpha(1+C)/2). Even after dividing by the high-acceleration
Newton normalization 1/(1-alpha/2), this is not 1+C. A repair must rederive the
constitutive function and measured Newton constant together. The previous
large-alpha bounded witness remains valid within its explicitly restricted
scope and supplies no PPN pass.

There is a separate zero-field extrapolation warning: for fixed alpha>0,
C_T=nu-1 diverges as t tends to zero, and N crosses zero at C_T=2/alpha-1.
At the quoted ceiling the unsuppressed transverse static-response pole lies near
t=2.56e-18 for both exact laws. This is outside L340's sampled acceleration
range and is not a prediction for a real astronomical object. It prevents
extending that finite sample into an all-field regularity claim. Here D=4/alpha
remains finite and the squared speed vanishes; this is a pole of the static
gain, not of the dynamical dispersion relation.

**Verification:** [check.py](check.py), [contract](contract.json),
[results](run1/results.json), and [validated manifest](run1/manifest.json).
Twelve checks include exact symbolic identities, a failing-health control and
separate numerical branch witnesses. Both a0 footings share these dimensionless
results. No expensive observational simulation was rerun.

**Next construction obligation:** change the response/inertia architecture
while retaining the exact selected kernel, both varied metric potentials and
the measured-G normalization. Each candidate must then face the same constraint,
PPN and zero-field tests. Merely increasing alpha or changing the kernel is
not closure.
