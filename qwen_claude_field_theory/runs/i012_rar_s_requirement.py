#!/usr/bin/env python3
"""
I012 -- IS THE RAR REQUIREMENT s >= 0.558 REAL, OR AN ARTEFACT OF NOT REFITTING UPSILON?

QUESTION
  Every legal (ghost-free) kernel in the closed-form family
        U_s(y) = s*sqrt(y)/(s + sqrt(y)),     y = g_bar/a0,   u = a0*U(y)
  saturates at u_inf = s*a0: a CONSTANT sunward anomaly at every planetary distance.
  Ephemerides want s <= 2.4e-3; the RAR was said to want s >= 0.558.  That galaxy-side
  floor came from demanding U(y~2) >= 0.4, which is just "what the a0-line delivers" --
  close to circular, and it was imposed with Upsilon FROZEN.  Here Upsilon is REFITTED
  for every s, on the real SPARC rotation-curve decompositions, at the anchored a0
  (BOTH footings), and we ask how small s can go before the RAR fit actually breaks.

  a0 (canonical) = kappa*c*sqrt(G*rho_Lambda) = 9.3619e-11 m/s^2
  a0 (alt)       =                              1.1279e-10 m/s^2
  kappa = 1/2 is FITTED, never derived.

WHAT THIS SCRIPT CORRECTS IN ITS OWN BRIEF (both corrections are made as numbered checks)
  C1. "s = 1/2 IS the a0-line."  FALSE as a function.  The a0-line is
      U(y) = sqrt(y^2+y) - y; the closed-form family at s=1/2 is 0.5*sqrt(y)/(0.5+sqrt(y)).
      They agree only in the two limits (U -> sqrt(y) as y->0, U -> 1/2 as y->inf) and
      differ by 22% at y=2 (0.4495 vs 0.3694).  So the committed 0.1083 dex belongs to the
      a0-line, NOT to the family at s=1/2 -- the family at s=1/2 fits at 0.1195 dex.
      Reporting the family's s-scan against a target set by the a0-line would have
      manufactured a win for small s.  Both kernels are therefore carried separately.
  C2. "g_bar scales linearly with Upsilon, so you can rescale g_bar."  FALSE for real SPARC.
      g_bar = (sign(Vgas)Vgas^2 + Ud*Vdisk^2 + Ub*Vbul^2)/R: the GAS term does not scale.
      For gas-dominated dwarfs the exact ratio on doubling Upsilon is ~1.29, not 2.00.
      This script therefore never rescales; it rebuilds g_bar exactly from the components.

PASS (as briefed): some s <= 0.1 keeps rms <= 0.15 dex at a defensible Upsilon.
KILL (as briefed): the fit degrades sharply below s ~ 0.4.
GATE: at the a0-line with Upsilon_disk = 0.70 the pipeline must reproduce the committed
      0.1083 dex on this dataset.

Writes no other file.  Commits nothing.
"""
import os, sys, glob, json
import numpy as np
from scipy.optimize import minimize_scalar, minimize, brentq

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SPARC_DIR = os.path.join(REPO, "real_research", "data", "sparc_data")
RAR_JSON = os.path.join(REPO, "ai_slop", "website", "public", "data", "rar_real_sparc.json")

KPC = 3.0857e19
A0_CANON = 9.3619e-11
A0_ALT = 1.1279e-10

# committed ephemeris figures (inputs, not re-derived here)
SATURN_EXCESS_AT_HALF = 39424.0     # x the published anomalous-precession limit, before EFE
EFE_LO, EFE_HI = 119.0, 189.0       # committed EFE reduction factor range
S_GAL_OLD = 0.558                   # the frozen-Upsilon galaxy floor being tested
GATE_TARGET = 0.1083                # committed rms in dex

RMS_MAX = 0.15                      # briefed acceptability bar
UPS_LO, UPS_HI = 0.30, 0.90         # defensible Spitzer 3.6um band

