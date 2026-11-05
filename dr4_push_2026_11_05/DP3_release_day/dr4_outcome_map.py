#!/usr/bin/env python3
"""DP3: the Gaia DR4 outcome-map scorer (NEW file; criteria FROZEN_CRITERIA.md, committed alone before this code).

It prints, per footing and never pooled, the label of the filed outcome map (OWNER_DECISION_2026-11-05_DR4_FORKS.md, 413c1c8e24,
D1-D6 adopted; D7/D8 closed by d71a111d1d) for the frozen D2 rows (NOTE_2026-10-22_FORK_SCORING_PRE_DR4.md, A1-A3), the R label
of the 10-21 kill line (campaign_fresh_gravity/OWNER_DECISION_2026-10-21_DR4_KILL_LINE.md) and every split, as a split.
Order of evaluation (criteria section 2): guard zone > 1.23 -> sub-Newton <= 1 - 3 sigma_b -> gate sigma_sys(b) < 0.048 / 0.058
-> rows under (b) (D5: overlap = BOTH EXCLUDED) -> robustness (a), (e), (g2) must give the identical label (A3.2).
It decides nothing about any number it is given: it only applies frozen rows. Newton-side wording: "v3s survives", never confirmed.

Run:
  python3 -B dr4_outcome_map.py --self-test                       (known answers; DP3_MUTATE=1 / 2 must make it fail)
  python3 -B dr4_outcome_map.py --pipeline-log pipeline_dr4.log --sigma-json sigma_sys_dr4.json --r-json cfg816_r_dr4_results.json --tag DR4
  python3 -B dr4_outcome_map.py --gamma canonical=1.004,alt=1.010 --sigma-fit canonical=0.019,alt=0.019 \
        --sig canonical:b=0.020,a=0.020,e=0.016,g2=0.022 --sig alt:b=0.020,a=0.020,e=0.018,g2=0.022 --R 1.003 --sigma-R 0.075 --N-R 2100
kappa = 1/2 FITTED; footings never pooled; not theory closed. Nothing here says the data favour the framework.
"""
import sys
sys.dont_write_bytecode = True
import argparse, json, math, os, re

MUT = os.environ.get("DP3_MUTATE", "").strip()
K = 2.0 if MUT == "1" else 3.0                    # MUTATE 1: the wrong sigma multiple
D5_ON = MUT != "2"                                # MUTATE 2: the frozen precedence (D5 not applied)

NEWTON = 1.000                                    # D3(a)
ANCHOR = {"canonical": 1.1614, "alt": 1.1917}     # Arm A floors (prereg Amendment 10; D2 rows; D2(a))
GUARD = 1.23                                      # prereg no-verdict edge; kill-line note N3
GATE = {"canonical": 0.048, "alt": 0.058}         # D2 A1 (tighter ceilings, every frozen g_ext)
SYS_A = 0.020                                     # frozen allowance (PREREG 1.5), definition (a)
GEXT = {"primary 1.778e-10 m/s^2": {"canonical": 1.1666821011084045, "alt": 1.1985790300437524},     # A3 / A1 AQUAL anchors
        "alternative 2.078e-10 m/s^2": {"canonical": 1.1447841306286448, "alt": 1.173011927619301}}  # (d2_sigma_sys_defs.py PRED)
INFO_NUMBERS = {"canonical": "bare law CW1 1.149 +- 0.027; D2 sec 4 QUMOND 1.175 / 1.151; FN6 window 1.00-1.04 (p <= 0.4)",
                "alt": "bare law CW1 1.208 +- 0.007; D2 sec 4 QUMOND 1.210 / 1.182; FN6 alt p 0.45 1.13-1.21"}
