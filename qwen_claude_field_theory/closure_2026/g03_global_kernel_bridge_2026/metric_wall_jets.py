"""Fifth KG corner jet from the SAME CMC metric Hamiltonian.

Tests the formerly explicit shared-wall compatibility premise. A failure is
a failure of this proposed common boundary experiment, not by itself a
universal causal no-go for the theory. No empirical data or parameter fit.
"""
import argparse
from functools import lru_cache
import json
from pathlib import Path
import time

import numpy as np
from scipy.integrate import solve_ivp
import sympy as s

from metric_initial_response import operators
from metric_static_background import solve_background, curved_matter_jets


@lru_cache(maxsize=1)
def derive_wall():
    d,coeff,_=operators()
    N,A,B,a0,Nd,Ad,Bd,Ndd,Add,Bdd,Lam,u,b,up,bp=d['symbols']
    w,wp,wpp,v,vp,vpp=s.symbols('w wp wpp v vp vpp')
    c,chi=s.symbols('c chi',real=True)
    PA,PB,ell3=s.symbols('PA PB ell3')
    pxx=PA/(4*A); pzz=PB/(2*B)
    trace=2*A**2*pxx+B**2*pzz
    Hkin=N*(2*A**4*pxx**2+B**4*pzz**2-trace**2/2)/(A**2*B)
    kinetic_res=s.factor(Hkin-N*(-PA*PB/(4*A)+B*PB**2/(8*A**2)))

    qs=[N,A,B,Nd,Ad,Bd,Ndd,Add,Bdd]
    variations=[N*v,A*w,B*w,Nd*v+N*vp,Ad*w+A*wp,Bd*w+B*wp,
        Ndd*v+2*Nd*vp+N*vpp,Add*w+2*Ad*wp+A*wpp,Bdd*w+2*Bd*wp+B*wpp]
    gauge={B:1,Bd:0,Bdd:0,Nd:N*u,Ad:A*b,Ndd:N*(up+u**2),Add:A*(bp+b**2)}
    eA,eB=[s.factor(sum(s.diff(e,q)*dq for q,dq in zip(qs,variations))
        .subs(gauge,simultaneous=True).subs({w:0,v:0})) for e in d['EL'][1:]]
    A4=(s.diff(Hkin,PA,PA)*eA+s.diff(Hkin,PA,PB)*eB).subs(B,1)+A*ell3/2
    B4=(s.diff(Hkin,PB,PA)*eA+s.diff(Hkin,PB,PB)*eB).subs(B,1)+ell3/2
    B4=s.factor(B4.subs(ell3,s.solve(A4,ell3)[0]))

    # Linearized KG is qddot = L0 q + delta(D) phidot + delta(L) phi.
    # D=Ndot/N-2Adot/A-Bdot/B. Use product-rule time jets, not an assigned fifth jet.
    mass,r,vel=s.symbols('mass r vel',real=True)
    w3,v3,a4,b4,v4=s.symbols('w3 v3 a4 b4 v4')
    Djets={0:0,1:v-3*w,2:v3-3*w3,3:v4-2*a4-b4}
    phi={0:r,1:N*vel,2:-N**2*mass**2*r,
         3:N**3*vel*(up+2*u**2+2*b*u-mass**2)}
    spatial={N:N*u,u:up,w:wp,wp:wpp,v:vp,vp:vpp}
    def dz(expr):
        return sum(s.diff(expr,key)*value for key,value in spatial.items())
    def L0(expr):
        return N**2*(dz(dz(expr))+(u+2*b)*dz(expr)-mass**2*expr)
    def deltaL(j,f):
        if j in [0,1]:
            return s.S.Zero
        if j==2:
            return N**2*(2*(v-w)*(dz(dz(f))+(u+2*b)*dz(f))
                +(vp+wp)*dz(f)-2*v*mass**2*f)
        # At the wall v3=w3=0, and f=phi0 is spatially constant.
        return -2*N**2*v3*mass**2*f
    q={0:s.S.Zero,1:s.S.Zero,2:s.S.Zero}
    for n in range(1,4):
        q[n+2]=s.expand(L0(q[n])+sum(s.binomial(n,j)*((Djets[j]*phi[n-j+1] if Djets[j]!=0 else 0)
            +deltaL(j,phi[n-j])) for j in range(n+1)))
    wall={w:0,v:0,w3:0,v3:0,a4:0,v4:0}
    fifth=s.factor(q[5].subs(wall).subs(b4,B4)/(N**3*vel))
    # Independent hand product-rule expression, before the action is used.
    direct=-B4/N**2+3*u*(vp+wp)+(vpp-3*wpp)+(3*u+2*b)*(vp-3*wp)
    highest=coeff[:,[2,5]]
    rhs=s.Matrix([0,2*c/N])-coeff[:,[1,4]]*s.Matrix([wp,vp])
    accelerations=(highest.inv()*rhs).applyfunc(s.factor)
    substitutions={wpp:accelerations[0],vpp:accelerations[1]}
    reduced=s.factor(fifth.subs(substitutions,simultaneous=True))
    y=s.symbols('y',positive=True)
    def chi_form(expr):
        return s.factor(expr.subs({u:a0*y},simultaneous=True)
            .subs(s.exp(-y),chi/(1-y)).subs(y,u/a0))
    reduced_chi=chi_form(reduced)
    expected_B4=-N*c/2-3*N**2*((b+u)*wp+(b+u*(1-u/a0)*s.exp(-u/a0))*vp)
    normal_res=s.factor((B4-expected_B4).subs(substitutions,simultaneous=True))
    on_shell_res=s.factor(reduced_chi.subs(chi,(1-u/a0)*s.exp(-u/a0))-reduced)
    # In z=Lx scaling w',v'=O(L), so slope terms disappear as L->0.
    limiting=s.factor(reduced_chi.subs({N:1,wp:0,vp:0}))
    M=s.symbols('M',positive=True)
    return d,coeff,reduced,dict(
        kinetic_reduction_residual=str(kinetic_res),kinetic_Hamiltonian=str(s.factor(Hkin)),
        normal_fourth_from_Hamiltonian=str(B4),
        normal_fourth_identity_residual=str(normal_res),
        wall_third_jet=str(s.factor(q[3].subs(wall))),
        wall_fourth_jet=str(s.factor(q[4].subs(wall))),
        KG_fifth_identity_residual=str(s.factor(fifth-direct)),
        raw_normalized_fifth_jet=str(fifth),
        on_shell_normalized_fifth_jet=str(reduced_chi),
        on_shell_reduction_residual=str(on_shell_res),
        small_slab_fifth_jet=str(limiting),
        positive_bump_small_slab_fifth_jet=str(s.factor(limiting.subs(c,-9*M))))


