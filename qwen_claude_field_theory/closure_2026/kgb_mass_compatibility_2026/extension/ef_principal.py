#!/usr/bin/env python3
"""Affine conformal Einstein-frame scalar-principal dictionary and controls.

The existing KGB principal is applicable in the vacuum exterior Einstein frame.
The physical matter coupling must be transformed when matter is present.
An EF static quadratic-energy check is not a full Jordan-frame Hamiltonian proof.
"""
import argparse
from functools import lru_cache
import importlib.util
import json
from pathlib import Path
import unittest
import mpmath as mp
import sympy as s

SOURCE = Path(__file__).resolve().parents[2]/'ticking_kgb_inverse_2026/kgb_inverse.py'


def action_dictionary(X,sigma,P,PX,PXX,GX,GXX):
    C = 1+sigma*X
    return dict(C=C,chi=X/C,P=P/C**2,P1=PX-2*sigma*P/C,
        P2=C**2*PXX-2*sigma*C*PX+2*sigma**2*P,
        G1=C*GX,G2=C**3*GXX+sigma*C**2*GX)


def background_dictionary(r,A,B,g,BrB,p,pr,X,Xr,sigma,q=-1,sqrt=mp.sqrt):
    """pr=dp/dr; BrB=B'/B. Requires C>0,D>0 and coherent scalar X.

    Only X' is needed for the EF Hessian; all X''/D' terms cancel.
    sqrt may be sympy.sqrt for exact symbolic evaluation.
    """
    C = 1+sigma*X
    h = sigma*Xr/C
    D = 1+r*h/2
    omega = sqrt(C)
    v = [q/sqrt(C*A),p/sqrt(C*B),0,0]
    H00 = -(g+h/2)*p/(C*B)
    H01 = -q*(g+h/2)/(C*sqrt(A*B))
    H11 = (pr-(BrB+h)*p/2)/(C*B)
    H22 = p*D/(C*B*r)
    H = [[H00,H01,0,0],[H01,H11,0,0],[0,0,H22,0],[0,0,0,H22]]
    return dict(C=C,h=h,D=D,R=omega*r,A=C*A,B=B/D**2,
        g=(g+h/2)/(omega*D),p=p/(omega*D),chi=X/C,v=v,H=H)


@lru_cache(None)
def evaluator():
    spec = importlib.util.spec_from_file_location('ef_dictionary_kgb_source',SOURCE)
    model = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(model)
    a = model.principal_template()
    args = [a['m'],a['G1'],a['G2'],a['P'],a['P1'],a['P2']]
    args += list(a['v'])+[a['H'][i,j] for i in range(4) for j in range(i,4)]
    return s.lambdify(args,(a['M'],a['T']),'mpmath',cse=True)


def evaluate(m,background,physical_jet):
    """Return the actual original KGB principal/stress after frame conversion.

    Input dictionaries follow the argument names of background_dictionary and
    action_dictionary; background must include X and sigma. Use mpmath inputs
    and a workdps context when high precision is needed.
    """
    bg = background_dictionary(**background)
    if bg['C']<=0 or bg['D']<=0 or bg['chi']<=0:
        raise ValueError('outside positive invertible timelike orientation chart')
    q = background.get('q',-1)
    norm_X = (q*q/background['A']-background['p']**2/background['B'])/2
    expected_Xr = (-q*q*background['g']/background['A']
        -background['p']*background['pr']/background['B']
        +background['p']**2*background['BrB']/(2*background['B']))
    norm_error = abs(norm_X-background['X'])/abs(background['X'])
    derivative_error = abs(expected_Xr-background['Xr'])/max(
        abs(expected_Xr),abs(background['Xr']),mp.mpf('1e-100'))
    a = action_dictionary(background['X'],background['sigma'],**physical_jet)
    principal,stress = evaluator()(m,a['G1'],a['G2'],a['P'],a['P1'],a['P2'],
        *bg['v'],*[bg['H'][i][j] for i in range(4) for j in range(i,4)])
    K,cross,radial,angular = principal[0,0],principal[0,1],principal[1,1],principal[2,2]
    points = [mp.mpf(0),mp.mpf(1)]
    if radial>angular:
        t = abs(cross)/(radial-angular)
        if 0<t<1:points.append(t)
    margin = min(K+angular-2*abs(cross)*t+(radial-angular)*t*t for t in points)
    bounded = bool(K>0 and radial<0 and angular<0)
    return dict(background=bg,action=a,principal=principal,stress=stress,
        kinetic=K,cross=cross,radial=radial,angular=angular,
        radial_discriminant=cross**2-K*radial,light_margin=margin,
        relative_clock_norm_error=norm_error,relative_clock_derivative_error=derivative_error,
        bounded_EF_static_quadratic_energy=bounded,
        strict_EF_scalar_cone=bool(bounded and K>abs(cross) and margin>0))


