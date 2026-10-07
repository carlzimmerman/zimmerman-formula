#!/usr/bin/env python3
"""CFG449: gas-dominated a0 rung, grown via (SR) SPARC flow/UMa gas discs re-distanced with CF4 then LVG TRGB/Cepheid moduli
(the EDD CMDs/TRGB table is captcha-gated; LVG carries the Anand+2021 / EDD TRGB moduli as a real table) and (IO) Iorio+2017
LITTLE THINGS 3D circular velocities with gas from Sigma_HI (thin-disc integrator) and Freeman stellar discs (SED M*, Hunter R_d).
Criteria: FROZEN_CRITERIA.md (128daa833). Statistic = CFG397's (bounded min of weighted log-g residuals, nu_mono; galaxy bootstrap 500, seed 7).
Inputs: data/ (Iorio finalrot.zip, LVG tables), ../CFG442_a0_rung_expansion/data/ (Oh+2015, Hunter+2012, Sesame), ../_external_data/cfg442/cf4_table2.dat.
Run: python3 cfg449_rung.py [--mutate] [--posthoc-io]
"""
import os, sys, io, re, json, math, zipfile, contextlib
import numpy as np
from scipy.optimize import minimize_scalar
from scipy.special import ellipk, i0, i1, k0, k1
HERE = os.path.dirname(os.path.abspath(__file__)); LANES = os.path.dirname(HERE)
sys.path.insert(0, LANES)
MUT = "--mutate" in sys.argv; POST = "--posthoc-io" in sys.argv          # POST: disclosed post-hoc run of IO despite the K0b fail; never the verdict
TAG = ("_MUTATE" if MUT else "") + ("_POSTHOC_IO" if POST else "")
with contextlib.redirect_stdout(io.StringIO()):
    import CFG4_common as C
DAT = os.path.join(HERE, "data"); D442 = os.path.join(LANES, "CFG442_a0_rung_expansion", "data")
CF4F = os.path.join(LANES, "_external_data", "cfg442", "cf4_table2.dat")
OUT = []
def P(s=""): print(s); OUT.append(str(s))
def finish(code, res=None):
    if res is not None: json.dump(res, open(os.path.join(HERE, f"cfg449_rung{TAG}_results.json"), "w"), indent=1)
    open(os.path.join(HERE, f"cfg449_rung{TAG}.out"), "w").write("\n".join(OUT) + "\n"); sys.exit(code)
KPC = 3.0857e19; G = 4.30091e-6                       # kpc (km/s)^2 / Msun
FOOT = (("canonical", 9.3603e-11), ("alt", 1.1312e-10), ("PAPER43 gas-point", 8.3e-11))
# ---------------------------------------------------------------- CFG397 / CFG442 machinery (unchanged)
# IO stars are stored as Vdisk = V_star/sqrt(0.5): Upsilon 0.5 gives V_star^2, 0.7 gives 1.4 V_star^2 (= M* x 1.4).
def rec(name, sample, R, Vobs, eV, Vgas, Vdisk, Vbul, **kw):
    return dict(name=name, sample=sample, R=np.asarray(R, float), Vobs=np.asarray(Vobs, float), eV=np.asarray(eV, float),
                Vgas=np.asarray(Vgas, float) * (0 if MUT else 1), Vdisk=np.asarray(Vdisk, float), Vbul=np.asarray(Vbul, float), **kw)
def sel_points(g):
    vg2 = np.sign(g["Vgas"]) * g["Vgas"] ** 2
    vb2 = vg2 + 0.5 * g["Vdisk"] ** 2 + 0.7 * g["Vbul"] ** 2
    return (vg2 >= 0.7 * vb2) & (vb2 > 0) & (g["Vobs"] > 0)
def arrays(gs, U):
    out = []
    for g in gs:
        m = sel_points(g); R = g["R"][m] * KPC; vg = g["Vgas"][m]
        b = (np.sign(vg) * vg ** 2 + U * g["Vdisk"][m] ** 2 + 1.4 * U * g["Vbul"][m] ** 2) * 1e6 / R
        o = (g["Vobs"][m] * 1e3) ** 2 / R
        w = 1 / (np.clip(g["eV"][m], 1, None) / np.clip(g["Vobs"][m], 1, None)) ** 2
        ok = (b > 0) & (o > 0)
        out.append((b[ok], o[ok], w[ok]))
    return out
