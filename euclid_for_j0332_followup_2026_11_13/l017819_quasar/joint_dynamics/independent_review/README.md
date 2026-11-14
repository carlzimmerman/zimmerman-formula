# Independent review of axisymmetric Jeans v2

**Verdict: equations and projection pass the stated restricted-model checks; actual high-n AQUAL numerical convergence and observational interpretation remain conditional.** No shared code was edited. This is not an endorsement of a theory fit.

## Equations and coordinate derivation

Primary checked: Cappellari2008 arXiv0806.0042v2 https://arxiv.org/html/0806.0042v2 , Section3.1.1 equations10–11 and Section3.1.5 equation35. These require cylindrical alignment, zero mixed Rz moment and constant b. They do not require the potential to be self-generated Newtonian gravity. Positive distribution functions are not guaranteed by Jeans solutions. k=1 means equal radial/azimuthal dispersions; full isotropy additionally requires b=1.

Independently let P=nu*<vz²>, gR=∂RΦ, gz=∂zΦ, no meridionalstreaming. Vertical equation gives P(R,z)=∫z∞nu*gz dz. Constantb gives <vR²>=bP/nu, and the radial equation gives <vphi²>=b(R∂RP+P)/nu+R*gR. Code's derivative with respect tolnR is exactly R∂RP. Reverse cumulativeSimpson correctly gives positive vertical pressure for positivegz atz>0 without subtracting nearlyequal cumulativeintegrals. Force must mean positivepotentialgradient, not inwardacceleration; actual producer gr/gt follows that convention.

Coordinate transform is x=u, y=los*sin(i)−v*cos(i), z=v*sin(i)+los*cos(i). LOS unitvector=(0,sin(i),cos(i)); its radial/azimuthal dotproducts are sin(i)*y/R and sin(i)*u/R. Thus projectedsecond=sin²(i)[<vR²>y²/R²+<vphi²>u²/R²]+cos²(i)<vz²>, as implemented. Firstmoment uses sin(i)*(u/R)*sqrt(<vphi²>−<vR²>) under k=1. Polararea integrates r dr dphi=r²dlnr dphi; LOS r*tan(t) Jacobian is correct.

ncx2.cdf((fiber_radius/seeing_sigma)²,df2,offset_distance²/seeing_sigma²) is exactly the throughput of a circular fiber for a circular normalizedGaussianPSF. Applying it to intrinsic surfacebrightness and moment numerators before ratio correctly includes seeing spillover and offset. The final centeredvariance is integratedrawsecond minus integratedmean squared, so unresolvedrotation is included rather than locally subtracted away.

## Independent non-spherical benchmark, actually executed

run_01/result.json uses a flattenedGaussian tracer with sR1,sz.6 in harmonicpotential Phi=(omegaR²R²+omegaz²z²)/2,omegaR2,omegaz3. This is not the root sphericalPlummer benchmark. Exactverticalmoment V=omegaz²sz²=3.24; exactazimuthalmoment bV+(omegaR²−bV/sR²)R². Projectedsurfacebrightness is an ellipticalGaussian with minorvariance sR²cos²i+sz²sin²i. Projectedrawsecond atsky(u,v) is V(bsin²i+cos²i)+(omegaR²−bV/sR²)sin²i*u²; projectedmean=k*sin(i)*sqrt(omegaR²−bV/sR²)*u.

Independently integrated these analyticprojectedfunctions with100×100GaussHermite skyexpectations and the finiteGaussianseeing fiberthroughput; no sharedLOS or polartrapezoid algorithm. Tested b=.8,1,1.2; inclinations0,45,90; offset(.2,−.1), plus reversedoffset at90; radius1,sigmaSeeing.25. Code uses440momentnodes,200radial×64phi×160LOS projection.

Observed maximum pointwiseverticalrelativeerror5.46e−5; maximumazimuthalrelativeerror6.39e−4 over25×25central(R,z)probes. Aperturelight relativeerror≤1.81e−7; rawsecond relativeerror≤8.94e−5; meanabsoluteerror≤5.69e−5 infixturevelocityunits. Offsetreversal changesmeansign andpreserveslight/second as expected. All registered assertions passed; v2manifestcompletedvalidated withcurrentinputs. These support numerical implementation in this finite smoothfixture, not an intervalbound orhigh-nAQUALaccuracycertificate.

## Actual loader/schema and astrometry

