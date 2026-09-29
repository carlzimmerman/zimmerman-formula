#!/usr/bin/env python3
"""Re-run, from a clean git-archive export of HEAD, the lanes behind the adopted STANDING_2026-09-29's REPORTED-ONLY lines that no
verification part has re-run (Parts 1-6 covered CFG43-50, CFG58-59, CFG61-99, CFG110-111): CFG1, CFG4_clusters, CFG4_switch, CFG8, CFG16,
CFG23 (both scripts), CFG25, CFG27, CFG31.  Each runs in its main mode and with MUTATE=1; the exit code, the "N/M checks pass" tally and
the full .out text (timing stripped) are compared with the committed files.  Git-ignored data present in the working tree under
real_research/data are symlinked into the export (data only, never code).  Each lane's outputs are deleted before its run, so a crash
cannot leave the archived file in place; GIT_DIR points at the repository (read-only use: CFG1 reads commit messages).
Run: python3 campaign_fresh_gravity/closure_map/verify_reported_only_2026-09-29.py EXPORT_DIR
"""
import os, re, sys, subprocess, time

REPO = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
EXPORT = os.path.abspath(sys.argv[1])
LANES = ["CFG1_evidence_audit", "CFG4_clusters", "CFG4_switch", "CFG8_chae_kernel", "CFG16_selfconsistent_floor", "CFG23_diagnostics",
         "CFG23_lcdm_control", "CFG25_fg016_lcdm_control", "CFG27_edge_thread_closure", "CFG31_coma_udgs_under_b"]
TIMING = re.compile(r"\(\s*\d+(\.\d+)?\s*s\)|\[\s*\d+(\.\d+)?\s*s\]|\d+(\.\d+)?\s*s\b")


def norm(text):
    return [TIMING.sub("<t>", l.rstrip()) for l in text.splitlines()]


def tally(text):
    m = re.findall(r"(\d+)/(\d+) checks pass", text)
    return "/".join(m[-1]) if m else "none"


rows = []
if not os.path.exists(EXPORT):
    os.makedirs(EXPORT)
    subprocess.run(f"git -C {REPO} archive HEAD | tar -x -C {EXPORT}", shell=True, check=True)
    data = os.path.join(REPO, "real_research", "data")
    linked = 0
    for root, dirs, files in os.walk(data):
        for f in files:
            src = os.path.join(root, f); dst = os.path.join(EXPORT, os.path.relpath(src, REPO))
            if not os.path.exists(dst):
                os.makedirs(os.path.dirname(dst), exist_ok=True); os.symlink(src, dst); linked += 1
    print(f"export created at HEAD; {linked} git-ignored data files symlinked")
head = subprocess.run(["git", "-C", REPO, "rev-parse", "--short", "HEAD"], capture_output=True, text=True).stdout.strip()
print(f"HEAD {head}")
for lane in LANES:
    for mode in ("0", "1"):
        env = dict(os.environ, MUTATE=mode, GIT_DIR=os.path.join(REPO, ".git"))   # read-only git access (CFG1 reads commit messages)
        suf = "_MUTATE" if mode == "1" else ""
        for fn in (lane + suf + ".out", lane + suf + "_results.json", lane + "_results" + suf + ".json"):
            fp = os.path.join(EXPORT, "campaign_fresh_gravity", fn)
            if os.path.exists(fp):
                os.remove(fp)                                         # so a crash cannot leave the archived output in place
        t0 = time.time()
        p = subprocess.run([sys.executable, os.path.join("campaign_fresh_gravity", lane + ".py")], cwd=EXPORT, env=env, capture_output=True, text=True, timeout=3600)
        new = os.path.join(EXPORT, "campaign_fresh_gravity", lane + suf + ".out")
        old = os.path.join(REPO, "campaign_fresh_gravity", lane + suf + ".out")
        nt = open(new).read() if os.path.exists(new) else "<NO OUTPUT WRITTEN>"
        ot = open(old).read() if os.path.exists(old) else ""
        a, b = norm(ot), norm(nt)
        ndiff = sum(1 for x, y in zip(a, b) if x != y) + abs(len(a) - len(b))
        tb = "Traceback" in p.stderr
        rows.append((lane, mode, p.returncode, tally(ot), tally(nt), ndiff, tb, time.time() - t0))
        print(f"{lane:28s} MUTATE={mode}  rc {p.returncode}  tally committed {tally(ot):>6s} / re-run {tally(nt):>6s}  differing lines {ndiff:3d}  traceback {tb}  ({time.time() - t0:.0f} s)", flush=True)
        if ndiff:
            for x, y in list(zip(a, b))[:400]:
                if x != y:
                    print(f"      committed: {x[:160]}\n      re-run:    {y[:160]}")
                    break
print(f"\n{len(rows)} runs; runs whose .out differs from the committed one (timing stripped): {sum(1 for r in rows if r[5])}; tracebacks: {sum(1 for r in rows if r[6])}")
