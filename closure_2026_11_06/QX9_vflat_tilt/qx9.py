#!/usr/bin/env python3
"""QX9: what drives QX8's Vflat slope b_V, and is it PAPER67's 'tilt with speed'? Criteria: FROZEN_CRITERIA.md
(0bd9b6c4b7). Reuses QX8's loader, fitter and solved parts read-only. kappa = 1/2 FITTED; not theory closed.
Footings never pooled.

Run from the repo root:
  OMP_NUM_THREADS=1 nice -n 15 python3 closure_2026_11_06/QX9_vflat_tilt/qx9.py            -> qx9.out / qx9.json
  OMP_NUM_THREADS=1 nice -n 15 python3 closure_2026_11_06/QX9_vflat_tilt/qx9.py --mutate   -> qx9_MUTATE.out / .json
"""
import os, sys, json
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, os.path.join(REPO, "closure_2026_11_06", "QX8_sparc_exact_field"))
import qx8 as Q8                                                   # noqa: E402  (read-only import)

UPS, NODES, FOOT = Q8.UPS, Q8.NODES, Q8.FOOT
lU, lN = np.log(UPS), np.log(NODES)
i50 = int(np.where(UPS == 0.50)[0][0])
NMOCK, NBOOT = 200, 2000
MUTATE = "--mutate" in sys.argv
tag = "_MUTATE" if MUTATE else ""
OUT = []
P = lambda s="": (print(s, flush=True), OUT.append(str(s)))


def mres_at(q, lg, iu):
    OK = q["OK"][:, iu]; r = np.log10(q["GO"]) - lg[:, iu]
    return float(np.sum(q["W"][OK] * r[OK]) / max(np.sum(q["W"][OK]), 1e-300))


def regress(rows, key, joint=True, boot=True, rng=None):
    rows = [p for p in rows if p["Vflat"] > 0 and p["SBeff"] > 0]
    lv = np.log10([p["Vflat"] for p in rows]); y = np.array([p[key] for p in rows])
    X = np.column_stack([np.ones(len(rows)), np.log10([p["SBeff"] for p in rows]), lv]) if joint else np.column_stack([np.ones(len(rows)), lv])
    b = np.linalg.lstsq(X, y, rcond=None)[0]; bv = float(b[-1])
    sd = None
    if boot:
        bs = []
        for _ in range(NBOOT):
            ii = rng.integers(0, len(rows), len(rows)); bs.append(np.linalg.lstsq(X[ii], y[ii], rcond=None)[0][-1])
        sd = float(np.std(bs))
    return dict(b_V=bv, sigma=sd, n=len(rows), z=(abs(bv) / sd if sd else None))


