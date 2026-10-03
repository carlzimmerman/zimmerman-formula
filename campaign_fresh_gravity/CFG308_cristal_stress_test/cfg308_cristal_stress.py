#!/usr/bin/env python3
"""CFG308 -- the CRISTAL a0 point at z ~ 5 stress-tested on framework-native inputs (owner: "stress test cristal too").
Frozen criteria: FROZEN_CRITERIA.md (ca50d064d), committed before any number of this lane was computed.
kappa = 1/2 FITTED.  The cold mass is still required; no dark-matter particle is added.  No halo-fit quantity enters any cell.
No sentence here says the data favour a law; a lean is not a detection.
Estimator: CFG223's implied s* (median-root of log10[D / nu(g_bar / (a0 s))]) and its 10,000-resample galaxy bootstrap, exec'd from the committed source;
native g_bar = M_bar x CFG216's thin exponential disc (as CFG303).  Grid: gas 7 x M* 3 x pressure (3 at R_e, 5 at R_out) x inclination 3 x radius 2 x sample 2
(six detections; nine with the three dust upper limits as bounds) = 1,008 decision cells; leave-one-out subgrids as control (iii).
Run:  python3 campaign_fresh_gravity/CFG308_cristal_stress_test/cfg308_cristal_stress.py            (MUTATE=1: every velocity x 1.5, separate outputs;
      the MUTATE run reads the main run's outputs).  CFG308_SERIAL=1 forces a single process (same numbers).
"""
import os, sys, io, csv, json, math, contextlib, time, hashlib
sys.dont_write_bytecode = True
import numpy as np
from scipy.optimize import brentq

T0 = time.time()
LANE = os.path.dirname(os.path.abspath(__file__))
CFG = os.path.dirname(LANE)
REPO = os.path.dirname(CFG)
MUT = os.environ.pop("MUTATE", "").strip() == "1"           # popped: the exec'd lanes must run in their committed (unmutated) mode
SERIAL = os.environ.get("CFG308_SERIAL", "").strip() == "1"
SFX = "_MUTATE" if MUT else ""
VF = 1.5 if MUT else 1.0
OUT, CHK = [], []


def P(s=""):
    print(s, flush=True); OUT.append(s)


def check(name, val, ok):
    CHK.append(bool(ok)); P(f"  [{'PASS' if ok else 'FAIL'}] {name}: {val}")


def sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()


def rel(p):
    return os.path.relpath(p, REPO)


def exec_upto(path, stop, env=None):
    """exec the committed source text of `path` up to the unique marker `stop` (stdout swallowed); returns (namespace, source)."""
    src = open(path).read()
    assert src.count(stop) == 1, (rel(path), stop, src.count(stop))
    saved = {}
    for k, v in (env or {}).items():
        saved[k] = os.environ.get(k); os.environ[k] = v
    ns = {"__file__": path, "__name__": "cfg308_exec"}
    try:
        with contextlib.redirect_stdout(io.StringIO()):
            exec(compile(src[:src.index(stop)], rel(path), "exec"), ns)
    finally:
        for k, v in saved.items():
            if v is None:
                os.environ.pop(k, None)
            else:
                os.environ[k] = v
    return ns, src


P(__doc__.split("Run:")[0].strip())
P(f"\nMODE: {'MUTATE (every velocity x 1.5)' if MUT else 'main'}")
P("Frozen file (sha256 at run time): FROZEN_CRITERIA.md " + sha(os.path.join(LANE, "FROZEN_CRITERIA.md")))

# ================================================================================================================ committed machinery
F223 = os.path.join(CFG, "CFG223_a0_over_cosmic_time", "cfg223_a0_over_time.py")
F216 = os.path.join(CFG, "CFG216_rc100_within_sample", "cfg216_rc100.py")
ns223, _ = exec_upto(F223, 'P("\\nCONTROLS")')
ns216, _ = exec_upto(F216, "# " + "-" * 96 + " data\n", env={"RC100_INPUT": "corrected"})
P(f"Loaded: {rel(F223)} (sha {sha(F223)[:12]}) up to its CONTROLS marker; {rel(F216)} (sha {sha(F216)[:12]}) up to its data marker")
analyse, expectations, bands, implied, place, Farr = (ns223[k] for k in ("analyse", "expectations", "bands", "implied", "place", "Farr"))
NU, A0L, Efun, K = ns223["NU"], ns223["A0L"], ns223["E"], ns223["K"]
disc_v2, G2SI, XN = ns216["disc_v2"], ns216["G2SI"], ns216["XN"]
crbyid, n220 = ns223["crbyid"], ns223["n220"]
vec_rows = n220["vec_rows"]
assert abs(XN - 1.678) < 1e-15

# ================================================================================================================ inputs (record files only)
AT = os.path.join(REPO, "data_assembly", "arxiv_tables")
kin = {r["id"]: r for r in csv.DictReader(open(os.path.join(AT, "cristal2025_kinematics.csv"), newline=""))}
dyn = {r["id"]: r for r in csv.DictReader(open(os.path.join(AT, "cristal2025_dynamics.csv"), newline=""))}
pts = list(csv.DictReader(open(os.path.join(AT, "cristal_vector", "cristal_points.csv"), newline="")))
c228 = {r["gid"]: r for r in csv.DictReader(open(os.path.join(CFG, "CFG228_alma_cubes", "cfg228_stage1_alpine_measurements.csv"), newline=""))}
jones = list(csv.DictReader(open(os.path.join(REPO, "data_assembly", "highz_literature_tables", "jones2021_alpine", "jones2021_table1_sample_classes.csv"), newline="")))
J303 = json.load(open(os.path.join(CFG, "CFG303_lcdm_free_inputs", "cfg303_rc100_cristal_LCDMFREE_results.json")))
C303 = J303["points"]["CRISTAL"]
pg303 = list(csv.DictReader(open(os.path.join(CFG, "CFG303_lcdm_free_inputs", "cfg303_cristal_pergalaxy_LCDMFREE.csv"), newline="")))

