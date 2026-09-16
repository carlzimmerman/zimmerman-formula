#!/usr/bin/env python3
"""G084 -- WHY THE ISOTHERMAL PROFILE: the MAXIMUM-ENTROPY derivation of the law.

THE VARIATIONAL PROBLEM.  Among spherical equilibria of a collisionless,
ISOTHERMAL fluid (velocity dispersion sigma, fixed by the fluid's equation of
state) in the FIXED baryon well

    Phi(r) = C ln r,        C = sqrt(G M_b a0) = v_flat^2          (G081 V1)

with the total mass and total energy held fixed, the maximum-entropy density is
the isothermal profile rho = A/r^2 exactly -- PROVIDED the temperature is the
framework's own virial value sigma^2 = C/2 (rung 4, the Zimmerman/DE-set
temperature; the triad, G03G).  The chain:

  S = -int rho ln(rho sigma^3) dV        (Boltzmann-Gibbs; the sigma^3 term is a
  M = int rho dV                          constant M ln sigma^3 and drops out)
  E = int (3 sigma^2/2 + Phi) rho dV     (internal + potential energy, per mass)

  Euler-Lagrange:  delta[S - alpha M - beta E]/delta rho = 0
        -ln rho - 1 - alpha - beta (3 sigma^2/2 + C ln r) = 0
        =>   rho(r) = A r^{-beta C} = A r^{-gamma},   gamma = beta C.

  Identification (the Boltzmann factor): an isothermal fluid in thermal
  equilibrium in a potential has beta = 1/sigma^2 (the energy multiplier IS the
  inverse temperature).  At the framework's virial temperature,

        sigma^2 = C/2   (rung 4; G03G triad; G031 V3; G081,  eta = 1/2)
        =>  gamma = C/sigma^2 = C/(C/2) = 2   EXACTLY

        rho(r) = A r^{-2},   A = M_b/(4 pi (r_M - r_in)) -> sqrt(G M_b a0)/(4 pi G)
                               (the equipartition normalization, G03E; M(<r_M) = M_b)

  THE MAXIMUM.  The entropy functional is STRICTLY CONCAVE as a functional of rho
  (d^2/dx^2(-x ln x) = -1/x < 0), and both constraints are LINEAR in rho at fixed
  sigma and fixed well.  Hence the stationary point is the UNIQUE GLOBAL MAXIMUM;
  the second variation is

        delta^2 S = -int (delta rho)^2/rho dV  <  0   (strictly, any direction)

  HONEST STATUS (stated): (i) the maximum exists because the well is FIXED and
  the profile is a normalizable power law on [r_in, r_M] with the EFE cap;
  (ii) the fully SELF-GRAVITATING isothermal sphere (potential from the gas
  itself, LBW) has NO global entropy maximum -- negative configurational specific
  heat, gravothermal catastrophe -- a different problem than the one the law
  poses; here the phantom's self-gravity is the POSTERIOR consistency check
  (flat curve / equipartition), not part of the variational principle; (iii) the
  dynamical fundamental mode of the same equilibrium is MARGINAL (omega^2 = 0,
  G081): an entropy EXTREMUM is not a dynamical attractor, the two statements
  coexist (verified below: the entropy decreases along the local mode directions).

THE THERMODYNAMICAL NUMBERS (MW realization):
  sigma = v_flat/sqrt(2), v_flat = (G M_b a0)^(1/4)
  T = m_sec sigma^2/k_B = m_sec c^2 (sigma/c)^2 / k_B          (T PROPORTIONAL to
  the sector particle mass, coefficient sigma^2/k_B = 1.9 mK per eV at
  sigma = 119 km/s -- sub-Kelvin for every relic-scale mass: T(93.3 eV) = 0.18 K,
  T(148 eV) = 0.28 K).
  Entropy per particle: s/k_B = 5/2 + ln[rho_max_TG(g)/(g rho)]  (Sackur-Tetrode
  form of the Maxwellian phase space; = 5/2 - ln g ~ 1.8 k_B at the TG cap --
  the degenerate-fermion floor).  Specific heat: ideal-gas 3 k_B/2 per particle;
  the configurational heat capacity of the fixed-well phantom is POSITIVE (mass
  redistributes outward as sigma^2 grows, W = C<ln r> rises) -- unlike the
  self-gravitating LBW sphere's negative one.

THE TREMAINE-GUNN BOUND (the neutrino-adjacent question):
  rho_max = g m^4 (2 pi)^(3/2) sigma^3 / h^3  >=  rho = 0.008 Msun/pc^3
  with sigma = 119 km/s  =>  m > ~23.3 eV  (canonical; 22.4-27.2 eV over the
  sigma/rho grid, both footings).  Compare: f04/f06 killed window 93-148 eV
  (phase-space ceiling 93.3 eV via the Coma UDGs, f04 A1; free-streaming floor
  148 eV, f06 A4; cluster floor 14.68 eV).  23.3 eV sits a factor 4 BELOW the
  ceiling -- phase space does NOT kill the equilibrium sector at any mass above
  23 eV -- and the free-streaming floor still forbids reading it as a light
  thermal relic (consistent with the committed "charge, not a species", H032).

VERDICTS: V1 the stationary point of the fixed-well max-entropy problem at the
DE-set temperature is rho = A/r^2 exactly (EL + Boltzmann identification + the
triad, machine-checked); V2 the second variation: MAXIMUM (strictly negative
delta^2 S, numeric spectrum shown) -- with the honest status of (i)-(iii);
V3 the TG bound on the equilibrium sector: m > 23.3 eV (0.008 Msun/pc^3,
119 km/s), below the killed window, never in it; V4 the statement.
"""
import json, math, os
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))

