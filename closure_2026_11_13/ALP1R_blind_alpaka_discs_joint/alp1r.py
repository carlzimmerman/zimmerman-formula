#!/usr/bin/env python3
"""ALP1R (READING.md, 8d3b72f35f): blind build of the crossing-speed joint on the 19 ALPAKA I ring curves.
Discs above v*(z) should follow the reference layout (baryons + SRJ3's reference cold dark energy halo at the record's share);
discs below should follow the law. SRJ2's srj2_rc.py prefix is executed read-only from its own path (as SRJ3) for FRZ1's halo.
  nice -n 19 python3 alp1r.py                 -> alp1r.json / alp1r.out
  ALP1R_TWIN=N (no cold component) | D (halo doubled) -> alp1r_MUTATE_TWN|TWD.json / .out
Adopts nothing. kappa = 1/2 FITTED; not theory closed."""
import os, sys, io, csv, json, math, contextlib, warnings
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"): os.environ[_v] = "1"
sys.dont_write_bytecode = True
warnings.filterwarnings("ignore")
import numpy as np
from scipy.optimize import brentq
from scipy.special import i0, i1, k0, k1, j1
from scipy.integrate import quad

HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
TWIN = os.environ.get("ALP1R_TWIN", "")
assert TWIN in ("", "N", "D")
OUT = []
def P(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); OUT.append(s)

# ---------------- owners' code, read-only (SRJ3's route) ----------------
SRC = os.path.join(REPO, "closure_2026_11_12", "SRJ2_regime_split_joint", "srj2_rc.py"); code = open(SRC).read()
NS = {"__file__": SRC, "__name__": "srj2_rc_lib"}
with contextlib.redirect_stdout(io.StringIO()):
    exec(compile(code[:code.index("json.dump(RES")], SRC, "exec"), NS)
FR, S, zstate = NS["FR"], NS["S"], NS["zstate"]
XTAB, FB, hh, G, MS, KPC, A0, glaw = (S[k] for k in ("XTAB", "FB", "hh", "G", "MS", "KPC", "A0", "glaw"))
MPC = 1e3 * KPC; m_nfw = FR["m_nfw"]; FOOTS = ("canonical", "alt")
P("ALP1R: crossing-speed joint on the ALPAKA I ring curves (READING 8d3b72f35f). TEST lane. Adopts nothing. kappa = 1/2 FITTED; not theory closed."
  + (f"  TWIN {TWIN}" if TWIN else ""))

# ---------------- boundary (own SI build) ----------------
GSI, MSUN, MPCSI = 6.67430e-11, 1.98892e30, 3.0857e22
XS, H0, OL = 5.41, 67.4e3 / 3.0857e22, 0.6847; OM = 1 - OL
def Ez(z): return math.sqrt(OM * (1 + z) ** 3 + OL)
def vstar(ft, z): return A0J[ft] / (10 * (1 + XS) * H0 * Ez(z)) / 1e3
A0J = {"canonical": 9.3603e-11, "alt": 1.1312e-10}
def vL(Mb, z): return (10 * GSI * (1 + XS) * Mb * MSUN * H0 * Ez(z)) ** (1 / 3) / 1e3

# ---------------- reference halo (SRJ3's construction) ----------------
_H = {}
def halo(X, Mb, z):
    key = (round(X, 10), round(math.log10(Mb), 9), round(z, 6))
    if key not in _H:
        conc, dta, omz = zstate(z); Mta = X * Mb * hh / (1 - FB); hbz = FR["halo_basics_z"]
        lM = brentq(lambda l: hbz(10 ** l, conc, dta, omz)["Mta"] / Mta - 1, math.log10(Mta) - 2, math.log10(Mta) + 1, xtol=1e-12)
        hb = hbz(10 ** lM, conc, dta, omz); a = MPC / hh / (1 + z)
        _H[key] = (hb["rs"] * a, hb["rta"] * a, hb["rta"] / hb["rs"], hb)
    return _H[key]
def CR(R_m, Mb, X, z):
    rs, rta, cta, _ = halo(X, Mb, z); r = np.minimum(R_m, rta)
    return X * Mb * MS * np.array([m_nfw(x) for x in np.atleast_1d(r / rs)]) / m_nfw(cta)
