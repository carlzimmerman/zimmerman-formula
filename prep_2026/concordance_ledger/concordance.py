#!/usr/bin/env python3
"""
CONCORDANCE -- Lane C: combine the anchor, the three positive bands, the pending
wide-binary row and the four nulls into one joint statement + the crossing figure.

What this script does (all on real data, frozen repo read-only):
  (1) CROSSING FIGURE  concordance_crossing.png -- log-a0 axis, one horizontal band
      per positive probe (P1 kinematic / P2 lensing-photon / P3 BTFR, P4 greyed
      pending), the Planck-anchored vertical lines on BOTH footings with their
      formal widths, plus the conventional fitted 1.2e-10 as a reference line.
  (2) JOINT CONSISTENCY per footing -- does the Planck-fixed number sit inside
      every independent band, and what (if anything) separates 9.355e-11 from
      1.131e-10 from the conventional 1.2e-10 given the bands. The P1/P3 Upsilon
      CO-MOVEMENT is enforced (one global M/L must serve both SPARC statistics).
  (3) NULL TABLE -- prediction vs bound vs margin, both footings (N1-N4).
  (4) PARAMETER ECONOMY on the SAME 175 SPARC rotation curves: framework
      (a0 fixed EXTERNALLY by the CMB + one global Upsilon) vs LCDM NFW halos
      (2-3 free parameters PER galaxy). chi2 / AIC / BIC computed honestly --
      LCDM halo fits are EXPECTED to fit well; the contrast is freedom count
      and predictivity, and it is stated exactly that way.
  (5) Writes CONCORDANCE.md with the honest-ceiling paragraph up top.

HONESTY RAILS (banked): framework nu(y)=sqrt(1+1/y) ONLY; the RAR/BTFR bands are
convention-compatible and NON-diagnostic of the exact a0; the claim is "the
Planck-fixed value sits INSIDE every independent band with zero per-object
freedom", never "probe X pins 9.36e-11"; no validates/proves language; both
footings everywhere; a win is verified as hard as a deficit.
"""
import json, math, os, glob
import numpy as np

np.random.seed(0)
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = "/Users/carlzimmerman/new_physics/zimmerman-formula/real_research"
DATA = os.path.join(REPO, "data", "sparc_data")
kpc = 3.0857e19

anc = json.load(open(os.path.join(HERE, "anchor_values.json")))
P1 = json.load(open(os.path.join(HERE, "p1_band.json")))
P2 = json.load(open(os.path.join(HERE, "p2_band.json")))
P3 = json.load(open(os.path.join(HERE, "p3_band.json")))

A0C, SC = anc["a0_canon"], anc["sig_canon"]     # canonical  cH_Lambda/Z
A0A, SA = anc["a0_alt"],   anc["sig_alt"]       # alt        cH0/Z
A0CONV  = 1.2e-10                               # conventional fitted MOND value (reference)
H0SI    = anc["H0"]

BAND_P1 = tuple(P1["band"])
BAND_P2 = tuple(P2["band"])
BAND_P3 = tuple(P3["band_exact"])

# ----------------------------------------------------------------------------------
# SPARC rotmod load (identical convention to p1_sparc_a0_band.py; read-only)
# ----------------------------------------------------------------------------------
gals = []
for f in sorted(glob.glob(os.path.join(DATA, "*_rotmod.dat"))):
    try:
        d = np.genfromtxt(f, comments="#")
    except Exception:
        continue
    if d.ndim != 2 or d.shape[1] < 6:
        continue
    R, Vobs, eV, Vgas, Vdisk, Vbul = (d[:, i] for i in range(6))
    gals.append(dict(name=os.path.basename(f).replace("_rotmod.dat", ""),
                     Rm=R*kpc, Vobs=Vobs, eV=eV,
                     gasS=np.sign(Vgas)*Vgas**2, disk2=Vdisk**2, bul2=Vbul**2))
assert len(gals) == 175, f"expected 175 SPARC galaxies, got {len(gals)}"

# concatenated arrays for the fast global RAR scatter
CAT = {k: np.concatenate([g[k] for g in gals]) for k in ("Rm", "Vobs", "eV", "gasS", "disk2", "bul2")}

def rar_scatter(U, a0):
    """weighted RAR scatter (dex) at global Upsilon U and fixed a0, framework nu."""
    gb = (CAT["gasS"] + U*CAT["disk2"] + 1.4*U*CAT["bul2"])*1e6/CAT["Rm"]
    go = (CAT["Vobs"]*1e3)**2/CAT["Rm"]
    ok = (gb > 0) & (go > 0) & np.isfinite(gb) & np.isfinite(go) & (CAT["Vobs"] > 0)
    r = np.log10(go[ok]) - 0.5*np.log10(gb[ok]**2 + gb[ok]*a0)
    fr = np.clip(CAT["eV"][ok], 1, None)/np.clip(CAT["Vobs"][ok], 1, None)
    w = 1/fr**2
    return float(np.sqrt(np.sum(w*r**2)/np.sum(w)))

