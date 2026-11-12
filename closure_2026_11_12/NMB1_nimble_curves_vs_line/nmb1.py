#!/usr/bin/env python3
"""
NMB1 -- the shape-measuring curves of DESI DR2 Results III (NIMBLE-A, NIMBLE-B; RRL, BHB) against the
framework's zero-parameter enclosed-mass line at 30 and 80 kpc.

Criteria: FROZEN_CRITERIA.md (committed alone, 1fd8ca964e, before this file existed).
Usage:    python3 -I nmb1.py /path/to/desi-dr2-mw-mass-figdata.zip
Writes:   nmb1.out, nmb1_results.json, nmb1_mut.out   (next to this file)

Order is fixed: KA1..KA6, then the mutations, then the graded numbers. A failed known-answer check stops the
script before any graded number is printed. kappa = 1/2 FITTED; not theory closed. Adopts nothing.
"""
import sys, os, io, csv, json, math, hashlib, zipfile, collections
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ZIP = sys.argv[1]
P = "desi-dr2-mw-mass-figdata/"
MD5 = "5b0cc3aa9947286eb9348e947d01182d"

# ---------------------------------------------------------------- constants (SI)
G, MSUN, KPC = 6.67430e-11, 1.98847e30, 3.0856775814913673e19
MB = 6.681e10 * MSUN                               # McMillan 2017 census, as DW1
FSPH = {30.0: 0.9777, 80.0: 0.9972}                # DW1's committed M_sph/M_b
A0 = {"canonical": 9.36e-11, "alt": 1.13e-10}
E_N = 0.01273                                      # repository's Local Group field, in a0 units
RAD = (30.0, 80.0)
L = math.log10(80.0 / 30.0)
QGATE, Q3 = 6.180, 11.829
LAMBDA = 0.5
TABLE4_ALL = {30.0: (11.423 - 11.0, 0.022), 80.0: (11.804 - 11.0, 0.0345)}   # log10(M / 1e11 Msun), the file's unit (run 1 compared against log10(M/Msun) and stopped at KA4)
T4R = [20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80]
T4 = {"rrl": [1.97, 2.38, 2.65, 3.11, 3.79, 4.38, 4.81, 5.19, 5.49, 5.79, 6.05, 6.24, 6.40],
      "bhb": [1.93, 2.24, 2.63, 2.97, 3.37, 3.89, 4.34, 4.72, 5.04, 5.43, 5.79, 6.10, 6.38]}
FIG8 = {("nimble-b", "rrl", 80.0): -6.50, ("nimble-a", "bhb", 80.0): -7.54,
        ("nimble-a", "rrl", 30.0): +5.91, ("nimble-b", "bhb", 30.0): -1.19}

OUT = open(os.path.join(HERE, "nmb1.out"), "w")
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
        json.dump({"lane": "NMB1", "label": "NO VERDICT (stopped at " + KA_FAIL[0].split()[0] + ")"},
                  open(os.path.join(HERE, "nmb1_results.json"), "w"), indent=1)
        sys.exit(0)

# ---------------------------------------------------------------- the line
def nu(y):
    return 1.0 / (1.0 - np.exp(-np.sqrt(np.maximum(np.asarray(y, float), 1e-14))))
MU = np.linspace(-1.0, 1.0, 4001)
def trapz(yv, xv):
    return float(np.sum((yv[1:] + yv[:-1]) * np.diff(xv)) / 2.0)
def M_line(r, a0, A=1.0, eN=0.0):
    """enclosed dynamical mass [1e11 Msun]; eN = 0 is E0, eN = E_N is G239's QUMOND angle average (E1)"""
    Mb = A * FSPH[r] * MB
    gb = G * Mb / (r * KPC) ** 2 / a0
    if eN == 0.0:
        return float(nu(gb)) * Mb / MSUN / 1e11
    gm = np.sqrt(gb * gb + eN * eN + 2 * gb * eN * MU)
    return trapz(nu(gm) * (gb + eN * MU), MU) / 2.0 / gb * Mb / MSUN / 1e11
def mu_line(a0, A=1.0, eN=0.0):
    return np.array([math.log10(M_line(r, a0, A, eN)) for r in RAD])

# ---------------------------------------------------------------- file access
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

# ---------------------------------------------------------------- linear algebra
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
sec("NMB1  NIMBLE curves of DESI DR2 Results III vs the framework's zero-parameter line   (criteria 1fd8ca964e)")
say("     TEST lane. kappa = 1/2 FITTED; not theory closed. Adopts nothing.")

