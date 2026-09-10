#!/usr/bin/env python3
"""Fixed-action homogeneous radiation constraints and bounded nearby solves.

No background coefficient is refitted. stdout is the result; no files written.
"""
from __future__ import annotations
import hashlib
import json
from pathlib import Path
import platform
import subprocess
import mpmath as mp
import sympy as s


def symbolic():
    a, lapse, vr, cr, pr = s.symbols("a N vr Cr pr", positive=True)
    Lr = cr * a**3 * vr**4 / lapse**3
    momentum = s.diff(Lr, vr)
    rho = s.simplify(-s.diff(Lr, lapse) / a**3)
    pressure = s.simplify(s.diff(Lr, a) / (3 * lapse * a**2))
    speed = (pr / (4 * cr * a**3))**s.Rational(1, 3)
    radiation_ham = s.simplify((pr * vr - Lr).subs(vr, lapse * speed))
    R = 3 * cr * (pr / (4 * cr))**s.Rational(4, 3)
    H, Q, j, bH, bQ, rho_r = s.symbols("H Q j bH bQ rho_r", real=True)
    k11, k12, k22 = s.symbols("k11 k12 k22", real=True)
    K = s.Matrix([[k11, k12], [k12, k22]])
    b = s.Matrix([bH, bQ])
    v = s.Matrix([H, Q])
    gradC = K * v
    J = s.Matrix([list(gradC), list(b)])
    Delta0 = (b.T * K.inv() * (3 * j * s.Matrix([Q, -H])))[0]
    response = s.simplify(J.inv() * s.Matrix([-rho_r, 0]))
    checks = {
        "radiation_eos": s.simplify(rho - 3 * pressure) == 0,
        "radiation_legendre": s.simplify(radiation_ham - lapse * R / a) == 0,
        "radiation_charge_relation": s.simplify(momentum.subs(vr, lapse * speed) - pr) == 0,
        "radiation_scale_force": s.simplify(-a * s.diff(R / a, a) / a**3 - R / a**4) == 0,
        "constraint_jacobian_gap_identity": s.factor(Delta0 * K.det() + 3 * j * J.det()) == 0,
        "linear_constraint_response": s.simplify(J * response + s.Matrix([rho_r, 0])) == s.zeros(2, 1),
    }
    # Exact canonical preservation with radiation, before restricting C or T.
    f, fh, fq, W, pt, vt, ptx, source_explicit = s.symbols('f fh fq W Ptau Vtau PtauX Ttau', real=True)
    Rc=s.Matrix([3*f-3*H*fh+rho_r,-3*H*fq])
    actual_b=s.Matrix([3*W,-2*Q*ptx])
    velocity_flow=K.inv()*(lapse*Rc+actual_b)
    Ct=H*fh+Q*fq-f+rho_r
    T=vt-pt+3*H*W
    Cdot=(gradC.T*velocity_flow)[0]+2*Q*Q*ptx-pt+vt-4*lapse*H*rho_r
    Delta=3*H*T+(actual_b.T*K.inv()*Rc)[0]
    F0=source_explicit+(actual_b.T*K.inv()*actual_b)[0]
    Tdot=source_explicit+(actual_b.T*velocity_flow)[0]
    checks.update({
        'exact_C_preservation_with_radiation':s.factor(Cdot-T+3*lapse*H*Ct)==0,
        'exact_T_preservation_source':s.factor(Tdot-lapse*Delta-F0+3*lapse*H*T)==0,
        'exact_chi_charge_conservation':s.factor((K*velocity_flow)[1]+2*Q*ptx+3*lapse*H*fq)==0,
    })
    return dict(checks=checks, passed=all(checks.values()), radiation_hamiltonian=str(radiation_ham),
                radiation_comoving_constant=str(R), linear_response=str(response),
                constraint_jacobian_determinant=str(J.det()))


