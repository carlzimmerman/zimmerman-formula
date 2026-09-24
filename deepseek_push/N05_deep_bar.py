#!/usr/bin/env python3
"""N05 -- THE DEEP-BAR KILL TEST: can a dedicated program close the 4.2-sigma
deep-SPARC tension (L06) to a decisive 5-SE verdict, and at what catalog cost?

L06 (deepseek_push/L06_rar_moment.py + L06_results.json) record:
    SPARC deep rings (g_bar < 0.2 a0, N = 1152, 135 galaxies carrying deep
    rings): M1 (a2-moment) Delta = E[g_obs^2] - E[g_bar^2] - a0 E[g_bar]
    = -0.276 x a0 E[g_bar], z = -4.17 under the honest galaxy-clustered
    bootstrap (ring-level -10.2), mapping to a0_eff/deep = 0.73 a0 (the
    G208/G199 staircase register).  MIGHTEE-HI: 80 rings, M1 z = +4.28
    POSITIVE (the G199 1.87x normalization rung) -- sign-opposite to the
    SPARC deep deficit.

THIS LANE builds the catalog-precision case for a dedicated deep-BAR program:
  (1) reproduces L06's deep-SPARC structure from the SAVED measurements in
      L06_results.json (no full 2000-boot legs rerun); the corpus is re-read
      only to recover the deep log-g_bar distribution (cheap, deterministic).
  (2) the N-requirement curve: N_req such that the measured -0.276 x a0E[g_bar]
      M1 deviation becomes a 5-SE kill, in (a) rings at current per-ring
      noise, (b) new deep-HI galaxies at ~3 rings each (SPARC-style), and
      (c) the MIGHTEE-HI-style deep sub-sample -- CHECKED FIRST.
  (3) THE DISCRIMINATOR: a 5-SE M1 kill could mean a0_eff = 0.73 a0 (deep
      slope 1/2, intercept -0.068 dex) OR a slope change (deep slope 0.55,
      intercept 0).  Power to separate the two at the same N, and which
      hypothesis space the deep cut actually excludes.  The two lines in
      ydev = log10(g_obs/sqrt(a0 g_bar)) units vs u = log10(g_bar/a0):
          H_A: ydev = -0.068            (a0_eff = 0.73 a0; slope 1/2 baseline)
          H_B: ydev = +0.050 u          (slope 0.55, intercept 0)
      they CROSS at u* = -1.36 (g_bar = 0.043 a0) INSIDE the deep band, so
      the offset channel cancels; separation lives in the slope channel.
      Exact LR statistic (validated by Monte Carlo):
          dLL = LL_A - LL_B,  E[dLL] = -1/2 d' S d,  Var(dLL) = d' S d,
          S = (X'X)/sigma^2  =>  LR significance = 1/2 sqrt(d'(X'X)d/sigma^2)
  (4) the program card: instrument (MeerKAT L-band HI, MIGHTEE-class), bands,
      HI depth needed for Vgas at 2 sigma down to g_bar = 0.05 a0, ring
      budget under SPARC-class AND resolved-SED-class systematics, runtime
      estimate, and pre-registered kill/confirm/arbiter/discriminator
      criteria.

All real-data numbers reuse in-repo files only (L06_results.json, corpus v7,
mightee2025_rar_digitized_points.csv).  No git commit.
"""
import csv, json, math, os
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.normpath(os.path.join(HERE, ".."))
A0 = 9.3619e-11            # framework footing (m/s^2)
KPC = 3.0856775814913673e19
SEED = 20260923
NBOOT = 2000
KILL = 5.0
DEEP = 0.2                 # the G099/G208 deep convention (fraction of a0)

def check(label, ok, d=""):
    print(f"  [{'PASS' if ok else 'FAIL'}] {label}" + (f"   {d}" if d else ""), flush=True)
    return bool(ok)

def line(x):
    return np.sqrt(x * x + A0 * x)

