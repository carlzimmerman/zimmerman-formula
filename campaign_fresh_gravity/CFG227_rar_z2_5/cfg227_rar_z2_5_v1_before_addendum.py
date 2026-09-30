#!/usr/bin/env python3
"""CFG227 -- the first compiled radial-acceleration relation (RAR) at z = 2-5 from tabulated kinematics and baryons.  Compilation; conversions as published; calibration-limited; author decompositions and tables;
not a detection.  LambdaCDM has no a0: the proxy is an effective-a0 PROXY.  kappa = 1/2 FITTED.  No sentence says the data favour a law.
Frozen criteria: FROZEN_CRITERIA.md here (e09ca6b74), committed before any g_obs, g_bar or delta of this lane was computed.
Run: python3 campaign_fresh_gravity/CFG227_rar_z2_5/cfg227_rar_z2_5.py        (MUTATE=1: g_obs x 1.5 at every point)"""
import os, sys, io, csv, json, math, tempfile, contextlib, time
sys.dont_write_bytecode = True
import numpy as np
from scipy.optimize import brentq
from scipy.integrate import quad
from scipy.special import i0e, i1e, k0e, k1e

LANE = os.path.dirname(os.path.abspath(__file__))
CFG = os.path.dirname(LANE)
REPO = os.path.dirname(CFG)
MUT = os.environ.pop("MUTATE", "").strip() == "1"            # the exec'd lane prefixes must not see MUTATE
sys.path.insert(0, CFG)
import CFG4_common as K
Z1DIR = os.path.join(REPO, "sonnet55_push", "puzzle_32pi", "agents", "Z1_causal_horizon_a0z")
sys.path.insert(0, Z1DIR)
import zcommon as Z1                                          # READ-ONLY: lcdm_native
OUT, CHK = [], []
T0 = time.time()


def P(s=""):
    print(s, flush=True); OUT.append(s)


def check(name, val, ok):
    CHK.append(bool(ok)); P(f"  [{'PASS' if ok else 'FAIL'}] {name}: {val}")


G2SI = 1e6 / 3.0856775814913673e19                            # (km/s)^2 per kpc -> m/s^2
G_KPC = 4.30091e-6                                            # kpc (km/s)^2 / Msun
XN = 1.678
OM = 0.315
NB, SEED = 10000, 227
KER = {"nu_mono": K.nu_mono, "P2": K.nu_p2}
A0F = {"canonical": K.A0["canonical"], "alt": K.A0["alt"]}
NU, A0L = KER["nu_mono"], A0F["canonical"]
TAB = ("FLAT", "PROXY", "H(z)", "M-DEC")
P(__doc__.split("Run:")[0].strip())


def E(z):
    return math.sqrt(OM * (1 + z) ** 3 + 1 - OM)


def R_dec(z, w0=-0.838, wa=-0.62):
    return math.sqrt((1.0 + z) ** (3.0 * (1.0 + w0 + wa)) * math.exp(-3.0 * wa * z / (1.0 + z)))


LAWS = {"FLAT": lambda z: 1.0, "PROXY": lambda z: Z1.lcdm_native(z), "H(z)": E, "M-DEC": R_dec}


def Farr(law, z):
    return np.array([LAWS[law](float(zz)) for zz in np.atleast_1d(z)])


def kpc_per_arcsec(z, H0=67.4, Om=OM):
    c = 299792.458
    dc = c / H0 * quad(lambda x: 1 / math.sqrt(Om * (1 + x) ** 3 + 1 - Om), 0, z)[0]            # Mpc
    return dc / (1 + z) * 1e3 * math.pi / 648000.0


def disc_v2(M, Re, Rr):                                        # CFG216's thin exponential disc (Freeman), (km/s)^2; Re, Rr in kpc
    Rd = Re / XN
    y = Rr / (2 * Rd)
    return 2 * G_KPC * M / Rd * y ** 2 * (i0e(y) * k0e(y) - i1e(y) * k1e(y))


