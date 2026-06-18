import numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
plt.rcParams.update({"figure.dpi":150,"savefig.dpi":150,"font.size":11,
    "axes.grid":True,"grid.alpha":0.25,"axes.spines.top":False,"axes.spines.right":False,
    "axes.titlesize":12,"figure.facecolor":"white","axes.facecolor":"white"})
C_FW="#7c3aed"; C_NEWTON="#64748b"; C_MOND="#0891b2"; C_DATA="#dc2626"

# (label, start_year, end_year, role-color, verdict-text)
role_kill=C_DATA; role_dist=C_FW; role_prem=C_MOND; role_theory="#64748b"
items=[
  ("Gaia DR4 — wide binaries",2026.4,2027.2,role_prem,"tests the PREMISE + a$_0$ value"),
  ("DESI DR3 — does DE evolve?",2026.5,2027.5,role_kill,"GATE: opens or closes a$_0$(z)"),
  ("Euclid / Rubin LSST",2027.0,2031.0,role_kill,"independent DE check"),
  ("ELT online — high-z kinematics",2028.5,2034.5,role_dist,"the DISTINCTIVE BTFR-sign test"),
  ("JWST + ALMA deep work",2026.0,2033.0,role_dist,"feeds the high-z BTFR"),
  ("Next-gen DM detectors",2026.0,2032.0,role_theory,"Branch E: rival road"),
  ("Lensing / cluster theory",2026.0,2035.0,role_theory,"waits on a person, not a telescope"),
]
items=items[::-1]
fig, ax = plt.subplots(figsize=(8.6,5.0))
for i,(lab,s,e,c,note) in enumerate(items):
    y=i
    p=FancyBboxPatch((s,y-0.30),e-s,0.60,boxstyle="round,pad=0.02,rounding_size=0.08",
        linewidth=0,facecolor=c,alpha=0.85,zorder=3)
    ax.add_patch(p)
    ax.text(s+0.06,y+0.0,lab,ha="left",va="center",fontsize=8.6,color="white",
        fontweight="bold",zorder=4)
    ax.text(e+0.12,y,note,ha="left",va="center",fontsize=7.7,color="#334155",style="italic")

# Cassini: already in hand
ax.axvspan(2025.6,2025.95,color="#15803d",alpha=0.18)
ax.text(2025.75,len(items)-0.35,"Cassini\nalready\nIN HAND\n(passed)",ha="center",va="top",
    fontsize=7.4,color="#14532d",fontweight="bold")

ax.set_yticks(range(len(items)))
ax.set_yticklabels(["" for _ in items])
ax.set_ylim(-0.7,len(items)-0.3)
ax.set_xlim(2025.5,2037.2)
ax.set_xticks(range(2026,2037,2))
ax.set_xlabel("approximate year of decisive news")
ax.set_title("The watchlist: when each test reports, and what it bears on")
# legend by role color
from matplotlib.patches import Patch
leg=[Patch(facecolor=role_kill,label="can KILL / dissolve (DE + sign)"),
     Patch(facecolor=role_dist,label="the DISTINCTIVE a$_0$(z) test"),
     Patch(facecolor=role_prem,label="tests the PREMISE / a$_0$ value"),
     Patch(facecolor=role_theory,label="theory front / rival road")]
ax.legend(handles=leg,frameon=False,fontsize=8.0,loc="lower right")
ax.text(2037.1,-0.62,"schematic timeline, dates approximate",ha="right",fontsize=6.5,color="#94a3b8")
fig.tight_layout(); fig.savefig("ch32_watchlist_timeline.png", bbox_inches="tight"); print("ok")
