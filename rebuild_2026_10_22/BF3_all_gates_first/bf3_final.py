#!/usr/bin/env python3
"""BF3 final read: arms, funnel, distinct joint forms, exact grade both footings, near misses, control, holdout selection. Exit 1 under MUTATE. kappa = 1/2 FITTED; not theory closed."""
import glob, hashlib, json, os, sys, time
from bf3_read import *
OUT = open(os.path.join(LANE, f"bf3_final{TAG}.out"), "w")
def say(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); OUT.write(s + "\n"); OUT.flush()
R = {}; arms = [("real", "canonical", ("A", "B", "E")), ("real", "alt", ("A", "B"))]
EXN = int(os.environ.get("BF3_EXACT_N", 300))
def line(o): return f"L sys {o['lens']['sys']:.1f} cov {o['lens']['cov']:.0f} b0 {o['lens']['sys_b0']:.1f}; G Z .3 {o['G']['0.3']['Z']:+.2f} .6 {o['G']['0.6']['Z']:+.2f} .85 {o['G']['0.85']['Z']:+.2f}; X {o['X']['mean']:+.3f} Z {o['X']['Z']:+.2f} sc {o['X']['scatter']:.3f} rms {o['X']['rms']:.3f}; S {o['S']['rms']:.4f} U {o['S']['U']:.2f} tilt {o['S']['tilt']:+.2f}"
JALL = {}
for arm, foot, fams in arms:
    fams = [f for f in fams if glob.glob(os.path.join(LANE, "shards", f"{arm}_{foot}_{f}", "*.json"))]; t0 = time.time(); la, ll, lc = lines(foot); say(f"\n=== {arm} {foot}: law chi^2_sys {lc:.2f}, L-abs {la:.1f}, L-law {ll:.1f}")
    for fam in fams:
        o = analyse(arm, foot, (fam,)); f = o["fams"][fam]; c = f["cnt"]; R[f"{arm}|{foot}|{fam}"] = f; J = distinct(f.get("joint_cheap", []), la); f["distinct"] = len(J)
        say(f"{fam}: shards {f['shards']} complete {f['complete']} stopped {f['stopped']}; tried {c.get('tried', 0):.4g}; gate-0 B {c.get('g0_B', 0)}; positive {c.get('positive', 0):.4g}; precut {c.get('precut', 0):.4g}; X pass {c.get('Xpass', 0):.4g}; X-strict {c.get('Xstrict', 0):.4g}; past lens-lo {c.get('lens_lo', 0):.4g}; kept cheap candidates {f.get('cand', 0)}, L-abs {f.get('cand_abs', 0)}; S run {f.get('n_S', 0)}; pass S sampled {f.get('cand_abs_S_sampled', 0)} L-abs + {f.get('cand_law_only_S_sampled', 0)} L-law; est {f.get('cand_S_est', 0):.4g}; distinct {len(J)}; k5 lost {c.get('k5_lost', 0)}")
        say(f"  funnel on 0.1 % sample, order frozen: n {c.get('s_n', 0)}, gate 0 {c.get('s_g0', 0)}, L-law {c.get('s_Ll', 0)}, L-law+G {c.get('s_LlG', 0)}, +X {c.get('s_LlGX', 0)}; L-abs {c.get('s_La', 0)}, L-abs+G {c.get('s_LaG', 0)}, +X {c.get('s_LaGX', 0)}; X alone {c.get('s_X', 0)}")
        for k, v in f.get("combos", {}).items(): say(f"  best {k:12s} score {v['score']:.3f} W{v['w']} {v['s'][:75]} cheap {v['cheap']} S {v['S']['rms']:.3f} {v['S']['U']:.2f}")
        Eg = E_get(foot); E2 = E_get("alt" if foot == "canonical" else "canonical"); other = "alt" if foot == "canonical" else "canonical"; lst = []
        for x in J[:EXN]:
            x = dict(x, fam=fam); e = exact_grade(x, foot, Eg); x["exact"] = {foot: e}; p = e["pass"]; ok = p["L_law"] and p["G"] and p["S"] and p["X"]; x["joint_law"] = ok; x["joint_abs"] = ok and p["L_abs"]
            if ok: e2 = exact_grade(x, other, E2); x["exact"][other] = e2; q = e2["pass"]; x["both_law"] = q["L_law"] and q["G"] and q["S"] and q["X"]; x["both_abs"] = x["joint_abs"] and x["both_law"] and q["L_abs"]; x["strict_both"] = p["X_strict"] and q["X_strict"]
            lst.append(x)
        f["exact_list"] = lst; n = len(lst); say(f"  exact on {n} distinct of {len(J)}: joint L-law {foot} {sum(x['joint_law'] for x in lst)}, L-abs {sum(x['joint_abs'] for x in lst)}; both footings L-law {sum(x.get('both_law', False) for x in lst)}, L-abs {sum(x.get('both_abs', False) for x in lst)}; X-strict both {sum(x.get('strict_both', False) for x in lst)}")
        for x in lst:
            if x.get("both_law"): JALL[(x["s"], x["w"], fam)] = x
        for x in [x for x in lst if x.get("both_abs")][:8]: say(f"   JOINT ABS W{x['w']} {fam} {x['s'][:80]} | {line(x['exact'][foot])}")
        # near misses on exact, both footings
        for k, v in f.get("combos", {}).items():
            x = dict(s=v["s"], w=v["w"], fam=fam); e = exact_grade(x, foot, Eg); e2 = exact_grade(x, other, E2); v["exact"] = {foot: e, other: e2}; say(f"  NEAR MISS {k}: W{v['w']} {v['s'][:70]} | {foot} {line(e)} fails {[a for a, b in e['pass'].items() if not b]} | {other} fails {[a for a, b in e2['pass'].items() if not b]}")
    say(f"  wall {time.time() - t0:.0f} s")
