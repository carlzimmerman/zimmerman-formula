"""Bounded, deterministic thermal-compression backreaction control (stdlib)."""
import json
import math
import resource
import sys
from pathlib import Path

OUT = Path(sys.argv[1])
checks = []


def check(name, error, tolerance):
    checks.append(dict(name=name, error=error, tolerance=tolerance,
                       passed=math.isfinite(error) and abs(error) <= tolerance))


def gamma_half_moments(x):
    # Lower incomplete gamma at half integers by direct integration recurrence.
    g = math.sqrt(math.pi) * math.erf(math.sqrt(x))
    nu = 0.5
    vals = []
    for _ in range(3):
        g = nu * g - x ** nu * math.exp(-x)
        vals.append(g)
        nu += 1
    mean = vals[1] / vals[0]
    var = vals[2] / vals[0] - mean * mean
    p = vals[0] / (math.sqrt(math.pi) / 2)
    return mean, var, p


def tracer(x):
    mean, var, p = gamma_half_moments(x)
    q = 2 * x / (3 * var)
    central = q * 4 * x ** 1.5 / (3 * math.sqrt(math.pi) * p)
    return dict(x=x, mean_t=mean, var_t=var, mass_ratio_at_unit_chi=q,
                central_dark_to_baryon_density=central,
                rms2_over_Rc2=mean/x,
                self_to_trap_energy_lower_bound=q*x/mean,
                L_equal_rms_mass_ratio_at_unit_chi=q*mean/x,
                L_equal_rms_central_density_ratio=central*mean/x,
                L_equal_rms_self_to_trap_energy_lower_bound=q)


def integrate(delta, eta, s, n):
    # r in r0=sqrt[T/(m*kappa0)]; h=log(rho/rho_c),
    # w=G M(<r)/(r0*c_s^2), z=integral r^2 dw.
    R = math.sqrt(20)
    step = R / n
    r = step * 1e-4
    h = -(s + delta) * r*r / (2*(1 + eta*delta))
    w, z = delta*r**3, 3*delta*r**5/5

    def rhs(rr, hh, ww):
        density = delta * math.exp(max(hh, -745))
        return (-(s*rr + ww/(rr*rr))/(1+eta*density),
                3*density*rr*rr, 3*density*rr**4)

    for _ in range(n):
        # Last point lands at R rather than R+epsilon.
        dx = min(step, R-r)
        a = rhs(r, h, w)
        b = rhs(r+dx/2, h+dx*a[0]/2, w+dx*a[1]/2)
        c = rhs(r+dx/2, h+dx*b[0]/2, w+dx*b[1]/2)
        d = rhs(r+dx, h+dx*c[0], w+dx*c[1])
        h += dx*(a[0]+2*b[0]+2*c[0]+d[0])/6
        w += dx*(a[1]+2*b[1]+2*c[1]+d[1])/6
        z += dx*(a[2]+2*b[2]+2*c[2]+d[2])/6
        r += dx
    return w, z/w, h


def solve(eta, s, q, n):
    target = q * 20**1.5
    lo, hi = -14., 20.
    low = integrate(math.exp(lo), eta, s, n)[0]
    high = integrate(math.exp(hi), eta, s, n)[0]
    assert low < target < high, (eta, s, low, target, high)
    for _ in range(38):
        mid = (lo+hi)/2
        w, _, _ = integrate(math.exp(mid), eta, s, n)
        if w < target:
            lo = mid
        else:
            hi = mid
    delta = math.exp((lo+hi)/2)
    w, meanr2, edgeh = integrate(delta, eta, s, n)
    return dict(eta=eta, s=s, central_density_ratio=delta,
                mean_r2=meanr2, relative_mass_residual=w/target-1,
                edge_density_ratio=delta*math.exp(max(edgeh, -745)))


rows = [tracer(x) for x in (5., 10., 20.)]
check('large x gamma mean', rows[-1]['mean_t']-1.5, 3e-7)
check('large x gamma variance', rows[-1]['var_t']-1.5, 7e-6)
for row in rows:
    check('normalization algebra x='+str(row['x']),
          3*row['mass_ratio_at_unit_chi']*row['var_t']/(2*row['x'])-1,
          1e-14)

