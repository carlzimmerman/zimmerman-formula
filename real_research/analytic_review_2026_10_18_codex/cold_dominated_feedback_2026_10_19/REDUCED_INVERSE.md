# A conditional regular inverse after the actual mode poles

Checkpoint ZAR-2026-10-19-11-CX. Analytic derivation by `/root`.
Inputs: `BOUNDARY_PAIRING.md`, `REGULAR_INVERSE.md`, `THRESHOLD_MODES.md`, and
the actual cold-dominated geometry in `GEOMETRY_AND_CAP.md`. The hypotheses
include no full action-frequency critical point, finitely many nondegenerate
circular extrema, and the exact positive fixed-warmth distributions. This
result does not assert the additional force condition below is satisfied.

## 1. Exact statement

At a nonzero actual mode frequency `nu_0`, let `N=ker(I-K_+(nu_0))`.
Assume the following condition for **every field in this kernel**:

    phi_j'(s_c)=0 whenever
       |nu_0|=Omega_j(0,L_c(s_c))=kappa_j(s_c),
       kappa_j'(s_c)=0,  kappa_j''(s_c)!=0.             (CF)

Only the fundamental harmonics `k=+1,-1` need this extra condition. Higher circular
harmonics are already quadratic after the actual `C^(1,1)` eigenfield
bootstrap. The energy-mode geometry, cap and endpoint estimates supply
that bootstrap for the selected cold-dominated family.

Then, for some `alpha>0`, in a small closed upper-half neighborhood of
`nu_0`,

    (I-K(z))^-1 = R_(nu_0)/(z-nu_0)+B_(nu_0)(z),      (1)

where `B_(nu_0)` is bounded and `C^alpha` in operator norm on `Y_gamma`,
including at `nu_0`, and

    R_(nu_0)=nu_0 sum_(a,b) phi_a (Q_Gram^-1)_ab ell_b

is the leading residue already identified in `REGULAR_INVERSE.md`.
For example any sufficiently small `alpha<min(gamma,1/2)` is admissible.
The lower-half assertion follows by reciprocity. If (CF) fails, this proof
does not give a bounded pole-subtracted inverse; moreover the single-mode
work criterion already fails. No actual failing mode is constructed here.

## 2. Extra regularity available on the kernel

Every kernel field is the field of a genuine energy mode. For the actual
cold family the density bootstrap makes it `C^(1,1)` in radius. On compact
eccentric action charts its receiving coefficients are `C^(1,1)` in actions.
On circular charts they are `C^(1,1)` in the smooth variables `(a,L)`,
`a=sqrt(J)`. All norms on the finite-dimensional kernel are equivalent,
so these bounds are uniform on its unit sphere.

On a regular eccentric resonance choose `t=k Omega-nu_0` and a complementary
coordinate. The coefficient vanishes on the resonant curve. Away from
support boundaries, Hadamard division writes it as `t v`, with `v` Lipschitz,
since its first derivative is Lipschitz.

The same statement for the **weighted** coefficient holds in all regular
source charts without needing unweighted division across an exterior cap
level. Work with `G=sqrt(w) phi_k`. On compact eccentric charts `sqrt(w)`
is smooth for the actual inverse away from its flat zeros; at a cap or
angular-momentum end it has smooth flat extension. In fact near the top
cap the correction in the inverse vanishes, and the baseline has
exponential flatness; at the angular-momentum ends all inverse factors
are dominated by the fixed exponential profile. Thus `sqrt(w)` and its
first two derivatives are bounded in these charts. It follows that `G`
is `C^(1,1)` there. It is zero on every complete regular resonance after
zero extension, so `G=t v` with `v` Lipschitz. Alternatively this weighted
division can be used locally only in the support collar, while ordinary
division applies in its positive-weight interior.

At a regular circular crossing `partial_L Omega!=0`, perform this division
in `L`, keeping `a` fixed. The quotient has uniformly bounded Lipschitz
dependence in `(a,L)` and vanishes at `a=0`: this is immediate where the
detuning on that boundary is nonzero and extends to its zero by continuity.
The test coefficient of an arbitrary `Y_gamma`
field is `C^gamma` in `(a,L)` and vanishes like `a^gamma`; the zero-extension
product remains valid in the ordinary-action frequency charts. In charts
solving for `L`, the integration is over fixed `a>=0`, so no ordinary-action
division regularity at `a=0` is being asserted.

## 3. Circular threshold densities under (CF)

Use the exact boundary-preserving coordinates of `REGULAR_INVERSE.md`:

    k Omega-nu_0=epsilon*(b^2+x^2),
    dJ dL=b c(b^2,x) db dx,
    rho=sqrt(b^2+x^2).

