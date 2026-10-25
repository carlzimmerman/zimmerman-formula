"""Shared figure style for the Dark River Tavern Menu (one picture per status-board tile). Plot only."""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]          # repository root
IMG = Path(__file__).resolve().parents[1] / "img"

STATUS = {   # board colours, same as make_status_board.py
    "PASS": "#2e8b57", "COND": "#d4a017", "UNDEC": "#5b7db1", "FAIL": "#c0392b", "OPEN": "#8a949e",
}
INK, MUTED, GRID = "#1d2327", "#5f6b73", "#e3e6e8"
DATA, MODEL, BAND = "#26323a", "#c0392b", "#d9dee2"   # measured points / framework prediction / allowed band

plt.rcParams.update({
    "figure.figsize": (8.0, 5.0), "figure.dpi": 150, "font.size": 10.5, "axes.edgecolor": MUTED,
    "axes.labelcolor": INK, "xtick.color": MUTED, "ytick.color": MUTED, "axes.grid": True, "grid.color": GRID,
    "axes.spines.top": False, "axes.spines.right": False, "legend.frameon": False, "font.family": "DejaVu Sans",
})


def finish(fig, slug, status, title, verdict, source):
    """Title strip in the tile's board colour, verdict line, source footer; save img/<slug>.png."""
    fig.subplots_adjust(top=0.80, bottom=0.17)
    fig.text(0.02, 0.955, title, fontsize=14, weight="bold", color=INK, va="top")
    fig.text(0.02, 0.885, verdict, fontsize=10.5, color=STATUS[status], weight="bold", va="top")
    fig.patches.append(matplotlib.patches.Rectangle((0, 0.985), 1, 0.015, transform=fig.transFigure,
                                                    color=STATUS[status], zorder=5))
    fig.text(0.02, 0.02, "source: " + source, fontsize=7.5, color=MUTED, va="bottom", wrap=True)
    IMG.mkdir(parents=True, exist_ok=True)
    fig.savefig(IMG / f"{slug}.png")
    plt.close(fig)
