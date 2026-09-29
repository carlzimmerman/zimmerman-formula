#!/usr/bin/env python3
"""CFG162 -- KURVS a0(z) as a function of the outer pressure-support strength: the crossing point, and where the published
prescriptions sit.

Frozen criteria: CFG162_FROZEN_CRITERIA.md (9f098e8a8).  This lane removes the which-calibration choice but adds a placement choice;
the decisive quantities remain the outer pressure support at 2-4.5 R_e and the total cold gas.
  axis        V_c^2 = V_obs^2 + s alpha_K21(x) sigma^2 (CFG160's functions), s in [0, 4].  KURVS with CFG141's sigma_out; SPARC anchor, same s.
  output 1    the decision cell (mu 0.67, delta 0, canonical): Delta'_flat(s), Delta'_H(s); s_mid (flat = -rival), s_f2 (flat = +2 sigma),
              s_h2 (rival = -2 sigma) by root-finding; bootstrap (2000, seed 162) and gas-bracket ranges; full-grid verdict counts.
  output 2    the gas axis at s = 1: Delta'(mu), mu in [0.25, 4]; break-evens by root-finding; only the molecular prior marked.
  placement   s_eq: Delta'_flat(s x K21) = Delta'_flat(prescription) at the decision cell, for none, K21, Price+2022 (n = 1:
              alpha = y K1(y)/K0(y)), Dalcanton & Stilp 2010 (alpha = 0.92 R/R_d), fixed height (P3), self-gravitating (P2).
  C1 (CFG160 rows), C2 (Price alpha), C3 (CFG141's P2 cell); R0 power; H1 [HEADLINE; MUTATE must change it]: s_mid exists in [0, 4].
MUTATE=1: every KURVS v_last x 10^0.3 (inherited from CFG140's exec'd prefix) -- no s_mid in [0, 4], H1 must FAIL (rc = 1).
kappa = 1/2 and Omega_c h^2 stay fitted.  Nothing here says the data favour either model, or that the theory is closed.
Run: python3 campaign_fresh_gravity/CFG162_pressure_axis.py   (MUTATE=1 for the control)
"""
import os, sys, io, math, json, contextlib
import numpy as np
from scipy.optimize import brentq
from scipy.special import k0e, k1e

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import CFG7_common as C

MUTATE = os.environ.get("MUTATE", "0") == "1"
R = C.Report("CFG162_pressure_axis", MUTATE)
P, check = R.P, R.check
P(__doc__.split("Run: python3")[0].strip())
if MUTATE:
    P("\n  *** MUTATE=1: every KURVS v_last x 10^0.3 (g_obs x 4) -- H1 must FAIL ***")

F141 = os.path.join(HERE, "CFG141_kurvs_measured_sigma.py")
src = open(F141).read()
g141 = {"__file__": F141, "__name__": "cfg141"}
with contextlib.redirect_stdout(io.StringIO()):                 # MUTATE inherited on purpose: it is this lane's declared MUTATE
    exec(compile(src[:src.index("# ================================================================== C1 / C2")], "CFG141", "exec"), g141)
KU2, SP, A0, E = g141["KU2"], g141["SP"], g141["A0"], g141["E"]
gbar, gpred, slope, KPC = g141["gbar"], g141["gpred"], g141["slope"], g141["KPC"]
score, score3, MUS, DELS, FOOTS = g141["score"], g141["score3"], g141["MUS"], g141["DELS"], g141["FOOTS"]
LN10 = math.log(10)


def alpha_k21(x):                                                # CFG160's, verbatim
    x = min(max(x, 0.0), 4.0)
    return -0.146 * x * x + 1.204 * x + 1.475


def a_k21(o):
    return alpha_k21(o["R"] / (1.68 * o["Rd"]) - 1.0)


def a_price(o):                                                  # Price et al. 2022 eq. 13, n = 1: rho ~ K0(R/R_d)
    y = o["R"] / o["Rd"]
    return y * k1e(y) / k0e(y)


def a_ds10(o):                                                   # Dalcanton & Stilp 2010 eq. 17: P ~ Sigma^0.92
    return 0.92 * o["R"] / o["Rd"]


