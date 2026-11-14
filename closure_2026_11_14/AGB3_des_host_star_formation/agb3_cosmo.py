"""AGB3 Parts S, J and E (criteria: FROZEN_CRITERIA.md in this folder).

AGB1's Part A model (DESI DR2 BAO + Dovekie supernovae, flat w0-wa, full covariance; fitter imported unchanged from
closure_2026_11_13/AGB1_progenitor_age_bias/) with an age term built from the hosts of this very sample:
    mu_model(z) + M + A_H x T_H(z),   T_H(z) = 0.030 mag/Gyr x [mean host age in the lowest redshift bin - mean host age at z]
A_H = 1 is the published slope acting on the sample's own age drift.

Usage: python3 -I agb3_cosmo.py MODE [outdir]
  S   the harness check KS, Part S and the chi2 grids Part J needs      -> agb3_S.json
  E   Part E: young hosts only                                          -> agb3_E.json
  J   Part J: arithmetic on agb3_S.json and agb3_D.json, fits nothing   -> agb3_J.json"""
import json, os, sys, time
for _v in ("VECLIB_MAXIMUM_THREADS", "OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS"):
    os.environ.setdefault(_v, "2")
import copy
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
MODE = sys.argv[1] if len(sys.argv) > 1 else "none"
OUTDIR = sys.argv[2] if len(sys.argv) > 2 else HERE
REPO = os.environ.get("AGB3_REPO") or os.path.normpath(os.path.join(HERE, "..", ".."))
AGB1 = os.path.join(REPO, "closure_2026_11_13", "AGB1_progenitor_age_bias")
AGB2 = os.path.join(REPO, "closure_2026_11_14", "AGB2_host_mass_step_redshift")
sys.argv = ["agb1_run.py", "AGB3"]                       # the imported modules read their mode from the command line
sys.path.insert(0, HERE); sys.path.insert(1, AGB2); sys.path.insert(2, AGB1)
import agb3_run as R3
import agb3_twocomp as T2
import agb2_galaxy as G
import agb2_joint as J2
import agb1_run as R1
import agb1_template as TPL

GRID_F, GRID_N = J2.GRID_F, J2.GRID_N
SLOPE = 0.030


def host_curve(z, ages, nb=20):
    """Mean host age in equal-count redshift bins: (bin mean redshift, bin mean age)."""
    b = R3.bins_of(z, nb)
    return np.array([z[b == k].mean() for k in range(nb)]), np.array([ages[b == k].mean() for k in range(nb)])


def t_h(zq, zc, ac):
    return SLOPE*(ac[0] - np.interp(zq, zc, ac))          # flat outside the bin range


def forks(F, name, coef, log, label):
    """Best fit, the fit with q0 = 0 and the fit with q >= 0, at a fixed coefficient (or free if coef is None)."""
    fixed = {} if (coef is None or name is None) else {name: coef}; free = [name] if (coef is None and name is not None) else []
    base = F.fit(fixed, free); today = F.fit(fixed, free, "today", extra=(base,)); never = F.fit(fixed, free, "never", extra=(today, base))
    for c in (today, never):                              # a constrained fit can never beat the unconstrained one
        if c["chi2"] < base["chi2"] - 1e-7: base = min([base, F.fit(fixed, free, "free", extra=(c,))], key=lambda r: r["chi2"])
    out = dict(base=base, today=today, never=never, D_today=today["chi2"] - base["chi2"], D_never=never["chi2"] - base["chi2"])
    log(f"  {label}: chi2 {base['chi2']:.4f}  Om {base['Om']:.4f} w0 {base['w0']:+.4f} wa {base['wa']:+.4f} q0 {base['q0']:+.4f}"
        + (f"  A_H {base['coef'][name]:+.4f}" if free else "") + f" | q0 = 0: dchi2 {out['D_today']:.3f} | never accelerated: dchi2 {out['D_never']:.3f}"
        f" (min q {never['qmin']:+.5f})  edge {base['edge']}")
    return out


def grids(F, name, log, label):
    """f(A), q0(A), t(A) on the 0.1 grid and n(A) on the 0.25 grid, for Part J."""
    f, q0, t, n, ff, tf = {}, {}, {}, {}, {}, {}
    prev = None
    for a in GRID_F:
        r = F.fit({name: a}, [], extra=(prev,)); prev = r; ff[a] = r
    prev = None
    for a in GRID_F:
        r = F.fit({name: a}, [], "today", extra=(ff[a], prev)); prev = r; tf[a] = r
        if r["chi2"] < ff[a]["chi2"] - 1e-7: ff[a] = min([ff[a], F.fit({name: a}, [], "free", extra=(r,))], key=lambda x: x["chi2"])
    prev = None
    for a in GRID_N:
        g = min(GRID_F, key=lambda x: abs(x - a))
        r = F.fit({name: a}, [], "never", extra=(tf[g], ff[g], prev)); prev = r; n[a] = r["chi2"]
    for a in GRID_F: f[a] = ff[a]["chi2"]; q0[a] = ff[a]["q0"]; t[a] = tf[a]["chi2"]
    log(f"  grids {label}: f(0) {f[0.0]:.3f} f(1) {f[1.0]:.3f}; t - f at A_H 0, 1: {t[0.0] - f[0.0]:.3f}, {t[1.0] - f[1.0]:.3f}; n - f at 0, 1: {n[0.0] - f[0.0]:.3f}, {n[1.0] - f[1.0]:.3f}")
    return dict(f=[f[a] for a in GRID_F], q0=[q0[a] for a in GRID_F], t=[t[a] for a in GRID_F], n=[n[a] for a in GRID_N])


