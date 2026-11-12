#!/usr/bin/env python3
"""
NIM2 -- NMB1's gate (NIMBLE-A, NIMBLE-B; RRL, BHB curves of DESI DR2 Results III) extended to three radii,
30, 50 and 80 kpc. Does the third radius add power?

Criteria: FROZEN_CRITERIA.md (sha256 in FREEZE_STAMP.txt), written before this file.
Usage:    python3 -I nim2.py /path/to/desi-dr2-mw-mass-figdata.zip
Writes:   nim2.out, nim2_results.json, nim2_mut.out   (next to this file)

Order is fixed: KA1..KA7, then the mutations, then the graded numbers. A failed known-answer check stops the
script before any graded number. Functions copied from NMB1 (nmb1.py) and MWJ1 (mwj1.py, M_sph); nothing of
theirs is run in place. kappa = 1/2 FITTED; not theory closed. Adopts nothing.
"""
import sys, os, io, csv, json, math, hashlib, zipfile, collections
import numpy as np
from scipy.stats import ncx2

HERE = os.path.dirname(os.path.abspath(__file__))
ZIP = sys.argv[1]
P = "desi-dr2-mw-mass-figdata/"
MD5 = "5b0cc3aa9947286eb9348e947d01182d"

# ---------------------------------------------------------------- constants (SI), as NMB1
G, MSUN, KPC = 6.67430e-11, 1.98847e30, 3.0856775814913673e19
MB = 6.681e10 * MSUN
A0 = {"canonical": 9.36e-11, "alt": 1.13e-10}
FOOT = ("canonical", "alt")
E_N = 0.01273
RAD = (30.0, 50.0, 80.0)
RAD2 = (30.0, 80.0)
L = math.log10(80.0 / 30.0); L1 = math.log10(50.0 / 30.0); L2 = math.log10(80.0 / 50.0)
QGATE, Q3 = 8.02, 14.16
QGATE2 = 6.180
LAMBDA = 0.5
TABLE4_ALL = {30.0: (11.423 - 11.0, 0.022), 50.0: (11.654 - 11.0, 0.0255), 80.0: (11.804 - 11.0, 0.0345)}
T4R = [20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80]
T4 = {"rrl": [1.97, 2.38, 2.65, 3.11, 3.79, 4.38, 4.81, 5.19, 5.49, 5.79, 6.05, 6.24, 6.40],
      "bhb": [1.93, 2.24, 2.63, 2.97, 3.37, 3.89, 4.34, 4.72, 5.04, 5.43, 5.79, 6.10, 6.38]}
FIG8 = {("nimble-b", "rrl", 80.0): -6.50, ("nimble-a", "bhb", 80.0): -7.54,
        ("nimble-a", "rrl", 30.0): +5.91, ("nimble-b", "bhb", 30.0): -1.19}
NMB1_TH = (11.4059, 0.0270, 11.8047, 0.0567)
NMB1_Q = {("E1", "canonical"): 4.89, ("E1", "alt"): 2.91, ("E0", "canonical"): 2.40, ("E0", "alt"): 0.05}

OUT = open(os.path.join(HERE, "nim2.out"), "w")
def say(s=""):
    print(s); OUT.write(str(s) + "\n"); OUT.flush()
def sec(t):
    say("\n" + "=" * 110); say(t); say("=" * 110)
KA_FAIL = []
def ka(name, ok, detail=""):
    say(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f"\n         ({detail})" if detail else ""))
    if not ok: KA_FAIL.append(name)
    return ok
def stop_if_failed():
    if KA_FAIL:
        say("\nSTOPPED: known-answer check failed -> NO VERDICT as frozen. No graded number was computed.")
        json.dump({"lane": "NIM2", "label": "NO VERDICT (stopped at " + KA_FAIL[0].split()[0] + ")"},
                  open(os.path.join(HERE, "nim2_results.json"), "w"), indent=1)
        sys.exit(0)

# ---------------------------------------------------------------- McMillan 2017 M_sph (copied from mwj1.py, its own constants)
TRAPZ = getattr(np, "trapezoid", None) or np.trapz
_G, _MSUN, _KPC = 6.674e-11, 1.989e30, 3.0857e19
_PC = _KPC / 1000.0; _MSUN_PC2 = _MSUN / _PC ** 2
MC = dict(thin =dict(S0=896.0*_MSUN_PC2, Rd=2.50*_KPC, zd=0.300*_KPC, Rm=0.0, vert="exp"),
          thick=dict(S0=183.0*_MSUN_PC2, Rd=3.02*_KPC, zd=0.900*_KPC, Rm=0.0, vert="exp"),
          HI   =dict(Sfid=10.0*_MSUN_PC2, Rfid=8.33*_KPC, Rd=7.00*_KPC, zd=0.085*_KPC, Rm=4.0*_KPC,  vert="sech2"),
          H2   =dict(Sfid= 2.0*_MSUN_PC2, Rfid=8.33*_KPC, Rd=1.50*_KPC, zd=0.045*_KPC, Rm=12.0*_KPC, vert="sech2"))
