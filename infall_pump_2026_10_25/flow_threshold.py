"""Check a necessary local energetic condition; do NOT infer an instability."""
import argparse,json
from pathlib import Path
import numpy as np
from live_collocated import Collocated
ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);args=ap.parse_args();m=Collocated(eta=.01,material_h_kpc=.125,wave_R_kpc=10000.);rows=[]
for name in ['run_infall','run_time_half','run_rest_control']:
 path=Path('infall_pump_2026_10_25')/name;state=np.load(path/'state.npz');a=state['a'];c=state['chi'];x=state['alpha'];rho=abs(a[0])**2/m.vol;mf=abs(a[1])**2;mt=abs(a[0])**2;q=mt/np.maximum(mt+mf,1e-300)
 U=m.geometry(a,c)[3];psi=a[0]/np.sqrt(m.vol);jf=m.k/m.sigma*m.w*np.imag(np.conj(psi[:-1])*U*psi[1:]);rf=.5*(m.r[1:]+m.r[:-1]);rhof=.5*(rho[1:]+rho[:-1]);vel=jf/np.maximum(rf**2*rhof,1e-300)
 u=.5*(m.enclosed(mt)[1:]+m.enclosed(mt)[:-1]);eta=m.g2**2*rhof**3/m.c**2;Delta=np.sqrt(np.maximum(rhof*((1-u)**-2-1),0));vcrit=np.sqrt(m.sigma*Delta/(1+eta));ratio=abs(vel)/np.maximum(vcrit,1e-100)
 mask=(q[:-1]>.99)&(q[1:]>.99)&(rf*m.rm>=1.5)&(rf*m.rm<=50)&(rhof>1e-10)
 i=np.flatnonzero(mask)[np.argmax(ratio[mask])];res=json.loads((path/'results.json').read_text());vunit=299792458/m.c/1000
 rows.append({'run':name,'time_Myr':res['completed_time_Myr'],'max_abs_flow_over_radial_phase_threshold':float(ratio[i]),'radius_of_max_kpc':float(rf[i]*m.rm),'flow_at_max_km_s':float(vel[i]*vunit),'threshold_at_max_km_s':float(vcrit[i]*vunit),'sample_radii':[{'r_kpc':r,'abs_flow_km_s':float(np.interp(r,rf*m.rm,abs(vel))*vunit),'threshold_km_s':float(np.interp(r,rf*m.rm,vcrit)*vunit)} for r in [1.5,3,10,30,50]]})
Path(args.output).write_text(json.dumps({'cases':rows,'assumptions':'Local pure-T WKB radial dispersion, quasistatic near field, velocity much smaller than c. Mixed interface and a full flow stability eigenproblem excluded. Above-threshold energetic waves alone do not prove growth.'},indent=2)+'\n');print(json.dumps(rows,indent=2))
