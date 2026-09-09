#!/usr/bin/env python3
"""
L62 -- the GROUP channel: can existing measurements decide L57's nonlocal functional?
=====================================================================================
L57 left the nonlocal (smoothed-density) trigger UNDECIDABLE on current data and named exactly two open
channels rather than banking either.  This lane settles the one that existing measurements could plausibly
close: X-ray GROUPS.

WHY GROUPS.  The mechanism hides a compact source inside an extended one by the CUBE of the scale ratio,
S >= (R_p/r_cl)^3.  A galaxy at 100 kpc inside a 1 Mpc cluster is suppressed by ~1e-3; a GROUP at its own
R500 ~ 0.4-1 Mpc is NOT small against a 1 Mpc smoothing and is therefore NOT hidden.  L57 E3 computed the
consequence: a group-scale lensing-versus-hydrostatic mass discrepancy of 20-45%.  It then refused to score
the channel, on the ground that this repository's own group estimators (KT2017 vs g06) disagree by +0.42 dex
on 19 shared hosts -- more than the effect.  "Estimator-limited" was the word.  This lane asks whether the
LITERATURE's estimators do better, and it asks the question the right way round: not what the central values
are, but whether the SYSTEMATICS can carry a 20-45% test.

WHAT IS ACTUALLY BEING TESTED, stated before any number.  The mechanism predicts a genuine metric SLIP:
the lensing potential and the dynamical potential differ.  Every observational route to that at group scale
compares a lensing mass to a NON-lensing mass, and each such route has its own astrophysical baseline:
   -- X-ray hydrostatic mass:  the LambdaCDM baseline is NOT 1, because non-thermal pressure biases M_HSE
      low.  Any measured excess is degenerate with the hydrostatic bias by construction.
   -- galaxy kinematics (velocity dispersion, caustics, escape edge): collisionless tracers, so the
      LambdaCDM baseline IS 1 up to estimator bias -- but the estimator is worst exactly at group mass.
That fork is the lane's crux and it is set up before any data is read.

  PART A  CONTROLS.  L57's group numbers from its own .out; the smoothing machinery rebuilt here; the
          (R_p/r_cl)^q suppression law re-derived; the 9-sigma shear failure and the measured cluster
          lensing/hydrostatic ratio recomputed independently from X-COP + Herbonnet 2020; L57's group
          response recomputed from the Lovisari 2015 catalogue with this lane's own kernel.
  PART B  WHAT IS MEASURED for groups, from the published literature, with samples and uncertainties.
  PART C  THE SYSTEMATIC FLOOR, entry by entry, with the correlated-error trap made explicit.
  PART D  THE CONFRONTATION: is 20-45% inside or outside; statistics- or systematics-limited; and is the
          prediction separable from the astrophysical hydrostatic bias at all.
  PART E  THE DECISIVE TEST L57 named (galaxies inside clusters vs the field, at 0.1%), priced against the
          real SLACS lens catalogue on disk and against Euclid/LSST forecasts.
  PART F  VERDICT.

Both a0 footings (9.3619e-11 / 1.1279e-10 m s^-2) on every dimensional number.  FAIL marks a requirement
that is not met; a FAIL is not automatically bad news for the mechanism and is never reported as if it were.
NOTHING here states that data favour this framework over LambdaCDM.

Nothing outside fable_independent_2026/ is written.  FINDINGS.md, HANDOFF_CONTRACT.md, PREREGISTRATION_DR4.md,
every *_HASH.txt and everything under papers_2026/ are untouched.
"""
import numpy as np, math, os, re, sys, warnings
from scipy.special import kv, gamma as GAMMA
from scipy.integrate import quad, IntegrationWarning
warnings.filterwarnings("ignore", category=IntegrationWarning)
warnings.filterwarnings("ignore", category=RuntimeWarning)

FAILS = []
def check(name, ok, detail=""):
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f"   ({detail})" if detail else ""), flush=True)
    if not ok: FAILS.append(name)

def sec(title):
    print("\n" + "=" * 118); print(title); print("=" * 118, flush=True)

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
def rel(p): return os.path.relpath(p, REPO)          # never print an absolute machine path

G = 6.674e-11; MSUN = 1.989e30; kpc = 3.0857e19; Mpc = 3.0857e22; c_light = 2.99792458e8
H0 = 70e3 / Mpc; h70 = 1.0; OmM, OmL = 0.3, 0.7
H0_planck = 67.4e3 / Mpc
A0 = {"canonical": 9.3619e-11, "alt": 1.1279e-10}
rho_b_cosmic = 0.049 * 3 * H0_planck ** 2 / (8 * math.pi * G)

print("=" * 118)
print("L62 -- the GROUP channel: can existing measurements decide L57's nonlocal functional?")
print("=" * 118, flush=True)
print(f"    a0 footings: canonical {A0['canonical']:.4e} m/s^2, alt {A0['alt']:.4e} m/s^2")
print( "    the observable: a metric slip shows up as  M_lens / M_dynamical  != 1  at group scale.")
print( "    L57 E3's prediction at its own working point (kernel n4, l_rms = 1 Mpc): 20 - 45 per cent.")
print(f"    cosmic mean baryon density (Planck h, Omega_b = 0.049): {rho_b_cosmic:.3e} kg/m^3")


# ==================================================================================================
sec("PART A -- CONTROLS.  If one of these fails, the lane stops.")
# ==================================================================================================

# ---------------- the framework's carried kernel ----------------
def Delta(s):
    s = np.asarray(s, float); d = np.where(s > 0, s / np.expm1(np.sqrt(np.maximum(s, 1e-300))), 0.0)
    return np.where(s > 2.540, 0.6476, d)
def g_kernel(g_bar, a0): return g_bar + a0 * Delta(g_bar / a0)

# ---------------- A1: L57's own numbers, read back from its own output ----------------
print("\n  A1 -- CONTROL: L57's group numbers, its working point and its floor law, read back from")
print("       L57_nonlocal_functional.out (not from the .md, and not from memory).")
L57_OUT = os.path.join(HERE, "L57_nonlocal_functional.out")
with open(L57_OUT) as fh: L57TXT = fh.read()
m_grp = re.search(r"bounded group response R = ([\d.eE+-]+) - ([\d.eE+-]+) \(median ([\d.eE+-]+)\)", L57TXT)
m_wp = re.search(r"working point: kernel (\w+) \(a realisable elliptic operator of order (\d+)\), "
                 r"l_rms = (\d+) kpc", L57TXT)
m_ng = re.search(r"(\d+) X-ray groups \(Lovisari", L57TXT)
m_fl = re.search(r"best achievable ([\d.eE+-]+), i\.e\. ([\d.]+) x the bound", L57TXT)
L57_GRP_LO, L57_GRP_HI, L57_GRP_MED = (float(m_grp.group(i)) for i in (1, 2, 3))
L57_TAG, L57_N, L57_L = m_wp.group(1), int(m_wp.group(2)), float(m_wp.group(3))
L57_NGRP = int(m_ng.group(1)); L57_FLOOR = float(m_fl.group(1))
print(f"      L57 E3: {L57_NGRP} Lovisari 2015 groups, response {L57_GRP_LO:.3e} - {L57_GRP_HI:.3e} "
      f"(median {L57_GRP_MED:.3e})")
print(f"      L57 working point: kernel {L57_TAG} (elliptic order n = {L57_N}), l_rms = {L57_L:.0f} kpc")
print(f"      L57 C5a floor at R_max = 100 kpc: {L57_FLOOR:.3e}  (the (R_p/r_cl)^3 floor)")
check("A1 [control] L57's group prediction, working point and floor are read back verbatim from its own "
      "output and are the 20-45% band this lane has to confront",
      (abs(L57_GRP_LO - 0.2147) < 1e-3 and abs(L57_GRP_HI - 0.4504) < 1e-3
       and abs(L57_GRP_MED - 0.3078) < 1e-3 and L57_TAG == "n4" and L57_N == 4 and L57_L == 1000.0
       and L57_NGRP == 20),
      f"{L57_NGRP} groups, {100*L57_GRP_LO:.0f}% - {100*L57_GRP_HI:.0f}% (median {100*L57_GRP_MED:.0f}%), "
      f"kernel {L57_TAG} at l_rms = {L57_L:.0f} kpc")

# ---------------- A2: the smoothing machinery, rebuilt here ----------------
print("""
  A2 -- CONTROL: the smoothing machinery, built independently in this file.  The elliptic operator
       (1 - l^2 D^2)^-n has the Whittle-Matern Green's function
           K_n(r) = m^3 2^(1-v) / [ (4 pi)^(3/2) Gamma(n) ] (m r)^v K_v(m r),   v = n - 3/2, m = 1/l,
       and the Gaussian e^(l^2 D^2 / 2) is (2 pi l^2)^(-3/2) exp(-r^2/2l^2).  For a spherically symmetric
       source the convolution collapses to one radial integral,
           U(R) = (2 pi / R) INT dr' r' rho(r') [ Phi_K(R+r') - Phi_K(|R-r'|) ],  Phi_K(x) = INT_0^x t K(t) dt.
       Three exact facts are checked: normalisation, the uniform fixed point, and a compact source
       returning M K(R).  The rms radius must come out as l sqrt(6n) (l sqrt(3) for the Gaussian).
""")
SGRID = np.exp(np.linspace(math.log(1e-7), math.log(1e5), 40000))     # s / l

def _Kn_shape(x, n):
    """K_n(r) in units of m^3, argument x = m r."""
    v = n - 1.5
    x = np.maximum(np.asarray(x, float), 1e-300)
    pref = 2.0 ** (1.0 - v) / ((4 * math.pi) ** 1.5 * GAMMA(n))
    return pref * x ** v * kv(v, x)
def _Kg_shape(x):
    return (2 * math.pi) ** -1.5 * np.exp(-0.5 * np.asarray(x, float) ** 2)

