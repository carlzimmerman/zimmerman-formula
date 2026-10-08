"""Visualize retained compact-source results only."""
from pathlib import Path
import json
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
base=Path(__file__).resolve().parent
rows=json.loads((base/"run_source_main_v2/results.json").read_text())["numeric"]
fig,ax=plt.subplots(figsize=(8,4.8),layout="constrained")
ax.axvspan(.001,1,color="#dddddd",alpha=.5,label="Baryonic source")
for row in rows:
    ax.plot(row["r"],row["acceleration_ratio"],linewidth=2.4,label="kappa = "+str(row["kappa"]))
ax.axhline(1,color="black",ls="--",lw=1,label="Original P2 law")
ax.set_xscale("log")
ax.set_xlim(.001,10)
ax.set_ylim(0,1.08)
ax.set_xlabel("Radius / source radius")
ax.set_ylabel("Acceleration / P2 acceleration of the same source")
ax.set_title("Finite-source correction in the proposed flux-gradient model")
ax.legend(loc="lower right")
ax.grid(alpha=.2)
fig.savefig(base/"source_matching.png",dpi=170)
