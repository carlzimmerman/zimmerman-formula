#!/usr/bin/env python3
"""FN6_powerlaw_screening small gates (criteria 5f0f4a5d99): T1 Cassini, T2 24 Local Group dwarfs, T3 SPARC, T4 planets,
form R (Phi_N + S Phi_ph[S rho]) only, both footings, on the frozen grid of 12 p x 4 L_MW, with the length per system
L = L_MW (M / 6e10 Msun)^p and M each system's own baryonic mass.
Engines: FN1b's (fn1b_small.py, copied verbatim in marked blocks, SHA-256 of the source below); KT33's cassini_v2 imported
read-only from FN1b's vendor_kt33/. Run: OMP_NUM_THREADS=1 nice -n 15 python3 -I -B fn6_small.py --part K/N [--mutate SEED --points p:L,...]
kappa = 1/2 FITTED and held fixed; not theory closed."""
import csv, glob, hashlib, importlib.util, json, math, os, resource, sys, time
sys.dont_write_bytecode = True
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"): os.environ[_v] = "1"
import numpy as np
import warnings   # this machine's Accelerate BLAS raises false FP flags in matmul (KT14, CW1, FN1b note it); results are checked finite
for _m in ("invalid value encountered in matmul", "divide by zero encountered in matmul", "overflow encountered in matmul"): warnings.filterwarnings("ignore", message=_m)
from scipy.optimize import brentq
from scipy.special import erf
T00 = time.time()
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(os.path.dirname(HERE))
RB = os.path.join(REPO, "rebuild_2026_10_22"); CG = os.path.join(REPO, "claude_goal_2026_11_03")
FN1B = os.path.join(REPO, "finish_2026_11_04", "FN1_action_call", "FN1b_fixed_length_static")
SRC_SHA = {"fn1b_small.py": "30822bf135f6b3be3a262131b688d114dbc740c7bf0edf12b64a1a0c85139248", "vendor_kt33/cassini_v2.py": "7d928d700ea4c371b4ac3551a19fa3fbda4f6bb8acac1d9842b4a689f13ac1bf"}
def _arg(k, d=None): return sys.argv[sys.argv.index(k) + 1] if k in sys.argv else d
PART = _arg("--part", "0/1"); KP, NP_ = (int(x) for x in PART.split("/")); SEED = _arg("--mutate"); MUT = SEED is not None
PTS = _arg("--points"); ODIR = _arg("--outdir", HERE); OUT = []; RES = {}; FAILS = []
TAG = f"mutate_s{SEED}" if MUT else f"part{KP}of{NP_}"
def P(s=""): print(s, flush=True); OUT.append(s)
def check(name, ok, msg):
    ok = bool(ok); P(f"{name} {'PASS' if ok else 'FAIL'}: {msg}"); RES.setdefault("checks", {})[name] = dict(ok=ok, msg=msg)
    if not ok: FAILS.append(name)
def rel(a, b): return abs(a / b - 1) if b != 0 else float("inf")
for k_, h_ in SRC_SHA.items():
    got = hashlib.sha256(open(os.path.join(FN1B, k_), "rb").read()).hexdigest(); check(f"K-src {k_}", got == h_, f"FN1b source SHA-256 {got[:16]}... (copied from {h_[:16]}...)")
# ---- frozen grid and the power-law length (criteria 5f0f4a5d99)
PS = [-0.5, -0.25, 0.0, 0.1, 0.2, 0.3, 0.35, 0.4, 0.45, 0.5, 0.6, 0.75]; LMWS = [1.0, 1.5, 2.0, 3.0]; M0 = 6.0e10
def Lof(LMW, p, M): return LMW * (M / M0) ** p   # kpc; M in Msun
SWITCH = 50.0   # Sun's sigma = L/r_M above which FN1b's exact linear response is used (validated by FN1b's V2/V3 at 20 and 50 r_M); at or below, the numeric engines
P(f"FN6 small gates [{TAG}] (criteria 5f0f4a5d99); form R; kappa = 1/2 FITTED; not theory closed")