def gdisc(M, Re, r):                                           # m/s^2
    return disc_v2(M, Re, r) / r * G2SI


# ---- machinery copied VERBATIM from the committed CFG222 script (nu1, gbar_of_gobs, delta_arr, load_rc100, exec_lane, rows_Re, rows_Rout)
RC_PATH = {"committed": os.path.join(REPO, "real_research", "data", "rc100_nestorshachar2023_table3.csv"),
           "corrected": os.path.join(REPO, "data_assembly", "rc100_provenance", "rc100_table3_six_fields_paper_values.csv")}


def nu1(nu, y):
    return float(nu(np.array([y]))[0])


def gbar_of_gobs(gobs, a0t, nu):
    q = gobs / a0t
    return a0t * 10 ** brentq(lambda ly: nu1(nu, 10 ** ly) * 10 ** ly - q, -80, 14, xtol=1e-14, rtol=1e-14)


def delta_arr(D, gb, Fa, a0, nu):
    return np.log10(D / nu(gb / (a0 * Fa)))


def load_rc100(path, mutate=False):
    z, D, gb, go = [], [], [], []
    for r in csv.DictReader(open(path, newline="")):
        zz, Re, Vc, fd = (float(r[k]) for k in ("z", "Re_kpc", "Vc_Re_kms", "fDM_within_Re"))
        if all(math.isfinite(v) for v in (zz, Re, Vc, fd)) and 0 < fd < 1:
            g = Vc ** 2 / Re * G2SI
            z.append(zz); go.append(g); gb.append((1 - fd) * g); D.append(1 / (1 - fd))
    z, D, gb, go = map(np.array, (z, D, gb, go))
    if mutate:
        D = D * 10 ** (0.2 * (z - np.median(z)))
    return dict(z=z, D=D, gb=gb, go=go)


def exec_lane(rel, stop):
    path = os.path.join(CFG, rel)
    src = open(path).read()
    ns = {"__file__": path, "__name__": "lane"}
    with contextlib.redirect_stdout(io.StringIO()):
        exec(compile(src[:src.index(stop)], rel, "exec"), ns)
    return ns


n213 = exec_lane("CFG213_dysmalpy_two_sided/cfg213_two_sided.py", "BINS = {")
n220 = exec_lane("CFG220_cristal_outer_independent/cfg220_outer_independent.py", "# ------------------------------------------------------------------------------------------------ controls")
cr, EXCL, galaxy_rows213 = n213["cr"], n213["EXCL"], n213["galaxy_rows"]
rows_for220, DET, byid = n220["rows_for"], n220["DET"], n220["byid"]
crbyid = {g["id"]: g for g in cr}


def rows_Re(ids, route, tau=0.0, mutate=False):
    """CRISTAL at R_e (CFG213's Z5 rows); route 'fit' (as galaxy_rows) or 'ind' (M_ind(tau) = M* + M_gas 10^tau, V_c and f_DM as the authors')."""
    out = []
    for i in ids:
        g = crbyid[i]
        if route == "fit":
            r = galaxy_rows213("Z5", [g], alpha=3.36, route=False, mutate=mutate)
            out.extend(r)
            continue
        if not all(math.isfinite(g[k]) for k in ("fdm", "Re", "sig0", "z", "Vrot", "logMstar", "f_molgas", "logMfit")):
            continue
        vc2_ad = g["Vrot"] ** 2 + 3.36 * g["sig0"] ** 2
        gbar0 = (1 - g["fdm"]) * vc2_ad / g["Re"] * G2SI
        Ms = 10 ** g["logMstar"]; Mind = Ms + Ms * g["f_molgas"] / (1 - g["f_molgas"]) * 10 ** tau
        gbar = gbar0 * Mind / 10 ** g["logMfit"]
        D = (vc2_ad / g["Re"] * G2SI) / gbar * (1.5 if mutate else 1.0)
        out.append(dict(id=i, z=g["z"], gbar=gbar, D=D))
    return out


