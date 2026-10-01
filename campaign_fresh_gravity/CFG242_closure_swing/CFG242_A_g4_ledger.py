#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
CFG242_A_g4_ledger -- route A (L14a), G4 by inspection (frozen plan section 4.2, gate order 2).

FROZEN (shared G4, verbatim): 'No constant beyond kappa and Omega_c h^2; a0's tie to Lambda is the CFG43 tie (P_cap = (kappa^2/8pi) rho_Lambda c^2) or a stated equivalent.'
FROZEN arm lines: 'G4 ledger by inspection (0.3 h): A1 and A2 PASS iff tau_bar is the tied tau_L and no other constant appears; A3 FAIL (beta = 1).'
Two cells are scored separately because the frozen text leaves one thing open: G4a 'the memory time is tied' and G4b 'no other constant appears'.
G4b exposes a point the frozen file did not fix: the free-energy stiffness eps_c = c theta^T_full of CFG70's F, declared here at CFG70's N6 value 1; by the
frozen constants rule (declared function shapes allowed only where the file names them) a number put in by hand is a constant, so G4b is scored STRICT (FAIL) and
the lenient reading (eps_c a declared normalisation) is reported beside it, not used.
Order: G0 came first for A2/A3 and failed, so A2/A3's G4 is a POST-HOC CONTINUATION; A1 (strict arm, no G0 in the frozen order) is scored here as MAIN.
MUTATE MA4: tau_bar = 1 t_f (free) instead of tau_L -> the G4a cell flips PASS -> FAIL (A2).
"""
import os, sys, math
sys.dont_write_bytecode = True
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import CFG242_common as C
R = C.Run("CFG242_A_g4_ledger")
P = R.P
MUT = R.mutate
P(__doc__.strip())
P(f"\n  tau_L = 1/(kappa sqrt(G rho_Lambda)) = {C.TAU_L_GYR:.2f} Gyr (canonical; rho_Lambda from the tie a0 = kappa c sqrt(G rho_Lambda): {C.RHO_L:.2f} Msun/kpc^3); kappa = 1/2 FITTED")
inv = {
 "A1": ["kappa (fitted)", "Omega_c h^2 (fitted)", "tau_bar free over {0.01, 0.1, 1, 10} t_f (CFG70's grid): NEW untied time scale", "eps_c = 1 declared (not named in the frozen file)",
        "declared shapes: smoothstep on [0,1] (latch source), exponential kernel family, CFG70 target forms"],
 "A2": ["kappa", "Omega_c h^2", f"tau_bar = tau_L = {C.TAU_L_GYR:.1f} Gyr: tied to rho_Lambda and kappa (no new constant)", "eps_c = 1 declared (not named in the frozen file)",
        "declared shapes: smoothstep, exponential kernel, CFG70 target forms, retarded one-step delay of the host mass (A3 only)"],
 "A3": ["as A2", "beta = 1 of the retarded Gauss-law mediator (CFG72: 'beta = 1 is an untied coupling'): NEW constant"],
}
for a, items in inv.items():
    P(f"\n  arm {a}:")
    for it in items:
        P(f"      - {it}")
g4a_A1 = False
g4a_A2 = (MUT != "MA4")
g4b_A1 = False; g4b_A2 = False
g4_A3 = False
lenient_A2 = g4a_A2
R.check("G4a arm A1: the memory time is tied (no)", g4a_A1, "tau_bar is scanned over a grid, not tied", kind="result")
R.check("G4a arm A2: the memory time is tied to tau_L = 1/(kappa sqrt(G rho_Lambda))", g4a_A2, f"{C.TAU_L_GYR:.1f} Gyr" + (" [MA4: tau_bar = 1 t_f]" if MUT == "MA4" else ""), kind="result")
R.check("G4b arm A2: no other constant appears (eps_c = 1 is a number put in by hand; STRICT reading)", g4b_A2, "eps_c untied; the lenient reading (a declared normalisation) would pass", kind="result")
R.check("G4 arm A3: beta = 1 untied", g4_A3, "FAIL by the frozen line", kind="result")
R.verdict("G4 arm A1 (main)", "FAIL", "tau_bar untied (grid); eps_c declared; binding at G4 in the frozen order (G3 strict is evaluated anyway: CFG242_A_g3_exchange.py)")
R.verdict("G4 arm A2 (post-hoc continuation)", "FAIL (strict) / PASS (lenient on eps_c)", "G4a tied PASS; G4b eps_c untied; reported both readings, strict is the verdict")
R.verdict("G4 arm A3 (post-hoc continuation)", "FAIL", "beta = 1 untied (frozen line) plus eps_c")
base = R.main_cells()
if MUT == "MA4":
    R.finish([base.get("G4a arm A2: the memory time is tied to tau_L = 1/(kappa sqrt(G rho_Lambda))") is True and not g4a_A2])
else:
    R.finish()