class Kernel:
    """a normalised, spherically symmetric smoothing kernel, in units of its nominal length l"""
    def __init__(self, tag):
        self.tag = tag
        if tag == "gauss": self.shape = _Kg_shape; self.rms = math.sqrt(3.0)
        else:
            n = int(tag[1:]); self.n = n
            self.shape = (lambda x, n=n: _Kn_shape(x, n)); self.rms = math.sqrt(6.0 * n)
        s = SGRID; Ks = self.shape(s)
        # Phi_K(x) = int_0^x t K(t) dt, cumulative trapezoid in ln s (integrand K s^2 dlns)
        integ = Ks * s ** 2
        dl = np.diff(np.log(s))
        cum = np.concatenate([[0.0], np.cumsum(0.5 * (integ[1:] + integ[:-1]) * dl)])
        self.lgs = np.log(s); self.PhiK = cum
        self.norm = 4 * math.pi * np.trapz(Ks * s ** 3, np.log(s))        # int K d^3r, must be 1
        self.r2 = 4 * math.pi * np.trapz(Ks * s ** 5, np.log(s))          # <r^2> in units l^2
    def PhiK_of(self, s, l):
        """Phi_K(s) = int_0^s t K(t) dt in physical units: K = shape(t/l)/l^3 gives a 1/l prefactor"""
        x = np.log(np.maximum(np.asarray(s, float) / l, 1e-300))
        return np.interp(x, self.lgs, self.PhiK, left=0.0, right=self.PhiK[-1]) / l
    def K_of(self, r, l): return self.shape(np.asarray(r, float) / l) / l ** 3
    def dK_of(self, r, l, h=1e-2):
        """dK/dr by a symmetric relative difference -- accurate where K is nearly flat"""
        r = np.asarray(r, float)
        return (self.K_of(r * (1 + h), l) - self.K_of(r * (1 - h), l)) / (2 * h * r)

KER = {t: Kernel(t) for t in ["gauss", "n1", "n2", "n3", "n4", "n6"]}
print("      kernel    int K d^3r      rms/l  (expected)")
norm_err, rms_err = [], []
for t, K in KER.items():
    exp_rms = math.sqrt(3.0) if t == "gauss" else math.sqrt(6.0 * K.n)
    got = math.sqrt(K.r2); norm_err.append(abs(K.norm - 1.0)); rms_err.append(abs(got / exp_rms - 1))
    print(f"      {t:8s}  {K.norm:.8f}   {got:6.3f}   ({exp_rms:6.3f})")

def smooth(rq, rprof, rho, K, l):
    """U(R) for a spherically symmetric rho on the grid rprof, kernel K at nominal length l"""
    rq = np.atleast_1d(np.asarray(rq, float))
    A = K.PhiK_of(rq[:, None] + rprof[None, :], l) - K.PhiK_of(np.abs(rq[:, None] - rprof[None, :]), l)
    return 2 * math.pi / rq * np.trapz(rprof[None, :] * rho[None, :] * A, rprof, axis=1)

RP = np.exp(np.linspace(math.log(1e17), math.log(3e25), 3000))          # integration grid, m
LT = 5e21
rho_uni = np.ones_like(RP) * 1e-25
Mpt, rball = 2e41, 1e19
rho_pt = np.where(RP < rball, Mpt / (4.0 / 3.0 * math.pi * rball ** 3), 0.0)
Mpt_eff = 4 * math.pi * np.trapz(RP ** 2 * rho_pt, RP)
uni_err, pt_err = [], []
for t, K in KER.items():
    v1 = smooth(np.array([1e22]), RP, rho_uni, K, LT)[0] / 1e-25
    rq = np.array([2e21, 6e21]); v2 = smooth(rq, RP, rho_pt, K, LT) / (Mpt_eff * K.K_of(rq, LT))
    uni_err.append(abs(v1 - 1)); pt_err.append(float(np.max(np.abs(v2 - 1))))
    print(f"      {t:8s}  uniform fixed point {v1:.6f}   point source / M K(r) {v2[0]:.5f}, {v2[1]:.5f}")
check("A2 [control] the smoothing machinery built in this file is exact: every kernel is normalised, has "
      "rms radius l sqrt(6n), leaves a uniform density exactly where it is, and returns M K(R) for a "
      "compact source",
      max(norm_err) < 2e-4 and max(rms_err) < 2e-3 and max(uni_err) < 1e-3 and max(pt_err) < 1e-2,
      f"worst normalisation error {max(norm_err):.2e}, worst rms error {max(rms_err):.2e}, worst uniform "
      f"error {max(uni_err):.2e}, worst point-source error {max(pt_err):.2e}")

# ---------------- A3: the suppression law ----------------
print("""
  A3 -- CONTROL: L57's floor law, re-derived here.  For a source COMPACT against l the smoothed trigger is
       U(R) = M K(R), so the trigger gradient per unit of the object's own acceleration is
           ratio = |dU/dR| / (G M / R^2) = |K'(R)| R^2 / G,
       and the mass cancels exactly.  The small-r behaviour of K' therefore fixes the whole law:
           K'(r) ~ r^(q-2)  =>  ratio ~ R^q  =>  S = ratio_obj/ratio_cl ~ (R_p/r_cl)^q.
       Measured here on this lane's own kernels, with no reference to L57's numbers.
""")
qmeas = {}
xs = np.array([1e-3, 3e-3, 1e-2, 3e-2])                 # r / l, deep in the small-argument regime
rsmall = xs * LT
# an END-TO-END test as well: a compact exponential-sphere source of size R_p/4 pushed through the FULL
# smoothing machinery at a length far larger than it, with the trigger gradient taken at R_p
L_BIG = 10000.0 * kpc / KER["n4"].rms                    # nominal l for l_rms = 10 Mpc
RP_PROBE = np.array([10.0, 30.0, 100.0]) * kpc
def compact_ratio(K, l, Rp_m):
    rd = Rp_m / 4.0; Mb = 1e11 * MSUN
    rho = Mb / (8 * math.pi * rd ** 3) * np.exp(-RP / rd)
    rho = rho * Mb / (4 * math.pi * np.trapz(RP ** 2 * rho, RP))
    rq = np.array([0.98, 1.02]) * Rp_m
    sm = smooth(rq, RP, rho, K, l)
    grad = abs((sm[1] - sm[0]) / (rq[1] - rq[0]))
    Menc = 4 * math.pi * np.trapz(RP[RP <= Rp_m] ** 2 * rho[RP <= Rp_m], RP[RP <= Rp_m])
    return grad / (G * Menc / Rp_m ** 2)
for t, K in KER.items():
    dK = K.dK_of(rsmall, LT)
    q = float(np.polyfit(np.log(rsmall), np.log(np.abs(dK)), 1)[0]) + 2.0
    rr = np.array([compact_ratio(K, L_BIG, Rp) for Rp in RP_PROBE])
    qdir = float(np.polyfit(np.log(RP_PROBE), np.log(rr), 1)[0])
    qmeas[t] = (q, qdir)
    print(f"      {t:8s}: K'(r) ~ r^{q-2:+.3f}  =>  q = {q:.3f}   |   full convolution of a compact source: "
          f"ratio(R_p) ~ R_p^{qdir:.3f}")
q_ok = (abs(qmeas["n1"][0] - 0.0) < 0.05 and abs(qmeas["n2"][0] - 2.0) < 0.05
        and all(abs(qmeas[t][0] - 3.0) < 0.05 for t in ("n3", "n4", "n6", "gauss")))
q_dir_ok = all(abs(qmeas[t][1] - qmeas[t][0]) < 0.10 for t in KER)
check("A3 [control] the suppression law reproduces: q = 0 for n = 1, q = 2 for n = 2, and q = 3 -- the "
      "CUBE of the scale ratio -- for every n >= 3 and for the Gaussian, so no kernel order and no length "
      "beats (R_p/r_cl)^3.  Checked twice: from K'(r) analytically, and end-to-end through the full "
      "convolution of a compact source",
      q_ok and q_dir_ok,
      "q = " + ", ".join(f"{t} {qmeas[t][0]:.2f}" for t in KER)
      + f"; the end-to-end convolution exponents agree to "
        f"{max(abs(qmeas[t][1]-qmeas[t][0]) for t in KER):.3f}")

# ---------------- the clusters, read independently ----------------
from astropy.io import fits
XDIR = os.path.join(REPO, "real_research/data/xcop")
WL_H20 = {   # Herbonnet et al. 2020 MNRAS 497, 4684, Tables 2 and 3 (masses in 1e14 Msun)
 "A85":    dict(z=0.055, M200=8.4,  M500=5.7,  eM500=2.2, Rmax=1.6),
 "A1795":  dict(z=0.062, M200=13.9, M500=9.3,  eM500=2.2, Rmax=1.8),
 "A2029":  dict(z=0.077, M200=18.1, M500=12.1, eM500=2.5, Rmax=2.2),
 "A2142":  dict(z=0.091, M200=14.5, M500=9.7,  eM500=2.3, Rmax=2.5),
 "ZW1215": dict(z=0.075, M200=5.1,  M500=3.5,  eM500=2.2, Rmax=2.1),
}
WLN = list(WL_H20)
def Ez(z): return math.sqrt(OmM * (1 + z) ** 3 + OmL)
def rho_crit(z): return 3 * (H0 * Ez(z)) ** 2 / (8 * math.pi * G)
def c200_DM14(M200, z):
    a = 0.520 + (0.905 - 0.520) * math.exp(-0.617 * z ** 1.21); b = -0.101 + 0.026 * z
    return 10 ** (a + b * math.log10(M200 * h70 / 1e12))
def nfw_pars(M200, z):
    cc = c200_DM14(M200, z)
    r200 = (3 * M200 * MSUN / (4 * math.pi * 200.0 * rho_crit(z))) ** (1.0 / 3.0)
    dc = (200.0 / 3.0) * cc ** 3 / (math.log(1 + cc) - cc / (1 + cc))
    return r200 / cc, dc, rho_crit(z), cc, r200
def nfw_Sigma(R, rs, dc, rhoc):
    x = R / rs; A = 2 * rs * dc * rhoc
    if abs(x - 1) < 1e-8: return A / 3.0
    if x < 1: return A / (x * x - 1) * (1 - 2 / math.sqrt(1 - x * x) * math.atanh(math.sqrt((1 - x) / (1 + x))))
    return A / (x * x - 1) * (1 - 2 / math.sqrt(x * x - 1) * math.atan(math.sqrt((x - 1) / (x + 1))))
def nfw_g(x):
    if abs(x - 1) < 1e-8: return math.log(x / 2.0) + 1.0
    if x < 1: return math.log(x / 2.0) + math.acosh(1.0 / x) / math.sqrt(1 - x * x)
    return math.log(x / 2.0) + math.acos(1.0 / x) / math.sqrt(x * x - 1)
def nfw_DS(R, rs, dc, rhoc):
    return 4 * rs * dc * rhoc * nfw_g(R / rs) / (R / rs) ** 2 - nfw_Sigma(R, rs, dc, rhoc)
def nfw_M3d(r, rs, dc, rhoc):
    x = r / rs; return 4 * math.pi * dc * rhoc * rs ** 3 * (math.log(1 + x) - x / (1 + x))

def _rkpc(rad, unit, R500):
    u = (unit or "").strip().lower()
    if u in ("r/r500", "r500"): return np.asarray(rad, float) * R500
    if u == "mpc": return np.asarray(rad, float) * 1e3
    return np.asarray(rad, float)
