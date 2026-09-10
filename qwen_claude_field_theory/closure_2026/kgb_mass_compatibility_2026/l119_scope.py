#!/usr/bin/env python3
"""Executable counterexamples to inference shortcuts in concurrent L119.

This does NOT refute every elliptic MOND construction. It tests the actual
implications used to label that architecture healthy before Dirac closure.
"""
import json
import unittest
import sympy as s


def multiplier_counterexample():
    q,N,p,pN,u,dq,dN=s.symbols('q N p pN u dq dN',real=True)
    lagrangian=dq**2/2-N*q
    H=p*p/2+N*q+u*pN
    pairs=((q,p),(N,pN))
    def pb(a,b):return s.expand(sum(s.diff(a,x)*s.diff(b,y)-s.diff(a,y)*s.diff(b,x) for x,y in pairs))
    constraints=[pN];preservations=[];fixed={}
    for _ in range(8):
        expression=pb(constraints[-1],H)
        preservations.append(expression)
        if expression.has(u):
            fixed=s.solve(expression,u,dict=True)[0];break
        poly=s.Poly(expression,q,N,p,pN)
        constraint=s.expand(expression/poly.LC())
        constraints.append(constraint)
    matrix=s.Matrix([[pb(a,b) for b in constraints] for a in constraints])
    rank=matrix.rank();first=len(constraints)-rank;second=rank
    # This finite-dimensional example has no additional reducibility or gauges.
    dof=len(pairs)-first-s.Rational(second,2)
    closed=[s.expand(pb(a,H.subs(fixed))).subs(dict.fromkeys((q,N,p,pN),0)) for a in constraints]
    return dict(lagrangian=lagrangian,lapse_velocity_hessian=s.diff(lagrangian,dN,2),
        lapse_hessian=s.diff(lagrangian,N,2),constraints=constraints,
        preservation=preservations,multiplier=fixed,matrix=matrix,det=matrix.det(),
        rank=rank,first_class=first,second_class=second,dof=dof,closure=closed)


def hda_product():
    p,ss,g,m=s.symbols('p ss g m',positive=True)
    w=s.Function('W');F=s.sqrt((p*p-m*g)*g*ss*ss)
    H=F+w(g*ss*ss)
    residual=s.simplify(s.diff(H,p)*s.diff(H,ss)-g*p*ss)
    # Nonconstant smooth W(z)=z; real domain p^2>mg.
    witness=s.simplify((s.diff(F+g*ss*ss,p)*s.diff(F+g*ss*ss,ss)-g*p*ss).subs({p:2,ss:1,g:1,m:1}))
    return dict(same_momentum_derivative=s.simplify(s.diff(H,p)-s.diff(F,p)),
                full_product_residual=residual,witness=witness)


class ScopeTests(unittest.TestCase):
    def test_linear_multiplier_is_not_necessarily_first_class(self):
        a=multiplier_counterexample()
        self.assertEqual(a['lapse_hessian'],0)
        self.assertEqual(a['lapse_velocity_hessian'],0)
        self.assertNotEqual(a['det'],0)

    def test_actual_preservation_closes_after_multiplier_fixed(self):
        a=multiplier_counterexample()
        self.assertTrue(a['multiplier'])
        self.assertTrue(all(e==0 for e in a['closure']))
        self.assertEqual(a['matrix']+a['matrix'].T,s.zeros(len(a['constraints'])))

    def test_unchanged_momentum_derivative_does_not_prove_hda(self):
        a=hda_product()
        self.assertEqual(a['same_momentum_derivative'],0)
        self.assertNotEqual(a['full_product_residual'],0)
        self.assertTrue(a['witness']>0)


def main():
    run=unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(ScopeTests))
    example=multiplier_counterexample()
    example['multiplier']={str(k):v for k,v in example['multiplier'].items()}
    print('L119_SCOPE='+json.dumps(dict(multiplier=example,hda=hda_product(),
        verdict='L119 displayed derivative checks do not certify health or first-class closure; elliptic architecture remains open'),default=str))
    return 0 if run.wasSuccessful() else 1


if __name__=='__main__':raise SystemExit(main())
