#!/usr/bin/env python3
"""WA1 report: K0, K4, labels, tables. Reads wa1_results.json, wa1_checks.json, hat/, resp/, key caches, scorecards. Writes wa1.out, wa1_summary.json. kappa = 1/2 FITTED; not theory closed; nothing here says the data favour the framework."""
import json, math, os, sys
from wa1_common import *
from wa1_fit import keys_block, J, build
R = J(HERE, "wa1_results.json"); CH = J(HERE, "wa1_checks.json"); O = []; say = lambda s="": O.append(s)
S1 = dict(LAW=("FAIL", "RQ3 B28 dkappa -0.07, -0.11"), UX3=("FAIL", "RQ3 B28 dkappa -0.21, -1.16"), P3=("FAIL", "BF2 dkappa -0.25, -0.97"), P7=("FAIL", "BF2 dkappa -0.24, -0.63"), MX1=("PASS", "MX1 README: sign right at both; mass short, sub Z -3.33"), BK2=("FAIL", "BK2 G13 dkappa -0.23, -0.79"))
S3 = dict(LAW=("NOT COMPUTABLE", "no action; reads no composition"), UX3=("NOT COMPUTABLE", "no action; reads source gas share"), P3=("NOT COMPUTABLE", "no action; reads source gas share"), P7=("NOT COMPUTABLE", "no action; reads source gas share"), MX1=("FAIL", "MX1: universal fall or reciprocity, not both"), BK2=("NOT COMPUTABLE", "no action; reads source gas share"))
def k0(cid, f):
    """every line against the scorecard on file"""
    if cid not in SCORE: return None
    Sc = J(SCORE[cid])["footings"][f]["rows"]; r = J(HERE, "resp", f"{cid}_{f}.json"); z = r["z0"]; d = {}
    for l, v in z.items():
        p = l.split("|"); rid = p[0]; o = Sc.get(rid)
        if rid in ("X", "B1", "B2") or not o: continue
        if len(p) > 1:
            if "bins" in o and p[1] in o["bins"]: d[l] = v - o["bins"][p[1]]
            elif "classes" in o: d[l] = v - o["classes"][p[1]]["Z"]
        elif rid == "A23a": d[l] = v - (o["value"] - 6) / math.sqrt(12)
        elif "Z" in o: d[l] = v - o["Z"]
    e = r["k0"]["extra"]
    if "Z" in Sc.get("B1", {}) and e.get("B1_rq3") is not None: d["B1"] = e["B1_rq3"] - Sc["B1"]["Z"]
    if "bins" in Sc.get("B2", {}) and e.get("B2_rq3"): d["B2"] = max(abs(e["B2_rq3"][k] - Sc["B2"]["bins"][k]) for k in e["B2_rq3"])
    if e.get("B23") and "value" in Sc.get("B23", {}): d["B23"] = e["B23"][0] - Sc["B23"]["value"]
    kb = keys_block(cid, f)
    kd = {}
    if kb:
        for i, k in enumerate(kb["ks"]):
            n = f"B{i + 4}:{k}"
            if n in Sc and "Z" in Sc[n]: kd[k] = kb["harness"][k] - Sc[n]["Z"]
    return dict(n=len(d), max_rows=max([abs(v) for v in d.values()] or [0]), worst=max(d, key=lambda k: abs(d[k])) if d else None, max_keys=max([abs(v) for v in kd.values()] or [0]), nk=len(kd))
def gates_at_hat(cid, f):
    h = J(HERE, "hat", f"{cid}_{f}.json"); g = h["g"]; q = {}
    if g.get("A1") is not None: q["A1"] = g["A1"] <= .110
    if g.get("A2") is not None: q["A2"] = .50 <= g["A2"] <= .80
    if g.get("A21") is not None: q["A21"] = abs(g["A21"]) <= .10
    if g.get("B24") is not None and cid != "UX3": q["B24"] = g["B24"] <= .10
    r0 = J(HERE, "resp", f"{cid}_{f}.json")["gates0"]
    if r0.get("A16"): q["A16"] = r0["A16"] in ("PASS", "FORM-DEPENDENT")
    if r0.get("A25"): q["A25"] = r0["A25"] == "PASS"
    return q, g, h, r0
