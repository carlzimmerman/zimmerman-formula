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
QUOTAS = [("constraint-first", .30), ("screened-preferred-frame", .20), ("spatially-nonlocal", .20),
          ("multi-sector", .15), ("degenerate", .10), ("novel", .05)]
# hard structural requirements per branch, derived from the seeded theorems (fed to the architect)
BRANCH_REQUIREMENTS = {
 "constraint-first": "THEOREM DC-001 (exhaustive, 108k candidates): ANY local candidate with no "
   "preferred-frame coupling and no spatial nonlocality is DEAD regardless of details. Your candidate "
   "MUST carry a lensing escape: EITHER one coupling with preferred_frame=true AND screened_by='e^-y', "
   "OR one coupling with nonlocal='spatial'. Submitting without one is an automatic dead-class dedup.",
 "screened-preferred-frame": "EVERY preferred_frame coupling MUST have screened_by='e^-y', AND "
   "kinetic_normalization_source MUST be 'independent' (P7: screened coupling must not set kinetic norm).",
 "spatially-nonlocal": "Use nonlocal='spatial' (elliptic) couplings only, never 'temporal' (P6). State "
   "explicitly how localization avoids a hidden propagating mode (P4; banked warning omega^2=c^2k^2/2).",
 "multi-sector": "Fields may split MOND dynamics vs lensing carrier, but every preferred_frame coupling "
   "must be screened_by='e^-y' and no lapse_weighted couplings (P3). Include the DC-001 lensing escape.",
 "degenerate": "Degenerate kinetic terms must be argued second-class in claimed_mechanism; still include "
   "the DC-001 lensing escape (screened PF or spatial nonlocal).",
 "novel": "Go OUTSIDE the listed families, but still respect every P-rule and include the DC-001 "
   "lensing escape (screened-e^-y preferred-frame coupling or spatial nonlocality).",
}


def J(name): return json.load(open(os.path.join(STATE, name)))
def W(name, obj): json.dump(obj, open(os.path.join(STATE, name), "w"), indent=1, sort_keys=True)
def P(name): return open(os.path.join(PROMPTS, name)).read()
def log(msg): print(f"[{time.strftime('%H:%M:%S')}] {msg}", flush=True)


def protocol_text():
    return open(os.path.join(HERE, "global_protocol.md")).read()


def pick_branch(gs):
    import random
    counts = gs.setdefault("branch_counts", {})
    total = sum(counts.values()) or 1
    # pick the branch furthest below quota (deterministic-ish exploration)
    deficit = [(q - counts.get(b, 0) / total, b) for b, q in QUOTAS]
    deficit.sort(reverse=True)
    return deficit[0][1] if random.random() < 0.8 else random.choice([b for b, _ in QUOTAS])


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
        if attempt == 2:
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
        cand = mc
    if status != "NEW":
        return
    cid = cm.register(cand, parent=cand.get("parent_candidate"),
                      mutation=cand.get("mutation_type"), reason=cand.get("reason_for_mutation"),
                      failed_gate=cand.get("failed_gate_being_addressed"))
    gs["branch_counts"][branch] = gs.get("branch_counts", {}).get(branch, 0) + 1
    log(f"  registered {cid}: {cand.get('name')}")
    # ---------- TIER 1: G0
    canon = cm.canonicalize(cand)
    cert0 = ev.gate_G0(cand, canon)
    record_cert(cid, cand, cert0, it)
    if cert0["status"] == "KILL":
        kill(cid, cand, cert0, it); return
    # ---------- TIER 2: derivation agent writes gate scripts, executed in order
    gate_status = {"G0": "PASS"}
    import gate_templates as gt
    for gate in ev.SCRIPT_GATES[:MAX_SCRIPT_GATES]:
        prior = ev.prior_certificate(cm.arch_hash(cand), gate)
        if prior and prior.get("status") == "PASS":
            gate_status[gate] = "PASS"; log(f"  {gate}: prior PASS loaded"); continue
        # TRUSTED TEMPLATE FIRST: deterministic, pre-verified math beats model-written scripts
        tc = gt.run(gate, cand)
        if tc is not None:
            record_cert(cid, cand, tc, it)
            gate_status[gate] = tc["status"]
            log(f"  {gate}: {tc['status']} (trusted template)")
            if tc["status"] == "KILL":
                kill(cid, cand, tc, it); return
            if tc["status"] in ("PASS",):
                continue
            # OPEN/CONDITIONAL/BLOCKED from a template: fall through to model script for more depth
        dctx = (f"CANDIDATE {cid}:\n{json.dumps(cand, indent=1)}\n\nGATE TO CERTIFY: {gate}\n\n"
                f"KNOWN RULES:\n{json.dumps(J('KNOWLEDGE_GRAPH.json')['rules'], indent=1)[:3000]}")
        script_reply = oc.chat(P("derivation.md"), dctx, temperature=0.3)
        script = extract_code(script_reply)
        if not script:
            gate_status[gate] = "BLOCKED"; log(f"  {gate}: no script produced"); break
        cert = ev.run_gate_script(cid, gate, script)
        # ---------- REFEREE attacks the script+output (independent; no architect confidence passed)
        if cert["status"] == "PASS":
            rctx = (f"CANDIDATE {cid} architecture:\n{json.dumps(cand, indent=1)}\n\nGATE: {gate}\n"
                    f"SCRIPT:\n```python\n{script[:6000]}\n```\nOUTPUT tail:\n"
                    f"{open(cert['script'].replace('.py','.out')).read()[-3000:]}")
            ref_reply = oc.chat(P("referee.md"), rctx, temperature=0.4)
            rj = oc.extract_json(ref_reply) or {}
            if rj.get("verdict") == "REFUTED":
                cert["status"] = "CONDITIONAL"
                cert["referee"] = rj.get("reason", "refuted")[:500]
        record_cert(cid, cand, cert, it)
        gate_status[gate] = cert["status"]
        log(f"  {gate}: {cert['status']}")
        if cert["status"] in ("KILL",):
            kill(cid, cand, cert, it); break
        if cert["status"] in ("BLOCKED",):
            break
    # ---------- outcome
    if all(gate_status.get(g) == "PASS" for g in ["G0"] + list(ev.SCRIPT_GATES[:MAX_SCRIPT_GATES])):
        promote_survivor(cid, cand, gate_status, it)
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


def main():
    max_it = int(sys.argv[1]) if len(sys.argv) > 1 else 10 ** 9
    try:
        oc.verify()
    except oc.OllamaUnavailable as e:
        cm.append_jsonl(os.path.join(DB, "failures.jsonl"),
                        {"stage": "startup", "reason": str(e), "status": "BLOCKED", "ts": time.time()})
        print(f"BLOCKED: {e}\nStart ollama (`ollama serve` + model '{oc.MODEL}') and re-run.")
        sys.exit(2)
    gs = J("GLOBAL_STATE.json")
    it0 = gs.get("iteration", 0)
    log(f"resuming at iteration {it0}; model={oc.MODEL}")
    it = it0
    try:
        while it < it0 + max_it:
            it += 1
            gs["iteration"] = it
            try:
                one_iteration(gs, it)
            except oc.OllamaUnavailable as e:
                log(f"BLOCKED mid-run: {e}"); gs["status"] = "BLOCKED"; break
            except Exception:
                cm.append_jsonl(os.path.join(DB, "failures.jsonl"),
                                {"iter": it, "stage": "runner", "reason": traceback.format_exc()[-800:],
                                 "ts": time.time()})
                log("iteration error (recorded, continuing)")
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
