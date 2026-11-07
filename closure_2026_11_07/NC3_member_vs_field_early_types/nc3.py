#!/usr/bin/env python3
"""NC3 (FROZEN_CRITERIA.md b5625a2299): cluster-member / group-central early types vs field early types at fixed M* x sigma.
python3 nc3.py            -> nc3.json / nc3.out
python3 nc3.py --mutate   -> nc3_MUTATE.json / nc3_MUTATE.out (M1 shuffled tags, M2 +0.10 dex injection)
QX22's MaNGA DynPop sample, accel() and cells reimplemented (KA1 checks QX22's D). One thread, seconds.
kappa = 1/2 FITTED; not theory closed."""
import json, math, os, sys, time, resource
for v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS"): os.environ[v] = "1"
import numpy as np
from astropy.io import fits
from astropy.coordinates import SkyCoord
import astropy.units as u

HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, "../.."))
MUT = "--mutate" in sys.argv; TAG = "nc3_MUTATE" if MUT else "nc3"; OUT = []
def P(s=""): print(s, flush=True); OUT.append(str(s))
G, MS, MPC, C = 6.6743e-11, 1.98892e30, 3.0857e22, 2.99792458e5; H0 = 70.0; NB = 2000
A0 = {"canonical": 9.3603e-11, "alt": 1.1312e-10}; LN10 = math.log(10)
nu = lambda y: 0.5 + np.sqrt(0.25 + 1 / y)

# ---------------- MaNGA DynPop, QX22 cuts verbatim
with fits.open(os.path.join(REPO, "_external_data/lam1_dynpop_2026_11_03/SDSSDR17_MaNGA_JAM_v2.fits")) as h:
    d = h[1].data
    lam, eps, sig, me, msr, z, q = (np.array(d[k], float) for k in ("Lambda_Re", "Eps_MGE", "Sigma_Re", "nsa_elpetro_mass", "nsa_sersic_mass", "z", "Qual"))
    AB = np.array(d["nsa_elpetro_absmag"], float); RA = np.array(d["obj_ra"], float); DE = np.array(d["obj_dec"], float)
    MT = np.array([np.array(h[i].data["log_Mt_rhalf"], float) for i in range(2, 12)])
    RH = np.array([np.array(h[i].data["rhalf_arcsec"], float) for i in range(2, 12)])
    X2 = np.array([np.array(h[i].data["chi2_dof"], float) for i in range(2, 12)])
nfin = np.sum(np.isfinite(MT) & np.isfinite(RH) & (RH > 0), axis=0)
sel = (q >= 1) & np.isfinite(me) & (me > 0) & np.isfinite(msr) & (z > 0.005) & np.isfinite(lam) & np.isfinite(eps) & (sig > 0) & (nfin >= 8)
lam, eps, sig, me, msr, z, AB, RA, DE = (x[sel] for x in (lam, eps, sig, me, msr, z, AB, RA, DE))
MT, RH, X2 = MT[:, sel], RH[:, sel], X2[:, sel]; n = len(z)
ur = AB[:, 2] - AB[:, 4]; red = np.isfinite(ur) & (ur >= 2.5); slow = (lam < 0.08 + eps / 4) & (eps < 0.4)
DA = C * z / H0 / (1 + z) * MPC
X2v = np.where(np.isfinite(X2) & np.isfinite(MT) & np.isfinite(RH) & (RH > 0), X2, np.inf)
order = np.argsort(X2v, axis=0, kind="stable"); jj = np.arange(n)
mtm, rhm = MT[order[0], jj], RH[order[0], jj]; mt2, rh2 = MT[order[1], jj], RH[order[1], jj]
cell = np.floor(me / 0.2).astype(int) * 1000 + np.floor(np.log10(sig) / 0.1).astype(int)
cellM = np.floor(me / 0.2).astype(int)
def accel(mt, rh, ms):
    r = rh * math.pi / 648000 * DA; return G * 10 ** mt * MS / r ** 2, G * 0.5 * 10 ** ms * MS / r ** 2