MBULGE, ABULGE = 9.23e9 * _MSUN, 0.70 * _KPC
def S0_of(c): return c["S0"] if "S0" in c else c["Sfid"] / math.exp(-c["Rm"] / c["Rfid"] - c["Rfid"] / c["Rd"])
def sigma_of_R(c, R):
    R = np.maximum(np.asarray(R, float), 1e-6 * _KPC); return S0_of(c) * np.exp(-c.get("Rm", 0.0) / R - R / c["Rd"])
def zcum(c, n=1201):
    zg = np.linspace(-10 * c["zd"], 10 * c["zd"], n)
    zz = (np.exp(-np.abs(zg) / c["zd"]) / (2 * c["zd"]) if c["vert"] == "exp" else 1.0 / np.cosh(zg / (2 * c["zd"])) ** 2 / (4 * c["zd"]))
    cum = np.concatenate([[0.0], np.cumsum((zz[1:] + zz[:-1]) / 2 * np.diff(zg))]); return zg, cum / cum[-1]
_MS = {}
def M_sph(r_kpc):
    if r_kpc not in _MS:
        r = float(r_kpc) * _KPC; tot = MBULGE * r ** 2 / (r + ABULGE) ** 2
        Rg = np.linspace(1e-4 * _KPC, min(r, 60 * _KPC), 4000); h = np.sqrt(np.maximum(r ** 2 - Rg ** 2, 0.0))
        for c in MC.values():
            zg, cum = zcum(c); tot += float(TRAPZ(2 * np.pi * Rg * sigma_of_R(c, Rg) * np.interp(h, zg, cum), Rg))
        _MS[r_kpc] = tot
    return _MS[r_kpc]
MSPH_TOT = M_sph(3000.0)
FSPH = {30.0: 0.9777, 50.0: M_sph(50.0) / MSPH_TOT, 80.0: 0.9972}

def m_hot(r):                                   # MB15, MWG1's model [Msun]
    return 4.3e10 * (r / 250.0) ** 1.5

# ---------------------------------------------------------------- the line (NMB1's, with optional hot gas)
def nu(y):
    return 1.0 / (1.0 - np.exp(-np.sqrt(np.maximum(np.asarray(y, float), 1e-14))))
MU = np.linspace(-1.0, 1.0, 4001)
def trapz(yv, xv):
    return float(np.sum((yv[1:] + yv[:-1]) * np.diff(xv)) / 2.0)
def M_line(r, a0, A=1.0, eN=0.0, gas=False):
    Mb = A * FSPH[r] * MB + (m_hot(r) * MSUN if gas else 0.0)
    gb = G * Mb / (r * KPC) ** 2 / a0
    if eN == 0.0:
        return float(nu(gb)) * Mb / MSUN / 1e11
    gm = np.sqrt(gb * gb + eN * eN + 2 * gb * eN * MU)
    return trapz(nu(gm) * (gb + eN * MU), MU) / 2.0 / gb * Mb / MSUN / 1e11
def mu_line(a0, A=1.0, eN=0.0, gas=False, rad=RAD):
    return np.array([math.log10(M_line(r, a0, A, eN, gas)) for r in rad])
H0 = 67.77e3 / 3.0856775814913673e22; RHOC = 3 * H0 ** 2 / (8 * math.pi * G)
M200 = 1.19e12 * MSUN; R200 = (3 * M200 / (4 * math.pi * 200 * RHOC)) ** (1 / 3); CN = 12.0
def mN(xx): return math.log(1 + xx) - xx / (1 + xx)
def mu_nfw(rad=RAD):
    return np.array([math.log10(M200 * mN(r * KPC / (R200 / CN)) / mN(CN) / MSUN / 1e11) for r in rad])

# ---------------------------------------------------------------- file access (as NMB1)
Z = zipfile.ZipFile(ZIP)
def rows(name):
    return list(csv.DictReader(io.TextIOWrapper(Z.open(P + name), encoding="utf-8")))
