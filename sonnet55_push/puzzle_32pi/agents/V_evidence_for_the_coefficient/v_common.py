"""v_common.py -- shared constants, SPARC loader and profile-likelihood machinery for the V lane (evidence for the coefficient).

Everything here re-implements (in my own directory, vectorised) the record's SPARC profile likelihood
(real_research/reviews/mi_a0_profile_likelihood_milgrom_footing_2026.py): Upsilon_disk free PER GALAXY on the grid
linspace(0.05, 3.0, 119), Upsilon_bulge = 1.4 Upsilon_disk, gas fixed (helium factor already in the SPARC files),
log10-space residuals, per-point variance = (2 dlnV/ln10)^2 + sig_int^2, sig_int calibrated so chi2/dof = 1 at the canonical a0.
The record's own kernel is g_obs^2 = g_bar^2 + g_bar a0 ('alpha1'); other interpolating functions (IFs) are added here.
"""
import glob, math, os
import numpy as np

REPO = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", ".."))  # repo root (this file is 4 levels down)
DATA = os.path.join(REPO, "real_research", "data")
c_l = 2.998e8                       # the record's script value (used ONLY to reproduce its numbers)
c_si = 2.99792458e8                 # exact
G_SI = 6.674e-11
kpc = 3.0857e19                     # record's value
Mpc_m = 3.0856775814913673e22
UGRID = np.linspace(0.05, 3.0, 119)

Z_F = math.sqrt(32 * math.pi / 3)   # framework Z, kappa = 1/2
Z_M = 2 * math.pi
OM_L, H0_PLANCK, H0_SHOES = 0.685, 67.4, 73.0

def H_si(H0_kms_mpc):
    return H0_kms_mpc * 1e3 / Mpc_m

# record's canonical a0 (rho_Lambda footing, kappa = 1/2) computed with the RECORD's constants (H0 = 2.184e-18 /s)
H0_REC = 2.184e-18
rho_L = OM_L * 3 * H0_REC**2 / (8 * math.pi * G_SI)
A0_FW_REC = (c_l / 2) * math.sqrt(G_SI * rho_L)     # 9.3614e-11

# ---------------------------------------------------------------- interpolating functions: g_obs = F(g_bar; a0)
def IF_alpha1(gb, a0):   # the record's kernel  g_obs^2 = g_bar^2 + g_bar a0   (nu = sqrt(1 + 1/y))
    return np.sqrt(gb * gb + gb * a0)
def IF_rar(gb, a0):      # McGaugh-Lelli-Schombert 2016 eq 4
    return gb / (1.0 - np.exp(-np.sqrt(gb / a0)))
def IF_simple(gb, a0):   # Famaey-Binney 2005
    return gb / 2 + np.sqrt(gb * gb / 4 + gb * a0)
def IF_standard(gb, a0): # Milgrom 1983, mu(x) = x/sqrt(1+x^2)
    return np.sqrt(gb * gb / 2 + gb * np.sqrt(gb * gb / 4 + a0 * a0))
IFS = {"alpha1 (record kernel)": IF_alpha1, "RAR (MLS16)": IF_rar, "simple": IF_simple, "standard": IF_standard}

def deep_limit_ok(F, a0=1e-10):
    """every IF must go to sqrt(g a0) for g << a0 and to g for g >> a0 (same a0 normalisation)"""
    lo = F(np.array([1e-16]), a0)[0] / math.sqrt(1e-16 * a0)
    hi = F(np.array([1e-6]), a0)[0] / 1e-6
    return abs(lo - 1) < 1e-3 and abs(hi - 1) < 1e-3

# ---------------------------------------------------------------- SPARC loader
def load_table():
    """SPARC Table 1 (whitespace delimited rows in the .mrt): name -> dict(D, eD, fD, inc, einc, Q)"""
    tab = {}
    for ln in open(os.path.join(DATA, "SPARC_Lelli2016c.mrt")):
        p = ln.split()
        if len(p) >= 18 and p[1].lstrip("-").isdigit() and p[4].isdigit():
            try:
                tab[p[0]] = dict(T=int(p[1]), D=float(p[2]), eD=float(p[3]), fD=int(p[4]), inc=float(p[5]),
                                 einc=float(p[6]), Q=int(p[17]))
            except ValueError:
                pass
    return tab

def load_sparc():
    tab = load_table()
    gals = []
    for f in sorted(glob.glob(os.path.join(DATA, "sparc_data", "*_rotmod.dat"))):
        try:
            d = np.genfromtxt(f, comments="#")
        except Exception:
            continue
        if d.ndim != 2 or d.shape[1] < 6:
            continue
        R, Vobs, eV, Vgas, Vdisk, Vbul = (d[:, i] for i in range(6))
        m = np.isfinite(R) & np.isfinite(Vobs) & (R > 0) & (Vobs > 0)
        if m.sum() < 3:
            continue
        name = os.path.basename(f).replace("_rotmod.dat", "")
        t = tab.get(name, {})
        gals.append(dict(name=name, Rm=R[m] * kpc, Vobs=Vobs[m], eV=np.clip(eV[m], 1.0, None), Vgas=Vgas[m],
                         Vdisk=Vdisk[m], Vbul=Vbul[m], **{k: t.get(k) for k in ("D", "eD", "fD", "inc", "einc", "Q", "T")}))
    return gals

