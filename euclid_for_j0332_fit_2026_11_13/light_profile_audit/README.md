# FOR J0332 stellar-light profile audit

## What the primary methods establish

Cabanac et al.2005, Table1 and Section3 (cached primary external_cabanac.txt in screeninginputs; original https://arxiv.org/abs/astro-ph/0504585): PSF-corrected GALFIT fits tried deVaucouleurs,freeSersic and exponential profiles, masked the ring, varied sky within +/-3sigma, and reported best-fit deVaucouleurs profiles. Rc seeing was0.5arcsec. Their radii are Rc=.36+/-.05arcsec,i=.36(noerror),J=.41+/-.01,H=.43+/-.01,Ks=.50+/-.01; ellipticity1-q=.20+/-.10 across bands. Direct exactshort excerpt (11words): "This yields best-fit de Vaucouleur profiles with effective radii". TableRadiusconvention not explicitly defined in inspectedtext, so cannot assert semi-major versuscircularized. Atq~.8thisdistinction~12%,notfactor2–3. Radiusvalues andn4 are model-dependent reportedlight fits,not independent massprofilemeasurements.

ECLIPSE-D primary fetched nersesian.pdf/text from https://eceb.astro.uni-bonn.de/public/dr1/nersesian.pdf Section3.1: VISlens/sourcefit freescentre,ellipticity,n,Re,nprior.5–10. Re explicitly circularized=sqrt(ab). AllnonVIS structuralparameters are FIXEDtoVIS; onlyfluxnormalizations and globalimageastrometricshifts vary. Section6.1acknowledges wavelengthdependentRe/gradients canbiasrecoveredphotometry; Section3.2calls formalSersicfitposterioruncertainties unrealisticallysmall and adds empiricalphotometricerrorcalibration. That calibration does NOT supply a resolvedstellarM/Lgradient orjointshape posterior.

## Released unconvolved map verification

AnalyticSersic descriptivefits to pre_psf.fits GALAXY_0 in eightbands,allowingamplitude,centre,Re,n,q,angle separately, recover VIS/NIRYJH shape Re~1.1338arcsec,n~5.912,q~.813535, with tinyvariations~.01%. SlightdifferencefromCOOLESTpointRe1.13918,n5.86872 reflects pixelintegrationandfittingweights. DECamshapealsoessentiallysame;centresshift. These are FITS OF RELEASED TEMPLATES, NOT independentrawimage constraints. Exactresults map_shape_fits.json; fractionaltemplate residuals~.0003–.0006 over.3<r<3arcsec.

Thus similarNIRprofiles inreleasedmaps are imposed byconstruction. They do not verify MstarfollowsVIS,constantM/L,absenceofcolourgradients,orindependentNIRRe~1.14. The adoptedgravityfit must remain conditional on observedVISlightasstellarprofile.

## n/Re discrepancy

Euclidfree-n versus historicaln4 can cause radiusdegeneracy, but inspected evidence cannot establish it explains the fullhistoricaldifference. Descriptivefixedn4fits ofEuclidunconvolvedVISmap give Re.66–1.17arcsec dependingradialrange,not.36 (fixed_n4_comparison.json). Differentseeing,sky,ringmask,dataDepthandextendedwingscanmatter; no independentrawCabanacimagefit oruncertaintyjointlikelihood was performed,so do notdeclareeither publishedprofilewrong.

Illustrative unit-totalprojectedSersic light fractions within circularizedradius1.497arcsec: Euclidpoint .5631; historicaln4Rc .8537,H .8196,Ks .7876. These show why adoptingprofilefamilychangesmassnormalization; they are not truecircularaperture fractionsforellipticalprofiles,notallstellarcomponentmeasurements,and not physicalmassconstraints. See sersic_enclosed_light_comparison.json.

## Honest uncertainty propagation

CSVmarginalRe,n,q,centreintervals do notgivecovariance. IndependentGaussian draws would invent a jointposterior and break knownn/Redegeneracy. Validboundedoptions: (1)one-at-a-timeprofileperturbations labelled sensitivity, using suppliedmarginalquantiles; (2)extremalgrids labelled nonprobabilistic envelopes; (3)preferredfollowup: refitVISlenslight jointwithsource,mass,sky,PSF andsample correlatedshape posterior. To testmassfollowsVISrequiresindependentmultibandshape/colourgradientconstraints using actualbands/RMS/PSF,notreleasedfixedshapemodels; a fullSEDrefit is not donehere. Historicaln4families can be alternate systematicprofiles,not assignedposteriorprobabilityfromformalReerrors.

Additionaldocumentationconflict: DTable2note says spectroscopicredshift is fixedforSEDwhenavailable; releasedREADMEandportal sayphoto-zfixed. Do not assume thisparticularstellarMstarwasspeczfixed without row-levelverification. Thisdoesnotchange fixedshapefinding.

Codeaudit_maps.py;inputhashes.json recordsunchangedmaps/COOLEST/tableSHA256. No originalinputsmodified.
