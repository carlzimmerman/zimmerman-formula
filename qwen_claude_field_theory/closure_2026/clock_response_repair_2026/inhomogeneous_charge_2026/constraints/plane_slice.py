#!/usr/bin/env python3
"""Full-gamma plane-symmetric instantaneous constraints and clock preservation.

Frozen constitutive action, not a fitted action. Positive-expansion K, flat
initial spatial metric, tau=t, physical Q uniform on this one initial slice.
Finite interval IVPs are not asymptotic matching or spacetime evolution.
"""
import argparse
from functools import lru_cache
import json
from pathlib import Path
import sys

import numpy as np
import sympy as sy
from scipy.integrate import quad, solve_ivp

HERE = Path(__file__).resolve().parent
REPAIR = HERE.parents[1]
sys.path.insert(0, str(REPAIR/'nonlinear_evolution_2026'))
from constitutive import Model
sys.path.insert(0, str(REPAIR/'finite_gradient_metric_2026/cubic'))
from cubic_debraiding import corrected


@lru_cache(maxsize=1)
def construct():
    Q,b,bx,k,h,kp = sy.symbols('Q b bx k h kp', real=True)
    P,p,r,Pt,Pxt,Ptt,V,Vt,Vtt,W,d,e,f,Wt,dt,et = sy.symbols(
        'P p r Pt Pxt Ptt V Vt Vtt W d e f Wt dt et', real=True)
    ga,M2,Lam,rho,pm = sy.symbols('ga M2 Lam rho pm', real=True)
    A,s,N,Np,Npp,A0,As = sy.symbols('A s N Np Npp A0 As', real=True)
    Qx = sy.Symbol('Qx', real=True)
    acceleration=sy.Symbol('acceleration',real=True)
    eta = sy.diag(-1,1,1,1)
    v = sy.Matrix([Q,b,0,0]); vu=eta*v
    X=Q**2-b**2; Y=b**2; theta=k+2*h; C=d+2*Y*e
    H=sy.diag(A,bx-k*Q,-h*Q,-h*Q)
    H[0,1]=H[1,0]=Qx-k*b
    box=sy.trace(eta*H); vvH=(vu.T*H*vu)[0]
    T3=2*ga*(box*v*v.T-v*(H*vu).T-(H*vu)*v.T+eta*vvH)
    lag=P-V+s*W
    T0=sy.diag(2*p*Q**2-P+V,lag+2*(p-s*d)*Y,lag,lag)
    T0[0,1]=T0[1,0]=2*p*Q*b
    Tm=sy.diag(rho,pm,pm,pm)
    total=T0+T3+Tm
    reverse=total-eta*sy.trace(eta*total)/2
    Ricvv=(vu.T*reverse*vu)[0]/M2-Lam*X
    Hnorm=sy.trace(eta*H*eta*H)
    # Scalar/metric variations and covariant commutator are analytical inputs
    # from the audited full action. All ensuing slice contractions are exact.
    Echi=(2*p*box-4*r*vvH-2*s*Q*Pxt-2*s*C*bx
          +2*ga*(box**2-Hnorm-Ricvv)).subs(Qx,0)
    Echi=sy.expand(Echi)
    EA=sy.diff(Echi,A); E0=Echi.subs({A:0,s:0}); Es=sy.diff(Echi,s)
    rho3=2*ga*(X*bx-Q*X*k-2*Q**3*h)
    flux3=2*ga*(X*Qx-b*(X*k+2*Q**2*h))
    ham=M2*(2*k*h+h*h-Lam)-(2*p*Q*Q-P+V+rho+rho3)
    clock=Vt-Pt+W*theta-2*d*k*Y-2*Q*C*bx
    nY=2*b*(Qx+Q*acceleration-k*b)
    clock_covariant=Pt-Vt+s*Wt-(s*Wt+d*nY+W*theta)+2*(Qx*d*b+Q*C*bx+acceleration*Q*d*b)
    nX=2*Q*(A+acceleration*b)-nY
    covariant_charge=2*p*Q+2*ga*Q*box+ga*nX
    charge_expected=2*p*Q+2*ga*(Q*bx-X*k-2*Q**2*h-b*Qx)
    covariant_flux=-2*b*(p+ga*box)-ga*(2*Q*Qx-2*b*bx)+2*s*d*b
    flux_expected=2*b*(s*d-p)+2*ga*(b*(A+Q*theta)-Q*Qx)
    # Chain derivatives at fixed tau. Constitutive p=P_X, r=P_XX,
    # Pt=P_tau and Pxt=P_Xtau: changing b changes X by -2b db.
    def db(expr):
        return (sy.diff(expr,b)-2*b*(sy.diff(expr,P)*p+sy.diff(expr,p)*r
                    +sy.diff(expr,Pt)*Pxt)
                +2*b*(sy.diff(expr,W)*d+sy.diff(expr,d)*e+sy.diff(expr,e)*f))
    spatial_matrix=sy.Matrix([[sy.diff(ham,k),sy.diff(ham,bx)],
                              [sy.diff(clock,k),sy.diff(clock,bx)]])
    spatial_rhs=-sy.Matrix([ham.subs({k:0,bx:0}),clock.subs({k:0,bx:0})])
    hb=sy.expand(db(ham)); cb=sy.expand(db(clock))
    hkt=sy.diff(ham,h); ckt=sy.diff(clock,h)
    # n(clock)=0 in tau=t. Spatial Einstein equations determine normal K
    # velocities; A=H_nn is solved by the debraided scalar equation.
    clock_t=Vtt-Ptt+Wt*theta-2*dt*k*Y-2*Q*(dt+2*Y*et)*bx
    clock_Q=-2*Q*Pxt-2*C*bx
    clock_k=W-2*d*Y; clock_h=2*W; clock_bx=-2*Q*C
    Txx=sy.expand(total[1,1].subs(Qx,0))
    Tyy=sy.expand(total[2,2].subs(Qx,0))
    nh=-(3*h*h-Lam+Txx/M2)/2
    nk=Lam-k*k-k*h-h*h+Npp/N-Tyy/M2-nh
    nQ=A+Np*b/N
    nb=Q*Np/N-k*b
    nbx=Q*Npp/N-Np*k*b/N-kp*b-2*k*bx
    preserve=N*(clock_t/N+clock_Q*nQ+clock_k*nk+clock_h*nh+cb*nb+clock_bx*nbx)
    preserve=sy.expand(preserve.subs({A:A0+As/N,s:1/N}, simultaneous=True))
    a2=sy.diff(preserve,Npp); a1=sy.diff(preserve,Np)
    a0=sy.diff(preserve,N); force=preserve.subs({N:0,Np:0,Npp:0})
    F=W-2*Q**2*C-2*Y*d
    Fprime=-2*b*bx*(C+2*Q**2*(3*e+2*Y*f))
    checks={
        'cubic_energy_no_acceleration':sy.expand(T3[0,0]-rho3)==0,
        'cubic_flux_no_acceleration':sy.expand(T3[0,1]-flux3)==0,
        'cubic_longitudinal_stress':sy.expand(T3[1,1]-2*ga*(X*A-2*Q*h*Y))==0,
        'cubic_transverse_stress':sy.expand(T3[2,2]-2*ga*(Q**2*A-2*Q*b*Qx+Q*k*Y+Y*bx))==0,
        'scalar_acceleration_linear':sy.expand(Echi-EA*A-E0-Es*s)==0,
        'scalar_acceleration_independent_lapse':sy.diff(EA,s)==0,
        'lapse_preservation_linear':sy.expand(preserve-a2*Npp-a1*Np-a0*N-force)==0,
        'lapse_longitudinal_F':sy.expand(a2-F)==0,
        'lapse_first_coefficient':sy.expand(a1-Fprime-4*Q*b*d*h)==0,
        'homogeneous_cubic_energy':sy.expand(rho3.subs({b:0,bx:0,k:h})+6*ga*h*Q**3)==0,
        'hamiltonian_acceleration_absent':not ham.has(A),
        'covariant_clock_lapse_gradient_cancellation':sy.expand(clock_covariant+clock)==0,
        'covariant_charge_projection':sy.expand(covariant_charge-charge_expected)==0,
        'covariant_spatial_current_projection':sy.expand(covariant_flux-flux_expected)==0,
    }
    if not all(checks.values()): raise AssertionError(checks)
    args=[Q,b,bx,k,h,kp,P,p,r,Pt,Pxt,Ptt,V,Vt,Vtt,W,d,e,f,Wt,dt,et,ga,M2,Lam,rho,pm]
    exprs=[*spatial_matrix,*spatial_rhs,hb,cb,hkt,ckt,EA,E0,Es,ham,clock,
           a2,a1,a0,force,Txx,Tyy,Echi]
    # A0,As are computed from EA,E0,Es; extra arguments are passed explicitly.
    evaluate=sy.lambdify(args+[A0,As,A,s],exprs,'numpy',cse=True)
    return dict(checks=checks,eval=evaluate,args=[str(x) for x in args],
                expressions={name:str(sy.factor(expr)) for name,expr in
                  dict(hamiltonian=ham,clock=clock,cubic_energy=rho3,cubic_flux=flux3,
                       scalar_acceleration_coefficient=EA,lapse_a2=a2,lapse_a1=a1,
                       lapse_a0=a0,lapse_force=force).items()})