sec("KNOWN-ANSWER CHECKS")
md5 = hashlib.md5(open(ZIP, "rb").read()).hexdigest()
ka("KA1 the file is the one named in the criteria", md5 == MD5, f"md5 {md5}")
stop_if_failed()

F10 = rows("fig10/desi-dr2-menc.csv")
CUR = collections.defaultdict(list)                 # (method, tracer) -> [(r, med, lo, hi)]
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

# mock residuals --------------------------------------------------------------------------------
MOCK = {}            # (method, tracer) -> {(halo, view): [(r, M)]}
TRUE = {}            # tracer -> {halo: [(r, M)]}
for tr, fig in (("rrl", "figA1"), ("bhb", "figA2")):
    t = collections.defaultdict(list)
    for r in rows(f"{fig}/truths.csv"): t[r["halo"]].append((float(r["r_kpc"]), float(r["Menc"])))
    TRUE[tr] = t
    for m in ("empdf", "gme", "nimble-a", "nimble-b"):
        d = collections.defaultdict(list)
        for r in rows(f"{fig}/{m}.csv"): d[(r["halo"], r["view"])].append((float(r["r_kpc"]), float(r["Menc_med"])))
        MOCK[(m, tr)] = d
KEYS = sorted(MOCK[("nimble-a", "rrl")].keys())
say(f"  mocks in the file: {len(KEYS)}  (haloes {sorted(set(k[0] for k in KEYS))}, views {sorted(set(k[1] for k in KEYS))})")
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
    """items: list of (method, tracer, r). Returns y, sigma, S_res, R, N (complete-case mocks)."""
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
KR = {}; det = []; ok4 = True
for r in RAD:
    th, sg, N, p = one_radius(r)
    ref, sref = TABLE4_ALL[r]
    ok4 &= abs(th - ref) <= sref and N >= 20
    KR[r] = max(1.0, sref / sg)
    det.append(f"{r:.0f} kpc: {th+11:.4f} +/- {sg:.4f} from {p} curves, N = {N} (Table 4: {ref+11:.3f} +/- {sref:.4f}; k = {KR[r]:.3f})")
ka("KA4 the machinery on all curves at one radius reproduces the paper's joint within one published sigma",
   ok4, "; ".join(det))
stop_if_failed()

ITEMS = [(m, tr, r) for r in RAD for m in ("nimble-a", "nimble-b") for tr in ("rrl", "bhb")]
def assemble(items, lam=LAMBDA, kr=None, hartlap=False, stat_only=False):
    y, s, Sres, R, N = build(items, lam)
    C = np.diag(s ** 2) if stat_only else ctot(s, Sres, R)
    kr = KR if kr is None else kr
    kv = np.array([kr[r] for (_, _, r) in items])
    C = C * np.outer(kv, kv)
    X = np.array([[1.0 if r == RAD[0] else 0.0, 1.0 if r == RAD[1] else 0.0] for (_, _, r) in items])
    pf = (N - len(items) - 2) / (N - 1) if hartlap else 1.0
    th, V, chi = gls(y, C, X, pf)
    return dict(y=y, s=s, C=C, X=X, th=th, V=V, chi=chi, N=N, p=len(items), pf=pf)
BASE = assemble(ITEMS)

# KA5 ------------------------------------------------------------------------------------------
x1, x2, s1, s2, rho = 1.0, 1.3, 0.2, 0.5, 0.4
Ct = np.array([[s1 * s1, rho * s1 * s2], [rho * s1 * s2, s2 * s2]])
tht, Vt, _ = gls(np.array([x1, x2]), Ct, np.ones((2, 1)))
den = s1 * s1 + s2 * s2 - 2 * rho * s1 * s2
cf_t = (x1 * (s2 * s2 - rho * s1 * s2) + x2 * (s1 * s1 - rho * s1 * s2)) / den
cf_v = s1 * s1 * s2 * s2 * (1 - rho * rho) / den
rng = np.random.default_rng(20261112)
mu0 = np.array([0.42, 0.80]); Lc = np.linalg.cholesky(BASE["C"]); Ci = np.linalg.inv(BASE["C"])
Vi = np.linalg.inv(BASE["V"]); Qs = []
for _ in range(20000):
    yy = BASE["X"] @ mu0 + Lc @ rng.standard_normal(len(ITEMS))
    d = BASE["V"] @ BASE["X"].T @ Ci @ yy - mu0
    Qs.append(float(d @ Vi @ d))