def a_p2(o):
    return 2.0 * o["R"] / o["Rd"]


class Sample:
    """per-object quantities that do not depend on the pressure correction, for one (mu, delta, footing)"""
    def __init__(self, objs, mu, dlt, foot, measured_gas=False):
        self.n = len(objs)
        self.V = np.array([o["V"] for o in objs]); self.eV = np.array([o["eV"] for o in objs])
        self.sig = np.array([o["sig"] for o in objs]); self.esig = np.array([o["esig"] for o in objs])
        self.R = np.array([o["R"] for o in objs])
        inc = [math.radians(o["inc"]) if np.isfinite(o["inc"]) and o["inc"] > 1 else math.radians(60) for o in objs]
        self.ti = np.array([2 * o["V"] ** 2 * o["einc"] / math.tan(i) for o, i in zip(objs, inc)])
        self.sm = np.array([o["sm"] for o in objs])
        gb = np.array([gbar(o, mu, dlt, measured_gas) for o in objs])
        self.gp, self.sl = {}, {}
        for rv in (False, True):
            a = np.array([A0[foot] * (E(o["z"]) if rv else 1.0) for o in objs])
            self.gp[rv] = np.array([gpred(g, aa) for g, aa in zip(gb, a)])
            self.sl[rv] = np.array([slope(g, aa) for g, aa in zip(gb, a)])
        self.base = {"K21": np.array([a_k21(o) for o in objs]), "Price": np.array([a_price(o) for o in objs]),
                     "DS10": np.array([a_ds10(o) for o in objs]), "P2": np.array([a_p2(o) for o in objs])}

    def DS(self, alpha, rival, idx=None):
        V, eV, sg, es, Rr, ti, sm, gp, sl = self.V, self.eV, self.sig, self.esig, self.R, self.ti, self.sm, self.gp[rival], self.sl[rival]
        if idx is not None:
            V, eV, sg, es, Rr, ti, sm, gp, sl, alpha = (q[idx] for q in (V, eV, sg, es, Rr, ti, sm, gp, sl, alpha))
        vc2 = V ** 2 + alpha * sg ** 2
        go = vc2 * 1e6 / (Rr * KPC)
        dlog = np.sqrt((2 * V * eV) ** 2 + (2 * alpha * sg * es) ** 2 + ti ** 2) / vc2 / LN10
        return np.log10(go / gp), np.hypot(dlog, sl * sm)


def pooled(d, s):                                                # CFG140's, vectorised
    w = 1 / s ** 2
    m = float(np.sum(w * d) / np.sum(w)); e = float(1 / math.sqrt(np.sum(w)))
    chi = float(np.sum(w * (d - m) ** 2)); dof = max(len(d) - 1, 1)
    if chi / dof > 1:
        e *= math.sqrt(chi / dof)
    return m, e


class Cell:
    def __init__(self, mu, dlt, foot):
        self.ku, self.sp = Sample(KU2, mu, dlt, foot), Sample(SP, mu, dlt, foot, measured_gas=True)

    def delta(self, s, rival, kind="K21", idx=None):
        k, ek = pooled(*self.ku.DS(s * self.ku.base[kind], rival, idx))
        a, ea = pooled(*self.sp.DS(s * self.sp.base[kind], rival))
        return k - a, math.hypot(ek, ea)

    def curves(self, s, idx=None):
        f, ef = self.delta(s, False, idx=idx); h, eh = self.delta(s, True, idx=idx)
        return f, ef, h, eh


def root(fun, lo=0.0, hi=4.0, step=0.01):
    grid = np.arange(lo, hi + step / 2, step)
    vals = [fun(x) for x in grid]
    for a, b, fa, fb in zip(grid[:-1], grid[1:], vals[:-1], vals[1:]):
        if fa == 0:
            return float(a)
        if fa * fb < 0:
            return float(brentq(fun, a, b, xtol=1e-10))
    return float("nan")