class Slice:
    def __init__(self, amplitude=0., width=.3, b0=0., rtol=2e-10, max_step=.02):
        self.source=json.loads((REPAIR/'cosmological_bridge_2026/radiation_002/result.json').read_text())['samples'][0]
        self.model=Model(.01,gamma=1e-6)
        self.amplitude=amplitude; self.width=width; self.b0=b0; self.rtol=rtol; self.max_step=max_step
        self.Q=self.source['q']; self.tau=self.source['tau']; self.audit=construct()
    def density(self,x):
        delta=self.amplitude*np.exp(-(x/self.width)**2)
        return self.source['rho_baryon']+delta+self.source['rho_radiation'], -2*x*delta/self.width**2
    def raw(self,x,b,h,bx=0.,k=0.,kp=0.,A0=0.,As=0.,A=0.,s=1.):
        Q=self.Q; j=self.model.jets(self.tau,Q*Q-b*b,b*b)
        rho,_=self.density(x); pm=self.source['rho_radiation']/3
        aliases={'P':'P','p':'P_X','r':'P_XX','Pt':'P_t','Pxt':'P_Xt','Ptt':'P_tt',
                 'V':'V','Vt':'V_t','Vtt':'V_tt','W':'W','d':'W_Y','e':'W_YY','f':'W_YYY',
                 'Wt':'W_t','dt':'W_Yt','et':'W_YYt'}
        vals={key:float(j[name]) for key,name in aliases.items()}
        vals.update(Q=Q,b=b,bx=bx,k=k,h=h,kp=kp,ga=self.model.gamma,M2=1.,Lam=.7,rho=rho,pm=pm)
        out=np.asarray(self.audit['eval'](*[vals[key] for key in self.audit['args']],A0,As,A,s),dtype=float)
        return out,j
    def point(self,x,state):
        b,h,N,Np=state
        if N<=0: raise ValueError('positive lapse lost')
        out,j=self.raw(x,b,h)
        mat=out[:4].reshape(2,2); rhs=out[4:6]
        k,bx=np.linalg.solve(mat,rhs)
        Q=self.Q; X=Q*Q-b*b; ga=self.model.gamma
        hp=-(j['P_X']*Q*b-ga*b*(X*k+2*Q*Q*h))
        out,j=self.raw(x,b,h,bx,k)
        rhop=self.density(x)[1]
        kp,bxx=np.linalg.solve(mat,-np.array([out[6]*bx+out[8]*hp-rhop,
                                             out[7]*bx+out[9]*hp]))
        EA,E0,Es=out[10:13]
        if abs(EA)<1e-8:raise ValueError('scalar acceleration degeneracy')
        A0=-E0/EA; As=-Es/EA; A=A0+As/N
        out,j=self.raw(x,b,h,bx,k,kp,A0,As,A,1/N)
        a2,a1,a0,force=out[15:19]
        if abs(a2)<1e-8:raise ValueError('clock lapse principal degeneracy')
        Npp=-(a1*Np+a0*N+force)/a2
        Txx,Tyy,Echi=out[19:22]
        nh=-(3*h*h-.7+Txx)/2
        nk=.7-k*k-k*h-h*h+Npp/N-Tyy-nh
        hessian=np.diag([A,bx-k*Q,-h*Q,-h*Q]);hessian[0,1]=hessian[1,0]=-k*b
        # corrected() represents the gradient by +sqrt(Y). Reflect the
        # spatial frame for b<0 as well as the Hessian; never mix orientations.
        reflect=np.diag([1.,-1. if b<0 else 1.,1.,1.])
        principal_hessian=reflect@hessian@reflect
        jj={key:float(j[value]) for key,value in {'PX':'P_X','PXX':'P_XX','W':'W','WY':'W_Y','WYY':'W_YY'}.items()}
        principal=[]
        for mu in (0.,1.):
            principal.append(corrected(jj,Q,1/N,b*b,mu,hessian_cov=principal_hessian))
        momentum=-2*hp-2*j['P_X']*Q*b+2*ga*b*(X*k+2*Q*Q*h)
        # Orthogonal check: rebuild Ricci from geometric normal velocities,
        # then use the original (not debraided) covariant scalar equation.
        eta=np.diag([-1.,1.,1.,1.]);vu=np.array([-Q,b,0.,0.])
        ricci=np.diag([-(nk+2*nh)-k*k-2*h*h+Npp/N,
                       nk+(k+2*h)*k-Npp/N,nh+(k+2*h)*h,nh+(k+2*h)*h])
        ricci[0,1]=ricci[1,0]=-2*hp
        box=np.trace(eta@hessian);vvH=vu@hessian@vu
        C=j['W_Y']+2*b*b*j['W_YY']
        direct_Echi=(2*j['P_X']*box-4*j['P_XX']*vvH-2*Q*j['P_Xt']/N-2*C*bx/N
                     +2*ga*(box*box-np.trace(eta@hessian@eta@hessian)-vu@ricci@vu))
        charge=2*j['P_X']*Q+2*ga*(Q*bx-X*k-2*Q*Q*h)
        spatial_current=2*b*(j['W_Y']/N-j['P_X'])+2*ga*b*(A+(k+2*h)*Q)
        return dict(x=float(x),b=float(b),Y=float(b*b),kt=float(h),kx=float(k),N=float(N),s=float(1/N),
                    Np=float(Np),Npp=float(Npp),bp=float(bx),bpp=float(bxx),ktp=float(hp),kxp=float(kp),
                    A=float(A),normal_Q=float(A+Np*b/N),normal_kx=float(nk),normal_kt=float(nh),
                    density=float(self.density(x)[0]),scalar_E_coefficient=float(EA),
                    covariant_charge_density=float(charge),covariant_spatial_current=float(spatial_current),
                    lapse_coefficients=[float(v) for v in (a2,a1,a0,force)],
                    matrix_determinant=float(np.linalg.det(mat)),matrix_condition=float(np.linalg.cond(mat)),
                    domain_margin=float(j['domain_denominator']),
                    residuals=[float(out[13]),float(momentum),float(out[14]),float(Echi),
                               float(a2*Npp+a1*Np+a0*N+force),float(direct_Echi)],
                    hessian=hessian.tolist(),principal=principal)
    def rhs(self,x,state):
        row=self.point(x,state)
        return [row['bp'],row['ktp'],state[3],row['Npp']]
    def solve(self,extent=.5):
        y0=[self.b0,self.source['H'],1/self.source['clock_rate'],0.]
        self.left=solve_ivp(self.rhs,(0.,-extent),y0,method='DOP853',rtol=self.rtol,
                            atol=self.rtol*.01,max_step=self.max_step,dense_output=True)
        self.right=solve_ivp(self.rhs,(0.,extent),y0,method='DOP853',rtol=self.rtol,
                             atol=self.rtol*.01,max_step=self.max_step,dense_output=True)
        if not self.left.success or not self.right.success:raise RuntimeError('slice/lapse IVP did not finish')
        self.extent=extent
        return self
    def state(self,x):return (self.left if x<0 else self.right).sol(x)
    def samples(self,count=101):
        rows=[]
        for x in np.linspace(-self.extent,self.extent,count):
            row=self.point(x,self.state(x))
            chi,error=quad(lambda xx:self.state(xx)[0],0.,x,epsabs=1e-12,epsrel=1e-12)
            row.update(chi=float(chi),chi_quadrature_error=float(error))
            rows.append(row)
        return rows

    def clock_time_difference(self,row,step):
        """One-sided second-order time derivative from actual frozen jets.

        Affine normal-time jet extension tests n(clock)=0 at time zero only;
        the extension is not asserted to solve the equations at finite time.
        """
        Q=self.Q;b=row['b'];k=row['kx'];h=row['kt'];bx=row['bp']
        accel=row['Np']/row['N']
        velocities=[row['normal_Q'],Q*accel-k*b,row['normal_kx'],row['normal_kt'],
                    Q*row['Npp']/row['N']-accel*k*b-row['kxp']*b-2*k*bx]
        def value(epsilon):
            q1,b1,k1,h1,bx1=np.array([Q,b,k,h,bx])+epsilon*np.array(velocities)
            j=self.model.jets(self.tau+epsilon*row['s'],q1*q1-b1*b1,b1*b1)
            return j['V_t']-j['P_t']+j['W']*(k1+2*h1)-2*j['W_Y']*k1*b1*b1-2*q1*(j['W_Y']+2*b1*b1*j['W_YY'])*bx1
        return float((-3*value(0.)+4*value(step)-value(2*step))/(2*step))


