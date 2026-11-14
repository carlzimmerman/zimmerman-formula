# Independent raw-code audit: nonnegative-host AQUAL profiles

**Verdict: limited implementation pass for the declared convex linear subproblem and stored conditional-MAP arithmetic.** No fullfit replication, globalmassoptimization certificate, observationallikelihood calibration or physicaltheory conclusion is established. Audited positive_profiles.py, operator_controls.py, run_host.py, contract_positive_01.json, positive_01/result.json, arbitrary_field_adapter.py and upstreamhost/inversion code read-only. Fullreviewhashes are inreview_provenance.json.

## Reconstructed optimization and independent check

Let D be hostbasis+lenslight+independentquasarA/B+sky design, W=D/RMS, y=data/RMS. At fixed nonlinearfield and fixedlnlambda, objective is half[||y−W(s,u)||²+lambda*sᵀR*s+uᵀNu*u], constraineds≥0; FOUR nuisancecoefficientsu remain unconstrained. This is sourcepositivity only, not a general fullynonnegativephotometricfit. Actual reportedlens/quasarcoefficients are positive in all sixfinalcases.

Partition H0=WᵀW into source/nuisanceblocks A,B,C0, with b=Wᵀy; C=C0+Nu. Profiling u=C^-1(bu−Bᵀs) yields sourceHessian S=A−BC^-1Bᵀ+lambdaR and rhs a=bs−BC^-1bu. ProductionPositiveState implements exactly this elimination. It correctly reconstructs nuisancecoefficients and evaluates the FULL originalobjective afterward, so the model-dependent eliminatedconstant is not accidentally dropped in masscomparisons.

With d=sqrt(diagS), z=d*s, K=d^-1 S d^-1, rhs=d^-1a, positive diagonal scaling preservesnonnegativity. If K=LLᵀ, NNLSmin||Lᵀz−L^-1rhs||² has gradient2(Kz−rhs), exactly the desiredQP. The Choleskytranspose/target solve are correct. R=LedgeᵀLedge+.01I and propernuisancepriors make the fullquadraticSPD, so feasibility+KKT identify its uniqueminimum to measuredfloattolerances.

Production checks source≥0, scaledprojectedgradient<1e−6 and nuisancegradient<1e−5; complementarity is additionally recorded. Activegradient uses min(g,0), the correct lower-bound sign. NumericalKKT is not interval/exactarithmetic certification and activeboundthresholds/scaling should remain explicit.

Independentboundedrun_01 comparedproductionPositiveState against a FULL augmentedleast-squares BVLS solution, withoutSchurelimination, on two deterministic17×8designs (one nuisancecolumn scaled1000)×three lnprecisions0/2/4. Nontrivialactivesourceboundaries and negativenuisancecoefficients were present. Maximumcoefficientdifference3.11e−15; objective difference≤1.78e−15. The test uses4source+4nuisanceparameters, not thefullactual445parameterproblem. Actualresultarithmetic and positiveamplitudes were also checked, no image/PDEfits rerun. v2manifestcompletedvalidated.

## Actual fixed-lnprecision2 comparison

At commonlnlambda2, same21²h.06sourcegraphprior, sameVISdata/PSF/mask/RMS, SS6rays, samefreequasarflux/skypriors:

| Lightfixture | AQUALlogM | AQUAL−SIE rawchi² | AQUAL−SIE penalizedMAPobjective |
|---|---:|---:|---:|
| run04 | 11.36622769 | +622.00650 | +317.90517 |
| run03 | 11.33132443 | +471.25052 | +242.69244 |

Every objective equals½(chi²+prior_penalty); deltaobjectives equal differences ofthosevalues. Gaussian`score` is explicitly removed frompositive-source output, and authornonclaims correctly rejectevidence/Bayesfactor/p-value/posterior interpretation. These comparisons are **penalizedpoint estimates conditional on a fixedsourceprior**, not marginalization over sourcecoefficients. They include no determinant/orthantnormalization/parameterintegration. Rawchi² differences likewise are not calibrated significances. ComparingMAPvalues across lnprecision0/2/4 as if selecting a statistically preferredregularization would be unjustified; code does not make thatclaim.

