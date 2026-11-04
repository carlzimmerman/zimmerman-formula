#!/usr/bin/env python3
"""FN2 A2 (FROZEN_CRITERIA.md, 755f05c3cf): PAPER66 v1.4 scorecard rows A, B0-B5 read from the scorers' output JSON.
Only stored fields and the AC1 scorer's own frozen functions (alpha_req, separated), imported read only, are used. It prints each
row's fields and evaluates a counter-outcome only where the tex states one (A, B3, B4). No other verdict word.
    python3 -B fn2_scorecard.py --known [--mutate]                       known answers K-A2a..g against the tex; MUTATE = R31 x 10
    python3 -B fn2_scorecard.py --read AC1_JSON [--kind K] [--u4 U4_JSON] [--tag T]   rows for a release (or MOCK) result
Writes fn2_scorecard[_MUTATE].out/.json (--known) or fn2_scorecard_read_<tag>.out/.json (--read) in this lane only.
kappa = 1/2 FITTED; footings never pooled; one disc excludes no model; not theory closed."""
import contextlib, io, json, math, os, re, sys
sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
AC1 = os.path.join(ROOT, "rebuild_2026_10_22", "AC1_alma_condor_predictions")
ARGS = sys.argv[1:]; MUT = "--mutate" in ARGS; TAG = "_MUTATE" if MUT else ""
def opt(k, d=None): return ARGS[ARGS.index(k) + 1] if k in ARGS else d
# ---- the AC1 scorer, imported read only (it consumes sys.argv at import; nothing is written at import) ----
_argv = sys.argv; sys.argv = [os.path.join(AC1, "ac1_score.py")]; sys.path.insert(0, AC1)
with contextlib.redirect_stdout(io.StringIO()):
    import ac1_score as S
sys.argv = _argv
if MUT: S.LP10 = S.LP10 * 10.0     # R31 x 10 in the L' conversion, as AC1's own MUTATE
OUT = []
def P(s=""): print(s, flush=True); OUT.append(str(s))
CAN, ALT = [k for k in S.FOOT if k.startswith("canon")][0], [k for k in S.FOOT if k.startswith("alt")][0]
RES = json.load(open(os.path.join(AC1, "ac1_results.json"))); FWD = RES["B"]["forward"]; RGRID = [1, 2, 3, 4, 6, 8]
TRUE = lambda x: str(x) in ("True", "true", "1")
fm = lambda x: "FLOOR" if x is None else f"{x:.3f}"

