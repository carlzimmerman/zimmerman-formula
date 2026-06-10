#!/usr/bin/env python3
"""
Door II bounded calculation: the Deffayet-Woodard nonlocal-metric MOND model vs the 2026 Cassini quadrupole
===========================================================================================================
agentD, 2026-06-10.  Decides the pre-registered fork from agentC_covariance_memo.md section 4:
  Q2 >= ~1e-26 robustly  -> DEW loophole joins AeST at the Cassini wall (perimeter re-closes)
  Q2 <= ~1e-27 with an RAR-compatible function -> the loophole leads
  in between / open -> say so.

STEP 1 RESULT (paper transcription, /tmp/dew/d2026/synthesis.tex + /tmp/dew/d2011/dew2011.tex):
  The DEW 2026 model (arXiv:2512.10513, JCAP 04 (2026) 081) IS AQUAL-reducible in the static
  weak-field limit.  Verbatim ingredients:
    Z[g] = (4c^4/a0^2) g^{mu nu} d_mu[box^-1 R_ab u^a u^b] d_nu[box^-1 R_rs u^r u^s]
            -> (4c^4/a0^2) grad(Psi).grad(Psi)              [their eq (Zdef)]
    f(Z) = (1/2) Z exp(-sqrt(|Z|)/3)                        [their eq (fdef)]
    deep-MOND g00 equation: (2c^2/a0 r^2) d/dr[r Psi']^2 = (8 pi G/c^2) rho   [their eq (BTFR3)]
    lensing tie: Phi = -Psi (ij Einstein equations unmodified) [their eqs (G00),(Gij)]
  Static limit derived here (two independent routes, Cartesian (Psi,Phi) Lagrangian and the
  2011 (a,b) Schwarzschild-gauge variation, BOTH give):
       div[ mu(|grad Psi|) grad Psi ] = 4 pi G rho / c^2          (Bekenstein-Milgrom AQUAL
                                                                   in the TOTAL potential)
       mu(g) = 1 - 2 f'(Z) = 1 - exp(-y) (1 - y/2),   y = 2g/(3a0),  g = c^2|grad Psi| (total)
  Checks: g->0: mu -> (3/2)y = g/a0 (exact deep-MOND, BTFR amplitude pinned);
          g>>a0: mu -> 1 exponentially;  mu=1 at g=3a0; mild anti-MOND overshoot
          mu_max = 1+e^-3/2 ~ 1.0249 at g=4.5a0 (the (1-y/2) factor goes negative).
  2011 equivalence: L_MOND = (9a0^2/32piG) y^2 e^{-y} [their eq (yAlone)] is the SAME model;
  their sharper published variant [their eq (example2)] reduces to F(y) = y^2 e^{-y-y^2}, i.e.
       mu_ex2(g) = 1 - exp(-y-y^2)(1 - y/2 - y^2),
  same deep-MOND limit, sharper screen.  We scan the family
       mu_alpha(g) = 1 - exp(-y - alpha y^2)(1 - y/2 - alpha y^2),  alpha in [0, 4]
  (alpha=0 the published 2026 f(Z); alpha=1 the published 2011 example2), which keeps the
  pinned deep-MOND normalization and varies only the screening sharpness -- exactly the
  freedom the 2026 paper names ("explore different possibilities for the interpolation
  function f(Z)").

STEP 2: the repo-VERIFIED Desmond+2024 (arXiv:2401.04796) eq (10)-(12) QUMOND quadrupole
  q-integral (10-facet audited in CASSINI_QUADRUPOLE_CONSTRAINT.md; q ~ 0.21-0.27 and
  Q2 ~ 3-5e-26 for RAR-fitting functions, matching Desmond Tab 1 ~2.9e-26 and Hees+2016
  3.5-4.4e-26).  Applied to the DEW nu (algebraic inverse of mu).  Because DEW statics are
  AQUAL (not QUMOND), PART 4 also solves the full nonlinear axisymmetric AQUAL problem
  directly (Picard + Legendre), validated on mu_simple against the QUMOND number.

Cassini 2026 (Park-Hees-Famaey, arXiv:2602.17884): Q2 = (1.6 +/- 1.8)e-27 s^-2;
  2-sigma ceiling 5.2e-27.  g_ext = 2.15e-10 m/s^2 FIXED per pre-registration (V=233 km/s,
  R=8.2 kpc), with 2.0-2.48e-10 (Gaia) as robustness range.
Footings per repo discipline: a0 = 1.2e-10 (DEW's OWN value, their eq (9)/(rhoDM)) PRIMARY;
  a0 = 9.36e-11 (framework pure-Lambda) secondary.
numpy/scipy only; every number reproducible.
"""
import numpy as np
from scipy.optimize import brentq
from scipy import integrate
from scipy.linalg import solve_banded
import glob, os

