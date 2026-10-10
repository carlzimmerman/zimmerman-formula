#!/usr/bin/env python3
"""CFG551 step G-template: the galaxy-tracer (particle-density) drained-shell templates, and the K-DEP gate.

Implements FROZEN_CRITERIA.md (b1b7c9e08), Task 2 "G (galaxy density)" and K-DEP.
- CIC-deposits the committed z = 0 particle snapshots (read-only) with the engine's own convention (cfg527_pm.Mesh.deposit):
  u = pos/dx, i0 = floor(u) mod M, i1 = (i0+1) mod M, CIC weights; rho_p = 1 + delta.
- K-DEP (gate): the S0 deposits reproduce the committed cfg526_S0_L200_rhop.npy (512^3 and 256^3) to max |d rho| <= 1e-4.
- Stacks rho_p(R5 run) against rho_p(S0) with CFG546's own statistic: the `run()` function of
  ../CFG546_drained_shell_cluster_lensing/cfg546_predict.py executed from its source with ONE declared substitution
  (the R5 field is this lane's particle deposit instead of the committed rho_g file). S0 centres, S0 r_ta, x bins 0.1 to 4,
  ratio of stacked means, 200 bootstrap draws, seed 546.
Outputs: cfg551_ptemplate.out / cfg551_ptemplate_results.json; deposited fields cached in ../../../_external_data/cfg551_work/.
Run: OMP_NUM_THREADS=2 nice -n 10 python3 cfg551_ptemplate.py
"""
import os
os.environ.setdefault("OMP_NUM_THREADS", "2"); os.environ.setdefault("OPENBLAS_NUM_THREADS", "2")
os.environ.setdefault("VECLIB_MAXIMUM_THREADS", "2")
import json, math, time, types
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
CFG = os.path.dirname(HERE)
EXT = os.path.normpath(os.path.join(HERE, "..", "..", "..", "_external_data"))
W530 = os.path.join(EXT, "cfg530_work")
WORK = os.path.join(EXT, "cfg551_work"); os.makedirs(WORK, exist_ok=True)
L = 200.0
SNAP = {
    ("S0", 512): os.path.join(EXT, "cfg411_work", "cfg411_S0_Rc3_MIXA_FLAT_canonical_N512_z0.npz"),
    ("S0", 256): os.path.join(W530, "runs", "S0_L200_N256", "cfg527_S0_TA_NOFILT_MASSCONS_fretcensus_FLAT_canonical_N256_drawSHELL_z0.npz"),
    ("LRcan", 512): os.path.join(W530, "runs", "LRcan_L200_N512", "cfg527_RES_TA_NOFILT_MASSCONS_fretcensus_FLAT_canonical_N512_drawSHELL_z0.npz"),
    ("LRcan", 256): os.path.join(W530, "runs", "LRcan_L200_N256", "cfg527_RES_TA_NOFILT_MASSCONS_fretcensus_FLAT_canonical_N256_drawSHELL_z0.npz"),
    ("LRalt", 256): os.path.join(W530, "runs", "LRalt_L200_N256", "cfg527_RES_TA_NOFILT_MASSCONS_fretcensus_FLAT_alt_N256_drawSHELL_z0.npz"),
    ("LRalt", 512): os.path.join(W530, "runs", "LRalt_L200_N512", "cfg527_RES_TA_NOFILT_MASSCONS_fretcensus_FLAT_alt_N512_drawSHELL_z0.npz"),
}
_lines = []
RES = {"criteria_commit": "b1b7c9e08", "checks": {}, "templates": {}}


def P(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); _lines.append(s)


def check(name, detail, ok, gated=True):
    P(f"  [{'PASS' if ok else 'FAIL'}]{'' if gated else ' (reported)'} {name}: {detail}")
    RES["checks"][name] = dict(ok=bool(ok), detail=detail, gated=gated)
    return ok


def deposit(path, M, chunk=4_000_000):
    """CIC deposit, cfg527_pm.Mesh.deposit convention, chunked; returns rho_p = 1 + delta (float32)."""
    dx = L / M
    pos_all = np.load(path)["pos"]
    rho = np.zeros(M ** 3, np.float64)
    for s in range(0, pos_all.shape[0], chunk):
        pos = pos_all[s:s + chunk].astype(np.float64)
        u = pos / dx; i0 = np.floor(u).astype(np.int64); w = (u - i0).astype(np.float32)
        i1 = (i0 + 1) % M; i0 = i0 % M
        for cx in (0, 1):
            ix = i1[:, 0] if cx else i0[:, 0]; wx = w[:, 0] if cx else 1 - w[:, 0]
            for cy in (0, 1):
                iy = i1[:, 1] if cy else i0[:, 1]; wy = w[:, 1] if cy else 1 - w[:, 1]
                for cz in (0, 1):
                    iz = i1[:, 2] if cz else i0[:, 2]; wz = w[:, 2] if cz else 1 - w[:, 2]
                    rho += np.bincount((ix * M + iy) * M + iz, weights=wx * wy * wz, minlength=M ** 3)
        del pos, u, i0, i1, w
    del pos_all
    rho = rho.reshape((M,) * 3)
    return (1.0 + (rho / rho.mean() - 1.0).astype(np.float32)).astype(np.float32)


