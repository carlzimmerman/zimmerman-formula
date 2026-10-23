#!/usr/bin/env python3
"""Z2_satellite_systematics -- how much of the dwarf-satellite excess is real?
Criteria: FROZEN_CRITERIA.md + ASSUMPTION_LEDGER.md (committed alone first, 5f7526ab41).

Task 1: reconcile T1's host-field tracking with CFG838/839 (factor grid: sample, residual, variable, statistic).
Task 2: pre-declared systematics tests on E3's clean sample (tides at the PM pericentre in S1's own MW field,
ellipticity / velocity gradient, member counts, UFD vs classical, host distance / field) and a frozen dynamically
clean subset, for v3 static (V3S), v3 dust-free (V3D, U1 B0) and plain AQUAL with the host field (MOND).

Run:  OMP_NUM_THREADS=1 nice -n 15 python3 z2_satellite_systematics.py            (-> .out, _results.json, CSV)
      OMP_NUM_THREADS=1 nice -n 15 python3 z2_satellite_systematics.py --mutate   (data replaced by a pure tidal artefact)
Deterministic (seeded), no network.  kappa = 1/2 FITTED; footings never pooled; not theory closed."""
import csv, json, math, os, resource, sys, time, warnings
import numpy as np
from scipy.stats import spearmanr, chi2 as chi2dist, theilslopes
from scipy.optimize import minimize_scalar

warnings.filterwarnings("ignore")
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, os.path.join(REPO, "doors_push_2026_10_22", "D10_native_Lstar"))
sys.path.insert(0, os.path.join(REPO, "campaign_fresh_gravity", "CFG51_walker_multiepoch"))
import d10_solver as S          # noqa: E402  (read-only)
import reduce_walker as RW      # noqa: E402  (read-only; main() is guarded)

MUT = "--mutate" in sys.argv
SFX = "_MUTATE" if MUT else ""
T0 = time.time()
OUT = []
def P(s=""):
    print(s, flush=True); OUT.append(str(s))
CHK = {}
def check(k, ok, val, thr, what):
    CHK[k] = dict(ok=bool(ok), value=val, threshold=thr, what=what)
    P(f"{k} {'PASS' if ok else 'FAIL'} {val} {thr}  ({what})")

# ------------------------------------------------------------------ constants (S1's)
G, MSUN, PC = 6.67430e-11, 1.989e30, 3.0856775814913673e16
KPC = 1e3 * PC
A0 = {"canonical": 9.3603e-11, "alt": 1.1312e-10}
FOOTS = ("canonical", "alt")
LFLOOR = {"canonical": 21.68, "alt": 22.85}
A_H = 3.0 * KPC
GE2_8KPC = 2.0592e-10
MHOST = {"MW": 6.0e10, "M31": 1.0e11, "field": 6.0e10}
NMC, NBOOT = 2000, 4000
DY, DL = 0.6, 0.3
FW_N = 2.0 * (4 / 3) ** 3 / (1 + (4 / 3) ** 2) ** 1.5
LFW = math.log10(FW_N)
R12 = 4.0 / 3.0
Q_SAFE, Q_EXP, E_FLAG, NQ_MIN, GRAD_P, NCLEAN_MIN = 0.5, 1.0, 0.5, 10, 0.01, 6
FLAV = ("V3S", "V3D", "MOND", "ISO")
R = dict(lane="Z2_satellite_systematics", mutate=MUT, frozen="5f7526ab41",
         constants=dict(a0=A0, L_floor=LFLOOR, NMC=NMC, NBOOT=NBOOT, q_safe=Q_SAFE, e_flag=E_FLAG, NQ_min=NQ_MIN,
                        grad_p=GRAD_P, MHOST=MHOST, FW_N=FW_N))
P("=" * 112)
P("Z2_satellite_systematics: how much of the dwarf-satellite excess is real?" + ("   *** MUTATE: data = pure tidal artefact ***" if MUT else ""))
P("kappa = 1/2 FITTED; footings canonical 9.3603e-11 / alt 1.1312e-10 m/s^2, never pooled; not theory closed")
P("=" * 112)

# ------------------------------------------------------------------ host field (S1's, mu = x/(1+x) law on Hernquist)
def g_host(R_m, Mb, a0):
    gN = G * Mb * MSUN / (R_m + A_H) ** 2
    return 0.5 * gN * (1 + np.sqrt(1 + 4 * a0 / gN))
def Mb_hi(a0):
    gN = GE2_8KPC ** 2 / (GE2_8KPC + a0)
    return gN * (8 * KPC + A_H) ** 2 / G / MSUN
def host_mass(host, ek, a0):
    return MHOST[host] * {"E_lo": 4.0e10 / 6.0e10, "E_mid": 1.0, "E_hi": Mb_hi(a0) / 6.0e10}[ek]

# ------------------------------------------------------------------ solver wrappers (D10, read-only; S1's grid)
GR = S.Grid2D(nper=24, Nt=16)
NSOLVE = [0]; WORST = [0.0]
def logG(y, xe, Lam):
    iso = xe <= 0
    sv = S.Solver2D(GR, y, 0.0 if iso else xe, Lam, isolated=iso)
    U, res, it = sv.solve(tol=1e-10)
    NSOLVE[0] += 1; WORST[0] = max(WORST[0], res)
    rf, gr = sv.field_monopole()
    _, vir, wo = S.jeans(rf, gr, [])
    return math.log10(6 * wo * R12 / y)

def lin3(x, xs, v):
    x = np.asarray(x, float)
    s0 = (v[1] - v[0]) / (xs[1] - xs[0]); s1 = (v[2] - v[1]) / (xs[2] - xs[1])
    return np.where(x < xs[1], v[1] + s0 * (x - xs[1]), v[1] + s1 * (x - xs[1]))
def interp2(ly, lL, ys, Ls, T):
    rows = [lin3(lL, Ls, T[i]) for i in range(3)]
    s0 = (rows[1] - rows[0]) / (ys[1] - ys[0]); s1 = (rows[2] - rows[1]) / (ys[2] - ys[1])
    return np.where(ly < ys[1], rows[1] + s0 * (ly - ys[1]), rows[1] + s1 * (ly - ys[1]))

# ================================================================== DATA (own implementation of E3/S1's build)
DATA = os.path.join(REPO, "real_research", "data")
CFG = os.path.join(REPO, "campaign_fresh_gravity")
def fl(x):
    try:
        v = float(x); return v if math.isfinite(v) else None
    except Exception:
        return None
LVDRAW = {}
def load_lvd():
    rows = []
    for fn, host in (("lvd_dwarf_mw.csv", "MW"), ("lvd_dwarf_m31.csv", "M31"), ("lvd_dwarf_local_field.csv", "field")):
        for r in csv.DictReader(open(os.path.join(DATA, "dsph", fn))):
            LVDRAW[r["name"]] = dict(r, _host=host)
            s = fl(r.get("vlos_sigma"))
            rh = fl(r.get("rhalf_sph_physical")) or fl(r.get("rhalf_physical"))
            ms = fl(r.get("mass_stellar")); mv = fl(r.get("M_V"))
            if not s or s <= 0 or not rh or rh <= 0:
                continue
            if ms is None and mv is not None:
                ms = 0.4 * (4.83 - mv) + 0.301
            if ms is None:
                continue
            rhe = fl(r.get("rhalf_sph_physical_em")) if fl(r.get("rhalf_sph_physical")) else fl(r.get("rhalf_physical_em"))
            rhp = fl(r.get("rhalf_sph_physical_ep")) if fl(r.get("rhalf_sph_physical")) else fl(r.get("rhalf_physical_ep"))
            rows.append(dict(name=r["name"], host=host, sigma=s, sem=fl(r.get("vlos_sigma_em")) or 0.1 * s,
                             sep=fl(r.get("vlos_sigma_ep")) or 0.1 * s, ul=bool(r.get("vlos_sigma_ul")),
                             rh=rh, rhem=rhe or 0.1 * rh, rhep=rhp or 0.1 * rh, logms=ms, MV=mv,
                             dmem=fl(r.get("distance_modulus_em")) or 0.1, dmep=fl(r.get("distance_modulus_ep")) or 0.1,
                             dhost=fl(r.get("distance_host")), dist=fl(r.get("distance")), ref=r.get("ref_vlos", ""),
                             ell=fl(r.get("ellipticity")), ell_ul=fl(r.get("ellipticity_ul"))))
    return rows
ALL = load_lvd()
BYNAME = {r["name"]: r for r in ALL}
ARR = list(csv.DictReader(open(os.path.join(CFG, "CFG257_ufd_kinematics_scoping", "arroyo_polonio2026_tableA1.csv"))))
arr_free = {r["lvd_name"]: float(r["sig_free"]) / float(r["sig_f0"]) for r in ARR}
arr_f07 = {r["lvd_name"]: float(r["sig_f07"]) / float(r["sig_f0"]) for r in ARR}
med_free = float(np.median(list(arr_free.values()))); med_f07 = float(np.median(list(arr_f07.values())))
GEH = {}; GEHN = {}
for r in csv.DictReader(open(os.path.join(CFG, "CFG257_ufd_kinematics_scoping", "geha_vs_lvd_match.csv"))):
    if r.get("geha_N_stars"):
        GEHN[r["lvd_name"]] = int(float(r["geha_N_stars"]))
    if r.get("geha_sigma_resolved") == "1" and fl(r.get("geha_sigma")):
        GEH[r["lvd_name"]] = (float(r["geha_sigma"]), fl(r.get("geha_e_sigma_ll")) or 0.1, fl(r.get("geha_e_sigma_ul")) or 0.1)
GEH2 = {r["full_name"]: r for r in csv.DictReader(open(os.path.join(CFG, "CFG257_ufd_kinematics_scoping", "geha2026_paperII_tableA1.csv")))}

def mcrit(a0):
    return a0 * (24.0 * PC) ** 2 / G / MSUN