# ------------------------------------------------------------------ constants
c = 2.99792458e8; G = 6.674e-11; Msun = 1.989e30; kpc = 3.0857e19; Mpc = 3.0857e22
H0 = 67.4e3/Mpc; OmL = 0.685; Lam = 3*OmL*H0**2/c**2
A0_FRAME = c**2*np.sqrt(Lam/(32*np.pi))   # 9.36e-11 framework pure-Lambda footing
A0_DEW   = 1.20e-10                       # DEW's own a0 (their eq (9): "a0 ~= 1.2e-10 m/s^2")
GM_SUN   = G*Msun

Q2_C, Q2_S = 1.6e-27, 1.8e-27             # Cassini 2026 central, 1 sigma
Q2_2SIG    = Q2_C + 2*Q2_S                # 5.2e-27 ceiling
GEXT_FIX   = 2.15e-10                     # pre-registered (V^2/R)
GEXT_GRID  = [2.0e-10, 2.15e-10, 2.32e-10, 2.48e-10]
DATADIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "data", "sparc_data")

# ------------------------------------------------------------------ PART 1: the DEW static limit
def mu_dew(x, alpha=0.0):
    """AQUAL mu of the DEW family.  x = g_total/a0.  alpha=0: the published 2026 f(Z)
    [= 2011 eq (yAlone)]; alpha=1: 2011 eq (example2).  mu = 1 - e^{-y-a y^2}(1-y/2-a y^2)."""
    y = 2.0*np.asarray(x, float)/3.0
    return 1.0 - np.exp(-y - alpha*y*y)*(1.0 - 0.5*y - alpha*y*y)

def gtot_from_gN_dew(yN, alpha=0.0):
    """Invert x mu(x) = yN  (spherical algebraic relation). yN = g_N/a0. Returns x = g/a0."""
    yN = float(yN)
    f = lambda x: x*mu_dew(x, alpha) - yN
    lo = 1e-12
    hi = max(10.0, 2.0*yN + 10.0)
    while f(hi) < 0: hi *= 2.0
    return brentq(f, lo, hi, xtol=1e-15, rtol=1e-13)

def nu_dew_one(yN, alpha=0.0):
    """QUMOND-equivalent nu(yN) = g/g_N from the algebraic inversion of the AQUAL mu."""
    x = gtot_from_gN_dew(yN, alpha)
    return x/yN

# benchmarks (validation + RAR comparison)
def nu_rar_one(y):     return 1.0/(1.0 - np.exp(-np.sqrt(y)))     # McGaugh/RAR IF
def nu_simple_one(y):  return 0.5 + np.sqrt(0.25 + 1.0/y)         # 'simple' nu (mu = x/(1+x))
def mu_simple(x):      return x/(1.0 + x)
def mu_standard(x):    return x/np.sqrt(1.0 + x*x)

