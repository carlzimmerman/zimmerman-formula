#!/usr/bin/env python3
# CFG180 POST-HOC reading of the B block (written after the B run; not frozen): a law with NO break-even (its R undefined,
# e.g. the rival over-predicts KROSS even at mu = 0.01) is counted as disfavoured by both brackets, instead of "n/a = not disfavoured".
import json, os
HERE = os.path.dirname(os.path.abspath(__file__))
j = json.load(open(os.path.join(HERE, "CFG180_attacks_B_results.json")))
lit, nobe = [], []
for vid, rows in j["variants"].items():
    for s, r in rows.items():
        fl = r["flags"]
        lit_both = [l for l in ("flat", "H") if fl[l] and fl[l][0] and fl[l][1]]
        nb_both = [l for l in ("flat", "H") if fl[l] is None or (fl[l][0] and fl[l][1])]
        if len(lit_both) == 1: lit.append((vid, s, lit_both))
        if len(nb_both) == 1: nobe.append((vid, s, nb_both))
print("literal frozen reading: exactly-one combos:", len(lit), lit)
print("no-break-even-counts-as-disfavoured reading: exactly-one combos:", len(nobe), nobe)
