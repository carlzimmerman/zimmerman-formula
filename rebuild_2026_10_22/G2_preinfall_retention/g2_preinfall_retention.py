"""G2_preinfall_retention -- PAPER36's collapse-mass retention rule ("the cold component keeps its collapse mass"),
transplanted to dwarf satellites as a pre-infall retention rule (zeta = 1 pre-infall, zeta = 0 post-infall / stripped).
Criteria: FROZEN_CRITERIA.md (92716d0148; A1 b3fbb9ed9d). Ledger: ASSUMPTION_LEDGER.md.

Run:  OMP_NUM_THREADS=1 nice -n 15 python3 g2_preinfall_retention.py            -> g2_preinfall_retention.out, _results.json,
                                                                                    g2_per_system.csv
      OMP_NUM_THREADS=1 nice -n 15 python3 g2_preinfall_retention.py --mutate   -> *_MUTATE.*  (M_coll -> 0 everywhere)
Deterministic (seeded), no network, seconds. kappa = 1/2 FITTED; not theory closed; cold energy, no particle."""
import csv, json, math, os, sys
import numpy as np
np.seterr(over="ignore", divide="ignore", invalid="ignore")
from scipy.integrate import quad
from scipy.optimize import brentq

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
DATA = os.path.join(REPO, "real_research", "data")
CFG = os.path.join(REPO, "campaign_fresh_gravity")
E3D = os.path.join(REPO, "doors_push_2026_10_22", "E3_dwarf_excess")
E6D = os.path.join(REPO, "doors_push_2026_10_22", "E6_native_fret")
MUT = "--mutate" in sys.argv
SFX = "_MUTATE" if MUT else ""

# ------------------------------------------------------------------ constants (ledger)
G, MSUN, PC = 6.67430e-11, 1.989e30, 3.0856775814913673e16
KPC, MPC = 1e3 * PC, 1e6 * PC
A0 = {"canonical": 9.3603e-11, "alt": 1.1312e-10}          # kappa = 1/2 FITTED
LSTAR_PC = 24.0                                            # CFG820 / E3
SUP = 5.364                                                # Omega_c/Omega_b (Planck; CFG886) -- LCDM-PROCESSED
FB = 1.0 / (1.0 + SUP)                                     # Omega_b/Omega_m
FRET_CENSUS = 0.10                                         # CFG416 census -- LCDM-PROCESSED
MHOST = {"MW": 6.0e10, "M31": 1.0e11}                      # E3/E6 (CFG332; external)
H_NAT, OM_NAT = 0.674, 0.313                               # E6 / CFG654 native column (h 0.67403, Omega_cb 0.31285)
OL_NAT = 1.0 - OM_NAT
H0SI = H_NAT * 100e3 / MPC
RHOC0 = 3 * H0SI ** 2 / (8 * math.pi * G) / MSUN * PC ** 3          # Msun / pc^3
RHOM0 = OM_NAT * RHOC0
T0 = 2.0 / (3.0 * math.sqrt(OL_NAT) * H0SI) * math.asinh(math.sqrt(OL_NAT / OM_NAT))  # s
GYR = 3.15576e16
RTA0 = {"MWonly": 0.83, "LG": 1.10}                        # Mpc; CFG548 K4 1.05-1.09 LG; MW-only scaled by (1/2)^(1/3)
ZC = (6.0, 10.0, 15.0)
ST_s = np.array([0.01, 0.1, 0.3, 1, 3, 10, 100, 1000])     # CFG691 screening table (as E3)
ST_S = np.array([0.0050, 0.048, 0.134, 0.358, 0.663, 0.894, 0.990, 0.998999])
NMC, NBOOT = 500, 3000
RNG = np.random.default_rng(20261022 + 2)

OUT = []
def P(s=""):
    print(s, flush=True); OUT.append(str(s))

def fl(x):
    try:
        v = float(x); return v if math.isfinite(v) else None
    except Exception:
        return None

def nu(y):
    y = np.maximum(np.asarray(y, float), 1e-30)
    return 0.5 * (1.0 + np.sqrt(1.0 + 4.0 / y))

def Sfun(s):
    s = np.asarray(s, float)
    out = np.interp(np.log(np.clip(s, 0.01, 1000)), np.log(ST_s), ST_S)
    out = np.where(s <= 0.01, s / 2, out)
    return np.where(s >= 1000, 1 - 1 / np.maximum(s, 1e-300), out)

def B_scr(Ms, r12, a0, Lstar_pc=LSTAR_PC):
    """E3/CFG820 recipe at r12 with M*/2 enclosed: 1 + S(r12/l)(nu - 1). Ms Msun, r12 m."""
    gb = G * (Ms / 2) * MSUN / r12 ** 2
    nv = nu(gb / a0)
    if Lstar_pc is None:
        return nv
    rM = np.sqrt(G * Ms * MSUN / a0)
    lg = (Lstar_pc * PC) ** 2 / (2 * rM)
    return 1 + Sfun(r12 / lg) * (nv - 1)

def Mb_plummer(Ms, Re, r):
    """Plummer baryons, scale a = R_e (projected half-light); Ms, r, Re consistent units (Msun, m)."""
    return Ms * r ** 3 / (r ** 2 + Re ** 2) ** 1.5

def Mph(Ms, Re, r, a0, Lstar_pc=LSTAR_PC):
    """screened tethered phantom inside r (Msun): M_b(<r) S(r/l)(nu(y(r)) - 1)."""
    mb = Mb_plummer(Ms, Re, r)
    nv = nu(G * mb * MSUN / r ** 2 / a0)
    if Lstar_pc is None:
        return mb * (nv - 1)
    rM = np.sqrt(G * Ms * MSUN / a0)
    lg = (Lstar_pc * PC) ** 2 / (2 * rM)
    return mb * Sfun(r / lg) * (nv - 1)