# ------------------------------------------------------------------ PART 2: Desmond eq (10)-(12)
def q_milgrom(etilde, nu_one, vmax=80.0):
    """Desmond+2024 eq (12) [Milgrom 2009 QUMOND quadrupole], transcribed verbatim from the
    repo-verified aest_cassini_quadrupole_full.py:
      q = (3/2) Int_0^vmax dv Int_-1^1 dxi (nu(Yarg)-1) [eN(3xi-5xi^3)+v^2(1-3xi^2)] / sqrt(D),
      D = eN^2 + v^4 + 2 eN v^2 xi,  Yarg = sqrt(D);  eN solves eN nu(eN) = etilde."""
    eN = brentq(lambda e: e*nu_one(e) - etilde, 1e-8, max(1e3, 10*etilde), xtol=1e-14, rtol=1e-12)
    def integrand(xi, v):
        D = eN*eN + v**4 + 2.0*eN*v*v*xi
        if D <= 0: return 0.0
        Y = np.sqrt(D)
        return (nu_one(Y) - 1.0)*(eN*(3*xi - 5*xi**3) + v*v*(1 - 3*xi*xi))/Y
    val, _ = integrate.dblquad(integrand, 0.0, vmax, lambda v: -1.0, lambda v: 1.0,
                               epsabs=1e-10, epsrel=1e-8)
    return 1.5*val, eN

def Q2_qumond(a0, nu_one, gext):
    q, eN = q_milgrom(gext/a0, nu_one)
    return -(3.0*a0**1.5)/(2.0*np.sqrt(GM_SUN))*q, q, eN

def boost_eta(a0, nu_one, gext):
    """Desmond eq (14): eta = nu_e (1 + (1/3) dln nu_e/dln eN)."""
    eN = brentq(lambda e: e*nu_one(e) - gext/a0, 1e-8, 1e3, xtol=1e-14, rtol=1e-12)
    nu_e = nu_one(eN); d = 1e-5
    dln = (np.log(nu_one(eN*(1+d))) - np.log(nu_e))/np.log(1+d)
    return nu_e*(1.0 + dln/3.0), nu_e, eN

def sig_over(Q2):
    """SIGNED tension vs the measurement Q2 = (+1.6 +/- 1.8)e-27: |Q2_pred - Q2_meas|/sigma.
    (A negative prediction is *further* from the measured central value, not closer.)"""
    return abs(Q2 - Q2_C)/Q2_S

def passes(Q2):
    return abs(Q2 - Q2_C) <= 2.0*Q2_S

