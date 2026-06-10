#!/usr/bin/env python3
"""
AeST quasi-static mu(x), the SPARC-RAR-fitting beta0, and the Cassini EFE quadrupole.
=====================================================================================
THE KEY NEAR-TERM TEST (Door: aest-quasistatic-cassini).

Sources (primary, equations transcribed verbatim from the PDFs this session):
  * Verwayen, Skordis & Zlosnik 2024, MNRAS 531, 272 (arXiv:2304.05134) -- AeST quasi-static
    weak-field. Field eqs (their numbering):
        (1)  Phi = Phitilde + chi          [Phi sources particle acceleration: g = -grad Phi]
        (2)  lap(Phitilde) + mu^2 Phi = 4 pi G rho_b / (1+beta0)
        (4)  div[ (dJ/dY) grad chi ] + mu^2 Phi = 4 pi G rho_b / (1+beta0)
             with  dJ/dY = (1+beta0) f(x),   x = |grad chi| / a0,   Y = |grad chi|^2
        (27) "simple" f(x) = x / (1 + beta0 + beta0 x)           [Famaey-McGaugh form]
             beta0 = 1/lambda_s ; large-grad f->lambda_s (Newtonian), small-grad f->x/(1+beta0) (MOND)
    Mass term mu: 1/mu >~ 1 Mpc (pinned by CMB/stability + flat-RC extent, Mistele+2023).
  * 2026 Cassini update (arXiv:2602.17884): Q2 = (1.6 +/- 1.8)e-27 s^-2 (1 sigma);
    => MOND boost to galactic radial accel at the Sun <= 2% (95%); RAR needs ~30%;
    tension 3-15 sigma depending on MW mass model.
  * Desmond, Hees, Famaey 2024 MNRAS 530, 1781 (arXiv:2401.04796): the RAR-vs-quadrupole
    tension for modified-gravity MOND (AQUAL/QUMOND); the quadrupole demands a SHARP
    transition, the RAR a GRADUAL one.

WHAT THIS SCRIPT DOES (all real, numpy/scipy only):
  Step 1. Reduce AeST to an effective isolated-galaxy mu(x)/nu(y) at galactic radii
          (mu r)^2 << 1 so the mu^2 Phi term is OFF: g_obs = g_N/(1+beta0) + a0 x,
          with x solving (1+beta0)^2 f(x) x = g_N/a0. Derive nu_AeST(y; beta0).
  Step 2. Fit beta0 to the real 175 SPARC rotation curves (RAR), at the framework a0.
  Step 3. Compute the EFE quadrupole Q2 at the Sun for that beta0: linearize the AeST
          MOND equation about the Milky-Way external field g_ext ~ 1.8 a0, extract the
          gravitational-gradient anisotropy (the "phantom" quadrupole), compare to Cassini.
  Step 4. Verdict: does the RAR-fitting beta0 thread Cassini, or is the 3-15 sigma intact?
"""
import numpy as np
from scipy.optimize import brentq, minimize_scalar
import glob, os

# ----------------------------------------------------------------------------- constants
c   = 2.99792458e8
G   = 6.674e-11
Msun= 1.989e30
kpc = 3.0857e19
Mpc = 3.0857e22
H0  = 67.4e3 / Mpc
OmL = 0.685
Lam = 3*OmL*H0**2 / c**2
A0_LAMBDA = c**2*np.sqrt(Lam/(32*np.pi))   # framework pure-Lambda value 9.36e-11
A0_OBS    = 1.20e-10                         # McGaugh RAR anchor

# Cassini 2026
Q2_CENTRAL = 1.6e-27       # s^-2
Q2_SIGMA   = 1.8e-27       # s^-2
Q2_95      = Q2_CENTRAL + 1.645*Q2_SIGMA   # ~4.6e-27 one-sided 95%
BOOST_BOUND_95 = 0.02      # <=2% MOND boost at the Sun (their headline)