def Xof(ft, z): return XTAB[ft]["z0.0"] if z < 1 else XTAB[ft]["z1.0"]

# ---------------- baryon fields ----------------
def freeman(R_kpc, Rd_kpc, M):
    y = np.maximum(np.asarray(R_kpc) / (2 * Rd_kpc), 1e-5)
    return 2 * G * M * MS / (Rd_kpc * KPC) * y ** 2 * (i0(y) * k0(y) - i1(y) * k1(y)) / (np.asarray(R_kpc) * KPC)
def hernq(R_kpc, a_kpc, M): return G * M * MS / ((np.asarray(R_kpc) + a_kpc) * KPC) ** 2

# ---------------- data ----------------
AT = os.path.join(REPO, "data_assembly", "arxiv_tables")
def rd(p): return list(csv.DictReader(open(p)))
samp = {r["id"]: r for r in rd(os.path.join(AT, "alpaka1_sample.csv"))}
prop = {r["id"]: r for r in rd(os.path.join(AT, "alpaka1_properties.csv"))}
obs = {r["id"]: r for r in rd(os.path.join(AT, "alpaka1_alma_obs.csv"))}
kin = {r["id"]: r for r in rd(os.path.join(AT, "alpaka1_kinematics.csv"))}
outer = {r["id"]: r for r in rd(os.path.join(AT, "alpaka1_digitised", "alpaka1_outer_summary.csv"))}
georows = list(csv.reader(open(os.path.join(AT, "alpaka1_geometry.csv"))))[1:]
geo = {r[0]: r for r in georows}   # id, star, pa_hst, e1, e2, i_hst, e1, e2, pa_alma, e1, e2, i_alma, e1, e2, ...
rings = {}
for r in rd(os.path.join(AT, "alpaka1_digitised", "alpaka1_vrot_digitised.csv")):
    rings.setdefault(r["id"], {}).setdefault(r["panel"], {})[int(r["ring"])] = r
ADF = {r["quantity"]: r for r in rd(os.path.join(REPO, "data_assembly", "adf22_5_literature_2026-10-02", "adf22web3_2609.06679_A7_values.csv"))}
ADF2 = {r["quantity"]: r for r in rd(os.path.join(REPO, "data_assembly", "adf22_5_literature_2026-10-02", "adf22_pdf_direct_reads_A7.csv"))}
DUN = {r["gid"].replace("ALPAKA", ""): r for r in rd(os.path.join(REPO, "campaign_fresh_gravity", "CFG229_class_m_gold", "cfg229_inputs_static.csv")) if r["gid"].startswith("ALPAKA")}
IDS = sorted(outer, key=int)
assert len(IDS) == 19

RJ1 = {2: 0.77, 3: 0.54, 4: 0.42, 5: 0.32, 6: 0.21, 7: 0.18}
ACO_MS, ACO_SB, ACI10, CI21 = 4.36, 0.8, 17.0, 0.55

def line_of(i):
    l = obs[i]["line"]
    if l.startswith("CO("): return ("CO", int(l[3]))
    if l == "\\CIi": return ("CI", 1)
    if l == "\\CIii": return ("CI", 2)
    raise ValueError(l)

def gas_mass(i, route):
    typ = prop[i]["type_ms_or_other"]; sb = (typ == "SB")
    if route == "GAS-D" and i in DUN: return float(DUN[i]["logMgas_He"]) and 10 ** float(DUN[i]["logMgas_He"])
    if i == "24":
        L10 = 10 ** float(ADF["logLp_CO10"]["value"]); a = ACO_SB if route == "GAS-LO" else ACO_MS
        return a * L10
    kind, J = line_of(i); Lp = float(prop[i]["lprime_1e10_kkmspc2"]) * 1e10
    if route == "GAS-LO":
        fac = ACO_SB / ACO_MS
        return (ACO_SB * Lp) if kind == "CO" else (ACI10 * fac * Lp)
    hi = (route == "GAS-HI")
    if kind == "CO":
        a = ACO_MS if (hi or not sb) else ACO_SB
        return a * Lp / RJ1[J]
    fac = 1.0 if (hi or not sb) else ACO_SB / ACO_MS
    return ACI10 * fac * Lp / (CI21 if J == 2 else 1.0)

