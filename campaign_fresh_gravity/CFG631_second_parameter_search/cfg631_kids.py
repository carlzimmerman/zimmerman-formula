"""CFG631 KiDS: partial-property tertiles of f30 early types (u-r, r-Ks, sSFR, photo-z, companion count), CFG531 estimator,
joint-permutation null (200 draws). The age signal (u-r) is the pre-declared confirmatory target. Criteria: FROZEN_CRITERIA.md
(06ca28e0d). Heads of cfg585_age.py (CFG531 estimator) and cfg509_counts.py executed unedited; no output of theirs is written.
Run: nice -n 10 python3 cfg631_kids.py   (about 20 min, ~1.2 GB)
"""
import os, sys, json, math, time
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import cfg631_common as K  # noqa: E402

try:
    os.nice(10)
except OSError:
    pass
OUT, CHECKS = [], []
NNULL, SEED = 200, 6310
D585 = {("A", "canonical"): 0.9411, ("A", "alt"): 0.8619, ("B", "canonical"): 0.9376, ("B", "alt"): 0.8586}


def P(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); OUT.append(s)


def check(c, m):
    CHECKS.append((bool(c), m)); P(f"  [{'PASS' if c else 'FAIL'}] {m}"); return bool(c)


t0 = time.time()
A, B = K.kids_heads()
raw, part, E2, qid = K.kids_props(A, B)
esd_loo, comps, all_bands, BANDS, CONS, FOOTS, NPATCH = (A[k] for k in ("esd_loo", "comps", "all_bands", "BANDS", "CONS", "FOOTS", "NPATCH"))
LM = A["LMSL"]
CELLS = [(c, f) for c in CONS for f in FOOTS]


def group_eps(mask):
    d, Cv, Lj = esd_loo(mask); out = {}
    for c, f in CELLS:
        cp = comps(c, f, mask); fb = all_bands(d, Cv, cp); mM = cp["moster"][0] + cp["moster"][1]
        out[(c, f)] = (fb, {bd: (Lj[:, ii] - mM[ii][None, :]) @ np.array(fb[bd]["wvec"]) for bd, ii in BANDS.items()})
    return out


def contrast(hi, lo):
    gh, gl = group_eps(hi), group_eps(lo); res = {}
    for c, f in CELLS:
        for bd in ("K9", "K-in"):
            (fh, lh), (fl, ll) = gh[(c, f)], gl[(c, f)]
            dv = lh[bd] - ll[bd]; vj = (NPATCH - 1) / NPATCH * np.sum((dv - dv.mean()) ** 2)
            vq = fh[bd]["sig"] ** 2 + fl[bd]["sig"] ** 2; s = math.sqrt(max(vj, vq)); dd = fh[bd]["eps"] - fl[bd]["eps"]
            res[(c, f, bd)] = dict(D=float(dd), sig=float(s), Z=float(dd / s), eps_hi=float(fh[bd]["eps"]), eps_lo=float(fl[bd]["eps"]))
    return res


def tert(v, base):
    t1, t2 = np.nanquantile(v[base], [1 / 3, 2 / 3]); return base & (v > t2), base & (v < t1)


def Tstat(res, bd="K9"):
    return float(np.mean([res[(c, f, bd)]["Z"] for c, f in CELLS]))


P("=" * 110)
P("CFG631 KiDS: which lens property tracks the inner excess of f30 early types at fixed M*? (age = confirmatory target)")
P("=" * 110)
P(f"f30 early {int(A['E'].sum())}; analysed (all five properties finite) {int(E2.sum())}")
P("\n--- controls")
r0 = contrast(A["OLD"], A["YOUNG"])
check(abs(r0[("A", "canonical", "K9")]["D"] - 0.9411) < 0.001, f"C3 CFG585 D(K9, A, canonical) reproduced: {r0[('A', 'canonical', 'K9')]['D']:+.4f} (+0.9411)")
MASK = {k: tert(part[k], E2) for k in K.KPROPS}
hi, lo = MASK["ur"]
check(abs(np.median(LM[hi]) - np.median(LM[lo])) < 0.05, f"C4 u-r HIGH/LOW median log M* {np.median(LM[hi]):.3f} / {np.median(LM[lo]):.3f} (0.05)")
lam = {}
for nm, mk in (("ur_HIGH", hi), ("ur_LOW", lo)):
    full, sd, jk = B["stat"](mk, B["wl"]); lam[nm] = (float(full[3]), float(sd[3]), jk[:, 3])
