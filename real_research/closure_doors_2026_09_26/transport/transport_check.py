#!/usr/bin/env python3
"""Bounded same-clock DBI transport audit; no imported research lane is executed.

One canonical pair (Theta,rho), S=int[rho Theta_t-rho Theta_x^2/2-U(rho)].
The numerical coordinate is fluid mass, not a new material species. Stop at
nonpositive cell Jacobian: the continued mass-coordinate wave is then outside
the single-clock positive-density domain.
"""
import argparse
import json
import math
import pathlib
import platform
import time

import numpy as np
import sympy as s


def exact_identities():
    rho, kap, lam, u, tau = s.symbols("rho kappa lambda u tau", positive=True)
    U = (s.sqrt(kap**2 + lam * rho**2) - kap) / lam
    UU = s.diff(U, rho, 2)
    assert s.simplify(UU - kap**2 / (kap**2 + lam * rho**2)**s.Rational(3, 2)) == 0
    # Constitutive equation inverted without allowing a negative square-root branch.
    u_of_rho = rho / s.sqrt(kap**2 + lam * rho**2)
    K = kap / lam * (1 - s.sqrt(1 - lam * u**2))
    assert s.simplify(s.diff(K, u).subs(u, u_of_rho) - rho) == 0
    assert s.simplify(s.diff(U, rho) - u_of_rho) == 0
    e = (s.sqrt(kap**2 * tau**2 + lam) - kap * tau) / lam
    assert s.simplify(tau * U.subs(rho, 1 / tau) - e) == 0
    assert s.simplify(s.diff(e, tau, 2) - kap**2 / (kap**2 * tau**2 + lam)**s.Rational(3, 2)) == 0
    eta = s.symbols("eta", positive=True)
    en = (s.sqrt(1 + eta**2 * tau**2) - 1) / eta**2
    assert s.simplify(s.diff(en, tau, 2) - (1 + eta**2 * tau**2)**(-s.Rational(3, 2))) == 0
    m, t, V = s.symbols("m t V", real=True)
    X = m - V * s.sin(m) * s.sin(t)
    jac = s.diff(X, m)
    vel = s.diff(X, t)
    assert s.simplify(s.diff(X, t, 2) - s.diff(X, m, 2)) == 0
    local_energy = vel**2 / 2 + jac**2 / 2
    energy = s.integrate(s.expand_trig(local_energy), (m, 0, 2 * s.pi))
    assert s.simplify(energy - 2 * s.pi * (s.Rational(1, 2) + V**2 / 4)) == 0
    # Same-state first two moments do not determine collisionless stress.
    a, b, va, vb = s.symbols("a b va vb", real=True)
    variance_numerator = (a + b) * (a * va**2 + b * vb**2) - (a * va + b * vb)**2
    assert s.factor(variance_numerator - a * b * (va - vb)**2) == 0
    # Homogeneous quadratic vs bounded DBI, each with n=J/a^3.
    n, Q0 = s.symbols("n Q0", positive=True)
    quadratic_energy = Q0 * n + n**2 / (2 * kap)
    dbi_energy = Q0 * n + (s.sqrt(kap**2 + lam * n**2) - kap) / lam
    dbi_pressure = n * s.diff(dbi_energy, n) - dbi_energy
    assert s.simplify(s.limit(dbi_energy / n, n, s.oo) - Q0 - 1 / s.sqrt(lam)) == 0
    assert s.limit(dbi_pressure / dbi_energy, n, s.oo) == 0
    assert s.limit((n * s.diff(quadratic_energy, n) - quadratic_energy) / quadratic_energy, n, s.oo) == 1
    return {
        "symbolic_checks": 12,
        "U": str(U), "U_second_derivative": str(UU),
        "mass_coordinate_energy": str(e),
        "normalized_energy_second_derivative": "(1+eta^2*tau^2)^(-3/2)",
        "chaplygin_exact_solution": str(X),
        "exact_energy": "2*pi*(1/2+V^2/4)",
        "moment_obstruction": "rho*(Pi-j^2/rho)=a*b*(va-vb)^2",
        "homogeneous_quadratic_w_limit": 1,
        "homogeneous_bounded_DBI_w_limit": 0,
    }


