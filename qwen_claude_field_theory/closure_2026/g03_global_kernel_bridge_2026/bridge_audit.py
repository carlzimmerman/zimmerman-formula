#!/usr/bin/env python3
"""Bounded audit of the f34/f35 static limit, not a relativistic certification.

Contract: real fields, positive bare G, A=2-K_B>0, B=2-c14>0,
clock-rest weak/static branch Q0->0, no homogeneous scalar charge, spherical
Gauss branch or uniform-gradient/long-wavelength limit. The static action
below spells out the f34/f35 source terms before eliminating spatial Psi.
Higher spatial derivatives are omitted only in this stated limit. We test
whether a regular single-valued scalar constitutive law can give either
exact target kernel at the new J_Y,Newton=30 corner. No Dirac/PPN/causality
certificate, finite-xi solution, data exclusion, or universal no-go follows.

Default: 0 iff internal algebra/numerics agree; --strict-corner: 2 iff the
named corner fails a necessary condition. Outputs are regenerated, never
loaded as certificates. See REPORT.md for proof, scope and normalization.
"""
import argparse
import datetime
import hashlib
import json
import math
from pathlib import Path
import platform
import subprocess
import time

import mpmath as mp
import scipy
from scipy.optimize import brentq
import sympy as sp

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]


def rar_slope(u):
    e = math.exp(-u)
    m = -math.expm1(-u)
    return 1/m - u*e/(2*m*m)


