"""Declared hard-wall approximation to unresolved logarithmic-barrier turns.

The cutoff is a numerical model parameter, NOT the exact original Hamiltonian.
Within the domain the original forces are used. Elastic events preserve energy.
"""
import json, sys, ctypes
from pathlib import Path
import numpy as np
from scipy.integrate import solve_ivp

p = Path(__file__).parent
source = (p/'reciprocal_collapse_v2.py').read_text()
body = source.split(' E0=')[0].split('for N,h in [(32,.000125),(64,.0000625)]:')[1]
lib=ctypes.CDLL(str((p/'collapse_force.dylib').resolve()))
lib.collapse_rhs.argtypes=[ctypes.c_int,ctypes.c_double,ctypes.POINTER(ctypes.c_double),ctypes.POINTER(ctypes.c_double)]
lib.collapse_rhs.restype=None
rows = []
for N, eps, tol in [(512,1e-08,2e-11)]:
    ns = {'N':N, 'np':np}
    exec('\n'.join(line[1:] if line.startswith(' ') else line for line in body.splitlines()),ns)
    m,w,dm = ns['m'],ns['w'],ns['dm']
    energy = ns['energy']; floor = np.sqrt(m/(1-eps))
    y = np.r_[ns['r'],ns['B'],ns['v'],ns['V']]
    E0 = energy(y[:N],y[N+1:-1],y[N],y[-1])
    def rhs(t,y):
        r,B,v,V = y[:N],y[N],y[N+1:-1],y[-1]
        vol = np.diff(np.r_[0,r**3])/3
        pressure = .005*(dm/np.maximum(vol,1e-20))**2
        q = np.minimum(m/r**2,1-eps/2)
        a = r*r*(pressure-np.r_[pressure[1:],0])/w+q*q/(1-q)-np.where(r<B,r/B**3,1/r**2)
        deriv = np.where(r<B,1.5*(B*B-r*r)/B**4,0)
        ab = (.6/B**3-.6/B**2-np.sum(w*deriv)-.75*dm/B**2)/.6
        return np.r_[v,V,a,ab]
    reference_rhs=rhs
    def rhs(t,y):
        out=np.empty_like(y)
        lib.collapse_rhs(N,eps,y.ctypes.data_as(ctypes.POINTER(ctypes.c_double)),out.ctypes.data_as(ctypes.POINTER(ctypes.c_double)))
        return out
    force_error=float(np.max(abs(rhs(0,y)-reference_rhs(0,y))/(1+abs(reference_rhs(0,y)))))
    assert force_error<1e-12
    def event(t,y): return float(np.min(y[:N]-floor))
    event.terminal=True; event.direction=-1
    events=[event]
    t=0.; sample_index=0; samples=[]; reflections=[]; failure=None
    while t<30 and len(reflections)<10000:
        grid=np.arange(sample_index,301,dtype=float)/10
        sol=solve_ivp(rhs,(t,30),y,method='DOP853',rtol=tol,atol=tol*.01,
                      events=events,t_eval=grid,dense_output=False,max_step=.025)
        if len(sol.t):
            for tt,z in zip(sol.t,sol.y.T):
                r=z[:N]
                samples.append(dict(radii=r.tolist(),velocities=z[N+1:-1].tolist(),
                    mass_inside_3=float(np.interp(3,np.r_[0,r],np.r_[0,m])),
                    mass_inside_5=float(np.interp(5,np.r_[0,r],np.r_[0,m])),
                    t=float(tt),B=float(z[N]),half=float(np.interp(.5,m,r)),edge=float(r[-1]),
                    energy=energy(r,z[N+1:-1],z[N],z[-1]),max_q=float(max(m/r**2)),
                    min_gap=float(min(np.diff(np.r_[0,r])))))
            sample_index+=len(sol.t)
        if not sol.success:
            failure=sol.message
            if len(sol.t): t=float(sol.t[-1]); y=sol.y[:,-1].copy()
            break
        if not len(sol.t_events[0]):
            t=30.;y=sol.y[:,-1].copy();break
        t=float(sol.t_events[0][-1]);y=sol.y_events[0][-1].copy()
        j=int(np.argmin(y[:N]-floor))
        before=energy(y[:N],y[N+1:-1],y[N],y[-1]);y[N+1+j]*=-1
        after=energy(y[:N],y[N+1:-1],y[N],y[-1])
        reflections.append(dict(t=t,node=j,speed=float(y[N+1+j]),energy_jump=after-before))
        print(json.dumps(dict(N=N,event_segment_end=t,events=len(reflections))),flush=True)
    if t<30 and failure is None: failure='event budget'
    row=dict(initial_force_comparison=force_error,N=N,epsilon=eps,tolerance=tol,final_time=t,failure=failure,initial_energy=E0,
             final_state=y.tolist(),samples=samples,reflections=reflections,
             max_energy_error=max(abs(s['energy']-E0) for s in samples))
    rows.append(row)
    Path(sys.argv[1]).write_text(json.dumps(dict(status="partial",rows=rows),indent=2))
    print(json.dumps({k:row[k] for k in ['N','epsilon','tolerance','final_time','failure','max_energy_error']}),flush=True)
checks=dict(completed=all(r['failure'] is None and r['final_time']==30 for r in rows),
    energy=all(r['max_energy_error']<1e-4 for r in rows),
    domain=all(s['max_q']<1 and s['min_gap']>0 for r in rows for s in r['samples']),
    elastic=all(e['energy_jump']==0 for r in rows for e in r['reflections']))
out=dict(checks=checks,all_pass=all(checks.values()),rows=rows,
    scope='Hard-wall numerical approximation; cutoff, integration and spatial comparisons required; no exact barrier or permanent bound-object claim.')
Path(sys.argv[1]).write_text(json.dumps(out,indent=2));sys.exit(0 if out['all_pass'] else 1)
