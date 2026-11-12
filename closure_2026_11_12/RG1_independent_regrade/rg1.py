#!/usr/bin/env python3
"""RG1: independent re-implementation of NMB1, PLT1, MWJ1, MWG1, MWI1 from their frozen criteria.
Criteria: FROZEN_CRITERIA.md in this folder.  Usage: python3 -I rg1.py <figdata_dir>
kappa = 1/2 FITTED; not theory closed. Adopts nothing."""
import csv, json, math, os, sys
import numpy as np
from scipy import integrate

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = sys.argv[1]
OUT = open(os.path.join(HERE, "rg1.out"), "w")
def say(s=""):
    print(s); OUT.write(str(s) + "\n"); OUT.flush()
RES = {}

G = 6.674e-11; MSUN = 1.989e30; KPC = 3.0857e19; PC = KPC / 1000.0
A0 = {"canonical": 9.36e-11, "alt": 1.13e-10}
EREC = 0.01273

def nu(y):
    y = np.maximum(np.asarray(y, float), 1e-300)
    return 1.0 / (-np.expm1(-np.sqrt(y)))

# ---------------- McMillan 2017 (parameters from DW1; integration my own) -------------------
SPC2 = MSUN / PC**2
DISCS = [  # (Sigma0 or None, Sfid, Rfid, Rd, zd, Rm, vertical)  lengths in kpc, Sigma in Msun/pc^2
    dict(name="thin", S0=896.0, Rd=2.50, zd=0.300, Rm=0.0, vert="exp"),
    dict(name="thick", S0=183.0, Rd=3.02, zd=0.900, Rm=0.0, vert="exp"),
    dict(name="HI", Sfid=10.0, Rfid=8.33, Rd=7.00, zd=0.085, Rm=4.0, vert="sech2"),
    dict(name="H2", Sfid=2.0, Rfid=8.33, Rd=1.50, zd=0.045, Rm=12.0, vert="sech2")]
MBUL, ABUL = 9.23e9, 0.70  # Msun, kpc
for d in DISCS:
    if "S0" not in d:
        d["S0"] = d["Sfid"] / math.exp(-d["Rm"] / d["Rfid"] - d["Rfid"] / d["Rd"])
def sig(d, R):  # Msun/kpc^2
    R = np.maximum(R, 1e-9)
    return d["S0"] * 1e6 * np.exp(-d["Rm"] / R - R / d["Rd"])
def vcdf(d, h):  # P(|z| < h)
    if d["vert"] == "exp":
        return -np.expm1(-h / d["zd"])
    return np.tanh(h / (2 * d["zd"]))   # sech^2(z/2zd)/(4zd) -> P(|z|<h) = tanh(h/(2 zd))
GL_X, GL_W = np.polynomial.legendre.leggauss(400)
def disc_mass(d):
    return integrate.quad(lambda R: 2 * math.pi * R * float(sig(d, R)), 0, 2000, points=[d["Rm"] + 1e-3, 10, 50], limit=400)[0]
def M_sph(r):
    """spherical enclosed baryon mass [Msun] within r [kpc]"""
    tot = MBUL * r * r / (r + ABUL) ** 2
    for d in DISCS:
        f = lambda R: 2 * math.pi * R * float(sig(d, R)) * float(vcdf(d, math.sqrt(max(r * r - R * R, 0.0))))
        pts = [p for p in (d["Rm"], 0.5 * r, 0.9 * r, 0.99 * r) if 0 < p < r]
        tot += integrate.quad(f, 0, r, points=pts, limit=500, epsabs=0, epsrel=1e-9)[0]
    return tot
MB_TOT = sum(disc_mass(d) for d in DISCS) + MBUL
_MS = {}
def Msph(r):
    k = round(float(r), 6)
    if k not in _MS: _MS[k] = M_sph(float(r))
    return _MS[k]

