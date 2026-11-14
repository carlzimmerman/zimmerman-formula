"""LGS4 POST HOC collector: the frozen collector's source, executed with three exact text substitutions (the run files
it reads and the two files it writes). The rules, thresholds and reading are the frozen ones, unchanged."""
import os
HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "lgs4_collect.py")
t = open(SRC).read()
def sub(text, old, new):
    assert text.count(old) == 1, f"expected exactly one occurrence of: {old!r} (found {text.count(old)})"
    return text.replace(old, new)
t = sub(t, 'f"lgs4_{sample}_{model}.json"', 'f"lgs4_posthoc_{sample}_{model}.json"')
t = sub(t, '"lgs4_collect.out"', '"lgs4_posthoc_collect.out"')
t = sub(t, '"lgs4_results.json"', '"lgs4_posthoc_results.json"')
exec(compile(t, SRC, "exec"), {"__file__": SRC, "__name__": "__main__"})
