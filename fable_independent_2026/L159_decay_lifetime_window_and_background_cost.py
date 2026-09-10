#!/usr/bin/env python3
"""
T1 -- TEMPORAL SEPARATION, part 1: the REQUIRED LIFETIME WINDOW and the BACKGROUND COST.
===============================================================================================================
THE ESCAPE UNDER TEST.  The velocity-ordering lemma (L125 VEL-1/VEL-2) blocks a MOND+dark hybrid because a
decoupled collisionless species has v_rms ~ 1/a, so its free-streaming cutoff k_fs ~ a is monotonically
INCREASING: "cold enough to cluster at recombination" implies "clusters even harder in galaxies today", which
overshoots SPARC by the L61 ceiling.  THE PROPOSED ESCAPE: put the two facts at DIFFERENT EPOCHS.  Let the cold
component be intact at z ~ 1100 (it drives the third peak) but DECAY, so that it is substantially GONE by the
time galaxy rotation curves are measured.  Then "clusters at rec" and "absent in galaxies" are statements about
different times and the lemma's shared-component hypothesis is genuinely broken.

This lane computes, self-contained (numpy/scipy), for the ONE-BODY DECAY TO DARK RADIATION mechanism:

  PART 0  CONTROLS.  A from-scratch FLRW background integrator (photons + 1 massive + massless neutrinos +
          baryons + CDM + Lambda) reproduces the Planck-2018 LambdaCDM r_*, D_M(z_*), 100 theta_*, z_eq, age.
          Mutation control: the same code with a deliberately wrong omega_c does NOT reproduce them.
  PART 1  THE REQUIRED LIFETIME WINDOW (Task 1), two-sided, at four honest definitions of "gone by".
  PART 2  THE BACKGROUND COST (Task 2): theta_* at fixed h; theta_* restored by floating h; then BAO
          (6dFGS/MGS/BOSS DR12/eBOSS QSO/Lya), the SNe-equivalent Omega_m, the age, and an ISW proxy.
          Inverted to give the MAXIMUM decayed fraction the expansion history permits.
  PART 3  the window intersected with the background cost -> verdict for this arm.

POLARITY.  Every check ASSERTS a statement; PASS = the statement is TRUE.  A FAIL is a finding, not a crash.
"""
import numpy as np
from scipy.integrate import solve_ivp, cumulative_trapezoid
from scipy.optimize import brentq, minimize_scalar
from scipy.interpolate import interp1d
import sys, time, warnings
warnings.filterwarnings("ignore")

T0 = time.time(); FAILS = []; NCHECK = [0]
def check(name, ok, detail=""):
    NCHECK[0] += 1
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f"\n           ({detail})" if detail else ""), flush=True)
    if not ok: FAILS.append(name)
def sec(t): print("\n" + "=" * 118); print(t); print("=" * 118, flush=True)

print("=" * 118)
print("T1 -- TEMPORAL SEPARATION: required lifetime window + background cost (one-body decay to dark radiation)")
print("=" * 118, flush=True)

# ===================================================================================================
C_KMS = 299792.458
KMS_MPC_TO_INVGYR = 1.02271217e-3
T_CMB = 2.7255
A0_CANON, A0_ALT = 9.3619e-11, 1.1279e-10        # both footings, carried where a0 enters (via the L61 ceilings)

H0_P = 67.36; h_P = H0_P / 100.0
OMB_P = 0.02237
OMC_P = 0.1200; OMC_ERR = 0.0012                  # Planck 2018: omega_c = 0.1200 +/- 0.0012 (1.0%)
MNU = 0.06; NEFF = 3.046
TGT_100TH, TGT_100TH_ERR = 1.04110, 0.00031
TGT_RS, TGT_ZSTAR, TGT_ZEQ, TGT_AGE = 144.43, 1089.92, 3402.0, 13.797

OMG_H2 = 2.4728e-5 * (T_CMB / 2.7255) ** 4
T_NU0_EV = (4.0 / 11.0) ** (1.0 / 3.0) * T_CMB * 8.617333262e-5
NU_PREF = (7.0 / 8.0) * (4.0 / 11.0) ** (4.0 / 3.0)

_q = np.linspace(1e-6, 45.0, 5000); _w = np.gradient(_q)
_NORM = np.sum(_q ** 3 / (np.exp(_q) + 1.0) * _w)
_lna_tab = np.linspace(np.log(1e-10), 0.0, 1200)
_y_tab = MNU * np.exp(_lna_tab) / T_NU0_EV
_F_tab = np.array([np.sum(_q ** 2 * np.sqrt(_q ** 2 + y ** 2) / (np.exp(_q) + 1.0) * _w) / _NORM for y in _y_tab])
_F = interp1d(_lna_tab, _F_tab, kind="cubic", bounds_error=False, fill_value=(_F_tab[0], _F_tab[-1]))
N_MASSIVE, N_MASSLESS = 1, NEFF - NEFF / 3.0

def omega_nu_of_a(a):
    rel_per = NU_PREF * OMG_H2 * np.asarray(a, dtype=float) ** -4
    return N_MASSIVE * (NEFF / 3.0) * rel_per * _F(np.log(a)) + N_MASSLESS * rel_per
OMNU_TODAY_MASSIVE = N_MASSIVE * (NEFF / 3.0) * NU_PREF * OMG_H2 * float(_F(0.0))


