"""Audit actual source functions; never run lane module top-level experiments.

Finite contract: n=12 periodic Fourier grid, u=(sin y,0,sin x), no unresolved
product modes; source ASTs are extracted without changing their bodies.
Also compare N04c's original classical evolution with its exact Stokes
solution and a corrected-index/sign version. No regularity claim is tested.
"""
import ast
import copy
import hashlib
import json
from pathlib import Path
import sys
import time

import numpy as np
import sympy as sp

ROOT = Path(__file__).resolve().parents[4]
HERE = Path(__file__).resolve().parent
LANE = ROOT / "deepseek_push/navier_stokes_attempt"
FILES = ["N03_supbarrier.py", "N03b_beta_family.py", "N04_galerkin.py",
         "N04b_equilibrium.py", "N04c_equilibrium_long.py",
         "N05_window_theorem.py", "N09_twofluid_galerkin.py", "N12_selfseeding.py"]


def tree(name):
    return ast.parse((LANE / name).read_text())


def function_node(t, name):
    return next(x for x in ast.walk(t) if isinstance(x, ast.FunctionDef) and x.name == name)


def bind(nodes, env):
    module = ast.fix_missing_locations(ast.Module(body=nodes, type_ignores=[]))
    exec(compile(module, "<audited-source-AST>", "exec"), env)


def rms(a):
    return float(np.sqrt(np.mean(np.sum(a*a, axis=0))))


def maxabs(a):
    return float(np.max(np.abs(a)))


def manufactured():
    n = 12
    k = np.fft.fftfreq(n) * n
    K1, K2, K3 = np.meshgrid(k, k, np.fft.rfftfreq(n)*n, indexing="ij")
    Ksq = K1*K1+K2*K2+K3*K3
    Ksq[0, 0, 0] = 1
    x,y,z = np.meshgrid(*(np.arange(n)*2*np.pi/n for _ in range(3)), indexing="ij")
    ug = np.stack([np.sin(y), np.zeros_like(x), np.sin(x)])
    uh = np.stack([np.fft.rfftn(a) for a in ug])
    exact_wrong = np.stack([np.sin(x)*np.cos(x), np.sin(y)*np.cos(y), np.zeros_like(x)])
    exact_correct = np.stack([np.zeros_like(x), np.zeros_like(x), np.sin(y)*np.cos(x)])
    reports = []
    for name in FILES:
        t = tree(name)
        invk=np.zeros_like(Ksq)
        invk[1:]=1/Ksq[1:]  # actual N12 source zeros the ENTIRE k_x=0 plane
        env = dict(np=np, n=n, N=n, K1=K1, K2=K2, K3=K3, Ksq=Ksq,
                   MASK=(Ksq <= (n/3)**2).astype(float), INVK=invk, uh=uh)
        names = ["to_real", "proj"] + (["nlin_real", "nlin_hat"] if name.startswith("N05") else ["nlin"])
        nodes = [function_node(t, key) for key in names]
        bind(nodes, env)
        raw = env["nlin_hat" if name.startswith("N05") else "nlin"](uh)
        raw_real = env["to_real"](raw)
        projected = env["to_real"](env["proj"](raw))
        exact_hat = np.stack([np.fft.rfftn(a) for a in exact_correct])
        corrected_projection = env["to_real"](env["proj"](exact_hat))
        assert maxabs(raw_real-exact_wrong) < 2e-14
        if name.startswith("N12"):
            expected_projection=np.stack([np.zeros_like(x),np.sin(y)*np.cos(y),np.zeros_like(x)])
            assert maxabs(projected-expected_projection) < 2e-14
        else:
            assert rms(projected) < 2e-14
        assert maxabs(corrected_projection-exact_correct) < 2e-14
        reports.append(dict(file=name, sha256=hashlib.sha256((LANE/name).read_bytes()).hexdigest(),
            function_lines={a.name:[a.lineno,a.end_lineno] for a in nodes},
            wrong_gradient_error=maxabs(raw_real-exact_wrong),
            projected_implemented_rms=rms(projected),
            projected_correct_rms=rms(corrected_projection),
            difference_rms=rms(projected-corrected_projection)))
        if name.startswith("N12"):
            divergence=np.fft.irfftn(sum(1j*k*env["proj"](raw)[j] for j,k in enumerate([K1,K2,K3])),s=(n,n,n))
            reports[-1]["projection_divergence_max"] = maxabs(divergence)
            reports[-1]["projector_defect"] = "INVK[1:]=1/Ksq[1:] drops inverse on all k_x=0 modes"
            assert maxabs(divergence) > 0.9
        if name.startswith("N05"):
            # The nested nlin_real differentiates the outer initial uh. It
            # scales linearly with a new velocity, not quadratically.
            scaled_raw=env["nlin_hat"](2*uh)
            reports[-1]["frozen_jacobian_linearity_error"] = maxabs(scaled_raw-2*raw)
            reports[-1]["quadratic_scaling_defect_real_rms"] = rms(env["to_real"](scaled_raw-4*raw))
            assert maxabs(scaled_raw-2*raw) < 1e-12
            assert reports[-1]["quadratic_scaling_defect_real_rms"] > 0.5
    # Exact independent symbolic derivation of this continuum witness.
    sx,sy,sz=sp.symbols("x y z", real=True)
    su=sp.Matrix([sp.sin(sy),0,sp.sin(sx)])
    D=su.jacobian([sx,sy,sz])
    assert sp.simplify(sp.trace(D)) == 0
    assert sp.simplify(D.T*su-sp.Matrix([sp.sin(sx)*sp.cos(sx),sp.sin(sy)*sp.cos(sy),0])) == sp.zeros(3,1)
    assert sp.simplify(D*su-sp.Matrix([0,0,sp.sin(sy)*sp.cos(sx)])) == sp.zeros(3,1)
    return dict(n=n, field="(sin(y),0,sin(x))", exact_correct_projected_rms="1/2",
                aliasing="all witness product modes have |k|<=2, below cutoff 4 and Nyquist 6", files=reports)


