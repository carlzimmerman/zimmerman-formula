r"""
CFG86 -- INDEPENDENT RE-DERIVATION OF CFG80 (LCDM comparator for the SLACS lensing-vs-dynamics gap of CFG33), FROZEN BEFORE ANY RUN
=====================================================================================================================================

Written before this script was executed. Disclosed reading before writing (all non-LCDM): CFG80_FROZEN_CRITERIA.md, CFG80_README.md, CFG80 LEDGER row,
CFG33 README + docstring, CFG69 README + docstring, docstrings of hunt_2026/h53, h9, h48, and the on-disk data (real_research/data/
slacs_auger2009_lenses.tsv, atlas3d_fj_table.tsv). NOT opened before my run: the CFG80 script, .out, _results.json (and no CFG33/CFG69/CFG45/h48
CODE). One non-LCDM plumbing count was done before this docstring: rows with numeric zlens,zsrc,sigma,RE,Mass,Fs,logMs = 70 of 85 lenses; ATLAS3D 258
usable rows, 187 with qual>=1. No halo mass, projected mass, alpha or gap was computed for any object.

QUESTION.  Through the CFG33 pipeline (70 SLACS lenses' Einstein masses vs ATLAS3D Q>=1 JAM masses, linear fit of log alpha_dyn in log sigma_e
evaluated at the lenses' SDSS sigma, median statistic, bootstrap, 0.10-dex floor) does a standard LCDM halo (Moster+2013 SHMR, Duffy+2008 NFW, Newtonian)
show the lensing-dynamics gap B shows (+0.15..+0.17 dex)?  Reproduce CFG80's headline; then attack the wording "B-specific statistically".

MODEL as I read it (all mine, no code from the lanes)
  Cosmology for lens geometry: flat, Om=0.3, h=0.7 (Auger). D_A(z1,z2) = c/H0/(1+z2) Int dz/E.  Sigma_crit = c^2/(4 pi G) D_s/(D_l D_ls).
      M_E = pi R_E^2 Sigma_crit with R_E = tabulated RE (kpc).  Validation: log10 M_E vs tabulated 'Mass' (2 decimals).
  Stars: lens projected stellar mass in R_E = alpha * Fs * M_E (Fs = Auger's Salpeter f_*, M_Salp = 10^logMs).  ATLAS3D: M_Salp = 10^(logML_Salp+logL),
      M_JAM = 10^(logML_JAM+logL), r_1/2 = 10^logr12 arcsec * Dist/206265 (kpc, 3D half-light sphere), sigma_e = 10^logsig_e; half of the stars inside r_1/2.
  Halo: M_h = Moster+2013 z=0 SHMR inverted on a fine log grid (M_h 1e9..10^15.5; np.interp; clamped outside) evaluated at M_* = alpha*M_Salp (the 'solved tie').
      Moster: M*/Mh = 2N[(Mh/M1)^-beta + (Mh/M1)^gamma]^-1, log M1=11.590, N=0.0351, beta=1.376, gamma=0.608 (from memory of the paper; endpoints checked).
      NFW 200c, rho_c(z=0) = 3 H0^2/(8 pi G), H0 = 67.4 (h=0.674); c = Duffy+2008 full 200c: 5.71 (Mh/(2e12/h))^-0.084 (h=0.674); m(t)=ln(1+t)-t/(1+t);
      f_b = 0.02237/(0.02237+0.1200) = 0.1571; added mass (1-f_b) M_NFW.  Newtonian, no phantom, no adiabatic contraction, no SHMR scatter.
  Lens solve:  alpha Fs + (1-f_b) M2D(<R_E; M_h(alpha M_Salp))/M_E = 1, bracket log M_* in [8,13.5] (brentq).  M2D = analytic untruncated NFW cylinder
      (Bartelmann 1996 / Wright & Brainerd 2000), X = c R/R200, h(X) = ln(X/2) + 2/sqrt(1-X^2) artanh sqrt((1-X)/(1+X)) (X<1), arctan form (X>1), h(1)=1+ln(1/2);
      M2D = M_h h(X)/m(c).   alpha_lens = M_*/M_Salp.
  ATLAS solve: 0.5 M_* + (1-f_b) M_NFW(<r_1/2; M_h(M_*)) = M_JAM/2 on the same bracket; alpha_dyn = M_*/M_Salp.  3D NFW x=r/R200 clipped to [1e-4,5].
      No root => excluded and counted.
  Statistic: y = log10 alpha_dyn regressed on (log10 sigma_e - 2.3) (unweighted least squares); Delta = median_i [log10 alpha_lens,i - fit(log10 sigma_lens,i - 2.3)]
      (lens sigma = SDSS 'sigma', no aperture correction); error = std of 2000 bootstraps (lenses and calibrators resampled, fit redone; my own RNG,
      default_rng(86): calibrators drawn first, then lenses -- CFG33's draw order is unknown to me, so the error carries ~1.6% Monte-Carlo noise);
      sigma_tot = sqrt(err^2+0.10^2); z = Delta/sigma_tot; z_stat = Delta/err.  Gate PASS iff |z|<=2 and >=35 lenses solved and >=94 calibrated.
  B's side is NOT re-derived (needs nu_mono and h53's phantom projection, which I did not read): B's numbers are TAKEN from the CFG33 README
      (gap +0.159/+0.171/+0.152/+0.168 for canonical V/I, alt V/I; stat errors 0.021/0.022/0.022/0.022) and used only as fixed comparison values.
      Consequently my B-minus-LCDM significance is UNPAIRED (err = sqrt(errB^2+errL^2)), more conservative than CFG80's paired bootstrap.

PASS LINES (reproduction of CFG80's README headline; CFG80 numbers as stated in its README/ledger, read before my run)
  P1 exact: 70 lenses, 258 ATLAS, 187 Q>=1, 70/70 lenses solved and 187/187 calibrated (LCDM base), no exclusions.
  P2 base: Delta_L = +0.037 dex, error 0.025, z=+0.36 (floor), z_stat=+1.5, alpha_lens ~0.82, alpha_dyn(at lenses) ~0.76.
      REPRODUCED-3dp if |Delta-0.037|<=0.0015; REPRODUCED-within-resolution if <=0.005; else the difference is stated as a non-reproduction.
      err within +-0.003; z within +-0.05; z_stat within +-0.2.
  P3 variants (same tolerance): V1 Dutton-Maccio c (log10 c = 0.905-0.101 log10(Mh/(1e12/h)), h=0.674): +0.011; V2 Duffy relaxed 200c (6.71,-0.091): +0.019;
      V3 all Mh x1/3: +0.075 (3.4 z_stat); V4 all Mh x3: -0.033; all Mh x100: -0.294, z=-2.61 (gate FAILS); x33 passes (CFG80 quotes -1.80 sigma in its MUTATE);
      x300 fails (CFG80: -3.50).  Gate-weakness statement to reproduce: fails at x100, passes at x33.
  P4 diagnostics: median log Mh lenses 14.36 (range 12.51..15.50), calibrators 12.13; median dark fraction inside R_E 42%, 3D dark fraction inside
      r_1/2 12%; 1 lens above the Moster grid top; no inner-clip galaxies.  Class SPECIFIC-TO-B (z<=2 with floor), not NON-DISCRIMINATING (x100 outcome differs).
  P5 caveats to reproduce: (a) with Moster tied to alpha x Salpeter masses the lens halos have median ~10^14.4; (b) halos x1/3 keep ~half of B's gap at 3.4 z_stat;
      (c) z-consistent halos: CFG80 says NOT computed; I compute it as an extension and report it separately (no CFG80 number to compare).

CONTROLS (a failed control is a failure; nothing tuned after seeing results)
  C0 data/plumbing: 70/258/187 counts; log M_E (mine) vs tabulated 'Mass': max |diff| <= 0.01 dex (table rounds to 0.005); rho_c(0.674) = 1.2605e11 within 3e-4 rel;
      f_b = 0.1571 within 5e-4; Moster inversion endpoints: M_*(Mh=1e9) = 10^4.28+-0.01 and M_*(Mh=10^15.5)=10^11.97+-0.01; monotonic inversion.
  C1 NFW closed forms: M(<R200) = M_h to 1e-12; monotone; R200 from 200 rho_c 4pi/3 R^3 = M_h to 1e-12; c(Mh) at 2e12/h equals 5.71 to 1e-12.
  C2 projection: analytic M2D vs my own numerical projection (line-of-sight Sigma(R) integrated with scipy.quad over the disc, and shell projection)
      to 1e-6 relative over M_h 1e10..1e16, R 0.3..100 kpc, all three c relations, X<1, X>1; continuity across X=1 to 1e-6; h(1)=1+ln(1/2); M2D >= M3D(<R).
  C3 solves: kbar(alpha_lens)=1 to 1e-9 at every solved lens; M_LCDM(<r_1/2)=M_JAM/2 to 1e-9 at every calibrator; halo switched off (Mh x1e-30) returns
      alpha_lens = 1/Fs and alpha_dyn = M_JAM/M_Salp to 1e-9; halo only lowers alpha.
  C4 estimator closed forms: (i) lens alphas placed exactly on the fitted line give Delta=0 to 1e-12; (ii) lens alphas = 10^k x fit give Delta = k to 1e-12;
      (iii) the fit recovers a synthetic log-linear alpha_dyn(sigma) to 1e-10; (iv) a pure Salpeter zero-point rescale of the lens table M_Salp->10^d M_Salp,
      Fs->10^d Fs shifts the LCDM lens alphas by exactly 10^-d (halo tie unchanged since physical M_* is the same) and Delta by -d to 1e-9 (checked at d=+-0.1 by full re-solve).
  C5 MUTATE witness: the halo mass entering every base solve / Moster(M_*) = 1 to 1e-12 (passes in the main run; fails under MUTATE by construction, ratio 100).
  H1 [HEADLINE] LCDM passes the CFG33 gate (P1 counts and |z|<=2).  MUTATE=1 multiplies every LCDM halo mass by 100: H1 must FAIL (rc 1), failing set must differ
      from the main run's.  C6: the gate outcome at x100 differs from x1 (else NON-DISCRIMINATING).

HALO-MASS LADDER (reported, not tuned): multipliers 0.01,0.03,0.1,1/3,1,3,10,33,100,300 on every halo (both lenses and calibrators): Delta, err, z (floor), z_stat, gate;
      report the interval of multipliers on which the gate passes.

ATTACK ON THE WORDING "B-specific statistically" (declared here, before any run)
  Definitions, evaluated per cell using B's fixed README gaps (worst case = smallest, alt V +0.152, err 0.022; and canonical V +0.159):
    S_a : LCDM's own statistical gap is not significant: |Delta_L| <= 2 err_L      (LCDM does not share B's 7-8 sigma statistical gap)
    S_b : B - LCDM > 2 sqrt(errB^2 + errL^2), unpaired  (B's excess over LCDM is significant)
    S_a_f: |Delta_L| <= 2 sqrt(err_L^2+0.10^2) (LCDM passes with the floor).
    'B-specific statistically' SUPPORTED in a cell iff S_a AND S_b.
  Cells in the DECLARED RANGE (54): halo multiplier m in {1/3,1,3}; halo tie in {solved Salpeter-tied (base): M_*=alpha M_Salp;  solved Chabrier-equivalent:
      M_* = s alpha M_Salp;  fixed Chabrier-equivalent: M_h = Moster(s M_Salp) for calibrators and Moster(10^logMc) for lenses, independent of alpha}, where s =
      median over the 70 lenses of 10^(logMc-logMs) (Auger); z-evaluation in {z=0 (base); z-consistent: lens halo with rho_c(z_l)=rho_c0[0.3(1+z)^3+0.7], Duffy (1+z)^-0.47
      (relaxed (1+z)^-0.44; Dutton-Maccio a(z),b(z) with a=0.520+0.385exp(-0.617 z^1.21), b=-0.101+0.026 z) and Moster+2013 z-evolution at z_l (M1: 11.590+1.195 z/(1+z);
      N: 0.0351-0.0247 z/(1+z); beta: 1.376-0.826 z/(1+z); gamma: 0.608+0.329 z/(1+z)), ATLAS3D calibrators at z=0}; c in {Duffy full, Duffy relaxed, Dutton-Maccio}.
      3x3x2x3 = 54.  Extended context (not counted in the verdict): m in {0.1, 10}.
  Extra decomposition at base (reported): z-consistent pieces separately (rho_c(z) only; Duffy (1+z) only; Moster z-evolution only).
  IMF/alpha zero-point axis: a Salpeter zero-point offset d between Auger and ATLAS3D (C4iv shows it shifts LCDM's Delta by exactly -d; I ASSUME B's shifts by -d as well,
      as CFG80 asserts 'almost equally'; B's side is not re-derived), d in {-0.10,-0.05,0,+0.05,+0.10} (the 0.10 floor).  S_b is d-invariant by construction; S_a is not.
  VERDICT RULES (declared): for wording W = S_a AND S_b over the 54 cells at d=0: ROBUST if >=90% of cells support W; CONDITIONAL if 50-90% (state which axis levels flip);
      NOT SUPPORTED if <50%.  Separately state which single axis levels flip S_a (marginal fractions) and whether S_b ever flips.  Then add the d axis: state the d-range in which the
      base cell supports W, and whether the +-0.10 floor range is inside it.

STANDING: kappa=1/2 is FITTED; nothing here says the data favour B or LCDM; no claim that the theory is closed.  Non-reproduction is a valid outcome.
Run: python3 CFG86_lcdm_slacs_rederivation.py   (MUTATE=1 for the control)
"""

