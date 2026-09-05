#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""g00_provenance.py -- G00 of FRIED_CHICKEN_ROADMAP_2026-09-04: hash the authoritative inputs, re-run the existing
regression commands with real exit codes, re-read the f31/f31b/f31c results, and write g00_manifest.json.
Checks can fail.  Nothing here is a physics gate; it is the authentication the gates stand on."""
import os, sys, json, hashlib, subprocess, time, re, glob
ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
os.chdir(ROOT)
T0 = time.time(); FAILS = []
def check(name, ok, detail=""):
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f"   ({detail})" if detail else ""), flush=True)
    if not ok: FAILS.append(name)
def sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()

AUTH = [  # authoritative inputs for T-A, T-Q, T-R, T-B and the PPN pipeline
    "qwen_claude_field_theory/closure_2026/FRIED_CHICKEN_SPEC.md",
    "opus_48_extended_research/papers/THE_COMPLETION.md",
    "qwen_claude_field_theory/theory_2026/aqual_solver_2026.py",
    "qwen_claude_field_theory/closure_2026/aqual_solar_gate_2026/audit.py",
    "qwen_claude_field_theory/closure_2026/aqual_solar_gate_2026/results.json",
    "qwen_claude_field_theory/closure_2026/smoothed_onset_action_2026/onset_action_gate.py",
    "qwen_claude_field_theory/closure_2026/smoothed_onset_action_2026/results.json",
    "qwen_claude_field_theory/closure_2026/generalized_aest_2026/gen_aest_alpha1_c2c4.py",
    "hunt_2026/hunt_lib.py", "hunt_2026/u10_ledger.py",
    "hunt_2026/f21_two_kernels_and_the_phantom_maximum.py", "hunt_2026/f23_kernel_transcription_audit.py",
    "hunt_2026/f24_aqual_quadrupole_rar_kernel.py", "hunt_2026/f25_profiled_kernel_comparison_mu10.py",
    "hunt_2026/f28_one_argument_pincer.py", "hunt_2026/f29_coherence_length_law.py", "hunt_2026/f30_ppn_screening_door.py",
    "hunt_2026/f31_ppn_k4_alpha1.py", "hunt_2026/f31b_ppn_k4_split.py", "hunt_2026/f31c_ppn_k4_operators.py",
]
print("=" * 100); print("G00 -- provenance"); print("=" * 100)
hashes = {}
for p in AUTH:
    ok = os.path.exists(p); hashes[p] = sha(p) if ok else None
    if not ok: check(f"authoritative input present: {p}", False)
check("H1 every authoritative input exists and is hashed", all(v for v in hashes.values()), f"{len(hashes)} files")
# symbolic caches: record hash + the source that produced them (the cache key the roadmap demands)
caches = {}
for pat, src in ((os.environ.get("SCRATCH", "") + "/L2dc_k4*.pkl", "hunt_2026/f31_ppn_k4_alpha1.py"),):
    for f in glob.glob(pat):
        caches[os.path.basename(f)] = dict(sha256=sha(f), producer=src, producer_sha256=hashes.get(src), size=os.path.getsize(f), location='session scratch (untracked)')
print(f"  symbolic caches found: {len(caches)} (keyed to producer source hash; untracked pickles are never reused without this record)")

# the existing regression commands (roadmap section 8), real exit codes
CMDS = [
    ("onset (10 tests)", "python3 -m unittest discover -s qwen_claude_field_theory/closure_2026/smoothed_onset_action_2026 -q"),
    ("elliptic phantom (2)", "python3 qwen_claude_field_theory/closure_2026/elliptic_phantom_action_gate_2026/test_elliptic_phantom_action_gate_2026.py"),
    ("exact mu Cassini (6)", "python3 -m unittest discover -s hunt_2026/exact_mu_cassini_2026 -q"),
]
runs = {}
for nm, cmd in CMDS:
    t = time.time()
    try:
        r = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=1800)
        out = (r.stdout + r.stderr)[-4000:]; rc = r.returncode
    except subprocess.TimeoutExpired:
        out, rc = "TIMEOUT", -1
    m = re.search(r"Ran (\d+) tests?", out); n = int(m.group(1)) if m else None
    okline = ("OK" in out.splitlines()[-1] if out.strip() else False) if n is not None else (rc == 0)
    runs[nm] = dict(cmd=cmd, rc=rc, tests=n, ok=okline, seconds=round(time.time() - t, 1), tail=out[-600:].replace(ROOT, '<repo>'))
    check(f"regression '{nm}': rc = {rc}, tests = {n}, ok = {okline}", rc == 0 and okline, f"{runs[nm]['seconds']} s")

# f31 / f31b / f31c: re-read the numbers from the committed outputs and state the reconciled status
def grab(path, pat):
    try: return [l.rstrip() for l in open(path) if re.search(pat, l)]
    except FileNotFoundError: return []
f31 = grab("hunt_2026/f31_ppn_k4_alpha1.out", r"^\s+(1/5|1/2)\s+\d\s+[0-9e+]+\s")
f31c = grab("hunt_2026/f31c_ppn_k4_operators.out", r"^\s+\(A\)|^\s+\(B\)")
res31 = grab("hunt_2026/f31_ppn_k4_alpha1.out", r"^RESULT"); res31c = grab("hunt_2026/f31c_ppn_k4_operators.out", r"^RESULT")
anchor_ok = any("-4.400000e+00" in l and " 0e+00 " in l for l in f31)
growth = any(" 1e+08 " in l and "e+08" in l.split()[3] for l in f31)
A_ok = any("(A)" in l and " 1e+04 " in l and "-7.1986e-04" in l for l in f31c)
B_fail = any("(B)" in l and " 1e+04 " in l and "1.7996e+04" in l for l in f31c)
check("F1 f31 anchors and growth re-read from the committed output: alpha_1(XI2=0) = -4.4 at K_B=1/5, J_Y=1; alpha_1 ~ 1e8 at XI2 = 1e8",
      anchor_ok and growth, f"{len(f31)} table rows read")
check("F2 f31c re-read: coherent stiffening gives drag -7.2e-4 at XI2 = 1e4 (propagator form); Hessian-squared gives +1.8e4 (fails like the trace operator)",
      A_ok and B_fail)
check("F3 the f31 output's verdict prose is the reconciled one (no 'no ghost' claim survives above its numbers)",
      any("reconciled" in l for l in open("hunt_2026/f31_ppn_k4_alpha1.out")) and not any("no ghost." in l for l in open("hunt_2026/f31_ppn_k4_alpha1.out")))
status_k4 = "OPEN on the operator; FAIL for (D^2 phi)^2 and |D_m D_n phi|^2; host-specific (AeST-type), not a T-B PPN value"
print(f"  k^4 PPN gate status: {status_k4}")

manifest = dict(gate="G00", date="2026-09-04", command="python3 qwen_claude_field_theory/closure_2026/g00_provenance.py",
                inputs_sha256=hashes, caches=caches, regressions=runs, f31_status=status_k4, fails=FAILS,
                elapsed_s=round(time.time() - T0, 1), python=sys.version.split()[0])
json.dump(manifest, open("qwen_claude_field_theory/closure_2026/g00_manifest.json", "w"), indent=1)
print(f"\nRESULT: {len(FAILS)} FAIL -> {FAILS}" if FAILS else "\nRESULT: 0 FAIL", f"  ({manifest['elapsed_s']} s)")
sys.exit(1 if FAILS else 0)
