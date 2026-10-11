#!/usr/bin/env python3
"""CFG626 side-by-side (exponential = CFG620's committed JSON; repaired nu_mono = this lane) and the kernel-robust /
kernel-dependent verdict per headline, per footing (FROZEN_CRITERIA.md 1c69c8300). Reads JSON only; writes cfg626_compare.json/.out.
kappa = 1/2 FITTED; footings never pooled; cold energy mass required; not "theory closed".
"""
import os, json, math
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
D620 = os.path.join(HERE, "..", "CFG620_anisotropic_velocity_target")
E = json.load(open(os.path.join(D620, "cfg620_results.json")))
EM = json.load(open(os.path.join(D620, "cfg620_results_MUTATE.json")))
M = json.load(open(os.path.join(HERE, "cfg626_results_mono.json")))
MM = json.load(open(os.path.join(HERE, "cfg626_results_mono_MUTATE.json")))
CR = json.load(open(os.path.join(HERE, "cfg626_crep.json")))
FEET = ("can", "alt")
OUT = []; RES = dict(lane="CFG626", criteria_commit="1c69c8300", C_REP_pass=CR["C_REP_pass"], C_REP_fails=CR["fails"])


def log(s=""):
    print(s); OUT.append(s)


def cells_f(f):
    return [f"MW_{f}", f"cluster_{f}", f"compact_{f}"]


def hol_f(f):
    return [f"cluster_{f}", f"compact_{f}"]


def rd(J, k, ic, al=1.0, t=None):
    t = t or ("10.0" if ic == "B" else "5.0")
    return J["runs"][f"{k}|A_{ic}_a{al}"]["reads"][t]


def own_hollow(J, k, mono):
    if mono:
        return bool(J["partS"][k]["hollow"]), J["cfg626"]["hollow_own_kernel"][k] is not None
    return bool(J["partS"][k]["hollow"]), J["cells"][k]["r_pk_toy"] is not None


def beta_inner(J, k):
    """median Part S beta over 0.05 r_M <= r < r_pk,exp (r_M units)."""
    rp = E["partS"][k]["r_pk_over_rM"]
    if rp is None:
        return None
    p = J["partS"][k]["profile"]; r = np.array(p["r"]); b = np.array(p["beta"])
    m = (r >= 0.05) & (r < rp)
    return float(np.median(b[m])) if m.any() else None


def lp_inner(J, k):
    s = J["partS"][k]
    if E["partS"][k]["r_pk_over_rM"] is None:
        return s["LP_ISO_hollow_dmin"]
    return s["LP_ISO_hollow_dmin"] if s["hollow"] else s["LP_ISO_outer_dmin"]


def label_f(J, f):
    """CFG620's label rules restricted to one footing's three cells."""
    V = J["verdict_detail"]; ks = cells_f(f); hk = [k for k in ks if k in V["hollow_held"]]
    sc = all(J["partS"][k]["self_consistent"] and J["partN"][k]["self_consistent"] for k in ks)
    g550 = all(V["G550_alpha1"][k] for k in ks); blow = any(V["blow_up"][k] for k in ks)
    en = all(0 <= V["energy_B_net"][k] <= 1 and 0 <= V["energy_C_whole"][k] <= 1 for k in ks)
    hold = all(V["hollow_held"][k] for k in hk)
    sym = J["sympy"]["K1_K5_pass"]
    tgt = "ANISOTROPIC TARGET DERIVED" if (sc and sym and g550 and not blow and en and hold) else (
        "INCONSISTENT" if ((not sc) or (not g550) or blow or (not en) or (not hold)) else "POSITED")
    edge = "SHARP" if all(abs(V["edge_FIXA"][k]["B"]) <= 0.1 and abs(V["edge_FIXA"][k]["C"]) <= 0.1 for k in ks) else "SOFTENED"
    comp = [k for k in ks if not k.startswith("MW")]
    works = "YES" if all(V["G550_alpha1"][k] and not V["blow_up"][k] and V["hollow_held"].get(k, True) for k in comp) else "NO"
    over = "HANDLED" if all(V["overfill_P"][k] <= 0.2 for k in ks) else "NOT HANDLED"
    rob = all(v["pass_"] for kk, v in V["alpha"].items() if kk.split("|")[0] in ks)
    return dict(target=tgt, edge=edge, works_in_compact=works, overfill=over, alpha="alpha-ROBUST" if rob else "NOT alpha-ROBUST")


