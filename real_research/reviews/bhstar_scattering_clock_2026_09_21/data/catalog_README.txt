File description of deGraaff2026_mnras_lrds_withdups_blackbody_eline_fits.fits (de Graaff et al. 2026)
This file contains 181 entries, but only 146 unique sources. Duplicate entries are flagged in the table.

Column              Unit        Description
pid                 -           JWST program ID   
srcid               -           MSA ID number   
root                -           DJA root name
file                -           DJA filename   
ra                  deg         Right ascension   
dec                 deg         Declination   
zspec               -           Spectroscopic redshift   
f444w_aper0.1       nJy         NIRCam/F444W circular aperture flux (radius 0.1 arcsec)    
mu                  -           Lensing magnification factor (obtained from Furtak et al. 2023 and Sarrouh et al. 2025)   
Ndup                -           Number of duplicate PRISM spectra in LRD table   
dup_filenames       -           DJA filenames of duplicate spectra   
use_dG26	    -           Flag to filter the 146 unique sources (with their highest S/N PRISM spectra) used in de Graaff+ 2026
lambda_v            um          Inflection wavelength of v-shape ([5, 16, 50, 84, 95] percentiles)   
beta_UV             -           UV slope (measured from PRISM spectrum; [5, 16, 50, 84, 95] percentiles)  
M_UV                mag         Absolute magnitude at 1500 AA (measured from PRISM spectrum, [5, 16, 50, 84, 95] percentiles)  
break_strength      -           Balmer break strength ([5, 16, 50, 84, 95] percentiles)   
beta_MBB            -           Power-law slope of modified blackbody ([5, 16, 50, 84, 95] percentiles)   
Teff                K           Effective temperature of modified blackbody ([5, 16, 50, 84, 95] percentiles)  
peak_wave           um          Peak wavelength of modified blackbody ([5, 16, 50, 84, 95] percentiles)  
logL_MBB            log erg/s   Integrated luminosity of modified blackbody ([5, 16, 50, 84, 95] percentiles)   
logL_5100           log erg/s   Optical luminosity 5100 AA ([5, 16, 50, 84, 95] percentiles)   
L5100_LMBB          -           Ratio of L_5100 to L_blackbody ([5, 16, 50, 84, 95] percentiles)   
Ha_total_ew         AA (rest)   Total (broad+narrow) Halpha EW ([5, 16, 50, 84, 95] percentiles)   
Hb_total_ew         AA (rest)   Total (broad+narrow) Hbeta EW ([5, 16, 50, 84, 95] percentiles)    
Balmer_dec_total    -           Total (broad+narrow) Balmer decrement Halpha/Hbeta ([5, 16, 50, 84, 95] percentiles)    
LHa_total           erg/s       Total (broad+narrow) Halpha luminosity ([5, 16, 50, 84, 95] percentiles)   
logLHa_total        log erg/s   Total (broad+narrow) Halpha luminosity ([5, 16, 50, 84, 95] percentiles)   
OIII_5007_ew        AA (rest)   Oiii_5007  EW ([5, 16, 50, 84, 95] percentiles)   
LOIII_5007          erg/s       Oiii_5007 luminosity ([5, 16, 50, 84, 95] percentiles)   
logLOIII_5007       log erg/s   Oiii_5007 luminosity ([5, 16, 50, 84, 95] percentiles)     
LOI_8446            erg/s       Oi_8446 luminosity ([5, 16, 50, 84, 95] percentiles)   
logLOI_8446         log erg/s   Oi_8446 luminosity ([5, 16, 50, 84, 95] percentiles)    


The LRD spectra were retrieved from the public DAWN JWST Archive and originate from the following JWST programs:

CANUCS (GTO-1208), Sarrouh et al. 2025 (5 spectra) 
CAPERS (GO-6368), PI: Dickinson (20 spectra) 
CEERS (GO-1345), Finkelstein et al. 2025 (2 spectra) 
DDT-2750, PI: Arrabal Haro (2 spectra) 
DDT-2767, PI: Kelly (1 spectrum) 
DDT-6585, PI: Coulter (3 spectra) 
GO-1433, PI: Coe (1 spectrum) 
GO-2198, Barrufet et al. 2025 (3 spectra) 
GO-4106, PIs: Nelson & Labbe  (9 spectra) 
GO-5545, PI: Barrufet (7 spectra)
GO-5997, PI: Looser (1 spectrum)
GO-8018, PI: Lin (8 spectra)
GO-8060, PI: Egami (3 spectra)
GTO-WIDE, (GTO-1212, GTO-1213, GTO-1215), Maseda et al. 2024 (5 spectra)  
JADES, (GTO-1180, GTO-1181, GTO-1286), Curtis-Lake et al. 2025, Scholtz et al. 2025 (16 spectra) 
Mirage or Miracle (GO-5224), PIs: Oesch & Naidu (13 spectra) 
NEXUS (GO-5105), Shen et al. 2024 (27 spectra)
RUBIES (GO-4233), de Graaff et al. 2025b (38 spectra) 
UNCOVER (GO-2561), Bezanson et al. 2024, Price et al. 2025 (17 spectra) 