# ---- the map, checked against PAPER66 v1.4 Table t:card (row text quoted from the tex) ----
MAP = [
 ("A", "U4_27928: G1 fails, nothing scored", "G1 passing at its frozen aperture counts against this forecast.",
  "cfg942_u4_RELEASE_results.json (CFG942 dir; byte-identical copy CFG806_u4_27928_scoring/cfg806_u4_results.json)",
  "results.measured.G1 (selection-aware S/N decides, CFG806 addendum A); results.measured.SN_selection; results.measured.G1_literal (information); results.measured.logMgas_UL; results.score.overall",
  "direct"),
 ("B0", "U4_28473 detected and V_c scored, conditional on the sister-unit noise and beam forecast",
  "Report measured noise/beam, detection and fit validity. Non-detection or an invalid fit challenges the forecast only under its stated conditions.",
  "ac1_score_RELEASE.json", "detected, gate, G1_3D.{S,SN,PASS}, G1_frozen.{SN,PASS} (printed beside); sig_ch and dv (noise per 10 km/s = sig_ch*sqrt(dv/10)); beam; fits.<incl>.valid",
  "direct fields; GAP: the tex gives no numeric tolerance for 'the sister-unit noise and beam hold', so measured/forecast ratios are printed with no call"),
 ("B1", "V_c >= Newton for the true baryons; lowest input-grid branch at 3 kpc is 431 km/s",
  "Compare the mass/pressure branches and uncertainties. A value below the grid challenges those inputs; it is not an unconditional test of a0.",
  "ac1_score_RELEASE.json + ac1_results.json", "fits.<incl>.V.{Vc_PB,Vc_P0}, fits.<incl>.error_calibration.<P-B|P0>.error, fits.<incl>.R_score; score.<branch>.<lgM*|shape>.'Newton|...' class",
  "GAP: no stored 'Newton grid at R_score' field; computed here from the frozen inputs (v2_exp, logMgas), z = (V - V_N,min)/error printed, no call (the tex gives no numeric line)"),
 ("B2", "Conditional example: at V_c ~ 430, alpha_CO = 4.36 with published masses is out for every reading",
  "Evaluate the branch-specific required gas conversion and interval. A different speed makes the 430 example inapplicable; it does not falsify the implication.",
  "ac1_score_RELEASE.json", "score.<branch>.<lgM*11.31|S1/S2, 11.35|S1/S2>.<kernel|footing|a0>.{nominal,lo,hi,class_}",
  "GAP: lg M* 11.11 (the tex's 0.88) is not a stored key (the scorer stores 11.31 and 11.35; 11.11 enters only as an interval end); recomputed with alpha_req. GAP: 'near 430' has no numeric width in the tex; |V-430|/error printed. Applies only if R_score = 3 kpc."),
 ("B3", "flat, F-DESI and the band not separated", "Any pair separated under the filed rule counts against this forecast.",
  "ac1_score_RELEASE.json", "score.<branch>.<lgM*|shape>.<kernel|footing|{F-flat,F-DESI,band low 0.325,band high 1.212}>.{nominal,ms_width}; rule = ac1_score.separated",
  "computed from stored fields (the scorer prints only flat vs R-H)"),
 ("B4", "R-H not separated", "Separation under the same rule counts against this forecast.",
  "ac1_score_RELEASE.json", "same fields, pair F-flat vs R-H; the scorer's printed line 'flat vs R-H: separated|not separated' (lg M* 11.31, canonical, n = 1)",
  "direct for the printed cells; computed from stored fields for the rest"),
 ("B5", "record only (route N retired)", "No live score.", "ac1_score_RELEASE.json", "score.<branch>.<lgM*|shape>.'route N|12.0/12.5/13.0' (computed, no weight)", "record only"),
]

def newton_v(lms, sh, alpha, R):
    """Newtonian V_c (km/s) of stars + gas at R kpc, from the frozen inputs the forward table used (exponential discs)."""
    Rd = S.SHAPES[sh] / 1.678; mg = 10 ** RES["B"]["logMgas"][alpha]
    return math.sqrt(S.PR["ns"]["v2_exp"](10 ** lms, Rd, R) + S.PR["ns"]["v2_exp"](mg, S.RDG, R))