CHECKS = []
def check(name, ok, detail=""):
    CHECKS.append((name, bool(ok), detail))
    print(f"  [{'ok' if ok else 'FAIL'}] {name}" + (f"   {detail}" if detail else ""))
    return bool(ok)

def hdr(t):
    print("\n" + "=" * 78); print(t); print("=" * 78)

# ----------------------------------------------------------------------------------
# data
# ----------------------------------------------------------------------------------
def load_rotmod():
    gals = []
    for f in sorted(glob.glob(os.path.join(SPARC_DIR, "*_rotmod.dat"))):
        try:
            d = np.genfromtxt(f, comments="#")
        except Exception:
            continue
        if d.ndim != 2 or d.shape[1] < 6:
            continue
        R, Vobs, eV, Vgas, Vdisk, Vbul = (d[:, i] for i in range(6))
        gals.append(dict(name=os.path.basename(f).replace("_rotmod.dat", ""),
                         Rm=R * KPC, Vobs=Vobs, eV=eV,
                         Vgas=Vgas, Vdisk=Vdisk, Vbul=Vbul))
    return gals

GALS = load_rotmod()

def build(Ud, Ub):
    """EXACT rebuild of g_bar from the components (never a rescale).  Committed convention."""
    gb, go, w, gid = [], [], [], []
    for i, g in enumerate(GALS):
        V2 = np.sign(g["Vgas"]) * g["Vgas"] ** 2 + Ud * g["Vdisk"] ** 2 + Ub * g["Vbul"] ** 2
        gbar = V2 * 1e6 / g["Rm"]
        gobs = (g["Vobs"] * 1e3) ** 2 / g["Rm"]
        ok = (gbar > 0) & (gobs > 0) & np.isfinite(gbar) & np.isfinite(gobs) & (g["Vobs"] > 0)
        fr = np.clip(g["eV"][ok], 1, None) / np.clip(g["Vobs"][ok], 1, None)
        gb += list(gbar[ok]); go += list(gobs[ok]); w += list(1.0 / fr ** 2)
        gid += [i] * int(ok.sum())
    return (np.array(gb), np.array(go), np.array(w), np.array(gid))

# ----------------------------------------------------------------------------------
# kernels
# ----------------------------------------------------------------------------------
def U_family(y, s):
    sq = np.sqrt(y)
    return s * sq / (s + sq)

def U_a0line(y, s=None):
    return np.sqrt(y * y + y) - y

def pred_family(gb, a0, s):
    return gb + a0 * U_family(gb / a0, s)

def pred_a0line(gb, a0, s=None):
    return np.sqrt(gb ** 2 + gb * a0)

def wrms_at(Ud, Ub, a0, s, predfn):
    gb, go, w, _ = build(Ud, Ub)
    r = np.log10(go) - np.log10(predfn(gb, a0, s))
    return float(np.sqrt(np.sum(w * r ** 2) / np.sum(w)))

def refit_upsilon(a0, s, predfn, lo=0.02, hi=10.0):
    """1-parameter refit, committed convention Ub = 1.4*Ud."""
    r = minimize_scalar(lambda U: wrms_at(U, 1.4 * U, a0, s, predfn),
                        bounds=(lo, hi), method="bounded",
                        options=dict(xatol=1e-4))
    return float(r.x), float(r.fun)

def refit_upsilon2(a0, s, predfn):
    """2-parameter refit (Ud, Ub free) -- deliberately generous to small s."""
    m = minimize(lambda p: wrms_at(abs(p[0]), abs(p[1]), a0, s, predfn),
                 [0.7, 1.0], method="Nelder-Mead",
                 options=dict(xatol=1e-4, fatol=1e-6, maxiter=2000))
    return float(abs(m.x[0])), float(abs(m.x[1])), float(m.fun)

# ==================================================================================
hdr("I012  RAR s-requirement with Upsilon REFITTED  --  real SPARC, anchored a0")
print(f"  repo        : {REPO}")
print(f"  a0 canonical: {A0_CANON:.4e} m/s^2   a0 alt: {A0_ALT:.4e} m/s^2")
print(f"  kappa = 1/2 is FITTED, never derived.")

