#!/usr/bin/env python3
"""HL3 grader (criteria ef4595f390 + AMENDMENT A1): per-bin cluster medians of rho on both legs with bootstrap 95 %
intervals (B 10,000, seed 1103, one value per cluster per bin = that cluster's median in the bin), Delta_b = lensing -
hydrostatic per shared bin (>= 6 clusters on each leg), S2 lensing-leg need (reported, not graded), S3 scatters, the label
per footing by the frozen rule, hand estimates HE-a..d.
    python3 hl3_grade.py            # hl3.json / hl3.out
    python3 hl3_grade.py --mutate   # M1-M3: hl3_MUTATE.json / hl3_MUTATE.out
Reads hl3_points.json (hl3.py). kappa = 1/2 FITTED; not theory closed. Adopts nothing."""
import os, sys, json, math, warnings, resource
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); MUT = "--mutate" in sys.argv; TAG = "hl3_MUTATE" if MUT else "hl3"; OUT = []
def P(s=""): print(s, flush=True); OUT.append(s)
PTS = json.load(open(os.path.join(HERE, "hl3_points.json")))
A0 = PTS["footings"]; EDGES = PTS["bin_edges"]; NB = len(EDGES) - 1; B, SEED = 10000, 1103
BIN = [f"{EDGES[i]}-{EDGES[i + 1]}" for i in range(NB)]
def glaw(gN, a0): return 0.5 * gN + np.sqrt(0.25 * gN ** 2 + a0 * gN)   # the loaders' law, restated
P(f"HL3 {'MUTATE' if MUT else 'GRADE'}: bins r/R500 {BIN}; B {B}, seed {SEED}; shared bin = >= 6 clusters on each leg. kappa = 1/2 FITTED; not theory closed.")
if not PTS["ka_all_pass"]: P("KNOWN ANSWER FAILED in hl3.py: stop, nothing graded."); sys.exit(2)

def matrix(points, foot, xkey="x", a0_override=None):
    """per-cluster per-bin median of rho -> (names, M[n, NB] with nan where the cluster has no point in the bin, counts[n, NB])."""
    names = sorted({p["name"] for p in points}); M = np.full((len(names), NB), np.nan); C = np.zeros((len(names), NB), int)
    for i, nm in enumerate(names):
        for b in range(NB):
            v = []
            for p in points:
                if p["name"] != nm or not (EDGES[b] <= p[xkey] < EDGES[b + 1]): continue
                v.append(p[f"rho_{foot}"] if a0_override is None else float(np.log10(10 ** p["lgtot"] / glaw(10 ** p["lgbar"], a0_override))))
            if v: M[i, b] = float(np.median(v)); C[i, b] = len(v)
    return names, M, C
def boot(M, rng):
    n = len(M); idx = rng.integers(0, n, (B, n))
    with warnings.catch_warnings():
        warnings.simplefilter("ignore"); return np.nanmedian(M[idx], axis=1)   # B x NB (nan where no resampled cluster has the bin)
def summ(M, S):
    with warnings.catch_warnings():
        warnings.simplefilter("ignore"); med = np.nanmedian(M, axis=0); lo = np.nanpercentile(S, 2.5, axis=0); hi = np.nanpercentile(S, 97.5, axis=0)
    n = np.isfinite(M).sum(axis=0); sd = np.array([float(np.std(M[np.isfinite(M[:, b]), b], ddof=1)) if n[b] >= 3 else np.nan for b in range(NB)])
    return dict(median=med.tolist(), lo=lo.tolist(), hi=hi.tolist(), n=n.tolist(), scatter=sd.tolist())
def compare(ML, MH, rng):
    SL, SH = boot(ML, rng), boot(MH, rng); L, H = summ(ML, SL), summ(MH, SH); D = SL - SH
    with warnings.catch_warnings():
        warnings.simplefilter("ignore"); dlo = np.nanpercentile(D, 2.5, axis=0); dhi = np.nanpercentile(D, 97.5, axis=0)
    dmed = np.array(L["median"]) - np.array(H["median"]); shared = [bool(L["n"][b] >= 6 and H["n"][b] >= 6) for b in range(NB)]
    return dict(L=L, H=H, delta=dmed.tolist(), dlo=dlo.tolist(), dhi=dhi.tolist(), shared=shared, SL=SL, SH=SH)
