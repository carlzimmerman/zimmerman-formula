# IC35: finite-multiplier switch collars and first-preservation-selected profiles

Base 2b8d5dd4169a4fa62c87f2ed6ed7d2e50e72a239, 2026-09-09.
The original complete-theory target remains **OPEN**.
Credit: Carl Zimmerman's exponential constitutive law, vacuum-scale relation,
and primordial-clock direction motivate the same-action construction.
This is not an empirical fit, a novelty-priority claim, or a full matched galaxy.

## 1. The actual switch and regularity question

Retain the IC29/30 full action, its fixed IC32 repaired 81-node D(S)
approximation, A=.1, E4=.01, wc=-.025, m=1 and h0=.5. The activation is
the existing IC18 smooth function of

    alpha=-exp(-3w)q/(3m h0).

It is zero for alpha^2<=1/2 and one for alpha^2>=3/4. In between,

    eta = a/(a+b),
    a=exp[-1/(alpha^2-1/2)], b=exp[-1/(3/4-alpha^2)].

The pin density is J eta exp(S) ell(w-wc). Variation precedes all restrictions.
Whenever eta>0 its multiplier equation enforces w=wc. The independent w equation
then reads

    W_vac - p_w + eta exp(S)ell = 0.

A generic nonzero W_vac-p_w would require ell proportional to 1/eta.
Finite ell needs W_vac-p_w=O(eta), not merely a small absolute numerical residual.

The construction tested here sets ell=0 and solves W_vac-p_w=0 as an actual
equation. For first preservation it also selects the data so that
ell_dot=0 and (W_vac-p_w)dot=0, with w=wc and wdot=0 on the initial slice.
It NEVER estimates ell by dividing a floating residual by tiny eta.

This is a regular initial/first-jet ansatz, not proof of a uniform nonlinear
extension: finite numerical error divided by arbitrarily tiny eta is uncontrolled.
Higher preservation and time-evolved matching remain necessary.

## 2. The spatial equations have a nondegenerate second-jet matrix

Use the radial action and independent metric evolution equations of IC30/33.
C denotes the total lapse equation and W=W_vac-p_w the unmultiplied w equation.
With ell=0, w=wc and zero w spatial derivatives, variation shows that C and W
are independent of eta even in the transition interval. No eta derivatives
are discarded before variation.

The actual coefficient matrix of (S'',Q'') is

    M = 4v exp(-2Q) [[1-u^2, 1], [-(2-u^2), -2]],
    v=m exp(S+2wc)/2, u=(S+2wc)/(S+wc).

The script obtains M by differentiating the varied equations and computes

    det(M)=16v^2 u^2 exp(-4Q).

Thus on the stated regular chart with m>0 and u>0, both equations can be
solved algebraically for the second spatial jets. This is a constraint-Euler
coefficient matrix, NOT a Poisson-bracket matrix and NOT a DOF count.

At the formal u=0 point the script computes rank 1. That calculation does not
supply the missing extension of D(S) to that point or resolve the zero-field
constraint stratum. No u=0 regularity claim follows from the u>0 construction.

## 3. Initial collars across the whole activation interval

The first family prescribes a C3 clock-momentum profile on r in [2,2+L]:

    q=q_out f((r-2)/L),
    f(x)=35x^4-84x^5+70x^6-20x^7,

with q_out taken from the same fixed-action reference state, not refitted.
Set initial w=wc, ell=0, and both fluid spatial gradients to zero.
Each fluid has the same positive canonical density as the reference state
on THIS initial slice. Its later dynamics are not frozen.

