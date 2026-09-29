J/MNRAS/482/2166   Tully-Fisher relation across 8Gyr since z~1   (Tiley+, 2019)
================================================================================
KROSS-SAMI: a direct IFS comparison of the Tully-Fisher relation across 8 Gyr
since z~=1.
    Tiley A.L., Bureau M., Cortese L., Harrison C.M., Johnson H.L., Stott J.P.,
    Swinbank A.M., Smail I., Sobral D., Bunker A.J., Glazebrook K., Bower R.G.,
    Obreschkow D., Bryant J.J., Jarvis M.J., Bland-Hawthorn J., Magdis G.,
    Medling A.M., Sweet S.M., Tonini C., Turner O.J., Sharples R.M.,
    Croom S.M., Goodwin M., Konstantopoulos I.S., Lorente N.P.F.,
    Lawrence J.S., Mould J., Owers M.S., Richards S.N.
   <Mon. Not. R. Astron. Soc., 482, 2166-2188 (2019)>
   =2019MNRAS.482.2166T    (SIMBAD/NED BibCode)
================================================================================
ADC_Keywords: Galaxies ; Rotational velocities ; Redshifts
Keywords: galaxies: evolution - galaxies: general -
          galaxies: kinematics and dynamics -
          galaxies: star formation

Abstract:
    We construct Tully-Fisher relations (TFRs), from large samples of
    galaxies with spatially resolved H{alpha} emission maps from the
    K-band Multi-Object Spectrograph (KMOS) Redshift One Spectroscopic
    Survey (KROSS) at z~1. We compare these to data from the
    Sydney-Australian-Astronomical-Observatory Multi-object Integral-Field
    Spectrograph (SAMI) Galaxy Survey at z~0. We stringently match the
    data quality of the latter to the former, and apply identical analysis
    methods and sub-sample selection criteria to both to conduct a direct
    comparison of the absolute K-band magnitude and stellar mass TFRs at
    z~1 and 0. We find that matching the quality of the SAMI data to that
    of KROSS results in TFRs that differ significantly in slope,
    zero-point, and (sometimes) scatter in comparison to the corresponding
    original SAMI relations. These differences are in every case as large
    as or larger than the differences between the KROSS z~1 and matched
    SAMI z~0 relations. Accounting for these differences, we compare the
    TFRs at z~1 and 0. For disc-like, star-forming galaxies we find no
    significant difference in the TFR zero-points between the two epochs.
    This suggests the growth of stellar mass and dark matter in these
    types of galaxies is intimately linked over this ~8Gyr period.

Description:
    The z~1 TFRs presented in this work are constructed from samples drawn
    from KROSS. For detailed descriptions of the KROSS sample selection,
    observations, and data reduction, see Stott et al.
    (2016MNRAS.457.1888S). KROSS comprises integral field unit (IFU)
    observations of 795 galaxies at 0.6~<z~<1, that target H{alpha},
    [NII]6548, and [NII]6583 emission from warm ionized gas that falls in
    the YJ band (~1.02-1.36{mu}m) of KMOS. All KROSS observations were
    carried out with KMOS on UT1 of the Very Large Telescope, Cerro
    Paranal, Chile. The core KROSS observations were undertaken during ESO
    observing periods P92-P95 (with programme IDs 092.B-0538, 093.B-0106,
    094.B-0061, and 095.B-0035).
    The z~0 TFRs presented in this work are constructed from samples drawn
    from the SAMI Galaxy Survey (Bryant et al. 2015MNRAS.447.2857B). Using
    the SAMI spectrograph (Croom et al. 2012MNRAS.421..872C) on the 3.9-m
    Anglo-Australian Telescope at Siding Spring Observatory. The SAMI
    Galaxy Survey has observed the spatially resolved stellar and gas
    kinematics of ~3000 galaxies in the redshift range 0.004<z<0.095, over
    a large range of local environments. This work uses SAMI observations
    of 824 galaxies with mapped kinematics out to or beyond one effective
    radius.
    In this work, we take steps to remove the potential for systematic
    biases between TFRs constructed at different redshifts by implementing
    a novel data 'matching' process, applied to the SAMI data to transform
    them so that they match the quality of KROSS observations. As stated
    in Introduction, we refer to these transformed data as the matched
    SAMI sample. Table A1 presents examples of the derived values from the
    KROSS, original SAMI, and matched SAMI rot-dom and disky galaxy
    sub-samples, that were used to construct the TFRs.

File Summary:
--------------------------------------------------------------------------------
 FileName      Lrecl  Records   Explanations
--------------------------------------------------------------------------------
ReadMe            80        .   This file
tablea1.dat       89      754   The derived properties used to construct the
                                KROSS, original SAMI, and matched SAMI TFRs
                                for the rot-dom and disky sub-samples
--------------------------------------------------------------------------------

See also:
    J/MNRAS/467/1965 : KMOS Redshift One Spectroscopic Survey (Harrison+, 2017)
    J/MNRAS/474/5076 : KMOS Redshift One Spectroscopic Survey (Johnson+, 2018)

Byte-by-byte Description of file: tablea1.dat
--------------------------------------------------------------------------------
   Bytes Format Units    Label    Explanations
--------------------------------------------------------------------------------
   1- 13  A13   ---      Survey   The source survey for the galaxy
                                   (KROSS, SAMI_matched or SAMI_original)
  15- 20  I6    ---      ID       The object ID for the corresponding survey
                                   for KROSS survey, KROSS NNNNNN in Simbad
      22  I1    ---    f_ID       [0/1] Flag indicating to which sub-sample(s)
                                   the galaxy belongs (1)
  24- 40 F17.15 [km/s]   logv2.2  Intrinsic rotation velocity (2)
  42- 62 E21.19 [km/s] e_logv2.2  Error on logv2.2 (2)
  64- 71  F8.5  [Msun]   logMstar The stellar mass derived via SED fitting with
                                   LEPHARE (3)
  73- 75  F3.1  [Msun] e_logMstar Error on logMstar (3)
  77- 83  F7.3  mag      KMAG     Absolute K-band magnitude in the Vega system
  85- 89  F5.3  mag    e_KMAG     Error on KMAG
--------------------------------------------------------------------------------
Note (1): Flag as follows:
   0 = the galaxy only belongs to the rot-dom sub-sample
   1 = the galaxy belongs to both the rot-dom and disky sub-samples
Note (2): For a unique measure of the intrinsic circular velocity for each
          galaxy, we adopt the v_2.2_ parameter of Harrison et al.
          (2017MNRAS.467.1965H, Cat. J/MNRAS/467/1965) derived from v_2.2,obs_,
          the line-of-sight velocity measured from the best-fitting model to the
          rotation curve at 1.3 times the effective (half-light) radius r_e_
          (convolved to the 'native' seeing of the velocity maps). This radius
          corresponds to 2.2 times the scale length of a purely exponential
          disc.
          The KROSS measurements of logv2.2 (and e_logv2.2) are taken directly
          from Harrison et al. (2017MNRAS.467.1965H, Cat. J/MNRAS/467/1965).
Note (3): The model SEDs were generated using the population synthesis models
          of Bruzual & Charlot (2003MNRAS.344.1000B). The LEPHARE routine fits
          for extinction, metallicity, age, star formation, and stellar mass,
          and allows for single burst, exponential decline, and constant star
          formation histories.
--------------------------------------------------------------------------------

History:
    From electronic version of the journal

================================================================================
(End)                                           Ana Fiallos [CDS]    27-Jun-2022
