"""Separate forces creating the initial source; don't label grid ringdown infall."""
import argparse,json
from pathlib import Path
import numpy as np
from cached_collocated import Collocated
from fine_initial import fine_initial
ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);args=ap.parse_args()
m=Collocated(eta=.01,material_h_kpc=.125,wave_R_kpc=10000.)
rows=[]
for case in ['formed','dilated']:
 a,x,c,v,meta=fine_initial(m,case,'nonlinear_transfer_2026_10_25/run_exact_equilibrium/state.npz')
 mu=m.pot(a,x,True)[1];kin=m.kd*a
 kin[:,:-1]+=m.ko*a[:,1:];kin[:,1:]+=m.ko*a[:,:-1]
 parts={'density_potential':mu*a,'gradient':kin,'alignment':m.J*m.alignment(a,x,c)}
 rho=abs(a[0])**2/m.vol
 def source_dot(Ha):
  ad=-1j*Ha/m.sigma;psi=a[0]/np.sqrt(m.vol);pd=ad[0]/np.sqrt(m.vol)
  D=m.k*m.w*np.imag(np.conj(pd[:-1])*psi[1:]+np.conj(psi[:-1])*pd[1:]);B=np.zeros(m.n)
  B[:-1]+=D*m.g2/m.sigma*(-1.5*rho[:-1]+.5*rho[1:]);B[1:]+=D*m.g2/m.sigma*(1.5*rho[1:]-.5*rho[:-1])
  G=2*m.J/m.sigma*np.imag(np.conj(ad[0])*m.alignment(a,x,c)[0]+np.conj(a[0])*m.alignment(ad,x,c)[0])
  return B,(m.g+2*m.g2*rho)*G
 def norm(v):return float(np.sqrt(np.sum(v*v/m.vol)))
 def pnorm(v):
  prev=np.cumsum(v)-v
  return float(np.sum((v*v+2*v*prev)/m.r))
 d={k:source_dot(H) for k,H in parts.items()};total=sum((b+cc for b,cc in d.values()))
 out={k:{'bulk_norm':norm(b),'conversion_norm':norm(cc),'total_norm':norm(b+cc),'poisson_norm_squared':pnorm(b+cc)} for k,(b,cc) in d.items()}
 mask=m.r*m.rm<.5
 # This masks the source, not a positive attribution of cross terms.
 out['all']={'total_norm':norm(total),'poisson_norm_squared':pnorm(total),'source_below_half_kpc_poisson_norm_squared':pnorm(total*mask),'source_above_half_kpc_poisson_norm_squared':pnorm(total*(~mask))}
 rows.append({'case':case,'force_components':out})
Path(args.output).write_text(json.dumps({'cases':rows,'interpretation':'Initial acceleration decomposition only. Norms are not additive because force components interfere.'},indent=2)+'\n');print(json.dumps(rows,indent=2))
