"""Evolve the SAME fixed collar-control profile by one canonical time jet.

Exact symbolic KG/action identities plus a finite-resolution falsification
test. No source refit, hard-coded rank, or inference of full theory closure.
"""
import argparse
from functools import lru_cache
import json
from pathlib import Path
import time

import numpy as np
from scipy.integrate import solve_ivp
import sympy as s

from metric_collar_control import control, basis_values
from metric_initial_response import operators
from metric_static_background import curved_matter_jets, solve_background
from metric_wall_jets import derive_wall


@lru_cache(maxsize=1)
def recursion_identities():
    """Ingredients of a formal linear-amplitude recursion, not its convergence."""
    d, old, _ = operators()
    N,A,B,a0,Nd,Ad,Bd,Ndd,Add,Bdd,Lam,u,b,up,bp = d['symbols']
    PA,PB,pm,qz,mass,q = s.symbols('PA PB pm qz mass q')
    Hkin = N*(-PA*PB/(4*A)+B*PB**2/(8*A**2))
    kA = (s.diff(Hkin,PA)/A).subs(B,1)
    kB = s.diff(Hkin,PB).subs(B,1)
    matter_H = N*(pm**2/(A**2*B)+A**2*qz**2/B+A**2*B*mass**2*q**2)/2
    kinetic = pm**2/(A**4*B**2)
    pt = (kinetic-qz**2/B**2-mass**2*q**2)/2
    pz = (kinetic+qz**2/B**2-mass**2*q**2)/2
    pressure = [s.factor(-s.diff(matter_H,A)-2*N*A*B*pt),
                s.factor(-s.diff(matter_H,B)-N*A**2*pz)]
    aa,ap,app,bb,bpp,bppp,v,vp,vpp = s.symbols('aa ap app bb bpp bppp v vp vpp')
    qs = [N,A,B,Nd,Ad,Bd,Ndd,Add,Bdd]
    variations = [N*v,A*aa,B*bb,Nd*v+N*vp,Ad*aa+A*ap,Bd*bb+B*bpp,
        Ndd*v+2*Nd*vp+N*vpp,Add*aa+2*Ad*ap+A*app,Bdd*bb+2*Bd*bpp+B*bppp]
    gauge = {B:1,Bd:0,Bdd:0,Nd:N*u,Ad:A*b,Ndd:N*(up+u**2),Add:A*(bp+b**2)}
    eq = [d['EL'][0]/(A**2*B),(A*d['EL'][1]+B*d['EL'][2])/(N*A**2*B)]
    lin = [s.factor(sum(s.diff(e,qq)*dq for qq,dq in zip(qs,variations))
                    .subs(gauge,simultaneous=True)) for e in eq]
    general = s.Matrix([[s.factor(s.diff(e,qq)) for qq in
                        [aa,ap,app,bb,bpp,bppp,v,vp,vpp]] for e in lin])
    conformal = general[:,:3]+general[:,3:6]
    cross = (conformal.row_join(general[:,6:])-old).applyfunc(s.factor)
    # Curvature difference from common g and first derivatives, unequal gddot.
    w = s.symbols('w')
    g=s.diag(-N**2,A**2,A**2,B**2); inv=g.inv()
    gtt=s.diag(-2*N**2*v,2*w*A**2,2*w*A**2,2*w*B**2)
    def dtGamma(alpha,beta,gamma):
        return sum(inv[alpha,j]*((gtt[j,gamma] if beta==0 else 0)
             +(gtt[j,beta] if gamma==0 else 0)
             -(gtt[beta,gamma] if j==0 else 0))/2 for j in range(4))
    Ricci=s.Matrix(4,4,lambda i,j:dtGamma(0,i,j)
        -(sum(dtGamma(k,i,k) for k in range(4)) if j==0 else 0))
    scalar=s.factor(sum(inv[i,j]*Ricci[i,j] for i in range(4) for j in range(4)))
    tau=(A*PA+PB)/2
    z=s.symbols('z',real=True)
    nf,af,pf,qf=[s.Function(name)(z) for name in ['N','A','p','q']]
    qdot=nf*pf/af**2
    pdot=s.diff(nf*af**2*s.diff(qf,z),z)-nf*af**2*mass**2*qf
    Jdot=pdot*s.diff(qf,z)+pf*s.diff(qdot,z)
    energy=(pf**2/af**4+s.diff(qf,z)**2+mass**2*qf**2)/2
    transverse=(pf**2/af**4-s.diff(qf,z)**2-mass**2*qf**2)/2
    radial=(pf**2/af**4+s.diff(qf,z)**2-mass**2*qf**2)/2
    ward=s.factor(Jdot-s.diff(nf,z)*af**2*energy
                  +2*nf*af*s.diff(af,z)*transverse-s.diff(nf*af**2*radial,z))
    return dict(known_transverse_velocity=str(kA),known_radial_velocity=str(kB),
        radial_minus_transverse_velocity=str(s.factor(kB-kA)),
        trace_kinematic_residual=str(s.factor(2*kA+kB+N*tau/(2*A**2))),
        pressure_force_residuals=[str(e) for e in pressure],
        general_lapse_trace_coefficients=str(general),
        general_column_order='a,a_prime,a_second,b,b_prime,b_second,v,v_prime,v_second',
        conformal_operator_residuals=[str(e) for e in cross],
        Ricci_scalar_difference=str(scalar),Ricci_normal_difference=str(s.factor(Ricci[0,0]/N**2)),
        Ricci_scalar_residual=str(s.factor(scalar-6*w/N**2)),
        Ricci_normal_residual=str(s.factor(Ricci[0,0]/N**2+3*w/N**2)),
        canonical_KG_momentum_Ward_residual=str(ward),
        gravitational_spatial_Noether_residual=str(d['noether']),
        scope='All formulas linear in perturbation about static vacuum. Coefficient '
              'matrix includes lower spatial derivatives; no assertion of Taylor convergence.')


