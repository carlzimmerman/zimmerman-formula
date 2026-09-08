#!/usr/bin/env python3
"""IC6 algebraic Schur operator and strong-space witness bridge.

Exact identities support IC6_STRONG_AUXILIARY.md. A bounded Fourier check
is a conditioning control, not a nonlinear-evolution or causality theorem.
"""
import argparse
from functools import lru_cache
import hashlib
import json
from pathlib import Path
import platform

import numpy as np
import sympy as sp

import nonlinear_square_completion as square

HERE = Path(__file__).resolve().parent
BASE = "0b75e72bf5797e451beb258847ade528cd9c4551"
PIN = "4c9a79caa9a6d54a6a5f006440886f54b9092d68978249fb79f95a0f73229ece"


@lru_cache(None)
def derive():
    if hashlib.sha256((HERE / "nonlinear_square_completion.py").read_bytes()).hexdigest() != PIN:
        raise RuntimeError("Frozen IC5 Hamiltonian dependency changed")
    # Unrestricted local second jets in passive t and gradient p=Ds.
    # The eliminated t response is obtained by varying this quadratic jet.
    A, M = sp.symbols("A M", positive=True)
    At = sp.Symbol("A_t", real=True)
    grad = sp.Matrix(sp.symbols("s_x s_y s_z", real=True))
    vgrad = sp.Matrix(sp.symbols("v_x v_y v_z", real=True))
    passive = sp.Symbol("delta_t", real=True)
    g2 = sp.Symbol("gradient_squared", nonnegative=True)
    quadratic = M*passive**2/2 + 2*At*passive*grad.dot(vgrad) + A*vgrad.dot(vgrad)
    passive_response = sp.solve(sp.diff(quadratic, passive), passive)[0]
    reduced = sp.factor(quadratic.subs(passive, passive_response))
    principal = sp.hessian(reduced, tuple(vgrad))
    schur_residual = (principal - (2*A*sp.eye(3)-4*At**2/M*grad*grad.T)).applyfunc(sp.factor)
    longitudinal = sp.factor((grad.T*principal*grad)[0]/grad.dot(grad))
    longitudinal = sp.factor(longitudinal.subs(grad.dot(grad),g2))
    # A symbolic radial restriction avoids assumptions about orientation.
    longitudinal = sp.factor(principal[0,0].subs({grad[0]:sp.sqrt(g2),grad[1]:0,grad[2]:0}))
    completion_residual = sp.factor(quadratic-reduced-M*(passive-passive_response)**2/2)

    d = square.derive()
    xi,u,T,h0 = (d[key] for key in ("xi","u","T","h0"))
    w,trace,m,vol,a02 = (d[key] for key in ("w","trace","m","vol","a02"))
    JT = 1+sp.exp(-6*w)*trace**2*d["F"]/(m*m*vol*vol*a02)
    H6 = d["Hnongrad"]+d["kinetic_shear"]*(1/JT-1)
    # Differentiate the IC6 Hamiltonian BEFORE imposing shear-free data.
    raw_mass = -sp.hessian(H6,(xi,u))
    normalization = m*vol*d["f"]*h0*h0
    mass = raw_mass.subs(d["Lam"],d["Lam_witness"]).subs(d["witness"])/normalization
    mass = mass.applyfunc(lambda e:sp.simplify(e.subs(sp.log(sp.Rational(5,9)),-d["ell"])))
    mass = mass.applyfunc(lambda e:sp.factor(e.subs(1/d["ell"],5*(T+sp.Rational(27,16))/54)))
    mass_bridge = (mass-d["mass"]).applyfunc(sp.factor)
    coordinate_map = d["coordinate_jacobian"]
    transformed_mass = (coordinate_map.T*mass*coordinate_map).applyfunc(sp.factor)
    ps,pt,px,pu,ds,dt = sp.symbols("p_s p_t p_xi p_u delta_s delta_t",real=True)
    new_momenta = {ps:px, pt:pu-d["b"]*px}
    canonical_residual = [sp.expand((ps*ds+pt*dt).subs(new_momenta)
                                    -(px*(ds-d["b"]*dt)+pu*dt))]
    k2 = sp.Symbol("k_squared",nonnegative=True)
    gradient_coefficient = d["alpha"]*sp.exp(sp.Rational(2,3))/(h0*h0)
    L0 = transformed_mass+sp.diag(2*gradient_coefficient*k2,0)
    inverse = L0.inv().applyfunc(sp.factor)
    determinant = sp.factor(L0.det())
    inverse_residual = (L0*inverse-sp.eye(2)).applyfunc(sp.factor)
    return locals()


def numerical_controls():
    d = derive()
    values = {d["T"]:-sp.Rational(27,16)+54/(5*sp.log(sp.Rational(9,5))),d["h0"]:1}
    matrix = sp.lambdify(d["k2"],d["L0"].subs(values),"numpy")
    ks = [0,1,4,16,64,256,1024,4096,16384]
    inverse_residuals,eigenvalues,weighted_norms = [],[],[]
    for k2 in ks:
        L = np.asarray(matrix(k2),dtype=float)
        inverse = np.linalg.inv(L)
        inverse_residuals.append(float(np.max(np.abs(L@inverse-np.eye(2)))))
        eigenvalues.append(float(np.linalg.eigvalsh(L)[0]))
        # E_r=H^(r+2) x H^(r+1); F_r=H^r x H^(r+1).
        # The common H^r factor cancels in this weighted inverse norm.
        weight = np.diag([1+k2,np.sqrt(1+k2)])
        source_weight_inv = np.diag([1,1/np.sqrt(1+k2)])
        weighted_norms.append(float(np.linalg.norm(weight@inverse@source_weight_inv,2)))
    return dict(tested_k_squared=ks,maximum_inverse_residual=max(inverse_residuals),
                minimum_eigenvalue=min(eigenvalues),weighted_inverse_norm_max=max(weighted_norms),
                weighted_inverse_norms=weighted_norms,
                scope="Nine real Fourier controls, not a proof over all k or nonlinear states")


def run():
    d = derive()
    residuals = dict(schur=list(d["schur_residual"]),mass_bridge=list(d["mass_bridge"]),
                     canonical=d["canonical_residual"],inverse=list(d["inverse_residual"]),
                     completion=[d["completion_residual"]])
    return dict(base=BASE,python=platform.python_version(),sympy=sp.__version__,numpy=np.__version__,
                input_sha256=PIN,exact_checks_passed=all(x==0 for vals in residuals.values() for x in vals),
                exact_residuals={k:[str(x) for x in v] for k,v in residuals.items()},
                schur_principal=str(d["principal"]),longitudinal=str(d["longitudinal"]),
                mass=str(d["mass"]),transformed_mass=str(d["transformed_mass"]),
                Fourier_determinant=str(d["determinant"]),Fourier_inverse=str(d["inverse"]),
                numerical=numerical_controls(),
                full_theory_closed=False,
                remaining=["Coupled physical evolution estimates and characteristic reduction",
                           "Regular plateau persistence, full PPN, galactic and cosmological matching"])


def main(argv=None):
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--require-full-theory",action="store_true")
    args=parser.parse_args(argv)
    result=run()
    print(json.dumps(result,indent=2,allow_nan=False))
    if not result["exact_checks_passed"]:
        return 1
    n=result["numerical"]
    if n["maximum_inverse_residual"]>=1e-8 or n["minimum_eigenvalue"]<=0:
        return 1
    return 2 if args.require_full_theory else 0


if __name__=="__main__":
    raise SystemExit(main())
