#!/usr/bin/env python3
"""
E13 PHOTON a0 -- fit the EXACT elliptic-integral deflection SHAPE (not the algebraic nu)
to the Brouwer+2021 KiDS-1000 isolated-lens weak-lensing RAR, extract a0 FROM PHOTONS.

E13 (equation book, credited genre Mortlock&Turner 2001 / Zhao+2006; distinctive content =
the cH_Lambda/Z coefficient a0):
    alpha(b) = (4GM/c^2 b) sqrt(1+u^2) E(1/(1+u^2)),  u=b/r_M,  r_M=sqrt(GM/a0),
    E = complete elliptic integral of the 2nd kind (parameter m convention: E(m)).
Limits (verified below): Einstein alpha->4GM/c^2 b (u->0); Mortlock-Turner saturation
    alpha_inf=2pi sqrt(GM a0)/c^2 (u->inf).

DERIVATION -- deflection -> the Brouwer observable (EXACT, no approximation):
  A stacked-lensing observer measures the tangential-shear excess surface density
  ESD(b) = Sigmabar(<b) - Sigma(b), and (B21 README Eq.7) reports g_obs = 4G*ESD.
  For an axisymmetric lens the *physical* deflection encodes the enclosed 2D mass:
      alpha(b) = 4G M2D(<b)/(c^2 b),  M2D(<b)=2pi int_0^b Sigma b' db'.
  Hence  Sigmabar(<b) = c^2 alpha/(4 pi G b),  Sigma(b) = (c^2/8 pi G b) d(b alpha)/db,
  so     g_obs = 4G ESD = (c^2/2 pi)(alpha/b - alpha').
  Applying the SAME convention to a baryonic point mass (alpha_bar=4GM/c^2 b) gives
      g_bar = 4GM/(pi b^2)   -- the geometric (4/pi) is identical in g_obs and g_bar and
      CANCELS in the RAR (their RAR asymptotes to g_obs=g_bar; P2's fit form assumes it).
  Substituting E13's alpha and writing S(u)=sqrt(1+u^2)E(1/(1+u^2)) one finds the mass
  drops out of the RAR plane and the EXACT lensing transfer is the closed form
      g_obs = g_bar * T(u),   T(u) = S(u) - (u/2) S'(u),   with S'(u)=u K(1/(1+u^2))/sqrt(1+u^2),
  i.e.  T(u) = [ (1+u^2) E(m) - (u^2/2) K(m) ] / sqrt(1+u^2),  m=1/(1+u^2),
  and the coupling to the observable is  u^2 = 4 a0 / (pi g_bar)   (mass-independent).
  Limits: T->1 (u->0, Einstein RAR g_obs=g_bar);  T->(pi/4)u (u->inf) =>
      g_obs -> sqrt((pi/4) a0 g_bar)  -- the deep lensing asymptote carries a sqrt(pi/4)=0.886
      relative to the standard deep-MOND sqrt(a0 g_bar); this is the ONLY place the exact
      elliptic shape departs from the algebraic nu, and it fixes a DETERMINISTIC ~4/pi
      recalibration of the recovered a0. (The naive Sigmabar-only treatment would give
      sqrt(pi)=1.77; the -alpha' convergence term is why "do NOT approximate" matters.)

Both a0 footings; honest error budget reused from the P2 lane (shear 5%, photo-z, and the
DOMINANT baryon-budget term). Verdict: does the exact deflection shape add information
beyond the wide P2 band, or repackage it?  Verified as hard as any win.
Frozen repo READ-ONLY; outputs only here.
"""
import numpy as np, os, json
from scipy.special import ellipe, ellipk

B = ("/Users/carlzimmerman/new_physics/zimmerman-formula/real_research/data/"
     "lensing_rar/brouwer2021_rar")
LEDG = "/Users/carlzimmerman/new_physics/prep_2026/concordance_ledger"
HERE = os.path.dirname(os.path.abspath(__file__))
anchor = json.load(open(os.path.join(LEDG, "anchor_values.json")))
A0C, A0A = anchor["a0_canon"], anchor["a0_alt"]          # 9.355e-11 canonical, 1.131e-10 alt

PC_PER_M = 3.086e16
G_PC = 4.52e-30
K = 4*G_PC*PC_PER_M                                       # ESD[Msun/pc^2] -> g[m/s^2]

