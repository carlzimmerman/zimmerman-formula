#!/usr/bin/env python3
"""CFG721 (FROZEN_CRITERIA.md, 94c4b06b3): which property carries the KiDS early-type lensing excess?
Part A: B21 released isolated RAR stacks, Sersic vs colour split offsets at the same g_bar (g_bar <= 1e-12).
Part B: own stacks (CFG585 head + CFG531 esd_loo, unedited) at matched Ks baryonic mass: six u-r sextiles, step vs continuous trend.
Raw lensing only; no law, no LCDM.  CFG721_MUTATE=1 CFG721_M=M1|M2 -> _MUTATE outputs, exit 1 iff the tooth bites."""
import os, io, json, math, tarfile, tempfile, contextlib
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__)); LANES = os.path.dirname(HERE); ROOT = os.path.dirname(LANES)
MUT = os.environ.get("CFG721_MUTATE", "0") == "1"; MODE = os.environ.get("CFG721_M", "") if MUT else ""
TAG = f"_MUTATE{MODE}" if MUT else ""
OUT, RES = [], {"lane": "CFG721", "criteria": "94c4b06b3", "mutate": MUT, "mode": MODE}


def P(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); OUT.append(s)


# ======================================================================== Part A
TAR = os.path.join(os.path.dirname(ROOT), "_external_data", "kids_lensing_zsplit", "brouwer2021_rar.tar")
tmp = tempfile.mkdtemp(prefix="cfg721_b21_")
with tarfile.open(TAR) as tf:
    for mbr in tf.getmembers():
        if mbr.isfile() and mbr.name.endswith(".txt") and ".." not in mbr.name and not mbr.name.startswith("/"):
            tf.extract(mbr, tmp, filter="data")


def find(name):
    for r, _, fs in os.walk(tmp):
        if name in fs:
            return os.path.join(r, name)
    raise FileNotFoundError(name)


def split_offset(stem, mins):
    d1 = np.loadtxt(find(f"Fig-8_RAR-KiDS-isolated_{stem}_1.txt")); d2 = np.loadtxt(find(f"Fig-8_RAR-KiDS-isolated_{stem}_2.txt"))
    gb = d1[:, 0]; e1 = d1[:, 1] / d1[:, 4]; e2 = d2[:, 1] / d2[:, 4]
    if MODE == "M1":
        e1, e2 = e2, e1
    n = len(gb); Cf = np.zeros((2 * n, 2 * n))
    cv = np.loadtxt(find(f"Fig-8_RAR-KiDS-isolated_{stem}s_covmatrix.txt"))
    for row in cv:
        m = 0 if np.isclose(row[0], mins[0]) else 1; nn = 0 if np.isclose(row[1], mins[0]) else 1
        i = int(np.argmin(np.abs(np.log(gb) - math.log(row[2])))); j = int(np.argmin(np.abs(np.log(gb) - math.log(row[3]))))
        Cf[m * n + i, nn * n + j] = row[4] / row[6]
    if MODE == "M1":
        Cf = np.block([[Cf[n:, n:], Cf[n:, :n]], [Cf[:n, n:], Cf[:n, :n]]])
    sel = np.where((gb <= 1e-12) & (e1 > 0) & (e2 > 0))[0]
    ell = np.log10(e2[sel] / e1[sel])
    J = np.zeros((len(sel), 2 * n))
    for k, i in enumerate(sel):
        J[k, i] = -1 / (math.log(10) * e1[i]); J[k, n + i] = 1 / (math.log(10) * e2[i])
    Cl = J @ Cf @ J.T; Ci = np.linalg.inv(Cl); one = np.ones(len(sel))
    var = 1 / (one @ Ci @ one); D = float(var * (one @ Ci @ ell))
    return dict(delta=D, sigma=float(math.sqrt(var)), Z=float(D / math.sqrt(var)), bins=sel.tolist(), ell=ell.tolist())


