#!/usr/bin/env python3
r"""CFG250 slope theory -- the mass-free a0 estimator from the local log-slope of V_c^2, its point-mass bias for an exponential
disc (+ a gas disc), and how a pressure-support correction shifts the slope.  PHASE 1, THEORY ONLY.

No measured KURVS velocity or dispersion is read.  The 'typical KURVS-like disc' uses only catalogue columns
(kurvs2023_integrated.csv: z_halpha, logMstar, reff_kpc) and the f_DM table's kurvs_id column (which ten discs).

T1  sympy: Phi(y) = y nu(y); s = d ln V_c^2 / d ln R = 1 - 2 dlnPhi/dlny for a point mass; P2 closed forms; nu_mono numerically;
    the inversion y(s); the sensitivity d ln a0 / ds; the kernel dependence of a0 at fixed (s, g_obs).
T2  flat a0 vs the rival a0 x E(z): E(1.5) exactly; the slope gap between the two laws at fixed g_obs.
T3  the point-mass bias: the full thin-disc (stars R_d + gas at a declared scale) slope vs the point-mass formula at the same g_obs,
    at R = 2, 3, 4, 6 R_d, for flat and rival, P2 and nu_mono; gas and mass brackets.  The generalisation that removes it: at a
    radius where the baryon SHAPE has Newtonian log-slope s_N, s = 1 + D(y)(s_N - 1) with D = dlnPhi/dlny, so
    D = (1 - s)/(1 - s_N) (s_N = -1 is the point mass): still free of the mass normalisation, but it needs the baryon shape.
T4  the pressure correction V_c^2 = V^2 + k sigma^2 R/R_d (k = 2 primary; k = 1; Kretschmer+2021 alpha(x); none): the slope shift
    s_a - s_c = (dP/V_a^2)(s_dP - s_c), the pressure fraction, and the resulting shift of the point-mass a0.
T5  what slope accuracy the test needs; the MUTATE analogue (V x R^0.1).
kappa = 1/2 and Omega_c h^2 stay fitted.  Nothing here says the data favour any law.
Run: python3 campaign_fresh_gravity/CFG250_massfree_slope_a0/CFG250_slope_theory.py
"""
import os
import sys
import csv
import math

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import sympy as sp
import cfg250_common as C

T = C.Tee("CFG250_slope_theory")
print(__doc__.split("Run: python3")[0].strip())
LN10 = math.log(10)
KER = {n: C.Kernel(n) for n in ("P2", "nu_mono")}

# ================================================================================================ T1
T.banner("T1  the point-mass slope law s(y) and its inversion")
y, s_ = sp.symbols("y s", positive=True)
Phi = sp.sqrt(y ** 2 + y)                                                     # P2: nu = sqrt(1 + 1/y)
s_expr = sp.simplify(1 - 2 * y * sp.diff(Phi, y) / Phi)
print(f"  P2: Phi(y) = y nu(y) = {Phi};  s(y) = 1 - 2 dlnPhi/dlny = {s_expr}")
ssym = sp.Symbol("s")
yinv = sp.solve(sp.Eq(ssym, -y / (1 + y)), y)
print(f"  inversion: y(s) = {yinv[0]}   (domain -1 < s < 0)")
dlnPhi_s = sp.simplify((y * sp.diff(Phi, y) / Phi).subs(y, yinv[0]))
dlna0_ds = sp.simplify(-dlnPhi_s * sp.diff(sp.log(yinv[0]), ssym))
print(f"  dlnPhi/dlny at y(s) = {dlnPhi_s};  a0 = g_obs / Phi(y(s))  =>  d ln a0 / ds |_g = {dlna0_ds}")
lim_deep = sp.limit(s_expr, y, 0)
lim_newt = sp.limit(s_expr, y, sp.oo)
print(f"  limits: deep MOND y -> 0: s -> {lim_deep};  Newton y -> oo: s -> {lim_newt}")
T.check("T1a P2 closed form: s(y) = -y/(1+y) and y(s) = -s/(1+s)",
        f"s = {s_expr}; y = {yinv[0]}", sp.simplify(s_expr + y / (1 + y)) == 0 and sp.simplify(yinv[0] + ssym / (1 + ssym)) == 0)
