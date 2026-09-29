J/ApJ/706/1364  SINS survey of high-redshift galaxies (Forster Schreiber+, 2009)
================================================================================
The SINS survey: SINFONI integral field spectroscopy of z ~ 2 star-forming
galaxies.
    Forster Schreiber N.M., Genzel R., Bouche N., Cresci G., Davies R.,
    Buschkamp P., Shapiro K., Tacconi L.J., Hicks E.K.S., Genel S.,
    Shapley A.E., Erb D.K., Steidel C.C., Lutz D., Eisenhauer F., Gillessen S.,
    Sternberg A., Renzini A., Cimatti A., Daddi E., Kurk J., Lilly S., Kong X.,
    Lehnert M.D., Nesvadba N., Verma A., McCracken H., Arimoto N., Mignoli M.,
    Onodera M.
   <Astrophys. J., 706, 1364-1428 (2009)>
   =2009ApJ...706.1364F
================================================================================
ADC_Keywords: Galaxies, spectra ; Surveys ; Spectroscopy ; Redshifts ;
              Equivalent widths ; Photometry
Keywords: galaxies: evolution - galaxies: high-redshift -
          galaxies: kinematics and dynamics - infrared: galaxies

Abstract:
    We present the Spectroscopic Imaging survey in the near-infrared
    (near-IR) with SINFONI (SINS) of high-redshift galaxies. With 80
    objects observed and 63 detected in at least one rest-frame optical
    nebular emission line, mainly H{alpha}, SINS represents the largest
    survey of spatially resolved gas kinematics, morphologies, and
    physical properties of star-forming galaxies at z~1-3. We describe the
    selection of the targets, the observations, and the data reduction. We
    then focus on the "SINS H{alpha} sample," consisting of 62
    rest-UV/optically selected sources at 1.3<z<2.6 for which we targeted
    primarily the H{alpha} and [NII] emission lines. Only ~30% of this
    sample had previous near-IR spectroscopic observations. The galaxies
    were drawn from various imaging surveys with different photometric
    criteria; as a whole, the SINS H{alpha} sample covers a reasonable
    representation of massive M_*_>~10^10^M_{sun}_ star-forming galaxies
    at z~1.5-2.5, with some bias toward bluer systems compared to pure
    K-selected samples due to the requirement of secure optical redshift.
    The H{alpha} morphologies tend to be irregular and/or clumpy. About
    one-third of the SINS H{alpha} sample galaxies are rotation-dominated
    yet turbulent disks, another one-third comprises compact and velocity
    dispersion-dominated objects, and the remaining galaxies are clear
    interacting/merging systems; the fraction of rotation-dominated
    systems increases among the more massive part of the sample.

Description:
    The observations of the SINS H{alpha} sample were carried out with
    SINFONI mounted at the Cassegrain focus of the VLT UT4 telescope.
    SINFONI consists of the near-IR cryogenic integral field spectrometer
    SPIFFI and of a curvature-sensor adaptive optics (AO) module called
    MACAO. The nominal FWHM spectral resolution for the pixel scales
    relevant to our SINS observations are as follows: R~1900, 2900, and
    4500 for J, H, and K at 125mas/pixel, and R~2700 and 5000 at
    50mas/pixel. The data were collected during 24 observing campaigns
    between 2003 March and 2008 July, as part of Guest Instrument and MPE
    guaranteed time observations. In addition, data of several GMASS
    ("Galaxy Mass Assembly ultra-deep Spectroscopic Survey"; J.D. Kurk et
    al., 2009Msngr.135...40K) targets were obtained under normal program
    allocations as part of a collaboration between the SINS and GMASS
    teams.

File Summary:
--------------------------------------------------------------------------------
 FileName   Lrecl  Records   Explanations
--------------------------------------------------------------------------------
ReadMe         80        .   This file
table1.dat    116       80   SINS survey: galaxies observed
table2.dat    125       62   Photometric properties of the SINS H{alpha}
                             sample galaxies
table3.dat    116       62   Properties derived from SED modeling of the SINS
                             H{alpha} sample galaxies
table6.dat     75       62   H{alpha} properties of the SINS H{alpha} sample
table7.dat    140       62   H{alpha} luminosities and equivalent widths of
                             the SINS H{alpha} sample
table8.dat    122       62   Star formation rate estimates of the SINS
                             H{alpha} sample
table9.dat    137       47   Dynamical properties and mass estimates of the
                             SINS H{alpha} sample
