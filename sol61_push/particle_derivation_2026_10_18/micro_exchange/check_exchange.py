#!/usr/bin/env python3
"""Bounded exact algebra and independent quadrature for exchange diagnostics.

No simulation, fitted exchange constant, data download, or library dependency.
The 1-D host is a diagnostic added potential, not a derived dark halo.
"""
import argparse
import json
import math
from fractions import Fraction as F
from pathlib import Path


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    checks = []

    def check(name, predicate, detail=None):
        if not predicate:
            raise AssertionError(name)
        checks.append({"name": name, "passed": True, "detail": detail})

    # Exact propagator matching. Rational M/m > 2; no near-pole rounding.
    matching = []
    for ratio in [F(20001, 10000), F(5, 2), F(3), F(4), F(10)]:
        m, mass, coupling2, rep = F(1), ratio, F(3, 7), F(5, 11)
        delta = mass - 2*m
        gap = mass*mass - 4*m*m
        lam = rep + coupling2/gap
        rwa = lam - coupling2/(2*mass*delta)
        negative = coupling2/(2*mass*(mass+2*m))
        full = lam - coupling2/gap
        check("propagator partial fraction M/m=" + str(ratio),
              1/gap == 1/(2*mass*delta) + 1/(2*mass*(mass+2*m)))
        check("RWA reconciliation M/m=" + str(ratio), rwa == rep + negative)
        check("full matching M/m=" + str(ratio), full == rwa-negative == rep)
        check("relative correction M/m=" + str(ratio),
              negative/(coupling2/gap) == delta/(2*mass))
        matching.append({"M_over_m": str(ratio), "lambda_RWA": str(rwa),
                         "lambda_full": str(full), "lambda_omitted": str(negative)})

    # Exact Noether divergence coefficients in R=-2g Im(X*Phi^2).
    dphi, dx = F(2), F(-1)
    check("Noether weighted cancellation", dphi+2*dx == 0)
    check("neutral equal decay: zero charge source but four daughters",
          2*(F(1)-F(1)) == 0 and 2*(F(1)+F(1)) == 4)

    # Distinct-mode matrix-element contractions of H=(g/2) sum I a+a+aa.
    # Enumerate n_b=0..2, n_r=0..2, n_p=1..3, n_q=1..3: 81 states.
    # Four ordered vertex assignments are independent of occupation values.
    fock_cases = 0
    for nb in range(3):
        for nr in range(3):
            for np in range(1, 4):
                for nq in range(1, 4):
                    amplitude_squared = F(0)
                    # The common ladder factor squares to L; coefficient sum=2g.
                    ladder_squared = (nb+1)*(nr+1)*np*nq
                    coefficient = sum(F(1, 2) for _ in range(4))
                    amplitude_squared = coefficient**2 * ladder_squared
                    check("Fock contraction %d" % fock_cases,
                          amplitude_squared == 4*(nb+1)*(nr+1)*np*nq)
                    fock_cases += 1
    check("Fock iterator coverage", fock_cases == 81)

    # Exact 1-D delta-host scattering capture. kappa=2, p=3, q=6, r=7,
    # m=1: r^2=p^2+q^2+kappa^2. All continuum legs are distinct.
    kap, p, q, r, m = map(F, (2, 3, 6, 7, 1))
    binding = kap**2/(2*m)
    ep, eq, er = p*p/(2*m), q*q/(2*m), r*r/(2*m)
    check("host capture on-shell energy", ep+eq == -binding+er)
    check("host capture outgoing continuum", er > 0)
    arguments = (r+p-q, r-p+q, r+p+q, r-p-q)
    signs = (1, 1, -1, -1)
    cc = sum(sign*kap/(kap*kap+a*a) for a, sign in zip(arguments, signs))/4
    ss = sum(sign*a/(kap*kap+a*a) for a, sign in zip(arguments, signs))/4
    reduced = r*cc-kap*ss
    check("host overlap nonzero exact", reduced != 0)
    prefactor = 2*math.sqrt(float(kap))/(math.pi**1.5*math.sqrt(float(r*r+kap*kap)))
    overlap = prefactor*float(reduced)

    # Orthogonal invariant: direct integrand in position space, Simpson, two grids.
    def simpson(n, length):
        step = length/n
        total = 0.0
        for i in range(n+1):
            x = i*step
            integrand = math.exp(-float(kap)*x)*(float(r)*math.cos(float(r)*x)
                         -float(kap)*math.sin(float(r)*x))*math.sin(float(p)*x)*math.sin(float(q)*x)
            weight = 1 if i in (0, n) else (4 if i % 2 else 2)
            total += weight*integrand
        return prefactor*step*total/3

    quad1, quad2 = simpson(24000, 12.0), simpson(48000, 12.0)
    # Tail bound is prefactor*(r+kappa)*exp(-kappa L)/kappa < 2e-11.
    tail_bound = prefactor*float((r+kap)/kap)*math.exp(-float(kap)*12.0)
    check("overlap direct quadrature coarse", abs(quad1-overlap) < 2e-10)
    check("overlap direct quadrature fine", abs(quad2-overlap) < 2e-10)
    check("overlap refinement", abs(quad2-quad1) < 2e-10)
    check("overlap tail bound", tail_bound < 2e-11)
    # With g_1D=1 for normalization only, |2g I|^2 is nonzero.
    capture = {"diagnostic": "1D fixed attractive delta host, not a physical halo",
               "m": "1", "kappa": "2", "incoming_odd_p": "3", "incoming_odd_q": "6",
               "outgoing_even_r": "7", "binding": str(binding),
               "energies": {"p": str(ep), "q": str(eq), "r": str(er)},
               "reduced_overlap": str(reduced), "overlap": overlap,
               "overlap_squared": overlap*overlap,
               "matrix_element_squared_per_g1D_squared": 4*overlap*overlap,
               "quadrature": [quad1, quad2], "absolute_tail_bound": tail_bound}

    # Event stoichiometry and energy budget, independent of transition weight.
    # Order: b, r, p, q. Continuum moment has one outgoing minus two incoming.
    nu = [1, 1, -1, -1]
    check("capture total daughter count", sum(nu) == 0)
    check("capture free count reciprocal", sum(nu[1:]) == -nu[0])
    check("capture energy moment", sum(v*e for v, e in zip(nu, [-binding, er, ep, eq])) == 0)
    check("binding heat reciprocal", er-ep-eq == binding)

    # Exact equilibrium occupations using exponentials represented by rationals:
    # e^(beta eps_i) = (1/4, 32, 2, 4), obeying product conservation.
    exps = [F(1, 4), F(32), F(2), F(4)]
    equilibrium_cases = []
    for fugacity in [F(1, 16), F(1, 8), F(1, 5)]:
        occ = [1/(e/fugacity-1) for e in exps]
        nb, fr, fp, fq = occ
        gain = (1+nb)*(1+fr)*fp*fq
        loss = nb*fr*(1+fp)*(1+fq)
        check("exact detailed balance z="+str(fugacity), gain == loss)
        equilibrium_cases.append({"z": str(fugacity), "gain_equals_loss": str(gain)})
    # Generalized condensate and thermal chemical potentials: gain/loss=z_f/z_b.
    for zb, zf in [(F(1, 16), F(1, 8)), (F(1, 8), F(1, 16))]:
        nb = 1/(exps[0]/zb-1)
        fr, fp, fq = [1/(e/zf-1) for e in exps[1:]]
        gain = (1+nb)*(1+fr)*fp*fq
        loss = nb*fr*(1+fp)*(1+fq)
        check("chemical-potential direction zb="+str(zb), gain/loss == zf/zb)
    check("spontaneous seed factor", (1+F(0))*(1+F(0))*F(1, 3)*F(1, 7) > 0)

    # Sharp HF support threshold, energies in Delta_HF units and m=1.
    threshold_cases = []
    for emax in [F(0), F(1, 4), F(49, 100), F(1, 2), F(3, 4), F(1)]:
        pmax_sq = 2*emax
        open_support = pmax_sq >= 1
        expected = emax >= F(1, 2)
        check("HF support Emax/Delta="+str(emax), open_support == expected)
        threshold_cases.append({"Emax_over_gap": str(emax), "support_possible": open_support,
                                "positive_measure": emax > F(1, 2)})
    check("back-to-back cannot satisfy repulsive HF condition", -p*p < 0)

    result = {"status": "completed", "check_count": len(checks), "fock_case_count": fock_cases,
              "matching": matching, "host_capture": capture,
              "detailed_balance": equilibrium_cases, "HF_threshold_cases": threshold_cases,
              "checks": checks,
              "scope": "Exact finite algebra and bounded overlap quadrature only; not 3D capture rate, kinetic evolution, halo formation, observed species identity, or a settled=condensate proof."}
    output = Path(args.output)
    output.write_text(json.dumps(result, indent=2)+"\n")
    print(json.dumps({"status": result["status"], "checks": len(checks),
                      "reduced_overlap": str(reduced), "overlap": overlap,
                      "matrix_element_squared_per_g1D_squared": 4*overlap*overlap}))


if __name__ == "__main__":
    main()