def rows_Rout(rdef, ids, route, tau=0.0, mutate=False):
    return [dict(id=r["id"], z=r["z"], gbar=r["gbar"], D=r["D"]) for r in rows_for220(rdef, ids, route, tau=tau, mutate=mutate)]



def ts(x, y):
    i, j = np.triu_indices(len(x), 1)
    dx = x[j] - x[i]; m = dx != 0
    return float(np.median((y[j] - y[i])[m] / dx[m]))



# ------------------------------------------------------------------------------------------------ data
AT = os.path.join(REPO, "data_assembly", "arxiv_tables")


def rd(path):
    return list(csv.DictReader(open(path, newline="")))


def f(x):
    try:
        v = float(str(x).strip())
        return v if math.isfinite(v) else float("nan")
    except (TypeError, ValueError):
        return float("nan")


J224B = json.load(open(os.path.join(CFG, "CFG224_gas_calibration", "cfg224b_conversion_drift_results.json")))
K_IN = {"B3": J224B["primary"]["ad|alpha_CO|B3 1.6<=z<3.0"]["K_local"], "B4": J224B["primary"]["ad|alpha_CO|B4 z>=3.0"]["K_local"]}
K_OUT = J224B["ace"]["K"]


def zbin(z):
    return "B3" if z < 3.0 else "B4"


PTS = []
GM = 1.5 if MUT else 1.0                                        # MUTATE multiplies g_obs


def add(set_, gid, z, r, V, eV, gobs, gbar, gstar, ggas, sgo=float("nan"), sgb=float("nan"), limit=False, group=None, extra=None):
    PTS.append(dict(set=set_, id=gid, z=z, r=r, V=V, eV=eV, gobs=gobs * GM, gbar=gbar, gstar=gstar, ggas=ggas, sgo=sgo, sgb=sgb, limit=limit, group=group or set_, extra=extra or {}))


# S1 Amvrosiadis+25
par = {r["alessid"]: r for r in rd(os.path.join(AT, "amvrosiadis_parent.csv"))}
for b in rd(os.path.join(AT, "amvrosiadis_bestfit.csv")):
    p = par[b["alessid"]]; z = f(p["z"])
    if not (2.0 <= z <= 5.0):
        continue
    re_kpc = f(b["re_arcsec"]) * kpc_per_arcsec(z); r = 2 * re_kpc
    V = f(b["vcirc_2re_kms"]); eV = 0.5 * (f(b["vcirc_2re_kms_errhi"]) + f(b["vcirc_2re_kms_errlo"]))
    Ms, Mg = 10 ** f(p["logMstar"]), 10 ** f(p["logMgas_msun"])
    eMs, eMg = 0.5 * (f(p["logMstar_errhi"]) + f(p["logMstar_errlo"])), f(p["logMgas_err"])
    gs, gg = gdisc(Ms, re_kpc, r), gdisc(Mg, re_kpc, r)
    sM = math.sqrt((Ms * math.log(10) * eMs) ** 2 + (Mg * math.log(10) * eMg) ** 2)
    add("S1 Amvrosiadis", b["alessid"], z, r, V, eV, V ** 2 / r * G2SI, gs + gg, gs, gg, 2 * 0.4343 * eV / V, 0.4343 * sM / (Ms + Mg), extra=dict(re_kpc=re_kpc, logMs=f(p["logMstar"]), logMg=f(p["logMgas_msun"])))
# S2 CRISTAL: the committed CFG213 / CFG220 rows (n213 / n220 and rows_Re / rows_Rout are defined by the copied machinery)
ids12 = [g["id"] for g in cr if g["id"] not in EXCL]
six = list(DET)
CR = [("CRISTAL R_e fit (12)", rows_Re(ids12, "fit")), ("CRISTAL R_e independent (6)", rows_Re(six, "ind")),
      ("CRISTAL R_out fit (6)", rows_Rout("table_Rout", six, "fit")), ("CRISTAL R_out independent (6)", rows_Rout("table_Rout", six, "ind"))]
