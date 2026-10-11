"""CFG700: early-type age signal on RAW lensing only. Criteria: FROZEN_CRITERIA.md (cc3a6a7cf).
Executes cfg585_age.py's head (unedited) for masks and the raw estimator esd_loo; no comps/environment/law used.
MUTATE: CFG700_MUTATE=1 multiplies the OLD group's WG by 0.8 (linearity check).
"""
import os, io, json, math, contextlib
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
LANES = os.path.dirname(HERE)
ROOT = os.path.dirname(LANES)
MUTATE = os.environ.get("CFG700_MUTATE", "0") == "1"
TAG = "_MUTATE" if MUTATE else ""
OUT, CHECKS = [], []


def P(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); OUT.append(s)


def check(c, m):
    CHECKS.append((bool(c), m)); P(f"  [{'PASS' if c else 'FAIL'}] {m}"); return bool(c)


for v in ("CFG585_MUTATE", "CFG531_MUTATE"):
    os.environ.pop(v, None)
path = os.path.join(LANES, "CFG585_age_settling", "cfg585_age.py")
ns = {"__file__": path, "__name__": "head"}
with contextlib.redirect_stdout(io.StringIO()):
    exec(compile(open(path).read().split('P("=" * 100)')[0], path, "exec"), ns)
U, F30, TYP, LMSL, esd_loo, NPATCH = (ns[k] for k in ("U", "F30", "TYP", "LMSL", "esd_loo", "NPATCH"))
G = esd_loo.__globals__
WG0 = G["WG"].copy()
ZL = np.load(os.path.join(ROOT, "real_research", "data", "lensing_rar", "lr_lenses.npz"))["z"]
assert len(ZL) == len(U)

# CFG589's early-type stratified tertiles (same code, same order)
C = F30 & (TYP == 1)
qb = np.quantile(LMSL[C], np.linspace(0, 1, 11)); qb[-1] += 1e-9
BIN_IDX = [np.where(C & (LMSL >= qb[i]) & (LMSL < qb[i + 1]))[0] for i in range(10)]