def M_line(r, a0, eN, A=1.0, extra=0.0, kern=nu):
    """framework enclosed mass [Msun]; extra = additional baryons inside r (hot gas)"""
    Mb = A * Msph(r) + extra
    gb = G * Mb * MSUN / (r * KPC) ** 2 / a0
    if eN == 0.0:
        return float(kern(gb)) * Mb
    gm = np.sqrt(gb * gb + eN * eN + 2 * gb * eN * GL_X)
    avg = 0.5 * np.sum(GL_W * kern(gm) * (gb + eN * GL_X))
    return float(avg / gb * Mb)

say("RG1 independent regrade.  kappa = 1/2 FITTED; not theory closed.  Adopts nothing.")
say("=" * 100)
say("INSTRUMENT")
comp = {d["name"]: disc_mass(d) for d in DISCS}
say("  components [1e10]: " + "  ".join(f"{k} {v/1e10:.4f}" for k, v in comp.items()) + f"  bulge {MBUL/1e10:.4f}")
say(f"  census total {MB_TOT:.5e} (target 6.681e10, {MB_TOT/6.681e10-1:+.4%});  stars {(comp['thin']+comp['thick']+MBUL)/1e10:.4f}e10, cold gas {(comp['HI']+comp['H2'])/1e10:.4f}e10")
f30, f80 = Msph(30) / MB_TOT, Msph(80) / MB_TOT
say(f"  M_sph/M_b at 30, 80 kpc: {f30:.4f}, {f80:.4f} (DW1 0.9777, 0.9972)")
LINE80 = {}
for foot, a0 in A0.items():
    e0 = M_line(80, a0, 0.0) / 1e11; e1 = M_line(80, a0, EREC) / 1e11
    LINE80[foot] = (e0, e1)
    say(f"  {foot:9}: E0(80) {e0:.4f} (rec {5.691 if foot=='canonical' else 6.219}), E1(80) {e1:.4f} (rec {4.977 if foot=='canonical' else 5.109}) x1e11")
    for rr, tc, ta in ((150, 5.252, 5.257), (200, 5.264, 5.266), (300, 5.270, 5.270)):
        v = M_line(rr, a0, EREC) / 1e11
        say(f"             E1({rr}) {v:.4f} (PLT1 KA4 {tc if foot=='canonical' else ta})")
    # closed form far field: [nu(e) + e nu'(e)/3] M_b
    e = EREC; h = 1e-7; dnu = (nu(e + h) - nu(e - h)) / (2 * h)
    say(f"             E1(2000) {M_line(2000, a0, EREC)/1e11:.4f} vs closed form {float(nu(e) + e*dnu/3)*Msph(2000)/1e11:.4f}")
RES["instrument"] = dict(MB=MB_TOT, f30=f30, f80=f80, line80=LINE80)

# ---------------- NMB1 -----------------------------------------------------------------------
say("=" * 100); say("NMB1")
def rcsv(p): return list(csv.DictReader(open(os.path.join(DATA, p))))
fig10 = rcsv("fig10/desi-dr2-menc.csv")
def curve(method, tracer):
    rows = [r for r in fig10 if r["method"] == method and r["tracer"] == tracer]
    return {float(r["r_kpc"]): (float(r["Menc_med"]), float(r["Menc_lo"]), float(r["Menc_hi"])) for r in rows}
def interp_loglog(rs, ms, r):
    rs = np.asarray(rs); ms = np.asarray(ms); o = np.argsort(rs)
    return 10 ** np.interp(math.log10(r), np.log10(rs[o]), np.log10(ms[o]), left=np.nan, right=np.nan)
def at(cv, r, k):
    if r in cv: return cv[r][k]
    rs = sorted(cv); return interp_loglog(rs, [cv[x][k] for x in rs], r)

MOCKDIR = {"rrl": "figA1", "bhb": "figA2"}
_mock = {}
def mocks(method, tracer):
    key = (method, tracer)
    if key not in _mock:
        rows = rcsv(f"{MOCKDIR[tracer]}/{method}.csv"); tr = rcsv(f"{MOCKDIR[tracer]}/truths.csv")
        est = {}
        for r in rows: est.setdefault((r["halo"], r["view"]), {})[float(r["r_kpc"])] = float(r["Menc_med"])
        tru = {}
        for r in tr: tru.setdefault(r["halo"], {})[float(r["r_kpc"])] = float(r["Menc"])
        _mock[key] = (est, tru)
    return _mock[key]