T.check("T1b P2 limits: s -> 0 (deep MOND) and s -> -1 (Newton)", f"{lim_deep}, {lim_newt}", lim_deep == 0 and lim_newt == -1)

km = KER["nu_mono"]
mask = km.lny < math.log(1e8)
mono_ok = bool(np.all(np.diff(km.s[mask]) < 0)) and km.phi_monotone
T.check("T1c nu_mono: Phi(y) monotone and s(y) strictly decreasing on 1e-9 < y < 1e8 (so y(s) is single-valued)",
        f"Phi monotone {km.phi_monotone}; s decreasing {bool(np.all(np.diff(km.s[mask]) < 0))} (the table clamps above 1e8.9)", mono_ok)
ygrid = np.array([0.01, 0.03, 0.1, 0.3, 1.0, 3.0, 10.0])
print("\n  s(y) for the two kernels (point mass):")
print("     y      s_P2     s_mono   | at fixed s: y_P2   y_mono   log10(a0_mono/a0_P2) at the same g_obs")
rows = []
for yy in ygrid:
    sP = float(KER["P2"].s_of_y(yy)); sM = float(km.s_of_y(yy))
    # at the P2 slope, what does each kernel infer?
    yP = float(KER["P2"].y_of_s(sP)); yM = float(km.y_of_s(sP))
    dl = math.log10(KER["P2"].Phi(yP) / km.Phi(yM)) if np.isfinite(yM) else float("nan")
    rows.append(dict(y=yy, s_P2=sP, s_mono=sM, y_P2_at_sP2=yP, y_mono_at_sP2=yM, dlog_a0_mono_minus_P2=dl))
    print(f"  {yy:6.2f}  {sP:+.4f}  {sM:+.4f}   | {yP:8.4f} {yM:8.4f}   {dl:+.3f}")
T.numbers["T1_s_table"] = rows
print("  reading: nu_mono approaches deep MOND as s ~ -sqrt(y)/2 (sub-leading g_bar/2 term), P2 as s ~ -y; at fixed (s, g_obs) the two")
print("  kernels infer a0 differing by the last column, so the estimator is kernel-conditional (P2 primary, nu_mono reported).")

# ================================================================================================ T2
T.banner("T2  the two laws: flat a0 vs a0 x E(z)")
integ = {int(r["kurvs_id"]): r for r in csv.DictReader(open(os.path.join(C.AT, "kurvs2023_integrated.csv")))}
ten = sorted(int(r["kurvs_id"]) for r in csv.DictReader(open(os.path.join(C.AT, "kurvs2023_fdm.csv"))))   # id column only
zs = np.array([float(integ[k]["z_halpha"]) for k in ten])
lm = np.array([float(integ[k]["logMstar"]) for k in ten])
re = np.array([float(integ[k]["reff_kpc"]) for k in ten])
zmed, lmmed, rdmed = float(np.median(zs)), float(np.median(lm)), float(np.median(re)) / 1.68
E15 = float(C.E(1.5)); Emed = float(C.E(zmed))
print(f"  E(z) = sqrt(0.315 (1+z)^3 + 0.685):  E(1.5) = {E15:.5f}  (log10 {math.log10(E15):.4f});  the ten discs' median z = {zmed:.3f}: "
      f"E = {Emed:.4f} (log10 {math.log10(Emed):.4f}); range over the ten {float(C.E(zs.min())):.3f}-{float(C.E(zs.max())):.3f}")
