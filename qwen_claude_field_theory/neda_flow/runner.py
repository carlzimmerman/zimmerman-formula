#!/usr/bin/env python3
"""AUTORESEARCH RUNNER — the persistent loop. Launch:  python3 runner.py [max_iterations]
(default: run until stop condition; Ctrl+C is the human override, state survives).

LOOP: load state -> load protocol -> pick branch (quota scheduler) -> ARCHITECT (one candidate) ->
canonicalize -> dedup -> G0 (deterministic) -> if survives: DERIVATION agent writes gate scripts
G1.. in order -> execute (script is the judge) -> REFEREE attacks -> record certificates ->
SYNTHESIS extracts the lesson -> update knowledge graph -> next candidate. Everything logged to
database/*.jsonl; checkpoint report every CHECKPOINT_EVERY iterations. Restartable: never restarts
science from iteration 1."""
import json, os, sys, time, traceback
import ollama_client as oc
import candidate_manager as cm
import evaluator as ev

HERE = os.path.dirname(os.path.abspath(__file__))
STATE, DB, PROMPTS = (os.path.join(HERE, d) for d in ("state", "database", "prompts"))
CHECKPOINT_EVERY = int(os.environ.get("AR_CHECKPOINT", "25"))
MAX_SCRIPT_GATES = int(os.environ.get("AR_MAX_GATES", "5"))   # per candidate per iteration (G1..G5 default)
DEEP_GATES = os.environ.get("AR_DEEP_GATES", "0") == "1"      # OFF by default: G4+ derivations are
#   untrustworthy on a local model AND were timing out (45min blocks). Cooker = prospector: it runs
#   G0 + trusted templates (G1-G3) and files anything clean as SURVIVOR_PENDING_AUDIT for Claude to
#   audit the deep gates. Set AR_DEEP_GATES=1 to re-enable Qwen-written gate scripts (slow, PENDING).
TRUSTED_GATES = ["G1", "G2", "G3"]                            # deterministic pre-verified templates
THEOREM_GATES = ["G4", "G5", "G6", "G8"]                                  # session no-gos as deterministic gates:
#   G6 slip-lock (DC-013, frame-free cannot lens), G8 P7/stiff-frame fork (DC-014). Neda KILLs what
#   these cover; only genuine escapees (2nd metric / novel) reach SURVIVOR_PENDING_AUDIT for Claude.
ESCAPE_MUTATION = os.environ.get("AR_ESCAPE_MUTATION", "0") == "1"  # OFF: a dead-class hit costs no
#   extra 13-min call -- round-robin + cooldown handle diversity instead. ON: one targeted mutation retry.
# Round-robin FREQUENCIES (times each branch appears per rotation cycle), re-weighted 2026-08-30 after
# the khronometric/preferred-frame family was CLOSED (DC-001 pincer + DC-010/KM-X1/door1 + FM-000004
# audit = the same P7 collision). The LIVE route is the spatially-nonlocal pure-metric corridor (no
# khronon, no preferred frame). Closed branches are kept at low rate ONLY to catch a genuinely novel
# escape (e.g. constraint-first carrying a nonlocal channel), not as equal search targets.
QUOTAS = [("bimetric", 3), ("spatially-nonlocal", 3), ("higher-derivative", 2), ("novel", 2),
          ("multi-sector", 1), ("constraint-first", 1), ("screened-preferred-frame", 1), ("degenerate", 1)]