# ------------------------------------------------------------------ native background / collapse
def rho_m(z):
    return RHOM0 * (1 + z) ** 3

def a_of_t(t):
    return (OM_NAT / OL_NAT) ** (1 / 3) * np.sinh(1.5 * math.sqrt(OL_NAT) * H0SI * t) ** (2 / 3)

def z_of_t(t):
    return 1.0 / a_of_t(t) - 1.0

def t_of_z(z):
    a = 1.0 / (1 + z)
    return 2.0 / (3.0 * math.sqrt(OL_NAT) * H0SI) * np.arcsinh(np.sqrt(OL_NAT / OM_NAT) * a ** 1.5)

def r_vir_pc(Mcoll, zc):
    return (3 * Mcoll / (4 * math.pi * 18 * math.pi ** 2 * rho_m(zc))) ** (1 / 3)

def m_profile(prof, Mcoll, r_pc, zc):
    """fraction of M_coll inside r (pc)."""
    Mcoll = np.maximum(np.asarray(Mcoll, float), 1e-30)
    if prof == "TH":
        return np.minimum(1.0, (r_pc / r_vir_pc(Mcoll, zc)) ** 3)
    if prof == "B85":
        return np.minimum(1.0, (r_pc / r_vir_pc(Mcoll, zc)) ** 0.75)
    if prof == "NFW":   # h48 / PAPER36: Dutton-Maccio c(M) z = 0, R200c, x clipped [1e-4, 5]
        c = 10 ** (0.905 - 0.101 * (np.log10(Mcoll * H_NAT) - 12.0))
        R200 = (3 * Mcoll / (4 * math.pi * 200 * RHOC0)) ** (1 / 3)
        x = np.clip(r_pc / R200, 1e-4, 5.0)
        m = lambda t: np.log1p(t) - t / (1 + t)
        return m(c * x) / m(c)
    raise ValueError(prof)

def moster_mstar(logMh):
    N, logM1, be, ga = 0.0351, 11.590, 1.376, 0.608           # h48 L83-86 (Moster+13 z = 0)
    x = 10 ** (logMh - logM1)
    return 10 ** logMh * 2 * N / (x ** (-be) + x ** ga)
_LMH = np.linspace(5.0, 15.5, 4201); _LMS = np.log10(moster_mstar(_LMH))
def shmr_halo(Ms):                                              # extrapolated below h48's 1e9 grid floor (labelled)
    return 10 ** np.interp(np.log10(np.asarray(Ms, float)), _LMS, _LMH)

# ------------------------------------------------------------------ host law field, Jacobi radius, orbits
def g_host(Mh, r_m, a0):
    gN = G * Mh * MSUN / r_m ** 2
    return nu(gN / a0) * gN

def tidal_k(Mh, D_m, a0):
    """Omega^2 - dg/dr at D (s^-2), host law field (point baryons)."""
    g = g_host(Mh, D_m, a0); h = 1e-4 * D_m
    dg = (g_host(Mh, D_m + h, a0) - g_host(Mh, D_m - h, a0)) / (2 * h)
    return g / D_m - dg

def r_tidal_pc(Msat_fn, k, lo=0.1, hi=1e6, it=80):
    """solve Msat(r) = k r^3 / G for r (pc), vectorised bisection in log r. Msat_fn(r_pc) -> Msun (array)."""
    lo = np.full_like(k, math.log(lo)); hi = np.full_like(k, math.log(hi))
    for _ in range(it):
        mid = 0.5 * (lo + hi); r = np.exp(mid)
        f = Msat_fn(r) * MSUN * G - k * (r * PC) ** 3
        lo = np.where(f > 0, mid, lo); hi = np.where(f > 0, hi, mid)
    return np.exp(0.5 * (lo + hi))

def Phi_host(r_kpc, Mh, a0, rref=1.0):
    return quad(lambda x: float(g_host(Mh, x * KPC, a0)) * KPC, rref, r_kpc, limit=200)[0]

def peri_apo(rk, vr, vt, Mh, a0):
    """rk kpc, v km/s -> (r_peri, r_apo) kpc in the host law field; residual check."""
    E = 0.5 * ((vr * 1e3) ** 2 + (vt * 1e3) ** 2) + Phi_host(rk, Mh, a0)
    L = rk * KPC * vt * 1e3
    f = lambda x: E - Phi_host(x, Mh, a0) - L ** 2 / (2 * (x * KPC) ** 2)
    rp = brentq(f, 1e-3, rk, xtol=1e-12, rtol=1e-14) if f(rk) > 0 and f(1e-3) < 0 else rk
    hi = rk * 1.01
    while f(hi) > 0:
        hi *= 2
    ra = brentq(f, rk, hi, xtol=1e-12, rtol=1e-14) if f(rk) > 0 else rk
    res = max(abs(f(rp)), abs(f(ra))) / max(abs(E), 1e-30)
    return rp, ra, res

def galcen(r):
    from astropy.coordinates import SkyCoord, Galactocentric, CartesianDifferential
    import astropy.units as u
    c = SkyCoord(ra=r["ra"] * u.deg, dec=r["dec"] * u.deg, distance=r["dist"] * u.kpc, pm_ra_cosdec=r["pmra"] * u.mas / u.yr,
                 pm_dec=r["pmdec"] * u.mas / u.yr, radial_velocity=r["vsys"] * u.km / u.s)
    gc = c.transform_to(Galactocentric(galcen_distance=8.122 * u.kpc, z_sun=20.8 * u.pc,
                                       galcen_v_sun=CartesianDifferential([12.9, 245.6, 7.78] * u.km / u.s)))
    x = np.array([gc.x.to(u.kpc).value, gc.y.to(u.kpc).value, gc.z.to(u.kpc).value])
    v = np.array([gc.v_x.to(u.km / u.s).value, gc.v_y.to(u.km / u.s).value, gc.v_z.to(u.km / u.s).value])
    rr = float(np.linalg.norm(x)); vr = float(np.dot(x, v) / rr); vt = float(math.sqrt(max(np.dot(v, v) - vr ** 2, 0.0)))
    return rr, vr, vt