def wall_response(y0,ratio,L):
    d,coeff,jet,_=derive_wall()
    N,A,B,a0,Nd,Ad,Bd,Ndd,Add,Bdd,Lam,u,b,up,bp=d['symbols']
    wp,vp=s.symbols('wp vp'); c=s.symbols('c',real=True)
    rhs=s.lambdify((u,b),d['rhs'].subs({a0:1,Lam:ratio}),'numpy')
    seed=solve_background(y0,ratio,L)['seed']
    def bgflow(z,Y):
        return [Y[2],Y[3],*np.asarray(rhs(*Y[2:]),float).reshape(2)]
    pieces=[solve_ivp(bgflow,(0,sign*L),seed,method='DOP853',rtol=1e-12,
        atol=1e-14,max_step=L/32,dense_output=True) for sign in [-1,1]]
    if not all(sol.success for sol in pieces):
        raise RuntimeError('Background integration failed')
    cf=s.lambdify((N,A,u,b,up,bp),coeff.subs({a0:1,Lam:ratio}),'numpy')
    jf=s.lambdify((N,A,u,b,up,bp,wp,vp,c),jet.subs({a0:1,Lam:ratio}),'numpy')
    chi=(1-y0)*np.exp(-y0)
    if chi==0:
        raise ValueError('Excluded chi=0 chart')
    forcing=-float(s.sympify(curved_matter_jets()['proper_time_stress_acceleration_coefficient']))
    def profile(x):
        return np.exp(1-1/(1-9*x*x)) if abs(x)<1/3 else 0.
    def values(x):
        n,a,uu,bb=pieces[0 if x<0 else 1].sol(L*x)
        upp,bpp=np.asarray(rhs(uu,bb),float).reshape(2)
        n,a=np.exp(n),np.exp(a)
        C=np.asarray(cf(n,a,uu,bb,upp,bpp),float)
        C*=np.array([L**2,L,1,L**2/chi,L/chi,1/chi]); C[1,:]*=chi
        return n,a,uu,bb,upp,bpp,C
    def flow(x,Y,scaled_c,active):
        n,a,_,_,_,_,C=values(x)
        target=np.array([0.,chi*forcing*n*n*profile(x)*active+2*scaled_c/n])
        low=C[:,[0,1,3,4]]@Y[[0,1,2,3]]
        second=np.linalg.solve(C[:,[2,5]],target-low)
        return np.array([Y[1],second[0],Y[3],second[1],a*a*Y[0]])
    def solve(method,rtol,atol):
        cols=[]
        for init,cc,ff in [([0,0,0,0,0],0.,1.),([0,1,0,0,0],0.,0.),
                            ([0,0,0,1,0],0.,0.),([0,0,0,0,0],1.,0.)]:
            sol=solve_ivp(lambda x,Y:flow(x,Y,cc,ff),(-1,1),init,method=method,
                rtol=rtol,atol=atol,max_step=1/40,dense_output=True)
            if not sol.success:
                raise RuntimeError('Response integration failed')
            cols.append(sol)
        matrix=np.column_stack([sol.y[[0,2,4],-1] for sol in cols[1:]])
        weights=np.linalg.solve(matrix,-cols[0].y[[0,2,4],-1])
        def dense(x):
            return cols[0].sol(x)+sum(wt*sol.sol(x) for wt,sol in zip(weights,cols[1:]))
        jets=[]
        for x in [-1,1]:
            n,a,uu,bb,upp,bpp,_=values(x); Y=dense(x)
            jets.append(float(jf(n,a,uu,bb,upp,bpp,L*Y[1],L*Y[3]/chi,weights[2]/chi)))
        return dense,weights[2],matrix,np.array(jets)
    coarse=solve('RK45',1e-9,1e-12); fine=solve('DOP853',1e-12,1e-14)
    dense,scaled_c,matrix,jets=fine; grid=np.linspace(-1,1,401); Y=dense(grid)
    residual=[]; dx=1e-5
    for x in np.linspace(-.99,.99,81):
        numeric=(dense(x+dx)-dense(x-dx))/(2*dx); predicted=flow(x,dense(x),scaled_c,1.)
        residual.append(np.max(abs(numeric-predicted)/(1+abs(predicted))))
    refinement=float(max(np.max(abs(Y-coarse[0](grid))/(1+abs(Y))),
        np.max(abs(jets-coarse[3]))/(1+np.max(abs(jets)))))
    return dict(y0=y0,Lambda_over_a0_squared=ratio,L=L,
        normalized_fifth_wall_jets=jets.tolist(),global_c=float(scaled_c/chi),
        boundary_matrix=matrix.tolist(),computed_boundary_rank=int(np.linalg.matrix_rank(matrix)),
        boundary_residual=float(np.max(abs(Y[[0,2,4]][:,[0,-1]]))),
        ODE_residual=float(max(residual)),refinement_difference=refinement,
        fifth_wall_jet_absolute_refinement=float(np.max(abs(jets-coarse[3]))),
        methods=['RK45','DOP853'],rtols=[1e-9,1e-12],atols=[1e-12,1e-14])


