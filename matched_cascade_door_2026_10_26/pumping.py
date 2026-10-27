"""Compression work on occupied local modes; explicitly not mode creation."""
import argparse,json
from pathlib import Path
import numpy as np
from scipy.optimize import minimize_scalar
from exact_vertex_checked import P,mode,exact_resonance,full_vertex
from spectrum import parameters

def energy_check(k,length):
 m=mode(k,length);rho,c,g,alpha,ell,M,lam=parameters(length);K=np.array(k)@np.array(k)
 from spectrum import omega
 bare=omega(k,length)[2]
 E=rho*K*abs(m['phi'])**2+bare/(rho*K)*m['A']**2+m['chit']**2+c*c*K*abs(m['chi'])**2+abs(m['ps'])**2+c*c*K*m['s']**2
 E+=M*M*(m['s']-lam*m['A'])**2
 return abs(E/m['w']-1)

def run(out):
 original=P.copy();stat=json.loads(Path('matched_cascade_door_2026_10_26/run_static_window/results.json').read_text());rows=[]
 for row in stat['rows']:
  length=row['length_pc'];P['rho']=row['local_patch']['rho'];P['u']=row['local_patch']['u'];rho=P['rho'];eta=P['g2']**2*rho**3/P['c']**2
  lam=parameters(length)[-1];beta=4*rho*P['c']**2*lam*lam/P['kappa']
  slope=2/3+beta/(2*(1+beta))-3*eta/(2*(1+eta))
  fn=lambda z:z**(2/3)*np.sqrt((1+beta*z)/(1+beta)*(1+eta)/(1+eta*z**3))
  opt=minimize_scalar(lambda z:-fn(z),bounds=(1,4),method='bounded',options={'xatol':1e-12})
  # Exact full-parent finite difference: rho and advected k change, u held fixed.
  derivatives=[]
  for eps in [1e-3,1e-4,1e-5]:
   vals=[]
   for sign in [-1,1]:
    factor=np.exp(sign*eps);P['rho']=rho*factor;vals.append(mode([80*factor**(1/3),0,0],length)['w'])
   derivatives.append(float(np.log(vals[1]/vals[0])/(2*eps)))
  P['rho']=rho
  k1,k2=exact_resonance(80,length);V,terms,modes=full_vertex(k1,k2,length,(4*np.pi/80)**3/3)
  N=.05**2*rho*rho*((4*np.pi/80)**3/3)/(64*modes[0]['A']**2)
  energy_errors=[energy_check(k,length) for k in [k1,k2,k1+k2]]
  assert max(energy_errors)<1e-9
  assert max(derivatives)-min(derivatives)<1e-6
  assert row['density_KKT_max']<1e-6 and row['gradient_max']<1e-8
  rows.append({'length_pc':length,'rho':rho,'u':P['u'],'eta':eta,'beta':beta,'static_law_error_percent':row['diagnostics']['law_error_percent'],
    'high_k_compression_slope':slope,'exact_q80_fixed_u_slopes':derivatives,
    'maximum_high_k_adiabatic_energy_gain_fraction':max(0,fn(opt.x)-1),'compression_at_maximum':float(opt.x),
    'exact_q80_vertex':V,'specified_weak_mode_coupling_per_Myr':abs(V)*np.sqrt(N)/P['tdyn_Myr'],
    'mode_energy_normalization_errors':energy_errors,'frequencies_per_Myr':[m['w']/P['tdyn_Myr'] for m in modes]})
 P.clear();P.update(original)
 rho=P['rho'];eta=P['g2']**2*rho**3/P['c']**2;lam=parameters(.1)[-1];b01=4*rho*P['c']**2*lam*lam/P['kappa']
 critical=.1*np.sqrt(((5*eta-4)/(7-2*eta))/b01)
 # beta -> infinity yields an upper envelope for every positive beta and C>=1.
 C=(3.5/eta)**(1/3);upper=C**(7/6)*np.sqrt((1+eta)/(1+eta*C**3))
 result={'rows':rows,'original_patch_pumping_threshold_pc':critical,'original_patch_all_beta_high_k_gain_upper_bound':upper-1,
 'scope':'Homogeneous high-k quantum-pressure regime, isotropic advected k, constant microscopic coefficients, conserved adiabatic mode action. Exact derivative control holds u fixed. No mode creation from zero classical amplitudes, no actual occupation or mean-flow solution, no radiative energy export.'}
 Path(out).write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))

if __name__=='__main__':
 a=argparse.ArgumentParser();a.add_argument('--output',required=True);run(a.parse_args().output)