SIX = ["02", "03", "07a", "11", "19", "20"]                  # CFG303 / CFG220 DET order
NINE = ["02", "03", "07a", "08", "11", "12", "19", "20", "23b"]   # CFG303's nine-disc order (ids12 with f_molgas)
UL = {"08", "12", "23b"}
CII_MAP = {"20", "23b"}                                        # inclinations from the [CII] flux map (table footnote g: 10a, 20, 23)
r20 = c228["DC494057"]                                         # CFG228 Stage 1: DC494057 = DEIMOS_COSMOS_494057 = CRISTAL-20 (HZ4)
assert r20["cube_tag"] == "DEIMOS_COSMOS_494057" and abs(float(r20["z"]) - crbyid["20"]["z"]) < 0.001
L20 = float(r20["L_CII"])
sig_mom = float(np.median([float(r["inc_moment_err"]) for r in jones]))
sig_3db = float(np.median([float(r["inc_3DBarolo_err"]) for r in jones]))
SIG_I = {i: (sig_mom if i in CII_MAP else sig_3db) for i in NINE}
vr_mk, vr_tab = vec_rows("outermost_data_marker"), vec_rows("table_Rout")
G = {}
for i in NINE:
    g = crbyid[i]; k = kin[i]; d = dyn[i]
    obs = max((r for r in pts if r["id"] == i and r["kind"] == "data"), key=lambda r: float(r["R_kpc"]))
    G[i] = dict(z=g["z"], lms=g["logMstar"], f=g["f_molgas"], fhi=float(k["errhi"]), flo=float(k["errlo"]), Re=g["Re"], Vrot=g["Vrot"], sig0=g["sig0"],
                inc=float(d["inc_deg"]), Rmk=vr_mk[i][0], Vtot=vr_mk[i][2], Rtab=vr_tab[i][0], Vtab=vr_tab[i][2], Robs=float(obs["R_kpc"]), Vobs=float(obs["V_kms"]),
                ul=i in UL)
    assert all(math.isfinite(v) for v in (G[i]["z"], G[i]["lms"], G[i]["f"], G[i]["Re"], G[i]["Vrot"], G[i]["sig0"], G[i]["inc"])), i
P("\nINPUTS (record files; no download)")
P(f"  CRISTAL tables, cristal_vector outer summary and observed markers; CFG228 L_[CII](CRISTAL-20 = DC494057) = {L20:.4e} Lsun -> log M_gas,[CII] (alpha 30) = {math.log10(30 * L20):.3f}")
P(f"  Jones+21 Table 1 median inclination errors: moment map {sig_mom:.1f} deg, 3DBarolo {sig_3db:.1f} deg  ->  sigma_i: " + ", ".join(f"{i} {SIG_I[i]:.1f}" for i in NINE))
P("  per disc: id  z  log M*  f_molgas (+hi/-lo)  R_e  V_rot(R_e)  sigma0  inc  | R_mk  V_tot(R_mk)  alpha_c = 3.36 R/R_e  V_r^2 = V_tot^2 - alpha_c sigma0^2  | raw marker V_obs")
for i in NINE:
    g = G[i]; ac = 3.36 * g["Rmk"] / g["Re"]
    P(f"    {i:4s} {g['z']:.3f} {g['lms']:.2f} {g['f']:.2f} (+{g['fhi']:.2f}/-{g['flo']:.2f}){' UL' if g['ul'] else '   '} {g['Re']:.1f} {g['Vrot']:6.1f} {g['sig0']:6.1f} {g['inc']:5.1f} | "
      f"{g['Rmk']:.3f} {g['Vtot']:6.1f} {ac:5.2f} {g['Vtot'] ** 2 - ac * g['sig0'] ** 2:9.0f} | {g['Vobs']:5.1f} at {g['Robs']:.3f}")
check("T0 inputs: the declared sigma_i (9.5 deg image, 19 deg [CII] map) are the Jones+21 medians on disk, and CFG228's L_[CII] row for CRISTAL-20 exists",
      f"medians {sig_3db:.2f} / {sig_mom:.2f}; L20 {L20:.4e}", abs(sig_3db - 9.5) < 1e-9 and abs(sig_mom - 19.0) < 1e-9 and L20 > 0)

# ================================================================================================================ the builder
GAS = ["G0", "G+", "G-", "C0", "C+", "C-", "S"]
ALPHA_CII = {"C0": 30.0, "C+": 30.0 * 10 ** 0.3, "C-": 30.0 * 10 ** -0.3}
DMS = [0.0, -0.15, 0.15]
PRES = {"Re": ["P_auth", "P168", "P0"], "Rout": ["P_auth", "P_B10", "P336", "P168", "P0"]}
INC = [0, -1, 1]
GFLOOR = 1e-20


def xi(Re, R):
    return disc_v2(1.0, Re, R) / R * G2SI


def build(ids, radius, gas, dms, pres, inc, ul_mode="limit", vf=VF, rdef="mk"):
    """one row-set: z, g_bar, g_obs (SI), D; 'floor' marks discs with no rotation left (g_obs = 0 carried as GFLOOR)."""
    z, gb, go, fl = [], [], [], []
    for i in ids:
        g = G[i]
        Ms0 = 10 ** g["lms"]
        Ms = 10 ** (g["lms"] + dms)
        if gas == "S":
            Mg = 0.0
        elif g["ul"]:
            Mg = Ms0 * g["f"] / (1 - g["f"]) if ul_mode == "limit" else 0.0
        else:
            f = g["f"] + g["fhi"] if gas == "G+" else (max(g["f"] - g["flo"], 0.0) if gas == "G-" else g["f"])
            Mg = Ms0 * f / (1 - f)
            if gas in ALPHA_CII and i == "20":
                Mg = ALPHA_CII[gas] * L20
        Mb = Ms + Mg
        if inc == 0:
            si = 1.0
        else:
            ip = min(max(g["inc"] + inc * SIG_I[i], 5.0), 90.0)
            si = (math.sin(math.radians(g["inc"])) / math.sin(math.radians(ip))) ** 2
        s0 = g["sig0"] * vf
        if radius == "Re":
            R = g["Re"]
            a = {"P_auth": 3.36, "P168": 1.68, "P0": 0.0}[pres]
            v2 = (g["Vrot"] * vf) ** 2 * si + a * s0 ** 2
        else:
            R, Vt = (g["Rmk"], g["Vtot"]) if rdef == "mk" else (g["Rtab"], g["Vtab"])
            Vt = Vt * vf
            ac = 3.36 * R / g["Re"]
            Vr2 = max(Vt ** 2 - ac * s0 ** 2, 0.0)
            if pres == "P_auth":
                v2 = Vt ** 2 + Vr2 * (si - 1.0)
            elif pres == "P_B10":
                v2 = Vr2 * si + 2 * XN * R / g["Re"] * s0 ** 2
            else:
                v2 = Vr2 * si + {"P336": 3.36, "P168": 1.68, "P0": 0.0}[pres] * s0 ** 2
        gobs = v2 / R * G2SI
        fl.append(gobs <= 0)
        z.append(g["z"]); gb.append(Mb * xi(g["Re"], R)); go.append(gobs if gobs > 0 else GFLOOR)
    z, gb, go = (np.asarray(v, float) for v in (z, gb, go))
    return dict(z=z, gb=gb, go=go, D=go / gb, floor=np.asarray(fl, bool))


