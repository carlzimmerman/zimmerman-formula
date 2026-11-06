#!/usr/bin/env python3
"""QX14 grader: does AGC 114905's environment supply QX4's external-field window? (FROZEN_CRITERIA.md, 922b5e8167)
usage: python3 -I qx14.py [main|MUTATE1|MUTATE2] DATADIR      (DATADIR = _external_data/qx14_agc114905)
Outputs qx14[_MODE].{out,json}, census.csv (main only). Both footings, never pooled. kappa = 1/2 FITTED; not theory closed."""
import contextlib, csv, io, json, math, os, sys
import numpy as np
from scipy.stats import chi2 as CHI2
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
MODE = sys.argv[1]; DATA = os.path.abspath(sys.argv[2])
sys.path.insert(0, os.path.join(ROOT, "gext_vectors_2026", "src")); import gext_estimator as GE   # read-only import
FOOT = dict(canonical=9.3603e-11, alt=1.1312e-10)
GSI, MSUN, KPC, MPC, CK = 6.674e-11, 1.989e30, 3.0857e19, 3.0857e22, 299792.458
CONV = 1e6 / 3.0857e19
D0 = 78.7; RP_MAX = 1.0; DV = 500.0; RAD = 0.75
OUT, RES = [], dict(mode=MODE)
def P(*a):
    s = " ".join(str(x) for x in a); OUT.append(s); print(s, flush=True)
def nu(y): y = np.maximum(np.asarray(y, float), 1e-30); return 0.5 + np.sqrt(0.25 + 1.0 / y)

# ------------------------------------------------ UD1 data (read-only exec, as QX4 iter2_efe) and KA2
UD1 = os.path.join(ROOT, "rebuild_2026_10_22", "UD1_agc114905_udg_rotation", "ud1.py")
src = open(UD1).read(); ns = dict(__file__=UD1, __name__="ud_import"); old = sys.argv; sys.argv = [UD1, "law"]
try:
    with contextlib.redirect_stdout(io.StringIO()): exec(compile(src[:src.index("# ---- K0a")], UD1, "exec"), ns)
finally: sys.argv = old
R, V, E, vb2 = (np.asarray(ns[k], float) for k in ("Rk", "V", "E", "vb2"))
Ro_kpc = float(R[-1]); Ro = Ro_kpc * KPC
I2 = json.load(open(os.path.join(ROOT, "closure_2026_11_06", "QX4_udg", "iter2.json")))["AGC114905"]
def law_v(ge, a0):
    gN = vb2 / R * CONV; gt = gN + ge * a0; g = nu(gt / a0) * gt - (nu(ge) * ge * a0 if ge > 0 else 0.0)
    return np.sqrt(np.maximum(g / CONV * R, 0))
GEG = np.concatenate([[0.0], np.exp(np.linspace(np.log(1e-3), np.log(3.0), 3000))])
WIN, GINT = {}, {}
for f, a0 in FOOT.items():
    p = np.array([CHI2.sf(float(np.sum(((V - law_v(g, a0)) / E) ** 2)), len(V)) for g in GEG]); ok = GEG[p >= 0.05]
    WIN[f] = (float(ok.min()), float(ok.max())); GINT[f] = (V[-1] * 1e3) ** 2 / Ro / a0
    d = max(abs(WIN[f][0] - I2[f]["p_ok"][0]), abs(WIN[f][1] - I2[f]["p_ok"][1]))
    P(f"KA2 [{f}] window g_e/a0 {WIN[f][0]:.4f}-{WIN[f][1]:.4f} (QX4 {I2[f]['p_ok'][0]:.4f}-{I2[f]['p_ok'][1]:.4f}), |diff| {d:.1e}"
      f" {'PASS' if d <= 1e-3 else 'FAIL'}; g_int {GINT[f]:.4f} a0 at R_out {Ro_kpc:.2f} kpc")
    RES.setdefault("KA2", {})[f] = dict(window=WIN[f], qx4=I2[f]["p_ok"], diff=d, ok=d <= 1e-3, g_int_over_a0=GINT[f])