# ---- verbatim from FN1b's fn1b_small.py lines 24-25 (constants); source SHA-256 in SRC_SHA
KAP = 0.5; A0SI = {"canonical": 9.3603e-11, "alt": 1.1312e-10}; LS = [0.024, 0.1, 0.25, 0.5, 1.0, 2.0]; KPC = 3.0857e19
GEXT, CEIL, HEES = 2.32e-10, 5.2e-27, 9.0e-27; Gk = 4.30091e-6; CONV = 3.0857e19 / 1e6; XCLIP = 200.0; M_MW = 7.0e10
# ---- end of verbatim lines 24-25

# ---- verbatim from FN1b's fn1b_small.py lines 28-29 (board-law simple nu); source SHA-256 in SRC_SHA
nu_s = lambda y: 0.5 + np.sqrt(0.25 + 1 / np.maximum(y, 1e-300))
dnu_s = lambda y: -1 / (2 * np.maximum(y, 1e-300) ** 2 * np.sqrt(0.25 + 1 / np.maximum(y, 1e-300)))
# ---- end of verbatim lines 28-29

nu, dnu = nu_s, dnu_s
def eta_newton(a0):   # FN1b's, without its nu = 1 twin
    eo = GEXT / a0; return brentq(lambda y: float(nu_s(y)) * y - eo, 1e-9, eo)
def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path); m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m
CV = load("kt33_cassini_v2", os.path.join(FN1B, "vendor_kt33", "cassini_v2.py")); GMc = CV.GM

# ---- verbatim from FN1b's fn1b_small.py lines 43-43 (T1 linear response); source SHA-256 in SRC_SHA
def q_lin(eta, sig): return (4 / 45) * math.sqrt(2 / math.pi) * eta * float(dnu(eta)) / sig ** 3
# ---- end of verbatim lines 43-43

# ---- verbatim from FN1b's fn1b_small.py lines 78-102 (T4: CZ3/AZ12 planet code, linear-response grade); source SHA-256 in SRC_SHA
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
# ---- end of verbatim lines 78-102

# ---- FN6 addition (not in FN1b): form R's planet monopole at any width, used where the Sun's sigma <= SWITCH.
# S applied to CZ3's SO phantom monopole (verbatim above) of the sigma-smoothed Sun, through the exact smeared-shell kernel
# of the same Gaussian, by parts (no density derivative): M~(r) = -int M_ph(s) dW(r, s)/ds ds, with M_ph(s) = s^2 F_SO(s).
def dWds(r, s, sg):
    """d/ds of the fraction of a unit shell of radius s, smeared by a 3D Gaussian of width sg, inside radius r."""
    R = r[:, None]; S = s[None, :]; sh = np.broadcast(R, S).shape; t = np.broadcast_to(R * S / sg ** 2, sh); pre = np.broadcast_to(sg / (math.sqrt(2 * math.pi) * S * S), sh)
    out = np.empty(sh); sm = t < 0.1; e0 = np.exp(-(R * R + S * S) / (2 * sg * sg))
    out[sm] = (2 * pre * e0 * (-(t ** 3) / 3) * (1 + t ** 2 / 10 + t ** 4 / 280))[sm]   # 2 pre e0 (sinh t - t cosh t), series
    A = np.exp(-(R - S) ** 2 / (2 * sg * sg)); B = np.exp(-(R + S) ** 2 / (2 * sg * sg)); out[~sm] = (pre * ((1 - t) * A - (1 + t) * B))[~sm]
    return out
def outer_field(F, r, sg, smax, n=20000, smin=1e-10):
    ls = np.linspace(math.log(smin), math.log(smax), n); s = np.exp(ls); M = s * s * F(s); out = np.empty_like(r)
    for i in range(0, len(r), 64):
        rr = r[i:i + 64]; out[i:i + 64] = -np.trapz(M[None, :] * dWds(rr, s, sg) * s[None, :], ls, axis=1) / rr ** 2
    return out
def grade_R_num(sig, eta, rMp, a0, N=160):
    """AZ12/CZ3's grade (rate() verbatim) with A(r) = a0 F_R(r / r_M): r in r_M, fields in a0, host field eta (Newtonian)."""
    Fso = lambda s: monopole(gh_pt(s, sig), 1.0, eta, N); rows = {}
    for nm, d in PL.items():
        e = ECC[nm]; a = d["a_au"] * AU; nn = math.sqrt(GMp / a ** 3); smax = a * (1 + e) / rMp + 12 * sig
        rt = rate(lambda r: a0 * outer_field(Fso, r / rMp, sig, smax), a, e, nn, 256) * YR / MAS; rows[nm] = dict(rate_mas_yr=rt, Z=abs(rt) / max(d["EPM"], d["INPOP"]))
    return rows