def derive():
    A, B, a0 = sp.symbols('A B a0', positive=True)
    p, z, s, n = sp.symbols('p z s n', real=True)
    j = sp.symbols('j', real=True)
    J = sp.Function('J')
    # One gradient component represents each isotropic contraction. p=grad Phi,
    # z=grad Psi, s=grad chi; matter source is -16*pi*Gt*rho*Phi.
    L = 2*z**2 - 4*p*z + (2-B)*p**2 + 2*A*p*s - A*(s**2+a0**2*J(s**2/a0**2))
    residuals = {'independent_Psi_flux': sp.diff(L, z)-4*(z-p)}
    Lred = sp.expand(L.subs(z, p))
    eta = A/B
    Ldiag = sp.expand(Lred.subs(p, n+eta*s))
    residuals['completion_of_square'] = sp.simplify(
        Ldiag - (-B*n**2-A*(1-eta)*s**2-A*a0**2*J(s**2/a0**2)))
    scalar_flux = sp.simplify(-sp.diff(Ldiag, s)/(2*A))
    # Verify the nonlinear flux by a polynomial test function too, independently
    # of how SymPy prints the derivative of a composed arbitrary function.
    W = sp.symbols('W', real=True)
    Jtest = W**2 + W**3/3
    actual = -sp.diff(Ldiag.subs(J(s**2/a0**2), Jtest.subs(W, s**2/a0**2)), s)/(2*A)
    target = (1-eta+sp.diff(Jtest,W).subs(W,s**2/a0**2))*s
    residuals['nonlinear_flux_polynomial_control'] = sp.simplify(actual-target)
    # Quadratic static Euler equations, with 4*pi*Gt*rho normalized to 1.
    Lq = L.subs(J(s**2/a0**2), j*s**2/a0**2)
    equations = [sp.diff(Lq,p)+4, sp.diff(Lq,z), sp.diff(Lq,s)]
    sol = sp.solve(equations, (p,z,s), dict=True)[0]
    measured_ratio = sp.simplify(sol[p]/(2/B))
    scalar_share_expr = sp.factor(measured_ratio-1)
    residuals['measured_G_from_Euler_equations'] = sp.simplify(
        scalar_share_expr-eta/(1+j-eta))
    residuals['independent_static_no_slip'] = sp.simplify(sol[z]-sol[p])
    etav = sp.Rational(180000,199999)  # K_B=1/5, c14=1/100000; not a fitted result.
    fs = sp.factor(scalar_share_expr.subs({A:sp.Rational(9,5), B:sp.Rational(199999,100000), j:30}))

    u = sp.symbols('u', positive=True)
    curve = u**2/(1-sp.exp(-u))
    D = sp.simplify(sp.diff(curve,u)/(2*u))
    h = u-3+(u+3)*sp.exp(-u)
    residuals['RAR_stationary_equation'] = sp.simplify(
        sp.diff(D,u) - sp.exp(-u)*h/(2*(1-sp.exp(-u))**3))
    residuals['RAR_root_uniqueness_convexity'] = sp.simplify(
        sp.diff(h,u,2)-(u+1)*sp.exp(-u))
    # Unique positive stationary root: h(0)=0, h'(0)=-1, h''>0,
    # h(3)>0. Its numerical value is computed in two arithmetic systems.
    root = brentq(lambda v:v-3+(v+3)*math.exp(-v), 2, 3, xtol=1e-14)
    with mp.workdps(70):
        root_mp = mp.findroot(lambda v:v-3+(v+3)*mp.exp(-v), (2,3))
        dm = 1/(1-mp.exp(-root_mp))-root_mp*mp.exp(-root_mp)/(2*(1-mp.exp(-root_mp))**2)
        fmin_rar_text = mp.nstr(1/dm-1, 60)
    assert abs(root-float(root_mp)) < 1e-12
    assert abs((1/rar_slope(root)-1)-float(fmin_rar_text)) < 1e-13
    x = sp.symbols('x', positive=True)
    mu = 1-sp.exp(-x)
    invD = sp.diff(x*mu,x)
    residuals['EXP_global_max_derivative'] = sp.simplify(sp.diff(invD,x)-(2-x)*sp.exp(-x))
    fmin_exp = sp.simplify(invD.subs(x,2)-1)
    rar_margin = rar_slope(2.5)-1/(1+float(fs))
    exp_margin = float(1/invD.subs(x,2)-1/(1+fs))

    # Correct energy density directly from lapse variation of L_phi=-N*a^3*K(v/N).
    N, av = sp.symbols('N a', positive=True)
    v, Q, Q0, K2, C = sp.symbols('v Q Q0 K2 C', real=True)
    K = sp.Function('K')
    rho_actual = sp.simplify(-sp.diff(-N*av**3*K(v/N),N).subs(N,1)/av**3).subs(v,Q)
    rho_target = K(Q)-Q*sp.diff(K(Q),Q)
    residuals['FLRW_lapse_density'] = sp.simplify(rho_actual-rho_target)
    Kquad = K2*(Q-Q0)**2
    rho_quad = sp.expand((Kquad-Q*sp.diff(Kquad,Q)).subs(Q,Q0+C/(2*K2*av**3)))
    residuals['FLRW_charge_substitution'] = sp.simplify(rho_quad+Q0*C/av**3+C**2/(4*K2*av**6))
    example = rho_quad.subs({K2:-10,Q0:1,C:-2,av:1})
    return {
        'exact_residuals': residuals,
        'static_action': L,
        'diagonal_action': Ldiag,
        'nonlinear_scalar_flux': scalar_flux,
        'scalar_share_formula': scalar_share_expr,
        'scalar_share': float(fs), 'scalar_share_exact': fs,
        'rar_minimum_at_u': root, 'rar_minimum_slope': rar_slope(root),
        'rar_share_infimum': fmin_rar_text, 'exp_share_infimum': fmin_exp,
        'rar_witness_margin': rar_margin, 'exp_witness_margin': exp_margin,
        'kernel_necessary_gates': {'nu_RAR': float(fs)>float(fmin_rar_text),
                                   'mu_exp': float(fs)>float(fmin_exp)},
        'rar_JN_upper_boundary': float(etav*(1+1/float(fmin_rar_text))-1),
        'exp_JN_upper_boundary': float(etav*(1+1/fmin_exp)-1),
        'rho_actual': rho_actual, 'rho_quadratic': rho_quad,
        'rho_healthy_example': example, 'rho_claimed_example': -example,
        'flrw_wrong_sign_residual': sp.simplify(rho_actual-(Q*sp.diff(K(Q),Q)-K(Q))),
        'same_action_corner_necessary_gate': rar_margin>0 and exp_margin>0,
    }


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--strict-corner',action='store_true')
    args=parser.parse_args()
    started=datetime.datetime.now(datetime.timezone.utc).isoformat()
    t0=time.monotonic()
    result=derive()
    assert all(v==0 for v in result['exact_residuals'].values()), result['exact_residuals']
    serialized=json.dumps(result,default=str,indent=2,sort_keys=True)+'\n'
    print(serialized)
    if args.strict_corner:
        return 0 if result['same_action_corner_necessary_gate'] else 2
    (HERE/'results.json').write_text(serialized)
    rel=lambda p:str(p.relative_to(ROOT))
    sources=[HERE/'bridge_audit.py',HERE/'test_bridge_audit.py',HERE/'REPORT.md',HERE/'results.json',
        ROOT/'STANDING.md',ROOT/'hunt_2026/f34_timedep_scalar_sector.py',ROOT/'hunt_2026/f35_measured_G.py',
        ROOT/'qwen_claude_field_theory/closure_2026/g03e_flrw_background.py']
    manifest={
        'schema_version':1, 'claim_id':'g03-global-kernel-bridge-2026',
        'repository':{'commit':subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),
                      'dirty':bool(subprocess.check_output(['git','status','--porcelain'],cwd=ROOT,text=True))},
        'command':'python3 -B '+rel(HERE/'bridge_audit.py'),
        'environment':{'software':['Python '+platform.python_version(),'SymPy '+sp.__version__,
                                   'SciPy '+scipy.__version__,'mpmath '+mp.__version__], 'hardware':platform.machine()},
        'mathematics':{'assertion_tested':__doc__, 'coefficient_domain':'real symbolic algebra; binary64 and 70-digit mpmath root',
            'conventions':'REPORT.md; large-scale G normalization tested explicitly',
            'inputs':['K_B=1/5','c14=1/100000','J_Y,Newton=30'],
            'bounds':{'RAR_root_bracket':[2,3],'RAR_counterexample_u':2.5,'EXP_counterexample_x':2},
            'non_claims':['full action closure','finite-xi no-go','observational exclusion','novel general theorem']},
        'randomness':{'used':False,'generator':'','seed':None},
        'run':{'started_at':started,'runtime_seconds':time.monotonic()-t0,'exit_status':0},
        'outputs':[{'path':rel(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in sources],
        'checks':[{'name':k,'passed':v==0} for k,v in result['exact_residuals'].items()],
        'result':'Named J_Y=30 corner fails both exact-kernel long-wavelength necessary gates; broader theory remains OPEN.',
        'residual_risks':['Static reduction only, not full covariant derivation.',
                          'Source files may be concurrently updated; hashes record inspected versions.',
                          '3 percent empirical cap is not established here; no observational exclusion claimed.']}
    (HERE/'computation_manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    return 0


if __name__=='__main__':
    raise SystemExit(main())
