#!/usr/bin/env python3
"""CFG436: T16's z-slope discriminator on CHEX-MATE. Rule: FROZEN_CRITERIA.md (committed alone first, 1ce251561).

x = (M_tot - M_b - M_ph)/(5.364 M_b) at R500 (def-A). SATURATION: x static. SLOW-RATE: x ~ F(z) = 1 - exp(-lam r(z) tau(z)).
G0: is there a public per-cluster CHEX-MATE (z, M500, Mgas) table? Indicative row: BFC stacks bin 3 / bin 4 of
arXiv 2609.09144, extracted exactly from the vector figure. Run: python3 cfg436_zslope.py [--mutate]  (seconds)
"""
import glob, json, math, os, re, sys
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
DATA = os.path.abspath(os.path.join(REPO, "..", "_external_data", "cfg436_work"))
sys.path.insert(0, os.path.join(HERE, ".."))
import CFG4_common as C4  # noqa: E402

MUT = "--mutate" in sys.argv
TAG = "_MUTATE" if MUT else ""
G, MSUN, MPC = 6.674e-11, 1.989e30, 3.0857e22
GYR = 3.156e16
OM, HH = 0.3, 0.7
H0 = HH * 100e3 / MPC
RHO500_0 = 1.55e-24            # T16's R500 density (kg/m^3) at z = 0
LAMS = {"win_lo": 0.0073, "PRIMARY_mid": 0.5 * (0.0073 + 0.0172), "win_hi": 0.0172, "universal": 0.016, "MW_floor": 0.028}
FSTAR = (0.012, 0.008, 0.016)
OUT, checks, res = [], {}, {"mutate": MUT}
say = OUT.append


def E(z):
    return math.sqrt(OM * (1 + z) ** 3 + 1 - OM)


def t_age(z):  # Gyr, flat LCDM, no radiation
    zz = np.linspace(z, 1000.0, 400001)
    lz = np.log1p(zz)
    integrand = 1.0 / np.array([E(v) for v in zz[::100]])
    # integrate in ln(1+z): dt = dln(1+z) / (H0 E)
    lzs = lz[::100]
    return float(np.trapz(integrand, lzs) / H0 / GYR)


def F_slow(z, lam, scale_density=True):
    rho = RHO500_0 * (E(z) ** 2 if scale_density else 1.0)
    tau = (t_age(z) - T2) * GYR
    return 1.0 - math.exp(-lam * math.sqrt(4 * math.pi * G * rho) * tau)


T2 = t_age(2.0)

# ======================= G0: data inventory ==========================================================
say(f"CFG436 CHEX-MATE z-slope (T16 discriminator)   MUTATE={MUT}")
say("\nG0 data gate: per-cluster CHEX-MATE table with z, M500 and M_gas,500 (>= 30 clusters)?")
gas_pat = re.compile(r"M_\{?\\(?:rm|mathrm)\{?\s*gas|M_\{?gas|M_\{?\\rm g[,}]|M_\{\\rm g\}|f_\{?\\(?:rm|mathrm)\{?\s*gas|gas\s+mass|M_\{?\\mathrm\{g\}", re.I)
inv = []
for tex in sorted(glob.glob(os.path.join(DATA, "src_*", "**", "*.tex"), recursive=True)):
    txt = "\n".join(l.split("%")[0] if not l.lstrip().startswith("%") else "" for l in open(tex, errors="ignore").read().splitlines())
    for m in re.finditer(r"\\begin\{(table\*?|longtable)\}(.*?)\\end\{\1\}", txt, re.S):
        body = m.group(2)
        rows = [r for r in body.split("\\\\") if r.count("&") >= 2]
        tabular = body.split("\\caption")[0] if "\\begin{tabular" in body else body
        gas_col = bool(gas_pat.search(re.sub(r"\\caption\{.*", "", tabular, flags=re.S)))
        inv.append(dict(file=os.path.relpath(tex, DATA), rows=len(rows), gas_column=gas_col))
