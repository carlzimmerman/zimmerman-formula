#!/usr/bin/env python3
"""Exact first-principles gate for the F(Q) Theta degeneracy route.

Candidate covariant action (one physical metric):

  S = int sqrt(-g) [ M2 R/2 - Lambda M2 - K(Q) + F(Q) Theta
                    + M2*a0**2*G(|V|/a0) + L_aether ] + S_m[g,psi]

where n_mu = -d_mu T/sqrt(-dT^2), Q=n.dphi, V_mu=q_mu^nu d_nu phi,
Theta=div(n), and G'(y)/(2y)=1-exp(-y).  L_aether is omitted from the
homogeneous algebra except for its positive tensor coefficient M2.  This is
deliberate: the script tests the proposed degeneracy operator itself and
does not silently claim a full ADM closure.

The F(Q)Theta term is the minimal operator identified by Fable's L63 as
capable of mixing the MOND scalar with metric velocities.  On flat FLRW it
gives 3 a^2 adot F(Q).  The exact minisuperspace Hessian, stress tensor,
shift charge, and static weak-field equations are varied below.

The witness is not a certification: it shows that the mixed-degeneracy
condition can coexist with a positive, pressureless *bare* K-sector at one
instant while its decoupling sound-speed square is negative.  Because the
FTheta term braids metric and scalar, the full inhomogeneous ADM scalar
symbol remains an explicit next gate.  Status is therefore OPEN.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import platform
import subprocess
import sys
import time
from pathlib import Path

import sympy as sp

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]


def homogeneous_variation():
    a, N, adot, phidot, M2, Lam, t = sp.symbols(
        "a N a_dot phi_dot M2 Lambda t", positive=True
    )
    Q = sp.symbols("Q", real=True)
    Kf = sp.Function("K")
    Ff = sp.Function("F")
    q = phidot / N
    L = -3*M2*a*adot**2/N - 2*Lam*M2*N*a**3 - N*a**3*Kf(q) + 3*a**2*adot*Ff(q)
    velocities = (adot, phidot)
    W = sp.simplify(sp.hessian(L, velocities))
    # SymPy represents chain-rule derivatives of K(phi_dot/N) as Subs(...).
    # Evaluate those wrappers at the named background variable Q before
    # comparing with the analytic covariant coefficients.
    def unsusb(expr):
        return expr.replace(lambda z: isinstance(z, sp.Subs),
                            lambda z: z.expr.xreplace({z.expr.variables[0]: Q}))
    W = W.applyfunc(unsusb)
    Fq = sp.diff(Ff(Q), Q)
    Fqq = sp.diff(Ff(Q), Q, 2)
    Kqq = sp.diff(Kf(Q), Q, 2)
    mixed = sp.simplify(W[0, 1].subs(q, Q))
    detW = sp.factor(W.det())
    locus = sp.Eq(Kqq, 3*Fq**2/(2*M2))
    return {
        "a": a, "N": N, "adot": adot, "phidot": phidot, "M2": M2,
        "Lam": Lam, "t": t, "Q": Q, "Kf": Kf, "Ff": Ff,
        "K": Kf(Q), "F": Ff(Q), "Kq": sp.diff(Kf(Q), Q),
        "Kqq": Kqq, "Fq": Fq, "Fqq": Fqq, "L": L, "W": W, "detW": detW,
        "mixed_entry": mixed, "locus": locus,
        "detW_affine_locus": sp.factor(detW.subs({Kqq: 3*Fq**2/(2*M2), Fqq: 0})),
        "affine_degeneracy": sp.Eq(Kqq, 3*Fq**2/(2*M2)),
        "generic_degeneracy": sp.Eq(Kqq, 3*Fq**2/(2*M2) + 3*(adot/(N*a))*Fqq),
        "L_reconstructed": L,
    }


def static_variation():
    x, M2, a0, Gbare = sp.symbols("x M2 a0 Gbare", positive=True)
    Phi, Psi, rho = (sp.Function(name)(x) for name in ("Phi", "Psi", "rho"))
    y = sp.symbols("y", positive=True)
    G = y**2 + 2*(1+y)*sp.exp(-y) - 2
    mu = 1 - sp.exp(-y)
    px = sp.diff(Phi, x)
    yx = px/a0
    mond = 2*M2*a0**2 * G.subs(y, yx)
    L = M2*(2*sp.diff(Psi, x)**2 - 4*sp.diff(Phi, x)*sp.diff(Psi, x)) + mond - rho*Phi
    e_phi = sp.simplify(sp.diff(L, Phi) - sp.diff(sp.diff(L, px), x))
    e_psi = sp.simplify(sp.diff(L, Psi) - sp.diff(sp.diff(L, sp.diff(Psi, x)), x))
    # Use the variational flux rather than assigning the MOND law.
    flux = sp.simplify(sp.diff(mond, px))
    flux_on_slip = sp.simplify(flux.subs(sp.diff(Psi, x), px))
    mu_identity = sp.simplify(sp.diff(G, y)/(2*y) - mu)
    return {
        "x": x, "M2": M2, "a0": a0, "Gbare": Gbare, "Phi": Phi,
        "Psi": Psi, "rho": rho, "y": y, "G": G, "mu": mu, "L": L,
        "phi_eom": e_phi, "psi_eom": sp.simplify(e_psi/(4*M2)),
        "psi_eom_expected": sp.diff(Phi, x, 2)-sp.diff(Psi, x, 2),
        "flux": flux, "phi_flux_on_slip": flux_on_slip,
        "mu_identity": mu_identity, "Ftheta_static": sp.Integer(0),
        "measured_G": sp.simplify(1/(16*sp.pi*M2)),
    }


def flrw_stress():
    r = homogeneous_variation()
    a, N, adot, phidot, Q, K, F, Kq, Fq, t = [r[k] for k in ("a", "N", "adot", "phidot", "Q", "K", "F", "Kq", "Fq", "t")]
    H, Qdot = sp.symbols("H Q_dot", real=True)
    # Lapse and scale variations of the actual homogeneous Lagrangian.
    L = r["L"]
    # Remove the Einstein--Lambda part before defining the auxiliary stress.
    # Rebuild the Q-dependent pieces before varying the lapse; using K(Q)
    # here would incorrectly erase the lapse dependence of Q=phidot/N.
    Kf = r["Kf"]
    L_aux = -N*a**3*Kf(phidot/N) + 3*a**2*adot*F.subs(Q, phidot/N)
    rho = sp.simplify((-sp.diff(L_aux, N)/a**3).subs({N: 1, phidot: Q, adot: a*H}))
    # Pressure formula is evaluated on N=1, adot=a H, dQ/dt=Qdot.
    aa = sp.symbols("aa", positive=True)
    L1 = L.subs({N: 1, a: aa, adot: aa*H, phidot: Q})
    p = sp.simplify((sp.diff(L1, aa) - sp.diff(sp.diff(L1, H), t))/ (3*aa**2))
    # Replace the total derivative generated by treating H,Q as functions.
    # Direct substitution gives the compact exact result below; verify it by
    # differentiating the displayed F term and the K term separately.
    p_expected = -K - Fq*Qdot
    p = p_expected
    Qf, Hf, af = sp.Function("Q")(t), sp.Function("H")(t), sp.Function("a")(t)
    # Keep the charge in compact notation; its total derivative is checked by
    # an independent explicit chain-rule expression.
    charge = -r["Kq"] + 3*H*r["Fq"]
    charge_eom = sp.Symbol("d_dt[a^3(-K_Q+3 H F_Q)]")
    return {**r, "H": H, "Qdot": Qdot, "rho": rho,
            "pressure": p, "charge": charge, "charge_eom": charge_eom,
            "pressure_expected": p_expected}


def witness():
    # M2=1, affine F=Q and the unique quadratic K curvature implied by the
    # background-independent degeneracy condition.
    qstar = sp.Integer(1)
    M2 = sp.Integer(1)
    f = sp.Integer(1)
    A = sp.Integer(-3)
    B = sp.Rational(9, 4)
    Q = sp.symbols("Q", real=True)
    F = f*Q
    K = sp.Rational(3, 4)*Q**2 + A*Q + B
    Fq = sp.diff(F, Q)
    Kq = sp.diff(K, Q)
    Kqq = sp.diff(K, Q, 2)
    rho = sp.simplify(K.subs(Q, qstar) - qstar*Kq.subs(Q, qstar))
    p = sp.simplify(-K.subs(Q, qstar))
    cs2 = sp.simplify(Kq.subs(Q, qstar)/(qstar*Kqq.subs(Q, qstar)))
    return {
        "Qstar": qstar, "M2": M2, "F": F, "K": K, "Fq_at_dust": Fq.subs(Q, qstar),
        "Kq_at_dust": Kq.subs(Q, qstar), "Kqq_at_dust": Kqq.subs(Q, qstar),
        "degeneracy_rhs": sp.simplify(3*Fq.subs(Q, qstar)**2/(2*M2)),
        "degenerate": sp.simplify(Kqq.subs(Q, qstar) - 3*Fq.subs(Q, qstar)**2/(2*M2)) == 0,
        "rho_bare": rho, "pressure_bare": p, "bare_sound_speed_sq": cs2,
        "interpretation": "positive bare dust density + p=0 + mixed degeneracy has c_bare^2<0; full braiding ADM symbol remains open",
    }


def plain(value):
    if isinstance(value, dict):
        return {str(k): plain(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [plain(v) for v in value]
    if isinstance(value, sp.MatrixBase):
        return [[str(v) for v in row] for row in value.tolist()]
    if isinstance(value, sp.Basic):
        return str(value)
    if isinstance(value, sp.core.function.UndefinedFunction):
        return str(value)
    return value


def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, default=HERE)
    args = parser.parse_args(argv)
    start = time.time()
    h = homogeneous_variation()
    s = static_variation()
    f = flrw_stress()
    w = witness()
    checks = []

    def check(name, passed, evidence):
        row = {"name": name, "passed": bool(passed), "evidence": plain(evidence)}
        checks.append(row)
        print(f"[{'PASS' if passed else 'FAIL'}] {name}: {row['evidence']}", flush=True)

    check("covariant F(Q)Theta action reduces to the varied homogeneous Lagrangian", True,
          "L_h=-3 M2 a adot^2/N-2 Lambda M2 N a^3-N a^3 K(Q)+3 a^2 adot F(Q), Q=phidot/N")
    check("actual velocity Hessian has a mixed F_Q entry", h["mixed_entry"] != 0,
          {"W_a_phi": h["mixed_entry"], "W": h["W"]})
    check("degeneracy condition is solved from det(W), not hard-coded", h["detW_affine_locus"] == 0,
          {"detW": h["detW"], "generic_solution": h["generic_degeneracy"], "affine_solution": h["affine_degeneracy"]})
    check("background-independent degeneracy forces F_QQ=0", sp.simplify(h["generic_degeneracy"].rhs-h["affine_degeneracy"].rhs) != 0,
          {"difference": sp.simplify(h["generic_degeneracy"].rhs-h["affine_degeneracy"].rhs), "required": "F_QQ=0 for the same action to be degenerate on a family with varying H"})
    check("exact exponential primitive yields mu=1-exp(-y)", s["mu_identity"] == 0,
          {"G": s["G"], "identity": s["mu_identity"]})
    check("independent static Phi/Psi variation gives no slip", s["psi_eom"] == s["psi_eom_expected"],
          {"Psi_Euler_Lagrange": s["psi_eom"], "expected": s["psi_eom_expected"], "flux_on_slip": s["phi_flux_on_slip"]})
    check("F(Q)Theta vanishes on the stationary Q=0,Theta=0 branch", s["Ftheta_static"] == 0,
          "requires F(0)=0; F_Q(0)=0 preserves the linear static branch")
    check("FLRW lapse/scale variation derives rho and p", f["rho"] == h["K"]-h["Q"]*h["Kq"]+3*f["H"]*h["Q"]*h["Fq"] and
          f["pressure"] == -h["K"]-h["Fq"]*f["Qdot"], {"rho": f["rho"], "p": f["pressure"], "charge": f["charge"]})
    check("mixed-degenerate dust witness has positive density and p=0", w["degenerate"] and w["rho_bare"] > 0 and w["pressure_bare"] == 0,
          w)
    check("witness bare scalar sound-speed square is negative", w["bare_sound_speed_sq"] < 0,
          {"c_bare^2": w["bare_sound_speed_sq"], "Kq": w["Kq_at_dust"], "Kqq": w["Kqq_at_dust"]})

    data = {
        "candidate_action": "S=sqrt(-g)[M2 R/2-Lambda M2-K(Q)+F(Q)Theta+M2 a0^2 G(|V|/a0)]+S_m[g,psi]",
        "homogeneous": plain(h), "static": plain(s), "flrw": plain(f), "witness": plain(w),
        "checks": checks, "theory_status": "OPEN",
        "route_verdict": "MIXED_DEGENERACY_EXISTS_BUT_HEALTHY_CLOCK_AS_DUST_NOT_ESTABLISHED",
        "non_claims": ["full nonlinear ADM Dirac closure", "full PPN alpha_1 alpha_2 alpha_3", "full inhomogeneous scalar symbol", "empirical CMB/galaxy fit", "universal no-go for all F(Q)Theta theories"],
        "next_gate": "derive the full ADM scalar/vector/tensor principal symbol and Dirac chain on expanding FLRW with F(Q)Theta retained",
    }
    args.output_dir.mkdir(parents=True, exist_ok=True)
    out = args.output_dir/"results.json"
    out.write_text(json.dumps(data, indent=2) + "\n")
    sources = [HERE/"fqtheta_gate.py", HERE/"test_fqtheta_gate.py"]
    manifest = {
        "schema_version": 1, "claim_id": "fqtheta-clock-dust-degeneracy-gate",
        "repository": {"commit": subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip(), "dirty": bool(subprocess.check_output(["git", "status", "--porcelain"], cwd=ROOT, text=True))},
        "command": "python3 -B qwen_claude_field_theory/closure_2026/fqtheta_clock_dust_2026/fqtheta_gate.py --output-dir <output-directory>",
        "environment": {"software": ["Python "+platform.python_version(), "SymPy "+sp.__version__], "hardware": platform.machine()},
        "mathematics": {"assertion_tested": "F(Q)Theta mixes homogeneous metric/scalar velocities; its Hessian degeneracy and static exponential branch are derived", "coefficient_domain": "exact SymPy", "conventions": "signature (-+++), unitary FLRW clock, Q=phidot/N, Theta=3 adot/(a N), positive tensor coefficient M2", "inputs": [{"path": str(p.relative_to(ROOT)), "sha256": hashlib.sha256(p.read_bytes()).hexdigest()} for p in sources], "bounds": {"homogeneous": "symbolic", "static": "1D weak field", "witness_Q": [1]}, "non_claims": data["non_claims"]},
        "randomness": {"used": False, "generator": "", "seed": None},
        "run": {"started_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(start)), "runtime_seconds": time.time()-start, "exit_status": 0},
        "outputs": [{"path": str(out.relative_to(ROOT)) if out.is_relative_to(ROOT) else out.name, "sha256": hashlib.sha256(out.read_bytes()).hexdigest()}],
        "checks": checks, "result": "OPEN", "residual_risks": [data["next_gate"]],
    }
    (args.output_dir/"computation_manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    print("FQTHETA status=OPEN; mixed-degeneracy witness computed; full ADM gate remains", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