def resid(go, gb, a0): return np.log(go) - np.log(nu(gb / a0) * gb)
def Dstat(r, grp, cl, idx=None):
    """QX22's cell statistic: sum_c w_c [median(r[grp]) - median(r[~grp])] / sum w_c, w_c = min(n1, n2), cells with >= 2 each."""
    if idx is not None: r, grp, cl = r[idx], grp[idx], cl[idx]
    o = np.argsort(cl, kind="stable"); r, grp, cl = r[o], grp[o], cl[o]; _, st = np.unique(cl, return_index=True); en = np.r_[st[1:], len(cl)]
    num = den = 0.0; nc = 0
    for a, b in zip(st, en):
        s = grp[a:b]; n1 = int(s.sum()); n2 = (b - a) - n1
        if n1 >= 2 and n2 >= 2:
            w = min(n1, n2); rr = r[a:b]; num += w * (np.median(rr[s]) - np.median(rr[~s])); den += w; nc += 1
    return (num / den if den else float("nan")), nc

# ---------------- T15 (Tully 2015 2MASS groups), table5 galaxies
def t15():
    L = [l.rstrip("\n").split("\t") for l in open(os.path.join(REPO, "campaign_fresh_gravity/_external_data/cfg393/t15_table5.tsv"))
         if l.strip() and not l.startswith("#")]
    hdr = [x.strip() for x in L[0]]; c = {k: i for i, k in enumerate(hdr)}
    def col(k):
        o = np.full(len(L) - 3, np.nan)
        for i, r in enumerate(L[3:]):
            try: o[i] = float(r[c[k]])
            except (ValueError, IndexError): pass
        return o
    T = {k: col(k) for k in ("_RA.icrs", "_DE.icrs", "HV", "Nmb", "Mlum", "PGC", "PGC1", "MType", "Vcmba")}
    g = np.isfinite(T["_RA.icrs"]) & np.isfinite(T["_DE.icrs"]); return {k: v[g] for k, v in T.items()}
T = t15(); TC = SkyCoord(T["_RA.icrs"] * u.deg, T["_DE.icrs"] * u.deg)
def tag(ra, de, cz, dv=300.0, rad=10.0):
    i, s, _ = SkyCoord(np.atleast_1d(ra) * u.deg, np.atleast_1d(de) * u.deg).match_to_catalog_sky(TC)
    ok = s.arcsec < rad
    if cz is not None: ok = ok & (np.abs(np.atleast_1d(cz) - T["HV"][i]) < dv)
    nm, ml, cen = T["Nmb"][i], T["Mlum"][i], T["PGC"][i] == T["PGC1"][i]
    clu = ok & (ml >= 100) & (nm >= 5); gcen = ok & cen & (ml >= 10) & (ml < 100) & (nm >= 3)
    gsat = ok & ~cen & (ml >= 10) & (ml < 100) & (nm >= 3); fld = ok & (nm == 1)
    return dict(ok=ok, IN=clu | gcen, cluster=clu, gcen=gcen, gsat=gsat, FIELD=fld, mtype=T["MType"][i], mlum=ml, cen=cen, vcmb=T["Vcmba"][i])

TG = tag(RA, DE, C * z)
early = TG["ok"] & np.isfinite(TG["mtype"]) & (TG["mtype"] <= -1)
P(f"NC3 {TAG}: MaNGA after QX22 cuts {n}; T15-matched {int(TG['ok'].sum())}; early types (MType <= -1) {int(early.sum())}")
for k in ("IN", "cluster", "gcen", "gsat", "FIELD"):
    P(f"   early & {k}: {int((early & TG[k]).sum())}   red & {k}: {int((red & TG['ok'] & TG[k]).sum())}")

