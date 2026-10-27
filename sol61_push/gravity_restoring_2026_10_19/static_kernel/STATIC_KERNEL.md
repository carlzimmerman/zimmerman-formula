# A static restoring-kernel discriminator

19 October 2026. Mathematical parent CE-PARTICLE-2026-10-18; initial
HEAD `9516ee01c79f35c04b7556050669ba77b0c98b99`. This is an internal proof
and bounded computation, not a literature-wide or all-phase no-go theorem.

The previous calculation identified a missing positive `K_g/k²` material
density kernel, `K_g=4piG`. The following result tests even an approximate
match on a finite band. Increasing source resonance, reducing a stable
static gap, or retaining its full canonical spatial gradients does not
repair the opposite momentum dependence in this class.

## 1. Exact claim and its hypotheses

Let `z=k²` range over a connected interval `I` of positive real numbers.
Let `A,B` be finite Hermitian matrices, `B>=0`, and

\[
 K(z)=A+zB>0\quad(z\in I).
\]

Let the density source vector `q` be independent of `z`. Permit an
additional local susceptibility `s>=0`, also independent of `z`. Define

\[
 \chi(z)=s+q^\dagger K(z)^{-1}q>0,
 \qquad h(z)=\chi(z)^{-1}.
 \tag{1}
\]

For a linear scalar probe coupled to that density, `delta rho=-chi U`.
Its constrained quadratic material energy is `h |delta rho|²/2`.
This latter interpretation requires the declared linear-source/Legendre
convention; an arbitrary unrelated response function may not be renamed
a density stiffness. Eliminating a local auxiliary density with energy
`sigma²/(2s)` realizes the term `s` when it is positive. At `s=0` that
auxiliary is absent.

Then `chi` is nonincreasing and `h` is nondecreasing throughout `I`.
Indeed, putting `v=K^-1 q`,

\[
 \chi'(z)=-v^\dagger Bv\leq0,
 \qquad h'(z)={v^\dagger Bv\over\chi(z)^2}\geq0.
 \tag{2}
\]

The derivative is an exact inverse-matrix identity. Positivity is not
inferred from a sample. `A` need not separately be positive if `K` is
positive on the admitted band. If a decoupled zero-curvature mode is
present, a positive regulator and a finite-response limit preserve the
ordering; divergent/undefined response is not a finite positive target.

For completeness, without the local auxiliary the constrained minimizer
of `x^dagger K x/2` at `q^dagger x=delta rho` is

\[
 x={K^{-1}q\over q^\dagger K^{-1}q}\,\delta\rho.
 \tag{3}
\]

Its Euler equation is `Kx=h delta rho q`, and its energy is the one above.
With the auxiliary, apply the same formula to
`diag(K,1/s)` and source vector `(q,1)`.

## 2. A sharp finite-band obstruction

The target positive quadratic polarization energy is

\[
 {K_g\over2}|P_L|^2
 ={1\over2}{K_g\over z}|\delta\rho|^2,
 \qquad P_L=-{ik\over k^2}\delta\rho.
 \tag{4}
\]

Its inverse density kernel decreases as `1/z`, the opposite of (2).
Suppose on `[z_a,z_b]`, `0<z_a<z_b`, a positive nondecreasing `h` obeyed

\[
 \left|{h(z)\over K_g/z}-1\right|\leq\epsilon<1.
\]

At the endpoints monotonicity requires

\[
 (1-\epsilon){K_g\over z_a}
 \leq h(z_a)\leq h(z_b)
 \leq(1+\epsilon){K_g\over z_b}.
\]

Consequently, writing `R=k_b/k_a`,

\[
 \boxed{\quad\epsilon\geq{z_b-z_a\over z_b+z_a}
 ={R^2-1\over R^2+1}.\quad}
 \tag{5}
\]

The bound is sharp in the entire monotone class: constant
`h=2K_g/(z_a+z_b)` attains the equal endpoint errors, and the intermediate
relative error is linear in `z`. It is therefore not merely an asymptotic
statement at zero momentum.

| Momentum ratio R | Smallest possible uniform relative error |
|---:|---:|
| 1.1 | 0.0950226 |
| 2 | 0.6 |
| 10 | 0.9801980 |
| 100 | 0.9998000 |

These are errors in the material kernel relative to the required kernel,
not fitted errors in a complete observed galaxy acceleration. The result
does not rule out a narrow accidental matching interval or a particular
inhomogeneous solution; those would be different claims with their own
source and boundary data.

