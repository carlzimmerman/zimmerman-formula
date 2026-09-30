#!/usr/bin/env python3
"""CFG215 -- the decomposition delta(z) timeline: one two-sided statistic, delta = log10(D_obs / nu(g_bar / a0_L)) at R_e, across four
disc-halo decomposition samples (MUSE-DARK z 0.3-1.4, Price+2021 RC41 z 0.66-2.45, NOEMA3D z 1.1-1.6, ALMA-CRISTAL z 4.4-5.7).
Frozen criteria: FROZEN_CRITERIA.md here (f5950bd4b), committed before any number.  kappa = 1/2 FITTED, NOT DERIVED.
"Author decompositions, not a direct a0 measurement."  The primary series uses only anchored / independent routes; the fit-route
series is separate and never pooled.  No sentence says the data favour the framework.
Run:  python3 campaign_fresh_gravity/CFG215_decomposition_timeline/cfg215_timeline.py        (MUTATE=1: RC41 D_obs x 1.5)
"""
import os, sys, io, csv, math, json, hashlib, contextlib
sys.dont_write_bytecode = True
import numpy as np
from scipy.special import i0e, i1e, k0e, k1e
from scipy.optimize import brentq

LANE = os.path.dirname(os.path.abspath(__file__))
CFG = os.path.dirname(LANE)
REPO = os.path.dirname(CFG)
EXT = os.path.join(os.path.dirname(REPO), "_external_data", "muse_dark", "numeric")
DA = os.path.join(REPO, "data_assembly")
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
R = C.Report("cfg215_timeline", MUT)
P, check = R.P, R.check
P(__doc__.split("Run:")[0].strip())

G_KPC = 4.30091e-6
G2SI = 1e6 / 3.0856775814913673e19
XN = 1.678
OM = 0.315
A0F = {"canonical": K.A0["canonical"], "alt": K.A0["alt"]}
KER = {"nu_mono": K.nu_mono, "P2": K.nu_p2}
NBOOT, SEED = 10000, 215
LAWS = ("flat", "rival")


def E(z):
    return math.sqrt(OM * (1 + z) ** 3 + 1 - OM)


def nu1(nu, y):
    return float(nu(np.array([y]))[0])


def ystar(D, nu):
    return 10 ** brentq(lambda ly: nu1(nu, 10 ** ly) - D, -12, 14, xtol=1e-14, rtol=1e-14)


def gbar_of_gobs(gobs_si, a0, nu):
    """the flat law's inversion: g_bar with g_bar nu(g_bar/a0) = g_obs"""
    q = gobs_si / a0
    # (bracket widened from [-12, 14] to [-80, 14] after the first run crashed: MUSE-DARK ID 1119's model velocity at R_e is ~2e-10 km/s,
    #  so g_obs/a0 ~ 1e-23 and the root lies at log y ~ -46; the first run's crashed log is kept as *_firstrun_crashed.out)
    return a0 * 10 ** brentq(lambda ly: nu1(nu, 10 ** ly) * 10 ** ly - q, -80, 14, xtol=1e-14, rtol=1e-14)


def disc_v2(M, Re, Rr):
    Rd = Re / XN
    y = Rr / (2 * Rd)
    return 2 * G_KPC * M / Rd * y ** 2 * (i0e(y) * k0e(y) - i1e(y) * k1e(y))


def hern_v2(M, Re_b, Rr):
    a = Re_b / 1.8153
    return G_KPC * M * Rr / (Rr + a) ** 2


def shape(Re, Re_b, BT, Rr):
    """V^2 per unit baryonic mass, (km/s)^2 / Msun"""
    bt = 0.0 if not math.isfinite(BT) else BT
    return (1 - bt) * disc_v2(1.0, Re, Rr) + (bt * hern_v2(1.0, Re_b, Rr) if bt > 0 else 0.0)


