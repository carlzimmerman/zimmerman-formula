"""CFG237 attack 2: the power pre-flight recomputed independently (frozen section 5.7), both conventions of the calibration systematic (S_half, S_max),
three combination rules (R-lin, R-quad, R-marg), g_bar-rescale and f_gas sensitivities, post hoc separable band B*.
MUTATE 4: swap flat and rival in the mock truth (the C6 'flat-true mocks centred on 0' line must fail).
MUTATE 6: sigma_int 0.15 -> 0.30 (the statistical-SD line against the README must fail)."""
import sys
from CFG237_common import *

t = start("CFG237_power")
ck = Checks()
R = {}
SIG_INT = 0.30 if MODE == "6" else 0.15
NM = 1000
B_OUT = 0.671; B_IN = 0.213

# ------------------------------------------------------------------ groups
d = load_s1()
P = s1_points(d)
G_S1 = dict(name="S1", z=P["z"], g_st=P["g_st"], g_gas=P["g_gas"], smeas=d.slog_gobs.values)
cr = load_cristal(); det = cr.loc[DETECTED6]
vec = load_vec_outer()


def cristal_group(name, rows):
    Mst = 10 ** det.logMstar.values; f = det.f_molgas.values
    Mg = Mst * f / (1 - f)
    gind = rows["gind"]
    share_st = Mst / (Mst + Mg)
    return dict(name=name, z=rows["z"], g_st=gind * share_st, g_gas=gind * (1 - share_st), smeas=np.full(len(gind), 0.08))


G_RE = cristal_group("CRISTAL_Re", cristal_Re_rows(det))
G_RO = cristal_group("CRISTAL_Rout", cristal_Rout_rows(det, vec, "table_Rout"))
GROUPS = [G_S1, G_RE, G_RO]


def gbar_tau(g, tau):
    return g["g_st"] + g["g_gas"] * 10 ** tau


def true_gobs(g, truth, tau_true=0.0):
    gb = gbar_tau(g, tau_true)
    F = LAWS[truth](g["z"])
    return gb * nu_mono(gb / (A0["canonical"] * F)), gb


def mocks(g, truth, N, rng, tau_true=0.0, sig_int=None, gscale=1.0, fgas_shift=0.0):
    g2 = dict(g)
    tot = g["g_st"] + g["g_gas"]
    if fgas_shift != 0.0:
        f = np.clip(g["g_gas"] / tot + fgas_shift, 0.0, 1.0)
        g2["g_st"] = tot * (1 - f); g2["g_gas"] = tot * f
    g2["g_st"] = g2["g_st"] * gscale; g2["g_gas"] = g2["g_gas"] * gscale
    gobs, gb = true_gobs(g2, truth, tau_true)
    gb0 = gbar_tau(g2, 0.0)
    si = SIG_INT if sig_int is None else sig_int
    sd = np.sqrt(si ** 2 + g["smeas"] ** 2)
    eps = rng.normal(0.0, 1.0, size=(N, len(gb0))) * sd
    lg = np.log10(gobs)[None, :] + eps
    # analysis at tau = 0 (nominal g_bar), law FLAT
    dl = lg - np.log10(gb0 * nu_mono(gb0 / A0["canonical"]))[None, :]
    return np.median(dl, axis=1), g2


def noise_free_delta(g2, truth, tau_an):
    gobs, _ = true_gobs(g2, truth, 0.0)
    gb = gbar_tau(g2, tau_an)
    return float(np.median(np.log10(gobs) - np.log10(gb * nu_mono(gb / A0["canonical"]))))


