import argparse,json
from pathlib import Path
import numpy as np
from scipy.linalg import eigh_tridiagonal
from spectrum import Curves,levels,MU
from kinetics_v3 import Rates,parcel,PROFILES
BASE=Path(__file__).resolve().parent

def main():
 p=argparse.ArgumentParser();p.add_argument('--output',required=True);args=p.parse_args()
 baseline=json.loads((BASE/'run_spectrum/results.json').read_text());fine=json.loads((BASE/'run_refine/results.json').read_text());tail=json.loads((BASE/'run_tail/results.json').read_text())
 conv=[]
 for label,d in [('refine',fine),('tail',tail)]:
  v=np.array(d['k_over_alpha3']).sum(axis=1)/np.array(baseline['k_over_alpha3']).sum(axis=1)-1
  conv.append(dict(label=label,max_total_rate_relative_change=float(max(abs(v))),max_level_binding_change=float(max(abs(x['D']-y['D']) for x,y in zip(d['levels'],baseline['levels'])))))
 # Orthogonal continuum normalization check: finite-volume eigenstates / local spacing.
 h=.04;L=200.;curves=Curves();r,ls,w=levels(curves,h,L);dip=curves.value(r,'dipole')
 pot=curves.value(r,'u')+.5+2/(2*MU*r*r)
 off=np.full(len(r)-1,-1/(2*MU*h*h))
 e,v=eigh_tridiagonal(pot+1/(MU*h*h),off,select='v',select_range=(0,.22),check_finite=False)
 box=abs((w[0]*dip*np.sqrt(h))@v)**2/np.gradient(e)
 cont=np.array(fine['strength'])[0];energies=np.array(fine['energies'])
 checks=[]
 for E in [.003,.01,.03,.1]:
  aa=float(np.interp(E,e,box));bb=float(np.interp(E,energies,cont))
  checks.append(dict(E=E,box_strength=aa,scattering_strength=bb,relative_difference=aa/bb-1))
 assert max(abs(x['relative_difference']) for x in checks)<.04
 # Outer nuclear domain and unexpected u bound states.
 spectra=[]
 for L in [120.,240.]:
  r,rows,w=levels(curves,.02,L)
  off=np.full(len(r)-1,-1/(2*MU*.02**2))
  u=eigh_tridiagonal(curves.value(r,'u')+.5+1/(MU*.02**2),off,select='v',select_range=(-1,-1e-10),eigvals_only=True,check_finite=False)
  spectra.append(dict(L=L,levels=rows,u_J0_bound_energies=u.tolist()))
 assert len(spectra[0]['levels'])==len(spectra[1]['levels'])==23
 assert max(abs(a['D']-b['D']) for a,b in zip(spectra[0]['levels'],spectra[1]['levels']))<1e-7
 rates=Rates(BASE/'run_refine/results.json')
 # Independent rate table interpolation and missed endpoint diagnostic.
 ratecheck=[]
 for T in [6.4e-8,1e-6,.001,.03]:
  en=rates.en;omega=en[None,:]+rates.D[:,None];q=omega**3*rates.S*np.exp(-en[None,:]/T)
  direct=4/3*rates.deg*(2*np.pi/(100*101/201))**1.5*T**-1.5*np.trapz(q,en,axis=1)
  k,_=rates.at(T)
  # First low-energy decade tests threshold-tail contribution, not exact omitted integral.
  low=en<10*en[0];high=en>1.
  ratecheck.append(dict(T=T,interpolation_relative_error=float(abs(sum(direct)/sum(k[1:])-1)),first_decade_integral_fraction=float(sum(np.trapz(q[:,low],en[low],axis=1))/sum(np.trapz(q,en,axis=1))),above_one_integral_fraction=float(sum(np.trapz(q[:,high],en[high],axis=1))/sum(np.trapz(q,en,axis=1)))))
 original=json.loads((BASE/'run_extend/results.json').read_text());eligible=[r for r in original['rows'] if r['applicable']]
 chosen=max(eligible or original['rows'],key=lambda r:r['states'][2]['molecular_mass_fraction'])
 tighter=[parcel(rates,chosen['alpha'],chosen['mass_eV'],Mb,b,tol=2e-10) for Mb,b in PROFILES]
 timecheck=dict(parameters=[chosen['alpha'],chosen['mass_eV']],relative_fraction_change=[float(abs(s['molecular_mass_fraction']/o['molecular_mass_fraction']-1)) for s,o in zip(tighter,chosen['states'])],states=tighter)
 assert max(timecheck['relative_fraction_change'])<.001
 valid_T=rates.Ts<=.05
 rmax_valid=float(max(rates.ks[valid_T,1:].sum(axis=1)/rates.ks[valid_T,0]))
 from scipy.special import lambertw
 cap_valid=float(201/101*rmax_valid*lambertw(1/rmax_valid).real)
 out=dict(valid_temperature_sampled_rate_ratio_max=rmax_valid,conditional_valid_temperature_mass_cap=cap_valid,convergence=conv,independent_box_normalization=checks,nuclear_domains=spectra,rate_coverage=ratecheck,timestep_refinement=timecheck)
 Path(args.output).write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:v for k,v in out.items() if k not in ['nuclear_domains','timestep_refinement']},indent=2));print('time refinement',timecheck['parameters'],timecheck['relative_fraction_change'])
if __name__=='__main__':main()
