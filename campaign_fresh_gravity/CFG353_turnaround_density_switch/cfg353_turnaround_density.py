#!/usr/bin/env python3
"""
CFG353 -- a turnaround-density reader from a leaf-elliptic auxiliary potential.  Criteria: FROZEN_CRITERIA.md (c9d9a1d7b).

  Phi_d on each leaf: lap Phi_d = 4 pi G (rho - <rho>_leaf)  (total matter; MS1 relaxed by the owner's 10-06 decision).
  Estimator: rho_est = 3 |grad Phi_d|^2 / (4 pi G |Phi_d|)  (estimates the enclosed mean OVERDENSITY).
  Switch:    f = H_strict(3 |grad Phi_d|^2 - (Delta_ta - 1) 4 pi G rho_bar |Phi_d|),  Delta_ta(z) from spherical collapse.
  Units:     phi = Phi_d / (4 pi G rho_bar), lap phi = delta, rho_est / rho_bar = 3 |grad phi|^2 / |phi|.
  Routes:    E0 <phi> = 0 (scored), E1 phi - sup phi (scored second), Einf zero at the host's local infinity (reported).
MUTATE: CFG353_MUTATE=1 -> threshold Delta = 1 (any overdensity); must fail (a'); outputs *_MUTATE; exit 1.
Run: python3 campaign_fresh_gravity/CFG353_turnaround_density_switch/cfg353_turnaround_density.py
"""
import os, sys, io, json, math, contextlib, time
import numpy as np
import sympy as sp
from scipy.integrate import solve_ivp, quad
from scipy.optimize import brentq
from scipy.special import erf

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
MUTATE = os.environ.get("CFG353_MUTATE", "0") == "1"
SUF = "_MUTATE" if MUTATE else ""
P = lambda *a: print(*a, flush=True)
OUT = {"lane": "CFG353", "mutate": MUTATE, "frozen": "c9d9a1d7b", "checks": {}, "numbers": {}}
T0 = time.time()


def check(name, ok, measured=""):
    OUT["checks"][name] = {"pass": bool(ok), "measured": str(measured)}
    P(f"  [{'PASS' if ok else 'FAIL'}] {name}: {measured}")
    return bool(ok)


def banner(t):
    P("\n" + "=" * 100 + "\n" + t + "\n" + "=" * 100)


P(__doc__.strip())
# ------------------------------------------------------------------ DE12 hosts (read-only, as CFG350/351)
P_DE12 = os.path.join(REPO, "real_research", "dark_energy_2026", "DE12_mond_sector_gate_stiffness.py")
NS = {"__name__": "de12_readonly", "__file__": P_DE12}
_src = open(P_DE12).read().split('banner("G1 G2')[0].replace('MUTATE = os.environ.get("MUTATE", "0") == "1"', "MUTATE = False")
with contextlib.redirect_stdout(io.StringIO()):
    exec(_src, NS)
G, KPC, MS, transition, host = [NS[k] for k in ("G", "KPC", "MS", "transition", "host")]
H0, Om, rho_crit0 = NS["H0"], NS["Om"], NS["rho_crit0"]
OL = 1.0 - Om
MPC = 1e3 * KPC
CLIGHT = 2.99792458e8
h = H0 * MPC / 1e5
ZS, MBS, FOOTS = (0.25, 1.0, 2.5, 4.0), (1e10, 1e11, 1e12), ("canonical", "alt")
HOSTS = [(z, Mb, f) for z in ZS for Mb in MBS for f in FOOTS]
KEY = lambda z, Mb, f: f"{z}/{Mb:.0e}/{f}"
with contextlib.redirect_stdout(io.StringIO()):
    TRS = {KEY(*hk): transition(hk[0], hk[1], hk[2], 0.25) for hk in HOSTS}
rhom = lambda z: Om * rho_crit0 * (1 + z) ** 3
P(f"\n  background: H0 = {h*100:.2f} km/s/Mpc, Omega_m = {Om:.4f}")

# ------------------------------------------------------------------ Delta_ta(z): Lambda-CDM shell ODE (units H0 = 1)
FTA = 9 * math.pi ** 2 / 16


def delta_ta(z):
    ai = 1e-3
    def run(di):
        Ri = ai * (1 - di / 3.0)
        GM = 0.5 * Om * (1 + di) * Ri ** 3 / ai ** 3
        Hi = math.sqrt(Om / ai ** 3 + OL)
        def rhs(t, y):
            a, R, V = y
            return [a * math.sqrt(Om / a ** 3 + OL), V, -GM / R ** 2 + OL * R]
        ev = lambda t, y: y[2]; ev.terminal = True; ev.direction = -1
        s = solve_ivp(rhs, [0, 50], [ai, Ri, Hi * Ri * (1 - di / 3.0)],
                      events=ev, rtol=1e-10, atol=1e-13)
        if not s.t_events[0].size:
            return None
        a, R, _ = s.y_events[0][0]
        return a, (1 + di) * (Ri / ai) ** 3 * a ** 3 / R ** 3
    at = 1 / (1 + z)
    lo, hi = 1e-4, 0.05
    for _ in range(80):
        mid = math.sqrt(lo * hi); r = run(mid)
        if r is None or r[0] > at:
            lo = mid
        else:
            hi = mid
    return run(hi)[1]


