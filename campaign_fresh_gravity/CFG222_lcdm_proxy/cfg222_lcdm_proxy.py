#!/usr/bin/env python3
"""CFG222 -- a LambdaCDM effective-a0 PROXY scored on real data with the machinery used for flat and H(z).
*** LambdaCDM has no a0.  This is an effective-a0 PROXY, not LambdaCDM.  A fair LambdaCDM test uses simulated galaxies. ***
Frozen criteria: FROZEN_CRITERIA.md here (35e3df460), committed before any proxy number.  kappa = 1/2 FITTED, NOT DERIVED.  Author decompositions, not a direct a0 measurement.
No sentence says the data favour a framework or LambdaCDM.  Laws: FLAT; H(z); the PRIMARY proxy = Z1's lcdm_native (puzzle_32pi, 1138d817f); sensitivities = the record's own a0(z)-lane
estimates (M-LCDM-DM14 = '+0.33 dex', D08, MAG) and Z1's M / dlogc variants.  Data: RC100 (committed and corrected tables) and CRISTAL z ~ 5 (CFG213 / CFG220 machinery).
Run:  python3 campaign_fresh_gravity/CFG222_lcdm_proxy/cfg222_lcdm_proxy.py        (MUTATE=1 runs the response control)
"""
import os, sys, io, csv, json, math, tempfile, contextlib, time
sys.dont_write_bytecode = True
import numpy as np
from scipy.optimize import brentq

LANE = os.path.dirname(os.path.abspath(__file__))
CFG = os.path.dirname(LANE)
REPO = os.path.dirname(CFG)
MUT = os.environ.pop("MUTATE", "").strip() == "1"            # the exec'd lane prefixes must not see MUTATE; this lane injects its own
SFX = "_MUTATE" if MUT else ""
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


G2SI = 1e6 / 3.0856775814913673e19
OM = 0.315
NB, NBW, SEED = 10000, 2000, 222
KER = {"nu_mono": K.nu_mono, "P2": K.nu_p2}
A0F = {"canonical": K.A0["canonical"], "alt": K.A0["alt"]}
CELLS = [("nu_mono", "canonical"), ("nu_mono", "alt"), ("P2", "canonical"), ("P2", "alt")]
PRIM = CELLS[0]
P(__doc__.split("Run:")[0].strip())

# ------------------------------------------------------------------------------------------------ the laws, F_L(z) = a0_L(z)/a0
def E(z):
    return math.sqrt(OM * (1 + z) ** 3 + 1 - OM)


h_ = 0.674
fc = lambda x: math.log(1 + x) - x / (1 + x)


def c_DM14(M, z):
    a = 0.520 + (0.905 - 0.520) * math.exp(-0.617 * z ** 1.21); b = -0.101 + 0.026 * z
    return 10 ** (a + b * math.log10(M * h_ / 1e12))


def c_D08(M, z):
    return 5.71 * (M * h_ / 2e12) ** (-0.084) * (1 + z) ** (-0.47)


def make_R(cfun, M=1e12):
    c0 = cfun(M, 0.0); base = c0 ** 2 / fc(c0)
    return lambda z: math.sqrt(0.315 * (1 + z) ** 3 + 0.685) ** (4 / 3) * (cfun(M, z) ** 2 / fc(cfun(M, z))) / base


LAWS = {"FLAT": lambda z: 1.0, "LCDM-PROXY": lambda z: Z1.lcdm_native(z), "H(z)": E}
SENS = {"DM14 (a0(z) lane, the +0.33 dex)": make_R(c_DM14), "D08": make_R(c_D08), "MAG (1+z)^0.92": lambda z: (1 + z) ** 0.92,
        "Z1 M = 1e11": lambda z: Z1.lcdm_native(z, M=1e11), "Z1 M = 1e13": lambda z: Z1.lcdm_native(z, M=1e13),
        "Z1 dlogc = +0.1": lambda z: Z1.lcdm_native(z, dlogc=0.1), "Z1 dlogc = -0.1": lambda z: Z1.lcdm_native(z, dlogc=-0.1)}
