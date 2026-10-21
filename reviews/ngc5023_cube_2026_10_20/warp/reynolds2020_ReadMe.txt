J/MNRAS/493/5089  HI asymmetries with LVHIS, VIVA, and HALOGAS (Reynolds+, 2020)
================================================================================
HI asymmetries in LVHIS, VIVA, and HALOGAS galaxies.
    Reynolds T.N., Westmeier T., Staveley-Smith L., Chauhan G., Lagos C.D.P.
   <Mon. Not. R. Astron. Soc., 493, 5089-5106 (2020)>
   =2020MNRAS.493.5089R    (SIMBAD/NED BibCode)
================================================================================
ADC_Keywords: Clusters, galaxy ; Galaxies, group ; Galaxies ; Radio lines ;
              H I data ; Spectroscopy
Keywords: galaxies: clusters: general - galaxies: groups: general -
          radio lines: galaxies

Abstract:
    We present an analysis of morphological, kinematic, and spectral
    asymmetries in observations of atomic neutral hydrogen (HI) gas from
    the Local Volume HI Survey (LVHIS), the VLA Imaging of Virgo in Atomic
    Gas (VIVA) survey, and the Hydrogen Accretion in Local Galaxies
    Survey. With the aim of investigating the impact of the local
    environment density and stellar mass on the measured HI asymmetries in
    future large HI surveys, we provide recommendations for the most
    meaningful measures of asymmetry for use in future analysis. After
    controlling for stellar mass, we find signs of statistically
    significant trends of increasing asymmetries with local density. The
    most significant trend we measure is for the normalized flipped
    spectrum residual (A_spec_), with mean LVHIS and VIVA values of
    0.204+/-0.011 and 0.615+/-0.068 at average weighted 10th
    nearest-neighbour galaxy number densities of log({rho}_10_/Mpc^-3^)
    =-1.64 and 0.88, respectively. Looking ahead to the Widefield ASKAP
    L-band Legacy All-sky Blind survey on the Australian Square Kilometre
    Array Pathfinder, we estimate that the number of detections will be
    sufficient to provide coverage over 5 orders of magnitude in both
    local density and stellar mass increasing the dynamic range and
    accuracy with which we can probe the effect of these properties on the
    asymmetry in the distribution of atomic gas in galaxies.

Description:
    We use the Local Volume HI Survey (LVHIS, Koribalski et al.
    2018MNRAS.478.1611K, Cat. J/MNRAS/478/1611), the VLA Imaging of Virgo
    in Atomic Gas survey (VIVA, Chung et al. 2009AJ....138.1741C), and the
    Hydrogen Accretion in Local Galaxies survey (HALOGAS, Heald et al.
    2011A&A...526A.118H) to investigate the influence of environment
    density on measured morphological, kinematic, and spectral asymmetry
    parameters.

    The Local Volume HI Survey (LVHIS, Koribalski et al.
    2018MNRAS.478.1611K, Cat. J/MNRAS/478/1611) was carried out on the
    Australia Telescope Compact Array (ATCA), observing HI in 82 nearby
    (<10Mpc) gas-rich spiral, dwarf, and irregular galaxies. The majority
    of LVHIS galaxies are members of local groups or pairs and have at
    least one close neighbour with an angular separation of <300arcsec
    (projected separation <17kpc) and a systemic velocity <800km/s. We
    exclude galaxies which are not covered by the 6dF Galaxy Survey due to
    incompleteness. We use LVHIS stellar masses from Wang et al.
    (2017MNRAS.472.3029W).

    The VLA Imaging of Virgo in Atomic Gas survey (VIVA, Chung et al.
    2009AJ....138.1741C) imaged 53 late-type galaxies in HI using the Karl
    G. Jansky Very Large Array (VLA) at an angular resolution of
    ~15arcsec. Here we use a subsample of 45 galaxies for which the
    reduced HI spectral line cubes are available.

    The Hydrogen Accretion in Local Galaxies survey (HALOGAS, Heald et al.
    2011A&A...526A.118H) on the Westerbork Synthesis Radio Telescope
    (WSRT) imaged 24 spiral galaxies in HI at an angular resolution of
    ~40arcsec. The HALOGAS sample is composed of galaxies residing in
    pairs and groups and includes both dominant and minor group members.
    Here we use a subsample of 18 galaxies which lie within the SDSS
    spectroscopic survey footprint (Strauss et al. 2002AJ....124.1810S).

File Summary:
--------------------------------------------------------------------------------
 FileName      Lrecl  Records   Explanations
--------------------------------------------------------------------------------
ReadMe            80        .   This file
tablea1.dat       62       79   Asymmetry parameters for LVHIS galaxies
tablea2.dat       61       45   Asymmetry parameters for VIVA galaxies
tablea3.dat       61       18   Asymmetry parameters for HALOGAS galaxies
--------------------------------------------------------------------------------