# ------------------------------------------------ host condition (Newtonian reading) and M_req
def hprime(x): return 0.5 + (x / 2 + 1) / (2 * np.sqrt(x * x / 4 + x))          # d(nu(x) x)/dx
def qualifies(M, dmin_kpc, f):
    """exists d >= dmin with g_N(d)/a0 in window and tidal |dg_h/dd| R_out < g_int (all in a0 units)."""
    a0 = FOOT[f]; lo, hi = WIN[f]
    d = np.exp(np.linspace(np.log(max(dmin_kpc, 1e-3)), np.log(max(dmin_kpc, 1e-3) * 1e4), 20000)) * KPC
    x = GSI * M * MSUN / d ** 2 / a0; t = 2 * x * hprime(x) * Ro / d
    ok = (x >= lo) & (x <= hi) & (t < GINT[f]); return bool(ok.any()), (float(d[ok][0] / KPC) if ok.any() else None)
def qx4_reading(M, dmin_kpc, f):
    """QX4's reading (reported only): g_e = host MOND field sqrt(G M a0)/d in window, tidal (g_e R/d) < g_int."""
    a0 = FOOT[f]; lo, hi = WIN[f]
    d = np.exp(np.linspace(np.log(max(dmin_kpc, 1e-3)), np.log(max(dmin_kpc, 1e-3) * 1e4), 20000)) * KPC
    x = np.sqrt(GSI * M * MSUN * a0) / d / a0; t = x * Ro / d
    return bool(((x >= lo) & (x <= hi) & (t < GINT[f])).any())
MREQ = {}
for f, a0 in FOOT.items():
    xs = np.linspace(WIN[f][0], WIN[f][1], 4001); dt = 2 * xs * hprime(xs) * Ro / (GINT[f])   # tidal-limited distance (m)
    M = xs * a0 * dt ** 2 / GSI / MSUN; i = int(np.argmin(M)); MREQ[f] = float(M[i])
    P(f"M_req [{f}] (Newtonian reading) = {M[i]:.3e} Msun at g_N {xs[i]:.4f} a0, d {dt[i] / KPC:.0f} kpc (host true field {xs[i] * nu(xs[i]):.3f} a0);"
      f" QX4's reading M_req = {I2[f]['host_Mb_min_Msun']:.2e}")
    RES.setdefault("M_req", {})[f] = dict(M=MREQ[f], gN=float(xs[i]), d_kpc=float(dt[i] / KPC), M_qx4=I2[f]["host_Mb_min_Msun"])

# ------------------------------------------------ completeness test (before reading the census)
dm0 = 5 * math.log10(D0 * (1 + D0 * GE.H0 / CK)) + 25
Mstar_lim = GE.ML_KS * 10 ** (-0.4 * (13.9 - dm0 - GE.MSUN_KS))
S_lim = 10 ** (0.5 * math.log10(200.0) - 1.207); MHI_lim = 2.356e5 * D0 ** 2 * S_lim
COMP = {f: bool(Mstar_lim <= MREQ[f] or 1.33 * MHI_lim <= MREQ[f]) for f in FOOT}
P(f"completeness: 2MPZ Ks<=13.9 M* limit {Mstar_lim:.2e}; ALFALFA HI limit (W50 200) {MHI_lim:.2e} (gas {1.33 * MHI_lim:.2e});"
  f" complete at M_req: {COMP}")
RES["completeness"] = dict(Mstar_lim=Mstar_lim, MHI_lim=MHI_lim, complete=COMP)

# ------------------------------------------------ target and census
J = json.load(open(os.path.join(DATA, "ned_lookup.json")))["Preferred"]
RA0, DE0 = J["Position"]["RA"], J["Position"]["Dec"]; cz_ned = J["Redshift"]["Value"] * CK
def sep(ra, de):
    r1, d1, r2, d2 = map(np.radians, (RA0, DE0, np.asarray(ra, float), np.asarray(de, float)))
    return np.degrees(np.arccos(np.clip(np.sin(d1) * np.sin(d2) + np.cos(d1) * np.cos(d2) * np.cos(r1 - r2), -1, 1)))