# hard structural requirements per branch, derived from the seeded theorems (fed to the architect)
BRANCH_REQUIREMENTS = {
 "constraint-first": "THEOREM DC-001 (exhaustive, 108k candidates): ANY local candidate with no "
   "preferred-frame coupling and no spatial nonlocality is DEAD regardless of details. Your candidate "
   "MUST carry a lensing escape: EITHER one coupling with preferred_frame=true AND screened_by='e^-y', "
   "OR one coupling with nonlocal='spatial'. Submitting without one is an automatic dead-class dedup.",
 "screened-preferred-frame": "EVERY preferred_frame coupling MUST have screened_by='e^-y', AND "
   "kinetic_normalization_source MUST be 'independent' (P7: screened coupling must not set kinetic norm).",
 "spatially-nonlocal": "Use nonlocal='spatial' (elliptic) couplings only, never 'temporal' (P6). "
   "SWEEP THEOREM (DC-011): a SINGLE mass gapping the localizer AND entering the kernel has an EMPTY "
   "window (freeze needs 1/m<1kpc, fidelity needs 1/m>2000kpc). Your localization MUST be SCALE-SPLIT: "
   "the operator gapping the extra mode (omega^2=c^2k^2/2) must be structurally DIFFERENT from the "
   "operator building the (-D^2)^-1 kernel (e.g. two-auxiliary localization). Declare both operators.",
 "multi-sector": "Fields may split MOND dynamics vs lensing carrier, but every preferred_frame coupling "
   "must be screened_by='e^-y' and no lapse_weighted couplings (P3). Include the DC-001 lensing escape.",
 "degenerate": "Degenerate kinetic terms must be argued second-class in claimed_mechanism; still include "
   "the DC-001 lensing escape (screened PF or spatial nonlocal).",
 "bimetric": "Two dynamical metrics (Hassan-Rosen family). KNOWN PRICE you MUST address in "
   "claimed_mechanism: ghost-free HR => linear Yukawa (fixed length scale) = ANTI-MOND; say HOW the "
   "ACCELERATION scale a0 and mu=1-e^-y arise (nonlinear helicity-0 sector / composite matter coupling "
   "/ f-sector structure) without the Boulware-Deser ghost; m_g~H0 sits on the Higuchi bound.",
 "higher-derivative": "Higher-derivative kinetic terms MUST name the Ostrogradsky evasion (degeneracy "
   "condition, constraint structure) in claimed_mechanism. Still need the lensing slip off the delta-R "
   "ray: state the carrier.",
 "novel": "Go OUTSIDE the listed families, but still respect every P-rule and include the DC-001 "
   "lensing escape (screened-e^-y preferred-frame coupling or spatial nonlocality).",
}


def J(name): return json.load(open(os.path.join(STATE, name)))
def W(name, obj): json.dump(obj, open(os.path.join(STATE, name), "w"), indent=1, sort_keys=True)
def P(name): return open(os.path.join(PROMPTS, name)).read()
def log(msg): print(f"[{time.strftime('%H:%M:%S')}] {msg}", flush=True)


def protocol_text():
    return open(os.path.join(HERE, "global_protocol.md")).read()


BRANCH_ORDER = [b for b, _ in QUOTAS]

def pick_branch(gs):
    """Strict round-robin over branches; a branch on cooldown (2 consecutive dead results) is skipped
    until its cooldown iteration passes. No branch monopolizes the search."""
    idx = gs.get("rr_index", -1)
    cooldown = gs.get("branch_cooldown", {})   # branch -> iteration until which it is skipped
    it_now = gs.get("iteration", 0)
    for step in range(1, len(BRANCH_ORDER) + 1):
        cand = BRANCH_ORDER[(idx + step) % len(BRANCH_ORDER)]
        if cooldown.get(cand, 0) <= it_now:
            gs["rr_index"] = (idx + step) % len(BRANCH_ORDER)
            return cand
    # all on cooldown -> take the next anyway
    gs["rr_index"] = (idx + 1) % len(BRANCH_ORDER)
    return BRANCH_ORDER[gs["rr_index"]]


def note_branch_dead(gs, branch):
    """Track consecutive dead results; after 2 in a row put the branch on a 10-iteration cooldown."""
    streak = gs.setdefault("dead_streak", {})
    streak[branch] = streak.get(branch, 0) + 1
    if streak[branch] >= 2:
        gs.setdefault("branch_cooldown", {})[branch] = gs.get("iteration", 0) + 10
        streak[branch] = 0
        log(f"  branch '{branch}' on cooldown (10 iters) after repeated dead results")


def note_branch_live(gs, branch):
    gs.setdefault("dead_streak", {})[branch] = 0


def recent_dead_ends(n=10):
    """Last n dedup hits with names + matched class, so the architect stops re-proposing them."""
    rows = [x for x in cm._load_jsonl(os.path.join(DB, "experiments.jsonl"))
            if x.get("stage") == "dedup"][-n:]
    return [{"name": x.get("name"), "family": x.get("family"), "matched": x.get("ref"),
             "why": x.get("why", "")} for x in rows]