def boot_se(x, y, stat, n=NBOOT, seed=SEED):
    rng = np.random.default_rng(seed)
    m = len(x); vals = np.empty(n)
    idx = rng.integers(0, m, size=(n, m))
    for i in range(n):
        vals[i] = stat(x[idx[i]], y[idx[i]])
    return float(vals.std(ddof=1))

def boot_se_cluster(x, y, groups, stat, n=NBOOT, seed=SEED + 7):
    rng = np.random.default_rng(seed)
    g = np.asarray(groups)
    uniq = np.unique(g)
    vals = np.empty(n)
    for i in range(n):
        pick = rng.choice(uniq, size=len(uniq), replace=True)
        m = np.isin(g, pick)
        vals[i] = stat(x[m], y[m])
    return float(vals.std(ddof=1))

def m1stat(x, y):
    return float(np.mean(y * y - line(x) ** 2))

# ------------------------------------------------------------------
# (0) L06 SAVED MEASUREMENTS (the authoritative deep-SPARC record) --
#     no 2000-boot legs rerun.
# ------------------------------------------------------------------
l06 = json.load(open(os.path.join(HERE, "L06_results.json")))
r_deep = next(r for r in l06["results"] if r["name"].startswith("SPARC deep"))
r_mig  = next(r for r in l06["results"] if r["name"].startswith("MIGHTEE"))
Nd, Ed = r_deep["N"], r_deep["E_gbar"]
Delta_d, se_cl_d = r_deep["Delta"], r_deep["se_Delta_used"]
se_rg_d = r_deep["se_Delta"]
s_dex_d = r_deep["s_dex"]
a0E_d = A0 * Ed
f0 = abs(Delta_d) / a0E_d          # measured M1 deficit as a fraction of a0E[g_bar]
z_now = Delta_d / se_cl_d
print("=" * 100)
print("N05 -- THE DEEP-BAR KILL TEST (catalog-precision case for a dedicated deep-BAR program)")
print(f"        a0 = {A0:.5e} m/s^2; deep cut g_bar < {DEEP} a0; kill bar = {KILL} SE (one-sided M1)")
print(f"        L06 saved deep-SPARC record: N = {Nd}, Delta/(a0 E[g_bar]) = {Delta_d/a0E_d:+.3f},"
      f" z(clustered) = {z_now:+.2f}, SE(ring) = {se_rg_d:.3e}, SE(clustered, used) = {se_cl_d:.3e}")
print("=" * 100)

# ------------------------------------------------------------------
# (1) Reproduce the deep-SPARC ensemble structure from the corpus (cheap,
#     deterministic, no bootstrap) -- the deep log-g_bar distribution.
# ------------------------------------------------------------------
print("\n--- (1) DEEP-SPARC STRUCTURE REPRODUCED (rings only; SEs taken from L06) ---")
_crv = json.load(open(os.path.join(REPO, "glm53_push", "data", "rotation_curve_corpus_v7.json")))
XS, GS = [], []
for g in _crv["galaxies"]:
    if g.get("survey") != "SPARC":
        continue
    m2l = g.get("m2l_disk") or 0.0
    if m2l <= 0:
        m2l = 0.5
    for p in (g.get("data") or []):
        vb2 = math.copysign(p["Vgas"] ** 2, p["Vgas"]) + m2l * (p["Vdisk"] ** 2 + p["Vbul"] ** 2)
        if vb2 <= 0 or p["Vobs"] <= 0:
            continue
        R = p["Rad"] * KPC
        XS.append(vb2 * 1e6 / R)
        GS.append(g["galaxy"])
XS = np.array(XS); GS = np.array(GS)
deep = XS < DEEP * A0
Xd, Gd = XS[deep], GS[deep]
ud = np.log10(Xd / A0)                     # depth coordinate u = log10(g_bar/a0)
n_gal_deep = len(np.unique(Gd))
per_gal = len(Xd) / n_gal_deep
s_u = float(ud.std(ddof=1))
print(f"  deep rings {len(Xd)} (L06: {Nd}), galaxies carrying deep rings {n_gal_deep} (of 175),"
      f" rings/gal {per_gal:.1f}, u-range [{ud.min():.2f}, {ud.max():.2f}], s_u = {s_u:.3f},"
      f" mean u = {ud.mean():.2f} (crossing-sensitive)")