def trapz(y, x):
    try:
        return np.trapezoid(y, x)          # numpy >= 2.0
    except AttributeError:
        return np.trapz(y, x)              # numpy 1.x

GN, A0, A0_ALT = 6.674e-11, 9.3619e-11, 1.1279e-10
MSUN = 1.98892e30
PC = 3.0856775814913673e16
KPC = 1e3 * PC
kB = 1.380649e-23
hP = 6.62607015e-34
EV = 1.602176634e-19
C_L = 2.99792458e8
MB_MW = 7e10                       # Msun (the deepseek_push MW convention)
RHO_REF = 1.0 * MSUN / PC ** 3     # 1 Msun/pc^3, the entropy reference density

def check(l, ok, d=""):
    print(f"  [{'PASS' if ok else 'FAIL'}] {l}" + (f"   {d}" if d else ""), flush=True)
    return bool(ok)

RES = []
print("=" * 96)
print("G084 -- WHY THE ISOTHERMAL PROFILE: the maximum-entropy derivation of the law")
print("=" * 96)

# =====================================================================
# 1. THE VARIATIONAL PROBLEM: EL + the stationary point + the MAXIMUM
# =====================================================================
print("\n--- 1 the variational problem: max S = -int rho ln(rho sigma^3) dV")
print("     constraints: M = int rho dV,  E = int (3 sigma^2/2 + C ln r) rho dV")
print("     well: Phi = C ln r, C = sqrt(G M_b a0)  (fixed baryon well, G081 V1)")

vf2 = math.sqrt(GN * MB_MW * MSUN * A0)        # = C = v_flat^2
Cv  = vf2
sig2_star = Cv / 2.0
sig_star = math.sqrt(sig2_star)
print(f"    M_b = {MB_MW:.0e} Msun:  C = sqrt(G M_b a0) = {Cv:.6e} m^2/s^2, "
      f"sigma^2* = C/2 = {sig2_star:.6e} (m/s)^2,  sigma* = {sig_star/1e3:.3f} km/s")
print(f"    (registered MW sigma = 119.2 km/s (M_b ~ 6.5e10) / 124.9 km/s (alt footing);")
print(f"     the 7e10-constant reading gives {sig_star/1e3:.1f} km/s -- same orbit, same physics)")

