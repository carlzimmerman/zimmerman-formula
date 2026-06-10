#!/usr/bin/env python3
"""
agentH3: the banked kill-test gauntlet run NUMERICALLY on the superfluid-DM-class hybrid (Berezhiani-Khoury)
============================================================================================================
Pre-registered in agentH3_gauntlet.md (forks locked before this run). Tests here:
  T1  Cassini Q2 / solar-system ephemerides  (verified Desmond eq (10)-(12) q-integral machinery
      from agentD_dew_quadrupole.py, anchors re-validated; PLUS the direct in-system phonon force,
      which needs no EFE machinery at all)
  T2  the agentE solar-reflex budget (survival line s < 0.34 a0  <=>  quasi-steady anomalous solar
      response < 2.4e-15 m/s^2; agentE_solar_reflex.out [2],[9])
  T3  SPARC pooled RAR vs the McGaugh baseline (0.1953 dex unweighted at Y=0.5, framework a0;
      mi_f4_hostile_upsilon.out) -- phonon-only nu_ph(y) = 1 + y^{-1/2} at the PUBLISHED abar
  T5  the WB/DR4 knee (EFE velocity boost vs the banked fork mi_f4_widebinary_efe.out)
      + the m-band clash vs the non-Huygens spec sheet (NONHUYGENS_DOOR_SYNTHESIS.md item 3)
  (T4, the lensing type split, runs in agentH3_typesplit.py on the lens catalog.)

PUBLISHED PINS (transcribed in agentH3_gauntlet.md):
  B-K 2015  (arXiv:1507.01019): m=0.6 eV, Lambda=0.2 meV, alpha = 0.86(Lambda/meV)^(-2/3) ~ 2.51
            [their eq (60): alpha^{3/2} Lambda = sqrt(a0 M_Pl) ~ 0.8 meV]; MW condensate R ~ 158 kpc (eq 45);
            "in the vicinity of individual stars the phonon effective theory breaks down" (sec 3.2, no criterion).
  BFK 2018  (arXiv:1711.05748): m=1 eV, Lambda=0.05 meV, alpha=5.7, beta=2, sigma/m=0.01 cm^2/g;
            abar = alpha^3 Lambda^2 / M_Pl ~ 0.87e-10 m/s^2 (eqs 9, 49); MOND limit a_phi = sqrt(abar a_b)
            (eq 8); phonon eq (34)-(35) sourced by rho_b ONLY; R_T <~ 310 kpc (m/eV)^{-8/7} (M/1e12)^{1/7}
            (sigma/m)^{2/7} (near eq 25).
  Mistele 2021 (arXiv:2103.16954): cbar = 3 fbar_beta (a_theta/a0) (sqrt(alpha)/m) sqrt(a0 M_Pl),
            fbar_beta = 1/sqrt(3(beta-1)(beta+3)); "cbar = 375 km/s (a_theta/a0)" at BFK fiducial;
            V_crit_perp = cbar sqrt(2/(2+f_beta^2)), f_beta = (3-beta) fbar_beta;
            Cherenkov exclusion sqrt(alpha)/m in [0.34, 3.29] /eV at beta=2 -> BFK fiducial 2.4 /eV EXCLUDED.
  Cassini 2026 (arXiv:2602.17884): Q2 = (1.6 +/- 1.8)e-27 s^-2.
  Perihelion bounds (repo pins, agentA_f4_eccentric.py): Mercury 0.0+/-1.05, Mars -0.020+/-0.037,
            Saturn 0.05+/-0.20 mas/cy.
numpy/scipy only; every number reproducible.  Agent H3, 2026-06-10.
"""
import numpy as np
from scipy.optimize import brentq, minimize_scalar
from scipy import integrate
from scipy.integrate import solve_ivp
import glob, os

# --------------------------------------------------------------------------- constants (SI + natural)
c     = 2.99792458e8          # m/s
G     = 6.674e-11
Msun  = 1.989e30
AU    = 1.495978707e11
kpc   = 3.0857e19
Mpc   = 3.0857e22
hbar  = 1.054571817e-34       # J s
eVJ   = 1.602176634e-19       # J
hbarc_eVm = 1.9732698e-7      # eV m  (hbar c / eVJ)
MPL_eV = 2.435e27             # REDUCED Planck mass in eV (2.435e18 GeV)
GM_SUN = G*Msun
GM_JUP = 1.26686534e17        # m^3/s^2 (Juno; Durante+2020, repo-pinned in agentE)
H0 = 67.4e3/Mpc; OmL = 0.685; Lam = 3*OmL*H0**2/c**2
A0_FRAME = c**2*np.sqrt(Lam/(32*np.pi))   # 9.36e-11 framework footing (only used for banked baselines)
A0_CANON = 1.2e-10