SAMP = {f: [r for r in ALL if r["logms"] < math.log10(mcrit(A0[f]))] for f in FOOTS}

def split_normal(rng, c, em, ep, n):
    z = rng.standard_normal(n); return c + np.where(z < 0, z * em, z * ep)
def build(rows, a0, rng, ups=2.0, binmode="free", sig_src="lvd", drop_ul=False):
    keep = [r for r in rows if not (drop_ul and r["ul"])]
    N = len(keep)
    lb = np.empty((N, NMC)); ly = np.empty((N, NMC)); la = np.empty((N, NMC))
    for i, r in enumerate(keep):
        s, sem, sep = r["sigma"], r["sem"], r["sep"]
        if sig_src == "lower" and r["name"] in GEH:
            gs, gl, gu = GEH[r["name"]]
            if gs < s: s, sem, sep = gs, gl, gu
        b = 1.0
        if binmode == "free": b = arr_free.get(r["name"], med_free)
        elif binmode == "f07": b = arr_f07.get(r["name"], med_f07)
        fD = 10 ** (split_normal(rng, 0.0, r["dmem"], r["dmep"], NMC) / 5.0)
        sig = np.abs(split_normal(rng, s, sem, sep, NMC)) * b
        rh = np.abs(split_normal(rng, r["rh"], r["rhem"], r["rhep"], NMC)) * fD
        ms = ups / 2.0 * 10 ** r["logms"] * fD ** 2
        r12 = R12 * rh * PC
        gobs = 3.0 * (sig * 1e3) ** 2 / r12; gbar = G * (ms / 2) * MSUN / r12 ** 2
        lb[i] = np.log10(gobs / gbar)
        ly[i] = np.log10(G * ms * MSUN / ((rh * PC) ** 2 * a0)); la[i] = np.log10(rh)
    return dict(lb=lb, ly=ly, la=la, rows=keep)
def lb_central(r):
    b = arr_free.get(r["name"], med_free); sig = r["sigma"] * b * 1e3
    r12 = R12 * r["rh"] * PC; M = 10 ** r["logms"]
    return math.log10(3 * sig ** 2 / r12 / (G * (M / 2) * MSUN / r12 ** 2))
def y0_of(r, a0):
    return G * 10 ** r["logms"] * MSUN / ((r["rh"] * PC) ** 2 * a0)
def xe_of(r, a0, ek="E_mid"):
    Rh = (r["dhost"] if r["dhost"] else r["dist"]) * KPC
    return float(g_host(Rh, host_mass(r["host"], ek, a0), a0) / a0)

# ================================================================== CFG838 / CFG839 committed rows
J838 = json.load(open(os.path.join(CFG, "CFG838_satellite_tides", "cfg838_results.json")))
J839 = json.load(open(os.path.join(CFG, "CFG839_pericentre_tides", "cfg839_results.json")))
S838 = list(J838["rows"].keys()); S839 = list(J839["rows"].keys())
R828 = {n: J838["rows"][n]["delta"] for n in S838}

# ================================================================== prediction tables (cached stage)
STAGE = os.path.join(HERE, "z2_stage_tables.json")
def tabulate():
    TAB = {}
    for f in FOOTS:
        a0 = A0[f]
        names = sorted(set([r["name"] for r in SAMP[f]]) | set(n for n in S838 if n in BYNAME))
        for n in names:
            r = BYNAME[n]; y0 = y0_of(r, a0); xe = xe_of(r, a0)
            ys = math.log10(y0) + np.array([-DY, 0.0, DY]); Ls = math.log10(LFLOOR[f] / r["rh"]) + np.array([-DL, 0.0, DL])
            t = dict(y0=y0, xe=xe, ys=ys.tolist(), Ls=Ls.tolist())
            if n in [s["name"] for s in SAMP[f]]:
                t["iso0"] = [logG(10 ** v, 0.0, 0.0) for v in ys]
                t["emb0"] = [logG(10 ** v, xe, 0.0) for v in ys]
                t["isoF"] = [[logG(10 ** v, 0.0, 10 ** w) for w in Ls] for v in ys]
                t["embF"] = [[logG(10 ** v, xe, 10 ** w) for w in Ls] for v in ys]
            else:   # S_838-only systems: central values only
                c0 = logG(y0, 0.0, 0.0); cF = logG(y0, 0.0, 10 ** Ls[1]); eF = logG(y0, xe, 10 ** Ls[1]); e0 = logG(y0, xe, 0.0)
                t["iso0"] = [c0] * 3; t["emb0"] = [e0] * 3; t["isoF"] = [[cF] * 3] * 3; t["embF"] = [[eF] * 3] * 3
                t["central_only"] = True
            TAB[f"{f}|{n}"] = t
        P(f"   [{f}] {len(names)} systems tabulated ({NSOLVE[0]} solves, worst residual {WORST[0]:.1e}, {time.time() - T0:.0f} s)")
    return TAB
P("\n--- prediction tables (D10 stiffened-AQUAL solver, S1's grid; 3-node y and Lambda grids) ---")
if os.path.exists(STAGE):
    TAB = json.load(open(STAGE)); P(f"   read cached {os.path.basename(STAGE)} ({len(TAB)} entries)")
else:
    TAB = tabulate(); json.dump(TAB, open(STAGE, "w"), indent=0)
def cen(f, n, key):
    t = TAB[f"{f}|{n}"]
    if key == "V3D": return LFW
    if key == "ISO": return t["iso0"][1]
    if key == "MOND": return t["emb0"][1]
    if key == "V3S0": return t["isoF"][1][1]
    if key == "V3S": return t["embF"][1][1]
    raise KeyError(key)
def pred_draws(f, X, key):
    o = np.empty_like(X["lb"])
    for i, r in enumerate(X["rows"]):
        t = TAB[f"{f}|{r['name']}"]; ys = np.array(t["ys"]); Ls = np.array(t["Ls"])
        if key == "V3D": o[i] = LFW
        elif key == "ISO": o[i] = lin3(X["ly"][i], ys, np.array(t["iso0"]))
        elif key == "MOND": o[i] = lin3(X["ly"][i], ys, np.array(t["emb0"]))
        else:
            lL = math.log10(LFLOOR[f]) - X["la"][i]
            T = np.array(t["isoF"] if key == "V3S0" else t["embF"])
            o[i] = interp2(X["ly"][i], lL, ys, Ls, T)
    return o

# ================================================================== ORBITS in S1's MW field (and CFG839's, for K4)
import astropy.units as u                      # noqa: E402
import astropy.coordinates as coord            # noqa: E402
RG = np.logspace(math.log10(0.02 * KPC), math.log10(5000 * KPC), 20000)
def field_tables(gfun):
    g = gfun(RG)
    Phi = np.concatenate([[0.0], np.cumsum(0.5 * (g[1:] + g[:-1]) * np.diff(RG))])
    return g, Phi
def galcen(rowsel, ndraw, rng):
    """rowsel: list of LVD raw rows. Returns pos (m), vel (m/s) arrays (n, ndraw+1, 3); draw 0 = central."""
    ra, dec, D, pa, pd_, vl = [], [], [], [], [], []
    for r in rowsel:
        c = [fl(r["ra"]), fl(r["dec"])]
        dm = fl(r["distance_modulus"]); dme = fl(r.get("distance_modulus_em")) or 0.0; dmp = fl(r.get("distance_modulus_ep")) or 0.0
        Dc = fl(r["distance"])
        dmd = np.concatenate([[0.0], split_normal(rng, 0.0, dme, dmp, ndraw)])
        D.append(Dc * 10 ** (dmd / 5.0))
        def dr(k):
            v = fl(r[k]); em = fl(r.get(k + "_em")) or 0.0; ep = fl(r.get(k + "_ep")) or 0.0
            return np.concatenate([[v], split_normal(rng, v, em, ep, ndraw)])
        pa.append(dr("pmra")); pd_.append(dr("pmdec")); vl.append(dr("vlos_systemic"))
        ra.append(np.full(ndraw + 1, c[0])); dec.append(np.full(ndraw + 1, c[1]))
    sh = (len(rowsel), ndraw + 1)
    sc = coord.SkyCoord(ra=np.array(ra).ravel() * u.deg, dec=np.array(dec).ravel() * u.deg, distance=np.array(D).ravel() * u.kpc,
                        pm_ra_cosdec=np.array(pa).ravel() * u.mas / u.yr, pm_dec=np.array(pd_).ravel() * u.mas / u.yr,
                        radial_velocity=np.array(vl).ravel() * u.km / u.s).transform_to(coord.Galactocentric())
    x = np.stack([sc.x.to(u.m).value, sc.y.to(u.m).value, sc.z.to(u.m).value], -1).reshape(sh + (3,))
    v = np.stack([sc.v_x.to(u.m / u.s).value, sc.v_y.to(u.m / u.s).value, sc.v_z.to(u.m / u.s).value], -1).reshape(sh + (3,))
    return x, v
def turning(x, v, g, Phi):
    """vectorised turning points over the last axis set; x, v (..., 3). Returns r_now, r_p, r_a, L."""
    rn = np.linalg.norm(x, axis=-1); Lm = np.linalg.norm(np.cross(x, v), axis=-1)
    E = 0.5 * np.sum(v * v, -1) + np.interp(rn, RG, Phi)
    flat_rn, flat_L, flat_E = rn.ravel(), Lm.ravel(), E.ravel()
    rp = np.empty_like(flat_rn); ra = np.empty_like(flat_rn)
    for i in range(len(flat_rn)):
        F = 2 * (flat_E[i] - Phi) - flat_L[i] ** 2 / RG ** 2
        k = np.searchsorted(RG, flat_rn[i])
        neg = np.where(F[:k] < 0)[0]
        if len(neg) == 0: rp[i] = RG[0]
        else:
            j = neg[-1]; rp[i] = RG[j] + (RG[j + 1] - RG[j]) * (0 - F[j]) / (F[j + 1] - F[j])
        negu = np.where(F[k:] < 0)[0]
        if len(negu) == 0: ra[i] = RG[-1]
        else:
            j = k + negu[0]; ra[i] = RG[j - 1] + (RG[j] - RG[j - 1]) * (0 - F[j - 1]) / (F[j] - F[j - 1])
    return rn, rp.reshape(rn.shape), ra.reshape(rn.shape), Lm