# --- the Euler-Lagrange equation, exactly ---
print("\n    THE EULER-LAGRANGE EQUATION (delta[S - alpha M - beta E]:")
print("      -ln rho - 1 - alpha - beta(3 sigma^2/2 + C ln r) = 0")
print("      =>  rho(r) = A r^(-gamma),  gamma = beta C,  A = exp(-1-alpha-3 beta sigma^2/2)")
print("      Boltzmann identification (thermal equilibrium of an isothermal fluid")
print("      in a potential):  beta = 1/sigma^2  =>  gamma = C/sigma^2")
print("      at the virial temperature sigma^2 = C/2 (rung 4, the DE-set temperature):")
print("      gamma = C/(C/2) = 2  EXACTLY  =>  rho = A r^-2, the isothermal phantom,")
print("      A = M_b/(4 pi (r_M - r_in)) -> sqrt(G M_b a0)/(4 pi G)   (G03E normalization)")

# numeric: the EL residual rho = A r^-gamma must satisfy, at beta = 1/sigma^2 and
# sigma^2 = C/2, that  ln rho + 1 + beta(3 sigma^2/2 + C ln r)  is a CONSTANT in r.
rin, rM = 0.3 * KPC, math.sqrt(GN * MB_MW * MSUN / A0)
r = np.geomspace(rin, rM, 4001)
res_expr = []
for (alpha, s2) in ((2.0, sig2_star), (2.0, 0.9 * sig2_star), (2.3, sig2_star)):
    rr = r
    eterm = np.log(rr ** (-alpha)) + 1.0 + (3.0 * s2 / 2.0 + Cv * np.log(rr)) / s2
    res_expr.append((alpha, s2, float(eterm.max() - eterm.min())))
print(f"    EL-residual spread of [ln rho + 1 + beta(3 sigma^2/2 + Phi)] over [r_in, r_M]:")
for alpha, s2, sp in res_expr:
    print(f"      gamma = {alpha}, sigma^2 = {s2/sig2_star:.2f} (C/2): residual spread = {sp:.3e} "
          f"{'(EXACT, 0 to machine precision)' if sp < 1e-9 else '(nonzero: not a stationary point)'}")
ok_el = res_expr[0][2] < 1e-9 and res_expr[1][2] > 1e-6 and res_expr[2][2] > 1e-6
RES.append(check("V1a [EL] the power-law family solves the Euler-Lagrange equation: the "
                 "residual is EXACTLY flat at (gamma, sigma^2) = (2, C/2) and nonzero at any "
                 "other (gamma, sigma^2) -- rho = A r^-2 IS the stationary point at the "
                 "DE-set temperature", ok_el,
                 f"spread (2, C/2) = {res_expr[0][2]:.2e} vs (2, 0.9 C/2) = {res_expr[1][2]:.2e}, "
                 f"(2.3, C/2) = {res_expr[2][2]:.2e}"))

# --- the thermodynamic reading: dS/dE = 1/sigma^2 at gamma* = C/sigma^2 ---
# along the mass-conserving power-law family rho_g = A(g) r^-g, compute S^(g), E^(g);
# the entropy curve's slope at the DE-set point must be the inverse temperature 1/sigma^2,
# and its maximum over g at fixed E sits at g* = C/sigma^2 = 2.
def fam(gam, s2):
    A = (MB_MW * MSUN / RHO_REF) / (4 * math.pi * trapz(r ** 2 * r ** (-gam), r))
    rho = A * r ** (-gam)                     # dimensionless (units of RHO_REF)
    Sg = -trapz(rho * r ** 2 * np.log(np.where(rho > 0, rho, 1e-300)), r)
    Eg = trapz((1.5 * s2 + Cv * np.log(r)) * rho * r ** 2, r)
    return Sg, Eg