def original_coefficient_jets():
    """Exact local jets of the original radiation-free reconstruction at a=1.

    No numerical ODE history or radiation-adjusted H is supplied to the action.
    The derivative vector is the original stationary m,v history.
    """
    a0, m0, v0 = mp.mpf(1), mp.mpf('.1'), mp.mpf('.5')
    I, Qc, M2, Lambda = mp.mpf('.1'), mp.mpf(1), mp.mpf(1), mp.mpf('.7')
    def state_flow(a, m, v):
        hb = mp.sqrt((Lambda + Qc * I / a**3 / M2) / 3)
        omega = (Qc * I / a**3) / (M2 * Lambda + Qc * I / a**3)
        md = hb * m * (mp.mpf('1.5') * omega + 3 * v * (m + 1) / (m + 2))
        vd = hb * (v - 1) * (3 * omega * (3*m*m+8*m+6) / (2*(m+1)*(m+2))
             + 3*v*(m*m+2*m+2)/(m+2)**2 - 2)
        return a * hb, md, vd
    flow = state_flow(a0, m0, v0)
    accel = tuple(mp.diff(lambda t: state_flow(a0+t*flow[0], m0+t*flow[1], v0+t*flow[2])[i], 0) for i in range(3))
    def coeffs(t):
        av = a0 + flow[0]*t + accel[0]*t*t/2
        mv = m0 + flow[1]*t + accel[1]*t*t/2
        A = I / av**3
        q = Qc / (1 + mv)
        U = mv * q * A
        d = A * U / (2*q*(q*A+U))
        Hb = mp.sqrt((Lambda + Qc * A / M2) / 3)
        return q, U, d, Hb
    jets = [tuple(mp.diff(lambda t: coeffs(t)[i], 0, order) for order in range(3)) for i in range(4)]
    return dict(a=a0, m=m0, v=v0, A=I, M2=M2, Lambda=Lambda, jets=jets,
                background_clock_density=Qc*I, parameters=dict(I=str(I),Qc=str(Qc),M2=str(M2),Lambda=str(Lambda)))


