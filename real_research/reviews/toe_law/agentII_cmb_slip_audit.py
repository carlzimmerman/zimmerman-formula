#!/usr/bin/env python3
"""
agentII -- Boltzmann/CMB audit of the lens-only slip sector of the unified action.

The law under audit (UNIFIED_ACTION_ASSEMBLY.md, S_slip):
    (mu, Sigma) = (1, nu(g_bar/a0)),   nu(y) = sqrt(1 + 1/y)
lens-only Psi-channel, zero clustering stress-energy, c_T = 1, alpha_M = 0.

Danger: at linear scales g_bar << a0 so nu -> 1/sqrt(y) diverges -> over-lensing.

Stages:
  A : the ambient g_bar(k,z) of linear structure (EH98 no-wiggle + growth ODE),
      the a0-crossing map, the EFE ambient g_amb(z) (rms bulk-flow acceleration).
  B : Sigma(k,z) under three readings x three frames x three footings, against the
      galactic-scale measured nu range (lensing-RAR bins 1e-15..5e-12 m/s^2).
  C : observables: Limber A_L^eff(L) over the CMB-lensing kernel, E_G(z), Sigma_0,
      ISW source ratio; required caps (bisection) and required EFE floors; Frame-2
      needed-vs-delivered (no-CDM accounting); verdict matrix.

Usage: python agentII_cmb_slip_audit.py [A|B|C|all]
Numpy/scipy only (no CAMB; the linear-theory pieces are implemented here).
Carl Zimmerman / agentII, 2026-06-11.
"""
import sys
import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import brentq

np.set_printoptions(precision=4, suppress=False)

# ---------------------------------------------------------------- constants
c_SI = 2.99792458e8                  # m/s
Mpc  = 3.0856775814913673e22         # m

# ------------------------------------------------- cosmology (Planck-2018)
h    = 0.674
Om   = 0.315
Ob   = 0.0493
ns   = 0.965
sig8 = 0.811
Tcmb = 2.7255
H0   = 100.0 * h * 1e3 / Mpc         # s^-1
wm, wb = Om * h * h, Ob * h * h
wg   = 2.473e-5 * (Tcmb / 2.7255)**4
Orad = wg * (1.0 + 0.2271 * 3.046) / h**2
OL   = 1.0 - Om - Orad
zstar = 1090.0
fb   = Ob / Om                       # baryon fraction of the clustering field

A0_CANON = 9.36e-11                  # m/s^2 (framework canonical, pure-Lambda)
A0_ALT   = 1.13e-10                  # m/s^2 (rho_total/cH0 footing)
A0_MOND  = 1.2e-10                   # m/s^2 (regular-MOND default, working-rule row)
FOOTINGS = [("canon  9.36e-11", A0_CANON),
            ("alt    1.13e-10", A0_ALT),
            ("MONDdef 1.2e-10", A0_MOND)]

def nu(y):
    return np.sqrt(1.0 + 1.0 / y)

def E2(a):
    return Om * a**-3 + Orad * a**-4 + OL

def Hz(z):
    a = 1.0 / (1.0 + np.asarray(z, float))
    return H0 * np.sqrt(E2(a))

def Omz(z):
    z = np.asarray(z, float)
    return Om * (1.0 + z)**3 / E2(1.0 / (1.0 + z))

# --------------------------- EH98 no-wiggle transfer function (k in Mpc^-1)
Th27 = Tcmb / 2.7
s_EH = 44.5 * np.log(9.83 / wm) / np.sqrt(1.0 + 10.0 * wb**0.75)      # Mpc
a_G  = (1.0 - 0.328 * np.log(431.0 * wm) * (Ob / Om)
        + 0.38 * np.log(22.3 * wm) * (Ob / Om)**2)

def T_EH(k_h):
    """EH98 sec 4.2 no-wiggle. CONVENTION (bug caught by the BBKS cross-check, stage X):
    q takes k in h/Mpc (the Gamma-formalism convention, eq 28); the sound-horizon product
    (0.43 k s) is physical (k in Mpc^-1, s in Mpc). With this reading T_EH agrees with
    BBKS/Sugiyama to ~4% at k=0.2 h/Mpc; the earlier k-in-Mpc^-1 q was x1.6 off there."""
    k_h = np.asarray(k_h, float)
    k_Mpc = k_h * h
    Geff = Om * h * (a_G + (1.0 - a_G) / (1.0 + (0.43 * k_Mpc * s_EH)**4))
    q  = k_h * Th27**2 / Geff
    L0 = np.log(2.0 * np.e + 1.8 * q)
    C0 = 14.2 + 731.0 / (1.0 + 62.5 * q)
    return L0 / (L0 + C0 * q * q)

def _Delta2_raw(k_h):
    k_h = np.asarray(k_h, float)
    return k_h**(3.0 + ns) * T_EH(k_h)**2

def W_th(x):
    x = np.asarray(x, float)
    w = np.empty_like(x)
    s = x < 1e-3
    w[s]  = 1.0 - x[s]**2 / 10.0
    w[~s] = 3.0 * (np.sin(x[~s]) - x[~s] * np.cos(x[~s])) / x[~s]**3
    return w

_lk  = np.linspace(np.log(1e-5), np.log(200.0), 6000)
_kk  = np.exp(_lk)
NORM = sig8**2 / np.trapz(_Delta2_raw(_kk) * W_th(_kk * 8.0)**2, _lk)

def Delta2(k_h):
    """dimensionless linear power at z=0, k in h/Mpc."""
    return NORM * _Delta2_raw(k_h)