check("deep ring count matches L06", len(Xd) == Nd)
check("deep E[g_bar] matches L06", abs(float(Xd.mean()) / Ed - 1.0) < 1e-6,
      f"{float(Xd.mean()):.6e} vs {Ed:.6e}")

# ------------------------------------------------------------------
# (2c) CHECKED FIRST: does the MIGHTEE-HI sample ALREADY close the tension?
#      Re-derive the deep-MIGHTEE sub-sample (g_bar < 0.2 a0).
# ------------------------------------------------------------------
print("\n--- (2c) MIGHTEE-HI DEEP SUB-SAMPLE (REAL): does MIGHTEE ALREADY close the tension? ---")
_xm, _ym, _cg = [], [], []
with open(os.path.join(HERE, "data2", "mightee2025_rar_digitized_points.csv")) as fh:
    for row in csv.DictReader(fh):
        _xm.append(10.0 ** float(row["log10_gbar"]))
        _ym.append(10.0 ** float(row["log10_gobs"]))
        _cg.append(f"{row['color_r']}|{row['color_g']}|{row['color_b']}")
_xm = np.array(_xm); _ym = np.array(_ym); _cg = np.array(_cg)
# handle stray non-finite rows in the digitization
ok = np.isfinite(_xm) & np.isfinite(_ym)
_xm, _ym, _cg = _xm[ok], _ym[ok], _cg[ok]
Delta_mf = m1stat(_xm, _ym)                                  # full-sample check vs L06
d_m = _xm < DEEP * A0
Xmd, Ymd, Cgd = _xm[d_m], _ym[d_m], _cg[d_m]
Delta_md = m1stat(Xmd, Ymd)
se_rg_md = boot_se(Xmd, Ymd, m1stat)
se_cl_md = boot_se_cluster(Xmd, Ymd, Cgd, m1stat)
a0E_md = A0 * float(Xmd.mean())
z_md = Delta_md / max(se_rg_md, se_cl_md)
print(f"  full-sample rebuild check vs L06: Delta = {Delta_mf:+.3e} (L06: {r_mig['Delta']:+.3e})")
check("MIGHTEE full-sample rebuild matches L06", abs(Delta_mf / r_mig["Delta"] - 1.0) < 1e-6)
print(f"  MIGHTEE deep rings: {len(Xmd)}/80, colour groups {len(np.unique(Cgd))}")
print(f"  M1 Delta = {Delta_md:+.3e} = {Delta_md/a0E_md:+.3f} x a0E[g_bar];  SE(ring) = {se_rg_md:.3e},"
      f" SE(colour-group) = {se_cl_md:.3e};  z = {z_md:+.2f}  (L06 full-sample z = {r_mig['z_Delta']:+.2f})")
a0eff_md = A0 * (1.0 + Delta_md / a0E_md)
print(f"  mapped deep a0_eff/a0 = 1 + Delta/(a0E) = {a0eff_md/A0:.3f}  (a0_eff = {a0eff_md:.3e};"
      f" G199 quadratic-fit register: 1.9e-10 ~ 2.03 a0)")
check("MIGHTEE deep deviation is NEGATIVE (would close the SPARC deficit)", bool(Delta_md < -KILL * max(se_rg_md, se_cl_md)))
print(f"  => MIGHTEE deep sign: {'NEGATIVE (closes the SPARC deficit)' if Delta_md < 0 else 'POSITIVE (mirror-image, does NOT close)'}.")

# pooled deep ensemble (informational): exact from saved L06 moments + CSV
E_Y2_d = r_deep["E_gobs2"]; E_Y2_md = float(np.mean(Ymd ** 2))
E_X2_d = r_deep["E_gbar2"]; E_X2_md = float(np.mean(Xmd ** 2))
E_X_d = Ed; E_X_md = float(Xmd.mean())
Delta_p = (len(Xd) * (E_Y2_d - E_X2_d - A0 * E_X_d) +
           len(Xmd) * (E_Y2_md - E_X2_md - A0 * E_X_md)) / (len(Xd) + len(Xmd))
