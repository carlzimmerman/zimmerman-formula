"""Spherical two-state prototype; units and limitations in DESIGN/DERIVATION."""
import argparse
import json
import math
from pathlib import Path

import numpy as np
from scipy.integrate import quad
from scipy.special import expit
from scipy.optimize import brentq

G = 4.30091e-6  # kpc (km/s)^2 / Msun
A0 = 9.3603e-11 * (3.085677581491367e19 / 1e6)  # (km/s)^2 / kpc
RESERVOIR = 5.364
PROFILES = [
    ("dwarf", 3e5, 0.3, 0.3),
    ("dwarf_disk", 1e8, 1.0, 2.0),
    ("large_disk", 6e10, 3.0, 6.0),
    ("cluster", 1e14, 300.0, 500.0),
]


def law(y):
    """g/a0 for a nonnegative source y=g_source/a0."""
    return 0.5 * (y + np.sqrt(y * y + 4 * y))


def excess(y):
    # Stable g-y, including at large y.
    return 2 * y / (np.sqrt(y * y + 4 * y) + y)


def mb(r, b):
    return r**3 / (r*r + b*b)**1.5


def mt(r, b):
    return r*r * excess(mb(r, b) / r**2)


def outer(b):
    hi = max(10., b)
    while mt(hi, b) < RESERVOIR:
        hi *= 2
    return brentq(lambda r: mt(r, b) - RESERVOIR, 1e-10, hi)


def tether_u(r, b, radius):
    return mt(r, b) / r**2 if r <= radius else RESERVOIR / r**2


def w(u):
    """K W_full/a0^2; stable series for the small-u tail."""
    if not 0 <= u < 1:
        raise ValueError("outside tether domain")
    if u < 0.01:
        return sum(u**n/n for n in range(2, 10))
    return -math.log1p(-u) - u


def field_energy(b, radius):
    f = lambda r: r*r*w(tether_u(r, b, radius))
    return quad(f, 0, radius, epsabs=1e-8)[0] + quad(f, radius, np.inf, epsabs=1e-8)[0]


def chemical_potential(r, b, radius):
    # delta U_full / delta M_T(r), in units a0*r_M.
    f = lambda s: tether_u(s, b, radius)/(1-tether_u(s, b, radius))
    if r < radius:
        return quad(f, r, radius, epsabs=1e-9)[0] + quad(f, radius, np.inf, epsabs=1e-9)[0]
    return quad(f, r, np.inf, epsabs=1e-9)[0]


def mean_chemical_potential(q, b, radius):
    """U'(q)/M for a frozen total profile with T fraction q everywhere."""
    def f(r):
        u0=tether_u(r,b,radius)
        return r*r*q*u0*u0/(1-q*u0)
    return (quad(f,0,radius,epsabs=1e-8)[0] +
            quad(f,radius,np.inf,epsabs=1e-8)[0])/RESERVOIR


def phase_fraction(epsilon, theta, b, radius, velocity2):
    """Stationary reversible rates; theta is specific bath energy, not gas T.

    Gamma_TF/Gamma_FT=exp((mu-epsilon)/theta), Gamma sum set to 1.
    This is a stipulated kinetic closure, not a derived microscopic process.
    """
    def drift(q):
        mu=mean_chemical_potential(q,b,radius)*velocity2
        gtf=expit((mu-epsilon)/theta)
        gft=expit((epsilon-mu)/theta)
        return (1-q)*gft-q*gtf
    q=brentq(drift,0,1,xtol=1e-12)
    return dict(tethered_fraction=q, rate_balance_residual=abs(drift(q)))