# \input{} tables (overview paper) count as tables too
for tex in sorted(glob.glob(os.path.join(DATA, "src_2010.11972", "master_*.tex"))):
    t = open(tex).read()
    rows = [r for r in t.split("\\\\") if r.count("&") >= 5 and "PSZ2" in r]
    inv.append(dict(file=os.path.relpath(tex, DATA), rows=len(rows), gas_column=bool(gas_pat.search(t.splitlines()[0]))))
qual = [i for i in inv if i["gas_column"] and i["rows"] >= 30]
say(f"  scanned {len(inv)} tables in {len(set(i['file'] for i in inv))} files; tables with a gas-mass column: "
    f"{[ (i['file'], i['rows']) for i in inv if i['gas_column']]}")
stmt_file = os.path.join(DATA, "src_2609.09144", "data.tex")
stmt = "no gas fraction measurements or individual three-dimensional electron density profiles have been obtained for the CHEX-MATE clusters"
has_stmt = stmt in open(stmt_file).read().replace("\n", " ")
say(f"  arXiv 2609.09144 (Sept 2026) states 'no gas fraction measurements ... obtained for the CHEX-MATE clusters': {has_stmt}")
G0 = bool(qual)
say(f"  G0 {'PASS' if G0 else 'FAIL'} -> PRIMARY verdict: {'(run)' if G0 else 'NOT POSSIBLE'}")
res["G0"] = dict(pass_=G0, inventory=inv, statement_found=has_stmt)

# ======================= z distribution of the full sample (forecast) =================================
zs = []
for tex in sorted(glob.glob(os.path.join(DATA, "src_2010.11972", "master_*b.tex"))):
    for r in open(tex).read().split("\\\\"):
        if "PSZ2" in r and r.count("&") >= 5:
            zs.append(float(r.split("&")[3]))
zs = np.array(zs)
say(f"\nCHEX-MATE overview tables: {len(zs)} clusters, z {zs.min():.3f}-{zs.max():.3f}, median {np.median(zs):.3f}, std {zs.std():.3f}")

# ======================= registered predictions ========================================================
say("\nRegistered predictions (T16): saturation x(z)/x(ref) = 1; slow-rate F(z)/F(ref), tau = t(z) - t(2)")
say(f"  t(0) = {t_age(0):.2f} Gyr, t(2) = {T2:.2f} Gyr -> tau(0) = {t_age(0)-T2:.2f} Gyr (T16: 10.3)")
pred = {}
for k, lam in LAMS.items():
    p = {}
    for scl in (True, False):
        r34 = F_slow(0.430, lam, scl) / F_slow(0.234, lam, scl)
        r_full = F_slow(0.6, lam, scl) / F_slow(0.05, lam, scl)
        zg = np.linspace(0.05, 0.6, 23)
        slope = float(np.polyfit(zg, np.log([F_slow(z, lam, scl) for z in zg]), 1)[0])
        p["Escaled" if scl else "fixed_rho"] = dict(R34=r34, R_06_005=r_full, dlnx_dz=slope)
    pred[k] = p
    say(f"  lam {lam:.4f} ({k}): R(bin4/bin3) = {p['Escaled']['R34']:.3f} [fixed-rho {p['fixed_rho']['R34']:.3f}];"
        f" x(0.6)/x(0.05) = {p['Escaled']['R_06_005']:.3f}; dlnx/dz = {p['Escaled']['dlnx_dz']:+.3f} [fixed-rho {p['fixed_rho']['dlnx_dz']:+.3f}]")
res["predictions"] = pred
rt0 = math.sqrt(4 * math.pi * G * RHO500_0) * (t_age(0) - T2) * GYR
c3b = bool(np.all(C4.nu_mono(np.logspace(-3, 3, 50)) >= 1))
checks["C3_T16_repro"] = bool(abs(rt0 - 11.74) / 11.74 < 0.03 and c3b)
say(f"  C3: rate x tau(0) = {rt0:.2f} (T16 11.74), nu_mono >= 1: {c3b} -> {'PASS' if checks['C3_T16_repro'] else 'FAIL'}")

