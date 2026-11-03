# AZ1 — Newtonian tidal reconstruction

κ = ½ FITTED; not theory closed

Pre-result freeze. Record check: ls of KT25–KT28 and existing AZ paths (none); git log through 1023fbaae9; rg for Newtonian tidal, tidal invariant, tau^4 and tidal mass estimator in rebuild and campaign. Nearest routes KT26/27 use the MOND acceleration and KT28 its tidal norm; CFG771 uses a Newtonian saddle but no mass estimator. No claim of exhaustive novelty.

Let T_N be the Hessian of the baryonic Newtonian potential, t=||T_N||_F, d=|grad t|. A point mass has t=sqrt(6) GM/r^3 and d=3t/r. Thus define GM_hat=(27/sqrt(6))*t^4/d^3 and xi=kappa sqrt(GM_hat/a0). The normalization is fixed by this identity, not an empirical fit. The formula is invariant under an added uniform Newtonian field. A nonzero host tide still enters; removing it by an object label is forbidden. At d=0 the rule is undefined: report this, do not clip silently.

First discriminator: an isolated point source has xi=r_M/2 at every radius, so this rule must face KT25's narrow alt Cassini failure. Use the existing KT16/KT28 quadrature model (external field enters nu but has zero Newtonian tide). This is an approximation to Cassini, not a new full field solution. If this necessary gate fails, stop expensive MW/dwarf/SPARC evaluation and mark those NOT EVALUABLE in this lane. Do not use the coarse result as a no-go for all tidal rules.

Inputs: a0 canonical 9.3603e-11 and alt 1.1312e-10 m/s^2; GMs=6.6743e-11*1.98892e30 SI; g_ext=2.32e-10 SI. nu(y)=1/2+sqrt(1/4+1/y). Report Q2 and ceiling ratio separately per footing. Gate: Q2 <= 5.2e-27 s^-2, the record's measured 1.6+2*1.8 in units 1e-27. Margin=1-Q2/ceiling. No new fitted physical number beyond kappa; external field and solar mass are inherited inputs.

Known answers: reconstruct GM and xi at synthetic GM=1,8 and r=0.25,1,4 to relative 1e-12; nu=1 gives zero quadrupole to absolute 1e-14 in dimensionless q. Independently require constant-width quadrature ceiling ratios within 0.005 absolute of KT25's 0.4806/1.057. Use (nr,nmu)=(4000,80), (8000,160), logarithmic r/r_M from 1e-7 to 1e5. Convergence tolerance 0.002 absolute in ceiling ratio; these are numerical tolerances, not measurement errors. If controls fail: NO VERDICT.

MUTATE: double the mass-estimator coefficient without changing the known-answer oracle. Its reconstructed mass must miss the 1e-12 line and be rejected. Separately run nu=1 quadrupole null. Every verdict goes in JSON. No fitted scan. All other twelve/RQ3 rows ungraded; no credit inherited from KT25.
