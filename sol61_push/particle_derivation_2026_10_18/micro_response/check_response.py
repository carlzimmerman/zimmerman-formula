"""Bounded algebra and finite checks for the explicit scalar response derivation.

This is a new calculation, not a reproduction of old halo runs. The long-wave
and analyticity claims are proved with their restrictions in DERIVATION.md.
"""
import json
import math
import sys
from pathlib import Path

import numpy as np
import scipy.optimize as opt
import sympy as s

out = Path(sys.argv[1])
assert out.is_dir()
checks = []


def check(name, value):
    ok = bool(value)
    checks.append({"name": name, "passed": ok})
    assert ok, name


# Obtain the carrier Hessian directly before imposing its background equations.
f, b, kc, c3, delta, mu, n = s.symbols("f b kc c3 delta mu n", real=True)
omega_nr = kc*f**4 + (delta-2*mu)*b**2 + 2*c3*b*f**2 - mu*f**2
Hnr = s.hessian(omega_nr, (f, b))/2
Hnr = Hnr.subs(mu, 2*kc*f**2+2*c3*b)
check("NR canonical amplitude Hessian 11", s.expand(Hnr[0, 0]-4*kc*f**2) == 0)
check("NR canonical amplitude Hessian 12", s.expand(Hnr[0, 1]-2*c3*f) == 0)
check("NR canonical amplitude Hessian 22", s.expand(Hnr[1, 1]-(delta-4*kc*f**2-4*c3*b)) == 0)

# The source-sector scalar in this formula is detuning, not its relativistic M.
Dc, kk, mass, source_mass = s.symbols("Dc k2 m M", positive=True)
Anr = 4*kc*n + kk/(2*mass)
Bnr2 = 4*c3**2*n
Dnr = Dc + kk/(2*source_mass)
check("NR source-mediated finite-range expansion", s.simplify(
    s.diff(Anr-Bnr2/Dnr, kk).subs(kk, 0)
    - (1/(2*mass)+2*c3**2*n/(source_mass*Dc**2))) == 0)
check("NR dilute local compressibility", s.simplify(
    (2*mass**2*n)/(4*n*(kc-c3**2/Dc))
    - mass**2/(2*(kc-c3**2/Dc))) == 0)
gs, lr = s.symbols("gs lambda_rep", positive=True)
full_prop = 1/(4*mass**2-source_mass**2)
split_prop = (1/(2*mass-source_mass)-1/(2*mass+source_mass))/(2*source_mass)
check("full source propagator frequency split", s.simplify(full_prop-split_prop) == 0)
lambda_total = lr+gs**2/(source_mass**2-4*mass**2)
lambda_rwa = lambda_total-gs**2/(2*source_mass*(source_mass-2*mass))
check("RWA threshold analytic mismatch", s.simplify(
    lambda_rwa-lr-gs**2/(2*source_mass*(source_mass+2*mass))) == 0)
check("fully matched threshold repulsion", s.simplify(
    lambda_total+gs**2*full_prop-lr) == 0)

# Canonical relativistic host: h= sqrt(2) delta f, t=delta chi.
host_f, chi, lam, aa, mm, nu, lc, w = s.symbols(
    "host_f chi lam a M2 nu lc w", real=True)
II = host_f**2
U = mm*chi**2/2 + nu*chi**3/3 + lc*chi**4/4
V = II + lam*II**2 + aa*chi*II + U
host_pot = V-w**2*II
H = s.hessian(host_pot, (host_f, chi))
H = s.diag(1/s.sqrt(2), 1)*H*s.diag(1/s.sqrt(2), 1)
stat_w2 = 1+2*lam*host_f**2+aa*chi
check("host canonical static Hessian 11", s.simplify(H[0, 0].subs(w**2, stat_w2)-4*lam*II) == 0)
check("host canonical static Hessian 12", s.simplify(H[0, 1]-s.sqrt(2)*aa*host_f) == 0)
check("host canonical static Hessian 22", s.simplify(H[1, 1]-s.diff(U, chi, 2)) == 0)