# ---------------- stripping budget (frozen), IN galaxies
def stripping(mask):
    rows = []; rh_kpc = rhm * math.pi / 648000 * DA / (MPC / 1e3)
    for j in np.where(mask)[0]:
        if TG["cen"][j]: rows.append(dict(central=True, proof01=True, proof05=True)); continue
        m = 10 * 10 ** me[j]; out = dict(central=False)
        for rp, key in ((0.1, "proof01"), (0.5, "proof05")):
            Mh = TG["mlum"][j] * 1e12 * rp; rt = rp * 1e3 * (m / (3 * Mh)) ** (1 / 3); out[key] = bool(rt >= 2 * rh_kpc[j]); out[f"rt_kpc_{rp}"] = rt
        out["r_half_kpc"] = float(rh_kpc[j]); rows.append(out)
    f01 = float(np.mean([r["proof01"] for r in rows])) if rows else float("nan"); f05 = float(np.mean([r["proof05"] for r in rows])) if rows else float("nan")
    sat = [r for r in rows if not r["central"]]
    return dict(n=len(rows), n_central=len(rows) - len(sat), frac_proof_rp01=f01, frac_proof_rp05=f05,
                median_rt_over_rh_rp01=float(np.median([r["rt_kpc_0.1"] / r["r_half_kpc"] for r in sat])) if sat else None)

# ---------------- grading
def grade(a0, base, grpIN, cl, inject=0.0, shuffle_seed=None, mass=me, imf=False):
    go, gb = accel(mtm, rhm, mass + (np.log10(np.array([fK(s) for s in sig])) if imf else 0.0))
    ok = base & np.isfinite(go) & np.isfinite(gb) & (go > 0) & (gb > 0)
    r = np.full(n, np.nan); r[ok] = resid(go[ok], gb[ok], a0) / LN10 + inject * grpIN[ok]
    g = grpIN.copy()
    if shuffle_seed is not None:
        rng0 = np.random.default_rng(shuffle_seed); g = g.copy()
        for c_ in np.unique(cl[ok]): i = np.where(ok & (cl == c_))[0]; g[i] = rng0.permutation(g[i])
    rr, gg, cc = r[ok], g[ok], cl[ok]
    D, nc = Dstat(rr, gg, cc)
    rng = np.random.default_rng(20261107)
    bs = np.array([Dstat(rr, gg, cc, rng.integers(0, len(rr), len(rr)))[0] for _ in range(NB)])
    st = float(np.nanstd(bs)); lo, hi = (float(x) for x in np.nanpercentile(bs, [2.5, 97.5]))
    return dict(D=float(D), cells=nc, n_IN=int(gg.sum()), n_FIELD=int((~gg).sum()), sigma_boot=st, ci_boot=[lo, hi], _r=r, _ok=ok)

def full(a0, base, grpIN, cl=cell, **kw):
    R = grade(a0, base, grpIN, cl, **kw)
    go2, gb2 = accel(mt2, rh2, me); go3, gb3 = accel(mtm, rhm, msr)
    def Dalt(go_, gb_):
        ok = base & np.isfinite(go_) & np.isfinite(gb_) & (go_ > 0) & (gb_ > 0)
        rr = resid(go_[ok], gb_[ok], a0) / LN10 + kw.get("inject", 0.0) * grpIN[ok]; return Dstat(rr, grpIN[ok], cl[ok])[0]
    smod = abs(R["D"] - Dalt(go2, gb2)); smass = abs(R["D"] - Dalt(go3, gb3))
    sD = math.sqrt(R["sigma_boot"] ** 2 + smod ** 2 + smass ** 2); lo, hi = R["D"] - 1.96 * sD, R["D"] + 1.96 * sD
    R.update(sigma_model=smod, sigma_mass=smass, sigma_D=sD, ci95=[lo, hi], halfwidth=1.96 * sD)
    if 1.96 * sD > 0.10 or R["cells"] < 5: lab = "NO POWER"
    elif R["D"] > 0 and lo > 0 and R["D"] >= 0.05: lab = "R5 SIGNAL"
    elif lo >= -0.05 and hi <= 0.05: lab = "NO DIFFERENCE"
    else: lab = "UNRESOLVED"
    R["label"] = lab; return R

A_SL, A_IC, K_TO_S = 0.38, -0.06, 1 / 0.63          # Posacki+2015 as QX26 (reported reading only)
def fK(se): return max(10 ** (A_SL * math.log10(se / 200.0) + A_IC) * K_TO_S, 1.0)
def pub(R): return {k: v for k, v in R.items() if not k.startswith("_")}