def crossings(cell, idx=None, hi=4.0):
    s_mid = root(lambda s: sum(cell.curves(s, idx)[q] for q in (0, 2)), hi=hi)
    s_f2 = root(lambda s: (lambda c: c[0] - 2 * c[1])(cell.curves(s, idx)), hi=hi)
    s_h2 = root(lambda s: (lambda c: c[2] + 2 * c[3])(cell.curves(s, idx)), hi=hi)
    return s_mid, s_f2, s_h2


def lean(f, ef, h, eh):
    fw, hw = abs(f) <= 2 * ef, abs(h) <= 2 * eh
    if fw and h < -2 * eh:
        return "lean flat"
    if hw and f > 2 * ef:
        return "lean rival"
    if fw and hw:
        return "both within 2 sigma"
    return "neither"


DEC = Cell(0.67, 0.0, "canonical")

# ================================================================== controls
R.banner("C1 / C2 / C3  CONTROLS")
j160 = json.load(open(os.path.join(HERE, "CFG160_kurvs_kretschmer" + ("_MUTATE" if MUTATE else "") + "_results.json")))["numbers"]["decision_cell"]
c1 = []
for s, key in ((0.6, "alpha x 0.6"), (1.0, "P4 primary"), (1.4, "alpha x 1.4")):
    f, ef, h, eh = DEC.curves(s)
    c1.append((s, round(f, 3) == round(j160[key]["df"], 3) and round(h, 3) == round(j160[key]["dh"], 3), f, j160[key]["df"], h, j160[key]["dh"]))
check("C1 CONTROL: at s = 0.6, 1.0, 1.4 the curve reproduces CFG160's committed decision-cell rows (3-decimal print)" + ("  [MUTATE]" if MUTATE else ""),
      "; ".join(f"s {s}: flat {f:+.4f} ({rf:+.4f}), rival {h:+.4f} ({rh:+.4f})" for s, ok, f, rf, h, rh in c1), all(r[1] for r in c1))
y = 50.0
ap = y * k1e(y) / k0e(y)
hstep = 1e-5
num = -(math.log(k0e(y * (1 + hstep)) * math.exp(-y * (1 + hstep))) - math.log(k0e(y * (1 - hstep)) * math.exp(-y * (1 - hstep)))) / (math.log(1 + hstep) - math.log(1 - hstep))
ok2 = abs(ap - (y + 0.5)) < 1.0 / y and abs(ap - (y + 0.5 + 3 / (8 * y))) < 1e-3 and abs(ap / num - 1) < 1e-8
check("C2 CONTROL: Price alpha(y) = y K1/K0 matches y + 1/2 + O(1/y) at y = 50 (next order to 1e-3) and the numerical -dlnK0/dlny (1e-8)",
      f"alpha(50) = {ap:.6f}; y + 1/2 + 3/(8y) = {y + 0.5 + 3 / (8 * y):.6f}; numerical {num:.8f}", ok2)
c141 = json.load(open(os.path.join(HERE, "CFG141_kurvs_measured_sigma" + ("_MUTATE" if MUTATE else "") + "_results.json")))["numbers"]["P2"]["0.67|0.0|canonical"]
p2f, _ = DEC.delta(1.0, False, kind="P2"); p2h, _ = DEC.delta(1.0, True, kind="P2")
ok3 = abs(p2f - c141["df"]) < 1e-12 and abs(p2h - c141["dh"]) < 1e-12
check("C3 CONTROL: the P2 prescription in the placement code reproduces CFG141's committed P2 decision cell (1e-12)",
      f"flat {p2f:+.6f} ({c141['df']:+.6f}); rival {p2h:+.6f} ({c141['dh']:+.6f})", ok3)

# ================================================================== R0 power (before any curve value)
R.banner("R0  POWER at the decision cell: (Delta'_flat - Delta'_H) / sigma")
pw = {s: (lambda c: (c[0] - c[2]) / max(c[1], c[3]))(DEC.curves(s)) for s in (0.0, 1.0, 2.0, 4.0)}
check("R0 (reported) POWER: separation of the two readings over the larger error, at s = 0, 1, 2, 4",
      ", ".join(f"s {s:.0f}: {v:.2f} sigma" for s, v in pw.items()), True, load_bearing=False)

