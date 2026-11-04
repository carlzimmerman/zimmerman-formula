#!/usr/bin/env python3
"""FN1b small gates at one universal Gaussian length L: T1 Cassini, T2 24 Local Group dwarfs, T3 SPARC, T4 planets.
Forms R (Phi_N + S Phi_ph[S rho], primary) and SO (Phi_N + Phi_ph[S rho], beside); both footings. Criteria e6e031a163.
Engines: KT33's cassini_v2 (vendored unchanged in vendor_kt33/, KT33 being uncommitted; known answers from fn1b_ka_snapshot.json); CZ2's dwarf code, CZ5's plain3 row, KT19's SPARC code and CZ3's planet
code copied verbatim (marked). Run: OMP_NUM_THREADS=1 nice -n 15 python3 -I -B fn1b_small.py [--mutate].
kappa = 1/2 FITTED and held fixed; not theory closed."""
import csv, glob, hashlib, importlib.util, json, math, os, resource, sys, time
sys.dont_write_bytecode = True
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"): os.environ[_v] = "1"
import numpy as np
import warnings   # this machine's Accelerate BLAS raises false FP flags in matmul (KT14, CW1 note it); results are checked finite below
for _m in ("invalid value encountered in matmul", "divide by zero encountered in matmul", "overflow encountered in matmul"): warnings.filterwarnings("ignore", message=_m)
from scipy.optimize import brentq
from scipy.special import erf
T00 = time.time()
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
RB = os.path.join(REPO, "rebuild_2026_10_22"); CG = os.path.join(REPO, "claude_goal_2026_11_03")
MUT = "--mutate" in sys.argv; OUT = []; RES = {}; FAILS = []
def P(s=""): print(s, flush=True); OUT.append(s)
def check(name, ok, msg):
    ok = bool(ok); P(f"{name} {'PASS' if ok else 'FAIL'}: {msg}"); RES.setdefault("checks", {})[name] = dict(ok=ok, msg=msg)
    if not ok: FAILS.append(name)
def rel(a, b): return abs(a / b - 1) if b != 0 else float("inf")
KAP = 0.5; A0SI = {"canonical": 9.3603e-11, "alt": 1.1312e-10}; LS = [0.024, 0.1, 0.25, 0.5, 1.0, 2.0]; KPC = 3.0857e19
GEXT, CEIL, HEES = 2.32e-10, 5.2e-27, 9.0e-27; Gk = 4.30091e-6; CONV = 3.0857e19 / 1e6; XCLIP = 200.0; M_MW = 7.0e10
FORMS = ("R", "SO")
P(f"FN1b small gates (criteria e6e031a163){'  [MUTATE: nu = 1]' if MUT else ''}; kappa = 1/2 FITTED; not theory closed")
nu_s = lambda y: 0.5 + np.sqrt(0.25 + 1 / np.maximum(y, 1e-300))
dnu_s = lambda y: -1 / (2 * np.maximum(y, 1e-300) ** 2 * np.sqrt(0.25 + 1 / np.maximum(y, 1e-300)))
if MUT:
    nu = lambda y: np.ones_like(np.asarray(y, float)); dnu = lambda y: np.zeros_like(np.asarray(y, float))
else:
    nu, dnu = nu_s, dnu_s
def eta_newton(a0):
    eo = GEXT / a0; return eo if MUT else brentq(lambda y: float(nu_s(y)) * y - eo, 1e-9, eo)
def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path); m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m

