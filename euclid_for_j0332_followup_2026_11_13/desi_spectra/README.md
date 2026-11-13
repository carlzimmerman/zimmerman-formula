# Four remaining Euclid–DESI sources: bounded checkpoint

**No independent source redshift recovered.** Four individual officialDESIviewer pages andtheir originalcamera flux/noise arrays+embeddedRedrock foregroundmodels were retrieved. Fourseparate boundedmultipletscans completedandtheirMathboxv2manifestsvalidated. No qualifyingcandidate. This advancesavailability/searchroute butdoesnotproduce a combinedlensing–dynamicsmeasurement.

|Target|Viewerforegroundz|Highestdiagnosticpeak|OII SNR|Hbeta SNR|OIIIgroup SNR|Outcome|
|---|---:|---:|---:|---:|---:|---|
|L000216|.43165543|.670255|4.31|2.19|.11|Rejected:singlefeaturedominates|
|L018096|.44144605|.695046|1.09|-2.47|4.88|Rejected:OIIIonly,Hbetanegative|
|L001368|.43246609|.603666|2.61|-.38|3.09|Rejected:nomultiplet|
|L002239|.53052004|.550920|1.32|3.87|.03|Rejected:nomultiplet|

These redshiftpeaks are **not source-redshiftcandidates** andhave noassignedastrophysicaluncertainty. Halphaoutsidecoverageatthesepeaks. No singleline/OIIIgroupalonepromoted. Sourceclaimsrequiremultipleindependentfeaturegroups; component4959and5007doNOTcountastwoindependentgroups.

## Data / targetidentity

Each EUCL-*directory containsviewer.html,responseheaders,fetch_provenance.json(rawURL/UTC/SHA/bytes/cataloguerow), spectrum.npz,model.npz,metadata.json andextraction_provenance.json. Originalwave/flux/noiseBokeharrays decodedwithoutresampling; Redrockmodel interpolation occursonlyinsearch. CorrectTARGETIDassertedbeforeanalysis. TotalHTML~6.25MB;nohundredsMBbulkcoadddownloaded. Officialviewerroutes:

- L000216 https://www.legacysurvey.org/viewer/desi-spectrum/dr1/targetid39633487598190898
- L018096 https://www.legacysurvey.org/viewer/desi-spectrum/dr1/targetid39627334772333431
- L001368 https://www.legacysurvey.org/viewer/desi-spectrum/dr1/targetid39627911682067852
- L002239 https://www.legacysurvey.org/viewer/desi-spectrum/dr1/targetid39633493826734184

L000216viewerz=.4316554267differsVAC.4316111289by.00004430,smallerthanVACformalZERR.00011261;likelycoadd/reductionselectiondifference,notassumedidenticalobservation. Analysisusesviewerzmatchingitsownmodel. OthersagreewithVAC. Metadataandprovenancepreserved;dataidentityisTARGETID,notmerelynearbycoordinate.

## Predeclared finite search

Adaptedpriorphasevalidatedscreeningmethod,withEACHforegroundredshiftandmaskupdated. Targetcontractjsonprecedesrun. zsfromviewerzl+.01to1.6,dz.0002;observedGaussian sigmas1.5/2.5/4A;OIIblend,Hbeta,OIIIdoubletfixedratio,Halpha. Positivenoise/finitebins;strongsky,telluricandforegroundlinemasks. Atleast3availableindependentgroups SNR>=3 andone>=5required. Noqualifyinggridpoints/peaksforanytarget.100independent50pixelblocksignflipnullspercamerapertarget:0qualifyingrealizationsineach100,notacalibratedfalsealarmprobability. Fourtargets,multiplelinewidthsand~5800ztrialsperobjectcompoundlookelsewhere;notcountingthesetrialsasindependentevidence.

Eachrun_01/manifest.json schema2statuscompleted,hashesbefore/afterandcommandrecorded,validatedagainstprojectroot. run_01/result.jsonauthoritative;summary.jsoncollectsresults. prepare.pyextractionhashesrecordedseparately. Initialadhocmethodnotmislabelledav2manifest. plot_results.pycreatesfullspectrum,subthresholdzoom,camera_checks.json. PriorityL000216/L018096zoomsvisuallyinspected;theyreinforcerejectionofmultipletinterpretation.

## Aliases / independentpublishedz

Read-onlyearlierECLIPSEscreenidentifiesallfourasearliestHuang2021 (2021ApJ...909...27H),withaliasesDESI-180.7746+69.8060,L000216;DESI-063.0145-18.9874,L018096;DESI-012.6879+05.1953,L001368;DESI-185.6850+70.6065,L002239. PriorphaseprimarycatalogueJ/ApJ/909/27containsforegroundzphot/spec,notverifiedsourcez. L001368discoveryzspec.3940differscurrentDESI.432466;cannotreinterpretoneasbackgroundsourcewithoutoriginalspectralvalidation. No independentlypublishedzsestablishedbythisboundedroute. Thisisnotanexhaustiveallliteratureproof.

## Interpretation / nextdecision

ObservedVDISPexistsbutneedsspectralsystematicsandaperturevalidation;missingzsblocksphysicaljointlensing–dynamicsinference. Noauthorscontacted. Viewerdata lackrawresolutionmatrices/maskbits;simplewidths,noise/template/skyresidualsandunknownsourceemissionmeansnullsearchcannotexcludesources. Atzsabove~1onlyOIIofthechosenfeaturesusuallyvisible;thesearchintentionallycannotconfirmsingleline/highzLyaobjects. Additionalvalidatedspectroscopy/otherlinecoveragewouldberequired,orbroaderpublicpaired-redshiftcatalogueroute,notrelaxingthresholdsuntilnoisebecomes'confirmation'.
