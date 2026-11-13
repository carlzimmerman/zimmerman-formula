#!/usr/bin/env python3
"""JNT1R (READING.md, 543118d9b8): blind re-grade of JNT1 row S. Which layout do the full SPARC rotation curves of the
galaxies above v_stiff fit: FRZ1's reference cold dark energy halo at the record's share (A = 1), the law, both, neither;
and the best-fit multiple A of the reference halo with its interval. Own code; QX8's loader and its exact-field term T
(parts/*.npz) are read read-only; PD1's share medians are read from pd1.json; SRJ2's membership from srj2_rc.json.
  nice -n 19 python3 jnt1r.py            -> jnt1r.json / .out
  nice -n 19 python3 jnt1r.py MUT_C      -> jnt1r_MUTATE_C.json / .out   (halo concentration halved)
  nice -n 19 python3 jnt1r.py MUT_E      -> jnt1r_MUTATE_E.json / .out   (velocity errors shuffled between galaxies)
kappa = 1/2 FITTED; not theory closed. Adopts nothing."""
import os, sys, json, math, io, contextlib
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"): os.environ[_v] = "1"
sys.dont_write_bytecode = True
import warnings; warnings.filterwarnings("ignore")
import numpy as np
from scipy.optimize import brentq

HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
MODE = sys.argv[1] if len(sys.argv) > 1 else "MAIN"; assert MODE in ("MAIN", "MUT_C", "MUT_E")
QX8D = os.path.join(REPO, "closure_2026_11_06", "QX8_sparc_exact_field")
sys.path.insert(0, QX8D); _a = sys.argv; sys.argv = [_a[0]]
with contextlib.redirect_stdout(io.StringIO()):
    import qx8 as Q8
sys.argv = _a
OUT = []
def P(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); OUT.append(s)

# ---------------- constants (SI) and the record's cosmology (CFG556 / FRZ1)
G, MS, KPC = 6.6743e-11, 1.98892e30, 3.0857e19; MPC = 1e3 * KPC; G_KPC = 4.3009172706e-6     # kpc (km/s)^2 / Msun
G_MPC = G_KPC * 1e-3                                                                          # Mpc (km/s)^2 / Msun
A0 = {"canonical": 9.360324825027975e-11, "alt": 1.1312035414413022e-10}; FOOTS = ("canonical", "alt")
VST = {"canonical": 265.8, "alt": 288.1}
h = 0.6736; Om = (0.02237 + 0.1200) / h ** 2; FB = 0.02237 / (0.02237 + 0.1200); RHO_M = Om * 2.77536627e11   # Msun/h per (Mpc/h)^3
PDJ = json.load(open(os.path.join(REPO, "closure_2026_11_09", "PD1_phantom_is_dust", "pd1.json")))
XTAB = {f: {zk: float(np.median([r["share_over_Mb"] for r in PDJ[f]["share_tables"][zk]])) for zk in ("z0.0", "z1.0")} for f in FOOTS}
SRJ2 = json.load(open(os.path.join(REPO, "closure_2026_11_12", "SRJ2_regime_split_joint", "srj2_rc.json")))
MEMB = {f: SRJ2["foot"][f]["G3b"]["f1.00"]["reported_reference"]["cluster_names"] for f in FOOTS}
CFAC = 0.5 if MODE == "MUT_C" else 1.0

