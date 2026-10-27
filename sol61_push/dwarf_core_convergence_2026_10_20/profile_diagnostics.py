"""Postprocessing for particle profiles, with no imposed dynamical symmetry.

Radial shell averages are measurements of supplied 3D particles. Flatness of
an average does not establish an isotropic 3D core. No forces are evaluated.

The softened weak-encounter relaxation SCREEN follows Ludlow, Schaye & Bower,
arXiv:1812.05777v2 (11 July 2019), section 3.2.1 equation (11), checked at
https://arxiv.org/html/1812.05777v2#S3.SS2.SSS1 . It uses

 t_relax / t_orb = Neff / (4 B),  t_orb=2 pi sqrt(R^3/(G M)),
 B=ln(1+(R/eps)^2)+(eps^2-2 R^2)/(3(eps^2+R^2))-ln(3/2).

Here M includes all supplied gravitating particle species and the exploratory
multicomponent substitution Neff=M^2/sum(m_i^2) is explicit. This assumes a
roughly virialized local population, weak uncorrelated encounters, an outer
impact parameter R and inner eps/sqrt(2). It is not a theorem for an evolving
multicomponent, anisotropic, tidally stripped dwarf. Collective discreteness
effects and actual collisional C22 transport are not represented by this
screen. In particular, cosmological circular-velocity convergence calibrations
are not adopted as a proof of density-slope or satellite convergence here.

Power-law slope fits profile the amplitude from independent Poisson shell
counts, equivalent to a multinomial likelihood conditional on the total
count. Their asymptotic likelihood-ratio intervals measure CONDITIONAL count
uncertainty only, excluding temporal correlations, realization variance,
centring bias, force/collision support and other systematic errors.
"""
import numpy as np
from scipy.optimize import brentq, minimize_scalar
from scipy.stats import chi2


G_PC_MSUN_MYR = 0.004498638185693768


def _enclosed(radius, mass, edges):
    order = np.argsort(radius, kind="stable")
    count = np.searchsorted(radius[order], edges, side="right")
    first = np.r_[0., np.cumsum(mass[order])]
    second = np.r_[0., np.cumsum(mass[order] ** 2)]
    enclosed_mass, enclosed_square = first[count], second[count]
    neff = np.divide(enclosed_mass ** 2, enclosed_square,
                     out=np.zeros_like(enclosed_mass), where=enclosed_square > 0.)
    return count, enclosed_mass, enclosed_square, neff


def shell_profile(x, m, centre, edges, cold=None):
    """Return selected-density shells (lo,hi] plus all-species gravity accounts.

    ``cold`` selects density tracers only. All x,m particles contribute to the
    gravitating enclosed masses and Neff. Inner material below the first edge
    is retained in enclosed accounts, even though it is outside fitted shells.
    """
    x, m, centre, edges = (np.asarray(value, float) for value in (x, m, centre, edges))
    if (x.shape != (len(m), 3) or centre.shape != (3,) or edges.ndim != 1
            or len(edges) < 2 or np.any(edges <= 0.) or np.any(np.diff(edges) <= 0.)
            or np.any(m <= 0.) or not all(np.all(np.isfinite(a)) for a in (x, m, centre, edges))):
        raise ValueError("finite positions, centre, positive masses and increasing positive edges required")
    selected = np.ones(len(m), bool) if cold is None else np.asarray(cold, bool)
    if selected.shape != m.shape:
        raise ValueError("density-selection mask must match the mass array")
    radius = np.linalg.norm(x - centre, axis=1)
    count, mass, square, neff = _enclosed(radius[selected], m[selected], edges)
    gcount, gmass, gsquare, gneff = _enclosed(radius, m, edges)
    shell_count, shell_mass, shell_square = np.diff(count), np.diff(mass), np.diff(square)
    volume = 4. * np.pi / 3. * np.diff(edges ** 3)
    shell_neff = np.divide(shell_mass ** 2, shell_square, out=np.zeros_like(shell_mass), where=shell_square > 0.)
    selected_mass = m[selected]
    equal_mass = len(selected_mass) == 0 or np.allclose(selected_mass, selected_mass[0], rtol=1.e-12, atol=0.)
    return dict(edges=edges.tolist(), radius=np.sqrt(edges[:-1] * edges[1:]).tolist(),
                count=shell_count.tolist(), mass=shell_mass.tolist(), Neff=shell_neff.tolist(),
                volume=volume.tolist(), density=(shell_mass / volume).tolist(),
                cumulative_count=count[1:].tolist(), cumulative_mass=mass[1:].tolist(),
                cumulative_Neff=neff[1:].tolist(),
                enclosed_count_at_edges=count.tolist(), enclosed_mass_at_edges=mass.tolist(),
                enclosed_Neff_at_edges=neff.tolist(),
                gravitating_cumulative_count=gcount[1:].tolist(),
                gravitating_cumulative_mass=gmass[1:].tolist(),
                gravitating_cumulative_Neff=gneff[1:].tolist(),
                gravitating_enclosed_count_at_edges=gcount.tolist(),
                gravitating_enclosed_mass_at_edges=gmass.tolist(),
                gravitating_enclosed_Neff_at_edges=gneff.tolist(),
                selected_equal_mass=bool(equal_mass),
                convention="density shells (lo,hi]; enclosed gravity includes all supplied species; radial averaging is diagnostic only")


