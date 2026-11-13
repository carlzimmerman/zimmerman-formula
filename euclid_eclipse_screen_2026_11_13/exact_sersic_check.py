"""Audit PS lensing approximation against Abel deprojection and adaptive LOS.

This is a numerical screen audit, not a screened-v3s fit or an exclusion test.
Run: python3 exact_sersic_check.py --output exact_sersic_check.json
"""
import argparse
import importlib.util
import json
import math
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.integrate import quad
from scipy.special import gammainc, gammaincinv, gammaln

ROOT = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("eclipse_screen", ROOT / "screen.py")
screen = importlib.util.module_from_spec(spec)
spec.loader.exec_module(screen)


def abel_mass_fraction(x, n):
    """Exact integral of spherical Abel-deprojected Sersic mass.

    The gamma-distributed surface-density derivative has shape 2n+1.
    For y <= b*x**(1/n), its angular kernel is unity; the remaining
    contribution has kernel 2/pi*(asin(u)-u*sqrt(1-u*u)).
    Tighter absolute tolerance than the screening-grid validation is used
    here to resolve the low-mass Gaussian benchmark at x=.01.
    """
    t0 = gammaincinv(2*n, .5) * x**(1/n)
    shape = 2*n+1

    def tail(t):
        u = min(1., (t0/t)**n)
        if u < .01:
            angular = 2*u**3/3 + u**5/5 + 3*u**7/28
        else:
            angular = math.asin(u)-u*math.sqrt(max(0., 1-u*u))
        return 2/math.pi*angular*math.exp((shape-1)*math.log(t)-t-gammaln(shape))

    return float(gammainc(shape, t0) + quad(
        tail, t0, np.inf, epsabs=1e-12, epsrel=1e-10, limit=200)[0])


def exact_diagnostics(mass, radius, re, n, a0):
    """Adaptive LOS, independent of screen.py's Gauss-Legendre/PS sum."""
    def integrands(t):
        sec = 1/math.cos(t)
        r = radius*sec
        gn = screen.G*mass*abel_mass_fraction(r/re, n)/r**2
        g = .5*(gn+math.sqrt(gn*gn+4*a0*gn))
        sensitivity = .5*(1-math.sqrt(gn/(gn+4*a0)))
        return g*sec, sensitivity

    a = quad(lambda t: integrands(t)[0], 0, math.pi/2,
             epsabs=1e-17, epsrel=1e-9, limit=100)[0]
    b = quad(lambda t: math.prod(integrands(t)), 0, math.pi/2,
             epsabs=1e-17, epsrel=1e-9, limit=100)[0]
    return 4*radius/screen.C**2*a, b/a


def main(output):
    result = {
        "assertion_tested": "PS approximation and fixed-impact a0 sensitivity agree with exact Abel/adaptive-LOS diagnostics for two named catalog candidates",
        "non_claims": "No v3s forward fit; no data likelihood, mass or photo-z refit, exclusion, or measurement of a0",
        "conventions": "Spherical isolated stellar-only simple-mu; photo-z physical radii and photo-z SED mass; A0 from screen.py",
        "gaussian_benchmarks": [], "candidates": [],
    }
    for x in [.01, .1, 1., 10.]:
        abel = abel_mass_fraction(x, .5)
        analytic = float(gammainc(1.5, math.log(2)*x*x))
        err = abel/analytic-1
        assert abs(err) < 1e-7
        result["gaussian_benchmarks"].append({"n": .5, "r_over_re": x,
            "abel_mass_fraction": abel, "analytic_mass_fraction": analytic,
            "relative_error": err})

    data = pd.read_csv(ROOT/"run_02"/"screen_all_15072.csv", low_memory=False)
    for uid in ["EUCL-DR1-L014994", "EUCL-DR1-L017819"]:
        row = data.loc[data.unique_identifier.eq(uid)].iloc[0]
        mass = 10**row.eclipse_log_survived_mass_med*screen.MSUN
        radius = row.einstein_radius_kpc_proxy*screen.MPC/1000
        re = row.effective_radius_kpc_proxy*screen.MPC/1000
        n = row.eclipse_sersic_index
        exact_alpha, exact_s = exact_diagnostics(mass, radius, re, n, screen.A0)
        ps_alpha, ps_s, _ = screen.diagnostics(mass, radius, re, n)
        assert abs(ps_alpha[0]/exact_alpha-1) < 1e-3
        assert abs(ps_s[0]-exact_s) < 1e-4
        root_abel = screen.exact_mass_fraction(radius/re, n)
        own_abel = abel_mass_fraction(radius/re, n)
        assert abs(root_abel-own_abel) < 1e-8
        h = 1e-4
        lo, _ = exact_diagnostics(mass, radius, re, n, screen.A0*math.exp(-h))
        hi, _ = exact_diagnostics(mass, radius, re, n, screen.A0*math.exp(h))
        fd = math.log(hi/lo)/(2*h)
        assert abs(fd-exact_s) < 1e-7
        scenarios = {}
        for name, mass_factor, a0_factor in [
            ("half_a0", 1., .5), ("double_a0", 1., 2.),
            ("higher_mass_0p2dex", 10**.2, 1.),
        ]:
            alpha, s = exact_diagnostics(mass*mass_factor, radius, re, n, screen.A0*a0_factor)
            scenarios[name] = {"mass_factor": mass_factor, "a0_factor": a0_factor,
                "deflection_fraction_change": alpha/exact_alpha-1, "S_alpha": s}
        result["candidates"].append({
            "unique_identifier": uid, "n": n, "r_over_re": radius/re,
            "exact_mass_fraction_at_RE": own_abel,
            "PS_mass_fraction_at_RE": float(screen.fraction_ps(radius/re, n)),
            "exact_alpha_unreduced_arcsec": exact_alpha/screen.ARCSEC,
            "exact_S_alpha": exact_s, "PS_S_alpha": float(ps_s[0]),
            "PS_alpha_relative_error": float(ps_alpha[0]/exact_alpha-1),
            "PS_S_alpha_absolute_error": float(ps_s[0]-exact_s),
            "exact_S_alpha_finite_difference": fd, "scenarios": scenarios,
        })
    strict = data.loc[data.strict_photometry_model_quality]
    result["strict_sample_context"] = {
        "count": len(strict), "S_at_least_0p1": int((strict.S_alpha_proxy >= .1).sum()),
        "gN_RE_over_a0_quantiles": strict.gN_RE_over_a0_proxy.quantile([0., .1, .5, .9, 1.]).to_dict(),
        "S_alpha_quantiles": strict.S_alpha_proxy.quantile([0., .1, .5, .9, 1.]).to_dict(),
        "interpretation": "Common S_alpha>=.1 is consistent with typical gN(RE) of a few a0 plus the lower-acceleration LOS tail; this is not a count of decisive tests.",
    }
    result["outcome"] = "finite candidate approximation/derivative checks passed; analytic Gaussian benchmark passed"
    output.write_text(json.dumps(result, indent=2)+"\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=ROOT/"exact_sersic_check.json")
    main(parser.parse_args().output)