# ------------------------------------------------------------------ data (own loader from LVD; E3's recipe)
def load_lvd():
    rows = []
    for fn, host in (("lvd_dwarf_mw.csv", "MW"), ("lvd_dwarf_m31.csv", "M31"), ("lvd_dwarf_local_field.csv", "field")):
        for r in csv.DictReader(open(os.path.join(DATA, "dsph", fn))):
            s = fl(r.get("vlos_sigma"))
            rh = fl(r.get("rhalf_sph_physical")) or fl(r.get("rhalf_physical"))
            ms = fl(r.get("mass_stellar")); mv = fl(r.get("M_V"))
            if not s or s <= 0 or not rh or rh <= 0:
                continue
            if ms is None and mv is not None:
                ms = 0.4 * (4.83 - mv) + 0.301
            if ms is None:
                continue
            sph = fl(r.get("rhalf_sph_physical"))
            rhe = fl(r.get("rhalf_sph_physical_em")) if sph else fl(r.get("rhalf_physical_em"))
            rhp = fl(r.get("rhalf_sph_physical_ep")) if sph else fl(r.get("rhalf_physical_ep"))
            rows.append(dict(name=r["name"], host=host, sigma=s, sem=fl(r.get("vlos_sigma_em")) or 0.1 * s,
                             sep=fl(r.get("vlos_sigma_ep")) or 0.1 * s, ul=bool(r.get("vlos_sigma_ul")),
                             rh=rh, rhem=rhe or 0.1 * rh, rhep=rhp or 0.1 * rh, logms=ms,
                             dmem=fl(r.get("distance_modulus_em")) or 0.1, dmep=fl(r.get("distance_modulus_ep")) or 0.1,
                             dhost=fl(r.get("distance_host")), dgc=fl(r.get("distance_gc")), mhi=fl(r.get("mass_HI")),
                             ra=fl(r.get("ra")), dec=fl(r.get("dec")), dist=fl(r.get("distance")), pmra=fl(r.get("pmra")),
                             pmdec=fl(r.get("pmdec")), vsys=fl(r.get("vlos_systemic"))))
    return rows

ALL = load_lvd()
ARR = list(csv.DictReader(open(os.path.join(CFG, "CFG257_ufd_kinematics_scoping", "arroyo_polonio2026_tableA1.csv"))))
arr_free = {r["lvd_name"]: float(r["sig_free"]) / float(r["sig_f0"]) for r in ARR}
med_free = float(np.median(list(arr_free.values())))
E3CSV = {(r["footing"], r["name"]): r for r in csv.DictReader(open(os.path.join(E3D, "e3_per_system.csv")))}
E6CSV = {(r["footing"], r["name"]): r for r in csv.DictReader(open(os.path.join(E6D, "e6_per_system.csv")))}

def sample(a0, hosts=("MW", "M31", "field")):
    mcrit = a0 * (LSTAR_PC * PC) ** 2 / G / MSUN
    return [r for r in ALL if r["host"] in hosts and r["logms"] < math.log10(mcrit)]

def split_normal(c, em, ep, n):
    z = RNG.standard_normal(n)
    return c + np.where(z < 0, z * em, z * ep)

def build(rows):
    N = len(rows)
    Md = np.empty((N, NMC)); Ms_ = np.empty((N, NMC)); R12 = np.empty((N, NMC)); Re_ = np.empty((N, NMC)); fDa = np.empty((N, NMC))
    for i, r in enumerate(rows):
        b = arr_free.get(r["name"], med_free)
        fD = 10 ** (split_normal(0.0, r["dmem"], r["dmep"], NMC) / 5.0)
        sig = np.abs(split_normal(r["sigma"], r["sem"], r["sep"], NMC)) * b
        rh = np.abs(split_normal(r["rh"], r["rhem"], r["rhep"], NMC)) * fD
        ms = 10 ** r["logms"] * fD ** 2                          # Upsilon_V = 2 (LVD mass_stellar)
        r12 = (4.0 / 3.0) * rh * PC
        Md[i] = 3.0 * (sig * 1e3) ** 2 * r12 / G / MSUN; Ms_[i] = ms; R12[i] = r12; Re_[i] = rh * PC; fDa[i] = fD
    return dict(Md=Md, Ms=Ms_, r12=R12, Re=Re_, fD=fDa, rows=rows)

def boot_median(X, n=NBOOT):
    N = X.shape[0]; meds = np.empty(n)
    for k in range(n):
        idx = RNG.integers(0, N, N); col = RNG.integers(0, X.shape[1], N)
        meds[k] = np.median(X[idx, col])
    return float(np.median(meds)), float(np.std(meds))

R = dict(lane="G2_preinfall_retention", mutate=MUT, criteria="92716d0148", amendment_A1="b3fbb9ed9d",
         constants=dict(a0=A0, Lstar_pc=LSTAR_PC, sup=SUP, fb=FB, fret_census=FRET_CENSUS, mhost=MHOST, h=H_NAT, Om=OM_NAT,
                        Rta0_Mpc=RTA0, zc=ZC, nmc=NMC, nboot=NBOOT, t0_Gyr=T0 / GYR))
CHK = []
def ck(k, ok, val, thr, what):
    CHK.append((k, bool(ok))); P(f"{k} {'PASS' if ok else 'FAIL'} {val} {thr}  ({what})")

P("G2_preinfall_retention  PAPER36 collapse-mass retention transplanted to dwarf satellites" + ("  [MUTATE: M_coll -> 0]" if MUT else ""))
P(f"kappa = 1/2 FITTED; footings canonical 9.3603e-11 / alt 1.1312e-10, never pooled; native background h {H_NAT} Om {OM_NAT}, "
  f"t0 = {T0 / GYR:.3f} Gyr\n")

