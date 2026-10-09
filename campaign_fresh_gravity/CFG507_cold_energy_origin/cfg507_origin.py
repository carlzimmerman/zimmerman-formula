#!/usr/bin/env python3
"""CFG507 -- where does the cold energy come from?  Three origin mechanisms the record has not run.
Frozen: FROZEN_CRITERIA.md (cec378664), committed alone before this script.

M1  early running (H^2-tracking) vacuum feeding cold energy:  rho_vac = rho_L + nu 3H^2/(8 pi G)
M2  the MOND field's dust charge sourced by baryons (conformal coupling A = exp(beta phi / Mbar_Pl))
M3  dark-energy seesaw relic m* = sqrt(rho_L^(1/4) M), thermal freeze-out  (FORCES A PARTICLE)

CFG507_MUTATE=1: M1 wrong sign (nu < 0), M2 beta = 0, M3 scrambled cosmology (200 draws).  Separate _MUTATE outputs.
Offline: on-disk DESI DR2 chains only.  kappa = 1/2 fitted.  The cold energy's mass is still required.  Never "theory closed".
"""
import os, json, math
import numpy as np
from scipy.integrate import solve_ivp, quad
from scipy.optimize import brentq, least_squares
from scipy.special import kve

HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(os.path.dirname(HERE))
CHAINS = os.path.abspath(os.path.join(ROOT, "..", "_external_data", "desi_dr2_chains"))
MUTATE = os.environ.get("CFG507_MUTATE", "0") == "1"
SLUG = "cfg507_origin" + ("_MUTATE" if MUTATE else "")
LOG, CH = [], []
OUT = {"lane": "CFG507", "frozen": "cec378664", "mutate": MUTATE}


def P(s=""):
    print(s, flush=True); LOG.append(s)


def check(n, ok, v=""):
    CH.append(bool(ok)); P(f"  [{'PASS' if ok else 'FAIL'}] {n} {v}")


# ---------------------------------------------------------------- cosmology (Planck-like, as CFG360/368)
h = 0.674; om_c, om_b, om_r = 0.1200, 0.02237, 4.18e-5
Oc, Ob, Or = om_c / h**2, om_b / h**2, om_r / h**2
OL = 1 - Oc - Ob - Or
ZFIT = np.linspace(0, 2.5, 126)
HUBBLE_GYR = 977.792 / (100 * h)          # 1/H0 in Gyr
SN = ("pantheonplus", "union3", "desy5")


def load_chain(name):
    d = os.path.join(CHAINS, name); hdr = open(os.path.join(d, "chain.1.txt")).readline().lstrip("#").split()
    iw, iw0, iwa = hdr.index("weight"), hdr.index("w"), hdr.index("wa"); rows = []
    for k in range(1, 5):
        x = np.loadtxt(os.path.join(d, f"chain.{k}.txt")); x = x[int(0.3 * len(x)):]; rows.append(x[:, [iw, iw0, iwa]])
    x = np.vstack(rows); wt = x[:, 0]
    return np.average(x[:, 1:], axis=0, weights=wt), np.cov(x[:, 1:].T, aweights=wt)


def chi2(mu, cov, w0, wa):
    d = np.array([w0, wa]) - mu
    return float(d @ np.linalg.solve(cov, d))


def cpl_project(E2fun, Om_obs):
    """CFG360/368 DECLARED, PROVISIONAL projection: least-squares CPL fit of ln E over 0 <= z <= 2.5 at the observer's Omega_m."""
    a = 1 / (1 + ZFIT); E2 = E2fun(a); ODE = 1 - Om_obs - Or
    def r(q):
        w0, wa = q; fde = a**(-3 * (1 + w0 + wa)) * np.exp(-3 * wa * (1 - a))
        return 0.5 * np.log(np.maximum(Om_obs * a**-3 + Or * a**-4 + ODE * fde, 1e-30)) - 0.5 * np.log(E2)
    f = least_squares(r, [-1.0, 0.0], xtol=1e-14, ftol=1e-14, gtol=1e-14)
    return float(f.x[0]), float(f.x[1]), float(np.abs(f.fun).max())


def t_of_a(a):
    """LCDM cosmic time (Gyr) from a = 0."""
    f = lambda x: 1.0 / (x * math.sqrt(Or * x**-4 + (Ob + Oc) * x**-3 + OL))
    return HUBBLE_GYR * quad(f, 0, a, limit=400, epsabs=0, epsrel=1e-10)[0]


