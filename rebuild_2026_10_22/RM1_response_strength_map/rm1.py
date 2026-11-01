#!/usr/bin/env python3
"""RM1 (FROZEN_CRITERIA.md): response strength f by delta on UR2's path, read only. RM1_PART G, I or MUTATE. f, delta FITTED; kappa = 1/2 FITTED, unused; not theory closed."""
import os
P = os.environ.get("RM1_PART", "G"); H = os.path.dirname(os.path.abspath(__file__)); UR2 = os.path.join(os.path.dirname(H), "UR2_response_mass_pinch")
s = open(os.path.join(UR2, "ur2.py")).read().replace("ur2_tail_add.py", "rm1_tail_add.py").replace("ur2_", f"rm1_{P}_").replace('"cache")', f'"cache_{P}")')
s = s.replace('t = open(os.path.join(UR1, "ur1_tail.py"))', 't = open(os.path.join(UR1, "ur1_tail.py"))')
exec(compile(s, __file__, "exec"), {"__file__": __file__, "__name__": "__main__"})