@lru_cache(maxsize=1)
def derive_next():
    z = s.symbols('z', real=True)
    nf, af, sigma = [s.Function(q)(z) for q in ['N', 'A', 'sigma']]
    raw = curved_matter_jets()['stress_time_coefficients']
    local = {'N': s.Function('N'), 'A': s.Function('A'),
             'sigma': s.Function('sigma'), 'z': z}
    jets = [[s.sympify(e, locals=local) for e in row] for row in raw]
    rho3 = s.simplify(s.factorial(3)*nf**2*jets[0][3])
    trace = [s.simplify(s.factorial(j)*(jets[2][j]+2*af**2*jets[3][j]))
             for j in [2, 3]]
    f2 = s.simplify(trace[0]/(nf**2*sigma))
    f3 = s.simplify(trace[1]/(nf**3*sigma))

    d, C, fifth, wall = derive_wall()
    N,A,B,a0,Nd,Ad,Bd,Ndd,Add,Bdd,Lam,u,b,up,bp = d['symbols']
    w,wp,wpp,v,vp,vpp = s.symbols('w wp wpp v vp vpp')
    c = s.symbols('c', real=True)
    vel, mass, rr, b5 = s.symbols('vel mass rr b5')
    spatial = {N: N*u, u: up, w: wp, wp: wpp, v: vp, vp: vpp}
    def dz(e):
        return sum(s.diff(e, q)*value for q, value in spatial.items())
    def wave(e):
        return N**2*(dz(dz(e))+(u+2*b)*dz(e)-mass**2*e)
    # Earlier metric jets vanish throughout the collar, not only at its ends.
    # q4 is obtained from the D''*phidot term of the KG equation.
    q4 = (v-3*w)*N*vel
    phi = {0: rr, 1: N*vel, 2: -N**2*mass**2*rr,
           3: wave(N*vel)}
    djets = {0: 0, 1: 0, 2: v-3*w, 3: 0, 4: -b5}
    # At the wall delta L^(4) phi0=0: phi0 is spatially constant and v4=0.
    deltaL3_phi1 = N**2*(2*(v-w)*(dz(dz(phi[1]))+(u+2*b)*dz(phi[1]))
                          +(vp+wp)*dz(phi[1])-2*v*mass**2*phi[1])
    q6 = wave(q4)+sum(s.binomial(4,j)*djets[j]*phi[5-j]
                    for j in range(5) if djets[j] != 0)
    q6 += s.binomial(4,3)*deltaL3_phi1
    raw_sixth = s.factor(q6.subs({w:0, v:0})/(N**3*vel))
    loc = {str(q):q for q in [*d['symbols'], w,wp,wpp,v,vp,vpp,c]}
    normal5 = s.sympify(wall['normal_fourth_from_Hamiltonian'], locals=loc)
    highest = C[:, [2,5]]
    accelerations = highest.inv()*(s.Matrix([0,2*c/N])-C[:,[1,4]]*s.Matrix([wp,vp]))
    substitutions = {wpp:accelerations[0], vpp:accelerations[1]}
    sixth = s.factor(raw_sixth.subs(b5,normal5).subs(substitutions, simultaneous=True))
    residual = s.factor(sixth-fifth-u*(wp+vp))
    omission = s.factor((raw_sixth.subs(b5,0)-raw_sixth.subs(b5,normal5))
                        .subs(substitutions, simultaneous=True))
    return dict(density_third=str(rho3), trace_second=str(trace[0]), trace_third=str(trace[1]),
        trace_second_coefficient=str(f2), trace_third_coefficient=str(f3),
        forcing_ratio=str(s.factor(f3/f2)), raw_sixth_jet=str(raw_sixth),
        on_shell_sixth_jet=str(sixth), sixth_identity_residual=str(residual),
        normal_metric_omission_residual=str(omission),
        scope='Leading epsilon^2 metric and epsilon^3 matter coefficients; sixth-wall '
              'identity assumes exact earlier cancellation on an open collar.')


