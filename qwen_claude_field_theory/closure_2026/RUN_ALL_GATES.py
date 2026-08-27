#!/usr/bin/env python3
"""RUN_ALL_GATES.py — one command reproducing every implemented calculation behind
FINAL_STATUS.md (referee-to-closure audit, 2026-08-27). Prints PASS/FAIL/OPEN per gate.
NOTE: a script exiting 0 means its internal checks passed; the LEDGER records what each
gate *established* (several gates PASS as computations while establishing a physics FAIL)."""
import subprocess, sys, os
R = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
GATES = [
    # (label, path, physics-verdict recorded in CLOSURE_LEDGER.md)
    ("G01-12 MMG suite",        "openai_push/final_closure/run_all.sh",                              "PASS (generic branch)"),
    ("G13 kernel swap",         "openai_push/final_closure/scripts/13_kernel_swap_ellipticity.py",   "PASS"),
    ("A1 Dirac+branch proofs",  "qwen_claude_field_theory/closure_2026/gate_dirac_branch_proofs.py", "PASS"),
    ("A2 k=0/y=0 sectors",      "qwen_claude_field_theory/closure_2026/sf54_mmg_k0_zero_mode_sector_2026.py",      "PASS"),
    ("A2b y=0 sector",          "qwen_claude_field_theory/closure_2026/sf55_mmg_y0_degenerate_branch_2026.py",      "PASS"),
    ("A3 matter conservation",  "openai_push/final_closure/gate_matter_conservation_derivation.py", "FAIL (Newtonian-order violation)"),
    ("A4 PPN",                  "openai_push/final_closure/scripts/ppn_mmg_gate_2026.py",            "FAIL (gamma=0, alpha_1=+4, alpha_3=-1)"),
    ("A5 lensing",              "openai_push/final_closure/gate_lensing_weakfield_derivation.py",    "FAIL (Phi=0, half-light)"),
    ("A6 FLRW+perturbations",   "openai_push/final_closure/scripts/14_flrw_perturbations.py",        "OPEN/FAIL (linear scalar sector empty)"),
    ("A7 spherical+EFE",        "openai_push/final_closure/gate_spherical_efe_2026.py",  "PASS (exact AQUAL, derived EFE)"),
    ("sf40 F(A^2) no-go",       "qwen_claude_field_theory/closure_2026/sf40_general_F_hessian_nogo_2026.py", "PASS (no-go proved)"),
    ("sf42 aux-Legendre 0-DOF", "qwen_claude_field_theory/closure_2026/sf42_aux_legendre_dof_2026.py",       "PASS"),
    ("sf50 DW phase space",     "qwen_claude_field_theory/closure_2026/sf50_dw_full_dof_retarded_phasespace_2026.py", "DW branch: B (rejected)"),
]
fails = []
for label, path, verdict in GATES:
    p = os.path.join(R, path)
    if not os.path.exists(p):
        print(f"  [OPEN] {label:26} — missing: {path}"); fails.append(label); continue
    cmd = ["bash", p] if path.endswith(".sh") else [sys.executable, p]
    r = subprocess.run(cmd, capture_output=True, timeout=1200, cwd=os.path.dirname(p))
    ok = r.returncode == 0
    print(f"  [{'ok' if ok else 'RED'}] {label:26} — ledger: {verdict}")
    if not ok: fails.append(label)
print("\n" + ("ALL GATE SCRIPTS GREEN — physics verdicts per CLOSURE_LEDGER.md (overall: FAILED)"
      if not fails else f"RED/missing: {fails}"))
sys.exit(1 if fails else 0)