def one_coupling(gamma, ref):
    M2, Lambda = ref['M2'], ref['Lambda']
    qj, uj, dj, hj = ref['jets']
    q0, H0, U0 = qj[0], hj[0], uj[0]
    def poly(j, t): return j[0] + j[1]*t + j[2]*t*t/2
    def P(X, t=mp.mpf(0)):
        q, U, d, Hb = (poly(j, t) for j in ref['jets'])
        return -U/2 * mp.log((U-2*d*X)/(U-2*d*q*q)) + 3*gamma*q*Hb*(X-q*q)
    W = U0 - 2*gamma*q0*q0*qj[1]
    Wt = uj[1] - 2*gamma*(2*q0*qj[1]**2 + q0*q0*qj[2])
    def evaluate(H, Q, rad):
        X = Q*Q
        pv = P(X)
        px = mp.diff(P, X)
        pxx = mp.diff(P, X, 2)
        pt = mp.diff(lambda t: P(X, t), 0)
        ptx = mp.diff(lambda xx: mp.diff(lambda t: P(xx, t), 0), X)
        ptt = mp.diff(lambda t: P(X, t), 0, 2)
        f = -3*M2*H*H + pv - U0 - M2*Lambda - 2*gamma*Q**3*H
        fh = -6*M2*H - 2*gamma*Q**3
        jq = 2*Q*px - 6*gamma*H*Q*Q
        B = 2*px + 4*Q*Q*pxx
        K = mp.matrix([[-6*M2, -6*gamma*Q*Q], [-6*gamma*Q*Q, B-12*gamma*H*Q]])
        Ki = K**-1
        C = -3*M2*H*H + 2*Q*Q*px-pv+U0-6*gamma*H*Q**3+M2*Lambda+rad
        T = uj[1] - pt + 3*H*W
        b = mp.matrix([3*W, -2*Q*ptx])
        Rc = mp.matrix([3*f-3*H*fh+rad, -3*H*jq])
        delta = 3*H*T + (b.T*Ki*Rc)[0]
        source = uj[2]-ptt+3*H*Wt+(b.T*Ki*b)[0]
        N = -source/delta
        fdot = Ki*(N*Rc+b)
        Hdt, Qdt = fdot[0], fdot[1]
        charge_dot = -6*gamma*Q*Q*Hdt+(B-12*gamma*H*Q)*Qdt+2*Q*ptx
        rho_clock = C + 3*M2*H*H-M2*Lambda-rad
        pressure_clock = pv-U0+W/N+2*gamma*Q*Q*Qdt/N
        ch = -6*M2*H-6*gamma*Q**3
        cq = Q*B-18*gamma*H*Q*Q
        J = mp.matrix([[ch,cq],[b[0],b[1]]])
        cdot = ch*Hdt+cq*Qdt+(2*Q*Q*ptx-pt+uj[1])-4*N*H*rad
        tdot = (b.T*fdot)[0]+uj[2]-ptt+3*H*Wt
        return dict(C=C,T=T,H=H,Q=Q,N=N,delta=delta,source=source,
          schur=B-12*gamma*H*Q+6*gamma*gamma*Q**4/M2,domain=U0-2*dj[0]*Q*Q,
          charge=jq,charge_dot_residual=charge_dot+3*N*H*jq,
          raychaudhuri_residual=2*M2*Hdt/N+rho_clock+pressure_clock+mp.mpf(4)/3*rad,
          C_preservation=cdot,T_preservation=tdot,K=K,b=b,J=J,
          radiation_flow=-4*N*H*rad,H_coordinate_dot=Hdt,Q_coordinate_dot=Qdt)
    baseline = evaluate(H0,q0,mp.mpf(0))
    linear = baseline['J']**-1*mp.matrix([-1,0])
    # Differentiate the actual off-shell block and source, not a restricted gap.
    def G(h,q):
        z=evaluate(h,q,mp.mpf(0));return z['source']+z['delta']
    eH=mp.matrix([1,0])
    explicit_rad=(baseline['b'].T*(baseline['K']**-1)*eH)[0]
    Nlinear=-(mp.diff(lambda h:G(h,q0),H0)*linear[0]
              +mp.diff(lambda q:G(H0,q),q0)*linear[1]+explicit_rad)/baseline['delta']
    charge_linear = -6*gamma*q0*q0*linear[0] + baseline['K'][1,1]*linear[1]
    # A one-dimensional solve is exactly the tertiary equation eliminated for H.
    def h_of_q(Q): return (mp.diff(lambda t:P(Q*Q,t),0)-uj[1])/(3*W)
    def radiation_required(Q): return -evaluate(h_of_q(Q),Q,mp.mpf(0))['C']
    previous_q=q0
    rows=[]
    ratios=['0','1e-4','1e-3','.01','.1','.3','1']
    for raw in ratios:
        ratio=mp.mpf(raw);rad=ratio*ref['background_clock_density']
        try:
            if not ratio: Q=q0
            else:
                guess=q0+linear[1]*rad if ratio<=mp.mpf('.001') else previous_q
                Q=mp.findroot(lambda q:radiation_required(q)-rad,(guess,guess*(1-mp.mpf('1e-6'))),tol=mp.mpf('1e-58'),maxsteps=60)
            H=h_of_q(Q)
            if isinstance(Q,mp.mpc) or isinstance(H,mp.mpc): raise ValueError('complex continuation')
            z=evaluate(H,Q,rad)
            previous_q=Q
            fields=('H','Q','N','delta','source','schur','domain','charge','C','T',
                    'charge_dot_residual','raychaudhuri_residual','C_preservation','T_preservation')
            row={k:str(z[k]) for k in fields}
            row.update(radiation_over_old_clock=raw,solved=True,
              regular_expanding_positive_lapse=bool(H>0 and z['N']>0 and z['domain']>0 and z['schur']!=0 and z['delta']!=0),
              delta_H=str(H-H0),delta_Q=str(Q-q0),delta_N=str(z['N']-1),delta_charge=str(z['charge']-ref['A']))
            assert max(abs(z[k]) for k in ('C','T','charge_dot_residual','raychaudhuri_residual','C_preservation','T_preservation'))<mp.mpf('1e-48')
            rows.append(row)
        except (ValueError,ZeroDivisionError,AssertionError) as exc:
            rows.append(dict(radiation_over_old_clock=raw,solved=False,error=str(exc)))
    tiny=mp.mpf('1e-8')*ref['background_clock_density']
    tq=mp.findroot(lambda q:radiation_required(q)-tiny,(q0,q0+linear[1]*tiny),tol=mp.mpf('1e-60'))
    tz=evaluate(h_of_q(tq),tq,tiny)
    errors={k:str(abs(actual-pred)/max(1,abs(pred))) for k,actual,pred in (
      ('H_slope',(tz['H']-H0)/tiny,linear[0]),('Q_slope',(tq-q0)/tiny,linear[1]),
      ('N_slope',(tz['N']-1)/tiny,Nlinear),('charge_slope',(tz['charge']-ref['A'])/tiny,charge_linear))}
    assert all(mp.mpf(v)<mp.mpf('1e-5') for v in errors.values())
    assert abs(baseline['C'])<mp.mpf('1e-60') and abs(baseline['T'])<mp.mpf('1e-60') and abs(baseline['N']-1)<mp.mpf('1e-58')
    det_identity=mp.det(baseline['J'])+mp.det(baseline['K'])*baseline['delta']/(3*ref['A'])
    assert abs(det_identity)<mp.mpf('1e-60')
    # Optional comparison: retain the OLD chi integration charge by allowing
    # physical a to shift at this fixed tau. Coefficient functions still do not.
    fixed_charge=[]
    previous_q=q0
    for raw in ratios:
        R=mp.mpf(raw)*ref['background_clock_density']
        def comp(Q):
            z=evaluate(h_of_q(Q),Q,mp.mpf(0))
            aa=(ref['A']/z['charge'])**(mp.mpf(1)/3)
            return aa,z
        def equation(Q):
            aa,z=comp(Q)
            return -z['C']-R/aa**4
        if not R: Q=q0
        else: Q=mp.findroot(equation,(previous_q,previous_q*(1-mp.mpf('1e-6'))),tol=mp.mpf('1e-58'))
        aa,_=comp(Q);rad=R/aa**4
        z=evaluate(h_of_q(Q),Q,rad);previous_q=Q
        assert abs(aa**3*z['charge']-ref['A'])<mp.mpf('1e-60')
        assert abs(z['C'])<mp.mpf('1e-48') and abs(z['T'])<mp.mpf('1e-48')
        fixed_charge.append(dict(comoving_radiation_over_reference_clock=raw,a=str(aa),
            actual_radiation_density=str(rad),H=str(z['H']),Q=str(Q),N=str(z['N']),
            conserved_chi_charge=str(aa**3*z['charge']),regular_expanding_positive_lapse=bool(z['H']>0 and z['N']>0 and z['domain']>0 and z['schur']!=0 and z['delta']!=0)))
    return dict(gamma=str(gamma),W_fixed=str(W),baseline_gap=str(-baseline['delta']),
      baseline_jacobian_determinant=str(mp.det(baseline['J'])),
      linear_per_unit_rho=dict(H=str(linear[0]),Q=str(linear[1]),N=str(Nlinear),charge=str(charge_linear)),
      fixed_old_charge_linear_a_response=str(-charge_linear/(3*ref['A'])),
      linear_response_small_radiation_errors=errors,rows=rows,
      fixed_old_charge_with_shifted_scale=fixed_charge)


def run():
    mp.mp.dps=70
    exact=symbolic();assert exact['passed']
    ref=original_coefficient_jets()
    runs=[one_coupling(mp.mpf(g),ref) for g in ('0','1e-6')]
    return dict(symbolic=exact,parameters=ref['parameters'],epoch=dict(a='1',m='.1',v='.5'),
      precision_digits=70,radiation_background='rho_r=R/a^4; rho_r/old_clock from 0 to 1',
      fixed_reconstruction_jets=[[str(v) for v in j] for j in ref['jets']],jet_order=['q','U','d','Hbar'],runs=runs,
      scope='Nearby homogeneous fixed-action radiation branches at one epoch. Changed integration charge is reported; no coefficient refitting, global radiation evolution, perturbation stability, or CMB claim.')


if __name__=='__main__':
    result=run()
    source=Path(__file__).resolve();root=next(p for p in source.parents if (p/'.git').exists())
    result['provenance']=dict(base='ebb49936640781e220c7b28ac4369acf36b46711',
      current_head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=root,text=True).strip(),
      source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),python=platform.python_version(),
      sympy=s.__version__,mpmath=mp.__version__)
    print(json.dumps(result,indent=2,sort_keys=True))