A_ser = split_offset("Sersicbin", (0.0, 2.0)); A_col = split_offset("Colorbin", (0.0, 2.5))
sd = math.sqrt(A_ser["sigma"] ** 2 + A_col["sigma"] ** 2); dd = A_col["delta"] - A_ser["delta"]
clsA = "COLOUR CARRIES IT" if dd >= 2 * sd else ("STRUCTURE CARRIES IT" if -dd >= 2 * sd else "BOTH / UNDECIDED")
P(f"CFG721  which property carries the early-type lensing excess  {('MUTATE ' + MODE) if MUT else 'PRIMARY'}")
P(f"Part A (B21, g_bar <= 1e-12, bins {A_col['bins']}):")
P(f"   colour split (u-r >= 2.5 vs < 2.5): Delta = {A_col['delta']:+.4f} +- {A_col['sigma']:.4f} (Z {A_col['Z']:+.2f})")
P(f"   Sersic split (n >= 2 vs < 2):      Delta = {A_ser['delta']:+.4f} +- {A_ser['sigma']:.4f} (Z {A_ser['Z']:+.2f})")
P(f"   colour - Sersic = {dd:+.4f} +- {sd:.4f} ({dd / sd:+.2f} sigma) -> {clsA}")
RES["A"] = dict(colour=A_col, sersic=A_ser, diff=dd, sigma_diff=sd, cls=clsA)

# ======================================================================== Part B
for v in ("CFG585_MUTATE", "CFG531_MUTATE"):
    os.environ.pop(v, None)
path = os.path.join(LANES, "CFG585_age_settling", "cfg585_age.py")
ns = {"__file__": path, "__name__": "head"}
with contextlib.redirect_stdout(io.StringIO()):
    exec(compile(open(path).read().split('P("=" * 100)')[0], path, "exec"), ns)
U, F30, TYP, LMSL, esd_loo, NPATCH = (ns[k] for k in ("U", "F30", "TYP", "LMSL", "esd_loo", "NPATCH"))
Lp, o, ix = ns["Lp"], ns["o"], ns["ix"]
G = esd_loo.__globals__; WG0, WW0 = G["WG"].copy(), G["WW"].copy()
LT = np.load(os.path.join(ROOT, "real_research", "data", "lensing_rar", "lr_lenses.npz"))
FC = LT["Mgal"] / 10 ** LT["logM"] - 1
kabs = np.array(Lp["MAG_ABS_Ks"], "f8")[o[ix]]
LK = 0.4 * (5.08 - kabs); cK = float(np.median(LMSL[F30]) - np.median(LK[F30])); LMK = LK + cK
LMBK = np.full(len(TYP), np.nan)
for ty in (0, 1):
    m = TYP == ty
    edges = np.arange(np.floor(LT["logM"][m].min() * 10) / 10, LT["logM"][m].max() + 0.1, 0.1)
    cen, med = [], []
    for a, b in zip(edges[:-1], edges[1:]):
        s = m & (LT["logM"] >= a) & (LT["logM"] < b)
        if s.sum() >= 20:
            cen.append(0.5 * (a + b)); med.append(np.median(FC[s]))
    LMBK[m] = LMK[m] + np.log10(1 + np.interp(LMK[m], cen, med))
S = F30 & np.isfinite(LMBK) & np.isfinite(U)
K9 = list(range(6, 15))
dall, Call, Lall = esd_loo(S); W = 1.0 / np.diag(Call)
Uc = U.copy()
qd = np.quantile(LMBK[S], np.linspace(0, 1, 11)); qd[-1] += 1e-9
dec = np.clip(np.searchsorted(qd, LMBK, side="right") - 1, 0, 9)
if MODE == "M2":
    rng = np.random.default_rng(721)
    for d in range(10):
        idx = np.where(S & (dec == d))[0]; Uc[idx] = rng.permutation(Uc[idx])