@lru_cache(None)
def symbolic_checks():
    X,sigma,P,PX,PXX,GX,GXX = s.symbols('X sigma P PX PXX GX GXX',real=True)
    C = 1+sigma*X
    DX = lambda e:s.diff(e,X)+s.diff(e,P)*PX+s.diff(e,PX)*PXX+s.diff(e,GX)*GXX
    a = action_dictionary(X,sigma,P,PX,PXX,GX,GXX)
    r,A,B,p = s.symbols('r A B p',positive=True)
    g,BrB,pr,h,hp,q = s.symbols('g BrB pr h hp q',real=True)
    D = 1+r*h/2
    Dp = h/2+r*hp/2
    # Transform coordinate derivatives before assembling the EF Hessian.
    transformed_pr = (pr-p*(h/2+Dp/D))/(C*D**2)
    transformed_BrB = (BrB-2*Dp/D)/(s.sqrt(C)*D)
    radial_H = (transformed_pr-transformed_BrB*p/(2*s.sqrt(C)*D))/(B/D**2)
    b = background_dictionary(r,A,B,g,BrB,p,pr,X,h*C/sigma,sigma,q,sqrt=s.sqrt)
    eta = s.diag(-1,1,1,1)
    oldv = s.Matrix([q/s.sqrt(A),p/s.sqrt(B),0,0])
    oldH = s.Matrix([[-g*p/B,-q*g/s.sqrt(A*B),0,0],
        [-q*g/s.sqrt(A*B),(pr-BrB*p/2)/B,0,0],
        [0,0,p/(B*r),0],[0,0,0,p/(B*r)]])
    k = s.Matrix([0,h/(2*s.sqrt(B)),0,0])  # covector grad(log Omega).
    conformalH = (oldH-k*oldv.T-oldv*k.T+eta*(k.T*eta*oldv)[0])/C
    Hres = s.Matrix(b['H'])-conformalH
    return dict(action=a,radial_hessian_after_derivative_cancellation=s.factor(radial_H),
        residuals=[s.factor(C**2*DX(a['P'])-a['P1']),
            s.factor(C**2*DX(a['P1'])-a['P2']),
            s.factor(C**2*DX(a['G1'])-a['G2']),
            s.factor(radial_H-(pr-p*(BrB+h)/2)/(C*B)),
            *[s.factor(e) for e in Hres]])


def mpvalue(v):
    return mp.mpf(str(s.N(v,mp.mp.dps)))


@lru_cache(None)
def mapped_halo_control(dps=60):
    """Map one exact source KGB flat-force halo; this is not the MOND target."""
    with mp.workdps(dps):
        R = s.Symbol('R',positive=True)
        w,sigma,m = s.Rational(1,100),s.Rational(1,10),s.Integer(1)
        At,Bt = R**(2*w),1+2*w
        chi = 1/(At*(2+w))
        pt = s.sqrt(Bt*w*chi)
        rho = 2*m*w/(Bt*R**2)
        G1 = s.factor(pt*rho/(2*chi*s.diff(chi,R)))
        G2 = s.factor(s.diff(G1,R)/s.diff(chi,R))
        C = 1/(1-sigma*chi)
        X = C*chi
        r = R/s.sqrt(C)
        rR = s.diff(r,R)
        A = At/C
        B = Bt/(C*rR**2)
        p = pt/rR
        physical = dict(r=r,A=A,B=B,g=s.diff(A,R)/(2*A*rR),
            BrB=s.diff(B,R)/(B*rR),p=p,pr=s.diff(p,R)/rR,X=X,
            Xr=s.diff(X,R)/rR,sigma=sigma,q=-s.Integer(1))
        GX = G1/C
        GXX = (G2-sigma*C**2*GX)/C**3
        jet = dict(P=s.Integer(0),PX=s.Integer(0),PXX=s.Integer(0),GX=GX,GXX=GXX)
        physical = {k:mpvalue(v.subs(R,1)) for k,v in physical.items()}
        jet = {k:mpvalue(v.subs(R,1)) for k,v in jet.items()}
        result = evaluate(mpvalue(m),physical,jet)
        expected_stress = mp.matrix([[mpvalue(rho.subs(R,1)),0,0,0],
            [0,0,0,0],[0,0,mpvalue(m*w*w/Bt),0],[0,0,0,mpvalue(m*w*w/Bt)]])
        error = max(abs(e) for e in result['stress']-expected_stress)/abs(expected_stress[0,0])
        result.update(dps=dps,physical_input=physical,physical_action_jet=jet,
            relative_EF_Einstein_stress_error=error,
            expected_EF_G1=mpvalue(G1.subs(R,1)),expected_EF_G2=mpvalue(G2.subs(R,1)),
            scope='One mapped exact flat-force source halo at R=1,w=0.01; not a universal mass law or exponential MOND profile.')
        return result