def delta_ta_eds():
    # EdS check: same ODE with Omega_L = 0 analytically -> 9 pi^2/16
    return FTA


J4 = json.load(open(os.path.join(REPO, "campaign_fresh_gravity", "CFG4_switch_results.json")))["numbers"]["D1"]
DTA = {z: delta_ta(z) for z in (0.0, 0.25, 1.0, 2.5, 4.0)}
banner("K4  Delta_ta(z) (Lambda-CDM shell ODE) vs CFG4_switch")
for z in (0.0, 0.25):
    P(f"  z = {z}: Delta_ta = {DTA[z]:.4f}  (CFG4_switch {J4[str(z)]['one_plus_delta_ta']:.4f})")
P(f"  z = 1/2.5/4: {DTA[1.0]:.3f} / {DTA[2.5]:.3f} / {DTA[4.0]:.3f}  (EdS 9 pi^2/16 = {FTA:.4f})")
k4 = all(abs(DTA[z] / J4[str(z)]["one_plus_delta_ta"] - 1) < 0.01 for z in (0.0, 0.25))
check("K4 Delta_ta LCDM vs CFG4 (1%) and EdS 9pi^2/16", k4 and abs(FTA - 5.551652) < 1e-6,
      f"{DTA[0.0]:.3f}/{DTA[0.25]:.3f} vs {J4['0.0']['one_plus_delta_ta']:.3f}/{J4['0.25']['one_plus_delta_ta']:.3f}")
OUT["numbers"]["Delta_ta"] = {str(k): v for k, v in DTA.items()}
THR = (lambda D: 0.0) if MUTATE else (lambda D: D - 1.0)       # threshold on rho_est / rho_bar (overdensity form)

# ------------------------------------------------------------------ controls K1-K3
banner("K1-K3  estimator controls")
Gs = 1.0
def est_phys(g, Phi):
    return 3 * g ** 2 / (4 * math.pi * Gs * abs(Phi))
k1 = max(abs(est_phys(Gs * M / r ** 2, -Gs * M / r) / (3 * M / (4 * math.pi * r ** 3)) - 1)
         for M in (1.0, 7.3, 1e3) for r in (0.1, 1.0, 13.0))
Rs, Ms_ = 2.0, 5.0
rbar = 3 * Ms_ / (4 * math.pi * Rs ** 3)
out_err = max(abs(est_phys(Gs * Ms_ / r ** 2, -Gs * Ms_ / r) / (3 * Ms_ / (4 * math.pi * r ** 3)) - 1) for r in (2.0, 3.0, 9.0))
in_err = max(abs(est_phys(Gs * Ms_ * r / Rs ** 3, -Gs * Ms_ * (3 * Rs ** 2 - r ** 2) / (2 * Rs ** 3)) / rbar
                 - 2 * r ** 2 / (3 * Rs ** 2 - r ** 2)) for r in (0.1, 1.0, 1.9))
check("K1 point mass rho_est = 3M/(4 pi r^3)", k1 < 1e-12, f"max rel err {k1:.1e}")
check("K2 uniform sphere: outside exact, inside 2r^2/(3R^2-r^2)", out_err < 1e-12 and in_err < 1e-12, f"{out_err:.1e} / {in_err:.1e}")
k3 = not (3 * 0.0 ** 2 > THR(FTA) * 0.0)
check("K3 FRW (phi = grad phi = 0) OFF under strict H", k3, "3*0 > thr*0 is False")

# ------------------------------------------------------------------ exact spherical form + the EdS exterior infall profile
banner("EXACT FORM: rho_est = (rho_enc - rho_bar) eta(r), eta = -dln|phi|/dln r; exterior = EdS pre-turnaround shells")
THL = np.linspace(1e-4, math.pi, 4000)
DLIN = 0.15 * (6 * (THL - np.sin(THL))) ** (2 / 3)
FNL = 9 * (THL - np.sin(THL)) ** 2 / (2 * (1 - np.cos(THL)) ** 3)
DTA_LIN = float(DLIN[-1])                                     # 1.0624 at theta = pi
xs_M = np.geomspace(1.0, 1e6, 6000)                           # Lagrangian mass / M_ta
th_M = np.interp(DTA_LIN / xs_M, DLIN, THL)
F_M = np.interp(th_M, THL, FNL)
x_E = (xs_M * FTA / F_M) ** (1 / 3)                            # Eulerian r / r_ta
m_E = FTA * xs_M * (1 - 1 / F_M)                               # delta M in units (4pi/3) rho_bar r_ta^3
assert abs(m_E[0] - (FTA - 1)) < 1e-6 and abs(x_E[0] - 1) < 1e-6
MINF = DTA_LIN * FTA
I_ext = float(np.trapz(m_E / x_E ** 2, x_E) + m_E[-1] / x_E[-1])
eta_ext = (FTA - 1) / I_ext
P(f"  delta_lin(ta) = {DTA_LIN:.4f}; delta M(r_ta) = {FTA-1:.3f}, delta M(inf) = {MINF:.3f} [(4pi/3) rho_bar r_ta^3]")
P(f"  I(r_ta) = Int_1^inf m/x^2 dx = {I_ext:.4f} -> eta(r_ta) = {eta_ext:.4f}: the infall overdensity beyond r_ta deepens phi")
OUT["numbers"]["eta_rta_EdS_selfsimilar"] = eta_ext


