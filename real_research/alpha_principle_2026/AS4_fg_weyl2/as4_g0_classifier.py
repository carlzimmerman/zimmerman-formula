"""AS4 gate G0 (as AS1-AS3) and classifier controls: AS2's CC1-CC5 plus CC6 for the AS4 same-class rule (several admissible roots whose P
all fall in one class -> that class, else NOT DIAGNOSTIC).
Usage: python3 as4_g0_classifier.py [MUTATE_3]   (MUTATE_3 swaps AGREES and NO IMPROVEMENT: the controls must FAIL, exit 1)."""
import sys
sys.dont_write_bytecode = True
import as4_common as A

C1 = A.C1
MODE = sys.argv[1] if len(sys.argv) > 1 else "NORMAL"
if MODE not in ("NORMAL", "MUTATE_3"):
    sys.exit(f"unknown mode {MODE}")
fails = []


def chk(tag, ok, msg):
    print(("  [PASS] " if ok else "  [FAIL] ") + tag + "  " + msg)
    if not ok:
        fails.append(tag)


def select_class(Ps, Pref, labels):
    cls = [A.A2.classify2(p, Pref, labels)[0] for p in Ps]
    return cls[0] if len(set(cls)) == 1 else "NOT DIAGNOSTIC"


print("MODE:", MODE)
b3 = C1.laneB_b3()
P_eh = C1.downstream_P(0.04795)
P_req = C1.downstream_P(0.009805)
chk("G0a", abs(C1.downstream_P(b3.fg) - b3.c5) < 1e-9, "lane B C5 reproduced")
chk("G0b", abs(P_eh / 92.914 - 1) < 1e-4, f"f_g = 0.04795: P = {P_eh:.5f}")
chk("G0c", abs(P_req / 137.036 - 1) < 1e-4, f"f_g = 0.009805: P = {P_req:.5f}")
chk("G0d", abs(C1.downstream_P(b3.f_needed) - b3.c6) < 1e-9, "lane B C6 reproduced")
labels = ("AGREES", "CLOSER", "NO IMPROVEMENT")
if MODE == "MUTATE_3":
    labels = ("NO IMPROVEMENT", "CLOSER", "AGREES")
    print("  MUTATE_3: AGREES <-> NO IMPROVEMENT swapped")
cases = [("CC1", [P_req], None, "AGREES"), ("CC2", [P_eh], P_eh, "NO IMPROVEMENT"), ("CC3", [120.0], 92.914, "CLOSER"),
         ("CC4", [80.0], 92.914, "NO IMPROVEMENT"), ("CC5", [P_eh], None, "NO IMPROVEMENT"),
         ("CC6a", [80.0, 85.0], 92.914, "NO IMPROVEMENT"), ("CC6b", [P_req, 80.0], 92.914, "NOT DIAGNOSTIC")]
for tag, Ps, ref, want in cases:
    got = select_class(Ps, ref, labels)
    chk(tag, got == want, f"P = {[round(p, 5) for p in Ps]}, reference {ref} -> {got} (must be {want})")
print("\nCHECKS FAILED:", fails if fails else "none")
sys.exit(1 if fails else 0)