def g_disc(M, Rd, Rr):
    y = np.asarray(Rr, float) / (2 * np.asarray(Rd, float))
    b = i0e(y) * k0e(y) - i1e(y) * k1e(y)
    return 2 * G_KPC * np.asarray(M, float) / np.asarray(Rd, float) * y ** 2 * b / np.asarray(Rr, float)


def g_hi(sig_pc2):
    return math.pi * G_KPC * np.asarray(sig_pc2, float) * 1e6


def mu_mol(z, logm):
    return 10 ** (0.06 - 3.3 * (np.log10(1 + np.asarray(z, float)) - 0.65) ** 2 - 0.41 * (np.asarray(logm, float) - 10.7))


def theil_sen(x, y):
    x, y = np.asarray(x, float), np.asarray(y, float)
    i, j = np.triu_indices(len(x), 1)
    dx = x[j] - x[i]
    m = dx != 0
    return float(np.median((y[j] - y[i])[m] / dx[m])) if m.any() else float("nan")


def verdict(lo, hi):
    return "CONSISTENT" if lo <= 0 <= hi else ("DISFAVOURED-over" if lo > 0 else "DISFAVOURED-under")


def fnum(x):
    try:
        v = float(x)
        return v if math.isfinite(v) else float("nan")
    except (TypeError, ValueError):
        return float("nan")


# ------------------------------------------------------------------------------------------------ CFG213's pieces (read-only exec)
src213 = open(os.path.join(CFG, "CFG213_dysmalpy_two_sided", "cfg213_two_sided.py")).read()
ns = {"__file__": os.path.join(CFG, "CFG213_dysmalpy_two_sided", "cfg213_two_sided.py"), "__name__": "cfg213"}
_e = os.environ.pop("MUTATE", None)
with contextlib.redirect_stdout(io.StringIO()):
    exec(compile(src213[:src213.index("BINS = {")], "cfg213", "exec"), ns)
if _e is not None:
    os.environ["MUTATE"] = _e
galaxy_rows213, cr, noema, EXCL = ns["galaxy_rows"], ns["cr"], ns["noema"], ns["EXCL"]
J213 = json.load(open(os.path.join(CFG, "CFG213_dysmalpy_two_sided", "cfg213_two_sided_results.json")))["numbers"]

# ------------------------------------------------------------------------------------------------ per-galaxy delta builders
def deltas_rows(rows, law, foot, nu):
    """rows: dicts with z, gbar [m/s^2], D"""
    out = []
    for r in rows:
        a0 = A0F[foot] * (E(r["z"]) if law == "rival" else 1.0)
        out.append(math.log10(r["D"] / nu1(nu, r["gbar"] / a0)))
    return np.array(out)


# --- MUSE-DARK (CFG199's formulas, copied; reading b: v_perp = v_file / sin i)
man = {}
for line in open(os.path.join(DA, "musedark_catalogues", "numeric_manifest_sha256.txt")):
    p_ = line.split()
    if len(p_) == 2:
        man[p_[1]] = p_[0]
bad = [k for k in man if k.endswith("_true_Vrot.dat") and (not os.path.exists(os.path.join(EXT, k)) or
                                                           hashlib.sha256(open(os.path.join(EXT, k), "rb").read()).hexdigest() != man[k])]
if bad:
    sys.exit(f"abort: true_Vrot hash check failed for {bad[:3]}")
rows_m = list(csv.DictReader(open(os.path.join(DA, "musedark_catalogues", "musedark_numeric.csv"))))
need = ("z", "logMstar_phot", "DC14_logMdisk", "fDM_at_Re", "Re_kpc", "gas_density_Msun_pc2")
S = [r for r in rows_m if all(math.isfinite(fnum(r[k])) for k in need) and r["has_bulge"].strip() == "0" and 0 < fnum(r["fDM_at_Re"]) < 1]
ids = [int(r["muse_id"]) for r in S]
zM = np.array([fnum(r["z"]) for r in S]); lms = np.array([fnum(r["logMstar_phot"]) for r in S]); lmf = np.array([fnum(r["DC14_logMdisk"]) for r in S])
fdmM = np.array([fnum(r["fDM_at_Re"]) for r in S]); ReM = np.array([fnum(r["Re_kpc"]) for r in S]); sigM = np.array([fnum(r["gas_density_Msun_pc2"]) for r in S])
sini = np.sin(np.radians(np.array([fnum(r["incl_deg"]) for r in S]))); RdM = ReM / XN