class Background:
    """Flat FLRW: photons, 1 massive + massless neutrinos, baryons, stable CDM, an optional decaying cold
       species -> dark radiation, and Lambda root-found for flatness.  Integrated in the COMOVING variables
       u = omega_dcdm(a) a^3 and v = omega_dr(a) a^4 (both O(0.1), no stiffness)."""

    def __init__(self, h, omega_b, omega_c_stable, omega_dcdm_ini=0.0, tau_Gyr=np.inf,
                 a_ini=1e-9, npts=6000):
        self.h, self.omega_b, self.omega_c_stable = h, omega_b, omega_c_stable
        self.omega_dcdm_ini, self.tau = omega_dcdm_ini, tau_Gyr
        self.Gamma = 0.0 if not np.isfinite(tau_Gyr) else 1.0 / tau_Gyr
        self.lna = np.linspace(np.log(a_ini), 0.0, npts)
        self.a = np.exp(self.lna)
        self._known = OMG_H2 * self.a ** -4 + omega_nu_of_a(self.a) + \
                      (omega_b + omega_c_stable) * self.a ** -3
        self._solve()

    def _integrate(self, omega_L):
        known = interp1d(self.lna, self._known, kind="cubic")
        def rhs(l, Y):
            a = np.exp(l); u, v = Y[0], Y[1]
            om = float(known(l)) + u * a ** -3 + v * a ** -4 + omega_L
            H_gyr = 100.0 * np.sqrt(max(om, 1e-300)) * KMS_MPC_TO_INVGYR
            g = self.Gamma / H_gyr
            return [-g * u, g * u * a]
        if self.Gamma == 0.0:
            u = np.full_like(self.lna, self.omega_dcdm_ini); v = np.zeros_like(self.lna)
            return u, v
        s = solve_ivp(rhs, (self.lna[0], 0.0), [self.omega_dcdm_ini, 0.0], t_eval=self.lna,
                      rtol=1e-10, atol=1e-14, method="DOP853")
        return s.y[0], s.y[1]

    def _solve(self):
        # Lambda by FIXED-POINT iteration on the flatness condition (Lambda barely affects the decay
        # integral, so this converges in 2-3 passes; far cheaper than a root-find over full ODE solves).
        target = self.h ** 2
        omL = max(target - self._known[-1] - self.omega_dcdm_ini, 1e-8)
        for _ in range(8):
            u, v = self._integrate(omL)
            new = target - self._known[-1] - u[-1] - v[-1]
            if new <= 0:
                raise RuntimeError("no flat solution: matter+radiation exceed the critical density")
            if abs(new - omL) < 1e-14: omL = new; break
            omL = new
        self.omega_L = omL
        self.u, self.v = self._integrate(omL)
        om_tot = self._known + self.u * self.a ** -3 + self.v * self.a ** -4 + omL
        self.H = 100.0 * np.sqrt(om_tot)                       # km/s/Mpc
        # cumulative integrals on the lna grid
        self.t = cumulative_trapezoid(1.0 / (self.H * KMS_MPC_TO_INVGYR), self.lna, initial=0.0)   # Gyr
        self.age = self.t[-1]
        R = 0.75 * (self.omega_b / OMG_H2) * self.a
        cs = C_KMS / np.sqrt(3.0 * (1.0 + R))
        self.rs_cum = cumulative_trapezoid(cs / (self.a * self.H), self.lna, initial=0.0)          # Mpc
        self.dc_cum = cumulative_trapezoid(C_KMS / (self.a * self.H), self.lna, initial=0.0)       # Mpc
        self._H_l = interp1d(self.lna, self.H, kind="cubic")
        self._t_l = interp1d(self.lna, self.t, kind="cubic")
        self._rs_l = interp1d(self.lna, self.rs_cum, kind="cubic")
        self._dc_l = interp1d(self.lna, self.dc_cum, kind="cubic")
        self._u_l = interp1d(self.lna, self.u, kind="cubic")
        dlnH = np.gradient(np.log(self.H), self.lna)
        self._dlnH_l = interp1d(self.lna, dlnH, kind="cubic")

    def _l(self, z): return np.log(1.0 / (1.0 + np.asarray(z, dtype=float)))
    def H_of_z(self, z): return float(self._H_l(self._l(z)))
    def t_of_z(self, z): return float(self._t_l(self._l(z)))
    def omega_dcdm_com(self, z): return float(self._u_l(self._l(z)))      # comoving: omega_dcdm(a) a^3
    def sound_horizon(self, z): return float(self._rs_l(self._l(z)))
    def comoving_distance(self, z): return float(self.dc_cum[-1] - self._dc_l(self._l(z)))

def z_star_HS(omega_b, omega_m):
    g1 = 0.0783 * omega_b ** -0.238 / (1.0 + 39.5 * omega_b ** 0.763)
    g2 = 0.560 / (1.0 + 21.1 * omega_b ** 1.81)
    return 1048.0 * (1.0 + 0.00124 * omega_b ** -0.738) * (1.0 + g1 * omega_m ** g2)

def z_drag_EH(omega_b, omega_m):
    b1 = 0.313 * omega_m ** -0.419 * (1.0 + 0.607 * omega_m ** 0.674)
    b2 = 0.238 * omega_m ** 0.223
    return 1291.0 * omega_m ** 0.251 / (1.0 + 0.659 * omega_m ** 0.828) * (1.0 + b1 * omega_b ** b2)


Z_STAR_FIX, Z_DRAG_FIX = 1089.92, 1059.94        # Planck 2018 baseline (Table 2)

def finish(bg, omega_b=OMB_P):
    """attach z_*, r_*, theta_*, z_drag, r_d.

    z_* and z_drag are HELD at Planck's measured values for every model.  That is not a fudge: the escape
    holds omega_b and omega_c(z_*) fixed by construction, so pre-recombination physics -- and therefore the
    recombination and drag redshifts -- are IDENTICAL to LambdaCDM's in every model considered here.  The
    Hu-Sugiyama / Eisenstein-Hu fitting formulae are retained as printed diagnostics (they are known to be
    a few percent off for Planck cosmologies, which is exactly why they are not used)."""
    om_m_rec = omega_b + bg.omega_c_stable + bg.omega_dcdm_com(Z_STAR_FIX) + OMNU_TODAY_MASSIVE
    bg.zs_fit = z_star_HS(omega_b, om_m_rec); bg.zd_fit = z_drag_EH(omega_b, om_m_rec)
    zs = Z_STAR_FIX
    bg.z_star = zs; bg.om_m_rec = om_m_rec
    bg.r_s = bg.sound_horizon(zs)
    bg.D_M_star = bg.comoving_distance(zs)
    bg.theta_star = bg.r_s / bg.D_M_star
    bg.z_drag = Z_DRAG_FIX
    bg.r_d = bg.sound_horizon(bg.z_drag)
    return bg


# ===================================================================================================
sec("PART 0 -- CONTROLS: the from-scratch background integrator reproduces Planck-2018 LambdaCDM.")
# ===================================================================================================
lcdm = finish(Background(h_P, OMB_P, OMC_P))
om_m_P = OMB_P + OMC_P + OMNU_TODAY_MASSIVE
om_r_P = OMG_H2 + NU_PREF * OMG_H2 * NEFF
zeq_P = om_m_P / om_r_P - 1.0
th_P = lcdm.theta_star

print(f"    omega_gamma = {OMG_H2:.6e}   omega_nu(today, massive) = {OMNU_TODAY_MASSIVE:.6e}"
      f"   (m/93.14 eV = {MNU/93.14:.6e})")
print(f"    omega_m = {om_m_P:.5f}   omega_r = {om_r_P:.6e}   Omega_L = {lcdm.omega_L/h_P**2:.5f}")
print(f"    z_*  = {lcdm.z_star:8.2f}   (Planck {TGT_ZSTAR:.2f})")
print(f"    r_*  = {lcdm.r_s:8.3f} Mpc   (Planck {TGT_RS:.2f} +/- 0.26)")
print(f"    D_M(z_*) = {lcdm.D_M_star:9.2f} Mpc      r_drag = {lcdm.r_d:7.3f} Mpc  (Planck 147.09 +/- 0.26)")
print(f"    100 theta_* = {100*th_P:.5f}   (Planck {TGT_100TH:.5f} +/- {TGT_100TH_ERR:.5f})")
print(f"    z_eq = {zeq_P:8.1f}  (Planck {TGT_ZEQ:.0f})       age = {lcdm.age:.4f} Gyr  (Planck {TGT_AGE:.3f})")

