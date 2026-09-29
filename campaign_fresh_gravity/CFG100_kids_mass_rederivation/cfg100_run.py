"""
CFG100 -- independent re-derivation of CFG110's within-colour-class stellar-mass test on the KiDS-1000 lensing signal, plus a power attack.
FROZEN BEFORE ANY RUN of this lane's scoring script (written 2026-09-29).

QUESTION
  (1) From CFG110_FROZEN_CRITERIA.md / CFG110_README.md (the only CFG110 material read) and my own code, do I reproduce: B's law mass-independence
      chi2 = 22.2/14 (p 0.075); the colour-blind Moster rejection 105/14; the power row R0 = 8.8 between B and colour-split LCDM?
  (2) ATTACK on the wording "B gets mass-independence right": is a p = 0.075 pass at 14 dof only a non-detection?  How much mass dependence could
      B's pass still hide (power / upper limits), where in the bins does the discriminating power sit, and how robust is the verdict to error
      inflation, the bin set and the mass-split edges?

MATERIAL READ (declared): CFG110_FROZEN_CRITERIA.md and CFG110_README.md (numbers in the README were therefore known before the run); the READMEs and
  docstrings of CFG61, CFG67, CFG77; CFG77's cfg77_lib.py (source of the kernel, projector, turnaround solver, NFW/Mandelbaum pieces; own copies, no
  import); the ESD normalisation lines of the June estimator agentK_jackknife_stack.py (KG = Msun/(3.0857e16)^2 and the leave-one-patch-out formula,
  jackknife factor (N-1)/N) -- read via grep because the per-lens sums do not carry the unit conversion.  NOT read, run or imported: any CFG110 script,
  .out or _results.json, CFG61/CFG67 code.
  ONE INDEPENDENCE LIMIT, DECLARED: the per-lens KiDS sums (WG, WW, NN per lens per g_bar bin) are taken from the on-disk data product
  real_research/data/lensing_rar/cfg110_perlens.npz (written by CFG110's staging pass; I did NOT re-stage from the 17 GB shear catalogue).  It is
  verified only at the level of per-(patch, class, bin) sums against the June file (control K1).  A mis-assignment of pair sums between lenses of the
  same patch and class would be invisible to K1; that is an untested shared-input dependency.

DATA.  ESD(class, subset, bin) = sum_patches WG / sum_patches WW / KG  [Msun/pc^2], Msun = 1.98847e30 kg.  Lenses: lr_lenses.npz (181,477), patch labels
  from lr_esd_jackknife.npz, class = typ (0 late, 1 early).  No m-bias correction (as June; it is a common constant).
BINS.  15 g_bar bins logspace(1e-15, 5e-12, 16) m/s^2.  K1 = the 1-halo bins where the M_gal-unweighted lens median R = sqrt(G M_gal/g_centre) of BOTH classes is
  < 0.3 Mpc; expected {8..14} (0-based), 7 bins (control K2).  Data vector D = [D_late(7), D_early(7)], 14 entries.
MASS BINS / CLASSES.  Within each class, split at the class median of log10 M_gal (number median, whole lr sample of that class); a lens at the median goes to
  the upper half.  D_c = ESD(c, high) - ESD(c, low).  Expected medians 10.448 (late), 10.810 (early).
COVARIANCE.  Leave-one-patch-out over the 50 June patches for each of the four ESDs (late-hi, late-lo, early-hi, early-lo); D_(-p) formed per patch; C = (N-1)/N
  sum_p (D_(-p) - mean)(D_(-p) - mean)^T.  Hartlap h = (50 - 14 - 2)/49 = 34/49; chi2 = h (D - D_m)^T C^-1 (D - D_m), dof 14.  For other bin sets p = 2 n_bins.
MODELS (nothing fitted; lens by lens through grouped cells, cell = class x 0.01 dex in log M_gal x 0.03 in z, evaluated at the cell means; lens weight M_gal;
  within a bin uniform in ln g with weight 1/g; pairs at R = sqrt(G M_gal / g), 6-point Gauss-Legendre in ln g per bin):
  B : point baryon M_gal + dark mass M_gal (nu_mono(G M_gal/(r^2 a0)) - 1) to r_e = 0.4 r_ta, frozen beyond; r_ta where the untruncated enclosed mean density =
      (1+delta_ta(a)) rho_m(a) at the lens z (own spherical-collapse solution); nu_mono re-implemented from its 8-line definition; a0 canonical 9.3603e-11 and alt
      1.1312e-10 m/s^2; flat LCDM Om 0.3153, h 0.6736.
  L (colour-split LCDM): point M_gal + NFW(M200c) truncated at 5 R200c, M200c from Mandelbaum+2016 (real_research/data/mandelbaum2016_lbg_halo_mass.tsv), red for early,
      blue for late, converted M200m -> M200c (h 0.673, Om 0.315), Dutton-Maccio c; clamped at the table ends; M_* = 10^logM.
  Mo (colour-blind Moster+13): M_* -> halo mass by inversion of the z = 0 Moster+13 relation (log M1 = 11.590, N = 0.0351, beta = 1.376, gamma = 0.608), the halo mass
      TAKEN AS M200c (declared assumption: I did not read CFG35's halo_mass; the 105/14 may depend on it).  Variant Mo_m (reported): the same halo mass taken as
      M200m and converted to M200c as for Mandelbaum.
PASS LINES.
 CONTROLS (a failure invalidates the corresponding downstream number):
  K1  per-(patch, class, bin) sums of the per-lens arrays reproduce the June sums (wgE, W, NN) to relative 1e-9.
  K2  the mass halves partition each class exactly; median log M_gal = 10.448 (late), 10.810 (early) to 5e-4; K1 bins = {8..14}.
  K3  projector: point mass DeltaSigma = M/(pi R^2) to 1e-12; SIS (M = k r) DeltaSigma = k/(4R) to 1e-3; NFW vs Wright & Brainerd closed form to 1e-3 (own
      formula); NFW enclosed mass at R200c equals M200c to 1e-6.
  K4  the law at fixed g <= 1e-12 (g = 1e-13, 1e-12): DeltaSigma at M_gal = 1e10 vs 1e11 agrees to 3% (edge excluded).
  K5  grouped-cell stacking vs exact per-lens on 300 random lenses per class: relative stack error < 1% (B, L, Mo) and |Delta D| < 0.05 sigma_D.
  K6  covariance algebra: the directly jackknifed D covariance equals T C60 T^T (the transformed 60x60 four-ESD jackknife covariance) to 1e-9 relative; chi2 by
      solve = Cholesky whitening = explicit inverse to 1e-8; C symmetric positive definite.
  K7  calibration null: 200 random within-class halvings (seed 100), D_null per class on K1, own jackknife covariance each, Hartlap: mean chi2 in [9.8, 18.2].
  K8  SWAPPED-CLASS control: the late and early data blocks (D and the covariance blocks) swapped, models kept with their classes: B chi2 moves by < 0.5 (B predicts
      D ~ 0) while at least one of L, Mo moves by > 2.
  K9  MUTATE=1 (early-class lens M_* and M_gal multiplied by 2; data untouched; the median partition is invariant): B chi2 (both footings) changes by < 0.1 against the
      main run and the Mo chi2 changes by > 3 (L reported).  Failed => the control failed; report as such.
  K10 power machinery: Monte Carlo (2e5 draws of N(mu, C/h)) reproduces the analytic non-central chi2 mean 14 + lambda and the power at alpha = 0.05 to 1%.
 REPRODUCTION against CFG110's stated numbers (tolerance = the displayed digits; APPROXIMATE if within 10% [chi2] and non-reproduction otherwise; causes to be
  investigated post hoc and labelled as such):
  P1 B chi2 = 22.2 (canonical; alt the same), p = 0.075;   P2 Mo chi2 = 105 (p ~ 4e-16);   P3 R0 = (D_L - D_B)^T h C^-1 (D_L - D_B) = 8.8;
  reported comparisons: L chi2 25.2 (p 0.033); Mo-B power 87; per-class chi2 (7 bins, p = 7 Hartlap): B 13.4 / 6.5, L 21.8 / 5.1, Mo 25.2 / 55.0 (late / early).
 READING lines (as CFG110's, not judged as pass/fail here): H1 = B p > 0.01 on both footings; H2 = L p > 0.01.
REPORTED ROWS (frozen now):
  R0  power row: lambda_LB = (D_L - D_B)^T h C^-1 (D_L - D_B); also lambda_MoB and the per-class / per-bin decomposition.
  R6  pair-weighted model stacks (weights = the data's own WW_ik instead of M_gal): chi2 for B, L, Mo.
  R7  amplitude fits D = A D_shape (shape = L or Mo, B's D subtracted): A_hat = (s^T P r)/(s^T P s), sigma_A = (s^T P s)^-1/2 with P = h C^-1, r = D - D_B; the 1-dof z for A = 0 and the
      one-sided 95% upper limit A_hat + 1.645 sigma_A; the L and Mo shapes recomputed with M_* shifted +-0.1 dex for all lenses (stellar-mass calibration).
POWER ANALYSIS (the attack).  Test statistic = B's mass-independence chi2 (h C^-1, 14 dof).  Alternatives (true D): (a) D_L, (b) D_B + 0.5 (D_L - D_B), (c) D_Mo.
  mu = D_alt - D_B; lambda = mu^T h C^-1 mu; expected chi2_B = 14 + lambda; power = P(nc-chi2(14, lambda) > chi2_crit(14, 0.05) = 23.685); also the same for the
  1-dof optimal amplitude test of A = 0 and the Neyman-Pearson B-vs-alt discrimination error rate Phi(-sqrt(lambda)/2).  Bin decomposition: c_i = mu_i (P mu)_i, per
  class, leave-one-bin-out lambda, single-bin z^2.  Detectable amplitude at 80% power (omnibus 14 dof and 1 dof) for the L and Mo shapes.
  Wording tests (declared): W1 "consistent with B" = p_B > 0.01.  W2 "data exclude LCDM-size (colour-split) mass dependence" = A_hat_L + 1.645 sigma < 1.  W3 the same for half-size (< 0.5).
  W4 = W2 for the Mo shape.  The phrase "B gets the mass-independence right" is allowed only if W3 holds; otherwise the only supported statement is W1 (a non-rejection).
SENSITIVITIES (reported, not pass/fail): error inflation x1.2, x1.5, x2 (chi2/f^2, power lambda/f^2) for B, L, Mo; bin sets (K1; K1 minus each bin; the 4 highest-g bins; the 3
  lowest-g K1 bins); mass-split edges (median [main]; q40|q60; q33|q67; q25|q75; single split at the class median shifted by -0.1 and +0.1 dex), each with its own
  jackknife covariance, models restricted to the same lenses, chi2 for B, L, Mo, lambda_LB, lambda_MoB.
Programme rules: no claim that the data favour the framework; kappa = 1/2 and Omega_c h^2 are fitted; a non-reproduction is a valid outcome; controls that fail are failures.
"""
import os, sys, json, math, time, hashlib
import numpy as np
from scipy import stats
from scipy.optimize import brentq
import cfg100_lib as L

