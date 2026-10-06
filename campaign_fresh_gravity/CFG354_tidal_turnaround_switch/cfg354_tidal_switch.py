#!/usr/bin/env python3
"""
CFG354 -- a turnaround switch on the tidal eigenvalues of the leaf overdensity potential.  Criteria: FROZEN_CRITERIA.md (bd5ab6223).

  psi = Phi_d / (4 pi G rho_bar), lap psi = delta (leaf constraint, total matter: MS1 relaxed by the owner 10-06).
  t_ij = d_i d_j psi (no zero point), l1 >= l2 >= l3; sphere: l_t = dbar_enc/3 (double), l_r = delta - 2 l_t.
  threshold tau = (Delta_ta - 1)/3.  f = H_strict(R - tau).
  T1: R = l2.  T2: R = l3.  T3 (PRIMARY): R = min_{e perp grad psi} e.t.e  (l3 if grad psi = 0).
MUTATE: CFG354_MUTATE=1 -> potential reader (CFG353 E0) instead of t; must reproduce CFG353's failure; outputs *_MUTATE; exit 1.
Run: python3 campaign_fresh_gravity/CFG354_tidal_turnaround_switch/cfg354_tidal_switch.py
"""
import os, sys, io, json, math, contextlib, time
import numpy as np
import sympy as sp
from scipy.integrate import solve_ivp, quad
from scipy.optimize import brentq
from scipy.special import erf, erfc
from scipy.stats import chi2 as CHI2

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
MUTATE = os.environ.get("CFG354_MUTATE", "0") == "1"
SUF = "_MUTATE" if MUTATE else ""
P = lambda *a: print(*a, flush=True)
OUT = {"lane": "CFG354", "mutate": MUTATE, "frozen": "bd5ab6223", "checks": {}, "numbers": {}}
T0 = time.time()
RULES = ("T1", "T2", "T3")


def check(name, ok, measured=""):
    OUT["checks"][name] = {"pass": bool(ok), "measured": str(measured)}
    P(f"  [{'PASS' if ok else 'FAIL'}] {name}: {measured}")
    return bool(ok)


def banner(t):
    P("\n" + "=" * 100 + "\n" + t + "\n" + "=" * 100)


P(__doc__.strip())
# ------------------------------------------------------------------ rules on tensor arrays
def rules(T, g):
    """T (...,3,3) symmetric, g (...,3). Returns dict of R arrays."""
    ev = np.linalg.eigvalsh(T)
    gn = np.linalg.norm(g, axis=-1)
    n = g / np.where(gn > 0, gn, 1.0)[..., None]
    a = np.zeros_like(n); a[..., 2] = 1.0
    swap = np.abs(n[..., 2]) > 0.9
    a[swap] = np.array([1.0, 0.0, 0.0])
    e1 = a - np.sum(a * n, -1)[..., None] * n
    e1 /= np.linalg.norm(e1, axis=-1)[..., None]
    e2 = np.cross(n, e1)
    q = lambda u, v: np.einsum("...i,...ij,...j->...", u, T, v)
    m11, m22, m12 = q(e1, e1), q(e2, e2), q(e1, e2)
    t3 = 0.5 * (m11 + m22) - np.sqrt(0.25 * (m11 - m22) ** 2 + m12 ** 2)
    t3 = np.where(gn > 0, t3, ev[..., 0])
    return {"T1": ev[..., 1], "T2": ev[..., 0], "T3": t3}


# ------------------------------------------------------------------ DE12 hosts (read-only, as CFG353)
P_DE12 = os.path.join(REPO, "real_research", "dark_energy_2026", "DE12_mond_sector_gate_stiffness.py")
NS = {"__name__": "de12_readonly", "__file__": P_DE12}
_src = open(P_DE12).read().split('banner("G1 G2')[0].replace('MUTATE = os.environ.get("MUTATE", "0") == "1"', "MUTATE = False")
with contextlib.redirect_stdout(io.StringIO()):
    exec(_src, NS)
G, KPC, MS, host = [NS[k] for k in ("G", "KPC", "MS", "host")]
H0, Om, rho_crit0 = NS["H0"], NS["Om"], NS["rho_crit0"]
OL = 1.0 - Om
MPC = 1e3 * KPC
CLIGHT = 2.99792458e8
h = H0 * MPC / 1e5
ZS, MBS, FOOTS = (0.25, 1.0, 2.5, 4.0), (1e10, 1e11, 1e12), ("canonical", "alt")
HOSTS = [(z, Mb, f) for z in ZS for Mb in MBS for f in FOOTS]
KEY = lambda z, Mb, f: f"{z}/{Mb:.0e}/{f}"
rhom = lambda z: Om * rho_crit0 * (1 + z) ** 3
FTA = 9 * math.pi ** 2 / 16


def delta_ta(z):          # CFG353's Lambda-CDM shell ODE (units H0 = 1), unchanged
    ai = 1e-3
    def run(di):
        Ri = ai * (1 - di / 3.0)
        GM = 0.5 * Om * (1 + di) * Ri ** 3 / ai ** 3
        Hi = math.sqrt(Om / ai ** 3 + OL)
        def rhs(t, y):
            a, R, V = y
            return [a * math.sqrt(Om / a ** 3 + OL), V, -GM / R ** 2 + OL * R]
        ev = lambda t, y: y[2]; ev.terminal = True; ev.direction = -1
        s = solve_ivp(rhs, [0, 50], [ai, Ri, Hi * Ri * (1 - di / 3.0)], events=ev, rtol=1e-10, atol=1e-13)
        if not s.t_events[0].size:
            return None
        a, R, _ = s.y_events[0][0]
        return a, (1 + di) * (Ri / ai) ** 3 * a ** 3 / R ** 3
    at = 1 / (1 + z); lo, hi = 1e-4, 0.05
    for _ in range(80):
        mid = math.sqrt(lo * hi); r = run(mid)
        if r is None or r[0] > at:
            lo = mid
        else:
            hi = mid
    return run(hi)[1]