# ================================================================== orbits / infall epochs (central values, per system)
P("[O] infall epochs from LVD proper motions in the host law field (MW baryons 6e10 point; no EFE); M31 hosts bracketed")
ORB = {}
k4res = 0.0; dgc = []
for r in ALL:
    if r["host"] not in ("MW", "M31"):
        for foot in A0:
            ORB[(foot, r["name"])] = dict(r_now=r["dhost"], vr=None, vt=None, r_peri=None, r_apo=None, src="isolated",
                                          z_inf={k: -1.0 for k in RTA0})
        continue
    for foot, a0 in A0.items():
        if r["host"] == "MW" and None not in (r["ra"], r["dec"], r["dist"], r["pmra"], r["pmdec"], r["vsys"]):
            rr, vr, vt = galcen(r)
            if foot == "canonical" and r["dgc"]:
                dgc.append(abs(rr / r["dgc"] - 1))
            rp, ra, res = peri_apo(rr, vr, vt, MHOST["MW"], a0)
            k4res = max(k4res, res)
            src = "PM"
        else:
            d = r["dhost"] or r["dgc"] or 100.0
            rr, vr, vt = d, None, None
            rp, ra, src = 0.3 * d, 2.0 * d, "bracket"
        zinf = {}
        for k, R0 in RTA0.items():
            tinf = T0 * min(1.0, (ra / (R0 * 1e3)) ** (9 / 8))
            zinf[k] = float(z_of_t(tinf))
        ORB[(foot, r["name"])] = dict(r_now=rr, vr=vr, vt=vt, r_peri=rp, r_apo=ra, src=src, z_inf=zinf)
mdgc = float(np.median(dgc))
ck("K4", k4res <= 1e-8 and mdgc <= 0.02, f"root residual {k4res:.1e}; median |r_GC/LVD - 1| {mdgc:.4f} (N {len(dgc)})",
   "<=1e-8 & <=0.02", "orbit roots and Galactocentric transform")
zi = [v["z_inf"]["LG"] for (f, n), v in ORB.items() if f == "canonical" and v["src"] == "PM"]
P(f"   MW satellites with PMs: {len(zi)}; z_inf (R_ta0 1.10 Mpc, earliest) median {np.median(zi):.2f}, max {max(zi):.2f}; "
  f"(0.83 Mpc) median {np.median([v['z_inf']['MWonly'] for (f, n), v in ORB.items() if f == 'canonical' and v['src'] == 'PM']):.2f}")
R["orbits_summary"] = dict(n_pm=len(zi), zinf_LG_median=float(np.median(zi)), zinf_LG_max=float(max(zi)), k4_residual=k4res,
                           median_dgc_frac=mdgc)

# ================================================================== baseline (E3 reproduction)
P("\n[E3] baseline: clean primary data above the screened prediction (L* = 24 pc)")
BASE = {}; XS = {}
for foot in A0:
    a0 = A0[foot]; rows = sample(a0); X = build(rows); XS[foot] = X
    Bs = B_scr(X["Ms"], X["r12"], a0)
    X["Mscr"] = X["Ms"] / 2 * Bs; X["Bs"] = Bs
    d = np.log10(X["Md"] / X["Mscr"])
    m, s = boot_median(d)
    BASE[foot] = dict(N=len(rows), O=m, s=s)
    P(f"   {foot:9s} N = {len(rows)}  O_E3 = {m:+.3f} +- {s:.3f} dex")
ck("K1", BASE["canonical"]["N"] == 45 and BASE["alt"]["N"] == 46 and abs(BASE["canonical"]["O"] - 0.89) <= 0.03
   and abs(BASE["alt"]["O"] - 0.85) <= 0.03, f"N {BASE['canonical']['N']}/{BASE['alt']['N']} O {BASE['canonical']['O']:+.3f}/"
   f"{BASE['alt']['O']:+.3f}", "45/46 & +0.89/+0.85 +-0.03", "E3 reproduced from LVD")
X = XS["canonical"]; rel_b = []; rel_m = []
for i, r in enumerate(X["rows"]):
    e = E3CSV[("canonical", r["name"])]
    rel_b.append(abs(np.median(X["Bs"][i]) / float(e["B_scr_L24"]) - 1)); rel_m.append(abs(np.median(X["Md"][i]) / float(e["M_dyn"]) - 1))
k2m, k2x = float(np.median(rel_b + rel_m)), float(max(rel_b + rel_m))
_w = int(np.argmax(np.maximum(rel_b, rel_m))); P(f"   K2 worst system: {X['rows'][_w]['name']} (B_scr {rel_b[_w]:.3f}, M_dyn {rel_m[_w]:.3f})")
ck("K2", k2m <= 0.02 and k2x <= 0.10, f"median {k2m:.4f} max {k2x:.4f}", "<=0.02 & <=0.10 (A1)", "per-system B_scr, M_dyn vs E3 CSV")
lr = []
for i, r in enumerate(X["rows"]):
    e = E6CSV.get(("canonical", r["name"]))
    if e and fl(e["L_req_F1"]):
        Mreq = np.median(X["Md"][i] - X["Mscr"][i])
        Mb = 10 ** r["logms"] + (10 ** r["mhi"] if r["mhi"] else 0.0)
        lr.append(abs((Mreq / (SUP * Mb)) / float(e["L_req_F1"]) - 1))
k5 = float(np.median(lr))
ck("K5", k5 <= 0.01, f"median |L_req/E6 - 1| {k5:.4f} (N {len(lr)})", "<=0.01", "L_req vs E6")
R["baseline"] = BASE; R["K2"] = dict(median=k2m, max=k2x); R["K5"] = k5