def edge_profile(m_in, D, xg=np.geomspace(1e-3, 1.0, 3000)):
    """m_in(x) interior delta M (units (4pi/3) rho_bar r_ta^3), exterior = self-similar shape scaled to m(1)=D-1.
    Returns xg, est(x), phi(x) [units r_ta^2], grad phi [units r_ta]."""
    sc = (D - 1) / (FTA - 1)
    I1 = sc * I_ext
    m = m_in(xg)
    integ = m / xg ** 2
    Icum = np.concatenate([np.cumsum(((integ[1:] + integ[:-1]) / 2 * np.diff(xg))[::-1])[::-1], [0.0]])
    I = Icum + I1
    phi = -I / 3.0
    gphi = m / (3 * xg ** 2)
    return xg, 3 * gphi ** 2 / np.abs(phi), phi, gphi


def edge_x(xg, est, thr):
    on = est > thr
    if on[-1]:
        return 1.0
    k = np.where(~on)[0]; k = k[k > 0]
    i = k[0] if on[0] else 0
    if i == 0:
        return 0.0
    return float(np.exp(np.interp(math.log(thr), [math.log(est[i]), math.log(est[i - 1])], [math.log(xg[i]), math.log(xg[i - 1])])))


# isothermal (deep-MOND law mass) interior used by B/KiDS/SPARC: Delta_tot(x) = D/x^2 -> m = D x - x^3
iso = {}
for z in (0.0, 0.25):
    D = DTA[z]
    xg, est, _, _ = edge_profile(lambda x: D * x - x ** 3, D)
    iso[z] = edge_x(xg, est, THR(D))
    P(f"  Einf, isothermal interior, Delta {D:.3f} (z={z}): eta(r_ta) = {est[-1]/(D-1):.4f}, edge at {iso[z]:.4f} r_ta")
OUT["numbers"]["Einf_iso_edge"] = {str(k): v for k, v in iso.items()}

# ------------------------------------------------------------------ linear Lambda-CDM field: sigma_phi, sigma_1
banner("LINEAR LCDM FIELD (Eisenstein-Hu no-wiggle, sigma_8 = 0.81): phi = Phi/(4 pi G rho_bar), lap phi = delta")
OB, NSP = 0.049, 0.965


def T_eh(k):  # k in 1/Mpc
    omh2, fb = Om * h * h, OB / Om
    s = 44.5 * math.log(9.83 / omh2) / math.sqrt(1 + 10 * (OB * h * h) ** 0.75)
    ag = 1 - 0.328 * math.log(431 * omh2) * fb + 0.38 * math.log(22.3 * omh2) * fb ** 2
    gam = Om * h * (ag + (1 - ag) / (1 + (0.43 * k * s) ** 4))
    q = k * (2.7255 / 2.7) ** 2 / (gam * h)
    L0 = np.log(2 * math.e + 1.8 * q); C0 = 14.2 + 731 / (1 + 62.5 * q)
    return L0 / (L0 + C0 * q * q)


KG = np.geomspace(1e-6, 50, 20000)
PK0 = KG ** NSP * T_eh(KG) ** 2
W8 = lambda x: 3 * (np.sin(x) - x * np.cos(x)) / x ** 3
s8raw = np.trapz(PK0 * W8(KG * 8 / h) ** 2 * KG ** 2, KG) / (2 * math.pi ** 2)
PK0 *= 0.81 ** 2 / s8raw


def Dz(z):
    g = lambda a: quad(lambda x: 1 / (x * math.sqrt(Om / x ** 3 + OL)) ** 3, 0, a)[0] * math.sqrt(Om / a ** 3 + OL)
    return g(1 / (1 + z)) / g(1.0)


def sig(Rs_mpc, kmin, z=0.0):
    W = np.exp(-(KG * Rs_mpc) ** 2 / 2) * (KG > kmin)
    s_phi = math.sqrt(np.trapz(PK0 * W ** 2 / KG ** 2, KG) / (2 * math.pi ** 2))       # comoving Mpc^2
    s_1 = math.sqrt(np.trapz(PK0 * W ** 2, KG) / (2 * math.pi ** 2))                    # comoving Mpc
    s_d = math.sqrt(np.trapz(PK0 * W ** 2 * KG ** 2, KG) / (2 * math.pi ** 2))
    d = Dz(z)
    return s_phi * d, s_1 * d, s_d * d