class DictionaryTests(unittest.TestCase):
    def test_symbolic_action_and_hessian_dictionary(self):
        self.assertEqual(symbolic_checks()['residuals'],[0]*20)

    def test_canonical_EF_action_control(self):
        X,sigma = s.symbols('X sigma',positive=True)
        a = action_dictionary(X,sigma,X*(1+sigma*X),1+2*sigma*X,2*sigma,0,0)
        self.assertEqual(s.factor(a['P1']),1)
        self.assertEqual(s.factor(a['P2']),0)

    def test_mapped_halo_metric_recovered(self):
        a = mapped_halo_control()
        with mp.workdps(60):
            self.assertLess(abs(a['background']['R']-1),mp.mpf('1e-50'))
            self.assertLess(abs(a['background']['A']-1),mp.mpf('1e-50'))
            self.assertLess(abs(a['background']['B']-mp.mpf('1.02')),mp.mpf('1e-50'))

    def test_mapped_halo_action_and_stress_recovered(self):
        a = mapped_halo_control()
        with mp.workdps(60):
            self.assertLess(abs(a['action']['G1']/a['expected_EF_G1']-1),mp.mpf('1e-50'))
            self.assertLess(abs(a['action']['G2']/a['expected_EF_G2']-1),mp.mpf('1e-50'))
            self.assertLess(a['relative_EF_Einstein_stress_error'],mp.mpf('1e-50'))
            self.assertLess(a['relative_clock_norm_error'],mp.mpf('1e-50'))
            self.assertLess(a['relative_clock_derivative_error'],mp.mpf('1e-50'))

    def test_canonical_actual_principal_and_non_strict_light_cone(self):
        with mp.workdps(60):
            bg = dict(zip(('r','A','B','g','BrB','p','pr','X','Xr','sigma','q'),
                          map(mp.mpf,('1','1','1','0','0','1','1','1.5','-1','.1','2'))))
            jet = dict(zip(('P','PX','PXX','GX','GXX'),map(mp.mpf,('1.725','1.3','.2','0','0'))))
            a = evaluate(mp.mpf(1),bg,jet)
            self.assertLess(max(abs(v) for v in a['principal']-mp.diag([1,-1,-1,-1])),mp.mpf('1e-50'))
            self.assertTrue(a['bounded_EF_static_quadratic_energy'])
            self.assertFalse(a['strict_EF_scalar_cone'])


def serial(a):
    if isinstance(a,dict):return {k:serial(v) for k,v in a.items()}
    if isinstance(a,(list,tuple)):return [serial(v) for v in a]
    if isinstance(a,mp.matrix):return [[serial(a[i,j]) for j in range(a.cols)] for i in range(a.rows)]
    if isinstance(a,(bool,int,str)):return a
    if isinstance(a,s.Basic):return str(a)
    return mp.nstr(a,45)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--result-file',type=Path)
    args = parser.parse_args()
    tests = unittest.TextTestRunner(verbosity=2).run(
        unittest.defaultTestLoader.loadTestsFromTestCase(DictionaryTests))
    result = serial(dict(symbolic=symbolic_checks(),mapped_halo=mapped_halo_control(),
        tests=dict(run=tests.testsRun,failures=len(tests.failures),errors=len(tests.errors),passed=tests.wasSuccessful())))
    output = json.dumps(result,indent=2)+'\n'
    if args.result_file:args.result_file.write_text(output)
    else:print(output)
    return 0 if tests.wasSuccessful() else 1


if __name__=='__main__':raise SystemExit(main())