def hms(s, hours):
    p = s.split(); v = abs(float(p[0])) + float(p[1]) / 60 + float(p[2]) / 3600; v = -v if p[0].strip().startswith("-") else v
    return v * 15 if hours else v
AL = []
for l in open(os.path.join(DATA, "alfalfa_a100_cone.tsv")):
    if l.startswith("#") or not l.strip(): continue
    c = l.rstrip("\n").split("\t")
    if c[0].strip() in ("AGC", "") or c[0].startswith("-"): continue
    ra = hms(c[4] if c[4].strip() else c[2], True); de = hms(c[5] if c[5].strip() else c[3], False)
    AL.append(dict(agc=c[0].strip(), ra=ra, dec=de, v=float(c[6]), S21=float(c[10])))
me = [a for a in AL if a["agc"] == "114905"][0]
dsep = float(sep(me["ra"], me["dec"])) * 3600; dcz = abs(me["v"] - cz_ned)
cz0 = cz_ned if (dsep <= 30 and dcz <= 20) else me["v"]
P(f"target: NED {RA0:.5f} {DE0:+.5f} cz {cz_ned:.1f}; ALFALFA 114905 sep {dsep:.1f}\" dcz {dcz:.1f} km/s -> cz0 = {cz0:.1f} ({'NED' if cz0 == cz_ned else 'ALFALFA'})")
RES["target"] = dict(ra=RA0, dec=DE0, cz_ned=cz_ned, alfalfa_sep_arcsec=dsep, alfalfa_dcz=dcz, cz0=cz0)
THMAX = math.degrees(RP_MAX / D0)
ROWS = []
def add(src, name, ra, de, v, kind, **kw):
    s = float(sep(ra, de)); ROWS.append(dict(src=src, name=name, ra=float(ra), dec=float(de), v=v, kind=kind, sep_deg=s, Rp_kpc=D0 * math.radians(s) * 1e3, **kw))
for l in csv.DictReader(open(os.path.join(DATA, "ned_cone.csv"))):
    if l["prefphytype"].strip() not in ("G", "GPair", "GTrpl", "GGroup"): continue
    v = float(l["z"]) * CK
    if abs(v - cz0) <= DV and float(sep(l["ra"], l["dec"])) < THMAX: add("NED", l["prefname"], l["ra"], l["dec"], v, "spec", ned_type=l["prefphytype"])
txt = [x for x in open(os.path.join(DATA, "hyperleda_cone.csv")).read().splitlines() if x.strip() and not x.startswith("#")]
HL = list(csv.DictReader(txt[0:]))
for l in HL:
    if not l["v"].strip() or l["objtype"].strip().upper() not in ("G", "M"): continue
    v = float(l["v"]); ra = float(l["al2000"]) * 15; de = float(l["de2000"])
    if abs(v - cz0) <= DV and float(sep(ra, de)) < THMAX:
        add("HyperLEDA", l["objname"], ra, de, v, "spec", kt=float(l["kt"]) if l["kt"].strip() else None, btc=float(l["btc"]) if l["btc"].strip() else None)
for a in AL:
    if abs(a["v"] - cz0) <= DV and float(sep(a["ra"], a["dec"])) < THMAX: add("ALFALFA", "AGC" + a["agc"], a["ra"], a["dec"], a["v"], "spec", S21=a["S21"])
