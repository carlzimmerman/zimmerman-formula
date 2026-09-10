#!/usr/bin/env python3
"""Exact trace-variance action and frozen-principal audit; NOT theory closure.

S = S_CAM_min + m*d/3 int dt N sqrt(h) (K - <K>_N)^2.
<K>_N = int N sqrt(h) K / int N sqrt(h), on compact positive-lapse leaves.
The quadratic nonzero-mode kinetic block is derived with spatial gauge E
retained. Generic backgrounds are frozen static principal jets, NOT asserted
globally solved spacetimes. All exceptional chains are rebuilt separately.
"""
import argparse
from functools import lru_cache
import importlib.util
import json
from pathlib import Path
import sympy as s


ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location(
    'existing_metric_constraint', ROOT / 'g03_global_kernel_bridge_2026/metric_constraint.py')
existing = importlib.util.module_from_spec(spec)
spec.loader.exec_module(existing)


def acceleration():
    m, a0, y = s.symbols('m a0 y', positive=True)
    g = s.Matrix(s.symbols('gx gy gz', real=True))
    norm = s.sqrt(g.dot(g))
    F = 2*m*a0**2*(1-(1+norm/a0)*s.exp(-norm/a0))
    tensor = (s.hessian(F, list(g))/(2*m)).subs(
        {g[0]: 0, g[1]: 0, g[2]: a0*y}).applyfunc(s.simplify)
    c = s.symbols('cos_theta', real=True)
    alpha = s.simplify(tensor[0, 0]*(1-c**2)+tensor[2, 2]*c**2)
    return dict(tensor=tensor, alpha=alpha, y=y, cos_theta=c,
                parallel_at_y2=tensor[2, 2].subs(y, 2),
                frozen_at_y2=s.exp(-2),
                missing_radial_term=s.simplify(tensor[2, 2]-tensor[0, 0]))


def variance():
    m = s.symbols('m', positive=True)
    d, P, h = s.symbols('d P homogeneous_K', real=True)
    v = s.symbols('volume0:3', positive=True)
    N = s.symbols('lapse0:3', positive=True)
    u = s.symbols('log_volume_dot0:3', real=True)
    W = sum(v[i]*N[i] for i in range(3))
    U = sum(v[i]*u[i] for i in range(3))
    mean = U/W
    variance_density = sum(v[i]*N[i]*(u[i]/N[i]-mean)**2 for i in range(3))
    trace = -m*sum(v[i]*u[i]**2/N[i] for i in range(3))/3 + m*d*variance_density/3
    degenerate = s.factor(trace.subs(d, 1))
    expected = -m*U**2/(3*W)
    momenta = [s.factor(s.diff(degenerate, ui)) for ui in u]
    Hess = s.hessian(degenerate, u)
    # Canonical trace p_i = P*volume_i; GR trace H on this constraint surface.
    Hgr = sum(-3*N[i]*(P*v[i])**2/(4*m*v[i]) for i in range(3))
    Uon = -3*P*W/(2*m)
    identity = s.factor((P*U + m*U**2/(3*W)-Hgr).subs(u[2],
        (Uon-v[0]*u[0]-v[1]*u[1])/v[2]))
    homogeneous = {u[i]: N[i]*h for i in range(3)}
    # N-dependence of the mean is varied, not discarded.
    lapse_residuals = [s.factor(s.diff(degenerate, Ni)-m*U**2*s.diff(W, Ni)/(3*W**2))
                      for Ni in N]
    return dict(trace_L=degenerate, identity_to_global_trace=s.factor(degenerate-expected),
                momenta=momenta, mean_trace_relations=[s.factor(momenta[i]/v[i]-momenta[0]/v[0])
                                                     for i in (1, 2)],
                trace_velocity_hessian=Hess, trace_velocity_hessian_rank=Hess.rank(),
                legendre_identity_residual=identity, lapse_variation_residuals=lapse_residuals,
                homogeneous_variance=s.factor(variance_density.subs(homogeneous)),
                homogeneous_trace_L=s.factor(trace.subs(homogeneous)))


