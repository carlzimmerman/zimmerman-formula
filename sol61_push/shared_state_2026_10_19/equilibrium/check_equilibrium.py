#!/usr/bin/env python3
"""Bounded deterministic TF and full GP/degenerate-baryon equilibrium controls.

This script checks stationarity, mass, virial and finite-box convergence. It does
not certify a continuum minimizer, its uniqueness, formation or orbital dynamics.
"""
import json
import math
import pathlib
import sys

import numpy as np
from scipy.integrate import solve_bvp, solve_ivp, simpson

HERE = pathlib.Path(__file__).resolve().parent
P = json.loads((HERE / "parameters.json").read_text())
OUT = pathlib.Path(sys.argv[1])
OUT.mkdir(parents=True, exist_ok=True)
K = P["K_scalar"]
KB = P["K_baryon"]
CB = 2.5 * KB


def tf(eta):
    # x=r/a, a^2=2K because 4*pi*G=1. h0=1.
    x0 = 1e-7
    q0 = 1 + eta
    y0 = [1 - q0*x0*x0/6, -q0*x0/3, x0**3/3, x0**3/3]
    def rhs(x, y):
        q = max(y[0], 0.)
        return [y[1], -2*y[1]/x - q - eta*q**1.5,
                x*x*q, x*x*q**1.5]
    def edge(x, y):
        return y[0]
    edge.terminal = True
    edge.direction = -1
    sol = solve_ivp(rhs, [x0, 4.], y0, events=edge, dense_output=True,
                    rtol=P["ODE_tolerance"], atol=2e-13, max_step=0.025)
    assert sol.success and len(sol.t_events[0]) == 1
    x1 = float(sol.t_events[0][0])
    y1 = sol.y_events[0][0]
    # 4*pi factors cancel from a common virial and mass check.
    grid = np.linspace(x0, x1, 4001)
    th, thp, id_, ib_ = sol.sol(grid)
    th = np.maximum(th, 0.)
    rho_d = th / (2*K)
    # eta may be varied as a dimensionless ODE parameter, equivalently KB varies.
    rho_b = eta * th**1.5 / (2*K)
    mass = id_ + eta*ib_
    a = math.sqrt(2*K)
    # h0=1, U=mu-h, mu=-M/R where mass in Poisson units.
    mu = -float((y1[2] + eta*y1[3]) / x1)
    U = mu - th
    S = simpson(K*rho_d**2 * grid**2, x=grid) * a**3
    # hb=h implies internal baryon energy = (3/5)rho_b*h.
    B = simpson(0.6*rho_b*th * grid**2, x=grid) * a**3
    W = 0.5*simpson((rho_d+rho_b)*U * grid**2, x=grid) * a**3
    result = {"eta": eta, "x1": x1, "radial_scalar_mass": float(y1[2])*a**3/(2*K),
              "radial_baryon_mass": float(eta*y1[3])*a**3/(2*K),
              "mu": mu, "mass_flux_residual": float(abs(-x1*x1*y1[1] - y1[2] - eta*y1[3])),
              "TF_virial_relative_residual": float(abs(3*S+2*B+W)/abs(W)),
              "scalar_internal": S, "baryon_internal": B, "gravity": W}
    if eta == 0:
        result["n1_radius_error"] = abs(x1-math.pi)
        result["n1_mass_error"] = abs(float(y1[2])-math.pi)
        assert result["n1_radius_error"] < 1e-8
        assert result["n1_mass_error"] < 1e-7
    assert result["mass_flux_residual"] < 1e-8
    assert result["TF_virial_relative_residual"] < 1e-7
    return result, sol


tf_rows = []
tf_seed = None
for eta in P["TF_etas"]:
    row, sol = tf(eta)
    tf_rows.append(row)
    if eta == 1:
        tf_seed = (row, sol)
seed, seed_sol = tf_seed
ND = seed["radial_scalar_mass"]
NB = seed["radial_baryon_mass"]