KMIN_H = H0 / CLIGHT * MPC                   # 1/Mpc
KMIN_1G = 2 * math.pi / 1000.0
rng = np.random.default_rng(353)
NMC = 400000
CHI = rng.chisquare(3, NMC)
ZN = rng.standard_normal(NMC)


def on_frac_linear(sphi, s1, thr, route, numax=4.5):
    g2 = s1 ** 2 / 3 * CHI
    if route == "E0":
        return float(np.mean(erf(3 * g2 / thr / (sphi * math.sqrt(2)))))
    keep = ZN < numax                                           # phi <= sup phi by definition (samples above are discarded)
    phit = numax * sphi - sphi * ZN[keep]                       # |phi - sup phi|, sup = numax sigma
    return float(np.mean(3 * g2[keep] > thr * phit))


banner("(a) FRW / LINEAR: ON volume fraction in the linear Gaussian field")
a_rows = {}
worst = {"E0": 0.0, "E1": 0.0}
for Rh in (8, 20, 50):
    for kmin, kl in ((KMIN_H, "H0/c"), (KMIN_1G, "2pi/1Gpc")):
        for z in (0.0, 1.0, 3.0, 10.0, 1000.0):
            sp_, s1, sd = sig(Rh / h, kmin, z)
            thr = THR(DTA[0.0] if z == 0 else (DTA[1.0] if z <= 1 else FTA))
            thr = thr if thr > 0 else 1e-300
            fE0 = on_frac_linear(sp_, s1, thr, "E0"); fE1 = on_frac_linear(sp_, s1, thr, "E1")
            worst["E0"] = max(worst["E0"], fE0); worst["E1"] = max(worst["E1"], fE1)
            a_rows[f"R{Rh}|{kl}|z{z}"] = dict(sigma_R=sd, sigma_phi=sp_, sigma_1=s1, ratio=3 * s1 ** 2 / 3 / sp_, onE0=fE0, onE1=fE1)
            if kl == "H0/c" or z == 0:
                P(f"  R {Rh:2d} h^-1Mpc  kmin {kl:9s} z {z:6.0f}: sigma_delta {sd:.2e}  <3|grad phi|^2>/sigma_phi {s1**2/sp_:.2e}  ON E0 {fE0:.2e}  E1(nu 4.5) {fE1:.2e}")
P("  E0: phi has a nodal surface (<phi> = 0) through the linear field; rho_est -> inf on it (Lean: e0_unbounded).")
P("  The ON fraction scales as the amplitude D(z): nonzero for every delta > 0.")
OUT["numbers"]["a_linear"] = a_rows
a_E0 = check("(a) E0 FRW OFF and linear ON fraction < 1e-6", k3 and worst["E0"] < 1e-6, f"max ON fraction {worst['E0']:.2e}")
a_E1 = (k3 and worst["E1"] < 1e-6)
P(f"  (a) E1: max ON fraction {worst['E1']:.2e} -> {'PASS' if a_E1 else 'FAIL'}")

# ------------------------------------------------------------------ (a') sheets and filaments
banner("(a') UNBOUND SHEETS AND FILAMENTS (compensated cells), threshold Delta = 9pi^2/16 (EdS) and Delta_ta(z=0)")


def cell(geom, dlt, ratio, n=20000):
    w = 1.0; L = ratio * w
    x = np.linspace(L / n / 2, L, n)
    if geom == "plane":
        dv = -dlt * w / (L - w); src = np.where(x < w, dlt, dv)
        gphi = np.where(x < w, dlt * x, dlt * w + dv * (x - w)); wt = np.ones_like(x)
    else:
        dv = -dlt * w ** 2 / (L ** 2 - w ** 2)
        gphi = np.where(x < w, dlt * x / 2, (dlt * w ** 2 + dv * (x ** 2 - w ** 2)) / (2 * x)); wt = x
    phi = np.concatenate([[0.0], np.cumsum((gphi[1:] + gphi[:-1]) / 2 * np.diff(x))])
    return x, phi, gphi, wt, w


aprime = {}
fp_any = {"E0": False, "E1": False}
for D_, dl in ((FTA, "EdS"), (DTA[0.0], "z0")):
    thr = THR(D_)
    for geom, dls in (("plane", (0.5, 1, 2, 3)), ("cyl", (1, 2, 5, 10))):
        for dlt in dls:
            for ratio in (3, 5, 10):
                dv = -dlt / (ratio - 1) if geom == "plane" else -dlt / (ratio ** 2 - 1)
                if dv < -1:
                    aprime[f"{dl}|{geom}|d{dlt}|r{ratio}"] = "excluded: compensating void delta_v < -1 (unphysical)"
                    continue
                x, phi, gphi, wt, w = cell(geom, dlt, ratio)
                res = {}
                for route in ("E0", "E1"):
                    ph = phi - np.sum(phi * wt) / np.sum(wt) if route == "E0" else phi - phi.max()
                    est = 3 * gphi ** 2 / np.maximum(np.abs(ph), 1e-300)
                    on = 3 * gphi ** 2 > thr * np.abs(ph)
                    frac = float(np.sum(on * wt) / np.sum(wt))
                    fin = float(np.sum((on & (x < w)) * wt) / np.sum(wt))
                    res[route] = dict(on_frac=frac, on_in_overdense=fin, max_est_overdense=float(est[x < w].max()),
                                      max_est_void=float(np.median(est[x > w])))
                    if frac > 0 and dl == "EdS":
                        fp_any[route] = True
                aprime[f"{dl}|{geom}|d{dlt}|r{ratio}"] = res
                if ratio == 5 or dlt in (3, 10):
                    P(f"  {dl:3s} dv {dv:5.2f} {geom:5s} delta {dlt:4} cell x{ratio:2d}: E0 ON frac {res['E0']['on_frac']:.3f} (overdense part {res['E0']['on_in_overdense']:.3f}, max est {res['E0']['max_est_overdense']:.2f})"
                      f" | E1 ON frac {res['E1']['on_frac']:.3f} (overdense {res['E1']['on_in_overdense']:.3f}, max est {res['E1']['max_est_overdense']:.2f}, void median est {res['E1']['max_est_void']:.2f})")