def scalar():
    m, k = s.symbols('m k', positive=True)
    d, alpha = s.symbols('d alpha', real=True)
    z, E, n, B, zd, Ed, pz, pE, pn, pB = s.symbols('z E n B zd Ed pz pE pn pB', real=True)
    qs, ps = [z, E, n, B], [pz, pE, pn, pB]
    K = s.diag(zd+k**2*(B-Ed), zd, zd)
    kinetic = s.expand(m*(s.trace(K*K)-s.trace(K)**2)/2 + m*d*s.trace(K)**2/3)
    potential = m*k**2*(z**2+2*n*z+alpha*n**2)
    L = kinetic+potential
    vs = s.solve([s.diff(L, zd)-pz, s.diff(L, Ed)-pE], [zd, Ed])
    H = s.factor((pz*zd+pE*Ed-L).subs(vs))
    generic = existing.linear_dirac(H, qs, ps, [pn, pB])
    original = existing.linear_dirac(H.subs(d, 0), qs, ps, [pn, pB])
    zero_alpha = existing.linear_dirac(H.subs(alpha, 0), qs, ps, [pn, pB])
    # d=1 changes the velocity Hessian; re-Legendre-transform the action.
    L1 = L.subs(d, 1)
    ev = s.solve(s.diff(L1, Ed)-pE, Ed)[0]
    H1 = s.factor((pE*Ed-L1).subs(Ed, ev))
    degenerate = existing.linear_dirac(H1, qs, ps, [pn, pB, pz])
    zero = existing.linear_dirac(H1.subs(alpha, 1), qs, ps, [pn, pB, pz])
    # Reduce auxiliaries AFTER retaining the spatial gauge in the canonical audit.
    Lg = L.subs(Ed, 0)
    aux = s.solve([s.diff(Lg, B), s.diff(Lg, n)], [B, n])
    reduced = s.factor(Lg.subs(aux))
    A = s.factor(s.diff(reduced, zd, 2)/2)
    cs2 = s.factor(-s.diff(reduced, z, 2)/(2*A*k**2))
    # Orthogonal frequency-domain EL determinant, not the reduced sound formula.
    om = s.symbols('omega', real=True)
    fields = [z, n, B]
    rows = [s.diff(Lg, z)+s.I*om*s.diff(Lg, zd), s.diff(Lg, n), s.diff(Lg, B)]
    operator = s.Matrix([r.subs(zd, -s.I*om*z) for r in rows]).jacobian(fields)
    dispersion_residual = s.factor(operator.det().subs(om**2, cs2*k**2))
    witnesses = []
    for dv in (s.Rational(-3, 2), s.Integer(2)):
        witnesses.append(dict(d=dv, kinetic=A.subs({d:dv, m:1}),
                              radial_speed_squared=cs2.subs({d:dv, alpha:-s.exp(-2)}),
                              frozen_speed_squared=cs2.subs({d:dv, alpha:s.exp(-2)})))
    return dict(L=L, H=H, H_trace_degenerate=H1,
                velocity_Hessian=s.hessian(L, [zd, Ed]),
                reduced_L=reduced, kinetic=A, speed_squared=cs2,
                frequency_operator=operator, dispersion_residual=dispersion_residual,
                trace_degenerate_z_velocity=s.diff(L1, zd),
                ghost_band=s.reduce_inequalities(A/m < 0, d),
                positive_kinetic_band=s.reduce_inequalities(A/m > 0, d),
                witnesses=witnesses), dict(generic=generic, original=original,
                    zero_lapse_symbol=zero_alpha,
                    trace_degenerate=degenerate, zero_field_trace_degenerate=zero)


