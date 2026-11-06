#!/usr/bin/env python3
"""DP2 Part 2: hidden-triple injection into the CFG943 Newtonian MOCK sky, run with and without a modelled NSS screen
(FROZEN_CRITERIA.md section 2). Every number is a MOCK. INFORMATION ONLY (owner D8): it can never change sigma_sys, a band or a verdict.

The sky generator (cfg943_common.make_catalogue, class A0_NEWTON), the frozen estimator (wide_binary_pipeline.bin_medians /
fit_gamma) and CFG943's frozen model medians are imported / read read-only. The triple and NSS models are DP2's own ASSUMPTIONS.
Run: OMP_NUM_THREADS=1 nice -n 10 python3 -B dp2_triples.py --ncat N1,N2 --K K     -> dp2_triples.out / _results.json
     ... --mutate                                                                  -> dp2_triples_MUTATE.out / _results.json
kappa = 1/2 FITTED; footings never pooled; not theory closed.
"""
import sys
sys.dont_write_bytecode = True
import os, json, socket, hashlib, time, argparse, resource

def _no_net(*a, **k):
    raise RuntimeError("network access forbidden in DP2")
socket.socket.connect = _no_net
socket.create_connection = _no_net

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
C943 = os.path.join(ROOT, "campaign_fresh_gravity", "CFG943_dr4_readiness")
sys.path.insert(0, C943)
import cfg943_common as C            # noqa: E402  read-only (imports the frozen pipeline read-only)
W = C.W

ap = argparse.ArgumentParser()
ap.add_argument("--ncat", default="30000")
ap.add_argument("--K", type=int, default=30)
ap.add_argument("--mutate", action="store_true")
ap.add_argument("--tag", default="", help="output suffix (declared extensions, e.g. more repeats)")
A = ap.parse_args()
TAG = ("_MUTATE" if A.mutate else "") + A.tag
OUT = []
FTS = [0.0, 0.05, 0.10, 0.20, 0.30]
T_DR4, T_DR3 = 66 / 12., 34 / 12.          # yr
THR_DR4, THR_DR3 = 0.10, 0.30              # mas, Dphys thresholds (assumption A-D)
YR = 3.15576e7
DAY = 86400.
FROZEN = ["prep_2026/gaia_dr4_prep/wide_binary_pipeline.py",
          "campaign_fresh_gravity/CFG943_dr4_readiness/cfg943_common.py",
          "campaign_fresh_gravity/CFG943_dr4_readiness/cfg943_mock_dryrun.py",
          "campaign_fresh_gravity/CFG943_dr4_readiness/cfg943_model_medians.npz"]


def P(s=""):
    OUT.append(s); print(s, flush=True)


def rss():
    return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1e6


def hashes():
    return {f: hashlib.sha256(open(os.path.join(ROOT, f), "rb").read()).hexdigest() for f in FROZEN}


h0 = hashes()
z = np.load(os.path.join(C943, "cfg943_model_medians.npz"))
assert np.array_equal(z["grid"], W.GRID)
MODS = {"canonical": (z["can_med"], z["can_sig"]), "alt": (z["alt_med"], z["alt_sig"])}
A0S = {"canonical": W.A0_CAN, "alt": W.A0_ALT}


def fit(c, vt, sel, rng):
    out = {}
    for foot in ("canonical", "alt"):
        ly = np.log10(c["g_proj"][sel] / A0S[foot])
        med, sig, cnt = W.bin_medians(ly, vt[sel], boot=200, rng=rng)
        g, sg, chi2, nb, kap = W.fit_gamma(med, sig, MODS[foot], W.GRID)
        out[foot] = (float(g), float(sg), float(kap))
    return out


