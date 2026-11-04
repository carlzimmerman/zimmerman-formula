# Declared KT39 bounded power-curvature scan

Before controls or physical runs, declare z=x+s^p, P=xQ(z)/z,
x=g.g/a0², s=ell²H:H/a0², with the unchanged simple-nu primitive and Q0=0.
The bounded grid is p={1.25,1.5,1.75} and common physical
ell={1.5,2,2.5,3,3.5,4} kpc:18 choices, each on both original a0 footings.
Power is now a searched parameter, alongside ell, unlike KT38's fixed2.
This is a phenomenological choice within the general action framework,
not literally Milgrom equation16 or a claimed fundamental derivation.

Retain the original24objects, original41 Upsilon samples1..3, original
baryons/gas conventions and two-sigma dispersion cuts. Implement full
A=[R-1+xR']g and B=p ell²s^(p-1)xR'H, with all spherical derivatives.
Do not modify KT37/KT38 sources. Before the population scan, check the
complete tensor energy variation, radial limits, p1/p2 old-action controls,
Newton/ell0/jointzero controls, weak scaling, and uniform-field variation.

Use the same three radial settings n1000/domain1,n2000/domain1,
n2000/domain2, rmin=1e-6a,rmax=domain*(200a+40ell). Require dispersion
changes<.02km/s, direct/weak/energy virial relative agreement<1e-3 or
absolute<1e-7(km/s)^2, Newtonian virial error<1e-3, selected actual-energy
finite-difference agreement<1e-3 at log-step1e-4, original sample identity,
and plain isolated QUMOND19/24 on both footings. Record invalid variance and
local negative total force without converting them into passes or changing
the existing global virial-screen criterion.

Report which of the18choices preserve at least17/24 on both footings as
an auxiliary comparison requested by the coordinator, not a new original
observational cut. Report every grid choice, including failures. There is
no automatic extension or optimization beyond this declared grid.

No continuous-Upsilon/exponent/length exclusion, monotonicity assumption,
actual satellite EFE prediction, isolation upper bound, complete equilibrium
claim or dynamical-health theorem follows. Numerical coverage is finite.
Bound the population run at600s wall/550s CPU/1MiBlog/one numerical thread.
CPU affinity is unavailable here and not requested. Pin actual HEAD and
all declared code/data inputs in fresh manifests.
