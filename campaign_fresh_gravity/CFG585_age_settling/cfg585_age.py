"""CFG585: do older early types carry more KiDS inner excess at fixed mass? Criteria: FROZEN_CRITERIA.md (6fc71e70f).
Executes CFG531's cfg531_kids.py UNEDITED up to its analysis section (definitions + data only; no CFG531 output written).
MUTATE: CFG585_MUTATE=1 relabels OLD/YOUNG at random within mass quintiles.
"""
import os, sys, io, json, math, contextlib
import numpy as np
from astropy.io import fits

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.abspath(os.path.join(HERE, "..", "CFG531_inner_halo_shortfall", "cfg531_kids.py"))
src = open(SRC).read()
cut = "EARLY = TYP == 1"
assert src.count(cut) == 1
os.environ.pop("CFG531_MUTATE", None)
ns = {"__file__": SRC, "__name__": "cfg531_head"}
with contextlib.redirect_stdout(io.StringIO()):
    exec(compile(src.split(cut)[0], SRC, "exec"), ns)
esd_loo, comps, all_bands = ns["esd_loo"], ns["comps"], ns["all_bands"]
F30, TYP, LMSL, BANDS, CONS, FOOTS, NPATCH = ns["F30"], ns["TYP"], ns["LMSL"], ns["BANDS"], ns["CONS"], ns["FOOTS"], ns["NPATCH"]
lens = ns["lens"]

REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
D = os.path.join(REPO, "real_research", "data", "lensing_rar")
MUTATE = os.environ.get("CFG585_MUTATE", "0") == "1"
TAG = "_MUTATE" if MUTATE else ""
OUT, CHECKS = [], []


def P(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); OUT.append(s)


def check(c, m):
    CHECKS.append((bool(c), m)); P(f"  [{'PASS' if c else 'FAIL'}] {m}"); return bool(c)


# ---- colours (exact RA/Dec match, as in the pre-flight)
b = fits.open(os.path.join(D, "KiDS_DR4_brightsample.fits"), memmap=True)[1].data
Lp = fits.open(os.path.join(D, "KiDS_DR4_brightsample_LePhare.fits"), memmap=True)[1].data
ra, dec = np.array(b["RAJ2000"], "f8"), np.array(b["DECJ2000"], "f8")
ur = np.array(Lp["MAG_ABS_u"] - Lp["MAG_ABS_r"], "f8")
key = lambda r, d: np.round(r * 1e6).astype(np.int64) * 10 ** 9 + np.round((d + 90) * 1e6).astype(np.int64)
kb = key(ra, dec); o = np.argsort(kb); kbs = kb[o]
kl = key(np.asarray(lens["ra"]), np.asarray(lens["dec"])); ix = np.clip(np.searchsorted(kbs, kl), 0, len(kbs) - 1)
ok = kbs[ix] == kl
U = np.full(len(kl), np.nan); U[ok] = ur[o[ix[ok]]]
assert ok.all() and np.all((U > 2.0) == (TYP == 1))

E = F30 & (TYP == 1)
lm = LMSL.copy()
qb = np.quantile(lm[E], np.linspace(0, 1, 6))
res = np.full(len(lm), np.nan); qid = np.full(len(lm), -1)
for i in range(5):
    m = E & (lm >= qb[i]) & (lm <= qb[i + 1]); res[m] = U[m] - np.median(U[m]); qid[m] = i
t1, t2 = np.nanquantile(res[E], [1 / 3, 2 / 3])
OLD, YOUNG = E & (res > t2), E & (res < t1)
if MUTATE:
    rng = np.random.default_rng(585); lab = np.zeros(len(lm), int); lab[OLD] = 1; lab[YOUNG] = -1
    for i in range(5):
        m = E & (qid == i); lab[m] = rng.permutation(lab[m])
    OLD, YOUNG = lab == 1, lab == -1

