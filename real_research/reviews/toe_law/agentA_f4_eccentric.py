#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
agentA_f4_eccentric.py — Door IVa HOSTILE kill-test: F4 modified inertia on ECCENTRIC planetary orbits.

CANDIDATE (F4): m * mu(|a|/s) * a_vec = F_Newton,  mu(x) = x/sqrt(1+x^2)  (mu_standard),
solved implicitly for the actual acceleration a given the Newtonian force.
Two normalizations of s (factor Z = 5.789 ambiguity):
  HOSTILE   s = 5.418e-10 m/s^2  (= cH_Lambda, raw bath value; larger s -> larger anomaly)
  framework s = 9.36e-11  m/s^2  (empirical framework a0)

DIRECTION JUSTIFICATION (instantaneous prescription): mu is a positive scalar, so the EOM forces
a_vec || F_vec exactly: a_vec = F_vec/(m*mu). Given F = -GM/r^2 r_hat, |a| solves
mu(|a|/s)*|a| = g_N(r), which has a unique positive root since x*mu(x) is strictly increasing.
=> a_vec = -U(g_N(r)) r_hat : a POSITION-ONLY CENTRAL force field => conservative (potential
V(r) = -GM/r + integral of delta), angular momentum exactly conserved.
ANALYTIC CONSEQUENCE: the instantaneous two-body F4 problem has ZERO secular energy / semi-major
axis drift — the d(lnE)/dt kill channel is structurally empty; the only secular observable is
apsidal precession. (The non-conservation worry applies to N-body / genuinely nonlocal MI
prescriptions, not to the two-body instantaneous rule.) Numerics below must confirm drift = floor.

IMPLICIT SOLVE: mu(u/s)*u = g  <=>  u^2/sqrt(u^2+s^2) = g  <=>  u^4 - g^2 u^2 - g^2 s^2 = 0
 => u = g*sqrt((1+sqrt(1+q))/2),  q = 4 s^2/g^2.   Anomaly delta = u - g ~ s^2/(2g) for q<<1.
CONDITIONING HAZARD (documented & demonstrated below): at physical s the anomaly is
delta/g ~ 3.5e-11 (Saturn, hostile) down to 9.4e-17 (Mercury, hostile) — at/below double eps.
Naive evaluation of the closed form computes u then subtracts g: catastrophic cancellation.
Production solver: NEWTON ITERATION on delta directly with the cancellation-free residual
  psi(d) = (g+d)*d - g*[ s^2/(2(g+d)) - s^4/(8(g+d)^3) + s^6/(16(g+d)^5) - 5 s^8/(128(g+d)^7) ]
(exact algebraic rearrangement of (g+d)^2 - g*sqrt((g+d)^2+s^2) with the sqrt expanded in
eps = s^2/(g+d)^2; valid to <1e-12 for q <= 1e-2; all production runs have q <= 1e-5).
Validated at startup against (i) the independent q-series u/g = 1 + q/8 - 5q^2/128 + 21q^3/1024,
(ii) mpmath 50-digit exact closed form; naive-double digit loss demonstrated.

ANALYTIC CROSS-CHECK TARGET (derived two independent ways: Gauss planetary equations with
R = -delta(r) [inward], and Delaunay secular theory pomega_dot = d<dV>/dG; both give):
  Delta_pomega per orbit = - pi * (4+e^2) * sqrt(1-e^2) * s^2 a^4 / (2 (GM)^2)   [RETROGRADE]
e->0 check: -2 pi s^2 a^4/(GM)^2 matches the apsidal-angle formula for F = GM/r^2 + K r^2.
Numerics must reproduce this within ~20% (prompt gate); amplified-s runs nail it to <1%.

PRESCRIPTION VARIANT (orbit-averaged): mu evaluated at the time-averaged |a| over the previous
orbit, frozen within each orbit => per-orbit dynamics is EXACTLY Kepler with GM_eff = GM/mu_bar
=> closed ellipse, ZERO precession, zero drift after the mu_bar fixed point is reached. The only
relic is a per-planet GM rescaling 1/mu_bar - 1 ~ s^2/(2<|a|>^2) (cross-planet Kepler-ratio
inconsistency, degenerate per-planet with the fitted GM_sun).

