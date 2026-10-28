#!/usr/bin/env python3
"""BS1_basin_switch: the frozen CL2 picture (S9 shape, L 4, T 10^12.3, measured cluster budget) with the switch keyed on the
BASIN mass - the sum of member M200s inside the zero-velocity surface a system belongs to - instead of the system's own M200.
FROZEN_CRITERIA.md committed alone first (aabf665e07); AMENDMENTS.md A1-A11 committed alone before this script (efc77e8136).

Harnesses executed read-only as text copies (patterns copied from CL2 b57ed8751f / CL3 47625a9db2 / HO2 / HO3):
X43 (SPARC, groups, clusters), X53 (lensing), X51 (dwarfs), HO2's head (MW: GD2 X5 box, GD1 McMillan). Data: UNGC
(Karachentsev+13, CFG548's frame and selection), CFG522's JSON (MW/M31/M33/LMC baryons), Kourkchi & Tully 2017 (record's
matcher `match_kt2017_host`), SPARC positions (record's merged NED/SIMBAD file). Nothing is downloaded.

kappa = 1/2 FITTED; footings never pooled (canonical primary); cold dark energy = gravitating w ~ 0 field component, never a
particle; the basin is a POSIT (nonlocal, no action written); not theory closed; nothing here says the data favour the framework.
Run:  PYTHONHASHSEED=0 OMP_NUM_THREADS=1 nice -n 15 python3 -I bs1_basin_switch.py        (BS1_MUTATE=1 twin: flags inverted)
"""
import os, sys, json, math, time, resource, io, contextlib, csv, importlib.util
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"): os.environ[_v] = "1"
for _v in [k for k in os.environ if k.endswith("_MUTATE") and k != "BS1_MUTATE"] + ["CFG528_POSTFREEZE"]: os.environ.pop(_v, None)
import numpy as np
from scipy import stats
from scipy.optimize import minimize

T0 = time.time(); MUTATE = os.environ.get("BS1_MUTATE", "0") == "1"; TAG = "_MUTATE" if MUTATE else ""
HERE = os.path.dirname(os.path.abspath(__file__)); REB = os.path.dirname(HERE); REPO = os.path.dirname(REB)
DATA = os.path.join(REPO, "real_research", "data"); CFGD = os.path.join(REPO, "campaign_fresh_gravity")
OUT = []
def P(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); OUT.append(s)
def rss(): return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / (1e9 if sys.platform == "darwin" else 1e6)
def rss_all(): return max(rss(), resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss / (1e9 if sys.platform == "darwin" else 1e6))
FEET = ("canonical", "alt"); A0SI = {"canonical": 9.3603e-11, "alt": 1.1312e-10}
TSW = 12.3; UPS_K = 0.6; MK_SUN = 3.28; SEED = 20261027
P(f"BS1_basin_switch  {'MUTATE (basin flags inverted at source; K1 must fail)' if MUTATE else 'normal run'}   criteria aabf665e07, amendments efc77e8136")
P("kappa = 1/2 FITTED; footings never pooled (canonical primary); route E (own M200 halo) iff M_basin > 10^T, else the law on baryons; "
  "the basin is a POSIT (nonlocal, no action); not theory closed")

# ================================================================== the record's M_b -> M200 relation (EM1 R1) and A1's M_b
EM1J = json.load(open(os.path.join(REB, "EM1_emergent_dust_law", "em1_emergent_results.json")))
REL = {t: (EM1J["rows"][t]["R1"]["a"], EM1J["rows"][t]["R1"]["b"]) for t in ("A_c2b_refit", "B_cfg886_bg")}
TAGS = tuple(REL)
def lgM200(lMb, tag="A_c2b_refit"): a, b = REL[tag]; return a + b * (lMb - 10.0)
def mb_of_mstar(Ms):
    """A1: F2's cold-gas relation inside its lens range 8.5 <= log M* <= 11.0, else the record's star factor 1.2."""
    l = math.log10(Ms)
    return Ms * (1.0 + 10 ** (-0.69 * l + 6.63)) if 8.5 <= l <= 11.0 else 1.2 * Ms
P(f"EM1 R1 relations: " + "; ".join(f"{t} a {a} b {b}" for t, (a, b) in REL.items()))

# ================================================================== (a) Local Group: CFG548's frame and selection (copied verbatim)
def vizier_tsv(path):
    rows = [l.rstrip("\n").split("\t") for l in open(path, encoding="latin-1") if l.strip() and not l.startswith("#")]
    hdr = [x.strip() for x in rows[0]]
    return [{hdr[i]: (r[i].strip() if i < len(r) else "") for i in range(len(hdr))} for r in rows[3:]]
def _f(x):
    try: return float(x)
    except Exception: return float("nan")
UNGC = vizier_tsv(os.path.join(DATA, "ungc_karachentsev2013.tsv"))
ACC = ("TRGB", "Cep", "RR", "HB", "SBF", "BS", "CMD", "geom")
def frame(f31):
    nm = np.array([r["Name"].strip() for r in UNGC]); MD = np.array([r["MD"].strip() for r in UNGC])
    ra = np.array([_f(r["_RAJ2000"]) for r in UNGC]); de = np.array([_f(r["_DEJ2000"]) for r in UNGC])
    D = np.array([_f(r["Dist"]) for r in UNGC]) * 1e3; V = np.array([_f(r["Vlg"]) for r in UNGC])
    fD = np.array([r["f_Dist"].strip() for r in UNGC]); Ti = np.array([_f(r["Ti1"]) for r in UNGC])
    un = np.nan_to_num(np.stack([np.cos(np.radians(de)) * np.cos(np.radians(ra)), np.cos(np.radians(de)) * np.sin(np.radians(ra)),
                                 np.sin(np.radians(de))], axis=1))
    i31 = int(np.where(nm == "MESSIER031")[0][0])
    xc = f31 * D[i31] * un[i31]; Dc = float(np.linalg.norm(xc)); nc = xc / Dc
    with np.errstate(all="ignore"):
        cth = un @ nc
        d31 = np.linalg.norm(D[:, None] * un - (D[i31] * un[i31])[None, :], axis=1)
    R = np.sqrt(np.clip(D ** 2 + Dc ** 2 - 2 * D * Dc * cth, 0, None)); Vr = V * (D - Dc * cth) / np.maximum(R, 1e-9)
    Rn = dict(zip(nm, R))
    return dict(name=nm, MD=MD, D=D, V=V, fD=fD, Ti=Ti, R=R, Vr=Vr, Rn=Rn, dMW=D, d31=d31, ra=ra, de=de)
def select(fr, win, groups=True):
    ok = np.isfinite(fr["R"]) & np.isfinite(fr["Vr"]) & np.isin(fr["fD"], ACC) & (fr["R"] >= win[0]) & (fr["R"] <= win[1])
    if groups:
        keep = np.array([(md in ("Milky Way", "MESSIER031", "MESSIER033")) or (np.isfinite(ti) and ti <= 0)
                         or (fr["Rn"].get(md, np.inf) < 1500.0) for md, ti in zip(fr["MD"], fr["Ti"])])
        ok &= keep
    return ok
def linfit_R0(R, Vr):
    A = np.vstack([R, np.ones_like(R)]).T
    (s, b), *_ = np.linalg.lstsq(A, Vr, rcond=None)
    return -b / s, s * 1e3, float(np.std(Vr - (s * R + b)))
FR = frame(2 / 3); SEL = select(FR, (600.0, 2500.0)); Rd, Vd = FR["R"][SEL], FR["Vr"][SEL]
R0D, H_lin, rms_lin = linfit_R0(Rd, Vd); R0D = float(R0D)
rngb = np.random.default_rng(SEED); boots = []
for _ in range(400):
    ii = rngb.integers(0, len(Rd), len(Rd)); boots.append(float(linfit_R0(Rd[ii], Vd[ii])[0]))
R0SIG = float(np.std(boots))
J548 = json.load(open(os.path.join(CFGD, "CFG548_local_group_zero_velocity_surface", "cfg548_results.json")))
mine = sorted((str(n), float(r), float(v)) for n, r, v in zip(FR["name"][SEL], Rd, Vd)); ref = sorted((s["name"], s["R_kpc"], s["Vr"]) for s in J548["sample"])
k2a = len(mine) == len(ref) and all(a[0] == b[0] and abs(a[1] - b[1]) < 1e-6 and abs(a[2] - b[2]) < 1e-6 for a, b in zip(mine, ref))
P(f"\n=== (a) LG: CFG548 frame f31 2/3, selection 0.6-2.5 Mpc: N {SEL.sum()} (reproduces CFG548's committed sample: {'PASS' if k2a else 'FAIL'})")
P(f"  straight-line fit V_r = {H_lin:.1f} km/s/Mpc (R - R0), rms {rms_lin:.1f} km/s -> R0_data = {R0D:.1f} +- {R0SIG:.1f} kpc (bootstrap 400, seed {SEED}); "
  f"NOT CFG548's model-based 830 kpc")

