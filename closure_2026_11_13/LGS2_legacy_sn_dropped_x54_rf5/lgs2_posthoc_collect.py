"""LGS2 POST HOC collector: the frozen collector lgs2_collect.py, unchanged in its rules, applied to the post-hoc RF5 grades
(lgs2_posthoc_rf5_<sample>.json from lgs2_posthoc_rf5_grade.py) and to the post-hoc M-D size control
(lgs2_posthoc_x54_rand197_CD.json). Writes lgs2_posthoc_results.json. Exact substitutions only.
kappa = 1/2 FITTED; not theory closed.
"""
import os

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "lgs2_collect.py")


def sub(text, old, new):
    assert text.count(old) == 1, f"expected exactly one occurrence of: {old!r} (found {text.count(old)})"
    return text.replace(old, new)


t = open(SRC).read()
t = sub(t, 'rr = {s: load(f"lgs2_rf5_{s}.json") for s in ("full", "des_only")}',
        'rr = {s: load(f"lgs2_posthoc_rf5_{s}.json") for s in ("full", "des_only")}')
t = sub(t, 'runs = {s: load(f"lgs2_x54_{s}.json") for s in ("full", "des_only", "rand197")}',
        'runs = {s: load(f"lgs2_x54_{s}.json" if s != "rand197" else "lgs2_posthoc_x54_rand197_CD.json") for s in ("full", "des_only", "rand197")}')
t = sub(t, 'open(os.path.join(HERE, "lgs2_results.json"), "w")', 'open(os.path.join(HERE, "lgs2_posthoc_results.json"), "w")')
exec(compile(t, SRC, "exec"), {"__name__": "__main__", "__file__": SRC})
