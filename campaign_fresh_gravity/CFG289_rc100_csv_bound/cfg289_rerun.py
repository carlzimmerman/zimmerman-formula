#!/usr/bin/env python3
"""CFG289 step 2: re-run every reader of the RC100 CSV twice, ORIG (original CSV) and FIX (the corrected copy substituted at the
original path), each in its own scratch mirror of the repo, and diff the outputs (FROZEN_CRITERIA.md, 80f05e155).

Usage:  python3 campaign_fresh_gravity/CFG289_rc100_csv_bound/cfg289_rerun.py <scratch_dir> [ORIG|FIX|MUTATE|ALL] [entry-substring ...]
  The mirror of each mode is <scratch_dir>/<mode>/zf (git archive of HEAD for the dirs below; everything else, including git-ignored
  files inside those dirs, is symlinked read-through).  Writes per-mode manifests <scratch_dir>/<mode>/manifest.json.  The committed
  repo is never written: the mirror dirs that scripts write into are real copies, and every symlink target's (size, mtime) is checked
  before and after each run (a change voids that run).  The comparison step is cfg289_compare.py.
"""
import json, os, shutil, subprocess, sys, time

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
ARCHIVE_DIRS = ["campaign_fresh_gravity", "hunt_2026", "real_research", "data_assembly",
                "qwen_claude_field_theory/papers_2026/mnras_submission_2026_v2"]
CSV_REL = "real_research/data/rc100_nestorshachar2023_table3.csv"
FIXED_REL = "real_research/data/rc100_nestorshachar2023_table3_CORRECTED.csv"
TIMEOUT = 1500

# (entry script, cwd: "root" or "dir", extra env)
ENTRIES = [
    ("campaign_fresh_gravity/CFG6_a0z_evidence.py", "root", {}),
    ("campaign_fresh_gravity/CFG52_a0z_feasibility/feas.py", "dir", {}),
    ("campaign_fresh_gravity/CFG90_a0z_rederivation/cfg90.py", "dir", {}),
    ("campaign_fresh_gravity/CFG216_rc100_within_sample/cfg216_rc100.py", "root", {}),
    ("campaign_fresh_gravity/CFG216_rc100_within_sample/cfg216_posthoc_index.py", "root", {}),
    ("campaign_fresh_gravity/CFG216_rc100_within_sample/rc100_input_correction_compare.py", "root", {}),
    ("campaign_fresh_gravity/CFG217_rc100_attack/cfg217_attack.py", "root", {}),
    ("campaign_fresh_gravity/CFG218_signal_vs_systematic/cfg218_ladder.py", "root", {}),
    ("campaign_fresh_gravity/CFG222_lcdm_proxy/cfg222_lcdm_proxy.py", "root", {}),
    ("campaign_fresh_gravity/CFG223_a0_over_cosmic_time/cfg223_a0_over_time.py", "root", {}),
    ("campaign_fresh_gravity/CFG227_rar_z2_5/cfg227_rar_z2_5.py", "root", {}),
    ("campaign_fresh_gravity/CFG233_rc100_referee/CFG233_main.py", "root", {}),
    ("campaign_fresh_gravity/CFG237_rar_z2_5_referee/CFG237_main.py", "root", {}),
    ("hunt_2026/h101_fdm_inversion_surveys.py", "root", {}),
    ("hunt_2026/h105_btfr_a0_meter.py", "root", {}),
    ("hunt_2026/h16_h27_h97.py", "root", {}),
    ("hunt_2026/k01_kernel_width_alpha.py", "root", {}),
    ("hunt_2026/k02_upsilon_amplification_a0z.py", "root", {}),
    ("hunt_2026/k03_a0z_desi_curve_and_upsilon_lever.py", "root", {}),
    ("hunt_2026/k04_inversion_upsilon_amplifier.py", "root", {}),
    ("hunt_2026/k_contrarian_lever.py", "root", {}),
    ("hunt_2026/k_high-z_amplified_scatter.py", "root", {}),
    ("hunt_2026/k_high-z_floor_census.py", "root", {}),
    ("qwen_claude_field_theory/papers_2026/mnras_submission_2026_v2/paper_numbers.py", "root", {}),
    ("real_research/a0z_clean_ledger.py", "root", {}),
    ("real_research/dark_sector_2026/L320_carrier_highz_price_rc100.py", "root", {}),
    ("real_research/dark_sector_2026/L322_additive_window_and_coincidence_test.py", "root", {}),
    ("real_research/dark_sector_2026/L323_rc100_framework_vs_lcdm_stress.py", "root", {}),
    ("real_research/dark_sector_2026/L332_kmos3d_trend_replication.py", "root", {}),
    ("real_research/rc100_audit_2026/L331_rc100_fairness_audit.py", "root", {}),
    ("real_research/papers/zimmerman_theory_figures.py", "root", {}),
    ("real_research/rc100_deepMOND_framework_fit.py", "root", {}),
]


