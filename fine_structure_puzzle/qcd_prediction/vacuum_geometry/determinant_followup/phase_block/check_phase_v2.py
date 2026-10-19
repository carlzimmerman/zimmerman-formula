"""Static spherical phase/radial-gauge block on its mixed boundary domain."""
import argparse
import json
from pathlib import Path
import mpmath as mp
import numpy as np
import scipy
from scipy.integrate import solve_ivp
import sympy as s


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--result", required=True)
    args = ap.parse_args()
    print("stage: symbolic factorization",flush=True)
    x = s.symbols("x", positive=True)
    h = s.coth(x)-1/x
    K = x/s.sinh(x)
    c = s.sqrt(2)*K/x
    W = s.Matrix([[h,-c],[-c,1/x]])
    U = W*W-W.diff(x)
    partner = (W*W+W.diff(x)).applyfunc(s.simplify)
    VA = h*h+(1+K*K)/x**2
    Vg = 2*K*K/x**2
    assert (partner-s.diag(VA,Vg)).applyfunc(s.simplify) == s.zeros(2)
    explicit = s.Matrix([[h*h+(3*K*K-1)/x**2,-2*c*(h+1/x)],
                         [-2*c*(h+1/x),2*(K*K+1)/x**2]])
    assert (U-explicit).applyfunc(s.simplify) == s.zeros(2)
    print("stage: scalar solution",flush=True)
    ug = 3*(x*s.coth(x)-1)
    # Elementary solution supplied independently by coordinator and verified here.
    ua = 3*(s.sinh(x)/x-x/s.sinh(x))
    assert s.simplify(-s.diff(ua,x,2)+VA*ua) == 0
    assert s.simplify(-s.diff(ug,x,2)+Vg*ug) == 0
    BA = s.simplify(s.diff(ua,x)-h*ua)
    assert s.simplify(BA-6*K*h) == 0
    assert s.series(ua,x,0,4).removeO() == x*x
    Dg = s.simplify(ug/x**2)
    DA0 = s.simplify(BA/(2*x))
    assert s.simplify(Dg/DA0-1/K) == 0
    refmass = 3*(s.cosh(x)-s.sinh(x)/x)
    Bmass = s.simplify(s.diff(refmass,x)-h*refmass)
    assert s.simplify(Bmass-3*(s.cosh(x)/x-1/s.sinh(x))) == 0
    DAm = BA/Bmass
    assert s.simplify(Dg/DAm-3*(s.sinh(x)*s.cosh(x)-x)/(2*x**3)) == 0
    print("stage: origin expansions",flush=True)

    # Independent matrix ODE with the actual mixed boundary functional.
    C = s.Matrix([[2,-2*s.sqrt(2)],[-2*s.sqrt(2),4]])
    V0 = s.Matrix([[-1,-s.sqrt(2)/3],[-s.sqrt(2)/3,-s.Rational(2,3)]])
    V2 = s.Matrix([[s.Rational(14,45),7*s.sqrt(2)/60],
                    [7*s.sqrt(2)/60,s.Rational(2,15)]])
    for i in range(2):
        for j in range(2):
            assert s.simplify(s.series(U[i,j],x,0,4).removeO()-C[i,j]/x**2-V0[i,j]-V2[i,j]*x*x) == 0
    O = s.Matrix([[s.sqrt(2),-1],[1,s.sqrt(2)]])/s.sqrt(3)
    assert (O.T*C*O-s.diag(0,6)).applyfunc(s.simplify) == s.zeros(2)
    Cn=np.array(C.evalf(),dtype=float)
    V0n=np.array(V0.evalf(),dtype=float)
    V2n=np.array(V2.evalf(),dtype=float)
    On=np.array(O.evalf(),dtype=float)
    coeffs=[]
    for col,p in [(0,1),(1,3)]:
        a=O[:,col]
        rhs=V0*a
        mat=(p+2)*(p+1)*s.eye(2)-C
        if p == 1:
            # Resonance is a freely addable regular l=2 solution; choose zero.
            b=O*s.Matrix([-s.Rational(2,9),0])
            assert (mat*b-rhs).applyfunc(s.simplify)==s.zeros(2,1)
        else:
            b=mat.inv()*rhs
        d=((p+4)*(p+3)*s.eye(2)-C).inv()*(V0*b+V2*a)
        coeffs.append((p,np.array(a.evalf(),dtype=float).ravel(),
                       np.array(b.evalf(),dtype=float).ravel(),
                       np.array(d.evalf(),dtype=float).ravel()))
    print("stage: matrix ODE",flush=True)
    def pot(t):
        if t < 0.002:
            return Cn/t**2+V0n+V2n*t*t
        ht=1/np.tanh(t)-1/t
        kt=t/np.sinh(t)
        ct=np.sqrt(2)*kt/t
        return np.array([[ht*ht+(3*kt*kt-1)/t**2,-2*ct*(ht+1/t)],
                         [-2*ct*(ht+1/t),2*(kt*kt+1)/t**2]])
    def ode(t,z):
        Y=z[:4].reshape(2,2); P=z[4:].reshape(2,2)
        return np.concatenate([P.ravel(),(pot(t)@Y).ravel()])
    rows=[]
    for X in [2,4,6]:
        hx=1/np.tanh(X)-1/X
        kx=X/np.sinh(X)
        Fexact=30*X*kx*hx*hx
        for eps in [0.001,0.0005]:
            Ystart=np.column_stack([a+b*eps**2+d*eps**4 for p,a,b,d in coeffs])
            Pstart=np.column_stack([p*a/eps+(p+2)*b*eps+(p+4)*d*eps**3 for p,a,b,d in coeffs])
            initial=np.concatenate([Ystart.ravel(),Pstart.ravel()])
            sol=solve_ivp(ode,(eps,X),initial,method="DOP853",rtol=5e-13,atol=1e-14)
            assert sol.success
            scales=np.diag([eps,eps**3])
            Y=sol.y[:4,-1].reshape(2,2)@scales
            P=sol.y[4:,-1].reshape(2,2)@scales
            F=np.linalg.det(np.vstack([Y[0,:],P[1,:]+Y[1,:]/X]))
            rel=abs(F/Fexact-1)
            assert rel < 5e-6
            Dphase=Fexact/((10/3)*X**3)
            Dghost=3*hx/X
            Z=Dghost/np.sqrt(Dphase)
            assert abs(Z*np.sqrt(kx)-1)<1e-13
            rows.append({"x":X,"origin_cutoff":eps,"matrix_mixed_boundary_det":F,
                         "exact_boundary_det":Fexact,"relative_discrepancy":rel,
                         "phase_det_ratio_to_unbroken_reference":Dphase,
                         "phase_plus_ghost_ratio":Z,"ODE_evaluations":sol.nfev})
            print("matrix case",X,eps,"residual",rel,flush=True)
    print("stage: scalar quadrature",flush=True)
    mp.mp.dps=60
    bounds=[]
    combined=[]
    for X in [mp.mpf(5),mp.mpf(10),mp.mpf(20)]:
        def ua_mp(t):
            if abs(t)<mp.mpf("1e-10"):
                return t*t-t**4/30+17*t**6/2520
            return 3*(mp.sinh(t)/t-t/mp.sinh(t))
        uaX=ua_mp(X)
        bax=6*(X/mp.sinh(X))*(mp.coth(X)-1/X)
        norm=mp.quad(lambda t:ua_mp(t)**2,[0,X])
        upper=uaX*bax/norm
        bounds.append({"x":str(X),"Rayleigh_upper_bound_for_smallest_scalar_eigenvalue":mp.nstr(upper,30),
                       "ratio_to_16_x_squared_exp_minus_2x":mp.nstr(upper/(16*X**2*mp.exp(-2*X)),30)})
        def real_integrand(t):
            if abs(t)<mp.mpf("1e-10"):
                return t*t/3
            return (mp.coth(t)-1/t)**2+(mp.cosh(t)/t-1/mp.sinh(t))**2/2
        I=mp.quad(real_integrand,[0,X])
        Zcombined=mp.sqrt(X*mp.sinh(X)**2/(9*I))
        residual=mp.log(Zcombined)-mp.log(mp.mpf(2)/3)-mp.mpf("1.5")*mp.log(X)
        combined.append({"x":str(X),"complete_static_J0_auxiliary_ratio":mp.nstr(Zcombined,30),
                         "x_times_log_residual":mp.nstr(X*residual,30)})
    out={"status":"passed","assertion_tested":"Exact phase/gauge factorization, scalar Robin determinant and reference identities; independent actual mixed-boundary matrix ODE checks",
         "software":{"sympy":s.__version__,"scipy":scipy.__version__,"numpy":np.__version__,"mpmath":mp.__version__},
         "matrix_checks":rows,"quasi_zero_Rayleigh_bounds":bounds,"complete_J0_auxiliary_comparison":combined,
         "non_claims":["Static spherical phase sector only","Reference has different holonomy and is not physical broken-vacuum matching","No four-collective-mode Jacobian added","No full QCD coefficient or alpha prediction"]}
    Path(args.result).write_text(json.dumps(out,indent=2)+"\n")
    print(json.dumps({"status":"passed","result":args.result}))


if __name__=="__main__":
    main()
