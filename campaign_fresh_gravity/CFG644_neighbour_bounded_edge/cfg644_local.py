#!/usr/bin/env python3
"""CFG644 local arm: T1 SPARC (KT2017 neighbours), T4 MW outer slope (M31; LMC bracket), T5 Tian+26 groups (KT2017 neighbours,
CFG543 sigma_log) and the X-COP bracket.  Criteria: FROZEN_CRITERIA.md (6a03c0870).
Read-only reuse: cfg644_lib, CFG4_common.load_sparc, the CFG11 KT2017 conventions (V/75, M_sun,K 3.28, Upsilon_K 0.6, SPARC gas
fit), CFG513 Prof via the CFG515 head (as CFG522 does), CFG543's module (read_groups, sigma_log, stats), CFG532b JSON.
MUTATE (CFG644_MUTATE=1): M1 r_nb = inf -> T1 rms, T4 profile and T5 P2 equal the candidate-B (record) values exactly.
Run: nice -n 10 python3 cfg644_local.py ; CFG644_MUTATE=1 nice -n 10 python3 cfg644_local.py
"""
import os, sys
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"):
    os.environ[_v] = "1"
import io, math, json, glob, time, contextlib
import numpy as np
from astropy.io import fits

T0 = time.time()
HERE = os.path.dirname(os.path.abspath(__file__))
LANES = os.path.dirname(HERE)
REPO = os.path.dirname(LANES)
sys.path.insert(0, HERE)
import cfg644_lib as N                                                       # noqa: E402
C, L = N.C, N.L
sys.path.insert(0, LANES)
import CFG4_common as C4                                                     # noqa: E402  (read-only)
try:
    os.nice(10)
except OSError:
    pass
MUTATE = os.environ.get("CFG644_MUTATE", "0") == "1"
SUF = "_MUTATE" if MUTATE else ""
DD = os.path.join(REPO, "real_research", "data")
FOOTS = ("canonical", "alt")
G = C.G_MPC
LOG, CHK = [], {}
RES = {"lane": "CFG644", "script": "cfg644_local", "mutate": MUTATE, "criteria_commit": "6a03c0870",
       "settings": "kappa = 1/2 FITTED; footings never pooled; cold energy mass required; not theory closed"}
DV_WIN, RPROJ = 750.0, 5.0                                                   # km/s, Mpc


def P(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); LOG.append(s)


def check(name, ok, msg, lb=True):
    CHK[name] = dict(ok=bool(ok), load_bearing=lb, msg=msg); P(f"  [{'PASS' if ok else 'FAIL'}]{'' if lb else ' (reported)'} {name}: {msg}")


P(__doc__.split("Run:")[0].strip())


def RNB(Mo, Mj, D, a0):
    if MUTATE:
        return np.inf, np.inf
    return N.r_nb_pairwise(Mo, Mj, D, G, a0), N.r_nb_summed(Mo, Mj, D, G, a0)


# ------------------------------------------------------------------ KT2017 (CFG11 conventions)
def read_vizier(path):
    rows, hdr, skip = [], None, 0
    for line in open(path):
        if line.startswith("#") or not line.strip():
            continue
        if hdr is None:
            hdr = line.rstrip("\n").split("\t"); skip = 2; continue
        if skip:
            skip -= 1; continue
        rows.append(line.rstrip("\n").split("\t"))
    return hdr, rows


def fnum(s):
    s = s.strip()
    return float(s) if s else float("nan")


hg, rg_ = read_vizier(os.path.join(DD, "kt2017_galaxies.tsv"))
ig = {k: i for i, k in enumerate(hg)}
kpgc = np.array([int(r[ig["PGC"]]) for r in rg_]); kgid = np.array([int(r[ig["PGC1"]]) for r in rg_])
kra = np.array([fnum(r[ig["RAJ2000"]]) for r in rg_]); kde = np.array([fnum(r[ig["DEJ2000"]]) for r in rg_])
kks = np.array([fnum(r[ig["Ksmag"]]) for r in rg_]); khrv = np.array([fnum(r[ig["HRV"]]) for r in rg_])
ug, inv = np.unique(kgid, return_inverse=True)
vmean = np.bincount(inv, weights=np.nan_to_num(khrv)) / np.maximum(np.bincount(inv, weights=np.isfinite(khrv).astype(float)), 1)
KV = vmean[inv]; KD = KV / 75.0
GAL = C4.load_sparc()
ls_, lg_ = [], []
for g in GAL:
    m = g["meta"]
    if m and m["MHI"] > 0 and m["L36"] > 0:
        ms_ = 0.5 * m["L36"] * 1e9; ls_.append(math.log10(ms_)); lg_.append(math.log10(1.33 * m["MHI"] * 1e9 / ms_))