def vacuum_seed():
    """Vary N,A,B before B=1; dimensionless m=a0=1, positive N'/NB.

    Spatial EH boundary term is removed with Dirichlet boundary completion.
    This is the existing plane-vacuum construction independently varied here.
    Its local solution is not a compact boundaryless static cosmology.
    """
    x=s.symbols('x', real=True)
    N,A,B=[s.Function(name)(x) for name in ('N','A','B')]
    Lam=s.symbols('Lambda', real=True)
    Y=s.diff(N,x)/(N*B)
    f=2*(1-(1+Y)*s.exp(-Y))
    L=(N*s.diff(A,x)**2+2*A*s.diff(A,x)*s.diff(N,x))/B-Lam*N*B*A**2+N*B*A**2*f
    EL=[s.diff(L,q)-s.diff(s.diff(L,s.diff(q,x)),x) for q in (N,A,B)]
    u=s.symbols('u', positive=True)
    b=s.symbols('b', real=True)
    du,db=s.symbols('du db', real=True)
    replace={s.diff(N,x,2):N*(du+u*u),s.diff(A,x,2):A*(db+b*b),
             s.diff(N,x):N*u,s.diff(A,x):A*b,s.diff(B,x):0,B:1}
    equations=[s.simplify(e.subs(replace, simultaneous=True)/factor)
               for e,factor in zip(EL,(-A**2,-2*N*A,-N*A**2))]
    ef=s.exp(-u); F=2*(1-(1+u)*ef); chi=(1-u)*ef
    expected=[2*db+2*chi*du+3*b*b+Lam-F+2*u*u*ef+4*b*u*ef,
              db+du+b*b+b*u+u*u+Lam-F,
              b*b+2*b*u+Lam-F+2*u*u*ef]
    C=equations[2]
    identity=s.simplify(s.diff(C,u)*du+s.diff(C,b)*db+(u+2*b)*C-u*equations[0]-2*b*equations[1])
    matrix=s.Matrix(equations[:2]).jacobian([db,du])
    discriminant=u*u-Lam+F-2*u*u*ef
    seed={u:20,Lam:32*s.pi}
    bseed=-20+s.sqrt(discriminant.subs(seed))
    return dict(EL_equations=equations, variation_residuals=[s.simplify(a-bb) for a,bb in zip(equations,expected)],
                radial_constraint_identity=identity, ODE_matrix=matrix,
                seed_y=20, seed_Lambda_over_a0_squared=32*s.pi,
                seed_discriminant=discriminant.subs(seed), seed_b=bseed,
                seed_constraint_residual=s.simplify(C.subs(seed).subs(b,bseed)),
                seed_alpha_radial=chi.subs(u,20),
                seed_ode_determinant=s.simplify(matrix.det().subs(seed)))


def global_and_vector():
    m,k=s.symbols('m k',positive=True)
    V,B,Vd,pV,pB=s.symbols('V B Vd pV pB',real=True)
    K=s.Matrix([[0,0,k*(Vd-B)/2],[0,0,0],[k*(Vd-B)/2,0,0]])
    L=m*(s.trace(K*K)-s.trace(K)**2)/2
    vv=s.solve(s.diff(L,Vd)-pV,Vd)[0]
    H=s.factor((pV*Vd-L).subs(Vd,vv))
    vec=existing.linear_dirac(H,[V,B],[pV,pB],[pB])
    A,N,Lam=s.symbols('scale N Lambda',positive=True)
    pA,pN,T,pT=s.symbols('p_scale p_N T p_T',real=True)
    adot=s.symbols('adot',real=True)
    L0=-3*m*A*adot**2/N-m*Lam*N*A**3
    vel=s.solve(s.diff(L0,adot)-pA,adot)[0]
    H0=s.factor((pA*adot-L0).subs(adot,vel))+N*pT
    qs,ps=[A,N,T],[pA,pN,pT]
    def pb(f,g):
        return s.simplify(sum(s.diff(f,q)*s.diff(g,p)-s.diff(f,p)*s.diff(g,q) for q,p in zip(qs,ps)))
    C=pb(pN,H0)
    constraints=[pN,C]
    bracket=s.Matrix([[pb(f,g) for g in constraints] for f in constraints])
    rank=bracket.rank(); fc=len(constraints)-rank
    return dict(vector_L=L,vector_H=H,one_vector_polarization=vec,
                zero_mode_H=H0,zero_mode_primaries=[pN],zero_mode_secondaries=[C],
                zero_mode_poisson_matrix=bracket,zero_mode_rank=rank,zero_mode_first_class=fc,
                zero_mode_pairs_including_matter_clock=len(qs)-fc-s.Rational(rank,2),
                zero_mode_preservation_residual=pb(C,H0),
                expanding_p_scale_squared=s.solve(C,pA**2)[0])