def label(prim, brac):
    """the frozen rule; prim/brac are compare() outputs for the primary and the bracket lensing sample."""
    sh = [b for b in range(NB) if prim["shared"][b]]
    if not sh: return "UNDECIDED (no shared bin)", sh
    def excl0(c, b): return c["dlo"][b] > 0 or c["dhi"][b] < 0
    if all(abs(prim["delta"][b]) <= 0.10 and prim["dlo"][b] <= 0 <= prim["dhi"][b] for b in sh): return "SAME SHAPE", sh
    b0 = sh[0]
    if all(c["delta"][b0] <= -0.15 and excl0(c, b0) for c in (prim, brac) if c["shared"][b0]) and brac["shared"][b0]: return "HYDROSTATIC-SPECIFIC", sh
    if any(prim["delta"][b] >= 0.15 and excl0(prim, b) and brac["shared"][b] and brac["delta"][b] >= 0.15 and excl0(brac, b) for b in sh): return "LENSING-SPECIFIC", sh
    return "UNDECIDED", sh

LENS = PTS["lensing"]; HYD = PTS["hydrostatic"]
L_prim = [p for p in LENS if not p["merger"]]; L_all = LENS
H_prim = [p for p in HYD if p["stars_measured"]]; H_noA = [p for p in H_prim if not p["a2319"]]; H_12 = HYD
P(f"samples: lensing primary {len({p['name'] for p in L_prim})} X-ray-selected clusters ({len(L_prim)} pts), bracket all {len({p['name'] for p in L_all})} ({len(L_all)} pts, mergers {PTS['mergers']}); "
  f"hydrostatic primary {len({p['name'] for p in H_prim})} with measured stars ({len(H_prim)} pts), without A2319 {len({p['name'] for p in H_noA})}, all 12 with imputed stars ({len(H_12)} pts)")
