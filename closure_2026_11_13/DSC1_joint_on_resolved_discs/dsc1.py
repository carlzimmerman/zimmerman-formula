#!/usr/bin/env python3
"""DSC1 (FROZEN_CRITERIA.md, 34edc4c9e7): the crossing-speed joint's distinctive statement on resolved outer rotation curves.
Discs above v*(z) should follow the reference layout (baryons + SRJ3's reference cold dark energy halo at the record's share);
discs below should follow the law. One free multiple A of the reference halo per group.
  nice -n 19 python3 dsc1.py                 -> dsc1.json / dsc1.out
  DSC1_TWIN=N (no cold component) / D (halo doubled) -> dsc1_MUTATE_TWN / _TWD .json / .out
Owners' code (SRJ2's srj2_rc.py, CFG401's cfg401_gas_shape.py, JNT2's jnt2_common.py) executed read-only from its own path.
Adopts nothing. kappa = 1/2 FITTED; not theory closed."""
import os, sys, io, csv, json, math, contextlib, warnings, importlib.util
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"): os.environ[_v] = "1"
warnings.filterwarnings("ignore")
sys.dont_write_bytecode = True
import numpy as np
from scipy.optimize import brentq
from scipy.special import i0, i1, k0, k1

HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
TWIN = os.environ.pop("DSC1_TWIN", "").strip().upper()
os.environ.pop("MUTATE", None)                        # CFG401's own MUTATE flag must stay off
OUT = []
def P(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); OUT.append(s)
def rel(p): return os.path.relpath(p, REPO)

# ---------------- owners' code, read-only ----------------
SJ = os.path.join(REPO, "closure_2026_11_12", "SRJ2_regime_split_joint"); SRC = os.path.join(SJ, "srj2_rc.py"); code = open(SRC).read()
NS = {"__file__": SRC, "__name__": "srj2_rc_lib"}
with contextlib.redirect_stdout(io.StringIO()):
    exec(compile(code[:code.index("json.dump(RES")], SRC, "exec"), NS)
FR, S, zstate, FOOTS = NS["FR"], NS["S"], NS["zstate"], NS["FOOTS"]
XTAB, FB, hh, Gs, MS, KPC, A0, glaw = (S[k] for k in ("XTAB", "FB", "hh", "G", "MS", "KPC", "A0", "glaw"))
MPC = 1e3 * KPC; m_nfw = FR["m_nfw"]
spec = importlib.util.spec_from_file_location("jnt2_common", os.path.join(REPO, "closure_2026_11_13", "JNT2_crossing_speed_joint", "jnt2_common.py"))
J = importlib.util.module_from_spec(spec); spec.loader.exec_module(J)
C401D = os.path.join(REPO, "campaign_fresh_gravity", "CFG401_genzel17_gas_shape")
src401 = open(os.path.join(C401D, "cfg401_gas_shape.py")).read()
pre401 = src401.split("LF = np.linspace(-3, 3, 601)")[0].replace("HERE = os.path.dirname(os.path.abspath(__file__))", "HERE = " + repr(C401D))
N401 = {"__name__": "cfg401_lib"}
with contextlib.redirect_stdout(io.StringIO()):
    exec(compile(pre401, os.path.join(C401D, "cfg401_gas_shape.py"), "exec"), N401)
T1, D401, gshape, C4, de401, E401 = N401["T1"], N401["data"], N401["gshape"], N401["C4"], N401["de"], N401["E"]

P("DSC1: the crossing-speed joint on resolved outer rotation curves (criteria 34edc4c9e7). TEST lane. Adopts nothing. kappa = 1/2 FITTED; not theory closed."
  + (f"  TWIN {TWIN}" if TWIN else ""))

# ---------------- reference halo (SRJ3's construction) ----------------
_H = {}
def halo(X, Mb_sun, z):
    key = (X, round(math.log10(Mb_sun), 8), round(z, 6))
    if key not in _H:
        conc, dta, omz = zstate(z); Mta = X * Mb_sun * hh / (1 - FB); hbz = FR["halo_basics_z"]
        lM = brentq(lambda l: hbz(10 ** l, conc, dta, omz)["Mta"] / Mta - 1, math.log10(Mta) - 2, math.log10(Mta) + 1, xtol=1e-12)
        hb = hbz(10 ** lM, conc, dta, omz); a = MPC / hh / (1 + z)
        _H[key] = (hb["rs"] * a, hb["rta"] * a, hb["rta"] / hb["rs"], hb)
    return _H[key]