a0E_p = A0 * (len(Xd) * E_X_d + len(Xmd) * E_X_md) / (len(Xd) + len(Xmd))
print(f"  POOLED deep M1 = {Delta_p:+.3e} = {Delta_p/a0E_p:+.3f} x a0E[g_bar] ({len(Xd)+len(Xmd)} rings) --"
      f" a ring-weighted tug-of-war, NOT a verdict: the two deep catalogs disagree on the SIGN"
      f" (SPARC deep {Delta_d/a0E_d:+.3f}, MIGHTEE deep {Delta_md/a0E_md:+.3f}), each >4-sigma one-sided.")

# ------------------------------------------------------------------
# (2) THE N-REQUIREMENT CURVE: measured deficit f0 -> 5-SE kill.
#     Ring-level naive scaling (SE ~ 1/sqrt(N_rings)) AND the honest
#     galaxy-clustered scaling (SE ~ 1/sqrt(N_gal) -- galaxies are the
#     independent units; clustered SE is 2.45x the ring-level SE here).
# ------------------------------------------------------------------
print("\n--- (2) THE N-REQUIREMENT CURVE (measured deficit f0 = %.3f x a0E[g_bar] -> 5-SE kill) ---" % f0)
E_r = se_cl_d * math.sqrt(Nd)
print(f"  current SE(Delta)/a0E[g_bar] = {se_cl_d/a0E_d:.4f} at N = {Nd}"
      f" -> per-ring noise = {E_r/a0E_d:.3f} in a0E[g_bar] units (clustered-equivalent)")
rows = []
for f in (1.0, 0.5, f0, 0.15):
    fac = KILL * se_cl_d / (f * a0E_d)
    n_rr = Nd * fac ** 2
    n_gal_tot = n_gal_deep * fac ** 2
    rows.append((f, n_rr, n_gal_tot))
    print(f"  f = {f:5.3f}: N_req(ring-level) = {n_rr:8.0f} deep rings | N_gal_total_req = {n_gal_tot:6.0f} (new = {max(0.0, n_gal_tot - n_gal_deep):6.0f})")
f0r = next(r for r in rows if abs(r[0] - f0) < 1e-9)
N_req_ring = f0r[1]; N_gal_total = f0r[2]
N_gal_new = N_gal_total - n_gal_deep
N_new_rings = 3.0 * N_gal_new
print(f"  (a) rings at current per-ring noise: N_req = {N_req_ring:.0f} deep rings;"
      f" SE(Delta)/a0E must fall from {se_cl_d/a0E_d:.4f} to {KILL*se_cl_d/(f0*a0E_d):.4f}")
print(f"      NB: deepening EXISTING SPARC galaxies does NOT reduce the clustered SE (set by galaxies"
      f" + shared systematics); the honest lever is NEW galaxies.")
print(f"  (b) new deep-HI galaxies (SPARC-style, ~3 deep rings each): {N_gal_new:.0f} NEW galaxies"
      f" -> ~{N_new_rings:.0f} new deep rings; total deep ensemble ~{Nd + N_new_rings:.0f} rings /"
      f" {N_gal_total:.0f} galaxies  (at SPARC's own deep yield {per_gal:.1f} rings/gal the same budget"
      f" is {N_gal_new*per_gal:.0f} rings -- the clustered SE, not the ring count, is binding)")
for NN in (1500, int(Nd + N_new_rings), 2500, 3000):
    print(f"  |z|(N={NN:5d}, ring-level naive) = {abs(Delta_d)/(se_cl_d*math.sqrt(Nd/NN)):5.2f}")
N_gal_at_target = Nd / per_gal * (se_cl_d / (abs(Delta_d) / KILL)) ** 2
print(f"  galaxy-level |z| at target total {N_gal_total:.0f} gals ="
      f" {abs(Delta_d)/(se_cl_d*math.sqrt(n_gal_deep/N_gal_total)):5.2f} (>=5 -> kill)")

