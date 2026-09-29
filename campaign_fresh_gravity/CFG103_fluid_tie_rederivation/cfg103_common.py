"""Shared helpers for CFG103 (independent re-derivation of CFG43).  Path-independent: outputs go next to the script.
MUTATE env var: 0 (default), 1 (multiplier replaced by a dynamical scalar), 2 (tie dropped).  Checks are recorded, printed, and
mirrored into <script>[_MUTATEk].out; exit code 1 if any load-bearing check failed."""
import os, sys, io, json

MUTATE = int(os.environ.get("MUTATE", "0"))
HERE = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.environ.get("CFG_REPO_ROOT") or os.path.abspath(os.path.join(HERE, *([os.pardir] * 0)))  # not used to read anything

class Log:
    def __init__(self, script):
        base = os.path.splitext(os.path.basename(script))[0]
        self.path = os.path.join(HERE, base + ("" if MUTATE == 0 else "_MUTATE%d" % MUTATE) + ".out")
        self.buf = io.StringIO(); self.checks = []
    def p(self, *a):
        s = " ".join(str(x) for x in a); print(s); self.buf.write(s + "\n")
    def check(self, name, ok, detail=""):
        self.checks.append((name, bool(ok), detail))
        self.p("[%s] %-34s %s" % ("PASS" if ok else "FAIL", name, detail))
    def finish(self, results=None):
        nf = sum(1 for c in self.checks if not c[1])
        self.p("SUMMARY MUTATE=%d: %d checks, %d failed" % (MUTATE, len(self.checks), nf))
        with open(self.path, "w") as f: f.write(self.buf.getvalue())
        if results is not None:
            with open(self.path.replace(".out", "_results.json"), "w") as f: json.dump(results, f, indent=1, default=float)
        sys.exit(1 if nf else 0)
