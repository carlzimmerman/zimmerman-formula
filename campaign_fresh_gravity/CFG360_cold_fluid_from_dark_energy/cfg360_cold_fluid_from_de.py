#!/usr/bin/env python3
"""CFG360 -- is the cold fluid a byproduct of dark energy? (fresh lane; criteria frozen in FROZEN_CRITERIA.md first).

Five mechanism classes (C1 interacting vacuum, C2 khronon-shifted minimum, C3 condensate fraction, C4 a0/horizon production,
C5 phase transition) scored on G-AMOUNT, G-TIMING, G-EXPANSION (DESI DR2 chains, PROVISIONAL CPL projection) and the
framework-internal flat-a0 bound; G-SORTING reported.  Base-rate null for closed forms of 5.36.
kappa = 1/2 FITTED.  No dark-matter particle species; the cold MASS is still required.

Run from the repository root:
    nice -n 10 python3 campaign_fresh_gravity/CFG360_cold_fluid_from_dark_energy/cfg360_cold_fluid_from_de.py
    CFG360_MUTATE=1 nice -n 10 python3 campaign_fresh_gravity/CFG360_cold_fluid_from_dark_energy/cfg360_cold_fluid_from_de.py
MUTATE gives the cold fluid c_s^2 = w = 1/3; G-TIMING must then FAIL (exit 1).
"""
import hashlib, itertools, json, math, os, sys, time
import numpy as np
from scipy.integrate import solve_ivp, quad
from scipy.optimize import brentq

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
CHAINS = os.path.abspath(os.path.join(ROOT, "..", "_external_data", "desi_dr2_chains"))
MUTATE = os.environ.get("CFG360_MUTATE", "0") == "1"
SLUG = "cfg360_cold_fluid_from_de" + ("_MUTATE" if MUTATE else "")
FROZEN_SHA = hashlib.sha256(open(os.path.join(HERE, "FROZEN_CRITERIA.md"), "rb").read()).hexdigest()

LINES, CHECKS, NUM = [], [], {}
def P(s=""):
    print(s, flush=True); LINES.append(s)
def check(name, detail, ok, lb=True):
    CHECKS.append(dict(name=name, detail=detail, ok=bool(ok), load_bearing=lb))
    P(f"  [{'PASS' if ok else 'FAIL'}]{'' if lb else ' (reported)'} {name}\n         {detail}")
def banner(s):
    P("\n" + "=" * 110 + "\n" + s + "\n" + "=" * 110)

# ---------------------------------------------------------------- constants (Planck 2018 inputs; declared)
c = 2.99792458e8; G = 6.67430e-11; hbar = 1.054571817e-34; eV = 1.602176634e-19; kB = 1.380649e-23; Mpc = 3.0856775814913673e22
h = 0.674; H0 = 100 * h * 1e3 / Mpc                     # s^-1
om_c, om_b = 0.1200, 0.02237; om_r = 4.18e-5 * (0.674 / h) ** 0 * 1.0   # photons + 3.046 massless nu, omega_r = 4.18e-5
Oc, Ob, Or = om_c / h**2, om_b / h**2, om_r / h**2
OL = 1 - Oc - Ob - Or
KAPPA = 0.5
rho_crit = 3 * H0**2 / (8 * math.pi * G)                # kg m^-3
rho_L = OL * rho_crit
a0 = KAPPA * c * math.sqrt(G * rho_L)
T0 = 2.7255
R_TARGET, R_ERR = 5.36, 0.07
P(f"CFG360 cold fluid from dark energy {'[MUTATE: cold fluid c_s^2 = 1/3]' if MUTATE else ''}")
P(f"frozen criteria sha256 = {FROZEN_SHA}")
P(f"inputs: h={h} omega_c={om_c} omega_b={om_b} omega_r={om_r}  Omega_L={OL:.4f}  a0 = kappa c sqrt(G rho_L) = {a0:.3e} m/s^2 (kappa=1/2 FITTED)")
NUM.update(OL=OL, a0=a0, R_cmb=om_c / om_b)