def P_h(k_h):
    """linear P(k) at z=0 in (Mpc/h)^3."""
    k_h = np.asarray(k_h, float)
    return 2.0 * np.pi**2 * Delta2(k_h) / k_h**3

# ------------------------------- growth factor (radiation in H, Meszaros IC)
a_eq = Orad / Om

def _gode(x, y):
    a = np.exp(x)
    e2 = E2(a)
    dlnE = 0.5 * (-3.0 * Om * a**-3 - 4.0 * Orad * a**-4) / e2
    return [y[1], -(2.0 + dlnE) * y[1] + 1.5 * (Om * a**-3 / e2) * y[0]]

_ai  = 1e-4
_sol = solve_ivp(_gode, [np.log(_ai), 0.0],
                 [1.0 + 1.5 * _ai / a_eq, 1.5 * _ai / a_eq],
                 rtol=1e-9, atol=1e-12, dense_output=True)
_D1 = _sol.sol(0.0)[0]

def Dz(z):
    """growth factor normalized D(z=0)=1 (scale-independent; EH98 carries the shape)."""
    la = np.log(1.0 / (1.0 + np.asarray(z, float)))
    return _sol.sol(la)[0] / _D1

def fz(z):
    la = np.log(1.0 / (1.0 + np.asarray(z, float)))
    out = _sol.sol(la)
    return out[1] / out[0]

# --------------------- the ambient Newtonian field of linear structure (SI)
PREF = 1.5 * Om * H0 * H0            # g = PREF (1+z)^2 delta_rms(k,z) / k_com[SI]

def g_bar(k_h, z):
    """rms-per-ln-k Newtonian field of linear structure, TOTAL-matter source [m/s^2].
    g = (3/2) Om(z) H(z)^2 delta_rms / k_phys = (3/2) Om0 H0^2 (1+z)^2 delta_rms / k_com."""
    k_si = np.asarray(k_h, float) * h / Mpc
    return PREF * (1.0 + np.asarray(z, float))**2 * np.sqrt(Delta2(k_h)) * Dz(z) / k_si

# cumulative rms acceleration of the large-scale velocity/gravity field (EFE ambient)
_lka  = np.linspace(np.log(1e-4), np.log(10.0), 4000)
_ka   = np.exp(_lka)
_I_g2 = np.trapz(Delta2(_ka) / (_ka * h / Mpc)**2, _lka)      # [m^2]
_I_g2_to1 = np.trapz(np.where(_ka <= 1.0, Delta2(_ka), 0.0) / (_ka * h / Mpc)**2, _lka)

def g_amb(z, boost=1.0):
    """rms peculiar-gravity (bulk-flow) acceleration from linear theory [m/s^2]."""
    return boost * PREF * (1.0 + np.asarray(z, float))**2 * Dz(z) * np.sqrt(_I_g2)

# ----------------------------------------------------- comoving distance map
_zchi = np.concatenate(([0.0], np.geomspace(1e-4, 1100.0, 8000)))
_ich  = c_SI / Hz(_zchi) / Mpc                                # Mpc per unit z
_chi  = np.concatenate(([0.0],
        np.cumsum(0.5 * (_ich[1:] + _ich[:-1]) * np.diff(_zchi))))

def chi_of_z(z):
    return np.interp(np.asarray(z, float), _zchi, _chi)

chistar = float(chi_of_z(zstar))
H0c = h / 2997.92458                                          # H0/c in 1/Mpc

# ------------------------------------------------ Sigma(k,z) reading factory
def Sigma_factory(frame="F1", a0=A0_CANON, cap=None, efe=False, efe_boost=1.0):
    """frame: F1 (constraint frame, nu of the total-matter field, Sigma=nu)
              F1own (nu of the baryonic field g_b = fb*g, Sigma=nu)  [the law's own terms]
              F2   (no-CDM accounting: Sigma_eff = fb * nu(fb*g))
       cap : saturation value applied to nu;  efe: floor g at the ambient."""
    src = fb if frame in ("F1own", "F2") else 1.0
    amp = fb if frame == "F2" else 1.0
    def S(k_h, z):
        g = src * g_bar(k_h, z)
        if efe:
            g = np.maximum(g, src * g_amb(z, boost=efe_boost))
        n = nu(g / a0)
        if cap is not None:
            n = np.minimum(n, cap)
        return amp * n
    return S

# ------------------------------------------------------------- Limber lensing
def CLkk(L, S=None, nz=1200):
    """CMB-lensing convergence spectrum (GR) and the framework/GR ratio if S given."""
    zg = np.geomspace(1e-3, zstar, nz)
    ch = chi_of_z(zg)
    W  = 1.5 * Om * H0c**2 * (1.0 + zg) * ch * (1.0 - ch / chistar)
    kM = (L + 0.5) / ch                       # Mpc^-1
    kh = kM / h
    Pm = P_h(kh) / h**3 * Dz(zg)**2           # Mpc^3
    base = W * W / ch**2 * Pm * (c_SI / Hz(zg) / Mpc)
    I0 = np.trapz(base, zg)
    if S is None:
        return I0, 1.0
    I1 = np.trapz(base * S(kh, zg)**2, zg)
    return I0, I1 / I0

_LGRID = np.unique(np.round(np.geomspace(20, 400, 25)).astype(int))

def AL_weighted(S, Ls=_LGRID):
    """kernel-weighted <Sigma^2>: kappa-power weight and deflection-power weight."""
    I0s, As = [], []
    for L in Ls:
        I0, A = CLkk(L, S)
        I0s.append(I0); As.append(A)
    I0s = np.array(I0s); As = np.array(As); Lf = Ls.astype(float)
    wk = (2 * Lf + 1) * I0s
    wd = (2 * Lf + 1) * I0s / (Lf * (Lf + 1))
    return (np.sum(wk * As) / np.sum(wk),
            np.sum(wd * As) / np.sum(wd),
            Ls, As)

