# NA1 amendment A1 (after the first run; committed before the rerun)

Kappa = 1/2 FITTED; not theory closed. Adopts nothing.

**What happened.** The first full run (log kept as `run_main_KAstop.txt`) failed KA7: the solver's w_tot at z 1e5 is
0.3225 against the frozen known answer 1/3 +- 0.01. The frozen known answer was mis-stated, not the code: at z 1e5 the
matter density is still about 3 % of the radiation density (1 + z_eq ~ 3.4e3), so the two-fluid value is
(1/3) / (1 + (1 + z_eq)/(1 + z)) = 0.322, not 1/3. The I7 rows do not use KA7's z 1e5 or z 50 values; D1 reads the solver
at z 3400 only, and D0 / D1-frozen / D2 / D3 / D4 fail without it.

**Disclosed.** That run did not stop at the KA (the I7 KA is evaluated at the end of the script), so it printed every
label before the KA7 failure was read: I5 DEAD BY REDUCTION / DEAD BY REDUCTION, I7 DEAD / DEAD. Those labels are
therefore seen before this amendment. Nothing graded changes in this amendment.

**A1-1 (KA7 restated).** KA7 compares the solver's w_tot (finite difference of H(z)) with the two-fluid analytic value
w_2f(z) = (1/3) / (1 + (1 + z_eq)/(1 + z)), 1 + z_eq = (ob + od) / (Omega_r h^2), Omega_r h^2 = 2.4728e-5 (T0 2.7255 K)
x (1 + 0.22711 x 3.046) (standard photons + three neutrino species, PROVISIONAL constants), at z = 1e5, 3400 and 50.
PASS if |w_tot - w_2f| <= 0.003 at all three.

**A1-2 (memory, no graded change).** Peak RSS was 1.025 GB (ru_maxrss; footprint 0.56 GB), over the 1 GB line. The web
loop is restructured to the same arithmetic with fewer live arrays: the Newtonian divergence is computed once per z, the
phantom divergence is accumulated per variant (fftn(g + F W) = fftn(g) + fftn(F W) by linearity), velocity components
are kept only for the z 0.25 flow sample. KA1 (r = SV5 json to 1e-6 rel) must still hold.

Kappa = 1/2 FITTED; not theory closed.