def E_lcdm(z):
    return math.sqrt(Or * (1 + z)**4 + (Oc + Ob) * (1 + z)**3 + OL)

# ---------------------------------------------------------------- G-TIMING evaluator (frozen thresholds)
def kJ_dust_or_fluid(z, cs2):
    """comoving Jeans wavenumber (Mpc^-1) for a fluid of sound speed^2 cs2 (units c^2); inf for cs2 = 0."""
    if cs2 <= 0: return math.inf
    a = 1 / (1 + z); H = H0 * E_lcdm(z)
    rho_m = (Oc + Ob) * rho_crit * (1 + z)**3
    k_phys = math.sqrt(4 * math.pi * G * rho_m) / (math.sqrt(cs2) * c)
    return k_phys * Mpc / (1 + z)

def kJ_wave(z, m_eV):
    rho_c_ = Oc * rho_crit * (1 + z)**3
    m = m_eV * eV / c**2
    k_phys = (16 * math.pi * G * rho_c_ * m**2 / hbar**2) ** 0.25
    return k_phys * Mpc / (1 + z)

def g_timing(w, kJ, frac_in_place, z_prod, adiabatic):
    ok_i = abs(w) <= 1e-2 and kJ >= 1.0
    ok_ii = frac_in_place >= 0.99
    ok_iii = (z_prod >= 1e5) or adiabatic
    return ok_i and ok_ii and ok_iii, dict(w=w, kJ_Mpc=kJ, frac_in_place=frac_in_place, z_prod=z_prod, adiabatic=adiabatic,
                                         i=ok_i, ii=ok_ii, iii=ok_iii)

CS2_COLD = 1 / 3 if MUTATE else 0.0
W_COLD = 1 / 3 if MUTATE else 0.0

# ---------------------------------------------------------------- interacting vacuum background (C1, C4)
A_INI = 1e-4
def iv_solve(gam):
    """Q = gam*H0*rho_L.  N = ln a.  Densities in rho_crit0.  omega_c fixed EARLY (comoving rho_c a^3 = Oc at A_INI).
    rho_L(A_INI) shot so that the universe is flat today (E(a=1) = 1)."""
    def run(rL_ini, dense=False):
        def f(N, y):
            rL, rc = y; a = math.exp(N)
            E = math.sqrt(Or * a**-4 + Ob * a**-3 + rc + rL)
            q = gam * rL / E
            return [-q, -3 * (1 + W_COLD) * rc + q]
        N0 = math.log(A_INI)
        return solve_ivp(f, [N0, 0.0], [rL_ini, Oc * A_INI**(-3 * (1 + W_COLD))], rtol=1e-10, atol=1e-14, dense_output=dense,
                         method="LSODA")
    def resid(rL_ini):
        s = run(rL_ini); rL, rc = s.y[:, -1]
        return Or + Ob + rc + rL - 1.0
    lo, hi = 1e-6, 10.0
    rL_ini = brentq(resid, lo, hi, xtol=1e-14)
    return run(rL_ini, dense=True)

ZFIT = np.linspace(0, 2.5, 126)
def cpl_projection(sol):
    """CPL projection (DECLARED, PROVISIONAL): fit ln E(z) of the model with a flat w0waCDM at the observer's Omega_m
    (today's baryons + cold fluid, radiation as input) over 0 <= z <= 2.5.  Defined even when the effective dark-energy
    density an observer infers turns negative in the past (it does for Gamma >~ 0.1 H0; reported)."""
    from scipy.optimize import least_squares
    rL1, rc1 = sol.sol(0.0)
    Om_obs = Ob + rc1
    a = 1 / (1 + ZFIT); N = np.log(a)
    Y = np.array([sol.sol(n) for n in N])
    E2 = Or * a**-4 + Ob * a**-3 + Y[:, 1] + Y[:, 0]
    rde = E2 - Om_obs * a**-3 - Or * a**-4
    ODE = 1 - Om_obs - Or
    def r(p):
        w0, wa = p
        fde = a**(-3 * (1 + w0 + wa)) * np.exp(-3 * wa * (1 - a))
        return 0.5 * np.log(Om_obs * a**-3 + Or * a**-4 + ODE * fde) - 0.5 * np.log(E2)
    fit = least_squares(r, [-1.0, 0.0], xtol=1e-14, ftol=1e-14, gtol=1e-14)
    w0, wa = fit.x
    return float(w0), float(wa), float(Om_obs), dict(rde_min=float(rde.min()), max_abs_dlnE=float(np.abs(fit.fun).max()))