print(f"  (the task text's 'E(1.5) ~ 2.2' is approximate; the exact value for Om = 0.315 is {E15:.4f})")
T.numbers.update(E_1p5=E15, z_med_ten=zmed, E_zmed=Emed, logMstar_med_ten=lmmed, Rd_med_ten_kpc=rdmed, ten_ids=ten)
T.check("T2a E(1.5) = sqrt(0.315 x 2.5^3 + 0.685) exactly", f"{E15:.6f}", abs(E15 - math.sqrt(0.315 * 15.625 + 0.685)) < 1e-12)
print("\n  the point-mass slope gap between the laws at fixed g_obs (P2, canonical a0 = 9.36e-11):")
print("   g_obs/a0   s_flat    s_rival(z_med)   gap")
a0 = C.A0["canonical"]
gaps = []
for t in (0.3, 0.5, 1.0, 2.0, 4.0):
    sf = float(KER["P2"].s_of_y(KER["P2"].Phi_inv(t)))
    sr = float(KER["P2"].s_of_y(KER["P2"].Phi_inv(t / Emed)))
    gaps.append(dict(g_over_a0=t, s_flat=sf, s_rival=sr, gap=sr - sf))
    print(f"   {t:6.2f}   {sf:+.3f}    {sr:+.3f}          {sr - sf:+.3f}")
T.numbers["T2_gaps"] = gaps

# ================================================================================================ T3
T.banner("T3  point-mass bias for an exponential disc (+ gas disc): full-disc slope vs the point-mass formula at the same g_obs")
print(f"  typical KURVS-like disc (catalogue medians of the ten f_DM discs): log M* = {lmmed:.2f}, R_d = R_eff/1.68 = {rdmed:.2f} kpc, "
      f"z = {zmed:.3f}")
print("  law: g_obs = nu(g_N/a) g_N in the disc plane (algebraic form), a = a0 (flat) or a0 E(z) (rival); thin exponential discs;")
print("  gas = mu M* in an exponential disc of scale R_gas (declared 2 R_d primary, as CFG140). s_disc = dlnV_c^2/dlnR numerically;")
print("  a0_PM = g_obs / Phi(y(s)) is what the point-mass estimator returns; bias = log10(a0_hat / a_true).")


def curve_slope(R, Ms, mu, Rd, rg, a, ker, geom="disc"):
    """g_obs and s = dlnV_c^2/dlnR of the full model at R."""
    h = 1e-4
    def lnV2(r):
        gN = C.gN_baryons(r, Ms, mu, Rd, rg, geom)
        return np.log(KER[ker].Phi(gN / a) * a * r)
    gN = C.gN_baryons(R, Ms, mu, Rd, rg, geom)
    g = KER[ker].Phi(gN / a) * a
    s = (lnV2(R * math.exp(h)) - lnV2(R * math.exp(-h))) / (2 * h)
    return float(g), float(s)


def sN_shape(R, mu, Rd, rg, geom="disc"):
    """the Newtonian log-slope of V_N^2 = g_N R for the baryon SHAPE (independent of the mass normalisation)."""
    h = 1e-4
    f = lambda r: math.log(float(C.gN_baryons(r, 1.0, mu, Rd, rg, geom)) * r)
    return (f(R * math.exp(h)) - f(R * math.exp(-h))) / (2 * h)


def estimate(g, s, sN, ker):
    """the shape-aware local estimator: s = 1 + D(y) (s_N - 1)  =>  D = (1 - s)/(1 - s_N), y = D^-1, a0 = g / Phi(y).
    s_N = -1 is the point-mass estimator of the idea (D = (1 - s)/2, y = -s/(1+s) for P2).  Returns +inf when the observed
    slope is too shallow for any finite a0 (D <= 1/2: the a0 LOWER-limit side), 0 when too steep (D >= 1: Newtonian, upper limit)."""
    D = (1.0 - s) / (1.0 - sN)
    yy = float(KER[ker].y_of_D(D))
    if not np.isfinite(yy):
        return float("inf") if D <= 0.75 else 0.0
    return g / float(KER[ker].Phi(yy))


