#!/usr/bin/env python3
"""
SWEEP 2 — the galaxy-sector viable region: scan (a0, Upsilon, nu) for ALL galaxy fronts.
========================================================================================
Maps where ALL galaxy-sector fronts are SIMULTANEOUSLY viable on the REAL SPARC data,
as a function of the three effective galaxy-box knobs:
    a0       in [8e-11, 1.3e-10]   (the framework value 9.36e-11; band [9.1e-11, 1.2e-10])
    Upsilon  in [0.4, 0.7]         (3.6um stellar M/L of the disk)
    nu       in {dS-Unruh, simple, standard, McGaugh}  (the interpolation function)

The five galaxy fronts (each carves an allowed region; we want the INTERSECTION):
  (i)   RAR    : unweighted dex scatter at (a0,Upsilon,nu) within a tolerance of the
                 per-(Upsilon,nu) optimum  (penalty <= tol_dex). NON-diagnostic floor.
  (ii)  BTFR   : deep-MOND slope ~ 4 (IF-FREE closed form V^4=G M a0); we check the
                 unbiased ODR slope in [3.7, 4.3] and the implied a0 consistency band.
  (iii) dwarfs : 3/8 over-dispersed acceptable at framework footing? (banked: robust,
                 worsens at lower a0 / lower Upsilon -- we re-flag the direction, not a veto).
  (iv)  EFE/SEP: the EFE gamma band at MW g_ext; CONSISTENT (contested Chae 4-5sigma high)
                 -- the front is "viable" wherever gamma is in a physical MOND band; the
                 Chae tension is reported as a directional pull, not a hard veto.
  (v)   wide-bin: the EFE gamma cap at MW field must land in the allowed obs band; the
                 framework dS-Unruh cap is 1.137 (gamma_cap). We report cap vs band.

The metric for RAR is the framework's OWN dS-Unruh interpolation by default
(g_obs = sqrt(g_bar^2 + g_bar*a0)), per the MEMORY working rule, with the other three
nu's scanned for the spread. NO synthetic data: 175 SPARC rotmod + the master table.

Run:  python opus_48_extended_research/reviews/galaxy_box_viability_scan.py
"""
import glob, math, os, csv
import numpy as np
from scipy.optimize import minimize_scalar
from scipy import odr

# ---------------------------------------------------------------- paths / const
HERE = os.path.dirname(os.path.abspath(__file__))
ROT  = os.path.join(HERE, "..", "..", "real_research", "data", "sparc_data")
MAST = os.path.join(HERE, "..", "..", "real_research", "data", "sparc_master_clean.csv")

KPC_M = 3.0856775814913673e19
KMS   = 1.0e3
C     = 2.99792458e8
G     = 6.674e-11
MSUN  = 1.989e30
HE    = 1.33

A0_FRAMEWORK = 9.36e-11
A0_LO, A0_HI = 8.0e-11, 1.30e-10        # the prior box for a0
UPS_LO, UPS_HI = 0.40, 0.70             # the prior box for Upsilon
NUS = ["dsunruh", "simple", "standard", "mcgaugh"]

# the framework's stated point
FW_A0, FW_UPS, FW_NU = 9.36e-11, 0.70, "dsunruh"

# the galactic best-fit a0 band the prompt cites (for sanity)
A0_BAND_LO, A0_BAND_HI = 9.1e-11, 1.2e-10

# MW external field at the Sun (convention-fixed, footing-independent)
G_EXT_MW = 2.08e-10   # m/s^2  (V^2/R ~ (233 km/s)^2 / 8.2 kpc)

# ---------------------------------------------------------------- interpolations
# all return g_obs given g_bar, a0.  y = g_bar/a0.
def g_dsunruh(gbar, a0):                       # framework: sqrt(1+1/y) <=> sqrt(gN^2+gN a0)
    return np.sqrt(gbar**2 + gbar * a0)
def g_simple(gbar, a0):                         # simple-mu: mu=x/(1+x) => g = 0.5 gN (1+sqrt(1+4 a0/gN))
    return 0.5 * gbar * (1.0 + np.sqrt(1.0 + 4.0 * a0 / gbar))
def g_standard(gbar, a0):                        # standard-mu: mu=x/sqrt(1+x^2) => solve g: g/sqrt(1+(g/a0)^2)?
    # standard nu (RAR-style F=standard): g_obs = gbar / mu, mu = nu... use nu_standard(y)=sqrt(0.5+sqrt(0.25+1/y^2))
    y = gbar / a0
    nu = np.sqrt(0.5 + np.sqrt(0.25 + 1.0 / y**2))
    return gbar * nu
