#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
BSX2 -- A KHRONON THAT PASSES THE GATES BS24 FAILS: drop the quadratic term of K(Q) and give J(Y) one scale.
The cubic khronon keeps BS24's moving phantom (BSK1), loses the galactic mass term that ended MOND at r_C,
keeps a Jeans length short at EVERY epoch (so sigma_8 and the forest are LCDM's), and filters the web's field out
of the MOND function (KiDS).  With J = Lambda j(Y/Lambda), a0 = kappa c sqrt(G rho_Lambda) is the statement that
the khronon's one function has one scale; kappa is the shape number beta of j (not derived).

THE DIAGNOSIS (BSX1, BSK1)
  In BS24 one constant mu sets three things: the static mass term mu^2 phi of eq. 35 (MOND ends at
  r_C ~ (r_M/mu^2)^(1/3)), the late Jeans length 1/mu of the khronon (sigma_8), and the filter k^2/(k^2 + k_J^2) that
  hides the web's field from the MOND function (KiDS).  The comoving Jeans length is (1+z)/mu, so a short one
  today is a long one at high z.  All three come from the QUADRATIC term of K(Q) = mu^2 (Q-1)^2.  BS24 note (sec.
  4.3.2, their eq. 86) that for K starting at cubic order the K term drops out of the Newtonian limit.

THE CONSTRUCTION
  K(Q) = (2 M^2/3) (Q - 1)^3   (BS24's eq. 81 with n = 2 only; M^2 = mu^2 K_3 is the one parameter).
  J(Y) = Lambda j(Y/Lambda) with j(u) = 1 - u + beta u^(3/2) + ... at low u (BS24 eq. 37's form, one scale).
  Background (BS24 eqs. 82-85, n = 2): q = Q-1 = (I0/(2 M^2 a^3))^(1/2), 8piG rho = (I0/a^3)(1 + 2q/3),
  8piG P = I0 q/(3 a^3), w = q/(3 + 2q); here c_ad^2 = dP/drho = q/(2(1+q)); sound speed from BS24 eq. 71.
  Late Jeans length: lambda_J,phys = (2 M^2 I0)^(-1/4) a^(3/4) -> COMOVING (2 M^2 I0)^(-1/4) a^(-1/4): only 5.6x
  larger at z = 1000 than today (the quadratic term gives 1000x).

CHECKS
  X1 (symbolic) the cubic K contributes c^2 K_Q = 2 M^2 Xi^2/c^2 in the PN limit: 1PN, so eq. 35 is pure AQUAL
     (no mu^2 phi term, r_C -> infinity); the quadratic control keeps -2 mu^2 Xi (BS24 eq. 22).
  X2 cosmology with the cubic K for lambda_J,0 = 3 kpc .. 1 Mpc: sigma_8 within 5% of 0.811; the MOND function's
     external field at KiDS lenses (z = 0.25) below the KiDS bound (7.2e-5 / 5.2e-5 a0, BS2); matter power at
     z = 3, k = 1-10 h/Mpc within 10% of LCDM (a forest proxy); early w <= 0.0164 for a in 1e-5..1e-3 (the GDM
     level BS24 use).  The same machinery as BSX1 (controls C1/C2 repeated).
  X3 (symbolic) one-scale J: a0 = 2 c^2 sqrt(Lambda)/(3 beta) and, with rho_Lambda = Lambda c^2/(8 pi G),
     a0 = kappa c sqrt(G rho_Lambda) with kappa = 2 sqrt(8 pi)/(3 beta): kappa = 1/2 <=> beta = 4 sqrt(8 pi)/3.
  MUTATE=1 restores the quadratic term (n = 1) at the same late Jeans length: X1's mass term returns (r_C finite)
  and X2's high-z Jeans length is 1000x longer, so sigma_8 fails (rc = 1).  MUTATE outputs go to separate files.

LIMITS  Linear theory for sigma_8, the forest proxy and the web field; the phantom's MASS BUDGET at Mpc radii (a
  conserved fluid must be assembled from the cosmic khronon dust; the parallel lane BSK3) and the stability of J's
  GR-recovery tail (BSK1 M5) are NOT settled here; the cubic K's strong coupling at Q -> 1 is not analysed.

Run from the repository root:  python3 real_research/bs_khronon_2026/BSX2_cubic_one_scale_khronon.py
"""
import os, sys, json, math, time
import numpy as np
import sympy as sp
from scipy.integrate import solve_ivp, quad
from scipy.optimize import brentq

HERE = os.path.dirname(os.path.abspath(__file__))
MUTATE = os.environ.get("MUTATE", "0") == "1"
LANE = "BSX2"
SLUG = "BSX2_cubic_one_scale_khronon"
P = lambda *a: print(*a, flush=True)
CH, OUT = [], {"lane": LANE, "mutate": MUTATE, "checks": {}, "numbers": {}}
T0 = time.time()


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


P(__doc__.split("CHECKS")[0].strip())
if MUTATE:
    P("\n  *** MUTATE=1: the quadratic term is restored (n = 1) at the same late Jeans length; X1 and X2 must FAIL ***")

# ============================================================================================ X1
banner("X1  THE CUBIC K LEAVES THE NEWTONIAN LIMIT: eq. 35 becomes pure AQUAL (no mu^2 phi term)")
cc, Xi, M2s, mu2s = sp.symbols('c Xi M2 mu2', positive=True)
Qs = 1 - Xi / cc**2                                          # BS24 eq. 18a
Qv = sp.Symbol('Q')
K_cubic = sp.Rational(2, 3) * M2s * (Qv - 1)**3
K_quad = mu2s * (Qv - 1)**2
KQ_c = sp.expand(cc**2 * sp.diff(K_cubic, Qv).subs(Qv, Qs))
KQ_q = sp.expand(cc**2 * sp.diff(K_quad, Qv).subs(Qv, Qs))
lead_c = sp.limit(KQ_c, cc, sp.oo)                           # the Newtonian-order piece (c^0)
lead_q = sp.limit(KQ_q, cc, sp.oo)
P(f"    cubic:     c^2 K_Q = {KQ_c}  -> Newtonian-order piece {lead_c}   (1PN only)")
P(f"    quadratic: c^2 K_Q = {KQ_q}  -> Newtonian-order piece {lead_q}   (BS24 eq. 22c: the mu^2 Xi term of eq. 25)")
lead_model = lead_q if MUTATE else lead_c                    # MUTATE: the model's K is the quadratic one
x1_ok = (lead_model == 0) and (sp.simplify(lead_q + 2 * mu2s * Xi) == 0)
OUT["numbers"]["X1"] = {"cubic": str(KQ_c), "quadratic": str(KQ_q)}
check("X1 the cubic K contributes only at 1PN (c^2 K_Q = 2 M^2 Xi^2/c^2), so the static equation is AQUAL with no "
      "mass term and no r_C; the quadratic control carries BS24's -2 mu^2 Xi",
      f"model Newtonian piece {lead_model}; cubic {lead_c}; quadratic control {lead_q}", x1_ok,
      "MOND-like lensing is no longer cut off at r_C ~ (r_M/mu^2)^(1/3): the static profile is AQUAL's at every radius")

# ---------------------------------------------------------------------------------------- cosmology (BSX1 machinery)
c = 2.99792458e8; Mpc = 3.0856775814913673e22; G = 6.67430e-11
h = 0.6736; om_b, om_c = 0.02237, 0.1200; T_CMB = 2.7255; N_eff = 3.046; ns = 0.965
H0 = 100 * h * 1e3 / Mpc; rho_crit0 = 3 * H0**2 / (8 * math.pi * G)
Og = (4 * 5.670374419e-8 * T_CMB**4 / c**3) / rho_crit0; Or = Og * (1 + N_eff * (7 / 8) * (4 / 11)**(4 / 3))
Ob, Oc = om_b / h**2, om_c / h**2; Om = Ob + Oc; OL = 1 - Om - Or
A0 = {"canonical": 9.3619e-11, "alt": 1.1279e-10}; SIG8 = 0.811; HC = h / 2997.92458
E_BOUND = {"canonical": 7.2e-5, "alt": 5.18e-5}


def T_EH98(k):
    th = T_CMB / 2.7; s = 44.5 * math.log(9.83 / (Om * h * h)) / math.sqrt(1 + 10 * om_b**0.75)
    ag = 1 - 0.328 * math.log(431 * Om * h * h) * (Ob / Om) + 0.38 * math.log(22.3 * Om * h * h) * (Ob / Om)**2
    ge = Om * h * (ag + (1 - ag) / (1 + (0.43 * k * s / h)**4)); q = k * th * th / ge
    L = math.log(2 * math.e + 1.8 * q); Cc = 14.2 + 731.0 / (1 + 62.5 * q); return L / (L + Cc * q * q)


def P_un(kh): k = kh * h; return k**ns * T_EH98(k)**2
def Wth(x): return 3 * (math.sin(x) - x * math.cos(x)) / x**3
PN = (SIG8 / math.sqrt(quad(lambda kh: kh**2 * P_un(kh) * Wth(8 * kh)**2 / (2 * math.pi**2), 1e-4, 60, limit=600)[0]))**2
KH = np.logspace(-3, 1, 64); LNK = np.log(KH)
W8 = np.array([Wth(8 * k)**2 for k in KH])
D2REF = np.array([kh**3 * PN * P_un(kh) / (2 * math.pi**2) for kh in KH])
FOREST = (KH >= 1.0) & (KH <= 10.0)


class PowerKhronon:
    """K = (2 M^2/(n+1)) (Q-1)^(n+1) (BS24 eq. 81, single power); n = 2 is the cubic khronon, n = 1 BS24's quadratic."""
    def __init__(self, M2, n):
        self.M2, self.n = M2, n
        target = 3 * HC**2 * Oc
        f = lambda I0: I0 * (1 + (n / (n + 1)) * (I0 / (2 * M2))**(1 / n)) - target
        self.I0 = brentq(f, 1e-9 * target, target)

    def q(self, a): return (self.I0 / (2 * self.M2 * a**3))**(1 / self.n)
    def rho8(self, a): return self.I0 / a**3 * (1 + (self.n / (self.n + 1)) * self.q(a))
    def w(self, a):
        qv = self.q(a); n = self.n; return qv / (n + 1 + n * qv)
    def cad2(self, a):
        qv = self.q(a); return qv / (self.n * (1 + qv))
    def kJ2(self, a): return a**2 * 0.5 * self.rho8(a) * (1 + self.w(a)) / self.cad2(a)
    def cs2(self, a, k):
        kj2 = self.kJ2(a); return self.cad2(a) * kj2 / (kj2 + k * k)
    def Omega_frac(self, a): return self.rho8(a) / 3.0 / HC**2
    def lamJ_phys(self, a): return a / math.sqrt(self.kJ2(a))       # Mpc


class CDM:
    def Omega_frac(self, a): return Oc / a**3
    def w(self, a): return 0.0
    def cs2(self, a, k): return 0.0
    def kJ2(self, a): return float("inf")
    def rho8(self, a): return 3 * HC**2 * Oc / a**3


def E2(a, X): return Or / a**4 + Ob / a**3 + X.Omega_frac(a) + OL
def dlnH_dN(a, X): return 0.5 * (-4 * Or / a**4 - 3 * Ob / a**3 - 3 * (1 + X.w(a)) * X.Omega_frac(a)) / E2(a, X)


def grow(X, kh, z_i=1000.0, z_out=(3.0, 0.25, 0.0)):
    k = kh * h; a_i = 1.0 / (1 + z_i)
    def rhs(N, Y):
        a = math.exp(N); db, vb, dk, vk = Y
        e2 = E2(a, X); Hc = a * HC * math.sqrt(e2)
        Obf = Ob / a**3 / e2; Okf = X.Omega_frac(a) / e2; wv = X.w(a)
        if isinstance(X, PowerKhronon):
            da = 1e-4; wN = (X.w(a * math.exp(da)) - X.w(a * math.exp(-da))) / (2 * da); cs = X.cs2(a, k)
        else:
            wN = 0.0; cs = 0.0
        src = -1.5 * (Obf * db + Okf * dk); dl = dlnH_dN(a, X)
        return [-vb, -vb + src - vb * (1 + dl), -(1 + wv) * vk - 3 * (cs - wv) * dk,
                -(1 - 3 * wv) * vk - (wN / (1 + wv)) * vk + (cs * k * k / Hc**2) * dk / (1 + wv) + src - vk * (1 + dl)]
    Ns = sorted(math.log(1 / (1 + z)) for z in z_out)
    sol = solve_ivp(rhs, (math.log(a_i), 0.0), [1.0, -1.0, 1.0, -1.0], method="LSODA", rtol=1e-7, atol=1e-12, t_eval=Ns)
    return {z: (sol.y[0][int(np.argmin(np.abs(sol.t - math.log(1 / (1 + z)))))],
                sol.y[2][int(np.argmin(np.abs(sol.t - math.log(1 / (1 + z)))))]) for z in z_out}


def dm_tot(r, z, X):
    a = 1 / (1 + z); ok = X.Omega_frac(a); ob = Ob / a**3
    return (ob * r[z][0] + ok * r[z][1]) / (ob + ok)


LCDM = CDM(); REF = [grow(LCDM, kh) for kh in KH]
REF_m = {z: np.array([dm_tot(r, z, LCDM) for r in REF]) for z in (0.0, 0.25, 3.0)}


def evaluate(X):
    res = [grow(X, kh) for kh in KH]
    m0 = np.array([dm_tot(r, 0.0, X) for r in res])
    s8 = math.sqrt(np.trapz(D2REF * (m0 / REF_m[0.0])**2 * W8, LNK))
    m3 = np.array([dm_tot(r, 3.0, X) for r in res]); pr3 = (m3 / REF_m[3.0])**2
    k25 = np.array([r[0.25][1] for r in res])
    D2K25 = D2REF * (REF_m[0.25] / REF_m[0.0])**2 * (k25 / REF_m[0.25])**2
    a = 0.8; k = KH * h; kj2 = X.kJ2(a)
    A_web = 0.5 * X.rho8(a) * a * math.sqrt(np.trapz(D2K25 * k**2 / (k**2 + kj2)**2, LNK)) * c**2 / Mpc
    return s8, pr3, A_web


s8_l, pr3_l, _ = evaluate(LCDM)
D2m25 = D2REF * (REF_m[0.25] / REF_m[0.0])**2
g_l = 0.5 * 3 * HC**2 * Om / 0.8**3 * 0.8 * math.sqrt(np.trapz(D2m25 / (KH * h)**2, LNK)) * c**2 / Mpc
banner("X2  COSMOLOGY OF THE CUBIC KHRONON: sigma_8, the forest proxy, the KiDS field, the early equation of state")
P(f"    controls (BSX1's): LCDM sigma_8 = {s8_l:.4f}; LCDM Newtonian web field at z = 0.25 = {g_l/A0['canonical']:.4f} a0")
n_use = 1 if MUTATE else 2
rows = {}
for lamJ0 in (0.0003, 0.001, 0.003, 0.01, 0.03, 0.1, 0.3, 1.0):                # physical Jeans length today, Mpc
    # pick the model's one parameter so that the late Jeans length today equals lamJ0
    def gap(lgM2):
        return math.log(PowerKhronon(10**lgM2, n_use).lamJ_phys(1.0) / lamJ0)
    lgM2 = brentq(gap, -2, 40)
    X = PowerKhronon(10**lgM2, n_use)
    s8, pr3, A = evaluate(X)
    wearly = max(X.w(a) for a in np.logspace(-5, -3, 60))
    lam1000 = X.lamJ_phys(1 / 1001) * 1001                        # comoving at z = 1000
    ok = {"sigma8": abs(s8 / SIG8 - 1) <= 0.05, "forest": float(np.min(pr3[FOREST])) >= 0.9,
          "kids": A / A0["canonical"] <= E_BOUND["canonical"] and A / A0["alt"] <= E_BOUND["alt"],
          "early_w": wearly <= 0.0164}
    rows[lamJ0] = {"log10_M2_per_Mpc2": round(lgM2, 3), "sigma8": round(s8, 4), "forest_min_ratio": round(float(np.min(pr3[FOREST])), 4),
                   "e_web_canonical": A / A0["canonical"], "e_web_alt": A / A0["alt"], "w_early_max": wearly,
                   "comoving_lamJ_z1000_Mpc": round(lam1000, 4), "passes": ok, "all": all(ok.values())}
    P(f"    lambda_J,0 = {lamJ0*1e3:6g} kpc (n = {n_use}): sigma_8 = {s8:.3f}  forest P/P_LCDM >= {np.min(pr3[FOREST]):.3f}  "
      f"e_web = {A/A0['canonical']:.2e} a0  max early w = {wearly:.1e}  comoving lambda_J(z=1000) = {lam1000:.3g} Mpc  "
      f"-> {'ALL PASS' if all(ok.values()) else 'fails ' + ','.join(k_ for k_, v in ok.items() if not v)}")
OUT["numbers"]["X2"] = {"lcdm_sigma8": s8_l, "lcdm_field_a0": g_l / A0["canonical"], "rows": {str(k): v for k, v in rows.items()}}
window = [k for k, v in rows.items() if v["all"]]
check("X2 the cubic khronon passes sigma_8 (5%), the forest proxy (10%), the KiDS external-field bound and the early "
      "equation of state together, over a range of its one parameter",
      f"passing lambda_J,0 = {[f'{w*1e3:g} kpc' for w in window]}",
      len(window) >= 1 and abs(s8_l / SIG8 - 1) < 0.01,
      "the comoving Jeans length grows only as (1+z)^(1/4) into the past, so a short one today stays short at z = 1000 "
      "(the quadratic term's grows as (1+z)); the same short Jeans length filters the web's field out of the MOND function")

# ============================================================================================ X3
banner("X3  ONE SCALE: J = Lambda j(Y/Lambda) makes a0 = kappa c sqrt(G rho_Lambda) an identity of the action")
Lam, beta, u, a0s, Gs = sp.symbols('Lambda beta u a_0 G', positive=True)
Ys = sp.Symbol('Y', positive=True)
J_one = Lam * (1 - Ys / Lam + beta * (Ys / Lam)**sp.Rational(3, 2))
J_bs24 = Lam - Ys + 2 * cc**2 / (3 * a0s) * Ys**sp.Rational(3, 2)            # BS24 eq. 37
a0_sol = sp.solve(sp.Eq(sp.expand(J_one).coeff(Ys**sp.Rational(3, 2)), sp.expand(J_bs24).coeff(Ys**sp.Rational(3, 2))), a0s)[0]
rhoL = Lam * cc**2 / (8 * sp.pi * Gs)
kappa_expr = sp.simplify(a0_sol / (cc * sp.sqrt(Gs * rhoL)))
beta_half = sp.solve(sp.Eq(kappa_expr, sp.Rational(1, 2)), beta)[0]
P(f"    a0 = {a0_sol};   kappa = a0/(c sqrt(G rho_Lambda)) = {kappa_expr};   kappa = 1/2  <=>  beta = {beta_half} = {float(beta_half):.4f}")
Lam_obs = 3 * (H0 / c)**2 * 0.6847 / 1.0                                  # Lambda = 3 H0^2 Omega_L / c^2 (1/m^2)
a0_check = float((2 * c**2 * math.sqrt(Lam_obs)) / (3 * float(beta_half)))
P(f"    with the observed Lambda (Omega_L = 0.6847, h = 0.6736): a0 = {a0_check:.4e} m/s^2 at beta = {float(beta_half):.3f} "
  f"(the canonical footing 9.36e-11)")
x3_ok = sp.simplify(kappa_expr - 2 * sp.sqrt(8 * sp.pi) / (3 * beta)) == 0 and abs(a0_check / 9.3619e-11 - 1) < 0.01
OUT["numbers"]["X3"] = {"a0": str(a0_sol), "kappa": str(kappa_expr), "beta_for_half": float(beta_half), "a0_check": a0_check}
check("X3 with one scale in J, the MOND acceleration is fixed by the cosmological constant J(0) = Lambda: "
      "a0 = 2 c^2 sqrt(Lambda)/(3 beta) = kappa c sqrt(G rho_Lambda), kappa = 2 sqrt(8 pi)/(3 beta); kappa = 1/2 is "
      "beta = 4 sqrt(8 pi)/3 and reproduces the canonical a0 = 9.36e-11 from Planck's Lambda",
      f"kappa = {kappa_expr}; beta(1/2) = {float(beta_half):.4f}; a0 = {a0_check:.4e}", x3_ok,
      "the framework's relation becomes structural (a0 and the vacuum energy are two coefficients of one function); "
      "kappa is the shape number beta of that function and is NOT derived (the zero-mode theorem stands)")

# ============================================================================================ VERDICT
banner("VERDICT")
n_ok = sum(1 for _, ok, _ in CH if ok); n_lb_fail = sum(1 for _, ok, lb in CH if (not ok) and lb)
P(f"""  Dropping the quadratic term of K(Q) removes, at one stroke, the three failures BSX1 found for BS24: the static mass
  term that ended MOND at r_C (X1: the cubic term is 1PN), and the long high-z Jeans length that suppressed sigma_8
  and forced a trade-off with KiDS (X2: the comoving Jeans length now grows only as (1+z)^(1/4)).  Passing window of
  the one parameter (late physical Jeans length): {[f'{w*1e3:g} kpc' for w in window]} -- sigma_8, a forest proxy, the KiDS
  external-field bound and the early equation of state together.  BS24's moving phantom (BSK1 M3) is untouched.
  With J = Lambda j(Y/Lambda) the framework's a0 = kappa c sqrt(G rho_Lambda) is an identity of the action, kappa = 1/2
  at beta = 4 sqrt(8 pi)/3 (X3).  NOT settled here: the phantom's mass budget at Mpc radii (BSK3), the stability of
  J's GR-recovery tail (BSK1 M5; a monotone j up to g ~ 1e3 a0 confines it to where the phantom is < 1e-3 of the
  field), and the cubic K's strong coupling at Q -> 1.  A candidate that passes the gates computed, not a theory.""")
P(f"\n  {n_ok}/{len(CH)} checks pass; load-bearing failures: {n_lb_fail}; wrote {SLUG}_results{'_MUTATE' if MUTATE else ''}.json ({time.time()-T0:.0f} s)")
json.dump(OUT, open(os.path.join(HERE, f"{SLUG}_results{'_MUTATE' if MUTATE else ''}.json"), "w"), indent=1, default=str)
sys.exit(1 if n_lb_fail else 0)