# ================================================================== the rule
def Mcoll_of(cell, rows, X, foot):
    N = len(rows); Mb = np.empty((N, NMC)); ok = np.ones(N, bool)
    for i, r in enumerate(rows):
        Mb[i] = X["Ms"][i] + (10 ** r["mhi"] * X["fD"][i] ** 2 if r["mhi"] else 0.0)
    if cell == "FREE":
        M = Mb / FB
    elif cell in ("CHEM-cons", "CHEM-nom"):
        key = "Lmin_-0.5|W2" if cell == "CHEM-cons" else "Lmin_+0.1|W1"
        L = np.array([fl((E6CSV.get((foot, r["name"])) or {}).get(key)) or np.nan for r in rows])
        ok = np.isfinite(L); M = Mb * np.where(ok, L, 1.0)[:, None] / FB
    elif cell == "CENSUS":
        M = Mb / (FB * FRET_CENSUS)
    elif cell == "SHMR":
        M = shmr_halo(X["Ms"])                     # PAPER36's own route (Moster+13), extrapolated
    if MUT:
        M = M * 0.0
    return M, ok

def apply_rule(foot, rows, X, cell, prof, zc, rta="MWonly", zeta_force=None):
    a0 = A0[foot]
    Mc, ok = Mcoll_of(cell, rows, X, foot)
    Mcold = (1 - FB) * Mc
    r12pc = X["r12"] / PC; Repc = X["Re"] / PC
    rv = r_vir_pc(np.maximum(Mc, 1e-30), zc)
    Msb = X["Ms"]
    # host tidal strength at pericentre
    k = np.empty_like(Msb); zinf = np.empty(len(rows))
    for i, r in enumerate(rows):
        o = ORB[(foot, r["name"])]
        k[i] = tidal_k(MHOST[r["host"]], o["r_peri"] * KPC, a0) if o["src"] != "isolated" else 0.0
        zinf[i] = o["z_inf"][rta]
    def Mc_in(rpc):
        return Mcold * m_profile(prof, Mc, rpc, zc)
    def Msat(rpc):
        return Mb_plummer(Msb, Repc, rpc) + np.maximum(Mph(Msb, Repc * PC, rpc * PC, a0), Mc_in(rpc))
    rt = r_tidal_pc(Msat, k)
    rt_b = r_tidal_pc(lambda rpc: Mb_plummer(Msb, Repc, rpc) + Mph(Msb, Repc * PC, rpc * PC, a0), k)   # baryons + phantom only
    Mret_t = Mc_in(rt)
    fex = np.where(Mret_t > 0, np.maximum(0.0, 1.0 - Mph(Msb, Repc * PC, rt * PC, a0) / np.maximum(Mret_t, 1e-300)), 0.0)
    deb = fex * Mc_in(np.minimum(r12pc, rt))
    zeta = ((zc > zinf)[:, None] & (rt_b > r12pc)).astype(float)
    if zeta_force is not None:
        zeta = np.full_like(zeta, zeta_force)
    Mpred = np.where(zeta > 0, X["Mscr"] + deb, X["Ms"] / 2)
    return dict(Mpred=Mpred, ok=ok, zeta=zeta, rt=rt, rt_b=rt_b, fex=fex, deb=deb, rv=rv, zinf=zinf)

CELLS_NAT = [(c, p, z) for c in ("FREE", "CHEM-cons", "CHEM-nom") for p in ("TH", "B85") for z in ZC]
CELLS_EXT = [(c, p, z) for c in ("CENSUS", "SHMR") for p in ("TH", "B85", "NFW") for z in ZC] + \
            [(c, "NFW", z) for c in ("FREE", "CHEM-cons", "CHEM-nom") for z in ZC]
PRIMARY = [("CHEM-cons", "TH", 10.0), ("FREE", "TH", 10.0)]

# K3 limits
X = XS["canonical"]; rows = X["rows"]
r0 = apply_rule("canonical", rows, X, "FREE", "TH", 10.0)
Xz = dict(X);
saveM = Mcoll_of
def _zero(cell, rows_, X_, foot_):
    M, ok = saveM(cell, rows_, X_, foot_); return M * 0.0, ok
Mcoll_of = _zero
rz = apply_rule("canonical", rows, X, "FREE", "TH", 10.0, zeta_force=1.0)
Mcoll_of = saveM
rn = apply_rule("canonical", rows, X, "FREE", "TH", 10.0, zeta_force=0.0)
k3a = float(np.max(np.abs(rz["Mpred"] / X["Mscr"] - 1))); k3b = float(np.max(np.abs(rn["Mpred"] / (X["Ms"] / 2) - 1)))
ck("K3", k3a <= 1e-12 and k3b <= 1e-12, f"M_coll->0 vs screened {k3a:.1e}; zeta=0 vs Newton {k3b:.1e}", "<=1e-12", "rule limits")

P("\n[R] the rule: O = median log10(M_dyn / M_pred), clean primary data; per footing, never pooled")
RES = {}; PER = []
def run_cell(foot, cell, prof, zc, rta="MWonly"):
    X = XS[foot]; rows = X["rows"]
    rr = apply_rule(foot, rows, X, cell, prof, zc, rta)
    sel = rr["ok"]
    d = np.log10(X["Md"] / rr["Mpred"])[sel]
    dE3 = np.log10(X["Md"] / X["Mscr"])[sel]
    m, s = boot_median(d)
    mE, _ = boot_median(dE3)
    # overshoot: per-system P(M_pred > M_dyn) > 0.977
    over = np.mean(d < 0, axis=1) > 0.977
    ov_names = [rows[idx]["name"] for j, idx in enumerate(np.where(sel)[0]) if over[j]]
    n0 = int(np.sum(np.median(rr["zeta"], axis=1)[sel] < 0.5))
    out = dict(N=int(sel.sum()), O=m, s=s, O_E3_same=mE, reduction=mE - m, frac_closed=(mE - m) / mE if mE else None,
               n_zeta0=n0, n_overshoot_2sig=int(over.sum()), overshoot=ov_names,
               med_fex=float(np.median(rr["fex"][sel])), med_rt_pc=float(np.median(rr["rt"][sel])),
               med_rvir_pc=float(np.median(rr["rv"][sel])), med_debris=float(np.median(rr["deb"][sel])),
               med_need=float(np.median((X["Md"] - X["Mscr"])[sel])))
    return out, rr

