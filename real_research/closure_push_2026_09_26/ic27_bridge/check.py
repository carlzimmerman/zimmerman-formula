#!/usr/bin/env python3
"""CD26-2: exact IC27 obstruction and an explicit IC28-family de Sitter action.

No existing research module is executed. SymPy checks displayed identities;
mpmath checks one parameter witness, not an interval theorem or a global PDE.
"""
import argparse
import json
import mpmath as mp
import sympy as s


def symbolic():
    S, q, z, R, w, A, D, E = s.symbols('S q z R w A D E', real=True)
    V = s.Function('V')(S)
    v0 = s.exp(S+2*w)/2
    v = v0+z*z
    h = -s.exp(2*S)*q*q/(6*v)-A*q*z-V-D*z*z-E*z**4-v*R
    hz = s.diff(h,z)
    out = {}
    def check(name, expression):
        value = s.factor(s.simplify(expression))
        assert value == 0, (name,value)
        out[name] = str(value)
    check('raw_auxiliary_equation', hz-(s.exp(2*S)*q*q*z/(3*v*v)-A*q-2*(D+R)*z-4*E*z**3))
    check('curvature_obstruction', s.diff(hz,R)+2*z)
    R1,R2 = s.symbols('R1 R2',real=True)
    check('two_curvature_residual_difference',hz.subs(R,R1)-hz.subs(R,R2)+2*z*(R1-R2))
    # Add lambda(z-Z(S)), then eliminate z,lambda by their actual equations.
    Z, Zp, Zpp, hss, hsz, hzz, hz0, lm = s.symbols('Z Zp Zpp hss hsz hzz hz0 lm',real=True)
    aux = s.Matrix([[hss-lm*Zpp,hsz,-Zp],[hsz,hzz,1],[-Zp,1,0]])
    check('holonomic_auxiliary_determinant',aux.det().subs(lm,-hz0)+hss+2*Zp*hsz+Zp**2*hzz+hz0*Zpp)
    b,c = s.symbols('b c',positive=True)
    htied = -s.exp(S)*q*q/(6*b)-A*q*c*s.exp(S/2)-V-D*c*c*s.exp(S)-E*c**4*s.exp(2*S)-b*s.exp(S)*R
    check('tied_branch_zero_aUV',s.exp(S)/(6*b)+s.diff(htied,q,2)/2)
    # Constant tensor action keeps the independent z auxiliary.
    t=s.exp(2*S)/v0
    hc=-t*q*q/6-A*q*z-V-D*z*z-E*z**4-v0*R
    hzzc=s.diff(hc,z,2)
    def reduced(i,j):
        return s.diff(hc,i,j)-s.diff(hc,i,z)*s.diff(hc,j,z)/hzzc
    check('constant_tensor_mass',2*s.exp(S-2*w)/t-1)
    check('constant_tensor_cone',-t*s.diff(hc,R)-s.exp(2*S))
    check('constant_tensor_auxiliary_schur',t/6+reduced(q,q)/2-A*A/(4*D+24*E*z*z))
    check('constant_tensor_HqR',reduced(q,R))
    check('constant_tensor_HRR',reduced(R,R))
    check('constant_tensor_HSR',reduced(S,R)+v0)
    # Exact fixed-function de Sitter construction, E4=0, A constant.
    S0,q0,m = s.symbols('S0 q0 m',real=True,nonzero=True)
    ell=-V/q0**2+m*(S-S0)**2/(2*q0**2)
    gamma=t/6-ell
    dfn=A*A/(4*gamma)
    zstar=-A*q/(2*dfn)
    hr=s.simplify(hc.subs({D:dfn,E:0,z:zstar},simultaneous=True))
    target=-ell*q*q-V-v0*R
    check('exact_auxiliary_elimination',hr-target)
    shell={q:q0,S:S0,R:0}
    check('de_sitter_zero_h',target.subs(shell))
    check('de_sitter_zero_lapse',s.diff(target,S).subs(shell))
    check('de_sitter_lapse_schur',s.diff(target,S,2).subs(shell)+m)
    check('de_sitter_trace_velocity',s.diff(target,q).subs(shell)/2-V.subs(S,S0)/q0)
    # All wavelengths, including k^2 redshift; no frozen-mixing shortcut.
    p,a,B,C,H,vv,mm=s.symbols('p a B C H v m',positive=True)
    M=-mm-2*B*p
    K=a-C*C/(2*M)
    L=2*C*vv*p/M
    W=-2*vv*p-8*vv*vv*p*p/M
    omega=s.factor(K*W-L*L+2*H*p*K*s.diff(L/K,p)-3*H*L)
    n0=(C*C+2*a*mm)*(C*(2*H-C)-2*a*mm)
    n1=8*a*(B*C*(3*H-C)+C*C*vv+2*a*mm*(vv-B))
    n2=16*B*a*a*(2*vv-B)
    denom=(2*B*p+mm)*(4*B*a*p+C*C+2*a*mm)
    check('exact_time_dependent_oscillator',omega*denom-p*vv*(n0+n1*p+n2*p*p))
    damp=3*H+2*H*p*s.diff(K,p)/K
    check('damping_lower_bound_identity',(damp-H)*denom-2*H*(2*a*(mm+2*B*p)**2+mm*C*C))
    check('physical_UV_speed',s.limit(omega/p,p,s.oo)-2*a*vv*(2*vv-B)/B)
    # Physical response. p=k^2 redshifts; background S,z,q are constant.
    generator=s.Matrix([[L,K],[-W,-3*H-L]])
    lapse_row=s.Matrix([[-4*vv*p/(mm+2*B*p),C/(mm+2*B*p)]])
    lapse_row_dot=-2*H*p*lapse_row.diff(p)+lapse_row*generator
    # dq=4vp*zeta/C+(m+2Bp)*deltaS/C; this is local in space.
    inverse_chart=s.Matrix([[1,0],[4*vv*p/C,(mm+2*B*p)/C]])
    lapse_flow=s.simplify(lapse_row_dot*inverse_chart)
    Q=(2*vv*(C-2*H)*p-16*a*vv*vv*p*p/C)/(mm+2*B*p)
    RR=-H-4*a*vv*p/C-2*H*mm/(mm+2*B*p)
    check('lapse_time_derivative_zeta_channel',lapse_flow[0]-Q)
    check('lapse_time_derivative_lapse_channel',lapse_flow[1]-RR)
    mcrit=B*C*(2*H-C)/(4*a*vv)
    check('first_channel_repaired',Q.subs(mm,mcrit)+8*a*vv*vv*p/(B*C))
    check('second_channel_irreducible_residue',(mm+2*B*p)*(RR+H+4*a*vv*p/C)+2*H*mm)
    psi=s.Matrix([[-1,H/(2*vv*p)]])
    psi_dot=s.simplify(-2*H*p*psi.diff(p)+psi*generator)
    expected=s.Matrix([[H,-a-H*H/(2*vv*p)]])+(H-C/2)*lapse_row
    for i in range(2):check('physical_potential_first_derivative_'+str(i),psi_dot[i]-expected[i])
    check('physical_chart_determinant',psi.col_join(psi_dot).det()-(4*B*a*p+(C-2*H)**2+2*a*mm)/(2*(2*B*p+mm)))
    # For zeta=0,deltaS=p*f, outside supp f:
    # RR*p*f -> H*m^2/B * (m-2B*Delta)^(-1) f.
    check('compact_data_nonlocal_lapse_tail',RR*p-(-H*p-4*a*vv*p*p/C-H*mm/B+H*mm*mm/(B*(mm+2*B*p))))
    # Exceptional, distinct candidate m=0,C=2H: retain k=0 separately.
    # The physical coordinate is (Psi,dq), not the original zeta.
    Jpsi=s.Matrix([[-1,H/(2*vv*p)],[0,1]])
    physical_generator=s.simplify((-2*H*p*Jpsi.diff(p)+Jpsi*generator)*Jpsi.inv())
    exceptional=s.simplify(physical_generator.subs({mm:0,C:2*H}))
    target_exceptional=s.Matrix([[-H,-a],[2*vv*(2*vv/B-1)*p,-2*H]])
    for i in range(2):
        for j in range(2):
            check('exceptional_local_generator_'+str(i)+str(j),exceptional[i,j]-target_exceptional[i,j])
    # Psi''+3H Psi'+[2H^2+2av(2v/B-1)p]Psi=0.
    check('exceptional_local_oscillator',(-2*H*p*target_exceptional.diff(p)+target_exceptional*target_exceptional)[0,0]
          +3*H*target_exceptional[0,0]+2*H*H+2*a*vv*(2*vv/B-1)*p)
    F,rho,Vp,Vpp=s.symbols('F rho Vp Vpp',real=True,nonzero=True)
    check('factorized_matter_schur',(Vpp*F+rho).subs(F,-rho/Vp)-rho*(1-Vpp/Vp))
    L0,L1,L2,V0,V1,V2,rr=s.symbols('L0 L1 L2 V0 V1 V2 rr',real=True)
    check('general_matter_lapse_schur',(-L2*q*q-V2+rr).subs(rr,L1*q*q+V1)-((L1-L2)*q*q+V1-V2))
    check('general_matter_no_slip_momentum_condition',(-2*L1*q)-2*(-L0*q)+2*q*(L1-L0))
    # New flattened-P0 action: V=e^S P_Lambda, L=e^S ell. This changes
    # the original active-pin potential and is not the old action's result.
    ell,rhop,wf,e2=s.symbols('ell rhop wf e2',real=True)
    zz,rp,ju,du=s.symbols('zeta Rp J_unitary drho_unitary',real=True)
    n=(2*H*rp+3*H*ju-4*vv*p*zz+du)/(2*B*p)
    chi=-e2*rp/(2*vv*p)
    zdot=a*rp-s.Rational(3,2)*ell*ju+H*n
    flows={zz:zdot,rp:-3*H*rp+2*vv*p*zz+2*vv*p*n,
           ju:-3*H*ju+rhop*n+wf*du,
           du:-3*H*(1+wf)*du-rhop*p*chi-e2*p*ju-3*rhop*zdot,
           H:-s.Rational(3,2)*ell*rhop,p:-2*H*p,rhop:-3*H*(1+wf)*rhop}
    dt=lambda expr:sum(s.diff(expr,key)*value for key,value in flows.items())
    Ps=-zz+H*rp/(2*vv*p); Tb=-rp/(2*vv*p)
    Jb=ju-rhop*rp/(2*vv*p); Dc=(du+3*H*ju)/p
    drb=du+3*H*rhop*rp/(2*vv*p)
    check('flat_potential_physical_Psi_flow',dt(Ps)-(-H*Ps+2*a*vv*p*Tb+s.Rational(3,2)*ell*Jb))
    check('flat_potential_physical_clock_flow',dt(Tb)-(-(2*vv/B-1)*Ps-Dc/(2*B)))
    check('flat_potential_comoving_density_flow',dt(Dc)-(-H*Dc+6*a*vv*rhop*Tb-e2*Jb))
    check('flat_potential_matter_momentum_flow',dt(Jb)-(-3*H*Jb+wf*drb+rhop*Ps))
    check('flat_potential_density_constraint',drb-(p*Dc-3*H*Jb))
    check('flat_potential_lapse_is_local_in_physical_chart',n-(2*vv/B*Ps+Dc/(2*B)))
    # Order (T_B,D_c,Psi,J_B); wave-number derivatives enter only the
    # displayed principal diagonal after eliminating the last two fields.
    Gp=s.Matrix([[0,-1/(2*B),-(2*vv/B-1),0],
                 [6*a*vv*rhop,-H,0,-e2],
                 [2*a*vv*p,0,-H,s.Rational(3,2)*ell],
                 [0,wf*p,rhop,-3*H*(1+wf)]])
    Gpdot=-2*H*p*Gp.diff(p)-s.Rational(3,2)*ell*rhop*Gp.diff(H)-3*H*(1+wf)*rhop*Gp.diff(rhop)
    accel=Gpdot+Gp*Gp
    for i in range(2):
        for j in range(4):
            want=-2*a*vv*(2*vv/B-1) if (i,j)==(0,0) else (-e2*wf if (i,j)==(1,1) else 0)
            check('flat_potential_principal_'+str(i)+str(j),s.diff(accel[i,j],p)-want)
    # The actual IC20 B(S) obstructs promoting homogeneous lapse degeneracy
    # to a symmetry of the full inhomogeneous Hamiltonian.
    up=(S+2*w)/(S+w); BB=s.exp(S+2*w)*(1-up*up)
    check('nonlinear_gradient_scaling_defect',s.diff(BB,S)-BB-2*w*s.exp(S+2*w)*up/(S+w)**2)
    # Further explicit active-pin action: B_new=b exp(S). The lapse equation
    # is a spectral constraint after y=exp(S/2), not an arbitrary-data inverse.
    b,Afield,Sx,Sxx,y,yx,yxx=s.symbols('b Afield Sx Sxx y yx yxx',real=True,nonzero=True)
    density=s.exp(S)*(Afield-b*Sx*Sx)
    euler=s.diff(density,S)-(s.diff(s.diff(density,Sx),S)*Sx+s.diff(s.diff(density,Sx),Sx)*Sxx)
    check('repaired_nonlinear_lapse_Euler',euler-s.exp(S)*(Afield+b*(Sx*Sx+2*Sxx)))
    check('positive_lapse_substitution',(Sx*Sx+2*Sxx).subs({Sx:2*yx/y,Sxx:2*yxx/y-2*yx*yx/y**2})-4*yxx/y)
    ff,fx=s.symbols('f fx',real=True)
    # One-dimensional pointwise identity before integration by parts. The
    # divergence generalizes with grad/div on the leaf.
    divergence=(yx*yx+y*yxx)*ff*ff+2*y*yx*ff*fx
    check('ground_state_energy_identity',4*b*(yx*ff+y*fx)**2+4*b*y*yxx*ff*ff-4*b*y*y*fx*fx-4*b*divergence)
    beta=s.symbols('beta',positive=True)
    check('repaired_positive_speed_example',(2*(1/(12*beta))*beta*(2*beta/beta-1))-s.Rational(1,6))
    # The background-independent IC30 static algebra, E4=0.
    ts,ds,aa,zz=s.symbols('ts ds aa zz',real=True,nonzero=True)
    check('static_auxiliary_coefficient',aa*(-3*aa*zz/ts)+2*ds*zz-zz*(2*ds-3*aa*aa/ts))
    return out


