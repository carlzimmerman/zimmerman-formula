# R2 audit: can finite stress supply finite current variation?

**Verdict: incomplete, with a specific missing derivative estimate.**
The present arguments establish vanishing layer mass of J_base from
finite stress, but do not establish a total-variation bound for the
specified full current J. This note neither constructs a native solution
violating that bound nor asserts that no such estimate can be proved.

Use the current representative and assumptions of
`COMBINED_CURRENT_EXCLUSION.md`, temporarily removing the finite-J
hypothesis. The exact decomposition is

    J=J_base-A curl(dPi),    0<A_min<=A<=A_max.

Finite stress already gives a uniform local L1 bound for J_base and its
vanishing layer mass. Consequently, obtaining a uniform local measure
bound for J is **equivalent** to obtaining a uniform local BV bound for
Pi (up to the known bounded base term and regular chart weights):

    ||dPi||_M <= A_min^-1 (||J||_M+||J_base||_M),
    ||J||_M <= ||J_base||_M+A_max ||dPi||_M.

Thus the exact missing estimate is a spacetime bound for both coordinate
derivatives of Pi. The signed endpoint argument bounds variation along
each clock slice, not the independent variation between clock slices.
Uniform convergence of Pi does not bound the latter variation.

## What the equations currently control

In a local orthonormal clock frame, define

    q=nP+2P n beta=exp(-2 beta)nPi.

Then curl(dPi)/E=D n-q e, and the exact full current is

    J/E=r(1-2 gamma D_eff)n+A q e.

The stress is algebraic in r,A,P,mu and n; it contains neither q nor nA.
The multiplier cancels from the displayed n coefficient, but that does
not yield a bound on the independent spatial current coefficient A q.
The exact constraints eA=W_P/r and ePi=exp(2 beta)D control the other
direction of differentiation. In a chart with unbounded boosts, conversion
of even those directional controls to coordinate variation additionally
carries unbounded clock-frame coefficients.

Differentiating the spatial constraints and using scalar evolution is a
plausible route to estimates for nA and nP. The earlier coercive inverse
estimates were proved on a compact on-branch hyperbolic state domain with
the required coefficient and geometric controls. They are not uniform
estimates for the present full-switch class with simultaneous unbounded
r and rapidity. In particular, applying those estimates here requires
proving the appropriate inverse remains quantitatively controlled across
the changing branch and controlling its sources without inserting the
unknown temporal variation or clock-frame derivatives into the constant.
The preceding local existence theorem does not provide that uniform
singular-layer estimate.

## Why bounded divergence is insufficient

The scalar equation gives div J=-E(V_phi+W_phi), a bounded source.
This controls one differential combination of two current components;
it supplies no coercive norm estimate for the divergence-free component.
For example, bounded functions Pi_k=k^-1 sin(k^3 t) converge uniformly to
zero, but ||dPi_k||_M grows like k^2 on a fixed rectangle. With constant
A, -A curl(dPi_k) has exactly zero divergence for every k. This is only
a counterexample to an estimate based on divergence and uniform Pi; it
is **not** a solution of the native polarization and scalar system.
The missing native-equation argument cannot be replaced by this example
in either direction.

An integration by parts does not fix the norm issue:

    J=J_base+Pi curl(dA)-curl(d(A Pi)).

It shifts the potentially unbounded derivative to A or to an improvement.
Even when A and Pi converge uniformly, small rapid loops can have large
variation. A finite-measure bound for a different improved current would
not automatically be a bound for the current required by the contraction
proof. The boundary ambiguity is therefore material to the admissible
class, not a change to the smooth native divergence equation.

## Exact remaining obligation

To remove finite-current control from the exclusion theorem, prove an
estimate of the form

    integral_K (|Pi_t|+|Pi_x|) dt dx <= C_K

for the relevant native layer solutions, with C_K independent of layer
width, maximum r, and maximum boost, from the retained stress, trace,
source and geometric bounds. Equivalently, prove a sufficient bound for
the temporal polarization derivative plus the necessary frame conversion.
Alternatively, one could replace the finite-current/product passage by
a separately justified weaker compactness theorem that controls its
nonlinear products. Neither implication is established by the arguments
audited here. The finite-current theorem remains valid and restricted;
removal of that assumption is an open differential estimate, not a
counterexample or a singular-selection theorem.

Independent delegated review, 2026-11-06. Read the actual PF10 exclusion
file with SHA256 recorded in COMBINED_CURRENT_AUDIT.md and the exact native
AC7 action in `action_search_2026_11_05/AC7_charge_switch/README.md`.
