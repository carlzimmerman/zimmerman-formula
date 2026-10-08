"""Plot retained bounded shell results; no new scientific calculation."""
import json
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
base=Path(__file__).resolve().parent
rows=json.loads((base/"run_main_v2/results.json").read_text())["numeric"]
fig,ax=plt.subplots(figsize=(8,4.8),layout="constrained")
for row in rows:
    radius=np.exp(np.array(row["log_r"]))
    ax.plot(radius,row["amplitude"],label="B = "+str(int(row["B"])),linewidth=2)
ax.set_xscale("log")
ax.set_xlabel("Radius / inner shell radius")
ax.set_ylabel("Rescaled spinor amplitude Y")
ax.set_title("Critical response in a finite shell")
ax.text(.5,.96,"Imposed zero endpoints; h = lambda6 = epsilon = 1",transform=ax.transAxes,ha="center",va="top",fontsize=10)
ax.text(.5,.89,"Nonzero-state threshold Bc = %.4f"%rows[0]["threshold"],transform=ax.transAxes,ha="center",va="top",fontsize=10)
ax.set_ylim(-.06,2.1)
ax.grid(alpha=.2)
ax.legend(loc="center right")
fig.savefig(base/"shell_profiles.png",dpi=170)
