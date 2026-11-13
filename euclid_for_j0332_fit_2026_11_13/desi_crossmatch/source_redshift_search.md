# Bounded source-redshift recovery search (2026-11-13)

All five DESI/ECLIPSE crossmatches cite Huang et al.2021 discovery. Primary catalogue https://cdsarc.cds.unistra.fr/viz-bin/ReadMe/J/ApJ/909/27?format=html&tex=true ; small1312rowtable retrieved as huang2021.tsv from https://vizier.cfa.harvard.edu/viz-bin/asu-tsv?-source=J/ApJ/909/27/cand&-out.all&-out.max=unlimited . Its zsp(SDSSDR16) and zph(Zhou2021) describe candidateforegroundgalaxies; no source-zcolumn. Exactmatchedaliases:

|ECLIPSE|Discoveryalias|Discoveryredshiftfield|
|---|---|---|
|L015780|DESI-151.4072+67.5076|zphot.431+/-.017, nospecz|
|L001368|DESI-012.6879+05.1953|zspec.3940 in discoverytable; differscurrentDESI.432466, not a verifiedsourcez|
|L002239|DESI-185.6850+70.6065|zphot.568+/-.035|
|L000216|DESI-180.7746+69.8060|zphot.416+/-.024|
|L018096|DESI-063.0145-18.9874|zphot.572+/-.073|

Exactcoordinate/sexagesimal/decimalaliaswebqueries and originalprimarycatalogue did not yield independentlyverifiedbackground-source redshifts. This is boundednullsearch,not proofthatnoneexists. No newsourcezassigned. Source redshift remains required for completeobservedlensing+dynamicscomparison.

## Actual individual L015780 observed spectrum recovered

OfficialDESIdata-accessdocumentation https://data.desi.lbl.gov/doc/access/ describes TARGETIDviewer and SPARCLsingle-spectrumretrieval. Targetviewer https://www.legacysurvey.org/viewer/desi-spectrum/dr1/targetid39633467440368852 was fetched as target_spectrum_page.html (1559790bytes), not a bulkcoadd. Page embeds originalb/r/z-camera wavelength,fluxandnoise arrays. extract_viewer_spectrum.py decodesgzip/base64Bokehorigwave,origflux0,orignoise0 WITHOUTresampling into L015780_viewer_spectrum.npz (2751,2326,2881bins). L015780_viewer_metadata.jsonconfirms TARGETID39633467440368852,foregroundGALAXYz=.428270373960303,ZERR.00010673116;humanVI_z/commentfieldsblank. These viewerarrays support laterforegroundsubtraction/emissionlineinspection; decodingaloneisnotnewsourceredshiftmeasurement. They lackrawFITSresolutionmatrices/maskbitsandarenotclaimedcompletecalibratedspectralproduct. HTMLandNPZhashes/observedURL inviewer_extraction_provenance.json.

VACrecordSURVEYmain,PROGRAMbright,HEALPIX7582. Officialdirectorylisting wasobserved/cached ashealpix7582_index.html:
https://data.desi.lbl.gov/public/dr1/spectro/redux/iron/healpix/main/bright/75/7582/
Exactcoaddlink https://data.desi.lbl.gov/public/dr1/spectro/redux/iron/healpix/main/bright/75/7582/coadd-main-bright-7582.fits is364858560bytes; NOTdownloaded. spectra-main-bright-7582.fits.gz is421299412bytes; NOTdownloaded. redrock-main-bright-7582.fits is740160bytes;notneededforthisboundedsearchandnotdownloaded. No unsupportedindividualFITSqueryURLinvented.

## Additional primary followupleads

HSTprogram18085visit57 listsDESI-151.4072+67.5076 asFlightReady(WFC3/UVIS),notarchived/observed: https://www.stsci.edu/hst-program-info/visits/?program=18085 . HST17307visitBW similarlylistsDESI-180.7746+69.8060 asFlightReady(ACS/WFC): https://www.stsci.edu/hst-program-info/visits/?program=17307 . These are proposed/plannedimaging,NOT source-spectroscopymeasurementsornewpublicimages. Statusmaychange;observedsearchdateabove.

Mostactionablenextstepis useactualL015780spectrumforforegroundtemplate subtractionandmulti-linebackgroundcandidate search, then independentlyvalidate lineidentification. A singlelineguess mustnotbe promoted tosecurez. Noauthorscontacted.
