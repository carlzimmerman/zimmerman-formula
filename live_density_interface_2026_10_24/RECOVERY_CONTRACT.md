# LD-10: density and boundary displaced together

Refine LD-8 tau.1 outer-wall candidate from128 to256 quadratic cells,
domain4,K3,beta1000,k120. Transfer species conservatively and record any
feasibility dilation. Then move the material cell edges near the wall by
delta*(r/Rwall)*exp(-((r-Rwall)/(.25Rwall))²), preserving species masses
during remapping; reconstruct phase. Both density and conversion relax again.
For each sign choose the largest admissible displacement in 1,.5,.2,.1,.05
kpc with monotone edges and saturation slack>1e-4. This avoids inserting an
unphysical over-saturated state by shifting phase alone through fixed mass.
Compare final boundary, energy, law and both stationarity residuals with the
refined reference. A smaller energy at another radius falsifies restoration
to that reference. A positive local Hessian is not substituted for this test.
240s experiment cap; incomplete recovery is explicitly resource-inconclusive.
