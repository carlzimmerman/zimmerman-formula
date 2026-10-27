#!/usr/bin/env python3
"""Research by explicit obligations; safe default is status, never background execution."""
import argparse
from contextlib import contextmanager
import fcntl
import json
from pathlib import Path
import signal
import sys
import tempfile
import time
import re
import math
from config import CONFIG
from engine import Store, canonical, load_registry, now, validate_contract, validate_checks, pinned_bytes, sha
import executor
import lean_cert
import llm
from prompts import make_prompt, EXPERIMENT_PROTOCOL

def parse_response(text):
    def unique(pairs):
        result = {}
        for k, v in pairs:
            if k in result: raise ValueError("Duplicate model JSON key")
            result[k] = v
        return result
    text = text.strip()
    fence = chr(96) * 3
    if text.startswith(fence+"json") and text.endswith(fence): text = text[7:-3].strip()
    value = json.loads(text, object_pairs_hook=unique,
                       parse_constant=lambda x: (_ for _ in ()).throw(ValueError("Nonfinite JSON")))
    if not isinstance(value, dict): raise ValueError("Expected response object")
    for field in ("hypothesis", "argument", "next_test"):
        if not isinstance(value.get(field), str) or not value[field].strip():
            raise ValueError("Missing response field: " + field)
    if not isinstance(value.get("assumptions"), list) or not all(isinstance(x, str) for x in value["assumptions"]):
        raise ValueError("Response assumptions must be an explicit list")
    for name in ('code','proof'):
        if name in value and not isinstance(value[name], str): raise ValueError(name+' must be text')
    if 'inputs' in value:
        if not isinstance(value['inputs'], list): raise ValueError('inputs must be a list')
        for item in value['inputs']:
            if not isinstance(item, dict) or not all(isinstance(item.get(k), str) and item[k] for k in ('name','path')):
                raise ValueError('Every input requires nonempty name and path')
    for name in ('required_checks','negative_checks'):
        if name in value and (not isinstance(value[name], list) or not value[name]
                or not all(isinstance(x,str) and x for x in value[name]) or len(set(value[name])) != len(value[name])):
            raise ValueError(name+' must be a nonempty list of unique check names')
    if 'timeout_s' in value and (type(value['timeout_s']) not in (int,float)
            or not math.isfinite(value['timeout_s']) or value['timeout_s']<=0):
        raise ValueError('timeout_s must be a finite positive number')
    return value

def snapshot_inputs(contract, work, original=None):
    directory = Path(work)/"pinned"; directory.mkdir()
    items = contract.get("context", []) + contract.get("inputs", [])
    if contract["kind"] in ("evaluator", "exploration"): items = items + [contract["evaluator"]]
    if contract["kind"] == "lean": items = items + contract["project_inputs"]
    originals = (original or contract).get('context', []) + (original or contract).get('inputs', [])
    if (original or contract)['kind'] in ('evaluator','exploration'): originals += [(original or contract)['evaluator']]
    if (original or contract)['kind'] == 'lean': originals += (original or contract)['project_inputs']
    index = []
    for i, item in enumerate(items):
        dest = directory/(str(i)+Path(item["path"]).suffix)
        dest.write_bytes(pinned_bytes(item))
        index.append({"original": originals[i]['path'], "copy": str(dest.relative_to(work)), "sha256": item["sha256"]})
    (directory/"index.json").write_text(canonical(index))