qs = np.quantile(Uc[S], np.linspace(0, 1, 7)); qs[-1] += 1e-9
pall = np.array([np.mean(dec[S] == d) for d in range(10)])
A, Aloo, med = [], [], []
for k in range(6):
    mk = S & (Uc >= qs[k]) & (Uc < qs[k + 1])
    r = np.zeros(len(TYP))
    for d in range(10):
        md = mk & (dec == d); frac = md.sum() / mk.sum()
        if frac > 0:
            r[md] = pall[d] / frac
    G["WG"] = WG0 * r[:, None]; G["WW"] = WW0 * r[:, None]
    dk, _, Lk = esd_loo(mk)
    G["WG"], G["WW"] = WG0.copy(), WW0.copy()
    A.append(math.log10((W[K9] @ dk[K9]) / (W[K9] @ dall[K9])))
    Aloo.append(np.log10((Lk[:, K9] @ W[K9]) / (Lall[:, K9] @ W[K9])))
    med.append(float(np.median(Uc[mk])))
A = np.array(A); Aloo = np.array(Aloo).T; dev = Aloo - Aloo.mean(0)
Cv = (NPATCH - 1) / NPATCH * dev.T @ dev; Ci = np.linalg.inv(Cv)
med = np.array(med)


def gls(X):
    F = X.T @ Ci @ X; beta = np.linalg.solve(F, X.T @ Ci @ A); cov = np.linalg.inv(F); r = A - X @ beta
    return beta, np.sqrt(np.diag(cov)), float(r @ Ci @ r)


bS, sS, chiS = gls(np.column_stack([np.ones(6), (med > 2.0).astype(float)]))
bC, sC, chiC = gls(np.column_stack([np.ones(6), med - 2.0]))
clsB = "STEP PREFERRED" if (chiC - chiS) >= 4 else ("CONTINUOUS PREFERRED" if (chiC - chiS) <= -4 else "UNDECIDED")
P(f"\nPart B (own stacks, matched Ks baryonic mass; six u-r sextiles, A_k vs the whole f30 sample, K9):")
for k in range(6):
    P(f"   sextile {k}: median u-r {med[k]:.3f}  A {A[k]:+.4f} +- {math.sqrt(Cv[k, k]):.4f}")
P(f"   step:       b = {bS[1]:+.4f} +- {sS[1]:.4f}  chi2 {chiS:.2f} / 4")
P(f"   continuous: c = {bC[1]:+.4f} +- {sC[1]:.4f} per mag  chi2 {chiC:.2f} / 4")
P(f"   chi2_cont - chi2_step = {chiC - chiS:+.2f} -> {clsB}")
RES["B"] = dict(median_ur=med.tolist(), A=A.tolist(), sigma=np.sqrt(np.diag(Cv)).tolist(), step=dict(b=float(bS[1]), s=float(sS[1]), chi2=chiS),
                cont=dict(c=float(bC[1]), s=float(sC[1]), chi2=chiC), dchi2=chiC - chiS, cls=clsB, c_K=cK)
rc = 0
if MUT:
    if MODE == "M1":
        J0 = json.load(open(os.path.join(HERE, "cfg721_results.json")))
        bite = abs(A_col["delta"] + J0["A"]["colour"]["delta"]) < 1e-9 and abs(A_ser["delta"] + J0["A"]["sersic"]["delta"]) < 1e-9
    else:
        bite = abs(bS[1]) < 2 * sS[1] and abs(bC[1]) < 2 * sC[1]
    RES["tooth_bites"] = bool(bite); P(f"\nMUTATE {MODE}: tooth bites {bite}"); rc = 1 if bite else 0
else:
    P(f"\nPart A: {clsA};  Part B: {clsB}")
json.dump(RES, open(os.path.join(HERE, f"cfg721_results{TAG}.json"), "w"), indent=1, default=float)
open(os.path.join(HERE, f"cfg721{TAG}.out"), "w").write("\n".join(OUT) + "\n")
raise SystemExit(rc)
