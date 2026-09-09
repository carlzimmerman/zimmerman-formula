#!/usr/bin/env python3
"""Physical metric observables of the fixed IC26 action, on its active pin.

Time derivatives are with respect to the varied clock coordinate T.
The k=0 shear is undefined and is deliberately not continued by division.
"""
import argparse
import json
import mpmath as mp
import sympy as s
import ic26_three_functions as action

OBSERVABLES=('Phi','Psi','delta_r_B','delta_m_B','clock_B')


def gauge_audit():
    """Derive pure-gauge perturbations from minus the background Lie derivative."""
    tau,x,y,z=s.symbols('tau x y z',real=True)
    k=s.symbols('k',positive=True);a=s.Function('a')(tau)
    time=s.Function('f')(tau)*s.cos(k*x)
    spatial=s.Function('ell')(tau)*s.cos(k*x)
    coords=(tau,x,y,z)
    xi=s.Matrix([time]+[s.diff(spatial,c) for c in coords[1:]])
    metric=s.diag(-1,a*a,a*a,a*a)
    perturb=s.zeros(4)
    for i in range(4):
        for j in range(4):
            perturb[i,j]=-sum(xi[n]*s.diff(metric[i,j],coords[n])
                +metric[n,j]*s.diff(xi[n],coords[i])
                +metric[i,n]*s.diff(xi[n],coords[j]) for n in range(4))
    phi=-perturb[0,0]/2
    psi=-perturb[2,2]/(2*a*a)
    b=perturb[0,1]*s.cos(k*x)/(-k*s.sin(k*x))
    E=(perturb[1,1]-perturb[2,2])/(-2*a*a*k*k)
    shear=b-a*a*s.diff(E,tau)
    H=s.diff(a,tau)/a
    rho=s.Function('rho')(tau);clock=s.Function('T')(tau)
    return {name:s.simplify(value) for name,value in dict(
        shear_time_shift=shear-time,
        lapse_potential=phi+s.diff(shear,tau),
        curvature_potential=psi-H*shear,
        density=-s.diff(rho,tau)*time+s.diff(rho,tau)*shear,
        clock=-s.diff(clock,tau)*time+s.diff(clock,tau)*shear).items()}


def constraint_fields(b,k_squared,phase):
    k2=mp.mpf(k_squared)
    if k2<=0:
        raise ValueError('Nonzero Fourier sector required; homogeneous shear has no inverse Laplacian')
    x=phase[:3];p=phase[3:];f=b['entries']
    source=p[0]-mp.mpf('1.5')*mp.fsum(row['j']*x[i+1] for i,row in enumerate(f))
    shear=-source/2
    chi=b['t']*shear/k2
    enthalpy=mp.fsum((1+row['w'])*row['h'] for row in f)
    lapse_source=b['red']['Sq']*p[0]+mp.fsum(row['u']*p[i+1] for i,row in enumerate(f))
    lapse_source+=(4*b['red']['SR']*k2-3*enthalpy)*x[0]
    M=b['M']-2*b['B']*k2
    if M==0:raise ValueError('Singular auxiliary lapse operator')
    return dict(s_TF=shear,chi=chi,delta_S=-lapse_source/M,M_k=M)


def reconstruct(b,k_squared,phase):
    """Independent lapse/curvature potentials, without imposing a slip ratio."""
    phase=mp.matrix(phase);r=constraint_fields(b,k_squared,phase)
    k2=mp.mpf(k_squared);dot=action.base.hamiltonian_generator(b,k2)*phase
    sd,_,zd=b['flow'];HQ=b['Qdot']
    wc=action.model.normalized.constants()['wc']
    v0=mp.exp(b['S']+2*wc)/2
    tlogdot=2*sd-(v0*sd+2*b['z']*zd)/b['v']
    sourcedot=dot[3]-mp.mpf('1.5')*mp.fsum(
        f['j']*(dot[i+1]-3*HQ*phase[i+1]) for i,f in enumerate(b['entries']))
    chidot=(tlogdot+2*HQ)*r['chi']-b['t']*sourcedot/(2*k2)
    E_inverse=mp.exp(-2*b['S'])
    Psi=-phase[0]-E_inverse*HQ*r['chi']
    Phi=r['delta_S']+E_inverse*(chidot-sd*r['chi'])
    r.update(Phi=Phi,Psi=Psi,chi_dot=chidot,clock_B=E_inverse*r['chi'],
             delta_r_B=(1+b['entries'][0]['w'])*(phase[4]/b['entries'][0]['j']+3*Psi),
             delta_m_B=(1+b['entries'][1]['w'])*(phase[5]/b['entries'][1]['j']+3*Psi))
    return r


def observable_matrix(b,k_squared):
    columns=[reconstruct(b,k_squared,mp.eye(6)[:,i]) for i in range(6)]
    return mp.matrix([[r[key] for r in columns] for key in OBSERVABLES])


