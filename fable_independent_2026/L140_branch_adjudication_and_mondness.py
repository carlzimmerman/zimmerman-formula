#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
fbA1 -- WHICH a0(z) DOES THE FRAMEWORK ACTUALLY IMPLY, and where is the universe MOND?
======================================================================================
TASK 0 (adjudicate) + TASK 1 (the MOND scale through cosmic history).

THE FORK, stated precisely.  The framework's scale is a0 = kappa c sqrt(G rho), kappa = 1/2 (FITTED).
  BRANCH A   rho = rho_DE, the DARK-ENERGY density.  Equivalently a0 = c^2 sqrt(Lambda/32pi)
             = c H_Lambda / Z, Z = sqrt(32 pi/3).  If w = -1, rho_DE is a CONSTANT of nature and
             a0 is the SAME at every epoch, recombination included.
  BRANCH B   rho = rho_tot(z).  Since H^2 = 8 pi G rho_tot/3, this is IDENTICALLY a0 = c H(z)/Z,
             i.e. a0(z) = a0(0) E(z), ~2.3e4 x larger at recombination.
The two are the SAME formula with a different rho.  This script settles which one the derivation
gives, then computes both.

Sub-laws inside branch A that the repository also carries, both computed here:
  A0  w = -1 exactly            -> a0(z) = const.
  A1  DESI CPL evolving DE      -> a0 propto sqrt(rho_DE(z)), a mild BUMP-then-DECLINE.
  A2  the stage-17 "switch-off" law from the DBI clock potential,
      a0(z)/a0(0) = [sqrt(1+nu0^2)/sqrt(1+nu0^2 (1+z)^6)]^(1/2), nu0 in [2.14e-5, 1.77e-4].
      This DECLINES above z ~ 20 and is ~0.002-0.006 of today's value at recombination.

WHAT IS "THE ACCELERATION" OF A COSMOLOGICAL PERTURBATION MODE -- stated before any number.
  The operative arm of this programme is modified GRAVITY (AQUAL/QUMOND: the Poisson equation is
  modified, div[mu(|grad Phi|/a0) grad Phi] = 4 pi G rho).  The argument of the interpolating
  function is therefore the PECULIAR GRAVITATIONAL FIELD of the mode,
        g(k,z) = |grad Phi_N| = (k/a) c^2 |Phi(k,z)| = 4 pi G rhobar(z) delta(k,z) / k_phys ,
  the two forms being the same by Poisson.  This is a per-mode rms amplitude, not a point value.
  THREE ESTIMATORS THAT ARE NOT THIS ONE, named so they are not confused with it:
    * a0/(cH): a statement about the BACKGROUND horizon, not about any perturbation.  L121 used it.
    * Phi/lambda (lambda = 2pi/k): the same as g but with the 2pi of the gradient dropped -- a
      factor 6.28 low.  It produced a retracted "the CMB sits at the MOND transition" claim twice.
    * c_s^2/r_s: the PRESSURE acceleration of a fluid element.  That is the modified-INERTIA
      argument (the closed arm), and it is ~1e5 x larger at recombination.
  All four are printed at recombination so the reader can see the six-decade spread.

THE SOURCE FORK, which is where a sloppy argument goes wrong in EITHER direction:
  (S1) "with a dark sector": Phi is the LCDM potential (CDM + baryons + radiation).  This is the
       right source if the framework keeps its cold Omega_dm.  It makes g LARGE and MOND WEAK.
  (S2) "no dark matter": Phi is sourced by baryons + photons only.  Baryons cannot grow before
       recombination (photon pressure), so Phi is ~30x smaller and MOND is much STRONGER.
  Using (S1) to declare "MOND is off at recombination" while ALSO claiming MOND replaces the dark
  matter is circular.  Both are computed.  (S2) is done analytically here from the EXACT
  radiation-era self-gravitating solution and is redone with a full tight-coupling integration in
  fbB2; the two are cross-checked.