R_KILL_MIN, R_CONS_MIN, R_K_KILL, R_K_CONS = 0.01, 0.01, 3.0, 2.0      # CFG825 (cfg816_r.py), Amendment 22
FOOTINGS = ("canonical", "alt")
VERDICTS = ("LAW_FIRST_EXCLUDED", "SCREENED_EXCLUDED", "BOTH_EXCLUDED")
WORDS = {
    "LAW_FIRST_EXCLUDED": "Newton side: v3s survives (not confirmed); bare law excluded (law-first reading of the D2 rows, gate holds)",
    "SCREENED_EXCLUDED": "boost side: v3s EXCLUDED (screened / medium-first reading); bare law survives this test",
    "BOTH_EXCLUDED": "BOTH EXCLUDED (D5): >= 3 sigma above Newton and >= 3 sigma below the law-first anchor; neither reading fits",
    "UNDECIDED": "UNDECIDED: no verdict word; raw gamma-hat, every sigma and both distances reported",
    "UNDECIDED_GATE": "UNDECIDED (gate): sigma_sys(b) at or above the D2 A1 ceiling; no verdict word, whatever gamma-hat is",
    "UNDECIDED_ROBUSTNESS": "UNDECIDED (A3.2): a robustness definition (a), (e) or (g2) gives a different label or is missing; no verdict word",
    "GUARD_ZONE": "guard zone (gamma-hat > 1.23): no verdict for every reading; never read as survival",
    "SUB_NEWTON_NO_VERDICT": "sub-Newtonian (gamma-hat <= 1 - 3 sigma): pipeline or contamination fault, NO VERDICT for every reading (D4)",
}
FIT_RE = re.compile(r"^\s*catalog \[a0 (canonical|alt footing)\]\s+gamma_inf = (\S+) \+- (\S+)\s+\(chi2/bin=(\S+), bins=(\d+), kappa=(\S+)\)", re.M)


def sig_tot(sfit, ssys):
    return math.sqrt(sfit ** 2 + ssys ** 2)


def rows(g, sfit, ssys, anchor):
    """Steps 2 and 4 for one sigma_sys and one anchor: the label and the numbers."""
    s = sig_tot(sfit, ssys)
    if g <= NEWTON - K * s:
        return "SUB_NEWTON_NO_VERDICT", s
    lf = (anchor - g) >= K * s
    sc = (g - NEWTON) >= K * s
    if lf and sc:
        return ("BOTH_EXCLUDED" if D5_ON else "LAW_FIRST_EXCLUDED"), s
    if lf:
        return "LAW_FIRST_EXCLUDED", s
    if sc:
        return "SCREENED_EXCLUDED", s
    return "UNDECIDED", s


def label(foot, g, sfit, sys_defs, anchor=None):
    """The filed label for one footing. sys_defs: {'b': .., 'a': .., 'e': .., 'g2': ..} (a missing key = not supplied)."""
    anchor = ANCHOR[foot] if anchor is None else anchor
    b = sys_defs.get("b")
    if b is None:
        raise ValueError("sigma_sys(b) is required (A3.1 primary)")
    s_b = sig_tot(sfit, b)
    out = dict(footing=foot, gamma=g, sigma_fit=sfit, sigma_sys=dict(sys_defs), sigma_b=s_b, anchor=anchor,
               edge_law_first_excluded_if_le=anchor - K * s_b, edge_screened_excluded_if_ge=NEWTON + K * s_b,
               edge_sub_newton_le=NEWTON - K * s_b, z_from_newton=(g - NEWTON) / s_b, z_below_anchor=(anchor - g) / s_b,
               gate_ceiling=GATE[foot], gate_pass=b < GATE[foot], robustness={})
    if g > GUARD:
        out["label"] = "GUARD_ZONE"; return out
    lab_b, _ = rows(g, sfit, b, anchor)
    if lab_b == "SUB_NEWTON_NO_VERDICT":
        out["label"] = lab_b; return out
    if not out["gate_pass"]:
        out["label"] = "UNDECIDED_GATE"; out["rows_b_label_information"] = lab_b; return out
    out["rows_b_label"] = lab_b
    if lab_b not in VERDICTS:
        out["label"] = lab_b
        for d in ("a", "e", "g2"):
            if sys_defs.get(d) is not None:
                out["robustness"][d] = rows(g, sfit, sys_defs[d], anchor)[0]
        return out
    ok = True
    for d in ("a", "e", "g2"):
        v = sys_defs.get(d)
        if v is None:
            out["robustness"][d] = "MISSING"; ok = False; continue
        ld = rows(g, sfit, v, anchor)[0]
        out["robustness"][d] = ld
        ok = ok and (ld == lab_b)
    out["label"] = lab_b if ok else "UNDECIDED_ROBUSTNESS"
    return out