def fit(parts):
    gb = np.concatenate([p[0] for p in parts]); go = np.concatenate([p[1] for p in parts]); w = np.concatenate([p[2] for p in parts])
    lgo, lgb = np.log10(go), np.log10(gb)
    f = lambda la: np.sum(w * (lgo - lgb - np.log10(C.nu_mono(gb / 10 ** la))) ** 2)
    return minimize_scalar(f, bounds=(-10.8, -9.3), method="bounded", options={"xatol": 1e-5}).x
def fit_boot(gs):
    parts = arrays(gs, 0.5); la = fit(parts)
    rng = np.random.default_rng(7)
    bs = [fit([parts[i] for i in rng.integers(0, len(parts), len(parts))]) for _ in range(500)]
    return dict(n=len(gs), log_a0=float(la), sd=float(np.std(bs)), npts=int(sum(len(p[0]) for p in parts)), names=[g["name"] for g in gs])
def rescale(g, f):
    h = dict(g); h["R"] = g["R"] * f; s = math.sqrt(f)
    for k in ("Vgas", "Vdisk", "Vbul"): h[k] = g[k] * s
    return h
def show(lab, r):
    if r is None or r["n"] < 2: P(f"  {lab:34s} N gal {0 if r is None else r['n']}: too few to fit"); return
    P(f"  {lab:34s} N gal {r['n']:3d} pts {r['npts']:4d}: a0 = {10 ** r['log_a0']:.3e} (log {r['log_a0']:+.3f} +- {r['sd']:.3f})")
# ---------------------------------------------------------------- SPARC
SP = [rec(g["name"], "SPARC", g["R"], g["Vobs"], g["eV"], g["Vgas"], g["Vdisk"], g["Vbul"], meta=g["meta"])
      for g in C.load_sparc() if g["meta"] and g["meta"]["Q"] <= 2]
SPd = {g["name"]: g for g in SP}
use_sp = [g for g in SP if sel_points(g).sum() >= 3]
P(f"CFG449 gas-dominated rung{' [MUTATE: gas dropped]' if MUT else ''}: SPARC Q<=2 galaxies with >= 3 gas-dominated points: {len(use_sp)}")
S0 = [g for g in use_sp if g["meta"]["fD"] in (2, 3, 5)]
# ---------------------------------------------------------------- distance catalogues
CF4 = {}
for l in open(CF4F):
    def fl(a, b):
        s = l[a - 1:b].strip(); return float(s) if s else None
    CF4[int(l[0:7])] = dict(pgc=int(l[0:7]), DMtrgb=fl(103, 107), DMceph=fl(114, 119), ra=fl(138, 145), dec=fl(147, 154))
cf_pgc = np.array(list(CF4)); cf_ra = np.array([CF4[k]["ra"] for k in cf_pgc]); cf_de = np.array([CF4[k]["dec"] for k in cf_pgc])
def cf4_ladder(e):
    if e is None: return None
    if e["DMtrgb"] is not None: return e["DMtrgb"], "CF4 TRGB"
    if e["DMceph"] is not None: return e["DMceph"], "CF4 Cepheid"
    return None
def sep_arcmin(ra, de, ra0, de0): return np.hypot((ra - ra0) * math.cos(math.radians(de0)), de - de0) * 60
LVG_POS = {}
for l in open(os.path.join(DAT, "lvg_table1.dat"), encoding="latin-1"):
    if len(l) < 35 or not re.match(r"\d\d\d\d\d\d\.\d[+-]\d{6}", l[19:34]): continue
    ra = 15 * (int(l[19:21]) + int(l[21:23]) / 60 + float(l[23:27]) / 3600)
    de = (int(l[28:30]) + int(l[30:32]) / 60 + int(l[32:34]) / 3600) * (-1 if l[27] == "-" else 1)
    LVG_POS[l[0:18].strip()] = (ra, de)