def interp_loglog(pts, x):
    pts = sorted(pts)
    if x < pts[0][0] * (1 - 1e-9) or x > pts[-1][0] * (1 + 1e-9): return float("nan")
    for (a, ma), (b, mb) in zip(pts, pts[1:]):
        if a * (1 - 1e-9) <= x <= b * (1 + 1e-9):
            if b == a: return ma
            f = (math.log(x) - math.log(a)) / (math.log(b) - math.log(a))
            return math.exp(math.log(ma) + f * (math.log(mb) - math.log(ma)))
    return float("nan")

def shrink(S, lam):
    return (1 - lam) * S + lam * np.diag(np.diag(S))
def corr_of(S):
    d = np.sqrt(np.diag(S)); return S / np.outer(d, d)
def gls(y, C, X, prec_factor=1.0):
    Ci = np.linalg.inv(C) * prec_factor
    V = np.linalg.inv(X.T @ Ci @ X)
    th = V @ X.T @ Ci @ y
    res = y - X @ th
    return th, V, float(res @ Ci @ res)

# ====================================================================================================
sec("NIM2  NMB1's gate extended to 30, 50 and 80 kpc   (criteria: FROZEN_CRITERIA.md, see FREEZE_STAMP.txt)")
say("     TEST lane. kappa = 1/2 FITTED; not theory closed. Adopts nothing.")
crit_sha = hashlib.sha256(open(os.path.join(HERE, "FROZEN_CRITERIA.md"), "rb").read()).hexdigest()
say(f"     criteria sha256 {crit_sha}")

sec("KNOWN-ANSWER CHECKS")
md5 = hashlib.md5(open(ZIP, "rb").read()).hexdigest()
ka("KA1 the file is the one named in the criteria", md5 == MD5, f"md5 {md5}")
stop_if_failed()

F10 = rows("fig10/desi-dr2-menc.csv")
CUR = collections.defaultdict(list)
for r in F10:
    CUR[(r["method"], r["tracer"])].append((float(r["r_kpc"]), float(r["Menc_med"]), float(r["Menc_lo"]), float(r["Menc_hi"])))
def data_at(method, tracer, r):
    c = CUR[(method, tracer)]
    med = interp_loglog([(a, m) for a, m, _, _ in c], r)
    lo = interp_loglog([(a, l) for a, _, l, _ in c], r)
    hi = interp_loglog([(a, h) for a, _, _, h in c], r)
    return math.log10(med), 0.5 * (math.log10(hi / med) + math.log10(med / lo)), med, lo, hi

worst = 0.0
for tr in ("rrl", "bhb"):
    for rr, tv in zip(T4R, T4[tr]):
        worst = max(worst, abs(data_at("joint", tr, float(rr))[2] - tv))
ka("KA2 fig10's joint rows reproduce Table 4's RRL and BHB columns (26 values, each within 0.011e11)",
   worst <= 0.011, f"largest difference {worst:.4f} e11")
stop_if_failed()

MOCK = {}; TRUE = {}
for tr, fig in (("rrl", "figA1"), ("bhb", "figA2")):
    t = collections.defaultdict(list)
    for r in rows(f"{fig}/truths.csv"): t[r["halo"]].append((float(r["r_kpc"]), float(r["Menc"])))
    TRUE[tr] = t
    for m in ("empdf", "gme", "nimble-a", "nimble-b"):
        d = collections.defaultdict(list)
        for r in rows(f"{fig}/{m}.csv"): d[(r["halo"], r["view"])].append((float(r["r_kpc"]), float(r["Menc_med"])))
        MOCK[(m, tr)] = d
KEYS = sorted(MOCK[("nimble-a", "rrl")].keys())
say(f"  mocks in the file: {len(KEYS)}")
def resid(method, tracer, r, key):
    est = interp_loglog(MOCK[(method, tracer)].get(key, [(1, 1)]), r)
    tru = interp_loglog(TRUE[tracer][key[0]], r)
    return math.log10(est / tru) if (est == est and tru == tru and est > 0) else float("nan")

worst3 = 0.0; det = []
for (m, tr, r), ref in FIG8.items():
    v = np.array([resid(m, tr, r, k) for k in KEYS]); v = v[~np.isnan(v)]
    med = (10 ** np.median(v) - 1) * 100
    worst3 = max(worst3, abs(med - ref)); det.append(f"{m} {tr} {r:.0f}: {med:+.2f} vs {ref:+.2f}")
ka("KA3 mock residuals reproduce Figure 8's median biases (four values, each within 2.5 points)",
   worst3 <= 2.5, "; ".join(det))