# ================================================================== output 1: the decision-cell curve and crossings
R.banner("OUTPUT 1  the decision cell (mu 0.67, delta 0, canonical): curves and crossing points")
S_GRID = np.round(np.arange(0.0, 4.0 + 1e-9, 0.01), 2)
curve = [DEC.curves(float(s)) for s in S_GRID]
for s in (0.0, 0.5, 0.6, 0.7, 0.8, 1.0, 1.4, 2.0, 3.0, 4.0):
    f, ef, h, eh = curve[int(round(s * 100))]
    P(f"  s {s:4.2f}: D'_flat {f:+.3f} +- {ef:.3f} ({f / ef:+.1f} sigma);  D'_H {h:+.3f} +- {eh:.3f} ({h / eh:+.1f} sigma);  {lean(f, ef, h, eh)}")
s_mid, s_f2, s_h2 = crossings(DEC)
P(f"  crossings (root-found): s_mid = {s_mid:.4f} (flat preferred below, rival above); s_f2 = {s_f2:.4f} (flat disfavoured above); "
  f"s_h2 = {s_h2:.4f} (rival disfavoured below)")
rng = np.random.default_rng(162)
boot = []
if np.isfinite(s_mid):
    for _ in range(2000):
        idx = rng.integers(0, DEC.ku.n, DEC.ku.n)
        boot.append(root(lambda s: sum(DEC.curves(s, idx)[q] for q in (0, 2)), step=0.05))
boot = np.array(boot)
bfin = boot[np.isfinite(boot)] if boot.size else boot
b16, b84 = (np.percentile(bfin, [16, 84]) if bfin.size else (float("nan"), float("nan")))
P(f"  bootstrap (2000 resamplings of the ten discs, seed 162, SPARC fixed): s_mid 16-84% = [{b16:.3f}, {b84:.3f}]; "
  f"{bfin.size}/{boot.size} resamples have a crossing in [0, 4]")
gas = {}
for mu in (0.25, 0.67, 1.5, 4.0):
    cm, cf, ch = crossings(DEC if mu == 0.67 else Cell(mu, 0.0, "canonical"))
    gas[mu] = dict(s_mid=cm, s_f2=cf, s_h2=ch)
    P(f"  gas bracket mu {mu}: s_mid {cm:.3f}, s_f2 {cf:.3f}, s_h2 {ch:.3f}")
alt = dict(zip(("s_mid", "s_f2", "s_h2"), crossings(Cell(0.67, 0.0, "alt"))))
P(f"  alt footing: s_mid {alt['s_mid']:.3f}, s_f2 {alt['s_f2']:.3f}, s_h2 {alt['s_h2']:.3f}")
check("H1 [HEADLINE] the preference crossing s_mid exists in [0, 4] at the decision cell" + ("  [MUTATE: v x 2]" if MUTATE else ""),
      f"s_mid = {s_mid:.4f}; bootstrap [{b16:.3f}, {b84:.3f}]; gas bracket " + ", ".join(f"mu {m}: {v['s_mid']:.3f}" for m, v in gas.items()),
      bool(np.isfinite(s_mid)))
R.num("output1", dict(curve=[dict(s=float(s), df=c[0], edf=c[1], dh=c[2], edh=c[3]) for s, c in zip(S_GRID, curve)],
                      s_mid=s_mid, s_f2=s_f2, s_h2=s_h2, boot16=float(b16), boot84=float(b84), boot_with_crossing=int(bfin.size),
                      gas_bracket={str(k): v for k, v in gas.items()}, alt=alt))

R.banner("full-grid verdicts against s (24 cells: 4 mu x 3 delta x 2 footings)")
cells = {(mu, dlt, foot): Cell(mu, dlt, foot) for mu in MUS for dlt in DELS for foot in FOOTS}
fg = {}
for s in np.arange(0.0, 4.0 + 1e-9, 0.25):
    cnt = {"lean flat": 0, "lean rival": 0, "both within 2 sigma": 0, "neither": 0}
    for c in cells.values():
        cnt[lean(*c.curves(float(s)))] += 1
    fg[f"{s:.2f}"] = cnt
    P(f"  s {s:4.2f}: " + ", ".join(f"{k} {v}" for k, v in cnt.items()))