TM = []
for l in csv.reader(open(os.path.join(DATA, "twompz_cone.csv"))):
    if l[0].strip() == "twomassID": continue
    tid, ra, de, ks, zp, zs = [x.strip() for x in l]; ra, de, ks, zp, zs = map(float, (ra, de, ks, zp, zs)); TM.append((tid, ra, de, ks, zp, zs))
    if float(sep(ra, de)) >= THMAX: continue
    if zs > 0:
        if abs(zs * CK - cz0) <= DV: add("2MPZ", tid, ra, de, zs * CK, "spec", ks=ks)
    elif (zp - 2 * 0.015) * CK <= cz0 + DV and (zp + 2 * 0.015) * CK >= cz0 - DV: add("2MPZ", tid, ra, de, None, "photoz_candidate", ks=ks, zphoto=zp)
# drop the target itself (within 15" of the target or the ALFALFA OC position)
ROWS = [r for r in ROWS if not (r["sep_deg"] * 3600 <= 15 or
        (abs(r["ra"] - me["ra"]) * 3600 * math.cos(math.radians(DE0)) <= 15 and abs(r["dec"] - me["dec"]) * 3600 <= 15))]
# dedupe within 15"
U = []
for r in sorted(ROWS, key=lambda r: (r["src"] != "HyperLEDA", r["src"] != "2MPZ")):
    for u in U:
        dd = math.degrees(math.acos(min(1, math.sin(math.radians(u["dec"])) * math.sin(math.radians(r["dec"])) + math.cos(math.radians(u["dec"])) * math.cos(math.radians(r["dec"])) * math.cos(math.radians(u["ra"] - r["ra"]))))) * 3600
        if dd <= 15:
            u["srcs"].append(r["src"])
            for k in ("kt", "btc", "ks", "S21"):
                if r.get(k) is not None and u.get(k) is None: u[k] = r[k]
            break
    else: U.append(dict(r, srcs=[r["src"]]))
# nearest 2MPZ / HyperLEDA photometry for any unique entry lacking it (15")
for u in U:
    if u.get("ks") is None and u.get("kt") is None:
        for (tid, ra, de, ks, zp, zs) in TM:
            if abs(ra - u["ra"]) * 3600 * math.cos(math.radians(de)) <= 15 and abs(de - u["dec"]) * 3600 <= 15: u["ks"] = ks
    if u.get("kt") is None and u.get("btc") is None:
        for l in HL:
            try: ra = float(l["al2000"]) * 15; de = float(l["de2000"])
            except ValueError: continue
            if abs(ra - u["ra"]) * 3600 * math.cos(math.radians(de)) <= 15 and abs(de - u["dec"]) * 3600 <= 15:
                if l["kt"].strip(): u["kt"] = float(l["kt"])
                if l["btc"].strip(): u["btc"] = float(l["btc"])
# masses
for u in U:
    K = u.get("ks") if u.get("ks") is not None else u.get("kt")
    if K is not None: Ms = GE.ML_KS * 10 ** (-0.4 * (K - dm0 - GE.MSUN_KS)); up = 3.0; basis = "Ks"
    elif u.get("btc") is not None: Ms = 1.5 * 10 ** (-0.4 * (u["btc"] - dm0 - 5.48)); up = 6.0; basis = "B"
    else: Ms = Mstar_lim; up = 3.0; basis = "no photometry: 2MPZ Ks limit (not detected at Ks<=13.9)"
    if u.get("S21") is not None: Mg = 1.33 * 2.356e5 * D0 ** 2 * u["S21"]; gb = "ALFALFA"
    else:
        lg = math.log10(max(Ms, 1)); fe = min(max(0.28 * lg - 2.12, 0), 1)
        Mg = (1 - fe) * (11500 * Ms ** 0.54 + 0.07 * Ms) + fe * 10 ** (1.47 * lg - 5.414); gb = "Chae recipe"
    u.update(Mstar=Ms, Mgas=Mg, Mb=Ms + Mg, Mb_up=up * (Ms + Mg), mass_basis=basis, gas_basis=gb)
if MODE == "MUTATE2": U = []
if MODE == "MUTATE1":
    for f in FOOT:
        U.append(dict(src="PLANT", name=f"planted 2xM_req [{f}]", ra=RA0, dec=DE0, v=cz0, kind="spec", sep_deg=0, Rp_kpc=1.0, srcs=["PLANT"],
                      Mstar=2 * MREQ[f], Mgas=0.0, Mb=2 * MREQ[f], Mb_up=2 * MREQ[f], mass_basis="planted", gas_basis="-", only=f))
