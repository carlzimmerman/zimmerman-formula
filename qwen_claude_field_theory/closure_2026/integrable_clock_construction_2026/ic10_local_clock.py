#!/usr/bin/env python3
"""IC10: full kinetic alignment and algebraic, local clock on eta=1.

The global action is specified in IC10_LOCAL_CLOCK.md. This computation tests
its vacuum expanding plateau, NOT its transition, PPN or galactic branch.
Fixed units m=h0=1,kappa=6; original exponential U and constants unchanged.
"""
import argparse
from functools import lru_cache
import json
import mpmath as mp
import sympy as s
import ic8_shear_integrability as ingredients


@lru_cache(None)
def build():
    old = ingredients.build()
    xi, u, rho = old["xi"], old["u"], old["rho"]
    C = s.simplify((old["htrace"]+s.exp((4-3*u)*xi)*rho**2/3
                    +3*s.exp((3*u-4)*xi))/s.exp((3*u-2)*xi))
    S, w = s.symbols("S w", real=True)
    X = s.exp(-2*S)/2
    u_of_Sw = (S+2*w)/(S+w)
    P = -s.exp(4*w)*C.subs(u, u_of_Sw)+6*s.exp(2*w)*X
    derivatives = s.Matrix([P, s.diff(P, w), s.diff(P, S), s.diff(P, w, 2),
                            s.diff(P, S, w), s.diff(P, S, 2)])
    evaluate = s.lambdify((S, w), derivatives, "mpmath", cse=True)
    return dict(S=S, w=w, P=P, X=X, C=C, u=u_of_Sw, evaluate=evaluate)


def state(S):
    S = mp.mpf(S)
    evaluate = build()["evaluate"]
    # Explicit interior secant seeds: mpmath's default +0.25 second seed
    # hits w=0,u=1 at S=1, the logarithmic boundary rather than this branch.
    w = mp.findroot(lambda w: evaluate(S, w)[1], (-S/4, -S/5),
                    tol=mp.power(10, -mp.mp.dps+10))
    if abs(mp.im(w)) > mp.power(10, -mp.mp.dps+10):
        raise ValueError("No real auxiliary root on this continuation")
    w = mp.re(w)
    u = (S+2*w)/(S+w)
    if not 0 < u < 1:
        raise ValueError("Auxiliary root outside the specified action chart")
    P, Pw, PS, Pww, PSw, PSS = evaluate(S, w)
    X, mstar = mp.exp(-2*S)/2, mp.exp(-mp.mpf(1)/6)
    PSS_effective = PSS-PSw*PSw/Pww
    PX = -PS/(2*X)
    kinetic = (PSS_effective+PS)/(2*X)
    bare_kinetic = (PSS+PS)/(2*X)
    speed_squared = PX/kinetic
    energy = -PS-P
    H = mp.sqrt(energy/(3*mstar)) if energy > 0 else mp.nan
    wS = -PSw/Pww
    physical_H = mp.exp(-w)*H*(1+3*speed_squared*wS)
    # p_w=0, C_w=H_w=-V P_w; differentiate at fixed p_T, NOT fixed X.
    auxiliary_schur = Pww-PSw*PSw/(PSS+PS)
    bracket = mp.matrix([[0, auxiliary_schur], [-auxiliary_schur, 0]])
    J = mp.exp(-2*w-mp.mpf(1)/6)
    return dict(S=S, w=w, u=u, P=P, PS=PS, PSS_effective=PSS_effective, X=X,
                PX=PX, kinetic=kinetic, bare_kinetic=bare_kinetic,
                speed_squared=speed_squared, energy=energy, H=H, physical_H=physical_H,
                constraint=Pw, auxiliary_bracket=bracket, auxiliary_schur=auxiliary_schur,
                constraint_schur_identity=auxiliary_schur-Pww*kinetic/bare_kinetic,
                activation_r=mp.exp(S)*J*H, clock_charge_density=PX*mp.sqrt(2*X),
                friedmann_residual=3*mstar*H*H-energy)


def evolve(start="0.1", end="0.2"):
    """Integrate the vacuum FLRW equations using S as monotone time.

    dS/dtau=3 H cs²; dln(barA)/dS=1/(3 cs²). No fitted expansion
    history, dust approximation, or k!=0-to-k=0 substitution is used.
    """
    start, end = mp.mpf(start), mp.mpf(end)
    a, b = state(start), state(end)
    efolds = mp.quad(lambda S: 1/(3*state(S)["speed_squared"]), [start, end])
    proper_time = mp.quad(lambda S: 1/(3*state(S)["H"]*state(S)["speed_squared"]), [start, end])
    return dict(barred_efolds=efolds, physical_efolds=efolds+b["w"]-a["w"],
                proper_time=proper_time,
                charge_ratio=mp.exp(3*efolds)*b["clock_charge_density"]/a["clock_charge_density"],
                friedmann_residual=b["friedmann_residual"])


