#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
CFG245 Gate C -- CLUSTERS AND THE BULLET (frozen criteria section 3).  Inputs: the committed per-cluster arrays of CFG4_clusters_results.json (read-only),
the Gate T results (the rate T needs), the record's Bullet numbers (CFG4_clusters_results.json numbers/H5; collision ~100 Myr ago, bullet_data_table.py:150).

  C1  X-COP identity.  For each of the 12 clusters at 0.8 R500: M_ph,i/M_b (P2 phantom), S_i = (Omega_c/Omega_b) M_b (recovered from the record's own identity ratio),
      M_class = M_ph + e_cl (S - M_ph) (R-FLUX-2) or max(S, ph) + ... fill-only (R-FLUX-1), e_cl = exp(-Gamma tau_cl);  Q_i = (M_b + M_class)/M_HSE,i.
      PASS iff median_i |Q_i - 1| <= 0.20 on both footings (the record's identity gate).  Verdict bracket tau_cl = 3.5 Gyr (generous); 7.9 and 13.8 reported.
  C2  Bullet.  delta_B = (1 - exp(-Gamma t_c)) max(1, rho_ph/rho_c), t_c = 0.1 Gyr; PASS iff <= 0.10.
  C3  what the class supplies in clusters (reported).
  WINDOW  [Gamma_T,min, Gamma_C,max]; binding rule: FAIL iff (R-FLUX-2) the window is empty or holds no declared candidate on both footings.
Run: ZF_REPO=<repo> python3 CFG245_C_clusters.py ; MUTATE=MT2b|MC1|MC2 python3 CFG245_C_clusters.py (exits 1 when the control bites)
"""
import os, sys, math, json
sys.dont_write_bytecode = True
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import CFG245_common as K

MUT = os.environ.get("MUTATE", "").strip()
SLUG = "CFG245_C_clusters"
POST = (K.upstream_binding() is not None) and not MUT
if POST:
    SLUG += "_POSTHOC"
R = K.Report(SLUG, MUT or None)
TAU_CL = {"generous": 3.5, "central": 7.9, "unfavourable": 13.8}
TAU_GAL = {"generous": K.T0, "central": 10.5, "unfavourable": 7.0}
TC_BULLET = 0.1
LINE_Q = 0.20


def clus(foot, kernel="P2"):
    arr, d = K.clusters(foot, kernel)
    ph = np.array([a["phantom_over_Mb"] for a in arr])
    newt = np.array([a["newt"] for a in arr])
    idr = np.array([a["id_ratio"] for a in arr])
    S = idr * (1.0 + newt) - 1.0              # the record's identity reading: total = M_b (1 + max(ph, S))  (S = cosmic share, 5.36)
    names = [a["name"] for a in arr]
    return ph, newt, idr, S, names, d


def Qvec(ph, newt, S, e, mode="two"):
    if mode == "two":
        Mc = ph + e * (S - ph)
    else:                                   # fill-only: the excess over the phantom is kept, a deficit is filled
        Mc = S + (1.0 - e) * np.maximum(ph - S, 0.0)
    return (1.0 + Mc) / (1.0 + newt)


def medQ(ph, newt, S, e, mode="two"):
    Q = Qvec(ph, newt, S, e, mode)
    return float(np.median(np.abs(Q - 1.0))), float(np.median(Q))


def e_required(ph, newt, S, mode="two"):
    """smallest e (largest Gamma tau) at which median |Q-1| <= 0.20"""
    grid = np.linspace(0.0, 1.0, 100001)
    ok = np.array([medQ(ph, newt, S, e, mode)[0] <= LINE_Q for e in grid[::50]])
    # refine by bisection
    if not ok.any():
        return None
    eg = grid[::50]
    i = int(np.argmax(ok))
    lo, hi = (eg[i - 1] if i > 0 else 0.0), eg[i]
    for _ in range(60):
        mid = 0.5 * (lo + hi)
        if medQ(ph, newt, S, mid, mode)[0] <= LINE_Q:
            hi = mid
        else:
            lo = mid
    return hi


def load_T():
    p = os.path.join(K.HERE, "CFG245_T_timescale_results.json")
    if not os.path.exists(p):
        raise SystemExit("run CFG245_T_timescale.py first (Gate T results are the input of the WINDOW)")
    return json.load(open(p))


def main():
    R.banner("CFG245 Gate C -- CLUSTERS AND THE BULLET" + ("  (POST-HOC EXTRA: an upstream gate already bound)" if POST else "") + (f"  (MUTATE {MUT})" if MUT else ""))
    Tj = load_T()
    num = Tj["numbers"]
    out = {}
    # ---------------------------------------------------------------- controls
    R.banner("CONTROLS")
    ctl = {}
    for foot in K.FOOTS:
        ph, newt, idr, S, names, d = clus(foot)
        med = float(np.median(idr)); sdv = float(np.std(idr, ddof=1))
        committed = d["numbers"]["H2"][f"{foot}|P2"]["id_ratio"]
        Q1 = float(np.median(Qvec(ph, newt, S, 1.0)))
        ctl[foot] = dict(S_mean=float(S.mean()), S_sd=float(S.std()), id_median=med, id_committed=committed, Q_gamma0=Q1, committed_sd=d["numbers"]["H2"][f"{foot}|P2"]["id_sd"])
        R.P(f"  {foot}: recovered cosmic share S = {S.mean():.4f} +- {S.std():.1e} (record: Omega_c/Omega_b = 5.36); identity ratio median {med:.4f} (committed {committed:.4f} +- {ctl[foot]['committed_sd']:.4f}); class at Gamma = 0: median Q = {Q1:.4f}")
    okc1 = all(abs(ctl[f]["Q_gamma0"] - ctl[f]["id_committed"]) < 0.005 for f in K.FOOTS) and all(ctl[f]["S_sd"] < 0.02 for f in K.FOOTS)
    R.cell("C-C1 Gamma = 0 reproduces the record's identity reading 0.946 +- 0.080 (to 0.005)", "PASS" if okc1 else "FAIL",
           "; ".join(f"{f}: median Q {ctl[f]['Q_gamma0']:.4f} vs committed {ctl[f]['id_committed']:.4f}" for f in K.FOOTS))
    # ---------------------------------------------------------------- C1
    R.banner("C1 -- X-COP identity at 0.8 R500: Q = (M_b + M_class)/M_HSE; PASS iff median |Q-1| <= 0.20 on both footings (generous bracket tau_cl = 3.5 Gyr)")
    R.P(f"  {'cand':5s} {'footing':10s} {'Gamma /Gyr':>11s} | " + " | ".join(f"tau_cl={TAU_CL[b]:4.1f}: e / med|Q-1| / out" for b in ("generous", "central", "unfavourable")))
    rows = {}
    for kern in ("P2",):
        for foot in K.FOOTS:
            ph, newt, idr, S, names, d = clus(foot, kern)
            rts = K.rates(foot)
            for c in K.CAND:
                G = rts[c]
                cells = []
                for b in ("generous", "central", "unfavourable"):
                    e = math.exp(-G * TAU_CL[b])
                    m, mq = medQ(ph, newt, S, e, "two")
                    cells.append((e, m, mq, "PASS" if m <= LINE_Q else "FAIL"))
                rows[(kern, foot, c)] = cells
                R.P(f"  {c:5s} {foot:10s} {G:11.6f} | " + " | ".join(f"{e:.3f} / {m:.3f} / {o}" for e, m, mq, o in cells))
    # complete relaxation, Gamma=0, one-sided, nu_mono
    R.P("  reference states (median over the 12 clusters):")
    ref = {}
    for foot in K.FOOTS:
        ph, newt, idr, S, names, d = clus(foot)
        ref[foot] = dict(complete_relax=medQ(ph, newt, S, 0.0), gamma0=medQ(ph, newt, S, 1.0), law_alone=float(np.median((1 + ph) / (1 + newt))),
                         eta=d["numbers"]["H2"][f"{foot}|P2"]["eta"], resid=d["numbers"]["H2"][f"{foot}|P2"]["resid"], resid_sig=d["numbers"]["H2"][f"{foot}|P2"]["resid_sig"])
        R.P(f"    {foot}: complete relaxation (e = 0): med|Q-1| = {ref[foot]['complete_relax'][0]:.3f}, median Q = {ref[foot]['complete_relax'][1]:.3f} (law alone median M_law/M_HSE = {ref[foot]['law_alone']:.3f}; committed eta = {ref[foot]['eta']:.2f}, residual {ref[foot]['resid']:.2f} M_b = {ref[foot]['resid_sig']:.0f} sigma); Gamma = 0: med|Q-1| = {ref[foot]['gamma0'][0]:.3f}")
    need = {}
    for foot in K.FOOTS:
        ph, newt, idr, S, names, d = clus(foot)
        e_req = e_required(ph, newt, S, "two")
        need[foot] = e_req
        R.P(f"    {foot}: C1 passes iff e_cl >= {e_req:.4f} (Gamma tau_cl <= {-math.log(e_req):.4f})  [frozen hand: e_cl >= 0.625, Gamma tau_cl <= 0.47]")
    # one-sided
    R.P("  R-FLUX-1 (fill-only), generous bracket: " + "; ".join(
        f"{c} {foot}: med|Q-1| = {medQ(*[clus(foot)[i] for i in (0, 1, 3)], math.exp(-K.rates(foot)[c]*TAU_CL['generous']), 'one')[0]:.3f}" for foot in K.FOOTS for c in K.CAND))
    # nu_mono (reported)
    R.P("  second kernel nu_mono (its own committed phantom), two-sided, generous bracket: " + "; ".join(
        f"{c} {foot}: med|Q-1| = {medQ(*[clus(foot, 'nu_mono')[i] for i in (0, 1, 3)], math.exp(-K.rates(foot)[c]*TAU_CL['generous']), 'two')[0]:.3f}" for foot in K.FOOTS for c in K.CAND))
    c1_cat = {}
    for c in K.CAND:
        cs = [rows[("P2", f, c)][0][3] for f in K.FOOTS]
        c1_cat[c] = "PASS" if all(x == "PASS" for x in cs) else ("FAIL" if all(x == "FAIL" for x in cs) else "AMBIGUOUS")
    R.cell("C1 (generous bracket, two-sided)", "per candidate: " + ", ".join(f"{c} {v}" for c, v in c1_cat.items()), "")
    # ---------------------------------------------------------------- C2 Bullet
    R.banner("C2 -- the Bullet: displacement of the cold mass toward the baryon-traced target during t_c = 0.1 Gyr (cores passed ~100 Myr ago, bullet_data_table.py:150)")
    bul = json.load(open(K.CLUST_PATH))["numbers"]["H5"]["bullet"]
    R.P(f"  record: lensing peaks on the galaxies, offsets {bul['main']['offset_kpc']:.0f} / {bul['sub']['offset_kpc']:.0f} kpc from the plasma; collisionless mass {bul['main']['dM_over_Mb_gal']:.1f}x / {bul['sub']['dM_over_Mb_gal']:.1f}x the aperture baryons (CFG4_clusters)")
    c2 = {}
    mult = 1000.0 if MUT == "MC2" else 1.0
    for foot in K.FOOTS:
        ph, newt, idr, S, names, d = clus(foot)
        enh = max(1.0, float(np.median(ph / S)))
        for c in K.CAND:
            G = K.rates(foot)[c] * mult
            dB = (1 - math.exp(-G * TC_BULLET)) * enh
            c2[(foot, c)] = dB
            R.P(f"  {c:5s} {foot:10s} Gamma t_c = {G*TC_BULLET:.4g}; flux-law enhancement max(1, median rho_ph/rho_c) = {enh:.2f}; delta_B = {dB:.4g}  -> {'PASS' if dB <= 0.10 else 'FAIL'}")
    c2_ok = all(v <= 0.10 for v in c2.values())
    R.cell("C2 Bullet (delta_B <= 0.10 for every candidate and footing)", "PASS" if c2_ok else "FAIL", f"max delta_B = {max(c2.values()):.3g}")
    # ---------------------------------------------------------------- C3
    R.banner("C3 -- what the class supplies in clusters (reported)")
    for foot in K.FOOTS:
        ph, newt, idr, S, names, d = clus(foot)
        resid_need = d["numbers"]["H2"][f"{foot}|P2"]["resid"]
        for c in K.CAND:
            e = math.exp(-K.rates(foot)[c] * TAU_CL["generous"])
            Mc2 = float(np.median(ph + e * (S - ph)))
            Mc1 = float(np.median(S + (1.0 - e) * np.maximum(ph - S, 0.0)))
            R.P(f"  {foot:10s} {c:5s}: cold mass after relaxation (median, M_b): two-sided {Mc2:.2f}, fill-only {Mc1:.2f}; the law's phantom {float(np.median(ph)):.2f}; the record's residual beyond the law {resid_need:.2f} M_b; Newtonian dark {float(np.median(newt)):.2f}")
    # ---------------------------------------------------------------- the WINDOW
    R.banner("WINDOW -- Gamma_T,min (Gate T-RAR 0.10-dex line, tau_gal) to Gamma_C,max (C1, tau_cl); binding rule: FAIL iff empty or no declared candidate inside on both footings (two-sided)")
    win = {}
    for br in ("generous", "central"):
        for foot in K.FOOTS:
            ph, newt, idr, S, names, d = clus(foot)
            e_req = need[foot]
            Gc_max = -math.log(e_req) / TAU_CL[br]
            reqs = num["T_RAR"][f"P2|{foot}|G-H"]["req_RAR10"]                   # Gamma*tau (the same for every candidate: it is a property of the passive state)
            Gt_min = (reqs / TAU_GAL[br]) if reqs is not None else None
            reqg1 = num["T_G1"][f"{foot}|G-H"]["req_G1"]
            Gg1 = (reqg1 / TAU_GAL[br]) if reqg1 is not None else None
            inside = {c: (Gt_min is not None and Gt_min <= K.rates(foot)[c] <= Gc_max) for c in K.CAND}
            win[(br, foot)] = dict(Gamma_T_min=Gt_min, Gamma_T_min_over_HL=(Gt_min / K.HL if Gt_min is not None else None), Gamma_G1_req=Gg1, Gamma_G1_req_over_HL=(Gg1 / K.HL if Gg1 is not None else None),
                                   Gamma_C_max=Gc_max, Gamma_C_max_over_HL=Gc_max / K.HL, inside=inside, nonempty=(Gt_min is not None and Gt_min <= Gc_max))
            R.P(f"  bracket {br:12s} (tau_gal = {TAU_GAL[br]:.1f}, tau_cl = {TAU_CL[br]:.1f} Gyr) {foot:10s}: Gamma_T,min = {Gt_min/K.HL:.2f} H_L (RAR 0.10), Gamma_G1,req = {Gg1/K.HL:.2f} H_L, Gamma_C,max = {Gc_max/K.HL:.2f} H_L  -> window {'non-empty' if win[(br, foot)]['nonempty'] else 'EMPTY'}; "
                f"candidates (in H_L): " + ", ".join(f"{c} {K.rates(foot)[c]/K.HL:.2f}{'*' if inside[c] else ''}" for c in K.CAND) + "  (* = inside)")
    # one-sided: T-RAR never passes
    one_pass = any(num["T_RAR"][f"P2-R-FLUX-1|{f}|{c}"]["req_RAR10"] is not None for f in K.FOOTS for c in K.CAND)
    R.P(f"  R-FLUX-1: Gate T-RAR (0.10 line) is reachable at any Gamma tau <= 30: {one_pass} (the excess at x about 1.1 is never removed) -> window empty by construction")
    cand_in = {c: all(win[("generous", f)]["inside"][c] for f in K.FOOTS) for c in K.CAND}
    cand_any = {c: any(win[("generous", f)]["inside"][c] for f in K.FOOTS) for c in K.CAND}
    binding = not any(cand_in.values()) and not any(cand_any.values())
    R.cell("C binding rule (two-sided, generous joint bracket)", "FAIL (BINDING)" if binding else "NOT BINDING",
           "no declared candidate lies inside the window on either footing" if binding else "inside: " + ", ".join(f"{c}={cand_in[c]}" for c in K.CAND))
    cell_win = ("empty/none" if binding else "has a candidate")

    # ---------------------------------------------------------------- MUTATE
    if MUT:
        # reference rate: the smallest rate T-G1 requires (the rate at which a class passing T would have to run), generous bracket
        def c1_at_G1req(mode):
            res = []
            for foot in K.FOOTS:
                ph, newt, idr, S, names, d = clus(foot)
                G = win[("generous", foot)]["Gamma_G1_req"] * (0.0 if MUT == "MT2b" else 1.0)
                e = math.exp(-G * TAU_CL["generous"])
                res.append("PASS" if medQ(ph, newt, S, e, mode)[0] <= LINE_Q else "FAIL")
            return res
        if MUT == "MT2b":
            base = None
            # baseline = Gamma_G1,req; mutated = Gamma = 0
            global_MUT = MUT
            res_m = c1_at_G1req("two")
            res_b = []
            for foot in K.FOOTS:
                ph, newt, idr, S, names, d = clus(foot)
                e = math.exp(-win[("generous", foot)]["Gamma_G1_req"] * TAU_CL["generous"])
                res_b.append("PASS" if medQ(ph, newt, S, e, "two")[0] <= LINE_Q else "FAIL")
            R.P(f"  MUTATE MT2b: C1 at the rate Gate T-G1 requires: baseline {res_b} -> with Gamma = 0 {res_m}")
            bites = (res_b != res_m) and all(x == "PASS" for x in res_m)
        elif MUT == "MC1":
            res_b, res_m = [], []
            for foot in K.FOOTS:
                ph, newt, idr, S, names, d = clus(foot)
                e = math.exp(-win[("generous", foot)]["Gamma_G1_req"] * TAU_CL["generous"])
                res_b.append("PASS" if medQ(ph, newt, S, e, "two")[0] <= LINE_Q else "FAIL")
                res_m.append("PASS" if medQ(ph, newt, S, e, "one")[0] <= LINE_Q else "FAIL")
            R.P(f"  MUTATE MC1: C1 at the rate Gate T-G1 requires: two-sided {res_b} -> one-sided {res_m}")
            bites = (res_b != res_m)
        elif MUT == "MC2":
            R.P(f"  MUTATE MC2: Gamma x 1e3: Bullet cell {'PASS' if c2_ok else 'FAIL'} (baseline expectation: PASS)")
            bites = (not c2_ok)
        else:
            raise SystemExit(f"MUTATE {MUT} is not a Gate C control")
        R.finish(dict(binding_fail=False, mutate_bites=bool(bites)))
        K.exit_mutate(bites, True)

    R.numbers = dict(
        controls=ctl, C1={f"{k[0]}|{k[1]}|{k[2]}": [dict(e=a, med_absQ1=b, medQ=c_, outcome=o) for a, b, c_, o in v] for k, v in rows.items()},
        reference=ref, e_required=need, C2={f"{k[0]}|{k[1]}": v for k, v in c2.items()},
        window={f"{k[0]}|{k[1]}": v for k, v in win.items()}, one_sided_T_RAR_reachable=one_pass, c1_cat=c1_cat)
    R.finish(dict(binding_fail=bool(binding), controls_ok=bool(okc1), c1_category=c1_cat, c2_ok=bool(c2_ok), post_hoc=POST))
    return 0


if __name__ == "__main__":
    sys.exit(main())