def build_mirror(base):
    zf = os.path.join(base, "zf")
    if os.path.exists(zf):
        sys.exit(f"mirror {zf} exists -- use a fresh scratch dir")
    os.makedirs(zf)
    tar = subprocess.run(["git", "-C", REPO, "archive", "HEAD"] + ARCHIVE_DIRS, capture_output=True, check=True).stdout
    subprocess.run(["tar", "-x", "-C", zf], input=tar, check=True)
    links = []
    # git-ignored / untracked files inside the archived dirs: symlink read-through
    for d in ARCHIVE_DIRS:
        for root, dirs, files in os.walk(os.path.join(REPO, d)):
            dirs[:] = [x for x in dirs if x not in (".git", "__pycache__")]
            rel = os.path.relpath(root, REPO)
            for f in files:
                src = os.path.join(root, f)
                dst = os.path.join(zf, rel, f)
                if not os.path.lexists(dst):
                    os.makedirs(os.path.dirname(dst), exist_ok=True)
                    os.symlink(src, dst)
                    links.append(src)
    # everything else at the top level (and the parent's _external_data) read-through
    for name in os.listdir(REPO):
        if name in (".git",) or os.path.lexists(os.path.join(zf, name)):
            continue
        os.symlink(os.path.join(REPO, name), os.path.join(zf, name))
    ext = os.path.join(os.path.dirname(REPO), "_external_data")
    if os.path.exists(ext) and not os.path.lexists(os.path.join(base, "_external_data")):
        os.symlink(ext, os.path.join(base, "_external_data"))
    return zf, links


def stat_targets(links):
    out = {}
    for p in links:
        try:
            s = os.stat(p)
            out[p] = (s.st_size, s.st_mtime_ns)
        except OSError:
            out[p] = None
    return out


def snapshot(zf):
    """(size, mtime_ns) of every real (non-symlink) file in the archived dirs of the mirror."""
    snap = {}
    for d in ARCHIVE_DIRS:
        for root, dirs, files in os.walk(os.path.join(zf, d)):
            dirs[:] = [x for x in dirs if x != "__pycache__"]
            for f in files:
                p = os.path.join(root, f)
                if os.path.islink(p):
                    continue
                s = os.stat(p)
                snap[os.path.relpath(p, zf)] = (s.st_size, s.st_mtime_ns)
    return snap


def run_mode(scratch, mode, only):
    base = os.path.join(scratch, mode)
    os.makedirs(base, exist_ok=True)
    zf, links = build_mirror(base)
    csv_path = os.path.join(zf, CSV_REL)
    if mode == "FIX":
        shutil.copyfile(os.path.join(REPO, FIXED_REL), csv_path)
    elif mode == "MUTATE":
        rows = open(os.path.join(REPO, CSV_REL)).read().splitlines()
        hdr = rows[0].split(",")
        r1 = rows[1].split(",")
        i = hdr.index("Vc_Re_kms")
        r1[i] = str(int(float(r1[i]) * 2))
        rows[1] = ",".join(r1)
        open(csv_path, "w").write("\n".join(rows) + "\n")
    entries = ENTRIES if mode != "MUTATE" else [e for e in ENTRIES if "cfg216_rc100.py" in e[0]]
    if only:
        entries = [e for e in entries if any(s in e[0] for s in only)]
    # scripts write into their own folders: materialise every read-through symlink there as a real copy, so that a script
    # overwriting a git-ignored file writes into the mirror, never through to the repo
    for script, _, _ in entries:
        sd = os.path.join(zf, os.path.dirname(script))
        for root, dirs, files in os.walk(sd):
            for f in files:
                p = os.path.join(root, f)
                if os.path.islink(p):
                    src = os.path.realpath(p)
                    os.unlink(p)
                    shutil.copy2(src, p)
                    if src in links:
                        links.remove(src)
    manifest = dict(mode=mode, mirror=zf, csv_sha256=subprocess.run(["shasum", "-a", "256", csv_path], capture_output=True,
                                                                     text=True).stdout.split()[0], runs=[])
    for script, cwdk, extra in entries:
        before = snapshot(zf)
        tbefore = stat_targets(links)
        cwd = zf if cwdk == "root" else os.path.join(zf, os.path.dirname(script))
        env = dict(os.environ)
        for k in ("MUTATE", "DATA", "RC100_INPUT"):
            env.pop(k, None)
        env.update(extra)
        env["ZF_REPO"] = zf
        env["MPLBACKEND"] = "Agg"
        t0 = time.time()
        try:
            p = subprocess.run([sys.executable, os.path.join(zf, script)], cwd=cwd, env=env, capture_output=True, text=True,
                               timeout=TIMEOUT)
            rc, so, se = p.returncode, p.stdout, p.stderr
        except subprocess.TimeoutExpired as e:
            rc, so, se = "TIMEOUT", (e.stdout or b"").decode(errors="replace") if isinstance(e.stdout, bytes) else (e.stdout or ""), "timeout"
        dt = time.time() - t0
        after = snapshot(zf)
        tafter = stat_targets(links)
        touched_targets = [os.path.relpath(p, REPO) for p in links if tbefore.get(p) != tafter.get(p)]
        changed = sorted(k for k in after if before.get(k) != after[k])
        tag = os.path.splitext(os.path.basename(script))[0]
        logdir = os.path.join(base, "logs")
        os.makedirs(logdir, exist_ok=True)
        open(os.path.join(logdir, f"{tag}.stdout"), "w").write(so or "")
        open(os.path.join(logdir, f"{tag}.stderr"), "w").write(se or "")
        manifest["runs"].append(dict(script=script, cwd=cwdk, rc=rc, seconds=round(dt, 1), changed=changed,
                                     symlink_targets_written=touched_targets))
        print(f"[{mode}] {script}: rc={rc} {dt:.0f}s, {len(changed)} files written" +
              (f"  *** WROTE THROUGH SYMLINKS: {touched_targets}" if touched_targets else ""), flush=True)
        json.dump(manifest, open(os.path.join(base, "manifest.json"), "w"), indent=1)
    return manifest


if __name__ == "__main__":
    scratch = os.path.abspath(sys.argv[1])
    mode = sys.argv[2] if len(sys.argv) > 2 else "ALL"
    only = sys.argv[3:]
    modes = ["ORIG", "FIX", "MUTATE"] if mode == "ALL" else [mode]
    for m in modes:
        run_mode(scratch, m, only)
