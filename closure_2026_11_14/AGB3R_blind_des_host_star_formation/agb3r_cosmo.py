"""AGB3R Parts S, J, E and check KS (blind re-grade of AGB3; rules: AGB3's FROZEN_CRITERIA.md, my READING.md).

AGB1's fitter (agb1_run.py, agb1_template.py) and AGB2's joint arithmetic (agb2_joint.joint) are imported unchanged.

Usage: python3 -I agb3r_cosmo.py MODE
  KS                      harness: A = 0 forks and AGB1's T_S at coefficient 1, `full` and `des_only`
  S_full S_des S_mass     T_H profiles (f, t, n on the Part J grids) and forks A_H = 0, 1, free
  S_zf2 S_zf5 S_host      the same for z_f 2, z_f 5 and the host-by-host correction
  E                       Part E: young, blue, log s >= -10, old, young DES (BAO + supernovae); young without BAO
  J                       Part J from the S_* outputs and agb3r_D.json
Each mode writes agb3r_<MODE>.json and prints its log.
"""
import json, os, sys, time, warnings
for _v in ("VECLIB_MAXIMUM_THREADS", "OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS"):
    os.environ.setdefault(_v, "2")
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
warnings.filterwarnings("ignore", category=RuntimeWarning)
import numpy as np

MODE = sys.argv[1] if len(sys.argv) > 1 else "KS"
AGB1 = os.path.normpath(os.path.join(HERE, "..", "..", "closure_2026_11_13", "AGB1_progenitor_age_bias"))
AGB2 = os.path.normpath(os.path.join(HERE, "..", "AGB2_host_mass_step_redshift"))
_argv = sys.argv; sys.argv = ["agb1_run.py", "AGB3R"]; sys.path.insert(0, AGB1)
import agb1_run as R1, agb1_template as TPL
sys.argv = ["agb2_joint.py", "AGB3R"]; sys.path.insert(0, AGB2)
from agb2_joint import joint
sys.argv = _argv
import agb3r_data as DA
import agb3r_model as M

SLOPE = 0.030
GRID_F = [round(x, 2) + 0.0 for x in np.arange(-1.0, 2.0 + 1e-9, 0.1)]
GRID_N = [round(x, 2) + 0.0 for x in np.arange(-1.0, 2.0 + 1e-9, 0.25)]
log = lambda m: print(m, flush=True)


# ---------------- words ----------------
def w2(q0, dt):
    if q0 < 0 and dt >= 4: return "ACCELERATING TODAY"
    if q0 > 0 and dt >= 4: return "DECELERATING TODAY"
    return "SIGN NOT SETTLED"


def w3(dn):
    if dn >= 9: return "NEVER-ACCELERATED EXCLUDED AT 3 SIGMA"
    if dn >= 4: return "NEVER-ACCELERATED DISFAVOURED"
    return "NEVER-ACCELERATED ALLOWED"


# ---------------- templates ----------------
def host_ages(meta, idx, kind, zf):
    z = meta.zHD[idx]
    return M.mean_age(meta.ls[idx], z, zf) if kind == "sfr" else M.mass_age(meta.lm[idx], z)


def th_curve(meta, sample, kind="sfr", zf=3.0):
    """T_H(z) from the means of the hosts' ages in the 20 equal-count zHD bins of the sample."""
    idx = np.where(meta.sample(sample))[0]; z = meta.zHD[idx]; age = host_ages(meta, idx, kind, zf)
    b = DA.bins(z, 20)
    zb = np.array([z[b == k].mean() for k in range(20)]); ab = np.array([age[b == k].mean() for k in range(20)])
    T = lambda zz: SLOPE*(ab[0] - np.interp(zz, zb, ab))
    return T, zb, ab


# ---------------- supernova subsets (as AGB1's SN builds a sub-sample) ----------------
_FULL = None


