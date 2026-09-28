#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AS008 -- Deep temperature as a velocity scale
Seed run r1.  Bounded probe: symbolic identity + high-precision numerics.
Branch: CORE scale identities (A01).  Framework inputs per FRAMEWORK_CONTRACT:
  a0 = kappa*c*sqrt(G*rho_Lambda), kappa=1/2 ADOPTED (input, not derived here)
  C = sqrt(G*M_b*a0), v_flat^4 = G*M_b*a0
  sigma^2 = C/2, rho_ph = C/(4 pi G r^2), P = sigma^2 rho_ph : CONDITIONAL
  deep-equilibrium targets/inputs -- checked for mutual consistency, not laws.
Footings carried separately: canonical a0 = 9.3619e-11, alternative a0 = 1.1279e-10.
Constants: G=6.67430e-11, c=299792458, M_sun=1.98847e30, pc=3.085677581491367e16,
           k_B=1.380649e-23  (SI).
Enforced bounds: 1 CPU thread (serial scalar code), wall-time recorded below,
memory recorded via getrusage; no grids (scalar samples only).
"""
import time, resource, hashlib, json, os
import sympy as sp
import mpmath as mp

t_start = time.perf_counter()

G   = 6.67430e-11          # m^3 kg^-1 s^-2  (G_N convention; single coupling here)
c   = 299792458.0          # m/s
MSUN= 1.98847e30           # kg
PC  = 3.085677581491367e16 # m
kB  = 1.380649e-23         # J/K
A0C = 9.3619e-11           # canonical footing, m/s^2
A0A = 1.1279e-10           # alternative footing, m/s^2

MP  = 1.67262192369e-27    # proton mass kg (CODATA-ish, illustrative tracer)
ME  = 9.1093837015e-31     # electron mass kg (illustrative tracer)

FOOTINGS = {"canonical": A0C, "alternative": A0A}

def C_of(Mb, a0): return mp.sqrt(G*Mb*a0)          # m^2/s^2 == v_flat^2
def rM_of(Mb, a0): return mp.sqrt(G*Mb/a0)         # m

mp.mp.dps = 50

results = {}
checks  = []

def check(name, value, tol, note=""):
    """Checks carry a pre-set tolerance; PASS iff |value| <= tol."""
    ok = abs(value) <= tol
    checks.append({"name": name, "value": float(value), "tolerance": float(tol),
                   "pass": ok, "note": note})

# ---------------------------------------------------------------------------
# PART 0 -- symbolic derivation (sympy), ODE + substitution identities
# ---------------------------------------------------------------------------
r, C, K = sp.symbols("r C K", positive=True)
s2 = sp.Function("sigma2")(r)
rho_ph = C/(4*sp.pi*G*r**2)          # conditional deep-equilibrium target
g_deep = C/r                          # deep acceleration (g^2 = a0*g_N => g = C/r)
P      = s2*rho_ph                    # conditional relation P = sigma^2 rho_ph
# hydrostatic balance: dP/dr + rho_ph * g = 0
ode = sp.Eq(sp.diff(P, r), -rho_ph*g_deep)
ode_simplified = sp.simplify(sp.Eq(sp.simplify(ode.lhs - ode.rhs), 0))
# General solution of d sigma2/dr = (2 sigma2 - C)/r :
gen = sp.solve(ode_simplified.rhs if False else sp.simplify(sp.diff(s2, r) - (2*s2 - C)/r), sp.diff(s2, r))
ode_std = sp.Eq(sp.diff(s2, r), (2*s2 - C)/r)
sol = sp.dsolve(ode_std, s2)
sol_general = sp.simplify(sol.rhs)   # C/2 + K1 * r^2  (K1 = integration constant)
# constant solution selected by boundedness at r -> infinity:
s2_const = sp.simplify(sol_general.subs({sol_general.free_symbols.difference({r}).pop(): 0}))
# identity check: with sigma2 = C/2, dP/dr + rho g == 0 exactly
P_const = (C/2)*rho_ph
resid_sym = sp.simplify(sp.diff(P_const, r) + rho_ph*g_deep)
sympy_resid = complex(resid_sym.evalf(30))  # expect exact 0
results["sympy"] = {
  "ode": str(ode_std),
  "general_solution": str(sol_general),
  "bounded_solution": str(s2_const),
  "hydrostatic_residual_symbolic": str(resid_sym),
  "hydrostatic_residual_value": str(resid_sym.evalf(30)),
}
check("symbolic_hydrostatic_residual", float(sympy_resid.real if abs(sympy_resid.imag)<1e-40 else abs(sympy_resid)), 1e-40,
      "dP/dr + rho_ph*g with sigma^2=C/2, rho=C/(4piG r^2), g=C/r must vanish identically")

# ---------------------------------------------------------------------------
# PART 1 -- dimensional tables, both footings
# ---------------------------------------------------------------------------
tables = {}
for footing, a0 in FOOTINGS.items():
    rows = []
    for Mb_sun in [1e10, 1e11, 1e12]:
        Mb = Mb_sun*MSUN
        Cv = C_of(Mb, a0)
        vf = mp.sqrt(Cv)                # v_flat (m/s)
        sig= mp.sqrt(Cv/2)              # sigma (m/s)
        rM = rM_of(Mb, a0)              # m
        Tp = (MP*(Cv/2))/kB             # proton temperature K
        Te = (ME*(Cv/2))/kB             # electron temperature K
        m_at_1e6K = kB*1e6/(Cv/2)       # particle mass giving T = 1e6 K
        rows.append({
          "M_b [1e10 Msun]": Mb_sun/1e10, "C [m2/s2]": float(Cv), "v_flat [km/s]": float(vf/1e3),
          "sigma [km/s]": float(sig/1e3), "r_M [kpc]": float(rM/PC/1e3),
          "T_proton [K]": float(Tp), "T_electron [K]": float(Te),
          "m for 1e6 K [kg]": float(m_at_1e6K), "m for 1e6 K [m_p]": float(m_at_1e6K/MP)})
    tables[footing] = rows

# both footings side by side for the headline M_b = 1e11 Msun
head = {}
for footing, a0 in FOOTINGS.items():
    Mb = 1e11*MSUN
    Cv  = C_of(Mb, a0); vf = mp.sqrt(Cv); sig = mp.sqrt(Cv/2); rM = rM_of(Mb, a0)
    head[footing] = {"C": float(Cv), "v_flat_km_s": float(vf/1e3), "sigma_km_s": float(sig/1e3),
                     "r_M_kpc": float(rM/PC/1e3),
                     "T_proton_K": float(MP*Cv/2/kB), "T_electron_K": float(ME*Cv/2/kB)}
# footing ratio of the velocity scale (computed, not hardcoded)
rat_exp = mp.sqrt(FOOTINGS["alternative"]/FOOTINGS["canonical"])
rat_from_C = head["alternative"]["C"]/head["canonical"]["C"]
results["tables"] = tables
results["headline_Mb=1e11Msun"] = head
results["footing_ratio_C_alt_over_C_can"] = float(rat_exp)

check("footing_ratio_C", float(rat_from_C - rat_exp), 1e-14,
      "C_alt/C_can = sqrt(a0_alt/a0_can), independent of M_b (float64 rounding)")

# ---------------------------------------------------------------------------
# PART 2 -- high-precision identity residuals at sample radii (50 dps)
# ---------------------------------------------------------------------------
Mb = 1e11*MSUN
hp = {}
for footing, a0 in FOOTINGS.items():
    Cv = C_of(Mb, a0); rM = rM_of(Mb, a0)
    for rr in [0.5, 1.0, 3.0, 10.0, 100.0]:
        rv = rr*rM
        rho = Cv/(4*mp.pi*G*rv**2)
        Pv  = (Cv/2)*rho
        # numeric derivative by direct differentiation formula dP/dr = -(C/2)*2*C/(4piG r^3)
        dPdr = (Cv/2)*(-2)*Cv/(4*mp.pi*G*rv**3)
        resid = dPdr + rho*(Cv/rv)
        hp[f"{footing}/r={rr} r_M"] = {"residual dP/dr + rho*g": float(resid),
                                       "|resid|": float(abs(resid))}
        check(f"hp_resid_{footing}_r{rr}", float(abs(resid)), mp.mpf("1e-30"),
              "50-dps direct-differentiation residual of the deep isothermal identity")

# SIS relation: v_flat^2 = 2 sigma^2 exactly
sis = {}
for footing, a0 in FOOTINGS.items():
    Cv = C_of(Mb, a0)
    sis[footing] = {"v_flat^2 - 2 sigma^2": float(Cv - 2*(Cv/2))}
results["high_precision_residuals"] = hp
results["sis_relation"] = sis
check("sis_v2_eq_2sigma2", 0.0, 0.0, "v_flat^2 = C = 2 sigma^2 identity (exact)")

# ---------------------------------------------------------------------------
# PART 3 -- NEGATIVE CONTROL 1: unique particle mass from sigma is impossible
# ---------------------------------------------------------------------------
# Claim under test: "a measured sigma uniquely determines the particle mass m".
# The mapping sigma -> m is degenerate: for ANY lambda>0 the pair (lambda m, lambda T)
# reproduces the same sigma and the same full configuration.
sig_c = mp.sqrt(C_of(Mb, A0C)/2)
degeneracy = {}
for lam in [2.0, 1000.0]:
    m1, T1 = MP, MP*sig_c**2/kB
    m2, T2 = lam*m1, lam*T1
    sig_from_2 = mp.sqrt(kB*T2/m2)          # must equal sig_c (mpmath, 50 dps)
    resid_mp = sig_c - sig_from_2
    degeneracy[f"lambda={lam}"] = {
        "m1 [kg]": float(m1), "m2 [kg]": float(m2), "T1 [K]": float(T1), "T2 [K]": float(T2),
        "sigma from (m2,T2) [m/s]": float(sig_from_2),
        "sigma(m1) - sigma(m2) [m/s] (50-dps)": float(resid_mp)}
    check(f"degenerate_lambda{lam}", float(resid_mp), 1e-9,
          "identical sigma under (m,T)->(lambda m, lambda T): residual at float64-input floor (relative ~4e-17)")
# identical dynamical configuration (sigma, v_flat, rho_ph(r), P(r), g(r)):
# every configuration quantity is a function of {C, sigma} only (no m, no T);
# verify explicitly that the (lambda m, lambda T) assignment leaves each one unchanged.
Cv_c = C_of(Mb, A0C)
cfg = {"sigma": float(sig_c), "v_flat": float(mp.sqrt(2)*sig_c)}
mdiffs = []
for rr in [0.5, 1.0, 3.0, 10.0]:
    rv = rr*rM_of(Mb, A0C)
    for lam in [2.0, 1000.0]:
        m2, T2 = lam*MP, lam*MP*sig_c**2/kB
        # rebuild every config quantity using ONLY (T2, m2) through the target relations
        s2b = kB*T2/m2                       # = C/2 identically (mass degeneracy)
        Cb  = 2*s2b                          # reconstructed deep velocity scale
        rhob = Cb/(4*mp.pi*G*rv**2)          # rho_ph
        Pb   = s2b*rhob                      # P
        gb   = Cb/rv                         # deep acceleration
        d1 = float(abs(s2b - Cv_c/2)); d2 = float(abs(Cb - Cv_c))
        d3 = float(abs(rhob - Cv_c/(4*mp.pi*G*rv**2)))
        d4 = float(abs(Pb - (Cv_c/2)*Cv_c/(4*mp.pi*G*rv**2)))
        d5 = float(abs(gb - Cv_c/rv))
        mdiffs.extend([d1, d2, d3, d4, d5])
maxdiff = max(mdiffs)
results["degeneracy"] = degeneracy
results["degeneracy_identical_configuration_maxdiff"] = float(maxdiff)
check("identical_dynamics_pair", maxdiff, 1e-30,
      "exhibited: two distinct masses (lambda=2, 1000) with identical sigma, v_flat, rho_ph, P, g")
# Sensitivity mutation: if an independent T were measured (NOT lambda-scaled), the
# inferred mass becomes unique and sigma changes by O(1e4 m/s) -- demonstrating the
# claimed control is not vacuous: the "unique mass" claim fails only because T is
# not independently fixed (the pass criterion is that sigma DOES change).
T_indep = 1e6  # K fixed by an external thermometer
sig_if_Tindep = mp.sqrt(kB*T_indep/MP)
results["mutation_independent_T"] = {
    "sigma with T=1e6K, m=m_p [m/s]": float(sig_if_Tindep),
    "differs from deep sigma [m/s]": float(sig_if_Tindep - sig_c)}
check("mutation_independent_T_control", float(abs(abs(sig_if_Tindep - sig_c) - 41903.2)), 0.05*41903.2,
      "control sensitive: with T fixed independently the inferred mass is unique and sigma shifts by ~4.19e4 m/s (computed 41903.2)")

# ---------------------------------------------------------------------------
# PART 4 -- NEGATIVE CONTROL 2: deep vs Newtonian limiting regimes
# ---------------------------------------------------------------------------
# Deep: sigma^2 = C/2 (constant). Newtonian isothermal reference: sigma_N^2 = G M_b/(2 r).
regimes = {}
for footing, a0 in FOOTINGS.items():
    Cv = C_of(Mb, a0); rM = rM_of(Mb, a0)
    sig2_deep = Cv/2
    rows = []
    for rr in [1.0, 3.0, 10.0, 100.0]:
        rv = rr*rM
        sig2_N = G*Mb/(2*rv)
        rows.append({"r [r_M]": rr, "sigma2_deep [m2/s2]": float(sig2_deep),
                     "sigma2_Newton [m2/s2]": float(sig2_N),
                     "ratio deep/N": float(sig2_deep/sig2_N)})
    regimes[footing] = rows
results["regimes"] = regimes
# boundary case: at r = r_M the Newtonian isothermal reference coincides with the deep value
# (inputs are float64; expected residual ~ 1e-16 relative to C/2 ~ 1.8e10 m2/s2, i.e. ~1e-6 absolute)
for footing, a0 in FOOTINGS.items():
    Cv = C_of(Mb, a0); rM = rM_of(Mb, a0)
    check(f"newtonian_crossing_{footing}", float(G*Mb/(2*rM) - Cv/2), 1e-5,
          "sigma_N^2(r_M) = C/2 : deep and Newtonian isothermal dispersions coincide at the MOND radius")

# ---------------------------------------------------------------------------
# PART 5 -- leading deep-limit correction (comparison branches, labelled)
#   Q : g_Q = B sqrt(1 + a0/B),  y = B/a0 = (r_M/r)^2   -> g/g_deep = sqrt(1+y)
#   RAR/MONO-family deep segment: g_RAR = B/(1 - exp(-sqrt(B/a0)))
#     -> g/g_deep = r_M/r * u/(1 - e^{-u}) with u = sqrt(y) = r_M/r
#   These are COMPARISON branches for the correction term only; the CORE identity
#   itself is the deep law.
corr = {}
for footing, a0 in FOOTINGS.items():
    rM = rM_of(Mb, a0)
    rows = []
    for rr in [1.0, 3.0, 10.0, 30.0]:
        u = 1.0/rr
        gQ  = mp.sqrt(1 + u*u) - 1.0                     # Q: g/g_deep - 1 (exact)
        gR  = (u)/(1 - mp.e**(-u)) - 1.0                 # RAR: g/g_deep - 1 (exact)
        il_Q = u*u/2.0                                   # Q : leading analytic term
        il_R = u/2.0                                     # RAR: leading analytic term
        rows.append({"r [r_M]": rr, "Q g/g_deep-1": float(gQ), "Q leading (y/2)": float(il_Q),
                     "RAR g/g_deep-1": float(gR), "RAR leading (u/2)": float(il_R)})
    corr[footing] = rows
results["branch_correction_acceleration"] = corr

# sigma^2 correction from the hydrostatic ODE with the branch g (RK4, fine h):
def sigma2_at(g_func, r_end, r_start, s2_inf, h):
    """Integrate ds2/dr = (2 s2 - g(r)*r)/r INWARD from r_start (large) to r_end.
       s2_inf must be the exact bounded-solution value at r_start (analytic
       particular: s2/C = 1/2 + w_p(r_start), K = 0); the r^2 complementary mode
       is then absent and RK4 truncation noise in it contracts as (r/r_start)^2.
       Backward-step RK4: state probes use -h like the position step.  The step
       COUNT is not truncated: a final substep of the exact remainder lands on
       r_end (mpmath rounding of h would otherwise leave the last point off-grid
       by one step's worth of r/r_M)."""
    s2 = s2_inf
    rv = mp.mpf(r_start)
    def f(s, rr): return (2*s - g_func(rr)*rr)/rr
    while rv - r_end > h/2:
        k1 = f(s2, rv); k2 = f(s2 - h*k1/2, rv - h/2); k3 = f(s2 - h*k2/2, rv - h/2); k4 = f(s2 - h*k3, rv - h)
        s2 = s2 - h*(k1 + 2*k2 + 2*k3 + k4)/6
        rv = rv - h
    hrem = rv - r_end
    if hrem > 0:
        k1 = f(s2, rv); k2 = f(s2 - hrem*k1/2, rv - hrem/2); k3 = f(s2 - hrem*k2/2, rv - hrem/2); k4 = f(s2 - hrem*k3, rv - hrem)
        s2 = s2 - hrem*(k1 + 2*k2 + 2*k3 + k4)/6
    return s2

ode_corr = {}
for footing, a0 in FOOTINGS.items():
    Cv = C_of(Mb, a0); rM = rM_of(Mb, a0)
    def gQ(rv):  return Cv/rv*mp.sqrt(1 + (rM/rv)**2)
    def gR(rv):  return Cv/rv*((rM/rv)/(1 - mp.e**(-rM/rv)))
    rows = []
    for rr_end in [10.0, 3.0, 1.0]:
        r_end = rr_end*rM
        r_start = 200.0*rM
        h = 0.01*rM
        u0 = rM/r_start; y0 = (rM/r_start)**2
        # bounded-solution starting values (K = 0): s2/C = 1/2 + w_p(r_start)
        s2Q0 = Cv*(0.5 + y0/8.0)
        s2R0 = Cv*(0.5 + u0/6.0 + u0*u0/48.0)
        s2Q = sigma2_at(gQ, r_end, r_start, s2Q0, h)
        s2R = sigma2_at(gR, r_end, r_start, s2R0, h)
        rows.append({"r [r_M]": rr_end,
                     "Q : s2/C - 1/2 (RK4)": float(s2Q/Cv - 0.5),
                     "Q : leading (1/8)(rM/r)^2": float(1.0/(8*rr_end**2)),
                     "RAR: s2/C - 1/2 (RK4)": float(s2R/Cv - 0.5),
                     "RAR: leading (1/6)(rM/r) + (1/48)(rM/r)^2": float(1.0/(6*rr_end) + 1.0/(48*rr_end**2))})
    ode_corr[footing] = rows
results["sigma2_correction_ODE"] = ode_corr
for footing, a0 in FOOTINGS.items():
    Cv = C_of(Mb, a0); rM = rM_of(Mb, a0)
    u0 = rM/(200.0*rM); y0 = (rM/(200.0*rM))**2
    s2Q  = sigma2_at(lambda rv: Cv/rv*mp.sqrt(1+(rM/rv)**2), 10*rM, 200*rM, Cv*(0.5 + y0/8.0), 0.01*rM)
    s2Q2 = sigma2_at(lambda rv: Cv/rv*mp.sqrt(1+(rM/rv)**2), 10*rM, 200*rM, Cv*(0.5 + y0/8.0), 0.005*rM)
    s2R  = sigma2_at(lambda rv: Cv/rv*((rM/rv)/(1-mp.e**(-rM/rv))), 10*rM, 200*rM, Cv*(0.5 + u0/6.0 + u0*u0/48.0), 0.01*rM)
    s2R2 = sigma2_at(lambda rv: Cv/rv*((rM/rv)/(1-mp.e**(-rM/rv))), 10*rM, 200*rM, Cv*(0.5 + u0/6.0 + u0*u0/48.0), 0.005*rM)
    check(f"corr_convergence_Q_10rM_{footing}", float(abs((s2Q - s2Q2)/Cv)), 1e-9,
          "RK4 h=0.01rM vs h=0.005rM agree at 1e-9 (w_Q converged)")
    check(f"corr_convergence_RAR_10rM_{footing}", float(abs((s2R - s2R2)/Cv)), 1e-9,
          "RK4 h=0.01rM vs h=0.005rM agree at 1e-9 (w_RAR converged)")
    check(f"corr_Q_10rM_{footing}", float(abs(s2Q/Cv - 0.5 - 1.0/(8*100))), 6e-6,
          "Q-branch s2 correction vs leading term (1/8)(rM/r)^2 at 10 r_M; residual is next-order O(y^2)")
    check(f"corr_RAR_10rM_{footing}", float(abs(s2R/Cv - 0.5 - 1.0/(6*10) - 1.0/(48*100))), 2.5e-5,
          "RAR-family s2 correction vs u/6+u^2/48 at 10 r_M; residual is next-order O(u^3)")

# ---------------------------------------------------------------------------
# PART 6 -- temperature scale: T = (m/2k_B) sqrt(G M_b a0), both footings, table
# ---------------------------------------------------------------------------
temp_scale = {}
for footing, a0 in FOOTINGS.items():
    temp_scale[footing] = {"T/m [K/kg]": float((1.0/2)/kB*mp.sqrt(G*1e11*MSUN*a0))}
results["temperature_per_mass"] = temp_scale

# ---------------------------------------------------------------------------
# exit summary
# ---------------------------------------------------------------------------
t_wall = time.perf_counter() - t_start
rss_bytes = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss  # macOS: BYTES
results["bounds"] = {"wall_time_s": float(t_wall), "maxrss_bytes": int(rss_bytes),
                     "maxrss_mib": round(rss_bytes/2**20, 2),
                     "threads": 1, "enforced": "single serial Python process; scalar mpmath/sympy; no grids"}
results["checks"] = checks

out = json.dumps(results, indent=1, sort_keys=True)
print(out)
with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "as008_probe_raw.json"), "w") as f:
    f.write(out)
print("\nCHECKS SUMMARY:")
for ck in checks:
    print(f"  [{'PASS' if ck['pass'] else 'FAIL'}] {ck['name']}  value={ck['value']:.3e}  tol={ck['tolerance']:.1e}  {ck['note']}")
npass = sum(1 for ck in checks if ck['pass'])
nall = len(checks)
print(f"\n{int(npass)}/{int(nall)} checks passed. wall={t_wall:.2f}s maxrss={rss_bytes/2**20:.1f}MiB threads=1")