def mock_resid(method, tracer, r):
    est, tru = mocks(method, tracer); out = {}
    for (h, v), cv in est.items():
        if min(cv) > r or max(cv) < r: continue
        me = cv[r] if r in cv else interp_loglog(list(cv), list(cv.values()), r)
        mt = interp_loglog(list(tru[h]), list(tru[h].values()), r)
        out[(h, v)] = math.log10(me / mt)
    return out

def build(items, lam=0.5, Rident=False, kscale=None):
    """items: list of (method, tracer, r).  Returns y, sig, C, S_res, N"""
    y = np.array([11.0 + math.log10(at(curve(m, t), r, 0)) for m, t, r in items])   # file unit 1e11 Msun
    sg = np.array([(math.log10(at(curve(m, t), r, 2) / at(curve(m, t), r, 0)) +
                    math.log10(at(curve(m, t), r, 0) / at(curve(m, t), r, 1))) / 2 for m, t, r in items])
    res = [mock_resid(m, t, r) for m, t, r in items]
    keys = sorted(set.intersection(*[set(x) for x in res]))
    Rm = np.array([[x[k] for k in keys] for x in res])
    S = np.cov(Rm, ddof=1)
    Sres = (1 - lam) * S + lam * np.diag(np.diag(S))
    dd = np.sqrt(np.diag(Sres)); R = Sres / np.outer(dd, dd)
    if Rident:
        C = np.diag(sg ** 2); Sres = np.zeros_like(C)
    else:
        C = np.outer(sg, sg) * R + Sres
    return y, sg, C, Sres, len(keys), Rm

def gls(y, C, X):
    Ci = np.linalg.inv(C); V = np.linalg.inv(X.T @ Ci @ X); th = V @ X.T @ Ci @ y
    return th, V

# K calibration and KA4 (all curves at one radius)
PUB = {30: 0.022, 80: 0.0345}; PUBC = {30: 11.423, 80: 11.804}
K = {}
for r in (30.0, 80.0):
    its = [(m, t, r) for m in ("empdf", "nimble-a", "nimble-b") for t in ("rrl", "bhb")]
    if r == 80.0: its += [("gme", t, r) for t in ("rrl", "bhb")]
    y, sg, C, Sres, N, _ = build(its)
    X = np.ones((len(its), 1)); th, V = gls(y, C, X)
    smine = math.sqrt(V[0, 0]); K[int(r)] = max(1.0, PUB[int(r)] / smine)
    say(f"  all-curve machinery at {r:.0f} kpc ({len(its)} curves, N = {N} mocks): {th[0]:.4f} +- {smine:.4f}"
        f"  (Table 4: {PUBC[int(r)]} +- {PUB[int(r)]}; KA4 {'PASS' if abs(th[0]-PUBC[int(r)]) <= PUB[int(r)] else 'FAIL'});  k_{r:.0f} = {K[int(r)]:.4f}")

# KA3: medians of M_est/M_true - 1
f08 = rcsv("fig08/summary.csv")
MAPN = {"nimble-b": "NIMBLE-B", "nimble-a": "NIMBLE-A", "empdf": "emPDF", "gme": "GME"}
for m, t, r, tgt in (("nimble-b", "rrl", 80.0, -6.50), ("nimble-a", "bhb", 80.0, -7.54), ("nimble-a", "rrl", 30.0, 5.91), ("nimble-b", "bhb", 30.0, -1.19)):
    mr = mock_resid(m, t, r); med = float(np.median([10 ** v - 1 for v in mr.values()])) * 100
    fv = [float(x["0.5"]) for x in f08 if x["quantity"] == "menc" and x["method"] == MAPN[m] and x["tracer"] == t and x["r_kpc"] and float(x["r_kpc"]) == r]
    say(f"  KA3 {m} {t} {r:.0f}: my median bias {med:+.2f} %, fig08 {fv[0] if fv else 'n/a'} (criteria {tgt:+.2f})")