# Family C
try:
    sn = os.path.join(LANE, "snapshot_L4.jsonl"); raw = open(sn, "rb").read(); nm = json.load(open(os.path.join(BF1, "chunks", "real_L4", "names.json"))); hits = sorted({tuple(json.loads(l)) for l in raw.splitlines()}); Ec = E_get("canonical"); y = np.tile(PROBE_Y, 3); e = np.repeat(PROBE_E, 49); passed = []; ng0 = 0
    for i, o_, j, w in hits:
        s = f"({nm[i]}{o_}{nm[j]})"
        try: H0 = tree(s, y, e, y * 0)
        except Exception: continue
        if np.all(np.isfinite(H0)) and np.max(np.abs(H0 * HMUT - 1)) <= 1e-12:
            ng0 += 1; x = dict(s=s, w=w, fam="C"); g = exact_grade(x, "canonical", Ec); x["exact"] = dict(canonical=g); passed.append(x)
    best = sorted(passed, key=lambda x: max(abs(x["exact"]["canonical"]["X"]["Z"]) / 2, x["exact"]["canonical"]["lens"]["sys"] / L_ABS, max(abs(x["exact"]["canonical"]["G"][str(k)]["Z"]) / 2 for k in GF), x["exact"]["canonical"]["S"]["rms"] / .110, abs(x["exact"]["canonical"]["S"]["U"] - .65) / .15))
    R["C"] = dict(n=len(hits), sha=hashlib.sha256(raw).hexdigest(), g0=ng0, joint_law=sum(all(x["exact"]["canonical"]["pass"][k] for k in ("L_law", "G", "S", "X")) for x in passed), best=best[:5]); say(f"\nFamily C: BF1 L4 snapshot {len(hits)} distinct, sha {R['C']['sha'][:16]}, gate 0 {ng0}, joint L-law canonical {R['C']['joint_law']}"); [say(f"  W{x['w']} {x['s'][:70]} | {line(x['exact']['canonical'])}") for x in best[:3]]
except FileNotFoundError as e_: say("Family C not read:", e_)
# control, like for like
say("\n=== control, Family A canonical, real rows r10 against scrambled X-COP rows, shards common to all arms")
ca = ["r10", "c1", "c2", "c3"]; nsh = [len(glob.glob(os.path.join(LANE, "shards", f"{a}_canonical_A", "*.json"))) for a in ca]; ms = min(nsh) if nsh else 0; say("shards per arm", dict(zip(ca, nsh)), "common", ms); CT = {}
for a in ca:
    if not ms: break
    o = analyse(a, "canonical", ("A",), maxshard=ms)["fams"]["A"]; c = o["cnt"]; J = distinct(o.get("joint_cheap", []), L_ABS); nS = o.get("cand_S_est", 0); t = c.get("tried", 1); CT[a] = dict(tried=t, Xpass=c.get("Xpass", 0), Xstrict=c.get("Xstrict", 0), cand=o.get("cand", 0), cand_abs=o.get("cand_abs", 0), S_est=nS, abs_S_est=o.get("cand_abs_S_est", 0), distinct=len(J)); say(f"{a}: tried {t:.4g}; X pass per 1e6 {1e6 * c.get('Xpass', 0) / t:.0f}; X-strict per 1e6 {1e6 * c.get('Xstrict', 0) / t:.0f}; cheap cand {o.get('cand', 0)}; joint est per 1e6 {1e6 * nS / t:.2f}; L-abs joint est per 1e6 {1e6 * o.get('cand_abs_S_est', 0) / t:.2f}; distinct sampled {len(J)}")
R["control"] = CT
# Selection for holdouts
sel = sorted(JALL.values(), key=lambda x: (gate_score_exact(x) if False else 0, 0)) if False else None
def gs(x):
    o = x["exact"]["canonical"]; a = x["exact"]["alt"]; f = lambda e: max(e["lens"]["sys"] / L_ABS, max(abs(e["G"][str(k)]["Z"]) / 2 for k in GF), e["S"]["rms"] / .110, abs(e["S"]["U"] - .65) / .15, abs(e["X"]["Z"]) / 2, e["X"]["scatter"] / .10); return max(f(o), f(a))
J = sorted(JALL.values(), key=lambda x: (gs(x), len(x["s"]), x["s"])); ja = [x for x in J if x.get("both_abs")]; pick = (ja or J)[:6]; st = [x for x in J if x.get("strict_both")]; lab = "joint" if J else "near miss"
if st and st[0] not in pick: pick.append(st[0])
R["selection"] = [dict(s=x["s"], w=x["w"], fam=x["fam"], both_abs=x.get("both_abs"), strict=x.get("strict_both"), score=gs(x), exact=x["exact"]) for x in pick]; say(f"\nboth-footing joints in exact lists: {len(J)}, L-abs {len(ja)}, X-strict {len(st)}. Selected {len(pick)}:"); [say(f"  W{x['w']} {x['fam']} {x['s']} score {gs(x):.3f} abs {x.get('both_abs')} strict {x.get('strict_both')}") for x in pick]
json.dump(R, open(os.path.join(LANE, f"bf3_final{TAG}.json"), "w"), indent=0, sort_keys=True, default=float); OUT.close(); sys.exit(1 if MUT else 0)