cfit = np.polyfit(ls_, lg_, 1)
LKk = 10 ** (-0.4 * (kks - (5 * np.log10(np.where(KD > 0, KD, np.nan)) + 25) - 3.28))
Msk = 0.6 * LKk
MBk = np.where(np.isfinite(Msk) & (Msk > 0), Msk * (1 + 10 ** np.polyval(cfit, np.log10(np.where(Msk > 0, Msk, 1.0)))), 0.0)
# group bodies: summed member baryons at the principal galaxy (first member if the principal is absent)
GB = {}
for gidx, gval in enumerate(ug):
    m = np.nonzero(inv == gidx)[0]
    pr = m[kpgc[m] == gval]; p0 = pr[0] if len(pr) else m[0]
    GB[int(gval)] = dict(Mb=float(MBk[m].sum()), ra=kra[p0], de=kde[p0], V=float(vmean[gidx]), members=m)
GIDS = np.array(list(GB.keys())); GRA = np.array([GB[k]["ra"] for k in GIDS]); GDE = np.array([GB[k]["de"] for k in GIDS])
GV = np.array([GB[k]["V"] for k in GIDS]); GMB = np.array([GB[k]["Mb"] for k in GIDS])
hG, rG_ = read_vizier(os.path.join(DD, "kt2017_groups_full.tsv")); iG = {k: i for i, k in enumerate(hG)}
GDc = {int(r[iG["PGC1"]]): fnum(r[iG["Dist"]]) for r in rG_}
GDIST = np.array([GDc.get(int(k), float("nan")) for k in GIDS]); GDIST = np.where(np.isfinite(GDIST) & (GDIST > 0), GDIST, GV / 75.0)
P(f"KT2017: {len(kpgc)} galaxies in {len(GIDS)} groups; SPARC gas fit log(Mg/M*) = {cfit[0]:+.3f} log M* {cfit[1]:+.3f}")


def angsep(ra1, de1, ra2, de2):
    r1, d1, r2, d2 = map(np.radians, (ra1, de1, ra2, de2))
    c = np.sin(d1) * np.sin(d2) + np.cos(d1) * np.cos(d2) * np.cos(r1 - r2)
    return np.arccos(np.clip(c, -1, 1))


def sep_lb(theta, Dist):
    """strict lower bound on the 3-D separation from a body at distance Dist to anything on the ray at angle theta."""
    return Dist * np.sin(np.minimum(theta, math.pi / 2))


def kt_neighbours(ra, de, V, Dist, own_gid, own_k=None, members=True):
    """bodies: other members of the own group (individually; members=False drops the whole own group), other groups (summed).
    Returns masses, the projected lower-bound separations (primary) and the reported 3-D separations (KT2017 'Dist' if given,
    else V/75; own-group members at the own distance)."""
    Mj, Dj, D3 = [], [], []
    if own_gid is not None and members:
        for i in GB[own_gid]["members"]:
            if own_k is not None and i == own_k:
                continue
            if MBk[i] > 0:
                d_ = float(sep_lb(angsep(ra, de, kra[i], kde[i]), Dist)); Mj.append(MBk[i]); Dj.append(d_); D3.append(d_)
    sel = (GIDS != (own_gid if own_gid is not None else -1)) & (np.abs(GV - V) <= DV_WIN) & (GMB > 0)
    th = angsep(ra, de, GRA[sel], GDE[sel])
    s = sep_lb(th, Dist)
    k = s <= RPROJ
    Dg = GDIST[sel][k]
    d3 = np.sqrt(np.maximum(Dist ** 2 + Dg ** 2 - 2 * Dist * Dg * np.cos(th[k]), 0.0))
    Mj += list(GMB[sel][k]); Dj += list(s[k]); D3 += list(np.maximum(d3, s[k]))
    return np.array(Mj), np.maximum(np.array(Dj), 1e-6), np.maximum(np.array(D3), 1e-6)


