#!/usr/bin/env python3
"""ALP1 (FROZEN_CRITERIA.md, b0e1ea1287): the crossing-speed joint's distinctive statement on the ALPAKA I ring curves.
Discs above v*(z) should follow the reference layout (baryons + SRJ3's reference cold dark energy halo at the record's share);
discs below should follow the law. One free multiple A of the reference halo per group; a shape-only test with a free
baryon scale per disc.
  nice -n 19 python3 alp1.py                  -> alp1.json / alp1.out
  ALP1_TWIN=N (no cold component) / D (halo doubled) -> alp1_MUTATE_TWN / _TWD .json / .out
Owners' code (SRJ2's srj2_rc.py, JNT2's jnt2_common.py, CFG401's prelude for KA-D) executed read-only from its own path.
Adopts nothing. kappa = 1/2 FITTED; not theory closed."""
import os, sys, io, csv, json, math, contextlib, warnings, importlib.util
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"): os.environ[_v] = "1"
warnings.filterwarnings("ignore")
sys.dont_write_bytecode = True
import numpy as np
from scipy.optimize import brentq
from scipy.special import i0, i1, k0, k1

HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
TWIN = os.environ.pop("ALP1_TWIN", "").strip().upper()
os.environ.pop("MUTATE", None)
OUT = []
def P(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); OUT.append(s)

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

P("ALP1: the crossing-speed joint on the ALPAKA I ring curves (criteria b0e1ea1287). TEST lane. Adopts nothing. kappa = 1/2 FITTED; not theory closed."
  + (f"  TWIN {TWIN}" if TWIN else ""))

# ---------------- reference halo (SRJ3's construction, as DSC1) ----------------
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

def freeman(R_kpc, Rd_kpc, M_sun):
    y = np.maximum(np.asarray(R_kpc, float) / (2 * Rd_kpc), 1e-4)
    return 2 * M_sun * (Gs * MS / (Rd_kpc * KPC)) * y ** 2 * (i0(y) * k0(y) - i1(y) * k1(y)) / (np.asarray(R_kpc, float) * KPC)

# ---------------- ALPAKA inputs (on disk) ----------------
AT = os.path.join(REPO, "data_assembly", "arxiv_tables")
def rows(p): return list(csv.DictReader(open(p)))
SAMP = {r["id"]: r for r in rows(os.path.join(AT, "alpaka1_sample.csv"))}
PROP = {r["id"]: r for r in rows(os.path.join(AT, "alpaka1_properties.csv"))}
OBS = {r["id"]: r for r in rows(os.path.join(AT, "alpaka1_alma_obs.csv"))}
KIN = {r["id"]: r for r in rows(os.path.join(AT, "alpaka1_kinematics.csv"))}
SUMM = {r["id"]: r for r in rows(os.path.join(AT, "alpaka1_digitised", "alpaka1_outer_summary.csv"))}
RINGS = rows(os.path.join(AT, "alpaka1_digitised", "alpaka1_vrot_digitised.csv"))
CM = {r["gid"].replace("ALPAKA", ""): r for r in rows(os.path.join(REPO, "campaign_fresh_gravity", "CFG229_class_m_gold", "cfg229_inputs_static.csv")) if r["gid"].startswith("ALPAKA")}
IDS = [i for i in SUMM]

# frozen conversions (criteria section 3; PROVISIONAL web-read values)
R_BOTH = {"CO(2-1)": 0.84, "CO(3-2)": 0.52, "CO(4-3)": 0.41, "CO(5-4)": 0.32, "CO(6-5)": 0.21, "CO(7-6)": 0.18}
R_CSG = {"CO(2-1)": 0.97, "CO(3-2)": 0.56}
A_CI, LCI_T = 17.0, 29.1
def rci(T):
    # optically thin LTE L'(2-1)/L'(1-0) of [CI]: (g2/g1) exp(-(E2-E1)/T) (A21/A10) (nu10/nu21)^3
    return (5 / 3) * math.exp(-(62.5 - 23.6) / T) * (2.68e-7 / 7.93e-8) * (492.16 / 809.34) ** 3