for foot in A0:
    for cells, tag in ((CELLS_NAT, "native"), (CELLS_EXT, "external")):
        for (c, p, z) in cells:
            o, rr = run_cell(foot, c, p, z)
            RES[f"{foot}|{c}|{p}|z{z:g}"] = dict(o, cls=tag)
            P(f"   {foot:9s} {tag:8s} {c:9s} {p:3s} z_c {z:4.0f}: N {o['N']:2d}  O = {o['O']:+.3f} +- {o['s']:.3f}  "
              f"(E3 same set {o['O_E3_same']:+.3f}; closed {100 * (o['frac_closed'] or 0):5.1f}%)  zeta0 {o['n_zeta0']}  "
              f"overshoot>2sig {o['n_overshoot_2sig']:2d}  med r_vir {o['med_rvir_pc']:7.1f} pc  r_t {o['med_rt_pc']:8.1f} pc  "
              f"f_ex {o['med_fex']:.2f}  debris {o['med_debris']:.2e} vs need {o['med_need']:.2e}")
            if (c, p, z) in PRIMARY:
                X = XS[foot]
                for i, r in enumerate(X["rows"]):
                    if not rr["ok"][i]:
                        continue
                    PER.append(dict(footing=foot, cell=f"{c}|{p}|z{z:g}", name=r["name"], host=r["host"], logMstar=r["logms"],
                                    r12_pc=float(np.median(X["r12"][i] / PC)), M_dyn=float(np.median(X["Md"][i])),
                                    M_scr=float(np.median(X["Mscr"][i])), M_pred=float(np.median(rr["Mpred"][i])),
                                    debris_r12=float(np.median(rr["deb"][i])), r_vir_pc=float(np.median(rr["rv"][i])),
                                    r_t_pc=float(np.median(rr["rt"][i])), r_t_baryon_pc=float(np.median(rr["rt_b"][i])),
                                    f_ex=float(np.median(rr["fex"][i])), zeta=float(np.median(rr["zeta"][i])),
                                    z_inf=float(rr["zinf"][i]), orbit=ORB[(foot, r["name"])]["src"],
                                    r_peri_kpc=ORB[(foot, r["name"])]["r_peri"], r_apo_kpc=ORB[(foot, r["name"])]["r_apo"],
                                    logO=float(np.median(np.log10(X["Md"][i] / rr["Mpred"][i])))))
# infall bracket sensitivity (primary cells, R_ta0 = 1.10 Mpc)
for foot in A0:
    for (c, p, z) in PRIMARY:
        o, _ = run_cell(foot, c, p, z, rta="LG")
        RES[f"{foot}|{c}|{p}|z{z:g}|RtaLG"] = dict(o, cls="native-infall-bracket")
        P(f"   {foot:9s} infall R_ta0 1.10 Mpc: {c} {p} z{z:g}: O = {o['O']:+.3f} +- {o['s']:.3f}, zeta0 {o['n_zeta0']}")

k6 = max(abs(RES[f"{f}|{c}|{p}|z{z:g}"]["O"] - RES[f"{f}|{c}|{p}|z{z:g}"]["O_E3_same"]) for f in A0 for (c, p, z) in CELLS_NAT)
ck("K6", k6 > 0.01, f"max |O_rule - O_E3| over native cells {k6:.3f}", ">0.01", "the rule moves the offset")

# ================================================================== breakage
P("\n[B] breakage")
BR = {}
# B1 TDGs: Lelli+15 -- zeta = 0 by the rule's own criterion (formed from tidal debris after the interaction)
T = list(csv.DictReader(open(os.path.join(DATA, "tidal_dwarfs", "lelli2015_tdg.csv"))))
lr_ = np.array([math.log10(float(t["Mdyn_over_Mbar"])) for t in T])
e_ = np.array([float(t["e_Mdyn_over_Mbar"]) / float(t["Mdyn_over_Mbar"]) / math.log(10) for t in T])
w = 1 / e_ ** 2; mT = float(np.sum(w * lr_) / np.sum(w)); sT = float(1 / math.sqrt(np.sum(w)))
c936 = json.load(open(os.path.join(CFG, "CFG936_below_law_systems", "cfg936_results.json")))
BR["B1"] = dict(N=len(T), zeta=0, mean_log_Mdyn_over_Mbar=mT, se=sT, z=mT / sT, cfg936_K1_means=c936["K1"]["means"])
b1 = abs(mT / sT) <= 2
P(f"   B1 TDGs (6): zeta = 0 -> Newton; data log Mdyn/Mbar = {mT:+.3f} +- {sT:.3f} ({mT / sT:+.2f} sigma) -> "
  f"{'NO BREAKAGE' if b1 else 'BROKEN'} (label from formation history; CFG936 route (i))")
# B2 DF2 / DF4 (CFG657 table; NGC 1052 host baryons 1e11 external; D 20 Mpc)
DFS = {"DF2": dict(Ms=2.0e8, Re=2.0, sig=(8.5, 2.3, 3.1), pos=(40.4451, -8.4028), age=8.28),
       "DF4": dict(Ms=1.5e8, Re=1.6, sig=(6.3, 2.5, 1.6), pos=(39.8128, -8.1160), age=10.68)}
