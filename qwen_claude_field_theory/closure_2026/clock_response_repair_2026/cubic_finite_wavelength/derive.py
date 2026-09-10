#!/usr/bin/env python3
"""Quadratic ADM action for a real finite-k scalar mode of the SAME cubic clock.

The action, lapse/shift block and kinetic rank are differentiated, not supplied.
Unitary tau=t; h_ij=a² exp(2 zeta) delta_ij; N^x=epsilon b sin(kx).
"""
import argparse
import json
from pathlib import Path
import sympy as s


def derive():
    a,H,q,M,gamma,k=s.symbols('a H q M2 gamma k',nonzero=True,real=True)
    ep,c,sn=s.symbols('epsilon cosine sine',real=True)
    z,zd,sigma,sd,n,b=s.symbols('z zd sigma sd n b',real=True)
    P,PX,PXX,W,WY,V,Lambda=s.symbols('P PX PXX W WY V Lambda',real=True)
    lapse=1+ep*n*c; conf=s.exp(ep*z*c);vol=a**3*conf**3
    shift=ep*b*sn;shift_x=ep*b*k*c
    z_x=-ep*k*z*sn;chi_x=-ep*k*sigma*sn
    D=H+ep*zd*c-shift*z_x
    Q=(q+ep*sd*c-shift*chi_x)/lapse
    Y=chi_x**2/(a*a*conf**2)
    X=Q*Q-Y;DX=X-q*q
    Kx=(D-shift_x)/lapse;Ky=D/lapse;trace=Kx+2*Ky
    lapchi=(-ep*k*k*sigma*c+z_x*chi_x)/(a*a*conf**2)
    R3=(-4*(-ep*k*k*z*c)-2*z_x*z_x)/(a*a*conf**2)
    # chi^i D_i Y begins at order epsilon^3 on this homogeneous background.
    cubic=gamma*(-s.Rational(2,3)*Q**3*trace+2*Q*Kx*Y+2*Q*Q*lapchi)
    raw=vol*lapse*(M*(Kx*Kx+2*Ky*Ky-trace*trace+R3-2*Lambda)/2+
        P+PX*DX+PXX*DX**2/2-V+cubic)+vol*(W+WY*Y)
    local2=s.expand(s.diff(raw,ep,2).subs(ep,0)/2)
    # Exact period average at quadratic order, no collocation or numerical quadrature.
    moments={(0,0):1,(1,0):0,(0,1):0,(2,0):s.Rational(1,2),
             (0,2):s.Rational(1,2),(1,1):0}
    L2=s.expand(sum(coef*moments[powers] for powers,coef in s.Poly(local2,c,sn).terms()))
    # Independent compact ADM derivation, supplied before seeing this expansion.
    f=-3*M*H*H+P-V-M*Lambda-2*gamma*q**3*H
    fh=s.diff(f,H);j=s.diff(f,q)+2*q*PX
    energy=H*fh+q*j-f;uv=zd-H*n;ev=sd-q*n
    shift_potential=-a*a*b/k;Bchi=2*PX+4*q*q*PXX
    compact=(-3*M*uv**2-6*gamma*q*q*uv*ev+(Bchi-12*gamma*H*q)*ev**2/2+
        3*z*(fh*zd+j*sd-energy*n)+s.Rational(9,2)*(f+W)*z*z+
        k*k/(a*a)*(M*z*z+2*M*n*z-(PX-WY-2*gamma*q*H)*sigma**2+
                    2*gamma*q*q*n*sigma-4*gamma*q*sigma*sd)-
        2*k*k/(a*a)*shift_potential*(M*uv+gamma*q*q*ev+j*sigma/2))
    assert s.expand(L2-a**3*compact/2)==0
    L0=s.factor(raw.subs(ep,0))
    assert s.factor(L0-a**3*(-3*M*H*H+P-V-M*Lambda-2*gamma*q**3*H+W))==0
    # Full finite-k lapse and longitudinal-shift Euler equations.
    aux=s.Matrix([n,b]);dyn=s.Matrix([zd,sd,z,sigma])
    F=s.hessian(L2,[n,b]);cross=s.Matrix([[s.diff(L2,v,w) for w in dyn] for v in aux])
    detF=s.factor(F.det());sol=-F.inv()*cross*dyn
    reduced_matrix=s.simplify(s.hessian(L2,list(dyn))-cross.T*F.inv()*cross)
    red=s.factor((dyn.T*reduced_matrix*dyn)[0]/2)
    assert s.factor(red-L2.subs({n:sol[0],b:sol[1]},simultaneous=True))==0
    K=s.simplify(reduced_matrix[:2,:2]);velocity_det=s.factor(K.det())
    assert velocity_det==0
    # A zero determinant is not enough: compute the actual rank and null vector.
    rank=K.rank();null=K.nullspace()
    assert (K*s.Matrix([H,q])).applyfunc(s.factor)==s.zeros(2,1)
    # Evaluate the SPECIFIED repaired background, not an extra fitting step.
    A,U,B0,qd=s.symbols('A U B0 qdot',real=True)
    bg={P:0,PX:A/(2*q)+3*gamma*q*H,PXX:(B0-A/q)/(4*q*q),
        W:U-2*gamma*q*q*qd,WY:A*U/(2*q*(q*A+U)),V:U,
        Lambda:3*H*H-(q*A+U)/M}
    Kbg=K.subs(bg).applyfunc(s.factor)
    Cbg=reduced_matrix[:2,2:].subs(bg).applyfunc(s.factor)
    Vbg=reduced_matrix[2:,2:].subs(bg).applyfunc(s.factor)
    hd=-(q*A+U)/(2*M)
    rates={a:a*H,H:hd,q:qd,A:-3*H*A,U:-A*qd-3*H*U}
    def dt(expr):return s.factor(sum(s.diff(expr,v)*r for v,r in rates.items()))
    r=q/H;T=s.Matrix([[1,0],[r,1]]);Td=s.Matrix([[0,0],[dt(r),0]])
    Kn=(T.T*Kbg*T).applyfunc(s.factor)
    Cn=(T.T*(Kbg*Td+Cbg*T)).applyfunc(s.factor)
    Vn=(T.T*Vbg*T+Td.T*Kbg*Td+Td.T*Cbg*T+T.T*Cbg.T*Td).applyfunc(s.factor)
    assert Kn[0,0]==0 and Kn[0,1]==0 and Kn[1,0]==0
    assert all(not ({B0,qd} & Cn[0,i].free_symbols) for i in range(2)), 'time-derivative rate list incomplete'
    # Integrate z*zd and u*zd by parts WITH the a³ time dependence included.
    constraint_z=s.factor(Vn[0,0]-dt(Cn[0,0]))
    mixing_velocity=s.factor(Cn[1,0]-Cn[0,1])
    mixing_field=s.factor(Vn[0,1]-dt(Cn[0,1]))
    effective_kinetic=s.factor(Kn[1,1]-mixing_velocity**2/constraint_z)
    effective_cross=s.factor(Cn[1,1]-mixing_velocity*mixing_field/constraint_z)
    # Keep this exact Schur expression; multivariate integer factorization of
    # its large numerator is unnecessary for evaluation or the Euler equation.
    effective_potential=Vn[1,1]-mixing_field**2/constraint_z
    def k2coef(e):return s.factor(s.diff(e,k,2).subs(k,0)/2)
    D2=k2coef(constraint_z);E2=k2coef(mixing_field)
    B2=k2coef(Cn[1,1]);C2=k2coef(Vn[1,1])-E2*E2/D2
    assert not ({B0,qd} & B2.free_symbols), 'high-k mixed derivative needs more rates'
    speed_infinity=s.factor(a*a*(dt(B2)-C2)/Kn[1,1])
    d=bg[WY];Sgamma=bg[W]-2*q*q*d
    assert s.factor(D2+a*Sgamma/(2*H*H))==0
    principal_K=B0-6*gamma*q*H+6*gamma**2*q**4/M
    principal_N=2*(A/(2*q)-d-gamma*(q*H+2*qd))-4*q*q*d*d/Sgamma-2*gamma**2*q**4/M
    assert s.factor(speed_infinity-principal_N/principal_K)==0
    facts=dict(conventions='real cosine mode averaged over a period; contravariant shift N^x=b sin(kx); tau=t',
        homogeneous_density=str(L0),quadratic_action=str(L2),lapse_shift_hessian=str(F),
        lapse_shift_determinant=str(detF),lapse_solution=str(s.factor(sol[0])),
        shift_solution=str(s.factor(sol[1])),reduced_velocity_matrix=str(K),
        reduced_velocity_determinant=str(velocity_det),reduced_velocity_rank=rank,
        reduced_velocity_nullspace=[str(v) for v in null],
        gauge_invariant_variable='u=sigma-(q/H)zeta',
        zeta_constraint_coefficient=str(constraint_z),mixing_velocity=str(mixing_velocity),
        mixing_field=str(mixing_field),effective_kinetic=str(effective_kinetic),
        effective_cross=str(effective_cross),effective_potential=str(effective_potential),
        constraint_k_squared_coefficient=str(D2),high_k_speed_squared=str(speed_infinity),
        high_k_includes_mixed_coefficient_time_derivative=True,
        reduced_Euler_equation='Aeff uddot + Adot_eff udot + (Bdot_eff-Ceff) u = 0',
        checks=dict(background_density=True,independent_raw_ADM_action=True,auxiliary_substitution=True,computed_kinetic_null=True,
                    transformed_nondynamical_coordinate=True,independent_principal_agreement=True,
                    exact_spatial_constraint_coefficient=True),
        scope='Exact quadratic scalar finite-k action on prescribed homogeneous repaired branch; not nonlinear DOF or CMB/galaxy certificate',
        full_theory_status='OPEN')
    ctx=dict(a=a,H=H,q=q,M=M,gamma=gamma,k=k,A=A,U=U,B0=B0,qd=qd,
        kinetic=effective_kinetic,cross=effective_cross,potential=effective_potential,
        constraint=constraint_z,velocity_mixing=mixing_velocity,field_mixing=mixing_field,
        pre_zeta_kinetic=Kn[1,1],quadratic_action=L2,lapse_shift_determinant=detF,
        constraint_k2=D2,high_k_speed=speed_infinity,raw_mixed=Cn[1,1],raw_potential=Vn[1,1])
    return facts,ctx

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--result-file',type=Path);args=p.parse_args()
    facts,_=derive()
    if args.result_file:args.result_file.write_text(json.dumps(facts,indent=2)+'\n')
    print(json.dumps(facts,indent=2))