chains = {nm: load_chain(nm) for nm in ("cmb", "pantheonplus", "union3", "desy5")}
P(f"CFG507 {'MUTATE ' if MUTATE else ''}run; frozen cec378664; h={h}, omega_c={om_c}, omega_b={om_b}, Omega_L={OL:.4f}")
for nm, (mu, cov) in chains.items():
    P(f"  chain {nm:12s}: <w0> {mu[0]:+.3f} +- {math.sqrt(cov[0,0]):.3f}, <wa> {mu[1]:+.3f} +- {math.sqrt(cov[1,1]):.3f}")
X0 = {k: chi2(*chains[k], -1.0, 0.0) for k in chains}
P("  LCDM chi2 cmb/PP/U3/DY5 = " + "/".join(f"{X0[k]:.2f}" for k in chains))
if not MUTATE:
    check("K5 Pantheon+ chain mean w0 within 0.01 of -0.838", abs(chains["pantheonplus"][0][0] + 0.838) < 0.01, f"({chains['pantheonplus'][0][0]:+.4f})")

# ================================================================ M1: early running vacuum -> cold energy
P("\n=== M1: running (H^2-tracking) vacuum feeding cold energy;  rho_vac = rho_L + nu 3H^2/8piG ===")
P("  exact: d rho_c/dN = -3(1-nu) rho_c + nu(4 Or a^-4 + 3 Ob a^-3);  comoving y = rho_c a^3:")
P("  y(N) = 4 nu Or/(1+3nu) [e^{3nu N - (1+3nu) N_i} - e^{-N}] + Ob [e^{3nu(N - N_i)} - 1]  (no cold energy before N_i)")


def y_closed(N, Ni, nu):
    if N <= Ni:
        return 0.0
    return 4 * nu * Or / (1 + 3 * nu) * (math.exp(3 * nu * N - (1 + 3 * nu) * Ni) - math.exp(-N)) + Ob * (math.exp(3 * nu * (N - Ni)) - 1)


def y_ode(N, Ni, nu):
    f = lambda n, y: [3 * nu * y[0] + nu * (4 * Or * math.exp(-n) + 3 * Ob)]
    s = solve_ivp(f, [Ni, N], [0.0], rtol=1e-12, atol=1e-30, method="DOP853")
    return float(s.y[0, -1])


N_REC = math.log(1e-3)


def switch_on(nu):
    """N_i such that omega_c(a = 1e-3) = 0.120 (CMB), or None."""
    g = lambda Ni: y_closed(N_REC, Ni, nu) - Oc
    lo, hi = -80.0, N_REC - 1e-9
    try:
        if g(lo) * g(hi) > 0:
            return None
        return brentq(g, lo, hi, xtol=1e-13)
    except (ValueError, OverflowError):
        return None


def m1_eval(nu):
    Ni = switch_on(nu)
    row = dict(nu=nu, amount_reachable=Ni is not None)
    if Ni is None:
        return row
    yz = lambda z: y_closed(-math.log(1 + z), Ni, nu)
    y0 = yz(0.0)
    rhoL = (1 - nu) - Or - Ob - y0
    def E2(a):
        a = np.asarray(a, float); y = np.array([y_closed(math.log(x), Ni, nu) for x in np.atleast_1d(a)])
        return (Or * a**-4 + Ob * a**-3 + y * a**-3 + rhoL) / (1 - nu)
    w0, wa, res = cpl_project(E2, Ob + y0)
    x2 = {k: chi2(*chains[k], w0, wa) for k in chains}
    dchi = {k: X0[k] - x2[k] for k in chains}          # positive = better than LCDM
    rv = lambda z: rhoL + nu * float(E2(1 / (1 + z))[0])
    a0r = {z: (math.sqrt(rv(z) / rv(0)) if rv(z) > 0 and rv(0) > 0 else float('nan')) for z in (1.0, 2.0, 2.5, 10.0)}
    f_in_1e5 = yz(1e5) / y0
    drift_3000_1100 = yz(1100) / yz(3000) - 1
    drift_1100_0 = y0 / yz(1100) - 1
    dneff = nu / (1 - nu) / (1.75 / 10.75)
    T_i_eV = 2.348e-4 / math.exp(Ni) * (3.91 / 10.75) ** (1 / 3)        # T0 = 2.348e-4 eV; g*s(T_i) ~ 10.75 (keV-MeV era)
    row.update(N_i=Ni, a_i=math.exp(Ni), z_i=math.exp(-Ni) - 1, T_i_eV=T_i_eV, omega_c_today=y0 * h**2, w0=w0, wa=wa, cpl_resid=res,
               dchi2=dchi, a0_ratio=a0r, frac_in_place_z1e5=f_in_1e5, drift_3000_1100=drift_3000_1100, drift_1100_0=drift_1100_0,
               dNeff=dneff)
    row["C_PRESENT"] = (f_in_1e5 >= 0.99) and (abs(drift_3000_1100) <= 0.01)
    row["C_NEFF"] = dneff <= 0.3
    row["C_LATE_not_excluded"] = all(dchi[k] >= -4 for k in SN)
    row["reproduces_DESI"] = all(dchi[k] >= 4 for k in SN)
    return row