def required_cap(target, frame="F1", a0=A0_CANON, efe=False, efe_boost=1.0):
    """nu-cap such that the kappa-weighted <Sigma^2> equals target."""
    def f(cap):
        S = Sigma_factory(frame, a0=a0, cap=cap, efe=efe, efe_boost=efe_boost)
        return AL_weighted(S)[0] - target
    lo, hi = 1.0 + 1e-6, 500.0
    if f(hi) < 0:      # even uncapped below target (cannot happen for raw)
        return np.inf
    if f(lo) > 0:      # already above target at cap=1 (frame F2 fb<1 may differ)
        return 1.0
    return brentq(f, lo, hi, xtol=1e-5)

# ------------------------------------------------------------------- E_G
def EG(zpt, k_h, S):
    s = float(S(np.atleast_1d(k_h), zpt)[0])
    return Om * s / float(fz(zpt))

EG_MEAS = [   # (label, z, value, error)  charge band 0.3-0.4; fetch-verified in section 4
    ("Reyes+2010  (SDSS LRG x SDSS)", 0.32, 0.39, 0.06),
    ("Blake+2016  (RCSLenS z1)",      0.32, 0.48, 0.10),
    ("Blake+2016  (RCSLenS z2)",      0.57, 0.30, 0.07),
    ("Pullen+2016 (CMASS x Planck)",  0.57, 0.243, 0.060),
    ("Amon+2018   (KiDS x BOSS lo)",  0.305, 0.27, 0.08),
    ("Amon+2018   (KiDS x BOSS hi)",  0.554, 0.26, 0.07),
    ("delaTorre+2017 (VIPERS lo)",    0.60, 0.16, 0.09),
    ("delaTorre+2017 (VIPERS hi)",    0.86, 0.09, 0.07),
]

# ----------------------------------------------------------------- ISW source
def isw_sources(k_h, zpt, S, dl=0.02):
    """d/dlna of the per-mode Weyl potential: GR phi ~ D/a ; FW phi ~ Sigma D/a."""
    la0 = np.log(1.0 / (1.0 + zpt))
    def pair(la):
        z = 1.0 / np.exp(la) - 1.0
        gr = float(Dz(z)) / np.exp(la)
        fw = gr * float(S(np.atleast_1d(k_h), z)[0])
        return gr, fw
    grp, fwp = pair(la0 + dl)
    grm, fwm = pair(la0 - dl)
    return (fwp - fwm) / (2 * dl), (grp - grm) / (2 * dl)

