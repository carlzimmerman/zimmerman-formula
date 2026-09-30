"""CFG230 script H: strength-rule audit, the section-8 recount (frozen and Amendment-1 encodings), wording scan, MUTATE M3 (swap the class of R02a)
and M9 (cite the Lean Dimension batch as grade L as of the FREEZE state; M9b evaluates the same citation at HEAD)."""
import re, os
import CFG230_common as C
import CFG230_data as D

R = C.Run("CFG230_H_claims_audit")
M = C.mode()
R.p(f"CFG230 H. repo=<repo> mode={M or 'main'}")
GR = {"L": 5, "S+R": 4, "S": 3, "N+R": 2, "N": 1, "D": 0, "M": 0}

def summarise(SUB, mut=None):
    out = {}
    for r in D.REQS:
        sub = [list(s_) for s_ in SUB[r]]
        if mut == "M3" and r == "R02":
            for s_ in sub:
                if s_[0].startswith("R02a") and s_[1] == "THEOREM" and s_[2] in ("S", "L"):
                    s_[1], s_[2] = "DECLARED-CHOICE", "D"
        lb = [s_ for s_ in sub if s_[3]]
        thm = [s_ for s_ in lb if s_[1] == "THEOREM"]
        nonthm = [s_ for s_ in lb if s_[1] != "THEOREM"]
        kind = "whole_theorem" if thm and not nonthm else ("core_plus_parts" if thm else "no_core")
        weakest = min(GR[s_[2]] for s_ in lb) if lb else None
        weakest_thm = min((GR[s_[2]] for s_ in thm), default=None)
        out[r] = dict(kind=kind, weakest_lb=weakest, weakest_theorem=weakest_thm,
                      refereed=any(s_[2] == "S+R" or D.REFEREE_FLAG.get(r) for s_ in thm),
                      lean=sum(1 for s_ in thm if s_[2] == "L"), own_S=any(s_[2] == "S" for s_ in thm),
                      classes=sorted({s_[1] for s_ in lb}))
    return out

def counts(summ):
    return dict(whole_theorem=[r for r, v in summ.items() if v["kind"] == "whole_theorem"],
                core_plus_parts=[r for r, v in summ.items() if v["kind"] == "core_plus_parts"],
                no_core=[r for r, v in summ.items() if v["kind"] == "no_core"],
                referee_cores=[r for r, v in summ.items() if v["refereed"]],
                lean_requirements=[r for r, v in summ.items() if v["lean"]],
                lean_cores=sum(v["lean"] for v in summ.values()),
                own_S=[r for r, v in summ.items() if v["own_S"]])

frozen = summarise(D.SUB); amend = summarise(D.SUB_AMEND1)
cf, ca = counts(frozen), counts(amend)

R.p("\n== 1. strength-rule audit of the requirement headlines (frozen encoding)")
viol = []
for r in D.REQS:
    v = frozen[r]; verb = D.STATED[r]
    cond = D.CONDITIONAL_ON.get(r, [])
    lb_declared = [s_ for s_ in D.SUB[r] if s_[3] and s_[1] == "DECLARED-CHOICE"]
    if verb == "must":
        ok = v["weakest_theorem"] is not None and v["weakest_theorem"] >= GR["S"] and (not lb_declared or bool(cond))
        why = f"theorem core weakest grade {v['weakest_theorem']}; declared load-bearing parts stated as conditional premises: {cond}"
    elif verb == "fails-in-class":
        ok = True; why = f"scoped wording; load-bearing classes {v['classes']}"
    else:  # moves-with
        ok = any(s_[1] == "DECLARED-CHOICE" for s_ in D.SUB[r] if s_[3]); why = "the requirement as a whole moves with a declared choice"
    R.check("CITATION-AUDIT", f"{r} stated '{verb}' is allowed by its evidence: {why}", ok)
    if not ok: viol.append(r)
R.res["strength_violations"] = viol
R.p("  per-requirement class and grade summary (used in the README):")
for r in D.REQS:
    v = frozen[r]
    R.p(f"    {r} {D.REQ_NAMES[r]}: {v['kind']}; load-bearing classes {v['classes']}; weakest load-bearing grade code {v['weakest_lb']}, weakest THEOREM grade code {v['weakest_theorem']} (5 L, 4 S+R, 3 S, 2 N+R, 1 N, 0 declared)")
R.res["summary_frozen"] = frozen; R.res["summary_amend1"] = amend

R.p("\n== 2. recount of the section-8 hand estimates from the encoded sub-claims")
E = D.EST
def line(key, label, got_list=None, got_n=None):
    n = got_n if got_n is not None else len(got_list)
    est, rng = E[key]
    inrng = (rng is None) or (rng[0] <= n <= rng[1])
    R.check("EXPECT", f"{label}: recount {n} vs hand estimate {est}" + (f" (range {rng})" if rng else ""), n == est, ("within range" if inrng else "OUTSIDE range") + (f"; {got_list}" if got_list is not None else ""))
