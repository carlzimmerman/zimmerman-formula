# FGF029: one extended-support coefficient

Retain the reviewed fifteen annular rows and fifteen old pressure columns M
exactly as stored. The changed pressure basis adds a free p(5)=t and moves the
zero boundary to6. Its only new basis function is h(x)=x-4 on[4,5], 6-x on[5,6],
zero elsewhere. Old hats, including the node4 hat, are unchanged. This is an
added free coefficient, not an extrapolated or measured pressure profile.

Project only h through the inherited spherical LOS geometry and tangent-plane
FFT beam; average with the same fifteen normalized mask-weighted annuli.
Use the parent geometry and verify reconstructed radius, transfer and all
weight hashes; check the 512 source patch includes radius6. If it does not,
stop rather than silently increase source support/grid. Cache no new map fit.
Call the resulting fifteen-element column k. The extended response is [M k].

For exact rational interpretation of the stored binary64 response, solve
h_M=M^-1 k and w=L_old M^-1. Then

    p_old=M^-1 d-h_M t,
    g=w d+mu t,              mu=-L_old h_M,
    n=(-h_M,1),              [M k] n=0,   L_extended n=mu.

If mu!=0, target identification fails although M remains invertible. This
single scalar t is the missing functional in this coordinate choice; pressure
changes are distributed over old nodes too. A further row r=(r_old,r_t) would
identify the target iff r_t-r_old h_M!=0. If zero, it annihilates the surviving
null direction and supplies no target information. This is a criterion, not
an assertion that a suitable physical measurement exists or is calibrated.

The explicit synthetic baseline is p_i=1e-5 exp(-x_i) at all sixteen free nodes,
including x=5; p(6)=0. Stored binary64 values are treated as exact rationals.
Its synthetic data are exactly [M k] times that baseline. They are generally
different from the earlier support5 baseline data and are not actual map fits.
For n normalized by n_t=1, define epsilon as one quarter of the minimum
baseline pressure-gap divided by absolute corresponding null-direction gap.
Then baseline +/- epsilon n remain strictly positive and decreasing through
the final zero endpoint and have identical synthetic observations. Save all
exact pressure values, epsilon, null vector, synthetic data and target changes.

Controls: byte-preserving old matrix inclusion; exact M inverse products;
direct LOS quadrature of the new hat at representative radii; fixed geometry,
weights and transfer checks; exact null and target decomposition; nonzero target
response or exceptional exact cancellation; strict witness gaps and identical
data; deliberately damaged null and zero new coefficient recover old model.
The added observation-row criterion has positive r=e_t and negative existing-
row controls, labeled algebraic rather than physical observations.

This is one changed-support experiment. No extra annuli, further support sweep,
actual pressure fit, covariance or continuum theorem. Exact stored-coefficient
algebra does not authenticate the finite physical response approximation.
No force or mass is inferred. Future MOND bridges preserve both a0=9.3619e-11
and1.1279e-10 m/s^2, separate vacuum/H histories and Q/RAR/registered M, with
actual density and total/electron-pressure conversion. No theory closure or
historical novelty claim follows.

One deterministic bounded run:120s wall,110s CPU, cooperative one-thread
numerical libraries,1MiB logs, no claimed memory limit. Exact Fraction checks
have zero tolerance; LOS quadrature tolerance1e-9. Stop on an input/geometry
failure or exact algebra failure; retain diagnostics instead of altering inputs.
