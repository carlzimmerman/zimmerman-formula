"""Offline monopole stellar-cohort stress test; not a live DF or accepted birth."""
import json,math,time,hashlib
from pathlib import Path
import numpy as np
from scipy.integrate import solve_ivp
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1]
cap=json.loads((ROOT/'sol61_push/cold_survey_capture_2026_10_24/capture_results.json').read_text())
G=.00430091;A0=9.3603e-11*3.085677581491367e10;results=[]
for tag in ['draco_hybrid','sextans_L4']:
    path=HERE/'runs'/f'{tag}.json';q=json.loads(path.read_text());un=q['physical'];gal=q['parameters']['galaxy']
    model=next(x for x in cap['models'] if x['name']==gal)
    rgrid=np.array(q['radial_grid']);hist=q['history'];times=np.array([h['t'] for h in hist]);cdfs=np.array([h['cdf'] for h in hist])
    aa=np.array([1.] if gal=='Draco' else [434.24183347957097,794.1886040039351])/ (1 if gal=='Draco' else un['Runit_pc'])
    sm=model['stellar_mass']/un['Munit_Msun'];a0=A0*un['Runit_pc']/un['Vunit_kms']**2
    def enc(t,r):
        i=max(0,min(len(times)-2,int(np.searchsorted(times,t)-1)));f=(t-times[i])/(times[i+1]-times[i])
        c=(1-f)*cdfs[i]+f*cdfs[i+1]
        return np.interp(r,rgrid,c,left=0,right=c[-1])
    def force(t,r):
        gn=sum(sm/len(aa)*r/(r*r+a*a)**1.5 for a in aa)
        baryon=.5*(gn+np.sqrt(gn*gn+4*a0*gn))
        return enc(t,r)/r**2+baryon
    for birth in [30.,80.]:
      for atr in aa:
        n=128;umax=6**3/(1+36)**1.5;u=(np.arange(n)+.5)/n*umax
        r0=atr/np.sqrt(u**(-2/3)-1);ell2=r0**3*force(birth,r0)
        def rhs(t,z):
            r=z[:n];vr=z[n:]
            return np.r_[vr,ell2/r**3-force(t,r)]
        end=times[-1];t_eval=np.linspace(birth,end,401)
        sol=solve_ivp(rhs,[birth,end],np.r_[r0,np.zeros(n)],method='DOP853',rtol=2e-7,atol=1e-9,t_eval=t_eval)
        assert sol.success and np.min(sol.y[:n])>0
        rr=sol.y[:n];vr=sol.y[n:];vv=vr*vr+ell2[:,None]/rr**2
        # Frozen initial monopole has exactly circular stationary orbits at r0.
        results.append(dict(tag=tag,galaxy=gal,birth_code_time=birth,birth_Myr=birth*un['tunit_Myr'],
            tracer_scale_pc=atr*un['Runit_pc'],late_median_radius_over_frozen=float(np.median(np.median(rr[:,301:],axis=0))/np.median(r0)),
            late_variance_trace_over_frozen=float(np.mean(vv[:,301:])/np.mean(ell2/r0**2)),
            initial_variance_trace_kms2=float(np.mean(ell2/r0**2)*un['Vunit_kms']**2/3),
            frozen_control='exact circular equilibrium in frozen monopole; no numerical frozen-orbit drift',
            accepted_birth=False,scope='counterfactual passive MONOPOLE cohort; full nonspherical force and backreaction absent',
            input_run_hash=hashlib.sha256(path.read_bytes()).hexdigest()))
(HERE/'stellar_response.json').write_text(json.dumps(dict(scope='stress diagnostic only, not a protected observed stellar population',results=results),indent=2)+'\n')
print(json.dumps(results,indent=2))