for gname, rows in CR:
    for r_ in rows:
        fm = f(crbyid[r_["id"]].get("f_molgas"))
        gb = r_["gbar"]
        add("S2 CRISTAL", r_["id"], r_["z"], float("nan"), float("nan"), float("nan"), gb * r_["D"], gb, (1 - fm) * gb if math.isfinite(fm) else float("nan"), fm * gb if math.isfinite(fm) else float("nan"), group=gname, extra=dict(f_molgas=fm))
# S3 ALPAKA I: stars-only LOWER LIMITS on g_bar at R_ext
samp = {r["id"]: r for r in rd(os.path.join(AT, "alpaka1_sample.csv"))}
kin = {r["id"]: r for r in rd(os.path.join(AT, "alpaka1_kinematics.csv"))}
prop = {r["id"]: r for r in rd(os.path.join(AT, "alpaka1_properties.csv"))}
outer = {r["id"]: r for r in rd(os.path.join(AT, "alpaka1_digitised", "alpaka1_outer_summary.csv"))}
ALP_LIST = []
for i, k_ in kin.items():
    z = f(samp[i]["z"])
    if z < 2.0:
        continue
    ALP_LIST.append(i)
    r = f(outer[i]["R_ext_kpc"]); V = f(k_["vext_kms"]); eV = 0.5 * (f(k_["vext_errhi"]) + f(k_["vext_errlo"]))
    Ms = f(prop[i]["mstar_1e10msun"]) * 1e10
    if not math.isfinite(Ms):
        continue
    Re = f(outer[i]["Re_kpc_dashed_line"])
    Re = Re if math.isfinite(Re) else r / 1.2
    Lp = f(prop[i]["lprime_1e10_kkmspc2"]) * 1e10
    gs = gdisc(Ms, Re, r)
    add("S3 ALPAKA (stars-only limit)", i, z, r, V, eV, V ** 2 / r * G2SI, gs, gs, 0.0, 2 * 0.4343 * eV / V, float("nan"), limit=True,
        extra=dict(Re_kpc=Re, g_incl_0p8=gdisc(Ms + 0.8 * Lp, Re, r) if math.isfinite(Lp) else float("nan"), g_incl_4p36=gdisc(Ms + 4.36 * Lp, Re, r) if math.isfinite(Lp) else float("nan")))
# S4 RC100 corrected table, z >= 2 (authors' decomposition; the low-information grey set)
d4 = load_rc100(RC_PATH["corrected"])
for z_, go_, gb_ in zip(d4["z"], d4["go"], d4["gb"]):
    if z_ >= 2.0:
        add("S4 RC100 (z >= 2)", "rc", float(z_), float("nan"), float("nan"), float("nan"), float(go_), float(gb_), float("nan"), float("nan"), group="S4 RC100 (z >= 2)")
P(f"\nPOINTS: S1 {sum(p['set'].startswith('S1') for p in PTS)}; S2 {sum(p['set'].startswith('S2') for p in PTS)} (groups {[len(r) for _, r in CR]}); S3 {sum(p['set'].startswith('S3') for p in PTS)} of {len(ALP_LIST)} ALPAKA discs with z >= 2; S4 {sum(p['set'].startswith('S4') for p in PTS)}")
P(f"gas-calibration bands from CFG224b: inner K_local of alpha_CO B3 {K_IN['B3']:.3f}, B4 {K_IN['B4']:.3f}; outer K_ACE {K_OUT:.3f}")


# ------------------------------------------------------------------------------------------------ deltas, bands, medians
def delta_of(gobs, gbar, z, law, cell=("nu_mono", "canonical")):
    nu, a0 = KER[cell[0]], A0F[cell[1]]
    return np.log10(gobs / (gbar * nu(gbar / (a0 * Farr(law, z)))))


IDX = {}


def med_ci(d):
    n = len(d)
    if n not in IDX:
        IDX[n] = np.random.default_rng(SEED * 1000 + n).integers(0, n, size=(NB, n))
    bs = np.median(d[IDX[n]], axis=1)
    return float(np.median(d)), float(np.percentile(bs, 2.5)), float(np.percentile(bs, 97.5))