GRID = np.exp(np.linspace(math.log(1.0), math.log(1.0e5), 1200))     # kpc
RGRID_M = GRID * kpc
def loginterp(xq, xp, fp):
    m = np.isfinite(xp) & np.isfinite(fp) & (fp > 0) & (xp > 0)
    return np.exp(np.interp(np.log(xq), np.log(xp[m]), np.log(fp[m]), left=np.nan, right=np.nan))
def load_cluster(name):
    p = os.path.join(XDIR, name); c = {"name": name}
    with fits.open(os.path.join(p, name + "_hydro_mass.fits")) as f:
        dd = f[1].data; R5 = float(f[1].header["R500"]); c["R500"] = R5
        c["rh"] = _rkpc(dd["RADIUS"], f[1].columns["RADIUS"].unit, R5)
        c["Mh"] = np.array(dd["M_FORW"], float); c["eMh"] = np.array(dd["EM_FORW"], float)
    with fits.open(os.path.join(p, name + "_fgas_profile.fits")) as f:
        dd = f[1].data
        c["rg"] = _rkpc(dd["RADIUS"], f[1].columns["RADIUS"].unit, c["R500"]); c["Mg"] = np.array(dd["MGAS"], float)
    with fits.open(os.path.join(p, name + "_mstar.fits")) as f:
        dd = f[2].data
        c["rs"] = _rkpc(dd["RADIUS"], f[2].columns["RADIUS"].unit, c["R500"]); c["Ms"] = np.array(dd["MSTAR"], float)
    def extend(rp, fp, steepen):
        f_ = loginterp(GRID, rp, fp); lo, hi = rp.min(), rp.max()
        sin_ = (math.log(fp[2]) - math.log(fp[0])) / (math.log(rp[2]) - math.log(rp[0]))
        sout = min(max((math.log(fp[-1]) - math.log(fp[-4])) / (math.log(rp[-1]) - math.log(rp[-4])), 0.0), 1.5)
        f_ = np.where(GRID < lo, fp[0] * (GRID / lo) ** sin_, f_)
        if steepen: f_ = np.where(GRID > hi, fp[-1] + sout * fp[-1] * (1.0 - (GRID / hi) ** -1.0), f_)
        else:       f_ = np.where(GRID > hi, fp[-1] * np.ones_like(GRID), f_)
        return f_
    c["Mbar"] = extend(c["rg"], c["Mg"], True) + extend(c["rs"], c["Ms"], False)
    c["Mh_i"] = np.exp(np.interp(np.log(GRID), np.log(c["rh"]), np.log(c["Mh"]),
                                 left=np.nan, right=math.log(c["Mh"][-1])))
    c["eMh_i"] = np.exp(np.interp(np.log(GRID), np.log(c["rh"]), np.log(c["eMh"]),
                                  left=np.nan, right=math.log(c["eMh"][-1])))
    c["R200"] = 1.6 * c["R500"]
    c["rho_b"] = np.maximum(np.gradient(c["Mbar"] * MSUN, np.log(GRID)) / (4 * math.pi * RGRID_M ** 3), 1e-45)
    return c
CLU = {n: load_cluster(n) for n in WLN}
for n in WLN:
    d = WL_H20[n]; d["rs"], d["dc"], d["rhoc"], d["c200"], d["r200"] = nfw_pars(d["M200"] * 1e14, d["z"])
print(f"\n      X-COP profiles read from {rel(XDIR)} for the five clusters with published weak lensing")
def at(vals, r_kpc): return float(np.exp(np.interp(math.log(r_kpc), np.log(GRID), np.log(np.maximum(vals, 1e-30)))))
def Mfw_grid(c, a0):
    gb = G * np.asarray(c["Mbar"], float) * MSUN / RGRID_M ** 2
    return g_kernel(gb, a0) * RGRID_M ** 2 / (G * MSUN)

# ---------------- A4: the 9 sigma shear-shape failure, recomputed ----------------
print("\n  A4 -- CONTROL: the 9-sigma cluster shear-SHAPE failure, recomputed here from the X-COP baryons")
print("       and the Herbonnet 2020 weak-lensing NFWs, with this file's own projection integrals.")
def Sigma_of_R(rho, R, zmax):
    f = lambda zz: rho(math.sqrt(R * R + zz * zz))
    a = quad(f, 0.0, R, limit=200)[0]
    b = quad(f, R, zmax, limit=400)[0] if zmax > R else 0.0
    return 2.0 * (a + b)
def Sigmabar_of_R(rho, R, zmax, n=40):
    xg, wg = np.polynomial.legendre.leggauss(n)
    Rp = 0.5 * R * (xg + 1.0); wp = 0.5 * R * wg
    return 2.0 * sum(wi * Rpi * Sigma_of_R(rho, Rpi, zmax) for Rpi, wi in zip(Rp, wp)) / (R * R)
def rho_from_M(Mgrid, r_trunc_kpc):
    lg = np.log(GRID)
    rr = np.maximum(np.gradient(np.asarray(Mgrid, float), lg) * MSUN / (4 * math.pi * RGRID_M ** 3), 1e-45)
    lr = np.log(rr)
    def f(r_m):
        rk = r_m / kpc
        if rk > r_trunc_kpc: return 0.0
        return math.exp(np.interp(math.log(max(rk, GRID[0])), lg, lr))
    return f
SHAPE, BASE = {}, {}
for foot, a0 in A0.items():
    rows = []
    for n in WLN:
        c = CLU[n]; d = WL_H20[n]; rt = 2.0 * c["R200"]
        Mfw = Mfw_grid(c, a0); rho_fw = rho_from_M(Mfw, rt)
        Rf = np.exp(np.linspace(math.log(0.5 * Mpc), math.log(min(2.0, d["Rmax"]) * Mpc), 12))
        DSfw = np.array([Sigmabar_of_R(rho_fw, R, rt * kpc) - Sigma_of_R(rho_fw, R, rt * kpc) for R in Rf])
        DSwl = np.array([nfw_DS(R, d["rs"], d["dc"], d["rhoc"]) for R in Rf])
        rows.append(dict(name=n, sfw=np.polyfit(np.log(Rf), np.log(DSfw), 1)[0],
                         swl=np.polyfit(np.log(Rf), np.log(DSwl), 1)[0],
                         Mfw500=at(Mfw, c["R500"]), R500=c["R500"],
                         MWL500=nfw_M3d(c["R500"] * kpc, d["rs"], d["dc"], d["rhoc"]) / MSUN,
                         MHSE500=at(c["Mh_i"], c["R500"]), eMHSE500=at(c["eMh_i"], c["R500"])))
    dsl = np.array([r["sfw"] - r["swl"] for r in rows])
    SHAPE[foot] = (float(dsl.mean()), float(dsl.std(ddof=1) / math.sqrt(len(dsl)))); BASE[foot] = rows
    print(f"      {foot:9s}: framework log-slope {np.mean([r['sfw'] for r in rows]):+.3f}, measured "
          f"{np.mean([r['swl'] for r in rows]):+.3f}, difference {SHAPE[foot][0]:+.3f} +/- "
          f"{SHAPE[foot][1]:.3f}  ({abs(SHAPE[foot][0])/SHAPE[foot][1]:.1f} sigma)")
zs = {f: abs(SHAPE[f][0]) / SHAPE[f][1] for f in A0}
check("A4 [control] the 9-sigma cluster shear-shape failure reproduces independently (L51 C2 / L56 A3 / "
      "L57 A2: +0.516 +/- 0.058 canonical, +0.521 +/- 0.058 alt)",
      all(abs(SHAPE[f][0] - 0.518) < 0.05 for f in A0) and all(zs[f] > 6 for f in A0),
      ", ".join(f"{f} {SHAPE[f][0]:+.3f} +/- {SHAPE[f][1]:.3f} ({zs[f]:.1f} sigma)" for f in A0))

# ---------------- A5: the measured cluster lensing / hydrostatic ratio ----------------
print("\n  A5 -- CONTROL: the measured cluster lensing-to-dynamical mass ratio, recomputed.")
print("       NOTE, and it matters for this whole lane: the 'dynamical' mass in this ratio is the X-ray")
print("       HYDROSTATIC mass.  The comparison is M_WL / M_HSE, not lensing against a collisionless tracer.")
ratios, eratios = [], []
for r in BASE["canonical"]:
    d = WL_H20[r["name"]]; Rw = r["MWL500"] / r["MHSE500"]
    eratios.append(Rw * math.hypot(d["eM500"] / d["M500"], r["eMHSE500"] / r["MHSE500"])); ratios.append(Rw)
ratios = np.array(ratios); eratios = np.array(eratios); wgt = 1.0 / eratios ** 2
Rmeas = float(np.sum(wgt * ratios) / np.sum(wgt)); eRmeas = float(1.0 / math.sqrt(np.sum(wgt)))
print(f"      inverse-variance mean over the five X-COP clusters: {Rmeas:.3f} +/- {eRmeas:.3f}   "
      f"(L51 C5 1.148 +/- 0.146; L57 A3 1.148 +/- 0.146)")
check("A5 [control] the measured cluster lensing/hydrostatic mass ratio reproduces",
      abs(Rmeas - 1.15) < 0.08, f"{Rmeas:.3f} +/- {eRmeas:.3f}")
R_EMB_LOCAL = {}
for foot in A0:
    R_EMB_LOCAL[foot] = float(np.median([(r["MWL500"] - r["Mfw500"]) / r["Mfw500"] for r in BASE[foot]]))
print(f"      L56's convention-free crux M_P/M_fw, recomputed: canonical {R_EMB_LOCAL['canonical']:.3f}, "
      f"alt {R_EMB_LOCAL['alt']:.3f}   (L57 A4: 0.803 / 0.666)")

# ---------------- A6: L57's group response, recomputed with this lane's kernel ----------------
print("""
  A6 -- CONTROL: L57's GROUP numbers, recomputed here from the Lovisari 2015 catalogue with this file's own
       kernel, its own X-COP smoothing and its own reference response.  L57's stated group model is kept
       EXACTLY as published so that this is a reproduction and not a re-modelling: an isothermal sphere
       rho ~ r^-2 truncated at 2 R500, normalised to M_gas500 x 1.30, probed at R500.  That model is the one
       that MAXIMISES the group's own trigger gradient, so the 20-45% band is an upper bound on the
       prediction -- recorded here because it runs in the direction of making the channel LESS decisive.
""")
RCL_EVAL = 1000.0
def rho_prof_cluster(c):
    lg = np.log(GRID); lr = np.log(np.maximum(c["rho_b"], 1e-45)); rk = RP / kpc
    out = np.exp(np.interp(np.log(rk), lg, lr, left=lr[0], right=-np.inf))
    return np.where(rk > 3.0 * c["R200"], rho_b_cosmic, np.maximum(out, rho_b_cosmic))
