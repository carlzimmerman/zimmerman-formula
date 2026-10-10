#!/usr/bin/env python3
"""CFG544 post-freeze diagnostics (reported, not verdict inputs; dated 2026-10-10).

(1) Whole-history energy bookkeeping for the FIX-2 settled-state runs: CFG541's drift-only settling from rest releases dW per
    M_cat (cfg541_results.json `dW_over_Vf2`); FIX-2 then takes energy back from the sink to heat the settled halo to its Jeans
    state (cfg544_results.json, fix2_C net sink). Net = dW + net_sink(fix2_C), compared with CFG541's E_sink.
(2) Edge of the FIX-2 end states: ln(r99 / r99_analytic).
(3) Overfill under FIX-2 (two-sided + OU), same injection and pairing as the frozen overfill test, 5 Gyr.
Run: OMP_NUM_THREADS=2 nice -n 10 python3 cfg544_post.py   (reads cfg544_results.json; writes cfg544_post.out/.json)
"""
import os, json
os.environ.setdefault("OMP_NUM_THREADS", "1")
from multiprocessing import Pool
import cfg544 as M

HERE = os.path.dirname(os.path.abspath(__file__))
R = json.load(open(os.path.join(HERE, "cfg544_results.json")))
J541 = M.J541
OUT, RES = [], {"lane": "CFG544", "post_freeze": True, "date": "2026-10-10"}


def log(s=""):
    print(s, flush=True); OUT.append(s)


def main():
    cells = {f"{s}_{f}": M.make_cell(s, f) for s in M.SYS for f in M.FOOT}
    en = {}
    for k, c in cells.items():
        j = J541["one_d"][c["foot"]][c["sys"]]
        ns = R["runs"][f"{k}|fix2_C"]["final"]["sink_cum_over_Vf2Mcat"]
        en[k] = dict(dW_settle_CFG541=j["dW_over_Vf2"], fix2_C_net_sink=ns, whole_history_net=j["dW_over_Vf2"] + ns,
                     Esink_CFG541=j["Esink_over_Vf2"], Kf_CFG541=j["Kf_over_Vf2"])
        log(f"{k}: drift-only release {j['dW_over_Vf2']:.3f} + FIX-2 reheating {ns:+.3f} = net {j['dW_over_Vf2'] + ns:.3f} V_f^2 per M_cat "
            f"(CFG541 E_sink {j['Esink_over_Vf2']:.3f}, K_f {j['Kf_over_Vf2']:.3f})")
    RES["energy_whole_history"] = en
    edge = {}
    for k in cells:
        ra = R["cells"][k]["r99_analytic"]
        edge[k] = {nm: float(__import__("math").log(R["runs"][f"{k}|{nm}"]["final"]["r99"] / ra))
                   for nm in ("fix2_B", "fix2_C", "C2_vlasov_eq", "fix1_B", "asis_B")}
        log(f"{k}: ln(r99/r99_analytic) " + ", ".join(f"{a} {b:+.3f}" for a, b in edge[k].items()))
    RES["edge_dln_r99"] = edge
    jobs = []
    for k, c in cells.items():
        jobs += [dict(c=c, name=f"{k}|over_fix2_base", ic="E", rule="two", ou=True, T=5.0),
                 dict(c=c, name=f"{k}|over_fix2_inj", ic="E", rule="two", ou=True, T=5.0, inject=True)]
    with Pool(2) as pool:
        out = pool.map(M.run, jobs, chunksize=1)
    runs = {o["name"]: o for o in out}
    P = {}
    for k, c in cells.items():
        inj, base = runs[f"{k}|over_fix2_inj"], runs[f"{k}|over_fix2_base"]
        Mi = (inj["n_particles"] - base["n_particles"]) * c["Mcat"] / M.NPART
        P[k] = (inj["final"]["excess_in_rstar"] - base["final"]["excess_in_rstar"]) / Mi
        log(f"{k}: overfill under FIX-2, P(5 Gyr) = {P[k]:+.3f}; base D {base['final']['D']:+.3f} logX {base['final']['logX']:+.3f}; "
            f"inj D {inj['final']['D']:+.3f} logX {inj['final']['logX']:+.3f}")
    RES["overfill_fix2_P"] = P
    RES["overfill_fix2_runs"] = {nm: dict(final={kk: o["final"][kk] for kk in ("logX", "D", "Mc_in_rstar_over_Mph", "r99", "excess_in_rstar")},
                                          gate=o["gate"], series=o["series"]) for nm, o in runs.items()}
    return 0


if __name__ == "__main__":
    rc = main()
    open(os.path.join(HERE, "cfg544_post.out"), "w").write("\n".join(OUT) + "\n")
    json.dump(RES, open(os.path.join(HERE, "cfg544_post.json"), "w"), indent=1)
    raise SystemExit(rc)