# ======================================================================= T1 Cassini
P("\n== T1 Cassini (Sun's own Q2; ceiling 5.2e-27, Hees 9.0e-27)")
CV = load("kt33_cassini_v2", os.path.join(HERE, "vendor_kt33", "cassini_v2.py"))
GMc = CV.GM
def q_lin(eta, sig): return (4 / 45) * math.sqrt(2 / math.pi) * eta * float(dnu(eta)) / sig ** 3
KA = json.load(open(os.path.join(HERE, "fn1b_ka_snapshot.json")))
cz4 = json.load(open(os.path.join(CG, "CZ4_solar_neighbourhood_filter", "cz4.json")))
T1 = {}; KA5a, KA5b, V2 = [], [], []
for foot, a0 in A0SI.items():
    rM = math.sqrt(GMc / a0); pref = 1.5 * a0 / rM; etaN = eta_newton(a0); eta0 = GEXT / a0
    # KA5a: KT33's stored baseline values at eps = 0.5 with the observed field (its own convention)
    for arm, so in (("source_only_hessian", 0.0), ("reciprocal", 0.5)):
        got = CV.quadrupole(eta0, 0.5, so, newtonian=MUT)["q_hessian_signed"]; ref = KA["run002_baseline"][foot][arm]
        KA5a.append(rel(got, ref)); P(f"  KA5a [{foot}] {arm}: q_hessian {got:.10g} (stored {ref:.10g}), rel {rel(got, ref):.1e}")
    # KA5b: KT16/CZ2's flux integral (no surface term) with the Newtonian field at sigma = 0.5: CZ2/CW1 HALF 1.179 / 2.97
    qf = CV.quadrupole(etaN, 0.5, 0.0, newtonian=MUT)["q_flux_signed"]; xf = abs(qf) * pref / CEIL; v = {"canonical": 1.179, "alt": 2.97}[foot]
    nd = len(str(v).split(".")[1]); KA5b.append(abs(round(xf, nd) - v) < 1e-9); P(f"  KA5b [{foot}] flux control at sigma 0.5, eta_N: {xf:.4g} x ceiling (CZ2/CW1 {v})")
    # V2: the analytic linear response against KT33's numeric Hessian at sigma 20 and 50 r_M
    for sg in (20.0, 50.0):
        for form, so in (("SO", 0.0), ("R", sg)):
            num = CV.quadrupole(etaN, sg, so, newtonian=MUT); an = q_lin(etaN, sg * (math.sqrt(2) if form == "R" else 1.0))
            r_ = num["q_hessian_signed"] / an if an != 0 else float("nan"); V2.append(abs(r_ - 1) if r_ == r_ else float("inf"))
            P(f"  V2 [{foot}] sigma {sg:.0f} r_M {form}: numeric q {num['q_hessian_signed']:.6e} (density route {num['q_density_signed']:.6e}), analytic {an:.6e}, ratio {r_:.5f}")
    env = cz4[foot]["TID"]["cassini"]["q_env_alltide"]; T1[foot] = {}
    for L in LS:
        sig = L * KPC / rM; row = {}
        for form in FORMS:
            q = q_lin(etaN, sig * (math.sqrt(2) if form == "R" else 1.0)); Q2 = abs(q) * pref
            row[form] = dict(sigma_rM=sig, q=q, Q2=Q2, x_ceiling=Q2 / CEIL, x_hees=Q2 / HEES, env_x_ceiling=env, total_x_ceiling=Q2 / CEIL + env, ok=bool(Q2 <= CEIL))
        T1[foot][str(L)] = row
        P(f"  T1 [{foot}] L {L:5.3f} kpc (sigma {sig:8.1f} r_M): Q2 R {row['R']['Q2']:.3e} ({row['R']['x_ceiling']:.2e} x ceiling, {row['R']['x_hees']:.2e} x Hees), SO {row['SO']['Q2']:.3e} ({row['SO']['x_ceiling']:.2e} x); CZ4 environment bound {env:.2e} x")
    RES.setdefault("T1_meta", {})[foot] = dict(eta_N=etaN, eta_obs=eta0, rM_AU=rM / 1.495978707e11, nu_e=float(nu(etaN)), dnu_e=float(dnu(etaN)))
check("KA5a", max(KA5a) <= 1e-6, f"KT33 quadrupole reproduces run_002 baseline q_hessian (source-only and reciprocal, eps 0.5), max rel {max(KA5a):.1e} (line 1e-6)")
check("KA5b", all(KA5b), "KT33 q_flux with eta_N at sigma 0.5 reproduces CZ2/CW1's HALF 1.179 / 2.97 x ceiling")
check("V2", max(V2) <= 0.02, f"analytic Cassini q against KT33's numeric Hessian at sigma 20, 50 r_M, both forms, max |ratio - 1| {max(V2):.2e} (line 0.02)")
RES["T1"] = T1

# ======================================================================= T4 planets (CZ3 / AZ12, verbatim pieces)
P("\n== T4 planets (AZ12's gate: worst Z = |rate| / max(EPM, INPOP) <= 2)")
GMp = 1.32712440018e20; AU = 149597870700.0; YR = 365.25 * 86400; MAS = math.pi / (180 * 3600 * 1000)
ECC = dict(Mercury=.206, Venus=.007, Earth=.017, Mars=.093, Jupiter=.048, Saturn=.054)
PL = json.load(open(os.path.join(RB, "RQ3_acceptance_v2", "tolerances.json")))["PLANETS"]
def rate(A, a, e, n, N):   # CZ3 / AZ12 verbatim
    t, w = np.polynomial.legendre.leggauss(N); E = math.pi * (t + 1); c = np.cos(E); r = a * (1 - e * c)
    return math.sqrt(1 - e * e) / (n * a * e) * float(np.sum(.5 * w * A(r) * (c - e)))
def monopole(h, a0, ge, N):   # CZ3 verbatim, nu switchable by the twin
    mu, w = np.polynomial.legendre.leggauss(N); H = h[:, None]; m = mu[None, :]; y = np.sqrt(H * H + ge * ge + 2 * H * ge * m) / a0
    return .5 * np.sum(w[None, :] * (nu(y) - 1) * (H + ge * m), axis=1)
def gh_pt(r, xi):   # CZ3 verbatim
    xi = np.broadcast_to(xi, r.shape); x = r / xi; out = np.empty_like(r); s = x < 1e-3
    out[~s] = (erf(x[~s] / math.sqrt(2)) - math.sqrt(2 / math.pi) * x[~s] * np.exp(-x[~s] ** 2 / 2)) / r[~s] ** 2; out[s] = math.sqrt(2 / math.pi) / 3 * r[s] / xi[s] ** 3; return out
def grade_field(h, a0, ge, orders=(256, 160)):   # CZ3's grade with a given field h(r)
    rows = {}
    for nm, d in PL.items():
        e = ECC[nm]; a = d["a_au"] * AU; nn = math.sqrt(GMp / a ** 3); s = max(d["EPM"], d["INPOP"]); rt = rate(lambda r: monopole(h(r), a0, ge, orders[1]), a, e, nn, orders[0]) * YR / MAS
        rows[nm] = dict(rate_mas_yr=rt, Z=abs(rt) / s)
    return rows
