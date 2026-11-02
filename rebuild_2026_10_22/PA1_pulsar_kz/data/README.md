Data file for "Empirical Modeling of Magnetic Braking in Millisecond Pulsars to Measure the Local Dark Matter Density and Effects of Orbiting Satellite Galaxies". 

Description of Folders: 
=======================================
v1: Dataset that was used in the original arXiv posting of Donlon et al. (2025). 

v2: Updated dataset with some minor changes:

	- Addition of distance to the catalog
 
	- Some new distance and proper motion data incorporated from ATNF after submission of paper
 
	- PSR J1453+1902 has been removed due to negative parallax
 
	- Proper motion now in units of mas/yr
 
	- Binary orbital period now in units of days
	
v3: Removed several pulsars from the data. This is the final version that was used in the published version of the paper. 

	- These include 5 black widows: J0023+0923, J0610-2100, J0636+5128, J1653-0158, and J2241-5236.

	- J2043+1711 was accidentally left in the catalog. It has been removed. 


Description of Files: 
=======================================
data.csv:  Full dataset. Modeled spindown and spin acceleration values are only provided for sources where these quantities are believed to be accurate (in other words, only for pulsars that satisfy the BSURF and CHAR_AGE cuts from the paper). 

binary_only.csv:  Only the data for the binary millisecond pulsars (no spin data). 


Description of Columns: 
=======================================
NAME:  Name of PSR 

GL:  Galactic longitude (degrees)

GB:	Galactic latitude (degrees)

PX:	Parallax (mas)

PX_ERR:	Uncertainty in parallax (mas)

PMTOT:	Total proper motion (mas/yr)

PMTOT_ERR:	Uncertainty in total proper motion (mas/yr)

DIST:	Distance to the pulsar (kpc). NOTE: This is a curated distance list, and is not necessarily equal to 1/PX! (Use this instead of 1/PX for analysis)

DIST_ERR:	Uncertainty in distance (kpc)

PS:	Spin period (s)

PS_ERR:	Uncertainty in spin period (s)

PSDOT_OBS:	Time derivative of the observed spin period (what is measured by PTAs) (s/s)

PSDOT_OBS_ERR:	Uncertainty in PSDOT_OBS (s/s)

PSDOT_SHK:	Shklovskii term for the spin period derivative (s/s)

PSDOT_SHK_ERR:	Uncertainty in the spin Shklovskii term (s/s)

PSDOT_B:	Directly computed intrinsic spindown term (see Eq. 7 of the paper) (s/s)

PSDOT_B_ERR:  Uncertainty in PSDOT_B_ERR (s/s)

MODEL_PSDOT_B:	Modeled intrinsic spindown term (see Eq. 12 of the paper) (s/s)

MODEL_PSDOT_B_ERR:	Uncertainty in MODEL_PSDOT_B (s/s)

ALOS_PS:	Line-of-sight acceleration, assuming MODEL_PSDOT_B is correct. The Shklovskii and magnetic braking terms have already been removed from this value. Equal to the Galactic acceleration assuming no other effects are present. (mm/s/yr = cm/s/decade)

ALOS_PS_ERR:	Uncertainty in ALOS_PS (mm/s/yr)

PB:	Binary orbital period (days)

PB_ERR:	Uncertainty in PB (days)

PBDOT:	Observed time derivative of the binary orbital period (what is measured by PTAs) (s/s)

PBDOT_ERR:	Uncertainty in PBDOT (s/s)

PBDOT_SHK:	Shklovskii term for the binary orbital period derivative (s/s)

PBDOT_SHK_ERR:	Uncertainty in PBDOT_SHK (s/s)

PBDOT_GR:	GR term for the binary orbital period derivative (decay from grav. wave emission) (s/s)

PBDOT_GR_ERR:	Uncertainty in PBDOT_GR (s/s)

ALOS_PB:	Line-of-sight acceleration, calculated using the binary orbital period data. The GR and Shklovskii terms have already been removed from this value. Equal to the Galactic acceleration assuming no other effects are present. (In most cases, use this over ALOS_PS if available, but consult ALOS_PS_ERR and ALOS_PB_ERR) (mm/s/yr)

ALOS_PB_ERR:	Uncertainty in ALOS_PB (mm/s/yr)

BSURF:	Minimum surface magnetic field strength at the surface of the pulsar, assuming a dipole magnetic field approximation (G)

BSURF_ERR:	Uncertainty in BSURF (G)

CHAR_AGE:  Characteristic age (s)

CHAR_AGE_ERR:  Uncertainty in CHAR_AGE (s)