stop_if_failed()

def build(items, lam=LAMBDA):
    Rm = np.array([[resid(m, tr, r, k) for (m, tr, r) in items] for k in KEYS])
    ok = ~np.isnan(Rm).any(axis=1); Rm = Rm[ok]; N = Rm.shape[0]
    S = np.cov(Rm, rowvar=False, ddof=1)
    Sres = shrink(S, lam)
    y = np.array([data_at(m, tr, r)[0] for (m, tr, r) in items])
    s = np.array([data_at(m, tr, r)[1] for (m, tr, r) in items])
    return y, s, Sres, corr_of(Sres), N
def ctot(s, Sres, R):
    return np.outer(s, s) * R + Sres

def one_radius(r, lam=LAMBDA, hartlap=False):
    meths = ("empdf", "nimble-a", "nimble-b") if r == 30.0 else ("empdf", "gme", "nimble-a", "nimble-b")
    items = [(m, tr, r) for m in meths for tr in ("rrl", "bhb")]
    y, s, Sres, R, N = build(items, lam)
    pf = (N - len(items) - 2) / (N - 1) if hartlap else 1.0
    th, V, _ = gls(y, ctot(s, Sres, R), np.ones((len(items), 1)), pf)
    return float(th[0]), float(math.sqrt(V[0, 0])), N, len(items)
KR = {}; det = []; ok4 = True; KA4ROWS = {}
for r in RAD:
    th1, sg, N, p = one_radius(r)
    ref, sref = TABLE4_ALL[r]
    ok4 &= abs(th1 - ref) <= sref and N >= 20
    KR[r] = max(1.0, sref / sg)
    KA4ROWS[r] = dict(theta=th1 + 11, sigma_mine=sg, N=N, curves=p, k=KR[r])
    det.append(f"{r:.0f} kpc: {th1+11:.4f} +/- {sg:.4f} from {p} curves, N = {N} (Table 4: {ref+11:.3f} +/- {sref:.4f}; k = {KR[r]:.3f})")
ka("KA4 the machinery on all curves at one radius reproduces the paper's joint within one published sigma (30, 50, 80)",
   ok4, "; ".join(det))
stop_if_failed()

def assemble(items, rad, lam=LAMBDA, kr=None, hartlap=False, stat_only=False):
    y, s, Sres, R, N = build(items, lam)
    C = np.diag(s ** 2) if stat_only else ctot(s, Sres, R)
    kr = KR if kr is None else kr
    kv = np.array([kr[r] for (_, _, r) in items])
    C = C * np.outer(kv, kv)
    X = np.array([[1.0 if r == rr else 0.0 for rr in rad] for (_, _, r) in items])
    pf = (N - len(items) - 2) / (N - 1) if hartlap else 1.0
    th, V, chi = gls(y, C, X, pf)
    return dict(y=y, s=s, C=C, X=X, th=th, V=V, chi=chi, N=N, p=len(items), pf=pf, rad=rad)
def items_for(rad):
    return [(m, tr, r) for r in rad for m in ("nimble-a", "nimble-b") for tr in ("rrl", "bhb")]
ITEMS = items_for(RAD); ITEMS2 = items_for(RAD2)

# KA5: NMB1 reproduced with the 50 kpc rows dropped ----------------------------------------------
B2 = assemble(ITEMS2, RAD2)
def Qof(th, V, mu):
    d = mu - th; return float(d @ np.linalg.inv(V) @ d)
q2 = {}
for rd, f in NMB1_Q:
    q2[(rd, f)] = Qof(B2["th"], B2["V"], mu_line(A0[f], 1.0, E_N if rd == "E1" else 0.0, rad=RAD2))
got = (B2["th"][0] + 11, math.sqrt(B2["V"][0, 0]), B2["th"][1] + 11, math.sqrt(B2["V"][1, 1]))
ok5 = all(abs(a - b) <= 0.0005 for a, b in zip(got, NMB1_TH)) and all(abs(round(q2[k], 2) - v) <= 0.01 for k, v in NMB1_Q.items())
ka("KA5 NMB1 reproduced with the 50 kpc rows dropped (theta, errors within 0.0005; Q within 0.01)", ok5,
   f"theta {got[0]:.4f} +/- {got[1]:.4f}, {got[2]:.4f} +/- {got[3]:.4f}; Q " +
   ", ".join(f"{rd} {f} {q2[(rd, f)]:.2f}" for rd, f in NMB1_Q))
