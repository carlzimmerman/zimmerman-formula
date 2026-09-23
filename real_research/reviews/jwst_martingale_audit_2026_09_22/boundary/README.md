# Boundary correction and finite transport audit

The strongest new candidate 07c49b691d2249e09248fcfdb8cdfb99 computes the
minimum threshold 5/3 correctly in code but claims 5/6 in its hypothesis and
argument. Its two small-k tests do not check the boundary-minimum regime,
maximum, variance sign, or stopping. Its wrong-threshold negative fixture is
legitimate as a false claimed minimum; the local referee's objection to that
specific fixture is not persuasive. Reject the false claim without discarding
the correctly solved critical point or threshold. Other attempts confuse
the minimum and maximum thresholds and put +E[h] in the correction.

## Exact model calculation

Units R=c=1, uniform conservative Thomson rate k, central isotropic emission,
all photons counted. Let Z=X_T dot U_T in [0,1], D=T-Z, and
h(z)=z^2/3-2kz/5. The prior exact polynomial satisfies LP=-2m and boundary
P=z^2+h; the raw second moment w has Lw=-2m and boundary w=z^2.
Consequently P-w is harmonic and stopped Dynkin gives

    w(0,0)=P(0,0)-E[h(Z)],
    E[D^2+h(Z)]=7k^2/20+1/3,
    Var(D)=1/3+k^2/10+(2k/5)E[Z]-(1/3)E[Z^2].

Integrability is not inferred from the script: any surviving state has at
least exp(-2k) chance of collision-free exit in the next time 2. The resulting
geometric tail gives finite moments of T. Bounded polynomials and the finite
second moment justify stopped identities. The mean identity E[D]=k/2 is the
already known benchmark. The plus sign fails even in vacuum, where Z=1,D=0.

One can avoid assuming regularity of the unknown w entirely: define the explicit
space-time polynomial G(t,s,z)=P(s,z)+2t*m(s,z)+t^2. Since LP=-2m and Lm=-1,
(partial_t+L)G=(-2m)+2m+2t*(-1)+2t=0. At exit G(T)=D^2+h(Z).
Bounded-time Dynkin therefore gives E[G(t wedge T)]=P(0,0). The bound
|G(t wedge T)|<=C_k*(1+T^2), with finite E[T^2], permits dominated convergence.
This directly proves the stated raw-second-moment relation within the model.

Since h''=2/3>0 and h(z)-h(3k/5)=(z-3k/5)^2/3,

    h_min = -3k^2/25                 for 0<k<=5/3,
            1/3-2k/5                for k>=5/3;
    h_max = 1/3-2k/5                for 0<k<=5/6,
            0                       for k>=5/6.

For k>=5/3 the derivative is nonpositive throughout [0,1], giving the stated
endpoint minimum. A convex function's maximum is at an endpoint; comparing
h(0)=0 and h(1) yields the separate 5/6 threshold. Thus

    1/3+k^2/10-h_max <= Var(D) <= 1/3+k^2/10-h_min.

These are proved model bounds from the range of h, not asserted optimal bounds
over physically realizable escape distributions. At small k the upper bound
is loose. Dimensional delay variance multiplies the expressions by (R/c)^2,
with k the radial Thomson optical depth of this uniform sphere.

## What was actually checked

Exact symbolic checks and six rational fixtures test extrema, h+1, and a false
minimum raised by 1/10. The separate sign proof above supplies the universal
reduction; a finite list alone would not do so.

Four independently seeded samples of 120,000 photons each use the PREEXISTING
3D continuous-flight solver. The raw-second-identity residuals are -1.055,
0.796,-0.142,0.335 Monte Carlo SE at k=0.25,1,2,5. Reversing the correction
fails by at least 28 SE; omitting it fails by at least 14 SE. Mean delay and
outgoing geometry checks also pass. Observed variances are approximately
0.1176,0.5173,1.1525,4.1669, within the respective bounds. All declared checks
pass and the manifest validates. SE estimates are approximate, not rigorous
confidence bounds. No raw paths were selected or fitted to enforce the result.

This numerical audit reuses one existing solver. A second independently coded
transport implementation remains outstanding. Literature overlap is only
partially checked (SOURCES.md); no new fundamental law or observational
confirmation is asserted. The exact identity still contains exit-angle moments.
