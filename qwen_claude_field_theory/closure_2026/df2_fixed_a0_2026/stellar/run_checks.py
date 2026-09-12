"""Print deterministic convergence and isolated DF2 reference calculations."""
import json
import platform
import time
import numpy as np
import scipy
from profile import Sersic, aperture_second_moment

started = time.monotonic()
G = 6.67430e-11
MSUN = 1.98847e30
KPC = 3.085677581491367e19
a0 = 9.3619e-11
stellar_mass = 2e8*MSUN
radius = 2.0*KPC
eta = G*stellar_mass/(a0*radius**2)
rows = []
for grid_size in (1025,2049,4097):
    profile = Sersic(n=.6,grid_size=grid_size)
    predictions = []
    for aperture in (.3,.5,.7,1.,2.,np.inf):
        row = {'aperture_Re': 'global' if np.isinf(aperture) else aperture}
        for law in ('newtonian','aqual'):
            moment = aperture_second_moment(profile,eta,aperture,law)
            row[law+'_second_moment_a0Re'] = moment
            row[law+'_sigma_kms'] = np.sqrt(a0*radius*moment)/1000
        predictions.append(row)
    rows.append({'grid_size':grid_size,'integrated_mass':profile.integrated_mass,
                 'central_density':profile.central_density,'predictions':predictions})
print(json.dumps({'python':platform.python_version(),'numpy':np.__version__,
    'scipy':scipy.__version__,'elapsed_seconds':time.monotonic()-started,
    'inputs':{'n':.6,'Mstar_solar':2e8,'Re_kpc':2.,'distance_Mpc':20.,
              'a0_m_s2':a0,'eta':eta,'mass_to_light_V_solar':2.},
    'convergence':rows,
    'interpretation':'Isolated spherical isotropic constant-M/L circular-aperture predictions. '
    'The KCWI masked weighted rectangular aperture is not modeled; these are not observed-aperture fits.'},
    indent=2,allow_nan=False))