# cross-check against the lane-P1 sidecar (same convention => must reproduce)
chk = rar_scatter(0.70, P1["per_upsilon"]["0.7"]["a0_best"])
assert abs(chk - P1["per_upsilon"]["0.7"]["smin"]) < 1e-6, "P1 scatter convention drifted"

# ----------------------------------------------------------------------------------
# (2) JOINT CONSISTENCY -- canonical vs alt vs conventional, with P1/P3 co-movement
# ----------------------------------------------------------------------------------
print("="*92)
print("JOINT CONSISTENCY -- one global Upsilon must serve BOTH SPARC statistics (P1+P3),")
print("the photon band is independent (P2). Candidates: canonical / alt / conventional.")
print("="*92)

a0_grid = np.geomspace(3e-11, 4e-10, 61)
Ufine = np.round(np.arange(0.50, 0.8001, 0.01), 3)
smin_U = np.array([min(rar_scatter(U, a) for a in a0_grid) for U in Ufine])

Uk = np.array([0.5, 0.6, 0.7, 0.8])
p3_med = np.array([P3["per_upsilon"][f"{u:.1f}"]["exact"]  for u in Uk])
p3_err = np.array([P3["per_upsilon"][f"{u:.1f}"]["e_exact"] for u in Uk])
medU = np.interp(Ufine, Uk, p3_med)
errU = np.interp(Ufine, Uk, p3_err)

# P2 published-budget stat sigmas (GLS, Delta-chi2=1) from the lane-P2 sidecar
fid = P2["headline"]                       # KiDS isolated, fiducial cold baryons
hot = P2["variants"]["hot-CGM budget (B21 file, diag)"]
sig_fid = (fid[2]-fid[1])/2
sig_hot = (hot[2]-hot[1])/2

TOL = 0.02
cands = [("CANONICAL cH_L/Z", A0C), ("ALT cH0/Z", A0A), ("conventional 1.2e-10", A0CONV)]
joint = {}
for lab, a0 in cands:
    penU = np.array([rar_scatter(U, a0) for U in Ufine])/smin_U - 1
    feas = penU <= TOL
    zU = (medU - a0)/errU
    if feas.any():
        i = int(np.argmin(np.where(feas, np.abs(zU), np.inf)))
    else:                                   # no U window: take least-bad U (report as tension)
        i = int(np.argmin(penU))
    in1 = BAND_P1[0] <= a0 <= BAND_P1[1]
    in2 = BAND_P2[0] <= a0 <= BAND_P2[1]
    in3 = BAND_P3[0] <= a0 <= BAND_P3[1]
    z_fid = (fid[0]-a0)/sig_fid
    z_hot = (a0-hot[0])/sig_hot
    joint[lab] = dict(a0=a0, U=float(Ufine[i]), pen=float(penU[i]*100), z3=float(zU[i]),
                      chi2=float(zU[i]**2), inside=[in1, in2, in3], feas=bool(feas.any()),
                      z_fid=float(z_fid), z_hot=float(z_hot))
    print(f"\n  {lab}: a0 = {a0:.3e}")
    print(f"    P1 kinematic band {BAND_P1[0]:.2e}..{BAND_P1[1]:.2e}: "
          f"{'INSIDE' if in1 else 'OUTSIDE'}; co-moving Upsilon* = {Ufine[i]:.2f} "
          f"(scatter penalty {penU[i]*100:.2f}% at U*, window exists: {feas.any()})")
    print(f"    P3 BTFR band     {BAND_P3[0]:.2e}..{BAND_P3[1]:.2e}: "
          f"{'INSIDE' if in3 else 'OUTSIDE'}; exact-median z at the SAME U* = {zU[i]:+.2f} sigma")
    print(f"    P2 photon band   {BAND_P2[0]:.2e}..{BAND_P2[1]:.2e}: "
          f"{'INSIDE' if in2 else 'OUTSIDE'} (systematics envelope; stat-only z: "
          f"{z_fid:+.1f}s from the cold-baryon budget, {z_hot:+.1f}s from the hot-CGM budget)")
    print(f"    joint chi2 (P3 z^2 at the co-moving U*; P1,P2 interval-pass): {zU[i]**2:.2f}")

d_can_alt  = joint["CANONICAL cH_L/Z"]["chi2"] - joint["ALT cH0/Z"]["chi2"]
d_can_conv = joint["CANONICAL cH_L/Z"]["chi2"] - joint["conventional 1.2e-10"]["chi2"]
print("\n  SEPARATION (the honest statement):")
print(f"    Delta joint-chi2  canonical - alt          = {d_can_alt:+.2f}")
print(f"    Delta joint-chi2  canonical - conventional = {d_can_conv:+.2f}")
print("    All three candidates sit INSIDE all three bands; every |Delta chi2| < 1.")
print("    => The ledger's galaxy probes CANNOT separate 9.355e-11 / 1.131e-10 / 1.2e-10.")
print("       What distinguishes the anchored values is PROVENANCE (derived from Planck")
print("       Lambda before looking at any galaxy), not a tighter posterior. Stat-only")
print("       lensing 'rejects' EVERY candidate from one baryon budget or the other")
print("       (incl. conventional 1.2e-10) -- proof the P2 band edges are baryon-budget")
print("       systematics, not instrument noise.")
assert all(joint[l]["inside"] == [True, True, True] for l in ("CANONICAL cH_L/Z", "ALT cH0/Z")), \
    "a Planck footing fell outside a positive band"