import os, sys, io, csv, json, math, hashlib
import numpy as np
from scipy.integrate import quad
from scipy.optimize import brentq

HERE = os.path.dirname(os.path.abspath(__file__))
MUTATE = os.environ.get("MUTATE", "0") == "1"
MODE = "MUTATE" if MUTATE else "main"
DATA = "/Users/carlzimmerman/new_physics/zimmerman-formula/real_research/data/"
LENS_F = DATA + "slacs_auger2009_lenses.tsv"
ATL_F = DATA + "atlas3d_fj_table.tsv"

FAILS = []
def check(name, ok, detail=""):
    print(("PASS " if ok else "FAIL ") + name + (("  " + detail) if detail else ""))
    if not ok:
        FAILS.append(name)

# frozen text unchanged?
frozen = open(os.path.join(HERE, "CFG86_FROZEN.txt")).read().strip()
check("FROZEN docstring == CFG86_FROZEN.txt", frozen == (__doc__ or "").strip(),
      "sha256 " + hashlib.sha256(frozen.encode()).hexdigest()[:16])
print("MODE", MODE)

# ---------------- constants ----------------
C_KMS = 299792.458
G = 4.30091e-6            # kpc (km/s)^2 / Msun
FB = 0.02237 / (0.02237 + 0.1200)
H_HALO = 0.674
H0_HALO = 67.4 / 1000.0   # km/s/kpc
RHOC0 = 3 * H0_HALO**2 / (8 * np.pi * G)   # Msun/kpc^3
H_LENS = 0.7
OM, OL = 0.3, 0.7
HALO_MULT_GLOBAL = 100.0 if MUTATE else 1.0
QUAL_MIN = 1
SIGMA_FLOOR = 0.10
NBOOT = 2000