def dex(ahat, a):
    if ahat == float("inf"):
        return float("inf")
    if ahat <= 0:
        return -float("inf")
    return math.log10(ahat / a)


Ms = 10 ** lmmed
xs = np.array([2.0, 3.0, 4.0, 6.0])
SHAPES = [(0.25, 2.0), (0.67, 1.0), (0.67, 2.0), (0.67, 3.0), (1.5, 2.0), (4.0, 2.0)]
DECL = (0.67, 2.0)                                                            # the analyst's declared shape (CFG140's gas model)

print("\n  (a) the Newtonian log-slope s_N = dlnV_N^2/dlnR of the baryon shape (point mass: -1), independent of M and of the law:")
print("     mu   R_gas/R_d |  R/R_d = 2       3       4       6")
sN_tab = {}
for mu, rg in SHAPES:
    vals = [sN_shape(x * rdmed, mu, rdmed, rg) for x in xs]
    sN_tab[(mu, rg)] = vals
    print(f"    {mu:4.2f}   {rg:3.1f}      |  " + "  ".join(f"{v:+.3f}" for v in vals))
T.numbers["T3_sN"] = {f"mu{mu}_Rg{rg}": v for (mu, rg), v in sN_tab.items()}

T3 = []
for ker in ("P2", "nu_mono"):
    for law, a in (("flat", a0), ("rival", a0 * Emed)):
        for mu, rg in SHAPES:
            line = []
            for j, x in enumerate(xs):
                R = x * rdmed
                g, s = curve_slope(R, Ms, mu, rdmed, rg, a, ker)
                a_pm = estimate(g, s, -1.0, ker)
                a_true_shape = estimate(g, s, sN_tab[(mu, rg)][j], ker)
                a_decl = estimate(g, s, sN_tab[DECL][j], ker)
                line.append(dict(x=x, R_kpc=R, g_over_a0=g / a0, s=s, sN_true=sN_tab[(mu, rg)][j],
                                 bias_PM=dex(a_pm, a), bias_shape_true=dex(a_true_shape, a), bias_shape_declared=dex(a_decl, a)))
            T3.append(dict(kernel=ker, law=law, mu=mu, Rgas_over_Rd=rg, rows=line))
T.numbers["T3_bias"] = T3


def fmt(b):
    return "  +inf " if b == float("inf") else ("  -inf " if b == -float("inf") else f"{b:+.3f}")


print("\n  (b) bias = log10(a0_hat / a_true) at R = 2, 3, 4, 6 R_d, typical disc; PM = point-mass estimator (the idea as stated);")
print("      DS = shape-aware estimator with the analyst's DECLARED shape (mu 0.67, R_gas 2 R_d) whatever the truth is.")
print("      +inf = the observed slope is too shallow for any finite a0 under that assumed shape (s >= 0 for PM).")
print("  kernel  law    mu  Rg/Rd |  PM:  2R_d    3R_d    4R_d    6R_d   |  DS(declared):  2R_d    3R_d    4R_d    6R_d")
for row in T3:
    pm = " ".join(fmt(r["bias_PM"]) for r in row["rows"])
    dd = " ".join(fmt(r["bias_shape_declared"]) for r in row["rows"])
    print(f"  {row['kernel']:7s} {row['law']:5s} {row['mu']:4.2f} {row['Rgas_over_Rd']:3.1f}  | {pm} | {dd}")

exact = [r["bias_shape_true"] for row in T3 for r in row["rows"]]
T.check("T3a control: the shape-aware estimator with the TRUE baryon shape returns a_true exactly (|bias| < 1e-4 dex, every row)",
        f"max |bias| = {max(abs(b) for b in exact):.2e} dex over {len(exact)} cases", max(abs(b) for b in exact) < 1e-4)
geo = []
for x in xs:
    g, s = curve_slope(x * rdmed, Ms, 0.67, rdmed, 2.0, a0, "P2", "point")
    geo.append(dex(estimate(g, s, -1.0, "P2"), a0))