def known():
    K = []
    def k(n, ok, x): K.append((n, bool(ok))); P(f"[{'PASS' if ok else 'FAIL'}] {n}: {x}")
    f = FWD["lgM*11.11|S2|alpha1.0"]; i3, i8 = RGRID.index(3), RGRID.index(8)
    vN = f["Newton"][i3]; vNf = newton_v(11.11, "S2", "1.0", 3.0)
    k("K-A2a B1 Newton V_c(3 kpc), lg M* 11.11, S2, alpha_CO 1 = 431 (tex) +- 0.5", abs(vN - 431) <= 0.5 and abs(vNf - vN) < 1e-6 * vN, f"ac1_results.json {vN:.3f}; recomputed from the frozen inputs {vNf:.3f}")
    a0c = S.FOOT[CAN] * S.RF0["F-flat"]
    a11, a31 = S.alpha_req(3.0, 430.0, 11.11, "S2", "n=1", a0=a0c), S.alpha_req(3.0, 430.0, 11.31, "S2", "n=1", a0=a0c)
    info = RES["B"]["halpha_430_at_3kpc_information"]
    k("K-A2b B2 alpha_CO,req at V_c 430, 3 kpc, n=1 flat canonical: 0.88 (11.11 S2) and 0.07 (11.31 S2) +- 0.005",
      a11 is not None and a31 is not None and abs(a11 - 0.88) <= 0.005 and abs(a31 - 0.07) <= 0.005, f"{fm(a11)} / {fm(a31)}; ac1_results.json information block {info['lgM*11.11|S2']['n=1|F-flat']} / {info['lgM*11.31|S2']['n=1|F-flat']}")
    s1 = {l: S.alpha_req(3.0, 430.0, l, "S1", "n=1", a0=a0c) for l in (11.11, 11.15, 11.31, 11.35)}
    k("K-A2c B2 every S1 branch FLOOR at V_c 430 (lg M* 11.11, 11.15, 11.31, 11.35)", all(v is None for v in s1.values()), ", ".join(f"{l}: {fm(v)}" for l, v in s1.items()))
    d3 = f[f"n=1|{CAN}|F-flat"][i3] - f[f"n=1|{CAN}|F-DESI"][i3]
    k("K-A2d B3 flat - F-DESI at 3 kpc = 2 km/s (tex) +- 0.5", abs(d3 - 2) <= 0.5, f"{d3:.3f}")
    d4 = f[f"n=1|{CAN}|R-H"][i3] - f[f"n=1|{CAN}|F-flat"][i3]
    k("K-A2e B4 R-H - flat at 3 kpc = 22 km/s (tex) +- 0.5", abs(d4 - 22) <= 0.5, f"{d4:.3f}")
    d5a, d5b = f[f"n=1|{CAN}|F-flat"][i3] - f["route N|12.5"][i3], f[f"n=1|{CAN}|F-flat"][i8] - f["route N|12.5"][i8]
    k("K-A2f B5 n=1 flat - route N 12.5 = 9 (3 kpc) and 22 (8 kpc) km/s (tex) +- 0.5", abs(d5a - 9) <= 0.5 and abs(d5b - 22) <= 0.5, f"{d5a:.3f} / {d5b:.3f}")
    # K-A2g: the reader's flat vs R-H call against the scorer's own printed call, every printed cell of a MOCK selftest
    sj = opt("--selftest-json", os.path.join(ROOT, "reviews/alma_readiness_2026_11_04/revision_v1_4/selftest/ac1_score_selftest_results.json"))
    so = os.path.join(os.path.dirname(sj), "ac1_score_selftest.out"); J = json.load(open(sj))["results"]
    printed = []; kind = None; cur = None
    for line in open(so):
        m = re.match(r"=== MOCK (\w+):", line.strip()); kind = m.group(1) if m else kind
        if line.strip().startswith("--- MUTATE"): kind = "bright_MUTATE"
        m = re.match(r"\s+(\S+\|\S+) (lgM\*[\d.]+\|S\d): alpha_req", line); cur = (kind, m.group(1), m.group(2)) if m else cur
        m = re.match(r"\s+flat vs R-H: (separated|not separated)", line)
        if m and cur: printed.append((cur, m.group(1) == "separated"))
    bad = [c for c, p in printed if S.separated(J[c[0]]["score"][c[1]][c[2]][f"n=1|{CAN}|F-flat"], J[c[0]]["score"][c[1]][c[2]][f"n=1|{CAN}|R-H"]) != p]
    k("K-A2g reader's flat vs R-H call equals the scorer's printed call on a MOCK selftest", printed and not bad, f"{len(printed)} printed cells, {len(bad)} differ ({os.path.relpath(sj, ROOT)})")
    return K

