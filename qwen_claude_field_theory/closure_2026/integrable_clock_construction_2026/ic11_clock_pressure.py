#!/usr/bin/env python3
"""IC11: activated convex pressure repair; bounded vacuum plateau only.

The complete phase-action lift and exact domain predicate are in
IC11_CLOCK_PRESSURE.md. This does not certify the activation transition.
"""
import argparse
from functools import lru_cache
import json
import mpmath as mp
import sympy as s
import ic10_local_clock as old


def eta(r):
    r = mp.mpf(r)
    d = (r*r-1)**2
    E = lambda t: mp.exp(-1/t) if t > 0 else mp.mpf(0)
    a, b = E(mp.mpf(1)/4-d), E(d-mp.mpf(1)/16)
    return a/(a+b)


def phase_delta(Xphysical, w, r):
    """Global Hamiltonian-density addition in m=h0=1 units."""
    return -eta(r)*mp.exp(-4*w)*mp.mpf(5)/64*(2*mp.exp(2*w)*Xphysical)**16


@lru_cache(None)
def build():
    data = old.build()
    S, w, X = data["S"], data["w"], data["X"]
    f = s.Rational(5, 64)*(2*X)**16
    P = data["P"]+f
    derivatives = s.Matrix([P, s.diff(P, w), s.diff(P, S), s.diff(P, w, 2),
                            s.diff(P, S, w), s.diff(P, S, 2)])
    return dict(S=S, w=w, X=X, P=P, f=f,
                evaluate=s.lambdify((S, w), derivatives, "mpmath", cse=True))


def state(S):
    S = mp.mpf(S)
    # Identical algebraic root follows from exact f_w=0, not an old Hubble fit.
    w = old.state(S)["w"]
    P, Pw, PS, Pww, PSw, PSS = build()["evaluate"](S, w)
    X, mstar = mp.exp(-2*S)/2, mp.exp(-mp.mpf(1)/6)
    eff = PSS-PSw**2/Pww
    PX, Q, Qbare = -PS/(2*X), (eff+PS)/(2*X), (PSS+PS)/(2*X)
    cs2, energy = PX/Q, -PS-P
    H = mp.sqrt(energy/(3*mstar)) if energy > 0 else mp.nan
    wS = -PSw/Pww
    physical_H = mp.exp(-w)*H*(1+3*cs2*wS)
    J = mp.exp(-2*w-mp.mpf(1)/6)
    r = mp.exp(S)*J*H
    A = Pww-PSw**2/(PSS+PS)
    plateau = bool(mp.mpf(3)/4 <= r*r <= mp.mpf(5)/4)
    healthy = bool(PX > 0 and Q >= PX and energy > 0 and physical_H > 0
                   and A != 0 and Qbare != 0)
    return dict(S=S, w=w, u=(S+2*w)/(S+w), X=X, P=P, PS=PS,
                PSS_effective=eff, PX=PX, kinetic=Q, bare_kinetic=Qbare,
                speed_squared=cs2, energy=energy, H=H, physical_H=physical_H,
                constraint=Pw, auxiliary_schur=A,
                constraint_schur_identity=A-Pww*Q/Qbare,
                activation_r=r, inside_eta_one=plateau,
                vacuum_healthy=healthy, admissible=plateau and healthy,
                clock_charge_density=PX*mp.sqrt(2*X),
                friedmann_residual=3*mstar*H*H-energy)


def plateau_boundaries():
    """Locate the two r^2=5/4 crossings bracketing the .03--.2 witness.

    Root solves do not establish that other disconnected plateaus cannot exist.
    """
    equation = lambda S: state(S)["activation_r"]**2-mp.mpf(5)/4
    return tuple(state(mp.findroot(equation, seeds)) for seeds in
                 ((mp.mpf(".01"), mp.mpf(".03")),
                  (mp.mpf(".2"), mp.mpf(".24"))))


