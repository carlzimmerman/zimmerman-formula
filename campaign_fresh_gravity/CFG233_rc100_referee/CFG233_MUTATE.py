"""CFG233 MUTATE controls M1..M7 (env MUTATE=k). Exit 1 when the control bites, 0 when it fails to bite."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from CFG233_common import *

k = int(os.environ.get("MUTATE", "1"))
t = start(f"CFG233_MUTATE_{k}")
B = 10000
d = load_rc100(); z = d["z"]; n = len(z); zmed = np.median(z)
zmax, zmin = z.max(), z.min()


def primary(zz, D, gb, zlaw=None, laws=("flat", "rival"), zreg=None):
    zl = zz if zlaw is None else zlaw
    zr = zz if zreg is None else zreg
    a = delta_of(D, gb, zl, laws[0]); b = delta_of(D, gb, zl, laws[1])
    bs = boot_ts(zr, [a, b], B, SEED_MAIN)
    sl = (ts(zr, a), ts(zr, b)); cf, cr = ci(bs[0]), ci(bs[1])
    return dict(slope_flat=sl[0], ci_flat=cf, slope_rival=sl[1], ci_rival=cr, cls=classify(cf, cr), sd=list(bs.std(1)))


base = primary(z, d["D"], d["gbar"])
print("base (unmutated):", base["slope_flat"], base["ci_flat"], base["slope_rival"], base["ci_rival"], base["cls"])
res = dict(base=base, mode=k)
bites = False
if k == 1:
    D = d["D"] * 10 ** (0.2 * (z - zmed))
    gb = d["gbar"]  # D_obs multiplied only (frozen text)
    m = primary(z, D, gb)
    ds_f = m["slope_flat"] - base["slope_flat"]; ds_r = m["slope_rival"] - base["slope_rival"]
    print(f"M1 inject D x 10^(0.2(z-zmed)): flat slope shift {ds_f:+.4f}, rival {ds_r:+.4f} (injection 0.2 exact; nu(g_bar) unchanged => expect 0.200 exactly) class {m['cls']}")
    bites = ds_f >= 0.19 and m["cls"] != "W-flat"
    res["mut"] = m; res["shift"] = (ds_f, ds_r)
elif k == 2:
    rng = np.random.default_rng(233)
    zs = rng.permutation(z)
    m = primary(z, d["D"], d["gbar"], zlaw=zs, zreg=zs)  # E(z) and the regression both at shuffled z
    print("M2 shuffle z:", m)
    inside = abs(m["slope_flat"]) < 2 * m["sd"][0] and abs(m["slope_rival"]) < 2 * m["sd"][1]
    bites = not (m["ci_rival"][1] < 0) and m["cls"] == "W-none"
    print("both slopes within 2 sd of 0:", inside, "; class", m["cls"])
    print("M2 note (kept): the frozen expectation was wrong. The rival's delta contains the mechanical term -0.5 log E(z) evaluated at whatever z is used for a0(z); shuffling z in both places leaves it (flat-true expectation -0.060).")
    m2 = primary(z, d["D"], d["gbar"], zlaw=z, zreg=zs)  # POST-HOC M2b (not frozen): shuffle the regression axis only
    print("M2b post-hoc (regression axis shuffled, a0(z) at true z):", {kk: m2[kk] for kk in ("slope_flat", "slope_rival", "cls")})
    res["mut"] = m; res["m2b_posthoc"] = m2
elif k == 3:
    m = primary(z, d["D"], d["gbar"], laws=("rival", "flat"))  # 'flat' := a0 E(z), 'rival' := constant a0
    print("M3 swap laws: reported-flat slope (= true rival) and reported-rival slope (= true flat):", m)
    bites = m["cls"] != "W-flat" and m["slope_flat"] < -0.07
    res["mut"] = m
elif k == 4:
    m41, *_ = rc41_match(d)
    s = sub(d, ~m41)
    m = primary(s["z"], s["D"], s["gbar"])
    print("M4 remove RC41 (n=%d):" % (~m41).sum(), m)
    bites = m["ci_flat"][1] < 0 and m["cls"] == "W-mixed"
    res["mut"] = m
elif k == 5:
    zm = zmax + zmin - z
    m = primary(z, d["D"], d["gbar"], zreg=zm)
    print("M5 mirror z (regression axis only):", m)
    a = ts_batch(z[None], delta_of(d["D"], d["gbar"], z, "flat")[None])[0]
    b = ts_batch(zm[None], delta_of(d["D"], d["gbar"], z, "flat")[None])[0]
    print("antisymmetry residual |slope + slope_mirror|:", abs(a + b))
    bites = abs(a + b) < 1e-12 and m["cls"] != "W-flat" and m["slope_rival"] > 0
    res["mut"] = m; res["antisym"] = abs(a + b)
elif k == 6:
    tau = 0.15
    kfac = 10 ** (tau * (z - zmed))          # assumed/true baryon mass  (g_bar' = g_bar / k)
    gb = d["gbar"] / kfac
    f2 = 1 - (1 - d["f"]) / kfac
    ok = (f2 > 0) & (f2 < 1)
    print("M6: rows with f' outside (0,1):", int((~ok).sum()))
    m = primary(z[ok], 1 / (1 - f2[ok]), gb[ok])
    # s_bar: sample mean of s = -dlognu/dlogy at flat law
    y = gb[ok] / A0["canonical"]; h = 1e-4
    s_loc = -(np.log10(nu_mono(y * 10 ** h)) - np.log10(nu_mono(y * 10 ** -h))) / (2 * h)
    sbar = float(s_loc.mean())
    pred = -(1 - sbar) * tau
    shift = m["slope_flat"] - base["slope_flat"]
    print(f"M6 gas/M_bar tilt tau={tau}: flat slope shift {shift:+.4f}; hand algebra -(1-s_bar)tau = {pred:+.4f} (s_bar {sbar:.3f}); class {m['cls']}")
    print(f"M6 note (kept): the frozen prediction had the wrong SIGN. Algebra: g_bar' = g_bar 10^(-tau dz) at fixed V_c raises D by 10^(tau dz), nu by 10^(s tau dz): delta shifts by +(1-s) tau = {-pred:+.4f}. Observed {shift:+.4f} (10 rows dropped for f' outside (0,1)); magnitude within {abs(abs(shift)-abs(pred))/abs(pred):.2f} of the algebra.")
    bites = abs(shift - pred) < 0.3 * abs(pred) and m["cls"] != "W-flat"  # frozen line as written (sign-wrong)
    res["mut"] = m; res["shift"] = shift; res["pred"] = pred
elif k == 7:
    gg = freeman_gbar(d["logM"], d["Re"])
    m = primary(z, d["D"], gg)  # D from f_DM, g_bar from the table M_bar thin disc (non-physical pairing)
    print("M7 mixed pairing:", m)
    dif = abs(m["slope_flat"] - base["slope_flat"])
    print("difference of flat slope from primary:", dif)
    bites = dif > 0.03
    res["mut"] = m; res["diff"] = dif
res["bites"] = bool(bites)
print(f"MUTATE {k}: control {'BITES' if bites else 'DOES NOT BITE (kept)'} -> exit {1 if bites else 0}")
savejson(f"CFG233_MUTATE_{k}", res)
sys.exit(1 if bites else 0)
