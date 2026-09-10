#!/usr/bin/env python3
"""Independent chain/connection tests for the general vacuum EF dictionary."""
import argparse
import importlib
import importlib.util
import json
from pathlib import Path
import unittest
import mpmath as mp
import sympy as s


def helper():
    try:
        return importlib.import_module('general_ef')
    except ModuleNotFoundError:
        raise AssertionError('general_ef helper has not been implemented')


def load_affine():
    path=Path(__file__).resolve().parents[2]/'kgb_mass_compatibility_2026/extension/ef_principal.py'
    spec=importlib.util.spec_from_file_location('independent_affine_dictionary_control',path)
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    return module


def canonical_inputs(C=mp.mpf('1.195'),C1=mp.mpf('.16'),C2=mp.mpf('.04'),Xr=-1):
    X=mp.mpf('1.5')
    bg=dict(r=mp.mpf(1),A=mp.mpf(1),B=mp.mpf(1),g=mp.mpf(0),BrB=mp.mpf(0),
        p=mp.mpf(1),pr=-mp.mpf(Xr),X=X,Xr=mp.mpf(Xr),C=C,C1=C1,q=mp.mpf(2))
    jet=dict(P=X*C,PX=C+X*C1,PXX=2*C1+X*C2,GX=mp.mpf(0),GXX=mp.mpf(0))
    return bg,jet,C2


