#!/usr/bin/env python3
"""FN2 A4 gate (FROZEN_CRITERIA.md, 755f05c3cf): dry-run, on MOCK cubes in a scratch directory outside the repo, every release-day
step that can run before the release: (1) AC1's own cutout test; (2) the runbook's pipe 'cat CUBE | python3 -I ac1_stream_cutout.py -'
on a MOCK cube placed at the release target, then 'ac1_score.py --cube' on that cutout (MOCK: the scorer prints and writes no result
file); (3) fn2_scorecard.py --read on a MOCK selftest JSON with the CFG942 MOCK U4 JSONs. NOT ALMA DATA. Writes only in this lane.
    python3 -B fn2_a4_dryrun.py SCRATCH_DIR
kappa = 1/2 FITTED; one disc excludes no model; not theory closed."""
import contextlib, hashlib, io, json, os, re, subprocess, sys, time
sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
AC1 = os.path.join(ROOT, "rebuild_2026_10_22", "AC1_alma_condor_predictions"); CFG942 = os.path.join(ROOT, "campaign_fresh_gravity", "CFG942_alma_scoring_readiness")
SCR = os.path.abspath(sys.argv[1]); os.makedirs(SCR, exist_ok=True); HOME = os.path.expanduser("~")
OUT = []; G = []
def P(s=""): print(s, flush=True); OUT.append(str(s))
def gate(n, ok, x=""): G.append((n, bool(ok))); P(f"[{'PASS' if ok else 'FAIL'}] {n} {x}")
def scrub(t):
    for a, b in ((SCR, "<scratch>"), (ROOT, "<repo>"), (HOME, "~")): t = t.replace(a, b)
    return t
ENV = dict(os.environ, OMP_NUM_THREADS="1", OPENBLAS_NUM_THREADS="1", VECLIB_MAXIMUM_THREADS="1", MKL_NUM_THREADS="1")
P("FN2 A4 dry run of the release-day steps. MOCK cubes only, NOT ALMA DATA. kappa = 1/2 FITTED; not theory closed.")
# (1) AC1's own cutout test (MOCK cubes in scratch)
d1 = os.path.join(SCR, "a4_cutout_test"); os.makedirs(d1, exist_ok=True)
r = subprocess.run(["nice", "-n", "15", sys.executable, "-B", os.path.join(AC1, "ac1_cutout_test.py"), d1], capture_output=True, text=True, env=ENV, cwd=ROOT)
for l in r.stdout.strip().splitlines(): P("    " + scrub(l))
gate("A4-G(1) ac1_cutout_test.py: every check PASS, exit 0", r.returncode == 0 and "[FAIL]" not in r.stdout, f"exit {r.returncode}")
# (2) MOCK cube at the release target (the scorer's own MOCK generator, bright class), streamed through the cutout tool, then scored
_argv = sys.argv; sys.argv = [os.path.join(AC1, "ac1_score.py")]; sys.path.insert(0, AC1)
with contextlib.redirect_stdout(io.StringIO()):
    import ac1_score as S
sys.argv = _argv
sp, Vc = S.spec("bright"); full = os.path.join(SCR, "a4_MOCK_bright_full.fits"); cut = os.path.join(SCR, "a4_MOCK_bright_cut.fits")
S.C.write_mock_cube(full, sp)
P(f"MOCK bright cube {os.path.getsize(full) / 1e6:.1f} MB at RA {S.RA:.6f}, Dec {S.DEC:.6f}, line {S.NU:.4f} GHz (OBJECT MOCK)")
t0 = time.time()
with open(full, "rb") as fin:
    r = subprocess.run([sys.executable, "-I", os.path.join(AC1, "ac1_stream_cutout.py"), "-", cut, repr(S.RA), repr(S.DEC), "4.5"], stdin=fin, capture_output=True, text=True, env=ENV)
prov = json.loads(r.stdout) if r.returncode == 0 else {}
okp = bool(prov) and prov.get("source_sha256") == hashlib.sha256(open(full, "rb").read()).hexdigest() and prov.get("source_bytes") == os.path.getsize(full)
P(f"cutout: exit {r.returncode}, {time.time() - t0:.1f} s; provenance {json.dumps({k: prov.get(k) for k in ('source_bytes', 'source_shape', 'box', 'half_arcsec', 'cutout_bytes')})}")
gate("A4-G(2a) the runbook's stream-cutout pipe on a MOCK cube: exit 0, source SHA-256 and bytes equal the file's", okp)
od = os.path.join(HERE, "a4_dryrun_scorer_output"); t0 = time.time()
r = subprocess.run(["nice", "-n", "15", "/usr/bin/time", "-l", "python3", "-B", os.path.join(AC1, "ac1_score.py"), "--cube", cut, "--output-dir", od], capture_output=True, text=True, env=ENV, cwd=ROOT)
rss = re.search(r"(\d+)\s+maximum resident set size", r.stderr); wall = time.time() - t0
for l in r.stdout.strip().splitlines(): P("    " + scrub(l))
g3 = re.search(r"G1-3D \(addendum, decides\).*-> (PASS|FAIL)", r.stdout); vt = re.search(r"thin-disc fit \[incl-Tadaki.*?V_c P-B (\d+) \+- (\d+)", r.stdout)
wrote = sorted(os.listdir(od)) if os.path.isdir(od) else []
gate("A4-G(2b) ac1_score.py --cube on the MOCK cutout: exit 0, G1-3D PASS, no result file written for a MOCK", r.returncode == 0 and g3 and g3.group(1) == "PASS" and not wrote,
     f"exit {r.returncode}; G1-3D {g3.group(1) if g3 else None}; Tadaki P-B V_c {vt.groups() if vt else None} of truth {Vc:.0f}; files written {wrote}; {wall:.0f} s; peak RSS {int(rss.group(1)) / 1e9 if rss else float('nan'):.2f} GB")
for p in (full, cut, cut + ".provenance.json"):
    if os.path.exists(p): os.remove(p)
if os.path.isdir(od) and not os.listdir(od): os.rmdir(od)
# (3) the scorecard reader on MOCK JSONs
sj = os.path.join(HERE, "a1_selftest_default", "ac1_score_selftest_results.json"); res = {}
for tag, u4 in (("MOCK_bright_U4a", "cfg942_u4_MOCK_a_results.json"), ("MOCK_bright_U4d", "cfg942_u4_MOCK_d_results.json")):
    r = subprocess.run(["python3", "-B", os.path.join(HERE, "fn2_scorecard.py"), "--read", sj, "--kind", "bright", "--u4", os.path.join(CFG942, u4), "--tag", tag], capture_output=True, text=True, env=ENV, cwd=ROOT)
    res[tag] = r.returncode; P(f"    reader {tag}: exit {r.returncode}; " + " | ".join(scrub(l)[:160] for l in r.stdout.splitlines() if l.startswith(("A:", "B0:", "B3:", "B4:"))))
gate("A4-G(3) fn2_scorecard.py --read on MOCK JSONs (U4 MOCK a: G1 pass; MOCK d: G1 fail): exit 0", all(v == 0 for v in res.values()), str(res))
P(f"\nA4 gate: {sum(o for _, o in G)} of {len(G)} PASS")
json.dump(dict(criteria="755f05c3cf", gates=G, cutout_provenance=prov), open(os.path.join(HERE, "fn2_a4_dryrun.json"), "w"), indent=1)
open(os.path.join(HERE, "fn2_a4_dryrun.out"), "w").write(scrub("\n".join(OUT)) + "\n")
sys.exit(0 if all(o for _, o in G) else 1)