def CR(Rm, Mb_sun, X, z):
    rs, rta, cta, _ = halo(X, Mb_sun, z); r = np.minimum(Rm, rta)
    return X * Mb_sun * MS * np.array([m_nfw(x) for x in np.atleast_1d(r / rs)]) / m_nfw(cta)
def Xof(ft, z): return XTAB[ft]["z0.0"] if z < 1 else XTAB[ft]["z1.0"]
CFAC = {"": 1.0, "N": 0.0, "D": 2.0}[TWIN]

# ---------------- baryon shapes ----------------
def freeman(R_kpc, Rd_kpc, M_sun):
    y = np.maximum(R_kpc / (2 * Rd_kpc), 1e-4)
    return 2 * M_sun * (Gs * MS / (Rd_kpc * KPC)) * y ** 2 * (i0(y) * k0(y) - i1(y) * k1(y)) / (R_kpc * KPC)
def hernq(R_kpc, a_kpc, M_sun): return Gs * MS * M_sun * R_kpc ** 2 / (R_kpc + a_kpc) ** 2 / (R_kpc * KPC) ** 2

# ---------------- Genzel six (CFG401's construction) ----------------
RC100 = {r["name"]: r for r in csv.DictReader(open(os.path.join(REPO, "data_assembly", "rc100_provenance", "rc100_table3_six_fields_paper_values.csv")))}
MB_ERR = {"COS4 01351": 0.5, "D3a 6397": 1.1, "GS4 43501": 0.37, "zC 406690": 0.7, "zC 400569": 1.2, "D3a 15504": 1.0}   # Table 1 prior 1 sigma (1e11)
MB_FIT = {"COS4 01351": 1.7, "D3a 6397": 2.3, "GS4 43501": 1.0, "zC 406690": 1.7, "zC 400569": 1.7, "D3a 15504": 2.1}    # Table 1 fit M_baryon (1e11)
PTS = list(csv.DictReader(open(os.path.join(REPO, "campaign_fresh_gravity", "CFG400_genzel17_selfcal", "cfg400_points.csv"))))
LEL = list(csv.DictReader(open(os.path.join(REPO, "data_assembly", "lelli2023_rotcur_digitised", "lelli2023_rotcur_digitised.csv"))))

def genzel_points(g, k, cut):
    z, kpa, inc, Rh, s0, bt, vc, ms, mb = T1[g]; R, V, eV = [], [], []
    for r in PTS:
        if r["galaxy"] != g or r["kind"] != "v": continue
        off = abs(float(r["offset_arcsec"]))
        if off < cut: continue
        R.append(off * kpa); V.append(abs(float(r["value"])) / math.sin(math.radians(inc))); eV.append(max(float(r["err"]), 1.0) / math.sin(math.radians(inc)))
    R, V, eV = map(np.array, (R, V, eV)); vc2 = V ** 2 + k * 3.36 * s0 ** 2 * (R / Rh)
    return R, vc2, np.sqrt((2 * V * eV / vc2 / math.log(10)) ** 2 + 0.05 ** 2)
def lelli_points(gal, k, kpa, Rhalf):
    R, V, e, s = [], [], [], []
    for r in LEL:
        if r["galaxy"] != gal: continue
        R.append(float(r["radius_arcsec"]) * kpa); V.append(float(r["vrot_kms"])); e.append(0.5 * (float(r["err_lo_kms"]) + float(r["err_hi_kms"])))
        s.append(37.0 if r["line"] == "Halpha" else 15.0)
    R, V, e, s = map(np.array, (R, V, e, s)); vc2 = V ** 2 + k * 3.36 * s ** 2 * (R / Rhalf)
    return R, vc2, np.sqrt((2 * V * e / vc2 / math.log(10)) ** 2 + 0.05 ** 2)