refs.dat      103       37   References
--------------------------------------------------------------------------------

See also:
   II/284  : COSMOS Multi-Wavelength Photometry Catalog (Capak+, 2007)
   VII/228 : Las Campanas Infrared Survey (Chen+, 2001-2002)
   J/ApJ/682/985 : FIREWORKS photometry of GOODS CDF-S (Wuyts+, 2008)
   J/ApJS/172/70 : zCOSMOS-bright catalog (Lilly+, 2007)
   J/A+A/462/553 : EIS: optical deep public survey (Mignano+, 2007)
   J/ApJ/647/128 : H{alpha} observations of UV-selected galaxies (Erb, 2006)
   J/A+A/437/883 : K20 survey: spectroscopic catalogue (Mignoli+, 2005)
   J/ApJ/622/772 : Redshift survey of submillimeter galaxies (Chapman+, 2005)
   J/AJ/127/2455 : Gemini Deep Deep Survey (GDDS) (Abraham+, 2004)
   J/ApJ/616/71  : Optical properties of SCUBA galaxies (Smail+, 2004)
   J/ApJ/592/728 : Lyman break galaxies at redshift z~3 (Steidel+, 2003)

Byte-by-byte Description of file: table1.dat
--------------------------------------------------------------------------------
   Bytes Format Units   Label     Explanations
--------------------------------------------------------------------------------
   1- 23  A23   ---     Name      Galaxy name
  24- 26  A3    ---   f_Name      [cehjl, ] Flag(s) on target galaxy (1)
  28- 33  F6.4  ---     zsp       Spectroscopic redshift (2)
      34  A1    ---   n_zsp       [gik] Note on redshift (3)
  36- 56  A21   ---     Class     Selection class (4)
      58  A1    ---   l_Kmag      Limit flag on Kmag
  59- 63  F5.2  mag     Kmag      ? K-band magnitude (Vega system)
      64  A1    ---   n_Kmag      [dfim] Note on Kmag (3)
  66- 93  A28   ---     Survey    Parent survey or field
  95-116  A22   ---     Ref       Reference(s) (see refs.dat file)
--------------------------------------------------------------------------------
Note (1): Flag as follows:
  c = These galaxies are known to host an AGN based on their optical (rest-UV)
      spectrum, or near-IR (rest-optical) spectrum from either previous
      long-slit observations or our SINFONI data. For all of those detected with
      SINFONI, clear signs of AGN activity are identified (from the
      [NII]/H{alpha} line ratio and/or the line widths). For K20-ID5, the
      rest-frame optical emission characteristics were argued by van Dokkum et
      al. (2005ApJ...622L..13V) to be more consistent with starburst-driven
      shock excitation rather than AGN activity.
  e = Q2346-BX404 and BX405 are an interacting pair, with angular separation of
      3.63", corresponding to a projected distance of 30.3kpc at the redshift of
      the sources.
  h = The SINFONI observations of GMASS-2113 targeted the catalog position
      reported by J. D. Kurk et al. (2009Msngr.135...40K), but a second
      component to the east was serendipitously detected with H{alpha} at the
      same redshift; the GMASS-2113W and 2113E pair has an angular separation of
      1.9", corresponding to a projected distance of 16.0kpc at the redshift of
      the pair.
  j = The SINFONI observations of SA12-8768 targeted the catalog position
      reported by Abraham et al. (2004, Cat. J/AJ/127/2455). A second component
      2.40" to the northwest was serendipitously detected with H{alpha} at the
      same redshift and at a (projected) distance of 19.8kpc.
  l = Radio galaxy, identified as H{alpha} emitter by Kurk et al.
      (2004A&A...428..793K).
Note (2): Spectroscopic redshift based on rest-frame UV emission or
     absorption lines (e.g., Ly{alpha}, interstellar absorption lines)
     obtained with optical spectroscopy, or based on H{alpha} from near-IR
     long-slit spectroscopy.
