#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CFG180 attacks A1-A8 (frozen in CFG180_FROZEN_CRITERIA.md section 6-A).  Seeds: SEED env (default 180; re-run 181).
Shared (not independent): the CFG165 pipeline (CFG180_lib.M).  Exit 0.
"""
import os
import sys
import json
import math
import copy
import csv
import time

import numpy as np

import CFG180_lib as L
M = L.M

SEED = int(os.environ.get("SEED", "180"))
NB = 300
PLACE = (1.00, 1.42, 1.62, 1.69, 3.00)
OUT = {}
T0 = time.time()


def P(*a):
    print(L.scrub(" ".join(str(x) for x in a)), flush=True)


def dex(x):
    return math.log10(x)


def dist_to_interval(R, lo, hi):
    if lo <= R <= hi:
        return 0.0
    if R < lo:
        return dex(lo / R)
    return dex(R / hi)


def summary(res_s, inb, litb, quad=False):
    both = []
    for law in L.LAWS:
        rl = res_s[law]["R"]
        if rl is None:
            continue
        if L.disfav_overlap(rl, inb, quad) and L.disfav_overlap(rl, litb, quad):
            both.append(law)
    return both


def flags(res_s, br, quad=False):
    o = {}
    for law in L.LAWS:
        rl = res_s[law]["R"]
        o[law] = None if rl is None else L.disfav_overlap(rl, br, quad)
    return o


def subsample(S, idx):
    n = len(S.R)
    S2 = copy.copy(S)
    for k, v in list(S.__dict__.items()):
        if isinstance(v, np.ndarray) and v.shape and len(v) == n:
            setattr(S2, k, v[idx])
        elif isinstance(v, list) and len(v) == n and k != "fdm_ids":
            setattr(S2, k, [v[i] for i in idx])
    return S2


def main():
    P("=" * 100)
    P(f"CFG180 attacks A1-A8.  seed={SEED}  repo=<repo>")
    P("=" * 100)
    Su = L.get_kurvs("inc_star_deg")
    Sk = L.get_kross()
    AS = L.get_anchor()
    ro = L.robs(float(np.median(Su.z)), float(np.median(Sk.z)), float(np.median(Su.logM)), float(np.median(Sk.logM)))
    inb, litb = ro["inrep"](2.0), ro["litb"](0.2)
    res = {s: L.solve_pair(Sk, Su, AS, s) for s in PLACE}

    # ---------------------------------------------------------------- A1
    P("\n=== A1 structural required precision: distance (dex) of the truth law's R to the OTHER law's 1-sigma interval ===")
    P("   w* = that distance; a bracket half-width w on R_obs disfavours the wrong law only if w < w*.")
    A1 = {}
    for s in PLACE:
        rf, rr = res[s]["flat"]["R"], res[s]["H"]["R"]
        w_flat_truth = dist_to_interval(rf["R"], rr["lo"] if rr["lo"] > 0 else 1e-9, rr["hi"])
        w_riv_truth = dist_to_interval(rr["R"], rf["lo"], rf["hi"])
        cls = ("STRUCTURALLY NON-DIAGNOSTIC" if (w_flat_truth < 0.02 and w_riv_truth < 0.02)
               else ("R_obs-limited" if max(w_flat_truth, w_riv_truth) >= 0.07 else "marginal"))
        A1[s] = dict(w_flat_truth=w_flat_truth, w_rival_truth=w_riv_truth, cls=cls)
        P(f"   s={s:4.2f}: flat-truth (R={rf['R']:.2f}) w*={w_flat_truth:.3f} dex   rival-truth (R={rr['R']:.2f}) w*={w_riv_truth:.3f} dex   -> {cls}")
    P("   descriptive: zero-width R_obs ranges where EXACTLY ONE law is disfavoured (frozen conservative intervals)")
    grid = np.geomspace(0.2, 30, 3000)
    for s in PLACE:
        rf, rr = res[s]["flat"]["R"], res[s]["H"]["R"]
        segs = []
        state = None
        start = None
        for r in grid:
            fd = not (rf["lo"] <= r <= rf["hi"])
            rd = not (rr["lo"] <= r <= rr["hi"])
            st = ("flat only" if fd and not rd else "rival only" if rd and not fd else "both" if fd and rd else "neither")
            if st != state:
                if state in ("flat only", "rival only"):
                    segs.append((state, start, prev))
                state, start = st, r
            prev = r
        if state in ("flat only", "rival only"):
            segs.append((state, start, prev))
        P(f"   s={s:4.2f}: " + "; ".join(f"{a}: R_obs in [{b:.2f}, {c:.2f}]" for a, b, c in segs))
    OUT["A1"] = A1

    # ---------------------------------------------------------------- A2
    P("\n=== A2 sample-size requirement: sigma_f = sqrt(f^2 sigma_raw^2 + sigma_anchor^2); intervals recomputed ===")
    fs = (1.0, 0.7, 0.5, 0.35, 0.25, 0.15, 0.1, 0.05, 0.0)
    A2 = {}
    for s in PLACE:
        row = {}
        for f in fs:
            r = L.solve_pair(Sk, Su, AS, s, sig_f=f)
            rf, rr = r["flat"]["R"], r["H"]["R"]
            if rf is None or rr is None:
                row[f] = None
                continue
            dj = bool(rf["hi"] < rr["lo"] or rr["hi"] < rf["lo"])
            djq = bool(rf["qhi"] < rr["qlo"] or rr["qhi"] < rf["qlo"])
            row[f] = dict(disjoint=dj, disjoint_quad=djq, flat=(rf["lo"], rf["R"], rf["hi"]), rival=(rr["lo"], rr["R"], rr["hi"]))
        fstar = next((f for f in fs if row[f] and row[f]["disjoint"]), None)
        fstar_q = next((f for f in fs if row[f] and row[f]["disjoint_quad"]), None)
        f0 = bool(row[0.0] and row[0.0]["disjoint"])
        if fstar is None:
            cls = "floor-limited (not disjoint even at f=0)"
        elif fstar >= 0.1:
            cls = f"reachable (f*={fstar}, N factor {1 / max(fstar, 1e-9) ** 2:.0f})" if fstar > 0 else "floor-limited"
        else:
            cls = f"N-hungry (f*={fstar})"
        A2[s] = dict(fstar=fstar, fstar_quad=fstar_q, disjoint_at_f0=f0, cls=cls, row={str(k): v for k, v in row.items()})
        P(f"   s={s:4.2f}: disjoint (conservative) at f = {[f for f in fs if row[f] and row[f]['disjoint']]};  quadrature-disjoint at f = {[f for f in fs if row[f] and row[f]['disjoint_quad']]};  f=0 disjoint {f0}  -> {cls}")
        P(f"           at f=0: flat {row[0.0]['flat'] if row[0.0] else None}  rival {row[0.0]['rival'] if row[0.0] else None}")
    P("   A2x (POST-HOC, labelled; not frozen): the same with NO anchor floor, sigma_f = f sigma_raw (the SPARC anchor error is common to both epochs, so treating it as an independent floor per sample double-counts it)")
    A2x = {}
    fsx = (1.0, 0.7, 0.5, 0.35, 0.25, 0.15, 0.1, 0.07, 0.05, 0.03, 0.02, 0.01)
    for s in PLACE:
        dj, djq = [], []
        for f in fsx:
            r = L.solve_pair(Sk, Su, AS, s, sig_f=f, anchor_floor=False)
            rf, rr = r["flat"]["R"], r["H"]["R"]
            if rf is None or rr is None:
                continue
            if rf["hi"] < rr["lo"] or rr["hi"] < rf["lo"]:
                dj.append(f)
            if rf["qhi"] < rr["qlo"] or rr["qhi"] < rf["qlo"]:
                djq.append(f)
        A2x[s] = dict(conservative=dj, quadrature=djq)
        P(f"   s={s:4.2f}: disjoint (conservative) at f = {dj};  (quadrature) at f = {djq};  largest f -> N factor 1/f^2: cons {('%.0f' % (1/max(dj)**2)) if dj else 'none in grid'}, quad {('%.0f' % (1/max(djq)**2)) if djq else 'none in grid'}")
    OUT["A2x"] = A2x
    OUT["A2"] = A2

    # ---------------------------------------------------------------- A3
    P("\n=== A3 R_obs precision from data already in the repo ===")
    rows = list(csv.DictReader(open(os.path.join(L.REPO, "data_assembly", "kmos3d_phibss", "phibss13_joined.csv"))))
    fl = lambda x: float(x) if x not in ("", "nan") else float("nan")
    clean = [r for r in rows if r["co_upper_limit"] == "0" and r["fgas_inconsistent_in_source"] == "0" and r["comp"] == ""
             and math.isfinite(fl(r["z_co"])) and math.isfinite(fl(r["mstar_msun"])) and fl(r["mmol_msun"]) > 0]
    P(f"   PHIBSS rows total {len(rows)}; clean (no CO limit, no inconsistent f_gas, no secondary component, z_CO finite) {len(clean)}  (target 51)")
    A3 = dict(n_clean=len(clean))
    if len(clean) == 51:
        y = np.array([math.log10(fl(r["mmol_msun"]) / fl(r["mstar_msun"])) for r in clean])
        lm = np.array([math.log10(fl(r["mstar_msun"])) - 10.5 for r in clean])
        lz = np.array([math.log10(1 + fl(r["z_co"])) for r in clean])

        def ols(X, y):
            n, k = X.shape
            b, *_ = np.linalg.lstsq(X, y, rcond=None)
            res = y - X @ b
            s2 = float(res @ res) / (n - k)
            cov = s2 * np.linalg.inv(X.T @ X)
            return b, np.sqrt(np.diag(cov)), n

        one = np.ones(len(y))
        fits = {}
        b, se, n = ols(np.column_stack([one, lm, lz]), y); fits["mass+z (n=51)"] = (b[2], se[2], n, b[1], se[1])
        b, se, n = ols(np.column_stack([one, lz]), y); fits["z only (n=51)"] = (b[1], se[1], n, None, None)
        m = np.array([fl(r["z_co"]) < 1.7 for r in clean])
        b, se, n = ols(np.column_stack([one, lm, lz])[m], y[m]); fits["mass+z, z<1.7"] = (b[2], se[2], n, b[1], se[1])
        for k, (e, sd, n, bm, sbm) in fits.items():
            hw = sd * dex(ro["fz"])
            P(f"   fit {k:18s}: e = {e:+.3f} +- {sd:.3f}  (n={n})" + (f"; mass coeff {bm:+.3f} +- {sbm:.3f}" if bm is not None else "") + f"   1-sigma half-width on R_obs = {hw:.3f} dex")
        A3["fits"] = {k: dict(e=v[0], se=v[1], n=v[2]) for k, v in fits.items()}
        e0, se0 = fits["mass+z (n=51)"][0], fits["mass+z (n=51)"][1]
        P(f"   in-repo e vs abstract-level 2.5: separation {(2.5 - e0) / se0:.2f} sigma (README target: exponent 0.23 +- 0.52; algebra 4.4 sigma with the README constants)")
        A3["sep_sigma"] = (2.5 - e0) / se0
        # required precision
        ws = [(s, A1[s]["w_flat_truth"], A1[s]["w_rival_truth"]) for s in PLACE]
        wpos = [max(a, b) for _, a, b in ws if max(a, b) > 0]
        P(f"   A1 w* values: {[(s, round(a, 3), round(b, 3)) for s, a, b in ws]}")
        P("   se needed on e for a 1-sigma-bracket half-width equal to w*: se_e = w*/log10(1+z ratio); rows needed ~ n_now (se_now/se_e)^2")
        for s, a, b in ws:
            w = max(a, b)
            if w > 0:
                se_need = w / dex(ro["fz"])
                P(f"     s={s:4.2f}: w*={w:.3f} dex -> se_e <= {se_need:.3f} (now {se0:.3f}) -> ~{51 * (se0 / se_need) ** 2:.0f} clean rows if the PHIBSS scatter stays and selection is uniform")
            else:
                P(f"     s={s:4.2f}: w*=0 for both truths -> no R_obs precision suffices")
        hw_now = se0 * dex(ro["fz"])
        if not wpos:
            A3["verdict"] = "w* = 0 for both truths at every s: no R_obs precision suffices"
        elif hw_now > min(wpos):
            A3["verdict"] = f"no existing in-repo dataset suffices: best 1-sigma half-width {hw_now:.3f} dex > smallest w*>0 {min(wpos):.3f} dex"
        else:
            A3["verdict"] = f"1-sigma half-width {hw_now:.3f} dex <= smallest w*>0 {min(wpos):.3f} dex"
        P(f"   -> {A3['verdict']}")
    # descriptive Sharma row (scaling-derived, KROSS-epoch only)
    sh = list(csv.DictReader(open(os.path.join(L.REPO, "data_assembly", "arxiv_tables", "sharma2024_gs21b.csv"))))
    zz = np.array([fl(r["Redshift"]) for r in sh]); ms = np.array([fl(r["Mstar"]) for r in sh])
    mh2 = np.array([fl(r["MH2"]) for r in sh]); mhi = np.array([fl(r["MHI"]) for r in sh])
    ok = np.isfinite(zz) & np.isfinite(ms) & (ms > 0) & np.isfinite(mh2) & np.isfinite(mhi)
    P(f"   descriptive (NOT used): sharma2024_gs21b.csv rows {len(sh)}, usable {int(ok.sum())}, z {zz[ok].min():.2f}-{zz[ok].max():.2f}; median MH2/M* {np.median(mh2[ok] / ms[ok]):.2f}, MHI/M* {np.median(mhi[ok] / ms[ok]):.2f}; "
      "KROSS-epoch only, scaling-derived (CFG165), no z ~ 1.5 counterpart, so no ratio.")
    P("   other candidates by name: romanoliveira2023_gasmasses.csv (6 rows, high-z ALMA), budhies_hi.csv and mightee_hi_highz (z < 0.5): none brackets z ~ 0.85 -> 1.5.")
    OUT["A3"] = A3

    # ---------------------------------------------------------------- A4
    P("\n=== A4 reconciling offset: KURVS anchor-corrected D'(mu_U = R_obs mu_be(KROSS)) in dex (and in sigma) ===")
    A4 = {}
    for s in PLACE:
        cU, cK = res[s]["curves"]
        line = []
        for nm, Rv in (("in-repo", ro["Rin"]), ("literature", ro["Rlit"])):
            for law in L.LAWS:
                bK = res[s][law]["K"]["mu"]
                if bK is None:
                    continue
                muU = Rv * bK
                d, sg = cU.at(muU)[law]
                line.append(f"{nm}/{L.NAMES[law]}: {d:+.3f} ({d / sg:+.1f} sigma)")
                A4[f"{s}|{nm}|{law}"] = (d, sg)
        P(f"   s={s:4.2f}: " + "; ".join(line))
    cU, cK = res[1.0]["curves"]
    Dchk = cU.dp(0.67, "flat") - cK.dp(0.67, "flat")
    P(f"   check: common-mu (0.67) flat differential D = D'_KURVS - D'_KROSS = {Dchk:+.4f} (CFG161/167: +0.148 +- 0.044)")
    OUT["A4"] = {k: list(v) for k, v in A4.items()}
    OUT["A4"]["D_common_mu"] = Dchk

    # ---------------------------------------------------------------- A5
    P("\n=== A5 interval convention: quadrature interval  R exp(-+ hypot(...)) instead of the frozen conservative one ===")
    A5 = {}
    for s in PLACE:
        fq_in = flags(res[s], inb, True); fq_lit = flags(res[s], litb, True)
        sm = summary(res[s], inb, litb, True)
        sm0 = summary(res[s], inb, litb, False)
        lab = "DIAGNOSTIC" if len(sm) == 1 else "NON-DIAGNOSTIC"
        A5[s] = dict(in_flags=fq_in, lit_flags=fq_lit, both=sm, label=lab, frozen_both=sm0)
        rf, rr = res[s]["flat"]["R"], res[s]["H"]["R"]
        P(f"   s={s:4.2f}: flat q-int [{rf['qlo']:.2f}, {rf['qhi']:.2f}] rival q-int [{rr['qlo']:.2f}, {'open' if not math.isfinite(rr['qhi']) else format(rr['qhi'], '.2f')}]"
          f" | in-repo flat/rival {fq_in['flat']}/{fq_in['H']}  lit flat/rival {fq_lit['flat']}/{fq_lit['H']}  both-bracket laws {[L.NAMES[x] for x in sm]} -> {lab}")
    OUT["A5"] = {str(s): v for s, v in A5.items()}

    # ---------------------------------------------------------------- A6
    P("\n=== A6 bracket width: in-repo k*sigma_e, literature +-a; summary at s=1 and 1.42 (frozen | quadrature intervals) ===")
    A6 = {}
    for s in (1.00, 1.42):
        for k in (1.0, 1.5, 2.0, 2.5, 3.0):
            for a in (0.10, 0.20, 0.30, 0.40):
                i_b, l_b = ro["inrep"](k), ro["litb"](a)
                sm = summary(res[s], i_b, l_b, False)
                sq = summary(res[s], i_b, l_b, True)
                A6[f"{s}|{k}|{a}"] = (len(sm) == 1, len(sq) == 1, [L.NAMES[x] for x in sm], [L.NAMES[x] for x in sq])
        P(f"   s={s:4.2f}: DIAGNOSTIC (exactly one law disfavoured by both) at (k, a): frozen intervals "
          f"{[(k, a) for k in (1.0, 1.5, 2.0, 2.5, 3.0) for a in (0.1, 0.2, 0.3, 0.4) if A6[f'{s}|{k}|{a}'][0]]}")
        P(f"           quadrature intervals {[(k, a, A6[f'{s}|{k}|{a}'][3][0]) for k in (1.0, 1.5, 2.0, 2.5, 3.0) for a in (0.1, 0.2, 0.3, 0.4) if A6[f'{s}|{k}|{a}'][1]]}  (third entry = the disfavoured law)")
    OUT["A6"] = A6

    # ---------------------------------------------------------------- A7
    P(f"\n=== A7 bootstrap of the root-find error (B={NB}, seed={SEED}): 16-84% of log10 R_law vs the frozen conservative interval ===")
    rng = np.random.default_rng(SEED)
    A7 = {}
    for s in (1.00, 1.42):
        store = {"flat": [], "H": []}
        nn = {"flat": 0, "H": 0}
        for b in range(NB):
            iu = rng.integers(0, len(Su.R), len(Su.R))
            ik = rng.integers(0, len(Sk.R), len(Sk.R))
            r = L.solve_pair(subsample(Sk, ik), subsample(Su, iu), AS, s)
            for law in L.LAWS:
                rl = r[law]["R"]
                if rl is None:
                    nn[law] += 1
                else:
                    store[law].append(math.log10(rl["R"]))
        for law in L.LAWS:
            v = np.array(store[law])
            rl = res[s][law]["R"]
            if len(v) < 30:
                P(f"   s={s:4.2f} {L.NAMES[law]}: only {len(v)} of {NB} resamples have both roots")
                continue
            q16, q50, q84 = np.percentile(v, [16, 50, 84])
            lo_f = dex(rl["lo"]) if rl["lo"] > 0 else -9
            hi_f = dex(rl["hi"]) if math.isfinite(rl["hi"]) else 9
            under = (lo_f - q16 > 0.03) or (q84 - hi_f > 0.03)
            A7[f"{s}|{law}"] = dict(q16=q16, q50=q50, q84=q84, n=len(v), no_root=nn[law], frozen_lo=lo_f, frozen_hi=hi_f, under=bool(under))
            P(f"   s={s:4.2f} {L.NAMES[law]:5s}: bootstrap 16/50/84% R = {10**q16:.2f} / {10**q50:.2f} / {10**q84:.2f} (n={len(v)}, no-root {nn[law]});"
              f" frozen [{rl['lo']:.2f}, {'open' if not math.isfinite(rl['hi']) else format(rl['hi'], '.2f')}] -> {'UNDER-COVERS' if under else 'adequate (frozen is at least as wide)'}"
              f"; bootstrap width {q84 - q16:.3f} dex")
    OUT["A7"] = A7

    # ---------------------------------------------------------------- A8
    P("\n=== A8 e-scan: point R_obs(e) = (1+z ratio)^e x mass factor; which laws are NOT disfavoured (R_obs inside the frozen interval) ===")
    A8 = {}
    es = [x * 0.25 for x in range(-4, 15)]
    for s in PLACE:
        txt = []
        one = []
        for e in es:
            Rv = ro["fz"] ** e * ro["mass_in"]
            nf = res[s]["flat"]["R"]["lo"] <= Rv <= res[s]["flat"]["R"]["hi"]
            nr = res[s]["H"]["R"]["lo"] <= Rv <= res[s]["H"]["R"]["hi"]
            tag = "both ok" if nf and nr else "flat only ok" if nf else "rival only ok" if nr else "both disfav"
            txt.append((e, tag))
            if nf != nr:
                one.append((e, tag))
        A8[s] = txt
        def rng_of(t):
            v = [e for e, g in txt if g == t]
            return f"[{min(v):+.2f},{max(v):+.2f}]" if v else "none"
        P(f"   s={s:4.2f}: e range both ok {rng_of('both ok')}; flat-only-ok {rng_of('flat only ok')}; rival-only-ok {rng_of('rival only ok')}; both disfavoured {rng_of('both disfav')}")
    OUT["A8"] = {str(s): v for s, v in A8.items()}

    fn = "CFG180_attacks_A_results.json" if SEED == 180 else f"CFG180_attacks_A_results_seed{SEED}.json"
    with open(os.path.join(L.HERE, fn), "w") as f:
        json.dump(OUT, f, indent=1, default=str)
    P(f"\nruntime {time.time() - T0:.1f} s")


if __name__ == "__main__":
    main()
