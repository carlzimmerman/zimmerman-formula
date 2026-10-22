#!/usr/bin/env python3
"""Every number in report.md / VERDICT.md / MUTATE.md must appear literally in a85.out
   (or, for mutation figures, in the corresponding a85_MUTATE_*.out)."""
import re
from collections import Counter

MUTS = ["newton_jeans", "wrong_aperture_radius", "corrupt_virial", "shift_anisotropy",
        "invert_b_lens", "tophat_psf", "deproj_bad", "beta_sign"]
base = open("a85.out").read()
muts = "".join(open("a85_MUTATE_%s.out" % m).read() for m in MUTS)
ok = True
for f, pool in (("report.md", base), ("VERDICT.md", base), ("MUTATE.md", base + muts)):
    toks = re.findall(r'(?<![\w.])[-+]?\d+(?:\.\d+)?(?:[eE][-+]?\d+)?', open(f).read())
    miss = Counter(t for t in toks if t not in pool)
    print("%-12s tokens %4d  unique %3d  missing %2d  %s"
          % (f, len(toks), len(set(toks)), len(miss), dict(miss) if miss else ""))
    ok = ok and not miss
print("ALL NUMBERS VERIFIED" if ok else "MISSING NUMBERS")
raise SystemExit(0 if ok else 1)
