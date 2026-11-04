"""Deterministic comoving momentum-bin decay/cascade transport in Einstein RD.

No thermal relic distribution is imposed. Nonabelian collisionless companions
are an explicit envelope; neutral-scalar/Goldstino scatter is tested separately.
"""
import os,sys
sys.dont_write_bytecode=True
for k in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','VECLIB_MAXIMUM_THREADS'):os.environ[k]='1'
import json,math,time,resource,argparse
from pathlib import Path
import numpy as np
from scipy.special import roots_laguerre
from numpy.polynomial.legendre import leggauss
from scipy.interpolate import PchipInterpolator
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2]
MP=2.435e18;HB=6.582119569509066e-25;TG0=2.7255*8.617333262145e-14;TN0=TG0*(4/11)**(1/3)
H0=2.1842852410855023e-18*HB;RHOC=3*MP**2*H0**2;RHOCHI=.265*RHOC
MPC_GEV=3.0856775814913673e22/(299792458*HB)
KEYS=['SU3','SU2','U1','GG'];MULT={'SU3':8,'SU2':3,'U1':1}
def radiation_table():
    # Exact equilibrium electron integrals; instantaneous neutrino decoupling
    # while electrons are ultrarelativistic is the stated thermodynamic model.
    y,w=roots_laguerre(64);T=np.geomspace(TG0*.5,.03,1000);rho=[];aa=[]
    for t in T:
        z=.00051099895/t;en=np.sqrt(y*y+z*z)
        factor=np.exp(np.maximum(-745,y-en))/(1+np.exp(-en))
        re=4/(2*np.pi**2)*t**4*np.dot(w,y*y*en*factor)
        pe=4/(6*np.pi**2)*t**4*np.dot(w,y**4/en*factor)
        gs=2+45/(2*np.pi**2)*(re+pe)/t**4
        a=TG0/t*(2/gs)**(1/3)
        rr=np.pi**2/15*t**4+re+7*np.pi**2/40*(TN0/a)**4
        aa.append(a);rho.append(rr)
    idx=np.argsort(aa)
    loga=np.log(np.asarray(aa)[idx]);lr=np.log(np.asarray(rho)[idx]);lt=np.log(T[idx])
    return PchipInterpolator(loga,lr,extrapolate=True),PchipInterpolator(loga,lt,extrapolate=True)
RAD,TEMP=radiation_table()
def g_entropy(T):
    return (2*np.pi**2/45)*3.909090909090909*TG0**3
def scale_row(row,e):
    r=dict(row);s=e/row['e'];r['e']=e
    for key,powr in [('mu_GeV',2.5),('R_GeV',2),('m_sigma_GeV',4),('m_phase_GeV',4),('m32_GeV',5),('photino_GeV',5),('min_heavy_gap_GeV',3)]:r[key]=row[key]*s**powr
    r['gauginos_GeV']={k:v*s**5 for k,v in row['gauginos_GeV'].items()}
    from kernels import widths
    r['widths']=widths(r,r['logmass_slopes']);return r
