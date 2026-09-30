#!/usr/bin/env python3
"""CFG218 -- the signal-to-systematic ladder: for each decomposition sample, the rival-vs-flat separation at its own accelerations and redshifts (signal),
the offset its baryon-mass route can produce (systematic), its statistical band, and the calibration precision needed for a 3-sigma-equivalent separation.
Frozen criteria: FROZEN_CRITERIA.md here (1a7550513), committed before any number.  kappa = 1/2 FITTED, NOT DERIVED.
A forecast built on quantities the record already holds: no data are scored against a law and no verdict is given.
Run:  python3 campaign_fresh_gravity/CFG218_signal_vs_systematic/cfg218_ladder.py        (MUTATE=1: E = 1)
"""
import os, sys, io, csv, math, json, re, contextlib
sys.dont_write_bytecode = True
import numpy as np
from scipy.optimize import brentq

LANE = os.path.dirname(os.path.abspath(__file__))
CFG = os.path.dirname(LANE)
REPO = os.path.dirname(CFG)
sys.path.insert(0, CFG)
_mut = os.environ.pop("MUTATE", None)
try:
    import CFG4_common as K
    import CFG7_common as C
finally:
    if _mut is not None:
        os.environ["MUTATE"] = _mut
MODE = (_mut or "").strip()
assert MODE in ("", "0", "1")
MUT = MODE == "1"
R = C.Report("cfg218_ladder", MUT)
P, check = R.P, R.check
P(__doc__.split("Run:")[0].strip())

G2SI = 1e6 / 3.0856775814913673e19
OM = 0.315
A0 = K.A0["canonical"]


def E(zz):
    return 1.0 if MUT else math.sqrt(OM * (1 + zz) ** 3 + 1 - OM)


def nu1(y):
    return float(K.nu_mono(np.array([y]))[0])


def gbar_of_gobs(gobs, a0):
    q = gobs / a0
    return a0 * 10 ** brentq(lambda ly: nu1(10 ** ly) * 10 ** ly - q, -80, 14, xtol=1e-14, rtol=1e-14)


# ------------------------------------------------------------------------------------------------ samples: CFG215's primary series (read-only exec) + RC100
src = open(os.path.join(CFG, "CFG215_decomposition_timeline", "cfg215_timeline.py")).read()
ns = {"__file__": os.path.join(CFG, "CFG215_decomposition_timeline", "cfg215_timeline.py"), "__name__": "cfg215"}
_e = os.environ.pop("MUTATE", None)
with contextlib.redirect_stdout(io.StringIO()):
    exec(compile(src[:src.index("# ------------------------------------------------------------------------------------------------ the two series")], "cfg215", "exec"), ns)
if _e is not None:
    os.environ["MUTATE"] = _e
SAMPLES = {"MUSE-DARK": ns["muse_ind"], "RC41": ns["rc41"], "NOEMA3D": ns["noe_ind"], "CRISTAL": ns["cri_ind"]}
rc = []
for r in csv.DictReader(open(os.path.join(REPO, "real_research", "data", "rc100_nestorshachar2023_table3.csv"), newline="")):
    z, Re, Vc, fd = (float(r[k]) for k in ("z", "Re_kpc", "Vc_Re_kms", "fDM_within_Re"))
    if 0 < fd < 1:
        g = Vc ** 2 / Re * G2SI
        rc.append(dict(z=z, gbar=(1 - fd) * g, D=1 / (1 - fd)))
SAMPLES["RC100"] = rc
J215 = json.load(open(os.path.join(CFG, "CFG215_decomposition_timeline", "cfg215_timeline_results.json")))["numbers"]
J216 = json.load(open(os.path.join(CFG, "CFG216_rc100_within_sample", "cfg216_rc100_results.json")))["numbers"]
J217 = json.load(open(os.path.join(CFG, "CFG217_rc100_attack", "cfg217_attack_results.json")))["numbers"]
BIAS = dict(J215["mock"]["bias"])
BIAS["RC100"] = -float(J217["G2"].get("median_delta_prior", -0.100)) if "median_delta_prior" in J217["G2"] else 0.100     # CFG217 G2: median Delta_prior -0.100 dex
CTX = {"MUSE-DARK": "no SED prior in the DC14 fit; independent route = SED + main-sequence H2", "RC41": "0.2-dex prior on SED + gas", "NOEMA3D": "measured CO gas",
       "CRISTAL": "1-dex prior on the fit; independent route = SED + dust gas", "RC100": "0.2-dex prior on SED + gas (b_s from the RC41 overlap)"}
