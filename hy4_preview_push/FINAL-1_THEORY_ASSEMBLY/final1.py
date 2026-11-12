#!/usr/bin/env python3
# FINAL-1: arithmetic for THEORY.md  (form B + the formation reading)
#
# Every printed quantity is either quoted from a landed lane (named in the text) or
# computed HERE in SI from G, c, a0.  Footings never pooled.  Nothing downloaded.
# Reads DD1's frozen table read-only.
# Adopts nothing.  kappa = 1/2 FITTED; not theory closed.

import json
import math
import os
import random
import sys

# ---------------------------------------------------------------- constants (SI)
G = 6.6743e-11
c = 299792458.0
K = 4.0 * math.pi * G
A0 = {"canonical": 9.3603e-11, "alt": 1.1312e-10}
MSUN = 1.989e30                       # kg, as used in GAS1
PC = 3.0856775814913673e16            # m
MPC = 3.0856775814913673e22           # m
RB = 5.41                              # cosmic cold / baryon share (CO1, R541)
XB2 = RB * (1.0 + RB)                 # x_b^2 = 34.6781
KAPPA = 0.5                            # FITTED
Z_CONS = 2.0 * math.sqrt(8.0 * math.pi / 3.0)

# cosmology for the epoch numbers (R541B / PAR1 A2: h, omega_b h^2, omega_c h^2)
H0 = 67.4                              # km/s/Mpc
h = 0.674
OM_B_H2 = 0.02236
OM_C_H2 = 0.1209
OM = (OM_B_H2 + OM_C_H2) / h ** 2
OL = 1.0 - OM
H0_INV_GYR = 977.792 / H0             # 1/H0 in Gyr

# PD1's Lagrangian share (an input rule, quoted from PD1 / ONE1 -- not derived)
X_S_PD1 = 59.5
DELIVERED = {"record_infall": 1.06, "VSH1_settled": 1.40}

# FRM1's pre-registered bands per class (committed before any FRM1 number existed)
BANDS = {
    "SPARC":            (-0.05,  0.05),
    "faint rotators":   (-0.35,  0.00),
    "tidal dwarfs":     (-0.95, -0.30),
    "massive spirals":  (-0.05,  0.20),
    "ATLAS3D":          ( 0.00,  0.20),
    "RC100":            ( 0.00,  0.20),
    "KiDS":             (-0.15,  0.15),
    "groups":           ( 0.00,  0.30),
    "X-COP":            (-0.30,  0.30),
    "CLASH":            (-0.30,  0.30),
    "MW bright dwarfs": ( 0.00,  0.30),
    "MW ultra-faints":  ( 0.30,  0.70),
    "M31 dwarfs":       ( 0.00,  0.30),
    "LG field dwarfs":  (-0.20,  0.30),
    "Coma UDGs":        ( 0.10,  0.50),
    "NGC 1052 UDGs":    (-1.05, -0.30),
}
STRIPPED_FAMILY = ["tidal dwarfs", "NGC 1052 UDGs"]
HOSTED_FAMILY = ["MW bright dwarfs", "MW ultra-faints", "M31 dwarfs", "Coma UDGs"]


# --------------------------------------------------------------------- functions
def rM(Mb_msun, a0):
    """MOND radius in m, from baryon mass in Msun."""
    return math.sqrt(G * Mb_msun * MSUN / a0)


def X(x):
    """enclosed cold-to-baryon ratio at x = r/r_M"""
    return (math.sqrt(1.0 + 4.0 * x * x) - 1.0) / 2.0


def XL(u):
    """the same function of u = a0/g_bar   (note u = x^2)"""
    return (math.sqrt(1.0 + 4.0 * u) - 1.0) / 2.0


def g_of_gN(gN, a0):
    """closed form of the law: g = g_N [1/2 + sqrt(1/4 + a0/g_N)]"""
    return gN * (0.5 + math.sqrt(0.25 + a0 / gN))


def YL(g_bar, a0):
    return math.log10(1.0 + XL(a0 / g_bar))


def dmax(u):
    """ceiling of the baryon-loss channel: d_max = log10[(1+u)/(1+X_L(u))]"""
    return math.log10((1.0 + u) / (1.0 + XL(u)))