# ---------------- data ----------------
def load_lenses():
    lines = [l for l in open(LENS_F) if not l.startswith("#")][1:]
    rows = list(csv.reader(io.StringIO("".join(lines)), delimiter="\t"))
    hdr = rows[0]
    data = [r for r in rows[3:] if len(r) == len(hdr)]
    ix = {h: i for i, h in enumerate(hdr)}
    need = ["zlens", "zsrc", "sigma", "RE", "Mass", "Fs", "logMs"]
    out = []
    for r in data:
        if all(r[ix[c]].strip() != "" for c in need):
            d = {c: float(r[ix[c]]) for c in need}
            d["logMc"] = float(r[ix["logMc"]]) if r[ix["logMc"]].strip() else float("nan")
            d["name"] = r[ix["SDSS"]]
            out.append(d)
    return len(data), out

def load_atlas():
    rows = [l.rstrip("\n").split("\t") for l in open(ATL_F) if not l.startswith("#")]
    hdr = rows[0]
    ix = {h: i for i, h in enumerate(hdr)}
    out = []
    for r in rows[1:]:
        try:
            d = {c: float(r[ix[c]]) for c in ["logsig_e", "logML_JAM", "logL", "logML_Salp", "logr12", "Dist_Mpc"]}
            d["qual"] = int(r[ix["qual"]])
            d["name"] = r[ix["name"]]
            out.append(d)
        except ValueError:
            continue
    return len(rows) - 1, out

n85, LENS = load_lenses()
nrowsA, ATL = load_atlas()
check("C0 counts: 85 rows -> 70 lenses", (n85, len(LENS)) == (85, 70), f"{n85},{len(LENS)}")
check("C0 counts: 258 ATLAS usable", len(ATL) == 258, str(len(ATL)))
CAL = [a for a in ATL if a["qual"] >= QUAL_MIN]
check("C0 counts: 187 Q>=1", len(CAL) == 187, str(len(CAL)))

# ---------------- lens geometry ----------------
def Ez(z): return math.sqrt(OM * (1 + z)**3 + OL)
def comoving_kpc(z1, z2):
    dh = C_KMS / (100 * H_LENS) * 1000.0   # kpc
    return dh * quad(lambda z: 1.0 / Ez(z), z1, z2, epsabs=1e-13, epsrel=1e-13)[0]
def sigma_crit_ME(zl, zs, RE):
    Dl = comoving_kpc(0, zl) / (1 + zl)
    Ds = comoving_kpc(0, zs) / (1 + zs)
    Dls = comoving_kpc(zl, zs) / (1 + zs)
    Sc = C_KMS**2 / (4 * np.pi * G) * Ds / (Dl * Dls)   # Msun/kpc^2
    return Sc, np.pi * RE**2 * Sc