See also:
  J/MNRAS/478/1611 : Local Volume H I Survey (LVHIS) (Koribalski+, 2018)

Byte-by-byte Description of file: tablea1.dat
--------------------------------------------------------------------------------
   Bytes Format Units     Label     Explanations
--------------------------------------------------------------------------------
   1-  8 A8     ---       Name      Galaxy name (LVHISNNN)
  10- 14 F5.2   [Mpc-3]   logrho    Logarithm of the environment density
                                     computed using the 10 nearest neighbours
                                     (Section 2.4)
  16- 19 F4.1   [Msun]    logMass   ? Logarithm of the stellar mass
  21- 22 I2     km/s      DVsys     Difference between the flux weighted mean
                                     systemic velocity and the systemic velocity
                                     defined as the mid-point of the spectrum at
                                     50% of the spectrum's peak height
                                     (Section 3.1.1)
  24- 25 I2     km/s      DVsysopt  ? Difference between the flux weighted mean
                                     systemic velocity from the HI spectrum and
                                     the optical velocity (Section 3.1.1)
  27- 31 F5.3   ---       Aspec     ? Spectrum residual (G1)
  33- 36 F4.2   ---       Aflux     ? Ratio of the integrated flux in the left
                                     and right halves of the spectrum divided at
                                     the systemic velocity (Section 3.1.2)
  38- 41 F4.2   ---       Apeak     ? Ratio between the left and right peaks of
                                     the spectrum (Section 3.1.3)
  43- 46 F4.2   ---       Amap      ? Bias corrected asymmetry parameter of
                                     integrated intensity (moment 0) map
                                     (Section 3.2.1)
  48- 51 F4.2   ---       <A1>      ? Mean first harmonic coefficient from
                                     Fourier analysis of moment 0 map over radii
                                     smaller than the optical radius
                                     (Section 3.2.2)
  53- 56 F4.2   ---       <A2>      ? Mean first harmonic coefficient from
                                     Fourier analysis of moment 0 map over radii
                                     larger than the optical radius
                                     (Section 3.2.2)
  58- 62 F5.3   ---       Avel      ? Velocity asymmetry parameter (G2)
--------------------------------------------------------------------------------

Byte-by-byte Description of file: tablea2.dat tablea3.dat
--------------------------------------------------------------------------------
   Bytes Format Units     Label     Explanations
--------------------------------------------------------------------------------
   1-  7 A7     ---       Name      Galaxy name (NGCNNNN)
   9- 13 F5.2   [Mpc-3]   logrho    Logarithm of the environment density
                                     computed using the 10 nearest neighbours
                                     (Section 2.4)
  15- 18 F4.1   [Msun]    logMass   ? Logarithm of the stellar mass
  20- 21 I2     km/s      DVsys     Difference between the flux weighted mean
                                     systemic velocity and the systemic velocity
                                     defined as the mid-point of the spectrum at
                                     50% of the spectrum's peak height
                                     (Section 3.1.1)
  23- 24 I2     km/s      DVsysopt  ? Difference between the flux weighted mean
                                     systemic velocity from the HI spectrum and
                                     the optical velocity (Section 3.1.1)
  26- 30 F5.3   ---       Aspec     Spectrum residual (G1)
  32- 35 F4.2   ---       Aflux     Ratio of the integrated flux in the left
                                     and right halves of the spectrum divided at
                                     the systemic velocity (Section 3.1.2)
  37- 40 F4.2   ---       Apeak     ? Ratio between the left and right peaks of
                                     the spectrum (Section 3.1.3)
  42- 45 F4.2   ---       Amap      Bias corrected asymmetry parameter of
                                     integrated intensity (moment 0) map
                                     (Section 3.2.1)
  47- 50 F4.2   ---       <A1>      ? Mean first harmonic coefficient from
                                     Fourier analysis of moment 0 map over radii
                                     smaller than the optical radius
                                     (Section 3.2.2)
  52- 55 F4.2   ---       <A2>      ? Mean first harmonic coefficient from
                                     Fourier analysis of moment 0 map over radii
                                     larger than the optical radius
                                     (Section 3.2.2)
  57- 61 F5.3   ---       Avel      ? Velocity asymmetry parameter (G2)
--------------------------------------------------------------------------------

Global Notes:
Note (G1): Sum of the absolute differences between the flux in each channel of
           the spectrum and the flux in the spectral channel of the spectrum
           flipped about the systemic velocity normalized by the integrated
           flux of the spectrum (Section 3.1.4).
Note (G2): Weighted median absolute deviation of the sum of the velocity field
           and the velocity field rotated by 180deg about the galaxy centre
           scaled by the 95th percentile of the difference map between the
           original and rotated velocity fields (Section 3.2.3)
--------------------------------------------------------------------------------

History:
    From electronic version of the journal

================================================================================
(End)                                           Ana Fiallos [CDS]    11-May-2023