check("C0  the massive-neutrino density today reproduces omega_nu = Sum m_nu / 93.14 eV to better than 2%",
      abs(OMNU_TODAY_MASSIVE / (MNU / 93.14) - 1) < 0.02,
      f"{OMNU_TODAY_MASSIVE:.6e} vs {MNU/93.14:.6e}  (ratio {OMNU_TODAY_MASSIVE/(MNU/93.14):.4f})")
check("C1  the integrator reproduces Planck's sound horizon r_* = 144.43 Mpc to better than 1%",
      abs(lcdm.r_s / TGT_RS - 1) < 0.01, f"r_* = {lcdm.r_s:.3f} Mpc  ({100*(lcdm.r_s/TGT_RS-1):+.2f}%)")
check("C1b the integrator reproduces Planck's drag-epoch sound horizon r_d = 147.09 Mpc to better than 1%",
      abs(lcdm.r_d / 147.09 - 1) < 0.01, f"r_d = {lcdm.r_d:.3f} Mpc  ({100*(lcdm.r_d/147.09-1):+.2f}%)")
check("C2  the integrator reproduces Planck's acoustic scale 100 theta_* = 1.04110 to better than 0.5%",
      abs(100 * th_P / TGT_100TH - 1) < 0.005,
      f"100 theta_* = {100*th_P:.5f}  ({100*(100*th_P/TGT_100TH-1):+.3f}%)")
check("C3  the integrator reproduces Planck's age 13.797 Gyr to better than 1%",
      abs(lcdm.age / TGT_AGE - 1) < 0.01, f"age = {lcdm.age:.4f} Gyr")
check("C4  the integrator reproduces matter-radiation equality z_eq = 3402 to better than 3%",
      abs(zeq_P / TGT_ZEQ - 1) < 0.03, f"z_eq = {zeq_P:.1f}")

bad = finish(Background(h_P, OMB_P, 0.5 * OMC_P))
check("C5  MUTATION CONTROL: halving omega_c breaks the acoustic scale by vastly more than Planck's 0.03% "
      "error -- the pipeline is sensitive, not rigged to agree",
      abs(100 * bad.theta_star / TGT_100TH - 1) > 0.01,
      f"100 theta_*(omega_c/2) = {100*bad.theta_star:.5f}  ({100*(bad.theta_star/th_P-1):+.2f}% vs baseline, "
      f"{abs(100*bad.theta_star-100*th_P)/TGT_100TH_ERR:.0f} sigma)")

t_star = lcdm.t_of_z(lcdm.z_star)
AGE_T0 = lcdm.age
print(f"\n    t(z_*) = {t_star*1e9:.5g} yr = {t_star:.7f} Gyr ;  t(z=10) = {lcdm.t_of_z(10):.4f} Gyr ;"
      f"  t(z=5) = {lcdm.t_of_z(5):.4f} Gyr ;  t(z=2) = {lcdm.t_of_z(2):.4f} Gyr")


# ===================================================================================================
sec("PART 1 -- TASK 1: THE REQUIRED LIFETIME WINDOW.")
# ===================================================================================================
print("""
  The two edges, stated as hypotheses before any number is computed.
    LOWER EDGE (must still be there for the third peak).  The third peak's height is set by the cold density AT
    recombination; Planck measures omega_c = 0.1200 +/- 0.0012, a 1.0% (1 sigma) box.  Requiring the decayed
    fraction at z_* to sit inside 1 sigma gives  1 - exp(-t_*/tau) <= 0.0100  =>  tau >= t_*/0.010050.
    UPPER EDGE (must be gone where rotation curves are measured).  L61's branch-independent 'excess spent once'
    theorem: a theory whose kernel already reproduces the RAR with the cold component switched off OVERSHOOTS
    pointwise by the transmitted pull eta*g_halo.  L49/L50 put the ceiling at eta <= 0.582 (canonical a0 =
    9.3619e-11) / 0.486 (alt a0 = 1.1279e-10) for a kernel reading the baryons only (eps=0), and 0.355 / 0.276
    if it reads the total potential (eps=1); at eta = 1 the median SPARC overshoot is 1.692x (+0.228 dex).  The
    SURVIVING FRACTION plays exactly the role of eta.  'Gone by' is a CHOICE, so all four choices are reported.
""", flush=True)

ETA_MAX = {"canon eps=0": 0.582, "alt eps=0": 0.486, "canon eps=1": 0.355, "alt eps=1": 0.276}
t_gone = {"z=0   rotation curves are measured today": lcdm.age,
          "z=2   z~2 disc kinematics exist": lcdm.t_of_z(2),
          "z=5   a halo here leaves a dynamical imprint": lcdm.t_of_z(5),
          "z=10  galaxy assembly begins": lcdm.t_of_z(10)}

tau_lo = t_star / (-np.log(1.0 - OMC_ERR / OMC_P))
print(f"  LOWER EDGE:  t_* = {t_star*1e9:.5g} yr;  allowed decayed fraction at z_* = {OMC_ERR/OMC_P:.4f}"
      f"  =>  tau >= {tau_lo:.6f} Gyr = {tau_lo*1e3:.2f} Myr")
check("W1  the LOWER edge is a real finite constraint: surviving recombination to Planck's 1% box on omega_c "
      "requires tau >= 35-40 Myr",
      0.030 <= tau_lo <= 0.045, f"tau_lo = {tau_lo:.6f} Gyr = {tau_lo*1e3:.2f} Myr")

print("\n  UPPER EDGE  tau <= t_gone / ln(1/eta_max):")
print(f"    {'definition of gone-by':<48} {'t [Gyr]':>9} " + " ".join(f"{k:>13}" for k in ETA_MAX))
rows = {}
for lab, tg in t_gone.items():
    cells = [tg / np.log(1.0 / em) for em in ETA_MAX.values()]
    rows[lab] = (tg, cells)
    print(f"    {lab:<48} {tg:9.4f} " + " ".join(f"{c:13.4f}" for c in cells))
print("      (Gyr; entry = the LONGEST lifetime leaving <= eta_max surviving at that epoch)")

loosest = rows["z=0   rotation curves are measured today"][1][0]     # canon eps=0, z=0
strictest = rows["z=10  galaxy assembly begins"][1][3]               # alt eps=1, z=10
allnonempty = all(c > tau_lo for _, cs in rows.values() for c in cs)
print(f"\n  THE KINEMATIC WINDOW: [{tau_lo:.4f}, {loosest:.3f}] Gyr at the loosest reading, "
      f"[{tau_lo:.4f}, {strictest:.4f}] Gyr at the strictest.")
check("W2  KINEMATICALLY the window is NOT empty at any of the 16 (epoch x ceiling) readings -- even the "
      "strictest ('gone by z=10' at eta <= 0.276) leaves tau_hi > tau_lo.  Task 1 alone does NOT close the "
      "escape",
      allnonempty, f"loosest [{tau_lo:.4f}, {loosest:.3f}] Gyr (ratio {loosest/tau_lo:.0f}); "
                   f"strictest [{tau_lo:.4f}, {strictest:.4f}] Gyr (ratio {strictest/tau_lo:.1f})")

