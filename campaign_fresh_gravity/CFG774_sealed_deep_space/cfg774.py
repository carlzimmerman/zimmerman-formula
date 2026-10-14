"""CFG774 -- sealed deep-space probe prediction (10 AU - 0.1 pc) for the committed stiffened action.

Criteria: FROZEN_CRITERIA.md (committed alone first). Imports CFG770's a_anom/background read-only (exec of its function
definitions only; CFG770's main block is not run).
Run: python3 cfg774.py   (CFG774_MUTATE=1 for the tooth).  Seconds.
"""
import hashlib
import json
import math
import os
import sys

MUT = os.environ.get("CFG774_MUTATE") == "1"
HERE = os.path.dirname(os.path.abspath(__file__))
SUF = "_MUTATE" if MUT else ""
OUTF = open(os.path.join(HERE, f"cfg774{SUF}.out"), "w")


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s)
    OUTF.write(s + "\n")


# --- read-only import of CFG770's definitions (everything above its 'K3 sympy' section)
src = open(os.path.join(HERE, "..", "CFG770_cassini_stiff_action", "cfg770.py")).read()
head = src.split("# ============================================================ K3 sympy linearization")[0]
head = head.replace('OUTF = open(os.path.join(HERE, f"cfg770{SUF}.out"), "w")', "OUTF = None")
ns = {"__file__": os.path.join(HERE, "cfg770_import.py"), "__name__": "cfg770_import"}
os.environ.pop("CFG770_MUTATE", None)
exec(compile(head, "cfg770_head", "exec"), ns)
a_anom, background, GM, AU, PC = ns["a_anom"], ns["background"], ns["GM"], ns["AU"], ns["PC"]
A0 = ns["A0"]

RES = {"lane": "CFG774", "mutate": MUT, "checks": {}, "table": {}}
FAILS = []


def check(name, ok, detail):
    P(f"  [{'PASS' if ok else 'FAIL'}] {name}: {detail}")
    RES["checks"][name] = dict(ok=bool(ok), detail=detail)
    if not ok:
        FAILS.append(name)


P("CFG774  sealed deep-space probe prediction" + ("  [MUTATE]" if MUT else ""))
GE = 2.32e-10
KILL = 1e-13
LST = [1e-4] if MUT else [5.75, 30.0, 100.0, 1000.0]
RS = [10, 30, 100, 300, 1000, 3000, 7000, 2e4, 1e5]

# K2: CFG770 T3 at 1 AU
b = background(GE, A0["canonical"])
k2v = a_anom(AU, 5.75 * PC / math.sqrt(2), b["Apar"], b["Aperp"])
check("K2 CFG770 import", abs(abs(k2v) / 4.2157e-15 - 1) <= 1e-4, f"a(1 AU) = {k2v:.5e} (CFG770 T3 4.2157e-15)")

P("\nF2/F3 dead-check: the simple-mu tail of the Sun's own field at 1 AU")
for f, a0 in A0.items():
    gN = GM / AU ** 2
    g = 0.5 * (gN + math.sqrt(gN ** 2 + 4 * gN * a0))
    P(f"  {f:9s}: tail {g - gN:.4e} m/s^2 = {(g - gN) / 3.66e-14:.0f}x the 1-AU bound -> F3 DEAD, F2 DEAD")

P("\nF1 table: anomalous radial acceleration (negative = sunward), m/s^2")
for f, a0 in A0.items():
    b = background(GE, a0)
    for L in LST:
        Lam = L * PC / math.sqrt(2)
        row = {}
        for r_au in RS + ["0.1pc"]:
            r = 0.1 * PC if r_au == "0.1pc" else r_au * AU
            row[str(r_au)] = float(f"{a_anom(r, Lam, b['Apar'], b['Aperp']):.4e}")
        RES["table"][f"{f}_Lstar_{L:g}"] = row
        P(f"  {f:9s} L* {L:8g} pc: " + "  ".join(f"{k}:{v:.3e}" for k, v in row.items()))
        if not MUT:
            k1 = abs(abs(row["10"]) / (GM / (L * PC) ** 2) - 1)
            if k1 > 1e-3:
                FAILS.append(f"K1 {f} {L}")
if not MUT:
    check("K1 a(r << lambda_e) = GM/L*^2", not any(x.startswith("K1") for x in FAILS), "all 8 rows at 10 AU within 1e-3")
    worst = max(abs(v) for row in RES["table"].values() for k, v in row.items() if k not in ("10", "30", "100", "300"))
    check("F1 below the kill line beyond 1000 AU", worst < KILL, f"max |a| = {worst:.3e} vs kill line {KILL:.0e}")
    blob = json.dumps(RES["table"], sort_keys=True).encode()
    RES["sha256"] = hashlib.sha256(blob).hexdigest()
    P(f"\nSEALED table sha256 = {RES['sha256']}")
else:
    mx = max(abs(v) for row in RES["table"].values() for v in row.values())
    P(f"\nM1 tooth: L* = 1e-4 pc gives max |a| = {mx:.3e} {'> kill line (bites)' if mx > KILL else '(DID NOT BITE)'}")
    FAILS.append("MUTATE (designed)")

json.dump(RES, open(os.path.join(HERE, f"cfg774_results{SUF}.json"), "w"), indent=1)
P("\nFAILS:", FAILS if FAILS else "none")
OUTF.close()
sys.exit(1 if FAILS else 0)