def architect_context(branch):
    kg, dead, surv, og = J("KNOWLEDGE_GRAPH.json"), J("DEAD_CLASSES.json"), J("SURVIVORS.json"), J("OPEN_GATES.json")
    fails = cm._load_jsonl(os.path.join(DB, "failures.jsonl"))[-8:]
    return (f"## RESEARCH BRANCH FOR THIS CANDIDATE: {branch}\n\n"
            f"## MANDATORY STRUCTURAL REQUIREMENTS FOR THIS BRANCH (hard filter, not advice)\n"
            f"{BRANCH_REQUIREMENTS.get(branch, '')}\n\n"
            f"## YOUR RECENT DEAD-END PROPOSALS (already killed at dedup — do NOT re-propose "
            f"anything structurally similar; change the ARCHITECTURE, not names)\n"
            f"{json.dumps(recent_dead_ends(), indent=1)[:3000]}\n\n"
            f"## GLOBAL PROTOCOL (immutable law)\n{protocol_text()[:9000]}\n\n"
            f"## ARCHITECTURE GRAMMAR\n{open(os.path.join(HERE,'architecture_grammar.md')).read()}\n\n"
            f"## KNOWLEDGE GRAPH (learned rules — every candidate MUST respect these)\n"
            f"{json.dumps(kg['rules'], indent=1)}\n\n"
            f"## DEAD CLASSES (never re-cook)\n{json.dumps(dead['classes'], indent=1)[:6000]}\n\n"
            f"## VERIFIED MECHANISM LIBRARY (compose from these; they are PROVEN ingredients)\n"
            f"{json.dumps(J('MECHANISM_LIBRARY.json')['mechanisms'], indent=1)[:2500]}\n\n"
            f"## CURRENT SURVIVORS\n{json.dumps(surv['ranked'], indent=1)[:3000]}\n\n"
            f"## OPEN GATES\n{json.dumps(og, indent=1)[:2000]}\n\n"
            f"## RECENT FAILURES\n{json.dumps(fails, indent=1)[:4000]}\n")


def one_iteration(gs, it):
    branch = pick_branch(gs)
    log(f"iter {it}: branch={branch}")
    # ---------- ARCHITECT (batch: up to 3 candidates per call — same 13-min generation)
    reply = oc.chat(P("architect.md"), architect_context(branch), temperature=0.9)
    batch = oc.extract_candidates(reply)
    ok = [c for c in batch if all(k in c for k in cm.REQUIRED_FIELDS)]
    if not ok:
        # empty/malformed (usually a thinking model that never emitted JSON): one FORCEFUL retry,
        # no extended thinking, schema spelled out, within the SAME iteration.
        empty = "EMPTY (no content -- likely spent the budget thinking)" if not reply.strip() else "unparseable/incomplete"
        log(f"  architect first pass {empty}; forcing a JSON-only retry")
        force = ("/no_think\nOutput ONLY a json object, NO thinking, NO prose. Propose ONE new candidate "
                 "architecture for the '" + branch + "' branch as:\n"
                 '```json\n{"candidates":[{"name":"...","family":"' + branch + '","fields":[{"name":"...",'
                 '"type":"scalar|vector|stf_tensor|metric|khronon|multiplier","kinetic":"none|standard|degenerate",'
                 '"timelike_background":false}],"couplings":[{"label":"...","sources":["..."],"order_in_phi":2,'
                 '"preferred_frame":false,"screened_by":null,"lapse_weighted":false,"nonlocal":"spatial"}],'
                 '"mond_realization":"nonlocal_F+","kinetic_normalization_source":"independent",'
                 '"claimed_mechanism":"...","predicted_weak_field":"...","inequivalence_argument":"..."}]}\n```\n'
                 "FROZEN (immutable): mu(y)=1-e^{-y}; F+(Z)=4[1-(1+sqrt(Z)/2)e^{-sqrt(Z)/2}], "
                 "mu(y)=1-2F+'(4y^2). Respect this branch's mandatory requirements. JSON only.")
        reply = oc.chat(P("architect.md"), architect_context(branch) + "\n\n" + force, temperature=0.3)
        batch = oc.extract_candidates(reply)
        ok = [c for c in batch if all(k in c for k in cm.REQUIRED_FIELDS)]
    log(f"  architect returned {len(batch)} candidate(s), {len(ok)} schema-complete")
    if ok:
        for n, cand in enumerate(ok[:3], 1):
            log(f"  -- candidate {n}/{min(len(ok),3)}: {cand.get('name','?')[:60]}")
            try:
                process_candidate(gs, it, branch, cand)
            except oc.OllamaUnavailable:
                raise
            except Exception:
                cm.append_jsonl(os.path.join(DB, "failures.jsonl"),
                                {"iter": it, "stage": "process_candidate",
                                 "reason": traceback.format_exc()[-600:], "ts": time.time()})
                log("     candidate error (recorded, continuing batch)")
        return
    # legacy single-candidate repair path
    cand = oc.extract_json(reply)
    missing = [k for k in cm.REQUIRED_FIELDS if not cand or k not in cand]
    if missing:
        # ONE repair attempt: show the model its own output + the exact missing fields
        fix = oc.chat(P("architect.md"),
                      f"Your previous reply was rejected: {'no parseable JSON' if not cand else 'missing fields '+str(missing)}.\n"
                      f"Previous reply (truncated):\n{reply[-3000:]}\n\n"
                      "Re-emit the SAME candidate as ONE complete json object in a ```json fence with ALL "
                      "required fields (name, family, fields, couplings, mond_realization, claimed_mechanism, "
                      "kinetic_normalization_source, predicted_weak_field, inequivalence_argument). JSON only.",
                      temperature=0.2)
        cand = oc.extract_json(fix)
        missing = [k for k in cm.REQUIRED_FIELDS if not cand or k not in cand]
    if missing:
        os.makedirs(os.path.join(DB, "rejected"), exist_ok=True)
        with open(os.path.join(DB, "rejected", f"iter{it:05d}.txt"), "w") as f:
            f.write(reply)
        cm.append_jsonl(os.path.join(DB, "failures.jsonl"),
                        {"iter": it, "stage": "architect", "reason": f"schema after repair: missing {missing}",
                         "raw_saved": f"database/rejected/iter{it:05d}.txt", "ts": time.time()})
        log(f"  architect output rejected (schema, missing {missing}) -- raw saved"); return
    process_candidate(gs, it, branch, cand)