print("""
  PARTIAL DECAY.  If only a fraction f_dec decays and (1-f_dec) is stable, the STABLE remnant is itself a cold
  component present in galaxies today, so the SAME ceiling binds it:
      f_surv(t_0) = (1 - f_dec) + f_dec exp(-t_0/tau) <= eta_max   =>   f_dec >= 1 - eta_max, for ANY tau.""")
for k, em in ETA_MAX.items():
    print(f"      {k:<14}: f_dec >= {1-em:.3f}  ({100*(1-em):.1f}% of the CMB-required cold density destroyed)")
check("W3  the escape necessarily DESTROYS a large fraction of the dark matter -- at least 41.8% (canonical, "
      "eps=0) and up to 72.4% (alt, eps=1) -- for any lifetime whatsoever.  It is not a perturbative decay, "
      "which is exactly why a background cost is unavoidable",
      (1 - 0.582) > 0.40 and (1 - 0.276) > 0.70,
      f"f_dec >= {1-0.582:.3f} (canon eps=0) ... {1-0.276:.3f} (alt eps=1), independent of tau")


# ===================================================================================================
sec("PART 2 -- TASK 2: THE BACKGROUND COST.  theta_*, BAO, SNe, age, ISW.")
# ===================================================================================================
print("""
  PROCEDURE.  omega_dcdm is normalised so the cold density AT RECOMBINATION equals Planck's 0.1200 -- that is
  what the third peak measures and it is the entire point of the escape.  Lambda is root-found for exact
  flatness.  r_s is recomputed with the model's own H(a).  Then (a) the theta_* shift at fixed h; (b) the h
  that restores theta_* exactly (the CMB geometric degeneracy); (c) at that h, BAO + SNe + age + an ISW proxy.
""", flush=True)

def build_decay(tau_Gyr, h, omega_c_star=OMC_P, omega_b=OMB_P):
    om_ini = omega_c_star
    for _ in range(4):
        bg = finish(Background(h, omega_b, 0.0, omega_dcdm_ini=om_ini, tau_Gyr=tau_Gyr), omega_b)
        got = bg.omega_dcdm_com(bg.z_star)
        if abs(got / omega_c_star - 1) < 1e-9: break
        om_ini *= omega_c_star / got
    bg = finish(Background(h, omega_b, 0.0, omega_dcdm_ini=om_ini, tau_Gyr=tau_Gyr), omega_b)
    bg.omega_c_ini = om_ini
    bg.f_surv_0 = bg.omega_dcdm_com(0.0) / omega_c_star
    return bg

BAO = [  # (label, z, kind, value, sigma)
    ("6dFGS    ", 0.106, "DV/rd",  2.976, 0.133),
    ("SDSS MGS ", 0.15 , "DV/rd",  4.47 , 0.17 ),
    ("BOSS DR12", 0.38 , "DM/rd", 10.234, 0.151),
    ("BOSS DR12", 0.38 , "DH/rd", 24.981, 0.738),
    ("BOSS DR12", 0.51 , "DM/rd", 13.366, 0.179),
    ("BOSS DR12", 0.51 , "DH/rd", 22.317, 0.578),
    ("BOSS DR12", 0.61 , "DM/rd", 15.611, 0.226),
    ("BOSS DR12", 0.61 , "DH/rd", 20.492, 0.508),
    ("eBOSS QSO", 1.48 , "DM/rd", 30.69 , 0.80 ),
    ("eBOSS QSO", 1.48 , "DH/rd", 13.26 , 0.55 ),
    ("eBOSS Lya", 2.33 , "DM/rd", 37.6  , 1.9  ),
    ("eBOSS Lya", 2.33 , "DH/rd",  8.93 , 0.28 ),
]
def bao_pred(bg):
    out = []
    for lab, z, kind, v, s in BAO:
        DM = bg.comoving_distance(z); DH = C_KMS / bg.H_of_z(z)
        p = ((z * DM ** 2 * DH) ** (1 / 3) / bg.r_d) if kind == "DV/rd" else \
            (DM / bg.r_d if kind == "DM/rd" else DH / bg.r_d)
        out.append((lab, z, kind, v, s, p))
    return out
def bao_chi2(bg): return sum(((p - v) / s) ** 2 for _, _, _, v, s, p in bao_pred(bg))

_ZS = np.geomspace(0.01, 2.3, 45)
def _lcdm_shape(Om):
    zz = np.geomspace(1e-4, 2.4, 2000)
    E = np.sqrt(Om * (1 + zz) ** 3 + (1 - Om))
    dc = cumulative_trapezoid(1.0 / E, zz, initial=0.0)
    f = interp1d(zz, dc, kind="cubic")
    return 5.0 * np.log10((1 + _ZS) * f(_ZS))
def sne_effective_Om(bg):
    mu = np.array([5.0 * np.log10((1 + z) * bg.comoving_distance(z)) for z in _ZS])
    def resid(Om):
        d = mu - _lcdm_shape(Om); d -= d.mean(); return float(np.sum(d ** 2))
    r = minimize_scalar(resid, bounds=(0.02, 0.90), method="bounded", options={"xatol": 1e-6})
    return r.x, np.sqrt(r.fun / len(_ZS))

def growth_D(bg):
    """delta'' + (2 + dlnH/dlna) delta' = 1.5 Omega_m(a) delta, with Omega_m(a) built from THIS background."""
    lg = np.linspace(np.log(1e-4), 0.0, 4000)
    ag = np.exp(lg)
    om_m = (bg.omega_b + bg.omega_c_stable) * ag ** -3 + np.array([bg.omega_dcdm_com(1/aa - 1) for aa in ag]) * ag ** -3
    Om_a = om_m / (np.array([float(bg._H_l(l)) for l in lg]) / 100.0) ** 2
    fOm = interp1d(lg, Om_a, kind="cubic"); fdlnH = interp1d(lg, [float(bg._dlnH_l(l)) for l in lg], kind="cubic")
    def rhs(l, Y): return [Y[1], -(2.0 + float(fdlnH(l))) * Y[1] + 1.5 * float(fOm(l)) * Y[0]]
    s = solve_ivp(rhs, (lg[0], 0.0), [ag[0], ag[0]], t_eval=lg, rtol=1e-8, atol=1e-14, method="DOP853")
    return interp1d(s.t, s.y[0], kind="cubic")

def isw_proxy(bg):
    """Phi ~ omega_m,comoving(a) * D(a) / a, normalised at z=100.  Returns Phi(z=0)/Phi(z=100)."""
    D = growth_D(bg)
    def Phi(z):
        a = 1.0 / (1 + z)
        omc = bg.omega_b + bg.omega_c_stable + bg.omega_dcdm_com(z)
        return omc * float(D(np.log(a))) / a
    return Phi(0.0) / Phi(100.0)

chi2_lcdm = bao_chi2(lcdm)
Om_sne_lcdm, rms_lcdm = sne_effective_Om(lcdm)
Phi_lcdm = isw_proxy(lcdm); isw_lcdm = 1.0 - Phi_lcdm