def grade_lin(kc):   # A(r) = kc r, the exact linear-response monopole of the smoothed Sun
    rows = {}
    for nm, d in PL.items():
        e = ECC[nm]; a = d["a_au"] * AU; nn = math.sqrt(GMp / a ** 3); s = max(d["EPM"], d["INPOP"]); rt = rate(lambda r: kc * r, a, e, nn, 256) * YR / MAS
        rows[nm] = dict(rate_mas_yr=rt, Z=abs(rt) / s)
    return rows
def kfac(eta): return (math.sqrt(2 / math.pi) / 3) * ((float(nu(eta)) - 1) + eta * float(dnu(eta)) / 3)
T4 = {}; KA6, V3 = [], []
for foot, a0 in A0SI.items():
    rM = math.sqrt(GMp / a0); etaN = eta_newton(a0); ge = etaN * a0
    kh = grade_field(lambda r: a0 * gh_pt(r / rM, 0.5), a0, ge)["Saturn"]["Z"]; v = {"canonical": 11.17, "alt": 18.13}[foot]; KA6.append(abs(round(kh, 2) - v) < 1e-9)
    P(f"  KA6 [{foot}] CZ3's HALF Saturn Z {kh:.4f} (CZ3 {v})")
    L0 = 0.024 * KPC; zn = grade_field(lambda r: a0 * gh_pt(r / rM, L0 / rM), a0, ge)["Saturn"]["Z"]; za = grade_lin(kfac(etaN) * GMp / L0 ** 3)["Saturn"]["Z"]
    r_ = zn / za if za != 0 else float("nan"); V3.append(abs(r_ - 1) if r_ == r_ else float("inf")); P(f"  V3 [{foot}] L 24 pc SO Saturn Z: numeric {zn:.6e}, analytic {za:.6e}, ratio {r_:.5f}")
    sat = cz4[foot]["TID"]["rows"]["Saturn"]; disc = sat["Z_sun_disc"] - sat["Z_sun"]; T4[foot] = {}
    for L in LS:
        row = {}
        for form in FORMS:
            Le = L * KPC * (math.sqrt(2) if form == "R" else 1.0); g = grade_lin(kfac(etaN) * GMp / Le ** 3); w = max(g, key=lambda p: g[p]["Z"])
            row[form] = dict(rows=g, worst=w, Z=g[w]["Z"], Saturn_Z=g["Saturn"]["Z"], disc_bound_Saturn=disc, ok=bool(g[w]["Z"] <= 2))
        T4[foot][str(L)] = row
        P(f"  T4 [{foot}] L {L:5.3f} kpc: worst R {row['R']['worst']} Z {row['R']['Z']:.2e}, SO {row['SO']['worst']} Z {row['SO']['Z']:.2e}; CZ4 disc bound at Saturn {disc:.2e}")
check("KA6", all(KA6), "CZ3's planet code reproduces CZ3's HALF Saturn Z 11.17 / 18.13")
check("V3", max(V3) <= 0.02, f"analytic planet monopole against CZ3's numeric monopole at L 24 pc (SO, Saturn), max |ratio - 1| {max(V3):.2e} (line 0.02)")
RES["T4"] = T4

# ======================================================================= T2 dwarfs (CZ2's code verbatim, marked)
P("\n== T2 dwarfs (E1 graded, line >= 15/24; STRICT >= plain E1; E2 and D3 beside)")
UPS = np.linspace(1, 3, 41)
def xi_loc(r, gm, gs, clip):   # CZ2 verbatim (unused here; sig_los needs the names)
    dg = np.abs(np.gradient(gm, r)); return np.minimum(gm * gm / np.maximum(dg * gs, 1e-300), clip)
def xi_tid(r, gm, gs, clip):   # CZ2 verbatim (unused here)
    tau = np.sqrt(np.gradient(gm, r) ** 2 + 2 * (gm / r) ** 2); lt = np.log(np.maximum(tau, 1e-300))
    dt = np.abs(tau * np.gradient(lt, np.log(r)) / r); return np.minimum(4 / math.sqrt(3) * tau ** 3 / np.maximum(dt * dt * gs, 1e-300), clip)
def rgrid(a, xi, n=2000): return np.geomspace(1e-4 * a, 60 * a + 8 * xi, n)   # CZ2 verbatim
def plummer(r, M, a): return 3 * M / (4 * math.pi * a ** 3) * (1 + (r / a) ** 2) ** -2.5   # CZ2 verbatim
def smooth_rows(r, rho, s, mask_small=False):   # CZ2 verbatim
    s = np.broadcast_to(np.asarray(s, float), r.shape); R, Rp, S = r[:, None], r[None, :], s[:, None]
    K = (Rp / (math.sqrt(2 * math.pi) * S * R)) * (np.exp(-(R - Rp) ** 2 / (2 * S * S)) - np.exp(-(R + Rp) ** 2 / (2 * S * S))); out = np.trapz(K * rho[None, :], r, axis=1)
    if mask_small:
        dr = np.gradient(r); m = s < 3 * dr; out[m] = rho[m]
    return out
def menc(r, rho):   # CZ2 verbatim
    f = 4 * math.pi * r * r * rho; return np.concatenate([[0.0], np.cumsum(0.5 * (f[1:] + f[:-1]) * np.diff(r))]) + 4 * math.pi * rho[0] * r[0] ** 3 / 3