def process_candidate(gs, it, branch, cand):
    # mandatory inequivalence answer (sec 25): candidate must state why it differs from killed classes
    if not cand.get("inequivalence_argument"):
        cm.append_jsonl(os.path.join(DB, "failures.jsonl"),
                        {"iter": it, "stage": "architect", "reason": "no inequivalence_argument",
                         "name": cand.get("name"), "ts": time.time()})
        log("  rejected: no inequivalence argument"); return
    # ---------- DEDUP (with ONE escape-mutation retry: don't waste the iteration)
    for attempt in (1, 2):
        status, ref = cm.dedup_check(cand)
        if status == "NEW":
            break
        why = dedup_reason(cand, ref)
        cm.append_jsonl(os.path.join(DB, "experiments.jsonl"),
                        {"iter": it, "stage": "dedup", "result": status, "ref": ref, "why": why[:300],
                         "name": cand.get("name"), "family": cand.get("family"),
                         "arch_hash": cm.arch_hash(cand), "ts": time.time()})
        os.makedirs(os.path.join(DB, "duplicates"), exist_ok=True)
        with open(os.path.join(DB, "duplicates", f"iter{it:05d}_a{attempt}.json"), "w") as f:
            json.dump(cand, f, indent=1)
        if not ESCAPE_MUTATION:
            note_branch_dead(gs, branch)
            log(f"  {status} (ref {ref}) — moving on (escape-mutation off; round-robin will rotate)"); return
        if attempt == 2:
            note_branch_dead(gs, branch)
            log(f"  {status} (ref {ref}) after escape retry — not run"); return
        log(f"  {status} (ref {ref}) — attempting escape mutation")
        mreply = oc.chat(P("architect.md"),
                         f"Your candidate below matched a DEAD CLASS and was rejected without testing.\n"
                         f"REASON: {why}\n\nCANDIDATE:\n{json.dumps(cand, indent=1)[:4000]}\n\n"
                         f"MUTATE THE ARCHITECTURE to escape this dead class while keeping the core idea. "
                         f"{BRANCH_REQUIREMENTS.get(branch, '')} "
                         f"Change structural fields (couplings/fields/screening/nonlocality), not names. "
                         f"Emit the complete corrected candidate as ONE json object in a ```json fence, "
                         f"all required fields, including a NEW inequivalence_argument that names this dead class.",
                         temperature=0.7)
        mc = oc.extract_json(mreply)
        if not mc or any(k not in mc for k in cm.REQUIRED_FIELDS):
            log("  escape mutation unusable — not run"); return
        if not structurally_different(cand, mc):
            log("  escape mutation only cosmetic (no structural axis changed) — not run"); return
        cand = mc
    if status != "NEW":
        return
    mstat, mref = cm.mechanism_dedup(cand)
    if mstat != "NEW":
        cm.append_jsonl(os.path.join(DB, "experiments.jsonl"),
                        {"iter": it, "stage": "mech_dedup", "result": mstat, "ref": mref,
                         "name": cand.get("name"), "ts": time.time()})
        note_branch_dead(gs, branch)
        log(f"  {mstat} (mechanism {mref}) — same mechanism as prior candidates, not run"); return
    cid = cm.register(cand, parent=cand.get("parent_candidate"),
                      mutation=cand.get("mutation_type"), reason=cand.get("reason_for_mutation"),
                      failed_gate=cand.get("failed_gate_being_addressed"))
    gs["branch_counts"][branch] = gs.get("branch_counts", {}).get(branch, 0) + 1
    log(f"  registered {cid}: {cand.get('name')}")
    run_gates(cid, cand, it)