# ======================= indicative row: vector-figure extraction =====================================
import fitz  # PyMuPDF
pdf = os.path.join(DATA, "src_2609.09144", "figures", "fgas_measured.pdf")
pg = fitz.open(pdf)[0]
drs = pg.get_drawings()
xt, yt = [], []
for d in drs:
    r = d["rect"]
    if d["color"] == (0.0, 0.0, 0.0) and d.get("fill") is not None and r.x0 < 300:
        if abs(r.width) < 1e-6 and abs(r.height - 6.0) < 0.05 and r.y1 > 270:
            xt.append(r.x0)                         # major x ticks (length 6)
        if abs(r.height) < 1e-6 and abs(r.width - 6.0) < 0.05 and r.x0 < 71:
            yt.append(r.y0)                         # major y ticks
xt, yt = sorted(set(round(v, 3) for v in xt)), sorted(set(round(v, 3) for v in yt))
# x: decades 1e13,1e14,1e15 ; y: 0.200 (top) ... 0.000 (bottom)
xfit = np.polyfit([13, 14, 15], xt, 1)
yfit = np.polyfit(np.linspace(0.2, 0.0, len(yt)), yt, 1)
xres = np.max(np.abs(np.polyval(xfit, [13, 14, 15]) - xt))
yres = np.max(np.abs(np.polyval(yfit, np.linspace(0.2, 0.0, len(yt))) - yt))
X2M = lambda px: 10 ** ((px - xfit[1]) / xfit[0])
Y2F = lambda py: (py - yfit[1]) / yfit[0]
blue = [d for d in drs if d["color"] and tuple(round(c, 3) for c in d["color"]) == (0.0, 0.0, 0.545)
        and d.get("fill") is None and len(d["items"]) == 1 and d["rect"].x0 > 200 and d["rect"].x1 < 300]
hbars = [d["rect"] for d in blue if abs(d["rect"].height) < 1e-6]
vbars = [d["rect"] for d in blue if abs(d["rect"].width) < 1e-6]
pts = []
for h, v in zip(hbars, vbars):   # drawn in pairs, same order
    pts.append(dict(M=X2M(v.x0), M_lo=X2M(h.x0), M_hi=X2M(h.x1), f=Y2F(h.y0), f_hi=Y2F(v.y0), f_lo=Y2F(v.y1)))
checks["C1_figure"] = bool(len(xt) == 3 and len(yt) == 9 and xres < 0.5 and yres < 0.5 and len(pts) == 4)
say(f"\nIndicative row: arXiv 2609.09144 figure fgas_measured.pdf (vector extraction)")
say(f"  calibration: x ticks {xt} (resid {xres:.3f} pt), {len(yt)} y ticks (resid {yres:.3f} pt); CHEX-MATE markers found: {len(pts)}"
    f" -> C1 {'PASS' if checks['C1_figure'] else 'FAIL'}")
for i, p in enumerate(pts):
    say(f"  marker {i+1}: M500c = {p['M']:.3e} [{p['M_lo']:.2e}, {p['M_hi']:.2e}]  f_gas = {p['f']:.4f} [{p['f_lo']:.4f}, {p['f_hi']:.4f}]")
checks["C2_bin12_order"] = bool(len(pts) == 4 and pts[0]["M"] < pts[1]["M"] < min(pts[2]["M"], pts[3]["M"]))
say(f"  C2 (markers 1 < 2 < 3,4 in mass, as bins 1 < 2 < 3,4 in M_SZ): {'PASS' if checks['C2_bin12_order'] else 'FAIL'}")