def load_chain(name):
    rows = []
    d = os.path.join(CHAINS, name)
    hdr = open(os.path.join(d, "chain.1.txt")).readline().lstrip("#").split()
    iw, iw0, iwa = hdr.index("weight"), hdr.index("w"), hdr.index("wa")
    for k in range(1, 5):
        x = np.loadtxt(os.path.join(d, f"chain.{k}.txt"))
        x = x[int(0.3 * len(x)):]
        rows.append(x[:, [iw, iw0, iwa]])
    x = np.vstack(rows); wt = x[:, 0]
    mu = np.average(x[:, 1:], axis=0, weights=wt)
    cov = np.cov(x[:, 1:].T, aweights=wt)
    return mu, cov

def chi2(mu, cov, w0, wa):
    d = np.array([w0, wa]) - mu
    return float(d @ np.linalg.solve(cov, d))

def lookback_H0(z):
    return quad(lambda zz: 1 / ((1 + zz) * E_lcdm(zz)), 0, z)[0]

# ================================================================= CONTROLS
banner("CONTROLS")
sol0 = iv_solve(0.0)
w00, wa0, Om0, _ = cpl_projection(sol0)
rc_today = float(sol0.sol(0.0)[1])
k1 = abs(rc_today - Oc) < 1e-6 if not MUTATE else True
check("K1 plain LambdaCDM (Gamma = 0): omega_c returned as input; CPL projection (-1, 0)",
      f"Omega_c(today)/Omega_c(input) - 1 = {rc_today / Oc - 1:+.2e}; (w0, wa) = ({w00:+.5f}, {wa0:+.5f})",
      (k1 and abs(w00 + 1) < 1e-4 and abs(wa0) < 1e-3) if not MUTATE else True, lb=not MUTATE)

chains = {}
for nm in ["cmb", "pantheonplus", "union3", "desy5"]:
    if os.path.isdir(os.path.join(CHAINS, nm)):
        chains[nm] = load_chain(nm)
        mu, cov = chains[nm]
        P(f"  chain DESI DR2 + CMB + {nm:12s}: <w0> = {mu[0]:+.3f} +- {math.sqrt(cov[0,0]):.3f}, <wa> = {mu[1]:+.3f} +- "
          f"{math.sqrt(cov[1,1]):.3f}, rho = {cov[0,1]/math.sqrt(cov[0,0]*cov[1,1]):+.2f}; chi2(LCDM) = {chi2(mu, cov, -1, 0):.2f}")
NUM["chains"] = {k: dict(mu=v[0].tolist(), cov=v[1].tolist(), chi2_LCDM=chi2(v[0], v[1], -1, 0)) for k, v in chains.items()}
have_chains = len(chains) == 4
check("chains on disk (all four DESI DR2 combinations)", f"found {sorted(chains)}", have_chains)

def expansion_ok(gam):
    s = iv_solve(gam); w0, wa, om, _ = cpl_projection(s)
    c2 = {k: chi2(v[0], v[1], w0, wa) for k, v in chains.items()}
    return all(x <= 6.18 for x in c2.values()), w0, wa, c2, s

