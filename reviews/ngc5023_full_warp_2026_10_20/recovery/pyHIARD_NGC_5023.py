

from pyHIARD.common_functions import download_cube,create_masks,select_emission
from astropy.io import fits
import os

galaxy_parameters = {'Galaxy': 'NGC_5023', 'DHIkpc': 18.6  ,'Distance': 6.6, 'Original_Model': 'Tir', 'RMS': 0.0002 , 'MHI': 6.1e8  }


def get_data(work_dir,sofia_call='sofia2'):
    '''Download the data for this galaxy and prepare the cube for usage'''
    succes= False
    outdir = os.path.dirname(os.path.abspath(__file__))
    try:
        Cube = fits.open(f"{outdir}/NGC_5023.fits",uint = False, do_not_scale_image_data=True,ignore_blank = True)
    except FileNotFoundError:
        url = 'https://zenodo.org/record/3715549/files/NGC5023-HR-cube.fits'
        name = 'NGC_5023'
        sizes=[[7,62],[420,600],[430,570]]
        try:
            Cube = fits.open(f"{outdir}/{name}_Original.fits",uint = False, do_not_scale_image_data=True,ignore_blank = True)
        except:
            Cube = download_cube(f'{name}_Original',url,sizes,outdir)
        Clean_Cube,hdr = select_emission(Cube[0].data,Cube[0].header,name,work_dir,sofia_call=sofia_call)
        fits.writeto(f"{outdir}/{name}.fits",Clean_Cube,hdr,overwrite = False)
        Cube[0].data=Clean_Cube
        Cube[0].header=hdr
        if url != '':
            os.system(f"rm -f {outdir}/{name}_Original.fits")
        del Clean_Cube
        del hdr
    #place_disclaimer(dir_to_place)
    return Cube
get_data.__doc__=f'''
NAME:
   get_data

PURPOSE:
   Download the data for this galaxy and prepare the cube for usage

CATEGORY:
   agc

INPUTS:

OPTIONAL INPUTS:


OUTPUTS:
   Cube = Cube in astropy format

OPTIONAL OUTPUTS:

PROCEDURES CALLED:
   Unspecified

NOTE:
'''

def place_disclaimer(dir_to_place):
    disclaimer = '''----- NGC 5023 -----

    is part of the HALOGAS Survey (Heald et al. 2011)
    If you make use of these data products in any publication or presentation, we kindly ask you to cite the following paper(s):

    Primary HALOGAS reference: Heald et al. (2011)
    and to include the following acknowledgement:

    This research made use of data from WSRT HALOGAS-DR1. The Westerbork Synthesis Radio Telescope is operated by ASTRON (Netherlands Institute for Radio Astronomy) with support from the Netherlands Foundation for Scientific Research NWO.

    Please download the original HR cube from
    https://www.astron.nl/halogas/data.php

    Original Cube Name  NGC5023-HR-cube.fits

    This model is created by P.Kamphuis and published in
    HALOGAS observations of NGC 5023 and UGC 2082: Modeling of non-cylindrically symmetric gas distributions in edge-on galaxies" Kamphuis, P.; Rand, R. J.; Józsa, G. I. G.; Zschaechner, L. K.; Heald, G. H.; Patterson, M. T.; Gentile, G.; Walterbos, R. A. M.; Serra, P.; & de Blok, W. J. G. 2013, MNRAS, 434, 2069

'''
    with open(f'{dir_to_place}/ACKNOWLEDGE_HALOGAS.txt', 'w') as file:
        file.writelines(disclaimer)
place_disclaimer.__doc__=f'''
NAME:
   place_disclaimer

PURPOSE:
   Place a disclaimer about the source, models and acknowledgements in the directory.

CATEGORY:
   agc

INPUTS:
    dir_to_place = The directory where the galaxy is cretated.

OPTIONAL INPUTS:


OUTPUTS:

OPTIONAL OUTPUTS:

PROCEDURES CALLED:
   Unspecified

NOTE:
'''