say("WA1_wall_common_cause. Not blind. kappa = 1/2 FITTED; not theory closed; footings never pooled; nothing here says the data favour the framework. Adopts nothing; the cold sector stays retired.")
say(); say("K0 reproduction, |dZ| rows <= 1e-6, keys <= 1e-4")
kok = True
for cid in list(REAL) + ["CAL"]:
    for f in FEET:
        q = k0(cid, f)
        if q: 
            ok = q["max_rows"] <= 1e-6 and q["max_keys"] <= 1e-4; kok &= ok; say(f"  {cid:4s} {f:9s} {q['n']} rows max {q['max_rows']:.2e} at {q['worst']}; {q['nk']} keys max {q['max_keys']:.2e}: {'PASS' if ok else 'FAIL'}")
say(f"K0 overall {'PASS' if kok else 'FAIL'}")
K = {}; 
try:
    a, b = J(RQ, "cache_keys", "law_g005_f034", "keys.json"), J(HERE, "cache_k2", "LAW_checkbase", "keys.json"); K["checkbase"] = max(abs(a[f"R1|c0|{f}"]["Z"][h][k] - b[f"R1|c0|{f}"]["Z"][h][k]) for f in FEET for h in ("h0672", "h0686") for k in a[f"R1|c0|{f}"]["Z"][h]); say(f"keys patch with tilt 0 against RQ3's cache, max |dZ| {K['checkbase']:.2e}")
except Exception as e: say(f"checkbase unavailable {e}")
bk = J(HERE, "cache_k2", "BK2_g005_f034", "keys.json"); m = [bk[f"R1|c0|{f}"]["Z"][h]["G-OUT-M3"] for f in FEET for h in ("h0672", "h0686")]; rec = [-0.09, -0.21, 0.03, -0.11]; K4 = max(abs(x - y) for x, y in zip(m, rec)); say(f"K4 BK2 M3 {np.round(m, 3).tolist()} record {rec}: {'PASS' if K4 <= .02 else 'FAIL'} (max diff {K4:.3f})")
say(); say("K1 known answer, priors off, tolerance 0.25 sigma on informed nuisances")
for f in FEET:
    for t, v in CH["K1"][f].items():
        bad = [(NN[j], round(v["injected"][j], 2), round(v["recovered"][j], 2)) for j in range(len(NN)) if v["info"][j] >= 1 and abs(v["recovered"][j] - v["injected"][j]) > .25]
        say(f"  {f:9s} {t:8s} {'PASS' if v['ok'] else 'FAIL'} {bad if bad else ''}")
