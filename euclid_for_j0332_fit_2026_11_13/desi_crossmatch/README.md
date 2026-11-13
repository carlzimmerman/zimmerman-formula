# Official DESI DR1 strong-lensing VAC crossmatch

Original requested unversionedfile returned404. Officialdirectoryindex exposed v1.0; HEADthenGETof https://data.desi.lbl.gov/public/dr1/vac/dr1/strong-lensing/v1.0/desi-sl-vac-v1.fits succeeded. Size596160bytes; SHA2560fb81f2272635605244e0c024b8405219f30d60ed60b58c0ed3079c47d3139b0 MATCHESofficial.sha256. Headershead_v1.txt/response_headers.txt; exactprovenance inprovenance.json.

Primarydocumentation https://data.desi.lbl.gov/doc/releases/dr1/vac/strong-lensing/ . Actualfilecontains2176observationrows/45columns,notallcolumnslistedinwebsitegenericschema. PositionsTARGET_RA/DEC,redrockZ/ZERR/ZWARN/DELTACHI2,VDISP/VDISP_IVARpresent. No separatelens/sourceZcolumns. It is a spectroscopytargetVAC,notallDESIspectraorallstronglenses.

Reproducecrossmatch.py withfitvenv. Contractcommittedbeforeclassification incontract.json; sourceECLIPSECSVhashrecorded. Matchradius1arcsec toall15072A/Bscreenrows. Exactly5matchedobservationrows,5uniqueTARGETIDand5uniquelenses; allpasspreliminaryGALAXY,ZWARN0,fiberstatus0,DELTACHI2>=40criteria. FourhavefinitepositiveVDISP/IVARandfractionalerror<.30. These are transparentheuristics,notcompleteDESIkinematicvalidationandnotconfirmationthatspectrumisolateslensratherthansource/blend. No redshiftpairwasmanufacturedfromthesingleredrockZ.

## FOR J0332

NoVACrowwithin1arcsec(oranynearby). Closestcataloguetarget17.3433degreesaway. Thus NO independentVDISPmeasurementforFORJ0332inthisspecificpublicVAC. ThisdoesnotexcludeotherDESI,SDSS,ESOorunpublishedspectroscopy. Cabanac302km/sisfromlensmodelandcannotbeusedasobserveddynamics.

## Followup

Bestcombinedexistingphotometry/model/VDISPscreen: EUCL-DR1-L015780,J100537.754+673027.15,gradeA,modelSuccess,final_sampleTrue; DESITARGETID39633467440368852,sep.09872arcsec,z=.42827037396,VDISP289.09094+/-45.77872km/s. ECLIPSEphotoz.43,logM11.69542. Source-redshiftstatusmissinginexistingscreenandVAC; obtainingverifiedsourcezandcheckingactualspectrumqualityisrequiredforquantitativelensing+dynamicsfollowup. This is candidatedataavailability,nottheoryvalidation.

Otherinteresting: L018096,J041203.472-185914.59,gradeA,final_sampleTrue,z=.4414461,VDISP379.82+/-83.14km/s,butmodelNoConsensus; L000216hasVDISP295.52+/-41.48butNoConsensus/notfinalsample;L001368modelSuccess,VDISP314.03+/-63.33,butECLIPSEstellarphotometrymissing;L002239MultiGalaxyLensandVDISP402.68+/-143.14fails30%precisioncut. Fullrow-levelresults matches_1arcsec.csv.

Radius-screenrobustnessnotestablishedoutside1arcsec,andfiberfluxblending/aperture/seeingcorrectionsmustbehandledbeforeusingVDISPinJeansanalysis. SourcezandobservedVDISPcannotbeinterchangedwithSIE-inferredvelocitydispersion.