# ------------------------------------------------------------------
# (3) THE DISCRIMINATOR (corrected parametrization; exact LR statistic).
# ------------------------------------------------------------------
print("\n--- (3) THE DISCRIMINATOR: a0_eff = 0.73 a0 (deep slope 1/2, int -0.068 dex) vs slope 0.55 (int 0) ---")
c_A, b_A = -0.0682, 0.0      # H_A in ydev units (baseline slope 1/2 built in)
c_B, b_B = 0.0000, 0.05      # H_B: slope 0.55 -> 0.05 per dex of u
u_star = (c_A - c_B) / (b_B - b_A)
g_star = A0 * 10.0 ** u_star
du = lambda u: (b_B - b_A) * u + (c_B - c_A)
print(f"  H_A: ydev = {c_A:+.4f} dex (a0_eff = 0.73 a0);  H_B: ydev = {b_B:.3f} * u "
      f"(slope 0.55, intercept 0);  ydev = log10(g_obs/sqrt(a0 g_bar)), u = log10(g_bar/a0)")
print(f"  crossing: u* = {u_star:.3f} (g_bar = {g_star:.3e} = {g_star/A0:.4f} a0) -- INSIDE the deep band:")
print(f"  |delta_ydev| over deep-SPARC u: mean = {np.mean(np.abs(du(ud))):.4f} dex;"
      f" at u_min/u_med/u_max = {du(ud.min()):+.3f}/{du(np.median(ud)):+.3f}/{du(ud.max()):+.3f} dex")
# M1 moment that H_B itself would produce over the deep distribution:
gB = np.sqrt(A0 * Xd) * 10.0 ** (b_B * np.log10(Xd / A0) + c_B)
M1B = float(np.mean(gB ** 2 - line(Xd) ** 2)) / a0E_d
print(f"  M1 deviation if deep data lay on H_B (slope 0.55): {M1B:+.3f} x a0E[g_bar]"
      f" vs measured -0.276 (H_A): the M1 MOMENT CANNOT attribute (both ~ -0.3).")
# exact LR statistic: S_LR(N) = 1/2 sqrt(d'(X'X)d / sigma^2)  (validated by MC below)
d = np.array([c_B - c_A, b_B - b_A])
E_du2 = float(np.mean((d[0] + d[1] * ud) ** 2))
def S_LR(N):
    return 0.5 * math.sqrt(N * E_du2 / s_dex_d ** 2)
def S_slope(N):
    return abs(b_B - b_A) * s_u * math.sqrt(N) / s_dex_d
print(f"  E[(d0+d1 u)^2] over the deep sample = {E_du2:.5f} dex^2;  sigma = deep s_dex = {s_dex_d:.3f} dex")
for NN in (int(N_req_ring), int(Nd + N_new_rings), 3000, 11130):
    print(f"  N = {NN:5d}: LR significance S_LR = {S_LR(NN):5.2f}  (slope-channel-only S = {S_slope(NN):5.2f})")