R_CI = round(rci(LCI_T), 2)

def gas_mass(i, var):
    line = OBS[i]["line"].strip(); Lp = float(PROP[i]["lprime_1e10_kkmspc2"]) * 1e10; typ = PROP[i]["type_ms_or_other"].strip()
    if i in CM and var != "CONVALL":
        m = 1.36 * 10 ** float(CM[i]["logMH2"])
        return m * (10 ** -0.3 if var == "GASm" else 10 ** 0.3 if var == "GASp" else 1.0), "class M (Dunne+22 x 1.36)"
    if "CI" in line:      # ID 13 [CI](2-1); ID 18 [CI](1-0) only under CONVALL
        if "CIii" in line:
            r = 1.0 if var == "GASm" else R_CI; m = A_CI * Lp / r * (2.0 if var == "GASp" else 1.0)
            return m, f"[CI](2-1): alpha_CI {A_CI} / R_CI {r}"
        m = A_CI * Lp * (10 ** -0.3 if var == "GASm" else 10 ** 0.3 if var == "GASp" else 1.0)
        return m, "[CI](1-0): alpha_CI 17"
    if var == "GASm": a, r = 0.8, 1.0
    elif var == "GASp": a, r = 4.36, R_CSG.get(line, R_BOTH[line])
    else: a, r = (0.8 if typ == "SB" else 4.36), R_BOTH[line]
    return a * Lp / r, f"{line}: alpha {a} / r_J1 {r}"

def build(ft, var):
    discs = []
    k = {"k0": 0.0, "k2": 2.0}.get(var, 1.0); fre = {"REx15": 1.5, "REd15": 1 / 1.5}.get(var, 1.0)
    for i in IDS:
        z = float(SAMP[i]["z"]); sm = PROP[i]["mstar_1e10msun"]
        Ms = float(sm) * 1e10 if sm not in ("nan", "") else float("nan")
        Ms *= 10 ** -0.3 if var == "MSm" else 10 ** 0.3 if var == "MSp" else 1.0
        Mg, groute = gas_mass(i, var)
        if var == "STARS" and Ms == Ms: Mg = 0.0
        Rext = float(SUMM[i]["R_ext_kpc"]); ReD = SUMM[i]["Re_kpc_dashed_line"]
        Re = (float(ReD) if ReD not in ("", "nan") else Rext / 1.2) * fre; Reg = Rext / 1.2 * fre
        rr = sorted([r for r in RINGS if r["id"] == i and r["panel"] == "V"], key=lambda r: float(r["R_kpc"]))
        R = np.array([float(r["R_kpc"]) for r in rr]); V = np.array([float(r["value_kms"]) for r in rr])
        eV = np.array([max(5.0, 0.5 * (abs(float(r["band_hi_kms"]) - float(r["value_kms"])) + abs(float(r["value_kms"]) - float(r["band_lo_kms"])))) for r in rr])
        sig = float(KIN[i]["sigma_m_kms"]); pterm = 3.36 * sig ** 2 * (R / Re)
        vc2 = V ** 2 + k * pterm
        e = np.sqrt((2 * V * eV / vc2 / math.log(10)) ** 2 + 0.05 ** 2)
        Mb = (Ms if Ms == Ms else 0.0) + Mg
        vc1 = np.sqrt(V ** 2 + pterm * Re / ((float(ReD) if ReD not in ("", "nan") else Rext / 1.2))); Re0 = float(ReD) if ReD not in ("", "nan") else Rext / 1.2
        vmeas = float(np.interp(Re0, R, vc1))
        d = dict(name=f"ALPAKA {i}", id=i, z=z, Ms=Ms, Mg=Mg, Mb=Mb, groute=groute, Re=Re, Reg=Reg, Re_rule="dashed" if ReD not in ("", "nan") else "R_ext/1.2",
                 R=R, V=V, vc2=vc2, e=e, sig=sig, ptfrac_out=float(pterm[-1] / V[-1] ** 2), vmeas=vmeas, typ=PROP[i]["type_ms_or_other"].strip(), line=OBS[i]["line"].strip(),
                 graded=bool(Ms == Ms))
        d["Rmax_over_Re"] = float(R.max() / Re0)
        X = Xof(ft, z); d["X"] = X
        d["y"] = np.log10(vc2 * 1e6); d["logR"] = np.log10(R * KPC)
        d["logMb"] = math.log10(Mb); d["vL"] = J.vL_kms(Mb, z); d["vstar"] = J.vstar_kms(ft, z); d["logMstar"] = J.logMstar(ft, z)
        d["above"] = bool(vmeas > d["vstar"]) if var == "MEAS" else bool(d["logMb"] > d["logMstar"])
        def gbar_of(beta, _Ms=Ms, _Mg=Mg, _Re=Re, _Reg=Reg, _R=R):
            g = freeman(_R, _Reg / 1.678, beta * _Mg)
            if _Ms == _Ms: g = g + freeman(_R, _Re / 1.678, beta * _Ms)
            return g
        def gc_of(beta, _Mb=Mb, _R=R, _z=z, _X=X):
            Rm = _R * KPC; return CFAC * Gs * CR(Rm, beta * _Mb, _X, _z) / Rm ** 2
        d["gb"] = gbar_of(1.0); d["gc"] = gc_of(1.0); d["gbar_of"] = gbar_of; d["gc_of"] = gc_of
        d["glaw"] = np.asarray(glaw(d["gb"], A0[ft]), float)
        discs.append(d)
    return discs

