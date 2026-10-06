"""Ported hydrogen laboratory on the action-admitted conserved FRW branch.
No multilevel atom, reionization, or CMB likelihood. See provenance.json.
"""
import json,sys,hashlib
from pathlib import Path
import numpy as np
from scipy.integrate import solve_ivp,cumulative_trapezoid,quad
from scipy.special import zeta
c=299792458.; G=6.67430e-11; kb=1.380649e-23; hp=6.62607015e-34; me=9.1093837015e-31; mh=1.6735575e-27
sigma=6.6524587321e-29; arad=7.5657e-16; ev=1.602176634e-19; T0=2.7255; H100=100000/3.085677581491367e22
wb=.02237; wc=.1200; h=.6736; wr=2.47282e-5*(1+.22710731766*3.046); wl=h*h-wb-wc-wr; Yp=.245
chi=13.598434599702*ev; E2=chi/4; E21=3*chi/4; lam=hp*c/E21; Lambda=8.22458
rhob0=3*H100**2*wb/(8*np.pi*G); nH0=(1-Yp)*rhob0/mh; ng0=16*np.pi*zeta(3)*(kb*T0/(hp*c))**3
etaH=nH0/ng0; fHe=Yp/(4*(1-Yp)); ZHI=2200.; ZLO=50.; zz=np.linspace(ZLO,ZHI,8601)
wm=wb+wc; vacuum_scale=1.
def Hbase(z):return H100*np.sqrt(wr*(1+z)**4+wm*(1+z)**3+vacuum_scale*wl)
def nH(z):return nH0*(1+z)**3

def saha(T, dens=None):
    dens=etaH*16*np.pi*zeta(3)*(kb*T/(hp*c))**3 if dens is None else dens
    S=(2*np.pi*me*kb*T/hp**2)**1.5*np.exp(-chi/(kb*T))/dens
    return 2/(1+np.sqrt(1+4/S)) if S>0 else 0.

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
def main():
 global wm,vacuum_scale,nH0
 control=sys.argv[2] if len(sys.argv)>2 else "none"
 if control=="cold_is_hydrogen":nH0*= (wb+wc)/wb
 out=Path(sys.argv[1]);out.mkdir(parents=True,exist_ok=True)
 results={}; arrays={};checks={}
 def check(name,value):checks[name]=bool(value); print(('PASS ' if value else 'FAIL ')+name)
 for label,matter,vscale,tol in [('cold_reference',wb+wc,1.,2e-8),('admitted_baryon_only',wb,1.,2e-8),('baryon_tight',wb,1.,2e-10),('baryon_vacuum_double',wb,2.,2e-8)]:
  wm=(wb+wc if control=="stale_H" else matter);vacuum_scale=vscale
  r,x,t=solve(label,tol=tol); results[label]=r; arrays[label]=x
  astar=1/(1+r['z_visibility_conformal_peak']); rb0=3*rhob0*c*c/(4*arad*T0**4)
  def integrand(a):return c/(H100*np.sqrt(3*(1+rb0*a))*np.sqrt(wr+wm*a+vscale*wl*a**4))
  r['sound_horizon_at_peak_Mpc']=quad(integrand,0,astar,epsabs=1e9,epsrel=1e-10)[0]/3.085677581491367e22
  r['H0_km_s_Mpc']=100*np.sqrt(wr+matter+vscale*wl)
  r['omitted_tau_below50_upper_bound']=quad(lambda z:nH(z)*r['xe_z50']*sigma*c/(Hbase(z)*(1+z)),0,50)[0]
  print(label,r['half_ionization_z'],r['z_visibility_conformal_peak'],r['sound_horizon_at_peak_Mpc'],r['sampled']['200']['xe'])
 wm=wb;vacuum_scale=1.
 z=np.linspace(800,1500,701);fv=wl/(wr*(1+z)**4+wb*(1+z)**3+wl)
 dlogH=.5*fv;eps=1e-2
 vacuum_scale=np.exp(eps);Hp=Hbase(z);vacuum_scale=np.exp(-eps);Hm=Hbase(z);vacuum_scale=1.
 # subtract near-unity accurately; finite precision absolute rather than relative gate
 fd=np.log(Hp/Hm)/(2*eps)
 check('vacuum log derivative analytic',np.max(abs(fd-dlogH))<5e-13)
 check('vacuum H sensitivity below 1e-8 across recombination',max(dlogH)<1e-8)
 check('both backgrounds neutralize without atom density substitution',all(results[k]['sampled']['200']['xe']<.001 for k in ['cold_reference','admitted_baryon_only']))
 check('ionization fraction physical',all(0<r['xe_grid_bounds'][0] and r['xe_grid_bounds'][1]<1.000001 for r in results.values()))
 check('tight tolerance transport convergence',max(abs(arrays['admitted_baryon_only']-arrays['baryon_tight']))<2e-7)
 check('vacuum doubling transport weak response',max(abs(arrays['admitted_baryon_only']-arrays['baryon_vacuum_double']))<2e-7)
 check('removing cold changes sound horizon substantially',results['admitted_baryon_only']['sound_horizon_at_peak_Mpc']>1.1*results['cold_reference']['sound_horizon_at_peak_Mpc'])
 check('reference cold mass never enters hydrogen density',abs(nH0-(1-Yp)*3*H100**2*wb/(8*np.pi*G*mh))<1e-14)
 a0=9.3603e-11;Lambdageo=3*H100**2*wl/c**2;A=2*Lambdageo*c**4/a0**2
 record={'checks':checks,'runs':results,'parameters':{'omega_b':wb,'omega_c_reference':wc,'omega_r':wr,'omega_lambda_fixed':wl,'Yp':Yp,'T0':T0,'nH0_m3':nH0,'neutrinos':'massless Neff=3.046 only; no massive neutrino matter term'},'vacuum_gate':{'z_range':[800,1500],'max_dlnH_dlnA_Qfixed':float(max(dlogH)),'Lambda_m_inverse2':Lambdageo,'declared_a0_m_s2':a0,'inferred_free_A_Q1_chi1':A,'target_A_for_32pi':64*np.pi,'selector':False},'max_xe_tolerance_error':float(max(abs(arrays['admitted_baryon_only']-arrays['baryon_tight']))),'max_xe_vacuum_doubling_error':float(max(abs(arrays['admitted_baryon_only']-arrays['baryon_vacuum_double']))),'scope':'Hydrogen three-level laboratory on admitted homogeneous projected-action branch with separately conserved ordinary matter. No new cold source, no perturbation transfer, no full CMB likelihood.'}
 (out/'results.json').write_text(json.dumps(record,indent=2)+'\n')
 np.savez_compressed(out/'histories.npz',z=zz,**arrays)
 return 0 if all(checks.values()) else 1
if __name__=='__main__':sys.exit(main())