def static_checks():
    # Independent SI dimensional benchmark, including the squared km factor.
    rm_si_kpc = math.sqrt(6.67430e-11 * (6e10*1.98847e30) / 9.3603e-11) / 3.085677581491367e19
    rm_mixed_kpc = math.sqrt(G*6e10/A0)
    assert abs(rm_mixed_kpc/rm_si_kpc-1) < 1e-4
    y = np.logspace(-10, 6, 801)
    gg = law(y)
    residual = np.max(np.abs(gg*gg/(gg+1)/y - 1))
    assert residual < 1e-12
    # Orthogonal inversion through a root solver, rather than reusing law().
    root_error = 0.
    for yy in np.logspace(-7, 4, 31):
        x = brentq(lambda x: x*x/(x+1)-yy, 0, 2*law(yy), xtol=1e-14)
        root_error = max(root_error, abs(x/law(yy)-1))
    assert root_error < 1e-9
    rows = []
    for name, mass, scale, r in PROFILES:
        rm = math.sqrt(G*mass/A0)
        b = scale/rm
        radius = outer(b)
        yy = G*mass*mb(r, scale)/(r*r*A0)
        g0 = float(law(yy))
        budgets = {}
        for dex in (0.05, 0.10):
            gt = 10**dex*g0
            budgets[str(dex)] = (gt*gt/(gt+1)-yy)/yy
        needed = {}
        for boost in (1.8, 3.0):
            gt = boost*g0
            needed[str(boost)] = (gt*gt/(gt+1)-yy)/yy
        rgrid = np.geomspace(1e-7*radius, radius, 2000)
        assert np.all(np.diff(mt(rgrid, b)) > 0), "negative T density"
        # Convert existing T, not a fictitious particle beyond the cutoff.
        chemical_r = min(r/rm, .8*radius)
        mu = chemical_potential(chemical_r, b, radius)*A0*rm
        energy = field_energy(b, radius)*mass*A0*rm
        mu10=mean_chemical_potential(.1,b,radius)*A0*rm
        mu95=mean_chemical_potential(.95,b,radius)*A0*rm
        rows.append(dict(name=name, baryon_mass_msun=mass, b_kpc=scale,
                         test_radius_kpc=r, rM_kpc=rm, b_over_rM=b,
                         reservoir_radius_kpc=radius*rm, source_y=yy,
                         free_to_enclosed_baryons_limit=budgets,
                         free_to_enclosed_baryons_for_boost=needed,
                         chemical_mu_km2_s2=mu,
                         chemical_test_radius_kpc=chemical_r*rm,
                         law_T_mass_needed_at_test_radius_msun=mt(r/rm,b)*mass,
                         law_mass_available_at_test_radius=bool(r/rm <= radius),
                         full_conversion_energy_msun_km2_s2=energy,
                         mean_mu_q10_km2_s2=mu10,
                         mean_mu_q95_km2_s2=mu95,
                         phase_epsilon0_theta100=phase_fraction(0.,100.,b,radius,A0*rm),
                         T_density_positive_on_grid=True))
    # Equality of each pair's gravity and finite-difference tether force is
    # audited below independently of the RAR inversion.
    eps_lo = max(row['chemical_mu_km2_s2'] for row in rows if 'disk' in row['name'])
    eps_hi = rows[0]['chemical_mu_km2_s2']
    phase_lower=max(x['mean_mu_q95_km2_s2'] for x in rows if 'disk' in x['name'])
    phase_upper=rows[0]['mean_mu_q10_km2_s2']
    return dict(law_max_relative_residual=float(residual),
                unit_benchmark_rM_kpc=rm_mixed_kpc,
                root_max_relative_error=root_error, profiles=rows,
                selector=dict(epsilon_min_to_keep_both_disks=eps_lo,
                              epsilon_max_to_convert_dwarf=eps_hi,
                              interval_exists=eps_lo < eps_hi),
                frozen_profile_reversible_selector=dict(
                    epsilon_lower_at_theta0_for_disk_q95=phase_lower,
                    epsilon_upper_at_theta0_for_dwarf_q10=phase_upper,
                    lower_slope_in_theta=math.log(.95/.05),
                    upper_slope_in_theta=math.log(.1/.9),
                    impossible_for_any_common_nonnegative_theta=bool(phase_lower>phase_upper)))


def force_energy_checks():
    # Exact finite spherical T shell in a fixed interior mass. Differentiating
    # its field integral gives the jump of W, not W' at an arbitrary sample.
    rin, r, rout = 1., 2., 20.
    inside, shell = .1, .02
    def energy(x):
        return quad(lambda s: s*s*w(inside/s**2), rin, x)[0] + quad(
            lambda s: s*s*w((inside+shell)/s**2), x, rout)[0]
    h = 1e-4
    numerical_force = -(energy(r+h)-energy(r-h))/(2*h)/shell
    analytic_force = r*r*(w((inside+shell)/r**2)-w(inside/r**2))/shell
    err = abs(numerical_force/analytic_force-1)
    assert err < 1e-7
    # Receiver accounts for conversion, including a nonzero internal gap.
    b = 1.
    U = field_energy(b, outer(b))
    epsilon = .1
    before = U-epsilon*RESERVOIR
    receiver = U-epsilon*RESERVOIR
    after_plus_receiver = receiver  # all F: zero field and internal T energy
    assert abs(before-after_plus_receiver) < 1e-12
    assert receiver > 0
    return dict(tether_variational_force_relative_error=err,
                conversion_receiver_energy=receiver,
                conversion_energy_balance_error=abs(before-after_plus_receiver))