NN = s.symbols("N", positive=True)
lapse_L = w**2*II/NN-NN*V
seagull = s.diff(lapse_L, NN, 2).subs(NN, 1)
check("lapse explicit second derivative", s.simplify(seagull-2*w**2*II) == 0)
qf = -s.diff(lapse_L, NN, host_f).subs(NN, 1)/s.sqrt(2)
check("lapse amplitude source", s.simplify(qf.subs(w**2, stat_w2)-2*s.sqrt(2)*stat_w2*host_f) == 0)

A, B, D, W, K2, O2 = s.symbols("A B D W K2 O2", positive=True)
K = s.Matrix([[K2+A, B], [B, K2+D]])
check("host static inverse Schur complement", s.simplify(K.inv()[0, 0]-1/(K2+A-B**2/(K2+D))) == 0)
check("host analytic derivative expansion", s.simplify(
    s.diff(K2+A-B**2/(K2+D), K2).subs(K2, 0)-(1+B**2/D**2)) == 0)
Om = s.symbols("Om", real=True)
dyn = s.Matrix([[K2+A-Om**2, -2*s.I*W*Om, B],
                [2*s.I*W*Om, K2-Om**2, 0],
                [B, 0, K2+D-Om**2]])
expected_det = (K2-Om**2)*((K2+A-Om**2)*(K2+D-Om**2)-B**2)-4*W**2*Om**2*(K2+D-Om**2)
check("phase-amplitude-mediator determinant", s.expand(dyn.det()-expected_det) == 0)
check("positive-gap amplitude roots at k=0", s.simplify(
    expected_det.subs(K2, 0)+Om**2*((A+4*W**2-Om**2)*(D-Om**2)-B**2)) == 0)
check("Goldstone sound coefficient", s.simplify(
    -(s.diff(expected_det, K2).subs({K2: 0, Om: 0}))
    /(s.diff(expected_det.subs(Om**2, O2), O2).subs({K2: 0, O2: 0}))
    -(A-B**2/D)/(A-B**2/D+4*W**2)) == 0)

# Exact target has an odd |P|^3 term even after critical quadratic subtraction.
u, a0, grav = s.symbols("u a0 Kgrav", positive=True)
Wfull = (-a0*u-a0**2*s.log(1-u/a0))/grav
Wrem = Wfull-u**2/(2*grav)
check("full target derivative", s.simplify(grav*s.diff(Wfull, u)-a0*u/(a0-u)) == 0)
check("residual target derivative", s.simplify(grav*s.diff(Wrem, u)-u**2/(a0-u)) == 0)
check("residual leading cubic", s.simplify(s.limit(Wrem/u**3, u, 0, dir="+")-1/(3*grav*a0)) == 0)

# Direct integration rederives the changed nodal-band route; no external theorem.
q, gap, cutoff = s.symbols("q gap cutoff", positive=True)
radial = q*(s.sqrt(q*q+gap*gap)-q)
anti = ((q*q+gap*gap)**s.Rational(3, 2)-q**3)/3
check("nodal-band radial antiderivative", s.simplify(s.diff(anti, q)-radial) == 0)
ren = -((cutoff**2+gap**2)**s.Rational(3, 2)-cutoff**3-gap**3)/3+cutoff*gap**2/2
check("nodal-band positive cubic coefficient", s.limit(ren/gap**3, gap, 0, dir="+") == s.Rational(1, 3))

# Concrete changed branch: tune the bare quartic to 2, holding the real mediator.
Mcrit, Ic, xc, epsc, mc, nnc, g2c, g3c, Xc = s.symbols(
    "Mc Ic xc epsc mc nnc g2c g3c Xc", positive=True)
chiseries = (-2*Ic/Mcrit+s.Rational(3, 2)*Ic**2/Mcrit**3
             +s.Rational(23, 4)*Ic**3/Mcrit**5)
Ucrit = Mcrit**2*chi**2/2-Mcrit*chi**3/8+chi**4/4
stationary_residual = s.diff(Ucrit, chi)+2*Mcrit*Ic
check("critical mediator series through I cubed", s.series(
    stationary_residual.subs(chi, chiseries), Ic, 0, 4).removeO().expand() == 0)