def run_gates(cid, cand, it):
    # ---------- TIER 1: G0
    canon = cm.canonicalize(cand)
    cert0 = ev.gate_G0(cand, canon)
    record_cert(cid, cand, cert0, it)
    if cert0["status"] == "KILL":
        kill(cid, cand, cert0, it); return
    # ---------- TIER 2: trusted templates (G1-G3). Deep gates (G4+) are prospector-out-of-scope by
    # default: queued OPEN for Claude audit rather than derived by the local model (see DEEP_GATES).
    gate_status = {"G0": "PASS"}
    import gate_templates as gt
    for gate in TRUSTED_GATES:
        prior = ev.prior_certificate(cm.arch_hash(cand), gate)
        if prior and prior.get("status") == "PASS":
            gate_status[gate] = "PASS"; log(f"  {gate}: prior PASS loaded"); continue
        tc = gt.run(gate, cand)
        if tc is None:                    # no template applies -> cannot trust-certify; leave OPEN
            gate_status[gate] = "OPEN"; log(f"  {gate}: OPEN (no trusted template)"); continue
        record_cert(cid, cand, tc, it)
        gate_status[gate] = tc["status"]
        log(f"  {gate}: {tc['status']} (trusted template)")
        if tc["status"] == "KILL":
            kill(cid, cand, tc, it); return

    # ---------- THEOREM GATES: run this session's proven deep no-gos deterministically (heavy lifting
    # in Neda, not Claude). G6 slip-lock (DC-013), G8 P7/stiff-frame fork (DC-014). KILL closes the
    # candidate here; OPEN means it genuinely escapes the theorems (bimetric/novel) -> escalate to audit.
    for gate in THEOREM_GATES:
        tc = gt.run(gate, cand)
        if tc is None:
            continue
        record_cert(cid, cand, tc, it)
        gate_status[gate] = tc["status"]
        log(f"  {gate}: {tc['status']} (theorem gate)")
        if tc["status"] == "KILL":
            kill(cid, cand, tc, it); return

    # ---------- optional deep-gate derivations (OFF by default; slow + PENDING_AUDIT even if PASS)
    if DEEP_GATES:
        for gate in [g for g in ev.SCRIPT_GATES[:MAX_SCRIPT_GATES] if g not in TRUSTED_GATES]:
            prior = ev.prior_certificate(cm.arch_hash(cand), gate)
            if prior and prior.get("status") == "PASS":
                gate_status[gate] = "PASS"; log(f"  {gate}: prior PASS loaded"); continue
            dctx = (f"CANDIDATE {cid}:\n{json.dumps(cand, indent=1)}\n\nGATE TO CERTIFY: {gate}\n\n"
                    f"KNOWN RULES:\n{json.dumps(J('KNOWLEDGE_GRAPH.json')['rules'], indent=1)[:3000]}")
            try:
                script = extract_code(oc.chat(P("derivation.md"), dctx, temperature=0.3))
            except oc.OllamaUnavailable:
                gate_status[gate] = "OPEN"; log(f"  {gate}: derivation timed out -> OPEN (queued audit)"); break
            if not script:
                gate_status[gate] = "OPEN"; log(f"  {gate}: no script -> OPEN"); break
            cert = ev.run_gate_script(cid, gate, script)
            record_cert(cid, cand, cert, it)
            gate_status[gate] = cert["status"]
            log(f"  {gate}: {cert['status']} (model script, PENDING_AUDIT)")
            if cert["status"] == "KILL":
                kill(cid, cand, cert, it); break
            if cert["status"] in ("BLOCKED", "OPEN"):
                break

    # ---------- outcome: clean through all TRUSTED gates => survivor for AUDIT (deep gates OPEN)
    if all(gate_status.get(g) == "PASS" for g in ["G0"] + TRUSTED_GATES) \
            and all(gate_status.get(g) != "KILL" for g in THEOREM_GATES):
        # survived the cheap gates AND the session's deterministic no-gos => genuinely novel
        # (2nd metric / structure outside the theorems). This is what actually merits Claude's audit.
        promote_survivor(cid, cand, gate_status, it)
    else:
        cm.set_status(cid, "EVALUATED", {"gates": gate_status})
    # ---------- SYNTHESIS: learn
    synth_ctx = (f"CANDIDATE {cid} gates: {json.dumps(gate_status)}\narchitecture:\n"
                 f"{json.dumps(cand, indent=1)[:4000]}")
    try:
        s = oc.chat(P("synthesis.md"), synth_ctx, temperature=0.5)
        sj = oc.extract_json(s)
        if sj and sj.get("rule"):
            kg = J("KNOWLEDGE_GRAPH.json")
            kg["rules"].append({"rule": sj["rule"][:400], "from_candidate": cid,
                                "observation": sj.get("observation", "")[:400], "ts": time.time(),
                                "status": "PROPOSED"})   # human/Claude promotes PROPOSED -> BINDING
            W("KNOWLEDGE_GRAPH.json", kg)
    except Exception as e:
        log(f"  synthesis skipped: {e}")


