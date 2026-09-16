# KEPLER_GRADE_CLUSTER_PREDICTIONS — quantifiable, falsifiable, measurement-ready (2026-09-15)

Derived entirely from the committed chain (the law G03E/G03G, the triad, the
universal surface density, the two-regime map; cluster data: X-COP ingests
G050/G057b, the temperature ratio G075, the partition G059).  Every number
below is a prediction with its measurement recipe and its falsifier.  The
standing honest context: the amplitude normalization (the free-dust
fraction) is NOT derived; the predictions here are the parts of the cluster
signal the framework fixes WITHOUT that freedom.

Constants: a0 = 9.3619e-11 (canonical), G, M_sun.  The floor:
sigma_floor(M_b) = (G M_b a0)^(1/4)/sqrt(2);  T_floor = mu m_p sigma_floor^2/(2 k_B),
mu = 0.6.  Per cluster: r_M = sqrt(G M_b/a0).

## P1 — THE TEMPERATURE-RATIO UNIVERSALITY (the 0.28-exact law)
T_obs/T_floor = (sigma_dyn/sigma_floor)^2 = 0.28 = 0.53^2 EXACTLY (G075,
scatter 0.05 dex over 12 clusters).  PREDICTION: the ratio obeys a closed
form in (M_dyn/M_b) with a UNIVERSAL exponent (G095 derives it; predicted
alpha-family: 1/2 BTFR-style, or 1 virial-style) and the SCATTER stays
< 0.1 dex when M_b is remeasured consistently.
MEASURE: per cluster, the HSE-inferred sigma_dyn at the temperature-
averaging radius vs sigma_floor from a photometric M_b (stellar + gas).
FALSIFIER: a cluster where the ratio departs the closed form by > 3 sigma.

## P2 — THE OUTER-PROFILE DECOMPOSITION (the law's phantom vs the dust)
For r > r_M (the deep window, g_N < a0 at cluster scale), the law fixes the
phantom component: rho_ph(r) = A/r^2, A = sqrt(G M_b a0)/(4 pi G), with the
free dust as the remaining mass.  PREDICTION per cluster: the residual after
subtracting A/r^2 follows the free-dust envelope with the slope
d ln rho_dust/d ln r in (-2.5, -2.0) (the NFW-class envelope), and the
CROSSOVER radius where the phantom = the dust sits at
r_x ~ (A/rho_dust_scale)^(1/2): the X-ray/WL-measurable.
MEASURE: deprojected density profiles (XMM+WL joint) out to R500, the G094-
audited ingests.
FALSIFIER: outer slope < -2.5 (steeper than NFW) or the phantom exceeding
the observed residual anywhere outside r_M.

## P3 — THE SHARE FUNCTION (the V4 rising-share, functionalized)
The phantom share s(r) = rho_ph(r)/(rho_ph(r) + rho_dust(r)) rises through
the a0 crossover with the KERNEL-slope: d s/d log(g_tot/a0) per cluster
predicted from the mu2-kernel form (share = 1 - mu2(g/2a0)-class).
PREDICTION: the 12-cluster median slope in (0.5, 1.0) per dex and the
Spearman rho > 0.7 (G050's V4, audited by G094).
MEASURE: per-cluster per-bin (g_tot, rho_tot) from the committed ingests;
the slope from the bisector fit.
FALSIFIER: flat share (no rise) at the crossover on > 1/3 of the clusters.

## P4 — THE GAS-FRACTION PROFILE (the baryon/dark split's shape)
The framework's split: f_gas(r) = M_gas(<r)/(M_b + M_ph + M_dust)(<r): the
PREDICTION is the gas fraction RISES with radius (baryons concentrated) and
its radial RUN is set by the phantom's r^-2 plus the dust envelope:
d ln f_gas/d ln r in (+0.3, +0.7) over (0.2, 1.0) R500-class; the absolute
value carries the free-dust normalization (open, stated).
MEASURE: X-ray gas masses vs the total from hydrostatics per bin (X-COP
already carries both).
FALSIFIER: a falling f_gas(r), or a jump > 0.15 at any single bin.

## P5 — "ARE THEY CLUSTERS AT ALL?" — THE COHERENCY DIAGNOSTIC
The framework's own test of whether the 12 X-COP systems are SINGLE
equilibrium structures or line-of-sight superpositions: the theory says
T(r)/T_floor(r) is a FUNCTION ONLY of M_dyn(<r)/M_b: the RATIO-PROFILES
per cluster must be self-similar (collapse onto one curve) if the systems
are coherent; a superposition scrambles the ratio-profile.
PREDICTION: the 12 ratio-profiles collapse (spread < 0.15 dex in the
ratio at fixed M_dyn/M_b).
MEASURE: the committed X-COP T(r) and M_dyn(<r) profiles, ratio vs the
argument, pooled scatter (G105 runs it).
FALSIFIER: scatter > 0.3 dex -> the sample is (partly) non-clusters, and
the clean subset carries the real signal.

## P6 — THE CROSS-INSTRUMENT EQUIPARTITION (gas vs galaxies)
The same dark sector sets both tracers' dispersions: the gas temperature-
weighted sigma_gas^2 and the galaxy velocity dispersion sigma_gal^2 both
equal virial forms of M_dyn(<r): sigma_gal^2/sigma_gas^2 = (the observed
anisotropy-corrected factor ~ 1.0-1.6): PREDICTION: the ratio is
mass-independent within the sample (spread < 0.2 dex).
MEASURE: published caustic/velocity-dispersion profiles vs the X-COP T(r).
FALSIFIER: a mass-trending ratio across the 12 clusters.

## THE TWO-REGIME MAP AT CLUSTER SCALE (the physics the predictions test)
For a cluster, r_M = 273 kpc (M_b = 5e13): inside r_M the field is strong
(Newtonian baryons + free dust; the law is OFF), outside r_M the field
crosses a0 (the law's deep regime) UNLESS the EFE (the surrounding LSS
field ~ g_ext) caps the phantom: the map is INVERTED relative to galaxies --
the phantom zone is the OUTER halo, and its inner boundary (the a0
crossing) is the observable transition at r_M = 273 kpc-class.  P2-P4 are
the direct tests of this inverted map.

## The open numbers (NOT predicted, by honesty): the free-dust fraction
per cluster (G098 measures its exact structure); the absolute amplitude of
the dust envelope; the EFE cap's precise line at cluster scale.

## The breakthrough question (the program's): the temperature ratio's
closed form (G095) IS the cluster amplitude problem in one number: if
T_obs/T_floor = (M_dyn/M_b)^alpha exactly with a clean alpha, the cluster
"missing mass" is the mass ratio the temperature itself measures -- the
cluster T IS the dark-to-baryon ratio, and the framework's floor is the
baryon thermometer.  The Kepler-grade statement: measure alpha to 0.02;
the theory predicts its value (G095) or it is a new empirical law the
framework must explain.