NIMB = [(m, t) for m in ("nimble-a", "nimble-b") for t in ("rrl", "bhb")]
def nimble_fit(curves=NIMB, lam=0.5, kk=None, Rident=False, invfac=1.0):
    its = [(m, t, r) for m, t in curves for r in (30.0, 80.0)]
    y, sg, C, Sres, N, _ = build(its, lam=lam, Rident=Rident)
    kk = K if kk is None else kk
    D = np.diag([kk[int(r)] for _, _, r in its]); C = D @ C @ D
    X = np.array([[1.0, 0.0] if r == 30.0 else [0.0, 1.0] for _, _, r in its])
    Ci = np.linalg.inv(C) * invfac
    V = np.linalg.inv(X.T @ Ci @ X); th = V @ X.T @ Ci @ y
    chi2 = float((y - X @ th) @ Ci @ (y - X @ th))
    return th, V, N, chi2, y, sg
th, V, Nm, chi2, ynm, sgnm = nimble_fit()
corr = V[0, 1] / math.sqrt(V[0, 0] * V[1, 1])
say(f"  N mocks = {Nm};  data vector y = " + " ".join(f"{v:.4f}" for v in ynm))
say(f"  sigma_stat = " + " ".join(f"{v:.4f}" for v in sgnm))
say(f"  NIMBLE combined: theta_30 = {th[0]:.4f} +- {math.sqrt(V[0,0]):.4f}, theta_80 = {th[1]:.4f} +- {math.sqrt(V[1,1]):.4f}, corr {corr:+.3f}; internal chi2 {chi2:.2f}/6")
LR = math.log10(80 / 30)
def grade(mu, th=th, V=V):
    d = th - mu; Q = float(d @ np.linalg.inv(V) @ d)
    z30 = (mu[0] - th[0]) / math.sqrt(V[0, 0]); z80 = (mu[1] - th[1]) / math.sqrt(V[1, 1])
    sp = math.sqrt(V[0, 0] + V[1, 1] - 2 * V[0, 1]) / LR
    zs = ((mu[1] - mu[0]) / LR - (th[1] - th[0]) / LR) / sp
    lab = "PASSES" if Q <= 6.180 else ("FAILS 2 to 3 sigma" if Q <= 11.829 else "FAILS beyond 3 sigma")
    dirn = "LOW" if (z30 < 0 and z80 < 0) else ("HIGH" if (z30 > 0 and z80 > 0) else "MIXED")
    return Q, z30, z80, zs, lab, dirn
NMB = {}
for eN, en in (("E1", EREC), ("E0", 0.0)):
    for foot, a0 in A0.items():
        mu = np.array([math.log10(M_line(30, a0, en)), math.log10(M_line(80, a0, en))])
        Q, z30, z80, zs, lab, dirn = grade(mu)
        NMB[f"{eN}_{foot}"] = dict(mu=mu.tolist(), Q=Q, z30=z30, z80=z80, zs=zs, label=lab)
        say(f"  {eN} {foot:9}: line {mu[0]:.4f}, {mu[1]:.4f}  Q = {Q:.3f}  z30 {z30:+.2f} z80 {z80:+.2f} zs {zs:+.2f}  {lab} {dirn if Q > 6.18 else ''}")
# fragility variants (reported)
for name, kw in (("NIMBLE-A only", dict(curves=NIMB[:2])), ("NIMBLE-B only", dict(curves=NIMB[2:])),
                 ("drop NIMBLE-A RRL", dict(curves=NIMB[1:])), ("lambda=1", dict(lam=1.0)),
                 ("k_r=1", dict(kk={30: 1.0, 80: 1.0}))):
    t2, V2, *_ = nimble_fit(**kw)
    qs = [grade(np.array(NMB[c]["mu"]), t2, V2)[0] for c in ("E1_canonical", "E1_alt", "E0_canonical", "E0_alt")]
    say(f"  variant {name:18}: theta {t2[0]:.4f} {t2[1]:.4f}  Q = " + ", ".join(f"{q:.2f}" for q in qs))