STAT = {}
for s in ("MUSE-DARK", "RC41", "NOEMA3D", "CRISTAL"):
    t = J215["table"][f"primary|{s}|flat|nu_mono|canonical"]
    STAT[s] = (t["hi"] - t["lo"]) / 2
STAT["RC100"] = (J216["results"]["nu_mono|canonical|flat"]["mhi"] - J216["results"]["nu_mono|canonical|flat"]["mlo"]) / 2

# ------------------------------------------------------------------------------------------------ definitions
def signal(rows):
    return np.array([abs(math.log10(nu1(r["gbar"] / (A0 * E(r["z"]))) / nu1(r["gbar"] / A0))) for r in rows])


def Y(rows, e, cache={}):
    """|median delta_flat| when the analysis baryons are the truth x 10^e (g_obs held fixed; truth = the flat law)"""
    ds = []
    for r in rows:
        key = (id(r), "gt")
        if key not in cache:
            cache[key] = gbar_of_gobs(r["D"] * r["gbar"], A0)
        gt = cache[key]
        ga = gt * 10 ** e
        ds.append(math.log10((r["D"] * r["gbar"] / ga) / nu1(ga / A0)))
    return abs(float(np.median(ds)))


def needed(rows, S):
    """the mass error e > 0 at which Y(e) = S/3 (None if Y stays below S/3 up to 1.5 dex)"""
    if S <= 1e-12:
        return None                  # (added after the MUTATE run crashed: with E = 1 the signal is 0 and no calibration can produce a separation)
    f = lambda e: Y(rows, e) - S / 3
    if f(1.5) < 0:
        return None
    return brentq(f, 1e-6, 1.5, xtol=1e-6)


R.banner("CONTROLS")
z0rows = [dict(z=0.0, gbar=r["gbar"], D=r["D"]) for r in SAMPLES["CRISTAL"]]
c1 = float(np.max(signal(z0rows)))
check("C1 the signal is 0 at z = 0", f"max {c1:.1e}", c1 < 1e-12)
mono = all(Y(SAMPLES["CRISTAL"], e2) >= Y(SAMPLES["CRISTAL"], e1) - 1e-12 for e1, e2 in ((0.0, 0.05), (0.05, 0.1), (0.1, 0.2), (0.2, 0.4)))
check("C2 Y(0) = 0 and Y(e) is monotone in |e|", f"Y(0) = {Y(SAMPLES['CRISTAL'], 0.0):.1e}; Y(0.1) = {Y(SAMPLES['CRISTAL'], 0.1):.3f}", Y(SAMPLES["CRISTAL"], 0.0) < 1e-9 and mono)
if not MUT:
    txt = open(os.path.join(CFG, "CFG213_dysmalpy_two_sided", "cfg213_two_sided.out")).read()
    blk = txt[txt.index("Z5 (CRISTAL primary)"):]
    vals = re.findall(r"D_flat\s+([0-9.]+)\s+D_rival\s+([0-9.]+)", blk)
    printed = float(np.median([abs(math.log10(float(b) / float(a))) for a, b in vals]))
    mine = float(np.median(signal(ns["cri_fit"])))
    check("C3 CRISTAL's signal median (12 fit-route rows) reproduces the separation implied by CFG213's printed D_flat and D_rival (to their 3-decimal rounding, 2e-3)",
          f"{mine:.4f} vs {printed:.4f} from {len(vals)} printed rows", abs(mine - printed) < 2e-3)

# ------------------------------------------------------------------------------------------------ the ladder
R.banner("THE LADDER  (nu_mono, canonical; dex in log D or delta)")
P(f"  {'sample':10s} {'n':>4s} {'z':>5s} {'signal S':>9s} {'stat band':>10s} {'b_s':>7s} {'S_sys=Y(b_s)':>13s} {'e for S/3':>10s}  classification; g_bar/a0 < 3: fraction; lowest quartile S / e needed")
LAD = {}
for s, rows in SAMPLES.items():
    S_i = signal(rows)
    S = float(np.median(S_i))
    sig, b = STAT[s], BIAS[s]
    ys = Y(rows, b)
    e3 = needed(rows, S)
    if ys > S:
        cls = "systematic-limited"
    elif sig > S:
        cls = "statistics-limited"
    elif S > 3 * max(ys, sig / 1.96):
        cls = "discriminating"
    else:
        cls = "marginal"
    gq = np.array([r["gbar"] / A0 for r in rows])
    q = gq <= np.percentile(gq, 25)
    rows_q = [r for r, m in zip(rows, q) if m]
    Sq = float(np.median(signal(rows_q)))
    eq = needed(rows_q, Sq)
    LAD[s] = dict(n=len(rows), z=float(np.median([r["z"] for r in rows])), S=S, stat=sig, b=b, S_sys=ys, e_needed=e3, cls=cls, frac_lt3=float(np.mean(gq < 3)), Sq=Sq, e_q=eq)
    P(f"  {s:10s} {len(rows):4d} {LAD[s]['z']:5.2f} {S:9.3f} {sig:10.3f} {b:+7.3f} {ys:13.3f} {('%.3f' % e3) if e3 is not None else '   n/a':>10s}  {cls}; "
      f"{LAD[s]['frac_lt3']:.2f}; {Sq:.3f} / {('%.3f' % eq) if eq is not None else 'n/a'}")