# ================================================================== T1 SPARC
P("\n================ T1: SPARC with KT2017 neighbours ================")
POS = json.load(open(os.path.join(DD, "sparc_positions_merged.json")))
T1 = {f: dict(rows=[]) for f in FOOTS}
nmatch = 0; nomatch = []
for g in GAL:
    m = g["meta"]; nm = g["name"]
    if not m or nm not in POS or POS[nm].get("ra") is None:
        nomatch.append(nm); continue
    ra, de = POS[nm]["ra"], POS[nm]["dec"]
    s = angsep(ra, de, kra, kde) * 180 / math.pi * 60
    k = int(np.argmin(s))
    if s[k] > 1.0:
        nomatch.append(nm); continue
    nmatch += 1
    Dm = m["D"]; Mb = 0.5 * m["L36"] * 1e9 + 1.33 * m["MHI"] * 1e9
    Rl = float(np.max(g["R"])) / 1e3
    V = khrv[k] if np.isfinite(khrv[k]) else KV[k]
    Mj, Dj, D3 = kt_neighbours(ra, de, V, Dm, int(kgid[k]), k)
    for foot in FOOTS:
        a0 = C.A0[foot]
        rp, rs = RNB(Mb, Mj, Dj, a0)
        r3 = RNB(Mb, Mj, D3, a0)[0]
        T1[foot]["rows"].append(dict(name=nm, Mb=Mb, R_last_kpc=Rl * 1e3, r_nb_kpc=rp * 1e3, r_nb_S_kpc=rs * 1e3, r_nb_3D_kpc=r3 * 1e3,
                                     r_edge_kpc=float(N.r_edge(Mb, G, a0)) * 1e3, n_nbr=len(Mj),
                                     n_closing=int((N.mtot(Mj) >= N.mtot(Mb)).sum()) if len(Mj) else 0))


def law_rms(g, rnb_kpc, ups=(0.5, 0.7), foot="canonical"):
    """rotmod law with the settled phantom frozen beyond r_nb (Upsilon 0.5/0.7; the record's ALG-type curve on rotmod baryons)."""
    a0 = C.A0[foot] / 1e3                                                    # (km/s)^2/kpc
    R = g["R"]; Vb2 = g["Vgas"] * np.abs(g["Vgas"]) + ups[0] * g["Vdisk"] ** 2 + ups[1] * g["Vbul"] ** 2
    gN = np.maximum(Vb2, 1e-9) / R
    gl = C.nu_mono(gN / a0) * gN
    Mph = (gl - gN) * R ** 2                                                 # G M_ph(<R)
    if np.isfinite(rnb_kpc) and rnb_kpc < R[-1]:
        Mf = np.interp(rnb_kpc, R, Mph)
        Mph = np.where(R > rnb_kpc, np.minimum(Mph, Mf), Mph)
    V = np.sqrt(np.maximum(Vb2 + Mph / R, 1e-9))
    ok = g["Vobs"] > 0
    return float(np.sqrt(np.mean(np.log10(g["Vobs"][ok] / V[ok]) ** 2)))