Note (3): Flag as follows:
  d = No K-band photometry was published by Erb et al. (2006ApJ...646..107E); 
      we measured the K-band magnitude from publicly available archival imaging
      obtained with the SOFI instrument at the ESO NTT as part of program ID
      071.A-0639 (PI: M. D. Lehnert).
  f = For BX 482, no K-band photometry is available. The H160-band magnitude is
      given, measured from deep HST/NICMOS imaging with the NIC2 camera through
      the F160W filter ({lambda}~1.6um; N. M. Forster Schreiber et al. 2009,
      in preparation).
  g = Daddi et al. (2004ApJ...600L.127D) reported an optical redshift of 2.25
      but noted that is was uncertain. Our SINFONI data clearly detected the
      H{alpha} and [NII] emission lines, at a redshift of 2.0343.
  i = GMASS-2113E is not included in the GMASS catalog but we cross-identified
      it in the Ks-selected FIREWORKS CDFS catalog of Wuyts et al. (2008,
      Cat. J/ApJ/682/985); the redshift listed is from our SINFONI H{alpha}
      detection, and the photometry is taken from Wuyts et al. (2008,
      cat. J/ApJ/682/985).
  k = The H{alpha} redshift from our SINFONI data is given.
  m = For these objects, the H-band magnitude is given; no K-band photometry is
      available.
Note (4): The class corresponds to the primary selection applied in the
     surveys from which our SINS targets were drawn. As explained in
     Section 2, a number of sources satisfy more than one criteria, e.g.,
     the majority of the K-selected objects also satisfy the sBzK color
     criteria. Class as follows:
   BX  = optically selected galaxy with z~2-2.5
   BM  = optically selected galaxy with z~1.5-2
   LBG = Lyman-break galaxy
   SMG = submillimeter selected galaxy
--------------------------------------------------------------------------------

Byte-by-byte Description of file: table2.dat
--------------------------------------------------------------------------------
   Bytes Format Units   Label     Explanations
--------------------------------------------------------------------------------
   1- 12  A12   ---     Name      Galaxy name
      13  A1    ---   f_Name      [a] Flag on name (1)
  15- 19  A5    ---     Ref       Photometric reference(s) (see refs.dat file)
      21  A1    ---   l_Bmag      Limit flag on Bmag
  22- 26  F5.2  mag     Bmag      ? B-band AB magnitude
  28- 31  F4.2  mag   e_Bmag      ? Bmag uncertainty
  33- 37  F5.2  mag     Gmag      ? G-band AB magnitude
  39- 42  F4.2  mag   e_Gmag      ? Gmag uncertainty
      44  A1    ---   l_Hmag      Limit flag on Hmag
  45- 49  F5.2  mag     Hmag      ? H-band magnitude (Vega system)
  51- 54  F4.2  mag   e_Hmag      ? Hmag uncertainty
  56- 60  F5.2  mag     Ksmag     ? Ks-band magnitude
  62- 65  F4.2  mag   e_Ksmag     ? Ksmag uncertainty
      67  A1    ---   l_B-Ks      Limit flag on B-K
  68- 71  F4.2  mag     B-Ks      ? Bmag-Ksmag color index
  73- 76  F4.2  mag   e_B-Ks      ? B-Ks uncertainty
  78- 81  F4.2  mag     G-Ks      ? Gmag-Ksmag color index
  83- 86  F4.2  mag   e_G-Ks      ? G-Ks uncertainty
      88  A1    ---   l_B-z       Limit flag on B-z
  89- 93  F5.2  mag     B-z       ? Bmag-z_AB_ color index
  95- 98  F4.2  mag   e_B-z       ? B-z uncertainty
      100  A1    ---   l_z-Ks      Limit flag on z-Ks
 101-104  F4.2  mag     z-Ks      ? z_AB_-Ksmag color index
 106-109  F4.2  mag   e_z-Ks      ? z-Ks uncertainty
 111-114  F4.2  mag     J-Ks      ? J_Vega_-Ksmag color index
 116-119  F4.2  mag   e_J-Ks      ? J-Ks uncertainty
 121-125  F5.3  mag     E(B-V)    E(B-V) value (2)
--------------------------------------------------------------------------------
Note (1):
  a = K-band photometry is not available from Erb et al. (2006ApJ...646..107E)
      in the SSA22a field; we used publicly available archival Ks imaging from
      SOFI at the ESO NTT, obtained under program 071.A-0639 (PI: M.D. Lehnert).
Note (2): All photometry has been corrected for Galactic extinction based
     on the dust maps and extinction curve of Schlegel et al.
     (1998ApJ...500..525S).
--------------------------------------------------------------------------------

Byte-by-byte Description of file: table3.dat
--------------------------------------------------------------------------------
   Bytes Format Units      Label   Explanations