RES = dict(lane="NC3", criteria="b5625a2299", mutate=MUT, note="kappa = 1/2 FITTED; not theory closed", foot={})
t0 = time.time()
okfin = np.isfinite(mtm) & np.isfinite(rhm)
baseP = early & (TG["IN"] | TG["FIELD"]) & okfin
STRIP = stripping(baseP & TG["IN"]); RES["stripping"] = STRIP
P(f"Stripping budget (IN early types, n {STRIP['n']}, {STRIP['n_central']} centrals unstripped): stripping-proof at r_half "
  f"(r_t >= 2 r_half) {STRIP['frac_proof_rp01']:.2f} at r_p 0.1 Mpc, {STRIP['frac_proof_rp05']:.2f} at 0.5 Mpc; median r_t/r_half (satellites, 0.1 Mpc) {STRIP['median_rt_over_rh_rp01']}")
for foot, a0 in A0.items():
    F = {}
    # KA1: QX22's D (red, low-lambda < 0.2 minus high-lambda > 0.5)
    go, gb = accel(mtm, rhm, me); okq = np.isfinite(go) & np.isfinite(gb) & (go > 0) & (gb > 0)
    A_, B_ = lam < 0.2, lam > 0.5; bq = okq & red & (A_ | B_)
    Dq = Dstat(resid(go[bq], gb[bq], a0), A_[bq], cell[bq])[0]
    q22 = json.load(open(os.path.join(REPO, "closure_2026_11_06/QX22_support_key/iter_1/qx22.json")))["foot"][foot]["D"]
    F["KA1"] = dict(D=Dq, qx22=q22, pass_=bool(abs(Dq - q22) <= 1e-6))
    P(f"\n[{foot}] KA1 QX22 D {Dq:+.6f} vs {q22:+.6f} -> {'PASS' if F['KA1']['pass_'] else 'FAIL'}")
    if not MUT:
        R = full(a0, baseP, TG["IN"]); F["primary"] = pub(R)
        P(f"[{foot}] PRIMARY early types: IN {R['n_IN']} vs FIELD {R['n_FIELD']}, cells {R['cells']}: D = {R['D']:+.4f} dex "
          f"(boot {R['sigma_boot']:.4f}, model {R['sigma_model']:.4f}, M* {R['sigma_mass']:.4f}; sigma_D {R['sigma_D']:.4f}); 95% [{R['ci95'][0]:+.4f}, {R['ci95'][1]:+.4f}] -> {R['label']}")
        r_, ok_ = R["_r"], R["_ok"]
        F["medians"] = dict(IN=float(np.median(r_[ok_ & TG["IN"]])), FIELD=float(np.median(r_[ok_ & TG["FIELD"]])))
        P(f"[{foot}]   raw medians (no matching): IN {F['medians']['IN']:+.4f}, FIELD {F['medians']['FIELD']:+.4f} dex")
        rep = {}
        for nm, base, grp, cl, kw in (
                ("cluster members only vs FIELD", early & (TG["cluster"] | TG["FIELD"]) & okfin, TG["cluster"], cell, {}),
                ("group centrals only vs FIELD", early & (TG["gcen"] | TG["FIELD"]) & okfin, TG["gcen"], cell, {}),
                ("group satellites vs FIELD", early & (TG["gsat"] | TG["FIELD"]) & okfin, TG["gsat"], cell, {}),
                ("FIELD cz < 6000", early & (TG["IN"] | (TG["FIELD"] & (C * z < 6000))) & okfin, TG["IN"], cell, {}),
                ("red u-r >= 2.5 instead of MType", red & TG["ok"] & (TG["IN"] | TG["FIELD"]) & okfin, TG["IN"], cell, {}),
                ("Posacki IMF per galaxy, M*-only cells", baseP, TG["IN"], cellM, dict(imf=True)),
                ("M*-only cells, no IMF", baseP, TG["IN"], cellM, {})):
            Rr = full(a0, base, grp, cl, **kw); rep[nm] = pub(Rr)
            P(f"[{foot}]   reported {nm}: n {Rr['n_IN']}/{Rr['n_FIELD']}, cells {Rr['cells']}, D {Rr['D']:+.4f} [{Rr['ci95'][0]:+.4f}, {Rr['ci95'][1]:+.4f}] -> {Rr['label']}")
        F["reported"] = rep
    else:
        # M1: 200 shuffles (point estimates), first shuffle with full CI
        shuf = []
        for k in range(200):
            go_, gb_ = accel(mtm, rhm, me); ok_ = baseP & np.isfinite(go_) & np.isfinite(gb_) & (go_ > 0) & (gb_ > 0)
            rr = resid(go_[ok_], gb_[ok_], a0) / LN10; g = TG["IN"][ok_].copy(); cl = cell[ok_]; rng0 = np.random.default_rng(20261108 + k)
            for c_ in np.unique(cl): i = np.where(cl == c_)[0]; g[i] = rng0.permutation(g[i])
            shuf.append(Dstat(rr, g, cl)[0])
        # first shuffle with its full CI (shuffled grouping used for the bootstrap and the model/mass terms)
        go_, gb_ = accel(mtm, rhm, me); ok_ = baseP & np.isfinite(go_) & np.isfinite(gb_) & (go_ > 0) & (gb_ > 0)
        gsh = TG["IN"].copy(); rng0 = np.random.default_rng(20261108)
        for c_ in np.unique(cell[ok_]): i = np.where(ok_ & (cell == c_))[0]; gsh[i] = rng0.permutation(gsh[i])
        R1s = full(a0, baseP, gsh)
        m1 = dict(mean_D_200=float(np.nanmean(shuf)), sd_D_200=float(np.nanstd(shuf)), first=pub(R1s),
                  pass_=bool(abs(np.nanmean(shuf)) <= 0.01 and R1s["ci95"][0] <= 0 <= R1s["ci95"][1]))
        F["M1"] = m1
        P(f"[{foot}] M1 shuffled tags: mean D over 200 {m1['mean_D_200']:+.4f} (sd {m1['sd_D_200']:.4f}); first shuffle D {R1s['D']:+.4f} "
          f"[{R1s['ci95'][0]:+.4f}, {R1s['ci95'][1]:+.4f}] -> {'PASS' if m1['pass_'] else 'FAIL'}")
        R2 = full(a0, baseP, TG["IN"], inject=0.10); F["M2"] = dict(**pub(R2), pass_=R2["label"] == "R5 SIGNAL")
        P(f"[{foot}] M2 +0.10 dex injected on IN: D {R2['D']:+.4f} [{R2['ci95'][0]:+.4f}, {R2['ci95'][1]:+.4f}] -> {R2['label']} -> {'PASS' if F['M2']['pass_'] else 'FAIL'}")
    RES["foot"][foot] = F