T.check("T3b control: on a true point-mass field the point-mass estimator returns a0 exactly (|bias| < 1e-6 dex)",
        [f"{b:+.1e}" for b in geo], all(abs(b) < 1e-6 for b in geo))

fl = [r for r in T3 if r["kernel"] == "P2" and r["law"] == "flat" and (r["mu"], r["Rgas_over_Rd"]) == DECL][0]["rows"]
rv = [r for r in T3 if r["kernel"] == "P2" and r["law"] == "rival" and (r["mu"], r["Rgas_over_Rd"]) == DECL][0]["rows"]
print("\n  (c) the slopes themselves (P2, declared shape mu 0.67, R_gas 2 R_d) and the signal between the laws:")
for f_, r_ in zip(fl, rv):
    print(f"   R = {f_['x']:.0f} R_d ({f_['R_kpc']:.1f} kpc): s_N {f_['sN_true']:+.3f} | flat s {f_['s']:+.3f} (g/a0 {f_['g_over_a0']:.2f}) | "
          f"rival s {r_['s']:+.3f} (g/a0 {r_['g_over_a0']:.2f}) | gap {r_['s'] - f_['s']:+.3f} | PM bias flat {fmt(f_['bias_PM'])}")
T.numbers["T3_signal_P2_declared"] = [dict(x=f_["x"], s_flat=f_["s"], s_rival=r_["s"], gap=r_["s"] - f_["s"], sN=f_["sN_true"])
                                      for f_, r_ in zip(fl, rv)]

print("\n  (d) the shape (gas) systematic of the DS estimator: the spread of its bias over the six declared shapes, P2, per radius:")
spread = []
for law in ("flat", "rival"):
    for j, x in enumerate(xs):
        bb = [row["rows"][j]["bias_shape_declared"] for row in T3 if row["kernel"] == "P2" and row["law"] == law]
        fin = [b for b in bb if np.isfinite(b)]
        spread.append(dict(law=law, x=x, n_finite=len(fin), lo=min(fin) if fin else None, hi=max(fin) if fin else None,
                           n_inf=len(bb) - len(fin)))
        print(f"   {law:5s} R = {x:.0f} R_d: finite in {len(fin)}/6 shapes; bias range "
              + (f"{min(fin):+.3f} .. {max(fin):+.3f} dex" if fin else "none") + (f"; {len(bb) - len(fin)} out of domain" if len(fin) < 6 else ""))
T.numbers["T3_DS_shape_spread"] = spread

print("\n  mass bracket (P2, flat, declared shape): the PM bias depends on the mass (regime); the DS bias with the true shape is 0 at any mass")
mass_rows = []
for dl in (-0.5, 0.0, +0.5):
    bb = []
    for j, x in enumerate(xs):
        g, s = curve_slope(x * rdmed, Ms * 10 ** dl, 0.67, rdmed, 2.0, a0, "P2")
        bb.append(dex(estimate(g, s, -1.0, "P2"), a0))
    mass_rows.append(dict(dlogM=dl, bias_PM=bb))
    print(f"   log M* {lmmed + dl:5.2f}: PM " + " ".join(fmt(b) for b in bb))
T.numbers["T3_mass_bracket"] = mass_rows
print("\n  READING T3: at 2-4 R_d a KURVS-like disc with gas at 2 R_d still has a RISING Newtonian curve (s_N > 0), so the MOND curve")
print("  there is flat or rising and the point-mass estimator (which assumes s_N = -1) reads a0 -> infinity. Only near 6 R_d does the")
print("  PM bias fall to ~0.1 dex (flat) / ~0.2 dex (rival), still with the rival's sign and gas-dependent. The shape-aware (DS) form")
print("  removes the bias exactly for the right shape; its residual systematic is the unmeasured gas shape (d).")