def triple_params(c, rng):
    """Hidden-triple parameters for every pair (assumption A-T); used for the chosen subset only."""
    n = len(c["vt"])
    host1 = rng.random(n) < 0.5
    Mh = np.where(host1, c["M1"], c["M2"])
    q = rng.uniform(0.1, 1.0, n)
    Pd = np.empty(n); todo = np.ones(n, bool)
    amax = c["r3d"] / 3.0                                     # m
    while todo.any():
        k = np.flatnonzero(todo)
        lp = rng.normal(5.03, 2.28, len(k))
        Pk = 10 ** lp
        a = (W.G * Mh[k] * (1 + q[k]) * W.MSUN * (Pk * DAY) ** 2 / (4 * np.pi ** 2)) ** (1 / 3.)
        ok = (Pk >= 1.0) & (a <= amax[k])
        Pd[k[ok]] = Pk[ok]; todo[k[ok]] = False
    Ps = Pd * DAY
    a_in = (W.G * Mh * (1 + q) * W.MSUN * Ps ** 2 / (4 * np.pi ** 2)) ** (1 / 3.)
    vrel = 2 * np.pi * a_in / Ps
    beta = q / (1 + q) - q ** 4 / (1 + q ** 4)
    u = rng.standard_normal((3, n)); u /= np.linalg.norm(u, axis=0)        # isotropic velocity direction
    return dict(q=q, m=q * Mh, P_yr=Pd / 365.25, a_au=a_in / W.AU, vph=beta * vrel, ux=u[0], uy=u[1], beta=beta,
                flat=rng.random(n))


def apply_triples(c, tp, is_t, T, kick=True, mass=True):
    """Returns (pmx, pmy) true relative PM with the hidden-triple effects for pairs in is_t."""
    dk = c["d"] / 1000.
    x = np.pi * T / tp["P_yr"]
    avg = np.abs(np.sin(x) / x)
    sc = np.where(is_t & mass, np.sqrt((c["Mt"] + tp["m"]) / c["Mt"]), 1.0)
    kx = np.where(is_t & kick, tp["vph"] * avg * tp["ux"] / (4.74e3 * dk), 0.0)
    ky = np.where(is_t & kick, tp["vph"] * avg * tp["uy"] / (4.74e3 * dk), 0.0)
    return sc * c["pmx"] + kx, sc * c["pmy"] + ky


def detect_phys(c, tp, is_t, T, thr):
    alpha = tp["beta"] * tp["a_au"] * c["plx"]                 # mas
    x = np.pi * T / tp["P_yr"]
    S = np.where(tp["P_yr"] <= T, alpha, alpha * (1 - np.cos(np.minimum(x, np.pi))))
    return is_t & (S >= thr)


def vt_from(c, pmx, pmy, boost=None):
    cc = dict(c); cc["pmx"], cc["pmy"] = pmx, pmy
    b = np.ones(len(pmx)) if boost is None else boost
    vt, _ = C.velocities(cc, b)
    return vt


def one(n_cat, k, fts, mutate=False):
    sky = C.make_catalogue(n_cat, np.random.default_rng([2026, 1105, n_cat, 0, k]), "A0_NEWTON")
    n = len(sky["vt"])
    allsel = np.ones(n, bool)
    rec = {}
    for fi, ft in enumerate(fts):
        trng = np.random.default_rng([2026, 1105, n_cat, fi, k])
        tp = triple_params(sky, trng)
        is_t = np.zeros(n, bool)
        is_t[trng.permutation(n)[:int(round(ft * n))]] = True
        r = dict(n_triples=int(is_t.sum()))
        frng = lambda j: np.random.default_rng([2026, 1105, n_cat, k, 99, j])
        for era, T, thr in (("DR4", T_DR4, THR_DR4), ("DR3a", T_DR3, THR_DR3)):
            pmx, pmy = apply_triples(sky, tp, is_t, T)
            vt = vt_from(sky, pmx, pmy)
            r[f"{era}_off"] = fit(sky, vt, allsel, frng(0))
            dets = {"Dphys": detect_phys(sky, tp, is_t, T, thr)}
            if era == "DR4":
                dets["flat0.5"] = is_t & (tp["flat"] < 0.5)
                dets["flat0.9"] = is_t & (tp["flat"] < 0.9)
            for dn, det in dets.items():
                r[f"{era}_on_{dn}"] = fit(sky, vt, ~det, frng(0))
                r[f"{era}_removed_{dn}"] = float(det.mean())
            if era == "DR4" and k < 5 and ft > 0:      # T2 / T3 nulls
                pz, qz = apply_triples(sky, tp, is_t, T, kick=False, mass=False)
                r["T2_null_off"] = fit(sky, vt_from(sky, pz, qz), allsel, frng(0))
                r["T3_null_on"] = fit(sky, vt, ~np.zeros(n, bool), frng(0))
        rec[ft] = r
    if mutate:
        b = W.gamma_of_y(sky["g_true"] / W.A0_CAN, 1.10, W.y_extN(W.A0_CAN))
        rec["mutate_boost_1.10"] = fit(sky, vt_from(sky, sky["pmx"], sky["pmy"], boost=b), allsel, np.random.default_rng([2026, 1105, n_cat, k, 99, 0]))
        rec["mutate_base"] = fit(sky, vt_from(sky, sky["pmx"], sky["pmy"]), allsel, np.random.default_rng([2026, 1105, n_cat, k, 99, 0]))
    del sky
    return rec