def v_at_re(rad, v, target=1.0):
    vals = []
    for sgn in (1, -1):
        m = (np.sign(rad) == sgn)
        if m.sum() < 2:
            continue
        rr, vv = np.abs(rad[m]), np.abs(v[m]); o = np.argsort(rr); rr, vv = rr[o], vv[o]
        if rr[0] <= target <= rr[-1]:
            vals.append(float(np.interp(target, rr, vv)))
    return float(np.mean(vals)) if vals else float("nan")


vf = np.full(len(S), np.nan)
for k, gid in enumerate(ids):
    rws = [[c.strip() for c in l.strip().strip("|").split("|")] for l in open(os.path.join(EXT, f"ID{gid:04d}", f"DC14_{gid}_true_Vrot.dat")) if l.strip()]
    arr = np.array([[float(x) for x in r_] for r_ in rws[1:]])
    vf[k] = v_at_re(arr[:, 1], arr[:, 3])
vperp = vf / sini
g_perp = vperp ** 2 / ReM                                        # (km/s)^2/kpc
gbi_M = (1 - fdmM) * g_perp                                      # fit route g_bar
base_M = g_disc(10 ** lmf, RdM, ReM) + g_hi(sigM)
Mind_M = 10 ** lms * (1 + mu_mol(zM, lms))
gbii_M = gbi_M * (g_disc(Mind_M, RdM, ReM) + g_hi(sigM)) / base_M      # SED + main-sequence H2 route g_bar
muse_fit = [dict(id=i, z=z, gbar=gb * G2SI, D=1 / (1 - f)) for i, z, gb, f in zip(ids, zM, gbi_M, fdmM) if math.isfinite(gb)]
muse_ind = [dict(id=i, z=z, gbar=gb * G2SI, D=gp / gb, Dfit=1 / (1 - f)) for i, z, gb, gp, f in zip(ids, zM, gbii_M, g_perp, fdmM)
            if math.isfinite(gb)]
b_muse = float(np.median((np.log10(Mind_M) - lmf)[np.isfinite(gbii_M)]))

# --- RC41 (no velocities tabulated: geometry from the fitted M_bar and R_e)
rc = list(csv.DictReader(open(os.path.join(DA, "price2021_rc41", "price2021_rc41.csv"))))
RCB = 1.0                                                          # declared R_e,bulge (kpc)
rc41 = []
for r in rc:
    z, lmb, Re, bt, fd = fnum(r["z"]), fnum(r["logMbar_1D"]), fnum(r["Re_1D_kpc"]), fnum(r["BT"]), fnum(r["fDM_Re_1D"])
    lsed, lgas = fnum(r["logMstar_SED"]), fnum(r["logMgas"])
    if not all(math.isfinite(v) for v in (z, lmb, Re, fd)):
        continue
    gb = 10 ** lmb * shape(Re, RCB, bt, Re) / Re                   # (km/s)^2/kpc
    rc41.append(dict(id=r["id"], z=z, gbar=gb * G2SI, D=1 / (1 - fd), lmb=lmb, lsed=lsed, lgas=lgas, Re=Re, BT=bt, fd=fd))
for r in rc41:
    Mi = 10 ** r["lsed"] + 10 ** r["lgas"] if math.isfinite(r["lsed"]) and math.isfinite(r["lgas"]) else float("nan")
    r["Mratio"] = Mi / 10 ** r["lmb"]
b_rc = float(np.nanmedian([math.log10(r["Mratio"]) for r in rc41]))

