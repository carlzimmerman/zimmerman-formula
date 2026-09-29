#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CFG180 main + MUTATE: independent re-derivation of CFG170 (two-epoch gas-ratio test).  From CFG180_FROZEN_CRITERIA.md alone.
  python3 CFG180_two_epoch_referee.py            -> stdout (CFG180_main.out) + CFG180_main_results.json ; exit 0 iff C1, C2 pass (else 2)
  MUTATE=k python3 ...  (k = 1..6)                -> CFG180_MUTATE_k.out/_results.json ; exit 1 iff the control bites, 0 if not
Shared (not independent): the KURVS/KROSS/SPARC pipeline, imported read-only from CFG165's module (see CFG180_lib.py).
"""
import os
import sys
import json
import math
import time

import numpy as np

import CFG180_lib as L
M = L.M

MODE = os.environ.get("MUTATE", "0")
OUT = {"mode": MODE, "rows": {}, "checks": {}}
T0 = time.time()


def P(*a):
    print(L.scrub(" ".join(str(x) for x in a)), flush=True)


# ---------------------------------------------------------------- README targets (read, not predicted)
PLACE = (1.00, 1.42, 1.62, 1.69, 3.00)
T_MU = {  # s: (flat KURVS, flat KROSS, rival KURVS, rival KROSS) each (central, lo, hi); None = open/absent
    1.00: ((2.109, 1.596, 2.705), (0.636, 0.478, 0.805), (0.621, 0.289, 1.006), (0.052, None, 0.185)),
    1.42: ((3.096, 2.423, 3.887), (0.998, 0.820, 1.188), (1.257, 0.822, 1.766), (0.352, 0.211, 0.504)),
    1.62: ((3.565, 2.808, 4.462), (1.166, 0.979, 1.367), (1.567, 1.076, 2.144), (0.494, 0.344, 0.655)),
    1.69: ((3.730, 2.942, 4.665), (1.225, 1.035, 1.429), (1.676, 1.165, 2.279), (0.544, 0.391, 0.707)),
    3.00: ((6.845, 5.407, 8.611), (2.301, 2.050, 2.569), (3.829, 2.873, 4.994), (1.475, 1.267, 1.698)),
}
T_R = {  # s: (flat (R, lo, hi), rival (R, lo, hi)); hi None = open
    1.00: ((3.32, 1.98, 5.66), (11.9, 1.56, None)),
    1.42: ((3.10, 2.04, 4.74), (3.57, 1.63, 8.39)),
    1.62: ((3.06, 2.06, 4.56), (3.17, 1.64, 6.23)),
    1.69: ((3.04, 2.06, 4.51), (3.08, 1.65, 5.83)),
    3.00: ((2.97, 2.11, 4.20), (2.60, 1.69, 3.94)),
}
T_SEP = {1.42: 0.0613, 1.62: 0.0155, 1.69: 0.0057, 3.00: 0.0579}


def rel(a, b):
    return abs(a - b) / abs(b)


def build(mode):
    Su = L.get_kurvs("inc_star_deg")
    Sk = L.get_kross()
    AS = L.get_anchor()
    kw = {}
    note = ""
    if mode == "1":
        Su.V = Su.V * 10 ** 0.3
        Su.eV = Su.eV * 10 ** 0.3
        note = "KURVS V and eV x 10^0.3"
    elif mode == "2":
        kw["swap"] = True
        note = "laws swapped inside the break-even solver"
    elif mode == "3":
        Sk.R = Sk.Reff.copy()
        note = "KROSS radius R = r_im (x = 0)"
    elif mode == "6":
        kw["hi"] = 1.0
        note = "mu search range [0.01, 1.0]"
    return Su, Sk, AS, kw, note


def main():
    P("=" * 100)
    P(f"CFG180 referee re-derivation of CFG170.  MODE={MODE}.  repo=<repo>")
    P("=" * 100)
    Su, Sk, AS, kw, note = build(MODE)
    if note:
        P("MUTATION:", note)
    P(f"KURVS n={len(Su.R)}  KROSS n={len(Sk.R)}  SPARC anchor n={len(AS.R)}")

    # ------------------------------------------------ solve everything
    res = {}
    for s in (0.0,) + PLACE + (0.6, 1.4):
        res[s] = L.solve_pair(Sk, Su, AS, s, **kw)
    resB = {s: L.solve_pair(Sk, Su, AS, s, conv="B", **kw) for s in PLACE}

    # ------------------------------------------------ R_obs
    medzU, medzK = float(np.median(Su.z)), float(np.median(Sk.z))
    mU, mK = float(np.median(Su.logM)), float(np.median(Sk.logM))
    ro = L.robs(medzU, medzK, mU, mK)
    inb = ro["inrep"](2.0)
    litb = ro["litb"](L.LIT_ALLOW)
    P(f"\n-- R_obs: median z KURVS {medzU:.3f} KROSS {medzK:.3f}; median log M* KURVS {mU:.3f} KROSS {mK:.3f}; (1+z) ratio {ro['fz']:.4f}")
    P(f"   mass factors in-repo {ro['mass_in']:.4f}  literature {ro['mass_lit']:.4f}")
    P(f"   in-repo   R_obs = {ro['Rin']:.3f}   2 sigma bracket [{inb[0]:.3f}, {inb[1]:.3f}]")
    P(f"   literature R_obs = {ro['Rlit']:.3f}  (+-20%) bracket [{litb[0]:.3f}, {litb[1]:.3f}]  (ABSTRACT-LEVEL constants; INPUTS)")
    OUT["robs"] = dict(zU=medzU, zK=medzK, logMU=mU, logMK=mK, fz=ro["fz"], mass_in=ro["mass_in"], mass_lit=ro["mass_lit"],
                       Rin=ro["Rin"], in_bracket=inb, Rlit=ro["Rlit"], lit_bracket=litb)

    # ------------------------------------------------ controls
    P("\n-- controls (frozen C1, C2)")
    c1f = res[1.00]["flat"]["U"]["mu"]
    c1r = res[1.00]["H"]["U"]["mu"]
    ok1 = (c1f is not None and c1r is not None and abs(c1f - 2.109) < 1e-3 and abs(c1r - 0.621) < 1e-3)
    P(f"  [{'PASS' if ok1 else 'FAIL'}] C1 KURVS s=1 break-evens {c1f} / {c1r} vs 2.109 / 0.621 (1e-3)")
    cvK = res[1.00]["curves"][1]
    d67f, d67r = cvK.dp(0.67, "flat"), cvK.dp(0.67, "H")
    ok2 = abs(d67f - (-0.0042)) < 1e-3 and abs(d67r - (-0.0821)) < 1e-3
    P(f"  [{'PASS' if ok2 else 'FAIL'}] C2 KROSS anchor-corrected D' at mu=0.67, s=1: {d67f:+.4f} / {d67r:+.4f} vs -0.0042 / -0.0821 (1e-3)")
    OUT["checks"]["C1"] = dict(ok=bool(ok1), flat=c1f, rival=c1r)
    OUT["checks"]["C2"] = dict(ok=bool(ok2), flat=d67f, rival=d67r)

    # ------------------------------------------------ R0 (printed before the matrix)
    P("\n-- R0 power (before any comparison): |log10 R_flat - log10 R_rival|")
    sep = {}
    for s in PLACE:
        rf, rr = res[s]["flat"]["R"], res[s]["H"]["R"]
        if rf and rr:
            sep[s] = abs(math.log10(rf["R"]) - math.log10(rr["R"]))
            P(f"   s={s:4.2f}: {sep[s]:.4f} dex   (in-repo 2-sigma bracket log-width {math.log10(inb[1] / inb[0]):.3f} dex)")
    OUT["sep"] = sep

    # ------------------------------------------------ break-even table
    P("\n-- break-even gas fraction mu_be [1 sigma root interval, convention A: sigma frozen at the central root]")
    for s in (0.0,) + PLACE:
        r = res[s]
        P(f"  s={s:4.2f}  flat  KURVS {L.fmtB(r['flat']['U']):26s} KROSS {L.fmtB(r['flat']['K']):26s} | "
          f"rival KURVS {L.fmtB(r['H']['U']):26s} KROSS {L.fmtB(r['H']['K'])}")
    P("\n-- R_law = mu_be(KURVS)/mu_be(KROSS) [conservative interval]")
    for s in (0.0,) + PLACE + (0.6, 1.4):
        r = res[s]
        P(f"  s={s:4.2f}  flat {L.fmtR(r['flat']['R']):26s} rival {L.fmtR(r['H']['R'])}    nroots(U,K flat)={r['flat']['U']['nroots']},{r['flat']['K']['nroots']} (rival)={r['H']['U']['nroots']},{r['H']['K']['nroots']}")

    # ------------------------------------------------ matrix
    mat = {}
    P("\n-- disfavoured matrix (frozen rule; literal form / overlap form must agree)   [flat, rival] x [in-repo, literature]")
    forms_agree = True
    for s in PLACE:
        row = {}
        for law in L.LAWS:
            rl = res[s][law]["R"]
            for nm, br in (("in", inb), ("lit", litb)):
                if rl is None:
                    row[(law, nm)] = None
                    continue
                a = L.disfav_overlap(rl, br)
                b = L.disfav_literal(rl, br)
                if a != b:
                    forms_agree = False
                row[(law, nm)] = a
        mat[s] = row
        def w(x):
            return "n/a" if x is None else ("DISFAV" if x else "not")
        P(f"  s={s:4.2f}: in-repo flat {w(row[('flat','in')]):6s} rival {w(row[('H','in')]):6s} | literature flat {w(row[('flat','lit')]):6s} rival {w(row[('H','lit')])}")
    both1 = [law for law in L.LAWS if mat[1.00][(law, "in")] and mat[1.00][(law, "lit")]]
    label = "DIAGNOSTIC" if len(both1) == 1 else "NON-DIAGNOSTIC"
    P(f"  laws disfavoured by BOTH brackets at s=1: {[L.NAMES[x] for x in both1]}  ->  summary {label}")
    P(f"  literal form and overlap form agree in every cell: {forms_agree}")
    OUT["matrix"] = {str(s): {f"{k[0]}|{k[1]}": v for k, v in row.items()} for s, row in mat.items()}
    OUT["label"] = label
    OUT["forms_agree"] = forms_agree

    # ------------------------------------------------ extras / explanatory
    P("\n-- explanatory checks")
    for law in L.LAWS:
        bU, bK = res[1.00][law]["U"], res[1.00][law]["K"]
        if bU["mu"] and bK["mu"]:
            P(f"   s=1 {L.NAMES[law]}: R in (1+mu) = {(1 + bU['mu']) / (1 + bK['mu']):.3f}")
    d001 = cvK.at(0.01)["H"]
    P(f"   KROSS rival D' at mu=0.01, s=1: {d001[0]:+.4f} +- {d001[1]:.4f}")
    OUT["extra"] = dict(rival_dp001=d001[0], rival_dp001_sig=d001[1])

    # ------------------------------------------------ pass lines
    P("\n-- PASS LINES vs the CFG170 README targets (targets read, not predicted)")
    fails = []

    def line(tag, ok, txt):
        P(f"  [{'PASS' if ok else 'FAIL'}] {tag}: {txt}")
        OUT["checks"][tag] = dict(ok=bool(ok), text=txt)
        if not ok:
            fails.append(tag)

    if MODE == "0":
        # P2 central mu_be and s=0
        bad = []
        for s in PLACE:
            for col, (law, smp) in enumerate((("flat", "U"), ("flat", "K"), ("H", "U"), ("H", "K"))):
                t = T_MU[s][col][0]
                m = res[s][law][smp]["mu"]
                tol = 0.10 if (s == 1.00 and law == "H" and smp == "K") else 0.015
                ok = (m is not None) and (rel(m, t) <= tol or (tol == 0.10 and abs(m - t) <= 0.006))
                if not ok:
                    bad.append((s, law, smp, m, t))
        none0 = all(res[0.0][law][smp]["mu"] is None for law in L.LAWS for smp in ("U", "K"))
        line("P2 central mu_be (20 values, 1.5%; KROSS rival s=1 10%)", not bad and none0, f"misses: {bad}; s=0 all 'no break-even': {none0}")
        # P3 intervals
        for conv, rr in (("A", res), ("B", resB)):
            n = m_ok = 0
            miss = []
            open_ok = True
            for s in PLACE:
                for col, (law, smp) in enumerate((("flat", "U"), ("flat", "K"), ("H", "U"), ("H", "K"))):
                    tc, tlo, thi = T_MU[s][col]
                    b = rr[s][law][smp]
                    for val, t, nm in ((b["mu_lo"], tlo, "lo"), (b["mu_hi"], thi, "hi")):
                        if t is None:
                            if val is not None:
                                open_ok = False
                            continue
                        n += 1
                        if val is not None and rel(val, t) <= 0.04:
                            m_ok += 1
                        else:
                            miss.append((s, law, smp, nm, None if val is None else round(val, 3), t))
            frac = m_ok / n
            line(f"P3{conv} intervals (4%, >= 90% of {n} numeric edges, open edge identical)", frac >= 0.9 and open_ok,
                 f"{m_ok}/{n} within 4%; open edge ok {open_ok}; misses {miss}")
        # P4 R_law
        bad = []
        for s in PLACE:
            for law, (tR, tlo, thi) in zip(L.LAWS, T_R[s]):
                rl = res[s][law]["R"]
                if rl is None:
                    bad.append((s, law, "none"))
                    continue
                if rel(rl["R"], tR) > 0.02:
                    bad.append((s, law, "R", round(rl["R"], 3), tR))
                tolE = 0.05 if (s == 1.00 and law == "H") else 0.06
                if rel(rl["lo"], tlo) > tolE:
                    bad.append((s, law, "lo", round(rl["lo"], 3), tlo))
                if thi is None:
                    if math.isfinite(rl["hi"]):
                        bad.append((s, law, "hi should be open", rl["hi"]))
                elif rel(rl["hi"], thi) > 0.06:
                    bad.append((s, law, "hi", round(rl["hi"], 3), thi))
        line("P4 R_law centre 2%, edges 6% (rival s=1 lo 5%, hi open)", not bad, f"misses {bad}")
        # P5 R_obs
        ok = (abs(ro["Rin"] - 1.00) <= 0.02 and abs(inb[0] - 0.73) <= 0.03 and abs(inb[1] - 1.39) <= 0.03 and abs(ro["Rlit"] - 2.02) <= 0.03
              and abs(litb[0] - 1.61) <= 0.03 and abs(litb[1] - 2.42) <= 0.03 and abs(medzU - 1.53) <= 0.01 and abs(medzK - 0.85) <= 0.01
              and abs(mU - 10.14) <= 0.01 and abs(mK - 10.04) <= 0.01 and abs(ro["fz"] - 1.3669) <= 0.001
              and abs(ro["mass_in"] - 0.935) <= 0.005 and abs(ro["mass_lit"] - 0.923) <= 0.005)
        line("P5 R_obs numbers", ok, f"Rin {ro['Rin']:.3f} [{inb[0]:.3f},{inb[1]:.3f}] Rlit {ro['Rlit']:.3f} [{litb[0]:.3f},{litb[1]:.3f}] z {medzU:.3f}/{medzK:.3f} logM {mU:.3f}/{mK:.3f} fz {ro['fz']:.4f} mass {ro['mass_in']:.4f}/{ro['mass_lit']:.4f}")
        # P6 matrix
        exp_ok = all(mat[s][(law, "in")] is True and mat[s][(law, "lit")] is False for s in PLACE for law in L.LAWS)
        line("P6 matrix exact (in-repo disfavours both at every s; literature neither), summary NON-DIAGNOSTIC, two forms agree",
             exp_ok and label == "NON-DIAGNOSTIC" and forms_agree, f"matrix ok {exp_ok}; label {label}; forms agree {forms_agree}")
        # P7 s=0.6/1.4
        r06, r14 = res[0.6], res[1.4]
        ok7 = (r06["flat"]["R"] is not None and rel(r06["flat"]["R"]["R"], 4.26) <= 0.03 and r06["H"]["R"] is None
               and r14["flat"]["R"] is not None and rel(r14["flat"]["R"]["R"], 3.11) <= 0.03
               and r14["H"]["R"] is not None and rel(r14["H"]["R"]["R"], 3.63) <= 0.04)
        line("P7 calibration-scatter rows (4.26, none, 3.11, 3.63)", ok7,
             f"s=0.6 flat {L.fmtR(r06['flat']['R'])} rival {L.fmtR(r06['H']['R'])}; s=1.4 flat {L.fmtR(r14['flat']['R'])} rival {L.fmtR(r14['H']['R'])}")
        # P8 R0
        ok8 = abs(sep[1.00] - 0.56) <= 0.02 and all(abs(sep[s] - T_SEP[s]) <= 0.01 for s in T_SEP)
        line("P8 R0 (0.56 dex at s=1; 0.01-0.06 at s>=1.42, +-0.01)", ok8, f"{ {k: round(v, 4) for k, v in sep.items()} }")
        # P9
        r19f = (1 + res[1.0]["flat"]["U"]["mu"]) / (1 + res[1.0]["flat"]["K"]["mu"])
        r19r = (1 + res[1.0]["H"]["U"]["mu"]) / (1 + res[1.0]["H"]["K"]["mu"])
        ok9 = abs(r19f - 1.90) <= 0.03 and abs(r19r - 1.54) <= 0.03 and abs(d001[0] - 0.0065) <= 0.003 and abs(d001[1] - 0.020) <= 0.003
        line("P9 explanatory checks", ok9, f"(1+mu) ratios {r19f:.3f}/{r19r:.3f}; rival D'(0.01) {d001[0]:+.4f} +- {d001[1]:.4f}")
        # P10 first-run convention: any missing +-sigma edge root => 'no break-even'
        changed = []
        for s in PLACE:
            for law in L.LAWS:
                edge_missing = any(res[s][law][smp][k] is None for smp in ("U", "K") for k in ("mu_lo", "mu_hi"))
                if edge_missing:
                    changed.append((s, L.NAMES[law]))
        ok10 = changed == [(1.00, "rival")]
        line("P10 first-run convention changes exactly the rival s=1 row", ok10, f"rows with a missing edge root: {changed}")
        core = ["C1", "C2", "P2 central mu_be (20 values, 1.5%; KROSS rival s=1 10%)"]
        overall = "REPRODUCES" if not fails else ("PARTIAL" if ("P6 matrix exact (in-repo disfavours both at every s; literature neither), summary NON-DIAGNOSTIC, two forms agree" not in fails and ok1 and ok2) else "DISAGREES")
        P(f"\nOVERALL (P1-P6 must all pass for REPRODUCES): {overall};  failing lines: {fails}")
        OUT["overall"] = overall
        OUT["fails"] = fails
    else:
        mutate_report(res, resB, inb, litb, Su, Sk, AS)
        return

    OUT["rows"] = {str(s): {law: dict(U=res[s][law]["U"], K=res[s][law]["K"], R=res[s][law]["R"]) for law in L.LAWS} for s in res}
    with open(os.path.join(L.HERE, "CFG180_main_results.json"), "w") as f:
        json.dump(OUT, f, indent=1, default=str)
    P(f"\nruntime {time.time() - T0:.1f} s")
    sys.exit(0 if (ok1 and ok2) else 2)


def mutate_report(res, resB, inb, litb, Su, Sk, AS):
    # baseline for comparison (unmutated pipeline, same code)
    Su0, Sk0, AS0, _, _ = build("0")
    base = {s: L.solve_pair(Sk0, Su0, AS0, s) for s in (1.00, 1.42)}
    R = lambda r: None if r is None else r["R"]
    b142f = R(base[1.42]["flat"]["R"])
    m142f = R(res[1.42]["flat"]["R"])
    bites = False
    P(f"\n-- MUTATE={MODE} report (baseline in the same run)")
    if MODE == "1":
        P(f"   R_flat(1.42) baseline {b142f:.3f}; mutated {m142f}")
        u = res[1.42]["flat"]["U"]["mu"]
        bites = (m142f is None) or (m142f > 1.5 * b142f)
        P(f"   mutated KURVS flat mu_be {u} (None = no root below mu=30: counted as R undefined = a rise beyond any finite line)")
    elif MODE == "2":
        m1 = R(res[1.00]["flat"]["R"])
        b1r = R(base[1.00]["H"]["R"])
        b1f = R(base[1.00]["flat"]["R"])
        P(f"   mutated R_flat(1) {m1}; baseline R_rival(1) {b1r:.3f}; baseline R_flat(1) {b1f:.3f}")
        bites = (m1 is not None) and abs(m1 / b1r - 1) <= 0.05 and (m1 / b1f > 2 or b1f / m1 > 2)
    elif MODE == "3":
        P(f"   R_flat(1.42) baseline {b142f:.3f}; mutated {m142f}")
        bites = (m142f is None) or abs(m142f / b142f - 1) > 0.25
    elif MODE in ("4", "5"):
        rl = base[1.42]["flat"]["R"]
        if MODE == "4":
            mult, br_in, br_lit = 1.0, (0.73 * rl["R"], 1.39 * rl["R"]), (0.8 * rl["R"], 1.2 * rl["R"])
            f0 = L.disfav_overlap(rl, (inb[0], inb[1]))
            f1 = L.disfav_overlap(rl, br_in)
            P(f"   flat in-repo flag at s=1.42: baseline {f0} -> mutated {f1}")
            bites = bool(f0 and not f1)
        else:
            br_lit = (0.8 * 10 * rl["R"], 1.2 * 10 * rl["R"])
            br_in = (0.73 * 10 * rl["R"], 1.39 * 10 * rl["R"])
            f0 = L.disfav_overlap(rl, litb)
            f1 = L.disfav_overlap(rl, br_lit)
            P(f"   flat literature-bracket flag at s=1.42: baseline {f0} -> mutated {f1} (in-repo-width variant: {L.disfav_overlap(rl, br_in)})")
            bites = bool((not f0) and f1)
    elif MODE == "6":
        u = res[1.00]["flat"]["U"]["mu"]
        P(f"   KURVS flat mu_be at s=1 with range [0.01, 1.0]: {u} (baseline 2.109)")
        bites = (u is None) and (res[1.00]["flat"]["R"] is None)
    P(f"MUTATE={MODE}: {'CONTROL BITES (exit 1)' if bites else 'CONTROL FAILED TO BITE (exit 0)'}")
    OUT["bites"] = bool(bites)
    with open(os.path.join(L.HERE, f"CFG180_MUTATE_{MODE}_results.json"), "w") as f:
        json.dump(OUT, f, indent=1, default=str)
    sys.exit(1 if bites else 0)


if __name__ == "__main__":
    main()
