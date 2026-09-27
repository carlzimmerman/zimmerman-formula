# Independent causal-completion audit and scoped Lean bridges

**Primary verdict: proved as written for the stated constant-coefficient
algebraic claims.** The final Lean file compiles with exit 0: eight theorems,
no warnings, no admitted proofs or custom axioms, and all axiom dependencies
contained in `{propext, Classical.choice, Quot.sound}`. The continuum support
argument below is an analytic audit, not a Lean PDE certificate.

**Normalized claim:** for the explicit constant-coefficient two-real-field
quadratic action below, the canonical Hamiltonian is nonnegative, its scalar
dispersion roots are positive for positive spatial momentum squared, and its
low-momentum branch can match any sound-speed-squared coefficient in `(0,1)`
and any positive quartic coefficient. Deleting the second field's time kinetic
term preserves positive reduced inertia but introduces a spatially nonlocal
acceleration operator. All field-count statements here concern this explicit
fixed-background action, not a constrained gravitational theory.

The source audited is `check.py`, SHA-256
`54d809f264b46530ab092065dbc5371828587b4913f4e58017c7eb2e9cb44938`.
Its `run1` contains 20 passing exact symbolic checks and a validated provenance
manifest. This review reconstructed the variational signs and physical-domain
conditions from the action rather than accepting the supplied dispersion as
an independent premise.

## Direct action audit

In one spatial dimension,

\[
\mathcal L=\frac12(z_t^2+\chi_t^2-z_x^2-\chi_x^2-m^2\chi^2)
 +g\chi z_t,\qquad m^2>0,\quad g\in\mathbb R.
\]

Independent variation gives

\[
z_{tt}-z_{xx}+g\chi_t=0,\qquad
\chi_{tt}-\chi_{xx}+m^2\chi-gz_t=0.
\]

The signs of the two mixing terms are opposite. The momenta are
`p_z=z_t+g chi` and `p_chi=chi_t`; the velocity Hessian is the identity. The
Legendre transform is

\[
\mathcal H=\frac12[(p_z-g\chi)^2+p_\chi^2+z_x^2+\chi_x^2+m^2\chi^2].
\]

It is nonnegative, with no velocity constraint in this two-field model.
This establishes two canonical scalar pairs here. It does not establish a
constraint count after gravitational coupling, or close a one-clock target.

For a mode proportional to `exp(i kx−i omega t)`, the field matrix is

\[
\begin{pmatrix}k^2-\omega^2&-ig\omega\\
ig\omega&k^2+m^2-\omega^2\end{pmatrix}.
\]

Its determinant is

\[
(r-q)(r-q-m_2)-g_2r,
\qquad r=\omega^2,\ q=k^2,\ m_2=m^2,\ g_2=g^2.
\]

The interpretation `g2=g²` is required when connecting the polynomial to the
real action. In the Lean polynomial lemmas `g2` is an explicitly nonnegative
real parameter. For `q>0,m2>0,g2≥0`, any real root `r` is strictly positive:
if `r≤0`, both factors in the first product are negative, while `−g2 r≥0`,
contradicting the zero polynomial. At `q=0` the massless root is zero, so that
boundary is deliberately excluded from the strict-positivity statement.

Write `A=m2+g2`. For

\[
r_{trial}=(m_2/A)q+(g_2^2/A^3)q^2,
\]

Lean proves the exact residual

\[
P(r_{trial},q)=-2g_2^3q^3/A^4+g_2^4q^4/A^6.
\]

Thus the first two coefficients cancel exactly. The source separately
differentiates the explicit lower square-root branch, establishing the stated
Taylor coefficients. The Lean polynomial lemma alone does not assert an
analytic remainder estimate or existence of that branch.

For target sound-speed squared `s∈(0,1)` and quartic coefficient `d>0`, take

\[
A=(1-s)^2/d,\quad m_2=sA,\quad g_2=(1-s)A.
\]

Lean checks all three parameters' positivity and the exact coefficient match.
Here `s` denotes speed squared, not speed. The fit does not remove the second
canonical pair or prove an embedding into the desired MOND action.

## Continuum energy/finite-cone argument, separately from Lean

For sufficiently smooth solutions with suitable decay and compactly supported
initial fields and velocities, define

