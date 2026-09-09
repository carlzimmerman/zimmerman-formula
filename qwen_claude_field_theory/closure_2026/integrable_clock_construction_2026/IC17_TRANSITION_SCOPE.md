# IC17 transition scope: a valid fixed-background obstruction, not a global no-go

Full theory: **OPEN**. This audit concerns Fable commit `0f56817c6`,
`fable_independent_2026/L35_TRANSITION_GHOST.md` lines 89–130 and its independent
symbolic source `L35_transition_ghost.py` lines 402–424 and 626–649.
It does not change Fable files or construct an IC17 transition solution.

## What survives independent checking

At fixed auxiliary coordinates, set

    h = −E rho²/3 + eta(−E rho/3)(−E G rho²/3 − B) + V(q),
    A = 1 + eta G,  r = −E rho/3,
    b = E G r²/12 + B E²/36.

Direct symbolic differentiation gives exactly

    aUV = E A/6 + h_rhorho/4
        = −(E G r/3) eta′ − b eta″
        = −(1/b) d(b² eta′)/dr.

The divided expression is used where b≠0; its expanded form extends through
zeros. With fixed E>0, G≠0 and finite B, the weighted-integral proof on each
sign interval of b is valid. On a complete nonconstant C² switch interval with
eta′ zero at both ends, aUV must be negative somewhere (hence on an open set).
For positive r the quadratic has at most one interior zero; other intervals
can simply be split at every zero. No numerical grid is needed for this fact.

The same fixed-q statement applies to the *single rising interval* of IC16/17's
one-sided activation where the assumed Hessian reduction is valid. Removing
the falling branch defeats the simpler two-branch inflection argument, not
this fixed-q weighted-integral theorem. A pole pressure finite at a chosen
interior q changes B but does not invalidate this identity.

## What fails: the stated variable-coefficient extension

L35 lines 117–120 assert that allowing E,G,B to vary along r requires only
that b not vanish on an open subinterval. That hypothesis is insufficient.
Here is an exact counterexample to that ODE assertion, **not** to the fixed-q
theorem and **not** an actual solution of any IC auxiliary constraints.

For 1≤r≤2, t=r−1, choose

    eta = 10t³ − 15t⁴ + 6t⁵,
    E = exp(r+2),  G = −3/(E r),
    B = (9r − (36/100) eta″)/E².

The plateau extension is C², exactly the stated theorem's regularity, but
not C-infinity. Then alpha=EGr/3=−1, b=−eta″/100, and

    aUV = eta′ + (eta″)²/100 > 0 throughout 1<r<2,
    eta′ = 30(r−1)²(r−2)² > 0.

Both first and second derivatives vanish at the endpoints; b has only the
three isolated zeros 1, 3/2, 2. Its pressure coefficient is positive throughout:
the exact extremum calculation gives |eta″|≤10/sqrt(3), so
9r−.36 eta″ ≥ 9−3.6/sqrt(3)>0.

The integrating factor chi=exp(integral alpha/b) diverges like
|r−3/2|^(−10/3). Thus chi eta′ does **not** vanish at this interior boundary.
Multiplying the ODE by mu=chi/b and discarding that boundary flux is invalid.
A sufficient replacement would be regular nonzero b over the closed interval,
or justified finite/vanishing flux conditions at every zero. Those conditions
must be established, not assumed, on a proposed physical trajectory.

The kinematic field chart can be reconstructed as
w=log(1+G)/2−1/12, xi=log(E)+3w, u=1+w/xi, S=xi−w.
The code checks E>0, −1<G<0, B>0, xi>0, 0<u<1, and S′>0 at 101 rational
points with 40-digit evaluation. These are explicitly bounded chart checks;
they do not impose h_q=0, matter constraints, or the IC17 pole-pressure form.

## Additional work required for a physical ghost claim

A negative off-constraint fixed-q point is not by itself a physical state.
One must establish an allowed background solving the actual auxiliary and
gravitational constraints, eliminate the *same action's* spatial auxiliary
block, and verify that aUV is the surviving physical kinetic coefficient.
IC12's spatial repair must not be silently imported into IC17's original IC11
spatial block; its rank and the high-wave-number Schur limit need checking.
Even a genuine negative-energy kinetic mode does not alone imply classical
growth at rate c k: the gradient terms and mixing determine the dispersion.

L35's turnaround-shell assignment additionally imports an approximate LCDM
infall profile. It is not a sourced solution of this action. In the switch
region, momentum-dependent activation changes the momentum–extrinsic-curvature
map; identifying r with an observed local expansion rate requires derivation.
There is no demonstrated mandatory ghost shell around every bound object.

None of these criticisms establishes a healthy full transition. Conversely,
the transition identity does not refute IC17's separate eta=1 pressure-pole
plateau, whose auxiliary reduction is different and must be audited directly.
The next construction still needs a same-action transition/constraint analysis,
not an inferred no-go or an inferred cure from separate reductions.

## Reproduction and interpretation

From this directory run:

    python3 -m unittest test_ic17_transition_scope.py -v
    python3 ic17_transition_scope.py
    python3 ic17_transition_scope.py --require-full-closure

The last command exits 2 after successful audit checks, because full IC closure
is not established; failed checks exit 1. Identities and polynomial sign
factorizations are exact SymPy computations. Chart samples are finite numerical
evidence only. Tests were first run before implementation and failed because
the audit module was absent, then rerun against the implementation.