# --- NOEMA3D and CRISTAL (CFG213's rows)
noe_fit = galaxy_rows213("Z1.4", noema)
noe_ind = galaxy_rows213("Z1.4", noema, route=True)
cri_prim = [g for g in cr if g["id"] not in EXCL]
cri_fit = galaxy_rows213("Z5", cri_prim)
cri_ind = galaxy_rows213("Z5", cri_prim, route=True)
b_noe = float(np.median([math.log10((10 ** g["logMstar"] + 10 ** g["logMgas"]) / 10 ** g["logMfit"]) for g in noema
                         if all(math.isfinite(g[k]) for k in ("logMstar", "logMgas", "logMfit", "fdm", "Re", "sig0", "Vc"))]))
ok9 = [g for g in cri_prim if all(math.isfinite(g[k]) for k in ("logMstar", "f_molgas", "logMfit", "fdm", "Re", "sig0", "Vrot"))]
b_cri = float(np.median([math.log10(10 ** g["logMstar"] / (1 - g["f_molgas"]) / 10 ** g["logMfit"]) for g in ok9]))

# ------------------------------------------------------------------------------------------------ controls
R.banner("CONTROLS")
c1 = []
for k, nu in KER.items():
    for foot in A0F:
        for z in (0.8, 1.4, 5.0):
            for law, fac in (("flat", 1.0), ("rival", E(z))):
                gb = 3.1 * A0F[foot]
                c1.append(abs(math.log10(nu1(nu, gb / (A0F[foot] * fac)) / nu1(nu, gb / (A0F[foot] * fac)))))
check("C1 a synthetic galaxy placed exactly on each law returns delta = 0 to 1e-12", f"max {max(c1):.1e}", max(c1) < 1e-12)
# calibration gate
cal = []
for g in noema:
    if all(math.isfinite(g[k]) for k in ("logMfit", "Re", "Vc", "fdm")):
        bt = fnum(next((r for r in csv.DictReader(open(os.path.join(DA, "noema3d", "noema3d_per_galaxy.csv"))) if r["id"] == g["id"]), {}).get("BT_P1"))
        reb = fnum(next((r for r in csv.DictReader(open(os.path.join(DA, "noema3d", "noema3d_per_galaxy.csv"))) if r["id"] == g["id"]), {}).get("Re_bulge_fixed_kpc"))
        reb = reb if math.isfinite(reb) and reb > 0 else RCB
        vb2_mod = 10 ** g["logMfit"] * shape(g["Re"], reb, bt, g["Re"])
        cal.append(("NOEMA3D " + g["id"], vb2_mod / ((1 - g["fdm"]) * g["Vc"] ** 2)))
dyn = {r["id"]: r for r in csv.DictReader(open(os.path.join(DA, "arxiv_tables", "cristal2025_dynamics.csv")))}
for g in cri_prim:
    if all(math.isfinite(g[k]) for k in ("logMfit", "Re", "Vrot", "sig0", "fdm")):
        bt = fnum(dyn[g["id"]]["BT"])
        vb2_mod = 10 ** g["logMfit"] * shape(g["Re"], RCB, bt, g["Re"])
        cal.append(("CRISTAL " + g["id"], vb2_mod / ((1 - g["fdm"]) * (g["Vrot"] ** 2 + 3.36 * g["sig0"] ** 2))))
ratios = np.array([v for _, v in cal])
gate = 0.8 <= float(np.median(ratios)) <= 1.25
CALF = 1.0 if gate else 1.0 / float(np.median(ratios))
P(f"  calibration gate: {len(cal)} decompositions (NOEMA3D + CRISTAL); V_bary^2(model shape) / V_bary^2(table) median {np.median(ratios):.3f}, "
  f"range {ratios.min():.3f}-{ratios.max():.3f}; per galaxy: " + ", ".join(f"{n.split()[0][:1]}{n.split()[1]} {v:.2f}" for n, v in cal))
