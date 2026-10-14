"""CFG783 -- cosmologically coupled black holes (k = 3) vs raw GWTC source masses, volume-limited.
Criteria: FROZEN_CRITERIA.md (committed alone first, bc9030977).  Data: _external_data/gwtc_eventapi/gwtc_allevents.json
(GWOSC event API, sha256 9802865c...; not committed).  Run: python3 -I cfg783.py  (CFG783_MUTATE=1: inject k = 3).  Seconds.
kappa = 1/2 FITTED; not theory closed.  This tests the black-hole half of CFG775/779, not the framework's gravity.
"""
import hashlib
import json
import math
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.abspath(os.path.join(HERE, "..", "..", "..", "_external_data", "gwtc_eventapi", "gwtc_allevents.json"))
SHA = "9802865cc8b41508f4073769758f7dbaf5498b22a907849d567083635e7e862a"
MUT = os.environ.get("CFG783_MUTATE") == "1"
OUT = []


def P(s=""):
    print(s, flush=True)
    OUT.append(str(s))


raw = open(DATA, "rb").read()
assert hashlib.sha256(raw).hexdigest() == SHA, "data hash mismatch"
ev = json.loads(raw)["events"]
rows = []
for name, e in ev.items():
    m1, m2, z, dl, snr = (e.get(k) for k in ("mass_1_source", "mass_2_source", "redshift", "luminosity_distance", "network_matched_filter_snr"))
    pa = e.get("p_astro")
    if None in (m1, m2, z, dl, snr):
        continue
    if pa is not None and pa < 0.5:
        continue
    if m1 < 3 or m2 < 3:
        continue
    rows.append((e.get("commonName", name), float(m1), float(z), float(dl), float(snr)))
# de-duplicate by common name (keep the highest version, i.e. the last listed)
uniq = {}
for r in rows:
    uniq[r[0]] = r
rows = list(uniq.values())
names = [r[0] for r in rows]
m1 = np.array([r[1] for r in rows]); z = np.array([r[2] for r in rows]); dl = np.array([r[3] for r in rows]); snr = np.array([r[4] for r in rows])
P(f"CFG783  GWTC BBH sample: N = {len(rows)} (p_astro >= 0.5 where given, m1, m2 >= 3 Msun, all fields present)" + ("  [MUTATE k = 3]" if MUT else ""))

dh = dl * snr / 8.0
Dcut = float(dl[np.argsort(z)[len(z) // 2]])
keep = (dh >= Dcut) & (dl <= Dcut)
mk, zk = m1[keep].copy(), z[keep]
if MUT:
    zbar = float(np.mean(zk))
    mk = mk * ((1 + zbar) / (1 + zk)) ** 3
P(f"  D_cut = {Dcut:.0f} Mpc (d_L of the median-z event); volume-limited N_kept = {keep.sum()}")


def delta(m, zz, rng=None):
    med = np.median(zz)
    lo, hi = zz <= med, zz > med
    d = np.mean(np.log10(m[hi])) - np.mean(np.log10(m[lo]))
    lev = math.log10((1 + np.mean(zz[hi])) / (1 + np.mean(zz[lo])))
    return d, lev, float(np.mean(zz[lo])), float(np.mean(zz[hi]))


d, lev, zl, zh = delta(mk, zk)
rng = np.random.default_rng(783)
bs = []
for _ in range(10000):
    i = rng.integers(0, len(mk), len(mk))
    try:
        bs.append(delta(mk[i], zk[i])[0])
    except Exception:
        pass
bs = np.array(bs)
lo, hi = np.percentile(bs, [16, 84])
sig = (hi - lo) / 2
dk3 = -3 * lev
khat = -d / lev
P(f"  bins: mean z low {zl:.3f}, high {zh:.3f}; Delta = mean log10 m1 (high - low) = {d:+.3f} [{lo:+.3f}, {hi:+.3f}] (sigma {sig:.3f})")
P(f"  predictions: k = 0 -> 0;  k = 3 -> {dk3:+.3f};  k_hat = {khat:+.2f} +- {sig / lev:.2f}")
d_raw = delta(m1, z)[0]
P(f"  K1 selection tooth: all events (no volume cut) Delta_raw = {d_raw:+.3f}  (selection pushes this positive)")
k2 = keep.sum() >= 20 and sig < abs(dk3) / 2
P(f"  K2 power: N_kept {keep.sum()} >= 20 and sigma {sig:.3f} < |Delta_k3|/2 = {abs(dk3) / 2:.3f}: {k2}")
if not k2:
    cls = "NOT DIAGNOSTIC (power)"
else:
    c3 = (d - dk3) / sig >= 3
    c0 = abs(d) / sig >= 3
    cls = ("k = 3 EXCLUDED" if c3 else "") + ("; " if c3 and c0 else "") + ("k = 0 EXCLUDED" if c0 else "")
    cls = cls or "NOT DIAGNOSTIC (neither excluded at 3 sigma)"
P(f"  CLASS: {cls}")
res = dict(N=len(rows), N_kept=int(keep.sum()), D_cut=Dcut, delta=d, ci=[float(lo), float(hi)], sigma=float(sig), delta_k3=dk3,
           k_hat=khat, k_hat_sigma=float(sig / lev), delta_raw=float(d_raw), z_lo=zl, z_hi=zh, K2=bool(k2), cls=cls, mutate=MUT,
           kept=[n for n, k in zip(names, keep) if k])
json.dump(res, open(os.path.join(HERE, f"cfg783_results{'_MUTATE' if MUT else ''}.json"), "w"), indent=1)
open(os.path.join(HERE, f"cfg783{'_MUTATE' if MUT else ''}.out"), "w").write("\n".join(OUT) + "\n")
if MUT:
    base = json.load(open(os.path.join(HERE, "cfg783_results.json")))["k_hat"]
    ok = abs((khat - base) - 3) <= max(2 * sig / lev, 0.5)
    print(f"MUTATE: injected k = 3 shifts k_hat by {khat - base:+.2f} (expected +3): {'bites' if ok else 'DID NOT BITE'}")
    sys.exit(1)