def mn(x): x = np.asarray(x, float); return np.log1p(x) - x / (1 + x)
def Omz(z): return Om * (1 + z) ** 3 / (Om * (1 + z) ** 3 + 1 - Om)
def dta_of(z): return 5.55 + (11.81 - 5.55) * (1 - Omz(z)) / (1 - Om)
def halo_M(M, z, cfac):
    """Own build of FRZ1's halo: M = M_200m (Msun/h), comoving Mpc/h radii."""
    c = cfac * 10.14 * (M / 2e12) ** -0.081 * (1 + z) ** -1.01; r2 = (3 * M / (4 * math.pi * 200 * RHO_M)) ** (1 / 3); mc = float(mn(c)); dta = dta_of(z)
    xta = brentq(lambda x: float(mn(c * x)) / mc / x ** 3 - dta / 200.0, 1.0, 80.0, xtol=1e-12)
    xc = brentq(lambda x: float(mn(c * x)) / mc / x ** 3 - 1.0 / Omz(z), 0.05, 1.0, xtol=1e-12)
    return dict(M=M, c=c, r200=r2, rs=r2 / c, rta=xta * r2, Mta=M * float(mn(c * xta)) / mc, r200c=xc * r2, M200c=M * float(mn(c * xc)) / mc)
_HC = {}
def halo(X, Mb_sun, z=0.0, cfac=None):
    cfac = CFAC if cfac is None else cfac; key = (round(X, 10), round(math.log10(Mb_sun), 10), round(z, 6), cfac)
    if key not in _HC:
        Mta = X * Mb_sun * h / (1 - FB)
        lM = brentq(lambda l: halo_M(10 ** l, z, cfac)["Mta"] / Mta - 1, math.log10(Mta) - 2, math.log10(Mta) + 1, xtol=1e-12)
        hb = halo_M(10 ** lM, z, cfac); a = 1 / (1 + z)
        _HC[key] = dict(hb, rs_m=hb["rs"] * a / h * MPC, rta_m=hb["rta"] * a / h * MPC, cta=hb["rta"] / hb["rs"])
    return _HC[key]
def CR(r, Mb_sun, X, z=0.0, cfac=None):
    """Cold dark energy mass (kg) inside physical radius r (m): X M_b m(r / r_s) / m(c_ta), r capped at r_ta."""
    if X <= 0: return np.zeros_like(np.asarray(r, float))
    H = halo(X, Mb_sun, z, cfac); rr = np.minimum(np.asarray(r, float), H["rta_m"])
    return X * Mb_sun * MS * mn(rr / H["rs_m"]) / float(mn(H["cta"]))
def glaw(g, a0): g = np.asarray(g, float); return 0.5 * g + np.sqrt(0.25 * g * g + a0 * np.maximum(g, 0.0))

# ---------------- data
GALS = Q8.load_sparc(); UPS = Q8.UPS; IU = {u: int(np.argmin(abs(UPS - u))) for u in (0.35, 0.50, 0.65)}
lU, lN = np.log(UPS), np.log(Q8.NODES)
def Tfine(ft, i):
    T = np.load(os.path.join(Q8.PARTS, ft, f"{i:03d}.npz"), allow_pickle=False)["T"]
    return np.array([np.interp(lU, lN, T[:, j]) for j in range(T.shape[1])])               # (npts, nups)
TF = {ft: [Tfine(ft, i) for i in range(len(GALS))] for ft in FOOTS}
BYNAME = {q["name"]: i for i, q in enumerate(GALS)}
def Mb_pd1(q):
    VB2 = np.sign(q["Vgas"]) * q["Vgas"] ** 2 + 0.5 * q["Vdisk"] ** 2 + 0.7 * q["Vbul"] ** 2
    return max(float(np.max(np.clip(VB2 * q["R"] / G_KPC, 0, None))), 1e3)
SIGC = 2 / math.log(10)                                                                       # 0.8686: dex of V^2 per fractional V error

def gal_data(i, sD=1.0, inc=0, eVsub=None):
    """Point arrays for galaxy i under a distance factor sD = D'/D and inclination shift inc (+1 / -1 x eInc)."""
    q = GALS[i]; m = q["meta"]; R = q["Rm"] * sD; GB = q["GB"]; GO = q["GO"] / sD
    Vobs = q["Vobs"].astype(float).copy(); eV = q["eV"].astype(float).copy()
    if eVsub is not None: eV = eVsub
    if inc:
        i0 = math.radians(m["Inc"]); i1 = math.radians(min(max(m["Inc"] + inc * m["eInc"], 1.0), 90.0)); sc = math.sin(i0) / math.sin(i1)
        Vobs = Vobs * sc; eV = eV * sc; GO = GO * sc ** 2
    s = SIGC * np.clip(eV, 1, None) / np.clip(Vobs, 1, None); W = 1 / s ** 2
    return dict(name=q["name"], R=R, GB=GB, GO=GO, OK=q["OK"], W=W, Mb=Mb_pd1(q) * sD ** 2, Rlast=float(R[-1]), Vflat=m["Vflat"], i=i)

