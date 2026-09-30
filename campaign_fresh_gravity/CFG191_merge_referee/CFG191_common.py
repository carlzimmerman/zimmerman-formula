"""CFG191_common -- shared harness for the CFG191 referee scripts (no CFG179 import; no repo write).
Repo root: env ZF_REPO, else walk up from this file to the directory that holds prep_2026/gaia_dr4_prep. Printed as <repo>.
Exit convention: exit 1 iff any load-bearing (LB) check fails (main: a control or LB check failed; MUTATE=1: the control bites)."""
import os, sys, json, pathlib, time
sys.dont_write_bytecode = True
HERE = pathlib.Path(__file__).resolve().parent

def find_repo():
    cands = []
    env = os.environ.get("ZF_REPO")
    if env:
        cands.append(pathlib.Path(env))
    p = HERE
    for _ in range(8):
        cands.append(p); p = p.parent
    for c in cands:
        if (c / "prep_2026" / "gaia_dr4_prep").is_dir():
            return c
    raise SystemExit("repo root not found; set ZF_REPO")

REPO = find_repo()

def rel(path):
    try:
        return "<repo>/" + str(pathlib.Path(path).resolve().relative_to(REPO.resolve()))
    except Exception:
        return "<external>/" + pathlib.Path(path).name

class Run:
    def __init__(self, name, title):
        self.name = name
        self.mutate = os.environ.get("MUTATE", "") not in ("", "0")
        self.lines, self.checks, self.findings, self.data = [], [], [], {}
        self.t0 = time.time()
        self.p("=" * 110)
        self.p(f"{name} -- {title}" + ("   [MUTATE=1]" if self.mutate else ""))
        self.p(f"repo = <repo>   (read-only inputs; nothing is written into the repo)")
        self.p("=" * 110)
    def p(self, *a):
        s = " ".join(str(x) for x in a)
        print(s); sys.stdout.flush()
        self.lines.append(s)
    def sec(self, s):
        self.p(""); self.p("-" * 110); self.p(s); self.p("-" * 110)
    def check(self, label, cond, detail="", lb=True):
        ok = bool(cond)
        self.checks.append(dict(label=label, ok=ok, lb=lb, detail=detail))
        self.p(f"  [{'PASS' if ok else 'FAIL'}]{'' if lb else ' (not load-bearing)'} {label}" + (f"\n         {detail}" if detail else ""))
        return ok
    def finding(self, item, verdict, detail):
        self.findings.append(dict(item=item, verdict=verdict, detail=detail))
        self.p(f"  FINDING {item}: {verdict}\n         {detail}")
    def finish(self):
        lbfail = [c["label"] for c in self.checks if c["lb"] and not c["ok"]]
        self.p(""); self.p("=" * 110)
        self.p(f"CHECKS: {sum(c['ok'] for c in self.checks)}/{len(self.checks)} pass; load-bearing failures: {len(lbfail)}  ({time.time()-self.t0:.0f} s)")
        if self.mutate:
            self.p("MUTATE control " + ("BITES (exit 1): " + "; ".join(lbfail) if lbfail else "DID NOT BITE (exit 0) -- control is toothless"))
        elif lbfail:
            self.p("LOAD-BEARING FAILURES (kept, not repaired): " + "; ".join(lbfail))
        suffix = "_MUTATE" if self.mutate else ""
        (HERE / f"{self.name}{suffix}.out").write_text("\n".join(self.lines) + "\n")
        (HERE / f"{self.name}{suffix}_results.json").write_text(json.dumps(dict(name=self.name, mutate=self.mutate, checks=self.checks, findings=self.findings, data=self.data), indent=1, default=float))
        sys.exit(1 if lbfail else 0)
