# IC31: nonlinear constrained exterior for the clock bridge

Base `90489d78165de9252ae984e5728f111373ae9640`, 2026-09-09.
**Full theory OPEN.** The previous goal turn made substantive progress:
IC30 derived the radial action and constructed momentum-compatible collar
data. This checkpoint solves the previously unfulfilled lapse and multiplier
equations on the pinned exterior. It does not claim the pin-off transition
has been solved, or replace that target with a homogeneous solution.

Credit: Carl Zimmerman's exponential constitutive law, vacuum-scale relation
and primordial-clock direction motivate this construction. No empirical fit,
new measured law or global novelty claim is made. The factor1/2 in his scale
relation remains input, not a derivation.

## 1. Hold the action fixed

Use the entire IC29 constant-tensor phase action as varied in IC30, with
v=v0, A=.1, E4=.01, h0=.5, wc=-.025, m=1, kappa=6 and the same two
minimally coupled fluid actions. D(S) is not reconstructed when changing a
radial source. IC29's constructed Q[0,1] history supplies fixed41/81-node
quintic-Hermite representations of D(S). Each is one fixed C2 approximate
action; agreement between them is not proof of an exact or global extension.

The reference state is at Q=.1. Its q and uniform fluid canonical momenta
are held fixed on the initial radial exterior. Sbar is found from the actual
homogeneous constraint of the supplied coefficient table. The lapse Schur
derivative is an output, not reset to the design target -1000 after adding
shear. No coefficient extrapolation outside the represented S interval is
allowed, including at nonlinear solver iterates.

On the initial slice Q is spatially constant, NOT constrained to be constant
in time. Ordinary fluid spatial gradients and radial momentum flux vanish
initially. The phase-space matter density is the same minimal-coupling
Hamiltonian as IC23/29, not a prescribed nonmetric force.

## 2. Derive the elliptic equation from the off-pin action first

`symbolic()` imports the actual eight IC30 Euler equations. It differentiates
before setting w=wc and eta=1. It then verifies the independent compact
expression below. With sh denoting the trace-free momentum amplitude,

    v=m exp(S+2wc)/2, t=exp(2S)/v,
    u=(S+2wc)/(S+wc), B=2v(1-u²),
    h=-tq²/6-Aqz-exp(S)P0-Dz²-E4z⁴,

the normalized Hamiltonian lapse constraint is

    C_S=h_S+rho_H+(2/3)t sh²
        +exp(-2Q)[B_S S'²+2B(S''+2S'/r)]=0.

Subscripts here are partial derivatives before auxiliary elimination; q,z
are independent fields. The action functions remain fixed functions of S:
they are differentiated with S, not varied as new fields or refitted. The sh² term
uses t_S=t, which holds for THIS constant-tensor action. The phase-space
fluid source rho_H is proportional to exp(S) at fixed Q and fluid momenta.

Solve the same-action auxiliary equation first:

    Aq+2Dz+4E4z³=0.

For D>0,E4>0 its unique real root is the IC30 hyperbolic expression. It is
substituted only after varying the action, so the reduced Hessian is
`h_SS-h_Sz²/h_zz`, not the unreduced h_SS. Numerical residuals are retained.

IC30's exact momentum equation permits

    sh(r)=amplitude*C_tail/r³, q'=Q'=0,
    C_tail=(7/4)(-q_reference).

This solves the spatial momentum constraint on the exterior. It does not
assert that an interior meeting the chosen boundary data already exists.

The lapse boundary-value problem is solved on 2<=r<=R with

    S'(2)=0, S(R)=Sbar.

These are explicit diagnostic boundary choices, not derived galactic
matching conditions. R=8 is the primary finite domain; R=12 tests sensitivity
of its inner response. Shear remains nonzero at R, so neither boundary is
claimed to be an exact join to FLRW or the infinite-radius limit.

## 3. Solve the remaining pinned auxiliaries without dropping matter

The full off-pin w variation supplies E_w^(0) and its actual ell coefficient.
The symbolic calculation verifies that this coefficient is exp(S), after
normalizing by J and setting eta=1. Thus

    ell=-[E_w^(0)/J-p_w,H]/exp(S).

For each minimally coupled fluid of equation-of-state parameter w_i,

    H_i/V=h_i(S,Q) exp[(1-3w_i)(w-wc)],
    p_w,H=sum_i (1-3w_i)h_i.

This off-pin derivative is essential: using only the lapse matter source
would omit the trace coupling in the multiplier equation. Here the code
retains it, verifies the derivative identity, and records the resulting ell.
The pin equation E_ell=0 is satisfied by w=wc, and the actual activation
argument is checked to remain on eta=1 throughout this exterior.

The shear equation is

    beta'-beta/r=-t(S)sh.