def leapfrog(x, v, gfun, Gyr=5.0, n=200000):
    x = x.copy(); v = v.copy(); dt = -Gyr * 3.156e16 / n
    acc = lambda x: -gfun(np.linalg.norm(x)) * x / np.linalg.norm(x)
    a = acc(x); rmin = rmax = np.linalg.norm(x)
    for _ in range(n):
        v += 0.5 * dt * a; x += dt * v; a = acc(x); v += 0.5 * dt * a
        rr = np.linalg.norm(x); rmin = min(rmin, rr); rmax = max(rmax, rr)
    return rmin, rmax

P("\n--- orbits: PM-based pericentres in S1's own MW field (law mu = x/(1+x) on Hernquist 6e10; E_lo/E_hi bracket) ---")
RNG_O = np.random.default_rng(20261102)
PMNAMES = sorted(set(n for f in FOOTS for n in [r["name"] for r in SAMP[f]] + S839 + ["Draco"]
                     if n in LVDRAW and fl(LVDRAW[n].get("pmra")) is not None and fl(LVDRAW[n].get("pmdec")) is not None
                     and fl(LVDRAW[n].get("vlos_systemic")) is not None and LVDRAW[n]["_host"] in ("MW", "field")))
NDRAW_O = 300
XO, VO = galcen([LVDRAW[n] for n in PMNAMES], NDRAW_O, RNG_O)
ORB = {}
for f in FOOTS:
    a0 = A0[f]
    for ek in ("E_mid", "E_lo", "E_hi"):
        Mb = host_mass("MW", ek, a0)
        gfun = (lambda rr, Mb=Mb, a0=a0: g_host(np.asarray(rr, float), Mb, a0))
        g, Phi = field_tables(gfun)
        xs, vs = (XO, VO) if ek == "E_mid" else (XO[:, :1], VO[:, :1])
        rn, rp, ra, Lm = turning(xs, vs, g, Phi)
        for i, n in enumerate(PMNAMES):
            ORB[f"{f}|{ek}|{n}"] = dict(rn=rn[i] / KPC, rp=rp[i] / KPC, ra=ra[i] / KPC, L=Lm[i])
    P(f"   [{f}] {len(PMNAMES)} PM systems x ({NDRAW_O}+1 draws E_mid; central E_lo/E_hi) ({time.time() - T0:.0f} s)")
def tidal_den(f, ek, n, draw=0):
    """(Omega_p^2 - Phi''(r_p)) [s^-2] at the pericentre of the given draw."""
    o = ORB[f"{f}|{ek}|{n}"]; rp = o["rp"][draw] * KPC; L = o["L"][draw]
    Mb = host_mass("MW", ek, A0[f])
    dg = (g_host(rp * 1.001, Mb, A0[f]) - g_host(rp * 0.999, Mb, A0[f])) / (0.002 * rp)
    return (L / rp ** 2) ** 2 - dg

# ---- K4b / K5 / K6: orbit and King-radius controls
dr_i = PMNAMES.index("Draco")
gN839 = lambda rr: (lambda gN: gN / (-np.expm1(-np.sqrt(np.maximum(gN / A0["canonical"], 1e-15)))))(G * 6.0e10 * MSUN / np.asarray(rr, float) ** 2)
g839, Phi839 = field_tables(gN839)
_, rp839, ra839, _ = turning(XO[dr_i:dr_i + 1, :1], VO[dr_i:dr_i + 1, :1], g839, Phi839)
k4b = (abs(rp839[0, 0] / KPC / 53.4 - 1), abs(ra839[0, 0] / KPC / 120.0 - 1))
gmid = lambda rr: g_host(rr, host_mass("MW", "E_mid", A0["canonical"]), A0["canonical"])
lmin, lmax = leapfrog(XO[dr_i, 0], VO[dr_i, 0], gmid)
od = ORB[f"canonical|E_mid|Draco"]
k5 = (abs(lmin / KPC / od["rp"][0] - 1), abs(lmax / KPC / od["ra"][0] - 1))
check("K5", max(k5) <= 0.02, f"Draco S1-field r_p/r_a {od['rp'][0]:.1f}/{od['ra'][0]:.1f} vs leapfrog {lmin / KPC:.1f}/{lmax / KPC:.1f} (max rel {max(k5):.4f})",
      "<= 0.02", "turning points vs a direct 5-Gyr leapfrog in S1's MW field")
Mpt, mpt, rpt = 1e11, 1e6, 50 * KPC
Om2 = G * Mpt * MSUN / rpt ** 3; ddg = -2 * G * Mpt * MSUN / rpt ** 3
rt_k = (G * mpt * MSUN / (Om2 - ddg)) ** (1 / 3); rt_ref = rpt * (mpt / (3 * Mpt)) ** (1 / 3)
check("K6", abs(rt_k / rt_ref - 1) <= 1e-3, f"rel {abs(rt_k / rt_ref - 1):.1e}", "<= 1e-3", "King radius, Newtonian point mass, circular orbit")

# ================================================================== VELOCITY GRADIENTS (Walker 2023 per-star, CFG51 members)
P("\n--- velocity gradients: Walker et al. 2023 per-star data, CFG51's member rule (read-only), >= 10 members ---")
COLS_RD = dict(RW.COLS, RAdeg=(234, 248, float), DEdeg=(250, 264, float))
def parse_rd(fn):
    import gzip
    rows = []
    for line in gzip.open(fn, "rt"):
        line = line.rstrip("\n"); r = {}
        for k, (a, b, t) in COLS_RD.items():
            s = line[a - 1:b].strip()
            r[k] = s if t is str else ((float("nan") if t is float else -1) if s == "" else t(s))
        rows.append(r)
    return rows
WROWS = []
for fn in ("hectocat.dat.gz", "m2fshi.dat.gz", "m2fsmed.dat.gz"):
    WROWS += parse_rd(os.path.join(DATA, "walker2023", fn))
POS = {}
for r in WROWS:
    if r["Gaia"] and (r["Target"], r["Gaia"]) not in POS and np.isfinite(r["RAdeg"]):
        POS[(r["Target"], r["Gaia"])] = (r["RAdeg"], r["DEdeg"])
STARS = RW.build_stars(WROWS)
LVDKEY = {}
for r in csv.DictReader(open(os.path.join(DATA, "dsph", "lvd_dwarf_mw.csv"))):
    LVDKEY[r["key"]] = r
def m2l_grad(v, e, X, sig):
    w = 1.0 / (sig * sig + e * e)
    A = X * np.sqrt(w)[:, None]; b = v * np.sqrt(w)
    beta = np.linalg.lstsq(A, b, rcond=None)[0]
    res = v - X @ beta
    return float(np.sum(np.log(1 / w) + w * res * res)), beta
def prof(v, e, X):
    fun = lambda s: m2l_grad(v, e, X, s)[0]
    top = max(4 * np.std(v), 30.0)
    grid = np.linspace(0, top, 400); vals = [fun(s) for s in grid]; i = int(np.argmin(vals))
    lo, hi = grid[max(i - 1, 0)], grid[min(i + 1, len(grid) - 1)]
    rr = minimize_scalar(fun, bounds=(lo, hi), method="bounded")
    best = min(rr.fun, vals[i])
    return best, m2l_grad(v, e, X, rr.x if rr.fun <= vals[i] else grid[i])[1]
def grad_test(v, e, xi, eta):
    X1 = np.column_stack([np.ones_like(v), xi, eta]); X0 = X1[:, :1]
    l1, b1 = prof(v, e, X1); l0, _ = prof(v, e, X0)
    D = max(l0 - l1, 0.0)
    return D, float(chi2dist.sf(D, 2)), b1
GRAD = {}
targets = sorted(set(s["target"] for s in STARS.values()))
for tg in targets:
    lv = LVDKEY.get(tg.lower())
    if lv is None or lv["name"] not in [r["name"] for r in SAMP["alt"]]:
        continue
    st = {k: s for k, s in STARS.items() if s["target"] == tg}
    mem, _, vc, _ = RW.membership(st, lv)
    mem = [s for s in mem if not (s["dof"] > 0 and s["p"] < 0.01)]        # CFG51 'clean': drop chi2-variable stars
    n = len(mem)
    if n < 10:
        GRAD[lv["name"]] = dict(n=n, testable=False); continue
    ra0, de0, Dk = float(lv["ra"]), float(lv["dec"]), float(lv["distance"])
    rd = np.array([POS[(s["target"], s["gaia"])] for s in mem])
    xi = (rd[:, 0] - ra0) * math.cos(math.radians(de0)) * math.pi / 180 * Dk; eta = (rd[:, 1] - de0) * math.pi / 180 * Dk
    v = np.array([s["vm"] for s in mem]); e = np.array([s["em"] for s in mem])
    D, p, b1 = grad_test(v, e, xi, eta)
    GRAD[lv["name"]] = dict(n=n, testable=True, D=D, p=p, k_kms_per_kpc=float(math.hypot(b1[1], b1[2])), flag=bool(p < GRAD_P),
                            rms_xi_kpc=float(np.sqrt(np.mean(xi ** 2 + eta ** 2))), _v=v.tolist(), _e=e.tolist(), _xi=xi.tolist(), _eta=eta.tolist())
    P(f"   {lv['name']:18s} N {n:3d}  |grad| {GRAD[lv['name']]['k_kms_per_kpc']:6.1f} km/s/kpc  -2dlnL {D:6.2f}  p {p:.3f}  -> {'FLAG' if p < GRAD_P else 'no gradient'}")