L488 = dict(z=1.46997, kpa=8.69, Ms=5.2e10, fbul=0.63, Rbul=0.35 * 8.69, Rdisc=0.88 * 8.69, L10=8.4e10 / 4.3)
def build(ft, var):
    """discs for one variant: list of dicts with R (kpc), y = log10 Vc^2 (SI), e, gb, gc (cold accel per unit A), mb, z, membership."""
    k = {"k0": 0.0, "k2": 2.0}.get(var, 1.0); cut = 0.3 if var == "BEAMHALF" else 0.6
    discs = []
    for g in T1:
        z, kpa, inc, Rh, s0, bt, vc, ms, mb = T1[g]
        Mb = mb * 1e11
        if var == "MBm": Mb = (mb - MB_ERR[g]) * 1e11
        if var == "MBp": Mb = (mb + MB_ERR[g]) * 1e11
        if var == "MBRC100": Mb = 10 ** float(RC100[g]["logMbar_Msun"])
        if var == "MBFIT": Mb = MB_FIT[g] * 1e11
        fgas = 1 - ms / mb if var not in ("MBm", "MBp", "MBRC100", "MBFIT") else max(0.0, 1 - ms * 1e11 / Mb)
        if var == "LELLI" and g == "zC 400569":
            R, vc2, e = lelli_points("zC-400569", k, 8.45, Rh); src = "Lelli+2023 (bracket)"
        else:
            R, vc2, e = genzel_points(g, k, cut); src = "Genzel+2017"
        gb = Mb * gshape(R, Rh, bt, fgas)
        discs.append(dict(name=g, src=src, z=z, Mb=Mb, Rhalf=Rh, R=R, vc2=vc2, e=e, gb=gb, vmeas=float(vc)))
    # zC-488879 (Lelli; CFG278 baryons)
    L = L488; alpha = 0.4 if var == "MBm" else 4.3; Ms = L["Ms"] * (2.0 if var == "MBp" else 1.0)
    R, vc2, e = lelli_points("zC-488879", k, L["kpa"], L["Rdisc"])
    Mg = alpha * L["L10"]; Mb = Ms + Mg
    gb = hernq(R, L["Rbul"] / 1.8153, Ms * L["fbul"]) + freeman(R, L["Rdisc"] / 1.678, Ms * (1 - L["fbul"])) + freeman(R, L["Rdisc"] / 1.678, Mg)
    near = np.abs(R - L["Rdisc"]) < 0.35 * L["Rdisc"]
    discs.append(dict(name="zC-488879", src="Lelli+2023", z=L["z"], Mb=Mb, Rhalf=L["Rdisc"], R=R, vc2=vc2, e=e, gb=gb,
                      vmeas=float(np.sqrt(np.mean(vc2[near]))) if near.any() else float("nan")))
    for d in discs:
        Rm = d["R"] * KPC; X = Xof(ft, d["z"])
        d["gc"] = CFAC * Gs * CR(Rm, d["Mb"], X, d["z"]) / Rm ** 2
        d["y"] = np.log10(d["vc2"] * 1e6); d["logR"] = np.log10(Rm)
        a0z = A0[ft] * (de401(d["z"]) if var == "A0DE" else 1.0)
        d["glaw"] = np.asarray(glaw(d["gb"], a0z), float)
        d["logMb"] = math.log10(d["Mb"]); d["vL"] = J.vL_kms(d["Mb"], d["z"]); d["vstar"] = J.vstar_kms(ft, d["z"])
        d["above"] = bool(d["vmeas"] > d["vstar"]) if var == "MEAS" else bool(d["logMb"] > J.logMstar(ft, d["z"]))
        d["Rmax_over_Rhalf"] = float(d["R"].max() / d["Rhalf"])
    return discs

# ---------------- statistics ----------------
AG = np.round(np.arange(0, 6.0 + 1e-9, 0.005), 3)
def model_y(d, kind, A=None):
    g = d["glaw"] if kind == "law" else d["gb"] + A * d["gc"]
    return np.log10(g) + d["logR"]
