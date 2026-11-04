"""CT09 terminal masses/forces and genuine massless-scalar Coulomb couplings."""
import sys,os
sys.dont_write_bytecode=True
for key in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','VECLIB_MAXIMUM_THREADS'):os.environ[key]='1'
from pathlib import Path
import json,math,time,resource
import numpy as np
from scipy.integrate import quad
from scipy.linalg import eigvalsh
from network import build_model,adapt,DCOEF,E,G
BASE=Path(__file__).resolve().parent

def spectrum(x):
 d=build_model(x,E,E,G,vertices=False)
 RY=np.einsum('a,aij->ij',DCOEF/math.sqrt(30),d['R']);Q2=RY@RY
 QF=np.zeros((73,73),complex);QF[:49,:49]=Q2;QF[49:,49:]=Q2[1:25,1:25]
 CS=np.block([[Q2.real,-Q2.imag],[Q2.imag,Q2.real]])
 O=adapt(d['O'],d['mS2'],CS);U=adapt(d['U'],d['mF'],QF)
 return d,O,U,CS,QF

def derivatives(x):
 d,O,U,CS,QF=spectrum(x);h=1e-4
 dp=build_model(x+h,E,E,G,vertices=False);dm=build_model(x-h,E,E,G,vertices=False)
 HS=(dp['H']-dm['H'])/(2*h);MF=(dp['MF']-dm['MF'])/(2*h)
 mS=np.sqrt(np.maximum(d['mS2'],0));mslope=np.diag(O.T@HS@O)/(2*np.maximum(mS,1e-30));mslope[mS<1e-12]=0
 fslope=np.diag(U.T@MF@U).real.copy();fslope[d['mF']<1e-12]=0
 return np.r_[mS,d['mF']],np.r_[mslope,fslope]

def scalar_coulomb(x):
 d=build_model(x,E,E,G,vertices=True);RY=np.einsum('a,aij->ij',DCOEF/math.sqrt(30),d['R']);Q2=RY@RY;CS=np.block([[Q2.real,-Q2.imag],[Q2.imag,Q2.real]])
 O=adapt(d['O'],d['mS2'],CS);qs=np.einsum('ia,ia->a',O,CS@O).real;m=np.sqrt(np.maximum(d['mS2'],0))
 low=min(m[(qs>.1)&(m>1e-12)]);L=np.where((qs>.1)&(abs(m-low)<1e-9))[0];N=np.where((qs<.01)&(m<1e-12))[0]
 RS=d['O'].T@O;c=np.einsum('ia,jb,kc,ijk->abc',RS,RS,RS,d['cubic'],optimize=True)
 # Any pair-exchange potential norm <= sum_a ||C_LLa||^2/(16 pi m^2).
 vals=[float(np.linalg.norm(c[np.ix_(L,L,[a])][:,:,0],2)**2/(16*math.pi*low**2)) for a in N]
 return dict(x=x,charged_scalar_mass=low,charged_light_real_count=len(L),neutral_zero_real_count=len(N),alpha_scalar_exchange_norm_bound=sum(vals),alpha_per_neutral_mode=vals)

def main(out):
 start=time.monotonic();src=json.loads((BASE/'run_network001/result.json').read_text());rows=[]
 maxerr=0
 for r in src['cases']:
  mass,slope=derivatives(r['x']);parents=[]
  for p in r['neutral_parents']:
   daughters=[]
   for q in p['terminal_daughters']:
    i=q['index'];maxerr=max(maxerr,abs(mass[i]-q['mass']))
    daughters.append(dict(**q,dm_dx=float(slope[i]),rest_energy=float(q['expected_number']*mass[i]),NR_force=float(q['expected_number']*slope[i])))
   parents.append(dict(index=p['index'],mass=p['mass'],to_light_pair=p['to_light_pair'],terminal_daughters=daughters,terminal_charged_rest_energy=sum(q['rest_energy'] for q in daughters if q['charged']),terminal_neutral_rest_energy=sum(q['rest_energy'] for q in daughters if not q['charged']),terminal_charged_NR_force=sum(q['NR_force'] for q in daughters if q['charged']),terminal_neutral_NR_force=sum(q['NR_force'] for q in daughters if not q['charged'])))
  rows.append(dict(x=r['x'],parents=parents))
 I2=1.8030853547393915
 inner=lambda p:quad(lambda q:q*q/(math.exp(q)+1),0,p,epsabs=1e-11)[0]
 inv=2*quad(lambda p:p/(math.exp(p)+1)*inner(p),0,60,epsabs=1e-11)[0]/I2**2
 couplings=[scalar_coulomb(x) for x in (0,3,5,10,20,25,30)]
 checks=dict(endpoint_mass_rebuild=maxerr<1e-10,finite_scalar_couplings=all(math.isfinite(r['alpha_scalar_exchange_norm_bound']) for r in couplings),FD_inverse_relative_speed=0<inv<1)
 result=dict(claim_id='CT09_TERMINAL_FORCE_AND_COULOMB',checks=checks,cases=rows,coulomb_scalar_cases=couplings,FD_inverse_relative_speed_coefficient=inv,alpha_max_gauge=2.5*G*G/(4*math.pi),scope='d(m/mu)/d(X/mu) via Hellmann-Feynman, h=1e-4; NR force per original rest parent. No terminal momentum distribution; actual force gains m/E. Scalar exchange norm only tree-zero neutral modes, not all finite-range exchange. Frozen FD relative velocity coefficient exact NR isotropic angular reduction.',runtime_seconds=time.monotonic()-start,peak_rss_bytes_macos=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
 Path(out).write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:result[k] for k in ('checks','FD_inverse_relative_speed_coefficient','alpha_max_gauge','coulomb_scalar_cases','runtime_seconds')}));assert all(checks.values())
if __name__=='__main__':main(sys.argv[1])