Both a0 footings (canonical 9.3619e-11, alt 1.1279e-10) carried everywhere.  Every check ASSERTS a
statement and CAN fail.
"""
import math, sys, time
import numpy as np
from scipy.integrate import quad, solve_ivp

T0 = time.time(); FAILS = []; NC = [0]
def check(name, ok, detail=""):
    NC[0] += 1
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f"   ({detail})" if detail else ""), flush=True)
    if not ok: FAILS.append(name)
def sec(t): print("\n" + "=" * 118); print(t); print("=" * 118, flush=True)
def info(s): print("  " + s, flush=True)

# ------------------------------------------------------------------ constants / cosmology (Planck 2018 TT,TE,EE+lowE+lensing)
c    = 2.99792458e8
G    = 6.67430e-11
Mpc  = 3.0856775814913673e22
h    = 0.6736
H0   = 100.0 * h * 1e3 / Mpc
om_b, om_c = 0.02237, 0.1200
Ob, Oc = om_b / h**2, om_c / h**2
T_CMB = 2.7255; N_eff = 3.046
# radiation
sigma_sb = 5.670374419e-8
rho_g = 4 * sigma_sb * T_CMB**4 / c**3          # photon mass-density today
rho_crit0 = 3 * H0**2 / (8 * math.pi * G)
Og = rho_g / rho_crit0
Onu = N_eff * (7.0/8.0) * (4.0/11.0)**(4.0/3.0) * Og
Or = Og + Onu
Om = Ob + Oc
OL = 1.0 - Om - Or
ns, As, kpiv = 0.965, 2.1e-9, 0.05          # kpiv in 1/Mpc
A0 = {"canonical": 9.3619e-11, "alt": 1.1279e-10}
Zc = math.sqrt(32 * math.pi / 3.0)
z_rec = 1089.9

def E(z, om=Om, orr=Or, ol=OL):
    zp = 1.0 + z
    return math.sqrt(orr * zp**4 + om * zp**3 + ol)

print("=" * 118)
print("fbA1 -- branch adjudication (A: a0 locked to Lambda   vs   B: a0 tracks H) + the MOND-ness of the universe")
print("=" * 118, flush=True)
info(f"cosmology: h={h}, Om={Om:.4f} (Ob={Ob:.4f}, Oc={Oc:.4f}), Or={Or:.6e}, OL={OL:.4f}, T={T_CMB} K, N_eff={N_eff}")
info(f"footings: canonical {A0['canonical']:.4e}, alt {A0['alt']:.4e} m/s^2;  Z = sqrt(32pi/3) = {Zc:.5f}")

# ==================================================================================================
sec("PART A -- THE ADJUDICATION.  What does the framework's own derivation give?")
# ==================================================================================================
H_Lam = H0 * math.sqrt(OL)                      # the de Sitter (asymptotic) Hubble rate
L_dS  = c / H_Lam                               # = sqrt(3/Lambda) since Lambda = 3 H_Lam^2/c^2
rho_DE = OL * rho_crit0
a0_2pi = c**2 / (2 * math.pi * L_dS)            # the brief's stated form
a0_Z   = c * H_Lam / Zc                         # = (c/2) sqrt(G rho_DE)
a0_half_sqrt = 0.5 * c * math.sqrt(G * rho_DE)
info(f"H_Lambda = H0 sqrt(OL) = {H_Lam:.5e} 1/s;  L_dS = sqrt(3/Lambda) = c/H_Lambda = {L_dS/Mpc:.1f} Mpc")
info(f"a0 = c^2/(2 pi L_dS)            = {a0_2pi:.5e} m/s^2   (the brief's form; = c H_Lambda/2pi)")
info(f"a0 = (c/2) sqrt(G rho_DE)       = {a0_half_sqrt:.5e} m/s^2   (kappa = 1/2, the CANONICAL footing)")
info(f"a0 = c H_Lambda / Z             = {a0_Z:.5e} m/s^2   (identical to the line above)")
info(f"a0 = c H0 / Z  (rho = rho_tot today) = {c*H0/Zc:.5e} m/s^2   (the ALT footing)")

check("A-1  the two forms of the CANONICAL footing are the same number: (c/2)sqrt(G rho_DE) = c H_Lambda/Z, "
      "and it reproduces the committed canonical a0 to 1%",
      abs(a0_half_sqrt / a0_Z - 1) < 1e-12 and abs(a0_Z / A0["canonical"] - 1) < 0.01,
      f"(c/2)sqrt(G rho_DE) = {a0_half_sqrt:.5e} = c H_L/Z = {a0_Z:.5e};  committed {A0['canonical']:.4e} "
      f"(ratio {a0_Z/A0['canonical']:.4f})")
check("A-2  the brief's a0 = c^2/(2 pi L_dS) is NOT the framework's canonical footing: it is Z/(2pi) = 0.921 "
      "of it (8% low).  The framework's kappa = 1/2 is a DIFFERENT posit from the naive de Sitter-Unruh 1/2pi "
      "-- stated so no number here is quietly swapped for the other",
      abs(a0_2pi / a0_Z - Zc / (2 * math.pi)) < 1e-12 and abs(a0_2pi / a0_Z - 1) > 0.05,
      f"a0(2pi form)/a0(canonical) = {a0_2pi/a0_Z:.4f} = Z/2pi;  a0(2pi form) = {a0_2pi:.4e} m/s^2")
check("A-3  a0/(c H0): the scale IS a dark-energy-scale acceleration, order 1/2pi -- the framework's signature",
      0.10 < A0["canonical"] / (c * H0) < 0.25 and 0.10 < A0["alt"] / (c * H0) < 0.25,
      f"canonical {A0['canonical']/(c*H0):.4f}, alt {A0['alt']/(c*H0):.4f}, 1/2pi = {1/(2*math.pi):.4f}")
check("A-4  THE FORK IS LITERALLY 'WHICH rho': (c/2)sqrt(G rho_crit(z)) = c H(z)/Z identically, so branch B is "
      "branch A's own formula with rho_DE -> rho_tot(z).  Nothing else distinguishes them",
      abs(0.5 * c * math.sqrt(G * rho_crit0 * E(3.0)**2) / (c * H0 * E(3.0) / Zc) - 1) < 1e-12,
      "(c/2)sqrt(G rho_tot(z)) == c H(z)/Z to machine precision")
check("A-5  THE TWO COMMITTED FOOTINGS ARE THE FORK EVALUATED TODAY: alt/canonical = 1/sqrt(OL). The repository's "
      "'both footings' habit already carries branch A and branch B at z = 0; they only diverge backwards",
      abs((A0["alt"] / A0["canonical"]) / (1 / math.sqrt(OL)) - 1) < 0.01,
      f"alt/canonical = {A0['alt']/A0['canonical']:.4f}  vs  1/sqrt(OL) = {1/math.sqrt(OL):.4f}")

info("")
info("ADJUDICATION.  The derivation reads the scale off the DE SITTER HORIZON: L_dS = sqrt(3/Lambda), and")
info("Lambda is a constant of the action.  Every route the programme certifies (MacDowell-Mansouri SO(4,1),")
info("the de Sitter-Unruh quadrature, the conformal-SO(4,1) and gauge-Yang-Mills routes) forces the FORM")
info("a0 propto c^2 sqrt(Lambda) -- i.e. rho = rho_DE.  None of them contains rho_matter or rho_radiation.")
info("=> BRANCH A is what the derivation implies.  With w = -1 exactly, a0 is a CONSTANT for all time.")
info("BRANCH B (a0 propto H) requires replacing rho_DE by rho_tot -- a different posit, not the derivation,")
info("and the repository's own papers label it 'the rival rising branch'.")
def c_DM14(M, z):
    a = 0.520 + (0.905 - 0.520) * math.exp(-0.617 * z ** 1.21); b = -0.101 + 0.026 * z
    return 10 ** (a + b * math.log10(M * h / 1e12))
def f_nfw(cc): return math.log(1 + cc) - cc / (1 + cc)
def a_s_lcdm(z, M=1e12):
    cz, c0 = c_DM14(M, z), c_DM14(M, 0.0)
    return E(z) ** (4. / 3.) * (cz ** 2 / f_nfw(cz)) / (c0 ** 2 / f_nfw(c0))
_dexB, _dexL = math.log10(E(2.5)), math.log10(a_s_lcdm(2.5))
info(f"LCDM's own emergent halo acceleration scale: naive g_dagger ~ sqrt(G rho_crit(z)) gives EXACTLY E(z), "
     f"i.e. branch B's law; the full halo-structure law E^(4/3) c^2/f(c) gives {_dexL:+.3f} dex at z = 2.5 vs "
     f"branch B's {_dexB:+.3f}")
check("A-6  BRANCH B IS NOT A DISTINCTIVE PREDICTION -- but the statement must be made precisely.  Its law "
      "a0 propto H(z) is IDENTICALLY the naive LCDM expectation for the emergent halo scale, "
      "g_dagger ~ sqrt(G rho_crit(z)) propto H(z), so the LEADING scaling is shared with a dark-matter halo "
      "population and carries no distinctive content.  The two are NOT numerically identical: the full "
      "halo-structure law differs by %.3f dex at z = 2.5.  It is branch A (FLAT) that is the distinctive one, "
      "because LCDM has no way to make the scale constant" % abs(_dexB - _dexL),
      abs(math.sqrt(G * rho_crit0 * E(2.5)**2) / (math.sqrt(G * rho_crit0) * E(2.5)) - 1) < 1e-12
      and abs(_dexB - _dexL) > 0.1,
      f"sqrt(G rho_crit(z)) = E(z) sqrt(G rho_crit(0)) identically; but LCDM halo law {_dexL:+.3f} dex vs "
      f"branch B {_dexB:+.3f} dex at z = 2.5 (differ by {abs(_dexB-_dexL):.3f} dex)")

# ==================================================================================================
sec("PART B -- a0(z) for every law on the table, z = 0 to 3000, both footings")
# ==================================================================================================
# DESI DR2 CPL (arXiv:2503.14738-class): w0 = -0.702, wa = -0.72
W0, WA = -0.702, -0.72
def rho_DE_ratio_cpl(z):
    a = 1.0 / (1.0 + z)
    return a ** (-3 * (1 + W0 + WA)) * math.exp(-3 * WA * (1 - a))
NU0_FLOOR, NU0_CEIL = 2.14e-5, 1.77e-4
def a0r_A0(z):  return 1.0
def a0r_A1(z):  return math.sqrt(rho_DE_ratio_cpl(z))
def a0r_A2(z, nu0=NU0_FLOOR):
    nu = nu0 * (1.0 + z)**3
    return (math.sqrt(1 + nu0**2) / math.sqrt(1 + nu**2)) ** 0.5
def a0r_B(z):   return E(z)

LAWS = [("A0 w=-1 (a0 LOCKED to Lambda)", a0r_A0),
        ("A1 DESI CPL sqrt(rho_DE(z))",   a0r_A1),
        ("A2 stage-17 switch-off (floor)", lambda z: a0r_A2(z, NU0_FLOOR)),
        ("A2 stage-17 switch-off (ceil)",  lambda z: a0r_A2(z, NU0_CEIL)),
        ("B  a0 propto H(z) (RIVAL)",      a0r_B)]
zs_tab = [0, 0.5, 1, 2, 2.5, 3, 5, 10, 20, 30, 100, 1089.9, 3000]
print(f"    {'law':34s}" + "".join(f"{('z='+str(z)):>10s}" for z in zs_tab))
for nm, f in LAWS:
    print(f"    {nm:34s}" + "".join(f"{f(z):10.4g}" for z in zs_tab))
info("(entries are a0(z)/a0(0); multiply by 9.3619e-11 canonical or 1.1279e-10 alt)")
check("B-1  branch A in ALL its sub-laws gives a0(z_rec) <= a0(0): locked A0 = 1.000, CPL A1 = %.3f, stage-17 "
      "A2 = %.4f-%.4f.  Branch B gives a0(z_rec)/a0(0) = %.3e.  The branches differ by 4-7 ORDERS at "
      "recombination" % (a0r_A1(z_rec), a0r_A2(z_rec, NU0_CEIL), a0r_A2(z_rec, NU0_FLOOR), a0r_B(z_rec)),
      a0r_A1(z_rec) <= 1.0 and a0r_A2(z_rec, NU0_FLOOR) < 0.01 and a0r_B(z_rec) > 1e4,
      f"A0 1.000 | A1 {a0r_A1(z_rec):.4f} | A2 {a0r_A2(z_rec,NU0_CEIL):.5f}-{a0r_A2(z_rec,NU0_FLOOR):.5f} | B {a0r_B(z_rec):.3e}")
check("B-2  the stage-17 law reproduces the repository's banked a0(z_rec)/a0(0) = 0.0060 (floor) / 0.0021 (ceiling) "
      "to 3% -- an independent regression on the committed number",
      abs(a0r_A2(1090, NU0_FLOOR) / 0.0060 - 1) < 0.03 and abs(a0r_A2(1090, NU0_CEIL) / 0.00209 - 1) < 0.03,
      f"floor {a0r_A2(1090,NU0_FLOOR):.5f} (banked 0.0060), ceiling {a0r_A2(1090,NU0_CEIL):.5f} (banked 0.00209)")
CPL_FITS = [("DESI DR2 BAO+CMB+SN(P18)", -0.702, -0.72), ("DESI DR1 BAO+CMB+PantheonPlus", -0.827, -0.75),
            ("DESI DR2 BAO+CMB+DESY5", -0.752, -0.86), ("a deep-wa corner", -0.64, -1.27)]
_rat3 = []
for nm, w0, wa in CPL_FITS:
    a = 0.25; r = a ** (-3 * (1 + w0 + wa)) * math.exp(-3 * wa * (1 - a)); _rat3.append(math.sqrt(r))
    info(f"CPL {nm:34s} (w0={w0}, wa={wa}):  a0(3)/a0(0) = {math.sqrt(r):.3f}")
check("B-3  the CPL sub-law A1 DECLINES for EVERY published DESI CPL fit: a0(3)/a0(0) spans %.2f-%.2f, which "
      "BRACKETS the programme's published 0.74 (that number corresponds to a particular DESI fit, not to the "
      "one used above -- stated rather than tuned).  Under evolving dark energy branch A makes MOND WEAKER in "
      "the past, never stronger" % (min(_rat3), max(_rat3)),
      max(_rat3) < 1.0 and min(_rat3) <= 0.74 <= max(_rat3),
      f"a0(3)/a0(0) over published CPL fits = {min(_rat3):.3f}-{max(_rat3):.3f}; programme's published value 0.74")

# ==================================================================================================
sec("PART C -- the MOND-ness of a perturbation mode.  Definition, then numbers.")
# ==================================================================================================
# ---- Eisenstein & Hu 1998 no-wiggle transfer function (their eqs 26-31)
def T_EH98(k):                       # k in 1/Mpc
    theta = T_CMB / 2.7
    s = 44.5 * math.log(9.83 / (Om * h * h)) / math.sqrt(1 + 10 * (om_b) ** 0.75)   # Mpc/h
    alpha_g = 1 - 0.328 * math.log(431 * Om * h * h) * (Ob / Om) + 0.38 * math.log(22.3 * Om * h * h) * (Ob / Om) ** 2
    ks = k * s / h
    gamma_eff = Om * h * (alpha_g + (1 - alpha_g) / (1 + (0.43 * ks) ** 4))
    q = k * theta * theta / gamma_eff
    L = math.log(2 * math.e + 1.8 * q)
    C = 14.2 + 731.0 / (1 + 62.5 * q)
    return L / (L + C * q * q)

def Delta_Phi_LCDM(k, z):
    """rms Newtonian potential per ln k for the LCDM (dark-sector) source, matter-era normalisation,
       times the (D/a) suppression factor which carries both the radiation era and Lambda."""
    return 0.6 * math.sqrt(As) * (k / kpiv) ** ((ns - 1) / 2.0) * T_EH98(k) * gfac(z)

# growth D(a) with radiation, normalised so D/a -> 1 deep in matter domination
def _growth():
    def rhs(N, y):
        a = math.exp(N); Ez2 = Or / a**4 + Om / a**3 + OL
        dlnH = 0.5 * (-4 * Or / a**4 - 3 * Om / a**3) / Ez2
        return [y[1], 1.5 * (Om / a**3 / Ez2) * y[0] - (2 + dlnH) * y[1]]
    a_i = 1e-7
    sol = solve_ivp(rhs, (math.log(a_i), 0.0), [a_i, a_i], method="DOP853", rtol=1e-10, atol=1e-16, dense_output=True)
    return sol
_S = _growth()
def D_of_a(a): return float(_S.sol(math.log(a))[0])
_a_md = 1.0 / (1.0 + 50.0)
_norm = D_of_a(_a_md) / _a_md
def gfac(z):
    a = 1.0 / (1.0 + z)
    return (D_of_a(a) / a) / _norm

# ---- sound horizon
def R_bg(z): return 0.75 * (Ob / Og) / (1.0 + z)
def r_s(z):
    f = lambda zz: (c / math.sqrt(3 * (1 + R_bg(zz)))) / (H0 * E(zz))
    return quad(f, z, 1e8, limit=400)[0] / Mpc          # comoving Mpc

rs_rec = r_s(z_rec)
info(f"sound horizon r_s(z_rec = {z_rec}) = {rs_rec:.2f} Mpc   (Planck r_s(z_*) = 144.43 Mpc)")
check("C-0  CONTROL: the background reproduces Planck's sound horizon at last scattering to 2%, so every scale "
      "k = n pi / r_s below is the real acoustic scale",
      abs(rs_rec / 144.43 - 1) < 0.02, f"r_s = {rs_rec:.2f} Mpc vs Planck 144.43")
z_eq = Om / Or - 1
check("C-0b CONTROL: matter-radiation equality reproduced to 3%", abs(z_eq / 3402.0 - 1) < 0.03, f"z_eq = {z_eq:.0f}")

info("")
info("DEFINITION USED THROUGHOUT (modified-gravity arm, the operative one):")
info("     g(k,z) = (k/a) c^2 |Phi(k,z)| = 4 pi G rhobar delta / k_phys      [per-mode rms peculiar gravity]")
info("     y = g/a0 ;  MOND regime  <=>  y < 1 ;  boost nu(y) = g_true/g_N")
info("Two kernels carried: nu_simple (alpha=2, Milgrom 1983, the framework's post-2026-07-30 kernel) and")
info("nu_line (the a0-line g^2 = g_N^2 + a0 g_N, which the repository's growth scripts use).  Both -> 1/sqrt(y).")
def nu_simple(y): return math.sqrt((1 + math.sqrt(1 + 4 / y**2)) / 2.0)
def nu_line(y):   return math.sqrt(1 + 1 / y)
check("C-0c CONTROL: both kernels give nu -> 1 as y -> inf and nu sqrt(y) -> 1 as y -> 0",
      abs(nu_simple(1e8) - 1) < 1e-8 and abs(nu_line(1e8) - 1) < 1e-8
      and abs(nu_simple(1e-8) * math.sqrt(1e-8) - 1) < 1e-4 and abs(nu_line(1e-8) * math.sqrt(1e-8) - 1) < 1e-4,
      f"nu_simple(1e-8)sqrt(y) = {nu_simple(1e-8)*math.sqrt(1e-8):.6f}, nu_line = {nu_line(1e-8)*math.sqrt(1e-8):.6f}")

# regression against L37's committed table at z = 1100
def g_of(k, z, dphi): return (k / Mpc) * (1 + z) * c**2 * dphi
_l810_k = 0.05830
_dphi = 0.6 * math.sqrt(As) * (_l810_k / kpiv) ** ((ns - 1) / 2.0) * T_EH98(_l810_k)
_g810 = g_of(_l810_k, 1100.0, _dphi)
def T_BBKS(k):                                  # k in 1/Mpc ; Sugiyama-corrected shape (what L37 used)
    Gam = Om * h * math.exp(-Ob - math.sqrt(2 * h) * Ob / Om); q = (k / h) / Gam
    return math.log(1 + 2.34 * q) / (2.34 * q) * (1 + 3.89 * q + (16.1 * q) ** 2 + (5.46 * q) ** 3 + (6.71 * q) ** 4) ** (-0.25)
_g810_bbks = g_of(_l810_k, 1100.0, 0.6 * math.sqrt(As) * (_l810_k / kpiv) ** ((ns - 1) / 2.0) * T_BBKS(_l810_k))
info(f"transfer function at k = 0.0583/Mpc: EH98-no-wiggle {T_EH98(_l810_k):.4f}, BBKS {T_BBKS(_l810_k):.4f}, "
     f"L37's 0.1592 -- the fitting formulas disagree by 40% here")
check("C-1  REGRESSION on the committed L37 lane: at z = 1100, k = 0.0583/Mpc (l ~ 810, the third peak) this "
      "lane's LCDM-source peculiar gravity agrees with L37's 8.16e-10 m/s^2 within a factor 2, the whole spread "
      "being the transfer-function fitting formula (EH98-no-wiggle vs BBKS).  The verdict does not move: y stays "
      "well above 1 on every variant",
      0.5 < _g810 / 8.159e-10 < 2.0 and 0.7 < _g810_bbks / 8.159e-10 < 1.4
      and min(_g810, _g810_bbks) / A0["canonical"] > 3.0,
      f"EH98 {_g810:.3e} (ratio {_g810/8.159e-10:.2f}), BBKS {_g810_bbks:.3e} (ratio {_g810_bbks/8.159e-10:.2f}); "
      f"y_A = {_g810_bbks/A0['canonical']:.1f}-{_g810/A0['canonical']:.1f}")

# ---- the table: y at the horizon, sound-horizon and third-peak scales, vs z
sec("PART C1 -- SOURCE (S1) 'WITH A DARK SECTOR': Phi = the LCDM potential.  y = g/a0 vs z.")
print(f"    {'z':>8s} {'k_H':>10s} {'k_s':>10s} {'k_3':>10s} | {'y_H A':>9s} {'y_s A':>9s} {'y_3 A':>9s} |"
      f" {'y_H B':>9s} {'y_s B':>9s} {'y_3 B':>9s} | {'nu_3 A':>7s} {'nu_3 B':>7s}")
ZGRID = [0, 0.5, 1, 2, 3, 5, 10, 30, 100, 300, 1089.9, 2000, 3000]
rows = []
for z in ZGRID:
    a = 1 / (1 + z)
    kH = a * H0 * E(z) / c * Mpc              # comoving 1/Mpc
    ks = math.pi / r_s(z)
    k3 = 3 * math.pi / r_s(z)
    out = {}
    for tag, a0f in (("A", lambda zz: A0["canonical"]), ("B", lambda zz: A0["canonical"] * E(zz))):
        for lbl, kk in (("H", kH), ("s", ks), ("3", k3)):
            gg = g_of(kk, z, Delta_Phi_LCDM(kk, z))
            out[lbl + tag] = gg / a0f(z)
    rows.append((z, kH, ks, k3, out))
    print(f"    {z:8.1f} {kH:10.4g} {ks:10.4g} {k3:10.4g} | {out['HA']:9.3g} {out['sA']:9.3g} {out['3A']:9.3g} |"
          f" {out['HB']:9.3g} {out['sB']:9.3g} {out['3B']:9.3g} | {nu_line(out['3A']):7.3f} {nu_line(out['3B']):7.3f}")
info("k_H = aH/c (horizon), k_s = pi/r_s (first acoustic peak), k_3 = 3 pi/r_s (THIRD peak); all comoving 1/Mpc.")

r_rec = [r for r in rows if abs(r[0] - z_rec) < 1][0][4]
check("C1-a  WITH a dark sector, branch A: the third-peak mode at recombination is NEWTONIAN, y = %.1f, so the "
      "MOND boost there is only nu = %.3f (a %.1f%% correction).  A constant a0 does essentially nothing to the CMB"
      % (r_rec["3A"], nu_line(r_rec["3A"]), 100 * (nu_line(r_rec["3A"]) - 1)),
      r_rec["3A"] > 3.0 and nu_line(r_rec["3A"]) < 1.2,
      f"y_3(z_rec) = {r_rec['3A']:.2f}, nu_line = {nu_line(r_rec['3A']):.4f}, nu_simple = {nu_simple(r_rec['3A']):.4f}")
check("C1-b  WITH a dark sector, branch B: the same mode is DEEP MOND, y = %.2e, boost nu = %.0f.  Branch B does "
      "NOT leave the CMB alone -- it multiplies the gravitational source term by ~1e2" % (r_rec["3B"], nu_line(r_rec["3B"])),
      r_rec["3B"] < 1e-2 and nu_line(r_rec["3B"]) > 10,
      f"y_3(z_rec) = {r_rec['3B']:.3e}, nu_line = {nu_line(r_rec['3B']):.1f}, nu_simple = {nu_simple(r_rec['3B']):.1f}")
zz0 = rows[0][4]
check("C1-c  TODAY the horizon-scale mode is deep MOND on BOTH branches (they coincide at z = 0 by construction): "
      "y_H(0) = %.2e.  The MOND regime for cosmological perturbations is a LOW-redshift, LARGE-scale place" % zz0["HA"],
      zz0["HA"] < 1e-2, f"y_H(z=0) = {zz0['HA']:.3e}, nu = {nu_line(zz0['HA']):.1f}")

# where is the A-branch boundary y=1 ?
sec("PART C2 -- where the MOND/Newton boundary sits in the (k, z) plane [branch A, dark-sector source]")
def y_of(k, z, branch):
    a0v = A0["canonical"] * (E(z) if branch == "B" else 1.0)
    return g_of(k, z, Delta_Phi_LCDM(k, z)) / a0v
info("y(k) is NOT monotonic (g ~ k T(k) peaks near k ~ 0.04/Mpc), so the Newtonian region is an INTERVAL in k;")
info("the table gives the full k-range where y > 1 (Newtonian), and everything outside it is MOND.")
print(f"    {'z':>8s} | {'k_H':>10s} | {'Newtonian band  y>1  [1/Mpc]':>34s} | {'y at k_H':>10s} | {'max y':>9s}")
KG = np.logspace(-5, 1.7, 900)
NEWT_BANDS = {}
for z in [0, 0.5, 1, 2, 5, 30, 300, 1089.9, 3000]:
    yv = np.array([y_of(kk, z, "A") for kk in KG])
    kH = (1 / (1 + z)) * H0 * E(z) / c * Mpc
    above = yv > 1.0
    if not above.any():
        band = "(none: MOND at every k)"
    else:
        band = f"{KG[above][0]:.3g} .. {KG[above][-1]:.3g}"
    NEWT_BANDS[z] = band
    print(f"    {z:8.1f} | {kH:10.4g} | {band:>34s} | {y_of(kH, z, 'A'):10.3g} | {yv.max():9.3g}")
check("C2-a  on branch A the Newtonian band OPENS UP as z increases and is EMPTY at z <~ 5: at z = 0 the peak y "
      "over all k is %.3f, i.e. EVERY linear mode in the universe is in the MOND regime today, while at "
      "recombination a wide band of scales is Newtonian" % max(y_of(kk, 0, "A") for kk in KG),
      max(y_of(kk, 0.0, "A") for kk in KG) < 1.0 and max(y_of(kk, z_rec, "A") for kk in KG) > 5.0,
      f"max_k y(z=0) = {max(y_of(kk,0.0,'A') for kk in KG):.3f}; max_k y(z_rec) = {max(y_of(kk,z_rec,'A') for kk in KG):.1f}")
info("Read: on branch A the MOND regime for perturbations is a LARGE-SCALE / LOW-z corner.  At recombination it")
info("has retreated to scales larger than the horizon, where a quasi-static MOND limit is not even defined.")

# ==================================================================================================
sec("PART C3 -- SOURCE (S2) 'NO DARK MATTER': the exact radiation-era potential.  This is the honest source "
    "for the question 'can MOND replace CDM at the CMB?'")
# ==================================================================================================
# EXACT self-gravitating radiation-fluid solution (Newtonian gauge, no CDM, R->0):
#   Phi(k,eta) = 3 Phi_p [sin(x) - x cos(x)] / x^3,  x = k eta / sqrt(3)
def eta_of_z(z, om=Om, orr=Or, ol=OL):          # conformal time, comoving Mpc
    f = lambda zz: c / (H0 * E(zz, om, orr, ol)) / Mpc
    return quad(f, z, 1e9, limit=400)[0]
def Phi_rad(k, z, Phi_p, om, orr, ol):
    x = k * eta_of_z(z, om, orr, ol) / math.sqrt(3)
    return 3 * Phi_p * (math.sin(x) - x * math.cos(x)) / x**3

Om_nodm, OL_nodm = Ob, 1.0 - Ob - Or
eta_rec_nodm = eta_of_z(z_rec, Om_nodm, Or, OL_nodm)
eta_rec_lcdm = eta_of_z(z_rec, Om, Or, OL)
info(f"conformal time at z_rec:  LCDM {eta_rec_lcdm:.1f} Mpc   |   baryon-only (no CDM) {eta_rec_nodm:.1f} Mpc")
info(f"radiation/matter at z_rec: LCDM rho_m/rho_r = {Om*(1+z_rec)**3/(Or*(1+z_rec)**4):.2f}   |   "
     f"baryon-only {Ob*(1+z_rec)**3/(Or*(1+z_rec)**4):.2f}  (so the pure-radiation solution is a fair approximation there)")

info("")
info("The exact RD potential OSCILLATES inside a decaying envelope |Phi|_env = 3 Phi_p / x^2, x = k eta/sqrt(3),")
info("and passes through ZERO twice per acoustic cycle.  Both are reported: the ENVELOPE (the conservative,")
info("phase-independent number, which gives the SMALLEST boost) and the instantaneous value at z_rec.")
print(f"    {'peak n':>7s} {'k [1/Mpc]':>11s} {'x=k.eta/r3':>11s} {'|Phi|/Phi_p':>12s} {'env/Phi_p':>10s} |"
      f" {'y_inst A':>9s} {'y_env A':>8s} {'nu_env A':>9s} | {'y_env B':>10s} {'nu_env B':>9s}")
nodm_rows = []
def r_s_nodm(z):
    f = lambda zz: (c / math.sqrt(3 * (1 + R_bg(zz)))) / (H0 * E(zz, Om_nodm, Or, OL_nodm))
    return quad(f, z, 1e8, limit=400)[0] / Mpc
rs_nodm = r_s_nodm(z_rec)
for n in (1, 2, 3, 4, 5):
    k = n * math.pi / rs_nodm
    Phi_p = (3.0 / 5.0) * math.sqrt(As) * (k / kpiv) ** ((ns - 1) / 2.0)
    x = k * eta_rec_nodm / math.sqrt(3)
    ph_i = abs(Phi_rad(k, z_rec, 1.0, Om_nodm, Or, OL_nodm))
    ph_e = 3.0 / x**2
    g_i = g_of(k, z_rec, ph_i * Phi_p); g_e = g_of(k, z_rec, ph_e * Phi_p)
    yiA = g_i / A0["canonical"]; yeA = g_e / A0["canonical"]; yeB = g_e / (A0["canonical"] * E(z_rec))
    nodm_rows.append((n, k, ph_i, ph_e, g_i, g_e, yiA, yeA, yeB))
    print(f"    {n:7d} {k:11.4g} {x:11.4g} {ph_i:12.4g} {ph_e:10.4g} | {yiA:9.3g} {yeA:8.3g} {nu_line(yeA):9.3f} |"
          f" {yeB:10.3e} {nu_line(yeB):9.1f}")
info(f"(no-CDM sound horizon r_s = {rs_nodm:.1f} Mpc, vs LCDM {rs_rec:.1f} Mpc -- see fbB2 for what that alone does)")
info("NOTE the node structure: nu = sqrt(1+1/y) DIVERGES wherever the potential passes through zero, so a MOND")
info("boost applied to an OSCILLATING source is largest exactly where the source is weakest.  That is a sign/shape")
info("statement, not an amplitude one, and it is the crux of the third-peak question.")

y3_inst_A = nodm_rows[2][6]
y3_nodm_A = nodm_rows[2][7]; y3_nodm_B = nodm_rows[2][8]
check("C3-a  THE CORRECTION THAT MATTERS.  With NO dark matter the potential at recombination is ~30x smaller, so "
      "the third-peak mode sits at y = %.2f on branch A -- NOT y ~ 5-9 as the dark-sector source gives.  Branch A "
      "is at the MOND TRANSITION at recombination in a no-CDM universe, not safely Newtonian" % y3_nodm_A,
      y3_nodm_A < r_rec["3A"] / 3.0,
      f"y_3 no-CDM = {y3_nodm_A:.3f} vs y_3 with-CDM = {r_rec['3A']:.2f} (factor {r_rec['3A']/y3_nodm_A:.1f} apart)")
check("C3-b  ...and the boost that follows is nu = %.2f (line kernel) / %.2f (simple kernel) -- a tens-of-percent "
      "enhancement, NOT the factor ~6 that replacing CDM would need (omega_c/omega_b = %.2f)"
      % (nu_line(y3_nodm_A), nu_simple(y3_nodm_A), om_c / om_b),
      nu_line(y3_nodm_A) < 0.5 * (1 + om_c / om_b),
      f"nu_A = {nu_line(y3_nodm_A):.3f} / {nu_simple(y3_nodm_A):.3f};  CDM/baryon source ratio needed = {1+om_c/om_b:.2f}")
check("C3-c  on branch B the same mode is deep MOND with nu = %.0f -- far MORE than the ~6 needed.  Branch B does "
      "not fail for lack of amplitude; if it fails it must fail on SHAPE, SIGN or TIMING (that is fbB2's job)"
      % nu_line(y3_nodm_B),
      nu_line(y3_nodm_B) > 1 + om_c / om_b,
      f"nu_B = {nu_line(y3_nodm_B):.1f} >> {1+om_c/om_b:.2f}")

# ==================================================================================================
sec("PART C4 -- the four estimators at recombination, side by side, so they are never confused again")
# ==================================================================================================
kk3 = 3 * math.pi / rs_rec
g_mg   = g_of(kk3, z_rec, Delta_Phi_LCDM(kk3, z_rec))
g_lam  = g_mg / (2 * math.pi)
cs2    = c**2 / (3 * (1 + R_bg(z_rec)))
g_mi   = cs2 / (rs_rec * Mpc / (1 + z_rec))
print(f"    modified-GRAVITY, per-mode |grad Phi| (THE operative one)  g = {g_mg:.3e} m/s^2   -> y_A = {g_mg/A0['canonical']:8.3g}")
print(f"    same, no-CDM source (envelope)                             g = {nodm_rows[2][5]:.3e} m/s^2   -> y_A = {y3_nodm_A:8.3g}")
print(f"    Phi/lambda (the 2pi-dropped version; retracted twice)       g = {g_lam:.3e} m/s^2   -> y_A = {g_lam/A0['canonical']:8.3g}")
print(f"    modified-INERTIA, pressure acceleration c_s^2/r_s(phys)     g = {g_mi:.3e} m/s^2   -> y_A = {g_mi/A0['canonical']:8.3g}")
print(f"    BACKGROUND horizon criterion a0/(cH)                                                 -> {A0['canonical']/(c*H0*E(z_rec)):8.3g}")
check("C4-a  the estimators span >5 orders at recombination, so 'is the CMB MOND?' has NO answer until the "
      "estimator is named.  L121's a0/cH = 6e-6 is a BACKGROUND statement and does NOT license 'MOND is off' for "
      "the perturbations, which sit at y = 0.2-9 depending on the source",
      (g_mi / g_mg) > 1e3 and (A0["canonical"] / (c * H0 * E(z_rec))) < 1e-4,
      f"MI/MG = {g_mi/g_mg:.1e}; a0/cH = {A0['canonical']/(c*H0*E(z_rec)):.1e}; MG y range no-CDM..with-CDM = "
      f"{y3_nodm_A:.2f}..{r_rec['3A']:.2f}")

sec("VERDICT (fbA1)")
print(f"""
  ADJUDICATION.  The framework's derivation reads a0 off the DE SITTER HORIZON: a0 = kappa c sqrt(G rho_DE)
  = c H_Lambda/Z.  rho_DE, not rho_tot.  With w = -1 that is a CONSTANT OF NATURE: a0 at recombination equals
  a0 today.  => BRANCH A.  Branch B (a0 propto H) is the same formula with rho_tot substituted; the programme's
  own papers call it "the rival rising branch", and it is ALSO exactly what LCDM predicts for the emergent halo
  scale g_dagger ~ sqrt(G rho_crit(z)) -- so branch B is not a distinctive prediction at all, while branch A
  (flat) is.  Inside branch A the repository's stage-17 clock law makes a0 SMALLER still in the past
  (a0(z_rec)/a0(0) = {a0r_A2(1090,NU0_FLOOR):.4f}-{a0r_A2(1090,NU0_CEIL):.5f}), and the DESI-CPL reading gives {a0r_A1(3.0):.2f} at z = 3.
  Every branch-A sub-law makes MOND WEAKER in the early universe, never stronger.

  WHERE THE UNIVERSE IS MOND (per-mode |grad Phi| vs a0):
    branch A, with a dark sector : y_3(z_rec) = {r_rec['3A']:.1f}  -> boost {nu_line(r_rec['3A']):.3f}  (Newtonian; CMB untouched)
    branch A, NO dark matter     : y_3(z_rec) = {y3_nodm_A:.2f}  -> boost {nu_line(y3_nodm_A):.2f}   (AT the transition; a real but small effect)
    branch B, either source      : y_3(z_rec) = {y3_nodm_B:.1e} -> boost {nu_line(y3_nodm_B):.0f}    (deep MOND; the CMB is a different theory)
    today, horizon scale         : y_H(0)     = {zz0['HA']:.1e} -> boost {nu_line(zz0['HA']):.0f}    (both branches agree at z = 0)
  The MOND regime for cosmological perturbations is a LOW-z, LARGE-SCALE corner on branch A and EVERYWHERE on
  branch B.  Whether the branch-A boost at recombination ({nu_line(y3_nodm_A):.2f}x) or the branch-B boost ({nu_line(y3_nodm_B):.0f}x) can do CDM's
  job is a question about the acoustic driving, not about the amplitude alone.  fbB2 answers it.
""")
print("=" * 118)
if FAILS:
    print(f"fbA1 INCOMPLETE: {len(FAILS)}/{NC[0]} FAILED: {FAILS}"); sys.exit(1)
print(f"fbA1 COMPLETE: {NC[0]}/{NC[0]} checks PASS.   [{time.time()-T0:.1f}s]")
print("=" * 118)
