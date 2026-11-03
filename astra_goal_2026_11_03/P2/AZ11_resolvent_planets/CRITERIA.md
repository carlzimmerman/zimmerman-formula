# AZ11 — squared-resolvent planetary monopole

κ = ½ FITTED; not theory closed

Pre-result. Record: ls AZ10 and M1, git log planets/resolvent, rg monopole/angular-average/radial-anomaly in KT filter records. AZ10 passes the reduced quadrupole gate; it has not faced the planetary radial anomaly. This is a necessary additional test, not a width scan.

Use AZ10's same xi=0.5 sqrt(GMs/a0), enclosed fraction gammainc(3,r/xi). Let h=GMs*f/r², e=g_e²/(g_e+a0), g_e=2.32e-10. For the filtered anomalous Poisson source div[(nu(|h rhat+e zhat|/a0)-1)(h rhat+e zhat)], Gauss' law gives the anomalous radial monopole
A(r)=1/2 integral_-1^1 [nu(sqrt(h²+e²+2he mu)/a0)-1](h+e mu) dmu.
This is exact for that specified source; it is not a complete derivation of the filter from gravity. Other multipoles and orbit geometry are not fitted. External-field conversion retains AZ10's spherical-MW conditional tag. Primary compare only the monopole to RQ3 C1's radial-anomaly line; a pass would not certify full ephemerides.

Inputs: RQ3 tolerances.json PLANETS and prep_2026/planetary_doors/BOUNDS.md (observational ephemeris-error summaries, no cosmological background used). GMs=1.32712440018e20 SI, AU=149597870700 m as RQ3; this GM is the measured ephemeris parameter instead of the mass-times-G approximation in AZ10. For each of six planets sigma=dg_tight*max(EPM,INPOP)/min(EPM,INPOP); PASS if all |A|/sigma<=2. Also report the old tighter 1-sigma ratios; no line moved. Output signed margin=2-|A|/sigma. Both footings independently. This is a conditional necessary-gate interpretation of published bounds, not a raw orbit refit.

Known answers: nu=1 gives zero to absolute 1e-25 SI; h/e->0 response A/h=nu(e/a0)-1+(e/a0)nu'(e/a0)/3, test at h/e=1e-4 to relative 1e-6. Angular Gauss orders 80/160 must change A/sigma by <=1e-5. The central field limit h/(GMs*r/(6xi³)) at r/xi=1e-6 must agree within 1e-5. MUTATE remove filtering (h=GMs/r²): the radial anomaly must violate at least one C1 bound by >10 in Z. No additional fit parameters, kappa remains 1/2 FITTED. Output results.json predeclared. Any control miss yields NO VERDICT. No full RQ3 scorecard or row-12 credit is claimed.