R.num("full_grid", fg)

# ================================================================== placement
R.banner("PLACEMENT  published prescriptions on the s-axis (rule frozen before any placement number)")
pres = {}
for name, fn in (("none (P0)", lambda rv: DEC.delta(0.0, rv)), ("Kretschmer+2021", lambda rv: DEC.delta(1.0, rv)),
                 ("Price+2022 (n = 1)", lambda rv: DEC.delta(1.0, rv, kind="Price")), ("Dalcanton & Stilp 2010", lambda rv: DEC.delta(1.0, rv, kind="DS10")),
                 ("fixed height (P3)", None), ("self-gravitating (P2)", lambda rv: DEC.delta(1.0, rv, kind="P2"))):
    if fn is None:
        kf3, ekf3 = score3(KU2, 0.67, 0.0, "canonical"); af3, eaf3 = score3(SP, 0.67, 0.0, "canonical", measured_gas=True)
        kh3, ekh3 = score3(KU2, 0.67, 0.0, "canonical", rival=True); ah3, eah3 = score3(SP, 0.67, 0.0, "canonical", measured_gas=True, rival=True)
        f, ef, h, eh = kf3 - af3, math.hypot(ekf3, eaf3), kh3 - ah3, math.hypot(ekh3, eah3)
    else:
        (f, ef), (h, eh) = fn(False), fn(True)
    s_eq = 0.0 if name.startswith("none") else (1.0 if name.startswith("Kretschmer") else root(lambda s: DEC.delta(s, False)[0] - f, hi=6.0))
    mu_f = root(lambda mu: Cell(mu, 0.0, "canonical").delta(s_eq, False)[0], lo=0.25, hi=4.0, step=0.25) if np.isfinite(s_eq) else float("nan")
    mu_h = root(lambda mu: Cell(mu, 0.0, "canonical").delta(s_eq, True)[0], lo=0.25, hi=4.0, step=0.25) if np.isfinite(s_eq) else float("nan")
    pres[name] = dict(s_eq=s_eq, df=f, edf=ef, dh=h, edh=eh, verdict=lean(f, ef, h, eh), mu_breakeven_flat=mu_f, mu_breakeven_rival=mu_h)
    P(f"  {name:24s}: s_eq {s_eq if np.isfinite(s_eq) else float('nan'):5.2f}{'' if np.isfinite(s_eq) else ' (UNPLACED)'};  own cell: flat {f:+.3f} "
      f"({f / ef:+.1f} sigma), rival {h:+.3f} ({h / eh:+.1f} sigma): {lean(f, ef, h, eh)};  break-even gas: flat {mu_f:.2f}, rival {mu_h:.2f}")
P("  Kretschmer+2021's stated 40% scatter: s in [0.6, 1.4].")
R.num("placement", pres)
side = sorted(set("below" if v["s_eq"] < s_mid else "above" for v in pres.values() if np.isfinite(v["s_eq"]) and not math.isclose(v["s_eq"], 0.0)))
P(f"  placed published prescriptions (excluding 'none') lie {' and '.join(side)} s_mid = {s_mid:.3f}")

# ================================================================== output 2: the gas axis at s = 1
R.banner("OUTPUT 2  the gas axis at s = 1 (delta 0, canonical)")
MU_GRID = np.exp(np.linspace(math.log(0.25), math.log(4.0), 60))
gcurve = []
for mu in MU_GRID:
    c = Cell(float(mu), 0.0, "canonical")
    gcurve.append(c.curves(1.0))
mu_f = root(lambda mu: Cell(mu, 0.0, "canonical").delta(1.0, False)[0], lo=0.25, hi=4.0, step=0.25)
mu_h = root(lambda mu: Cell(mu, 0.0, "canonical").delta(1.0, True)[0], lo=0.25, hi=4.0, step=0.25)
P(f"  break-even total gas at s = 1: flat mu_f = {mu_f:.3f}, rival mu_h = {mu_h:.3f}.  Molecular prior marked: mu_mol = 0.67 (the paper's 40%), "
  f"range 0.67-1.5 (molecular fractions 0.4-0.6); HI unmarked (unmeasured)")
