"""Necessary causal-screen gates, not a relativistic MOND construction.

Exact finite quadratic actions audit: retarded variation, one-pole response,
healthy/ghost localization, and preservation of a source-derived negative
static-energy direction under unconstrained healthy oscillator additions.
No new constraints, gyroscopic terms or changes to the original static block
are included in the last statement. Those are explicit possible loopholes.
"""
import argparse
import json
from pathlib import Path
import platform
import time

import sympy as s
from selective_screen import derive as derive_screen


def derive():
    start = time.monotonic()
    # A lower-triangular, nonsymmetric discrete retarded kernel.
    f = s.Matrix(s.symbols('f0:3'))
    retarded = s.Matrix([[1,0,0],[2,1,0],[3,2,1]])
    action = (f.T*retarded*f)[0]/2
    gradient = s.Matrix([s.diff(action,v) for v in f])
    hessian = s.hessian(action,list(f))
    checks = {'retarded_action_varies_to_symmetric_kernel':
              hessian == (retarded+retarded.T)/2}

    # Local two-oscillator action; omega2 and Omega2 can depend on spatial k.
    u,r,du,dr,pu,pr = s.symbols('u r du dr p_u p_r',real=True)
    z,omega2,Omega2,g,sigma = s.symbols('z omega2 Omega2 g sigma',real=True)
    L = (du**2-omega2*u**2+sigma*(dr**2-Omega2*r**2))/2+g*u*r
    Hvel = s.hessian(L,[du,dr])
    velocities = s.solve([s.diff(L,du)-pu,s.diff(L,dr)-pr],[du,dr])
    Hamiltonian = s.factor((pu*du+pr*dr-L).subs(velocities))
    stiffness = -s.hessian(L.subs({du:0,dr:0}),[u,r])
    M = z*Hvel-stiffness
    effective = s.factor(M[0,0]-M[0,1]*M[1,0]/M[1,1])
    checks['localized_Euler_Lagrange_matches_elimination'] = s.cancel(
        effective-(z-omega2+g**2/(sigma*(Omega2-z)))) == 0
    cases = {}
    for name,sign in [('healthy',1),('ghost',-1)]:
        values = {omega2:4,Omega2:9,g:1,sigma:sign}
        mat = M.subs(values)
        determinant = s.Poly(mat.det(),z)
        numerator = s.Poly(mat[1,1],z)  # observable u-u propagator numerator
        common = s.gcd(determinant,numerator)
        poles = s.solve(determinant.as_expr(),z)
        checks[name+'_exact_pole_residuals'] = all(s.simplify(determinant.eval(p))==0 for p in poles)
        eigen = Hvel.subs(values).eigenvals()
        cases[name] = {'frequency_matrix':[[str(v) for v in row] for row in mat.tolist()],
            'determinant':str(determinant.as_expr()), 'omega_squared':[float(p) for p in poles],
            'static_response_correction':float((effective-(z-omega2)).subs(values).subs(z,0)),
            'velocity_Hessian_rank':Hvel.subs(values).rank(),
            'negative_kinetic_count':sum(m for v,m in eigen.items() if v<0),
            'common_polynomial_factor_degree':common.degree(),
            'propagator_pole_count':determinant.degree()-common.degree(),
            'Legendre_velocities':{str(v):str(e.subs(values)) for v,e in velocities.items()}}

    # General completed-square identity: no numerical spectrum assumption.
    a,b,d = s.symbols('h11 h12 h22',real=True)
    Haux = s.Matrix([[a,b],[b,d]])
    C = s.Matrix(2,2,s.symbols('c0:4'))
    xx,rr = s.Matrix(s.symbols('x0:2')),s.Matrix(s.symbols('r0:2'))
    y11,y12,y22 = s.symbols('v11 v12 v22',real=True)
    V = s.Matrix([[y11,y12],[y12,y22]])
    Veff = V-C*Haux.inv()*C.T
    potential = (xx.T*V*xx+rr.T*Haux*rr-2*xx.T*C*rr)[0]/2
    shifted = rr-Haux.inv()*C.T*xx
    completed = (xx.T*Veff*xx+shifted.T*Haux*shifted)[0]/2
    checks['general_completed_square_identity'] = s.cancel(potential-completed)==0

    # Fresh source-built gravity witness, not a hand-entered unstable matrix.
    base = derive_screen()
    checks['source_gravity_checks_pass'] = all(base['checks'].values())
    names = 'A c14 c2 K xi2 k omega beta j'
    symbols = {str(v):v for v in s.symbols(names,real=True)}
    R = s.Matrix([[s.sympify(v,locals=symbols) for v in row] for row in base['reduced_kernel']])
    qstar = s.sympify(base['q_threshold'],locals=symbols)
    vals = dict(zip([symbols[v] for v in ['A','c14','c2','K','xi2','beta']],
                    [s.Rational(9,5),s.Rational(1,100000),s.Rational(1,100),10,1,s.Rational(1,4)]))
    W = (-R.subs(symbols['omega'],0).subs(symbols['j'],symbols['A']/(2-symbols['c14'])-1)
         .subs(vals).subs(symbols['k']**2,2*qstar.subs(vals)))
    coupling = s.eye(2)/100
    aux_witness = s.Matrix([[2,1],[1,3]])
    correction = coupling*aux_witness.inv()*coupling.T
    after = W-correction
    checks['witness_auxiliary_positive_definite'] = aux_witness[0,0]>0 and aux_witness.det()>0
    checks['witness_static_softening_positive_definite'] = correction[0,0]>0 and correction.det()>0
    # Genuine elliptic escape: wrong-sign nondynamical auxiliary is NOT a ghost.
    # It stiffens a physical scalar without adding a canonical pair, but its
    # reduced spatially nonlocal equation fails finite-domain propagation.
    q,m,m0,distance = s.symbols('q m m0 distance',positive=True)
    Le = (du**2-(q+m0**2)*u**2+(q+m**2)*r**2)/2+g*u*r
    rsolve = s.solve(s.diff(Le,r),r)[0]
    Lreduced = s.factor(Le.subs(r,rsolve))
    dispersion = s.factor(-s.diff(Lreduced,u,2))
    He = pu**2/2+(q+m0**2)*u**2/2-(q+m**2)*r**2/2-g*u*r
    def pb(f,h):
        return s.expand(s.diff(f,u)*s.diff(h,pu)-s.diff(f,pu)*s.diff(h,u)
                        +s.diff(f,r)*s.diff(h,pr)-s.diff(f,pr)*s.diff(h,r))
    constraints = [pr,pb(pr,He)]
    bracket = s.Matrix([[pb(a,b) for b in constraints] for a in constraints])
    multiplier = -g*pu/(q+m**2)
    closed = all(s.cancel((pb(c,He)+pb(c,pr)*multiplier).subs(r,rsolve))==0
                 for c in constraints)
    Green = s.exp(-m*distance)/(4*s.pi*distance)
    checks['elliptic_reduced_dispersion'] = s.cancel(dispersion-(q+m0**2+g**2/(q+m**2)))==0
    checks['elliptic_constraint_preservation'] = closed
    checks['elliptic_reduced_energy_positive'] = dispersion.is_positive
    checks['Yukawa_Green_off_origin'] = s.simplify(-s.diff(Green,distance,2)
        -2*s.diff(Green,distance)/distance+m**2*Green)==0
    checks['Yukawa_Green_delta_normalization'] = s.limit(-4*s.pi*distance**2*s.diff(Green,distance),distance,0)==1
    elliptic = {'action':str(Le),'reduced_action':str(Lreduced),'omega_squared':str(dispersion),
                'constraints':list(map(str,constraints)),
                'poisson_matrix':[[str(v) for v in row] for row in bracket.tolist()],
                'constraint_preservation_closed':closed,'bracket_rank':bracket.rank(),
                'physical_mode_count':int(2-(len(constraints)-bracket.rank())-s.Rational(bracket.rank(),2)),
                'off_source_initial_acceleration':float((-g**2*Green).subs({g:1,m:1,distance:1})),
                'exact_off_source_initial_acceleration':str(-g**2*Green),
                'scope':'u is physical, not a gauge potential; u(0,x)=delta^3(x), udot=0. Equally, smooth nonnegative compact initial data give a nonzero exterior Yukawa convolution.'}
    return {'checks':{k:bool(v) for k,v in checks.items()},'python':platform.python_version(),
            'sympy':s.__version__, 'retarded_Hessian':[[str(v) for v in row] for row in hessian.tolist()],
            'retarded_gradient_equals_retarded_equation':gradient==retarded*f,
            'local_action':str(L),'local_Hamiltonian':str(Hamiltonian),
            'effective_observable_kernel':str(effective), **cases,
            'negative_direction_before':float(W[0,0]),'negative_direction_after':float(after[0,0]),
            'exact_negative_direction_before':str(W[0,0]),'exact_negative_direction_after':str(after[0,0]),
            'elliptic':elliptic,
            'source_gravity_provenance':base['source'],
            'scope':'Finite real quadratic sectors, exact rational witnesses; source-derived k!=0 scalar negative direction.',
            'nonclaims':['full covariant construction','nonlinear DOF count','MOND empirical prediction',
                         'universal no-go for causal nonlocal gravity','novelty',
                         'extensions with contact counterterms or new constraints ruled out'],
            'runtime_seconds':round(time.monotonic()-start,3)}


