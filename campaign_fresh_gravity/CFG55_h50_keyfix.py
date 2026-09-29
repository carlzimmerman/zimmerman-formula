#!/usr/bin/env python3
"""CFG55 re-run with h50's name-key artefact corrected -- a DISCLOSED, post-hoc variant (reported only; CFG55's committed outputs untouched).

h50 (hunt_2026/h50_gc_dispersions.py) keys its galaxy table NGC{n:04d} ('NGC0720') but takes each GC's galaxy from the catalogue name as
written ('NGC720_...'), so NGC 720 and NGC 821 (133 GC velocities) are skipped silently.  CFG55's SLUGGS-table key has the same
inconsistency ('NGC821').  Found by CFG76's independent re-derivation (276c78784).

This runner applies one-line substitutions IN MEMORY, each asserted to occur exactly once; no file on disk is changed:
  P1  h50:   the GC's galaxy key is zero-padded to NGC{n:04d};
  P2  CFG38: its C1 control compares only the galaxies that have a line in h50's committed output (the two restored ones do not);
  P3  CFG55: the SLUGGS-table key is zero-padded the same way;
  P4  CFG55: its report is renamed, so the outputs are CFG55_sluggs_dynamical_masses_H50KEYFIX.out / _results.json;
  P5  CFG55: the CFG38 source it executes passes through P2.
Expected by construction, not failures of the variant: CFG55's C1 (CFG38's committed 19-galaxy means) and C3 (exactly 16 galaxies).
NGC 720 lies outside ATLAS3D, so the JAM sample gains NGC 821 only (16 -> 17).
Run: python3 campaign_fresh_gravity/CFG55_h50_keyfix.py
"""
import os, sys, builtins

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import CFG4_common as C4


def sub_once(src, old, new, what):
    n = src.count(old)
    assert n == 1, f"{what}: expected exactly one occurrence, found {n}"
    return src.replace(old, new)


P1 = ('key = nm.split("_")[0]',
      'key = nm.split("_")[0]; key = f"NGC{int(key[3:]):04d}" if key[:3] == "NGC" and key[3:].isdigit() else key')
P2 = ('com[r["name"]]) for r in RES50)', 'com[r["name"]]) for r in RES50 if r["name"] in com)')
P3 = ('("NGC" + v["NGC"].strip())', '("NGC" + v["NGC"].strip().zfill(4))')
P4 = ('C.Report("CFG55_sluggs_dynamical_masses", MUTATE)', 'C.Report("CFG55_sluggs_dynamical_masses_H50KEYFIX", MUTATE)')
P5 = ('src = open(os.path.join(HERE, "CFG38_sluggs_massive_passive.py")).read()',
      'src = _PATCH38(open(os.path.join(HERE, "CFG38_sluggs_massive_passive.py")).read())')

_orig_exec_slices = C4.exec_slices


def exec_slices(path, slices, ns=None, name="committed"):
    """C4.exec_slices with P1 applied to h50's source; identical otherwise (same namespace set-up, read-only open, line numbers kept)."""
    if os.path.basename(path) != "h50_gc_dispersions.py":
        return _orig_exec_slices(path, slices, ns, name)
    src = sub_once(builtins.open(path).read(), *P1, "P1 (h50 GC key)")
    ns = {"__file__": path, "__name__": name, "open": C4._ro_open} if ns is None else ns
    ns.setdefault("__file__", path)
    ns.setdefault("__name__", name)
    ns["open"] = C4._ro_open
    with C4.quiet_env() as buf:
        for a, b in slices:
            ia = 0 if a is None else (src.index(a) if isinstance(a, str) else a)
            ib = len(src) if b is None else (src.index(b, ia) if isinstance(b, str) else b)
            exec(compile("\n" * src[:ia].count("\n") + src[ia:ib], path, "exec"), ns)
    return ns, buf.getvalue()


C4.exec_slices = exec_slices

path55 = os.path.join(HERE, "CFG55_sluggs_dynamical_masses.py")
src55 = builtins.open(path55).read()
for (old, new), what in ((P3, "P3 (CFG55 SLUGGS key)"), (P4, "P4 (CFG55 report name)"), (P5, "P5 (CFG55 reads CFG38)")):
    src55 = sub_once(src55, old, new, what)
print("CFG55 with h50's name-key artefact corrected (DISCLOSED post-hoc variant; P1-P5 applied in memory, files on disk unchanged).")
ns = {"__file__": path55, "__name__": "__main__", "_PATCH38": lambda s: sub_once(s, *P2, "P2 (CFG38 C1 lookup)")}
exec(compile(src55, path55, "exec"), ns)
