"""Hydrogen-only Peebles/RECFAST-like laboratory; NOT a multilevel CMB likelihood.
Writes scientific JSON to supplied output directory, default this directory.
"""
import json,sys,hashlib,platform,subprocess
from pathlib import Path
import numpy as np
import scipy
from scipy.integrate import solve_ivp, cumulative_trapezoid, quad
from scipy.optimize import brentq
from scipy.special import zeta
HERE=Path(__file__).resolve().parent; ROOT=HERE.parents[2]
OUT=Path(sys.argv[1]).resolve() if len(sys.argv)>1 else HERE
c=299792458.; G=6.67430e-11; kb=1.380649e-23; hp=6.62607015e-34; me=9.1093837015e-31; mh=1.6735575e-27
sigma=6.6524587321e-29; arad=7.5657e-16; ev=1.602176634e-19; T0=2.7255; H100=100000/3.085677581491367e22
wb=.02237; wm=.02237+.1200+.00064; h=.6736; wr=2.47282e-5*(T0/2.7255)**4*(1+.22710731766*3.046); wl=h*h-wm-wr; Yp=.245
chi=13.598434599702*ev; E2=chi/4; E21=3*chi/4; lam=hp*c/E21; Lambda=8.22458
rhob0=3*H100**2*wb/(8*np.pi*G); nH0=(1-Yp)*rhob0/mh; ng0=16*np.pi*zeta(3)*(kb*T0/(hp*c))**3
etaH=nH0/ng0; eta=rhob0/(mh*ng0); fHe=Yp/(4*(1-Yp))
def Hbase(z): return H100*np.sqrt(wr*(1+z)**4+wm*(1+z)**3+wl)
def nH(z):return nH0*(1+z)**3
def saha(T, dens=None):
    dens=etaH*16*np.pi*zeta(3)*(kb*T/(hp*c))**3 if dens is None else dens
    S=(2*np.pi*me*kb*T/hp**2)**1.5*np.exp(-chi/(kb*T))/dens
    return 2/(1+np.sqrt(1+4/S)) if S>0 else 0.
def tail(q): return quad(lambda t:t*t*np.exp(-t)/(-np.expm1(-t)),q,np.inf,epsabs=1e-30)[0]/(2*zeta(3))
Thalf=brentq(lambda T:saha(T)-.5,2500,6000); qhalf=chi/(kb*Thalf)
qtail=brentq(lambda q:np.log(tail(q)/etaH),15,40)
checks={}
def check(n,b):checks[n]=bool(b);print(('PASS ' if b else 'FAIL ')+n)
check('Saha half reconstruction',abs(saha(Thalf)-.5)<1e-10)
check('exact photon-tail half ionized fraction <<1 per H',tail(qhalf)/etaH<1e-5)
check('tail polynomial omitted in older proxy matters',tail(qtail)/ (np.exp(-qtail)/(2*zeta(3)))>500)
# Exact implicit Saha derivative finite-difference control using changed etaH.
def half_eta(eta_new):
 return brentq(lambda T: (2*np.pi*me*kb*T/hp**2)**1.5*np.exp(-chi/(kb*T))/(eta_new*16*np.pi*zeta(3)*(kb*T/(hp*c))**3)-.5,2500,6000)