def mstar(i):
    if i == "24": return 10 ** float(ADF["logMstar"]["value"])
    return float(prop[i]["mstar_1e10msun"]) * 1e10

def Re_of(i):
    o = outer[i]
    if o["Re_kpc_dashed_line"]: return float(o["Re_kpc_dashed_line"]), "dashed optical R_e"
    if i == "24": return float(ADF2["umehata25_F444W_n1_Re"]["value"]), "F444W n=1 (ADF22 record)"
    return float(o["R_ext_kpc"]) / 1.2, "R_ext/1.2"

def incl(i):
    g = geo[i]; star = g[1].strip() == "*"
    ih, ia = float(g[5]), float(g[11]); eh, ea = 0.5 * (float(g[6]) + float(g[7])), 0.5 * (float(g[12]) + float(g[13]))
    if star or math.isnan(ih): return (ia, ea, "ALMA", None if math.isnan(ih) else ih)
    return (ih, eh, "HST", ia)

def disc_data(i):
    V = rings[i]["V"]; Sg = rings[i]["sigma"]; ks = sorted(V)
    R = np.array([float(V[k]["R_kpc"]) for k in ks]); v = np.array([float(V[k]["value_kms"]) for k in ks])
    eV = np.array([max(abs(float(V[k]["band_hi_kms"]) - float(V[k]["band_lo_kms"])) / 2, 1.0) for k in ks])
    sg = np.array([float(Sg[k]["value_kms"]) for k in ks])
    return R, v, eV, sg

BASE = {}
for i in IDS:
    R, v, eV, sg = disc_data(i); z = float(samp[i]["z"]); iu, ei, iw, ialt = incl(i); Re, Rrule = Re_of(i)
    BASE[i] = dict(id=i, name=samp[i]["name"], z=z, R=R, V=v, eV=eV, sig=sg, Re=Re, Re_rule=Rrule, i_used=iu, e_i=ei, i_which=iw, i_alt=ialt,
                   type=prop[i]["type_ms_or_other"], line=obs[i]["line"], Vext=float(kin[i]["vext_kms"]), beam=float(obs[i]["beam_major_arcsec"]),
                   Rarc=np.array([float(rings[i]["V"][k]["R_arcsec"]) for k in sorted(rings[i]["V"])]))

# ---------------- per-variant disc construction ----------------
FRAG = ("k0", "k2", "MB-", "MB+", "GAS-LO", "GAS-HI", "RE-", "RE+", "MEAS")
REPORTED = ("GAS-D", "IALT", "GAS2RD", "BULGE", "COSMIC", "Z2")
CFAC = {"": 1.0, "N": 0.0, "D": 2.0}[TWIN]

def build(ft, var):
    ds = []
    for i in IDS:
        b = BASE[i]; z = b["z"]
        k = {"k0": 0.0, "k2": 2.0}.get(var, 1.0)
        Ms = mstar(i) * {"MB-": 10 ** -0.2, "MB+": 10 ** 0.2}.get(var, 1.0)
        route = var if var in ("GAS-LO", "GAS-HI", "GAS-D") else "P"
        Mg = gas_mass(i, route)
        Re = b["Re"] * {"RE-": 1 / 1.5, "RE+": 1.5}.get(var, 1.0); Rd = Re / 1.678
        R = b["R"]; V = b["V"]; eV = b["eV"]
        Vc2 = V ** 2 + k * 3.36 * b["sig"] ** 2 * (R / Re)
        y = np.log10(Vc2); e = np.sqrt((2 * V * eV / (Vc2 * math.log(10))) ** 2 + 0.05 ** 2)
        if var == "IALT" and b["i_alt"] is not None:
            y = y + 2 * math.log10(math.sin(math.radians(b["i_used"])) / math.sin(math.radians(b["i_alt"])))
        Mb = Ms + Mg
        def gbar(mu, Ms=Ms, Mg=Mg, Rd=Rd, R=R):
            if var == "BULGE":
                return mu * (freeman(R, Rd, 0.7 * Ms) + hernq(R, 1.0 / 1.815, 0.3 * Ms) + freeman(R, Rd, Mg))
            return mu * (freeman(R, Rd, Ms) + freeman(R, (2 * Rd if var == "GAS2RD" else Rd), Mg))
        X = 5.41 if var == "COSMIC" else Xof(ft, z)
        def ghalo(mu, Mb=Mb, X=X, z=z, R=R):
            return CFAC * G * CR(R * KPC, mu * Mb, X, z) / (R * KPC) ** 2
        vs = vstar(ft, z); vl = vL(Mb, z)
        above = (b["Vext"] > vs) if var == "MEAS" else (vl > vs)
        sinc = max(2 * math.log10(math.e) * (1 / math.tan(math.radians(b["i_used"]))) * math.radians(b["e_i"]), 0.02)
        ds.append(dict(id=i, z=z, R=R, y=y, e=e, w=1 / e ** 2, Ms=Ms, Mg=Mg, Mb=Mb, Re=Re, gbar=gbar, ghalo=ghalo, vstar=vs, vL=vl,
                       above=bool(above), sinc=sinc, reach=float(R[-1] / Re), n=len(R)))
    if var == "Z2": ds = [d for d in ds if d["z"] >= 2]
    return ds