--------------------------------------------------------------------------------
   1- 12  A12   ---        Name    Galaxy name
  14- 19  A6    ---        SFH     Best-fitting star formation history (3)
  21- 24  I4    Myr        Age     ? Age
  26- 29  I4    Myr      E_Age     ? Positive error in Age (4)
  31- 34  I4    Myr      e_Age     ? Negative error in Age (4)
  36- 38  F3.1  mag        Av      ? Extinction
  40- 42  F3.1  mag      E_Av      ? Positive error in Av (4)
  44- 46  F3.1  mag      e_Av      ? Negative error in Av (4)
  48- 52  F5.2 10+10Msun   Mass    ? Stellar mass
  54- 57  F4.2 10+10Msun E_Mass    ? Positive error in Mass (4)
  59- 62  F4.2 10+10Msun e_Mass    ? Negative error in Mass (4)
  64- 69  F6.2  mag        VMag    ? Rest-frame absolute V-band AB magnitude,
                                   uncorrected for extinction
  71- 74  F4.2  mag      E_VMag    ? Positive error in VMag (4)
  76- 79  F4.2  mag      e_VMag    ? Negative error in VMag (4)
  81- 86  F6.2  Msun/yr    SFR     ? Star formation rate
  88- 92  F5.1  Msun/yr  E_SFR     ? Positive error in SFR (4)
  94- 99  F6.2  Msun/yr  e_SFR     ? Negative error in SFR (4)
 101-105  F5.2  Gyr-1      sSFR    ? Specific SFR (i.e., the ratio of star
                                   formation rate over stellar mass)
 107-110  F4.1  Gyr-1    E_sSFR    ? Positive error in sSFR (4)
 112-116  F5.2  Gyr-1    e_sSFR    ? Negative error in sSFR (4)
--------------------------------------------------------------------------------
Note (3): The best-fitting star formation history as follows:
  CSF    = constant star formation rate;
  tau300 = exponentially declining star formation rate with e-folding timescale
           of {tau}=300Myr.
Note (4): The formal (random) fitting uncertainties are given, derived from
     the 68% confidence intervals based on 200 Monte Carlo simulations for
     the default set of Bruzual & Charlot (2003MNRAS.344.1000B) models with
     solar metallicity, the Chabrier (2003PASP..115..763C) IMF, and the
     Calzetti et al. (2000ApJ...533..682C) reddening law; systematic
     uncertainties (from SED modeling assumptions) are estimated to be
     typically +/-30% for the stellar masses, +/-0.3mag for the extinctions,
     and factors of ~2-3 for the ages as well as for the absolute and
     specific star formation rates (see Section 3 and Appendix A).
--------------------------------------------------------------------------------

Byte-by-byte Description of file: table6.dat
--------------------------------------------------------------------------------
   Bytes Format Units      Label Explanations
--------------------------------------------------------------------------------
   1- 12  A12   ---        Name  Galaxy name
  14- 17  F4.2  arcsec     Rap   ? Radius of the circular aperture (5)
  19- 24  F6.4  ---        zHa   Redshift (6)
      25  A1    ---      f_zHa   [)] ): vacuum (6)
      27  A1    ---      l_FHa   Limit flag on FHa
  28- 31  F4.1 10-20W/m2   FHa   H{alpha} flux in 10^-17^erg/s/cm^2^ (6)
  33- 35  F3.1 10-20W/m2 E_FHa   ? Positive error on FHa
  37- 39  F3.1 10-20W/m2 e_FHa   ? Negative error on FHa
  41- 43  I3    km/s       Sig   ? Velocity dispersion (6)
  45- 48  I4    km/s     E_Sig   ? Positive error on Sig
  50- 51  I2    km/s     e_Sig   ? Negative error on Sig
      53  A1    ---      l_r1/2  Limit flag on r1/2
  54- 56  F3.1  kpc        r1/2  ? Intrinsic H{alpha} half-light radius (7)
  58- 60  F3.1  kpc      e_r1/2  ? r1/2 uncertainty
  62- 65  F4.1  kpc        FWHM  ? Intrinsic FWHM size along the major axis (8)
  67- 69  F3.1  kpc      e_FWHM  ? FWHM uncertainty
      71  A1    ---      l_FBB   Limit flag on FBB
  72- 75  F4.2  ---        FBB   ? Fractional contribution of the H{alpha}
                                 emission line to the broadband flux density (9)
