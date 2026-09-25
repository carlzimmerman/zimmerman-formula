#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
BSX3 -- WHY NO KINETIC FUNCTION REPAIRS THE KHRONON-DUST AETHER, AND THE PHANTOM'S MASS BUDGET.
(1) For ANY K(Q), the static mass term a galaxy feels and the late cosmological Jeans scale of the khronon are the
same scale: mu_eff^2 = k_J,phys^2 (1 + c_ad^2), exactly.  KiDS's external-field bound needs a short Jeans length,
MOND-like lensing to ~1 Mpc needs a long mass-term range; the identity makes them one number, so the BSX1 pincer
holds for every K.  (2) BSX2's cubic 'repair' (PAPER33 v1) is withdrawn: at the parameters that passed cosmology its
K-sector density in a galaxy exceeds the MOND phantom by ~1e7 and its mass-term range is a few kpc.  (3) The mass-
budget gate the phantom-as-conserved-fluid picture owes: where does the deep-MOND phantom of a KiDS lens exhaust
the dark fluid it can have assembled?

(1) THE IDENTITY (symbolic, general K).  BS24's khronon on FRW: 8 pi G rho = Q K_Q - K, 8 pi G P = K (their eqs. 44,
54, 57), so c_ad^2 = dP/drho = K_Q/(Q K_QQ) and the Jeans wavenumber of their eq. 71 is
    k_J,phys^2 = 4 pi G rho (1 + w)/c_ad^2 = (1/2) Q^2 K_QQ .
In a static region Q = Q_bar (1 - Xi/c^2) (their eq. 18a with the cosmic Q_bar), and the K part of the 00 equation,
-(c^2/2) delta(Q K_Q), linearises to mu_eff^2 Xi with
    mu_eff^2 = (1/2) Q (K_Q + Q K_QQ)  =>  mu_eff^2 / k_J,phys^2 = 1 + K_Q/(Q K_QQ) = 1 + c_ad^2 .
BS24's quadratic K reproduces their eq. 25 (mu^2 Xi) and their k_J = a mu.  The identity is exact.

(2) THE CUBIC REPAIR AT ITS OWN PARAMETERS.  K = (2M^2/3)(Q-1)^3 at the M^2 that BSX2 found passing cosmology (late
Jeans length 0.3-3 kpc): the linear mass-term range 1/mu_eff equals that Jeans length, so r_C = (r_M/mu_eff^2)^(1/3)
is a few kpc; and the nonlinear K density M^2 Xi^2/(4 pi G c^2) at galactic potentials dwarfs the MOND phantom.
BSX2's X1 (the cubic term is "1PN") was a formal c -> infinity limit at fixed M^2 and does not hold at M^2 ~ 1e17
Mpc^-2.

(3) THE MASS BUDGET.  A conserved phantom (BSK1 M2) must be assembled from dark fluid that fell in.  The deep-MOND
phantom inside r is M_ph(<r) = (r/r_M - 1) M_b.  Two budgets for a lens of baryonic mass M_b:
  (a) generous: the LCDM halo mass M_200 of its stellar mass (Moster, Naab & White 2013 SHMR at z = 0.25), i.e. the
      dark fluid falls in as CDM does; (b) tight: the galaxy's own cosmic share (Omega_dm/Omega_b) M_b.
  The budget radius is where M_ph(<r) reaches the budget.  KiDS-1000 isolated lenses (Brouwer+2021) are clean to
  R = 0.3 Mpc and measured to 3 Mpc.

CONTROLS
  I1 is checked on BS24's quadratic K (mu_eff = mu, k_J = a mu) and on the cubic K against BSX2's committed Jeans
  lengths.  MUTATE=1 replaces BS24's static identification Q = Q_bar(1 - Xi/c^2) by Q = 1 - Xi/c^2 (dropping the
  cosmic background, as a formal PN count does): the identity then fails for the cubic K (its linear term vanishes),
  which is exactly BSX2's X1 slip -- I1 and I2 must FAIL (rc = 1).  MUTATE outputs go to separate files.