HERE = os.path.dirname(os.path.abspath(__file__))
MUTATE = os.environ.get("MUTATE") == "1"
OUT = os.path.join(HERE, "cfg100_results_MUTATE.json" if MUTATE else "cfg100_results.json")
T0 = time.time()
def log(*a):
    print(*a, flush=True)
FROZEN_SHA = hashlib.sha256(open(os.path.join(HERE, "cfg100_FROZEN.txt"), "rb").read()).hexdigest()
log("CFG100  MUTATE=%d  frozen-text sha256 %s" % (MUTATE, FROZEN_SHA[:16]))
np.set_printoptions(linewidth=200, precision=3, suppress=True)
NPATCH = 50
KG = 1.98847e30 / (3.0857e16) ** 2
checks = {}
def check(name, ok, msg):
    checks[name] = bool(ok)
    log("  [%s] %s: %s" % ("PASS" if ok else "FAIL", name, msg))

# ---------------------------------------------------------------- inputs
lens = np.load(os.path.join(L.DATA, "lr_lenses.npz"))
z = lens["z"].copy(); logM = lens["logM"].copy(); Mgal = lens["Mgal"].copy(); typ = lens["typ"].copy()
jk = np.load(os.path.join(L.DATA, "lr_esd_jackknife.npz")); patch = jk["patch"]
pl = np.load(os.path.join(L.DATA, "cfg110_perlens.npz")); WG, WW, NN = pl["WG"], pl["WW"], pl["NN"]
assert np.allclose(pl["gbar_edges"], L.GEDGE) and np.allclose(jk["gbar_edges"], L.GEDGE)
nL = len(z)
lmg_raw = np.log10(Mgal)          # partition variable, from the un-mutated masses
if MUTATE:
    e = typ == 1
    logM[e] += math.log10(2.0); Mgal[e] *= 2.0