Vcrit = mc**2*Ic+(2+epsc)*Ic**2+2*Mcrit*chi*Ic+Ucrit
effective_series = s.series(Vcrit.subs(chi, chiseries), Ic, 0, 5).removeO()
check("critical effective potential through I fourth", s.simplify(
    effective_series-(mc**2*Ic+epsc*Ic**2+Ic**3/Mcrit**2
                      +s.Rational(23, 8)*Ic**4/Mcrit**4)) == 0)
Iparam = Mcrit*xc/2+3*xc**2/16+xc**3/(2*Mcrit)
Sparam = 3*xc**2/4+2*xc**3/Mcrit
check("critical exact mediator parameterization", s.simplify(
    stationary_residual.subs({chi: -xc, Ic: Iparam})) == 0)
check("critical exact positive-S parameterization", s.simplify(
    (s.diff(Vcrit, Ic)-mc**2).subs({epsc: 0, chi: -xc, Ic: Iparam})-Sparam) == 0)
check("critical exact convex derivative", s.simplify(
    s.diff(Sparam, xc)/s.diff(Iparam, xc)
    -(4-4*Mcrit**2/(Mcrit**2+3*Mcrit*xc/4+3*xc**2))) == 0)
ncrit = s.sqrt(Xc/g3c)
critical_pressure = s.simplify(ncrit*Xc-g3c*ncrit**3/3)
check("critical NR Legendre pressure", s.simplify(
    critical_pressure-2*Xc**s.Rational(3, 2)/(3*s.sqrt(g3c))) == 0)
check("critical density derivative", s.simplify(s.diff(critical_pressure, Xc)-ncrit) == 0)
check("critical stable compressibility", s.simplify(
    s.diff(critical_pressure, Xc, 2)-1/(2*s.sqrt(g3c*Xc))) == 0)
g2negative = s.symbols("g2negative", negative=True)
nt = -3*g2negative/(4*g3c)
Ut = g2negative*nnc**2/2+g3c*nnc**3/3
Xt = -3*g2negative**2/(16*g3c)
check("attractive-quartic coexistence slope", s.simplify(s.diff(Ut, nnc).subs(nnc, nt)-Xt) == 0)
check("attractive-quartic coexistence zero pressure", s.simplify((nnc*Xt-Ut).subs(nnc, nt)) == 0)
YY, pp = s.symbols("Y p", positive=True)
Pnegative = -2*YY**s.Rational(3, 2)/(3*s.sqrt(g3c))  # X=-Y
check("continued negative-X branch has negative time kinetic coefficient", s.diff(Pnegative, YY, 2) < 0)