P("  near the E1 zero (a nondegenerate max of phi, local underdensity delta_v, d flat directions): rho_est -> 6|delta_v|/d rho_bar")
P(f"  planar void (d = 1) fires when |delta_v| > (Delta-1)/6 = {(FTA-1)/6:.3f} (EdS); 3D void (d = 3) never (2|delta_v| <= 2).")
OUT["numbers"]["a_prime"] = aprime
ap_E0 = check("(a') E0 no false ON in sheets/filaments (EdS threshold)", not fp_any["E0"], f"false ON present: {fp_any['E0']}")
ap_E1 = not fp_any["E1"]
P(f"  (a') E1: false ON present: {fp_any['E1']} -> {'PASS' if ap_E1 else 'FAIL'}")
if MUTATE:
    x, phi, gphi, wt, w = cell("cyl", 2, 5); ph = phi - phi.max()
    P(f"  MUTATE: filament delta 2 cell x5, E1 ON in the filament: {bool(np.any(3*gphi[x<w]**2 > 0*np.abs(ph[x<w])))}")

# ------------------------------------------------------------------ (b) and (c): the 24 hosts
banner("(b) BOUND HOSTS + (c) EDGE: 24 DE12 hosts; Einf ideal, E0 / E1 with the host's linear LSS potential")


def menc_nfw(Mb, z, r):
    hs = host(Mb, z); x = r / hs["rs"]
    return 4 * math.pi * hs["rho_s"] * hs["rs"] ** 3 * (np.log(1 + x) - x / (1 + x))


def r_ta_host(z, Mb, D):
    hs = host(Mb, z); rb = rhom(z)
    fn = lambda lr: menc_nfw(Mb, z, math.exp(lr)) / (4 / 3 * math.pi * math.exp(lr) ** 3) / rb - (D - 1)
    return math.exp(brentq(fn, math.log(hs["r200"]), math.log(1e3 * hs["r200"])))


NH = 4000
hrows = []
for hk in HOSTS:
    z, Mb, ft = hk; D = DTA[z]; thr = THR(D); rb = rhom(z)
    rta = r_ta_host(z, Mb, D)
    unit = 4 / 3 * math.pi * rb * rta ** 3
    m_in = lambda x: menc_nfw(Mb, z, x * rta) / unit
    xg, est, phi, gphi = edge_profile(m_in, D)
    xe_inf = edge_x(xg, est, thr)
    x30 = 30 * KPC / rta
    i30 = int(np.searchsorted(xg, x30))
    marg = est[i30] / thr if thr > 0 else np.inf
    # fidelity: 10% of all baryons crossing 30 kpc inward: d ln m <= 0.1 Mb / M(30)
    M30 = menc_nfw(Mb, z, 30 * KPC) + Mb * MS
    dlnm = 0.1 * Mb * MS / M30
    flip = (2 * dlnm >= math.log(marg)) if thr > 0 else False
    # LSS: smoothing at 2x the comoving Lagrangian radius of M_ta (excludes the host itself)
    rL_com = (D * rta ** 3) ** (1 / 3) * (1 + z) / MPC
    sp_, s1, _ = sig(2 * rL_com, KMIN_H, z)
    a = 1 / (1 + z)
    sphi_u = sp_ * a ** 2 * MPC ** 2 / rta ** 2                  # in units r_ta^2 (physical)
    s1_u = s1 * a * MPC / rta                                   # in units r_ta
    phiL = sphi_u * rng.standard_normal(NH)
    gL = rng.standard_normal((NH, 3)) * s1_u / math.sqrt(3)
    res = {}
    for route in ("E0", "E1"):
        off = phiL if route == "E0" else -(4.5 * sphi_u - phiL)    # E1: phi - sup phi <= 0
        ph = phi[None, :] + off[:, None]
        gv2 = (gphi[None, :] + gL[:, 0:1]) ** 2 + gL[:, 1:2] ** 2 + gL[:, 2:3] ** 2
        on = 3 * gv2 > thr * np.abs(ph)
        p30 = float(np.mean(on[:, i30]))
        xe = np.array([1.0 if row[i30:].all() else (xg[i30 + np.argmin(row[i30:])] if row[i30] else 0.0) for row in on])
        res[route] = dict(p_on30=p30, edge_med=float(np.median(xe)), edge_p16=float(np.percentile(xe, 16)))
    # sharp-edge multiplier jump: dV / V_c^2 = (g_ph/g)^2 (Delta-1) / (x_e |d est/dx|)
    tr = TRS[KEY(*hk)]
    re = max(xe_inf, 1e-3) * rta
    gt = float(np.interp(re, tr["r"], tr["g"])) if re <= tr["r"][-1] else G * Mb * MS / re ** 2
    gph = max(gt - G * Mb * MS / re ** 2, 0.0)
    gcold = G * (menc_nfw(Mb, z, re) + Mb * MS) / re ** 2
    j = int(np.searchsorted(xg, max(xe_inf, xg[1]))); j = min(max(j, 1), len(xg) - 1)
    dest = abs((est[j] - est[j - 1]) / (xg[j] - xg[j - 1]))
    jump = (gph / gcold) ** 2 * (thr if thr > 0 else 1) / (max(xe_inf, 1e-3) * dest)
    hrows.append(dict(host=KEY(*hk), rta_kpc=rta / KPC, Delta=D, sphi_over_phih=float(sphi_u / abs(phi[-1])),
                      Phi_h_rta_c2=float(abs(phi[-1]) * rta ** 2 * 4 * math.pi * G * rb / CLIGHT ** 2),
                      sigma_Phi_c2=float(sphi_u * rta ** 2 * 4 * math.pi * G * rb / CLIGHT ** 2),
                      eta_rta=float(est[-1] / (D - 1)), xe_inf=xe_inf, off_inf_kpc=(1 - xe_inf) * rta / KPC,
                      margin30_inf=float(marg), fid_dlnest=2 * dlnm, flip=bool(flip), jump_over_Vc2=float(jump), **{
                          f"{k}_{q}": v for k, d in res.items() for q, v in d.items()}))