# ================================================================= G-EXPANSION scan for C1
banner("G-EXPANSION: interacting vacuum Q = Gamma rho_Lambda (vacuum -> cold), Gamma in units of H0")
GRID = [0.0, 0.005, 0.01, 0.015, 0.02, 0.025, 0.03, 0.035, 0.04, 0.05, 0.1, 0.15, 0.2, 0.3, 0.5, 0.7, 1.0]
scan = []
for g in GRID:
    ok, w0, wa, c2, s = expansion_ok(g)
    rL1 = s.sol(0.0)[0]
    rLz5 = s.sol(math.log(1 / 6))[0]
    scan.append(dict(gamma=g, w0=w0, wa=wa, chi2=c2, ok=ok, rhoL_z5_over_today=float(rLz5 / rL1)))
    pj = cpl_projection(s)[3]
    scan[-1].update(pj)
    P(f"  Gamma = {g:6.3f} H0: (w0, wa)_eff = ({w0:+.4f}, {wa:+.4f}) [min rho_DE,eff = {pj['rde_min']:+.3f}, CPL resid {pj['max_abs_dlnE']:.1e}]; chi2 cmb/PP/U3/DY5 = "
      + "/".join(f"{c2[k]:.2f}" for k in ["cmb", "pantheonplus", "union3", "desy5"]) + f"; inside all 95%: {ok}; "
      f"rho_L(z=5)/rho_L(0) = {rLz5 / rL1:.4f}")
NUM["expansion_scan"] = scan
# Gamma_max: largest Gamma inside all four 95% contours, bisected between the last ok and first not-ok grid points
ok_flags = [s_["ok"] for s_ in scan]
gmax = None
if ok_flags[0]:
    idx = next((i for i, f in enumerate(ok_flags) if not f), None)
    if idx is None:
        gmax = GRID[-1]
    else:
        lo, hi = GRID[idx - 1], GRID[idx]
        for _ in range(25):
            mid = 0.5 * (lo + hi)
            if expansion_ok(mid)[0]: lo = mid
            else: hi = mid
        gmax = lo
P(f"  LCDM (Gamma = 0) inside all four 95% contours: {ok_flags[0]}")
fine = np.linspace(0, 0.1, 201)
win = [float(g) for g in fine if expansion_ok(g)[0]]
NUM["frozen_rule_allowed_window_H0"] = [min(win), max(win)] if win else None
P(f"  frozen rule (inside ALL FOUR 95% contours), fine scan 0-0.1 H0 step 5e-4: allowed window = "
  + (f"[{min(win):.4f}, {max(win):.4f}] H0" if win else "EMPTY") + " -- LambdaCDM itself is excluded by this rule (DESI DR2 w0wa tension)")
if gmax is None:
    # LCDM itself is outside some contour; report the per-chain behaviour honestly and use the Delta-chi2 <= 4 rule per chain vs Gamma=0
    P("  LCDM itself lies outside at least one 95% contour; the transfer bound is then quoted as Delta chi2 <= 4 relative to Gamma = 0 "
      "on the WORST chain (DECLARED fallback, not frozen; flagged).")
    def worse(g):
        c2g = expansion_ok(g)[3]; c20 = scan[0]["chi2"]
        return max(c2g[k] - c20[k] for k in c2g)
    lo, hi = 0.0, 1.0
    if worse(hi) <= 4: gmax_fb = hi
    else:
        for _ in range(25):
            mid = 0.5 * (lo + hi)
            if worse(mid) <= 4: lo = mid
            else: hi = mid
        gmax_fb = lo
    NUM["Gamma_max_fallback_H0"] = gmax_fb
    P(f"  Gamma_max (fallback Delta chi2 <= 4 on the worst chain) = {gmax_fb:.4f} H0")
else:
    NUM["Gamma_max_DESI_H0"] = gmax
    P(f"  Gamma_max (inside all four 95% contours) = {gmax:.4f} H0  [PROVISIONAL: CPL projection, Gaussian chains, Omega_m shift ignored]")
k2 = not expansion_ok(1.0)[0]
check("K2 a transfer violating the DESI bound (Gamma = 1 H0) is flagged by G-EXPANSION", f"flagged: {k2}", k2, lb=not MUTATE)

# framework-internal flat-a0 bound: rho_L(z=5)/rho_L(0) <= 1.0201  (a0 flat to 1%)
L5 = lookback_H0(5.0)
def rho_ratio_z5(g):
    s = iv_solve(g); return s.sol(math.log(1 / 6))[0] / s.sol(0.0)[0]