P("   (systems of S_E3 not listed have no per-star data on disk or < 10 members: not certifiable, not flagged)")
# K7: power and false-flag control on the largest member set
big = max([k for k, v in GRAD.items() if v.get("testable")], key=lambda k: GRAD[k]["n"])
gb = GRAD[big]; vv, ee, xx, yy = (np.array(gb[k]) for k in ("_v", "_e", "_xi", "_eta"))
rng7 = np.random.default_rng(7)
ang = rng7.uniform(0, 2 * math.pi)
_, p_inj, _ = grad_test(vv + 10.0 * (xx * math.cos(ang) + yy * math.sin(ang)), ee, xx, yy)
nf = 0
for _ in range(200):
    pm = rng7.permutation(len(vv)); _, ps, _ = grad_test(vv[pm], ee[pm], xx, yy); nf += ps < GRAD_P
check("K7", p_inj < GRAD_P and nf / 200 <= 0.03, f"{big} (N {gb['n']}, rms radius {gb['rms_xi_kpc']:.3f} kpc): injected 10 km/s/kpc p {p_inj:.3g}; shuffled false-flag rate {nf / 200:.3f}",
      "p < 0.01 and <= 0.03", "velocity-gradient test power and size")
for k in GRAD:
    for kk in ("_v", "_e", "_xi", "_eta"):
        GRAD[k].pop(kk, None)
R["gradients"] = GRAD

# ================================================================== MEMBER COUNTS N_q
COLL = {}
for line in open(os.path.join(DATA, "dsph", "collins2013_m31_dsph.tsv")):
    if line.startswith("#") or not line.strip(): continue
    p_ = line.rstrip("\n").split("\t")
    if len(p_) > 4 and p_[1].strip().startswith("And"):
        try: COLL["Andromeda " + p_[1].strip()[4:].strip()] = int(p_[4])
        except ValueError: pass
COLL["Cassiopeia II"] = COLL.get("Andromeda XXX")
def ref_key(s):
    s = s.replace("+", "").replace(" ", "")
    i = 0
    while i < len(s) and s[i].isalpha(): i += 1
    return (s[:i].lower(), s[i:i + 4])
def Nq_of(r):
    ref = r["ref"]
    if ref.startswith("Geha2026"):
        if r["name"] in GEHN: return GEHN[r["name"]], "Geha II"
        if r["name"] in GEH2: return int(GEH2[r["name"]]["N_stars"]), "Geha II"
        return 9, "Geha-cited, absent from Geha II (< 10 by its rule)"
    if ref.startswith("Collins2013") and COLL.get(r["name"]):
        return COLL[r["name"]], "Collins 2013"
    for a in ARR:
        if a["lvd_name"] == r["name"] and ref_key(a["ref"]) == (ref_key(ref)[0], ref_key(ref)[1]):
            return int(a["N_stars"]), "Arroyo-Polonio (same dataset)"
    ds = 0.5 * (r["sem"] + r["sep"])
    return 0.5 * (r["sigma"] / ds) ** 2, "N_eff proxy"

# ================================================================== per-system attribute table
def attrs(f):
    a0 = A0[f]; out = {}
    for r in SAMP[f]:
        n = r["name"]; d = dict(host=r["host"], MV=r["MV"], logms=r["logms"], rh=r["rh"])
        d["ell"] = r["ell"] if r["ell"] is not None else (r["ell_ul"] if r["ell_ul"] is not None else float("nan"))
        d["ell_flag"] = bool(r["ell"] is not None and r["ell"] >= E_FLAG) or bool(r["ell"] is None and r["ell_ul"] is not None and r["ell_ul"] >= E_FLAG)
        g = GRAD.get(n, {}); d["grad_testable"] = bool(g.get("testable")); d["grad_flag"] = bool(g.get("flag", False))
        d["Nq"], d["Nq_src"] = Nq_of(r); d["dsig_frac"] = 0.5 * (r["sem"] + r["sep"]) / r["sigma"]
        d["ufd"] = bool(r["MV"] is not None and r["MV"] > -7.7)
        d["binary_specific"] = n in arr_free
        d["x_e"] = TAB[f"{f}|{n}"]["xe"]; d["D_host"] = r["dhost"] if r["dhost"] else r["dist"]
        d["y0"] = y0_of(r, a0); d["Lam"] = LFLOOR[f] / r["rh"]
        d["lb0"] = lb_central(r); d["sig_obs"] = r["sigma"] * arr_free.get(n, med_free)
        r12 = R12 * r["rh"] * PC; Ms = 10 ** r["logms"]
        d["r12_pc"] = R12 * r["rh"]
        for F in FLAV + ("V3S0",):
            d[f"logG_{F}"] = cen(f, n, F)
        gint_iso = 10 ** d["logG_ISO"] * G * (Ms / 2) * MSUN / r12 ** 2
        Rh = d["D_host"] * KPC; Mb = host_mass(r["host"], "E_mid", a0)
        dgdD = abs(g_host(Rh * 1.001, Mb, a0) - g_host(Rh * 0.999, Mb, a0)) / (0.002 * Rh)
        d["logT_now"] = math.log10(dgdD * r12 / gint_iso)
        d["pm"] = f"{f}|E_mid|{n}" in ORB
        for F in FLAV:
            m = Ms * 10 ** d[f"logG_{F}"] / FW_N
            d[f"logrho_int_{F}"] = math.log10(m / d["r12_pc"] ** 3)
            if d["pm"]:
                den = tidal_den(f, "E_mid", n, 0)
                rt = (G * m * MSUN / den) ** (1 / 3)
                d[f"q_{F}"] = r12 / rt
                dens = np.array([tidal_den(f, "E_mid", n, k) for k in range(1, NDRAW_O + 1)])
                qd = r12 / (G * m * MSUN / dens) ** (1 / 3)
                d[f"q_{F}_p16_p84"] = [float(np.percentile(qd, 16)), float(np.percentile(qd, 84))]
                d[f"q_{F}_bracket_lo_hi"] = [float(r12 / (G * m * MSUN / tidal_den(f, ek, n, 0)) ** (1 / 3)) for ek in ("E_lo", "E_hi")]
            else:   # no PM: present-distance circular lower bound (Omega^2 = g/r)
                Mb = host_mass(r["host"], "E_mid", a0); gg = g_host(Rh, Mb, a0)
                dg = (g_host(Rh * 1.001, Mb, a0) - g_host(Rh * 0.999, Mb, a0)) / (0.002 * Rh)
                d[f"q_{F}"] = None
                d[f"q_{F}_now_lowerbound"] = float(r12 / (G * m * MSUN / (gg / Rh - dg)) ** (1 / 3))
        if d["pm"]:
            o = ORB[f"{f}|E_mid|{n}"]
            d["r_peri_kpc"] = float(o["rp"][0]); d["r_apo_kpc"] = float(o["ra"][0])
            d["r_peri_p16_p84"] = [float(np.percentile(o["rp"][1:], 16)), float(np.percentile(o["rp"][1:], 84))]
            d["logrho_tid"] = math.log10(tidal_den(f, "E_mid", n, 0) / (G * MSUN / PC ** 3))
            Mbm = host_mass("MW", "E_mid", a0); rp = o["rp"][0] * KPC
            dgp = abs(g_host(rp * 1.001, Mbm, a0) - g_host(rp * 0.999, Mbm, a0)) / (0.002 * rp)
            d["logT_peri"] = math.log10(dgp * r12 / gint_iso)
        out[n] = d
    return out
ATT = {f: attrs(f) for f in FOOTS}
P(f"   attributes built ({time.time() - T0:.0f} s)")

# ================================================================== datasets, residual draws
RNG = np.random.default_rng(20261101)
DATASETS = {}
for f in FOOTS:
    DATASETS[(f, "primary")] = build(SAMP[f], A0[f], RNG)
    DATASETS[(f, "W")] = build(SAMP[f], A0[f], RNG, ups=4.0, binmode="f07", sig_src="lower", drop_ul=True)
if MUT:   # pure tidal artefact: lb = V3S + log10 q_V3S + N(0, 0.1); q at present distance where no pericentre
    rngm = np.random.default_rng(2)
    for f in FOOTS:
        for ds in ("primary", "W"):
            X = DATASETS[(f, ds)]; pv = pred_draws(f, X, "V3S")
            for i, r in enumerate(X["rows"]):
                a = ATT[f][r["name"]]; q = a["q_V3S"] if a["q_V3S"] is not None else a["q_V3S_now_lowerbound"]
                X["lb"][i] = pv[i] + math.log10(q) + rngm.normal(0, 0.1, NMC)
        for n, a in ATT[f].items():
            q = a["q_V3S"] if a["q_V3S"] is not None else a["q_V3S_now_lowerbound"]
            a["lb0"] = a["logG_V3S"] + math.log10(q) + rngm.normal(0, 0.1)
RES = {}
for f in FOOTS:
    for ds in ("primary", "W"):
        X = DATASETS[(f, ds)]
        for F in FLAV + ("V3S0",):
            RES[(f, ds, F)] = X["lb"] - pred_draws(f, X, F)
def boot_ix(N, rng):
    return rng.integers(0, N, (NBOOT, N)), rng.integers(0, NMC, (NBOOT, N))
def bmed(D, idx_sys, rng):
    idx_sys = np.asarray(idx_sys)
    if len(idx_sys) == 0: return float("nan"), float("nan")
    i, c = boot_ix(len(idx_sys), rng)
    meds = np.median(D[idx_sys[i], c], axis=1)
    return float(np.median(meds)), float(np.std(meds))

# ---- K1 / K2 reproduction
P("\n--- K1/K2: E3 and S1 reproduced with this lane's own code ---")
ST_s = np.array([0.01, 0.1, 0.3, 1, 3, 10, 100, 1000]); ST_S = np.array([0.0050, 0.048, 0.134, 0.358, 0.663, 0.894, 0.990, 0.998999])
def nu1(y):
    y = np.maximum(np.asarray(y, float), 1e-30); return 0.5 * (1.0 + np.sqrt(1.0 + 4.0 / y))