def analyse(g, seed, N=NM, gscale=1.0, fgas_shift=0.0, B=B_OUT, sig_int=None, swap=False):
    rng = np.random.default_rng(seed)
    out = {}
    tr = {"FLAT": "FLAT", "Hz": "Hz", "PROXY": "PROXY"}
    if swap:
        tr = {"FLAT": "Hz", "Hz": "FLAT", "PROXY": "PROXY"}
    med = {}
    for T in ("FLAT", "Hz", "PROXY"):
        med[T], g2 = mocks(g, tr[T], N, rng, sig_int=sig_int, gscale=gscale, fgas_shift=fgas_shift)
    sd = float(np.std(med["FLAT"], ddof=1))
    sig_H = abs(float(np.median(med["Hz"]))); sig_P = abs(float(np.median(med["PROXY"])))
    # calibration systematic, noise-free, truth FLAT analysis at tau = +-B
    d0 = noise_free_delta(g2, tr["FLAT"], 0.0); dp = noise_free_delta(g2, tr["FLAT"], +B); dm = noise_free_delta(g2, tr["FLAT"], -B)
    S_half = abs(dp - dm) / 2; S_max = max(abs(dp - d0), abs(dm - d0))
    d0H = noise_free_delta(g2, tr["Hz"], 0.0); dpH = noise_free_delta(g2, tr["Hz"], +B); dmH = noise_free_delta(g2, tr["Hz"], -B)
    S_halfH = abs(dpH - dmH) / 2; S_maxH = max(abs(dpH - d0H), abs(dmH - d0H))
    out = dict(sd=sd, sig_H=sig_H, sig_P=sig_P, S_half=S_half, S_max=S_max, S_half_Hz=S_halfH, S_max_Hz=S_maxH, dp=dp, dm=dm, d0=d0,
               medFLAT_mean=float(np.mean(med["FLAT"])), frac_flat_within2sd=float(np.mean(np.abs(med["FLAT"]) < 2 * sd)),
               frac_Hz_within2sd_of_noisefree=float(np.mean(np.abs(med["Hz"] - np.median(med["Hz"])) < 3 * sd)))
    for nm, S in (("half", S_half), ("max", S_max)):
        out[f"lin_H_{nm}"] = bool(sig_H > S + 2 * sd); out[f"lin_P_{nm}"] = bool(sig_P > S + 2 * sd)
        out[f"need_H_{nm}"] = S + 2 * sd; out[f"need_P_{nm}"] = S + 2 * sd
        out[f"quad_H_{nm}"] = bool(sig_H > 2 * math.sqrt(sd ** 2 + (S / math.sqrt(3)) ** 2)); out[f"quad_P_{nm}"] = bool(sig_P > 2 * math.sqrt(sd ** 2 + (S / math.sqrt(3)) ** 2))
    return out


def marg(g, seed, N=20000, B=B_OUT):
    rng = np.random.default_rng(seed)
    res = {}
    # tau_true ~ U(-B, B) per mock: loop in chunks over tau draws (vectorised by binning tau)
    taus = rng.uniform(-B, B, N)
    bins = np.linspace(-B, B, 41); idx = np.digitize(taus, bins) - 1
    for T in ("FLAT", "Hz", "PROXY"):
        m = np.empty(N)
        for b in np.unique(idx):
            sel = np.where(idx == b)[0]
            tm = 0.5 * (bins[b] + bins[min(b + 1, len(bins) - 1)])
            m[sel], _ = mocks(g, T, len(sel), rng, tau_true=tm)
        res[T] = m
    out = {}
    for T in ("Hz", "PROXY"):
        lo_T = np.percentile(res[T], 5); hi_F = np.percentile(res["FLAT"], 95); lo_F = np.percentile(res["FLAT"], 5); hi_T = np.percentile(res[T], 95)
        # separable iff the two distributions separate in either direction
        out[T] = dict(p5_T=float(lo_T), p95_T=float(hi_T), p5_F=float(lo_F), p95_F=float(hi_F), separable=bool(lo_T > hi_F or hi_T < lo_F))
    out["flat_iqr"] = [float(np.percentile(res["FLAT"], 25)), float(np.percentile(res["FLAT"], 75))]
    return out


def bstar(g, seed, which="H", S_key="S_half"):
    """largest B (dex) at which R-lin says separable (bisection on B, noise-free systematic recomputed, mocks fixed)."""
    rng = np.random.default_rng(seed)
    med = {T: mocks(g, T, NM, rng)[0] for T in ("FLAT", "Hz", "PROXY")}
    _, g2 = mocks(g, "FLAT", 2, rng)
    sd = float(np.std(med["FLAT"], ddof=1)); sig = abs(float(np.median(med["Hz" if which == "H" else "PROXY"])))
    def sysB(B):
        d0 = noise_free_delta(g2, "FLAT", 0.0); dp = noise_free_delta(g2, "FLAT", B); dm = noise_free_delta(g2, "FLAT", -B)
        return abs(dp - dm) / 2 if S_key == "S_half" else max(abs(dp - d0), abs(dm - d0))
    if sig <= 2 * sd: return 0.0
    lo, hi = 0.0, 3.0
    if sysB(hi) + 2 * sd < sig: return hi
    for _ in range(60):
        mid = 0.5 * (lo + hi)
        if sysB(mid) + 2 * sd < sig: lo = mid
        else: hi = mid
    return 0.5 * (lo + hi)