J522 = json.load(open(os.path.join(CFGD, "CFG522_local_group_timing", "cfg522_results.json")))["D6"]
BIG4 = {"Milky Way": J522["MW"]["M_b"], "MESSIER031": J522["M31"]["M_b"], "MESSIER033": J522["M33"]["M_b"],
        "LMC": J522["MW+M31+M33+LMC"]["M_b"] - J522["MW"]["M_b"] - J522["M31"]["M_b"] - J522["M33"]["M_b"]}
KLUM = {r["Name"].strip(): _f(r["KLum"]) for r in UNGC}
def lg_basin(R0, ups=UPS_K, summed=False):
    inside = [str(n) for n, r in zip(FR["name"], FR["R"]) if np.isfinite(r) and r < R0]
    Mb, skipped = {}, []
    for n in inside:
        if n in BIG4: Mb[n] = BIG4[n]
        elif np.isfinite(KLUM.get(n, float("nan"))): Mb[n] = mb_of_mstar(ups * 10 ** KLUM[n])
        else: skipped.append(n)
    big_in = [n for n in BIG4 if n in Mb]
    if summed: M = 10 ** lgM200(math.log10(sum(Mb.values())))
    else: M = float(sum(10 ** lgM200(math.log10(v)) for v in Mb.values()))
    M4 = float(sum(10 ** lgM200(math.log10(BIG4[n])) for n in big_in))
    return dict(lgM=math.log10(M), lgM_big4=math.log10(M4) if M4 > 0 else None, n_members=len(inside), n_massed=len(Mb), n_skipped=len(skipped),
                skipped=sorted(skipped), big4_inside=big_in, members=sorted(inside))
LGP = lg_basin(R0D)
P(f"  LG basin (R < R0_data): {LGP['n_members']} UNGC rows, {LGP['n_massed']} with a mass, {LGP['n_skipped']} without KLum (skipped; lower bound); "
  f"big four inside: {LGP['big4_inside']}; log M_basin {LGP['lgM']:.4f} (big four alone {LGP['lgM_big4']:.4f}) vs T 12.3 -> {'ROUTE E' if LGP['lgM'] > TSW else 'LAW'}")
P("  own log M200 (A): " + "; ".join(f"{n} {lgM200(math.log10(v)):.3f}" for n, v in BIG4.items()))

# field dwarfs (A5) and the satellites (rule f)
X1 = list(csv.DictReader(open(os.path.join(REB, "X1_hosted_recount", "x1_per_system.csv"))))
DWARFS = {}
for r in X1:
    if r["footing"] == "canonical": DWARFS[r["name"]] = dict(host=r["host"], cls=r["cls"], lm=float(r["logMstar"]))
UMAP = {"Aquarius": "DDO210", "Cetus": "Cetus", "IC 1613": "IC1613", "Leo A": "LeoA", "Leo T": "LeoT", "NGC 6822": "NGC6822",
        "Pegasus dIrr": "Pegasus", "Phoenix": "Phoenix", "Sagittarius dIrr": "Sag dIr", "Tucana": "Tucana", "UGC 4879": "UGC04879", "WLM": "WLM"}
FIELD = sorted(n for n, d in DWARFS.items() if d["host"] not in ("MW", "M31"))
assert len(FIELD) == 13 and set(UMAP) == set(FIELD) - {"Antlia B"}, FIELD
def field_R(n, antlia_var=False):
    if n == "Antlia B": return float(FR["Rn"]["NGC3109"]) if antlia_var else None
    return float(FR["Rn"][UMAP[n]])
P("  field dwarfs, barycentric R (kpc): " + "; ".join(f"{n} {field_R(n):.0f}" if field_R(n) is not None else f"{n} (not in UNGC)" for n in FIELD))

# ================================================================== (b) SPARC: positions, UNGC (A6), KT2017 (record's matcher)
MRT = {}
for line in open(os.path.join(DATA, "SPARC_Lelli2016c.mrt")):
    tok = line.split()
    if len(tok) != 19: continue
    try: v = [float(t) for t in tok[1:18]]
    except ValueError: continue
    MRT[tok[0]] = dict(D=v[1], lMb=math.log10((0.5 * v[6] + 1.33 * v[12]) * 1e9))
SNAMES = sorted(f.replace("_rotmod.dat", "") for f in os.listdir(os.path.join(DATA, "sparc_data")) if f.endswith("_rotmod.dat"))
SNAMES = [n for n in SNAMES if n in MRT]
OWN = {t: {n: 10 ** lgM200(MRT[n]["lMb"], t) for n in SNAMES} for t in TAGS}
POS = json.load(open(os.path.join(DATA, "sparc_positions_merged.json")))
_spec = importlib.util.spec_from_file_location("cosmicweb_ro", os.path.join(REPO, "real_research", "reviews", "project_sparc_a0_vs_cosmicweb.py"))
CW = importlib.util.module_from_spec(_spec); _spec.loader.exec_module(CW)
KTG, KTGRP = CW.load_kt2017()
KS = []
for ln in open(CW.KTGAL):                                                          # the same row filter as load_kt2017, plus Ksmag
    if ln.startswith("#") or not ln.strip(): continue
    p = ln.rstrip("\n").split("\t")
    if p[0].strip() == "PGC" or p[0].startswith("---") or len(p) < 6: continue
    try: row = (float(p[1]), float(p[2]), float(p[3]), int(p[5]))
    except Exception: continue
    KS.append(_f(p[4]))
KS = np.array(KS); assert len(KS) == len(KTG)
GDIST = {}
for r in vizier_tsv(os.path.join(DATA, "kt2017_groups_full.tsv")):
    try: GDIST[int(r["PGC1"])] = _f(r["Dist"])
    except ValueError: pass
UNGC_RA, UNGC_DE = FR["ra"], FR["de"]
SP = {}
for n in SNAMES:
    p = POS.get(n); d = dict(pos=p is not None and p.get("ra") is not None, cz=(p or {}).get("cz"))
    if d["pos"]:
        sep = np.degrees(CW.angsep_rad(p["ra"], p["dec"], np.nan_to_num(UNGC_RA), np.nan_to_num(UNGC_DE)))
        j = int(np.argmin(sep)); d["ungc"] = str(FR["name"][j]) if sep[j] < 0.05 else None
        d["ungc_R"] = float(FR["R"][j]) if sep[j] < 0.05 else None
    if d["pos"] and d["cz"] is not None:
        host = CW.match_kt2017_host(p["ra"], p["dec"], p["cz"], KTG, KTGRP)
        sep = np.degrees(CW.angsep_rad(p["ra"], p["dec"], KTG[:, 0], KTG[:, 1])); cand = (sep < 0.05) & (np.abs(KTG[:, 2] - p["cz"]) < 350.0)
        if cand.any():
            i = int(np.where(cand)[0][np.argmin(sep[cand])]); pg = int(KTG[i, 3])
            assert KTGRP.get(pg) == host
            mem = [int(k) for k in np.where(KTG[:, 3] == pg)[0] if int(k) != i]
            d.update(kt=dict(pgc1=pg, Nm=(host[0] if host else None), self_row=i, others=mem, dist=GDIST.get(pg, float("nan"))))
    SP[n] = d