## 3. Why a Jeans crossing is not the restoring mechanism

Eliminating the ordinary Newtonian gravitational potential gives

\[
 E_{\rm total}^{(2)}={1\over2}
 \left[h(z)-{K_g\over z}\right]|\delta\rho|^2.
 \tag{6}
\]

On the same stable material interval,

\[
 {d\over dz}\left(h-{K_g\over z}\right)
 =h'+{K_g\over z^2}>0.
 \tag{7}
\]

There is at most one zero on each connected admitted band. If endpoint
signs differ, there is exactly one. If also `z h(z)` tends to zero at the
lower endpoint and grows beyond `K_g` at the upper one, this is the usual
Jeans separation between unstable and stable wavelengths. Neither the
existence nor uniqueness of a crossing without such range assumptions is
being asserted. The desired material quadratic term would cancel the
gravitational term at every scale; (7) prevents that within this class.

One can see the sign directly in a contact theory with a healthy static
scalar coupled to density. Eliminating that scalar gives

\[
 h_{\rm scalar}(z)=g_0-{g_s^2\over z+M_s^2},
 \qquad h'_{\rm scalar}={g_s^2\over(z+M_s^2)^2}>0.
 \tag{8}
\]

Even tuning `g0=g_s²/M_s²` leaves
`g_s² z/[M_s²(z+M_s²)]`, not a positive `1/z` stiffness. At zero mass the
scalar-mediated term is negative. A Gauss-law electric field can instead
produce positive Coulomb energy, but it is a new constraint/gauge sector;
it is not a healthy real-amplitude minimization of (8). Its source would
also need a positive gravitational-density dictionary. The original
particle action contains no such force carrier.

## 4. Matching the proof to the actual particles

For the stated positive-charge coherent NR source/daughter background,
the parent report gives canonical amplitudes with

\[
 A=\begin{pmatrix}4k_c n&2c_3\sqrt n\\
 2c_3\sqrt n&\Delta\end{pmatrix},\quad
 B=\operatorname{diag}(1/(2m),1/(2M)),\quad
 q=\sqrt2m(\sqrt n,2b_0)^T,
\]

where `Delta=delta-2mu`, `b0=-c3 n/Delta` and
`mu=2(kc-c3²/Delta)n`. Thus (1) has exactly the required form on a stable
background. The negative source-amplitude entry in `q` does not evade (2).
The fully threshold-matched contact correction changes `A`, not the
nonnegative `B` or the derivative identity. The new neutral atom/molecule
derivation in `../collective_response/COLLECTIVE_RESPONSE.md` provides a
different density/phase basis with the same static structure in its even
mass sector. Its odd-sector instability must also be checked before calling
that particular homogeneous neutral state stable.

The separately specified canonical host's lapse susceptibility has a
nonnegative local term plus an inverse amplitude kernel of this form.
Its interpretation as physical stress-energy response must retain the
proper phase-space Legendre transform and the specified lapse convention.
A full self-gravitating relativistic metric constraint problem is not
replaced by this scalar-probe theorem.

The hypotheses are not a classification of all phases. Momentum-dependent
source operators, flowing or inhomogeneous states, quantum/thermal nonlocal
kernels, a genuinely incompressible phase, physical support, extra gauge
constraints or other microscopic derivative interactions may fail them.
For example, a gapped conserved-density phase in another system can have
`chi(0,k)~k²`, giving inverse `1/k²`; continuity alone does not exclude it.
No such phase/operator has been derived for the present positive-density
carrier. An all-loop exclusion would require additional work.

## 5. Bounded implementation evidence

`check_kernel.py`, `contract.json` and `run_001/` record 75 exact/finite
controls. They check inverse-derivative and constrained Euler/energy
identities, five declared two-component matrices, fifteen positive-momentum
points, the sharp endpoint algebra and scalar-exchange sign. One example
uses an exact stable dilute-source NR background with `m=1`, `M=2.001`,
`c3=.0001`, `lambda_rep=.0001`, `mu=(M-2m)/1000`; it is explicitly the
retained-source RWA convention. No physical Newton constant was fitted to
that example. The general claims are proved in (2), (5) and (7), not
established by the finite count.

The runner pins the original action, prior response note and executed code,
with actual revision, software, caps and result hashes. The implementation
uses exact rational/algebraic arithmetic; displayed sample summaries are
binary64 conversions. The run is completed; its validator and focused
independent review are separate records. No external theorem is needed for
this inverse-matrix proof, and no novelty claim is made.
