#!/usr/bin/env python3
"""Read-only independent canonical-coordinate control for source_evolution.

No change to the constitutive action: subtract only a time-dependent total
derivative from the same quadratic Lagrangian. Fixed M2=1, k>0, real arithmetic.
"""
import importlib.util
import json
from pathlib import Path
import platform
import time

import numpy as np
import scipy
from scipy.integrate import solve_ivp
import sympy as sy

PATH = Path(__file__).resolve().parents[1] / "evolve.py"
spec = importlib.util.spec_from_file_location("audited_source_evolution", PATH)
e = importlib.util.module_from_spec(spec)
spec.loader.exec_module(e)


def shifted_coefficients(model, t, k, amplitude):
    c = e.coefficients(model, t, k, amplitude)
    b = model.background(float(t))
    td = b["Hdot"] + 3 * model.gamma * c["q"]**2 * b["qdot"]
    theta = c["Theta"]
    # h=2r/Theta, g=-rho/Theta.  Lnew=Lold-d[a^3(h z^2/2+g z)]/a^3dt.
    bt = c["J"] * c["R"] * c["r"] / c["den"]
    ft = -c["J"] * c["f"] / c["den"]
    ct = (2*c["r"]*((theta-c["H"])/theta+td/theta**2)
          + c["R"]**2*c["r"]**2/c["den"])
    st = c["S"] - c["rho"]*td/theta**2
    return c, bt, ft, ct, st


def shifted_rhs(t, state, model, k, amplitude):
    c, bt, ft, ct, st = shifted_coefficients(model, t, k, amplitude)
    z, w = state
    zd = (w/c["a"]**3-bt*z-ft)/c["A"]
    wd = c["a"]**3*(bt*zd+ct*z+st)
    return np.array([zd, wd])


def reconstruct(t, state, model, k, amplitude):
    c, bt, ft, ct, st = shifted_coefficients(model, t, k, amplitude)
    z, w = state
    p = w+c["a"]**3*(2*c["r"]*z/c["Theta"]-c["rho"]/c["Theta"])
    # Exact Phi=Psi from original zeta Euler and momentum equations; this form
    # also avoids subtracting the leading zeta in -zeta+H p/(2 a^3 r).
    phi = ((c["H"]-c["Theta"])*z/c["Theta"]
           + c["H"]*w/(2*c["a"]**3*c["r"])
           - c["H"]*c["rho"]/(2*c["r"]*c["Theta"]))
    return np.array([z,p]), phi


def exact_checks():
    a,r,theta,H,td,rho,A,J,R,den,f = sy.symbols("a r theta H td rho A J R den f", nonzero=True)
    z,w = sy.symbols("z w")
    bt,ft = J*R*r/den,-J*f/den
    ce=2*r+R**2*r**2/den
    ss=-R*r*f/den
    h,g=2*r/theta,-rho/theta
    hd3h=2*r*(H/theta-td/theta**2)
    gd3h=rho*td/theta**2
    p=w+a**3*(h*z+g)
    old_v=(p/a**3-(h+bt)*z-(g+ft))/A
    new_v=(w/a**3-bt*z-ft)/A
    old_pd=a**3*((h+bt)*old_v+ce*z+ss)
    ct=2*r*((theta-H)/theta+td/theta**2)+R**2*r**2/den
    new_wd=a**3*(bt*new_v+ct*z+ss-gd3h)
    checks={
        "velocity_identity":sy.factor(old_v-new_v)==0,
        "momentum_derivative_identity":sy.factor(old_pd-new_wd-a**3*(h*new_v+hd3h*z+gd3h))==0,
        "potential_identity":sy.factor(-z+H*p/(2*a**3*r)-((H-theta)*z/theta+H*w/(2*a**3*r)-H*rho/(2*r*theta)))==0,
    }
    if not all(checks.values()):
        raise AssertionError(checks)
    return checks


