# Conserved fluid source and a regular-center obstruction

Verdict: proved under the stated regular stationary center and matter
conditions. The original expansion action cannot support a center with
rho_c+3p_c>=2U on its finite nonzero-Theta branch. This is a scoped
obstruction, not an observational exclusion of every parameter choice or
every modified gravity theory. Self-review; base
9ea1d20e76382aa367b33456cb0d544345f3868c. Fifteen exact symbolic identities
pass. The 32π goal remains open.

## A covariant source, with all stresses included

Introduce a separate matter velocity potential chi and
X_m=−g^{mu nu}partial_mu chi partial_nu chi/2. Its action is
integral sqrt(−g) p_m(X_m), with pressure p_m and density
rho_m=2X_m p_{m,X}−p_m. This describes an irrotational barotropic fluid
where X_m>0 and the equation of state is physically appropriate. It is
not the preferred foliation field T from the gravity action.

For a stationary spherical fluid take chi=omega t+psi(r) and
F=N²−exp(2sigma)V²>0. The vanishing radial-current branch gives

    psi'=−omega exp(2sigma)V/F,
    X_m=omega²/(2F).

The four-velocity is parallel to the timelike stationary Killing vector.
Time independence and zero radial current solve the matter phase equation
on this fluid patch. Its hydrostatic equation is

    p_m'=−(rho_m+p_m) F'/(2F).

This follows directly by differentiating X_m and p_m. Eliminating psi'
in the zero-current sector uses the envelope condition: its variation
vanishes there. The reduced source action is r²N exp(sigma)p_m(X_m).
Its contributions to the metric Euler equations are

    E_N/(r²exp(sigma))=p_m−(rho_m+p_m)N²/F,
    E_V/(r²N exp(sigma))=(rho_m+p_m)exp(2sigma)V/F,
    (E_sigma−V E_V)/(r²N exp(sigma))=p_m.

Thus this is a pressure and momentum source, not merely a density inserted
into the lapse equation. A free boundary and a global vacuum extension of
the matter field are not constructed here. These open-patch conservation
equations are enough for the necessary central limits below.

## Regular central limits

For a controlled comparison replace the quadratic polarization term by
−xi M²P²; the original theory has xi=1. The cubic term and its beta are
unchanged. Assume a regular finite-curvature spherical center with

    N=N_c[1+n1 r²/2+o(r²)], sigma=s2 r²+o(r²),
    V=−N_c h_c r+O(r³), P=p1 r+o(r),
    Theta→3h_c, N_c>0, h_c>0,

and finite density rho_c and isotropic pressure p_c. The positive h_c
condition keeps the center inside the chosen finite positive-Theta branch.
These leading limits are regularity assumptions, not an assumed global
source solution. In particular, higher noninteger corrections to P are
not silently prohibited by an analyticity requirement.

Put S=3lambda−1>0. Taking the radial metric, lapse and polarization limits
independently yields

    3S h_c²/2+2s2−2n1−U/M²+p_c/M²=0,
    3S h_c²/2+6s2−6p1−U/M²−rho_c/M²=0,
    n1=xi p1.

The cubic terms vanish in these limits because P=O(r) and Theta has a
finite nonzero limit. Subtraction gives

    s2=(3−xi)p1/2+(rho_c+p_c)/(4M²).

Substituting in either metric limit gives the same central relation

    U=3M²S h_c²/2+3M²(1−xi)p1+(rho_c+3p_c)/2.

The script checks both independent substitutions, not just one rearranged
equation.

## Consequence for the original xi=1 action

At the critical quadratic tuning xi=1, the central acceleration coefficient
p1 drops out:

    rho_c+3p_c=2U−3M²S h_c²<2U.

No beta occurs. Imposing beta²=128π/3 cannot remedy this source obstruction.
Using the model's vacuum relation U=3M²S H²/2 gives

    h_c²=H²−(rho_c+3p_c)/(3M²S).

For the earlier illustrative parameters H=M²=1, lambda=2, U=7.5,
the allowed active central density is below 15. A proposed center with
rho_c=100 and p_c=1 would require h_c²=−88/15, so no real regular
stationary center of this branch can have those data.

This does not identify U automatically with the Einstein-inferred observed
dark-energy density. Lambda=3H² while U depends also on lambda and M²;
their observational/local coupling calibration is unfinished. Large lambda
or a larger U could change the density ceiling and would require separate
cosmological and local tests. No present-day likelihood or measured source
profile was used in this obstruction.

The result also does not exclude nonspherical or time-dependent sources,
exotic stresses, a different action, or a nonregular preferred foliation.
Taking h_c=0 leaves the action's Theta pole and is not a demonstrated
regular escape. An exact deep-MOND central force can scale as sqrt(r) for
a finite-density sphere; such behavior violates the regular center limits
used here and needs a finite-curvature/ultraviolet analysis before it can be
accepted as a physical source solution. None is supplied by a vacuum
critical-point continuation.

## A quadratic detuning changes the problem, with a clear cost

For xi>1 the necessary relation allows a positive finite p1 to balance
larger active density. For example, if h_c=H and the same vacuum relation
holds,

    p1=(rho_c+3p_c)/[6M²(xi−1)].

This removes the algebraic cancellation, but does not prove a full fluid
interior exists or is healthy. Eliminating P in the small-field quadratic
sector gives M²a²/xi, making the special xi=1 cancellation explicit.

In the same conditional weak spherical reduction used earlier, the detuned
action becomes

    Lweak=−M²g²+2M²Pg−xi M²P²−C P³,
    g=xi P+P²/a0bare, b=g−P=(xi−1)P+P²/a0bare,
    a0bare=2M²/(3C).

For any fixed xi>1, as P→0,

    g/b→xi/(xi−1).

The strict infrared limit is Newtonian, so the original exact square-root
force law does not persist to arbitrarily weak fields. A finite MOND-like
window is still possible when (xi−1)a0bare<<P<<xi a0bare; within this
reduced approximation g² approximately equals xi² a0bare b. Its existence
and observed scale require a coupled solution and Newton calibration. A
small detuning is therefore a possible regularization to investigate, not
a coefficient prediction or an observationally verified repair. It adds a
parameter that itself needs physical determination.

## Research decision and evidence

Do not spend further effort presenting the vacuum critical branches as
physical source solutions before this central condition is addressed.
The original xi=1 action is obstructed for regular stationary centers
whose active density exceeds the fixed 2U ceiling. That scope is now
closed by an exact local argument; general vacuum matching is not refuted.

Next plausible routes are a physically derived departure from the critical
quadratic tuning, additional degrees of freedom that change the central
constraint, or a justified nonregular/time-dependent source analysis. Each
must preserve a demonstrable galaxy regime and independently determine
the coefficient and vacuum scale. Merely choosing xi,beta,U to make 32π
would remain a fit.

expansion_bridge_source_center.py checks five source-envelope identities,
three central Euler limits, four central-relation identities and three
detuned reduced-action identities. The bounded-run contract and validated
manifest record the script, exact arithmetic, domain and result. No fluid
BVP, new observations, critical crossing theorem or full dynamical/causal
health test was performed in this checkpoint.
