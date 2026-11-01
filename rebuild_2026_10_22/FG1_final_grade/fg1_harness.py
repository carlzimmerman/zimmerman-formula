#!/usr/bin/env python3
"""FG1 (FROZEN_CRITERIA.md): C3 and C4 on LEE1's harness, read only up to its Part B, as NL1 does. kappa = 1/2 FITTED; T LOCATED; not theory closed.
Run: PYTHONHASHSEED=0 OMP_NUM_THREADS=1 nice -n 15 python3 -I fg1_harness.py"""
import os, sys, json, types
H = os.path.dirname(os.path.abspath(__file__)); RB = os.path.dirname(H); os.chdir(H)
LS = open(os.path.join(RB, "LEE1_look_elsewhere", "lee1.py")).read(); LS = LS[:LS.index("# ================= Part B: 24 seeded draws =================")]; os.environ.pop("LEE1_MUTATE", None)
m = types.ModuleType("lee1_ro"); sys.modules["lee1_ro"] = m; NS = m.__dict__; NS["__file__"] = os.path.join(H, "lee1_ro.py"); exec(compile(LS, os.path.join(RB, "LEE1_look_elsewhere", "lee1.py"), "exec"), NS)
k0 = all(ok for k, ok in NS["checks"] if k.startswith(("K0", "K2a", "K2b"))); L, T = 7.082, 12.3; tag = f"shpS9_L{L}_T{T}"
NS["STAT"].clear(); r, _ = NS["call"](NS["run_x43"], "on", tag + "_B"); fc = NS["call"](NS["run_x53"], "on", tag); fr = NS["call"](NS["run_x53"], "off", tag); C3 = NS["grade"](r, fc, fr, NS["R51"], f"C3 T {T} L {L}")
rl, _ = NS["call"](NS["run_x43"], "law", "a2"); fl = NS["call"](NS["run_x53"], "law", "a2"); fo = NS["call"](NS["run_x53"], "off", "a2"); dl = NS["call"](NS["run_x51"], "law"); C4 = NS["grade"](rl, fl, fo, dl, "C4 law")
json.dump(dict(k0=k0, L=L, T=T, C3=C3, C4=C4, C4_U={f: {t: rl["footings"][f]["sparc"][t]["U_median"] for t in rl["footings"][f]["sparc"]} for f in rl["footings"]}, C4_dwarf_ind={f: dl["footings"][f]["individuals"] for f in dl["footings"]}, C3_dwarf_ind={f: NS["R51"]["footings"][f]["individuals"] for f in NS["R51"]["footings"]}), open("fg1_harness_results.json", "w"), indent=1, default=float); print("FG1 harness done", k0, flush=True)