# lambda = 0 with Hartlap-type factor
t2, V2, N2, *_ = nimble_fit(lam=0.0, invfac=(Nm - 8 - 2) / (Nm - 1))
qs = [grade(np.array(NMB[c]["mu"]), t2, V2)[0] for c in ("E1_canonical", "E1_alt", "E0_canonical", "E0_alt")]
say(f"  variant lambda=0, Hartlap  : theta {t2[0]:.4f} {t2[1]:.4f}  Q = " + ", ".join(f"{q:.2f}" for q in qs))
RES["NMB1"] = dict(theta=th.tolist(), V=V.tolist(), sig=[math.sqrt(V[0, 0]), math.sqrt(V[1, 1])], corr=corr, K=K, N=Nm, cases=NMB)

# ---------------- PLT1 -----------------------------------------------------------------------
say("=" * 100); say("PLT1")
FLOOR = math.log10(1.2)
def load_rows(fn, col):
    out = []
    for r in rcsv(fn):
        M, lo, hi, rk = float(r[col]), float(r["err_lo_Msun"]), float(r["err_hi_Msun"]), float(r["r_kpc"])
        if rk < 100: continue
        ok = M > 0 and 0 < lo < M and hi > 0
        out.append(dict(label=r["label"], r=rk, M=M, lo=lo, hi=hi, ok=ok))
    return out
ROWS = {"H": load_rows("fig13/literature-halo-stars.csv", "Menc_Msun"), "S": load_rows("fig13/literature-other-tracers.csv", "value_Msun")}
for c, rows in ROWS.items():
    say(f"  class {c}: {len(rows)} rows at r >= 100 ({sum(not x['ok'] for x in rows)} unusable): " +
        "; ".join(f"{x['label']} {x['r']:.0f} {x['M']/1e11:.2f}(-{x['lo']/1e11:.2f}+{x['hi']/1e11:.2f})" for x in rows))
def pulls(rows, a0, eN, A=1.0, hot=None, rmin=100.0, floor=FLOOR):
    z = []
    for x in rows:
        if not x["ok"] or x["r"] < rmin: continue
        extra = hot(x["r"]) if hot else 0.0
        L = math.log10(M_line(x["r"], a0, eN, A, extra))
        lm = math.log10(x["M"])
        s = math.log10(x["M"] / (x["M"] - x["lo"])) if L <= lm else math.log10((x["M"] + x["hi"]) / x["M"])
        z.append((L - lm) / math.sqrt(s * s + floor * floor))
    return z
PLT = {}
for eN, en in (("E1", EREC), ("E0", 0.0)):
    for foot, a0 in A0.items():
        d = {}
        for c in ("H", "S"):
            zz = pulls(ROWS[c], a0, en); z150 = pulls(ROWS[c], a0, en, rmin=150.0)
            d[c] = dict(med=float(np.median(zz)), n=len(zz), med150=float(np.median(z150)) if z150 else None, n150=len(z150), pulls=zz)
        PLT[f"{eN}_{foot}"] = d
        say(f"  {eN} {foot:9}: H median {d['H']['med']:+.3f} (n {d['H']['n']}), S median {d['S']['med']:+.3f} (n {d['S']['n']});"
            f"  r>=150: H {d['H']['med150']:+.3f} (n {d['H']['n150']}), S {d['S']['med150']:+.3f} (n {d['S']['n150']})")
        say("       pulls H: " + " ".join(f"{v:+.2f}" for v in d["H"]["pulls"]) + " | S: " + " ".join(f"{v:+.2f}" for v in d["S"]["pulls"]))
RES["PLT1"] = PLT

