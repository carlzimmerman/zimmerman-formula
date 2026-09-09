"""Initial-data-only derivative control; never used for evolved fields.

Compares IC47 with analytic derivatives of its stored Taylor polynomials.
Also differentiates the float samples at 70 digits to separate sampling
error from differentiation arithmetic. This is not a high-precision solve.
"""
import json
import mpmath as mp
import numpy as np
import ic46_centered_evolution as centered
from ic47_jacobian_evolution import fixed_jacobian


class InitialControl(centered.Evolution):
    def derivative(self, side, value, order=1):
        if hasattr(self, 'initial'):
            fields, _ = self.fields(self.initial)
            for index, row in ((0,2),(1,6),(2,4)):
                if np.array_equal(value, fields[side,index]):
                    coefficients=np.polynomial.polynomial.polyder(self.coeff[row],order)
                    return self.poly(coefficients,self.offset[side])
        return super().derivative(side,value,order)


def sampling_error(e):
    records=[]
    with mp.workdps(70):
        for side in (0,1):
            x=[mp.mpf(float(v)) for v in e.offset[side]]
            n=len(x)
            weights=[1/mp.fprod(x[i]-x[j] for j in range(n) if j!=i) for i in range(n)]
            D=mp.matrix(n)
            for i in range(n):
                for j in range(n):
                    if i!=j:D[i,j]=weights[j]/weights[i]/(x[i]-x[j])
                D[i,i]=-sum(D[i,j] for j in range(n) if i!=j)
            coeff=e.coeff[2]
            samples=mp.matrix([mp.mpf(float(v)) for v in e.poly(coeff,e.offset[side])])
            exact_samples=mp.matrix([mp.polyval([mp.mpf(float(v)) for v in coeff[::-1]],v) for v in x])
            dd=np.polynomial.polynomial.polyder(coeff,2)
            truth=mp.matrix([mp.polyval([mp.mpf(float(v)) for v in dd[::-1]],v) for v in x])
            for label, values in [('float_samples',samples),('polynomial_samples_70_digits',exact_samples)]:
                error=D*D*values-truth
                records.append(dict(side=side,data=label,max_second_derivative_error=float(max(abs(v) for v in error))))
    return records


def main():
    rows=[]
    for nodes in (7,9):
        for cls in (centered.Evolution,InitialControl):
            e=cls(nodes=nodes)
            with fixed_jacobian(1e-8):
                _,diagnostic=e.rhs(e.initial.copy(),0.)
            rows.append(dict(nodes=nodes,control=cls.__name__,diagnostic=diagnostic,
                             sampling=sampling_error(e)))
    print(json.dumps(dict(full_theory='OPEN',scope='Initial slice only; polynomial derivative oracle cannot evolve unknown data',runs=rows),indent=2))


if __name__=='__main__':main()
