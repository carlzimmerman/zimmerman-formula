#!/usr/bin/env python3
"""Scoped matter/domain obstructions to promoting the cylinder source test.

This does not test the full theory's causal response with ordinary matter.
It checks why the previously prescribed source is not that response.
"""
from pathlib import Path
import hashlib
import json
import subprocess
import sys
import time

import numpy as np
import sympy as sp

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]


def main():
    start = time.time()
    checks = []

    def check(name, ok, evidence):
        checks.append(dict(name=name, passed=bool(ok), evidence=evidence))
        print(('ok: ' if ok else 'FAIL: ') + name)

    t, x, a, r, E, Q, eps, z = sp.symbols('t x a r E Q eps z', real=True)
    Z = sp.Function('Z')(t, x)
    rho = 2*(-sp.diff(Z, x, 2)+a*a*Z)
    flux = 2*sp.exp(-a*x)*(sp.diff(Z, t, x)-a*sp.diff(Z, t))
    px = 2*(-sp.exp(-2*a*x)*sp.diff(Z, t, 2)+a*sp.diff(Z, x)-a*a*Z)
    identities = [sp.simplify(sp.exp(-a*x)*sp.diff(rho,t)+sp.diff(flux,x)+2*a*flux),
                  sp.simplify(sp.exp(-a*x)*sp.diff(flux,t)+sp.diff(px,x)+a*(rho+px))]
    check('external source satisfies both conservation identities', identities == [0,0], list(map(str,identities)))

    # In any spherical metric ds2=g_AB dx^A dx^B+r^2 dOmega^2,
    # sqrt(-g4) F^AB is the two-dimensional alternating symbol times r^2 E.
    # Maxwell equations are therefore partial_A(r^2 E)=0, independently
    # of lapse and shift. No spherical neutral matter current is present.
    A, B, C = sp.symbols('A B C', positive=True)
    g2 = sp.Matrix([[-A,B],[B,C]])
    F = sp.Matrix([[0, E*sp.sqrt(-g2.det())],[-E*sp.sqrt(-g2.det()),0]])
    raised = sp.simplify(g2.inv()*F*g2.inv().T)
    density = sp.simplify(sp.sqrt(-g2.det())*r*r*raised[0,1])
    check('spherical source-free Maxwell reduces to constant flux', sp.simplify(density+r*r*E)==0,
          dict(densitized_Ftx=str(density), equations='partial_t(r^2 E)=partial_x(r^2 E)=0'))
    rho_em = Q*Q/(2*r**4)
    drho = sp.diff(rho_em.subs(r,r*sp.exp(eps*z)),eps).subs(eps,0)
    check('fixed Maxwell charge has only the already included area response',
          sp.simplify(drho+4*rho_em*z)==0,
          dict(delta_rho=str(drho), additional_compact_flux='delta Q=0 by space/time constancy and compact support'))

    # The exact tested spatial Z is B''. Compact smoothness makes all
    # boundary jets zero; the density integral is a boundary expression.
    Bump = sp.Function('B')(x)
    rho_bump = 2*(-sp.diff(Bump,x,4)+a*a*sp.diff(Bump,x,2))
    primitive = 2*(-sp.diff(Bump,x,3)+a*a*sp.diff(Bump,x))
    check('constructed additional density has exactly zero spatial integral',
          sp.simplify(sp.diff(primitive,x)-rho_bump)==0,
          'Integral rho dx=[2(-B third derivative+a^2 B first derivative)] at both compact-support endpoints=0.')
    width = sp.Rational(9,20)
    explicit = sp.exp(-1/(1-(x/width)**2))
    center = sp.simplify(rho_bump.subs(Bump,explicit).doit().subs(x,0))
    # Strictly positive center + zero integral proves negative somewhere;
    # this exact sign check does not infer positivity from sampled values.
    check('density is nonzero and signed at an exact illustrative acceleration',
          bool(center.subs(a,sp.Rational(2)).is_positive),
          dict(center_expression=str(center), exact_test_a=2,
               interpretation='At a=2 center>0; zero integral forces negative density somewhere. General branch condition is given by center expression.'))
    # More generally L=-d_x^2+a^2 is injective on compact smooth functions:
    # integral Z L Z=integral[(Z_x)^2+a^2 Z^2]>0. Thus any nonzero
    # compact B'' has nonzero, zero-integral rho for every real a.
    product_identity = sp.simplify(Z*(-sp.diff(Z,x,2)+a*a*Z)
                          +sp.diff(Z*sp.diff(Z,x),x)-sp.diff(Z,x)**2-a*a*Z**2)
    check('signed-density argument is independent of numerical background a', product_identity==0,
          'Integration by parts: integral Z(-Z_xx+a^2 Z)=integral (Z_x)^2+a^2 Z^2>0 for nonzero compact Z; rho cannot vanish identically.')
    killing_primitive=2*sp.exp(a*x)*(a*Z-sp.diff(Z,x))
    check('compact source has exactly zero Killing energy',
          sp.simplify(sp.diff(killing_primitive,x)-sp.exp(a*x)*rho)==0,
          'Integral e^(ax) rho_s dx is the endpoint value of 2e^(ax)(aZ-Z_x), hence zero for any compact smooth Z. Positive particle additions have strictly positive Killing energy.')
    wrong=sp.simplify(sp.exp(a*x)*(rho+Z)-sp.diff(killing_primitive,x))
    check('Killing energy negative control detects an added nonconserved density',
          sp.simplify(wrong-sp.exp(a*x)*Z)==0 and wrong!=0, str(wrong))
    evaluate=sp.lambdify((x,a),rho_bump.subs(Bump,explicit).doit(),'numpy')
    numeric=[]
    for av in (.5,2.,4.):
        for order in (128,256,512):
            nodes,weights=np.polynomial.legendre.leggauss(order)
            points=float(width)*nodes
            values=evaluate(points,av)
            weighted=weights*float(width)*np.exp(av*points)*values
            numeric.append(dict(a=av,order=order,minimum=float(np.min(values)),maximum=float(np.max(values)),
                                relative_energy_residual=float(abs(np.sum(weighted))/np.sum(abs(weighted)))))
    check('independent quadrature retains signed density and zero Killing energy',
          all(row['minimum']<0<row['maximum'] and row['relative_energy_residual']<1e-8 for row in numeric),numeric)

    ell, p = sp.symbols('ell p', positive=True)
    jumps = [sp.simplify(p*(x+ell)-p*x),sp.simplify(sp.exp(a*(x+ell))/sp.exp(a*x))]
    check('the affine cylinder cannot be periodically identified as this scalar/lapse background',
          jumps[0]==p*ell and sp.simplify(jumps[1]-sp.exp(a*ell))==0,
          dict(U_jump=str(jumps[0]),lapse_ratio=str(jumps[1]),
               general_obstruction='Every smooth real scalar U on a compact closed leaf attains extrema, where DU=0; the globally constant nonzero-gradient cylinder is outside that domain.'))

    failures=[row['name'] for row in checks if not row['passed']]
    result=dict(checks=checks,diagnostic_failures=failures,
        conclusion='The prescribed compact source is not a linear perturbation of the specified empty-particle, radial-electrovac background. The exact cylinder is not a background in the original compact-leaf domain.',
        scope='Positive-mass particle additions about zero particle density; linear spherical Maxwell; same exact background and original compact-domain specification. Differences about nonzero particle backgrounds, nonspherical matter, and full constrained retarded responses remain untested.',
        G03_status='OPEN',runtime_seconds=time.time()-start)
    output=HERE/'matter_admissibility_results.json'
    output.write_text(json.dumps(result,indent=2)+'\n')
    manifest=dict(schema_version=1,claim_id='C-H-cylinder-source-admissibility-obstructions',
        repository=dict(commit=subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip(),
                        dirty=bool(subprocess.check_output(['git','status','--porcelain'],text=True))),
        command='python3 '+str(Path(__file__).resolve().relative_to(ROOT)),
        environment=dict(software=['Python '+sys.version.split()[0],'SymPy '+sp.__version__,'NumPy '+np.__version__],hardware='CPU'),
        mathematics=dict(assertion_tested=result['conclusion'],coefficient_domain='exact symbolic',
            conventions='signature -+++; rho is orthonormal density; x is proper cylinder distance',
            inputs=[dict(path=str((HERE/name).relative_to(ROOT)),sha256=hashlib.sha256((HERE/name).read_bytes()).hexdigest())
                    for name in ('g03_matter_admissibility.py','ACTION.md','g03_retarded_screen.py')],
            bounds=dict(sector='linear spherical electric Maxwell, empty particle background, smooth compact spatial source',
                        quadrature_orders=[128,256,512],accelerations=[.5,2,4],bump_width=.45),
            non_claims=['full theory causal no-go','positive material realization of the external source','full matter initial-value uniqueness']),
        randomness=dict(used=False,generator='',seed=None),
        run=dict(started_at=time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime(start)),runtime_seconds=time.time()-start,exit_status=int(bool(failures))),
        outputs=[dict(path=str(output.relative_to(ROOT)),sha256=hashlib.sha256(output.read_bytes()).hexdigest())],
        checks=checks,result='PASS' if not failures else 'FAIL',residual_risks=[result['scope']])
    (HERE/'matter_admissibility_manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    print(f'{len(checks)-len(failures)}/{len(checks)} checks; full G03 remains OPEN')
    return int(bool(failures))


if __name__=='__main__':
    sys.exit(main())