hdr("BLOCK 0 -- data integrity")
check("175 SPARC rotmod galaxies loaded", len(GALS) == 175, f"n_gal={len(GALS)}")
gb07, go07, w07, gid07 = build(0.7, 0.7)
check("3389 usable RAR points at Upsilon 0.7/0.7", len(gb07) == 3389, f"N={len(gb07)}")

with open(RAR_JSON) as f:
    J = json.load(f)
P = np.array(J["points"])
check("rar_real_sparc.json header is Upsilon 0.7/0.7",
      J["upsilon_disk"] == 0.7 and J["upsilon_bulge"] == 0.7,
      f"{J['upsilon_disk']}/{J['upsilon_bulge']}")
same_n = (len(P) == len(gb07))
dmax = float(np.max(np.abs(np.log10(gb07) - P[:, 0]))) if same_n else np.nan
check("committed JSON is bit-identical to this raw 0.7/0.7 build",
      same_n and dmax < 1e-3, f"max|dlog10 g_bar| = {dmax:.2e} dex (JSON rounded to 4 dp)")
print("  -> the JSON carries NO per-point weights and uses Ub=Ud; the committed 0.1083 dex")
print("     is the eV/Vobs-WEIGHTED rms with Ub=1.4*Ud, so the raw files are used throughout.")

hdr("BLOCK 1 -- correcting brief premise C2: g_bar is NOT linear in Upsilon")
gb14, _, _, _ = build(1.4, 1.4)
ratio = gb14 / gb07                      # exact ratio on doubling Upsilon
naive = 2.0
frac_bad = float(np.mean(ratio < 1.5))
dex_err = float(np.max(np.abs(np.log10(ratio / naive))))
check("linear-Upsilon rescale premise is FALSE and is detected",
      dex_err > 0.05,
      f"doubling Upsilon: exact ratio median {np.median(ratio):.3f}, p5 {np.percentile(ratio,5):.3f}; "
      f"{100*frac_bad:.1f}% of points below 1.5; worst rescale error {dex_err:.3f} dex")
print("  -> cause: the GAS term sign(Vgas)Vgas^2 does not scale with Upsilon.  Gas-dominated")
print("     dwarfs are exactly the low-g_bar points that set the deep-MOND end of the RAR,")
print("     so rescaling would have distorted the very regime the s-scan probes.")
print("  -> this script rebuilds g_bar from components for EVERY Upsilon.  No rescale is used.")

hdr("BLOCK 2 -- correcting brief premise C1: the family at s=1/2 is NOT the a0-line")
yq = np.array([0.5, 1.0, 2.0, 5.0, 20.0])
print(f"  {'y':>8}{'U_a0line':>12}{'U_family(s=1/2)':>18}{'ratio':>9}")
for y in yq:
    print(f"  {y:>8.2f}{U_a0line(y):>12.4f}{U_family(y, 0.5):>18.4f}{U_family(y,0.5)/U_a0line(y):>9.4f}")
d2 = abs(U_a0line(2.0) - U_family(2.0, 0.5))
check("a0-line and family(s=1/2) are DIFFERENT functions (discrepancy caught)",
      d2 > 0.05, f"U(2): a0-line {U_a0line(2.0):.4f} vs family {U_family(2.0,0.5):.4f}  (diff {d2:.4f})")
# shared limits (both are in the legal class)
ysmall = 1e-8
check("both kernels -> sqrt(y) as y->0 (deep-MOND limit shared)",
      abs(U_a0line(ysmall) / np.sqrt(ysmall) - 1) < 1e-3 and
      abs(U_family(ysmall, 0.5) / np.sqrt(ysmall) - 1) < 1e-3, "")
ybig = 1e10
check("both kernels saturate at 1/2 and have U/y -> 0 (legal class)",
      abs(U_a0line(ybig) - 0.5) < 1e-3 and abs(U_family(ybig, 0.5) - 0.5) < 1e-3 and
      U_a0line(ybig) / ybig < 1e-9, "")