Atallfinalcases scaledKKT≤1.99e−13, all lens/quasar-amplitudes>18.48nativeintegratedfluxunits. Centralprecision directexactmass checks change objective+.10638/+.13859 (run04/run03), smallrelative tothestatedgaps but finite checks only. No finalcase lies atdeclaredscan/libraryedge. All masslocaltrials/gridfallback metadata retained. A bestexactgridnode can be labeledsuccessFalse while stillbeing a validfinite-gridresult; do not relabelit a convergedcontinuousglobaloptimum.

## Geometry/field/shape scope and material gaps

AQUALfield uses fixeda0, zl=.32022095721117494,zs1.210, edge-on oblateconstantM/L Sérsic with masscenter=lightcenter. Major-axisradius converted tophysicalunits once. projected_deflection includesDls/Ds; mappedrotates intrinsicmajor/minor deflections towest/north, appliesoddquadrant signs, interpolates radiallogcoordinate andmasslibrary. No extra distancefactor is applied byadapter. Exacttwo-point shear is solved anew perfield andsourcecenter followsmappedquasar, with independentpointfluxes. Therefore thetwoimagepoints alone do NOT measuremass; extendedhostplusnuisanceassumptions drives theprofile. Sourceoperator is continuousper-neighborzero-paddedbilinear with fullnormalizedVISPSF; finitegrid/edgebrightness andpixelquadrature are still modelinglimits.

**SIEcomparison is not a one-parameter a0 test.** pureSIE is defined ONCE fromrun04chosenmassparameters andcataloguemasscenter before thefixtureloop. It stays thatsameSIE even forrun03foregroundlightfixture. Thus it is a fixedreferenceSIE through a matchedlinearoperator, not an independentlyreoptimizedSIE for everylightfixture/positive-sourceprecision. Its radialmassfamily/ellipticity/orientation andcenter differfromAQUAL's lightfollowingmass. AQUALcenter is(−.144448,+.046739)arcsec; referenceSIEcenter(−.162976,+.091129), offset≈.048arcsec. TheforegroundSérsic itself is matchedwithineachcase, but themassshapes are not. Aχ²gap cannot isolatea0, identifydarkmatter, or be readasatheoryexclusion. A same-light/same-center Newtonian or alternativea0control is needed for that narrowercomparison; newton_control had no completedresult atthisreview and was not awaited.

Bothlightfixtures are earlierSIE-deblend-dependentpoint estimates, not independentphotometricpriors. Changingfield moves/resizes mappedsourcecoverage relative tothefixedgraphprior; sourceprior/gridcovariance is not an exactphysicalinvariance. Positivehostsource hasedgeflux and remainsfinitegriddependent. Inaddition, fixedquasarastrometry/PSFcenter, singleSérsiclight, zeroexternalconvergence, fixedinclination and diagonalnoise are materialconditions. StellarSEDmass was not independentlyvalidatedafterhostrepair and mustnotbe silentlyreintroduced aspreciseprior.

Libraryprojection/massinterpolation is approximate; SS8 and directfield controls are finite-numericalchecks, notuniformbounds. Masssearch scans11.2–11.5 in.01dex, expands onlyifedgecriteriontriggers, andrefinesatmostthreefinite-gridlocalminima. Narrow/missed minima betweeninitialnodes or outsideselectedintervals are notexcluded. This does not invalidate reportedfinitebestfits, but prevents universalglobaloptimalityclaims.

## Evidence and terminal state

Smallindependentexperiment: check_schur.py, contract.json, launch.json, run_01/{result.json,manifest.json}. Allsharedinputs unchanged, v2record validates. Reviewinput/outputSHA256s arelisted inreview_provenance.json, includingactualproductionpositive_01result andmanifest. Session8685 returnedcompleted; no reviewjob remainsactive. No largefits or newphysicalparameteroptimization were launched.