BASE = assemble(ITEMS, RAD)

# KA6: synthetic ------------------------------------------------------------------------------------
x1, x2, s1, s2, rho = 1.0, 1.3, 0.2, 0.5, 0.4
Ct = np.array([[s1 * s1, rho * s1 * s2], [rho * s1 * s2, s2 * s2]])
tht, Vt, _ = gls(np.array([x1, x2]), Ct, np.ones((2, 1)))
den = s1 * s1 + s2 * s2 - 2 * rho * s1 * s2
cf_t = (x1 * (s2 * s2 - rho * s1 * s2) + x2 * (s1 * s1 - rho * s1 * s2)) / den
cf_v = s1 * s1 * s2 * s2 * (1 - rho * rho) / den
rng = np.random.default_rng(20261112)
mu0 = np.array([0.42, 0.62, 0.80]); Lc = np.linalg.cholesky(BASE["C"]); Ci = np.linalg.inv(BASE["C"])
Vi = np.linalg.inv(BASE["V"]); Qs = []
for _ in range(20000):
    yy = BASE["X"] @ mu0 + Lc @ rng.standard_normal(len(ITEMS))
    d = BASE["V"] @ BASE["X"].T @ Ci @ yy - mu0
    Qs.append(float(d @ Vi @ d))
Qs = np.array(Qs)
ka("KA6 estimator and gate on synthetic data (closed form to 1e-10; mean Q 3.00 +/- 0.06; rejection 0.0455 +/- 0.005)",
   abs(tht[0] - cf_t) < 1e-10 and abs(Vt[0, 0] - cf_v) < 1e-10 and abs(Qs.mean() - 3.0) <= 0.06
   and abs((Qs > QGATE).mean() - 0.0455) <= 0.005,
   f"closed form {abs(tht[0]-cf_t):.1e}, {abs(Vt[0,0]-cf_v):.1e}; mean Q {Qs.mean():.3f}; rejection {(Qs > QGATE).mean():.4f}")

# KA7: line and inputs -------------------------------------------------------------------------------
ref7 = {("canonical", 0.0): 5.691, ("alt", 0.0): 6.219, ("canonical", E_N): 4.977, ("alt", E_N): 5.109}
w7 = max(abs(M_line(80.0, A0[f], 1.0, e) / v - 1) for (f, e), v in ref7.items())
f30, f80 = M_sph(30.0) / MSPH_TOT, M_sph(80.0) / MSPH_TOT
ok7 = w7 <= 0.005 and abs(f30 - 0.9777) <= 0.001 and abs(f80 - 0.9972) <= 0.001 and abs(m_hot(50.0) / 3.8e9 - 1) <= 0.03
ka("KA7 line at 80 kpc within 0.5 %; M_sph fractions at 30, 80 within 0.001 of DW1; MB15 3.8e9 inside 50 kpc within 3 %", ok7,
   "; ".join(f"{f} {'E1' if e else 'E0'} {M_line(80.0, A0[f], 1.0, e):.3f}" for (f, e) in ref7)
   + f"; worst {w7:.2%}; f30 {f30:.4f}, f80 {f80:.4f}, f50 (used) {FSPH[50.0]:.4f}; MB15(<50) {m_hot(50.0):.3e}")
stop_if_failed()

# ---------------------------------------------------------------- gate
def curv(v):
    return (v[2] - v[1]) / L2 - (v[1] - v[0]) / L1
GC = np.array([1.0 / L1, -1.0 / L2 - 1.0 / L1, 1.0 / L2])
def gate(th, V, mu):
    d = mu - th
    Q = float(d @ np.linalg.inv(V) @ d)
    z = d / np.sqrt(np.diag(V))
    pd = (th[2] - th[0]) / L; pl = (mu[2] - mu[0]) / L
    sp = math.sqrt(V[0, 0] + V[2, 2] - 2 * V[0, 2]) / L
    zs = (pl - pd) / sp
    cd, cl = curv(th), curv(mu); sc = math.sqrt(float(GC @ V @ GC)); zc = (cl - cd) / sc
    if Q <= QGATE:
        lab = "PASSES"
        if abs(zs) > 2: lab += " [slope pull beyond 2]"
        if abs(zc) > 2: lab += " [curvature pull beyond 2]"
    else:
        lab = "FAILS " + ("LOW" if (z < 0).all() else "HIGH" if (z > 0).all() else "MIXED")
        if abs(zs) > 2: lab += " SHAPE"
        if abs(zc) > 2: lab += " CURVATURE"
        lab += " (2 to 3 sigma)" if Q <= Q3 else " (beyond 3 sigma)"
    return dict(Q=Q, z30=z[0], z50=z[1], z80=z[2], zs=zs, slope_line=pl, slope_data=pd, sigma_slope=sp,
                zc=zc, curv_line=cl, curv_data=cd, sigma_curv=sc, label=lab)