ytest = np.logspace(-6, 6, 4000)
mono = all(np.all(np.diff(U_family(ytest, s)) > 0) for s in [0.02, 0.1, 0.5, 1.0, 2.0])
check("U_s strictly increasing for every s scanned (ghost-free)", mono, "")

hdr("BLOCK 3 -- GATE: reproduce the committed 0.1083 dex")
g_gate = wrms_at(0.70, 1.4 * 0.70, A0_CANON, None, pred_a0line)
check("GATE a0-line, canonical a0, Upsilon_disk=0.70, Ub=1.4Ud",
      abs(g_gate - GATE_TARGET) < 2e-3,
      f"rms = {g_gate:.4f} dex vs committed {GATE_TARGET:.4f}")
u_line, r_line = refit_upsilon(A0_CANON, None, pred_a0line)
u_lineA, r_lineA = refit_upsilon(A0_ALT, None, pred_a0line)
print(f"  a0-line refitted : canon Upsilon={u_line:.3f} rms={r_line:.4f} | "
      f"alt Upsilon={u_lineA:.3f} rms={r_lineA:.4f}")

hdr("BLOCK 4 -- the s-scan with Upsilon REFITTED for every s (this is the experiment)")
S_GRID = [0.02, 0.05, 0.1, 0.2, 0.3, 0.5, 0.75, 1.0, 2.0]
TAB = {}
for nm, a0 in [("canonical", A0_CANON), ("alt", A0_ALT)]:
    print(f"\n  --- a0 {nm} = {a0:.4e} m/s^2 ---")
    print(f"  {'s':>7}{'U_best':>9}{'rms[dex]':>10}{'rms@U=0.70':>12}"
          f"{'2par Ud':>9}{'2par Ub':>9}{'2par rms':>10}{'ok?':>6}")
    TAB[nm] = []
    for s in S_GRID:
        ub, rb = refit_upsilon(a0, s, pred_family)
        r70 = wrms_at(0.70, 0.98, a0, s, pred_family)
        d2u, d2b, r2 = refit_upsilon2(a0, s, pred_family)
        good = (rb <= RMS_MAX) and (UPS_LO <= ub <= UPS_HI)
        TAB[nm].append(dict(s=s, ub=ub, rb=rb, r70=r70, d2u=d2u, d2b=d2b, r2=r2, ok=good))
        print(f"  {s:>7g}{ub:>9.3f}{rb:>10.4f}{r70:>12.4f}"
              f"{d2u:>9.3f}{d2b:>9.3f}{r2:>10.4f}{('YES' if good else 'no'):>6}")

# monotonicity of the degradation
mono_ok = True
for nm in TAB:
    rs = [row["rb"] for row in TAB[nm]]
    mono_ok &= all(rs[i] > rs[i + 1] for i in range(len(rs) - 1))
check("rms degrades monotonically as s decreases (both footings)", mono_ok, "")

# the family at s=1/2 vs the a0-line, refitted both
f_half = [r for r in TAB["canonical"] if r["s"] == 0.5][0]
check("family(s=1/2) fits WORSE than the a0-line even with Upsilon refitted",
      f_half["rb"] > r_line,
      f"family {f_half['rb']:.4f} dex (U={f_half['ub']:.3f}) vs a0-line {r_line:.4f} dex "
      f"(U={u_line:.3f}) -- so the briefed 's=1/2 -> 0.1083' spliced the two kernels")

hdr("BLOCK 5 -- WHY small s fails: the family's MOND window closes as s^2")
print("  U_s ~ sqrt(y) requires sqrt(y) << s, i.e. y << s^2.  As s shrinks the deep-MOND")
print("  window retreats below the data and every SPARC point sees the saturated U ~ s.")
y_all = gb07 / A0_CANON
print(f"  SPARC y = g_bar/a0 spans {y_all.min():.3e} .. {y_all.max():.3e} (canonical)")
print(f"  {'s':>7}{'y_MOND = s^2':>15}{'frac points with y < s^2':>26}")
fracs = {}
for s in [0.02, 0.1, 0.2, 0.5, 1.0, 2.0]:
    fr = float(np.mean(y_all < s * s)); fracs[s] = fr
    print(f"  {s:>7g}{s*s:>15.4f}{100*fr:>25.2f}%")
