#!/usr/bin/env python3
"""Exact auxiliary-field and static-component checks for F(X) R + K(X)(dX)^2.

These checks establish variation identities, not degeneracy, health, or PPN.
No old zero-KGB-current substitution is used: the total current is set to zero.
"""
from functools import lru_cache
import unittest
import sympy as s


@lru_cache(None)
def component_data():
    A, B, r, X = s.symbols("A B r X", positive=True)
    q, p = s.symbols("q p", nonzero=True)
    F, Fx, Fxx, K, Echi, P, PX, GX, boxphi = s.symbols("F Fx Fxx K Echi P PX GX boxphi")
    g, b, xr, xrr, rho, pr, pt = s.symbols("g b xr xrr rho pr pt")
    # b=B'/(2B). Equatorial coordinate components suffice for spherical tensors.
    metric = s.diag(-A, B, r**2, r**2)
    einstein = s.diag(A*rho, B*pr, r**2*pt, r**2*pt)
    clock, dx = s.Matrix([q, p, 0, 0]), s.Matrix([0, xr, 0, 0])
    Fr, Frr = Fx*xr, Fx*xrr+Fxx*xr**2
    hessianF = s.diag(-A*g*Fr/B, Frr-b*Fr, r*Fr/B, r*Fr/B)
    boxF = (Frr+(g-b+2/r)*Fr)/B
    derivative_norm = xr**2/B
    Egrav = (F*einstein+metric*boxF-hessianF+K*dx*dx.T
             - metric*K*derivative_norm/2-Echi*clock*clock.T/2)
    stress = ((PX-GX*boxphi)*clock*clock.T+P*metric
              -GX*(dx*clock.T+clock*dx.T)+metric*GX*p*xr/B)
    Etotal = Egrav-stress/2
    current = ((PX+Echi-GX*boxphi)*p-GX*xr)/B
    zero_current = {PX: GX*boxphi+GX*xr/p-Echi}
    solved = Etotal.subs(zero_current).subs(q**2, A*(2*X+p**2/B)).applyfunc(s.factor)
    density = 2*(Fx*xrr+(Fxx-K/2)*xr**2+(2/r-b)*Fx*xr)/B+2*X*GX*xr/p-P
    radial = P-2*(g+2/r)*Fx*xr/B-K*xr**2/B
    angular = P+GX*p*xr/B-2*(boxF-Fr/(B*r))+K*xr**2/B
    return locals()


