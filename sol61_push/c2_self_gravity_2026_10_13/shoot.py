"""Deterministic bounded C2 + Einstein equilibrium shoots; not certified roots."""
from pathlib import Path
import json
import numpy as np
from scipy.integrate import solve_ivp, simpson
from scipy.optimize import root, brentq

OUT=Path(__file__).parent/'numeric_run'
Y0=brentq(lambda x:np.tan(x)-x,np.pi+1e-5,1.5*np.pi-1e-5,xtol=1e-14)
UC0=1-Y0/np.sin(Y0)
LAMBDA0=1/UC0
records=[]
arrays={}

def integrate(uc,Y,eps,tight=False):
    y0=1e-6 if tight else 1e-5
    rho=1+2*uc+1.5*eps*uc**2
    p=-1+.5*eps*uc**2
    u0=uc-(1+eps*uc)*(rho/3+p)*y0**2/4
    w0=rho*y0**3/3
    def rhs(y,z):
        u,w=z
        B=1-eps*w/(2*y)
        return [-(1+eps*u)*(w+y**3*(-1+.5*eps*u**2))/(2*y**2*B),y**2*(1+2*u+1.5*eps*u**2)]
    def near_horizon(y,z):return 1-eps*z[1]/(2*y)-.05
    near_horizon.terminal=True
    near_horizon.direction=-1
    sol=solve_ivp(rhs,(y0,Y),[u0,w0],method='DOP853',rtol=2e-12 if tight else 2e-10,atol=2e-14 if tight else 2e-12,dense_output=True,events=near_horizon)
    assert sol.success and abs(sol.t[-1]-Y)<1e-12, 'integration/horizon trial failure'
    return sol