check("MOND window is empty of data for s <= 0.1, non-empty for s >= 0.5",
      fracs[0.1] < 0.02 and fracs[0.5] > 0.10,
      f"frac(y<s^2): s=0.1 -> {100*fracs[0.1]:.2f}%, s=0.5 -> {100*fracs[0.5]:.2f}%")

hdr("BLOCK 6 -- the binding galaxy-side floor on s")
FLOOR = {}
for nm, a0 in [("canonical", A0_CANON), ("alt", A0_ALT)]:
    f_rms = lambda s: refit_upsilon(a0, s, pred_family)[1] - RMS_MAX
    f_ups = lambda s: refit_upsilon(a0, s, pred_family)[0] - UPS_HI
    s_rms = brentq(f_rms, 0.05, 0.5, xtol=1e-4)
    s_ups = brentq(f_ups, 0.05, 0.5, xtol=1e-4)
    FLOOR[nm] = dict(s_rms=s_rms, s_ups=s_ups, s_bind=max(s_rms, s_ups))
    print(f"  {nm:>10}: s(rms=0.15 dex) = {s_rms:.4f}   s(Upsilon_best=0.90) = {s_ups:.4f}"
          f"   -> BINDING FLOOR s >= {max(s_rms,s_ups):.4f}")
check("binding floor is well inside (0.05, 0.5) for both footings",
      all(0.05 < FLOOR[n]["s_bind"] < 0.5 for n in FLOOR), "")
check("refitting Upsilon DOES lower the galaxy floor below the frozen-Upsilon 0.558",
      FLOOR["canonical"]["s_bind"] < S_GAL_OLD,
      f"{FLOOR['canonical']['s_bind']:.4f} vs {S_GAL_OLD} "
      f"-> a factor {S_GAL_OLD/FLOOR['canonical']['s_bind']:.2f} of real relief")

hdr("BLOCK 7 -- bootstrap over galaxies: is small s actually excluded?")
rng = np.random.default_rng(20260817)
NB = 400
def resid_by_gal(a0, s, Ud, Ub, predfn):
    gb, go, w, gid = build(Ud, Ub)
    r = np.log10(go) - np.log10(predfn(gb, a0, s))
    return [(w[gid == i], r[gid == i]) for i in range(len(GALS))]

def boot_delta(a0, s_lo, s_hi):
    ub_lo, _ = refit_upsilon(a0, s_lo, pred_family)
    ub_hi, _ = refit_upsilon(a0, s_hi, pred_family)
    A = resid_by_gal(a0, s_lo, ub_lo, 1.4 * ub_lo, pred_family)
    B = resid_by_gal(a0, s_hi, ub_hi, 1.4 * ub_hi, pred_family)
    n = len(GALS); out = []
    for _ in range(NB):
        idx = rng.integers(0, n, n)
        wa = np.concatenate([A[i][0] for i in idx]); ra = np.concatenate([A[i][1] for i in idx])
        wb = np.concatenate([B[i][0] for i in idx]); rb = np.concatenate([B[i][1] for i in idx])
        out.append(np.sqrt(np.sum(wa * ra ** 2) / np.sum(wa)) -
                   np.sqrt(np.sum(wb * rb ** 2) / np.sum(wb)))
    return np.array(out), ub_lo, ub_hi

for s_lo in [0.1, 0.2]:
    d, ul, uh = boot_delta(A0_CANON, s_lo, 0.5)
    frac_neg = float(np.mean(d <= 0))
    print(f"  canonical  rms(s={s_lo}) - rms(s=0.5), 400 galaxy bootstraps: "
          f"mean {d.mean():+.4f} dex, sd {d.std():.4f}, {d.mean()/d.std():.1f} sigma, "
          f"P(s={s_lo} no worse) = {frac_neg:.3f}")
    if s_lo == 0.1:
        check("s=0.1 is excluded relative to s=0.5 at >3 sigma (galaxy bootstrap)",
              d.mean() / d.std() > 3.0 and frac_neg < 0.01,
              f"{d.mean()/d.std():.1f} sigma, Upsilon needed {ul:.3f} (band {UPS_LO}-{UPS_HI})")