LVG_DM = {}
for l in open(os.path.join(DAT, "lvg_table6.dat"), encoding="latin-1"):
    if len(l) < 36 or not re.match(r"\s*\d+\.\d\d", l[19:24]): continue
    e = l[25:29].strip()
    LVG_DM.setdefault(l[0:18].strip(), []).append(dict(DM=float(l[19:24]), e=float(e) if e else None, meth=l[30:34].strip(), ref=l[35:54].strip()))
lv_names = list(LVG_POS); lv_ra = np.array([LVG_POS[n][0] for n in lv_names]); lv_de = np.array([LVG_POS[n][1] for n in lv_names])
def lvg_ladder(ra, de):
    s = sep_arcmin(lv_ra, lv_de, ra, de); i = int(np.argmin(s))
    if s[i] > 1.0: return None, f"no LVG entry within 1' (nearest {lv_names[i]} {s[i]:.1f}')"
    nm = lv_names[i]; rows = LVG_DM.get(nm, [])
    for meth in ("TRGB", "Cep"):
        rr = [r for r in rows if r["meth"] == meth]
        if not rr: continue
        yr = lambda r: int(r["ref"][:4]) if r["ref"][:4].isdigit() else 0
        rr.sort(key=lambda r: (r["ref"] != "2021AJ....162...80A", "EDD" not in r["ref"], -yr(r)))
        return (rr[0]["DM"], f"LVG {meth} ({nm}, DM {rr[0]['DM']:.2f} +- {rr[0]['e']}, {rr[0]['ref']}, sep {s[i]:.2f}')", rr[0]["e"]), None
    return None, f"LVG {nm} (sep {s[i]:.2f}'): no TRGB/Cep row (methods {sorted(set(r['meth'] for r in rows))})"
D_of = lambda dm: 10 ** ((dm - 25) / 5)
# ---------------------------------------------------------------- SR (EDD route via CF4 -> LVG)
ses = json.load(open(os.path.join(D442, "sesame_sr.json")))
SR, sr_log = [], []
for g in use_sp:
    if g["meta"]["fD"] not in (1, 4): continue
    s = ses[g["name"]]; d = None; note = []
    sc = sep_arcmin(cf_ra, cf_de, s["ra"], s["dec"]); i = int(np.argmin(sc))
    if sc[i] <= 1.0:
        d = cf4_ladder(CF4[int(cf_pgc[i])]); note.append(f"CF4 PGC {int(cf_pgc[i])}: {'no TRGB/Cep' if d is None else d[1]}")
    else: note.append("no CF4 within 1'")
    if d is None:
        d, why = lvg_ladder(s["ra"], s["dec"]); note.append(d[1] if d is not None else why)
    if d is None: sr_log.append((g["name"], g["meta"]["D"], None, "; ".join(note))); continue
    Dn = D_of(d[0]); f = Dn / g["meta"]["D"]
    h = rescale(g, f); h.update(sample="SR", D_old=g["meta"]["D"], D_new=Dn, method=d[1], e_DM=d[2] if len(d) > 2 else None)
    SR.append(h); sr_log.append((g["name"], g["meta"]["D"], Dn, "; ".join(note)))
# ---------------------------------------------------------------- IO route (Iorio+2017)
def vc2_thin(Rt, St, Rev):
    """V^2 [km/s]^2 of a razor-thin disc with surface density St [Msun/kpc^2] tabulated at Rt [kpc], at radii Rev."""
    dR = np.median(np.diff(Rt)) if len(Rt) > 1 else Rt[0]; Rout = Rt[-1] + 0.5 * dR
    N = 4000; dr = Rout / N; r = (np.arange(N) + 0.5) * dr
    S = np.interp(r, Rt, St, left=St[0], right=St[-1]); S[r > Rout] = 0
    m = 2 * np.pi * r * S * dr
    def phi(x):
        a = r[None, :]; X = x[:, None]; k2 = 4 * a * X / (a + X) ** 2
        return -(2 * G / np.pi) * np.sum(m[None, :] * ellipk(np.clip(k2, 0, 1 - 1e-15)) / (a + X), axis=1)
    h = 6 * dr
    return Rev * (phi(Rev + h) - phi(Rev - h)) / (2 * h)
