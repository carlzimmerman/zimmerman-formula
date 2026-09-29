#!/usr/bin/env bash
# Verify the ChainCert library: it builds, no `sorry`, and every theorem depends only on the three standard axioms.
# Usage: ChainCert/verify_chain.sh            (main run: exit 0 iff all pass)
#        MUTATE=1 ChainCert/verify_chain.sh   (control: adds a theorem proved by `sorry`; the check MUST fail, exit 1)
set -u
cd "$(dirname "$0")/.."
STD='\[propext, Classical.choice, Quot.sound\]'
if [ "${MUTATE:-0}" = "1" ]; then
  cat > ChainCert/_Mutate.lean <<'EOM'
import ChainCert.Chain
theorem mutated_claim : (1 : Nat) = 2 := by sorry
#print axioms mutated_claim
#print axioms ChainPremises.btfr_limit_redshift_independent
EOM
  OUT=$(lake env lean ChainCert/_Mutate.lean 2>&1); rm -f ChainCert/_Mutate.lean
else
  lake build ChainCert || { echo "FAIL: build"; exit 1; }
  OUT=$(lake env lean ChainCert/Axioms.lean 2>&1)
fi
N=$(printf '%s\n' "$OUT" | grep -c "depends on axioms")
BAD=$(printf '%s\n' "$OUT" | grep "depends on axioms" | grep -v -E "$STD" | wc -l | tr -d ' ')
SORRY=$(printf '%s\n' "$OUT" | grep -c -E "sorry")
echo "theorems checked: $N; with non-standard axioms: $BAD; sorry mentions: $SORRY"
if [ "$BAD" != "0" ] || [ "$SORRY" != "0" ] || [ "$N" = "0" ]; then echo "VERIFY: FAIL"; exit 1; fi
echo "VERIFY: PASS"