def main():
    GALS = Q8.load_sparc(); n = len(GALS)
    rng = np.random.default_rng(20261106)
    P(f"QX9 Vflat slope{' -- MUTATE (planted +0.20/dex in mocks)' if MUTATE else ''}. kappa = 1/2 FITTED; not theory closed. n galaxies {n}.")
    q8 = json.load(open(os.path.join(REPO, "closure_2026_11_06", "QX8_sparc_exact_field", "qx8.json")))
    RES = dict(lane="QX9", criteria="0bd9b6c4b7", mutate=MUTATE, footings={})
    labels = {}
    for foot, a0 in FOOT.items():
        parts = [dict(np.load(os.path.join(Q8.PARTS, foot, f"{i:03d}.npz"), allow_pickle=False)) for i in range(n)]
        rows = []; LG = {}
        for k, (q, pt) in enumerate(zip(GALS, parts)):
            lgl = np.log10(np.maximum(Q8.nu(q["GB"] / a0) * q["GB"], 1e-300))
            Tf = np.array([np.interp(lU, lN, pt["T"][:, j]) for j in range(pt["T"].shape[1])])
            lge = lgl + Tf; LG[k] = dict(law=lgl, ex=lge)
            il = Q8.fit_one(q, lgl)[2]; ie = Q8.fit_one(q, lge)[2]
            m = q["meta"]
            rows.append(dict(k=k, name=q["name"], Vflat=m["Vflat"], SBeff=m["SBeff"], Qf=m["Q"], Inc=m["Inc"],
                             mres_law=mres_at(q, lgl, il), mres_ex=mres_at(q, lge, ie),
                             fix_law=mres_at(q, lgl, i50), fix_ex=mres_at(q, lge, i50),
                             U_law=float(UPS[il]), U_ex=float(UPS[ie]), il=int(il), ie=int(ie),
                             bulgefree=bool(np.all(q["Vbul"] == 0)),
                             gasdom=bool(np.median(np.sign(q["Vgas"]) * q["Vgas"] ** 2) > np.median(0.5 * q["Vdisk"] ** 2))))
        F = {}
        if not MUTATE:
            # KA1: reproduce QX8's b_V from its own per-galaxy table
            for key in ("mres_law", "mres_ex"):
                ref = q8["footings"][foot]["SB_trend"][key]["slope_V"]
                mine = regress(rows, key, boot=False)["b_V"]
                P(f"[{foot}] KA1 {key}: QX9 {mine:+.6f} vs QX8 {ref:+.6f} -> {'PASS' if abs(mine - ref) <= 1e-6 else 'FAIL'}")
                F[f"KA1_{key}"] = dict(qx9=mine, qx8=ref, ok=abs(mine - ref) <= 1e-6)
            # Q1: FG1's Upsilon tilt on the same fits
            for mk, uk in (("law", "U_law"), ("ex", "U_ex")):
                good = [p for p in rows if p["Qf"] <= 2 and p["Inc"] >= 30 and p["Vflat"] > 0]
                lo = [p[uk] for p in good if p["Vflat"] < 100]; hi = [p[uk] for p in good if p["Vflat"] > 150]
                t = float(np.median(lo) - np.median(hi)); F[f"FG1_U_tilt_{mk}"] = t
                P(f"[{foot}] Q1 FG1-style Upsilon tilt ({mk}): median U(V<100) - median U(V>150) = {t:+.3f} (FG1 line |t| <= 0.15)")
        # checks S0-S6 for law and exact field
        sets = dict(S0_all=rows,
                    S2_FG1cut=[p for p in rows if p["Qf"] <= 2 and p["Inc"] >= 30],
                    S4_bulgefree=[p for p in rows if p["bulgefree"]],
                    S5_gasdom=[p for p in rows if p["gasdom"]],
                    S6_offedge=None)
        if not MUTATE:
            for mk in ("law", "ex"):
                key, fkey, uk = f"mres_{mk}", f"fix_{mk}", f"U_{mk}"
                tab = {}
                tab["S0_joint"] = regress(rows, key, rng=rng)
                tab["S1_simple"] = regress(rows, key, joint=False, rng=rng)
                tab["S2_FG1cut"] = regress(sets["S2_FG1cut"], key, rng=rng)
                tab["S3_fixedU050"] = regress(rows, fkey, rng=rng)
                tab["S4_bulgefree"] = regress(sets["S4_bulgefree"], key, rng=rng)
                tab["S5_gasdom"] = regress(sets["S5_gasdom"], key, rng=rng)
                off = [p for p in rows if 0.30 < p[uk] < 1.20]
                tab["S6_offedge"] = regress(off, key, rng=rng)
                tab["S2S6"] = regress([p for p in off if p["Qf"] <= 2 and p["Inc"] >= 30], key, rng=rng)
                nedge = dict(lo=sum(p[uk] <= 0.30 for p in rows), hi=sum(p[uk] >= 1.20 for p in rows))
                P(f"[{foot}] {mk}: refit U at grid edges: {nedge['lo']} at 0.30, {nedge['hi']} at 1.20")
                for s, v in tab.items():
                    P(f"[{foot}] {mk} {s:14s}: b_V {v['b_V']:+.4f} +- {v['sigma']:.4f} ({v['z']:.1f} sigma, n {v['n']})")
                F[mk] = dict(checks=tab, edges=nedge)
        # S7 mocks (null) or planted mocks (MUTATE): drawn from the LAW at each galaxy's law-fit U, refit with the law
        # (frozen null); also drawn from the exact field and refit with it (reported).
        for mk in ("law", "ex"):
            bvs = []
            for it in range(NMOCK):
                mrows = []
                for p in rows:
                    q = GALS[p["k"]]; lg = LG[p["k"]][mk]; iu = p["il"] if mk == "law" else p["ie"]
                    R = q["Rm"]; gp = 10 ** lg[:, iu]
                    V = np.sqrt(np.maximum(gp * R, 0)) / 1e3 + rng.normal(0, np.clip(q["eV"], 1e-3, None))
                    GO = (np.abs(V) * 1e3) ** 2 / R
                    if MUTATE and p["Vflat"] > 0:
                        GO = GO * 10 ** (0.20 * np.log10(p["Vflat"] / 100.0))
                    qm = dict(q); qm["GO"] = np.maximum(GO, 1e-300)
                    ju = Q8.fit_one(qm, lg)[2]
                    mrows.append(dict(p, mock=mres_at(qm, lg, ju)))
                bvs.append(regress(mrows, "mock", boot=False)["b_V"])
            bvs = np.array(bvs)
            F[f"mock_{mk}"] = dict(median=float(np.median(bvs)), p2_5=float(np.percentile(bvs, 2.5)), p97_5=float(np.percentile(bvs, 97.5)))
            P(f"[{foot}] {'planted ' if MUTATE else ''}mocks from {mk}: b_V median {np.median(bvs):+.4f}, 95 % [{np.percentile(bvs, 2.5):+.4f}, {np.percentile(bvs, 97.5):+.4f}] ({NMOCK} mocks)")
        RES["footings"][foot] = F
        if not MUTATE:
            lab = {}
            for mk in ("law", "ex"):
                tab = F[mk]["checks"]; real = tab["S0_joint"]["b_V"]; mo = F["mock_law"]
                inside = mo["p2_5"] <= real <= mo["p97_5"]
                lose = (tab["S3_fixedU050"]["z"] < 2) or (tab["S2S6"]["z"] < 2)
                keep = all(tab[s]["z"] >= 2 for s in ("S2_FG1cut", "S3_fixedU050", "S6_offedge"))
                lab[mk] = "ARTEFACT" if (inside or lose) else ("REAL" if (not inside and keep) else "MIXED")
                P(f"[{foot}] {mk}: real b_V {real:+.4f}; inside law-mock 95 %: {inside}; loses significance (S3 or S2+S6): {lose}; keeps under S2,S3,S6: {keep} -> {lab[mk]}")
            labels[foot] = lab; F["label"] = lab
    if MUTATE:
        ok = True
        nul = json.load(open(os.path.join(HERE, "qx9.json")))
        for foot in FOOT:
            for mk in ("law", "ex"):
                sh = RES["footings"][foot][f"mock_{mk}"]["median"] - nul["footings"][foot][f"mock_{mk}"]["median"]
                b = abs(sh - 0.20) <= 0.07; ok &= (b if mk == "law" else True)
                P(f"[{foot}] MUTATE {mk}: recovered shift (planted median - null median) {sh:+.4f} (line 0.20 +- 0.07) -> {'BITES' if b else 'DOES NOT BITE'}{'' if mk == 'law' else ' (reported)'}")
        P(f"MUTATE overall (law mocks, frozen): {'BITES' if ok else 'DOES NOT BITE'}")
        RES["bites"] = ok
    else:
        overall = {}
        for mk in ("law", "ex"):
            a, b = labels["canonical"][mk], labels["alt"][mk]
            overall[mk] = a if a == b else f"SPLIT ({a}/{b}): no label"
            P(f"LABEL {mk}: {overall[mk]}")
        RES["label"] = overall
    open(os.path.join(HERE, f"qx9{tag}.out"), "w").write("\n".join(OUT) + "\n")
    json.dump(RES, open(os.path.join(HERE, f"qx9{tag}.json"), "w"), indent=1, default=float)
    return 0 if (not MUTATE or RES["bites"]) else 1


if __name__ == "__main__":
    sys.exit(main())