def build_raw_marker(ids, alpha_kind, vf=VF):
    """diagnostic D1: the outermost OBSERVED marker (projected, beam-smeared, uncorrected), deprojected, + alpha sigma0^2, at G0 / dM* 0 / committed i."""
    z, gb, go = [], [], []
    for i in ids:
        g = G[i]
        R = g["Rmk"]
        a = 3.36 * R / g["Re"] if alpha_kind == "3.36R/Re" else float(alpha_kind)
        v2 = (g["Vobs"] * vf / math.sin(math.radians(g["inc"]))) ** 2 + a * (g["sig0"] * vf) ** 2
        z.append(g["z"]); gb.append(10 ** g["lms"] / (1 - g["f"]) * xi(g["Re"], R)); go.append(max(v2 / R * G2SI, GFLOOR))
    z, gb, go = (np.asarray(v, float) for v in (z, gb, go))
    return dict(z=z, gb=gb, go=go, D=go / gb)


def status(r):
    return "root" if not r["unbounded"] else ("no root (floor)" if r["log_s"] < 0 else "no root (ceiling)")


def eval_set(p):
    r, lb, I = analyse(p)
    return dict(s=r["s"], log_s=r["log_s"], status=status(r), unb_frac=r["unb_frac"], lo68=r["lo68"], hi68=r["hi68"], lo95=r["lo95"], hi95=r["hi95"], n=r["n"], z_med=r["z_med"])


def expect(p):
    out = {}
    for L in ("FLAT", "H(z)"):
        Dt, gt = place(p, Farr(L, p["z"]), NU, A0L)
        out[L] = 10 ** float(implied(Dt, gt, NU, A0L)[0][0])
    out["E(z_med)"] = Efun(float(np.median(p["z"])))
    return out


def eval_cell(spec):
    radius, sample, ids, gas, dms, pres, inc = spec
    lo_ul = sample == "nine" and gas != "S"
    pA = build(ids, radius, gas, dms, pres, inc, "limit")
    rA = eval_set(pA)
    ex = expect(pA)
    cell = dict(radius=radius, sample=sample, gas=gas, dMstar=dms, pressure=pres, inclination=inc, n=len(ids), ids=list(ids), A=rA, exp=ex,
                n_floor=int(pA["floor"].sum()))
    if MUT:
        q = build(ids, radius, gas, dms, pres, inc, "limit", vf=1.0)
        ok = ~(pA["floor"] | q["floor"])
        cell["m1_err"] = float(np.max(np.abs(np.log10(pA["D"][ok]) - np.log10(q["D"][ok]) - math.log10(2.25)))) if ok.any() else 0.0
    if lo_ul:
        pB = build(ids, radius, gas, dms, pres, inc, "zero")
        cell["B"] = eval_set(pB)
        if MUT:
            q = build(ids, radius, gas, dms, pres, inc, "zero", vf=1.0)
            ok = ~(pB["floor"] | q["floor"])
            if ok.any():
                cell["m1_err"] = max(cell["m1_err"], float(np.max(np.abs(np.log10(pB["D"][ok]) - np.log10(q["D"][ok]) - math.log10(2.25)))))
        cell["bound"] = "UL bracket"
        lo95, hi95 = min(rA["lo95"], cell["B"]["lo95"]), max(rA["hi95"], cell["B"]["hi95"])
        inside = {L: lo95 <= ex[L] <= hi95 for L in ("FLAT", "H(z)", "E(z_med)")}
        cell["root_bearing"] = rA["status"] == "root" or cell["B"]["status"] == "root"
    elif gas == "S":
        cell["bound"] = "stars-only upper"
        lo95, hi95 = 0.0, rA["hi95"]
        inside = {L: ex[L] <= hi95 for L in ("FLAT", "H(z)", "E(z_med)")}
        cell["root_bearing"] = rA["status"] == "root"
    else:
        cell["bound"] = "none"
        lo95, hi95 = rA["lo95"], rA["hi95"]
        inside = {L: lo95 <= ex[L] <= hi95 for L in ("FLAT", "H(z)", "E(z_med)")}
        cell["root_bearing"] = rA["status"] == "root"
    cell["env95"] = (lo95, hi95)
    cell["F_in"], cell["H_in"], cell["Hz_in_Ezmed"] = inside["FLAT"], inside["H(z)"], inside["E(z_med)"]
    return cell


# ================================================================================================================ control (i): CFG303 identity
P("\nCONTROL (i): CFG303's committed CRISTAL cells reproduced by this lane's builder and CFG223's estimator")
K_RE, K_RO, K_9, K_TAB = ("R_e native, six", "R_out native, six, outermost data marker (primary)", "R_e native, twelve-disc set with SED+gas",
                          "R_out native, six, table R_out (CFG223's radius; model curve at or beyond the last marker)")
ident = {}
if not MUT:
    for key, ids, radius, rdef in ((K_RE, SIX, "Re", "mk"), (K_RO, SIX, "Rout", "mk"), (K_9, NINE, "Re", "mk"), (K_TAB, SIX, "Rout", "tab")):
        p = build(ids, radius, "G0", 0.0, "P_auth", 0, "limit", rdef=rdef)
        rows = [r for r in pg303 if r["point"] == key]
        assert [r["id"] for r in rows] == list(ids), (key, [r["id"] for r in rows])
        dg = max(max(abs(p["gb"][j] / float(r["g_bar_native_ms2"]) - 1), abs(p["go"][j] / float(r["g_obs_ms2"]) - 1)) for j, r in enumerate(rows))
        r_, lb, I = analyse(p)
        r_["expected"] = expectations(p, r_["log_s"], lb, I)
        bd, nr = bands(p)
        c = C303[key]
        d = max(abs(r_["log_s"] - math.log10(c["s"])), *(abs(math.log10(r_[k]) - math.log10(c[k])) for k in ("lo95", "lo68", "hi68", "hi95")))
        d = max(d, *(abs(math.log10(r_["expected"][L]["s"]) - math.log10(c["expected"][L]["s"])) for L in c["expected"]))
        d = max(d, *(abs(r_["expected"][L]["pull"] - c["expected"][L]["pull"]) for L in c["expected"]))
        d = max(d, *(abs(math.log10(bd[float(k)]) - math.log10(v)) for k, v in c["bands"].items()))
        ident[key] = dict(dg=dg, d=d, s=r_["s"], lo68=r_["lo68"], hi68=r_["hi68"], lo95=r_["lo95"], hi95=r_["hi95"], unb=r_["unb_frac"],
                          eF=r_["expected"]["FLAT"]["s"], eH=r_["expected"]["H(z)"]["s"], pF=r_["expected"]["FLAT"]["pull"], pH=r_["expected"]["H(z)"]["pull"])
        P(f"  {key[:60]:60s}: s* {r_['s']:.4f} 68% [{r_['lo68']:.3f}, {r_['hi68']:.3f}] 95% [{r_['lo95']:.3f}, {r_['hi95']:.3f}]; expected FLAT {r_['expected']['FLAT']['s']:.3f} "
          f"H(z) {r_['expected']['H(z)']['s']:.3f} (pulls {r_['expected']['FLAT']['pull']:+.2f} / {r_['expected']['H(z)']['pull']:+.2f}); max rel |dg| vs CFG303 CSV {dg:.1e}; max |diff| vs CFG303 JSON {d:.1e}")
    check("(i-a) per-galaxy g_bar and g_obs from this builder at the committed settings equal CFG303's per-galaxy CSV (R_e six, R_out six, R_e nine at the limit, table R_out)",
          "max relative difference " + ", ".join(f"{v['dg']:.1e}" for v in ident.values()), max(v["dg"] for v in ident.values()) <= 2e-6)
    check("(i-b) R_e six: s*, 68/95 edges, expected s* and pulls (four laws) and the +-0.15/0.30 dex bands equal CFG303's JSON (2.01 [0.24, 7.27] / [0.001, 14.9])",
          f"max |diff| {ident[K_RE]['d']:.1e}", ident[K_RE]["d"] <= 1e-9)
    check("(i-b) R_out six (outermost data marker): the same against CFG303's JSON (1.95 [0.42, 5.05] / [0.001, 8.78])", f"max |diff| {ident[K_RO]['d']:.1e}", ident[K_RO]["d"] <= 1e-9)
    check("(i-b) nine discs with the upper limits AT the limit (R_e) equal CFG303's nine-disc set with the limits used as values (0.674)", f"max |diff| {ident[K_9]['d']:.1e}",
          ident[K_9]["d"] <= 1e-9)
    check("D2 (identity, not graded): CFG303's table-R_out variant (1.90) reproduced", f"max |diff| {ident[K_TAB]['d']:.1e}", ident[K_TAB]["d"] <= 1e-9)