def field(name, M):
    f = os.path.join(WORK, f"cfg551_{name}_N{M}_rhop.npy")
    if not os.path.exists(f):
        t0 = time.time()
        np.save(f, deposit(SNAP[(name, M)], M))
        P(f"  deposited {name} N{M} ({time.time() - t0:.0f} s)")
    return np.load(f, mmap_mode="r")


P(__doc__.split("Run:")[0].strip())

# ---------------------------------------------------------------- K-DEP
P("\n== K-DEP: this lane's CIC deposit of the S0 snapshots vs the committed cfg526_S0_L200_rhop.npy")
kdep = True
for M in (512, 256):
    mine = field("S0", M)
    ref = np.load(os.path.join(W530, "profiles", f"N{M}", "cfg526_S0_L200_rhop.npy"), mmap_mode="r")
    dmax = 0.0
    for a in range(0, M, 64):
        dmax = max(dmax, float(np.max(np.abs(np.asarray(mine[a:a + 64], np.float64) - np.asarray(ref[a:a + 64], np.float64)))))
    kdep &= check(f"K-DEP S0 N{M}", f"max |d rho_p| = {dmax:.2e} (gate 1e-4)", dmax <= 1e-4)
RES["K_DEP"] = bool(kdep)

# ---------------------------------------------------------------- CFG546 run() with one declared substitution
src_path = os.path.join(CFG, "CFG546_drained_shell_cluster_lensing", "cfg546_predict.py")
src = open(src_path).read()
cut = src.index('P(__doc__.split("Run:")[0].strip())')
OLD = 'F = np.load(os.path.join(d, f"cfg526_{fname}_L200_rhog.npy"), mmap_mode="r")'
NEW = 'F = FIELDS[(fname, N)]'
assert src.count(OLD) == 1
C = types.ModuleType("cfg546p"); C.__file__ = src_path
exec(compile(src[:cut].replace(OLD, NEW), src_path, "exec"), C.__dict__)
C.FIELDS = {}
C.P = P                                   # route its printing into this lane's log
C.check = check
C.RES = {"runs": {}, "checks": RES["checks"]}

runs = {}
if kdep:
    for name, M in (("LRcan", 512), ("LRcan", 256), ("LRalt", 256), ("LRalt", 512)):
        if not os.path.exists(SNAP[(name, M)]):
            P(f"\n  {name} N{M}: snapshot missing, skipped"); continue
        C.FIELDS[(name, M)] = field(name, M)
        P(f"\n---- particle template: {name} N{M} (rho_p of the R5 run vs rho_p of S0, S0 centres)")
        runs[(name, M)] = C.run(M, name)
        C.FIELDS.clear()
    XC = np.array(C.XC)
    m = (XC >= 0.2) & (XC <= 3.0)
    for b in ("clusters", "groups"):
        try:
            a = np.array(runs[("LRcan", 512)]["bins"][b]["rel"]); c = np.array(runs[("LRcan", 256)]["bins"][b]["rel"])
            al = np.array(runs[("LRalt", 256)]["bins"][b]["rel"])
        except KeyError:
            continue
        s = float(np.sum(a[m] * c[m]) / np.sum(c[m] ** 2))
        T = {"canonical": a.tolist(), "alt": (s * al).tolist(), "s_res_p": s, "canonical_256": c.tolist(), "alt_256": al.tolist(),
             "canonical_sig": runs[("LRcan", 512)]["bins"][b]["rel_sig"],
             "alt_sig": (s * np.array(runs[("LRalt", 256)]["bins"][b]["rel_sig"])).tolist(),
             "canonical_256_sig": runs[("LRcan", 256)]["bins"][b]["rel_sig"], "alt_256_sig": runs[("LRalt", 256)]["bins"][b]["rel_sig"]}
        if ("LRalt", 512) in runs and b in runs[("LRalt", 512)]["bins"]:
            T["alt_512_reported"] = runs[("LRalt", 512)]["bins"][b]["rel"]
            T["alt_512_reported_sig"] = runs[("LRalt", 512)]["bins"][b]["rel_sig"]
        RES["templates"][b] = T
        P(f"\n  {b}: s_res,p (512 can onto 256 can, 0.2-3 r_ta) = {s:.3f}")
    RES["xc"] = XC.tolist()
    RES["runs"] = {f"N{M}_{n}": v for (n, M), v in runs.items()}

    # side-by-side with the lensing (rho_g) template, clusters
    G = json.load(open(os.path.join(CFG, "CFG546_drained_shell_cluster_lensing", "cfg546_predict_results.json")))
    tg = np.array(G["templates"]["clusters"]["canonical"])
    if "clusters" in RES["templates"]:
        tp = np.array(RES["templates"]["clusters"]["canonical"])
        P("\n== clusters, 512^3 canonical: rho_p (galaxy tracer) template vs rho_g (lensing) template")
        for j in range(1, len(XC), 2):
            if XC[j] > 3.0: break
            P(f"   x {XC[j]:.2f}: rel_p {tp[j]:+.4f}   rel_g {tg[j]:+.4f}")

json.dump(RES, open(os.path.join(HERE, "cfg551_ptemplate_results.json"), "w"), indent=1, default=float)
open(os.path.join(HERE, "cfg551_ptemplate.out"), "w").write("\n".join(_lines) + "\n")