rows = []
for M in (1., 10., 100., 1000.):
    ell = 2-1/M
    a = 2*M
    cubic = -3*M/8

    # This rescaled coexistence polynomial is strictly increasing for x>0.
    def poly(x):
        return (ell*x**4/M**3+3*ell*x**3/(4*M**2)
                +(137*ell/64-1)*x*x/M+(3*ell/4-.5)*x-1)

    x = opt.brentq(poly, 0, 4, xtol=1e-14, rtol=1e-14)
    chi0 = -x
    U0 = M*M*x*x/2+M*x**3/8+x**4/4
    I0 = math.sqrt(U0/ell)
    w2 = 1+2*ell*I0-a*x
    Ar = 4*ell*I0
    Br = math.sqrt(2)*a*math.sqrt(I0)
    Dr = M*M+2*cubic*chi0+3*chi0**2
    Aeff = Ar-Br**2/Dr
    Z = 1+Br**2/Dr**2
    qsq = 8*w2*w2*I0
    seagull_r = 2*w2*I0
    susceptibility0 = seagull_r+qsq/Aeff
    cs2 = Aeff/(Aeff+4*w2)
    static_eig = np.linalg.eigvalsh([[Ar, Br], [Br, Dr]])
    dynamic_gap2 = np.linalg.eigvalsh([[Ar+4*w2, Br], [Br, Dr]])
    check("strict homogeneous static amplitude curvature M="+str(M), min(static_eig) > 0)
    check("positive dynamical amplitude gaps M="+str(M), min(dynamic_gap2) > 0)
    check("positive subluminal Goldstone speed M="+str(M), 0 < cs2 < 1)
    check("enthalpy compressibility identity M="+str(M), abs(susceptibility0-seagull_r/cs2)/susceptibility0 < 3e-14)

    # Thermodynamic derivative from the independent scalar stationarity equation.
    # Finite differences are a diagnostic; exact identities above are the proof.
    def energy_in_lapse(N):
        xi = w2/N**2

        def eq(c):
            density = (xi-1-a*c)/(2*ell)
            return M*M*c+cubic*c*c+c**3+a*density

        root = opt.brentq(eq, chi0-.1, chi0+.1, xtol=2e-14, rtol=2e-14)
        density = (xi-1-a*root)/(2*ell)
        potential = density+ell*density**2+a*root*density+M*M*root**2/2+cubic*root**3/3+root**4/4
        return xi*density+potential

    eps = 1e-5
    slope1 = -(energy_in_lapse(1+eps)-energy_in_lapse(1-eps))/(2*eps)
    eps = 5e-6
    slope2 = -(energy_in_lapse(1+eps)-energy_in_lapse(1-eps))/(2*eps)
    fd_error = abs(slope2/susceptibility0-1)
    check("direct nonlinear lapse response M="+str(M), fd_error < 8e-6)
    check("refined nonlinear lapse derivative M="+str(M), abs(slope1-slope2)/susceptibility0 < 8e-6)
    finite_k = []
    for kval in (0., .01, .1, 1., 10.):
        mat = np.array([[Ar+kval*kval, Br], [Br, Dr+kval*kval]])
        direct = seagull_r+qsq*np.linalg.inv(mat)[0, 0]
        schur = seagull_r+qsq/(kval*kval+Ar-Br**2/(Dr+kval*kval))
        check("direct matrix vs Schur M,k="+str((M,kval)), abs(direct/schur-1) < 2e-12)
        finite_k.append({"k_over_host_vacuum_mass": kval, "minus_d_rho_d_lapse": schur})
    rows.append({"M_over_host_mass": M, "I": I0, "chi": chi0, "omega_squared": w2,
                 "static_amplitude_curvature_eigenvalues": static_eig.tolist(),
                 "dynamical_amplitude_gap_squared": dynamic_gap2.tolist(),
                 "A_eff": Aeff, "amplitude_gradient_factor_Z": Z,
                 "sound_speed_squared": cs2, "enthalpy": seagull_r,
                 "density_lapse_susceptibility_at_zero_k": susceptibility0,
                 "independent_nonlinear_derivative_relative_error": fd_error,
                 "finite_k": finite_k})

result = {
    "assertion_tested": "Exact static amplitude Hessians, source/Schur/phase identities, target cubic and nodal integral; finite independent lapse-response and matrix comparisons at four mediator masses and five momenta.",
    "status": "implementation and finite assertion verified in the stated range",
    "checks": checks,
    "checks_count": len(checks),
    "host_rows": rows,
    "non_claims": [
        "No observational validation or universal exclusion of gapless, critical, anisotropic or nonanalytic completions.",
        "No claim that the produced dilute carrier is condensed or occupies the homogeneous charged-host branch.",
        "Static homogeneous host lapse susceptibility is not a full self-consistent relativistic galaxy/Einstein solution.",
        "No physical a0, kappa or vacuum-energy normalization is fixed.",
        "No all-loop analyticity proof for gapless phonons; the analytic obstruction concerns the stated finite static amplitude gap, regular analytic state/derivative expansion."
    ]
}
(out/"results.json").write_text(json.dumps(result, indent=2)+"\n")
print(json.dumps({"checks": len(checks), "host_rows": [{k: row[k] for k in (
    "M_over_host_mass", "A_eff", "sound_speed_squared", "density_lapse_susceptibility_at_zero_k",
    "independent_nonlinear_derivative_relative_error")} for row in rows]}, indent=2))