# ---------------- statistics (DSC1's) ----------------
AG = np.round(np.arange(0, 6.0 + 1e-9, 0.005), 3)
def model_y(d, kind, A=None):
    g = d["glaw"] if kind == "law" else d["gb"] + A * d["gc"]
    return np.log10(g) + d["logR"]
def halves(d):
    m = np.median(d["R"]); inn = d["R"] <= m; return inn, ~inn
def S_of(d, y):
    inn, out = halves(d); return float(y[out].mean() - y[inn].mean())
def sigS(d):
    inn, out = halves(d); return math.sqrt(float((d["e"][out] ** 2).sum() / out.sum() ** 2 + (d["e"][inn] ** 2).sum() / inn.sum() ** 2))
def vratio(d, y):
    v2 = 10 ** y; o = np.argsort(d["R"])[-2:]; return float(math.sqrt(v2[o].mean() / v2.max()))
def chi_d(d, kind, A=None): return float((((d["y"] - model_y(d, kind, A)) / d["e"]) ** 2).sum())
def chi_grid(ds): return np.array([sum(chi_d(d, "ref", A) for d in ds) for A in AG])
def interval(grid, ch, scale, lvl):
    ok = grid[ch - ch.min() <= lvl * scale]; return [float(ok.min()), float(ok.max())]
def shape_line(ds, kind, A, s2):
    w = np.array([1 / sigS(d) ** 2 for d in ds]); dif = np.array([S_of(d, d["y"]) - S_of(d, model_y(d, kind, A)) for d in ds])
    D = float((w * dif).sum() / w.sum()); sg = math.sqrt(1 / w.sum()) * math.sqrt(s2)
    return dict(D=D, sigma=sg, holds=bool(abs(D) <= 2 * sg))
def meanres(ds, kind, A, s2):
    r = np.concatenate([d["y"] - model_y(d, kind, A) for d in ds]); w = np.concatenate([1 / d["e"] ** 2 for d in ds])
    return dict(mean=float((w * r).sum() / w.sum()), sigma=float(math.sqrt(s2 / w.sum())))

