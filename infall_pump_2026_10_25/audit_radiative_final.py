import argparse,json
from pathlib import Path
import numpy as np
from live_collocated import Collocated
from radiative_modes_final import decompose
ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);args=ap.parse_args();m=Collocated(eta=.01,material_h_kpc=.125,wave_R_kpc=10000.);r=m.wr;rows=[]
for omega in [0.,.2,20.]:
 if omega==0:u=np.ones_like(r)*1e-5;ut=np.zeros_like(r)
 else:
  center=2500/m.rm;width=600/m.rm;k=omega*m.tdyn/m.c;env=np.exp(-.5*((r-center)/width)**2);u=1e-5*env*np.cos(k*(r-center));ur=1e-5*env*(-(r-center)/width**2*np.cos(k*(r-center))-k*np.sin(k*(r-center)));ut=-m.c*ur
 d=decompose(r,u/r,ut/r,m.c,m.tdyn,500/m.rm,5000/m.rm);d['input_omega_rad_Myr']=omega;rows.append(d)
out={'cases':rows,'interpretation':'Analytic outgoing Gaussian packets and static1/r field on the actual far grid. Spectral windows need not resolve a sub-cycle low-frequency packet.'};Path(args.output).write_text(json.dumps(out,indent=2)+'\n');print(out)
assert rows[0]['outgoing_characteristic_energy']<1e-25
assert rows[2]['incoming_fraction']<1e-4
assert rows[2]['windowed_spectra'][0]['windowed_fraction_above10_rad_Myr']>.99

assert all(abs(z["decomposition_identity_error"])<1e-12 for z in rows)
