# Independent audit: direct bounded variational weak equations

**Verdict: proved as a well-defined boundary-reduced EL--KKT weak
formulation extending the native smooth equations.** This removes the
need to define products in the expanded gradient equations. It proves
neither existence from the terminal BV data nor uniqueness, and does not
identify every singular interpretation of the original higher-derivative
action with this formulation.

Reviewed `pf13/BOUNDED_WEAK_FORM.md`, SHA256
`a2fb87693b2104c1ddaca4c3ac7a052c94277880f5d7aa374165fe7b2b64cabb`,
and `pf13/CONTRACT.md`. Independent delegated audit, 2026-11-06.

## 1. Function class and variation

Take phi,A,Pi locally W1,infinity, dphi locally BV, and compact strict
timelike/cap ranges. In a regular conformal metric let

    E=exp(2 alpha+2 beta), P=exp(-2 beta)Pi,
    r=exp(-alpha)sqrt(phi_t^2-phi_x^2)>=r_min,
    Q=Ar>=1, mu>=0, mu(Q-1)=0.

The candidate's C1 metric with locally integrable distributional second
derivatives is a sufficient concrete class for its curvature and bounded
stress equation. The metric and inverse must remain nondegenerate and
locally bounded; these requirements are part of the compact regular chart.
More singular metric classes need their own specified curvature/junction
definition and are not silently included.

The action density

    L=E[H-mu(Ar-1)]-A(phi_t Pi_x-phi_x Pi_t)

is locally integrable. Smooth compact variations of phi,A,Pi have
well-defined first variations. Small phi variations remain timelike
because the domain margin is strict. The multiplier is interpreted by
the KKT conditions, not by an unconstrained multiplier variation that
would incorrectly impose Ar=1 everywhere. All stationarity equations
below are equations for the augmented density plus those KKT conditions.

## 2. Direct Euler equations, with signs

Use H_A=r D_eff, H_P=-W_P and
D_eff=(Ar-1)/gamma-r^2. Variation of A gives the a.e. identity

    phi_t Pi_x-phi_x Pi_t=E r(D_eff-mu)=E r D.

For Pi the canonical derivatives are

    L_Pi=-exp(2 alpha)W_P,
    L_Pi_t=A phi_x,    L_Pi_x=-A phi_t.

Its distributional Euler equation is therefore

    -exp(2 alpha)W_P-partial_t(A phi_x)
                          +partial_x(A phi_t)=0,

which reduces exactly to

    phi_t A_x-phi_x A_t=exp(2 alpha)W_P

almost everywhere. This cancellation remains valid at the stated
regularity: A is Lipschitz, dphi is BV, the mixed derivatives of phi
commute distributionally, and the potentially singular terms are
multiplied by the same continuous A and cancel. Equivalently it is the
distributional exterior-product identity d(A dphi)=dA wedge dphi.

Since partial r/partial phi_a=n^a, the scalar current is

    J^t=E(h-mu A)n^t-A Pi_x,
    J^x=E(h-mu A)n^x+A Pi_t.

The scalar equation and its test form are

    div J=-E(V_phi+W_phi),
    integral J^a partial_a eta=integral E(V_phi+W_phi) eta.

The signs in the actual file pass. All currents and displayed products
are bounded measurable functions. Indeed the A equation also bounds mu
from the bounded derivatives, r_min and compact constitutive variables;
assuming bounded mu explicitly is consistent. No derivative-measure
product R n(r) or D_r n(r) is introduced.

## 3. Relation to the first-order native density

The algebraic minimization in A at fixed r,D is strictly convex:
H_AA=r^2/gamma>0. With Ar>=1, it gives

    Q=1+gamma max(D+r^2,0),
    mu=max(-(D+r^2),0).

Eliminating A,mu in H-QD recovers exactly the boundary-reduced native
density F=-D+r^2/2-V-W minus the full-switch quadratic correction.
The envelope derivative agrees with the displayed first-order currents
almost everywhere, including the C1 switch. Thus within the stipulated
auxiliary regularity class this is an actual weak variational formulation
of that boundary-reduced action, not an arbitrary replacement PDE.