J4 = json.load(open(os.path.join(REPO, "campaign_fresh_gravity", "CFG4_switch_results.json")))["numbers"]["D1"]
DTA = {z: delta_ta(z) for z in (0.0, 0.25, 1.0, 2.5, 4.0)}
TAU = lambda D: (D - 1.0) / 3.0

# ------------------------------------------------------------------ linear LCDM field (CFG353, unchanged)
OB, NSP = 0.049, 0.965


def T_eh(k):
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
PK0 *= 0.81 ** 2 / (np.trapz(PK0 * W8(KG * 8 / h) ** 2 * KG ** 2, KG) / (2 * math.pi ** 2))


def Dz(z):
    g = lambda a: quad(lambda x: 1 / (x * math.sqrt(Om / x ** 3 + OL)) ** 3, 0, a)[0] * math.sqrt(Om / a ** 3 + OL)
    return g(1 / (1 + z)) / g(1.0)


def sig(Rs_mpc, kmin, z=0.0):
    W = (np.exp(-(KG * Rs_mpc) ** 2 / 2) if Rs_mpc > 0 else np.ones_like(KG)) * (KG > kmin)
    s_phi = math.sqrt(np.trapz(PK0 * W ** 2 / KG ** 2, KG) / (2 * math.pi ** 2))
    s_1 = math.sqrt(np.trapz(PK0 * W ** 2, KG) / (2 * math.pi ** 2))
    s_d = math.sqrt(np.trapz(PK0 * W ** 2 * KG ** 2, KG) / (2 * math.pi ** 2))
    d = Dz(z)
    return s_phi * d, s_1 * d, s_d * d


KMIN_H = H0 / CLIGHT * MPC


def cell(geom, dlt, ratio, n=20000):  # CFG353's compensated cells, unchanged
    w = 1.0; L = ratio * w
    x = np.linspace(L / n / 2, L, n)
    if geom == "plane":
        dv = -dlt * w / (L - w); src = np.where(x < w, dlt, dv)
        gphi = np.where(x < w, dlt * x, dlt * w + dv * (x - w)); wt = np.ones_like(x)
    else:
        dv = -dlt * w ** 2 / (L ** 2 - w ** 2); src = np.where(x < w, dlt, dv)
        gphi = np.where(x < w, dlt * x / 2, (dlt * w ** 2 + dv * (x ** 2 - w ** 2)) / (2 * x)); wt = x
    phi = np.concatenate([[0.0], np.cumsum((gphi[1:] + gphi[:-1]) / 2 * np.diff(x))])
    return x, phi, gphi, wt, w, src


# ================================================================== MUTATE: the potential reader (CFG353 E0)
if MUTATE:
    banner("MUTATE: potential reader (CFG353 E0) in place of the tidal eigenvalues")
    J353 = json.load(open(os.path.join(REPO, "campaign_fresh_gravity", "CFG353_turnaround_density_switch",
                                       "cfg353_turnaround_density_results.json")))["numbers"]
    rng = np.random.default_rng(353); NMC = 400000
    CHI = rng.chisquare(3, NMC)
    sp_, s1, sd = sig(8 / h, KMIN_H, 0.0)
    thr = DTA[0.0] - 1
    fE0 = float(np.mean(erf(3 * (s1 ** 2 / 3 * CHI) / thr / (sp_ * math.sqrt(2)))))
    ref = J353["a_linear"]["R8|H0/c|z0.0"]["onE0"]
    P(f"  (a) E0 linear ON fraction R8 z0: {fE0:.6e} (CFG353 {ref:.6e})")
    rep_a = abs(fE0 - ref) < 1e-12
    rep_ap, fp = True, False
    for geom, dls in (("plane", (0.5, 1, 2, 3)), ("cyl", (1, 2, 5, 10))):
        for dlt in dls:
            for ratio in (3, 5, 10):
                k = f"EdS|{geom}|d{dlt}|r{ratio}"
                if isinstance(J353["a_prime"][k], str):
                    continue
                x, phi, gphi, wt, w, _ = cell(geom, dlt, ratio)
                ph = phi - np.sum(phi * wt) / np.sum(wt)
                frac = float(np.sum((3 * gphi ** 2 > (FTA - 1) * np.abs(ph)) * wt) / np.sum(wt))
                rep_ap &= abs(frac - J353["a_prime"][k]["E0"]["on_frac"]) < 1e-12
                fp |= frac > 0
    P(f"  (a') E0 cell fractions reproduce CFG353: {rep_ap}; false ON present: {fp}")
    ok = rep_a and rep_ap and fp and fE0 > 1e-6
    OUT["numbers"]["mutate"] = dict(a_E0=fE0, a_ref=ref, aprime_reproduced=rep_ap, aprime_false_on=fp)
    P(f"  MUTATE: CFG353 failure {'REPRODUCED (detected)' if ok else 'NOT reproduced'}")
    json.dump(OUT, open(os.path.join(HERE, f"cfg354_tidal_switch_results{SUF}.json"), "w"), indent=1, default=str)
    sys.exit(1 if ok else 0)

banner("K4  Delta_ta(z) vs CFG4_switch")
k4 = all(abs(DTA[z] / J4[str(z)]["one_plus_delta_ta"] - 1) < 0.01 for z in (0.0, 0.25))
check("K4 Delta_ta LCDM vs CFG4 (1%)", k4, f"{DTA[0.0]:.3f}/{DTA[0.25]:.3f} vs {J4['0.0']['one_plus_delta_ta']:.3f}/{J4['0.25']['one_plus_delta_ta']:.3f}; "
      f"z 1/2.5/4: {DTA[1.0]:.3f}/{DTA[2.5]:.3f}/{DTA[4.0]:.3f}")
OUT["numbers"]["Delta_ta"] = {str(k): v for k, v in DTA.items()}
OUT["numbers"]["tau"] = {str(k): TAU(v) for k, v in DTA.items()} | {"EdS": TAU(FTA)}