--------------------------------------------------------------------------------
Note (5): Used to extract the spatially integrated spectrum of each source.
Note (6): Redshift (vacuum), flux, and velocity dispersion of H{alpha}
     derived by fitting a Gaussian profile to the line emission in the
     spatially integrated spectrum. The velocity dispersion is corrected
     for spectral instrumental resolution. The uncertainties correspond to
     the formal 68% confidence intervals derived from 100 Monte Carlo
     simulations. For undetected sources, the optical redshift is given
     (parenthesis flag) and the 3{sigma} upper limit on the flux is given.
     The limits are computed based on the noise spectrum within an aperture
     of radius 1", assuming H{alpha} at the wavelength expected for the
     optical redshift and an intrinsic width corresponding
     {sigma}_int_=130km/s, the average for the detected sources.
Note (7): Intrinsic (corrected for spatial resolution) H{alpha} half-light
     radius derived from curve-of-growth analysis from spectra integrated
     in circular apertures of increasing radius. The measurement errors
     account for typical seeing variations during the observations and
     uncertainties from the PSF shape.
Note (8): Intrinsic FWHM size along the major axis, derived from fitting a
     1D Gaussian to the H{alpha} light profile taken in 6-pixels-wide
     circular apertures along the major axis of each galaxy. For some of
     the sources with faintest H{alpha} surface brightness, major axis
     profiles are too unreliable for an FWHM determination. The measurement
     errors account for typical seeing variations during the observations
     and uncertainties from the PSF shape.
Note (9): Fractional contribution of the H{alpha} emission line to the
     observed broadband flux density (K for sources at 2<z<2.6 and H for
     those at 1.3<z<2).
--------------------------------------------------------------------------------

Byte-by-byte Description of file: table7.dat
--------------------------------------------------------------------------------
   Bytes Format Units    Label Explanations
--------------------------------------------------------------------------------
   1- 12  A12   ---      Name  Galaxy name
      14  A1    ---    l_Lobs  Limit flag on lobs
  15- 19  F5.2  10+35W   Lobs  Observed H{alpha} line luminosity (10)
  21- 24  F4.2  10+35W E_Lobs  ? Positive error on Lobs
  26- 29  F4.2  10+35W e_Lobs  ? Negative error on Lobs
      31  A1    ---    l_L0    Limit flag on L0
  32- 36  F5.2  10+35W   L0    ? Intrinsic H{alpha} line luminosity (10)
  38- 41  F4.2  10+35W E_L0    ? Positive error on L0
  43- 46  F4.2  10+35W e_L0    ? Negative error on L0
      48  A1    ---    l_L00   Limit flag on L00
  49- 54  F6.2  10+35W   L00   ? Intrinsic H{alpha} line luminosity
                                 with attenuation (10)
  56- 60  F5.1  10+35W E_L00   ? Positive error on L00
  62- 66  F5.1  10+35W e_L00   ? Negative error on L00
  68- 73  F6.2  10+35W   L0p   ? Predicted intrinsic H{alpha} line luminosity 
                                 from best-fit parameters (11)
  75- 80  F6.2  10+35W E_L0p   ? Positive error on L0p
  82- 86  F5.2  10+35W e_L0p   ? Negative error on L0p
      88  A1    ---    l_Wsin  Limit flag on Wsin
  89- 92  I4    0.1nm    Wsin  ? SINFONI H{alpha} equivalent width (12)
  94- 96  I3    0.1nm  E_Wsin  ? Positive error on Wsin
  98-100  I3    0.1nm  e_Wsin  ? Negative error on Wsin
     102  A1    ---    l_Wbb   Limit flag on Wbb
 103-106  I4    0.1nm    Wbb   ? H{alpha} equivalent width from the broadband
                               magnitudes (13)
 108-110  I3    0.1nm  E_Wbb   ? Positive error on Wbb
 112-114  I3    0.1nm  e_Wbb   ? Negative error on Wbb
     116  A1    ---    l_W0bb  Limit flag on W0bb
 117-120  I4    0.1nm    W0bb  ? H{alpha} equivalent width from the broadband
                                magnitudes corrected for extra attenuation (13)
 122-124  I3    0.1nm  E_W0bb  ? Positive error on W0bb
 126-128  I3    0.1nm  e_W0bb  ? Negative error on W0bb
 130-132  I3    0.1nm    Wp    ? Predicted H{alpha} equivalent width (14)
 134-136  I3    0.1nm  E_Wp    ? Positive error on Wp
 138-140  I3    0.1nm  e_Wp    ? Negative error on Wp