def r_label(R, sR):
    if R - 1 >= R_KILL_MIN and R - 1 >= R_K_KILL * sR:
        return "KILLED"
    if abs(R - 1) < R_CONS_MIN and R_K_CONS * sR <= R_CONS_MIN:
        return "CONSISTENT"
    return "UNDECIDED"


def splits(res, rlab):
    out = []
    labs = {f: res[f]["label"] for f in res}
    if len(labs) == 2 and len(set(labs.values())) > 1:
        out.append(f"SPLIT (footings): canonical {labs['canonical']} vs alt {labs['alt']}; reported separately, never pooled")
    if rlab is not None:
        for f, l in labs.items():
            g_ex = l in ("SCREENED_EXCLUDED", "BOTH_EXCLUDED")
            if g_ex and rlab != "KILLED":
                out.append(f"SPLIT (gamma-hat rows vs R, N6), {f}: gamma-hat {l}, R {rlab}; never merged into one framework verdict")
            if rlab == "KILLED" and not g_ex:
                out.append(f"SPLIT (gamma-hat rows vs R, N6), {f}: R KILLED (CFG740), gamma-hat {l}; never merged into one framework verdict")
    for f in res:
        for gk, info in res[f].get("gext_information", {}).items():
            if info["label"] != res[f]["label"] and res[f]["label"] in VERDICTS + ("UNDECIDED",):
                out.append(f"information split ({f}, g_ext {gk}): A3 AQUAL-anchor reading {info['label']} vs the Arm A rows {res[f]['label']} "
                           f"(D2(a) keeps the Arm A rows; no verdict weight)")
    return out


def score(gam, sfit, sysd, R=None, sR=None, NR=None, tag="", nss_status=None):
    """Full report. gam, sfit: {footing: value}; sysd: {footing: {'b','a','e','g2'}}."""
    L, res = [], {}
    P = L.append
    P(f"DR4 OUTCOME MAP ({tag or 'untagged'}). kappa = 1/2 FITTED; footings never pooled; not theory closed."
      + ("  [DP3_MUTATE=%s]" % MUT if MUT else ""))
    P(f"  frozen rows: Newton {NEWTON:.3f}; law-first anchor = Arm A floor (canonical {ANCHOR['canonical']}, alt {ANCHOR['alt']}); "
      f"guard > {GUARD}; gate sigma_sys(b) < {GATE['canonical']} / {GATE['alt']}; sigma = sqrt(sigma_fit^2 + sigma_sys^2); {K:g} sigma")
    for f in FOOTINGS:
        if f not in gam:
            continue
        r = label(f, gam[f], sfit[f], sysd[f])
        r["gext_information"] = {}
        for gk, an in GEXT.items():
            ri = label(f, gam[f], sfit[f], sysd[f], anchor=an[f])
            r["gext_information"][gk] = dict(anchor=an[f], label=ri["label"], z_below_anchor=ri["z_below_anchor"],
                                             edge_law_first_excluded_if_le=ri["edge_law_first_excluded_if_le"])
        res[f] = r
        sd = sysd[f]
        P(f"[{f}] gamma-hat {gam[f]:.4f}  sigma_fit {sfit[f]:.4f}  sigma_sys (b) {sd.get('b')}  (a) {sd.get('a')}  (e) {sd.get('e')}  (g2) {sd.get('g2')}"
          f"  -> sigma_b {r['sigma_b']:.4f}")
        P(f"[{f}] D2 rows (Arm A anchor {r['anchor']}): law-first excluded if gamma-hat <= {r['edge_law_first_excluded_if_le']:.4f}; "
          f"screened excluded if >= {r['edge_screened_excluded_if_ge']:.4f}; sub-Newton if <= {r['edge_sub_newton_le']:.4f}; "
          f"distances (g-1)/sigma {r['z_from_newton']:+.2f}, (anchor-g)/sigma {r['z_below_anchor']:+.2f}; gate {'PASS' if r['gate_pass'] else 'FAIL'}")
        if r["robustness"]:
            P(f"[{f}] robustness (A3.2): " + ", ".join(f"({d}) {v}" for d, v in r["robustness"].items()))
        P(f"[{f}] LABEL: {r['label']}  --  {WORDS[r['label']]}")
        for gk, info in r["gext_information"].items():
            P(f"[{f}] information only, g_ext {gk}: A3 AQUAL anchor {info['anchor']:.4f} -> {info['label']} "
              f"(law-first edge {info['edge_law_first_excluded_if_le']:.4f}, (anchor-g)/sigma {info['z_below_anchor']:+.2f})")
        P(f"[{f}] information only: {INFO_NUMBERS[f]}; Newton reference 1.000 exactly (D3(a)); pipeline Newton draws are information")
    if nss_status:
        P(f"  NSS-off rung (D7 N4): {nss_status}")
    P("  D7 N4.3: the 3-20 kAU ladder rung fails the 1-sigma_fit rule in ~40 % of MOCK repeats under a correct model (CFG943); stated beside any systematic-limited reading")
    rlab = None
    if R is not None and sR is not None:
        rlab = r_label(R, sR)
        need = 1 + max(R_KILL_MIN, R_K_KILL * sR)
        P(f"[R] CFG825 primary: R {R:.4f}  sigma_R {sR:.4f} (from N_R = {NR if NR is not None else '?'} pairs entering R, N1)  -> {rlab}; "
          f"a kill needs R >= {need:.3f}; CONSISTENT is unreachable while sigma_R > 0.005")
        if rlab == "UNDECIDED":
            P("[R] UNDECIDED is neither a kill nor a survival of CFG740 (10-21 kill line)")
    else:
        P("[R] not supplied")
    P("  N7: CFG740 falsifier 1 beyond ~37 kAU and falsifier 2 (log-slope 2) are NOT scored (no registered statistic)")
    P("  D8: the mock-triple injection test, if run, is information only; it changes no sigma_sys, band or verdict")
    sp = splits(res, rlab)
    for s in sp:
        P("  " + s)
    if not sp:
        P("  no split")
    return L, dict(footings=res, R=dict(R=R, sigma_R=sR, N_R=NR, label=rlab), splits=sp, mutate=MUT, k=K, d5=D5_ON)