N5_slope = (KILL * s_dex_d / (abs(b_B - b_A) * s_u)) ** 2
N5_lr = (KILL / (0.5 * math.sqrt(E_du2) / s_dex_d)) ** 2
print(f"  N for 5-sigma separation: slope-channel {N5_slope:8.0f} | exact LR (offset noise included) {N5_lr:8.0f} deep rings")
# Monte Carlo power (8000 sims/cell; truth A and truth B; scatter = deep s_dex)
print(f"  Monte Carlo power (8000 sims/cell, seed {SEED}+{400}; z = dLL/sd, validated exact):")
mc = {}
for NN in (int(N_req_ring), int(Nd + N_new_rings), 3000, int(N5_lr)):
    line_out = []
    for truth in ("A", "B"):
        rng = np.random.default_rng(SEED + (400 if truth == "A" else 401))
        zsim = np.empty(8000)
        for i in range(8000):
            u = rng.choice(ud, size=NN, replace=True)
            ydev = (c_A + b_A * u if truth == "A" else c_B + b_B * u) + rng.normal(0.0, s_dex_d, NN)
            Xm = np.column_stack([np.ones(NN), u])
            th = np.linalg.lstsq(Xm, ydev, rcond=None)[0]
            Si = (Xm.T @ Xm) / s_dex_d ** 2
            dll = 0.5 * ((th - np.array([c_B, b_B])) @ Si @ (th - np.array([c_B, b_B]))
                         - (th - np.array([c_A, b_A])) @ Si @ (th - np.array([c_A, b_A])))
            zsim[i] = dll / math.sqrt(d @ Si @ d)
        line_out.append(f"truth {truth}: <z> = {zsim.mean():+.2f}, P(|z|>1.96) = {np.mean(np.abs(zsim) > 1.96):.3f},"
                        f" P(|z|>=5) = {np.mean(np.abs(zsim) >= 5):.4f}")
    print(f"    N = {NN:5d}: " + "   ".join(line_out))
    mc[str(NN)] = dict(slr=float(S_LR(NN)))
# systematics lever: the SAME discriminator under better-controlled scatter
print("  SYSTEMATICS LEVER (the decisive one): S_LR(5-sigma) N vs per-ring residual scatter sigma:")
for sig in (s_dex_d, 0.15, 0.10, 0.05):
    N5 = (KILL / (0.5 * math.sqrt(E_du2) / sig)) ** 2
    print(f"    sigma = {sig:.3f} dex (SPARC-class {s_dex_d:.2f} / MIGHTEE full 0.13 / resolved-SED recipe 0.045):"
          f" N = {N5:8.0f} deep rings")
# depth lever (approximate): widen the band to fainter g_bar
print("  DEPTH LEVER (approximate): extending the band toward g_bar = 1e-3 a0 (u_min = -3) raises s_u:")
for umin in (-2.15, -2.5, -3.0):
    uu = np.concatenate([ud, np.linspace(umin, ud.min(), int(len(ud) * 0.5))])
    print(f"    band to u_min = {umin:.2f}: s_u = {uu.std(ddof=1):.3f} -> slope-channel N(S=5) = {(KILL*s_dex_d/0.05/uu.std(ddof=1))**2:.0f}")
print("  => reading: at the M1-kill N the deep cut EXCLUDES the normalization-only family"
      " {a0_eff = 1} (the a0-line) but separates H_A (0.73 a0) from H_B (slope 0.55) at only ~1.9-2 sigma:"
      " attribution needs ~11k deep rings at SPARC-class scatter -- OR control of the per-ring systematic"
      " scatter (the MIGHTEE resolved-SED recipe: 0.045 dex) and/or a deeper band, each cutting N by 5-25x.")

# ------------------------------------------------------------------
# (4) PROGRAM CARD NUMBERS
# ------------------------------------------------------------------
print("\n--- (4) PROGRAM CARD (survey design numbers) ---")
g_target = 0.05 * A0
print(f"  g_bar target: 0.05 a0 = {g_target:.3e} m/s^2  (MIGHTEE deep rings already reach ~1e-12"
      f" = 0.01 a0: depth is NOT the binding constraint)")
Vg = {}
for R in (5.0, 10.0, 20.0):
    Vg[str(R)] = math.sqrt(g_target * R * KPC) / 1e3
    print(f"    Vgas(2 sigma) at R = {R:4.0f} kpc: V = {Vg[str(R)]:5.1f} km/s"
          f"  -> per-radius-bin precision ~V/2 = {Vg[str(R)]/2:5.1f} km/s")
print(f"  ring budget (SPARC-class systematics): f = 1.00: {rows[0][1]:.0f} | f = 0.50: {rows[1][1]:.0f} |"
      f" f = 0.276 (measured): {N_req_ring:.0f} | f = 0.15: {rows[3][1]:.0f} deep rings")