--------------------------------------------------------------------------------
Note (10): Observed and intrinsic H{alpha} line luminosities in 10^42^erg/s.
     L^0^(H{alpha}) is computed assuming the best-fit extinction A_V,SED_
     from the SED modeling and the Calzetti et al. (2000ApJ...533..682C)
     reddening law, and L^00^(H{alpha}) is computed assuming extra
     attenuation toward the HII regions with A_V,neb_=A_V,SED_/0.44.
     Uncertainties on the luminosities include the formal 1{sigma}
     uncertainties of the H{alpha} line fluxes, as well as those of A_V_
     from the SED modeling for the intrinsic luminosities; 3{sigma} upper
     limits are given for sources undetected in H{alpha}.
Note (11): Predicted intrinsic H{alpha} line luminosities computed from
     Bruzual & Charlot (2003MNRAS.344.1000B) models for the best-fit
     parameters of each galaxy (Table 3). Uncertainties are computed based
     on those of the best-fit properties derived from the SED modeling.
Note (12): H{alpha} equivalent widths from the H{alpha} line fluxes and
     estimates of the underlying continuum flux density from our SINFONI
     data. Uncertainties account for the formal 1{sigma} uncertainties on
     the H{alpha} line fluxes and on the continua; 3{sigma} upper limits
     are given for sources undetected in H{alpha}, and 3{sigma} lower
     limits are given for those undetected in the continuum.
Note (13): H{alpha} equivalent widths derived from our H{alpha} line flux
     measurements and estimates of the underlying continuum obtained from
     the broadband magnitudes (K band for sources at 2<z<2.6 and H for
     those at 1.3<z<2) after correcting for the contribution by the
     H{alpha} line (Table 6). The W^rest^_BB_(H{alpha}) are computed from
     the observed H{alpha} fluxes and broadband magnitudes, equivalent to
     assuming the same extinction applies to the HII regions and the stars.
     The W^rest,00^_BB_(H{alpha}) are corrected for extra attenuation
     toward the HII regions, using the best-fit extinction A_V,SED_ from
     the SED modeling, the Calzetti et al. (2000ApJ...533..682C) reddening
     law, and applying A_V,neb_=A_V,SED_/0.44. Uncertainties account for
     the formal 1{sigma} uncertainties on the H{alpha} line fluxes and on
     broadband magnitudes, as well as for the best-fit A_V_ from the SED
     modeling for W^rest,00^_BB_(H{alpha}); 3{sigma} upper limits are given
     for sources undetected in H{alpha}.
Note (14): Predicted H{alpha} equivalent widths computed from Bruzual &
     Charlot (2003MNRAS.344.1000B) models for the best-fit parameters of
     each galaxy (Table 3). Uncertainties are computed based on those of
     the best-fit properties derived from the SED modeling.
--------------------------------------------------------------------------------

Byte-by-byte Description of file: table8.dat
--------------------------------------------------------------------------------
   Bytes Format Units      Label Explanations
--------------------------------------------------------------------------------
   1- 12  A12   ---        Name  Source name
  14- 19  F6.2  Msun/yr    SFRi  ? Intrinsic star formation rate from SED
  21- 25  F5.1  Msun/yr  E_SFRi  ? Positive error on SFR (15)
  27- 32  F6.2  Msun/yr  e_SFRi  ? Negative error on SFR (15)
      34  A1    ---      l_SFR0  Limit flag on SFR0
  35- 39  F5.1  Msun/yr    SFR0  ? Intrinsic star formation rate derived from
                                 the H{alpha} line luminosity (16)
  41- 44  F4.1  Msun/yr  E_SFR0  ? Positive error in SFR0
  46- 49  F4.1  Msun/yr  e_SFR0  ? Negative error in SFR0
      51  A1    ---      l_SFR00 Limit flag on SFR00
  52- 57  F6.1  Msun/yr    SFR00 ? Intrinsic star formation rate derived from
                                 the H{alpha} line luminosity + correction (16)
  59- 63  F5.1  Msun/yr  E_SFR00 ? Positive error in SFR00
  65- 69  F5.1  Msun/yr  e_SFR00 ? Negative error in SFR00
      71  A1    ---      l_LoUV  Limit flag on LoUV
  72- 75  F4.1 10+21W/Hz   LoUV  ? Observed UV luminosity density (17)
  77- 79  F3.1 10+21W/Hz e_LoUV  ? LoUV uncertainty (17)
      81  A1    ---      l_L0UV  Limit flag on L0UV
  82- 87  F6.1 10+21W/Hz   L0UV  ? Intrinsic UV luminosity (17)
  89- 93  F5.1 10+21W/Hz E_L0UV  ? Positive error in L0UV
  95- 99  F5.1 10+21W/Hz e_L0UV  ? Negative error in L0UV
     101  A1    ---      l_SFRuv Limit flag on SFRuv
 102-108  F7.2  Msun/yr    SFRuv ? Intrinsic star formation rate derived from
                                 the rest-frame UV luminosity density (18)
 110-115  F6.2  Msun/yr  E_SFRuv ? Positive error in SFRuv
 117-122  F6.2  Msun/yr  e_SFRuv ? Negative error in SFRuv