def dressing_slip(b,k_squared,phase):
    """Predict metric slip from raw auxiliary variation, not the metric map."""
    r=constraint_fields(b,k_squared,phase);raw=b['raw'];k2=mp.mpf(k_squared)
    aux_source=raw['Sz']*r['delta_S']+raw['qz']*phase[3]+4*raw['zR']*k2*phase[0]
    dz=-aux_source/raw['zz']
    delta_log=2*dz/b['z']-r['delta_S']
    background_log_dot=2*b['flow'][2]/b['z']-b['flow'][0]
    invariant=delta_log+background_log_dot*mp.exp(-2*b['S'])*r['chi']
    return dict(delta_z=dz,dressing_perturbation_B=invariant,
                slip=-b['z']**2/b['v']*invariant,
                auxiliary_residual=raw['zz']*dz+aux_source)


def tensor_mass_variation(b,k_squared,phase):
    """Physical TT action coefficient: a_phys^3 M_T² (gamma_tau)²/8."""
    fields=constraint_fields(b,k_squared,phase)
    dz=dressing_slip(b,k_squared,phase)['delta_z']
    wc=action.model.normalized.constants()['wc'];v0=mp.exp(b['S']+2*wc)/2
    M2=2*mp.exp(b['S']-2*wc)/b['t']
    variation=(v0*fields['delta_S']+2*b['z']*dz)/b['v']-fields['delta_S']
    rate=(v0*b['flow'][0]+2*b['z']*b['flow'][2])/b['v']-b['flow'][0]
    invariant=variation+rate*mp.exp(-2*b['S'])*fields['chi']
    return dict(M_T_squared=M2,delta_log_M2_B=invariant,
                log_M2_background_rate=rate,
                nonclaim='Normalized action units; this is not the measured Newton constant')


def slip_audit():
    """Exact reduction from the unreduced quadratic Hamiltonian and h_z=0."""
    k,H,t,v,a,d,C,e,rr,ds=s.symbols('k2 H t v a d C e rr deltaS')
    zeta,p=s.symbols('zeta p')
    js=s.symbols('j1:3',nonzero=True);us=s.symbols('u1:3')
    ws=s.symbols('w1:3');sig=s.symbols('sigma1:3');si=s.symbols('s1:3')
    enthalpy=sum(j*u for j,u in zip(js,us))
    mass=s.Rational(9,2)*sum(w*j*u for w,j,u in zip(ws,js,us))
    mix=sum(j*x for j,x in zip(js,sig))
    # Explicit H2 before lapse elimination; irrelevant lapse-only term omitted.
    h=a*p*p+4*d*k*p*zeta-t*p*mix/2
    h+=sum(w*u*sx*sx/(2*j)-3*w*u*sx*zeta
           for w,u,j,sx in zip(ws,us,js,si))
    h+=(-2*v*k+8*rr*k*k+mass)*zeta*zeta+3*t*mix*mix/8
    h+=ds*(C*p+sum(u*sx for u,sx in zip(us,si))+(4*e*k-3*enthalpy)*zeta)
    pd=-s.diff(h,zeta)/2-3*H*p
    R=p-s.Rational(3,2)*mix
    Rd=pd-s.Rational(3,2)*sum(j*s.diff(h,sx)-3*H*j*x for j,sx,x in zip(js,si,sig))
    expected=-3*H*R-2*d*k*p+(2*v*k-8*rr*k*k)*zeta-2*e*k*ds
    v0,z,sd,zd,chi,hSz,hqz,hzz=s.symbols('v0 z sd zd chi hSz hqz hzz',nonzero=True)
    E=s.symbols('E',nonzero=True)
    vd=v0*sd+2*z*zd;tlog=2*sd-vd/v
    # Shift evolution from the already derived Rdot and chi=-t R/(2k²).
    cd=(tlog-H)*chi+t*d*p-t*v*zeta+4*t*rr*k*zeta+t*e*ds
    phi=ds+(cd-sd*chi)/E;psi=-zeta-H*chi/E
    general=(1+e/v)*ds+d*p/v+4*rr*k*zeta/v+(tlog-sd)*chi/E
    reduced={d:2*z*hqz/hzz,e:-v0+2*z*hSz/hzz,rr:-4*z*z/hzz}
    dz=-(hSz*ds+hqz*p-8*z*k*zeta)/hzz
    target=-z*z/v*(2*dz/z-ds+(2*zd/z-sd)*chi/E)
    return dict(momentum_shear_evolution=s.expand(Rd-expected),
        metric_slip=s.factor((phi-psi-general).subs(t,E/v)),
        auxiliary_dressing=s.factor((general.subs(reduced)-target).subs(v,v0+z*z)))


def kinetic_coordinates(b,k_squared):
    quad=action.prior.quadratic(b,k_squared)
    R=mp.cholesky(quad['A']).T
    Dinv=mp.diag([mp.mpf('.5'),1,1]);T=mp.zeros(6)
    X=R*2*Dinv*quad['L']/b['Qdot']
    P=R*2*Dinv*quad['K']/b['Qdot']
    for i in range(3):
        for j in range(3):
            T[i,j]=R[i,j];T[i+3,j]=X[i,j];T[i+3,j+3]=P[i,j]
    return T