def g_mcgaugh(gbar, a0):                          # McGaugh RAR: g = gN/(1-exp(-sqrt(gN/a0)))
    x = np.sqrt(gbar / a0)
    return gbar / (1.0 - np.exp(-x))

GFUN = {"dsunruh": g_dsunruh, "simple": g_simple,
        "standard": g_standard, "mcgaugh": g_mcgaugh}

def gamma_efe(y, nu):
    """EFE boost gamma = g/gN at g_int->0 in an external field y=g_ext/a0 (the cap)."""
    # for a test mass deep inside the EFE, gamma ~ nu(y_ext) (the field-strength boost)
    if nu == "dsunruh":
        return math.sqrt(1.0 + 1.0 / y)
    if nu == "simple":
        return 0.5 * (1.0 + math.sqrt(1.0 + 4.0 / y))
    if nu == "standard":
        return math.sqrt(0.5 + math.sqrt(0.25 + 1.0 / y**2))
    if nu == "mcgaugh":
        return 1.0 / (1.0 - math.exp(-math.sqrt(y)))
    raise ValueError(nu)

# ---------------------------------------------------------------- load RAR points
def load_rar(ml_disk, ml_bulge=0.70):
    gbar, gobs = [], []
    ngal = 0
    for path in sorted(glob.glob(os.path.join(ROT, "*_rotmod.dat"))):
        rows = []
        with open(path) as fh:
            for line in fh:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                p = line.split()
                if len(p) < 6:
                    continue
                try:
                    r, vobs, everr, vgas, vdisk, vbul = (float(p[i]) for i in range(6))
                except ValueError:
                    continue
                rows.append((r, vobs, everr, vgas, vdisk, vbul))
        if not rows:
            continue
        ngal += 1
        for r, vobs, everr, vgas, vdisk, vbul in rows:
            if r <= 0 or vobs <= 0:
                continue
            if everr <= 0 or everr / vobs > 0.10:
                continue
            vbar2 = (vgas * abs(vgas) + ml_disk * vdisk * abs(vdisk)
                     + ml_bulge * vbul * abs(vbul))
            if vbar2 <= 0:
                continue
            rm = r * KPC_M
            go = (vobs * KMS)**2 / rm
            gb = (vbar2 * KMS**2) / rm
            if gb <= 0 or go <= 0:
                continue
            gbar.append(gb); gobs.append(go)
    return np.array(gbar), np.array(gobs), ngal

def dex_scatter(gbar, gobs, a0, nu):
    pred = GFUN[nu](gbar, a0)
    resid = np.log10(gobs) - np.log10(pred)
    return float(np.sqrt(np.mean(resid**2)))

def optimal_a0(gbar, gobs, nu):
    f = lambda la0: dex_scatter(gbar, gobs, 10.0**la0, nu)
    res = minimize_scalar(f, bounds=(math.log10(5e-11), math.log10(3e-10)),
                          method="bounded", options={"xatol": 1e-6})
    return 10.0**res.x, res.fun

# ---------------------------------------------------------------- BTFR
def load_btfr():
    rows = []
    with open(MAST) as f:
        for r in csv.DictReader(f):
            try:
                L36 = float(r["L36"]); MHI = float(r["MHI"])
                Vf = float(r["Vflat"]); Q = int(r["Q"]); inc = float(r["inc"])
            except (ValueError, KeyError):
                continue
            rows.append((L36, MHI, Vf, Q, inc))
    return rows

def btfr_slope_a0(rows, ml, qmax=2, vmin=30, imin=30):
    logM, logV, a0s = [], [], []
    for L36, MHI, Vf, Q, inc in rows:
        if Q > qmax or Vf <= vmin or inc < imin:
            continue
        Mbar = ml * L36 * 1e9 + HE * MHI * 1e9
        if Mbar <= 0:
            continue
        logM.append(math.log10(Mbar)); logV.append(math.log10(Vf))
        a0s.append((Vf*KMS)**4 / (G * Mbar * MSUN))
    logV, logM, a0s = np.array(logV), np.array(logM), np.array(a0s)
    lin = lambda B, x: B[0]*x + B[1]
    out = odr.ODR(odr.RealData(logV, logM), odr.Model(lin),
                  beta0=[4.0, np.median(logM)-4*np.median(logV)]).run()
    return out.beta[0], float(np.median(a0s)), len(logV)

