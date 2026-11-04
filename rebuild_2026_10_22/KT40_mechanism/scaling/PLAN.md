# KT40 scaling mechanism: fixed-law explanatory computation

Base checkpoint: KT39 p=9/8, ell=3 kpc, original baryons/a0/cuts and accepted
raw analytic, Solar and dwarf files. Git starting revision:
e7f1ac9ca025031f5ec15679645913b10f66f4ad.

This task derives the dimensionless curvature ratio, point-mass and
external-field crossover lengths, and exact Plummer compactness/size scaling.
It separates radial A and B contributions to the already computed dwarf
virial and derives the large-ell/rM Solar quadrupole coefficient. It does not
retune any parameter or claim a new empirical pass. The script checks exact
algebraic identities, Q primitive differentiation, large-lambda asymptotics
against accepted Solar data, and dwarf reconstruction against accepted
p9/8 outputs. Work scope is scaling/ only; historical sources remain frozen.

Finite arithmetic controls and numerical tables do not prove a global law
for arbitrary density profiles. chi=s^p/x is an action-input discriminator,
not by itself an observable force ratio; the full Hessian stress is retained.
Solar asymptotics hold at fixed positive external eta and p, and cannot be
read as a uniform mass-decoupling theorem. Upsilon1,2,3 sample points are
explanatory representatives of the original41-point screen, not an extension.
