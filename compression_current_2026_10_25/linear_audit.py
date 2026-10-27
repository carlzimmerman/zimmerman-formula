import argparse,json,sys
from pathlib import Path
import numpy as np
from compression import Compression
ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);args=ap.parse_args();m=Compression(eta=1.,wave_R_kpc=10000.);a=np.load('nonlinear_transfer_2026_10_25/run_exact_equilibrium/state.npz')['a'];rho=abs(a[0])**2/m.vol;rows=[]
for eta in [0.,.01,1.]:
 g2=m.g2*np.sqrt(eta);eta_local=g2*g2*rho**3/m.c**2;eps=.001;S=1+eps*eps+eta_local;hi=(S+np.sqrt(S*S-4*eps*eps))/2;lo=eps*eps/hi
 # Substitute stable roots into the polynomial, scaled to avoid cancellation.
 high_res=np.max(abs(hi-S+eps*eps/hi)/np.maximum(S,1));low_res=np.max(abs(lo-S+eps*eps/lo)/np.maximum(S,1));assert high_res<1e-12 and low_res<1e-12
 rows.append({'calibration_eta':eta,'g2':float(g2),'max_eta_local':float(max(eta_local)),'radius_at_max_kpc':float(m.r[np.argmax(eta_local)]*m.rm),'high_branch_speed_over_c_max':float(np.sqrt(max(hi))),'material_frequency_ratio_at_max_eta':float(np.sqrt(lo[np.argmax(eta_local)])/eps),'dispersion_residual':float(max(high_res,low_res))})
out={'scope':'Uniform pure-T quadratic sector with positive Omega², test Omega/(ck)=.001. Local density from actual benchmark; no local EOS replacement in dynamics. Not a completed relativistic model.','max_benchmark_T_density':float(max(rho)),'rows':rows};Path(args.output).write_text(json.dumps(out,indent=2)+'\n');print(out)
