# CFG195_common.py -- shared plumbing for the CFG195 referee scripts (output convention, repo lookup, checks).
import os, sys, json
os.environ.setdefault("OMP_NUM_THREADS", "2"); os.environ.setdefault("OPENBLAS_NUM_THREADS", "2")
sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))

def find_repo():
    p = os.environ.get("ZF_REPO")
    if p and os.path.isdir(os.path.join(p, "campaign_fresh_gravity")):
        return p
    d = HERE
    for _ in range(12):
        if os.path.isdir(os.path.join(d, "campaign_fresh_gravity")) and os.path.isdir(os.path.join(d, "fable_independent_2026")):
            return d
        d = os.path.dirname(d)
    return None

class Tee:
    def __init__(self, path): self.f = open(path, "w"); self.s = sys.__stdout__
    def write(self, t):
        self.s.write(t); self.f.write(t)
    def flush(self): self.s.flush(); self.f.flush()

class Run:
    """name = script stem; MUTATE env selects the control; outputs named by mode."""
    def __init__(self, stem, mutate_ok):
        self.mut = os.environ.get("MUTATE", "")
        self.mut = self.mut if self.mut in mutate_ok else ""
        suffix = f"_MUTATE{self.mut}" if self.mut else ""
        self.base = os.path.join(HERE, f"{stem}{suffix}")
        sys.stdout = Tee(self.base + ".out")
        self.out = {"mutate": self.mut or None, "checks": {}, "numbers": {}}
        self.CH = []
        print(f"{stem}  mutate={self.mut or 'none'}  repo=<repo>")
    def check(self, name, measured, ok, load_bearing=True, note=""):
        ok = bool(ok); self.CH.append((name, ok, load_bearing))
        self.out["checks"][name] = {"ok": ok, "load_bearing": load_bearing, "measured": str(measured), "note": note}
        print(f"  [{'PASS' if ok else 'FAIL'}]{'' if load_bearing else ' (reported)'} {name}\n         measured: {measured}" + (f"\n         note: {note}" if note else ""))
        return ok
    def num(self, k, v): self.out["numbers"][k] = v
    def finish(self):
        lb_fail = [n for n, ok, lb in self.CH if lb and not ok]
        npass = sum(ok for _, ok, _ in self.CH)
        print(f"\n{npass}/{len(self.CH)} checks pass; load-bearing failures: {lb_fail}")
        json.dump(self.out, open(self.base + "_results.json", "w"), indent=1, default=str)
        if self.mut:
            bit = bool(lb_fail)
            print(f"MUTATE={self.mut}: control {'BITES' if bit else 'DID NOT BITE (a finding)'}; exit {1 if bit else 0}")
            sys.stdout.flush(); sys.exit(1 if bit else 0)
        print("main run: exit", 1 if lb_fail else 0); sys.stdout.flush()
        sys.exit(1 if lb_fail else 0)
