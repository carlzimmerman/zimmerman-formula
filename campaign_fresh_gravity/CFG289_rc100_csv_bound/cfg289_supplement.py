#!/usr/bin/env python3
"""CFG289 step 2b (added after the first comparison; disclosed in README.md): two readers the driver could not bound as written.

  * CFG90's cfg90.py hard-codes the repository's absolute path, so in both mirrors it read the real repo's ORIGINAL CSV (its FIX
    run was therefore not a FIX run).  Here a copy with REPO pointed at each mirror is run in both mirrors (the committed script is
    untouched).
  * CFG52's pooled result is computed by pooled.py (and mock_bias.py) from feas.py's per-galaxy output; neither names the CSV, so the
    driver did not run them.  They are run here in both mirrors after feas.py.
Usage: python3 campaign_fresh_gravity/CFG289_rc100_csv_bound/cfg289_supplement.py <scratch_dir>   (the dir cfg289_rerun.py filled)
Writes <name>_{ORIG,FIX}.out into this lane.
"""
import os, re, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
scratch = os.path.abspath(sys.argv[1])
for mode in ("ORIG", "FIX"):
    zf = os.path.join(scratch, mode, "zf")
    d90 = os.path.join(zf, "campaign_fresh_gravity", "CFG90_a0z_rederivation")
    src = open(os.path.join(d90, "cfg90.py")).read()
    patched, n = re.subn(r'^REPO = ".*"$', f'REPO = "{zf}"', src, count=1, flags=re.M)
    assert n == 1, "cfg90.py REPO line not found"
    open(os.path.join(d90, "cfg90_mirrorpath.py"), "w").write(patched)
    subprocess.run([sys.executable, "cfg90_mirrorpath.py"], cwd=d90, capture_output=True, check=True)
    # the mirror path is printed nowhere in cfg90.out, but scrub it anyway before copying into the lane
    out = open(os.path.join(d90, "cfg90.out")).read().replace(zf, "<mirror>")
    open(os.path.join(HERE, f"cfg90_mirrorpath_{mode}.out"), "w").write(out)
    d52 = os.path.join(zf, "campaign_fresh_gravity", "CFG52_a0z_feasibility")
    for s in ("pooled.py", "mock_bias.py"):
        p = subprocess.run([sys.executable, s], cwd=d52, capture_output=True, text=True, check=True)
        open(os.path.join(HERE, f"cfg52_{s[:-3]}_{mode}.out"), "w").write(p.stdout.replace(zf, "<mirror>"))
    print(f"{mode}: cfg90 (mirror path) and CFG52 pooled/mock_bias written")