AG = np.round(np.arange(0, 6.0 + 1e-9, 0.005), 6); LMU = np.round(np.arange(-1.0, 0.5 + 1e-9, 0.02), 6)

def mod_y(gb, gh, A, R):   # (nA, nR) model log10(V^2 / (km/s)^2)
    g = gb[None, :] + np.asarray(A)[:, None] * gh[None, :]
    return np.log10(np.maximum(g, 1e-30) * (R * KPC)[None, :] / 1e6)

def prep(ft, d):
    """per disc: amplitude-test chi2(A) with the inclination prior; law chi2; shape-test chi2(A) minimised over mu; model S values."""
    a0 = A0[ft]; R = d["R"]; y = d["y"]; w = d["w"]; lam = 1 / d["sinc"] ** 2
    gb = d["gbar"](1.0); gh = d["ghalo"](1.0)
    def amp(m):   # m (nA, nR)
        r = y[None, :] - m; sw = w.sum(); swr = (w * r).sum(1)
        return (w * r * r).sum(1) - swr ** 2 / (sw + lam)
    mA = mod_y(gb, gh, AG, R); chiA = amp(mA)
    mL = np.log10(glaw(gb, a0) * R * KPC / 1e6)[None, :]; chiL = float(amp(mL)[0])
    res0 = float(np.median(y - mA[0]))
    SA = mA[:, -1] - mA[:, 0]; SL = float(mL[0, -1] - mL[0, 0])
    # shape test: free mu
    chiS_all = np.empty((len(LMU), len(AG))); SS_all = np.empty((len(LMU), len(AG))); chiLS = np.empty(len(LMU)); SLS = np.empty(len(LMU))
    for j, lm in enumerate(LMU):
        mu = 10 ** lm; m = mod_y(d["gbar"](mu), d["ghalo"](mu), AG, R)
        chiS_all[j] = (w[None, :] * (y[None, :] - m) ** 2).sum(1); SS_all[j] = m[:, -1] - m[:, 0]
        ml = np.log10(glaw(d["gbar"](mu), a0) * R * KPC / 1e6); chiLS[j] = (w * (y - ml) ** 2).sum(); SLS[j] = ml[-1] - ml[0]
    jb = chiS_all.argmin(0); chiS = chiS_all[jb, np.arange(len(AG))]; SS = SS_all[jb, np.arange(len(AG))]
    jl = int(chiLS.argmin())
    sd = float(y[-1] - y[0]); ssd = float(math.hypot(d["e"][-1], d["e"][0]))
    return dict(chiA=chiA, chiL=chiL, SA=SA, SL=SL, res0=res0, chiS=chiS, SS=SS, lmu_best=LMU[jb], chiLS=float(chiLS[jl]), SLS=float(SLS[jl]),
                lmu_law=float(LMU[jl]), Sd=sd, sS=ssd, mod_A1_minus_y=None)