if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--output',type=Path)
    p.add_argument('--require-causal-hidden-free',action='store_true')
    args = p.parse_args()
    result = derive()
    if args.output:
        args.output.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    for i,(name,ok) in enumerate(result['checks'].items(),1):
        print('[{}] {} {}'.format('ok' if ok else 'FAIL',i,name))
    print('Healthy/ghost pole counts:',result['healthy']['propagator_pole_count'],result['ghost']['propagator_pole_count'])
    print('Healthy/ghost static corrections:',result['healthy']['static_response_correction'],result['ghost']['static_response_correction'])
    print('Negative gravity direction:',result['negative_direction_before'],'->',result['negative_direction_after'])
    admissible = any(v['static_response_correction']<0 and v['negative_kinetic_count']==0
                     and v['propagator_pole_count']<=1 for v in [result['healthy'],result['ghost']])
    admissible = admissible or (result['elliptic']['physical_mode_count']<=1
        and result['checks']['elliptic_reduced_energy_positive']
        and result['elliptic']['off_source_initial_acceleration']==0)
    print('Elliptic physical-mode count:',result['elliptic']['physical_mode_count'])
    print('Elliptic off-source acceleration:',result['elliptic']['exact_off_source_initial_acceleration'])
    print('Minimal causal hidden-free completion exists:',admissible)
    raise SystemExit(1 if not all(result['checks'].values()) else
                     2 if args.require_causal_hidden_free and not admissible else 0)