dl = lam["ur_HIGH"][2] - lam["ur_LOW"][2]; sdl = math.sqrt((NPATCH - 1) / NPATCH * np.sum((dl - dl.mean()) ** 2))
P(f"  (reported) companion lambda u-r HIGH {lam['ur_HIGH'][0]:.3f} +- {lam['ur_HIGH'][1]:.3f}, LOW {lam['ur_LOW'][0]:.3f} +- {lam['ur_LOW'][1]:.3f}; "
  f"diff Z {(lam['ur_HIGH'][0] - lam['ur_LOW'][0]) / sdl:+.2f}")

P("\n--- observed contrasts D = eps(HIGH) - eps(LOW) of each partial property (K9 primary; error = CFG531 rule)")
OBS = {}
for k in K.KPROPS:
    OBS[k] = contrast(*MASK[k])
    P(f"  {k:6s} " + "  ".join(f"[{c} {f[:3]}] {OBS[k][(c, f, 'K9')]['D']:+.3f}+-{OBS[k][(c, f, 'K9')]['sig']:.3f} (Z {OBS[k][(c, f, 'K9')]['Z']:+.2f})" for c, f in CELLS)
      + f"   T(K9) {Tstat(OBS[k]):+.2f}  T(K-in) {Tstat(OBS[k], 'K-in'):+.2f}")
P(f"  ({time.time() - t0:.0f} s)")

# variant: u-r partialled only on M*, z, env
Dm = [(qid[E2] == q).astype(float) for q in range(5)] + [LM[E2], raw["z"][E2], raw["env"][E2]]
X = np.column_stack(Dm); y = raw["ur"][E2]; v = np.full(len(LM), np.nan); v[E2] = y - X @ np.linalg.lstsq(X, y, rcond=None)[0]
VARI = contrast(*tert(v, E2))
P("  (reported) u-r partialled on M*, z, env only: " + "  ".join(f"[{c} {f[:3]}] {VARI[(c, f, 'K9')]['D']:+.3f} (Z {VARI[(c, f, 'K9')]['Z']:+.2f})" for c, f in CELLS))
# known-signal recovery: raw M* tertiles
KS = contrast(*tert(LM, E2))
P("  MUTATE known signal, raw log M* tertiles: " + "  ".join(f"[{c} {f[:3]}] {KS[(c, f, 'K9')]['D']:+.3f} (Z {KS[(c, f, 'K9')]['Z']:+.2f})" for c, f in CELLS))
check(all(KS[(c, f, "K9")]["D"] > 0 and KS[(c, f, "K9")]["Z"] >= 2 for c, f in CELLS), "MUTATE known-signal recovery: M* tertiles D > 0 with Z >= 2 in all four cells")

# ---------------- joint-permutation null
P(f"\n--- null: {NNULL} joint permutations of the partial-property block within log M* quintiles")
rng = np.random.default_rng(SEED)
idxE = np.where(E2)[0]
NULL = {k: {"K9": [], "K-in": []} for k in K.KPROPS}
NULLZ = []
for i in range(NNULL):
    perm = idxE.copy()
    for q in range(5):
        m = np.where(qid[idxE] == q)[0]; perm[m] = idxE[m[rng.permutation(len(m))]]
    for k in K.KPROPS:
        vk = np.full(len(LM), np.nan); vk[idxE] = part[k][perm]
        r = contrast(*tert(vk, E2))
        for bd in ("K9", "K-in"):
            NULL[k][bd].append(Tstat(r, bd))
        NULLZ += [r[(c, f, "K9")]["Z"] for c, f in CELLS]
    if (i + 1) % 20 == 0:
        P(f"  null draw {i + 1}/{NNULL} ({time.time() - t0:.0f} s)")