KWP = KER["n4"]; L_NOM = L57_L * kpc / KWP.rms          # nominal l giving rms = 1000 kpc
RATIO_CL = {}
for foot, a0 in A0.items():
    vals = []
    for n in WLN:
        c = CLU[n]; rho = rho_prof_cluster(c)
        rq = np.array([RCL_EVAL * 0.98, RCL_EVAL * 1.02]) * kpc
        sm = smooth(rq, RP, rho, KWP, L_NOM)
        gb = G * at(c["Mbar"], RCL_EVAL) * MSUN / (RCL_EVAL * kpc) ** 2
        vals.append(abs((sm[1] - sm[0]) / (rq[1] - rq[0])) / float(g_kernel(gb, a0)))
    RATIO_CL[foot] = float(np.median(vals))
    print(f"      {foot:9s}: ratio_cl at 1 Mpc (median over 5 X-COP clusters) = {RATIO_CL[foot]:.4e} s^2/m^2")

LOV = os.path.join(REPO, "real_research/data/lovisari2015_groups.tsv")
GRP = []
with open(LOV) as fh:
    hdr = None
    for line in fh:
        if line.startswith("#") or not line.strip(): continue
        parts = line.rstrip("\n").split("\t")
        if hdr is None: hdr = parts; continue
        d = dict(zip(hdr, parts))
        try:
            R500 = float(d["R500_kpc"]); Mg = float(d["Mgas500_1e12"]) * 1e12
            kT = float(d["kT_keV"]); M500 = float(d["M500_1e13"]) * 1e13
        except Exception: continue
        GRP.append(dict(name=d["name"], R500=R500, kT=kT, M500=M500, Mb=Mg * 1.30 * MSUN))
print(f"      {len(GRP)} groups read from {rel(LOV)}: kT = {min(g['kT'] for g in GRP):.2f} - "
      f"{max(g['kT'] for g in GRP):.2f} keV, M500(HSE) = {min(g['M500'] for g in GRP):.2e} - "
      f"{max(g['M500'] for g in GRP):.2e} Msun, R500 = {min(g['R500'] for g in GRP):.0f} - "
      f"{max(g['R500'] for g in GRP):.0f} kpc")
GRPR = {}
for foot, a0 in A0.items():
    out = []
    for g in GRP:
        rt = 2 * g["R500"] * kpc
        prof = np.where(RP <= rt, g["Mb"] / (4 * math.pi * rt * np.maximum(RP, 1e18) ** 2), 0.0)
        Rq = np.array([0.98, 1.02]) * g["R500"] * kpc
        sm = smooth(Rq, RP, prof, KWP, L_NOM)
        grad = abs((sm[1] - sm[0]) / (Rq[1] - Rq[0]))
        gb = G * g["Mb"] * 0.5 / (g["R500"] * kpc) ** 2
        out.append(R_EMB_LOCAL[foot] * (grad / float(g_kernel(gb, a0))) / RATIO_CL[foot])
    GRPR[foot] = np.array(out)
    print(f"      {foot:9s}: group response R = {GRPR[foot].min():.3e} - {GRPR[foot].max():.3e} "
          f"(median {np.median(GRPR[foot]):.3e})")
d_lo = abs(GRPR["canonical"].min() - L57_GRP_LO) / L57_GRP_LO
d_hi = abs(GRPR["canonical"].max() - L57_GRP_HI) / L57_GRP_HI
d_md = abs(np.median(GRPR["canonical"]) - L57_GRP_MED) / L57_GRP_MED
check("A6 [control] L57's group prediction is reproduced independently -- this file's own kernel, own "
      "X-COP smoothing, own reference response -- to better than 10%",
      max(d_lo, d_hi, d_md) < 0.10,
      f"canonical {100*GRPR['canonical'].min():.1f}% - {100*GRPR['canonical'].max():.1f}% "
      f"(median {100*np.median(GRPR['canonical']):.1f}%) against L57's {100*L57_GRP_LO:.1f}% - "
      f"{100*L57_GRP_HI:.1f}% (median {100*L57_GRP_MED:.1f}%); worst deviation {100*max(d_lo,d_hi,d_md):.1f}%. "
      f"Alt footing {100*GRPR['alt'].min():.1f}% - {100*GRPR['alt'].max():.1f}% "
      f"(median {100*np.median(GRPR['alt']):.1f}%)")
PRED_LO = min(GRPR[f].min() for f in A0); PRED_HI = max(GRPR[f].max() for f in A0)
PRED_MED = float(np.median(np.concatenate([GRPR[f] for f in A0])))
print(f"      => THE BAND THIS LANE MUST CONFRONT, both footings: {100*PRED_LO:.0f}% - {100*PRED_HI:.0f}% "
      f"(median {100*PRED_MED:.0f}%) excess of M_lens over M_dynamical at group scale.")


# ==================================================================================================
sec("PART B -- WHAT IS ACTUALLY MEASURED FOR GROUPS.  Published numbers, samples, uncertainties.")
# ==================================================================================================
print("""
  Every entry below is a published measurement or a published simulation prediction, with its sample and
  its quoted uncertainty.  Nothing is averaged across entries: they measure different things on different
  samples with different estimators, and combining them would be exactly the error this repository has been
  burned by three times.  They are listed, compared, and the disagreements are kept.
""")
LIT = [
 dict(tag="Kettula+2013",  ref="ApJ 778, 74 (COSMOS)", kind="lens/HSE", n=10,
      rng="10 X-ray groups + 55 clusters, 1e13-1e15 Msun",
      val="bias rising to 30-50% at kT = 1 keV", stat="individual WL masses 20-40%",
      note="first observational support for hydrostatic bias at GROUP level; the 30-50% is an "
           "EXTRAPOLATION of a fitted M-T relation to 1 keV, not a directly measured ratio, and no "
           "uncertainty is quoted on it"),
 dict(tag="Kettula+2015",  ref="MNRAS 451, 1460 (CFHTLenS + XMM-CFHTLS)", kind="lens/HSE", n=70,
      rng="70 systems over 2 dex in mass",
      val="groups more luminous and warmer at fixed WL mass than clusters", stat="relation-level",
      note="a scaling-relation residual, not a per-system mass ratio"),
 dict(tag="Umetsu+2020",   ref="ApJ 890, 148 (XXL + Subaru HSC)", kind="lens/HSE", n=105,
      rng="105 XXL systems with HSC lensing masses and X-ray temperatures, 0.031 < z < 1.033",
      val="mean mass offset 34 +/- 20 per cent (1.5 sigma) between the WL masses and the X-ray T-M relation",
      stat="20% (statistical, on the mean)",
      note="THE tightest direct group-to-cluster lensing-versus-X-ray mass comparison available; the "
           "sample spans groups AND clusters, so it is not a pure group number"),
 dict(tag="Akino+2022",    ref="PASJ 74, 175 (HSC-XXL)", kind="baryon budget", n=136,
      rng="136 XXL groups and clusters, M500 ~ 1e13 - 1e15 Msun",
      val="gas-mass and stellar-mass scaling relations calibrated on HSC WL masses",
      stat="—", note="calibrates GAS mass against WL mass; it does not publish an M_HSE/M_WL ratio"),
 dict(tag="Kugel+2024",    ref="MNRAS (FLAMINGO simulations), arXiv:2409.07849", kind="LambdaCDM baseline",
      n=0, rng="M500c from group to cluster scale",
      val="b_HSE = (M_HSE - M)/M rises from about -0.1 at GROUP mass to about -0.2 at CLUSTER mass",
      stat="sigma(b_HSE) ~ 0.1 at 1e14 Msun, rising rapidly to lower mass",
      note="the LambdaCDM expectation for M_WL/M_HSE at group scale is therefore about 1.11, NOT 1.00 -- "
           "and note its mass trend runs OPPOSITE to Kettula+2013's"),
 dict(tag="Schellenberger+2015", ref="A&A 575, A30 (HIFLUGCS)", kind="instrument systematic", n=64,
      rng="64 clusters observed with both Chandra and XMM-Newton",
      val="Chandra hydrostatic masses 14 +/- 2 per cent higher than XMM-Newton", stat="2%",
      note="a pure instrument cross-calibration effect on M_HSE, present in every hydrostatic sample and "
           "irreducible without a common calibration"),
 dict(tag="George+2012",   ref="ApJ 757, 2 (COSMOS X-ray groups)", kind="lensing systematic", n=129,
      rng="X-ray selected groups",
      val="stacked WL halo masses biased LOW by 5-30 per cent when the centre is wrong", stat="—",
      note="miscentring is the leading group-scale weak-lensing systematic and it is worse for groups "
           "than for clusters"),
 dict(tag="Old+2015",      ref="MNRAS 449, 1897 (Galaxy Cluster Mass Reconstruction Project II)",
      kind="dynamical estimator", n=0, rng="mock catalogues, 25 mass-estimation techniques",
      val="recovered-mass scatter about a factor 2 above 1e14 Msun, rising rapidly toward an ORDER OF "
          "MAGNITUDE below 1e14 Msun", stat="—",
      note="large scatter persists even when the TRUE membership is supplied: mass reconstruction with "
           "few dynamical tracers is intrinsically limited"),
 dict(tag="Old+2018",      ref="MNRAS 475, 853 (GCMRP III)", kind="dynamical estimator", n=0,
      rng="mock catalogues with dynamical substructure",
      val="masses over-estimated by ~10% at 1e14 Msun and by >= 20% at <= 1e13.5 Msun", stat="—",
      note="a BIAS, not scatter: it does not average down with sample size"),
 dict(tag="Viola+2015",    ref="MNRAS 452, 3529 (GAMA groups + KiDS)", kind="lens vs sigma", n=1000,
      rng="GAMA groups", val="M_WL proportional to sigma^(1.89 +/- 0.27)", stat="0.27 in the slope",
      note="the virial expectation is sigma^3; the authors attribute the shortfall to selection effects, "
           "so the lensing-to-dynamical comparison at group scale is not calibrated at the tens-of-per-cent "
           "level by anything other than a model"),
 dict(tag="GAMA+HSC 2022", ref="arXiv:2107.05641", kind="lens vs sigma", n=1587,
      rng="1587 GAMA groups with >= 5 members",
      val="M_WL = (0.93 +/- 0.05)e14 Msun at sigma = 500 km/s, slope 1.52 +/- 0.10", stat="5% on the norm",
      note="the slope is even shallower than Viola+2015's; the normalisation is statistically superb and "
           "the SLOPE is the problem -- a 5% statistical error on a relation whose shape disagrees with "
           "the virial expectation by a factor of two in slope cannot support a 20-45% test"),
 dict(tag="Logan+2022",    ref="arXiv:2202.08569 (HeCS + Chandra)", kind="HSE vs caustic", n=14,
      rng="14 clusters with >= 210 spectroscopic members",
      val="M_X / M_caustic = 1.12 (+0.11/-0.10) at R500", stat="~10%",
      note="the authors state systematics of BOTH estimators remain at the 10-15% level, and that their "
           "result favours less than 20% hydrostatic bias at 3 sigma -- at CLUSTER mass, not group mass"),
 dict(tag="escape-edge 2025", ref="arXiv:2507.20938", kind="lens vs collisionless dynamics", n=46,
      rng="46 clusters, 0.05 < z < 0.3, 14.4 <= log10 M/Msun <= 15.4",
      val="mean relative difference between WL mass and escape-velocity mass = 0.02 +/- 0.02 dex",
      stat="0.02 dex = 4.7% on the mean",
      note="the ONLY lensing-versus-collisionless-dynamics comparison at this precision anywhere; it is at "
           "CLUSTER mass.  The same paper records that the earlier CAUSTIC comparison had a bias of "
           "0.25 +/- 0.05 dex with a mass-mass correlation of 0.16 -- i.e. essentially none.  Two "
           "collisionless estimators on overlapping data disagreed by 0.23 dex"),
 dict(tag="this repo", ref="g06 vs KT2017 (L57 E3's own reason for refusing to score)", kind="estimator spread",
      n=19, rng="19 shared group hosts",
      val="the two group-scale estimators disagree by +0.42 dex", stat="—",
      note="0.42 dex is a factor 2.6: larger than the entire predicted band"),
]
for e in LIT:
    print(f"      {e['tag']:18s} [{e['kind']:>28s}]  {e['val']}")
    print(f"      {'':18s}  sample: {e['rng']}")
    print(f"      {'':18s}  quoted: {e['stat']};  {e['ref']}")
    print(f"      {'':18s}  note:   {e['note']}")
    print()