Qs = np.array(Qs)
ka("KA5 estimator and gate on synthetic data (closed form to 1e-10; mean Q 2.00 +/- 0.05; rejection 0.0455 +/- 0.005)",
   abs(tht[0] - cf_t) < 1e-10 and abs(Vt[0, 0] - cf_v) < 1e-10 and abs(Qs.mean() - 2.0) <= 0.05
   and abs((Qs > QGATE).mean() - 0.0455) <= 0.005,
   f"closed form {abs(tht[0]-cf_t):.1e}, {abs(Vt[0,0]-cf_v):.1e}; mean Q {Qs.mean():.3f}; rejection {(Qs > QGATE).mean():.4f}")

# KA6 ------------------------------------------------------------------------------------------
ref6 = {("canonical", 0.0): 5.691, ("alt", 0.0): 6.219, ("canonical", E_N): 4.977, ("alt", E_N): 5.109}
w6 = max(abs(M_line(80.0, A0[f], 1.0, e) / v - 1) for (f, e), v in ref6.items())
ka("KA6 the line reproduces the record at 80 kpc (E0 5.691 / 6.219; E1 4.977 / 5.109; each within 0.5 %)",
   w6 <= 0.005, "; ".join(f"{f} {'E1' if e else 'E0'} {M_line(80.0, A0[f], 1.0, e):.3f}" for (f, e) in ref6)
   + f"; worst {w6:.2%}")
stop_if_failed()

# ---------------------------------------------------------------- the gate
def gate(th, V, mu):
    d = mu - th
    Q = float(d @ np.linalg.inv(V) @ d)
    z30, z80 = d[0] / math.sqrt(V[0, 0]), d[1] / math.sqrt(V[1, 1])
    pd = (th[1] - th[0]) / L; pl = (mu[1] - mu[0]) / L
    sp = math.sqrt(V[0, 0] + V[1, 1] - 2 * V[0, 1]) / L
    zs = (pl - pd) / sp
    if Q <= QGATE: lab = "PASSES"
    else:
        lab = "FAILS " + ("LOW" if (z30 < 0 and z80 < 0) else "HIGH" if (z30 > 0 and z80 > 0) else "MIXED")
        if abs(zs) > 2: lab += " SHAPE"
        lab += " (2 to 3 sigma)" if Q <= Q3 else " (beyond 3 sigma)"
    if Q <= QGATE and abs(zs) > 2: lab += " [slope pull beyond 2]"
    return dict(Q=Q, p=math.exp(-Q / 2), z30=z30, z80=z80, zs=zs, slope_line=pl, slope_data=pd, sigma_slope=sp, label=lab)

# ---------------------------------------------------------------- mutations (separate output)
MUT = open(os.path.join(HERE, "nmb1_mut.out"), "w")
def msay(s): MUT.write(s + "\n"); MUT.flush()
msay("NMB1 mutations (criteria 1fd8ca964e). Each must bite.")
bite = True
for f, a0 in A0.items():
    g = gate(BASE["th"], BASE["V"], mu_line(a0, 2.0)); b = g["label"].startswith("FAILS HIGH"); bite &= b
    msay(f"M1 A = 2,   E0 {f:9s}: Q = {g['Q']:8.2f}  z30 {g['z30']:+.2f} z80 {g['z80']:+.2f}  -> {g['label']}  [{'bites' if b else 'DOES NOT BITE'}]")
    g = gate(BASE["th"], BASE["V"], mu_line(a0, 0.5)); b = g["label"].startswith("FAILS LOW"); bite &= b
    msay(f"M2 A = 0.5, E0 {f:9s}: Q = {g['Q']:8.2f}  z30 {g['z30']:+.2f} z80 {g['z80']:+.2f}  -> {g['label']}  [{'bites' if b else 'DOES NOT BITE'}]")
g = gate(BASE["th"], BASE["V"], np.array([BASE["th"][1], BASE["th"][1]])); b = g["label"].startswith("FAILS") and "SHAPE" in g["label"]; bite &= b
msay(f"M3 point mass (mu_30 = mu_80 = theta_80): Q = {g['Q']:8.2f}  zs {g['zs']:+.2f}  -> {g['label']}  [{'bites' if b else 'DOES NOT BITE'}]")
MUT.close()
sec("MUTATIONS")
say(f"  M1, M2, M3 written to nmb1_mut.out: {'all bite' if bite else 'AT LEAST ONE DOES NOT BITE -> NO POWER'}")
if not bite:
    json.dump({"lane": "NMB1", "label": "NO POWER"}, open(os.path.join(HERE, "nmb1_results.json"), "w"), indent=1)
    sys.exit(0)