@lru_cache(maxsize=1)
def derive():
    a, v = acceleration(), variance()
    sc, dc = scalar()
    vacuum=vacuum_seed()
    global_vector=global_and_vector()
    m, a0, y = s.symbols('m a0 y', positive=True)
    p, q = s.symbols('Phi_gradient Psi_gradient', positive=True)
    Lstatic = m*(q*q-2*p*q)+2*m*a0*a0*(1-(1+p/a0)*s.exp(-p/a0))
    spatial = s.factor(s.diff(Lstatic, q)/(2*m))
    flux = s.factor((-s.diff(Lstatic, p)/(2*m)).subs(q,p))
    phantom=s.simplify(p-flux)
    phantom_slope=s.simplify(s.diff(phantom,p).subs(p,a0*y))
    scale, adot, N, Lam, M = s.symbols('scale adot N Lambda M_dust', positive=True)
    L0 = -3*m*scale*adot**2/N - m*Lam*N*scale**3-N*M
    friedmann = s.factor(s.solve(s.diff(L0,N),adot**2)[0]/(N**2*scale**2))
    hp, hc, vp, vc, k, om = s.symbols('hp hc vp vc k omega', real=True)
    hh=s.Matrix([[hp,hc,0],[hc,-hp,0],[0,0,0]])
    hd=hh.subs({hp:vp,hc:vc})
    Ltt=m*(s.trace(hd*hd)-k*k*s.trace(hh*hh))/8
    Ktt=s.hessian(Ltt,[vp,vc]); Vtt=-s.hessian(Ltt,[hp,hc])
    tensor_poles=s.solve(s.det(om**2*Ktt-Vtt),om**2)
    checks = {
        'static_Psi_equation_independent': spatial == q-p,
        'physical_flux_from_variation': s.simplify(flux-p*(1-s.exp(-p/a0)))==0,
        'phantom_boost_slope_is_radial_lapse_hessian': s.simplify(phantom_slope-a['tensor'][2,2])==0,
        'radial_hessian_is_not_frozen_coupling': s.simplify(a['missing_radial_term']+y*s.exp(-y))==0,
        'gradient_witness_not_a_frozen_coupling_pass': all(
            float(w['kinetic'])>0 and float(w['radial_speed_squared'])<0
            and float(w['frozen_speed_squared'])>0 for w in sc['witnesses']),
        'frequency_determinant_checks_reduced_pole': sc['dispersion_residual']==0,
        'mean_varied_including_denominator': all(x==0 for x in v['lapse_variation_residuals']),
        'variance_equivalent_trace_constraint': v['identity_to_global_trace']==0 and
            v['legendre_identity_residual']==0 and all(x==0 for x in v['mean_trace_relations']),
        'homogeneous_variance_vanishes': v['homogeneous_variance']==0,
        'FLRW_from_lapse_before_gauge_fix': s.simplify(friedmann-Lam/3-M/(3*m*scale**3))==0,
        'degenerate_primary_from_action': sc['trace_degenerate_z_velocity']==0,
        'all_computed_constraint_chains_close': all(c['preservation_closed'] for c in dc.values()),
        'TT_trace_variance_vanishes': s.trace(hh)==0 and s.trace(hd)==0,
        'TT_luminal_positive': all(s.simplify(r-k**2)==0 for r in tensor_poles)
            and all(e.is_positive for e in Ktt.eigenvals()),
        'actual_plane_vacuum_variation': all(x==0 for x in vacuum['variation_residuals']),
        'radial_constraint_propagates': vacuum['radial_constraint_identity']==0,
        'framework_vacuum_seed_regular_and_radially_negative':
            vacuum['seed_constraint_residual']==0 and float(vacuum['seed_discriminant'])>0
            and float(vacuum['seed_ode_determinant'])!=0 and float(vacuum['seed_alpha_radial'])<0,
        'homogeneous_nonlinear_preservation': global_vector['zero_mode_preservation_residual']==0,
        'vector_primary_preservation': global_vector['one_vector_polarization']['preservation_closed'],
    }
    return dict(checks=checks, acceleration=a, variance=v, scalar=sc, dirac=dc,
                static=dict(Psi_flux=spatial, Phi_flux=flux, G_measured=1/(8*s.pi*m),
                            phantom_acceleration=phantom, phantom_slope=phantom_slope,
                            phantom_stationary_points=s.solve(s.diff(phantom,p),p),
                            phantom_maximum=phantom.subs(p,a0)),
                FLRW=dict(L=L0, H_squared=friedmann),
                tensor=dict(L=Ltt, kinetic=Ktt, frequency_squared=tensor_poles),
                vacuum_seed=vacuum,
                global_and_vector=global_vector,
                status='OPEN full theory; regular scalar trace repair fails the radial principal-health gate',
                scope='Exact symbolic action blocks and finite Dirac systems; no nonlinear global closure or empirical proof.')


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--require-closure',action='store_true')
    args=parser.parse_args()
    r=derive()
    print(json.dumps(r,default=str,indent=2))
    if not all(r['checks'].values()):
        return 1
    # No mechanism in this audit supplies global hyperbolicity, PPN, or closure.
    return 2 if args.require_closure else 0


if __name__=='__main__':
    raise SystemExit(main())