def halves(d):
    m = np.median(d["R"]); inn = d["R"] <= m; out = ~inn
    return inn, out
def S_of(d, y):
    inn, out = halves(d); return float(y[out].mean() - y[inn].mean())
def sigS(d):
    inn, out = halves(d); return math.sqrt(float((d["e"][out] ** 2).sum() / out.sum() ** 2 + (d["e"][inn] ** 2).sum() / inn.sum() ** 2))
def vratio(d, y):
    v2 = 10 ** y; o = np.argsort(d["R"])[-2:]; return float(math.sqrt(v2[o].mean() / v2.max()))
def chi_grid(ds):
    return np.array([sum(float((((d["y"] - model_y(d, "ref", A)) / d["e"]) ** 2).sum()) for d in ds) for A in AG])
def interval(ch, scale, lvl):
    ok = AG[ch - ch.min() <= lvl * scale]; return [float(ok.min()), float(ok.max())]
def shape_line(ds, kind, A, s2):
    w = np.array([1 / sigS(d) ** 2 for d in ds]); dif = np.array([S_of(d, d["y"]) - S_of(d, model_y(d, kind, A)) for d in ds])
    D = float((w * dif).sum() / w.sum()); sg = math.sqrt(1 / w.sum()) * math.sqrt(s2)
    return dict(D=D, sigma=sg, holds=bool(abs(D) <= 2 * sg))
def group(ds):
    if not ds: return dict(n=0)
    N = sum(len(d["R"]) for d in ds); ch = chi_grid(ds); i = int(np.argmin(ch)); Ab = float(AG[i])
    s2 = max(1.0, float(ch[i]) / max(N - 1, 1)); i95 = interval(ch, s2, 4.0); i68 = interval(ch, s2, 1.0)
    chl = sum(float((((d["y"] - model_y(d, "law")) / d["e"]) ** 2).sum()) for d in ds)
    c1 = float(ch[int(np.argmin(abs(AG - 1.0)))]); c0 = float(ch[0])
    power = bool(any(not (i95[0] <= a <= i95[1]) for a in (0.0, 1.0, 2.0)))
    sh = {"ref_A1": shape_line(ds, "ref", 1.0, s2), "ref_bestA": shape_line(ds, "ref", Ab, s2), "baryons_A0": shape_line(ds, "ref", 0.0, s2), "law": shape_line(ds, "law", None, s2)}
    perd = []
    for d in ds:
        chd = np.array([float((((d["y"] - model_y(d, "ref", A)) / d["e"]) ** 2).sum()) for A in AG])
        perd.append(dict(name=d["name"], bestA=float(AG[int(np.argmin(chd))]), S_data=S_of(d, d["y"]), S_ref1=S_of(d, model_y(d, "ref", 1.0)), S_bar=S_of(d, model_y(d, "ref", 0.0)),
                         S_law=S_of(d, model_y(d, "law")), sigS=sigS(d), Vratio_data=vratio(d, d["y"]), Vratio_ref1=vratio(d, model_y(d, "ref", 1.0)),
                         Vratio_bar=vratio(d, model_y(d, "ref", 0.0)), Vratio_law=vratio(d, model_y(d, "law")),
                         chi2_ref1=float((((d["y"] - model_y(d, "ref", 1.0)) / d["e"]) ** 2).sum()), chi2_bar=float((((d["y"] - model_y(d, "ref", 0.0)) / d["e"]) ** 2).sum()),
                         chi2_law=float((((d["y"] - model_y(d, "law")) / d["e"]) ** 2).sum()), npts=len(d["R"])))
    return dict(n=len(ds), names=[d["name"] for d in ds], N=N, chi2_A0=c0, chi2_A1=c1, chi2_law=chl, chi2_min=float(ch[i]), bestA=Ab, s2=s2, i95=i95, i68=i68,
                power=power, shape=sh, per_disc=perd)