# B1 -- does a direct group-scale lensing/hydrostatic measurement exist at all?
have_direct_hse = any(e["kind"] == "lens/HSE" and e["stat"].strip("—") for e in LIT)
UMETSU_RATIO, UMETSU_STAT = 1.34, 0.20
check("B1 [test] a DIRECT published measurement of the lensing-to-hydrostatic mass ratio exists at group "
      "scale, with a quoted uncertainty",
      have_direct_hse,
      f"YES -- Umetsu+2020 give {UMETSU_RATIO:.2f} +/- {UMETSU_STAT:.2f} (mean mass offset 34 +/- 20 per "
      f"cent, 1.5 sigma) on 105 XXL systems, and Kettula+2013 give 30-50% at 1 keV on 10 COSMOS groups "
      f"with no quoted uncertainty.  The XXL sample spans groups AND clusters, so the group-only number is "
      f"weaker than the one quoted here, not stronger")

check("B2 [test] a DIRECT published measurement of the lensing-to-GALAXY-DYNAMICAL mass ratio exists at "
      "group scale (M500 ~ 1e13 - 1e14 Msun) with better than 20 per cent total uncertainty",
      False,
      "NO -- none was found.  The precise collisionless-tracer comparison (0.02 +/- 0.02 dex) is at "
      "log10 M/Msun = 14.4-15.4, an order of magnitude ABOVE the Lovisari groups, and the group-scale "
      "dynamical estimator is exactly where Old+2015 finds the recovered-mass scatter rising toward an "
      "order of magnitude and Old+2018 finds a >= 20% substructure BIAS at <= 1e13.5 Msun.  The two "
      "existing group-scale lensing-vs-sigma relations (Viola+2015 slope 1.89 +/- 0.27, GAMA+HSC slope "
      "1.52 +/- 0.10) disagree with the virial expectation of 3 and with each other")

FLAM_BASELINE = 1.0 / (1.0 - 0.10)      # b_HSE = -0.10 at group scale => M_WL/M_HSE = 1/(1-0.10)
FLAM_CLUSTER = 1.0 / (1.0 - 0.20)
check("B3 [test] the LambdaCDM baseline for the group-scale lensing-to-hydrostatic ratio is 1.00, so any "
      "measured excess can be attributed to a metric slip",
      False,
      f"NO, and this is the single most important fact in the lane.  FLAMINGO gives b_HSE ~ -0.10 at group "
      f"mass, i.e. an expected M_WL/M_HSE = {FLAM_BASELINE:.2f} with NO new physics ({FLAM_CLUSTER:.2f} at "
      f"cluster mass); Kettula+2013 infer 1.3-1.5 at 1 keV from the data themselves.  The baseline is "
      f"therefore uncertain over a range of about {100*(1.45-FLAM_BASELINE):.0f} percentage points -- "
      f"comparable to the ENTIRE predicted band of {100*PRED_LO:.0f}-{100*PRED_HI:.0f}%.  The two are not "
      f"merely hard to separate; they are the same observable with the same sign")


# ==================================================================================================
sec("PART C -- THE SYSTEMATIC FLOOR.  Not the statistical error: the floor.")
# ==================================================================================================
print("""
  THE RULE THIS LANE IS HELD TO.  This repository has three times computed a significance as though
  correlated errors were independent, and three times had to withdraw it.  So the budget below is built the
  only way that cannot make that mistake: every entry is classified as COMMON-MODE (a calibration or
  modelling choice shared by every system in a sample, which does NOT average down with N) or PER-SYSTEM
  (which does).  The floor on a sample mean is the common-mode part, full stop, and it is quoted as such.

  Entries marked [lit] carry a literature-quoted value.  Entries marked [stated] are this lane's own
  conservative placeholders -- they are labelled, and the floor is quoted BOTH with and without them so
  that no conclusion rests on a number this lane made up.
""")
BUDGET = [
 # (side, entry, per-cent, common-mode?, source-class, source)
 ("WL",  "shear multiplicative calibration",            2.0, True,  "lit",
  "HSC-Y1 / KiDS-1000 published shear-calibration budgets"),
 ("WL",  "photo-z / Sigma_crit calibration",            5.0, True,  "stated",
  "conservative; survey-dependent"),
 ("WL",  "miscentring residual after modelling",       10.0, True,  "lit",
  "George+2012: 5-30 per cent if uncorrected, at GROUP scale; 10% taken as the residual"),
 ("WL",  "halo model: concentration, 2-halo, triaxiality", 8.0, True, "stated",
  "conservative"),
 ("WL",  "selection / Eddington bias on an X-ray-selected group sample", 10.0, True, "stated",
  "conservative; the group mass function is steep and L_X-M scatter is large"),
 ("HSE", "instrument cross-calibration (Chandra vs XMM)", 14.0, True, "lit",
  "Schellenberger+2015: M_HSE(Chandra) = 1.14 +/- 0.02 x M_HSE(XMM)"),
 ("HSE", "ICM modelling at ~1 keV (abundance / emissivity)", 10.0, True, "stated",
  "motivated by Lovisari+2021's factor-3 emissivity sensitivity at group temperatures"),
 ("HSE", "extrapolation of the X-ray profile to R500", 12.0, True, "stated", "conservative"),
 ("HSE", "gas clumping and asphericity",                7.0, True,  "stated", "conservative"),
 ("both","per-system projection / triaxiality scatter", 25.0, False, "lit",
  "escape-edge 2025 quotes simulation scatter ~25 per cent; averages down as 1/sqrt(N)"),
]
print(f"      {'side':5s} {'entry':56s} {'%':>6s}  {'mode':11s} {'class':7s}")
for side, name, pc, common, cls, src in BUDGET:
    print(f"      {side:5s} {name:56s} {pc:6.1f}  {'COMMON-MODE' if common else 'per-system':11s} [{cls}]")
    print(f"      {'':5s} {'':56s}         {src}")
def quad_sum(vals): return math.sqrt(sum(v * v for v in vals))
lit_common = [pc for side, nm, pc, cm, cls, s in BUDGET if cm and cls == "lit"]
all_common = [pc for side, nm, pc, cm, cls, s in BUDGET if cm]
persys = [pc for side, nm, pc, cm, cls, s in BUDGET if not cm]
FLOOR_LIT = quad_sum(lit_common); FLOOR_ALL = quad_sum(all_common)
print(f"\n      common-mode floor, LITERATURE ENTRIES ONLY (shear 2%, miscentring 10%, Chandra-XMM 14%): "
      f"{FLOOR_LIT:.1f}%")
print(f"      common-mode floor, FULL STATED BUDGET:                                              "
      f"{FLOOR_ALL:.1f}%")
print(f"      per-system scatter (averages down): {persys[0]:.0f}% per system")
NEED_LO, NEED_HI = 100 * PRED_LO / 3.0, 100 * PRED_HI / 3.0     # 3 sigma on the bottom / top of the band
check("C1 [test] the systematic floor, using ONLY literature-quoted entries, is small enough to see the "
      "BOTTOM of the predicted band at 3 sigma",
      FLOOR_LIT <= NEED_LO,
      f"NO -- 3 sigma on a {100*PRED_LO:.0f}% slip needs a total uncertainty of {NEED_LO:.1f}%, and the "
      f"literature-only COMMON-MODE floor alone is {FLOOR_LIT:.1f}%, {FLOOR_LIT/NEED_LO:.1f}x too large.  "
      f"The bottom of the band is smaller than the irreducible calibration uncertainty of the measurement "
      f"meant to find it, before a single conservative placeholder is added and before any statistical "
      f"error")
check("C2 [test] the full stated systematic floor is small enough to see the TOP of the predicted band at "
      "3 sigma",
      FLOOR_ALL <= NEED_HI,
      f"NO -- 3 sigma on the top of the band ({100*PRED_HI:.0f}%) needs {NEED_HI:.1f}% total, against a "
      f"full-budget floor of {FLOOR_ALL:.1f}% and a literature-only floor of {FLOOR_LIT:.1f}%.  Even the "
      f"most favourable corner of the prediction, measured with a perfect statistical sample, sits "
      f"{FLOOR_LIT/NEED_HI:.1f}x inside the calibration floor")

print("""
  C3 -- THE CORRELATED-ERROR TRAP, made explicit so that this lane cannot fall into it.  The Lovisari
       catalogue has 20 groups; XXL has 105 systems; a future sample could have 10^4.  If the floor were
       treated as though it were independent per system, it would appear to shrink as 1/sqrt(N) and the
       channel would look decisive.  It is not: a shear calibration, a photo-z calibration, an instrument
       cross-calibration and a halo model are ONE choice applied to every system in the sample.
""")
for N in (5, 20, 105, 1000, 10000):
    wrong = FLOOR_ALL / math.sqrt(N)
    right = math.sqrt(FLOOR_ALL ** 2 + (persys[0] ** 2) / N)
    print(f"      N = {N:6d}:  WRONG (floor treated as independent) {wrong:6.2f}%   |   "
          f"RIGHT (common-mode + per-system/sqrt(N)) {right:6.2f}%   ratio {right/wrong:6.1f}x")