E3REF = {"canonical": dict(EN=2.013, law=0.557), "alt": dict(EN=1.998, law=0.508)}
S1REF = {"canonical": dict(V3S=1.331, MOND=1.130, ISO=0.553), "alt": dict(V3S=1.299, MOND=1.075, ISO=0.502)}
k1, k2, REPRO = [], [], {}
rngk = np.random.default_rng(11)
for f in FOOTS:
    X = DATASETS[(f, "primary")]; N = len(X["rows"]); allix = np.arange(N)
    EN = bmed(X["lb"], allix, rngk)[0]
    ms = 10 ** (X["ly"]) * (10 ** X["la"] * PC) ** 2 * A0[f] / G / MSUN; r12 = R12 * 10 ** X["la"] * PC
    law = bmed(X["lb"] - np.log10(nu1(G * (ms / 2) * MSUN / r12 ** 2 / A0[f])), allix, rngk)[0]
    k1 += [abs(EN - E3REF[f]["EN"]), abs(law - E3REF[f]["law"])]
    vals = {F: bmed(RES[(f, "primary", F)], allix, rngk) for F in FLAV}
    for F in ("V3S", "MOND", "ISO"):
        k2.append(abs(vals[F][0] - S1REF[f][F]))
    REPRO[f] = dict(E_N=EN, law=law, N=N, **{F: list(vals[F]) for F in FLAV})
    P(f"   [{f}] N {N}: Newton E_N {EN:+.3f}, unscreened law {law:+.3f} | V3S {vals['V3S'][0]:+.3f}+-{vals['V3S'][1]:.3f}, "
      f"MOND {vals['MOND'][0]:+.3f}, ISO {vals['ISO'][0]:+.3f}, V3D {vals['V3D'][0]:+.3f}+-{vals['V3D'][1]:.3f}")
check("K1", (len(SAMP["canonical"]), len(SAMP["alt"])) == (45, 46) and max(k1) <= 0.02, f"N {len(SAMP['canonical'])}/{len(SAMP['alt'])}; max |diff| {max(k1):.3f}",
      "45/46 and <= 0.02", "E3: Newton E_N and the unscreened law")
s1csv = list(csv.DictReader(open(os.path.join(REPO, "rebuild_2026_10_22", "S1_v3_hosted_small", "s1_per_system.csv"))))
u1csv = list(csv.DictReader(open(os.path.join(REPO, "rebuild_2026_10_22", "U1_v3_dust_content", "u1_satellites_per_system.csv"))))
dper, du1 = 0.0, 0.0
for row in s1csv:
    a = ATT[row["footing"]][row["name"]]
    dper = max(dper, abs(a["logG_ISO"] - float(row["logG_iso0"])), abs(a["logG_MOND"] - float(row["logG_emb0"])),
               abs(a["logG_V3S"] - float(row["logG_v3_Lfloor"])), abs(float(row["log_gobs_gbar"]) - (a["lb0"] if not MUT else float(row["log_gobs_gbar"]))))
for row in u1csv:
    a = ATT[row["footing"]][row["name"]]
    du1 = max(du1, abs((a["lb0"] - LFW) - float(row["Delta_B0"])))
check("K2", max(k2) <= 0.02 and dper <= 0.01 and du1 <= 0.005, f"S1 chain max |diff| {max(k2):.3f}; per-system logG {dper:.1e}; V3D vs U1 B0 {du1:.1e}",
      "<= 0.02 / 0.01 / 0.005", "S1's S2/S3/S4 medians, S1 per-system central logG, U1 Delta_B0")
R["reproduction"] = REPRO

# ================================================================== regression helpers
def ols(x, r):
    x = np.asarray(x, float); r = np.asarray(r, float); xm = x - x.mean()
    return float(np.sum(xm * (r - r.mean())) / np.sum(xm * xm))
def ols_multi(Xc, r):
    A = np.column_stack([np.ones(len(r))] + [np.asarray(c, float) for c in Xc])
    return np.linalg.lstsq(A, np.asarray(r, float), rcond=None)[0][1:]
def boot_coef(Xc, r, seed=20261024, nb=4000):
    r = np.asarray(r, float); n = len(r); idx = np.random.default_rng(seed).integers(0, n, (nb, n))
    Xc = [np.asarray(c, float) for c in Xc]
    out = []
    for ii in idx:
        try: out.append(ols_multi([c[ii] for c in Xc], r[ii]))
        except Exception: pass
    out = np.array(out)
    return ols_multi(Xc, r), np.nanstd(out, axis=0)
def spear(x, r, sign=+1, nperm=10000, seed=838):
    x = np.asarray(x, float); r = np.asarray(r, float)
    rho = float(spearmanr(r, sign * x)[0])
    rng = np.random.default_rng(seed); cnt = 0
    for _ in range(nperm):
        cnt += spearmanr(r, sign * rng.permutation(x))[0] >= rho
    return rho, (cnt + 1) / (nperm + 1)

# ================================================================== TASK 1: reconciliation grid
P("\n" + "=" * 112)
P("TASK 1: T1's host-field tracking vs CFG838/839 (factor grid; slope sign: + = residual rises with x_e / T, falls with D)")
P("=" * 112)
k3 = []
J_T1 = json.load(open(os.path.join(REPO, "rebuild_2026_10_22", "T1_efe_strength", "t1_efe_strength_results.json")))
T1REF = {"canonical": (0.7607, 0.7792), "alt": (0.8382, 0.8526)}
for f in FOOTS:
    A = ATT[f]; names = [r["name"] for r in SAMP[f]]
    lx = np.array([math.log10(A[n]["x_e"]) for n in names]); ly = np.array([math.log10(A[n]["y0"]) for n in names])
    res = np.array([A[n]["lb0"] - A[n]["logG_V3S0"] for n in names])
    b = ols(lx, res); bp = ols_multi([lx, ly], res)[0]
    k3 += [abs(b - T1REF[f][0]), abs(bp - T1REF[f][1])]
    P(f"   [{f}] T1 tracking slope at eps = 0: {b:+.4f} (T1 {T1REF[f][0]:+.4f}); A3 partial with log y0 {bp:+.4f} (T1 {T1REF[f][1]:+.4f})")
check("K3", max(k3) <= 0.02, f"max |diff| {max(k3):.4f}", "<= 0.02", "T1 tracking slope (eps 0) and A3 partial slope")
r838 = [J838["rows"][n] for n in S838]
rho_T = float(spearmanr([x["delta"] for x in r838], [x["logT"] for x in r838])[0]); rho_D = float(spearmanr([x["delta"] for x in r838], [x["D"] for x in r838])[0])
r839 = [J839["rows"][n] for n in S839]; rho_Tp = float(spearmanr([x["delta"] for x in r839], [x["logTp"] for x in r839])[0])
check("K4", abs(rho_T - (-0.00)) <= 0.01 and abs(rho_D - (-0.02)) <= 0.01 and abs(rho_Tp - 0.08) <= 0.01 and max(k4b) <= 0.02,
      f"rho(D,logT) {rho_T:+.3f}, rho(D,D) {rho_D:+.3f}, rho(D,logTp) {rho_Tp:+.3f}; Draco in CFG839's field r_p/r_a {rp839[0, 0] / KPC:.1f}/{ra839[0, 0] / KPC:.1f}",
      "|diff| <= 0.01; 2 %", "CFG838/839 statistics from their rows; own orbit code in CFG839's field")

# per-system reconciliation table (both samples, E3 data conventions)
def recon_rows(f):
    a0 = A0[f]; out = {}
    names = sorted(set([r["name"] for r in SAMP[f]]) | set(n for n in S838 if n in BYNAME))
    for n in names:
        r = BYNAME[n]
        if n in ATT[f]:
            a = ATT[f][n]; d = dict(lb0=a["lb0"], x_e=a["x_e"], D=a["D_host"], logT_now=a["logT_now"], logT_peri=a.get("logT_peri"),
                                    MV=r["MV"], host=r["host"], y0=a["y0"], Lam=a["Lam"])
        else:
            Ms = 10 ** r["logms"]; r12 = R12 * r["rh"] * PC
            Dh = r["dhost"] if r["dhost"] else r["dist"]; Rh = Dh * KPC; Mb = host_mass(r["host"], "E_mid", a0)
            gint = 10 ** cen(f, n, "ISO") * G * (Ms / 2) * MSUN / r12 ** 2
            dgdD = abs(g_host(Rh * 1.001, Mb, a0) - g_host(Rh * 0.999, Mb, a0)) / (0.002 * Rh)
            lTp = None
            if f"{f}|E_mid|{n}" in ORB:
                rp = ORB[f"{f}|E_mid|{n}"]["rp"][0] * KPC; Mbm = host_mass("MW", "E_mid", a0)
                lTp = math.log10(abs(g_host(rp * 1.001, Mbm, a0) - g_host(rp * 0.999, Mbm, a0)) / (0.002 * rp) * r12 / gint)
            d = dict(lb0=lb_central(r), x_e=TAB[f"{f}|{n}"]["xe"], D=Dh, logT_now=math.log10(dgdD * r12 / gint), logT_peri=lTp,
                     MV=r["MV"], host=r["host"], y0=y0_of(r, a0), Lam=LFLOOR[f] / r["rh"])
            if MUT: d["lb0"] = cen(f, n, "V3S") + 0.3 * d["logT_now"]
        for F in ("V3S0", "V3S", "ISO"):
            d[f"R_{F}"] = d["lb0"] - cen(f, n, F)
        d["R_N"] = d["lb0"] - LFW
        d["R_828"] = R828.get(n)
        out[n] = d
    return out
REC = {f: recon_rows(f) for f in FOOTS}
VARS = {"log x_e": (lambda d: math.log10(d["x_e"]), +1), "log D": (lambda d: math.log10(d["D"]), -1),
        "log T_now": (lambda d: d["logT_now"], +1), "log T_peri": (lambda d: d["logT_peri"], +1)}