NT = {k: {bd: np.array(NULL[k][bd]) for bd in NULL[k]} for k in K.KPROPS}
MX = np.max(np.abs(np.array([NT[k]["K9"] for k in K.KPROPS])), axis=0)
zr = float(np.mean(np.abs(np.array(NULLZ)) >= 2))
P(f"  null: rate of |Z| >= 2 per cell (K9) {zr:.3f} (nominal 0.046); max|T| 95th percentile {np.percentile(MX, 95):.2f}")
for k in K.KPROPS:
    P(f"  null T(K9) {k:6s} mean {NT[k]['K9'].mean():+.2f} sd {NT[k]['K9'].std(ddof=1):.2f}")

P("\n--- verdicts (frozen)")
RES = {}
for k in K.KPROPS:
    T = Tstat(OBS[k]); pfw = float((np.sum(MX >= abs(T)) + 1) / (NNULL + 1))
    p1 = float((np.sum(NT[k]["K9"] >= T) + 1) / (NNULL + 1)); zemp = float((T - NT[k]["K9"].mean()) / NT[k]["K9"].std(ddof=1))
    same = len({np.sign(OBS[k][(c, f, "K9")]["D"]) for c, f in CELLS}) == 1
    RES[k] = dict(T=T, p_fw=pfw, p_one_sided_pos=p1, Z_emp=zemp, same_sign=same, T_kin=Tstat(OBS[k], "K-in"),
                  label=("ASSOCIATED" if (pfw < 0.05 and same) else "NOT ASSOCIATED"))
    P(f"  {k:6s} T(K9) {T:+.2f}  Z_emp {zemp:+.2f}  family-wise p {pfw:.3f}  same sign all cells {same}  -> {RES[k]['label']}")
age = RES["ur"]; Dc = {cf: OBS["ur"][(cf[0], cf[1], "K9")]["D"] for cf in CELLS}
if age["p_one_sided_pos"] < 0.05 and all(Dc[cf] > 0 and Dc[cf] >= 0.5 * D585[cf] for cf in CELLS):
    av = "AGE CONFIRMED, " + ("STRENGTHENS" if all(Dc[cf] > D585[cf] for cf in CELLS) else "HOLDS")
elif all(Dc[cf] < 0.5 * D585[cf] for cf in CELLS):
    av = "AGE FADES"
else:
    av = "NOT CONFIRMED"
P(f"\nAGE VERDICT (u-r, all other properties controlled): {av}")
P("  D(K9) partial vs CFG585: " + "  ".join(f"[{c} {f[:3]}] {Dc[(c, f)]:+.3f} vs {D585[(c, f)]:+.3f}" for c, f in CELLS)
  + f"; one-sided empirical p {age['p_one_sided_pos']:.3f}")
P(f"\nchecks: {sum(c for c, _ in CHECKS)}/{len(CHECKS)} pass   ({time.time() - t0:.0f} s)")


def jk(o):
    return {"|".join(kk): vv for kk, vv in o.items()}


json.dump(dict(age_verdict=av, results=RES, observed={k: jk(OBS[k]) for k in K.KPROPS}, variant_ur_mzenv=jk(VARI), known_signal_mstar=jk(KS),
               cfg585_check=jk(r0), lambda_ur={k: v[:2] for k, v in lam.items()}, null_absZ2_rate=zr, null_maxT_95=float(np.percentile(MX, 95)),
               null_T={k: {bd: v.tolist() for bd, v in NT[k].items()} for k in K.KPROPS}, n_analysed=int(E2.sum()), checks=CHECKS),
          open(os.path.join(K.HERE, "cfg631_kids_results.json"), "w"), indent=1, default=float)
open(os.path.join(K.HERE, "cfg631_kids.out"), "w").write("\n".join(OUT) + "\n")