# ------------------------------------------------------------------ PART 4: direct AQUAL solver
def aqual_Q2(mu_fn, etilde, Nr=700, Nth=64, lmax=8, rmin=2e-3, rmax=80.0,
             omega=0.6, tol=1e-11, itmax=400, fitwin=(0.03, 0.25), verbose=False):
    """Solve div[mu(|grad psi|) grad psi] = 4 pi delta^3, grad psi -> etilde zhat at infinity,
    in MOND units (r in r_M = sqrt(GM/a0), psi in a0 r_M, |grad psi| in a0).
    Picard: psi = psi_base + dpsi, psi_base = -1/r + etilde r cos(theta);
      lap dpsi = div[(1-mu(|grad psi|)) grad psi]  (RHS at current iterate).
    Legendre-spectral in theta (Gauss nodes), 2nd-order FD in u = ln r, tridiagonal per l.
    Returns Q2 in units a0^{3/2}/sqrt(GM) (multiply by a0^{1.5}/sqrt(GM_sun) for s^-2),
    defined by  dpsi_(l=2)(r) -> a2 r^2  inside  =>  Q2_dimless = -3 a2   [dPhi = -(Q2/3) r^2 P2].
    """
    u = np.linspace(np.log(rmin), np.log(rmax), Nr); du = u[1]-u[0]; r = np.exp(u)
    xg, wg = np.polynomial.legendre.leggauss(Nth)           # xg = cos(theta)
    sinth = np.sqrt(1.0 - xg**2)
    # Legendre P_l and P_l' at nodes, projection weights
    P  = np.zeros((lmax+1, Nth)); dP = np.zeros((lmax+1, Nth))
    for l in range(lmax+1):
        cl = np.zeros(l+1); cl[-1] = 1.0
        P[l]  = np.polynomial.legendre.legval(xg, cl)
        dP[l] = np.polynomial.legendre.legval(xg, np.polynomial.legendre.legder(cl))
    proj = (2*np.arange(lmax+1)[:, None]+1)/2.0 * P * wg    # f_l = proj @ f(theta)
    R, X = np.meshgrid(r, xg, indexing='ij')                # (Nr, Nth)
    psi_base = -1.0/R + etilde*R*X
    dpsi_l = np.zeros((lmax+1, Nr))                         # spectral anomaly
    Q2_hist = []
    for it in range(itmax):
        # reconstruct dpsi and its gradients spectrally
        dpsi   = (dpsi_l[:, :, None]*P[:, None, :]).sum(0)
        ddpsi_du = np.gradient(dpsi_l, du, axis=1)
        dpsi_dr  = (ddpsi_du[:, :, None]*P[:, None, :]).sum(0)/R
        dpsi_dth = (dpsi_l[:, :, None]*dP[:, None, :]).sum(0)*(-sinth[None, :])  # d/dtheta
        g_r  = 1.0/R**2 + etilde*X + dpsi_dr            # d(psi_base+dpsi)/dr
        g_th = -etilde*sinth[None, :] + dpsi_dth/R      # (1/r) d/dtheta: base gives -e sin(th)
        gmag = np.sqrt(g_r**2 + g_th**2)
        one_minus_mu = 1.0 - mu_fn(gmag)
        s_r, s_th = one_minus_mu*g_r, one_minus_mu*g_th
        # div s = (1/r^2) d(r^2 s_r)/dr + 1/(r sin) d(sin s_th)/dth
        #       = (1/r^2) d(r^2 s_r)/dr - 1/r * [ d(sqrt(1-x^2) s_th)/dx ] / ... use x-form:
        # 1/(r sinth) d_theta(sinth s_th) = -(1/r) d/dx [ sqrt(1-x^2) s_th ]   (x = cos theta)
        r2sr = R**2*s_r
        d_r2sr_du = np.gradient(r2sr, du, axis=0)
        term1 = d_r2sr_du/(R**3)                            # (1/r^2) d/dr = (1/r^3) d/du
        f_x = sinth[None, :]*s_th
        d_fx_dx = np.gradient(f_x, xg, axis=1)
        term2 = -d_fx_dx/R
        src = term1 + term2
        src_l = np.einsum('lt,rt->lr', proj, src)
        # radial solves: psi'' + psi' - l(l+1) psi = r^2 src_l   (in u = ln r)
        new_l = np.zeros_like(dpsi_l)
        for l in range(lmax+1):
            a = np.full(Nr, 1.0/du**2 - 0.5/du)             # sub
            b = np.full(Nr, -2.0/du**2 - l*(l+1))           # diag
            cc = np.full(Nr, 1.0/du**2 + 0.5/du)            # super
            rhs = r**2*src_l[l]
            # inner BC: regular  dpsi/du = l dpsi  ->  one-sided
            b[0] = -1.0/du - l; cc[0] = 1.0/du; rhs[0] = 0.0
            # outer BC: decaying dpsi/du = -(l+1) dpsi
            a[-1] = -1.0/du; b[-1] = 1.0/du + (l+1); rhs[-1] = 0.0
            ab = np.zeros((3, Nr)); ab[0, 1:] = cc[:-1]; ab[1] = b; ab[2, :-1] = a[1:]
            new_l[l] = solve_banded((1, 1), ab, rhs)
        delta = np.max(np.abs(new_l - dpsi_l))
        dpsi_l = (1-omega)*dpsi_l + omega*new_l
        # Q2 from the l=2 interior plateau
        m = (r >= fitwin[0]) & (r <= fitwin[1])
        a2 = np.median(dpsi_l[2][m]/r[m]**2)
        Q2_hist.append(-3.0*a2)
        if verbose and it % 25 == 0:
            print(f"      it {it:3d}  max|d|={delta:.2e}  Q2_dimless={-3*a2:+.4e}")
        if delta < tol and it > 10:
            break
    spread = float(np.std((dpsi_l[2][m]/r[m]**2)))/max(abs(a2), 1e-30)
    return -3.0*a2, it, spread