P(f"census: {len(U)} unique neighbours (R_p < {RP_MAX} Mpc, |dcz| <= {DV} km/s), "
  f"{sum(u['kind'] == 'photoz_candidate' for u in U)} photo-z candidates")
for f in FOOT:
    for u in U:
        if u.get("only") not in (None, f): continue
        q_c, dq = qualifies(u["Mb"], u["Rp_kpc"], f); q_u, _ = qualifies(u["Mb_up"], u["Rp_kpc"], f)
        u.setdefault("q", {})[f] = dict(central=q_c, d_kpc=dq, upper=q_u, qx4_reading=qx4_reading(u["Mb"], u["Rp_kpc"], f))
for u in sorted(U, key=lambda u: -u["Mb"] / max(u["Rp_kpc"], 1) ** 2)[:15]:
    P(f"   {u['name'][:28]:28s} {'+'.join(u['srcs']):24s} {u['kind']:16s} R_p {u['Rp_kpc']:6.0f} kpc v {u['v'] if u['v'] is None else round(u['v'])}"
      f" Mb {u['Mb']:.2e} (up {u['Mb_up']:.1e}, {u['mass_basis'][:10]}) qual {json.dumps({f: (q['central'], q['upper'], q['qx4_reading']) for f, q in u['q'].items()})}")

# ------------------------------------------------ large-scale field (record's SPARC method, ks115)
est = GE.GextEstimator(os.path.join(ROOT, "gext_vectors_2026", "data", "raw", "2mpp_vizier.tsv"),
                       os.path.join(ROOT, "gext_vectors_2026", "data", "raw", "mcxc.tsv"), catalog_mode="ks115")