def sig_los(M, a, mode, a0, ge, xi0=0.0):   # CZ2 verbatim
    if mode in ("LOC", "TID"):
        r = rgrid(a, XCLIP); rho = plummer(r, M, a); gN = Gk * menc(r, rho) / r ** 2; gq = np.sqrt(gN * gN + ge * ge)
        X = xi_loc(r, nu(gq / a0) * gq, a0 / KAP, XCLIP) if mode == "LOC" else xi_tid(r, nu(gq / a0) * gN, a0 / KAP, XCLIP)
    else:
        X = xi0; r = rgrid(a, X); rho = plummer(r, M, a); gN = Gk * menc(r, rho) / r ** 2
    gh = gN if mode == "plain" else Gk * menc(r, smooth_rows(r, rho, X, mode in ("LOC", "TID"))) / r ** 2
    g = gN + (nu(np.sqrt(ge * ge + gh * gh) / a0) - 1) * gh; return math.sqrt(np.trapz(rho * r * g * 4 * math.pi * r * r, r) / (3 * M))
DATA = os.path.join(REPO, "real_research/data/dsph/mcconnachie2012_dsph.csv"); rows = []
for d in csv.DictReader(open(DATA)):   # CZ2 verbatim sample cuts
    if not d["e_sigma*"] or float(d["VMag"]) > -8 or d["Name"].startswith(("M32", "NGC", "Sagittarius")): continue
    rows.append(dict(name=d["Name"], sub=d["SubG"], D=float(d["D"]), L=10 ** (-0.4 * (float(d["VMag"]) - 4.83)), a=float(d["R2"]) / 1e3, s=float(d["sigma*"]), e=float(d["e_sigma*"]), MHI=float(d["M.HI"]) * 1e6 if d["M.HI"] else 0.0))
cz1 = json.load(open(os.path.join(CG, "CZ1_newtonian_external_field", "cz1.json")))
E2G = {r_["name"]: r_["ge_over_a0"] for r_ in cz1["dwarf|alt|E2|plain"]["rows"]}
GEV = {"E0": lambda d, a0: (200.0 ** 2 / d["D"]) if d["sub"] == "MW" else 0.0, "E1": lambda d, a0: Gk * M_MW / d["D"] ** 2 if d["sub"] == "MW" else 0.0,
       "E2": lambda d, a0: E2G[d["name"]] * A0SI["alt"] * CONV, "ISO": lambda d, a0: 0.0}
fi = [r_["name"] for r_ in rows].index("Fornax")
check("K-sample", len(rows) == 24, f"dwarf sample {len(rows)} (CZ2: 24)")
# --- fast fixed-width path: CZ2's smoothing as a trapezoid-weighted matrix, built once per (dwarf, L)
def kmat(r, s):
    R, Rp = r[:, None], r[None, :]; K = (Rp / (math.sqrt(2 * math.pi) * s * R)) * (np.exp(-(R - Rp) ** 2 / (2 * s * s)) - np.exp(-(R + Rp) ** 2 / (2 * s * s)))
    w = np.empty_like(r); dd = np.diff(r); w[0] = dd[0] / 2; w[-1] = dd[-1] / 2; w[1:-1] = (dd[:-1] + dd[1:]) / 2; return K * w[None, :]
def resmooth(r, gp, Km):
    """The outer S of form R on a spherical phantom: field -> enclosed phantom mass -> density -> Gaussian -> field."""
    Mp = gp * r * r / Gk; rp = np.gradient(Mp, r) / (4 * math.pi * r * r); return Gk * menc(r, Km @ rp) / r ** 2
MU, WMU = np.polynomial.legendre.leggauss(64)
def mplum(x): return x ** 3 / (1 + x * x) ** 1.5   # CZ5 verbatim
def ph_vec(h, ge, a0):   # CZ5's vector-nu l = 0 phantom monopole (plain3 / R3 lines, verbatim algebra)
    H = h[:, None]; Mu = MU[None, :]; gf = np.sqrt(np.maximum(H * H + ge * ge - 2 * ge * H * Mu, 1e-300)); Fr = (nu(gf / a0) - 1) * (-H + ge * Mu)
    if ge > 0: Fr = Fr - (float(nu(ge / a0)) - 1) * ge * Mu
    return -0.5 * (Fr @ WMU)
def sig_of(r, rho, g, M): return math.sqrt(max(np.trapz(rho * r * g * 4 * math.pi * r * r, r), 0) / (3 * M))
class Dwarf:
    """One dwarf at one L (L = 0: plain). Unit-mass profiles; every Upsilon reuses them."""
    def __init__(s, d, L):
        s.d, s.L = d, L; s.r = rgrid(d["a"], L); s.ru = plummer(s.r, 1.0, d["a"]); s.gNu = Gk * menc(s.r, s.ru) / s.r ** 2
        if L > 0: s.Km = kmat(s.r, L); s.ghu = Gk * menc(s.r, s.Km @ s.ru) / s.r ** 2
        else: s.Km = None; s.ghu = s.gNu
        s.giu = Gk * mplum(s.r / d["a"]) / s.r ** 2
    def sigma(s, M, a0, ge, form):
        r = s.r; rho = M * s.ru; gN = M * s.gNu; gh = M * s.ghu
        if form in ("SO", "plain"): return sig_of(r, rho, gN + (nu(np.sqrt(ge * ge + gh * gh) / a0) - 1) * gh, M)
        if form == "R":
            gp = (nu(np.sqrt(ge * ge + gh * gh) / a0) - 1) * gh; return sig_of(r, rho, gN + (resmooth(r, gp, s.Km) if s.Km is not None else gp), M)
        gi = M * s.giu; ph = ph_vec(gh if s.Km is not None else gi, ge, a0)
        if form == "D3R" and s.Km is not None: ph = resmooth(r, ph, s.Km)
        return sig_of(r, rho, gi + ph, M)   # D3SO / D3R
