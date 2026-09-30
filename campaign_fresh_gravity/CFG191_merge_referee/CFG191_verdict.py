#!/usr/bin/env python3
"""CFG191_verdict -- collects the results JSONs of s1-s5b (main and MUTATE) and prints REPRODUCES / PARTIAL / DISAGREES per frozen pass line.
No CFG179 file is read here (the comparison with CFG179's own outputs is CFG191_compare_cfg179.py, run only after these results were saved)."""
import json, pathlib, sys
sys.dont_write_bytecode = True
H = pathlib.Path(__file__).resolve().parent
def load(n, m=False):
    p = H/f"{n}{'_MUTATE' if m else ''}_results.json"
    return json.loads(p.read_text()) if p.exists() else None
def ok(res, prefix):
    cs = [c for c in res["checks"] if c["label"].startswith(prefix)]
    return bool(cs) and all(c["ok"] for c in cs)
S = {k: load(k) for k in ("CFG191_s1_theorem", "CFG191_s2_coma_udg", "CFG191_s3_solar_q2", "CFG191_s4_scorecard", "CFG191_s5_dr4_mapping", "CFG191_s5b_pipeline_tier2", "CFG191_s5c_picard_check")}
M = {k: load(k, True) for k in S}
out = []
def row(item, line, verdict, note): out.append((item, line, verdict, note))
s1, s2, s3, s4, s5, s5b, s5c = (S[k] for k in S)
row("(a)", "A1 theorem: six declared points negative, sympy = root-finding", "REPRODUCES" if ok(s1, "A1d") else "DISAGREES", "F(z+ze)-F(ze)-F(z) < 0 at all six; F=cz exact")
row("(a)", "A2 strict sub-additivity on the 200x200 grid (P2, nu_simple; nu_RAR z is not concave at large z, informational)", "REPRODUCES" if ok(s1, "A2b P2") and ok(s1, "A2a") else "DISAGREES", "")
row("(a)", "A3 vector form forces linearity (min |R|/|G(a)| > 1e-6)", "REPRODUCES" if ok(s1, "A3a") and ok(s1, "A3b") else "DISAGREES", "")
row("(a)", "A4 'only B (ownership) escapes'", "PARTIAL" if ok(s1, "A4a") and ok(s1, "A4b") else "DISAGREES", "true for laws that keep a sqrt regime at the scale; screened, linear-source and anisotropic-linear laws also have zero residual; premise P2 unstated")
row("(a)", "A5 line-T survival ratios (README) within 0.02", "REPRODUCES" if ok(s1, "A5a") else "DISAGREES", "")
h = s2["data"]["headline"]
row("(b)", "B4 E7+P2 offset +1.309/+1.275 dex, 5.6/5.4 sigma", "REPRODUCES" if ok(s2, "B4a") and ok(s2, "B4b") else "DISAGREES", f"mine {h['canonical']['offset']:+.3f}/{h['alt']['offset']:+.3f} dex = {h['canonical']['sigma']:.2f}/{h['alt']['sigma']:.2f} sigma")
row("(b)", "framing: 'fails at 5.6/5.4 sigma'", "PARTIAL", f"offset over a declared 0.235 budget; first-infall field gives {s2['data']['sweep']['0.112'][0][1]:.2f}/{s2['data']['sweep']['0.112'][1][1]:.2f} sigma; ownership isolated {h['canonical']['iso']/0.2355:.2f} sigma")
p2 = [v for k, v in s3["data"]["table"].items() if k.startswith("P2")]; rr = [v for k, v in s3["data"]["table"].items() if k.startswith("nu_RAR")]
row("(c)", "C2 sign: strict-law Q2 > ceiling for all P2 entries", "REPRODUCES" if ok(s3, "C2a") else "DISAGREES", f"P2 {min(p2):.2f}-{max(p2):.2f}, nu_RAR {min(rr):.2f}-{max(rr):.2f}")
row("(c)", "C2 range: '4.0-5.7 x'", "PARTIAL", "P2 alone 3.63-4.81 (below 4.0 at the low end); nu_RAR 4.74-6.29; no single kernel spans 4.0-5.7")
row("(d)", "D1 9/14 vs 6/14 (8 vs 6 on 13)", "REPRODUCES" if ok(s4, "D1b") and ok(s4, "D1c") else "DISAGREES", "")
v = s4["data"]["variants"]
row("(d)", "D4 order preserved in every frozen recount variant", "REPRODUCES" if ok(s4, "D4") else "DISAGREES", f"discriminating {v['disc7|canonical']}, dedup {v['dedup10|canonical']}, thr3.0 {v['thr3.0|canonical']}; a tie (3,3) with every flagged row out (variant added after the freeze)")
row("(d)", "framing: '9/14 vs 6/14' as evidence", "PARTIAL", "7 of 14 rows differ, sign test p = 0.227; G1 convention; G13/G14 and G1 double-counted in README's list; rival = QUMOND-1D recipe not E7")
row("(e)", "E1 arithmetic 5.8-6.5 / 6.8-8.1 / 2.9 sigma_tot", "REPRODUCES" if ok(s5, "E1") else "DISAGREES", "")
sm = s5b["data"]["summary"]
row("(e)", "E2/E3/tier-2: 'Arm A (merge, P2 ... full solve)' kernel label", "DISAGREES" if ok(s5b, "T2-a") and ok(s5b, "T2-b") and ok(s5, "E0b") else "PARTIAL", f"Arm A is the nu_RAR solve; my P2 merge (frozen estimator) canonical {sm['P2|canonical|1.778e-10']['floor']:.3f}-{sm['P2|canonical|1.778e-10']['top']:.3f}, alt {sm['P2|alt|1.778e-10']['floor']:.3f}-{sm['P2|alt|1.778e-10']['top']:.3f}; control reproduces Arm A within 0.013")
row("(e)", "MI '1.08' value", "PARTIAL", "retired alpha=1 number (Amendment 3); in force 1.0310 (Amendment 4)")
row("(e)", "'DR4 decides merge vs ownership'", "PARTIAL", "Arm A vs Arm C 5.8 sigma_tot; screened merge readings (Arm B 1.000, chain <= 1.0725/1.0900) omitted; Arm B = Arm C = Newton on this estimator")
print(f"{'item':5s} {'frozen pass line':100s} {'verdict':11s} note")
for it, ln, vd, nt in out: print(f"{it:5s} {ln[:100]:100s} {vd:11s} {nt}")
print("\nMUTATE outcomes (exit 1 = control bites):")
for k in S:
    m = M[k]
    if m is None: print(f"  {k}: MUTATE results missing"); continue
    lb = [c["label"] for c in m["checks"] if c["lb"] and not c["ok"]]
    print(f"  {k}: {'BITES' if lb else 'DID NOT BITE'} ({len(lb)} load-bearing failures)")
main_fail = {k: [c['label'] for c in S[k]['checks'] if c['lb'] and not c['ok']] for k in S}
print("\nmain-run load-bearing failures:", {k: v for k, v in main_fail.items() if v} or "none")
(H/"CFG191_verdict.out").write_text("\n".join(f"{it} | {ln} | {vd} | {nt}" for it, ln, vd, nt in out) + "\n")