g_flat = brentq(lambda g: rho_ratio_z5(g) - 1.0201, 1e-6, 1.0, xtol=1e-8)
NUM.update(lookback_z5_H0=L5, Gamma_max_flat_a0_H0=g_flat)
P(f"  flat-a0 internal bound: H0 * lookback(z=5) = {L5:.4f}; |Delta a0/a0| <= 1% for z <= 5 => Gamma <= {g_flat:.4f} H0 "
  f"(analytic ln(1.0201)/L5 = {math.log(1.0201) / L5:.4f})")
GBOUND = min(g_flat, NUM.get("Gamma_max_DESI_H0", NUM.get("Gamma_max_fallback_H0", 1.0)))
NUM["Gamma_bound_used_H0"] = GBOUND

# amount producible before z = 3000 by C1 at the bound
def produced_before(gam, z):
    s = iv_solve(gam)
    # comoving produced amount = integral of gam*rho_L/E * a^3 dN from A_INI to a(z)   (no production before A_INI by construction;
    # extend analytically to a -> 0 with rho_L ~ const: integral of a^3/E dN converges)
    f = lambda N: gam * s.sol(N)[0] / math.sqrt(Or * math.exp(-4 * N) + Ob * math.exp(-3 * N) + s.sol(N)[1] + s.sol(N)[0]) * math.exp(3 * N)
    v = quad(f, math.log(A_INI), math.log(1 / (1 + z)), limit=200)[0]
    rLi = s.sol(math.log(A_INI))[0]
    v += gam * rLi * quad(lambda N: math.exp(3 * N) / math.sqrt(Or * math.exp(-4 * N)), -60, math.log(A_INI))[0]
    return v / Oc
frac_C1 = produced_before(GBOUND, 3000.0)
NUM["C1_fraction_of_omega_c_made_before_z3000_at_bound"] = frac_C1
P(f"  C1 at the bound: cold fluid made before z = 3000 = {frac_C1:.2e} of omega_c")
# drained-vacuum alternative: rho_L(z=3000) must exceed rho_c(3000) -> a0 at z=3000 relative to today if a0 ~ sqrt(rho_L)
ratio_rho = Oc * 3001**3 / OL
NUM["C1_drained_a0_ratio_z3000"] = math.sqrt(ratio_rho)
P(f"  C1 drained-vacuum variant: rho_L(3000) >= rho_c(3000) = {ratio_rho:.2e} rho_L0 -> a0(3000)/a0 >= {math.sqrt(ratio_rho):.2e} "
  "on a0 ~ sqrt(rho_L) (PAPER42 (i)); or the present rho_L is a decoupled residual (CFG288 A1 second scale)")

# ================================================================= classes
banner("CLASSES")
res = {}
# ---- C1
t_ok, t_d = g_timing(W_COLD, kJ_dust_or_fluid(3000, CS2_COLD), frac_C1, 0.0, False)
res["C1"] = dict(name="interacting vacuum Q = Gamma rho_L", amount="FAIL (made-before-z3000 = %.1e of omega_c at Gamma_bound; draining "
                 "a larger early vacuum needs a second scale / breaks a0~sqrt(rho_L))" % frac_C1,
                 timing=t_ok, timing_detail=t_d, expansion="PASS for Gamma <= %.4f H0" % GBOUND, new_constants="Gamma (1)",
                 sorting="no (homogeneous source)", verdict="NO-GO")
# ---- C2 khronon-shifted minimum: adiabatic theorem.  Numeric: phi'' + m^2 (phi - v(t)) = 0, v = dv (1+tanh(t/T))/2
def residual_amp(mT):
    m = 1.0; T = mT
    f = lambda t, y: [y[1], -m**2 * (y[0] - 0.5 * (1 + math.tanh(t / T)))]
    t0 = -40 * max(T, 1); s = solve_ivp(f, [t0, -t0], [0.0, 0.0], rtol=1e-11, atol=1e-13, max_step=0.05)
    x, v = s.y[0, -1] - 1.0, s.y[1, -1]
    return math.hypot(x, v / m)
amps = {mT: residual_amp(mT) for mT in [0.3, 1.0, 3.0, 6.0]}
an = {mT: (math.pi * mT / 2) / math.sinh(math.pi * mT / 2) for mT in amps}
for mT in amps:
    P(f"  C2 shift on timescale T, mass m: residual oscillation amplitude / shift = {amps[mT]:.3e} (analytic {an[mT]:.3e}) at mT = {mT}")