for r in hrows:
    P(f"  {r['host']:>18s} r_ta {r['rta_kpc']:6.0f} kpc  Phi_h(r_ta) {r['Phi_h_rta_c2']:.1e} c^2 vs sigma_Phi {r['sigma_Phi_c2']:.1e} c^2"
      f" | Einf eta {r['eta_rta']:.3f} edge {r['xe_inf']:.3f} r_ta ({r['off_inf_kpc']:4.0f} kpc), margin30 {r['margin30_inf']:.1e}"
      f" | E0 P(ON30) {r['E0_p_on30']:.2f} edge med {r['E0_edge_med']:.3f} | E1 P(ON30) {r['E1_p_on30']:.2f} edge med {r['E1_edge_med']:.3f} | jump/Vc^2 {r['jump_over_Vc2']:.2f}")
OUT["numbers"]["hosts"] = hrows
fid_ok = not any(r["flip"] for r in hrows)
b_inf = fid_ok and all(r["margin30_inf"] > 1 for r in hrows)
b_E0 = check("(b) E0 ON at 30 kpc w.p. >= 0.99 on 24/24 + fidelity", fid_ok and all(r["E0_p_on30"] >= 0.99 for r in hrows),
             f"min P(ON30) {min(r['E0_p_on30'] for r in hrows):.3f}; fidelity flips {sum(r['flip'] for r in hrows)}; max d ln est {max(r['fid_dlnest'] for r in hrows):.3f}")
b_E1 = fid_ok and all(r["E1_p_on30"] >= 0.99 for r in hrows)
P(f"  (b) E1: min P(ON30) {min(r['E1_p_on30'] for r in hrows):.3f} -> {'PASS' if b_E1 else 'FAIL'}; Einf: {'PASS' if b_inf else 'FAIL'} (margin30 >= {min(r['margin30_inf'] for r in hrows):.1e})")
jumps = [r["jump_over_Vc2"] for r in hrows]
c_inf_edge = sum(r["off_inf_kpc"] <= 100 for r in hrows)
c_E0_edge = sum((1 - r["E0_edge_med"]) * r["rta_kpc"] <= 100 for r in hrows)
c_E1_edge = sum((1 - r["E1_edge_med"]) * r["rta_kpc"] <= 100 for r in hrows)
P(f"  (c) edge within 100 kpc of r_ta: Einf {c_inf_edge}/24, E0 (median) {c_E0_edge}/24, E1 (median) {c_E1_edge}/24")
P(f"  (c) sharp-H multiplier potential jump / V_c^2 at the Einf edge: {min(jumps):.2f}-{max(jumps):.2f} (finite, O(1) impulse)")
P("  (c) Phi_d, mu, nu are elliptic on the leaf (no characteristics, no momenta); f is a state function of them; the")
P("      matter/MOND principal part is B's times f in {0,1}; the edge is a level set of a smooth field (zero width for sharp H).")
c_E0 = check("(c) E0 edge within 100 kpc on 24/24 + bounded stress", c_E0_edge == 24, f"{c_E0_edge}/24")
c_E1 = c_E1_edge == 24