def x_defA(fgas, M500, z, a0, fstar):
    rhoc = 3 * (H0 * E(z)) ** 2 / (8 * math.pi * G)
    R500 = (3 * M500 * MSUN / (4 * math.pi * 500 * rhoc)) ** (1 / 3)
    Mb = (fgas + fstar) * M500 * MSUN
    gN = G * Mb / R500 ** 2
    nu = float(C4.nu_mono(np.array([gN / a0]))[0])
    return (M500 * MSUN - Mb - (nu - 1) * Mb) / (5.364 * Mb), gN / a0, R500 / (MPC / 1000)


Z3, Z4 = 0.234, 0.430
rng = np.random.default_rng(436)
ND = 20000
lamP = LAMS["PRIMARY_mid"]
Rslow = pred["PRIMARY_mid"]["Escaled"]["R34"]
ind = {}
for asg, (i3, i4) in (("A_draw_order", (2, 3)), ("B_swapped", (3, 2))):
    p3, p4 = dict(pts[i3]), dict(pts[i4])
    s3 = 0.5 * (p3["f_hi"] - p3["f_lo"])
    s4 = 0.5 * (p4["f_hi"] - p4["f_lo"])
    if MUT and asg == "A_draw_order":
        # plant bin 4 so that x4 = Rslow * x3 (canonical a0, central f_star), errors / 10
        x3c = x_defA(p3["f"], p3["M"], Z3, C4.A0["canonical"], FSTAR[0])[0]
        from scipy.optimize import brentq
        p4["f"] = brentq(lambda f: x_defA(f, p4["M"], Z4, C4.A0["canonical"], FSTAR[0])[0] - Rslow * x3c, 0.02, 0.5)
        s3, s4 = s3 / 10, s4 / 10
        say(f"  *** MUTATE: bin-4 f_gas planted at {p4['f']:.4f}, errors / 10 ***")
    for foot in C4.FOOTS:
        a0 = C4.A0[foot]
        for fs_lab, fs in (("fstar0.012", FSTAR[0]), ("fstar0.008", FSTAR[1]), ("fstar0.016", FSTAR[2])):
            x3, y3, R3 = x_defA(p3["f"], p3["M"], Z3, a0, fs)
            x4, y4, R4 = x_defA(p4["f"], p4["M"], Z4, a0, fs)
            f3d = rng.normal(p3["f"], s3, ND)
            f4d = rng.normal(p4["f"], s4, ND)
            Rd = np.array([x_defA(a, p4["M"], Z4, a0, fs)[0] / x_defA(b, p3["M"], Z3, a0, fs)[0]
                           for a, b in zip(f4d[:4000], f3d[:4000])])
            Robs, sR = x4 / x3, float(np.std(Rd))
            powr = abs(1 - Rslow) >= 2 * sR
            if not powr:
                v = "NON-DIAGNOSTIC"
            else:
                dS, dR = abs(Robs - 1) / sR, abs(Robs - Rslow) / sR
                v = ("FAVOURS SATURATION" if dS <= 2 and dR > 3 else "FAVOURS SLOW-RATE" if dR <= 2 and dS > 3
                     else "NEITHER" if dS > 3 and dR > 3 else "INCONCLUSIVE")
            ind[f"{asg}|{foot}|{fs_lab}"] = dict(x3=x3, x4=x4, y3=y3, y4=y4, R500_3=R3, R500_4=R4, R_obs=Robs, sigma_R=sR,
                                                R_slow=Rslow, power=bool(powr), verdict=v)
say(f"\n  Indicative R = x(bin4, z {Z4})/x(bin3, z {Z3}); slow-rate R_slow = {Rslow:.3f} (lam {lamP:.4f}), saturation 1")
for k, v in ind.items():
    say(f"  {k:36s} x3 {v['x3']:.3f} x4 {v['x4']:.3f} (y {v['y3']:.2f}/{v['y4']:.2f})  R_obs {v['R_obs']:.3f} +- {v['sigma_R']:.3f}"
        f"  power {'ok' if v['power'] else 'NO'} -> {v['verdict']}")