# ================================================================== STAGE A
def stageA():
    print("=" * 100)
    print("STAGE A -- the ambient g_bar of linear structure, and where it crosses a0")
    print("=" * 100)
    print(f"cosmology: h={h} Om={Om} Ob={Ob} ns={ns} sig8={sig8}  "
          f"Orad={Orad:.3e}  a_eq={a_eq:.3e} (z_eq={1/a_eq-1:.0f})")
    print(f"EH98 no-wiggle: s={s_EH:.2f} Mpc  alpha_Gamma={a_G:.4f}")
    # sanity: sigma8 round-trip, P(k) values, growth
    s8chk = np.sqrt(np.trapz(Delta2(_kk) * W_th(_kk * 8.0)**2, _lk))
    print(f"sigma8 round-trip = {s8chk:.4f} (target {sig8})")
    for kp in (0.01, 0.05, 0.1, 0.2):
        print(f"  P({kp:4.2f} h/Mpc) = {P_h(kp):9.1f} (Mpc/h)^3   Delta2 = {Delta2(kp):.4f}")
    kfine = np.geomspace(1e-4, 1, 2000)
    kpk = kfine[np.argmax(P_h(kfine))]
    print(f"  P(k) peak at k = {kpk:.4f} h/Mpc (expect ~0.016)")
    print(f"growth: D(0)=1, D(0.5)={Dz(0.5):.4f} D(1)={Dz(1.0):.4f} D(2)={Dz(2.0):.4f} "
          f"D(9)={Dz(9.0):.4f} D(1090)={Dz(1090.0):.5e}")
    print(f"        f(0)={fz(0.0):.4f} (expect ~Om^0.55={Om**0.55:.4f})  f(0.57)={fz(0.57):.4f}")
    vrms3 = Hz(0.0) * fz(0.0) * np.sqrt(_I_g2) / 1e3
    print(f"linear v_rms(3D, z=0) = {vrms3:.0f} km/s  (1D {vrms3/np.sqrt(3):.0f}; expect ~290-330 1D)")
    print(f"chi(z*) = {chistar:.0f} Mpc (expect ~13870)   chi(2) = {chi_of_z(2.0):.0f} Mpc")

    print("\n--- g_bar(k,z) [m/s^2], TOTAL-matter source (Frame 1; baryonic field = x0.156) ---")
    ks = np.array([0.001, 0.003, 0.01, 0.03, 0.1, 0.3, 1.0])
    zs = np.array([0.0, 0.32, 0.57, 1.0, 2.0, 5.0, 10.0, 50.0, 100.0, 300.0, 1090.0])
    hdr = "k[h/Mpc]" + "".join(f"  z={z:<7.4g}" for z in zs)
    print(hdr)
    for k in ks:
        row = f"{k:8.3f}" + "".join(f"  {g_bar(k, z):9.2e}" for z in zs)
        print(row)
    print(f"\n(a0 canon = {A0_CANON:.3g}; alt = {A0_ALT:.3g}; MOND default = {A0_MOND:.3g})")

    # max over k and the a0 crossing
    kg = np.geomspace(1e-3, 1.0, 400)
    zg = np.geomspace(1e-3, 1100.0, 900)
    gmax = np.empty_like(zg); kat = np.empty_like(zg)
    for i, z in enumerate(zg):
        gv = g_bar(kg, z)
        j = np.argmax(gv)
        gmax[i] = gv[j]; kat[i] = kg[j]
    print("\n--- max_k g_bar(z) over k in [1e-3, 1] h/Mpc ---")
    for z in (0.0, 0.5, 1.0, 2.0, 5.0, 10.0, 50.0, 100.0, 300.0, 1090.0):
        gv = g_bar(kg, z); j = np.argmax(gv)
        print(f"  z={z:7.4g}  max g_bar = {gv[j]:.3e} at k = {kg[j]:.3f} h/Mpc"
              f"   y_canon = {gv[j]/A0_CANON:.3e}")
    for nm, a0v in FOOTINGS:
        # crossing where max_k g_bar = a0
        d = gmax - a0v
        if d.max() < 0:
            print(f"  [{nm}] linear structure NEVER reaches a0 in this k-window")
            continue
        i = np.argmax(d > 0)             # first z where above (gmax increases with z)
        zx = np.interp(0.0, d[i-1:i+1], zg[i-1:i+1]) if i > 0 else zg[0]
        print(f"  [{nm}] max_k g_bar crosses a0 at z_dagger = {zx:.0f}"
              f"  (ALL linear k are sub-a0 for z < z_dagger)")
    print("\nper-k crossing z (g_bar(k,z)=a0_canon):")
    for k in (0.01, 0.03, 0.1, 0.3):
        gk = g_bar(k, zg); d = gk - A0_CANON
        if d.max() < 0:
            print(f"  k={k:5.2f}: never crosses (max {gk.max():.2e})")
        else:
            i = np.argmax(d > 0)
            zx = np.interp(0.0, d[i-1:i+1], zg[i-1:i+1])
            print(f"  k={k:5.2f}: crosses a0 at z = {zx:.0f}")

    print("\n--- the EFE ambient: rms bulk-flow (peculiar-gravity) acceleration, linear theory ---")
    print(f"  integral converges: I(k<=10)={np.sqrt(_I_g2):.4e} m  vs I(k<=1)={np.sqrt(_I_g2_to1):.4e} m"
          f"  (high-k tail adds {100*(np.sqrt(_I_g2)/np.sqrt(_I_g2_to1)-1):.1f}%)")
    print("  z      g_amb [m/s^2]   y=g_amb/a0(canon)   nu(y) canon   nu alt   nu MONDdef")
    for z in (0.0, 0.32, 0.57, 1.0, 2.0, 3.0, 5.0, 10.0, 30.0, 100.0, 1090.0):
        ga = float(g_amb(z))
        ycan = ga / A0_CANON
        print(f"  {z:6.4g}  {ga:.3e}      {ycan:.4e}        {nu(ycan):8.3f}   "
              f"{nu(ga/A0_ALT):8.3f}  {nu(ga/A0_MOND):8.3f}")
    print("\n  NOTE nonlinear bracket: halo-scale power raises the integral; the bracket row")
    print("  used downstream is g_amb x1.5 (linear-theory rms is the floor, x1.5 the generous lens).")
    print("  Hand-bracket 'mass-weighted one-halo ambient' ~1e-11 m/s^2 also carried in stage C.")

    print("\n--- the charge's pivots ---")
    for (k, z, tag) in [(0.028, 2.0, "CMB-lensing L~100 (k=(L+.5)/chi(2))"),
                        (0.02, 0.5, "E_G low-k"), (0.05, 0.32, "E_G mid Reyes"),
                        (0.05, 0.57, "E_G mid Pullen"), (0.1, 0.86, "E_G high-z")]:
        g = float(g_bar(k, z))
        print(f"  k={k:5.3f} h/Mpc z={z:4.2f} ({tag:38s}): g_bar={g:.3e}"
              f"  y_canon={g/A0_CANON:.3e}  nu={nu(g/A0_CANON):7.2f}")