if not MUT:
    # ---------------- two added reads
    kx = json.load(open(os.path.join(REPO, "closure_2026_11_07/KX1_kids_joint_budget/kx1.json")))
    RES["kids_read"] = kx["M2"]; P(f"\nKiDS isolated lenses (KX1 M2, law with joint budget): {json.dumps(kx['M2'])[:400]}")
    q33 = json.load(open(os.path.join(REPO, "closure_2026_11_06/QX33_clash_lookback_shape/qx33.json")))["footings"]
    RES["clash_read"] = {f: dict(all_radii=dict(HIGH=q33[f]["Q1_HIGH"], LOW=q33[f]["Q1_LOW_reported"]),
                                 past_BCG=dict(HIGH=q33[f]["drop_r_lt_50kpc"]["Q1_HIGH"], LOW=q33[f]["drop_r_lt_50kpc"]["Q1_LOW"])) for f in q33}
    for f, v in RES["clash_read"].items():
        P(f"CLASH s [{f}] past the BCG (r > 50 kpc): HIGH {v['past_BCG']['HIGH']['median']:+.3f} {v['past_BCG']['HIGH']['ci']}, LOW {v['past_BCG']['LOW']['median']:+.3f} {v['past_BCG']['LOW']['ci']}; "
          f"all radii HIGH {v['all_radii']['HIGH']['median']:+.3f}, LOW {v['all_radii']['LOW']['median']:+.3f}")
    # ---------------- SLUGGS and X-ray 7, tagged by T15 (reported)
    def vz(fn):
        L = [l.rstrip("\n").split("\t") for l in open(os.path.join(REPO, "real_research/data", fn), encoding="latin-1") if l.strip() and not l.startswith("#")]
        h_ = [x.strip() for x in L[0]]; return [dict(zip(h_, [x.strip() for x in r])) for r in L[3:]]
    S = {}
    for r in vz("sluggs_forbes2017_galaxies.tsv"):
        try: S[int(r["NGC"])] = (float(r["RAJ2000"]), float(r["DEJ2000"]))
        except (ValueError, KeyError): pass
    c330 = json.load(open(os.path.join(REPO, "campaign_fresh_gravity/CFG330_sluggs_icgc_clip/cfg330_icgc_K0_results.json")))["per_galaxy"]
    sl = {}
    for f in A0:
        pg = c330[f"nu_mono|{f}"]; rows = {}
        for k, v in pg.items():
            ng = int(k)
            if ng not in S: continue
            t = tag(S[ng][0], S[ng][1], None, rad=60.0)
            cls = "IN" if t["IN"][0] else ("FIELD" if t["FIELD"][0] else ("group sat" if t["gsat"][0] else ("unmatched" if not t["ok"][0] else "other")))
            rows[f"NGC{ng}"] = dict(off=v["off"], cls=cls, Mlum_1e12=float(t["mlum"][0]) if t["ok"][0] else None, central=bool(t["cen"][0]))
        med = {c_: float(np.median([x["off"] for x in rows.values() if x["cls"] == c_])) for c_ in {x["cls"] for x in rows.values()}}
        cnt = {c_: sum(1 for x in rows.values() if x["cls"] == c_) for c_ in med}
        sl[f] = dict(rows=rows, median=med, count=cnt); P(f"SLUGGS [{f}] (CFG330 K0 outer offsets, dex): medians {med}, counts {cnt}")
    RES["sluggs"] = sl
    q24 = json.load(open(os.path.join(REPO, "closure_2026_11_06/QX24_environment_key/iter_1/qx24.json")))
    xr = {}
    for f in A0:
        per = q24["foot"][f]["T2"]["per"]; rows = {}
        for nm, (ra, de, _) in q24["ell_positions"].items():
            t = tag(ra, de, None, rad=60.0)
            cls = "IN" if t["IN"][0] else ("FIELD" if t["FIELD"][0] else ("group sat" if t["gsat"][0] else ("unmatched" if not t["ok"][0] else "other")))
            rows[nm] = dict(off=per[nm]["offset"], cls=cls, Mlum_1e12=float(t["mlum"][0]) if t["ok"][0] else None, Nmb_central=bool(t["cen"][0]))
        xr[f] = rows; P(f"X-ray ellipticals [{f}] (QX24 T2 raw offsets): " + "; ".join(f"{k} {v['off']:+.2f} {v['cls']}" for k, v in rows.items()))
    RES["xray7"] = xr
    # ---------------- labels
    labs = {f: RES["foot"][f]["primary"]["label"] for f in A0}
    ka = all(RES["foot"][f]["KA1"]["pass_"] for f in A0)
    if labs["canonical"] == labs["alt"] == "NO DIFFERENCE" and STRIP["frac_proof_rp01"] >= 0.5: k4 = "K4 FIRES (no member residue at r_half; stripping cannot remove it there)"
    elif labs["canonical"] == labs["alt"] == "R5 SIGNAL": k4 = "R5 SUPPORTED at galaxy scale"
    else: k4 = "K4 NOT DECIDED"
    RES.update(labels=labs, KA_all=ka, K4_reading=k4)
    P(f"\nLABELS (before MUTATE gates): canonical {labs['canonical']}, alt {labs['alt']}; KA1 {'PASS' if ka else 'FAIL'}; {k4}")
RES["seconds"] = time.time() - t0; RES["peak_rss_GB"] = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1e9
P(f"runtime {RES['seconds']:.0f} s, peak RSS {RES['peak_rss_GB']:.2f} GB")
json.dump(RES, open(os.path.join(HERE, TAG + ".json"), "w"), indent=1, default=lambda o: o.tolist() if hasattr(o, "tolist") else str(o))
open(os.path.join(HERE, TAG + ".out"), "w").write("\n".join(OUT) + "\n")