def word_above(G_):
    if G_["n"] < 3: return "NO POWER (fewer than three discs above)"
    if not G_["power"]: return "NO POWER (interval excludes none of 0, 1, 2)"
    inside = G_["i95"][0] <= 1.0 <= G_["i95"][1]; sh = G_["shape"]
    if inside and sh["ref_A1"]["holds"]: return "JOINT'S STATEMENT HOLDS ON THE RESOLVED DISCS"
    if not inside: return "JOINT'S STATEMENT FAILS ON THE RESOLVED DISCS (A = 1 " + ("above" if G_["i95"][1] < 1.0 else "below") + " the interval)"
    lighter = [k for k in ("baryons_A0", "law") if sh[k]["holds"]] + (["best A"] if G_["bestA"] < 1.0 and sh["ref_bestA"]["holds"] else [])
    if lighter: return "JOINT'S STATEMENT FAILS ON THE RESOLVED DISCS (shape: reference fails, passes: " + ", ".join(lighter) + ")"
    return "NO VERDICT (shape fits nothing)"
def word_below(G_):
    if G_["n"] < 3: return "NO POWER (fewer than three discs below)"
    sh = G_["shape"]; sep = abs(G_["chi2_law"] - G_["chi2_A1"]) >= 4 * G_["s2"] or (sh["law"]["holds"] != sh["ref_A1"]["holds"])
    if not sep: return "NO POWER (law and reference not separated)"
    return "LAW HOLDS BELOW" if (sh["law"]["holds"] and G_["chi2_law"] - G_["chi2_min"] <= 4 * G_["s2"]) else "LAW FAILS BELOW"

VARS = ["main", "k0", "k2", "MBm", "MBp", "MEAS", "MBRC100", "MBFIT", "LELLI", "A0DE", "BEAMHALF"]
FRAG = ["k0", "k2", "MBm", "MBp", "MEAS"]
if TWIN: VARS, FRAG = ["main"], []
RES = dict(lane="DSC1", criteria="34edc4c9e7", twin=TWIN or None, note="Adopts nothing. kappa = 1/2 FITTED; not theory closed.", foot={})
for ft in FOOTS:
    R_ = RES["foot"][ft] = {}
    for var in VARS:
        ds = build(ft, var); ab = [d for d in ds if d["above"]]; be = [d for d in ds if not d["above"]]
        GA, GB = group(ab), group(be)
        R_[var] = dict(members=[dict(name=d["name"], src=d["src"], z=d["z"], logMb=d["logMb"], vL=d["vL"], vmeas=d["vmeas"], vstar=d["vstar"], logMstar=J.logMstar(ft, d["z"]),
                                      above=d["above"], npts=len(d["R"]), Rmax_kpc=float(d["R"].max()), Rmax_over_Rhalf=d["Rmax_over_Rhalf"]) for d in ds],
                       above=GA, below=GB, word_above=word_above(GA) if GA["n"] else "NO POWER (fewer than three discs above)",
                       word_below=word_below(GB) if GB["n"] else "NO POWER (fewer than three discs below)")
    m = R_["main"]
    R_["fragile_above"] = sorted(v for v in FRAG if R_[v]["word_above"].split(" (")[0] != m["word_above"].split(" (")[0])
    R_["fragile_below"] = sorted(v for v in FRAG if R_[v]["word_below"].split(" (")[0] != m["word_below"].split(" (")[0])