def evolve(start=".03", end=".1"):
    start, end = mp.mpf(start), mp.mpf(end)
    lo, hi = plateau_boundaries()
    if not lo["S"] < start < end < hi["S"]:
        raise ValueError("Integration must stay inside the identified plateau")
    a, b = state(start), state(end)
    efolds = mp.quad(lambda S: 1/(3*state(S)["speed_squared"]), [start, end])
    time = mp.quad(lambda S: 1/(3*state(S)["H"]*state(S)["speed_squared"]), [start, end])
    return dict(barred_efolds=efolds, physical_efolds=efolds+b["w"]-a["w"],
                proper_time=time,
                charge_ratio=mp.exp(3*efolds)*b["clock_charge_density"]/a["clock_charge_density"])


def identities():
    X, w = s.symbols("X w", positive=True)
    f = s.Rational(5, 64)*(2*X)**16
    # X here denotes tilde X; the physical argument is exp(-2w) X.
    lifted = s.exp(-4*w)*f.subs(X, s.exp(2*w)*X)
    S = s.symbols("S", real=True)
    fS = f.subs(X, s.exp(-2*S)/2)
    linear = s.symbols("a")*X
    return dict(
        conformal_phase_lift=s.simplify(s.exp(4*w)*lifted.subs(X, s.exp(-2*w)*X)-f),
        auxiliary_root_unchanged=s.diff(f, w),
        pressure_gradient=s.diff(f, X)-s.Rational(5, 2)*(2*X)**15,
        pressure_kinetic=s.diff(f, X)+2*X*s.diff(f, X, 2)-s.Rational(155, 2)*(2*X)**15,
        pressure_energy=2*X*s.diff(f, X)-f-31*f,
        S_derivative=s.diff(fS, S)+32*fS,
        S_second_derivative=s.diff(fS, S, 2)-1024*fS,
        linear_cannot_change_cone_gap=2*X*s.diff(linear, X, 2),
    )


def report():
    mp.mp.dps = 55
    fields = ("S", "PX", "kinetic", "speed_squared", "energy", "physical_H", "activation_r")
    rows = []
    for S in (".0001", ".001", ".01", ".03", ".05", ".1", ".2", ".24"):
        bg = state(S)
        rows.append({**{k: mp.nstr(bg[k], 24) for k in fields},
                     "inside_eta_one": bg["inside_eta_one"], "admissible": bg["admissible"]})
    scan = [state(mp.mpf(".0001")+mp.mpf(".4999")*i/500) for i in range(501)]
    active = [bg for bg in scan if bg["inside_eta_one"]]
    return dict(candidate="IC11 convex pressure only", full_theory="OPEN",
                exact_checks={k: s.simplify(v) == 0 for k, v in identities().items()},
                samples=rows,
                plateau_crossings=[{k: mp.nstr(bg[k], 24) for k in fields}
                                   for bg in plateau_boundaries()],
                finite_scan=dict(S_min=".0001", S_max=".5", samples=501,
                                 eta_one_samples=len(active),
                                 unhealthy_eta_one_samples=sum(not bg["vacuum_healthy"] for bg in active)),
                FLRW={k: mp.nstr(v, 30) for k, v in evolve().items()},
                nonclaims=["No global exclusion of additional disconnected plateau components",
                           "Excluded pressure-continuation states are not solutions of the transition action",
                           "No matter-coupled cone, transition Dirac rank, or strong-coupling certificate",
                           "No baryon-only MOND, slip/PPN, measured G, realistic cosmology or full closure"])


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--require-full-closure", action="store_true")
    args = parser.parse_args()
    result = report()
    print(json.dumps(result, indent=2))
    if not all(result["exact_checks"].values()) or result["finite_scan"]["unhealthy_eta_one_samples"]:
        return 1
    return 2 if args.require_full_closure else 0


if __name__ == "__main__":
    raise SystemExit(main())