# ------------------------------------------------------------------ main block
print(f"sigma_int = {SIG_INT}; mocks per (group, truth) = {NM}; seeds 237 (main), 238 (check), 239 (marginalised, 20,000)")
TARGET = {"S1": dict(sd=0.077, S=0.233, sigH=0.050, sigP=0.022, need=0.388),
          "CRISTAL_Re": dict(sd=0.080, S=0.363, sigH=0.275, sigP=0.209, need=0.523),
          "CRISTAL_Rout": dict(sd=0.077, S=0.324, sigH=0.340, sigP=0.264, need=0.479)}
for g in GROUPS:
    nm = g["name"]
    print(f"\n=== {nm}: n = {len(g['z'])}; gas share of g_bar: {np.round(g['g_gas'] / (g['g_st'] + g['g_gas']), 2)}; g_bar/a0: {np.round((g['g_st'] + g['g_gas']) / A0['canonical'], 1)}")
    a = analyse(g, SEED, swap=(MODE == "4")); b_ = analyse(g, SEED2, swap=(MODE == "4"))
    R[nm] = dict(main=a, check=b_)
    print(f"   seed 237: SD {a['sd']:.4f} | signal H(z) {a['sig_H']:.4f}  proxy {a['sig_P']:.4f} | S_half {a['S_half']:.4f}  S_max {a['S_max']:.4f} (+B {a['dp']:+.3f}, -B {a['dm']:+.3f}, no shift {a['d0']:+.3f})")
    print(f"   seed 238: SD {b_['sd']:.4f} | signal H(z) {b_['sig_H']:.4f}  proxy {b_['sig_P']:.4f}")
    print(f"   (S_half/S_max with truth H(z): {a['S_half_Hz']:.4f} / {a['S_max_Hz']:.4f})")
    for key in ("half", "max"):
        print(f"   R-lin [{key}]: needs > {a['need_H_' + key]:.3f}; vs H(z): {'POSSIBLE' if a['lin_H_' + key] else 'NOT possible'}; vs proxy: {'POSSIBLE' if a['lin_P_' + key] else 'NOT possible'}   | R-quad: H(z) {'POSSIBLE' if a['quad_H_' + key] else 'NOT possible'}, proxy {'POSSIBLE' if a['quad_P_' + key] else 'NOT possible'}")
    mg = marg(g, SEED3)
    R[nm]["marg"] = mg
    print(f"   R-marg (tau_true ~ U(-0.671, 0.671), 20,000 mocks): H(z) separable {mg['Hz']['separable']} (5th pct H(z) {mg['Hz']['p5_T']:+.3f}, 95th pct FLAT {mg['Hz']['p95_F']:+.3f}; FLAT IQR {mg['flat_iqr'][0]:+.3f}..{mg['flat_iqr'][1]:+.3f}); proxy separable {mg['PROXY']['separable']}")
    if MODE not in ("4", "6"):
        tg = TARGET[nm]
        def rel(x, y): return abs(x / y - 1)
        ck.add(f"T {nm} SD within 10% of README {tg['sd']}", rel(a["sd"], tg["sd"]) <= 0.10, f"mine {a['sd']:.4f}")
        ck.add(f"T {nm} signal H(z) within 10% of README {tg['sigH']}", rel(a["sig_H"], tg["sigH"]) <= 0.10, f"mine {a['sig_H']:.4f}")
        ck.add(f"T {nm} signal proxy within 10% of README {tg['sigP']}", rel(a["sig_P"], tg["sigP"]) <= 0.10, f"mine {a['sig_P']:.4f}")
        ok_h = rel(a["S_half"], tg["S"]) <= 0.10; ok_m = rel(a["S_max"], tg["S"]) <= 0.10
        ck.add(f"T {nm} calibration systematic within 10% of README {tg['S']} (either convention)", ok_h or ok_m, f"S_half {a['S_half']:.4f} ({'match' if ok_h else 'no'}), S_max {a['S_max']:.4f} ({'match' if ok_m else 'no'})")
        ck.add(f"T {nm} class: NOT possible vs H(z) under R-lin in both conventions", (not a["lin_H_half"]) and (not a["lin_H_max"]))
        ck.add(f"T {nm} needs > README {tg['need']} within 10% (either convention)", rel(a["need_H_half"], tg["need"]) <= 0.10 or rel(a["need_H_max"], tg["need"]) <= 0.10, f"half {a['need_H_half']:.3f} max {a['need_H_max']:.3f}")
    # C6 planted-law recovery: true-law median within 2 SD of 0 in >= 90%; other law offset matches noise-free within 3 SD
    ok6 = a["frac_flat_within2sd"] >= 0.90
    tag = "M4 " if MODE == "4" else ""
    ck.add(f"{tag}C6 {nm}: flat-true mocks centred on 0 (|median| < 2 SD in >= 90%)", ok6, f"{a['frac_flat_within2sd']:.3f}")
    ck.add(f"{tag}C6 {nm}: H(z)-true median within 3 SD of its noise-free value in >= 90%", a["frac_Hz_within2sd_of_noisefree"] >= 0.90, f"{a['frac_Hz_within2sd_of_noisefree']:.3f}")
    if MODE == "6":
        tg = TARGET[nm]
        ck.add(f"M6 {nm}: statistical SD within 10% of README {tg['sd']}", abs(a["sd"] / tg["sd"] - 1) <= 0.10, f"mine {a['sd']:.4f} (sigma_int 0.30)")

