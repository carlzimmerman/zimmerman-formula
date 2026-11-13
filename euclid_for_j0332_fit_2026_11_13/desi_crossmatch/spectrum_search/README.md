# Bounded L015780 source-multiplet search

Outcome: **no verified source redshift, and no multiplet candidate meeting the predeclared screening rule**. The scope is the finite redshift/width/mask scan below, not a sourceabsence or detectionlimit assertion.

Actualb/r/zflux+noiseviewerarrays were used. The embeddedRedrockmodel ColumnDataSource p266421,origwave/origflux0,was extracted toredrock_viewer_model.npz; model_extraction.json recordsidentity/grid7780points. Itsforegroundredshift is.42827037396. Noforegroundcontinuum guessedinplaceof availablemodel. Residual151pixelmediancontinuum removed aftersubtraction.

Contract.json declared zs.44–1.60 atdz.0002,observedGaussian sigma1.5,2.5,4A,independent OIIblend/Hbeta/OIIIdoublet/Halpha groups. OIII4959/5007ratiofixed.33557. Masksspecifiedbadnoise,strongsky,telluricandforegroundlinewindows. PerbandGaussianmatchedfilter inversevarianceweighted; overlappingcamerascombinenumerators/denominators. Aqualifyingcandidatewouldneed at least3distinctgroups>=3sigma,one>=5sigma,with3availablegroups. Noqualifyinggridpoints orlocalpeaks. Lyalpha/singlelinehighzinterpretationsnotattempted. Searchstarts.44,so.42827<zs<.44notcovered.

Strongestdiagnosticpeak z=.4538,sigma2.5A has OII1.719,Hbeta2.469,OIII2.887,Halpha.468 SNR; allsubthreshold. It is NOT a backgroundredshiftcandidateand receivesno redshiftuncertainty orphysicalinterpretation. Plot subthreshold_peak.png inspectedvisually; featuresdonotshowconvincingmultiplet. spectrum_diagnostic.png showsobservedflux/model/fullresiduals.

Independentcameraoverlapcheck:51retainedb/rbins,medianstandardizeddifference.0703,robustscatter.838;75r/zbins,median.2164,scatter.977. Noqualifyingcandidatefallsinneedofcamerarepeatvalidation; strongestdiagnosticOIIinb,Hbeta/OIIIinr,Halphainz. A line withindependentoverlapcouldbecheckedincameraseparately; singlecameraresidualisnotautomaticallyindependentconfirmation.

100nullrealizations usedindependent50pixelblocksignflips percamera,seed7419,eachrerunningallredshifts/widths. Nonepassedqualifyingrule. These nulls preservewithinblockstructure only; they neitherfullymodelsky/template residualsnor calibrateastrophysicalfalsealarmprobability. Evenapassingcandidatewouldrequireindependentlinevalidationandlookelsewhereaccounting. Noformal p-valuequoted.

## Provenance / validation

Initialadhoctrace renamed initial_run_trace.json; it is NOT a mathematicalmanifest. Authoritativeboundedrerun: run_01/manifest.json schema_version2,run.statuscompleted,validatedagainstprojectroot usingMathboxvalidate_manifest.py. Code,exactinputs,contracthashesbefore/after,command/runtime/randomseed recorded. run_01/result.json isauthoritativefiniteoutput. contract.json ispredeclaredscreeningdetails; bounded_contract.json isrunnercontract. EnvironmentPython3.9.6,numpy1.26.4,scipy1.13.1. Zeroexit/validmanifest establishesprovenance,notastrophysicalcorrectness.

Viewerdata lackFITSresolutionmatrices/maskbitvectors; spectraresampling/correlations/sky/templateerrorsunmodelled. FixedwidthGaussiansandfixedOIIblendmaymissbroader,narrower,absorbedorunusuallineratios. Atzs>~1onlyOIIofthelistedgroupsusuallyvisible,so3groupcriterionisintentionallyincapableofconfirminghighzsinglelinecases. Nullresultcannotruleoutsuchsources. Fullrawcoaddnotdownloaded; noauthorscontacted.