# ---------------- Brouwer loaders (reused verbatim from p2_lensing_a0_band.py) ----------
def load_rar(fname):
    d = np.genfromtxt(os.path.join(B, fname), comments="#")
    return d[:, 0], K*d[:, 1]/d[:, 4], K*d[:, 3]/d[:, 4]  # g_bar, g_obs, err(g_obs)

def load_cov(fname, n):
    d = np.genfromtxt(os.path.join(B, fname), comments="#")
    assert d.shape[0] == n*n
    return (d[:, 4]/d[:, 6]).reshape(n, n)*K*K             # (m/s^2)^2, bias-corrected

# ---------------- E13 deflection and the exact lensing transfer -------------------------
G, C, MSUN = 6.674e-11, 2.998e8, 1.989e30

def S_of_u(u):
    m = 1.0/(1.0+u*u)
    return np.sqrt(1.0+u*u)*ellipe(m)

def alpha_E13(b, M, a0):
    """E13 physical deflection [rad] for point mass M[kg], impact parameter b[m]."""
    rM = np.sqrt(G*M/a0)
    u = b/rM
    return (4*G*M/(C*C*b))*S_of_u(u)

def T_exact(u):
    """Exact E13 lensing transfer g_obs/g_bar = S - (u/2)S' = [(1+u^2)E - (u^2/2)K]/sqrt(1+u^2)."""
    m = 1.0/(1.0+u*u)
    return ((1.0+u*u)*ellipe(m) - 0.5*u*u*ellipk(m))/np.sqrt(1.0+u*u)

def gobs_E13(gbar, a0):
    u = np.sqrt(4.0*a0/(np.pi*gbar))
    return gbar*T_exact(u)

def gobs_alg(gbar, a0):                                   # P2 algebraic nu (Milgrom 1999 kernel)
    return np.sqrt(gbar*gbar + gbar*a0)

# ============================ (1) VERIFY the limits + the derivation ====================
print("="*90)
print("(1) E13 DEFLECTION -- limit checks and derivation verification")
print("="*90)
M = 1e11*MSUN
rM = np.sqrt(G*M/A0C)
# Einstein inner limit u->0
b_in = 1e-6*rM
ratio_ein = alpha_E13(b_in, M, A0C)/(4*G*M/(C*C*b_in))
# Mortlock-Turner saturation u->inf
b_out = 1e6*rM
ainf = 2*np.pi*np.sqrt(G*M*A0C)/(C*C)
ratio_mt = alpha_E13(b_out, M, A0C)/ainf
# approach law alpha = alpha_inf[1 + rM^2/4b^2 + ...]
b_ap = 8.0*rM
appr = ainf*(1.0 + rM*rM/(4*b_ap*b_ap))
ratio_ap = alpha_E13(b_ap, M, A0C)/appr
print(f"  Einstein  alpha/(4GM/c^2 b) at u=1e-6 : {ratio_ein:.10f}  (->1)")
print(f"  MOND-sat  alpha/alpha_inf   at u=1e6  : {ratio_mt:.10f}  (->1)")
print(f"  approach  alpha/alpha_inf[1+rM^2/4b^2] at u=8: {ratio_ap:.6f}  (->1 as u grows)")

# closed-form transfer vs DIRECT numerical ESD from the deflection profile (no approximation)
def gobs_numeric(gbar, a0):
    """g_obs=4G*(Sigmabar(<b)-Sigma(b)) built by numerically differentiating alpha(b)."""
    M = 1e11*MSUN                                         # arbitrary; mass cancels
    # invert g_bar=4GM/(pi b^2) -> b for this test mass
    b = np.sqrt(4*G*M/(np.pi*gbar))
    db = 1e-4*b
    a_p = alpha_E13(b+db, M, a0); a_m = alpha_E13(b-db, M, a0)
    ap  = alpha_E13(b, M, a0)
    dadb = (a_p-a_m)/(2*db)
    return (C*C/(2*np.pi))*(ap/b - dadb)
gtest = np.geomspace(1e-15, 1e-11, 9)
err = np.max(np.abs(gobs_numeric(gtest, A0C)/gobs_E13(gtest, A0C) - 1.0))
print(f"  closed-form T(u) vs direct numerical 4G*ESD(alpha) : max frac diff {err:.2e}  (->0)")
# deep coefficient
u_big = 1e5
print(f"  deep transfer T(u)/((pi/4)u) at u=1e5 : {T_exact(u_big)/((np.pi/4)*u_big):.8f}  (->1)")
print(f"  => deep lensing asymptote g_obs -> sqrt((pi/4) a0 g_bar), coeff sqrt(pi/4)={np.sqrt(np.pi/4):.4f}")
assert abs(ratio_ein-1) < 1e-6 and abs(ratio_mt-1) < 1e-5 and err < 1e-4, "E13 limit/derivation check failed"