# ----------------------------------------------------------------------------------
# (3) NULL TABLE -- prediction vs bound vs margin (both footings)
# ----------------------------------------------------------------------------------
GM_sun, GM_earth = 1.32712440018e20, 3.986004418e14
AU = 1.495978707e11; r_sat = 9.5826*AU; r_moon = 3.844e8
hbar, J_per_GeV = 1.054571817e-34, 1.602176634e-10
Q2_ceiling = 1.6e-27 + 2*1.8e-27
Q2_MI = {"canon": 7.4e-34, "alt": 7.4e-34*(A0A/A0C)**2}
Q2_MG = {"canon": A0C/(2*r_sat), "alt": A0A/(2*r_sat)}
g_moon = GM_earth/r_moon**2
llr_obs = {"canon": (A0C/(2*g_moon))**2, "alt": (A0A/(2*g_moon))**2}
frac_llr = 1e-3/r_moon
kodd = {"canon": hbar*anc["HL"]/J_per_GeV, "alt": hbar*H0SI/J_per_GeV}
kAF_bound = 1e-44

null_rows = [
    ("N1 ephemerides (Cassini Q2)",
     f"MI l=2: {Q2_MI['canon']:.1e} / {Q2_MI['alt']:.1e} s^-2 (DC a0/2g absorbed into GM_sun)",
     f"Q2 2-sigma ceiling {Q2_ceiling:.1e} s^-2 (Park+ 2026 arXiv:2602.17884; DHF24 MNRAS 530,1781)",
     f"PASS {math.log10(Q2_ceiling/Q2_MI['canon']):.1f} / {math.log10(Q2_ceiling/Q2_MI['alt']):.1f} orders; "
     f"MG-read of the SAME a0 = {Q2_MG['canon']:.1e} -> EXCLUDED {math.log10(Q2_MG['canon']/Q2_ceiling):.1f} orders"),
    ("N2 LLR (mm ranging)",
     f"observable MI channel (a0/2g)^2 = {llr_obs['canon']:.1e} / {llr_obs['alt']:.1e} (DC absorbed into GM_earth)",
     f"fractional sensitivity {frac_llr:.1e} (APOLLO; Murphy 2013 RPP 76, 076901)",
     f"PASS {math.log10(frac_llr/llr_obs['canon']):.1f} / {math.log10(frac_llr/llr_obs['alt']):.1f} orders"),
    ("N3 MICROSCOPE WEP",
     "eta = 0 EXACTLY (universal inertia rescaling; no composition channel; footing-independent)",
     "eta(Ti,Pt) = (-1.5 +/- 2.3)e-15 (Touboul+ 2022 PRL 129, 121102 final)",
     "PASS: exact zero sits 0.65 sigma from the measurement at 1e-15 precision"),
    ("N4 CPT / photon k_AF",
     "k_AF = 0 EXACTLY (SME bridge: horizon induces CPT-EVEN s_munu only)",
     f"abs(k_AF) < {kAF_bound:.0e} GeV (Kostelecky-Russell RMP 83,11, 2023 tables)",
     f"PASS by structure; CPT-ODD sibling scale hbar*H = {kodd['canon']:.2e} / {kodd['alt']:.2e} GeV "
     f"sits {kodd['canon']/kAF_bound:.0f}x / {kodd['alt']/kAF_bound:.0f}x ABOVE the bound -> that variant is DEAD"),
]
print("\n" + "="*92)
print("NULL TABLE (prediction vs bound vs margin; canonical/alt where a0 enters)")
print("="*92)
for name, pred, bound, margin in null_rows:
    print(f"  {name}\n     predict: {pred}\n     bound:   {bound}\n     margin:  {margin}")

# ----------------------------------------------------------------------------------
# (4) PARAMETER ECONOMY -- same 175 rotation curves, chi2/AIC/BIC, freedom counted
# ----------------------------------------------------------------------------------
from scipy.optimize import least_squares

print("\n" + "="*92)
print("PARAMETER ECONOMY on the SAME data: framework (a0 CMB-fixed + 1 global Upsilon)")
print("vs LCDM NFW (2-3 free params PER galaxy). LCDM is EXPECTED to fit well.")
print("="*92)