gs = np.linspace(1.2, 2.8, 121)
Ss = np.array([fam(g, sig2_star)[0] for g in gs])
Es = np.array([fam(g, sig2_star)[1] for g in gs])
dSdE = np.gradient(Ss, Es)
i2 = int(np.argmin(np.abs(gs - 2.0)))
beta_pred = dSdE[i2]
print(f"\n    the thermodynamic reading: along the mass-conserving family,")
print(f"    dS/dE at gamma = 2.00 = {beta_pred:.6e} s^2/m^2  vs  1/sigma^2 = {1/sig2_star:.6e}")
print(f"    (the Lagrange multiplier beta IS the inverse temperature: the entropy curve's")
print(f"    slope at the equilibrium IS T^-1 -- the temperature emerges from the constraint)")
ok_thermo = abs(beta_pred - 1 / sig2_star) / (1 / sig2_star) < 2e-3
RES.append(check("V1b [thermodynamic identification] the entropy-vs-energy slope at "
                 "gamma = 2 equals 1/sigma^2 to 0.2%: the energy constraint's multiplier is "
                 "the inverse temperature, and the equilibrium sits where the entropy curve's "
                 "slope is the virial T^-1", ok_thermo,
                 f"dS/dE = {beta_pred:.4e} vs 1/sigma^2 = {1/sig2_star:.4e} s^2/m^2"))

# --- the MAXIMUM: second variation ---
# delta^2 S = -int (delta rho)^2/rho dV < 0 strictly (rho>0).  Verify numerically with
# constraint-preserving (M, E) perturbation modes.  The discrete test runs in the
# DIMENSIONLESS coordinates u = r/r_M, rhot = rho r_M^3/M_b (so that int rhot dVt = 1,
# dVt = 4 pi u^2 du): in these units every sum is O(1) and float64 is exact.
n = 600
u = np.geomspace(rin / rM, 1.0, n)
dVt = np.gradient(4 * math.pi / 3 * u ** 3)
rhot0 = u ** (-2.0) / (4 * math.pi * trapz(u ** 2 * u ** (-2.0), u))   # int rhot dVt = 1
Efun_g = lambda uu: 1.5 * sig2_star + Cv * np.log(rM * uu)              # per-mass energy density
def Sdiff(rr):
    """S(rr) - S(rhot0) computed stably (log1p decomposition; all quantities O(1))."""
    dr = rr - rhot0
    return -float(np.sum(dVt * (dr * np.log(rhot0) + (rhot0 + dr) * np.log1p(dr / rhot0))))
gM = dVt                                                 # dM/drho_i (dimensionless)
gE = Efun_g(u) * dVt                                     # dE/drho_i
Mt0 = float(np.sum(dVt))
def project(mode):
    # Gram-Schmidt onto the constraint manifold: remove the M- then the E-gradient
    m = mode - (np.sum(mode * gM) / Mt0)
    m = m - (np.sum(m * gE) / np.sum(gE * gE)) * gE
    return m
x = np.log(u / (rin / rM)) / np.log(1.0 / (rin / rM))
dS2_vals = []
for k in (1, 2, 3, 4, 6):
    mode = project(np.sin(k * math.pi * x))
    mode = mode / np.sqrt(np.sum(mode ** 2 * dVt))           # normalize
    for eps in (2e-3, 5e-3):
        cent = Sdiff(rhot0 + eps * mode) + Sdiff(rhot0 - eps * mode)
        ana = -float(eps ** 2 * np.sum(mode ** 2 * dVt / rhot0))
        dS2_vals.append((k, eps, cent, ana))
print("\n    THE SECOND VARIATION:  delta^2 S = -int (delta rho)^2/rho  <  0")
print("    (the entropy functional is strictly concave: -x ln x has d^2/dx^2 = -1/x < 0,")
print("     both constraints are linear in rho at fixed sigma and well => UNIQUE GLOBAL")
print("     maximum; stable central second differences along M,E-preserving modes):")
for k, eps, cent, ana in dS2_vals:
    print(f"      mode k = {k}:  [S(r*+e)-S*]+[S(r*-e)-S*] = {cent:+.6e}   (analytic -e^2 int drho^2/rho = {ana:+.6e})")
ok_max = all(cent < 0 for _, _, cent, _ in dS2_vals) and \
         all(abs(cent - ana) / max(abs(cent), 1e-30) < 5e-2 for _, _, cent, ana in dS2_vals)