GBN = {g["name"]: g for g in GAL}
for foot in FOOTS:
    rows = T1[foot]["rows"]
    bites = [r for r in rows if r["r_nb_kpc"] < r["R_last_kpc"]]
    bitesS = [r for r in rows if r["r_nb_S_kpc"] < r["R_last_kpc"]]
    bites3 = [r for r in rows if r["r_nb_3D_kpc"] < r["R_last_kpc"]]
    ratio = np.array([r["r_nb_kpc"] / r["R_last_kpc"] for r in rows])
    ratioS = np.array([r["r_nb_S_kpc"] / r["R_last_kpc"] for r in rows])
    drms = {}
    for r in bites + [x for x in bitesS if x not in bites]:
        gg = GBN[r["name"]]
        drms[r["name"]] = dict(primary=law_rms(gg, r["r_nb_kpc"], foot=foot) - law_rms(gg, np.inf, foot=foot),
                               bracket_S=law_rms(gg, r["r_nb_S_kpc"], foot=foot) - law_rms(gg, np.inf, foot=foot))
    allrms0 = np.array([law_rms(GBN[r["name"]], np.inf, foot=foot) for r in rows])
    allrms1 = np.array([law_rms(GBN[r["name"]], r["r_nb_kpc"], foot=foot) for r in rows])
    T1[foot].update(n_matched=len(rows), n_bite=len(bites), n_bite_S=len(bitesS), bites=[r["name"] for r in bites],
                    bites_S=[r["name"] for r in bitesS], bites_3D_reported=[r["name"] for r in bites3], d_rms=drms, min_rnb_over_Rlast=float(np.min(ratio)),
                    min_rnbS_over_Rlast=float(np.min(ratioS)),
                    pct_rnb_over_Rlast={p_: float(np.percentile(np.where(np.isfinite(ratio), ratio, 1e9), p_)) for p_ in (1, 5, 16, 50)},
                    frac_with_closing=float(np.mean([r["n_closing"] > 0 for r in rows])),
                    sample_mean_rms_B=float(allrms0.mean()), sample_mean_rms_HNB=float(allrms1.mean()),
                    verdict="UNCHANGED" if not bites else "BITES")
    lowest = sorted(rows, key=lambda r: r["r_nb_kpc"] / r["R_last_kpc"])[:5]
    P(f"  [{foot}] matched {len(rows)} (no environment data: {len(nomatch)}); with a closing neighbour {T1[foot]['frac_with_closing']:.2f}; "
      f"bite (r_nb < R_last) {len(bites)} {T1[foot]['bites']}; bracket S {len(bitesS)} {T1[foot]['bites_S']}; min r_nb/R_last "
      f"{T1[foot]['min_rnb_over_Rlast']:.2f} (S {T1[foot]['min_rnbS_over_Rlast']:.2f}); sample mean rms {allrms0.mean():.5f} -> {allrms1.mean():.5f}; "
      f"reported 3-D (KT distances) bites {T1[foot]['bites_3D_reported']}")
    for r in lowest:
        P(f"      lowest: {r['name']:10s} R_last {r['R_last_kpc']:.1f} kpc, r_nb {r['r_nb_kpc']:.1f} kpc (S {r['r_nb_S_kpc']:.1f}), "
          f"r_edge {r['r_edge_kpc']:.0f} kpc, closing {r['n_closing']}/{r['n_nbr']}; 3-D r_nb {r['r_nb_3D_kpc']:.1f} kpc")
    for k_, v_ in drms.items():
        P(f"      d rms {k_}: primary {v_['primary']:+.4f} dex, bracket S {v_['bracket_S']:+.4f} dex")
    P(f"  [{foot}] T1 VERDICT: {T1[foot]['verdict']}")
    if MUTATE:
        check(f"M1 [{foot}] r_nb = inf: SPARC sample rms unchanged exactly", allrms0.mean() == allrms1.mean(), "identical")
T1["no_environment_data"] = nomatch
RES["T1"] = T1

# ================================================================== T4 MW
P("\n================ T4: MW outer slope (M31 neighbour; LMC bracket) ================")
p515 = os.path.join(LANES, "CFG515_census_edge_resolution", "cfg515_mw.py")
src = open(p515).read(); mk = "J513 = json.load("
assert src.count(mk) == 1
for v in ("CFG515_MUTATE", "CFG513_MUTATE"):
    os.environ.pop(v, None)
NSM = {"__file__": p515, "__name__": "cfg515_ro"}
with contextlib.redirect_stdout(io.StringIO()):
    exec(compile(src[:src.index(mk)], "cfg515_ro", "exec"), NSM)
Prof, GK = NSM["Prof"], NSM["G"]
MB_PRIM, MB_M31, D_LG = NSM["MB_PRIM"], NSM["MB_M31"], NSM["D_LG"]
A0K = NSM["NS"]["A0"]
MB_LMC, D_LMC = 3e9, 50.0
J532 = json.load(open(os.path.join(LANES, "CFG532_mw_gaia_rotation_curves", "cfg532b_results.json")))