class GeneralDictionaryTests(unittest.TestCase):
    def test_action_chain_rule_for_arbitrary_functions(self):
        x=s.Symbol('x',positive=True)
        C,P,G=[s.Function(name)(x) for name in ('C','P','G')]
        Dchi=lambda expression:s.diff(expression,x)/s.diff(x/C,x)
        a=helper().action_dictionary(x,C,s.diff(C,x),s.diff(C,x,2),
            P,s.diff(P,x),s.diff(P,x,2),s.diff(G,x),s.diff(G,x,2))
        expected=(P/C**2,Dchi(P/C**2),Dchi(Dchi(P/C**2)),
            s.diff(G,x)*C/(C-x*s.diff(C,x)),
            Dchi(s.diff(G,x)*C/(C-x*s.diff(C,x))))
        for key,value in zip(('P','P1','P2','G1','G2'),expected):
            self.assertEqual(s.factor(a[key]-value),0,key)

    def test_affine_action_limit(self):
        X,sigma,P,PX,PXX,GX,GXX=s.symbols('X sigma P PX PXX GX GXX')
        C=1+sigma*X
        a=helper().action_dictionary(X,C,sigma,0,P,PX,PXX,GX,GXX)
        expected=(PX-2*sigma*P/C,C*C*PXX-2*sigma*C*PX+2*sigma*sigma*P,
                  C*GX,C**3*GXX+sigma*C*C*GX)
        for key,value in zip(('P1','P2','G1','G2'),expected):
            self.assertEqual(s.factor(a[key]-value),0,key)

    def test_hessian_against_conformal_connection(self):
        r,A,B,C=s.symbols('r A B C',positive=True)
        g,b,p,pr,X,z,C1,q=s.symbols('g b p pr X z C1 q',real=True)
        out=helper().background_dictionary(r,A,B,g,b,p,pr,X,z,C,C1,q,sqrt=s.sqrt)
        h=C1*z/C;eta=s.diag(-1,1,1,1)
        v=s.Matrix([q/s.sqrt(A),p/s.sqrt(B),0,0])
        H=s.Matrix([[-g*p/B,-q*g/s.sqrt(A*B),0,0],
            [-q*g/s.sqrt(A*B),(pr-b*p/2)/B,0,0],
            [0,0,p/(B*r),0],[0,0,0,p/(B*r)]])
        k=s.Matrix([0,h/(2*s.sqrt(B)),0,0])
        transformed=(H-k*v.T-v*k.T+eta*(k.T*eta*v)[0])/C
        self.assertEqual(s.simplify(s.Matrix(out['H'])-transformed),s.zeros(4))

    def test_radial_hessian_cancels_second_background_derivatives(self):
        r,C,B=s.symbols('r C B',positive=True)
        p,pr,b,h,hp=s.symbols('p pr b h hp')
        D=1+r*h/2;Dp=h/2+r*hp/2
        pR=(pr-p*(h/2+Dp/D))/(C*D*D)
        bR=(b-2*Dp/D)/(s.sqrt(C)*D)
        H11=(pR-bR*p/(2*s.sqrt(C)*D))/(B/(D*D))
        self.assertEqual(s.factor(H11-(pr-(b+h)*p/2)/(C*B)),0)

    def test_nonaffine_canonical_EF_principal(self):
        with mp.workdps(70):
            bg,jet,C2=canonical_inputs(*map(mp.mpf,('1.195','.16','.04')))
            result=helper().evaluate(mp.mpf(1),bg,jet,C2)
            self.assertLess(max(abs(v) for v in result['principal']-mp.diag([1,-1,-1,-1])),mp.mpf('1e-60'))
            self.assertTrue(result['bounded_EF_static_quadratic_energy'])
            self.assertFalse(result['strict_EF_scalar_cone'])
            self.assertLess(result['relative_clock_norm_error'],mp.mpf('1e-60'))
            self.assertLess(result['relative_clock_derivative_error'],mp.mpf('1e-60'))

    def test_negative_field_jacobian_is_not_excluded(self):
        with mp.workdps(70):
            bg,jet,C2=canonical_inputs(*map(mp.mpf,('.5','.7','.04')),Xr=0)
            result=helper().evaluate(mp.mpf(1),bg,jet,C2)
            self.assertLess(result['action']['Dfield'],0)
            self.assertLess(max(abs(v) for v in result['principal']-mp.diag([1,-1,-1,-1])),mp.mpf('1e-60'))

    def test_singular_field_map_is_rejected(self):
        bg,jet,C2=canonical_inputs(C=mp.mpf(3),C1=mp.mpf(2))
        with self.assertRaises(ValueError):helper().evaluate(mp.mpf(1),bg,jet,C2)

    def test_affine_exact_halo_keeps_same_stress_and_principal(self):
        with mp.workdps(70):
            old=load_affine().mapped_halo_control(70)
            bg=dict(old['physical_input']);sigma=bg.pop('sigma')
            bg.update(C=1+sigma*bg['X'],C1=sigma)
            result=helper().evaluate(mp.mpf(1),bg,old['physical_action_jet'],mp.mpf(0))
            for key in ('stress','principal'):
                self.assertLess(max(abs(v) for v in result[key]-old[key]),mp.mpf('1e-60'))
            self.assertTrue(result['strict_EF_scalar_cone'])

    def test_third_C_jet_absent_but_second_C_jet_effective(self):
        x=s.Symbol('x');x0=s.Rational(3,2)
        polynomials=[1+x/10+x*x/50+k*(x-x0)**3 for k in (0,7)]
        with mp.workdps(70):
            bg,jet,_=canonical_inputs(*map(mp.mpf,('1.195','.16','.04')))
            jet.update(P=mp.mpf('.7'),PX=mp.mpf('1.3'),PXX=mp.mpf('.2'),GX=mp.mpf('.1'),GXX=mp.mpf('.3'))
            outputs=[]
            for poly in polynomials:
                C,C1,C2=[mp.mpf(str(s.N(s.diff(poly,x,n).subs(x,x0),70))) for n in range(3)]
                inputs=dict(bg,C=C,C1=C1)
                outputs.append(helper().evaluate(mp.mpf(1),inputs,jet,C2))
            self.assertNotEqual(s.diff(polynomials[0],x,3),s.diff(polynomials[1],x,3))
            self.assertEqual(outputs[0]['principal'],outputs[1]['principal'])
            changed=helper().evaluate(mp.mpf(1),bg,jet,mp.mpf('.08'))
            self.assertGreater(max(abs(v) for v in changed['principal']-outputs[0]['principal']),mp.mpf('.01'))

    def test_conditional_inverse_curvature_variation(self):
        X,C,C1,j,P,PX,PXX,GX,GXX=s.symbols('X C C1 j P PX PXX GX GXX',nonzero=True)
        a=helper().action_dictionary(X,C,C1,2*j,P,PX,PXX,GX,GXX)
        # Conditional input from the separate inverse derivation: f=C1/2,
        # dPXX/dj=PX/f and dGXX/dj=GX/f; lower physical jets are held fixed.
        Dj=lambda e:s.diff(e,j)+2*PX/C1*s.diff(e,PXX)+2*GX/C1*s.diff(e,GXX)
        factor=2*C**3/(C1*(C-X*C1)**2)
        self.assertEqual(s.factor(Dj(a['P2'])-factor*a['P1']),0)
        self.assertEqual(s.factor(Dj(a['G2'])-factor*a['G1']),0)


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--result-file',type=Path)
    args=parser.parse_args()
    result=unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(GeneralDictionaryTests))
    evidence=dict(tests=result.testsRun,failures=len(result.failures),errors=len(result.errors),passed=result.wasSuccessful())
    if result.wasSuccessful():
        with mp.workdps(70):
            bg,jet,C2=canonical_inputs(*map(mp.mpf,('1.195','.16','.04')))
            evidence['canonical_nonaffine']=helper().serial(helper().evaluate(mp.mpf(1),bg,jet,C2))
    output=json.dumps(evidence,indent=2)+'\n'
    if args.result_file:args.result_file.write_text(output)
    else:print(output)
    return 0 if result.wasSuccessful() else 1


if __name__=='__main__':raise SystemExit(main())