def structurally_different(parent, child):
    """A mutation is admissible only if it moves a STRUCTURAL coordinate, not just names/coefficients.
    Compare canonical signatures on: field-type multiset, kinetic ranks, preferred-frame set,
    screening pattern, nonlocality type, mond_realization. Cosmetic-only edits are rejected."""
    def sig(c):
        cn = cm.canonicalize(c)
        return (
            tuple(sorted((f["type"], f["kinetic"], f["timelike_background"]) for f in cn["fields"])),
            tuple(sorted((cp["preferred_frame"], cp["screened_by"], cp["nonlocal"], cp["order_in_phi"])
                         for cp in cn["couplings"])),
            cn["mond_realization"], cn["family"])
    return sig(parent) != sig(child)


def dedup_reason(cand, ref):
    """Why did this candidate die at dedup? Targeted feedback for the escape mutation."""
    canon = cm.canonicalize(cand)
    if ref and ref.startswith("DC-"):
        for dc in J("DEAD_CLASSES.json")["classes"]:
            if dc["class_id"] == ref:
                return ev.explain_dead_match(canon, dc)
    return f"identical canonical architecture already evaluated (ref {ref})"


def extract_code(text):
    import re
    m = re.search(r"```python\s*(.*?)```", text, re.S)
    return m.group(1) if m else None


def record_cert(cid, cand, cert, it):
    row = dict(cert); row.update({"candidate_id": cid, "arch_hash": cm.arch_hash(cand),
                                  "iter": it, "ts": time.time()})
    row.pop("notes", None)
    cm.append_jsonl(os.path.join(DB, "experiments.jsonl"), row)


def kill(cid, cand, cert, it):
    cm.set_status(cid, "KILL", {"failed_gate": cert["gate"]})
    cm.append_jsonl(os.path.join(DB, "failures.jsonl"),
                    {"candidate_id": cid, "arch_hash": cm.arch_hash(cand), "failed_gate": cert["gate"],
                     "decisive_certificate": cert.get("certificate", "")[:500],
                     "scope_of_failure": "candidate", "iter": it, "ts": time.time()})
    with open(os.path.join(HERE, "kills", f"{cid}.json"), "w") as f:
        json.dump({"candidate": cand, "kill_certificate": cert}, f, indent=1)
    log(f"  KILL at {cert['gate']}")