def relaxation_screen(profile, eps, G=G_PC_MSUN_MYR, age_Myr=10000.):
    """Return a heuristic local encounter screen, not empirical convergence."""
    if eps <= 0. or G <= 0. or age_Myr <= 0.:
        raise ValueError("eps, G and screening age must be positive")
    radius = np.asarray(profile["edges"], float)
    mass = np.asarray(profile["gravitating_enclosed_mass_at_edges"], float)
    neff = np.asarray(profile["gravitating_enclosed_Neff_at_edges"], float)
    ratio2 = (radius / eps) ** 2
    bracket = np.log1p(ratio2) + (1. - 2. * ratio2) / (3. * (1. + ratio2)) - np.log(1.5)
    valid = (mass > 0.) & (neff > 1.) & (radius > eps / np.sqrt(2.)) & (bracket > 0.)
    torb, trelax = np.full(len(radius), np.nan), np.full(len(radius), np.nan)
    torb[valid] = 2. * np.pi * np.sqrt(radius[valid] ** 3 / (G * mass[valid]))
    trelax[valid] = neff[valid] / (4. * bracket[valid]) * torb[valid]

    def nullable(values):
        return [float(value) if np.isfinite(value) else None for value in values]

    return dict(radius=radius[1:].tolist(), torb_Myr=nullable(torb[1:]),
                t_relax_Myr=nullable(trelax[1:]), valid=valid[1:].tolist(),
                pass_age=(valid[1:] & (trelax[1:] >= age_Myr)).tolist(),
                edge_torb_Myr=nullable(torb), edge_t_relax_Myr=nullable(trelax),
                edge_valid=valid.tolist(), age_Myr=float(age_Myr), eps=float(eps),
                heuristic_screen_only=True,
                assumptions="weak uncorrelated softened encounters; local virial speed and scale R; explicit multicomponent Neff substitution; no guarantee for tides, collective noise, or density slopes",
                source="https://arxiv.org/html/1812.05777v2#S3.SS2.SSS1 equation (11)")


def _edge_index(edges, value):
    hit = np.flatnonzero(np.isclose(edges, value, rtol=1.e-10, atol=0.))
    if len(hit) != 1:
        raise ValueError("fit interval endpoints must match recorded shell edges; partial shell counts cannot be assigned")
    return int(hit[0])


def _log_integral(lo, hi, q):
    width = np.log(hi / lo)
    if abs(q) < 1.e-6:
        return np.log(width) + q * .5 * (np.log(lo) + np.log(hi)) + q * q * width * width / 24.
    return q * np.log(lo) + np.log(np.abs(np.expm1(q * width))) - np.log(abs(q))


def fit_powerlaw(profile, rmin, rmax, confidence=.95):
    """Fit rho=A r^-gamma using every shell in the chosen edge-aligned interval."""
    if not profile["selected_equal_mass"]:
        raise ValueError("Poisson count density-slope fits require equal-mass selected particles")
    if not 0. < confidence < 1.:
        raise ValueError("confidence must lie strictly between zero and one")
    edges = np.asarray(profile["edges"], float)
    first, last = _edge_index(edges, rmin), _edge_index(edges, rmax)
    if last <= first:
        raise ValueError("fit interval must have increasing edges")
    lo, hi = edges[first:last], edges[first + 1:last + 1]
    counts = np.asarray(profile["count"], float)[first:last]
    count = int(np.sum(counts))
    result = dict(interval=[float(rmin), float(rmax)], edge_indices=[first, last],
                  fit_bin_count=last - first, fit_count=count, conditional_Poisson_only=True,
                  confidence=float(confidence), uncertainty_scope="asymptotic conditional Poisson profile-likelihood only; no temporal/ensemble/systematic uncertainty",
                  gamma_definition="rho proportional to r^(-gamma)")
    if count == 0:
        result.update(fit_valid=False, gamma=None, gamma_interval=[None, None], gamma_ci95=[None, None],
                      failure="no selected particles in interval", expected_shell_counts=[],
                      poisson_deviance=None, gof_df=last - first - 2, gof_pvalue=None,
                      gof_asymptotic_valid=False)
        return result

    def loglike(gamma):
        q = 3. - gamma
        logp = _log_integral(lo, hi, q) - _log_integral(float(rmin), float(rmax), q)
        return float(counts @ logp)

    bounds = (-6., 6.)
    fit = minimize_scalar(lambda gamma: -loglike(gamma), bounds=bounds, method="bounded",
                          options=dict(xatol=1.e-9))
    gamma = float(fit.x); maximum = loglike(gamma)
    threshold = maximum - .5 * chi2.ppf(confidence, 1)
    lower = brentq(lambda value: loglike(value) - threshold, bounds[0], gamma) if loglike(bounds[0]) < threshold else None
    upper = brentq(lambda value: loglike(value) - threshold, gamma, bounds[1]) if loglike(bounds[1]) < threshold else None
    q = 3. - gamma
    expected = count * np.exp(_log_integral(lo, hi, q) - _log_integral(float(rmin), float(rmax), q))
    positive = counts > 0.
    deviance = float(2. * (np.sum(counts[positive] * np.log(counts[positive] / expected[positive]))
                           - np.sum(counts - expected)))
    deviance = max(deviance, 0.)
    degrees = last - first - 2
    gof_valid = degrees > 0 and bool(np.all(expected >= 5.))
    result.update(fit_valid=bool(fit.success), gamma=gamma, gamma_interval=[lower, upper],
                  gamma_ci95=[lower, upper] if np.isclose(confidence, .95) else [None, None],
                  loglike=maximum, parameter_search_bounds=list(bounds),
                  interval_bound_limited=lower is None or upper is None,
                  expected_shell_counts=expected.tolist(), poisson_deviance=deviance,
                  gof_df=degrees, gof_pvalue=float(chi2.sf(deviance, degrees)) if gof_valid else None,
                  gof_asymptotic_valid=gof_valid,
                  gof_scope="asymptotic conditional Poisson shell-average powerlaw model fit; not a test of 3D asphericity")
    return result