def run_case(row,nq=480,dx=.035,angular=12,companion='collisionless',density_factor=1.,until=1.,save_spectrum=False):
    m=row['m_sigma_GeV'];ma=row['m_phase_GeV'];R=row['R_GeV'];mi={**row['gauginos_GeV'],'GG':row['m32_GeV']}
    w=row['widths'];Gs=w['sigma_total'];Ga=w['phase_total'];bs={k:v/Gs for k,v in w['sigma'].items()};ba={k:v/Ga for k,v in w['phase'].items()}
    nper=2*bs['U1']+4*bs['aa']*ba['U1'];N0=RHOCHI/mi['U1']/nper*density_factor
    # An actual initially cold mother is stipulated at 20 MeV. Its preparation
    # is a state input; a separate H=m misalignment test appears below.
    ai=TG0/.02*(4/11)**(1/3);xmin=math.log(ai);xmax=math.log(until)
    q=np.geomspace(ai*m*1e-10,2e-3,nq);lq=np.log(q);dl=lq[1]-lq[0]
    spec={k:np.zeros(nq) for k in KEYS};ph=np.zeros(nq);ns=1.;radq=0.;cross=np.zeros(2);travel=0.;maxfrac=0.;maxpre=0.;maxprod=0.;t=0.;energyerr=0.;neutralcontact=0.;maxfloquet=0.;samples={};chi_yield_by_time=[];maxoccupation=0.;maxnumbercheck=0.
    g=math.sqrt(29/200)*row['e'];Ymax=32*math.sqrt(24*row['e']**2+30*g*g)
    C6=32768*Ymax**4/(16*math.pi**2*row['min_heavy_gap_GeV']**2)
    z,zw=leggauss(angular);zw=zw/2;zz=z[None,:];zw=zw[None,:]
    nstep=math.ceil((xmax-xmin)/dx);xs=np.linspace(xmin,xmax,nstep+1)
    snapshots=[('BBN_100keV',TG0/.0001*(4/11)**(1/3)),('equality_benchmark',1/3401),('recombination_benchmark',1/1101)]
    xs=np.unique(np.r_[xs,[math.log(a) for _,a in snapshots if ai<a<until]])
    def deposit(arr,pp,nn):
        pp,nn=np.broadcast_arrays(np.asarray(pp),np.asarray(nn));pp=pp.ravel();nn=nn.ravel();sel=nn>0;pp=pp[sel];nn=nn[sel]
        if not len(nn):return
        frac=(np.log(np.maximum(pp,q[0]))-lq[0])/dl;idx=np.clip(frac.astype(int),0,nq-2)
        # Linear q interpolation conserves number and relativistic energy.
        f=np.clip((pp-q[idx])/(q[idx+1]-q[idx]),0,1)
        arr+=np.bincount(idx,weights=nn*(1-f),minlength=nq)+np.bincount(idx+1,weights=nn*f,minlength=nq)
    def calc(a):
        ep=np.sqrt(ma*ma+(q/a)**2);ener={k:np.sqrt(mi[k]**2+(q/a)**2) for k in KEYS}
        rh=N0/a**3*(ns*m+np.dot(ph,ep)+sum(np.dot(spec[k],ener[k]) for k in KEYS))+radq*N0/a**4
        rr=math.exp(float(RAD(math.log(a))));rest=.05*RHOC/a**3+.685*RHOC
        return ep,ener,rh,rr,math.sqrt((rh+rr+rest)/(3*MP**2))
    for lo,hi in zip(xs,xs[1:]):
        a=math.exp((lo+hi)/2);dd=hi-lo;ep,en,rh,rr,H=calc(a);dt=dd/H;t+=dt
        maxfrac=max(maxfrac,rh/rr)
        if a<1/3401:maxpre=max(maxpre,rh/rr)
        if ns>1e-6 or ph.sum()>1e-6:maxprod=max(maxprod,rh/rr)
        if ns>0 and ma<m/2:
            # Canonical Cartesian cubic; narrow-band redshift crossing check.
            # Only interpret for eta<<1, not the separate large primordial fit.
            Sigma=math.sqrt(2*N0*ns*m/a**3)/m;eta=(1-(ma/m)**2)*Sigma/(math.sqrt(2)*R)
            maxfloquet=max(maxfloquet,math.pi*eta*eta*m/(4*H*(1-4*(ma/m)**2)))
        # Exact exponential decay over a midpoint-H cell; phase source uses
        # half-before/half-after Strang insertion for its own decay.
        dns=ns*(-math.expm1(-min(745,Gs*dt)));ns-=dns
        for k in KEYS:
            p=math.sqrt(max(0,m*m/4-mi[k]**2));deposit(spec[k],a*p,2*dns*bs[k])
        if bs['aa']>0:deposit(ph,a*math.sqrt(max(0,m*m/4-ma*ma)),dns*bs['aa'])
        ep=np.sqrt(ma*ma+(q/a)**2);dn=ph*(-np.expm1(-np.minimum(745,Ga*ma/ep*dt)));ph-=dn
        active=dn>1e-35
        if np.any(active):
            ea=ep[active,None];pa=(q[active]/a)[:,None];number=dn[active,None]
            for k in KEYS:
                beta=math.sqrt(max(0,1-4*(mi[k]/ma)**2));ener=ea/2+pa/2*beta*zz
                mom=np.sqrt(np.maximum(0,ener*ener-mi[k]**2));deposit(spec[k],a*mom,2*number*ba[k]*zw)
        if bs['aa']>0:deposit(ph,a*math.sqrt(max(0,m*m/4-ma*ma)),dns*bs['aa'])
        # Transparent companion endpoints. The 'instant' endpoint converts
        # every companion's energy to hidden gauge radiation each step. It is
        # a budget envelope, not the solved nonabelian collision operator.
        if companion=='instant':
            for k in ['SU3','SU2']:radq+=a*np.dot(spec[k],en[k]);spec[k]*=0
        # Cross-section dimensional diagnostics for nonabelian self reactions.
        g=math.sqrt(29/200)*row['e'];alpha=g*g/(4*math.pi)
        for ii,k in enumerate(['SU3','SU2']):
            nk=spec[k].sum();emean=np.dot(spec[k],en[k])/max(nk,1e-300)
            cross[ii]+=N0/a**3*nk*alpha**2/max(emean**2,1e-300)*dt
        # Lift the explicit TP04 heavy-contact majorant to sub-gap energies;
        # E_bound=m_sigma covers every cascade daughter at production, and
        # replacing all hidden particles by that energy only overestimates it.
        # This is for that named local operator class, not all-order thermal QFT.
        ntot=N0/a**3*sum(spec[k].sum() for k in KEYS)
        neutralcontact+=ntot*338*C6*C6*m*m/math.pi*dt*spec['U1'].sum()/nper
        # Per helicity occupation f_j=n_j/(g*d^3q/(2pi)^3). A violation is
        # diagnostic failure of the classical source, not a degenerate relic.
        shell=(q*np.exp(dl/2))**3-(q*np.exp(-dl/2))**3
        ff=N0*spec['U1']*6*math.pi**2/(2*shell)
        maxoccupation=max(maxoccupation,float(ff.max()))
        # Occupation-weighted path integrated from each actual birth time.
        travel+=dt/a*np.dot(spec['U1'],(q/a)/np.sqrt(mi['U1']**2+(q/a)**2))
        for name,sa in snapshots:
            if abs(hi-math.log(sa))<1e-10:
                ep,en,rh,rr,H=calc(sa);pn=N0/sa**3*(np.dot(ph,(q/sa)**2/ep)+sum(np.dot(spec[k],(q/sa)**2/en[k]) for k in KEYS))+radq*N0/sa**4
                dn=pn/((7*np.pi**2/120)*(TN0/sa)**4)
                samples[name]=dict(a=sa,DeltaNeff_pressure_equivalent=dn,hidden_over_SM=rh/rr,phase_remaining_per_mother=float(ph.sum()),chi_produced_per_mother=float(spec['U1'].sum()),chi_mean_v=float(np.dot(spec['U1'],(q/sa)/en['U1'])/max(spec['U1'].sum(),1e-300)))
    ep,en,rh,rr,H=calc(until);nchi=spec['U1'].sum();Om={k:float(N0*np.dot(spec[k],en[k])/RHOC) for k in KEYS}
    abundance=N0*nchi*mi['U1']/RHOC;Fs=travel/max(nchi,1e-300)/MPC_GEV
    pp=q/mi['U1'];ww=spec['U1']/max(nchi,1e-300);cumulative=np.cumsum(ww);percentiles={str(x):float(np.interp(x,cumulative,pp)) for x in [.1,.5,.9]}
    # High-energy neutral Goldstino width is an unavoidable partial decay.
    F=row['mu_GeV']**2/math.sqrt(31);tau=HB*16*math.pi*F*F/mi['U1']**5;survival=math.exp(-4.3549488e17/tau)
    # Initial coherent-amplitude diagnostic at H=m. Harmonic misalignment
    # redshifts as matter; standard high-T degrees106.75 are explicit.
    Tosc=math.sqrt(m*MP/math.sqrt(math.pi**2*106.75/90));sosc=2*math.pi**2/45*106.75*Tosc**3;Yreq=N0/g_entropy(0)
    Sigma=math.sqrt(2*m*Yreq*sosc)/m;eta=Sigma/(math.sqrt(2)*R)
    Gamma=Gs;Tapprox=math.sqrt(Gamma*MP/math.sqrt(math.pi**2*3.36/90))
    result=dict(t=row['t'],e=row['e'],mchi_GeV=mi['U1'],m_sigma_GeV=m,m_phase_GeV=ma,companion_endpoint=companion,nper_expected=nper,nper_integrated=float(nchi),yield_normalization_relative_error=float(nchi/nper-1),initial_mother_Y=Yreq,initial_mother_number_GeV3=N0,initial_temperature_GeV=.02,initial_radial_fraction=float(N0*m/ai**3/math.exp(float(RAD(math.log(ai))))),max_hidden_to_SM=maxfrac,max_hidden_to_SM_before_equality=maxpre,max_hidden_to_SM_during_decays=maxprod,Omega_chi_rest=abundance,Omega_species_energy=Om,free_streaming_Mpc=float(Fs),free_streaming_below_1kpc=bool(Fs<.001),q_over_m_percentiles=percentiles,snapshots=samples,nonabelian_dimensional_optical_depth_SU3_SU2=list(map(float,cross)),neutral_heavy_contact_optical_depth_majorant=neutralcontact,maximum_phase_Floquet_cross_exponent_for_fitted_late_condensate=maxfloquet,unavoidable_Ward_partial_tau_s=tau,unavoidable_Ward_survival_13p8Gyr=survival,SM_comoving_entropy_change=0.,remaining_sigma=ns,remaining_phase=float(ph.sum()),H_today_over_reference=H/H0,primordial_harmonic_diagnostic=dict(H_equals_m_T_GeV=Tosc,Sigma_required_GeV=Sigma,Sigma_required_over_R=Sigma/R,eta_required=eta,maximum_small_amplitude_over_R=.01,small_misalignment_abundance_fraction=(.01*R/Sigma)**2,linear_Floquet_cross_exponent_at_H_m=math.pi*eta*eta/4,interpretation='If Sigma/R is large the linearized misalignment estimate is not a prediction; it demonstrates failure of this small-harmonic initial state'),decay_temperature_RD_control_GeV=Tapprox,time_steps=len(xs)-1,q_bins=nq,angular_nodes=angular)
    result['maximum_shell_occupation_per_helicity']=maxoccupation
    result['Pauli_classical_source_valid']=bool(maxoccupation<1)
    result['neutral_contact_diagnostic_revision']='v3 averages the named four-fermion majorant only over existing photinos and fermionic targets; v2 integrated it before daughter birth and was a deliberately loose non-applicability diagnostic'
    if save_spectrum:result['spectrum']={k:list(map(float,spec[k])) for k in KEYS};result['q_GeV']=list(map(float,q))
    return result