# ------------------------------------------------------------------ PART 5: SPARC RAR cost
def load_sparc(Yd=0.5, Yb=0.7):
    gN, go = [], []
    for fn in sorted(glob.glob(os.path.join(DATADIR, "*_rotmod.dat"))):
        d = np.genfromtxt(fn)
        if d.ndim != 2 or d.shape[1] < 6: continue
        R = d[:, 0]*kpc; Vo = d[:, 1]*1e3; Vg = d[:, 3]*1e3; Vd = d[:, 4]*1e3; Vb = d[:, 5]*1e3
        V2 = Vg*np.abs(Vg) + Yd*Vd*np.abs(Vd) + Yb*Vb*np.abs(Vb)
        ok = (R > 0) & (Vo > 0) & (V2 > 0)
        gN.append(V2[ok]/R[ok]); go.append(Vo[ok]**2/R[ok])
    return np.concatenate(gN), np.concatenate(go)

def binned_medians(gN, go, nbin=16):
    lN, lo = np.log10(gN), np.log10(go)
    bins = np.linspace(lN.min(), lN.max(), nbin+1)
    ic = 0.5*(bins[1:] + bins[:-1]); med = []
    for i in range(nbin):
        m = (lN >= bins[i]) & (lN < bins[i+1])
        med.append(np.median(lo[m]) if m.sum() >= 5 else np.nan)
    med = np.array(med); ok = ~np.isnan(med)
    return ic[ok], med[ok]

def binned_medians_se(gN, go, nbin=16):
    """Binned medians WITH standard errors (1.4826 MAD / sqrt(N) per bin)."""
    lN, lo = np.log10(gN), np.log10(go)
    bins = np.linspace(lN.min(), lN.max(), nbin+1)
    ic, med, se = [], [], []
    for i in range(nbin):
        m = (lN >= bins[i]) & (lN < bins[i+1])
        if m.sum() >= 5:
            v = lo[m]; md = np.median(v)
            ic.append(0.5*(bins[i]+bins[i+1])); med.append(md)
            se.append(1.4826*np.median(np.abs(v-md))/np.sqrt(m.sum()))
    return np.array(ic), np.array(med), np.array(se)

def rar_rms(nu_one, a0, ic, med):
    mod = np.array([np.log10(nu_one(10**v/a0)*10**v) for v in ic])
    return float(np.sqrt(np.mean((med - mod)**2)))

def rar_chi2(nu_one, a0, ic, med, se):
    mod = np.array([np.log10(nu_one(10**v/a0)*10**v) for v in ic])
    return float(np.sum(((med - mod)/se)**2))/len(ic)

def unbinned_scatter(nu_one, a0, gN, go):
    """UNWEIGHTED dex rms of log10(g_obs) about the model (repo convention)."""
    mod = np.array([np.log10(nu_one(g/a0)*g) for g in gN])
    return float(np.sqrt(np.mean((np.log10(go) - mod)**2)))

