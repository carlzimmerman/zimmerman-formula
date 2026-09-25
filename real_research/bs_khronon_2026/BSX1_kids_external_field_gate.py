#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
BSX1 -- THE BLANCHET-SKORDIS KHRONON AGAINST THE KiDS EXTERNAL-FIELD GATE, from their own linear cosmology: the
MOND function reads the gradient of the khronon's OWN potential, filtered by k^2/(k^2 + k_J^2); with the
k-dependent sound speed of their eq. 71 the same Jeans scale also sets sigma_8.  A scan in mu asks whether any
value passes KiDS's external-field bound, a MOND-like lensing profile to ~1 Mpc and sigma_8 together.

THE THEORY TESTED
  Blanchet & Skordis, JCAP 11 (2024) 040, arXiv:2404.06584 ("BS24"), their linear cosmology (sec. 4):
    - the khronon is a GDM fluid (eqs. 64-75) with w(a) and adiabatic c_ad^2(a) from K(Q); the DBI form (eq. 87)
      gives 8 pi G rho_K = I0/a^3 + (2mu^2/lam)[sqrt(1 + lam Z^2) - 1], 8 pi G P_K = (2mu^2/lam)[1 - 1/sqrt(1+lam Z^2)],
      Z = I0/(2 mu^2 a^3), and c_ad^2 = Z/[(1 + lam Z^2)(sqrt(1 + lam Z^2) + Z)] (eqs. 89, 94);
    - its sound speed is k-dependent (eq. 71): c_s^2 = c_ad^2 k_J^2/(k_J^2 + k^2), k_J^2 = 4 pi G a^2 rho_K (1+w)/c_ad^2;
    - the acceleration of the khronon congruence -- the argument of the MOND function J(Y) -- is A_i = grad_i Ups
      (eq. 61b) with Ups = -4 pi G a^2 rho_K Delta_K/(k^2 + k_J^2) in Fourier space (eq. 67 and its footnote 9).
  Their two published benchmarks (their Fig. 1): (A) mu^-1 = 22.3 Mpc, lam_D = 1; (B) mu^-1 = 223 kpc, lam_D = 30.

THE GATE (the one C-H/K + switch failed in BS2/BS3)
  KiDS-1000 isolated-lens lensing bounds a uniform external field in the MOND function at e = g_ext/a0 <= 7.2e-5
  (canonical; 5.2e-5 alt; BS2 E7).  C-H/K's kernel reads the Newtonian field of a LCDM-like web, 0.013-0.015 a0,
  and is excluded (BS2 +569, BS3 +404 with a free two-halo term).  BS24's kernel reads A = grad Ups instead: the
  khronon's own potential gradient, which the k_J filter removes on scales larger than the late Jeans length.

METHOD
  Sub-horizon Newtonian-gauge GDM equations (Ma-Bertschinger form) for baryons + the khronon, in N = ln a, one
  Fourier mode at a time, from z = 1000 (identical growing-mode initial data for every model, so ratios to LCDM
  isolate the khronon); background with the khronon's exact w(a).  LCDM reference = the same code with w = c_s = 0.
  sigma_8 and spectra: L341's EH98 transfer normalised to sigma_8 = 0.811, times each model's growth ratio.
  Fields at the KiDS lens redshift z = 0.25: rms |grad Ups| (BS24) and rms |grad Phi| (LCDM control) from linear
  theory over k = 1e-3..10 h/Mpc.  BS24's crossover radius r_C ~ (r_M/mu^2)^(1/3) (their eq. 38) marks where the
  mu^2 term ends MOND-like behaviour; the full static profile with that term was confronted with KiDS for AeST (the
  same quasi-static equation) by Mistele, McGaugh & Hossenfelder, A&A 676, A100 (2023), and is not redone here.