def plateau_boundary():
    """First upper eta=1 boundary found on this local continuation.

    Outside it the plateau pressure is not the full candidate action.
    """
    S = mp.findroot(lambda S: state(S)["activation_r"]**2-mp.mpf(5)/4,
                    (mp.mpf("0.2"), mp.mpf("0.3")))
    return state(S)


@lru_cache(None)
def identities():
    m, J, p, q, pt, qt = s.symbols("m J p q pt qt", nonzero=True)
    phase = 2*pt*qt+2*p*q/3-(2*pt**2-p*p/3)/(m*J)
    stationary = {pt: m*J*qt/2, p: -m*J*q}
    w, Ktf2, Ktrace, R = s.symbols("w Ktf2 Ktrace R", real=True)
    compact = m*s.exp(4*w)*s.exp(-2*w-s.Rational(1, 6))*s.exp(-2*w)*(Ktf2-2*Ktrace**2/3+R)/2
    Einstein = m*s.exp(-s.Rational(1, 6))*(Ktf2-2*Ktrace**2/3+R)/2
    PS, PSS, PSw, Pww, X = s.symbols("PS PSS PSw Pww X", nonzero=True)
    eff = PSS-PSw**2/Pww
    kinetic, bare = (eff+PS)/(2*X), (PSS+PS)/(2*X)
    # Spatial Hamiltonian bracket: H_p=v, H_{T_i}=V P_X h^ij T_j,
    # p_T=V P_X v, yielding the spatial momentum density exactly.
    V, PX, v, Ti = s.symbols("V PX v Ti", nonzero=True)
    return {
        "trace_EL": s.simplify(s.diff(phase, p).subs(stationary)),
        "tensor_EL": s.simplify(s.diff(phase, pt).subs(stationary)),
        "full_kinetic_Legendre": s.simplify(phase.subs(stationary)-m*J*(qt**2-2*q*q/3)/2),
        "conformal_Einstein_ADM_density": s.simplify(compact-Einstein),
        "fixed_momentum_auxiliary_Schur": s.factor(Pww-PSw**2/(PSS+PS)-Pww*kinetic/bare),
        "clock_charge_FLRW_identity": s.factor(1+eff/PS-kinetic/ (PS/(2*X))),
        "clock_Hamiltonian_spatial_bracket": s.expand(v*(V*PX*Ti)-(V*PX*v)*Ti),
    }


def report():
    mp.mp.dps = 60
    rows = []
    for value in ("0.1", "0.15", "0.2", "0.5", "1"):
        bg = state(value)
        _, singular, _ = mp.svd(bg["auxiliary_bracket"])
        row = {key: mp.nstr(bg[key], 24) for key in
               ("S", "w", "u", "PX", "kinetic", "speed_squared", "energy", "physical_H", "activation_r", "constraint")}
        row["auxiliary_rank_at_tolerance_1e-40"] = sum(abs(v) > mp.mpf("1e-40") for v in singular)
        row["inside_eta_one"] = abs(bg["activation_r"]**2-1) <= mp.mpf(1)/4
        rows.append(row)
    boundary = plateau_boundary()
    return dict(candidate="IC10", full_theory="OPEN", exact_checks={k: s.simplify(v) == 0 for k, v in identities().items()},
                action_clock_pressure=str(build()["P"]), samples=rows,
                finite_FLRW={k: mp.nstr(v, 30) for k, v in evolve().items()},
                next_plateau_boundary={k: mp.nstr(boundary[k], 24) for k in ("S", "u", "activation_r", "speed_squared")},
                nonclaims=["Only the eta=1 vacuum action is reduced to Einstein plus a local clock",
                           "No global Dirac, matter-coupled causality or transition certificate",
                           "No all-time cosmology or strong-coupling cutoff determination",
                           "No AQUAL, lensing, PPN, measured-G, k=0/y=0 global matching or novelty claim"])


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--require-full-closure", action="store_true")
    args = parser.parse_args()
    result = report()
    print(json.dumps(result, indent=2))
    if not all(result["exact_checks"].values()):
        return 1
    return 2 if args.require_full_closure else 0


if __name__ == "__main__":
    raise SystemExit(main())