def headlines(J, f, mono):
    V = J["verdict_detail"]; ks = cells_f(f); hk = hol_f(f); h = {}
    h["1_hollow_exists"] = {k: own_hollow(J, k, mono) for k in hk}
    h["2_held"] = {k: dict(held=V["hollow_held"][k], H_B=V["hollow_detail"][k]["B"]["H"], H_C=V["hollow_detail"][k]["C"]["H"],
                           sH_B=V["hollow_detail"][k]["B"]["sH"], FIX2_H=V["hollow_FIX2"][k],
                           FIX2_overfill=bool(max(x for x in V["hollow_FIX2"][k].values() if x is not None) >= 0.3)) for k in hk}
    h["3_anisotropy"] = {k: dict(beta_inner=(J["partS"][k]["beta_hollow_median"] if not mono else beta_inner(J, k)),
                                 beta_bulk=J["partS"][k]["beta_bulk_median"],
                                 edge_sr2_st2=J["partS"][k]["edge_sr2_over_st2_last_bin"],
                                 LP_ISO_inner=(J["partS"][k]["LP_ISO_hollow_dmin"] if not mono else lp_inner(J, k))) for k in ks}
    h["4_edge"] = dict(frozen={k: (V["edge_FIXA"][k]["B"], V["edge_FIXA"][k]["C"]) for k in ks},
                       t138_a1_a2={kk: v["dln_r99"] for kk, v in V["alpha"].items()
                                   if kk.split("|")[0] in ks and kk.split("|")[2] in ("a1.0", "a2.0")})
    h["5_G550"] = {k: (rd(J, k, "B")["G550"], rd(J, k, "C")["G550"]) for k in ks}
    h["5_G550_detail"] = {k: dict(B=(rd(J, k, "B")["d_D_last2"], rd(J, k, "B")["d_logXJ_last2"]),
                                  C=(rd(J, k, "C")["d_D_last2"], rd(J, k, "C")["d_logXJ_last2"])) for k in ks}
    h["6_t138_a_ge1"] = {kk: v["pass_"] for kk, v in V["alpha"].items() if kk.split("|")[0] in ks and kk.split("|")[2] in ("a1.0", "a2.0")}
    h["7_a05_B_edge"] = {k: V["alpha"][f"{k}|B|a0.5"]["dln_r99"] for k in ks}
    h["7_a05_all"] = {kk: v["pass_"] for kk, v in V["alpha"].items() if kk.split("|")[0] in ks and kk.endswith("a0.5")}
    h["8_overfill_P"] = {k: V["overfill_P"][k] for k in ks}
    h["9_kids_sharp_branch"] = all(abs(v) <= 0.1 for v in h["4_edge"]["t138_a1_a2"].values())
    h["labels"] = label_f(J, f)
    h["extra"] = dict(rstar_kpc={k: J["cells"][k]["rstar_kpc"] for k in ks}, C4={k: J["cells"][k]["C4"] for k in ks},
                      energy_B={k: V["energy_B_net"][k] for k in ks}, energy_C={k: V["energy_C_whole"][k] for k in ks},
                      blow={k: V["blow_up"][k] for k in ks}, edge_FIX2=V["edge_FIX2"], edge_FIXAG=V["edge_FIXAG"],
                      H_FIXAG={k: V["hollow_AG"].get(k) for k in hk},
                      partS_sc={k: (J["partS"][k]["self_consistent"], J["partS"][k]["solver_err"]) for k in ks},
                      partN_sc={k: (J["partN"][k]["self_consistent"], J["partN"][k]["solver_err"]) for k in ks},
                      beta_shell_partN={k: J["partN"][k]["beta_shell_median"] for k in ks},
                      LP_MIRROR={k: (J["partS"][k]["LP_MIRROR_dmin"], J["partS"][k]["LP_MIRROR_hollow_dmin"]) for k in ks})
    return h


def verdicts(e, m, f):
    v = {}
    hk = hol_f(f)
    v["1_hollow_exists"] = all(all(m["1_hollow_exists"][k]) for k in hk)
    v["2_held"] = all(e["2_held"][k]["held"] and m["2_held"][k]["held"] and e["2_held"][k]["FIX2_overfill"] and m["2_held"][k]["FIX2_overfill"]
                      for k in hk)
    a3 = []
    for k in hk:
        be, bm = e["3_anisotropy"][k]["beta_inner"], m["3_anisotropy"][k]["beta_inner"]
        ratio = (bm / be) if (be not in (None, 0) and bm is not None) else None
        a3.append(bm is not None and bm < 0 and ratio is not None and 0.5 <= ratio <= 2.0)
        a3.append((e["3_anisotropy"][k]["LP_ISO_inner"] <= 0.02) == (m["3_anisotropy"][k]["LP_ISO_inner"] <= 0.02))
    for k in cells_f(f):
        a3.append(abs(e["3_anisotropy"][k]["beta_bulk"]) <= 0.1 and abs(m["3_anisotropy"][k]["beta_bulk"]) <= 0.1)
        a3.append(e["3_anisotropy"][k]["edge_sr2_st2"] <= 0.05 and m["3_anisotropy"][k]["edge_sr2_st2"] <= 0.05)
    v["3_anisotropy"] = all(a3)
    v["4_edge"] = (e["labels"]["edge"] == m["labels"]["edge"]) and all(abs(x) <= 0.1 for x in e["4_edge"]["t138_a1_a2"].values()) \
        and all(abs(x) <= 0.1 for x in m["4_edge"]["t138_a1_a2"].values())
    v["5_G550_pattern"] = e["5_G550"] == m["5_G550"]
    v["5_target_label"] = e["labels"]["target"] == m["labels"]["target"]
    v["6_t138_a_ge1"] = all(e["6_t138_a_ge1"].values()) and all(m["6_t138_a_ge1"].values())
    v["7_alpha"] = (e["labels"]["alpha"] == m["labels"]["alpha"]) and all(x > 0.1 for x in e["7_a05_B_edge"].values()) \
        and all(x > 0.1 for x in m["7_a05_B_edge"].values())
    v["8_overfill"] = e["labels"]["overfill"] == m["labels"]["overfill"]
    v["9_kids"] = e["9_kids_sharp_branch"] == m["9_kids_sharp_branch"]
    return v