@lru_cache(maxsize=4)
def evolve_control(y0, ratio, L):
    chi = (1-y0)*np.exp(-y0)
    if chi == 0 or y0 <= 0:
        raise ValueError('This regular positive-field scaling excludes chi=0 and y0<=0')
    previous = control(y0, ratio, L)  # Regenerate, do not trust stored verdicts.
    weights = np.asarray(previous['source_weights'])
    d, coeff, _ = operators()
    N,A,B,a0,Nd,Ad,Bd,Ndd,Add,Bdd,Lam,u,b,up,bp = d['symbols']
    symbolic = derive_next()
    f2 = -float(s.sympify(symbolic['trace_second_coefficient']))
    f3 = -float(s.sympify(symbolic['trace_third_coefficient']))
    seed = solve_background(y0, ratio, L)['seed']
    rhs = s.lambdify((u,b),d['rhs'].subs({a0:1,Lam:ratio}), 'numpy')
    def bgflow(x,Y):
        return L*np.array([Y[2],Y[3],*np.asarray(rhs(*Y[2:]),float).reshape(2)])
    bg = [solve_ivp(bgflow,(0,sign),seed,method='DOP853',rtol=2e-13,
                   atol=2e-15,max_step=1/96,dense_output=True) for sign in [-1,1]]
    if not all(sol.success for sol in bg):
        raise RuntimeError('Background integration failed')
    cf = s.lambdify((N,A,u,b,up,bp),coeff.subs({a0:1,Lam:ratio}),'numpy')
    wp,vp = s.symbols('wp vp'); cc = s.symbols('c',real=True)
    loc = {str(q):q for q in [*d['symbols'],wp,vp,cc]}
    jf = s.lambdify((N,A,u,b,up,bp,wp,vp,cc),
        s.sympify(symbolic['on_shell_sixth_jet'],locals=loc).subs({a0:1,Lam:ratio}),'numpy')
    def values(x):
        lnN,lnA,uu,bb = bg[0 if x<0 else 1].sol(x)
        upp,bpp = np.asarray(rhs(uu,bb),float).reshape(2)
        nn,aa = np.exp(lnN),np.exp(lnA)
        C = np.asarray(cf(nn,aa,uu,bb,upp,bpp),float)
        C *= np.array([L**2,L,1,L**2/chi,L/chi,1/chi]); C[1] *= chi
        return nn,aa,uu,bb,upp,bpp,C
    # Proportional forcing columns provide a linearity SANITY check, not an
    # independent operator/physics validation. The identity follows from KG.
    def integrate(method,rtol,atol,step):
        count = 2; columns = count+3
        initial = np.zeros((5,columns)); initial[1,count]=1; initial[3,count+1]=1
        global_c = np.zeros(columns); global_c[-1]=1
        probes = {}
        def flow(x,flat):
            Y = flat.reshape(5,columns)
            n,a,_,_,_,_,C = values(x)
            basis = basis_values(x); profile = basis@weights
            target = np.zeros((2,columns))
            target[1,:count] = chi*n**3*profile*np.array([f3,f2])
            if abs(profile)>1e-4:
                index = int(np.argmax(basis))
                if index not in probes:
                    probes[index] = [float(x),float(n),float(target[1,0]/chi)]
            target[1] += 2*global_c/n
            second = np.linalg.solve(C[:,[2,5]],target-C[:,[0,1,3,4]]@Y[[0,1,2,3]])
            return np.vstack([Y[1],second[0],Y[3],second[1],a*a*Y[0]]).reshape(-1)
        sol = solve_ivp(flow,(-1,1),initial.reshape(-1),method=method,rtol=rtol,
                        atol=atol,max_step=step,dense_output=True)
        if not sol.success:
            raise RuntimeError('Next-jet response integration failed: '+sol.message)
        end = sol.y[:,-1].reshape(5,columns)
        matrix = end[[0,2,4],count:]
        match = np.linalg.solve(matrix,-end[[0,2,4],:count])
        def dense(x):
            Y = sol.sol(x).reshape((5,columns)+np.shape(x))
            return Y[:,:count]+np.einsum('ij...,jk->ik...',Y[:,count:],match)
        return dense,match,matrix,[probes[i] for i in sorted(probes)]
    coarse = integrate('RK45',2e-10,2e-13,1/144)
    fine,match,matrix,probes = integrate('DOP853',2e-13,3e-15,1/192)
    grid = np.linspace(-1,1,2001); Y = fine(grid)[:,0]; Yc = coarse[0](grid)[:,0]
    c3 = match[2,0]/chi; c3c = coarse[1][2,0]/chi
    def endpoint_control(dense,cc):
        ends = dense(np.array([-1.,1.]))[:,0]
        return np.array([cc,L*ends[1,0],L*ends[3,0]/chi,
                         L*ends[1,1],L*ends[3,1]/chi])
    M3 = endpoint_control(fine,c3); M3c = endpoint_control(coarse[0],c3c)
    scales = np.asarray(previous['control_row_scales'])
    signal = np.linalg.norm(M3/scales)
    control_error = np.linalg.norm((M3-M3c)/scales)
    peak = np.max(abs(Y),axis=1)
    collar = abs(grid)>=.8
    wall = []; wall_coarse = []
    for x in [-1.,1.]:
        n,a,uu,bb,upp,bpp,_ = values(x)
        state = fine(x)[:,0]; state_c = coarse[0](x)[:,0]
        wall.append(float(jf(n,a,uu,bb,upp,bpp,L*state[1],L*state[3]/chi,c3)))
        wall_coarse.append(float(jf(n,a,uu,bb,upp,bpp,L*state_c[1],L*state_c[3]/chi,c3c)))
    ode = []; dx=1e-5
    for x in np.linspace(-.99,.99,161):
        state = fine(x)[:,0]; n,a,_,_,_,_,C=values(x)
        target=np.array([0.,chi*f3*n**3*(basis_values(x)@weights)+2*match[2,0]/n])
        sec=np.linalg.solve(C[:,[2,5]],target-C[:,[0,1,3,4]]@state[[0,1,2,3]])
        predicted=np.array([state[1],sec[0],state[3],sec[1],a*a*state[0]])
        derivative=(fine(x+dx)[:,0]-fine(x-dx)[:,0])/(2*dx)
        ode.append(float(np.max(abs(predicted-derivative)/(1+abs(predicted)))))
    ratio_source = f3/f2
    equiv = np.max(abs(fine(grid)[:,0]-ratio_source*fine(grid)[:,1]))/max(np.max(abs(Y)),1e-300)
    refine = np.max(abs(Y-Yc))/max(np.max(abs(Y)),1e-300)
    boundary = float(np.max(abs(Y[[0,2,4]][:,[0,-1]])))
    next_resolution = signal/max(control_error,1e-12)
    # This is a survival requirement, separate from whether the audit worked.
    failure = next_resolution>100 and signal>1e-5
    return dict(y0=y0,Lambda_over_a0_squared=ratio,L=L,input_weights=previous['source_weights'],
        forcing_probes=probes, second_control_relative=previous['reintegrated_control_scaled_residual'],
        earlier_collar_relative=previous['relative_collar_tail'],
        third_control=M3.tolist(),third_control_scaled_norm=float(signal),
        third_control_scaled_refinement=float(control_error),next_control_resolution=float(next_resolution),
        normalized_sixth_wall_jets=wall,sixth_wall_absolute_refinement=float(max(abs(np.array(wall)-wall_coarse))),
        sixth_wall_scope='Conditional sixth-jet value if earlier numerical collar cancellation '
            'has an exact lift; no bound here on all omitted higher spatial derivatives.',
        third_collar_relative=float(max(np.max(abs(Y[i,collar]))/max(peak[i],1e-300) for i in [0,2])),
        refinement_relative=float(refine),ODE_residual=max(ode),boundary_residual=boundary,
        source_multiplication_identity_relative=float(equiv),
        computed_matching_rank=int(np.linalg.matrix_rank(matrix)),matching_matrix=matrix.tolist(),
        audit_checks_pass=bool(previous['success'] and refine<1e-5 and max(ode)<1e-5
            and boundary<1e-9 and equiv<1e-8),
        fixed_profile_next_collar_gate='FAIL' if failure else 'UNRESOLVED')


