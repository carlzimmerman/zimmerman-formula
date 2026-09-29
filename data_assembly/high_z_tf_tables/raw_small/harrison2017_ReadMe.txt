J/MNRAS/467/1965     KMOS Redshift One Spectroscopic Survey    (Harrison+, 2017)
================================================================================
The KMOS Redshift One Spectroscopic Survey (KROSS):
rotational velocities and angular momentum of z ~= 0.9 galaxies.
    Harrison C.M., Johnson H.L., Swinbank A.M., Stott J.P., Bower R.G.,
    Smail I., Tiley A.L., Bunker A.J., Cirasuolo M., Sobral D., Sharples R.M.,
    Best P., Bureau M., Jarvis M.J., Magdis G.
   <Mon. Not. R. Astron. Soc., 467, 1965-1983 (2017)>
   =2017MNRAS.467.1965H    (SIMBAD/NED BibCode)
================================================================================
ADC_Keywords: Galaxy catalogs ; Redshifts
Keywords: galaxies: evolution - galaxies: kinematics and dynamics

Abstract:
    We present dynamical measurements for 586 H{alpha}-detected
    star-forming galaxies from the KMOS (K-band Multi-Object Spectrograph)
    Redshift One Spectroscopic Survey (KROSS). The sample represents
    typical star-forming galaxies at this redshift (z=0.6-1.0), with a
    median star formation rate of ~=7M_{sun}_/yr and a stellar mass range
    of log(M*_[M_{sun}_])~9-11. We find that the rotation
    velocity-stellar mass relationship (the inverse of the Tully-Fisher
    relationship) for our rotationally dominated sources
    (v_C_/{sigma}_0_>1) has a consistent slope and normalization as that
    observed for z=0 discs. In contrast, the specific angular momentum
    (j*; angular momentum divided by stellar mass) is ~=0.2-0.3dex lower
    on average compared to z=0 discs. The specific angular momentum scales
    as j_s_{prop.to}M*^0.6+/-0.2^, consistent with that expected for dark
    matter (i.e. j_DM_{prop.to} M_DM_^2/3^). We find that z~=0.9
    star-forming galaxies have decreasing specific angular momentum with
    increasing Sersic index. Visually, the sources with the highest
    specific angular momentum, for a given mass, have the most
    disc-dominated morphologies. This implies that an angular
    momentum-mass-morphology relationship, similar to that observed in
    local massive galaxies, is already in place by z~=1.

Description:
    KROSS is an IFS survey of 795 z=0.6-1.0 typical star-forming galaxies
    designed to spatially resolve the H{alpha} emission-line kinematics.
    The targets were selected from four extragalactic deep fields that are
    covered by a wide range of archival multi-wavelength photometric and
    spectroscopic data.

    We present new measurements and results based on IFU data of ~600
    H{alpha}-detected z=0.6-1.0 star-forming galaxies that were observed
    as part of KROSS (Stott et al. 2016MNRAS.457.1888S). These sources are
    representative of log(M*[M_{sun}_])~=9-11 star-forming galaxies at
    this redshift. Using a combination of broad-band imaging and our IFU
    data we have made measurements of inclination angles, half-light
    radii, morphological and kinematic position angles, rotational
    velocities, intrinsic velocity dispersions and specific angular
    momentum.

File Summary:
--------------------------------------------------------------------------------
 FileName      Lrecl  Records   Explanations
--------------------------------------------------------------------------------
ReadMe            80        .   This file
krossv2.dat      468      586   KROSS V2 catalog
--------------------------------------------------------------------------------

See also:
 J/ApJS/203/24 : Structural parameters of CANDELS galaxies (van der Wel+, 2012)
 http://astro.dur.ac.uk/KROSS : KROSS Home Page

Byte-by-byte Description of file: krossv2.dat
--------------------------------------------------------------------------------
   Bytes Format Units     Label     Explanations