def gp(tau, L, tol, guess=None):
    r = np.linspace(0., L, 201)
    if guess is None:
        inner = np.minimum(np.maximum(r, 1e-7), seed["x1"])
        th, thp, id_, ib_ = seed_sol.sol(inner)
        # Smooth initial scalar surface; the BVP determines the final tail.
        u = np.sqrt(np.maximum(th, 0.) + 0.002*np.exp(-r))
        up = np.gradient(u, r)
        mu = seed["mu"]
        pot = np.where(r < seed["x1"], mu-th, -(ND+NB)/np.maximum(r, 1e-6))
        potp = np.gradient(pot, r)
        ids = np.minimum(id_, ND)
        ibs = np.minimum(ib_, NB)
        ids[0] = ibs[0] = 0.
        y = np.array([u, up, pot, potp, ids, ibs])
        par = np.array([mu+0.05, mu])
    else:
        y = guess.sol(r)
        par = guess.p.copy()
    def rhs(r, y, par):
        u, up, U, Up, id_, ib_ = y
        b = np.maximum((par[1]-U)/CB, 0.)**1.5
        return np.array([up, (2*K*u*u + U-par[0])*u/tau,
                         Up, u*u+b, r*r*u*u, r*r*b])
    def bc(y0, yL, par):
        return np.array([y0[1], y0[3], y0[4], y0[5], yL[0],
                         yL[2]+L*yL[3], yL[4]-ND, yL[5]-NB])
    S_matrix = np.zeros((6, 6))
    S_matrix[1, 1] = -2.
    S_matrix[3, 3] = -2.
    sol = solve_bvp(rhs, bc, r, y, p=par, S=S_matrix, tol=tol,
                    bc_tol=tol*0.1, max_nodes=7000)
    assert sol.success, (tau, L, tol, sol.message)
    r = np.linspace(0., L, 6001)
    u, up, U, Up, id_, ib_ = sol.sol(r)
    d = u*u
    b = np.maximum((sol.p[1]-U)/CB, 0.)**1.5
    T = simpson(tau*up*up*r*r, x=r)
    E_d = simpson(K*d*d*r*r, x=r)
    E_b = simpson(1.5*KB*b**(5/3)*r*r, x=r)
    W = 0.5*simpson((d+b)*U*r*r, x=r)
    # A finite Dirichlet box has a surface virial term; it is negligible here.
    vir = 2*T + 3*E_d + 2*E_b + W
    b_edge_idx = np.flatnonzero(b > 0)
    b_edge = float(r[b_edge_idx[-1]])
    # Direct baryon cutoff equation, independent of sampled edge.
    from scipy.optimize import brentq
    b_edge_root = brentq(lambda rr: sol.sol(rr)[2]-sol.p[1], 0., L)
    scalar_rms = math.sqrt(simpson(r**4*d, x=r)/ND)
    baryon_rms = math.sqrt(simpson(r**4*b, x=r)/NB)
    overlap = simpson(d*b*r*r, x=r)
    # Restricted rigid relative translation curvature, NOT a normal-mode frequency.
    omega_rigid_sq = ((ND+NB)/(3*ND*NB))*overlap
    bc_res = float(np.max(np.abs(bc(sol.y[:,0], sol.y[:,-1], sol.p))))
    norm_d = float(simpson(r*r*d, x=r))
    norm_b = float(simpson(r*r*b, x=r))
    row = {"tau": tau, "L": L, "tol": tol, "bvp_nodes": len(sol.x),
           "max_reported_rms_residual": float(np.max(sol.rms_residuals)),
           "boundary_residual": bc_res, "mu_d": float(sol.p[0]), "mu_b": float(sol.p[1]),
           "central_scalar_density": float(d[0]), "central_baryon_density": float(b[0]),
           "radial_scalar_mass": norm_d, "radial_baryon_mass": norm_b,
           "mass_relative_error": max(abs(norm_d-ND)/ND, abs(norm_b-NB)/NB),
           "baryon_radius": b_edge_root, "scalar_rms": scalar_rms, "baryon_rms": baryon_rms,
           "T": float(T), "scalar_internal": float(E_d), "baryon_internal": float(E_b),
           "gravity": float(W), "energy": float(T+E_d+E_b+W),
           "virial_relative_residual": float(abs(vir)/abs(W)),
           "finite_box_surface_virial_estimate": float(tau*L**3*up[-1]**2),
           "rigid_relative_omega_sq": float(omega_rigid_sq),
           "homology_second_variation": float(2*(T+E_b)+6*E_d)}
    assert bc_res < tol
    assert row["mass_relative_error"] < 2e-6
    assert row["virial_relative_residual"] < 2e-5
    assert np.min(u[:-1]) > -1e-8
    profile_r = np.linspace(0., L, P["output_profile_samples"])
    profile = sol.sol(profile_r)
    profile_d = profile[0]**2
    profile_b = np.maximum((sol.p[1]-profile[2])/CB, 0.)**1.5
    record = {"r": profile_r.tolist(), "rho_d": profile_d.tolist(),
              "rho_b": profile_b.tolist(), "U": profile[2].tolist(),
              "u": profile[0].tolist(), "u_prime": profile[1].tolist()}
    return row, record, sol


gp_rows = []
profiles = {}
for tau in P["GP_taus"]:
    previous = None
    for L, tol in zip(P["GP_box_radii"], P["bvp_tolerances"]):
        row, prof, previous = gp(tau, L, tol, previous)
        gp_rows.append(row)
        profiles[f"tau={tau};L={L};tol={tol}"] = prof
    coarse, fine = gp_rows[-2:]
    assert abs(coarse["energy"]-fine["energy"])/abs(fine["energy"]) < 1e-4
    assert abs(coarse["mu_d"]-fine["mu_d"]) < 1e-4
    assert abs(coarse["mu_b"]-fine["mu_b"]) < 1e-4

result = {"finite_assertion": "Four TF central-ratio profiles and six full coupled GP/baryon stationary BVPs pass the explicit mass, residual, virial, pure-n1 and two-box comparisons in this script.",
          "interpretation": "Numerical stationarity and selected finite controls only. Global continuum energetic-minimum existence is a separate analytic result; BVP output is not a certified identification of that minimizer.",
          "TF": tf_rows, "fixed_radial_masses": {"scalar": ND, "baryon": NB},
          "GP": gp_rows, "randomness": "none"}
(OUT / "results.json").write_text(json.dumps(result, indent=2) + "\n")
(OUT / "profiles.json").write_text(json.dumps(profiles, separators=(",", ":")) + "\n")
print(json.dumps({"TF_cases": len(tf_rows), "GP_cases": len(gp_rows),
                  "max_GP_virial_relative_residual": max(r["virial_relative_residual"] for r in gp_rows),
                  "max_GP_mass_relative_error": max(r["mass_relative_error"] for r in gp_rows)}))