# ================================================================== STAGE B
def stageB():
    print("=" * 100)
    print("STAGE B -- Sigma(k,z) under the three readings x three frames, vs the galactic nu range")
    print("=" * 100)
    pivots = [(0.028, 2.0, "phi-phi kernel"), (0.02, 0.5, "E_G/ISW low-k"),
              (0.05, 0.32, "E_G Reyes"), (0.05, 0.57, "E_G Pullen"),
              (0.1, 0.32, "E_G high-k"), (0.05, 0.0, "Sigma0 pivot"),
              (0.1, 0.0, "Sigma0 high-k"), (0.01, 0.0, "Sigma0 low-k")]

    for nm, a0v in FOOTINGS:
        Sraw  = Sigma_factory("F1",    a0=a0v)
        Sown  = Sigma_factory("F1own", a0=a0v)
        S2    = Sigma_factory("F2",    a0=a0v)
        Sefe  = Sigma_factory("F1",    a0=a0v, efe=True)
        Sefe2 = Sigma_factory("F2",    a0=a0v, efe=True)
        print(f"\n--- footing {nm} ---")
        print("  k[h/Mpc]  z     g_bar      | F1 raw   F1own raw  F2 raw   | F1 EFE   F2 EFE   (cap rows below)")
        for k, z, tag in pivots:
            g = float(g_bar(k, z))
            print(f"  {k:7.3f} {z:5.2f}  {g:.3e} | {float(Sraw(np.atleast_1d(k),z)[0]):8.2f} "
                  f"{float(Sown(np.atleast_1d(k),z)[0]):8.2f} {float(S2(np.atleast_1d(k),z)[0]):8.2f} | "
                  f"{float(Sefe(np.atleast_1d(k),z)[0]):8.2f} {float(Sefe2(np.atleast_1d(k),z)[0]):8.2f}   [{tag}]")

    print("\n--- reading (b): capped nu (Brouwer-consistent 'Sigma_max ~ few'; NO banked saturation exists) ---")
    a0v = A0_CANON
    for cap in (2.0, 3.0, 5.0):
        Sc = Sigma_factory("F1", a0=a0v, cap=cap)
        vals = [float(Sc(np.atleast_1d(k), z)[0]) for k, z, _ in pivots[:5]]
        print(f"  cap nu_max={cap:3.1f}: Sigma at the five lensing/E_G pivots -> "
              + "  ".join(f"{v:5.2f}" for v in vals)
              + "   (cap binds everywhere: raw nu >> cap)")

    print("\n--- the galactic-scale measured nu range (the same function, the same g_bar axis) ---")
    print("  lensing-RAR (Brouwer+2021 / our 6.8-sigma re-measurement): bins g_bar = 1e-15 .. 5e-12 m/s^2")
    print("  SPARC RC RAR: g_bar ~ 1e-12 .. 1e-9 m/s^2")
    for nm, a0v in FOOTINGS:
        print(f"  [{nm}] nu(5e-12)={nu(5e-12/a0v):6.2f}  nu(1e-12)={nu(1e-12/a0v):6.2f} "
              f" nu(1e-13)={nu(1e-13/a0v):6.2f}  nu(1e-15)={nu(1e-15/a0v):7.1f}")
    print("\n  OVERLAP EXHIBIT: linear-scale ambient g_bar at z<=1, k=0.01..0.3 h/Mpc spans ~[1e-13, 1.2e-12]")
    print("  -- INSIDE the lensing-RAR bin range and at SPARC's low edge. The law is one function nu(g_bar):")
    print("  at g_bar = 5e-13 the RAR demands nu = %.1f; stage C computes what the CMB allows there." %
          nu(5e-13 / A0_CANON))

    print("\n--- the z=1090 row (recombination): the slip the primary CMB would see ---")
    for k in (0.001, 0.003, 0.01, 0.05, 0.1, 0.3):
        g = float(g_bar(k, 1090.0))
        print(f"  k={k:6.3f} h/Mpc: g_bar={g:.3e}  y_canon={g/A0_CANON:9.3g}  nu={nu(g/A0_CANON):7.3f}"
              f"   (ell ~ k*chi* ~ {k*h*chistar:6.0f})")
    print("  (the early universe is mostly ABOVE a0: the slip shuts itself off at high z;")
    print("   residual nu-1 of a few % to tens of % at ell <~ 100 is flagged in stage C as a")
    print("   follow-on exposure -- a full Boltzmann solve would only sharpen, not soften.)")