This statement does not prove the same regularity for A reconstructed
from every weak solution of F. Nor does it prove equivalence to an
undefined distributional acceleration expression in the original action.
The earlier replacement of P.acceleration by -D removed a divergence
involving clock derivatives. At singular gradients its direct reading
requires boundary/product conventions. The specified weak formulation
and Noether-current representative are explicit choices of mathematical
extension of the equivalent smooth variational equations, without adding
a new bulk interaction or regulator.

## 4. Metric equation and why it remains essential

On shell of the algebraic constraint, variation at fixed A,Pi gives

    T_ab=H g_ab+(r h-mu Ar)n_a n_b,
    T_perp=H+P W_P.

The topological density has no metric dependence in these variables.
The transverse P variation supplies P W_P. These are bounded functions,
so they carry no matter surface measure in this bounded class. The
metric-dependent field redefinition is legitimate for the displayed
auxiliary variational system; it must not be used to define otherwise
undefined products in a different singular formulation by assertion.

Full Einstein equations are imposed as independent weak equations.
Weak field Euler equations do not automatically supply inner-variation
stationarity or the smooth Noether multiplier identity at gradient jumps.
The smooth identity multiplies the scalar equation by dphi and uses
chain rules for the stress. A BV dphi can jump, so that multiplication
and chain-rule step is not supplied by the weak scalar equation alone.

For an explicit general illustration, take a Lorentz-invariant scalar
L=F(X), F(X)=(X-3/2)^2/2, and phi=2t+max(x,0) in flat 1+1 spacetime.
Then X is 2 on the left and 3/2 on the right. The normal scalar flux
F_X phi_x vanishes on both sides, so the scalar Euler equation holds
weakly. Nevertheless T_xx=F_X phi_x^2+F jumps from 1/8 to 0, and its
divergence contains a delta. This is not an AC2q solution or counterexample;
it directly demonstrates why the asserted general weak Noether inference
would be invalid. The native full stress conditions still have to be
checked, rather than inferred by that chain rule.

No generic entropy inequality has been adopted. The full Einstein/stress
equalities may be stronger than an entropy inequality for a selected
reduced subsystem. An entropy solution of that subsystem need not solve
these full variational equations.

## 5. Jump conditions for piecewise regular members

Assume a regular interface and regular one-sided traces. Continuity of
the Lipschitz fields phi,A,Pi gives common tangential derivatives of their
traces. For a normal covector nu, the scalar distributional equation gives

    [J^a nu_a]=0.

The Pi canonical normal flux is

    (A phi_x,-A phi_t).nu.

Its jump is zero because A and the tangential phi derivative are common.
The a.e. Pi equation on each side and its weak variational form retain
the normal polarization condition; the A equation relates the normal
Pi derivative to D on each side. In a locally orthonormal interface chart
with common tangential slope s, the conjugate factor is A s, as in the
earlier corner derivation. There is no additional independent A flux:
A enters this before-IBP action without derivatives.

With bounded stress the Einstein equation has no matter delta source.
In a regular junction geometry Israel therefore gives zero extrinsic
curvature jump (and the common intrinsic geometry is already continuous).
The outer Einstein/Codazzi and Gauss constraints then give the ordinary
normal stress/energy flux conditions. These assertions use the regular
piecewise metric hypotheses; they are not an unproved weak Bianchi
theorem for arbitrary distributional metrics.

Thus the direct weak equations recover the earlier normal scalar,
polarization and full stress matching. They do not evade the audited
small-acoustic regular-corner obstruction. A general weak member need
not have such a regular interface or traces, so no classification of all
bounded BV solutions follows.

## Remaining theorem, now stated precisely

There is a concrete weak system; the absence of a definition for expanded
BV products is no longer a reason to stop. The missing work is to prove
existence from the terminal incoming data and uniqueness in this specified
full-equation class, or to prove nonexistence in it. Weak compactness of
the individual bounded factors alone does not pass their nonlinear
products or the obstacle constraints. A spatial auxiliary inverse alone
does not provide such an evolution construction. No claim of existence,
nonuniqueness, or a selected singular continuation is made by this audit.