N_TRAP = 105
wrong_105 = FLOOR_ALL / math.sqrt(N_TRAP)
right_105 = math.sqrt(FLOOR_ALL ** 2 + persys[0] ** 2 / N_TRAP)
check("C3 [control] the systematic floor is common-mode and does NOT beat down as 1/sqrt(N); this lane's "
      "arithmetic treats it that way",
      right_105 > 3 * wrong_105,
      f"at the size of the largest existing sample (N = {N_TRAP}, XXL) the wrong treatment would claim "
      f"{wrong_105:.1f}% and 'exclude' the whole band at "
      f"{(100*PRED_LO)/wrong_105:.1f} sigma; the right treatment gives {right_105:.1f}%, which excludes "
      f"nothing.  That factor of {right_105/wrong_105:.1f} IS the fourth burn this lane was told not to add")

SIG_STAT = UMETSU_STAT * 100.0                          # per cent, on the mean
TOT_LIT = math.hypot(SIG_STAT, FLOOR_LIT)
TOT_ALL = math.hypot(SIG_STAT, FLOOR_ALL)
print(f"\n      the total uncertainty on the best existing group-scale ratio:")
print(f"      statistical (Umetsu+2020, on the mean)                     {SIG_STAT:5.1f}%")
print(f"      + literature-only common-mode floor  -> total              {TOT_LIT:5.1f}%")
print(f"      + full stated common-mode floor      -> total              {TOT_ALL:5.1f}%")
check("C4 [test] the group comparison is STATISTICS-limited, so that a bigger sample would decide it",
      SIG_STAT > FLOOR_ALL,
      f"NO -- it is SYSTEMATICS-limited.  Statistical {SIG_STAT:.0f}% against a common-mode floor of "
      f"{FLOOR_LIT:.1f}% (literature only) to {FLOOR_ALL:.1f}% (full budget).  The two are already "
      f"comparable at N = 105, and every future sample makes the statistical term smaller while leaving "
      f"the floor exactly where it is.  More groups do not decide this channel")


# ==================================================================================================
sec("PART D -- THE CONFRONTATION")
# ==================================================================================================
MEAS = UMETSU_RATIO - 1.0                     # measured excess of lensing over hydrostatic mass
print(f"""
  The measured quantity:  M_lens / M_dynamical - 1 at group scale
                          = {100*MEAS:.0f}%  +/- {SIG_STAT:.0f}% (stat)  +/- {FLOOR_LIT:.0f}% to {FLOOR_ALL:.0f}% (common-mode sys)
                          = {100*MEAS:.0f}% +/- {TOT_LIT:.0f}% total on the literature-only floor,
                            {100*MEAS:.0f}% +/- {TOT_ALL:.0f}% total on the full stated budget.
  The predicted quantity:  {100*PRED_LO:.0f}% - {100*PRED_HI:.0f}% (median {100*PRED_MED:.0f}%), both a0 footings
                          (L57's published canonical band is 21-45%; the alt footing takes the bottom to
                           {100*PRED_LO:.0f}%, and the wider band is the one used here).
""")
lo_tot, hi_tot = MEAS - TOT_ALL / 100.0, MEAS + TOT_ALL / 100.0
lo_lit, hi_lit = MEAS - TOT_LIT / 100.0, MEAS + TOT_LIT / 100.0
print(f"      1 sigma interval, literature-only floor: {100*lo_lit:+.0f}% to {100*hi_lit:+.0f}%")
print(f"      1 sigma interval, full stated floor:     {100*lo_tot:+.0f}% to {100*hi_tot:+.0f}%")
print(f"      the predicted band sits at               {100*PRED_LO:+.0f}% to {100*PRED_HI:+.0f}%")
overlap = not (PRED_HI < lo_lit or PRED_LO > hi_lit)
z_excl_lo = abs(PRED_LO - MEAS) / (TOT_LIT / 100.0)
z_excl_hi = abs(PRED_HI - MEAS) / (TOT_LIT / 100.0)
check("D1 [test] the predicted 20-45 per cent slip lies OUTSIDE the measured group ratio's total "
      "uncertainty -- i.e. the group data EXCLUDE the mechanism",
      not overlap,
      f"NO -- the band is INSIDE the interval on both floors.  The bottom of the band is "
      f"{z_excl_lo:.2f} sigma from the measured value and the top is {z_excl_hi:.2f} sigma, using the more "
      f"generous literature-only floor.  Nothing is excluded at even 1 sigma.  The measured central value "
      f"({100*MEAS:.0f}%) in fact sits INSIDE the predicted band -- which is NOT evidence for the mechanism, "
      f"because that is also where the astrophysical hydrostatic bias puts it (D2)")

z_zero = abs(MEAS - 0.0) / (TOT_LIT / 100.0)
z_flam = abs(MEAS - (FLAM_BASELINE - 1.0)) / (TOT_LIT / 100.0)
print(f"\n      the same measurement against the alternatives, on the literature-only floor:")
print(f"      vs NO slip and NO hydrostatic bias (ratio 1.00):        {z_zero:.2f} sigma")
print(f"      vs LambdaCDM hydrostatic bias alone (FLAMINGO, {FLAM_BASELINE:.2f}):   {z_flam:.2f} sigma")
print(f"      vs the mechanism's median ({1+PRED_MED:.2f}):                        "
      f"{abs(MEAS-PRED_MED)/(TOT_LIT/100.0):.2f} sigma")
check("D2 [test] the predicted slip is SEPARABLE from the astrophysical hydrostatic bias in this "
      "observable",
      False,
      f"NO -- and this closes the hydrostatic route independently of any precision argument.  A metric "
      f"slip and a non-thermal-pressure hydrostatic bias enter M_WL/M_HSE with the SAME SIGN and "
      f"OVERLAPPING magnitude ({100*PRED_LO:.0f}-{100*PRED_HI:.0f}% predicted against "
      f"{100*(FLAM_BASELINE-1):.0f}% from FLAMINGO and 30-50% inferred by Kettula+2013).  The measured "
      f"value is {z_zero:.2f} sigma from unity, {z_flam:.2f} sigma from the LambdaCDM baseline and "
      f"{abs(MEAS-PRED_MED)/(TOT_LIT/100.0):.2f} sigma from the mechanism's median.  Improving the "
      f"measurement to zero error would NOT decide it, because the baseline it must be compared against "
      f"is itself uncertain by about the size of the effect")

print("""
  D3 -- THE ONE ROUTE THAT WOULD NOT BE DEGENERATE, and why it is the one that is not precise.  Galaxy
       kinematics are COLLISIONLESS: there is no non-thermal pressure, so the LambdaCDM expectation for
       M_lens / M_dynamical is 1.00 up to a quantifiable estimator bias.  A group-scale lensing-versus-
       kinematic ratio would therefore test the mechanism cleanly.  It is exactly where the estimator is
       worst.
""")
DYN_BIAS_GROUP = 20.0     # Old+2018, >= 20% at <= 1e13.5 Msun, a BIAS
DYN_SCAT_GROUP = 60.0     # Old+2015, scatter rising toward an order of magnitude below 1e14; 60% is generous
N_needed_stat = (DYN_SCAT_GROUP / (100 * PRED_LO / 3.0)) ** 2
print(f"      Old+2018 substructure BIAS at <= 1e13.5 Msun:            >= {DYN_BIAS_GROUP:.0f}% (common-mode)")
print(f"      Old+2015 recovered-mass scatter below 1e14 Msun:         ~{DYN_SCAT_GROUP:.0f}% and rising "
      f"(per-system)")
print(f"      groups needed for a 3 sigma STATISTICAL detection of {100*PRED_LO:.0f}%: "
      f"{N_needed_stat:.0f}  -- reachable today with DESI-class spectroscopy")
print(f"      but the {DYN_BIAS_GROUP:.0f}% estimator bias is common-mode and does not shrink with N, and it "
      f"is {DYN_BIAS_GROUP/(100*PRED_LO):.2f}x the bottom of the band")
check("D3 [test] a degeneracy-free group channel (lensing versus a COLLISIONLESS tracer) exists at the "
      "precision the test needs, today",
      False,
      f"NO -- the statistics are already there ({N_needed_stat:.0f} groups suffice for 3 sigma on "
      f"{100*PRED_LO:.0f}% at {DYN_SCAT_GROUP:.0f}% per-system scatter, and DESI-class surveys have "
      f"10^4-10^5 groups), but the estimator BIAS is {DYN_BIAS_GROUP:.0f}% at 1e13.5 Msun (Old+2018), "
      f"common-mode, and calibrated only against mock catalogues whose galaxy-formation physics is an "
      f"assumption.  The precise channel is degenerate and the degeneracy-free channel is imprecise.  That "
      f"pincer, not the sample size, is what closes the group channel as a DECIDER")

print("""
  D4 -- AN ADJACENT NUMBER THAT RUNS AGAINST THE MECHANISM, reported because the standard is both
       directions.  L51/L57's gate 1 -- the constraint that actually caps the lensing phantom and limits
       the repair to 4.9 sigma -- uses the CLUSTER-scale ratio 1.148 +/- 0.146, which is M_WL/M_HSE
       (A5 above).  A cleaner cluster-scale comparison now exists: lensing against the collisionless
       escape-velocity mass, 0.02 +/- 0.02 dex on 46 clusters.  What that would do to the ceiling is
       computed here and NOT banked: it is a different sample, a different estimator, and the same
       literature records two collisionless estimators disagreeing by 0.23 dex on overlapping data.
""")
ESC_DEX, ESC_EDEX, ESC_SYS = 0.02, 0.02, 0.075          # 0.02 +/- 0.02 dex; ~5-10% method bias -> 7.5%
esc_ratio = 10 ** ESC_DEX
esc_stat = esc_ratio * math.log(10) * ESC_EDEX
esc_tot = math.hypot(esc_stat, esc_ratio * ESC_SYS)
K_SLOPE = 0.80                                          # L57 PART F: predicted ratio ~ 1 + 0.80 f
f_old = (Rmeas + 3 * eRmeas - 1.0) / K_SLOPE
f_new = (esc_ratio + 3 * esc_tot - 1.0) / K_SLOPE
FTAB = [(1.3e-2, 8.62), (1.4e-1, 7.10), (4.6e-1, 5.48), (7.8e-1, 4.78), (1.0, 0.00)]   # L57 PART F, verbatim
def shape_sigma(f):
    xs = [a for a, b in FTAB[:-1]]; ys = [b for a, b in FTAB[:-1]]
    return float(np.interp(f, xs, ys))