# ====================================================================================================
sec("THE INSTRUMENT")
say("  curve            r    M_med [1e11]   16th    84th    log10 M   sigma_stat [dex]")
for (m, tr, r) in ITEMS:
    lg, s, med, lo, hi = data_at(m, tr, r)
    say(f"  {m:9s} {tr:3s}  {r:4.0f}   {med:7.3f}     {lo:6.3f}  {hi:6.3f}   {lg+11:7.4f}   {s:.4f}")
th, V = BASE["th"], BASE["V"]
say(f"\n  mocks used N = {BASE['N']}; shrinkage {LAMBDA}; error calibration k_30 = {KR[30.0]:.3f}, k_80 = {KR[80.0]:.3f}")
say(f"  NIMBLE-only common log10(M/Msun):  30 kpc {th[0]+11:.4f} +/- {math.sqrt(V[0,0]):.4f}  ({10**th[0]:.3f} e11)")
say(f"                                     80 kpc {th[1]+11:.4f} +/- {math.sqrt(V[1,1]):.4f}  ({10**th[1]:.3f} e11)")
say(f"  correlation between the two: {V[0,1]/math.sqrt(V[0,0]*V[1,1]):+.3f};  slope 30 to 80 kpc: {(th[1]-th[0])/L:.3f} +/- "
    f"{math.sqrt(V[0,0]+V[1,1]-2*V[0,1])/L:.3f}")
chi6 = BASE["chi"]; x = chi6 / 2
say(f"  internal consistency of the eight numbers about it: chi2 = {chi6:.2f} on 6 dof, p = {math.exp(-x)*(1+x+x*x/2):.3f}  (reported)")
say(f"  Table 4 joint (all methods) for comparison: 11.423 +/- 0.022 at 30, 11.804 +/- 0.035 at 80")

VAR = collections.OrderedDict()
VAR["NIMBLE-A only"] = assemble([i for i in ITEMS if i[0] == "nimble-a"])
VAR["NIMBLE-B only"] = assemble([i for i in ITEMS if i[0] == "nimble-b"])
VAR["NIMBLE-A RRL dropped"] = assemble([i for i in ITEMS if not (i[0] == "nimble-a" and i[1] == "rrl")])
kr0 = {r: max(1.0, TABLE4_ALL[r][1] / one_radius(r, 0.0, True)[1]) for r in RAD}
kr1 = {r: max(1.0, TABLE4_ALL[r][1] / one_radius(r, 1.0)[1]) for r in RAD}
VAR["lambda = 0 (Hartlap)"] = assemble(ITEMS, lam=0.0, kr=kr0, hartlap=True)
VAR["lambda = 1"] = assemble(ITEMS, lam=1.0, kr=kr1)
VAR["k = 1"] = assemble(ITEMS, kr={30.0: 1.0, 80.0: 1.0})
# implementation choice the criteria do not fix: lambda variants with the graded k instead of their own
ALT = {"lambda = 0 (Hartlap), graded k": assemble(ITEMS, lam=0.0, hartlap=True), "lambda = 1, graded k": assemble(ITEMS, lam=1.0)}
STAT = assemble(ITEMS, kr={30.0: 1.0, 80.0: 1.0}, stat_only=True)