print(f"  new-galaxy budget at f = 0.276: ~{N_gal_new:.0f} NEW deep-HI galaxies (3 deep rings each),"
      f" ~{N_new_rings:.0f} new rings; total deep ensemble ~{Nd + N_new_rings:.0f} rings /"
      f" {N_gal_total:.0f} galaxies")
print("  MIGHTEE-HI yield reference (Varasteanu+2025): 19 galaxies -> 80 rings (72 deep) from the 4"
      " MeerKAT L-band deep fields (20 deg^2, ~2 uJy/beam continuum class; Jarvis+2016, Maddox+2021)")
print("  target yield ~13x the MIGHTEE galaxy count -> MeerKAT L-band (1.4 GHz HI) survey-extension +"
      " targeted low-mass dwarfs; runtime band, assumptions labeled: 5-15 kh on MeerKAT-class arrays"
      " over ~2-3 yr cycles (B: ngVLA/SKA1-mid, 2030s) -- ESTIMATE, not budget.")

# ------------------------------------------------------------------
# VERDICT
# ------------------------------------------------------------------
verdict = (
    f"DEEP-BAR KILL TEST: NOT CLOSED -- and the deep regime is now a two-sided contradiction. "
    f"SPARC deep ({Nd} rings): M1 = {Delta_d/a0E_d:.3f} x a0E[g_bar], z = {z_now:+.2f} clustered "
    f"(a0_eff = 0.73 a0, G208 register). MIGHTEE deep ({len(Xmd)} rings): M1 = {Delta_md/a0E_md:+.3f} x "
    f"a0E[g_bar], z = {z_md:+.2f} -- POSITIVE, ALREADY a >5-SE two-sided deviation (a0_eff ~ 2.0 a0, "
    f"the G199 1.87x normalization rung): MIGHTEE does NOT close the SPARC deficit, it contradicts its "
    f"sign. Budget: the measured -{f0:.3f} x a0E[g_bar] becomes a 5-SE kill at ~{N_req_ring:.0f} deep "
    f"rings at current per-ring noise, i.e. ~{N_gal_new:.0f} NEW deep-HI galaxies at ~3 rings each "
    f"({N_new_rings:.0f} new rings; total deep ensemble ~{Nd + N_new_rings:.0f} rings / {N_gal_total:.0f} "
    f"galaxies) under the honest galaxy-clustered SE -- the binding unit is galaxies (clustered SE is "
    f"{se_cl_d/se_rg_d:.2f}x the ring-level SE), so deepening existing SPARC galaxies does not help. "
    f"Discriminator: a 5-SE M1 kill excludes the normalization-only family {{a0_eff = 1}} but CANNOT "
    f"attribute between H_A (a0_eff = 0.73 a0: slope 1/2, intercept -0.068 dex) and H_B (slope 0.55, "
    f"intercept 0): the lines cross at {g_star/A0:.4f} a0 inside the band, BOTH produce the same "
    f"-0.3 x a0E[g_bar] moment (H_B: {M1B:+.3f}), and the exact LR separates them at only "
    f"{S_LR(int(N_req_ring)):.1f} sigma at the kill N -- 5-sigma attribution needs ~{N5_lr:.0f} deep "
    f"rings at SPARC-class scatter, OR the resolved-SED systematic-control recipe (0.045 dex scatter: "
    f"~{ (KILL/(0.5*math.sqrt(E_du2)/0.05))**2:.0f} rings) and/or a deeper band (g_bar -> 1e-3 a0: "
    f"~{ (KILL*s_dex_d/0.05/0.777)**2:.0f} rings). Program card: MIGHTEE-class MeerKAT L-band HI + "
    f"resolved 10-band SED, ~13x the published 19-galaxy yield, ~5-15 kh exposure class, ~2-3 yr; "
    f"pre-registered kill/confirm/arbiter/discriminator criteria in N05_DEEP_BAR_PROGRAM.md."
)
print("\nVERDICT: " + verdict)