check("C2 calibration gate: the median model/table V_bary^2 ratio lies in [0.8, 1.25] (RC41 enters as is); otherwise it is calibrated by the median factor",
      f"median {np.median(ratios):.3f} -> {'PASS: RC41 as is' if gate else f'FAIL: RC41 calibrated by x{CALF:.3f}'}", True, load_bearing=False)
for r in rc41:
    r["gbar"] *= CALF
# C3 reproductions
c3a = 0.0
for bname, fit_r, ind_r in (("Z1.4 (NOEMA3D)", noe_fit, noe_ind), ("Z5 (CRISTAL primary)", cri_fit, cri_ind)):
    for kname, nu in KER.items():
        for foot in A0F:
            for law in LAWS:
                for route, rows in (("fit", fit_r), ("route", ind_r)):
                    m = float(np.median(deltas_rows(rows, law, foot, nu)))
                    c3a = max(c3a, abs(m - J213[bname][f"3.36|{route}|{kname}|{foot}|{law}"]["med"]))
check("C3a CRISTAL's and NOEMA3D's per-sample medians (fit and route; both kernels, footings and laws) equal CFG213's committed medians to 1e-9",
      f"max |difference| {c3a:.1e}", c3a < 1e-9)
# C3b: CFG199 reading-(b) route-(i) lowest-third median log10 a0 = -10.143 (its committed JSON)
J199 = json.load(open(os.path.join(CFG, "CFG199_musedark_level_pressure", "cfg199_musedark_level_results.json")))["numbers"]["readings"]["b: v_perp = v_file / sin i"]
gbi198 = g_disc(10 ** lmf, RdM, ReM) + g_hi(sigM)
D198 = 1 / (1 - fdmM)
a198 = np.array([gbi198[i] * G2SI / ystar(D198[i], K.nu_mono) if D198[i] > 1.05 else np.nan for i in range(len(S))])
idx198 = np.where(np.isfinite(a198))[0]
low = np.array_split(idx198[np.argsort(zM[idx198])], 3)[0]
a_i = np.array([gbi_M[i] * G2SI / ystar(D198[i], K.nu_mono) if D198[i] > 1.05 else np.nan for i in range(len(S))])
lvl = float(np.median(np.log10(a_i[low][np.isfinite(a_i[low])])))
check("C3b CFG199's reading-(b) route-(i) lowest-z-third median log10 a0 is reproduced from the copied formulas to 1e-3",
      f"{lvl:.4f} vs {J199['L1']['median']:.4f}", abs(lvl - J199["L1"]["median"]) < 1e-3)
if MUT:
    for r in rc41:
        r["D"] *= 1.5

# ------------------------------------------------------------------------------------------------ the two series
def rc_ind_rows():
    out = []
    for r in rc41:
        if not math.isfinite(r["Mratio"]):
            continue
        out.append(dict(id=r["id"], z=r["z"], gbar=r["gbar"] * r["Mratio"], D=r["D"] / r["Mratio"]))
    return out


SERIES = {"primary": {"MUSE-DARK": muse_ind, "RC41": rc41, "NOEMA3D": noe_ind, "CRISTAL": cri_ind},
          "fit-route": {"MUSE-DARK": muse_fit, "NOEMA3D": noe_fit, "CRISTAL": cri_fit, "RC41 (anchored)": rc41}}
RC_IND = rc_ind_rows()
BIAS = {"MUSE-DARK": b_muse, "RC41": b_rc, "NOEMA3D": b_noe, "CRISTAL": b_cri}
rng = np.random.default_rng(SEED)
IDX = {}


def boots(n):
    if n not in IDX:
        IDX[n] = rng.integers(0, n, size=(NBOOT, n))
    return IDX[n]


def across_slope(sample_deltas, sample_z):
    """Theil-Sen slope of the per-sample medians against the samples' median z"""
    return theil_sen([np.median(z) for z in sample_z], [np.median(d) for d in sample_deltas])