def acc_SI_to_eV(a):   return a/c**2*hbarc_eVm          # acceleration as energy (natural units)
def acc_eV_to_SI(a):   return a/hbarc_eVm*c**2

# --------------------------------------------------------------------------- the two published fiducials
class SFDM:
    def __init__(self, name, m_eV, Lam_eV, alpha, beta=2.0, arxiv=""):
        self.name, self.m, self.Lam, self.alpha, self.beta, self.arxiv = name, m_eV, Lam_eV, alpha, beta, arxiv
        self.abar = acc_eV_to_SI(alpha**3*Lam_eV**2/MPL_eV)        # a0-analog, m/s^2  (BFK eq 9)
        self.sqrt_alpha_over_m = np.sqrt(alpha)/m_eV               # /eV  (Mistele's constrained combo)
        fb = 1.0/np.sqrt(3*(beta-1)*(beta+3))                      # fbar_beta
        self.fbar = fb; self.fbeta = (3-beta)*fb
        # cbar/c per unit (a_theta/abar)  [Mistele 2103.16954 sec 3]
        self.K = 3*fb*self.sqrt_alpha_over_m*np.sqrt(acc_SI_to_eV(self.abar)*MPL_eV)
    def cbar(self, atheta_over_abar):   return self.K*atheta_over_abar*c   # m/s

BFK  = SFDM("BFK-2018 fiducial", 1.0, 0.05e-3, 5.7,  arxiv="1711.05748")
BK15 = SFDM("B-K-2015 fiducial", 0.6, 0.2e-3,  0.86*(0.2)**(-2/3), arxiv="1507.01019")

# MW inputs
R0      = 8.2*kpc
V_SUN   = 233e3                                  # m/s (repo convention, agentD/agentA)
GBAR_MW = np.array([1.1e-10, 1.5e-10, 1.8e-10])  # baryonic Newtonian field at the Sun: bracket
                                                 # (McMillan-2017-class models .. McGaugh-RAR inversion)
RHO_LOC = 0.4e9*eVJ/c**2/1e-6                    # 0.4 GeV/cm^3 in kg/m^3 (local DM density, standard)

# banked comparators
Q2_C, Q2_S = 1.6e-27, 1.8e-27
PERI_BOUNDS = {'Mercury': ('INPOP15a-C2', 0.0, 1.05), 'Mars': ('EPM2011', -0.020, 0.037),
               'Saturn': ('INPOP15a-C2', 0.05, 0.20)}
PLANETS = {'Mercury': (0.38710*AU, 0.2056), 'Venus': (0.72333*AU, 0.0068), 'Earth': (1.0*AU, 0.0167),
           'Mars': (1.52371*AU, 0.0934), 'Jupiter': (5.2029*AU, 0.0484), 'Saturn': (9.5367*AU, 0.0539)}
AGENTE_ASUN   = 2.09e-7      # |a_sun| mean (agentE [2])
AGENTE_BUDGET = (0.34*9.36e-11)**2/(2*AGENTE_ASUN)   # quasi-steady anomalous solar response line
DATADIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "data", "sparc_data")

P = print

# =========================================================================== verified Q2 machinery
def q_milgrom_eN(eN, nu_one, vmax=80.0):
    """Desmond+2024 eq (12) [Milgrom 2009 QUMOND quadrupole], verbatim from the repo-verified
    agentD_dew_quadrupole.py -- EXCEPT eN is set DIRECTLY (the phonon sector is sourced by the
    baryonic Newtonian field, so the Newtonian-equivalent external field IS g_bar/abar; no inversion)."""
    def integrand(xi, v):
        D = eN*eN + v**4 + 2.0*eN*v*v*xi
        if D <= 0: return 0.0
        Y = np.sqrt(D)
        return (nu_one(Y) - 1.0)*(eN*(3*xi - 5*xi**3) + v*v*(1 - 3*xi*xi))/Y
    val, _ = integrate.dblquad(integrand, 0.0, vmax, lambda v: -1.0, lambda v: 1.0,
                               epsabs=1e-10, epsrel=1e-8)
    return 1.5*val

def q_milgrom(etilde, nu_one, vmax=80.0):
    eN = brentq(lambda e: e*nu_one(e) - etilde, 1e-8, max(1e3, 10*etilde), xtol=1e-14, rtol=1e-12)
    return q_milgrom_eN(eN, nu_one, vmax), eN

def Q2_from_q(a0, q):  return -(3.0*a0**1.5)/(2.0*np.sqrt(GM_SUN))*q

def boost_eta_eN(eN, nu_one):
    """Desmond eq (14): eta = nu_e (1 + (1/3) dln nu_e/dln eN), eN given directly."""
    nu_e = nu_one(eN); d = 1e-5
    dln = (np.log(nu_one(eN*(1+d))) - np.log(nu_e))/np.log(1+d)
    return nu_e*(1.0 + dln/3.0), nu_e