LB = np.round(np.arange(-1.0, 1.0 + 1e-9, 0.02), 3); AGS = np.round(np.arange(0, 6.0 + 1e-9, 0.05), 3)
def shape_only(ds):
    """free baryon scale beta per disc (halo recomputed with beta M_b), profile chi2 over beta, A grid AGS."""
    tot = np.zeros(len(AGS)); bb = []
    for d in ds:
        tab = np.zeros((len(LB), len(AGS)))
        for j, lb in enumerate(LB):
            b = 10 ** lb; gb = d["gbar_of"](b); gc = d["gc_of"](b)
            m = np.log10(gb[None, :] + AGS[:, None] * gc[None, :]) + d["logR"][None, :]
            tab[j] = (((d["y"][None, :] - m) / d["e"][None, :]) ** 2).sum(axis=1)
        tot += tab.min(axis=0); bb.append(float(LB[np.argmin(tab[:, int(np.argmin(abs(AGS - 1.0)))])]))
    N = sum(len(d["R"]) for d in ds); i = int(np.argmin(tot)); s2 = max(1.0, float(tot[i]) / max(N - 1, 1))
    i95 = interval(AGS, tot, s2, 4.0)
    return dict(bestA=float(AGS[i]), chi2_min=float(tot[i]), s2=s2, i95=i95, speaks=bool(any(not (i95[0] <= a <= i95[1]) for a in (0.0, 1.0, 2.0))),
                logbeta_at_A1=bb, chi2_A0=float(tot[0]), chi2_A1=float(tot[int(np.argmin(abs(AGS - 1.0)))]))

def group(ds, do_shape=True):
    if not ds: return dict(n=0)
    N = sum(len(d["R"]) for d in ds); ch = chi_grid(ds); i = int(np.argmin(ch)); Ab = float(AG[i])
    s2 = max(1.0, float(ch[i]) / max(N - 1, 1)); i95 = interval(AG, ch, s2, 4.0); i68 = interval(AG, ch, s2, 1.0)
    chl = sum(chi_d(d, "law") for d in ds); c1 = float(ch[int(np.argmin(abs(AG - 1.0)))]); c0 = float(ch[0])
    power = bool(any(not (i95[0] <= a <= i95[1]) for a in (0.0, 1.0, 2.0)))
    sh = {"ref_A1": shape_line(ds, "ref", 1.0, s2), "ref_bestA": shape_line(ds, "ref", Ab, s2), "baryons_A0": shape_line(ds, "ref", 0.0, s2), "law": shape_line(ds, "law", None, s2)}
    mr = {"A0": meanres(ds, "ref", 0.0, s2), "A1": meanres(ds, "ref", 1.0, s2), "law": meanres(ds, "law", None, s2)}
    perd = []
    for d in ds:
        chd = np.array([chi_d(d, "ref", A) for A in AG])
        perd.append(dict(name=d["name"], bestA=float(AG[int(np.argmin(chd))]), S_data=S_of(d, d["y"]), S_ref1=S_of(d, model_y(d, "ref", 1.0)), S_bar=S_of(d, model_y(d, "ref", 0.0)),
                         S_law=S_of(d, model_y(d, "law")), sigS=sigS(d), Vratio_data=vratio(d, d["y"]), Vratio_ref1=vratio(d, model_y(d, "ref", 1.0)), Vratio_law=vratio(d, model_y(d, "law")),
                         chi2_ref1=chi_d(d, "ref", 1.0), chi2_bar=chi_d(d, "ref", 0.0), chi2_law=chi_d(d, "law"), npts=len(d["R"]),
                         res_bar_out=float(d["y"][-1] - model_y(d, "ref", 0.0)[-1]), res_law_out=float(d["y"][-1] - model_y(d, "law")[-1])))
    G_ = dict(n=len(ds), names=[d["name"] for d in ds], N=N, chi2_A0=c0, chi2_A1=c1, chi2_law=chl, chi2_min=float(ch[i]), bestA=Ab, s2=s2, i95=i95, i68=i68,
              power=power, shape=sh, meanres=mr, per_disc=perd)
    if do_shape: G_["shape_only"] = shape_only(ds)
    return G_
