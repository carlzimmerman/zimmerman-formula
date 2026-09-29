J/MNRAS/496/3531       Abell 963 and Abell 2192 HI data          (Gogate+, 2020)
================================================================================
BUDHIES IV: Deep 21-cm neutral hydrogen, optical, and UV imaging data of
Abell 963 and Abell 2192 at z ~ 0.2.
    Gogate A.R., Verheijen M.A.W., Deshev B.Z., Van Gorkom J.H.,
    Montero-castano M., Van Der Hulst J.M., Jaffe Y.L., Poggianti B.M.
   <Mon. Not. R. Astron. Soc., 496, 3531-3552 (2020)>
   =2020MNRAS.496.3531G    (SIMBAD/NED BibCode)
================================================================================
ADC_Keywords: Clusters, galaxy ; H I data ; Redshifts ;
              Photometry ; Optical ; Ultraviolet
Keywords: galaxies: clusters: general - galaxies: evolution -
          galaxies: photometry - radio lines: galaxies

Abstract:
    In this paper, we present data from the Blind Ultra-Deep HI
    Environmental Survey (BUDHIES), which is a blind 21-cm HI spectral
    line imaging survey undertaken with the Westerbork Synthesis Radio
    Telescope. Two volumes were surveyed, each with a single pointing and
    covering a redshift range of 0.164<z<0.224. Within these two
    volumes, this survey targeted the clusters Abell 963 and Abell 2192,
    which are dynamically different and offer unique environments to study
    the process of galaxy evolution within clusters. With an integration
    time of 117x12h on Abell 963 and 72x12h on Abell 2192, a total
    of 166 galaxies were detected and imaged in HI. While the clusters
    themselves occupy only 4 per cent of the 73400Mpc^3^ surveyed by
    BUDHIES, most of the volume consists of large-scale structures in
    which the clusters are embedded, including foreground and background
    overdensities and voids. We present the data processing and source
    detection techniques and counterpart identification based on a
    wide-field optical imaging survey using the Isaac Newton Telescope and
    deep ultraviolet (UV) Galaxy Evolution Explorer (GALEX) imaging.
    Finally, we present HI and optical catalogues of the detected sources
    as well as atlases of their global HI properties, which include
    integrated column density maps, position-velocity diagrams, global HI
    profiles, and optical and UV images of the HI sources.

Description:
    In this paper, we have presented the results of a blind, 21-cm HI
    imaging survey with the WSRT, covering a redshift range of
    0.164<z<0.224 in each of two pointings, thereby surveying a total
    volume of 73-400Mpc^3^ within the FWQM of the primary beam with a
    velocity resolution of 19km/s and an average angular resolution
    of 23x38arcsec^2^.

    A total of 166 galaxies are detected within the total survey volume,
    none of which have been previously detected in HI. We have also
    presented ancillary optical imaging data of the two fields in the
    Harris B and R bands, obtained with the Wide-Field Camera on the INT
    on La Palma.

    In addition, we have obtained deep, near- and far-UV ancillary imaging
    data of the two fields with the GALEX satellite.

File Summary:
--------------------------------------------------------------------------------
 FileName      Lrecl  Records   Explanations
--------------------------------------------------------------------------------
ReadMe            80        .   This file
tablea1.dat      110      127   Catalogue containing the HI properties of the
                                 detected galaxies in A963
tablea2.dat      110       39   Catalogue containing the HI properties of the
                                 detected galaxies in A2192
tablea3.dat       84      127   The optical properties of the HI detected
                                 galaxies in A963
tablea4.dat       84       39   The optical properties of the HI detected
                                 galaxies in A2192
--------------------------------------------------------------------------------

Byte-by-byte Description of file: tablea1.dat tablea2.dat
--------------------------------------------------------------------------------
   Bytes Format Units     Label     Explanations