def run_dwarfs(L, jobs):
    """One dwarf at a time (one smoothing matrix in memory). jobs: (footing, field, form). Returns counts and per-dwarf rows."""
    cnt = {j: 0 for j in jobs}; det = {j: [] for j in jobs}
    for d in rows:
        dw = Dwarf(d, L)
        for j in jobs:
            foot, field, form = j; a0 = A0SI[foot] * CONV; ge = GEV[field](d, a0)
            sp = np.array([dw.sigma(u * d["L"] + 1.33 * d["MHI"], a0, ge, form) for u in UPS]); ok = bool((np.abs(sp - d["s"]) <= 2 * d["e"]).any())
            cnt[j] += ok; det[j].append(dict(name=d["name"], obs=d["s"], pred_U2=float(sp[20]), passed=ok))
        del dw
    return cnt, det
# KA3: CZ2's E1 plain and HALF (verbatim sig_los), KT15's universal 2 kpc on alt with its field and isolated
ka3 = {}
for foot in A0SI:
    a0 = A0SI[foot] * CONV
    for mode in ("plain", "HALF"):
        n = 0
        for d in rows:
            ge = GEV["E1"](d, a0); sp = np.array([sig_los(u * d["L"] + 1.33 * d["MHI"], d["a"], "plain" if mode == "plain" else "const", a0, ge, 0.5 * math.sqrt(Gk * (u * d["L"] + 1.33 * d["MHI"]) / a0)) for u in UPS])
            n += bool((np.abs(sp - d["s"]) <= 2 * d["e"]).any())
        ka3[f"{foot}|E1|{mode}"] = n
c2, _ = run_dwarfs(2.0, [("alt", "E0", "SO"), ("alt", "ISO", "SO")]); ka3["alt|E0|2kpc"] = c2[("alt", "E0", "SO")]; ka3["alt|ISO|2kpc"] = c2[("alt", "ISO", "SO")]
P(f"  KA3 counts: {ka3}")
check("KA3", ka3 == {"canonical|E1|plain": 18, "canonical|E1|HALF": 18, "alt|E1|plain": 18, "alt|E1|HALF": 18, "alt|E0|2kpc": 9, "alt|ISO|2kpc": 10},
      "CZ2's E1 plain 18 and HALF 18 per footing; KT15's universal 2 kpc on alt 9/24 with (200 km/s)^2/D and 10/24 isolated")
# KA3b: D3 at L = 0 on CZ5's grid reproduces CZ5's plain3
ka3b = {}
for foot in A0SI:
    a0 = A0SI[foot] * CONV; n = 0; fs = None
    for i, d in enumerate(rows):
        r = rgrid(d["a"], XCLIP); ge = GEV["E1"](d, a0); sp = []
        for u in UPS:
            M = u * d["L"] + 1.33 * d["MHI"]; rho = plummer(r, M, d["a"]); gi = Gk * M * mplum(r / d["a"]) / r ** 2; sp.append(sig_of(r, rho, gi + ph_vec(gi, ge, a0), M))
        sp = np.array(sp); n += bool((np.abs(sp - d["s"]) <= 2 * d["e"]).any())
        if i == fi: fs = float(sp[20])
    ka3b[foot] = (n, fs)
P(f"  KA3b plain3 counts / Fornax U2: {ka3b}")
check("KA3b", ka3b["canonical"][0] == 17 and ka3b["alt"][0] == 18 and abs(round(ka3b["canonical"][1], 2) - 12.59) < 1e-9 and abs(round(ka3b["alt"][1], 2) - 13.15) < 1e-9,
      "D3 at L = 0 on CZ5's grid reproduces CZ5's plain3 E1: 17 / 18, Fornax 12.59 / 13.15 km/s")
# V4 (dwarfs): with nu - 1 replaced by 1, R's re-smoothed field at L equals the field of rho smoothed at sqrt(2) L
v4d = []
Fo = rows[fi]
for L in LS:
    dw = Dwarf(Fo, L); r = dw.r; a = Fo["a"]; t = resmooth(r, dw.ghu, dw.Km); dref = Gk * menc(r, kmat(r, math.sqrt(2) * L) @ dw.ru) / r ** 2
    m = (r >= 0.1 * a) & (r <= 10 * a); v4d.append(float(np.max(np.abs(t[m] / dref[m] - 1)))); del dw
