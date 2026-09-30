#!/usr/bin/env python3
"""CFG212 -- BUDHIES external-field POWER pre-flight: can HI widths near A963 / A2192 separate an EFE-merge law from B's isolated law?
Frozen criteria: FROZEN_CRITERIA.md here (6df482512), committed before any number.  kappa = 1/2 FITTED, NOT DERIVED.
Uses positions, HI redshifts and published cluster masses only.  The W20 / W50 columns are NEVER read by this script.
S_opt = sqrt(sum Delta_i^2) / sigma is an UPPER bound on any real test's separation (optimal known-template test).
Run:  python3 campaign_fresh_gravity/CFG212_budhies_efe_preflight/cfg212_budhies_preflight.py      (MUTATE=1: A963 mass x 100)
"""
import os, sys, csv, math, itertools
sys.dont_write_bytecode = True
import numpy as np
from scipy.integrate import quad
from scipy.optimize import brentq

LANE = os.path.dirname(os.path.abspath(__file__))
CFG = os.path.dirname(LANE)
REPO = os.path.dirname(CFG)
sys.path.insert(0, CFG)
_mut = os.environ.pop("MUTATE", None)
try:
    import CFG4_common as K
    import CFG7_common as C
finally:
    if _mut is not None:
        os.environ["MUTATE"] = _mut
MODE = (_mut or "").strip()
assert MODE in ("", "0", "1")
MUT = MODE == "1"
R = C.Report("cfg212_budhies_preflight", MUT)
P, check = R.P, R.check
P(__doc__.split("Run:")[0].strip())

CKMS, G, MSUN, MPC = 299792.458, 6.67430e-11, 1.98847e30, 3.0856775814913673e22
H0, OM = 70.0, 0.3
A0 = {"canonical": K.A0["canonical"], "alt": K.A0["alt"]}
KER = {"P2": K.nu_p2, "nu_mono": K.nu_mono}


def E(z):
    return math.sqrt(OM * (1 + z) ** 3 + 1 - OM)


def DA_mpc(z):
    dc = CKMS / H0 * quad(lambda x: 1 / E(x), 0, z)[0]
    return dc / (1 + z)


def hms(h, m, s):
    return 15 * (float(h) + float(m) / 60 + float(s) / 3600)


def dms(sign, d, m, s):
    v = float(d) + float(m) / 60 + float(s) / 3600
    return -v if sign.strip() == "-" else v


def sep_rad(ra1, de1, ra2, de2):
    ra1, de1, ra2, de2 = map(np.radians, (ra1, de1, ra2, de2))
    s = np.sin((de2 - de1) / 2) ** 2 + np.cos(de1) * np.cos(de2) * np.sin((ra2 - ra1) / 2) ** 2
    return 2 * np.arcsin(np.sqrt(s))


CL = {"A963": dict(z=0.206, ra=hms(10, 17, 14.22), dec=dms(" ", 39, 1, 22.1), M=8.92e14, M_opt=1.4e15, sig=993.0, sig_opt=1350.0),
      "A2192": dict(z=0.188, ra=hms(16, 26, 36.99), dec=dms(" ", 42, 40, 10.1), M=2.27e14, M_opt=2.3e14 / 0.7, sig=653.0, sig_opt=653.0,
                    ra_alt=246.64774, dec_alt=42.727723)}
if MUT:
    CL["A963"]["M"] *= 100
    CL["A963"]["M_opt"] *= 100
    P("  MUTATE=1: A963 mass x 100")
C200 = 4.0

# ---- read ONLY the needed columns (never W20 / W50)
NEED = ("cluster", "rah", "ram", "ras", "de_sign", "ded", "dem", "des", "z_hi", "mhi_1e9msun")
gal = []
with open(os.path.join(REPO, "data_assembly", "high_z_tf_tables", "budhies_joined.csv"), newline="") as f:
    for r in csv.DictReader(f):
        gal.append({k: r[k] for k in NEED})
P(f"  {len(gal)} HI detections read (columns {', '.join(NEED)}; W20/W50 not read)")


def nfw_mass(M200, z, r_mpc):
    rhoc = 3 * (H0 * 1e3 / MPC * E(z)) ** 2 / (8 * math.pi * G)
    R200 = (3 * M200 * MSUN / (4 * math.pi * 200 * rhoc)) ** (1 / 3) / MPC
    rs = R200 / C200
    m = lambda x: math.log(1 + x) - x / (1 + x)
    return M200 * m(r_mpc / rs) / m(C200), R200


