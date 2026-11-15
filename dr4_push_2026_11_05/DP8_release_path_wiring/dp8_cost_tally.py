#!/usr/bin/env python3
"""DP8 cost tally: wall time and peak RSS of every stage log (logs/*.time, /usr/bin/time -l), plus the D3 / D5b logs inside the
dry run's own folder. Writes checks/cost_tally.out. Compute is quoted only from this tally. Offline; reads files.
kappa = 1/2 FITTED; footings never pooled; not theory closed.
"""
import sys
sys.dont_write_bytecode = True
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
files = sorted((HERE / "logs").glob("*.time")) + sorted((HERE / "dry_run_dr3").glob("*.time"))
rows, tot = [], 0.0
for f in files:
    t = f.read_text(errors="replace")
    w = re.search(r"^\s*([0-9.]+) real", t, re.M)
    m = re.search(r"^\s*(\d+)\s+maximum resident set size", t, re.M)
    wall = float(w.group(1)) if w else None
    rss = int(m.group(1)) / 1024 ** 3 if m else None
    inner = f.parent.name == "dry_run_dr3"
    if wall is not None and not inner:
        tot += wall
    rows.append((("dry_run_dr3/" if inner else "") + f.stem, wall, rss, inner))
lines = ["DP8 cost tally (from /usr/bin/time -l stage logs; 'inside' = a step within the c3 dry run, already counted in c3_dry_run)",
         f"{'stage':44s} {'wall s':>9s} {'peak RSS GB':>12s}"]
for n, w, r, inner in rows:
    lines.append(f"{n:44s} {('%.1f' % w) if w is not None else '-':>9s} {('%.2f' % r) if r is not None else '-':>12s}" + ("   (inside)" if inner else ""))
pk = max((r for _, _, r, _ in rows if r is not None), default=0.0)
lines.append(f"total wall of the lane's stages (not double-counting the steps inside the dry run): {tot:.0f} s ({tot / 60:.1f} min); largest peak RSS {pk:.2f} GB")
lines.append("kappa = 1/2 FITTED; footings never pooled; not theory closed.")
(HERE / "checks" / "cost_tally.out").write_text("\n".join(lines) + "\n")
print("\n".join(lines))
