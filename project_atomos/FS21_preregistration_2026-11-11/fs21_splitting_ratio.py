#!/usr/bin/env python3
"""FS21 evaluator: reads a data file of variants and applies FS21_FROZEN_CRITERIA.md's reading rule. Nothing is tunable here.

Usage: python3 fs21_splitting_ratio.py <data.json>
Each variant: name, source, ordering ("NO"/"IO"), d21, s21, d3, s3_plus, s3_minus, which ("31" or "32"), rule_variant (bool).
Only rule_variant = true entries enter the claim status; the others are reported.
"""
import json
import math
import os
import sys

Z2 = 32 * math.pi / 3
P_FINAL = 0.004          # sigma_R / R assumed for the final JUNO reading (frozen)


def phi(x):
    return 0.5 * (1 + math.erf(x / math.sqrt(2)))


def label(pull):
    a = abs(pull)
    return "CONSISTENT" if a <= 2 else ("TENSION" if a <= 3 else "EXCLUDED")


def main(path):
    data = json.load(open(path))
    rows, status = [], {}
    for v in data["variants"]:
        s3 = 0.5 * (v["s3_plus"] + v["s3_minus"])
        sign = 1 if v["ordering"] == "NO" else -1
        d31 = v["d3"] if v["which"] == "31" else v["d3"] + sign * v["d21"]
        d32 = d31 - sign * v["d21"]
        frac = math.hypot(s3 / v["d3"], v["s21"] / v["d21"])
        row = dict(name=v["name"], source=v["source"], rule_variant=v["rule_variant"])
        for tag, d in (("C31", d31), ("C32", d32)):
            R = d / v["d21"]
            sR = R * frac
            pull = (R - Z2) / sR
            sf = P_FINAL * Z2
            chance = phi((Z2 + 2 * sf - R) / sR) - phi((Z2 - 2 * sf - R) / sR)
            row[tag] = dict(R=R, sigma=sR, pull=pull, precision=frac, reading=label(pull), decisive=frac <= 0.01,
                            chance_pass_if_unrelated=chance)
        rows.append(row)
    for tag in ("C31", "C32"):
        rv = [r[tag] for r in rows if r["rule_variant"]]
        if all(x["reading"] == "EXCLUDED" for x in rv):
            status[tag] = "KILLED"
        elif all(x["decisive"] and x["reading"] == "CONSISTENT" for x in rv):
            status[tag] = "SURVIVED (DECISIVE)"
        else:
            status[tag] = "OPEN"
    print(f"FS21 reading of {os.path.basename(path)}: Z^2 = {Z2:.6f}")
    for r in rows:
        print(f"  {r['name']}{'' if r['rule_variant'] else ' (reported only)'} [{r['source']}]")
        for tag in ("C31", "C32"):
            x = r[tag]
            print(f"    {tag}: R = {x['R']:.3f} +- {x['sigma']:.3f} ({100*x['precision']:.2f} %), pull {x['pull']:+.2f} -> {x['reading']}"
                  f"{', DECISIVE' if x['decisive'] else ''}; chance of a final pass if unrelated {x['chance_pass_if_unrelated']:.2f}")
    print("  claim status: " + ", ".join(f"{k} {v}" for k, v in status.items()))
    out = os.path.join(os.path.dirname(os.path.abspath(path)), "fs21_reading_" + os.path.splitext(os.path.basename(path))[0] + ".json")
    json.dump(dict(Z2=Z2, rows=rows, status=status, data=data), open(out, "w"), indent=1)


if __name__ == "__main__":
    main(sys.argv[1])