# ------------------------------------------------------------------ main
def main():
    np.set_printoptions(precision=4)
    print("#"*100)
    print("# DEW nonlocal-metric MOND (arXiv:2512.10513) vs Cassini 2026 quadrupole -- Door II decision calc")
    print("#"*100)
    print(f"  Cassini 2026: Q2 = (1.6 +/- 1.8)e-27 s^-2; 2-sigma ceiling {Q2_2SIG:.1e}")
    print(f"  g_ext = {GEXT_FIX:.2e} m/s^2 (pre-registered), robustness {GEXT_GRID}")
    print(f"  footings: a0(DEW own) = {A0_DEW:.3e}; a0(framework) = {A0_FRAME:.4e}\n")

    # ---- PART 1: the function
    print("="*100); print("PART 1  the DEW static-limit AQUAL mu (derived; two routes agree)"); print("="*100)
    print("  mu(g) = 1 - exp(-y)(1 - y/2),  y = 2g/(3 a0)   [from f(Z)=Z/2 exp(-sqrt(Z)/3), mu = 1-2f'(Z)]")
    print(f"  {'g/a0':>6} {'mu_DEW':>9} {'mu_simple':>10} {'mu_standard':>12}")
    for x in (0.1, 0.5, 1.0, 1.792, 2.297, 3.0, 5.0, 10.0):
        print(f"  {x:>6.3f} {mu_dew(x):>9.4f} {mu_simple(x):>10.4f} {mu_standard(x):>12.4f}")
    print("  NOTE mu_DEW > 1 for g > 3a0 (anti-MOND overshoot, max 1.0249 at 4.5a0): sign-mixed EFE source.\n")

    # ---- PART 2: validation of the verified q-integral
    print("="*100); print("PART 2  VALIDATION: Desmond eq(10)-(12) on RAR & simple nu (repo-verified anchors)"); print("="*100)
    print(f"  target: q ~ 0.21-0.27, Q2 ~ 3-5e-26 (CASSINI_QUADRUPOLE_CONSTRAINT.md, 10-facet audited;")
    print(f"          Desmond+2024 Tab 1 ~2.9e-26; Hees+2016 3.5-4.4e-26)")
    for lab, nu1 in [("RAR nu", nu_rar_one), ("simple nu", nu_simple_one)]:
        for a0 in (A0_DEW, A0_FRAME):
            Q2, q, eN = Q2_qumond(a0, nu1, GEXT_FIX)
            print(f"  {lab:<10} a0={a0:.3e}: etilde={GEXT_FIX/a0:5.3f} eN={eN:5.3f} "
                  f"q={q:+.4f}  Q2={Q2:+.3e}  ({sig_over(Q2):5.1f} sigma over Cassini)")
    print()

    # ---- PART 3: DEW Q2 (QUMOND-equivalent nu)
    print("="*100); print("PART 3  DEW published f(Z): Q2 via the verified q-integral (QUMOND-equivalent nu)"); print("="*100)
    print(f"  {'a0':>10} {'g_ext':>9} {'etilde':>7} {'eN':>6} {'q':>8} {'Q2 [s^-2]':>12} {'|Q2|/2sig':>10} {'sigma':>7} {'boost':>7}")
    rows = {}
    for a0, flab in [(A0_DEW, "DEW-own"), (A0_FRAME, "framework")]:
        for gext in GEXT_GRID:
            Q2, q, eN = Q2_qumond(a0, lambda y: nu_dew_one(y, 0.0), gext)
            eta, nu_e, _ = boost_eta(a0, lambda y: nu_dew_one(y, 0.0), gext)
            tag = " <-- PRE-REG" if abs(gext - GEXT_FIX) < 1e-13 else ""
            if abs(gext - GEXT_FIX) < 1e-13: rows[flab] = (Q2, q, eN, eta)
            print(f"  {a0:>10.3e} {gext:>9.2e} {gext/a0:>7.3f} {eN:>6.3f} {q:>+8.4f} {Q2:>+12.3e}"
                  f" {abs(Q2)/Q2_2SIG:>9.1f}x {sig_over(Q2):>7.1f} {eta-1:>7.1%}{tag}")
    print()

    # ---- PART 4: direct AQUAL solve (the model's true formulation)
    print("="*100); print("PART 4  direct nonlinear AQUAL solve (Picard+Legendre), validation then DEW"); print("="*100)
    unit = lambda a0: a0**1.5/np.sqrt(GM_SUN)
    print("  validation on mu_simple (vs QUMOND nu_simple above; literature: same ballpark, ~10-30% apart):")
    for a0 in (A0_DEW,):
        et = GEXT_FIX/a0
        Q2d, nit, spr = aqual_Q2(mu_simple, et)
        print(f"    AQUAL mu_simple  a0={a0:.2e}: Q2_dimless={Q2d:+.4f} -> Q2={Q2d*unit(a0):+.3e} s^-2"
              f"  (iters {nit}, plateau spread {spr:.1%})")
        Q2q, _, _ = Q2_qumond(a0, nu_simple_one, GEXT_FIX)
        print(f"    QUMOND same fn ratio AQUAL/QUMOND = {Q2d*unit(a0)/Q2q:.3f}")
    print("  validation on mu_standard:")
    et = GEXT_FIX/A0_DEW
    Q2d, nit, spr = aqual_Q2(mu_standard, et)
    print(f"    AQUAL mu_standard a0={A0_DEW:.2e}: Q2={Q2d*unit(A0_DEW):+.3e} s^-2 (iters {nit}, spread {spr:.1%})")
    print("  DEW published f(Z), both footings:")
    aqual_dew = {}
    for a0, flab in [(A0_DEW, "DEW-own"), (A0_FRAME, "framework")]:
        et = GEXT_FIX/a0
        Q2d, nit, spr = aqual_Q2(lambda g: mu_dew(g, 0.0), et)
        aqual_dew[flab] = Q2d*unit(a0)
        print(f"    AQUAL mu_DEW a0={a0:.3e} (etilde={et:.3f}): Q2_dimless={Q2d:+.4f} -> "
              f"Q2={Q2d*unit(a0):+.3e} s^-2  ({sig_over(Q2d*unit(a0)):.1f} sigma; {abs(Q2d*unit(a0))/Q2_2SIG:.1f}x 2sig)"
              f"  [iters {nit}, spread {spr:.1%}]")
    print()

    # ---- PART 5: the family scan -- can ANY DEW f(Z) thread RAR + Cassini?
    print("="*100); print("PART 5  family scan mu_alpha (alpha=0 published 2026; alpha=1 published 2011 ex2)"); print("="*100)
    print("  Tension convention: SIGNED, sigma = |Q2_pred - 1.6e-27|/1.8e-27 (PASS = within 2 sigma).")
    scans = []
    for Yd, ylab in [(0.5, "Y=0.5 (standard)"), (0.7, "Y=0.7 (framework conv.)")]:
        gNy, goy = load_sparc(Yd=Yd)
        ic, med, se = binned_medians_se(gNy, goy)
        scans.append((Yd, ylab, gNy, goy, ic, med, se))
    print(f"  SPARC: {len(scans[0][2])} points, 175 galaxies; bin SEs ~{np.median(scans[0][6]):.3f} dex")
    print("  benchmark RAR-nu (binned rms / chi2_bin / unbinned dex):")
    for Yd, ylab, gNy, goy, ic, med, se in scans:
        for a0 in (A0_DEW, A0_FRAME):
            print(f"    {ylab:<24} a0={a0:.2e}: rms={rar_rms(nu_rar_one,a0,ic,med):.4f}"
                  f"  chi2/bin={rar_chi2(nu_rar_one,a0,ic,med,se):8.1f}"
                  f"  unbinned={unbinned_scatter(nu_rar_one,a0,gNy,goy):.4f}")
    # AQUAL-based alpha scan at both footings (the model's true formulation)
    print(f"\n  AQUAL alpha scan (direct nonlinear solve; QUMOND proxy in parens), g_ext={GEXT_FIX:.2e}:")
    print(f"  {'alpha':>6} | {'Q2_AQUAL(a0 own)':>17} {'sig':>6} | {'Q2_AQUAL(a0 frm)':>17} {'sig':>6} |"
          f" {'rms Y.5/a0d':>11} {'chi2/bin':>9} | {'rms Y.7/a0f':>11} {'chi2/bin':>9}")
    unit = lambda a0: a0**1.5/np.sqrt(GM_SUN)
    alphas = [0.0, 0.25, 0.4, 0.5, 0.6, 0.75, 1.0, 1.5, 2.0]
    scan_rows = []
    for al in alphas:
        mu1 = lambda g, _a=al: mu_dew(g, _a)
        nu1 = lambda y, _a=al: nu_dew_one(y, _a)
        Qo = aqual_Q2(mu1, GEXT_FIX/A0_DEW)[0]*unit(A0_DEW)
        Qf = aqual_Q2(mu1, GEXT_FIX/A0_FRAME)[0]*unit(A0_FRAME)
        Qo_q = Q2_qumond(A0_DEW, nu1, GEXT_FIX)[0]
        r1 = rar_rms(nu1, A0_DEW, scans[0][4], scans[0][5]); c1 = rar_chi2(nu1, A0_DEW, *scans[0][4:7])
        r2 = rar_rms(nu1, A0_FRAME, scans[1][4], scans[1][5]); c2 = rar_chi2(nu1, A0_FRAME, *scans[1][4:7])
        scan_rows.append((al, Qo, Qf, r1, c1, r2, c2))
        p1 = "P" if passes(Qo) else " "
        p2 = "P" if passes(Qf) else " "
        print(f"  {al:>6.2f} | {Qo:>+12.3e} {p1:1} ({Qo_q:+.1e}) {sig_over(Qo):>5.1f} | {Qf:>+15.3e} {p2:1} {sig_over(Qf):>5.1f} |"
              f" {r1:>11.4f} {c1:>9.1f} | {r2:>11.4f} {c2:>9.1f}")
    print("    [P = passes the 2026 measurement at 2 sigma]")

    # fragility of any passing window vs g_ext (a cancellation-tuned pass must survive 2.0-2.48e-10)
    print(f"\n  g_ext fragility of the passing window (AQUAL, a0 = DEW's own {A0_DEW:.2e}):")
    print(f"  {'alpha':>6} " + " ".join(f"{g*1e10:>9.2f}" for g in GEXT_GRID) + "   (g_ext / 1e-10; entries Q2 [1e-27], * = pass)")
    for al in (0.4, 0.5, 0.6, 0.75, 1.0):
        vals = []
        for gext in GEXT_GRID:
            Q = aqual_Q2(lambda g, _a=al: mu_dew(g, _a), gext/A0_DEW)[0]*unit(A0_DEW)
            vals.append(f"{Q*1e27:>+8.1f}{'*' if passes(Q) else ' '}")
        print(f"  {al:>6.2f} " + " ".join(vals))
    print()

    # ---- PART 6: verdict
    print("="*100); print("PART 6  VERDICT inputs (fork: >=1e-26 robust -> re-close; <=1e-27 RAR-compatible -> leads)"); print("="*100)
    Q2_own = rows.get("DEW-own", (np.nan,)*4)[0]
    Q2_frm = rows.get("framework", (np.nan,)*4)[0]
    print(f"  PUBLISHED 2026 f(Z), g_ext={GEXT_FIX:.2e}:")
    print(f"    QUMOND-equiv:  Q2(own a0) = {Q2_own:+.3e} ({sig_over(Q2_own):.1f} sig)   "
          f"Q2(framework a0) = {Q2_frm:+.3e} ({sig_over(Q2_frm):.1f} sig)")
    if aqual_dew:
        ao, af = aqual_dew.get('DEW-own', np.nan), aqual_dew.get('framework', np.nan)
        print(f"    direct AQUAL:  Q2(own a0) = {ao:+.3e} ({sig_over(ao):.1f} sig)   "
              f"Q2(framework a0) = {af:+.3e} ({sig_over(af):.1f} sig)")
    print(f"    [published 2011 example2 = alpha=1 row of the scan above]")
    print(f"  Cassini 2026:  Q2 = (+1.6 +/- 1.8)e-27; 2-sigma window [-2.0e-27, +5.2e-27]")
    print(f"  RAR cost of sharpening into the passing window: read chi2/bin columns above.")
    print("#"*100)

if __name__ == "__main__":
    main()
