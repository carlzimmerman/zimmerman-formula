"""CFG89 -- see cfg89_FROZEN_docstring.txt (frozen before any run; sha256 printed below). MUTATE=1 -> v_obs x 0.5; MUTATE=nu1 -> Newtonian kernel."""
import sys, os, json, hashlib, warnings
warnings.filterwarnings('ignore')
import numpy as np
from scipy.integrate import quad
from scipy.special import ellipk
from scipy.optimize import brentq
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from cfg89_lib import *
from cfg89_lib import _mean_stats

HERE = os.path.dirname(os.path.abspath(__file__))
MUT = os.environ.get("MUTATE", "")
tag = {"": "main", "1": "MUTATE", "nu1": "MUTATE_nu1"}[MUT]
out = open(f"{HERE}/cfg89_{tag}.out", "w")
def P_(*a):
    s = " ".join(str(x) for x in a); print(s); out.write(s + "\n")
P_("frozen docstring sha256:", hashlib.sha256(open(f"{HERE}/cfg89_FROZEN_docstring.txt", "rb").read()).hexdigest()[:16], " mode:", tag)

D = load(); N = len(D["vmax"])
vfac = 0.5 if MUT == "1" else 1.0
kmain = "newton" if MUT == "nu1" else "mono"
fails = []
def check(name, ok, detail):
    P_(("PASS " if ok else "FAIL ") + name + " :: " + detail)
    if not ok: fails.append(name)

