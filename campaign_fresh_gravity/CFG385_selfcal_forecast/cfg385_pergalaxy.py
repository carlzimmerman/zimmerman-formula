"""CFG385 POST-FREEZE (labelled): each galaxy has its OWN free calibration f_j (the realistic case: per-galaxy gas/M* errors).
Per galaxy: n points log-uniform in y over its own span; a0 is shared. Joint Fisher over (f_1..f_G, a0) -> sigma(log a0)."""
import math, json, os, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
def b(k, y):
    y = np.asarray(y, float)
    return 1/(2*(1+y)) if k == "P2" else np.sqrt(y)/(2*np.expm1(np.sqrt(y)))
def sig(k, G, n, ymin, ymax, s):
    y = np.logspace(math.log10(ymin), math.log10(ymax), n); bb = b(k, y)
    # marginalise each galaxy's f analytically: info on a0 per galaxy = sum b^2 - (sum (1-b) b)^2 / sum (1-b)^2
    I = (np.sum(bb**2) - np.sum((1-bb)*bb)**2/np.sum((1-bb)**2)) / s**2
    return 1/math.sqrt(G*I) if I > 0 else float("inf")
rows = {}
print("Per-galaxy free calibration: sigma(log a0) [target 0.22 dex = DE law vs rival at 3 sigma]")
for lab, (G, n, ymin, ymax, s) in {
    "KURVS-like: 10 discs x 3 pts, y 0.06-3, 0.1 dex": (10, 3, 0.06, 3.0, 0.1),
    "KURVS-like, 10 discs x 6 pts": (10, 6, 0.06, 3.0, 0.1),
    "RC100-like: 100 discs x 2 pts, y 1.1-4.4": (100, 2, 1.1, 4.4, 0.1),
    "NEEDED z~2.5: 20 discs x 6 pts, y 0.1-5, 0.1 dex": (20, 6, 0.1, 5.0, 0.1),
    "NEEDED z~2.5: 40 discs x 6 pts, y 0.1-5, 0.1 dex": (40, 6, 0.1, 5.0, 0.1),
    "NEEDED z~2.5: 20 discs x 6 pts, y 0.3-10, 0.1 dex": (20, 6, 0.3, 10.0, 0.1),
}.items():
    v = {k: sig(k, G, n, ymin, ymax, s) for k in ("P2", "expRAR")}
    rows[lab] = v
    print(f"  {lab}: P2 {v['P2']:.3f}  expRAR {v['expRAR']:.3f}  -> {'DECIDES' if max(v.values()) <= 0.22 else 'does NOT decide'}")
json.dump(rows, open(os.path.join(HERE, "cfg385_pergalaxy_results.json"), "w"), indent=1)
