# An alternative with exact charge and a coherent pressure bound

2026-10-11. This is a **different two-complex-field action**, not a result
for the earlier one-complex-field potential. It addresses the missing
weighted-number and coherent-stress hypotheses in [PRESSURE_BOUND.md](PRESSURE_BOUND.md).
No previous conversion yield is transferred to this action.

## Action and protected energy budget

Use canonical complex fields phi and chi, charges 1 and 2, respectively:

\[
 {\cal L}=|\partial\phi|^2+|\partial\chi|^2-V,\quad
 V=m^2|\phi|^2+4m^2|\chi|^2+
 \left|\sqrt\Delta\,\chi+{g\over\sqrt\Delta}\phi^2\right|^2,
 \quad m,\Delta>0,\quad g\in\mathbb R.
\]

A constant vacuum term can be added but is excluded from the material energy
and stress below. Write U for the final nonnegative square. Expansion gives
source mass M^2=4m^2+Delta, the conversion vertex
g(chi* phi^2+chi phi*^2), and quartic coupling g^2/Delta. Unlike an arbitrary
trilinear potential, its positive-square form gives a global energy bound.
The origin is its unique zero-energy minimum.

The transformation phi -> exp(i alpha) phi, chi -> exp(2i alpha) chi
is an exact global symmetry. Define the positive-charge convention

\[
 Q=\int i(\phi^*\dot\phi-\dot\phi^*\phi)
 +2i(\chi^*\dot\chi-\dot\chi^*\chi)\,d^3x.
\]

Assume smooth classical solutions in a fixed periodic box, or decaying
fields with all integration-by-parts boundary terms absent. E and Q are
conserved. Let G be the integrated gradient energy. Completing time-derivative
squares gives the exact identity

\[
 D:=E-mQ=\int|\dot\phi+im\phi|^2+
 |\dot\chi+2im\chi|^2+|\nabla\phi|^2+|\nabla\chi|^2+U\,d^3x\ge0.
\]

The same argument with opposite signs gives E>=m|Q|. Thus arbitrary classical
nonlinear evolution cannot release most of the positive-charge rest energy
into gradients or motion in the rotating frame if eta=D/E is initially
small. This statement does not discard nonzero source momenta or nonlinear
vertices. It is classical; a renormalized quantum inequality has not been
established here.

A homogeneous circular source chi=A exp(-iMt), phi=0 has E/V=2M^2 A^2 and
Q/V=4M A^2, hence eta=1-2m/M. It is already a cold charged energy reservoir.
The construction converts its carrier; it does not create net charge or
explain the initial energy amount. Exactly zero classical daughters remain
zero. Nonzero classical seeds modify eta and must be included in E and Q.
Quantum vacuum seeding requires a separate quantum treatment.

## Full classical stress, including interactions

Let PV be the integrated one-third trace of the spatial stress:

\[
 PV=\int(|\dot\phi|^2+|\dot\chi|^2)-G/3-\int V.
\]

Writing time derivatives as rotating-frame derivatives plus their rest
rotations and applying Cauchy-Schwarz yields

\[
 |PV|\le D+2\sqrt{DE}.
\]

For detail, the non-cross terms have absolute sum at most D. The cross
terms are bounded by twice the square root of the rotating-frame derivative
energy times \(\int m^2|\phi|^2+4m^2|\chi|^2\le E\).
Thus even instantaneous pressure is bounded by eta+2sqrt(eta) times density.

A stronger time-averaged statement retains the exact virial boundary term.
Define S=Re integral(phi* dot(phi)+chi* dot(chi)). The equations of motion give

\[
 PV=\dot S+{2\over3}G+
 \operatorname{Re}\int w^*(z+w),\quad
 z=\sqrt\Delta\chi,\quad w={g\over\sqrt\Delta}\phi^2.
\]

Indeed, if V_c=2Re(z* w) and B=integral |w|^2, the cubic and quartic
contributions to this remainder are V_c/2+B. This is exactly the expression
shown; the quadratic terms cancel in the virial identity.

Put M=2m sqrt(1+u_*^2), so Delta=4m^2u_*^2. Then

