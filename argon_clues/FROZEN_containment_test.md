# Frozen criteria (written before containment_test.py was run) -- exploratory, argon_clues, no CFG id taken
Question: is the fitted CFG745 k (median missing mass / f_hot, X-COP, 12 clusters, aperture 1000 kpc = 0.70-0.95 R500) equal to R0 x (fraction of the free pool inside the aperture), with that fraction computed from the cluster's own profile?
Inputs: CFG624 G2 per_cluster (M_hse, M_b, M_NCE, frac_R500) both footings; R0 in {4.80, 5.364}; f_hot,cl in {0.85, 0.95} (CFG745's declared bracket).
Quantities: eps_i = resid_i / (f_hot R0) (implied containment relative to R0 f M_b(<ap)).
T1 (necessary): median eps_i <= 1 for every (footing, R0, f) combination; any cluster with eps_i > 1 is listed (needs total hot gas > aperture gas, true physically; reported, not a failure).
T2 (structure): the free pool lives where the cluster's mass is; predicted aperture dependence: Spearman(eps_i, frac_R500) > 0 (larger aperture, more pool). Pass if rho > 0 with p < 0.1 either footing; a significantly negative rho contradicts a pool that grows with radius.
T3 (NFW containment, exploratory): eps_NFW,i = m(c x_ap)/m(c) with the cluster's NFW (Duffy c(M200) solved to reproduce M_hse(<1000 kpc), R200 = r200 of that NFW), compared to eps_i x (M_hot,tot/M_gas,ap). The ratio M_hot,tot/M_gas,ap is NOT in the data: T3 can only bound it. Reported as the value of that ratio that would be required; implausible if > 2.
Mutation: replace f_hot by f_hot=0.08 (groups) -> T1 must fail (eps>>1).
Declared: nothing here uses KiDS/eRASS1 lensing; 'x1.8' in the lensing is a different aperture and not tested.