def run():
    amplitude, k, tmax = 1e-7, 100., 4.
    model = e.Model(tmax)
    c, bt, ft, ct, st = shifted_coefficients(model, 0., k, amplitude)
    y0 = [0., c["a"]**3*ft]
    # Orthogonal coordinate-change check against original equations, using
    # random states that are not assumed to lie on a solved trajectory.
    rng = np.random.default_rng(803)
    errors = []
    for t in np.linspace(0., tmax, 21):
        state = rng.normal(size=2)*1e-7
        old_state, _ = reconstruct(t,state,model,k,amplitude)
        newdot = shifted_rhs(t,state,model,k,amplitude)
        olddot = e.rhs(t,old_state,model,k,amplitude)
        c = e.coefficients(model,t,k,amplitude)
        b = model.background(float(t))
        td = b["Hdot"]+3*model.gamma*c["q"]**2*b["qdot"]
        h = 2*c["r"]/c["Theta"]
        hd3h = 2*c["r"]*(c["H"]/c["Theta"]-td/c["Theta"]**2)
        gd3h = c["rho"]*td/c["Theta"]**2
        transformed = np.array([newdot[0],newdot[1]+c["a"]**3*(h*newdot[0]+hd3h*state[0]+gd3h)])
        errors.append(float(np.linalg.norm(transformed-olddot)/max(np.linalg.norm(olddot),1e-30)))
    grid = np.linspace(0.,tmax,161)
    records=[]
    for method, rtol in [("DOP853",1e-10),("DOP853",1e-12),("Radau",1e-10)]:
        start=time.monotonic()
        sol=solve_ivp(lambda t,y:shifted_rhs(t,y,model,k,amplitude),(0.,tmax),y0,
                      method=method,rtol=rtol,atol=rtol*amplitude*1e-3,
                      dense_output=True,first_step=1e-4)
        if not sol.success:
            raise RuntimeError(sol.message)
        samples=[]
        for t, state in zip(grid,sol.sol(grid).T):
            old, phi = reconstruct(t,state,model,k,amplitude)
            c=e.coefficients(model,t,k,amplitude)
            f=e.fields(t,old,model,k,amplitude)
            samples.append(dict(t=float(t),zeta=float(old[0]),p=float(old[1]),
                                Phi=float(phi),response=float(-2*c["r"]*phi/c["rho"]),
                                field_formula_abs_error=float(abs(phi-f["Phi"]))))
        records.append(dict(method=method,rtol=rtol,nfev=sol.nfev,seconds=time.monotonic()-start,samples=samples))
    comparisons=[]
    for index in (0,2):
        for field in ("zeta","p","Phi","response"):
            x=np.array([r[field] for r in records[index]["samples"]])
            ref=np.array([r[field] for r in records[1]["samples"]])
            comparisons.append(dict(method=records[index]["method"],field=field,
                                    max_abs_error=float(np.max(np.abs(x-ref))),
                                    max_scaled_error=float(np.max(np.abs(x-ref))/max(np.max(np.abs(ref)),1e-30))))
    start=time.monotonic()
    original=e.integrate(model,k,amplitude,rtol=1e-10)
    original_elapsed=time.monotonic()-start
    original_values=[]
    for t in grid:
        state=original.sol(t)
        f=e.fields(t,state,model,k,amplitude)
        c=e.coefficients(model,t,k,amplitude)
        original_values.append(dict(zeta=state[0],p=state[1],Phi=f["Phi"],response=-2*c["r"]*f["Phi"]/c["rho"]))
    original_comparisons=[]
    for field in ("zeta","p","Phi","response"):
        x=np.array([r[field] for r in original_values])
        ref=np.array([r[field] for r in records[1]["samples"]])
        original_comparisons.append(dict(field=field,max_abs_error=float(np.max(np.abs(x-ref))),
                                        max_scaled_error=float(np.max(np.abs(x-ref))/max(np.max(np.abs(ref)),1e-30))))
    return dict(scope="Equivalent canonical-coordinate integration of the fixed signed dust probe",
                status="Conditional on floating-point tolerances and SciPy solvers; no global physical claim",
                python=platform.python_version(),numpy=np.__version__,scipy=scipy.__version__,sympy=sy.__version__,
                bounds=dict(k=k,tmax=tmax,gamma=model.gamma,amplitude=amplitude,grid_points=len(grid),seed=803),
                exact_checks=exact_checks(),coordinate_identity_max_relative_error=max(errors),records=records,comparisons=comparisons,
                original_solver=dict(method="DOP853",rtol=1e-10,nfev=original.nfev,seconds=original_elapsed,comparisons=original_comparisons))


if __name__=="__main__":
    print(json.dumps(run(),indent=2))