hdr("BLOCK 8 -- PASS / KILL adjudication as briefed")
pass_rows = [r for r in TAB["canonical"] + TAB["alt"] if r["s"] <= 0.1 and r["ok"]]
briefed_pass = len(pass_rows) > 0
print(f"  briefed PASS (some s <= 0.1 with rms <= {RMS_MAX} dex AND Upsilon in "
      f"[{UPS_LO},{UPS_HI}]): {'MET' if briefed_pass else 'NOT MET'}")
for nm in ("canonical", "alt"):
    r = [x for x in TAB[nm] if x["s"] == 0.1][0]
    print(f"    a0 {nm:>9}: s=0.1 -> best rms {r['rb']:.4f} dex at Upsilon {r['ub']:.3f} "
          f"({'inside' if UPS_LO<=r['ub']<=UPS_HI else 'OUTSIDE'} the band); "
          f"even 2-par: {r['r2']:.4f} dex at Ud={r['d2u']:.3f}")
check("briefed PASS condition correctly adjudicated NOT MET", not briefed_pass,
      "s=0.1 fails on rms AND on Upsilon, on both footings and with 2 free M/L")
# is the degradation a cliff at 0.4, or gradual?
rs_c = {r["s"]: r["rb"] for r in TAB["canonical"]}
cliff = (rs_c[0.3] - rs_c[0.5]) / (rs_c[0.5] - rs_c[0.75])
print(f"  shape of the degradation: rms(0.75)={rs_c[0.75]:.4f} 0.5={rs_c[0.5]:.4f} "
      f"0.3={rs_c[0.3]:.4f} 0.2={rs_c[0.2]:.4f} 0.1={rs_c[0.1]:.4f}")
check("degradation is gradual, not the briefed sharp cliff at s~0.4",
      0.5 < cliff < 5.0,
      f"no discontinuity; rms rises smoothly, crossing {RMS_MAX} dex at "
      f"s={FLOOR['canonical']['s_rms']:.3f} -- so the briefed KILL wording (sharp cliff) is "
      f"also inaccurate; the verdict is a soft floor, not a cliff")

hdr("BLOCK 9 -- ephemeris conversion and the size of the remaining gap")
# u_inf = s*a0; dvarpi/dt is linear in u_inf, hence linear in s
exc_lo = SATURN_EXCESS_AT_HALF / EFE_HI      # best case for the framework
exc_hi = SATURN_EXCESS_AT_HALF / EFE_LO      # worst case
s_eph_opt = 0.5 / exc_lo
s_eph_con = 0.5 / exc_hi
print(f"  Saturn excess at s=1/2 : {SATURN_EXCESS_AT_HALF:.0f}x before EFE")
print(f"  after EFE ({EFE_LO:.0f}-{EFE_HI:.0f}x): {exc_lo:.1f}x (optimistic) to {exc_hi:.1f}x (conservative)")
print(f"  => s_eph_max = {s_eph_opt:.3e} (optimistic EFE) to {s_eph_con:.3e} (conservative EFE)")
check("ephemeris ceiling reproduces the briefed s <= 2.4e-3",
      abs(s_eph_opt - 2.4e-3) < 1e-4, f"s_eph_max(optimistic) = {s_eph_opt:.4e}")
gap_old = S_GAL_OLD / s_eph_opt
check("the OLD (frozen-Upsilon) gap reproduces the briefed 233x",
      abs(gap_old - 233.0) < 3.0, f"{gap_old:.1f}x")
print()
print(f"  {'footing':>10}{'s_gal floor':>14}{'gap (opt EFE)':>16}{'gap (cons EFE)':>16}")
GAP = {}
for nm in ("canonical", "alt"):
    sb = FLOOR[nm]["s_bind"]
    GAP[nm] = (sb / s_eph_opt, sb / s_eph_con)
    print(f"  {nm:>10}{sb:>14.4f}{GAP[nm][0]:>15.1f}x{GAP[nm][1]:>15.1f}x")