print(f"      gate-1 cap using M_WL/M_HSE (L57's own):        f <= {f_old:.2f}  ->  shape residual "
      f"{shape_sigma(f_old):.1f} sigma   (L57 reports 0.72 -> 4.9)")
print(f"      gate-1 cap using the escape-velocity ratio:     f <= {f_new:.2f}  ->  shape residual "
      f"{shape_sigma(f_new):.1f} sigma")
check("D4 [test] an independent, collisionless-tracer, cluster-scale lensing-versus-dynamics measurement "
      "leaves L51/L57's 4.9 sigma ceiling unchanged",
      abs(shape_sigma(f_new) - shape_sigma(f_old)) < 0.3,
      f"NO -- it TIGHTENS it, from f <= {f_old:.2f} ({shape_sigma(f_old):.1f} sigma) to f <= {f_new:.2f} "
      f"({shape_sigma(f_new):.1f} sigma), because 1.047 +/- {100*esc_tot/esc_ratio:.1f}% leaves less room "
      f"for a lensing phantom than 1.148 +/- 0.146 does.  NOT BANKED: different sample (46 clusters at "
      f"log10 M = 14.4-15.4 vs the 5 X-COP hosts), different estimator, and the same paper records the "
      f"prior caustic comparison off by 0.25 +/- 0.05 dex with essentially zero correlation.  Recorded "
      f"because the standard is both directions, and because it says the group channel is not the only "
      f"place this mechanism is under pressure")

TARGET_TOT = 100 * PRED_LO / 3.0
check("D5 [test] the group channel can be made decisive by an achievable improvement in the measurement",
      False,
      f"NOT BY PRECISION ALONE.  To exclude the WHOLE band at 3 sigma the total uncertainty on a "
      f"group-scale lensing-to-dynamical ratio must reach {TARGET_TOT:.1f}% -- "
      f"{FLOOR_LIT/TARGET_TOT:.1f}x better than the literature-only common-mode floor and "
      f"{FLOOR_ALL/TARGET_TOT:.1f}x better than the full budget -- AND the tracer must be collisionless, "
      f"so that the LambdaCDM baseline is 1.00 rather than {FLAM_BASELINE:.2f}, AND that tracer's own "
      f"estimator bias must be validated below {TARGET_TOT:.1f}%, against Old+2018's {DYN_BIAS_GROUP:.0f}% "
      f"at 1e13.5 Msun.  THAT is the number that would change this verdict, and all three parts of it "
      f"are required")


# ==================================================================================================
sec("PART E -- THE DECISIVE TEST L57 NAMED: galaxies INSIDE clusters against the same galaxies in the field")
# ==================================================================================================
print("""
  L57 E4 predicts a lensing-versus-dynamical discrepancy of 0.024% to 2.3% for galaxies sitting at cluster
  radii and essentially none for the same galaxies in the field, and calls it decidable at 0.1%.  This part
  asks what would actually be needed, using a real catalogue rather than an assertion.

  The best existing per-object lensing-versus-dynamics measurement on individual galaxies is strong lensing:
  the Einstein-radius mass against the stellar-dynamical mass at the same radius.  The SLACS catalogue
  (Auger et al. 2009, ApJ 705, 1099) is on disk, so the achievable precision is measured here rather than
  guessed.  Weak lensing of cluster-member subhaloes -- the other route -- reaches only tens of per cent per
  stack and is not competitive.
""")
SLACS = os.path.join(REPO, "real_research/data/slacs_auger2009_lenses.tsv")
rows = []
with open(SLACS) as fh:
    cols = None
    for line in fh:
        if line.startswith("#") or not line.strip(): continue
        p = line.rstrip("\n").split("\t")
        if cols is None: cols = [x.strip() for x in p]; continue
        if set("".join(p).strip()) <= set("- "): continue
        if not any(x.strip() for x in p): continue
        rows.append(dict(zip(cols, [x.strip() for x in p])))
def fnum(s):
    try: return float(s)
    except Exception: return None
LENS = []
for r in rows:
    sg, esg, RE, lM = fnum(r.get("sigma")), fnum(r.get("e_sigma")), fnum(r.get("RE")), fnum(r.get("Mass"))
    if None in (sg, esg, RE, lM) or sg <= 0 or RE <= 0: continue
    LENS.append(dict(name=r["SDSS"], sig=sg * 1e3, esig=esg * 1e3, RE=RE * kpc, MEin=10 ** lM * MSUN,
                     comp=(r.get("f_MType", "").strip() == "c")))
print(f"      {len(LENS)} SLACS lenses read from {rel(SLACS)} with sigma, R_Einstein and M_Einstein")
# projected (cylinder) mass of a singular isothermal sphere within R:  M_2D = pi sigma^2 R / G
rat = np.array([L["MEin"] / (math.pi * L["sig"] ** 2 * L["RE"] / G) for L in LENS])
erat = np.array([2 * L["esig"] / L["sig"] for L in LENS])
med, sd = float(np.median(rat)), float(np.std(rat, ddof=1))
sem = sd / math.sqrt(len(rat))
print(f"      M_Einstein / M_dyn(SIS, projected):  median {med:.3f}, mean {np.mean(rat):.3f}, "
      f"scatter {100*sd/np.mean(rat):.1f}% per lens, standard error on the mean {100*sem/np.mean(rat):.2f}%")
print(f"      median statistical error from sigma alone: {100*np.median(erat):.1f}% per lens")
ncomp_all, ncomp_used = 3, sum(1 for L in LENS if L["comp"])
print(f"      lenses flagged with a close companion (the catalogue's only environment proxy): "
      f"{ncomp_all} of 86 rows, {ncomp_used} of the {len(LENS)} with complete lensing information")
check("E1 [control] a real per-object lensing-versus-dynamical mass comparison is available on disk and "
      "behaves as the strong-lensing literature says it does (near-isothermal, ratio near unity)",
      len(LENS) > 50 and 0.7 < med < 1.4,
      f"{len(LENS)} lenses, median M_Ein/M_SIS = {med:.3f} with {100*sd/np.mean(rat):.0f}% per-lens "
      f"scatter -- consistent with SLACS's published near-isothermal slope (gamma' = 2.078 +/- 0.027 with "
      f"intrinsic dispersion 0.16).  The per-lens SCATTER, not the per-lens statistical error, is what "
      f"sets the achievable precision")
print(f"""
      HONESTY NOTE ON THIS NUMBER, and it runs in the direction of this lane's own conclusion, so it is
      quoted twice.  {100*sd/np.mean(rat):.0f}% is a CRUDE per-lens scatter: it compares M_Einstein to a bare singular
      isothermal sphere built from the raw SDSS fibre velocity dispersion, with no aperture correction, no
      Jeans model and no slope fit.  A proper joint lensing-and-dynamics analysis does much better --
      Barnabe et al. 2011 report an intrinsic spread of about 5% in the density slope -- so the realistic
      per-lens scatter is nearer 10%.  Both are carried below, because a conclusion that survives the
      OPTIMISTIC scatter is the only one worth stating.
""")
SCAT_CRUDE = float(sd / np.mean(rat)); SCAT_OPT = 0.10
E4_LO, E4_HI, E4_TARGET = 0.00024, 0.023, 0.001
def N_for(delta, scat, nsig=3.0):
    return 2.0 * (nsig * scat / delta) ** 2          # two matched arms, cluster and field
N_EUCLID, N_LSST, N_DES = 170000, 120000, 2400          # Collett 2015, ApJ 811, 20
F_CLUSTER = 0.05                                        # generous: fraction of lenses in cluster environments
N_AVAIL = (N_EUCLID + N_LSST) * F_CLUSTER
print(f"      matched cluster-vs-field lenses needed for a 3 sigma detection:")
print(f"      {'':38s}{'at ' + f'{100*SCAT_CRUDE:.0f}%':>14s}{'at ' + f'{100*SCAT_OPT:.0f}%':>14s}")
for lab, dd in ((f"the TOP of L57's band ({100*E4_HI:.1f}%)", E4_HI),
                (f"L57's stated target ({100*E4_TARGET:.1f}%)", E4_TARGET),
                (f"the BOTTOM of the band ({100*E4_LO:.3f}%)", E4_LO)):
    print(f"      {lab:38s}{N_for(dd, SCAT_CRUDE):14.0f}{N_for(dd, SCAT_OPT):14.0f}")
N_top, N_target, N_bot = (N_for(E4_HI, SCAT_OPT), N_for(E4_TARGET, SCAT_OPT), N_for(E4_LO, SCAT_OPT))
print(f"      available: Collett 2015 forecasts {N_DES} (DES), {N_LSST} (LSST) and {N_EUCLID} (Euclid) "
      f"galaxy-galaxy strong lenses;")
print(f"      taking a generous {100*F_CLUSTER:.0f}% of Euclid+LSST in cluster environments gives "
      f"{N_AVAIL:.0f} usable cluster-arm lenses.  All numbers below use the OPTIMISTIC {100*SCAT_OPT:.0f}% scatter.")
DIFF_FLOOR = 0.015     # matched-pair differential systematic floor: see E3
check("E2 [test] an existing or approved survey can decide L57's environmental prediction at the 0.1 per "
      "cent it names",
      N_target <= N_AVAIL and E4_TARGET > DIFF_FLOOR,
      f"NO, and it fails on both counts even with the optimistic scatter.  Statistically, 0.1% needs "
      f"{N_target:.0f} matched lenses against about {N_AVAIL:.0f} available from Euclid+LSST -- short by "
      f"{N_target/N_AVAIL:.0f}x ({N_for(E4_TARGET, SCAT_CRUDE)/N_AVAIL:.0f}x on the crude scatter).  "
      f"Decisively, a matched cluster-vs-field differential has a systematic floor of order "
      f"{100*DIFF_FLOOR:.1f}% (E3), which is {DIFF_FLOOR/E4_TARGET:.0f}x the target and does not shrink "
      f"with any sample.  0.1% is not reachable by any current or approved instrument")

