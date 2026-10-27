"""Versioned contracts, immutable evidence and persistent research scheduling."""
import hashlib
import json
from pathlib import Path
import shutil
import sqlite3
import uuid
import os
import stat
import ast
from collections import Counter
from datetime import datetime, timezone

VERSION = 'obligations-v2.2'
ROLES = ('constructive', 'counterexample', 'referee')

def now():
    return datetime.now(timezone.utc).isoformat()

def canonical(value):
    return json.dumps(value, sort_keys=True, ensure_ascii=False, allow_nan=False, indent=2)

def sha(data):
    return hashlib.sha256(data).hexdigest()

def fingerprint(value):
    return sha(canonical(value).encode())

def experiment_signature(response, executable):
    try: code = ast.dump(ast.parse(response.get('code', '')), include_attributes=False)
    except (SyntaxError, TypeError): return None
    return fingerprint({'code': code,
        'hypothesis': ' '.join(response.get('hypothesis','').split()).casefold(),
        'assumptions': response.get('assumptions', []),
        'inputs': [(x['name'], x.get('path'), x['sha256']) for x in executable.get('inputs', [])],
        'required': executable.get('required_checks'), 'negative': executable.get('negative_checks')})

def copy_artifacts(source, destination):
    """Copy regular single-link files by descriptor; never follow generated links."""
    total, entries = 0, 0
    flags = os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK
    def walk(fd, dest):
        nonlocal total, entries
        dest.mkdir()
        for name in sorted(os.listdir(fd)):
            entries += 1
            if entries > 1024: raise ValueError('Artifact file-count limit exceeded')
            try: child = os.open(name, flags, dir_fd=fd)
            except OSError as e: raise ValueError('Unsafe artifact entry: '+name) from e
            try:
                info = os.fstat(child)
                if stat.S_ISDIR(info.st_mode): walk(child, dest/name)
                elif stat.S_ISREG(info.st_mode) and info.st_nlink == 1:
                    total += info.st_size
                    if info.st_size > 64*1024*1024 or total > 256*1024*1024:
                        raise ValueError('Artifact byte limit exceeded')
                    remaining = 64*1024*1024
                    with (dest/name).open('xb') as out:
                        while True:
                            block = os.read(child, min(1024*1024, remaining+1))
                            if not block: break
                            remaining -= len(block)
                            if remaining < 0: raise ValueError('Artifact grew beyond limit')
                            out.write(block)
                else: raise ValueError('Only regular files and directories can be archived')
            finally: os.close(child)
    fd = os.open(source, flags | os.O_DIRECTORY)
    try: walk(fd, Path(destination))
    finally: os.close(fd)

def pinned_bytes(item):
    path = Path(item['path']).resolve(strict=True)
    data = path.read_bytes()
    if sha(data) != item.get('sha256'):
        raise ValueError(f'Pinned input changed: {path}')
    return data

def validate_checks(required, negative):
    for name, values in [('required_checks', required), ('negative_checks', negative)]:
        if (not isinstance(values, list) or not values
                or not all(isinstance(x, str) and x for x in values)
                or len(set(values)) != len(values)):
            raise ValueError(name+' must be a nonempty list of unique check names')
    unknown = sorted(set(negative) - set(required))
    if unknown:
        raise ValueError('negative_checks must be a subset of required_checks; unknown names: '
                         + ', '.join(unknown) + '. Reuse the SAME check names in every mode; '
                         'designated checks must evaluate to false in negative mode, not use inverted names.')