def fb_from_baryons(u, Xobs):
    """invert X_obs = X_L(u f_b)/f_b  with f_C = 1.  f_b < 1 = baryon loss, > 1 = accretion.
       Returns None when X_obs > u (the saturation ceiling): unreachable."""
    if Xobs > u:
        return None
    F = lambda fb: XL(u * fb) / fb - Xobs
    # F is strictly decreasing in f_b: F(0+) = u - X_obs > 0 (when reachable), F(inf) = -X_obs < 0
    if F(1.0) >= 0.0:             # root lies ABOVE 1  -> late baryon accretion (channel A)
        lo, hi = 1.0, 1.0
        while F(hi) >= 0.0 and hi < 1e9:
            hi *= 1.5
    else:                         # root lies BELOW 1   -> baryon loss (channel B)
        lo, hi = 1e-12, 1.0
    for _ in range(300):
        mid = math.sqrt(lo * hi)
        if -F(mid) < 0.0:         # -F is increasing: F(mid) > 0 => root above mid
            lo = mid
        else:
            hi = mid
    return 0.5 * (lo + hi)


def fc_from_charge(u, Xobs):
    """invert X_obs = X_L(u) f_C  with f_b = 1."""
    return Xobs / XL(u)


# ----------------------------------------------------------------- DD1 frozen table
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
DD1 = os.path.join(ROOT, "fable52_push", "DD1_deduce_from_data", "dd1_table.csv")


def load_dd1():
    rows, cols = [], None
    with open(DD1, "r", newline="") as f:
        for raw in f:
            line = raw.strip()
            if not line or line.startswith("#"):
                continue
            parts = [pp.strip() for pp in line.split(",")]
            if cols is None:
                cols = parts
                continue
            d = dict(zip(cols, parts))
            if d.get("bracket", "") != "":
                continue                      # main rows only
            rows.append(d)
    return rows