def gbar_tau(p, tau):
    if not (math.isfinite(p["gstar"]) and math.isfinite(p["ggas"])) or p["limit"]:
        return p["gbar"]
    return p["gstar"] + p["ggas"] * 10 ** tau


GROUPS = []
for p in PTS:
    if p["group"] not in GROUPS:
        GROUPS.append(p["group"])
GROUPS = [g for g in GROUPS if not g.startswith("S3")]
P("\nPOINT TABLES are in cfg227_points.csv; GROUP MEDIANS of delta_L (nu_mono, canonical; 95% bootstrap interval; the lower limits of S3 enter no median), with the gas-mass shifts of the bands")
RES = {}
for g in GROUPS:
    sel = [p for p in PTS if p["group"] == g]
    z = np.array([p["z"] for p in sel]); go = np.array([p["gobs"] for p in sel]); gb = np.array([p["gbar"] for p in sel])
    hasgas = np.array([math.isfinite(p["gstar"]) and math.isfinite(p["ggas"]) for p in sel])
    P(f"\n  {g}  (n = {len(sel)}, z {z.min():.2f} to {z.max():.2f}; {int(hasgas.sum())} with a gas component for the bands)")
    RES[g] = {}
    for law in TAB:
        m, lo, hi = med_ci(delta_of(go, gb, z, law))
        bands = {}
        if hasgas.any():
            for nm, tau in (("-outer", None), ("-inner", None), ("+inner", None), ("+outer", None)):
                pass
            for lab, sgn, K in (("-outer", -1, None), ("-inner", -1, "in"), ("+inner", 1, "in"), ("+outer", 1, None)):
                taus = np.array([sgn * (K_IN[zbin(p["z"])] if K == "in" else K_OUT) for p in sel])
                gbt = np.array([gbar_tau(p, t) for p, t in zip(sel, taus)])
                bands[lab] = float(np.median(delta_of(go, gbt, z, law)))
        RES[g][law] = dict(median=m, lo=lo, hi=hi, bands=bands)
        bs = ("   bands: " + "  ".join(f"{k} {v:+.3f}" for k, v in bands.items())) if bands else "   (no gas component: no band)"
        P(f"    {law:6s} median {m:+.3f} [{lo:+.3f}, {hi:+.3f}]{bs}")

# ------------------------------------------------------------------------------------------------ controls
P("\nCONTROLS")
S1 = [p for p in PTS if p["set"].startswith("S1")]
alp_with = sum(1 for p in PTS if p["set"].startswith("S3"))
check("C1 counts: S1 nine; ALPAKA ten discs at z >= 2 of which nine carry M*; CRISTAL groups 12 / 6 / 6 / 6; S4 the RC100 corrected rows at z >= 2 (reported)", f"S1 {len(S1)}; ALPAKA {len(ALP_LIST)} / {alp_with}; CRISTAL {[len(r) for _, r in CR]}; S4 {sum(p['set'].startswith('S4') for p in PTS)}",
      len(S1) == 9 and len(ALP_LIST) == 10 and alp_with == 9 and [len(r) for _, r in CR] == [12, 6, 6, 6])
mx, nz, tot = 0.0, 0, 0
for law in TAB:
    for p in S1:
        ga = p["gbar"] * NU(np.array([p["gbar"] / (A0L * LAWS[law](p["z"]))]))[0] * A0L * 0 + p["gbar"] * float(NU(np.array([p["gbar"] / (A0L * LAWS[law](p["z"]))]))[0])     # g_obs exactly on law L
        V = math.sqrt(ga * p["r"] / G2SI); go = V ** 2 / p["r"] * G2SI                                                                                                              # through the observable V and r
        mx = max(mx, abs(float(delta_of(np.array([go]), np.array([p["gbar"]]), np.array([p["z"]]), law)[0])))
        for other in TAB:
            if other != law:
                tot += 1; nz += int(abs(float(delta_of(np.array([go]), np.array([p["gbar"]]), np.array([p["z"]]), other)[0])) > 1e-3)