def run():
    exact=construct(); cases=[]
    for label,amplitude,b0 in [('homogeneous_control',0.,0.),('uniform_matter_finite_gradient',0.,.009),
                                ('baryon_gaussian',.0001,0.)]:
        coarse=Slice(amplitude=amplitude,b0=b0).solve()
        fine=Slice(amplitude=amplitude,b0=b0,rtol=2e-12,max_step=.005).solve()
        rows=fine.samples()
        refinement=max(float(np.max(np.abs(coarse.state(x)-fine.state(x)))) for x in np.linspace(-.5,.5,101))
        fd=[]
        for step in (1e-3,5e-4):
            errs=[]
            for x in np.linspace(-.45,.45,37):
                derivative=(-fine.state(x+2*step)+8*fine.state(x+step)-8*fine.state(x-step)+fine.state(x-2*step))/(12*step)
                errs.append(float(np.max(np.abs(derivative-fine.rhs(x,fine.state(x))))))
            fd.append(dict(step=step,max_fourth_order_derivative_residual=max(errs)))
        residuals=np.max(np.abs([r['residuals'] for r in rows]),axis=0)
        timefd=[dict(step=step,max_clock_normal_derivative= max(abs(fine.clock_time_difference(row,step))
                         for row in rows[::25])) for step in (1e-4,5e-5)]
        if max(residuals)>1e-9 or refinement>1e-8 or max(f['max_fourth_order_derivative_residual'] for f in fd)>1e-6:
            raise AssertionError('constraint/refinement/independent-derivative gate failed')
        if max(f['max_clock_normal_derivative'] for f in timefd)>1e-7:
            raise AssertionError('independent clock-time finite-difference gate failed')
        charge,charge_error=quad(lambda x:fine.point(x,fine.state(x))['covariant_charge_density'],-.5,.5,
                                 epsabs=1e-12,epsrel=1e-12)
        left_flux=rows[0]['N']*rows[0]['covariant_spatial_current']
        right_flux=rows[-1]['N']*rows[-1]['covariant_spatial_current']
        cases.append(dict(label=label,parameters=dict(amplitude=amplitude,b0=b0,width=.3,extent=.5,
                         gamma=1e-6,coarse_rtol=2e-10,fine_rtol=2e-12,coarse_max_step=.02,fine_max_step=.005),rows=rows,
                         max_residuals=residuals.tolist(),max_state_refinement_error=refinement,
                         finite_difference_checks=fd,clock_time_difference_checks=timefd,
                         Y_range=[min(r['Y'] for r in rows),max(r['Y'] for r in rows)],
                         s_range=[min(r['s'] for r in rows),max(r['s'] for r in rows)],
                         minimum_domain_margin=min(r['domain_margin'] for r in rows),
                         minimum_lapse_F=min(r['lapse_coefficients'][0] for r in rows),
                         maximum_constraint_matrix_condition=max(r['matrix_condition'] for r in rows),
                         charge_density_range=[min(r['covariant_charge_density'] for r in rows),
                                               max(r['covariant_charge_density'] for r in rows)],
                         charge_integral_per_unit_transverse_area=float(charge),
                         charge_integral_quadrature_error=float(charge_error),
                         inherited_homogeneous_charge_same_coordinate_volume=float(fine.source['scalar_charge']),
                         coordinate_clock_time_boundary_flux_left=float(left_flux),
                         coordinate_clock_time_boundary_flux_right=float(right_flux),
                         instantaneous_box_charge_derivative=float(left_flux-right_flux),
                         longitudinal_Xi_range=[min(r['principal'][1]['quarter_finite_gamma'] for r in rows),
                                                max(r['principal'][1]['quarter_finite_gamma'] for r in rows)]))
    return dict(exact_checks=exact['checks'],expressions=exact['expressions'],cases=cases,
                scope='Full gamma frozen action; finite interval plane initial constraints plus clock-preserving positive lapse IVP and instantaneous evolution jets.',
                non_claims=['Not a global asymptotically FLRW solution or a matched exterior',
                            'Not spacetime evolution, nonlinear well-posedness or stability over time',
                            'No coefficient reconstruction, additional matter species, or cosmological/CMB calibration'])


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--result-file',required=True,type=Path)
    args=parser.parse_args();result=run();args.result_file.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(dict(exact_checks=result['exact_checks'],cases=[{k:v for k,v in c.items() if k!='rows'} for c in result['cases']]),indent=2))