P("  V4 dwarfs (Fornax): max rel " + ", ".join(f"L {L}: {x:.1e}" for L, x in zip(LS, v4d)))
v4d_ok = {str(L): x <= 1e-3 for L, x in zip(LS, v4d)}
# graded counts
T2 = {foot: {} for foot in A0SI}
pj = [(foot, f, fm) for foot in A0SI for f, fm in (("E1", "plain"), ("E2", "plain"), ("E1", "D3SO"))]; pc, _ = run_dwarfs(0.0, pj)
plain = {foot: dict(E1=pc[(foot, "E1", "plain")], E2=pc[(foot, "E2", "plain")], D3=pc[(foot, "E1", "D3SO")]) for foot in A0SI}
P(f"  plain QUMOND on this grid: {plain}")
for L in LS:
    jobs = [(foot, f, fm) for foot in A0SI for f, fm in (("E1", "R"), ("E2", "R"), ("E1", "D3R"), ("E1", "SO"), ("E2", "SO"), ("E1", "D3SO"))]
    cnt, det = run_dwarfs(L, jobs)
    for foot in A0SI:
        row = {}
        for form in FORMS:
            dd = det[(foot, "E1", form)]
            row[form] = dict(E1=cnt[(foot, "E1", form)], E2=cnt[(foot, "E2", form)], D3=cnt[(foot, "E1", "D3" + form)], fornax_U2=dd[fi]["pred_U2"],
                             ok=bool(cnt[(foot, "E1", form)] >= 15), strict=bool(cnt[(foot, "E1", form)] >= plain[foot]["E1"]),
                             evaluable=(form == "SO" or v4d_ok[str(L)]), passed=[x["name"].split(" (")[0] for x in dd if x["passed"]])
        T2[foot][str(L)] = row
        P(f"  T2 [{foot}] L {L:5.3f} kpc: R E1 {row['R']['E1']}/24 (E2 {row['R']['E2']}, D3 {row['R']['D3']}, Fornax {row['R']['fornax_U2']:.2f}); "
          f"SO E1 {row['SO']['E1']}/24 (E2 {row['SO']['E2']}, D3 {row['SO']['D3']}, Fornax {row['SO']['fornax_U2']:.2f}); plain E1 {plain[foot]['E1']}")
RES["T2"] = T2; RES["T2_plain"] = plain; RES["V4_dwarfs"] = dict(zip(map(str, LS), v4d))

# ======================================================================= T3 SPARC (KT19's code verbatim, marked)
P("\n== T3 SPARC (KT19's statistic; PASS = SURVIVES SPARC)")
D = os.path.join(REPO, "real_research/data/sparc_data"); MRT = os.path.join(REPO, "real_research/data/SPARC_Lelli2016c.mrt")
G = 4.30091e-6; A0K = {"canonical": 9.3603e-11 * CONV, "alt": 1.1312e-10 * CONV}; EPS = 0.55
tab = {}
for line in open(MRT):   # KT19 verbatim
    p = line.split()
    if len(p) >= 18 and p[1].isdigit(): tab[p[0]] = dict(L=float(p[7]) * 1e9, Rd=float(p[11]), MHI=float(p[13]) * 1e9)
GAL = []
for fn in sorted(glob.glob(os.path.join(D, "*_rotmod.dat"))):   # KT19 verbatim
    nm = os.path.basename(fn).replace("_rotmod.dat", "")
    try: d = np.genfromtxt(fn, comments="#")
    except Exception: continue
    if d.ndim != 2 or d.shape[1] < 6 or len(d) < 3 or nm not in tab: continue
    R, Vo, eV, Vg, Vd, Vb = (d[:, j] for j in range(6)); o = np.argsort(R); R, Vo, eV, Vg, Vd, Vb = R[o], Vo[o], eV[o], Vg[o], Vd[o], Vb[o]
    Bg = Vg * np.abs(Vg); Bs = 0.5 * Vd * np.abs(Vd) + 0.7 * Vb * np.abs(Vb); q = (R > 0) & (Vo > 0) & (eV > 0) & (eV / np.maximum(Vo, 1e-9) < 0.1) & (Bg + Bs > 0)
    if q.sum() < 3: continue
    GAL.append(dict(name=nm, R=R, Vo=Vo, Bg=Bg, Bs=Bs, q=q, **tab[nm]))
P(f"  galaxies {len(GAL)}, points {sum(g['q'].sum() for g in GAL)}")
def Mprof(g, f):   # KT19 verbatim
    B = g["Bg"] + f * g["Bs"]; M = np.maximum(B * g["R"] / G, 0.0); Mm = np.maximum.accumulate(M); return Mm, int(np.sum(Mm != M))
def smoothed_ratio(g, f, xi, n=1500):   # KT19 verbatim (n fixed at KT19's default)
    R = g["R"]; Mm, _ = Mprof(g, f); Mb = 0.5 * f * g["L"] + 1.33 * g["MHI"]; Rl = R[-1]; Rd = max(g["Rd"], 0.1)
    r = np.geomspace(min(R[0], 0.01) * 0.1, Rl * 10 + 8 * xi + 10 * Rd, n)
    Mi = np.where(r < R[0], Mm[0] * (r / R[0]) ** 3, np.interp(r, R, Mm)); x = np.maximum(r - Rl, 0); Mi = Mi + np.where(r > Rl, max(Mb - Mm[-1], 0) * (1 - (1 + x / Rd) * np.exp(-x / Rd)), 0.0)
    dM = np.gradient(Mi, r); rho = np.maximum(dM, 0) / (4 * math.pi * r * r)
    Rr, Rp = r[:, None], r[None, :]; K = (Rp / (math.sqrt(2 * math.pi) * xi * Rr)) * (np.exp(-(Rr - Rp) ** 2 / (2 * xi * xi)) - np.exp(-(Rr + Rp) ** 2 / (2 * xi * xi)))
    rs = np.trapz(K * rho[None, :], r, axis=1)
    cm = lambda rh: np.concatenate([[0.0], np.cumsum(0.5 * (4 * math.pi * r[1:] ** 2 * rh[1:] + 4 * math.pi * r[:-1] ** 2 * rh[:-1]) * np.diff(r))])
    M0, M1 = cm(rho), cm(rs); return np.interp(R, r, M1) / np.maximum(np.interp(R, r, M0), 1e-30), float(M1[-1] / M0[-1])