L_R = np.array([d["RE"] for d in LENS])
L_z = np.array([d["zlens"] for d in LENS])
L_ME = np.array([sigma_crit_ME(d["zlens"], d["zsrc"], d["RE"])[1] for d in LENS])
L_MS = 10**np.array([d["logMs"] for d in LENS])
L_FS = np.array([d["Fs"] for d in LENS])
L_MC = 10**np.array([d["logMc"] for d in LENS])
L_sig = np.array([d["sigma"] for d in LENS])
L_x = np.log10(L_sig) - 2.3
dME = np.abs(np.log10(L_ME) - np.array([d["Mass"] for d in LENS]))
check("C0 M_E vs tabulated Mass <=0.01 dex", dME.max() <= 0.01, f"max {dME.max():.4f} median {np.median(dME):.4f}")
S_CHAB = float(np.median(10**(np.array([d["logMc"] for d in LENS]) - np.array([d["logMs"] for d in LENS]))))
print("s (Chab/Salp median) =", round(S_CHAB, 4), " log10 =", round(math.log10(S_CHAB), 4))

A_sig = 10**np.array([a["logsig_e"] for a in CAL])
A_x = np.log10(A_sig) - 2.3
A_L = 10**np.array([a["logL"] for a in CAL])
A_MJ = 10**np.array([a["logML_JAM"] for a in CAL]) * A_L
A_MS = 10**np.array([a["logML_Salp"] for a in CAL]) * A_L
A_r = 10**np.array([a["logr12"] for a in CAL]) * np.array([a["Dist_Mpc"] for a in CAL]) * 1000.0 / 206264.806

# ---------------- Moster SHMR ----------------
def shmr_logMs(logMh, z=0.0, parts=True):
    zz = z / (1 + z)
    logM1 = 11.590 + 1.195 * zz
    N = 0.0351 - 0.0247 * zz
    beta = 1.376 - 0.826 * zz
    gam = 0.608 + 0.329 * zz
    x = 10**(logMh - logM1)
    return logMh + np.log10(2 * N / (x**(-beta) + x**gam))

_GRID = np.linspace(9.0, 15.5, 13001)
_inv_cache = {}
def halo_logmass_fn(z=0.0):
    key = round(z, 6)
    if key not in _inv_cache:
        ls = shmr_logMs(_GRID, z)
        assert np.all(np.diff(ls) > 0)
        _inv_cache[key] = ls
    ls = _inv_cache[key]
    def f(logMs):
        return float(np.interp(logMs, ls, _GRID))   # clamps at 9 and 15.5
    return f

ls0 = shmr_logMs(np.array([9.0, 15.5]), 0.0)
check("C0 Moster endpoints", abs(ls0[0] - 4.28) <= 0.01 and abs(ls0[1] - 11.97) <= 0.01, f"{ls0[0]:.3f} {ls0[1]:.3f}")
check("C0 rho_c(0.674)=1.2605e11 Msun/Mpc^3", abs(RHOC0 * 1e9 / 1.2605e11 - 1) < 3e-4, f"{RHOC0*1e9:.5e}")
check("C0 f_b = 0.1571", abs(FB - 0.1571) < 5e-4, f"{FB:.5f}")

# ---------------- NFW ----------------
def c_duffy_full(Mh, z=0.0, zc=False):
    return 5.71 * (Mh / (2e12 / H_HALO))**-0.084 * ((1 + z)**-0.47 if zc else 1.0)
def c_duffy_rel(Mh, z=0.0, zc=False):
    return 6.71 * (Mh / (2e12 / H_HALO))**-0.091 * ((1 + z)**-0.44 if zc else 1.0)
def c_dm(Mh, z=0.0, zc=False):
    if zc:
        a = 0.520 + (0.905 - 0.520) * math.exp(-0.617 * z**1.21)
        b = -0.101 + 0.026 * z
    else:
        a, b = 0.905, -0.101
    return 10**(a + b * math.log10(Mh / (1e12 / H_HALO)))
CREL = {"duffy": c_duffy_full, "relaxed": c_duffy_rel, "dm": c_dm}

def mfun(t): return np.log1p(t) - t / (1 + t)

def r200(Mh, rhoc): return (3 * Mh / (4 * np.pi * 200 * rhoc))**(1 / 3)

def m3d(r, Mh, c, R200):
    x = np.clip(r / R200, 1e-4, 5.0)
    return Mh * mfun(c * x) / mfun(c)

def hfun(X):
    X = float(X)
    if abs(X - 1) < 1e-7:
        return 1 + math.log(0.5)
    if X < 1:
        s = math.sqrt(1 - X * X)
        eps = X * X / (1 + s)
        return -X * X * math.log(X) / (s * (1 + s)) + (math.log1p(-eps / 2) + eps * math.log(2)) / s
    return math.log(X / 2) + math.acos(1 / X) / math.sqrt(X * X - 1)

def m2d(R, Mh, c, R200):
    return Mh * hfun(c * R / R200) / float(mfun(c))

# ---------------- model config ----------------
class Cfg:
    def __init__(self, mult=1.0, tie="solved_salp", zmode="z0", crel="duffy", dzero=0.0,
                 zrho=False, zc=False, zmost=False):
        self.mult = mult; self.tie = tie; self.crel = crel; self.dzero = dzero
        if zmode == "full":
            zrho = zc = zmost = True
        self.zrho, self.zc, self.zmost = zrho, zc, zmost
    def label(self):
        z = "zfull" if (self.zrho and self.zc and self.zmost) else ("z0" if not (self.zrho or self.zc or self.zmost) else
            "z[" + ("r" if self.zrho else "") + ("c" if self.zc else "") + ("m" if self.zmost else "") + "]")
        return f"m={self.mult:g} tie={self.tie} {z} c={self.crel}"

def rhoc_z(z): return RHOC0 * (OM * (1 + z)**3 + OL)

def halo_props(cfg, logMs_fixed_or_solved, z, is_lens, i):
    """return (Mh, c, R200, logMh_unmult) for the halo, given the stellar mass argument logMs (solved) / fixed."""
    raise NotImplementedError