lmg = np.log10(Mgal)

# ---------------------------------------------------------------- K1 (data sums), K2 (partition, median, K1 bins)
log("== controls on inputs")
mx = 0.0
for name, a, b in (("WG", WG, jk["wgE"]), ("WW", WW, jk["W"]), ("NN", NN, jk["NN"])):
    for c in (0, 1):
        for p in range(NPATCH):
            m = (patch == p) & (typ == c)
            s = a[m].sum(0); r = b[p, c]
            mx = max(mx, float(np.max(np.abs(s - r) / np.maximum(np.abs(r), 1e-300))))
check("K1 per-patch sums vs June", mx <= 1e-9, "max relative deviation %.2e (<= 1e-9)" % mx)

med = {c: float(np.median(lmg_raw[typ == c])) for c in (0, 1)}
part_ok = True
for c in (0, 1):
    hi = (typ == c) & (lmg_raw >= med[c]); lo = (typ == c) & (lmg_raw < med[c])
    part_ok &= (hi.sum() + lo.sum() == (typ == c).sum()) and not np.any(hi & lo)
gcen = np.sqrt(L.GEDGE[:-1] * L.GEDGE[1:]) / L.SI_ACC
def wmedian_R(c):    # lens median (unweighted) of R = sqrt(G Mgal / g_centre) per bin
    return np.array([np.median(np.sqrt(L.G_MPC * 10 ** lmg_raw[typ == c] / g)) for g in gcen])
Rmed = np.array([wmedian_R(0), wmedian_R(1)])
K1 = [k for k in range(15) if Rmed[0, k] < 0.3 and Rmed[1, k] < 0.3]
check("K2 partition/medians/K1", part_ok and abs(med[0] - 10.448) < 5e-4 and abs(med[1] - 10.810) < 5e-4 and K1 == list(range(8, 15)),
      "medians %.4f late %.4f early; K1 = %s; median R late %s" % (med[0], med[1], K1, np.round(Rmed[0][K1], 3)))
K1 = np.array(K1)
log("  class counts: late %d early %d" % ((typ == 0).sum(), (typ == 1).sum()))

# ---------------------------------------------------------------- groups + model tables
def build_groups():
    key = typ.astype(np.int64) * 10 ** 9 + np.floor(lmg / 0.01).astype(np.int64) * 1000 + np.floor(z / 0.03).astype(np.int64)
    u, gi, cnt = np.unique(key, return_inverse=True, return_counts=True)
    mean = lambda x: np.bincount(gi, weights=x) / cnt
    return gi, dict(n=cnt, Mgal=10 ** mean(lmg), logM=mean(logM), z=mean(z), typ=np.bincount(gi, weights=typ) / cnt)
gi, GR = build_groups()
NG = len(GR["n"])
log("  groups: %d" % NG)

def build_table(kind):
    t = time.time()
    tab = np.zeros((NG, 15))
    for g in range(NG):
        tab[g] = L.v_one(kind, GR["Mgal"][g], GR["logM"][g], GR["z"][g], int(round(GR["typ"][g])))
    log("  table %-12s %5.1fs" % (kind, time.time() - t))
    return tab

def mstack(tab, mask):
    w = np.bincount(gi[mask], weights=Mgal[mask], minlength=NG)
    return (w @ tab) / w.sum()
def mstack_pw(tab, mask):
    out = np.zeros(15)
    for k in range(15):
        w = np.bincount(gi[mask], weights=WW[mask, k], minlength=NG)
        out[k] = (w @ tab[:, k]) / w.sum()
    return out

# ---------------------------------------------------------------- data sums, jackknife
def psums(mask):
    wg = np.zeros((NPATCH, 15)); w = np.zeros((NPATCH, 15))
    for k in range(15):
        wg[:, k] = np.bincount(patch[mask], weights=WG[mask, k], minlength=NPATCH)
        w[:, k] = np.bincount(patch[mask], weights=WW[mask, k], minlength=NPATCH)
    return wg, w