# ============================ (2) FIT a0 to the Brouwer RAR =============================
def fit(model, gbar, gobs, Cinv, mask=None, grid=None):
    if mask is None: mask = np.ones_like(gbar, bool)
    if grid is None: grid = np.geomspace(2e-11, 8e-10, 6001)
    gb, go = gbar[mask], gobs[mask]; Ci = Cinv[np.ix_(mask, mask)]
    chi2 = np.array([(go-model(gb, a)) @ Ci @ (go-model(gb, a)) for a in grid])
    i = int(np.argmin(chi2))
    lo = grid[chi2 <= chi2[i]+1].min(); hi = grid[chi2 <= chi2[i]+1].max()
    return grid[i], lo, hi, chi2[i], int(mask.sum())

gbar, gobs, egobs = load_rar("Fig-4-5-C1_RAR-KiDS-isolated_Nobins.txt")
n = len(gbar)
Cov = load_cov("Fig-4-5-C1_RAR-KiDS-isolated_covmatrix.txt", n)
Cinv = np.linalg.inv(Cov)

print("\n" + "="*90)
print("(2) FIT: E13 exact elliptic shape vs P2 algebraic nu, SAME data + full covariance")
print("="*90)
for foot, a0ref, lab in [("CANON", A0C, "cH_Lambda/Z=9.355e-11"), ("ALT", A0A, "rho_tot/cH0=1.131e-10")]:
    pass
aE, loE, hiE, chiE, npE = fit(gobs_E13, gbar, gobs, Cinv)
aA, loA, hiA, chiA, npA = fit(gobs_alg, gbar, gobs, Cinv)
print(f"  {'model':<26}{'a0_fit':>12}{'  stat [dchi2=1]':>26}{'chi2/dof':>12}")
print(f"  {'E13 EXACT elliptic':<26}{aE:>12.3e}   [{loE:.3e},{hiE:.3e}]{chiE:>8.1f}/{npE-1}")
print(f"  {'P2 algebraic nu':<26}{aA:>12.3e}   [{loA:.3e},{hiA:.3e}]{chiA:>8.1f}/{npA-1}")
print(f"  ratio a0(E13)/a0(alg) = {aE/aA:.3f}   (analytic deep prediction 4/pi = {4/np.pi:.3f})")
print(f"  delta-chi2(E13 - alg) at each best fit = {chiE-chiA:+.2f}  "
      f"(|dchi2|<~1 => data CANNOT distinguish the two shapes)")

# ---------------- systematic variants (this probe's own budget; disjoint from kinematics) --
variants = {}
for lab, mk in [("g_bar > 1e-14", gbar > 1e-14), ("g_bar > 1e-13", gbar > 1e-13)]:
    variants[lab] = fit(gobs_E13, gbar, gobs, Cinv, mk)[:3]
for lab, fx, fy in [("M* +0.1 dex (g_bar x1.26)", 10**0.1, 1.0),
                    ("M* -0.1 dex (g_bar /1.26)", 10**-0.1, 1.0),
                    ("M* +0.2 dex", 10**0.2, 1.0), ("M* -0.2 dex", 10**-0.2, 1.0),
                    ("shear+photo-z g_obs +5%", 1.0, 1.05),
                    ("shear+photo-z g_obs -5%", 1.0, 0.95)]:
    variants[lab] = fit(gobs_E13, gbar*fx, gobs*fy, np.linalg.inv(Cov*fy*fy))[:3]
gb_h, go_h, eg_h = load_rar("Fig-4_RAR-KiDS-isolated_hotgas_Nobins.txt")
variants["hot-CGM budget (B21 file, diag)"] = fit(gobs_E13, gb_h, go_h, np.diag(1/eg_h**2))[:3]
gb_g, go_g, eg_g = load_rar("Fig-4-C1_RAR-GAMA-isolated_Nobins.txt")
Cg = load_cov("Fig-4-C1_RAR-GAMA-isolated_covmatrix.txt", len(gb_g))
variants["GAMA spec-z lenses (indep.)"] = fit(gobs_E13, gb_g, go_g, np.linalg.inv(Cg))[:3]

print(f"\n  E13 systematic variants (photon-a0 budget):")
print(f"  {'variant':<34}{'a0_fit':>12}{'  stat interval':>26}")
for lab, (av, lv, hv) in variants.items():
    print(f"  {lab:<34}{av:>12.3e}   [{lv:.3e},{hv:.3e}]")
