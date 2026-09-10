#!/usr/bin/env python3
"""Coupled EH/cuscuton/field-dust quadratic action; not a full MOND certificate.

Exact spatially isotropic scalar Fourier sector, expanding FLRW, unitary clock.
SymPy constructs the ADM density before expansion; no entered ranks or PPN values.
No external numerical data or network required. Prints all scientific results.
"""
import json
import math
import sympy as s


def run():
    checks = {}

    def check(name, condition):
        checks[name] = bool(condition)
        if not checks[name]:
            raise AssertionError(name)

    a, H, M, W, Q, A, B, C, k2 = s.symbols('a H M2 mu2 Q KQ KQQ C kphys2', positive=True)
    K0, V, Lam, K3, CQ, CT, WD = s.symbols('K0 V Lambda KQQQ CQ Ctau mu2_tau', real=True)
    z, zd, zx, zxx, sig, sd, sx, al, be, bx, bxx, t = s.symbols(
        'z zd zx zxx sigma sigmad sx alpha beta bx bxx amplitude', real=True)
    hd = -(W + Q*A)/(2*M)
    qd = -3*H*A/B
    ad = -3*H*A
    rates = {a: H*a, H: hd, Q: qd, A: ad, B: K3*qd, C: CQ*qd+CT, W:WD, k2: -2*H*k2}

    def dt(expr):
        return sum(s.diff(expr, var)*rate for var, rate in rates.items())

    def eq(left, right):
        return s.factor(left-right) == 0

    # h_ij=a^2 exp(2 amplitude*z) delta_ij; N=1+amplitude*alpha;
    # N^x=amplitude*beta_x/a^2. Exact one-dimensional representatives of scalar modes.
    N = 1+t*al
    q = (Q+t*sd-t**2*bx*sx/a**2)/N
    Y = s.exp(-2*t*z)*t**2*sx**2/a**2
    R3 = s.exp(-2*t*z)*(-4*t*zxx-2*t**2*zx**2)/a**2
    U = H+t*zd-t**2*bx*zx/a**2
    extrinsic = (-6*U**2+4*U*t*bxx/a**2)/N**2
    # C(Q) derivatives multiply Y=O(t^2), so only its background value enters L2.
    K = K0+A*(q-Q)+B*(q-Q)**2/2
    density = a**3*s.exp(3*t*z)*(M*N*(R3+extrinsic-2*Lam)/2
                    + W-N*V+N*(K-C*Y))
    raw = s.expand(s.diff(density, t, 2).subs(t, 0)/(2*a**3))
    # Integration by parts with periodic/decaying spatial boundary data.
    red = s.expand(raw.subs(bx*zx, -bxx*z).subs(bx*sx, -bxx*sig).subs(z*zxx, -zx**2))
    czz = red.coeff(zd).coeff(z)
    red = s.expand(red-czz*z*zd-(3*H*czz+dt(czz))*z**2/2)
    czs = red.coeff(sd).coeff(z)
    red = s.expand(red-czs*z*sd-czs*sig*zd-(3*H*czs+dt(czs))*sig*z)
    red = s.factor(red.subs(V, 3*M*H**2-Lam*M-Q*A+K0))
    target = M*(-3*(zd-H*al)**2+zx**2/a**2-2*al*zxx/a**2
                    +2*(zd-H*al)*bxx/a**2) + B*(sd-Q*al)**2/2-3*A*sig*zd-C*sx**2/a**2+A*sig*bxx/a**2
    check('ADM_expansion_and_background_IBP', eq(red, target))
    fourier = s.expand(red.subs({zx**2: a**2*k2*z**2, sx**2: a**2*k2*sig**2,
                                zxx: -a**2*k2*z, bxx: -a**2*k2*be}))
    shift_eq = s.diff(fourier, be)
    lapse_solution = s.solve(shift_eq, al)[0]
    check('finite_k_momentum_constraint', eq(lapse_solution, zd/H+A*sig/(2*M*H)))
    after_shift = s.factor(fourier.subs(al, lapse_solution))
    u, ud, p, pz = s.symbols('u ud p pz', real=True)
    r = Q/H
    switched = s.expand(after_shift.subs({sig: u+r*z, sd: ud+r*zd+dt(r)*z}))
    cuz = switched.coeff(zd).coeff(u)
    switched = s.expand(switched-cuz*u*zd-cuz*z*ud-(3*H*cuz+dt(cuz))*u*z)
    czz2 = switched.coeff(zd).coeff(z)
    switched = s.expand(switched-czz2*z*zd-(3*H*czz2+dt(czz2))*z**2/2)
    d = Q*A/(2*M*H)
    e = -3*A/B+Q*W/(2*M*H**2)
    f = B*Q*W/(2*M*H**2)
    mix = A-2*C*Q
    D = W-Q*A+2*C*Q**2
    az = e*f-k2*D/H**2
    normal = B*(ud-d*u)**2/2-3*A**2*u**2/(4*M)-C*k2*u**2 \
             +z*(f*(ud-d*u)+k2*mix*u/H)+az*z**2/2
    check('full_reduced_quadratic_action', eq(switched, normal))
    check('no_clock_velocity_after_reduction', s.diff(switched, zd) == 0)

    # Canonical constraint algebra AFTER the finite-k lapse/shift solve and clock gauge.
    # Keep a^3: p is an actual conjugate momentum, not an unlabelled rescaled density.
    velocity = s.solve(s.Eq(p, s.diff(a**3*normal, ud)), ud)[0]
    ham = s.factor((p*ud-a**3*normal).subs(ud, velocity))
    secondary = -s.diff(ham, z)
    coords, momenta = [u, z], [p, pz]

    def pb(x, y, qs, ps):
        return s.factor(sum(s.diff(x, q0)*s.diff(y, p0)-s.diff(x, p0)*s.diff(y, q0)
                            for q0, p0 in zip(qs, ps)))

    constraints = [pz, secondary]
    brackets = s.Matrix([[pb(x,y,coords,momenta) for y in constraints] for x in constraints])
    rank = brackets.rank()
    coeff = s.factor(brackets[0,1])
    R = 3*A*f/B+k2*D/H**2
    check('computed_bracket_coefficient', eq(coeff, a**3*R))
    check('computed_bracket_determinant', eq(brackets.det(), (a**3*R)**2))
    # Time dependence enters preservation explicitly. Nonzero R fixes the primary multiplier.
    multiplier = s.symbols('multiplier', real=True)
    preservation = dt(secondary)+pb(secondary, ham+multiplier*pz, coords, momenta)
    fixed_multiplier = s.solve(preservation, multiplier)[0]
    check('secondary_preservation_closes', eq(preservation.subs(multiplier, fixed_multiplier), 0))
    # Derive, rather than enter, the high-k physical sound speed and regular kinetic coefficient.
    zsol = s.solve(s.diff(normal,z), z)[0]
    lag_one = s.factor(normal.subs(z,zsol))
    kinetic = s.factor(s.diff(lag_one,ud,2))
    cs_uv = s.factor(-s.limit(s.diff(lag_one,u,2)/k2,k2,s.oo)/s.limit(kinetic,k2,s.oo))
    check('UV_sound_speed_from_action', eq(cs_uv,(2*C-mix**2/D)/B))
    # Orthogonal expansion of the covariant two-field density in a local inertial frame.
    pit, pix = s.symbols('pi_time pi_space', real=True)
    clock_norm = s.sqrt((1+t*pit)**2-t**2*pix**2)
    local_q = ((1+t*pit)*(Q+t*sd)-t**2*pix*sx)/clock_norm
    local_y = -(Q+t*sd)**2+t**2*sx**2+local_q**2
    local_density = W*clock_norm+K0+A*(local_q-Q)+B*(local_q-Q)**2/2-C*local_y
    local_quadratic = s.expand(s.diff(local_density,t,2).subs(t,0)/2)
    spatial_matrix = -s.hessian(local_quadratic,[sx,pix])
    check('covariant_local_gradient_matrix',spatial_matrix == s.Matrix([[2*C,mix],[mix,D]]))
    schur = s.factor(spatial_matrix.det()/D/B)
    check('local_clock_Schur_agrees_with_full_ADM_UV', eq(schur, cs_uv))
    check('frozen_clock_limit', eq(s.limit(cs_uv,W,s.oo),2*C/B))
    check('Lorentz_invariant_quadratic_control', eq(cs_uv.subs(C,A/(2*Q)),A/(Q*B)))

    # Inverse construction: tune the ACTUAL reduced speed, not the frozen-clock speed.
    m, target_ratio = s.symbols('m target_ratio', positive=True)
    epsilon = (1+target_ratio*(m-1))/(1+m-target_ratio)
    proposed_C = A*epsilon/(2*Q)
    repaired_D = s.factor(D.subs({W:m*Q*A,C:proposed_C}))
    repaired_cs = s.factor(cs_uv.subs({W:m*Q*A,C:proposed_C}))
    check('constructive_clock_response_coefficient', eq(repaired_cs,target_ratio*A/(Q*B)))
    check('regular_clock_gradient_for_repair', eq(repaired_D,Q*A*m**2/(1+m-target_ratio)))
    check('distance_from_zero_gradient_boundary',eq(epsilon-1/(1+m),
                target_ratio*m**2/((1+m)*(1+m-target_ratio))))
    # Constructive FLRW reconstruction for constant m: U(tau)=m Qbar KQ,
    # V(tau)=m rho_chi, H^2=Lambda/3+(1+m)rho_chi/(3 M2).
    check('tracking_clock_background_conservation',eq(m*Q*B*qd,-3*H*m*Q*A))
    check('tracking_background_Raychaudhuri',eq((1+m)*Q*B*qd/(6*M*H),-(1+m)*Q*A/(2*M)))
    # Fixed illustrative dimensionless cosh-K parameters; not a data fit.
    samples=[]
    mv, Mv, Q0, Zv, K2v, Iv, Lv, At = 1e-5,1.,1.,1e-3,0.5,0.1,0.7,1e-4
    for j in range(37):
        av=10**(-6+j/4)
        Aval=Iv/av**3
        zz=math.asinh(Aval/(2*K2v*Zv))
        Qv=Q0+Zv*zz
        Bval=2*K2v*math.cosh(zz)
        kval=2*K2v*Zv**2*(math.cosh(zz)-1)
        rhov=Qv*Aval-kval
        H2v=Lv/3+(1+mv)*rhov/(3*Mv)
        Wv=mv*Qv*Aval
        ev=-3*Aval/Bval+Qv*Wv/(2*Mv*H2v)
        rv=At/(At+Aval)
        speed=rv*Aval/(Qv*Bval)
        # Factored forms avoid cancellation; symbolic equivalence is tested above.
        dv=Qv*Aval*mv**2/(1+mv-rv)
        gap=rv*mv**2/((1+mv)*(1+mv-rv))
        check('FLRW_quadratic_sample_'+str(j),H2v>0 and rhov>0 and ev<0 and dv>0 and 0<speed<1)
        samples.append(dict(a=av,H2=H2v,rho_chi=rhov,e=ev,D=dv,cs2=speed,
                            epsilon_minus_gradient_boundary=gap))
    # Initial trial failed at long wavelengths: retain it as an adversarial control.
    badpoint = {a:1,H:1,M:1,W:s.Rational(1,10),Q:1,A:1,B:100,
                C:proposed_C.subs({m:s.Rational(1,10),target_ratio:s.Rational(1,10),A:1,Q:1}),
                k2:s.Rational(1,10**6)}
    check('UV_positive_is_not_full_kinetic_health', kinetic.subs(badpoint)<0 and cs_uv.subs(badpoint)>0)
    # Choose m in the independently derived e<0 region; no other parameter changes.
    point = {a:1,H:1,M:1,W:s.Rational(1,100),Q:1,A:1,B:100,
             C:proposed_C.subs({m:s.Rational(1,100),target_ratio:s.Rational(1,10),A:1,Q:1})}
    checks_point = []
    for kval in [s.Rational(1,10**6),s.Rational(1,100),1,100,10**6]:
        sub = dict(point); sub[k2] = kval
        checks_point.append({'kphys2':str(kval),'kinetic':str(kinetic.subs(sub)),
                             'bracket_det':str(brackets.det().subs(sub))})
        check('positive_kinetic_k2_'+str(kval), kinetic.subs(sub)>0)
    check('positive_subluminal_constructed_UV_speed', 0<cs_uv.subs(point)<1)

    # k=0 must be derived before division by the shift equation. No beta equation remains.
    I, ps, pa = s.symbols('I ps palpha', real=True, nonzero=True)
    hom = s.expand(a**3*fourier.subs(k2,0).subs(A,I/a**3))
    hom_hessian = s.hessian(hom,[zd,sd])
    sol = s.solve([pz-s.diff(hom,zd),ps-s.diff(hom,sd)],[zd,sd])
    hham = s.factor((pz*zd+ps*sd-hom).subs(sol))
    hqs,hps = [z,sig,al],[pz,ps,pa]
    hsecondary = s.diff(hham,al)

    def dth(expr):
        return s.factor(dt(expr).subs(A,I/a**3))

    htertiary_raw = s.factor(dth(hsecondary)+pb(hsecondary,hham,hqs,hps))
    htertiary = s.factor(-2*M*htertiary_raw/W)
    check('homogeneous_tertiary_from_preservation',eq(htertiary,pz+3*I*sig))
    hfourth_raw = s.factor(dth(htertiary)+pb(htertiary,hham,hqs,hps))
    hfourth = s.factor(hfourth_raw/(3*I*Q))
    check('homogeneous_lapse_constraint',eq(hfourth,al+ps/(a**3*B*Q)))
    hc = [pa,hsecondary,htertiary,hfourth]
    hbrackets = s.Matrix([[pb(x,y,hqs,hps) for y in hc] for x in hc])
    hrank = hbrackets.rank()
    hpreservation = dth(hfourth)+pb(hfourth,hham+multiplier*pa,hqs,hps)
    hfixed = s.solve(hpreservation,multiplier)[0]
    check('homogeneous_chain_closes',eq(hpreservation.subs(multiplier,hfixed),0))

    # Reconstruct finite-k lapse/shift primaries too, without relying on the Lagrangian solve.
    # First eliminate the actual second-class shift pair; remaining canonical brackets are unchanged.
    pbeta = s.symbols('pbeta', real=True)
    full = a**3*fourier
    fv = s.solve([pz-s.diff(full,zd),ps-s.diff(full,sd)],[zd,sd])
    fh = s.factor((pz*zd+ps*sd-full).subs(fv))
    shift_secondary = s.factor(s.diff(fh,be))
    beta_solution = s.solve(shift_secondary,be)[0]
    bqs,bps = [z,sig,al,be],[pz,ps,pa,pbeta]
    bpair = [pbeta,shift_secondary]
    bmatrix = s.Matrix([[pb(x,y,bqs,bps) for y in bpair] for x in bpair])
    staged_h = s.factor(fh.subs(be,beta_solution))
    sc = s.factor(s.diff(staged_h,al))
    tc = s.factor(dt(sc)+pb(sc,staged_h,hqs,hps))
    check('finite_k_clock_tertiary',eq(tc,-W*(pz+3*a**3*A*sig)/(2*M)+a**3*k2*mix*sig))
    last_pres = s.factor(dt(tc)+pb(tc,staged_h,hqs,hps))
    alpha_solution = s.solve(last_pres,al)[0]
    ac = al-alpha_solution
    full_constraints = [pbeta,shift_secondary,pa,sc,tc,ac]
    full_matrix = s.Matrix([[pb(x,y,bqs,bps) for y in full_constraints] for x in full_constraints])
    full_rank = full_matrix.rank()
    check('lapse_fixing_coefficient',eq(pb(tc,sc,hqs,hps),-a**3*(3*Q*A*W/(2*M)+k2*D)))
    # The preservation equation is affine in the primary multiplier: do not send
    # its large time-dependent forcing through the general-purpose nonlinear solver.
    forcing = dt(ac)+pb(ac,staged_h,hqs,hps)
    multiplier_coefficient = pb(ac,pa,hqs,hps)
    final_lam = -forcing/multiplier_coefficient
    check('full_finite_k_staged_chain_closes',eq(forcing+multiplier_coefficient*final_lam,0))

    return {'scope':'Quadratic EH/cuscuton/chi sector on FLRW only; full MOND theory OPEN',
            'checks':checks, 'L2_per_a3':str(target), 'reduced_L2_per_a3':str(normal),
            'finite_k':{'constraints':[str(c) for c in constraints],
                       'poisson_matrix':str(brackets),'rank':rank,
                       'second_class':rank,'first_class':len(constraints)-rank,
                       'canonical_scalar_pairs':(2*len(coords)-2*(len(constraints)-rank)-rank)//2,
                       'kinetic':str(kinetic),'UV_cs2':str(cs_uv)},
            'homogeneous':{'constraints':[str(c) for c in hc],
                           'poisson_matrix':str(hbrackets),'rank':hrank,
                           'velocity_hessian_rank':hom_hessian.rank(),
                           'second_class':hrank,'first_class':len(hc)-hrank,
                           'canonical_global_pairs':(2*len(hqs)-2*(len(hc)-hrank)-hrank)//2,
                           'not_a_wave_count':'fixed finite comoving cell; global boundary/gauge choice matters'},
            'full_gauge_fixed_finite_k':{'constraints':[str(c) for c in full_constraints],
                           'poisson_matrix':str(full_matrix),'rank':full_rank,
                           'second_class':full_rank,'first_class':len(full_constraints)-full_rank,
                           'scalar_pairs':(2*len(bqs)-2*(len(full_constraints)-full_rank)-full_rank)//2,
                           'shift_pair_matrix':str(bmatrix),'shift_pair_rank':bmatrix.rank(),
                           'scope':'quadratic scalar sector, spatial gauge and tau=t fixed; not nonlinear Dirac'},
            'repair':{'epsilon':str(epsilon),'C':str(proposed_C),'D':str(repaired_D),
                      'cs2':str(repaired_cs),'domain':'m>0, 0<target_ratio<=1; KQ,KQQ,Q>0',
                      'finite_k_no_ghost_sufficient':'e=-3 KQ/KQQ+Q mu2/(2 M2 H^2)<0'},
            'quadratic_positive_example':checks_point,
            'tracking_cosh_background_samples':samples,
            'remaining':['nonlinear full Dirac analysis','complete MOND source/lensing coupling',
                         'physical PPN','full-action Boltzmann observables','IR masses and growth',
                         'zero-field strong coupling','causality of elliptic response','empirical likelihood']}


if __name__ == '__main__':
    print(json.dumps(run(),indent=2))