def sparc_basins(R0, lgLG, ups=UPS_K, mode="primary"):
    """{tag: {name: M_basin (Msun)}} for galaxies with a multi-member basin; others absent (= alone, CL2 flag).
    mode: primary (A2 self term) | summed | allKs | distfb (group without Dist takes the SPARC distance)."""
    out = {t: {} for t in TAGS}; info = {}
    for n, d in SP.items():
        if d.get("ungc_R") is not None and d["ungc_R"] < R0:
            for t in TAGS: out[t][n] = 10 ** lgLG
            info[n] = dict(kind="LG", ungc=d["ungc"], R=d["ungc_R"]); continue
        kt = d.get("kt")
        if kt is None or kt["Nm"] is None or kt["Nm"] < 2: continue
        dist = kt["dist"]
        if not np.isfinite(dist):
            if mode != "distfb": info[n] = dict(kind="no Dist", pgc1=kt["pgc1"], Nm=kt["Nm"]); continue
            dist = MRT[n]["D"]
        rows = kt["others"] + ([kt["self_row"]] if mode == "allKs" else [])
        mbs = []
        for k in rows:
            if not np.isfinite(KS[k]): continue
            lL = -0.4 * (KS[k] - 5 * math.log10(dist) - 25.0 - MK_SUN); mbs.append(mb_of_mstar(ups * 10 ** lL))
        for t in TAGS:
            if mode == "summed": M = 10 ** lgM200(math.log10(10 ** MRT[n]["lMb"] + sum(mbs)), t)
            elif mode == "allKs": M = float(sum(10 ** lgM200(math.log10(m)) for m in mbs))
            else: M = OWN[t][n] + float(sum(10 ** lgM200(math.log10(m)) for m in mbs))
            out[t][n] = M
        info[n] = dict(kind="KT2017", pgc1=kt["pgc1"], Nm=kt["Nm"], n_rows_used=len(mbs), n_rows_noKs=len(rows) - len(mbs), dist=dist)
    return out, info
nmatch = sum(1 for d in SP.values() if d.get("kt")); nmulti = sum(1 for d in SP.values() if d.get("kt") and d["kt"]["Nm"] and d["kt"]["Nm"] >= 2)
nodist = sum(1 for d in SP.values() if d.get("kt") and d["kt"]["Nm"] and d["kt"]["Nm"] >= 2 and not np.isfinite(d["kt"]["dist"]))
inLG = sorted(n for n, d in SP.items() if d.get("ungc_R") is not None and d["ungc_R"] < R0D)
KTSTAT = dict(n_sparc=len(SNAMES), n_pos=sum(d["pos"] for d in SP.values()), n_cz=sum(d["pos"] and d["cz"] is not None for d in SP.values()),
              n_matched=nmatch, n_multi=nmulti, n_multi_no_dist=nodist, in_LG=inLG)
P(f"\n=== (b) SPARC basins: {KTSTAT['n_sparc']} galaxies; {KTSTAT['n_pos']} with a position, {KTSTAT['n_cz']} with cz; KT2017 matched {nmatch} "
  f"(record's matcher 0.05 deg / 350 km/s), Nm >= 2: {nmulti}, of which {nodist} groups lack Dist (kept on CL2 flag, A3); inside R0_data (rule a): {inLG}")

# ================================================================== flag tables (per configuration)
def dwarf_flags(R0, lgLG, T, antlia_var=False):
    """{f: {name: flag}}: satellites -> LG flag (rule f); field -> LG flag if R < R0, else alone (own M200 on A1's M_b)."""
    out = {}
    for f in FEET:
        lg_ok = lgLG > T[f]; d = {}
        for n, x in DWARFS.items():
            if x["host"] in ("MW", "M31"): d[n] = lg_ok
            else:
                R = field_R(n, antlia_var)
                d[n] = lg_ok if (R is not None and R < R0) else (10 ** lgM200(math.log10(mb_of_mstar(10 ** x["lm"]))) > 10 ** T[f])
        out[f] = d
    return out
def dwarf_flags_alone():
    return {f: {n: x["host"] in ("MW", "M31") for n, x in DWARFS.items()} for f in FEET}            # CL2's own flags
CFG = dict(T={f: TSW for f in FEET}, SP=None, DW=dwarf_flags_alone(), MW=None)
FLOG, DLOG, MWLOG = [], [], []
def BS1_FLAG(name, tag, f, M200, a_):
    sp = CFG["SP"]; Mb = sp[tag].get(name) if sp is not None else None
    flag = bool((Mb if Mb is not None else M200) > 10 ** CFG["T"][f])
    if MUTATE: flag = not flag
    FLOG.append((name, tag, f, flag, float(M200), bool(a_))); return flag
def BS1_DFLAG(name, f):
    flag = bool(CFG["DW"][f][name])
    if MUTATE: flag = not flag
    DLOG.append((name, f, flag)); return flag
def BS1_MWFLAG(lM, foot):
    flag = bool(lM > CFG["T"][foot]) if CFG["MW"] is None else bool(CFG["MW"][foot])
    if MUTATE: flag = not flag
    MWLOG.append((foot, float(lM), flag)); return flag

# ================================================================== the law floor + scorers (CL2/CL3 copies; MUTATE acts at the flag source)
MODE = {"m": "on"}; STAT = {}
def _new(): return dict(n=0, viol=0, law=0)
def nu(y): return 0.5 + np.sqrt(0.25 + 1.0 / y)
def _combine(law, rE, key, above):
    if MODE["m"] == "off": return rE
    if MODE["m"] == "law": return law
    out = rE if above else law
    s = STAT.setdefault(key, _new()); tol = 1e-12 * np.maximum(np.abs(out), 1e-300)
    s["n"] += 1; s["viol"] += int(np.any(np.abs(out - (rE if above else law)) > tol)); s["law"] += int(not above)
    return out
LAST = {"law": False}
def LF_G(gb, gh, a0, key="g", above=False):
    gb = np.asarray(gb, float); gh = np.broadcast_to(np.asarray(gh, float), np.broadcast(gb, np.asarray(gh)).shape)
    gbb = np.broadcast_to(gb, gh.shape); pos = gbb > 0
    law = np.where(pos, nu(np.where(pos, gbb, 1.0) / a0) * gbb, gbb)
    return _combine(law, gbb + gh, key, bool(above))
def LF_M(Mb, Mh, r, G, a0, key="M", above=False):
    Mb = np.asarray(Mb, float); Mh = np.asarray(Mh, float); r = np.asarray(r, float)
    with np.errstate(divide="ignore", invalid="ignore"):
        law = np.where((r > 0) & (Mb > 0), Mb * nu(np.maximum(G * Mb / np.where(r > 0, r, 1.0) ** 2, 1e-300) / a0), Mb)
    out = _combine(law, Mb + Mh, key, bool(above))
    LAST["law"] = bool(MODE["m"] == "law" or (MODE["m"] == "on" and not bool(above)))
    return out
def run_copy(src_path, edits, fname, extra=None):
    src = open(src_path).read()
    for old, new in edits:
        assert src.count(old) == 1, (src_path, old[:60]); src = src.replace(old, new)
    ns = {"__file__": os.path.join(HERE, fname), "__name__": fname[:-3], "LF_G": LF_G, "LF_M": LF_M, "LAST": LAST,
          "BS1_FLAG": BS1_FLAG, "BS1_DFLAG": BS1_DFLAG}
    if extra: ns.update(extra)
    argv0 = sys.argv; sys.argv = [ns["__file__"]]
    try:
        with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
            try: exec(compile(src, ns["__file__"], "exec"), ns)
            except SystemExit: pass
    finally:
        sys.argv = argv0
    return ns