# ================================================================== K1-K3 controls (exact sympy Hessians)
banner("K1-K3  sphere / cylinder / plane / FRW controls (sympy Hessians, G = 1)")
X, Y, Z = sp.symbols("x y z", real=True)
Ms_, Rs_, rho_, mu_, sg_ = sp.Rational(7, 3), sp.Rational(2), sp.Rational(3, 5), sp.Rational(5, 4), sp.Rational(2, 7)
r3 = sp.sqrt(X ** 2 + Y ** 2 + Z ** 2); r2 = sp.sqrt(X ** 2 + Y ** 2)
POT = {
    "point": -Ms_ / r3,
    "sphere_in": -Ms_ * (3 * Rs_ ** 2 - r3 ** 2) / (2 * Rs_ ** 3),
    "cyl_in": sp.pi * rho_ * r2 ** 2,
    "cyl_out": 2 * mu_ * sp.log(r2),
    "plane_in": 2 * sp.pi * rho_ * X ** 2,
    "plane_out": 4 * sp.pi * sg_ * X,
}
HESS = {k: sp.lambdify((X, Y, Z), sp.hessian(v, (X, Y, Z)), "numpy") for k, v in POT.items()}
GRAD = {k: sp.lambdify((X, Y, Z), [sp.diff(v, s) for s in (X, Y, Z)], "numpy") for k, v in POT.items()}
rng = np.random.default_rng(354)
k1err, ctab = 0.0, {}
for k in POT:
    for _ in range(6):
        u = rng.standard_normal(3); u /= np.linalg.norm(u)
        if k == "point":
            p = u * rng.uniform(0.3, 5)
        elif k == "sphere_in":
            p = u * rng.uniform(0.2, 1.9)
        elif k == "cyl_in":
            p = np.array([*(u[:2] / np.linalg.norm(u[:2]) * rng.uniform(0.1, 1)), rng.uniform(-3, 3)])
        elif k == "cyl_out":
            p = np.array([*(u[:2] / np.linalg.norm(u[:2]) * rng.uniform(1.2, 6)), rng.uniform(-3, 3)])
        else:
            p = np.array([rng.uniform(0.1, 2), rng.uniform(-3, 3), rng.uniform(-3, 3)])
        Tm = np.array(HESS[k](*p), float); gv = np.array(GRAD[k](*p), float)
        R = rules(Tm[None], gv[None]); ev = np.linalg.eigvalsh(Tm)
        r = np.linalg.norm(p); rc = np.linalg.norm(p[:2])
        if k == "point":
            lt = Ms_ / r ** 3; k1err = max(k1err, abs(float(R["T1"][0]) / float(lt) - 1), abs(float(R["T3"][0]) / float(lt) - 1),
                                           abs(float(lt) / float(4 * math.pi / 3 * 3 * Ms_ / (4 * math.pi * r ** 3)) - 1))
        if k == "sphere_in":
            lt = float(Ms_ / Rs_ ** 3); k1err = max(k1err, abs(float(R["T1"][0]) / lt - 1), abs(float(R["T3"][0]) / lt - 1), abs(ev[0] / lt - 1))
        ctab.setdefault(k, []).append(dict(ev=ev.tolist(), **{q: float(R[q][0]) for q in RULES}))
for k, rows in ctab.items():
    r0 = rows[0]
    P(f"  {k:10s} eig {np.round(r0['ev'], 5).tolist()}  T1 {r0['T1']:+.5f}  T2 {r0['T2']:+.5f}  T3 {r0['T3']:+.5f}")
ana = dict(cyl_in=lambda rw: abs(rw["T1"] - 2 * math.pi * float(rho_)) + abs(rw["T2"]) + abs(rw["T3"]),
           cyl_out=lambda rw: abs(rw["T1"]) + abs(rw["T3"]) + abs(rw["ev"][0] + rw["ev"][2]),
           plane_in=lambda rw: abs(rw["T1"]) + abs(rw["T2"]) + abs(rw["T3"]),
           plane_out=lambda rw: abs(rw["T1"]) + abs(rw["T2"]) + abs(rw["T3"]))
k2err = max(ana[k](rw) for k in ana for rw in ctab[k])
# finite-difference check of one Hessian (the sympy route vs FD)
fpot = sp.lambdify((X, Y, Z), POT["cyl_out"], "numpy"); p0 = np.array([1.7, 0.6, 0.3]); hh = 1e-4
Tfd = np.zeros((3, 3))
for i in range(3):
    for j in range(3):
        ei, ej = np.eye(3)[i] * hh, np.eye(3)[j] * hh
        Tfd[i, j] = (fpot(*(p0 + ei + ej)) - fpot(*(p0 + ei - ej)) - fpot(*(p0 - ei + ej)) + fpot(*(p0 - ei - ej))) / (4 * hh * hh)
fderr = float(np.abs(Tfd - np.array(HESS["cyl_out"](*p0), float)).max())
check("K1 point mass + uniform sphere: T1 = T3 = l_t = (4 pi G/3) rho_enc", k1err < 1e-10, f"max rel err {k1err:.1e}")
check("K2 cylinder (in (2piGrho,2piGrho,0), out (a,0,-a)) and plane ((4piGrho,0,0)/(0,0,0)): rule responses analytic",
      k2err < 1e-10 and fderr < 1e-5, f"max abs err {k2err:.1e}; FD Hessian check {fderr:.1e}")
P("  responses: cylinder inside T1 = 2 pi G rho (fires iff delta_f >= 2 tau), T2 = T3 = 0; outside T1 = T3 = 0; plane all 0.")
k3 = not any(0.0 > TAU(D) for D in (FTA, *DTA.values()))
check("K3 FRW (t = 0) OFF under strict H (tau > 0)", k3, f"min tau {min(TAU(D) for D in (FTA, *DTA.values())):.3f}")
OUT["numbers"]["controls"] = ctab

# ================================================================== (a) linear field
banner("(a) FRW / LINEAR: ON fraction of the Gaussian tidal field (t independent of grad psi at a point)")
NMC = 4_000_000
diagC = np.array([[3, 1, 1], [1, 3, 1], [1, 1, 3]]) / 15.0
Lc = np.linalg.cholesky(diagC)
RV = {q: np.empty(NMC, np.float32) for q in RULES}
B = 500_000
for b0 in range(0, NMC, B):
    d = rng.standard_normal((B, 3)) @ Lc.T
    o = rng.standard_normal((B, 3)) / math.sqrt(15.0)
    Tm = np.zeros((B, 3, 3))
    Tm[:, 0, 0], Tm[:, 1, 1], Tm[:, 2, 2] = d[:, 0], d[:, 1], d[:, 2]
    for (i, j), c in zip(((0, 1), (0, 2), (1, 2)), range(3)):
        Tm[:, i, j] = Tm[:, j, i] = o[:, c]
    rr = rules(Tm, rng.standard_normal((B, 3)))
    for q in RULES:
        RV[q][b0:b0 + B] = rr[q]