ALL = dict(LAWS); ALL.update(SENS)
TAB = ("FLAT", "LCDM-PROXY", "H(z)")


def Farr(law, z):
    return np.array([ALL[law](float(zz)) for zz in z])


# ------------------------------------------------------------------------------------------------ machinery
def nu1(nu, y):
    return float(nu(np.array([y]))[0])


def gbar_of_gobs(gobs, a0t, nu):
    q = gobs / a0t
    return a0t * 10 ** brentq(lambda ly: nu1(nu, 10 ** ly) * 10 ** ly - q, -80, 14, xtol=1e-14, rtol=1e-14)


def delta_arr(D, gb, Fa, a0, nu):
    return np.log10(D / nu(gb / (a0 * Fa)))


def expected_arr(gobs, FT, FL, a0, nu):
    gt = np.array([gbar_of_gobs(g, a0 * ft, nu) for g, ft in zip(gobs, FT)])
    return delta_arr(gobs / gt, gt, FL, a0, nu)


def ts(x, y):
    i, j = np.triu_indices(len(x), 1)
    dx = x[j] - x[i]; m = dx != 0
    return float(np.median((y[j] - y[i])[m] / dx[m]))


_IDX = {}


def IDX(n, B):
    if (n, B) not in _IDX:
        _IDX[(n, B)] = np.random.default_rng(SEED * 1000 + n).integers(0, n, size=(B, n))
    return _IDX[(n, B)]


def ts_boot(x, y, B=NB):
    n = len(x); I = IDX(n, B); i, j = np.triu_indices(n, 1); o = np.empty(B)
    for k in range(B):
        xb, yb = x[I[k]], y[I[k]]
        dx = xb[j] - xb[i]; m = dx != 0
        o[k] = np.median((yb[j] - yb[i])[m] / dx[m])
    return o


def med_boot(d, B=NB):
    return np.median(d[IDX(len(d), B)], axis=1)


def verdict(lo, hi):
    return "CONSISTENT" if lo <= 0 <= hi else ("DISFAVOURED-over" if lo > 0 else "DISFAVOURED-under")


# ------------------------------------------------------------------------------------------------ RC100
RC_PATH = {"committed": os.path.join(REPO, "real_research", "data", "rc100_nestorshachar2023_table3.csv"),
           "corrected": os.path.join(REPO, "data_assembly", "rc100_provenance", "rc100_table3_six_fields_paper_values.csv")}


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


def rc_slopes(ds, law, cell, B=NB):
    nu, a0 = KER[cell[0]], A0F[cell[1]]
    Fa = Farr(law, ds["z"])
    d = delta_arr(ds["D"], ds["gb"], Fa, a0, nu)
    return d, ts(ds["z"], d), ts_boot(ds["z"], d, B)


def rc_expected(ds, TL, LL, cell):
    nu, a0 = KER[cell[0]], A0F[cell[1]]
    return expected_arr(ds["go"], Farr(TL, ds["z"]), Farr(LL, ds["z"]), a0, nu)


def rc_tilt_point(ds, law, cell, t):
    """the slope of delta_L on z after CFG217's tilt t (dex change of the analysis baryon mass between z = 0.6 and 2.5, log-linear in log10 (1 + z)); D is recomputed as g_obs / g_bar'."""
    nu, a0 = KER[cell[0]], A0F[cell[1]]
    x = np.log10((1 + ds["z"]) / 2.5); DLOG = math.log10(3.5 / 1.6)
    gb = ds["gb"] * 10 ** ((t / DLOG) * x)
    return ts(ds["z"], delta_arr(ds["go"] / gb, gb, Farr(law, ds["z"]), a0, nu)), gb


def rc_tilt_scan(ds, law, cell, tilts):
    nu, a0 = KER[cell[0]], A0F[cell[1]]
    pts = []
    for t in tilts:
        s, gb = rc_tilt_point(ds, law, cell, t)
        d = delta_arr(ds["go"] / gb, gb, Farr(law, ds["z"]), a0, nu)
        pts.append((s, ts_boot(ds["z"], d, NBW)))
    return pts


