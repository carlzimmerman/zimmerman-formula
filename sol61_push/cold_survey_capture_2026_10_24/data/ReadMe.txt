J/A+A/698/A53       Sextans dwarf spheroidal members            (Tolstoy+, 2025)
================================================================================
A 3D view of dwarf galaxies with Gaia and VLT FLAMES.
II. The Sextans dwarf spheroidal.
    Tolstoy E., Battaglia G., Arroyo-Polonio J.M., Brown A.G.A., van Essen T.,
    Massari D., Skuladottir A., Irwin M.J., Taibi S., Pritchard J.
    <Astron. Astrophys. 698, A53 (2025)>
    =2025A&A...698A..53T        (SIMBAD/NED BibCode)
================================================================================
ADC_Keywords: Galaxies, nearby ; Stars, giant ; Radial velocities ;
              Spectroscopy ; Optical
Keywords: stars: abundances - galaxies: dwarf - galaxies: evolution -
          galaxies: individual: Sextans dwarf spheroidal

Abstract:
    The Sextans dwarf spheroidal galaxy has been challenging to study in a
    comprehensive way as it is highly extended on the sky, with an
    uncertain but large tidal radius of between 80-160 arcminutes (or
    3-4kpc), and an extremely low central surface brightness of
    Sigma_V_~26.2mag/arcsec^2^.

    Here, we present a new homogeneous survey of 41 VLT/FLAMES multi-fibre
    spectroscopic pointings that contain 2108 individual spectra, and
    combined with Gaia DR3 photometry and astrometry we present vlos
    measurements for 333 individual red giant branch stars that are
    consistent with membership in the Sextans dwarf spheroidal galaxy. In
    addition, we provide the metallicity, [Fe/H], determined from the two
    strongest CaII triplet lines, for 312 of these stars.

    We look again at the global characteristics of Sextans, deriving a
    mean line-of-sight velocity of <vlos>=+227.1km/s and a mean
    metallicity of <[Fe/H]>=-2.37. The metallicity distribution is clearly
    double-peaked, with the highest peak at [Fe/H]=-2.81 and another
    broader peak at [Fe/H]~=-2.09. Thus, it appears that Sextans hosts two
    populations and the superposition leads to a radial variation in the
    mean metallicity, with the more metal-rich population being centrally
    concentrated.

    In addition, there is an intriguing group of nine probable members in
    the outer region of Sextans at higher [Fe/H] than the mean in this
    region. If these stars were confirmed as members, they would eliminate
    the metallicity gradient. We also look again at the colour-magnitude
    diagram of the resolved stellar population in Sextans, and at the
    relation between Sextans and the intriguingly nearby globular cluster,
    Pal 3.

    The global properties of Sextans have not changed significantly
    compared to previous studies, but they are now more precise, and the
    sample of known members in the outer regions is now more complete.

Description:
    We present our new measurements of vlos and [Fe/H] for new and
    archival data for individual stars in the Sextans dSph from the ESO
    (European Southern Observatory) Very Large Telescope (VLT)
    FLAMES/GIRAFFE spectra of RGB stars. These data were collected between
    2003 and 2019 in two main observing campaigns

    From a combination of new and old re-processed archival VLT/FLAMES LR8
    data, we have obtained a uniform sample of [Fe/H], vlos and Gaia DR3
    astrometric parameters for 312 individual member RGB stars, extending
    to (and beyond) the nominal tidal radius.

    The full sample of measurements of the 604 likely members of the
    Sextans dSph are presented online (Table D.1). Table D.1 includes,
    where it is available, FLAMES spectroscopic information, and for those
    stars not in the FLAMES sample but with a reliable Walker vlos
    measurement (Walker et al. 2023ApJS..268...19W, Cat. J/ApJS/268/19),
    these are also included in Table D.1. In addition, the FLAMES
    spectroscopic and Gaia DR3 properties of the 9 probable members that
    are vlos members but have uncertain Sextans membership based on Gaia
    DR3 are included in Table D.1. In Table D.2 we also provide the Gaia
    DR3 and spectroscopic information for the stars for which we have
    FLAMES observations but either are very clear non-members on the basis
    of their spectroscopic vlos or their spectroscopic measurements were
    not found to be reliable enough. If the unreliable spectroscopic
    members are likely Gaia members then this also noted in Table D.1 and
    D.2.

File Summary:
--------------------------------------------------------------------------------
 FileName   Lrecl  Records  Explanations
--------------------------------------------------------------------------------
ReadMe         80        .  This file
tabled1.dat   225      612 *Full sample of measurements of the 604 likely
                             members of the Sextans dSph
tabled2.dat   178     1713  Gaia DR3 and spectroscopic information for the stars
                             for which we have FLAMES observations but either
                             are very clear non-members on the basis of their
                             spectroscopic vlos or their spectroscopic
                             measurements were not found to be reliable enough
--------------------------------------------------------------------------------
Note on tabled1.dat: We have included here all the Gaia DR3 likely members in
  this table even those without FLAMES spectra.
--------------------------------------------------------------------------------

See also:
         I/355 : Gaia DR3 Part 1. Main source (Gaia Collaboration, 2022)
 J/ApJS/268/19 : M2FS + Hectochelle spectra of dSph in MW halo (Walker+, 2023)
 J/A+A/675/A49 : vlos of Sculptor dSph red giants (Tolstoy+, 2023)

Byte-by-byte Description of file: tabled1.dat
--------------------------------------------------------------------------------
   Bytes Format Units     Label       Explanations
