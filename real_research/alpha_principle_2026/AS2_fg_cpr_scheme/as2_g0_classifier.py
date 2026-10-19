"""AS2 gate G0 (as in AS1, lane B's chain by import via as1_common) and the frozen AS2 classifier controls CC1-CC5.
Usage: python3 as2_g0_classifier.py [MUTATE_3]   (MUTATE_3 swaps the AGREES and NO IMPROVEMENT labels: the controls must FAIL, exit 1).
No SM fixed point, f_g or P in the CPR scheme is computed here."""
import sys
sys.dont_write_bytecode = True
import as2_common as A

C1 = A.C1
MODE = sys.argv[1] if len(sys.argv) > 1 else "NORMAL"
if MODE not in ("NORMAL", "MUTATE_3"):
    sys.exit(f"unknown mode {MODE}")
fails = []


def chk(tag, ok, msg):
    print(("  [PASS] " if ok else "  [FAIL] ") + tag + "  " + msg)
    if not ok:
        fails.append(tag)


print("MODE:", MODE)
b3 = C1.laneB_b3()
print("G0  (AS1 definition; lane B b3 executed by import)")
P_exact = C1.downstream_P(b3.fg)
chk("G0a", abs(P_exact - b3.c5) < 1e-9, f"lane B f_g = {b3.fg:.9f}: P = {P_exact:.6f} vs C5 {b3.c5:.6f}")
P_eh = C1.downstream_P(0.04795)
chk("G0b", abs(P_eh / 92.914 - 1) < 1e-4, f"f_g = 0.04795: P = {P_eh:.5f} vs 92.914")
P_req = C1.downstream_P(0.009805)
chk("G0c", abs(P_req / 137.036 - 1) < 1e-4, f"f_g = 0.009805: P = {P_req:.5f} vs 137.036")
chk("G0d", abs(C1.downstream_P(b3.f_needed) - b3.c6) < 1e-9, "lane B C6 reproduced")

labels = ("AGREES", "CLOSER", "NO IMPROVEMENT")
if MODE == "MUTATE_3":
    labels = ("NO IMPROVEMENT", "CLOSER", "AGREES")
    print("  MUTATE_3: AGREES <-> NO IMPROVEMENT swapped")
print("\nClassifier controls (AS2 rule: CLOSER iff |Delta| > 2% and |P - 137.036| < |P_EH - 137.036|; no reference -> 44.12)")
cases = [("CC1", P_req, None, "AGREES", "f_g = 0.009805"),
         ("CC2", P_eh, P_eh, "NO IMPROVEMENT", "P = P(0.04795), reference P_EH = P(0.04795) (equality)"),
         ("CC3", 120.0, 92.914, "CLOSER", "P = 120, reference 92.914"),
         ("CC4", 80.0, 92.914, "NO IMPROVEMENT", "P = 80, reference 92.914"),
         ("CC5", P_eh, None, "NO IMPROVEMENT", "P = P(0.04795), no reference -> 44.12")]
for tag, Pv, ref, want, desc in cases:
    got, dl = A.classify2(Pv, ref, labels)
    chk(tag, got == want, f"{desc}: P = {Pv:.5f}, Delta = {dl:+.4f} -> {got} (must be {want})")
print("\nCHECKS FAILED:", fails if fails else "none")
sys.exit(1 if fails else 0)