def model_lg(d, ft, kind, A=1.0, withT=False):
    """log10 g_mod (npts, nups) for kind 'ref' (A x the record's halo) or 'law'."""
    X = XTAB[ft]["z0.0"]
    if kind == "ref": g = d["GB"] + (G * CR(d["R"], d["Mb"], A * X) / d["R"] ** 2)[:, None]
    else: g = glaw(d["GB"], A0[ft])
    lg = np.log10(np.maximum(g, 1e-300))
    return lg + TF[ft][d["i"]] if withT else lg

def gal_stats(d, lg, iu):
    """At U index iu: d_i, e_i, shape Delta_i, its error, and point sums."""
    OK = d["OK"][:, iu]; r = np.log10(d["GO"]) - lg[:, iu]; W = d["W"]
    w = np.where(OK, W, 0.0); sw = w.sum(); di = float((w * r).sum() / sw); ei = 1 / math.sqrt(sw)
    out_ = d["R"] >= d["Rlast"] / 2; wo, wi = w * out_, w * (~out_)
    if wo.sum() > 0 and wi.sum() > 0:
        Dl = float((wo * r).sum() / wo.sum() - (wi * r).sum() / wi.sum()); eD = math.sqrt(1 / wo.sum() + 1 / wi.sum())
    else: Dl, eD = None, None
    return dict(d=di, e=ei, D=Dl, eD=eD, chi2=float((w * r * r).sum()), npt=int(OK.sum()), swr=float((w * r).sum()), sw=float(sw))

def fit_U(d, lg):
    """Record's fit mode: per-galaxy U on the grid by minimum weighted rms; returns the U index."""
    OK = d["OK"]; r = np.where(OK, np.log10(d["GO"])[:, None] - lg, 0.0); w = np.where(OK, d["W"][:, None], 0.0)
    return int(np.argmin((w * r * r).sum(0) / np.maximum(w.sum(0), 1e-300)))

def cls(vals, errs):
    v = np.array(vals); n = len(v); med = float(np.median(v)); mad = float(np.median(abs(v - med)))
    se = max(1.2533 * 1.4826 * mad / math.sqrt(n), float(np.median(errs)) / math.sqrt(n))
    return dict(n=n, med=med, se=se, line=bool(abs(med) <= 0.10 and abs(med) <= 3 * se))

AGRID = np.round(np.arange(0.0, 5.0001, 0.01), 2)
def chi2_A(D, ft, ucase):
    """chi2 (in units of the quoted errors) summed over galaxies, on the A grid; also per galaxy."""
    per = np.zeros((len(D), len(AGRID)))
    for k, d in enumerate(D):
        for j, A in enumerate(AGRID):
            lg = model_lg(d, ft, "ref", A)
            iu = fit_U(d, lg) if ucase == "fit" else IU[ucase]
            per[k, j] = gal_stats(d, lg, iu)["chi2"]
    return per