def v2_freeman(R, M, Rd):
    y = np.clip(R / (2 * Rd), 1e-8, None); S0_ = M / (2 * np.pi * Rd ** 2)
    return 4 * np.pi * G * S0_ * Rd * y ** 2 * (i0(y) * k0(y) - i1(y) * k1(y))
# K0b: integrator control
Rd_t = 1.0; Rt = np.arange(0.25, 10.0001, 0.25); St = 1e8 * np.exp(-Rt / Rd_t); Rev = np.linspace(0.5, 4, 15)
k0b = float(np.max(np.abs(vc2_thin(Rt, St, Rev) / v2_freeman(Rev, 2 * np.pi * 1e8 * Rd_t ** 2, Rd_t) - 1)))
k0b_ok = k0b <= 0.02
for dRd in (0.1, 0.025):                                       # post-hoc diagnosis of the K0b result (reported only, gates nothing)
    Rt2 = np.arange(dRd, 10.0001, dRd); e2 = np.abs(vc2_thin(Rt2, 1e8 * np.exp(-Rt2), Rev) / v2_freeman(Rev, 2 * np.pi * 1e8, 1.0) - 1)
    P(f"  K0b diagnosis (post-hoc): sampling Rd*{dRd}: max |dV2/V2| = {e2.max():.4f}; at Rd/4 sampling, max beyond 0.75 Rd = "
      f"{float(np.max(np.abs(vc2_thin(Rt, St, Rev[Rev >= 0.75]) / v2_freeman(Rev[Rev >= 0.75], 2 * np.pi * 1e8, 1.0) - 1))):.4f}")
P(f"K0b thin-disc integrator vs analytic Freeman (0.5-4 Rd): max |dV2/V2| = {k0b:.4f} -> {'PASS' if k0b_ok else 'FAIL'}")
key = lambda s: re.sub(r"[^a-z0-9]", "", s.lower())
OH2 = {key(l[0:8]): dict(MK=l[146:151].strip(), MSED=l[152:157].strip()) for l in open(os.path.join(D442, "oh15_table2.dat"))}
OH1 = {}
for l in open(os.path.join(D442, "oh15_table1.dat")):
    p = l[9:31].split()
    ra = 15 * (int(p[0]) + int(p[1]) / 60 + float(p[2]) / 3600); sg = -1 if p[3][0] == "-" else 1
    de = sg * (abs(int(p[3])) + int(p[4]) / 60 + float(p[5]) / 3600); OH1[key(l[0:8])] = (ra, de)
HUN = {}
for l in open(os.path.join(D442, "hunter12_table1.dat")):
    pg = l[20:25].strip(); rd = l[108:112].strip()
    HUN[key(l[4:13])] = dict(pgc=int(pg) if pg else None, D=float(l[86:90]), Rd=float(rd) if rd else None)
HUN["cvnidwa"]["pgc"] = 42275
ALIAS = {"cvidwa": "cvnidwa"}
SPARC_ALIAS = {"ddo50": "UGC04305", "ddo87": "UGC05918", "ddo126": "UGC07559", "ddo154": "DDO154", "ddo168": "DDO168",
               "ngc2366": "NGC2366", "wlm": "UGCA444"}
zf = zipfile.ZipFile(os.path.join(DAT, "iorio17_finalrot.zip"))
IOR = {}
for n in sorted(zf.namelist()):
    mm = re.match(r"finalrot/(\w+)_onlinetab\.txt$", n)
    if not mm or mm.group(1) == "ddo216b": continue
    txt = zf.read(n).decode("latin-1"); Dio = float(re.search(r"Distance:\s*([0-9.]+)", txt).group(1))
    a = np.array([[float(v) for v in l.split()] for l in txt.splitlines() if l.strip() and not l.startswith("#")])
    IOR[ALIAS.get(mm.group(1), mm.group(1))] = dict(D=Dio, R=a[:, 1], Vc=a[:, 6], eVc=a[:, 7], S=a[:, 10])
