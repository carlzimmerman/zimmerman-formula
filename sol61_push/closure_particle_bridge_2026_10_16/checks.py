"""Bounded controls for the October 16 research checkpoint; standard library only.

No fitted likelihood, transfer function, or coupled dark-sector evolution.
Run from repository root with one argument: fresh run output directory.
"""
import json
import math
import sys
from fractions import Fraction as F
from pathlib import Path

out = Path(sys.argv[1])
assert out.is_dir()
checks = []

def check(name, condition):
    checks.append({"name": name, "passed": bool(condition)})
    assert condition, name

# Route A: explicitly stipulated broken-phase Higgs decay, MB bath, constant g*.
# Lportal = -lambdaHX |H|^2 |X|^2. h -> X X* -> 4 daughters.
mh, vev, mpl = 125.0, 246.0, 1.2209e19  # GeV, unreduced M_Pl
md, ustar, gs, gr = 0.001, 0.02, 106.75, 106.75
mx = 2 * md * math.sqrt(1 + ustar**2)
omega_h2, density_conversion = 0.12, 2.742e8  # illustrative standard cosmology
yd = omega_h2 / (density_conversion * md)
yield_prefactor = 135 / (8 * math.pi**3 * 1.66 * gs * math.sqrt(gr))
width = yd * mh**2 / (4 * yield_prefactor * mpl)
phase = math.sqrt(1 - 4 * mx**2 / mh**2)
portal = math.sqrt(width * 16 * math.pi * mh / (vev**2 * phase))
check("yield inverted with four daughters", abs(4 * yield_prefactor * mpl * width / mh**2 / yd - 1) < 1e-14)
check("portal width normalization", abs(portal**2 * vev**2 * phase / (16 * math.pi * mh) / width - 1) < 1e-14)

# Exact daughter energy from isotropic X decay in a stationary Higgs frame.
gamma_x = mh / (2 * mx)
beta_x = math.sqrt(1 - 1 / gamma_x**2)
estar, pstar = mx / 2, md * ustar
emin = gamma_x * (estar - beta_x * pstar)
emax = gamma_x * (estar + beta_x * pstar)
emean = gamma_x * estar
check("mean daughter energy mh/4", abs(emean / (mh / 4) - 1) < 1e-14)
check("boost endpoints physical", md < emin < emean < emax)
check("four daughter average energies conserve Higgs energy", abs(4 * emean / mh - 1) < 1e-14)

# Collisionless kinematic CONTROL: monochromatic mean momentum, instantaneous
# production, prescribed entropy history. Not an actual freeze-in spectrum.
tgamma0, gs0 = 2.348e-13, 3.91  # GeV
prod_temperature = mh / 3
aprod = tgamma0 / prod_temperature * (gs0 / gs)**(1/3)
uprod = math.sqrt((emean / md)**2 - 1)
anr = aprod * uprod
aeq = 1 / 3401.0
h0 = 67.4 * 1000 / 3.085677581491367e22  # s^-1
omega_r, c, mpc = 9.2e-5, 299792458.0, 3.085677581491367e22
rad_prefactor = c / (h0 * math.sqrt(omega_r)) / mpc
lambda_fs_rd = rad_prefactor * anr * (math.asinh(aeq / anr) - math.asinh(aprod / anr))

def simpson_log_free_stream(n):
    lo, hi = math.log(aprod), math.log(aeq)
    step = (hi - lo) / n
    def fn(x):
        a = math.exp(x)
        return a * anr / math.sqrt(a*a + anr*anr)
    acc = fn(lo) + fn(hi)
    for i in range(1, n):
        acc += (4 if i % 2 else 2) * fn(lo + i * step)
    return rad_prefactor * step * acc / 3

fs_num = [simpson_log_free_stream(n) for n in (1024, 2048)]
check("radiation-only distance independent quadrature", max(abs(x / lambda_fs_rd - 1) for x in fs_num) < 1e-8)
check("cold at equality in collisionless control", anr / aeq < 1e-5)

# A validity test of that CONTROL using the lane's adopted low-speed cross
# section: total number yield, isotropic mono-speed opposite-sign mixture.
# At 1 keV visible temperature the example is far below the source resonance.
t_test, gs_test, gr_test = 1e-6, 3.91, 3.36  # GeV
a_test = tgamma0 / t_test
utest = anr / a_test
vtest = c * utest / math.sqrt(1 + utest**2)
mean_relative_speed = 4 * vtest / 3  # exact angular average for equal speeds
hbarc, hbar = 1.973269804e-14, 6.582119569e-25  # GeV cm, GeV s
entropy_cm3 = 2 * math.pi**2 / 45 * gs_test * t_test**3 / hbarc**3
number_cm3 = yd * entropy_cm3
sigma_over_mass, gev_to_g = 0.3, 1.7826619216279e-24
sigma_cm2 = sigma_over_mass * md * gev_to_g
h_test = 1.66 * math.sqrt(gr_test) * t_test**2 / mpl / hbar
collision_over_h = number_cm3 * sigma_cm2 * mean_relative_speed * 100 / h_test
check("scattering screen below source resonance", utest < ustar / 10)
check("collisionless continuation inconsistent with adopted scattering screen", collision_over_h > 1)