Solve C=W=0 for S'',Q''. The independently varied momentum and shear-gauge
equations give

    sh'=-q'/2-3(Q'+1/r)sh,
    beta'=beta/r-t sh.

This defines a six-component spatial ODE for (S,S',Q,Q',sh,beta).
At r=2 set S to the midpoint of the fixed coefficient interval, Q to the
reference Q, and S'=Q'=sh=beta=0. These are diagnostic initial choices,
not measured galactic boundary data.

Runs with widths .01 and .02 span eta=0 through eta=1 with finite ell=0.
The full metric equations determine their qdot and shdot; those rates are not
zero in general. Therefore these collars are NOT certified static galaxies,
even where q=0 initially.

## 4. First preservation selects a clock profile rather than accepting a guess

An arbitrary smoothstep profile need not have regular time derivatives of
the multiplier. In the second family q(r) is therefore an UNKNOWN, determined
alongside the lapse rate U(r)=Sdot(r). U here is not the constitutive primitive
U(c) in the action.

All full metric time rates come from IC33, including Q',Q'',q' and shear.
The initial fluid gradients vanish but their first rates are nonzero:

    (sigma_i')dot=(1+w_i) H_i S'/j_i,
    j_i,dot=-3HQ j_i, HQ=h_q/2.

This contributes -3HQ(rho+p) to Cdot and the corresponding weighted trace
term to Wdot. Omitting that matter response would change the construction.

Let Fz=2D+12E4 z^2>0 on the selected auxiliary branch. Spatial differentiation
of Aq+2Dz+4E4z^3=0 and of the momentum constraint gives the q'' coefficients

    z'' = -(A/Fz) q'' + terms independent of q'',
    sh'' = -q''/2 + terms independent of q''.

Using the actual Qdot and shift equations, the direct t q'' terms cancel,
leaving the derived coefficient

    d(Qdot'')/d(q'') = gamma = A^2/(2Fz).

The code checks this both algebraically and by varying q'' in its full
field-jet chain rule. Spatial third jets S''',Q''' are obtained by differentiating
C=W=0; no interpolated Qdot'' source is substituted.

After eliminating zdot from the differentiated z constraint, write

    Cdot = c2 U''+c1 U'+c0 U + fC + C_Q'' gamma q'',
    Wdot = w2 U''+w1 U'+w0 U + fW + W_Q'' gamma q''.

Here fC,fW are evaluated with q''=0; subscripts Q'' indicate partial derivatives
with respect to that spatial jet, not differentiation of the whole equation.
c2=C_S'', w2=W_S''. Consequently the actual matrix for (U'',q'') is

    M1 = M diag(1,gamma),
    det(M1)=gamma det(M).

It is nonzero on the selected regular branch with A!=0 and Fz>0.
No desired rank or determinant is assigned to either matrix.

Solving these equations with Cdot=Wdot=0 determines q'' AND U''.
The spatial integration state is

    (S,S',Q,Q',sh,beta,q,q',U,U').

These ten ODE variables are initial fields and jets, NOT ten propagating
physical degrees of freedom. A full canonical/Dirac analysis remains separate.

At r=2 use the same S,Q values and zero initial S',Q',sh,beta, set

    q=-3m h0 exp(3wc)/sqrt(2), q'=-100, U=U'=0,

and integrate in BOTH radial directions. The center is the actual eta=0
switch edge. Widths .002,.004,.006 are tested; the widest reaches both the
inactive and fully active plateaus. This family's profile is selected by
first-preservation equations; it is not the prescribed smoothstep family.

## 5. Numerical scope and independent checks

Use DOP853 with dense output, no coefficient extrapolation.
The prescribed-profile solver has rtol1e-11, atol1e-13, maximum step L/100.
The first-preservation solver has rtol1e-10, atol1e-12, maximum step L/160.
Tests sample 401/801 points, as recorded in the run contract.

Independent five-point differentiation of the integrated dense solution checks
the first-order spatial ODE, lapse/w equations, momentum, and shift gauge.
It also differentiates the full metric qdot and shdot rates to check momentum
preservation, including the generated ordinary-fluid momentum.

The directly solved C/W and Cdot/Wdot residuals alone are not independent
proofs: they are linear-system residuals. Dense-solution differential defects
and the independent momentum-preservation check are reported separately.
Smaller finite-difference spacing can increase roundoff; the 401/801 audit
is not automatically a convergence theorem.

Activation values are evaluated with mpmath for log reporting. The existence
of tiny positive eta does not turn an absolute residual into a relative bound
on ell. The construction specifies ell=elldot=0 and solves their undivided
equations; a continuum/interval certificate near the switch remains absent.

## 6. What this does and does not establish

The exact algebra removes an immediate local second-jet obstruction.
Numerically, mixed-activation constraint data and first-preservation-selected
profiles can be constructed without changing the action coefficients or
introducing a divergent multiplier into the data.

This is NOT:
- a matched static MOND galaxy and FLRW spacetime;
- a higher-preservation or many-step evolution across the switch;
- a full Dirac bracket/DOF, PPN, stability, causal-response or strong-coupling proof;
- a resolution of the u=0/y=0 chart or global coefficient extension;
- an empirical cluster, binary, galaxy or CMB result;
- a derivation of the vacuum-scale coefficient 1/2 or a Lean certificate.

The next unavoidable calculation is the second time-preservation condition
and then actual mixed-branch evolution with regular multiplier and moving
interface conditions. The selected collar still needs physical inner/outer
matching, not just a numerical interval crossing. Do not infer all higher
preservation from the first one, or divide by eta while ignoring conditioning.
The complete original requirements remain intact and the full theory OPEN.