say("K2 noise, mean pull against shrinkage: " + ", ".join(f"{f} max diff {CH['K2'][f]['maxdiff']:.3f} {'PASS' if CH['K2'][f]['ok'] else 'FAIL'}" for f in FEET))
say("K3 calibration, fraction of fresh mocks past the 95 % line: " + ", ".join(f"{k} {v['frac']:.3f} {'PASS' if v['ok'] else 'FAIL'}" for k, v in CH["K3"].items()))
say(); say("Nuisance sign: theta in prior sigma about the centre. Label needs p_prof >= 0.05, all |pull| <= 2, line-only gates, untouched lines, S1, S2, S3.")
SUM = {}; ncell = 12
for cid in list(REAL) + ["CAL"]:
    for f in FEET:
        c = R["cells"][f"{cid}|{f}"]; th = np.array(c["theta"]); lines = c["lines"]; z0, zh = np.array(c["z0"]), np.array(c["zhat"]); tc = np.array(c["touched"])
        q, g, h, r0 = gates_at_hat(cid, f); hl = h["l"]; sX = build(cid, f)["sX"]; clos = [zh[i] - (hl[l] / sX[l] if l in sX else hl[l]) for i, l in enumerate(lines) if l in hl and not l.startswith("K|") and tc[i]]; clo = float(np.sqrt(np.mean(np.square(clos)))) if clos else 0.0
        unt = {l: float(zh[i]) for i, l in enumerate(lines) if not tc[i]}
        if r0.get("A7") is not None: unt["A7"] = float(r0["A7"])
        untf = {l: round(v, 2) for l, v in unt.items() if abs(v) > 2}; pull = float(np.abs(th).max()); pok = pull <= 2; pv = c["p_prof"]; lg = all(q.values()); tagx = " [X-COP TRAINED]" if cid == "UX3" else ""
        s1 = S1.get(cid, ("n/a", "")); s2 = r0.get("C1", "n/a"); s3 = S3.get(cid, ("n/a", ""))
        if cid == "CAL": lab = "CALIBRATOR, no label"
        elif pv < .05: lab = "WALLS HOLD"
        elif not pok: lab = "PULLED"
        elif lg and not untf and s1[0] == "PASS" and s2 == "PASS" and s3[0] != "FAIL": lab = "CLEARS"
        elif lg: lab = "SOFT CLEARS, WALLS STAND"
        else: lab = "WALLS HOLD (line-only gate)"
        SUM[f"{cid}|{f}"] = dict(label=lab, chi2_0=c["chi2_0"], chi2_prof=c["chi2_prof"], chi2_marg=c["chi2_marg"], dim=c["dim"], p_0=c["p_0"], p_prof=c["p_prof"], p_marg=c["p_marg"], asym_prof=c["asym_prof"], asym_p0=c["asym_p0"], p_box=c.get("p_box_mock"), chi2_box=c.get("chi2_box"), D=c.get("D"), p_scramble=c.get("p_scramble"), pull=dict(zip(NN, np.round(th, 3).tolist())), max_pull=pull, closure=clo, gates={k: bool(v) for k, v in q.items()}, untouched_fail=untf, n_untouched=len(unt), S1=s1[0], S2=s2, S3=s3[0], mock_clears_rate_pull=c["mock_rate_pull_ok"], mock_rate_pull_untouched=c["mock_rate_pull_untouched_ok"], mock95=c["mock_95_prof"], bonf=min(1.0, ncell * pv))
        say(); say(f"=== {cid} {f}{tagx}: {lab}")
        say(f"  lines {c['n_lines']}, dim {c['dim']}; chi2_0 {c['chi2_0']:.1f} p_emp {c['p_0']:.2e} asym {c['asym_p0']:.1e}; chi2_prof {c['chi2_prof']:.1f} p_emp {pv:.2e} asym {c['asym_prof']:.1e} (mock median {c['mock_median_prof']:.1f}, 95 % {c['mock_95_prof']:.1f}); chi2_marg {c['chi2_marg']:.1f} p_emp {c['p_marg']:.2e}; box chi2 {c.get('chi2_box', float('nan')):.1f} p {c.get('p_box_mock', float('nan')):.2e}; Bonferroni x12 {min(1.0, ncell * pv):.2e}")
        say(f"  D = chi2_0 - chi2_prof {c.get('D', 0):.1f}; scramble median {c.get('scr_median_D', 0):.1f}, p_scr {c.get('p_scramble', 0):.4f}. Restart gap {c['restart_gap']:.2e}. Closure rms on touched rows {clo:.3f}{' NOT CONVERGED' if clo > .5 else ''}")
        say("  pulls: " + ", ".join(f"{n} {v:+.2f} ({NUIS[n][0] + NUIS[n][1] * v:+.3f})" for n, v in zip(NN, th)))
        rel = c.get("release", {}); say("  release, D_j [required shift without prior, sigma]: " + ", ".join(f"{n} {v['D']:.1f}" + (f" [{v['required']:+.1f}]" if v.get("required") is not None else "") for n, v in rel.items()))
        say(f"  gates at fit: {q}; untouched fails {untf} of {len(unt)}; S1 {s1[0]} ({s1[1]}), S2 planets {s2}, S3 {s3[0]} ({s3[1]})")
        say(f"  mock rate, pull and p OK {c['mock_rate_pull_ok']:.3f}; with untouched {c['mock_rate_pull_untouched_ok']:.3f} (line-only and structural aren't mocked)")
        say("  line: z(0) -> z(fit)" + "".join(f"\n    {l:22s} {a:+8.2f} -> {b:+8.2f}{'' if t else '  untouched'}" for l, a, b, t in zip(lines, z0, zh, tc)))
        if cid in S1:
            sn = R["sens"][f"{cid}|{f}"]; say(f"  sensitivity, no label: priors x2 chi2 {sn['x2']['chi2_prof']:.1f} p {sn['x2']['p_prof']:.2e} max pull {np.abs(sn['x2']['theta']).max():.2f}; A12 for A13 chi2 {sn['a12']['chi2_prof']:.1f} p {sn['a12']['p_prof']:.2e}; no disputed rows, {sn['nodisp']['n_lines']} lines, chi2 {sn['nodisp']['chi2_prof']:.1f} p {sn['nodisp']['p_prof']:.2e}; POST-RESULT X-COP floor 0.05 dex per bin chi2 {sn['xfl']['chi2_prof']:.1f} p {sn['xfl']['p_prof']:.2e} max pull {np.abs(sn['xfl']['theta']).max():.2f}; POST-RESULT no X-COP chi2 {sn['nox']['chi2_prof']:.1f} p {sn['nox']['p_prof']:.2e} max pull {np.abs(sn['nox']['theta']).max():.2f}")