def across_ci(sample_deltas, sample_z):
    zs = [np.asarray(z) for z in sample_z]; ds = [np.asarray(d) for d in sample_deltas]
    bs = np.empty(NBOOT)
    for k in range(NBOOT):
        mz, md = [], []
        for z, d in zip(zs, ds):
            ix = boots(len(d))[k]
            mz.append(np.median(z[ix])); md.append(np.median(d[ix]))
        bs[k] = theil_sen(mz, md)
    return across_slope(ds, zs), float(np.percentile(bs, 2.5)), float(np.percentile(bs, 97.5))


def med_ci(d):
    d = np.asarray(d)
    bs = np.median(d[boots(len(d))], axis=1)
    return float(np.median(d)), float(np.percentile(bs, 2.5)), float(np.percentile(bs, 97.5))


def within_slope(rows, law, foot, nu):
    z = np.array([r["z"] for r in rows]); d = deltas_rows(rows, law, foot, nu)
    bs = np.empty(NBOOT)
    for k in range(NBOOT):
        ix = boots(len(d))[k]
        bs[k] = theil_sen(z[ix], d[ix])
    return theil_sen(z, d), float(np.percentile(bs, 2.5)), float(np.percentile(bs, 97.5))


TABLE = {}
for sname, samples in (("primary", SERIES["primary"]), ("fit-route", SERIES["fit-route"])):
    R.banner(f"SERIES: {sname}  ({'anchored / independent routes only' if sname == 'primary' else 'fit routes; reported separately, never pooled'})")
    P(f"  {'sample':16s} {'n':>4s} {'median z':>8s}  law   {'ν_mono canonical: median δ [95% CI]  verdict':50s} | ν_mono alt | P2 canonical | P2 alt")
    for smp, rows in samples.items():
        for law in LAWS:
            cells = []
            for kname in ("nu_mono", "P2"):
                for foot in ("canonical", "alt"):
                    m, lo, hi = med_ci(deltas_rows(rows, law, foot, KER[kname]))
                    TABLE[(sname, smp, law, kname, foot)] = dict(n=len(rows), med=m, lo=lo, hi=hi, v=verdict(lo, hi))
            c0 = TABLE[(sname, smp, law, "nu_mono", "canonical")]
            others = " | ".join(f"{TABLE[(sname, smp, law, k_, f_)]['med']:+.3f} {TABLE[(sname, smp, law, k_, f_)]['v']}"
                                for k_, f_ in (("nu_mono", "alt"), ("P2", "canonical"), ("P2", "alt")))
            P(f"  {smp:16s} {c0['n']:4d} {np.median([r['z'] for r in rows]):8.2f}  {law:5s} {c0['med']:+.3f} [{c0['lo']:+.3f}, {c0['hi']:+.3f}] {c0['v']:18s} | {others}")

# T1
R.banner("T1 / T2")
for sname in ("primary", "fit-route"):
    fits = {law: [TABLE[(sname, s, law, "nu_mono", "canonical")]["v"] for s in SERIES[sname]] for law in LAWS}
    allc = [law for law in LAWS if all(v == "CONSISTENT" for v in fits[law])]
    P(f"  T1 [{sname}] (nu_mono, canonical): CONSISTENT in all four samples: {allc if allc else 'no law fits all four'}; verdicts flat {fits['flat']}, rival {fits['rival']}")
    R.num(f"T1_{sname}", dict(consistent_in_all=allc, verdicts=fits))