R.num("output2", dict(mu=[float(m) for m in MU_GRID], curve=[dict(df=c[0], edf=c[1], dh=c[2], edh=c[3]) for c in gcurve], mu_f=mu_f, mu_h=mu_h))

# ================================================================== figure (main run only)
if not MUTATE:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    fig, ax = plt.subplots(1, 2, figsize=(12, 4.6))
    cf = np.array(curve)
    for j, lab, col in ((0, "flat a0", "tab:blue"), (2, "rival a0 ~ H(z)", "tab:red")):
        ax[0].plot(S_GRID, cf[:, j], color=col, label=lab); ax[0].fill_between(S_GRID, cf[:, j] - cf[:, j + 1], cf[:, j] + cf[:, j + 1], color=col, alpha=0.15)
    ax[0].axhline(0, color="k", lw=0.8)
    for v, ls in ((s_mid, "-"), (s_f2, "--"), (s_h2, ":")):
        if np.isfinite(v):
            ax[0].axvline(v, color="gray", ls=ls, lw=0.9)
    ax[0].axvspan(0.6, 1.4, color="green", alpha=0.07)
    for name, v in pres.items():
        if np.isfinite(v["s_eq"]):
            ax[0].plot([v["s_eq"]], [-0.45], marker="v", color="k"); ax[0].annotate(name.split(" (")[0], (v["s_eq"], -0.45), rotation=60, fontsize=7,
                                                                                         xytext=(2, 4), textcoords="offset points")
    ax[0].set_xlabel("outer pressure-support strength s (x Kretschmer+2021 alpha)"); ax[0].set_ylabel("Delta' (dex), decision cell mu = 0.67")
    ax[0].set_title(f"s_mid = {s_mid:.2f} (solid), s_f2 = {s_f2:.2f} (dashed), s_h2 = {s_h2:.2f} (dotted)", fontsize=9); ax[0].legend(fontsize=8)
    gc = np.array(gcurve)
    for j, lab, col in ((0, "flat a0", "tab:blue"), (2, "rival a0 ~ H(z)", "tab:red")):
        ax[1].plot(MU_GRID, gc[:, j], color=col, label=lab); ax[1].fill_between(MU_GRID, gc[:, j] - gc[:, j + 1], gc[:, j] + gc[:, j + 1], color=col, alpha=0.15)
    ax[1].axhline(0, color="k", lw=0.8); ax[1].set_xscale("log")
    ax[1].axvspan(0.67, 1.5, color="orange", alpha=0.15, label="molecular prior 0.67-1.5"); ax[1].axvline(0.67, color="orange", lw=1)
    for v in (mu_f, mu_h):
        if np.isfinite(v):
            ax[1].axvline(v, color="gray", ls="--", lw=0.9)
    ax[1].set_xlabel("total cold gas mu = M_gas/M*  (s = 1)"); ax[1].set_ylabel("Delta' (dex), delta 0, canonical")
    ax[1].set_title(f"break-even: flat mu = {mu_f:.2f}, rival mu = {mu_h:.2f} (dashed)", fontsize=9); ax[1].legend(fontsize=8)
    fig.tight_layout(); fig.savefig(os.path.join(HERE, "CFG162_pressure_gas_axes.png"), dpi=130); plt.close(fig)
    P("  wrote CFG162_pressure_gas_axes.png")

reading = (f"a map, not a verdict: at the decision cell flat a0 is preferred for outer pressure support below s_mid = {s_mid:.2f} x Kretschmer's alpha "
           f"(bootstrap [{b16:.2f}, {b84:.2f}]) and the rival above it; the placed prescriptions lie {' and '.join(side)} s_mid; at s = 1 the break-even gas is "
           f"flat {mu_f:.2f}, rival {mu_h:.2f}") if np.isfinite(s_mid) else "no preference crossing in [0, 4]"
R.num("reading", reading)
P(f"\n    READING (declared): {reading}")
nf = R.write()
raise SystemExit(1 if nf else 0)