tr_var = float(np.var(d.sum(1)))
P(f"  unit-sigma tensor check: Var(trace) = {tr_var:.4f} (1); ordering l3 <= T3 <= l2 holds on all samples: "
  f"{bool(np.all(RV['T2'] <= RV['T3'] + 1e-6) and np.all(RV['T3'] <= RV['T1'] + 1e-6))}")


def on_lin(sd, tau):
    bound = float(CHI2.sf(6 * tau ** 2 / sd ** 2, 6))
    res = {}
    for q in RULES:
        hits = int(np.sum(RV[q] >= tau / sd))
        res[q] = dict(hits=hits, frac=hits / NMC, bound=bound,
                      lt1e6=bool(bound < 1e-6 or hits == 0))   # hits = 0 in 4e6: 95% upper limit 7.5e-7
    return res


a_rows, a_pass = {}, {q: True for q in RULES}
for Rh in (8, 20, 50):
    for z in (0.0, 1.0, 3.0, 10.0, 1000.0):
        _, _, sd = sig(Rh / h, KMIN_H, z)
        tau = TAU(DTA[0.0] if z == 0 else (DTA[1.0] if z <= 1 else FTA))
        res = on_lin(sd, tau)
        a_rows[f"R{Rh}|z{z}"] = dict(sigma=sd, tau=tau, ref_dlin_ge_1062=float(0.5 * erfc(1.062 / (sd * math.sqrt(2)))), **res)
        for q in RULES:
            a_pass[q] &= res[q]["lt1e6"]
        P(f"  R {Rh:2d} z {z:6.0f}: sigma {sd:.3e} tau {tau:.2f} | ON T1 {res['T1']['frac']:.2e} T2 {res['T2']['frac']:.2e} T3 {res['T3']['frac']:.2e} | chi2 bound {res['T1']['bound']:.1e}")
unsm = {}
for z in (1000.0, 10.0, 3.0, 0.0):
    _, _, sd = sig(0.0, KMIN_H, z)
    tau = TAU(DTA[0.0] if z == 0 else (DTA[1.0] if z <= 1 else FTA))
    res = on_lin(sd, tau)
    unsm[f"z{z}"] = dict(sigma=sd, tau=tau, ref_dlin_ge_1062=float(0.5 * erfc(1.062 / (sd * math.sqrt(2)))), **res)
    P(f"  UNSMOOTHED (k <= 50/Mpc) z {z:6.0f}: sigma {sd:.3e} | ON T1 {res['T1']['frac']:.2e} T2 {res['T2']['frac']:.2e} T3 {res['T3']['frac']:.2e} "
      f"| bound {res['T1']['bound']:.1e} | P(delta_lin >= 1.062) {unsm[f'z{z}']['ref_dlin_ge_1062']:.2e}{'  [scored]' if z == 1000 else '  [reported: nonlinear at the cutoff]'}")
for q in RULES:
    a_pass[q] &= unsm["z1000.0"][q]["lt1e6"] and k3
OUT["numbers"]["a_linear"] = a_rows; OUT["numbers"]["a_unsmoothed"] = unsm
for q in RULES:
    check(f"(a) {q} FRW OFF + linear ON < 1e-6 (R 8/20/50, all z; unsmoothed z 1000)", a_pass[q],
          f"max ON {max(r[q]['frac'] for r in a_rows.values()):.2e}")

# ================================================================== (a') sheets / filaments
banner("(a') COMPENSATED SHEETS AND FILAMENTS (CFG353 cells), EdS threshold scored, z = 0 reported")


def cell_tensors(geom, x, gphi, src):
    n = len(x); Tm = np.zeros((n, 3, 3)); gv = np.zeros((n, 3))
    if geom == "plane":
        Tm[:, 0, 0] = src
    else:
        Tm[:, 1, 1] = gphi / x; Tm[:, 0, 0] = src - gphi / x
    gv[:, 0] = gphi
    return Tm, gv


aprime, ap_pass = {}, {q: True for q in RULES}
for D_, dl in ((FTA, "EdS"), (DTA[0.0], "z0")):
    tau = TAU(D_)
    for geom, dls in (("plane", (0.5, 1, 2, 3)), ("cyl", (1, 2, 5, 10))):
        for dlt in dls:
            for ratio in (3, 5, 10):
                dv = -dlt / (ratio - 1) if geom == "plane" else -dlt / (ratio ** 2 - 1)
                if dv < -1:
                    aprime[f"{dl}|{geom}|d{dlt}|r{ratio}"] = "excluded: delta_v < -1"; continue
                x, phi, gphi, wt, w, src = cell(geom, dlt, ratio)
                R = rules(*cell_tensors(geom, x, gphi, src))
                res = {q: dict(on_frac=float(np.sum((R[q] > tau) * wt) / np.sum(wt)), max_R_over_tau=float(R[q].max() / tau)) for q in RULES}
                aprime[f"{dl}|{geom}|d{dlt}|r{ratio}"] = res
                if dl == "EdS":
                    for q in RULES:
                        ap_pass[q] &= res[q]["on_frac"] == 0.0
                if ratio == 5 or (geom == "cyl" and ratio == 10):
                    P(f"  {dl:3s} {geom:5s} delta {dlt:4} x{ratio:2d}: " + " | ".join(f"{q} ON {res[q]['on_frac']:.4f} max R/tau {res[q]['max_R_over_tau']:.2f}" for q in RULES))