HOST = (40.2700, -8.2558); DMPC = 20.0
B2 = {}
for nm, dd in DFS.items():
    dra = (dd["pos"][0] - HOST[0]) * math.cos(math.radians(HOST[1])); ddec = dd["pos"][1] - HOST[1]
    Dp = math.radians(math.hypot(dra, ddec)) * DMPC * 1e3         # kpc
    zform = float(z_of_t(T0 - dd["age"] * GYR))
    r12 = 4 / 3 * dd["Re"] * 1e3                                   # pc
    for foot, a0 in A0.items():
        out = {}
        for fM, lab in ((0.5, "host x0.5"), (1.0, "host 1e11"), (3.0, "host x3")):
            Mh = 1e11 * fM
            k = np.array([tidal_k(Mh, Dp * KPC, a0)])
            Ms = np.array([dd["Ms"]]); Re = np.array([dd["Re"] * 1e3])
            rtb = float(r_tidal_pc(lambda rpc: Mb_plummer(Ms, Re, rpc) + Mph(Ms, Re * PC, rpc * PC, a0, None), k)[0])
            # pericentre needed for r_t = r12 (baryons + unscreened phantom)
            Msat12 = float(Mb_plummer(Ms, Re, r12)[0] + Mph(Ms, Re * PC, r12 * PC, a0, None)[0])
            fpk = lambda Dk: tidal_k(Mh, Dk * KPC, a0) * (r12 * PC) ** 3 / G / MSUN - Msat12
            Dneed = brentq(fpk, 0.01, 1e4)
            # zeta = 1 predictions (FREE TH z 10; CENSUS TH z 10): sigma at r12
            res = {}
            for cell, Mcoll in (("FREE", dd["Ms"] / FB), ("CENSUS", dd["Ms"] / (FB * FRET_CENSUS))):
                if MUT:
                    Mcoll = 0.0
                Mc = (1 - FB) * Mcoll
                zc = max(zform, 1.0)
                mcin = lambda rpc: Mc * m_profile("TH", np.array([max(Mcoll, 1e-30)]), rpc, zc)
                Msat = lambda rpc: Mb_plummer(Ms, Re, rpc) + np.maximum(Mph(Ms, Re * PC, rpc * PC, a0, None), mcin(rpc))
                rt = float(r_tidal_pc(Msat, k)[0])
                fex = max(0.0, 1 - float(Mph(Ms, Re * PC, rt * PC, a0, None)[0]) / max(float(mcin(np.array([rt]))[0]), 1e-300))
                Mlaw = float(Mb_plummer(Ms, Re, r12)[0] + Mph(Ms, Re * PC, r12 * PC, a0, None)[0])
                Mp = Mlaw + fex * float(mcin(np.array([min(r12, rt)]))[0])
                sp = math.sqrt(G * Mp * MSUN / (3 * r12 * PC)) / 1e3
                res[cell] = dict(sigma_pred=sp, r_t_pc=rt, f_ex=fex, z_obs=(sp - dd["sig"][0]) / dd["sig"][1])
            sN = math.sqrt(G * dd["Ms"] / 2 * MSUN / (3 * r12 * PC)) / 1e3
            out[lab] = dict(D_proj_kpc=Dp, r_t_baryon_law_pc=rtb, r12_pc=r12, stripped_at_Dproj=rtb <= r12, D_peri_needed_kpc=Dneed,
                            zeta1=res, sigma_newton=sN)
        B2[f"{nm}|{foot}"] = dict(z_form_from_age=zform, **out)
        o = out["host 1e11"]
        P(f"   B2 {nm} {foot:9s}: D_proj {o['D_proj_kpc']:.0f} kpc, r_t(baryons+law) {o['r_t_baryon_law_pc']:.0f} pc vs r12 "
          f"{o['r12_pc']:.0f} pc -> stripped at D_proj: {o['stripped_at_Dproj']}; pericentre needed {o['D_peri_needed_kpc']:.1f} kpc "
          f"(x0.5/x3 host: {out['host x0.5']['D_peri_needed_kpc']:.1f}/{out['host x3']['D_peri_needed_kpc']:.1f}); age {dd['age']} Gyr "
          f"-> z_form {zform:.2f}; zeta=1 sigma_pred FREE {o['zeta1']['FREE']['sigma_pred']:.1f} / CENSUS "
          f"{o['zeta1']['CENSUS']['sigma_pred']:.1f} vs obs {dd['sig'][0]} +{dd['sig'][1]} (z {o['zeta1']['FREE']['z_obs']:+.1f} / "
          f"{o['zeta1']['CENSUS']['z_obs']:+.1f}); Newton {o['sigma_newton']:.1f}")
BR["B2"] = B2
b2_native_zeta0 = all(B2[f"{n}|{f}"]["host 1e11"]["stripped_at_Dproj"] for n in DFS for f in A0)
b2_zeta1_broken = all(B2[f"{n}|{f}"]["host 1e11"]["zeta1"]["FREE"]["z_obs"] > 2 for n in DFS for f in A0)
P(f"   B2 reading: criterion gives zeta = 0 natively (stripped at D_proj): {b2_native_zeta0}; zeta = 1 prediction broken (>2 sigma): "
  f"{b2_zeta1_broken}")
# B3 UFD overshoot (primary native cells)
for foot in A0:
    for (c, p, z) in PRIMARY:
        o = RES[f"{foot}|{c}|{p}|z{z:g}"]
        P(f"   B3 {foot:9s} {c} {p} z{z:g}: overshoot > 2 sigma in {o['n_overshoot_2sig']} systems {o['overshoot']}")
cmp_names = ("Segue 1", "Willman 1", "Carina III")
for e in PER:
    if e["name"] in cmp_names and e["cell"] == "FREE|TH|z10":
        P(f"      compact {e['footing']:9s} {e['name']:11s}: logO screened {math.log10(e['M_dyn'] / e['M_scr']):+.2f} -> rule {e['logO']:+.2f}")
