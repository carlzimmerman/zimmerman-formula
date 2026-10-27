"""Proof-only candidates for a reviewed fixed Lean statement; explicit axiom audit."""
import os
from pathlib import Path
import re
import uuid
import json
import subprocess
import hashlib

from engine import pinned_bytes, validate_contract, sha
from executor import environment, run_process, sandbox_command

FOUNDATION = {'propext', 'Classical.choice', 'Quot.sound'}
_FILE_HASHES = {}

def compiled_environment(project, compiler):
    """Hash a superset of imported compiled definitions; cache only unchanged inodes."""
    files = {}
    roots = [Path(project)/'.lake/build/lib', Path(project)/'.lake/packages', compiler.parent.parent/'lib']
    candidates = [compiler]
    for root in roots:
        if root.exists():
            candidates.extend(p for p in root.rglob('*') if p.is_file() and
                              ('.olean' in p.name or p.suffix in ('.ir','.so','.dylib')))
    for path in sorted(set(candidates)):
        s = path.stat()
        key = (str(path),s.st_size,s.st_mtime_ns,s.st_ctime_ns,s.st_ino)
        digest = _FILE_HASHES.get(key)
        if digest is None:
            h = hashlib.sha256()
            with path.open('rb') as f:
                for block in iter(lambda:f.read(1024*1024),b''): h.update(block)
            digest = h.hexdigest(); _FILE_HASHES[key] = digest
        files[str(path)] = digest
    digest = sha(json.dumps(files,sort_keys=True).encode())
    return {'digest':digest,'files':files}

def installed_compiler(project):
    r = subprocess.run(['elan','which','lean'],cwd=project,capture_output=True,text=True,timeout=10,check=True)
    return Path(r.stdout.strip()).resolve(strict=True)
FORBIDDEN = re.compile(r'\b(?:sorry|admit|axiom|constant|opaque|def|theorem|lemma|example|namespace|section|end|'
                       r'import|export|open|set_option|attribute|instance|unsafe|partial|noncomputable|'
                       r'macro|syntax|elab|initialize|run_tac|run_elab|native_decide|implemented_by)\b|[#;`]|--|/-')

def render(contract, proof):
    if not isinstance(contract.get('statement'), str) or not contract['statement'].strip():
        raise ValueError('Missing fixed target statement')
    if not isinstance(proof, str) or not proof.strip() or len(proof) > 20000:
        raise ValueError('Supply only a bounded tactic proof body')
    if FORBIDDEN.search(proof) or any(ord(c) < 32 and c not in '\n\t\r' for c in proof):
        raise ValueError('Declarations, metaprogramming and admissions are not allowed in proof candidates')
    if proof.lstrip().startswith('by '): proof = proof.lstrip()[3:]
    lines = '\n'.join('  '+line for line in proof.expandtabs(4).splitlines())
    return (contract.get('preamble', 'import Mathlib')+'\n\n'
            'theorem OrchTarget : ('+contract['statement']+') := by\n'+lines+
            '\n\n#print axioms OrchTarget\n#check OrchTarget\n')

def allowed_axioms(output):
    matches = re.findall(r"'?OrchTarget'? (?:depends on axioms:\s*\[([^\]]*)\]|does not depend on any axioms)", output)
    if len(matches) != 1: return False
    return {x.strip() for x in matches[0].split(',') if x.strip()} <= FOUNDATION

def certify(contract, proof, work):
    validate_contract(contract)
    if contract['kind'] != 'lean': raise ValueError('Not a Lean contract')
    code = render(contract, proof)
    work = Path(work).resolve(); work.mkdir(parents=True, exist_ok=True)
    path = work/('proof-'+uuid.uuid4().hex+'.lean'); path.write_text(code)
    env = environment(work)
    for k in ('HOME', 'ELAN_HOME', 'LEAN_SYSROOT'):
        if k in os.environ: env[k] = os.environ[k]
    try:
        # Resolve an already installed compiler and import caches directly. Loading Lake's
        # workspace inside a read-only sandbox can trigger dependency refreshes; proof
        # checking must never update or delete the shared research project's packages.
        compiler = installed_compiler(contract['project_dir'])
        project = Path(contract['project_dir'])
        before = compiled_environment(project,compiler)
        if contract.get('environment_digest') and before['digest'] != contract['environment_digest']:
            raise ValueError('Compiled Lean environment changed since target was frozen')
        (work/'environment.json').write_text(json.dumps(before,sort_keys=True))
        manifest = json.loads((project/'lake-manifest.json').read_text())
        libraries = [project/'.lake/build/lib/lean'] + [
            project/manifest.get('packagesDir','.lake/packages')/p['name']/'.lake/build/lib/lean'
            for p in manifest['packages']]
        env['LEAN_PATH'] = os.pathsep.join(str(p) for p in libraries)
        argv = [str(compiler), str(path)]
        if contract.get('machine_proposed'):
            argv = sandbox_command(argv, work, [contract['project_dir'], Path.home()/'.elan'])
        r = run_process(argv, contract['project_dir'], env,
                        min(600, max(1, float(contract.get('timeout_s', 120)))), work/'lean')
        out = (work/r['stdout']).read_text(errors='replace') + (work/r['stderr']).read_text(errors='replace')
        for item in contract['project_inputs']: pinned_bytes(item)
        if compiled_environment(project,compiler)['digest'] != before['digest']:
            raise ValueError('Compiled Lean environment changed during proof checking')
        if path.read_text() != code: raise ValueError('Proof file changed during compilation')
        ok = r['complete'] and allowed_axioms(out) and not re.search(r'\bsorry\b|\berror:', out)
        return {'validity': 'formal_checked' if ok else 'invalid',
                'outcome': 'supported' if ok else 'inconclusive', 'run': r,
                'target': contract['statement'], 'proof': path.name, 'compiler_sha256':sha(compiler.read_bytes()),
                'environment_digest':before['digest'],
                'scope': 'Exact theorem under reviewed definitions and premises; not empirical validation.'}
    except (OSError, ValueError, subprocess.SubprocessError) as e:
        return {'validity': 'invalid', 'outcome': 'inconclusive', 'reason': str(e)}
