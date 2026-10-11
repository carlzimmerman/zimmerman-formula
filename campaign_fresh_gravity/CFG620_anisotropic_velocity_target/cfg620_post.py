#!/usr/bin/env python3
"""CFG620 post-run diagnostics (written after the main run started; no label is changed by this script, it only checks two
numerical points the main run raised). Dated 2026-10-10.

D1: the Part N solver for cluster_alt stopped at the frozen-code iteration cap (400 Newton steps) with bin error 1.9e-3 > 1e-3.
    Re-solve the same problem with a higher cap (same code path) and report the error and the change in the moments.
D2: the LP ISO test found locally isotropic second moments feasible in the compact hollow at 120 bins (d_min 0 / 0.024).
    Extract the t = 0 LP solution and rebuild its density on a 4x finer grid (as the main script does for the ME target), to see
    whether it is a smooth density or a binning artefact (sub-bins emptied). Also repeat the feasibility LP with 240 bins.
kappa = 1/2 FITTED; cold energy mass required; not "theory closed".
"""
import os, sys, json, math, warnings
import numpy as np
warnings.filterwarnings("ignore", message=".*encountered in matmul.*")
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import cfg620 as C
import cfg620_lib as L
from scipy.optimize import linprog

OUT = []; RES = {"lane": "CFG620", "script": "cfg620_post.py", "date": "2026-10-10"}


def log(s=""):
    print(s, flush=True); OUT.append(s)


cells = C.all_cells()
# ---- D1
d1 = {}
for k in ("cluster_can", "cluster_alt"):
    c = cells[k]
    T0 = C.toy_target(c)
    lib, M = T0["lib"], T0["M"]
    s1 = L.maxent(lib, M, itmax=3000, gis=30000)
    s2r, s2t, beta, _, _ = L.moments(lib, s1["y"], M)
    rc = T0["rc"]; sh = (rc > 0.1) & (rc < 0.9)
    d1[k] = dict(err_frozen_cap=T0["sol"]["err"], err_high_cap=s1["err"], it=s1["it"],
                 max_abs_dbeta_shell=float(np.max(np.abs(beta[sh] - T0["beta"][sh]))),
                 max_rel_ds2r=float(np.max(np.abs(s2r / T0["s2r"] - 1))), max_rel_ds2t=float(np.max(np.abs(s2t / T0["s2t"] - 1))),
                 beta_shell_median_high_cap=float(np.median(beta[sh])))
    log(f"D1 {k}: bin err {d1[k]['err_frozen_cap']:.2e} (cap 400) -> {d1[k]['err_high_cap']:.2e} ({s1['it']} it); "
        f"max |d beta| shell {d1[k]['max_abs_dbeta_shell']:.2e}; max rel d s2r {d1[k]['max_rel_ds2r']:.2e}, d s2t {d1[k]['max_rel_ds2t']:.2e}")
RES["D1"] = d1

# ---- D2
d2 = {}
for k in ("compact_can", "compact_alt", "cluster_can"):
    c = cells[k]; b = c["b_over_rM"]; R = 1.0 / c["Mb"]
    Mb, Mph, g = C.law_S(b, R)
    rho = lambda r: np.gradient(Mph(r), r) / np.asarray(r) ** 2
    rlo = C.lib_floor(rho, 0.005, R)
    rec = {}
    for nb in (120, 240):
        F = L.Field(g, rlo, R); lib = L.Library(F, rlo, R, nb=nb, sub=2)
        M = L.bin_masses(lib, Mph)
        rc = np.exp(0.5 * (lib.ub[1:] + lib.ub[:-1])); rb = M / np.diff(np.exp(lib.ub) ** 3)
        kpk = int(np.argmax(np.where(rc >= 0.05, rb, -1))); hol = np.where((rc >= 0.05) & (rc < rc[kpk]))[0]
        nc = lib.P.shape[0]
        A = ((lib.Vt[:, hol] - 2 * lib.Vr[:, hol]).T) / M[hol][:, None]
        res = linprog(np.zeros(nc), A_eq=np.vstack([(lib.P / M[None, :]).T, A]),
                      b_eq=np.concatenate([np.ones(M.size), np.zeros(hol.size)]), bounds=(0, None), method="highs",
                      options=dict(time_limit=300.0))
        o = dict(status=int(res.status), feasible=bool(res.status == 0), n_hollow_bins=int(hol.size))
        if res.status == 0:
            ubf, Mf = C.fine_recon(dict(lib=lib, sol=dict(y=res.x)), nsub=4)
            Mt = np.diff(Mph(np.exp(ubf))); rf = np.exp(0.5 * (ubf[1:] + ubf[:-1]))
            sel = (rf >= 0.05) & (rf < rc[kpk])
            dl = np.log10(np.maximum(Mf[sel], 1e-300) / Mt[sel])
            me = L.maxent(lib, M); ubf2, Mf2 = C.fine_recon(dict(lib=lib, sol=me), nsub=4)
            dl2 = np.log10(np.maximum(Mf2[sel], 1e-300) / Mt[sel])
            o.update(LP_fine_dlog_min=float(dl.min()), LP_fine_dlog_max=float(dl.max()),
                     LP_fine_subbins_below_minus1dex=int(np.sum(dl < -1)), n_fine_subbins=int(sel.sum()),
                     ME_fine_dlog_min=float(dl2.min()), ME_fine_dlog_max=float(dl2.max()))
        rec[str(nb)] = o
        log(f"D2 {k} nb {nb}: isotropic-moment LP in the hollow {'FEASIBLE' if o['feasible'] else 'infeasible'} (status {res.status}); "
            + (f"LP solution fine-grid log10(M/M_law) in [{o['LP_fine_dlog_min']:.2f}, {o['LP_fine_dlog_max']:.2f}], "
               f"{o['LP_fine_subbins_below_minus1dex']}/{o['n_fine_subbins']} sub-bins below -1 dex; ME target "
               f"[{o['ME_fine_dlog_min']:.2f}, {o['ME_fine_dlog_max']:.2f}]" if o["feasible"] else ""))
    d2[k] = rec
RES["D2"] = d2
json.dump(RES, open(os.path.join(HERE, "cfg620_post.json"), "w"), indent=1)
open(os.path.join(HERE, "cfg620_post.out"), "w").write("\n".join(OUT) + "\n")
