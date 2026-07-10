#!/usr/bin/env python3
"""Convergence/robustness of w: vary radial resolution NR, angular NT. If w(beta) is stable, the
Method-B result is trustworthy. Also re-print the validation ratio each time."""
import numpy as np, importlib.util
spec=importlib.util.spec_from_file_location("mb","/private/tmp/claude-501/-Users-carlzimmerman-new-physics-zimmerman-formula/bc6058d7-6ce0-4f8c-8635-25bfd772ff6d/scratchpad/vector_elastic_w/methodB_fem.py")
mb=importlib.util.module_from_spec(spec); spec.loader.exec_module(mb)
a0=9.36e-11; gx=2.2; betas=[0.0,0.33,0.6,0.95,2.0]
print(f"{'NR':>6} {'NT':>6} {'valid':>7} | "+"  ".join(f"w({b})" for b in betas[1:]))
for NR,NT in [(500,700),(900,1200),(1300,1600),(900,2000),(1800,1400)]:
    out,sc=mb.solve_modal(a0,gx,betas,NR=NR,NT=NT)
    valid=out[0.0]/sc
    ws=[out[b]/out[0.0] for b in betas[1:]]
    print(f"{NR:>6} {NT:>6} {valid:>7.3f} | "+"  ".join(f"{w:6.4f}" for w in ws))
print("exit 0")