# ---------------------------------------------------------------- mutations
MUT = open(os.path.join(HERE, "nim2_mut.out"), "w")
def msay(s): MUT.write(s + "\n"); MUT.flush()
msay("NIM2 mutations. Each must bite.")
bite = True
th, V = BASE["th"], BASE["V"]
for f in FOOT:
    g = gate(th, V, mu_line(A0[f], 2.0)); b = g["label"].startswith("FAILS HIGH"); bite &= b
    msay(f"M1 A = 2, E0 census {f:9s}: Q = {g['Q']:8.2f}  z {g['z30']:+.2f} {g['z50']:+.2f} {g['z80']:+.2f}  -> {g['label']}  [{'bites' if b else 'DOES NOT BITE'}]")
    g = gate(th, V, mu_line(A0[f], 2.0, E_N))
    msay(f"   (reported) A = 2, E1 census {f:9s}: Q = {g['Q']:8.2f}  -> {g['label']}")
g = gate(th, V, np.array([th[2]] * 3)); b = g["label"].startswith("FAILS") and (abs(g["zs"]) > 2 or abs(g["zc"]) > 2); bite &= b
msay(f"M2 point mass (mu = theta_80 at all radii): Q = {g['Q']:8.2f}  z_s {g['zs']:+.2f}  z_c {g['zc']:+.2f}  -> {g['label']}  [{'bites' if b else 'DOES NOT BITE'}]")
msay("kappa = 1/2 FITTED; not theory closed. Adopts nothing.")
MUT.close()
sec("MUTATIONS")
say(f"  M1, M2 written to nim2_mut.out: {'all bite' if bite else 'AT LEAST ONE DOES NOT BITE -> NO POWER'}")
if not bite:
    json.dump({"lane": "NIM2", "label": "NO POWER"}, open(os.path.join(HERE, "nim2_results.json"), "w"), indent=1)
    sys.exit(0)

# ====================================================================================================
sec("THE INSTRUMENT")
say("  curve            r    M_med [1e11]   16th    84th    log10 M   sigma_stat [dex]")
for (m, tr, r) in ITEMS:
    lg, s, med, lo, hi = data_at(m, tr, r)
    say(f"  {m:9s} {tr:3s}  {r:4.0f}   {med:7.3f}     {lo:6.3f}  {hi:6.3f}   {lg+11:7.4f}   {s:.4f}")
say(f"\n  mocks used N = {BASE['N']}; shrinkage {LAMBDA}; k_30 = {KR[30.0]:.3f}, k_50 = {KR[50.0]:.3f}, k_80 = {KR[80.0]:.3f}")
cor = V / np.sqrt(np.outer(np.diag(V), np.diag(V)))
for i, r in enumerate(RAD):
    say(f"  NIMBLE-only log10(M/Msun) at {r:2.0f} kpc: {th[i]+11:.4f} +/- {math.sqrt(V[i,i]):.4f}  ({10**th[i]:.3f} e11)")
say(f"  correlations: 30-50 {cor[0,1]:+.3f}, 30-80 {cor[0,2]:+.3f}, 50-80 {cor[1,2]:+.3f}")
sp3 = math.sqrt(V[0, 0] + V[2, 2] - 2 * V[0, 2]) / L
say(f"  slope 30-80: {(th[2]-th[0])/L:.3f} +/- {sp3:.3f};  slope 30-50: {(th[1]-th[0])/L1:.3f};  slope 50-80: {(th[2]-th[1])/L2:.3f}")
say(f"  curvature c = {curv(th):+.3f} +/- {math.sqrt(float(GC @ V @ GC)):.3f}")
chi9 = BASE["chi"]
from scipy.stats import chi2 as _chi2
say(f"  internal consistency: chi2 = {chi9:.2f} on 9 dof, p = {_chi2.sf(chi9, 9):.3f}  (reported)")
say(f"  NMB1 two-radius (reproduced): 30 {B2['th'][0]+11:.4f} +/- {math.sqrt(B2['V'][0,0]):.4f}; 80 {B2['th'][1]+11:.4f} +/- {math.sqrt(B2['V'][1,1]):.4f}; "
    f"slope sigma {math.sqrt(B2['V'][0,0]+B2['V'][1,1]-2*B2['V'][0,1])/L:.3f}")