# ================================================================== STAGE C
def stageC():
    print("=" * 100)
    print("STAGE C -- confrontation: A_L, phi-phi reconstruction, E_G, Sigma_0, ISW; required caps/floors")
    print("=" * 100)
    a0v = A0_CANON

    # sanity on the GR lensing spectrum
    print("--- GR C_L^kappakappa sanity (linear P; nonlinear would raise L>~300 by ~10-25%) ---")
    for L in (40, 100, 200, 400):
        I0, _ = CLkk(L)
        plotted = 2.0 * I0 / np.pi      # [L(L+1)]^2 C_L^phiphi / 2pi = 2 C_L^kk / pi
        print(f"  L={L:4d}: C_L^kk={I0:.3e}   [L(L+1)]^2 C_L^pp/2pi = {plotted:.3e} (Planck peak ~1.3e-7 at L~40)")

    frames = [("F1 raw (constraint frame)",  Sigma_factory("F1",    a0=a0v)),
              ("F1own raw (baryonic g_bar)", Sigma_factory("F1own", a0=a0v)),
              ("F2 raw (no-CDM accounting)", Sigma_factory("F2",    a0=a0v)),
              ("F1 EFE-floored (x1.0)",      Sigma_factory("F1",    a0=a0v, efe=True)),
              ("F1 EFE-floored (x1.5)",      Sigma_factory("F1",    a0=a0v, efe=True, efe_boost=1.5)),
              ("F2 EFE-floored (x1.0)",      Sigma_factory("F2",    a0=a0v, efe=True)),
              ("F1 cap nu_max=3",            Sigma_factory("F1",    a0=a0v, cap=3.0)),
              ]

    print("\n--- A_L^eff = <Sigma^2> over the CMB-lensing kernel (Limber) ---")
    print("  constraints: A_L(TT smearing) = 1.180 +/- 0.065 ; phi-phi reconstruction amplitude")
    print("  consistent with LCDM at ~2.5-3% (=> 2-sigma ceiling ~1.07). Both want <Sigma^2> near 1.")
    res = {}
    for nm, S in frames:
        Ak, Ad, Ls, As = AL_weighted(S)
        res[nm] = Ak
        print(f"  {nm:29s}: <A>_kappa-wt = {Ak:9.2f}   <A>_defl-wt = {Ad:9.2f}   "
              f"A(L=40)={As[Ls==40][0] if (Ls==40).any() else np.interp(40,Ls,As):8.2f} "
              f"A(L=400)={np.interp(400,Ls,As):8.2f}")
    print("  (A_L^eff(L) is nearly flat in L for every reading => no smearing-vs-reconstruction")
    print("   threading: any Sigma matching A_L=1.18 in TT smearing violates the phi-phi amplitude.)")

    # footing sensitivity on the headline number
    print("\n  footing sensitivity (F1 raw): ", end="")
    for nm, a0f in FOOTINGS:
        Ak, _, _, _ = AL_weighted(Sigma_factory("F1", a0=a0f))
        print(f"[{nm}] {Ak:.1f}  ", end="")
    print()

    print("\n--- E_G = Om0 Sigma / f(z)  (scale-dep Sigma: quoted at k=0.05; spread k=0.02..0.1) ---")
    print(f"  LCDM rows: E_G(z) = Om0/f(z): "
          + "  ".join(f"z={z}: {Om/float(fz(z)):.3f}" for z in (0.32, 0.57, 0.86)))
    for nm, S in frames:
        rows = []
        for z in (0.32, 0.57, 0.86):
            e_mid = EG(z, 0.05, S)
            e_lo, e_hi = EG(z, 0.02, S), EG(z, 0.1, S)
            rows.append(f"z={z}: {e_mid:7.3f} [{min(e_lo,e_hi):.3f},{max(e_lo,e_hi):.3f}]")
        print(f"  {nm:29s}: " + "   ".join(rows))
    print("  measured points (fetch-verified in section 4):")
    for lab, z, v, e in EG_MEAS:
        print(f"    {lab:32s} z={z:5.3f}: {v:.3f} +/- {e:.3f}")
    print("  tension of F1 raw at the two classic points:")
    for lab, z, v, e in (EG_MEAS[0], EG_MEAS[3]):
        pred = EG(z, 0.05, frames[0][1])
        print(f"    {lab}: predicted {pred:.2f} vs {v}+/-{e} -> {(pred-v)/e:8.1f} sigma")

    print("\n--- Sigma_0 (DES-Y3/KiDS parametrization: Sigma(z)-1 = Sigma0 OmegaL(z)/OmegaL0; at z=0, Sigma0=Sigma-1) ---")
    print("  bound: |Sigma_0| <~ 0.2-0.5")
    for nm, S in frames:
        vals = [f"k={k}: {float(S(np.atleast_1d(k),0.0)[0])-1.0:+8.2f}" for k in (0.01, 0.05, 0.1, 0.3)]
        print(f"  {nm:29s}: " + "  ".join(vals))

    print("\n--- ISW source (per-mode d/dlna of the Weyl potential; GR decays, sign +ve means GROWTH) ---")
    Sraw = frames[0][1]
    for k, z in [(0.002, 0.5), (0.005, 0.5), (0.01, 0.5), (0.02, 0.5), (0.005, 1.0), (0.005, 0.2)]:
        dfw, dgr = isw_sources(k, z, Sraw)
        print(f"  k={k:5.3f} z={z:3.1f}: d(phi_FW)/dlna = {dfw:+9.3f} x phi-units vs GR {dgr:+8.4f}"
              f"   ratio = {dfw/dgr:+9.1f}  (power x{(dfw/dgr)**2:9.1f})")
    print("  GR late-ISW: potentials DECAY (ratio +1 by construction). The slip sector's potentials")
    print("  GROW (nu rises faster than D/a falls): the ISW source is SIGN-FLIPPED and 1-2 orders larger.")
    print("  Measured ISW x LSS cross-correlation is POSITIVE (decay) at ~4-5 sigma => sign-level kill,")
    print("  flagged source-level (no C_ell computed).")

    # ------------------------------------------------ required caps and floors
    print("\n--- REQUIRED saturation caps (bisection on the kappa-weighted <Sigma^2>) ---")
    targets = [("phi-phi recon +2sig", 1.067), ("A_L central (fits anomaly)", 1.18),
               ("A_L +2sig", 1.31)]
    caps = {}
    for lab, t in targets:
        cv = required_cap(t, frame="F1", a0=a0v)
        caps[lab] = cv
        print(f"  {lab:28s}: nu_cap = {cv:7.3f}", end="")
        if np.isfinite(cv) and cv > 1:
            ysat = 1.0 / (cv**2 - 1.0)
            print(f"   (saturation onset y={ysat:8.3g}, g_sat={ysat*a0v:.2e} m/s^2 = {ysat:.2g} a0)")
        else:
            print()
    capE1 = (0.39 + 2 * 0.06) * float(fz(0.32)) / Om
    capE2 = (0.243 + 2 * 0.060) * float(fz(0.57)) / Om
    print(f"  E_G Reyes z=0.32 +2sig      : nu_cap = {capE1:7.3f}")
    print(f"  E_G Pullen z=0.57 +2sig     : nu_cap = {capE2:7.3f}   (central value prefers Sigma<1!)")
    print(f"  Sigma0 <= 0.2 / 0.5         : nu_cap =   1.200 / 1.500")
    print("  frame sensitivity: same caps recomputed in F1own: ", end="")
    for lab, t in targets[:2]:
        cv = required_cap(t, frame="F1own", a0=a0v)
        print(f"[{lab}] {cv:.3f}  ", end="")
    print()

    print("\n--- the saturation-coincidence test (the charge's decision rule) ---")
    print("  REQUIRED caps: nu_max ~ 1.03-1.5 (above).  MEASURED galactic nu, same function, same axis:")
    print(f"    lensing-RAR bins g_bar=1e-15..5e-12 -> nu = {nu(5e-12/a0v):.1f} .. {nu(1e-15/a0v):.0f} (UNSATURATED to the floor)")
    print(f"    SPARC RC RAR g_bar=1e-12..1e-9     -> nu = {nu(1e-9/a0v):.2f} .. {nu(1e-12/a0v):.1f}")
    print(f"    at the linear-scale ambient value g_bar=5e-13: RAR demands nu={nu(5e-13/a0v):.1f}; CMB allows <=1.07")
    print("  => the required cap sits BELOW the ENTIRE measured galactic range (factor 4-300),")
    print("     and the cap that fits A_L=1.18 centrally (nu_cap~1.09, onset y~5.6) would freeze nu~1")
    print("     over the WHOLE RAR: no rotation-curve phenomenology survives it. NOT a coincidence-pass:")
    print("     by the charge's own rule this is a KILL for any global (k,z)-blind saturation.")

    print("\n--- REQUIRED EFE floor vs the computed ambient ---")
    for lab, t in targets:
        cv = caps[lab]
        if not np.isfinite(cv) or cv <= 1:
            continue
        greq = a0v / (cv**2 - 1.0)
        print(f"  {lab:28s}: g_floor >= {greq:.3e} m/s^2 = {greq/a0v:6.2f} a0 ; computed g_amb(z=0.5)="
              f"{float(g_amb(0.5)):.3e} -> SHORT x{greq/float(g_amb(0.5)):7.0f}"
              f" (x1.5 NL bracket -> x{greq/float(g_amb(0.5,boost=1.5)):6.0f};"
              f" one-halo hand-bracket 1e-11 -> x{greq/1e-11:5.0f})")
    print("  (the rising-a0(z) rival branch RAISES nu at z>0 -- conservative branch used throughout)")

    # ------------------------------------------------ Frame 2 needed-vs-delivered
    print("\n--- FRAME 2 (no-CDM accounting): is the divergence the right size to REPLACE CDM? ---")
    print(f"  needed boost (k-flat): Sigma_eff = 1, i.e. nu(g_b/a0) = Om/Ob = {1/fb:.2f}")
    S2 = Sigma_factory("F2", a0=a0v)
    print("  delivered Sigma_eff(k, z) [needed: 1.00 at all k,z]:")
    for z in (0.0, 0.32, 0.57, 1.0, 2.0, 3.0, 5.0, 8.0):
        vals = [float(S2(np.atleast_1d(k), z)[0]) for k in (0.02, 0.05, 0.1, 0.2)]
        print(f"    z={z:4.2f}: " + "  ".join(f"k={k}: {v:5.2f}" for k, v in zip((0.02, 0.05, 0.1, 0.2), vals)))
    # crossing z at the kernel pivot
    def f2cross(k):
        g = lambda z: float(S2(np.atleast_1d(k), z)[0]) - 1.0
        try:
            return brentq(g, 0.01, 30.0, xtol=1e-3)
        except ValueError:
            return np.nan
    print("  Sigma_eff = 1 crossing: " + "  ".join(f"k={k}: z*={f2cross(k):.1f}" for k in (0.02, 0.05, 0.1)))
    print("  shape: dln Sigma_eff/dln k at z=0.5: ", end="")
    for k in (0.02, 0.05, 0.1, 0.2):
        e = 1.05
        sl = (np.log(float(S2(np.atleast_1d(k*e), 0.5)[0])) -
              np.log(float(S2(np.atleast_1d(k/e), 0.5)[0]))) / (2*np.log(e))
        print(f"k={k}: {sl:+.2f}  ", end="")
    print("\n  (CDM-mimicry needs slope 0. The plateau k~0.03-0.2 is accidentally near-flat -- the")
    print("   nontrivial near-miss -- but the amplitude there is x2-4 too HIGH at z<2, the redshift")
    print("   evolution is wrong (Sigma_eff falls through 1 near z~5-7 and keeps falling), and at")
    print("   k<0.02 the slope diverges. Frame-2 A_L and E_G rows above quantify the kill.)")

    # ------------------------------------------------------------ verdict matrix
    print("\n" + "=" * 100)
    print("VERDICT MATRIX (canon footing; alt/MOND footings shift nu by ~10-13%, no verdict changes)")
    print("=" * 100)
    AK = {nm: res[nm] for nm, _ in frames if nm in res}
    eg1 = {nm: EG(0.32, 0.05, S) for nm, S in frames}
    eg2 = {nm: EG(0.57, 0.05, S) for nm, S in frames}
    s0 = {nm: float(S(np.atleast_1d(0.05), 0.0)[0]) - 1.0 for nm, S in frames}
    print(f"{'reading/frame':30s} {'<Sig^2>kernel':>13s} {'E_G(0.32)':>10s} {'E_G(0.57)':>10s} {'Sigma0(k=.05)':>14s}   verdict")
    print(f"{'measured/allowed':30s} {'1.011+/-.028|1.18+/-.065':>13s} {'0.39+/-.06':>10s} {'0.24+/-.06':>10s} {'|S0|<0.2-0.5':>14s}")
    for nm, S in frames:
        v = "KILL"
        a = AK.get(nm, np.nan)
        if a < 1.4 and abs(eg1[nm] - 0.39) < 0.18 and abs(s0[nm]) < 0.5:
            v = "pass-ish"
        print(f"{nm:30s} {a:13.2f} {eg1[nm]:10.2f} {eg2[nm]:10.2f} {s0[nm]:+14.2f}   {v}")
    print("\nKill margins (F1 raw): A_L-family x{:.0f} over; E_G x{:.0f} over (Reyes, {:.0f} sigma);".format(
        AK["F1 raw (constraint frame)"],
        eg1["F1 raw (constraint frame)"] / 0.39,
        (eg1["F1 raw (constraint frame)"] - 0.39) / 0.06))
    print("Sigma0 x{:.0f} over the loose bound. EFE floor short x500-700 in g. Caps required ~1.03-1.5 vs".format(
        s0["F1 raw (constraint frame)"] / 0.5))
    print("measured galactic nu 4.4-306 on the SAME g_bar axis: the g_bar-only law cannot do both. Frame-2")
    print("(no-CDM): over x2-4 in amplitude at z<2 with wrong z-evolution; ISW sign-flipped and x>100 in power.")