SAMPLES = lambda f: {"S_E3": [r["name"] for r in SAMP[f]], "S_838": [n for n in S838 if n in REC[f]],
                     "S_839": [n for n in S839 if n in REC[f]], "S_ovl": [n for n in S838 if n in ATT[f]],
                     "S_E3+S_838": sorted(set([r["name"] for r in SAMP[f]]) | set(n for n in S838 if n in REC[f]))}
GRID = {}
for f in FOOTS:
    for sname, names in SAMPLES(f).items():
        for res in ("R_V3S0", "R_V3S", "R_ISO", "R_N", "R_828"):
            for vname, (fun, sg) in VARS.items():
                rows = [REC[f][n] for n in names if REC[f][n].get(res) is not None and (vname != "log T_peri" or REC[f][n]["logT_peri"] is not None)]
                if len(rows) < 5: continue
                x = np.array([fun(d) for d in rows]); r_ = np.array([d[res] for d in rows])
                b, sd = boot_coef([sg * x], r_); rho, p = spear(x, r_, sg, nperm=2000)
                GRID[f"{f}|{sname}|{res}|{vname}"] = dict(N=len(rows), b=float(b[0]), sd=float(sd[0]), z=float(b[0] / sd[0]), rho=rho, p=p)
P(f"\n   factor grid (OLS slope +- bootstrap sd, z; one-sided Spearman rho, permutation p)  [{time.time() - T0:.0f} s]")
for f in FOOTS:
    P(f"   [{f}]")
    for k, v in GRID.items():
        if not k.startswith(f + "|"): continue
        _, sname, res, vname = k.split("|")
        if res == "R_V3S" and sname not in ("S_E3",): continue
        P(f"     {sname:11s} {res:7s} {vname:10s} N {v['N']:2d}: b {v['b']:+.3f} +- {v['sd']:.3f} (z {v['z']:+.1f}) | rho {v['rho']:+.2f} p {v['p']:.3f}")
def strong(v): return v["z"] >= 2 or v["p"] < 0.05
def weak(v): return abs(v["z"]) < 1 and v["p"] > 0.2
ATTR = {}
for f in FOOTS:
    base = GRID[f"{f}|S_E3|R_V3S0|log x_e"]
    swaps = {"sample -> S_838": GRID.get(f"{f}|S_838|R_V3S0|log x_e"), "sample -> S_ovl": GRID.get(f"{f}|S_ovl|R_V3S0|log x_e"),
             "residual -> R_N": GRID.get(f"{f}|S_E3|R_N|log x_e"), "residual -> R_ISO": GRID.get(f"{f}|S_E3|R_ISO|log x_e"),
             "variable -> log D": GRID.get(f"{f}|S_E3|R_V3S0|log D"), "variable -> log T_now": GRID.get(f"{f}|S_E3|R_V3S0|log T_now"),
             "variable -> log T_peri": GRID.get(f"{f}|S_E3|R_V3S0|log T_peri")}
    cause = [k for k, v in swaps.items() if v is not None and strong(base) and (abs(v["z"]) < 1 or v["p"] > 0.2)]
    # statistic swap: Spearman on the base cell
    if strong(base) and base["p"] > 0.2: cause.append("statistic -> Spearman")
    ATTR[f] = dict(base=base, swaps=swaps, causes=cause, reading=(", ".join(cause) if cause else "COMBINED (no single swap removes it)"))
    P(f"   [{f}] T1 cell z {base['z']:+.1f}, p {base['p']:.4f}. Single swaps that remove the trend (z < 1 or p > 0.2): {ATTR[f]['reading']}")
R["task1"] = dict(grid=GRID, attribution=ATTR, rows={f: REC[f] for f in FOOTS})

# ---- V3: is T1's trend real? (S_E3, R_V3S0 vs log x_e)
P("\n--- V3: is T1's host-field trend real? (S_E3, R_V3S0 vs log x_e; also R_V3S, R_ISO, R_N, MOND) ---")
V3 = {}
for f in FOOTS:
    A = ATT[f]; names = [r["name"] for r in SAMP[f]]
    lx = np.array([math.log10(A[n]["x_e"]) for n in names])
    cov = {"log y0": np.array([math.log10(A[n]["y0"]) for n in names]), "log Lambda": np.array([math.log10(A[n]["Lam"]) for n in names]),
           "M_V": np.array([A[n]["MV"] for n in names]), "log sigma": np.array([math.log10(A[n]["sig_obs"]) for n in names]),
           "binary-specific": np.array([1.0 if A[n]["binary_specific"] else 0.0 for n in names]),
           "M31": np.array([1.0 if A[n]["host"] == "M31" else 0.0 for n in names])}
    mw = np.array([A[n]["host"] == "MW" for n in names])
    V3[f] = {}
    for res in ("V3S0", "V3S", "ISO", "MOND", "V3D"):
        r_ = np.array([A[n]["lb0"] - A[n][f"logG_{res}"] for n in names])
        b0, s0 = boot_coef([lx], r_)
        bc, sc = boot_coef([lx, cov["log y0"], cov["log Lambda"]], r_)
        rho_mw, p_mw = spear(lx[mw], r_[mw], +1, nperm=5000)
        rho_all, p_all = spear(lx, r_, +1, nperm=5000)
        jk = [ols(np.delete(lx, i), np.delete(r_, i)) for i in range(len(r_))]
        jkz = []
        ts = float(theilslopes(r_, lx)[0])
        prox = {}
        for cn, cv in cov.items():
            bb, ss = boot_coef([lx, cv], r_)
            prox[cn] = dict(b_xe=float(bb[0]), sd_xe=float(ss[0]), b_cov=float(bb[1]), sd_cov=float(ss[1]))
        tracks = (bc[0] / sc[0] >= 2) and (p_mw < 0.05) and (min(jk) > 0) and (ts > 0)
        proxy = [cn for cn, v in prox.items() if v["b_xe"] / v["sd_xe"] < 1 and abs(v["b_cov"] / v["sd_cov"]) >= 2]
        # jackknife z: drop-one slope with bootstrap sd of the base
        drop_kill = [names[i] for i in range(len(r_)) if jk[i] / s0[0] < 1]
        notrob = (p_all > 0.05) or bool(drop_kill)
        cls = "TRACKS HOST FIELD" if tracks else ("PROXY (" + ", ".join(proxy) + ")" if proxy else ("NOT ROBUST" if notrob else "UNDECIDED"))
        V3[f][res] = dict(b=float(b0[0]), sd=float(s0[0]), b_ctrl=float(bc[0]), sd_ctrl=float(sc[0]), rho_all=rho_all, p_all=p_all,
                          rho_MW=rho_mw, p_MW=p_mw, N_MW=int(mw.sum()), jk_min=float(min(jk)), jk_max=float(max(jk)),
                          jk_min_drop=names[int(np.argmin(jk))], drop_kill=drop_kill, theil_sen=ts, proxy=prox, cls=cls)
        P(f"   [{f}] {res:5s} b {b0[0]:+.3f}+-{s0[0]:.3f} | +y0,Lambda {bc[0]:+.3f}+-{sc[0]:.3f} | rho all {rho_all:+.2f} (p {p_all:.3f}), MW {rho_mw:+.2f} (p {p_mw:.3f}, N {mw.sum()}) "
          f"| jk [{min(jk):+.2f}, {max(jk):+.2f}] (min drops {names[int(np.argmin(jk))]}) | TS {ts:+.2f} -> {cls}")
        if res == "V3S0":
            for cn, v in prox.items():
                P(f"        + {cn:16s}: b_xe {v['b_xe']:+.3f}+-{v['sd_xe']:.3f} | b_cov {v['b_cov']:+.3f}+-{v['sd_cov']:.3f}")
    # permutation control (frozen): host fields shuffled among systems must not class TRACKS HOST FIELD
    lxp = np.random.default_rng(2).permutation(lx); r_ = np.array([A[n]["lb0"] - A[n]["logG_V3S0"] for n in names])
    bcp, scp = boot_coef([lxp, cov["log y0"], cov["log Lambda"]], r_); rmp, pmp = spear(lxp[mw], r_[mw], +1, nperm=5000)
    jkp = [ols(np.delete(lxp, i), np.delete(r_, i)) for i in range(len(r_))]
    trp = (bcp[0] / scp[0] >= 2) and (pmp < 0.05) and (min(jkp) > 0) and (float(theilslopes(r_, lxp)[0]) > 0)
    V3[f]["perm_control"] = dict(b_ctrl=float(bcp[0]), sd_ctrl=float(scp[0]), p_MW=pmp, tracks=bool(trp))
    P(f"   [{f}] permutation control (x_e shuffled, seed 2): partial {bcp[0]:+.3f}+-{scp[0]:.3f}, MW p {pmp:.3f} -> {'TRACKS (control FAILS)' if trp else 'does not track (control OK)'}")
R["V3_trend"] = V3

# ================================================================== TASK 2: systematics tests and the clean subset
P("\n" + "=" * 112)
P("TASK 2: physical systematics on S_E3 (primary data; bootstrap median of per-draw residuals; W beside the clean subset)")
P("=" * 112)
rngb = np.random.default_rng(20261103)
def split(f, F, mask, ds="primary"):
    D = RES[(f, ds, F)]; idx = np.arange(D.shape[0])
    a = bmed(D, idx[mask], rngb); b = bmed(D, idx[~mask], rngb)
    return dict(N_in=int(mask.sum()), in_=a, N_out=int((~mask).sum()), out=b, diff=(a[0] - b[0], math.hypot(a[1], b[1])) if mask.sum() and (~mask).sum() else (float("nan"), float("nan")))
