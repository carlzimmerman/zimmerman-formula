#!/usr/bin/env python3
"""DP3: sigma_sys definitions (a), (b), (e), (g2) on ANY frozen-cut catalogue, by the D2 lane's recipe (NEW file).

The recipe is doors_push_2026_10_22/D2_wide_binary_fork/d2_sigma_sys_defs.py (A2/A3 of the D2 note), which is hard-wired to the
DR3 paths; this file takes the catalogues as arguments so the same recipe can run on DR4. Same estimator, same seed and the same
call order, so on the DR3 inputs it must reproduce the D2 lane's ladder shifts (FROZEN_CRITERIA.md D6). The frozen pipeline is
IMPORTED READ-ONLY (functions only; nothing written into prep_2026); a socket guard forbids any network access.
  ladder rungs (post-filters of the base catalogue): R_chance < 0.001; 3 <= s < 20 kAU;  NSS-off probe: a separate catalogue, s < 30 kAU
  (b)  = max(0.020, 1/2 x full spread of {base, rungs, NSS-off})        (A3.1 primary)
  (a)  = 0.020;  (e) = delete-one jackknife over {base, rungs, NSS-off};  (g2) = sqrt(0.020^2 + sigma_build^2), sigma_build from an
       Amendment 18 seed-sweep manifest (seed_sweep_manifest*.json 'sigma_build'), or the DR3 bound 0.44 x 0.019 if none is given (flagged)
If --nss-off is not given the NSS-off rung is NOT IMPLEMENTED (D7 N4.1): (b) and (e) are computed without it and the output says so.
Extra builds (--extra NAME=CSV) are fitted and reported only (the D2 lane's V4/V5); they are not ladder rungs.
Run: OMP_NUM_THREADS=1 nice -n 10 python3 -B dp3_sigma_sys.py --base CAT.csv [--nss-off NSSOFF.csv] [--extra V4=..] [--seed-manifest M.json] --out-json S.json
kappa = 1/2 FITTED; footings never pooled; not theory closed. DR3 numbers are code-path tests, never results (Amendment 7(e)).
"""
import sys
sys.dont_write_bytecode = True
import argparse, csv, hashlib, json, math, os, socket
import numpy as np


def _no_net(*a, **k):
    raise RuntimeError("network access forbidden (DP3 sigma_sys)")


socket.socket.connect = _no_net
socket.create_connection = _no_net
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, os.path.join(ROOT, "prep_2026", "gaia_dr4_prep"))
import wide_binary_pipeline as wbp  # noqa: E402  (read-only import)

NM = 1_000_000                       # as the D2 lane (declared there: smaller than the frozen 3,000,000)
SEED = 20261216
SBUILD_DR3_BOUND = 0.44 * 0.019


def rows_of(path):
    return list(csv.DictReader(open(path)))


def arrays(rows):
    s = np.array([float(r["sep_kAU"]) for r in rows]) * wbp.KAU
    vp = np.array([float(r["v_perp_kms"]) for r in rows]) * 1e3
    Mt = np.array([float(r["M1_msun"]) + float(r["M2_msun"]) for r in rows])
    return wbp.G * Mt * wbp.MSUN / s ** 2, vp / np.sqrt(wbp.G * Mt * wbp.MSUN / s)


def sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--base", required=True); ap.add_argument("--nss-off", default=None)
    ap.add_argument("--extra", action="append", default=[]); ap.add_argument("--seed-manifest", default=None)
    ap.add_argument("--out-json", required=True); ap.add_argument("--tag", default="")
    ap.add_argument("--stage-a", default=None, help="OPTIONAL (open issue O6, owner decision needed): add the ladder rung RUWE < 1.2 on both components, "
                    "ruwe looked up by source_id in this stage_A.npz (as seed_sweep.py --ladder does); off = the D2 recipe")
    a = ap.parse_args(argv)
    rng = np.random.default_rng(SEED)
    pop = wbp.make_population(NM, rng, dr4=True)
    A0 = {"canonical": wbp.A0_CAN, "alt": wbp.A0_ALT}
    MOD = {f: wbp.model_medians(pop, A0[f], wbp.GRID, rng) for f in ("canonical", "alt")}
    base = rows_of(a.base)
    var = {"V0 base": base,
           "V1 ladder: R_chance < 0.001": [r for r in base if float(r["R_chance"]) < 0.001],
           "V2 ladder: sep 3-20 kAU": [r for r in base if 3.0 <= float(r["sep_kAU"]) < 20.0]}
    if a.nss_off:
        var["V3 NSS-off probe (s < 30 kAU)"] = [r for r in rows_of(a.nss_off) if float(r["sep_kAU"]) < 30.0]
    for e in a.extra:
        k, p = e.split("=", 1)
        var["extra " + k] = rows_of(p)
    if a.stage_a:
        z = np.load(a.stage_a); sid = z["source_id"]; o = np.argsort(sid); sid, ru = sid[o], z["ruwe"][o]
        def rw(x):
            x = np.int64(x); i = min(np.searchsorted(sid, x), len(sid) - 1)
            return ru[i] if sid[i] == x else np.nan
        var["V6 ladder: RUWE < 1.2 both (O6)"] = [r for r in base if rw(r["source_id1"]) < 1.2 and rw(r["source_id2"]) < 1.2]
    fits, lines = {}, []
    P = lambda s: (print(s, flush=True), lines.append(s))
    P(f"DP3 sigma_sys ({a.tag or 'untagged'}); master MC {len(pop['s_obs']):,d} after selection; NSS-off rung "
      + ("given" if a.nss_off else "NOT IMPLEMENTED (D7 N4.1): sigma_sys(b) is computed without it"))
    for f in ("canonical", "alt"):
        for name, rr in var.items():
            gN, vt = arrays(rr)
            med, sig, cnt = wbp.bin_medians(np.log10(gN / A0[f]), vt, boot=200, rng=rng)
            g, sg, chi2, nb, kap = wbp.fit_gamma(med, sig, MOD[f], wbp.GRID)
            fits[f"{f}|{name}"] = dict(N=len(rr), gamma=float(g), sigma_fit=float(sg), kappa=float(kap))
            P(f"  {f:9s} {name:34s} N={len(rr):6d}  gamma-hat {g:.4f} +- {sg:.4f}  kappa {kap:.4f}")
    sb = None
    if a.seed_manifest:
        sb = json.load(open(a.seed_manifest)).get("sigma_build")
    out = dict(tag=a.tag, base=os.path.basename(a.base), base_sha256=sha(a.base), nss_off=(os.path.basename(a.nss_off) if a.nss_off else None),
               nss_off_status=("IMPLEMENTED (catalogue given)" if a.nss_off else "NOT IMPLEMENTED (D7 N4.1); sigma_sys(b) computed without it"),
               fits=fits, seed_manifest=(os.path.basename(a.seed_manifest) if a.seed_manifest else None))
    ladder = [k for k in var if k.startswith(("V1", "V2", "V3", "V6"))]
    for f in ("canonical", "alt"):
        g0 = fits[f"{f}|V0 base"]["gamma"]
        gl = [g0] + [fits[f"{f}|{k}"]["gamma"] for k in ladder]
        spread = max(gl) - min(gl)
        n = len(gl)
        loo = [np.mean([x for j, x in enumerate(gl) if j != i]) for i in range(n)]
        jk = math.sqrt((n - 1) / n * sum((x - np.mean(loo)) ** 2 for x in loo))
        if sb and f in sb:
            sbf, src = float(sb[f]["sigma_build"]), "seed-sweep manifest"
        else:
            sbf, src = SBUILD_DR3_BOUND, "PLACEHOLDER: the DR3 bound 0.44 x 0.019 (no seed-sweep manifest given)"
        shifts = {k: fits[f"{f}|{k}"]["gamma"] - g0 for k in ladder}
        sf0 = fits[f"{f}|V0 base"]["sigma_fit"]
        out[f] = dict(b=max(0.020, 0.5 * spread), a=0.020, e=jk, g2=math.sqrt(0.020 ** 2 + sbf ** 2), sigma_build=sbf, sigma_build_source=src,
                      spread=spread, shifts=shifts, base_gamma=g0, base_sigma_fit=sf0,
                      stability_gate_information=dict(max_abs_shift=max(abs(x) for x in shifts.values()), sigma_fit=sf0,
                                                      shifts_below_1_sigma_fit={k: abs(v) < sf0 for k, v in shifts.items()}))
        P(f"[{f}] shifts " + ", ".join(f"{k.split(':')[0]} {v:+.4f}" for k, v in shifts.items()) +
          f"; spread {spread:.4f}; (b) {out[f]['b']:.4f}  (a) 0.0200  (e) {jk:.4f}  (g2) {out[f]['g2']:.4f} [sigma_build {sbf:.4f}, {src}]")
    json.dump(out, open(a.out_json, "w"), indent=1, default=float)
    open(os.path.splitext(a.out_json)[0] + ".out", "w").write("\n".join(lines) + "\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
