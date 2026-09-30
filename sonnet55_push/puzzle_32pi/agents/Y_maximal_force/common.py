"""Shared helpers for lane Y (maximal force / dS C-metric): predeclaration-hash check and check ledger."""
import hashlib
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))


def hash_status():
    exp = open(os.path.join(HERE, "PREDECLARED.sha256")).read().strip()
    got = hashlib.sha256(open(os.path.join(HERE, "PREDECLARED.md"), "rb").read()).hexdigest()
    return exp, got, exp == got


class Ledger:
    def __init__(self, name):
        self.name = name
        self.res = []
        exp, got, ok = hash_status()
        print(f"[{name}] PREDECLARED.md sha256 = {got}  ({'matches the stored hash' if ok else 'MISMATCH with stored hash'})")
        self.check("pre-declared file unchanged since it was hashed", ok)

    def check(self, label, cond):
        self.res.append(bool(cond))
        print(f"  [{'OK' if cond else 'FAIL'}] {label}")

    def must_fail(self, label, cond):
        """control: the WRONG statement must be detected as false"""
        self.res.append(not bool(cond))
        print(f"  [{'OK' if not cond else 'FAIL'}] CONTROL (wrong claim must be rejected): {label}")

    def finish(self):
        n, k = len(self.res), sum(self.res)
        print(f"\nRESULT {self.name}: {k}/{n} checks pass" + ("" if k == n else "  <-- FAILURES"))
        sys.exit(0 if k == n else 1)