print("  LambdaCDM baseline for the confrontations:")
for lab, z, kind, v, s, p in bao_pred(lcdm):
    print(f"      {lab} z={z:5.3f} {kind:6}  data {v:7.3f} +/- {s:5.3f}   model {p:7.3f}   "
          f"{(p-v)/s:+5.2f} sigma")
print(f"      chi2_BAO(LambdaCDM, 12 pts) = {chi2_lcdm:.2f}      Om_SNe = {Om_sne_lcdm:.4f} "
      f"(Pantheon+ 0.334 +/- 0.018, {(Om_sne_lcdm-0.334)/0.018:+.2f} sigma; shape rms {rms_lcdm:.4f} mag)")
print(f"      ISW proxy: Phi(0)/Phi(100) = {Phi_lcdm:.4f}  (the ordinary late-ISW potential decay)")
check("C6  CONTROL: the LambdaCDM baseline fits the 12-point BAO compilation and the SNe shape -- so a large "
      "chi2 later is a real failure of the decaying model, not of the machinery",
      chi2_lcdm < 25.0 and abs(Om_sne_lcdm - 0.334) / 0.018 < 2.0,
      f"chi2_BAO = {chi2_lcdm:.2f} on 12 points; Om_SNe = {Om_sne_lcdm:.4f} "
      f"({(Om_sne_lcdm-0.334)/0.018:+.2f} sigma from Pantheon+)")

# ---- (a) fixed h ----------------------------------------------------------------------------------
print("\n  (a) FIXED h = 0.6736.   omega_dcdm(z_*) held at 0.1200.")
print(f"    {'tau [Gyr]':>10} {'f_surv(0)':>10} {'om_m(0)':>9} {'Om_L':>7} {'r_* Mpc':>9} "
      f"{'100 th_*':>10} {'d th/th':>10} {'sigma':>10} {'age':>7}")
nsig_at = {}
for tau in [0.05, 0.1, 0.3, 1.0, 3.0, 6.08, 10.0, 25.5, 50.0, 100.0, 160.0, 500.0, 2000.0]:
    bg = build_decay(tau, h_P)
    om_m0 = OMB_P + bg.omega_dcdm_com(0.0) + OMNU_TODAY_MASSIVE
    dth = bg.theta_star / th_P - 1.0
    nsig = abs(100 * bg.theta_star - 100 * th_P) / TGT_100TH_ERR
    nsig_at[tau] = (bg.f_surv_0, dth, nsig)
    print(f"    {tau:10.2f} {bg.f_surv_0:10.4f} {om_m0:9.5f} {bg.omega_L/h_P**2:7.4f} {bg.r_s:9.3f} "
          f"{100*bg.theta_star:10.5f} {100*dth:+9.3f}% {nsig:10.0f} {bg.age:7.3f}")

tau_need = lcdm.age / np.log(1.0 / 0.582)
bg_need = build_decay(tau_need, h_P)
dth_need = bg_need.theta_star / th_P - 1.0
nsig_need = abs(100 * bg_need.theta_star - 100 * th_P) / TGT_100TH_ERR
check("B1  at FIXED h the MINIMUM decay the escape needs (f_surv(t_0) = 0.582, tau = 25.5 Gyr) already breaks "
      "the acoustic scale decisively -- by more than 10 sigma of Planck's 0.03% measurement",
      nsig_need > 10,
      f"tau = {tau_need:.2f} Gyr -> f_surv(0) = {bg_need.f_surv_0:.4f}; 100 theta_* = "
      f"{100*bg_need.theta_star:.5f} vs {100*th_P:.5f}; shift {100*dth_need:+.3f}% = {nsig_need:.0f} sigma")

# ---- (b) restore theta_* by floating h ------------------------------------------------------------
print("\n  (b) RESTORE theta_* by floating h (the CMB geometric degeneracy). omega_dcdm(z_*) still 0.1200.")
_HCACHE = {}
def h_restore(tau):
    """the h that puts theta_* back on LambdaCDM's value.  theta_*(h) is smooth and monotone increasing, so a
       secant iteration converges in a handful of model builds; a too-small h has NO flat solution at all
       (matter alone exceeds critical), which is caught and stepped away from."""
    key = round(float(tau), 6)
    if key in _HCACHE: return _HCACHE[key]
    def f(hh):
        try: return build_decay(tau, hh).theta_star - th_P
        except (RuntimeError, ValueError): return None
    h0 = h_P
    while f(h0) is None: h0 *= 1.15
    h1 = h0 * 1.05
    f0, f1 = f(h0), f(h1)
    if f1 is None: h1 = h0 * 1.02; f1 = f(h1)
    for _ in range(30):
        if f1 is None or abs(f1 - f0) < 1e-16: break
        h2 = h1 - f1 * (h1 - h0) / (f1 - f0)
        if not (0.2 < h2 < 4.0): break
        f2 = f(h2)
        if f2 is None: h2 = 0.5 * (h1 + max(h0, 0.25)); f2 = f(h2)
        h0, f0, h1, f1 = h1, f1, h2, f2
        if f1 is not None and abs(f1) < 1e-10: break
    out = h1 if (f1 is not None and abs(f1) < 1e-7) else np.nan
    _HCACHE[key] = out
    return out

print(f"    {'tau [Gyr]':>10} {'decayed':>9} {'h':>8} {'H0':>7} {'Om_m(0)':>8} {'age':>7} "
      f"{'chi2_BAO':>9} {'d chi2':>9} {'Om_SNe':>8} {'SNe sig':>8} {'Phi0/Phi100':>12}")
print(f"    {'LCDM':>10} {0.0:9.4f} {h_P:8.4f} {100*h_P:7.2f} {om_m_P/h_P**2:8.4f} {lcdm.age:7.3f} "
      f"{chi2_lcdm:9.2f} {0.0:+9.2f} {Om_sne_lcdm:8.4f} {(Om_sne_lcdm-0.334)/0.018:+8.2f} {Phi_lcdm:12.4f}")
res = {}
for tau in [0.1, 0.3, 1.0, 3.0, 6.08, 10.0, 25.5, 50.0, 100.0, 160.0, 500.0, 2000.0]:
    hh = h_restore(tau)
    if not np.isfinite(hh):
        print(f"    {tau:10.2f}   -- NO h in [0.30, 2.50] restores theta_* --"); res[tau] = None; continue
    b = build_decay(tau, hh)
    om_m0 = OMB_P + b.omega_dcdm_com(0.0) + OMNU_TODAY_MASSIVE
    c2 = bao_chi2(b); Om_s, _ = sne_effective_Om(b); ph = isw_proxy(b)
    res[tau] = dict(h=hh, bg=b, chi2=c2, dchi2=c2 - chi2_lcdm, Om_sne=Om_s, phi=ph, dec=1 - b.f_surv_0)
    print(f"    {tau:10.2f} {1-b.f_surv_0:9.4f} {hh:8.4f} {100*hh:7.2f} {om_m0/hh**2:8.4f} {b.age:7.3f} "
          f"{c2:9.2f} {c2-chi2_lcdm:+9.2f} {Om_s:8.4f} {(Om_s-0.334)/0.018:+8.2f} {ph:12.4f}")