def group(ft, ds, P_, test):
    """test 'amp' or 'shape'. Returns the group statistics."""
    if not ds: return dict(n=0)
    key, keyL, keyS, keySL = ("chiA", "chiL", "SA", "SL") if test == "amp" else ("chiS", "chiLS", "SS", "SLS")
    ch = sum(P_[d["id"]][key] for d in ds); chL = sum(P_[d["id"]][keyL] for d in ds)
    N = sum(d["n"] for d in ds); p = 1 if test == "amp" else 1 + len(ds)
    j = int(ch.argmin()); cmin = float(ch[j]); s2 = max(1.0, cmin / max(N - p, 1))
    in95 = AG[ch - cmin <= 4 * s2]; in68 = AG[ch - cmin <= s2]
    iv = lambda A: int(round(A / 0.005))
    def shape(Svec_fn):
        num = den = 0.0
        for d in ds:
            q = P_[d["id"]]; sm = Svec_fn(q); wt = 1 / q["sS"] ** 2; num += (q["Sd"] - sm) * wt; den += wt
        D = num / den; sD = math.sqrt(s2 / den); return dict(D=D, sD=sD, holds=bool(abs(D) <= 2 * sD))
    shA = lambda A: shape(lambda q: q[keyS][iv(A)])
    out = dict(n=len(ds), N=N, test=test, chi_min=cmin, s2=s2, bestA=float(AG[j]), i95=[float(in95.min()), float(in95.max())], i68=[float(in68.min()), float(in68.max())],
               chi0=float(ch[0]), chi1=float(ch[iv(1.0)]), chi2=float(ch[iv(2.0)]), chiL=float(chL),
               ex0=bool(ch[0] - cmin > 4 * s2), ex1=bool(ch[iv(1.0)] - cmin > 4 * s2), ex2=bool(ch[iv(2.0)] - cmin > 4 * s2),
               shape_A1=shA(1.0), shape_best=shA(float(AG[j])), shape_A0=shA(0.0), shape_law=shape(lambda q: q[keySL]),
               ids=[d["id"] for d in ds])
    out["power"] = bool(out["ex0"] or out["ex1"] or out["ex2"])
    out["law_within"] = bool(chL - cmin <= 4 * s2)
    return out

def word_above(g):
    if g["n"] < 3 or not g["power"]: return "NO POWER"
    a1_in = not g["ex1"]
    lighter = []
    if g["bestA"] < 1 and g["shape_best"]["holds"]: lighter.append("a lighter halo (best A %.3f)" % g["bestA"])
    if g["law_within"] and g["shape_law"]["holds"]: lighter.append("the law")
    if (not g["ex0"]) and g["shape_A0"]["holds"]: lighter.append("baryons alone")
    if a1_in and g["shape_A1"]["holds"]: return "JOINT'S STATEMENT HOLDS ON THE ALPAKA DISCS"
    if not a1_in:
        side = "A = 1 above the interval (too heavy)" if g["i95"][1] < 1 else "A = 1 below the interval (too light)"
        return "JOINT'S STATEMENT FAILS ON THE ALPAKA DISCS (%s; fits: %s)" % (side, ", ".join(lighter) if lighter else "none of a lighter halo, the law, baryons alone")
    passes = [x for x, ok in (("A = 0", g["shape_A0"]["holds"]), ("best A", g["bestA"] < 1 and g["shape_best"]["holds"]), ("the law", g["shape_law"]["holds"])) if ok]
    if passes: return "JOINT'S STATEMENT FAILS ON THE ALPAKA DISCS (A = 1 shape fails, %s passes it; fits: %s)" % (", ".join(passes), ", ".join(lighter) if lighter else "none")
    return "NO VERDICT (shape fits nothing)"
def short(w): return w.split(" (")[0] if not w.startswith("NO VERDICT") else w
def word_below(g):
    if g["n"] < 3: return "NO POWER"
    same = g["shape_law"]["holds"] == g["shape_A1"]["holds"]
    if abs(g["chiL"] - g["chi1"]) < 4 * g["s2"] and same: return "NO POWER"
    return "LAW HOLDS BELOW" if (g["shape_law"]["holds"] and g["law_within"]) else "LAW FAILS BELOW"

def floor(ds, P_):
    if not ds: return None
    return float(np.median([P_[d["id"]]["res0"] for d in ds]))