def sn_subset(mask, name):
    """AGB1's SN object for the distance-file rows in `mask`: inverse covariance inverted, sub-block taken, inverted."""
    global _FULL
    if _FULL is None: _FULL = R1.SN("full")
    s = object.__new__(R1.SN); W = _FULL.W
    s.W = W if mask.all() else np.linalg.inv(np.linalg.inv(W)[np.ix_(mask, mask)])
    s.ids, s.z, s.zh, s.mu = _FULL.ids[mask], _FULL.z[mask], _FULL.zh[mask], _FULL.mu[mask]
    s.n = int(mask.sum()); s.n_des = int((s.ids == 10).sum()); s.sample = name
    s.W1 = s.W@np.ones(s.n); s.s11 = float(s.W1.sum()); s.T = {}
    return s


def hd_meta():
    meta = DA.Meta(); hd = DA.read_hd(); j = DA.hd_index(meta, hd)
    sn = R1.SN("full")
    if not (np.allclose(sn.z, hd["zHD"], 0, 1e-9) and np.allclose(sn.mu, hd["MU"], 0, 1e-9)):
        raise SystemExit("distance file order differs from AGB1's loader")
    return meta, hd, j


def slim(d):
    keep = ("chi2", "chi2_bao", "chi2_sn", "Om", "w0", "wa", "q0", "qmin", "z_qmin", "hrd", "coef", "edge", "x3", "con")
    return {k: d[k] for k in keep if k in d}


# ---------------- fits ----------------
def forks(F, tname, base_fits, log, names=("A0", "A1", "Afree")):
    """AGB1 run_block's forks: base, q0 = 0 (started also from the base), never (also from the q0 = 0 fit and the base)."""
    out = {}
    for name in names:
        if name == "Afree": fixed, fr = {}, [tname]
        else: fixed, fr = {tname: 0.0 if name == "A0" else 1.0}, []
        base = base_fits[name]
        today = F.fit(fixed, fr, "today", extra=(base,))
        never = F.fit(fixed, fr, "never", extra=(today, base))
        for c in (today, never):
            if c["chi2"] < base["chi2"] - 1e-7:
                base = min([base, F.fit(fixed, fr, "free", extra=(c,))], key=lambda r: r["chi2"])
        out[name] = dict(base=slim(base), today=slim(today), never=slim(never), D_today=today["chi2"] - base["chi2"],
                         D_never=never["chi2"] - base["chi2"])
        A = base["coef"].get(tname, 0.0)
        log(f"  fork {name}: A {A:+.4f} chi2 {base['chi2']:.4f} Om {base['Om']:.4f} w0 {base['w0']:+.4f} wa {base['wa']:+.4f}"
            f" q0 {base['q0']:+.4f} (min q {base['qmin']:+.4f} at z {base['z_qmin']:.2f}) edge {base['edge']} | q0 = 0: dchi2 {out[name]['D_today']:.3f}"
            f" | never: dchi2 {out[name]['D_never']:.3f} (Om {never['Om']:.4f} w0 {never['w0']:+.4f} wa {never['wa']:+.4f} min q {never['qmin']:+.5f})"
            f"  -> {w2(base['q0'], out[name]['D_today'])}; {w3(out[name]['D_never'])}")
    return out