# ================================================================================================ T4
T.banner("T4  the pressure correction and the slope")
print("  observed V^2 = V_c^2 - P_true; the analyst reconstructs V_a^2 = V^2 + P_a.  With dP = P_a - P_true:")
print("     s_a - s_c = (dP / V_a^2) (s_dP - s_c),  s_dP = dln dP/dlnR  (= 1 for k sigma^2 R/R_d with constant sigma).")
print("  Kretschmer+2021: alpha(x) sigma^2 with x = R/R_e - 1; its log-slope is alpha'(x) (x+1)/alpha(x):")
k21_rows = []
for x in (1.0, 2.0, 3.0):
    al = float(C.alpha_k21(x)); dal = -0.292 * x + 1.204
    k21_rows.append(dict(R_over_Re=x + 1, alpha=al, dlnalpha_dlnR=dal * (x + 1) / al))
    print(f"     R/R_e = {x + 1:.0f} (R/R_d = {1.68 * (x + 1):.2f}): alpha = {al:.3f}, dln(alpha)/dlnR = {dal * (x + 1) / al:.3f}; "
          f"k=2 equivalent alpha = 2 R/R_d = {2 * 1.68 * (x + 1):.2f}")
T.numbers["T4_K21"] = k21_rows
T4 = []
presc = ("none", "k1", "k2", "K21x1")
h = 1e-4
for law, a in (("flat", a0), ("rival", a0 * Emed)):
    for sig in (30.0, 45.0, 60.0):
        for j, x in enumerate(xs):
            R = x * rdmed
            Vc2 = lambda r: curve_slope(r, Ms, 0.67, rdmed, 2.0, a, "P2")[0] * r * C.KPC / 1e6       # (km/s)^2
            g, sc = curve_slope(R, Ms, 0.67, rdmed, 2.0, a, "P2")
            a_match = estimate(g, sc, sN_tab[DECL][j], "P2")                   # = a exactly (T3a)
            for pt in presc:
                V2 = Vc2(R) - float(C.pressure_term(R, sig, rdmed, pt))
                for pa in presc:
                    if V2 <= 0:
                        T4.append(dict(law=law, sigma=sig, x=x, truth=pt, analyst=pa, pressure_dominated=True))
                        continue
                    Va2 = lambda r: Vc2(r) - float(C.pressure_term(r, sig, rdmed, pt)) + float(C.pressure_term(r, sig, rdmed, pa))
                    sa = (math.log(Va2(R * math.exp(h))) - math.log(Va2(R * math.exp(-h)))) / (2 * h)
                    ga = Va2(R) * 1e6 / (R * C.KPC)
                    dP = float(C.pressure_term(R, sig, rdmed, pa)) - float(C.pressure_term(R, sig, rdmed, pt))
                    kt = not (pa.startswith("K21") or pt.startswith("K21"))
                    pred = (dP / Va2(R)) * (1.0 - sc) if kt else None
                    a_hat = estimate(ga, sa, sN_tab[DECL][j], "P2")
                    T4.append(dict(law=law, sigma=sig, x=x, truth=pt, analyst=pa, pressure_dominated=False, s_c=sc, s_a=sa,
                                   ds=sa - sc, ds_formula=pred, f_true=float(C.pressure_term(R, sig, rdmed, pt)) / Vc2(R),
                                   Vobs_over_sigma=math.sqrt(V2) / sig, dlog_a0_DS=dex(a_hat, a_match)))
kpairs = [r for r in T4 if not r["pressure_dominated"] and r["ds_formula"] is not None]
ok_formula = all(abs(r["ds"] - r["ds_formula"]) < 1e-5 for r in kpairs)
T.check("T4a the slope-shift formula s_a - s_c = (dP/V_a^2)(1 - s_c) matches the numerical slope for every k-type pair (1e-5)",
        f"{len(kpairs)} pairs; max |diff| {max(abs(r['ds'] - r['ds_formula']) for r in kpairs):.1e}", ok_formula)