check("C2 non-vacuous placement: S1 galaxies with g_obs set exactly on each law through V and r give delta_L = 0 under their own law and |delta| > 1e-3 under the other laws in >= 90% of the rows", f"max |delta| {mx:.1e}; other-law sensitivity {100 * nz / tot:.0f}%", mx < 1e-9 and nz / tot >= 0.90)
rr = np.linspace(0.05, 20, 4000); v2 = np.array([disc_v2(1.0, XN, x) for x in rr]) / (G_KPC * 1.0 / 1.0)
far = disc_v2(1.0, XN, 50.0) / (G_KPC / 50.0)
check("C3 the disc function: Freeman's peak V^2 = 0.3872 G M / R_d to 0.003 and V^2 -> G M / r far away (r = 50 R_d) to 1e-3", f"peak {v2.max():.4f}; far field ratio {far:.5f}", abs(v2.max() - 0.3872) < 0.003 and abs(far - 1) < 1e-3)
ok4 = True
for law in TAB:
    for p in S1:
        d3 = [float(delta_of(np.array([p["gobs"]]), np.array([gbar_tau(p, t)]), np.array([p["z"]]), law)[0]) for t in (0.3, 0.0, -0.3)]
        ok4 &= d3[0] < d3[1] < d3[2]
check("C4 band direction: raising the gas mass raises g_bar and lowers every delta_L at every S1 point (tau = +0.3 < 0 < -0.3)", f"{ok4}", ok4)
J222 = json.load(open(os.path.join(CFG, "CFG222_lcdm_proxy", "cfg222_lcdm_proxy_results.json")))["main"]
L222 = {"CRISTAL R_e fit (12)": "CRISTAL R_e, fit route, n = 12", "CRISTAL R_e independent (6)": "CRISTAL R_e, independent route, six class-A", "CRISTAL R_out fit (6)": "CRISTAL R_out, fit route, six", "CRISTAL R_out independent (6)": "CRISTAL R_out, independent route, six"}
c5 = max(abs(RES[g][law]["median"] - J222[L222[g]][law]["stat"]) for g in L222 for law in ("FLAT", "H(z)")) if not MUT else 0.0
J216 = json.load(open(os.path.join(CFG, "CFG216_rc100_within_sample", "cfg216_rc100_corrected_results.json")))["numbers"]["results"]
d_all = delta_arr(d4["D"], d4["gb"], np.ones(len(d4["z"])), A0L, NU)
c5b = abs(ts(d4["z"], d_all) - J216["nu_mono|canonical|flat"]["slope"])
check("C5 the CRISTAL group medians of delta_FLAT and delta_H(z) equal CFG222's committed values to 1e-9 and the RC100 corrected loader reproduces CFG216's committed FLAT slope", f"CRISTAL max |difference| {c5:.1e}; RC100 slope difference {c5b:.1e}", (c5 < 1e-9 or MUT) and c5b < 1e-9)
if MUT:
    ok = True
    for law in TAB:
        d1 = np.array([float(delta_of(np.array([p["gobs"]]), np.array([p["gbar"]]), np.array([p["z"]]), law)[0]) for p in PTS])
        d0 = np.array([float(delta_of(np.array([p["gobs"] / 1.5]), np.array([p["gbar"]]), np.array([p["z"]]), law)[0]) for p in PTS])
        ok &= float(np.max(np.abs((d1 - d0) - math.log10(1.5)))) < 1e-9
    check("MUTATE g_obs x 1.5 at every point shifts every delta_L by +0.176 to 1e-9 and leaves g_bar unchanged", f"{ok}", ok)
    open(os.path.join(LANE, "cfg227_rar_z2_5_MUTATE.out"), "w").write("\n".join(OUT) + "\n")
    sys.exit(0 if all(CHK) else 1)