def y_ext_of(g_obs, a0, nu):
    q = g_obs / a0
    if q <= 0:
        return 0.0
    return brentq(lambda ly: float(nu(np.array([10 ** ly]))[0]) * 10 ** ly - q, -12, 12, xtol=1e-14, rtol=1e-14)


def delta(y_int, y_e, nu, form):
    y_e = 10 ** y_e if y_e != 0.0 else 0.0
    g_iso = float(nu(np.array([y_int]))[0]) * y_int
    if y_e == 0.0:
        return 0.0
    if form == "perp":
        g_efe = float(nu(np.array([math.hypot(y_int, y_e)]))[0]) * y_int
    else:
        g_efe = float(nu(np.array([y_int + y_e]))[0]) * (y_int + y_e) - float(nu(np.array([y_e]))[0]) * y_e
    return 0.5 * math.log10(g_efe / g_iso)


# ------------------------------------------------------------------------------------------------ controls
R.banner("CONTROLS")
check("C1 with the cluster masses set to 0 every Delta = 0 (no external field)", "delta(0.3, y_ext = 0) = " + f"{delta(0.3, 0.0, K.nu_p2, 'perp')}",
      delta(0.3, 0.0, K.nu_p2, "perp") == 0.0)
lim = []
for nm, nu in KER.items():
    lim.append((nm, float(nu(np.array([1e9]))[0]), float(np.sqrt(1e-9) * nu(np.array([1e-9]))[0])))
ye_big = math.log10(1e6)
strong = delta(0.3, ye_big, K.nu_p2, "perp")
want = 0.5 * math.log10(float(K.nu_p2(np.array([math.hypot(0.3, 1e6)]))[0]) / float(K.nu_p2(np.array([0.3]))[0]))
check("C2 kernel limits nu(1e9) -> 1, sqrt(y) nu(y) -> 1 at y = 1e-9; strong-field EFE ratio -> nu(y_ext)/nu(y_int)",
      f"{lim}; strong-field Delta {strong:.6f} vs {want:.6f}",
      all(abs(a - 1) < 1e-3 and abs(b - 1) < 1e-3 for _, a, b in lim) and abs(strong - want) < 1e-9)
g0 = gal[0]; c0 = CL[g0["cluster"]]
ra0, de0 = hms(g0["rah"], g0["ram"], g0["ras"]), dms(g0["de_sign"], g0["ded"], g0["dem"], g0["des"])
from astropy.coordinates import SkyCoord
import astropy.units as u
th_ast = SkyCoord(ra0 * u.deg, de0 * u.deg).separation(SkyCoord(c0["ra"] * u.deg, c0["dec"] * u.deg)).radian
Rmine = float(sep_rad(ra0, de0, c0["ra"], c0["dec"])) * DA_mpc(c0["z"])
check("C3 R_proj of the table's first galaxy: haversine vs astropy's separation, times D_A, agree to 1e-6 Mpc",
      f"{Rmine:.9f} vs {th_ast * DA_mpc(c0['z']):.9f} Mpc", abs(Rmine - th_ast * DA_mpc(c0["z"])) < 1e-6)

# ------------------------------------------------------------------------------------------------ geometry and membership
DA = {k: DA_mpc(v["z"]) for k, v in CL.items()}


def members(sig_key, alt_centre=False):
    out = []
    for g in gal:
        c = CL[g["cluster"]]
        z = float(g["z_hi"])
        dv = CKMS * abs(z - c["z"]) / (1 + c["z"])
        ra, de = hms(g["rah"], g["ram"], g["ras"]), dms(g["de_sign"], g["ded"], g["dem"], g["des"])
        rc, dc = (c["ra_alt"], c["dec_alt"]) if (alt_centre and "ra_alt" in c) else (c["ra"], c["dec"])
        Rp = float(sep_rad(ra, de, rc, dc)) * DA[g["cluster"]]
        out.append(dict(cl=g["cluster"], R=Rp, member=dv < 3 * c[sig_key], dv=dv))
    return out


def s_opt(mem, mass_key, deproj, y_int, sig, form, nu, foot):
    ds = []
    for m in mem:
        if not m["member"]:
            ds.append(0.0); continue
        c = CL[m["cl"]]
        r = max(m["R"] * deproj, 1e-3)
        Menc, _ = nfw_mass(c[mass_key], c["z"], r)
        g_obs = G * Menc * MSUN / (r * MPC) ** 2
        ly = y_ext_of(g_obs, A0[foot], nu)
        ds.append(delta(y_int, ly, nu, form))
    ds = np.array(ds)
    return math.sqrt(float(np.sum(ds ** 2))) / sig, ds


