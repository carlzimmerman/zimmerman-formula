"""PA1 A1 shared: catalogue parser (values only, floats and a name pattern; nothing executed) and geometry. kappa = 1/2 FITTED; not theory closed."""
import csv, math, os, re
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); DATA = os.path.join(HERE, "data"); R0 = 8.122
def _f(x):
    try: v = float(x)
    except (TypeError, ValueError): return math.nan
    return v if math.isfinite(v) else math.nan
def load(sample, dmax=3.0):
    """binary: ALOS_PB. all: ALOS_PB if present, else ALOS_PS. returns dict of arrays; order is the file's."""
    rows = list(csv.DictReader(open(os.path.join(DATA, "binary_only.csv" if sample == "binary" else "data.csv"), newline="")))
    out = dict(name=[], l=[], b=[], d=[], derr=[], y=[], e=[], src=[])
    for r in rows:
        nm = (r.get("NAME") or "").strip()
        if not nm: continue  # units row
        if not re.fullmatch(r"[A-Za-z0-9+\-./ ]{1,24}", nm): raise SystemExit("bad name")
        y, e, s = _f(r.get("ALOS_PB")), _f(r.get("ALOS_PB_ERR")), "PB"
        if sample != "binary" and not (y == y and e == e and e > 0): y, e, s = _f(r.get("ALOS_PS")), _f(r.get("ALOS_PS_ERR")), "PS"
        d = _f(r.get("DIST"))
        if not (y == y and e == e and e > 0 and d == d and 0 < d <= dmax): continue
        out["name"].append(nm); out["l"].append(_f(r["GL"])); out["b"].append(_f(r["GB"])); out["d"].append(d); out["derr"].append(_f(r.get("DIST_ERR"))); out["y"].append(y); out["e"].append(e); out["src"].append(s)
    for k in ("l", "b", "d", "derr", "y", "e"): out[k] = np.array(out[k], float)
    return out
def geom(l, b, d, zsun=0.0):
    """Galactocentric: Sun at (-R0, 0, zsun)-side. x toward GC from Sun. returns R, z, n (cyl basis at each point needed by los)."""
    L, B = np.radians(l), np.radians(b)
    n = np.c_[np.cos(B) * np.cos(L), np.cos(B) * np.sin(L), np.sin(B)]     # x to GC, y rotation, z north; origin Sun
    x = -R0 + d * n[:, 0]; y = d * n[:, 1]; z = zsun + d * n[:, 2]; R = np.hypot(x, y)
    return R, z, n, x, y
def alos(aR, az, aRsun, azsun, x, y, n):
    """a_R is the outward cylindrical component at pulsar; aRsun at the Sun, whose outward is -x."""
    ax = aR * x / R_of(x, y); ay = aR * y / R_of(x, y)
    return (ax - (-aRsun)) * n[:, 0] + ay * n[:, 1] + (az - azsun) * n[:, 2]
def R_of(x, y): return np.hypot(x, y)