def sigma_b_from_ladder(base, rungs):
    """A3 (b): max(0.020, 1/2 x full spread of {base} U rungs)."""
    gl = [base] + list(rungs)
    return max(SYS_A, 0.5 * (max(gl) - min(gl)))


# ------------------------------------------------------------------ self-test (criteria section 3)
def self_test():
    L, ok_all = [], True
    def T(name, ok, detail=""):
        nonlocal ok_all
        ok_all = ok_all and bool(ok)
        L.append(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f"  -- {detail}" if detail else ""))
    sf = lambda N: 0.019 * math.sqrt(30000.0 / N)
    cases = [("T1", "canonical", 30000, 0.020, {}, 1.000, "LAW_FIRST_EXCLUDED"),
             ("T2", "canonical", 30000, 0.020, {}, 1.081, "UNDECIDED"),
             ("T3", "canonical", 30000, 0.020, {}, 1.100, "SCREENED_EXCLUDED"),
             ("T4", "canonical", 30000, 0.020, {}, 1.250, "GUARD_ZONE"),
             ("T5", "canonical", 30000, 0.020, {}, 0.900, "SUB_NEWTON_NO_VERDICT"),
             ("T6", "alt", 30000, 0.020, {}, 1.095, "BOTH_EXCLUDED"),
             ("T7", "canonical", 30000, 0.020, {}, 0.920, "LAW_FIRST_EXCLUDED"),
             ("T8", "canonical", 6210, 0.0375, {}, 1.000, "UNDECIDED"),
             ("T9", "canonical", 6210, 0.020, {}, 1.000, "LAW_FIRST_EXCLUDED"),
             ("T10", "canonical", 30000, 0.050, {}, 1.000, "UNDECIDED_GATE"),
             ("T11", "alt", 30000, 0.050, {}, 1.000, "LAW_FIRST_EXCLUDED"),
             ("T12", "canonical", 30000, 0.020, {"e": 0.025}, 1.075, "UNDECIDED_ROBUSTNESS"),
             ("T13", "canonical", 30000, 0.020, None, 1.000, "UNDECIDED_ROBUSTNESS"),
             ("T14", "alt", 30000, 0.020, {}, 1.120, "SCREENED_EXCLUDED")]
    all_lines = []
    for cid, f, N, b, over, g, want in cases:
        sysd = {"b": b} if over is None else dict({"b": b, "a": b, "e": b, "g2": b}, **over)
        lines, rep = score({f: g}, {f: sf(N)}, {f: sysd}, tag=f"self-test {cid}")
        all_lines += lines
        got = rep["footings"][f]["label"]
        T(f"{cid} {f} N {N} sigma_sys(b) {b} gamma-hat {g:.3f} -> {want}", got == want, f"got {got}")
    # E1 the 2c edges
    tab = [(30000, 0.020, 1.079, 1.083), (30000, 0.0375, 1.035, 1.126), (15000, 0.020, 1.061, 1.100),
           (6210, 0.020, 1.022, 1.139), (6210, 0.0375, 0.993, 1.168)]
    e1 = []
    for N, s, lo, hi in tab:
        sb = sig_tot(sf(N), s)
        e1.append(abs(ANCHOR["canonical"] - K * sb - lo) <= 0.0006 and abs(NEWTON + K * sb - hi) <= 0.0006)
    alt = [(30000, 0.020, 1.109), (6210, 0.020, 1.053), (6210, 0.0375, 1.023)]
    for N, s, lo in alt:
        e1.append(abs(ANCHOR["alt"] - K * sig_tot(sf(N), s) - lo) <= 0.0012)
    T("E1 the 2c edge table (5 canonical rows, 3 alt law-first edges)", all(e1), f"{sum(e1)}/{len(e1)}")
    # E2 sigma_sys(b) from the D2 DR3 shifts
    sbc = sigma_b_from_ladder(0.0, [0.015, 0.033, 0.075]); sba = sigma_b_from_ladder(0.0, [-0.013, -0.025, 0.058])
    T("E2 sigma_sys(b) from the D2 DR3 ladder shifts = 0.0375 / 0.0415", abs(sbc - 0.0375) < 1e-9 and abs(sba - 0.0415) < 1e-9,
      f"{sbc:.4f} / {sba:.4f}")
    # E3 the R rule against CFG816's own case table and the kill-line note
    r_cases = [(1.083, 0.028, "UNDECIDED"), (1.085, 0.028, "KILLED"), (1.001, 0.028, "UNDECIDED"), (1.005, 0.004, "CONSISTENT"),
               (1.005, 0.006, "UNDECIDED"), (1.009, 0.002, "CONSISTENT"), (1.011, 0.002, "KILLED"), (1.05, 0.02, "UNDECIDED")]
    e3 = [r_label(R, s) == w for R, s, w in r_cases]
    need = 1 + max(R_KILL_MIN, R_K_KILL * 0.075)
    T("E3 R rule = CFG816 case table (8) and kill-line 'needs R >= 1.22' at sigma_R 0.075", all(e3) and abs(need - 1.225) < 1e-9,
      f"{sum(e3)}/8; needs {need:.3f}")
    try:                                                               # the frozen classify itself, imported read-only, if importable
        here = os.path.dirname(os.path.abspath(__file__))
        sys.path.insert(0, os.path.join(here, "..", "..", "campaign_fresh_gravity", "CFG816_dr4_r_statistic_scoring"))
        import cfg816_r
        e3b = [cfg816_r.classify(R, s) == r_label(R, s) for R, s, _ in r_cases] + [cfg816_r.classify(1.2, 0.075) == r_label(1.2, 0.075)]
        T("E3b r_label == cfg816_r.classify (read-only import) on every case", all(e3b), f"{sum(e3b)}/{len(e3b)}")
    except Exception as exc:                                           # noqa: BLE001
        T("E3b cfg816_r.classify importable", False, repr(exc))
    # E4 wording
    bad = [l for l in all_lines if re.search(r"v3s (is )?confirmed", l)]
    lf_lines = [l for l in all_lines if "LABEL: LAW_FIRST_EXCLUDED" in l]
    T("E4 no 'v3s confirmed'; every LAW_FIRST_EXCLUDED line says 'v3s survives'", not bad and lf_lines and all("v3s survives" in l for l in lf_lines),
      f"{len(bad)} bad lines; {len(lf_lines)} law-first lines")
    # E5 splits: MOCK B3 pattern and a footing disagreement
    _, rep = score({"canonical": 1.165, "alt": 1.095}, {"canonical": 0.019, "alt": 0.019},
                   {f: {"b": 0.02, "a": 0.02, "e": 0.02, "g2": 0.02} for f in FOOTINGS}, R=1.11, sR=0.075, NR=2100, tag="self-test E5")
    sp = rep["splits"]
    T("E5 split detector: gamma-hat SCREENED_EXCLUDED with R UNDECIDED, and canonical vs alt",
      any("gamma-hat SCREENED_EXCLUDED, R UNDECIDED" in s for s in sp) and any(s.startswith("SPLIT (footings)") for s in sp),
      f"{len(sp)} split lines")
    L.append(f"{sum(1 for l in L if '[PASS]' in l)}/{len(L)} checks pass" + (f"  [DP3_MUTATE={MUT}: a failure is REQUIRED]" if MUT else ""))
    return L, ok_all