def promote_survivor(cid, cand, gates, it):
    """SURVIVOR = machine-passed all run gates. NOT 'viable' — needs remaining gates + human audit
    of every gate script (see program.md). Never over-claim."""
    surv = J("SURVIVORS.json")
    surv["ranked"].append({"candidate_id": cid, "name": cand.get("name"), "family": cand.get("family"),
                           "gates_machine_passed": [g for g, s in gates.items() if s == "PASS"],
                           "status": "SURVIVOR_PENDING_AUDIT", "iter": it, "ts": time.time()})
    W("SURVIVORS.json", surv)
    with open(os.path.join(HERE, "survivors", f"{cid}.json"), "w") as f:
        json.dump(cand, f, indent=1)
    cm.set_status(cid, "SURVIVOR")
    log(f"  *** SURVIVOR (pending audit): {cid} ***")
    cm.append_jsonl(os.path.join(DB, "discoveries.jsonl"),
                    {"candidate_id": cid, "event": "survivor_pending_audit", "iter": it, "ts": time.time()})


def checkpoint(gs, it):
    fails = cm._load_jsonl(os.path.join(DB, "failures.jsonl"))
    exps = cm._load_jsonl(os.path.join(DB, "experiments.jsonl"))
    surv = J("SURVIVORS.json")["ranked"]
    by_gate = {}
    for f_ in fails:
        g = f_.get("failed_gate", f_.get("stage", "?")); by_gate[g] = by_gate.get(g, 0) + 1
    rep = (f"# checkpoint {it:05d}\n\niterations: {it}\nexperiments: {len(exps)}\n"
           f"failures by gate/stage: {json.dumps(by_gate)}\nsurvivors: {len(surv)}\n"
           f"branch counts: {json.dumps(gs.get('branch_counts', {}))}\n"
           f"latest survivors: {json.dumps(surv[-3:], indent=1)}\n")
    with open(os.path.join(HERE, "reports", f"checkpoint_{it:05d}.md"), "w") as f:
        f.write(rep)
    log(f"checkpoint written ({it})")
    # ---- batch auto-commit: LOCAL ONLY, NEVER PUSH (pushes are human/Claude-controlled).
    # One commit per AR_BATCH (default 50) candidate dispositions (tested or ruled out).
    disposed = len(exps)
    last = gs.get("last_commit_disposed", 0)
    if disposed - last >= int(os.environ.get("AR_BATCH", "50")):
        try:
            import subprocess
            repo = os.path.abspath(os.path.join(HERE, "..", ".."))
            subprocess.run(["git", "add", "qwen_claude_field_theory/neda_flow"], cwd=repo,
                           capture_output=True, timeout=60)
            rc = subprocess.run(["git", "commit", "-q", "-m",
                                 f"neda_flow batch: {disposed - last} candidates tested/ruled-out "
                                 f"(total {disposed} experiment rows, iter {it}); survivors {len(surv)}; "
                                 f"fails-by-gate {json.dumps(by_gate)}"],
                                cwd=repo, capture_output=True, timeout=60)
            if rc.returncode == 0:
                gs["last_commit_disposed"] = disposed
                log(f"  BATCH commit (local only, never pushes): {disposed - last} dispositions")
        except Exception as e:
            log(f"  batch commit skipped: {e}")