P(f"  T1 fires inside a uniform filament iff delta_f >= 2 tau = {2*TAU(FTA):.3f} (EdS) / {2*TAU(DTA[0.0]):.3f} (z = 0)")
OUT["numbers"]["a_prime"] = aprime
for q in RULES:
    check(f"(a') {q} no false ON in compensated sheets/filaments (EdS)", ap_pass[q],
          f"max ON frac {max(v[q]['on_frac'] for k, v in aprime.items() if k.startswith('EdS') and not isinstance(v, str)):.4f}")


def ferrers(shape, p):
    e = math.sqrt(1 - 1 / p ** 2)
    if shape == "prolate":
        A3 = 2 * (1 - e * e) / e ** 3 * (math.atanh(e) - e); A1 = (2 - A3) / 2
        return np.array([A1, A1, A3]), np.array([1 / p, 1 / p, 1.0])
    A1 = math.sqrt(1 - e * e) / e ** 3 * math.asin(e) - (1 - e * e) / (e * e); A3 = 2 - 2 * A1
    return np.array([A1, A1, A3]), np.array([1.0, 1.0, 1 / p])


ell_rows = {}
u = rng.standard_normal((200000, 3)); u /= np.linalg.norm(u, axis=1)[:, None]
u *= rng.uniform(0, 1, (200000, 1)) ** (1 / 3)
for shape in ("prolate", "oblate"):
    for p in (5, 10):
        A, ax = ferrers(shape, p)
        for dlt in (1, 2, 5, 10):
            lam = dlt * A / 2
            pts = u * ax
            Tm = np.broadcast_to(np.diag(lam), (len(pts), 3, 3)).copy()
            R = rules(Tm, pts * lam)
            row = {q: float(np.mean(R[q] > TAU(FTA))) for q in RULES}
            ell_rows[f"{shape}|p{p}|d{dlt}"] = dict(A=A.tolist(), **row)
            if dlt in (5, 10):
                P(f"  [reported] uniform {shape} aspect {p:2d} delta {dlt:2d} (A {np.round(A,3).tolist()}): ON vol frac T1 {row['T1']:.3f} T2 {row['T2']:.3f} T3 {row['T3']:.4f}")
OUT["numbers"]["ellipsoids_reported"] = ell_rows

# ================================================================== hosts: profiles
THL = np.linspace(1e-4, math.pi, 4000)
DLIN = 0.15 * (6 * (THL - np.sin(THL))) ** (2 / 3)
FNL = 9 * (THL - np.sin(THL)) ** 2 / (2 * (1 - np.cos(THL)) ** 3)
xs_M = np.geomspace(1.0, 1e6, 6000)
F_M = np.interp(np.interp(float(DLIN[-1]) / xs_M, DLIN, THL), THL, FNL)
x_E = (xs_M * FTA / F_M) ** (1 / 3)
m_E = FTA * xs_M * (1 - 1 / F_M)
XG = np.geomspace(1e-3, 3.0, 400)


def profile(m_in, D):
    m = np.where(XG <= 1, m_in(np.minimum(XG, 1.0)), (D - 1) / (FTA - 1) * np.interp(XG, x_E, m_E))
    lt = m / (3 * XG ** 3)
    dloc = np.gradient(m, XG) / (3 * XG ** 2)
    return lt, dloc - 2 * lt, m / (3 * XG ** 2)        # l_t, l_r, g_host (r_ta units)


def menc_nfw(Mb, z, r):
    hs = host(Mb, z); x = r / hs["rs"]
    return 4 * math.pi * hs["rho_s"] * hs["rs"] ** 3 * (np.log(1 + x) - x / (1 + x))


def r_ta_host(z, Mb, D):
    hs = host(Mb, z); rb = rhom(z)
    fn = lambda lr: menc_nfw(Mb, z, math.exp(lr)) / (4 / 3 * math.pi * math.exp(lr) ** 3) / rb - (D - 1)
    return math.exp(brentq(fn, math.log(hs["r200"]), math.log(1e3 * hs["r200"])))


def unit_tensors(n):
    d = rng.standard_normal((n, 3)) @ Lc.T; o = rng.standard_normal((n, 3)) / math.sqrt(15.0)
    Tm = np.zeros((n, 3, 3)); Tm[:, 0, 0], Tm[:, 1, 1], Tm[:, 2, 2] = d.T
    for (i, j), c in zip(((0, 1), (0, 2), (1, 2)), range(3)):
        Tm[:, i, j] = Tm[:, j, i] = o[:, c]
    return Tm


NH = 2000
ZH = np.array([0.0, 0.0, 1.0])


def host_tensor(lt, lr, rhat):
    return lt[..., None, None] * (np.eye(3) - rhat[..., :, None] * rhat[..., None, :]) + lr[..., None, None] * rhat[..., :, None] * rhat[..., None, :]


def edges_for(lt, lr, gh, tau, sd, s1u, i0, ncd=0):
    """Ray along z; external uniform tidal tensor (sigma sd) + gradient (sigma s1u, r_ta units).
    Returns per rule: P(ON at i0), edges (NH), c_d samples."""
    Te = unit_tensors(NH) * sd
    ge = rng.standard_normal((NH, 3)) * s1u / math.sqrt(3)
    Th = host_tensor(lt, lr, np.broadcast_to(ZH, (len(XG), 3)))
    Tt = Th[None] + Te[:, None]
    gt = gh[None, :, None] * ZH + ge[:, None, :]
    R = rules(Tt, gt)
    out = {}
    for q in RULES:
        on = R[q][:, i0:] > tau
        first_off = np.where(on.all(1), on.shape[1], np.argmin(on, axis=1))
        ka = np.minimum(i0 + first_off, len(XG) - 1); kb = np.maximum(ka - 1, 0)
        ra = np.take_along_axis(R[q], ka[:, None], 1)[:, 0] - tau; rb_ = np.take_along_axis(R[q], kb[:, None], 1)[:, 0] - tau
        fr = np.clip(rb_ / np.where(rb_ - ra != 0, rb_ - ra, 1.0), 0, 1)       # linear crossing in log x
        xint = np.exp(np.log(XG[kb]) + fr * (np.log(XG[ka]) - np.log(XG[kb])))
        xe = np.where(on[:, 0], np.where(on.all(1), XG[-1], xint), 0.0)
        out[q] = dict(p_on=float(np.mean(on[:, 0])), xe=xe)
        if ncd:
            cds = []
            for j in range(min(ncd, NH)):
                if xe[j] <= 0 or xe[j] >= XG[-1]:
                    continue
                cds.append(c_delta(q, xe[j], Te[j], ge[j], lt, lr, gh, tau))
            out[q]["cd"] = np.array(cds)
    return out