B1 = 3 * math.log(2) - math.pi / 2
S_MEAS = json.load(open(os.path.join(REB, "GS1_measured_gas_outskirts", "gs1_gas_slope_results.json")))["slope"]["s_meas"]
NAT_h, NAT_OM, NAT_wb = 0.6856427, 0.2976016, 0.0223081
NAT_OB = NAT_wb / NAT_h ** 2; NAT_RRAT = (NAT_OM - NAT_OB) / NAT_OB
GC2X = """
GC2_LOG = []
def _gc2_ext(Mg500, R500, z, Mbt_cut):
    r = RG; rc = 0.15*R500; beta = 2/3; sh = (1 + (r/rc)**2)**(-1.5*beta)
    Rm = R500; sm = (1 + (Rm/rc)**2)**(-1.5*beta)
    sh = np.where(r > Rm, sm*(r/Rm)**-GC2_SLOPE, sh)
    dm = 4*np.pi*(r*MPC)**2*sh; M = np.r_[0, np.cumsum(0.5*(dm[1:] + dm[:-1])*np.diff(r*MPC))]
    Mbx = 1.2*M*(Mg500*MSUN/np.interp(R500, r, M))
    rta = r_ta_com(Mbt_cut)/(1 + z)
    for n in range(1, 200):
        Mbt = float(np.interp(rta, RM, Mbx)); new = r_ta_com(Mbt)/(1 + z)
        if abs(new/rta - 1) < 1e-6: rta = new; break
        rta = new
    Mbt = float(np.interp(rta, RM, Mbx))
    GC2_LOG.append(float(Mbt/Mbt_cut))
    return np.where(RM <= rta, Mbx, Mbt), Mbt
"""
def budget_edit():
    old_prep = '    Mg500 = cl["Mgas500"]*qd**2.5; R500 = cl["R500"]*qd; Mg, rho_g = gas(Mg500, R500, "P"); Mb = Mg*(1 + 0.20); Mbt = float(Mb[-1])'
    pre = 'NX = {"__file__": X30SRC, "__name__": "x30_ro", "GC2_SLOPE": %r}\n' % S_MEAS
    pre += 'assert codeX.count(%r) == 1\n' % old_prep
    pre += 'codeX = codeX.replace(%r, %r)\n' % (old_prep, old_prep + '\n    Mb, Mbt = _gc2_ext(Mg500, R500, cl["z"], Mbt)')
    pre += 'codeX = codeX.replace("PREP = {}\\ndef prep", %r + "PREP = {}\\ndef prep")\n' % GC2X
    pre += ('codeX = codeX.replace("H0_946 = 67.4e3/MPC946", "H0_946 = %r*100e3/MPC946")\n'
            'codeX = codeX.replace("OB946 = 0.0493; OC946 = 5.364*OB946", "OB946 = %r; OC946 = %r*OB946")\n'
            'codeX = codeX.replace("Mfair=5.364*Mbt", "Mfair=%r*Mbt")\n'
            'assert all(t in codeX for t in ("_gc2_ext", "H0_946 = %r", "Mfair=%r"))' % (NAT_h, NAT_OB, NAT_RRAT, NAT_RRAT, NAT_h, NAT_RRAT))
    return ('NX = {"__file__": X30SRC, "__name__": "x30_ro"}', pre)
_A2 = json.load(open(os.path.join(REB, "X48_native_cf_zoom", "x48_analyze_results_ng48_A2.json")))
S9 = [_A2["cf_by_mass"][k] for k in ("1e+12", "1e+13", "1e+14")]
def cf_table(L): return [L * v / S9[2] for v in S9]
def tstr(T): return f"{T['canonical']}" if T["canonical"] == T["alt"] else "{'canonical': %r, 'alt': %r}[%s]" % (T["canonical"], T["alt"], "{F}")
def run_x43(L, T, label):
    MODE["m"] = "on"; tab = cf_table(L)
    ETAF = (lambda M, tab=tab: 4.0 / (3.0 * B1) * float(np.interp(math.log10(M), [12.0, 13.0, 14.0], tab)) ** 1.25)
    ed = [('sc = ETA_USE["v"] * sigma_coll(tag, M)[0] * MSUNE / PC2',
           'sc = (ETA_FUN(M) if (ETA_FUN is not None and ETA_USE["v"] == ETA) else ETA_USE["v"]) * sigma_coll(tag, M)[0] * MSUNE / PC2'),
          ('rows.append(fit_one(q, np.log10(np.maximum(q["GB"] + (GE * Mh / q["Rm"] ** 2)[:, None], 1e-300))))',
           'rows.append(fit_one(q, np.log10(np.maximum(LF_G(q["GB"], (GE * Mh / q["Rm"] ** 2)[:, None], A0[f], "sparc", a_), 1e-300))))'),
          ("        s, a_ = sig_core(f, tag, M200, rule); act += a_",
           "        s, a_ = sig_core(f, tag, M200, rule); a_ = BS1_FLAG(q['name'], tag, f, M200, a_) if rule else a_; act += a_"),
          ('V[i] = dvecN(int(i), foot, hk, pp["Mb"] + Mh)', 'V[i] = dvecN(int(i), foot, hk, LF_M(pp["Mb"], Mh, RM, GX, A0[foot], "clusters", a_))'),
          ('Mh = math.pi * sc * r0 ** 2 * B(np.minimum(rr, R200) / r0); gN = gN + Mh / Mb / XG ** 2',
           'Mh = math.pi * sc * r0 ** 2 * B(np.minimum(rr, R200) / r0); gN = LF_G(gN, Mh / Mb / XG ** 2, A0[foot] / (G540 * Mb / a ** 2), "groups" if dlM == 0.0 else "groups_d", act)'),
          ("for cf in (3.0, 5.0):", "for cf in ():"),
          ('f"x43_collapse_core{TAG}.out"', f'"bs1_x43copy_{label}{TAG}.out"'), ('f"x43_collapse_core_results{TAG}.json"', f'"bs1_x43copy_{label}{TAG}_results.json"'),
          ('"x43_x30_machinery"', '"bs1_x30_machinery"'),
          ("    return max(s, sc), sc > s", "    return max(s, sc), M > 10 ** " + tstr(T).replace("{F}", "f")), budget_edit()]
    ns = run_copy(os.path.join(REB, "X43_collapse_core_floor", "x43_collapse_core.py"), ed, "bs1_x43copy.py", {"ETA_FUN": ETAF})
    return ns["RES"]
def run_x53(mode, L, T, label):
    MODE["m"] = mode
    ed = [('return Mb + Mh, (M200, R200, Sig, above)', 'return LF_M(Mb, Mh, RGRID_PC, Gpc, a0u(foot), "lensing", above), (M200, R200, Sig, above)'),
          ('tab[gi] = AQ.delta_sigma(Rn[b] * 1e6, RGRID_PC, M, "const")', 'tab[gi] = AQ.delta_sigma(Rn[b] * 1e6, RGRID_PC, M, "linear" if (halo and LAST["law"]) else "const")'),
          ('os.path.join(HERE, "x53_step0_results.json")', repr(os.path.join(REB, "X53_outer_lensing_law_vs_halos", "x53_step0_results.json"))),
          ('H_PRIMARY = dict(bg="A_c2b_refit", cf="cf4", zR200=None)', 'H_PRIMARY = dict(bg="A_c2b_refit", cf="x48", zR200=None)'),
          ("absorbed=1 - res / e0", "absorbed=1 - res / max(e0, 1e-300)"), ("100 * (1 - res / e0)", "100 * (1 - res / max(e0, 1e-300))"),
          ("{25.0 / e:.2f}", "{25.0 / max(e, 1e-300):.2f}"),
          ('f"x53_outer_lensing_results{SFX}.json"', f'"bs1_x53copy_{mode}_{label}{TAG}_results.json"'), ('f"x53_outer_lensing{SFX}.out"', f'"bs1_x53copy_{mode}_{label}{TAG}.out"'),
          ('cf = 4.0 if cfmode == "cf4" else float(np.interp(math.log10(M), CF48_L, CF48_C))', "cf = float(np.interp(math.log10(M), [12.0, 13.0, 14.0], %r))" % cf_table(L)),
          ("return M200, R200, solve_r0(M200, R200, Sig), Sig, sc > SIGA0[foot]", "return M200, R200, solve_r0(M200, R200, Sig), Sig, M200 > 10 ** " + tstr(T).replace("{F}", "foot"))]
    ns = run_copy(os.path.join(REB, "X53_outer_lensing_law_vs_halos", "x53_outer_lensing.py"), ed, "bs1_x53copy.py")
    return ns["FT"]
ALLCLS = tuple(dict.fromkeys(r["cls"] for r in X1))
def run_x51(label):
    MODE["m"] = "on"
    ed = [("gp = gN + G * Mh / r12 ** 2", 'gp = float(LF_G(gN, G * Mh / r12 ** 2, A0[f], "dwarfs", BS1_DFLAG(r["name"], f)))'),
          ('out.append(dict(name=r["name"], cls=r["cls"],', 'out.append(dict(host=r["host"], gp=gp, gN=gN, gh=G * Mh / r12 ** 2, gobs=gobs, name=r["name"], cls=r["cls"],'),
          ('f"x51_dwarfs{TAG}.out"', f'"bs1_x51copy_{label}{TAG}.out"'), ('f"x51_dwarfs_results{TAG}.json"', f'"bs1_x51copy_{label}{TAG}_results.json"')]
    ns = run_copy(os.path.join(REB, "X51_dwarf_cooling_floor", "x51_dwarfs.py"), ed, "bs1_x51copy.py")
    rows = {f: ns["rows"](f, ALLCLS) for f in FEET}
    return dict(RES=ns["RES"], rows=rows)