def main():
    t0 = time.time()
    RES = dict(lane="DP2 Part 2", mode="MUTATE" if A.mutate else "main", information_only=True, mock=True,
               model_npz_sha256=h0[FROZEN[3]], fts=FTS, K=A.K, runs={}, checks={})
    P("DP2 Part 2: hidden-triple injection, CFG943 Newton MOCK sky (every number a MOCK; INFORMATION ONLY, owner D8). kappa = 1/2 FITTED.")
    P(f"model medians: CFG943 cfg943_model_medians.npz sha256 {h0[FROZEN[3]][:16]}; pipeline sha256 {h0[FROZEN[0]][:16]}")
    if A.mutate:
        recs = [one(30000, k, [0.0], mutate=True) for k in range(10)]
        d = {foot: float(np.mean([r["mutate_boost_1.10"][foot][0] - r["mutate_base"][foot][0] for r in recs])) for foot in ("canonical", "alt")}
        bites = d["canonical"] >= 0.05
        RES["mutate_shift"] = d; RES["checks"]["T4_mutate_bites"] = bites
        P(f"T4 MUTATE boost gamma_inf 1.10 on a Newton sky, N 30,000, K 10: mean gamma-hat shift canonical {d['canonical']:+.4f}, alt {d['alt']:+.4f} "
          f"-> {'BITES' if bites else 'DOES NOT BITE: Part 2 NOT DIAGNOSTIC'}")
    else:
        for n_cat in [int(x) for x in A.ncat.split(",")]:
            recs = []
            for k in range(A.K):
                recs.append(one(n_cat, k, FTS))
                if k % 5 == 4:
                    P(f"  N_cat {n_cat}: {k + 1}/{A.K} repeats ({time.time() - t0:.0f} s, peak RSS {rss():.0f} MB)")
            summ = {}
            for ft in FTS:
                rs = [r[ft] for r in recs]; s = {}
                for key in rs[0]:
                    if key.startswith("T2") or key.startswith("T3") or key == "n_triples":
                        continue
                    if "removed" in key:
                        s[key] = float(np.mean([r[key] for r in rs])); continue
                    for foot in ("canonical", "alt"):
                        g = np.array([r[key][foot][0] for r in rs]); sg = np.array([r[key][foot][1] for r in rs])
                        s[f"{key}|{foot}"] = dict(mean=float(g.mean()), rms=float(g.std(ddof=1)), sg_mean=float(sg.mean()))
                for era, dns in (("DR4", ("Dphys", "flat0.5", "flat0.9")), ("DR3a", ("Dphys",))):
                    for dn in dns:
                        for foot in ("canonical", "alt"):
                            dd = np.array([r[f"{era}_off"][foot][0] - r[f"{era}_on_{dn}"][foot][0] for r in rs])
                            s[f"shift_{era}_{dn}|{foot}"] = dict(mean=float(dd.mean()), rms=float(dd.std(ddof=1)))
                summ[str(ft)] = s
            # null checks on the first 5 repeats
            t2 = all(r[ft]["T2_null_off"][f][0] == r[0.0]["DR4_off"][f][0] for r in recs[:5] for ft in FTS[1:] for f in ("canonical", "alt"))
            t3 = all(r[ft]["T3_null_on"][f][0] == r[ft]["DR4_off"][f][0] for r in recs[:5] for ft in FTS[1:] for f in ("canonical", "alt"))
            RES["runs"][str(n_cat)] = dict(summary=summ, repeats=[{str(a): b for a, b in r.items()} for r in recs], T2=t2, T3=t3)
            P(f"=== N_cat {n_cat}, K {A.K}: T2 null (no kick, no mass) == f_t 0: {'PASS' if t2 else 'FAIL'}; T3 null (p_det 0) shift 0: {'PASS' if t3 else 'FAIL'}")
            P("  f_t   foot  g_off(DR4)  rms   | g_on Dphys (removed)  shift | g_on p0.5 shift | g_on p0.9 shift | DR3a: g_off  g_on Dphys (removed) shift")
            for ft in FTS:
                s = summ[str(ft)]
                for foot in ("canonical", "alt"):
                    P(f"  {ft:.2f}  {foot[:3]}   {s[f'DR4_off|{foot}']['mean']:.4f}   {s[f'DR4_off|{foot}']['rms']:.4f} | "
                      f"{s[f'DR4_on_Dphys|{foot}']['mean']:.4f} ({s['DR4_removed_Dphys']:.3f})  {s[f'shift_DR4_Dphys|{foot}']['mean']:+.4f} | "
                      f"{s[f'DR4_on_flat0.5|{foot}']['mean']:.4f} {s[f'shift_DR4_flat0.5|{foot}']['mean']:+.4f} | "
                      f"{s[f'DR4_on_flat0.9|{foot}']['mean']:.4f} {s[f'shift_DR4_flat0.9|{foot}']['mean']:+.4f} | "
                      f"{s[f'DR3a_off|{foot}']['mean']:.4f}  {s[f'DR3a_on_Dphys|{foot}']['mean']:.4f} ({s['DR3a_removed_Dphys']:.3f}) {s[f'shift_DR3a_Dphys|{foot}']['mean']:+.4f}")
            if n_cat == 30000:
                m0 = summ["0.0"]["DR4_off|canonical"]["mean"]
                tol = max(3 * 0.0168 / np.sqrt(A.K), 0.005)
                t1 = abs(m0 - 1.0037) <= tol
                RES["checks"]["T1_known_answer"] = dict(passed=t1, mean=m0, ref=1.0037, tol=tol)
                P(f"T1 known answer f_t 0, N 30,000: mean gamma-hat canonical {m0:.4f} vs CFG943 A0 1.0037 (tol {tol:.4f}): {'PASS' if t1 else 'FAIL'}")
            offs = [summ[str(ft)]["DR4_off|canonical"]["mean"] for ft in FTS]
            RES["checks"][f"T5_monotone_{n_cat}"] = bool(np.all(np.diff(offs) > 0))
            P(f"T5 gamma_off rises with f_t (canonical) at N {n_cat}: {'yes' if np.all(np.diff(offs) > 0) else 'NO'} {np.round(offs, 4).tolist()}")
            RES["checks"][f"T2_{n_cat}"], RES["checks"][f"T3_{n_cat}"] = t2, t3
    h1 = hashes()
    RES["checks"]["T6_frozen_unchanged"] = h0 == h1
    P(f"T6 frozen files unchanged: {'PASS' if h0 == h1 else 'FAIL'}; peak RSS {rss():.0f} MB; {time.time() - t0:.0f} s")
    json.dump(RES, open(os.path.join(HERE, f"dp2_triples{TAG}_results.json"), "w"), indent=1, default=float)
    open(os.path.join(HERE, f"dp2_triples{TAG}.out"), "w").write("\n".join(OUT) + "\n")


if __name__ == "__main__":
    main()
