#!/usr/bin/env python3
"""AS034 supplementary: (a) exact C^2 jump at the splice (regularity class C^1 \\ C^2),
(b) dense argmax of |log10(nu_mono/nu_RAR)| to pin the 0.0104-dex landmark,
(c) h'_RAR > P on (0, y_star) so the max() rule selects RAR exactly below the splice.
Single thread, mpmath 50 dps."""
import json, os, resource, time
t0 = time.monotonic()
os.environ.setdefault("OMP_NUM_THREADS", "1")
import mpmath as mp
mp.mp.dps = 50
DELTA = mp.mpf("0.05")

def h_RAR(y):
    s = mp.sqrt(y); return y / (mp.exp(s) - 1)
def hp_RAR(y):
    s = mp.sqrt(y); e = mp.exp(s)
    return (2 * (e - 1) - s * e) / (2 * (e - 1) ** 2)
def nu_RAR(y):
    s = mp.sqrt(y); return 1 / (1 - mp.exp(-s))

# reload exact landmarks from analysis.json
base = os.path.dirname(os.path.abspath(__file__))
a = json.load(open(os.path.join(base, "raw_outputs", "analysis.json")))
y_p = mp.mpf(a["y_p"]); h_p = mp.mpf(a["h_p"]); y_star = mp.mpf(a["y_star"])
hRAR_ys = mp.mpf(a["h_RAR_y_star"])
P = lambda y: DELTA * h_p / (y + y_p)
def h_mono(y):
    return hRAR_ys + DELTA * h_p * mp.log((y + y_p) / (y_star + y_p))
def nu_mono(y):
    return 1 + h_mono(y) / y

out = {}
# (a) C^2 jump: h''_mono(y+) = -delta h_p/(y+y_p)^2 (exact analytic);
#     h''_RAR(y-) via mp.diff at y_star - 1e-9 (finite offset, 50-digit diff)
hpp_mono_plus = -DELTA * h_p / (y_star + y_p) ** 2
hpp_RAR = mp.diff(hp_RAR, y_star, 1)          # second derivative at splice
hpp_RAR_side = mp.diff(hp_RAR, y_star - mp.mpf("1e-9"), 1)
out["hpp_mono_at_splice_plus"] = str(hpp_mono_plus)
out["hpp_RAR_at_splice"] = str(hpp_RAR)
out["hpp_RAR_just_below"] = str(hpp_RAR_side)
out["C2_jump_hpp_mono_minus_hpp_RAR"] = str(hpp_mono_plus - hpp_RAR)

# (b) dense dex scan y in [12, 17]
best = (mp.mpf(-1), None)
for i in range(20001):
    yv = mp.mpf("12") + (mp.mpf("17") - mp.mpf("12")) * mp.mpf(i) / 20000
    dd = mp.fabs(mp.log(nu_mono(yv) / nu_RAR(yv)) / mp.log(10))
    if dd > best[0]:
        best = (dd, yv)
out["dex_dense_max"] = str(best[0])
out["dex_dense_argmax_y"] = str(best[1])
out["dex_claim_0_0104_supported"] = best[0] < mp.mpf("0.0104")

# (c) D_alt = h'_RAR - P > 0 on (0, y_star): log grid 1e-10 .. y_star
pts = [mp.mpf(10) ** (-10 + 0.1 * i) for i in range(171)]  # 1e-10..1e6, cut below
vals = []
mn = (mp.mpf("inf"), None)
for yv in pts:
    if yv >= y_star:
        break
    dv = hp_RAR(yv) - P(yv)
    if dv < mn[0]:
        mn = (dv, yv)
    vals.append(float(dv))
out["Dalt_min_over_0_to_ystar_log_grid"] = str(mn[0])
out["Dalt_min_at_y"] = str(mn[1])
out["Dalt_positive_count"] = sum(1 for v in vals if v > 0)
out["Dalt_total_count"] = len(vals)

# linear fine scan just below splice
ylo = y_star * (1 - mp.mpf("1e-3"))
n = 20000
mn2 = (mp.mpf("inf"), None)
for i in range(1, n + 1):
    yv = ylo + (y_star - ylo) * mp.mpf(i) / n
    dv = hp_RAR(yv) - P(yv)
    if dv < mn2[0]:
        mn2 = (dv, yv)
out["Dalt_fine_min_just_below"] = str(mn2[0])
out["Dalt_fine_min_at_y"] = str(mn2[1])

out["bounds"] = {"wall_sec": round(time.monotonic() - t0, 3),
                 "peak_rss_bytes": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}
json.dump(out, open(os.path.join(base, "raw_outputs", "supplementary.json"), "w"), indent=1, default=str)
print(json.dumps(out, indent=1, default=str))
