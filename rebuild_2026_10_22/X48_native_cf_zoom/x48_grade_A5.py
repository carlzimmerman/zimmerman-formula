#!/usr/bin/env python3
"""X48 AMENDMENT A5 grade (10^12 only): nine-seed ng 80 median against the window [3.3, 4.6] and against A3's ng 64 median
(CONVERGED if within 20 %); per-seed r_-2 / r_conv and r_-2 / (3 eps) at both ng; [eps-LIMITED] if most ng 80 seeds have
r_-2 <= 2 x 3 eps; bootstrap 68 % (10 000, seed 20261026); NFW-fit median. Criteria a0cbcc6928.
    python3 x48_grade_A5.py              # A5: ng 80 (tag A5) vs ng 64 (tag A3)
    X48A5_K1=1 python3 x48_grade_A5.py   # K1: ng 64 (A3) vs ng 48 (A2) must reproduce x48_grade_A3.json; writes nothing else"""
import json, os, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
K1 = os.environ.get("X48A5_K1") == "1"
HI, LO = ((64, "ng64_A3"), (48, "ng48_A2")) if K1 else ((80, "ng80_A5"), (64, "ng64_A3"))
RH = json.load(open(os.path.join(HERE, f"x48_analyze_results_{HI[1]}.json")))["runs"]
RL = json.load(open(os.path.join(HERE, f"x48_analyze_results_{LO[1]}.json")))["runs"]
W = (3.3, 4.6)
def rows(R, ng): return {o["seed"]: o for k, o in R.items() if o.get("flag") == "ok" and o.get("ng") == ng and abs(o["M"] / 1e12 - 1) < 1e-6}
def eps(seed, ng):
    z = np.load(os.path.join(HERE, "runs", f"M1e12_s{seed}_ng{ng}", "snap_zf.npz"), allow_pickle=True)
    return float(json.loads(str(z["meta"]))["eps"])
a, b = rows(RH, HI[0]), rows(RL, LO[0])
rng = np.random.default_rng(20261026)
def stats(d):
    cf = np.array([d[s]["cf"] for s in sorted(d)]); bs = np.median(cf[rng.integers(0, len(cf), (10000, len(cf)))], axis=1)
    return float(np.median(cf)), [float(x) for x in np.percentile(bs, [16, 84])], float(np.median([d[s]["c_nfw_fit"] for s in d]))
mh, bh, nh = stats(a); ml, bl, nl = stats(b)
win = "IN WINDOW" if W[0] <= mh <= W[1] else ("ABOVE WINDOW" if mh > W[1] else "BELOW WINDOW")
sh = mh / ml - 1; res = "CONVERGED" if abs(sh) <= 0.20 else f"RESOLUTION-DEPENDENT ({'falls' if sh < 0 else 'rises'})"
if K1:
    G = json.load(open(os.path.join(HERE, "x48_grade_A3.json")))
    d = max(abs(mh - G["ng64"]["median"]), abs(ml - G["ng48"]["median"]), *(abs(x - y) for x, y in zip(bh, G["ng64"]["boot68"])))
    ok = d == 0.0 and res == G["resolution"] and win == G["window_label"]
    print(f"X48 A5 K1 (grade script on ng 64 vs ng 48 reproduces x48_grade_A3.json): max |d| {d:.1e}, labels {win} / {res}: {'PASS' if ok else 'FAIL'}")
    sys.exit(0 if ok else 1)
OUT = [f"X48 A5 grade (10^12; ng {HI[0]} vs ng {LO[0]}; eps unchanged; convergence beyond ng {HI[0]} not tested); kappa = 1/2 FITTED; not theory closed"]
OUT.append(f"  ng {HI[0]}: {len(a)} seeds; median c_f {mh:.2f} (68 % {bh[0]:.2f}-{bh[1]:.2f}); NFW-fit median {nh:.2f}")
OUT.append(f"  ng {LO[0]}: {len(b)} seeds; median c_f {ml:.2f} (68 % {bl[0]:.2f}-{bl[1]:.2f}); NFW-fit median {nl:.2f}")
per = {}
for s in sorted(set(a) | set(b)):
    p = {}
    for tag, d_, ng in (("lo", b, LO[0]), ("hi", a, HI[0])):
        if s in d_:
            e3 = 3 * eps(s, ng)
            p.update({f"cf_{tag}": d_[s]["cf"], f"q_conv_{tag}": d_[s]["rm2"] / d_[s]["rconv"], f"q_3eps_{tag}": d_[s]["rm2"] / e3, f"rconv_{tag}": d_[s]["rconv"], f"3eps_{tag}": e3})
    per[s] = p
    OUT.append(f"    seed {s}: " + "; ".join(f"{k} {v:.4g}" for k, v in p.items()))
lim = [s for s in a if per[s]["q_3eps_hi"] <= 2.0]
epsl = len(lim) > len(a) / 2
OUT.append(f"  WINDOW [3.3, 4.6]: {win};  RESOLUTION: median shift {100 * sh:+.0f} % -> {res}{'  [eps-LIMITED]' if epsl else ''}")
OUT.append(f"  ng {HI[0]} seeds with r_-2 <= 2 x 3 eps: {sorted(lim)} ({len(lim)}/{len(a)})")
OUT.append("  note: the constrained field is drawn on each grid; per-seed shifts mix resolution and realisation.")
print("\n".join(OUT)); open(os.path.join(HERE, "x48_grade_A5.out"), "w").write("\n".join(OUT) + "\n")
json.dump(dict(window=W, hi=dict(ng=HI[0], median=mh, boot68=bh, nfw=nh, n=len(a)), lo=dict(ng=LO[0], median=ml, boot68=bl, nfw=nl, n=len(b)),
               window_label=win, resolution=res, shift=sh, eps_limited=epsl, eps_limited_seeds=sorted(lim), per_seed=per),
          open(os.path.join(HERE, "x48_grade_A5.json"), "w"), indent=1)