def profile_block(F, tname, log):
    """f, t on GRID_F and n on GRID_N (warm starts as agb2_joint's main), A free, and forks A0, A1, Afree."""
    free = F.fit({}, [tname])
    log(f"  A free: A {free['coef'][tname]:+.4f} chi2 {free['chi2']:.4f} Om {free['Om']:.4f} w0 {free['w0']:+.4f} wa {free['wa']:+.4f} q0 {free['q0']:+.4f}")
    prof, prev = {}, free
    for a in GRID_F:
        r = F.fit({tname: a}, [], extra=(prev, free)); prof[a] = r; prev = r
    low = min(prof.values(), key=lambda r: r["chi2"])
    if low["chi2"] < free["chi2"] - 1e-7:
        free = min([free, F.fit({}, [tname], extra=(low,))], key=lambda r: r["chi2"])
        log(f"  A free re-fitted from the grid minimum: A {free['coef'][tname]:+.4f} chi2 {free['chi2']:.4f}")
    t, tfit, prev = {}, {}, None
    for a in GRID_F:
        r = F.fit({tname: a}, [], "today", extra=(prof[a], prev)); prev = r; tfit[a] = r
        if r["chi2"] < prof[a]["chi2"] - 1e-7:
            b = F.fit({tname: a}, [], "free", extra=(r, prof[a]))
            if b["chi2"] < prof[a]["chi2"]:
                log(f"  A {a:+.2f}: free fit improved by {prof[a]['chi2'] - b['chi2']:.2e} from the q0 = 0 point"); prof[a] = b
        t[a] = r["chi2"]
    n, prev = {}, None
    for a in GRID_N:
        g = min(GRID_F, key=lambda x: abs(x - a))
        r = F.fit({tname: a}, [], "never", extra=(tfit[g], prof[g], prev)); prev = r; n[a] = r
    for a in GRID_F:
        nn = f"  never {n[a]['chi2']:10.4f} (+{n[a]['chi2'] - prof[a]['chi2']:.3f}) min q {n[a]['qmin']:+.5f}" if a in n else ""
        log(f"  A {a:+.2f}  f {prof[a]['chi2']:10.4f} Om {prof[a]['Om']:.4f} w0 {prof[a]['w0']:+.4f} wa {prof[a]['wa']:+.4f} q0 {prof[a]['q0']:+.4f}"
            f" edge {prof[a]['edge']} | q0 = 0: {t[a]:10.4f} (+{t[a] - prof[a]['chi2']:.3f}){nn}")
    base = {"A0": prof[0.0], "A1": prof[1.0], "Afree": free}
    fk = forks(F, tname, base, log)
    # the lower of the fork fit and the profile fit, for each constrained point at A = 0 and 1
    best = {}
    for nm, a in (("A0", 0.0), ("A1", 1.0)):
        b = min(fk[nm]["base"]["chi2"], prof[a]["chi2"]); td = min(fk[nm]["today"]["chi2"], t[a]); nv = min(fk[nm]["never"]["chi2"], n[a]["chi2"])
        q0 = fk[nm]["base"]["q0"] if fk[nm]["base"]["chi2"] <= prof[a]["chi2"] else prof[a]["q0"]
        best[nm] = dict(q0=q0, D_today=td - b, D_never=nv - b,
                        diff_vs_fork=dict(base=prof[a]["chi2"] - fk[nm]["base"]["chi2"], today=t[a] - fk[nm]["today"]["chi2"],
                                          never=n[a]["chi2"] - fk[nm]["never"]["chi2"]))
        log(f"  {nm} best of fork and profile: q0 {q0:+.4f} dchi2_today {best[nm]['D_today']:.3f} dchi2_never {best[nm]['D_never']:.3f}"
            f" (profile minus fork: base {best[nm]['diff_vs_fork']['base']:+.1e}, today {best[nm]['diff_vs_fork']['today']:+.1e},"
            f" never {best[nm]['diff_vs_fork']['never']:+.1e}) -> {w2(q0, best[nm]['D_today'])}; {w3(best[nm]['D_never'])}")
    fmin = free["chi2"]
    S = dict(A_free=free["coef"][tname], chi2_free=fmin, q0_free=free["q0"], D_A0=prof[0.0]["chi2"] - fmin, D_A1=prof[1.0]["chi2"] - fmin)
    log(f"  A_H free {S['A_free']:+.4f}: dchi2(A_H = 0) {S['D_A0']:.3f}  dchi2(A_H = 1) {S['D_A1']:.3f}")
    return dict(free=slim(free), summary=S, grid_f=GRID_F, grid_n=GRID_N, f=[prof[a]["chi2"] for a in GRID_F],
                q0=[prof[a]["q0"] for a in GRID_F], t=[t[a] for a in GRID_F], n=[n[a]["chi2"] for a in GRID_N],
                n_qmin=[n[a]["qmin"] for a in GRID_N], profile={f"{a:+.2f}": slim(prof[a]) for a in GRID_F}, forks=fk, best=best)