CONTROLS
  C1 the integrator's LCDM run reproduces sigma_8 = 0.811 (1%); C2 the LCDM Newtonian field at z = 0.25 agrees with
  BS3's mock (0.0150 a0) within 25%; C3 the DBI background: w from eqs. 89 equals eq. 94a, and the late-time Jeans
  wavenumber is k_J = a mu (the physical Jeans length is 1/mu, independent of w); C4 (documentary) with the
  k-dependence of eq. 71 removed (c_s^2 -> c_ad^2 at all k) the pressure is no longer capped at the self-gravity
  level and sigma_8 falls further: eq. 71's k-dependence LIMITS the damage to a cancellation of self-gravity.
  MUTATE=1 sets the khronon's sound speed to zero (pure dust): the sigma_8 and external-field suppressions must
  vanish, so G1 and E1 must FAIL (rc = 1).  MUTATE outputs go to separate files.

Run from the repository root:  python3 real_research/bs_khronon_2026/BSX1_kids_external_field_gate.py
"""
import os, sys, json, math, time
import numpy as np
from scipy.integrate import solve_ivp, quad
from scipy.optimize import brentq

HERE = os.path.dirname(os.path.abspath(__file__))
MUTATE = os.environ.get("MUTATE", "0") == "1"
LANE = "BSX1"
SLUG = "BSX1_kids_external_field_gate"
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


P(__doc__.split("METHOD")[0].strip())
if MUTATE:
    P("\n  *** MUTATE=1: the khronon's sound speed is set to zero (pure dust); G1 and E1 must FAIL ***")

# ---------------------------------------------------------------------------------------- cosmology (L341/L142 machinery)
c = 2.99792458e8; Mpc = 3.0856775814913673e22; G = 6.67430e-11; MSUN = 1.989e30; KPC = Mpc / 1e3
h = 0.6736; om_b, om_c = 0.02237, 0.1200; T_CMB = 2.7255; N_eff = 3.046; ns = 0.965
H0 = 100 * h * 1e3 / Mpc; rho_crit0 = 3 * H0**2 / (8 * math.pi * G)
Og = (4 * 5.670374419e-8 * T_CMB**4 / c**3) / rho_crit0; Or = Og * (1 + N_eff * (7 / 8) * (4 / 11)**(4 / 3))
Ob, Oc = om_b / h**2, om_c / h**2; Om = Ob + Oc; OL = 1 - Om - Or
A0 = {"canonical": 9.3619e-11, "alt": 1.1279e-10}; SIG8 = 0.811
HC = h / 2997.92458                                                # H0/c in 1/Mpc
E_BOUND = {"canonical": 7.2e-5, "alt": 5.18e-5}                     # BS2 E7: KiDS bound on a shared external field
BS3_FIELD = 0.0150                                                  # BS3: rms |g| at isolated lenses, z = 0.25, canonical


def T_EH98(k):
    th = T_CMB / 2.7; s = 44.5 * math.log(9.83 / (Om * h * h)) / math.sqrt(1 + 10 * om_b**0.75)
    ag = 1 - 0.328 * math.log(431 * Om * h * h) * (Ob / Om) + 0.38 * math.log(22.3 * Om * h * h) * (Ob / Om)**2
    ge = Om * h * (ag + (1 - ag) / (1 + (0.43 * k * s / h)**4)); q = k * th * th / ge
    L = math.log(2 * math.e + 1.8 * q); Cc = 14.2 + 731.0 / (1 + 62.5 * q); return L / (L + Cc * q * q)


def P_un(kh): k = kh * h; return k**ns * T_EH98(k)**2
def Wth(x): return 3 * (math.sin(x) - x * math.cos(x)) / x**3
PN = (SIG8 / math.sqrt(quad(lambda kh: kh**2 * P_un(kh) * Wth(8 * kh)**2 / (2 * math.pi**2), 1e-4, 60, limit=600)[0]))**2
def Delta2_lin0(kh): return kh**3 * PN * P_un(kh) / (2 * math.pi**2)     # dimensionless power today (LCDM)


KH = np.logspace(-3, 1, 64)                                          # h/Mpc; grid for fields and sigma_8
LNK = np.log(KH)
W8 = np.array([Wth(8 * k)**2 for k in KH])
D2REF = np.array([Delta2_lin0(k) for k in KH])


def sigma8_from(D2):                                                 # D2 = dimensionless power on KH at z = 0
    return math.sqrt(np.trapz(D2 * W8, LNK))


# ---------------------------------------------------------------------------------------- the DBI khronon (BS24 eqs. 87-95)
class Khronon:
    def __init__(self, mu_inv_mpc, lam, dust=False):
        self.mu = 1.0 / mu_inv_mpc; self.lam = lam; self.dust = dust
        target = 3 * HC**2 * Oc                                     # 8 pi G rho_K0 / c^2 in 1/Mpc^2
        f = lambda I0: I0 + (2 * self.mu**2 / lam) * (math.sqrt(1 + lam * (I0 / (2 * self.mu**2))**2) - 1) - target
        self.I0 = brentq(f, 1e-6 * target, target)

    def Z(self, a): return self.I0 / (2 * self.mu**2 * a**3)

    def rho8(self, a):                                              # 8 pi G rho_K / c^2 (physical, 1/Mpc^2)
        Zv = self.Z(a); return self.I0 / a**3 + (2 * self.mu**2 / self.lam) * (math.sqrt(1 + self.lam * Zv**2) - 1)

    def p8(self, a):
        Zv = self.Z(a); return (2 * self.mu**2 / self.lam) * (1 - 1 / math.sqrt(1 + self.lam * Zv**2))

    def w(self, a): return 0.0 if self.dust else self.p8(a) / self.rho8(a)

    def w94(self, a):
        Zv = self.Z(a); s = math.sqrt(1 + self.lam * Zv**2); return Zv / (1 + self.lam * Zv**2 + (1 + Zv) * s)

    def cad2(self, a):
        if self.dust: return 0.0
        Zv = self.Z(a); s = math.sqrt(1 + self.lam * Zv**2); return Zv / ((1 + self.lam * Zv**2) * (s + Zv))

    def kJ2(self, a):                                               # comoving, 1/Mpc^2
        ca = self.cad2(a)
        if ca <= 0: return float("inf")
        return a**2 * 0.5 * self.rho8(a) * (1 + self.w(a)) / ca

    def cs2(self, a, k, kdep=True):                                 # BS24 eq. 71
        ca = self.cad2(a)
        if ca <= 0: return 0.0
        if not kdep: return ca
        kj2 = self.kJ2(a); return ca * kj2 / (kj2 + k * k)

    def Omega_frac(self, a): return self.rho8(a) / 3.0 / HC**2     # rho_K(a)/rho_crit0


class CDM:
    dust = True
    def Omega_frac(self, a): return Oc / a**3
    def w(self, a): return 0.0
    def cs2(self, a, k, kdep=True): return 0.0
    def kJ2(self, a): return float("inf")
    def rho8(self, a): return 3 * HC**2 * Oc / a**3


def E2(a, X):
    return Or / a**4 + Ob / a**3 + X.Omega_frac(a) + OL


def dlnH_dN(a, X):
    wv = X.w(a)
    num = -4 * Or / a**4 - 3 * Ob / a**3 - 3 * (1 + wv) * X.Omega_frac(a)
    return 0.5 * num / E2(a, X)


def grow(X, kh, z_i=1000.0, z_out=(0.25, 0.0), kdep=True):
    """Two-fluid sub-horizon GDM growth for one mode; returns {z: (delta_b, delta_K)} with identical growing-mode ICs."""
    k = kh * h
    a_i = 1.0 / (1 + z_i)

    def rhs(N, Y):
        a = math.exp(N); db, vb, dk, vk = Y
        e2 = E2(a, X); Hc = a * HC * math.sqrt(e2)                  # conformal H in 1/Mpc
        Obf = Ob / a**3 / e2; Okf = X.Omega_frac(a) / e2
        wv = X.w(a)
        if isinstance(X, Khronon) and not X.dust:
            da = 1e-4
            wN = (X.w(a * math.exp(da)) - X.w(a * math.exp(-da))) / (2 * da)
        else:
            wN = 0.0
        cs = 0.0 if (MUTATE or X.dust) else X.cs2(a, k, kdep)
        src = -1.5 * (Obf * db + Okf * dk)                         # k^2 Psi / Hc^2
        dl = dlnH_dN(a, X)
        ddb = -vb
        dvb = -vb + src - vb * (1 + dl)
        ddk = -(1 + wv) * vk - 3 * (cs - wv) * dk
        dvk = -(1 - 3 * wv) * vk - (wN / (1 + wv)) * vk + (cs * k * k / Hc**2) * dk / (1 + wv) + src - vk * (1 + dl)
        return [ddb, dvb, ddk, dvk]

    Ns = sorted([math.log(1 / (1 + z)) for z in z_out])
    sol = solve_ivp(rhs, (math.log(a_i), 0.0), [1.0, -1.0, 1.0, -1.0], method="LSODA", rtol=1e-7, atol=1e-12,
                    t_eval=Ns, dense_output=False)
    out = {}
    for zz in z_out:
        j = int(np.argmin(np.abs(sol.t - math.log(1 / (1 + zz)))))
        out[zz] = (sol.y[0][j], sol.y[2][j])
    return out


def run_model(X, kdep=True):
    """Growth on the KH grid -> total-matter and khronon spectra relative to the LCDM reference (same ICs)."""
    res = [grow(X, kh, kdep=kdep) for kh in KH]
    return res


LCDM = CDM()
REF = run_model(LCDM)
def dm_tot(r, z, X):
    a = 1 / (1 + z); ok = X.Omega_frac(a); ob = Ob / a**3
    return (ob * r[z][0] + ok * r[z][1]) / (ob + ok)


REF_m0 = np.array([dm_tot(r, 0.0, LCDM) for r in REF])
REF_m25 = np.array([dm_tot(r, 0.25, LCDM) for r in REF])


def spectra(X, res):
    """sigma_8 and the z = 0.25 khronon/total-matter power, scaled from the LCDM EH98 reference by growth ratios."""
    m0 = np.array([dm_tot(r, 0.0, X) for r in res])
    D2m0 = D2REF * (m0 / REF_m0)**2
    k25 = np.array([r[0.25][1] for r in res])
    m25 = np.array([dm_tot(r, 0.25, X) for r in res])
    # LCDM at z = 0.25 = D2REF * (REF_m25/REF_m0)^2; model khronon at z = 0.25 relative to that
    D2K25 = D2REF * (REF_m25 / REF_m0)**2 * (k25 / REF_m25)**2
    D2m25 = D2REF * (REF_m25 / REF_m0)**2 * (m25 / REF_m25)**2
    return sigma8_from(D2m0), D2K25, D2m25, m0 / REF_m0


def field_rms(X, D2, z, filt=True):
    """rms |grad Ups| (filt = True, BS24 eq. 67) or |grad Phi| (filt = False, Newtonian) in m/s^2 at redshift z."""
    a = 1 / (1 + z); k = KH * h                                     # 1/Mpc comoving
    fourpiGrho = 0.5 * X.rho8(a) if filt else 0.5 * (3 * HC**2 * Om / a**3)   # 4 pi G rho / c^2, 1/Mpc^2 physical
    kj2 = X.kJ2(a) if filt else 0.0                                  # dust (c_ad = 0): k_J -> inf, Ups = 0 (their eq. 67)
    integrand = D2 * k**2 / (k**2 + kj2)**2                          # Mpc^2
    I = math.sqrt(np.trapz(integrand, LNK))                          # Mpc
    # A = (1/a) d/dx_comoving [4 pi G a^2 rho Delta/(k^2 + kJ^2)] -> 4 pi G a rho * (Mpc) ; restore c^2 and units
    return fourpiGrho * a * I * c**2 / Mpc                           # (1/Mpc^2)(Mpc) c^2 / Mpc-to-m -> m/s^2


# ============================================================================================ C1-C3
banner("C1-C3  CONTROLS: the LCDM spectrum, the LCDM field at the KiDS lens redshift, BS24's DBI background")
s_lcdm, _, D2m25_lcdm, _ = spectra(LCDM, REF)
g_lcdm = field_rms(LCDM, D2m25_lcdm, 0.25, filt=False)
P(f"    LCDM: sigma_8 = {s_lcdm:.4f} (reference 0.811);  rms |grad Phi| at z = 0.25, k = 1e-3..10 h/Mpc: "
  f"{g_lcdm:.3e} m/s^2 = {g_lcdm/A0['canonical']:.4f} a0 (BS3 mock: {BS3_FIELD} a0)")
check("C1 the two-fluid integrator's LCDM run reproduces sigma_8 = 0.811 to 1%", f"{s_lcdm:.4f}",
      abs(s_lcdm / SIG8 - 1) < 0.01)
check("C2 the LCDM Newtonian field at z = 0.25 agrees with BS3's isolated-lens mock (0.0150 a0) within 25%",
      f"{g_lcdm/A0['canonical']:.4f} a0 vs {BS3_FIELD}", abs(g_lcdm / A0['canonical'] / BS3_FIELD - 1) < 0.25,
      "the linear field that BS2/BS3 scored; the BS24 kernel's field below is computed with the same spectrum")
BENCH = {"A (mu^-1 = 22.3 Mpc, lam_D = 1)": (22.3, 1.0), "B (mu^-1 = 223 kpc, lam_D = 30)": (0.223, 30.0)}
c3_ok = True; c3_rows = {}
for lab, (mi, lam) in BENCH.items():
    X = Khronon(mi, lam)
    wd = max(abs(X.w(a) - X.w94(a)) for a in np.logspace(-3, 0, 50))
    kj_ratio = math.sqrt(X.kJ2(1.0)) / (1.0 * X.mu)
    a_turn = (X.I0 / (2 * X.mu**2))**(1 / 3)
    wmax = max(X.w(a) for a in np.logspace(-4, 0, 400))
    c3_rows[lab] = {"I0": X.I0, "w0": X.w(1.0), "cad2_0": X.cad2(1.0), "kJ_over_a_mu_today": kj_ratio,
                    "z_turn(Z=1)": 1 / a_turn - 1, "w_max": wmax, "w_eq89_vs_eq94_maxdiff": wd}
    P(f"    {lab}: w today {X.w(1.0):.3e}, c_ad^2 today {X.cad2(1.0):.3e}, Z = 1 at z = {1/a_turn - 1:.0f}, "
      f"max w = {wmax:.3g};  k_J/(a mu) today = {kj_ratio:.4f};  |w(89) - w(94a)| <= {wd:.1e}")
    c3_ok = c3_ok and wd < 1e-8 and abs(kj_ratio - 1) < 0.01
OUT["numbers"]["controls"] = {"sigma8_lcdm": s_lcdm, "g_lcdm_a0": g_lcdm / A0['canonical'], "benchmarks": c3_rows}
check("C3 BS24's DBI background: eq. 89's w equals eq. 94a, and the late Jeans wavenumber is k_J = a mu (physical "
      "Jeans length 1/mu, independent of w)", f"{json.dumps({k: round(v['kJ_over_a_mu_today'], 4) for k, v in c3_rows.items()})}",
      c3_ok)

# ============================================================================================ G, E: the benchmarks
banner("G, E  THE BENCHMARKS: sigma_8 and the MOND function's external field at KiDS lenses (z = 0.25)")
bench_out = {}
for lab, (mi, lam) in BENCH.items():
    X = Khronon(mi, lam, dust=MUTATE)
    res = run_model(X)
    s8, D2K25, D2m25, ratio0 = spectra(X, res)
    A_web = field_rms(X, D2K25, 0.25, filt=True)
    g_new = field_rms(X, D2m25, 0.25, filt=False)
    rows = {}
    for foot, a0 in A0.items():
        rows[foot] = {"e_web": A_web / a0, "e_bound": E_BOUND[foot], "over_bound": A_web / a0 / E_BOUND[foot]}
    rC = {f"{m:.0e}": ((math.sqrt(G * m * MSUN / A0['canonical']) / Mpc) / X.mu**2)**(1 / 3) for m in (1e10, 6e10, 3e11)}
    iK = [int(np.argmin(np.abs(KH - kk))) for kk in (0.01, 0.1, 1.0)]
    bench_out[lab] = {"sigma8": s8, "growth_ratio_k=0.01/0.1/1": [round(float(ratio0[i]), 4) for i in iK],
                      "A_web_m_s2": A_web, "g_newton_model_m_s2": g_new, "footings": rows,
                      "r_C_Mpc_by_Mb": {k_: round(v, 3) for k_, v in rC.items()}}
    P(f"    {lab}:")
    P(f"      sigma_8 = {s8:.3f} (LCDM 0.811);  total-matter growth / LCDM at k = 0.01/0.1/1 h/Mpc: "
      f"{bench_out[lab]['growth_ratio_k=0.01/0.1/1']}")
    P(f"      MOND-function external field rms |grad Ups| = {A_web:.3e} m/s^2 = {A_web/A0['canonical']:.2e} a0 (canonical), "
      f"{A_web/A0['alt']:.2e} a0 (alt);  KiDS bound 7.2e-5 / 5.2e-5 -> x{rows['canonical']['over_bound']:.3g} / x{rows['alt']['over_bound']:.3g}")
    P(f"      (the model's own Newtonian web field, for comparison: {g_new/A0['canonical']:.2e} a0)")
    P(f"      r_C ~ (r_M/mu^2)^(1/3) for M_b = 1e10 / 6e10 / 3e11 Msun: "
      + " / ".join(f"{v:.2f}" for v in rC.values()) + " Mpc")
OUT["numbers"]["benchmarks"] = bench_out
bA = bench_out["A (mu^-1 = 22.3 Mpc, lam_D = 1)"]; bB = bench_out["B (mu^-1 = 223 kpc, lam_D = 30)"]
g1_ok = (bA["sigma8"] < 0.9 * SIG8) and (bB["sigma8"] < 0.9 * SIG8)
check("G1 with their own k-dependent sound speed (eq. 71) both published benchmarks suppress linear sigma_8 below "
      "0.9 x 0.811 (the late khronon does not self-gravitate below 1/mu, after the DBI turning point)",
      f"A: sigma_8 = {bA['sigma8']:.3f}; B: sigma_8 = {bB['sigma8']:.3f}", g1_ok,
      "BS24 checked w(a) against GDM constraints but left the k-dependent sound speed to future work; here it is "
      "integrated -- a linear-theory statement (nonlinear MOND growth is not included)")
e1_ok = bA["footings"]["canonical"]["over_bound"] > 1 and bA["footings"]["alt"]["over_bound"] > 1
check("E1 benchmark A's MOND-function external field at KiDS lenses exceeds KiDS-1000's bound on both footings "
      "(the gate C-H/K + switch failed); benchmark B's is recorded",
      f"A: e = {bA['footings']['canonical']['e_web']:.2e} (x{bA['footings']['canonical']['over_bound']:.3g} canonical, "
      f"x{bA['footings']['alt']['over_bound']:.3g} alt); B: e = {bB['footings']['canonical']['e_web']:.2e} "
      f"(x{bB['footings']['canonical']['over_bound']:.3g})", e1_ok,
      "BS2's chi^2 profile puts a uniform field of this size at Delta chi^2 of order +100..+300 on KiDS-1000")

# ============================================================================================ S: the scan in mu
banner("S  THE PINCER ON mu: KiDS's external-field bound, a MOND-like lens profile to ~1 Mpc, and sigma_8")
MU_SCAN = [0.03, 0.1, 0.223, 0.5, 1.0, 3.0, 10.0, 22.3, 50.0, 100.0]
scan = {}
for lam in (1.0, 30.0):
    for mi in MU_SCAN:
        X = Khronon(mi, lam, dust=MUTATE)
        res = run_model(X)
        s8, D2K25, _, _ = spectra(X, res)
        e = field_rms(X, D2K25, 0.25, filt=True) / A0["canonical"]
        rC = ((math.sqrt(G * 6e10 * MSUN / A0['canonical']) / Mpc) / X.mu**2)**(1 / 3)
        passes = {"efe": e <= E_BOUND["canonical"], "rC>=1Mpc": rC >= 1.0, "sigma8": abs(s8 / SIG8 - 1) <= 0.1}
        scan[f"lam={lam:g},mu^-1={mi:g}Mpc"] = {"sigma8": round(s8, 4), "e_web": e, "r_C_MW_Mpc": round(rC, 3),
                                                "passes": passes, "all": all(passes.values())}
        P(f"    lam_D = {lam:4g}  mu^-1 = {mi:7.3f} Mpc: sigma_8 = {s8:6.3f}  e_web = {e:9.2e} a0  r_C(6e10) = {rC:7.3f} Mpc"
          f"   efe {'ok' if passes['efe'] else '--'}  r_C {'ok' if passes['rC>=1Mpc'] else '--'}  "
          f"sigma_8 {'ok' if passes['sigma8'] else '--'}")
OUT["numbers"]["scan"] = scan
n_all = sum(1 for v in scan.values() if v["all"])
check("S1 no mu in 0.03-100 Mpc (lam_D = 1 and 30) passes all three at once: e_web <= 7.2e-5 (KiDS), r_C >= 1 Mpc for "
      "a Milky-Way lens (MOND-like lensing to ~1 Mpc), sigma_8 within 10% of 0.811",
      f"{n_all} of {len(scan)} grid points pass all three", n_all == 0,
      "the three requirements pull mu in different directions; r_C uses BS24's order-of-magnitude eq. 38 and the "
      "1 Mpc criterion follows the flat KiDS circular velocities (Brouwer+21; Mistele+2024)", load_bearing=False)

efe_ok_mu = sorted({float(k_.split("mu^-1=")[1][:-3]) for k_, v in scan.items() if v["passes"]["efe"]})
rc_ok_mu = sorted({float(k_.split("mu^-1=")[1][:-3]) for k_, v in scan.items() if v["passes"]["rC>=1Mpc"]})
n_kids = sum(1 for v in scan.values() if v["passes"]["efe"] and v["passes"]["rC>=1Mpc"])
P(f"    KiDS alone: the external-field bound passes for mu^-1 in {efe_ok_mu} Mpc; r_C(MW) >= 1 Mpc for mu^-1 in {rc_ok_mu} Mpc")
OUT["numbers"]["kids_alone"] = {"efe_ok_mu_inv": efe_ok_mu, "rC_ok_mu_inv": rc_ok_mu, "both": n_kids}
check("S2 KiDS alone leaves no mu: its external-field bound needs a short Jeans length (mu^-1 <~ 0.3 Mpc), a MOND-like "
      "lens profile to ~1 Mpc needs a long one (mu^-1 >~ 10 Mpc; BS24 eq. 38)",
      f"{n_kids} of {len(scan)} grid points pass both; external field ok for mu^-1 <= {max(efe_ok_mu) if efe_ok_mu else None} Mpc, "
      f"r_C ok for mu^-1 >= {min(rc_ok_mu) if rc_ok_mu else None} Mpc", n_kids == 0,
      "the same mu sets the filter that hides the web's field (k_J = a mu) and the radius where the mu^2 term ends MOND "
      "(r_C); r_C is BS24's order-of-magnitude estimate, so this is a pincer with a factor ~30 gap in mu^-1, not a theorem",
      load_bearing=False)

# ============================================================================================ C4
banner("C4  CONTROL: remove the k-dependence of eq. 71 (c_s^2 -> c_ad^2 at every k) for benchmark A")
XA = Khronon(22.3, 1.0)
resA_flat = [grow(XA, kh, kdep=False) for kh in KH]
s8_flat, _, _, _ = spectra(XA, resA_flat)
P(f"    benchmark A: sigma_8 with eq. 71 = {bA['sigma8']:.3f};  with c_s^2 = c_ad^2 at all k = {s8_flat:.3f}")
check("C4 (documentary) with c_s^2 = c_ad^2 at every k (no cap from eq. 71) benchmark A's sigma_8 falls further: "
      "eq. 71 caps the pressure at the self-gravity level, so the suppression it gives is the cancellation, not more",
      f"eq. 71: {bA['sigma8']:.3f}; adiabatic: {s8_flat:.3f}", s8_flat < bA['sigma8'], load_bearing=False)
OUT["numbers"]["C4"] = {"sigma8_eq71": bA["sigma8"], "sigma8_adiabatic": s8_flat}

# ============================================================================================ VERDICT
banner("VERDICT")
n_ok = sum(1 for _, ok, _ in CH if ok); n_lb_fail = sum(1 for _, ok, lb in CH if (not ok) and lb)
P(f"""  The MOND function of BS24 reads the acceleration of the khronon congruence, A = grad Ups, which in their linear
  cosmology is the gradient of the khronon's OWN potential filtered by k^2/(k^2 + k_J^2) -- not the Newtonian field of
  the web that C-H/K's kernel reads.  At the KiDS lens redshift:
    benchmark A (mu^-1 = 22.3 Mpc): e = {bA['footings']['canonical']['e_web']:.2e} a0, x{bA['footings']['canonical']['over_bound']:.3g} the KiDS bound; sigma_8 = {bA['sigma8']:.3f}; r_C(MW) = {list(bA['r_C_Mpc_by_Mb'].values())[1]} Mpc
    benchmark B (mu^-1 = 223 kpc): e = {bB['footings']['canonical']['e_web']:.2e} a0, x{bB['footings']['canonical']['over_bound']:.3g} the KiDS bound; sigma_8 = {bB['sigma8']:.3f}; r_C(MW) = {list(bB['r_C_Mpc_by_Mb'].values())[1]} Mpc
  Scan: {n_all} of {len(scan)} (mu, lam_D) points pass the external-field bound, a 1 Mpc MOND-like lens profile and
  sigma_8 together.  LIMITS: linear theory for the web and for sigma_8 (nonlinear MOND growth excluded); the r_C
  criterion is BS24's order-of-magnitude eq. 38 (the full static profile: Mistele+2023 for AeST); the growth starts
  at z = 1000 with identical data for every model, so pre-recombination effects of the khronon are not included.""")
P(f"\n  {n_ok}/{len(CH)} checks pass; load-bearing failures: {n_lb_fail}; wrote {SLUG}_results{'_MUTATE' if MUTATE else ''}.json"
  f" ({time.time() - T0:.0f} s)")
outname = f"{SLUG}_results{'_MUTATE' if MUTATE else ''}.json"
json.dump(OUT, open(os.path.join(HERE, outname), "w"), indent=1, default=str)
sys.exit(1 if n_lb_fail else 0)