def census_rta_kpc(Mb):
    f, lMta = L.fret_census(Mb)
    R = (3 * 10 ** lMta / (4 * math.pi * 11.806 * 0.315 * 2.775e11)) ** (1 / 3)
    return R * 1000 / 0.674


def slope(R, V):
    return float(np.polyfit(np.log(R), np.log(V), 1)[0])


T4 = {}
for foot in FOOTS:
    fm = L.fret_census(MB_PRIM)[0]; f31 = L.fret_census(MB_M31)[0]
    mw = Prof("mw", Mb=MB_PRIM, foot=foot, fret=fm)
    m31 = Prof("m31", Mb=MB_M31, foot=foot, fret=f31, point=True)
    lmc = Prof("lmc", Mb=MB_LMC, foot=foot, fret=L.fret_census(MB_LMC)[0], point=True)
    gmw = lambda r: GK * mw.M_enc(np.asarray(r, float)) / np.asarray(r, float) ** 2
    Tmw = mw.Mb_tot() + mw.Mcold; T31 = m31.Mb_tot() + m31.Mcold; Tl = lmc.Mb_tot() + lmc.Mcold

    def pair(other, D):
        lo, hi = 0.0, 1.0
        for _ in range(80):
            t = 0.5 * (lo + hi); r = t * D
            if float(gmw(np.array([r]))[0]) > GK * float(other.M_enc(np.array([D - r]))[0]) / (D - r) ** 2:
                lo = t
            else:
                hi = t
        return 0.5 * (lo + hi) * D

    def summed(others):
        Dm = min(D for _, D in others); lo, hi = 0.0, 1.0
        for _ in range(80):
            t = 0.5 * (lo + hi); r = t * Dm
            gs = sum(GK * float(o.M_enc(np.array([D - r]))[0]) / (D - r) ** 2 for o, D in others)
            if float(gmw(np.array([r]))[0]) > gs:
                lo = t
            else:
                hi = t
        return 0.5 * (lo + hi) * Dm

    if MUTATE:
        rnb = rS = np.inf
    else:
        rnb = pair(m31, D_LG) if T31 >= Tmw else np.inf
        rS = summed([(m31, D_LG), (lmc, D_LMC)]) if (T31 + Tl) >= Tmw else np.inf
    rta = census_rta_kpc(MB_PRIM)

    def Mh(r, rcut):
        r = np.asarray(r, float)
        if not np.isfinite(rcut) or rcut >= mw.redge:
            return mw.M_enc(r)
        Mu = mw.Mcold - float(mw.Mdark(np.array([rcut]))[0])
        return mw.Mb_enc(r) + mw.Mdark(np.minimum(r, rcut)) + Mu * np.minimum(r / rta, 1.0) ** 3

    Rw = np.linspace(15.0, 27.5, 26)
    out = {}
    for nm_, rc in (("B", np.inf), ("HNB", rnb), ("bracket_S", rS)):
        V = np.sqrt(GK * Mh(Rw, rc) / Rw)
        out[nm_] = dict(r_cut_kpc=float(rc), slope_15_27p5=slope(Rw, V), V20=float(np.sqrt(GK * Mh(np.array([20.0]), rc)[0] / 20.0)),
                        Vc60=float(np.sqrt(GK * Mh(np.array([60.0]), rc)[0] / 60.0)),
                        M_settled_total=float(Mh(np.array([1e5]), rc)[0] - mw.Mb_tot()) if np.isfinite(rc) else float(mw.Mcold),
                        M_inside_780=float(Mh(np.array([780.0]), rc)[0]))
    vpred = NSM["v_pred"]
    tim = {}
    for nm_, rc in (("B", np.inf), ("HNB", rnb)):
        vp = vpred(lambda d, rc=rc: GK * float(Mh(np.array([d]), rc)[0] + m31.M_enc(np.array([d]))[0]) / d ** 2)
        tim[nm_] = dict(v_pred=float(vp), z=float((abs(vp) - abs(NSM["VR_LG"])) / NSM["EVR_LG"]))
    out["LG_timing_CONTEXT"] = tim
    dsl = out["HNB"]["slope_15_27p5"] - out["B"]["slope_15_27p5"]
    dslS = out["bracket_S"]["slope_15_27p5"] - out["B"]["slope_15_27p5"]
    dV = math.log10(out["HNB"]["V20"] / out["B"]["V20"])
    key = "canonical|RMv" if foot == "canonical" else "alt|RMv"
    miss = J532["combined"]["RGB_LIM"].get(key, {}).get("pairs", {}).get("Ou24+Jiao23|rho0.0", {}).get("mean", float("nan"))
    verdict = ("UNCHANGED" if (rnb > 27.5 and abs(dV) < 0.001) else
               ("RESCUES" if (np.isfinite(miss) and dsl <= 0.5 * miss) else "WORSENS" if dsl > 0 else "UNCHANGED"))
    T4[foot] = dict(r_nb_kpc=float(rnb), r_nb_S_kpc=float(rS), r_edge_mw_kpc=float(mw.redge), r_ta_mw_kpc=rta, M31_closes=bool(T31 >= Tmw),
                    Mtot_mw=Tmw, Mtot_m31=T31, profiles=out, d_slope=dsl, d_slope_S=dslS, dlogV20=dV, cfg532b_miss_Ou24_Jiao23=miss,
                    verdict=verdict)
    P(f"  [{foot}] MW edge {mw.redge:.0f} kpc, r_ta {rta:.0f} kpc; M_tot MW {Tmw:.2e} vs M31 {T31:.2e} (closes {T31 >= Tmw}); "
      f"r_nb {rnb:.1f} kpc (bracket S with LMC {rS:.1f} kpc)")
    P(f"      LG timing (context, CFG515 strict statistic, M31 unbounded since the MW does not close its basin): B v {tim['B']['v_pred']:.1f} "
      f"(z {tim['B']['z']:+.1f}) -> H-NB v {tim['HNB']['v_pred']:.1f} (z {tim['HNB']['z']:+.1f})")
    if foot == "canonical" and not MUTATE:
        check("K7 candidate-B LG timing reproduces CFG515's census cell (v -168.7, z +13.5; within 0.2 km/s)", abs(tim["B"]["v_pred"] + 168.7) < 0.2,
              f"v {tim['B']['v_pred']:.2f}")
    for nm_, o in [(k_, v_) for k_, v_ in out.items() if k_ != "LG_timing_CONTEXT"]:
        P(f"      {nm_:9s}: slope(15-27.5) {o['slope_15_27p5']:+.5f}  V20 {o['V20']:.3f}  Vc60 {o['Vc60']:.2f}  settled {o['M_settled_total']:.3e}  "
          f"M(<780) {o['M_inside_780']:.3e}")
    P(f"  [{foot}] d slope H-NB {dsl:+.2e} (S {dslS:+.2e}); d log V20 {dV:+.2e}; CFG532b miss (Ou24+Jiao23) {miss:+.3f} -> T4 VERDICT: {verdict}")
    if MUTATE:
        check(f"M1 [{foot}] r_nb = inf: MW profile = candidate-B Prof exactly", out["HNB"]["slope_15_27p5"] == out["B"]["slope_15_27p5"]
              and out["HNB"]["M_inside_780"] == out["B"]["M_inside_780"], "identical")