# =================== CONTROLS ===================
if not MUT:
    P_("\n== CONTROLS ==")
    # C4 table
    nine = int((D["vmax"] > 340).sum()); i568 = int(np.argmax(D["vmax"]))
    check("C4a table", N == 23 and nine == 9 and D["vmax"][i568] == 568 and D["dv"][i568] == 16 and D["r"][i568] == 41,
          f"N={N}, n(v>340)={nine}, fastest {D['vmax'][i568]}+-{D['dv'][i568]} at {D['r'][i568]} kpc")
    check("C4b Simard vs Ogle", np.all(D["i"] == D["i_s"]) and np.max(np.abs(D["Rd_s"] / D["Rd"] - 1)) < 0.02,
          f"i equal: {np.all(D['i']==D['i_s'])}; max |Rd_S/Rd_O-1| = {np.max(np.abs(D['Rd_s']/D['Rd']-1)):.4f}")
    # C1 Freeman vs direct ring summation
    Rd = 1.0
    def Phi(R):   # potential of exp disc (G=M=Rd=1, Sigma=exp(-R')/(2 pi))
        def f(Rp):
            m = 4 * R * Rp / (R + Rp) ** 2
            return 0.0 if m >= 1 - 1e-15 else (Rp * np.exp(-Rp)) * (2.0 / (R + Rp)) * ellipk(m) / np.pi
        v = 0
        for a, b in [(0, R), (R, 2 * R + 5), (2 * R + 5, 80)]:
            v += quad(f, a, b, limit=400, epsabs=1e-13, epsrel=1e-12)[0]
        return -v
    worst = 0
    for R in [0.5, 1.0, 2.0, 5.0]:
        h = 1e-3 * R
        gr = (Phi(R + h) - Phi(R - h)) / (2 * h)       # g = dPhi/dR (GM/Rd^2 units)
        gf = g_freeman(np.array([R]), np.array([1.0]), np.array([1.0 / G]))[0]
        worst = max(worst, abs(gr / gf - 1))
    check("C1i Freeman vs ring-summation", worst < 5e-3, f"max rel dev over r/Rd=0.5,1,2,5: {worst:.2e}")
    rr = np.linspace(0.5, 5, 2000); vv = g_freeman(rr, 1.0, 1.0 / G) * rr
    rpk = rr[np.argmax(vv)]
    check("C1ii Freeman peak", abs(rpk - 2.15) < 0.03, f"peak at {rpk:.3f} Rd, v^2/(GM/Rd) = {vv.max():.4f}")
    lim = g_freeman(np.array([50.0]), np.array([1.0]), np.array([1.0 / G]))[0] * 50.0 ** 2  # g r^2 /(GM), GM=1
    check("C1iii far limit", abs(lim - 1) < 0.01, f"g r^2/(GM) at 50 Rd = {lim:.5f}")
    xs = 3.7; num = quad(lambda R: 2 * np.pi * R * np.exp(-R) / (2 * np.pi), 0, xs)[0]
    check("C1iv disc enclosed mass", abs(num - (1 - (1 + xs) * np.exp(-xs))) < 1e-8, f"{num:.10f}")
    # C2 Hernquist
    a = 1.7; M = 1.0
    rho = lambda r: M * a / (2 * np.pi * r * (r + a) ** 3)
    r0 = 5.3; num = quad(lambda r: 4 * np.pi * r * r * rho(r), 0, r0, epsabs=1e-13, epsrel=1e-12)[0]
    check("C2i Hernquist enclosed mass", abs(num - M * r0**2 / (r0 + a) ** 2) < 1e-8, f"{num:.10f} vs {M*r0**2/(r0+a)**2:.10f}")
    rr = np.linspace(0.2, 20, 200000) * a; vc2 = rr / (rr + a) ** 2
    check("C2ii Hernquist v_c peak", abs(rr[np.argmax(vc2)] / a - 1) < 1e-3 and abs(vc2.max() * 4 * a - 1) < 1e-6, f"peak at {rr[np.argmax(vc2)]/a:.4f} a, v^2 4a/GM = {vc2.max()*4*a:.7f}")
    rh = brentq(lambda r: r * r / (r + a) ** 2 - 0.5, 0.1, 100)
    check("C2iii Hernquist half-mass", abs(rh / a - (1 + np.sqrt(2))) < 1e-9, f"{rh/a:.9f}")
    def Sig(s):   # projected surface density, a=M=1, s = R/a
        X = np.arccosh(1 / s) / np.sqrt(1 - s * s) if s < 1 else np.arccos(1 / s) / np.sqrt(s * s - 1)
        return (1 / (2 * np.pi * (1 - s * s) ** 2)) * ((2 + s * s) * X - 3)
    # verify closed-form Sigma against numeric line-of-sight projection at s = 0.6, 2.0
    for s in (0.6, 2.0):
        lo = quad(lambda z: 2 * (1 / (2 * np.pi)) / (np.hypot(s, z) * (np.hypot(s, z) + 1) ** 3), 0, np.inf, epsabs=1e-13, epsrel=1e-11)[0]
        assert abs(lo / Sig(s) - 1) < 1e-6, (s, lo, Sig(s))
    Mp = lambda s: quad(lambda t: 2 * np.pi * t * Sig(t), 0, s, points=[1.0] if s > 1 else None, limit=400)[0]
    sre = brentq(lambda s: Mp(s) - 0.5, 0.5, 5)
    check("C2iv R_e = 1.8153 a", abs(sre - 1.8153) < 1e-3, f"projected half-mass radius = {sre:.5f} a")
    # C3 units + kernels
    v = np.sqrt(G * 1e11 * MSUN / (10 * KPC)) / 1e3
    check("C3a units", abs(v - 207.0) < 0.5, f"{v:.2f} km/s")
    yy = np.linspace(1e-4, YP, 5000)
    check("C3b mono==RAR (y<=y_p), continuity, peak", np.max(np.abs(nu_mono(yy) / nu_rar(yy) - 1)) < 1e-12 and abs(nu_mono(YP*(1+1e-9)) / nu_mono(YP*(1-1e-9)) - 1) < 1e-8 and abs(YP - 2.54) < 0.01 and abs(HP - 0.6476) < 5e-4,
          f"y_p={YP:.4f}, h_p={HP:.5f}")
    check("C3c nu(1)", abs(nu_mono(1.0) - 1.582) < 1e-3 and abs(nu_p2(1.0) - 2 ** 0.5) < 1e-12, f"mono {float(nu_mono(1.0)):.4f}, P2 {float(nu_p2(1.0)):.4f}")