def slip_row(b,k_squared):
    return mp.matrix([[dressing_slip(b,k_squared,mp.eye(6)[:,i])['slip'] for i in range(6)]])


def slip_preservation(b,k_squared):
    """Test invariance of the linear no-slip subspace, retaining its source."""
    k2=mp.mpf(k_squared);ell=slip_row(b,k2)
    derivative=mp.matrix([[mp.diff(lambda dt:slip_row(
        action.completed(action.moved(b,dt)),k2*mp.exp(-2*b['Qdot']*dt))[0,i],0)
        for i in range(6)]])
    rate=derivative+ell*action.base.hamiltonian_generator(b,k2)
    inverse=kinetic_coordinates(b,k2)**-1
    a=ell*inverse;c=rate*inverse
    aa=(a*a.T)[0]
    perpendicular=c if aa==0 else c-(c*a.T)[0]/aa*a
    norm=mp.norm(perpendicular)
    direction=perpendicular.T/norm if norm else mp.zeros(6,1)
    phase=inverse*direction
    rows=mp.matrix([list(a/mp.norm(a)) if mp.norm(a) else [0]*6,
                    list(c/mp.norm(c)) if mp.norm(c) else [0]*6])
    singular=list(mp.svd(rows,compute_uv=False))
    return dict(slip_row=list(ell),preservation_row=list(rate),
        normalized_singular_values=singular,
        sampled_row_rank=sum(x>mp.mpf('1e-25') for x in singular),
        zero_slip_phase=list(phase),initial_slip=(ell*phase)[0],
        initial_slip_derivative=(rate*phase)[0],
        maximum_slip_derivative_on_unit_kinetic_no_slip_sphere=norm,
        nonclaim='Finite-k cosmological no-slip subspace, not the galactic static branch or a PPN measurement')


def mode_observables(b,k_squared):
    spectrum=action.frequencies(b,k_squared)
    vector=mp.matrix(spectrum['fastest_mode_x_velocity'])
    quad=action.prior.quadratic(b,k_squared)
    x=vector[:3];velocity=mp.matrix(vector[3:])
    momentum=(quad['K']**-1)*(mp.diag([2,1,1])*velocity/2-quad['L']*mp.matrix(x))
    phase=mp.matrix(list(x)+list(momentum))
    normal=phase[0] if abs(phase[0])>mp.mpf('1e-35') else mp.norm(phase)
    phase/=normal
    metric=reconstruct(b,k_squared,phase);dressing=dressing_slip(b,k_squared,phase)
    tensor=tensor_mass_variation(b,k_squared,phase)
    return dict(all_roots=spectrum['roots'],fastest_root=spectrum['fastest_instantaneous_root'],
        mode_phase=list(phase),observables={key:metric[key] for key in OBSERVABLES},
        slip=metric['Phi']-metric['Psi'],
        dressing_identity_residual=metric['Phi']-metric['Psi']-dressing['slip'],
        tensor_mass=tensor,
        tensor_slip_residual=metric['Phi']-metric['Psi']+tensor['delta_log_M2_B'],
        eigen_residual=spectrum['residual'],
        normalization='zeta=1 unless |zeta|<1e-35, then unit phase norm',
        nonclaim='An instantaneous Euler eigenvector is not a finite-time cosmological growth history')


def report():
    with mp.workdps(50):
        history=action.evolve(1,max_step=.005,rtol=1e-12)
        points=[]
        for Q in (0,1):
            b=action.completed_at(history,Q)
            for k in ('.001','.01','.1','1','10','100'):
                k2=mp.mpf(k)
                points.append(dict(Q=Q,k_squared=k2,metric_map=observable_matrix(b,k2),
                    preservation=slip_preservation(b,k2),mode=mode_observables(b,k2)))
        exact={**gauge_audit(),**slip_audit()}
        checks=dict(exact_identities=all(v==0 for v in exact.values()),
            background=history['success'],
            zero_slip_initial_data=all(abs(x['preservation']['initial_slip'])<mp.mpf('1e-30') for x in points),
            eigen_residuals=all(x['mode']['eigen_residual']<mp.mpf('1e-30') for x in points),
            dressing_identity=all(abs(x['mode']['dressing_identity_residual'])<mp.mpf('1e-30') for x in points),
            tensor_slip_identity=all(abs(x['mode']['tensor_slip_residual'])<mp.mpf('1e-30') for x in points))
        return dict(full_theory='OPEN',checks=checks,exact_identities={k:str(v) for k,v in exact.items()},
            points=points,
            homogeneous_sector='k=0 has no uniquely reconstructible scalar shift from its gradient; IC26 background constraints remain separate',
            nonclaims=['No galactic Phi=Psi or PPN certificate from cosmological slip',
                'No photon-baryon collision model, CMB/galaxy empirical fit, global action extension or full nonlinear closure',
                'Derived identities use the existing reduced quadratic action; not an independent revariation of every full covariant term'])


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--require-full-closure',action='store_true')
    args=p.parse_args()
    result=report()
    print(json.dumps(result,default=action.prior.serial,indent=2))
    raise SystemExit(1 if not all(result['checks'].values()) else 2 if args.require_full_closure else 0)