def rows(m, u4=None):
    R = {}
    # A
    if u4 is not None:
        me, sc = u4["results"]["measured"], u4["results"]["score"]
        R["A"] = dict(G1=TRUE(me["G1"]), SN_selection=me["SN_selection"], G1_literal_information=TRUE(me["G1_literal"]), logMgas_UL=me.get("logMgas_UL"),
                      overall=sc.get("overall"), object=me.get("object"), counter_outcome_met=TRUE(me["G1"]))
    else: R["A"] = dict(note="needs cfg942_u4's results JSON (--u4)")
    # B0
    n10 = m["sig_ch"] * 1e3 * math.sqrt(m["dv"] / 10)
    R["B0"] = dict(detected=TRUE(m["detected"]), gate=m.get("gate"), G1_3D_SN=m["G1_3D"]["SN"], G1_3D_PASS=TRUE(m["G1_3D"]["PASS"]), G1_frozen_SN=m["G1_frozen"]["SN"],
                   G1_frozen_PASS=TRUE(m["G1_frozen"]["PASS"]), noise_mJy_per_10kms=n10, noise_over_sister_forecast_0171=n10 / 0.171, noise_over_listed_0434=n10 / 0.4342,
                   beam_arcsec=m["beam"][:2], beam_over_forecast=[m["beam"][0] / 0.109, m["beam"][1] / 0.085],
                   fits_valid={nm: TRUE(f["valid"]) for nm, f in (m.get("fits") or {}).items()}, object=m.get("object"))
    fits = m.get("fits") or {}; sc = m.get("score") or {}
    # B1
    b1 = {}
    for nm, f in fits.items():
        if not TRUE(f["valid"]): b1[nm] = "FIT NOT CONSTRAINED: not scored"; continue
        Rs = float(f["R_score"]); grid = {f"lgM*{l}|{sh}|alpha{a}": newton_v(l, sh, a, Rs) for l in (11.11, 11.15, 11.31, 11.35) for sh in ("S1", "S2") for a in ("1.0", "4.36")}
        lo_k = min(grid, key=grid.get)
        for bn, vk in (("P-B", "Vc_PB"), ("P0", "Vc_P0")):
            V, e = float(f["V"][vk]), float(f["error_calibration"][bn]["error"])
            b1[f"{nm}|{bn}"] = dict(R_score_kpc=Rs, G2_reached=TRUE(f["G2_reached"]), V=V, error=e, newton_grid_min=grid[lo_k], newton_grid_min_branch=lo_k, z_vs_grid_min=(V - grid[lo_k]) / e,
                                   extrapolated_below_0p5kpc=Rs <= 0.5 and float(f["R90_dep_kpc"]) < 0.5,
                                   newton_classes={k_: sc.get(f"{nm}|{bn}", {}).get(k_, {}).get(f"Newton|{CAN}|F-flat", {}).get("class_") for k_ in sc.get(f"{nm}|{bn}", {})})
    R["B1"] = b1
    # B2
    b2 = {}
    for bn, (V, e, Rs) in ((k_, (v[0], v[1], v[2])) for k_, v in (m.get("branches") or {}).items()):
        V, e, Rs = float(V), float(e), float(Rs); a0c = S.FOOT[CAN]
        x = dict(applicable_R3=abs(Rs - 3.0) < 1e-9, V=V, error=e, dist_430_in_error=(V - 430.0) / e,
                 alpha_req_n1_flat_canon={f"{l}|{sh}": S.alpha_req(Rs, V, l, sh, "n=1", a0=a0c) for l in (11.11, 11.31) for sh in ("S1", "S2")})
        out = tot = 0
        for k_, row in sc.get(bn, {}).items():
            for rd, iv in row.items():
                if rd.startswith(("Newton", "route N")): continue
                tot += 1; lo, hi = (0.0 if iv["lo"] is None else iv["lo"]), iv["hi"]
                out += int(iv["class_"] == "FLOOR" or hi is None or not (lo <= 4.36 <= hi))
        x.update(readings_with_4p36_outside_interval=out, readings=tot); b2[bn] = x
    R["B2"] = b2
    # B3, B4
    PAIRS3 = [("F-flat", "F-DESI"), ("F-flat", "band low 0.325"), ("F-flat", "band high 1.212"), ("F-DESI", "band low 0.325"), ("F-DESI", "band high 1.212"), ("band low 0.325", "band high 1.212")]
    b3, b4 = {}, {}
    for bn, srow in sc.items():
        for k_, row in srow.items():
            for kn in ("n=1", "nu_mono", "n=2"):
                for fn in (CAN, ALT):
                    g = lambda a: row[f"{kn}|{fn}|{a}"]
                    b3[f"{bn}|{k_}|{kn}|{fn}"] = [p for p in PAIRS3 if S.separated(g(p[0]), g(p[1]))]
                    b4[f"{bn}|{k_}|{kn}|{fn}"] = S.separated(g("F-flat"), g("R-H"))
    R["B3"] = dict(cells=len(b3), cells_with_a_separated_pair=sum(1 for v in b3.values() if v), n1_canonical_cells_with_a_separated_pair=sum(1 for c, v in b3.items() if v and "|n=1|canon" in c),
                   counter_outcome_met=any(b3.values()), separated=[c for c, v in b3.items() if v])
    R["B4"] = dict(cells=len(b4), cells_separated=sum(b4.values()), n1_canonical_cells_separated=sum(1 for c, v in b4.items() if v and "|n=1|canon" in c), counter_outcome_met=any(b4.values()))
    R["B5"] = dict(note="record only (route N retired); no live score")
    return R