For a kernel field let `g(b,x)` denote its weighted receiving harmonic.
At any resonant higher harmonic `|k|>=2`, the oscillator expansion and
`C^(1,1)` radial regularity give `g=O(rho^2)` and zero first jet at the
origin. For the fundamental, (CF) gives exactly the same conclusion.
In all these cases `g` is `C^(1,1)` and `|grad g|<=C rho`.

An arbitrary test-field coefficient `f` is `C^gamma` in `(b,x)`, vanishes
like `b^gamma`, and has bounded `C^gamma` norm. On the one-sided frequency
support `s=rho^2>=0`, a kernel/test coarea density has the form

    q_cross(s)=sqrt(s) integral_0^pi
          sin(theta) g(sqrt(s) sin(theta),sqrt(s) cos(theta))
          f(sqrt(s) sin(theta),sqrt(s) cos(theta)) c(...) dtheta.

Consequently `q_cross(s)=O(s^((3+gamma)/2))`, and
`q_cross(s)/s` has a zero-extended `C^gamma` norm controlled by the test norm.
Here is the local increment check. Put `rho=sqrt(s)`, `rho'=sqrt(t)`,
`h=|s-t|`, and suppose `h<=s/2`. The factor `g/rho` is Lipschitz in `rho`
and is `O(rho)`. The change in `f` contributes at most
`C rho^(1-gamma) h^gamma`. The change in `g/rho` contributes at most
`C h rho^(gamma-1)<=C h^gamma` on this range. Smooth angular Jacobians
obey the same bound. If `h>s/2`, the value bound
`O(s^((1+gamma)/2))` controls the increment by `C h^gamma`, since
`(1+gamma)/2>gamma`. Integrating in angle proves the assertion.

For two kernel fields,

    q_00(s)=sqrt(s) integral sin(theta) g_a^* g_b c(...) dtheta

satisfies `q_00(s)/s^2 in C^(1/2)` after zero extension. Indeed the integrand
after division is `g_a^* g_b/rho^3`, which is `O(rho)` and Lipschitz in
`rho`, using `g=O(rho^2)` and `grad g=O(rho)`. Composition with `sqrt(s)`
gives the asserted exponent. Factors varying smoothly with frequency do
not reduce these bounds.

## 4. Exact divisibility of the frequency blocks

Write `delta=z-nu_0`. For a compactly supported density and its Cauchy
transform, whenever the displayed quotients extend as above,

    Cq(delta)-Cq(0)=delta C(q(t)/t)(delta),
    Cq(delta)-Cq(0)-delta C(q(t)/t)(0)
                       =delta^2 C(q(t)/t^2)(delta).    (2)

These identities follow by algebra under the integral, with the same
upper-boundary convention on both sides. The stated Holder bounds justify
the boundary limits and give operator-norm `C^alpha` Cauchy transforms.

On regular charts a cross density is `t` times a `C^gamma` density, by
Section 2. A kernel/kernel density is `t^2` times a Lipschitz density.
On circular threshold charts Section 3 supplies their respective quotients.
Nonresonant charts and the infinite nonresonant harmonic tail are analytic
with the required first two derivatives: differentiated multipliers are
`O(1/|k|)` and `O(1/k^2)`, and Parseval bounds their bilinear sums.
Thus (2) applies to the complete, rather than merely localized, blocks.

Choose fixed Fredholm domain/range complements at `nu_0`. In this block
decomposition the two off-diagonal blocks vanish at zero and have the form

    A_01(z)=delta B_01(z),   A_10(z)=delta B_10(z),

where `B_01,B_10` are bounded `C^alpha` maps. The kernel/cokernel block is

    A_00(z)=delta M+delta^2 C_00(z),
    M=Q_Gram/nu_0,

with `C_00` bounded `C^alpha`. The complementary block has a bounded
`C^alpha` inverse. All these statements use kernel fields on both sides
where required, rather than differentiating `K` twice on arbitrary Holder
fields.

## 5. Schur inversion leaves a regular remainder

The Schur complement is exactly

    S(z)=delta[M+delta C(z)],
    C=C_00-B_01 A_11^-1 B_10,

where `C` is bounded `C^alpha`. Positivity of the actual `Q_Gram` makes
`M` invertible. Hence

    S^-1=delta^-1 M^-1
            -M^-1 C(z)[M+delta C(z)]^-1.

The second term is bounded `C^alpha` through zero. In the other inverse
blocks the factor `delta` from every off-diagonal block cancels the possible
simple pole. Ordinary block inversion proves (1), with a bounded Holder
remainder on the entire field space. This discharges the reduced-inverse
obligation **conditional on (CF)**; it does not prove (CF).

Together with `HIGH_FREQUENCY_INVERSE.md`, there are only finitely many
mode neighborhoods for the selected halo. This result reduces their
threshold obstruction to the actual fundamental circular force traces.
Transferring the regular remainder to the full work estimate still requires
the standard smooth-source transform estimates and the receiving-harmonic
summation with their actual conventions; those steps are not relabeled as
proved by this operator statement.