def run(a0, f=1.0, filt=True, cache=None):   # KT19 verbatim (EPS 0.55, mass-scaled xi): KA4 only
    rr, med_in, allr = [], [], []
    for g in GAL:
        B = g["Bg"] + f * g["Bs"]; q = g["q"] & (B > 0); gb = B[q] / g["R"][q]; go = g["Vo"][q] ** 2 / g["R"][q]
        if filt:
            Mb = 0.5 * f * g["L"] + 1.33 * g["MHI"]; xi = EPS * math.sqrt(G * Mb / a0); key = (g["name"], f)
            if cache is not None and key in cache: ratio = cache[key]
            else: ratio = smoothed_ratio(g, f, xi)[0]; cache is not None and cache.__setitem__(key, ratio)
            gh = gb * ratio[q]
        else: gh = gb
        gm = gb + (nu(gh / a0) - 1) * gh; r = np.log10(go) - np.log10(gm); rr.append(math.sqrt(np.mean(r * r))); allr.append(r); med_in.append(r[g["R"][q] < 2 * g["Rd"]])
    a = np.concatenate(allr); i = np.concatenate(med_in); return dict(rms=float(math.sqrt(np.mean(np.square(rr)))), med=float(np.median(a)), med_inner=float(np.median(i)) if len(i) else None, n_inner=int(len(i)))
ka4 = {}
for foot, a0 in A0K.items():
    base = run(a0, filt=False); fl = run(a0, filt=True, cache={}); ka4[foot] = (round(fl["rms"], 4), round(fl["rms"] - base["rms"], 4)); RES.setdefault("T3_plain", {})[foot] = base
P(f"  KA4 KT19 eps 0.55 (filter rms, d rms): {ka4}")
check("KA4", ka4["canonical"] == (0.172, 0.0029) and ka4["alt"] == (0.1697, -0.0004), "KT19's code reproduces filter rms 0.1720 / 0.1697 and d rms +0.0029 / -0.0004")
def profiles(g, f, xi, n=1500):
    """KT19's smoothed_ratio grid and kernel (same lines), returning the source ratio, the R ratio per footing, and V4's two test ratios."""
    R = g["R"]; Mm, _ = Mprof(g, f); Mb = 0.5 * f * g["L"] + 1.33 * g["MHI"]; Rl = R[-1]; Rd = max(g["Rd"], 0.1)
    r = np.geomspace(min(R[0], 0.01) * 0.1, Rl * 10 + 8 * xi + 10 * Rd, n)
    Mi = np.where(r < R[0], Mm[0] * (r / R[0]) ** 3, np.interp(r, R, Mm)); x = np.maximum(r - Rl, 0); Mi = Mi + np.where(r > Rl, max(Mb - Mm[-1], 0) * (1 - (1 + x / Rd) * np.exp(-x / Rd)), 0.0)
    dM = np.gradient(Mi, r); rho = np.maximum(dM, 0) / (4 * math.pi * r * r)
    Rr, Rp = r[:, None], r[None, :]; K = (Rp / (math.sqrt(2 * math.pi) * xi * Rr)) * (np.exp(-(Rr - Rp) ** 2 / (2 * xi * xi)) - np.exp(-(Rr + Rp) ** 2 / (2 * xi * xi)))
    rs = np.trapz(K * rho[None, :], r, axis=1)
    cm = lambda rh: np.concatenate([[0.0], np.cumsum(0.5 * (4 * math.pi * r[1:] ** 2 * rh[1:] + 4 * math.pi * r[:-1] ** 2 * rh[:-1]) * np.diff(r))])
    M0, M1 = cm(rho), cm(rs); ratio = np.interp(R, r, M1) / np.maximum(np.interp(R, r, M0), 1e-30); out = dict(ratio=ratio, ratio_p={})
    def outer(gp):
        Mp = gp * r * r / G; rp = np.gradient(Mp, r) / (4 * math.pi * r * r); return np.interp(R, r, cm(np.trapz(K * rp[None, :], r, axis=1))) / np.maximum(np.interp(R, r, cm(rp)), 1e-30)
    ghs = G * np.maximum(M1, 1e-300) / r ** 2
    for foot, a0 in A0K.items(): out["ratio_p"][foot] = outer((nu(ghs / a0) - 1) * ghs)
    if g["name"] == "NGC2403":
        x2 = math.sqrt(2) * xi; K2 = (Rp / (math.sqrt(2 * math.pi) * x2 * Rr)) * (np.exp(-(Rr - Rp) ** 2 / (2 * x2 * x2)) - np.exp(-(Rr + Rp) ** 2 / (2 * x2 * x2)))
        out["v4_test"] = ratio * outer(ghs); out["v4_ref"] = np.interp(R, r, cm(np.trapz(K2 * rho[None, :], r, axis=1))) / np.maximum(np.interp(R, r, M0), 1e-30)
    return out