def word_above(G_):
    if G_["n"] < 3: return "NO POWER (fewer than three discs above)"
    if not G_["power"]: return "NO POWER (interval excludes none of 0, 1, 2)"
    inside = G_["i95"][0] <= 1.0 <= G_["i95"][1]; sh = G_["shape"]
    fits = []
    if 0 < G_["bestA"] < 1 and sh["ref_bestA"]["holds"]: fits.append("a lighter halo")
    if G_["i95"][0] <= 0.0: fits.append("baryons alone")
    if G_["chi2_law"] - G_["chi2_min"] <= 4 * G_["s2"]: fits.append("the law")
    if G_["bestA"] == 0.0 and G_["meanres"]["A0"]["mean"] < -2 * G_["meanres"]["A0"]["sigma"]: fits = ["nothing: the baryon model exceeds the dynamics"]
    if inside and sh["ref_A1"]["holds"]: return "JOINT'S STATEMENT HOLDS ON THE ALPAKA DISCS"
    if not inside:
        return "JOINT'S STATEMENT FAILS ON THE ALPAKA DISCS (A = 1 " + ("above" if G_["i95"][1] < 1.0 else "below") + " the interval; fits instead: " + (", ".join(fits) or "none named") + ")"
    lighter = [k for k in ("baryons_A0", "law") if sh[k]["holds"]] + (["best A"] if G_["bestA"] < 1.0 and sh["ref_bestA"]["holds"] else [])
    if lighter: return "JOINT'S STATEMENT FAILS ON THE ALPAKA DISCS (shape: reference fails, passes: " + ", ".join(lighter) + ")"
    return "NO VERDICT (shape fits nothing)"
def word_below(G_):
    if G_["n"] < 3: return "NO POWER (fewer than three discs below)"
    sh = G_["shape"]; sep = abs(G_["chi2_law"] - G_["chi2_A1"]) >= 4 * G_["s2"] or (sh["law"]["holds"] != sh["ref_A1"]["holds"])
    if not sep: return "NO POWER (law and reference not separated)"
    return "LAW HOLDS BELOW" if (sh["law"]["holds"] and G_["chi2_law"] - G_["chi2_min"] <= 4 * G_["s2"]) else "LAW FAILS BELOW"
def head(w): return w.split(" (")[0]

VARS = ["main", "k0", "k2", "GASm", "GASp", "MSm", "MSp", "REx15", "REd15", "MEAS", "STARS", "CONVALL"]
FRAG = ["k0", "k2", "GASm", "GASp", "MSm", "MSp", "REx15", "REd15", "MEAS"]
if TWIN: VARS, FRAG = ["main"], []
RES = dict(lane="ALP1", criteria="b0e1ea1287", twin=TWIN or None, R_CI=R_CI, note="Adopts nothing. kappa = 1/2 FITTED; not theory closed.", foot={})
for ft in FOOTS:
    R_ = RES["foot"][ft] = {}
    for var in VARS:
        ds = build(ft, var); gr = [d for d in ds if d["graded"]]
        ab = [d for d in gr if d["above"]]; be = [d for d in gr if not d["above"]]
        dsh = var in ("main",) + tuple(FRAG)
        GA, GB = group(ab, dsh), group(be, dsh)
        R_[var] = dict(members=[dict(name=d["name"], z=d["z"], logMs=(math.log10(d["Ms"]) if d["Ms"] == d["Ms"] else None), logMg=math.log10(d["Mg"]) if d["Mg"] > 0 else None,
                                      groute=d["groute"], logMb=d["logMb"], vL=d["vL"], vmeas=d["vmeas"], vstar=d["vstar"], logMstar=d["logMstar"], above=d["above"], graded=d["graded"],
                                      npts=len(d["R"]), Rmax_kpc=float(d["R"].max()), Re=d["Re"], Re_rule=d["Re_rule"], Rmax_over_Re=d["Rmax_over_Re"], sigma_m=d["sig"],
                                      ptfrac_out=d["ptfrac_out"], typ=d["typ"], line=d["line"]) for d in ds],
                       above=GA, below=GB, word_above=word_above(GA) if GA["n"] else "NO POWER (fewer than three discs above)",
                       word_below=word_below(GB) if GB["n"] else "NO POWER (fewer than three discs below)")
    m = R_["main"]
    R_["fragile_above"] = sorted(v for v in FRAG if head(R_[v]["word_above"]) != head(m["word_above"]))
    R_["fragile_below"] = sorted(v for v in FRAG if head(R_[v]["word_below"]) != head(m["word_below"]))