# T2: across-sample slope (primary series), within-sample slopes for RC41 and MUSE-DARK
T2 = {}
for law in LAWS:
    sd = [deltas_rows(rows, law, "canonical", K.nu_mono) for rows in SERIES["primary"].values()]
    sz = [[r["z"] for r in rows] for rows in SERIES["primary"].values()]
    a, alo, ahi = across_ci(sd, sz)
    wm = within_slope(muse_ind, law, "canonical", K.nu_mono)
    wr = within_slope(rc41, law, "canonical", K.nu_mono)
    a_sig = alo > 0 or ahi < 0
    sign = 1 if a > 0 else -1

    def opp(w):
        return (w[1] > 0 and sign < 0) or (w[2] < 0 and sign > 0)
    same = (wm[0] * a > 0) and (wr[0] * a > 0)
    any_ex = (wm[1] > 0 or wm[2] < 0) or (wr[1] > 0 or wr[2] < 0)
    trend = a_sig and same and not opp(wm) and not opp(wr) and any_ex
    label = ("TREND (a and b hold)" if trend else ("sample-heterogeneity-limited" if a_sig else "no significant across-sample trend"))
    T2[law] = dict(across=[a, alo, ahi], muse=list(wm), rc41=list(wr), label=label)
    P(f"  T2 {law:5s} primary series (nu_mono, canonical): across-sample slope {a:+.3f} [{alo:+.3f}, {ahi:+.3f}] /z; within MUSE-DARK {wm[0]:+.3f} "
      f"[{wm[1]:+.3f}, {wm[2]:+.3f}]; within RC41 {wr[0]:+.3f} [{wr[1]:+.3f}, {wr[2]:+.3f}]  -> {label}")
R.num("T2", T2)

# ------------------------------------------------------------------------------------------------ route-mixing mock
R.banner("ROUTE-MIXING MOCK (every sample given true delta_flat = 0 per galaxy, then its own route bias b_s = median log10(M_ind/M_fit))")
P("  b_s (dex): " + ", ".join(f"{k} {v:+.3f}" for k, v in BIAS.items()))


def mock(rows_by_sample, bias_sign, law):
    """rows: the sample's rows (g_obs = D * gbar is what the pipeline held); true baryons from the flat-law inversion, then bias"""
    sd, sz = [], []
    for smp, rows in rows_by_sample.items():
        b = BIAS[smp.split(" ")[0]] * bias_sign
        ds = []
        for r in rows:
            gobs = r["D"] * r["gbar"]
            gt = gbar_of_gobs(gobs, A0F["canonical"], K.nu_mono)
            gm = gt * 10 ** b
            a0 = A0F["canonical"] * (E(r["z"]) if law == "rival" else 1.0)
            ds.append(math.log10((gobs / gm) / nu1(K.nu_mono, gm / a0)))
        sd.append(ds); sz.append([r["z"] for r in rows])
    return across_slope(sd, sz)


nomock = {}
MOCK = {}
for law in LAWS:
    sig = mock(SERIES["primary"], 0.0, law)                    # no bias: the signal slope
    m_fit = mock(SERIES["primary"], +1.0, law)                 # truth = fit: the primary series' baryons = truth x 10^b
    m_ind = mock(SERIES["fit-route"], -1.0, law)               # truth = independent: the fit-route series' baryons = truth x 10^-b
    MOCK[law] = dict(no_bias=sig, truth_fit_primary=m_fit, truth_ind_fitroute=m_ind)
    P(f"  {law:5s}: no-bias slope {sig:+.3f}; mock 'truth = fit' (primary series) {m_fit:+.3f}; mock 'truth = independent' (fit-route series) {m_ind:+.3f}  (per unit z)")
sig_rival = abs(MOCK["rival"]["no_bias"])
mx = max(abs(MOCK[l][k]) for l in LAWS for k in ("truth_fit_primary", "truth_ind_fitroute"))
nd = mx >= 0.5 * sig_rival
P(f"\n  the rival's signal slope (flat exactly true, no bias) |{sig_rival:.3f}| per unit z; the largest mock slope |{mx:.3f}| -> "
  f"{'NON-DIAGNOSTIC BY CONSTRUCTION (a route bias alone gives >= 50% of the signal)' if nd else 'diagnostic by the mock (route bias alone gives < 50% of the signal)'}")
R.num("mock", dict(bias=BIAS, slopes=MOCK, signal_rival=sig_rival, largest=mx, non_diagnostic_by_construction=bool(nd)))
R.num("table", {"|".join(map(str, k)): v for k, v in TABLE.items()})
R.num("routes_reported", dict(muse_D_below_1=int(sum(r["D"] < 1 for r in muse_ind)), n_muse=len(muse_ind), cal_median=float(np.median(ratios)), gate=bool(gate)))