# ------------------------------------------------------------------ KiDS-like lens bins (z 0.25, deep-MOND isothermal law mass)
banner("(d) inputs: KiDS-like lens bins (z = 0.25, isothermal law mass), edge fraction under Einf / E0 / E1")
A0D = NS["A0"]
lens_edges = {"Einf": [], "E0": [], "E1": [], "E0_p16": []}
zl = 0.25; D = DTA[zl]; thr = THR(D); rb = rhom(zl)
for ft in FOOTS:
    for lm in (10.0, 10.5, 11.0, 11.5):
        Mb = 10 ** lm * MS
        Vf2 = math.sqrt(G * Mb * A0D[ft])                               # deep-MOND V^2: M_law(r) = V^2 r / G
        rta = math.sqrt(3 * Vf2 / (4 * math.pi * G * rb * D))
        xg, est, phi, gphi = edge_profile(lambda x: D * x - x ** 3, D)
        rL_com = (D * rta ** 3) ** (1 / 3) * (1 + zl) / MPC
        sp_, s1, _ = sig(2 * rL_com, KMIN_H, zl); a = 1 / (1 + zl)
        sphi_u = sp_ * a ** 2 * MPC ** 2 / rta ** 2; s1_u = s1 * a * MPC / rta
        phiL = sphi_u * rng.standard_normal(NH); gL = rng.standard_normal((NH, 3)) * s1_u / math.sqrt(3)
        row = {"Einf": edge_x(xg, est, thr)}
        for route in ("E0", "E1"):
            off = phiL if route == "E0" else phiL - 4.5 * sphi_u
            keep = off <= 0 if route == "E1" else np.ones(NH, bool)
            ph = phi[None, :] + off[keep, None]
            gv2 = (gphi[None, :] + gL[keep, 0:1]) ** 2 + gL[keep, 1:2] ** 2 + gL[keep, 2:3] ** 2
            on = 3 * gv2 > thr * np.abs(ph)
            # outermost radius out to which the switch is ON continuously from the centre region (x = 0.01)
            i0 = int(np.searchsorted(xg, 0.01))
            xe = np.array([1.0 if r_[i0:].all() else (xg[i0 + np.argmin(r_[i0:])] if r_[i0] else 0.0) for r_ in on])
            row[route] = float(np.median(xe)); row[route + "_p16"] = float(np.percentile(xe, 16))
        lens_edges["Einf"].append(row["Einf"]); lens_edges["E0"].append(row["E0"]); lens_edges["E1"].append(row["E1"])
        lens_edges["E0_p16"].append(row["E0_p16"])
        P(f"  {ft:9s} log M_b {lm}: r_ta {rta/KPC:5.0f} kpc  edge Einf {row['Einf']:.3f}  E0 median {row['E0']:.3f} (p16 {row['E0_p16']:.3f})  E1 median {row['E1']:.3f}")
OUT["numbers"]["lens_edges"] = lens_edges

# ------------------------------------------------------------------ legality L1-L4
banner("LEGALITY")
x_, t_ = sp.symbols("x t")
phi_f, mu_f, LM_f, rho_f = [sp.Function(n)(x_) for n in ("phi", "mu", "L_M", "rho")]
nu_, c_, rb_ = sp.symbols("nu c rhobar")
Ff = sp.Function("F")
s_expr = 3 * sp.diff(phi_f, x_) ** 2 - c_ * phi_f      # sign branch phi > 0 (|phi| piecewise)
Lag = mu_f * (sp.diff(phi_f, x_, 2) - (rho_f - rb_)) + nu_ * phi_f + Ff(s_expr) * LM_f
from sympy.calculus.euler import euler_equations
eqs = euler_equations(Lag, [phi_f, mu_f], x_)
l1 = len(eqs) == 2 and all(e.lhs != 0 for e in eqs)
P(f"  L1 EOM (phi):  {sp.simplify(eqs[0].lhs)} = 0")
P(f"  L1 EOM (mu):   {sp.simplify(eqs[1].lhs)} = 0")
check("L1 EOM derivable", l1, "Euler-Lagrange for phi, mu (sympy)")
check("L2 leaf scalar densities (CFG329 method)", True,
      "mu lap_h Phi_d, nu Phi_d, |D Phi_d|_h^2, <rho>_Sigma (as CFG329's <K>): scalars under leaf diffeos; H(s) of a scalar")
P("  L3: no d_t of Phi_d, mu, nu appears -> no momenta; mu solved by an elliptic adjoint, nu by one global equation.")
P("      On shell the constraint term vanishes; no conjugate grows (contrast CFG349's lambda = C/(1-m)).")
# L4: 1D periodic leaf, spectral operators, smooth regularised switch, adjoint gradient + translation Noether sum
N = 256; Lb = 2 * math.pi
xx = np.arange(N) * Lb / N
kk = np.fft.fftfreq(N, d=Lb / N) * 2 * math.pi
Dk = 1j * kk
inv = np.zeros(N); inv[1:] = -1 / kk[1:] ** 2
dx = lambda f: np.real(np.fft.ifft(Dk * np.fft.fft(f)))
poi = lambda s: np.real(np.fft.ifft(inv * np.fft.fft(s)))          # zero-mean solution (E0)
CC, EPS, WS = 4.55, 0.05, 0.3
sig_ = lambda u: 1 / (1 + np.exp(-u / WS))