def run(ft, var):
    ds = build(ft, var); P_ = {d["id"]: prep(ft, d) for d in ds}
    res = dict(var=var, discs=[], groups={})
    for side, sel in (("ABOVE", True), ("BELOW", False)):
        gd = [d for d in ds if d["above"] == sel]
        fl = floor(gd, P_); at_floor = (fl is not None and fl < -0.15)
        ga, gs = group(ft, gd, P_, "amp"), group(ft, gd, P_, "shape")
        gate = "shape" if at_floor else "amp"; gg = gs if at_floor else ga
        wf = word_above if side == "ABOVE" else word_below
        res["groups"][side] = dict(n=len(gd), floor_median_res0=fl, at_floor=at_floor, gate=gate, amp=ga, shape=gs,
                                   word=(wf(gg) if gg.get("n", 0) else "NO POWER"), word_amp=(wf(ga) if ga.get("n", 0) else "NO POWER"),
                                   word_shape=(wf(gs) if gs.get("n", 0) else "NO POWER"))
    for d in ds:
        q = P_[d["id"]]
        res["discs"].append(dict(id=d["id"], name=BASE[d["id"]]["name"], z=d["z"], logMs=math.log10(d["Ms"]), logMg=math.log10(d["Mg"]), logMb=math.log10(d["Mb"]),
                                 Re=d["Re"], Re_rule=BASE[d["id"]]["Re_rule"], vL=d["vL"], vstar=d["vstar"], Vext=BASE[d["id"]]["Vext"], above=d["above"], n=d["n"],
                                 reach=d["reach"], sinc=d["sinc"], res0=q["res0"], chiA_best=float(AG[q["chiA"].argmin()]), chiS_best=float(AG[q["chiS"].argmin()]),
                                 lmu_at_A1=float(q["lmu_best"][200]), lmu_at_A0=float(q["lmu_best"][0]), lmu_law=q["lmu_law"], Sd=q["Sd"], S_A1=float(q["SA"][200]), S_A0=float(q["SA"][0]), S_law=q["SL"],
                                 chiA0=float(q["chiA"][0]), chiA1=float(q["chiA"][200]), chiL=q["chiL"], resA1=float(np.median(d["y"] - mod_y(d["gbar"](1.0), d["ghalo"](1.0), [1.0], d["R"])[0])),
                                 resLaw=float(np.median(d["y"] - np.log10(glaw(d["gbar"](1.0), A0[ft]) * d["R"] * KPC / 1e6)))))
    return res

# ---------------- known answers ----------------
KA = {}
v0 = {ft: A0J[ft] / (10 * (1 + XS) * H0) / 1e3 for ft in FOOTS}
KA["KA-B"] = dict(vstar0=v0, pass_=bool(abs(v0["canonical"] - 668.53) <= 0.01 and abs(v0["alt"] - 807.93) <= 0.01))
zk, lMk, Rek = 2.24, 10.95, 4.31; Mk = 10 ** lMk; Rk = Rek * KPC
gk = G * Mk / 2 * MS / Rk ** 2 + G * float(CR(np.array([Rk]), Mk, XTAB["canonical"]["z1.0"], zk)[0]) / Rk ** 2
KA["KA-S"] = dict(g_mod=gk, target=4.4288e-10, pass_=bool(abs(gk / 4.4288e-10 - 1) <= 1e-3))
# KA-SI: disc 20 outermost ring, canonical, by independent routes in SI
d20 = [d for d in build("canonical", "main") if d["id"] == "20"][0]; Rl = float(d20["R"][-1]); Rd20 = d20["Re"] / 1.678
def g_hankel(R_kpc, Rd_kpc, M):
    Rd = Rd_kpc * 3.0857e19; Rm = R_kpc * 3.0857e19; S0 = M * 1.989e30 / (2 * math.pi * Rd ** 2)
    f = lambda k: S0 * Rd ** 2 / (1 + (k * Rd) ** 2) ** 1.5 * j1(k * Rm) * k
    val = 0.0; kmax = 400 / Rd; edges = np.linspace(0, kmax, 801)
    for a_, b_ in zip(edges[:-1], edges[1:]): val += quad(f, a_, b_, limit=200)[0]
    return 2 * math.pi * 6.674e-11 * val