Run from the repository root:  python3 real_research/bs_khronon_2026/BSX3_jeans_mass_identity_and_budget.py
"""
import os, sys, json, math
import numpy as np
import sympy as sp
from scipy.optimize import brentq

HERE = os.path.dirname(os.path.abspath(__file__))
MUTATE = os.environ.get("MUTATE", "0") == "1"
LANE = "BSX3"
SLUG = "BSX3_jeans_mass_identity_and_budget"
P = lambda *a: print(*a, flush=True)
CH, OUT = [], {"lane": LANE, "mutate": MUTATE, "checks": {}, "numbers": {}}


def check(name, measured, ok, reading="", load_bearing=True):
    ok = bool(ok)
    CH.append((name, ok, load_bearing))
    OUT["checks"][name] = {"ok": ok, "measured": str(measured), "load_bearing": load_bearing}
    P(f"  [{'PASS' if ok else 'FAIL'}] {name}")
    P(f"         measured: {measured}")
    if reading:
        P(f"         reading:  {reading}")
    return ok


def banner(t):
    P("\n" + "=" * 110); P(t); P("=" * 110)


P(__doc__.split("CONTROLS")[0].strip())
if MUTATE:
    P("\n  *** MUTATE=1: static Q = 1 - Xi/c^2 (cosmic background dropped); I1 and I2 must FAIL ***")

# ============================================================================================ I1
banner("I1  THE IDENTITY: mu_eff^2 = k_J,phys^2 (1 + c_ad^2) for ANY K(Q)")
Q, Qb, cc, Xi = sp.symbols('Q Qbar c Xi', positive=True)
Kf = sp.Function('K')
KQ = sp.diff(Kf(Q), Q); KQQ = sp.diff(Kf(Q), Q, 2)
rho8 = Q * KQ - Kf(Q); p8 = Kf(Q)
cad2 = sp.simplify(sp.diff(p8, Q) / sp.diff(rho8, Q))
kJ2 = sp.simplify(sp.Rational(1, 2) * (rho8 + p8) / cad2)                        # 4 pi G rho (1+w)/c_ad^2 (8piG units)
Q_static = (1 - Xi / cc**2) if MUTATE else Qb * (1 - Xi / cc**2)             # BS24 eq. 18a, with the cosmic Q_bar
QK = lambda q: q * sp.diff(Kf(q), q)
# linear coefficient of -(c^2/2) delta(Q K_Q) in Xi, about Xi = 0
QKexpr = (Q * KQ).subs(Q, Q_static).doit()
mu_eff2 = sp.simplify(sp.diff(-(cc**2 / 2) * QKexpr, Xi).subs(Xi, 0))
mu_eff2_Qb = mu_eff2 if MUTATE else mu_eff2
ratio = sp.simplify(mu_eff2 / kJ2.subs(Q, Qb)) if not MUTATE else sp.simplify(mu_eff2 / kJ2.subs(Q, 1))
P(f"    c_ad^2 = {cad2};   k_J,phys^2 = {kJ2}")
P(f"    static mass term mu_eff^2 = {mu_eff2}")
P(f"    mu_eff^2 / k_J^2 = {ratio}")
target = 1 + cad2.subs(Q, Qb)
ident_ok = sp.simplify(ratio - target) == 0
# controls: BS24's quadratic K (mu_eff -> mu, k_J -> mu as Q_bar -> 1) and the cubic (mu_eff^2 = 2 M^2 q at Q_bar = 1 + q)
mu2s, M2s, q = sp.symbols('mu2 M2 q', positive=True)
quadK = mu2s * (Q - 1)**2; cubK = sp.Rational(2, 3) * M2s * (Q - 1)**3
def mu_eff_of(Kexpr):
    Qs_ = (1 - Xi / cc**2) if MUTATE else (1 + q) * (1 - Xi / cc**2)
    return sp.simplify(sp.diff(-(cc**2 / 2) * (Q * sp.diff(Kexpr, Q)).subs(Q, Qs_), Xi).subs(Xi, 0))
def kJ_of(Kexpr, Qv):
    r8 = Q * sp.diff(Kexpr, Q) - Kexpr; ca = sp.diff(Kexpr, Q) / sp.diff(r8, Q)
    return sp.simplify((sp.Rational(1, 2) * (r8 + Kexpr) / ca).subs(Q, Qv))
quad_mu = sp.limit(mu_eff_of(quadK), q, 0); quad_kJ = sp.limit(kJ_of(quadK, 1 + q), q, 0)
cub_mu = mu_eff_of(cubK); cub_kJ = kJ_of(cubK, 1 + q)
P(f"    quadratic K (BS24): mu_eff^2 -> {quad_mu},  k_J^2 -> {quad_kJ}   (their eq. 25's mu^2 and k_J = a mu)")
P(f"    cubic K:           mu_eff^2 = {sp.factor(cub_mu)},  k_J^2 = {sp.factor(cub_kJ)}")
cub_ratio = sp.simplify(cub_mu / cub_kJ) if cub_kJ != 0 else sp.oo
ctrl_ok = sp.simplify(quad_mu - mu2s) == 0 and sp.simplify(quad_kJ - mu2s) == 0 and sp.limit(cub_ratio, q, 0) == 1
OUT["numbers"]["I1"] = {"cad2": str(cad2), "kJ2": str(kJ2), "mu_eff2": str(mu_eff2), "ratio": str(ratio),
                        "quadratic": [str(quad_mu), str(quad_kJ)], "cubic": [str(cub_mu), str(cub_kJ)]}
check("I1 for any K(Q): the static mass term a galaxy feels equals the late Jeans scale of the khronon, "
      "mu_eff^2 = k_J,phys^2 (1 + c_ad^2) exactly (checked on BS24's quadratic K and on the cubic K)",
      f"mu_eff^2/k_J^2 = {ratio}; quadratic -> (mu^2, mu^2); cubic ratio -> {sp.limit(cub_ratio, q, 0)} as q -> 0",
      ident_ok and ctrl_ok,
      "the same second derivative K_QQ at the cosmic background sets both; no choice of K separates them")

# ============================================================================================ I2
banner("I2  BSX2's CUBIC 'REPAIR' AT ITS OWN PASSING PARAMETERS: MOND ends at a few kpc; the K density dwarfs the phantom")
G = 6.67430e-11; c = 2.99792458e8; MSUN = 1.989e30; KPC = 3.0856775814913673e19; MPC = KPC * 1e3
A0 = {"canonical": 9.3619e-11, "alt": 1.1279e-10}
bsx2 = json.load(open(os.path.join(HERE, "BSX2_cubic_one_scale_khronon_results.json")))
rows = bsx2["numbers"]["X2"]["rows"]
h = 0.6736; om_c = 0.1200; Oc = om_c / h**2; HC = h / 2997.92458
MB = 6e10 * MSUN; vf = (G * MB * A0["canonical"])**0.25
i2 = {}
for key in ("0.0003", "0.001", "0.003"):
    r = rows[key]; M2_mpc = 10**r["log10_M2_per_Mpc2"]; M2 = M2_mpc / MPC**2          # 1/m^2
    target = 3 * HC**2 * Oc
    I0 = brentq(lambda I: I * (1 + (2 / 3) * (I / (2 * M2_mpc))**0.5) - target, 1e-9 * target, target)
    q0 = (I0 / (2 * M2_mpc))**0.5
    mu_eff2 = float(sp.N(cub_mu.subs({M2s: M2, q: q0}))) if not MUTATE else 0.0
    lam_eff_kpc = (1 / math.sqrt(mu_eff2)) / KPC if mu_eff2 > 0 else float("inf")
    r_M = math.sqrt(G * MB / A0["canonical"])
    r_C_kpc = ((r_M / mu_eff2)**(1 / 3)) / KPC if mu_eff2 > 0 else float("inf")
    # nonlinear K density at galactic potentials vs the deep-MOND phantom density, r = 10 / 30 / 100 kpc
    dens = {}
    for rk in (10, 30, 100):
        rr = rk * KPC; phi = vf**2 * (1 + math.log(1000 / rk))                          # |phi|, MOND log potential out to 1 Mpc
        rhoK = M2 * c**2 * (phi / c**2)**2 / (4 * math.pi * G)                          # M^2 Xi^2/(4 pi G c^2)
        rho_ph = vf**2 / (4 * math.pi * G * rr**2)
        dens[rk] = rhoK / rho_ph
    i2[key] = {"lambda_J0_kpc": float(key) * 1e3, "q0": q0, "mu_eff_inv_kpc": lam_eff_kpc, "r_C_MW_kpc": r_C_kpc,
               "rhoK_over_rho_ph_at_10_30_100kpc": {k_: f"{v:.2e}" for k_, v in dens.items()}}
    P(f"    lambda_J,0 = {float(key)*1e3:4g} kpc: q0 = {q0:.2e};  1/mu_eff = {lam_eff_kpc:.3g} kpc;  r_C(MW) = {r_C_kpc:.3g} kpc;  "
      f"K density / MOND phantom at 10/30/100 kpc = " + " / ".join(f"{v:.1e}" for v in dens.values()))
OUT["numbers"]["I2"] = i2
worst_rC = max(v["r_C_MW_kpc"] for v in i2.values())
min_ratio = min(float(v["rhoK_over_rho_ph_at_10_30_100kpc"][10]) for v in i2.values())
check("I2 at every late Jeans length that BSX2 found passing cosmology (0.3-3 kpc), the cubic khronon's galactic "
      "mass-term range is that Jeans length, MOND ends inside ~10 kpc, and its K density at 10 kpc exceeds the MOND "
      "phantom by >= 1e6: BSX2's repair (PAPER33 v1) is withdrawn",
      f"max r_C(MW) = {worst_rC:.3g} kpc; min K/phantom density at 10 kpc = {min_ratio:.2e}",
      worst_rC < 10 and min_ratio > 1e6,
      "BSX2 X1's 'the cubic term is 1PN' is a c -> infinity limit at fixed M^2; the passing M^2 (~1e15-1e17 Mpc^-2) "
      "is not O(c^0), so the term is not negligible -- a formal PN count must be evaluated at the parameters used")

# ============================================================================================ I3
banner("I3  THE PINCER FOR EVERY K: KiDS's field bound needs k_J large, MOND to ~1 Mpc needs mu_eff small")
P("    BSX1 (their filter k^2/(k^2 + k_J^2), CDM-like khronon spectrum on large scales): the KiDS external-field bound")
P("    needs 1/k_J,phys <~ 0.22 Mpc at z = 0.25.  BS24's eq. 38: r_C = (r_M/mu_eff^2)^(1/3) >= 1 Mpc for a Milky-Way")
P("    lens needs 1/mu_eff >= (1 Mpc^3/r_M)^(1/2).  With mu_eff = k_J (1 + c_ad^2)^(1/2), c_ad^2 << 1 today:")
r_M_mpc = math.sqrt(G * MB / A0["canonical"]) / MPC
need_mu_inv = math.sqrt(1.0 / r_M_mpc)
efe_max = 0.223
P(f"    MOND to 1 Mpc: 1/mu_eff >= {need_mu_inv:.1f} Mpc;  KiDS field bound: 1/k_J <= {efe_max} Mpc  -> gap x{need_mu_inv/efe_max:.0f}")
OUT["numbers"]["I3"] = {"need_mu_inv_Mpc": need_mu_inv, "efe_max_Mpc": efe_max}
check("I3 (the pincer for every K) the scale KiDS's field bound needs (<= 0.22 Mpc) and the scale MOND-like lensing to "
      "1 Mpc needs (>= ~10 Mpc) differ by a factor ~40 and are, by I1, the same scale",
      f"1/mu_eff >= {need_mu_inv:.1f} Mpc vs 1/k_J <= {efe_max} Mpc", need_mu_inv / efe_max > 10,
      "r_C is BS24's order-of-magnitude eq. 38 and the field bound is linear theory; the factor ~40 gap is what "
      "makes the statement robust to those approximations", load_bearing=False)

# ============================================================================================ B
banner("B  THE MASS BUDGET: where the deep-MOND phantom of a KiDS lens exhausts the dark fluid it can have assembled")
def moster_Mstar(Mh, z):                                         # Moster, Naab & White 2013, eqs. 2 and 11-14
    zz = z / (1 + z)
    M1 = 10**(11.590 + 1.195 * zz); N = 0.0351 - 0.0247 * zz; beta = 1.376 - 0.826 * zz; gamma = 0.608 + 0.329 * zz
    return 2 * N * Mh / ((Mh / M1)**(-beta) + (Mh / M1)**gamma)
def Mh_of_Mstar(Ms, z=0.25):
    return 10**brentq(lambda lg: math.log10(moster_Mstar(10**lg, z)) - math.log10(Ms), 9.0, 15.5)
Ob_frac = 0.02237 / (0.02237 + 0.1200); DM_over_B = 0.1200 / 0.02237
bins = {"log M* 10.0": 1e10, "log M* 10.5": 3.16e10, "log M* 10.7": 5e10, "log M* 10.9": 8e10}
budget = {}
for lab, Ms in bins.items():
    Mb = 1.4 * Ms                                                # baryons: stars + cold gas (a common KiDS-lens convention)
    Mh = Mh_of_Mstar(Ms)
    for foot, a0 in A0.items():
        rM = math.sqrt(G * Mb * MSUN / a0) / MPC                 # Mpc
        r_gen = rM * (1 + Mh / Mb)                               # M_ph(<r) = (r/r_M - 1) M_b reaches M_200
        r_tight = rM * (1 + DM_over_B)                           # reaches the galaxy's own cosmic share
        budget[(lab, foot)] = {"M_b": Mb, "M_200": Mh, "r_M_kpc": rM * 1e3, "r_budget_generous_Mpc": r_gen,
                               "r_budget_tight_Mpc": r_tight}
    b = budget[(lab, "canonical")]
    P(f"    {lab}: M_b = {b['M_b']:.2e}, M_200 (Moster+13, z = 0.25) = {b['M_200']:.2e} Msun, r_M = {b['r_M_kpc']:.1f} kpc;"
      f"  budget radius: generous {b['r_budget_generous_Mpc']:.2f} Mpc, tight {b['r_budget_tight_Mpc']*1e3:.0f} kpc (canonical)")
OUT["numbers"]["B"] = {f"{k[0]}|{k[1]}": v for k, v in budget.items()}
gen_min = min(v["r_budget_generous_Mpc"] for v in budget.values())
gen_max = max(v["r_budget_generous_Mpc"] for v in budget.values())
tight_max = max(v["r_budget_tight_Mpc"] for v in budget.values())
n_short_gen = sum(1 for v in budget.values() if v["r_budget_generous_Mpc"] < 0.3)
check("B1 (measurement) the budget radius with CDM-like accretion (M_200 from Moster+13) against the KiDS-1000 clean "
      "isolated-lens radius 0.3 Mpc, per stellar-mass bin and footing",
      f"generous budget radius {gen_min:.2f}-{gen_max:.2f} Mpc; bins/footings running out inside 0.3 Mpc: {n_short_gen}/{len(budget)}",
      True,
      "a conserved phantom can only be as large as the dark fluid the galaxy accreted; the deep-MOND phantom grows "
      "linearly with radius (M_ph = (r/r_M - 1) M_b), a LCDM halo does not", load_bearing=False)
check("B2 (measurement) the same with only the galaxy's own cosmic share (Omega_dm/Omega_b) M_b",
      f"tight budget radius <= {tight_max*1e3:.0f} kpc", True,
      "the swarm lane BSK3's KiDS failure (+91 inside 0.3 Mpc) corresponds to a budget of this kind; BSK3 itself is "
      "not reproduced here", load_bearing=False)

# ============================================================================================ VERDICT
banner("VERDICT")
n_ok = sum(1 for _, ok, _ in CH if ok); n_lb_fail = sum(1 for _, ok, lb in CH if (not ok) and lb)
P(f"""  (1) For any kinetic function K(Q), the static mass term a galaxy feels and the khronon's late Jeans scale are one
  scale, mu_eff^2 = k_J^2 (1 + c_ad^2) (I1).  KiDS's external-field bound needs that scale short (<= 0.22 Mpc) and
  MOND-like lensing to ~1 Mpc needs it long (>= ~{need_mu_inv:.0f} Mpc): the khronon-as-dark-fluid aether of Blanchet &
  Skordis is closed by KiDS for every K, not only for their benchmarks (I3 with BSX1).
  (2) PAPER33 v1's cubic repair is withdrawn: at its passing parameters MOND ends inside ~{worst_rC:.0f} kpc and the
  K density dwarfs the phantom by >= 1e6 (I2).  The one-scale identity a0 = kappa c sqrt(G rho_Lambda) of v1's X3 is
  algebra and stands.
  (3) The budget: with CDM-like accretion the conserved phantom of a KiDS lens runs out at {gen_min:.2f}-{gen_max:.2f} Mpc
  ({n_short_gen} of {len(budget)} bin/footing cases inside the 0.3 Mpc clean radius); with only the galaxy's own cosmic
  share it runs out by {tight_max*1e3:.0f} kpc.  A conserved phantom reproduces KiDS's MOND-like lensing only if galaxies
  accrete more dark fluid than LCDM halos hold at those radii -- a question for nonlinear growth in the theory.
  Design lesson: the MOND function must not read the acceleration of the cosmological dark fluid.""")
P(f"\n  {n_ok}/{len(CH)} checks pass; load-bearing failures: {n_lb_fail}; wrote {SLUG}_results{'_MUTATE' if MUTATE else ''}.json")
json.dump(OUT, open(os.path.join(HERE, f"{SLUG}_results{'_MUTATE' if MUTATE else ''}.json"), "w"), indent=1, default=str)
sys.exit(1 if n_lb_fail else 0)
