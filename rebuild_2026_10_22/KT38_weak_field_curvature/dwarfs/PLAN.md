# KT38 isolated Plummer discriminator, declared before the physical run

The new functional choice is z=x+s^2, with x=g.g/a0^2 and
s=ell^2 H:H/a0^2, P=xQ(z)/z, Q(0)=0 and unchanged simple nu. The fixed
exponent two is a structural choice; ell is the single continuous parameter.
Use the five predeclared common physical lengths .3,1,3,5,10 kpc, both
original a0 footings, the original 24-object sample, original baryon and gas
conventions, and all 41 original Upsilon values from 1 to 3. Keep the
two-sigma dispersion cuts fixed.

Retain the complete spherical Hessian contribution:

    g_ph=Cg-(Dg')'-2D(g'-g/r)/r,
    C=R-1+xR', D=2ell^2 s xR'.

The independent virial forms and controls are those derived from the full
action in KT37, now evaluated with the KT38 A/B tensors. In particular the
finite-difference energy uses g^2[R(x+s^2)-1], not the old energy. The direct
force integral, its integration-by-parts form, and fixed-radius homology
variation must agree within1e-3 relative or1e-7(km/s)^2 absolute. Selected
finite differences of the actual energy use log-step1e-4.

Use rmin=1e-6a and rmax=domain*(200a+40ell), on n=1000/domain1,
n=2000/domain1, and n=2000/domain2. Require all dispersions to change by
less than .02km/s; Newtonian Plummer virial error below1e-3; finite
predictions; unchanged plain isolated control19/24 on both footings; exact
sample equality to the prior original sample.

Every Upsilon is explicitly evaluated. No Upsilon monotonicity, continuous
range exclusion, actual satellite EFE prediction, or isolation upper bound
is assumed. Negative variances are recorded as failures, not clipped into
physical passing predictions. This is a finite discriminator of the stated
functional choice; it cannot reject all curvature or generalized actions.

One numerical thread, wall600s/CPU550s,1MiBlog cap; no randomness. A CPU
affinity restriction is unavailable on this platform and is not requested.
All outputs go to new run directories. KT37 source and outputs remain
read-only inputs; the actual current HEAD and complete declared input hashes
are recorded by the bounded runner.