# release census
say(); say("Release census, cells where a nuisance has the largest D_j and D_j >= 4")
cnt = {n: [] for n in NN}; hlp = {n: [] for n in NN}
for k in SUM:
    if k.startswith("CAL"): continue
    rel = R["cells"][k]["release"]; b = max(rel, key=lambda n: rel[n]["D"])
    if rel[b]["D"] >= 4: cnt[b].append(k)
    for n in NN:
        if rel[n]["D"] >= 4: hlp[n].append(k)
for n in NN: say(f"  {n:8s} largest in {len(cnt[n])} cells {cnt[n]}; D >= 4 in {len(hlp[n])} cells")
best = max(NN, key=lambda n: len(cnt[n])); say(f"Most helped: {best}. Look-elsewhere: 12 cells, 108 single-release looks.")
labs = [SUM[k]["label"] for k in SUM if not k.startswith("CAL")]; good = [k for k in SUM if not k.startswith("CAL") and SUM[k]["label"] in ("CLEARS", "SOFT CLEARS, WALLS STAND") and SUM[k]["p_scramble"] < .05]; nscr = sum(1 for k in SUM if not k.startswith("CAL") and SUM[k]["p_scramble"] < .05)
ver = "COMMON CAUSE POINTS AT THE DATA" if good else ("PARTIAL" if nscr >= 6 else "WALLS HOLD UNDER MARGINALISATION"); say(f"p_scramble < 0.05 in {nscr} of 12 cells; better-than-WALLS-HOLD with p_scr < 0.05: {good}"); say(f"LANE VERDICT: {ver}")
open(os.path.join(HERE, "wa1.out"), "w").write("\n".join(O) + "\n"); json.dump(dict(verdict=ver, cells=SUM, census={n: cnt[n] for n in NN}, most=best, K0=kok), open(os.path.join(HERE, "wa1_summary.json"), "w"), indent=1, sort_keys=True, default=float); print(ver)