RES = dict(criteria="ef4595f390", amendment="A1", B=B, seed=SEED, bins=BIN, footings=A0, samples={}, label={}, S2={}, S3={}, HE={}, KA4_check={}, MUTATE={})
def fmt(c, b): return f"{c['delta'][b]:+.3f} [{c['dlo'][b]:+.3f}, {c['dhi'][b]:+.3f}]"
for f, a0 in A0.items():
    rng = np.random.default_rng(SEED)
    nL, ML, CL = matrix(L_prim, f); nH, MH, CH = matrix(H_prim, f)
    prim = compare(ML, MH, rng)
    _, MLa, _ = matrix(L_all, f); brac = compare(MLa, MH, rng)
    _, MLd, _ = matrix(L_prim, f, xkey="x_donahue"); bracD = compare(MLd, MH, rng)
    _, MHn, _ = matrix(H_noA, f); noA = compare(ML, MHn, rng)
    _, MH12, _ = matrix(H_12, f); h12 = compare(ML, MH12, rng)
    def matched(points_h, points_l):
        """hydrostatic per-cluster per-bin median of rho(x) read at the LENSING sample's x values in that bin (sampling check)."""
        names = sorted({p["name"] for p in points_h}); M = np.full((len(names), NB), np.nan)
        for i, nm in enumerate(names):
            xs = np.array(sorted(p["x"] for p in points_h if p["name"] == nm)); rs = np.array([p[f"rho_{f}"] for p in sorted((q for q in points_h if q["name"] == nm), key=lambda q: q["x"])])
            for b in range(NB):
                xl = np.array(sorted({p["x"] for p in points_l if EDGES[b] <= p["x"] < EDGES[b + 1]})); xl = xl[(xl >= xs.min()) & (xl <= xs.max())]
                if len(xl): M[i, b] = float(np.median(np.interp(np.log(xl), np.log(xs), rs)))
        return names, M
    _, MHm = matched(H_prim, L_prim); mx = compare(ML, MHm, rng)
    lab, sh = label(prim, brac)
    P(); P(f"===== [{f}] a0 {a0:.4e}")
    P(f"  bin       | lensing primary median [95 %] (n)        | hydrostatic primary median [95 %] (n)    | Delta_b = L - H [95 %]        shared")
    for b in range(NB):
        L, H = prim["L"], prim["H"]
        ls = f"{L['median'][b]:+.3f} [{L['lo'][b]:+.3f}, {L['hi'][b]:+.3f}] ({L['n'][b]:2d})" if L["n"][b] else "-- (0)"
        hs = f"{H['median'][b]:+.3f} [{H['lo'][b]:+.3f}, {H['hi'][b]:+.3f}] ({H['n'][b]:2d})" if H["n"][b] else "-- (0)"
        ds = fmt(prim, b) if (L["n"][b] and H["n"][b]) else "--"
        P(f"  {BIN[b]:9s} | {ls:40s} | {hs:40s} | {ds:30s} {'SHARED' if prim['shared'][b] else ('reported, not graded' if (L['n'][b] and H['n'][b]) else '')}")
    P(f"  brackets, Delta_b per shared bin: all 20 lensing clusters: " + "; ".join(f"{BIN[b]} {fmt(brac, b)} (n_L {brac['L']['n'][b]})" for b in sh))
    P(f"                                    Donahue r500 for the lensing x: " + "; ".join(f"{BIN[b]} {fmt(bracD, b)}" for b in sh))
    P(f"                                    hydrostatic without A2319: " + "; ".join(f"{BIN[b]} {fmt(noA, b)} (n_H {noA['H']['n'][b]})" for b in sh))
    P(f"                                    hydrostatic all 12 (5 imputed): " + "; ".join(f"{BIN[b]} {fmt(h12, b)} (n_H {h12['H']['n'][b]})" for b in sh))
    P(f"                                    hydrostatic read at the lensing points' x (matched sampling): " + "; ".join(f"{BIN[b]} {fmt(mx, b)} (n_H {mx['H']['n'][b]})" for b in sh))
    # S2: lensing-leg need at R500, else at the outermost shared bin
    b2 = 3 if prim["shared"][3] else (sh[-1] if sh else None)
    if b2 is not None:
        L, H = prim["L"], prim["H"]; needL = (10 ** L["median"][b2], 10 ** L["lo"][b2], 10 ** L["hi"][b2]); needH = (10 ** H["median"][b2], 10 ** H["lo"][b2], 10 ** H["hi"][b2])
        h500 = (10 ** H["median"][3], 10 ** H["lo"][3], 10 ** H["hi"][3], H["n"][3]) if H["n"][3] else None
        RES["S2"][f] = dict(bin=BIN[b2], at_R500=bool(b2 == 3), lensing_need=needL, hydrostatic_need_same_bin=needH, hydrostatic_need_0p75_1p0=h500, NA2_baryon_traced_F={"canonical": 4.206, "alt": 3.811}[f])
        P(f"  S2 (reported, not graded): the 0.75-1.0 bin is {'shared' if b2 == 3 else 'NOT shared (lensing leg ends at 600 kpc = 0.59 R500 at most); S2 is reported at the outermost shared bin ' + BIN[b2]}. "
          f"Lensing-leg need 10^rho = x{needL[0]:.2f} [{needL[1]:.2f}, {needL[2]:.2f}]; X-COP hydrostatic plain-law need in the same bin x{needH[0]:.2f} [{needH[1]:.2f}, {needH[2]:.2f}]"
          + (f"; X-COP plain-law need in 0.75-1.0 (hydrostatic only, {h500[3]} clusters) x{h500[0]:.2f} [{h500[1]:.2f}, {h500[2]:.2f}]" if h500 else "") + f"; NA2's baryon-traced F at the captured amount {RES['S2'][f]['NA2_baryon_traced_F']}.")
    # S3
    S3 = dict(lensing=prim["L"]["scatter"], hydrostatic=prim["H"]["scatter"])
    def pooled(sc, n): w = [(n[b] - 1) for b in sh if np.isfinite(sc[b])]; return float(math.sqrt(sum((n[b] - 1) * sc[b] ** 2 for b in sh if np.isfinite(sc[b])) / sum(w))) if w else float("nan")
    S3["pooled_shared_lensing"] = pooled(prim["L"]["scatter"], prim["L"]["n"]); S3["pooled_shared_hydrostatic"] = pooled(prim["H"]["scatter"], prim["H"]["n"]); S3["h56_per_cluster_a0_scatter"] = 0.176
    RES["S3"][f] = S3
    P(f"  S3 per-cluster scatter of rho at fixed r/R500 (dex): lensing " + ", ".join(f"{BIN[b]} {prim['L']['scatter'][b]:.3f}" for b in range(NB) if np.isfinite(prim['L']['scatter'][b]))
      + "; hydrostatic " + ", ".join(f"{BIN[b]} {prim['H']['scatter'][b]:.3f}" for b in range(NB) if np.isfinite(prim['H']['scatter'][b]))
      + f"; pooled over shared bins lensing {S3['pooled_shared_lensing']:.3f} vs hydrostatic {S3['pooled_shared_hydrostatic']:.3f} (h56 per-cluster a0 scatter 0.176)")
    # KA4 consistency
    if prim["shared"][3]:
        ok = abs(prim["delta"][3] - 0.031) <= math.sqrt(((prim["dhi"][3] - prim["dlo"][3]) / 2) ** 2 + (1.96 * 0.020) ** 2)
        RES["KA4_check"][f] = dict(applicable=True, delta_0p75_1p0=prim["delta"][3], consistent=bool(ok)); P(f"  KA4 check in 0.75-1.0: Delta_b {fmt(prim, 3)} vs HL2 +0.031 +- 0.020 -> {'consistent' if ok else 'INCONSISTENT'}")
    else:
        RES["KA4_check"][f] = dict(applicable=False, note="0.75-1.0 not shared; noted, not checked"); P(f"  KA4 check: the 0.75-1.0 bin is not shared (lensing leg ends at 0.59 R500); noted, not checked. HL2's +0.031 +- 0.020 is a mass ratio at R500, HL3's Delta_b at {BIN[sh[-1]] if sh else '-'} is a residual difference inside R500; different radius, no check.")
    # hand estimates
    HE = {}
    HE["HE-a"] = dict(claim="0-0.25 bin Delta_b in [-0.10, 0]", value=prim["delta"][0] if prim["shared"][0] else None, hit=bool(prim["shared"][0] and -0.10 <= prim["delta"][0] <= 0.0))
    HE["HE-b"] = dict(claim="S2 lensing need within x1.3 of X-COP's in the same bin", value=(needL[0] / needH[0]) if b2 is not None else None, hit=bool(b2 is not None and abs(math.log10(needL[0] / needH[0])) <= math.log10(1.3)))
    HE["HE-c"] = dict(claim="D1 extends the lensing leg to the 0.75-1.0 bin for >= 10 clusters", value=int(prim["L"]["n"][3]), hit=bool(prim["L"]["n"][3] >= 10), note="D1 NOT RUN (profiles are figures only)")
    HE["HE-d"] = dict(claim="S3 lensing scatter exceeds hydrostatic by >= 0.05 dex (pooled over shared bins)", value=S3["pooled_shared_lensing"] - S3["pooled_shared_hydrostatic"], hit=bool(S3["pooled_shared_lensing"] - S3["pooled_shared_hydrostatic"] >= 0.05))
    RES["HE"][f] = HE
    def hev(v): return "-" if v["value"] is None else (f"{v['value']:+.3f}" if isinstance(v["value"], float) else str(v["value"]))
    P("  hand estimates: " + "; ".join(f"{k} {'HIT' if v['hit'] else 'MISS'} ({hev(v)})" for k, v in HE.items()))
    RES["samples"][f] = dict(primary={k: v for k, v in prim.items() if k not in ("SL", "SH")}, bracket_all20={k: v for k, v in brac.items() if k not in ("SL", "SH")},
                             bracket_donahue_r500={k: v for k, v in bracD.items() if k not in ("SL", "SH")}, hyd_noA2319={k: v for k, v in noA.items() if k not in ("SL", "SH")}, hyd_all12_imputed={k: v for k, v in h12.items() if k not in ("SL", "SH")}, hyd_matched_x={k: v for k, v in mx.items() if k not in ("SL", "SH")},
                             per_cluster_lensing=dict(zip(nL, ML.tolist())), per_cluster_hydrostatic=dict(zip(nH, MH.tolist())), shared_bins=[BIN[b] for b in sh])
    # ---------------- MUTATE
    if MUT:
        MU = {}
        # M1 legs swapped: every Delta_b flips sign (identity on the grader)
        D1 = np.array(prim["H"]["median"]) - np.array(prim["L"]["median"]); flip = all(abs(D1[b] + prim["delta"][b]) < 1e-12 for b in sh)
        sw = dict(prim); sw = dict(L=prim["H"], H=prim["L"], delta=(-np.array(prim["delta"])).tolist(), dlo=(-np.array(prim["dhi"])).tolist(), dhi=(-np.array(prim["dlo"])).tolist(), shared=prim["shared"])
        swb = dict(L=brac["H"], H=brac["L"], delta=(-np.array(brac["delta"])).tolist(), dlo=(-np.array(brac["dhi"])).tolist(), dhi=(-np.array(brac["dlo"])).tolist(), shared=brac["shared"])
        lab_sw, _ = label(sw, swb); MU["M1"] = dict(flips=bool(flip), swapped_label=lab_sw, holds=bool(flip))
        P(f"  M1 legs swapped: Delta_b -> " + ", ".join(f"{BIN[b]} {D1[b]:+.3f}" for b in sh) + f"; sign flips exactly: {flip}; swapped-leg label {lab_sw} -> {'HOLDS' if flip else 'BROKEN'}")
        # M2 plant +-0.30 dex on the lensing leg's innermost shared bin
        if sh:
            b0 = sh[0]; r2 = {}
            for sgn, want in ((+0.30, "LENSING-SPECIFIC"), (-0.30, "HYDROSTATIC-SPECIFIC")):
                MLp = ML.copy(); MLp[:, b0] += sgn; MLap = MLa.copy(); MLap[:, b0] += sgn; rngm = np.random.default_rng(SEED)
                pp = compare(MLp, MH, rngm); bb = compare(MLap, MH, rngm); labp, _ = label(pp, bb); r2[f"{sgn:+.2f}"] = dict(label=labp, delta_b0=pp["delta"][b0], lo=pp["dlo"][b0], hi=pp["dhi"][b0], wanted=want, bites=bool(labp == want))
                P(f"  M2 plant {sgn:+.2f} dex on lensing {BIN[b0]}: Delta_b {pp['delta'][b0]:+.3f} [{pp['dlo'][b0]:+.3f}, {pp['dhi'][b0]:+.3f}] -> label {labp} (wanted {want}) -> {'BITES' if labp == want else 'NO BITE'}")
            MU["M2"] = dict(runs=r2, bites=bool(all(v["bites"] for v in r2.values())))
        else: MU["M2"] = dict(runs={}, bites=False)
        # M3 a0 -> 10 a0 on the lensing leg only: Delta_b must move by more than its interval in every shared bin
        _, ML10, _ = matrix(L_prim, f, a0_override=10 * a0); rngm = np.random.default_rng(SEED); p10 = compare(ML10, MH, rngm); m3 = []
        for b in sh:
            mv = abs(p10["delta"][b] - prim["delta"][b]); width = prim["dhi"][b] - prim["dlo"][b]; m3.append(dict(bin=BIN[b], move=mv, width=width, half=width / 2, bites=bool(mv > width)))
        MU["M3"] = dict(bins=m3, bites=bool(m3 and all(x["bites"] for x in m3)))
        P(f"  M3 a0 -> 10 a0 on the lensing leg: Delta_b moves by " + ", ".join(f"{x['bin']} {x['move']:.3f} vs interval width {x['width']:.3f}" for x in m3) + f" -> {'BITES' if MU['M3']['bites'] else 'NO BITE'}")
        RES["MUTATE"][f] = MU
        if not MU["M2"]["bites"]: lab = "UNDECIDED (NO POWER)"
    RES["label"][f] = dict(label=lab, shared_bins=[BIN[b] for b in sh])
    P(f"  LABEL [{f}]: {lab}  (shared bins {[BIN[b] for b in sh]})")
P(); P("LABELS: " + " / ".join(f"{f} {RES['label'][f]['label']}" for f in A0) + ". S2 is reported, not graded. kappa = 1/2 FITTED; not theory closed. Adopts nothing.")
RES["rss_MB"] = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1e6; P(f"peak RSS {RES['rss_MB']:.0f} MB")
json.dump(RES, open(os.path.join(HERE, TAG + ".json"), "w"), indent=1, default=float); open(os.path.join(HERE, TAG + ".out"), "w").write("\n".join(OUT) + "\n")