# ---------------------------------------------------------------- perturbations (exact transformations of the rotmod content)
def transform(g, dist_scale=1.0, gas_scale=1.0, dinc_deg=0.0):
    """Return a modified copy of a galaxy.
    dist_scale s: D -> s D.  R -> sR; Vobs unchanged; Vbar^2 -> s Vbar^2 (mass ~ D^2, radius ~ D).  Net: g_bar unchanged,
                  g_obs -> g_obs / s.  (M_gas ~ D^2 and L ~ D^2: both baryon components scale together.)
    gas_scale e: gas MASS -> e * gas mass, i.e. Vgas^2 -> e Vgas^2 (sign kept).
    dinc: inclination i -> i + dinc.  Vobs -> Vobs sin i / sin i',  errV likewise;  surface densities (face-on) scale as cos i'/cos i
          so Vbar^2 -> (cos i'/cos i) Vbar^2  (stellar and gas)."""
    h = dict(g)
    s = dist_scale
    R = g["Rm"] * s
    Vobs, eV = g["Vobs"].copy(), g["eV"].copy()
    Vg, Vd, Vb = g["Vgas"].copy(), g["Vdisk"].copy(), g["Vbul"].copy()
    # distance: baryon velocities scale as sqrt(s)
    rs = math.sqrt(s)
    Vg, Vd, Vb = Vg * rs, Vd * rs, Vb * rs
    if gas_scale != 1.0:
        Vg = Vg * math.sqrt(gas_scale)
    if dinc_deg != 0.0 and g.get("inc"):
        # cap at 85 deg: the face-on deprojection (cos i) is singular for edge-on discs (an earlier version clipped cos(90 deg) to 1e-3
        # and boosted V_bar by 4x for the i = 90 galaxies -- the sanity check 'both signs of the shift lower a0' caught it)
        i0d = min(g["inc"], 85.0)
        i0 = math.radians(i0d); i1 = math.radians(min(max(i0d + dinc_deg, 5.0), 85.0))
        f_v = math.sin(i0) / math.sin(i1)
        f_b = math.sqrt(math.cos(i1) / math.cos(i0))
        Vobs, eV = Vobs * f_v, eV * f_v
        Vg, Vd, Vb = Vg * f_b, Vd * f_b, Vb * f_b
    h.update(Rm=R, Vobs=Vobs, eV=np.clip(eV, 1.0, None), Vgas=Vg, Vdisk=Vd, Vbul=Vb)
    return h

# ---------------------------------------------------------------- profile likelihood
def _prep(g, ug=None):
    """precompute per-galaxy arrays for all Upsilon at once: gbar[U, m], log gobs[m], sig_obs[m]"""
    ug = UGRID if ug is None else ug
    gobs = (g["Vobs"] * 1e3) ** 2 / g["Rm"]
    Vbar2 = (np.sign(g["Vgas"]) * g["Vgas"] ** 2)[None, :] + ug[:, None] * g["Vdisk"][None, :] ** 2 \
        + 1.4 * ug[:, None] * g["Vbul"][None, :] ** 2
    gbar = Vbar2 * 1e6 / g["Rm"][None, :]
    sig = (g["eV"] / g["Vobs"]) * 2.0 / math.log(10)
    return gobs, gbar, sig

class Profile:
    """Profile likelihood on a list of galaxies for a given IF; Upsilon_disk free per galaxy."""
    def __init__(self, gals, IF, ulo=None, uhi=None, ufixed=None):
        """Upsilon_disk free on UGRID (default: the record's 0.05-3.0); ulo/uhi restrict it; ufixed = one fixed value (bulge 1.4x)"""
        self.IF = IF
        if ufixed is not None:
            ug = np.array([ufixed])
        elif ulo is not None:
            ug = UGRID[(UGRID >= ulo - 1e-9) & (UGRID <= uhi + 1e-9)]
        else:
            ug = None
        self.ug = ug
        self.pre = [_prep(g, ug) for g in gals]
        self.npts = sum(len(p[0]) for p in self.pre)
        self.ngal = len(gals)
    def chi2(self, a0, sig_int):
        tot = 0.0
        n = 0
        for gobs, gbar, sig in self.pre:
            ok = (gbar > 0) & np.isfinite(gbar)          # [U, m]
            with np.errstate(all="ignore"):
                pred = self.IF(np.where(ok, gbar, 1.0), a0)
                r = np.log10(gobs)[None, :] - np.log10(pred)
                v = np.where(ok, r * r / (sig[None, :] ** 2 + sig_int ** 2), 0.0)
            # the record's version drops points with gbar<=0 for that Upsilon; identical when Vgas,Vdisk,Vbul >= 0 (true for SPARC except tiny gas dips)
            s = v.sum(axis=1)
            k = int(np.argmin(np.where(ok.sum(axis=1) > 0, s, np.inf)))
            tot += s[k]
            n += int(ok[k].sum())
        return tot, n
    def calibrate_sig_int(self, a0_ref):
        lo, hi = 0.001, 0.60
        for _ in range(45):
            mid = 0.5 * (lo + hi)
            ch, n = self.chi2(a0_ref, mid)
            dof = n - self.ngal - 1
            if ch / dof > 1.0:
                lo = mid
            else:
                hi = mid
        return 0.5 * (lo + hi)
    def scan(self, a0s, sig_int):
        return np.array([self.chi2(a, sig_int)[0] for a in a0s])

def parabola_min(a0s, chis, k=6):
    """refine the profile minimum by a local quadratic fit in ln a0 around the grid minimum; return (a0_hat, sigma_ind_frac)"""
    la = np.log(a0s)
    i = int(np.argmin(chis))
    lo, hi = max(0, i - k), min(len(a0s), i + k + 1)
    p = np.polyfit(la[lo:hi] - la[i], chis[lo:hi], 2)
    xmin = -p[1] / (2 * p[0])
    sig_ln = 1.0 / math.sqrt(p[0])            # Dchi2 = 1  ->  (x - xmin)^2 p0 = 1
    return math.exp(la[i] + xmin), sig_ln