Rather than reuse IC30's constant-t formula, integrate the variable coefficient:

    beta/r=-integral_2^r t(S(R))sh(R)/R dR.

The omitted additive constant is only the residual shift convention. A
cubic representation of the integrand is integrated, and the shear equation
is independently checked at the intervening midpoints. The q Euler equation
then determines Qdot. On the pinned slice the physical normal expansion is

    H_normal=exp(-S-wc)[-tq/6-Az/2].

This follows from Qdot minus one third of the shift divergence; it is not
identified with Qdot alone. Positive values establish an expanding initial
slice, not a viable time-evolved cosmology by themselves. The Q Euler equation
still determines qdot, and full constraint preservation must still be solved.

## 4. Actual radial constraint linearization

At fixed q,sh,Q and fluid momenta, after eliminating z, the linearized lapse
constraint takes the self-adjoint radial form

    L f = (1/r²)(r² a f')' + V_L f,
    a=2B exp(-2Q),
    V_L=h_SS-h_Sz²/h_zz+rho_H+(2/3)t sh²
          +exp(-2Q)[2B_S(S''+2S'/r)+B_SS S'²].

Both the potential and the coefficient of f' are checked by differentiation
of the actual varied equation, not inserted as target stability parameters.
For a>0 and V_L<=-epsilon<0 everywhere on a finite interval, with
f'(2)=0 and f(R)=0, integration by parts gives

    integral r² f Lf dr
      =-integral r² a f'² dr+integral r² V_L f² dr < 0

for every nonzero real admissible f. Thus the homogeneous radial lapse
boundary problem has no nonzero kernel under those stated hypotheses.
This elementary conditional argument does not infer a uniform bound from
sampling, and does not count the full nonlinear theory's constraints.

The numerical code samples the actual a,V_L and also constructs the
128/256-cell finite-volume Jacobian in the r²dr measure. The inner boundary
has zero flux; the outer Dirichlet face uses the actual half-cell distance.
The symmetric tridiagonal matrix's largest eigenvalue is calculated, not
assigned. Its grid values are reported. These are auxiliary boundary-operator
eigenvalues, NOT the propagating scalar frequencies or a ghost test. The
matrix is not advertised as a Poisson-bracket matrix or a k=0 DOF count.

## 5. Numerical checks and limitations

Test amplitudes0,.5,1,2 for EACH fixed coefficient table. BVP initial grids
have121/241 nodes, tolerance1e-9, max12000 adaptive nodes. The model checks
the coefficient domain at every evaluated iterate. The zero-shear control
must return the homogeneous solution; nonzero shear must give a nonzero
lapse response rather than a hard-coded background.

The represented slope is integrated to define the reported S itself, so its
first derivative is precisely the represented slope. The second derivative
is independently obtained by differentiating that slope polynomial. The
original lapse constraint is then evaluated at2001 points with these jets,
not with S'' replaced by the differential equation's right-hand side. The
difference from the solver's S component is also recorded. Thus its residual
is a numerical check capable of failing, not an algebraic zero imposed by
the solver formula.

The w residual is an algebraic back-substitution check, not independent
evidence for evolution or the pin-off limit. Finite ell and a nonzero derived
coefficient establish solvability only on this pinned exterior. Pin-off still
requires the separate compatibility condition analyzed in IC30.

Preliminary runs reach amplitude2 without leaving the coefficient interval
approximately[.1,.104953195]. At amplitude1 the inner lapse changes by about
4.9864e-4, with ell near13.334 there. These are dimensionless model outputs,
not observed galactic potentials. Final authoritative numbers and statuses
belong to the bounded run records, not this preliminary summary.

## 6. Exact remaining implication

This is a nonlinear constrained initial exterior, not a completed spacetime.
The constructive next step is to derive the q evolution and preserve C_S,C_z
using the actual inhomogeneous Qdot,qdot, matter evolution and shear evolution.
Then connect its inner boundary to a solution crossing eta=0 into the
unpinned MOND branch. The chosen Neumann boundary is not that connection.

The fixed C2 tables must ultimately be replaced by a controlled single global
coefficient function, including derivative regularity needed for evolution.
The remaining original requirements are unchanged: full nonlinear Dirac
closure and all homogeneous/zero-field strata, healthy counted clock and
tensor modes through the transition, causal response and interaction scales,
full PPN and measured coupling, realistic cosmology and empirical tests.
Neither the vacuum-density arithmetic nor seven designed e-folds is a CMB
fit. No Lean certificate is claimed; Lean/lake were absent on the checked PATH.

Use the Mathbox bounded runner for the new scientific script and the full
closure suite. Strict scientific exit2 means all scoped checks passed but
the full theory remains OPEN; exit1 means a scoped check actually failed.
The finite evidence and analytical identities receive self-review and
mathematical proofreading, not an independent referee certificate.