# ---------------- MWJ1 / MWG1 window ---------------------------------------------------------
say("=" * 100); say("MWJ1 / MWG1 windows")
EG = np.round(np.arange(0, 0.03 + 1e-12, 0.0005), 4)
AG = np.round(np.arange(0.70, 1.80 + 1e-12, 0.01), 2)
iV = np.linalg.inv(V)
def gates(a0, eN, A=1.0, hot=None):
    ex30 = hot(30.0) if hot else 0.0; ex80 = hot(80.0) if hot else 0.0
    mu = np.array([math.log10(M_line(30, a0, eN, A, ex30)), math.log10(M_line(80, a0, eN, A, ex80))])
    d = th - mu; Q = float(d @ iV @ d)
    mH = np.median(pulls(ROWS["H"], a0, eN, A, hot)); mS = np.median(pulls(ROWS["S"], a0, eN, A, hot))
    pH = np.median(pulls(ROWS["H"], a0, eN, A, hot, rmin=150.0)); pS = np.median(pulls(ROWS["S"], a0, eN, A, hot, rmin=150.0))
    g1 = Q <= 6.180; g2 = abs(mH) <= 2 and abs(mS) <= 2; g2p = abs(pH) <= 2 and abs(pS) <= 2
    return g1, g2, g2p, dict(Q=Q, mH=float(mH), mS=float(mS), pH=float(pH), pS=float(pS))
def field_range(a0, A=1.0, hot=None):
    ok = []; first = {}
    for e in EG:
        g1, g2, g2p, info = gates(a0, float(e), A, hot)
        if g1 and g2 and g2p: ok.append(float(e))
        else:
            first.setdefault("fail", (float(e), "G1" if not g1 else ("G2" if not g2 else "G2p"), info))
    contig = bool(ok) and len(ok) == int(round((max(ok) - min(ok)) / 0.0005)) + 1
    return ok, contig, first
MWJ = {}
for foot, a0 in A0.items():
    ok, contig, first = field_range(a0)
    MWJ[foot] = dict(range=[min(ok), max(ok)] if ok else None, contiguous=contig, rec_passes=EREC in ok)
    g = gates(a0, EREC)
    say(f"  MWJ1 {foot:9} A=1: field range {MWJ[foot]['range']} contiguous {contig}; first failing e_N {first.get('fail', ('-',))[0]} by {first.get('fail', (0,'-'))[1]}")
    say(f"           at (0.01273, 1): Q {g[3]['Q']:.3f}; H {g[3]['mH']:+.3f}, S {g[3]['mS']:+.3f}; plateau H {g[3]['pH']:+.3f}, S {g[3]['pS']:+.3f}")
# full window (coarse report): amplitude range at e_N = 0, 0.008, 0.01273 and labels
for foot, a0 in A0.items():
    W = []
    for e in EG:
        for A in AG:
            g1, g2, g2p, _ = gates(a0, float(e), float(A))
            if g1 and g2 and g2p: W.append((float(e), float(A)))
    MWJ[foot]["W_size"] = len(W)
    rc = {"canonical": (1.256, 1.310, 0.008), "alt": (1.152, 1.208, 0.015)}[foot]
    rcin = any(rc[0] - 1e-9 <= A <= rc[1] + 1e-9 and e <= rc[2] + 1e-9 for e, A in W)
    at1 = [e for e, A in W if abs(A - 1) < 1e-9]
    lab = ("CLOSES AT THE RECORD'S VALUES" if (EREC, 1.0) in W else
           "CLOSES WITH CENSUS BARYONS, WEAKER FIELD" if at1 else
           "CLOSES ONLY WITH MORE BARYONS" if W else "DOES NOT CLOSE")
    MWJ[foot]["label"] = lab + (", ROTATION CURVE INSIDE" if rcin else ", ROTATION CURVE OUTSIDE")
    for e0 in (0.0, 0.008):
        As = [A for e, A in W if abs(e - e0) < 1e-9]
        say(f"  MWJ1 {foot:9} A range at e_N {e0}: {[min(As), max(As)] if As else None}")
    say(f"  MWJ1 {foot:9} window size {len(W)} grid points; label: {MWJ[foot]['label']}")