# K1 / K2 controls (main only)
if not MUTATE:
    yk = [y_closed(math.log(a), math.log(1e-8), 0.0) for a in (1e-6, 1e-3, 1.0)]
    E2k = lambda a: (Or * np.asarray(a)**-4 + Ob * np.asarray(a)**-3 + (1 - Or - Ob)) / 1.0
    w0k, wak, _ = cpl_project(E2k, Ob)
    check("K1 M1 nu = 0: no cold energy and (w0, wa) = (-1, 0) to 1e-5", max(abs(v) for v in yk) == 0 and abs(w0k + 1) < 1e-5 and abs(wak) < 1e-5,
          f"(max y = {max(abs(v) for v in yk):.1e}; w0+1 = {w0k+1:+.1e}, wa = {wak:+.1e})")
    # pure radiation closed form x = rho_c/rho_r = 4nu/(1+3nu) (e^{(1+3nu)(N-Ni)} - 1); compare with the ODE (baryons off)
    nu_k, Ni_k, N_k = 1e-3, math.log(1e-9), math.log(1e-6)
    f = lambda n, y: [-3 * (1 - nu_k) * y[0] + nu_k * 4 * Or * math.exp(-4 * n)]
    s = solve_ivp(f, [Ni_k, N_k], [0.0], rtol=1e-12, atol=1e-40, method="DOP853")
    x_num = s.y[0, -1] / (Or * math.exp(-4 * N_k)); x_an = 4 * nu_k / (1 + 3 * nu_k) * (math.exp((1 + 3 * nu_k) * (N_k - Ni_k)) - 1)
    yo = y_ode(math.log(1e-3), math.log(1e-8), 1e-3); yc = y_closed(math.log(1e-3), math.log(1e-8), 1e-3)
    check("K2 M1 pure-radiation closed form vs ODE to 1e-6 (and full closed form vs ODE)", abs(x_num / x_an - 1) < 1e-6 and abs(yo / yc - 1) < 1e-6,
          f"(rad {x_num/x_an-1:+.1e}; full {yo/yc-1:+.1e})")

if not MUTATE:
    NU = [1e-8, 1e-7, 1e-6, 1e-5, 3e-5, 7e-5, 1e-4, 3e-4, 1e-3, 3e-3, 1e-2, 3e-2, 0.1]
else:
    NU = [-x for x in (1e-8, 1e-6, 1e-4, 1e-3, 1e-2, 3e-2, 0.1)]
rows = [m1_eval(nu) for nu in NU]
P(f"  {'nu':>9s} {'amount':>6s} {'z_i':>9s} {'T_i[eV]':>9s} {'in@1e5':>7s} {'drift3000-1100':>14s} {'drift1100-0':>11s} {'dNeff':>7s} "
  f"{'w0':>7s} {'wa':>7s} {'dchi2 PP/U3/DY5':>20s} {'a0(2)/a0':>9s} {'a0(10)/a0':>9s}  pass")
for r in rows:
    if not r["amount_reachable"]:
        P(f"  {r['nu']:+9.1e} {'NO':>6s}  -- amount unreachable (no switch-on gives omega_c = 0.120 at z = 1000)"); continue
    ok = r["C_PRESENT"] and r["C_NEFF"] and r["C_LATE_not_excluded"]
    P(f"  {r['nu']:+9.1e} {'yes':>6s} {r['z_i']:9.2e} {r['T_i_eV']:9.2e} {r['frac_in_place_z1e5']:7.4f} {r['drift_3000_1100']:+14.2e} {r['drift_1100_0']:+11.2e} "
      f"{r['dNeff']:7.4f} {r['w0']:+7.3f} {r['wa']:+7.3f} {r['dchi2']['pantheonplus']:+6.2f}/{r['dchi2']['union3']:+6.2f}/{r['dchi2']['desy5']:+6.2f} "
      f"{r['a0_ratio'][2.0]:9.5f} {r['a0_ratio'][10.0]:9.4f}  {'ALL' if ok else 'no'}")