--------------------------------------------------------------------------------
Note (15): Intrinsic star formation rate corresponding 68% confidence
     intervals derived from the SED modeling (Table 3).
Note (16): Intrinsic star formation rate derived from the H{alpha} line
     luminosity (see Table 7), applying the conversion of Kennicutt
     (1998ApJ...498..541K) adjusted to a Chabrier (2003PASP..115..763C)
     IMF. The SFR^0^(H{alpha}) are computed assuming the best-fit
     extinction A_V,SED_ from the SED modeling and the Calzetti et al.
     (2000ApJ...533..682C) reddening law, and the SFR^00^(H{alpha}) are
     computed assuming extra attenuation toward the HII regions with
     A_V,neb_=A_V,SED_/0.44. Uncertainties are propagated from those of the
     luminosities; 3{sigma} upper limits are given for sources undetected
     in H{alpha}.
Note (17): Observed and intrinsic rest-frame UV luminosity densities in
     10^28^erg/s/Hz, derived from either the B- or G-band magnitude (see
     Table 2) as described in Section 8.1. The extinction correction uses
     the best-fit extinction A_V,SED_ from the SED modeling and is computed
     for a rest-frame wavelength of 1500{AA} assuming the Calzetti et al.
     (2000ApJ...533..682C) reddening law. Uncertainties are computed from
     those of the observed magnitudes, as well as of the best-fit A_V_ from
     the SED modeling for the intrinsic luminosity; the 3{sigma} upper
     limit is given for SA15-7353, undetected in the B band.
Note (18): Intrinsic star formation rate derived from the rest-frame UV
     luminosity density, applying the conversion of Kennicutt
     (1998ApJ...498..541K) adjusted to a Chabrier (2003PASP..115..763C) IMF
     and corrected for extinction using the best-fit extinction A_V,SED_
     from the SED modeling as for the intrinsic rest-frame UV luminosity.
     Uncertainties are propagated from those of the luminosities; the
     3{sigma} upper limit is given for SA15-7353, undetected in the B band.
--------------------------------------------------------------------------------

Byte-by-byte Description of file: table9.dat
--------------------------------------------------------------------------------
   Bytes Format Units      Label    Explanations
--------------------------------------------------------------------------------
   1- 12  A12   ---        Name     Source name
      13  A1    ---      f_Name     [i] Flag on name (1)
  15- 37  A23   ---        Met      Method used to derive the circular velocity
                                    Vel and dynamical mass Mdyn (2)
  39- 44  A6    ---        Kin      Kinemetry class (Disk or Merger) (3)
  46- 48  I3    km/s       Vel/2    Half the observed velocity ({nu}_obs_/2) (4)
  50- 51  I2    km/s     e_Vel/2    Vel/2 uncertainty
  53- 56  F4.2  ---        V/2sig   Rotation- or dispersion-dominated galaxy (5)
  58- 61  F4.2  ---      E_V/2sig   Positive error on V/2sig
  63- 66  F4.2  ---      e_V/2sig   Negative error on V/2sig
  68- 70  F3.1  ---        Vrot/sig ? Ratio of circular velocity and velocity
                                    dispersion (6)
  72- 74  F3.1  ---      e_Vrot/sig ? Vrot/sig uncertainty
      76  A1    ---      l_Vel      Limit flag on Vel
  77- 79  I3    km/s       Vel      Disk circular velocity ({nu}_d_) (7)
  81- 83  I3    km/s     E_Vel      ? Positive error on Vel
  85- 87  I3    km/s     e_Vel      ? Negative error on vel
  89- 92  F4.2 10+10Msun   M0       ? Total gas mass from SFR0 (8)
  94- 97  F4.2 10+10Msun E_M0       ? Positive error on M0
  99-102  F4.2 10+10Msun e_M0       ? Negative error on M0
 104-108  F5.2 10+10Msun   M00      ? Total gas mass from SFR00 (8)
 110-113  F4.2 10+10Msun E_M00      ? Positive error on M00
 115-118  F4.2 10+10Msun e_M00      ? Negative error on M00
     120  A1    ---      l_Mdyn     Limit flag on Mdyn
 121-125  F5.2 10+10Msun   Mdyn     Total dynamical mass
 127-131  F5.2 10+10Msun E_Mdyn     ? Positive error on Mdyn
 133-137  F5.2 10+10Msun e_Mdyn     ? Negative error on Mdyn