dlog=(np.log(half_eta(etaH*1.0001))-np.log(half_eta(etaH/1.0001)))/(2*np.log(1.0001))
check('Saha logarithmic density sensitivity',abs(dlog-1/(qhalf-1.5))<1e-9)
ZHI=2200.; ZLO=50.; zz=np.linspace(ZLO,ZHI,8601)
def solve(label,Hscale=1.,clock=1.,F=1.,twophoton=1.,escape=1.,tol=2e-8):
 def quantities(z,xx,Tm):
    T=T0*(1+z); nn=nH(z); HH=Hbase(z)*Hscale*clock
    tt=max(Tm,1.)/1e4
    alpha=clock*F*1e-19*4.309*tt**(-.6166)/(1+.6703*tt**.5300)
    # Detailed balance evaluates alpha at radiation temperature; do not reuse alpha(Tm).
    tr=T/1e4; alpha_r=clock*F*1e-19*4.309*tr**(-.6166)/(1+.6703*tr**.5300)
    beta=alpha_r*(2*np.pi*me*kb*T/hp**2)**1.5*np.exp(-E2/(kb*T))
    NN=nn*max(1-xx,1e-20)
    resc=escape*8*np.pi*HH/(lam**3*NN)
    cc=(clock*twophoton*Lambda+resc)/(clock*twophoton*Lambda+resc+beta)
    return T,nn,HH,alpha,beta,cc,resc
 def rhs(z,v):
    xx,Tm=v; T,nn,HH,alpha,beta,cc,_=quantities(z,xx,Tm)
    dx=cc*(nn*alpha*xx*xx-beta*(1-xx)*np.exp(-E21/(kb*T)))/(HH*(1+z))
    comp=8*(clock*sigma)*arad*T**4*xx/(3*me*c*(1+fHe+xx))
    dT=2*Tm/(1+z)+comp*(Tm-T)/(HH*(1+z))
    return [dx,dT]
 sol=solve_ivp(rhs,[ZHI,ZLO],[saha(T0*(1+ZHI),nH(ZHI)),T0*(1+ZHI)],method='Radau',rtol=tol,atol=[tol*1e-4,tol],dense_output=True,max_step=5.)
 if not sol.success:raise RuntimeError(sol.message)
 xe,Tm=sol.sol(zz); HH=Hbase(zz)*Hscale*clock
 opacity=nH(zz)*xe*(clock*sigma)*c/(HH*(1+zz))
 tau=cumulative_trapezoid(opacity,zz,initial=0)
 # Missing residual optical depth below z=50; bounds reported, no reionization modeled.
 R=3*rhob0*c*c/(4*arad*T0**4)/(1+zz)
 td=cumulative_trapezoid(opacity/R,zz,initial=0)
 gz=opacity*np.exp(-tau)
 geta=nH(zz)*xe*(clock*sigma)*c/(1+zz)*np.exp(-tau)
 def at1(t):return float(np.interp(1,t,zz))
 ip=int(np.argmax(geta)); peak=zz[ip]; gh=geta[ip]/2
 ilo=np.flatnonzero(geta[:ip]<gh)[-1]; ihi=ip+np.flatnonzero(geta[ip:]<gh)[0]
 lo=np.interp(gh,geta[ilo:ilo+2],zz[ilo:ilo+2]); hi=np.interp(gh,geta[ihi-1:ihi+1][::-1],zz[ihi-1:ihi+1][::-1])
 zhalf=np.interp(.5,xe,zz)
 vals={}
 for z in (1600,1400,1200,1100,1000,800,500,200,50):
    xx,tm=sol.sol(z); t,nn,hh,al,be,cc,re=quantities(z,xx,tm)
    vals[str(z)]={'xe':float(xx),'Tm':float(tm),'C':float(cc),'beta_s':float(be),'Lambda_s':clock*twophoton*Lambda,'escape_s':float(re),'nH_alpha_over_H':float(nn*al/hh),'Lambda_over_H':float(clock*twophoton*Lambda/hh)}
 result={'label':label,'half_ionization_z':float(zhalf),'z_tau1_no_reion_z50_cutoff':at1(tau),'z_drag_tau1_z50_cutoff':at1(td),'z_visibility_conformal_peak':float(peak),'z_visibility_redshift_density_peak':float(zz[np.argmax(gz)]),'visibility_conformal_FWHM_z':float(hi-lo),'visibility_half_max_z':[float(lo),float(hi)],'xe_z50':float(xe[0]),'xe_grid_bounds':[float(xe.min()),float(xe.max())],'sampled':vals,'nfev':sol.nfev,'max_step':5,'rtol':tol}
 return result,xe,Tm
results={}; arrays={}
for label,kw in [('baseline',{}),('H_plus10',{'Hscale':1.1}),('H_minus10',{'Hscale':.9}),('no_two_photon',{'twophoton':0.}),('no_Lya_escape',{'escape':0.}),('F114',{'F':1.14}),('common_clock_plus10',{'clock':1.1}),('tight_tolerance',{'tol':2e-10})]:
 r,x,t=solve(label,**kw);results[label]=r;arrays[label]=x
 print(label,'z_tau1',r['z_tau1_no_reion_z50_cutoff'],'zpeak',r['z_visibility_conformal_peak'],'FWHM',r['visibility_conformal_FWHM_z'],'x200',r['sampled']['200']['xe'])