# ------------------------------------------------------------------------------------------------ CRISTAL (CFG213 / CFG220 machinery, exec'd read-only)
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


def cr_med(rows, law, cell, B=NB):
    nu, a0 = KER[cell[0]], A0F[cell[1]]
    z = np.array([r["z"] for r in rows]); gb = np.array([r["gbar"] for r in rows]); D = np.array([r["D"] for r in rows])
    d = delta_arr(D, gb, Farr(law, z), a0, nu)
    bs = med_boot(d, B)
    return float(np.median(d)), float(np.percentile(bs, 2.5)), float(np.percentile(bs, 97.5)), float(np.std(bs)), d


def cr_exp(rows, TL, LL, cell):
    nu, a0 = KER[cell[0]], A0F[cell[1]]
    z = np.array([r["z"] for r in rows]); go = np.array([r["gbar"] * r["D"] for r in rows])
    return float(np.median(expected_arr(go, Farr(TL, z), Farr(LL, z), a0, nu)))


# ------------------------------------------------------------------------------------------------ controls
P("\nCONTROLS")
ref = {"DM14": (make_R(c_DM14), (1.233, 1.756, 2.126, 2.823)), "D08": (make_R(c_D08), (1.427, 2.284, 2.802, 3.667)), "MAG": (lambda z: (1 + z) ** 0.92, (1.892, 2.748, 3.166, 3.785))}
zc = (1.0, 2.0, 2.5, 3.25)
dmaxc = max(abs(f(z) - v) for f, vals in ref.values() for z, v in zip(zc, vals))
check("C1 law values: Z1's F(2.5) = 2.16 +- 0.02; the a0(z) lane's DM14 / D08 / MAG ratios at z = 1 / 2 / 2.5 / 3.25 to 0.005", f"Z1 F(2.5) {LAWS['LCDM-PROXY'](2.5):.3f}; max |difference| {dmaxc:.4f}", abs(LAWS["LCDM-PROXY"](2.5) - 2.16) < 0.02 and dmaxc < 0.005)
J216 = {t: json.load(open(os.path.join(CFG, "CFG216_rc100_within_sample", f"cfg216_rc100{'_corrected' if t == 'corrected' else ''}_results.json")))["numbers"]["results"] for t in RC_PATH}
DS = {t: load_rc100(p, mutate=MUT) for t, p in RC_PATH.items()}
DS0 = {t: load_rc100(p, mutate=False) for t, p in RC_PATH.items()}
c2 = 0.0
if not MUT:
    for t in RC_PATH:
        for cell in CELLS:
            for law, lab in (("FLAT", "flat"), ("H(z)", "rival")):
                _, s, _ = rc_slopes(DS0[t], law, cell, B=10)
                c2 = max(c2, abs(s - J216[t][f"{cell[0]}|{cell[1]}|{lab}"]["slope"]))
check("C2a RC100: the FLAT and H(z) slopes of delta on z (both tables, four cells) equal CFG216's committed values", f"max |difference| {c2:.1e}", c2 < 1e-9 or MUT)
J213 = json.load(open(os.path.join(CFG, "CFG213_dysmalpy_two_sided", "cfg213_two_sided_results.json")))["numbers"]["Z5 (CRISTAL primary)"]
J220 = json.load(open(os.path.join(CFG, "CFG220_cristal_outer_independent", "cfg220_outer_independent_results.json")))["cells"]
c2b = 0.0
ids12 = [g["id"] for g in cr if g["id"] not in EXCL]
r12 = rows_Re(ids12, "fit")
for cell in CELLS:
    for law, lab in (("FLAT", "flat"), ("H(z)", "rival")):
        nu, a0 = KER[cell[0]], A0F[cell[1]]
        z = np.array([r["z"] for r in r12]); gb = np.array([r["gbar"] for r in r12]); D = np.array([r["D"] for r in r12])
        m = float(np.median(delta_arr(D, gb, Farr(law, z), a0, nu)))
        c2b = max(c2b, abs(m - J213[f"3.36|fit|{cell[0]}|{cell[1]}|{lab}"]["med"]))