# ---------------- modes ----------------
def mode_KS(res):
    bao = R1.BAO("all"); out = {}; allok = True
    for sample in ("full", "des_only"):
        A1j = json.load(open(os.path.join(AGB1, f"agb1_A_{sample}.json")))["forks"]
        sn = R1.SN(sample); sn.add_template("TS", TPL.T(sn.z, "S")); F = R1.Fitter("A", sn, bao)
        log(f"KS {sample}: {sn.n} supernovae")
        b0 = F.fit({"TS": 0.0}, []); b1 = F.fit({"TS": 1.0}, [], extra=(b0,))
        fk = forks(F, "TS", {"A0": b0, "A1": b1}, log, names=("A0", "A1"))
        rows = {}
        for nm in ("A0", "A1"):
            for k in ("D_today", "D_never"):
                mine, ref = fk[nm][k], A1j[nm][k]; ok = abs(mine - ref) <= 0.01; allok &= ok
                rows[f"{nm}_{k}"] = dict(mine=mine, agb1=ref, passed=bool(ok))
                log(f"  KS {sample} {nm} {k}: {mine:.4f} vs AGB1 {ref:.4f} (|diff| {abs(mine - ref):.4f} <= 0.01) -> {'PASS' if ok else 'FAIL'}")
        out[sample] = dict(rows=rows, forks=fk)
    res["KS"] = dict(samples=out, passed=bool(allok))
    log(f"KS -> {'PASS' if allok else 'FAIL'}")