# ---- HO2's head (MW machinery), read-only text copy; the branch flag goes through BS1_MWFLAG
HO2SRC = os.path.join(REB, "HO2_sluggs_milkyway_heldout", "ho2_heldout.py"); _t = open(HO2SRC).read()
_t = _t[:_t.index("# ================================================================== orchestration")]
_old = 'bg = BGR[tag]; lM = bg["a"] + bg["b"] * (math.log10(Mb) - 10); flag = lM > TSW'; assert _t.count(_old) == 1
_t = _t.replace(_old, 'bg = BGR[tag]; lM = bg["a"] + bg["b"] * (math.log10(Mb) - 10); flag = BS1_MWFLAG(lM, foot)')
HO2NS = {"__file__": os.path.join(HERE, "bs1_ho2copy.py"), "__name__": "bs1_ho2copy", "BS1_MWFLAG": BS1_MWFLAG}
with contextlib.redirect_stdout(io.StringIO()):
    exec(compile(_t, HO2NS["__file__"], "exec"), HO2NS)
CF_TAB0 = list(HO2NS["CF_TAB"])
def run_sigma(): return HO2NS["child_sigma"]()
def run_mw(L):
    HO2NS["CF_TAB"][:] = cf_table(L); return HO2NS["child_mw"]()

import multiprocessing as _mp
def _child(name, cfg, args):
    CFG.update(cfg); STAT.clear(); FLOG.clear(); DLOG.clear(); MWLOG.clear()
    r = globals()[name](*args)
    return r, {k: dict(v) for k, v in STAT.items()}, list(FLOG), list(DLOG), list(MWLOG)
def call(fn, *args):
    """K3: every scorer runs in its own forked process (one thread); the flag configuration is passed explicitly."""
    with _mp.get_context("fork").Pool(1, maxtasksperchild=1) as pool:
        return pool.apply(_child, (fn.__name__, dict(CFG), args))

# ================================================================== CL2's grade (verbatim logic) + HO3's rules
def grade(R43_, F53_, F53re_, R51_, lab, quiet=False):
    out = {}
    for f in FEET:
        F = R43_["footings"][f]; sp = {t: F["sparc"][t] for t in F["sparc"]}; gr = F["groups"]; cl = F["clusters"]
        c0 = cl["cells"]["h0672"]; dw = R51_["footings"][f]["classes"]
        Lf, Lre = F53_[f]["all"], F53re_[f]["all"]
        dL = Lf["H2H"]["chi2"] - Lf["L2H"]["chi2"]; dE = Lf["H2H"]["chi2"] - Lre["H2H"]["chi2"]
        dLp = F53_[f]["primary"]["H2H"]["chi2"] - F53_[f]["primary"]["L2H"]["chi2"]
        fails = []
        if not all(s["line"] for s in sp.values()): fails.append("SPARC line")
        if not gr["PASS"]: fails.append(f"groups ({gr['verdict']}, Z {gr['Z']:+.2f})")
        fails += cl["fails"]
        fails += [f"dwarfs {c} ({'UNDER' if v['median'] > 0 else 'OVER'}, Z {v['Z']:+.2f})" for c, v in dw.items() if not abs(v["Z"]) < 2]
        if not (dL <= 9.0 and dE < 0): fails.append(f"lensing (ENV2H-L2H {dL:+.1f}, ENV2H-H2H {dE:+.1f})")
        v = "ENVIRONMENT SWITCH UNIFIES" if not fails else "ENV FAILS: " + ", ".join(fails)
        if not quiet:
            P(f"\n  [{f}] {lab}")
            for t, s in sp.items(): P(f"    SPARC [{t}]: rms {s['rms']:.4f}, median U {s['U_median']:.2f}, line {'PASS' if s['line'] else 'FAIL'}; route E in {s['n_active']}/175")
            P(f"    groups: mean {gr['mean']:+.4f} Z {gr['Z']:+.2f} -> {gr['verdict']}")
            P("    clusters: " + "; ".join(f"{k} Z {c0[k]['Z']:+.2f}{'' if cl['ok'][k] else ' FAIL'}" for k in c0))
            P("    dwarfs: " + "; ".join(f"{c} {d['median']:+.3f} (Z {d['Z']:+.2f})" for c, d in dw.items()))
            P(f"    lensing: dchi2(ENV2H-L2H) {dL:+.1f}, dchi2(ENV2H-H2H) {dE:+.1f}")
            P(f"    -> {'every CL2 line passes' if not fails else 'fails: ' + ', '.join(fails)}")
        out[f] = dict(verdict=v, fails=fails, sparc={t: dict(rms=s["rms"], U=s["U_median"], line=s["line"]) for t, s in sp.items()},
                      groups=dict(mean=gr["mean"], Z=gr["Z"], verdict=gr["verdict"]), clusters={k: dict(pred=c0[k]["pred"], meas=c0[k]["meas"], Z=c0[k]["Z"], ok=cl["ok"][k]) for k in c0},
                      dwarfs={c: dict(median=d["median"], Z=d["Z"]) for c, d in dw.items()},
                      lensing=dict(L2H=Lf["L2H"]["chi2"], ENV2H=Lf["H2H"]["chi2"], H2H=Lre["H2H"]["chi2"], d_LF_L=dL, d_LF_H=dE, d_LF_L_primary=dLp))
        out[f]["n_routeE_sparc"] = {t: int(s["n_active"]) for t, s in sp.items()}
    return out
P0, PMIN = 0.0455, 0.01; S2T = {}
def thr(N):
    if N not in S2T:
        rng = np.random.default_rng(SEED); qs = []
        for _ in range(4): qs.append(np.median(np.abs(rng.standard_normal((50000, N))), axis=1))
        S2T[N] = float(np.percentile(np.concatenate(qs), 99))
    return S2T[N]
def rules(Z):
    Z = np.asarray(Z, float); N = len(Z); a = np.abs(Z)
    k = int((a >= 2).sum()); p1 = float(stats.binom.sf(k - 1, N, P0))
    med = float(np.median(a)); t2 = thr(N)
    zmax = float(a.max()); p2 = float(2 * stats.norm.sf(zmax)); p3 = float(-math.expm1(N * math.log1p(-p2))) if p2 < 1 else 1.0
    ok = dict(S1=bool(p1 >= PMIN), S2=bool(med <= t2), S3=bool(p3 >= PMIN))
    return dict(N=N, k_beyond2=k, S1_p=p1, median_absZ=med, S2_threshold=t2, maxabsZ=zmax, S3_p=p3, ok=ok,
                verdict="CONSISTENT WITH ERRORS" if all(ok.values()) else "EXCESS SCATTER: " + ", ".join(r for r, v in ok.items() if not v))
def dwarf_grade(R51x, lab, quiet=False):
    out = {}
    for f in FEET:
        R = R51x["rows"][f]; rowsf = []
        for x in R:
            x = dict(x); x["Z"] = x["E"] / x["s"]; rowsf.append(x)
        sat = [x for x in rowsf if x["host"] in ("MW", "M31")]; iso = sorted([x for x in rowsf if x["host"] not in ("MW", "M31")], key=lambda x: x["name"])
        g_iso = rules([x["Z"] for x in iso]); g_sat = rules([x["Z"] for x in sat])
        per = {x["name"]: dict(E=x["E"], s=x["s"], Z=x["Z"], branch="route E halo" if CFGFLAG(R51x, f, x["name"]) else "law") for x in iso}
        flags = {nm: dict(per[nm], flag="ABOVE PICTURE" if per[nm]["Z"] >= 2 else ("BELOW PICTURE" if per[nm]["Z"] <= -2 else "CONSISTENT")) for nm in ("Leo T", "Phoenix", "IC 1613")}
        out[f] = dict(isolated=g_iso, satellites=g_sat, per_field=per, flags=flags, beyond2=sorted([(x["name"], round(x["Z"], 2)) for x in iso if abs(x["Z"]) >= 2], key=lambda t: -abs(t[1])))
        if not quiet:
            P(f"  [{f}] {lab}: field N {g_iso['N']}: |Z|>=2 {g_iso['k_beyond2']} (S1 p {g_iso['S1_p']:.2e} {'PASS' if g_iso['ok']['S1'] else 'FAIL'}); "
              f"median|Z| {g_iso['median_absZ']:.2f} vs {g_iso['S2_threshold']:.2f} ({'PASS' if g_iso['ok']['S2'] else 'FAIL'}); max|Z| {g_iso['maxabsZ']:.2f} "
              f"(S3 p {g_iso['S3_p']:.2e} {'PASS' if g_iso['ok']['S3'] else 'FAIL'}) -> {g_iso['verdict']}")
            P("     field per object: " + "; ".join(f"{n} {v['E']:+.3f}+-{v['s']:.3f} (Z {v['Z']:+.2f}, {'halo' if v['branch'].startswith('route') else 'law'})" for n, v in per.items()))
            P(f"     satellites N {g_sat['N']}: {g_sat['verdict']}")
    return out