# =================== MAIN ===================
P40 = {"model": "disc", "Rd_src": "ogle"}
P56 = {"model": "bulge", "Rd_src": "simard"}
def line(tag, s):
    return f"{tag:34s} mean {s['mean']:+.4f} +- {s['sig']:.4f} ({s['z']:+.2f}s) [sem {s['sem']:.4f}, floor {s['floor'][3]:.4f}: model {s['floor'][0]:.4f} M* {s['floor'][1]:.4f} gas {s['floor'][2]:.4f}] | slope {s['slope']:+.3f} +- {s['slope_se']:.3f} ({s['slope_z']:+.2f}s) | nine ({s['n9']}) {s['m9']:+.4f} +- {s['sig9']:.4f} ({s['z9']:+.2f}s) [sem9 {s['sem9']:.4f}] | H1 {'PASS' if s['H1'] else 'FAIL'} H2 {'PASS' if s['H2'] else 'FAIL'}"
R = {}
P_("\n== MAIN (frozen): kernel", kmain, "==")
for foot in ("canonical", "alt"):
    R[f"c40_{foot}"] = summary(D, P40, kmain, foot, "disc", vfac=vfac)
    R[f"c56_{foot}"] = summary(D, P56, kmain, foot, "bulge", vfac=vfac)
    P_(line(f"CFG40-model {foot}", R[f"c40_{foot}"]))
    P_(line(f"CFG56-model {foot}", R[f"c56_{foot}"]))
s56 = R["c56_canonical"]; s40 = R["c40_canonical"]
P_(f"\nCFG56-model: mean on galaxy scatter alone = {s56['mean']:.4f}/{s56['sem']:.4f} = {s56['z_scatter']:.2f} sigma;   CFG40-model: {s40['mean']:.4f}/{s40['sem']:.4f} = {s40['z_scatter']:.2f} sigma")
P_(f"std of offsets: CFG56 {s56['off'].std(ddof=1):.4f}, CFG40 {s40['off'].std(ddof=1):.4f};  y=g_N/a0 range {s56['y'].min():.2f}..{s56['y'].max():.2f}; n(y>y_p)={int((s56['y']>YP).sum())}")

# C5 disc-only control and bulge-model B/T=0
if not MUT:
    z0 = summary(D, {**P56, "Rd_src": "ogle", "BT_override": np.zeros(N)}, "mono", "canonical", "bulge")
    check("C5a B/T=0 (Ogle Rd) == CFG40-model mean", abs(z0["mean"] - s40["mean"]) < 1e-9, f"{z0['mean']:+.10f} vs {s40['mean']:+.10f}")
    z1 = summary(D, {**P56, "BT_override": np.zeros(N)}, "mono", "canonical", "bulge")
    check("C5b B/T=0 (Simard Rd) within 1e-3 of CFG40-model", abs(z1["mean"] - s40["mean"]) < 1e-3, f"{z1['mean']:+.5f} vs {s40['mean']:+.5f}")
    P_(line("disc-only, Simard Rd, B/T=0", z1))
    # BT consistency
    BTm = 10 ** (-0.4 * D["rb"]) / (10 ** (-0.4 * D["rb"]) + 10 ** (-0.4 * D["rd"]))
    P_(f"S2: B/T from rbMag/rdMag vs table B/T_r: max |diff| = {np.max(np.abs(BTm - D['BT'])):.3f}; median {np.median(BTm-D['BT']):+.3f}")