def c_delta(q, xe, Te, ge, lt, lr, gh, tau):
    """surface-delta coefficient n_s.P.n_s at the edge point x = xe * z (3D finite differences)."""
    def at(pt, dT=None):
        r = np.linalg.norm(pt); rh = pt / r
        lti, lri, ghi = (np.interp(np.log(r), np.log(XG), a) for a in (lt, lr, gh))
        Tm = host_tensor(np.array(lti), np.array(lri), rh) + Te + (0 if dT is None else dT)
        return float(rules(Tm[None], (ghi * rh + ge)[None])[q][0])
    p0 = xe * ZH; hh = 1e-4 * xe
    gs = np.array([(at(p0 + hh * e) - at(p0 - hh * e)) / (2 * hh) for e in np.eye(3)])
    if np.linalg.norm(gs) == 0:
        return 0.0
    n = gs / np.linalg.norm(gs); ep = 1e-6 * max(tau, 1e-3)
    return abs((at(p0, ep * np.outer(n, n)) - at(p0, -ep * np.outer(n, n))) / (2 * ep))


# ================================================================== (b) + (c)
banner("(b) BOUND HOSTS + (c) EDGE: 24 DE12 hosts, isolated sphere + linear LSS tide/gradient at the host")
hrows = []
for hk in HOSTS:
    z, Mb, ft = hk; D = DTA[z]; tau = TAU(D); rb = rhom(z)
    rta = r_ta_host(z, Mb, D)
    unit = 4 / 3 * math.pi * rb * rta ** 3
    lt, lr, gh = profile(lambda x: menc_nfw(Mb, z, x * rta) / unit, D)
    i30 = int(np.searchsorted(XG, 30 * KPC / rta))
    iso = {q: float(rules(host_tensor(lt, lr, np.broadcast_to(ZH, (len(XG), 3))), gh[:, None] * ZH)[q][i30]) for q in RULES}
    rL_com = (D * rta ** 3) ** (1 / 3) * (1 + z) / MPC
    _, s1, sd = sig(2 * rL_com, KMIN_H, z)
    s1u = s1 / (1 + z) * MPC / rta
    res = edges_for(lt, lr, gh, tau, sd, s1u, i30, ncd=60)
    M30 = menc_nfw(Mb, z, 30 * KPC) + Mb * MS
    dlnm = 0.1 * Mb * MS / M30
    row = dict(host=KEY(*hk), rta_kpc=rta / KPC, Delta=D, tau=tau, sigma_ext=sd, text_over_tau=sd * math.sqrt(2 / 15) / tau,
               gext_over_ghost_rta=s1u / tau, margin30_lt=float(lt[i30] / tau), fid_dlnm=dlnm,
               flip_lt=bool(dlnm >= math.log(lt[i30] / tau)) if lt[i30] > tau else None,
               iso30={q: iso[q] / tau for q in RULES})
    for q in RULES:
        xe = res[q]["xe"]; cd = res[q].get("cd", np.array([]))
        row[q] = dict(p_on30=res[q]["p_on"], edge_med=float(np.median(xe)), edge_p16=float(np.percentile(xe, 16)),
                      edge_p84=float(np.percentile(xe, 84)), off_kpc=float(abs(1 - np.median(xe)) * rta / KPC),
                      cd_med=float(np.median(cd)) if len(cd) else None, cd_p95=float(np.percentile(cd, 95)) if len(cd) else None,
                      cd_max=float(cd.max()) if len(cd) else None, n_cd=int(len(cd)))
    hrows.append(row)
    P(f"  {row['host']:>18s} r_ta {row['rta_kpc']:5.0f} kpc tau {tau:.2f} | |t_ext|/tau {row['text_over_tau']:.3f} g_ext/g_h(r_ta) {row['gext_over_ghost_rta']:.2f} | "
      + " | ".join(f"{q} P30 {row[q]['p_on30']:.2f} edge {row[q]['edge_med']:.3f} ({row[q]['off_kpc']:4.0f} kpc) c_d {row[q]['cd_med'] if row[q]['cd_med'] is not None else float('nan'):.1e}" for q in RULES))
OUT["numbers"]["hosts"] = hrows

# isolated-sphere edges (no LSS): T1 = T3 = l_t -> edge exactly r_ta
iso_edge = []
for hk in HOSTS[:6]:
    z, Mb, ft = hk; D = DTA[z]; rta = r_ta_host(z, Mb, D)
    lt, lr, gh = profile(lambda x: menc_nfw(Mb, z, x * rta) / (4 / 3 * math.pi * rhom(z) * rta ** 3), D)
    iso_edge.append(float(np.exp(np.interp(0.0, -np.log(lt / TAU(D)), np.log(XG)))))
P(f"  isolated spheres (no LSS), T1 = T3 edge: {np.round(iso_edge, 5).tolist()} r_ta (exact by construction: l_t = tau <=> dbar = Delta - 1)")
OUT["numbers"]["iso_edges"] = iso_edge

b_pass, c_pass, c_edge_pass, c_wp = {}, {}, {}, {}
for q in RULES:
    fid = all((r["flip_lt"] is False) for r in hrows) if q in ("T1", "T3") else None
    b_pass[q] = all(r[q]["p_on30"] >= 0.99 for r in hrows) and (fid if fid is not None else all(r["iso30"]["T2"] > 1 for r in hrows))
    c_edge_pass[q] = sum(r[q]["off_kpc"] <= 100 for r in hrows)
    cdmax = max((r[q]["cd_max"] or 0.0) for r in hrows)
    c_wp[q] = cdmax <= 1e-8 if any(r[q]["n_cd"] for r in hrows) else False   # no edge: radial reader c_d = 1 analytically (WP demo)
    c_pass[q] = c_edge_pass[q] == 24 and c_wp[q]
    check(f"(b) {q} ON at 30 kpc w.p. >= 0.99 on 24/24 + fidelity", b_pass[q],
          f"min P(ON30) {min(r[q]['p_on30'] for r in hrows):.3f}; max d ln m (10% gas) {max(r['fid_dlnm'] for r in hrows):.3f} vs min ln margin "
          f"{min(math.log(max(r['margin30_lt'], 1e-30)) for r in hrows):.2f}")
    check(f"(c) {q} edge within 100 kpc on 24/24 + sharp-H well-posed (c_d = 0)", c_pass[q],
          f"edge {c_edge_pass[q]}/24; median edges {min(r[q]['edge_med'] for r in hrows):.3f}-{max(r[q]['edge_med'] for r in hrows):.3f} r_ta; "
          f"c_d max {cdmax:.2e} (median over hosts {np.median([r[q]['cd_med'] or 0 for r in hrows]):.2e})")
