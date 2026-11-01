#!/usr/bin/env python3
"""UR2's path on NR2 MEDIAN, read only: run_lane(here, prefix, tail, part). kappa = 1/2 FITTED, unused; not theory closed."""
import json, os
def run_lane(here, pfx, tail, part):
    rb = os.path.dirname(here); nr2 = os.path.join(rb, "NR2_low_mass_ng80"); J = json.load(open(os.path.join(nr2, "nr2_results.json")))
    s = open(os.path.join(rb, "UR2_response_mass_pinch", "ur2.py")).read().replace("ur2_tail_add.py", tail).replace("ur2_", f"{pfx}_{part}_").replace('"cache")', f'"cache_{pfx}_{part}")')
    p = "d = d.replace('json.dumps([math.log10(29.26 / E), math.log10(24.34 / E), 0.0])', 'json.dumps([math.log10(%r), math.log10(%r), 0.0])'); d = d.replace('os.path.join(NRD, \"NR1_PRIMARY_cf_table.json\")', %r)\nassert 'NR1_PRIMARY_cf_table' not in d and '29.26 / E' not in d\n" % (J["r10"], J["r11"], repr(os.path.join(nr2, "NR2_MEDIAN_cf_table.json")))
    assert s.count("import re\n") == 1; s = s.replace("import re\n", "import re\n" + p)
    exec(compile(s, os.path.join(here, pfx + ".py"), "exec"), {"__file__": os.path.join(here, pfx + ".py"), "__name__": "__main__"})