def classify_flatness(profile, fit, screen, eps, age_Myr=10000., preferred_age_Myr=20000.):
    """Conditional flat-profile candidate; empirical convergence remains external.

    Flatness requires the whole two-sided 95% conditional interval in (-.3,.3),
    preventing an outward-rising hollow profile from passing an upper bound.
    """
    first, last = fit["edge_indices"]
    rmin, rmax = fit["interval"]
    failed = []
    if rmax / rmin < 3. - 1.e-12:
        failed.append("radial_lever_arm")
    if rmin < 2.8 * eps:
        failed.append("force_resolution")
    if np.asarray(profile["enclosed_count_at_edges"])[first] < 200:
        failed.append("enclosed_selected_count")
    if fit["fit_bin_count"] < 3:
        failed.append("radial_bin_count")
    relaxation = np.asarray(screen["edge_t_relax_Myr"], float)[first:last + 1]
    if not np.all(np.isfinite(relaxation)) or np.any(relaxation < age_Myr):
        failed.append("relaxation_age")
    lower, upper = fit["gamma_ci95"]
    if not fit["fit_valid"] or lower is None or upper is None:
        sampling = "inconclusive"
    elif lower > -.3 and upper < .3:
        sampling = "flat_conditional"
    elif lower >= .3 or upper <= -.3:
        sampling = "nonflat"
    else:
        sampling = "inconclusive"
    numerical_pass = len(failed) == 0
    gof_valid = bool(fit.get("gof_asymptotic_valid", False))
    gof_pass = gof_valid and fit["gof_pvalue"] >= .05
    if not gof_valid:
        failed.append("powerlaw_model_gof_unavailable")
    elif not gof_pass:
        failed.append("powerlaw_model_misfit")
    flat = numerical_pass and sampling == "flat_conditional" and gof_pass
    return dict(verdict=("flat_profile_candidate_pending_convergence" if flat else
                         "inconclusive_unresolved" if not numerical_pass else
                         "inconclusive_model_fit" if not gof_valid else
                         "powerlaw_model_misfit" if not gof_pass else
                         "nonflat_conditional" if sampling == "nonflat" else "inconclusive_sampling"),
                flat_candidate=bool(flat), numerical_screen_pass=bool(numerical_pass),
                preferred_relaxation_pass=bool(np.all(np.isfinite(relaxation)) and np.all(relaxation >= preferred_age_Myr)),
                preferred_force_radius_5eps_pass=bool(rmin >= 5. * eps),
                conditional_powerlaw_gof_pass=bool(gof_pass),
                sampling_flatness=sampling, failed_gates=failed, core_established=False,
                temporal_and_ensemble_uncertainty_missing=True,
                required_further_checks="independent timestep, softening, particle number and collision-support convergence; centring, 3D shape and temporal/ensemble uncertainty")


def compare_profiles(a, b, tolerance=.1):
    """Compare all supplied bins, never selecting bins because they agree."""
    edges_a, edges_b = np.asarray(a["edges"], float), np.asarray(b["edges"], float)
    coverage = edges_a.shape == edges_b.shape and np.array_equal(edges_a, edges_b)
    if not coverage:
        return dict(coverage_match=False, all_within_tolerance=False, within_tolerance=[],
                    relative_difference=[], verdict="inconclusive_coverage", tolerance=float(tolerance))
    da, db = np.asarray(a["density"], float), np.asarray(b["density"], float)
    valid = np.isfinite(da) & np.isfinite(db) & (da > 0.) & (db > 0.)
    difference = np.divide(np.abs(db - da), da, out=np.full_like(da, np.inf), where=da > 0.)
    within = valid & (difference <= tolerance)
    return dict(coverage_match=True, all_within_tolerance=bool(len(within) > 0 and np.all(within)),
                within_tolerance=within.tolist(), valid_density=valid.tolist(),
                relative_difference=[float(value) if np.isfinite(value) else None for value in difference],
                tolerance=float(tolerance), comparison="absolute density difference divided by first profile density; all bins retained")