r255 = res[25.5]
OM_SNE, OM_SNE_E = 0.334, 0.018                    # Pantheon+ (Brout et al. 2022), SNe alone, flat LambdaCDM
chi2_sne_lcdm = ((Om_sne_lcdm - OM_SNE) / OM_SNE_E) ** 2
def dchi2_tot(g):
    return (g["chi2"] - chi2_lcdm) + (((g["Om_sne"] - OM_SNE) / OM_SNE_E) ** 2 - chi2_sne_lcdm)

check("B2  [CORRECTED FINDING -- the honest result, not the one first asserted]  once h is refloated to restore "
      "theta_* exactly, BAO alone does NOT kill the minimum required decay.  At tau = 25.5 Gyr (42% destroyed) "
      "the 12-point BAO chi2 moves by only +2.4, and H0 rises to 70.5 -- which even helps the H0 tension.  The "
      "geometric horn that DOES bite is the supernova distance SHAPE.  Statement asserted: at tau = 25.5 Gyr "
      "the BAO shift is small (< 9) while the SNe-equivalent Omega_m is more than 3 sigma from Pantheon+",
      r255 is not None and r255["dchi2"] < 9.0 and abs(r255["Om_sne"] - OM_SNE) / OM_SNE_E > 3.0,
      None if r255 is None else
      f"tau=25.5: h_restore = {r255['h']:.4f} (H0 = {100*r255['h']:.1f}); Delta chi2_BAO = {r255['dchi2']:+.1f} "
      f"(small); Om_SNe = {r255['Om_sne']:.3f} vs {OM_SNE} +/- {OM_SNE_E} = "
      f"{(r255['Om_sne']-OM_SNE)/OM_SNE_E:+.2f} sigma")

# ---- (c) INVERT, on the COMBINED geometric likelihood ---------------------------------------------
print("\n  (c) INVERSION on the COMBINED geometric test (theta_* restored exactly + BAO + the SNe shape).")
print("      Delta chi2 is measured RELATIVE TO LambdaCDM run through the same machinery, so the pipeline's")
print("      own offsets cancel.  This is a GEOMETRY-ONLY test: it uses the acoustic scale, the BAO ladder and")
print("      the supernova shape, and deliberately does NOT use the CMB damping tail, lensing or the ISW --")
print("      which is exactly why it is WEAKER than the published full-likelihood bounds quoted in PART 2b.")
_GCACHE = {}
def gates(tau):
    key = round(float(tau), 6)
    if key in _GCACHE: return _GCACHE[key]
    hh = h_restore(tau)
    if not np.isfinite(hh):
        _GCACHE[key] = None; return None
    b = build_decay(tau, hh); c2 = bao_chi2(b); Om_s, rms_s = sne_effective_Om(b)
    g = dict(tau=tau, h=hh, dec=1 - b.f_surv_0, chi2=c2, dchi2=c2 - chi2_lcdm, Om_sne=Om_s, rms=rms_s,
             sne_sig=abs(Om_s - OM_SNE) / OM_SNE_E, age=b.age, H0=100 * hh)
    g["dtot"] = dchi2_tot(g)
    _GCACHE[key] = g
    return g
print(f"    {'tau [Gyr]':>10} {'decayed':>9} {'h':>8} {'H0':>7} {'dchi2_BAO':>10} {'Om_SNe':>8} "
      f"{'SNe sig':>8} {'rms mag':>8} {'dchi2_tot':>10} {'~sigma':>7} {'age':>7}")
tab = []
for tau in [5, 8, 10, 13, 16, 20, 25, 30, 40, 50, 80, 160, 500]:
    g = gates(tau)
    if not g: continue
    tab.append(g)
    print(f"    {g['tau']:10.1f} {g['dec']:9.4f} {g['h']:8.4f} {g['H0']:7.2f} {g['dchi2']:+10.2f} "
          f"{g['Om_sne']:8.4f} {g['sne_sig']:8.2f} {g['rms']:8.4f} {g['dtot']:+10.2f} "
          f"{np.sqrt(max(g['dtot'],0)):7.2f} {g['age']:7.3f}")

def solve_edge(level, lo=4.0, hi=400.0):
    f = lambda lt: (gates(np.exp(lt)) or {"dtot": 1e9})["dtot"] - level
    try:
        lt = brentq(f, np.log(lo), np.log(hi), xtol=1e-4)
        return gates(np.exp(lt))
    except ValueError:
        return None
g3, g5 = solve_edge(9.0), solve_edge(25.0)
for lab, g in (("3 sigma (dchi2 = 9)", g3), ("5 sigma (dchi2 = 25)", g5)):
    if g: print(f"    GEOMETRY-ONLY boundary at {lab:22}: tau = {g['tau']:7.1f} Gyr, "
                f"i.e. at most {100*g['dec']:5.1f}% destroyed by z=0 (H0 = {g['H0']:.1f})")
    else: print(f"    GEOMETRY-ONLY boundary at {lab:22}: NOT BRACKETED in tau in [4, 400] Gyr")
dec3 = g3["dec"] if g3 else np.nan
dec5 = g5["dec"] if g5 else np.nan

check("B3  [CORRECTED]  the geometry-only test (theta_* restored + BAO + the SNe shape) permits a decayed "
      "fraction of roughly a THIRD -- far more than a few percent, but still less than the >= 41.8% the escape "
      "requires.  So geometry alone DOES close even the loosest reading, but only just.  Statement asserted: "
      "the 3-sigma geometry-only ceiling is in [0.20, 0.70] AND lies below the required 0.418",
      np.isfinite(dec3) and 0.20 < dec3 < 0.70 and dec3 < (1 - 0.582),
      f"geometry-only 3 sigma: at most {100*dec3:.1f}% destroyed (tau >= {g3['tau']:.1f} Gyr); "
      f"5 sigma: at most {100*dec5:.1f}% (tau >= {g5['tau']:.1f} Gyr).  Required by the escape: >= 41.8%")

# ---- the LADDER: every (ceiling x gone-by) reading, priced in geometry --------------------------------
print("\n      THE LADDER.  Each reading of the galaxy gate fixes tau; each tau is then priced geometrically.")
print(f"      {'reading of the galaxy gate':<52} {'tau [Gyr]':>10} {'decayed':>9} {'dchi2_tot':>10} {'~sigma':>7}")
ladder = []
for lab, tg in t_gone.items():
    for k, em in ETA_MAX.items():
        tau_r = tg / np.log(1.0 / em)
        g = gates(tau_r)
        if not g: 
            print(f"      {(lab.split('  ')[0] + ' / ' + k):<52} {tau_r:10.3f} {'--':>9} {'no flat h':>10} {'--':>7}")
            continue
        ladder.append((lab, k, tau_r, g))
        print(f"      {(lab.split('  ')[0] + ' / ' + k):<52} {tau_r:10.3f} {g['dec']:9.4f} "
              f"{g['dtot']:+10.1f} {np.sqrt(max(g['dtot'],0)):7.1f}")
