# Correction after the first density-coupling run

The Cartesian variation passed the contracted flat, rigid-rotation and zero-vorticity checks. Two additional guessed general-slope identities failed: the general correction contains (1-p^2)(n-2p), not n(1-p^2). Consequently a uniform-density flow does not have zero correction for every p; it does for p=0 and p=+/-1.

Independent cylindrical derivation: set Q=-(g^2 omega)'/(rho chi), omega=(p+1)v/r, and chemical correction Z=g' X omega=g^2 omega^2/(2rho chi). Then g_grav=v^2/r+Q(v/r-v')+Z'. With g=g0 sqrt(rho) and rho proportional to r^-n, the two contributions combine into (1-p^2)(n-2p)g0^2 v^2/(chi r^3). This agrees with the Cartesian result. The expected formula is corrected, not its tolerance. The originally contracted flat-curve result is unchanged. Original density_run is retained, and final evidence is density_run2. The control still removes the required Z' and must fail.