passing = [r for r in rows if r["amount_reachable"] and r["C_PRESENT"] and r["C_NEFF"] and r["C_LATE_not_excluded"]]
desi_ok = [r for r in passing if r["reproduces_DESI"]]
desi_any = [r for r in rows if r["amount_reachable"] and r["reproduces_DESI"]]
nu_max_present = max([r["nu"] for r in passing], default=None)

# Separate-universe isocurvature (main only): growing-mode patches (same rho(t), local a scaled by e^zeta).
iso = {}
if not MUTATE:
    P("\n  M1 isocurvature, separate universes in the radiation era (production on, baryons off):")
    nu_s, Ni_s, zeta = 1e-5, math.log(1e-9), 1e-4
    def patch(scale, switch):
        # local a(t) = scale * a_bar(t); radiation density rho_r(t) identical in proper time (growing mode)
        # switch 'T': on when local T (i.e. local rho_r) reaches T_i;  'tau': on at proper time t_i;  'clock': on when a spectator clock with
        # its own fluctuation dtau reads t_i (dtau = +1e-4 t_i here, uncorrelated with zeta)
        # in pure radiation rho_r(t) ~ t^-2, so N_i in the background time: local switch-on in terms of background ln a_bar
        if switch in ("T", "tau"):
            Ni_bar = Ni_s
        else:
            Ni_bar = Ni_s + 0.5 * math.log(1 + 1e-4)
        Nb = math.log(1e-6)                                           # read-out at background ln a_bar
        x = 4 * nu_s / (1 + 3 * nu_s) * (math.exp((1 + 3 * nu_s) * (Nb - Ni_bar)) - 1)   # rho_c / rho_r, same in proper time for T/tau
        return x
    xA = patch(1.0, "T")
    for sw in ("T", "tau", "clock"):
        xB = patch(math.exp(zeta), sw)
        S = math.log(xB / xA)            # entropy perturbation of the cold energy w.r.t. radiation at equal rho_r: S = d ln(rho_c/rho_r^(3/4)) ~ d ln x
        beta_iso = S**2 / (S**2 + zeta**2)
        iso[sw] = dict(S_over_zeta=S / zeta, beta_iso=beta_iso, pass_=beta_iso <= 0.02)
        P(f"    switch {sw:5s}: S/zeta = {S/zeta:+.3e}, beta_iso = {beta_iso:.3e}  ({'pass' if beta_iso <= 0.02 else 'FAIL'})")
    P("    -> a switch keyed to the local temperature or to local proper time is adiabatic (S = 0): in the growing mode both are")
    P("       the same local clock. Isocurvature appears only for a trigger with its OWN fluctuation (a spectator clock):")
    P("       S = (1/2) d ln t_i per unit, so beta_iso <= 0.02 needs |d tau / t_i| <= 0.29 zeta. CORRECTION to the frozen hand")
    P("       expectation 'S-t EXCLUDED': a global-time switch is not excluded unless its clock fluctuates independently.")

if MUTATE:
    m1_mut_ok = all(not r["amount_reachable"] for r in rows)
    P(f"\n  MUTATE M1 wrong sign (nu < 0, cold -> vacuum): amount reachable at {sum(r['amount_reachable'] for r in rows)} of {len(rows)} nu values")
    check("MUTATE M1: the wrong-sign exchange fails C-AMOUNT at every nu (produces no positive cold energy)", m1_mut_ok)
    m1_verdict = "MUTATE"
else:
    if passing:
        m1_verdict = "RESTATEMENT"
    else:
        m1_verdict = "EXCLUDED"
    P(f"\n  M1 parameter values passing C-AMOUNT + C-PRESENT + C-NEFF + C-LATE: nu <= {nu_max_present:.0e} (grid); "
      f"amount = (nu, T_i) -> one free combination nu/a_i for one number")
    lst = ", ".join("%.0e" % r["nu"] for r in desi_any)
    P("  Any nu reproducing DESI (dchi2 >= 4 on PP, U3, DY5)?  " + ("yes at nu = " + lst if desi_any else "NO, at any nu on the grid"))
    P(f"  ... and also passing C-PRESENT + C-NEFF?  {'YES' if desi_ok else 'NO'}")
    P(f"  M1 VERDICT: {m1_verdict}  (two constants nu, T_i; the amount is their combination; DESI not reproduced)")