sec("THE GATE   Q <= 6.180 on 2 dof.  z = (line - data)/sigma; negative = line below the data")
CASES = [("E1", "canonical", E_N), ("E1", "alt", E_N), ("E0", "canonical", 0.0), ("E0", "alt", 0.0)]
RES = {}
for rd, f, e in CASES:
    mu = mu_line(A0[f], 1.0, e)
    g = gate(th, V, mu)
    sides = {k: gate(v["th"], v["V"], mu) for k, v in VAR.items()}
    flips = [k for k, s in sides.items() if (s["Q"] <= QGATE) != (g["Q"] <= QGATE)]
    lab = g["label"] + (", FRAGILE" if flips else "")
    say(f"\n  {rd} {f}:  line {10**mu[0]:.3f} / {10**mu[1]:.3f} e11 at 30 / 80 kpc")
    say(f"     Q = {g['Q']:.2f} (p = {g['p']:.4f});  z30 = {g['z30']:+.2f}, z80 = {g['z80']:+.2f};  slope line {g['slope_line']:.3f} vs data "
        f"{g['slope_data']:.3f} +/- {g['sigma_slope']:.3f}, z_s = {g['zs']:+.2f}")
    say(f"     LABEL: {lab}")
    for k, s in sides.items():
        say(f"       variant {k:24s} Q = {s['Q']:7.2f}  z30 {s['z30']:+.2f} z80 {s['z80']:+.2f} z_s {s['zs']:+.2f}  {'pass' if s['Q'] <= QGATE else 'fail'}"
            + ("   <- other side" if k in flips else ""))
    for k, v in ALT.items():
        s = gate(v["th"], v["V"], mu)
        say(f"       (unfixed choice) {k:31s} Q = {s['Q']:7.2f}  {'pass' if s['Q'] <= QGATE else 'fail'}")
    s = gate(STAT["th"], STAT["V"], mu)
    say(f"       reported: published bands only  Q = {s['Q']:7.2f}  z30 {s['z30']:+.2f} z80 {s['z80']:+.2f}")
    # amplitude that minimises Q
    grid = np.linspace(0.6, 2.6, 2001); qq = np.array([gate(th, V, mu_line(A0[f], a, e))["Q"] for a in grid])
    i = int(np.argmin(qq)); inside = grid[qq <= qq[i] + 1.0]
    say(f"       reported: A* = {grid[i]:.3f} [{inside.min():.3f}, {inside.max():.3f}], Q(A*) = {qq[i]:.2f}")
    RES[f"{rd}_{f}"] = dict(label=lab, **{k: float(v) for k, v in g.items() if k != "label"},
                            line_30=10 ** mu[0], line_80=10 ** mu[1], flips=flips, A_star=float(grid[i]),
                            A_star_lo=float(inside.min()), A_star_hi=float(inside.max()), Q_at_A_star=float(qq[i]),
                            variants={k: s["Q"] for k, s in sides.items()}, Q_published_bands=s["Q"])

sec("REPORTED, NOT GRADED")
H0 = 67.77e3 / 3.0856775814913673e22; rhoc = 3 * H0 ** 2 / (8 * math.pi * G)
M200 = 1.19e12 * MSUN; r200 = (3 * M200 / (4 * math.pi * 200 * rhoc)) ** (1 / 3); cN = 12.0
mN = lambda xx: math.log(1 + xx) - xx / (1 + xx)
nfw = np.array([math.log10(M200 * mN(r * KPC / (r200 / cN)) / mN(cN) / MSUN / 1e11) for r in RAD])
gN = gate(th, V, nfw)
say(f"  the paper's NFW (1.19e12, c = 12): {10**nfw[0]:.3f} / {10**nfw[1]:.3f} e11; Q = {gN['Q']:.2f}; z30 {gN['z30']:+.2f}, z80 {gN['z80']:+.2f}, z_s {gN['zs']:+.2f}  -> {gN['label']}")
for m in ("empdf", "gme"):
    for tr in ("rrl", "bhb"):
        lg, s, med, lo, hi = data_at(m, tr, 80.0)
        say(f"  {m:6s} {tr} at 80 kpc: {med:.2f} (+{hi-med:.2f}, -{med-lo:.2f}) e11")
for f, v in (("canonical", 4.486839), ("alt", 4.579205)):
    say(f"  matched-field AQUAL value of today's correction lane, {f}: {v:.3f} e11 at 80 kpc, pull {(math.log10(v)-th[1])/math.sqrt(V[1,1]):+.2f}")

sec("LABELS")
say("  E1 canonical / E1 alt / E0 canonical / E0 alt:")
say("  " + "  /  ".join(RES[f"{rd}_{f}"]["label"] for rd, f, _ in CASES))
json.dump(dict(lane="NMB1", criteria="1fd8ca964e", date="2026-11-12", zip_md5=md5, N_mocks=BASE["N"], shrinkage=LAMBDA,
               k=KR, theta=[float(t) for t in th], V=[[float(v) for v in row] for row in V],
               chi2_internal_6dof=chi6, cases=RES,
               nfw=dict(Q=gN["Q"], z30=gN["z30"], z80=gN["z80"], zs=gN["zs"], label=gN["label"])),
          open(os.path.join(HERE, "nmb1_results.json"), "w"), indent=1)
say("\nNMB1 COMPLETE. kappa = 1/2 FITTED; not theory closed. Adopts nothing.")