b3 = all(RES[f"{f}|{c}|{p}|z{z:g}"]["n_overshoot_2sig"] < 5 for f in A0 for (c, p, z) in PRIMARY)
BR["B3"] = dict(ok=b3)
# B4 isolated LVD field dwarfs (zeta = 1, no host truncation: r_t = r_vir)
B4 = {}
for foot, a0 in A0.items():
    rows = [r for r in ALL if r["host"] == "field" and r["logms"] < math.log10(a0 * (LSTAR_PC * PC) ** 2 / G / MSUN * 100)]
    Xf = build(rows); Xf["Mscr"] = Xf["Ms"] / 2 * B_scr(Xf["Ms"], Xf["r12"], a0)
    for (c, p, z) in (("FREE", "TH", 10.0), ("CENSUS", "TH", 10.0)):
        Mc, _ = Mcoll_of(c, rows, Xf, foot)
        deb = (1 - FB) * Mc * m_profile(p, Mc, Xf["r12"] / PC, z)
        ph = Mph(Xf["Ms"], Xf["Re"], r_vir_pc(np.maximum(Mc, 1e-30), z) * PC, a0)
        fex = np.maximum(0.0, 1 - ph / np.maximum((1 - FB) * Mc, 1e-300))
        d = np.log10(Xf["Md"] / (Xf["Mscr"] + fex * deb)); m, s = boot_median(d)
        dE, _ = boot_median(np.log10(Xf["Md"] / Xf["Mscr"]))
        B4[f"{foot}|{c}|{p}|z{z:g}"] = dict(N=len(rows), O=m, s=s, O_screened=dE)
        P(f"   B4 {foot:9s} isolated field dwarfs (stars only in g_bar) N {len(rows)} {c} {p} z{z:g}: O = {m:+.3f} +- {s:.3f} "
          f"(screened alone {dE:+.3f})")
BR["B4"] = B4
R["breakage"] = BR

# ================================================================== verdict
P("\n[V] verdict (native set decides; external cells reported separately)")
VER = {}
for foot in A0:
    pc = RES[f"{foot}|CHEM-cons|TH|z10"]; pf = RES[f"{foot}|FREE|TH|z10"]
    nat = [RES[f"{foot}|{c}|{p}|z{z:g}"] for (c, p, z) in CELLS_NAT]
    closes_all = all(abs(o["O"]) <= 2 * o["s"] for o in nat)
    prim_close = abs(pc["O"]) <= 2 * pc["s"]
    over = any(o["O"] < -2 * o["s"] for o in nat)
    nat_close_any = [k for k in RES if k.startswith(foot + "|") and RES[k]["cls"] == "native" and abs(RES[k]["O"]) <= 2 * RES[k]["s"]]
    ext_close = [k for k in RES if k.startswith(foot + "|") and RES[k]["cls"] == "external" and abs(RES[k]["O"]) <= 2 * RES[k]["s"]]
    nobreak = b1 and b3 and (b2_native_zeta0 or not b2_zeta1_broken)
    if prim_close and closes_all and nobreak:
        v = "CLOSES THE GAP"
    elif pc["reduction"] >= 0.2 and not over:
        v = "PARTIAL"
    elif pc["reduction"] >= 0.2 and over:
        v = "PARTIAL (native set straddles: some cells overshoot)"
    else:
        v = "FAILS"
    ext_detail = {k.split("|", 1)[1]: RES[k]["n_overshoot_2sig"] for k in ext_close}
    if ext_close and not prim_close:
        v += " + RESTS ON A NON-NATIVE INPUT where it closes (median only; B3 overshoot counts " + \
             ", ".join(f"{k} {n}" for k, n in ext_detail.items()) + ")"
    rng = (min(o["O"] for o in nat), max(o["O"] for o in nat))
    VER[foot] = dict(verdict=v, primary_CHEMcons=dict(O=pc["O"], s=pc["s"], frac_closed=pc["frac_closed"]),
                     primary_FREE=dict(O=pf["O"], s=pf["s"], frac_closed=pf["frac_closed"]), native_range=rng,
                     native_cells_closing=nat_close_any, external_cells_closing=ext_close, overshoot_any_native=over,
                     no_breakage=nobreak, external_overshoot=ext_detail,
                     native_closing_overshoot={k.split("|", 1)[1]: RES[k]["n_overshoot_2sig"] for k in nat_close_any}, B2_native_zeta0=b2_native_zeta0, B2_zeta1_broken=b2_zeta1_broken)
    P(f"   {foot:9s}: {v}")
    P(f"      primary CHEM-cons TH z10: O {pc['O']:+.3f} +- {pc['s']:.3f} (closed {100 * pc['frac_closed']:.0f}%); FREE TH z10: "
      f"O {pf['O']:+.3f} +- {pf['s']:.3f} (closed {100 * pf['frac_closed']:.0f}%); native range {rng[0]:+.2f}..{rng[1]:+.2f}")
    P(f"      native cells within 2s: {[k.split('|', 1)[1] for k in nat_close_any]}")
    P(f"      external (LCDM-processed) cells within 2s: {[k.split('|', 1)[1] for k in ext_close]}")
R["verdict"] = VER; R["cells"] = RES
R["checks"] = {k: v for k, v in CHK}
npass = sum(v for _, v in CHK)
P(f"\nG2_PREINFALL_RETENTION COMPLETE: {npass}/{len(CHK)} checks PASS.")
open(os.path.join(HERE, f"g2_preinfall_retention{SFX}.out"), "w").write("\n".join(OUT) + "\n")
json.dump(R, open(os.path.join(HERE, f"g2_preinfall_retention_results{SFX}.json"), "w"), indent=1, default=float)
if PER:
    with open(os.path.join(HERE, f"g2_per_system{SFX}.csv"), "w", newline="") as fh:
        wr = csv.DictWriter(fh, fieldnames=list(PER[0].keys())); wr.writeheader(); wr.writerows(PER)
sys.exit(0 if npass == len(CHK) else 1)
