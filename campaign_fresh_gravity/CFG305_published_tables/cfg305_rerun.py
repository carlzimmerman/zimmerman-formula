#!/usr/bin/env python3
"""CFG305 step 3 (a parametrised copy of CFG289's cfg289_rerun.py; CFG289's committed file is untouched): re-run every reader of the
RC100 CSV with ORIG = the CORRECTED CSV and FIX = the PUBLISHED CSV, each in its own scratch mirror of the repo (FROZEN_CRITERIA.md,
82dfcc1b3).

Two reader groups (frozen):
  O  readers of the original path (CFG289's 32 entry points + four RC100_INPUT=corrected runs).
       ORIG: the CORRECTED CSV substituted at the original path.
       FIX:  the PUBLISHED CSV at the original path AND at the CORRECTED path; the paper-values file with the confirmed cells replaced.
       MUTATE: as FIX, with the MUTATE copy (row 50 log M_baryon +0.30 dex) instead of the PUBLISHED CSV; L323 and cfg216_rc100.py only.
  C  readers of the CORRECTED path (CFG217 corrected mode, the MNRAS v3 paper_numbers.py read-only, CFG290's referee checks).
       ORIG: nothing substituted.   FIX: the PUBLISHED CSV at the CORRECTED path; the paper-values file with the confirmed cells
       replaced; the original path untouched (paper_numbers reads it as "the earlier transcription").
Usage:  python3 campaign_fresh_gravity/CFG305_published_tables/cfg305_rerun.py <scratch_dir> <O|C> [ORIG|FIX|MUTATE|ALL] [entry-substring ...]
  The mirror of each run is <scratch_dir>/<group>_<mode>/zf (git archive of HEAD for the dirs below; everything else, including
  git-ignored files inside those dirs, is symlinked read-through).  Writes manifests <scratch_dir>/<group>_<mode>/manifest.json.  The
  committed repo is never written: the mirror dirs that scripts write into are real copies, and every symlink target's (size, mtime) is
  checked before and after each run (a change voids that run).  The comparison step is cfg305_compare.py.
"""
import json, os, shutil, subprocess, sys, time

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
ARCHIVE_DIRS = ["campaign_fresh_gravity", "hunt_2026", "real_research", "data_assembly",
                "qwen_claude_field_theory/papers_2026/mnras_submission_2026_v2",
                "qwen_claude_field_theory/papers_2026/mnras_submission_2026_v3"]
CSV_REL = "real_research/data/rc100_nestorshachar2023_table3.csv"
CORR_REL = "real_research/data/rc100_nestorshachar2023_table3_CORRECTED.csv"
PUB_REL = "real_research/data/rc100_nestorshachar2023_table3_PUBLISHED.csv"
PV_REL = "data_assembly/rc100_provenance/rc100_table3_six_fields_paper_values.csv"
CONF = os.path.join(HERE, "cfg305_confirm_results.json")
TIMEOUT = 1500
CORRMODE = {"RC100_INPUT": "corrected"}