# ---------------- known answers (main run only) ----------------
KA = {}
if not TWIN:
    # KA-G: CFG402's method on CFG401's data, zC 406690 DE penalty
    LF = np.linspace(-4, 3, 701); SC = np.logspace(-3, 2, 251); dz = D401["zC 406690"]
    def chi402(a0):
        gb = gshape(dz["R"], dz["Rh"], dz["bt"], dz["fgas"]); best = 1e99
        for lf in LF:
            gn = gb * 10 ** lf * 1e11; best = min(best, float(np.sum(((np.log10(dz["gobs"]) - np.log10(C4.nu_mono(gn / a0) * gn)) / dz["elog"]) ** 2)))
        return best
    kag = {}
    for ft in FOOTS:
        cmin = min(chi402(A0[ft] * s) for s in SC); kag[ft] = chi402(A0[ft] * de401(dz["z"])) - cmin
    ds = build("canonical", "main"); mx = 0.0
    for d in ds[:6]:
        dd = D401[d["name"]]; gobs = d["vc2"] * 1e6 / (d["R"] * KPC)
        mx = max(mx, float(np.max(np.abs(gobs / dd["gobs"] - 1))), float(np.max(np.abs(d["e"] / dd["elog"] - 1))), float(np.max(np.abs(d["R"] / dd["R"] - 1))))
    KA["KA-G"] = dict(zC406690_DE_penalty=kag, target={"canonical": 5.94, "alt": 7.18}, data_maxrel=mx,
                      pass_=bool(abs(kag["canonical"] - 5.94) <= 0.01 and abs(kag["alt"] - 7.18) <= 0.01 and mx <= 1e-12))
    # KA-S: SRJ3 K5
    r = RC100["zC 400569"]; z = float(r["z"]); Mb = 10 ** float(r["logMbar_Msun"]); Re = float(r["Re_kpc"]) * KPC
    gmod = Gs * Mb / 2 * MS / Re ** 2 + Gs * float(CR(np.array([Re]), Mb, Xof("canonical", z), z)[0]) / Re ** 2
    KA["KA-S"] = dict(g_mod=gmod, target=4.4288e-10, pass_=bool(abs(gmod / 4.4288e-10 - 1) <= 1e-3))
    # KA-B
    KA["KA-B"] = dict(vstar0={f: J.vstar0_kms(f) for f in FOOTS}, logMstar_z2={f: J.logMstar(f, 2.0) for f in FOOTS},
                      pass_=bool(abs(J.vstar0_kms("canonical") - 668.5) < 0.1 and abs(J.vstar0_kms("alt") - 807.9) < 0.1 and abs(J.logMstar("canonical", 2.0) - 11.28) < 0.006 and abs(J.logMstar("alt", 2.0) - 11.53) < 0.006))
    # KA-SI: D3a 15504 outermost point, by hand in SI (separate constants and code path)
    d = [x for x in ds if x["name"] == "D3a 15504"][0]; z, kpa, inc, Rh, s0, bt, vc, ms, mb = T1["D3a 15504"]
    GSI, MSUN, KPCSI = 6.674e-11, 1.989e30, 3.0857e19; j = int(np.argmax(d["R"])); Rk = float(d["R"][j]); Rsi = Rk * KPCSI
    Mbs = mb * 1e11 * MSUN; fg = 1 - ms / mb; st = 1 - fg
    def fre(Rd, M):
        y = Rk / (2 * Rd); return 2 * GSI * M / (Rd * KPCSI) * y * y * (i0(y) * k0(y) - i1(y) * k1(y)) / Rsi
    a = 1 / 1.8153; gbh = fre(Rh / 1.678, Mbs * st * (1 - bt)) + GSI * Mbs * st * bt * (Rk / (Rk + a)) ** 2 / Rsi ** 2 + fre(2 * Rh / 1.678, Mbs * fg)
    rs_, rta_, cta_, hb = halo(Xof("canonical", z), mb * 1e11, z)
    H = 100e3 * hh / 3.0857e22 * math.sqrt(FR["Om"] * (1 + z) ** 3 + 1 - FR["Om"]); rhom = FR["Om"] * 3 * (100e3 * hh / 3.0857e22) ** 2 / (8 * math.pi * GSI) * (1 + z) ** 3
    rs_si = (3 * hb["M"] / hh * MSUN / (4 * math.pi * 200 * rhom)) ** (1 / 3) / hb["c"]; mn = lambda x: math.log(1 + x) - x / (1 + x)
    gch = GSI * Xof("canonical", z) * mb * 1e11 * MSUN * mn(Rsi / rs_si) / mn(cta_) / Rsi ** 2
    KA["KA-SI"] = dict(R_kpc=Rk, gbar_hand=gbh, gbar_script=float(d["gb"][j]), gcold_hand=gch, gcold_script=float(d["gc"][j]),
                       pass_=bool(abs(gbh / d["gb"][j] - 1) <= 0.01 and abs(gch / d["gc"][j] - 1) <= 0.01))
    RES["known_answers"] = KA
    # inventory: ineligible sets, discs above v*(z) on stars alone (lower bound on M_b)
    AT = os.path.join(REPO, "data_assembly", "arxiv_tables"); inv = {}
    zal = {r["id"]: float(r["z"]) for r in csv.DictReader(open(os.path.join(AT, "alpaka1_sample.csv")))}
    alp_ids = [r["id"] for r in csv.DictReader(open(os.path.join(AT, "alpaka1_digitised", "alpaka1_outer_summary.csv")))]
    alp = [(i, zal[i], math.log10(float(r["mstar_1e10msun"]) * 1e10)) for r in csv.DictReader(open(os.path.join(AT, "alpaka1_properties.csv"))) for i in [r["id"]] if i in alp_ids and r["mstar_1e10msun"] not in ("nan", "")]
    cid = [r["id"] for r in csv.DictReader(open(os.path.join(AT, "cristal2025_dynamics.csv")))]
    cri = [(r["id"], float(r["z_cii"]), float(r["logMstar"])) for r in csv.DictReader(open(os.path.join(AT, "cristal2025_sample.csv"))) if r["id"] in cid and r["logMstar"] not in ("nan", "")]
    noe = [(r["id"], float(r["z"]), math.log10(10 ** float(r["logMstar_SED"]) + 10 ** float(r["logMgas_CO_P1"]))) for r in csv.DictReader(open(os.path.join(REPO, "data_assembly", "noema3d", "noema3d_per_galaxy.csv")))]
    kur = [(r["kurvs_id"], float(r["z_halpha"]), float(r["logMstar"])) for r in csv.DictReader(open(os.path.join(AT, "kurvs2023_integrated.csv"))) if r["logMstar"] not in ("nan", "")]
    for nm, rows, what in (("ALPAKA I (curves on disk: %d)" % len(alp_ids), alp, "stars alone"), ("CRISTAL (curves: %d)" % len(cid), cri, "stars alone"),
                           ("NOEMA3D (10)", noe, "stars + CO gas"), ("KURVS (22)", kur, "stars alone")):
        inv[nm] = {ft: dict(n_with_mass=len(rows), above=[(i, z_, round(l, 2)) for i, z_, l in rows if l > J.logMstar(ft, z_)], basis=what) for ft in FOOTS}
    RES["inventory_membership"] = inv