# ---------------- known answers (main run only) ----------------
KA = {}
if not TWIN:
    KA["KA-B"] = dict(vstar0={f: J.vstar0_kms(f) for f in FOOTS}, logMstar_z2={f: J.logMstar(f, 2.0) for f in FOOTS},
                      pass_=bool(abs(J.vstar0_kms("canonical") - 668.53) < 0.01 and abs(J.vstar0_kms("alt") - 807.93) < 0.01 and abs(J.logMstar("canonical", 2.0) - 11.28) < 0.006 and abs(J.logMstar("alt", 2.0) - 11.53) < 0.006))
    # KA-D: DSC1's numbers with this lane's halo code
    C401D = os.path.join(REPO, "campaign_fresh_gravity", "CFG401_genzel17_gas_shape")
    src401 = open(os.path.join(C401D, "cfg401_gas_shape.py")).read()
    pre401 = src401.split("LF = np.linspace(-3, 3, 601)")[0].replace("HERE = os.path.dirname(os.path.abspath(__file__))", "HERE = " + repr(C401D))
    N401 = {"__name__": "cfg401_lib"}
    with contextlib.redirect_stdout(io.StringIO()):
        exec(compile(pre401, os.path.join(C401D, "cfg401_gas_shape.py"), "exec"), N401)
    z_, kpa, inc, Rh, s0, bt, vc, ms, mb = N401["T1"]["D3a 15504"]
    Rk = 12.94805715970247; gcd = float(Gs * CR(np.array([Rk * KPC]), mb * 1e11, Xof("canonical", z_), z_)[0] / (Rk * KPC) ** 2)
    rc = {r["name"]: r for r in rows(os.path.join(REPO, "data_assembly", "rc100_provenance", "rc100_table3_six_fields_paper_values.csv"))}["zC 400569"]
    zz = float(rc["z"]); Mb = 10 ** float(rc["logMbar_Msun"]); Rem = float(rc["Re_kpc"]) * KPC
    gmod = Gs * Mb / 2 * MS / Rem ** 2 + Gs * float(CR(np.array([Rem]), Mb, Xof("canonical", zz), zz)[0]) / Rem ** 2
    KA["KA-D"] = dict(gcold_D3a15504=gcd, target_gcold=1.1652012867480988e-10, gmod_zC400569=gmod, target_gmod=4.4290158363859417e-10,
                      pass_=bool(abs(gcd / 1.1652012867480988e-10 - 1) <= 1e-3 and abs(gmod / 4.4290158363859417e-10 - 1) <= 1e-3))
    # KA-SI: ALPAKA 18 outermost ring by hand in SI (separate constants and code path)
    ds = build("canonical", "main"); d = [x for x in ds if x["id"] == "18"][0]; j = int(np.argmax(d["R"]))
    GSI, MSUN, KPCSI = 6.674e-11, 1.989e30, 3.0857e19; Rk = float(d["R"][j]); Rsi = Rk * KPCSI
    def fre(Rd, M):
        y = Rk / (2 * Rd); return 2 * GSI * M * MSUN / (Rd * KPCSI) * y * y * (i0(y) * k0(y) - i1(y) * k1(y)) / Rsi
    gbh = fre(d["Re"] / 1.678, d["Ms"]) + fre(d["Reg"] / 1.678, d["Mg"])
    rs_, rta_, cta_, hb = halo(d["X"], d["Mb"], d["z"])
    rhom = FR["Om"] * 3 * (100e3 * hh / 3.0857e22) ** 2 / (8 * math.pi * GSI) * (1 + d["z"]) ** 3
    rs_si = (3 * hb["M"] / hh * MSUN / (4 * math.pi * 200 * rhom)) ** (1 / 3) / hb["c"]; mn = lambda x: math.log(1 + x) - x / (1 + x)
    gch = GSI * d["X"] * d["Mb"] * MSUN * mn(Rsi / rs_si) / mn(cta_) / Rsi ** 2
    vk = float(d["V"][j]); gobs_h = ((vk * 1e3) ** 2 + 3.36 * (d["sig"] * 1e3) ** 2 * Rk / (float(SUMM["18"]["Re_kpc_dashed_line"]))) / Rsi
    gobs_s = 10 ** d["y"][j] / (Rk * KPC)
    KA["KA-SI"] = dict(id="18", R_kpc=Rk, gbar_hand=gbh, gbar_script=float(d["gb"][j]), gcold_hand=gch, gcold_script=float(d["gc"][j]), gobs_hand=gobs_h, gobs_script=gobs_s,
                       pass_=bool(abs(gbh / d["gb"][j] - 1) <= 0.01 and abs(gch / d["gc"][j] - 1) <= 0.01 and abs(gobs_h / gobs_s - 1) <= 0.01))
    KA["KA-L"] = dict(R_CI=rci(LCI_T), pass_=bool(abs(rci(LCI_T) - 0.33) <= 0.01))
    RES["known_answers"] = KA