RES["T4"] = T4

# ================================================================== T5 groups (Tian+26) and X-COP bracket
P("\n================ T5: Tian+26 groups (CFG543 P2 with r_nb) and the X-COP bracket ================")
for v in ("CFG543_MUTATE",):
    os.environ.pop(v, None)
sys.path.insert(0, os.path.join(LANES, "CFG543_group_supply"))
with contextlib.redirect_stdout(io.StringIO()):
    import cfg543_group_supply as M543                                       # noqa: E402  (read-only)
rows543 = M543.read_groups()
M543.GEO = M543.gas_geometry(M543.lovisari())
J543 = json.load(open(os.path.join(LANES, "CFG543_group_supply", "cfg543_results.json")))
CFG_P2 = dict(kind="P2")
T5 = {}
grp_env = []
for o in rows543:
    s = angsep(o["ra"], o["de"], kra, kde) * 180 / math.pi * 60
    k = np.nonzero(s < 30)[0]
    if not len(k):
        grp_env.append(None); continue
    kk = k[np.argmin(np.where(np.isfinite(kks[k]), kks[k], 99))]
    gid = int(kgid[kk]); V = GB[gid]["V"]; Dist = V / 75.0
    if not np.isfinite(Dist) or Dist <= 0:
        grp_env.append(None); continue
    Mj, Dj, D3 = kt_neighbours(o["ra"], o["de"], V, Dist, gid, members=False)
    grp_env.append((Mj, Dj, gid, Dist, D3))