def validate_contract(c):
    for key in ('id', 'kind', 'question', 'model_version', 'assumptions'):
        if not c.get(key): raise ValueError(f'Contract missing {key}')
    if not isinstance(c['assumptions'], list) or not all(isinstance(x, str) for x in c['assumptions']):
        raise ValueError('Assumptions must be explicit strings')
    if c['kind'] not in ('research', 'exploration', 'evaluator', 'lean'): raise ValueError('Unknown contract kind')
    if c['kind'] not in ('research', 'exploration'):
        for key in ('reviewed_by', 'review_note'):
            if not isinstance(c.get(key), str) or not c[key].strip():
                raise ValueError(f'Executable contract requires {key}')
    for item in c.get('context', []) + c.get('inputs', []): pinned_bytes(item)
    if c['kind'] in ('evaluator', 'exploration'):
        pinned_bytes(c['evaluator'])
        required, negative = c.get('required_checks', []), c.get('negative_checks', [])
        validate_checks(required, negative)
        names = [x.get('name') for x in c.get('inputs', [])]
        if len(set(names)) != len(names) or any(not isinstance(x, str) or not x for x in names):
            raise ValueError('Input names must be present and unique')
    if c['kind'] == 'lean':
        for key in ('statement', 'preamble', 'toolchain', 'project_dir', 'project_inputs'):
            if not c.get(key): raise ValueError(f'Lean contract missing {key}')
        if (Path(c['project_dir'])/'lean-toolchain').read_text().strip() != c['toolchain']:
            raise ValueError('Lean toolchain differs from reviewed contract')
        for item in c['project_inputs']: pinned_bytes(item)
    return c

def load_registry(directory):
    contracts = []
    for p in sorted(Path(directory).glob('*.json')):
        c = json.loads(p.read_text())
        items = c.get('context', []) + c.get('inputs', []) + c.get('project_inputs', [])
        if c.get('evaluator'): items.append(c['evaluator'])
        for item in items: item['path'] = str((p.parent/item['path']).resolve())
        if c.get('project_dir'): c['project_dir'] = str((p.parent/c['project_dir']).resolve())
        contracts.append(validate_contract(c))
    by_id = {c['id']: c for c in contracts}
    if len(by_id) != len(contracts) or not contracts: raise ValueError('Registry must contain unique obligation IDs')
    def visit(key, active):
        if key in active: raise ValueError('Dependency cycle: ' + key)
        if key not in by_id: raise ValueError('Unknown dependency: ' + key)
        for dep in by_id[key].get('depends_on', []): visit(dep, active | {key})
    for key in by_id: visit(key, set())
    return contracts