def a_interval(per, D, jk=True):
    tot = per.sum(0); j0 = int(np.argmin(tot)); Ab = float(AGRID[j0]); npt = sum(int(d["OK"][:, IU[0.50]].sum()) for d in D)
    resc = tot[j0] / max(npt - 1, 1)
    def band(k): sel = AGRID[tot - tot[j0] <= k * resc]; return [float(sel.min()), float(sel.max())]
    o = dict(A_best=Ab, chi2_min=float(tot[j0]), npts=npt, rescale=float(resc), chi2_95=band(4.0), chi2_68=band(1.0), edge=bool(j0 in (0, len(AGRID) - 1)))
    if jk and len(D) >= 3:
        Aj = np.array([float(AGRID[int(np.argmin(np.delete(per, k, 0).sum(0)))]) for k in range(len(D))])
        se = math.sqrt((len(D) - 1) / len(D) * float(((Aj - Aj.mean()) ** 2).sum()))
        o.update(A_jk=Aj.tolist(), jk_se=se)
        o["int95"] = [min(o["chi2_95"][0], Ab - 2 * se), max(o["chi2_95"][1], Ab + 2 * se)]
        o["int68"] = [min(o["chi2_68"][0], Ab - se), max(o["chi2_68"][1], Ab + se)]
    else:
        o["int95"], o["int68"] = o["chi2_95"], o["chi2_68"]
    o["excl"] = {str(a): bool(not (o["int95"][0] <= a <= o["int95"][1])) for a in (0, 1, 2)}
    o["A1_inside"] = not o["excl"]["1"]
    o["per_gal_A"] = [float(AGRID[int(np.argmin(per[k]))]) for k in range(len(D))]
    return o

def grade(D, ft, ucase="0.5", withT_ref=False, jk=True, per=None):
    """Lines and word for a set of galaxies D on footing ft. ucase '0.35', '0.5', '0.65' (fixed) or 'fit'."""
    uc = float(ucase) if ucase != "fit" else "fit"
    rows = []; ref_sums = [0.0, 0.0, 0.0]; law_sums = [0.0, 0.0, 0.0]; refA0 = []
    for d in D:
        lr = model_lg(d, ft, "ref", 1.0, withT_ref); ll = model_lg(d, ft, "law", withT=True); ln_ = model_lg(d, ft, "law", withT=False); l0 = model_lg(d, ft, "ref", 0.0)
        iur = fit_U(d, lr) if uc == "fit" else IU[uc]; iul = fit_U(d, ll) if uc == "fit" else IU[uc]
        sr, sl, sn, s0 = gal_stats(d, lr, iur), gal_stats(d, ll, iul), gal_stats(d, ln_, fit_U(d, ln_) if uc == "fit" else IU[uc]), gal_stats(d, l0, fit_U(d, l0) if uc == "fit" else IU[uc])
        # L3 in the record's fit mode (always per-galaxy U)
        fr, fl = gal_stats(d, lr, fit_U(d, lr)), gal_stats(d, ll, fit_U(d, ll))
        for S_, f_ in ((ref_sums, fr), (law_sums, fl)):
            S_[0] += f_["chi2"]; S_[1] += f_["swr"]; S_[2] += f_["sw"]
        rows.append(dict(name=d["name"], Vflat=d["Vflat"], logMb=math.log10(d["Mb"]), Rlast_kpc=d["Rlast"] / KPC, U_ref=float(UPS[iur]), U_law=float(UPS[iul]),
                         ref=sr, law=sl, law_noT=sn, A0=s0, fitU_ref=float(UPS[fit_U(d, lr)]), fitU_law=float(UPS[fit_U(d, ll)])))
    def lines(key):
        dd = [r[key]["d"] for r in rows]; ee = [r[key]["e"] for r in rows]
        sh = [(r[key]["D"], r[key]["eD"]) for r in rows if r[key]["D"] is not None]
        c1 = cls(dd, ee); c2 = cls([a for a, _ in sh], [b for _, b in sh]) if len(sh) >= 1 else None
        return c1, c2, len(rows) - len(sh)
    L = {}
    for key in ("ref", "law", "law_noT", "A0"):
        c1, c2, nleft = lines(key); L[key] = dict(L1=c1, L2=c2, shape_left_out=nleft)
    rr = dict(rms=math.sqrt(ref_sums[0] / ref_sums[2]), mean=ref_sums[1] / ref_sums[2]); rl = dict(rms=math.sqrt(law_sums[0] / law_sums[2]), mean=law_sums[1] / law_sums[2])
    L["ref"]["L3"] = dict(fit_mode=rr, law_fit_mode=rl, line=bool(rr["rms"] <= rl["rms"] + 0.010 and abs(rr["mean"]) <= 0.05))
    L["law"]["L3"] = dict(fit_mode=rl, line=bool(rl["rms"] <= 0.0660 and abs(rl["mean"]) <= 0.05))
    if per is None: per = chi2_A(D, ft, "fit" if uc == "fit" else uc)
    AI = a_interval(per, D, jk)
    n = len(D); power = bool(n >= 5 and any(AI["excl"].values()))
    fails = [k for k in ("L1", "L2", "L3") if not (L["ref"][k]["line"] if L["ref"][k] is not None else False)]
    if not AI["A1_inside"]: fails = ["A = 1 outside the 95 % interval"] + fails
    if n < 5: word = "NO POWER (n < 5)"
    elif not power: word = "NO POWER (interval excludes none of 0, 1, 2)"
    elif fails: word = "REFERENCE FAILS AT THE RECORD SHARE [" + "; ".join(fails) + "]"
    else: word = "REFERENCE FITS AT THE RECORD SHARE"
    lf = [k for k in ("L1", "L2", "L3") if not (L["law"][k]["line"] if L["law"][k] is not None else False)]
    law_word = "THE LAW FITS" if not lf else "THE LAW FAILS [" + "; ".join(lf) + "]"
    return dict(n=n, ucase=ucase, withT_ref=withT_ref, rows=rows, lines=L, A=AI, power=power, word=word, law_word=law_word), per

