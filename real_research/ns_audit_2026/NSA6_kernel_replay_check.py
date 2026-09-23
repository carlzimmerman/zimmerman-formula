#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
NSA6 -- IS THE OPENAI (C) PROOF REALLY CHECKED?  Kernel replay of every declaration, and a source scan for anything
that could slip past the kernel.  (Follow-up to NSA4, which showed the proved statement IS Fefferman's (C)/(D).)

WHAT #print axioms CANNOT SEE
  A declaration added to the environment without passing the kernel (environment hacking: unsafe metaprogramming,
  `debug.skipKernelTC`, hand-written oleans) leaves no axiom footprint.  `leanchecker` -- the lean4checker tool
  upstreamed into the Lean toolchain (v4.34.0-rc2 ships it) -- reloads each compiled module and REPLAYS every new
  declaration through the kernel.  `--fresh` replays the whole import closure, Mathlib included, into an empty
  environment.

CHECKS
  K1 SOURCE SCAN of the 817 project .lean files: no sorry/admit, no `axiom`, no native_decide / ofReduceBool /
     trustCompiler, no implemented_by / extern / csimp, no `unsafe`, no environment-editing API, no
     debug.skipKernelTC, no custom syntax / elab / macro, no run_cmd / #eval, no set_option, no `opaque`, no
     `import Lean` metaprogramming.
  K2 `lake env leanchecker <module>` for each of the 816 compiled NavierStokes.* modules, one process per module,
     NPAR (default 6) at a time: every declaration replayed through the kernel on top of its imports; every exit 0
     required.  HISTORY: a first attempt ran all modules in ONE process (leanchecker starts every module's replay
     at once); it was killed for memory (exit 137) after 22.7 min, printing a 'problem' in
     NavierStokes.PeriodicViscosity -- that module replays alone with exit 0, so the flag was the kill, not the
     kernel.  Hence one bounded process per module.
  K3 (FRESH=1 only) `lake env leanchecker --fresh NavierStokes.ComparatorSolution`: the ENTIRE closure of the
     submitted theorem -- all of Mathlib plus the project -- replayed into an empty environment.  Slow; run
     separately and recorded when done.
  WHAT THIS STILL TRUSTS: the Lean C++ kernel itself (leanchecker uses the same kernel; an independent
  implementation such as nanoda or lean4lean would remove that) and Mathlib's definitions meaning what they say
  (checked for the statement's constants in NSA4 F4).
  MUTATE=1 runs the K1 scanner on a synthetic hostile snippet (sorry, axiom, native_decide, skipKernelTC,
  unsafe): it must flag all five and K1 must FAIL (rc = 1).

Run from the repository root:  python3 real_research/ns_audit_2026/NSA6_kernel_replay_check.py   (FRESH=1 adds K3)
"""
import os, re, sys, json, time, subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
CLONE = os.path.join(ROOT, "deepseek_push", "navier_stokes_attempt", "openai_NS_lean")
MUTATE = os.environ.get("MUTATE", "0") == "1"
FRESH = os.environ.get("FRESH", "0") == "1"
SLUG = "NSA6_kernel_replay_check"
P = lambda *a: print(*a, flush=True)
CH, OUT = [], {"lane": "NSA6", "mutate": MUTATE, "fresh": FRESH, "checks": {}, "numbers": {}}


def check(name, measured, ok, reading="", load_bearing=True):
    ok = bool(ok)
    CH.append((name, ok, load_bearing))
    OUT["checks"][name] = {"ok": ok, "measured": str(measured), "load_bearing": load_bearing}
    P(f"  [{'PASS' if ok else 'FAIL'}] {name}")
    P(f"         measured: {measured}")
    if reading:
        P(f"         reading:  {reading}")
    return ok


def banner(t):
    P("\n" + "=" * 104); P(t); P("=" * 104)


def strip_comments(src):
    src = re.sub(r"/-.*?-/", "", src, flags=re.S)
    return re.sub(r"--[^\n]*", "", src)


PATTERNS = {
    "sorry/admit": r"\bsorry\b|\badmit\b",
    "axiom": r"^\s*(private\s+|protected\s+)?axiom\s",
    "native_decide/ofReduceBool/trustCompiler": r"\bnative_decide\b|ofReduceBool|reduceBool|trustCompiler",
    "implemented_by/extern/csimp": r"implemented_by|@\[extern|@\[csimp",
    "unsafe": r"\bunsafe\b",
    "environment API": r"addDeclWithoutChecking|addDeclCore|Kernel\.Environment|modifyEnv|setEnv",
    "skipKernelTC": r"skipKernelTC",
    "custom syntax/elab/macro": r"^\s*(elab|elab_rules|macro_rules|macro|syntax|declare_syntax_cat)\b",
    "run_cmd/#eval": r"run_cmd|run_elab|run_meta|#eval",
    "set_option": r"\bset_option\b",
    "opaque": r"^\s*(private\s+)?opaque\s",
    "Lean metaprogramming import": r"^\s*import\s+Lean\b|Lean\.Elab|Lean\.Meta",
}


def scan(texts):
    hits = {k: [] for k in PATTERNS}
    for name, txt in texts:
        body = strip_comments(txt)
        for k, pat in PATTERNS.items():
            if re.search(pat, body, flags=re.M):
                hits[k].append(name)
    return hits


if not os.path.isdir(CLONE):
    P(f"OpenAI clone not found at {CLONE}"); sys.exit(2)
commit = subprocess.run(["git", "-C", CLONE, "rev-parse", "HEAD"], capture_output=True, text=True).stdout.strip()
OUT["numbers"]["clone_commit"] = commit
P(f"OpenAI clone commit {commit}")

# ============================================================================================ K1
banner("K1  SOURCE SCAN FOR ANYTHING THAT COULD BYPASS OR WEAKEN THE KERNEL")
files = []
for base in ("NavierStokes",):
    for dp, _, fns in os.walk(os.path.join(CLONE, base)):
        files += [os.path.join(dp, f) for f in fns if f.endswith(".lean")]
files.append(os.path.join(CLONE, "NavierStokes.lean"))
texts = [(os.path.relpath(f, CLONE), open(f, encoding="utf-8").read()) for f in files]
if MUTATE:
    texts.append(("SYNTHETIC_HOSTILE.lean", "set_option debug.skipKernelTC true\naxiom cheat : False\n"
                  "unsafe def x : Nat := 0\ntheorem t : 1 = 1 := by native_decide\ntheorem s : False := sorry\n"))
hits = scan(texts)
for k, v in hits.items():
    P(f"    {k:42s} {len(v):3d} file(s){'  ' + ', '.join(v[:3]) if v else ''}")
OUT["numbers"]["K1"] = {"n_files": len(texts), "hits": hits}
nhit = sum(len(v) for v in hits.values())
check("K1 the project source contains no sorry, axiom, native_decide, unsafe code, environment API, "
      "skipKernelTC, custom elaborators, #eval, set_option or opaque", f"{len(texts)} files scanned; {nhit} hits",
      nhit == 0, "plain Mathlib-style proofs: nothing in the source can route a declaration around the kernel")

# ============================================================================================ K2
banner("K2  leanchecker: REPLAY EVERY NavierStokes.* DECLARATION THROUGH THE KERNEL (one process per module)")
if MUTATE:
    P("    (skipped under MUTATE)")
else:
    from concurrent.futures import ThreadPoolExecutor
    NPAR = int(os.environ.get("NPAR", "6"))                   # ~5 GB per process: bounded concurrency
    libdir = os.path.join(CLONE, ".lake", "build", "lib", "lean")
    mods = sorted(os.path.relpath(os.path.join(dp, f), libdir)[:-6].replace(os.sep, ".")
                  for dp, _, fns in os.walk(os.path.join(libdir, "NavierStokes")) for f in fns if f.endswith(".olean"))

    def replay(m):
        t = time.time()
        r = subprocess.run(["lake", "env", "leanchecker", m], cwd=CLONE, capture_output=True, text=True, timeout=3600)
        err = (r.stdout + r.stderr).strip().replace(ROOT + os.sep, "")
        return m, r.returncode, time.time() - t, err

    t0 = time.time()
    with ThreadPoolExecutor(max_workers=NPAR) as ex:
        rows = list(ex.map(replay, mods))
    dt = time.time() - t0
    bad = [(m, rc, e[-300:]) for m, rc, _, e in rows if rc != 0]
    with open(os.path.join(HERE, f"{SLUG}_leanchecker.log"), "w") as fh:
        for m, rc, sec, e in rows:
            fh.write(f"{m}\trc={rc}\t{sec:.1f}s\t{e.splitlines()[-1] if e else ''}\n")
    P(f"    {len(mods)} modules replayed, {NPAR} at a time; failures {len(bad)}; wall {dt / 60:.1f} min; "
      f"slowest {max(r[2] for r in rows):.0f} s")
    for m, rc, e in bad[:10]:
        P(f"      FAIL {m} rc={rc}: {e}")
    OUT["numbers"]["K2"] = {"modules": len(mods), "npar": NPAR, "failures": bad, "wall_s": dt,
                            "first_attempt": "all modules at once in one process: killed (exit 137, memory) after "
                                             "22.7 min; the flagged module NavierStokes.PeriodicViscosity then "
                                             "replayed alone with exit 0 (10 s, 5 GB)"}
    check("K2 every declaration in every one of the NavierStokes.* modules replays through the Lean kernel",
          f"{len(mods)} modules; failures {len(bad)}", len(mods) >= 800 and not bad,
          "no environment hacking: what the compiled files contain is what the kernel accepts")

# ============================================================================================ K3
if FRESH and not MUTATE:
    banner("K3  leanchecker --fresh: THE WHOLE CLOSURE (MATHLIB + PROJECT) INTO AN EMPTY ENVIRONMENT")
    t0 = time.time()
    r = subprocess.run(["lake", "env", "leanchecker", "--fresh", "-v", "NavierStokes.ComparatorSolution"],
                       cwd=CLONE, capture_output=True, text=True)
    dt = time.time() - t0
    log = (r.stdout + r.stderr).replace(ROOT + os.sep, "")
    open(os.path.join(HERE, f"{SLUG}_fresh.log"), "w").write(log)
    P(f"    exit {r.returncode}; wall {dt / 60:.1f} min")
    OUT["numbers"]["K3"] = {"exit": r.returncode, "wall_s": dt, "log_tail": log.splitlines()[-5:]}
    check("K3 the entire import closure of the submitted theorem replays into an empty environment",
          f"exit {r.returncode}; {dt / 60:.1f} min", r.returncode == 0,
          "Mathlib's compiled files are also kernel-clean for everything the theorem uses")

# ============================================================================================ verdict
banner("VERDICT")
n_fail = sum(1 for _, ok, lb in CH if lb and not ok)
if MUTATE:
    P("  MUTATE: the scanner " + ("flagged the hostile snippet, as required." if n_fail else "MISSED the hostile snippet (bad)."))
elif n_fail:
    P("  A check failed; see above.  No trust conclusion is drawn from this run.")
else:
    P("""  The OpenAI proof is what it appears to be at the machine level: plain Mathlib-style source with no
  kernel-bypass constructs, and every project declaration re-accepted by the Lean kernel on replay.  Together with
  NSA4 (the proved statement is Fefferman's (C)/(D), verbatim), the remaining trust is in the Lean kernel
  implementation itself and in the Clay process -- not in OpenAI's code.""")

OUT["n_checks"], OUT["n_fail_load_bearing"] = len(CH), n_fail
outname = f"{SLUG}_results{'_MUTATE' if MUTATE else ''}{'_FRESH' if FRESH and not MUTATE else ''}.json"
json.dump(OUT, open(os.path.join(HERE, outname), "w"), indent=1, default=str)
P(f"\n  {sum(1 for _, ok, _ in CH if ok)}/{len(CH)} checks pass; load-bearing failures: {n_fail}; wrote {outname}")
sys.exit(0 if n_fail == 0 else 1)