def identity_R(sig, rMp):
    """V3R(b): with nu - 1 -> 1 and no host field, F_R must equal the field of the Sun smoothed at sqrt(2) sigma (S_L S_L = S_sqrt2L)."""
    idm = 0.0
    for nm, d in PL.items():
        e = ECC[nm]; r = d["a_au"] * AU * (1 - e * np.cos(np.linspace(0, math.pi, 64))) / rMp
        F = outer_field(lambda s: gh_pt(s, sig), r, sig, d["a_au"] * AU * (1 + e) / rMp + 12 * sig); idm = max(idm, float(np.max(np.abs(F / gh_pt(r, math.sqrt(2) * sig) - 1))))
    return idm

# ---- verbatim from FN1b's fn1b_small.py lines 124-186 (T2: CZ2's dwarf code, FN1b's fixed-width Dwarf class); source SHA-256 in SRC_SHA
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
# ---- end of verbatim lines 124-186

# ---- verbatim from FN1b's fn1b_small.py lines 256-295 (T3: KT19's SPARC sample and plain statistic); source SHA-256 in SRC_SHA
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
# ---- end of verbatim lines 256-295

# ---- verbatim from FN1b's fn1b_small.py lines 301-327 (T3: FN1b's profile and R statistic, KT19's rule); source SHA-256 in SRC_SHA
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
# ---- end of verbatim lines 301-327


# ======================================================================= FN6: masses, MUTATE factors, checks, grid
ETA = {foot: eta_newton(a0) for foot, a0 in A0SI.items()}
BASE = {foot: run(a0, filt=False) for foot, a0 in A0K.items()}   # KT19's plain QUMOND rms on this sample (FN1b's T3_plain)
FAC = dict(Sun=1.0, dw=[1.0] * len(rows), gal=[1.0] * len(GAL), MW=1.0)
if MUT:   # pooled shuffle of the reference masses among the 181 systems (Sun, 24 dwarfs, KT19's 155 galaxies, Milky Way), before L is assigned (criteria: MUTATE)
    sys.path.insert(0, os.path.join(RB, "UX5_mw_stellar_mass")); import ux5_core   # first, so the vendored module finds it
    K33 = load("kt33_mw_reciprocal", os.path.join(FN1B, "vendor_kt33", "mw_reciprocal.py")); Cc = K33.C; gm_ = K33.gas_mass()
    IPm = [K33.rho_cell(c)[1] for c in K33.cells() if Cc.L.RD_TAG[0] <= c["rd"] <= Cc.L.RD_TAG[1] and Cc.L.MSTAR_TAG[0] <= K33.rho_cell(c)[1] <= Cc.L.MSTAR_TAG[1]]
    mw_ref = float(np.median(np.array(IPm) + gm_)); names = ["Sun"] + [d["name"] for d in rows] + [g["name"] for g in GAL] + ["Milky Way"]
    ref = np.array([1.0] + [2.0 * d["L"] + 1.33 * d["MHI"] for d in rows] + [0.5 * g["L"] + 1.33 * g["MHI"] for g in GAL] + [mw_ref])
    perm = np.random.default_rng(int(SEED)).permutation(len(ref)); fac = ref[perm] / ref; n1 = 1 + len(rows)
    FAC = dict(Sun=float(fac[0]), dw=[float(x) for x in fac[1:n1]], gal=[float(x) for x in fac[n1:n1 + len(GAL)]], MW=float(fac[-1]))
    RES["mutate"] = dict(seed=int(SEED), n_systems=len(ref), MW_ref_mass=mw_ref, Sun_gets=names[perm[0]], Sun_mass=float(ref[perm[0]]), MW_gets=names[perm[-1]], MW_mass=float(ref[perm[-1]]),
                         Fornax_gets=names[perm[1 + fi]], factors=FAC)
    P(f"  MUTATE seed {SEED}: the Sun gets {names[perm[0]]} ({ref[perm[0]]:.3g} Msun), the Milky Way {names[perm[-1]]} ({ref[perm[-1]]:.3g}), Fornax {names[perm[1 + fi]]}")