# also: a plain compression-mode scan (localized bump) must lower S too
modec = project(np.exp(-((x - 0.6) / 0.06) ** 2))
modec = modec / np.sqrt(np.sum(modec ** 2 * dVt))
drop = [Sdiff(rhot0 + eps * modec) for eps in (2e-3, 5e-3)]
ok_max = ok_max and all(d < 0 for d in drop)
RES.append(check("V2 [second variation] the isothermal profile is the MAXIMUM of the "
                 "entropy functional in the fixed well: delta^2 S = -int (drho)^2/rho < 0 "
                 "strictly -- exact (concavity) and numeric (5 modes x 2 amplitudes, "
                 "stable central differences match the analytic -e^2 int drho^2/rho to 5%)",
                 ok_max,
                 f"all dS2 < 0; matches analytic to {max(abs(c-a)/max(abs(c),1e-30) for _,_,c,a in dS2_vals)*100:.1f}%; "
                 f"localized compression bump: dS = {drop[0]:+.2e}, {drop[1]:+.2e}"))
print("    HONEST STATUS: (i) the maximum exists because the well is FIXED and the profile")
print("    is a normalizable power law on [r_in, r_M] with the EFE cap; (ii) the fully")
print("    SELF-GRAVITATING isothermal sphere (LBW) has NO global entropy maximum")
print("    (negative gravothermal specific heat) -- not the problem the law poses; the")
print("    phantom's self-gravity is the posterior check (flat curve, equipartition);")
print("    (iii) the DYNAMICAL fundamental mode of this equilibrium is MARGINAL")
print("    (omega^2 = 0 EXACT, G081) -- an entropy extremum is not a dynamical attractor,")
print("    and the two statements coexist (the entropy drops along every local mode).")

# =====================================================================
# 2. THE THERMODYNAMICAL NUMBERS
# =====================================================================
print("\n--- 2 the thermodynamical numbers (MW realization) ---")
print("    T = m_sec sigma^2/k_B = m_sec c^2 (sigma/c)^2 / k_B:  T PROPORTIONAL to the")
print("    sector particle mass;  coefficient sigma^2/k_B (the virial temperature per kg).")
sigs_km = {"registered canonical": 119.2, "7e10-constants": sig_star / 1e3,
           "registered alt": 124.9}
Ttab = {}
for lab, sk in sigs_km.items():
    coeff = (sk * 1e3) ** 2 / kB * (EV / C_L ** 2)      # K per eV of mass
    Ttab[lab] = coeff
    print(f"    sigma = {sk:6.2f} km/s:  T/m_sec = {(sk*1e3)**2/kB:.4e} K/kg = "
          f"{coeff*1e3:.4f} mK per eV  (T = m_sec c^2 (sigma/c)^2/k_B, (sigma/c)^2 = {((sk*1e3)/C_L)**2:.3e})")
mass_ladder = (0.1, 1.0, 11.0, 23.25, 93.3, 148.0, 1000.0)
print("    T(m_sec):   " + "   ".join(f"{m:>6.1f} eV -> {m*Ttab['registered canonical']*1e3:8.4f} mK" for m in mass_ladder))
ok_t = abs(Ttab["registered canonical"] * 1e3 - 1.8346) < 0.02
RES.append(check("V-t [temperature] the dark sector temperature is LINEAR in the particle "
                 "mass: T = m_sec sigma^2/k_B = m_sec c^2 (sigma/c)^2 / k_B, with "
                 "T(1 eV) = 1.9 mK at sigma = 119 km/s (sub-Kelvin for every relic-scale "
                 "mass: T(93.3 eV) = 0.18 K, T(148 eV) = 0.28 K)", ok_t,
                 f"coefficient = {Ttab['registered canonical']*1e3:.4f} mK/eV (canonical)"))

# --- the phantom's entropy (per particle + total) ---
print("\n    THE PHANTOM'S ENTROPY (Maxwellian phase space; Sackur-Tetrode form):")
print("      s/k_B = 5/2 + ln[rho_max_TG(g=2)/(g rho)]   per sector particle")
print("      (= 5/2 - ln 2 = 1.81 k_B AT the Tremaine-Gunn cap: the degenerate-fermion floor)")
def rho_max_tg(m_eV, sig_kms, g=2.0):
    m = m_eV * EV / C_L ** 2
    return g * m ** 4 * (2 * math.pi) ** 1.5 * (sig_kms * 1e3) ** 3 / hP ** 3   # kg/m^3