# ---------------- print ----------------
def fm(G_):
    if not G_["n"]: return "n 0"
    sh = G_["shape"]; mr = G_["meanres"]; so = G_.get("shape_only")
    s = (f"n {G_['n']} ({', '.join(x.replace('ALPAKA ', '') for x in G_['names'])}), N {G_['N']}; chi2 A0 {G_['chi2_A0']:.1f} A1 {G_['chi2_A1']:.1f} law {G_['chi2_law']:.1f} min {G_['chi2_min']:.1f}; "
         f"best A {G_['bestA']:.3f} 68% [{G_['i68'][0]:.3f}, {G_['i68'][1]:.3f}] 95% [{G_['i95'][0]:.3f}, {G_['i95'][1]:.3f}] s2 {G_['s2']:.2f} power {G_['power']}; "
         f"mean res A0 {mr['A0']['mean']:+.3f} A1 {mr['A1']['mean']:+.3f} law {mr['law']['mean']:+.3f} (+- {mr['A0']['sigma']:.3f}); "
         f"shape D: ref1 {sh['ref_A1']['D']:+.3f} bestA {sh['ref_bestA']['D']:+.3f} bar {sh['baryons_A0']['D']:+.3f} law {sh['law']['D']:+.3f} (sigma {sh['ref_A1']['sigma']:.3f}); "
         f"holds ref1 {sh['ref_A1']['holds']} bestA {sh['ref_bestA']['holds']} bar {sh['baryons_A0']['holds']} law {sh['law']['holds']}")
    if so: s += f"; SHAPE-ONLY best A {so['bestA']:.2f} 95% [{so['i95'][0]:.2f}, {so['i95'][1]:.2f}] s2 {so['s2']:.2f} speaks {so['speaks']} (log beta at A=1 {', '.join(f'{b:+.2f}' for b in so['logbeta_at_A1'])})"
    return s
