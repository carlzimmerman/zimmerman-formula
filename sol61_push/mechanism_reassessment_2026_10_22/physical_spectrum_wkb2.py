"""Free spectator production on a declared smooth inflation-to-radiation history.
No occupied parent; background and minimal curvature coupling are inputs.
"""
import json,sys
from pathlib import Path
import numpy as np
from scipy.integrate import solve_ivp,simpson

def basis(N,k,mass):
    def W(n):
        a=np.exp(n);H=1/(1+a*a);eps=2*a*a/(1+a*a);ah=a*H
        om=np.sqrt(k*k+mass*mass*a*a);on=mass*mass*a*a/om
        onn=2*mass*mass*a*a/om-mass**4*a**4/om**3
        delta=-ah*ah*(2-eps)-.5*ah*ah*(onn+(1-eps)*on)/om+.75*(ah*on/om)**2
        return om+delta/(2*om)
    a=np.exp(N);H=1/(1+a*a);h=1e-4
    return W(N),a*H*(W(N+h)-W(N-h))/(2*h)

def mode(k,mass,early,late,tol):
    # H_inf=1, a=exp(N), H=1/(1+a²); epsilon=-d ln H/dN.
    start=min(-2.,np.log(k/early)); end=.5*np.log(1/late-1)
    a=np.exp(start);H=1/(1+a*a);omega,omega_prime=basis(start,k,mass)
    u=1/np.sqrt(2*omega)+0j
    up=(-1j*omega-omega_prime/(2*omega))*u
    def rhs(N,y):
        a=np.exp(N);H=1/(1+a*a);eps=2*a*a/(1+a*a)
        return [y[1],-(1-eps)*y[1]-(k*k/(a*H)**2+(mass/H)**2-(2-eps))*y[0]]
    s=solve_ivp(rhs,(start,end),[u,up/(a*H)],method='DOP853',rtol=tol,atol=tol*.001)
    a=np.exp(end);H=1/(1+a*a);omega,omega_prime=basis(end,k,mass)
    u,un=s.y[:,-1];up=a*H*un
    beta=(omega*u-1j*(up+omega_prime/(2*omega)*u))/np.sqrt(2*omega)
    return float(abs(beta)**2),float(-2*np.imag(u.conjugate()*up)),bool(s.success)

rows=[]
for count,early,late,tol in [(121,50.,.01,2e-10),(241,100.,.005,2e-11)]:
    k=np.geomspace(1e-5,10.,count);a=np.sqrt(1/late-1);species=[]
    for mass in [1.,2*np.sqrt(1+.02**2)]:
        vals=[mode(x,mass,early,late,tol) for x in k]
        occupation=np.array([v[0] for v in vals]);measure=k**3*occupation
        integral=simpson(measure,x=np.log(k))
        ncom=integral/np.pi**2 # both particle and antiparticle for complex field
        speed2=k*k/(k*k+(a*mass)**2)
        species.append(dict(mass=mass,k=k.tolist(),occupation=occupation.tolist(),
            n_comoving=ncom,n_physical=ncom/a**3,
            rms_speed=float(np.sqrt(simpson(measure*speed2,x=np.log(k))/integral)),
            low_tail_fraction=float(simpson(measure[k<=1e-3],x=np.log(k[k<=1e-3]))/integral),
            high_tail_fraction=float(simpson(measure[k>=5],x=np.log(k[k>=5]))/integral),
            max_wronskian_error=max(abs(v[1]-1) for v in vals),solved=all(v[2] for v in vals)))
        print(json.dumps({k:v for k,v in species[-1].items() if k not in ['k','occupation']}),flush=True)
    # Illustrative MeV benchmark, full radiation thermalization and conserved entropy.
    mgev=.001;Mpl=2.435e18;gstar=106.75
    temperature=(90/(np.pi**2*gstar))**.25*np.sqrt(Mpl*late*mgev)
    entropy=2*np.pi**2/45*gstar*temperature**3
    neff=(species[0]['n_physical']+2*species[1]['n_physical'])*mgev**3
    yield_eff=neff/entropy
    rows.append(dict(count=count,early_frequency_ratio=early,late_H=late,tolerance=tol,a=a,species=species,
        temperature_GeV=temperature,yield_if_all_X_decay=yield_eff,
        target_yield=4.37e-10/mgev,abundance_fraction=yield_eff/(4.37e-10/mgev)))
checks=dict(solved=all(s['solved'] for r in rows for s in r['species']),
    wronskian=all(s['max_wronskian_error']<1e-3 for r in rows for s in r['species']),
    abundance_refinement=abs(rows[0]['yield_if_all_X_decay']/rows[1]['yield_if_all_X_decay']-1)<.05,
    spectral_edges=all(s['low_tail_fraction']<.02 and s['high_tail_fraction']<.01 for r in rows for s in r['species']))
out=dict(checks=checks,all_pass=all(checks.values()),rows=rows,
    scope='Linear minimal spectator, H_inf=m_Phi, specified background and vacuum. MeV mapping and radiation entropy are assumptions; no interacting production or identification with the polarization medium.')
Path(sys.argv[1]).write_text(json.dumps(out,indent=2));sys.exit(0 if out['all_pass'] else 1)