def process_response(store, contract, role, response, request):
    validate_contract(contract)
    with tempfile.TemporaryDirectory(prefix="orch-v2-") as td:
        executable = contract
        if contract['kind'] == 'research' and response.get('code') and response.get('required_checks'):
            executable = exploration_contract(contract, response, td)
        snapshot_inputs(executable, td)
        if executable["kind"] in ("evaluator", "exploration"):
            if executable['kind'] == 'exploration' and role in ('constructive','counterexample','referee','repair'):
                duplicate = store.duplicate_experiment(contract, response, executable)
                if duplicate:
                    return store.record(contract,role,response,
                        {'validity':'invalid','outcome':'inconclusive','duplicate_of':duplicate,
                         'reason':'Duplicate experiment: same claim, assumptions, program, input bytes and check specification. '
                                  'Implement a materially different calculation, not cosmetic edits; use CLI replay for replication.'},
                        request=request,work=td)
            result = executor.evaluate(executable, Path(td)/"evaluation")
            result['execution_contract'] = executable
        elif contract["kind"] == "lean" and response.get("proof"):
            result = lean_cert.certify(contract, response["proof"], Path(td)/"formal")
        else:
            result = {"validity": "proposal", "outcome": "inconclusive",
                      "reason": "No executable Python with required checks, or Lean proof body, was supplied."}
        return store.record(contract, role, response, result, request=request, work=td)

def replay_attempt(store, ident):
    old = store.load(ident)
    original = old['result'].get('execution_contract', old['contract'])
    if original['kind'] == 'research': raise ValueError('Proposal has no executed code to replay')
    path = Path(store.db.execute('SELECT path FROM attempts WHERE id=?',(ident,)).fetchone()[0])
    index = json.loads((path.parent/'artifacts/pinned/index.json').read_text())
    mapping = {x['original']:str(path.parent/'artifacts'/x['copy']) for x in index}
    restored = json.loads(canonical(original))
    for key in ('context','inputs'):
        for item in restored.get(key,[]): item['path']=mapping[item['path']]
    if restored['kind'] in ('evaluator','exploration'):
        restored['evaluator']['path']=mapping[restored['evaluator']['path']]
    with tempfile.TemporaryDirectory(prefix='orch-replay-') as td:
        snapshot_inputs(restored, td, original)
        if restored['kind'] == 'lean': result=lean_cert.certify(restored,old['response']['proof'],Path(td)/'formal')
        else: result=executor.evaluate(restored,Path(td)/'evaluation')
        result['execution_contract']=original
        return store.record(old['contract'],'replication',old['response'],result,
                            request={'parent':ident,'origin':'archived replay'},work=td)

def exploration_contract(obligation, response, work):
    code = response['code']
    if not isinstance(code, str) or len(code) > 100000: raise ValueError('Invalid generated program')
    path = Path(work)/'candidate.py'; path.write_text(code)
    inputs = []
    repo = CONFIG['root'].parent.parent.resolve()
    for item in response.get('inputs', []):
        if not isinstance(item, dict) or not isinstance(item.get('path'), str) or not isinstance(item.get('name'), str):
            raise ValueError('Every input needs a name and a repository-relative path')
        p = (repo/item['path']).resolve(strict=True)
        if not p.is_relative_to(repo) or '.git' in p.parts or any(s.startswith('.') for s in p.relative_to(repo).parts):
            raise ValueError('Generated inputs must be visible research files inside the repository')
        if p.suffix.lower() not in {'.csv','.tsv','.json','.txt','.dat','.fits','.gz','.npy','.npz','.md','.lean','.py'}:
            raise ValueError('Unsupported research input type')
        inputs.append({'name': item['name'], 'path': str(p), 'sha256': sha(p.read_bytes())})
    return {**obligation, 'kind': 'exploration', 'evaluator': {'path':str(path),'sha256':sha(code.encode())},
            'required_checks': response['required_checks'], 'negative_checks': response.get('negative_checks', []),
            'inputs': inputs, 'timeout_s': min(1800, max(1, float(response.get('timeout_s', 120)))),
            'candidate_hypothesis': response['hypothesis'], 'candidate_assumptions': response['assumptions']}

def advisory_call(store, contract, role, prompt, parent):
    """Archive every model judgement, but never treat it as a machine proof."""
    raw, metadata = llm.generate('referee' if 'referee' in role else role, prompt, store)
    response = json.loads(raw.strip())
    if not isinstance(response, dict): raise ValueError('Expected a JSON object from the model')
    record = store.record(contract, role, response,
        {'validity':'proposal', 'outcome':'inconclusive', 'reason':'Model assessment is advisory'},
        request={'prompt':prompt, 'model':metadata, 'raw_response':raw, 'parent':parent})
    return response, record