def CFGFLAG(R51x, f, name): return R51x["flags"][f][name]

def flat(d, pre=""):
    if isinstance(d, dict):
        o = {}
        for k, v in d.items(): o.update(flat(v, f"{pre}/{k}"))
        return o
    if isinstance(d, (list, tuple)): return {pre: tuple(d)} if all(isinstance(x, str) for x in d) else {f"{pre}[{i}]": x for i, x in enumerate(d)}
    if isinstance(d, np.bool_): return {pre: bool(d)}
    return {pre: d}
def same(a, b, tol=1e-6):
    fa, fb = flat(a), flat(b); bad = []
    if set(fa) != set(fb): return False, ["keys differ: " + str(sorted(set(fa) ^ set(fb))[:5])]
    for k in fa:
        x, y = fa[k], fb[k]
        if isinstance(x, (bool, str, tuple)) or isinstance(y, (bool, str, tuple)) or x is None:
            if x != y: bad.append(k)
        elif abs(x - y) > tol * max(1.0, abs(y)): bad.append(k)
    return not bad, bad[:5]

checks = []; RES = dict(criteria="aabf665e07", amendments="efc77e8136", mutate=MUTATE,
                        picture=dict(shape="S9", L=4.0, T=TSW, cf_table=cf_table(4.0), budget="GS1 measured"))
RES["LG"] = dict(R0_data_kpc=R0D, R0_sigma_kpc=R0SIG, H_lin=H_lin, rms_lin=rms_lin, N_fit=int(SEL.sum()), basin=LGP,
                 field_R_kpc={n: field_R(n) for n in FIELD}, antlia_B_at_NGC3109_R=field_R("Antlia B", True))
RES["KT2017"] = KTSTAT

# ================================================================== STEP 0 / K0: every basin = the system alone
P("\n=== STEP 0 (K0): basin = the system alone (satellites keep CL2's satellite clause)")
CFG.update(T={f: TSW for f in FEET}, SP=None, DW=dwarf_flags_alone(), MW=None)
r43_0, st, fl0, _, _ = call(run_x43, 4.0, CFG["T"], "K0_alone"); P(f"  X43 copy done [{time.time() - T0:.0f} s]")
F53on, _, _, _, _ = call(run_x53, "on", 4.0, CFG["T"], "K0"); F53off, _, _, _, _ = call(run_x53, "off", 4.0, CFG["T"], "K0"); P(f"  X53 copies done [{time.time() - T0:.0f} s]")
r51_0, st51, _, dl0, _ = call(run_x51, "K0_alone"); r51_0["flags"] = CFG["DW"]
g0 = grade(r43_0, F53on, F53off, r51_0["RES"], "K0 (basin alone)", quiet=True)
CL2J = json.load(open(os.path.join(REB, "CL2_native_cf_slope", "cl2_native_slope_results.json")))["S9_L4"]["grade"]
g0cmp = {f: {k: v for k, v in g0[f].items() if k != "n_routeE_sparc"} for f in FEET}
k0a, bad = same(g0cmp, CL2J)
P(f"  K0a CL2 S9 L4 committed grade, every leaf (both footings) to 1e-6, fail lists exact: {'PASS' if k0a else 'FAIL ' + str(bad)}")
for f in FEET: P(f"    [{f}] " + (", ".join(g0[f]["fails"]) or "every line passes") + f"; SPARC A {g0[f]['sparc']['A_c2b_refit']['rms']:.6f}, groups Z {g0[f]['groups']['Z']:+.4f}")
HO3CSV = {(r["footing"], r["name"]): r for r in csv.DictReader(open(os.path.join(REB, "HO3_dwarf_individuals_heldout", "ho3_dwarf_individuals_per_object.csv")))}
dg0 = dwarf_grade(r51_0, "K0", quiet=True)
k0b = all(abs(dg0[f]["per_field"][n]["E"] - float(HO3CSV[(f, n)]["E"])) < 1e-6 and abs(dg0[f]["per_field"][n]["Z"] - float(HO3CSV[(f, n)]["Z"])) < 1e-4 for f in FEET for n in FIELD)
HO3J = json.load(open(os.path.join(REB, "HO3_dwarf_individuals_heldout", "ho3_dwarf_individuals_results.json")))["footings"]
k0b = k0b and all(abs(dg0[f]["flags"][n]["Z"] - HO3J[f]["flags"][n]["Z"]) < 1e-6 for f in FEET for n in ("Leo T", "Phoenix")) and \
      all(dg0[f]["isolated"]["ok"] == HO3J[f]["subsamples"]["isolated"]["ok"] and abs(dg0[f]["isolated"]["maxabsZ"] - HO3J[f]["subsamples"]["isolated"]["maxabsZ"]) < 1e-6 for f in FEET)
P(f"  K0b HO3's 13 field residuals (E to 1e-6, Z to CSV precision; Leo T/Phoenix Z to 1e-6; S1-S3): {'PASS' if k0b else 'FAIL'}")
C0, _, _, _, _ = call(run_sigma)
HO2NS["TAB"].update(lg=np.array(C0["lg"]), lsc={t: np.array(v) for t, v in C0["lsc"].items()})
mw0, _, _, _, mwl0 = call(run_mw, 4.0)
HO2J = json.load(open(os.path.join(REB, "HO2_sluggs_milkyway_heldout", "ho2_heldout_results.json")))["mw"]
k0c = mw0["S0_GD2"]["ok"] and mw0["S0_GD1"]["ok"] and all(mw0["box"][k]["cls"] == HO2J["box"][k]["cls"] and mw0["box"][k]["counts"] == HO2J["box"][k]["counts"] for k in HO2J["box"]) and \
      all(abs(mw0["mcmillan"]["rows"][k][q] - HO2J["mcmillan"]["rows"][k][q]) < 1e-6 for k in HO2J["mcmillan"]["rows"] for q in ("K_R0", "z_Kz_BR", "vc_R0"))
mc0 = mw0["mcmillan"]["rows"]["canonical|A_c2b_refit"]
P(f"  K0c HO2 MW: box {mw0['box']['canonical|A_c2b_refit']['cls']} (canonical A), McMillan K_z {mc0['K_R0']:.1f} (z {mc0['z_Kz_BR']:+.1f}) -> {mc0['branch']}; "
  f"GD2/GD1 step 0 {mw0['S0_GD2']['ok']}/{mw0['S0_GD1']['ok']}: {'PASS' if k0c else 'FAIL'}   [{time.time() - T0:.0f} s]")
checks += [("K0a_CL2_grade", k0a), ("K0b_HO3_field", k0b), ("K0c_HO2_MW", k0c)]
RES["K0"] = dict(grade=g0, ho3_field={f: dg0[f]["per_field"] for f in FEET}, mw=dict(box={k: dict(cls=v["cls"], counts=v["counts"]) for k, v in mw0["box"].items()}, mcmillan=mc0))
def finish(code):
    RES["checks"] = {k: bool(v) for k, v in checks}; n = sum(bool(v) for _, v in checks)
    P(f"\nchecks {n}/{len(checks)}: " + ", ".join(f"{k} {'PASS' if v else 'FAIL'}" for k, v in checks) + f"; runtime {time.time() - T0:.0f} s; peak RSS {rss_all():.2f} GB (max over processes)")
    open(os.path.join(HERE, f"bs1_basin_switch{TAG}.out"), "w").write("\n".join(OUT) + "\n")
    json.dump(RES, open(os.path.join(HERE, f"bs1_basin_switch_results{TAG}.json"), "w"), indent=1, default=float, sort_keys=True)
    sys.exit(code)
if not (k0a and k0b and k0c) and not MUTATE:
    P("STOPPED AT STEP 0: the machinery does not reproduce CL2 / HO2 / HO3 with basins set to the systems alone."); RES["verdict"] = "STOPPED AT STEP 0"; finish(1)

