#!/usr/bin/env python3
"""FN6_powerlaw_screening extended V4, POST-RESULT and reported only (AMENDMENTS.md): FN1b's V4 identity (S_L S_L = S_sqrt2L,
nu - 1 -> 1) run on every dwarf and every SPARC galaxy at its own power-law length, at the points that pass all five gates.
The frozen V4 (Fornax and NGC 2403 only) is in fn6_small.py and is unchanged.
Engines: FN1b's (fn1b_small.py, copied verbatim in marked blocks, SHA-256 of the source below); KT33's cassini_v2 imported
read-only from FN1b's vendor_kt33/. Run: OMP_NUM_THREADS=1 nice -n 15 python3 -I -B fn6_v4x.py (after fn6_label.py)
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


# ======================================================================= FN6 extended V4 (post-result, reported): every system at its own L
lab = json.load(open(os.path.join(HERE, "fn6_label.json"))); PTS_ = sorted({tuple(x) for f in A0SI for x in lab["labels"][f]["passing"]})
P(f"FN6 extended V4 [post-result, reported] (criteria 5f0f4a5d99); form R; kappa = 1/2 FITTED; not theory closed\n  points: {PTS_}")
V4X = {}
for p, LMW in PTS_:
    t0 = time.time(); dmax, dworst, gmax, gworst, nd_bad, ng_bad = 0.0, None, 0.0, None, 0, 0
    for d in rows:   # FN1b's V4 lines for Fornax, applied to every dwarf at its own L for Upsilon_V = 1, 2, 3
        e_ = 0.0
        for j in (0, 20, 40):
            L = Lof(LMW, p, UPS[j] * d["L"] + 1.33 * d["MHI"]); dw = Dwarf(d, L); r = dw.r; a = d["a"]
            t = resmooth(r, dw.ghu, dw.Km); dref = Gk * menc(r, kmat(r, math.sqrt(2) * L) @ dw.ru) / r ** 2; m = (r >= 0.1 * a) & (r <= 10 * a); e_ = max(e_, float(np.max(np.abs(t[m] / dref[m] - 1)))); del dw
        nd_bad += e_ > 1e-3
        if e_ > dmax: dmax, dworst = e_, d["name"]
    for g in GAL:   # FN1b's V4 lines for NGC 2403 (profiles' own branch, reached by the name), applied to every galaxy at its own L
        L = Lof(LMW, p, 0.5 * g["L"] + 1.33 * g["MHI"]); pn = profiles(dict(g, name="NGC2403"), 1.0, L); m = pn["v4_ref"] >= 0.1
        e_ = float(np.max(np.abs(pn["v4_test"][m] / pn["v4_ref"][m] - 1))) if m.any() else float("nan"); ng_bad += not (e_ <= 1e-3)
        if e_ > gmax: gmax, gworst = e_, g["name"]
    V4X[f"{p}|{LMW}"] = dict(dwarfs_max=dmax, dwarfs_worst=dworst, dwarfs_over_line=int(nd_bad), sparc_max=gmax, sparc_worst=gworst, sparc_over_line=int(ng_bad), runtime_s=round(time.time() - t0, 1))
    P(f"  (p {p}, L_MW {LMW}): dwarfs max {dmax:.1e} ({dworst}), {nd_bad} of 24 over 1e-3; SPARC max {gmax:.1e} ({gworst}), {ng_bad} of {len(GAL)} over 1e-3 [{time.time() - t0:.0f} s]")
RES["V4X"] = V4X; RES["peak_rss_GB"] = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 2 ** 30; RES["runtime_s"] = round(time.time() - T00, 1); RES["failed_checks"] = FAILS
P(f"\npeak RSS {RES['peak_rss_GB']:.2f} GB; runtime {RES['runtime_s']:.0f} s; failed checks: {FAILS if FAILS else 0}")
open(os.path.join(HERE, "fn6_v4x.out"), "w").write("\n".join(OUT) + "\n"); json.dump(RES, open(os.path.join(HERE, "fn6_v4x.json"), "w"), indent=1, default=float)