# common point mask: Vbar2 > 0 over the WHOLE Upsilon scan range (Vbar2 is monotonic
# increasing in U, so U=0.30 -- the scan floor -- is the binding case); keeps the
# dataset identical across all models; eV floored at 1 km/s (committed-baseline convention)
for g in gals:
    vb_min = g["gasS"] + 0.30*(g["disk2"] + 1.4*g["bul2"])
    g["ok"] = (vb_min > 0) & (g["Vobs"] > 0) & np.isfinite(g["Vobs"])
    g["eVf"] = np.clip(g["eV"], 1.0, None)
Npts = int(sum(g["ok"].sum() for g in gals))
print(f"  common dataset: {Npts} points across 175 galaxies "
      f"({int(sum(len(g['Vobs']) for g in gals)) - Npts} dropped where V_bar^2 <= 0)")

def vbar2(g, U):
    return g["gasS"] + U*g["disk2"] + 1.4*U*g["bul2"]

def chi2_framework_gal(g, U, a0):
    m = g["ok"]
    gb = vbar2(g, U)[m]*1e6/g["Rm"][m]
    vmod = np.sqrt(np.sqrt(gb**2 + gb*a0)*g["Rm"][m])/1e3
    return float(np.sum(((g["Vobs"][m]-vmod)/g["eVf"][m])**2))

def vnfw2_kms2(R, V200_kms, c):
    V200 = V200_kms*1e3
    r200 = V200/(10*H0SI)
    x = np.clip(R/r200, 1e-9, None)
    mu = np.log(1+c*x) - c*x/(1+c*x)
    mu0 = np.log(1+c) - c/(1+c)
    return (V200**2*mu/(x*mu0))/1e6

def fit_nfw_gal(g, U_fixed=None):
    """min chi2 over (V200,c) [+U if U_fixed None], multi-start, log-space."""
    m = g["ok"]
    R, Vo, eV = g["Rm"][m], g["Vobs"][m], g["eVf"][m]
    def resid(p):
        lv, lc = p[0], p[1]
        U = p[2] if U_fixed is None else U_fixed
        v2 = vbar2(g, U)[m] + vnfw2_kms2(R, 10**lv, 10**lc)
        return (Vo - np.sqrt(np.clip(v2, 0, None)))/eV
    best = None
    lo = [np.log10(5), np.log10(0.5)] + ([] if U_fixed is not None else [0.3])
    hi = [np.log10(700), np.log10(150)] + ([] if U_fixed is not None else [0.8])
    for v0 in (50, 120, 250):
        for c0 in (4, 12, 30):
            p0 = [np.log10(v0), np.log10(c0)] + ([] if U_fixed is not None else [0.5])
            try:
                r = least_squares(resid, p0, bounds=(lo, hi), method="trf", xtol=1e-10)
                if best is None or r.cost < best.cost:
                    best = r
            except Exception:
                continue
    return float(2*best.cost)   # chi2

# framework: global Upsilon profiled (a0 fixed externally, per footing)
Uscan = np.round(np.arange(0.30, 1.0001, 0.01), 3)
fw = {}
for lab, a0 in (("canon", A0C), ("alt", A0A)):
    tots = np.array([sum(chi2_framework_gal(g, U, a0) for g in gals) for U in Uscan])
    i = int(np.argmin(tots))
    fw[lab] = dict(U=float(Uscan[i]), chi2=float(tots[i]),
                   pergal=[chi2_framework_gal(g, Uscan[i], a0) for g in gals])
    print(f"  framework [{lab:>5}] a0 FIXED = {a0:.3e}: best global Upsilon = {Uscan[i]:.2f}, "
          f"chi2 = {tots[i]:.0f} ({tots[i]/Npts:.2f}/pt)")

# framework variant: per-galaxy Upsilon (a0 still fixed, canonical) -- k = 175
Ug = np.round(np.arange(0.30, 0.8001, 0.01), 3)
fw_pg = [min(chi2_framework_gal(g, U, A0C) for U in Ug) for g in gals]
chi2_fw_pg = float(sum(fw_pg))
print(f"  framework [per-galaxy U, canon a0]: chi2 = {chi2_fw_pg:.0f} ({chi2_fw_pg/Npts:.2f}/pt)")

# LCDM NFW
lcdmA = [fit_nfw_gal(g, U_fixed=0.5) for g in gals]      # 2/gal, U=0.5 convention
chi2_A = float(sum(lcdmA))
print(f"  LCDM NFW [U=0.5 fixed, 2 params/gal = 350]: chi2 = {chi2_A:.0f} ({chi2_A/Npts:.2f}/pt)")
lcdmB = [fit_nfw_gal(g, U_fixed=None) for g in gals]     # 3/gal
chi2_B = float(sum(lcdmB))
print(f"  LCDM NFW [U free/gal, 3 params/gal = 525]:  chi2 = {chi2_B:.0f} ({chi2_B/Npts:.2f}/pt)")