def witness(dps):
    mp.mp.dps=dps
    w=-mp.mpf(1)/40; S0=mp.mpf(5); A=mp.mpf(1)/10
    primitive=lambda c:(1-c)*(mp.log(1-c)**2-2*mp.log(1-c)+2)-2
    olda=27*mp.exp(-mp.mpf(1)/2)/(8*mp.log(mp.mpf(9)/5)**2)
    lam=6*mp.exp(-mp.mpf(1)/2)-olda*primitive(mp.mpf(4)/9)
    a02=lam/(32*mp.pi)
    P=lambda S:-mp.exp(4*w)*(lam+a02*primitive(((S+2*w)/(S+w))**2))+3*mp.exp(2*w-2*S)
    V=lambda S:mp.exp(S)*P(S)
    t=lambda S:2*mp.exp(S-2*w)
    u=(S0+2*w)/(S0+w); vv=mp.exp(S0+2*w)/2
    cg=mp.mpf(1)/10
    a=t(S0)*cg*(1-u*u)/(2*u*u)
    ell0=t(S0)/6-a
    q0=-mp.sqrt(-V(S0)/ell0)
    H=-ell0*q0; C=2*mp.diff(V,S0)/q0
    mmax=C*(2*H-C)/(2*a); mm=mmax/2
    ell=lambda S:-V(S)/q0**2+mm*(S-S0)**2/(2*q0**2)
    df=lambda S:A*A/(4*(t(S)/6-ell(S)))
    z0=-A*q0/(2*df(S0)); B=2*vv*(1-u*u)
    h=lambda S,q,z:-t(S)*q*q/6-A*q*z-V(S)-df(S)*z*z
    hzz=mp.diff(lambda zz:h(S0,q0,zz),z0,2)
    hsz=mp.diff(lambda SS:mp.diff(lambda zz:h(SS,q0,zz),z0),S0)
    hss=mp.diff(lambda SS:h(SS,q0,z0),S0,2)
    residuals={'h':h(S0,q0,z0),'hS':mp.diff(lambda SS:h(SS,q0,z0),S0),
               'hz':mp.diff(lambda zz:h(S0,q0,zz),z0),
               'schur_plus_m':hss-hsz*hsz/hzz+mm,
               'physical_UV_minus_target':2*a*vv*u*u/(mp.exp(2*S0)*(1-u*u))-cg}
    n0=(C*C+2*a*mm)*(C*(2*H-C)-2*a*mm)
    n1=8*a*(B*C*(3*H-C)+C*C*vv+2*a*mm*(vv-B))
    n2=16*B*a*a*(2*vv-B)
    assert V(S0)<0 and 0<mp.diff(P,S0)<-P(S0)
    assert 0<a<t(S0)/6 and 0<C<2*H and 0<B<vv and 0<mm<mmax
    assert min(n0,n1,n2)>0
    assert (-mp.exp(-3*w)*q0/(3*mp.mpf('.5')))**2>mp.mpf('.75')
    assert max(abs(x) for x in residuals.values())<mp.mpf(10)**(-dps+12)
    # Source-fixed action test: solve actual lapse/auxiliary equations for new
    # positive matter at Q=0, keeping the SAME D and same q0. No reconstruction.
    source_rows=[]
    for rho in ['0','0.000001','0.001']:
        rho=mp.mpf(rho)
        rhoS=lambda S:rho*mp.exp(S-S0)
        fs=lambda S,z:mp.diff(lambda SS:h(SS,q0,z),S)+rhoS(S)
        fz=lambda S,z:-A*q0-2*df(S)*z
        ss,zz=mp.findroot((fs,fz),(S0,z0),tol=mp.mpf(10)**(-dps+10))
        source_rows.append({'rho_at_S0':str(rho),'S':str(ss),'z':str(zz),
                            'max_constraint_residual':str(max(abs(fs(ss,zz)),abs(fz(ss,zz))))})
    # Coefficient domain is only sampled here; continuity yields an unspecified
    # open interval analytically. This is not interval-certified global D.
    domain=[]
    for dx in ['-.001','0','.001']:
        ss=S0+mp.mpf(dx)
        domain.append({'S':str(ss),'D':str(df(ss)),'L':str(ell(ss)),
                       'gamma':str(t(ss)/6-ell(ss))})
    nums=dict(S0=S0,wc=w,A=A,Lambda=lam,a02=a02,P0=P(S0),Pprime=mp.diff(P,S0),
              V=V(S0),Vprime=mp.diff(V,S0),q0=q0,z0=z0,H_coordinate=H,
              H_proper=H/mp.exp(S0+w),C=C,C_over_H=C/H,m0=mm,mmax=mmax,
              aUV=a,B=B,v=vv,t=t(S0),D=df(S0),physical_UV_speed_squared=cg,
              n0=n0,n1=n1,n2=n2,static_gap_on_pin=2*df(S0)-3*A*A/t(S0),
              first_channel_repair_m=B*C*(2*H-C)/(4*a*vv),
              irreducible_metric_tail_prefactor=(H-C/2)*H*mm*mm/B)
    # Independent exceptional fixed action, m=0. P0 has a local minimum.
    Se=mp.findroot(lambda SS:mp.diff(P,SS),(mp.mpf('3.8'),mp.mpf('4.1')))
    ue=(Se+2*w)/(Se+w); ve=mp.exp(Se+2*w)/2
    ae=t(Se)*cg*(1-ue*ue)/(2*ue*ue); Le=t(Se)/6-ae
    qe=-mp.sqrt(-V(Se)/Le); He=-Le*qe
    De=lambda SS:A*A/(4*(t(SS)/6+V(SS)/qe**2))
    rhoe=mp.mpf('0.000001')
    qe_matter=-mp.sqrt(qe*qe*(1-rhoe/mp.diff(V,Se)))
    Me=rhoe*(1-mp.diff(V,Se,2)/mp.diff(V,Se))
    Be=2*ve*(1-ue*ue); Ce=-2*(-mp.diff(V,Se)/qe**2)*qe_matter
    Ke0=ae-Ce*Ce/(2*Me)
    assert abs(mp.diff(P,Se))<mp.mpf(10)**(-dps+10)
    assert mp.diff(P,Se,2)>0 and V(Se)<0 and Me>0 and Ke0<0
    exceptional_record={k:str(value) for k,value in dict(S_star=Se,P0=P(Se),
        Pprime=mp.diff(P,Se),Psecond=mp.diff(P,Se,2),q0=qe,H=He,D=De(Se),
        scalar_speed_squared=cg,positive_matter_rho=rhoe,q_matter=qe_matter,
        matter_lapse_schur=Me,positive_k_squared_auxiliary_pole=Me/(2*Be),
        low_k_scalar_K=Ke0).items()}
    return {'dps':dps,'numbers':{k:str(v) for k,v in nums.items()},
            'residuals':{k:str(v) for k,v in residuals.items()},
            'fixed_action_matter_response':source_rows,'sampled_coefficient_domain':domain,
            'exceptional_vacuum_candidate_and_matter_control':exceptional_record}


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--output',required=True)
    args=parser.parse_args()
    checks=symbolic(); rows=[witness(50),witness(80)]
    keys=rows[0]['numbers'].keys()
    err=max(abs(mp.mpf(rows[0]['numbers'][k])-mp.mpf(rows[1]['numbers'][k]))/
            max(1,abs(mp.mpf(rows[1]['numbers'][k]))) for k in keys)
    assert err<mp.mpf('1e-40')
    result={'scope':'Exact symbolic local action identities; finite-precision vacuum witness. Full theory OPEN.',
            'symbolic_checks':checks,'witnesses':rows,'max_precision_relative_change':str(err),
            'flattened_potential_candidate':'Separate constant-P0 active-pin action; local physical matter system. A further B=b exp(S) gradient counterterm gives an exact nonlinear positive-lapse ground-state equation; existence and full constraint preservation are not assumed.',
            'non_claims':['No globally extended coefficient action or solved pin transition',
                          'No matter cosmology, nonlinear health, PPN or causal-support theorem',
                          'Positive oscillator coefficients are not a global nonlinear stability theorem']}
    with open(args.output,'w') as f:json.dump(result,f,indent=2)
    print(json.dumps({'symbolic_checks':len(checks),'precision_relative_change':str(err),
                      'q0':rows[-1]['numbers']['q0'],'m0':rows[-1]['numbers']['m0'],
                      'full_theory':'OPEN'}))


if __name__=='__main__':main()