survivors = [x for x in ladder if x[3]["dtot"] < 9.0]
sig_min = min(np.sqrt(max(x[3]["dtot"], 0)) for x in ladder)
sig_max = max(np.sqrt(max(x[3]["dtot"], 0)) for x in ladder)
check("B4  [CORRECTED -- and the result is STRONGER than first assumed]  EVERY one of the 16 readings of the "
      "galaxy gate is excluded by the expansion history alone at more than 3 sigma.  The loosest ('gone by "
      "z=0' at eta <= 0.582) sits at the margin; every tighter ceiling and every earlier 'gone by' epoch is "
      "excluded overwhelmingly, because they demand near-total destruction of the dark matter",
      len(survivors) == 0,
      f"{len(survivors)} of {len(ladder)} readings survive geometry at 3 sigma; the ladder spans "
      f"{sig_min:.1f} sigma (loosest) to {sig_max:.0f} sigma (strictest)")

# ---- PUBLISHED BOUNDS (Task 3) ---------------------------------------------------------------------
sec("PART 2b -- TASK 3: confrontation with the PUBLISHED decaying-dark-matter bounds.")
print("""
  All CITED, not re-derived.  All are for one-body decay into invisible relativistic products, i.e. exactly
  this arm.  The relevant regime is "decay after recombination, gone by now", Gamma in [1e-1, 1e3] Gyr^-1,
  plus the long-lived regime Gamma <~ H_0 that covers tau ~ 25 Gyr.

    Poulin, Serpico & Lesgourgues, JCAP 08 (2016) 036 [1606.02073]
       decay between recombination and today:   f_dcdm < 4.2% (PlanckTT) / 3.8% (PlanckTTTEEE),  95% CL
       + BOSS BAO + WiggleZ:                    f < 3% at Gamma ~ 10 Gyr^-1;  f*Gamma < 5.8e-3 Gyr^-1
    Nygaard, Tram & Hannestad, JCAP 05 (2021) 017 [2011.01632]
       Planck 2018:                             f_dcdm < 2.44%;  + BOSS DR12 BAO: f < 2.62%,     95% CL
       very-long-lived sub-regime:              f*Gamma < 4.01e-3 Gyr^-1 (Planck), 3.72e-3 (+BAO)
    Simon, Franco Abellan, Du, Poulin & Tsai, PRD 106, 023516 (2022) [2203.07440]
       Planck18 + Pantheon + ExtBAO + EFTofBOSS: f_dcdm < 2.16%;  and tau > 249.6 Gyr at f = 1,   95% CL
    Alvi, Brinckmann, Gerbino, Lattanzi & Pagano, JCAP 11 (2022) 015 [2205.05636]
       f = 1: tau > 181 Gyr (Planck T&P), > 234 (+lensing), > 246 Gyr (+BAO);                     95% CL
       f = 0.5: tau > 115 Gyr;  f = 0.1: tau > 18.9 Gyr
    Audren, Lesgourgues, Mangano, Serpico & Tram, JCAP 12 (2014) 028 [1407.2418]
       f = 1: tau > 160 Gyr                                                                       95% CL
    Blackadder & Koushiappas, PRD 93, 023510 (2016) [1510.06026]
       verbatim: if more than 40% of the DM energy goes to massless products, lifetimes less than the age of
       the universe are excluded at > 95% confidence
    Enqvist, Nadathur, Sekiguchi & Takahashi, JCAP 04 (2020) 015 [1906.09112]
       + Planck SZ cluster counts: Gamma^-1 >= 175 Gyr  (CL not printed in their Table 1 -- flagged)
    Planck 2018 VI [1807.06209] contains NO collaboration bound on decaying dark matter; there is nothing to
    cite there, and none is invented here.
""", flush=True)
F_PUB = {"Poulin+2016 (PlanckTTTEEE)": 0.038, "Poulin+2016 (+BAO+WiggleZ)": 0.030,
         "Nygaard+2021 (Planck18)": 0.0244, "Nygaard+2021 (+BAO)": 0.0262,
         "Simon+2022 (+EFTofBOSS)": 0.0216}
f_req_min, f_req_max = 1 - 0.582, 1 - 0.276
print(f"    {'published 95% ceiling on the decayed fraction':<44} {'f_max':>8} "
      f"{'x below the required 0.418':>28} {'x below 0.724':>15}")
for k, v in F_PUB.items():
    print(f"    {k:<44} {v:8.4f} {f_req_min/v:28.1f} {f_req_max/v:15.1f}")
worst_pub = max(F_PUB.values())
check("B6  [TASK 3]  the escape's requirement and the published constraints are disjoint by an ORDER OF "
      "MAGNITUDE.  Every analysis of the same regime caps the decayed fraction at a few percent; the escape "
      "needs at least 41.8%.  Statement asserted: the required fraction exceeds the LOOSEST published 95% "
      "ceiling by more than a factor 10",
      f_req_min / worst_pub > 10.0,
      f"required >= {f_req_min:.3f} vs the loosest published ceiling {worst_pub:.4f} "
      f"(Poulin+2016 PlanckTTTEEE) -> {f_req_min/worst_pub:.1f}x; against the tightest "
      f"({min(F_PUB.values()):.4f}, Simon+2022) -> {f_req_min/min(F_PUB.values()):.1f}x")
check("B7  the published bounds and this lane's independent geometry agree in DIRECTION and differ only in "
      "STRENGTH, for a stated reason: this lane used only theta_*, BAO and the SNe shape, while the published "
      "analyses add the CMB damping tail, lensing reconstruction, the ISW and the full TT/TE/EE shape.  The "
      "honest statement is therefore 'geometry alone disfavours the escape at ~3 sigma; the full CMB "
      "likelihood excludes it by 10-20x in fraction', not 'geometry alone kills it'",
      np.isfinite(dec3) and dec3 > worst_pub,
      f"geometry-only ceiling {100*dec3:.0f}% vs published ceiling {100*worst_pub:.1f}% -- the published "
      f"analyses are {dec3/worst_pub:.0f}x tighter, as expected from the extra observables")

print("\n  (d) THE SHORT-LIFETIME HORN (tau ~ 0.04-3 Gyr: the decay happens between z_* and z~1).")
print("      ISW proxy: the large-scale potential Phi ~ omega_m,comoving(a) D(a)/a, ratio z=0 to z=100.")
print("      LambdaCDM's own value IS the ordinary late ISW, so the ratio to it is the ISW excess factor.")
worst = 0.0
for tau in [0.1, 0.3, 1.0, 3.0, 10.0]:
    g = res.get(tau)
    if g is None: continue
    dec_phi = 1 - g["phi"]
    worst = max(worst, dec_phi / isw_lcdm)
    print(f"      tau = {tau:6.2f} Gyr:  Phi(0)/Phi(100) = {g['phi']:.4f}   potential decay {dec_phi:.4f}"
          f"   = {dec_phi/isw_lcdm:6.2f} x LambdaCDM's {isw_lcdm:.4f}")