for s, ctx in CTX.items():
    P(f"    {s}: {ctx}")
P("\n  RC100 differential version (cited from CFG217, not recomputed): the flat slope is exactly zero at -0.075 dex and the rival slope exactly zero at -0.25 dex of "
  "differential baryon-mass change between z 0.6 and 2.5; a 3-sigma-equivalent separation needs the differential calibration known to about +-0.06 dex.")
# POST HOC (written after the frozen numbers were seen; reported only): the sample size at which the statistical band alone would allow a 3-sigma-equivalent
# separation, n_needed = n x (sigma / (1.96 S/3))^2 (never below n), and the figure
P("\n  POST HOC (reported only): n needed for the statistical band alone to reach a 3-sigma-equivalent separation (band <= 1.96 S/3):")
for s_, v in LAD.items():
    lim = 1.96 * v["S"] / 3
    v["n_needed"] = int(math.ceil(v["n"] * max(1.0, (v["stat"] / lim) ** 2))) if lim > 1e-12 else None      # (None when the signal is 0: MUTATE, E = 1)
    P(f"    {s_:10s} now n = {v['n']:3d}, band {v['stat']:.3f} vs {lim:.3f} -> n >= {v['n_needed'] if v['n_needed'] else 'never (signal 0)'}")
R.num("ladder", LAD)
if not MUT:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    names = list(LAD)
    x = np.arange(len(names))
    fig, ax = plt.subplots(figsize=(11.5, 6.4))
    w = 0.26
    ax.bar(x - w, [LAD[n]["S"] for n in names], w, color="#d1541f", label="signal S: rival-vs-flat separation in log D at the sample's own g_bar and z")
    ax.bar(x, [max(LAD[n]["S_sys"], 1e-3) for n in names], w, color="#6a3d9a", label="systematic: δ offset from the sample's baryon-mass route bias b_s")
    ax.bar(x + w, [LAD[n]["stat"] for n in names], w, color="#888888", label="statistical band (half-width of the 95% CI on the median δ)")
    for i, n in enumerate(names):
        ax.text(i, 0.6, LAD[n]["cls"], ha="center", va="top", fontsize=9, color="0.15", fontweight="bold")
        ax.text(i, 0.53, f"n = {LAD[n]['n']}, z ≈ {LAD[n]['z']:.1f}\nb_s = {LAD[n]['b']:+.2f} dex\ncalibration for a 3σ-equivalent\nseparation: ±{LAD[n]['e_needed']:.2f} dex" if LAD[n]["e_needed"] else f"n = {LAD[n]['n']}", ha="center", va="top", fontsize=8, color="0.3")
    ax.set_xticks(x); ax.set_xticklabels(names, fontsize=10)
    ax.set_ylim(0, 0.64); ax.set_ylabel("dex", fontsize=11)
    ax.set_title("signal vs systematic vs statistics, per decomposition sample (ν_mono, canonical; CFG218)\nno sample is 'discriminating'; the calibration needed is 0.02–0.11 dex", fontsize=11.5)
    ax.legend(fontsize=8.6, loc="upper center", bbox_to_anchor=(0.5, 0.60))
    ax.grid(alpha=0.25, axis="y")
    fig.text(0.01, 0.008, "A forecast from quantities already in the record; no data are scored against a law here. κ = ½ fitted.", fontsize=8, color="0.3")
    plt.tight_layout(rect=(0, 0.03, 1, 1))
    plt.savefig(os.path.join(LANE, "cfg218_ladder.png"), dpi=150)
    P("  wrote cfg218_ladder.png")
if MUT:
    R.banner("MUTATE RESPONSE")
    smax = max(v["S"] for v in LAD.values())
    nodisc = all(v["cls"] != "discriminating" for v in LAD.values())
    check("MUTATE: with E = 1 every signal is 0 and no sample is classified 'discriminating'", f"max signal {smax:.1e}; classes {[v['cls'] for v in LAD.values()]}", smax < 1e-12 and nodisc)
R.write(here=LANE)