def evidence_packet(store, ident):
    a = store.load(ident)
    packet = {k:a[k] for k in ('id','contract','role','response','result')}
    root = a.get('request', {}).get('root') if a.get('request') else None
    if root: packet['original_hypothesis'] = store.load(root)['response'].get('hypothesis')
    text = canonical(packet)
    if len(text) > 45000: raise ValueError('Evidence packet exceeds context limit; compact the experiment output')
    return text

def repair_packet(store, ident):
    a=store.load(ident)
    path=Path(store.db.execute('SELECT path FROM attempts WHERE id=?',(ident,)).fetchone()[0])
    logs={}
    for name in a['artifacts']:
        if name.endswith(('.stdout','.stderr')):
            logs[name]=(path.parent/name).read_text(errors='replace')[-3000:]
    result = {k:v for k,v in a['result'].items() if k != 'execution_contract'}
    return canonical({'previous_response':a['response'],'result':result,'execution_logs':logs})

def attempt_lean(store, contract, parent):
    packet = evidence_packet(store, parent['id'])
    prompt = ('Return JSON with statement (a SINGLE LINE Lean proposition using Mathlib) and rationale. '
        'Freeze the strongest load-bearing mathematical statement supported by this exact experiment, '
        'with every assumption explicit. Do not assume the desired conclusion, unit response, lambda=1, '
        'or kappa=1/2 unless the result is explicitly only conditional on that assumption. '
        'An algebraic fragment is not the physical theory. No proof, declarations, comments, imports '
        'or tactic blocks in statement. If no defensible mathematical statement exists, return '
        '{"statement":null,"rationale":"explain the missing implication"}. Evidence:\n'+packet)
    target, frozen = advisory_call(store, contract, 'formal-target-referee', prompt, parent['id'])
    statement = target.get('statement')
    if not statement: return {'result':{'validity':'proposal','outcome':'inconclusive'}, 'reason':target.get('rationale')}
    if (not isinstance(statement, str) or len(statement)>8000 or '\n' in statement or ':=' in statement
            or lean_cert.FORBIDDEN.search(statement) or re.search(r'\b(?:by|where)\b', statement)):
        raise ValueError('Formal target must be a proposition, not executable declarations')
    project = CONFIG['lean_project']
    pins = []
    for name in ('lean-toolchain','lakefile.toml','lake-manifest.json'):
        p = project/name
        pins.append({'path':str(p), 'sha256':sha(p.read_bytes())})
    formal = {**contract, 'kind':'lean', 'statement':statement, 'preamble':'import Mathlib',
              'reviewed_by':'machine target referee; NOT independent scientific approval',
              'review_note':target.get('rationale','Candidate theorem only'), 'machine_proposed':True,
              'project_dir':str(project), 'toolchain':(project/'lean-toolchain').read_text().strip(),
              'project_inputs':pins}
    formal['environment_digest'] = lean_cert.compiled_environment(project,lean_cert.installed_compiler(project))['digest']
    error = ''
    for retry in range(CONFIG['doors']['repair_attempts']+1):
        proof_prompt = ('Return JSON {"proof":"Lean tactic body"} proving EXACTLY this frozen statement. '
            'Do not change it, introduce axioms, sorry, declarations, custom tactics or metaprogramming. '
            'Mathlib is imported. Statement: '+statement+'\nPrevious compiler output:\n'+error)
        proof, proposed = advisory_call(store, formal, 'formalizer', proof_prompt, frozen['id'])
        with tempfile.TemporaryDirectory(prefix='orch-proof-') as td:
            snapshot_inputs(formal, td)
            try: result = lean_cert.certify(formal, proof.get('proof',''), Path(td)/'formal')
            except ValueError as e: result = {'validity':'invalid','outcome':'inconclusive','reason':str(e)}
            checked = store.record(formal, 'formal-verification', proof, result,
                                   request={'parent':parent['id'],'target_record':frozen['id'],
                                            'proof_record':proposed['id'],'repair':retry}, work=td)
            if result['validity'] == 'formal_checked': return checked
            error = result.get('reason','')
            for p in (Path(td)/'formal').glob('*.std*'): error += p.read_text(errors='replace')[-6000:]
    return checked