line("whole_theorem", "requirements whose whole statement rests on a THEOREM", cf["whole_theorem"])
line("core_plus_parts", "THEOREM core plus scoped/declared parts", cf["core_plus_parts"])
line("no_core", "no THEOREM core", cf["no_core"])
line("referee_cores", "THEOREM core referee-reproduced", cf["referee_cores"])
line("lean_cores", "THEOREM cores Lean-certified (committed certificate, sub-claim count)", None, cf["lean_cores"])
R.p(f"  (Lean-certified cores sit in requirements {cf['lean_requirements']})")
R.check("EXPECT", f"THEOREM core resting on this lane's own derivation with no referee: definition problem. Frozen count 2 (R02a, R12(a) GR ext.); grade-S cores in the encoding: {cf['own_S']}", len(cf["own_S"]) == 2, "the frozen phrase 'this lane's own new derivation' is not the same as 'grade S'; by grade S the count is larger (kept as a definition miss)")
R.p("  Amendment-1 encoding (the Lean Dimension module is committed, a288aad86): R02a splits into an L monomial statement and an S Newtonian half")
R.p(f"    whole {ca['whole_theorem']}; core+parts {ca['core_plus_parts']}; no core {ca['no_core']}; referee {ca['referee_cores']}; Lean cores {ca['lean_cores']} in {ca['lean_requirements']}")
R.res["counts_frozen"] = cf; R.res["counts_amend1"] = ca
R.check("EXPECT", "whole-statement THEOREM requirements: about 3 of 12", len(cf["whole_theorem"]) == 3)

R.p("\n== 3. wording scan (the frozen file as committed, and this lane's README when present)")
banned = [r"\bproves?\b", r"\bproved\b", r"\bimpossible\b", r"no theory can", r"\bguarantee", r"data favou?r", r"theory is closed", r"\bconfirm(s|ed)? the framework"]
neg = re.compile(r"\b(not|nothing|never|no requirement|does not|do not|cannot|without|without saying)\b", re.I)
paths = [os.path.join(C.REPO, "campaign_fresh_gravity/CFG230_FROZEN_CRITERIA.md"), os.path.join(C.HERE, "CFG230_README.md")]
flag = 0
for p_ in paths:
    if not os.path.isfile(p_): continue
    for i, ln in enumerate(open(p_, encoding="utf-8").read().splitlines(), 1):
        for b in banned:
            if re.search(b, ln, re.I) and not neg.search(ln):
                flag += 1; R.p(f"  FLAG {os.path.basename(p_)}:{i}: {ln[:150]}")
R.check("CITATION-AUDIT", "no banned strength wording outside a negation", flag == 0, f"{flag} flagged lines")

# ---------------------------------------------------------------- MUTATE
def tierX(classes, drop_T_on=()):
    out = []
    for k, (n, cells) in classes.items():
        hit = [r for r, v in cells.items() if v == "F[T]" and r not in drop_T_on]
        if hit: out.append(k)
    return out

if M == "M3":
    mut = summarise(D.SUB, "M3"); cm = counts(mut)
    x0 = tierX(D.CLASSES); x1 = tierX(D.CLASSES, drop_T_on=("R02",))
    R.p(f"  M3: R02a swapped THEOREM -> DECLARED-CHOICE. whole-theorem {cf['whole_theorem']} -> {cm['whole_theorem']}; core+parts {cf['core_plus_parts']} -> {cm['core_plus_parts']}; requirements with a THEOREM core {[r for r in D.REQS if frozen[r]['kind']!='no_core']} -> {[r for r in D.REQS if mut[r]['kind']!='no_core']}")
    R.p(f"      tier X classes {x0} -> {x1} (an F[T] on R02 loses its tag; C07 and C14 keep their F[T] on R01)")
    R.p("      per-cell expectation of the frozen file (the F[T] labels resting on R02 leave tier X) holds; per-class it does NOT: C07 and C14 stay in tier X through R01. Frozen expectation partly wrong, kept.")
    R.res["M3"] = {"whole_before": cf["whole_theorem"], "whole_after": cm["whole_theorem"], "tierX_before": x0, "tierX_after": x1}
    C.bite(R, cf["whole_theorem"] != cm["whole_theorem"] or x0 != x1, f"THEOREM-whole count {len(cf['whole_theorem'])} -> {len(cm['whole_theorem'])}; tier X unchanged ({x0}) because R01 still carries the tag")

def grade_L_allowed(path_rel, ref):
    """rule: grade L needs the module tracked at `ref` AND a passing verify_chain listing at that ref."""
    rc, tr = C.git("ls-tree", "-r", "--name-only", ref, "--", C.os.path.join(D.LEAN_DIR, path_rel))
    tracked = bool(tr.strip())
    rc2, vc = C.git("show", f"{ref}:{D.LEAN_DIR}verify_chain.out")
    passing = rc2 == 0 and "VERIFY: PASS" in vc
    return tracked and passing, tracked, passing
if M in ("M9", "M9b"):
    ref = "a288aad86^" if M == "M9" else "HEAD"
    ok, tracked, passing = grade_L_allowed("Dimension.lean", ref)
    R.p(f"  {M}: cite Lean Dimension.lean as grade L for R02a as of {ref}: tracked={tracked}, verify_chain PASS listed={passing} -> audit {'ALLOWS' if ok else 'REFUSES'}")
    if M == "M9":
        R.p("  M9 as frozen (pending state): evaluated at the parent of the peer's commit a288aad86 (the repository state in which the batch was pending). NOTE: the coordinator's freeze commit b31f5e705 came AFTER a288aad86, so at the freeze commit the batch was already committed; the frozen file's statement that it was pending was true of the working tree when I read it, not of the freeze commit.")
        C.bite(R, not ok, "the strength rule refuses an uncommitted certificate")
    else:
        R.p("  M9b (added after the freeze; not in the frozen list): at HEAD the batch is committed (a288aad86), so the audit allows grade L for the monomial statement; this is the reason the frozen M9 premise no longer holds today.")
        C.bite(R, not ok, "expected NOT to bite at HEAD (the certificate is committed)")
R.write()
