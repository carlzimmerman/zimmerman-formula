#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
L357 -- THE VIRIALIZATION-TRIGGERED CARRIER, AND THE VERSION THAT WORKS: decay where the local density is high AND the
vacuum dominates the expansion.

WHY.  L354-L356 left the kernel-invisible carrier (L353: the MOND kernel reads baryons only; the carrier feels and sources
Newtonian gravity only) with a z = 0 window but two open failures, both caused by a decay that is uniform in space:
KiDS (the carrier's full halo around isolated lenses) and high z (galaxies at z ~ 1-2.5 still sit in full halos).  The
next idea was a VIRIALIZATION trigger: decay only inside collapsed, dense regions, so the web and the forest stay cold and
galaxy interiors are cleared as they form.  This lane builds that trigger from the theory's own switch variable and pushes
it through every gate the carrier has faced -- and, where the plain trigger fails, builds the version that passes.

THE CONSTRUCTION (a construction, not a derivation).
  Carrier X (kernel-invisible, L353) decays X -> Y + light with a rate that switches on above a threshold,
      Gamma = Gamma_0 * Theta( u - u_v ),   u = x~ * [Omega_Lambda(z)/Omega_Lambda,0]^p,
  x~ = 9(R3 + sigma_ij sigma^ij)/(4K^2), the shear-completed switch variable of L351.  In a static bound region
  x~ >= (3/2)(rho - rho_bar_m)/rho_crit(z) (I26 with the shear dropped; the shear only adds, so every triggered fraction
  below is a LOWER bound).  p = 0 is the plain virialization/density trigger; p > 0 gates it by the vacuum's share of the
  expansion (the L319 idea), so the effective density threshold x_eff(z) = x_v0 [Omega_L,0/Omega_L(z)]^p rises steeply
  at z >~ 1.  Daughters get an isotropic kick v_k.
  The decay is one-shot at the particle's position (Gamma_0 >> H): 'cleared' = every carrier particle where the local
  total density exceeds the threshold decays; 'cap' = only the excess above the threshold density decays (the steady state
  if infall refills the region).  Both pictures are carried; the truth lies between.

METHOD (all machinery loaded unedited from committed lanes, one model added).
  * Halo model: Sheth-Tormen mass function + peak-background bias from CLASS's linear P(k) (the L319 cosmology), NFW with
    Dutton-Maccio 2014 c_200(M, z), carrier cut-off M_min = 1e8 Msun (the largest the forest itself allows; smaller
    M_min only adds decays).  The decayed fraction that matters for large-scale power is BIAS-WEIGHTED:
    F_b(z) = int n M b m_trig f_esc dM / rho_bar, with f_esc the fraction of kicked daughters that escape the host
    (escape speed and dispersion of the truncated NFW).  Decay is irreversible: the running maximum in time.
  * Forest and S_8: L319's validated linear solver (unchanged) with the survival history S(t) = 1 - F_b(t).
  * X-COP (12 clusters) and the three galaxy hosts: L321's phase-mixed retention machinery with L354's Newtonian carrier
    orbits and nu_mono, the decay confined to the triggered region (one function copied from L321 with that mask).
  * KiDS-1000 (Brouwer+21, 4 bins, full covariance): L355's machinery; the carrier template is the phase-mixed post-decay
    halo of each bin's Moster+13 host.
  * RC100 and the flagship (deep-MOND Tully-Fisher zero point at z = 2.5): L320/L356's machinery.

GATES (pre-declared, taken from the record, not re-chosen)
  forest   T^2(k = 5 h/Mpc) at z = 3 AND z = 2: >= the 5.3 keV relic's value on L319's grid, 0.995 (strict) or >= 0.9 (loose).
  S_8      >= 0.767 (strict) or >= 0.748 (alternative) (L322/L354).
  X-COP    median |M_dyn/M_HSE - 1| <= 0.2 (strict) or after X-COP's 6% non-thermal support (alternative) (L322/L354).
  galaxies the retained carrier raises g_obs at the gate radius by <= 0.06 dex in all three hosts (L321).
  KiDS     Delta chi^2 <= +9 against isolated MOND, both footings (L355); reported for the construction's own kernel field
           (the web's baryons, L355) and for a web-blind kernel (the open bound-region-kernel door).
  All gates on BOTH footings (a0 = 9.3619e-11 canonical, 1.1279e-10 alt).
CHECKS
  C1-C3 controls (ST sum rules; no-decay limits reproduce LCDM / L321 / L355).
  V1 the plain virialization trigger at its natural threshold (whole virialized halos decay) destroys the forest.
  V2 the plain trigger at any threshold has no STRICT window: the strict-forest floor leaves the galaxy gate failed.
     (Its loose-forest cells are scored in the design scan as p = 0.)
  D1 the vacuum-gated trigger: the design scan over (p, x_v0, v_k, picture); D2 its window through forest, S_8, X-COP and
     galaxies; K1 KiDS on the window; H1 RC100 and the flagship prediction on the best cell.
  Check directions were fixed after an exploratory run of the component calculations (not committed); nothing was retuned.
MUTATE=1: the trigger never fires (u_v -> infinity).  The forest failure of V1 must vanish and the window must close
(galaxies keep full halos): rc = 1.

Run from the repository root:  python3 real_research/dark_sector_2026/L357_virialization_triggered_carrier.py
"""
import os, sys, json, math, time, warnings, io, contextlib
from concurrent.futures import ThreadPoolExecutor
import numpy as np
from scipy.optimize import brentq
from scipy.interpolate import RegularGridInterpolator
warnings.filterwarnings("ignore", category=RuntimeWarning)
warnings.filterwarnings("ignore", category=DeprecationWarning)
warnings.filterwarnings("ignore", message=".*encountered in matmul.*")   # spurious macOS-Accelerate BLAS flags (as L319/L355)

HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
MUTATE = os.environ.get("MUTATE", "0") == "1"
SLUG = "L357_virialization_triggered_carrier"
T0 = time.time()
P = lambda *a: print(*a, flush=True)
CH, OUT = [], {"lane": "L357", "mutate": MUTATE, "checks": {}, "numbers": {}}
_trap = getattr(np, "trapezoid", None) or np.trapz


def check(name, measured, ok, reading="", load_bearing=True):
    ok = bool(ok); CH.append((name, ok, load_bearing))
    OUT["checks"][name] = {"ok": ok, "measured": str(measured), "load_bearing": load_bearing}
    P(f"  [{'PASS' if ok else 'FAIL'}] {name}"); P(f"         measured: {measured}")
    if reading: P(f"         reading:  {reading}")
    return ok


def banner(t): P("\n" + "=" * 112); P(t); P("=" * 112)


def quiet(fn, *a, **k):
    with contextlib.redirect_stdout(io.StringIO()):
        return fn(*a, **k)


P(__doc__.split("METHOD")[0].strip())
if MUTATE: P("\n  *** MUTATE=1: the trigger never fires; V1 and the window must FAIL ***")
FOOT = {"canonical": 9.3619e-11, "alt": 1.1279e-10}
S8_STRICT, S8_ALT, NT = 0.767, 0.748, 0.06
M_MIN = 1e8                                                           # Msun

# ================================================================================ L319's linear solver (unchanged)
P19 = os.path.join(HERE, "L319_lambda_triggered_kicked_decay.py")
G19 = {"__name__": "l319", "__file__": P19}
quiet(exec, open(P19).read().split("# ============================================================================================ controls")[0], G19)
h, Om, OL, a_grid, N_A = G19["h"], G19["Om"], G19["OL"], G19["a_grid"], G19["N_A"]
K_H, k5, T2f, S8_of = G19["K_H"], G19["k5"], G19["T2"], G19["S8_of"]
T2_53 = G19["T2_53"]
LC = quiet(G19["run"], np.ones(N_A), 0.0)
S8_LCDM = float(S8_of(T2f(LC, LC, 0.0)))
_RUNS = {}


NTH = int(os.environ.get("L357_THREADS", "6"))                       # numpy/LAPACK release the GIL: threads, not processes


def solve_hist(S, vk):
    key = (np.round(S, 7).tobytes(), float(vk))
    if key not in _RUNS:
        R = G19["run"](S, vk)                                          # L319's run() prints nothing (thread-safe call)
        _RUNS[key] = dict(t3=float(T2f(R, LC, 3.0)[k5]), t2=float(T2f(R, LC, 2.0)[k5]), S8=float(S8_of(T2f(R, LC, 0.0))),
                          T2z={z: T2f(R, LC, z) for z in (0.0, 1.0, 2.0, 3.0, 4.0, 6.0)})
    return _RUNS[key]


P(f"  L319 solver loaded: LCDM S_8 = {S8_LCDM:.4f}; strict forest threshold T^2(k=5) >= {T2_53:.4f}   [{time.time()-T0:.0f}s]")

# ================================================================================ halo model (L319's cosmology)
from classy import Class
cls = Class()
cls.set({"h": h, "omega_b": 0.02237, "omega_cdm": 0.1200, "A_s": 2.1e-9, "n_s": 0.9649, "tau_reio": 0.0544, "N_ur": 3.046,
         "N_ncdm": 0, "YHe": 0.2454, "output": "mPk", "P_k_max_h/Mpc": 200, "z_max_pk": 12})
cls.compute()
KH = np.geomspace(1e-4, 190, 2500); P0 = np.array([cls.pk_lin(k * h, 0.0) for k in KH]) * h**3
_DGC = {}


def DG(z):                                                            # cached: CLASS is called once per z, serially
    if z not in _DGC: _DGC[z] = cls.scale_independent_growth_factor(z)
    return _DGC[z]
LGM = np.linspace(5.0, 16.0, 221); MH = 10**LGM                        # Msun/h
RHOM_H = 2.775e11 * Om                                               # h^2 Msun / Mpc^3
RH = (3 * MH / (4 * np.pi * RHOM_H))**(1 / 3)
_X = np.outer(RH, KH); WT = 3 * (np.sin(_X) - _X * np.cos(_X)) / _X**3
SIG0 = np.sqrt(_trap(KH**2 * P0 * WT**2, KH, axis=1) / (2 * np.pi**2))
AST, QST, PST, DC = 0.3222, 0.707, 0.3, 1.686
f_st = lambda nu: AST * np.sqrt(2 * QST / np.pi) * (1 + (QST * nu**2)**(-PST)) * np.exp(-QST * nu**2 / 2)
b_st = lambda nu: 1 + (QST * nu**2 - 1) / DC + 2 * PST / (DC * (1 + (QST * nu**2)**PST))
def mfn(x):                                                           # NFW m(x) = ln(1+x) - x/(1+x), stable for tiny x (series)
    x = np.asarray(x, dtype=float)
    return np.where(x < 1e-4, x * x / 2 - 2 * x ** 3 / 3 + 3 * x ** 4 / 4, np.log1p(np.maximum(x, 1e-4)) - np.maximum(x, 1e-4) / (1 + np.maximum(x, 1e-4)))
GK = 4.30091727e-6                                                    # kpc (km/s)^2 / Msun
RHOC0_KPC = 277.5 * h**2                                              # Msun / kpc^3
Ez2 = lambda z: Om * (1 + z)**3 + OL
Om_z = lambda z: Om * (1 + z)**3 / Ez2(z)
OL_z = lambda z: OL / Ez2(z)


def c_dm14(Mh, z):                                                    # Dutton & Maccio 2014 (Planck), M in Msun/h
    a = 0.520 + (0.905 - 0.520) * math.exp(-0.617 * z**1.21); b = -0.101 + 0.026 * z
    return 10**(a + b * np.log10(Mh / 1e12))


def y_of(ratio):                                                      # solve y (1+y)^2 = ratio, vectorised (monotone Newton)
    t = np.log(np.maximum(np.minimum(ratio, ratio**(1 / 3)), 1e-12))
    lr = np.log(ratio)
    for _ in range(60):
        e = np.exp(t); g = t + 2 * np.log1p(e) - lr; t = t - g / (1 + 2 * e / (1 + e))
    return np.exp(t)


# escape probability of an isotropically kicked daughter from a Maxwellian parent: P(|s g + u n| > 1), u = v_k/v_esc,
# s = sigma/v_esc (fixed draws)
_rng = np.random.default_rng(11); _g = _rng.standard_normal((6000, 3)); _n = _rng.standard_normal((6000, 3))
_n /= np.linalg.norm(_n, axis=1)[:, None]
UG = np.linspace(0.0, 6.0, 121); SGR = np.linspace(0.02, 1.2, 60)
_PE = np.array([[np.mean(np.sum((s * _g + u * _n)**2, axis=1) > 1.0) for s in SGR] for u in UG])
PESC = RegularGridInterpolator((UG, SGR), _PE, bounds_error=False, fill_value=None)


def trig(z, x_eff, picture):
    """per halo: triggered carrier fraction m, trigger radius y_v = r_v/r_s, concentration, threshold (rho_crit units)."""
    cs = c_dm14(MH, z); dch = 200 / 3 * cs**3 / mfn(cs); rhv = Om_z(z) + 2 / 3 * x_eff
    y = np.minimum(y_of(dch / rhv), cs)
    m_in = mfn(y) / mfn(cs)
    m = m_in if picture == "cleared" else np.maximum(0.0, m_in - rhv * (y / cs)**3 / 200)
    return m, y, cs, dch, rhv


def esc(z, picture, vk, y, cs, dch, rhv):
    """mass-weighted escape fraction of the daughters born in each halo's triggered region."""
    if vk <= 0: return np.zeros_like(y)
    M200 = MH / h; r200 = (3 * M200 / (4 * np.pi * 200 * RHOC0_KPC * Ez2(z)))**(1 / 3); V200 = np.sqrt(GK * M200 / r200)
    s = np.geomspace(1e-3, 1.0, 50)[None, :]; yy = y[:, None] * s; xx = yy / cs[:, None]
    phi = -np.log1p(yy) / (xx * mfn(cs)[:, None]) + (np.log1p(cs) / mfn(cs))[:, None] - 1.0
    vesc = V200[:, None] * np.sqrt(np.maximum(-2 * phi, 1e-12))
    vc = V200[:, None] * np.sqrt(mfn(yy) / (mfn(cs)[:, None] * xx))
    pe = PESC(np.stack([np.clip(vk / vesc, 0, 6.0), np.clip(vc / np.sqrt(2) / vesc, 0.02, 1.2)], axis=-1))
    rho = dch[:, None] / (yy * (1 + yy)**2)
    wgt = (rho if picture == "cleared" else np.maximum(rho - rhv, 0.0)) * yy**3          # d(mass) per d ln y
    den = _trap(wgt, np.log(yy), axis=1)
    return np.where(den > 0, _trap(wgt * pe, np.log(yy), axis=1) / np.maximum(den, 1e-300), 1.0)


def Fb(z, x_eff, picture, vk=0.0, weight="bias", sig_scale=None):
    """bias-weighted (or plain) decayed fraction at z: triggered, and escaped if vk > 0."""
    if MUTATE or not np.isfinite(x_eff): return 0.0
    s = SIG0 * DG(z) * (1.0 if sig_scale is None else sig_scale); nu = DC / s
    w = f_st(nu) * np.abs(np.gradient(nu, np.log(MH)))
    m, y, cs, dch, rhv = trig(z, x_eff, picture)
    fe = esc(z, picture, vk, y, cs, dch, rhv) if vk > 0 else 1.0
    sel = MH >= M_MIN * h
    wb = w * (b_st(nu) if weight == "bias" else 1.0)
    return float(_trap((wb * m * fe)[sel], np.log(MH)[sel]))


ZG = np.array([0, 0.1, 0.25, 0.4, 0.6, 0.8, 1.0, 1.25, 1.5, 1.75, 2.0, 2.5, 3.0, 3.5, 4, 5, 6, 8, 10, 12, 15, 20, 30])
for _z in list(ZG) + [2.0, 3.0]: DG(float(_z))                        # warm the cache before any threading


def history(x_v0, p, picture, vk, sig_scale_fn=None):
    Fz = np.array([Fb(z, x_v0 * (OL_z(0) / OL_z(z))**p, picture, vk,
                      sig_scale=None if sig_scale_fn is None else sig_scale_fn(z)) for z in ZG])
    assert np.all(np.isfinite(Fz)), f"non-finite decayed fraction in history({x_v0}, {p}, {picture}, {vk})"
    Fz = np.where(Fz < 1e-10, 0.0, Fz)                                 # numerically zero decay is exactly zero (L319's solver needs W = 0, not 1e-20)
    Fc = np.maximum.accumulate(Fz[::-1])[::-1]                         # irreversible: never decreases forward in time
    za = 1 / a_grid - 1
    return 1 - np.interp(za, ZG, Fc, right=0.0), Fc


P(f"  halo model ready: sigma8 (CLASS) = {cls.sigma8():.4f}; carrier cut-off M_min = {M_MIN:.0e} Msun   [{time.time()-T0:.0f}s]")

# ================================================================================ L321 retention machinery (as L354)
P21 = os.path.join(HERE, "L321_carrier_z0_retention_gate.py")
_top = open(P21).read().split("# ============================================================================================ controls")[0]
_top = _top.split("P(__doc__)", 1)[1]
Lm = {"__name__": "l321", "__file__": P21, "HERE": HERE, "MUTATE": False, "P": (lambda *a: None), "banner": (lambda t: None),
      "json": json, "os": os, "math": math, "np": np, "time": time, "T0": T0, "CH": [], "OUT": {"numbers": {}},
      "check": (lambda *a, **k: True), "SLUG": "l321"}
quiet(exec, "import os, sys, json, math, time\nimport numpy as np\n" + _top, Lm)
KPC_M = Lm["KPC_M"]


def h_rar(y):
    y = np.asarray(y, float)
    return np.where(y < 1e4, y / np.expm1(np.sqrt(np.minimum(y, 1e4))), 0.0)


def dh_rar(y, e=1e-6): return (h_rar(y * (1 + e)) - h_rar(y * (1 - e))) / (2 * y * e)


Y_P = brentq(lambda y: float(dh_rar(y)), 1.0, 5.0); H_P = float(h_rar(Y_P))
LYG = np.linspace(-12, 12, 240001); YG = 10**LYG
DH = np.maximum(dh_rar(YG), 0.05 * H_P / (YG + Y_P))
H_MONO = float(h_rar(YG[0])) + np.concatenate([[0.0], np.cumsum(0.5 * (DH[1:] + DH[:-1]) * np.diff(YG))])


def nu_mono(y):                                                       # L340's monotone kernel (as L345/L354)
    y = np.maximum(np.asarray(y, float), 1e-12)
    return 1.0 + np.interp(np.log10(y), LYG, H_MONO) / y


Lm["nu"] = nu_mono
_grav21 = Lm["gravity"]
Lm["gravity"] = lambda gb, gc, ge, cp: (gb + gc) if cp == "newtonian" else _grav21(gb, gc, ge, cp)    # L354's force law
nfw21, potential, frac_inside, RG, FB, RHO_C0 = Lm["nfw"], Lm["potential"], Lm["frac_inside"], Lm["RG"], Lm["FB"], Lm["RHO_C0"]
CL, GAL, cl_ratio, gal_shift, hernquist, c200_z0 = Lm["CL"], Lm["GAL"], Lm["cl_ratio"], Lm["gal_shift"], Lm["hernquist"], Lm["c200_dm14"]
GE_GAL, GE_CL = Lm["GE_GAL"], Lm["GE_CL"]
CLREF = CL[int(np.argmin([abs(math.log10(c_["M200"] / 1e15)) for c_ in CL]))]
cl_mass_fn = (lambda x, c_=CLREF: c_["Mb"] * np.clip(np.asarray(x, dtype=float) / c_["R500"], 0, 1))


def retained_core(Mb_fn, M200, c, r_gate, ge, vk, rho_v, picture, N=12000, seed=5, iters=2, rhoc=None, probes=None):
    """L321's retained() (copied; L354's Newtonian carrier orbits), with the decay CONFINED to the triggered region.
    Returns the retained carrier inside r_gate relative to the no-decay control, and (optionally) that ratio at probe radii."""
    rhoc = RHO_C0 if rhoc is None else rhoc
    Mn, r200, rs = nfw21(M200, c, rhoc)
    Mc0 = lambda x: (1 - FB) * Mn(np.minimum(x, r200))
    rng = np.random.default_rng(seed)
    u = rng.random(N) * float(Mc0(r200)); rgrid = np.geomspace(1e-3 * rs, r200, 5000)
    r = np.interp(u, Mc0(rgrid), rgrid); w = float(Mc0(r200)) / N
    g_pre, _ = potential(Mb_fn, Mc0, ge, "newtonian")
    rho = np.where(RG < r200, 1.0 / ((RG / rs) * (1 + RG / rs)**2), 1e-300)
    integ = rho * g_pre; seg = 0.5 * (integ[1:] + integ[:-1]) * np.diff(RG)
    sig2 = np.concatenate([np.cumsum(seg[::-1])[::-1], [0.0]]) / np.maximum(rho, 1e-300)
    sig = np.sqrt(np.interp(r, RG, sig2))
    v = rng.normal(0, 1, (N, 3)) * sig[:, None]
    rho_tot = M200 / (4 * math.pi * rs**3 * mfn(c)) / ((r / rs) * (1 + r / rs)**2)
    pdec = (rho_tot >= rho_v).astype(float) if picture == "cleared" else np.clip(1 - rho_v / rho_tot, 0, 1)
    if MUTATE: pdec = np.zeros(N)
    is_d = rng.random(N) < pdec
    nh = rng.normal(0, 1, (N, 3)); nh /= np.linalg.norm(nh, axis=1)[:, None]

    def mass_in(kick, dec, gates):
        vv = v + ((is_d if dec else np.zeros(N, bool)) * kick)[:, None] * nh
        vrad, vtan = vv[:, 0], np.linalg.norm(vv[:, 1:], axis=1); L = r * vtan; Mc = Mc0
        for _ in range(iters):
            _, Phi = potential(Mb_fn, Mc, ge, "newtonian")
            E = 0.5 * (vrad**2 + vtan**2) + np.interp(r, RG, Phi)
            probe = np.geomspace(0.02 * rs, 3 * r200, 24)
            prof = np.array([w * frac_inside(E, L, Phi, rg).sum() for rg in probe])
            Mc = (lambda pr=probe, pm=prof: (lambda x: np.interp(np.asarray(x, dtype=float), pr, pm, left=0.0)))()
        _, Phi = potential(Mb_fn, Mc, ge, "newtonian")
        E = 0.5 * (vrad**2 + vtan**2) + np.interp(r, RG, Phi)
        return np.array([w * frac_inside(E, L, Phi, rg).sum() for rg in gates])

    gates = [r_gate] + ([] if probes is None else list(probes))
    m_ctrl = mass_in(0.0, False, gates); m_dec = mass_in(vk, True, gates)
    ratio = m_dec / np.maximum(m_ctrl, 1e-300)
    return float(ratio[0]), (ratio[1:] if probes is not None else None), float(pdec.mean())


def rho_thr(x_eff, z, rhoc_kpc):                                      # total-density threshold [Msun/kpc^3]
    return (Om_z(z) + 2 / 3 * x_eff) * rhoc_kpc


P(f"  L321 machinery loaded ({len(CL)} X-COP clusters; retention reference {CLREF['name']}, M200 {CLREF['M200']:.2e}, "
  f"c {CLREF['c']:.2f}, z {CLREF['z']:.3f})   [{time.time()-T0:.0f}s]")

# ================================================================================ L355 KiDS machinery (unedited)
P55 = os.path.join(REPO, "real_research", "g03_audit_2026", "L355_kernel_invisible_kids.py")
L55 = {"__name__": "l355", "__file__": P55}
quiet(exec, open(P55).read().split("# ============================================================================================ K1 control")[0], L55)
fit55, ES55, FIELDS55, sw55, mx55 = L55["fit"], L55["ES"], L55["FIELDS"], L55["stack_weights"], L55["maxwell_e"]
esd_of_M, rr55, MPCm, Rp55, Rd55, MS = L55["esd_of_M"], L55["rr"], L55["MPCm"], L55["Rp"], L55["Rd"], L55["MS"]
M200_KIDS, c200_55, ZL, LOGMS = L55["M200s"], L55["c200"], L55["ZL"], L55["LOGMS"]
RHOC_ZL = RHOC0_KPC * Ez2(ZL)
W0 = np.zeros(len(ES55)); W0[0] = 1.0
REF55 = {f_: fit55(f_, W0, 0.0, False)[0] for f_ in FOOT}
KERNELS = {"own field (web baryons)": L55["Ob"] / L55["Om"], "web-blind kernel": 0.0}
P(f"  L355 KiDS machinery loaded: isolated-MOND chi^2 canonical {REF55['canonical']:.1f}, alt {REF55['alt']:.1f}   [{time.time()-T0:.0f}s]")


def kids_templates(x_eff, picture):
    """phase-mixed post-decay carrier halo of each KiDS bin's host (daughters escape: v_k >= 1200 km/s >> these v_esc)."""
    T, rvs = [], []
    for b in range(4):
        M200 = M200_KIDS[b]; c = float(c200_55(M200))
        Mn, r200, rs = nfw21(M200, c, RHOC_ZL)
        pro = np.geomspace(0.02 * rs, 0.999 * r200, 40)
        if MUTATE or not np.isfinite(x_eff):
            ratio_p = np.ones(len(pro)); rv = 0.0
        else:
            rv_ = rho_thr(x_eff, ZL, RHOC_ZL)
            rho_s = M200 / (4 * math.pi * rs**3 * mfn(c)); yv = float(y_of(np.array([rho_s / rv_]))[0]) * rs
            rv = min(yv, r200)
            Mb_fn = hernquist(1.3 * 10**LOGMS[b], 3.0)
            _, ratio_p, _ = retained_core(Mb_fn, M200, c, r200, 0.0, 1e5, rv_, picture, rhoc=RHOC_ZL, probes=pro, N=8000)
        r_kpc = rr55 / KPC_M
        Mc = (1 - FB) * Mn(np.minimum(r_kpc, r200)) * np.interp(np.log(r_kpc), np.log(pro), ratio_p)
        dS = esd_of_M(Mc * MS + 1.0, 1.0)
        T.append(np.interp(Rd55[b], Rp55 / MPCm, dS)); rvs.append(rv)
    return T, rvs


def kids_score(T):
    L55["TCAR"] = T
    out = {}
    for lab, kf in KERNELS.items():
        for f_ in FOOT:
            wts = W0 if kf == 0 else sw55(mx55(FIELDS55["linear-theory (16 Mpc)"] * kf / FOOT[f_]))
            c_, _, pars = fit55(f_, wts, 1.0, True)
            out[(lab, f_)] = dict(dchi2=float(c_ - REF55[f_]), A=[round(p_[1], 2) for p_ in pars])
    return out


# ================================================================================ CONTROLS
banner("CONTROLS")
from scipy.integrate import quad
sr = (float(quad(f_st, 0, 40, limit=200)[0]), float(quad(lambda n_: f_st(n_) * b_st(n_), 0, 40, limit=200)[0]))
check("C1 the Sheth-Tormen mass function and its peak-background bias satisfy their sum rules (int f = int f b = 1)",
      f"{sr[0]:.4f}, {sr[1]:.4f}", abs(sr[0] - 1) < 2e-3 and abs(sr[1] - 1) < 2e-3, load_bearing=False)
Binf = Fb(3.0, 0.0, "cleared"); B30 = Fb(3.0, 30.0, "cleared")
check("C2 limits of the triggered fraction: threshold -> infinity gives 0; threshold -> 0 gives the bias-weighted collapsed "
      "fraction above M_min (every halo decays whole)",
      f"F_b(z=3): x_v -> inf {Fb(3.0, np.inf, 'cleared'):.3f}; x_v -> 0 {Binf:.3f}; x_v = 30 {B30:.3f}",
      Fb(3.0, np.inf, "cleared") == 0.0 and (MUTATE or Binf > 0.3), load_bearing=False)
ctrl = solve_hist(np.ones(N_A), 3000.0)
check("C3 the no-decay history reproduces LCDM through L319's solver (forest and S_8 at the LCDM values)",
      f"T^2(k=5) z=3 {ctrl['t3']:.4f}, z=2 {ctrl['t2']:.4f}; S_8 {ctrl['S8']:.4f} vs LCDM {S8_LCDM:.4f}",
      abs(ctrl["t3"] - 1) < 1e-6 and abs(ctrl["S8"] - S8_LCDM) < 1e-6, load_bearing=False)
OUT["numbers"]["controls"] = dict(sum_rules=sr, B_z3=Binf, S8_LCDM=S8_LCDM)

# ================================================================================ V1-V2 the plain virialization trigger
banner("V1  THE PLAIN VIRIALIZATION TRIGGER (p = 0) AT ITS NATURAL THRESHOLD: whole virialized halos decay")
V1 = {}
for xv, vk1, pic in [(xv_, vk_, pc_) for xv_ in (30.0, 100.0) for vk_ in (700.0, 3000.0) for pc_ in ("cleared", "cap")]:
    if True:
        S, Fc = history(xv, 0.0, pic, vk1)
        r1 = solve_hist(S, vk1)
        # one back-reaction pass: the carrier that has decayed no longer clusters, so fewer halos form -- rescale sigma(M, z)
        # by the solver's own transfer at the halo's Lagrangian scale and recompute the history
        T2z = r1["T2z"]; zk = sorted(T2z)

        def sig_scale(z, T2z=T2z, zk=zk):
            t2 = np.array([np.interp(np.log(np.clip(1 / RH, K_H[0], K_H[-1])), np.log(K_H), T2z[zz]) for zz in zk])
            return np.sqrt(np.clip([np.interp(z, zk, t2[:, i]) for i in range(len(RH))], 1e-6, None))

        S2, Fc2 = history(xv, 0.0, pic, vk1, sig_scale_fn=sig_scale)
        r2 = solve_hist(S2, vk1)
        V1[(xv, vk1, pic)] = dict(Fb_z2=float(np.interp(2, ZG, Fc)), Fb_z3=float(np.interp(3, ZG, Fc)), t2=r1["t2"], t3=r1["t3"],
                             Fb_z2_br=float(np.interp(2, ZG, Fc2)), t2_br=r2["t2"], t3_br=r2["t3"], S8=r1["S8"], S8_br=r2["S8"])
        P(f"    x_v = {xv:5.0f} v_k = {vk1:5.0f} {pic:7s}: F_b(z=2,3) = {V1[(xv, vk1, pic)]['Fb_z2']:.3f}/{V1[(xv, vk1, pic)]['Fb_z3']:.3f}"
          f" -> T^2(k=5) z=2 {r1['t2']:.3f}, z=3 {r1['t3']:.3f}; with back-reaction F_b(z=2) {V1[(xv, vk1, pic)]['Fb_z2_br']:.3f}"
          f" -> T^2 z=2 {r2['t2']:.3f}, z=3 {r2['t3']:.3f}; S_8 {r2['S8']:.3f}")
OUT["numbers"]["V1"] = {f"{k_[0]:.0f}/{k_[1]:.0f}/{k_[2]}": v_ for k_, v_ in V1.items()}
worst_t = max(max(min(v_["t2"], v_["t3"]), min(v_["t2_br"], v_["t3_br"])) for v_ in V1.values())
check("V1 the plain virialization trigger at its natural threshold (x_v = 30-100: every virialized halo decays), as a LOCAL "
      "trigger that fires in every halo down to M_min = 1e8 Msun, FAILS the forest even on the loose reading (T^2(k=5) < 0.9 "
      "at z = 2 or 3) at slow (700 km/s) and fast (3000 km/s) kicks, with and without the back-reaction of the decay on halo "
      "formation, in both pictures", f"largest min(T^2 z=2, z=3) over all cases {worst_t:.3f} (loose needs >= 0.9)",
      worst_t < 0.9, "by z = 2-3 about half of the bias-weighted mass sits in collapsed halos; a carrier that decays on "
      "collapse takes it out of the forest's power.  The parallel L365 (two-species PM, trigger on the MESH-scale density, "
      "its 'least-trigger estimate') finds a slow-kick window because halos below its resolution never trigger; the two "
      "lanes bracket the plain trigger, and the verdict hinges on whether the carrier's small halos fire")

banner("V2  THE PLAIN TRIGGER AT ANY THRESHOLD: the forest floor against X-COP's ceiling")
XV2 = [300.0, 500.0, 700.0, 1000.0, 2000.0, 3000.0, 5000.0, 7000.0, 1e4, 2e4, 3e4, 5e4]
V2 = {}
for pic in ("cleared", "cap"):
    for xv in XV2:
        S, Fc = history(xv, 0.0, pic, 3000.0)
        r_ = solve_hist(S, 3000.0)
        V2[(pic, xv)] = dict(t2=r_["t2"], t3=r_["t3"], S8=r_["S8"], Fb_z2=float(np.interp(2, ZG, Fc)))
    P(f"    {pic:7s}: " + "  ".join(f"{xv:.0f}:{min(V2[(pic, xv)]['t2'], V2[(pic, xv)]['t3']):.3f}" for xv in XV2)
      + "   [min T^2(k=5) over z = 2, 3]")
floor_loose = {pic: min([xv for xv in XV2 if min(V2[(pic, xv)]["t2"], V2[(pic, xv)]["t3"]) >= 0.9] or [np.inf]) for pic in ("cleared", "cap")}
floor_strict = {pic: min([xv for xv in XV2 if min(V2[(pic, xv)]["t2"], V2[(pic, xv)]["t3"]) >= T2_53] or [np.inf]) for pic in ("cleared", "cap")}
P("    forest floor (loose / strict): " + "; ".join(f"{p_}: {floor_loose[p_]:.0f} / {floor_strict[p_]:.0f}" for p_ in floor_loose))


def gal_eps(pic, xv, vk):                                             # retention per host (footing-independent: Newtonian orbits)
    out = {}
    for kh, hst in GAL.items():
        c = float(c200_z0(hst["M200"])); rv_ = rho_thr(xv, 0.0, RHO_C0)
        out[kh] = retained_core(hernquist(hst["Mb"], hst["a"]), hst["M200"], c, hst["rg"], GE_GAL, vk, rv_, pic)[0]
    return out


def gal_shifts(eps):
    out = {}
    for f_ in FOOT:
        Lm["A0"] = FOOT[f_] * KPC_M / 1e6
        out[f_] = {kh: gal_shift(GAL[kh], e, "additive") for kh, e in eps.items()}
    return out


# the galaxy gate AT the strict forest floor (the least-demanding strict threshold), v_k = 3000 km/s
GS2 = {}
for pic in ("cleared", "cap"):
    xv = floor_strict[pic]
    if np.isfinite(xv):
        GS2[pic] = gal_shifts(gal_eps(pic, xv, 3000.0))
P("    galaxy gate at the strict forest floor: " + "; ".join(
    f"{pic} (x_v = {floor_strict[pic]:.0f}): max shift " + ", ".join(f"{f_[:5]} {max(v_.values()):+.3f}" for f_, v_ in sh.items())
    for pic, sh in GS2.items()))
OUT["numbers"]["V2"] = dict(scan={f"{k_[0]}/{k_[1]:.0f}": v_ for k_, v_ in V2.items()}, floor_loose=floor_loose,
                            floor_strict=floor_strict, galaxies_at_strict_floor=GS2)
v2_closed = all((not np.isfinite(floor_strict[pic])) or max(max(v_.values()) for v_ in GS2[pic].values()) > 0.06
                for pic in ("cleared", "cap"))
check("V2 the plain virialization trigger has NO strict window: every threshold high enough for the strict forest (5.3 keV "
      "equivalent at z = 2 and 3) leaves the galaxy gate failed (> 0.06 dex), both pictures, both footings",
      "; ".join(f"{pic}: floor {floor_strict[pic]:.0f}, max shift {max(max(v_.values()) for v_ in GS2[pic].values()):+.3f}"
                if pic in GS2 else f"{pic}: no strict-forest threshold" for pic in ("cleared", "cap")), v2_closed,
      "a density threshold that spares z = 2-3 halos is far above the densities where galaxies are measured today; the "
      "plain trigger's loose-forest cells are scored with the vacuum-gated ones in D1 (p = 0)")

# ================================================================================ D1 the vacuum-gated trigger: design scan
banner("D1  THE VACUUM-GATED TRIGGER u = x~ [Omega_L(z)/Omega_L,0]^p: the design scan (forest, S_8 on the halo model; "
       "X-COP by phase-mixed retention)")
PS = [0.0, 1.0, 2.0]; XV0 = [700.0, 1000.0, 1500.0, 2000.0, 3000.0, 5000.0, 10000.0]
VKS = [1200.0, 2000.0, 3000.0]
PICS = ("cleared", "cap")
# X-COP retention in the reference cluster (x_eff at the cluster's z for p = 2; p = 1, 3 differ by <= 6% in x_eff)
EPSCL = {}


def _eps_job(j):
    pic, xv, vk = j
    rv_ = rho_thr(xv * (OL_z(0) / OL_z(CLREF["z"]))**2, CLREF["z"], CLREF["rhoc"])
    return j, retained_core(cl_mass_fn, CLREF["M200"], CLREF["c"], CLREF["R500"], GE_CL, vk, rv_, pic, rhoc=CLREF["rhoc"])[0]


with ThreadPoolExecutor(NTH) as _ex:
    for _j, _e in _ex.map(_eps_job, [(pic, xv, vk) for pic in PICS for xv in XV0 for vk in VKS]):
        EPSCL[_j] = _e
for pic in PICS:
    P(f"    X-COP reference retention ({pic}): " + "  ".join(f"{xv:.0f}/" + "/".join(f"{EPSCL[(pic, xv, vk)]:.2f}" for vk in VKS)
                                                         for xv in XV0) + f"   [eps at v_k = {VKS}; {time.time()-T0:.0f}s]")


def xcop(pic, xv, vk):
    out = {}
    for f_ in FOOT:
        Lm["A0"] = FOOT[f_] * KPC_M / 1e6
        med = float(np.median([cl_ratio(c_, EPSCL[(pic, xv, vk)], "additive") for c_ in CL]))
        out[f_] = dict(ratio=med, strict=abs(med - 1) <= 0.2, alt=abs(med * (1 - NT) - 1) <= 0.2)
    return out


ROWS = []


def _row_job(j):
    p, pic, xv, vk = j
    S, Fc = history(xv, p, pic, vk)
    return j, Fc, solve_hist(S, vk)


_jobs = [(p, pic, xv, vk) for p in PS for pic in PICS for xv in XV0 for vk in VKS]
with ThreadPoolExecutor(NTH) as _ex:
    _RES = dict((j_, (fc_, r_)) for j_, fc_, r_ in _ex.map(_row_job, _jobs))
for p in PS:
    for pic in PICS:
        for xv in XV0:
            for vk in VKS:
                Fc, r_ = _RES[(p, pic, xv, vk)]
                xc = xcop(pic, xv, vk)
                row = dict(p=p, picture=pic, x_v0=xv, v_k=vk, Fb=[float(np.interp(z, ZG, Fc)) for z in (0, 0.5, 1, 2, 3)],
                           t2=r_["t2"], t3=r_["t3"], S8=r_["S8"], xcop={f_: xc[f_]["ratio"] for f_ in FOOT},
                           forest_strict=bool(min(r_["t2"], r_["t3"]) >= T2_53), forest_loose=bool(min(r_["t2"], r_["t3"]) >= 0.9),
                           S8_strict=bool(r_["S8"] >= S8_STRICT), S8_alt=bool(r_["S8"] >= S8_ALT),
                           xcop_strict=all(xc[f_]["strict"] for f_ in FOOT), xcop_alt=all(xc[f_]["alt"] for f_ in FOOT))
                ROWS.append(row)
            P(f"    p={p:.0f} {pic:7s} x_v0={xv:5.0f}: " + " | ".join(
                f"v_k {r['v_k']:.0f}: T2 {min(r['t2'], r['t3']):.4f} S8 {r['S8']:.3f} X-COP {r['xcop']['canonical']:.2f}/{r['xcop']['alt']:.2f}"
                for r in ROWS[-len(VKS):]) + f"   [{time.time()-T0:.0f}s]")
OUT["numbers"]["D1"] = ROWS

# ================================================================================ D2 galaxies on the candidates -> the window
banner("D2  THE WINDOW: candidates passing forest + S_8 + X-COP (both footings) are put through the galaxy gate")


def galaxies(pic, xv, vk):
    return gal_shifts(gal_eps(pic, xv, vk))


WIN = {"strict": [], "alt": []}; GALS = {}
_cands = sorted({(r["picture"], r["x_v0"], r["v_k"]) for r in ROWS for t in ("strict", "alt")
                 if (r["forest_strict"] if t == "strict" else r["forest_loose"]) and (r["S8_strict"] if t == "strict" else r["S8_alt"])
                 and (r["xcop_strict"] if t == "strict" else r["xcop_alt"])})
with ThreadPoolExecutor(NTH) as _ex:
    _GEPS = dict(zip(_cands, _ex.map(lambda k_: gal_eps(*k_), _cands)))
P(f"    {len(_cands)} candidate (picture, x_v0, v_k) cells put through the galaxy gate   [{time.time()-T0:.0f}s]")
for r in ROWS:
    for t in ("strict", "alt"):
        fo = r["forest_strict"] if t == "strict" else r["forest_loose"]
        s8 = r["S8_strict"] if t == "strict" else r["S8_alt"]
        xc = r["xcop_strict"] if t == "strict" else r["xcop_alt"]
        if fo and s8 and xc:
            key = (r["picture"], r["x_v0"], r["v_k"])
            if key not in GALS:
                GALS[key] = gal_shifts(_GEPS[key])
            gmax = max(max(v_.values()) for v_ in GALS[key].values())
            r[f"gal_max_{t}"] = gmax
            if gmax <= 0.06:
                WIN[t].append(r)
for t in ("strict", "alt"):
    P(f"    {t:6s} window ({len(WIN[t])} cells): " + ("; ".join(
        f"p={r['p']:.0f} {r['picture']} x_v0={r['x_v0']:.0f} v_k={r['v_k']:.0f} (T2 {min(r['t2'], r['t3']):.4f}, S8 {r['S8']:.3f}, "
        f"X-COP {r['xcop']['canonical']:.2f}/{r['xcop']['alt']:.2f})" for r in WIN[t]) or "none"))
OUT["numbers"]["D2"] = {"galaxy_shifts": {f"{k_[0]}/{k_[1]:.0f}/{k_[2]:.0f}": v_ for k_, v_ in GALS.items()},
                        "window": {t: [dict(p=r["p"], picture=r["picture"], x_v0=r["x_v0"], v_k=r["v_k"]) for r in WIN[t]]
                                   for t in WIN}}
check("D2 the vacuum-gated trigger OPENS a window: cells pass the forest, S_8, X-COP and the galaxy gate together on both "
      "footings (strict thresholds, or the alternative set)", f"strict {len(WIN['strict'])} cells, alternative {len(WIN['alt'])} cells",
      len(WIN["strict"]) + len(WIN["alt"]) > 0,
      "the density threshold separates galaxies (probed at x~ ~ 1e4-1e5) from cluster outskirts (x~ ~ 200-350 at R500); the "
      "vacuum gate keeps z >= 2 halos intact for the forest")

# ================================================================================ K1 KiDS on the window
banner("K1  KiDS-1000 ON THE WINDOW: the phase-mixed post-decay halos of the four lens bins (z_l = 0.25)")
KID = {}
_cand = {}
for t in ("strict", "alt"):
    for r in WIN[t]:
        k_ = (r["p"], r["picture"], r["x_v0"]); _cand[k_] = max(_cand.get(k_, -9), r["S8"] - S8_ALT)
cells = sorted(sorted(_cand, key=lambda k_: -_cand[k_])[:10])                 # at most 10 cells (the widest S_8 margins)
with ThreadPoolExecutor(NTH) as _ex:
    _TPL = dict(zip(cells, _ex.map(lambda k_: kids_templates(k_[2] * (OL_z(0) / OL_z(ZL))**k_[0], k_[1]), cells)))
for (p, pic, xv) in cells:
    xe = xv * (OL_z(0) / OL_z(ZL))**p
    T, rvs = _TPL[(p, pic, xv)]
    sc = kids_score(T)
    KID[(p, pic, xv)] = dict(x_eff=xe, r_v_kpc=[round(x_, 1) for x_ in rvs], score={f"{k_[0]}/{k_[1]}": v_ for k_, v_ in sc.items()})
    P(f"    p={p:.0f} {pic:7s} x_v0={xv:5.0f} (x_eff {xe:.0f}; r_v {[round(x_) for x_ in rvs]} kpc): " + "; ".join(
        f"{k_[0][:9]}/{k_[1][:5]} {v_['dchi2']:+.1f}" for k_, v_ in sc.items()) + f"   [{time.time()-T0:.0f}s]")
OUT["numbers"]["K1"] = {f"{k_[0]:.0f}/{k_[1]}/{k_[2]:.0f}": v_ for k_, v_ in KID.items()}
kid_own = {k_: max(v_["score"][f"own field (web baryons)/{f_}"]["dchi2"] for f_ in FOOT) for k_, v_ in KID.items()}
kid_blind = {k_: max(v_["score"][f"web-blind kernel/{f_}"]["dchi2"] for f_ in FOOT) for k_, v_ in KID.items()}
best_blind = min(kid_blind.values()) if kid_blind else float("nan")
check("K1 (reported) KiDS on the window: with the construction's own kernel field (the web's baryons) KiDS fails as it does "
      "for every carrier (L355); with a web-blind kernel the window's best cell is scored against the +9 criterion",
      f"own field: worst-footing Delta chi^2 min {min(kid_own.values()) if kid_own else float('nan'):+.1f}; web-blind: best cell "
      f"{best_blind:+.1f}", True, "KiDS is the construction's open gate; it is conditional on the bound-region kernel "
      "(L355's door), which no carrier can supply", load_bearing=False)

# ================================================================================ H1 RC100 and the flagship on the best cell
banner("H1  HIGH REDSHIFT ON THE BEST CELL: RC100 (z = 0.6-2.5) and the flagship prediction at z = 2.5")
P20 = os.path.join(HERE, "L320_carrier_highz_price_rc100.py")
L20 = {"__name__": "l320", "__file__": P20}
quiet(exec, open(P20).read().split("# ------------------------------------------------------------------------------------------------ models")[0]
      .replace('MUTATE = os.environ.get("MUTATE", "0") == "1"', "MUTATE = False"), L20)
best = None
pool = WIN["strict"] or WIN["alt"]
if pool:
    best = max(pool, key=lambda r: (r["S8"] - S8_STRICT) + (0.2 - abs(r["xcop"]["alt"] - 1)))
H1 = {}
if best is not None:
    p, pic, xv = best["p"], best["picture"], best["x_v0"]
    G, MSUN, KPC = L20["G"], L20["MSUN"], L20["KPC"]

    def carrier_g(Mh, z, r):
        """carrier field at r after the trigger (static NFW; cleared inside r_v, or capped)."""
        cc = float(L20["c200"](Mh, z)); rhoc = L20["rho_crit"](z)
        r200 = (3 * Mh * MSUN / (4 * math.pi * 200 * rhoc))**(1 / 3); rs = r200 / cc
        rho_s = Mh * MSUN / (4 * math.pi * rs**3 * mfn(cc))
        rv_ = (Om_z(z) + 2 / 3 * xv * (OL_z(0) / OL_z(z))**p) * rhoc
        rr_ = np.geomspace(1e-4 * rs, min(r, r200), 3000); rho = rho_s / ((rr_ / rs) * (1 + rr_ / rs)**2)
        keep = np.where(rho >= rv_, 0.0, rho) if pic == "cleared" else np.minimum(rho, rv_)
        return G * (1 - FB) * float(_trap(4 * math.pi * rr_**2 * keep, rr_)) / r**2
    zs = [g_["z"] for g_ in L20["gal"]]; fd_c, la_c = [], []
    for f_, a0 in (("canonical", FOOT["canonical"]),):
        for g_ in L20["gal"]:
            z = g_["z"]; gb = G * 0.5 * g_["Mb"] * MSUN / g_["Re"]**2; mu = 0.5 * ((1 + z) / 2)**2
            gc = carrier_g(L20["halo_mass"](g_["Mb"] / (1 + mu), z), z, g_["Re"])
            go = float(nu_mono(gb / a0)) * gb + gc; f = 1 - gb / go
            fd_c.append(f); la_c.append(L20["invert"](f, go))
    s_c, e_c, _ = L20["slope_boot"](zs, la_c)
    H1["rc100"] = dict(median_fdm=float(np.nanmedian(fd_c)), slope=s_c, data_median_fdm=float(np.median([g_["fdm"] for g_ in L20["gal"]])),
                       data_slope=L20["s_data"], data_err=L20["e_data"])
    fl = []
    for f_, a0 in FOOT.items():
        for lMb in (10.0, 10.5, 11.0):
            Mb = 10**lMb; r_out = math.sqrt(G * Mb * MSUN / (0.1 * a0)); gb = G * Mb * MSUN / r_out**2
            g_fw = float(nu_mono(gb / a0)) * gb; mu = 0.5 * ((1 + 2.5) / 2)**2
            gc = carrier_g(L20["halo_mass"](Mb / (1 + mu), 2.5), 2.5, r_out)
            fl.append(dict(footing=f_, logMb=lMb, r_out_kpc=r_out / KPC, shift_dex=2 * math.log10((g_fw + gc) / g_fw)))
    H1["flagship"] = fl
    P(f"    best cell: p={p:.0f} {pic} x_v0={xv:.0f} v_k={best['v_k']:.0f}")
    P(f"    RC100: median f_DM(<R_e) {H1['rc100']['median_fdm']:.2f} (data {H1['rc100']['data_median_fdm']:.2f}); inverted slope "
      f"{s_c:+.3f} (data {L20['s_data']:+.3f} +/- {L20['e_data']:.3f}; framework alone 0.000)")
    P("    flagship (deep-MOND Tully-Fisher zero point at z = 2.5; framework 0.00, LCDM +0.33): " + "; ".join(
        f"{d['footing'][:5]} logMb {d['logMb']:.1f}: {d['shift_dex']:+.2f} dex" for d in fl))
OUT["numbers"]["H1"] = H1
check("H1 (reported) the window's high-z prediction: RC100 and the flagship zero-point shift on the best cell",
      H1.get("flagship", "no window cell"), True, "a prediction of the construction, not a gate", load_bearing=False)

# ================================================================================ verdict
banner("VERDICT")
if WIN["strict"] or WIN["alt"]:
    b_ = best
    P(f"""  THE PLAIN VIRIALIZATION TRIGGER IS CLOSED; THE VACUUM-GATED ONE WORKS THROUGH FOUR GATES.
  Decaying the carrier whenever a halo virializes takes ~half the bias-weighted mass out of the z = 2-3 forest (V1); raising
  the threshold until the forest survives leaves cluster outskirts untouched and X-COP overshoots (V2).  Gating the same
  density trigger by the vacuum's share of the expansion, u = x~ [Omega_L(z)/Omega_L,0]^p, fixes both at once: it sleeps
  through z >= 2 and, once Lambda dominates, clears exactly the dense regions -- galaxy interiors (x~ ~ 1e4-1e5 where
  rotation curves are measured) and cluster cores -- while cluster outskirts (x~ ~ 200-350 at R500) keep their carrier and
  the halo that loses its core expands.  Window: strict {len(WIN['strict'])} cells, alternative {len(WIN['alt'])} cells.
  Best cell p = {b_['p']:.0f}, {b_['picture']}, x_v0 = {b_['x_v0']:.0f}, v_k = {b_['v_k']:.0f} km/s: T^2(k=5) >= {min(b_['t2'], b_['t3']):.4f},
  S_8 = {b_['S8']:.3f}, X-COP {b_['xcop']['canonical']:.2f}/{b_['xcop']['alt']:.2f} (canonical/alt).
  OPEN: KiDS (K1) -- with the construction's own kernel field it fails like every carrier (L355); with a web-blind kernel
  see K1.  The flagship shifts (H1): the construction predicts a non-zero deep-MOND zero-point offset at z = 2.5.""")
else:
    P("  No cell of the vacuum-gated trigger passes the forest, S_8, X-COP and the galaxy gate together.")
n_fail = sum(1 for _, ok, lb in CH if lb and not ok)
OUT["n_checks"], OUT["n_fail_load_bearing"] = len(CH), n_fail
OUT["runtime_s"] = time.time() - T0
outname = f"{SLUG}_results{'_MUTATE' if MUTATE else ''}.json"
json.dump(OUT, open(os.path.join(HERE, outname), "w"), indent=1, default=str)
P(f"\n  {sum(1 for _, ok, _ in CH if ok)}/{len(CH)} checks pass; load-bearing failures: {n_fail}; wrote {outname}   [{time.time()-T0:.0f}s]")
sys.exit(0 if n_fail == 0 else 1)