mem_p = members("sig")
mem_o = members("sig_opt")
for cl in CL:
    mm = [m for m in mem_p if m["cl"] == cl]
    P(f"  {cl}: {len(mm)} detections in its field; members (|dv| < 3 sigma) {sum(m['member'] for m in mm)}; members within 1 / 2 Mpc projected: "
      f"{sum(m['member'] and m['R'] < 1 for m in mm)} / {sum(m['member'] and m['R'] < 2 for m in mm)}; median R of members "
      f"{np.median([m['R'] for m in mm if m['member']]):.2f} Mpc (D_A {DA[cl]:.0f} Mpc)")

R.banner("POWER")
S_p, d_p = s_opt(mem_p, "M", math.sqrt(1.5), 0.3, 0.20, "perp", K.nu_p2, "canonical")
S_o, d_o = s_opt(mem_o, "M_opt", 1.0, 0.1, 0.15, "perp", K.nu_p2, "canonical")
inner = np.array([m["member"] and m["R"] < 1 for m in mem_p])
P(f"  PRIMARY cell (M200 primary, r = sqrt(1.5) R, y_int 0.3, sigma 0.20, perpendicular, P2, canonical): S_opt = {S_p:.2f}; "
  f"median Delta over members {np.median(d_p[[m['member'] for m in mem_p]]):+.4f}, min {d_p.min():+.4f} dex; share of sum Delta^2 "
  f"from members within 1 Mpc {np.sum(d_p[inner] ** 2) / max(np.sum(d_p ** 2), 1e-30):.2f}")
P(f"  OPTIMISTIC cell (M high, r = R, y_int 0.1, sigma 0.15, A963 membership sigma 1350, perpendicular, P2, canonical): S_opt = {S_o:.2f}; "
  f"min Delta {d_o.min():+.4f} dex")
grid = []
for mk, dp, yi, sg, fm, kn, ft, ac, sk in itertools.product(("M", "M_opt"), (math.sqrt(1.5), 1.0), (0.3, 0.1, 1.0), (0.20, 0.15), ("perp", "par"),
                                                             ("P2", "nu_mono"), ("canonical", "alt"), (False, True), ("sig", "sig_opt")):
    mem = members(sk, alt_centre=ac)
    s, _ = s_opt(mem, mk, dp, yi, sg, fm, KER[kn], ft)
    grid.append(dict(mass=mk, deproj=round(dp, 4), y_int=yi, sigma=sg, form=fm, kernel=kn, footing=ft, A2192_alt_centre=ac, membership=sk, S=s))
Smax = max(g["S"] for g in grid)
best = max(grid, key=lambda g: g["S"])
P(f"  full grid: {len(grid)} cells; S_opt max {Smax:.2f} at {best}; cells with S_opt >= 3: {sum(g['S'] >= 3 for g in grid)}; >= 2: "
  f"{sum(g['S'] >= 2 for g in grid)}")
if S_o < 3:
    verdict = "P1: NON-DIAGNOSTIC (S_opt < 3 even in the optimistic cell): no W50 test is frozen"
elif S_p >= 3:
    verdict = "P2: a W50 test may be frozen next (S_opt >= 3 in the primary cell)"
else:
    verdict = "power only under optimistic inputs: not run unless the inputs are tightened"
P(f"\n  -> {verdict}")
P("  Note (from the data chat's note): the HI-mass limit (2e9 Msun at the field centres) rises away from the field centres, so the outer "
  "members are the more massive HI discs; HI-deficient cluster cores lower the number of inner members.")
if MUT:
    # (added after the first MUTATE run, kept as *_MUTATE_firstrun*: that run printed S_opt 6.55 against the main run's 1.04 but did
    #  not state the frozen control as a check; the check below recomputes the unmutated primary cell in-process)
    CL["A963"]["M"] /= 100          # (second fix, kept as *_MUTATE_secondrun*: that run divided BOTH clusters' masses, so its
                                    #  unmutated reference printed 1.02 instead of the main run's 1.04; the check passed either way)
    S_un, _ = s_opt(members("sig"), "M", math.sqrt(1.5), 0.3, 0.20, "perp", K.nu_p2, "canonical")
    check("MUTATE: with the A963 mass x 100 the primary-cell S_opt rises above its unmutated value", f"{S_un:.2f} -> {S_p:.2f}", S_p > S_un)
R.num("primary", dict(S=S_p)); R.num("optimistic", dict(S=S_o)); R.num("grid_max", best); R.num("verdict", verdict)
R.num("grid", grid)
R.write(here=LANE)