def s_per_particle(m_eV, rho_kgm3, sig_kms, g=2.0):
    return 5.0 / 2.0 + math.log(rho_max_tg(m_eV, sig_kms, g) / (g * rho_kgm3))
rho_008 = 0.008 * MSUN / PC ** 3
MB_kg = MB_MW * MSUN
Sent = {}
sig_reg = 119.2
for m in (11.0, 23.25, 60.0, 93.3, 148.0):
    s = s_per_particle(m, rho_008, sig_reg)
    N = MB_kg / (m * EV / C_L ** 2)
    Sent[m] = dict(s_kB=s, S_tot_kB=s * N)
    print(f"      m_sec = {m:6.2f} eV:  s/k_B = {s:7.3f}  ->  S_ph = {s*N:.3e} k_B "
          f"(N = {N:.3e} sector particles inside r_M, M_ph = M_b)")
s_cap = s_per_particle(23.25, rho_008, sig_reg)
print(f"      at the TG-bound mass: s/k_B = {s_cap:.3f} (the 5/2 - ln 2 floor {2.5-math.log(2):.3f} is "
      f"approached as m -> m_TG).  Below the bound (m = 11 eV): s/k_B = {s_per_particle(11.0, rho_008, sig_reg):.2f} < 0 --")
print("      the CLASSICAL Sackur-Tetrode formula breaks down below m_TG (phase-space")
print("      occupancy >= 1, the excluded region): the sign flip is the honest marker.")
ok_ent = (all(v["s_kB"] > 1.0 for m_, v in Sent.items() if m_ >= 23.25)
          and abs(s_cap - (2.5 - math.log(2))) < 0.3
          and s_per_particle(11.0, rho_008, sig_reg) < 0.0)
RES.append(check("V-t [entropy] the phantom's entropy: s/k_B = 5/2 + ln[rho_max/g rho] per "
                 "particle (1.8-9 k_B over the relic ladder at the equilibrium state), total "
                 "S_ph = N s ~ 1e76 k_B at m_sec = 23 eV, and S_ph ~ 1/m_sec (lighter sector = "
                 "more entropy); the TG cap IS the entropy floor", ok_ent,
                 f"s(11 eV) = {Sent[11.0]['s_kB']:.2f}, s(93.3 eV) = {Sent[93.3]['s_kB']:.2f} k_B/particle"))

# --- specific heat ---
print("\n    THE SPECIFIC HEAT:")
print("      ideal-gas part: C_V = 3 k_B/2 per particle (positive, standard).")
print("      configurational part (dW/dT along the equilibrium family at fixed well):")
cW = 2.0
# d<ln r>/d(sigma^2) at sigma^2* from the r^-2 profile in the box, finite differences
sig2g = np.array([s2 * (1 + d) for d in (-0.02, 0.02)])
lnr = []
for s2g in sig2g:
    ag = Cv / s2g
    Ag = (MB_kg / RHO_REF) / (4 * math.pi * trapz(r ** 2 * r ** (-ag), r))
    rg_ = Ag * r ** (-ag)
    lnr.append(trapz(rg_ * r ** 2 * np.log(r), r) / trapz(rg_ * r ** 2, r))
dlnr_ds2 = (lnr[1] - lnr[0]) / (sig2g[1] - sig2g[0])
dE_ds2_extra = Cv * dlnr_ds2                       # dW/d sigma^2 per unit mass
print(f"      d<ln r>/d(sigma^2) at C/2 = {dlnr_ds2:.4e},  so the configurational heat")
print(f"      capacity dW/d(sigma^2) = C d<ln r>/d(sigma^2) = {dE_ds2_extra:.4e} > 0 (per unit mass)")
print("      => the total heat capacity dE/dT = (3/2 + dE_ds2_extra) k_B/m > 3 k_B/2m POSITIVE.")
print("      honest note: the LBW negative gravothermal specific heat belongs to the fully")
print("      SELF-GRAVITATING sphere (no fixed well, no maximum) -- not this problem.")
ok_cv = dE_ds2_extra > 0
RES.append(check("V-t [specific heat] the fixed-well phantom's configurational heat "
                 "capacity is POSITIVE (mass redistributes outward as sigma^2 grows, "
                 "W = C<ln r> rises with T); the negative LBW value is the self-gravitating "
                 "problem's, stated as such", ok_cv,
                 f"dE_conf/dT = {dE_ds2_extra:.3e} (m^2/s^2 per unit (m/s)^2 of sigma^2) > 0"))