check("C2b CRISTAL R_e, fit route, the twelve discs: the FLAT and H(z) medians (four cells) equal CFG213's committed values", f"max |difference| {c2b:.1e}", c2b < 1e-9)
c2c = 0.0
for route in ("ind", "fit"):
    for rdef in ("table_Rout",):
        rr = rows_Rout(rdef, DET, route)
        for cell in CELLS:
            for law, lab in (("FLAT", "flat"), ("H(z)", "rival")):
                c2c = max(c2c, abs(cr_med(rr, law, cell, B=10)[0] - J220[f"{route}|{cell[0]}|{cell[1]}|{rdef}"][lab][0]))
check("C2c CRISTAL R_out, both routes, the six: the FLAT and H(z) medians (four cells) equal CFG220's committed values", f"max |difference| {c2c:.1e}", c2c < 1e-9)
six = list(DET)
ri, rc_ = rows_Re(six, "ind"), galaxy_rows213("Z5", [crbyid[i] for i in six], alpha=3.36, route=True)
ri_sorted = {r["id"]: r for r in ri}
c2d = max(max(abs(ri_sorted[r["id"]]["gbar"] / r["gbar"] - 1), abs(ri_sorted[r["id"]]["D"] / r["D"] - 1)) for r in rc_)
check("C2d CRISTAL R_e, independent route, the six: this lane's g_bar and D equal CFG213's galaxy_rows(route=True)", f"max relative difference {c2d:.1e}", c2d < 1e-12)
# C3: non-vacuous placement through the observables (RC100 six-field CSV) for every law
rng0 = np.random.default_rng(SEED)
recs, tags = [], []
for law in ALL:
    for zz in (0.61, 1.0, 1.53, 2.0, 2.52):
        for y in (0.03, 0.3, 1.0, 3.0, 30.0):
            for cell in (PRIM,):
                nu, a0 = KER[cell[0]], A0F[cell[1]]
                a0l = a0 * ALL[law](zz); nuv = nu1(nu, y); gobs = y * a0l * nuv; fd = 1 - 1 / nuv
                recs.append(dict(name=f"{law}|{zz}|{y}", z=zz, Re_kpc=5.0, Vc_Re_kms=math.sqrt(gobs * 5.0 / G2SI), fDM_within_Re=fd, logMbar_Msun=11.0)); tags.append(law)
with tempfile.NamedTemporaryFile("w", suffix=".csv", delete=False, newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(recs[0])); w.writeheader(); w.writerows(recs); SYN = f.name
dsyn = load_rc100(SYN); os.unlink(SYN)
assert len(dsyn["z"]) == len(recs)
nu, a0 = KER[PRIM[0]], A0F[PRIM[1]]
dmax3, oth3 = 0.0, []
for law in ALL:
    sel = np.array([t == law for t in tags])
    sub = {k: v[sel] for k, v in dsyn.items()}
    dmax3 = max(dmax3, float(np.max(np.abs(delta_arr(sub["D"], sub["gb"], Farr(law, sub["z"]), a0, nu)))))
    for other in ALL:
        if other != law:
            oth3.extend(np.abs(delta_arr(sub["D"], sub["gb"], Farr(other, sub["z"]), a0, nu)).tolist())
frac3 = float(np.mean(np.array(oth3) > 1e-3))
check("C3 non-vacuous placement: synthetic rows on each law (FLAT, H(z), the proxy, its 7 sensitivities) through V_c, R_e, f_DM, read by the loader and scored by the machinery: |delta| < 1e-9 and >= 90% of the other-law deltas > 1e-3",
      f"max |delta| {dmax3:.1e}; other-law sensitivity {100 * frac3:.0f}%", dmax3 < 1e-9 and frac3 >= 0.90)
