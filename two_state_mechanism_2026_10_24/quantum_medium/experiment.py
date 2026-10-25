"""Cold two-component Bose Gaussian response; not a nonlinear galaxy solver."""
import argparse
import json
import numpy as np
from scipy.integrate import solve_ivp

G=6.67430e-11; HBAR=1.054571817e-34; C=299792458.
EVKG=1.7826619216279e-36; MSUN=1.98847e30; KPC=3.085677581491367e19
ETA=5.364
PROFILES=[(3e5,.3),(1e8,1.),(6e10,3.),(1e14,300.)]

def matrix(Q,eps,gravity=True):
    z=np.array([1.,-1/np.sqrt(eps)]);v=np.array([1.,np.sqrt(eps)])
    return np.diag([Q*Q,Q*Q/(eps*eps)])+np.outer(z,z)-(np.outer(v,v) if gravity else 0),z

def threshold(eps):
    a=eps*(1-eps*eps);b=eps*(1+eps)**2
    return np.sqrt(2*b/(a+np.sqrt(a*a+4*b)))

def spectrum(Q,eps,gravity):
    D,z=matrix(Q,eps,gravity)
    w2,e=np.linalg.eigh(D);r=(z@e)**2
    stable=bool(w2[0]>0)
    return dict(Q=float(Q),epsilon=eps,gravity=gravity,w2=w2.tolist(),
                dipole_residues=r.tolist(),stable=stable,
                positive_spectral_weights=(r/(2*np.sqrt(w2))).tolist() if stable else None)

def energy_test(Q,eps,rtol):
    D,z=matrix(Q,eps)
    x0=np.array([.2,-.1]);v0=np.array([.1,.3])
    def rhs(t,y): return np.r_[y[2:],-D@y[:2]]
    sol=solve_ivp(rhs,(0,1.),np.r_[x0,v0],method='DOP853',rtol=rtol,atol=rtol*.01,
                  t_eval=np.linspace(0,1,101))
    assert sol.success
    x,v=sol.y[:2],sol.y[2:]
    E=.5*np.sum(v*v,axis=0)+.5*np.sum(x*(D@x),axis=0)
    scale=.5*np.dot(v0,v0)+.5*np.linalg.norm(D)*np.dot(x0,x0)
    return dict(Q=Q,epsilon=eps,rtol=rtol,initial_energy=float(E[0]),
                max_energy_error_over_initial_positive_scale=float(np.max(abs(E-E[0]))/scale),
                final=sol.y[:,-1].tolist())

def checks():
    determinant_error=equal_error=sum_error=resolve_error=0.
    for eps in [.01,.1,1.]:
        for Q in [.001,.1,1.,10.]:
            D,z=matrix(Q,eps)
            t=Q*Q;formula=(t*t+eps*(1-eps*eps)*t-eps*(1+eps)**2)/eps**2
            determinant_error=max(determinant_error,abs(np.linalg.det(D)-formula)/max(1,abs(formula)))
            w2,e=np.linalg.eigh(D);res=(z@e)**2
            sum_error=max(sum_error,abs(sum(res)-z@z)/(z@z))
            om=.71+.13j
            direct=z@np.linalg.solve(D-om**2*np.eye(2),z)
            modal=sum(res/(w2-om**2))
            resolve_error=max(resolve_error,abs(direct-modal)/max(1,abs(direct)))
        D,_=matrix(threshold(eps),eps)
        assert abs(np.linalg.det(D)) < 1e-8
    for Q in [.001,.1,1.,10.]:
        D,_=matrix(Q,1.)
        equal_error=max(equal_error,float(np.max(abs(np.linalg.eigvalsh(D)-[Q*Q-2,Q*Q+2]))))
    assert determinant_error<1e-10 and sum_error<1e-12 and resolve_error<1e-10 and equal_error<1e-12
    return dict(determinant_relative_error=determinant_error,equal_mass_absolute_error=equal_error,
                dipole_sum_rule_relative_error=sum_error,resolvent_relative_error=resolve_error)

def physical(eps,m_ev,M,b):
    m=m_ev*EVKG;rad=b*KPC;mass=M*MSUN
    rho=ETA*mass/(4*np.pi*rad**3/3);n=rho/(m*(1+eps))
    omega0=np.sqrt(4*np.pi*G*rho/(1+eps));k=np.pi/rad
    Q=HBAR*k*k/(2*m*omega0);QJ=threshold(eps)
    sigma=np.sqrt(G*(1+ETA)*mass/(6*rad))
    occupation=[float(n*(np.sqrt(2*np.pi)*HBAR/(ms*sigma))**3) for ms in [m,eps*m]]
    speed=HBAR*k/(eps*m*C)
    return dict(Mb_solar=M,b_kpc=b,m_eV=m_ev,epsilon=eps,rho_kg_m3=rho,
                Q=Q,stable_object_mode=bool(Q>QJ),
                critical_mass_eV=HBAR*k*k/(2*omega0*QJ)/EVKG,
                jeans_wavelength_kpc=2*np.pi/np.sqrt(2*m*omega0*QJ/HBAR)/KPC,
                mode_speed_over_c= speed,nonrelativistic=bool(speed<.1),
                occupation_proxy=occupation,alpha_G=G*m*m/(HBAR*C))

def main(output):
    result=dict(checks=checks(),spectra=[],energy_tests=[],physical_scan=[])
    for eps in [.01,.1,1.]:
        for gravity in [False,True]:
            for Q in np.geomspace(.001,100,101):
                result['spectra'].append(spectrum(Q,eps,gravity))
        for Q in [.3*threshold(eps),2*threshold(eps)]:
            for rtol in [1e-8,1e-11]:
                result['energy_tests'].append(energy_test(Q,eps,rtol))
        for m in np.geomspace(1e-27,1e-19,241):
            rows=[physical(eps,float(m),M,b) for M,b in PROFILES]
            result['physical_scan'].append(dict(epsilon=eps,m_eV=float(m),profiles=rows,
                all_nonrelativistic=all(r['nonrelativistic'] for r in rows),
                dwarf_stable_disk_unstable_cluster_stable=bool(rows[0]['stable_object_mode'] and not rows[2]['stable_object_mode'] and rows[3]['stable_object_mode'])))
    result['threshold_examples']=[physical(.1,1e-22,M,b) for M,b in PROFILES]
    result['summary']=dict(spectra=len(result['spectra']),energy_tests=len(result['energy_tests']),
        universal_parameter_points=len(result['physical_scan']),
        all_nonrelativistic_points=sum(r['all_nonrelativistic'] for r in result['physical_scan']),
        proxy_separation_points=sum(r['dwarf_stable_disk_unstable_cluster_stable'] for r in result['physical_scan']),
        max_fine_energy_error=max(r['max_energy_error_over_initial_positive_scale'] for r in result['energy_tests'] if r['rtol']==1e-11))
    with open(output,'w') as f:json.dump(result,f,indent=2,allow_nan=False)
    print(json.dumps(dict(summary=result['summary'],checks=result['checks'],thresholds=result['threshold_examples'])))

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--output',required=True)
    main(p.parse_args().output)