for foot, a0si in (("canonical", 9.36e-11), ("alt", 1.13e-10)):
    a0 = C.A0[foot]
    D_, s_, rr, D3_, s3_ = [], [], [], [], []
    for o, env in zip(rows543, grp_env):
        Mb = 10 ** o["lM"]; smult = 1.0
        if env is not None:
            Mj, Dj, gid, Dist, D3 = env
            rp, rS = RNB(Mb, Mj, Dj, a0)
            r3 = RNB(Mb, Mj, D3, a0)[0]
        else:
            rp = rS = r3 = np.inf
        Ssup = M543.COLD_PER_B * Mb / 0.10
        if np.isfinite(rp):
            smult = min(1.0, float(N.phantom(Mb, rp, G, a0)) / Ssup)
        sm3 = min(1.0, float(N.phantom(Mb, r3, G, a0)) / Ssup) if np.isfinite(r3) else 1.0
        lp = M543.sigma_log(o, a0si, CFG_P2, 0.0, smult)
        lp2 = M543.sigma_log(o, a0si, CFG_P2, 0.01, smult)
        D_.append(o["ls"] - lp); s_.append((lp2 - lp) / 0.01)
        l3 = M543.sigma_log(o, a0si, CFG_P2, 0.0, sm3); l32 = M543.sigma_log(o, a0si, CFG_P2, 0.01, sm3)
        D3_.append(o["ls"] - l3); s3_.append((l32 - l3) / 0.01)
        rr.append(dict(id=o["id"], Re_kpc=o["Re"], r_nb_kpc=float(rp) * 1e3, r_nb_S_kpc=float(rS) * 1e3, r_nb_3D_kpc=float(r3) * 1e3,
                       smult=smult, env=env is not None,
                       r_nb_over_Re=float(rp) * 1e3 / o["Re"]))
    st = M543.stats(D_, s_)
    ref = J543["footings"]["can" if foot == "canonical" else "alt"]["configs"]["P2"]
    # control: smult = 1 everywhere reproduces the record's P2
    D0 = [o["ls"] - M543.sigma_log(o, a0si, CFG_P2, 0.0, 1.0) for o in rows543]
    k6 = abs(float(np.mean(D0)) - ref["mean"])
    check(f"K6 [{foot}] CFG543 sigma_log with smult = 1 reproduces the record's P2 mean ({ref['mean']:+.5f})", k6 < 1e-10, f"|d| {k6:.1e}")
    nb5 = [x for x in rr if x["r_nb_over_Re"] < 5]
    T5[foot] = dict(P2_HNB=st, n_env=int(sum(x["env"] for x in rr)), n_rnb_lt_5Re=len(nb5), groups=rr,
                    min_rnb_over_Re=float(min(x["r_nb_over_Re"] for x in rr)),
                    n_closing_any=int(sum(np.isfinite(x["r_nb_kpc"]) for x in rr)))
    P(f"  [{foot}] Tian groups {len(rows543)}; KT2017 environment for {T5[foot]['n_env']}; with a closing neighbour "
      f"{T5[foot]['n_closing_any']}; r_nb < 5 Re: {len(nb5)} {[x['id'] for x in nb5]}; min r_nb/Re {T5[foot]['min_rnb_over_Re']:.1f}; "
      f"P2 H-NB mean {st['mean']:+.5f} (Z {st['Z']:+.2f}, {st['label']})")
    T5[foot]["P2_record"] = dict(mean=ref["mean"], Z=ref["Z"])
    st3 = M543.stats(D3_, s3_)
    n3 = [x["id"] for x in rr if x["r_nb_3D_kpc"] / x["Re_kpc"] < 5]
    T5[foot]["reported_3D"] = dict(P2=st3, n_rnb_lt_5Re=len(n3), ids=n3)
    P(f"  [{foot}] reported 3-D (KT distances): r_nb < 5 Re for {len(n3)} {n3}; P2 {st3['mean']:+.5f} (Z {st3['Z']:+.2f}, {st3['label']})")
    T5[foot]["dP2"] = st["mean"] - ref["mean"]
    T5[foot]["verdict"] = "UNCHANGED" if (len(nb5) == 0 and abs(st["mean"] - ref["mean"]) < 0.005) else "CHANGED"
    P(f"  [{foot}] P2 record {ref['mean']:+.5f} -> H-NB {st['mean']:+.5f} (d {st['mean'] - ref['mean']:+.5f}) -> T5 groups VERDICT: {T5[foot]['verdict']}")
    if MUTATE:
        check(f"M1 [{foot}] r_nb = inf: P2 = CFG543's exactly", abs(st["mean"] - ref["mean"]) < 1e-12, f"d {st['mean'] - ref['mean']:+.1e}")