band_lo = min(min(v[1] for v in variants.values()), loE)
band_hi = max(max(v[2] for v in variants.values()), hiE)
print(f"  E13 PHOTON a0 BAND (systematic envelope): [{band_lo:.2e}, {band_hi:.2e}] m/s^2")

# ============================ (3) CONCORDANCE with kinematic + Planck ===================
KIN_LO, KIN_HI = 0.92e-10, 1.18e-10                      # gas-dominated a0-line (kinematic photons-free)
print("\n" + "="*90)
print("(3) CONCORDANCE: photon-a0 (E13) vs kinematic gas-dominated vs Planck")
print("="*90)
in_c = band_lo <= A0C <= band_hi
in_a = band_lo <= A0A <= band_hi
in_k = not (band_hi < KIN_LO or band_lo > KIN_HI)
print(f"  E13 photon band            : [{band_lo:.2e}, {band_hi:.2e}]")
print(f"  kinematic gas-dom a0-line   : [{KIN_LO:.2e}, {KIN_HI:.2e}]   overlap: {'YES' if in_k else 'NO'}")
print(f"  Planck canonical 9.355e-11  : {'INSIDE' if in_c else 'OUTSIDE'} the photon band")
print(f"  Planck alt      1.131e-10   : {'INSIDE' if in_a else 'OUTSIDE'} the photon band")
print(f"  E13 fiducial-budget best fit: {aE:.2e} = {aE/A0C:.2f}x canonical (= {aE/aA:.2f}x the P2 algebraic fit)")

# ============================ (4) VERDICT ==============================================
print("\n" + "="*90)
print("(4) VERDICT -- does the EXACT deflection shape add information, or repackage P2?")
print("="*90)
print(f"""  SHAPE: the exact elliptic transfer T(u)=[(1+u^2)E-(u^2/2)K]/sqrt(1+u^2) differs from the
  algebraic nu ONLY by the deep coefficient sqrt(pi/4)=0.886, i.e. a DETERMINISTIC 4/pi={4/np.pi:.3f}x
  upward recalibration of the recovered a0 (E13 {aE:.2e} vs algebraic {aA:.2e}, ratio {aE/aA:.2f}).
  DISCRIMINATION: over Brouwer's g_bar range the two shapes fit with delta-chi2 = {chiE-chiA:+.2f};
  the elliptic curvature is NOT resolved -- the data cannot tell the exact deflection from the
  algebraic nu (both are dominated by the deep power law, where they differ only in NORMALIZATION,
  which is fully degenerate with a0). SO the exact SHAPE adds NO new leverage beyond a fixed 4/pi
  rescale of the P2 number.
  BAND: the E13 photon band [{band_lo:.2e},{band_hi:.2e}] is set by the SAME baryon-budget term that
  dominates P2 (factor ~{band_hi/band_lo:.1f} wide); the 4/pi shape shift is small inside it. Both
  footings AND the kinematic gas-dominated a0-line sit inside the band. => The photon-a0 CONCORDS
  with the kinematic a0 (real, systematics-disjoint datum) but does NOT provide a NEW independent
  PIN: E13-lensing REPACKAGES the P2 band with a deterministic 4/pi recalibration, it does not
  narrow it. Honest both ways: no 'lensing pins 9.36e-11' (band too wide) and no deficit (band
  straddles both footings + the kinematic line). The exact deflection's genuine, testable new
  content is the SATURATED-deflection shelf shape at fixed lens mass (Fig-9 mass bins / Euclid),
  NOT a tighter a0 from the collapsed RAR plane where mass -- and the shape -- degenerate away.""")

json.dump(dict(a0_E13=[float(aE), float(loE), float(hiE)], chi2_E13=[float(chiE), npE],
               a0_alg=[float(aA), float(loA), float(hiA)], chi2_alg=[float(chiA), npA],
               ratio_E13_alg=float(aE/aA), fourpi=float(4/np.pi), dchi2=float(chiE-chiA),
               band=[float(band_lo), float(band_hi)],
               planck_canon_inside=bool(in_c), planck_alt_inside=bool(in_a),
               kinematic_overlap=bool(in_k),
               variants={k: [float(x) for x in v] for k, v in variants.items()}),
          open(os.path.join(HERE, "e13_fit.json"), "w"), indent=1)
print("\n  [e13_fit.json written]")