# reproduction table
if not MUT:
    P_("\n== REPRODUCTION vs README targets (tolerance 0.0015 dex / 0.05 sigma) ==")
    kp = "mono"
    def rep(label, mine, target, tol):
        ok = abs(mine - target) <= tol
        P_(f"{'REPRODUCED' if ok else 'DIFFERS   '} {label:52s} mine {mine:+.4f}  README {target:+.4f}  diff {mine-target:+.4f}")
    a = R["c40_canonical"]; b = R["c40_alt"]; c = R["c56_canonical"]; d = R["c56_alt"]
    rep("T1 CFG40 canonical mean", a["mean"], 0.107, 0.0015); rep("T1 CFG40 canonical mean err (total)", a["sig"], 0.075, 0.0015); rep("T1 CFG40 z(mean)", a["z"], 1.42, 0.05)
    rep("T1 CFG40 slope", a["slope"], 0.194, 0.0015); rep("T1 CFG40 slope err", a["slope_se"], 0.100, 0.0015)
    rep("T1 CFG40 nine", a["m9"], 0.170, 0.0015); rep("T1 CFG40 z(nine)", a["z9"], 2.06, 0.05)
    rep("T1 CFG40 alt mean", b["mean"], 0.092, 0.0015); rep("T1 CFG40 alt err", b["sig"], 0.074, 0.0015); rep("T1 CFG40 alt nine", b["m9"], 0.156, 0.0015); rep("T1 CFG40 alt z(nine)", b["z9"], 1.92, 0.05)
    pm = summary(D, {"model": "point", "Rd_src": "ogle"}, kp, "canonical", "disc"); sp = summary(D, {"model": "sph", "Rd_src": "ogle"}, kp, "canonical", "disc")
    rep("T1 point mean", pm["mean"], 0.059, 0.0015); rep("T1 point nine", pm["m9"], 0.113, 0.0015); rep("T1 sph mean", sp["mean"], 0.141, 0.0015); rep("T1 sph nine", sp["m9"], 0.201, 0.0015)
    asy = summary(D, {**P40, "asym": True}, kp, "canonical", "disc")
    rep("T1 asymptotic mean", asy["mean"], 0.144, 0.0015); rep("T1 asymptotic nine", asy["m9"], 0.191, 0.0015)
    rep("T2 CFG56 canonical mean", c["mean"], 0.105, 0.0015); rep("T2 CFG56 mean err (total)", c["sig"], 0.063, 0.0015); rep("T2 CFG56 z(mean)", c["z"], 1.67, 0.05)
    rep("T2 CFG56 slope", c["slope"], 0.166, 0.0015); rep("T2 CFG56 slope err", c["slope_se"], 0.092, 0.0015); rep("T2 CFG56 z(slope)", c["slope_z"], 1.80, 0.05)
    rep("T2 CFG56 nine", c["m9"], 0.164, 0.0015); rep("T2 CFG56 z(nine)", c["z9"], 2.34, 0.05)
    rep("T2 CFG56 alt mean", d["mean"], 0.090, 0.0015); rep("T2 CFG56 alt slope", d["slope"], 0.165, 0.0015); rep("T2 CFG56 alt nine", d["m9"], 0.149, 0.0015); rep("T2 CFG56 alt z(nine)", d["z9"], 2.17, 0.05)
    rep("T2 CFG56 model floor term", c["floor"][0], 0.001, 0.0015); rep("T2 CFG40 model floor term", a["floor"][0], 0.041, 0.0015); rep("T2 CFG56 M* term", c["floor"][1], 0.059, 0.0015)
    rep("T2 5.8 sigma on galaxy scatter alone", c["z_scatter"], 5.8, 0.05)
    p2c = summary(D, P56, "p2", "canonical", "bulge"); p2d = summary(D, P40, "p2", "canonical", "disc")
    rep("T3 P2 CFG56 mean", p2c["mean"], 0.132, 0.0015); rep("T3 P2 CFG56 z(mean)", p2c["z"], 2.06, 0.05); rep("T3 P2 CFG56 z(nine)", p2c["z9"], 2.69, 0.05)
    rep("T3 P2 CFG40 mean", p2d["mean"], 0.134, 0.0015); rep("T3 P2 CFG40 z(mean)", p2d["z"], 1.75, 0.05); rep("T3 P2 CFG40 z(nine)", p2d["z9"], 2.35, 0.05)
    rar = summary(D, P56, "rar", "canonical", "bulge")
    P_(f"RAR vs mono (CFG56 model): max |offset diff| = {np.max(np.abs(rar['off']-c['off'])):.2e}; mean {rar['mean']:+.5f} vs {c['mean']:+.5f}; nine {rar['m9']:+.5f} vs {c['m9']:+.5f}")
    P_(line("P2 CFG56-model canonical", p2c)); P_(line("P2 CFG40-model canonical", p2d))
    P_(f"V1 verdicts (mono, canonical): H1 {'PASS' if c['H1'] else 'FAIL'} (frozen PASS), H2 {'PASS' if c['H2'] else 'FAIL'} (frozen FAIL); clause z: mean {c['z']:.2f}, slope {c['slope_z']:.2f}, nine {c['z9']:.2f}; under P2 H1 {'PASS' if p2c['H1'] else 'FAIL'} (frozen FAIL)")

