#!/usr/bin/env python3
"""CFG726 POST-HOC control diagnosis (not frozen, no verdict weight): where the failed controls bite.
(a) M-ADD eRASS1: radial range where the additive-law excess E > 0 (members as R_e 15 kpc Hernquists vs the smooth co-distributed
    stellar profile of the harness), for 12 clusters spanning the sample; (b) eFEDS: which groups break M0 / M-ADD and the stack-level
    size of each; T-E re-scored with the shape-mismatch groups' H-MM set to the law (does any T-E label move?).
Run from the repository root:  OMP_NUM_THREADS=1 nice -n 10 python3 campaign_fresh_gravity/CFG726_merger_memory/cfg726_control_diag.py"""
import os, sys, json, math
import numpy as np
os.environ["CFG726_MODE"] = "none"
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import cfg726 as C                                                     # noqa: E402  (MODE none: library only)
out = {}
d = np.load(os.path.join(C.LANES, "CFG687_erass1_shear_stack", "cfg687_percluster.npz"))
lamj = json.load(open(os.path.join(C.WORK, "lambda.json")))
rows = []
for i in np.linspace(0, len(d["mg"]) - 1, 12).astype(int):
    Mg = C.erass_gas(i, d); Mb = 1.2 * Mg; Mstar = 0.2 * float(Mg[-1]); N = max(1, int(round(lamj["Nmem"][i])))
    T = C.law_M(Mb, "canonical", C.nu_add) - Mb
    h, rt, xe = C.prog_halo(C.R_OBS, C.M652.hern(C.R_OBS, 1.0, C.RE_GAL), Mstar / N, float(d["z"][i]), C.A0K["canonical"], C.nu_add)
    Ncum = np.interp(C.DK / 1000.0, C.RGRID, Mg) / Mg[-1]
    Cm = N * C.convolve_members(C.DK, Ncum, C.R_OBS, h, C.RK_GRID)
    E = np.maximum(Cm - T, 0.0); k = np.where(E > 0)[0]
    rows.append(dict(i=int(i), r_max_kpc=float(C.RK_GRID[k].max()) if len(k) else 0.0, max_E_msun=float(E.max()), T_at_first_node=float(T[0]), M_b_at_first_node=float(Mb[0]), r_first_node_kpc=float(C.RK_GRID[0]),
                     E_over_Mb_150kpc=float(np.interp(150.0, C.RK_GRID, E) / np.interp(150.0, C.RK_GRID, Mb))))
    print(f"  M-ADD eRASS1 cluster {i}: E>0 out to {rows[-1]['r_max_kpc']:.1f} kpc; max E {rows[-1]['max_E_msun']:.2e} Msun (T and M_b at the first grid node {rows[-1]['r_first_node_kpc']:.2f} kpc = {rows[-1]['T_at_first_node']:.1e} / {rows[-1]['M_b_at_first_node']:.1e}); E/M_b at 150 kpc {rows[-1]['E_over_Mb_150kpc']:.1e}")
out["MADD_erass"] = rows
W = os.path.join(C.EXT, "cfg652_work")
I = np.load(os.path.join(W, "cfg652_inputs.npz")); MD = np.load(os.path.join(W, "cfg652_models.npz")); EM = np.load(os.path.join(C.WORK, "efeds.npz"))
keep = I["Mcond"] > 0; idx = np.where(keep)[0]
r0 = np.nanmax(np.abs(EM["base__c540__canonical"][keep] / MD["canonical__x1__b"][keep] - 1), 1)
ra = np.nanmax(np.abs(EM["hmm__add__canonical"][keep] / EM["base__add__canonical"][keep] - 1), 1)
fb = I["Mbcg"][keep] / I["Mcond"][keep]
out["efeds_M0_groups_over_2pct"] = int((r0 > 0.02).sum()); out["efeds_M0_worst"] = dict(group=int(idx[np.argmax(r0)]), rel=float(r0.max()), Mhot=float(I["Mhot"][idx[np.argmax(r0)]]))
out["efeds_M0_second"] = float(np.sort(r0)[-2])
out["efeds_MADD_groups"] = int((ra > 1e-12).sum()); out["efeds_MADD_groups_with_Mbcg_over_half"] = int(((ra > 1e-12) & (fb > 0.5)).sum())
print(f"  eFEDS M0: {out['efeds_M0_groups_over_2pct']} of {keep.sum()} groups > 2%; worst group {out['efeds_M0_worst']} ; second {out['efeds_M0_second']:.3f}")
print(f"  eFEDS M-ADD: {out['efeds_MADD_groups']} groups with nonzero additive excess, of which {out['efeds_MADD_groups_with_Mbcg_over_half']} have M_bcg/M_cond > 0.5 "
      f"(CFG652's profile puts 0.5 M_cond in the BCG; the frozen progenitor rule puts M_bcg there)")
WW = np.load(os.path.join(W, "cfg652_esd.npz"))["WW"][keep]
for kern in ("s", "mono"):
    for foot in ("canonical", "alt"):
        h = EM[f"hmm__{kern}__{foot}"][keep].copy(); b = EM[f"base__{kern}__{foot}"][keep]
        stack_h = (WW * h).sum(0) / WW.sum(0); bad = ra > 1e-12; h[bad] = b[bad]; stack_c = (WW * h).sum(0) / WW.sum(0); stack_b = (WW * b).sum(0) / WW.sum(0)
        out[f"efeds_stack|{kern}|{foot}"] = dict(hmm_over_law=(stack_h / stack_b).tolist(), cleaned_over_law=(stack_c / stack_b).tolist())
        print(f"  eFEDS {kern} {foot[:3]}: stack H-MM/law per bin " + " ".join(f"{x:.3f}" for x in stack_h / stack_b) + " | shape-mismatch groups reset: "
              + " ".join(f"{x:.3f}" for x in stack_c / stack_b))
json.dump(out, open(os.path.join(HERE, "cfg726_control_diag.json"), "w"), indent=1)