def main():
    log("CFG626 kernel re-check of CFG620: exponential (CFG620 JSON) vs repaired nu_mono (this lane)")
    log(f"C-REP (exp through the CFG626 driver vs CFG620): {'PASS' if CR['C_REP_pass'] else 'FAIL'}; "
        f"max run dev {max(v['max_abs_dev'] for v in CR['runs'].values()):.1e} over {len(CR['runs'])} runs; "
        f"cells max rel dev {max(v['max_rel_dev'] for v in CR['cells'].values()):.1e}; dW max rel dev {max(CR['dW'].values()):.1e}")
    log(f"kernel check: {json.dumps(M['cfg626']['kernel_check'])}")
    RES["per_footing"] = {}
    for f in FEET:
        e, m = headlines(E, f, False), headlines(M, f, True)
        v = verdicts(e, m, f)
        RES["per_footing"][f] = dict(exp=e, mono=m, robust=v)
        log(f"\n===== footing {f} =====")
        for name in ("1_hollow_exists", "2_held", "3_anisotropy", "5_G550", "5_G550_detail", "6_t138_a_ge1", "7_a05_B_edge", "7_a05_all",
                     "8_overfill_P", "9_kids_sharp_branch", "labels"):
            log(f"  {name}:\n     exp  {json.dumps(e[name])}\n     mono {json.dumps(m[name])}")
        log(f"  4_edge frozen:\n     exp  {json.dumps(e['4_edge']['frozen'])}\n     mono {json.dumps(m['4_edge']['frozen'])}")
        log(f"  4_edge 13.8 Gyr a1/a2:\n     exp  {json.dumps(e['4_edge']['t138_a1_a2'])}\n     mono {json.dumps(m['4_edge']['t138_a1_a2'])}")
        for kk in ("rstar_kpc", "C4", "energy_B", "energy_C", "blow", "H_FIXAG", "partS_sc", "partN_sc", "beta_shell_partN", "LP_MIRROR"):
            log(f"  extra {kk}:\n     exp  {json.dumps(e['extra'][kk])}\n     mono {json.dumps(m['extra'][kk])}")
        log(f"  VERDICTS (True = KERNEL-ROBUST): {json.dumps(v)}")
    RES["labels_global"] = dict(exp=E["labels"], mono=M["labels"])
    RES["label_changes"] = {k: (E["labels"][k], M["labels"][k]) for k in E["labels"] if E["labels"][k] != M["labels"][k]}
    RES["controls"] = dict(exp={k: v for k, v in E["verdict_detail"]["controls"].items() if k not in ("C2p_detail", "C5_detail")},
                           mono={k: v for k, v in M["verdict_detail"]["controls"].items() if k not in ("C2p_detail", "C5_detail")},
                           CS_identical=all(abs(E["CS"][k] - M["CS"][k]) <= 1e-12 for k in ("bin_err", "maxdev_r_le_3", "maxdev_r_0p1_to_3")),
                           C2p_mono=M["verdict_detail"]["controls"]["C2p_detail"], C5_mono=M["verdict_detail"]["controls"]["C5_detail"])
    RES["MUTATE"] = dict(exp={k: (v["bites"] if isinstance(v, dict) else v) for k, v in EM["MUTATE"].items()},
                         mono={k: (v["bites"] if isinstance(v, dict) else v) for k, v in MM["MUTATE"].items()},
                         mono_detail=MM["MUTATE"])
    RES["lyapunov"] = dict(exp=E["verdict_detail"]["lyapunov_max_rise_F"], mono=M["verdict_detail"]["lyapunov_max_rise_F"])
    log(f"\nGlobal labels exp {json.dumps(E['labels'])}\n              mono {json.dumps(M['labels'])}")
    log(f"Label changes: {json.dumps(RES['label_changes'])}")
    log(f"Controls: {json.dumps(RES['controls'], default=str)}")
    log(f"MUTATE: exp {json.dumps(RES['MUTATE']['exp'])} / mono {json.dumps(RES['MUTATE']['mono'])}")
    log(f"MUTATE mono detail: {json.dumps(MM['MUTATE'], default=str)}")
    log(f"Lyapunov largest rise: {json.dumps(RES['lyapunov'])}")
    json.dump(RES, open(os.path.join(HERE, "cfg626_compare.json"), "w"), indent=1, default=str)
    open(os.path.join(HERE, "cfg626_compare.out"), "w").write("\n".join(OUT) + "\n")


if __name__ == "__main__":
    main()