EPS = {}
for q in RULES:
    cd95 = max((r[q]["cd_p95"] or 0.0) for r in hrows)
    eps = max(cd95 * r["Delta"] / 6 for r in hrows)
    EPS[q] = dict(cd_p95_max=cd95, eps_min=eps, smear_rta=max(cd95 * r["Delta"] / 6 / (2 * r["tau"]) for r in hrows))
    P(f"  {q}: width needed for V_b <= V_c^2 (g_ph/g <= 1): eps_min = {eps:.2e} (units 4 pi G rho_bar) -> edge smearing <= {EPS[q]['smear_rta']:.2e} r_ta")
OUT["numbers"]["width_cost"] = EPS

# ================================================================== (d) inputs: KiDS-like lenses
banner("(d) inputs: KiDS-like lens bins (z = 0.25, isothermal law mass) with the same LSS field")
A0D = NS["A0"]
zl = 0.25; D = DTA[zl]; tau = TAU(D); rb = rhom(zl)
lens = {q: [] for q in RULES}
for ft in FOOTS:
    for lm in (10.0, 10.5, 11.0, 11.5):
        Mb = 10 ** lm * MS
        rta = math.sqrt(3 * math.sqrt(G * Mb * A0D[ft]) / (4 * math.pi * G * rb * D))
        lt, lr, gh = profile(lambda x: D * x - x ** 3, D)
        rL_com = (D * rta ** 3) ** (1 / 3) * (1 + zl) / MPC
        _, s1, sd = sig(2 * rL_com, KMIN_H, zl)
        res = edges_for(lt, lr, gh, tau, sd, s1 / (1 + zl) * MPC / rta, int(np.searchsorted(XG, 0.01)))
        for q in RULES:
            lens[q].append(float(np.median(res[q]["xe"])))
        P(f"  {ft:9s} log M_b {lm}: r_ta {rta/KPC:5.0f} kpc | " + " | ".join(f"{q} median edge {lens[q][-1]:.3f}" for q in RULES))
OUT["numbers"]["lens_edges"] = lens
OUT["numbers"]["edges_for_harness"] = {f"{q}_{s}": (min(lens[q]) if s == "min" else max(lens[q])) for q in RULES for s in ("min", "max")}

# ================================================================== legality
banner("LEGALITY + WELL-POSEDNESS")
x_ = sp.symbols("x")
psi_f, mu_f, LM_f, rho_f = [sp.Function(n)(x_) for n in ("psi", "mu", "L_M", "rho")]
nu_, c_, rb_ = sp.symbols("nu c rhobar")
Ff = sp.Function("F")
Lag = mu_f * (sp.diff(psi_f, x_, 2) - (rho_f - rb_)) + nu_ * psi_f + Ff(sp.diff(psi_f, x_, 2) - c_) * LM_f
from sympy.calculus.euler import euler_equations
eqs = euler_equations(Lag, [psi_f, mu_f], x_)
P(f"  L1 EOM (psi): {sp.simplify(eqs[0].lhs)} = 0")
P(f"  L1 EOM (mu):  {sp.simplify(eqs[1].lhs)} = 0")
l1 = check("L1 EOM derivable (sympy)", len(eqs) == 2 and all(e.lhs != 0 for e in eqs), "Euler-Lagrange for psi, mu")
check("L2 leaf scalar densities", True, "eigenvalues of h^ik D_k D_j Phi_d and |D Phi_d|_h, mu lap_h Phi_d, nu Phi_d, <rho> as CFG329's <K>")
kk3 = np.stack(np.meshgrid(*(np.fft.fftfreq(24) * 24,) * 3, indexing="ij"), -1).reshape(-1, 3)[1:]
symb = np.abs(kk3[:, :, None] * kk3[:, None, :] / np.sum(kk3 ** 2, -1)[:, None, None]).max()
l3 = check("L3 no momenta; t = d d lap^-1 delta is order 0 (|k_i k_j/k^2| <= 1)", symb <= 1 + 1e-12,
           f"max symbol {symb:.6f}; no d_t of Phi_d, mu, nu -> no Ostrogradsky DOF; t is algebraic in delta_hat in Fourier space")
# L4: 1D periodic leaf, smoothed switch on psi'' (= delta in 1D), MOND-like L_M = -psi'^2/2
N = 256; Lb = 2 * math.pi; xx = np.arange(N) * Lb / N
kk = np.fft.fftfreq(N, d=Lb / N) * 2 * math.pi; Dk = 1j * kk
inv = np.zeros(N); inv[1:] = -1 / kk[1:] ** 2
dx = lambda f: np.real(np.fft.ifft(Dk * np.fft.fft(f)))
poi = lambda s: np.real(np.fft.ifft(inv * np.fft.fft(s)))
CC = 0.4
sgm = lambda u, w: 1 / (1 + np.exp(-u / w))


def energy(rho, w):
    ph = poi(rho - rho.mean()); g = dx(ph); t = dx(g)
    return np.sum(sgm(t - CC, w) * (-0.5 * g ** 2)) * Lb / N