def audit():
    start=time.monotonic(); symbolic=derive_next()
    recurrence=recursion_identities()
    cases=[evolve_control(.5,0.,.02),evolve_control(10.5,float(32*s.pi),.002)]
    exact = [recurrence['trace_kinematic_residual'],recurrence['Ricci_scalar_residual'],
             recurrence['Ricci_normal_residual'],*recurrence['pressure_force_residuals'],
             recurrence['canonical_KG_momentum_Ward_residual'],
             recurrence['gravitational_spatial_Noether_residual'],
             *recurrence['conformal_operator_residuals']]
    return dict(symbolic=symbolic,recursion=recurrence,cases=cases,runtime_seconds=time.monotonic()-start,
        audit_checks_pass=bool(symbolic['sixth_identity_residual']=='0' and symbolic['density_third']=='0'
                              and all(e=='0' for e in exact)
                              and all(r['audit_checks_pass'] for r in cases)),
        verdict='Fixed prior profiles do not have an established invariant wall-control subspace. '
            'A failed next-jet collar gate is not a no-go for every source or for the full theory.')


def exit_status(result, require_preserved):
    if not result['audit_checks_pass']:
        return 1
    if require_preserved and any(r['fixed_profile_next_collar_gate']!='PASS' for r in result['cases']):
        return 2
    return 0


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--output',type=Path); p.add_argument('--require-preserved-collar',action='store_true')
    args=p.parse_args(); result=audit()
    if args.output:
        args.output.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    print('Exact KG trace third derivative:',result['symbolic']['trace_third'])
    for row in result['cases']:
        print('y0',row['y0'],'fixed-profile gate',row['fixed_profile_next_collar_gate'],
              'control/error',row['next_control_resolution'],'sixth wall',row['normalized_sixth_wall_jets'])
    print('Audit checks:',result['audit_checks_pass'])
    return exit_status(result,args.require_preserved_collar)


if __name__=='__main__':
    raise SystemExit(main())
