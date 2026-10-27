"""Conditional additive isolated-law baseline stress test; see BASELINE_EXTENSION.md."""
import importlib.util
import json
import math
import resource
import sys
from pathlib import Path

from scipy.integrate import quad

BASE = Path("sol61_push/cfg853_independent_transport_2026_10_19")
spec = importlib.util.spec_from_file_location("cfg853_compute", BASE / "compute.py")
c = importlib.util.module_from_spec(spec)
spec.loader.exec_module(c)


def main(destination):
    source = json.loads((BASE / "source_extraction.json").read_text())
    stockdata = json.loads((BASE / "run_002/results.json").read_text())
    sx = next(x for x in stockdata["four_dwarf_budget_cases"] if
              x["name"] == "Sextans" and x["mode"] == "original" and x["footing"] == "canonical")
    mstar = sx["Mstar_Msun"]
    pop = source["populations"]
    a1, a2 = [source["distance_kpc"]*1000*math.tan(math.radians(x["Rh_deg"])) for x in pop]
    fraction = pop[0]["fraction"]
    cases = []
    localchecks = []

    def check(label, condition):
        localchecks.append({"name": label, "pass": bool(condition)})
        if not condition:
            raise AssertionError(label)

    for footing, a0 in c.A0.items():
        for kernel in ["rational", "exponential"]:
            def gstar(r):
                return c.G_PC_KMS*mstar*sum(
                    f*r/(r*r+a*a)**1.5 for f, a in [(fraction,a1),(1-fraction,a2)])

            def g0(r):
                gn = gstar(r)
                if gn == 0:
                    return 0.0
                y = gn * 1e6/c.PC/a0
                nu = .5+math.sqrt(.25+1/y) if kernel == "rational" else -1/math.expm1(-math.sqrt(y))
                return gn*nu

            moments = []
            for a in [a1,a2]:
                val = quad(lambda x: a*x**3*(1+x*x)**-2.5*g0(a*x),
                           0, math.inf, epsabs=1e-9, epsrel=1e-10)[0]
                def compact(t):
                    x = t/(1-t)
                    return a*x**3*(1+x*x)**-2.5*g0(a*x)/(1-t)**2
                other = quad(compact, 0, 1, epsabs=1e-9, epsrel=1e-10)[0]
                check(footing+kernel+str(a)+" independent integration domains",
                      math.isclose(val,other,rel_tol=1e-9,abs_tol=1e-10))
                moments.append(val)
            residual = [p["sigma_kms"]**2-v for p,v in zip(pop,moments)]
            check(footing+kernel+" both residuals positive", min(residual)>0)
            floor = c.mass_floor(a1,a2,*map(math.sqrt,residual))
            check(footing+kernel+" finite positive-measure residual feasible", floor["finite_positive_measure_possible"])
            allowance = c.COLD_RATIO/c.FRET*mstar
            check(footing+kernel+" fails even whole cold stock allowance", floor["sharp_floor_Msun"]>allowance)
            check(footing+kernel+" outer-only floor fails whole cold stock allowance",
                  floor["single_tracer_floor_Msun"][1]>allowance)
            # Directly reconstruct the full two moments from the extremizing extra shell plus baseline.
            for a,p,v in zip([a1,a2],pop,moments):
                shell_extra = c.G_PC_KMS*floor["sharp_floor_Msun"]/(3*a) * (
                    1+(floor["saturating_shell_radius_pc"]/a)**2)**-1.5
                check(footing+kernel+str(a)+" full-moment shell closure",
                      math.isclose(v+shell_extra,p["sigma_kms"]**2,rel_tol=1e-10))
            cases.append({"footing":footing,"kernel":kernel,"baseline_second_moments_kms2":moments,
                          "extra_residual_second_moments_kms2":residual,
                          "extra_mass_bound":floor,"generous_extra_allowance_Msun":allowance,
                          "minimum_extra_mass_over_allowance":floor["sharp_floor_Msun"]/allowance,
                          "outer_only_extra_mass_over_allowance":floor["single_tracer_floor_Msun"][1]/allowance,
                          "meaning":"Baseline granted without charging its mass to stock; extra receives all cold stock"})
    result = {"checkpoint":"CFG853-20261019-A-baseline-extension","cases":cases,
              "checks":localchecks,"n_checks":len(localchecks),"all_checks_pass":all(x["pass"] for x in localchecks),
              "peak_rss_bytes_on_Darwin":resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
              "non_claims":["No matched observed virial moments","No backreacting or nonlinear extra-mass force tested",
                            "Stellar-mass mixture .63/.37 is assumed, not derived from selected number fractions or equal M/L alone",
                            "Old total M/L assumed","No formation or kinetic law"]}
    Path(destination).write_text(json.dumps(result,indent=2,allow_nan=False)+"\n")
    print(json.dumps({"checks":len(localchecks),"cases":cases},indent=2))


if __name__ == "__main__":
    main(sys.argv[1])