def signed_profile_control():
    # Frozen-operator repair only. f is smooth, compactly supported, zero mean,
    # and has a nonzero constant plateau. sigma=-f'' vanishes on that plateau.
    x,chi=s.symbols('x chi',real=True); f=s.Function('f')(x)
    V=6*f/(1-chi); W=-chi*V; sigma=-s.diff(f,x,2)
    residuals=[s.factor(-4*(s.diff(W,x,2)+chi*s.diff(V,x,2))),
        s.factor(-4*(s.diff(W,x,2)+s.diff(V,x,2))-24*sigma)]
    return dict(operator_residuals=[str(r) for r in residuals],
        curvature_on_plateau=str(s.factor(-3*W)),
        assumptions='f smooth compact support, integral f=0, nonzero constant observer plateau; '
            'c=0 follows from integral P=integral f=0, not imposed on general sources.',
        scope='Only frozen leading operator. Neither full background lifting nor all-order shared walls established.')


def audit():
    start=time.monotonic(); _,_,_,symbolic=derive_wall()
    rows=[wall_response(.5,0.,.02),wall_response(.5,0.,.01),
        wall_response(10.5,float(32*s.pi),.002),wall_response(10.5,float(32*s.pi),.001)]
    signed=signed_profile_control()
    exactkeys=['kinetic_reduction_residual','normal_fourth_identity_residual',
        'KG_fifth_identity_residual','on_shell_reduction_residual','wall_third_jet','wall_fourth_jet']
    checks=dict(action_and_KG_jet_identities=all(symbolic[k]=='0' for k in exactkeys),
        numerical_response_resolved=all(r['boundary_residual']<1e-9 and r['ODE_residual']<1e-6
            and r['refinement_difference']<1e-6 for r in rows),
        signed_frozen_control=all(v=='0' for v in signed['operator_residuals']))
    incompatible=any(max(abs(v) for v in row['normalized_fifth_wall_jets'])
        >100*max(row['fifth_wall_jet_absolute_refinement'],1e-12) for row in rows)
    return dict(symbolic=symbolic,responses=rows,signed_control=signed,checks=checks,
        original_shared_C5_wall_gate='FAIL' if incompatible else 'UNRESOLVED',
        runtime_seconds=time.monotonic()-start,
        verdict='Original nonnegative-bump pair fails shared C5 Dirichlet matter-wall compatibility '
            'in the stated perturbative family; this limits the earlier conditional causal witness. '
            'Signed frozen-profile repair is not full theory closure.')


def main():
    p=argparse.ArgumentParser(description=__doc__); p.add_argument('--output',type=Path)
    p.add_argument('--require-shared-C5-walls',action='store_true'); args=p.parse_args(); r=audit()
    if args.output:
        args.output.write_text(json.dumps(r,indent=2,sort_keys=True)+'\n')
    for i,(key,val) in enumerate(r['checks'].items(),1):
        print('[%s] %02d %s'%('ok' if val else 'FAIL',i,key))
    print('Computed small-slab fifth jet:',r['symbolic']['positive_bump_small_slab_fifth_jet'])
    for row in r['responses']:
        print('y0',row['y0'],'L',row['L'],'wall jets',row['normalized_fifth_wall_jets'])
    print('Original shared-C5-wall gate:',r['original_shared_C5_wall_gate'])
    if not all(r['checks'].values()):
        return 1
    return 2 if args.require_shared_C5_walls and r['original_shared_C5_wall_gate']=='FAIL' else 0


if __name__=='__main__':
    raise SystemExit(main())