# ---------------- print ----------------
def fm(G_):
    if not G_["n"]: return "n 0"
    sh = G_["shape"]
    return (f"n {G_['n']} ({', '.join(G_['names'])}), N {G_['N']}; chi2 A0 {G_['chi2_A0']:.1f} A1 {G_['chi2_A1']:.1f} law {G_['chi2_law']:.1f} min {G_['chi2_min']:.1f}; "
            f"best A {G_['bestA']:.3f} 68% [{G_['i68'][0]:.3f}, {G_['i68'][1]:.3f}] 95% [{G_['i95'][0]:.3f}, {G_['i95'][1]:.3f}] s2 {G_['s2']:.2f} power {G_['power']}; "
            f"shape D (data - model; 2 sigma): ref1 {sh['ref_A1']['D']:+.3f} bestA {sh['ref_bestA']['D']:+.3f} bar {sh['baryons_A0']['D']:+.3f} law {sh['law']['D']:+.3f} (sigma {sh['ref_A1']['sigma']:.3f}); "
            f"holds ref1 {sh['ref_A1']['holds']} bestA {sh['ref_bestA']['holds']} bar {sh['baryons_A0']['holds']} law {sh['law']['holds']}")
for ft in FOOTS:
    R_ = RES["foot"][ft]
    P(f"\n===== {ft}")
    for mm in R_["main"]["members"]:
        P(f"[{ft}]  {mm['name']:11s} {mm['src']:12s} z {mm['z']:.3f} logMb {mm['logMb']:.2f} (logM* {mm['logMstar']:.2f}) v_L {mm['vL']:.0f} v_meas {mm['vmeas']:.0f} v* {mm['vstar']:.0f} km/s "
          f"-> {'ABOVE' if mm['above'] else 'below'}; {mm['npts']} pts, R_max {mm['Rmax_kpc']:.1f} kpc = {mm['Rmax_over_Rhalf']:.2f} R_1/2")
    for var in VARS:
        v = R_[var]
        P(f"[{ft}] {var:8s} ABOVE: {fm(v['above'])}")
        P(f"[{ft}] {var:8s}   -> {v['word_above']}")
        P(f"[{ft}] {var:8s} BELOW: {fm(v['below'])}")
        P(f"[{ft}] {var:8s}   -> {v['word_below']}")
    for grp in ("above", "below"):
        G_ = R_["main"][grp]
        for pd in G_.get("per_disc", []):
            P(f"[{ft}]   main {grp} {pd['name']:11s} best A {pd['bestA']:.3f}; S data {pd['S_data']:+.3f} +- {pd['sigS']:.3f}, ref1 {pd['S_ref1']:+.3f}, bar {pd['S_bar']:+.3f}, law {pd['S_law']:+.3f}; "
              f"V_out/V_peak data {pd['Vratio_data']:.3f} ref1 {pd['Vratio_ref1']:.3f} bar {pd['Vratio_bar']:.3f} law {pd['Vratio_law']:.3f}; chi2 ref1 {pd['chi2_ref1']:.1f} bar {pd['chi2_bar']:.1f} law {pd['chi2_law']:.1f} ({pd['npts']} pts)")
    P(f"[{ft}] WORD ABOVE: {R_['main']['word_above']}" + (f"; FRAGILE ({', '.join(R_['fragile_above'])})" if R_["fragile_above"] else ""))
    P(f"[{ft}] WORD BELOW: {R_['main']['word_below']}" + (f"; FRAGILE ({', '.join(R_['fragile_below'])})" if R_["fragile_below"] else ""))
