# CS28 continuation: exchange the free coupling for a hierarchy

This gives a sharper conditional formula, not a predicted number. Keep the
MV28 one-loop SU(5) beta function and its common-threshold vacuum condition.
Define the positive gauge integration constant Lambda_5 by

    1/g^2(mu)=10k ln(mu/Lambda_5),   k=1/(16pi^2),
    L=ln(mu_*/Lambda_5)>0.                                 (7)

Here mu_* is the renormalization scale used at the trial radial minimum.
Lambda_5 is the formal mass-independent SU(5) one-loop integration constant,
not a demonstrated confinement scale of an unbroken low-energy gauge group.
Thresholds and the proportionality between mu_* and the field amplitude
remain uncomputed. The equation defines the convention for this calculation.

At the radial stationary surface g_*^2=29lambda_*^2/200,

    lambda_*^2=320pi^2/(29L),
    alpha=h_*^2/lambda_*^2,
    B_curv/V_model = C(alpha)/L^2,
    C(alpha)=100alpha(16alpha+13)/[87(1+30alpha)].            (8)

This is the original leading-log formula with its coupling eliminated in
favor of a hierarchy. It has two independent dimensionless inputs,
alpha and L, rather than two free Yukawa couplings. No parameter has been
measured or fitted to obtain (8).

If, additionally, the SU(6) block normalization alpha=1/30 holds specifically
at mu_*, the coefficient collapses to a rational number:

    C(1/30)=7/27,
    B_curv/V_model=7/(27L^2),
    V_tree=f_*^2/2,
    B_curv=7f_*^2/(54L^2).                                 (9)

This is a conditional relation between a stiffness and a scale hierarchy.
It is not a universal numerical stiffness ratio. In particular L is not
selected by dimensional transmutation alone: a renormalization-group
integration constant must be matched to the vacuum scale by extra dynamics.
The absolute parameter f and full gravitational matching are also open.

## The normalization is a boundary condition, not an RG invariant

It would be incorrect to impose an SU(6) relation at an unspecified high
scale and assume it survives the broken SU(5) running down to the vacuum.
At alpha=1/30 on the SU(5) stationary surface, equation (2) gives

    d ln(alpha)/dt=(8/5)k lambda_*^2=32/(29L)>0.            (10)

Thus (9) needs matching at mu_* or a full enlarged-theory calculation that
actually delivers alpha(mu_*)=1/30. A larger-group normalization by itself
does not supply that dynamical matching. Equation (8) is the applicable
formula when the low-energy alpha differs.

## Can making h and lambda dynamical choose them?

As a minimal trial, treat h and lambda as independent positive moduli,
holding f fixed and adding no stabilizing-sector potential. At tree level

    U=f^2/(1+30alpha),
    (partial U/partial ln h)/U=-60alpha/(1+30alpha),
    (partial U/partial ln lambda)/U=+60alpha/(1+30alpha).    (11)

There is no stationary point at finite positive alpha: this construction
pushes the ratio toward a boundary instead of selecting it. At alpha=1/30
the two logarithmic slopes are -1 and +1, respectively. Merely renaming
couplings as fields does not stabilize them. Their kinetic terms, f
dependence, extra F terms and stabilizing potentials would be new physical
inputs. Loop stabilization or strong dynamics is not excluded by this
tree-level calculation; it requires a specified model and its own check.

## Next discriminating model

A useful replacement must supply more than a relation between two cubic
coefficients. It must (i) produce preferential B anomalous-dimension terms
satisfying DERIVATION.md equation (6) if perturbative fixed-point selection
is intended, (ii) evade that file's interior-SCFT obstruction by changing
its hypotheses or field content, and (iii) stabilize the scale hierarchy
and coupling ratio rather than treating them as adjustable matching data.
One must then redo the full threshold, vacuum and gravity calculation.
No such completed replacement is claimed here.