def make_halo(cfg, logMs, z, fixed_logMs=None):
    zM = z if cfg.zmost else 0.0
    f = halo_logmass_fn(zM)
    if cfg.tie == "solved_salp":
        lm = f(logMs)
    elif cfg.tie == "solved_chab":
        lm = f(logMs + math.log10(S_CHAB))
    else:
        lm = f(fixed_logMs)
    Mh = 10**lm * cfg.mult * HALO_MULT_GLOBAL
    zc_ = z if cfg.zc else 0.0
    c = CREL[cfg.crel](Mh, zc_, cfg.zc)
    rc = rhoc_z(z) if cfg.zrho else RHOC0
    return Mh, c, r200(Mh, rc), lm

def kbar_lens(logMs, i, cfg, ret=False):
    d = cfg.dzero
    MS = L_MS[i] * 10**d; FS = L_FS[i] * 10**d
    Mstar = 10**logMs
    Mh, c, R200, lm = make_halo(cfg, logMs, L_z[i], fixed_logMs=math.log10(L_MC[i]))
    halo = (1 - FB) * m2d(L_R[i], Mh, c, R200) / L_ME[i]
    k = Mstar / MS * FS + halo
    if ret:
        return k, Mh, halo
    return k - 1.0

def solve_lens(i, cfg):
    f = lambda lm: kbar_lens(lm, i, cfg)
    if f(8.0) > 0 or f(13.5) < 0:
        return None
    lm = brentq(f, 8.0, 13.5, xtol=1e-12, rtol=1e-14)
    return lm

def dyn_resid(logMs, j, cfg, ret=False):
    Mstar = 10**logMs
    fixed = math.log10(A_MS[j] * S_CHAB)
    Mh, c, R200, lm = make_halo(cfg, logMs, 0.0, fixed_logMs=fixed)
    Mdm = (1 - FB) * float(m3d(A_r[j], Mh, c, R200))
    tot = 0.5 * Mstar + Mdm
    if ret:
        return tot, Mh, Mdm, R200
    return tot - A_MJ[j] / 2

def solve_dyn(j, cfg):
    f = lambda lm: dyn_resid(lm, j, cfg)
    if f(8.0) > 0 or f(13.5) < 0:
        return None
    return brentq(f, 8.0, 13.5, xtol=1e-12, rtol=1e-14)

# ---------------- statistic ----------------
def gap_stat(la, xl, ld, xd, seed=86, nboot=NBOOT):
    """la: log alpha_lens (solved lenses), xl their log sigma-2.3; ld,xd calibrators. returns Delta, err."""
    p = np.polyfit(xd, ld, 1)
    delta = float(np.median(la - np.polyval(p, xl)))
    rng = np.random.default_rng(seed)
    nc, nl = len(xd), len(xl)
    out = np.empty(nboot)
    for b in range(nboot):
        ic = rng.integers(0, nc, nc)
        il = rng.integers(0, nl, nl)
        pb = np.polyfit(xd[ic], ld[ic], 1)
        out[b] = np.median(la[il] - np.polyval(pb, xl[il]))
    return delta, float(np.std(out)), p

def run_cfg(cfg, nboot=NBOOT, full=False):
    lm_l = [solve_lens(i, cfg) for i in range(len(LENS))]
    lm_d = [solve_dyn(j, cfg) for j in range(len(CAL))]
    li = [i for i, v in enumerate(lm_l) if v is not None]
    dj = [j for j, v in enumerate(lm_d) if v is not None]
    la = np.array([lm_l[i] - math.log10(L_MS[i] * 10**cfg.dzero) for i in li])
    ld = np.array([lm_d[j] - math.log10(A_MS[j]) for j in dj])
    res = dict(cfg=cfg.label(), n_lens=len(li), n_cal=len(dj))
    UNFIT = (len(li) < 35) or (len(dj) < 94)
    if len(li) < 5 or len(dj) < 5:
        res.update(delta=float("nan"), err=float("nan"), z=float("nan"), zstat=float("nan"), gate="UNFIT"); return res
    delta, err, p = gap_stat(la, L_x[li], ld, A_x[dj], nboot=nboot)
    st = math.sqrt(err**2 + SIGMA_FLOOR**2)
    z = delta / st; zs = delta / err
    gate = "UNFIT" if UNFIT else ("PASS" if abs(z) <= 2 else ("FAIL+" if z > 0 else "FAIL-"))
    res.update(delta=delta, err=err, z=z, zstat=zs, gate=gate, slope=float(p[0]))
    if full:
        res.update(_li=li, _dj=dj, _lm_l=lm_l, _lm_d=lm_d, _la=la, _ld=ld, _p=p)
    return res

def fmt(r):
    return (f"{r['cfg']:52s} n={r['n_lens']}/{r['n_cal']}  Delta={r['delta']:+.4f} err={r['err']:.4f}  "
            f"z={r['z']:+.2f} zstat={r['zstat']:+.2f} {r['gate']}")

# =============================== CONTROLS ===============================
print("\n=== CONTROLS ===")
# C1 NFW
worst = 0.0; mono = True
for lgM in np.arange(9.0, 17.6, 0.25):
    Mh = 10**lgM
    for nm, cr in CREL.items():
        c = cr(Mh); R = r200(Mh, RHOC0)
        worst = max(worst, abs(float(m3d(R, Mh, c, R)) / Mh - 1))
        rr = R * np.linspace(1e-3, 1, 200)
        mono &= bool(np.all(np.diff(m3d(rr, Mh, c, R)) > 0))
        worst = max(worst, abs((200 * RHOC0 * 4 * np.pi / 3 * R**3) / Mh - 1))
check("C1 M(<R200)=Mh and R200 identity to 1e-12; monotone", worst < 1e-12 and mono, f"worst {worst:.2e}")
check("C1 c(Mh=2e12/h)=5.71", abs(c_duffy_full(2e12 / H_HALO) - 5.71) < 1e-12)

# C2 projection vs numerical
def rho_nfw(r, Mh, c, R200):
    rs = R200 / c
    rhos = Mh / (4 * np.pi * rs**3 * float(mfun(c)))
    t = r / rs
    return rhos / (t * (1 + t)**2)