if __name__ == "__main__":
    P(f"FN2 A2 scorecard reader. AC1 scorer imported read only (sha256 {__import__('hashlib').sha256(open(os.path.join(AC1, 'ac1_score.py'), 'rb').read()).hexdigest()[:16]}...)."
      + (" MUTATE: R31 x 10 in the L' conversion." if MUT else "") + " kappa = 1/2 FITTED; one disc excludes no model; not theory closed.")
    if "--known" in ARGS:
        P("\nRow map, PAPER66 v1.4 Table t:card:")
        for r, pred, ev, fil, fld, note in MAP: P(f"  {r}: '{pred}' | evaluation: '{ev}' | file: {fil} | fields: {fld} | {note}")
        P("\nKnown answers against the tex:"); K = known(); ok = all(o for _, o in K)
        P(f"\nknown answers: {sum(o for _, o in K)} of {len(K)} PASS" + (" (MUTATE: K-A2b must fail)" if MUT else ""))
        json.dump(dict(map=[dict(zip(("row", "prediction", "evaluation", "file", "fields", "note"), x)) for x in MAP], known=K, mutate=MUT),
                  open(os.path.join(HERE, f"fn2_scorecard{TAG}.json"), "w"), indent=1)
        open(os.path.join(HERE, f"fn2_scorecard{TAG}.out"), "w").write("\n".join(OUT) + "\n")
        if MUT:
            bit = not dict(K)["K-A2b B2 alpha_CO,req at V_c 430, 3 kpc, n=1 flat canonical: 0.88 (11.11 S2) and 0.07 (11.31 S2) +- 0.005"]
            P(f"MUTATE {'bites' if bit else 'DOES NOT BITE'}"); open(os.path.join(HERE, f"fn2_scorecard{TAG}.out"), "a").write(f"MUTATE {'bites' if bit else 'DOES NOT BITE'}\n"); sys.exit(1)
        sys.exit(0 if ok else 1)
    if "--read" in ARGS:
        J = json.load(open(opt("--read"))); m = J["results"][opt("--kind")] if opt("--kind") else J
        u4 = json.load(open(opt("--u4"))) if opt("--u4") else None; R = rows(m, u4); tag = opt("--tag", "release")
        if str(m.get("object")) == "MOCK": P("*** MOCK input, NOT ALMA DATA ***")
        for r in ("A", "B0", "B1", "B2", "B3", "B4", "B5"): P(f"{r}: " + json.dumps(R[r], default=str))
        json.dump(R, open(os.path.join(HERE, f"fn2_scorecard_read_{tag}.json"), "w"), indent=1, default=str)
        open(os.path.join(HERE, f"fn2_scorecard_read_{tag}.out"), "w").write("\n".join(OUT) + "\n"); sys.exit(0)
    print(__doc__); sys.exit(2)