if KP == 0 and not MUT:
    P("\n== known answer KA2 and validation (run once, part 0)")
    ka2 = {}
    for foot, a0 in A0SI.items():
        rM = math.sqrt(GMc / a0); pref = 1.5 * a0 / rM; LMW2 = 0.5 * math.sqrt(GMc * M0 / a0) / KPC; Ls = Lof(LMW2, 0.5, 1.0); sig = Ls * KPC / rM
        x = abs(CV.quadrupole(ETA[foot], sig, 0.0)["q_flux_signed"]) * pref / CEIL; xr = abs(CV.quadrupole(ETA[foot], sig, sig)["q_hessian_signed"]) * pref / CEIL
        ka2[foot] = dict(L_MW_kpc=LMW2, L_sun_pc=Ls * 1e3, sigma_rM=sig, KT25_flux_x_ceiling=x, R_x_ceiling=xr)
        P(f"  KA2 [{foot}] p 1/2, L_MW = r_M(6e10)/2 = {LMW2:.4f} kpc: Sun's L {Ls * 1e3:.5f} pc = {sig:.12f} r_M; KT25's form (SO, flux) {x:.4f} x ceiling; form R {xr:.4f} x")
    check("KA2", abs(ka2["canonical"]["KT25_flux_x_ceiling"] / 1.179 - 1) <= 0.01, f"p = 1/2 with L = r_M/2 gives CZ2's KT25 Cassini ratio 1.179 x canonical within 1 %: {ka2['canonical']['KT25_flux_x_ceiling']:.4f} (alt {ka2['alt']['KT25_flux_x_ceiling']:.4f}, CZ2 2.97, reported)")
    kd = {}   # reported check of the mass-scaled length path on the dwarfs: p = 1/2, L = r_M/2 per Upsilon is CZ2's HALF mode (SO form)
    for foot in A0SI:
        a0 = A0SI[foot] * CONV; LMWd = 0.5 * math.sqrt(Gk * M0 / a0); n = 0
        for d in rows:
            ge = GEV["E1"](d, a0); ok = False
            for u in UPS:
                M = u * d["L"] + 1.33 * d["MHI"]; dw = Dwarf(d, Lof(LMWd, 0.5, M))
                if abs(dw.sigma(M, a0, ge, "SO") - d["s"]) <= 2 * d["e"]: ok = True; break
            n += ok
        kd[foot] = n
    check("K-HALF-dwarfs", kd == {"canonical": 18, "alt": 18}, f"reported: the per-Upsilon power-law length at p = 1/2, L = r_M/2 (SO form) gives CZ2's HALF E1 counts 18 / 18: {kd['canonical']} / {kd['alt']}")
    RES["KA2"] = ka2; RES["K_HALF_dwarfs"] = kd; v2, v3 = [], []
    for foot, a0 in A0SI.items():
        rM = math.sqrt(GMc / a0); rMp = math.sqrt(GMp / a0)
        for sg in (20.0, 50.0):
            num = CV.quadrupole(ETA[foot], sg, sg)["q_hessian_signed"]; an = q_lin(ETA[foot], sg * math.sqrt(2)); v2.append(abs(num / an - 1))
            zn = grade_R_num(sg, ETA[foot], rMp, a0)["Saturn"]["Z"]; za = grade_lin(kfac(ETA[foot]) * GMp / (sg * rMp * math.sqrt(2)) ** 3)["Saturn"]["Z"]; v3.append(abs(zn / za - 1))
            P(f"  V2/V3R [{foot}] sigma {sg:.0f} r_M, form R: Cassini q numeric/analytic {num / an:.6f}; Saturn Z numeric/analytic {zn / za:.6f}")
    check("V2", max(v2) <= 0.02, f"form R Cassini, KT33 numeric against the linear response at sigma 20, 50 r_M: max |ratio - 1| {max(v2):.2e} (FN1b's line 0.02)")
    check("V3R", max(v3) <= 0.02, f"form R planets, numeric engine against the linear response at sigma 20, 50 r_M (Saturn Z): max |ratio - 1| {max(v3):.2e} (FN1b's V3 line 0.02)")