gb_si = g_hankel(Rl, Rd20, d20["Ms"]) + g_hankel(Rl, Rd20, d20["Mg"]); gb_sc = float(d20["gbar"](1.0)[-1])
rs_, rta_, cta_, hb = halo(Xof("canonical", d20["z"]), d20["Mb"], d20["z"])
rhom = FR["Om"] * 3 * (100e3 * hh / 3.0857e22) ** 2 / (8 * math.pi * 6.674e-11) * (1 + d20["z"]) ** 3
rs_si = (3 * hb["M"] / hh * 1.989e30 / (4 * math.pi * 200 * rhom)) ** (1 / 3) / hb["c"]
mn = lambda x: math.log(1 + x) - x / (1 + x)
gh_si = 6.674e-11 * Xof("canonical", d20["z"]) * d20["Mb"] * 1.989e30 * mn(Rl * 3.0857e19 / rs_si) / mn(cta_) / (Rl * 3.0857e19) ** 2
gh_sc = float(d20["ghalo"](1.0)[-1]) / CFAC if CFAC else float(G * CR(np.array([Rl * KPC]), d20["Mb"], Xof("canonical", d20["z"]), d20["z"])[0] / (Rl * KPC) ** 2)
KA["KA-SI"] = dict(disc="20", R_kpc=Rl, gbar_SI=gb_si, gbar_script=gb_sc, ghalo_SI=gh_si, ghalo_script=gh_sc, rs_SI_kpc=rs_si / 3.0857e19, rs_script_kpc=rs_ / KPC,
                   pass_=bool(abs(gb_si / gb_sc - 1) <= 0.01 and abs(gh_si / gh_sc - 1) <= 0.01))
kd = {i: abs(np.mean(BASE[i]["V"][-2:]) / BASE[i]["Vext"] - 1) for i in IDS}
KA["KA-D"] = dict(max_dev=max(kd.values()), worst=max(kd, key=kd.get), pass_=bool(max(kd.values()) <= 0.02))
KA_ALL = all(KA[k]["pass_"] for k in KA)
P(f"KA-B v*(0) {v0['canonical']:.2f} / {v0['alt']:.2f} km/s -> {'PASS' if KA['KA-B']['pass_'] else 'FAIL'}; KA-S g_mod {gk:.4e} (SRJ3 4.4288e-10) -> {'PASS' if KA['KA-S']['pass_'] else 'FAIL'}")
P(f"KA-SI disc 20 at R {Rl:.3f} kpc: g_bar SI(Hankel) {gb_si:.4e} vs script {gb_sc:.4e}; g_halo SI {gh_si:.4e} vs script {gh_sc:.4e}; r_s {rs_si/3.0857e19:.2f} vs {rs_/KPC:.2f} kpc -> {'PASS' if KA['KA-SI']['pass_'] else 'FAIL'}")
P(f"KA-D V_ext vs mean of last two rings: max dev {KA['KA-D']['max_dev']:.4f} (ID {KA['KA-D']['worst']}) -> {'PASS' if KA['KA-D']['pass_'] else 'FAIL'}")