def evolve(N, eta, mach, cfl=0.4, end=2 * np.pi):
    dx = 2 * np.pi / N
    m = np.arange(N) * dx
    disp = np.zeros(N)
    vel = -mach * np.sin(m)
    # Exact kinetic-flow / potential-flow splitting (velocity Verlet).
    # Sound speed in mass coordinates <=1, so cfl<1 controls the linear limit.
    dt0 = cfl * dx
    steps = int(np.ceil(end / dt0))
    dt = end / steps

    def jac(u):
        return 1 + (np.roll(u, -1) - u) / dx

    def energy(u, v):
        q = jac(u)
        internal = q * q / (np.sqrt(1 + eta * eta * q * q) + 1)
        return float(dx * np.sum(0.5 * v * v + internal))

    def acc(u):
        q = jac(u)
        ep = q / np.sqrt(1 + eta * eta * q * q)
        return (ep - np.roll(ep, 1)) / dx

    E0 = energy(disp, vel)
    eerr, perr, minjac, uerr, verr = 0., 0., 1., 0., 0.
    previous_min = 1.
    event = None
    t = 0.
    for step in range(steps):
        vel += .5 * dt * acc(disp)
        disp += dt * vel
        vel += .5 * dt * acc(disp)
        t = (step + 1) * dt
        qmin = float(jac(disp).min())
        eerr = max(eerr, abs(energy(disp, vel) / E0 - 1))
        perr = max(perr, abs(float(dx * vel.sum())))
        minjac = min(minjac, qmin)
        if eta == 0:
            uerr = max(uerr, float(np.max(abs(disp + mach * np.sin(m) * np.sin(t)))))
            verr = max(verr, float(np.max(abs(vel + mach * np.sin(m) * np.cos(t)))))
        if qmin <= 0:
            event = t - dt + dt * previous_min / (previous_min - qmin)
            break
        previous_min = qmin
    return dict(N=N, eta=eta, mach=mach, cfl=cfl, dt=dt, steps=step + 1,
                elapsed_dimensionless_time=t, first_zero_jacobian_interpolated=event,
                min_jacobian=minjac, relative_energy_drift=eerr,
                absolute_momentum_drift=perr, exact_displacement_linf=uerr,
                exact_velocity_linf=verr,
                mass=2 * np.pi, mass_note="Exactly fixed by periodic mass-coordinate domain; not a fitted quantity",
                physical_domain="Stopped at first nonpositive edge Jacobian" if event else "All sampled edge Jacobians positive")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    started = time.monotonic()
    symbolic = exact_identities()
    # Exact-solution spatial refinement, one complete acoustic period.
    benchmark = [evolve(N, 0., .5) for N in (64, 128, 256, 512)]
    orders = [math.log(benchmark[i]["exact_displacement_linf"] /
                      benchmark[i+1]["exact_displacement_linf"], 2) for i in range(3)]
    assert min(orders) > 1.9
    assert max(x["relative_energy_drift"] for x in benchmark) < 2e-4
    # Full nonlinear shifted DBI; positive- and high-Mach branches.
    full = [evolve(N, eta, mach) for eta in (.1, .25, .5)
            for mach in (.5, 2.) for N in (128, 256, 512)]
    for r in full:
        assert r["relative_energy_drift"] < 2e-4
        assert r["absolute_momentum_drift"] < 1e-11
        assert (r["first_zero_jacobian_interpolated"] is not None) == (r["mach"] == 2.)
    # Independent time-step refinement on one nonlinear collapsing branch.
    timestep = [evolve(512, .25, 2., cfl=c) for c in (.4, .2, .1)]
    event_spread = max(r["first_zero_jacobian_interpolated"] for r in timestep) - min(r["first_zero_jacobian_interpolated"] for r in timestep)
    assert event_spread < 2e-5
    # Exact cold-limit crossing; no continuation into negative-density branch.
    exact_crossing = [dict(mach=M, t_cross=math.asin(1/M), ballistic_cross=1/M,
                          relative_delay=M*math.asin(1/M)-1) for M in (2., 4., 8., 16.)]
    # Same rho and j but arbitrary stress: rho=1,j=0, counterstreams +-V.
    moment_examples = [dict(rho=1., current=0., speed=V, stress=V*V) for V in (0., 1., 2.)]
    output = dict(result="Exact cold-limit obstruction plus finite-range verified nonlinear DBI transport",
                  symbolic=symbolic, benchmark=benchmark, measured_spatial_orders=orders,
                  nonlinear=full, timestep_refinement=timestep, event_time_spread=event_spread,
                  exact_cold_limit_crossing=exact_crossing, same_state_different_stress=moment_examples,
                  exact_subcritical_bound="For 0<=M<1, tau>=1-M>0 for all m,t in exact eta=0 model",
                  exact_rebound="At t=pi: X=m and v=+M sin(m), opposite its initial velocity",
                  nonlinear_domain="eta=0.1,0.25,0.5; Mach=0.5,2; N=128,256,512; t<=2pi",
                  non_claims=["No full covariant or coupled gravity action is certified", "Finite-eta runs do not prove all-data/global well-posedness", "A positive canonical Hessian does not guarantee global invertibility of the fluid map", "No extra complex wave field or particle species was introduced", "Does not show DBI passes CMB, halo clearing, lensing, or merger observations", "A barotropic pressure cannot reproduce arbitrary collisionless multistream stresses from density/current alone"],
                  software=dict(python=platform.python_version(),numpy=np.__version__,sympy=s.__version__),
                  runtime_seconds=time.monotonic()-started)
    target = pathlib.Path(args.output)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(output, indent=2)+"\n")
    print(json.dumps({"result":output["result"],"runtime_seconds":output["runtime_seconds"],
                      "spatial_orders":orders,"event_time_spread":event_spread,
                      "worst_energy_drift":max(r["relative_energy_drift"] for r in benchmark+full+timestep),
                      "full_DBI_Mach2_finest":[r for r in full if r["N"]==512 and r["mach"]==2.]},indent=2))


if __name__ == "__main__":
    main()