def sig_over(Q2):  return abs(Q2 - Q2_C)/Q2_S

# interpolation functions
def nu_rar_one(y):     return 1.0/(1.0 - np.exp(-np.sqrt(y)))
def nu_simple_one(y):  return 0.5 + np.sqrt(0.25 + 1.0/y)
def nu_ph_one(y):      return 1.0 + 1.0/np.sqrt(y)          # phonon sector: a_tot/a_b = 1 + sqrt(abar/a_b)

# =========================================================================== perihelion machinery
def dpomega_gauss(a, e, k_over_r=None, const_A=None, n_f=200000):
    """Apsidal precession per orbit from the Gauss planetary equation for a radial perturbation R(r):
       dpomega = sqrt(1-e^2)/(n a e) * Int (-R cos f) dt,  dt = r^2/h df.
       R = -k/r (attractive 1/r force, the phonon term) or R = +A (validation case)."""
    GM = GM_SUN; p = a*(1-e*e); h = np.sqrt(GM*p); n = np.sqrt(GM/a**3)
    f = np.linspace(0, 2*np.pi, n_f)
    r = p/(1+e*np.cos(f))
    R = (-k_over_r/r) if k_over_r is not None else np.full_like(r, const_A)
    integ = (-R*np.cos(f))*(r*r/h)
    return np.sqrt(1-e*e)/(n*a*e)*np.trapz(integ, f)

def dpomega_analytic_kr(a, e, k):
    """Closed form for R = -k/r:  dpom/orbit = (2 pi k a (1-e^2)/(GM e^2)) (1 - 1/sqrt(1-e^2))."""
    return 2*np.pi*k*a*(1-e*e)/(GM_SUN*e*e)*(1 - 1/np.sqrt(1-e*e))

def dpomega_analytic_const(a, e, A):
    """Closed form for R = +A const:  dpom/orbit = 2 pi A a^2 sqrt(1-e^2)/GM."""
    return 2*np.pi*A*a*a*np.sqrt(1-e*e)/GM_SUN

def dpomega_twobody(a, e, k, orbits=60):
    """Direct integration cross-check: 2-body + radial -k/r force; apsidal drift from the
    Laplace-Runge-Lenz vector angle."""
    GM = GM_SUN
    r0 = a*(1-e); v0 = np.sqrt(GM*(2/r0 - 1/a))
    def rhs(t, s):
        x, y, vx, vy = s
        r = np.hypot(x, y)
        ax = -GM*x/r**3 - k*x/r**2   # -k/r * rhat
        ay = -GM*y/r**3 - k*y/r**2
        return [vx, vy, ax, ay]
    Torb = 2*np.pi*np.sqrt(a**3/GM)
    sol = solve_ivp(rhs, [0, orbits*Torb], [r0, 0, 0, v0], rtol=1e-12, atol=1e-6, dense_output=True,
                    method='DOP853', max_step=Torb/50)
    # secular apsidal rate = linear fit to the (unwrapped, densely sampled) LRL angle,
    # which removes the within-orbit periodic libration that a 2-point measurement aliases
    t = np.linspace(0, orbits*Torb, 4000)
    x, y, vx, vy = sol.sol(t)
    r = np.hypot(x, y); L = x*vy - y*vx
    Ax = (vy*L)/GM - x/r; Ay = (-vx*L)/GM - y/r
    th = np.unwrap(np.arctan2(Ay, Ax))
    slope = np.polyfit(t, th, 1)[0]
    return slope*Torb

def mas_per_cy(dpom_per_orbit, a):
    Torb_yr = 2*np.pi*np.sqrt(a**3/GM_SUN)/(365.25*86400)
    return dpom_per_orbit*(100/Torb_yr)*180/np.pi*3600*1000

# =========================================================================== SPARC machinery (agentD loader)
def load_sparc(Yd=0.5, Yb=0.7):
    gN, go, sg = [], [], []
    for fn in sorted(glob.glob(os.path.join(DATADIR, "*_rotmod.dat"))):
        d = np.genfromtxt(fn)
        if d.ndim != 2 or d.shape[1] < 6: continue
        R = d[:, 0]*kpc; Vo = d[:, 1]*1e3; eV = d[:, 2]*1e3
        Vg = d[:, 3]*1e3; Vd = d[:, 4]*1e3; Vb = d[:, 5]*1e3
        V2 = Vg*np.abs(Vg) + Yd*Vd*np.abs(Vd) + Yb*Vb*np.abs(Vb)
        ok = (R > 0) & (Vo > 0) & (V2 > 0)
        gN.append(V2[ok]/R[ok]); go.append(Vo[ok]**2/R[ok])
        sg.append(2/np.log(10)*eV[ok]/Vo[ok])
    return np.concatenate(gN), np.concatenate(go), np.concatenate(sg)