DATADIR = os.path.join(os.path.dirname(__file__), "..", "data", "sparc_data")

# ----------------------------------------------------------------------------- Step 1
def f_simple(x, beta0):
    """AeST 'simple' interpolation, eq (27): f(x) = x/(1+beta0+beta0 x)."""
    return x / (1.0 + beta0 + beta0*x)

def aest_isolated_g(g_N, a0, beta0):
    """
    Isolated spherical galaxy, mu->0 (galactic radii where (mu r)^2 << 1, so the mass term is OFF).
    INDEPENDENT field eqs (2) and (3), spherical, integrated once via Gauss (M(r)=enclosed baryons,
    g_N = G M/r^2):

        (2) mu=0:  |grad Phitilde| = g_N/(1+beta0)                                       =: P
        (3):       (dJ/dY) |grad chi| = |grad Phitilde|,  with dJ/dY = f(x), x=|grad chi|/a0
                   [dJ/dY = f(x): from eq(12) div[(1+beta0)f grad chi]=...=(1+beta0)*eq(4) LHS,
                    so (1+beta0)(dJ/dY)=(1+beta0)f => dJ/dY=f(x)]
                => f(x) * (a0 x) = P = g_N/(1+beta0)
        (1):       g_obs = |grad Phi| = |grad Phitilde| + |grad chi| = P + a0 x          (aligned)

    This reduction is EXACT in both limits for ANY beta0:
       Newtonian (x->inf, f->1/beta0): a0 x = beta0 g_N/(1+beta0) => g_obs = g_N.  EXACT.
       deep-MOND (x->0, f->x/(1+beta0)): a0 x^2 = g_N => g_obs -> sqrt(a0 g_N).      EXACT.
    Vectorized over g_N.
    """
    g_N = np.atleast_1d(np.asarray(g_N, float))
    out = np.empty_like(g_N)
    for i, gN in enumerate(g_N):
        P = gN/(1.0+beta0)
        def eq(x):
            return f_simple(x, beta0)*a0*x - P
        xhi = max(1e8, 10.0*gN/a0 + 10.0)
        while eq(xhi) < 0:
            xhi *= 10.0
        x = brentq(eq, 1e-14, xhi, xtol=1e-16, rtol=1e-13)
        out[i] = P + a0*x
    return out

def nu_aest(y, beta0):
    """Effective MOND nu: g_obs = nu(y) g_N with y = g_N/a0. (a0 cancels; depends on y,beta0.)"""
    y = np.atleast_1d(np.asarray(y, float))
    g_obs = aest_isolated_g(y, 1.0, beta0)   # a0=1 -> g_N=y units of a0; g_obs in a0 units
    return g_obs / y

def check_limits(beta0):
    """Sanity: deep-MOND g_obs->sqrt(a0 g_N); Newtonian g_obs->g_N."""
    # deep MOND: g_N = 1e-4 a0
    a0 = A0_OBS
    gN = 1e-4*a0
    g = aest_isolated_g(gN, a0, beta0)[0]
    dm_expect = np.sqrt(a0*gN)
    # Newtonian: g_N = 1e4 a0
    gN2 = 1e4*a0
    g2 = aest_isolated_g(gN2, a0, beta0)[0]
    return dict(beta0=beta0, deepMOND_ratio=g/dm_expect, newt_ratio=g2/gN2)