ORDER = [20] + [j for k in range(1, 21) for j in (20 - k, 20 + k)]   # Upsilon_V = 2 first; a dwarf passes if any Upsilon in [1, 3] does
def run_point(p, LMW):
    t0 = time.time(); R_ = dict(p=p, L_MW=LMW); Ls = Lof(LMW, p, 1.0 * FAC["Sun"]); R_["L_sun_kpc"] = Ls; R_["T1"], R_["T4"], R_["T2"], R_["T3"] = {}, {}, {}, {}
    for foot, a0 in A0SI.items():
        rM = math.sqrt(GMc / a0); pref = 1.5 * a0 / rM; etaN = ETA[foot]; sig = Ls * KPC / rM
        if sig > SWITCH: q = q_lin(etaN, sig * math.sqrt(2)); eng = "linear response"
        else: q = CV.quadrupole(etaN, sig, sig)["q_hessian_signed"]; eng = "KT33 numeric"
        Q2 = abs(q) * pref; R_["T1"][foot] = dict(sigma_rM=sig, engine=eng, q=q, Q2=Q2, x_ceiling=Q2 / CEIL, x_hees=Q2 / HEES, ok=bool(Q2 <= CEIL), evaluable=True)
        rMp = math.sqrt(GMp / a0); sp = Ls * KPC / rMp
        if sp > SWITCH: Le = Ls * KPC * math.sqrt(2); g = grade_lin(kfac(etaN) * GMp / Le ** 3); eng = "linear response"; idr = None
        else: g = grade_R_num(sp, etaN, rMp, a0); eng = "numeric R"; idr = identity_R(sp, rMp)
        w = max(g, key=lambda k: g[k]["Z"]); R_["T4"][foot] = dict(sigma_rM=sp, engine=eng, worst=w, Z=g[w]["Z"], Saturn_Z=g["Saturn"]["Z"], identity_maxrel=idr, ok=bool(g[w]["Z"] <= 2), evaluable=bool(idr is None or idr <= 1e-3))
    # T2: CZ2's model, E1 field, form R; each dwarf's L from its own mass at each Upsilon_V (as CZ2's HALF mode does)
    cnt = {f: 0 for f in A0SI}; psd = {f: [] for f in A0SI}; fz = {}; under = 0; Lfx = None
    for i, d in enumerate(rows):
        ok = {f: False for f in A0SI}; cur = (None, None)
        for j in ORDER:
            u = UPS[j]; M = u * d["L"] + 1.33 * d["MHI"]; L = Lof(LMW, p, M * FAC["dw"][i])
            if cur[0] != L: cur = (L, Dwarf(d, L))
            dw = cur[1]
            if j == 20:
                under += bool(L < 3 * d["a"] * ((dw.r[-1] / dw.r[0]) ** (1 / (len(dw.r) - 1)) - 1))
                if i == fi: Lfx = L
            for foot in A0SI:
                if ok[foot]: continue
                a0 = A0SI[foot] * CONV; s_ = dw.sigma(M, a0, GEV["E1"](d, a0), "R")
                if i == fi and j == 20: fz[foot] = s_
                if abs(s_ - d["s"]) <= 2 * d["e"]: ok[foot] = True
            if all(ok.values()): break
        for f in A0SI: cnt[f] += ok[f]; ok[f] and psd[f].append(d["name"])
        del cur
    v4d = 0.0; Fo = rows[fi]
    for j in (0, 20, 40):   # FN1b's V4 (dwarfs) on Fornax, at its own L for Upsilon_V = 1, 2, 3
        L = Lof(LMW, p, (UPS[j] * Fo["L"] + 1.33 * Fo["MHI"]) * FAC["dw"][fi]); dw = Dwarf(Fo, L); r = dw.r; a = Fo["a"]
        t = resmooth(r, dw.ghu, dw.Km); dref = Gk * menc(r, kmat(r, math.sqrt(2) * L) @ dw.ru) / r ** 2; m = (r >= 0.1 * a) & (r <= 10 * a); v4d = max(v4d, float(np.max(np.abs(t[m] / dref[m] - 1)))); del dw
    for f in A0SI: R_["T2"][f] = dict(E1=cnt[f], fornax_U2=fz[f], passed=psd[f], ok=bool(cnt[f] >= 15), evaluable=bool(v4d <= 1e-3))
    R_["T2_meta"] = dict(V4_fornax=v4d, L_fornax_U2_kpc=Lfx, n_under_resolved_U2=under)
    # T3: KT19's model and statistic, each galaxy at its own L (KT19's Mb)
    prof = {}; unres = 0; Lg = []
    for k, g in enumerate(GAL):
        L = Lof(LMW, p, (0.5 * g["L"] + 1.33 * g["MHI"]) * FAC["gal"][k]); prof[g["name"]] = profiles(g, 1.0, L); Lg.append(L)
        Rg = g["R"]; rr = np.geomspace(min(Rg[0], 0.01) * 0.1, Rg[-1] * 10 + 8 * L + 10 * max(g["Rd"], 0.1), 1500); unres += bool(L < 3 * float(np.max(np.interp(Rg, rr[1:], np.diff(rr)))))
    pn = prof["NGC2403"]; m = pn["v4_ref"] >= 0.1; v4s = float(np.max(np.abs(pn["v4_test"][m] / pn["v4_ref"][m] - 1))) if m.any() else float("nan")
    for foot, a0 in A0K.items():
        s_ = stat(a0, foot, prof, "R"); d_ = s_["rms"] - BASE[foot]["rms"]; lb = lab19(d_, s_["med"])
        R_["T3"][foot] = dict(**s_, d_rms=d_, label=lb, ok=bool(lb == "SURVIVES SPARC"), evaluable=bool(v4s == v4s and v4s <= 1e-3))
    R_["T3_meta"] = dict(V4_ngc2403=v4s, L_min_kpc=min(Lg), L_med_kpc=float(np.median(Lg)), L_max_kpc=max(Lg), n_under_resolved=unres); del prof
    R_["runtime_s"] = round(time.time() - t0, 1); R_["rss_GB"] = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 2 ** 30
    return R_