# C4: expectation identity through the loader
d0 = DS0["committed"]
c4 = 0.0
for TL in TAB:
    FT = Farr(TL, d0["z"])
    gt = np.array([gbar_of_gobs(g, a0 * ft, nu) for g, ft in zip(d0["go"], FT)])
    fd = 1 - gt / d0["go"]
    rows4 = [dict(name="x", z=zz, Re_kpc=5.0, Vc_Re_kms=math.sqrt(g * 5.0 / G2SI), fDM_within_Re=f_, logMbar_Msun=11.0) for zz, g, f_ in zip(d0["z"], d0["go"], fd)]
    with tempfile.NamedTemporaryFile("w", suffix=".csv", delete=False, newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows4[0])); w.writeheader(); w.writerows(rows4); SYN = f.name
    d4 = load_rc100(SYN); os.unlink(SYN)
    for LL in TAB:
        s_obs = ts(d4["z"], delta_arr(d4["D"], d4["gb"], Farr(LL, d4["z"]), a0, nu))
        s_exp = ts(d0["z"], rc_expected(d0, TL, LL, PRIM))
        c4 = max(c4, abs(s_obs - s_exp))
check("C4 expectation identity: a sample built under truth T (through the observables and the loader) has an observed slope of delta_L equal to the expected slope e(L|T) for all nine (L, T)", f"max |difference| {c4:.1e}", c4 < 1e-9)

if MUT:
    ok = True
    for t in RC_PATH:
        for cell in CELLS:
            for law in TAB:
                s1 = rc_slopes(DS[t], law, cell, B=10)[1]; s0 = rc_slopes(DS0[t], law, cell, B=10)[1]
                ok &= abs((s1 - s0) - 0.2) < 1e-9 + 1e-3 * 0            # the injection is a shift of exactly +0.2 (z - z_med) in delta
    for rdef, ids in (("Re12", ids12),):
        pass
    rows_m = rows_Re(ids12, "fit", mutate=True); rows_u = rows_Re(ids12, "fit", mutate=False)
    for cell in CELLS:
        for law in TAB:
            ok &= abs(cr_med(rows_m, law, cell, B=10)[0] - cr_med(rows_u, law, cell, B=10)[0] - math.log10(1.5)) < 1e-9
    check("MUTATE the RC100 injection (D x 10^(0.2 (z - z_med))) shifts every law's slope by +0.200 and the CRISTAL injection (D x 1.5) every median by log10 1.5, to 1e-9", f"{ok}", ok)
    open(os.path.join(LANE, "cfg222_lcdm_proxy_MUTATE.out"), "w").write("\n".join(OUT) + "\n")
    sys.exit(0 if all(CHK) else 1)

# ------------------------------------------------------------------------------------------------ the results
CAV = {"RC100": "gas route: M_bary is the authors' fit, prior-anchored to SED + Tacconi-type gas scalings that grow with z; the window column is CFG217's tilt of the analysis baryon mass between z = 0.6 and 2.5",
       "CRfit": "gas route: M_bary is the authors' fit (a 1-dex Gaussian prior fitted jointly with the halo); no independent gas calibration enters",
       "CRind": "gas route: SED M* + dust gas (Scoville-type, single-band T_d); the window column is the uniform gas-mass offset tau (dex) that would move the verdict"}
RES = {}
P("\nMAIN TABLE: ONE row per data set and route; for each law the observed statistic [95% CI], z vs its OWN expectation, z vs the FLAT-true expectation (primary cell: nu_mono, canonical)")
P("  statistic: RC100 = Theil-Sen slope of delta on z (per unit z); CRISTAL = median delta.  z = (observed - expected)/bootstrap sd; 'window' = the gas-calibration range over which the law is CONSISTENT with 0")
tilts = np.round(np.arange(-0.60, 0.6001, 0.05), 3)
taus = np.round(np.arange(-1.0, 1.0001, 0.05), 3)
rows_spec = []
for t in ("committed", "corrected"):
    rows_spec.append((f"RC100 {t} (n = {len(DS[t]['z'])})", "RC100", t))