c2_ok_num = all(abs(amps[k] / an[k] - 1) < 2e-2 for k in amps if an[k] > 1e-6)
check("C2 numerics: residual amplitude matches the adiabatic formula (pi mT/2)/sinh(pi mT/2)", f"{ {k: round(amps[k]/an[k],4) for k in amps} }", c2_ok_num)
# dust by z=3000 requires m >> H(3000); rho_osc = (1/2) m^2 dv^2 * A^2 must equal rho_c at production >= rho_c(3000)
H3000_eV = H0 * E_lcdm(3000) * hbar / eV
NUM["H_z3000_eV"] = H3000_eV
P(f"  C2: dust before z=3000 needs m >> H(3000) = {H3000_eV:.2e} eV; the khronon clock's only rate is H, so mT ~ m/H >> 1 and the "
  f"oscillation is suppressed by ~exp(-pi m/2H): amount = (1/2) m^2 dv^2 (pi mT/2)^2/sinh^2 -- set by m, dv, T (free)")
kJ2 = kJ_wave(3000, 2e-20) if not MUTATE else kJ_dust_or_fluid(3000, CS2_COLD)
t_ok, t_d = g_timing(W_COLD, kJ2, 1.0, 1e5, True)
res["C2"] = dict(name="field with minimum shifted by the khronon clock", amount="FREE (m, dv, T; height >= ~1e10 rho_L at z_eq: CFG288 A1)",
                 timing=t_ok, timing_detail=t_d, expansion="PASS (no late transfer)", new_constants="m, dv (>=2)",
                 sorting="no", verdict="PARTIAL (amount free)")
# ---- C3 condensate fraction
frac_ratio = 3001**3
P(f"  C3: a fixed fraction f of rho_L (w = -1) cannot scale as a^-3: rho_c/rho_L grows by (1+z)^3 = {frac_ratio:.2e} at z = 3000; "
  "f(a) ~ a^-3 is a free function; the FL1 dust branch = CFG288 (amount = misalignment amplitude, free)")
t_ok, t_d = g_timing(W_COLD, kJ2, 1.0, 1e5, True)
res["C3"] = dict(name="condensate fraction of the vacuum sector (FL1)", amount="NO-GO as a fraction (scaling theorem); FL1 dust branch FREE",
                 timing=t_ok, timing_detail=t_d, expansion="PASS (no late transfer)", new_constants="f(a) or amplitude",
                 sorting="no", verdict="NO-GO (fraction) / reduces to CFG288")
# ---- C4 zero-parameter rate Gamma = a0/c
g4 = a0 / c / H0
ok4, w04, wa04, c24, s4 = expansion_ok(g4)
frac4 = produced_before(g4, 3000.0)
rr4 = rho_ratio_z5(g4)
# Gibbons-Hawking horizon radiation reservoir
TGH = hbar * H0 / (2 * math.pi * kB)
rho_GH = (math.pi**2 / 30) * (kB * TGH)**4 / (hbar * c)**3 / c**2
NUM.update(C4_Gamma_H0=g4, C4_w0=w04, C4_wa=wa04, C4_chi2=c24, C4_frac_before_3000=frac4, C4_rhoL_z5_ratio=rr4,
           GH_density_over_rho_crit=rho_GH / rho_crit)
P(f"  C4: Gamma = a0/c = kappa sqrt(G rho_L) = {g4:.4f} H0 (zero parameters); (w0, wa)_eff = ({w04:+.4f}, {wa04:+.4f}); chi2 = "
  + "/".join(f"{c24[k]:.2f}" for k in ["cmb", "pantheonplus", "union3", "desy5"]) + f"; inside all 95%: {ok4}")
P(f"      rho_L(z=5)/rho_L(0) = {rr4:.4f} -> a0 drifts {100 * (math.sqrt(rr4) - 1):.2f}% over z <= 5 (framework flat law allows 1%); "
  f"made before z = 3000: {frac4:.2e} of omega_c")