# ================================================================== K1 helpers (independent recomputation of the flag)
def k1_sparc(flog, SPT, T):
    v = 0; n = 0; own_dev = 0.0
    for name, tag, f, flag, M200, a_ in flog:
        n += 1; own_dev = max(own_dev, abs(M200 / OWN[tag][name] - 1))
        Mb = SPT[tag].get(name) if SPT is not None else None
        exp = (Mb if Mb is not None else OWN[tag][name]) > 10 ** T[f]
        v += int(bool(exp) != bool(flag))
    return dict(n=n, viol=v, own_M200_maxdev=own_dev)
def k1_list(log, table):
    v = sum(int(bool(table[f][n]) != bool(fl)) for n, f, fl in log); return dict(n=len(log), viol=v)
def k1_mw(log, LGflag):
    v = sum(int(bool(LGflag[f]) != bool(fl)) for f, lM, fl in log); return dict(n=len(log), viol=v)

# ================================================================== BS1 configurations
def make_cfg(R0, L=4.0, T=None, ups=UPS_K, summed=False, mode="primary", antlia_var=False):
    T = T or {f: TSW for f in FEET}
    lg = lg_basin(R0, ups, summed)
    spt, info = sparc_basins(R0, lg["lgM"], ups, mode if not summed else "summed")
    dw = dwarf_flags(R0, lg["lgM"], T, antlia_var)
    mwf = {f: bool(lg["lgM"] > T[f]) for f in FEET}
    return dict(L=L, T=T, lg=lg, spt=spt, info=info, dw=dw, mw=mwf)
def sparc_flagset(c):
    return {(t, f): tuple(sorted(n for n in SNAMES if ((c["spt"][t].get(n) or OWN[t][n]) > 10 ** c["T"][f]))) for t in TAGS for f in FEET}
def changed_list(c):
    rows = []
    for t in TAGS:
        for n in SNAMES:
            for f in FEET:
                Mb = c["spt"][t].get(n); own = OWN[t][n] > 10 ** c["T"][f]; new = (Mb if Mb is not None else OWN[t][n]) > 10 ** c["T"][f]
                if own != new: rows.append(dict(name=n, bg=t, footing=f, lgM200_own=math.log10(OWN[t][n]), lgM_basin=math.log10(Mb), **{k: v for k, v in c["info"][n].items() if k in ("kind", "pgc1", "Nm", "ungc", "dist")}))
    return rows

PRIM = make_cfg(R0D)
P(f"\n=== BS1 PRIMARY (canonical primary, alt reported): R0_data {R0D:.1f} kpc, LG log M_basin {PRIM['lg']['lgM']:.4f} -> {'ROUTE E' if PRIM['mw']['canonical'] else 'LAW'} (T 12.3)")
CH = changed_list(PRIM)
chA = sorted({(r["name"], round(r["lgM200_own"], 3), round(r["lgM_basin"], 3), r.get("kind"), r.get("Nm")) for r in CH if r["bg"] == "A_c2b_refit" and r["footing"] == "canonical"})
chB = sorted({r["name"] for r in CH if r["bg"] == "B_cfg886_bg" and r["footing"] == "canonical"})
P(f"  SPARC flags changed law -> route E (bg A): {len(chA)}; bg B: {len(chB)} (same set: {sorted(x[0] for x in chA) == chB})")
for x in chA: P(f"    {x[0]:12s} own lgM200 {x[1]:.3f} -> basin {x[2]:.3f} ({x[3]}{', Nm ' + str(x[4]) if x[4] else ''})")
nodist_list = sorted(n for n, v in PRIM["info"].items() if v["kind"] == "no Dist")
P(f"  multi-member KT2017 groups without Dist (kept on the CL2 flag, A3): {len(nodist_list)} galaxies")
RES["primary_basins"] = dict(changed_A_canonical=[dict(name=x[0], lgM200_own=x[1], lgM_basin=x[2], kind=x[3], Nm=x[4]) for x in chA], changed_B=chB,
                             no_dist=nodist_list, info=PRIM["info"], lgM_basin_sparc={t: {n: math.log10(v) for n, v in PRIM["spt"][t].items()} for t in TAGS})

def run_config(c, lab, lens=None, mw=True, x43_cache=None):
    flab = "".join(ch if ch.isalnum() or ch in ".-" else "_" for ch in lab)
    CFG.update(T=c["T"], SP=c["spt"], DW=c["dw"], MW=c["mw"])
    key = (c["L"], tuple(sorted(c["T"].items())), tuple(sorted(sparc_flagset(c).items())))
    if x43_cache is not None and key in x43_cache: r43, k1s = x43_cache[key]; P(f"  ({lab}: SPARC flag set equals an earlier run; X43 result reused)")
    else:
        r43, st43, flog, _, _ = call(run_x43, c["L"], c["T"], flab)
        k1s = k1_sparc(flog, c["spt"], c["T"]); k1s["stat_viol"] = sum(v["viol"] for v in st43.values())
        if x43_cache is not None: x43_cache[key] = (r43, k1s)
    r51, st51, _, dlog, _ = call(run_x51, flab); r51["flags"] = c["dw"]
    k1d = k1_list(dlog, c["dw"]); k1d["stat_viol"] = sum(v["viol"] for v in st51.values())
    out = dict(r43=r43, r51=r51, k1=dict(sparc=k1s, dwarfs=k1d))
    if mw:
        mkey = (c["L"], tuple(sorted(c["mw"].items())))
        if mkey in MWC: m, k1m = MWC[mkey]; P(f"  ({lab}: LG flag and L equal an earlier run; MW result reused)")
        else:
            m, _, _, _, mwl = call(run_mw, c["L"]); k1m = k1_mw(mwl, c["mw"]); MWC[mkey] = (m, k1m)
        out["mw"] = m; out["k1"]["mw"] = k1m
    P(f"  [{lab}] runs done [{time.time() - T0:.0f} s]")
    return out
X43C = {}; MWC = {}
RP = run_config(PRIM, "primary", x43_cache=X43C)
P("\n--- (A) calibration lines, re-graded where flags change")
gA = grade(RP["r43"], F53on, F53off, RP["r51"]["RES"], "BS1 primary (S9, L 4, T 12.3; basin flags)")
P("\n--- (B) Milky Way (held out): branch from the LG basin")
def mw_summary(m, lab):
    o = {}
    for f in FEET:
        b = m["box"][f"{f}|A_c2b_refit"]; mc = m["mcmillan"]["rows"][f"{f}|A_c2b_refit"]
        o[f] = dict(cls=b["cls"], counts=b["counts"], branches=b["branches"], n_L1_L2a_L2b=b["counts"]["L1&L2a&L2b"], best=b["best"], passing=b["passing"],
                    mcmillan=dict(branch=mc["branch"], vc_R0=mc["vc_R0"], z_vc=mc["z_vc_Eilers"], K_R0=mc["K_R0"], z_Kz=mc["z_Kz_BR"], L1=mc["L1"], L2a=mc["L2a"], L2b=mc["L2b"], L3=mc["L3"]),
                    reported_B=dict(cls=m["box"][f"{f}|B_cfg886_bg"]["cls"], counts=m["box"][f"{f}|B_cfg886_bg"]["counts"]))
        P(f"  [{f}] {lab}: X5 box {b['cls']}; cells passing L1+L2a+L2b: {b['counts']['L1&L2a&L2b']}, all four: {b['counts']['all']}; branches {b['branches']}; "
          f"McMillan ({mc['branch']}) V_c {mc['vc_R0']:.1f} (z {mc['z_vc_Eilers']:+.1f}), K_z {mc['K_R0']:.1f} (z {mc['z_Kz_BR']:+.1f}), L1 {mc['L1']} L2a {mc['L2a']} L2b {mc['L2b']} L3 {mc['L3']}")
    return o
mwA = mw_summary(RP["mw"], "BS1 primary")
P("\n--- (C) LG field dwarfs one by one (held out): HO3's rules, branch from (a)")
dA = dwarf_grade(RP["r51"], "BS1 primary")
for f in FEET:
    P(f"  [{f}] Leo T {dA[f]['flags']['Leo T']['E']:+.3f} (Z {dA[f]['flags']['Leo T']['Z']:+.2f}, {dA[f]['flags']['Leo T']['flag']}); Phoenix {dA[f]['flags']['Phoenix']['E']:+.3f} "
      f"(Z {dA[f]['flags']['Phoenix']['Z']:+.2f}, {dA[f]['flags']['Phoenix']['flag']}); IC 1613 {dA[f]['flags']['IC 1613']['E']:+.3f} (Z {dA[f]['flags']['IC 1613']['Z']:+.2f}, {dA[f]['flags']['IC 1613']['flag']})")
