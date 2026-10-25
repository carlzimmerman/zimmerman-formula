"""Necessary self-virial support of the conditional Plummer profiles; no equilibrium proof."""
import os
for k in ['OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS']:os.environ[k]='1'
import json,pathlib,numpy as np
from scipy.integrate import quad
P=pathlib.Path(__file__).resolve().parent;ROOT=P.parents[1];G=.00430091;eta=1500.
I=quad(lambda x:x**4/(1+x*x)**4.5,0,np.inf,epsabs=1e-13)[0];J=quad(lambda x:x*x/(1+x*x)**3,0,np.inf,epsabs=1e-13)[0];assert abs(I-2/35)<1e-12 and abs(J-np.pi/16)<1e-12
models=json.loads((ROOT/'sol61_push/cold_survey_capture_2026_10_24/capture_results.json').read_text())['models'];rows=[]
for m in models:
 M=m['cold_mass'];b=m['cold_scale_pc'];Ka=15*eta**2*M/(28*b*b);W=-3*np.pi*G*M*M/(32*b);Kr=-.5*W;fraction=Ka/Kr
 assert abs(fraction-80*eta**2/(7*np.pi*G*M*b))<1e-12
 rows.append(dict(name=m['name'],mass_Msun=M,b_pc=b,amplitude_kinetic_Msun_kms2=Ka,self_gravity_W_Msun_kms2=W,stationary_required_K_Msun_kms2=Kr,amplitude_fraction_of_required_K=fraction,phase_fraction_if_exact_smooth_density=max(0,1-fraction),phase_rms_if_exact_smooth_density_kms=float(np.sqrt(max(0,2*(Kr-Ka)/M)))))
print(json.dumps(dict(eta_pc_kms=eta,G=G,integral_amplitude=I,integral_gravity=J,models=rows,scope='necessary stationary self-virial support ONLY IF the exact instantaneous single-field density equals the smooth Plummer profile; coarse-grained density can hide additional amplitude-gradient support; not sufficient equilibrium, not bound-remnant selection; baryons/tides ignored, no stellar survival inference'),indent=2))