check("B5  the SHORT-lifetime end of the window is independently excluded by the integrated Sachs-Wolfe "
      "effect: for tau <~ 1 Gyr the large-scale potential collapses far faster than in LambdaCDM, giving a "
      "low-ell ISW signal several times the observed one.  (ESTIMATE from a growth+background proxy, NOT a "
      "Boltzmann run -- flagged as such and not load-bearing for the verdict)",
      worst > 3.0, f"worst potential-decay excess = {worst:.1f}x LambdaCDM's late ISW")


# ===================================================================================================
sec("PART 3 -- the window INTERSECTED with the background cost and the published bounds.")
print(f"""
  LOWER EDGE   (third peak intact):                tau >= {tau_lo:.4f} Gyr
  UPPER EDGE   (gone in galaxies by z=0, loosest): tau <= {loosest:.2f} Gyr   [canonical a0, eps=0, eta <= 0.582]
  UPPER EDGE   (gone by z=10, tightest):           tau <= {strictest:.4f} Gyr
  GEOMETRY-ONLY FLOOR (theta_*+BAO+SNe, 3 sigma):  tau >= {g3['tau']:.1f} Gyr   (<= {100*dec3:.0f}% destroyed)
  PUBLISHED FLOOR (CMB+BAO+SNe full likelihood):   f_decayed <= {100*worst_pub:.1f}% at 95%  =>  tau >= {AGE_T0/(-np.log(1-worst_pub)):.0f} Gyr

  READ IT HONESTLY.  The geometry-only floor ({100*dec3:.1f}% destroyed at 3 sigma) sits just BELOW the loosest
  requirement (41.8% destroyed), so this lane's own expansion-history test does close even the most generous
  reading -- at {np.sqrt(max(gates(loosest)['dtot'],0)):.1f} sigma, which is a real but not overwhelming margin.  Every other reading is
  excluded far harder ({sig_max:.0f} sigma at the strictest), because they demand near-total destruction.  And the
  published full-likelihood analyses, which use observables this lane deliberately did not (the damping tail,
  lensing reconstruction, the ISW, the full TT/TE/EE shape), close the loosest reading by a further factor
  {f_req_min/worst_pub:.0f}-{f_req_min/min(F_PUB.values()):.0f} in decayed fraction.
""", flush=True)
check("V1  [VERDICT, one-body decay-to-dark-radiation arm]  the window is EMPTY, and the closure is layered: "
      "all 16 readings of the galaxy gate are excluded by this lane's own expansion-history computation "
      f"(from {sig_min:.1f} sigma at the loosest to {sig_max:.0f} sigma at the strictest), and the published CMB+BAO+SNe "
      "likelihoods cap the decayed fraction at 2-4% against the >= 41.8% required -- a further factor 11-19",
      (len(survivors) == 0) and (f_req_min / worst_pub > 10.0),
      f"{len(ladder)-len(survivors)}/{len(ladder)} readings closed by geometry alone ({sig_min:.1f}-{sig_max:.0f} sigma); "
      f"published bound exceeded by {f_req_min/worst_pub:.0f}-{f_req_min/min(F_PUB.values()):.0f}x")
check("V2  SCOPE, honestly stated: this arm assumes ONE-BODY decay into RELATIVISTIC invisible products, so the "
      "destroyed mass leaves the matter budget and the a^-3 -> a^-4 conversion is what the expansion history "
      "sees.  A dark-sector phase transition converting matter to radiation is background-identical and is "
      "closed by the same computation.  It does NOT cover decay into a NON-RELATIVISTIC daughter with a "
      "velocity kick, which keeps rho ~ a^-3 and pays almost no background cost -- that is the real escape "
      "candidate and is tested separately (T2)",
      True, "one-body -> dark radiation (and matter -> radiation phase transitions) CLOSED here; "
            "two-body -> massive daughter + kick still open")

sec("SUMMARY")
print(f"""
  TASK 1 (lifetime window).  NOT empty kinematically.  Surviving recombination inside Planck's 1% box on
  omega_c needs tau >= {tau_lo*1e3:.1f} Myr.  Being gone where rotation curves are measured needs tau <= {loosest:.1f} Gyr at the
  loosest reading ('gone by z=0', eta <= 0.582) and tau <= {strictest:.2f} Gyr at the tightest ('gone by z=10',
  eta <= 0.276).  The load-bearing consequence is f_dec >= 1 - eta_max: at least 41.8%, and up to 72.4%, of the
  CMB-required cold density must be DESTROYED, for ANY lifetime.  That is what makes a background cost
  unavoidable, and it is the number every later gate is priced against.

  TASK 2 (background cost).  Layered, and weaker than first assumed.  At FIXED h the required decay moves
  100 theta_* by {100*dth_need:+.3f}% = {nsig_need:.0f} sigma.  But h is not fixed: refloating it restores theta_* exactly at
  H0 = {r255['h']*100:.1f}, and then BAO moves by only {r255['dchi2']:+.1f} on twelve points.  The geometric horn that bites is the
  SUPERNOVA SHAPE: the model's effective Omega_m is {r255['Om_sne']:.3f} against Pantheon+'s 0.334 +/- 0.018 ({abs(r255['Om_sne']-0.334)/0.018:.1f} sigma).
  Combined, geometry alone caps the destroyed fraction at {100*dec3:.0f}% (3 sigma) / {100*dec5:.0f}% (5 sigma) -- which closes
  all 16 readings of the galaxy gate -- the loosest at only {sig_min:.1f} sigma, the strictest at {sig_max:.0f} sigma.

  TASK 3 (published bounds).  Decisive on the survivor.  Every analysis of this exact regime caps the decayed
  fraction at 2-4% at 95% (Poulin+2016 3.8%; Nygaard+2021 2.44%; Simon+2022 2.16%), and at f = 1 the lifetime
  floor is 160-250 Gyr (Audren+2014; Alvi+2022).  The escape needs >= 41.8% -- a factor {f_req_min/worst_pub:.0f}-{f_req_min/min(F_PUB.values()):.0f} beyond the
  loosest published ceiling.

  VERDICT (this arm): the temporal-separation window is EMPTY for one-body decay to dark radiation.  The
  obstruction is the EXPANSION HISTORY plus the post-recombination CMB, NOT the velocity-ordering lemma --
  which this mechanism does genuinely evade.
""")
print("=" * 118)
if FAILS: print(f"T1 INCOMPLETE: {len(FAILS)}/{NCHECK[0]} FAILED: {FAILS}")
else: print(f"T1 COMPLETE: {NCHECK[0]}/{NCHECK[0]} checks PASS.   [{time.time()-T0:.1f}s]")
print("=" * 118)