OUT["M1"] = dict(rows=rows, iso=iso, nu_max_present=nu_max_present, reproduces_DESI_any=[r["nu"] for r in desi_any],
                 reproduces_DESI_and_passes=[r["nu"] for r in desi_ok], verdict=m1_verdict)

# ================================================================ M2: baryon-sourced dust charge of the MOND field
P("\n=== M2: the MOND field's dust branch with its charge SOURCED BY BARYONS (A = exp(beta phi/Mbar_Pl)) ===")
# units: Mbar_Pl = 1, H0 = 1 -> rho_crit0 = 3.  LCDM background (test field).  P(X) = -rho_L + (M^4/2)(X/X0 - 1)^2
beta = 0.0 if MUTATE else 1.0
X0f, M4 = 0.5 * (1e-3)**2, 1e6           # phidot0 = 1e-3 (H0 Mbar_Pl units), M^4 >> sourced charge -> linear regime
phid0 = math.sqrt(2 * X0f)
rhob0 = 3 * Ob
def Hf(a):
    return math.sqrt(Or * a**-4 + (Ob + Oc) * a**-3 + OL)
def rhs(N, y):
    a = math.exp(N); J, phi, t = y; Hh = Hf(a)
    eps = J / (a**3 * (M4 / X0f) * phid0)             # first guess; refine with phidot = phid0 sqrt(1+eps)
    for _ in range(3):
        eps = J / (a**3 * (M4 / X0f) * phid0 * math.sqrt(1 + eps))
    phidot = phid0 * math.sqrt(1 + eps)
    return [beta * a**3 * (rhob0 * a**-3) / Hh, phidot / Hh, 1.0 / Hh]
N0, N1 = math.log(1e-9), 0.0
sol = solve_ivp(rhs, [N0, N1], [0.0, 0.0, 0.0], rtol=1e-11, atol=1e-30, dense_output=True, method="DOP853")
def m2_state(a):
    J, phi, t = sol.sol(math.log(a))
    eps = J / (a**3 * (M4 / X0f) * phid0)
    for _ in range(5):
        eps = J / (a**3 * (M4 / X0f) * phid0 * math.sqrt(1 + eps))
    X = X0f * (1 + eps)
    PX = (M4 / X0f) * eps; Pv = -OL * 3 + 0.5 * M4 * eps**2
    rho_d = 2 * X * PX - Pv - OL * 3                  # field energy minus its vacuum part
    return rho_d / (rhob0 * a**-3), beta * phi, t
ident = []
for a in (1e-4, 1e-3, 0.1, 1.0):
    Rs, dlnA, t = m2_state(a)
    ident.append((a, Rs, dlnA))
    P(f"  a = {a:7.0e}: rho_d,src/rho_b = {Rs:.6e}   Delta ln A = {dlnA:.6e}   ratio {Rs/dlnA if dlnA else float('nan'):.6f}")
if MUTATE:
    m2_mut_ok = all(abs(Rs) < 1e-12 for _, Rs, _ in ident)
    check("MUTATE M2: beta = 0 -> sourced share vanishes (|R_src| < 1e-12)", m2_mut_ok, f"(max {max(abs(Rs) for _, Rs, _ in ident):.1e})")
    m2_verdict = "MUTATE"; m2 = {}