--------------------------------------------------------------------------------
Note (1):
   i = This source is classified as (minor) merger from its H{alpha} kinematics,
       and a small faint close companion is also seen in H{alpha} and continuum
       emission; the kinematic properties reported here are for the larger main
       disk component of the system.
Note (2): Method used to derive the circular velocity and dynamical mass
          estimates as explained in Section 9.5. In brief, methods as follows:
  Kinematic modeling = from full kinematic modeling of the velocity field and
                       velocity dispersion map (Genzel et al.
                       2008ApJ...687...59G; Cresci et al. 2009ApJ...697..115C).
  Velocity gradient+width = for sources with rotation-dominated kinematics, the
                            values adopted are averages obtained from estimates
                            based on the observed velocity gradient and on the
                            integrated velocity line width in the framework of
                            rotating disks.
  Velocity width     = for sources with dispersion-dominated kinematics, we used
                       virial isotropic estimates.
     Galaxies that are undetected in our SINFONI data or for which we
     cannot establish whether their kinematics are rotation- or
     dispersion-dominated due to poorer S/N are excluded.
Note (3): Classification based on quantitative analysis of the H{alpha}
     kinematics through kinemetry (see Shapiro et al. 2008ApJ...682..231S,
     and Section 9.1).
Note (4): The {nu}_obs_ is the full observed difference between the maximum
     and minimum relative velocities from the H{alpha} kinematics across
     the source, uncorrected for inclination.
Note (5): Ratio of half the observed velocity gradient to the
     source-integrated velocity dispersion (from Table 6), derived from the
     H{alpha} kinematics and uncorrected for inclination. We treated
     galaxies with {nu}_obs_/(2{sigma}_int_)>0.4 as rotation-dominated and
     those with {nu}_obs_/(2{sigma}_int_)<0.4 as dispersion-dominated (see
     Section 9).
Note (6): Ratio of inclination-corrected circular velocity and intrinsic
     local velocity dispersion for the disks with kinematic modeling,
     corrected for inclination (Genzel et al. 2008ApJ...687...59G; Cresci
     et al. 2009ApJ...697..115C).
Note (7): Disk circular velocity (or equivalent (3{sigma}_int_)^0.5^ for
     objects with dispersion-dominated H{alpha} kinematics) derived
     according to the method given in the second column and described in
     Section 9.5.
Note (8): Total gas masses estimated from the H{alpha} star formation rate
     surface densities (within the H{alpha} half-light radius
     r_1/2_(H{alpha) from Table 6) through the Schmidt-Kennicutt relation
     as derived by Bouche et al. (2007ApJ...671..303B). Two estimates are
     listed, depending on the extinction correction applied to the H{alpha}
     line luminosities: M^0^_gas_ uses SFR^0^(H{alpha}) derived using the
     best-fit extinction A_V,SED_ from the SED modeling (Table 3) and the
     Calzetti et al. (2000ApJ...533..682C) reddening law, and M^00^_gas_
     uses SFR^00^(H{alpha}) assuming extra attenuation toward the HII
     regions with A_V,neb_=A_V,SED_/0.44.
--------------------------------------------------------------------------------

Byte-by-byte Description of file: refs.dat
--------------------------------------------------------------------------------
   Bytes Format Units   Label     Explanations
--------------------------------------------------------------------------------
   1-  2  I2    ---     Ref       Reference number
   4- 22  A19   ---     BibCode   Bibcode
  24- 53  A30   ---     Aut       First author's name
  55-103  A49   ---     Comm      Comment
--------------------------------------------------------------------------------

History:
    From electronic version of the journal

================================================================================
(End)                                     Emmanuelle Perret [CDS]    16-Dec-2011