say(f"  Table 4 joint at 50 kpc for comparison: 11.654 +0.025 -0.026")

VAR = collections.OrderedDict()
VAR["NIMBLE-A only"] = assemble([i for i in ITEMS if i[0] == "nimble-a"], RAD)
VAR["NIMBLE-B only"] = assemble([i for i in ITEMS if i[0] == "nimble-b"], RAD)
VAR["NIMBLE-A RRL dropped"] = assemble([i for i in ITEMS if not (i[0] == "nimble-a" and i[1] == "rrl")], RAD)
kr0 = {r: max(1.0, TABLE4_ALL[r][1] / one_radius(r, 0.0, True)[1]) for r in RAD}
kr1 = {r: max(1.0, TABLE4_ALL[r][1] / one_radius(r, 1.0)[1]) for r in RAD}
VAR["lambda = 0 (Hartlap)"] = assemble(ITEMS, RAD, lam=0.0, kr=kr0, hartlap=True)
VAR["lambda = 1"] = assemble(ITEMS, RAD, lam=1.0, kr=kr1)
VAR["k = 1"] = assemble(ITEMS, RAD, kr={r: 1.0 for r in RAD})
STAT = assemble(ITEMS, RAD, kr={r: 1.0 for r in RAD}, stat_only=True)

sec("THE GATE   Q <= 8.02 on 3 dof.  z = (line - data)/sigma; negative = line below the data")
CASES = [(rd, f, gas) for gas in (False, True) for rd in ("E1", "E0") for f in FOOT]
def cname(rd, f, gas): return f"{rd} {f} {'MB15' if gas else 'census'}"
RES = {}; MU_OF = {}
for rd, f, gas in CASES:
    mu = mu_line(A0[f], 1.0, E_N if rd == "E1" else 0.0, gas); MU_OF[(rd, f, gas)] = mu
    g = gate(th, V, mu)
    sides = {k: gate(v["th"], v["V"], mu) for k, v in VAR.items()}
    flips = [k for k, s in sides.items() if (s["Q"] <= QGATE) != (g["Q"] <= QGATE)]
    lab = g["label"] + (", FRAGILE" if flips else "")
    say(f"\n  {cname(rd, f, gas)}:  line {10**mu[0]:.3f} / {10**mu[1]:.3f} / {10**mu[2]:.3f} e11 at 30 / 50 / 80 kpc")
    say(f"     Q = {g['Q']:.2f} (p = {_chi2.sf(g['Q'], 3):.4f});  z30 {g['z30']:+.2f}, z50 {g['z50']:+.2f}, z80 {g['z80']:+.2f};  "
        f"slope line {g['slope_line']:.3f} vs data {g['slope_data']:.3f} +/- {g['sigma_slope']:.3f} (z_s {g['zs']:+.2f});  "
        f"curvature line {g['curv_line']:+.3f} vs data {g['curv_data']:+.3f} +/- {g['sigma_curv']:.3f} (z_c {g['zc']:+.2f})")
    say(f"     LABEL: {lab}")
    for k, s in sides.items():
        say(f"       variant {k:24s} Q = {s['Q']:7.2f}  z {s['z30']:+.2f} {s['z50']:+.2f} {s['z80']:+.2f} z_s {s['zs']:+.2f} z_c {s['zc']:+.2f}  "
            f"{'pass' if s['Q'] <= QGATE else 'fail'}" + ("   <- other side" if k in flips else ""))
    s = gate(STAT["th"], STAT["V"], mu)
    say(f"       reported: published bands only  Q = {s['Q']:7.2f}")
    RES[cname(rd, f, gas)] = dict(label=lab, **{k: float(v) for k, v in g.items() if k != "label"},
                                  line=[float(10 ** x) for x in mu], flips=flips,
                                  variants={k: s2["Q"] for k, s2 in sides.items()}, Q_published_bands=s["Q"])

mu_n = mu_nfw()
gN = gate(th, V, mu_n)
nfw_pass = gN["Q"] <= QGATE
say(f"\n  the paper's NFW (comparator): {10**mu_n[0]:.3f} / {10**mu_n[1]:.3f} / {10**mu_n[2]:.3f} e11; Q = {gN['Q']:.2f}; "
    f"z {gN['z30']:+.2f} {gN['z50']:+.2f} {gN['z80']:+.2f}; z_s {gN['zs']:+.2f}; curvature {gN['curv_line']:+.3f} (z_c {gN['zc']:+.2f})  -> {gN['label']}")