--------------------------------------------------------------------------------
   1-  3  I3    ---       KID       KROSS ID (KID)
   5- 26  A22   ---       Name      Object name (NAME)
  28- 37  F10.6 deg       RAdeg     Right ascension (J2000) (RA)
  39- 48  F10.6 deg       DEdeg     Declination (J2000) (DEC)
  50- 57  F8.4  mag       Kmag      K-band magnitude (K_AB)
  59- 66  F8.4  mag       rmag      r-band magnitude (R_AB)
  68- 75  F8.4  mag       zmag      z-band magnitude (Z_AB)
  77- 82  F6.2  mag       HMAG      Absolute H-band magnitude (MH)
  84-105 E22.15 Msun      Mass      Stellar mass, scaled from HMAG with a fixed
                                     mass-to-light ratio (MASS)
 107-114  F8.6  ---       VDW12n    Sersic index n from van der Wel et al.
                                    (2012, Cat. J/ApJS/203/24) (VDW12_N)
 116-117  A2    ---       im-Type   [HIKz' ] Band of broad-band image used in
                                     the analyses (IM_TYPE)
     119  I1    ---       Qual      [1/4] Quality flag for the data
                                     (QUALITY_FLAG) (1)
 121-130  F10.6 deg       PAim      Positional angle of the broad-band image
                                    (PA_IM)
 132-140  F9.6  kpc       Rim       Deconvolved continuum half-light radii,
                                    R1/2, from the image (R_IM)
 142-149  F8.6  kpc     e_Rim       rms uncertainty on Rim (R_IM_ERR)
 151-153  F3.1  ---     f_Rim       [0/1] Note on Rim (R_FLAG) (2)
 155-162  F8.6  ---       b/a       The observed axis ratio b/a from the
                                     broad-band image (B_O_A)
 164-171  F8.5  deg       thetaim   The inferred inclination angle, {theta}im,
                                     with error. If thetaim<25 then excluded
                                     from the analyses(THETA_IM)
 173-180  F8.5  deg     e_thetaim   rms uncertainty on thetaim (THETA_IM_ERR)
     182  I1    ---     f_thetaim   [0/1] If =1 then the inclination angle was
                                     fixed to 53+/-18{deg} (THETA_FLAG)
 184-191  F8.6  ---       z         Redshift from H{alpha} (Z)
 193-214 E22.15 mW/m2     FHa       Observed aperture H{alpha} flux (F_HA)
 216-237 E22.15 10-7W     LHa       Observed H{alpha} luminosity with a factor
                                     of x1.5 aperture correction applied(L_HA)
 239-247  F9.6  Msun/yr   SFR       Inferred star formation rate from H{alpha}
                                     luminosity and applying an Av correction
                                     (SFR)
 249-256  F8.4  km/s      sigmaTot  Velocity dispersion from the
                                     galaxy-integrated (aperture) spectrum
                                     (SIGMA_TOT)
     258  I1    ---       fAGN      [0/1] If =1 AGN emission affecting the
                                     emission-line properties and are excluded
                                     from the final analyses (AGN_FLAG)
     260  I1    ---       fIRR      [0/1] if =1 unphysical measurements for the
                                     rotational velocities and/or the
                                     half-light radii (IRR_FLAG)
 262-271  F10.6 deg       PAvel     Position angle of the major kinematic axis
                                     (VEL_PA)
 273-281  F9.5  km/s      V2.2obs   Observed velocity measured at 1.3 R1/2
                                     (i.e. ~=2.2 RD), v2.2 (V22_OBS)
 283-292  F10.5 km/s      V2.2      Intrinsic v2.2 after inclination and
                                     beam-smearing corrections (V22)
 294-302  F9.5  km/s      VCobs     Observed velocity measured at 2 R1/2
                                     (i.e. ~=3.4 RD)(VC_OBS)
 304-313  F10.5 km/s      VC        Intrinsic vC after inclination and
                                     beam-smearing corrections (VC)
 315-324  F10.5 km/s    e_VC        Error on VC (lower value) (VC_ERR_L)
 326-335  F10.5 km/s    E_VC        Error on VC (upper value) (VC_ERR_H)
     337  I1    ---       fEXTRAP   [0/2] If =1, vC extrapolated >2 pixels
                                     beyond the extent of the data,
                                     if =2 then vC was estimated by scaling
                                     sigmaTot (EXTRAP_FLAG)
 339-341  A3    ---       KinType   Kinematic classification (KIN_TYPE) (3)
     343  A1    ---     l_JS        [-] limit flag on JS
 344-350  F7.2 km/s.kpc   JS        Specific angular momentum, js (JS)
 352-358  F7.2 km/s.kpc e_JS         Error on JS (lower value) (JS_ERR_LOW)
 360-367  F8.2 km/s.kpc E_JS         Error on JS (lower value) (JS_ERR_HIGH)
 369-375  F7.2 km/s.kpc   JN         Specific angular momentum, jn,
                                      using individual n values (JN)
 377-384  F8.3  ---       sigma0Obs  Observed corrected velocity dispersion
                                      (SIGMA0_OBS)
 386-393  F8.3  ---     e_sigma0Obs  ?=-999 rms uncertainty on sigma0Obs
                                      (SIGMA0_OBS_ERR)
 395-402  F8.3  ---       sigma0     Beam smaearing corrected velocity
                                      dispersion (SIGMA0)
 404-411  F8.3  ---     e_sigma0     ?=-999 rms uncertainty on sigma0
                                      (SIGMA0_ERR)
     413  A1    ---     f_sigma0     [MOX] Flag on sigma0 (SIGMA0_FLAG) (4)
 415-424  F10.5 ---       RD/RPSF    Ratio between the disk radius (in arcsec)
                                      and half of the seeing FWHM (RD_RPSF)
 426-435  F10.5 ---     e_RD/RPSF    ?=-999 rms uncertainty on RD/RPSF
                                      (RD_RPSF_ERR)
 437-446  F10.5 ---       Qg         Global Toomre parameter (Q_g)
 448-457  F10.5 ---     E_Qg         ?=-999 Error on Qg (upper value)
                                      (Q_g_ERR_HIGH)
 459-468  F10.5 ---     e_Qg         ?=-999 Error on Qg (lower value)
                                      (Q_g_ERR_LOW)
--------------------------------------------------------------------------------
Note (1): Quality flag as follows:
   1 = H{alpha}-detected, spatially resolved and both thetaim and R1/2 were
        measured from the broad-band
   2 = H{alpha}-detected and spatially resolved but thetaim was fixed
        (see THETA_FLAG) and/or R1/2 was estimated from the kinematic
        (see R_FLAG)
   3 = H{alpha} detected and resolved in the IFU data but only an upper limit
        on R1/2
   4 = H{alpha} detected but unresolved in the IFU data
Note (2): If =1 then R1/2 is an upper limit, if =0.5 then R1/2 was estimated
   using a fit to the kinematic data.
Note (3): Kinematic classification as follows:
    RT+ = 'gold' rotationally dominated
    RT  = rotationally dominated
    DN  = dispersion dominated
    X   = IFU data are spatially unresolved
Note (4): Flag on sigma0 as follows:
    M = dispersion measured from the median of all available pixels
    O = dispersion measured in the outskirts of the disk
    X = not explained in the paper
--------------------------------------------------------------------------------

History:
    Copied at http://astro.dur.ac.uk/KROSS

================================================================================
(End)                                      Patricia Vannier [CDS]    18-Nov-2019