def io_record(k, D_new, method):
    t = IOR[k]; hu = HUN.get(k); oh = OH2.get(k)
    if hu is None or hu["Rd"] is None: return None, "no Hunter R_d"
    if oh is None or not oh["MSED"]: return None, "no Oh+2015 MstarSED"
    fg = D_new / t["D"]; fs = D_new / hu["D"]
    R = t["R"] * fg
    vg2 = vc2_thin(t["R"], 1.33 * t["S"] * 1e6, t["R"]) * fg
    Ms = float(oh["MSED"]) * 1e7 * fs ** 2; Rd = hu["Rd"] * fs
    vs2 = v2_freeman(R, Ms, Rd)
    g = rec(k, "IO", R, t["Vc"], t["eVc"], np.sign(vg2) * np.sqrt(np.abs(vg2)), np.sqrt(vs2 / 0.5), 0 * R,
            D_iorio=t["D"], D_hunter=hu["D"], D_new=D_new, method=method, Mstar_SED=Ms, Rd=Rd)
    return g, None
IO, io_log, C2rows = [], [], []
if POST: P("POST-HOC MODE: IO route run despite the K0b result (disclosed departure; nothing in this mode is the frozen verdict)")
if k0b_ok or POST:
    for k in IOR:
        if k in SPARC_ALIAS: continue
        hu = HUN.get(k); d = cf4_ladder(CF4.get(hu["pgc"])) if hu and hu["pgc"] else None
        if d is None and k in OH1:
            d, why = lvg_ladder(*OH1[k])
            if d is None: io_log.append((k, f"excluded: no CF4/LVG ladder distance ({why})")); continue
        if d is None: io_log.append((k, "excluded: no position/distance")); continue
        g, why = io_record(k, D_of(d[0]), d[1])
        if g is None: io_log.append((k, f"excluded: {why}")); continue
        ns = int(sel_points(g).sum())
        io_log.append((k, f"{d[1]} D {g['D_new']:.2f} (Iorio {g['D_iorio']}, Hunter {g['D_hunter']}); gas points {ns}"))
        if ns >= 3: IO.append(g)
    # C2: overlap control at the SPARC distance, single-galaxy fits
    for k, sn in SPARC_ALIAS.items():
        if k not in IOR: continue
        s = SPd.get(sn)
        if s is None: C2rows.append(dict(name=k, sparc=sn, status="SPARC galaxy not in Q<=2 list")); continue
        g, why = io_record(k, s["meta"]["D"], "SPARC distance")
        if g is None: C2rows.append(dict(name=k, sparc=sn, status=why)); continue
        ni, nsp = int(sel_points(g).sum()), int(sel_points(s).sum())
        row = dict(name=k, sparc=sn, n_io=ni, n_sparc=nsp)
        if ni >= 3 and nsp >= 3:
            li, ls = float(fit(arrays([g], 0.5))), float(fit(arrays([s], 0.5)))
            row.update(log_io=li, log_sparc=ls, d=li - ls, bound=any(abs(v - b) < 1e-3 for v in (li, ls) for b in (-10.8, -9.3)), g=g, s=s)
        else: row["status"] = "fewer than 3 gas points in a route"
        C2rows.append(row)
# ---------------------------------------------------------------- empty-selection check (MUTATE)
if len(use_sp) + len(IO) == 0:
    P("MUTATE: empty gas-dominated selection detected (SPARC and IO) -> exit 1"); finish(1)
# ---------------------------------------------------------------- report
P(""); P("SR (SPARC flow/UMa gas discs; CF4 then LVG TRGB/Cepheid):")
for nm, Do, Dn, note in sr_log:
    P(f"  {nm:10s} D_SPARC {Do:6.2f}  -> {'D_new %6.2f (ratio %.3f)' % (Dn, Dn / Do) if Dn else 'not added':28s} [{note}]")