sat_same = all(PRIM["dw"][f][n] == dwarf_flags_alone()[f][n] for f in FEET for n in DWARFS if DWARFS[n]["host"] in ("MW", "M31"))
P(f"  satellites' flag {'UNCHANGED (LG passes the switch): HO3 satellite grade carried' if sat_same else 'CHANGED (LG below the switch): satellites on the law, graded above'}")

def verdict(g, m, d):
    V = {}
    for f in FEET:
        A = not g[f]["fails"]; B = m[f]["n_L1_L2a_L2b"] > 0; C = all(d[f]["isolated"]["ok"].values())
        cf = [r for r, v in d[f]["isolated"]["ok"].items() if not v]
        if A and B and C: v = "BASIN SWITCH HOLDS"
        elif A and B: v = "BASIN SWITCH RESOLVES THE MW CONTRADICTION (field dwarfs fail " + ", ".join(cf) + "; |Z|>=2: " + "; ".join(f"{n} {z:+.2f}" for n, z in d[f]["beyond2"]) + ")"
        else:
            lines = list(g[f]["fails"]) + ([] if B else [f"Milky Way ({m[f]['cls']})"]) + ([] if C else ["field dwarfs (" + ", ".join(cf) + ")"])
            v = "BASIN SWITCH FAILS: " + ", ".join(lines)
        V[f] = dict(verdict=v, A_calibration_kept=A, B_mw_fixed=B, C_field_holds=C)
    return V
VA = verdict(gA, mwA, dA)
RES["primary"] = dict(grade=gA, mw=mwA, dwarfs=dA, satellites_flag_unchanged=sat_same, k1=RP["k1"], verdict=VA)

# ================================================================== reported variants
P("\n=== REPORTED VARIANTS (not graded; each with its own lines)")
VAR = {}
def variant(lab, c, lens=None, mw=True):
    r = run_config(c, lab, mw=mw, x43_cache=X43C)
    g = grade(r["r43"], lens[0] if lens else F53on, lens[1] if lens else F53off, r["r51"]["RES"], lab, quiet=True)
    d = dwarf_grade(r["r51"], lab, quiet=True)
    m = mw_summary(r["mw"], lab) if mw else None
    nch = len({x["name"] for x in changed_list(c) if x["bg"] == "A_c2b_refit" and x["footing"] == "canonical"})
    o = dict(lgM_LG=c["lg"]["lgM"], LG_routeE={f: c["mw"][f] for f in FEET}, n_sparc_changed_A=nch, k1=r["k1"],
             fails={f: g[f]["fails"] for f in FEET}, field={f: dict(ok=d[f]["isolated"]["ok"], beyond2=d[f]["beyond2"]) for f in FEET},
             field_branches={n: d["canonical"]["per_field"][n]["branch"] for n in FIELD})
    if mw: o["mw"] = {f: dict(cls=m[f]["cls"], n_L1_L2a_L2b=m[f]["n_L1_L2a_L2b"]) for f in FEET}; o["verdict"] = {f: v["verdict"] for f, v in verdict(g, m, d).items()}
    P(f"  {lab}: LG lgM {c['lg']['lgM']:.4f} (route E: {o['LG_routeE']}); SPARC flags changed (A, canonical) {nch}; canonical fails: {g['canonical']['fails'] or 'none'}; "
      f"alt fails: {g['alt']['fails'] or 'none'}; field canonical {d['canonical']['isolated']['verdict']}" + (f"; MW canonical {m['canonical']['cls']} ({m['canonical']['n_L1_L2a_L2b']} cells L1+L2a+L2b)" if mw else "")
      + (f"\n      verdict: canonical {o['verdict']['canonical']} | alt {o['verdict']['alt']}" if mw else ""))
    return o
# CL3 one-number variant (A7): lensing carried from CL3's committed JSON
CL3J = json.load(open(os.path.join(REB, "CL3_one_number", "cl3_one_number_results.json")))
T3 = {f: float(f"{CL3J['L3.75']['T'][f]:.4f}") for f in FEET}
def lens_from(gr):
    F = {f: {"all": {"H2H": {"chi2": gr[f]["lensing"]["ENV2H"]}, "L2H": {"chi2": gr[f]["lensing"]["L2H"]}},
             "primary": {"H2H": {"chi2": gr[f]["lensing"]["d_LF_L_primary"]}, "L2H": {"chi2": 0.0}}} for f in FEET}
    Fre = {f: {"all": {"H2H": {"chi2": gr[f]["lensing"]["H2H"]}}} for f in FEET}
    return F, Fre
VAR["CL3_L3.75"] = variant(f"CL3 one number (L 3.75, T {T3['canonical']} / {T3['alt']})", make_cfg(R0D, L=3.75, T=T3), lens=lens_from(CL3J["L3.75"]["grade"]))
VAR["UpsK_0.5"] = variant("Upsilon_K 0.5", make_cfg(R0D, ups=0.5))
VAR["UpsK_0.8"] = variant("Upsilon_K 0.8", make_cfg(R0D, ups=0.8))
VAR["summed_baryons"] = variant("summed-baryon M_basin", make_cfg(R0D, summed=True))
VAR["allKs_self"] = variant("literal all-Ks self term (A2 variant)", make_cfg(R0D, mode="allKs"))
VAR["dist_fallback"] = variant("groups without Dist take the SPARC distance", make_cfg(R0D, mode="distfb"))
VAR["R0_minus_1sigma"] = variant(f"R0_data - 1 sigma ({R0D - R0SIG:.0f} kpc)", make_cfg(R0D - R0SIG))
VAR["R0_plus_1sigma"] = variant(f"R0_data + 1 sigma ({R0D + R0SIG:.0f} kpc)", make_cfg(R0D + R0SIG))
VAR["AntliaB_at_NGC3109"] = variant("Antlia B at NGC 3109's position", make_cfg(R0D, antlia_var=True), mw=False)
RES["variants"] = VAR
memb = {lab: {n: (field_R(n) is not None and field_R(n) < R) for n in FIELD} for lab, R in (("R0-1s", R0D - R0SIG), ("R0", R0D), ("R0+1s", R0D + R0SIG))}
RES["LG"]["field_membership"] = memb
P("  field-dwarf LG membership (R < R0): " + "; ".join(f"{lab}: " + ", ".join(n for n, v in d.items() if v) for lab, d in memb.items()))

# ================================================================== verdict + checks
P("\n=== VERDICT (frozen; canonical primary, alt reported with its own)")
for f in FEET: P(f"  [{f}] {VA[f]['verdict']}   (A {VA[f]['A_calibration_kept']}, B {VA[f]['B_mw_fixed']}, C {VA[f]['C_field_holds']})")
RES["verdict"] = dict(canonical=VA["canonical"]["verdict"], alt=VA["alt"]["verdict"])
k1p = RP["k1"]; allk1 = [k1p] + [v["k1"] for v in VAR.values()]
viol = sum(k["sparc"]["viol"] + k["sparc"]["stat_viol"] + k["dwarfs"]["viol"] + k["dwarfs"]["stat_viol"] + k.get("mw", {}).get("viol", 0) for k in allk1)
nk1 = sum(k["sparc"]["n"] + k["dwarfs"]["n"] + k.get("mw", {}).get("n", 0) for k in allk1)
k1 = viol == 0 and nk1 > 0 and k1p["sparc"]["own_M200_maxdev"] < 1e-9
P(f"K1 every system's branch equals its basin flag (independent recomputation): {viol} violations in {nk1} decisions; own M200 max rel dev {k1p['sparc']['own_M200_maxdev']:.1e}: {'PASS' if k1 else 'FAIL'}")
checks.append(("K1_branch_equals_basin_flag", k1))
k2 = k2a and np.isfinite(R0SIG) and KTSTAT["n_matched"] > 0
P(f"K2 R0_data from CFG548's committed selection and seed {SEED}; KT2017 matches {KTSTAT['n_matched']} (Nm>=2: {KTSTAT['n_multi']}): {'PASS' if k2 else 'FAIL'}")
checks.append(("K2_reproducible_inputs", k2)); checks.append(("K3_rss", rss_all() < 1.0))
for fn in ("bs1_x43copy.py", "bs1_x53copy.py", "bs1_x51copy.py"):
    try: os.remove(os.path.join(HERE, fn))
    except OSError: pass
finish(0 if all(v for _, v in checks) else 1)