\[
 \int|z|^2\le u_*^2E,\qquad
 B\le2\int U+2\int|z|^2\le2D+2u_*^2E.
\]

Consequently the remainder has absolute value at most
sqrt(2D(D+u_*^2E)). Also |S|<=sqrt(ED)/m: the rest-rotation terms in S have
zero real part. Over **any interval of length T** along such a solution,

\[
 \boxed{\left|{\overline P\over\rho}\right|
 \le {2\sqrt\eta\over mT}+{2\eta\over3}
 +\sqrt{2\eta(\eta+u_*^2)},\qquad \rho=E/V.}
\]

No ensemble, dilute-particle assumption, momentum cutoff, or neglect of
interaction stress enters this classical result. Smooth existence over the
interval and the boundary conditions are hypotheses, not proven here.

For u_*=0.001 and the circular-source eta=4.99999625e-7, the bulk bound is
1.55807734e-6. At mT=1e6 the endpoint contribution is 1.41421304e-9, giving
|average P|/rho <1.56e-6. The instantaneous bound is 0.001414714.
The averaging interval may start at any time because E and Q are conserved.
Seeded states use their actual eta rather than the unseeded source value.
These bounds do not prove a small sound speed, halo behavior or a particular
particle fraction.

## A cold linear production band in this action

Linearize daughters around chi=A exp(-iMt). They obey

\[
 \ddot\phi_p+(p^2+m^2)\phi_p+2gA e^{-iMt}\phi_{-p}^*=0.
\]

Taking phi=exp(-iMt/2) psi removes the periodic coefficient. Set
D_p=p^2+m^2-M^2/4 and c=2gA. The constant real system has characteristic
polynomial

\[
 (s^2+D_p)^2+M^2s^2-c^2=0.
\]

Since 2D_p+M^2>0 for physical p, its positive growth branch exists exactly
when D_p^2<c^2. Thus the only exponential daughter band is

\[
 |p^2-m^2u_*^2|<2|gA|.
\]

Choosing 2gA=2 epsilon m^2, epsilon=1e-7, gives
8e-7<p^2/m^2<1.2e-6 and center growth approximately epsilon m. This is an
exact linear reduction about a fixed classical circular source. The quartic
term does not enter at linear order. It can affect depletion and saturation,
so the earlier Gaussian calculation cannot simply be reused.

This supplies an instability that amplifies a daughter seed; it does not
compute nonlinear conversion from quantum vacuum or the final abundance.
The source amplitude, charge, mass splitting and coupling are inputs.

## Self-audit and remaining obligations

Normalized claim: for the specified smooth classical Minkowski solutions,
E-mQ is the displayed positive functional and the averaged stress bound
holds for every finite interval. Verdict: **proved as written under these
explicit restrictions**, by the internal algebra and inequalities above.
This is self-review, not an independent audit or a novelty claim.

Dependency audit:

* Exact symmetry and canonical Noether charge: checked by substitution;
  sign checked on the positive circular source.
* Energy-square identity: checked by direct expansion, including gradients.
* Virial identity: checked from both field equations and homogeneity degrees
  of the quadratic, cubic and quartic potential terms.
* Cauchy-Schwarz estimates and endpoint term: checked with integrated norms;
  no positivity of instantaneous pressure assumed.
* Linear instability: checked by the constant four-dimensional real system;
  degenerate band edges have zero exponential growth, not guaranteed bounded
  solutions.
* Expansion, renormalized quantum dynamics, and global smooth existence:
  not addressed by this proof.

[charged_checks.py](charged_checks.py) supplies 248 finite algebra and
linear-eigenvalue checks, all passing. [Results](charged_checks_run/results.json)
and [manifest](charged_checks_run/manifest.json) record them. The universal
claims rest on the derivation, not those finite samples. Its algebra test
coupling g=0.01 is arbitrary and is not a physical benchmark fit.

The original user goal remains open: this is a protected alternative for
producing and retaining a low-pressure carrier, but production efficiency,
cosmological evolution, source origin, abundance, and the repository's
acceleration/vacuum connection remain unproved. The next discriminating
step is an expanding version of the energy-charge control and a new
production calculation that includes this action's required quartic term.