if KA:
    P("\nKnown answers: " + "; ".join(f"{k} {'PASS' if v['pass_'] else 'FAIL'}" for k, v in KA.items()))
    P(f"  KA-G zC 406690 DE penalty {KA['KA-G']['zC406690_DE_penalty']['canonical']:.3f} / {KA['KA-G']['zC406690_DE_penalty']['alt']:.3f} (CFG402 5.94 / 7.18); data max rel {KA['KA-G']['data_maxrel']:.1e}")
    P(f"  KA-S g_mod {KA['KA-S']['g_mod']:.4e} (SRJ3 4.4288e-10); KA-B v*(0) {KA['KA-B']['vstar0']}, logMstar(2) {KA['KA-B']['logMstar_z2']}")
    P(f"  KA-SI D3a 15504 at {KA['KA-SI']['R_kpc']:.2f} kpc: g_bar {KA['KA-SI']['gbar_hand']:.4e} vs {KA['KA-SI']['gbar_script']:.4e}; g_cold {KA['KA-SI']['gcold_hand']:.4e} vs {KA['KA-SI']['gcold_script']:.4e} m/s^2")
    for nm, v in RES["inventory_membership"].items():
        P(f"  inventory {nm}: " + "; ".join(f"{ft} {len(v[ft]['above'])} of {v[ft]['n_with_mass']} above on {v[ft]['basis']} {v[ft]['above']}" for ft in FOOTS))
    if not all(v["pass_"] for v in KA.values()):
        for ft in FOOTS: RES["foot"][ft]["main"]["word_above"] = "NO VERDICT (known answer failed)"
        P("A KNOWN ANSWER FAILED -> NO VERDICT")
P("\nDSC1 ABOVE: " + " / ".join(RES["foot"][f]["main"]["word_above"] for f in FOOTS) + " (canonical / alt)")
P("DSC1 BELOW: " + " / ".join(RES["foot"][f]["main"]["word_below"] for f in FOOTS) + " (canonical / alt)")
P("Adopts nothing. kappa = 1/2 FITTED; not theory closed.")
tag = f"_MUTATE_TW{TWIN}" if TWIN else ""
json.dump(RES, open(os.path.join(HERE, f"dsc1{tag}.json"), "w"), indent=1, default=float)
open(os.path.join(HERE, f"dsc1{tag}.out"), "w").write("\n".join(OUT) + "\n")