# Orthogonal Simpson integrations of normalized radial moments.
for x in (5., 10., 20.):
    n = 4000
    h = math.sqrt(2*x)/n
    ints = []
    for power in (2, 4, 6):
        sm = 0.
        for j in range(n+1):
            rr = h*j
            weight = 1 if j in (0, n) else 4 if j % 2 else 2
            sm += weight*rr**power*math.exp(-rr*rr/2)
        ints.append(sm*h/3)
    mean, var, _ = gamma_half_moments(x)
    check('independent quadrature mean '+str(x), ints[1]/ints[0]/2-mean, 3e-12)
    check('independent quadrature variance '+str(x),
          (ints[2]/ints[0]-(ints[1]/ints[0])**2)/4-var, 2e-11)

# Homogeneous no-selfgravity check can be approximated by delta -> 0.
for s in (1., 2., 5.):
    _, r2, _ = integrate(1e-9, 0., s, 800)
    mean, _, _ = gamma_half_moments(10*s)
    check('ODE no-selfgravity moment '+str(s), r2-2*mean/s, 3e-8)

q = rows[1]['mass_ratio_at_unit_chi']
profiles = []
summaries = []
for eta in (.1, 1., 10.):
    coarse = solve(eta, 1., q, 2400)
    base = solve(eta, 1., q, 4800)
    fine = solve(eta, 1., q, 9600)
    check('mesh width '+str(eta), base['mean_r2']/fine['mean_r2']-1, 3e-6)
    check('mesh central '+str(eta),
          base['central_density_ratio']/fine['central_density_ratio']-1, 3e-6)
    check('coarse convergence '+str(eta),
          max(0., abs(base['mean_r2']-fine['mean_r2'])-abs(coarse['mean_r2']-fine['mean_r2'])), 1e-10)
    eps = .002
    minus, plus = solve(eta, 1-eps, q, 4800), solve(eta, 1+eps, q, 4800)
    minus2, plus2 = solve(eta, 1-eps/2, q, 4800), solve(eta, 1+eps/2, q, 4800)
    der = (plus['mean_r2']-minus['mean_r2'])/(2*eps)
    der2 = (plus2['mean_r2']-minus2['mean_r2'])/eps
    check('derivative refinement '+str(eta), der/der2-1, 2e-5)
    criticality = -3*q*der2/40
    b = -base['mean_r2']/der2
    comparisons = []
    for s in (1., 1.1, 2., 5., 10.):
        row = base if s == 1 else solve(eta, s, q, 4800)
        check('mass residual '+str((eta,s)), row['relative_mass_residual'], 2e-9)
        p = 1-row['mean_r2']/base['mean_r2']
        comparisons.append(dict(s=s, compression_fraction=p,
                                tracer_rational=1-1/s,
                                slope_matched_rational=(s-1)/(s-1+b)))
        profiles.append(row)
    summaries.append(dict(eta=eta, normalized_susceptibility=criticality,
                          local_rational_a_over_a0=b,
                          central_density_ratio=base['central_density_ratio'],
                          mean_r2=base['mean_r2'], response=comparisons))

result = dict(base_checkpoint='f659e6d8e1ee4cf2b756f091aff56b018da1fb1e',
              assertion_tested='Exact truncated tracer normalization and bounded stationary selfconsistent contact/gravity controls',
              tracer=rows, selfconsistent=summaries, profiles=profiles,
              checks=checks, all_passed=all(c['passed'] for c in checks),
              observed_max_rss_platform_units=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
              non_claims=['No certified stability, continuum error theorem or physical state selection.',
                          'Compression is not a common acceleration dipole; no kappa or abundance is derived.'])
OUT.write_text(json.dumps(result, indent=2)+'\n')
print(json.dumps(dict(all_passed=result['all_passed'], checks=len(checks),
                      tracer=rows, selfconsistent=summaries), indent=2))
sys.exit(0 if result['all_passed'] else 1)