def tertiles(perm_rng=None):
    ter = np.full(len(U), -1)
    for idx in BIN_IDX:
        dc = U[idx] - np.median(U[idx])
        if perm_rng is not None:
            dc = perm_rng.permutation(dc)
        o = np.argsort(dc, kind="stable"); n = len(idx)
        for k in range(3):
            ter[idx[o[k * n // 3:(k + 1) * n // 3]]] = k
    return [(ter == k) & C for k in range(3)]


YOUNG, MID, OLD = tertiles()
if MUTATE:
    G["WG"] = WG0.copy(); G["WG"][OLD] *= 0.8
BANDS = {"K9": list(range(6, 15)), "K-in": [12, 13, 14], "K-mid": [9, 10, 11], "K-out": [6, 7, 8]}

dall, Call, _ = esd_loo(C)
W = 1.0 / np.diag(Call)


def amp(mo, my):
    do, _, Lo = esd_loo(mo); dy, _, Ly = esd_loo(my); out = {}
    for b, ks in BANDS.items():
        a = math.log10((W[ks] @ do[ks]) / (W[ks] @ dy[ks]))
        al = np.log10((Lo[:, ks] @ W[ks]) / (Ly[:, ks] @ W[ks]))
        sj = math.sqrt((NPATCH - 1) / NPATCH * ((al - al.mean()) ** 2).sum())
        out[b] = (a, sj)
    return out, do, dy


P("=" * 100)
P(f"CFG700  early-type age signal on RAW lensing (no model)  {'*** MUTATE: OLD WG x 0.8 ***' if MUTATE else 'PRIMARY'}")
P("=" * 100)
for name, m in (("OLD", OLD), ("MID", MID), ("YOUNG", YOUNG)):
    P(f"  {name:5s} N {m.sum():6d}  median u-r {np.median(U[m]):.3f}  median log M* {np.median(LMSL[m]):.3f}  median z {np.median(ZL[m]):.3f}")
P("\n--- controls")
check(abs(np.median(LMSL[OLD]) - np.median(LMSL[YOUNG])) < 0.02, f"C1 median log M* OLD-YOUNG {np.median(LMSL[OLD]) - np.median(LMSL[YOUNG]):+.4f} (< 0.02)")
dz = np.median(ZL[OLD]) - np.median(ZL[YOUNG])
zflag = not check(abs(dz) < 0.02, f"C2 median lens z OLD-YOUNG {dz:+.4f} (< 0.02)")
if not MUTATE:
    dsum, _, _ = esd_loo(OLD | MID | YOUNG)
    check(np.max(np.abs(dsum - dall)) < 1e-10 * np.max(np.abs(dall)) + 1e-14, f"C3 OLD+MID+YOUNG closure max|diff| {np.max(np.abs(dsum - dall)):.2e}")

res, do, dy = amp(OLD, YOUNG)
P("\n--- raw ESD per bin (h M_sun/pc^2 units of the CFG531 estimator), OLD / YOUNG / ratio")
for k in range(6, 15):
    P(f"  bin {k:2d}: OLD {do[k]:9.4f}  YOUNG {dy[k]:9.4f}  ratio {do[k] / dy[k]:6.3f}  (all-early sigma {1 / math.sqrt(W[k]):.4f})")

res_null = None
if not MUTATE:
    rng = np.random.default_rng(700)
    nulls = {b: [] for b in BANDS}
    for i in range(200):
        y, mi, o = tertiles(rng)
        r, _, _ = amp(o, y)
        for b in BANDS:
            nulls[b].append(r[b][0])
    nulls = {b: np.array(v) for b, v in nulls.items()}
    check(abs(nulls["K9"].mean()) < nulls["K9"].std() / 3, f"C4 null mean {nulls['K9'].mean():+.4f} vs sigma/3 {nulls['K9'].std() / 3:.4f}")
    res_null = {b: dict(mean=float(v.mean()), sd=float(v.std()), frac_ge=float((v >= res[b][0]).mean())) for b, v in nulls.items()}

P("\n--- amplitude A = log10(OLD/YOUNG), weighted raw ESD")
for b in BANDS:
    a, sj = res[b]
    line = f"  {b:5s} A {a:+.4f} (x{10 ** a:.2f})  jackknife sigma {sj:.4f} (Z_jk {a / sj:+.2f})"
    if res_null:
        sd = res_null[b]["sd"]; line += f"  null sigma {sd:.4f} -> Z_emp {a / sd:+.2f}  (emp/jk {sd / sj:.2f}; null frac >= A {res_null[b]['frac_ge']:.3f})"
    P(line)

verdict = None
if not MUTATE:
    a = res["K9"][0]; Z = a / res_null["K9"]["sd"]
    verdict = "AGE SIGNAL ON RAW DATA" if (a > 0 and Z >= 2) else "NONE" if abs(Z) < 1 else "WEAK"
    if zflag:
        verdict += " (FLAGGED: lens-z medians differ)"
    P(f"\nVERDICT (K9): {verdict}")
else:
    G["WG"] = WG0
    base, _, _ = amp(OLD, YOUNG)
    for b in BANDS:
        check(abs(res[b][0] - base[b][0] - math.log10(0.8)) < 1e-6, f"MUTATE {b}: dA {res[b][0] - base[b][0]:+.7f} vs log10(0.8) {math.log10(0.8):+.7f}")
P(f"\nchecks: {sum(c for c, _ in CHECKS)}/{len(CHECKS)} pass")
json.dump(dict(verdict=verdict, A={b: dict(A=v[0], sig_jk=v[1]) for b, v in res.items()}, null=res_null,
               esd_old=do.tolist(), esd_young=dy.tolist(), N=dict(old=int(OLD.sum()), young=int(YOUNG.sum())), checks=CHECKS),
          open(os.path.join(HERE, f"cfg700_results{TAG}.json"), "w"), indent=1, default=float)
open(os.path.join(HERE, f"cfg700_raw{TAG}.out"), "w").write("\n".join(OUT) + "\n")