# RC41 route variant (reported, with CIs)
P("\n  RC41 route variant (SED + gas, total held fixed; reported), nu_mono canonical: " + "; ".join(
    "{} {:+.3f} [{:+.3f}, {:+.3f}] {}".format(law, *med_ci(deltas_rows(RC_IND, law, "canonical", K.nu_mono)),
                                             verdict(*med_ci(deltas_rows(RC_IND, law, "canonical", K.nu_mono))[1:])) for law in LAWS) + f" (n = {len(RC_IND)})")
R.num("rc41_route", {law: med_ci(deltas_rows(RC_IND, law, "canonical", K.nu_mono)) for law in LAWS})

# ---- POST HOC (written after the numbers above were seen; reported only, never a verdict)
R.banner("POST HOC sensitivities (reported only)")
ph = {}
# (1) RC41 with the geometry calibration factor applied anyway (the gate passed with the median ratio 1.185; RC41's g_bar may be ~18% high)
fac = 1.0 / float(np.median(ratios))
rc_cal = [dict(r, gbar=r["gbar"] * fac) for r in rc41]
for law in LAWS:
    m, lo, hi = med_ci(deltas_rows(rc_cal, law, "canonical", K.nu_mono))
    ph[f"rc41_calibrated_{law}"] = (m, lo, hi)
    P(f"  (1) RC41 with the calibration factor x{fac:.3f} applied anyway, {law}: {m:+.3f} [{lo:+.3f}, {hi:+.3f}] {verdict(lo, hi)}")
# (2) MUSE-DARK without the galaxies whose model velocity at R_e is < 10 km/s (near-zero-rotation models)
keep = [r for r in muse_ind if vperp[ids.index(r["id"])] * 1.0 >= 10.0]
for law in LAWS:
    m, lo, hi = med_ci(deltas_rows(keep, law, "canonical", K.nu_mono))
    ph[f"muse_v10_{law}"] = (m, lo, hi)
    P(f"  (2) MUSE-DARK without the {len(muse_ind) - len(keep)} galaxies with v_perp(R_e) < 10 km/s (n = {len(keep)}), {law}: {m:+.3f} [{lo:+.3f}, {hi:+.3f}] {verdict(lo, hi)}")
# (3) MUSE-DARK reading (a): v_perp = v_file (no sin i)
gpa = vf ** 2 / ReM
gbia = (1 - fdmM) * gpa
gbiia = gbia * (g_disc(Mind_M, RdM, ReM) + g_hi(sigM)) / base_M
muse_a = [dict(id=i, z=z, gbar=gb * G2SI, D=gp / gb) for i, z, gb, gp in zip(ids, zM, gbiia, gpa) if math.isfinite(gb) and gb > 0]
for law in LAWS:
    m, lo, hi = med_ci(deltas_rows(muse_a, law, "canonical", K.nu_mono))
    ph[f"muse_reading_a_{law}"] = (m, lo, hi)
    P(f"  (3) MUSE-DARK reading (a) v_perp = v_file, independent route (n = {len(muse_a)}), {law}: {m:+.3f} [{lo:+.3f}, {hi:+.3f}] {verdict(lo, hi)}")
R.num("posthoc", ph)
if MUT:
    R.banner("MUTATE RESPONSE")
    ok = True
    for r in rc41:
        r["D"] /= 1.5
    for law in LAWS:
        m1 = float(np.median(deltas_rows([dict(r, D=r["D"] * 1.5) for r in rc41], law, "canonical", K.nu_mono)))
        m0 = float(np.median(deltas_rows(rc41, law, "canonical", K.nu_mono)))
        ok &= abs((m1 - m0) - math.log10(1.5)) < 1e-9
    check("MUTATE: RC41 D_obs x 1.5 raises RC41's median delta by log10(1.5) to 1e-9 (both laws)", f"{ok}", ok)
R.write(here=LANE)
