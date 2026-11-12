#!/bin/sh
# FINAL-20 (KAPPA_AUDIT): recompile FINAL-16's Lean file(s).
# (a) the working-tree file at its EXACT committed path
# (b) an axiom probe built from the working-tree source
# (c) an axiom probe built from the HEAD (committed) blob
# No output is filtered, piped through head/tail, or discarded.
set -u
cd /Users/carlzimmerman/new_physics/zimmerman-formula/fable_independent_2026/lean_2026 || exit 9
LEAN_PATH="$(for d in .lake/packages/*/.lake/build/lib/lean; do [ -d "$d" ] && printf '%s:' "$(cd "$d" && pwd)"; done | sed 's/:$//')"
export LEAN_PATH
AUD=/Users/carlzimmerman/new_physics/zimmerman-formula/hy4_preview_push/FINAL-20_kappa_audit

echo "### (a) exact committed path: closure_2026_11_11/FINAL16_kappa_real/FINAL16.lean"
lean /Users/carlzimmerman/new_physics/zimmerman-formula/closure_2026_11_11/FINAL16_kappa_real/FINAL16.lean \
  > "$AUD/compile_FINAL16.out" 2>&1
echo "LEAN_EXIT_a=$?"
echo "--- full contents of compile_FINAL16.out ---"
cat "$AUD/compile_FINAL16.out"
echo "--- end (a) ---"

echo "### (b) axiom probe, working-tree source: probe_ax_FINAL16_wc.lean"
lean "$AUD/probe_ax_FINAL16_wc.lean" > "$AUD/compile_ax_FINAL16_wc.out" 2>&1
echo "LEAN_EXIT_b=$?"
echo "--- full contents of compile_ax_FINAL16_wc.out ---"
cat "$AUD/compile_ax_FINAL16_wc.out"
echo "--- end (b) ---"

echo "### (c) axiom probe, HEAD blob source: probe_ax_FINAL16_head.lean"
lean "$AUD/probe_ax_FINAL16_head.lean" > "$AUD/compile_ax_FINAL16_head.out" 2>&1
echo "LEAN_EXIT_c=$?"
echo "--- full contents of compile_ax_FINAL16_head.out ---"
cat "$AUD/compile_ax_FINAL16_head.out"
echo "--- end (c) ---"

echo "ALL_DONE"