# ---------------- runs ----------------
RES = dict(lane="ALP1R", reading="8d3b72f35f", twin=TWIN or None, KA=KA, note="Adopts nothing. kappa = 1/2 FITTED; not theory closed.", foot={})
VARS = ("main",) + FRAG + REPORTED
for ft in FOOTS:
    RF = RES["foot"][ft] = {}
    for var in VARS:
        RF[var] = run(ft, var)
    M = RF["main"]
    P(f"\n[{ft}] v*(z): " + ", ".join(f"z {z:.2f} {vstar(ft, z):.1f}" for z in (0.561, 1.456, 2.103, 2.504, 3.089, 3.63)) + " km/s")
    P(f"[{ft}] per disc (main): id z logM* logMgas logMb Re(rule) vL v* Vext side reach n sigma_inc | res0 resA1 resLaw (median ring y - model, dex) | best A amp / shape | log mu at A=1 / A=0 / law | S data, A1, A0, law")
    for r in M["discs"]:
        P(f"[{ft}]  {r['id']:>2} {r['z']:.3f} {r['logMs']:.2f} {r['logMg']:.2f} {r['logMb']:.2f} {r['Re']:.2f}({r['Re_rule'][:6]}) {r['vL']:.0f} {r['vstar']:.0f} {r['Vext']:.0f} "
          f"{'ABOVE' if r['above'] else 'below'} {r['reach']:.2f} {r['n']} {r['sinc']:.3f} | {r['res0']:+.3f} {r['resA1']:+.3f} {r['resLaw']:+.3f} | {r['chiA_best']:.3f} / {r['chiS_best']:.3f} | "
          f"{r['lmu_at_A1']:+.2f} / {r['lmu_at_A0']:+.2f} / {r['lmu_law']:+.2f} | {r['Sd']:+.3f} {r['S_A1']:+.3f} {r['S_A0']:+.3f} {r['S_law']:+.3f}")
    for var in VARS:
        for side in ("ABOVE", "BELOW"):
            g = RF[var]["groups"][side]
            if g["n"] == 0:
                P(f"[{ft}] {var:7s} {side}: n 0 -> NO POWER"); continue
            line = f"[{ft}] {var:7s} {side}: n {g['n']} floor res0 {g['floor_median_res0']:+.3f} ({'AT FLOOR, gate shape' if g['at_floor'] else 'gate amplitude'})"
            for t in ("amp", "shape"):
                q = g[t]
                line += (f" | {t}: N {q['N']} chi_min {q['chi_min']:.1f} s2 {q['s2']:.2f} bestA {q['bestA']:.3f} 95% [{q['i95'][0]:.3f}, {q['i95'][1]:.3f}] 68% [{q['i68'][0]:.3f}, {q['i68'][1]:.3f}]"
                         f" dchi(0,1,2) {q['chi0']-q['chi_min']:.1f}/{q['chi1']-q['chi_min']:.1f}/{q['chi2']-q['chi_min']:.1f} dchiLaw {q['chiL']-q['chi_min']:.1f} 4s2 {4*q['s2']:.1f}"
                         f" shapeD A1 {q['shape_A1']['D']:+.3f}+-{q['shape_A1']['sD']:.3f}{'h' if q['shape_A1']['holds'] else 'F'} A0 {q['shape_A0']['D']:+.3f}{'h' if q['shape_A0']['holds'] else 'F'}"
                         f" best {q['shape_best']['D']:+.3f}{'h' if q['shape_best']['holds'] else 'F'} law {q['shape_law']['D']:+.3f}{'h' if q['shape_law']['holds'] else 'F'}")
            P(line)
            P(f"[{ft}] {var:7s} {side}: WORD {g['word']}   (amp word: {short(g['word_amp'])}; shape word: {short(g['word_shape'])})")
    base_w = {s: short(M["groups"][s]["word"]) for s in ("ABOVE", "BELOW")}
    flips = [v for v in FRAG if any(short(RF[v]["groups"][s]["word"]) != base_w[s] for s in ("ABOVE", "BELOW"))]
    RF["fragile_by"] = flips
    lab = f"{M['groups']['ABOVE']['word']} / {M['groups']['BELOW']['word']}" + (" ; FRAGILE (" + ", ".join(flips) + ")" if flips else "")
    RF["label_before_twins"] = lab if KA_ALL else "NO VERDICT (known answer fails)"
    P(f"[{ft}] LABEL (before twins): {RF['label_before_twins']}")
    P(f"[{ft}] membership counts above/total: main {sum(r['above'] for r in M['discs'])}/19; " + "; ".join(f"{v} {sum(r['above'] for r in RF[v]['discs'])}/{len(RF[v]['discs'])}" for v in VARS if v != "main"))

nm = "alp1r" + (f"_MUTATE_TW{TWIN}" if TWIN else "")
json.dump(RES, open(os.path.join(HERE, nm + ".json"), "w"), indent=1, default=lambda o: o.tolist() if hasattr(o, "tolist") else str(o))
open(os.path.join(HERE, nm + ".out"), "w").write("\n".join(OUT) + "\nAdopts nothing. kappa = 1/2 FITTED; not theory closed.\n")