P("=" * 100)
P(f"CFG585  older vs younger early types (KiDS f30, validated environment)  {'*** MUTATE: random relabel ***' if MUTATE else 'PRIMARY'}")
P("=" * 100)
P(f"f30 early {E.sum()}; OLD {OLD.sum()} / YOUNG {YOUNG.sum()}; colour residual separation {np.median(res[OLD]) - np.median(res[YOUNG]):.3f} mag")
P("\n--- controls")
check(abs(np.median(lm[OLD]) - np.median(lm[YOUNG])) < 0.05, f"C1 median log M* OLD {np.median(lm[OLD]):.3f} vs YOUNG {np.median(lm[YOUNG]):.3f} (0.05)")

R = {}
for cls, mk in (("early_all", E), ("old", OLD), ("young", YOUNG)):
    if cls == "early_all" and MUTATE:
        continue
    dcl, Ccl, Lcl = esd_loo(mk)
    for c in CONS:
        for foot in FOOTS:
            if cls == "early_all" and not (c == "A" and foot == "canonical"):
                continue
            cp = comps(c, foot, mk)
            fb = all_bands(dcl, Ccl, cp)
            mM = cp["moster"][0] + cp["moster"][1]
            loo = {bd: (Lcl[:, ii] - mM[ii][None, :]) @ np.array(fb[bd]["wvec"]) for bd, ii in BANDS.items()}
            R[f"{cls}|{c}|{foot}"] = dict(n=int(mk.sum()), bands={bd: dict(eps=fb[bd]["eps"], sig=fb[bd]["sig"], Z=fb[bd]["Z"]) for bd in BANDS},
                                         loo={bd: v for bd, v in loo.items()})
if not MUTATE:
    e0 = R["early_all|A|canonical"]["bands"]["K-in"]["eps"]
    check(abs(e0 - 0.5378) < 0.005, f"C2 CFG531 full-early eps(K-in, A, canonical) reproduced: {e0:+.4f} vs +0.5378")

P("\n--- D = eps_old - eps_young (error = max(jackknife, quadrature), CFG531's rule)")
calls = {}
for c in CONS:
    for foot in FOOTS:
        row = []
        for bd in ("K-in", "K9"):
            eo, ey = R[f"old|{c}|{foot}"], R[f"young|{c}|{foot}"]
            dv = eo["loo"][bd] - ey["loo"][bd]
            vj = (NPATCH - 1) / NPATCH * np.sum((dv - dv.mean()) ** 2)
            vq = eo["bands"][bd]["sig"] ** 2 + ey["bands"][bd]["sig"] ** 2
            dd = eo["bands"][bd]["eps"] - ey["bands"][bd]["eps"]; s = math.sqrt(max(vj, vq))
            R[f"D|{c}|{foot}|{bd}"] = dict(D=dd, sig=s, Z=dd / s, eps_old=eo["bands"][bd]["eps"], eps_young=ey["bands"][bd]["eps"])
            row.append(f"{bd}: old {eo['bands'][bd]['eps']:+.3f} young {ey['bands'][bd]['eps']:+.3f}  D {dd:+.3f} +- {s:.3f} (Z {dd / s:+.2f})")
        P(f"  [{c} {foot:9s}] " + "   ".join(row))
zs = [R[f"D|{c}|{f}|K-in"]["Z"] for c in CONS for f in FOOTS]
verdict = "CONFIRMED" if all(z >= 2 for z in zs) else ("CONTRADICTED" if all(z <= -2 for z in zs) else "NOT CONFIRMED [LOW POWER]")
P(f"\nVERDICT: {verdict}   (K-in Z per cell: {['%+.2f' % z for z in zs]})")
if MUTATE:
    ok_m = all(abs(z) < 2 for z in zs)
    check(ok_m, f"MUTATE: random relabel gives |Z| < 2 in all four K-in cells: {['%+.2f' % z for z in zs]}")
P(f"\nchecks: {sum(c for c, _ in CHECKS)}/{len(CHECKS)} pass")
json.dump(dict(verdict=verdict, R={k: ({kk: (vv.tolist() if hasattr(vv, 'tolist') else vv) for kk, vv in v.items()} if isinstance(v, dict) else v) for k, v in R.items()}, checks=CHECKS),
          open(os.path.join(HERE, f"cfg585_results{TAG}.json"), "w"), indent=1, default=lambda x: x.tolist() if hasattr(x, "tolist") else str(x))
open(os.path.join(HERE, f"cfg585_age{TAG}.out"), "w").write("\n".join(OUT) + "\n")