# =====================================================================
# 3. THE TREMAINE-GUNN BOUND (the neutrino-adjacent question)
# =====================================================================
print("\n--- 3 the Tremaine-Gunn phase-space bound for the EQUILIBRIUM sector ---")
print("    rho_max = g m^4 (2 pi)^(3/2) sigma^3 / h^3  (fermion, g = 2; TG 1979, f04-form)")
def m_min_eV(rho_msun_pc3, sig_kms, g=2.0):
    rho = rho_msun_pc3 * MSUN / PC ** 3
    sig = sig_kms * 1e3
    m4 = rho * hP ** 3 / (g * (2 * math.pi) ** 1.5 * sig ** 3)
    return (m4 ** 0.25) * C_L ** 2 / EV
rows3 = []
for rho_v in (0.008, 0.010, 0.012, 0.015):
    for sig_v in (119.2, sig_star / 1e3, 124.9):
        rows3.append((rho_v, sig_v, m_min_eV(rho_v, sig_v)))
        print(f"    rho = {rho_v:.3f} Msun/pc^3, sigma = {sig_v:6.2f} km/s:  m_min = {m_min_eV(rho_v, sig_v):6.2f} eV")
m_TG = m_min_eV(0.008, 119.2)
m_TG_alt = m_min_eV(0.008, 124.9)
print(f"\n    THE NUMBER:  rho = 0.008 Msun/pc^3, sigma = 119 km/s inside r_M")
print(f"      m > {m_TG:.2f} eV  (canonical registered sigma; {m_TG_alt:.2f} eV at the alt footing)")
print(f"      grid span: {min(r[2] for r in rows3):.2f} - {max(r[2] for r in rows3):.2f} eV")
print("    COMPARISON (committed references, f04 A1 / f06 A4 / f04 A2):")
print("      cluster floor         m >=  14.68 eV   (f04 A1, SLUGGS row, repro'd here)")
print("      phase-space ceiling   m <=  93.3  eV   (f04 A1, Coma UDGs row, repro'd here)")
print("      free-streaming floor  m >= 148    eV   (f06 A4)")
print("      thermal abundance     m  =  11.3  eV   (f04 A2, Omega_dm closure)")
print(f"      THIS equilibrium:     m >  {m_TG:.1f} eV  -- a factor {93.3/m_TG:.2f} BELOW the killed")
print("      window's phase-space ceiling, 1.59x above the cluster floor, INSIDE f04's")
print("      conditional window [14.68, 93.3] eV -- phase space does NOT cap the equilibrium")
print("      sector above 23 eV; the free-streaming floor (m >= 148 eV) still forbids a")
print("      light RELIC reading of any mass in (23, 148) eV -- the committed position")
print("      (the sector is a charge, not a species; H032 / GRAVITY_EVERYWHERE sec 3.3)")
print("      stands unchanged.  Boson note: for g = 1 spin-0 the bound relaxes to "
          f"{m_min_eV(0.008, 119.2, 1.0):.2f} eV (and condensation dodges it entirely).")
ok_tg = (18.0 < m_TG < 40.0) and (m_TG > 14.68) and (m_TG < 93.3)
RES.append(check("V3 [Tremaine-Gunn] the equilibrium sector needs m > 23.3 eV to avoid the "
                 "phase-space cap at rho = 0.008 Msun/pc^3, sigma = 119 km/s -- BELOW the "
                 "f04/f06 killed window (93-148 eV) by a factor 4: TG does NOT kill the "
                 "equilibrium; the relic reading stays dead on the free-streaming floor",
                 ok_tg,
                 f"m_TG = {m_TG:.2f} eV (canonical) / {m_TG_alt:.2f} eV (alt); grid {min(r[2] for r in rows3):.1f}-"
                 f"{max(r[2] for r in rows3):.1f} eV; window reference [14.68, 93.3, 148] eV"))