# (entry script, cwd: "root" or "dir", extra env)
ENTRIES = [
    ("campaign_fresh_gravity/CFG6_a0z_evidence.py", "root", {}),
    ("campaign_fresh_gravity/CFG52_a0z_feasibility/feas.py", "dir", {}),
    ("campaign_fresh_gravity/CFG90_a0z_rederivation/cfg90.py", "dir", {}),
    ("campaign_fresh_gravity/CFG216_rc100_within_sample/cfg216_rc100.py", "root", {}),
    ("campaign_fresh_gravity/CFG216_rc100_within_sample/cfg216_rc100.py", "root", CORRMODE),
    ("campaign_fresh_gravity/CFG216_rc100_within_sample/cfg216_posthoc_index.py", "root", {}),
    ("campaign_fresh_gravity/CFG216_rc100_within_sample/cfg216_posthoc_index.py", "root", CORRMODE),
    ("campaign_fresh_gravity/CFG217_rc100_attack/cfg217_attack.py", "root", {}),
    ("campaign_fresh_gravity/CFG217_rc100_attack/cfg217_attack.py", "root", CORRMODE),
    ("campaign_fresh_gravity/CFG218_signal_vs_systematic/cfg218_ladder.py", "root", {}),
    ("campaign_fresh_gravity/CFG218_signal_vs_systematic/cfg218_ladder.py", "root", CORRMODE),
    # moved after CFG216-218 (frozen): it compares their outputs
    ("campaign_fresh_gravity/CFG216_rc100_within_sample/rc100_input_correction_compare.py", "root", {}),
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
ENTRIES_C = [
    ("campaign_fresh_gravity/CFG217_rc100_attack/cfg217_attack.py", "root", CORRMODE),
    ("qwen_claude_field_theory/papers_2026/mnras_submission_2026_v3/paper_numbers.py", "root", {}),
    ("campaign_fresh_gravity/CFG290_mnras_v3_referee/cfg290_referee_checks.py", "root", {}),
]
MUTATE_ENTRIES = ("L323_rc100_framework_vs_lcdm_stress.py", "CFG216_rc100_within_sample/cfg216_rc100.py")
# a committed file the captured stdout of an entry is also compared with (reproduction control)
STDOUT_REF = {"qwen_claude_field_theory/papers_2026/mnras_submission_2026_v3/paper_numbers.py":
              "qwen_claude_field_theory/papers_2026/mnras_submission_2026_v3/paper_numbers.out"}


def tag_of(script, extra):
    t = os.path.splitext(os.path.basename(script))[0]
    return t + ("__" + "_".join(f"{k}-{v}" for k, v in sorted(extra.items())) if extra else "")


def paper_values_published(dst):
    """the mirror copy of the paper-values file with the CONFIRMED cells replaced (string as printed); every other byte unchanged"""
    conf = json.load(open(CONF))["rc100_confirmed_cells"]
    cmap = {(c["idx"], c["field"]): c["published"] for c in conf}
    raw = open(os.path.join(REPO, PV_REL), newline="").read()
    nl = "\r\n" if "\r\n" in raw else "\n"
    rows = raw.split(nl)
    hdr = rows[0].split(",")
    import csv as _csv, io as _io
    n = 0
    for k in range(1, len(rows)):
        if not rows[k]:
            continue
        cells = next(_csv.reader(_io.StringIO(rows[k])))
        hit = False
        for f in hdr:
            if (cells[0], f) in cmap:
                cells[hdr.index(f)] = cmap[(cells[0], f)]
                hit = True
                n += 1
        if hit:
            b = _io.StringIO()
            _csv.writer(b, lineterminator="").writerow(cells)
            rows[k] = b.getvalue()
    open(dst, "w", newline="").write(nl.join(rows))
    return n


def clone(src, dst):
    """CFG305: an APFS copy-on-write clone (clonefile) where possible, else a byte copy.  CFG289 byte-copied every read-through file
    under an entry's directory; for the real_research entries that is ~47 GB and the disk could not hold it (disclosed).  A clone has
    the same content and is a separate file, so a script that overwrites it writes into the mirror only."""
    try:
        import ctypes
        libc = ctypes.CDLL("libc.dylib", use_errno=True)
        if libc.clonefile(src.encode(), dst.encode(), 0) == 0:
            return
    except Exception:
        pass
    shutil.copy2(src, dst)


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


def substitute(zf, path_rel, src):
    p = os.path.join(zf, path_rel)
    if os.path.islink(p):
        os.unlink(p)            # never write through a read-through link
    shutil.copyfile(src, p)


def run_mode(scratch, group, mode, only):
    base = os.path.join(scratch, f"{group}_{mode}")
    os.makedirs(base, exist_ok=True)
    zf, links = build_mirror(base)
    subs = {}
    if group == "O" and mode == "ORIG":
        substitute(zf, CSV_REL, os.path.join(REPO, CORR_REL)); subs[CSV_REL] = "CORRECTED"
    elif mode in ("FIX", "MUTATE"):
        if mode == "FIX":
            src, lab = os.path.join(REPO, PUB_REL), "PUBLISHED"
        else:
            src, lab = os.path.join(base, "rc100_MUTATE.csv"), "MUTATE (PUBLISHED, row 50 logMbar +0.30)"
            subprocess.run([sys.executable, os.path.join(HERE, "cfg305_build_published.py"), src], env=dict(os.environ, MUTATE="1"), check=True)
        if group == "O":
            substitute(zf, CSV_REL, src); subs[CSV_REL] = lab
        substitute(zf, CORR_REL, src); subs[CORR_REL] = lab
        pvp = os.path.join(zf, PV_REL)
        if os.path.islink(pvp):
            os.unlink(pvp)
        npv = paper_values_published(pvp); subs[PV_REL] = f"confirmed cells replaced ({npv})"
    if group == "O":
        entries = ENTRIES if mode != "MUTATE" else [e for e in ENTRIES if any(m in e[0] for m in MUTATE_ENTRIES) and not e[2]]
    else:
        assert mode in ("ORIG", "FIX"), "group C has no MUTATE run (its liveness check is the printed sha256)"
        entries = ENTRIES_C
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
                    clone(src, p)
                    if src in links:
                        links.remove(src)
    shas = {rel: subprocess.run(["shasum", "-a", "256", os.path.join(zf, rel)], capture_output=True, text=True).stdout.split()[0]
            for rel in (CSV_REL, CORR_REL, PV_REL)}
    manifest = dict(group=group, mode=mode, mirror=zf, substituted=subs, sha256=shas, csv_sha256=shas[CSV_REL], runs=[])
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
        tag = tag_of(script, extra)
        logdir = os.path.join(base, "logs")
        os.makedirs(logdir, exist_ok=True)
        open(os.path.join(logdir, f"{tag}.stdout"), "w").write(so or "")
        open(os.path.join(logdir, f"{tag}.stderr"), "w").write(se or "")
        manifest["runs"].append(dict(script=script, tag=tag, extra=extra, cwd=cwdk, rc=rc, seconds=round(dt, 1), changed=changed,
                                     symlink_targets_written=touched_targets, stdout_ref=STDOUT_REF.get(script)))
        print(f"[{group}_{mode}] {tag}: rc={rc} {dt:.0f}s, {len(changed)} files written" +
              (f"  *** WROTE THROUGH SYMLINKS: {touched_targets}" if touched_targets else ""), flush=True)
        json.dump(manifest, open(os.path.join(base, "manifest.json"), "w"), indent=1)
    return manifest


if __name__ == "__main__":
    scratch = os.path.abspath(sys.argv[1])
    group = sys.argv[2]
    assert group in ("O", "C")
    mode = sys.argv[3] if len(sys.argv) > 3 else "ALL"
    only = sys.argv[4:]
    modes = (["ORIG", "FIX", "MUTATE"] if group == "O" else ["ORIG", "FIX"]) if mode == "ALL" else [mode]
    for m in modes:
        run_mode(scratch, group, m, only)