P(""); P("IO (Iorio+2017 non-SPARC galaxies):")
for k, s in io_log: P(f"  {k:10s} {s}")
P(""); P("C2 overlap control (single-galaxy a0, SPARC distance; |d| <= 0.10 each):")
c2 = [r for r in C2rows if "d" in r]
for r in C2rows:
    if "d" in r: P(f"  {r['name']:8s} ({r['sparc']}) IO {r['log_io']:+.3f} SPARC {r['log_sparc']:+.3f} d {r['d']:+.3f} (pts {r['n_io']}/{r['n_sparc']}){' [fit bound]' if r['bound'] else ''}")
    else: P(f"  {r['name']:8s} ({r['sparc']}) {r.get('status')} (pts {r.get('n_io')}/{r.get('n_sparc')})")
c2_ok = len(c2) >= 2 and all(abs(r["d"]) <= 0.10 for r in c2)
c2_joint = None
if c2:
    c2_joint = float(fit(arrays([r["g"] for r in c2], 0.5)) - fit(arrays([r["s"] for r in c2], 0.5)))
    P(f"  joint-set d (IO - SPARC) = {c2_joint:+.3f} dex over {len(c2)} galaxies")
P(f"  C2 -> {'PASS' if c2_ok else 'FAIL'}{'' if c2_ok else ' (IO report-only)'}")
P(""); P("Fits:")
res = {}
def F(lab, gs):
    r = fit_boot(gs) if len(gs) >= 2 else dict(n=len(gs)); res[lab] = r; show(lab, r); return r
r0 = F("S0 (CFG397 anchor)", S0)
c0 = abs(r0["log_a0"] - (-9.953)) <= 0.002 and abs(r0["sd"] - 0.071) <= 0.002
P(f"  C0 reproduce CFG397 anchor (-9.953 +- 0.071): {'PASS' if c0 else 'FAIL'}")
F("SR only", SR); F("IO only", IO)
F("S0+SR", S0 + SR); F("S0+SR+IO (all routes)", S0 + SR + IO)
SRq = [g for g in SR if g["e_DM"] is None or g["e_DM"] <= 0.5]
F("POST-HOC (reported only): S0+SR with e_DM <= 0.5 mag", S0 + SRq)
vlab = "S0+SR+IO (all routes)" if c2_ok else "S0+SR"
V = S0 + SR + (IO if c2_ok else []); rv = res[vlab]
k1 = {U: float(fit(arrays(V, U))) for U in (0.3, 0.5, 0.7)}; dk = k1[0.7] - k1[0.5]; k1ok = abs(dk) <= 0.05
P(f"K1 Upsilon check on {vlab}: log a0 at 0.3/0.5/0.7 = {k1[0.3]:+.3f}/{k1[0.5]:+.3f}/{k1[0.7]:+.3f}; 0.5->0.7 shift {dk:+.3f} -> {'PASS' if k1ok else 'FAIL'}")
est = rv["sd"] <= 0.05 and k1ok
P(""); P(("[POST-HOC, NOT THE VERDICT] " if POST else "") + f"RUNG {'ESTABLISHED' if est else 'NOT ESTABLISHED'} (verdict sample {vlab}: N {rv['n']}, sd {rv['sd']:.3f} {'<=' if rv['sd'] <= 0.05 else '>'} 0.05; K1 {'pass' if k1ok else 'fail'})")
for foot, a0 in FOOT:
    d = rv["log_a0"] - math.log10(a0)
    P(f"  {vlab} vs {foot:18s} {a0:.4e}: {d:+.3f} dex ({d / rv['sd']:+.2f} sigma) -> {'consistent' if abs(d) < 2 * rv['sd'] else 'differs'}")
P(f"  shift from CFG397 anchor: {rv['log_a0'] - (-9.953):+.3f} dex")
strip = lambda r: {k: v for k, v in r.items() if k not in ("g", "s")}
finish(0, dict(posthoc_io=POST, K0b=k0b, C0=c0, C2=dict(passed=c2_ok, rows=[strip(r) for r in C2rows], joint=c2_joint), fits=res, K1=k1, K1_pass=k1ok,
               verdict_sample=vlab, established=est, sr_log=sr_log, io_log=io_log))