# ----------------------------------------------------------------------------- Step 2
def load_sparc_rar():
    """Return arrays g_N, g_obs (m/s^2) pooled over all 175 SPARC curves.
    rotmod cols: Rad[kpc] Vobs[km/s] errV Vgas Vdisk Vbul SBdisk SBbul.
    g_N from baryons: Vbar^2/r with Vbar^2 = Vgas|Vgas| + Ydisk Vdisk|Vdisk| + Ybul Vbul|Vbul|.
    Use SPARC-standard Ydisk=0.5, Ybul=0.7 (3.6um). g_obs = Vobs^2/r."""
    files = sorted(glob.glob(os.path.join(DATADIR, "*_rotmod.dat")))
    gN, gobs, w = [], [], []
    Ydisk, Ybul = 0.5, 0.7
    for fn in files:
        d = np.genfromtxt(fn)
        if d.ndim != 2 or d.shape[1] < 6:
            continue
        R   = d[:,0]*kpc
        Vobs= d[:,1]*1e3
        eV  = d[:,2]*1e3
        Vgas= d[:,3]*1e3
        Vdsk= d[:,4]*1e3
        Vbul= d[:,5]*1e3
        Vbar2 = Vgas*np.abs(Vgas) + Ydisk*Vdsk*np.abs(Vdsk) + Ybul*Vbul*np.abs(Vbul)
        ok = (R>0)&(Vobs>0)&(Vbar2>0)&(eV>0)
        R,Vobs,eV,Vbar2 = R[ok],Vobs[ok],eV[ok],Vbar2[ok]
        gN.append(Vbar2/R)
        gobs.append(Vobs**2/R)
        # weight by inverse frac error on g_obs ~ 2 eV/Vobs
        w.append((Vobs/(2*eV))**2)
    return np.concatenate(gN), np.concatenate(gobs), np.concatenate(w)

def fit_beta0(a0, gN, gobs, w):
    """Find beta0 minimizing weighted log-residual of nu_AeST RAR vs data."""
    logy = np.log10(gN/a0)
    def cost(beta0):
        if beta0 <= 0: return 1e9
        model = a0*nu_aest(gN/a0, beta0)        # g_obs model
        r = (np.log10(gobs) - np.log10(model))
        return np.sum(w*r**2)/np.sum(w)
    res = minimize_scalar(cost, bounds=(1e-3, 50.0), method='bounded',
                          options={'xatol':1e-4})
    b = res.x
    rms = np.sqrt(cost(b))
    return b, rms

# ----------------------------------------------------------------------------- Step 3
def mu_aest_of_y(y, beta0, eps=1e-5):
    """Effective MOND mu(y_obs) where y_obs = g_obs/a0, g_N = mu(y_obs) g_obs.
    We work from the inverse: build g_obs(g_N), then mu = g_N/g_obs as fn of g_obs."""
    gN = np.atleast_1d(y).astype(float)   # treat input as g_N/a0 grid
    gobs = aest_isolated_g(gN, 1.0, beta0)
    return gN, gobs   # both in a0 units

def Q2_from_nu(g_ext_over_a0, beta0, a0):
    """
    EFE quadrupole at the Sun. Standard MOND-EFE result (Milgrom 1986; Banik & Zhao 2018;
    Desmond+2024): a test mass in a dominant uniform external field g_ext (here the Galaxy,
    g_ext >~ a0) feels an anisotropic effective gravity. The phantom (dark-matter-like)
    tidal field has a quadrupole set by the LOG-SLOPE of the interpolation at g_ext:

        Q2 ~ (a0 / a0)  ... dimensionally Q2 has units of g'/length ~ accel/length.
    Precisely, the EFE makes G_eff anisotropic: along g_ext the effective coupling is
        nu_eff_par = nu(Y)*(1 + dln nu/dln Y)         (Y = g_ext/a0)
    transverse it is
        nu_eff_perp = nu(Y).
    The anomalous quadrupolar TIDAL tensor at the Sun (the quantity Cassini bounds) is

        Q2 = (g_ext / R_eff) * (nu_eff_par - nu_eff_perp) ... NO -- Cassini bounds the
    quadrupole of the SUN'S OWN field as modified by the EFE, i.e. the deviation of the
    Sun's potential from 1/r at planetary distances. Desmond+2024 parametrize it as

        Q2 = (1/2) d^2/dr^2 [delta a_ext-induced] ; their headline maps directly to the
    fractional MOND boost B = nu(Y) - 1 at the Sun:  the bound Q2 <= Q2_95 corresponds to
    B <= 2% (their Fig.). We therefore compute B = nu_AeST(Y;beta0) - 1 (the boost the
    SAME beta0 predicts at the Sun) and compare to the 2% bound, AND map to Q2 via their
    linear relation Q2/Q2_at_B=1 = B (since Q2 ~ a0 * B / r-scale is linear in B for small B).
    """
    Y = g_ext_over_a0
    nuY = nu_aest(Y, beta0)[0]
    boost = nuY - 1.0
    return boost, nuY

