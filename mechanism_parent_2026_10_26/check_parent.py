"""Bounded symbolic/linear checks; no nonlinear formation claim."""
import argparse
import json
from pathlib import Path
import numpy as np
import sympy as sp
from scipy.linalg import expm
from scipy.integrate import solve_ivp
from scipy.sparse import diags
from scipy.sparse.linalg import spsolve


def symbolic():
    s, n, h, lam, M, Y = sp.symbols('s n h lam M Y', real=True)
    L = -M**2*(s-lam*n)**2/2+h*s*Y
    se = sp.solve(sp.diff(L, s), s)[0]
    assert sp.simplify(L.subs(s, se)-h*lam*n*Y-h**2*Y**2/(2*M**2)) == 0
    w, cs, k, om = sp.symbols('w cs k om', positive=True)
    D = M**2*lam**2*n**2/w
    H = h*n
    B = M**2*lam*n
    matrix = sp.Matrix([[w*((cs+D)*k**2-om**2), -sp.I*B*k, 0],
                        [sp.I*B*k, k**2+M**2-om**2, sp.I*H*om],
                        [0, -sp.I*H*om, k**2-om**2]])
    det = w*((cs+D)*k**2-om**2)*((k**2+M**2-om**2)*(k**2-om**2)-H**2*om**2)-B**2*k**2*(k**2-om**2)
    assert sp.simplify(matrix.det()-det) == 0
    e, v = sp.symbols('e v', real=True)
    A = 1+H**2/M**2
    low = sp.expand(det.subs({k:e, om:e*sp.sqrt(v)})).coeff(e, 4)/(w*M**2)
    expected = A*v**2-(1+A*cs+(A-1)*D)*v+cs
    assert sp.simplify(low-expected) == 0
    assert sp.simplify(expected.subs(v, 1)-(A-1)*(1-cs-D)) == 0
    assert sp.simplify(det.subs(k, 0)+w*om**4*(om**2-M**2-H**2)) == 0
    return {'eliminated_interaction':str(sp.expand(L.subs(s, se))),
            'checks':['mediator elimination', 'Hermitian determinant',
                      'low-frequency reduction', 'cone threshold', 'zero-k gap']}


def ham(k, cs, D, h, M=1., n=1., w=1.):
    lam=np.sqrt(D*w)/(M*n); B=M*M*lam*n; H=h*n
    K=np.zeros((6,6),complex)
    K[0,0]=w*(cs+D)*k*k
    K[1,1]=k*k+M*M+H*H
    K[2,2]=k*k
    K[0,1]=-1j*B*k; K[1,0]=1j*B*k
    K[1,5]=K[5,1]=-H
    K[3:,3:]=np.diag([1/w,1,1])
    J=np.block([[np.zeros((3,3)),np.eye(3)],[-np.eye(3),np.zeros((3,3))]])
    return K,J@K,lam


def dispersion():
    cases=0; max_real=0.; max_poly=0.; min_energy=float('inf'); rows=[]
    for cs in [.001,.1,.6]:
      for D in [.01,.1,.9*(1-cs),1-cs,1.2*(1-cs)]:
       for h in [0.,.2,2.,10.]:
        A=1+h*h
        low=np.sort(np.roots([A,-(1+A*cs+(A-1)*D),cs]))
        assert np.max(np.abs(np.imag(low)))<1e-12
        low=np.real(low)
        assert min(low)>0
        if h>0:
            assert (low[-1]<=1+1e-12)==(D<=1-cs+1e-12)
        for k in np.logspace(-2,2,41):
            K,F,lam=ham(k,cs,D,h)
            mine=float(np.linalg.eigvalsh(K)[0]);min_energy=min(min_energy,mine)
            assert mine>0
            vals=np.linalg.eigvals(F)
            max_real=max(max_real,float(np.max(abs(vals.real))/max(1,np.max(abs(vals)))))
            assert np.max(abs(vals.real))<1e-8*max(1,np.max(abs(vals)))
            pos=np.sort(vals.imag[vals.imag>0]);assert len(pos)==3
            for om in pos:
                x=om*om
                t1=((cs+D)*k*k-x)*(k*k+1-x)*(k*k-x)
                t2=-((cs+D)*k*k-x)*h*h*x
                t3=-D*k*k*(k*k-x)
                res=abs(t1+t2+t3)/max(1,abs(t1)+abs(t2)+abs(t3))
                max_poly=max(max_poly,float(res))
                assert res<1e-7
            if abs(k-.01)<1e-12:
                # Two light modes only; a massive phase speed is not a cone test.
                err=float(np.max(abs(pos[:2]**2/k**2-low)/low))
                rows.append({'cs_squared':cs,'D':D,'h':h,'low_speed_squared':low.tolist(),
                             'finite_k_0p01_relative_error':err,'parent_causal':bool(cs+D<=1+1e-12)})
            cases+=1
    return {'mode_cases':cases,'parameter_sets':len(rows),'max_relative_eigenvalue_real_part':max_real,
            'max_normalized_cubic_residual':max_poly,'minimum_Hessian_eigenvalue':min_energy,'rows':rows}


