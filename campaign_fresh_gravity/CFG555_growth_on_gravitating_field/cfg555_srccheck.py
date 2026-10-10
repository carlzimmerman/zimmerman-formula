#!/usr/bin/env python3
"""CFG555 cross-check (reported; verifies the fail as hard as a win): the captured delta_src = delta_grav - delta_p must be the engine's e - comp,
i.e. (a) zero outside the catchments, (b) summing to ~0 on every catchment (per-catchment mass conservation), and (c) its positive part inside
the catchments must carry the engine's excess Sum e (= N^3 e_mean) to the precision allowed by e and comp overlapping in the same cells.
Also the excess is located: the share of the gravitating P excess at the k of max|P-1| that comes from the source auto- and cross-terms.
  nice -n 10 python3 cfg555_srccheck.py RUN [RUN ...]   (cache names from cfg555_compute.py) -> cfg555_srccheck.json / .out (appended per run)"""
import os, sys, json, time
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import cfg555_compute as CC
OUTJ = os.path.join(HERE, "cfg555_srccheck.json")

def check(name):
    spec, s0base = CC.RUNS[name]
    mod = CC.load_engine(spec); mesh = mod.Mesh(spec["N"]); dta = mod.dta_table()
    js = json.load(open(spec["base"] + ".json"))["snap"]["z0"]
    pos = np.load(spec["base"] + "_z0.npz")["pos"].astype(np.float64); npart = pos.shape[0]
    delta = mesh.deposit(pos); del pos
    rec = []; inv0 = mesh.inv
    def inv_rec(xk):
        rec.append(xk); del rec[:-3]
        return inv0(xk)
    mesh.inv = inv_rec
    _, info = mod.forces(mesh, delta, 1.0, spec["switch"], spec["branch"], spec["foot"], dta, diag=True)
    mesh.inv = inv0
    num = sum(kv * x for kv, x in zip(mesh.kvec, rec)); del rec
    dgk = (-num / (1j * 1.5 * mod.Om)).astype(np.complex64); del num; dgk[0, 0, 0] = 0
    src = ((mesh.inv(dgk) - delta) * 1.5 * mod.Om).astype(np.float64).ravel(); del dgk   # engine units (a = 1)
    cm = mod._INC["catch"]; r, nc = mod.catch_labels(cm); mm = r >= 0
    out_abs = float(np.abs(src[~mm]).sum()); tot_abs = float(np.abs(src).sum())
    S = np.bincount(r[mm], weights=src[mm], minlength=nc); A = np.bincount(r[mm], weights=np.abs(src[mm]), minlength=nc)
    Pp = np.bincount(r[mm], weights=np.maximum(src[mm], 0), minlength=nc)
    big = A > 1e-3 * A.max()
    esum = float(js.get("e_sum", js["e_mean"] * spec["N"] ** 3))
    res = dict(name=name, N=spec["N"], n_catch=int(nc), outside_abs_share=out_abs / tot_abs,
               max_abs_catch_sum_over_catch_abs=float(np.max(np.abs(S[big]) / A[big])),
               total_sum_over_total_abs=float(src.sum() / tot_abs), positive_part_sum=float(Pp.sum()), engine_e_sum=esum,
               positive_over_e_sum=float(Pp.sum() / esum))
    # where the excess comes from: P_grav - P_part = P_src + 2 P_cross at the k of the max deviation (k <= 1)
    dsrc = (src / (1.5 * mod.Om)).reshape(delta.shape).astype(np.float32)
    kb, pp, _ = mod.measure_pk(mesh, delta, npart); _, ps, _ = mod.measure_pk(mesh, dsrc, npart)
    _, pg, _ = mod.measure_pk(mesh, (delta + dsrc).astype(np.float32), npart)
    s0 = json.load(open(s0base + ".json"))["snap"]["z0"]; k = np.array(kb); m = k <= 1.0
    rg = np.array(pg) / np.interp(k, s0["k"], s0["P"]); i = int(np.argmax(np.abs(rg[m] - 1)))
    kk = k[m][i]; j = int(np.nonzero(k == kk)[0][0])
    res.update(k_at_max=float(kk), r_grav=float(rg[j]), r_part=float(pp[j] / np.interp(kk, s0["k"], s0["P"])),
               Psrc_over_PS0=float(ps[j] / np.interp(kk, s0["k"], s0["P"])),
               twoPcross_over_PS0=float((pg[j] - pp[j] - ps[j]) / np.interp(kk, s0["k"], s0["P"])),
               corr_coeff_src_part=float((pg[j] - pp[j] - ps[j]) / (2 * np.sqrt(pp[j] * ps[j]))))
    return res

if __name__ == "__main__":
    try: os.nice(10)
    except OSError: pass
    allr = json.load(open(OUTJ)) if os.path.exists(OUTJ) else {}
    for n in sys.argv[1:]:
        t0 = time.time(); allr[n] = check(n); allr[n]["runtime_s"] = time.time() - t0
        print(json.dumps(allr[n]), flush=True)
        json.dump(allr, open(OUTJ, "w"), indent=1)
    lines = []
    for n, v in allr.items():
        lines.append(f"{n} (N {v['N']}, {v['n_catch']} catchments): outside-catchment |src| share {v['outside_abs_share']:.1e}; max per-catchment |sum|/sum|src| "
                     f"{v['max_abs_catch_sum_over_catch_abs']:.1e}; positive part / engine Sum e {v['positive_over_e_sum']:.4f}; at k {v['k_at_max']:.2f}: r_grav {v['r_grav']:.4f} "
                     f"= r_part {v['r_part']:.4f} + P_src/P_S0 {v['Psrc_over_PS0']:.4f} + 2P_cross/P_S0 {v['twoPcross_over_PS0']:.4f} (corr {v['corr_coeff_src_part']:.3f})")
    open(os.path.join(HERE, "cfg555_srccheck.out"), "w").write("\n".join(lines) + "\n"); print("\n".join(lines))