rows_spec += [("CRISTAL R_e, fit route, n = 12", "CRfit", ("Re", "fit", ids12)), ("CRISTAL R_e, independent route, six class-A", "CRind", ("Re", "ind", six)),
              ("CRISTAL R_out, fit route, six", "CRfit", ("Rout", "fit", six)), ("CRISTAL R_out, independent route, six", "CRind", ("Rout", "ind", six))]


def cr_rows(spec, tau=0.0):
    kind, route, ids = spec
    return rows_Re(ids, route, tau) if kind == "Re" else rows_Rout("table_Rout", ids, route, tau)


for label, kind, spec in rows_spec:
    P(f"\n  {label}  [{CAV[kind]}]")
    RES[label] = {}
    for law in TAB:
        if kind == "RC100":
            ds = DS[spec]
            d, s, bs = rc_slopes(ds, law, PRIM)
            e_flat = ts(ds["z"], rc_expected(ds, "FLAT", law, PRIM))
            sd = float(np.std(bs)); lo, hi = float(np.percentile(bs, 2.5)), float(np.percentile(bs, 97.5))
            # CFG233's per-resample expectation
            ex = rc_expected(ds, "FLAT", law, PRIM); exb = ts_boot(ds["z"], ex)
            z_rec = (s - e_flat) / float(np.std(bs - exb))
            pts = rc_tilt_scan(ds, law, PRIM, tilts)
            sl = np.array([p[0] for p in pts]); cons = [t_ for t_, p in zip(tilts, pts) if np.percentile(p[1], 2.5) <= 0 <= np.percentile(p[1], 97.5)]
            f_ = lambda tt, ds_=ds, law_=law: rc_tilt_point(ds_, law_, PRIM, tt)[0]
            try:
                tstar = brentq(f_, -0.8, 0.8, xtol=1e-6)
            except ValueError:
                tstar = None
            win = f"tilt t* {tstar:+.3f} dex; slope CI includes 0 for t in [{min(cons):+.2f}, {max(cons):+.2f}]" if (cons and tstar is not None) else ("tilt t* " + (f"{tstar:+.3f}" if tstar is not None else "none in [-0.8, 0.8]") + "; slope CI never includes 0 on the grid" if not cons else "")
            z_own, z_flat = s / sd, (s - e_flat) / sd
            RES[label][law] = dict(stat=s, lo=lo, hi=hi, sd=sd, e_flat=e_flat, z_own=z_own, z_flat=z_flat, z_flat_rec=z_rec, window=win)
            P(f"    {law:11s} slope {s:+.3f} [{lo:+.3f}, {hi:+.3f}]  expected if FLAT true {e_flat:+.3f}  z(own) {z_own:+.2f}  z(flat-true) {z_flat:+.2f} (per-resample expectation {z_rec:+.2f});  {win}")
        else:
            rows = cr_rows(spec)
            m, lo, hi, sd, d = cr_med(rows, law, PRIM)
            e_flat = cr_exp(rows, "FLAT", law, PRIM)
            win = "n/a (fit route: no calibration enters)"
            if kind == "CRind":
                def f_(tau, rows_spec=spec, law_=law):
                    rr = cr_rows(rows_spec, tau)
                    return cr_med(rr, law_, PRIM, B=10)[0]
                try:
                    tstar = brentq(f_, -3.0, 3.0, xtol=1e-6)
                except ValueError:
                    tstar = None
                cons = []
                for tau in taus:
                    mm, l2, h2, _, _ = cr_med(cr_rows(spec, float(tau)), law, PRIM, NBW)
                    if l2 <= 0 <= h2:
                        cons.append(float(tau))
                win = f"tau* {tstar:+.3f} dex; CONSISTENT for tau in [{min(cons):+.2f}, {max(cons):+.2f}]" if (cons and tstar is not None) else (f"tau* {tstar:+.3f}" if tstar is not None else "tau* none in [-3, 3]") + ("; never CONSISTENT on the grid" if not cons else f"; CONSISTENT for tau in [{min(cons):+.2f}, {max(cons):+.2f}]")
            z_own, z_flat = m / sd, (m - e_flat) / sd
            RES[label][law] = dict(stat=m, lo=lo, hi=hi, sd=sd, e_flat=e_flat, z_own=z_own, z_flat=z_flat, verdict=verdict(lo, hi), window=win)
            P(f"    {law:11s} median {m:+.3f} [{lo:+.3f}, {hi:+.3f}] {verdict(lo, hi):18s} expected if FLAT true {e_flat:+.3f}  z(own) {z_own:+.2f}  z(flat-true) {z_flat:+.2f};  {win}")