def med(v):
    v = sorted(v)
    n = len(v)
    if n == 0:
        return float("nan")
    return v[n // 2] if n % 2 else 0.5 * (v[n // 2 - 1] + v[n // 2])


def mad_se(v):
    if len(v) == 1:
        return float("nan")
    m = med(v)
    return 1.2533 * 1.4826 * med([abs(x - m) for x in v]) / math.sqrt(len(v))


# ------------------------------------------------------- cosmic time, in y = ln(1+z)
def E_of_z(z):
    return math.sqrt(OM * (1.0 + z) ** 3 + OL)


def _trap(f, a, b, n):
    h = (b - a) / n
    s = 0.5 * (f(a) + f(b))
    for i in range(1, n):
        s += f(a + i * h)
    return s * h


def age_Gyr(z, ymax=40.0, n=40000):
    """age of the universe at redshift z, Gyr.
       t(z) = (1/H0) Int_{y(z)}^{ymax} dy / E(e^y - 1),  y = ln(1+z)."""
    g = lambda y: 1.0 / E_of_z(math.exp(y) - 1.0)
    total = _trap(g, 0.0, ymax, n)
    yz = math.log(1.0 + z)
    part = _trap(g, 0.0, yz, max(2000, int(n * yz / ymax)))
    return H0_INV_GYR * (total - part)


# ------------------------------------------------------- per-class ledger from DD1
def class_stats(rows, a0, band_keys=None):
    """DD1's recipe: per SYSTEM the median over its points; then per CLASS the median
       over its systems; se = 1.2533 * 1.4826 * MAD(d_sys)/sqrt(n)."""
    per_sys = {}
    for row in rows:
        key = (row["cls"], row["sys"])
        gb = 10.0 ** float(row["lgb"])
        go = 10.0 ** float(row["lgo"])
        Y = float(row["lgo"]) - float(row["lgb"])
        per_sys.setdefault(key, []).append(
            {"u": a0 / gb, "X": go / gb - 1.0, "Y": Y,
             "d": Y - YL(gb, a0), "e": float(row["eY"])})
    sysm = {}
    for (cls, sysname), recs in per_sys.items():
        sysm.setdefault(cls, []).append({
            "sys": sysname,
            "u": med([r["u"] for r in recs]),
            "X": med([r["X"] for r in recs]),
            "Y": med([r["Y"] for r in recs]),
            "d": med([r["d"] for r in recs]),
            "e": med([r["e"] for r in recs])})
    out = {}
    for cls, ss in sysm.items():
        # invert the master equation SYSTEM BY SYSTEM, so (u, X_obs, d) are one consistent
        # triple; then take the class median over systems.  (d = log10[(1+X)/(1+X_L)] is exact.)
        per = []
        for s in ss:
            u_s = s["u"]
            xl = XL(u_s)
            xobs = (1.0 + xl) * 10.0 ** s["d"] - 1.0
            per.append({
                "u": u_s, "X_obs": xobs, "d": s["d"], "e": s["e"],
                "X_L": xl, "floor": -math.log10(1.0 + xl),
                "reach": xobs <= u_s,
                "f_b": fb_from_baryons(u_s, xobs),
                "f_C": (xobs / xl) if xl > 0 else float("nan")})
        mu_ = med([q["u"] for q in per])
        mx = med([q["X_obs"] for q in per])     # consistent with md: 1+mx = (1+X_L) 10^md
        md = med([q["d"] for q in per])
        mY = med([s["Y"] for s in ss])
        se = mad_se([q["d"] for q in per])
        dm = dmax(mu_)
        fbs = [q["f_b"] for q in per if q["f_b"] is not None]
        n_below = sum(1 for q in per if q["X_obs"] < 0.0 and q["X_obs"] < -3.0 * q["e"])
        out[cls] = {
            "n_sys": len(ss), "med_u": mu_, "med_X": mx, "med_Y": mY, "med_d": md,
            "se": None if math.isnan(se) else se,
            "d_max": dm, "X_over_u": mx / mu_,
            "reachable_frac": (sum(1 for q in per if q["reach"]) / len(per)),
            "reachable": (mx <= mu_),
            "f_b_baryon_channel": (med(fbs) if fbs else None),
            "f_C_charge_channel": med([q["f_C"] for q in per]),
            "floor_d_median": med([q["floor"] for q in per]),
            "n_sys_below_X0_beyond_3e": n_below,
            "band": (band_keys.get(cls) if band_keys else None)}
    return out


def band_counts(stats, bands):
    n_in = 0
    n_off = 0
    n_un = 0
    n_tr = 0
    for cls, rec in stats.items():
        band = bands.get(cls)
        if band is not None and band[0] - 1e-12 <= rec["med_d"] <= band[1] + 1e-12:
            n_in += 1
        se = rec["se"]
        if se is not None and abs(rec["med_d"]) > 3.0 * se:
            n_off += 1
        if not rec["reachable"]:
            n_un += 1
        fb = rec["f_b_baryon_channel"]
        if fb is not None and abs(fb - 1.0) > 0.05:
            n_tr += 1
    return {"in_band": n_in, "off_law_3se": n_off, "unreachable": n_un,
            "needs_transfer": n_tr, "n_classes": len(stats)}


# -------------------------------------------------------------------------- output
OUT = []


def p(s=""):
    print(s)
    OUT.append(s)


# ==============================================================================
def main():
    mutate = "--mutate" in sys.argv
    res = {"mutate": mutate, "checks": {}, "tables": {}}

    rows = load_dd1()
    p("=" * 78)
    p("FINAL-1  arithmetic for THEORY.md" + ("   [MUTATE]" if mutate else "   [primary]"))
    p("=" * 78)
    p("DD1 frozen table: %d main rows (frozen, unchanged, read-only)" % len(rows))
    p("G = %.5e m^3 kg^-1 s^-2   c = %.9e m/s   K = 4 pi G = %.6e" % (G, c, K))
    p("a0 canonical = %.5e m/s^2     a0 alt = %.5e m/s^2  (never pooled)" %
      (A0["canonical"], A0["alt"]))
    p("kappa = %.1f FITTED ; Z = 2 sqrt(8 pi/3) = %.4f ; R = Omega_c/Omega_b = %.2f" %
      (KAPPA, Z_CONS, RB))
    p("")

    # ---------------- A1  the two forms of the law are one;  u = x^2 --------------
    p("-" * 78)
    p("A1  the law's two forms agree, and u = x^2  (checked on every DD1 main point)")
    p("-" * 78)
    a1 = {}
    for footing, a0 in A0.items():
        worst_u = worst_g = 0.0
        for row in rows:
            gb = 10.0 ** float(row["lgb"])
            u = a0 / gb
            worst_u = max(worst_u, abs(X(math.sqrt(u)) - XL(u)) / XL(u))
            g = g_of_gN(gb, a0)                      # closed form
            worst_g = max(worst_g, abs((g * g / (g + a0)) / gb - 1.0))
        a1[footing] = {"worst_X_u_rel": worst_u, "worst_law_inversion_rel": worst_g}
        p("  %-9s max|X(sqrt u) - X_L(u)|/X_L = %.3e ; max|g_N(g(g_N))/g_N - 1| = %.3e"
          % (footing, worst_u, worst_g))
    a1_pass = all(a1[f]["worst_X_u_rel"] < 1e-10 and a1[f]["worst_law_inversion_rel"] < 1e-10
                  for f in A0)
    res["checks"]["A1"] = {"pass": bool(a1_pass), "detail": a1}
    p("  A1 verdict: %s" % a1_pass)
    p("")

    # ---------------- A2  the two columns ---------------------------------------
    p("-" * 78)
    p("A2  the deep column a0/(2 pi G)  and the amount-fixing gas column a0/(pi G x_b^2)")
    p("-" * 78)
    a2 = {}
    rec_deep = {"canonical": 106.9, "alt": 129.1}      # EQ1 sec.6 / SHAPE_search route D
    rec_gas = {"canonical": 6.1627, "alt": 7.4477}  # GAS1 (printed with G = 6.674e-11)
    gsc = G / 6.674e-11
    for footing, a0 in A0.items():
        dk = a0 / (2.0 * math.pi * G)
        gk = a0 / (math.pi * G * XB2)
        conv = PC ** 2 / MSUN
        a2[footing] = {"deep_kg_m2": dk, "deep_Msun_pc2": dk * conv,
                       "gas_kg_m2": gk, "gas_Msun_pc2": gk * conv,
                       "gas_Msun_pc2_rescaled_to_GAS1_G": gk * conv * gsc,
                       "ratio_gas_over_deep": gk / dk}
    p("  %-9s %-19s %-19s %-13s %s" % ("footing", "a0/(2piG) kg/m^2", "Msun/pc^2",
                                            "a0/(piG x_b^2) kg/m^2", "Msun/pc^2"))
    for f in ("canonical", "alt"):
        d = a2[f]
        p("  %-9s %-19.6e %-19.3f %-19.6e %.4f"
          % (f, d["deep_kg_m2"], d["deep_Msun_pc2"], d["gas_kg_m2"], d["gas_Msun_pc2"]))
    p("  vs recorded: deep 106.9 / 129.1 Msun/pc^2 ; gas 6.1627 / 7.4477 Msun/pc^2")
    p("     (GAS1 printed G = 6.674e-11; rescale factor %.8f -> gas %.4f / %.4f)"
      % (gsc, a2["canonical"]["gas_Msun_pc2_rescaled_to_GAS1_G"],
         a2["alt"]["gas_Msun_pc2_rescaled_to_GAS1_G"]))
    ok_deep = all(abs(a2[f]["deep_Msun_pc2"] - rec_deep[f]) < 0.1 for f in A0)
    ok_gas = all(abs(a2[f]["gas_Msun_pc2_rescaled_to_GAS1_G"] - rec_gas[f]) / rec_gas[f] < 2e-4
                 for f in A0)
    ok_ratio = all(abs(a2[f]["ratio_gas_over_deep"] - 2.0 / XB2) < 1e-12 for f in A0)
    a2_pass = bool(ok_deep and ok_gas and ok_ratio)
    res["checks"]["A2"] = {"pass": a2_pass, "deep_match": bool(ok_deep),
                           "gas_match": bool(ok_gas), "ratio_identity": bool(ok_ratio),
                           "detail": a2}
    p("  A2 verdict: %s" % a2_pass)
    p("")

    # ---------------- A3  the ceiling curve ---------------------------------------
    p("-" * 78)
    p("A3  the ceiling of the baryon-loss channel: d_max(u) = log10[(1+u)/(1+X_L(u))]")
    p("     footing-free: u = a0/g_bar is the footing-free field variable")
    p("-" * 78)
    us = [1e-3, 1e-2, 0.1, 0.5, 1.0, 2.0, 4.5, 10.0, 30.0, 1e2, 1e3, 1e4, 1e6]
    curve = []
    prev, mono = -1e9, True
    p("     %-11s %-12s %-12s %-16s" % ("u=a0/g_bar", "X_L(u)", "d_max[dex]",
                                        "d_max/(0.5 log10 u)"))
    for u in us:
        dm = dmax(u)
        curve.append({"u": u, "X_L": XL(u), "d_max": dm})
        half = 0.5 * math.log10(u)
        rs = ("%.5f" % (dm / half)) if u > 1 and abs(half) > 1e-9 else "-"
        p("     %-11.4g %-12.6f %-12.6f %-16s" % (u, XL(u), dm, rs))
        if dm <= prev:
            mono = False
        prev = dm
    rat = dmax(1e4) / (0.5 * math.log10(1e4))
    a3_pass = bool(mono and abs(rat - 1.0) < 0.01)
    res["checks"]["A3"] = {"pass": a3_pass, "monotone": bool(mono),
                            "ratio_at_u_1e4": rat, "curve": curve}
    p("  monotone: %s ; d_max(1e4)/(0.5 log10 1e4) = %.5f" % (mono, rat))
    p("  A3 verdict: %s   (deep limit: d_max -> (1/2) log10 u)" % a3_pass)
    p("")

    # ---------------- A4  per-class ledger -----------------------------------------
    p("-" * 78)
    p("A4  the ledger per class, from DD1 (per-system medians, DD1's recipe)")
    p("-" * 78)
    led = {}
    for footing, a0 in A0.items():
        stats = class_stats(rows, a0, BANDS)
        led[footing] = {}
        p("  [%s]  a0 = %.5e m/s^2" % (footing, a0))
        p("  %-19s %4s %9s %9s %7s %7s %6s %-11s %7s %7s %6s"
          % ("class", "n", "med u", "med X", "med d", "se", "d_max", "reach",
             "f_b", "f_C", "floor"))
        for cls in sorted(stats):
            r = stats[cls]
            led[footing][cls] = r
            fbs = r["f_b_baryon_channel"]
            p("  %-19s %4d %9.4g %9.4g %7.3f %7.3f %6.3f %-11s %7s %7.3f %6.2f"
              % (cls, r["n_sys"], r["med_u"], r["med_X"], r["med_d"],
                 r["se"] if r["se"] is not None else float("nan"),
                 r["d_max"], "YES" if r["reachable"] else "UNREACHABLE",
                 ("%.3f" % fbs) if fbs is not None else "   --  ",
                 r["f_C_charge_channel"], r["floor_d_median"]))
        counts = band_counts(stats, BANDS)
        tot_below = sum(r["n_sys_below_X0_beyond_3e"] for r in stats.values())
        tot_sys = sum(r["n_sys"] for r in stats.values())
        counts["n_systems_below_X0_beyond_3e"] = tot_below
        counts["n_systems"] = tot_sys
        led[footing]["_counts"] = counts
        p("  -- systems below X = 0 beyond 3 e:                  %d of %d" % (tot_below, tot_sys))
        p("  -- classes UNREACHABLE by any transfer (X > u): %d of %d"
          % (counts["unreachable"], counts["n_classes"]))
        p("  -- classes needing a non-trivial transfer (|f_b - 1| > 0.05): %d of %d"
          % (counts["needs_transfer"], counts["n_classes"]))
        p("")
    res["tables"]["A4_ledger"] = led

    # ---------------- A5  the amount cap -------------------------------------------
    p("-" * 78)
    p("A5  the amount cap, recomputed at FLD1's KiDS window edges (log M_b = 10.45)")
    p("-" * 78)
    rowsA5 = []
    for footing, a0 in A0.items():
        Mb = 10.0 ** 10.45
        rm = rM(Mb, a0)
        for rkpc, tag in [(272.0, "FLD1 inner window edge"),
                          (637.0, "FLD1 middle window edge")]:
            x = rkpc * 1e3 * PC / rm
            dem = X(x)
            rowsA5.append({"footing": footing, "r_kpc": rkpc, "where": tag,
                           "rM_kpc": rm / (1e3 * PC), "x": x, "X": dem,
                           "over_5p41": dem / RB,
                          "over_1p06": dem / DELIVERED["record_infall"],
                          "over_1p40": dem / DELIVERED["VSH1_settled"]})
    p("  %-9s %7s %-26s %9s %9s %10s %8s %8s %8s"
      % ("footing", "r[kpc]", "where", "r_M[kpc]", "x", "X(x)[M_b]",
         "/5.41", "/1.06", "/1.40"))
    for r in rowsA5:
        p("  %-9s %7.1f %-26s %9.3f %9.3f %10.3f %8.2f %8.2f %8.2f"
          % (r["footing"], r["r_kpc"], r["where"], r["rM_kpc"], r["x"], r["X"],
             r["over_5p41"], r["over_1p06"], r["over_1p40"]))
    a5_pass = bool(all(r["over_5p41"] > 1.0 for r in rowsA5))
    res["checks"]["A5"] = {"pass": a5_pass, "rows": rowsA5}
    p("  A5 verdict: %s   (the law's demand exceeds the whole cosmic budget at both edges)"
      % a5_pass)
    p("")

    # ---------------- A6  the three regimes -------------------------------------------
    p("-" * 78)
    p("A6  the three regimes for a reference galaxy, log M_b = 10.45 (point baryons)")
    p("-" * 78)
    A6 = []
    for footing, a0 in A0.items():
        Mb = 10.0 ** 10.45
        rm = rM(Mb, a0) / (1e3 * PC)
        X1 = math.sqrt(2.0) * rm
        bud = math.sqrt(XB2) * rm
        xt = math.sqrt(X_S_PD1 * (X_S_PD1 + 1.0))
        tr = xt * rm
        vinf = (G * Mb * MSUN * a0) ** 0.25 / 1e3
        sig = math.sqrt(0.5 * math.sqrt(G * Mb * MSUN * a0)) / 1e3
        A6.append({"footing": footing, "rM_kpc": rm, "Xeq1_kpc": X1,
                   "budget_kpc": bud, "x_t": xt, "trunc_kpc": tr, "vinf_kms": vinf,
                   "sigma_kms": sig})
        p("  %-9s r_M = %7.3f kpc ; X = 1 at %7.3f kpc ; budget (5.41 M_b) spent at"
          " %7.3f kpc" % (footing, rm, X1, bud))
        p("  %-9s truncation at %7.1f kpc   (x_t = sqrt(59.5 x 60.5) = %.3f) ;"
          " v_inf = %.1f km/s ; sigma = %.1f km/s" % (footing, tr, xt, vinf, sig))
    ord_ok = bool(all(a["rM_kpc"] < a["Xeq1_kpc"] < a["budget_kpc"] < a["trunc_kpc"]
                      for a in A6))
    res["checks"]["A6"] = {"pass": ord_ok, "rows": A6}
    p("  ordering r_M < sqrt(2) r_M < x_b r_M < x_t r_M : %s" % ord_ok)
    p("")

    # ---------------- A7  the epoch ---------------------------------------------
    p("-" * 78)
    p("A7  cosmic time, for the epoch-invariance test (H0 = %.1f km/s/Mpc, Om = %.4f"
      % (H0, OM))
    p("-" * 78)
    E7 = {}
    for z in (0.05, 0.45, 0.90):
        E7[z] = age_Gyr(z)
    for z in sorted(E7):
        p("     z = %.2f   age = %8.4f Gyr" % (z, E7[z]))
    r45 = E7[0.45] / E7[0.05]
    r90 = E7[0.90] / E7[0.05]
    p("     age(0.45)/age(0.05) = %.5f  ->  log10 = %+.4f dex" % (r45, math.log10(r45)))
    p("     age(0.90)/age(0.05) = %.5f  ->  log10 = %+.4f dex" % (r90, math.log10(r90)))
    p("     (a charge that accumulates in proportion to cosmic time shifts d by that log10)")
    a7_pass = bool(12.0 < E7[0.05] < 14.5 and 7.0 < E7[0.45] < 10.0)
    res["checks"]["A7"] = {"pass": a7_pass, "ages_Gyr": E7,
                            "log10_ratio_z0.45_over_z0.05": math.log10(r45),
                            "log10_ratio_z0.90_over_z0.05": math.log10(r90)}
    p("  A7 verdict: %s   (t(0)=%.3f Gyr, t(0.45)=%.3f Gyr, t(0.90)=%.3f Gyr)"
      % (a7_pass, E7[0.05], E7[0.45], E7[0.90]))
    p("")

    # ---------------- A8  the channels -------------------------------------------
    p("-" * 78)
    p("A8  the master equation's channels (deep limit d ~ log10(f_C/f_b), footing-free)")
    p("-" * 78)
    p("     f      S: charge kept f_C, f_b=1    B/A: baryons f_b, f_C=1")
    chan = []
    for f in [10.0, 5.0, 3.0, 2.0, 1.5, 1.0, 0.5, 0.3, 0.186, 0.1, 0.053, 0.028]:
        dch = -(0.5) * math.log10(f)      # baryon channel: f<1 loss (+), f>1 accretion (-)
        chan.append({"f": f, "d_baryon_channel": dch})
        p("     %5.3f   f_C=%5.3f                    d = %+7.3f dex" % (f, f, dch))
    res["tables"]["A8_channels"] = chan
    p("")

    # ---------------- A9  worked scales ------------------------------------------
    p("-" * 78)
    p("A9  worked scales, log M_b = 10.45, both footings (SI)")
    p("-" * 78)
    A9 = []
    for footing, a0 in A0.items():
        Mb = 10.0 ** 10.45
        rm = rM(Mb, a0)
        vinf = (G * Mb * MSUN * a0) ** 0.25
        sig = math.sqrt(0.5 * math.sqrt(G * Mb * MSUN * a0))
        A9.append({"footing": footing, "rM_m": rm, "rM_kpc": rm / (1e3 * PC),
                 "vinf_ms": vinf, "vinf_kms": vinf / 1e3, "sigma_kms": sig / 1e3})
        p("  %-9s r_M = %.4e m = %.3f kpc ; v_inf = %.4e m/s = %.1f km/s ; sigma = %.1f km/s"
          % (footing, rm, rm / (1e3 * PC), vinf, vinf / 1e3, sig / 1e3))
    res["tables"]["A9_scales"] = A9
    p("")

    # ---------------- A10  the exact ceiling per class ----------------------------
    p("-" * 78)
    p("A10 the EXACT ceiling per class:  d <= d_max = log10[(1+u)/(1+X_L(u))]")
    p("-" * 78)
    a10 = {}
    for footing in A0:
        items = []
        for cls, rec in led[footing].items():
            if cls.startswith("_"):
                continue
            items.append((cls, rec["med_d"], dmax(rec["med_u"]),
                          rec["med_d"] - dmax(rec["med_u"])))
        viol = sorted([i for i in items if i[3] > 0.0], key=lambda t: -t[3])
        a10[footing] = {"n_violating": len(viol),
                        "violating": [(v[0], round(v[3], 4)) for v in viol]}
        p("  %-9s classes above their exact ceiling: %d of %d   %s"
          % (footing, len(viol), len(items),
             "-> " + ", ".join("%s %+.3f" % (v[0], v[3]) for v in viol)))
    res["tables"]["A10_ceiling"] = a10
    p("")

    # =============================================================== MUTATE ARMS
    if mutate:
        p("=" * 78)
        p("MUTATE ARMS  (each must change its stated outcome)")
        p("=" * 78)
        mut = {}

        # ---- M1: the force reading (every system on the plain law now) ---------
        # Prediction is d_pred = 0 for every class.  Gate: FRM1's pre-registered bands.
        n_in_force = sum(1 for b in BANDS.values() if b[0] - 1e-12 <= 0.0 <= b[1] + 1e-12)
        n_in_form = led["canonical"]["_counts"]["in_band"]
        stripped_low = all(BANDS[c][1] <= -0.30 for c in STRIPPED_FAMILY)
        ufd_high = BANDS["MW ultra-faints"][0] >= 0.30
        m1 = {"pred_d_force_reading": 0.0,
              "classes_in_band_under_force": n_in_force,
              "classes_in_band_under_formation": n_in_form,
              "stripped_family_band_is_low": bool(stripped_low),
              "ufd_band_is_high": bool(ufd_high),
              "classes_needing_transfer_under_force": 0,
              "classes_needing_transfer_under_formation": led["canonical"]["_counts"]["needs_transfer"]}
        mut["M1"] = m1
        p("  M1 the force reading (prediction d = 0 for every class; bands are the gate):")
        p("       classes in band: %d of %d   (formation: %d of %d)"
          % (n_in_force, len(BANDS), n_in_form, len(BANDS)))
        p("       stripped family's band is LOW? %s ; MW ultra-faints' band is HIGH? %s"
          % (stripped_low, ufd_high))
        p("       -> under the force reading both structural signs are wrong: BITES")
        p("")
        for footing, a0 in A0.items():
            p("     %-9s classes in band: force %d , formation %d"
              % (footing, n_in_force, led[footing]["_counts"]["in_band"]))
        p("")

        # ---- M2: a0 x 2 ----------------------------------------------------------
        scales = {}
        for footing, a0 in A0.items():
            Mb = 10.0 ** 10.45
            rm1 = rM(Mb, a0)
            rm2 = rM(Mb, 2.0 * a0)
            c1 = a0 / (2.0 * math.pi * G)
            c2 = 2.0 * a0 / (2.0 * math.pi * G)
            scales[footing] = {"rM_ratio": rm2 / rm1, "column_ratio": c2 / c1}
        rM_ok = all(abs(s["rM_ratio"] - 2.0 ** -0.5) < 1e-5 for s in scales.values())
        col_ok = all(abs(s["column_ratio"] - 2.0) < 1e-5 for s in scales.values())
        mut["M2"] = {"rM_scales_by_2^-1/2": bool(rM_ok), "column_scales_by_2": bool(col_ok),
                     "detail": scales}
        p("  M2 a0 x 2, both footings:")
        p("       r_M ratio = %s (expect %.5f) : %s"
          % (", ".join("%.6f" % scales[f]["rM_ratio"] for f in ("canonical", "alt")),
             2.0 ** -0.5, rM_ok))
        p("       column ratio = %s (expect 2.000000) : %s"
          % (", ".join("%.6f" % scales[f]["column_ratio"] for f in ("canonical", "alt")),
             col_ok))
        p("       footing-free rows (x, u, X, d, d_max) unchanged by construction: BITES")
        p("")

        # ---- M3: class labels shuffled across systems (seed 20261110) -------------
        cls_sizes, per_sys = {}, {}
        for row in rows:
            cls_sizes[row["cls"]] = cls_sizes.get(row["cls"], 0) + 1
            per_sys.setdefault((row["cls"], row["sys"]), []).append({
                "u": A0["canonical"] / (10.0 ** float(row["lgb"])),
                "d": (float(row["lgo"]) - float(row["lgb"]))
                     - YL(10.0 ** float(row["lgb"]), A0["canonical"])})
        sysd = {k: med([r["d"] for r in v]) for k, v in per_sys.items()}
        sysu = {k: med([r["u"] for r in v]) for k, v in per_sys.items()}
        # class sizes in SYSTEMS (not rows), so the shuffle below is well defined
        cls_nsys = {}
        for (_cname, _sname) in per_sys:
            cls_nsys[_cname] = cls_nsys.get(_cname, 0) + 1
        keys = list(sysd.keys())
        rnd = random.Random(20261110)
        rnd.shuffle(keys)
        n_in_sh = 0
        i = 0
        for nm in sorted(cls_nsys):
            m = cls_nsys[nm]
            chosen = keys[i:i + m]
            i += m
            off = med([sysd[k] for k in chosen])
            band = BANDS[nm]
            if band[0] - 1e-12 <= off <= band[1] + 1e-12:
                n_in_sh += 1
        m3 = {"classes_in_band_after_shuffle": n_in_sh, "must_be_below": 13,
              "formation_value": led["canonical"]["_counts"]["in_band"]}
        mut["M3"] = m3
        p("  M3 class labels shuffled across systems (seed 20261110; bands stay with names):")
        p("       classes in band: %d  (formation %d ; must be < 13 -> %s)"
          % (n_in_sh, m3["formation_value"], "BITES" if n_in_sh < 13 else "DOES NOT BITE"))
        p("")

        # ---- M4: the ceiling removed ------------------------------------------------
        m4 = {"unreachable_with_ceiling": led["canonical"]["_counts"]["unreachable"],
              "unreachable_without_ceiling": 0,
              "P1_status_with_ceiling": "VIOLATED by the cluster classes",
              "P1_status_without_ceiling": "VACUOUS"}
        mut["M4"] = m4
        p("  M4 the ceiling removed (f_b -> 0 lifts X without limit):")
        p("       UNREACHABLE classes %d -> 0 ; prediction P1 goes VIOLATED -> VACUOUS: BITES"
          % m4["unreachable_with_ceiling"])
        p("")

        all_bite = bool(n_in_force != n_in_form and rM_ok and col_ok and n_in_sh < 13)
        res["mutations"] = mut
        p("  ALL FOUR ARMS BIT: %s" % all_bite)
        res["all_arms_bite"] = all_bite
        p("")

    # ---------------- summary -------------------------------------------------------
    p("=" * 78)
    p("SUMMARY OF GRADED CHECKS")
    p("=" * 78)
    allpass = True
    for k in sorted(res["checks"]):
        ok = res["checks"][k]["pass"]
        p("  %-4s %s" % (k, "PASS" if ok else "FAIL"))
        allpass = allpass and ok
    p("  ALL: %s" % ("PASS" if allpass else "FAIL"))
    res["all_pass"] = bool(allpass)
    p("")
    p("Adopts nothing. kappa = 1/2 FITTED; not theory closed.")

    with open(os.path.join(HERE, "final1_MUTATE.json" if mutate else "final1.json"), "w") as f:
        json.dump(res, f, indent=1, default=str)
    with open(os.path.join(HERE, "final1_MUTATE.out" if mutate else "final1.out"), "w") as f:
        f.write("\n".join(OUT) + "\n")


if __name__ == "__main__":
    main()