def stat(a0, foot, prof, form, f=1.0):
    rr, med_in, allr = [], [], []
    for g in GAL:
        B = g["Bg"] + f * g["Bs"]; q = g["q"] & (B > 0); gb = B[q] / g["R"][q]; go = g["Vo"][q] ** 2 / g["R"][q]; pr = prof[g["name"]]
        gh = gb * pr["ratio"][q]; gp = (nu(gh / a0) - 1) * gh
        if form == "R": gp = gp * pr["ratio_p"][foot][q]
        gm = gb + gp; r = np.log10(go) - np.log10(gm); rr.append(math.sqrt(np.mean(r * r))); allr.append(r); med_in.append(r[g["R"][q] < 2 * g["Rd"]])
    a = np.concatenate(allr); i = np.concatenate(med_in); return dict(rms=float(math.sqrt(np.mean(np.square(rr)))), med=float(np.median(a)), med_inner=float(np.median(i)) if len(i) else None)
def lab19(d, med): return "FAILS SPARC" if (d > 0.02 or abs(med) > 0.05) else "HURT" if d > 0.005 else "SURVIVES SPARC"   # KT19's frozen rule
eq = smoothed_ratio(GAL[0], 1.0, 0.5)[0]; chk = profiles(GAL[0], 1.0, 0.5)["ratio"]
check("K-SP", float(np.max(np.abs(eq - chk))) == 0.0, f"the fixed-L profile code returns KT19's smoothed_ratio exactly ({GAL[0]['name']}, xi 0.5): max diff {float(np.max(np.abs(eq - chk))):.1e}")
T3 = {foot: {} for foot in A0K}; v4s = {}
for L in LS:
    prof = {g["name"]: profiles(g, 1.0, L) for g in GAL}; pn = prof["NGC2403"]; m = pn["v4_ref"] >= 0.1
    v4s[str(L)] = float(np.max(np.abs(pn["v4_test"][m] / pn["v4_ref"][m] - 1))) if m.any() else float("nan")
    for foot, a0 in A0K.items():
        base = RES["T3_plain"][foot]; row = {}
        for form in FORMS:
            s_ = stat(a0, foot, prof, form); d_ = s_["rms"] - base["rms"]; lb = lab19(d_, s_["med"])
            row[form] = dict(**s_, d_rms=d_, label=lb, ok=bool(lb == "SURVIVES SPARC"), evaluable=(form == "SO" or (v4s[str(L)] == v4s[str(L)] and v4s[str(L)] <= 1e-3)))
        T3[foot][str(L)] = row
        P(f"  T3 [{foot}] L {L:5.3f} kpc: R rms {row['R']['rms']:.4f} d {row['R']['d_rms']:+.4f} med {row['R']['med']:+.4f} {row['R']['label']}; "
          f"SO rms {row['SO']['rms']:.4f} d {row['SO']['d_rms']:+.4f} med {row['SO']['med']:+.4f} {row['SO']['label']}")
    del prof
P("  V4 SPARC (NGC 2403): max rel " + ", ".join(f"L {k}: {v:.1e}" for k, v in v4s.items()))
RES["T3"] = T3; RES["V4_sparc"] = v4s
check("V4", all(x <= 1e-3 for x in v4d) and all(v == v and v <= 1e-3 for v in v4s.values()),
      f"reciprocal re-smoothing identity S_L S_L = S_sqrt2L: dwarfs max {max(v4d):.1e}, SPARC max {max(v for v in v4s.values() if v == v):.1e} (line 1e-3)")

# ======================================================================= summary of the small gates
P("\n== Small gates per (form, footing, L): T1 Cassini, T2 dwarfs E1, T3 SPARC, T4 planets")
ev = dict(T1=RES["checks"]["V2"]["ok"], T4=RES["checks"]["V3"]["ok"])
SUM = {}
for form in FORMS:
    for foot in A0SI:
        for L in LS:
            k = str(L); g = dict(T1=T1[foot][k][form]["ok"], T2=T2[foot][k][form]["ok"], T3=T3[foot][k][form]["ok"], T4=T4[foot][k][form]["ok"])
            ne = [t for t, e in (("T1", ev["T1"]), ("T2", T2[foot][k][form]["evaluable"]), ("T3", T3[foot][k][form]["evaluable"]), ("T4", ev["T4"])) if not e]
            SUM[f"{form}|{foot}|{k}"] = dict(gates=g, not_evaluable=ne)
            P(f"  {form:2s} [{foot:9s}] L {L:5.3f}: " + " ".join(f"{t} {'P' if v else 'F'}" for t, v in g.items()) + (f"  NOT EVALUABLE: {ne}" if ne else ""))
RES["summary"] = SUM
fin = all(math.isfinite(x) for foot in A0SI for L in LS for form in FORMS for x in (T1[foot][str(L)][form]["Q2"], T4[foot][str(L)][form]["Z"], T3[foot][str(L)][form]["rms"], T2[foot][str(L)][form]["fornax_U2"]))
check("K-finite", fin, "every graded value (Q2, worst Z, SPARC rms, Fornax sigma) is finite")
rss = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 2 ** 30; RES["peak_rss_GB"] = rss; RES["failed_checks"] = FAILS; RES["runtime_s"] = round(time.time() - T00, 1)
P(f"\npeak RSS {rss:.2f} GB; runtime {time.time() - T00:.0f} s; failed checks: {FAILS if FAILS else 0}")
sfx = "_MUTATE" if MUT else ""
open(os.path.join(HERE, f"fn1b_small{sfx}.out"), "w").write("\n".join(OUT) + "\n"); json.dump(RES, open(os.path.join(HERE, f"fn1b_small{sfx}.json"), "w"), indent=1, default=float)
sys.exit(1 if (MUT or FAILS) else 0)