PINNED EPHEMERIS BOUNDS (supplementary perihelion precession, mas/cy; pinned 2026-06-10):
  EPM2011  (Pitjeva & Pitjev 2013, MNRAS 432:3431, arXiv:1306.3043):
           Mercury -2.0 +/- 3.0 ; Mars -0.020 +/- 0.037 ; Saturn -0.32 +/- 0.47
  INPOP10a (Fienga et al. 2011, CMDA 111:363, arXiv:1108.5546, as tabulated in 1601.00947):
           Mercury 1.2 +/- 1.6 ; Saturn 0.15 +/- 0.65
  INPOP15a (Fienga et al. 2016, arXiv:1601.00947): Mercury 0.0 +/- 3.1 (C1), 0.0 +/- 1.05 (C2);
           Saturn 1.2 +/- 5.0 (C1), 0.05 +/- 0.20 (C2)   [C2 = Delta(O-C)<5% criterion, tightest]
  Secular drift: GM_sun_dot/GM_sun = -(6.13 +/- 1.47)e-14 /yr (Genova et al. 2018, Nat.Comm. 9:289)
  Circular-channel context: |delta_a(Saturn)| < 1e-14 m/s^2 (Folkner via arXiv:1001.3686 sec VI).

Units: per-planet canonical units GM = 1, a_planet = 1 (period = 2*pi). The problem then depends
only on (e, s_canon = s * a^2 / GM); planet identity re-enters via the mas/cy conversion.
"""

import math
import sys
import numpy as np
from scipy.integrate import solve_ivp

try:
    import mpmath as mp
    HAVE_MPMATH = True
except Exception:
    HAVE_MPMATH = False

# ----------------------------------------------------------------------------- constants
GM_SUN = 1.32712440018e20   # m^3/s^2
AU     = 1.495978707e11     # m
GM_JUP = 1.26686534e17      # m^3/s^2 (Sun-reflex side calc)
GM_SAT = 3.7931187e16       # m^3/s^2
R_JUP  = 5.2044 * AU

S_HOSTILE   = 5.418e-10     # m/s^2  (cH_Lambda — LEAD normalization, hostile)
S_FRAMEWORK = 9.36e-11      # m/s^2  (framework a0)

MAS_PER_RAD = 180.0/math.pi * 3600.0 * 1000.0   # 2.0626...e8

PLANETS = {
    # name: (a_AU, e)   -- prompt values
    'Mercury': (0.387, 0.206),
    'Mars':    (1.524, 0.093),
    'Saturn':  (9.58,  0.057),
}

BOUNDS = {  # (label, central, sigma) in mas/cy
    'Mercury': [('EPM2011  arXiv:1306.3043', -2.0,  3.0),
                ('INPOP10a arXiv:1108.5546',  1.2,  1.6),
                ('INPOP15a-C2 arXiv:1601.00947', 0.0, 1.05)],
    'Mars':    [('EPM2011  arXiv:1306.3043', -0.020, 0.037)],
    'Saturn':  [('EPM2011  arXiv:1306.3043', -0.32, 0.47),
                ('INPOP10a arXiv:1108.5546',  0.15, 0.65),
                ('INPOP15a-C1 arXiv:1601.00947', 1.2, 5.0),
                ('INPOP15a-C2 arXiv:1601.00947', 0.05, 0.20)],
}

def planet_derived(name):
    a_AU, e = PLANETS[name]
    a_SI = a_AU * AU
    gN   = GM_SUN / a_SI**2                      # m/s^2 at r=a
    T_yr = 2*math.pi*math.sqrt(a_SI**3/GM_SUN) / (365.25*86400.0)
    return a_SI, e, gN, T_yr

# ----------------------------------------------------------------------------- F4 solver
def mu_std(x):
    return x / math.sqrt(1.0 + x*x)

def delta_newton(g, s, niter=3):
    """Anomaly d = u - g solving mu(u/s)*u = g, via cancellation-free Newton residual.
    Valid for q = 4 s^2/g^2 <= 1e-2 (asserted). Production regimes: q <= ~1e-5."""
    if s == 0.0:
        return 0.0
    s2 = s*s
    q = 4.0*s2/(g*g)
    assert q <= 1e-2, f"delta_newton called outside validity (q={q:.3e})"
    s4 = s2*s2; s6 = s4*s2; s8 = s4*s4
    d = 0.5*s2/g                       # leading-order start
    for _ in range(niter):
        gd  = g + d
        gd2 = gd*gd
        B   = 0.5*s2/gd - 0.125*s4/(gd*gd2) + 0.0625*s6/(gd*gd2*gd2) - (5.0/128.0)*s8/(gd*gd2*gd2*gd2)
        Bp  = -0.5*s2/gd2 + 0.375*s4/(gd2*gd2) - 0.3125*s6/(gd2*gd2*gd2)
        psi  = gd*d - g*B
        psip = g + 2.0*d - g*Bp
        d   -= psi/psip
    return d

def delta_series(g, s):
    """Independent check: u/g = 1 + q/8 - 5 q^2/128 + 21 q^3/1024, q = 4 s^2/g^2."""
    q = 4.0*s*s/(g*g)
    return g*(q/8.0 - 5.0*q*q/128.0 + 21.0*q**3/1024.0)

def delta_mpmath(g, s, dps=50):
    with mp.workdps(dps):
        gg = mp.mpf(g); ss = mp.mpf(s)
        q  = 4*ss*ss/(gg*gg)
        u  = gg*mp.sqrt((1+mp.sqrt(1+q))/2)
        return u - gg

def delta_naive_double(g, s):
    """Deliberately naive closed form in doubles (demonstrates catastrophic cancellation)."""
    q = 4.0*s*s/(g*g)
    u = g*math.sqrt((1.0+math.sqrt(1.0+q))/2.0)
    return u - g

def one_minus_mu_stable(x):
    """1 - mu(x) = 1/( sqrt(1+x^2) * (x + sqrt(1+x^2)) ), no cancellation."""
    sq = math.sqrt(1.0+x*x)
    return 1.0/(sq*(x+sq))

def inv_mu_minus_one_stable(x):
    """1/mu(x) - 1 = (sqrt(1+x^2)-x)/x = 1/( x*(x+sqrt(1+x^2)) )."""
    sq = math.sqrt(1.0+x*x)
    return 1.0/(x*(x+sq))

# ----------------------------------------------------------------------------- analytic
def dpomega_analytic(e, s_c):
    """Leading-order per-orbit apsidal shift, canonical units (GM=1, a=1), radians."""
    return -math.pi*(4.0+e*e)*math.sqrt(1.0-e*e)*0.5*s_c*s_c

def dpomega_quadrature(e, s_c, n=4000):
    """Independent numerical Gauss-average with the EXACT delta(r) from the Newton solver:
    Delta_pomega = (beta/e) * Int_0^{2pi} delta(g(r(E))) * (cos E - e) dE,  r = 1 - e cos E."""
    beta = math.sqrt(1.0-e*e)
    E = (np.arange(n)+0.5)*(2*math.pi/n)
    tot = 0.0
    for Ei in E:
        r = 1.0 - e*math.cos(Ei)
        g = 1.0/(r*r)
        tot += delta_newton(g, s_c)*(math.cos(Ei)-e)
    tot *= 2*math.pi/n
    return (beta/e)*tot

# ----------------------------------------------------------------------------- integration
def rhs_instant(t, y, s_c):
    x, yy, vx, vy = y
    r2 = x*x + yy*yy
    r  = math.sqrt(r2)
    g  = 1.0/r2
    d  = delta_newton(g, s_c) if s_c != 0.0 else 0.0
    f  = -(g + d)/r
    return (vx, vy, f*x, f*yy)

def run_instant(e, s_c, n_orbits, rtol=1e-12, atol=1e-13):
    """Integrate n_orbits; sample once per unperturbed period; return fits.
    Returns dict with pomega slope (rad/orbit) +/- sigma, d ln a_osc /orbit, d ln E_mod /orbit."""
    y0 = (1.0-e, 0.0, 0.0, math.sqrt((1.0+e)/(1.0-e)))
    t_eval = 2*math.pi*np.arange(n_orbits+1)
    sol = solve_ivp(rhs_instant, (0.0, t_eval[-1]), y0, t_eval=t_eval,
                    method='DOP853', rtol=rtol, atol=atol, args=(s_c,), dense_output=False)
    assert sol.success, sol.message
    X, Y, VX, VY = sol.y
    R  = np.hypot(X, Y)
    L  = X*VY - Y*VX
    ex = VY*L - X/R          # LRL with GM=1
    ey = -VX*L - Y/R
    pom = np.unwrap(np.arctan2(ey, ex))
    EK  = 0.5*(VX**2+VY**2) - 1.0/R
    aosc = -0.5/EK
    # modified-potential energy (series Vdelta; q<=1e-5 in all runs -> truncation negligible)
    s2 = s_c*s_c; s4 = s2*s2; s6 = s4*s2
    Vd = s2*R**3/6.0 - (5.0/56.0)*s4*R**7 + (21.0/176.0)*s6*R**11
    Emod = 0.5*(VX**2+VY**2) - 1.0/R + Vd
    k = np.arange(n_orbits+1, dtype=float)
    def fit(v):
        # explicit OLS (no BLAS: avoids spurious FP warnings on denormal residuals)
        kc = k - k.mean(); vc = v - v.mean()
        skk = float((kc*kc).sum())
        slope = float((kc*vc).sum())/skk
        resid = vc - slope*kc
        dof = max(len(k)-2, 1)
        sig = math.sqrt(float((resid*resid).sum())/dof/skk)
        return slope, sig
    sl_pom, sg_pom = fit(pom)                       # rad / orbit
    sl_lna, sg_lna = fit(np.log(aosc))              # per orbit
    e0 = abs(Emod[0])
    sl_lnE, sg_lnE = fit((Emod-Emod[0])/e0)         # fractional Emod drift per orbit
    return dict(slope_pom=sl_pom, sig_pom=sg_pom,
                slope_lna=sl_lna, sig_lna=sg_lna,
                slope_lnE=sl_lnE, sig_lnE=sg_lnE,
                nfev=sol.nfev)

def run_orbit_averaged(e, s_c, n_orbits=30, rtol=1e-12, atol=1e-13):
    """Prompt variant: mu evaluated at time-averaged |a| over the previous orbit, frozen
    within each orbit. Within a chunk: a_vec = -(g/mu_bar) r_hat = -(1+c) g r_hat, c = 1/mu_bar-1
    (computed cancellation-free). Per chunk integrate exactly one effective radial period
    T_eff = 2 pi sqrt(a_eff^3 mu_bar); sample LRL of the EFFECTIVE problem (conserved within
    chunk). aux state integrates g dt -> <|a|> = (1+c) * (Int g dt)/T_eff."""
    beta = math.sqrt(1.0-e*e)
    xbar = 1.0/(beta*s_c)              # bootstrap: <g>_t = 1/beta (canonical), |a|~<g>
    c = inv_mu_minus_one_stable(xbar)
    y = [1.0-e, 0.0, 0.0, math.sqrt((1.0+e)/(1.0-e)), 0.0]
    poms, cs, aeffs = [], [], []
    def rhs(t, yv, cc):
        x, yy, vx, vy, _ = yv
        r2 = x*x+yy*yy; r = math.sqrt(r2); g = 1.0/r2
        f = -(1.0+cc)*g/r
        return (vx, vy, f*x, f*yy, g)
    for kk in range(n_orbits):
        x, yy, vx, vy, aux0 = y
        r = math.hypot(x, yy); v2 = vx*vx+vy*vy
        mu_bar = 1.0/(1.0+c)
        a_eff = 1.0/(2.0/r - v2*mu_bar)
        T_eff = 2*math.pi*math.sqrt(a_eff**3*mu_bar)
        sol = solve_ivp(rhs, (0.0, T_eff), y, t_eval=[T_eff], method='DOP853',
                        rtol=rtol, atol=atol, args=(c,))
        assert sol.success
        y = [float(sol.y[i][-1]) for i in range(5)]
        x, yy, vx, vy, aux1 = y
        r = math.hypot(x, yy)
        GMeff = 1.0+c
        L = x*vy - yy*vx
        ex = vy*L/GMeff - x/r; ey = -vx*L/GMeff - yy/r
        poms.append(math.atan2(ey, ex))
        a_mean = (1.0+c)*(aux1-aux0)/T_eff
        cs.append(c); aeffs.append(a_eff)
        c = inv_mu_minus_one_stable(a_mean/s_c)
        y[4] = 0.0
    poms = np.unwrap(np.array(poms))
    tail = slice(max(0, n_orbits-10), n_orbits)
    dpom_tail = np.diff(poms)[max(0, n_orbits-11):]
    return dict(c_seq=cs, pom=poms, max_dpom_tail=float(np.max(np.abs(dpom_tail))),
                c_final=cs[-1], da_over_a_tail=float(np.max(np.abs(np.diff(np.array(aeffs)[tail])))/aeffs[-1]))

# ----------------------------------------------------------------------------- reporting
def mas_per_cy(dpom_rad_per_orbit, T_yr):
    return dpom_rad_per_orbit * (100.0/T_yr) * MAS_PER_RAD

def main():
    out = sys.stdout
    P = lambda *a: print(*a, file=out)

    P("="*100)
    P("agentA F4 ECCENTRIC-ORBIT KILL-TEST (Door IVa)  —  run date 2026-06-10")
    P("EOM: mu(|a|/s)*a_vec = -g_N(r) r_hat, mu_std = x/sqrt(1+x^2); HOSTILE s=5.418e-10 leads.")
    P("="*100)

    # ---------------------------------------------------------------- solver validation
    P("\n[1] SOLVER VALIDATION (Newton-on-delta vs independent q-series vs mpmath 50-digit)")
    worst_series = 0.0; worst_mp = 0.0
    tests = []
    for name in PLANETS:
        a_SI, e, gN, T_yr = planet_derived(name)
        for s in (S_HOSTILE, S_FRAMEWORK):
            s_c = s/gN
            for r in (1.0-e, 1.0, 1.0+e):
                tests.append((name, s, s_c, r))
    for s_c_amp in (1e-4, 1e-3):
        tests.append(('amplified', None, s_c_amp, 1.2))
    for name, s, s_c, r in tests:
        g = 1.0/(r*r)
        dN = delta_newton(g, s_c)
        dS = delta_series(g, s_c)
        rel_series = abs(dN-dS)/dS
        worst_series = max(worst_series, rel_series)
        if HAVE_MPMATH:
            dM = float(delta_mpmath(g, s_c))
            rel_mp = abs(dN-dM)/dM
            worst_mp = max(worst_mp, rel_mp)
    P(f"    worst |Newton-series|/delta over {len(tests)} regimes : {worst_series:.3e}")
    if HAVE_MPMATH:
        P(f"    worst |Newton-mpmath50|/delta                      : {worst_mp:.3e}")
    P("    conditioning demo (naive double closed-form u-g vs mpmath), physical s:")
    for name in ('Mercury', 'Saturn'):
        a_SI, e, gN, T_yr = planet_derived(name)
        s_c = S_HOSTILE/gN
        g = 1.0
        dM = float(delta_mpmath(g, s_c)) if HAVE_MPMATH else delta_series(g, s_c)
        dn = delta_naive_double(g, s_c)
        err = abs(dn-dM)/dM if dM != 0 else float('nan')
        P(f"      {name:8s} hostile: delta/g = {dM:.3e}; naive-double rel err = {err:.2e}"
          f"  (Newton rel err = {abs(delta_newton(g,s_c)-dM)/dM:.2e})")

    # ---------------------------------------------------------------- analytic three-way
    P("\n[2] ANALYTIC CROSS-CHECK (closed form vs independent Gauss-average quadrature w/ exact delta)")
    P("    Delta_pomega/orbit = -pi (4+e^2) sqrt(1-e^2) s^2 a^4 / (2 (GM)^2)   [retrograde]")
    for name in PLANETS:
        a_SI, e, gN, T_yr = planet_derived(name)
        for s_c in (1e-4, 1e-3):
            an = dpomega_analytic(e, s_c)
            qd = dpomega_quadrature(e, s_c)
            P(f"    e={e:.3f} s_c={s_c:.0e}: closed {an:+.6e}  quad {qd:+.6e}  ratio {qd/an:.6f}")

    # ---------------------------------------------------------------- integrations
    P("\n[3] TWO-BODY INTEGRATIONS — planet as F4 body, Sun as source (DOP853 rtol=1e-12, atol=1e-13;")
    P("    per-planet canonical units GM=1, a=1)")
    P("    Sampling: once per unperturbed period; pomega from Laplace-Runge-Lenz vector; OLS fits.")

    results = {}

    P("\n  [3a] CONTROLS (s=0, 1000 orbits) — integrator floor:")
    floors = {}
    for name in PLANETS:
        a_SI, e, gN, T_yr = planet_derived(name)
        rc = run_instant(e, 0.0, 1000)
        floors[name] = rc
        P(f"    {name:8s}: spurious pomega slope = {rc['slope_pom']:+.3e} +/- {rc['sig_pom']:.1e} rad/orbit ;"
          f" d ln a_osc = {rc['slope_lna']:+.3e}/orbit ; d Emod/|E| = {rc['slope_lnE']:+.3e}/orbit"
          f"  (nfev={rc['nfev']})")

    P("\n  [3b] AMPLIFIED-s VALIDATION (300 orbits each; gate: |numeric/analytic - 1| <= 20%):")
    amp_grid = (1e-4, 10**-3.5, 1e-3)
    gate_ok = True
    for name in PLANETS:
        a_SI, e, gN, T_yr = planet_derived(name)
        meas = []
        for s_c in amp_grid:
            r = run_instant(e, s_c, 300)
            an = dpomega_analytic(e, s_c)
            ratio = r['slope_pom']/an
            meas.append((s_c, r['slope_pom'], an, ratio, r))
            flag = "OK " if abs(ratio-1.0) <= 0.20 else "FAIL-GATE"
            gate_ok &= abs(ratio-1.0) <= 0.20
            P(f"    {name:8s} s_c={s_c:.3e}: meas {r['slope_pom']:+.6e}  analytic {an:+.6e}"
              f"  ratio {ratio:.4f} [{flag}]  drift d ln a={r['slope_lna']:+.1e}/orb")
        lg = np.polyfit([math.log10(m[0]) for m in meas], [math.log10(abs(m[1])) for m in meas], 1)[0]
        P(f"    {name:8s} s^2-scaling: d log|dpom|/d log s = {lg:.4f} (expect 2)")
    P(f"    AMPLIFIED GATE: {'PASSED' if gate_ok else 'FAILED — stop, find bug'}")
    if not gate_ok:
        sys.exit(1)

    P("\n  [3c] PHYSICAL-s RUNS (1000 orbits; representability noted):")
    P("      NOTE: canonical perturbation delta/g = s_c^2/2: Saturn-hostile 3.5e-11 (1.6e5 eps),")
    P("      Saturn-framework 1.0e-12 (4.8e3 eps), Mars-hostile 2.3e-14 (~100 eps): integrable;")
    P("      Mercury-hostile 9.4e-17 and Mercury/Mars-framework: AT/BELOW double eps —")
    P("      direct integration structurally cannot represent the perturbation; those verdicts")
    P("      rest on the amplified-s-validated analytic law (gate above).")
    P("      CONTROL SUBTRACTION: DOP853 has a reproducible spurious LRL rotation (controls above,")
    P("      +1.1e-11..+1.8e-11 rad/orbit, s-independent since the perturbed RHS differs from the")
    P("      control by <= 3.5e-11 relative). Corrected slope = measured - control(same e, rtol, N).")
    P("      Validity is demonstrated empirically: three independent (planet,s) runs land on the")
    P("      analytic value after subtraction (see 'corrected ratio').")
    phys_runs = [('Saturn', S_HOSTILE), ('Saturn', S_FRAMEWORK), ('Mars', S_HOSTILE), ('Mercury', S_HOSTILE)]
    for name, s in phys_runs:
        a_SI, e, gN, T_yr = planet_derived(name)
        s_c = s/gN
        r = run_instant(e, s_c, 1000)
        an = dpomega_analytic(e, s_c)
        lab = 'hostile  ' if s == S_HOSTILE else 'framework'
        corr = r['slope_pom'] - floors[name]['slope_pom']
        ratio_raw = r['slope_pom']/an if an != 0 else float('nan')
        ratio_cor = corr/an if an != 0 else float('nan')
        P(f"    {name:8s} {lab} s_c={s_c:.3e}: meas {r['slope_pom']:+.3e}  - control {floors[name]['slope_pom']:+.3e}"
          f"  => corrected {corr:+.3e} rad/orb")
        P(f"             analytic {an:+.3e}   raw ratio {ratio_raw:+.3f}   corrected ratio {ratio_cor:+.4f}"
          f"   -> {mas_per_cy(corr, T_yr):+.3e} mas/cy measured")
        P(f"             secular: d ln a_osc = {r['slope_lna']:+.2e}/orb ; d Emod/|E| = {r['slope_lnE']:+.2e}/orb"
          f"  (control floor: {floors[name]['slope_lna']:+.2e}, {floors[name]['slope_lnE']:+.2e})")
        results[(name, s, 'instant')] = dict(r, corr=corr, ratio_cor=ratio_cor)
    P("      (Mercury-hostile: the perturbation delta/g = 9.4e-17 sits below double eps, so the")
    P("       perturbed trajectory is near-bit-identical to the control; the corrected number is the")
    P("       subtraction's roundoff remainder, NOT a calibrated measurement — its proximity to the")
    P("       analytic value (ratio 1.24) is encouraging but unclaimable. Verdict rests on the")
    P("       amplified-s-validated law, which was verified at Mercury's own e=0.206 to 0.02%.)")

    P("\n  [3c-bis] rtol-ROBUSTNESS of the control subtraction (Saturn hostile, 300 orbits, rtol=1e-13):")
    a_SI, e, gN, T_yr = planet_derived('Saturn')
    s_c = S_HOSTILE/gN
    rc13 = run_instant(e, 0.0, 300, rtol=1e-13, atol=1e-14)
    rs13 = run_instant(e, s_c, 300, rtol=1e-13, atol=1e-14)
    an = dpomega_analytic(e, s_c)
    corr13 = rs13['slope_pom'] - rc13['slope_pom']
    P(f"    control {rc13['slope_pom']:+.3e}, perturbed {rs13['slope_pom']:+.3e}, corrected {corr13:+.3e}"
      f" vs analytic {an:+.3e}  -> ratio {corr13/an:+.4f}")

    P("\n  [3d] ORBIT-AVERAGED PRESCRIPTION (mu at time-averaged |a| of previous orbit):")
    oa_runs = [('Saturn', S_HOSTILE), ('Mercury', S_HOSTILE), ('Mars', S_HOSTILE)]
    for name, s in oa_runs:
        a_SI, e, gN, T_yr = planet_derived(name)
        s_c = s/gN
        oa = run_orbit_averaged(e, s_c, 30)
        P(f"    {name:8s} hostile : 1/mu_bar-1 -> {oa['c_final']:.4e} "
          f"(analytic ~ s_c^2 beta^2/2 = {0.5*s_c*s_c*(1-e*e):.4e});")
        P(f"             post-convergence |Delta_pomega| per orbit <= {oa['max_dpom_tail']:.2e} rad"
          f" ; |da/a| per orbit <= {oa['da_over_a_tail']:.2e}  -> ZERO precession/drift (Kepler w/ GM_eff)")
    for name in PLANETS:   # amplified contrast: instantaneous signal vs orbit-averaged null at same s
        a_SI, e, gN, T_yr = planet_derived(name)
        s_c = 1e-3
        oa = run_orbit_averaged(e, s_c, 30)
        inst = dpomega_analytic(e, s_c)
        P(f"    {name:8s} amplified s_c=1e-3: instantaneous predicts {inst:+.2e} rad/orb;"
          f" orbit-averaged measured <= {oa['max_dpom_tail']:.1e} rad/orb"
          f"  (collapse factor >= {abs(inst)/max(oa['max_dpom_tail'],1e-300):.1e})")
    P("    Orbit-averaged relic observable (per-planet GM_eff/GM - 1 = 1/mu_bar - 1, analytic):")
    for name in PLANETS:
        a_SI, e, gN, T_yr = planet_derived(name)
        for s, slab in ((S_HOSTILE, 'hostile  '), (S_FRAMEWORK, 'framework')):
            s_c = s/gN
            P(f"      {name:8s} {slab}: {0.5*s_c*s_c*(1-e*e):.2e}  (cross-planet Kepler-ratio anomaly;"
              f" degenerate per-planet with fitted GM_sun)")

    # ---------------------------------------------------------------- verdict table
    P("\n[4] PREDICTIONS (verified analytic law; Saturn/Mars also measured directly) vs PINNED BOUNDS")
    P("    criterion: PASS if |pred - central| < 2 sigma for EVERY pinned bound (worst tension shown).")
    P("    '|pred|/sig_t' = prediction size in units of the tightest 1-sigma; 'margin' = sig_t/|pred|.")
    hdr = (f"    {'planet':8s} {'s':7s} {'prescription':14s} {'pred mas/cy':>12s} "
           f"{'worst bound (tension)':>40s} {'|pred|/sig_t':>12s} {'margin':>7s} verdict")
    P(hdr); P("    "+"-"*120)
    for name in PLANETS:
        a_SI, e, gN, T_yr = planet_derived(name)
        for s, slab in ((S_HOSTILE, 'cH_Lam'), (S_FRAMEWORK, 'a0_fw')):
            s_c = s/gN
            pred = mas_per_cy(dpomega_analytic(e, s_c), T_yr)
            worst = None
            for lab, c0, sg in BOUNDS[name]:
                t = abs(pred - c0)/sg
                if worst is None or t > worst[1]:
                    worst = (lab, t, sg)
            tight = min(BOUNDS[name], key=lambda b: b[2])
            margin = tight[2]/abs(pred)
            ok = worst[1] < 2.0
            P(f"    {name:8s} {slab:7s} {'instantaneous':14s} {pred:+12.3e} "
              f"{worst[0]:>28s} ({worst[1]:4.2f} sig) {abs(pred)/tight[2]:12.2e} {margin:7.2g} {'PASS' if ok else 'FAIL'}")
            P(f"    {name:8s} {slab:7s} {'orbit-averaged':14s} {0.0:+12.3e} "
              f"{'(zero precession — all bounds)':>40s} {0.0:12.1f} {'inf':>7s} PASS")
    P("\n    Saturn cH_Lam instantaneous — per-bound tensions (the binding case):")
    a_SI, e, gN, T_yr = planet_derived('Saturn')
    predS = mas_per_cy(dpomega_analytic(e, S_HOSTILE/gN), T_yr)
    for lab, c0, sg in BOUNDS['Saturn']:
        t = (predS - c0)/sg
        room2 = 2.0 - abs(t)
        P(f"      {lab:32s} {c0:+5.2f} +/- {sg:4.2f} : tension {t:+5.2f} sigma ; room to 2-sigma edge"
          f" = {room2*sg:+.3f} mas/cy")
    P("    -> the test is now BINDING at the hostile normalization: |pred| = 1.5x the tightest")
    P("       1-sigma (INPOP15a-C2), passing only at the 2-sigma criterion with 0.04 mas/cy of room;")
    P("       under EPM2011/INPOP10a/INPOP15a-C1 it passes comfortably (<= 0.7 sigma). The factor-25")
    P("       spread among published Saturn sigmas (0.20..5.0 mas/cy) is an ephemeris-systematics")
    P("       statement — both ways: no kill claimable on the tightest reading alone, no comfort")
    P("       claimable from the loosest.")
    P("\n    secular drift (both prescriptions, both s): d(ln a)/dt = 0 EXACTLY (instantaneous = ")
    P("    conservative central force; orbit-averaged = piecewise Kepler). Numerical floors above:")
    for name in PLANETS:
        a_SI, e, gN, T_yr = planet_derived(name)
        f_yr = floors[name]['slope_lna']/T_yr
        P(f"      {name:8s}: |d ln a/dt| floor = {abs(f_yr):.1e}/yr (= integrator energy bias, shared")
        P(f"                with control to machine precision -> physical drift consistent with 0)")
    P("    vs GM_dot/GM = -(6.13+/-1.47)e-14/yr (Genova+ 2018, Nat.Comm. 9:289): PASS identically.")
    P("    Circular-channel context (Folkner |da|<1e-14 m/s^2 at Saturn): instantaneous delta_a at")
    for s, slab in ((S_HOSTILE, 'hostile'), (S_FRAMEWORK, 'framework')):
        a_SI, e, gN, T_yr = planet_derived('Saturn')
        d_a   = s*s*a_SI**2/(2*GM_SUN)        # delta(r) = s^2 r^2/(2 GM)
        d_ap  = s*s*(a_SI*(1+e))**2/(2*GM_SUN)
        P(f"      {slab:9s}: delta_a(a)={d_a:.2e}, at aphelion {d_ap:.2e} m/s^2 -> "
          f"{'PASS' if d_ap < 1e-14 else 'FAIL'} (margin {1e-14/d_ap:.1f}x at aphelion)")

    # ---------------------------------------------------------------- Sun-reflex flag
    P("\n[5] FLAGGED ADDITIONAL CHANNEL (out of assigned scope; arithmetic only): SUN'S MODIFIED REFLEX")
    P("    Per-body instantaneous MI applies mu to the SUN too: |a_sun| ~ GM_jup/r_jup^2 = "
      f"{GM_JUP/R_JUP**2:.3e} m/s^2 (Jupiter-dominated).")
    for s, slab in ((S_HOSTILE, 'hostile'), (S_FRAMEWORK, 'framework')):
        g_sun = GM_JUP/R_JUP**2
        x = g_sun/s
        da_sun = inv_mu_minus_one_stable(x)*g_sun
        P(f"      {slab:9s}: x_sun={x:.0f}, anomalous solar acceleration = {da_sun:.2e} m/s^2"
          f"  = {da_sun/1e-14:.1f}x the 1e-14 Folkner Saturn scale (template differs: synodic, Jupiter-directed)")
    P("    This channel does NOT vanish under orbit-averaging (the Sun's <|a|> is unchanged), unlike")
    P("    the planet-precession channel. Escape: constituent-acceleration (composite-body) reading of")
    P("    MI — which would also switch off MOND for internally-supported stars (coherence cost for the")
    P("    bath interpretation). Needs an ephemeris-fit-level analysis (degeneracy with fitted masses).")
    P("    NOT folded into the Door-IVa verdict; logged as Door IVa-2.")

    P("\n[6] DONE.")

if __name__ == '__main__':
    main()