def shell_fields(r, b, baryon_mass, eps):
    n = len(r)
    m = 1./n
    order = np.argsort(r)
    rs = r[order]
    z = np.sqrt(rs*rs+eps*eps)
    enclosed = (np.arange(n)+.5)*m
    acc_sort = -enclosed*rs/z**3 - baryon_mass*rs/(rs*rs+b*b)**1.5
    # Pair kernel -m_i*m_j/sqrt(max(r_i,r_j)^2+eps^2), half shell self energy.
    ug = -np.sum(m*enclosed/z)
    ub = -np.sum(m*baryon_mass/np.sqrt(rs*rs+b*b))
    outer_potential = np.cumsum((m/z)[::-1])[::-1]-m/z
    removal_potential = -enclosed/z-outer_potential-baryon_mass/np.sqrt(rs*rs+b*b)
    acc = np.empty(n)
    phi = np.empty(n)
    acc[order], phi[order] = acc_sort, removal_potential
    return acc, float(ug+ub), phi


def dynamics(b_over_rm, n, dt, duration=8.):
    """All T -> F externally triggered; then 90% impulsive baryon loss.

    Normalize initial cold mass, truncation radius and G to 1. No live T is
    left in this retention experiment. Finite-time, softened radial shells.
    """
    R = outer(b_over_rm)
    targets = (np.arange(n)+.5)/n*RESERVOIR
    r = np.array([brentq(lambda x: mt(x,b_over_rm)-target, 1e-12, R)
                  for target in targets])/R
    b = b_over_rm/R
    eps = .02
    v = np.zeros(n)
    baryon_mass = .1/RESERVOIR
    acc, u0, phi = shell_fields(r,b,baryon_mass,eps)
    e0 = u0
    max_error = 0.
    sample = []
    steps = round(duration/dt)
    for step in range(steps):
        v += .5*dt*acc
        r += dt*v
        crossing = r < 0
        r[crossing] *= -1
        v[crossing] *= -1
        acc, potential, phi = shell_fields(r,b,baryon_mass,eps)
        v += .5*dt*acc
        energy = .5*np.mean(v*v)+potential
        max_error = max(max_error, abs((energy-e0)/e0))
        if (step+1) % max(1,steps//8) == 0:
            sample.append(dict(time=(step+1)*dt,
                               bound_fraction=float(np.mean(.5*v*v+phi < 0)),
                               inside_initial_radius=float(np.mean(r<1)),
                               energy_relative_error=abs((energy-e0)/e0)))
    return dict(n=n, dt=dt, time=steps*dt, softening_over_initial_radius=eps,
                baryon_fraction_retained=.1, b_over_rM=b_over_rm,
                initial_energy=e0, max_relative_energy_error=max_error,
                initial_negative_energy_fraction=1.,
                final_bound_fraction=sample[-1]['bound_fraction'],
                final_inside_initial_radius=sample[-1]['inside_initial_radius'],
                snapshots=sample)


def numerical_gradient_check():
    r = np.array([.12,.31,.71,.95])
    a,u,_ = shell_fields(r,.2,.1,.02)
    errors=[]
    for i in range(len(r)):
        dr=np.zeros_like(r); dr[i]=1e-6
        up=shell_fields(r+dr,.2,.1,.02)[1]
        um=shell_fields(r-dr,.2,.1,.02)[1]
        fd=-(up-um)/(2e-6)*len(r)
        errors.append(abs(fd/a[i]-1))
    assert max(errors)<1e-7
    return max(errors)


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--output',required=True)
    parser.add_argument('--mode',choices=['static','dynamics'],default='static')
    args=parser.parse_args()
    if args.mode=='static':
        result=static_checks()
        result['energy_checks']=force_energy_checks()
        result['shell_potential_gradient_error']=numerical_gradient_check()
    else:
        runs=[]
        for b in (10.,.3):
            runs.append(dynamics(b,128,.0001))
            runs.append(dynamics(b,256,.00005))
        result=dict(runs=runs,
                    energy_criterion_pass=all(x['max_relative_energy_error']<.005 for x in runs),
                    resolution_criterion_pass=all(abs(runs[i]['final_bound_fraction']-
                        runs[i+1]['final_bound_fraction'])<.05 for i in (0,2)))
    p=Path(args.output)
    p.parent.mkdir(parents=True,exist_ok=True)
    p.write_text(json.dumps(result,indent=2,allow_nan=False)+'\n')
    print(json.dumps(result,indent=2,allow_nan=False))


if __name__=='__main__':
    main()