vA = {v["verdict"] for k, v in ind.items() if k.startswith("A_") and "fstar0.012" in k}
vB = {v["verdict"] for k, v in ind.items() if k.startswith("B_") and "fstar0.012" in k}
if vA != vB or len(vA) > 1:
    ind_head = f"NOT POSSIBLE (verdict depends on the unlabelled bin assignment: A {sorted(vA)}, B {sorted(vB)})"
else:
    ind_head = vA.pop()
say(f"  INDICATIVE ROW: {ind_head}")
res["indicative"] = dict(rows=ind, headline=ind_head, R_slow=Rslow)

# ======================= forecast ======================================================================
say("\nForecast for a per-cluster CHEX-MATE test (if a table existed):")
fc = {}
sz = float(zs.std())
for k in ("win_lo", "PRIMARY_mid", "win_hi", "MW_floor"):
    sl = pred[k]["Escaled"]["dlnx_dz"]
    for sig in (0.3, 0.5):
        s_slope = sig / (math.sqrt(len(zs)) * sz)
        fc[f"{k}|sig{sig}"] = dict(pred_slope=sl, sigma_slope=s_slope, signif=abs(sl) / s_slope)
    say(f"  lam {LAMS[k]:.4f}: predicted dlnx/dz {sl:+.3f}; {len(zs)} clusters, std z {sz:.3f}: sigma(slope) = "
        f"{fc[f'{k}|sig0.3']['sigma_slope']:.3f} (scatter 0.3) / {fc[f'{k}|sig0.5']['sigma_slope']:.3f} (0.5) -> "
        f"{fc[f'{k}|sig0.3']['signif']:.1f} / {fc[f'{k}|sig0.5']['signif']:.1f} sigma")
# hydrostatic-bias drift: dlnx/dlnM_tot at fixed M_b ~ M_tot/(M_tot - M_b - M_ph); use bin-3 numbers
v0 = ind["A_draw_order|canonical|fstar0.012"]
amp = (1 / (pts[2]["f"] + FSTAR[0])) / (5.364 * v0["x3"])
slP = abs(pred["PRIMARY_mid"]["Escaled"]["dlnx_dz"])
db_max = 0.5 * slP * 0.55 / amp      # drift in ln(1-b) over dz = 0.55 that mimics half the slope
say(f"  bias amplification dlnx/dln M_tot = {amp:.2f}; a drift in ln(1-b) of {db_max:.3f} over z 0.05-0.6 fakes half the PRIMARY slope")
fc["bias_amp"] = amp
fc["max_ln1mb_drift"] = db_max
res["forecast"] = fc

prim = "NOT POSSIBLE" if not G0 else "(not run)"
say(f"\nPRIMARY VERDICT (T16 z-slope on CHEX-MATE): {prim}")
if not G0:
    say("  missing: per-cluster M_gas,500 (or f_gas) and a total mass (HSE / WL / dynamical) on one footing for the CHEX-MATE"
        " clusters; the collaboration's per-cluster gas products are not public (the Sept-2026 BFC paper says none exist).")
res["primary_verdict"] = prim
res["checks"] = checks
say("\nchecks: " + json.dumps(checks))
if MUT:
    det = ind["A_draw_order|canonical|fstar0.012"]["verdict"] == "FAVOURS SLOW-RATE"
    say(f"MUTATE detected (planted slow-rate bin 4, errors/10 -> FAVOURS SLOW-RATE under A): {det}")
    res["mutate_detected"] = bool(det)
print("\n".join(OUT))
json.dump(res, open(os.path.join(HERE, f"cfg436_results{TAG}.json"), "w"), indent=1, default=float)
if MUT:
    sys.exit(1 if res["mutate_detected"] else 0)
sys.exit(0 if all(checks.values()) else 1)