def chase_doors(store, contract, parent, max_depth=None):
    current = parent
    report = {'root':parent['id'], 'survived_doors':0, 'status':'testing'}
    depth_limit = CONFIG['doors']['max_depth'] if max_depth is None else max_depth
    if parent['result'].get('outcome') != 'supported' or parent['result']['validity'] not in ('candidate_checked','checked'):
        return dict(report, status='initial_test_did_not_support_hypothesis')
    for depth in range(1, depth_limit+1):
        try: packet = evidence_packet(store, current['id'])
        except (ValueError,OSError) as e: return dict(report,status='inconclusive',reason=str(e))
        referee_prompt = ('You are a skeptical referee for a generated physics experiment. Read the actual '
            'code and results. Reject fabricated observations, definitions equalling themselves, missing units, '
            'circular a0 calibration, diagnostic passes hiding failed claims, and underpowered nulls called proof. '
            'Check the experiment addresses its stated hypothesis. A passing control is not scientific truth. '
            'Return JSON with decision advance/reject/inconclusive, reason, and next_test: a precise independent '
            'necessary consequence that could kill THIS hypothesis. Prefer a different computational route. '
            'Also include door_contract with hypothesis (exact consequence), assumptions (list), required_checks '
            '(list of named load-bearing checks) and negative_checks (nonempty subset). The coder cannot alter '
            'these fields. Do not change the action or smuggle in a dark-matter particle. Evidence:\n'+packet)
        try:
            review, review_record = advisory_call(store, contract, 'door-referee', referee_prompt, current['id'])
            if review.get('decision') != 'advance' or not review.get('next_test'):
                return dict(report, status='halted_by_referee', review=review_record['id'])
            frozen = review.get('door_contract')
            if not isinstance(frozen, dict) or any(not frozen.get(k) for k in ('hypothesis','assumptions','required_checks','negative_checks')):
                return dict(report, status='inconclusive', reason='Referee did not freeze the next door contract')
            validate_checks(frozen['required_checks'], frozen['negative_checks'])
            prompt = make_prompt(contract, 'counterexample', store.recent(contract))
            prompt += '\nFIXED NEXT DOOR (test this consequence of the current hypothesis):\n'+canonical(review)
            for retry in range(CONFIG['doors']['repair_attempts']+1):
                raw, metadata = llm.generate('counterexample', prompt, store)
                request = {'prompt':prompt,'raw_response':raw,'model':metadata,'parent':current['id'],
                           'root':parent['id'],'door':depth,'repair':retry,'referee':review_record['id']}
                try:
                    response = parse_response(raw)
                    if any(response.get(k) != frozen[k] for k in ('hypothesis','assumptions','required_checks','negative_checks')):
                        raise ValueError('Worker changed the frozen door hypothesis, assumptions or checks')
                    child = process_response(store, contract, 'door-'+str(depth), response, request)
                except (ValueError, OSError) as e:
                    child = store.record(contract, 'door-'+str(depth), {'raw':raw},
                        {'validity':'invalid','outcome':'inconclusive','reason':str(e)}, request=request)
                result = child['result']
                if result['validity'] in ('candidate_checked','checked'): break
                prompt = (EXPERIMENT_PROTOCOL+'\nRepair this fixed door without changing any frozen fields: '
                          +canonical(frozen)+'\nLatest failed response and execution output:\n'
                          +repair_packet(store,child['id']))
            if result['validity'] not in ('candidate_checked','checked'):
                return dict(report, status='inconclusive', last=child['id'])
            if result['outcome'] != 'supported':
                return dict(report, status='rejected_at_door', last=child['id'])
            post_prompt = ('Review the executed door against this frozen requirement: '+canonical(frozen)+
                '\nDid the code actually test it with real inputs and meaningful controls? Reject tautologies, '
                'fabricated observations and circular normalization. Return JSON with decision advance/reject/'
                'inconclusive and reason. This is an advisory review, not proof. Actual code and results:\n'+
                evidence_packet(store, child['id']))
            post, post_record = advisory_call(store, contract, 'door-post-referee', post_prompt, child['id'])
            if post.get('decision') != 'advance':
                return dict(report, status='halted_by_post_review', last=child['id'], review=post_record['id'])
            report['survived_doors'] += 1
            current = child
        except (RuntimeError, ValueError, OSError) as e:
            return dict(report, status='inconclusive', reason=str(e))
    report['status'] = 'survived_tested_doors_not_scientifically_confirmed'
    try: report['lean'] = attempt_lean(store, contract, current)
    except (RuntimeError, ValueError, OSError) as e: report['lean'] = {'error':str(e)}
    return report