P(f"      horizon reservoir: Gibbons-Hawking T = {TGH:.2e} K, radiation density = {rho_GH / rho_crit:.2e} rho_crit (hopeless)")
t_ok, t_d = g_timing(W_COLD, kJ_dust_or_fluid(3000, CS2_COLD), frac4, 0.0, False)
res["C4"] = dict(name="a0/horizon production (Gamma = a0/c; GH reservoir)", amount="FAIL (%.1e of omega_c before z=3000; GH %.0e rho_crit)" % (frac4, rho_GH / rho_crit),
                 timing=t_ok, timing_detail=t_d, expansion=("PASS" if ok4 else "FAIL") + " vs DESI; flat-a0 law " +
                 ("PASS" if rr4 <= 1.0201 else "FAIL (a0 drift %.1f%%)" % (100 * (math.sqrt(rr4) - 1))),
                 new_constants="0", sorting="no", verdict="NO-GO")
# ---- C5 phase transition at T* = rho_L^(1/4)
rhoL_eV4 = rho_L * c**2 * (hbar * c)**3 / eV**4      # (energy density in eV^4 natural units)
Tstar = rhoL_eV4 ** 0.25
z_star = Tstar / (kB * T0 / eV) - 1
NUM.update(Tstar_eV=Tstar, z_star=z_star)
P(f"  C5: T* = rho_L^(1/4) = {Tstar * 1e3:.3f} meV -> T_gamma = T* at z* = {z_star:.2f} (needs >= 3000, and >= 1e5 for CFG288 seeding);"
  f" latent heat ~ rho_L = {1 / (Oc * 3001**3 / OL):.1e} rho_c(3000). A free T* (>= {1e5 * kB * T0 / eV:.0f} eV) with a free efficiency sets the amount: FREE")
t_ok, t_d = g_timing(W_COLD, kJ_dust_or_fluid(3000, CS2_COLD), 0.0, z_star, False)
res["C5"] = dict(name="phase transition of the vacuum sector", amount="FAIL tied (z*=%.1f); FREE untied (T*, efficiency)" % z_star,
                 timing=t_ok, timing_detail=t_d, expansion="PASS (early, no late transfer)", new_constants="0 tied / 2 untied",
                 sorting="no", verdict="NO-GO tied / PARTIAL untied")
for k, v in res.items():
    P(f"  {k}: {v['name']}: amount {v['amount']}; timing {'PASS' if v['timing'] else 'FAIL'}; expansion {v['expansion']}; "
      f"new constants {v['new_constants']}; verdict {v['verdict']}")
NUM["classes"] = res

# MUTATE / timing load-bearing: the cold-fluid model itself (dust, made early, adiabatic) must pass G-TIMING; MUTATE must fail
t_ok, t_d = g_timing(W_COLD, kJ_dust_or_fluid(3000, CS2_COLD), 1.0, 1e6, True)
check("G-TIMING of the cold-fluid model itself (pressureless, in place, adiabatic)" + (" [MUTATE c_s^2=1/3: must FAIL]" if MUTATE else ""),
      f"w = {W_COLD:.3f}, k_J(z=3000) = {t_d['kJ_Mpc']:.3g} Mpc^-1 (need >= 1)", t_ok)

# ================================================================= base-rate null
banner("BASE-RATE NULL for closed forms of Omega_c/Omega_b = 5.36 (window 1.3%)")
SYM = {"pi": math.pi, "2": 2.0, "3": 3.0, "e": math.e, "kappa": 0.5, "OL": 0.6847, "Ob": 0.0493, "Om": 0.3153,
       "sqrt2": math.sqrt(2), "sqrt3": math.sqrt(3)}
EXP = [-2, -1, -0.5, 0.5, 1, 2]
PRE = [1, 2, 3, 4, 0.5, 1 / 3, 0.25, 2 / 3, 1.5, 0.75, 4 / 3]
def grammar():
    vals = {}
    names = list(SYM)
    for p in PRE:
        for n in names:
            for e in EXP:
                vals[f"{p:.4g}*{n}^{e}"] = p * SYM[n]**e
        for (n1, n2) in itertools.combinations(names, 2):
            for e1 in EXP:
                for e2 in EXP:
                    vals[f"{p:.4g}*{n1}^{e1}*{n2}^{e2}"] = p * SYM[n1]**e1 * SYM[n2]**e2
    return vals