check('physical ionization interval all controls',all(r['xe_grid_bounds'][0]>0 and r['xe_grid_bounds'][1]<1.000001 for r in results.values()))
check('both ground-state channels contribute',results['no_two_photon']['sampled']['1100']['xe']>results['baseline']['sampled']['1100']['xe'] and results['no_Lya_escape']['sampled']['1100']['xe']>results['baseline']['sampled']['1100']['xe'])
check('common clock exact degeneracy numerical',np.max(abs(arrays['baseline']-arrays['common_clock_plus10']))<2e-7)
check('tight tolerance xe convergence',np.max(abs(arrays['baseline']-arrays['tight_tolerance']))<2e-7)
check('saha earlier than kinetic half ionization',Thalf/T0-1>results['baseline']['half_ionization_z'])
check('drag is later than photon tau1',results['baseline']['z_drag_tau1_z50_cutoff']<results['baseline']['z_tau1_no_reion_z50_cutoff'])
check('visibility width distinct from epoch gap',abs(results['baseline']['visibility_conformal_FWHM_z'])>3*abs(results['baseline']['z_drag_tau1_z50_cutoff']-results['baseline']['z_tau1_no_reion_z50_cutoff']))
# Local exact C-factor sensitivities, finite difference independent checks.
local=results['baseline']['sampled']['1100']; beta=local['beta_s']; resc=local['escape_s']; L=Lambda
CC=lambda a,h:(L+h*resc)/(L+h*resc+a*beta)
epssens=1e-4
sens_a=(np.log(1.0001*CC(1.0001,1))-np.log(CC(1/1.0001,1)/1.0001))/(2*np.log(1.0001))
sens_H=(np.log(CC(1,1.0001)/1.0001)-np.log(CC(1,1/1.0001)*1.0001))/(2*np.log(1.0001))
exact_a=CC(1,1); exact_H=-1+resc*beta/((L+resc)*(L+resc+beta))
check('local alphaB bottleneck sensitivity equals C',abs(sens_a-exact_a)<1e-9)
check('local H sensitivity includes Lyalpha escape',abs(sens_H-exact_H)<1e-9)
# Finite z=0..50 omitted residual opacity is bounded with x <= x50 (no reionization).
x50=results['baseline']['xe_z50']
missing_tau_bound=quad(lambda z:nH(z)*x50*sigma*c/(Hbase(z)*(1+z)),0,50)[0]
inputs=['fable_independent_2026/L37_RECOMBINATION.md','fable_independent_2026/L182_recombination_kernel_solver.py','fable_independent_2026/L183_class_kernel_recombination.py','real_research/reviews/mi_recombination_why_2026.py','real_research/reviews/cmb_inertia_recombination.py']
inputs += [str(p.relative_to(ROOT)) for p in sorted((HERE/'sources').glob('*')) if p.is_file()]
record={'checks':checks,'hydrogen_eta':etaH,'baryon_eta_approx_mass_mH':eta,'photon_entropy_per_baryon_k':2*np.pi**4/(45*zeta(3))/eta,'Saha':{'Thalf_K':Thalf,'zhalf':Thalf/T0-1,'chi_over_kThalf':qhalf,'ionizing_blackbody_photons_per_H_at_half':tail(qhalf)/etaH,'tail_inventory_crossing_q':qtail,'tail_inventory_crossing_T':chi/(kb*qtail),'dlnT_half_dlnetaH':dlog,'dlnT_half_dlnalphaEM':2*qhalf/(qhalf-1.5)},'cosmology':{'omega_b':wb,'omega_m':wm,'omega_r':wr,'h':h,'Yp':Yp,'T0':T0,'massive_neutrino_note':'0.00064 treated as matter; N_eff=3.046 treated as radiation, slight early double counting of 0.06eV mass density, not exact Planck neutrino thermodynamics'},'runs':results,'local_sensitivities_z1100':{'dln_net_rate_dln_alphaB':exact_a,'dln_net_rate_dln_H':exact_H},'missing_tau_zbelow50_upper_bound_no_reion':missing_tau_bound,'common_clock_max_xe_error':float(np.max(abs(arrays['baseline']-arrays['common_clock_plus10']))),'tight_tolerance_max_xe_error':float(np.max(abs(arrays['baseline']-arrays['tight_tolerance']))),'provenance':{'head':subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),'python':sys.version,'numpy':np.__version__,'scipy':scipy.__version__,'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'input_sha256':{p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in inputs}},'scope':'Hydrogen-only effective three-level toy, helium electrons omitted; no multilevel or CMB fit; no extra energy injection or reionization.'}
(OUT/'atomic_results.json').write_text(json.dumps(record,indent=2)+'\n')
sys.exit(0 if all(checks.values()) else 1)