def static():
    M=2.;lam=.3;rows=[]
    # Periodic n=1+.2cos(x)+.1cos(3x), averages over 2pi.
    exact=sum(lam**2*M*M*k*k*a*a/(4*(M*M+k*k)) for k,a in [(1,.2),(3,.1)])
    for N in [64,128,256,512]:
        dx=2*np.pi/N;x=np.arange(N)*dx;n=1+.2*np.cos(x)+.1*np.cos(3*x)
        mat=diags([-np.ones(N-1)/dx**2,np.full(N,M*M+2/dx**2),-np.ones(N-1)/dx**2],[-1,0,1],format='lil')
        mat[0,-1]=mat[-1,0]=-1/dx**2
        s=spsolve(mat.tocsr(),M*M*lam*n)
        energy=float(np.mean(((np.roll(s,-1)-s)/dx)**2+M*M*(s-lam*n)**2)/2)
        e=abs(energy-exact)
        rows.append({'N':N,'energy_average':energy,'absolute_error':e})
    ratios=[rows[i]['absolute_error']/rows[i+1]['absolute_error'] for i in range(3)]
    assert all(3.9<r<4.1 for r in ratios)
    assert rows[-1]['absolute_error']<1e-7
    return {'exact_continuum_energy_average':exact,'rows':rows,'error_ratios':ratios}


def evolution():
    k=.7;cs=.1;D=.25;h=2.
    K,F,lam=ham(k,cs,D,h)
    z=np.zeros(6,complex);z[0]=.01
    z[1]=-1j*lam*k*z[0]/(1+k*k)  # s statically relaxed at initial density.
    z[5]=h*z[1]                 # chi_t=0; chi itself is also zero.
    def energy(a):return float(np.real(np.vdot(a,K@a))/2)
    E0=energy(z)
    t=np.linspace(0,100,501)
    sol=solve_ivp(lambda t,y:F@y,(0,100),z,t_eval=t,rtol=1e-11,atol=1e-13,method='DOP853')
    assert sol.success
    exact=expm(F*100)@z
    error=float(np.linalg.norm(sol.y[:,-1]-exact)/np.linalg.norm(exact))
    drift=max(abs(energy(a)-E0)/E0 for a in sol.y.T)
    peak=float(np.max(abs(sol.y[2])))
    assert error<1e-8 and drift<1e-8 and peak>1e-5
    return {'initial_energy':E0,'max_relative_energy_drift':drift,'endpoint_vs_matrix_exponential':error,
            'peak_chi_amplitude':peak,'initial_chi':0,'initial_chi_velocity':0,
            'non_claim':'One deliberately displaced periodic linear mode; reversible exchange, no outgoing cooling or galaxy formation.'}


if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);args=ap.parse_args()
    result={'symbolic':symbolic(),'dispersion':dispersion(),'static':static(),'linear_evolution':evolution(),
            'outcome':'finite assertions passed; mathematical restrictions remain as stated in DERIVATION.md'}
    Path(args.output).write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:({a:b for a,b in v.items() if a!='rows'} if isinstance(v,dict) else v) for k,v in result.items()},indent=2))