def mode_S(res, cfg):
    meta, hd, j = hd_meta(); bao = R1.BAO("all")
    sample = "des_only" if cfg == "des" else "full"
    kind = "mass" if cfg == "mass" else "sfr"; zf = {"zf2": 2.0, "zf5": 5.0}.get(cfg, 3.0)
    sn = R1.SN(sample); mask = (hd["ids"] == 10) if sample == "des_only" else np.ones(len(hd["ids"]), bool)
    T, zb, ab = th_curve(meta, sample, kind, zf)
    if cfg == "host":
        jj = j[mask]; age = host_ages(meta, jj, "sfr", 3.0)
        vec = SLOPE*(ab[0] - age)
        sn.add_template("TH", vec)
        res["host_vector"] = dict(mean=float(vec.mean()), sd=float(vec.std()))
        log(f"S_{cfg}: host-by-host correction 0.030 x (a_1 - age_i): mean {vec.mean():+.4f} mag, sd {vec.std():.4f}")
    else:
        sn.add_template("TH", T(sn.z))
    zs = [0.03, 0.05, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
    th = [float(T(z)) for z in zs]
    zg = np.linspace(0, 1.2, 241)
    res.update(sample=sample, kind=kind, zf=zf, n_sn=sn.n, bin_z=zb.tolist(), bin_age=ab.tolist(), T_H=dict(z=zs, mag=th),
               T_H_max=float(T(zg).max()), mean_age_at=dict(z=[0.03, 0.1, 0.2, 0.3, 0.5, 0.7, 1.0],
                                                           age=[float(np.interp(z, zb, ab)) for z in (0.03, 0.1, 0.2, 0.3, 0.5, 0.7, 1.0)]))
    log(f"S_{cfg}: sample {sample} ({sn.n} supernovae), host ages {kind}, z_f {zf}")
    log("  T_H at z " + " ".join(f"{z:5.2f}" for z in zs))
    log("  T_H mag  " + " ".join(f"{v:5.3f}" for v in th) + f"   (max over 0-1.2: {res['T_H_max']:.3f})")
    log("  bin mean age at z 0.03 0.1 0.2 0.3 0.5 0.7 1.0: " + " ".join(f"{v:.2f}" for v in res["mean_age_at"]["age"]))
    F = R1.Fitter("A", sn, bao)
    res.update(profile_block(F, "TH", log))


def mode_E(res):
    meta, hd, j = hd_meta(); bao = R1.BAO("all"); out = {}
    for name in ("young", "blue", "ls10", "old", "young_des", "full"):
        mask = meta.sample(name)[j]
        for with_bao in ((True, False) if name in ("young", "full") else (True,)):
            sn = sn_subset(mask, name); F = R1.Fitter("A", sn, bao if with_bao else None)
            key = name + ("" if with_bao else "_noBAO")
            log(f"E {key}: {sn.n} supernovae ({sn.n_des} DES){'' if with_bao else ', no BAO'}")
            base = F.fit({}, [])
            fk = forks(F, "none", {"A0": base}, log, names=("A0",))["A0"]
            fk["word_today"] = w2(fk["base"]["q0"], fk["D_today"]); fk["word_ever"] = w3(fk["D_never"]); fk["n_sn"] = sn.n; fk["n_des"] = sn.n_des
            out[key] = fk
    res["E"] = out


def mode_J(res):
    D = json.load(open(os.path.join(HERE, "agb3r_D.json")))
    d2 = D["D2"]["primary"]; d2p = D["D2"]["P"]; u = D["U"]["primary"]
    S = {k: json.load(open(os.path.join(HERE, f"agb3r_S_{k}.json"))) for k in ("full", "des", "mass")}
    cfgs = [("primary", "full", d2["A"], d2["sd_A"]), ("des_only", "des", d2["A"], d2["sd_A"]),
            ("D2_P", "full", d2p["A"], d2p["sd_A"]), ("half", "full", 2*d2["A"], 2*d2["sd_A"]),
            ("mass_T_H", "mass", d2["A"], d2["sd_A"]), ("U_prior", "full", u["A"], u["sd_A"]),
            ("no_prior_full", "full", None, None), ("no_prior_des", "des", None, None), ("no_prior_mass", "mass", None, None)]
    out = {}
    for name, sk, ah, sh in cfgs:
        s = S[sk]
        r = joint(np.array(s["grid_f"]), np.array(s["f"]), np.array(s["q0"]), np.array(s["grid_n"]), np.array(s["n"]),
                  np.array(s["t"]), ah, sh)
        r["word_today"] = w2(r["q0"], r["D_today"]); r["word_ever"] = w3(r["D_never"]); r["distances"] = sk
        out[name] = r
        pr = f"prior {ah:+.4f} +- {sh:.4f}" if sh else "no prior"
        log(f"J {name:14s} (T_H {sk}, {pr}): A_H {r['A']:+.3f} 68% {r['ci68']} dchi2(0) {r['D_A0']:.3f} dchi2(1) {r['D_A1']:.3f}"
            f" | q0 {r['q0']:+.4f} today dchi2 {r['D_today']:.3f} (at A {r['A_today']:+.3f}) never dchi2 {r['D_never']:.3f} (at A {r['A_never']:+.3f})"
            f" edges {r['edge']} -> {r['word_today']}; {r['word_ever']}")
    res["J"] = out


def main():
    t0 = time.time(); res = dict(mode=MODE, numpy=np.__version__)
    log(f"AGB3R mode {MODE}")
    if MODE == "KS": mode_KS(res)
    elif MODE.startswith("S_"): mode_S(res, MODE[2:])
    elif MODE == "E": mode_E(res)
    elif MODE == "J": mode_J(res)
    else: raise SystemExit(f"unknown mode {MODE}")
    res["seconds"] = round(time.time() - t0, 1)
    with open(os.path.join(HERE, f"agb3r_{MODE}.json"), "w") as fh: json.dump(res, fh, indent=1, default=float)
    log(f"wrote agb3r_{MODE}.json ({res['seconds']} s)")


if __name__ == "__main__":
    main()