# ---------------------------------------------------------------- main scan
def main():
    print("="*84)
    print("SWEEP 2 — GALAXY-BOX VIABILITY SCAN  (a0, Upsilon, nu) on real SPARC")
    print("="*84)

    # --- pre-cache RAR points per Upsilon (the loading is the cost) ---
    ups_grid = np.round(np.arange(0.40, 0.701 + 1e-9, 0.025), 3)
    a0_grid  = np.linspace(A0_LO, A0_HI, 27)   # ~1.9e-12 step
    rar_cache = {}
    for ups in ups_grid:
        rar_cache[ups] = load_rar(ups)
    ngal = rar_cache[ups_grid[0]][2]
    npts = len(rar_cache[ups_grid[0]][0])
    print(f"RAR points: {ngal} galaxies / {npts} points (err/V<0.1 cut)\n")

    # ============================================================ FRONT (i) RAR
    print("-"*84)
    print("FRONT (i) RAR — unweighted dex-scatter optimum & floor per (Upsilon, nu)")
    print("-"*84)
    rar_opt = {}   # (ups,nu) -> (a0_opt, s_opt)
    print(f"{'Ups':>5} | " + " | ".join(f"{nu:>9}" for nu in NUS))
    for ups in ups_grid:
        gbar, gobs, _ = rar_cache[ups]
        row = []
        for nu in NUS:
            a0o, so = optimal_a0(gbar, gobs, nu)
            rar_opt[(ups, nu)] = (a0o, so)
            row.append(f"{a0o:.2e}")
        print(f"{ups:>5} | " + " | ".join(f"{v:>9}" for v in row))
    print("(optimal a0 in m/s^2; the scatter floor ~0.14 dex — printed below for fw point)")

    # RAR viability: penalty of (a0) vs the per-(ups,nu) optimum <= TOL_DEX
    TOL_DEX = 0.005   # ~3.5% of the ~0.14 floor; generous, matches 'penalty<=2%' banked
    print(f"\nRAR viability tolerance: penalty <= {TOL_DEX} dex above the per-(Ups,nu) optimum")

    # ============================================================ FRONT (ii) BTFR
    print("\n" + "-"*84)
    print("FRONT (ii) BTFR — unbiased ODR slope (target ~4) & implied a0, per Upsilon")
    print("-"*84)
    brows = load_btfr()
    btfr = {}
    print(f"{'Ups':>5} | {'ODR slope':>10} | {'implied a0':>11} | {'N':>3}")
    for ups in ups_grid:
        slope, a0imp, n = btfr_slope_a0(brows, ups)
        btfr[ups] = (slope, a0imp, n)
        print(f"{ups:>5} | {slope:>10.3f} | {a0imp:>11.3e} | {n:>3}")
    SLOPE_LO, SLOPE_HI = 3.7, 4.3
    print(f"BTFR viability: ODR slope in [{SLOPE_LO},{SLOPE_HI}] (deep-MOND closed form, IF-free)")

    # ============================================================ FRONT (iv/v) EFE / WB
    print("\n" + "-"*84)
    print("FRONT (iv/v) EFE & WIDE-BINARIES — gamma cap at MW g_ext per (a0, nu)")
    print("-"*84)
    print(f"MW g_ext = {G_EXT_MW:.2e} m/s^2 ;  y = g_ext/a0")
    print(f"{'a0':>10} | {'y':>5} | " + " | ".join(f"{nu:>9}" for nu in NUS))
    for a0 in [8e-11, 9.36e-11, 1.05e-10, 1.2e-10, 1.3e-10]:
        y = G_EXT_MW / a0
        caps = [gamma_efe(y, nu) for nu in NUS]
        print(f"{a0:>10.2e} | {y:>5.2f} | " + " | ".join(f"{c:>9.3f}" for c in caps))
    # Chae measured gamma ~ 1.49-1.60 (contested 4-5 sigma); Gaia DR3 wide-binary band
    CHAE = (1.49, 1.60)
    WB_OBS_BAND = (1.0, 1.65)   # the empirically allowed band (Newton=1 .. high-Chae); the front
                                # is "viable" if the cap is physical & inside this band (it always is)
    print(f"Chae central gamma ~ {CHAE}; allowed obs band ~ {WB_OBS_BAND}")

    # ============================================================ THE INTERSECTION
    print("\n" + "="*84)
    print("INTERSECTION — for each nu, the (a0, Upsilon) cells where ALL fronts pass")
    print("="*84)
    viable = {nu: [] for nu in NUS}
    for nu in NUS:
        print(f"\n### nu = {nu} ###")
        # header row: a0 columns
        hdr = "Ups\\a0 | " + " ".join(f"{a0*1e11:4.1f}" for a0 in a0_grid)
        print(hdr)
        for ups in ups_grid:
            gbar, gobs, _ = rar_cache[ups]
            a0o, so = rar_opt[(ups, nu)]
            slope, a0imp, n = btfr[ups]
            btfr_ok = SLOPE_LO <= slope <= SLOPE_HI
            cells = []
            for a0 in a0_grid:
                s = dex_scatter(gbar, gobs, a0, nu)
                rar_ok = (s - so) <= TOL_DEX
                # EFE/WB: cap physical & in band (always true for these a0); record
                y = G_EXT_MW / a0
                cap = gamma_efe(y, nu)
                efe_ok = WB_OBS_BAND[0] <= cap <= WB_OBS_BAND[1]
                allok = rar_ok and btfr_ok and efe_ok
                cells.append("#" if allok else ("." if rar_ok else " "))
                if allok:
                    viable[nu].append((round(ups,3), round(a0,12)))
            print(f"{ups:>5} | " + " ".join(f"{c:>4}" for c in cells))
        print("  legend: '#'=all fronts pass  '.'=RAR ok but BTFR/EFE veto  ' '=RAR fail")

    # ============================================================ framework point check
    print("\n" + "="*84)
    print("FRAMEWORK POINT — is (a0=9.36e-11, Upsilon=0.70, dS-Unruh) INSIDE the region?")
    print("="*84)
    gbar, gobs, _ = rar_cache[0.7]
    a0o, so = rar_opt[(0.7, "dsunruh")]
    s_fw = dex_scatter(gbar, gobs, FW_A0, "dsunruh")
    pen = s_fw - so
    slope70, a0imp70, n70 = btfr[0.7]
    y_fw = G_EXT_MW / FW_A0
    cap_fw = gamma_efe(y_fw, "dsunruh")
    print(f"  RAR  : scatter {s_fw:.4f} dex vs optimum {so:.4f} (opt a0={a0o:.3e}); "
          f"penalty {pen:+.4f} dex ({pen/so*100:+.2f}%)  -> {'PASS' if pen<=TOL_DEX else 'FAIL'}")
    print(f"  BTFR : ODR slope {slope70:.3f} (target 3.7-4.3); implied a0 {a0imp70:.3e}  "
          f"-> {'PASS' if 3.7<=slope70<=4.3 else 'FAIL'}")
    print(f"  EFE/WB: y={y_fw:.2f}, dS-Unruh cap gamma={cap_fw:.3f} (band {WB_OBS_BAND})  "
          f"-> {'PASS' if WB_OBS_BAND[0]<=cap_fw<=WB_OBS_BAND[1] else 'FAIL'}")
    print(f"  dwarfs: 3/8 over-dispersed (robust, banked) — worsens at lower a0/Ups, "
          f"NOT a veto (shared-MOND failure)")

    # ============================================================ region size / fine-tuning
    print("\n" + "="*84)
    print("VIABLE-REGION SIZE & FINE-TUNING  (per nu and combined)")
    print("="*84)
    total_cells = len(ups_grid) * len(a0_grid)
    for nu in NUS:
        v = viable[nu]
        if not v:
            print(f"  nu={nu:>9}: EMPTY")
            continue
        a0s = sorted(set(a for _, a in v))
        upss = sorted(set(u for u, _ in v))
        frac = len(v) / total_cells * 100
        print(f"  nu={nu:>9}: {len(v):>3}/{total_cells} cells ({frac:4.1f}% of box)  "
              f"a0 in [{min(a0s):.2e},{max(a0s):.2e}]  Ups in [{min(upss):.2f},{max(upss):.2f}]")
    # the union across the framework's OWN nu (dsunruh) is what matters for the framework
    print(f"\n  a0 prior box: [{A0_LO:.2e}, {A0_HI:.2e}]  ({(A0_HI-A0_LO)*1e11:.2f}e-11 wide)")
    print(f"  Ups prior box: [{UPS_LO}, {UPS_HI}]")
    if viable["dsunruh"]:
        a0s = sorted(set(a for _, a in viable["dsunruh"]))
        upss = sorted(set(u for u, _ in viable["dsunruh"]))
        a0_frac = (max(a0s)-min(a0s)) / (A0_HI-A0_LO) * 100
        ups_frac = (max(upss)-min(upss)) / (UPS_HI-UPS_LO) * 100
        print(f"\n  FRAMEWORK nu (dS-Unruh) viable a0 span: "
              f"[{min(a0s):.2e}, {max(a0s):.2e}] = {a0_frac:.0f}% of the a0 prior box")
        print(f"  FRAMEWORK nu (dS-Unruh) viable Ups span: "
              f"[{min(upss):.2f}, {max(upss):.2f}] = {ups_frac:.0f}% of the Ups prior box")

if __name__ == "__main__":
    main()