def dex_scatter(nu_one, a0, gN, go, w=None):
    mod = np.log10(np.array([nu_one(g/a0) for g in gN])*gN)
    r = np.log10(go) - mod
    if w is None: return float(np.sqrt(np.mean(r**2)))
    return float(np.sqrt(np.sum(w*r**2)/np.sum(w)))

# =========================================================================== run
def main():
    P("#"*104)
    P("# agentH3 GAUNTLET -- superfluid-DM-class hybrid (Berezhiani-Khoury) vs the banked kill-tests")
    P("# pre-registered forks: agentH3_gauntlet.md (locked before this run)")
    P("#"*104)

    # ---------------- PART 0: pins reproduced from scratch (gate) ----------------
    P("\n" + "="*104); P("PART 0  published parameters reproduced from scratch (gate)"); P("="*104)
    for M in (BFK, BK15):
        P(f"  {M.name} (arXiv:{M.arxiv}): m={M.m} eV, Lambda={M.Lam*1e3:.2f} meV, alpha={M.alpha:.3f}, beta={M.beta:.0f}")
        P(f"    abar = alpha^3 Lambda^2/M_Pl = {M.abar:.3e} m/s^2"
          f"   [BFK eq49 quotes 0.87e-10; B-K calibrated to ~1.2e-10]")
        P(f"    alpha^(3/2) Lambda = {M.alpha**1.5*M.Lam*1e3:.3f} meV   [B-K eq60: ~0.8 meV]")
        P(f"    sqrt(alpha)/m = {M.sqrt_alpha_over_m:.3f} /eV ; cbar(a_theta=abar) = {M.cbar(1.0)/1e3:.1f} km/s"
          f"   [Mistele quotes 375 km/s for BFK]")
    ok_abar = abs(BFK.abar - 0.87e-10) < 0.02e-10 and abs(BFK.cbar(1.0)/1e3 - 375) < 10
    P(f"  GATE: abar and cbar reproduce the published values -> {'PASS' if ok_abar else 'FAIL'}")

    # ---------------- PART 1: geography ----------------
    P("\n" + "="*104); P("PART 1  geography: is the solar system inside the MW superfluid core?"); P("="*104)
    for (m, M, sm, lab) in [(1.0, 1e12, 0.01, "BFK fiducial (m=1 eV, sigma/m=0.01)"),
                            (0.6, 1e12, 0.01, "BFK formula at B-K m=0.6 eV")]:
        RT = 310*(m)**(-8/7)*(M/1e12)**(1/7)*(sm)**(2/7)
        P(f"  R_T <= 310 (m/eV)^-8/7 (M/1e12)^1/7 (sigma/m)^2/7 kpc = {RT:6.1f} kpc   [{lab}]")
    P(f"  B-K 2015 condensate radius (their eq 45 worked value, m=0.6 eV, Lam=0.2 meV): ~158 kpc")
    P(f"  BFK worked galaxy examples: 49-82 kpc (their eqs 51-52); MW-mass halo: tens-to-150 kpc")
    P(f"  Sun at R0 = {R0/kpc:.1f} kpc  ->  INSIDE the coherent phase by ~x6-19 in radius, ALL published configs.")
    P(f"  (MW M<~1e12/h: 'almost completely condensate' -- 1507.01019 eq 18 context.)")
    P(f"  => The phonon force EXISTS at the solar position; the solar system does NOT escape by geography.")

    # ---------------- PART 2: the screening-criterion chain ----------------
    P("\n" + "="*104); P("PART 2  the screening-criterion chain, computed from the published parameters"); P("="*104)
    P("  [B-K's published escape is one sentence: 'in the vicinity of individual stars the phonon EFT breaks")
    P("   down' (1507.01019 sec 3.2) -- no radius, no criterion. Computing every standard candidate:]")
    for M in (BFK, BK15):
        P(f"\n  --- {M.name} ---")
        ath = np.sqrt(M.abar*GBAR_MW)                       # local galactic phonon acceleration
        cb  = M.cbar(ath/M.abar)
        P(f"  local galactic a_theta = sqrt(abar g_bar) = {ath[0]:.2e}..{ath[2]:.2e} m/s^2"
          f"  (g_bar bracket {GBAR_MW[0]:.1e}..{GBAR_MW[2]:.1e})")
        P(f"  (a) LONGITUDINAL SOUND SPEED  cbar = {cb[0]/1e3:.0f}..{cb[2]/1e3:.0f} km/s ;"
          f"  V_sun = {V_SUN/1e3:.0f} km/s  ->  Mach {V_SUN/cb[2]:.2f}..{V_SUN/cb[0]:.2f}  SUBSONIC")
        P(f"      V_crit_perp = {0.98387*cb[0]/1e3:.0f}..{0.98387*cb[2]/1e3:.0f} km/s -> the naive Landau/supersonic")
        P(f"      screen does NOT engage at the solar circle (the Sun is ~x2 below the critical speed).")
        rdis = 2*GM_SUN/cb**2
        P(f"  (b) DISRUPTION BUBBLE (infall sqrt(2GM/r) > cbar): r_dis = {rdis[2]/AU:.4f}..{rdis[0]/AU:.4f} AU")
        P(f"      vs Mercury 0.387 AU: the bubble is x{0.387/(rdis[0]/AU):.0f}+ inside Mercury -- protects NOTHING")
        P(f"      planetary. (And structurally: the Sun's mass sources phonons in the INTACT region r > r_dis")
        P(f"      regardless -- excising a 0.01-AU core does not turn off the Sun-sourced phonon force at planets.)")
        lam_dB = 6.62607015e-34/(M.m*eVJ/c**2*V_SUN)
        ell    = (M.m*eVJ/c**2/RHO_LOC)**(1/3)
        P(f"  (c) COHERENCE: lambda_dB = {lam_dB*1e3:.2f} mm vs interparticle l = {ell*1e6:.1f} um ->"
          f" ratio {lam_dB/ell:.0f} >> 1: coherent at planetary radii (B-K's own premise holds there)")
        xi = hbar/(M.m*eVJ/c**2*cb[1])
        P(f"  (d) HEALING LENGTH xi = hbar/(m cbar) = {xi*1e3:.2f} mm -- no AU-scale decoherence scale exists")
        rM = np.sqrt(GM_SUN/M.abar)
        r_superlum = M.K*rM
        P(f"  (e) SUPERLUMINAL BREAKDOWN: around the Sun a_theta(r) = sqrt(abar GM)/r -> cbar(r) = c at")
        P(f"      r = {r_superlum/AU:.1f} AU: INSIDE this radius the published dispersion gives cbar > c --")
        P(f"      the non-relativistic phonon EFT is formally out of its domain for r < {r_superlum/AU:.1f} AU")
        P(f"      (Mercury..Saturn inside or at the edge). This is the one computed sense in which the EFT")
        P(f"      'breaks down near stars' -- but it removes PREDICTIVITY, not the force: the static background")
        P(f"      solution a_phi = sqrt(abar a_b) is what the theory offers, and perturbations about it are")
        P(f"      superluminal. No screening mechanism emerges from the published EFT at planetary radii.")
        P(f"  (f) CHERENKOV (published): exclusion sqrt(alpha)/m in [0.34, 3.29] /eV (beta=2, Mistele eq 17);")
        P(f"      this config: {M.sqrt_alpha_over_m:.2f} /eV -> {'EXCLUDED' if 0.34 < M.sqrt_alpha_over_m < 3.29 else 'allowed'}"
          f"  (stellar phonon Cherenkov losses; evaded only by the two-field variant, arXiv:2009.03003,")
        P(f"      whose STATIC force -- the thing the gauntlet tests -- is engineered to be the same).")

    # ---------------- PART 3: T1 Cassini / ephemerides ----------------
    P("\n" + "="*104); P("PART 3  T1: Cassini Q2 + direct ephemeris confrontation"); P("="*104)
    P("  -- T1a: the DIRECT in-system phonon force (face-value reading R1) --")
    P("  a_phi(r) = sqrt(abar GM_sun)/r  inside r_EFE = sqrt(GM/g_bar,ext); EFE transition:")
    for M in (BFK,):
        rEFE = np.sqrt(GM_SUN/GBAR_MW[1])
        P(f"    r_EFE = {rEFE/AU:.0f} AU (g_bar mid) -- all planets are DEEP inside the Sun-dominated phonon zone")
        k = np.sqrt(M.abar*GM_SUN)
        P(f"    k = sqrt(abar GM) = {k:.3e} m^2/s^2  (abar = {M.abar:.2e}, {M.name})")
        P(f"    {'planet':<9}{'a_phi [m/s^2]':>14}{'a_phi/g_N':>11}{'dpom [mas/cy]':>16}{'bound [mas/cy]':>17}{'over':>12}")
        for pl, (a, e) in PLANETS.items():
            aphi = k/a; gN = GM_SUN/a**2
            dp = dpomega_analytic_kr(a, e, k); mas = mas_per_cy(dp, a)
            if pl in PERI_BOUNDS:
                lab, c0, sg = PERI_BOUNDS[pl]
                over = abs(mas - c0)/(2*sg)
                P(f"    {pl:<9}{aphi:>14.2e}{aphi/gN:>11.2e}{mas:>+16.3e}  {lab} {c0:+.2f}+/-{sg:.2f}{over:>11.1e}x")
            else:
                P(f"    {pl:<9}{aphi:>14.2e}{aphi/gN:>11.2e}{mas:>+16.3e}{'':>17}{'':>12}")
        # validations of the precession machinery
        aS, eS = PLANETS['Saturn']
        d_an = dpomega_analytic_kr(aS, eS, k); d_nu = dpomega_gauss(aS, eS, k_over_r=k)
        d_tb = dpomega_twobody(aS, eS, k, orbits=60)
        P(f"    machinery validation (Saturn): analytic {d_an:+.4e}, Gauss-integral {d_nu:+.4e},"
          f" 2-body LRL {d_tb:+.4e} rad/orbit (ratio {d_tb/d_an:.3f}; 60-orbit fit -- the osculating-omega")
        P(f"    libration ~k/(g_N e) is x6 the per-orbit secular term, so short arcs alias it)")
        A = 1e-12
        v_an = dpomega_analytic_const(aS, eS, A); v_nu = dpomega_gauss(aS, eS, const_A=A)
        P(f"    validation (const radial A=1e-12): analytic {v_an:+.4e} vs Gauss {v_nu:+.4e} rad/orbit")
    P("\n  -- T1b: the EFE quadrupole proper (verified Desmond eq (10)-(12) machinery) --")
    P("  anchors (must reproduce agentD_dew_quadrupole.out PART 2):")
    for lab, nu1, a0, et, qexp, Qexp in [("RAR nu   ", nu_rar_one, A0_CANON, 2.15e-10/A0_CANON, -0.2720, 4.654e-26),
                                          ("simple nu", nu_simple_one, A0_CANON, 2.15e-10/A0_CANON, -0.2849, 4.876e-26)]:
        q, eN = q_milgrom(et, nu1)
        Q2 = Q2_from_q(a0, q)
        P(f"    {lab} a0=1.2e-10 etilde={et:.3f}: q={q:+.4f} (banked {qexp:+.4f})  Q2={Q2:+.3e} (banked {Qexp:+.3e})"
          f"  -> {'PASS' if abs(q-qexp)<3e-3 else 'FAIL'}")
    P("  phonon sector: nu_ph(y) = 1 + y^(-1/2) (the MOND form persists at ALL y; no Newtonian-restoration knee),")
    P("  e_N set DIRECTLY = g_bar,MW(R0)/abar (the phonon is sourced by baryons; no nu-inversion):")
    for M in (BFK, BK15):
        for gb in GBAR_MW:
            eN = gb/M.abar
            q = q_milgrom_eN(eN, nu_ph_one)
            Q2 = Q2_from_q(M.abar, q)
            eta, nu_e = boost_eta_eN(eN, nu_ph_one)
            tag = ""
            if gb == GBAR_MW[1]:
                q160 = q_milgrom_eN(eN, nu_ph_one, vmax=160.0)
                tag = f"  [vmax 80->160: dq/q = {abs(q160-q)/abs(q):.1e}]"
            P(f"    {M.name:<18} g_bar={gb:.1e} e_N={eN:5.2f}: q={q:+.4f}  Q2={Q2:+.3e} s^-2"
              f"  = {sig_over(Q2):5.1f} sigma over Cassini-2026; boost eta-1={eta-1:+.0%}{tag}")
    P("  exactness check: for the scale-free nu_ph - 1 = y^(-1/2) the substitution v -> sqrt(eN) w removes eN")
    P("  from the q-integral entirely; the coefficient is a pure number, q_ph = -3/7:")
    for eN in (0.5, 1.0, 2.0, 4.0):
        P(f"    eN={eN}: q_ph = {q_milgrom_eN(eN, nu_ph_one, vmax=200.0):.6f}   (-3/7 = {-3/7:.6f})")
    P("    [formulation caveat: the phonon statics are AQUAL-form; the repo-measured AQUAL/QUMOND ratio on")
    P("     mu_simple is 0.875 (agentD PART 4) -- a ~12% effect, immaterial at these sigma levels.]")
    P("  -- T1 screened reading R2: Q2_ph = 0, all rows above -> 0; passes trivially. But PART 2 shows NO")
    P("     computed criterion shuts the force off at planetary radii; the only computed breakdown (superluminal")
    P("     zone, ~10 AU) removes predictivity, not the force. R2 = 'escapes by incompleteness' (prereg T1 fork A).")

    # ---------------- PART 4: T2 solar reflex ----------------
    P("\n" + "="*104); P("PART 4  T2: the agentE solar-reflex budget"); P("="*104)
    P("  SfDM is force-based, not magnitude-keyed inertia: the reflex channel is the phonon force ON THE SUN")
    P("  sourced by Jupiter (r_J-modulated, the agentE carrier). Budget line (agentE [2],[9]):")
    P(f"    survival s < 0.34 a0  <=>  quasi-steady anomalous solar response < {AGENTE_BUDGET:.2e} m/s^2")
    dJ = PLANETS['Jupiter'][0]
    for M in (BFK,):
        g_loc = GM_SUN/dJ**2
        lo = (GM_JUP/dJ**2)*np.sqrt(M.abar/g_loc)     # EFE-suppressed (Jupiter phonon source in the Sun's field)
        hi = np.sqrt(M.abar*GM_JUP)/dJ                # isolated deep-MOND pair bracket
        P(f"  R1 face-value ({M.name}): delta_a_sun = {lo:.2e} (EFE-suppressed) .. {hi:.2e} (isolated) m/s^2")
        P(f"    over budget: x{lo/AGENTE_BUDGET:.1e} .. x{hi/AGENTE_BUDGET:.1e}")
        eJ = PLANETS['Jupiter'][1]
        P(f"    r_J-modulated fraction (Jupiter e={eJ}): pk-pk ~ {2*eJ*lo:.1e}..{4*eJ*hi:.1e} m/s^2 --")
        P(f"    the TIME-VARYING part alone is x{2*eJ*lo/AGENTE_BUDGET:.0e}+ over the line; not GM-absorbable")
        P(f"    (agentE: GM_J-absorbing fits are independently refuted by Juno at 20-1000x).")
    P("  R2 screened: delta_a_sun = 0 -> passes trivially (same incompleteness price as T1-R2).")

    # ---------------- PART 5: T3 SPARC ----------------
    P("\n" + "="*104); P("PART 5  T3: SPARC pooled RAR vs the McGaugh baseline"); P("="*104)
    P("  published-fit ledger first (the task premise corrected): BFK 1711.05748 fit TWO galaxies")
    P("  (IC 2574, UGC 2953; sec VII) and quote NO RAR scatter -- there is no published BFK SPARC-wide fit.")
    P("  The published SPARC-wide confrontation is Mistele+ 2201.07282 (169 galaxies): 'even the best fits ...")
    P("  unsatisfactory'; M/L 'unnatural dependence on size'; best fits sit in the NON-MOND regime; forcing the")
    P("  MOND regime -> strong-lensing tension. And 2009.03003: the MOND-limit condition fails (eps>=1) at r>~20 kpc.")
    P("  This run: the phonon-only skeleton nu_ph at the PUBLISHED abar (zero freedom), both Upsilon conventions:")
    for Yd in (0.5, 0.70):
        gN, go, sg = load_sparc(Yd=Yd, Yb=1.4*Yd)   # SPARC convention Y_bul = 1.4 Y_disk (mi_f4 scripts)
        w = 1.0/np.maximum(sg, 1e-3)**2
        base_u = dex_scatter(nu_rar_one, A0_FRAME, gN, go)
        base_w = dex_scatter(nu_rar_one, A0_FRAME, gN, go, w)
        exp_u = 0.1953 if Yd == 0.5 else 0.2095
        P(f"\n  Upsilon_disk = {Yd} ({len(gN)} points):")
        P(f"    McGaugh nu, framework a0 (banked baseline): unweighted {base_u:.4f} dex"
          f"  [mi_f4_hostile gate {exp_u}: {'PASS' if abs(base_u-exp_u)<0.002 else 'FAIL'}]"
          f"  (this-run weighted: {base_w:.4f})")
        base_uc = dex_scatter(nu_rar_one, A0_CANON, gN, go)
        P(f"    McGaugh nu, canonical a0=1.2e-10:           unweighted {base_uc:.4f} dex"
          f"  (per the #1 rule both footings shown)")
        for M in (BFK, BK15):
            u = dex_scatter(nu_ph_one, M.abar, gN, go)
            wv = dex_scatter(nu_ph_one, M.abar, gN, go, w)
            P(f"    SfDM phonon-only, published abar={M.abar:.2e} ({M.name.split()[0]}):"
              f" unweighted {u:.4f} dex (weighted {wv:.4f})  -> penalty {u-base_u:+.4f} unw")
        r = minimize_scalar(lambda la: dex_scatter(nu_ph_one, 10**la, gN, go),
                            bounds=(-11.5, -9.0), method='bounded')
        u_best = r.fun; a_best = 10**r.x
        P(f"    SfDM phonon-only, FREE abar fit: best abar = {a_best:.2e} -> {u_best:.4f} dex"
          f"  (penalty vs McGaugh {u_best-base_u:+.4f})")
        # high-acceleration overshoot diagnostic (the no-knee tail)
        mod = np.log10(np.array([nu_ph_one(g/BFK.abar) for g in gN])*gN)
        res = mod - np.log10(go)
        for ycut in (10, 100):
            m = gN/BFK.abar > ycut
            if m.sum() > 10:
                P(f"    high-acceleration overshoot (y > {ycut}, N={m.sum()}): model-data = {np.mean(res[m]):+.4f} dex"
                  f"  [the unscreened y^(-1/2) tail]")
        P(f"    [condensate gravity ADDS to g_obs at all radii -> can only worsen the overshoot as a one-function")
        P(f"     RAR; as a per-galaxy FIT it adds freedom -- that is what 2201.07282 ran, verdict above.]")

    # ---------------- PART 6: T5 WB / DR4 knee + the m-band clash ----------------
    P("\n" + "="*104); P("PART 6  T5: the WB/DR4 knee + the spec-sheet mass-band clash"); P("="*104)
    P("  No dedicated published SfDM wide-binary prediction exists (searched 2026-06-10; the WB literature")
    P("  covers MOND-as-gravity classes). Computed here from the published force law, both readings:")
    P("  R1 face-value: WB separations (2-30 kAU) sit OUTSIDE every computed breakdown scale (bubble ~0.01 AU,")
    P("  superluminal zone ~10 AU) and INSIDE r_EFE (~6000 AU partially) -- the EFE-saturated boost applies:")
    for M in (BFK, BK15):
        for gb in GBAR_MW:
            eN = gb/M.abar
            eta, nu_e = boost_eta_eN(eN, nu_ph_one)
            P(f"    {M.name:<18} g_bar={gb:.1e}: e_N={eN:5.2f}  force boost eta-1 = {eta-1:+.0%}"
              f"  velocity boost sqrt(eta)-1 = {np.sqrt(eta)-1:+.1%}")
    eta_mid, _ = boost_eta_eN(GBAR_MW[1]/BFK.abar, nu_ph_one)
    vb = np.sqrt(eta_mid)
    P(f"\n  DR4-fork placement (banked: F4 +2-4%, simple +13-16%, McGaugh +11-14% velocity):")
    P(f"    SfDM face-value: {vb-1:+.0%} velocity -- the LARGEST boost of any candidate on the board;")
    P(f"    DR3 placement (mi_f4_widebinary_efe Newton-MC medians 0.588/0.639; data 0.647+-0.02/0.816+-0.075):")
    P(f"    SfDM-shifted medians ~{0.588*vb:.3f}/{0.639*vb:.3f} -> bin-1 sits ~{(0.588*vb-0.647)/0.02:.0f} sigma")
    P(f"    ABOVE the data (contamination-degeneracy caveat rides); a DR4 clean null at ~3% kills it decisively.")
    P(f"    -> prereg T5 fork A: SfDM lands on the DETECTION branch of the DR4 fork, OPPOSITE F4.")
    P(f"  R2 maximally-screened: null branch (Newton-degenerate) -- requires the same uncomputed screen as T1-R2,")
    P(f"  now stretched from 10 AU to >30 kAU with no published mechanism at all.")
    P("\n  -- the m-band clash (flagged in the task; arithmetic, no fork) --")
    band = (1.3e-29, 1.6e-24)
    for M in (BFK, BK15):
        P(f"    {M.name}: m = {M.m} eV = {M.m/band[1]:.1e}x the spec band TOP ({band[1]:.1e} eV);"
          f" {np.log10(M.m/band[1]):.1f} decades above")
    m_clim = 1.0*BFK.cbar(np.sqrt(BFK.abar*GBAR_MW[1])/BFK.abar)/c   # m below which local cbar > c (at fixed abar, alpha)
    P(f"    forcing m into the band at fixed (abar, alpha): cbar ~ 1/m -> local cbar = c already at m = {m_clim:.1e} eV;")
    P(f"    at the band top (1.6e-24 eV) cbar/c ~ {m_clim/1.6e-24:.1e} -- the non-relativistic phonon EFT cannot")
    RT_band = 310*(1.6e-24)**(-8/7)
    P(f"    exist there; and R_T(m=1.6e-24 eV) = {RT_band:.1e} kpc vs horizon ~1.4e7 kpc ({np.log10(RT_band/1.4e7):.0f}")
    P(f"    decades past it) -- the collisional-thermalization picture is void: the band belongs to fuzzy-DM-class")
    P(f"    mechanisms, NOT the B-K superfluid. Conversely B-K's knee abar = alpha^3 Lambda^2/M_Pl is Lambda-set,")
    P(f"    m-free: the spec's DR4 knee-position discriminator (~5e-28 eV) cannot probe it, and B-K's a0 carries")
    P(f"    NO Lambda_cosmological tie (banked: 'a0 is a fitted phonon coupling, not cH').")

    P("\n" + "#"*104)
    P("# verdict assembly in agentH3_gauntlet.md")
    P("#"*104)

if __name__ == "__main__":
    main()