def sigma_los(R, Mh, c, R200):
    f = lambda z: rho_nfw(math.hypot(R, z), Mh, c, R200)
    return 2 * quad(f, 0, np.inf, epsabs=0, epsrel=1e-11, limit=200)[0]
def m2d_disc(R, Mh, c, R200):
    return quad(lambda u: 2 * np.pi * u * sigma_los(u, Mh, c, R200), 0, R, epsabs=0, epsrel=1e-9, limit=200)[0]
def m2d_shell(R, Mh, c, R200):
    def f(r):
        w = 1.0 if r <= R else 1 - math.sqrt(1 - R * R / (r * r))
        return 4 * np.pi * r * r * rho_nfw(r, Mh, c, R200) * w
    a = quad(f, 0, R, epsabs=0, epsrel=1e-11, limit=200)[0]
    b = quad(f, R, 100 * R200, epsabs=0, epsrel=1e-11, limit=400)[0]
    # tail beyond 100 R200: integrand ~ (R^2/(2 r^2)) 4 pi r^2 rho ~ r^-3 ; add analytic bound via quad to inf
    t = quad(f, 100 * R200, np.inf, epsabs=0, epsrel=1e-9, limit=200)[0]
    return a + b + t
maxd = 0.0; maxs = 0.0; npt = 0; hasX1 = False; hasXlt = hasXgt = False
for lgM in [10, 12, 14, 16]:
    Mh = 10.0**lgM
    for nm, cr in CREL.items():
        c = cr(Mh); R2 = r200(Mh, RHOC0)
        for R in [0.3, 3.0, 30.0, 100.0, R2 / c, 0.9 * R2 / c, 2.5 * R2 / c]:
            X = c * R / R2
            hasXlt |= X < 1; hasXgt |= X > 1; hasX1 |= abs(X - 1) < 1e-12
            a = m2d(R, Mh, c, R2)
            maxd = max(maxd, abs(m2d_disc(R, Mh, c, R2) / a - 1))
            maxs = max(maxs, abs(m2d_shell(R, Mh, c, R2) / a - 1))
            assert a >= float(m3d(R, Mh, c, R2)) * (1 - 1e-12) or R / R2 > 5
            npt += 1
check("C2 analytic M2D vs numerical (disc, shell) <=1e-6, X<1,X>1,X=1 covered", maxd < 1e-6 and maxs < 1e-6 and hasXlt and hasXgt and hasX1,
      f"n={npt} disc {maxd:.2e} shell {maxs:.2e}")
check("C2 h(1)=1+ln(1/2)", abs(hfun(1.0) - (1 + math.log(0.5))) < 1e-15)
cont = max(abs(hfun(1 - 1e-6) - hfun(1 + 1e-6)), 0)
check("C2 continuity across X=1 (<1e-6)", cont < 1e-6, f"{cont:.2e}")
import mpmath as mp
mp.mp.dps = 50
def h_mp(X):
    X = mp.mpf(X)
    if X < 1:
        return mp.log(X / 2) + 2 / mp.sqrt(1 - X * X) * mp.atanh(mp.sqrt((1 - X) / (1 + X)))
    return mp.log(X / 2) + 2 / mp.sqrt(X * X - 1) * mp.atan(mp.sqrt((X - 1) / (X + 1)))
wm = max(abs(hfun(X) / float(h_mp(X)) - 1) for X in [1e-6, 1e-5, 7e-5, 1e-3, 0.01, 0.1, 0.5, 0.9, 1.1, 2, 10, 100])
check("C2 h(X) vs 50-digit literal formula <=1e-12", wm < 1e-12, f"{wm:.2e}")

# C4 estimator closed forms
rng = np.random.default_rng(1)
xd = rng.uniform(-0.3, 0.4, 80); ldd = -0.1 + 0.2 * xd
xl = rng.uniform(-0.1, 0.35, 30)
d0, e0, _ = gap_stat(-0.1 + 0.2 * xl, xl, ldd, xd, nboot=50)
check("C4i lenses on the fit line: Delta=0", abs(d0) < 1e-12, f"{d0:.1e}")
d1, _, _ = gap_stat(-0.1 + 0.2 * xl + 0.137, xl, ldd, xd, nboot=50)
check("C4ii lenses = fit +k: Delta=k", abs(d1 - 0.137) < 1e-12, f"{d1-0.137:.1e}")
p = np.polyfit(xd, ldd, 1)
check("C4iii fit recovers synthetic law", abs(p[0] - 0.2) < 1e-10 and abs(p[1] + 0.1) < 1e-10)

# ---------------- base + solves ----------------
print("\n=== BASE RUN ===")
BASE = Cfg()
t = run_cfg(BASE, full=True)
print(fmt(t))
li, dj = t["_li"], t["_dj"]
# C3
res_l = max(abs(kbar_lens(t["_lm_l"][i], i, BASE)) for i in li)
res_d = max(abs(dyn_resid(t["_lm_d"][j], j, BASE)) / (A_MJ[j] / 2) for j in dj)
check("C3 kbar(alpha_lens)=1 (<=1e-9) and M(<r_1/2)=M_JAM/2 (<=1e-9)", res_l < 1e-9 and res_d < 1e-9, f"{res_l:.1e} {res_d:.1e}")
if not MUTATE:
    off = Cfg(mult=1e-30)
    a_l = [solve_lens(i, off) for i in range(70)]
    a_d = [solve_dyn(j, off) for j in range(len(CAL))]
    e1 = max(abs(10**a_l[i] / L_MS[i] - 1 / L_FS[i]) / (1 / L_FS[i]) for i in range(70))
    e2 = max(abs(10**a_d[j] / A_MS[j] - A_MJ[j] / A_MS[j]) / (A_MJ[j] / A_MS[j]) for j in range(len(CAL)))
    check("C3 halo off: alpha_lens=1/Fs, alpha_dyn=M_JAM/M_Salp (1e-9)", e1 < 1e-9 and e2 < 1e-9, f"{e1:.1e} {e2:.1e}")
    lowers = all(10**t["_lm_l"][i] / L_MS[i] <= 1 / L_FS[i] * (1 + 1e-12) for i in li) and all(10**t["_lm_d"][j] / A_MS[j] <= A_MJ[j] / A_MS[j] * (1 + 1e-12) for j in dj)
    check("C3 halo only lowers alpha", lowers)
    # C4iv zero-point
    for dz in (0.10, -0.10):
        r = run_cfg(Cfg(dzero=dz), nboot=200)
        b = run_cfg(BASE, nboot=200)
        check(f"C4iv zero-point d={dz:+.2f} shifts Delta by -d to 1e-9", abs((r["delta"] - b["delta"]) + dz) < 1e-9, f"{(r['delta']-b['delta'])+dz:.1e}")
