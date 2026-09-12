"""Hermes push harness: checks that cannot be literal True, both a0 footings, the kernel, and the commit guard."""
import subprocess, sys, numpy as np
A0 = {"canonical": 9.3619e-11, "alt": 1.1279e-10}          # m/s^2
KAPPA = 0.5                                                   # fitted, not derived
def nu_rar(x):
    x = np.maximum(np.asarray(x, dtype=float), 1e-300); return 1.0/(1.0 - np.exp(-np.sqrt(x)))
_CH = []
def check(name, ok, detail=""):
    """ok must be a computed bool; a literal True/False is rejected by the guard below (call sites are grepped)."""
    _CH.append(bool(ok)); print(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f"\n           ({detail})" if detail else ""), flush=True)
def summary(tag):
    print(f"\n{tag} COMPLETE: {sum(_CH)}/{len(_CH)} checks PASS."); return sum(_CH), len(_CH)
def commit_guard(paths=("hermes_push",)):
    """No personal data, no absolute machine paths, no literal-True checks."""
    pat = "|".join(["gm" + "ail", "/Us" + "ers/", r"check\([^,]*,\s*True\b"])        # assembled so this file does not match itself
    bad = subprocess.run(["grep", "-rn", "-i", "-E", "--exclude=harness.py", pat, *paths], capture_output=True, text=True).stdout
    if bad.strip(): print("COMMIT GUARD FAILED:\n" + bad); sys.exit(1)
    print("commit guard ok")
if __name__ == "__main__": commit_guard()
