#!/usr/bin/env python3
"""Run A74 mutations, record exit code and the checks each kills.  Merges into
mutation_results.json so the sweep can be done in batches."""
import os, re, json, subprocess, sys, time

HERE = os.path.dirname(os.path.abspath(__file__))
ALL = ["drop_gal", "drop_lens", "floor10", "a0_off20", "sersic35", "arcsec",
       "imf_prior", "no_boot", "boot_draws", "kappa_de", "thermal_pi", "treu_shift",
       "u_prior", "cluster_a", "b_marg", "resp_lin", "lambda_off", "ups_window",
       "h0_70", "omega"]
JF = os.path.join(HERE, "mutation_results.json")
rows = json.load(open(JF)) if os.path.exists(JF) else []
done = {r["mut"] for r in rows}

mode = sys.argv[1] if len(sys.argv) > 1 else "all"
MUTS = ALL if mode == "all" else [m for m in mode.split(",") if m in ALL]

for m in MUTS:
    if m in done:
        continue
    t0 = time.time()
    env = dict(os.environ, A74_MUTATE=m)
    r = subprocess.run([sys.executable, os.path.join(HERE, "a74_checks.py")],
                       env=env, capture_output=True, text=True)
    out = r.stdout + r.stderr
    fails = re.findall(r"^\s+(C\d+)\s+FAIL", out, re.M)
    crash = "Traceback" in out
    row = dict(mut=m, exit=int(r.returncode), fails=sorted(set(fails), key=lambda s: int(s[1:])),
               crash=crash, secs=round(time.time() - t0, 1))
    rows = [x for x in rows if x["mut"] != m] + [row]
    rows.sort(key=lambda x: ALL.index(x["mut"]))
    json.dump(rows, open(JF, "w"), indent=1)
    print("%-12s exit %d  %5.1fs  %s%s" % (m, r.returncode, time.time() - t0,
                                           ",".join(row["fails"]) or "-",
                                           "  CRASH" if crash else ""), flush=True)

print("\nkill matrix so far (%d/%d):" % (len(rows), len(ALL)))
for r in rows:
    print("  %-12s exit %d  kills %s" % (r["mut"], r["exit"], ", ".join(r["fails"]) or "NOTHING"))
killed = set()
for r in rows:
    killed |= set(r["fails"])
print("\nchecks killed by at least one mutation:", len(killed))