Read bothactual best_field_refined.npz: shape448×80, finitegr/gt, monotone radial/angularnodes; logmasses11.3043146996(run03),11.3665655666(run04), zl.32022095721117494,zs1.21,a0SI9.3603e−11. light array is[cx,cn,lnRe_major,lnn,q,phi_west]. Loader exp(light[2])*kpc_per_arcsec therefore correctly uses majoraxisphysicalradius, without doublecircularization. Unit-total Abeltracer density/q/re³ is appropriate; its arbitraryluminositynormalization cancels in momentratios. Force sphericalpolar→cylindrical conversion signs andreflection atnegativez agree with producer. Sphericaltail usesmass anda0units consistently. It is still an assumedtail, not angularmultipole validation.

NativeVISFITS WCS is used for MEAN_FIBER_RA/DEC withzeroorigin; pixel49.5 subtraction defineslocalcutout coordinates. Root's nativefiber(-.28838927,−.05529467)arcsec and lightrelative(-.14394110,−.10203393) are compatible withthatconvention. Rotatingthis vector by lightPA correctly produces major/minoroffset. Separate wcs_vis_lp.json originmustnotreplace nativeFITScenter. WCSroundtrip validatesinverseconsistency, not surveyabsoluteastrometricaccuracy.

Runner main angularscale is hardcoded to this lensredshift rather than derived/asserted perfield. It matches BOTH auditedfiles exactly here, so no current mismatch was found; general reuse needs explicitassertions. Likewise the separate specification.physical_light must agree withNPZlight for offsetrotation/centering; loadercurrentlydoesnotassertthis. Inclination is notstored in theNPZschema; actualfieldproducer usesedge-on.

## Material qualifications

1. Loaderusesobservedq directlyasintrinsicflattening: consistent atedge-on(default90). Simply changing aperture(inclination) does NOT construct the correspondingnew oblatedeprojection/potential. Otherinclinations require recomputingbothdensityandfield with qint²=(qobs²−cos²i)/sin²i. Gaussianbenchmarkinclinationtests exerciseprojection oftheSAMEintrinsicfixture, notnewobserved-profiledeprojections.
2. b is sigmaR²/sigmaz²; beta_z=1−1/b. It is NOT the spherical beta usedinmany lensJeanspriors. b=.8,1,1.2 correspondsbeta_z=−.25,0,+.1667. k=1atb≠1doesnotmeanfullyisotropic.
3. CodeclipsnegativeSatohdelta underthesqrt andreportsinvalidlightfraction. Ifthisfractionismaterial, k1means/centeredsigmas are NOT a physicalSatohsolution; rawsecondmaystillhaveitsownvalidity. Negativeazimuthal/verticalmoments and negativeintegratedsecond must invalidate interpretation; RMS's max(second,0) guard is not a physicalrepair. Codeonlyexplicitlyreportsnegativeazimuthalmoments atspecifiedtolerance; checkverticalpressure too.
4. OutsideR/z momentgrid values arezero while tracerlight stays in denominator. outside_moment_grid_light_fraction thereforediagnosesnumeratordilution; a smallLIGHTfraction alone is NOT a rigorous boundonmissedSECONDmoment. Furthermore finiteverticalboundarypressure affectsinterior moments and isnotmeasuredbyoutsideprojectedlightfraction. Extent/node/LOS/rmin convergence must be assessed on actualhigh-ntracers. BelowRmin interpolationclamps; belowmomentgridlight isnotseparatelyreported. Logcoordinates and farfieldforceclipping/continuation needactualsourceconvergencechecks.
5. GaussianPSFseeing,FWHM conversion and.75arcsecfiber are explicitassumptions/scenarios; no measuredexposureseeing hasbeenestablished. ActualchromaticPSF, throughput/quasarcontamination andluminosity-weightedLOSVD differfroma mathematicallyGaussianfit when LOSVDisnonGaussian. PublishedpPXF sigma is notautomaticallyanexactmodelsecondmomentwithGaussianerrors. Stellartracerlight isSIE-deblend-dependent andmultibandphotometryhasnotyieldedavalidindependentmassprior.
6. PositiveJeansmoments are necessarybutnot sufficientfora positiveDF orstablegalaxy. No orbitdistribution,screenedfullaction,externalfield orphysicaltheoryexclusion iscertifiedhere.

Strongestsafestatement: v2 passes a genuinelynon-spherical exactmoment+independentfinitefiberprojection benchmark. ActualAQUAL predictions canbe reported as explicitlyconditional dynamical scenarios once thefield/extent/grid convergence andmomentpositivity reports are checked; they cannotyetbe promotedtoa completeobservational likelihood or a calibratedtheoryexclusion.
