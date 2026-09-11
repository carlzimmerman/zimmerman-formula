#!/usr/bin/env python3
import unittest
import numpy as np
import evolve


class LapseOperator(unittest.TestCase):
    def test_matches_polynomial_and_the_evolution_derivatives(self):
        self.assertTrue(hasattr(evolve,'solve_lapse'),'compatible lapse operator missing')
        r=np.linspace(0,1,65);dr=r[1]
        exact=1+.01*(r*r-1)+.003*(r**4-1)
        a=np.divide(-2,r,out=np.zeros_like(r),where=r>0);b=np.full_like(r,.7)
        source=.06+.06*r*r-b*exact
        got=evolve.solve_lapse(r,a,b,source,b[0]/3,source[0]/3)
        np.testing.assert_allclose(got,exact,rtol=0,atol=2e-11)
        first,second=evolve.derivatives(got,dr)
        residual=second-a*first-b*got-source
        self.assertLess(max(abs(residual[1:-1])),2e-10)

    def test_nonpolynomial_boundary_solution_refines_at_fourth_order(self):
        errors=[]
        for size in (33,65):
            r=np.linspace(0,1,size);e=np.exp(-r*r)
            exact=1+.01*(e-np.exp(-1.))
            first=-.02*r*e;second=.01*(4*r*r-2)*e
            a=np.divide(-2,r,out=np.zeros_like(r),where=r>0)+.1*r
            b=.7+.01*r*r;source=second-a*first-b*exact
            source[0]=-.06-b[0]*exact[0]
            got=evolve.solve_lapse(r,a,b,source,b[0]/3,source[0]/3)
            errors.append(float(max(abs(got-exact))))
        self.assertLess(errors[1],errors[0]/8,errors)


if __name__=='__main__':unittest.main(verbosity=2)