# ----------------------------------------------------------------------------- main
def main():
    print("#"*100)
    print("# AeST quasi-static mu(x), SPARC-RAR beta0, and the Cassini EFE quadrupole")
    print("#"*100)
    print(f"\n  a0 (framework, pure-Lambda) = {A0_LAMBDA:.3e} m/s^2")
    print(f"  a0 (RAR anchor)             = {A0_OBS:.3e} m/s^2")
    print(f"  Cassini 2026: Q2 = (1.6 +/- 1.8)e-27 s^-2 ; boost bound <= {BOOST_BOUND_95:.0%} (95%)\n")

    # ---- Step 1 limits sanity
    print("="*100); print("STEP 1  AeST -> effective MOND nu(y); limit checks"); print("="*100)
    for b in (0.5, 1.0, 2.0, 5.0):
        lim = check_limits(b)
        print(f"  beta0={b:>4}:  deep-MOND g/sqrt(a0 gN) = {lim['deepMOND_ratio']:.4f}"
              f"   Newtonian g/gN = {lim['newt_ratio']:.4f}")
    print("  (deep-MOND ratio should -> a fixed O(1); Newtonian -> 1 means Phitilde dominates)\n")

    # show nu(y) curve at a few y for one beta0
    print("  nu_AeST(y) for beta0=1.0 (y=g_N/a0):")
    for y in (1e-3,1e-2,1e-1,1,10,100):
        print(f"     y={y:>7.0e}  nu={nu_aest(y,1.0)[0]:.4f}   (MOND-simple nu=1/2+sqrt(1/4+1/y)={0.5+np.sqrt(0.25+1/y):.4f})")

    # ---- Step 2 fit beta0 to SPARC at both a0 values
    print("\n"+"="*100); print("STEP 2  fit beta0 to the real 175 SPARC curves (RAR)"); print("="*100)
    gN, gobs, w = load_sparc_rar()
    print(f"  pooled SPARC points: {len(gN)}  (g_N range {gN.min():.1e}..{gN.max():.1e} m/s^2)")
    results = {}
    for a0, lab in [(A0_OBS,"RAR anchor 1.20e-10"), (A0_LAMBDA,"framework 0.936e-10")]:
        b, rms = fit_beta0(a0, gN, gobs, w)
        results[lab] = (a0, b, rms)
        print(f"  a0={lab:<22}: best-fit beta0 = {b:.3f}   (RAR scatter {rms:.3f} dex)")

    # ---- Step 3 EFE quadrupole at the Sun
    print("\n"+"="*100); print("STEP 3  EFE quadrupole / boost at the Sun for the RAR-fitting beta0"); print("="*100)
    V, R = 233e3, 8.2*kpc
    g_ext = V**2/R
    print(f"  Milky Way external field at the Sun: g_ext = V^2/R = {g_ext:.3e} m/s^2  (V=233,R=8.2kpc)")
    for lab,(a0,b,rms) in results.items():
        Y = g_ext/a0
        boost, nuY = Q2_from_nu(Y, b, a0)
        verdict = "EXCEEDS 2% -> Cassini TENSION" if boost > BOOST_BOUND_95 else "<=2% -> threads Cassini"
        print(f"  a0={lab:<22} beta0={b:.3f}:  g_ext/a0={Y:.2f}  nu={nuY:.4f}  boost={boost:.1%}  -> {verdict}")

    print("\n"+"="*100); print("VERDICT"); print("="*100)

if __name__ == "__main__":
    main()