if MODE in ("4", "6"):
    pass
else:
    # sensitivities (declared): g_bar rescale and f_gas +-0.2 for S1; also B*
    print("\n=== sensitivity: S1 g_bar rescaled (so D rises) ===")
    sens = {}
    for gs in (1.0, 0.75, 0.5, 0.3):
        a = analyse(G_S1, SEED, N=NM, gscale=gs)
        sens[gs] = a
        print(f"   s_gb {gs}: signal H(z) {a['sig_H']:.3f} proxy {a['sig_P']:.3f} | SD {a['sd']:.3f} | S_half {a['S_half']:.3f} S_max {a['S_max']:.3f} | R-lin needs {a['need_H_half']:.3f} / {a['need_H_max']:.3f}: {'POSSIBLE' if (a['lin_H_half'] or a['lin_H_max']) else 'NOT possible'} (half:{a['lin_H_half']}, max:{a['lin_H_max']})")
    R["S1_gscale"] = sens
    print("\n=== sensitivity: S1 f_gas +-0.2 ===")
    for fs_ in (-0.2, 0.2):
        a = analyse(G_S1, SEED, N=NM, fgas_shift=fs_)
        print(f"   f_gas {fs_:+.1f}: signal H(z) {a['sig_H']:.3f} | S_half {a['S_half']:.3f} S_max {a['S_max']:.3f} | R-lin half:{a['lin_H_half']} max:{a['lin_H_max']}")
    print("\n=== post hoc separable band B* (R-lin, vs H(z) and vs proxy) ===")
    TB = {"S1": (None, None), "CRISTAL_Re": (0.27, 0.13), "CRISTAL_Rout": (0.44, 0.28)}
    R["Bstar"] = {}
    for g in GROUPS:
        row = {}
        for wh in ("H", "P"):
            for sk in ("S_half", "S_max"):
                row[f"{wh}_{sk}"] = bstar(g, SEED, wh, sk)
        R["Bstar"][g["name"]] = row
        print(f"   {g['name']}: B*(H(z)) half {row['H_S_half']:.3f}, max {row['H_S_max']:.3f} | B*(proxy) half {row['P_S_half']:.3f}, max {row['P_S_max']:.3f}   README: H(z) {TB[g['name']][0]}, proxy {TB[g['name']][1]}")
        if TB[g["name"]][0] is not None:
            tH, tP = TB[g["name"]]
            okH = any(abs(row[k] / tH - 1) <= 0.10 for k in ("H_S_half", "H_S_max")); okP = any(abs(row[k] / tP - 1) <= 0.10 for k in ("P_S_half", "P_S_max"))
            ck.add(f"T {g['name']} B*(H(z)) within 10% of README {tH} (either convention)", okH)
            ck.add(f"T {g['name']} B*(proxy) within 10% of README {tP} (either convention)", okP)
        else:
            ck.add("T S1 'never separable' (B* = 0 against H(z) under both conventions)", row["H_S_half"] == 0.0 and row["H_S_max"] == 0.0, f"{row['H_S_half']:.3f}, {row['H_S_max']:.3f}")

savejson("CFG237_power", R)
nf = ck.n_fail("M" + MODE) if MODE else 0
print(f"\nSUMMARY: {len(ck.rows)} lines, {ck.n_fail()} FAIL ({nf} counted for the exit code)")
for r_ in ck.rows:
    if not r_[1]: print("   FAILED" + (" (expected, kept)" if r_[3] else "") + ":", r_[0], "::", r_[2])
if MODE:
    print("MUTATE", MODE, "bites" if nf > 0 else "DOES NOT BITE"); sys.exit(1 if nf > 0 else 0)
sys.exit(0)