# C5 witness: halo mass entering solves / Moster(M_*)
f0 = halo_logmass_fn(0.0)
wit = []
for i in li:
    lm = t["_lm_l"][i]; Mh = make_halo(BASE, lm, L_z[i], None)[0]
    wit.append(Mh / 10**f0(lm))
for j in dj:
    lm = t["_lm_d"][j]; Mh = make_halo(BASE, lm, 0.0, None)[0]
    wit.append(Mh / 10**f0(lm))
wit = np.array(wit)
check("C5 witness: halo mass / Moster(M_*) = 1 (1e-12)", np.max(np.abs(wit - 1)) < 1e-12, f"ratio median {np.median(wit):.4g}")

# ---------------- headline row ----------------
print("\n=== HEADLINE (P1-P4) ===")
th = run_cfg(BASE, nboot=2000, full=True)
print(fmt(th))
ok_counts = th["n_lens"] == 70 and th["n_cal"] == 187
check("P1 70/70 lenses solved, 187/187 calibrated", ok_counts, f"{th['n_lens']}/{th['n_cal']}")
la, ld = th["_la"], th["_ld"]
al_med = 10**np.median(la); ad_at = 10**np.median(np.polyval(th["_p"], L_x))
print(f"alpha_lens median {al_med:.3f}  alpha_dyn at lenses' sigma (median of fit) {ad_at:.3f}   slope dlogalpha_dyn/dlogsigma {th['slope']:+.3f}")
lmh_l = np.array([make_halo(BASE, th["_lm_l"][i], L_z[i])[3] for i in th["_li"]])
lmh_d = np.array([make_halo(BASE, th["_lm_d"][j], 0.0)[3] for j in th["_dj"]])
darkfrac_l = np.array([1 - 10**th["_lm_l"][i] / L_MS[i] * L_FS[i] for i in th["_li"]])
darkfrac_d = np.array([1 - 0.5 * 10**th["_lm_d"][j] / (A_MJ[j] / 2) for j in th["_dj"]])
nabove = int(np.sum(np.array([th["_lm_l"][i] for i in th["_li"]]) > shmr_logMs(np.array([15.5]))[0]))
nclip = int(np.sum([A_r[j] < 1e-4 * make_halo(BASE, th["_lm_d"][j], 0.0)[2] for j in th["_dj"]]))
print(f"median log Mh lenses {np.median(lmh_l):.2f} (range {lmh_l.min():.2f}..{lmh_l.max():.2f}); calibrators {np.median(lmh_d):.2f} (range {lmh_d.min():.2f}..{lmh_d.max():.2f})")
print(f"median projected dark fraction inside R_E {np.median(darkfrac_l):.3f}; median 3D dark fraction inside r_1/2 (of M_JAM/2) {np.median(darkfrac_d):.3f}")
print(f"lenses above Moster grid top (M_*>10^11.97): {nabove}; calibrators with r_1/2<1e-4 R200: {nclip}")
lens_slope = float(np.polyfit(L_x[th['_li']], la, 1)[0])
print(f"lens slope dlog alpha_lens/dlog sigma = {lens_slope:+.3f}")
check("H1 [HEADLINE] LCDM passes CFG33 gate (counts and |z|<=2)", th["gate"] == "PASS", f"{th['gate']} z={th['z']:+.2f}")

# =============================== MUTATE / ladder ===============================
print("\n=== HALO-MASS LADDER (both sides, every halo mass x m) ===")
ladder = {}
for m in [0.01, 0.03, 0.1, 1 / 3, 1, 3, 10, 33, 100, 300]:
    r = run_cfg(Cfg(mult=m), nboot=1000)
    ladder[m] = r
    print(fmt(r))
passm = [m for m, r in ladder.items() if r["gate"] == "PASS"]
print("gate PASSES for multipliers", passm)
if not MUTATE:
    c6 = ladder[100]["gate"] != ladder[1]["gate"]
    check("C6 gate outcome at x100 differs from x1 (else NON-DISCRIMINATING)", c6, f"{ladder[1]['gate']} -> {ladder[100]['gate']}")

# =============================== variants P3 ===============================
print("\n=== VARIANTS P3 ===")
variants = {
    "V1 Dutton-Maccio c": Cfg(crel="dm"),
    "V2 Duffy relaxed": Cfg(crel="relaxed"),
    "V3 Mh x1/3": Cfg(mult=1 / 3),
    "V4 Mh x3": Cfg(mult=3),
}
var_res = {}
for k, c in variants.items():
    var_res[k] = run_cfg(c, nboot=2000)
    print(k, "::", fmt(var_res[k]))

# =============================== z-consistent extension ===============================
print("\n=== z-CONSISTENT EXTENSION (lens halos at z_lens; calibrators z=0) ===")
zres = {}
for nm, c in {"full": Cfg(zmode="full"), "rho_c(z) only": Cfg(zrho=True), "Duffy (1+z) only": Cfg(zc=True), "Moster z-evol only": Cfg(zmost=True)}.items():
    zres[nm] = run_cfg(c, nboot=2000)
    print(nm, "::", fmt(zres[nm]))