for ft in FOOTS:
    R_ = RES["foot"][ft]
    P(f"\n===== {ft}")
    for mm in R_["main"]["members"]:
        P(f"[{ft}]  {mm['name']:9s} z {mm['z']:.3f} {mm['typ']:2s} {mm['line']:8s} logM* {mm['logMs'] if mm['logMs'] is None else round(mm['logMs'], 2)} logMg {mm['logMg']:.2f} ({mm['groute']}) "
          f"logMb {mm['logMb']:.2f} (logM*(z) {mm['logMstar']:.2f}) v_L {mm['vL']:.0f} v_meas {mm['vmeas']:.0f} v* {mm['vstar']:.0f} -> {'ABOVE' if mm['above'] else 'below'}{'' if mm['graded'] else ' (NOT GRADED: no M*)'}; "
          f"{mm['npts']} rings, R_max {mm['Rmax_kpc']:.2f} kpc = {mm['Rmax_over_Re']:.2f} R_e ({mm['Re_rule']}, R_e {mm['Re']:.2f}); sigma_m {mm['sigma_m']:.0f}, pressure/V^2 at R_max {mm['ptfrac_out']:.3f}")
    for var in VARS:
        v = R_[var]
        P(f"[{ft}] {var:8s} ABOVE: {fm(v['above'])}")
        P(f"[{ft}] {var:8s}   -> {v['word_above']}")
        P(f"[{ft}] {var:8s} BELOW: {fm(v['below'])}")
        P(f"[{ft}] {var:8s}   -> {v['word_below']}")
    for grp in ("above", "below"):
        for pd in R_["main"][grp].get("per_disc", []):
            P(f"[{ft}]   main {grp} {pd['name']:9s} best A {pd['bestA']:.3f}; S data {pd['S_data']:+.3f} +- {pd['sigS']:.3f}, ref1 {pd['S_ref1']:+.3f}, bar {pd['S_bar']:+.3f}, law {pd['S_law']:+.3f}; "
              f"outer res bar {pd['res_bar_out']:+.3f} law {pd['res_law_out']:+.3f}; chi2 ref1 {pd['chi2_ref1']:.1f} bar {pd['chi2_bar']:.1f} law {pd['chi2_law']:.1f} ({pd['npts']} pts)")
    P(f"[{ft}] WORD ABOVE: {R_['main']['word_above']}" + (f"; FRAGILE ({', '.join(R_['fragile_above'])})" if R_["fragile_above"] else ""))
    P(f"[{ft}] WORD BELOW: {R_['main']['word_below']}" + (f"; FRAGILE ({', '.join(R_['fragile_below'])})" if R_["fragile_below"] else ""))
if KA:
    P("\nKnown answers: " + "; ".join(f"{k} {'PASS' if v['pass_'] else 'FAIL'}" for k, v in KA.items()))
    P(f"  KA-B v*(0) {KA['KA-B']['vstar0']}, logMstar(2) {KA['KA-B']['logMstar_z2']}")
    P(f"  KA-D g_cold D3a 15504 {KA['KA-D']['gcold_D3a15504']:.5e} (DSC1 1.16520e-10); g_mod zC 400569 {KA['KA-D']['gmod_zC400569']:.5e} (DSC1 4.42902e-10)")
    k_ = KA["KA-SI"]; P(f"  KA-SI ALPAKA 18 at {k_['R_kpc']:.3f} kpc: g_bar {k_['gbar_hand']:.4e} vs {k_['gbar_script']:.4e}; g_cold {k_['gcold_hand']:.4e} vs {k_['gcold_script']:.4e}; g_obs {k_['gobs_hand']:.4e} vs {k_['gobs_script']:.4e} m/s^2")
    P(f"  KA-L R_CI {KA['KA-L']['R_CI']:.4f}")
    if not all(v["pass_"] for v in KA.values()):
        for ft in FOOTS: RES["foot"][ft]["main"]["word_above"] = "NO VERDICT (known answer failed)"
        P("A KNOWN ANSWER FAILED -> NO VERDICT")
P("\nALP1 ABOVE: " + " / ".join(RES["foot"][f]["main"]["word_above"] for f in FOOTS) + " (canonical / alt)")
P("ALP1 BELOW: " + " / ".join(RES["foot"][f]["main"]["word_below"] for f in FOOTS) + " (canonical / alt)")
P("Adopts nothing. kappa = 1/2 FITTED; not theory closed.")
tag = f"_MUTATE_TW{TWIN}" if TWIN else ""
json.dump(RES, open(os.path.join(HERE, f"alp1{tag}.json"), "w"), indent=1, default=float)
open(os.path.join(HERE, f"alp1{tag}.out"), "w").write("\n".join(OUT) + "\n")
