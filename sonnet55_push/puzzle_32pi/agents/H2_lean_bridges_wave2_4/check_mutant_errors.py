"""For every MUTATE file: (i) every false variant `M*` (not *_refuted) must contain at least one Lean error INSIDE ITS OWN source lines (so it fails by its own
proof script, not by inheriting a `sorry` from another failing declaration); (ii) every refutation twin `M*_refuted` must contain no error line.
Reads <module>_MUTATE.lean and <module>_MUTATE.out; exit 0 iff all hold."""
import re, sys
mods = ["P1_wall_dS", "P2_sds_surface_gravity", "P3_record_iff", "P4_macdowell_mansouri", "P5_ext_thermo", "P6_dimension",
        "P7_offset_family", "P8_omega_lambda", "PuzzleChain"]
bad = 0; nfalse = 0; ntwin = 0
for m in mods:
    lines = open(m + "_MUTATE.lean", encoding="utf-8").read().splitlines()
    out = open(m + "_MUTATE.out", encoding="utf-8").read().splitlines()
    err_lines = sorted(int(mm.group(1)) for mm in (re.match(r"%s_MUTATE\.lean:(\d+):\d+: error" % re.escape(m), l) for l in out) if mm)
    starts = []                      # (start_line, name)
    for i, l in enumerate(lines, 1):
        mm = re.match(r"theorem\s+(M[0-9][A-Za-z0-9_]*)", l)
        if mm:
            starts.append((i, mm.group(1)))
    # end of a declaration = line before the next top-level `theorem`, `-- M`, `#print` or `end`
    tops = [i for i, l in enumerate(lines, 1) if re.match(r"(theorem |-- M|#print|end |open |import )", l)]
    for (i, name) in starts:
        nxt = min([t for t in tops if t > i] + [len(lines) + 1])
        errs = [e for e in err_lines if i <= e < nxt]
        if name.endswith("_refuted"):
            ntwin += 1
            if errs:
                print("TWIN WITH ERROR:", m, name, errs); bad += 1
        else:
            nfalse += 1
            if not errs:
                print("FALSE VARIANT WITHOUT OWN ERROR:", m, name); bad += 1
print("false variants with an error inside their own lines: %d checked; twins error-free: %d checked; problems: %d" % (nfalse, ntwin, bad))
sys.exit(1 if bad else 0)