RES["T5"] = T5

# X-COP bracket: equal-total-mass neighbour separation that puts r_nb at R500, and the clusters' mutual separations
XJ = json.load(open(os.path.join(DD, "xcop", "xcop_r500_ettori2019.json")))
pos = {}
for c in XJ:
    fl = sorted(glob.glob(os.path.join(DD, "xcop", c, "*.fits")))
    for f in fl:
        for hd in fits.open(f):
            if "RA" in hd.header and "DEC" in hd.header:
                pos[c] = (float(hd.header["RA"]), float(hd.header["DEC"])); break
        if c in pos:
            break
XC = {}
for foot in FOOTS:
    a0 = C.A0[foot]; rowsx = []
    for c, d in XJ.items():
        Mb = 0.149 * d["M500"] * 1e14                                        # CFG4 measured median f_bar 0.149 (bracket)
        R5 = d["R500"]
        lo, hi = R5, 60.0
        for _ in range(60):
            mid = 0.5 * (lo + hi)
            if float(N.r_pair(Mb, Mb, mid, G, a0)) > R5:
                hi = mid
            else:
                lo = mid
        rowsx.append(dict(name=c, z=d["z"], R500=R5, Dcrit_equal_mass_Mpc=0.5 * (lo + hi), has_pos=c in pos))
    pairs = []
    names = [c for c in XJ if c in pos]
    for i in range(len(names)):
        for j in range(i + 1, len(names)):
            a, b_ = names[i], names[j]
            dz = abs(XJ[a]["z"] - XJ[b_]["z"]) * 2.998e5
            if dz > 1500:
                continue
            zbar = 0.5 * (XJ[a]["z"] + XJ[b_]["z"])
            chi = 2.998e5 / 70.0 * zbar
            s = float(angsep(pos[a][0], pos[a][1], pos[b_][0], pos[b_][1])) * chi / (1 + zbar)
            pairs.append(dict(a=a, b=b_, dcz=dz, proj_Mpc=s))
    XC[foot] = dict(clusters=rowsx, close_pairs=pairs, label="BRACKET (no neighbour catalogue on disk)")
    P(f"  [{foot}] X-COP: D_crit (equal-mass neighbour puts r_nb at R500) {min(r['Dcrit_equal_mass_Mpc'] for r in rowsx):.2f}-"
      f"{max(r['Dcrit_equal_mass_Mpc'] for r in rowsx):.2f} Mpc; X-COP pairs within 1500 km/s: "
      + ("; ".join(f"{p['a']}-{p['b']} {p['proj_Mpc']:.1f} Mpc" for p in pairs) or "none"))
RES["XCOP"] = XC
RES["checks"] = CHK
RES["elapsed_s"] = round(time.time() - T0, 1)
nlb = sum(1 for c in CHK.values() if c["load_bearing"] and not c["ok"])
P(f"\n{sum(c['ok'] for c in CHK.values())}/{len(CHK)} checks pass; elapsed {RES['elapsed_s']} s")
json.dump(RES, open(os.path.join(HERE, f"cfg644_local_results{SUF}.json"), "w"), indent=1, default=float)
open(os.path.join(HERE, f"cfg644_local{SUF}.out"), "w").write("\n".join(LOG) + "\n")
sys.exit(1 if nlb else 0)