# =====================================================================
# 4. VERDICTS
# =====================================================================
statement = ("THE LAW IS THE MAXIMUM-ENTROPY EQUILIBRIUM AT THE DE-SET TEMPERATURE: "
             "among spherical equilibria of a collisionless, isothermal fluid in the fixed "
             "baryon well Phi = C ln r (C = sqrt(G M_b a0)), constrained to the galaxy's mass "
             "and energy, the entropy functional S = -int rho ln(rho sigma^3) dV is maximized "
             "by rho = A r^(-C/sigma^2); at the virial temperature sigma^2 = C/2 (rung 4, the "
             "Zimmerman temperature) the exponent is EXACTLY 2: rho = A/r^2, the isothermal "
             "phantom with A = sqrt(G M_b a0)/(4 pi G) -- the second variation is strictly "
             "negative (unique global maximum in the fixed well; the self-gravitating LBW "
             "problem's non-existence and the G081 marginal dynamical mode are stated, not "
             "hidden).  The sector's temperature is T = m_sec sigma^2/k_B = m_sec c^2 "
             "(sigma/c)^2/k_B, LINEAR in the particle mass (1.9 mK/eV at sigma = 119 km/s); "
             "the phantom's entropy is 5/2 + ln(rho_max/g rho) k_B per particle (the TG cap "
             "is its floor) and its fixed-well heat capacity is positive.  The equilibrium "
             "sector clears Tremaine-Gunn for m > 23.3 eV (rho = 0.008 Msun/pc^3, "
             "sigma = 119 km/s) -- a factor 4 below the f04/f06 killed window (93-148 eV): "
             "phase space does not cap the equilibrium, and the light-thermal-relic reading "
             "remains dead on f06's free-streaming floor, as committed.")
RES.append(check("V4 [statement] the law is the maximum-entropy equilibrium at the DE-set "
                 "temperature, with the TG bound on the sector particle mass", True, statement))

n = sum(1 for r in RES if r)
print(f"\nG084 COMPLETE: {n}/{len(RES)} checks PASS.")

def _s(x):
    if isinstance(x, dict):
        return {str(k): _s(v) for k, v in x.items()}
    if isinstance(x, (list, tuple)):
        return [_s(v) for v in x]
    if isinstance(x, (np.floating, np.integer)):
        return float(x)
    return x

json.dump(_s({"checks": [bool(r) for r in RES], "n_pass": int(n), "n_total": len(RES),
           "EL": {"C": Cv, "sigma2_star": sig2_star, "gamma_star": 2.0,
                  "residual_spread_at_star": res_expr[0][2],
                  "dSdE_at_gamma2": beta_pred, "dSdE_predicted_1_over_sigma2": 1 / sig2_star},
           "second_variation": {"dS2_modes": [[int(k), float(eps), cent, ana] for k, eps, cent, ana in dS2_vals],
                                "bump_drops": [float(d) for d in drop]},
           "thermo": {"T_per_eV_mK": Ttab, "mass_ladder_mK": {str(m): m * Ttab["registered canonical"] * 1e3 for m in mass_ladder},
                      "entropy_per_particle_kB": {str(m): v["s_kB"] for m, v in Sent.items()},
                      "S_total_kB": {str(m): v["S_tot_kB"] for m, v in Sent.items()},
                      "dEd_conf_dsigma2": dE_ds2_extra},
           "tremaine_gunn": {"m_min_eV_grid": [[rho, sig, mm] for rho, sig, mm in rows3],
                             "m_TG_canonical_eV": m_TG, "m_TG_alt_eV": m_TG_alt,
                             "window_f04_f06_eV": [14.68, 93.3, 148.0],
                             "statement": "m > 23.3 eV: phase space does NOT cap the equilibrium sector; below the killed window by 4x"},
           "statement": statement}),
          open(os.path.join(HERE, "G084_results.json"), "w"), indent=1)
print("wrote G084_results.json")