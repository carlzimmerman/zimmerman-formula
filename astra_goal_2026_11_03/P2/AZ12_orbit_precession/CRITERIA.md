# AZ12 — actual secular precession of the squared-resolvent monopole

κ = ½ FITTED; not theory closed

Pre-result continuation requested by owner after phase one. Record: ls P2/AZ*, git log through 1fadaa469a, rg perihelion/orbit-average in earlier AZ criteria and prep_2026/planetary_doors/laneR_bounds_compute.py. AZ11 used point-radius acceleration bounds; this lane removes precisely that conversion approximation. No width, kernel-power or baryon scan.

Use the SAME filtered source and Newtonian-external-field conversion as AZ11. Compute its exact radial monopole A(r) by angular quadrature, then its first-order secular perihelion rate over an eccentric Kepler orbit. For inward A>0 and eccentric anomaly E:
<omega_dot>=sqrt(1-ecc²)/(n*a*ecc) * integral_0^2pi A(a(1-ecc*cos E))*(cos E-ecc) dE/(2pi).
Here n=sqrt(GMs/a³). This follows from Gauss' radial equation and dt=(1-ecc cos E)dE/n. It uses the complete radial profile rather than a constant or linear-force replacement.

Inputs: six a values and EPM/INPOP supplementary-precession 1-sigma errors (mas/year) in RQ3 tolerances.json PLANETS, as attributed in prep_2026/planetary_doors/BOUNDS.md. Eccentricities Mercury .206, Venus .007, Earth .017, Mars .093, Jupiter .048, Saturn .054 from the on-disk laneR table. Use RQ3 a=.387 for Mercury rather than laneR's apparent .397 transcription discrepancy. GMs=1.32712440018e20 SI, AU=149597870700, year=365.25 days. a0 footings 9.3603e-11 and 1.1312e-10; physical external g_e=2.32e-10, g_Ne=g_e²/(g_e+a0); xi=.5 sqrt(GMs/a0), kappa=.5 FITTED. These are framework/solar inputs, no cosmological background.

Grade each footing against the more generous published error max(EPM,INPOP): |rate|/sigma<=2 for all six. Print each ephemeris comparison separately and margin 2-Z. The absence of covariance and raw tracking residuals prevents a joint likelihood or full ephemeris exclusion. This tests the declared monopole; higher multipoles and parameter refits remain uncomputed, explicitly conditional. Do not claim a complete RQ3 C1 pass.

Known answers in dimensionless a=n=1 at each eccentricity: constant inward A=1 -> -sqrt(1-e²); harmonic inward A=r -> -1.5 sqrt(1-e²); inverse-square A=1/r² -> zero. Absolute error <=1e-10. Integrate at orbit/angular orders (128,80) and (256,160); changes in rate/sigma <=1e-5. Newtonian nu=1 null rate <=1e-12 mas/year. MUTATE omit the time weight by averaging uniformly in true anomaly for a constant force: it returns zero and must differ from the correct constant-force oracle by >0.5. Every footing has these controls. Output results.json predeclared. Failed control gives NO VERDICT. No new free physical parameter; no claim of a full action.