--------------------------------------------------------------------------------
   1-  3  I3    ---       Index     Serial number assigned to each HI detection
   5- 25  A21   ---       HIName    HI name (HIJHHMMSS.ss+DDMMSS.s)
  27- 28  I2    h         RAh       HI centre Right ascension (J2000)
  30- 31  I2    min       RAm       HI centre Right ascension (J2000)
  33- 37  F5.2  s         RAs       HI centre Right ascension (J2000)
      38  A1    ---       DE-       HI centre Declination sign (J2000)
  39- 40  I2    deg       DEd       HI centre Declination (J2000)
  42- 43  I2    arcmin    DEm       HI centre Declination (J2000)
  45- 48  F4.1  arcsec    DEs       HI centre Declination (J2000)
  50- 56  F7.5  ---       z         HI redshift
  58- 63  F6.1  Mpc       Dlum      Luminosity distance to the galaxy derived
                                     from co-moving distances based on the HI
                                     redshifts and the adopted cosmology
  65- 69  F5.1  km/s      W20       HI linewidth at 20 per cent of the peak HI
                                     flux (1)
  71- 74  F4.1  km/s    e_W20       HI linewidth at 20 per cent of the peak HI
                                     flux error
  76- 80  F5.1  km/s      W50       HI linewidth at 50 per cent of the peak HI
                                     flux (1)
  82- 86  F5.1  km/s    e_W50       HI linewidth at 50 per cent of the peak HI
                                     flux error
  88- 92  F5.1 mJy.km/s   Sint      Primary beam corrected integrated HI flux
                                     density, obtained from the R4 cubes
  94- 97  F4.1 mJy.km/s e_Sint      Primary beam corrected integrated HI flux
                                     density error
  99-103  F5.2 10+9Msun   MHI       Total HI mass
 105-108  F4.2 10+9Msun e_MHI       Total HI mass error
     110  I1    ---       Type      [1/3] Type of profile based on the
                                     global HI profile (2)
--------------------------------------------------------------------------------
Note (1): derived from the R4 cubes. These linewidths have not been corrected
  for instrumental broadening.
Note (2): Type as follows:
  1 = double horned
  2 = single Gaussian like
  3 = asymmetric
--------------------------------------------------------------------------------

Byte-by-byte Description of file: tablea3.dat tablea4.dat
--------------------------------------------------------------------------------
   Bytes Format Units   Label    Explanations
--------------------------------------------------------------------------------
   1-  3  I3    ---     Index    Serial number assigned to each HI detection
   5- 25  A21   ---     HIName   HI name (HIJHHMMSS.ss+DDMMSS.s)
  27- 28  I2    h       RAh      HI centre Right ascension (J2000)
  30- 31  I2    min     RAm      HI centre Right ascension (J2000)
  33- 37  F5.2  s       RAs      HI centre Right ascension (J2000)
      38  A1    ---     DE-      HI centre Declination sign (J2000)
  39- 40  I2    deg     DEd      HI centre Declination (J2000)
  42- 43  I2    arcmin  DEm      HI centre Declination (J2000)
  45- 49  F5.2  arcsec  DEs      HI centre Declination (J2000)
  51- 53  I3    deg     PA       Position angle
  55- 62  F8.6  ---     zopt     ?=0 Optical redshift z from the literature for
                                  those objects which have optical spectroscopy
  64- 67  F4.1  mag     Bmag     B magnitude (1)
      68  A1    ---   n_Bmag     [*] Note on Bmag (2)
  70- 73  F4.1  mag     Rmag     R magnitude (1)
      74  A1    ---   n_Rmag     [*] Note on Rmag (2)
  76- 79  F4.1  mag     FUVmag   ?=0 Observed FUV magnitude extracted from GALEX
  81- 84  F4.1  mag     NUVmag   ?=0 Observed NUV magnitude extracted from GALEX
--------------------------------------------------------------------------------
Note (1): magnitude calculated after INT data reduction and source extraction.
   These values have not been extinction or k-corrected.
Note (2): Note as follows:
   * = Galaxies close to bright stars or at the edge of the field with
        incorrect/unavailable INT magnitudes. The values given are converted
        from SDSS u, g, r, and i magnitudes.
--------------------------------------------------------------------------------

History:
    From electronic version of the journal

References:
    Jaffe et al., Paper I   2013MNRAS.431.2111J, Cat. J/MNRAS/431/2111
    Jaffe et al., Paper II  2015MNRAS.448.1715J
    Jaffe et al., Paper III 2016MNRAS.461.1202J
================================================================================
(End)                                           Ana Fiallos [CDS]    05-Jul-2023