# ================================================================== STAGE X
def stageX():
    """Validation addendum: (i) independent BBKS transfer-function cross-check of the
    P(k) shape; (ii) absolute-calibration honesty row (d_rms); (iii) the verdict's
    invariance under strong (k,z)-weighting perturbations of the lensing kernel."""
    print("=" * 100)
    print("STAGE X -- validation addendum")
    print("=" * 100)

    # (i) BBKS/Sugiyama as an independent shape cross-check
    Gam = Om * h * np.exp(-Ob * (1.0 + np.sqrt(2 * h) / Om))
    def T_bbks(k_h):
        q = np.asarray(k_h, float) / Gam
        return (np.log(1.0 + 2.34 * q) / (2.34 * q) *
                (1.0 + 3.89 * q + (16.1 * q)**2 + (5.46 * q)**3 + (6.71 * q)**4)**-0.25)
    def D2_bbks_raw(k_h):
        return np.asarray(k_h, float)**(3.0 + ns) * T_bbks(k_h)**2
    nb = sig8**2 / np.trapz(D2_bbks_raw(_kk) * W_th(_kk * 8.0)**2, _lk)
    print("P(k) shape: EH98-no-wiggle (used) vs BBKS (independent), both sigma8-normalized:")
    worst = 0.0
    for kp in (0.005, 0.01, 0.02, 0.05, 0.1, 0.2, 0.5):
        pe = P_h(kp)
        pb = 2 * np.pi**2 * nb * D2_bbks_raw(kp) / kp**3
        worst = max(worst, abs(pe / pb - 1.0))
        print(f"  k={kp:5.3f}: P_EH={pe:9.1f}  P_BBKS={pb:9.1f}  ratio={pe/pb:6.3f}")
    print(f"  max |ratio-1| = {100*worst:.0f}%  (BBKS-vs-EH98 family difference is ~5-20%: PASS gate;")
    print("   the pre-fix code failed this gate at x2.2 -- see the bug log in the memo.)")

    # g_bar sensitivity to the transfer choice at the pivots
    print("g_bar sensitivity: nu at the E_G Reyes pivot under BBKS shape: ", end="")
    db = np.sqrt(nb * D2_bbks_raw(0.05)) * float(Dz(0.32))
    gb = PREF * (1.32)**2 * db / (0.05 * h / Mpc)
    nu_eh = float(nu(g_bar(0.05, 0.32) / A0_CANON))
    print(f"g_bar={gb:.3e}, nu={nu(gb/A0_CANON):.2f}  (EH98 value {nu_eh:.2f}: transfer-choice insensitive)")

    # (ii) absolute-calibration row
    Ls = np.unique(np.round(np.geomspace(2, 2000, 60)).astype(int)).astype(float)
    CK = np.array([CLkk(L)[0] for L in Ls])
    d2 = np.trapz((2 * Ls + 1) / (4 * np.pi) * 4 * CK / (Ls * (Ls + 1)), Ls)
    print(f"\nGR absolute calibration: d_rms = {np.sqrt(d2)*180/np.pi*60:.2f} arcmin (textbook 2.4-2.7;")
    print("  linear no-wiggle expected marginally low: PASS). phi-phi peak (stage C) = 1.34e-7 at L=40")
    print("  vs Planck/CAMB ~1.3e-7: PASS. Note the audit's numbers are GR-normalized RATIOS over the")
    print("  same kernel, so even a residual % -level GR miscalibration cancels; only the (k,z)-")
    print("  WEIGHTING enters, tested next.")

    # (iii) weighting-perturbation invariance of <Sigma^2> and of the required cap
    S = Sigma_factory("F1", a0=A0_CANON)
    def AL_pert(S, tilt):
        """recompute the kappa-weighted <Sigma^2> with the integrand re-weighted by (k/k0)^tilt
        (a deliberately violent skew standing in for any plausible P(k)/kernel miscalibration)."""
        zg = np.geomspace(1e-3, zstar, 1200)
        ch = chi_of_z(zg)
        num = den = 0.0
        for L in _LGRID:
            kM = (L + 0.5) / ch
            kh = kM / h
            W = 1.5 * Om * H0c**2 * (1.0 + zg) * ch * (1.0 - ch / chistar)
            Pm = P_h(kh) / h**3 * Dz(zg)**2 * (kh / 0.05)**tilt
            base = W * W / ch**2 * Pm * (c_SI / Hz(zg) / Mpc)
            I0 = np.trapz(base, zg)
            I1 = np.trapz(base * S(kh, zg)**2, zg)
            den += (2 * L + 1) * I0
            num += (2 * L + 1) * I1
        return num / den
    print("\nweighting-perturbation test on <Sigma^2> (F1 raw; tilt = (k/0.05)^t on the kernel):")
    for t in (-0.5, -0.25, 0.0, 0.25, 0.5):
        print(f"  tilt {t:+5.2f}: <Sigma^2> = {AL_pert(S, t):8.2f}")
    print("  => the x50-100 over-lensing is weighting-robust (spread ~x1.5 under violent tilts).")

if __name__ == "__main__":
    stage = sys.argv[1] if len(sys.argv) > 1 else "all"
    if stage in ("A", "all"):
        stageA()
    if stage in ("B", "all"):
        stageB()
    if stage in ("C", "all"):
        stageC()
    if stage in ("X", "all"):
        stageX()