# ---------------- known answers
RES = dict(lane="JNT1R", reading="543118d9b8", mode=MODE, note="Adopts nothing. kappa = 1/2 FITTED; not theory closed.", KA={}, foot={})
P(f"JNT1R {MODE} (reading 543118d9b8). Adopts nothing. kappa = 1/2 FITTED; not theory closed.")
P(f"XTAB {XTAB}")
if MODE == "MAIN":
    n175 = len(GALS); ka1 = {"n": n175}
    tgt = {("canonical", "law"): (0.1124, 0.0504), ("canonical", "exact"): (0.1181, 0.0594), ("alt", "law"): (0.1029, 0.0239)}
    ok1 = n175 == 175
    for (ft, kind), (trms, tmean) in tgt.items():
        a = b = c = 0.0
        for i, q in enumerate(GALS):
            lg = np.log10(np.maximum(glaw(q["GB"], A0[ft]), 1e-300)) + (TF[ft][i] if kind == "exact" else 0.0)
            OK = q["OK"][:, IU[0.50]]; r = np.log10(q["GO"]) - lg[:, IU[0.50]]; w = q["W"][OK]
            a += float((w * r[OK]).sum()); b += float((w * r[OK] ** 2).sum()); c += float(w.sum())
        rms, mean = math.sqrt(b / c), a / c; ok = abs(rms - trms) <= 5e-4 and abs(mean - tmean) <= 5e-4; ok1 &= ok
        ka1[f"{ft}_{kind}"] = dict(rms=rms, mean=mean, target=[trms, tmean], pass_=ok)
        P(f"KA1 [{ft} {kind}] fixed U 0.50 on {n175}: rms {rms:.4f} mean {mean:+.4f} (QX8 {trms} / +{tmean}) -> {'PASS' if ok else 'FAIL'}")
    ka1["pass_"] = bool(ok1); RES["KA"]["KA1"] = ka1
    # KA2: SRJ3's zC 400569 with the own halo at z
    z, lMb, Re_k, Vc = 2.24, 10.95, 4.31, 241.0; X = XTAB["canonical"]["z1.0"]; Mb = 10 ** lMb; Re = Re_k * KPC
    gb = G * Mb / 2 * MS / Re ** 2; gm = gb + G * float(CR(Re, Mb, X, z, 1.0)) / Re ** 2; go = (Vc * 1e3) ** 2 / Re
    dd = math.log10(go / gb) - math.log10(gm / gb); ok2 = abs(dd - (-0.0061041)) <= 1e-6
    RES["KA"]["KA2"] = dict(d=dd, target=-0.0061041, pass_=bool(ok2)); P(f"KA2 SRJ3 zC 400569: d {dd:+.7f} (srj3.json -0.0061041) -> {'PASS' if ok2 else 'FAIL'}")
    # KA3: membership from own v_vir
    ka3 = {}
    for ft in FOOTS:
        X0 = XTAB[ft]["z0.0"]; above = []; vv = {}
        for q in GALS:
            H = halo(X0, Mb_pd1(q), 0.0, 1.0); v = math.sqrt(G_MPC * H["M200c"] / H["r200c"]); vv[q["name"]] = v
            if v > VST[ft]: above.append(q["name"])
        ok3 = sorted(above) == sorted(MEMB[ft]); close = sorted(((abs(v - VST[ft]), n) for n, v in vv.items()))[:3]
        ka3[ft] = dict(above=above, srj2=MEMB[ft], pass_=bool(ok3), nearest_to_boundary=[(n, vv[n]) for _, n in close])
        P(f"KA3 [{ft}] own v_vir above {VST[ft]}: {len(above)} {above} vs SRJ2 {len(MEMB[ft])} -> {'PASS' if ok3 else 'FAIL'}; nearest the boundary {[(n, round(vv[n], 1)) for _, n in close]}")
    RES["KA"]["KA3"] = ka3
    # KA4: SI second route for one member
    nm = "NGC5371"; q = GALS[BYNAME[nm]]; Mb = Mb_pd1(q); X0 = XTAB["canonical"]["z0.0"]; H = halo(X0, Mb, 0.0, 1.0)
    GSI, MSUN, MPCSI = 6.674e-11, 1.989e30, 3.0857e22; H0 = 67.36e3 / MPCSI; rhom = Om * 3 * H0 ** 2 / (8 * math.pi * GSI)
    r200 = (3 * H["M"] / h * MSUN / (4 * math.pi * 200 * rhom)) ** (1 / 3); rs = r200 / H["c"]; Rl = float(q["R"][-1]) * 3.0857e19
    mm = lambda x: math.log(1 + x) - x / (1 + x); crsi = X0 * Mb * MSUN * mm(Rl / rs) / mm(H["cta"]); crsc = float(CR(Rl, Mb, X0, 0.0, 1.0)) * MSUN / MS
    ok4 = abs(r200 / (H["r200"] / h * MPCSI) - 1) <= 0.01 and abs(crsi / crsc - 1) <= 0.01
    RES["KA"]["KA4"] = dict(name=nm, r200m_SI_kpc=r200 / 3.0857e19, r200m_script_kpc=H["r200"] / h * 1e3, rs_kpc=rs / 3.0857e19, c=H["c"], CR_SI_Msun=crsi / MSUN, CR_script_Msun=crsc / MSUN, pass_=bool(ok4))
    P(f"KA4 SI {nm}: r_200m {r200 / 3.0857e19:.2f} vs {H['r200'] / h * 1e3:.2f} kpc; c {H['c']:.2f}, r_s {rs / 3.0857e19:.1f} kpc; C_R(R_last {Rl / 3.0857e19:.1f} kpc) {crsi / MSUN:.4e} vs {crsc / MSUN:.4e} Msun -> {'PASS' if ok4 else 'FAIL'}")
    RES["KA"]["all_pass"] = bool(ok1 and ok2 and all(ka3[f]["pass_"] for f in FOOTS) and ok4)