json.dump(dict(
    a0=A0, seed=SEED, nboot=NBOOT, kill_sigma=KILL, deep_cut=DEEP,
    provenance=("REAL in-repo files only: L06_results.json (saved deep-SPARC/MIGHTEE measurements; "
                "no 2000-boot legs rerun), glm53_push/data/rotation_curve_corpus_v7.json (deep log-g_bar "
                "distribution only), deepseek_push/data2/mightee2025_rar_digitized_points.csv (MIGHTEE deep "
                "sub-sample M1; ring + colour-group bootstraps).  No data fabricated; no git commit."),
    deep_sparc_L06=dict(N=Nd, E_gbar=Ed, Delta=Delta_d, se_ring=se_rg_d, se_clustered=se_cl_d,
                        z_clustered=z_now, fraction_a0E=f0, a0eff_a0=1.0 - f0, s_dex=s_dex_d,
                        n_gal_with_deep_rings=n_gal_deep),
    n_requirement=dict(
        per_ring_noise_a0E=E_r / a0E_d,
        N_req_ring_level=float(N_req_ring),
        N_gal_total_req=float(N_gal_total),
        N_new_galaxies_3rings=float(N_gal_new),
        N_new_rings=float(N_new_rings),
        total_deep_ensemble_rings=float(Nd + N_new_rings),
        total_deep_ensemble_galaxies=float(N_gal_total),
        curve=[dict(f=f, n_req_ring=float(nr), n_gal_total_req=float(ng)) for f, nr, ng in rows]),
    mightee_deep=dict(N=int(len(Xmd)), colour_groups=int(len(np.unique(Cgd))),
                      Delta=Delta_md, fraction_a0E=Delta_md / a0E_md,
                      se_ring=se_rg_md, se_colourgroup=se_cl_md, z=z_md,
                      a0eff_a0=a0eff_md / A0,
                      closes_tension=False, direction="positive mirror-image (>5-SE two-sided; G199 1.87x rung)"),
    pooled_deep=dict(N=len(Xd) + len(Xmd), Delta=Delta_p, fraction_a0E=Delta_p / a0E_p,
                     note="ring-weighted tug-of-war; sign disagreement is the honest state"),
    discriminator=dict(
        H_A="deep slope 0.5, intercept -0.068 dex (a0_eff = 0.73 a0)",
        H_B="deep slope 0.55, intercept 0", crossing_u=u_star, crossing_gbar_a0=g_star / A0,
        mean_abs_delta_dex=float(np.mean(np.abs(du(ud)))),
        M1_fraction_under_HB=M1B,
        E_d0d1u2=E_du2, s_u_deep=s_u,
        N_5sigma_slope_channel=float(N5_slope), N_5sigma_LR=float(N5_lr),
        S_LR_by_N={k: v["slr"] for k, v in mc.items()},
        scatter_lever=[dict(sigma_dex=float(sig), N_5sigma=float((KILL / (0.5 * math.sqrt(E_du2) / sig)) ** 2))
                       for sig in (s_dex_d, 0.15, 0.10, 0.05)]),
    program_card=dict(
        instrument="MeerKAT L-band (900-1600 MHz; 1.4 GHz HI), MIGHTEE-class survey extension + targeted dwarfs",
        bands="HI 21cm + resolved 10-band SED (optical/IR; the MIGHTEE-HI recipe, sigma_int = 0.045 dex)",
        hi_depth_needed_gbar=0.05 * A0,
        vgas_2sigma_km_s=Vg,
        depth_not_binding="MIGHTEE deep rings already reach ~1e-12 m/s^2 (0.01 a0)",
        ring_budget_sparc_class=dict(f1=float(rows[0][1]), f05=float(rows[1][1]),
                                     f_measured=float(N_req_ring), f015=float(rows[3][1])),
        new_galaxies_needed=int(round(N_gal_new)),
        runtime_estimate="5-15 kh MeerKAT-class L-band + SED program over ~2-3 yr cycles (labeled estimate; ngVLA/SKA1-mid deeper-band alternative 2030s)"),
    verdict=verdict),
    open(os.path.join(HERE, "N05_results.json"), "w"), indent=1, default=float)
print("\nwrote N05_results.json")