--------------------------------------------------------------------------------
   1- 19  I19   ---       GaiaDR3     Gaia DR3 identification number
  21- 29  F9.5  deg       RAdeg       Gaia right ascension (ICRS) at Ep=2016.0
  31- 38  F8.5  deg       DEdeg       Gaia declination (ICRS) at Ep=2016.0
  40- 45  F6.3  mag       Gmag        Gaia G magnitude
  47- 52  F6.3  mag       BPmag       Gaia BP magnitude
  54- 59  F6.3  mag       RPmag       Gaia RP magnitude
  61- 67  F7.4  mas       plx         Gaia parallax
  69- 74  F6.4  mas     e_plx         Gaia parallax error
  76- 81  F6.3  mas/yr    pmRA        Gaia proper motion along RA
  83- 87  F5.3  mas/yr  e_pmRA        Gaia proper motion along RA error
  89- 94  F6.3  mas/yr    pmDE        Gaia proper motion along DE
  96-100  F5.3  mas/yr  e_pmDE        Gaia proper motion along DE error
 102-119  A18   ---       FLAMESfield Name of the VLT/FLAMES pointing
 121-128  A8    ---       SpecName    Name of object in VLT/FLAMES pointing
     130  I1    ---       Nspec       ? Number of individual VLT/FLAMES spectra
                                       combined
 132-137  F6.2  ---       CombSN      ? Combined signal to noise for the
                                       FLAMES spectra (1)
 139-144  F6.2  km/s      Vel         ? Average radial velocity for the
                                       FLAMES spectra (2)
 146-150  F5.3  km/s    e_Vel         ? Average radial velocity error for the
                                       FLAMES spectra (2)
 152-156  F5.3  km/s      varVel      ? Variance of radial velocity
                                       measurements, if Nspec>1 (2)
 158-162  F5.2  [-]       [Fe/H]      ? Average [Fe/H] for FLAMES spectra (3)
 164-168  F5.3  [-]     e_[Fe/H]      ? Error on average [Fe/H] for
                                       FLAMES spectra (3)
 170-174  F5.3  [-]       var[Fe/H]   ? Variance of [Fe/H] measurements,
                                       if Nspec>1 (3)
 176-180  F5.3  ---       Pmem        [0/1] Probability of membership from
                                       Battaglia et al. (2022A&A...657A..54B,
                                       Cat. J/A+A/657/A54) analysis (4)
 182-225  A44   ---       Notes       Previous observations (5)
--------------------------------------------------------------------------------
Note (1): the signal-to-noise of the single (for Nspec=1) or combined
  VLT/FLAMES spectra.
Note (2): The vlos for this star measured from VLT/FLAMES spectra, averaged if
  Nspec>1.
  The velocities in this table can be reliable if the stars are members,
  but are advised to be used with caution, if at all. They are not used in this
  paper. Some stars have other better FLAMES spectra as part of this survey and
  are thus listed in Table.D.1 with those values (which may differ from what is
  here).
Note (3): [Fe/H] for the star determined from the CaT measurement from
  VLT/FLAMES spectra, averaged if Nspec>1.
Note (4): Stars with Pmem=0 are stars with VLT/FLAMES spectroscopic vlos
  compatible with membership in Sextans but the Gaia proper motions and/or
  parallaxes are just on the wrong side of the membership cuts. They are
  borderline members.
Note (5): Notes refer to previous measurements of these stars:
  Walker et al. (2023ApJS..268...19W, Cat. J/ApJS/268/19) (W23) with the radial
   velocity, Theler et al. (2020A&A...642A.176T, Cat. J/A+A/642/A176);
   Shetrone et al. (2001ApJ...548..592S); Aoki et al. (2009A&A...502..569A).
--------------------------------------------------------------------------------

Byte-by-byte Description of file: tabled2.dat
--------------------------------------------------------------------------------
   Bytes Format Units   Label        Explanations
--------------------------------------------------------------------------------
   1- 19  I19   ---     GaiaDR3      ? Gaia DR3 identifier
  21- 31  F11.7 deg     RAdeg        Gaia right ascension (ICRS) at Ep=2016.0
  33- 43  E11.3 deg     DEdeg        Gaia declination (ICRS) at Ep=2016.0
  45- 62  A18   ---     FLAMESfield  FLAMES field name
  64- 71  A8    ---     Specname     FLAMES target name
  73- 81  F9.6  mag     Gmag         ? Gaia DR3 G magnitude
  83- 93  F11.7 ---     S/N          Signal-to-noise ratio
  95-101  F7.2  km/s    Vel          Helioenctric radial velocity
 103-106  F4.2  ---     Pmem         [0/1]? Probability of membership
 108-111  A4    ---     Cmem         Membership class (1)
 113-178  A66   ---     Notes        Why rejected
--------------------------------------------------------------------------------
Note (1): Membership class code as follows:
   LM  = likely member
   LMp = likely member, the star maybe a member but it is peculiar
          (a C-star or a double star, for example)
   M   = member
   Mp  = member, the star is a member but it is peculiar
          (a C-star or a double star, for example)
   NM  = not member
--------------------------------------------------------------------------------

Acknowledgements:
    Eline Tolstoy, etolstoy(at)astro.rug.nl

References:
    Tolstoy et al., Paper I     2023A&A...675A..49T, Cat. J/A+A/675/A49

================================================================================
(End)                                        Patricia Vannier [CDS]  22-Apr-2025