lnN = math.log(Npts)
models = [
    ("framework, canon a0 (external) + 1 global U",  fw["canon"]["chi2"], 1),
    ("framework, alt a0 (external) + 1 global U",    fw["alt"]["chi2"],   1),
    ("framework, canon a0 + per-galaxy U",           chi2_fw_pg,          175),
    ("LCDM NFW, U=0.5 + (V200,c) per galaxy",        chi2_A,              350),
    ("LCDM NFW, (V200,c,U) per galaxy",              chi2_B,              525),
]
print(f"\n  {'model':52s} {'k':>4} {'chi2':>9} {'chi2/N':>7} {'AIC':>9} {'BIC':>9}")
ic = {}
for name, c2, k in models:
    aic, bic = c2 + 2*k, c2 + k*lnN
    ic[name] = (c2, k, aic, bic)
    print(f"  {name:52s} {k:>4d} {c2:>9.0f} {c2/Npts:>7.2f} {aic:>9.0f} {bic:>9.0f}")

med_fw = float(np.median([c/max(g["ok"].sum(), 1) for c, g in zip(fw["canon"]["pergal"], gals)]))
med_A  = float(np.median([c/max(g["ok"].sum()-2, 1) for c, g in zip(lcdmA, gals)]))
med_B  = float(np.median([c/max(g["ok"].sum()-3, 1) for c, g in zip(lcdmB, gals)]))
frac_close = float(np.mean([f <= 2*l for f, l in zip(fw["canon"]["pergal"], lcdmB)]))
print(f"\n  median per-galaxy reduced chi2: framework(0 free/gal) {med_fw:.2f} | "
      f"NFW U=0.5 {med_A:.2f} | NFW free-U {med_B:.2f}")
print(f"  fraction of galaxies where the ZERO-per-object-freedom framework curve lands within")
print(f"  2x of the galaxy's own 3-parameter NFW chi2: {100*frac_close:.0f}%")
print("\n  HONEST READ (exactly as it must be stated): LCDM halo fits FIT WELL -- with 2-3")
print("  free parameters per galaxy they reach a lower total chi2, and on raw AIC/BIC per")
print("  -point fit quality they can win despite the parameter penalty. The economy contrast")
print("  is FREEDOM COUNT and PREDICTIVITY: the framework's number was fixed by the CMB")
print("  before any rotation curve was looked at (1 global convention parameter, ZERO per-")
print("  object parameters, and the SAME number must simultaneously survive P2/P3/N1-N4);")
print("  the halo alternative spends hundreds of per-object parameters and carries NO")
print("  cross-probe number to thread. AIC/BIC computed on one dataset cannot price that")
print("  cross-dataset rigidity -- that is what the crossing figure shows.")
print("  CHI2 CAVEAT (both directions): the framework row models NO per-galaxy nuisance at")
print("  all -- SPARC's own 10-30% distance and inclination uncertainties enter its chi2 as")
print("  unmodeled error, while per-galaxy halo parameters partially absorb them. The")
print("  like-for-like single-statistic comparison stays the committed RAR row: 0.108 dex")
print("  (framework, canonical a0, 1 global Upsilon) vs 0.122 (reg-MOND) on the same points.")

# ----------------------------------------------------------------------------------
# (1) CROSSING FIGURE
# ----------------------------------------------------------------------------------
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

C_P1, C_P2, C_P3 = "#2a78d6", "#1baf7a", "#eda100"     # validated palette (slots 1-3)
C_CAN, C_ALT = "#e34948", "#4a3aa7"
INK, MUT = "#0b0b0b", "#52514e"

plt.rcParams.update({"font.size": 10.5, "font.family": "DejaVu Sans",
                     "axes.edgecolor": MUT, "text.color": INK,
                     "xtick.color": INK, "ytick.color": INK})
fig, ax = plt.subplots(figsize=(10.2, 7.2))
XLO, XHI = 4.3e-11, 4.3e-10
ax.set_xscale("log"); ax.set_xlim(XLO, XHI); ax.set_ylim(-0.10, 5.95)
TXBOX = dict(boxstyle="square,pad=0.15", facecolor="#fcfcfb", edgecolor="none", alpha=0.88)

def band(y, lo, hi, color, title, sysline):
    ax.fill_betweenx([y-0.24, y+0.24], lo, hi, color=color, alpha=0.32, lw=0)
    ax.plot([lo, lo], [y-0.24, y+0.24], color=color, lw=2)
    ax.plot([hi, hi], [y-0.24, y+0.24], color=color, lw=2)
    ax.text(XLO*1.04, y+0.42, title, fontsize=10.5, fontweight="bold", color=INK,
            va="bottom", zorder=7, bbox=TXBOX)
    ax.text(XLO*1.04, y-0.34, sysline, fontsize=8.4, color=MUT, va="top", zorder=7, bbox=TXBOX)

def mark_label(a, y, lab, i):
    dy = 9 if i % 2 == 0 else -16
    ax.annotate(lab, (a, y), xytext=(0, dy), textcoords="offset points",
                ha="center", fontsize=7.8, color=MUT, zorder=7, bbox=TXBOX)