# Naturalness diagnostics: portal tree shift if lambdaHPhi=0 at matching.
# They are sensitivities, not a computed renormalized self-energy.
gap = mx*mx - 4 * md*md
portal_mass_shift = portal * vev**2 / 2
dark_loop_scale = (2.168e-6)**2 / (16 * math.pi**2)
check("illustrative portal mass shift positive", portal_mass_shift > 0)
bare_source_mass2 = mx**2 - portal_mass_shift
max_portal_positive_bare_mass = 2 * mx**2 / vev**2
max_omega_positive_bare_mass = omega_h2 * (max_portal_positive_bare_mass / portal)**2
check("minimal portal benchmark needs additional source stabilization", bare_source_mass2 < 0)
lambda_h = mh**2 / (2 * vev**2)
lambda_x_floor = portal**2 / (4 * lambda_h)
lambda_x = 1e-18
check("explicit source quartic above sufficient stability floor", lambda_x > lambda_x_floor)
square_cases = 0
for w in (F(-2), F(0), F(3)):
    for z in (F(0), F(1,10), F(2)):
        lh, lp, lx = F(1,4), F(1,10), F(1,20)
        raw = lh*w*w + lp*w*z + lx*z*z
        squares = lh*(w+lp*z/(2*lh))**2 + (lx-lp*lp/(4*lh))*z*z
        check("stabilized portal exact square %d" % square_cases, raw == squares and squares >= 0)
        square_cases += 1

# Route B: exact rational conservation/scale-link identities in c=1 units.
count_b = 0
for w in (F(-1), F(-9,10), F(-11,10)):
    for q in (F(-1,10), F(0), F(1,10)):
        for ratio in (F(1,10), F(1), F(5)):
            # q=Q/(H rhoDE), s=dln a0/dln a, Q>0 into cold matter
            s = (-3 * (1+w) - q) / 2
            cold_slope = -3 + q / ratio
            baryon_slope = -3
            check("exchange invariant %d" % count_b,
                  2*s + 3*(1+w) + ratio*(cold_slope-baryon_slope) == 0)
            count_b += 1

# Route C: shell projection sign, exact rational parameterization
# x=R/r_shell=2t/(1+t^2), s=sqrt(1-x^2)=(1-t^2)/(1+t^2).
shell_cases = 0
for t in (F(1,100), F(1,10), F(1,3), F(1,2), F(9,10)):
    x, ss = 2*t/(1+t*t), (1-t*t)/(1+t*t)
    raw = (1-ss)/(x*x) - 1/(2*ss)
    stable = -x*x/(2*ss*(1+ss)**2)
    check("shell shear exact %d" % shell_cases, raw == stable and raw < 0)
    shell_cases += 1

# Finite nonnegative shell mixture: strictly exterior to all sampled R.
shell_mixture = []
for radius in (0.1, 0.3, 0.8):
    ds = 0.0
    for rs, mass in ((1., 2.), (2., 1.), (5., 4.)):
        ss = math.sqrt(1 - (radius/rs)**2)
        ds -= mass * radius**2 / (2*math.pi*rs**4*ss*(1+ss)**2)
    check("positive exterior mixture gives negative excess density R=%s" % radius, ds < 0)
    shell_mixture.append({"R": radius, "DeltaSigma": ds})

result = {
    "verdict": "conditional production bridge; collisionless control fails its own scattering screen; exact exchange and exterior-shell reductions",
    "portal": dict(m_GeV=md, M_GeV=mx, ustar=ustar, omega_h2_input=omega_h2,
                   yield_daughters=yd, yield_parents=yd/2, Gamma_h_GeV=width,
                   lambda_HX=portal, Higgs_branching_assuming_total_4p1MeV=width/0.0041,
                   gamma_X=gamma_x, daughter_energy_GeV=[emin, emean, emax],
                   portal_tree_mass_shift_GeV2=portal_mass_shift,
                   portal_shift_over_m2=portal_mass_shift/md**2,
                   portal_shift_over_threshold_gap=portal_mass_shift/gap,
                   bare_source_mass2_GeV2=bare_source_mass2,
                   max_lambda_positive_bare_source_mass=max_portal_positive_bare_mass,
                   max_omega_h2_positive_bare_source_mass=max_omega_positive_bare_mass,
                   lambda_H=lambda_h, lambda_X_sufficient_floor=lambda_x_floor,
                   lambda_X_example=lambda_x,
                   dark_loop_dimensional_scale_over_gap=dark_loop_scale/gap),
    "collisionless_control": dict(Tprod_GeV=prod_temperature, a_prod=aprod, a_nr=anr,
                   p_over_m_equality=anr/aeq, radiation_only_distance_Mpc=lambda_fs_rd,
                   independent_quadrature_Mpc=fs_num, T_screen_GeV=t_test,
                   p_over_m_screen=utest, Gamma_elastic_over_H=collision_over_h),
    "exchange_cases": count_b, "shell_exact_cases": shell_cases,
    "stabilized_portal_exact_cases": square_cases,
    "shell_mixture": shell_mixture, "checks": checks,
    "non_claims": ["No full momentum Boltzmann solution or viable combined candidate established",
                   "Portal coupling calibrated to stipulated abundance; no derived abundance or mass",
                   "No cosmological likelihood or observational exclusion",
                   "Shell result uses spherical ordinary weak-field mass lensing; not arbitrary modified metrics",
                   "Self-review only; no global novelty claim"]
}
(out / "results.json").write_text(json.dumps(result, indent=2) + "\n")
print(json.dumps({k: v for k, v in result.items() if k != "checks"}, indent=2))
print("All %d bounded controls passed." % len(checks))