else:
    check("K3 M2 identity rho_d,src/rho_b = Delta ln A (to 1e-2 relative, linear regime)", all(abs(Rs / dl - 1) < 1e-2 for _, Rs, dl in ident),
          f"(max dev {max(abs(Rs/dl-1) for _, Rs, dl in ident):.1e})")
    # the share grows like the elapsed time since the source switched on: R_src(t) = beta phidot0 t / Mbar_Pl
    t_yr = lambda z: t_of_a(1 / (1 + z)) * 1e9
    t3000, t1100, t0 = t_yr(3000), t_yr(1100), t_yr(0)
    rate_tie = 5.364 / t1100                          # d ln A/dt [1/yr] for R_src(z=1100) = 5.364
    gdot_tie = 2 * rate_tie
    drift_tie = t1100 / t3000 - 1
    dlnA_since = rate_tie * t0
    rate_today = 5.364 / t0                           # the softer option: R_src(today) = 5.364
    Rmax_today = (2e-13 / 2) * t0                     # C-GDOT ceiling on the sourced share today
    P(f"  times (LCDM): t(3000) = {t3000:.4e} yr, t(1100) = {t1100:.4e} yr, t0 = {t0:.4e} yr")
    P(f"  tie R_src(z=1100) = 5.364 needs d ln A/dt = {rate_tie:.3e}/yr -> |Gdot/G| = {gdot_tie:.2e}/yr (bound 2e-13: x{gdot_tie/2e-13:.1e});")
    P(f"     comoving drift z 3000 -> 1100 = {drift_tie:+.2f} (bound 0.01); Delta ln A to today = {dlnA_since:.2e} (BBN/CMB bound 0.05)")
    P(f"  softer tie R_src(today) = 5.364: |Gdot/G| = {2*rate_today:.2e}/yr (x{2*rate_today/2e-13:.1e} over); share at z=1100 = {5.364*t1100/t0:.2e}, "
      f"i.e. not present by recombination")
    P(f"  C-GDOT ceiling on the baryon-sourced share today: R_src <= {Rmax_today:.2e} = {Rmax_today/5.364:.1e} of 5.364")
    m2 = dict(t3000_yr=t3000, t1100_yr=t1100, t0_yr=t0, gdot_tie_per_yr=gdot_tie, drift_tie_3000_1100=drift_tie, dlnA_to_today_tie=dlnA_since,
              gdot_soft_per_yr=2 * rate_today, Rsrc_max_today=Rmax_today, C_PRESENT_tie=abs(drift_tie) <= 0.01, C_GDOT_tie=gdot_tie <= 2e-13)
    tie_excluded = not (m2["C_PRESENT_tie"] and m2["C_GDOT_tie"])
    m2_verdict = "RESTATEMENT (baryon-sourced tie EXCLUDED: C-PRESENT, C-GDOT; amount = the free initial charge J_i, CFG288 A2)" if tie_excluded else "VIABLE-CONDITIONAL"
    P("  inherited (not re-run): the dust branch needs an extra scale M (CFG288 road S: M >= 4.24 eV) and breaks at stream crossing (L374).")
    P(f"  M2 VERDICT: {m2_verdict}")
OUT["M2"] = dict(identity=ident, beta=beta, verdict=m2_verdict, **m2)

# ================================================================ M3: dark-energy seesaw relic (forces a particle)
P("\n=== M3: dark-energy seesaw relic m* = sqrt(rho_L^(1/4) M), thermal freeze-out  [FORCES A FIELD QUANTUM] ===")
MBAR, MPL = 2.435e18, 1.22089e19                      # GeV
RHOC_GEV4 = 8.0992e-47                                # rho_crit0 / h^2 in GeV^4
GEV2_TO_CM3S = 1.1674e-17
GSTAR_T = np.array([1e-4, 1e-3, 0.01, 0.1, 0.15, 0.2, 0.5, 1.0, 2.0, 4.0, 10.0, 50.0, 80.0, 100.0, 150.0, 300.0, 1e4])
GSTAR_G = np.array([3.36, 10.75, 10.75, 17.25, 40.0, 55.0, 61.75, 69.0, 75.75, 80.0, 86.25, 86.25, 90.0, 96.0, 102.0, 106.75, 106.75])


def gstar(T):
    return float(np.interp(math.log10(max(T, 1e-4)), np.log10(GSTAR_T), GSTAR_G))


def omega_h2(m, sv, g):
    """Boltzmann: dW/dx = -(lam/x^2)(e^W - e^{2Weq - W}), W = ln Y; Omega h^2 = 2.744e8 m Y_inf."""
    def lnYeq(x):
        gs = gstar(m / x)
        return math.log(45 / (4 * math.pi**4) * g / gs * x**2) + math.log(kve(2, x)) - x
    def f(x, W):
        T = m / x; gs = gstar(T)
        lam = math.sqrt(math.pi / 45) * MPL * math.sqrt(gs) * m * sv
        We = lnYeq(x)
        return [-(lam / x**2) * (math.exp(W[0]) - math.exp(2 * We - W[0]))]
    s = solve_ivp(f, [1.0, 2000.0], [lnYeq(1.0)], method="Radau", rtol=1e-8, atol=1e-10)
    dev = np.abs(s.y[0] - np.array([lnYeq(x) for x in s.t]) - math.log(2.5))     # x_f: Y = 2.5 Y_eq
    return 2.744e8 * m * math.exp(s.y[0, -1]), float(s.t[np.argmin(dev)])