@contextmanager
def owner_lock(root):
    root = Path(root); root.mkdir(parents=True, exist_ok=True)
    with (root/"owner.lock").open("a") as f:
        try: fcntl.flock(f, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError: raise ValueError("Another v2 writer owns this runtime")
        try: yield
        finally: fcntl.flock(f, fcntl.LOCK_UN)

def write_status(store, state, latest=None):
    status = dict(store.summary(), ts=now(), state=state, latest=latest)
    p = store.root/"status.json"; tmp = p.with_suffix(".tmp")
    tmp.write_text(canonical(status)); tmp.replace(p)
    if store.root == CONFIG['runtime'].resolve():
        legacy = CONFIG['root']/'status.json'
        temp = legacy.with_suffix('.tmp'); temp.write_text(canonical(status)); temp.replace(legacy)
        (CONFIG['root']/'watch_digest.md').write_text(
            '# Autoresearch v2\n\nState: '+state+'\n\n'+canonical(store.summary())+'\n')
    return status

def one_iteration(store, contracts):
    contract, role = store.next_job(contracts)
    memory = store.search_memory(contract)
    routes = CONFIG.get('research_routes',{}).get(contract['id'],[])
    route = routes[memory['primary_attempts'] % len(routes)] if routes else None
    search = {'policy':'route-memory-v1','route':route,'memory':memory}
    prompt, frozen, parent = '', {}, None
    write_status(store, 'running', {'obligation':contract['id'], 'role':role, 'phase':'model_generation', 'route':route})
    for retry in range(CONFIG['doors']['repair_attempts']+1):
        request, raw, response = {'role':role,'repair':retry,'parent':parent,'search':search}, None, None
        try:
            if not prompt: prompt = make_prompt(contract, role, store.recent(contract), store.shared(contracts), search=search)
            request['prompt'] = prompt
            raw, metadata = llm.generate(role, prompt, store)
            request.update(model=metadata,raw_response=raw)
            response = parse_response(raw)
            if any(response.get(k)!=v for k,v in frozen.items()):
                raise ValueError('Repair changed the original hypothesis, assumptions or checks')
            # Preserve the scientific claim immediately, but do not freeze an invalid
            # execution protocol. Otherwise the worker cannot repair its own schema.
            for key in ('hypothesis','assumptions'): frozen.setdefault(key,response[key])
            if response.get('code') and response.get('required_checks'):
                validate_checks(response['required_checks'], response.get('negative_checks'))
                for key in ('required_checks','negative_checks'): frozen.setdefault(key,response[key])
            attempt = process_response(store,contract,role if retry==0 else 'repair',response,request)
        except (RuntimeError,ValueError,OSError,TypeError,KeyError) as e:
            attempt = store.record(contract,role if retry==0 else 'repair',response or {'raw':raw},
                {'validity':'invalid','outcome':'inconclusive','reason':str(e)},request=request)
        if attempt['result']['validity'] != 'invalid': break
        parent=attempt['id']
        prompt = (EXPERIMENT_PROTOCOL+'\nRepair the latest failed experiment. Return ONLY its corrected JSON object. '
                  'Do not echo previous answers or append explanations. Fix code and unfrozen protocol metadata; '
                  'do not weaken check meanings or force booleans. Frozen fields must be copied exactly:\n'
                  +canonical(frozen)+'\nResearch obligation: '+contract['question']
                  +'\nAssigned route: '+canonical(route)
                  +'\nPrevious code/response and actual execution output:\n'+repair_packet(store,attempt['id']))
    if attempt['result']['validity'] in ('candidate_checked','checked') and attempt['result']['outcome']=='supported':
        doors=chase_doors(store,contract,attempt)
        store.record(contract,'door-summary',doors,
            {'validity':'proposal','outcome':'inconclusive','reason':doors['status']},request={'parent':attempt['id']})
        attempt['doors']=doors
    write_status(store, "running", attempt)
    return attempt

def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--runtime", type=Path, default=CONFIG["runtime"])
    parser.add_argument("--contracts", type=Path, default=CONFIG["contracts"])
    sub = parser.add_subparsers(dest="command")
    sub.add_parser("status"); sub.add_parser("plan")
    run = sub.add_parser("run")
    run.add_argument("--iterations", type=int, default=1)
    run.add_argument("--continuous", action="store_true")
    run.add_argument("--interval", type=float, default=5)
    check = sub.add_parser("check")
    check.add_argument("obligation"); check.add_argument("--proof-file", type=Path)
    replay = sub.add_parser("replay"); replay.add_argument("attempt")
    review = sub.add_parser("review")
    review.add_argument("attempt"); review.add_argument("decision", choices=["accept", "reject", "needs_work"])
    review.add_argument("--reviewer", required=True); review.add_argument("--note", required=True)
    args = parser.parse_args(argv)
    command = args.command or "status"
    if command == "status":
        if not (args.runtime/"ledger_v2.sqlite").exists():
            print(canonical({"state": "stopped", "attempts": 0, "legacy": "Historical ledger is not promoted."}))
            return 0
        with Store(args.runtime) as store:
            print(canonical(dict(store.summary(), status=json.loads((args.runtime/"status.json").read_text())
                if (args.runtime/"status.json").exists() else None)))
        return 0
    with owner_lock(args.runtime), Store(args.runtime) as store:
        contracts = load_registry(args.contracts) if command != 'replay' else []
        by_id = {c["id"]: c for c in contracts}
        if command == "plan":
            contract, role = store.next_job(contracts)
            print(canonical({"next": contract["id"], "role": role, "contract": contract}))
        elif command == "review":
            attempt = store.load(args.attempt)
            if by_id.get(attempt["contract"]["id"]) != attempt["contract"]:
                raise ValueError("Review requires the current registered contract")
            store.review(args.attempt, args.decision, args.reviewer, args.note)
            print("Review recorded; no hypothesis was added to a known-results file.")
        elif command == "check":
            if args.obligation not in by_id: raise ValueError("Unknown obligation")
            contract = by_id[args.obligation]
            if contract["kind"] == "research": raise ValueError("This obligation has no fixed verifier yet")
            response = {"proof": args.proof_file.read_text()} if args.proof_file else {}
            if contract["kind"] == "lean" and not response.get("proof"): raise ValueError("--proof-file required")
            print(canonical(process_response(store, contract, "verification", response, {"origin": "CLI check"})))
        elif command == "replay":
            print(canonical(replay_attempt(store, args.attempt)))
        elif command == "run":
            if args.iterations < 1 or args.interval < 0: raise ValueError("Use positive iterations and nonnegative interval")
            def stop(signum, frame): raise KeyboardInterrupt
            previous = {s: signal.signal(s, stop) for s in (signal.SIGTERM, signal.SIGINT)}
            try:
                n = 0
                while args.continuous or n < args.iterations:
                    attempt = one_iteration(store, contracts)
                    print(canonical(attempt), flush=True); n += 1
                    if args.continuous or n < args.iterations:
                        time.sleep(max(args.interval, 30 if attempt["result"]["validity"] == "invalid" else 0))
            except KeyboardInterrupt:
                pass
            finally:
                write_status(store, "stopped")
                for s, handler in previous.items(): signal.signal(s, handler)
    return 0

if __name__ == "__main__":
    try: sys.exit(main())
    except (ValueError, OSError) as e:
        print("orchestrator:", e, file=sys.stderr); sys.exit(2)