def hd_order(d):
    """Index of each Hubble-diagram row in the host table (the two files list the supernovae in different orders)."""
    cid = [l.split()[1] for l in open(os.path.join(R1.DES5, "DES-Dovekie_HD.csv")) if l.startswith("SN:")]
    pos = {c: i for i, c in enumerate(d.cid)}
    return np.array([pos[c] for c in cid])


def subsample(sn, cov, sel):
    """AGB1's SN object restricted to the rows in sel (covariance sub-block, as AGB1 does for a dropped supernova)."""
    s = copy.copy(sn); s.W = np.linalg.inv(cov[np.ix_(sel, sel)])
    s.ids, s.z, s.zh, s.mu = sn.ids[sel], sn.z[sel], sn.zh[sel], sn.mu[sel]
    s.n = int(sel.sum()); s.n_des = int((s.ids == 10).sum()); s.W1 = s.W@np.ones(s.n); s.s11 = float(s.W1.sum()); s.T = {}
    return s


def main():
    t0 = time.time(); log = lambda m: print(m, flush=True)
    log(f"AGB3 cosmology part, mode {MODE}")
    if MODE == "J":
        D = json.load(open(os.path.join(OUTDIR, "agb3_D.json")))["fits"]; S = json.load(open(os.path.join(OUTDIR, "agb3_S.json")))
        Af, An = np.array(GRID_F), np.array(GRID_N)
        d2, d2p, u = D["primary"]["D2"], D["fork_P"]["D2"], D["primary"]["U"]
        pri = dict(D2=(d2["A"], d2["sd_A"]), D2_P=(d2p["A"], d2p["sd_A"]), half=(2*d2["A"], 2*d2["sd_A"]), U=(u["A"], u["sd_A"]))
        combos = [("primary", "full_sfr", "D2"), ("des_only", "des_only_sfr", "D2"), ("reading_P", "full_sfr", "D2_P"),
                  ("half_template", "full_sfr", "half"), ("mass_only_drift", "full_mass", "D2"), ("U_prior", "full_sfr", "U")]
        res = dict(mode="J", priors={k: list(v) for k, v in pri.items()}, combos={})
        for name, gk, pk in combos:
            g = S["grids"][gk]; ah, sh = pri[pk]
            r = J2.joint(Af, np.array(g["f"]), np.array(g["q0"]), An, np.array(g["n"]), np.array(g["t"]), ah, sh); res["combos"][name] = r
            log(f"  {name:16s} prior {ah:+.3f} +- {sh:.3f} on grids {gk}: joint A_H {r['A']:+.3f} (68% {r['ci68']})  dchi2(0) {r['D_A0']:.2f} dchi2(1) {r['D_A1']:.2f}"
                f" | q0 {r['q0']:+.3f}; q0 = 0: dchi2 {r['D_today']:.3f}; never accelerated: dchi2 {r['D_never']:.3f}  edges {r['edge']}")
        for gk in S["grids"]:
            g = S["grids"][gk]; r = J2.joint(Af, np.array(g["f"]), np.array(g["q0"]), An, np.array(g["n"]), np.array(g["t"])); res.setdefault("no_prior", {})[gk] = r
            log(f"  no prior, grids {gk}: A_H {r['A']:+.3f} (68% {r['ci68']}) dchi2(0) {r['D_A0']:.2f} dchi2(1) {r['D_A1']:.2f}  edges {r['edge']}")
        with open(os.path.join(OUTDIR, "agb3_J.json"), "w") as fh: json.dump(res, fh, indent=1, default=float)
        log("wrote agb3_J.json"); return
    d = R3.DES(); idx = hd_order(d)
    age_sfr = {zf: T2.age(d.lm, d.ls, d.z, zf=zf) for zf in (3.0, 2.0, 5.0)}; age_mass = G.age(d.lm, d.z)
    bao = R1.BAO("all")
    if MODE == "S":
        res = dict(mode="S", grid_f=GRID_F, grid_n=GRID_N, curves={}, fits={}, grids={}, KS={}); ks_ok = True
        for sample in ("full", "des_only"):
            sn = R1.SN(sample); m = d.mask(sample); F = R1.Fitter("A", sn, bao)
            A1 = json.load(open(os.path.join(AGB1, f"agb1_A_{sample}.json")))["forks"]
            zc, ac = host_curve(d.z[m], age_sfr[3.0][m]); res["curves"][f"{sample}_sfr"] = dict(z=zc.tolist(), age=ac.tolist())
            sn.add_template("hosts", t_h(sn.z, zc, ac)); sn.add_template("age", TPL.T(sn.z, "S"))
            log(f"sample {sample}: {sn.n} supernovae; T_H at the sample's redshifts: min {sn.T['hosts'][0].min():+.4f} max {sn.T['hosts'][0].max():+.4f} mag")
            k0 = forks(F, "hosts", 0.0, log, f"{sample} A_H = 0 (AGB1's A = 0 fork)"); k1 = forks(F, "age", 1.0, log, f"{sample} AGB1's template at 1 (AGB1's A = 1 fork)")
            ks = dict(today_A0=[k0["D_today"], A1["A0"]["D_today"]], never_A0=[k0["D_never"], A1["A0"]["D_never"]],
                      today_A1=[k1["D_today"], A1["A1"]["D_today"]], never_A1=[k1["D_never"], A1["A1"]["D_never"]])
            ok = all(abs(v[0] - v[1]) <= 0.01 for v in ks.values()); ks["passed"] = bool(ok); ks_ok = ks_ok and ok; res["KS"][sample] = ks
            log(f"KS {sample}: " + "; ".join(f"{k} {v[0]:.3f} ({v[1]:.3f})" for k, v in ks.items() if k != "passed") + f" -> {'PASS' if ok else 'FAIL'}")
            one = forks(F, "hosts", 1.0, log, f"{sample} A_H = 1 (published slope on this sample's drift)")
            fr = forks(F, "hosts", None, log, f"{sample} A_H free")
            res["fits"][sample] = dict(A0=k0, A1=one, Afree=fr, A_free=fr["base"]["coef"]["hosts"], D_A0=k0["base"]["chi2"] - fr["base"]["chi2"],
                                       D_A1=one["base"]["chi2"] - fr["base"]["chi2"])
            log(f"  {sample}: A_H free {res['fits'][sample]['A_free']:+.3f}; dchi2(A_H = 0) {res['fits'][sample]['D_A0']:.3f}; dchi2(A_H = 1) {res['fits'][sample]['D_A1']:.3f}")
            res["grids"][f"{sample}_sfr"] = grids(F, "hosts", log, f"{sample}, star-formation ages")
            if sample == "full":
                for key, ages in (("mass", age_mass), ("zf2", age_sfr[2.0]), ("zf5", age_sfr[5.0])):
                    zc2, ac2 = host_curve(d.z[m], ages[m]); res["curves"][f"full_{key}"] = dict(z=zc2.tolist(), age=ac2.tolist())
                    sn.add_template(key, t_h(sn.z, zc2, ac2)); res["fits"][f"full_{key}"] = dict(A1=forks(F, key, 1.0, log, f"full, {key}: A_H = 1"))
                res["grids"]["full_mass"] = grids(F, "mass", log, "full, mass-only ages")
                per = SLOPE*(ac[0] - age_sfr[3.0][idx]); sn.add_template("perhost", per)
                res["fits"]["full_perhost"] = dict(A1=forks(F, "perhost", 1.0, log, "full, correction host by host (reported): coefficient 1"))
        res["KS_passed"] = bool(ks_ok); res["seconds"] = round(time.time() - t0, 1)
        with open(os.path.join(OUTDIR, "agb3_S.json"), "w") as fh: json.dump(res, fh, indent=1, default=float)
        log(f"wrote agb3_S.json  ({res['seconds']} s)")
    elif MODE == "E":
        sn = R1.SN("full"); cov = np.linalg.inv(sn.W)
        ls, col, ids = d.ls[idx], d.col[idx], d.ids[idx]
        assert np.all(d.z[idx] == sn.z)
        sel = dict(young=ls >= -9.5, blue=col <= 0.8, young10=ls >= -10.0, old=ls < -9.5, young_des=(ls >= -9.5) & (ids == 10))
        res = dict(mode="E", fits={})
        for name, s in sel.items():
            sub = subsample(sn, cov, s); F = R1.Fitter("A", sub, bao)
            r = forks(F, None, None, log, f"{name} ({sub.n} supernovae, {sub.n_des} DES), published moduli")
            sub.add_template("age", TPL.T(sub.z, "S")); fr = F.fit({}, ["age"], extra=(r["base"],))
            r.update(n=sub.n, n_des=sub.n_des, A_S_free=fr["coef"]["age"], D_AS0=r["base"]["chi2"] - fr["chi2"], D_AS1=F.fit({"age": 1.0}, [], extra=(fr,))["chi2"] - fr["chi2"])
            log(f"     AGB1's template free on this subsample: A {r['A_S_free']:+.3f}; dchi2(0) {r['D_AS0']:.3f}; dchi2(1) {r['D_AS1']:.3f}")
            res["fits"][name] = r
        res["seconds"] = round(time.time() - t0, 1)
        with open(os.path.join(OUTDIR, "agb3_E.json"), "w") as fh: json.dump(res, fh, indent=1, default=float)
        log(f"wrote agb3_E.json  ({res['seconds']} s)")
    else:
        raise SystemExit(f"unknown mode {MODE}")


if __name__ == "__main__":
    main()