P("\n  Extrapolation flags: DM14 is fitted to z <= 5 (the CRISTAL discs reach z = 5.69: slightly above), Duffy+2008 to z <~ 2 and the Magneticum rise to z <~ 2-3 (both EXTRAPOLATED at CRISTAL's z); the primary proxy's values: "
  + ", ".join(f"F({zz}) = {LAWS['LCDM-PROXY'](zz):.2f}" for zz in (1.0, 2.0, 2.5, 4.5, 5.5)))

# ------------------------------------------------------------------------------------------------ the other three cells
P("\nTABLE 2: z vs OWN expectation in the other three kernel/footing cells (slope for RC100, median for CRISTAL)")
P(f"  {'row':44s} {'cell':22s} " + " ".join(f"{l:>12s}" for l in TAB))
R2 = {}
for label, kind, spec in rows_spec:
    for cell in CELLS[1:]:
        zs = []
        for law in TAB:
            if kind == "RC100":
                d, s, bs = rc_slopes(DS[spec], law, cell)
                zs.append(s / float(np.std(bs)))
            else:
                m, lo, hi, sd, d = cr_med(cr_rows(spec), law, cell)
                zs.append(m / sd)
        R2[(label, cell)] = zs
        P(f"  {label:44s} {cell[0] + ' ' + cell[1]:22s} " + " ".join(f"{z_:+12.2f}" for z_ in zs))
P("\nTABLE 3: the proxy sensitivities on the primary cell: z vs OWN expectation (z vs flat-true in brackets)")
P(f"  {'row':44s} " + " ".join(f"{s[:16]:>18s}" for s in SENS))
R3 = {}
for label, kind, spec in rows_spec:
    zs = []
    for law in SENS:
        if kind == "RC100":
            d, s, bs = rc_slopes(DS[spec], law, PRIM); sd = float(np.std(bs)); e = ts(DS[spec]["z"], rc_expected(DS[spec], "FLAT", law, PRIM))
            zs.append((s / sd, (s - e) / sd))
        else:
            rows = cr_rows(spec); m, lo, hi, sd, d = cr_med(rows, law, PRIM); e = cr_exp(rows, "FLAT", law, PRIM)
            zs.append((m / sd, (m - e) / sd))
    R3[label] = zs
    P(f"  {label:44s} " + " ".join(f"{a:+7.2f} ({b:+6.2f})  " for a, b in zs))
P(f"\n{sum(CHK)}/{len(CHK)} controls pass; {time.time() - T0:.0f} s")
P("Reading rule: these are descriptions of where the data sit against each law's expectation given the gas route; LambdaCDM has no a0 and a fair LambdaCDM test uses simulated galaxies; no sentence says the data favour a framework or LambdaCDM.")
json.dump({"main": RES, "other_cells": {f"{k[0]}|{k[1]}": v for k, v in R2.items()}, "sensitivities": {k: v for k, v in R3.items()}, "controls": dict(passed=sum(CHK), n=len(CHK))}, open(os.path.join(LANE, "cfg222_lcdm_proxy_results.json"), "w"), indent=1, default=float)
open(os.path.join(LANE, "cfg222_lcdm_proxy.out"), "w").write("\n".join(OUT) + "\n")
sys.exit(0 if all(CHK) else 1)