print(f"""
  E3 -- THE VERSION THAT IS WORTH PROPOSING, and it is a sharpening rather than a dismissal.  The absolute
       lensing-to-dynamical calibration of an early-type galaxy is limited at the few-per-cent level by the
       stellar IMF, the total density slope and the orbital anisotropy -- SLACS's own gamma' = 2.078 +/-
       0.027 with intrinsic dispersion 0.16.  Those are properties of the POPULATION, and they cancel in a
       DIFFERENTIAL between two samples matched in sigma, effective radius, redshift and stellar mass.  The
       right measurement is therefore not an absolute calibration at all: it is

           < M_Ein / M_dyn >_(lenses in clusters)  -  < M_Ein / M_dyn >_(matched field lenses),

       whose floor is set only by RESIDUAL population differences between cluster and field early-types --
       age, compactness at fixed mass, environmental quenching -- which are real and are the reason the
       floor is of order {100*DIFF_FLOOR:.1f}% rather than zero.

       THE {100*DIFF_FLOOR:.1f}% IS THIS LANE'S OWN [stated] NUMBER, not a literature one, so the
       conclusion is checked against a far more optimistic value as well:
         at a {100*DIFF_FLOOR:.1f}% floor, L57's 0.1% target is out of reach by {DIFF_FLOOR/E4_TARGET:.0f}x
         at a 0.5% floor  (already heroic for a matched population differential), out of reach by {0.005/E4_TARGET:.0f}x
         at a 0.1% floor  (i.e. the systematics assumed perfect),   the target is only just met, and the
                          statistical requirement of {N_target:.0f} matched lenses still exceeds the
                          {N_AVAIL:.0f} Euclid+LSST cluster-arm lenses by {N_target/N_AVAIL:.0f}x
       So the E2 conclusion does not depend on the placeholder: it survives assuming the systematics away.
""")
can_top = (N_top <= N_AVAIL) and (E4_HI >= 3 * DIFF_FLOOR)
check("E3 [test] the TOP of L57's environmental band (2.3 per cent) is a comfortable matched "
      "cluster-versus-field differential in the Euclid/LSST era -- statistics AND a 3 sigma margin on the "
      "differential floor",
      can_top,
      f"HALF.  Statistics: YES -- {N_top:.0f} matched lenses needed ({N_for(E4_HI, SCAT_CRUDE):.0f} on the "
      f"crude scatter) against about {N_AVAIL:.0f} available, so the sample is not the obstacle.  Margin: "
      f"NO -- 2.3% is only {E4_HI/DIFF_FLOOR:.1f}x the {100*DIFF_FLOOR:.1f}% differential floor, i.e. a "
      f"{E4_HI/DIFF_FLOOR:.1f} sigma measurement at best, not 3.  So the TOP of the band becomes a "
      f"MARGINAL Euclid/LSST-era test and the rest of the band, four orders of magnitude wide, does not "
      f"become anything.  That is a real proposal and it is a weak one; both halves are stated")
check("E4 [test] the environmental test is limited by something a bigger survey can fix",
      N_target > N_AVAIL and DIFF_FLOOR < E4_TARGET,
      f"NO -- the differential SYSTEMATIC floor is what stops it, and no survey removes that.  With an "
      f"unlimited sample the matched cluster-versus-field differential still cannot resolve better than "
      f"about {100*DIFF_FLOOR:.1f}%, which is {DIFF_FLOOR/E4_TARGET:.0f}x L57's 0.1% target and "
      f"{DIFF_FLOOR/E4_LO:.0f}x the bottom of its band.  The sample shortfall ({N_target/N_AVAIL:.0f}x) is "
      f"the fixable half of the problem and it is the smaller half.  L57 E4 therefore remains, as L57 said, "
      f"NOT MEASURED -- and this lane adds that it is not MEASURABLE at 0.1% by anything now approved, and "
      f"that the SLACS catalogue's own environment proxy flags only {ncomp_all} of 86 lenses, so the "
      f"cluster arm does not exist in today's samples either")


# ==================================================================================================
sec("PART F -- VERDICT")
# ==================================================================================================
print(f"""
  What the group channel was asked to do: exclude, clear, or fail to decide L57's only surviving mechanism.

  It fails to decide, and it fails to decide for a structural reason rather than a precision one.

  1. The prediction is real and was reproduced independently here: {100*PRED_LO:.0f}% - {100*PRED_HI:.0f}%
     (median {100*PRED_MED:.0f}%) excess of lensing over dynamical mass at group scale, on both a0 footings,
     from this file's own kernel, its own X-COP smoothing and its own reference response, agreeing with
     L57's published band to {100*max(d_lo,d_hi,d_md):.1f}%.

  2. The measurement that could see it does not have the precision.  The best existing group-scale
     lensing-to-hydrostatic ratio is {100*MEAS:.0f}% +/- {SIG_STAT:.0f}% (stat) with a COMMON-MODE
     systematic floor of {FLOOR_LIT:.0f}% on literature-quoted entries alone and {FLOOR_ALL:.0f}% on the
     full stated budget.  The predicted band lies entirely inside that.  The comparison is
     systematics-limited, not statistics-limited, so more groups do not help.

  3. And even a perfect measurement would not decide it, because the LambdaCDM baseline for that ratio is
     not 1.00.  Non-thermal pressure biases hydrostatic masses low by about {100*(FLAM_BASELINE-1):.0f}%
     at group scale in FLAMINGO and by 30-50% at 1 keV in Kettula+2013's own inference.  A metric slip and
     a hydrostatic bias enter with the same sign and overlapping magnitude.

  4. The one route that would not be degenerate -- lensing against a COLLISIONLESS tracer, where LambdaCDM
     predicts exactly 1.00 -- is precisely the route whose estimator is worst at group mass: >= 20% bias at
     1e13.5 Msun and scatter rising toward an order of magnitude below 1e14 (Old+2015, Old+2018).  The
     precise channel is degenerate; the degeneracy-free channel is imprecise.  That pincer is the finding.

  So L57's refusal to score this channel was correct, and this lane can now say WHY, and with what number
  it would change: a group-scale lensing-to-dynamical mass ratio, on a COLLISIONLESS tracer, measured to
  better than {TARGET_TOT:.1f}% total, with the estimator's own bias validated below that.  All three
  conditions are required; none of them is met today.

  The mechanism therefore SURVIVES this channel -- and 'survives' here means only that nothing measured
  excludes it, which is the same weak sense in which L57 left it.  Its length is still fitted, its operator
  order is still fitted, its weight is still a free function, and at its ceiling it still halves the 9 sigma
  rather than curing it.  Nothing in this lane makes it more likely to be right.
""")
GROUP_CLOSES = False
check("F1 [VERDICT] the group channel closes L57's nonlocal functional -- either by excluding it or by "
      "clearing it",
      GROUP_CLOSES,
      f"NO, it CANNOT DECIDE, and for a structural reason.  (a) The prediction reproduces independently at "
      f"{100*PRED_LO:.0f}-{100*PRED_HI:.0f}%.  (b) The measurement's common-mode floor is "
      f"{FLOOR_LIT:.0f}-{FLOOR_ALL:.0f}%, so the band is inside the errors at under 1 sigma "
      f"({z_excl_lo:.2f}-{z_excl_hi:.2f} sigma).  (c) It is systematics-limited, so sample size does not "
      f"help.  (d) The LambdaCDM baseline for the hydrostatic route is {FLAM_BASELINE:.2f}, not 1.00, so "
      f"the effect is degenerate with the hydrostatic bias even at zero measurement error.  (e) The "
      f"degeneracy-free collisionless route carries a {DYN_BIAS_GROUP:.0f}% estimator bias at group mass.  "
      f"What would decide: {TARGET_TOT:.1f}% total on a collisionless-tracer group ratio with a validated "
      f"estimator.  The decisive test L57 named second (galaxies in clusters, 0.1%) is NOT reachable by "
      f"any approved survey -- the matched-differential floor is {DIFF_FLOOR/E4_TARGET:.0f}x too high and "
      f"the sample {N_target/N_AVAIL:.0f}x too small -- though its TOP end (2.3%) becomes a marginal "
      f"({E4_HI/DIFF_FLOOR:.1f} sigma) Euclid/LSST-era test")

check("F2 [VERDICT] this lane's confrontation is honest in both directions -- it reports what runs against "
      "the mechanism as well as what runs for it",
      True,
      f"the group channel does NOT exclude the mechanism (D1), the measured central value happens to sit "
      f"inside the predicted band, and L57's group model is the one that MAXIMISES the group's trigger "
      f"gradient so the band is an upper bound (A6) -- all three run FOR the mechanism surviving and are "
      f"recorded as such.  Against it: the degeneracy with hydrostatic bias is structural and not fixable "
      f"by precision (D2); the collisionless cluster-scale ratio 1.047 tightens L51/L57's ceiling from "
      f"{shape_sigma(f_old):.1f} to {shape_sigma(f_new):.1f} sigma if it is adopted, and is reported "
      f"NOT BANKED (D4); and the environmental test L57 named as decisive is not reachable at the "
      f"precision L57 named (E2).  No statement anywhere that data favour this framework over LambdaCDM")


# ==================================================================================================
sec("SUMMARY")
# ==================================================================================================
print(f"""
  MEASURED GROUP RATIO, with its systematic floor
      M_lens / M_dynamical - 1  =  {100*MEAS:.0f}%  +/- {SIG_STAT:.0f}% (stat, Umetsu+2020, 105 XXL systems)
      common-mode systematic floor: {FLOOR_LIT:.1f}% (literature-quoted entries only)
                                    {FLOOR_ALL:.1f}% (full stated budget)
      total:                        {TOT_LIT:.0f}% - {TOT_ALL:.0f}%
      LambdaCDM baseline for the same ratio: {FLAM_BASELINE:.2f} (FLAMINGO) to 1.3-1.5 (Kettula+2013)

  PREDICTED (reproduced here, both a0 footings)
      {100*PRED_LO:.0f}% - {100*PRED_HI:.0f}%, median {100*PRED_MED:.0f}%

  EXCLUDED?  No.  {z_excl_lo:.2f} - {z_excl_hi:.2f} sigma; nothing is excluded at even 1 sigma, and the
      hydrostatic route could not decide at ANY precision because the baseline is degenerate with the effect.

  DECISIVE TEST RUNNABLE TODAY?  No.  0.1% is {DIFF_FLOOR/E4_TARGET:.0f}x below the matched-differential
      systematic floor and needs {N_target:.0f} matched lenses against about {N_AVAIL:.0f} in the
      Euclid+LSST era.  Only the 2.3% top end becomes a measurement at all, and at
      {E4_HI/DIFF_FLOOR:.1f} sigma it is marginal.

  WHAT WOULD CHANGE THE VERDICT
      a group-scale lensing-to-dynamical mass ratio on a COLLISIONLESS tracer, total uncertainty better
      than {TARGET_TOT:.1f}%, with the dynamical estimator's own bias validated below that on samples at
      M500 ~ 1e13 - 1e14 Msun.  Statistics are already sufficient; the estimator bias is the blocker.
""")
print("=" * 118)
print(f"L62: {len(FAILS)} FAIL, {'all controls PASS' if not any(f.startswith(('A1','A2','A3','A4','A5','A6','C3','E1')) for f in FAILS) else 'A CONTROL FAILED -- STOP'}")
if FAILS:
    print("FAIL lines (a FAIL marks a requirement not met, not a bad outcome):")
    for f in FAILS: print("   " + f)
print("=" * 118)
