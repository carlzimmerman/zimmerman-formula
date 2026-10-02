#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
CFG286 -- DERIVED TIDAL STRIPPING OF THE SATELLITES' COLLAPSE-COLD CORES AT THEIR MEASURED PERICENTRES.

The derived cold-mass rule (PAPER36; CFG35-CFG45 reading S) closes the Milky Way ultra-faint offset but over-predicts the classical
satellites (M31 LVD -2.67 sigma).  Hypothesis (owner-directed): each satellite keeps its collapse-cold mass only inside its tidal radius
at its measured pericentre, the tidal radius from the host's field under the programme's own law.  Zero new constants.

Everything is frozen in FROZEN_CRITERIA.md (written before this script; its sha256 is printed below).  In one line each:
  HOST     spherical, static: g_h(r) = nu_mono(y) G M_host / r^2, M_host = 6.0e10 (MW) / 1.2e11 (M31) Msun (the record's), both footings.
  ORBITS   54 MW systems, 1000 Monte Carlo draws of (distance, pmra, pmdec, vlos) from the LVD's two-piece errors (seed 286), astropy
           Galactocentric 'v4.0'; kick-drift-kick leapfrog backward (dt = 0.5 Myr) up to t_H = 13.80 Gyr; pericentre = the most recent
           local minimum of r(t), parabola-refined; no pericentre within t_H -> no tide.
  JACOBI   r_t^3 = G m(<r_t) / D_t,  D_t = (v_p / r_p)^2 - dg_h/dr |_{r_p}  (King 1962), m(<r) = the satellite's own law mass of its
           (Plummer) baryons + f_ex (1 - f_b) M_NFW(<r; M_c); median D_t over the draws.
  STRIP    g(r_ev) = a_int(g_N) + f_ex (1 - f_b) G M_NFW(< min(r_ev, r_t)) / r_ev^2, r_ev = (4/3) r_half; f_ex as committed;
           r_t = inf is reading S, r_t = 0 is reading L (= CFG244's (a1) "own nothing").
  STAT     CFG45's own P1 / P2 statistics and error recipe, exec'd read-only (KM median + bootstrap(1000, seed 42) + Upsilon floor +
           collapse-mass floor for the ultra-faints; 1.2533 std / sqrt(n) + floors for the classicals); r_t re-solved in every variant.
  M31      no M31-centric velocities on disk: primary route = projected radius x the MW pool's q' = r_p / R_proj (isotropic view) with
           eta = v_p / v_c(r_p); alternate route = the record's 3D distance x the MW pool's q = r_p / r_now.
  VERDICT  H1: |z_UFD| < 2 both footings.  H2: |z| < 2 for MW classical, M31 LVD, M31 Collins+13 both footings.  JOINT PASS / PARTIAL /
           FAIL as frozen (section 9), the binding population named.
MODES: MUTATE=0 main; MUTATE=1 every pericentre x2 at fixed pericentre speed (its UNCHANGED check must FAIL, rc 1, for the stripping to
bite); MUTATE=2 r_t = inf throughout; MUTATE=3 r_t = 0 throughout (their load-bearing checks are the CFG45 reproductions).
kappa = 1/2 FITTED.  No dark-matter particle: the cold fluid's MASS is still required (a declared SHMR supplies it).  Nothing here says
the theory is closed or that the data favour the framework.
Run: python3 campaign_fresh_gravity/CFG286_satellite_tidal_stripping/cfg286_tidal_stripping.py   (MUTATE=1/2/3 for the controls)
"""
import sys
sys.dont_write_bytecode = True
import os, io, math, csv, json, time, hashlib, contextlib
import numpy as np
from scipy.optimize import brentq

HERE = os.path.dirname(os.path.abspath(__file__))
LANES = os.path.dirname(HERE)
sys.path.insert(0, LANES)
import CFG7_common as C

MODE = int(os.environ.get("MUTATE", "0"))
SLUG = "cfg286_tidal_stripping" + (f"_MUTATE{MODE}" if MODE else "")
R = C.Report(SLUG, False)
P, check = R.P, R.check
T0 = time.time()
P(__doc__.split("Run: python3")[0].strip())
FROZEN = os.path.join(HERE, "FROZEN_CRITERIA.md")
P(f"\n  FROZEN_CRITERIA.md sha256 {hashlib.sha256(open(FROZEN, 'rb').read()).hexdigest()}")
if MODE:
    P(f"\n  *** MUTATE={MODE}: " + {1: "every pericentre x2 at fixed pericentre speed -- the UNCHANGED check must FAIL for the stripping to bite",
                                 2: "no stripping (r_t = infinity) throughout -- must reproduce CFG45's reading S",
                                 3: "full stripping (r_t = 0) throughout -- must reproduce CFG45's reading L / CFG244 (a1)"}[MODE] + " ***")
FOOTS = ("canonical", "alt")
POPS = ("ufd", "cls", "m31", "col")
# load-bearing scope (frozen section 10): in MUTATE runs only the mode's own check is load-bearing; everything else is reported there.
LB0 = MODE == 0
PLAB = {"ufd": "P1 MW ultra-faints (31 + 9 limits)", "cls": "P2 MW classical (14)", "m31": "P3 M31 LVD (34)", "col": "P4 M31 Collins+13 (14)"}

# ================================================================================================ the record's machinery (read-only)
_e = os.environ.get("MUTATE"); os.environ["MUTATE"] = "0"
_src = open(os.path.join(LANES, "CFG45_rule_readings.py")).read()
g45 = {"__file__": os.path.join(LANES, "CFG45_rule_readings.py"), "__name__": "cfg45_prefix"}
with contextlib.redirect_stdout(io.StringIO()):
    exec(compile(_src[:_src.index("FLOORS = (1e8, 3e8, 1e9, 3e9, 1e10)")], "CFG45_rule_readings.py", "exec"), g45)
os.environ.pop("MUTATE") if _e is None else os.environ.__setitem__("MUTATE", _e)
SAMPLES, UL, A0H, UPS_V = g45["SAMPLES"], g45["UL"], g45["A0H"], g45["UPS_V"]
a_int, infall_gas, halo_mass, nfw_enclosed, FB = g45["a_int"], g45["infall_gas"], g45["halo_mass"], g45["nfw_enclosed"], g45["FB"]
edge_info, km_median, boot, collapse = g45["edge_info"], g45["km_median"], g45["boot"], g45["collapse"]
G_SAT, MSUN_SAT, SI_SAT = g45["G_SAT"], g45["MSUN_SAT"], g45["SI_SAT"]
assert g45["MCF"] == 1.0
FLOORS = (1e8, 3e8, 1e9, 3e9, 1e10)
C45 = json.load(open(os.path.join(LANES, "CFG45_rule_readings_results.json")))["numbers"]
C28 = json.load(open(os.path.join(LANES, "CFG28_ufd_referee_results.json")))["numbers"]
DSPH = os.path.join(C.REPO, "real_research", "data", "dsph")

KPC_M = 3.0857e19                      # FG001's kpc in m (SI_SAT[2])
MYR_S = 3.15576e13
KMS = 1e3 * MYR_S / KPC_M              # km/s -> kpc/Myr
ACC = MYR_S ** 2 / KPC_M               # m/s^2 -> kpc/Myr^2
T_H_MYR = float(C.LCDM.t(1.0)) * C.UNIT_GYR * 1e3
MW_MB, M31_MB = 6.0e10, 1.2e11
MW_MB_CENSUS_HI = 7.3e10
M31_RA, M31_DEC, M31_D = 10.684583333, 41.269166667, 785.0     # FG001's "00 42 44.3", "+41 16 09", 785 kpc
NDRAW, DT = 1000, 0.5
P(f"\n  t_H = {T_H_MYR / 1e3:.3f} Gyr (CFG7_common.LCDM);  MW / M31 baryons {MW_MB:.1e} / {M31_MB:.1e} Msun;  a0 (estimator) {A0H}")


def fnum(v):
    try:
        x = float(v); return x if math.isfinite(x) else None
    except (TypeError, ValueError):
        return None


# ================================================================================================ the host field
class Host:
    """spherical static host: g(r) = nu(y) G M / r^2 [+ optional debris], tabulated in ln r; units kpc, Myr."""

    def __init__(self, M, a0, nu=None, debris=None, label=""):
        self.M, self.a0, self.label = M, a0, label
        nu = C.nu_mono if nu is None else nu
        self.lnr = np.linspace(math.log(0.01), math.log(1e5), 20001)
        r = np.exp(self.lnr)
        self.g_si = self.g_direct_si(r, nu, debris)
        self.lng = np.log(self.g_si * ACC)
        self.dlng = np.gradient(self.lng, self.lnr)
        # potential: Phi(r) = int g dr = int g r dln r (zero at the inner grid edge; only differences matter)
        gr = self.g_si * ACC * r
        self.phi = np.concatenate([[0.0], np.cumsum(0.5 * (gr[1:] + gr[:-1]) * np.diff(self.lnr))])
        self.nu, self.debris = nu, debris

    def g_direct_si(self, r_kpc, nu=None, debris=None):
        nu = self.nu if nu is None else nu
        debris = getattr(self, "debris", None) if debris is None else debris
        r = np.asarray(r_kpc, float) * KPC_M
        gN = G_SAT * self.M * MSUN_SAT / r ** 2
        g = np.asarray(nu(gN / self.a0), float) * gN
        if debris is not None:
            fex, Mc = debris
            g = g + fex * (1 - FB) * G_SAT * np.asarray(nfw_enclosed(Mc, np.asarray(r_kpc, float)), float) * MSUN_SAT / r ** 2
        return g

    def g(self, r):                       # kpc/Myr^2
        return np.exp(np.interp(np.log(r), self.lnr, self.lng))

    def dgdr(self, r):                    # Myr^-2
        return self.g(r) / r * np.interp(np.log(r), self.lnr, self.dlng)

    def vc(self, r):                      # kpc/Myr
        return np.sqrt(self.g(r) * r)

    def phi_at(self, r):
        return np.interp(np.log(r), self.lnr, self.phi)

    def acc(self, x):
        r = np.sqrt(x[:, 0] ** 2 + x[:, 1] ** 2 + x[:, 2] ** 2)
        return -(self.g(r) / r)[:, None] * x


def Dt_of(host, rp, vp, peri_factor=1.0):
    """King's tidal denominator at pericentre, Myr^-2; rp in kpc, vp in kpc/Myr (pericentre x factor at fixed speed for MUTATE=1)."""
    rp = np.minimum(np.asarray(rp, float) * peri_factor, 9.9e4)
    return (np.asarray(vp, float) / rp) ** 2 - host.dgdr(rp)


def peri_analytic(host, X, V):
    """exact pericentre in a static spherical potential: the root of 2 (E - Phi) r^2 - L^2 below r_now (vectorised bisection in ln r)."""
    r0 = np.linalg.norm(X, axis=1); L = np.linalg.norm(np.cross(X, V), axis=1)
    E = 0.5 * np.sum(V ** 2, axis=1) + host.phi_at(r0)
    f = lambda r: 2 * (E - host.phi_at(r)) * r ** 2 - L ** 2
    lo = np.full(len(r0), math.log(0.0101)); hi = np.log(r0)
    for _ in range(80):
        mid = 0.5 * (lo + hi); fm = f(np.exp(mid))
        neg = fm < 0
        lo = np.where(neg, mid, lo); hi = np.where(neg, hi, mid)
    rp = np.exp(0.5 * (lo + hi))
    return rp, L / rp


def integrate_backward(host, X, V, dt=DT, tmax=T_H_MYR):
    """kick-drift-kick leapfrog, backward in time; the most recent pericentre (local minimum of r), parabola-refined.  Returns r_p, v_p,
    t_since (Myr); NaN where no pericentre is found within tmax.  L = |x x v| is conserved exactly by KDK for a central force."""
    N = len(X)
    L = np.linalg.norm(np.cross(X, V), axis=1)
    rp = np.full(N, np.nan); tp = np.full(N, np.nan)
    act = np.arange(N); x = X.copy(); v = -V.copy()
    a = host.acc(x)
    r_prev2 = None; r_prev = np.linalg.norm(x, axis=1)
    nsteps = int(round(tmax / dt))
    for n in range(1, nsteps + 1):
        v += 0.5 * dt * a; x += dt * v; a = host.acc(x); v += 0.5 * dt * a
        r_c = np.sqrt(x[:, 0] ** 2 + x[:, 1] ** 2 + x[:, 2] ** 2)
        if r_prev2 is not None:
            hit = (r_prev < r_prev2) & (r_prev <= r_c)
            if hit.any():
                den = r_prev2[hit] - 2 * r_prev[hit] + r_c[hit]
                den = np.where(den > 0, den, np.inf)
                rp[act[hit]] = r_prev[hit] - 0.125 * (r_c[hit] - r_prev2[hit]) ** 2 / den
                tp[act[hit]] = (n - 1 + 0.5 * (r_prev2[hit] - r_c[hit]) / den) * dt
                k = ~hit
                act, x, v, a, r_c, r_prev = act[k], x[k], v[k], a[k], r_c[k], r_prev[k]
        r_prev2, r_prev = r_prev, r_c
        if len(act) == 0:
            break
    return rp, L / rp, tp


# ================================================================================================ the MW phase-space draws
MWROWS = {r["name"]: r for r in csv.DictReader(open(os.path.join(DSPH, "lvd_dwarf_mw.csv")))}
M31ROWS = {r["name"]: r for r in csv.DictReader(open(os.path.join(DSPH, "lvd_dwarf_m31.csv")))}
MWSYS = [d["name"] for d in SAMPLES["ufd"]] + [d["name"] for d in UL] + [d["name"] for d in SAMPLES["cls"]]
assert len(MWSYS) == len(set(MWSYS)) == 54


def two_piece(rng, c, em, ep, n):
    em = em if em is not None else ep; ep = ep if ep is not None else em
    if em is None:
        return np.full(n, c), "no error"
    z = rng.standard_normal(n)
    return c + np.where(z > 0, z * ep, z * em), ""


rng = np.random.default_rng(286)
DRAW = {}
missing = []
for nm in MWSYS:
    r = MWROWS[nm]
    cols = {}
    for k in ("distance", "pmra", "pmdec", "vlos_systemic"):
        c, em, ep = fnum(r[k]), fnum(r[k + "_em"]), fnum(r[k + "_ep"])
        assert c is not None, (nm, k)
        vals, note = two_piece(rng, c, em, ep, NDRAW)
        if note:
            missing.append(f"{nm}:{k}")
        cols[k] = np.concatenate([[c], vals])                  # index 0 = the table (central) values
    cols["distance"] = np.maximum(cols["distance"], 0.1 * cols["distance"][0])
    DRAW[nm] = dict(ra=fnum(r["ra"]), dec=fnum(r["dec"]), host=r["host"], dgc=fnum(r["distance_gc"]), vgsr=fnum(r["velocity_gsr"]), **cols)

from astropy import units as u
from astropy.coordinates import SkyCoord, Galactocentric, galactocentric_frame_defaults
with galactocentric_frame_defaults.set("v4.0"):
    GC = Galactocentric()
    names = MWSYS
    ra = np.concatenate([np.full(NDRAW + 1, DRAW[n]["ra"]) for n in names])
    dec = np.concatenate([np.full(NDRAW + 1, DRAW[n]["dec"]) for n in names])
    sc = SkyCoord(ra=ra * u.deg, dec=dec * u.deg, distance=np.concatenate([DRAW[n]["distance"] for n in names]) * u.kpc,
                  pm_ra_cosdec=np.concatenate([DRAW[n]["pmra"] for n in names]) * u.mas / u.yr,
                  pm_dec=np.concatenate([DRAW[n]["pmdec"] for n in names]) * u.mas / u.yr,
                  radial_velocity=np.concatenate([DRAW[n]["vlos_systemic"] for n in names]) * u.km / u.s, frame="icrs")
    g = sc.transform_to(GC)
    XALL = np.stack([g.x.to_value(u.kpc), g.y.to_value(u.kpc), g.z.to_value(u.kpc)], axis=1)
    VALL = np.stack([g.v_x.to_value(u.km / u.s), g.v_y.to_value(u.km / u.s), g.v_z.to_value(u.km / u.s)], axis=1) * KMS
    P(f"  Galactocentric frame ('v4.0'): R0 = {GC.galcen_distance}, z_sun = {GC.z_sun}, v_sun = {GC.galcen_v_sun}")
SL = {n: slice(i * (NDRAW + 1), (i + 1) * (NDRAW + 1)) for i, n in enumerate(names)}
if missing:
    P("  draws with no error column (table value used): " + ", ".join(missing))

# ================================================================================================ C-HOST
HOSTS = {(h, f): Host(M, A0H[f], label=f"{h}|{f}") for h, M in (("MW", MW_MB), ("M31", M31_MB)) for f in FOOTS}
R.banner("C-HOST / C-COORD  CONTROLS")
rr = np.exp(np.random.default_rng(1).uniform(math.log(0.5), math.log(3000.0), 1000))
dev = max(float(np.max(np.abs(H.g(rr) / (H.g_direct_si(rr) * ACC) - 1))) for H in HOSTS.values())
H = HOSTS[("MW", "canonical")]
rdeep = math.sqrt(G_SAT * MW_MB * MSUN_SAT / (1e-4 * H.a0)) / KPC_M
deep = float(H.g(np.array([rdeep]))[0] / (math.sqrt(G_SAT * MW_MB * MSUN_SAT * H.a0) / (rdeep * KPC_M) * ACC) - 1)
check("C-HOST: the tabulated host field equals the direct formula on 1000 radii in [0.5, 3000] kpc; deep limit at y = 1e-4",
      f"max |rel dev| {dev:.1e} (<= 1e-6); deep-limit deviation {deep:+.1e} (|.| <= 1e-3; nu_mono's next-order term)", dev <= 1e-6 and abs(deep) <= 1e-3, load_bearing=LB0)
# ADDED BEFORE THE FIRST RUN, DISCLOSED: the frozen 1e-3 tolerance above ignores the kernel's known next-order term (nu ~ 1/sqrt(y) + 1/2), which is
# 5e-3 at y = 1e-4, so that control is expected to fail as frozen; it is kept unchanged.  This reported diagnostic checks the expansion instead.
_y = 1e-4
_nx = float(C.nu_mono(np.array([_y]))[0]) * math.sqrt(_y) - (1 + 0.5 * math.sqrt(_y))
check("C-HOST diagnostic (reported; added before the first run): nu_mono(y) sqrt(y) equals 1 + sqrt(y)/2 at y = 1e-4 (the deep limit with its "
      "next-order term)", f"difference {_nx:+.1e} (expected O(y/12) ~ 1e-5)", abs(_nx) <= 3e-5, load_bearing=False)
for f in FOOTS:
    Hm = HOSTS[("MW", f)]
    P(f"    MW host ({f}): v_c = " + ", ".join(f"{float(Hm.vc(np.array([r_]))[0]) / KMS:.1f}" for r_ in (8.122, 20, 50, 100, 200, 400))
      + " km/s at 8.1 / 20 / 50 / 100 / 200 / 400 kpc")
rnow_c = {n: float(np.linalg.norm(XALL[SL[n]][0])) for n in names}
cc = [(n, rnow_c[n], DRAW[n]["dgc"]) for n in names]
bad = [(n, a, b) for n, a, b in cc if b is None or abs(a - b) > max(1.5, 0.02 * b)]
check("C-COORD: the central Galactocentric distances equal the LVD's distance_gc within max(1.5 kpc, 2%) for all 54 MW systems",
      f"max |d| {max(abs(a - b) for n, a, b in cc if b is not None):.2f} kpc; failures: {bad}", not bad, load_bearing=LB0)
vr_c = {n: float(np.dot(XALL[SL[n]][0], VALL[SL[n]][0]) / rnow_c[n] / KMS) for n in names}
dv = [abs(vr_c[n] - DRAW[n]["vgsr"]) for n in names if DRAW[n]["vgsr"] is not None]
check("C-COORD (reported): central Galactocentric radial velocities against the LVD's velocity_gsr (its own solar motion; line-of-sight GSR "
      "is not v_r, so a sanity check only)", f"median |d| {np.median(dv):.1f} km/s, max {max(dv):.1f} km/s over {len(dv)}", True, load_bearing=False)

# ================================================================================================ ORBITS
R.banner("ORBITS  backward leapfrog in the static law host (both footings), 54 systems x (1 central + 1000 draws)")
ORB = {}
for f in FOOTS:
    t = time.time()
    rp, vp, tp = integrate_backward(HOSTS[("MW", f)], XALL, VALL)
    ORB[f] = dict(rp=rp, vp=vp, tp=tp)
    P(f"    {f}: {len(rp)} orbits in {time.time() - t:.0f} s; draws with no pericentre within t_H: {int(np.isnan(rp).sum())}")
# C-ORB
worst = {}
for f in FOOTS:
    idx0 = np.array([SL[n].start for n in names])
    rpa, _ = peri_analytic(HOSTS[("MW", f)], XALL[idx0], VALL[idx0])
    rl = ORB[f]["rp"][idx0]
    ok = np.isfinite(rl)
    worst[f] = (float(np.max(np.abs(rl[ok] / rpa[ok] - 1))), int((~ok).sum()))
    alla, _ = peri_analytic(HOSTS[("MW", f)], XALL, VALL)
    okk = np.isfinite(ORB[f]["rp"])
    worst[f + "_all"] = float(np.mean(np.abs(ORB[f]["rp"][okk] / alla[okk] - 1) > 0.01))
    ORB[f]["rp_analytic"] = alla
check("C-ORB: every central orbit's leapfrog pericentre equals the exact (E, L) root to 1%",
      "; ".join(f"{f}: max |rel| {worst[f][0]:.2e} ({worst[f][1]} central orbits without a pericentre in t_H); fraction of all draws off by > 1%: "
                f"{worst[f + '_all']:.4f}" for f in FOOTS), all(worst[f][0] <= 0.01 for f in FOOTS), load_bearing=LB0)

PF = 2.0 if MODE == 1 else 1.0
DT_MW = {}           # (foot, name) -> dict(med, p16, p84, ...) in Myr^-2
PERI = {}
for f in FOOTS:
    Hm = HOSTS[("MW", f)]
    for n in names:
        s = SL[n]
        rp, vp, tp = ORB[f]["rp"][s], ORB[f]["vp"][s], ORB[f]["tp"][s]
        Dt = np.where(np.isfinite(rp), Dt_of(Hm, np.where(np.isfinite(rp), rp, 1.0), np.where(np.isfinite(rp), vp, 0.0), PF), 0.0)
        Dd = Dt[1:]
        DT_MW[(f, n)] = dict(med=float(np.median(Dd)), p16=float(np.percentile(Dd, 16)), p84=float(np.percentile(Dd, 84)))
        rpd = rp[1:]
        PERI[(f, n)] = dict(rp_central=float(rp[0]), rp_med=float(np.nanmedian(rpd)), rp16=float(np.nanpercentile(rpd, 16)),
                            rp84=float(np.nanpercentile(rpd, 84)), t_med=float(np.nanmedian(tp[1:])), vp_med=float(np.nanmedian(vp[1:])) / KMS,
                            nopr=float(np.mean(~np.isfinite(rpd))), rnow=rnow_c[n], vr_now=vr_c[n])

# ================================================================================================ the M31 pool (MW-derived orbit shapes)
rngv = np.random.default_rng(2861)
cos_t = rngv.uniform(-1.0, 1.0, len(XALL)); sin_t = np.sqrt(1.0 - cos_t ** 2)
rnow_all = np.linalg.norm(XALL, axis=1)
POOL = {}
for f in FOOTS:
    Hm = HOSTS[("MW", f)]
    rp = ORB[f]["rp"]; vp = ORB[f]["vp"]
    draw_mask = np.ones(len(XALL), bool); draw_mask[[SL[n].start for n in names]] = False     # the pool uses the 54 x 1000 random draws
    has = np.isfinite(rp) & draw_mask
    eta = np.where(has, vp / Hm.vc(np.where(has, rp, 1.0)), np.nan)
    POOL[f] = dict(qproj=(rp / np.maximum(rnow_all * sin_t, 1e-9))[draw_mask], q3d=(rp / rnow_all)[draw_mask], eta=eta[draw_mask],
                   has=has[draw_mask])
    P(f"    M31 pool ({f}): {int(draw_mask.sum())} entries, {int(POOL[f]['has'].sum())} with a pericentre; median q' = r_p/R_proj "
      f"{np.nanmedian(POOL[f]['qproj'][POOL[f]['has']]):.3f}, median q = r_p/r_now {np.nanmedian(POOL[f]['q3d'][POOL[f]['has']]):.3f}, "
      f"median eta = v_p/v_c(r_p) {np.nanmedian(POOL[f]['eta'][POOL[f]['has']]):.3f}")


def angsep(ra1, dec1, ra2, dec2):
    a1, d1, a2, d2 = map(math.radians, (ra1, dec1, ra2, dec2))
    return math.acos(min(1.0, math.sin(d1) * math.sin(d2) + math.cos(d1) * math.cos(d2) * math.cos(a1 - a2)))


def hms(s):
    h, m, x = [float(t) for t in s.split()]; return (h + m / 60 + x / 3600) * 15.0


def dms(s):
    sg = -1.0 if s.strip().startswith("-") else 1.0
    a, b, c = [abs(float(t)) for t in s.replace("+", "").replace("-", "").split()]
    return sg * (a + b / 60 + c / 3600)


M31GEO = {}
for d in SAMPLES["m31"]:
    r = M31ROWS[d["name"]]
    M31GEO[("m31", d["name"])] = dict(Rproj=M31_D * angsep(fnum(r["ra"]), fnum(r["dec"]), M31_RA, M31_DEC), D3=d["D"])
for d in SAMPLES["col"]:
    M31GEO[("col", d["name"])] = dict(Rproj=M31_D * angsep(hms(d["ra"]), dms(d["dec"]), M31_RA, M31_DEC), D3=d["D"])


def Dt_m31(f, Rval, route, pf=PF):
    """median / 16 / 84 percentile tidal denominator over the MW pool for an M31 satellite at radius Rval (kpc)."""
    Hm = HOSTS[("M31", f)]; po = POOL[f]
    q = po["qproj"] if route == "proj" else po["q3d"]
    has = po["has"]
    rp = np.where(has, np.minimum(q * Rval, 9.9e4), 1.0)
    vp = np.where(has, po["eta"] * Hm.vc(rp), 0.0)
    Dt = np.where(has, Dt_of(Hm, rp, vp, pf), 0.0)
    rpm = rp[has]
    return dict(med=float(np.median(Dt)), p16=float(np.percentile(Dt, 16)), p84=float(np.percentile(Dt, 84)),
                rp_med=float(np.median(rpm)), rp16=float(np.percentile(rpm, 16)), rp84=float(np.percentile(rpm, 84)))


def Dt_m31_circ(f, Rval, pf=PF):
    Hm = HOSTS[("M31", f)]
    rp = np.array([Rval]); vp = Hm.vc(rp)
    v = float(Dt_of(Hm, rp, vp, pf)[0]); return dict(med=v, p16=v, p84=v, rp_med=Rval, rp16=Rval, rp84=Rval)


DT_M31 = {}
for f in FOOTS:
    for key, geo in M31GEO.items():
        DT_M31[(f, "proj") + key] = Dt_m31(f, geo["Rproj"], "proj")
        DT_M31[(f, "3d") + key] = Dt_m31(f, geo["D3"], "3d")
        DT_M31[(f, "literal") + key] = Dt_m31_circ(f, geo["Rproj"])
        DT_M31[(f, "bound") + key] = Dt_m31_circ(f, geo["D3"])


# ================================================================================================ the satellite: mass profile, Jacobi radius, stripped sigma
def parts(d, foot, ups=None, floor_mh=None, gas=False):
    a0 = A0H[foot]; ups = UPS_V if ups is None else ups
    Ms = ups * d["LV"]
    Mb = Ms + (max(1.33 * d["MHI"], infall_gas(d)) if gas else 1.33 * d["MHI"])
    rh_pc = (4.0 / 3.0) * d["rh"]; rh = rh_pc * 3.0857e16
    gN = G_SAT * 0.5 * Mb * MSUN_SAT / rh ** 2
    g = a_int(gN, 0.0, a0)
    Mh = float(halo_mass(UPS_V * d["LV"]))
    if floor_mh is not None and UPS_V * d["LV"] < 1e5:
        Mh = floor_mh
    ph, r_e = edge_info(Mb, foot)
    fex = max(0.0, 1.0 - ph / ((1 - FB) * Mh))
    return dict(a0=a0, Mb=Mb, rh_pc=rh_pc, rh=rh, gN=gN, g_law=g, Mh=Mh, fex=fex, a_pl=rh_pc / 1000.0 * math.sqrt(2 ** (2 / 3.) - 1))


def Mb_enc(pt, r_kpc, profile):
    if profile == "point":
        return pt["Mb"]
    return pt["Mb"] * r_kpc ** 3 / (r_kpc ** 2 + pt["a_pl"] ** 2) ** 1.5


def M_law_enc(pt, r_kpc, profile):
    rm = r_kpc * KPC_M
    gN = G_SAT * Mb_enc(pt, r_kpc, profile) * MSUN_SAT / rm ** 2
    return a_int(gN, 0.0, pt["a0"]) * rm ** 2 / (G_SAT * MSUN_SAT)


def m_enc(pt, r_kpc, profile="plummer"):
    return M_law_enc(pt, r_kpc, profile) + pt["fex"] * (1 - FB) * float(nfw_enclosed(pt["Mh"], r_kpc))


def solve_rt(mfun, Dt_myr):
    """King/Jacobi radius [kpc]: r^3 D_t = G m(<r); inf if D_t <= 0 or no crossing below 1e4 kpc."""
    if not (Dt_myr > 0):
        return math.inf
    Dsi = Dt_myr / MYR_S ** 2
    F = lambda lr: math.log(G_SAT * MSUN_SAT * mfun(math.exp(lr))) - math.log((math.exp(lr) * KPC_M) ** 3 * Dsi)
    lo, hi = math.log(1e-4), math.log(1e4)
    if F(hi) >= 0:
        return math.inf
    if F(lo) <= 0:
        return 1e-4
    return math.exp(brentq(F, lo, hi, xtol=1e-13, rtol=1e-15, maxiter=500))


JAC_RES = [0.0]


def sigma_strip(d, foot, Dt, ups=None, floor_mh=None, gas=False, rt_force=None, profile="plummer", trunc_phantom=False):
    """FG001's estimator with the debris truncated at the Jacobi radius; returns (sigma km/s, r_t kpc, parts)."""
    pt = parts(d, foot, ups, floor_mh, gas)
    if rt_force is not None:
        rt = rt_force
    else:
        rt = solve_rt(lambda r: m_enc(pt, r, profile), Dt)
        if math.isfinite(rt) and rt > 1e-4:
            JAC_RES[0] = max(JAC_RES[0], abs((rt * KPC_M) ** 3 * Dt / MYR_S ** 2 / (G_SAT * MSUN_SAT * m_enc(pt, rt, profile)) - 1))
    G, Ms_, kpc = SI_SAT
    r = np.asarray(pt["rh_pc"] / 1000.0)
    conv = G * Ms_ / (r * kpc) ** 2
    g = pt["g_law"]
    if trunc_phantom and rt < float(r):
        mass = 0.5 * pt["Mb"] + (M_law_enc(pt, rt, profile) - Mb_enc(pt, rt, profile)) + pt["fex"] * (1 - FB) * float(nfw_enclosed(pt["Mh"], rt))
        g = G_SAT * mass * MSUN_SAT / pt["rh"] ** 2
    elif rt > 0:
        g += float(pt["fex"] * (1 - FB) * np.asarray(nfw_enclosed(pt["Mh"], np.minimum(r, rt)), float) * conv)
    return math.sqrt(g * pt["rh"] / 3.0) / 1e3, rt, pt


# ================================================================================================ the statistics (CFG45's recipe)
def dt_lookup(pop, f, name, route, which="med"):
    if pop in ("ufd", "ul", "cls"):
        return DT_MW[(f, name)][which]
    return DT_M31[(f, route, pop, name)][which]


def offsets(pop, f, route="proj", which="med", **kw):
    gas = pop != "ufd"
    samp = SAMPLES[pop]
    x = np.array([math.log10(d["sig"] / sigma_strip(d, f, dt_lookup(pop, f, d["name"], route, which), gas=gas, **kw)[0]) for d in samp])
    if pop != "ufd":
        return x, None
    xu = np.array([math.log10(d["sig_ul"] / sigma_strip(d, f, dt_lookup("ul", f, d["name"], route, which), gas=False, **kw)[0]) for d in UL])
    return x, xu


def pop_stat(pop, f, route="proj", which="med", **kw):
    if pop == "ufd":
        x, xu = offsets(pop, f, route, which, **kw)
        m = km_median(x, xu); err = boot(x, xu)
        uv = [km_median(*offsets(pop, f, route, which, ups=u_, **kw)) for u_ in (1.0, 4.0)]
        f_ups = 0.5 * abs(uv[1] - uv[0])
        flo = [km_median(*offsets(pop, f, route, which, floor_mh=fm, **kw)) for fm in FLOORS]
        f_mh = 0.5 * (max(flo) - min(flo))
        tot = math.sqrt(err ** 2 + f_ups ** 2 + f_mh ** 2)
        return dict(med=m, km=m, err=err, f_ups=f_ups, f_mh=f_mh, tot=tot, z=m / tot, per=x.tolist(), per_ul=xu.tolist())
    x, _ = offsets(pop, f, route, which, **kw)
    uv = [offsets(pop, f, route, which, ups=u_, **kw)[0] for u_ in (1.0, 4.0)]
    f_ups = 0.5 * abs(float(np.median(uv[1])) - float(np.median(uv[0])))
    flo = [float(np.median(offsets(pop, f, route, which, floor_mh=fm, **kw)[0])) for fm in FLOORS]
    err = 1.2533 * float(np.std(x)) / math.sqrt(len(x))
    tot = math.sqrt(err ** 2 + f_ups ** 2 + (0.5 * (max(flo) - min(flo))) ** 2)
    return dict(med=float(np.median(x)), err=err, f_ups=f_ups, f_mh=0.5 * (max(flo) - min(flo)), tot=tot, z=float(np.median(x)) / tot, per=x.tolist())


RT_FORCE = {2: math.inf, 3: 0.0}.get(MODE)
ST, ST_S, ST_L = {}, {}, {}
for f in FOOTS:
    for p in POPS:
        ST[(p, f, "proj")] = pop_stat(p, f, "proj", rt_force=RT_FORCE)
        ST_S[(p, f)] = pop_stat(p, f, "proj", rt_force=math.inf)
        ST_L[(p, f)] = pop_stat(p, f, "proj", rt_force=0.0)
    for p in ("m31", "col"):
        ST[(p, f, "3d")] = pop_stat(p, f, "3d", rt_force=RT_FORCE)

# ================================================================================================ controls M2 / M3 (inline in every mode) and C-JAC
R.banner("CONTROLS M2 (no stripping = CFG45 reading S) / M3 (full stripping = CFG45 reading L = CFG244 (a1)) / C-JAC")


def cmp(ours, key_uf, key_cl):
    devs = []
    for f in FOOTS:
        u_ = C45["UF"][f"{f}|{key_uf}"]; o = ours[("ufd", f)]
        devs += [abs(o["km"] - u_["km"]), abs(o["err"] - u_["err"]), abs(o["f_ups"] - u_["f_ups"]), abs(o["f_mh"] - u_["f_mh"]),
                 abs(o["tot"] - u_["tot"]), abs(o["z"] - u_["z"])]
        for p in ("cls", "m31", "col"):
            c_ = C45["CL"][f"{p}|{f}|{key_cl}"]; o = ours[(p, f)]
            devs += [abs(o["med"] - c_["med"]), abs(o["tot"] - c_["tot"]), abs(o["z"] - c_["z"])]
    return max(devs), len(devs)


d2, n2 = cmp(ST_S, "S", "S")
d3, n3 = cmp(ST_L, "L", "L")
d28 = max(abs(ST_L[("ufd", f)]["km"] - C28["RES"][f]["km"][0]) for f in FOOTS)
check("M2 CONTROL: no stripping (r_t = inf) reproduces CFG45's committed reading S (UF km/err/f_ups/f_mh/tot/z; CL med/tot/z; 4 populations, "
      "both footings)", f"max |d| {d2:.1e} over {n2} numbers (<= 1e-9)", d2 <= 1e-9, load_bearing=MODE in (0, 2))
check("M3 CONTROL: full stripping (r_t = 0) reproduces CFG45's committed reading L (= B's frozen isolated law, CFG244's (a1) 'own nothing'), "
      "and P1's KM median equals CFG28's committed RES", f"max |d| {d3:.1e} over {n3} numbers; CFG28 KM |d| {d28:.1e} (<= 1e-9)",
      d3 <= 1e-9 and d28 <= 1e-9, load_bearing=MODE in (0, 3))
# Kepler check of the Jacobi solver: point-mass satellite, Newtonian point host, circular orbit
Hk = Host(1e11, 1e-30, nu=lambda y: np.ones_like(np.asarray(y, float)))
rk, mk = 50.0, 1e8
vk = Hk.vc(np.array([rk])); Dk = float(Dt_of(Hk, np.array([rk]), vk)[0])
rt_k = solve_rt(lambda r: mk, Dk); rt_exact = rk * (mk / (3 * 1e11)) ** (1 / 3.)
check("C-JAC CONTROL: the Jacobi solve satisfies r_t^3 D_t = G m(<r_t) for every satellite solved; Kepler limit r_p (m / 3M)^(1/3)",
      f"max residual {JAC_RES[0]:.1e} (<= 1e-8); Kepler {rt_k:.6f} vs {rt_exact:.6f} kpc (rel {rt_k / rt_exact - 1:+.1e}, <= 1e-6)",
      JAC_RES[0] <= 1e-8 and abs(rt_k / rt_exact - 1) <= 1e-6, load_bearing=LB0)


# ================================================================================================ per-satellite table
def sat_rows(f):
    rows = []
    for p in POPS:
        samp = SAMPLES[p] + (UL if p == "ufd" else [])
        for i, d in enumerate(samp):
            is_ul = p == "ufd" and i >= len(SAMPLES["ufd"])
            gas = p != "ufd"
            key = "ul" if is_ul else p
            Dt = dt_lookup(key, f, d["name"], "proj")
            s_st, rt, pt = sigma_strip(d, f, Dt, gas=gas, rt_force=RT_FORCE)
            s_S = sigma_strip(d, f, Dt, gas=gas, rt_force=math.inf)[0]
            row = dict(pop=p + ("_ul" if is_ul else ""), name=d["name"], footing=f, D_t=Dt, r_t_kpc=rt, r_ev_kpc=pt["rh_pc"] / 1000.0,
                       rt_over_rev=rt / (pt["rh_pc"] / 1000.0), fex=pt["fex"], M_c=pt["Mh"], dlogsig_strip_minus_S=math.log10(s_st / s_S),
                       sigma_obs=d.get("sig", d.get("sig_ul")), sigma_pred=s_st, offset=math.log10(d.get("sig", d.get("sig_ul")) / s_st))
            if p in ("ufd", "cls"):
                pr = PERI[(f, d["name"])]
                row.update(rp_med=pr["rp_med"], rp16=pr["rp16"], rp84=pr["rp84"], rp_central=pr["rp_central"], t_since_Myr=pr["t_med"],
                           vp_kms=pr["vp_med"], no_peri_frac=pr["nopr"], r_now=pr["rnow"], vr_now=pr["vr_now"], route="orbit")
            else:
                dd = DT_M31[(f, "proj", p, d["name"])]
                row.update(rp_med=dd["rp_med"], rp16=dd["rp16"], rp84=dd["rp84"], rp_central=float("nan"), t_since_Myr=float("nan"),
                           vp_kms=float("nan"), no_peri_frac=float("nan"), r_now=M31GEO[(p, d["name"])]["D3"], vr_now=float("nan"),
                           R_proj=M31GEO[(p, d["name"])]["Rproj"], route="M31 projected x MW pool")
            rows.append(row)
    return rows


ROWS = {f: sat_rows(f) for f in FOOTS}

R.banner("PERICENTRES (law host, median of 1000 draws; M31 = projected radius x the MW pool)")
for f in FOOTS:
    P(f"  --- {f} ---")
    for p in POPS:
        rs = [r_ for r_ in ROWS[f] if r_["pop"].startswith(p)]
        rpm = np.array([r_["rp_med"] for r_ in rs]); ratio = np.array([r_["rt_over_rev"] for r_ in rs])
        nstr = int(np.sum(ratio < 1))
        P(f"    {PLAB[p]:34s}: median r_p {np.median(rpm):6.1f} kpc (range {rpm.min():.1f}-{rpm.max():.1f}); median r_t/r_ev "
          f"{np.median(ratio[np.isfinite(ratio)]) if np.isfinite(ratio).any() else float('inf'):.2f}; r_t < r_ev in {nstr} of {len(rs)}"
          + (": " + ", ".join(f"{r_['name']} ({r_['rt_over_rev']:.2f})" for r_ in rs if r_["rt_over_rev"] < 1) if nstr else ""))
    for nm in ("Sagittarius", "LMC", "Tucana III", "Crater II", "Antlia II", "Draco"):
        r_ = next(x for x in ROWS[f] if x["name"] == nm)
        P(f"      {nm:12s} r_p {r_['rp_med']:.1f} [{r_['rp16']:.1f}, {r_['rp84']:.1f}] kpc, last pericentre {r_['t_since_Myr']:.0f} Myr ago, "
          f"r_t {r_['r_t_kpc']:.3f} kpc vs r_ev {r_['r_ev_kpc']:.3f} kpc, d log sigma {r_['dlogsig_strip_minus_S']:+.4f}")
    inside = [r_["name"] for r_ in ROWS[f] if r_.get("route") == "orbit" and r_["rp_med"] < 8.122]
    P(f"    median pericentre inside R0 (the point-mass host is not the Galaxy there; flagged): {inside}")

# ================================================================================================ the verdict
R.banner("H1 / H2 AND THE VERDICT (CFG45's error recipe; primary M31 route = projected radius)")
for f in FOOTS:
    for p in POPS:
        s, s0 = ST[(p, f, "proj")], ST_S[(p, f)]
        P(f"    {f:9s} {PLAB[p]:34s}: {s['med']:+.4f} +- {s['tot']:.4f} dex  z = {s['z']:+.2f}   [no stripping (S): {s0['med']:+.4f}, z {s0['z']:+.2f}; "
          f"shift {s['med'] - s0['med']:+.4f} dex, {s['z'] - s0['z']:+.2f} sigma]")
    for p in ("m31", "col"):
        s = ST[(p, f, "3d")]
        P(f"    {f:9s} {PLAB[p] + ' [3D route]':34s}: {s['med']:+.4f} +- {s['tot']:.4f} dex  z = {s['z']:+.2f}")
H1 = {f: abs(ST[("ufd", f, "proj")]["z"]) < 2 for f in FOOTS}
H2 = {f: all(abs(ST[(p, f, "proj")]["z"]) < 2 for p in ("cls", "m31", "col")) for f in FOOTS}
H2alt = {f: all(abs(ST[(p, f, "3d" if p != "cls" else "proj")]["z"]) < 2 for p in ("cls", "m31", "col")) for f in FOOTS}
both = {f: H1[f] and H2[f] for f in FOOTS}
if all(H1.values()) and all(H2.values()) and all(H2alt.values()):
    VERDICT = "JOINT PASS"
elif all(H1.values()) and all(H2.values()):
    VERDICT = "PARTIAL (the M31 part fails under the alternate 3D route)"
elif sum(both.values()) == 1:
    VERDICT = "PARTIAL (joint on one footing only)"
elif (all(H1.values()) and sum(H2.values()) == 1) or (all(H2.values()) and sum(H1.values()) == 1):
    VERDICT = "PARTIAL (one hypothesis on both footings, the other on one)"
else:
    VERDICT = "FAIL"
BIND = {}
for f in FOOTS:
    bad_ = [(abs(ST[(p, f, "proj")]["z"]), p) for p in POPS if abs(ST[(p, f, "proj")]["z"]) >= 2]
    BIND[f] = (PLAB[max(bad_)[1]] + f" (z {ST[(max(bad_)[1], f, 'proj')]['z']:+.2f}, {ST[(max(bad_)[1], f, 'proj')]['med']:+.3f} dex)") if bad_ else None
check("H1 ultra-faints consistent: |z| < 2 on both footings",
      "; ".join(f"{f}: {ST[('ufd', f, 'proj')]['med']:+.3f} dex, z {ST[('ufd', f, 'proj')]['z']:+.2f}" for f in FOOTS), all(H1.values()), load_bearing=LB0)
check("H2 classicals consistent: |z| < 2 for MW classical, M31 LVD and M31 Collins+13 on both footings (primary M31 route)",
      "; ".join(f"{f}: " + ", ".join(f"{p} {ST[(p, f, 'proj')]['z']:+.2f}" for p in ("cls", "m31", "col")) for f in FOOTS), all(H2.values()), load_bearing=LB0)
check("H2-alt (decides PARTIAL): the same with the M31 3D route", "; ".join(f"{f}: " + ", ".join(
    f"{p} {ST[(p, f, '3d' if p != 'cls' else 'proj')]['z']:+.2f}" for p in ("cls", "m31", "col")) for f in FOOTS), all(H2alt.values()),
      load_bearing=False)
P(f"\n    VERDICT: {VERDICT}" + ("" if VERDICT == "JOINT PASS" else "   binding population: " + "; ".join(f"{f}: {BIND[f]}" for f in FOOTS)))
one_sig = {f: all(abs(ST[(p, f, "proj")]["z"]) < 1 for p in POPS) for f in FOOTS}
a2 = {f: all(ST[(p, f, "proj")]["z"] > -2 for p in ("cls", "m31", "col")) for f in FOOTS}
P(f"    reported: all four within 1 sigma (CFG59's strict level): {one_sig};  the record's one-sided A2 (no classical population below -2 sigma): {a2}")
P("    caveat (CFG244 / CFG259): the ultra-faint preference for a retained core is carried by a few systems, with margins of fractions of a chi^2.")

# ================================================================================================ reported rows
REP = {}
if MODE == 0:
    R.banner("REPORTED ROWS (never verdicts)")
    # 6: pericentre floor
    for f in FOOTS:
        out = {}
        for p in POPS:
            lo = pop_stat(p, f, "proj", which="p16")["med"]; hi = pop_stat(p, f, "proj", which="p84")["med"]
            fl = 0.5 * abs(hi - lo); s = ST[(p, f, "proj")]
            out[p] = dict(med_p16=lo, med_p84=hi, floor=fl, z_with=s["med"] / math.sqrt(s["tot"] ** 2 + fl ** 2))
        REP[f"peri_floor|{f}"] = out
        P(f"    [6 pericentre floor] {f}: " + "; ".join(f"{p} floor {v['floor']:.4f} -> z {v['z_with']:+.2f}" for p, v in out.items()))
    # 3: point-mass baryons; 4: phantom truncated too
    for lab, kw in (("3 point-mass baryons in m(<r)", dict(profile="point")), ("4 phantom truncated too", dict(trunc_phantom=True))):
        for f in FOOTS:
            out = {p: pop_stat(p, f, "proj", **kw) for p in POPS}
            REP[f"{lab}|{f}"] = {p: dict(med=v["med"], z=v["z"]) for p, v in out.items()}
            P(f"    [{lab}] {f}: " + "; ".join(f"{p} {v['med']:+.4f} (z {v['z']:+.2f})" for p, v in out.items()))
    # 5: M31 literal projected circular and the minimal-tide bound
    for route in ("literal", "bound"):
        for f in FOOTS:
            out = {p: pop_stat(p, f, route) for p in ("m31", "col")}
            REP[f"5 M31 {route}|{f}"] = {p: dict(med=v["med"], z=v["z"]) for p, v in out.items()}
            P(f"    [5 M31 {route}] {f}: " + "; ".join(f"{p} {v['med']:+.4f} (z {v['z']:+.2f})" for p, v in out.items()))

    # 1, 2, 7: host variants (pericentres by the exact (E, L) root on the same draws; main's no-pericentre flags kept)
    def host_variant_stats(label, hostfun):
        saveMW, saveM31 = dict(DT_MW), dict(DT_M31)
        res = {}
        for f in FOOTS:
            Hv = hostfun(f)
            rpa, vpa = peri_analytic(Hv, XALL, VALL)
            has = np.isfinite(ORB[f]["rp"])
            for n in names:
                s_ = SL[n]
                Dt = np.where(has[s_], Dt_of(Hv, rpa[s_], vpa[s_]), 0.0)[1:]
                DT_MW[(f, n)] = dict(med=float(np.median(Dt)), p16=float(np.percentile(Dt, 16)), p84=float(np.percentile(Dt, 84)))
            res[f] = {p: pop_stat(p, f, "proj") for p in ("ufd", "cls")}
        DT_MW.clear(); DT_MW.update(saveMW); DT_M31.clear(); DT_M31.update(saveM31)
        return res

    for lab, hf in (("1 MW host 7.3e10 Msun", lambda f: Host(MW_MB_CENSUS_HI, A0H[f])),
                    ("2 MW host, exponential RAR kernel", lambda f: Host(MW_MB, A0H[f], nu=lambda y: 1.0 / (-np.expm1(-np.sqrt(np.maximum(np.asarray(y, float), 1e-12))))))):
        res = host_variant_stats(lab, hf)
        for f in FOOTS:
            REP[f"{lab}|{f}"] = {p: dict(med=v["med"], z=v["z"], shift=v["med"] - ST[(p, f, "proj")]["med"]) for p, v in res[f].items()}
            P(f"    [{lab}] {f}: " + "; ".join(f"{p} {v['med']:+.4f} (z {v['z']:+.2f}; shift {v['med'] - ST[(p, f, 'proj')]['med']:+.4f})"
                                              for p, v in res[f].items()))
    # 7: the hosts' own rule debris
    fexh = {}
    for hname, Mb_h, Ms_h in (("MW", MW_MB, 5.0e10), ("M31", M31_MB, 1.0e11)):
        for f in FOOTS:
            ph, _ = edge_info(Mb_h, f); Mc = collapse(Ms_h, "blue")
            fexh[(hname, f)] = (max(0.0, 1.0 - ph / ((1 - FB) * Mc)), Mc, ph)
    P("    [7 the hosts' own rule f_ex] " + "; ".join(f"{h} {f}: f_ex {v[0]:.3f} (M_c {v[1]:.2e}, edge phantom {v[2]:.2e})" for (h, f), v in fexh.items()))
    REP["7 host fex"] = {f"{h}|{f}": v for (h, f), v in fexh.items()}
    if any(v[0] > 0 for (h, f), v in fexh.items() if h == "MW"):
        res = host_variant_stats("7 MW host + its own debris", lambda f: Host(MW_MB, A0H[f], debris=(fexh[("MW", f)][0], fexh[("MW", f)][1])))
        for f in FOOTS:
            REP[f"7 MW host + debris|{f}"] = {p: dict(med=v["med"], z=v["z"], shift=v["med"] - ST[(p, f, "proj")]["med"]) for p, v in res[f].items()}
            P(f"    [7 MW host + its own debris] {f}: " + "; ".join(f"{p} {v['med']:+.4f} (z {v['z']:+.2f}; shift "
                                                                  f"{v['med'] - ST[(p, f, 'proj')]['med']:+.4f})" for p, v in res[f].items()))
    if any(v[0] > 0 for (h, f), v in fexh.items() if h == "M31"):
        P("    [7] the M31 host's own debris is > 0; its row is not run (M31 enters only through the pool transfer; stated, not computed).")

# ================================================================================================ MUTATE=1 check
if MODE == 1:
    R.banner("M1  PERICENTRE x2 (fixed pericentre speed): does the classicals' prediction move?")
    main = json.load(open(os.path.join(HERE, "cfg286_tidal_stripping_results.json")))["numbers"]["ST"]
    dmax = {}
    for f in FOOTS:
        for p in ("cls", "m31", "col"):
            dmax[(p, f)] = ST[(p, f, "proj")]["med"] - main[f"{p}|{f}|proj"]["med"]
    P("    shifts of the median offsets vs the main run: " + "; ".join(f"{p}|{f} {v:+.4f}" for (p, f), v in dmax.items()))
    unchanged = all(abs(v) < 0.01 for v in dmax.values())
    check("M1 [MUTATE; must FAIL for the stripping to bite] UNCHANGED: every classical population's median offset within 0.01 dex of the main run's, "
          "both footings", f"max |shift| {max(abs(v) for v in dmax.values()):.4f} dex", unchanged)
    R.num("M1_shifts", {f"{p}|{f}": v for (p, f), v in dmax.items()})

# ================================================================================================ outputs
R.num("mode", MODE)
R.num("ST", {f"{p}|{f}|{route}": dict(med=s["med"], err=s["err"], f_ups=s["f_ups"], f_mh=s["f_mh"], tot=s["tot"], z=s["z"])
             for (p, f, route), s in ST.items()})
R.num("ST_S", {f"{p}|{f}": dict(med=s["med"], tot=s["tot"], z=s["z"]) for (p, f), s in ST_S.items()})
R.num("ST_L", {f"{p}|{f}": dict(med=s["med"], tot=s["tot"], z=s["z"]) for (p, f), s in ST_L.items()})
R.num("H1", H1); R.num("H2", H2); R.num("H2alt", H2alt); R.num("VERDICT", VERDICT); R.num("BIND", BIND)
R.num("one_sigma", one_sig); R.num("A2_one_sided", a2)
R.num("controls", dict(C_ORB=worst, M2=d2, M3=d3, CFG28=d28, C_JAC=JAC_RES[0]))
R.num("reported", REP)
R.num("n_stripped", {f: {p: int(sum(1 for r_ in ROWS[f] if r_["pop"].startswith(p) and r_["rt_over_rev"] < 1)) for p in POPS} for f in FOOTS})
if MODE == 0:
    keys = ["pop", "name", "footing", "route", "r_now", "R_proj", "vr_now", "rp_central", "rp_med", "rp16", "rp84", "t_since_Myr", "vp_kms",
            "no_peri_frac", "D_t", "M_c", "fex", "r_t_kpc", "r_ev_kpc", "rt_over_rev", "dlogsig_strip_minus_S", "sigma_obs", "sigma_pred", "offset"]
    with open(os.path.join(HERE, "cfg286_pericentres.csv"), "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=keys, extrasaction="ignore")
        w.writeheader()
        for f in FOOTS:
            for r_ in ROWS[f]:
                w.writerow({k: (f"{r_[k]:.6g}" if isinstance(r_.get(k), float) else r_.get(k, "")) for k in keys})
    np.savez_compressed(os.path.join(HERE, "cfg286_orbit_draws.npz"), names=np.array(names), X=XALL, V=VALL,
                        **{f"{k}_{f}": ORB[f][k] for f in FOOTS for k in ("rp", "vp", "tp", "rp_analytic")})
P(f"\n  run time {time.time() - T0:.0f} s.  kappa = 1/2 FITTED; the cold fluid's mass is still required; nothing here says the theory is closed.")
nf = R.write(here=HERE)
sys.exit(1 if nf else 0)