# ------ MUTATE bite
if MUT:
    P_("\n== MUTATE verdict: H1 and H2 must both FAIL ==")
    if MUT == "1":
        check("C6 MUTATE=1 H1 fails", not s56["H1"], f"z={s56['z']:+.2f}")
        check("C6 MUTATE=1 H2 fails", not s56["H2"], f"clauses: mean {s56['z']:+.2f}, slope {s56['slope_z']:+.2f}, nine {s56['z9']:+.2f}")
    else:
        check("C6b MUTATE=nu1 mean > +0.15 and H1 fails", s56["mean"] > 0.15 and not s56["H1"], f"mean {s56['mean']:+.3f} z={s56['z']:+.2f}")

# =================== SENSITIVITIES ===================
if not MUT:
    P_("\n== SENSITIVITY (CFG56 model, mono, canonical unless stated; columns: mean(z) | slope(z) | nine(z) | floor) ==")
    SENS = {}
    def sens(label, P=None, **kw):
        PP = {**P56, **(P or {})}
        kind = kw.pop("kind", "bulge")
        s = summary(D, PP, kw.pop("kern", "mono"), kw.pop("foot", "canonical"), kind, **kw)
        SENS[label] = {k: float(s[k]) for k in ("mean", "z", "slope", "slope_z", "m9", "z9", "sem", "sem9")} | {"floor": s["floor"][3]}
        P_(f"{label:44s} {s['mean']:+.3f} ({s['z']:+.2f}) | {s['slope']:+.3f} ({s['slope_z']:+.2f}) | {s['m9']:+.3f} ({s['z9']:+.2f}) | fl {s['floor'][3]:.3f}  H1 {'P' if s['H1'] else 'F'} H2 {'P' if s['H2'] else 'F'}")
        return s
    P_("-- S1 disc scale length / radius / bulge scale")
    sens("headline (Simard Rd)"); sens("Ogle Rd", {"Rd_src": "ogle"})
    sens("Rd x0.8", {"Rdscale": 0.8}); sens("Rd x1.25", {"Rdscale": 1.25}); sens("Rd capped 25 kpc", {"Rdcap": 25.0})
    sens("Rd = Rhl/1.678", {"Rd_src": "rhl"}); sens("2MFGC 08638 Rd -> 20 kpc", {"Rd_override": {4: 20.0}})
    sens("r x0.9", {"rscale": 0.9}); sens("r x1.1", {"rscale": 1.1}); sens("bulge scale x0.5", {"bscale": 0.5}); sens("bulge scale x2", {"bscale": 2.0})
    P_("-- S2 B/T")
    sens("B/T + 0.10", {"dBT": 0.10}); sens("B/T - 0.10", {"dBT": -0.10}); sens("B/T x0.5", {"BTscale": 0.5}); sens("B/T x2", {"BTscale": 2.0})
    for q in (1.25, 1.5, 2.0): sens(f"bulge M/L x{q} (total M* fixed)", {"q": q})
    sens("bulge as point mass", {"bulge_point": True}); sens("no bulge (B/T=0, Simard Rd)", {"BT_override": np.zeros(N)})
    P_("-- S3 M/L, gas")
    for d in (-0.2, -0.1, 0.1, 0.2): sens(f"M* x10^{d:+.1f}", {"dMs": d})
    sens("gas x0", {"gasfac": 0.0}); sens("gas x2", {"gasfac": 2.0})
    P_("-- S4 inclination")
    sens("i + 5 deg (v_obs -> v sin i/sin(i+5))", incl=5.0); sens("i - 5 deg", incl=-5.0)
    base = summary(D, P56, "mono", "canonical", "bulge")
    hi = np.where(D["i"] > 80)[0]; lo = np.where(D["i"] < 50)[0]
    keep = np.array([k for k in range(N) if D["i"][k] <= 80]); sens(f"drop i>80 (n={len(hi)})", idx=keep)
    keep = np.array([k for k in range(N) if D["i"][k] >= 50]); sens(f"drop i<50 (n={len(lo)})", idx=keep)
    P_(f"corr(offset, i) = {np.corrcoef(base['off'], D['i'])[0,1]:+.3f};  corr(offset, r/Rd) = {np.corrcoef(base['off'], D['r']/D['Rd_s'])[0,1]:+.3f};  corr(offset, B/T) = {np.corrcoef(base['off'], D['BT'])[0,1]:+.3f}")
    sv = np.hypot(D["dv"] / (D["vmax"] * np.log(10)), np.abs(1 / np.tan(np.radians(D["i"]))) * np.radians(5) / np.log(10))
    P_(f"per-galaxy v+inclination errors (dex): median {np.median(sv):.4f}, max {sv.max():.4f} ({D['name'][int(np.argmax(sv))]}); added stat term on 23-mean sqrt(sum sig^2)/N = {np.sqrt((sv**2).sum())/N:.4f} -> sem {np.hypot(base['sem'], np.sqrt((sv**2).sum())/N):.4f}")
    P_("-- S7 kernel / footing / a0")
    for k in ("mono", "rar", "p2"):
        for f in ("canonical", "alt"): sens(f"kernel {k} {f}", kern=k, foot=f)
    sens("a0 x0.99", {"a0fac": 0.99}); sens("a0 x1.01", {"a0fac": 1.01}); sens("asymptotic v^4=GMa0", {"asym": True})

    # ---- S5 leave-one-out
    P_("\n-- S5 leave-one-out (full recompute incl. floor / floor fixed)")
    b = base
    P_(f"{'dropped':30s} {'v':>4s} {'off':>7s} | 23-mean z (drop) | slope z | nine z (8 or 9, floor recomputed) | nine z (floor fixed)")
    rows = []
    for k in range(N):
        idx = np.array([j for j in range(N) if j != k])
        s = summary(D, P56, "mono", "canonical", "bulge", idx=idx)
        sf = summary(D, P56, "mono", "canonical", "bulge", idx=idx, fixed_floor=b["floor"])
        rows.append((D["name"][k], D["vmax"][k], b["off"][k], s["z"], s["slope_z"], s["z9"], sf["z9"], s["m9"], sf["sig9"]))
    for r in sorted(rows, key=lambda r: r[5]):
        star = "*" if r[1] > 340 else " "
        P_(f"{r[0][:28]:30s}{star}{r[1]:4.0f} {r[2]:+7.3f} | {r[3]:+.2f} | {r[4]:+.2f} | {r[5]:+.2f} (mean {r[7]:+.3f}) | {r[6]:+.2f}")
    P_(f"(base: mean z {b['z']:+.2f}, slope z {b['slope_z']:+.2f}, nine z {b['z9']:+.2f}; * = one of the nine; dominant = drop moves the nine z by > 0.3)")
    dom = [r[0] for r in rows if r[1] > 340 and abs(r[5] - b["z9"]) > 0.3]
    P_("dominant members of the nine (>0.3 sigma move):", dom if dom else "none")
    # drop pairs among nine (which two pairs minimise the significance)
    import itertools
    nn = [k for k in range(N) if D["vmax"][k] > 340]
    prs = []
    for pr in itertools.combinations(nn, 2):
        idx = np.array([j for j in range(N) if j not in pr]); s = summary(D, P56, "mono", "canonical", "bulge", idx=idx)
        prs.append((s["z9"], s["m9"], [D["name"][j][-14:] for j in pr]))
    prs.sort(); P_("lowest nine-clause z after dropping two of the nine:", [(round(a, 2), round(m, 3), n) for a, m, n in prs[:3]])
    fl9 = floor_terms(D, P56, "mono", "canonical", "bulge", np.array(nn))
    P_(f"floor recomputed on the nine's own mean: model {fl9[0]:.4f} M* {fl9[1]:.4f} gas {fl9[2]:.4f} total {fl9[3]:.4f} -> nine z = {b['m9']/np.hypot(b['sem9'], fl9[3]):+.2f} (headline uses the 23-sample floor {b['floor'][3]:.4f}: {b['z9']:+.2f})")
    P_("offsets of the nine (name, v, r, offset, y=g_N/a0):")
    for k in sorted(nn, key=lambda j: -D["vmax"][j]): P_(f"   {D['name'][k]:28s} {D['vmax'][k]:4.0f} r={D['r'][k]:4.0f} kpc  off {b['off'][k]:+.3f}  y {b['y'][k]:.2f}  B/T {D['BT'][k]:.2f}  Rd {D['Rd_s'][k]:.1f}")

    # ---- S6 selection
    P_("\n-- S6 selection on the outcome")
    off = b["off"]; lvp = np.log10(b["vp"]); lvo = np.log10(D["vmax"])
    def top9(key): return np.argsort(-key)[:9]
    for lab, key in (("nine largest v_obs (headline)", D["vmax"]), ("nine largest v_pred (law)", b["vp"]), ("nine largest M_b", b["Mb"]), ("nine largest r", D["r"]), ("nine largest r/Rd", D["r"] / D["Rd_s"] * -1)):
        idx9 = top9(key); m, se = _mean_stats(off, idx9)
        P_(f"{lab:34s} mean {m:+.3f}  sigma(with floor) {np.hypot(se, b['floor'][3]):.3f}  z {m/np.hypot(se, b['floor'][3]):+.2f}  overlap with the fastest nine: {len(set(idx9)&set(top9(D['vmax'])))}")
    rng = np.random.default_rng(89); m9 = off[top9(D["vmax"])].mean()
    perm = np.array([off[rng.choice(N, 9, replace=False)].mean() for _ in range(200000)])
    P_(f"random 9 of 23: mean {perm.mean():+.3f}, sd {perm.std():.3f}; fraction >= the fastest-nine mean {m9:+.3f}: {np.mean(perm>=m9):.4f}; the nine-vs-other-14 gap {m9-off[[j for j in range(N) if j not in top9(D['vmax'])]].mean():+.3f}")
    P_(f"corr(offset, log v_obs) = {np.corrcoef(off, lvo)[0,1]:+.3f}; corr(offset, log v_pred) = {np.corrcoef(off, lvp)[0,1]:+.3f}; corr(offset, log Mb) = {np.corrcoef(off, np.log10(b['Mb']))[0,1]:+.3f}")
    # winner's curse: selection bias of the max of a noisy curve is small next to the scatter
    json.dump({"main": {k: {kk: (vv if not isinstance(vv, (np.ndarray,)) else vv.tolist()) for kk, vv in v.items() if kk not in ("off", "y", "Mb", "vp")} for k, v in R.items()}, "sens": SENS},
              open(f"{HERE}/cfg89_results.json", "w"), default=lambda o: bool(o) if isinstance(o, np.bool_) else float(o), indent=1)

P_("\nCONTROL FAILURES:", fails if fails else "none")
out.close()
sys.exit(1 if fails and not MUT else (0 if not fails else 1))