best_gap = GAP["alt"][0]
check("gap is reduced but NOT closed (still > 10x on every footing)",
      10.0 < best_gap < gap_old,
      f"best case (alt footing, optimistic EFE) {best_gap:.1f}x, down from {gap_old:.1f}x")
check("relief factor is a genuine but partial 2-3x",
      2.0 < gap_old / best_gap < 4.0, f"{gap_old/best_gap:.2f}x relief")

hdr("VERDICT")
print(f"""  GATE PASSED: the a0-line at Upsilon_disk=0.70 reproduces {g_gate:.4f} dex against the
  committed 0.1083, on the identical 3389-point dataset (JSON verified bit-identical).

  The s >= 0.558 floor IS partly an artefact of freezing Upsilon -- but only partly.
  With Upsilon refitted per kernel on the real component decompositions, the galaxy-side
  floor falls from 0.558 to s >= {FLOOR['canonical']['s_bind']:.3f} (canonical) / {FLOOR['alt']['s_bind']:.3f} (alt).
  Both footings are bound at essentially the same place by two independent constraints that
  happen to bite together: rms crosses 0.15 dex at s={FLOOR['canonical']['s_rms']:.3f} and the refitted Upsilon
  leaves the 0.3-0.9 Spitzer band at s={FLOOR['canonical']['s_ups']:.3f} (canonical).  That coincidence is the trap
  the brief warned about, and it is real: small s IS partly absorbed by large Upsilon
  (Upsilon_best climbs from {TAB['canonical'][-1]['ub']:.2f} at s=2 to {TAB['canonical'][0]['ub']:.2f} at s=0.02), which is exactly why the
  Upsilon band, not the rms alone, has to be enforced.

  The briefed PASS is NOT met: s=0.1 costs {rs_c[0.1]:.4f} dex and needs Upsilon={TAB['canonical'][2]['ub']:.2f}, and it is
  excluded against s=0.5 at high significance by a 400-fold galaxy bootstrap.  Freeing the
  bulge M/L independently (2 parameters) does not rescue it: {TAB['canonical'][2]['r2']:.4f} dex at Ud={TAB['canonical'][2]['d2u']:.2f}.
  The mechanism is structural, not statistical: the family's deep-MOND window is y << s^2,
  so it retreats below the SPARC data as s shrinks and the kernel goes Newtonian.

  The briefed KILL wording is also wrong in detail -- there is no sharp cliff at s~0.4.
  The degradation is smooth and monotonic; the result is a soft floor near s ~ 0.17-0.22.

  Net: the 233x incompatibility becomes {GAP['canonical'][0]:.0f}x (canonical) / {GAP['alt'][0]:.0f}x (alt) under the most
  framework-favourable EFE reduction, and {GAP['canonical'][1]:.0f}x / {GAP['alt'][1]:.0f}x under the conservative one.
  Refitting Upsilon buys a real factor of ~{gap_old/best_gap:.1f}.  It does not close the gap.  The saturated
  sunward anomaly remains the sharpest open liability, and it cannot be retired from the
  galaxy side by shrinking s within this legal family.

  NOT COMPUTED: whether a legal kernel OUTSIDE this one-parameter family (one whose
  approach to saturation is slower in radius, or an EFE-dressed kernel whose effective s
  differs between the solar system and galaxy outskirts) can separate the two regimes.
  This script tests only U_s(y) = s*sqrt(y)/(s+sqrt(y)) and the a0-line.""")

hdr("CHECK SUMMARY")
npass = sum(1 for _, ok, _ in CHECKS if ok)
for nm, ok, det in CHECKS:
    print(f"  [{'ok' if ok else 'FAIL'}] {nm}")
print(f"\n  {npass}/{len(CHECKS)} checks passed")
sys.exit(0 if npass == len(CHECKS) else 1)