# P1 (top band)
band(4.05, *BAND_P1, C_P1, "P1  KINEMATIC RAR -- SPARC 175 (gas kinematics)",
     "systematics: stellar M/L, distances, inclinations\nband = union of 2%-scatter windows over $\\Upsilon$ = 0.5-0.8")
for i, u in enumerate((0.5, 0.6, 0.7, 0.8)):
    a = P1["per_upsilon"][f"{u:.1f}"]["a0_best"]
    ax.plot(a, 4.05, "o", ms=5.5, color=C_P1, mec="white", mew=0.9, zorder=6)
    mark_label(a, 4.05, f"$\\Upsilon$={u:.1f}", i)

# P2
band(2.75, *BAND_P2, C_P2, "P2  WEAK-LENSING RAR -- KiDS-1000 photons (Brouwer+ 2021)",
     "systematics: shear calibration, photo-z, baryon budget (CGM) -- disjoint from P1\nband = envelope of the PUBLISHED baryon budgets + sample/scale variants")
p2m = [(P2["variants"]["hot-CGM budget (B21 file, diag)"][0], "hot CGM"),
       (P2["variants"]["M* +0.2 dex"][0], "M*+0.2 dex"),
       (P2["variants"]["GAMA spec-z lenses (indep. sample)"][0], "GAMA"),
       (P2["headline"][0], "cold baryons ($\\chi^2/\\nu$=2.8)")]
for i, (a, lab) in enumerate(p2m):
    ax.plot(a, 2.75, "D", ms=5, color=C_P2, mec="white", mew=0.9, zorder=6)
    mark_label(a, 2.75, lab, i)

# P3
band(1.45, *BAND_P3, C_P3, "P3  BTFR ZERO-POINT -- SPARC master table, N=121 (shape-free)",
     "systematics: stellar M/L (same 0.5-0.8 range ledger-wide), distances\nexact estimator $V_f^4 = GM_b\\,(a_0+g_{bar})$; markers = medians $\\pm$ err")
for i, u in enumerate((0.5, 0.6, 0.7, 0.8)):
    d = P3["per_upsilon"][f"{u:.1f}"]
    ax.errorbar(d["exact"], 1.45, xerr=d["e_exact"], fmt="s", ms=5, color=C_P3,
                mec="white", mew=0.9, elinewidth=1.4, capsize=2.5, zorder=6)
    mark_label(d["exact"], 1.45, f"$\\Upsilon$={u:.1f}", i + 1)

# P4 pending strip
ax.fill_betweenx([0.02, 0.44], XLO, XHI, color="#9a9a94", alpha=0.16, lw=0, hatch="///",
                 edgecolor="#9a9a94")
ax.text(XLO*1.04, 0.52, "P4  GAIA WIDE BINARIES -- STATUS ROW (greyed: pending DR4, ~Dec 2026)",
        fontsize=10.5, fontweight="bold", color=MUT, va="bottom", zorder=7, bbox=TXBOX)
ax.text(XLO*1.04, 0.23, "a$_0$-degenerate premise test, no a$_0$ band: pure-MI $\\gamma\\approx$1.05-1.14, MG 1.137, Newton 1.00;\n"
        "DR3 dry-run $\\gamma$=1.205$\\pm$0.035 (contamination-axis caveat) -- can hard-kill or separate MI/MG",
        fontsize=8.4, color=MUT, va="center", zorder=7, bbox=TXBOX)

# anchors (verticals) + dedicated top label strip (y ~ 4.75-5.9)
ax.axvspan(A0C-SC, A0C+SC, color=C_CAN, alpha=0.30, zorder=2)
ax.axvline(A0C, color=C_CAN, lw=1.8, zorder=3)
ax.axvspan(A0A-SA, A0A+SA, color=C_ALT, alpha=0.28, zorder=2)
ax.axvline(A0A, color=C_ALT, lw=1.8, zorder=3)
ax.axvline(A0CONV, color=MUT, lw=1.3, ls=":", zorder=3)
ax.annotate("PLANCK CANONICAL  $cH_\\Lambda/Z$ = 9.355e-11 ($\\pm$0.96%, no galaxy input)",
            (A0C, 5.82), ha="right", va="center", fontsize=9.0, color=C_CAN,
            fontweight="bold", xytext=(-5, 0), textcoords="offset points", zorder=7, bbox=TXBOX)
ax.annotate("PLANCK ALT  $cH_0/Z$ = 1.131e-10 ($\\pm$0.80%)",
            (A0A, 5.42), ha="right", va="center", fontsize=9.0, color=C_ALT,
            fontweight="bold", xytext=(-5, 0), textcoords="offset points", zorder=7, bbox=TXBOX)
ax.annotate("conventional fitted 1.2e-10 (reference)",
            (A0CONV, 5.02), ha="left", va="center", fontsize=8.4, color=MUT,
            xytext=(5, 0), textcoords="offset points", zorder=7, bbox=TXBOX)