T2 = {}; CLEAN = {}
for f in FOOTS:
    A = ATT[f]; names = [r["name"] for r in DATASETS[(f, "primary")]["rows"]]
    arr = lambda key: np.array([A[n][key] for n in names])
    T2[f] = {}
    pm = arr("pm")
    ell_ok = ~arr("ell_flag"); grad_ok = ~arr("grad_flag"); nq_ok = np.array([A[n]["Nq"] >= NQ_MIN for n in names])
    for F in ("V3S", "V3D", "MOND", "ISO"):
        out = {}
        r_c = np.array([A[n]["lb0"] - A[n][f"logG_{F}"] for n in names])
        q = np.array([A[n][f"q_{F}"] if A[n][f"q_{F}"] is not None else np.nan for n in names])
        safe = pm & (q < Q_SAFE)
        # (a) tides
        out["a_split_q<0.5_among_PM"] = split(f, F, safe)
        sel = pm
        lq = np.log10(q[sel]); rr = r_c[sel]
        b, sd = boot_coef([lq], rr); rho, p = spear(lq, rr, +1, nperm=5000)
        lrt = np.array([A[n]["logrho_tid"] for n in np.array(names)[sel]]); lri = np.array([A[n][f"logrho_int_{F}"] for n in np.array(names)[sel]])
        bp, sp = boot_coef([lrt, lri], rr)
        out["a_q"] = dict(N_PM=int(sel.sum()), N_safe=int(safe.sum()), N_exposed=int(np.sum(pm & (q >= Q_EXP))), b_logq=float(b[0]), sd=float(sd[0]), rho=rho, p=p,
                          partial_logrho_tid=float(bp[0]), sd_partial=float(sp[0]), z_partial=float(bp[0] / sp[0]),
                          tides_implicated=bool(bp[0] / sp[0] >= 2), median_q=float(np.nanmedian(q[sel])))
        # (b) ellipticity / gradient
        out["b_split_ell<0.5"] = split(f, F, ell_ok)
        ev = arr("ell").astype(float); okv = np.isfinite(ev)
        rho_e, p_e = spear(ev[okv], r_c[okv], +1, nperm=5000); out["b_ell_rho"] = dict(rho=rho_e, p=p_e)
        out["b_grad_flags"] = {n: A[n]["grad_flag"] for n in names if A[n]["grad_testable"]}
        # (c) quality
        out["c_split_Nq>=10"] = split(f, F, nq_ok)
        lnq = np.log10(arr("Nq").astype(float)); rho_n, p_n = spear(lnq, r_c, -1, nperm=5000)
        rho_s, p_s = spear(arr("dsig_frac").astype(float), r_c, +1, nperm=5000)
        out["c_rho"] = dict(rho_logNq_neg=rho_n, p_logNq=p_n, rho_dsig=rho_s, p_dsig=p_s)
        out["c_split_binary_specific"] = split(f, F, arr("binary_specific"))
        # (d) UFD
        out["d_split_UFD"] = split(f, F, arr("ufd"))
        # (e) host distance / field
        lxe = np.log10(arr("x_e").astype(float)); lD = np.log10(arr("D_host").astype(float))
        bx, sx = boot_coef([lxe], r_c); bd, sdd = boot_coef([lD], r_c)
        out["e"] = dict(b_logxe=float(bx[0]), sd_logxe=float(sx[0]), rho_logxe=spear(lxe, r_c, +1, nperm=5000),
                        b_logD=float(bd[0]), sd_logD=float(sdd[0]), rho_logD_neg=spear(lD, r_c, -1, nperm=5000))
        out["e_split_MW"] = split(f, F, arr("host") == "MW")
        # clean subsets
        qV = np.array([A[n]["q_V3D"] if A[n]["q_V3D"] is not None else np.nan for n in names])
        base_ok = ell_ok & grad_ok & nq_ok
        masks = {"clean": safe & base_ok, "STRICT": pm & (qV < Q_SAFE) & base_ok, "C2-C4": base_ok}
        cl = {}
        allix = np.arange(len(names))
        Dall = bmed(RES[(f, "primary", F)], allix, rngb)
        for mk, m in masks.items():
            v = bmed(RES[(f, "primary", F)], allix[m], rngb) if m.sum() else (float("nan"), float("nan"))
            Wn = [r["name"] for r in DATASETS[(f, "W")]["rows"]]; mW = np.array([n in set(np.array(names)[m]) for n in Wn])
            vW = bmed(RES[(f, "W", F)], np.arange(len(Wn))[mW], rngb) if mW.sum() else (float("nan"), float("nan"))
            # f_sys with joint bootstrap
            D = RES[(f, "primary", F)]; Nn = len(names); ii = rngb.integers(0, Nn, (NBOOT, Nn)); cc = rngb.integers(0, NMC, (NBOOT, Nn))
            fs = []
            for k in range(NBOOT):
                vals = D[ii[k], cc[k]]; inm = m[ii[k]]
                if inm.sum() == 0: continue
                da = np.median(vals); dc = np.median(vals[inm]); fs.append(1 - dc / da)
            fs = np.array(fs)
            N_ = int(m.sum())
            if N_ < NCLEAN_MIN: c_ = "TOO FEW"
            elif v[0] >= 3 * v[1] and v[0] >= 0.5 * Dall[0]: c_ = "ROBUST"
            elif v[0] >= 2 * v[1]: c_ = "REDUCED"
            else: c_ = "NOT ROBUST"
            cl[mk] = dict(N=N_, names=list(np.array(names)[m]), Delta=v, Delta_W=vW, Delta_all=Dall,
                          f_sys=float(1 - v[0] / Dall[0]) if N_ else float("nan"),
                          f_sys_68=[float(np.percentile(fs, 16)), float(np.percentile(fs, 84))] if len(fs) else None,
                          f_sys_95=[float(np.percentile(fs, 2.5)), float(np.percentile(fs, 97.5))] if len(fs) else None, cls=c_)
        # per-test fractions
        ft = {}
        for tk, m in (("C1 q<0.5 (PM)", safe), ("C2 ell<0.5", ell_ok), ("C3 no gradient", grad_ok), ("C4 Nq>=10", nq_ok), ("UFD only", arr("ufd")), ("MW only", arr("host") == "MW")):
            v = bmed(RES[(f, "primary", F)], allix[m], rngb) if m.sum() else (float("nan"), float("nan"))
            ft[tk] = dict(N=int(m.sum()), Delta=v, f=float(1 - v[0] / Dall[0]) if m.sum() else float("nan"))
        out["clean"] = cl; out["per_test_fraction"] = ft
        T2[f][F] = out
        P(f"\n   [{f}] {F}: all N {len(names)} Delta {Dall[0]:+.3f}+-{Dall[1]:.3f}")
        a_ = out["a_q"]
        P(f"     (a) PM systems {a_['N_PM']}: median q {a_['median_q']:.2f}; safe (q<{Q_SAFE}) {a_['N_safe']}, exposed (q>={Q_EXP}) {a_['N_exposed']}; "
          f"b(log q) {a_['b_logq']:+.3f}+-{a_['sd']:.3f}, rho {a_['rho']:+.2f} p {a_['p']:.3f}; partial log rho_tid {a_['partial_logrho_tid']:+.3f}+-{a_['sd_partial']:.3f} "
          f"(z {a_['z_partial']:+.1f}) -> {'TIDES IMPLICATED' if a_['tides_implicated'] else 'not implicated'}")
        for key, lab in (("a_split_q<0.5_among_PM", "(a) q<0.5 (PM) vs rest"), ("b_split_ell<0.5", "(b) ell<0.5 vs >=0.5"), ("c_split_Nq>=10", "(c) Nq>=10 vs <10"),
                         ("c_split_binary_specific", "(c) binary-specific vs median"), ("d_split_UFD", "(d) UFD vs classical"), ("e_split_MW", "(e) MW vs M31/field")):
            s_ = out[key]
            P(f"     {lab:32s}: in N {s_['N_in']:2d} {s_['in_'][0]:+.3f}+-{s_['in_'][1]:.3f} | out N {s_['N_out']:2d} {s_['out'][0]:+.3f}+-{s_['out'][1]:.3f} | diff {s_['diff'][0]:+.3f}+-{s_['diff'][1]:.3f}")
        P(f"     (b) rho(ell) {out['b_ell_rho']['rho']:+.2f} p {out['b_ell_rho']['p']:.3f}; (c) rho(-log Nq) {out['c_rho']['rho_logNq_neg']:+.2f} p {out['c_rho']['p_logNq']:.3f}, "
          f"rho(dsig/sig) {out['c_rho']['rho_dsig']:+.2f} p {out['c_rho']['p_dsig']:.3f}")
        e_ = out["e"]
        P(f"     (e) b(log x_e) {e_['b_logxe']:+.3f}+-{e_['sd_logxe']:.3f} rho {e_['rho_logxe'][0]:+.2f} p {e_['rho_logxe'][1]:.3f}; b(log D) {e_['b_logD']:+.3f}+-{e_['sd_logD']:.3f} "
          f"rho(-) {e_['rho_logD_neg'][0]:+.2f} p {e_['rho_logD_neg'][1]:.3f}")
        for mk, c_ in cl.items():
            P(f"     subset {mk:7s} N {c_['N']:2d}: Delta {c_['Delta'][0]:+.3f}+-{c_['Delta'][1]:.3f}  (W {c_['Delta_W'][0]:+.3f}+-{c_['Delta_W'][1]:.3f}); "
              f"f_sys {c_['f_sys']:+.2f} 68% {np.round(c_['f_sys_68'], 2).tolist() if c_['f_sys_68'] else None} 95% {np.round(c_['f_sys_95'], 2).tolist() if c_['f_sys_95'] else None} -> {c_['cls']}")
            P(f"        {', '.join(c_['names'])}")
        P("     per-test fractions: " + "; ".join(f"{k} N {v['N']} f {v['f']:+.2f}" for k, v in ft.items()))
R["task2"] = T2

