"""p56: do extreme-TNO orbits (JPL SBDB, a > 150 AU, q > 30 AU, 90 objects) constrain the kernel turn-off y_t (p55)?
Anomalous solar acceleration (toward the Sun) A(r) = (nu_fix(y) - 1) g_N, y = g_N/a0, a0 = 9.3603e-11, nu_fix with k = 2 turn-off; exact law = y_t -> inf.
(V) astrometric visibility over the observed arc T: d = A(r_now) T^2/2 versus 0.1 arcsec at the object's distance (upper bound: an orbit fit absorbs part of it).
(P) secular apsidal precession (Gauss): dw/dt = sqrt(1-e^2)/(n a e) * <A cos f>_t, vs the giant planets' quadrupole
    dw/dt_pl = (3/4) n J2R2/(a^2 (1-e^2)^2) (5 cos^2 i - 1), J2R2 = (1/2) sum m_j a_j^2 / M_sun; compare timescales with 4.5 Gyr.
Galactic external field (~1.8 a0) neglected: g_N >> g_ext inside 2000 AU except near the largest aphelia (noted).
Checks (written before the run): C1 data (90 objects, Sedna a ~ 544); C2 the turn-off (y_t = 128.9) is astrometrically invisible for every object (max d/precision < 1);
C3 report how many objects have turn-off precession faster than the planets' (no pass/fail on the number; the check is that the count is computed for y_t = 100, 128.9, 1000).
Run: python3 p56_etno_turnoff.py | MUTATE=1: the exact law (no turn-off) -- C2 must fail (it is visible, as the planets already show)
"""
import os, sys, json, math
import numpy as np
MUTATE = os.environ.get("MUTATE") == "1"
res = []
def check(n, ok): res.append(bool(ok)); print(("PASS  " if ok else "FAIL  ") + n)
here = os.path.dirname(os.path.abspath(__file__))
d = json.load(open(os.path.join(here, "../../../_external_data/etno_sbdb/etno_a150_q30.json")))
F = d["fields"]; rows = [dict(zip(F, r)) for r in d["data"]]
AU, GM, a0, yr = 1.495978707e11, 1.32712440018e20, 9.3603e-11, 3.15576e7
sed = [r for r in rows if "Sedna" in r["full_name"]][0]
check(f"C1 data: {len(rows)} objects, Sedna a = {sed['a']} AU", len(rows) == 90 and abs(float(sed["a"]) - 543.7) < 5)
def A(r, yt):
    gN = GM / r**2; y = gN / a0
    nu1 = math.sqrt(1 + 1 / y) - 1
    return nu1 * gN / (1 + (y / yt)**2) if yt else nu1 * gN
def r_now(o):
    a, e, M = float(o["a"]) * AU, float(o["e"]), math.radians(float(o["ma"]))
    E = M
    for _ in range(100): E = E - (E - e * math.sin(E) - M) / (1 - e * math.cos(E))
    return a * (1 - e * math.cos(E))
def precess(o, yt):
    a, e, inc = float(o["a"]) * AU, float(o["e"]), math.radians(float(o["i"]))
    n = math.sqrt(GM / a**3)
    Ms = np.linspace(0, 2 * np.pi, 4001)[:-1]; acc = 0.0
    for M in Ms:
        E = M
        for _ in range(60): E = E - (E - e * math.sin(E) - M) / (1 - e * math.cos(E))
        f = 2 * math.atan2(math.sqrt(1 + e) * math.sin(E / 2), math.sqrt(1 - e) * math.cos(E / 2))
        acc += A(a * (1 - e * math.cos(E)), yt) * math.cos(f)
    wdot = math.sqrt(1 - e**2) / (n * a * e) * acc / len(Ms)
    planets = [(1/1047.35, 5.2), (1/3497.9, 9.54), (1/22902.9, 19.19), (1/19412.2, 30.07)]
    J2R2 = 0.5 * sum(m * (aa * AU)**2 for m, aa in planets)
    wpl = 0.75 * n * J2R2 / (a**2 * (1 - e**2)**2) * (5 * math.cos(inc)**2 - 1)
    return wdot, wpl
yt0 = None if MUTATE else 128.915
worst = 0; wname = ""
for o in rows:
    r = r_now(o); T = float(o["data_arc"]) * 86400.0
    disp = 0.5 * A(r, yt0) * T**2; prec = 0.1 / 206265 * r
    if disp / prec > worst: worst, wname, wr = disp / prec, o["full_name"].strip(), r / AU
print(f"   largest astrometric signal / 0.1-arcsec precision = {worst:.3g} ({wname}, now at {wr:.0f} AU)")
check("C2 the turn-off (y_t = 128.9) is astrometrically invisible for all 90 objects (max ratio < 1)" + ("  [MUTATE: exact law]" if MUTATE else ""), worst < 1)
counts = {}
for yt in (100.0, 128.915, 1000.0):
    fast = []; 
    for o in rows:
        w, wp = precess(o, yt)
        if abs(w) > abs(wp): fast.append((o["full_name"].strip(), float(o["a"]), 2 * math.pi / abs(w) / yr / 1e9, 2 * math.pi / abs(wp) / yr / 1e9))
    counts[yt] = fast
    print(f"   y_t = {yt:7.1f}: {len(fast)}/90 objects precess faster from the turn-off than from the giant planets")
for nm, a, tw, tp in sorted(counts[128.915], key=lambda t: -t[1])[:8]:
    print(f"      {nm:32s} a = {a:7.1f} AU: turn-off apsidal period {tw:6.2f} Gyr vs planets {tp:7.2f} Gyr")
w, wp = precess(sed, 128.915); print(f"   Sedna: turn-off {2*math.pi/abs(w)/yr/1e9:.2f} Gyr ({'retro' if w<0 else 'pro'}grade) vs planets {2*math.pi/abs(wp)/yr/1e9:.2f} Gyr")
check("C3 counts computed for y_t = 100, 128.9, 1000", len(counts) == 3)
print(f"\n{sum(res)}/{len(res)} pass" + ("  (MUTATE)" if MUTATE else ""))
sys.exit(0 if all(res) else 1)