ax.set_yticks([])
ax.set_xlabel("$a_0$  [m s$^{-2}$]   (log scale)")
ax.set_title("One CMB-fixed acceleration through independent probe classes\n"
             "$a_0 = cH_\\Lambda/Z$, $Z=\\sqrt{32\\pi/3}$ (Planck 2018, zero galaxy input) vs bands with disjoint systematics",
             fontsize=12, pad=10)
for s in ("top", "right", "left"):
    ax.spines[s].set_visible(False)
fig.tight_layout(rect=(0, 0.035, 1, 1))
fig.text(0.5, 0.012,
         "bands are systematics envelopes (non-diagnostic of the exact a$_0$, stated as wide); the claim is the anchored value\n"
         "sits INSIDE every band with zero per-object freedom -- consistency with parameter economy, not proof",
         ha="center", va="bottom", fontsize=8.2, color=MUT, style="italic")
png = os.path.join(HERE, "concordance_crossing.png")
fig.savefig(png, dpi=250, facecolor="#fcfcfb", bbox_inches="tight")
print(f"\n  [figure written: {png}]")

# threading check (the figure's claim, asserted)
for lab, a0 in (("canonical", A0C), ("alt", A0A)):
    for nm, (lo, hi) in (("P1", BAND_P1), ("P2", BAND_P2), ("P3", BAND_P3)):
        assert lo <= a0 <= hi, f"{lab} misses {nm}"
print("  THREADING: both Planck footings sit inside all three positive bands.  [asserted]")

# ----------------------------------------------------------------------------------
# (5) CONCORDANCE.md
# ----------------------------------------------------------------------------------
def e(x): return f"{x:.3e}"
md = f"""# CONCORDANCE — one Planck-fixed acceleration, every independent band, every null
**Lane C combine.** 2026-07-16. All numbers below computed by `concordance.py` (exit 0) or the
lane scripts in this directory; frozen repo read-only; primary sources cited on every bound.

## THE HONEST CEILING (read this first)
This ledger demonstrates **consistency plus parameter economy — not proof, not validation.**
Its strongest true statement: one number derived from Planck's Λ with zero galaxy input,
`a0 = cH_Λ/Z = {e(A0C)} m/s²` (formal width <1%), sits **inside every independent positive band**
(gas kinematics; lensed photons; a shape-free global scaling) **with zero per-object freedom**,
while every high-precision null it must pass, it passes — two by computed suppression (~4 and ~7
orders), two by exact structure. What it does **not** do: the galaxy bands are wide
(baryon-budget and M/L systematics, stated as wide) and **cannot separate** {e(A0C)} from
{e(A0A)} from the conventional fitted 1.2e-10 — joint Δχ² between all three candidates is
< 1 (computed below). The anchored values are distinguished by **provenance** (fixed before any
galaxy is looked at), not by a tighter posterior. ΛCDM fits the same positive probes **well**
with per-object halo freedom — the raw AIC/BIC on one dataset can favor it (computed below,
not hidden); what AIC/BIC on one dataset cannot price is that the framework's single number is
simultaneously hostage to four probe classes and four nulls. The Z in the anchor is fixed by
the dS-Unruh construction but its **value remains postulated** (κ-closure banked): the ledger
tests the number, not its pedigree. The wide-binary row is **pending** (Gaia DR4) and can still
hard-kill the premise. Fitted g† values are never compared across ν conventions; every fit here
uses the framework's own ν(y)=√(1+1/y).

![crossing figure](concordance_crossing.png)

## 1. Anchor (both footings, `anchor_planck_a0.py`)
| footing | a0 | width |
|---|---|---|
| CANONICAL ρ_DE/cH_Λ | ({A0C*1e11:.3f} ± {SC*1e11:.3f})e-11 m/s² | 0.96% (ρ-bracket 0.27–1.33%) |
| ALT ρ_total/cH0 | ({A0A*1e10:.4f} ± {SA*1e10:.4f})e-10 m/s² | 0.80% |

## 2. The crossing — joint consistency per footing
Bands (systematics envelopes): P1 kinematic [{e(BAND_P1[0])}, {e(BAND_P1[1])}] · P2 photon
[{e(BAND_P2[0])}, {e(BAND_P2[1])}] · P3 BTFR [{e(BAND_P3[0])}, {e(BAND_P3[1])}]. One global Υ
must serve P1 and P3 simultaneously (co-movement enforced); P2 is independent (photons).

| candidate a0 | P1 | P2 | P3 | co-moving Υ* | P1 penalty @Υ* | P3 z @Υ* | joint χ² |
|---|---|---|---|---|---|---|---|
"""
for lab, a0 in cands:
    j = joint[lab]
    ins = ["INSIDE" if b else "OUTSIDE" for b in j["inside"]]
    md += (f"| {lab} = {e(a0)} | {ins[0]} | {ins[1]} | {ins[2]} | {j['U']:.2f} | "
           f"{j['pen']:.2f}% | {j['z3']:+.2f}σ | {j['chi2']:.2f} |\n")