# =============================== 54-cell declared range ===============================
print("\n=== DECLARED-RANGE GRID (54 cells) and extended context ===")
B_GAPS = {"canV": (0.159, 0.021), "canI": (0.171, 0.022), "altV": (0.152, 0.022), "altI": (0.168, 0.022)}
def evaluate_W(r):
    bg, be = B_GAPS["altV"]
    Sa = abs(r["delta"]) <= 2 * r["err"]
    Sb = (bg - r["delta"]) > 2 * math.sqrt(be**2 + r["err"]**2)
    Saf = abs(r["delta"]) <= 2 * math.sqrt(r["err"]**2 + SIGMA_FLOOR**2)
    return Sa, Sb, Saf
grid = []
for m in [1 / 3, 1, 3, 0.1, 10]:
    for tie in ["solved_salp", "solved_chab", "fixed_chab"]:
        for zm in ["z0", "full"]:
            for cr in ["duffy", "relaxed", "dm"]:
                r = run_cfg(Cfg(mult=m, tie=tie, zmode=zm, crel=cr), nboot=1000)
                r["axes"] = (m, tie, zm, cr)
                r["Sa"], r["Sb"], r["Saf"] = evaluate_W(r)
                r["W"] = r["Sa"] and r["Sb"]
                grid.append(r)
core = [g for g in grid if g["axes"][0] in (1 / 3, 1, 3)]
ext = [g for g in grid if g["axes"][0] in (0.1, 10)]
print(f"{'m':>5} {'tie':12s} {'z':5s} {'c':8s}  Delta    err    zstat  zfloor gate  Sa Sb Saf W")
for g in grid:
    m, tie, zm, cr = g["axes"]
    print(f"{m:5.2f} {tie:12s} {zm:5s} {cr:8s} {g['delta']:+.4f} {g['err']:.4f} {g['zstat']:+6.2f} {g['z']:+6.2f} {g['gate']:5s} {int(g['Sa'])}  {int(g['Sb'])}  {int(g['Saf'])}  {int(g['W'])}")
def frac(lst, key): return sum(1 for g in lst if g[key]) / len(lst)
print(f"\nDECLARED RANGE ({len(core)} cells): S_a {frac(core,'Sa'):.3f}  S_b {frac(core,'Sb'):.3f}  S_a_floor {frac(core,'Saf'):.3f}  W=S_a&S_b {frac(core,'W'):.3f}")
print(f"EXTENDED context ({len(ext)} cells): S_a {frac(ext,'Sa'):.3f}  S_b {frac(ext,'Sb'):.3f}  S_a_floor {frac(ext,'Saf'):.3f}  W {frac(ext,'W'):.3f}")
print("gap range over the 54 cells: %+.3f .. %+.3f" % (min(g['delta'] for g in core), max(g['delta'] for g in core)))
print("axis marginals in the 54 cells (fraction with S_a | S_b | W):")
for ai, nm, levels in [(0, "m", [1/3, 1, 3]), (1, "tie", ["solved_salp", "solved_chab", "fixed_chab"]), (2, "z", ["z0", "full"]), (3, "c", ["duffy", "relaxed", "dm"])]:
    for lv in levels:
        sub = [g for g in core if g["axes"][ai] == lv]
        print(f"   {nm}={lv!s:12s} n={len(sub):2d}  S_a {frac(sub,'Sa'):.2f}  S_b {frac(sub,'Sb'):.2f}  W {frac(sub,'W'):.2f}   mean Delta {np.mean([g['delta'] for g in sub]):+.3f}")
Wfrac = frac(core, "W")
verdict = "ROBUST" if Wfrac >= 0.9 else ("CONDITIONAL" if Wfrac >= 0.5 else "NOT SUPPORTED")
print("VERDICT on wording 'B-specific statistically' over the declared range at d=0:", verdict, f"({Wfrac:.3f})")
# sensitivity of S_b to B's best case
Sb_can = sum(1 for g in core if (B_GAPS['canI'][0] - g['delta']) > 2 * math.sqrt(B_GAPS['canI'][1]**2 + g['err']**2)) / len(core)
print("S_b with B canonical I (+0.171):", round(Sb_can, 3), " min B-LCDM difference over 54 cells (alt V B): %+.3f" % min(B_GAPS['altV'][0] - g['delta'] for g in core))

# zero-point axis on base and variants
print("\n=== IMF ZERO-POINT AXIS d (Auger Salpeter scale relative to ATLAS3D's; Delta_L(d) = Delta_L - d exactly, C4iv) ===")
for nm, r in [("base", th), ("V3 Mh/3", var_res["V3 Mh x1/3"]), ("V4 Mh x3", var_res["V4 Mh x3"]),
              ("V1 DM c", var_res["V1 Dutton-Maccio c"]), ("z-full", zres["full"])]:
    line = []
    for d in [-0.10, -0.05, 0.0, 0.05, 0.10]:
        dl = r["delta"] - d
        Sa = abs(dl) <= 2 * r["err"]
        line.append(f"d={d:+.2f}: DeltaL={dl:+.3f} Sa={int(Sa)}")
    lo = r["delta"] - 2 * r["err"]; hi = r["delta"] + 2 * r["err"]
    print(f"{nm:9s} " + " | ".join(line) + f"   => S_a holds for d in [{lo:+.3f},{hi:+.3f}]")
bg, be = B_GAPS["altV"]
print(f"B (alt V) stat gap {bg:+.3f}-d exceeds 2 sigma ({2*be:.3f}) for d < {bg-2*be:+.3f}; S_b is d-invariant (assumes B shifts by -d too).")

# save json
if not MUTATE or True:
    def clean(r): return {k: v for k, v in r.items() if not k.startswith("_") and k not in ("axes",)}
    js = dict(mode=MODE, base=clean(th), ladder={str(k): clean(v) for k, v in ladder.items()}, variants={k: clean(v) for k, v in var_res.items()},
              zext={k: clean(v) for k, v in zres.items()},
              grid=[dict(clean(g), axes=[str(a) for a in g["axes"]], Sa=bool(g["Sa"]), Sb=bool(g["Sb"]), Saf=bool(g["Saf"]), W=bool(g["W"])) for g in grid],
              fails=FAILS)
    json.dump(js, open(os.path.join(HERE, f"CFG86_results_{MODE}.json"), "w"), indent=1)

print("\nFAILED CHECKS:", FAILS)
sys.exit(1 if FAILS else 0)