if not MUTATE:
    ok4, xf4 = omega_h2(100.0, 2.2e-26 / GEV2_TO_CM3S, 2)
    check("K4 M3 Boltzmann: m = 100 GeV, <sigma v> = 2.2e-26 cm^3/s -> Omega h^2 in [0.10, 0.13]", 0.10 <= ok4 <= 0.13, f"({ok4:.4f}, x_f ~ {xf4:.1f})")

ALPHAS = [("1/137", 1 / 137.036), ("1/128", 1 / 128.0), ("alpha_W", 0.0338), ("1/4pi", 1 / (4 * math.pi)), ("alpha_s", 0.118), ("1", 1.0)]
KS = [0.25, 0.5, 1.0, 2.0]; GS = [1, 2, 4]; MS = [("Mbar_Pl", MBAR), ("M_Pl", MPL)]


def rhoL_gev4(omc):
    OLp = 1 - (om_b + omc) / h**2 - Or
    return OLp * RHOC_GEV4 * h**2


def mstar(omc, M):
    return math.sqrt(rhoL_gev4(omc) ** 0.25 * M)


def score(omc_target, table=None, m_override=None):
    hits, rows3 = 0, []
    for mn, M in MS:
        m = mstar(omc_target, M) if m_override is None else m_override[mn]
        for an, al in ALPHAS:
            for k in KS:
                for g in GS:
                    sv = k * math.pi * al**2 / m**2
                    oh2 = table(mn, m, an, k, g) if table else omega_h2(m, sv, g)[0]
                    hit = abs(oh2 - omc_target) <= 0.001 * omc_target / 0.120
                    hits += hit; rows3.append(dict(M=mn, m=m, alpha=an, k=k, g=g, sv_cm3s=sv * GEV2_TO_CM3S, omega_h2=oh2, hit=bool(hit)))
    return hits, rows3


m3 = {}
if not MUTATE:
    P(f"  rho_L^(1/4) = {rhoL_gev4(om_c)**0.25*1e12:.4f} meV;  m*(Mbar_Pl) = {mstar(om_c, MBAR):.1f} GeV,  m*(M_Pl) = {mstar(om_c, MPL):.1f} GeV")
    hits, rows3 = score(om_c)
    oh = np.array([r["omega_h2"] for r in rows3])
    best = min(rows3, key=lambda r: abs(math.log(r["omega_h2"] / 0.120)))
    P(f"  144 forms: Omega h^2 spans {oh.min():.3g} .. {oh.max():.3g} (median {np.median(oh):.3g}); hits within 0.120 +- 0.001: {hits}  (p = {hits/144:.4f})")
    P(f"  closest form: M = {best['M']}, alpha = {best['alpha']}, k = {best['k']}, g = {best['g']}: Omega h^2 = {best['omega_h2']:.4f} "
      f"(<sigma v> = {best['sv_cm3s']:.2e} cm^3/s)")
    for r in rows3:
        if r["hit"]:
            P(f"    HIT: M = {r['M']}, alpha = {r['alpha']}, k = {r['k']}, g = {r['g']}: Omega h^2 = {r['omega_h2']:.5f}")
    # alpha needed for each M/k/g: Omega ~ 1/<sigma v> ~ m^2/alpha^2 -> the amount is the coupling
    P("  scaling: Omega h^2 ~ m*^2 / (k alpha^2), so the amount is set by the chosen coupling (a continuous dial), not by rho_L alone.")
    # free streaming with a late kinetic decoupling T_kd = 1 MeV (conservative)
    m = mstar(om_c, MBAR); Tkd = 1e-3; akd = 2.348e-13 / Tkd * (3.91 / 10.75) ** (1 / 3); vkd = math.sqrt(3 * Tkd / m)
    lam_fs = vkd * akd * math.log(om_r / (om_c + om_b) / akd) * (2997.92 / h) / math.sqrt(Or)
    P(f"  C-COLD: free-streaming length (T_kd = 1 MeV) = {lam_fs:.1e} Mpc (< 0.1); C-PRESENT: frozen out at T ~ m*/x_f ~ {m/25:.0f} GeV (z ~ 1e14);")
    P("  C-NEFF: non-relativistic at BBN, its energy there is negligible; C-ADIAB: a thermal relic of the reheated plasma is adiabatic.")
    P("  C-PARTICLE: YES, a TeV-scale massive particle (a WIMP-like field quantum). Direct/indirect detection: not tested here (no data on disk).")
    pred = (hits >= 1) and (hits / 144 < 0.01)
    m3_verdict = ("PREDICTIVE-PENDING (check MUTATE scrambled draws)" if pred else
                  "RESTATEMENT (amount set by the chosen coupling; passes C-COLD/C-PRESENT/C-NEFF/C-ADIAB as a standard WIMP; FORCES A PARTICLE)")
    P(f"  M3 VERDICT: {m3_verdict}")
    m3 = dict(m_star_GeV={mn: mstar(om_c, M) for mn, M in MS}, hits=hits, p=hits / 144, best=best, rows=rows3, lam_fs_Mpc=lam_fs, verdict=m3_verdict)