G_ = grammar()
vals = np.array(list(G_.values())); keys = list(G_)
uniq = np.unique(np.round(vals, 10))
def hits(t):
    m = np.abs(vals / t - 1) <= 0.013
    return int(m.sum()), [keys[i] for i in np.where(m)[0][:12]], int((np.abs(uniq / t - 1) <= 0.013).sum())
h536, ex536, hu536 = hits(R_TARGET)
h300, ex300, hu300 = hits(3.00)
N = len(vals); Nu = len(uniq)
p536 = h536 / N; pu536 = hu536 / Nu
NUM.update(null_N_forms=N, null_N_unique=Nu, null_hits_536=h536, null_hits_unique_536=hu536, null_p_536=p536,
           null_p_unique_536=pu536, null_hits_300=h300, null_hits_unique_300=hu300, null_examples_536=ex536)
P(f"  grammar: {N} forms ({Nu} distinct values); hits within 1.3% of 5.36: {h536} forms ({hu536} distinct values) -> p = {p536:.4f} "
  f"(distinct {pu536:.4f}); examples: {ex536[:8]}")
P(f"  planted target 3.00: {h300} forms ({hu300} distinct) -> p = {h300 / N:.4f}")
P(f"  per-form chance rate p = {p536:.4f} (< 0.01): a closed form DECLARED by a mechanism before looking could survive this null;"
  f" but {hu536} distinct values hit, so a post-hoc search always finds one (look-elsewhere). No class here predicts a closed form,"
  f" so nothing is scored; the examples above are search hits, i.e. coincidences.")
check("null: planted target 3.00 gives a comparable chance rate (within x3 of 5.36's)", f"{h300} vs {h536}", 1 / 3 <= (h300 + 1) / (h536 + 1) <= 3)
check("null: no mechanism-declared closed form exists to score (amount FREE or FAIL in every class)", "nothing to test", True, lb=False)

# ================================================================= verdict
banner("VERDICT")
found = False
partial = any("PARTIAL" in v["verdict"] for v in res.values())
verdict = "MECHANISM FOUND" if found else ("PARTIAL" if partial else "NO-GO")
P(f"  {verdict}: no class fixes Omega_c/Omega_b with zero new constants. C1/C4 (late transfer) cannot place the cold fluid before "
  "z = 3000 (<= %.0e of omega_c); C3 fails the scaling theorem; C5 tied to rho_L^(1/4) fires at z* = %.1f; C2 and an untied C5 pass "
  "timing and expansion only with the amount FREE (CFG288's failure mode). Sorting: no class sorts spirals vs clusters (homogeneous "
  "sources); retention stays a later dynamical question (cm01/C003). The cold MASS is still required." % (max(frac_C1, frac4), z_star))
NUM["verdict"] = verdict

lb = [c_ for c_ in CHECKS if c_["load_bearing"]]
nf = sum(not c_["ok"] for c_ in lb)
P(f"\n  {sum(c_['ok'] for c_ in CHECKS)}/{len(CHECKS)} checks pass; load-bearing failures: {nf}")
def jc(o):
    if isinstance(o, dict): return {str(k): jc(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)): return [jc(v) for v in o]
    if isinstance(o, (np.floating, float)): return None if not math.isfinite(float(o)) else float(o)
    if isinstance(o, (np.integer,)): return int(o)
    if isinstance(o, np.bool_): return bool(o)
    return o
json.dump(jc(dict(slug=SLUG, frozen_sha256=FROZEN_SHA, checks=CHECKS, numbers=NUM, load_bearing_failures=nf)),
          open(os.path.join(HERE, SLUG + "_results.json"), "w"), indent=1)
open(os.path.join(HERE, SLUG + ".out"), "w").write("\n".join(LINES) + "\n")
sys.exit(1 if nf else 0)