class DerivativeCurvatureVariation(unittest.TestCase):
    def test_auxiliary_chi_euler_lagrange(self):
        Fx, K, Kx, R, xr, xrr, B, g, b, r = s.symbols("Fx K Kx R xr xrr B g b r", nonzero=True)
        # measure'/measure=g+b+2/r; derivative of 2K*chi'/B is explicit.
        derivative_momentum = (g+b+2/r)*2*K*xr/B + 2*Kx*xr**2/B + 2*K*xrr/B-4*K*xr*b/B
        euler = Fx*R+Kx*xr**2/B-derivative_momentum
        boxX = (xrr+(g-b+2/r)*xr)/B
        self.assertEqual(s.factor(euler-(Fx*R-Kx*xr**2/B-2*K*boxX)), 0)

    def test_auxiliary_metric_chain_and_scalar_current_sign(self):
        lam = s.symbols("lam")
        v = s.Matrix(s.symbols("v0:4"))
        inverse = s.Matrix(4, 4, lambda i, j: s.Symbol("ginv%d%d" % (i, j)))
        X = -(v.T*inverse*v)[0]/2
        for i in range(4):
            for j in range(4):
                self.assertEqual(s.diff(lam*X, inverse[i, j]), -lam*v[i]*v[j]/2)
        A, B, q, p = s.symbols("A B q p", nonzero=True)
        staticX = q*q/(2*A)-p*p/(2*B)
        self.assertEqual(-s.diff(lam*staticX, p), lam*p/B)

    def test_static_F_hessian_directly_from_connection(self):
        t, r, theta, phi = s.symbols("t r theta phi", real=True)
        A, B, F = s.Function("A")(r), s.Function("B")(r), s.Function("F")(r)
        coords = [t, r, theta, phi]
        metric = s.diag(-A, B, r**2, r**2*s.sin(theta)**2)
        inverse = metric.inv()
        hessian = s.zeros(4)
        for i in range(4):
            for j in range(4):
                gamma_r = sum(inverse[1, k]*(s.diff(metric[k, i], coords[j])
                            +s.diff(metric[k, j], coords[i])-s.diff(metric[i, j], coords[k]))
                            for k in range(4))/2
                hessian[i, j] = s.diff(F, coords[i], coords[j])-gamma_r*s.diff(F, r)
        expected = s.diag(-s.diff(A,r)*s.diff(F,r)/(2*B),
                          s.diff(F,r,2)-s.diff(B,r)*s.diff(F,r)/(2*B),
                          r*s.diff(F,r)/B, r*s.sin(theta)**2*s.diff(F,r)/B)
        self.assertTrue(all(s.simplify(e)==0 for e in hessian-expected))

    def test_mixed_equation_uses_the_total_current(self):
        d = component_data()
        residual = d["Etotal"][1,0]/d["B"]+d["q"]*d["current"]/2
        self.assertEqual(s.factor(residual), 0)

    def test_density_radial_angular_equations_on_total_zero_current(self):
        d = component_data()
        for index, scale, geo, rhs in ((0,d["A"],d["rho"],d["density"]),
                                      (1,d["B"],d["pr"],d["radial"]),
                                      (2,d["r"]**2,d["pt"],d["angular"])):
            self.assertEqual(s.factor(2*d["solved"][index,index]/scale-(2*d["F"]*geo-rhs)),0)

    def test_constant_F_recovers_the_original_zero_current_equations(self):
        d=component_data()
        constant={d["Fx"]:0,d["Fxx"]:0,d["K"]:0}
        expected=[2*d["X"]*d["GX"]*d["xr"]/d["p"]-d["P"],
                  d["P"],d["P"]+d["GX"]*d["p"]*d["xr"]/d["B"]]
        for name,target in zip(("density","radial","angular"),expected):
            self.assertEqual(s.factor(d[name].subs(constant)-target),0)

    def test_radial_B_elimination_and_highest_derivative_determinant(self):
        d=component_data()
        F,Fx,K,g,r,B,xr,xrr,P=[d[k] for k in ("F","Fx","K","g","r","B","xr","xrr","P")]
        Br=s.symbols("Br")
        geom_pr=(1/B-1)/r**2+2*g/(B*r)
        Bsolution=(2*F*(1+2*r*g)+2*r*r*(g+2/r)*Fx*xr+r*r*K*xr*xr)/(2*F+r*r*P)
        self.assertEqual(s.factor((2*F*geom_pr-d["radial"]).subs(B,Bsolution)),0)
        gr=s.symbols("gr")
        density_eq=B*(2*F*((1-1/B)/r**2+Br/(B*B*r))-d["density"])
        angular_eq=B*(2*F*(gr+g*g-g*Br/(2*B)+(g-Br/(2*B))/r)/B-d["angular"])
        equations=[s.expand(e.subs(d["b"],Br/(2*B))) for e in (density_eq,angular_eq)]
        coefficients=s.Matrix([[s.diff(e,z) for z in (Br,xrr)] for e in equations])
        self.assertEqual(s.factor(coefficients.det()-2*F*Fx*(1/r-g)/B),0)
        summed=s.factor(sum(equations))
        for term in (xrr,d["Fxx"],K):
            self.assertEqual(s.diff(summed,term),0)
        expected_sum=((1/r-g)*(F*Br/B-2*Fx*xr)
                      +2*F*((B-1)/r**2+gr+g*g+g/r)
                      -d["GX"]*xr*(2*B*d["X"]/d["p"]+d["p"]))
        self.assertEqual(s.factor(summed-expected_sum),0)

    def test_linear_F_auxiliary_equation(self):
        X,F0,alpha,R,norm,boxX=s.symbols("X F0 alpha R norm boxX")
        F=F0+alpha*X
        K=3*alpha**2/(2*F)
        Echi=alpha*R-s.diff(K,X)*norm-2*K*boxX
        expected=alpha*R+3*alpha**3*norm/(2*F**2)-3*alpha**2*boxX/F
        self.assertEqual(s.factor(Echi-expected),0)


if __name__ == "__main__":
    unittest.main(verbosity=2)