else:
    # scrambled cosmology: 200 draws R' in [3, 8]; precompute Omega h^2 on an m grid per form (m* moves only as rho_L'^(1/8))
    rng = np.random.default_rng(507)
    Rs = rng.uniform(3, 8, 200)
    omcs = Rs * om_b
    grids = {}
    for mn, M in MS:
        ms = [mstar(o, M) for o in omcs]
        grids[mn] = np.linspace(min(ms) * 0.999, max(ms) * 1.001, 7)
    TAB = {}
    for mn, _ in MS:
        for an, al in ALPHAS:
            for k in KS:
                for g in GS:
                    TAB[(mn, an, k, g)] = np.array([omega_h2(mm, k * math.pi * al**2 / mm**2, g)[0] for mm in grids[mn]])
    def table(mn, m, an, k, g):
        return float(np.exp(np.interp(m, grids[mn], np.log(TAB[(mn, an, k, g)]))))
    hits_d = []
    for o in omcs:
        hd, _ = score(o, table=table)
        hits_d.append(hd)
    hits_d = np.array(hits_d)
    real_hits, _ = score(om_c, table=table) if (min(omcs) <= om_c <= max(omcs)) else (None, None)
    P(f"  200 scrambled cosmologies (R' in [3, 8]): hits per draw mean {hits_d.mean():.3f}, max {hits_d.max()}, draws with >= 1 hit {int((hits_d>=1).sum())}, "
      f"99th percentile {np.percentile(hits_d, 99):.1f}")
    P(f"  real cosmology on the same interpolated tables: {real_hits} hits")
    m3 = dict(hits_per_draw_mean=float(hits_d.mean()), hits_per_draw_max=int(hits_d.max()), draws_with_hit=int((hits_d >= 1).sum()),
              p99=float(np.percentile(hits_d, 99)), real_hits_interp=real_hits, R_draws=Rs.tolist(), hits=hits_d.tolist())
    REAL_EXACT_HITS = 1                               # from the main run (exact solves), cfg507_origin.out
    pred = REAL_EXACT_HITS > np.percentile(hits_d, 99)
    P(f"  frozen PREDICTIVE leg: real exact hits {REAL_EXACT_HITS} {'>' if pred else '<='} scrambled 99th percentile {np.percentile(hits_d, 99):.1f} "
      f"-> M3 PREDICTIVE: {'YES' if pred else 'NO'}; fraction of scrambled draws with >= as many hits: {(hits_d >= REAL_EXACT_HITS).mean():.3f}")
    m3["predictive"] = bool(pred); m3["frac_draws_ge_real"] = float((hits_d >= REAL_EXACT_HITS).mean())
    m3_verdict = "MUTATE"
OUT["M3"] = {**m3, "verdict": m3_verdict}

# ---------------------------------------------------------------- summary
P("\n=== SUMMARY ===")
if not MUTATE:
    P(f"  M1 early running vacuum -> cold:  {m1_verdict}")
    P(f"  M2 baryon-sourced MOND-field charge: {m2_verdict}")
    P(f"  M3 dark-energy seesaw relic:      {m3_verdict}")
    if m3_verdict.startswith("PREDICTIVE-PENDING"):
        P("  PREDICTIVE result: none for M1/M2; M3 has one grammar hit, decided by the scrambled-cosmology MUTATE run (frozen rule).")
    else:
        P("  PREDICTIVE result: none.")
    P("  The cold energy's origin is still an input unless the M3 MUTATE says otherwise; its mass is still required. kappa = 1/2 fitted.")
P(f"\n{sum(CH)}/{len(CH)} checks pass")
open(os.path.join(HERE, SLUG + ".out"), "w").write("\n".join(LOG) + "\n")
json.dump(OUT, open(os.path.join(HERE, SLUG + "_results.json"), "w"), indent=1, default=float)
raise SystemExit(0 if all(CH) else 1)