RES["MWJ1"] = MWJ

HOT = {"MB15": (4.3e10, 250.0, 1.5), "S15": (2.6e10, 300.0, 1.5), "F20": (5.5e10, 280.0, 1.5), "F17": (1.2e11, 250.0, 2.0)}
def hotf(m, cap=False, scale=1.0):
    Mr, rr, p = HOT[m]
    return lambda r: scale * Mr * (min(r, rr) if cap else r) ** p / rr ** p
MWG = {}
say(f"  MWG1 KA2: MB15 inside 50 kpc = {hotf('MB15')(50.0):.3e} (target 3.8e9)")
NEED = {"canonical": (1.71e10, 2.07e10), "alt": (1.01e10, 1.39e10)}
for m in HOT:
    h27 = hotf(m)(27.0)
    say(f"  MWG1 part 1 {m}: M_hot(<27) = {h27:.3e}; fraction of lower need: canonical {h27/NEED['canonical'][0]:.3f}, alt {h27/NEED['alt'][0]:.3f}")
for foot, a0 in A0.items():
    for m in HOT:
        for cap in (False, True):
            ok, contig, first = field_range(a0, 1.0, hotf(m, cap))
            g = gates(a0, EREC, 1.0, hotf(m, cap))
            key = f"{foot}_{m}" + ("_capped" if cap else "")
            MWG[key] = dict(range=[min(ok), max(ok)] if ok else None, contiguous=contig, rec_passes=EREC in ok, at_rec=g[3])
            say(f"  MWG1 {foot:9} {m:5}{' capped' if cap else '       '}: field range {MWG[key]['range']} contig {contig}; record's field passes {EREC in ok};"
                f" at 0.01273 Q {g[3]['Q']:.2f}, H {g[3]['mH']:+.2f}, S {g[3]['mS']:+.2f}, plateau H {g[3]['pH']:+.2f}, S {g[3]['pS']:+.2f}")
    g1, g2, g2p, inf = gates(a0, 0.0, 1.0, hotf("MB15", False, 10.0))
    say(f"  MWG1 {foot:9} M1 (10x MB15, e_N 0): G1 {g1} G2 {g2} G2p {g2p} -> {'bites' if not (g1 and g2 and g2p) else 'DOES NOT BITE'}")
RES["MWG1"] = MWG

# ---------------- MWI1 -----------------------------------------------------------------------
say("=" * 100); say("MWI1")
INV = [("LN15", 6.08, 1.14), ("McM17", 5.43, 0.57), ("C20", 5.04, 0.43), ("I25", 6.18, 0.21), ("L25", 2.607, 0.363)]
AR = {"canonical": (1.256, 1.310), "alt": (1.152, 1.208)}
MWI = {}
for hot in (0.15, hotf("MB15")(27.0) / 1e10):
    for foot in A0:
        req = [A * 6.681 - 1.191 - hot for A in AR[foot]]
        zs = {n: (req[0] - m) / e for n, m, e in INV}
        cls = {n: ("SUPPLIED" if z <= 1 else "WITHIN 2 SIGMA" if z <= 2 else "NOT SUPPLIED") for n, z in zs.items()}
        MWI[f"{foot}_hot{hot:.4f}"] = dict(req=req, z=zs, cls=cls)
        say(f"  hot {hot:.4f}e10 {foot:9}: required stars {req[0]:.3f} to {req[1]:.3f}e10;  z " +
            ", ".join(f"{n} {z:+.2f} ({cls[n]})" for n, z in zs.items()))
say(f"  my census cold gas {(comp['HI']+comp['H2'])/1e10:.4f}e10, stars {(comp['thin']+comp['thick']+MBUL)/1e10:.4f}e10")
RES["MWI1"] = MWI

json.dump(RES, open(os.path.join(HERE, "rg1_results.json"), "w"), indent=1, default=float)
say("\nRG1 numbers saved. kappa = 1/2 FITTED; not theory closed. Adopts nothing.")
# kappa = 1/2 FITTED; not theory closed. Adopts nothing.
