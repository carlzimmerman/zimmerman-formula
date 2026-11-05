# HC011 force-law comparison, frozen before fit

Use NGC7331 outer 17 SPARC radii r>=rmax/2. Keep distance14.7Mpc and inclination as published. Test velocity residuals with original errV, not squared-velocity linearization. Signed gas term retained. Nine fixed stellar M/L choices ud=.3,.5,.7, ub=.5,.7,.9; also an explicitly exploratory nuisance fit ud in [.1,1.2], ub in [.1,1.4].

Three empirical additions: Vmodel²=Vbar²+B(r/r0)^s, r0=25kpc, B>=0. Central s=-1; extended inverse-radius force s=0; free s in [-3,3]. Optimize full17 and two complementary alternating-radius train/test splits. These are interpolation diagnostics with shared systematics, not independent galaxy validation. Compare held-out km/s RMSE and original-error normalized RMSE. Profile intervals only if explicitly labeled conditional; no population p-values.

Also test a specified BH-only nonlinear scalar: delta g=sqrt(G Q aLambda)/r, Q set to primary N7331 33-degree upper limit rescaled to14.7Mpc. aLambda=c²sqrt(Lambda/(32pi)), Lambda1.09e-52m^-2 fixed, not fitted. Include Newtonian BH term for this model. This is a generous fixed-charge diagnostic, not a complete conservative relativistic theory. Assess needed free inverse-radius amplitude relative to this coefficient.

Exact checks: Schwarzschild-de Sitter horizon area bounds; surface-gravity target; scalar particle charge/source reciprocity; inverse-square and Yukawa effective enclosed mass behavior; additive vacuum-term ambiguity. These are scoped derivations, several established in prior project work, not novel discoveries. Original question remains open absent a fully specified successful alternative.
