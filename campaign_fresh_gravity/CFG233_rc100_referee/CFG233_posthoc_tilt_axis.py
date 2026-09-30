"""CFG233 POST-HOC (written after the CFG217 disclosure and the calc chat's follow-up; reported only, nothing frozen changes):
a pure baryon-mass TILT of total size T dex between z = 0.6 and z = 2.5 on two axes (linear in z = my original definition; linear in log10(1+z) = the calc chat's),
in two row-handling variants: (A) my original (rows with f' outside (0,1) excluded), (B) no exclusion (D' = g_obs / g_bar', a pure tilt of g_bar at fixed V_c).
Sign convention: T is the CHANGE of the baryon mass between z = 0.6 and 2.5 applied to the table: g_bar' = g_bar * 10^(T p(z)), p(0.6) = -pivot..., p(2.5)-p(0.6) = 1.
T < 0 lowers the baryons at high z (raises delta at high z): the direction that helps the rival (calc chat's negative dex). T > 0 is the opposite direction.
A constant offset does not change a Theil-Sen slope, so the pivot is irrelevant to the slopes (the pivot is z = median z).
sd = bootstrap SD over galaxies of the tilted sample's slope (N = 10000, seed 233), the same construction as the main run."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from CFG233_common import *

start("CFG233_posthoc_tilt_axis")
d = load_rc100(); z = d["z"]; n = len(z); zmed = float(np.median(z))
ZLO, ZHI = 0.6, 2.5
B = 10000
ex = expected_slopes(d["gobs"], z)
sR, mF = ex["rival"][0], ex["flat"][1]
print(f"sample z {z.min():.2f}-{z.max():.2f}, median {zmed:.2f}; expected slopes on the full sample: rival-true delta_flat {sR:+.4f}, flat-true delta_rival {mF:+.4f}")
print("axes: 'linear' p(z) = (z - zmed)/(2.5 - 0.6);  'log10(1+z)' p(z) = (log10(1+z) - log10(1+zmed))/(log10(3.5) - log10(1.6)).  T = total change of the baryon mass between z=0.6 and z=2.5 in dex.")
print("my ORIGINAL scan (attack a) used the linear axis with the total taken over the sample's z range (1.91 wide, 0.61-2.52), variant A, sd from B=2000.")
def prof(axis):
    if axis == "linear":
        return (z - zmed) / (ZHI - ZLO)
    x = np.log10(1 + z); return (x - np.log10(1 + zmed)) / (np.log10(1 + ZHI) - np.log10(1 + ZLO))
def run(T, axis, variant, Bn=B, seed=SEED_MAIN):
    kf = 10 ** (T * prof(axis))                 # g_bar' = g_bar * kf
    gb = d["gbar"] * kf
    D = d["gobs"] / gb
    f2 = 1 - gb / d["gobs"]
    m = np.ones(n, bool) if variant == "B" else ((f2 > 0) & (f2 < 1))
    zz = z[m]
    fl, rv = delta_pair(D[m], gb[m], zz)
    o = dict(T=T, axis=axis, variant=variant, n=int(m.sum()), slope_flat=ts(zz, fl), slope_rival=ts(zz, rv))
    if Bn:
        bs = boot_ts(zz, [fl, rv], Bn, seed)
        o["sd_flat"], o["sd_rival"] = float(bs[0].std()), float(bs[1].std())
        o["ci_flat"], o["ci_rival"] = ci(bs[0]), ci(bs[1]); o["cls"] = classify(o["ci_flat"], o["ci_rival"])
        # tensions: slope minus expectation over sd (expected slopes of the FULL sample, g_obs unchanged)
        o["flat_vs_flat"] = (o["slope_flat"] - 0.0) / o["sd_flat"]
        o["flat_vs_rival"] = (o["slope_flat"] - sR) / o["sd_flat"]
        o["rival_vs_flat"] = (o["slope_rival"] - mF) / o["sd_rival"]
        o["rival_vs_rival"] = (o["slope_rival"] - 0.0) / o["sd_rival"]
    return o
R = dict(expected=(sR, mF))
print("\n=== (b)/(c) zero tilt row (both axes identical): sd = bootstrap SD over galaxies of the observed sample, N = %d resamples, seed 233" % B)
z0 = run(0.0, "linear", "B"); R["zero"] = z0
print(f"  flat slope {z0['slope_flat']:+.4f} sd {z0['sd_flat']:.4f}; rival slope {z0['slope_rival']:+.4f} sd {z0['sd_rival']:.4f}")
print("\n=== (d) table. columns: axis | variant | T | n | flat slope, sd | rival slope, sd | tensions: flat-slope vs flat / vs rival ; rival-slope vs flat / vs rival | class")
rows = []
for axis in ("log10(1+z)", "linear"):
    ax = "linear" if axis == "linear" else "log"
    for variant in ("B", "A"):
        for T in (-0.10, -0.15, -0.20, -0.25, -0.30, -0.35):
            o = run(T, "linear" if axis == "linear" else "log", variant); rows.append(o)
            print(f"  {axis:10} | {variant} | {T:+.2f} | n={o['n']:3d} | flat {o['slope_flat']:+.4f} (sd {o['sd_flat']:.4f}) | rival {o['slope_rival']:+.4f} (sd {o['sd_rival']:.4f}) | flat: {o['flat_vs_flat']:+.2f} / {o['flat_vs_rival']:+.2f} ; rival: {o['rival_vs_flat']:+.2f} / {o['rival_vs_rival']:+.2f} | {o['cls']}")
R["rows"] = rows
print("\n  opposite sign (T > 0: baryons raised at high z; the direction AGAINST the rival), calc-chat axis, variant B:")
opp = []
for T in (0.10, 0.20, 0.30):
    o = run(T, "log", "B"); opp.append(o)
    print(f"  log10(1+z) | B | {T:+.2f} | flat {o['slope_flat']:+.4f} (sd {o['sd_flat']:.4f}) | rival {o['slope_rival']:+.4f} | flat: {o['flat_vs_flat']:+.2f} / {o['flat_vs_rival']:+.2f}")
R["opposite"] = opp
print("\n=== (e) total tilt at which the flat slope reaches 3.6 sigma from flat's expectation (0): bisection on the point slope = 3.6 x sd, sd from the zero-tilt row (%.4f); then the tension is re-evaluated with the sd re-bootstrapped at that tilt" % z0["sd_flat"])
sol = {}
for axis in ("log", "linear"):
    for variant in ("B", "A"):
        lo, hi = 0.0, -0.8
        f = lambda T: run(T, axis, variant, Bn=0)["slope_flat"] - 3.6 * z0["sd_flat"]
        if f(hi) * f(lo) > 0:
            sol[f"{axis}/{variant}"] = None; print(f"  {axis}/{variant}: no root in [-0.8, 0]"); continue
        for _ in range(40):
            mid = 0.5 * (lo + hi)
            if f(mid) * f(lo) <= 0: hi = mid
            else: lo = mid
        Tm = 0.5 * (lo + hi); chk = run(Tm, axis, variant)
        sol[f"{axis}/{variant}"] = dict(T=Tm, n=chk["n"], tension_own_sd=chk["flat_vs_flat"], sd=chk["sd_flat"], slope=chk["slope_flat"])
        print(f"  axis {axis:6} variant {variant}: T = {Tm:+.4f} dex (n = {chk['n']}); slope {chk['slope_flat']:+.4f}, own sd {chk['sd_flat']:.4f} -> tension {chk['flat_vs_flat']:+.2f}")
R["solutions_3p6"] = sol
# my ORIGINAL definition reproduced: linear axis with total over the sample's z range 1.91
print("\n=== my ORIGINAL scan rows reproduced with this script (linear axis, total over 1.91 = the sample's range, variant A, B=%d): total -> flat slope, flat-vs-flat tension" % B)
orig = []
for tot in (0.10, 0.15, 0.20, 0.25, 0.26, 0.30, 0.35):
    tau = tot / (z.max() - z.min())
    kf = 10 ** (-tau * (z - zmed)); gb = d["gbar"] * kf; D = d["gobs"] / gb; f2 = 1 - gb / d["gobs"]; m = (f2 > 0) & (f2 < 1)
    fl, rv = delta_pair(D[m], gb[m], z[m]); bs = boot_ts(z[m], [fl], B, SEED_MAIN)
    o = dict(total=tot, n=int(m.sum()), slope=ts(z[m], fl), sd=float(bs[0].std())); o["tension"] = o["slope"] / o["sd"]; orig.append(o)
    print(f"  {tot:.2f}: n={o['n']} flat {o['slope']:+.4f} sd {o['sd']:.4f} tension {o['tension']:+.2f}")
R["original_reproduced"] = orig
savejson("CFG233_posthoc_tilt_axis", R)
