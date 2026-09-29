#!/usr/bin/env python3
"""ledger_rerun3.py -- independent re-run of newly committed campaign lanes from a clean `git archive HEAD` export.

Exports a broad set of directories (campaign_fresh_gravity, real_research, prep_2026, hunt_2026, data_assembly,
fable_independent_2026 without lean_2026, opus_48_extended_research) at HEAD so every dependency the scripts load is present,
runs each script main + MUTATE, and records: exact exit code, expected exit code, and whether the script's own final tally
line equals the tally line in the lane's COMMITTED .out (timing fields stripped). Usage: ledger_rerun3.py SCRATCH [slug ...]
Nothing under the working tree is touched. Expected exits come from the lanes' READMEs (stated in JOBS) or, where the README is
silent, from the committed .out's own tally (see JOBS) (failures > 0 => exit 1).
"""
import json, os, re, subprocess, sys, tempfile

REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
scratch = sys.argv[1] if len(sys.argv) > 1 else tempfile.mkdtemp(prefix="ledger_rerun3_")
only = set(sys.argv[2:])
head = subprocess.run(["git", "rev-parse", "HEAD"], cwd=REPO, capture_output=True, text=True).stdout.strip()
CF = "campaign_fresh_gravity"
# slug: (dir relative to repo, script, main-arg-or-env, expected main exit or None=derive, committed .out, mutate style)
JOBS = {
    "CFG61": (CF, "CFG61_kids_colour_split.py", 1, "CFG61_kids_colour_split.out", "env"),
    "CFG62": (CF, "CFG62_population_split.py", None, "CFG62_population_split.out", "env"),
    "CFG63": (CF + "/CFG63_discrimination_forecast", "forecast.py", 0, "forecast.out", "arg"),
    "CFG64": (CF + "/CFG64_kernel_robustness", "CFG64_kernel_robustness.py", 1, "cfg64_kernel_robustness.out", "env"),
    "CFG65": (CF, "CFG65_debris_shape.py", 0, "CFG65_debris_shape.out", "env"),
    "CFG66": (CF, "CFG66_bootes_tucana_systematics.py", 0, "CFG66_bootes_tucana_systematics.out", "env"),
    "CFG67": (CF, "CFG67_lcdm_control_kids_split.py", None, "CFG67_lcdm_control_kids_split.out", "env"),
    "CFG68": (CF, "CFG68_lcdm_super_spirals.py", 1, "CFG68_lcdm_super_spirals.out", "env"),                       # README: main exits 1 (H1 failed)
    "CFG69": (CF, "CFG69_lcdm_comparator.py", None, "CFG69_lcdm_comparator.out", "env"),
    "CFG70": (CF + "/CFG70_memory_kernel_exchange", "cfg70_memory_kernel_exchange.py", None, "cfg70_memory_kernel_exchange.out", "env", ("a", "b", "1")),
    "CFG71": (CF, "CFG71_universal_fraction_dynamical_sluggs.py", None, "CFG71_universal_fraction_dynamical_sluggs.out", "env"),
    "CFG72": (CF + "/CFG72_lightcone_exchange", "cfg72_lightcone_exchange.py", 1, "cfg72_lightcone_exchange.out", "env", ("a", "b", "c", "1")),   # README: rc 1 by design
    "CFG73": (CF, "CFG73_lcdm_uf_rederive.py", 1, "CFG73_lcdm_uf_rederive.out", "env"),                             # README: rc 1 by design
    "CFG74": (CF, "CFG74_lcdm_variants.py", 1, "CFG74_lcdm_variants.out", "env"),                                   # README: rc 1 by design
}
paths = [CF, "real_research", "prep_2026", "hunt_2026", "data_assembly", "opus_48_extended_research",
         "fable_independent_2026", ":(exclude)fable_independent_2026/lean_2026"]
os.makedirs(scratch, exist_ok=True)
if not os.path.isdir(os.path.join(scratch, CF)):
    ar = subprocess.Popen(["git", "archive", "HEAD"] + paths, cwd=REPO, stdout=subprocess.PIPE)
    subprocess.run(["tar", "-x", "-C", scratch], stdin=ar.stdout, check=True)
print("exported HEAD", head[:9], "to", scratch, flush=True)

def committed_tally(relpath):
    """last tally-looking line of the lane's committed .out, read from git (not from the run copy)."""
    r = subprocess.run(["git", "show", f"HEAD:{relpath}"], cwd=REPO, capture_output=True, text=True)
    return last_tally(r.stdout) if r.returncode == 0 else ""

def last_tally(out):
    for ln in reversed(out.strip().splitlines()):
        if re.search(r"\b\d+\s*/\s*\d+\b|checks pass|load-bearing|failures", ln):
            return re.sub(r"\(\s*\d+\s*s\s*\)|\s+", " ", ln).strip()[:170]
    return ""

results = []
for slug, spec in JOBS.items():
    d, script, exp_main, out_name, style = spec[:5]
    mut_modes = spec[5] if len(spec) > 5 else ("1",)
    if only and slug not in only:
        continue
    cwd = os.path.join(scratch, d)
    ctally = committed_tally(f"{d}/{out_name}")
    if exp_main is None:
        m = re.search(r"failures\D*(\d+)", ctally)
        exp_main = 1 if (m and int(m.group(1)) > 0) else 0
    runs = [("main", exp_main, None)] + [(("MUTATE" if m == "1" else f"MUTATE={m}"), 1, m) for m in mut_modes]
    for label, expect, mval in runs:
        e = dict(os.environ); e.pop("MUTATE", None)
        args = [sys.executable, script]
        if label != "main":
            if style == "env": e["MUTATE"] = mval
            else: args.append("MUTATE")
        try:
            p = subprocess.run(args, cwd=cwd, env=e, capture_output=True, text=True, timeout=1800)
            code, out = p.returncode, p.stdout + p.stderr
        except subprocess.TimeoutExpired:
            code, out = -9, "TIMEOUT"
        tb = "Traceback" in out
        tally = last_tally(out)
        same = (tally == ctally) if label == "main" else None
        results.append(dict(slug=slug, mode=label, exit=code, expect=expect, match=(code == expect) and not tb,
                            traceback=tb, tally=tally, committed_tally=ctally if label == "main" else None, tally_same=same))
        flag = "OK " if (code == expect and not tb) else "DIFFERS"
        print(f"{slug:<6}{label:<8} exit {code:>3} (expected {expect}) {flag}{' TRACEBACK' if tb else ''}"
              f"{'' if same is None else ('  tally==committed' if same else '  TALLY DIFFERS')}  {tally}", flush=True)
        if label == "main" and same is False:
            print(f"        committed tally: {ctally}", flush=True)
json.dump(dict(head=head, results=results), open(os.path.join(scratch, "ledger_rerun3_results.json"), "w"), indent=1)
bad = [r for r in results if not r["match"] or r["tally_same"] is False]
print(f"\n{len(results)} runs at HEAD {head[:9]}; {len(bad)} differ (exit code, traceback or tally)")
for r in bad:
    print("  DIFFERS:", r["slug"], r["mode"], "exit", r["exit"], "expected", r["expect"], "| tally same:", r["tally_same"])
