#!/usr/bin/env python3
"""Derivative checks independent of the new symbolic implementation."""
from pathlib import Path
import sys
import unittest
import mpmath as mp
import numpy as np

HERE=Path(__file__).resolve().parent
CLOSURE=HERE.parents[1]
REFERENCE=CLOSURE/'kgb_universal_clock_2026'/'structure'
sys.path.insert(0,str(REFERENCE))
import check_next_preservation as reference


class FastDerivatives(unittest.TestCase):
    def evaluator(self):
        # Catches a missing implementation without hiding an import error.
        self.assertTrue((HERE/'fast.py').is_file(),'fast analytic evaluator has not been implemented')
        import fast
        return fast.single

    def test_analytic_partials_match_independent_60_digit_reference(self):
        single=self.evaluator()
        cases=[('1e-6','.1','.5','3e-8','-20.8245196960960745','.525','259.6853685595673'),
               ('2e-6','.153793693461797103','.5','5.20116491998896476e-8','-27.4430902101841915','.525','259.6853685595673'),
               ('2e-6','.3','.7','1e-7','.12','.8','-.07'),
               ('4e-6','2','.4','.002','-.2','.9','.08'),
               ('1e-3','.8','.5','.5','.7','1.2','.2')]
        for strings in cases:
            with self.subTest(point=strings),mp.workdps(60):
                eps,y,X,U,w,F,f=map(mp.mpf,strings)
                old,A,B,N=reference.next_parts(eps,(X,F,y,U,w),f)
                actual=single(*map(float,strings))
                for key,want in (('A',A),('B',B),('N',N)):
                    np.testing.assert_allclose(actual[key],list(map(float,want)),rtol=2e-10,atol=1e-12)
                np.testing.assert_allclose([actual[k] for k in ('P','H','K','Gamma')],
                                          [float(old[k]) for k in ('P','H','kappa','gamma')],rtol=2e-12)

    def test_prior_pair_next_determinant_at_60_and_80_digits(self):
        single=self.evaluator()
        for precision in (60,80):
            out=reference.check(precision)
            w1,w2,y2,u2,f=map(float,out['seed'])
            first=single(1e-6,.1,.5,3e-8,w1,.525,f)
            second=single(2e-6,y2,.5,2e-6*u2,w2,.525,f)
            B=first['B']-second['B'];N=first['N']-second['N']
            determinant=N[0]*B[1]-N[1]*B[0]
            normalized=determinant/(np.linalg.norm(N)*np.linalg.norm(B))
            np.testing.assert_allclose(normalized,float(out['normalized_next_determinant']),rtol=2e-9)

    def test_N_is_derivative_of_original_raw_action_curvatures(self):
        # Omitting differentiation of the changing inner vector field fails this.
        single=self.evaluator()
        sys.path.insert(0,str(CLOSURE/'kgb_nonaffine_clock_2026'))
        import nonaffine_inverse as original
        cases=[(1e-6,.1,.5,3e-8,-20.8245196960960745,.525,259.6853685595673),
               (2e-6,.153793693461797103,.5,5.20116491998896476e-8,-27.4430902101841915,.525,259.6853685595673),
               (1e-3,.8,.5,.5,.7,1.2,.2)]
        for eps,y,X,U,w,F,f in cases:
            with self.subTest(eps=eps,y=y):
                row=single(eps,y,X,U,w,F,f);geo=row['geometry']
                point=np.array([y,X,U,w,F])
                direction=np.array([f/(geo['ry']*w),1.,-2-2*f*geo['g']*(2*X+U)/w,f*row['W']/w,f])
                base=1e-3*min(abs(v/d) for v,d in zip(point,direction) if d!=0)
                def raw(curve_point):
                    yy,xx,uu,ww,ff=curve_point
                    _,pxx,gxx=original.action_curvatures(eps,yy,xx,uu,ww/f,F0=ff,f0=f,j0=0.,X0=xx)
                    return np.array([pxx,gxx])/f
                errors=[]
                for factor in (3.,1.,.3,.1):
                    h=base*factor
                    estimate=(raw(point+h*direction)-raw(point-h*direction))/(2*h)
                    errors.append(np.max(np.abs(estimate-row['N']))/max(np.max(np.abs(row['N'])),1.))
                print('RAW_CURVATURE_PLATEAU',eps,y,base,errors)
                self.assertTrue(any(max(pair)<1e-5 for pair in zip(errors,errors[1:])),errors)

    def test_complex_step_first_preservation_includes_shared_f_flow(self):
        # Catches loss of complex values or failure to include Df=j in E.
        single=self.evaluator()
        eps=1e-3;point=np.array([.8,.5,.5,.7,1.2,.2]);j=-.3
        row=single(eps,*point);geo=row['geometry'];y,X,U,w,F,f=point
        direction=np.array([f/(geo['ry']*w),1.,-2-2*f*geo['g']*(2*X+U)/w,f*row['W']/w,f,j])
        shifted=single(eps,*(point+1e-25j*direction))
        got=np.imag(shifted['A']+(f+1e-25j*j)*shifted['B'])/1e-25
        np.testing.assert_allclose(got,row['N']+j*row['B'],rtol=2e-12,atol=1e-9)


if __name__=='__main__':unittest.main(verbosity=2)