def main(out,mode):
    start=time.monotonic();rows=json.loads((HERE/'run_kernels/result.json').read_text())['rows'];results=[]
    if mode=='coarse':
        for row in rows:
            results.append(run_case(row,nq=480,dx=.035,angular=12,save_spectrum=True))
        for idx in [1,4,6]:results.append(run_case(rows[idx],nq=720,dx=.0175,angular=20,save_spectrum=False))
        for idx in [1,4,6]:results.append(run_case(rows[idx],nq=480,dx=.035,angular=12,companion='instant'))
    elif mode=='scaling':
        for idx in [1,4,6]:
            for e in [.004,.005,.006,.01]:results.append(run_case(scale_row(rows[idx],e),nq=480,dx=.035,angular=12))
    checks=dict(all_yields_conserved=max(abs(r['yield_normalization_relative_error']) for r in results)<.005,all_phases_decayed=max(r['remaining_phase'] for r in results)<1e-8,SM_entropy_explicit=all(r['SM_comoving_entropy_change']==0 for r in results),nonnegative_all=all(r['Omega_chi_rest']>0 and r['free_streaming_Mpc']>0 for r in results))
    result=dict(claim_id='GC03_RADIAL_CASCADE_'+mode,checks=checks,cases=results,runtime_seconds=time.monotonic()-start,peak_rss_bytes_macos=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,scope='Actual deterministic decay-source transport with exact two-body cascade boost and Einstein backreaction; no nonabelian collision operator, no finite SUGRA current completion')
    Path(out).write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(dict(checks=checks,runtime=result['runtime_seconds'],selected=[{k:r[k] for k in ['t','e','companion_endpoint','free_streaming_Mpc','initial_mother_Y','max_hidden_to_SM','Omega_species_energy','unavoidable_Ward_survival_13p8Gyr','primordial_harmonic_diagnostic']} for r in results]),indent=2));assert all(checks.values()),checks
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--out',required=True);p.add_argument('--mode',default='coarse');a=p.parse_args();main(a.out,a.mode)