def parse_kv(s):
    return {k: float(v) for k, v in (x.split("=") for x in s.split(",") if x)}


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--self-test", action="store_true")
    ap.add_argument("--pipeline-log"); ap.add_argument("--gamma"); ap.add_argument("--sigma-fit")
    ap.add_argument("--sigma-json", help="dp3_sigma_sys.py output: {footing: {b, a, e, g2, ...}, nss_off_status}")
    ap.add_argument("--sig", action="append", default=[], help="footing:b=..,a=..,e=..,g2=.. (overrides --sigma-json)")
    ap.add_argument("--r-json", help="cfg816_r results JSON (branches.primary)"); ap.add_argument("--R", type=float)
    ap.add_argument("--sigma-R", type=float); ap.add_argument("--N-R", type=int)
    ap.add_argument("--tag", default=""); ap.add_argument("--out"); ap.add_argument("--json-out")
    a = ap.parse_args(argv)
    if a.self_test:
        L, ok = self_test()
        print("\n".join(L))
        return 0 if ok else 1
    gam, sfit = {}, {}
    if a.pipeline_log:
        txt = open(a.pipeline_log, encoding="utf-8").read()
        for m in FIT_RE.finditer(txt):
            f = "canonical" if m.group(1) == "canonical" else "alt"
            gam[f], sfit[f] = float(m.group(2)), float(m.group(3))
        if set(gam) != set(FOOTINGS):
            raise SystemExit(f"the pipeline log lacks a footing fit line: found {sorted(gam)}")
    if a.gamma:
        gam.update(parse_kv(a.gamma))
    if a.sigma_fit:
        sfit.update(parse_kv(a.sigma_fit))
    sysd, nss = {f: {} for f in FOOTINGS}, None
    if a.sigma_json:
        J = json.load(open(a.sigma_json))
        nss = J.get("nss_off_status")
        for f in FOOTINGS:
            for d in ("b", "a", "e", "g2"):
                if J.get(f, {}).get(d) is not None:
                    sysd[f][d] = float(J[f][d])
    for s in a.sig:
        f, kv = s.split(":", 1)
        sysd[f].update(parse_kv(kv))
    R = sR = NR = None
    if a.r_json:
        p = json.load(open(a.r_json))["branches"]["primary"]
        R, sR, NR = p["R"], p["sigma_R"], p["N"]
    R = a.R if a.R is not None else R
    sR = a.sigma_R if a.sigma_R is not None else sR
    NR = a.N_R if a.N_R is not None else NR
    gam = {f: gam[f] for f in FOOTINGS if f in gam}
    L, rep = score(gam, sfit, sysd, R, sR, NR, tag=a.tag, nss_status=nss)
    print("\n".join(L))
    if a.out:
        open(a.out, "w").write("\n".join(L) + "\n")
    if a.json_out:
        json.dump(rep, open(a.json_out, "w"), indent=1, default=float)
    return 0


if __name__ == "__main__":
    sys.exit(main())
