# Dynamical rotating-state checkpoint

User asked dynamically derive state including rotation/cooling, reduceparams,
conserveenergy and testdisk tether vsdwarf/cluster freewithouttypeswitches.
New rotating_state folder only. Evolved 2coherent packets, incoming .2 and
transverse0/.5, two charged Schrodinger fields, Coulomb+Newtonselfgravity,
fixedPlummerbaryonpotentialmass1/5.364. G=Md=b1;h=hbar/(m sqrt(GMd b)).
Normeach1/(1+eps);allmassandcounterchargeslive. Coherence assumed; baryons notlive.

Coolingchannel=explicitmatterwaveenergytransport fromcore r<2.5 toexterior,
no friction ordeletedenergy. Periodicbox; photonradiationnotimplemented.
Coreenergyhalfselfpotentialconvention;transportnotproofirreversiblerelaxation.
Exacteps1 equalfields invariant=>rhocharge0 forrotation/collapse, noelectric
support. Offset.05 equalmass tested; epsilon.1 spreadsminus andproducessupport
butboth nonrotatingandrotating, notdiskselector.

12mainconfigs h.5/1 *[(eps1offset0),(eps1offset.05),(eps.1offset0)]*spin0/.5.
6refinements N32/48dt.01/.005/.0025eps1offset.05h.5spin.5. 4boxprobeconfigs
N32L16/N48L24h.5eps.1spin0/.5 (2duplicatesreference). Alltime1.
Energymaxmain2.71e-6,number8e-15;partition1.78e-15. Refinementenergy
2.45e-7,6.13e-8,1.53e-8;stateerrorsfactor4. HamiltonianFD2.42e-11,
roundtrip1.13e-15. SymmetricchargeL1~1e-15support0.

Largeboxeps.1h.5: support96.43%noorbit/95.02%orbit, merelyoutwardforce
window0.5..1.5g; NOTtetherfraction. Coreenergychange-.48427/-.49471,
coremasschange-.00340/-.02412;edge.148/.152%. Smallboxedge1.7%,supportdiff
~.1percentagepoint. h1lightmassrunsedge4.9%, noescapeclaims.
Coremassspatialnotconverged .7816N32vs.8097N48 inrefine; sharp mask quadrature
notseparatedfromfield error. Lzdrift~9e-5equalmassrot,.052worstlightmass.
Periodickernel/gridnotcontinuousrotationinvariant. NoisolatedLzclaim.

Physicalmapping482points2eps*241m:0meetcommon32³rotationphase-resolution
andnonrelcriteriaforfourprofiles. Numerical limitation notphysics exclusion.
Atm1e-22eVh=13.30,.3991,.009408,2.304e-5. Dimensionlessrunsnot4galaxies
withcommonmass. Coherentdipoleradiationestimateeps.1A1loss/tdyn=
4.94e-15,4.94e-12,1.40e-8,9.50e-7; notbound/notactualemission/noenergysubtraction.

run_state,run_refine,run_probe completedvalid. Noactivejobs. No exactmanybody
thermalization,statepreparation,stabletethers,freeboundretention orRARderived.
ReadREADME/AUDIT before interpreting. Priorfilesunchanged; no publication.
