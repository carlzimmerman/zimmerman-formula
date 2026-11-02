#!/usr/bin/env python3
"""UX5 part 1 grid. python3 ux5_grid.py FOOT [--a15]. All forms, boxes B175, BV, BV2. Checkpoints per cell in cache/; rerun resumes (preemptible). kappa = 1/2 FITTED; not theory closed."""
import itertools, json, sys
from ux5_core import *
foot = sys.argv[1]; ax = 1.5 if "--a15" in sys.argv else 1.0; a0 = A0[foot] * ax; g, Mu = grid(a0); LU = Lapl(g); os.makedirs("cache", exist_ok=True)
HT, HK, FK = (0.25, 0.30, 0.35), (0.72, 0.90, 1.08), (0.12, 0.26, 0.35)
def cells():
    for sb, mbb, rd in itertools.product(L.SIG_B_GRID, L.MBB_GRID, L.RD_GRID):
        yield dict(box="B175", sb=sb, mbb=mbb, rd=rd)
    if ax != 1.0: return
    for sb, mbb, rd, ht, hk, fk in itertools.product(L.SIG_B_GRID, L.MBB_GRID, L.RD_GRID, HT, HK, FK):
        yield dict(box="BV", sb=sb, mbb=mbb, rd=rd, ht=ht, hk=hk, fk=fk)
    for sb, mbb, rd, ht, hk, fk in itertools.product(L.SIG_B_GRID, L.MBB_GRID, [L.RD_GRID[2], L.RD_GRID[3], L.RD_GRID[4]], HT, HK, FK):
        yield dict(box="BV2", sb=sb, mbb=mbb, rd=rd, ht=ht, hk=hk, fk=fk, rdk=2.0)
f = f"cache/{foot}_{ax}.jsonl"; nd = sum(1 for _ in open(f)) if os.path.exists(f) else 0
with open(f, "a") as w:
    for i, c in enumerate(cells()):
        if i < nd: continue
        rhof, ms = rho_struct(c["sb"], c["mbb"], c["rd"], c.get("ht"), c.get("hk"), c.get("fk"), c.get("rdk"))
        o = solve(rhof, a0, g, Mu, LU, "QRA"); o.update(c); o["Mstar"] = ms; o["inp"] = bool(L.RD_TAG[0] <= c["rd"] <= L.RD_TAG[1] and L.MSTAR_TAG[0] <= ms <= L.MSTAR_TAG[1]); w.write(json.dumps(o) + "\n"); w.flush()