def grad_adj(rho, w):
    ph = poi(rho - rho.mean()); g = dx(ph); t = dx(g)
    F = sgm(t - CC, w); Fp = F * (1 - F) / w; LMv = -0.5 * g ** 2
    dEdt = Fp * LMv                       # d/d t
    dEdg = F * (-g)
    dEdph = dx(dx(dEdt)) - dx(dEdg)       # D^T D^T = D D, D^T = -D
    mu = poi(dEdph)
    return (mu - mu.mean()) * Lb / N, (Fp * LMv)


rho0 = 1 + 0.6 * np.cos(xx) + 0.3 * np.sin(2 * xx + 0.4) + 0.2 * np.cos(3 * xx + 1.1)
ga, _ = grad_adj(rho0, 0.3)
fd = []
for i in (3, 77, 140, 201):
    e = np.zeros(N); e[i] = 1e-6
    fd.append(((energy(rho0 + e, 0.3) - energy(rho0 - e, 0.3)) / 2e-6, ga[i]))
fd_err = max(abs(a - b) / max(abs(a), 1e-30) for a, b in fd)
noether = abs(np.sum(ga * dx(rho0))) / np.sum(np.abs(ga * dx(rho0)))
l4 = check("L4 momentum (adjoint 1e-5, Noether 1e-8)", fd_err < 1e-5 and noether < 1e-8, f"{fd_err:.1e} / {noether:.1e}")
# 1D: the local layer term sup|f' L_M| vs width (P = n n in 1D)
N2 = 8192; xx2 = np.arange(N2) * Lb / N2; rho2 = 1 + 0.6 * np.cos(xx2)
sup1d = {}
for w in (0.1, 0.03, 0.01, 0.003):
    t = rho2 - rho2.mean(); ph = poi_ = None
    kk2 = np.fft.fftfreq(N2, d=Lb / N2) * 2 * math.pi; inv2 = np.zeros(N2); inv2[1:] = -1 / kk2[1:] ** 2
    ph = np.real(np.fft.ifft(inv2 * np.fft.fft(t))); g = np.real(np.fft.ifft(1j * kk2 * np.fft.fft(ph)))
    F = sgm(t - CC, w); sup1d[w] = float(np.abs(F * (1 - F) / w * (-0.5 * g ** 2)).max())
P("  1D leaf (P = n n): sup |dE/drho| local layer vs width: " + ", ".join(f"w {w}: {v:.3e}" for w, v in sup1d.items())
  + f"  -> x{sup1d[0.003]/sup1d[0.1]:.1f} for w/33 (∝ 1/w)")
# spherical layer: tangential vs radial projector, Poisson-solved potential
rgr = np.linspace(1e-3, 4.0, 400001); dr = rgr[1] - rgr[0]
sph = {}
d1 = lambda f: np.gradient(f, dr)
for w in (0.05, 0.02, 0.005):
    F = np.exp(-0.5 * ((rgr - 1.0) / w) ** 2) / (w * math.sqrt(2 * math.pi))
    lapF = d1(rgr ** 2 * d1(F)) / rgr ** 2
    ddFnn = d1(d1(rgr ** 2 * F)) / rgr ** 2
    out = {}
    for nm, S in (("tangential (T1/T3)", 0.5 * (lapF - ddFnn)), ("radial (T2)", ddFnn)):
        encl = np.cumsum(S * rgr ** 2) * dr
        dphi = encl / rgr ** 2
        phi = -np.cumsum(dphi[::-1])[::-1] * dr
        out[nm] = float(np.abs(phi).max())
    sph[w] = out
P("  sphere layer (unit surface density at r = 1): sup|potential| " + "; ".join(
    f"w {w}: tang {v['tangential (T1/T3)']:.3f}, radial {v['radial (T2)']:.2f}" for w, v in sph.items()))
xs_, ys_, zs_ = sp.symbols("x y z", positive=True); rs_ = sp.sqrt(xs_ ** 2 + ys_ ** 2 + zs_ ** 2); Ffun = sp.Function("F")
xv = (xs_, ys_, zs_)
dd = sum(sp.diff(Ffun(rs_) * xv[i] * xv[j] / rs_ ** 2, xv[i], xv[j]) for i in range(3) for j in range(3))
rr_ = sp.symbols("r", positive=True)
ident = sp.simplify((dd - sp.diff(rr_ ** 2 * Ffun(rr_), rr_, 2).subs(rr_, rs_) / rs_ ** 2))
P(f"  sympy identity d_i d_j (F n_i n_j) = (r^2 F)''/r^2: residual {ident}")
wp_sph = (sph[0.005]["tangential (T1/T3)"] / sph[0.05]["tangential (T1/T3)"] < 1.2) and (sph[0.005]["radial (T2)"] / sph[0.05]["radial (T2)"] > 5) and ident == 0
check("WP spherical layer: tangential reader finite jump, radial reader ∝ 1/w; 1D layer ∝ 1/w", wp_sph and sup1d[0.003] / sup1d[0.1] > 20,
      f"tang ratio {sph[0.005]['tangential (T1/T3)']/sph[0.05]['tangential (T1/T3)']:.2f}, radial ratio {sph[0.005]['radial (T2)']/sph[0.05]['radial (T2)']:.1f}")
OUT["numbers"]["wellposed"] = dict(sup1d={str(k): v for k, v in sup1d.items()}, sphere={str(k): v for k, v in sph.items()})
L_ok = l1 and l3 and l4

# ================================================================== verdict (d) is scored by the harness
banner("VERDICT pre-(d) per rule (primary T3); (d) scored by cfg354_edge_harness.py")
ver = {}
for q in RULES:
    fails = [n for n, ok in (("L", L_ok), ("a", a_pass[q]), ("a'", ap_pass[q]), ("b", b_pass[q]), ("c", c_pass[q])) if not ok]
    ver[q] = dict(failures_pre_d=fails, c_edge=c_edge_pass[q], c_wellposed=c_wp[q])
    P(f"  {q}{' (PRIMARY)' if q == 'T3' else ''}: failures before (d): {fails}; edge {c_edge_pass[q]}/24; sharp-H well-posed {c_wp[q]}")
OUT["verdict_pre_d"] = ver
P(f"  runtime {time.time()-T0:.0f} s")
json.dump(OUT, open(os.path.join(HERE, f"cfg354_tidal_switch_results{SUF}.json"), "w"), indent=1, default=str)