def esd_full_loo(mask):
    wg, w = psums(mask)
    tg, tw = wg.sum(0), w.sum(0)
    return tg / tw / KG, (tg[None] - wg) / (tw[None] - w) / KG

def masks_for(scheme):
    """returns list of 4 masks [late-lo, late-hi, early-lo, early-hi]"""
    out = []
    for c in (0, 1):
        m = typ == c; x = lmg_raw
        if scheme == "q50":            lo_t = hi_t = med[c]
        elif scheme.startswith("q"):   # e.g. q40|q60
            a, b = scheme[1:].split("|q"); lo_t = float(np.quantile(x[m], int(a) / 100)); hi_t = float(np.quantile(x[m], int(b) / 100))
        elif scheme.startswith("s"):   # shifted median
            lo_t = hi_t = med[c] + float(scheme[1:])
        out += [m & (x < lo_t), m & (x >= hi_t)]
    return out

def data4(masks):
    f = np.zeros((4, 15)); l = np.zeros((4, NPATCH, 15))
    for i, m in enumerate(masks):
        f[i], l[i] = esd_full_loo(m)
    return f, l

def assemble(full4, loo4, K, order=(0, 1)):
    K = np.asarray(K)
    Dfull = np.concatenate([full4[2 * c + 1][K] - full4[2 * c][K] for c in order])
    Dloo = np.concatenate([loo4[2 * c + 1][:, K] - loo4[2 * c][:, K] for c in order], axis=1)
    dev = Dloo - Dloo.mean(0)
    C = (NPATCH - 1) / NPATCH * dev.T @ dev
    return Dfull, C
def hart(p): return (NPATCH - p - 2) / (NPATCH - 1)
def chi2(r, C, h):
    return float(h * r @ np.linalg.solve(C, r))
def model_D(m4, K):
    K = np.asarray(K)
    return np.concatenate([m4[2 * c + 1][K] - m4[2 * c][K] for c in (0, 1)])
def pv(x, dof): return float(stats.chi2.sf(x, dof))

# ---------------------------------------------------------------- build tables
kinds = ["B_canonical", "B_alt", "L", "Mo"]
if not MUTATE: kinds += ["Mo_m", "L+", "L-", "Mo+", "Mo-"]
tabs = {k: build_table(k) for k in kinds}

masks_main = masks_for("q50")
m4 = {k: np.array([mstack(tabs[k], m) for m in masks_main]) for k in kinds}
full4, loo4 = data4(masks_main)
Dd, C = assemble(full4, loo4, K1)
p14 = 2 * len(K1); h14 = hart(p14)
log("== main statistic: 14 bins, h = %.6f" % h14)
log("  D late :", Dd[:7]); log("  D early:", Dd[7:])
log("  sigma  :", np.sqrt(np.diag(C))[:7], np.sqrt(np.diag(C))[7:])
DM = {k: model_D(m4[k], K1) for k in kinds}
for k in kinds:
    log("  D_%-12s late %s | early %s" % (k, DM[k][:7], DM[k][7:]))
X = {k: chi2(Dd - DM[k], C, h14) for k in kinds}
R = {}
R["chi2"] = X
R["p"] = {k: pv(X[k], 14) for k in kinds}
log("  --- R0 (power row, printed before data comparison as frozen) ---")
def lam(mu, C_, h_): return float(h_ * mu @ np.linalg.solve(C_, mu))
lam_LB = lam(DM["L"] - DM["B_canonical"], C, h14); lam_MB = lam(DM["Mo"] - DM["B_canonical"], C, h14)
log("  lambda(L-B) = %.3f   lambda(Mo-B) = %.3f   lambda(L-Mo)=%.3f" % (lam_LB, lam_MB, lam(DM["L"] - DM["Mo"], C, h14)))
for k in kinds:
    log("  chi2 %-12s = %8.3f / 14   p = %.3g" % (k, X[k], R["p"][k]))

