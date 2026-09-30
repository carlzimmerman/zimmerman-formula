# Outer modes and a finite trace-shooting transition

Status: exact linear-mode derivation plus finite nonlinear event classification.
This is self-review. It does not supply a smooth global solution or select 32π.
Base da55ac3fa9745c12a7192a12dfd0b65d8d801f68. The necessary system and
numerical stabilization are defined in EXPANSION_BRIDGE_RADIAL_RESULTS.md.

## Exact linear equations from the nonlinear radial system

Around the P=0 de Sitter branch write N=1+Phi, sigma=Psi,
W=−H+deltaW, theta=3H+deltaTheta. Put B=lambda−1>0 and
S=3lambda−1. To first order the necessary equations are

    Phi'=P,
    Psi'=rP'+P,
    B deltaTheta'=2HrP'+4HP,
    deltaW'+(deltaTheta+3deltaW)/r−H(Phi'+Psi')=0,
    HS deltaTheta+2Psi/r²−2P/r=0.

Five exact symbolic differentiations check these linearizations against the
nonlinear polarization, gradient, momentum, trace and constraint equations.
The cubic beta interaction drops out at this order; no unproved import of
vacuum stability or cosmological scalar dynamics is used.

Differentiating the constraint and using the gradient and momentum equations
gives

    P'=−B deltaTheta/(H r²)−2P/r,
    deltaTheta'=−2deltaTheta/r.

The general solution of this linear system is

    deltaTheta=Ctheta/r²,
    P=Cp/r²+B Ctheta/(H r³),
    deltaW=−lambda Ctheta/r²+Cw/r³,
    Psi=−HS Ctheta/2+Cp/r+B Ctheta/(H r²),
    Phi=Cn−Cp/r−B Ctheta/(2H r²).

Eight further symbolic identities verify these modes and their boundary
constants. The final v2 script therefore checks thirteen exact identities.

If one imposes the *specific normalized flat-spatial de Sitter foliation*
boundary Psi→0, then Ctheta=0 in this linear family. Choosing Phi→0 also
sets Cn=0. Cp and Cw remain: the surviving P tail is Cp/r².
This is a chosen foliation boundary, not a theorem that every asymptotically
de Sitter geometry must satisfy Ctheta=0. A constant spatial asymptote and
other foliation data cannot be silently excluded on geometric grounds.
Likewise the formal large-r mode expressions do not independently establish
a horizon-regular or uniformly valid nonlinear continuation.

This identifies an actual matching obligation. The local deep-MOND annulus
has P proportional to 1/r, whereas this chosen linear outer branch has P
proportional to 1/r². One must connect them through the nonlinear radial
system; extending the local reduced profile indefinitely is not a solution.
The beta normalization remains absent from the outer linear equations.

## Fixed-coupling finite shooting experiment

Keep beta=10, lambda=2, H=1 and the same initial-flux label GM=1e−16.
The inner radius is 1e−6. Vary only

    deltaTheta0=factor beta P0³/[9(lambda−1)], deltaW0=0,

and resolve the initial algebraic metric constraint. The tested event is
D=−1e−6; the alternative stopping condition is r=0.01. Neither is an
actual de Sitter boundary condition. No mass/interior parameter or target
coefficient was fitted in this experiment.

The coarse scan has denominator events for factors 0,0.1,0.2,0.3,0.305,
and reaches r=0.01 without that event for 0.31,0.32,0.5. Twelve bisection
steps on the initial interval [0.305,0.31] produce the finite classification
bracket

    [0.30621826171875005, 0.306219482421875].

Both endpoint classifications agree at the original and tighter integration
tolerances. This bracket is for the stated finite event, not a certified
mathematical bifurcation or a value of beta. At the lower endpoint the event
occurs near r=0.00194294308 with R approximately −2.05e−7; at the upper
endpoint the integration reaches r=0.01 with D approximately −0.12047 and
R approximately 0.00268286. The latter branch has growing P near that
endpoint and has not matched the decaying outer modes.

## The near-transition trajectory is still not a regular crossing

For the same lower-endpoint factor, tighten only the denominator cutoff.
At D≈−1e−7 and −1e−8 the endpoint radii approach 0.001942943314,
but R remains about −2.067e−7 and −2.069e−7. Correspondingly P' changes
from approximately −2.067 to −20.688. The upper endpoint again reaches
r=0.01 without either event.

Thus the much smaller numerator near the shooting transition is useful
evidence for locating the bottleneck, but it is not zero. The necessary
regularity condition D=R=0 has not been met. Finite classification agreement
does not prove that a smooth separatrix exists between these trajectories,
that it crosses to the desired outer branch, or that it would select beta.

The v2 shooting contract records the original IVP file as an execution input,
because the script loads only its reviewed definitions and does not run or
modify its old evidence driver. Scripts, parameters, bounds, actual argv and
outputs are pinned in their bounded-run manifests. The earlier v1 runs are
preserved; v2 adds full-equation linearization checks and smaller-cutoff
rechecks rather than altering prior evidence.

## Next mathematical step

Solve the critical algebraic constraints C=D=R=0, determine the allowed
finite radial slopes, and connect their manifolds to both inner MOND data
and the selected outer mode boundary. The present event bisection supplies
initial estimates; using it as the final smooth-crossing solution would be
an error. A desingularized radial parameter or a boundary-value formulation
can test that connection without dividing by D at the critical point.

At fixed beta this first tests whether the initial trace and shift constants
can satisfy global matching. Only after these data are accounted for could
regularity conceivably constrain a coupling. Repeat with other source masses
and independently specified interiors before treating any discrete value as
universal. The vacuum offset, full equation completeness, causal/dynamical
health and observational dictionary remain outstanding. The exact target
Lambda=32πa0² is not derived by this checkpoint.