sec("SEPARATION LABELS")
SEP = {}
for f in FOOT:
    SEP[f] = {}
    for gas in (False, True):
        p0 = RES[cname("E0", f, gas)]["Q"] <= QGATE; p1 = RES[cname("E1", f, gas)]["Q"] <= QGATE
        SEP[f][f"E0_vs_E1_{'MB15' if gas else 'census'}"] = "SEPARATES" if p0 != p1 else "DOES NOT SEPARATE"
    opp = [cname(rd, f, gas) for rd, _, gas in CASES if _ == f and (RES[cname(rd, f, gas)]["Q"] <= QGATE) != nfw_pass]
    opp = sorted(set(opp))
    SEP[f]["vs_NFW"] = "SEPARATES" if len(opp) == 4 else "PARTLY SEPARATES" if opp else "DOES NOT SEPARATE"
    SEP[f]["vs_NFW_opposite_cases"] = opp
    say(f"  {f}: E0 vs E1 census: {SEP[f]['E0_vs_E1_census']};  E0 vs E1 MB15: {SEP[f]['E0_vs_E1_MB15']};  framework vs NFW: {SEP[f]['vs_NFW']}"
        + (f" ({', '.join(opp)})" if opp else ""))

sec("POWER COMPARISON WITH NMB1 (reported)")
V2 = B2["V"]; V2i = np.linalg.inv(V2); V3i = np.linalg.inv(V)
def lam2(a, b): d = a[[0, 2]] - b[[0, 2]]; return float(d @ V2i @ d)
def lam3(a, b): d = a - b; return float(d @ V3i @ d)
def pw(lmb, dof, gt): return float(ncx2.sf(gt, dof, lmb)) if lmb > 0 else float(_chi2.sf(gt, dof))
say(f"  errors: 30 kpc {math.sqrt(V2[0,0]):.4f} -> {math.sqrt(V[0,0]):.4f};  80 kpc {math.sqrt(V2[1,1]):.4f} -> {math.sqrt(V[2,2]):.4f};  "
    f"slope 30-80 {math.sqrt(V2[0,0]+V2[1,1]-2*V2[0,1])/L:.3f} -> {sp3:.3f};  50 kpc (new) {math.sqrt(V[1,1]):.4f}")
POW = {}
pairs = []
for f in FOOT:
    for gas in (False, True):
        pairs.append((f"{f} {'MB15' if gas else 'census'}: E0 vs E1", MU_OF[("E0", f, gas)], MU_OF[("E1", f, gas)]))
for rd, f, gas in CASES:
    pairs.append((f"{cname(rd, f, gas)} vs NFW", MU_OF[(rd, f, gas)], mu_n))
say("  pair                                   lambda(2 radii)  power(2 dof, 6.18)   lambda(3 radii)  power(3 dof, 8.02)")
for nm, a, b in pairs:
    l2, l3 = lam2(a, b), lam3(a, b)
    POW[nm] = dict(lambda2=l2, power2=pw(l2, 2, QGATE2), lambda3=l3, power3=pw(l3, 3, QGATE))
    say(f"  {nm:38s} {l2:10.3f}       {POW[nm]['power2']:8.3f}           {l3:10.3f}       {POW[nm]['power3']:8.3f}"
        + ("   no gain" if POW[nm]["power3"] <= POW[nm]["power2"] else ""))

sec("LABELS")
for k, v in RES.items():
    say(f"  {k:24s} {v['label']}")
say(f"  {'paper NFW (comparator)':24s} {gN['label']}")
json.dump(dict(lane="NIM2", date="2026-11-12", criteria_sha256=crit_sha, zip_md5=md5, N_mocks=BASE["N"], shrinkage=LAMBDA,
               k=KR, ka4=KA4ROWS, f50=FSPH[50.0], theta=[float(t) for t in th], V=[[float(x) for x in row] for row in V],
               chi2_internal_9dof=chi9, nmb1_repro=dict(theta=[float(t) for t in B2["th"]], V=[[float(x) for x in row] for row in V2],
                                                         Q={f"{a} {b}": q for (a, b), q in q2.items()}),
               cases=RES, nfw={k: (float(v) if not isinstance(v, str) else v) for k, v in gN.items()},
               separation=SEP, power=POW),
          open(os.path.join(HERE, "nim2_results.json"), "w"), indent=1)
say("\nNIM2 COMPLETE. kappa = 1/2 FITTED; not theory closed. Adopts nothing.")