# ---------------------------------------------------------------- K3 projector, K4 deep-regime, K6 cov algebra
if not MUTATE:
    log("== controls on machinery")
    Rg = np.array([0.02, 0.05, 0.3, 1.0])
    r = np.geomspace(1e-5, 50.0, 4000); M = 1e11
    d_pm = L.dsigma(Rg, r, np.full_like(r, M)) - M / (math.pi * Rg ** 2) * 0
    e_pm = float(np.max(np.abs(d_pm / (M / (math.pi * Rg ** 2)) - 1)))
    k_ = 3e9; r2 = np.geomspace(1e-6, 500.0, 6000)
    d_sis = L.dsigma(Rg[:3], r2, k_ * r2); e_sis = float(np.max(np.abs(d_sis / (k_ / (4 * Rg[:3])) - 1)))
    M200 = 1e12; c_ = L.conc(M200); R200 = (3 * M200 / (4 * math.pi * 200 * L.RHOC_H674)) ** (1 / 3); rs = R200 / c_
    rhos = M200 / (4 * math.pi * rs ** 3 * float(L._nfw_m(c_)))
    r3 = np.geomspace(1e-5, 400 * R200, 8000); Mn = M200 * L._nfw_m(r3 / rs) / float(L._nfw_m(c_))
    Rt = np.array([0.02, 0.1, 0.3, 0.6]) * R200
    e_nfw = float(np.max(np.abs(L.dsigma(Rt, r3, Mn) / L.nfw_ds_wb(Rt, rs, rhos) - 1)))
    e_mr = abs(M200 * float(L._nfw_m(R200 / rs)) / float(L._nfw_m(c_)) / M200 - 1)
    check("K3 projector", e_pm < 1e-12 and e_sis < 1e-3 and e_nfw < 1e-3 and e_mr < 1e-6,
          "point %.1e, SIS %.1e, NFW-WB %.1e, M(<R200c) %.1e" % (e_pm, e_sis, e_nfw, e_mr))
    # K4 deep-regime mass independence (law, canonical), fixed g, z = 0.3
    e4 = 0.0; a0 = L.A0["canonical"]
    for gsi in (1e-13, 1e-12):
        g = gsi / L.SI_ACC; vals = []
        for Mg in (1e10, 1e11):
            Rr = math.sqrt(L.G_MPC * Mg / g); re = 0.4 * L.r_ta_law(Mg, a0, 0.3)
            rr = np.geomspace(1e-4, re, 1500); Md = Mg * (L.nu_mono(L.G_MPC * Mg / rr ** 2 / a0) - 1.0)
            vals.append(float(L.dsigma(np.array([Rr]), rr, Md)[0]) + Mg / (math.pi * Rr ** 2) - Mg / (math.pi * Rr ** 2))
            vals[-1] = float(L.dsigma(np.array([Rr]), rr, Md)[0])   # dark part (the baryon point mass is mass-dependent by construction)
        e4 = max(e4, abs(vals[1] / vals[0] - 1))
    check("K4 law deep-regime mass independence (dark part, g<=1e-12)", e4 < 0.03, "max |ratio-1| = %.2e (R inside edge)" % e4)
    # K6 covariance algebra
    C60_dev = loo4.transpose(1, 0, 2).reshape(NPATCH, 60); C60_dev = C60_dev - C60_dev.mean(0)
    C60 = (NPATCH - 1) / NPATCH * C60_dev.T @ C60_dev
    T = np.zeros((14, 60))
    for ci in (0, 1):
        for jj, k in enumerate(K1):
            T[ci * 7 + jj, (2 * ci + 1) * 15 + k] = 1.0; T[ci * 7 + jj, (2 * ci) * 15 + k] = -1.0
    e_t = float(np.max(np.abs(T @ C60 @ T.T - C)) / np.max(np.abs(C)))
    rr_ = Dd - DM["B_canonical"]
    c_solve = chi2(rr_, C, h14); Lc = np.linalg.cholesky(C); c_chol = float(h14 * np.sum(np.linalg.solve(Lc, rr_) ** 2)); c_inv = float(h14 * rr_ @ np.linalg.inv(C) @ rr_)
    ev = np.linalg.eigvalsh(C)
    check("K6 covariance algebra", e_t < 1e-9 and abs(c_solve / c_chol - 1) < 1e-8 and abs(c_solve / c_inv - 1) < 1e-8 and ev.min() > 0 and np.allclose(C, C.T),
          "T C60 T^T vs C: %.1e; solve/chol/inv %.6f %.6f %.6f; eig min %.3g max %.3g" % (e_t, c_solve, c_chol, c_inv, ev.min(), ev.max()))
    # K5 grouped vs exact per-lens
    rng = np.random.default_rng(100)
    e5s = 0.0; e5d = 0.0
    sig = np.sqrt(np.diag(C))
    for kind in ("B_canonical", "L", "Mo"):
        for c in (0, 1):
            idx = rng.choice(np.where(typ == c)[0], 300, replace=False)
            ve = np.array([L.v_one(kind, Mgal[i], logM[i], z[i], c) for i in idx]); w = Mgal[idx]
            hi = lmg_raw[idx] >= med[c]
            ex = lambda sel: (w[sel] @ ve[sel]) / w[sel].sum()
            ap = lambda sel: (w[sel] @ tabs[kind][gi[idx][sel]]) / w[sel].sum()
            for sel in (np.ones(300, bool), hi, ~hi):
                e5s = max(e5s, float(np.max(np.abs(ap(sel)[K1] / ex(sel)[K1] - 1))))
            dD = (ap(hi) - ap(~hi))[K1] - (ex(hi) - ex(~hi))[K1]
            e5d = max(e5d, float(np.max(np.abs(dD) / sig[c * 7:(c + 1) * 7])))
    check("K5 grouped vs exact per-lens", e5s < 0.01 and e5d < 0.05, "max stack rel err %.2e; max |dD|/sigma_D %.2e" % (e5s, e5d))

    # K7 null
    rng = np.random.default_rng(100); chis = []
    idx_c = [np.where(typ == c)[0] for c in (0, 1)]
    for it in range(200):
        masks = []
        for c in (0, 1):
            perm = rng.permutation(idx_c[c]); a = np.zeros(nL, bool); b = np.zeros(nL, bool)
            a[perm[: len(perm) // 2]] = True; b[perm[len(perm) // 2:]] = True
            masks += [b, a]
        f_, l_ = data4(masks); Dn, Cn = assemble(f_, l_, K1)
        chis.append(chi2(Dn, Cn, h14))
    chis = np.array(chis)
    check("K7 calibration null (200 random halvings)", 9.8 <= chis.mean() <= 18.2, "mean chi2 %.2f (14), frac p<0.05 = %.3f, sd %.2f (expect ~5.3)" % (chis.mean(), np.mean(stats.chi2.sf(chis, 14) < 0.05), chis.std()))
    R["null_mean"] = float(chis.mean())

    # K8 swap
    perm = np.r_[7:14, 0:7]
    Dsw, Csw = Dd[perm], C[np.ix_(perm, perm)]
    sw = {k: chi2(Dsw - DM[k], Csw, h14) for k in ("B_canonical", "L", "Mo")}
    dB = abs(sw["B_canonical"] - X["B_canonical"]); dL = abs(sw["L"] - X["L"]); dM = abs(sw["Mo"] - X["Mo"])
    check("K8 swapped-class control", dB < 0.5 and max(dL, dM) > 2, "swapped chi2 B %.2f (was %.2f), L %.2f (%.2f), Mo %.2f (%.2f)" % (sw["B_canonical"], X["B_canonical"], sw["L"], X["L"], sw["Mo"], X["Mo"]))
    R["swap"] = sw

# ---------------------------------------------------------------- MUTATE reading
if MUTATE:
    main = json.load(open(os.path.join(HERE, "cfg100_results.json")))
    dcan = abs(X["B_canonical"] - main["chi2"]["B_canonical"]); dalt = abs(X["B_alt"] - main["chi2"]["B_alt"])
    dmo = abs(X["Mo"] - main["chi2"]["Mo"]); dl = abs(X["L"] - main["chi2"]["L"])
    check("K9 MUTATE: B unchanged, Mo moves", dcan < 0.1 and dalt < 0.1 and dmo > 3,
          "B canon %.3f -> %.3f, B alt %.3f -> %.3f, Mo %.2f -> %.2f (d=%.2f), L %.2f -> %.2f (d=%.2f)" % (main["chi2"]["B_canonical"], X["B_canonical"], main["chi2"]["B_alt"], X["B_alt"], main["chi2"]["Mo"], X["Mo"], dmo, main["chi2"]["L"], X["L"], dl))
    R["mutate_delta"] = dict(B_canonical=dcan, B_alt=dalt, Mo=dmo, L=dl)
    R["checks"] = checks
    json.dump(R, open(OUT, "w"), indent=1)
    log("elapsed %.0fs; checks %d/%d; rc %d" % (time.time() - T0, sum(checks.values()), len(checks), 0 if all(checks.values()) else 1))
    sys.exit(0 if all(checks.values()) else 1)

# ---------------------------------------------------------------- reproduction table
log("== reproduction against CFG110's stated numbers")
def rep(name, mine, target, dig, tol_rel=0.10):
    ok = round(mine, dig) == round(target, dig)
    st = "REPRODUCED" if ok else ("APPROXIMATE" if abs(mine / target - 1) <= tol_rel else "DIFFERENT")
    log("  %-34s mine %-10.4g CFG110 %-8g %s" % (name, mine, target, st))
    return st
R["repro"] = {
 "P1 B canon chi2": rep("P1 B canonical chi2/14", X["B_canonical"], 22.2, 1),
 "P1 B alt chi2": rep("P1 B alt chi2/14", X["B_alt"], 22.2, 1),
 "P1 p": rep("P1 p(B canonical)", R["p"]["B_canonical"], 0.075, 3),
 "P2 Mo chi2": rep("P2 Moster chi2/14", X["Mo"], 105, 0),
 "P3 R0": rep("P3 lambda(L-B)", lam_LB, 8.8, 1),
 "L chi2": rep("L chi2/14", X["L"], 25.2, 1),
 "p(L)": rep("p(L)", R["p"]["L"], 0.033, 3),
 "MoB power": rep("lambda(Mo-B)", lam_MB, 87, 0),
}
# per class
def perclass(k):
    o = []
    for c in (0, 1):
        s = slice(7 * c, 7 * c + 7)
        o.append(chi2((Dd - DM[k])[s], C[s, s], hart(7)))
    return o
pc = {k: perclass(k) for k in ("B_canonical", "L", "Mo", "Mo_m")}
R["perclass"] = pc
targets = {"B_canonical": (13.4, 6.5), "L": (21.8, 5.1), "Mo": (25.2, 55.0)}
for k, t in targets.items():
    for c, nm in ((0, "late"), (1, "early")):
        rep("R1 %s %s chi2/7" % (k, nm), pc[k][c], t[c], 1)
log("  per-class chi2 (7 bins, own Hartlap): " + "; ".join("%s late %.2f early %.2f" % (k, v[0], v[1]) for k, v in pc.items()))
log("  variants: Mo_m chi2 %.2f (p %.2g), lambda(Mo_m-B) = %.2f;  B_alt-B_canonical dchi2 %.3f" % (X["Mo_m"], R["p"]["Mo_m"], lam(DM["Mo_m"] - DM["B_canonical"], C, h14), X["B_alt"] - X["B_canonical"]))
R["lam"] = dict(LB=lam_LB, MoB=lam_MB, Mo_mB=lam(DM["Mo_m"] - DM["B_canonical"], C, h14))
R["D"] = dict(data=Dd.tolist(), sigma=np.sqrt(np.diag(C)).tolist(), **{k: DM[k].tolist() for k in kinds})
R["readings"] = dict(H1_B_canon=R["p"]["B_canonical"] > 0.01, H1_B_alt=R["p"]["B_alt"] > 0.01, H2_L=R["p"]["L"] > 0.01)
log("  readings: H1 canon %s alt %s (p %.3f / %.3f);  H2 L %s (p %.3f);  lambda(L-B) %.2f %s 9" % (R["readings"]["H1_B_canon"], R["readings"]["H1_B_alt"], R["p"]["B_canonical"], R["p"]["B_alt"], R["readings"]["H2_L"], R["p"]["L"], lam_LB, ">=" if lam_LB >= 9 else "<"))

# ---------------------------------------------------------------- R6 pair-weighted model stacks
mpw = {k: np.array([mstack_pw(tabs[k], m) for m in masks_main]) for k in ("B_canonical", "L", "Mo")}
Dpw = {k: model_D(mpw[k], K1) for k in mpw}
Xpw = {k: chi2(Dd - Dpw[k], C, h14) for k in mpw}
log("== R6 pair-weighted (WW) model stacks: " + ", ".join("%s chi2 %.2f (p %.3g)" % (k, Xpw[k], pv(Xpw[k], 14)) for k in Xpw) + ";  lambda(L-B) %.2f lambda(Mo-B) %.2f" % (lam(Dpw["L"] - Dpw["B_canonical"], C, h14), lam(Dpw["Mo"] - Dpw["B_canonical"], C, h14)))
R["R6"] = dict(chi2=Xpw, lamLB=lam(Dpw["L"] - Dpw["B_canonical"], C, h14), lamMB=lam(Dpw["Mo"] - Dpw["B_canonical"], C, h14))

# ---------------------------------------------------------------- R7 amplitude fits (+- 0.1 dex M* shift)
P = h14 * np.linalg.inv(C)
rB = Dd - DM["B_canonical"]
log("== R7 amplitude fits  D - D_B = A (D_shape - D_B)   [A=0 B, A=1 shape; stat error only]")
R["R7"] = {}
for nm, ks in (("L", ("L", "L-", "L+")), ("Mo", ("Mo", "Mo-", "Mo+"))):
    for kk in ks:
        if kk in DM: dmk = DM[kk]
        else:
            dmk = model_D(np.array([mstack(tabs[kk], m) for m in masks_main]), K1)
        s = dmk - DM["B_canonical"]
        A = float(s @ P @ rB / (s @ P @ s)); sA = float((s @ P @ s) ** -0.5)
        R["R7"][kk] = dict(A=A, sA=sA, z0=A / sA, ub95=A + 1.645 * sA, lo95=A - 1.645 * sA, lam=float(s @ P @ s), chi2=chi2(Dd - dmk, C, h14))
        log("  shape %-4s: A = %+.3f +- %.3f  (z(A=0) %+.2f;  A=1 is %.2f sigma away; one-sided 95%% UL %.3f; lambda %.2f; chi2 %.2f)" % (kk, A, sA, A / sA, (1 - A) / sA, A + 1.645 * sA, s @ P @ s, R["R7"][kk]["chi2"]))

# ---------------------------------------------------------------- power analysis
log("== POWER of B's mass-independence chi2 (14 dof, alpha 0.05; Hartlap-consistent lambda = mu^T h C^-1 mu)")
crit = float(stats.chi2.ppf(0.95, 14)); log("  chi2_crit(14, 0.05) = %.3f" % crit)
alts = {"(a) colour-split LCDM": DM["L"] - DM["B_canonical"], "(b) half of (a)": 0.5 * (DM["L"] - DM["B_canonical"]), "(c) Moster": DM["Mo"] - DM["B_canonical"]}
R["power"] = {}
rng = np.random.default_rng(100)
Lc = np.linalg.cholesky(C / h14); Cinv = np.linalg.inv(C)
for nm, mu in alts.items():
    l_ = lam(mu, C, h14)
    pw = float(stats.ncx2.sf(crit, 14, l_)) if l_ > 0 else 0.05
    zdraw = rng.standard_normal((200000, 14)); x = mu[None] + zdraw @ Lc.T
    ch = h14 * np.einsum("ij,jk,ik->i", x, Cinv, x)
    mc_mean, mc_pow = float(ch.mean()), float(np.mean(ch > crit))
    pw1 = float(stats.norm.sf(1.96 - math.sqrt(l_)) + stats.norm.cdf(-1.96 - math.sqrt(l_)))
    npe = float(stats.norm.cdf(-math.sqrt(l_) / 2))
    contrib = mu * (P @ mu)
    R["power"][nm] = dict(lam=l_, expected_chi2=14 + l_, power_omnibus=pw, mc_mean=mc_mean, mc_power=mc_pow, power_1dof=pw1, NP_error_rate=npe,
                          contrib_late=float(contrib[:7].sum()), contrib_early=float(contrib[7:].sum()), contrib=contrib.tolist())
    log("  %-24s lambda %6.2f  E[chi2_B] %6.2f  power(14dof) %.3f (MC %.3f, MC mean %.2f)  power(1dof amp) %.3f  NP equal-error rate %.3f" % (nm, l_, 14 + l_, pw, mc_pow, mc_mean, pw1, npe))
    log("      per-bin contribution c_i (late, K1 bins 8..14 from low-g/large-R to high-g): %s" % np.round(contrib[:7], 2))
    log("                                 (early):                                       %s   class sums %.2f | %.2f" % (np.round(contrib[7:], 2), contrib[:7].sum(), contrib[7:].sum()))
    # leave-one-bin-out (drop a bin from both classes, same h, sub-block covariance)
    lb = []
    for j in range(7):
        keep = [i for i in range(14) if i % 7 != j]
        lb.append(float(h14 * mu[keep] @ np.linalg.solve(C[np.ix_(keep, keep)], mu[keep])))
    sz = (mu / np.sqrt(np.diag(C))) ** 2 * h14
    R["power"][nm]["loo_bin"] = lb
    log("      lambda dropping bin j (both classes) j=8..14: %s   (full %.2f)" % (np.round(lb, 2), l_))
    log("      single-bin z^2 (late): %s   (early): %s" % (np.round(sz[:7], 2), np.round(sz[7:], 2)))
check_mc = all(abs(v["mc_mean"] / (14 + v["lam"]) - 1) < 0.01 and abs(v["mc_power"] - v["power_omnibus"]) < 0.01 for v in R["power"].values())
check("K10 power machinery (MC vs analytic)", check_mc, "; ".join("%s: mean %.3f vs %.3f, power %.3f vs %.3f" % (k.split()[0], v["mc_mean"], 14 + v["lam"], v["mc_power"], v["power_omnibus"]) for k, v in R["power"].items()))
# detectable amplitude
for nm, key in (("L", "(a) colour-split LCDM"), ("Mo", "(c) Moster")):
    l1 = R["power"][key]["lam"]
    lstar = brentq(lambda l_: stats.ncx2.sf(crit, 14, l_) - 0.8, 0.1, 200)
    R["power"][key]["A80_omnibus"] = math.sqrt(lstar / l1); R["power"][key]["A80_1dof"] = 2.8016 / math.sqrt(l1)
    log("  shape %s: amplitude with 80%% power: omnibus 14-dof test A = %.2f (lambda* %.2f);  1-dof amplitude test A = %.2f" % (nm, R["power"][key]["A80_omnibus"], lstar, R["power"][key]["A80_1dof"]))
# wording tests
W = {"W1": R["p"]["B_canonical"] > 0.01, "W2": R["R7"]["L"]["ub95"] < 1, "W3": R["R7"]["L"]["ub95"] < 0.5, "W4": R["R7"]["Mo"]["ub95"] < 1}
R["wording"] = W
log("== wording tests: W1 (p_B>0.01) %s | W2 (UL_L<1) %s | W3 (UL_L<0.5) %s | W4 (UL_Mo<1) %s  => 'B gets mass-independence right' allowed: %s" % (W["W1"], W["W2"], W["W3"], W["W4"], W["W3"]))

# ---------------------------------------------------------------- sensitivities
log("== SENSITIVITY: error inflation (chi2/f^2; lambda/f^2)")
R["inflate"] = {}
for f in (1.0, 1.2, 1.5, 2.0):
    row = {k: X[k] / f ** 2 for k in ("B_canonical", "L", "Mo")}
    row["lamLB"] = lam_LB / f ** 2; row["lamMB"] = lam_MB / f ** 2
    row["powLB"] = float(stats.ncx2.sf(crit, 14, row["lamLB"])); row["powMB"] = float(stats.ncx2.sf(crit, 14, row["lamMB"]))
    R["inflate"][str(f)] = row
    log("  x%.1f: B %.2f (p %.3f)  L %.2f (p %.3f)  Mo %.2f (p %.2g)  lambda(L-B) %.2f power %.2f  lambda(Mo-B) %.1f power %.2f" % (f, row["B_canonical"], pv(row["B_canonical"], 14), row["L"], pv(row["L"], 14), row["Mo"], pv(row["Mo"], 14), row["lamLB"], row["powLB"], row["lamMB"], row["powMB"]))

log("== SENSITIVITY: bin sets (main mass split), local Hartlap")
R["bins"] = {}
sets = {"K1 (8-14)": list(K1)}
for j in K1: sets["K1 minus %d" % j] = [k for k in K1 if k != j]
sets["highest-g 4 (11-14)"] = [11, 12, 13, 14]; sets["lowest-g 3 (8-10)"] = [8, 9, 10]; sets["bins 8-11"] = [8, 9, 10, 11]
for nm, Ks in sets.items():
    Dk, Ck = assemble(full4, loo4, Ks); pk = 2 * len(Ks); hk = hart(pk)
    dm = {k: model_D(m4[k], Ks) for k in ("B_canonical", "L", "Mo")}
    row = {k: chi2(Dk - dm[k], Ck, hk) for k in dm}
    row["dof"] = pk; row["lamLB"] = lam(dm["L"] - dm["B_canonical"], Ck, hk); row["lamMB"] = lam(dm["Mo"] - dm["B_canonical"], Ck, hk)
    R["bins"][nm] = row
    log("  %-22s dof %2d: B %6.2f (p %.3f) L %6.2f (p %.3f) Mo %7.2f  lambda(L-B) %5.2f lambda(Mo-B) %6.1f" % (nm, pk, row["B_canonical"], pv(row["B_canonical"], pk), row["L"], pv(row["L"], pk), row["Mo"], row["lamLB"], row["lamMB"]))

log("== SENSITIVITY: mass-split edges (K1, 14 bins; own jackknife)")
R["edges"] = {}
for sc in ("q50", "q40|q60", "q33|q67", "q25|q75", "s-0.1", "s+0.1"):
    mk = masks_for(sc); f4, l4 = data4(mk); Dk, Ck = assemble(f4, l4, K1)
    mm = {k: np.array([mstack(tabs[k], m) for m in mk]) for k in ("B_canonical", "L", "Mo")}
    dm = {k: model_D(mm[k], K1) for k in mm}
    row = {k: chi2(Dk - dm[k], Ck, h14) for k in dm}
    row["lamLB"] = lam(dm["L"] - dm["B_canonical"], Ck, h14); row["lamMB"] = lam(dm["Mo"] - dm["B_canonical"], Ck, h14)
    row["n"] = [int(m.sum()) for m in mk]
    R["edges"][sc] = row
    log("  %-8s n=%s: B %6.2f (p %.3f) L %6.2f (p %.3f) Mo %7.2f  lambda(L-B) %5.2f lambda(Mo-B) %6.1f" % (sc, row["n"], row["B_canonical"], pv(row["B_canonical"], 14), row["L"], pv(row["L"], 14), row["Mo"], row["lamLB"], row["lamMB"]))

R["checks"] = checks; R["frozen_sha256"] = FROZEN_SHA
json.dump(R, open(OUT, "w"), indent=1, default=float)
log("elapsed %.0fs; checks %d/%d; rc %d" % (time.time() - T0, sum(checks.values()), len(checks), 0 if all(checks.values()) else 1))
sys.exit(0 if all(checks.values()) else 1)