# ---- per-system CSV
rows_out = []
for f in FOOTS:
    for n, a in ATT[f].items():
        row = dict(footing=f, name=n, host=a["host"], M_V=a["MV"], ufd=a["ufd"], D_host_kpc=a["D_host"], x_e=a["x_e"], ell=a["ell"], ell_flag=a["ell_flag"],
                   grad_testable=a["grad_testable"], grad_flag=a["grad_flag"], N_q=a["Nq"], N_q_src=a["Nq_src"], dsig_frac=a["dsig_frac"],
                   binary_specific=a["binary_specific"], pm=a["pm"], r_peri_kpc=a.get("r_peri_kpc"), r_apo_kpc=a.get("r_apo_kpc"),
                   logT_now=a["logT_now"], logT_peri=a.get("logT_peri"), lb0=a["lb0"])
        for F in FLAV:
            row[f"Delta_{F}"] = a["lb0"] - a[f"logG_{F}"]
            row[f"q_{F}"] = a[f"q_{F}"] if a[f"q_{F}"] is not None else ""
            row[f"q_{F}_now_lb"] = a.get(f"q_{F}_now_lowerbound", "")
            row[f"q_{F}_p16"], row[f"q_{F}_p84"] = a.get(f"q_{F}_p16_p84", ["", ""])
            row[f"q_{F}_Elo"], row[f"q_{F}_Ehi"] = a.get(f"q_{F}_bracket_lo_hi", ["", ""])
        row["r_peri_p16"], row["r_peri_p84"] = a.get("r_peri_p16_p84", ["", ""])
        row["Delta_V3S0"] = a["lb0"] - a["logG_V3S0"]
        rows_out.append(row)
with open(os.path.join(HERE, f"z2_per_system{SFX}.csv"), "w", newline="") as fh:
    w = csv.DictWriter(fh, fieldnames=list(rows_out[0].keys())); w.writeheader(); [w.writerow(r) for r in rows_out]

# ================================================================== VERDICTS (frozen lines)
P("\n" + "=" * 112); P("VERDICTS (frozen lines)"); P("=" * 112)
VER = {}
for f in FOOTS:
    VER[f] = {F: dict(V1=T2[f][F]["clean"]["clean"]["cls"], Delta_clean=T2[f][F]["clean"]["clean"]["Delta"], Delta_all=T2[f][F]["clean"]["clean"]["Delta_all"],
                      f_sys=T2[f][F]["clean"]["clean"]["f_sys"], f_sys_68=T2[f][F]["clean"]["clean"]["f_sys_68"], f_sys_95=T2[f][F]["clean"]["clean"]["f_sys_95"],
                      tides=T2[f][F]["a_q"]["tides_implicated"], strict=T2[f][F]["clean"]["STRICT"]["cls"], c2c4=T2[f][F]["clean"]["C2-C4"]["cls"])
              for F in ("V3S", "V3D", "MOND", "ISO")}
    VER[f]["V3_T1_trend"] = V3[f]["V3S0"]["cls"]
    for F in ("V3S", "V3D", "MOND", "ISO"):
        v = VER[f][F]
        P(f"   [{f}] {F:4s} V1 {v['V1']:10s} clean {v['Delta_clean'][0]:+.3f}+-{v['Delta_clean'][1]:.3f} vs all {v['Delta_all'][0]:+.3f}; "
          f"f_sys {v['f_sys']:+.2f} 68% {np.round(v['f_sys_68'], 2).tolist() if v['f_sys_68'] else None}; tides {'IMPLICATED' if v['tides'] else 'not implicated'}; "
          f"STRICT {v['strict']}; C2-C4 {v['c2c4']}")
    P(f"   [{f}] V3 T1's host-field trend: {VER[f]['V3_T1_trend']}")
R["verdicts"] = VER
if MUT:
    okm = all(VER[f]["V3S"]["tides"] for f in FOOTS)
    P(f"\n   MUTATE expectations: K1-K3 FAIL; TIDES IMPLICATED for V3S on both footings: {okm}")
    R["mutate_tides_fired"] = okm

# ================================================================== A1 (POST-RESULT, reported only; no frozen line or check changed)
P("\n--- A1 post-result diagnostics (reported only; see AMENDMENT_A1.md) ---")
A1 = {}
for f in FOOTS:
    A = ATT[f]; names = [r["name"] for r in DATASETS[(f, "primary")]["rows"]]; N = len(names)
    lx = np.array([math.log10(A[n]["x_e"]) for n in names]); mv = np.array([A[n]["MV"] for n in names])
    A1[f] = {}
    # (1) how much of each subset's drop is the subset's host-field / luminosity selection?
    for F in ("V3S", "V3D", "MOND", "ISO"):
        r_ = np.array([A[n]["lb0"] - A[n][f"logG_{F}"] for n in names])
        A1[f][F] = {}
        for mk in ("clean", "C2-C4"):
            m = np.array([n in set(T2[f][F]["clean"][mk]["names"]) for n in names])
            if m.sum() < 2: continue
            def drops(ii):
                rr, xx, vv, mm = r_[ii], lx[ii], mv[ii], m[ii]
                if mm.sum() < 1 or (~mm).sum() < 1: return (np.nan,) * 3
                obs = np.median(rr) - np.median(rr[mm])
                c1 = ols_multi([xx], rr); fit1 = rr.mean() + c1[0] * (xx - xx.mean())
                c2 = ols_multi([xx, vv], rr); A_ = np.column_stack([np.ones(len(rr)), xx, vv]); co = np.linalg.lstsq(A_, rr, rcond=None)[0]; fit2 = A_ @ co
                return obs, np.median(fit1) - np.median(fit1[mm]), np.median(fit2) - np.median(fit2[mm])
            o0 = drops(np.arange(N))
            bs = np.array([drops(ii) for ii in np.random.default_rng(31).integers(0, N, (2000, N))])
            ex = bs[:, 0] - bs[:, 1]; ex2 = bs[:, 0] - bs[:, 2]
            A1[f][F][mk] = dict(obs_drop=float(o0[0]), exp_drop_xe=float(o0[1]), exp_drop_xe_MV=float(o0[2]),
                                excess_over_xe=float(o0[0] - o0[1]), sd_excess_over_xe=float(np.nanstd(ex)),
                                excess_over_xe_MV=float(o0[0] - o0[2]), sd_excess_over_xe_MV=float(np.nanstd(ex2)))
            v = A1[f][F][mk]
            P(f"   [{f}] {F:4s} {mk:6s}: drop of the median residual {v['obs_drop']:+.3f}; expected from x_e selection {v['exp_drop_xe']:+.3f}, "
              f"from x_e + M_V {v['exp_drop_xe_MV']:+.3f} -> left for the systematics {v['excess_over_xe']:+.3f}+-{v['sd_excess_over_xe']:.3f} / "
              f"{v['excess_over_xe_MV']:+.3f}+-{v['sd_excess_over_xe_MV']:.3f}")
    # (2) clean subset under the host-mass bracket and under the 84th-percentile q (orbit MC)
    ell_ok = np.array([not A[n]["ell_flag"] for n in names]); grad_ok = np.array([not A[n]["grad_flag"] for n in names])
    nq_ok = np.array([A[n]["Nq"] >= NQ_MIN for n in names]); allix = np.arange(N)
    for F in ("V3S", "MOND", "ISO"):
        for lab, qf in (("E_lo", lambda a: a.get(f"q_{F}_bracket_lo_hi", [np.nan, np.nan])[0]), ("E_hi", lambda a: a.get(f"q_{F}_bracket_lo_hi", [np.nan, np.nan])[1]),
                        ("q84", lambda a: a.get(f"q_{F}_p16_p84", [np.nan, np.nan])[1])):
            q = np.array([qf(A[n]) if A[n]["pm"] else np.nan for n in names], float)
            m = (q < Q_SAFE) & ell_ok & grad_ok & nq_ok
            v = bmed(RES[(f, "primary", F)], allix[m], rngb) if m.sum() else (np.nan, np.nan)
            A1[f][F][f"clean_{lab}"] = dict(N=int(m.sum()), names=list(np.array(names)[m]), Delta=list(v))
            P(f"   [{f}] {F:4s} clean with {lab:4s}: N {int(m.sum()):2d} Delta {v[0]:+.3f}+-{v[1]:.3f}  ({', '.join(np.array(names)[m])})")
    # (3) host-field slope at fixed luminosity: data (log g_obs/g_bar) and each flavor's own prediction
    lb = np.array([A[n]["lb0"] for n in names])
    bd, sdd = boot_coef([lx, mv], lb)
    A1[f]["fixedMV_slope"] = dict(data=[float(bd[0]), float(sdd[0])])
    line = f"   [{f}] d/dlog x_e at fixed M_V: data log(g_obs/g_bar) {bd[0]:+.3f}+-{sdd[0]:.3f}"
    for F in ("V3S", "MOND", "ISO", "V3S0"):
        pr = np.array([A[n][f"logG_{F}"] for n in names]); bp, sp = boot_coef([lx, mv], pr)
        A1[f]["fixedMV_slope"][F] = [float(bp[0]), float(sp[0])]
        line += f" | {F} prediction {bp[0]:+.3f}+-{sp[0]:.3f}"
    P(line)
R["A1_posthoc"] = A1

# ------------------------------------------------------------------ K8 + close
rss = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / (1024 ** 3 if sys.platform == "darwin" else 1024 ** 2)
check("K8", rss < 1.0, f"peak RSS {rss:.2f} GB", "< 1 GB", "memory")
npass = sum(1 for v in CHK.values() if v["ok"]); ntot = len(CHK)
R["checks"] = CHK; R["runtime_s"] = time.time() - T0; R["n_solves"] = NSOLVE[0]
P(f"\nZ2_SATELLITE_SYSTEMATICS COMPLETE: {npass}/{ntot} checks PASS.  ({time.time() - T0:.0f} s)")
json.dump(R, open(os.path.join(HERE, f"z2_satellite_systematics_results{SFX}.json"), "w"), indent=1, default=lambda o: o.tolist() if hasattr(o, "tolist") else (bool(o) if isinstance(o, np.bool_) else str(o)))
open(os.path.join(HERE, f"z2_satellite_systematics{SFX}.out"), "w").write("\n".join(OUT) + "\n")
sys.exit(0 if npass == ntot else 1)