def instrument_galerkin(corrected):
    node = copy.deepcopy(function_node(tree("N04c_equilibrium_long.py"), "galerkin"))
    if corrected:
        # Replace only the advection contraction. D[j][i]=partial_j u_i.
        new = ast.parse('''def nlin(uh):
    ug = to_real(uh)
    waves = (K1,K2,K3)
    D = [[np.fft.irfftn(1j*waves[j]*uh[i],s=(n,n,n),axes=(0,1,2))
          for i in range(3)] for j in range(3)]
    conv = [sum(ug[j]*D[j][i] for j in range(3)) for i in range(3)]
    return np.stack([np.fft.rfftn(c,axes=(0,1,2)) for c in conv])
''').body[0]
        for i,child in enumerate(node.body):
            if isinstance(child, ast.FunctionDef) and child.name == "nlin":
                node.body[i] = new
            if isinstance(child, ast.FunctionDef) and child.name == "nlin_real_derivs":
                for sub in ast.walk(child):
                    if isinstance(sub, ast.AugAssign) and isinstance(sub.value, ast.BinOp):
                        sub.value.right = ast.parse("derivs[i][j]", mode="eval").body
            if isinstance(child, ast.FunctionDef) and child.name == "rhs":
                child.body = ast.parse("return proj(lam*u) - proj(nlin(u)) + proj(drag_hat(u)) + fhat").body
    # Return exact state/init/forcing for comparison; no original files changed.
    result = node.body[-1].value
    for key,value in [("state","u"),("initial","uh"),("forcing","fhat"),("Ksq","Ksq")]:
        result.keys.append(ast.Constant(key)); result.values.append(ast.Name(value,ast.Load()))
    ast.fix_missing_locations(node)
    if corrected:
        (OUTDIR / "corrected_galerkin.py").write_text(
            '"""Isolated N04c repair: contraction, convection sign, matching diagnostic.\n'
            'Derived from the pinned original; benchmark returns states for audit.\n'
            'No claim of continuum regularity or numerical convergence in N.\n"""\n'
            'import numpy as np\nimport time\n\n'+ast.unparse(node)+"\n")
    env=dict(np=np,time=time)
    bind([node],env)
    return env["galerkin"]


def pair_comparison():
    original = instrument_galerkin(False)
    repaired = instrument_galerkin(True)
    parameters = dict(n=12,nu=0.05,c_d=0.0,a0cap=None,A=1.0,T=2.0,seed=7,every=1,track_g29=True)
    runs = {"original":original(dt=0.004,tag="audit-original",**parameters),
            "corrected":repaired(dt=0.004,tag="audit-corrected",**parameters),
            "corrected_half_dt":repaired(dt=0.002,tag="audit-corrected-half-dt",**parameters)}
    n = parameters["n"]
    def real(h):
        return np.stack([np.fft.irfftn(v,s=(n,n,n)) for v in h])
    report={"parameters":parameters,"dt":0.004,"runs":{}}
    for key,r in runs.items():
        u=real(r["state"])
        h=r["state"]
        k=np.fft.fftfreq(n)*n
        waves=np.meshgrid(k,k,np.fft.rfftfreq(n)*n,indexing="ij")
        div=np.fft.irfftn(sum(1j*waves[j]*h[j] for j in range(3)),s=(n,n,n))
        deriv=[[np.fft.irfftn(1j*waves[j]*h[i],s=(n,n,n)) for j in range(3)] for i in range(3)]
        adv=np.stack([sum(u[j]*deriv[i][j] for j in range(3)) for i in range(3)])
        energy_cancellation=float(np.mean(np.sum(u*adv,axis=0)))
        residual = r["ene"][-1]-r["ene"][0]-np.trapz(-parameters["nu"]*r["Z_real"]+r["Pf"]+r["Pd"],r["t"])
        damping=np.exp(-parameters["nu"]*r["Ksq"]*parameters["T"])
        stokes=damping*r["initial"]+(1-damping)/(parameters["nu"]*r["Ksq"])*r["forcing"]
        stokes_error=rms(real(h-stokes))
        report["runs"][key]=dict(final_sup=float(r["sup"][-1]), final_energy=float(r["ene"][-1]),
            final_enstrophy=float(r["enst"][-1]), maximum_divergence=maxabs(div),
            convective_energy_cancellation=energy_cancellation, integrated_energy_residual=float(residual),
            rms_difference_from_exact_stokes=stokes_error,cfl=float(r["cfl"]))
        assert maxabs(div) < 1e-12 and abs(energy_cancellation) < 1e-12
        assert abs(residual) < 2e-6
    original_stokes=report["runs"]["original"]["rms_difference_from_exact_stokes"]
    assert original_stokes < 1e-11
    difference=rms(real(runs["corrected"]["state"]-runs["original"]["state"]))
    time_error=rms(real(runs["corrected_half_dt"]["state"]-runs["corrected"]["state"]))
    assert difference > 1e-4 and time_error < 1e-8
    report.update(corrected_vs_original_rms=difference,corrected_dt_halving_rms=time_error,
                  seed="numpy.default_rng(7), same random initial state as source",
                  caveat="Finite n=12 comparison, not a reproduction of n=32 T=200 lane and no continuum inference")
    return report


if __name__ == "__main__":
    output=Path(sys.argv[1])
    OUTDIR=output.parent
    result=dict(manufactured=manufactured(),comparison=pair_comparison())
    output.write_text(json.dumps(result,indent=2)+"\n")
    print(json.dumps(result,indent=2))