T.numbers["T4_pressure"] = T4
print("\n  pressure fraction f = P_k2/V_c^2 (truth k = 2) and V_obs/sigma, typical disc, mu 0.67, P2:")
for law in ("flat", "rival"):
    for sig in (30.0, 45.0, 60.0):
        cells = []
        for x in xs:
            q = [r for r in T4 if r["law"] == law and r["sigma"] == sig and r["truth"] == "k2" and r["analyst"] == "k2" and r["x"] == x][0]
            cells.append("pressure-dominated (V_c^2 < P)" if q["pressure_dominated"] else f"f {q['f_true']:.2f}, V/sig {q['Vobs_over_sigma']:.2f}")
        print(f"   {law:5s} sigma {sig:4.0f}: " + " | ".join(f"{x:.0f}R_d {c}" for x, c in zip(xs, cells)))
print("\n  slope shift ds and the DS a0 shift in dex (declared shape; analyst prescription vs truth; typical disc, mu 0.67):")
print("   law    truth -> analyst  sigma  |  R/R_d = 2               3                 4                 6")
for law in ("flat", "rival"):
    for (pt, pa) in (("k1", "k2"), ("K21x1", "k2"), ("k2", "k1"), ("k2", "K21x1"), ("k2", "none")):
        for sig in (30.0, 45.0, 60.0):
            cells = []
            for x in xs:
                q = [r for r in T4 if r["law"] == law and r["sigma"] == sig and r["truth"] == pt and r["analyst"] == pa and r["x"] == x][0]
                cells.append("   P-dominated   " if q["pressure_dominated"] else f"{q['ds']:+.3f} ({fmt(q['dlog_a0_DS']).strip():>6s})")
            print(f"   {law:5s}  {pt:6s} -> {pa:6s} {sig:4.0f}   | " + "  ".join(cells))
print("  READING T4: a mis-specified pressure term moves s by (dP/V_a^2)(1 - s_c); an OVER-correction (truth weaker than k = 2)")
print("  steepens the reconstructed curve upward and reads as a LARGER a0 (the rival's direction); an under-correction the reverse.")
print("  sigma-gradient: with a local sigma(R) ~ R^gamma in k sigma^2 R/R_d the pressure term's own slope is 1 + 2 gamma instead of 1.")

# ================================================================================================ T5
T.banner("T5  what slope accuracy the test needs (P2, DS estimator with the declared shape, flat truth)")
dl = math.log10(Emed)
req = []
for j, f_ in enumerate(fl):
    s0, g0, sN = f_["s"], f_["g_over_a0"] * a0, sN_tab[DECL][j]
    a_hat = estimate(g0, s0, sN, "P2")
    lo, hi = 0.0, 1.0
    for _ in range(80):
        mid = 0.5 * (lo + hi)
        a2 = estimate(g0, s0 + mid, sN, "P2")
        if a2 == float("inf") or math.log10(a2 / a_hat) > dl:
            hi = mid
        else:
            lo = mid
    dmut = dex(estimate(g0, s0 + 0.2, sN, "P2"), a_hat)
    req.append(dict(x=f_["x"], s=s0, sN=sN, ds_equiv_rival=0.5 * (lo + hi), mutate_dlog_a0=dmut))
    print(f"   R = {f_['x']:.0f} R_d: s = {s0:+.3f}, s_N = {sN:+.3f}; a coherent slope error of {0.5 * (lo + hi):+.3f} mimics the whole "
          f"flat->rival gap ({dl:.3f} dex); MUTATE V x R^0.1 (ds = +0.2) moves a0 by {fmt(dmut).strip()} dex")
T.numbers["T5_requirements"] = req
print("  READING T5: a coherent slope error of about +0.1 is the entire separation of the two laws at KURVS radii. The point-mass bias")
print("  (T3, 0.1 to >1 dex) and a mis-specified pressure term (T4) are each of that size or larger, so the estimator needs the")
print("  baryon SHAPE (gas extent) and the pressure prescription controlled to ~0.05 in slope before the stack can separate the laws.")

rc = T.finish()
sys.exit(rc)