# ------------------------------------------------------------------------------------------------ outputs
P(f"\n{sum(CHK)}/{len(CHK)} controls pass; {time.time() - T0:.0f} s")
P("Reading rule: compilation; conversions as published; calibration-limited; the S1 / S3 baryon models are ours (thin exponential discs, the tabulated R_e for stars and gas); ALPAKA points are stars-only lower limits on g_bar; LambdaCDM has no a0; no sentence says the data favour a law.")
with open(os.path.join(LANE, "cfg227_points.csv"), "w", newline="") as fh:
    w = csv.writer(fh)
    w.writerow(["set", "group", "id", "z", "r_kpc", "V_kms", "eV_kms", "g_obs", "g_bar", "D", "sig_log_gobs", "sig_log_gbar", "lower_limit_on_gbar", "f_gas_of_gbar"] + [f"delta_{l}" for l in TAB] + ["g_bar_inner_minus", "g_bar_inner_plus", "g_bar_outer_minus", "g_bar_outer_plus", "g_bar_incl_gas_alpha0.8", "g_bar_incl_gas_alpha4.36"])
    for p in PTS:
        kin_ = K_IN[zbin(p["z"])]
        bands = [gbar_tau(p, -kin_), gbar_tau(p, kin_), gbar_tau(p, -K_OUT), gbar_tau(p, K_OUT)]
        fg = p["ggas"] / p["gbar"] if (math.isfinite(p["ggas"]) and not p["limit"]) else float("nan")
        w.writerow([p["set"], p["group"], p["id"], f"{p['z']:.4f}", f"{p['r']:.3f}", f"{p['V']:.1f}", f"{p['eV']:.1f}", f"{p['gobs']:.4e}", f"{p['gbar']:.4e}", f"{p['gobs'] / p['gbar']:.4f}", f"{p['sgo']:.4f}", f"{p['sgb']:.4f}", int(p["limit"]), f"{fg:.3f}"]
                   + [f"{float(delta_of(np.array([p['gobs']]), np.array([p['gbar']]), np.array([p['z']]), l)[0]):+.4f}" for l in TAB] + [f"{b:.4e}" for b in bands]
                   + [f"{p['extra'].get('g_incl_0p8', float('nan')):.4e}", f"{p['extra'].get('g_incl_4p36', float('nan')):.4e}"])
lines = ["| group | n | z range | median delta_FLAT [95%] | delta_PROXY | delta_H(z) | delta_M-DEC | FLAT with gas +-inner / +-outer |", "|---|---|---|---|---|---|---|---|"]
for g in GROUPS:
    sel = [p for p in PTS if p["group"] == g]; z = [p["z"] for p in sel]; r_ = RES[g]
    b = r_["FLAT"]["bands"]
    bs = (f"{b['-inner']:+.2f} / {b['+inner']:+.2f}; {b['-outer']:+.2f} / {b['+outer']:+.2f}") if b else "no gas component"
    lines.append(f"| {g} | {len(sel)} | {min(z):.2f}-{max(z):.2f} | {r_['FLAT']['median']:+.3f} [{r_['FLAT']['lo']:+.3f}, {r_['FLAT']['hi']:+.3f}] | " + " | ".join(f"{r_[l]['median']:+.3f} [{r_[l]['lo']:+.3f}, {r_[l]['hi']:+.3f}]" for l in TAB[1:]) + f" | {bs} |")
open(os.path.join(LANE, "cfg227_table.md"), "w").write("\n".join(lines) + "\n")
json.dump(dict(groups=RES, points=[dict(p, extra=None) for p in PTS], k_in=K_IN, k_out=K_OUT, controls=dict(passed=sum(CHK), n=len(CHK)), deltas={p_["id"] + "|" + p_["group"]: {l: float(delta_of(np.array([p_["gobs"]]), np.array([p_["gbar"]]), np.array([p_["z"]]), l)[0]) for l in TAB} for p_ in PTS}),
          open(os.path.join(LANE, "cfg227_rar_z2_5_results.json"), "w"), indent=1, default=float)
open(os.path.join(LANE, "cfg227_rar_z2_5.out"), "w").write("\n".join(OUT) + "\n")
sys.exit(0 if all(CHK) else 1)