GRID = [(p, L) for p in PS for L in LMWS]
if PTS: todo = [tuple(float(x) for x in s.split(":")) for s in PTS.split(",")]
else: todo = [pt for i, pt in enumerate(GRID) if i % NP_ == KP]
CK = os.path.join(ODIR, f"fn6_small_{TAG}.jsonl"); done = {}
if os.path.exists(CK):
    for ln in open(CK):
        o = json.loads(ln); done[(o["p"], o["L_MW"])] = o
P(f"\n== grid points this process: {len(todo)} ({len(done)} already in the checkpoint)")
ALL = {}
for p, LMW in todo:
    if (p, LMW) in done: o = done[(p, LMW)]
    else:
        o = run_point(p, LMW); open(CK, "a").write(json.dumps(o, default=float) + "\n")
    ALL[(p, LMW)] = o
    gs = {f: " ".join(f"{t} {'P' if o[t][f]['ok'] else 'F'}{'' if o[t][f]['evaluable'] else '(NE)'}" for t in ("T1", "T4", "T2", "T3")) for f in A0SI}
    P(f"  p {p:+.2f} L_MW {LMW:.1f}: L_sun {o['L_sun_kpc'] * 1e3:.4g} pc | can: {gs['canonical']} (Q2 {o['T1']['canonical']['x_ceiling']:.2e}x, Z {o['T4']['canonical']['Z']:.2e}, dw {o['T2']['canonical']['E1']}, "
      f"SP d {o['T3']['canonical']['d_rms']:+.4f}) | alt: {gs['alt']} (Q2 {o['T1']['alt']['x_ceiling']:.2e}x, Z {o['T4']['alt']['Z']:.2e}, dw {o['T2']['alt']['E1']}, SP d {o['T3']['alt']['d_rms']:+.4f}) [{o['runtime_s']:.0f} s]")
fin = all(math.isfinite(x) for o in ALL.values() for f in A0SI for x in (o["T1"][f]["Q2"], o["T4"][f]["Z"], o["T3"][f]["rms"], o["T2"][f]["fornax_U2"]))
check("K-finite", fin, "every graded value (Q2, worst Z, SPARC rms, Fornax sigma) is finite")
RES["peak_rss_GB"] = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 2 ** 30; RES["failed_checks"] = FAILS; RES["runtime_s"] = round(time.time() - T00, 1); RES["base_T3"] = BASE; RES["eta_N"] = ETA
P(f"\npeak RSS {RES['peak_rss_GB']:.2f} GB; runtime {RES['runtime_s']:.0f} s; failed checks: {FAILS if FAILS else 0}")
open(os.path.join(ODIR, f"fn6_small_{TAG}.out"), "w").write("\n".join(OUT) + "\n"); json.dump(RES, open(os.path.join(ODIR, f"fn6_small_{TAG}.json"), "w"), indent=1, default=float)
sys.exit(1 if FAILS else 0)