for b in [100,1000,10000]:
    eps=1/b
    stages=[]
    solutions=[]
    guess=np.array([UC0,Y0])
    for tight in [False,True]:
        trials=[]
        def residual(q):
            uc,Y=map(float,q)
            assert uc>0 and 3.5<Y<5.5, 'shoot left frozen neighborhood'
            sol=integrate(uc,Y,eps,tight)
            u,w=sol.y[:,-1]
            residuals=[float(u),float(w-Y**3)]
            samples=sol.sol(np.linspace(sol.t[0],Y,101))
            trials.append({'uc':uc,'Y':Y,'residuals':residuals,'sample_min_u':float(samples[0].min()),'trial_only':True})
            return residuals
        res=root(residual,guess,method='hybr',tol=1e-10)
        uc,Y=map(float,res.x)
        end=residual(res.x)
        assert res.success and max(abs(v) for v in end)<1e-8, (b,res.message,end)
        sol=integrate(uc,Y,eps,tight)
        y=np.linspace(0,Y,1001)
        u,w=sol.sol(np.maximum(y,sol.t[0])); u[0]=uc; w[0]=0
        B=np.ones_like(y); B[1:]=1-eps*w[1:]/(2*y[1:])
        assert u.min()>=-1e-8 and B.min()>.5, (b,'physical sample admission')
        solutions.append((uc,Y,y,u,w,B))
        stages.append({'tight':tight,'root_success':bool(res.success),'message':str(res.message),'endpoint':end,'trial_count':len(trials),'trials':trials})
        guess=res.x
    uc,Y,y,u,w,B=solutions[-1]
    base=solutions[0]
    changes={'uc':abs(uc-base[0]),'Y':abs(Y-base[1]),'u_profile':float(np.max(np.abs(u-base[3]))),'w_profile':float(np.max(np.abs(w-base[4]))),'B_profile':float(np.max(np.abs(B-base[5]))),'endpoint':max(abs(v) for v in stages[-1]['endpoint'])}
    assert max(changes.values())<=1e-6, (b,'refinement',changes)
    BR=1-eps*Y**2/2
    # omega=sqrt(2X0), peak lapse=1, X=X0(1+epsilon*u).
    N=1/np.sqrt(1+eps*u)
    rhoex=2*u+1.5*eps*u**2
    integral_areal=float(simpson(rhoex*y*y,x=y))
    integral_proper=float(simpson(rhoex*y*y/np.sqrt(B),x=y))
    integral_q=float(simpson(u*np.sqrt(1+eps*u)*y*y/np.sqrt(B),x=y))
    # Overall common factors: 4pi*rho0*(ell/(2sqrtb))^3 for E,
    # 4pi*rho0*sqrt(2/X0)*(ell/(2sqrtb))^3 for Q.
    assert abs(integral_areal-2*Y**3/3)<1e-6
    assert integral_proper>integral_areal, 'proper volume differs'
    # Exterior B(sY)=1-eps*Y²*(1/(3s)+s²/6); unique maximum at s=1.
    def be(s):return 1-eps*Y**2*(1/(3*s)+s*s/6)
    horizon=brentq(be,1+1e-8,np.sqrt(6/(eps*Y**2))*2)
    sgrid=np.linspace(1,min(2,(1+horizon)/2),501)
    Bext=be(sgrid)
    N2ext=Bext/BR
    psi2bar=2/Bext*(BR/Bext-1) # psi'^2/X0
    assert np.min(Bext)>0 and np.min(psi2bar)>=-1e-12
    Xbar=(2/N2ext-Bext*psi2bar)/2
    assert np.max(abs(Xbar-1))<1e-12
    arrays[f'b{b}_core']=np.column_stack([y,u,w,B,N])
    arrays[f'b{b}_exterior']=np.column_stack([sgrid,Bext,N2ext,psi2bar])
    records.append({'b':b,'epsilon':eps,'uc':uc,'Y':Y,'central_d_over_X0':eps*uc,'central_excess_density_over_rho0':float(2*uc+1.5*eps*uc**2),'R_over_ell':Y/(2*np.sqrt(b)),'edge_B':BR,'central_N':float(N[0]),'min_sample_u':float(u.min()),'min_B':float(B.min()),'refinement_changes':changes,'integrals':{'areal_excess':integral_areal,'proper_excess':integral_proper,'proper_charge':integral_q,'areal_prediction':2*Y**3/3,'areal_volume_mean_excess_over_rho0':3*integral_areal/Y**3,'proper_volume_mean_excess_over_rho0':integral_proper/float(simpson(y*y/np.sqrt(B),x=y))},'exterior_horizon_over_R':horizon,'shoot_stages':stages})

theta=LAMBDA0+(1-LAMBDA0)*np.sinc(np.linspace(0,Y0,10001)/np.pi)
ys=np.linspace(0,Y0,10001)
Iu=float(simpson(theta**2*ys**2,x=ys)); I4=float(simpson(theta*ys**4,x=ys))
stiff_factor=Iu-LAMBDA0*I4/3
assert stiff_factor>0
assert abs(Iu-5*LAMBDA0**2*Y0**3/6)<1e-10
assert abs(I4-LAMBDA0*Y0**3*(Y0**2/5-2))<1e-9
np.savez_compressed(OUT/'profiles.npz',**arrays)
payload={'all_passed':True,'arithmetic':'float64; conditional on tolerances/libraries','weak_limit':{'Y0':Y0,'uc0':UC0,'lambda0':LAMBDA0,'Iu':Iu,'I4':I4,'homologous_stiffness_factor':stiff_factor,'Y0_squared':Y0**2},'cases':records,'column_order':{'core':['y','u','w','B','N'],'exterior':['r_over_R','B','N_squared','psi_prime_squared_over_X0']},'physical_nonclaims':['Einstein action assumed, not derived','No root certification','No formation or receiving','No full stability or degenerate-vacuum health','No horizon extension']}
(OUT/'results.json').write_text(json.dumps(payload,indent=2)+'\n')
print(json.dumps({'all_passed':True,'cases':[{k:c[k] for k in ['b','uc','Y','edge_B','central_N']} for c in records],'weak_limit':payload['weak_limit']}))