def main():
    max_it = int(sys.argv[1]) if len(sys.argv) > 1 else 10 ** 9
    try:
        oc.verify()
    except oc.OllamaUnavailable as e:
        cm.append_jsonl(os.path.join(DB, "failures.jsonl"),
                        {"stage": "startup", "reason": str(e), "status": "BLOCKED", "ts": time.time()})
        print(f"BLOCKED: {e}\nStart ollama (`ollama serve` + model '{oc.MODEL}') and re-run.")
        sys.exit(2)
    # self-check: the evaluator must still reproduce every hand-derived verdict before any science
    import subprocess as _sp
    chk = _sp.run([sys.executable, os.path.join(HERE, "tests", "test_oracle.py")],
                  capture_output=True, text=True)
    if chk.returncode != 0:
        print(f"SELF-CHECK FAILED — evaluator no longer reproduces established physics:\n{chk.stdout}{chk.stderr}")
        print("Refusing to run. Fix the regression (or the baseline, with a documented reason) first.")
        sys.exit(3)
    log("self-check: oracle regression green")
    gs = J("GLOBAL_STATE.json")
    it0 = gs.get("iteration", 0)
    log(f"resuming at iteration {it0}; model={oc.MODEL}")
    # ---- ledger integrity sweep: every candidate file's arch_hash must match its ledger rows.
    bad = []
    for fn in os.listdir(os.path.join(HERE, "candidates")):
        cid = fn.replace(".json", "")
        try:
            cand = json.load(open(os.path.join(HERE, "candidates", fn)))
        except Exception:
            bad.append(cid); continue
        rows = [x for x in cm._load_jsonl(os.path.join(DB, "candidates.jsonl"))
                if x.get("candidate_id") == cid and "arch_hash" in x]
        if rows and rows[0]["arch_hash"] != cm.arch_hash(cand):
            bad.append(cid)
    if bad:
        log(f"LEDGER INTEGRITY FAILURE {bad} -- refusing to run (fix the ledger first)"); sys.exit(3)
    log(f"ledger integrity: {len(os.listdir(os.path.join(HERE,'candidates')))} candidates verified")
    # ---------- finish half-gated candidates from an interrupted run (REGISTERED = gates incomplete)
    for row in cm._load_jsonl(os.path.join(DB, "candidates.jsonl")):
        cid = row.get("candidate_id")
        if not cid or cm.latest_status(cid) != "REGISTERED":
            continue
        cpath = os.path.join(HERE, "candidates", f"{cid}.json")
        if not os.path.exists(cpath):
            continue
        log(f"resuming half-gated candidate {cid} (prior gate PASSes reload from db)")
        try:
            run_gates(cid, json.load(open(cpath)), it0)
        except oc.OllamaUnavailable as e:
            log(f"BLOCKED during resume: {e}"); break
        except Exception:
            cm.append_jsonl(os.path.join(DB, "failures.jsonl"),
                            {"stage": "resume_gates", "candidate_id": cid,
                             "reason": traceback.format_exc()[-600:], "ts": time.time()})
            log(f"  resume error for {cid} (recorded)")
    it = it0
    try:
        while it < it0 + max_it:
            it += 1
            gs["iteration"] = it
            try:
                one_iteration(gs, it)
            except oc.OllamaUnavailable as e:
                # institutional-grade: infrastructure hiccups are WAITED OUT, not fatal.
                log(f"ollama unavailable mid-run ({e}); waiting to retry (Ctrl+C to stop)")
                waited = 0
                while True:
                    time.sleep(120); waited += 120
                    try:
                        oc.verify(); log(f"ollama back after {waited}s — resuming"); break
                    except oc.OllamaUnavailable:
                        if waited % 1200 == 0:
                            log(f"still waiting for ollama ({waited//60} min)")
                continue
            except Exception:
                cm.append_jsonl(os.path.join(DB, "failures.jsonl"),
                                {"iter": it, "stage": "runner", "reason": traceback.format_exc()[-800:],
                                 "ts": time.time()})
                log("iteration error (recorded, continuing)")
            # exhaustion detector: N consecutive iterations with zero NEW mechanisms => the grammar
            # is saturated; "NO VIABLE CANDIDATE FOUND" is a legitimate scientific outcome.
            regs = len(cm._load_jsonl(os.path.join(DB, "candidates.jsonl")))
            if regs == gs.get("last_reg_count", 0):
                gs["no_new_streak"] = gs.get("no_new_streak", 0) + 1
            else:
                gs["no_new_streak"] = 0
            gs["last_reg_count"] = regs
            if gs["no_new_streak"] >= int(os.environ.get("AR_EXHAUST_N", "40")):
                with open(os.path.join(HERE, "reports", f"EXHAUSTION_{it:05d}.md"), "w") as f:
                    f.write(f"# NO NEW MECHANISM in {gs['no_new_streak']} consecutive iterations\n"
                            f"The current grammar appears SATURATED: every proposal is a duplicate, a dead "
                            f"class, or a killed mechanism. Legitimate outcome: NO VIABLE CANDIDATE FOUND "
                            f"in the explored domain. Next moves: expand the grammar (new mechanism axes) "
                            f"or accept the structural no-go. Stopping.\n")
                gs["status"] = "NO_VIABLE_CANDIDATE_IN_GRAMMAR"
                log(f"EXHAUSTION: {gs['no_new_streak']} iterations with no new mechanism — stopping (see reports/)")
                break
            if it % CHECKPOINT_EVERY == 0:
                checkpoint(gs, it)
            W("GLOBAL_STATE.json", gs)
    except KeyboardInterrupt:
        log("human override (Ctrl+C) — state saved")
    W("GLOBAL_STATE.json", gs)
    checkpoint(gs, it)
    log(f"stopped at iteration {it}")


if __name__ == "__main__":
    main()
