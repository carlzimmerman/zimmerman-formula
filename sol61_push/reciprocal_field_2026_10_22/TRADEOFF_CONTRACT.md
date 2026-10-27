# Radius/growth sensitivity, declared before this run

Do not let the predecessor's .001 instantaneous-growth tolerance be the sole numerical basis for the radius result. Using the same explicit EdS history, compute the maximum final amplitude at k=.1/Mpc for a passive positive-surplus radius of 10,100,500 kpc. The radius theorem needs ell>=R/pi; the zero-P-stiffness, quasistatic model at equality is the permissive diagnostic. Also invert final-amplitude retentions .99,.95,.90 into ell and radius. These thresholds are declared sensitivities, not observational constraints. They do not account for a compact mass lensing outside its surplus radius.

Repeat each value with RK45 versus DOP853 at tighter tolerance; absolute difference <1e-7. Check amplitude decreases with length and the inversion residual is <1e-8. No data fit, no covariant or radiation-era interpretation.