class Store:
    def __init__(self, root):
        self.root = Path(root).resolve()
        self.root.mkdir(parents=True, exist_ok=True)
        self.db = sqlite3.connect(self.root/'ledger_v2.sqlite')
        self.db.execute('PRAGMA journal_mode=WAL')
        self.db.executescript('''
          CREATE TABLE IF NOT EXISTS attempts (
            id TEXT PRIMARY KEY, obligation TEXT, contract_hash TEXT, role TEXT,
            verifier TEXT, validity TEXT, outcome TEXT, path TEXT, sha256 TEXT, created TEXT);
          CREATE TABLE IF NOT EXISTS reviews (
            seq INTEGER PRIMARY KEY, attempt TEXT, decision TEXT, reviewer TEXT, note TEXT, created TEXT);
          CREATE TABLE IF NOT EXISTS calls (
            id TEXT PRIMARY KEY, reserved REAL, actual REAL, state TEXT, created TEXT);
        ''')
        self.db.commit()

    def close(self): self.db.close()

    def __enter__(self): return self

    def __exit__(self, *args): self.close()

    def record(self, contract, role, response, result, request=None, work=None):
        ident = uuid.uuid4().hex
        directory = self.root/'attempts'/ident
        directory.mkdir(parents=True, exist_ok=False)
        hashes = {}
        if work:
            copy_artifacts(work, directory/'artifacts')
            for p in sorted((directory/'artifacts').rglob('*')):
                if p.is_file(): hashes[str(p.relative_to(directory))] = sha(p.read_bytes())
        data = {'id': ident, 'created': now(), 'verifier': VERSION, 'contract': contract,
                'contract_hash': fingerprint(contract), 'role': role, 'request': request,
                'response': response, 'result': result, 'artifacts': hashes}
        path = directory/'evidence.json'
        content = canonical(data)
        with path.open('x') as f: f.write(content)
        self.db.execute('INSERT INTO attempts VALUES (?,?,?,?,?,?,?,?,?,?)',
                        (ident, contract['id'], data['contract_hash'], role, VERSION,
                         result['validity'], result.get('outcome', 'inconclusive'),
                         str(path), sha(content.encode()), data['created']))
        self.db.commit()
        return {'id': ident, 'path': str(path), 'result': result}

    def load(self, ident):
        row = self.db.execute('SELECT path,sha256 FROM attempts WHERE id=?', (ident,)).fetchone()
        if not row: raise ValueError('Unknown attempt: ' + ident)
        p = Path(row[0]); content = p.read_bytes()
        if sha(content) != row[1]: raise ValueError('Evidence manifest changed')
        data = json.loads(content)
        for name, expected in data['artifacts'].items():
            artifact = (p.parent/name).resolve()
            if not artifact.is_relative_to(p.parent.resolve()) or sha(artifact.read_bytes()) != expected:
                raise ValueError('Evidence artifact changed: ' + name)
        return data

    def review(self, ident, decision, reviewer, note):
        if decision not in ('accept', 'reject', 'needs_work') or not reviewer.strip() or not note.strip():
            raise ValueError('Review requires a decision, named reviewer and rationale')
        a = self.load(ident)
        if decision == 'accept' and (a['verifier'] != VERSION or a['result']['validity'] not in ('checked', 'formal_checked')):
            raise ValueError('Only current checked evidence can be accepted; proposals need a fixed contract')
        self.db.execute('INSERT INTO reviews(attempt,decision,reviewer,note,created) VALUES (?,?,?,?,?)',
                        (ident, decision, reviewer, note, now()))
        self.db.commit()

    def accepted(self, contract):
        rows = self.db.execute('''SELECT a.id FROM attempts a JOIN reviews r ON r.attempt=a.id
          WHERE a.obligation=? AND a.contract_hash=? AND a.verifier=? AND r.decision='accept'
          AND r.seq=(SELECT MAX(seq) FROM reviews WHERE attempt=a.id)''',
          (contract['id'], fingerprint(contract), VERSION)).fetchall()
        for (ident,) in rows:
            if self.load(ident)['result'].get('outcome') == 'supported': return True
        return False

    def next_job(self, contracts):
        by_id = {c['id']: c for c in contracts}
        eligible = [c for c in contracts if not self.accepted(c) and all(
            dep in by_id and self.accepted(by_id[dep]) for dep in c.get('depends_on', []))]
        if not eligible: raise ValueError('No unresolved obligation has satisfied dependencies')
        def count(c):
            return self.db.execute('SELECT COUNT(*) FROM attempts WHERE contract_hash=? AND verifier=? AND role IN (?,?,?)',
                                   (fingerprint(c), VERSION, *ROLES)).fetchone()[0]
        c = min(eligible, key=lambda c: ((count(c)+1) / max(1, float(c.get('priority', 1))), c['id']))
        return c, ROLES[count(c) % len(ROLES)]

    def recent(self, contract, limit=6):
        ids = self.db.execute('SELECT id FROM attempts WHERE contract_hash=? AND verifier=? ORDER BY created DESC LIMIT ?',
                              (fingerprint(contract), VERSION, limit)).fetchall()
        return [self.load(x[0]) for x in ids]

    def shared(self, contracts):
        return [{'contract': c, 'status': 'independently reviewed supporting evidence'}
                for c in contracts if self.accepted(c)]

    def duplicate_experiment(self, contract, response, executable):
        signature = experiment_signature(response, executable)
        if signature is None: return None
        rows = self.db.execute('''SELECT id FROM attempts WHERE contract_hash=? AND verifier=?
          AND validity IN ('candidate_checked','checked','invalid') ORDER BY created DESC''',
          (fingerprint(contract), VERSION)).fetchall()
        for (ident,) in rows:
            old = self.load(ident)
            result = old['result']
            # Retry infrastructure failures freely. Complete control failures and completed
            # evaluations are deterministic repeats; explicit CLI replay bypasses this check.
            if result['validity'] == 'invalid' and result.get('reason') != 'Control expectations not met': continue
            prior = result.get('execution_contract')
            if prior and experiment_signature(old['response'], prior) == signature: return ident
        return None

    def search_memory(self, contract):
        rows = self.db.execute('SELECT id FROM attempts WHERE obligation=? ORDER BY created DESC LIMIT 1000',
                               (contract['id'],)).fetchall()
        records = [self.load(ident) for (ident,) in rows]
        hypotheses, failures, rejected, seen = Counter(), Counter(), [], set()
        for a in records:
            response, result = a['response'], a['result']
            hypothesis = response.get('hypothesis')
            if isinstance(hypothesis, str): hypotheses[hypothesis] += 1
            if result['validity'] == 'invalid': failures[result.get('reason','unspecified')] += 1
            if a['role'] in ('door-referee','door-post-referee') and response.get('decision') == 'reject':
                parent = (a.get('request') or {}).get('parent')
                target = self.load(parent) if parent else None
                claim = (target or {}).get('response',{}).get('hypothesis','Unspecified hypothesis')
                if claim in seen or len(rejected) >= 6: continue
                seen.add(claim)
                rejected.append({'id':a['id'], 'attempt':parent, 'hypothesis':claim[:400],
                    'reason':str(response.get('reason',''))[:1000],
                    'suggested_next_test':str(response.get('next_test',''))[:600],
                    'same_contract':a['contract_hash'] == fingerprint(contract)})
        count = self.db.execute('SELECT COUNT(*) FROM attempts WHERE obligation=? AND role IN (?,?,?)',
                               (contract['id'], *ROLES)).fetchone()[0]
        return {'advisory_only':True, 'scope':'Latest 1000 records for this obligation, including earlier versions',
                'primary_attempts':count, 'rejected_routes':rejected,
                'repeated_hypotheses':[{'hypothesis':h[:400],'times':n} for h,n in hypotheses.most_common(5)],
                'frequent_failures':[{'reason':r[:400],'times':n} for r,n in failures.most_common(5)]}

    def summary(self):
        counts = dict(self.db.execute('SELECT validity,COUNT(*) FROM attempts WHERE verifier=? GROUP BY validity', (VERSION,)))
        return {'verifier': VERSION, 'attempts': sum(counts.values()), 'by_validity': counts,
                'reviews': self.db.execute('SELECT COUNT(*) FROM reviews').fetchone()[0],
                'api_spend_or_reserved_usd': self.spend(),
                'meaning': 'Checked artifacts are conditional evidence, not physical truth or novelty.'}

    def spend(self):
        return self.db.execute('SELECT COALESCE(SUM(COALESCE(actual,reserved)),0) FROM calls').fetchone()[0]

    def reserve(self, dollars, budget):
        if dollars <= 0: raise ValueError('Call reservation must be positive')
        self.db.execute('BEGIN IMMEDIATE')
        if self.spend() + dollars > budget:
            self.db.rollback(); return None
        ident = uuid.uuid4().hex
        self.db.execute('INSERT INTO calls VALUES (?,?,NULL,?,?)', (ident, dollars, 'pending', now()))
        self.db.commit()
        return ident

    def settle(self, ident, actual):
        if actual is not None and actual < 0: raise ValueError('Negative API cost')
        self.db.execute('UPDATE calls SET actual=?,state=? WHERE id=? AND state=?',
                        (actual, 'complete' if actual is not None else 'unknown', ident, 'pending'))
        self.db.commit()