else:
    P("  not applicable in MUTATE mode (every value is mutated); see the main run")

# ================================================================================================================ the grid
specs = []
SAMPLES = [("six", SIX), ("nine", NINE)] + [(f"loo-{d}", [i for i in SIX if i != d]) for d in SIX]
for radius in ("Re", "Rout"):
    for sname, ids in SAMPLES:
        for gas in GAS:
            for dms in DMS:
                for pres in PRES[radius]:
                    for inc in INC:
                        specs.append((radius, sname, tuple(ids), gas, dms, pres, inc))
P(f"\nTHE GRID: {len(specs)} cells ({sum(1 for s in specs if not s[1].startswith('loo'))} decision cells + {sum(1 for s in specs if s[1].startswith('loo'))} leave-one-out cells)")
t1 = time.time()
if SERIAL:
    cells = [eval_cell(s) for s in specs]
else:
    import multiprocessing as mp
    with mp.get_context("fork").Pool(min(12, os.cpu_count() or 1)) as pool:
        cells = pool.map(eval_cell, specs, chunksize=8)
P(f"  evaluated in {time.time() - t1:.0f} s ({'serial' if SERIAL else 'process pool, fork'})")
# C5: a deterministic spot-check that the pool equals a serial evaluation in this process
spot = list(range(0, len(specs), max(1, len(specs) // 24)))[:24]
d5 = 0.0
for j in spot:
    c = eval_cell(specs[j])
    for k in ("s", "lo68", "hi68", "lo95", "hi95"):
        d5 = max(d5, abs(c["A"][k] - cells[j]["A"][k]))
    d5 = max(d5, abs(c["exp"]["H(z)"] - cells[j]["exp"]["H(z)"]), 0.0 if (c["F_in"], c["H_in"]) == (cells[j]["F_in"], cells[j]["H_in"]) else 1.0)
check("C5 the process-pool results equal a serial re-evaluation in this process (24 spread cells; s*, edges, H(z) expectation, flags)", f"max |diff| {d5:.1e}", d5 == 0.0)

DEC = [c for c in cells if not c["sample"].startswith("loo")]
LOO = {d: [c for c in cells if c["sample"] == f"loo-{d}"] for d in SIX}


def key(c):
    return (c["radius"], c["sample"], c["gas"], c["dMstar"], c["pressure"], c["inclination"])


BY = {key(c): c for c in cells}


def fractions(cs):
    n = len(cs)
    fH = sum(not c["H_in"] for c in cs) / n
    fFi = sum(c["F_in"] for c in cs) / n
    return dict(n=n, frac_H_excl=fH, frac_F_in=fFi, frac_F_excl=1 - fFi, frac_H_in=1 - fH,
                n_rival_disfavoured=sum((not c["H_in"]) and c["F_in"] for c in cs), n_flat_disfavoured=sum((not c["F_in"]) and c["H_in"] for c in cs),
                n_both_excluded=sum((not c["F_in"]) and (not c["H_in"]) for c in cs), n_both_inside=sum(c["F_in"] and c["H_in"] for c in cs),
                n_point_no_root=sum(c["A"]["status"] != "root" and (c.get("B") is None or c["B"]["status"] != "root") for c in cs))


def decision(fr):
    if fr["frac_H_excl"] >= 0.80 and fr["frac_F_in"] >= 0.80:
        return "RIVAL ROBUSTLY DISFAVOURED"
    if fr["frac_F_excl"] >= 0.80 and fr["frac_H_in"] >= 0.80:
        return "FLAT ROBUSTLY DISFAVOURED"
    return "NOT DISCRIMINATING"


def fstr(fr):
    return (f"n {fr['n']}: H(z) excluded {fr['frac_H_excl']:.3f}, FLAT inside {fr['frac_F_in']:.3f} (FLAT excluded {fr['frac_F_excl']:.3f}); rival-disfavoured cells "
            f"{fr['n_rival_disfavoured']}, flat-disfavoured {fr['n_flat_disfavoured']}, both excluded {fr['n_both_excluded']}, both inside {fr['n_both_inside']}; point no root {fr['n_point_no_root']}")


def cstr(c):
    a = c["A"]
    s = f"s* {a['s']:.3f} ({a['status']}, no-root resamples {a['unb_frac']:.0%}) 68% [{a['lo68']:.3f}, {a['hi68']:.3f}] 95% [{a['lo95']:.3f}, {a['hi95']:.3f}]"
    if c.get("B"):
        b = c["B"]
        s += f" | UL-at-zero end s* {b['s']:.3f} ({b['status']}) 95% [{b['lo95']:.3f}, {b['hi95']:.3f}]"
    s += f"; envelope [{c['env95'][0]:.3f}, {c['env95'][1]:.3f}] ({c['bound']}); expected FLAT {c['exp']['FLAT']:.3f}, H(z) {c['exp']['H(z)']:.3f} (E(z_med) {c['exp']['E(z_med)']:.3f})"
    s += f"; FLAT {'in' if c['F_in'] else 'OUT'}, H(z) {'in' if c['H_in'] else 'OUT'}"
    return s


# ---------------------------------------------------------------------------------------------------------------- committed cells inside the grid
P("\nTHE COMMITTED CELLS INSIDE THE GRID (G0, dM* 0, P_auth, committed inclination)")
for radius in ("Re", "Rout"):
    for sname in ("six", "nine"):
        P(f"  {radius:4s} {sname:4s}: " + cstr(BY[(radius, sname, "G0", 0.0, "P_auth", 0)]))
if not MUT:
    d_grid = 0.0
    for radius, k303 in (("Re", K_RE), ("Rout", K_RO)):
        a = BY[(radius, "six", "G0", 0.0, "P_auth", 0)]["A"]
        d_grid = max(d_grid, *(abs(a[k] - ident[k303][k]) for k in ("s", "lo68", "hi68", "lo95", "hi95")), abs(BY[(radius, "six", "G0", 0.0, "P_auth", 0)]["exp"]["H(z)"] - ident[k303]["eH"]))
    a9 = BY[("Re", "nine", "G0", 0.0, "P_auth", 0)]["A"]
    d_grid = max(d_grid, *(abs(a9[k] - ident[K_9][k]) for k in ("s", "lo68", "hi68", "lo95", "hi95")))
    check("(i-c) the grid's committed cells (R_e six, R_out six, R_e nine at the limit) equal the identity runs above", f"max |diff| {d_grid:.1e}", d_grid <= 1e-12)

# ---------------------------------------------------------------------------------------------------------------- the decision
P("\nTHE DECISION GRID (1,008 cells: radius x sample {six, nine-with-UL-bounds} x gas x M* x pressure x inclination)")
FR = fractions(DEC)
DECISION = decision(FR)
P("  ALL: " + fstr(FR))
P(f"  -> DECISION (frozen rule, 80% / 80%): {DECISION}")
SEC = {}
SEC["root-bearing cells only"] = fractions([c for c in DEC if c["root_bearing"]])
cz = [dict(c, H_in=c["Hz_in_Ezmed"]) for c in DEC]
SEC["H(z) target = E(z_med)"] = fractions(cz)
for radius in ("Re", "Rout"):
    SEC[f"radius {radius}"] = fractions([c for c in DEC if c["radius"] == radius])
SEC["six-disc sample only"] = fractions([c for c in DEC if c["sample"] == "six"])
SEC["nine-disc (UL bounds) only"] = fractions([c for c in DEC if c["sample"] == "nine"])
SEC["stars-only cells (S)"] = fractions([c for c in DEC if c["gas"] == "S"])
SEC["detected-gas cells (not S)"] = fractions([c for c in DEC if c["gas"] != "S"])
P("  secondary readings (reported; they cannot change the headline):")
for k, v in SEC.items():
    P(f"    {k:30s}: {fstr(v)}  [rule would read: {decision(v)}]")

# ---------------------------------------------------------------------------------------------------------------- marginals and the dominant axis
P("\nMARGINALS AND THE DOMINANT AXIS (within each radius sub-grid of the decision grid)")
AX = {"gas": GAS, "dMstar": DMS, "pressure": None, "inclination": INC, "sample": ["six", "nine"]}
MARG, SWING = {}, {}
for radius in ("Re", "Rout"):
    sub = [c for c in DEC if c["radius"] == radius]
    for ax, levels in AX.items():
        levels = PRES[radius] if ax == "pressure" else levels
        m = {}
        for lv in levels:
            cs = [c for c in sub if c[ax] == lv]
            m[str(lv)] = dict(n=len(cs), frac_H_excl=sum(not c["H_in"] for c in cs) / len(cs), frac_F_excl=sum(not c["F_in"] for c in cs) / len(cs))
        MARG[f"{radius}|{ax}"] = m
        sH = max(v["frac_H_excl"] for v in m.values()) - min(v["frac_H_excl"] for v in m.values())
        sF = max(v["frac_F_excl"] for v in m.values()) - min(v["frac_F_excl"] for v in m.values())
        SWING.setdefault(ax, {})[radius] = dict(H=sH, F=sF)
        P(f"  {radius:4s} {ax:11s}: " + "; ".join(f"{lv} H-excl {v['frac_H_excl']:.2f} F-excl {v['frac_F_excl']:.2f}" for lv, v in m.items()) + f"  | swing H {sH:.2f}, F {sF:.2f}")
fRe = sum(not c["H_in"] for c in DEC if c["radius"] == "Re") / sum(1 for c in DEC if c["radius"] == "Re")
fRo = sum(not c["H_in"] for c in DEC if c["radius"] == "Rout") / sum(1 for c in DEC if c["radius"] == "Rout")
gRe = sum(not c["F_in"] for c in DEC if c["radius"] == "Re") / sum(1 for c in DEC if c["radius"] == "Re")
gRo = sum(not c["F_in"] for c in DEC if c["radius"] == "Rout") / sum(1 for c in DEC if c["radius"] == "Rout")
SWING["radius"] = {"both": dict(H=abs(fRe - fRo), F=abs(gRe - gRo))}
SW_H = {ax: max(v["H"] for v in d.values()) for ax, d in SWING.items()}
SW_F = {ax: max(v["F"] for v in d.values()) for ax, d in SWING.items()}
DOM = max(SW_H, key=SW_H.get)
DOM_F = max(SW_F, key=SW_F.get)
P(f"  radius axis: H-excl R_e {fRe:.2f} vs R_out {fRo:.2f} (swing {abs(fRe - fRo):.2f}); F-excl {gRe:.2f} vs {gRo:.2f}")
P("  swings in frac_H_excl (max over radius): " + ", ".join(f"{a} {v:.2f}" for a, v in sorted(SW_H.items(), key=lambda t: -t[1])))
P("  swings in frac_F_excl (max over radius): " + ", ".join(f"{a} {v:.2f}" for a, v in sorted(SW_F.items(), key=lambda t: -t[1])))
P(f"  -> DOMINANT AXIS (frozen metric, H(z)-exclusion swing): {DOM}; for FLAT's exclusion: {DOM_F}")
EXT = {"gas": ("G+", "G-"), "dMstar": (0.15, -0.15), "pressure": ("P0", "P_auth"), "inclination": (1, -1)}
DLS = {}
for ax, (lo, hi) in EXT.items():
    ds = []
    for c in DEC:
        if c["sample"] != "six" or c["gas"] == "S" or c[ax] != lo:
            continue
        k2 = dict(radius=c["radius"], sample=c["sample"], gas=c["gas"], dMstar=c["dMstar"], pressure=c["pressure"], inclination=c["inclination"])
        k2[ax] = hi
        o = BY[(k2["radius"], k2["sample"], k2["gas"], k2["dMstar"], k2["pressure"], k2["inclination"])]
        if c["A"]["status"] == "root" and o["A"]["status"] == "root":
            ds.append(abs(o["A"]["log_s"] - c["A"]["log_s"]))
    DLS[ax] = dict(n=len(ds), median=float(np.median(ds)) if ds else None)
ds = [abs(BY[("Rout",) + key(c)[1:]]["A"]["log_s"] - c["A"]["log_s"]) for c in DEC if c["radius"] == "Re" and c["sample"] == "six" and c["gas"] != "S" and c["pressure"] == "P_auth"
      and c["A"]["status"] == "root" and BY[("Rout",) + key(c)[1:]]["A"]["status"] == "root"]
DLS["radius (P_auth)"] = dict(n=len(ds), median=float(np.median(ds)) if ds else None)
P("  median |d log10 s*| between extreme levels (six discs, root-bearing matched pairs): " +
  ", ".join(f"{a} {v['median']:.3f} (n {v['n']})" if v["median"] is not None else f"{a} n/a (n 0)" for a, v in DLS.items()))

# ---------------------------------------------------------------------------------------------------------------- leave-one-out (control iii)
P("\nCONTROL (iii): LEAVE-ONE-OUT (the full (a)-(e) grid on each five-disc subset of the six)")
LOOR = {}
for d in SIX:
    fr = fractions(LOO[d]); dec = decision(fr)
    pr = {r: BY[(r, f"loo-{d}", "G0", 0.0, "P_auth", 0)] for r in ("Re", "Rout")}
    LOOR[d] = dict(fractions=fr, decision=dec, committed_cells={r: dict(s=v["A"]["s"], status=v["A"]["status"], lo95=v["A"]["lo95"], hi95=v["A"]["hi95"],
                                                                         lo68=v["A"]["lo68"], hi68=v["A"]["hi68"], eH=v["exp"]["H(z)"], F_in=v["F_in"], H_in=v["H_in"])
                                                                 for r, v in pr.items()})
    P(f"  drop {d:4s}: {fstr(fr)} -> {dec}")
    for r, v in pr.items():
        P(f"       committed cell {r:4s}: " + cstr(v))
FR_LOO_POOL = fractions([c for d in SIX for c in LOO[d]])
P("  pooled over the six LOO subgrids (reported): " + fstr(FR_LOO_POOL))
loo_ok = all(v["decision"] == DECISION for v in LOOR.values())
if MUT:
    P(f"  (MUTATE run: LOO decisions reported only) full {DECISION}; LOO " + ", ".join(f"{d}: {v['decision']}" for d, v in LOOR.items()))
else:
  check("(iii) LOO stability: the frozen decision recomputed on each of the six leave-one-out subgrids equals the full-grid decision",
        f"full {DECISION}; LOO " + ", ".join(f"{d}: {v['decision']}" for d, v in LOOR.items()), loo_ok)

# ---------------------------------------------------------------------------------------------------------------- structural checks C1-C4
P("\nSTRUCTURAL CHECKS (monotonicity of the median-root; point estimates, matched cells, both ends of the UL bracket)")
TOL = 1e-9


def le(a, b):
    """s_a <= s_b, with ties at the bracket floor/ceiling satisfied"""
    return a <= b * (1 + TOL) or (a >= 999.0 and b >= 999.0) or (a <= 0.0011 and b <= 0.0011)


def ends(c):
    return [c["A"]["s"]] + ([c["B"]["s"]] if c.get("B") else [])


viol = {"C1": 0, "C2": 0, "C3": 0, "C4": 0}
ncmp = {"C1": 0, "C2": 0, "C3": 0, "C4": 0}
for c in cells:
    r, sm, gas, dms, pres, inc = key(c)
    if gas == "G0":
        a, b = BY[(r, sm, "G+", dms, pres, inc)], BY[(r, sm, "G-", dms, pres, inc)]
        for x, y, z_ in zip(ends(a), ends(c), ends(b)):
            ncmp["C1"] += 1; viol["C1"] += not (le(x, y) and le(y, z_))
    if dms == 0.0:
        a, b = BY[(r, sm, gas, 0.15, pres, inc)], BY[(r, sm, gas, -0.15, pres, inc)]
        for x, y, z_ in zip(ends(a), ends(c), ends(b)):
            ncmp["C1"] += 1; viol["C1"] += not (le(x, y) and le(y, z_))
    if pres == "P0":
        chain = ["P0", "P168", "P_auth"] if r == "Re" else ["P0", "P168", "P336", "P_B10"]
        seq = [BY[(r, sm, gas, dms, p_, inc)] for p_ in chain]
        for e in range(len(ends(c))):
            v = [ends(x)[e] for x in seq]
            ncmp["C2"] += 1; viol["C2"] += not all(le(v[t], v[t + 1]) for t in range(len(v) - 1))
    if gas == "S":
        sS = c["A"]["s"]
        for g2 in GAS[:-1]:
            for x in ends(BY[(r, sm, g2, dms, pres, inc)]):
                ncmp["C3"] += 1; viol["C3"] += not le(x, sS)
    if c.get("B"):
        ncmp["C3"] += 1; viol["C3"] += not le(c["A"]["s"], c["B"]["s"])
    if inc == 0:
        a, b = BY[(r, sm, gas, dms, pres, 1)], BY[(r, sm, gas, dms, pres, -1)]
        for x, y, z_ in zip(ends(a), ends(c), ends(b)):
            ncmp["C4"] += 1; viol["C4"] += not (le(x, y) and le(y, z_))
check("C1 s*(G+) <= s*(G0) <= s*(G-) and s*(M* +0.15) <= s*(0) <= s*(-0.15) in every matched set", f"{ncmp['C1'] - viol['C1']}/{ncmp['C1']} hold", viol["C1"] == 0)
check("C2 s* non-decreasing in the pressure term (R_e: P0 <= P168 <= P_auth; R_out: P0 <= P168 <= P336 <= P_B10)", f"{ncmp['C2'] - viol['C2']}/{ncmp['C2']} hold", viol["C2"] == 0)
check("C3 stars-only s* >= every gas level's s*, and the UL-at-zero end >= the UL-at-limit end", f"{ncmp['C3'] - viol['C3']}/{ncmp['C3']} hold", viol["C3"] == 0)
check("C4 s*(inclination -sigma_i) >= s*(committed) >= s*(+sigma_i)", f"{ncmp['C4'] - viol['C4']}/{ncmp['C4']} hold", viol["C4"] == 0)

# ---------------------------------------------------------------------------------------------------------------- diagnostics D1
P("\nDIAGNOSTIC D1 (outside the decision): the raw outermost OBSERVED marker (projected, beam-smeared, no correction), deprojected, + alpha sigma0^2; G0, dM* 0, committed i, six")
D1 = {}
for ak in ("0", "1.68", "3.36", "3.36R/Re"):
    p = build_raw_marker(SIX, ak)
    r1 = eval_set(p); ex = expect(p)
    D1[ak] = dict(r1, eH=ex["H(z)"], eF=ex["FLAT"], D=[float(x) for x in p["D"]], F_in=r1["lo95"] <= ex["FLAT"] <= r1["hi95"], H_in=r1["lo95"] <= ex["H(z)"] <= r1["hi95"])
    P(f"  alpha {ak:8s}: per-disc D " + ", ".join(f"{i} {x:.2f}" for i, x in zip(SIX, p["D"])) + f"; s* {r1['s']:.3f} ({r1['status']}, no-root {r1['unb_frac']:.0%}) "
      f"95% [{r1['lo95']:.3f}, {r1['hi95']:.3f}]; FLAT {'in' if D1[ak]['F_in'] else 'OUT'}, H(z) {ex['H(z)']:.2f} {'in' if D1[ak]['H_in'] else 'OUT'}")

# ---------------------------------------------------------------------------------------------------------------- MUTATE checks
MCH = {}
if MUT:
    P("\nMUTATE CONTROLS (every velocity x 1.5; compared with the main run's grid)")
    y = np.geomspace(1e-10, 1e10, 400001)
    slope = np.diff(np.log(NU(y))) / np.diff(np.log(y))
    check("M0 precondition: d log nu_mono / d log y lies in [-1/2, 0] (so the median delta falls by at most 0.5 per dex of s)", f"range [{slope.min():.6f}, {slope.max():.2e}]",
          slope.min() >= -0.5 - 1e-6 and slope.max() <= 1e-9)
    m1 = max(c["m1_err"] for c in cells)
    check("M1 every non-floored log D moves by +log10(2.25) = +0.35218 exactly, in every build of every cell", f"max |error| {m1:.1e}", m1 <= 1e-12)
    main_csv = os.path.join(LANE, "cfg308_grid.csv")
    if os.path.exists(main_csv):
        mrows = {(r["radius"], r["sample"], r["gas"], float(r["dMstar"]), r["pressure"], int(r["inclination"])): r for r in csv.DictReader(open(main_csv, newline=""))}
        nroot, nok, facs, bad = 0, 0, [], []
        for c in cells:
            m = mrows[key(c)]
            for tag, mine in (("A", c["A"]), ("B", c.get("B"))):
                if mine is None:
                    continue
                st = m[f"status_{tag}"]; s0 = float(m[f"s_{tag}"])
                if st != "root":
                    continue
                nroot += 1
                ok = (mine["s"] >= 5.0625 * s0 * (1 - 1e-9)) or (mine["status"] == "no root (ceiling)" and 5.0625 * s0 > 999.0)
                nok += ok
                if mine["status"] == "root":
                    facs.append(mine["s"] / s0)
                if not ok:
                    bad.append((key(c), tag, s0, mine["s"]))
        MCH["M2"] = dict(n_root=nroot, n_ok=nok, factor_median=float(np.median(facs)), factor_min=float(np.min(facs)), factor_q=[float(v) for v in np.percentile(facs, [5, 25, 75, 95])])
        P(f"  rise factors (root -> root): median {np.median(facs):.2f}, min {np.min(facs):.3f}, 5-95% {np.percentile(facs, 5):.2f}-{np.percentile(facs, 95):.2f}; first violations {bad[:3]}")
        check("M2 in every main-run root, s* rises by >= 2.25^2 = 5.0625 (or reaches the 1000 ceiling)", f"{nok}/{nroot}", nroot > 0 and nok == nroot)
    else:
        check("M2 the main run's cfg308_grid.csv is present to compare against", "missing", False)
    m3 = 0.0
    for radius in ("Re", "Rout"):
        p = build(SIX, radius, "G0", 0.0, "P_auth", 0, "limit")
        f = lambda ls: float(np.median(np.log10(p["D"]) - np.log10(NU(p["gb"] / (A0L * 10 ** ls)))))
        bq = brentq(f, -3.0, 3.0, xtol=1e-13, rtol=1e-13)
        m3 = max(m3, abs(bq - BY[(radius, "six", "G0", 0.0, "P_auth", 0)]["A"]["log_s"]))
        P(f"  committed cell {radius}: mutated s* {BY[(radius, 'six', 'G0', 0.0, 'P_auth', 0)]['A']['s']:.4f}; scalar brentq {10 ** bq:.4f}")
    check("M3 the committed cells' mutated s* equal an independent scalar brentq re-solve (|d log10 s| <= 1e-6)", f"max {m3:.1e}", m3 <= 1e-6)
    if "M2" in MCH:
        P(f"  {'HIT ' if MCH['M2']['n_ok'] == MCH['M2']['n_root'] else 'MISS'} H10a every root-bearing cell rises by >= 5.06: {MCH['M2']['n_ok']}/{MCH['M2']['n_root']}")
        P(f"  {'HIT ' if 6 <= MCH['M2']['factor_median'] <= 20 else 'MISS'} H10b median rise factor between 6 and 20: {MCH['M2']['factor_median']:.2f}")

# ---------------------------------------------------------------------------------------------------------------- hand estimates (main run)
HE = {}
if not MUT:
    P("\nHAND ESTIMATES (frozen in the criteria; scored here, misses kept)")
    rootc = SEC["root-bearing cells only"]
    Sc = [c for c in DEC if c["gas"] == "S"]
    p0 = [c for c in DEC if c["radius"] == "Rout" and c["pressure"] == "P0" and c["sample"] == "six"]
    rcom = BY[("Rout", "six", "G0", 0.0, "P_auth", 0)]
    flips = [d for d in SIX if LOOR[d]["committed_cells"]["Rout"]["H_in"] != rcom["H_in"]]
    HE = {
        "H1 control (i) exact": all(v["d"] <= 1e-9 for v in ident.values()),
        "H2 frac_H_excl in [0.45, 0.80]": 0.45 <= FR["frac_H_excl"] <= 0.80,
        "H3 frac_F_in in [0.45, 0.75]": 0.45 <= FR["frac_F_in"] <= 0.75,
        "H4 decision NOT DISCRIMINATING": DECISION == "NOT DISCRIMINATING",
        "H5a root-only: H(z) excluded in 40-75% of root cells": 0.40 <= rootc["frac_H_excl"] <= 0.75,
        "H5b root-only: FLAT inside in >= 90% of root cells": rootc["frac_F_in"] >= 0.90,
        "H6a dominant axis = pressure": DOM == "pressure",
        "H6b gas route second": sorted(SW_H, key=lambda a: -SW_H[a])[1] == "gas",
        "H7 R_out P0: no root in every six-disc cell": all(c["A"]["status"] != "root" for c in p0),
        "H8 H(z) not excluded in >= 80% of stars-only cells": sum(c["H_in"] for c in Sc) / len(Sc) >= 0.80,
        "H9a decision LOO-stable": loo_ok,
        "H9b the committed R_out H(z) exclusion flips under >= 1 LOO": len(flips) >= 1,
        "H11 D1 alpha 0: no root": D1["0"]["status"] != "root",
        "H12 frac_F_excl < 0.5": FR["frac_F_excl"] < 0.5,
    }
    detail = {
        "H2 frac_H_excl in [0.45, 0.80]": f"{FR['frac_H_excl']:.3f}", "H3 frac_F_in in [0.45, 0.75]": f"{FR['frac_F_in']:.3f}", "H4 decision NOT DISCRIMINATING": DECISION,
        "H5a root-only: H(z) excluded in 40-75% of root cells": f"{rootc['frac_H_excl']:.3f} (n {rootc['n']})", "H5b root-only: FLAT inside in >= 90% of root cells": f"{rootc['frac_F_in']:.3f}",
        "H6a dominant axis = pressure": DOM, "H6b gas route second": sorted(SW_H, key=lambda a: -SW_H[a])[1],
        "H7 R_out P0: no root in every six-disc cell": f"{sum(c['A']['status'] != 'root' for c in p0)}/{len(p0)}",
        "H8 H(z) not excluded in >= 80% of stars-only cells": f"{sum(c['H_in'] for c in Sc)}/{len(Sc)}", "H9a decision LOO-stable": str(loo_ok),
        "H9b the committed R_out H(z) exclusion flips under >= 1 LOO": f"committed R_out H(z) {'in' if rcom['H_in'] else 'OUT'}; flips when dropping {flips}",
        "H11 D1 alpha 0: no root": D1["0"]["status"], "H12 frac_F_excl < 0.5": f"{FR['frac_F_excl']:.3f}", "H1 control (i) exact": "see control (i)",
    }
    for k, v in HE.items():
        P(f"  {'HIT ' if v else 'MISS'} {k}: {detail[k]}")
    P("  H10 (MUTATE factors) is scored by the MUTATE run.")

# ================================================================================================================ outputs
grid_path = os.path.join(LANE, f"cfg308_grid{SFX}.csv")
with open(grid_path, "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["cell", "in_decision", "radius", "sample", "ids", "gas", "dMstar", "pressure", "inclination", "n", "bound", "n_floor",
                "s_A", "status_A", "unb_frac_A", "lo68_A", "hi68_A", "lo95_A", "hi95_A", "s_B", "status_B", "lo95_B", "hi95_B",
                "env_lo95", "env_hi95", "s_exp_FLAT", "s_exp_Hz", "E_zmed", "FLAT_in", "Hz_in", "Hz_in_Ezmed", "root_bearing"])
    for j, c in enumerate(cells):
        a, b = c["A"], c.get("B")
        w.writerow([j, int(not c["sample"].startswith("loo")), c["radius"], c["sample"], " ".join(c["ids"]), c["gas"], c["dMstar"], c["pressure"], c["inclination"], c["n"], c["bound"], c["n_floor"],
                    f"{a['s']:.6g}", a["status"], f"{a['unb_frac']:.4f}", f"{a['lo68']:.6g}", f"{a['hi68']:.6g}", f"{a['lo95']:.6g}", f"{a['hi95']:.6g}",
                    f"{b['s']:.6g}" if b else "", b["status"] if b else "", f"{b['lo95']:.6g}" if b else "", f"{b['hi95']:.6g}" if b else "",
                    f"{c['env95'][0]:.6g}", f"{c['env95'][1]:.6g}", f"{c['exp']['FLAT']:.6g}", f"{c['exp']['H(z)']:.6g}", f"{c['exp']['E(z_med)']:.6g}",
                    int(c["F_in"]), int(c["H_in"]), int(c["Hz_in_Ezmed"]), int(c["root_bearing"])])
npass = sum(CHK)
P(f"\n{npass}/{len(CHK)} checks pass   ({time.time() - T0:.0f} s)")


def jclean(o):
    if isinstance(o, dict):
        return {str(k): jclean(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)):
        return [jclean(v) for v in o]
    if isinstance(o, (np.floating, np.integer)):
        return o.item()
    if isinstance(o, np.bool_):
        return bool(o)
    if isinstance(o, np.ndarray):
        return o.tolist()
    return o


RES = dict(lane="CFG308", mode="MUTATE" if MUT else "main", frozen_criteria_commit="ca50d064d", frozen_criteria_sha256=sha(os.path.join(LANE, "FROZEN_CRITERIA.md")),
           n_cells=len(cells), n_decision_cells=len(DEC), n_loo_cells=sum(len(v) for v in LOO.values()),
           decision=DECISION, fractions=FR, secondary=SEC, marginals=MARG, swings=SWING, swing_H=SW_H, swing_F=SW_F, dominant_axis=DOM, dominant_axis_for_FLAT=DOM_F,
           dlog_s_extremes=DLS, loo=LOOR, loo_pooled=FR_LOO_POOL, loo_stable=loo_ok,
           committed_cells={f"{r}|{s}": dict(A=BY[(r, s, "G0", 0.0, "P_auth", 0)]["A"], B=BY[(r, s, "G0", 0.0, "P_auth", 0)].get("B"), exp=BY[(r, s, "G0", 0.0, "P_auth", 0)]["exp"],
                                             F_in=BY[(r, s, "G0", 0.0, "P_auth", 0)]["F_in"], H_in=BY[(r, s, "G0", 0.0, "P_auth", 0)]["H_in"]) for r in ("Re", "Rout") for s in ("six", "nine")},
           identity=ident, structural=dict(n=ncmp, violations=viol), diagnostic_D1=D1, mutate=MCH, hand_estimates=HE,
           inputs=dict(L_CII_20=L20, sigma_i=SIG_I, alpha_CII=ALPHA_CII, dMstar=DMS, g_obs_floor=GFLOOR),
           checks=dict(passed=npass, n=len(CHK)))
json.dump(jclean(RES), open(os.path.join(LANE, f"cfg308_cristal_stress{SFX}_results.json"), "w"), indent=1)
open(os.path.join(LANE, f"cfg308_cristal_stress{SFX}.out"), "w").write("\n".join(OUT) + "\n")
sys.exit(0 if npass == len(CHK) else 1)
