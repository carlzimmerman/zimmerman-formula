#!/usr/bin/env python3
"""CFG305 POST HOC (labelled; outside the frozen reader list): two readers that were committed AFTER the criteria (82dfcc1b3, 21:23)
and so are not in FROZEN_CRITERIA.md's scope, but feed the a0(z) chart:
  * campaign_fresh_gravity/CFG303_lcdm_free_inputs/cfg303_rc100_cristal_LCDMFREE.py (committed 2d9bdc1b9, 21:39): RC100 route B
    (SED M* + scaling gas through CFG223's estimator) reads the paper-values file through CFG223's RC_PATH["corrected"];
  * campaign_fresh_gravity/CHART_a0z_rar_z0_5_2026-10-01/chart_a0z_one.py (5f436da8c, 21:58): plots CFG223's RC100 quartiles
    (faint) and CFG303's route-B quartiles.
Run in the group-O mirrors cfg305_rerun.py filled (O_ORIG = the CORRECTED table, O_FIX = the PUBLISHED table, the paper-values file
with the confirmed cells replaced), after the frozen runs and the comparison.  Read-through links in the two lane dirs are first
replaced by clones, so nothing is written into the repo.  No frozen classification depends on this.
Usage: python3 campaign_fresh_gravity/CFG305_published_tables/cfg305_posthoc_chart_readers.py <scratch_dir>
Writes cfg305_posthoc_chart_readers.out and <name>_POSTHOC_PUBFIX.diff here.
"""
import difflib, os, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.dont_write_bytecode = True
import cfg305_rerun as RR

scratch = os.path.abspath(sys.argv[1])
RUNS = [("campaign_fresh_gravity/CFG303_lcdm_free_inputs", "cfg303_rc100_cristal_LCDMFREE.py",
         ["cfg303_rc100_cristal_LCDMFREE.out", "cfg303_rc100_pergalaxy_LCDMFREE.csv"]),
        ("campaign_fresh_gravity/CHART_a0z_rar_z0_5_2026-10-01", "chart_a0z_one.py", ["chart_a0z_one.out"])]
lines = []
P = lambda s="": (print(s, flush=True), lines.append(s))
P("CFG305 POST HOC (labelled; outside the frozen scope): the a0(z) chart's RC100 inputs on the CORRECTED (O_ORIG) and PUBLISHED (O_FIX) tables")
OUT = {}
for mode in ("ORIG", "FIX"):
    zf = os.path.join(scratch, f"O_{mode}", "zf")
    for d, scr, outs in RUNS:
        dd = os.path.join(zf, d)
        for f in os.listdir(dd):
            p = os.path.join(dd, f)
            if os.path.islink(p):
                t = os.path.realpath(p); os.unlink(p); RR.clone(t, p)
        env = dict(os.environ, MPLBACKEND="Agg")
        for k in ("MUTATE", "DATA", "RC100_INPUT"):
            env.pop(k, None)
        p = subprocess.run([sys.executable, os.path.join(dd, scr)], cwd=zf, env=env, capture_output=True, text=True, timeout=3000)
        txt = {}
        for o in outs:
            fp = os.path.join(dd, o)
            txt[o] = open(fp).read().replace(zf, "<mirror>") if os.path.exists(fp) else None
        txt["<stdout>"] = p.stdout.replace(zf, "<mirror>")
        OUT[(mode, scr)] = dict(rc=p.returncode, txt=txt, err=p.stderr.strip().splitlines()[-1:] if p.returncode else [])
        P(f"  [{mode}] {scr}: rc {p.returncode}" + (f"; stderr tail {OUT[(mode, scr)]['err']}" if p.returncode else ""))
for d, scr, outs in RUNS:
    body = []
    for o in ["<stdout>"] + outs:
        a, b = OUT[("ORIG", scr)]["txt"].get(o), OUT[("FIX", scr)]["txt"].get(o)
        if a is None or b is None:
            body.append(f"# {o}: missing in one run (ORIG {a is not None}, FIX {b is not None})")
            continue
        body += list(difflib.unified_diff(a.splitlines(), b.splitlines(), fromfile=f"ORIG/{o}", tofile=f"FIX/{o}", lineterm="", n=0))
    name = os.path.splitext(scr)[0]
    open(os.path.join(HERE, f"{name}_POSTHOC_PUBFIX.diff"), "w").write("\n".join(body).replace(scratch, "<scratch>") + "\n")
    nd = sum(1 for l in body if l[:1] in "+-" and not l.startswith(("+++", "---")))
    P(f"\n{scr}: rc ORIG {OUT[('ORIG', scr)]['rc']} / FIX {OUT[('FIX', scr)]['rc']}; {nd} differing lines (FIX vs ORIG)")
    for l in body:
        if l[:1] in "+-" and not l.startswith(("+++", "---")) and any(k in l for k in ("RC100", "FAIL", "PASS", "Q4", "Q1", "Q2", "Q3", "route B")):
            P("   " + l[:240])
open(os.path.join(HERE, "cfg305_posthoc_chart_readers.out"), "w").write("\n".join(lines).replace(scratch, "<scratch>") + "\n")