# ---------------- the row
def build(ft, sD_sign=0, inc=0, shuffle=False):
    idx = [BYNAME[n] for n in MEMB[ft]]; D = []
    for k, i in enumerate(idx):
        m = GALS[i]["meta"]; sD = 1.0 + sD_sign * m["eD"] / m["D"]
        eVsub = None
        if shuffle:
            j = idx[(k + 1) % len(idx)]; qj = GALS[j]; frac = np.clip(qj["eV"], 1, None) / np.clip(qj["Vobs"], 1, None)
            xn_j = qj["R"] / qj["R"][-1]; xn_i = GALS[i]["R"] / GALS[i]["R"][-1]; eVsub = np.interp(xn_i, xn_j, frac) * np.clip(GALS[i]["Vobs"], 1, None)
        D.append(gal_data(i, sD, inc, eVsub))
    return D

def fmt_word(g): return f"{g['word']} | {g['law_word']}"
for ft in FOOTS:
    R = RES["foot"][ft] = {}
    D = build(ft, shuffle=(MODE == "MUT_E"))
    main, per = grade(D, ft, "0.5"); R["main"] = main
    A = main["A"]; Lr, Ll = main["lines"]["ref"], main["lines"]["law"]
    P(f"\n[{ft}] n {main['n']} {MEMB[ft]}")
    P(f"[{ft}] {'galaxy':12s} Vflat logMb Rlast | ref A=1: d      Delta  | law+T: d     Delta  | law noT d | A=0: d   Delta | A_i")
    for r, Ai in zip(main["rows"], A["per_gal_A"]):
        fD = lambda x: f"{x:+.3f}" if x is not None else "  n/a "
        P(f"[{ft}] {r['name']:12s} {r['Vflat']:5.0f} {r['logMb']:5.2f} {r['Rlast_kpc']:5.1f} | {r['ref']['d']:+.3f} {fD(r['ref']['D'])} | {r['law']['d']:+.3f} {fD(r['law']['D'])} | {r['law_noT']['d']:+.3f} | {r['A0']['d']:+.3f} {fD(r['A0']['D'])} | {Ai:.2f}  (e {r['ref']['e']:.4f}, fitU ref {r['fitU_ref']:.2f} law {r['fitU_law']:.2f})")
    for key, lab in (("ref", "reference A=1"), ("law", "law + T"), ("law_noT", "law no T"), ("A0", "A = 0 (no cold)")):
        l1, l2 = main["lines"][key]["L1"], main["lines"][key]["L2"]
        P(f"[{ft}] {lab:16s} L1 off {l1['med']:+.4f} se {l1['se']:.4f} -> {'holds' if l1['line'] else 'FAILS'}; L2 shape {l2['med']:+.4f} se {l2['se']:.4f} -> {'holds' if l2['line'] else 'FAILS'} (left out {main['lines'][key]['shape_left_out']})")
    P(f"[{ft}] L3 fit mode: reference rms {Lr['L3']['fit_mode']['rms']:.4f} mean {Lr['L3']['fit_mode']['mean']:+.4f} vs law+T rms {Lr['L3']['law_fit_mode']['rms']:.4f} mean {Lr['L3']['law_fit_mode']['mean']:+.4f} -> ref {'holds' if Lr['L3']['line'] else 'FAILS'}; law abs line {'holds' if Ll['L3']['line'] else 'FAILS'}")
    P(f"[{ft}] A_best {A['A_best']:.2f} (chi2_min {A['chi2_min']:.0f} on {A['npts']} pts, rescale {A['rescale']:.1f}); chi2 95 % {A['chi2_95']}, 68 % {A['chi2_68']}; jk se {A.get('jk_se', float('nan')):.3f}; "
      f"95 % [{A['int95'][0]:.2f}, {A['int95'][1]:.2f}], 68 % [{A['int68'][0]:.2f}, {A['int68'][1]:.2f}]; excludes {A['excl']}; per-galaxy A median {np.median(A['per_gal_A']):.2f}")
    P(f"[{ft}] WORD (fixed U 0.50): {fmt_word(main)}")
    if MODE != "MAIN":
        continue
    # brackets
    BR = {}
    for uc in ("0.35", "0.65", "fit"):
        g, _ = grade(D, ft, uc); BR[f"U {uc}"] = g
    g, _ = grade(D, ft, "0.5", withT_ref=True, per=per); BR["ref + T"] = g
    for s, lab in ((+1, "D +eD"), (-1, "D -eD")):
        g, _ = grade(build(ft, sD_sign=s), ft, "0.5"); BR[lab] = g
    for s, lab in ((+1, "i +eInc"), (-1, "i -eInc")):
        g, _ = grade(build(ft, inc=s), ft, "0.5"); BR[lab] = g
    JK = {}
    if len(D) >= 3:
        for k in range(len(D)):
            Dk = D[:k] + D[k + 1:]; g, _ = grade(Dk, ft, "0.5", per=np.delete(per, k, 0)); JK[D[k]["name"]] = g
    for lab, g in list(BR.items()) + [(f"jk -{k}", v) for k, v in JK.items()]:
        P(f"[{ft}]   {lab:14s}: A_best {g['A']['A_best']:.2f} 95 % [{g['A']['int95'][0]:.2f}, {g['A']['int95'][1]:.2f}]; ref L1 {g['lines']['ref']['L1']['med']:+.4f} L2 {g['lines']['ref']['L2']['med']:+.4f}; law L1 {g['lines']['law']['L1']['med']:+.4f} L2 {g['lines']['law']['L2']['med']:+.4f} -> {fmt_word(g)}")
    words = {main["word"]} | {g["word"] for g in BR.values()} | {g["word"] for g in JK.values()}
    lwords = {main["law_word"]} | {g["law_word"] for g in BR.values()} | {g["law_word"] for g in JK.values()}
    frag = len(words) > 1; lfrag = len(lwords) > 1
    R["brackets"] = {k: dict(word=g["word"], law_word=g["law_word"], A=g["A"], ref_L1=g["lines"]["ref"]["L1"], ref_L2=g["lines"]["ref"]["L2"], ref_L3=g["lines"]["ref"]["L3"], law_L1=g["lines"]["law"]["L1"], law_L2=g["lines"]["law"]["L2"], law_L3=g["lines"]["law"]["L3"]) for k, g in BR.items()}
    R["jackknife"] = {k: dict(word=g["word"], law_word=g["law_word"], A_best=g["A"]["A_best"], int95=g["A"]["int95"], ref_L1=g["lines"]["ref"]["L1"]["med"], ref_L2=g["lines"]["ref"]["L2"]["med"]) for k, g in JK.items()}
    R["fragile"] = frag; R["law_fragile"] = lfrag
    # TW-N must make L1 fail on canonical (power to see the cold component)
    twn = main["lines"]["A0"]["L1"]; R["TWN"] = dict(L1=twn, bites=bool(not twn["line"]))
    P(f"[{ft}] TW-N (A = 0): L1 off {twn['med']:+.4f} -> {'FAILS (bites)' if not twn['line'] else 'holds (DOES NOT BITE)'}")
    R["word_as_frozen_pre_mutation"] = main["word"] + (" FRAGILE" if frag and not main["word"].startswith("NO POWER") else "")
    R["law_word"] = main["law_word"] + (" FRAGILE" if lfrag else "")
    P(f"[{ft}] FRAGILE (ref word) {frag}: {sorted(words)}; law FRAGILE {lfrag}: {sorted(lwords)}")

if MODE == "MAIN":
    json.dump(RES, open(os.path.join(HERE, "jnt1r.json"), "w"), indent=1, default=float)
    open(os.path.join(HERE, "jnt1r.out"), "w").write("\n".join(OUT) + "\nAdopts nothing. kappa = 1/2 FITTED; not theory closed.\n")
else:
    tag = MODE.split("_")[1]
    json.dump(RES, open(os.path.join(HERE, f"jnt1r_MUTATE_{tag}.json"), "w"), indent=1, default=float)
    open(os.path.join(HERE, f"jnt1r_MUTATE_{tag}.out"), "w").write("\n".join(OUT) + "\nAdopts nothing. kappa = 1/2 FITTED; not theory closed.\n")