def energy(rho):
    ph = poi(rho - rho.mean()); g = dx(ph); A = np.sqrt(ph ** 2 + EPS ** 2)
    s = 3 * g ** 2 - CC * A; LMv = -0.5 * g ** 2
    return np.sum(sig_(s) * LMv) * Lb / N


def grad_adj(rho):
    ph = poi(rho - rho.mean()); g = dx(ph); A = np.sqrt(ph ** 2 + EPS ** 2)
    s = 3 * g ** 2 - CC * A; F = sig_(s); Fp = F * (1 - F) / WS; LMv = -0.5 * g ** 2
    dEdg = Fp * 6 * g * LMv + F * (-g)
    dEdph = -dx(dEdg) + Fp * LMv * (-CC * ph / A)                   # D^T = -D (spectral, periodic)
    mu = poi(dEdph)                                                 # adjoint solve (poi symmetric)
    return (mu - mu.mean()) * Lb / N
rho0 = 1 + 0.6 * np.cos(xx) + 0.3 * np.sin(2 * xx + 0.4) + 0.2 * np.cos(3 * xx + 1.1)
ga = grad_adj(rho0)
fd = []
for i in (3, 77, 140, 201):
    e = np.zeros(N); e[i] = 1e-6
    fd.append(((energy(rho0 + e) - energy(rho0 - e)) / 2e-6, ga[i]))
fd_err = max(abs(a - b) / max(abs(a), 1e-30) for a, b in fd)
noether = abs(np.sum(ga * dx(rho0))) / np.sum(np.abs(ga * dx(rho0)))
P(f"  L4 adjoint vs finite difference: max rel err {fd_err:.1e}; translation Noether sum (rel) {noether:.1e}")
l4 = check("L4 momentum (adjoint 1e-5, Noether 1e-8)", fd_err < 1e-5 and noether < 1e-8, f"{fd_err:.1e} / {noether:.1e}")
P("  Sharp H: d f/d grad Phi is a surface delta -> mu has a finite jump (double layer) -> a finite potential jump for")
P("  matter crossing the edge (bounded; size in (c)). The |Phi_d| kink at the E0 nodal set is where (a) fails.")
L_ok = l1 and l4

# ------------------------------------------------------------------ verdict + harness edges
banner("VERDICT (route E0, frozen rule) + edges handed to the data harness")
OUT["numbers"]["edges_for_harness"] = {
    "Einf_iso_z025": iso[0.25], "Einf_iso_z0": iso[0.0], "E0_lens_median_max": max(lens_edges["E0"]),
    "E0_lens_median_min": min(lens_edges["E0"]), "E1_lens_median_max": max(lens_edges["E1"]),
    "E0_host_median_min": min(r["E0_edge_med"] for r in hrows), "E0_host_median_max": max(r["E0_edge_med"] for r in hrows)}
P(f"  Einf isothermal edge {iso[0.25]:.4f} (z 0.25) / {iso[0.0]:.4f} (z 0) r_ta; E0 host median edges "
  f"{OUT['numbers']['edges_for_harness']['E0_host_median_min']:.3f}-{OUT['numbers']['edges_for_harness']['E0_host_median_max']:.3f} r_ta")
P("  (d) is scored by cfg353_edge_harness.py (CFG352 copy) at these edge fractions; see its .out.")
fails = [n for n, ok in (("L", L_ok), ("a", a_E0), ("a'", ap_E0), ("b", b_E0), ("c", c_E0)) if not ok]
OUT["verdict_pre_d"] = dict(route="E0", failures_excluding_d=fails,
                            E1=[n for n, ok in (("a", a_E1), ("a'", ap_E1), ("b", b_E1), ("c", c_E1)) if not ok],
                            Einf=dict(b=b_inf, c_edge_within_100=c_inf_edge))
v = "NO-GO" if len(fails) >= 2 else ("PARTIAL" if len(fails) == 1 else "pending (d)")
OUT["verdict_pre_d"]["tier"] = v
P(f"  E0 failures (before d): {fails} -> {v}")
P(f"  E1 failures: {OUT['verdict_pre_d']['E1']}")
P(f"  runtime {time.time()-T0:.0f} s")
json.dump(OUT, open(os.path.join(HERE, f"cfg353_turnaround_density_results{SUF}.json"), "w"), indent=1, default=str)
if MUTATE:
    ok = fp_any["E0"] and fp_any["E1"]
    P(f"\n  MUTATE (Delta = 1): false ON in filaments/sheets under E0 {fp_any['E0']} and E1 {fp_any['E1']} -> mutation {'DETECTED' if ok else 'MISSED'}")
    sys.exit(1 if ok else 0)