\[
h=\tfrac12(z_t^2+\chi_t^2+z_x^2+\chi_x^2+m^2\chi^2),
\qquad F=-(z_tz_x+\chi_t\chi_x).
\]

Substitution of the two equations gives `h_t+F_x=0`: the mixing contributions
`−g z_t chi_t` and `+g chi_t z_t` cancel. The scalar inequality

\[
|ab+cd|\le\tfrac12(a^2+b^2+c^2+d^2+e^2)
\]

is Lean-certified and implies `|F|≤h` with
`a=z_t,b=z_x,c=chi_t,d=chi_x,e=m chi`.

If initial support is contained in `[-R,R]`, the right exterior energy obeys

\[
\frac{d}{dt}\int_{R+t}^{\infty}h\,dx=F(R+t,t)-h(R+t,t)\le0,
\]

and the left exterior has derivative `−F−h≤0`. Initially both vanish and
energy is nonnegative, so both remain zero. Initial vanishing of the fields
then fixes the otherwise constant exterior solutions to zero. This supplies
the finite-speed support argument for smooth finite-energy solutions of this
constant-coefficient system. Existence/uniqueness and the moving-domain
integration argument are not formalized in the supplied Lean file. The
statement is not inferred from group velocity alone.

## Deleting the second time derivative

Without `chi_t²/2`, variation yields the elliptic constraint

\[
(m^2-\partial_x^2)\chi=gz_t.
\]

On Fourier modes the reduced inertia is `1+g²/(m²+k²)>0`, and

\[
\omega^2=\frac{k^2(m^2+k^2)}{m^2+g^2+k^2}.
\]

This is positive but does not give finite propagation. With
`A=m²+g²`, the exact acceleration operator is

\[
z_{tt}=(m^2-\partial_x^2)(A-\partial_x^2)^{-1}\partial_x^2z
=\partial_x^2z+g^2z-g^2A(A-\partial_x^2)^{-1}z.
\]

Lean certifies the corresponding scalar resolvent identity for every
nonnegative Fourier eigenvalue `ell`. For nonnegative, nonzero compact initial
`z0`, outside its support the two local terms vanish. The one-dimensional
Green kernel is positive,

\[
G_A(x-y)=\frac{e^{-\sqrt A|x-y|}}{2\sqrt A},
\]

so the remaining initial acceleration is strictly negative when `g²>0`:

\[
z_{tt}(x,0)=-g^2A\int G_A(x-y)z_0(y)\,dy\ne0.
\]

For a time-twice-differentiable solution initially zero with zero velocity at
that exterior point, this gives a nonzero response at arbitrarily small positive
times. The positivity of this integral and propagation-of-support reasoning
are analytic arguments, not Lean-certified PDE theorems. They are independent
of the source's high-momentum group-velocity calculation.

## Exact formal scope and validation

`DoorsCausal20260926.lean` contains eight algebra/order certificates:

1. exact Legendre-transform square;
2. nonnegative Hamiltonian;
3. positive real dispersion root for `q>0`;
4. exact low-root polynomial residual;
5. coefficient matching with positive parameters;
6. positive reduced elliptic inertia;
7. elliptic acceleration resolvent identity;
8. energy-flux inequality.

The dependency graph is explicit action → direct variation/Legendre transform
→ scalar algebra → formal consequences. The full continuum support argument
is an additional analytic dependency, stated above under its regularity and
boundary assumptions. No formal declaration assumes the desired sign as a
hypothesis; the signs follow from positivity domains and square identities.

The final compiler status, source hash, command and theorem-level axiom reports
are recorded in `lean_record.json`; only a successful final log is accepted.
No statements about nonlinear gravitational health, a one-clock completion,
PPN, lensing or a cosmological fit are certified by this file.

The accepted command, run from the existing Lean project directory, is:

```sh
/opt/homebrew/bin/lake env lean -j 1 DoorsCausal20260926.lean
```

It completed in 40.69 seconds. `lean_final.log` contains the accepted output.
One earlier draft failed because a redundant `ring` tactic followed a goal
already closed by `field_simp`; that log is retained as development evidence
and excluded from the accepted certificate. The final proofreading pass checked
signs, squared-parameter conventions, boundary restrictions and formal versus
analytic scope without changing the mathematics. No existing source or build
configuration was modified.