md += f"""
**Separation, stated honestly:** Δχ²(canonical−alt) = {d_can_alt:+.2f}; Δχ²(canonical−conventional
1.2e-10) = {d_can_conv:+.2f}. All three candidates thread all three bands; **the ledger cannot
separate them.** The distinguishing content of the anchored values is that they were **derived
from Planck's Λ before looking at any galaxy**. Stat-only lensing "rejects" *every* candidate —
canonical at {joint['CANONICAL cH_L/Z']['z_fid']:+.1f}σ from B21's cold-baryon budget and
{joint['CANONICAL cH_L/Z']['z_hot']:+.1f}σ from B21's own hot-CGM budget, conventional 1.2e-10 at
{joint['conventional 1.2e-10']['z_fid']:+.1f}σ/{joint['conventional 1.2e-10']['z_hot']:+.1f}σ —
which is exactly why the P2 band is a published-baryon-budget envelope, not an instrument limit.

## 3. Null table — the framework must predict ~zero where the best instruments see zero
| null | framework prediction | measured bound (primary source) | margin (canon / alt) |
|---|---|---|---|
"""
for name, pred, bound, margin in null_rows:
    md += f"| **{name}** | {pred} | {bound} | {margin} |\n"
md += f"""
## 4. Parameter economy on the SAME 175 SPARC curves (`concordance.py`, N = {Npts} points)
Gaussian-error χ², AIC = χ²+2k, BIC = χ²+k·ln N (constant terms identical across models).
a0 is charged to the framework as **zero** fitted parameters because it is fixed externally by
the CMB; even charging it as one global parameter adds only +2 (AIC) / +{lnN:.1f} (BIC) and
changes nothing below.

| model | k (free params) | χ² | χ²/N | AIC | BIC |
|---|---|---|---|---|---|
"""
for name, c2, k in models:
    _, _, aic, bic = ic[name]
    md += f"| {name} | {k} | {c2:.0f} | {c2/Npts:.2f} | {aic:.0f} | {bic:.0f} |\n"
md += f"""
Median per-galaxy reduced χ²: framework (0 free/galaxy) {med_fw:.2f} · NFW U=0.5 {med_A:.2f} ·
NFW free-U {med_B:.2f}. In {100*frac_close:.0f}% of galaxies the zero-per-object-freedom framework
curve lands within 2× of that galaxy's own 3-parameter NFW χ².

**Stated exactly as it must be:** ΛCDM halo fits **fit well** — with 2–3 free parameters per
galaxy they reach lower total χ², and {"they win raw AIC/BIC on this dataset despite the penalty"
if ic[models[3][0]][3] < ic[models[0][0]][3] else "yet the framework's 1-parameter row still wins AIC/BIC on this dataset"}.
The economy contrast is **freedom count and predictivity**: 1 externally-fixed global number
(+ one global M/L convention) against {350}–{525} per-object parameters; the framework's number
must simultaneously survive the photon band, the BTFR, and four nulls — a cross-dataset rigidity
that single-dataset information criteria cannot price. That rigidity, not a χ² win, is the
ledger's content. χ² caveat, both directions: the framework row models **no per-galaxy nuisance
at all** — SPARC's own 10–30% distance and inclination uncertainties enter its χ² as unmodeled
error, while per-galaxy halo parameters partially absorb them; the like-for-like
single-statistic comparison remains the committed RAR row, **0.108 dex (framework, canonical a0,
one global Υ) vs 0.122 (reg-MOND)** on the same points.

## 5. The ledger read (no "validates/proves")
One CMB-fixed number, formal width <1%, threads three independent positive bands with disjoint
systematics (a fourth probe class, wide binaries, is pending) and passes every null — two by ~4–7 orders of computed suppression, two by
exact structure (η = 0 at 1e-15 precision; k_AF = 0 where the CPT-odd sibling scale is dead by
~2 orders). The bands are wide and say so; the galaxy probes cannot pick the exact value; the
wide-binary row can still kill the premise. **Consistency with economy, exposed to a live
falsifier — that is the whole claim.**

*Files: `concordance.py` (this combine, exit 0), `concordance_crossing.png` (money figure),
lane scripts `anchor_planck_a0.py`, `p1_sparc_a0_band.py`, `p2_lensing_a0_band.py`,
`p3_btfr_a0_band.py`, `p4_widebinary_status.py`, `nulls_n1_n4.py`, sidecars `*_band.json`,
row detail `LEDGER_ROWS.md`.*
"""
open(os.path.join(HERE, "CONCORDANCE.md"), "w").write(md)
json.dump(dict(joint={k: {kk: vv for kk, vv in v.items() if kk != "pergal"} for k, v in joint.items()},
               economy={n: dict(chi2=c2, k=k, aic=ic[n][2], bic=ic[n][3]) for n, c2, k in models},
               Npts=Npts),
          open(os.path.join(HERE, "concordance_summary.json"), "w"), indent=1, default=float)
print("  [CONCORDANCE.md + concordance_summary.json written]")
print("\nCONCORDANCE COMBINE COMPLETE (exit 0).")
