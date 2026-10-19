"""AS1 gate G0 (downstream pipeline, lane B's code by import) and the frozen classifier controls.
Usage: python3 as1_g0_downstream.py [MUTATE_3]
  MUTATE_3 swaps the AGREES and NO IMPROVEMENT labels inside the classifier; the classifier controls must then FAIL (exit 1).
Normal mode exits 0 iff every gating check passes."""
import sys
sys.dont_write_bytecode = True
import as1_common as C

MODE = sys.argv[1] if len(sys.argv) > 1 else "NORMAL"
if MODE not in ("NORMAL", "MUTATE_3"):
    sys.exit(f"unknown mode {MODE}")
fails = []


def chk(tag, ok, msg):
    print(("  [PASS] " if ok else "  [FAIL] ") + tag + "  " + msg)
    if not ok:
        fails.append(tag)


print("MODE:", MODE)
b3 = C.laneB_b3()
print("lane B b3_forced_vs_required.py executed by import (exit 0); its own C5 objects are used, nothing retyped.")
print(f"  lane B internal values: f_g(EH) = {b3.fg!r}, C5 = {b3.c5!r}, f_g(C6) = {b3.f_needed!r}, C6 = {b3.c6!r}")

print("\nG0  downstream pipeline f_g -> g_Y* -> alpha_Y^-1(M_Z) (b3.aY_inv_at) + alpha_2^-1(M_Z) (measured) + 9.106 (measured)")
P_exact = C.downstream_P(b3.fg)
chk("G0a", abs(P_exact - b3.c5) < 1e-9, f"with lane B's own f_g = {b3.fg:.9f}: P = {P_exact:.6f} vs lane B C5 = {b3.c5:.6f} (abs tol 1e-9)")
P_eh = C.downstream_P(C.FG_EH_QUOTED)
chk("G0b", abs(P_eh / 92.914 - 1) < 1e-4, f"f_g = {C.FG_EH_QUOTED}: P = {P_eh:.5f} vs 92.914 (rel {P_eh/92.914-1:+.2e}, tol 1e-4)")
P_req = C.downstream_P(C.FG_REQ_QUOTED)
chk("G0c", abs(P_req / 137.036 - 1) < 1e-4, f"f_g = {C.FG_REQ_QUOTED}: P = {P_req:.5f} vs 137.036 (rel {P_req/137.036-1:+.2e}, tol 1e-4)")
P_c6 = C.downstream_P(b3.f_needed)
chk("G0d", abs(P_c6 - b3.c6) < 1e-9, f"with lane B's C6 f_g = {b3.f_needed:.9f}: P = {P_c6:.9f} vs lane B C6 = {b3.c6:.9f}")

print("\nClassifier controls (always run; not trials).  Threshold for CLOSER vs NO IMPROVEMENT = the frozen EH miss 44.12 (>= rule).")
labels = ("AGREES", "CLOSER", "NO IMPROVEMENT")
if MODE == "MUTATE_3":
    labels = ("NO IMPROVEMENT", "CLOSER", "AGREES")   # AGREES <-> NO IMPROVEMENT swapped
    print("  MUTATE_3: classifier labels AGREES and NO IMPROVEMENT swapped")
cls_req, d_req = C.classify(P_req, C.EH_MISS_QUOTED, labels)
cls_eh, d_eh = C.classify(P_eh, C.EH_MISS_QUOTED, labels)
print(f"    f_g = {C.FG_REQ_QUOTED}: P = {P_req:.5f}, Delta = {d_req:+.3e}, |P-137.036| = {abs(P_req-C.ALPHA_INV0):.5f} -> {cls_req}")
print(f"    f_g = {C.FG_EH_QUOTED}: P = {P_eh:.5f}, Delta = {d_eh:+.3e}, |P-137.036| = {abs(P_eh-C.ALPHA_INV0):.5f} -> {cls_eh}")
chk("CC1", abs(P_req / 137.036 - 1) < 1e-4 and cls_req == "AGREES", "f_g = 0.009805 must give P = 137.036 and AGREES")
chk("CC2", abs(P_eh / 92.914 - 1) < 1e-4 and cls_eh == "NO IMPROVEMENT",
    "f_g = 0.04795 must give P = 92.914 and NO IMPROVEMENT (|P-137.036| >= 44.12)")
# boundary semantics of the >= rule, tested directly on the classifier with a value exactly at the threshold
cls_b, _ = C.classify(C.ALPHA_INV0 - C.EH_MISS_QUOTED, C.EH_MISS_QUOTED, labels)
chk("CC3", cls_b == "NO IMPROVEMENT", f"exact boundary |P-137.036| = 44.12 -> {cls_b} (must be NO IMPROVEMENT by the >= rule)")
cls_c, _ = C.classify(C.ALPHA_INV0 - 30.0, C.EH_MISS_QUOTED, labels)
chk("CC4", cls_c == "CLOSER", f"|P-137.036| = 30 (>2%, <44.12) -> {cls_c} (must be CLOSER)")

print("\nCHECKS FAILED:", fails if fails else "none")
sys.exit(1 if fails else 0)