ka1 = []
rows = list(csv.DictReader(open(os.path.join(ROOT, "gext_vectors_2026", "data", "gext_vectors.csv"))))
for r in (rows[0], rows[len(rows) // 2], rows[-1]):
    no = est.eN_at(float(r["ra"]), float(r["dec"]), float(r["D"]))["eN"]; mx = est.eN_at(float(r["ra"]), float(r["dec"]), float(r["D"]), completeness=True, missing_baryons_x8=True)["eN"]
    d = max(abs(math.log10(no) - float(r["log_eN_noclu"])), abs(math.log10(mx) - float(r["log_eN_maxclu"]))); ka1.append(d)
P(f"KA1 estimator reproduces gext_vectors.csv on 3 rows: max |diff| {max(ka1):.1e} dex {'PASS' if max(ka1) <= 1e-6 else 'FAIL'}")
RES["KA1"] = dict(max_diff_dex=max(ka1), ok=max(ka1) <= 1e-6)
if MODE == "MUTATE2": eno = emx = 0.0
else:
    eno = est.eN_at(RA0, DE0, D0)["eN"]; emx = est.eN_at(RA0, DE0, D0, completeness=True, missing_baryons_x8=True)["eN"]
SIG = 0.4530334594066687    # NV2 nv2_coverage.json E1_sigma_median
tp = GE.radec_to_cart(RA0, DE0) * D0; r5 = np.linalg.norm(est.gal_pos - tp, axis=1); m5 = (r5 < 5.0) & (r5 > GE.EXCL_KPC)
g5 = np.linalg.norm(((est.gal_pos[m5] - tp) / r5[m5, None] * (GSI * est.gal_mass[m5] * MSUN / (r5[m5] * MPC) ** 2)[:, None]).sum(0)) / GE.A0 if m5.any() else 0.0
P(f"large-scale field (Chae/record, ks115): e_N noclu {eno:.3e}, maxclu {emx:.3e} (units 1.2e-10); 5-Mpc truncation (sensitivity, noclu) {g5:.3e}; sigma_E1 {SIG:.3f} dex")
RES["field"] = dict(eN_noclu=eno, eN_maxclu=emx, eN_5Mpc_noclu=g5, sigma_dex=SIG)

# ------------------------------------------------ labels
for f, a0 in FOOT.items():
    lo, hi = WIN[f]; k = GE.A0 / a0
    no, mx = eno * k, emx * k; gm = math.sqrt(no * mx) if no > 0 and mx > 0 else 0.0; top = mx * 10 ** SIG
    nb = [u for u in U if u.get("only") in (None, f)]
    hostC = [u["name"] for u in nb if u["q"][f]["central"] and u["kind"] == "spec"]
    hostU = [u["name"] for u in nb if u["q"][f]["upper"]]
    field_in = lo <= gm <= hi; field_below = top < lo
    if hostC or field_in: lab = "RESCUED (EFE)"
    elif not hostU and field_below and COMP[f]: lab = "NOT RESCUED (EFE excluded)"
    else: lab = "NO VERDICT"
    P(f"[{f}] window {lo:.4f}-{hi:.4f} a0; field band {no:.2e}-{mx:.2e} a0 (E1 {gm:.2e}, top+1sig {top:.2e}); hosts central {hostC}, at M_up {hostU};"
      f" complete {COMP[f]} -> {lab}; QX4-reading hosts {[u['name'] for u in nb if u['q'][f]['qx4_reading']]}")
    RES.setdefault("label", {})[f] = dict(label=lab, field_noclu=no, field_maxclu=mx, field_E1=gm, field_top=top, hosts_central=hostC, hosts_upper=hostU,
                                          qx4_reading_hosts=[u["name"] for u in nb if u["q"][f]["qx4_reading"]])
# directed plant (reported): MW-mass host at 100 kpc
for f in FOOT:
    a, _ = qualifies(6e10, 100.0, f); b = qx4_reading(6e10, 100.0, f)
    x = GSI * 6e10 * MSUN / (100 * KPC) ** 2 / FOOT[f]
    P(f"MW-mass host (6e10) at >= 100 kpc [{f}]: g_N(100 kpc) {x:.4f} a0; qualifies Newtonian reading {a}; QX4 reading {b}")
    RES.setdefault("MW_plant", {})[f] = dict(gN_100=x, newtonian=a, qx4_reading=b)
P("kappa = 1/2 FITTED; not theory closed.")
name = "qx14" if MODE == "main" else f"qx14_{MODE}"
json.dump(RES, open(os.path.join(HERE, name + ".json"), "w"), indent=1, default=str)
open(os.path.join(HERE, name + ".out"), "w").write("\n".join(OUT) + "\n")
if MODE == "main":
    with open(os.path.join(HERE, "census.csv"), "w", newline="") as fh:
        w = csv.writer(fh); w.writerow(["name", "sources", "kind", "ra", "dec", "cz", "Rp_kpc", "Mstar", "Mgas", "Mb", "Mb_up", "mass_basis", "gas_basis",
                                        "qual_canon_central", "qual_canon_up", "qual_alt_central", "qual_alt_up", "qx4_reading_canon", "qx4_reading_alt"])
        for u in sorted(U, key=lambda u: u["Rp_kpc"]):
            w.writerow([u["name"], "+".join(u["srcs"]), u["kind"], f"{u['ra']:.5f}", f"{u['dec']:.5f}", "" if u["v"] is None else f"{u['v']:.0f}", f"{u['Rp_kpc']:.1f}",
                        f"{u['Mstar']:.3e}", f"{u['Mgas']:.3e}", f"{u['Mb']:.3e}", f"{u['Mb_up']:.3e}", u["mass_basis"], u["gas_basis"],
                        u["q"]["canonical"]["central"], u["q"]["canonical"]["upper"], u["q"]["alt"]["central"], u["q"]["alt"]["upper"],
                        u["q"]["canonical"]["qx4_reading"], u["q"]["alt"]["qx4_reading"]])
