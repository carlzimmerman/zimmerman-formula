#!/usr/bin/env python3
"""CFG217 POST HOC (a referee question relayed by the orchestrator, 2026-09-29; written after the frozen numbers were seen; reported only, never a verdict).
Question: is V1's differential factor (the '1.20 / 0.85' of the README) larger than the 'about 0.15 to 0.25 dex between z ~ 0.6 and z ~ 2.5' it is labelled with, and is
the '3.6 sigma' a per-sample CI or a tension against the flat expectation?
What this computes, from the lane's own data and functions (cfg217_attack.py exec'd read-only up to its POST HOC block; MUTATE=1 passes through to the lane's own injection and is checked), on all N galaxies with the
reconstructed M* (the post hoc block's sample):
  (1) for each gas variant Vk the per-galaxy factor (1 + mu')/(1 + mu): the half-median differential the README quoted (median in z <= z_med vs z > z_med), the
      z < 1 vs z > 2 differential (the G5 line), and the ENDPOINT-EQUIVALENT tilt on the chart's own axis: beta from the regression of log10(factor) on
      x = log10((1 + z)/2.5), tilt = beta x log10(3.5/1.6) (the change between z = 0.6 and z = 2.5);
  (2) the pure log-linear tilt that reproduces the variant's flat slope (the 'effective tilt', on the same axis as the chart), and the variant's own z-scores;
  (3) for a PURE tilt t on that axis: the flat slope, its bootstrap sd (2,000 galaxy resamples, seed 217) and the z-score |slope - 0| / sd against the flat expectation
      (0), for t = -0.10 ... -0.40 dex, and the tilt at which the z-score reaches 2, 3 and 3.6.
Definition of the README's '3.6 sigma' (analyse() in cfg217_attack.py): z_vs_flat_true = (observed flat slope - 0) / sd of the slope over 10,000 galaxy resamples of the
SAME sample, i.e. a TENSION AGAINST THE FLAT EXPECTATION using the observed-sample bootstrap sd; it is not a per-sample CI test (the CI excluding 0 is a separate, equivalent
statement).  It does not include mock-to-mock variation beyond the observed sample's own scatter.
Run: python3 campaign_fresh_gravity/CFG217_rc100_attack/cfg217_label_check.py    (RC100_INPUT=corrected for the corrected-input copy)
"""
import os, sys, io, math, contextlib
sys.dont_write_bytecode = True
import numpy as np

LANE = os.path.dirname(os.path.abspath(__file__))
path = os.path.join(LANE, "cfg217_attack.py")
src = open(path).read()
ns = {"__file__": path, "__name__": "cfg217"}
MUT = os.environ.get("MUTATE", "").strip() == "1"                 # the lane's own MUTATE (D x 10^(0.2 (z - z_med))) is passed through to the exec'd setup
with contextlib.redirect_stdout(io.StringIO()):
    exec(compile(src[:src.index('R.banner("POST HOC')], "cfg217", "exec"), ns)
z, gobs0, gbar0, delta_arr, ts, BASE, VAR, logMs, mu0, zmed, N, DLOG, CORR, J216 = (ns[k] for k in ("z", "gobs0", "gbar0", "delta_arr", "ts", "BASE", "VAR", "logMs", "mu0", "zmed", "N", "DLOG", "CORR", "J216"))
out = []


def P(s=""):
    print(s); out.append(s)


P(__doc__.split("Run:")[0].strip())
P(f"\n  input: {'CORRECTED six-field RC100 copy' if CORR else 'the committed RC100 CSV'}; N = {N}; z {z.min():.2f}-{z.max():.2f}; median z {zmed:.2f}; DLOG = log10(3.5/1.6) = {DLOG:.3f}")
x = np.log10((1 + z) / 2.5)
Mfull = 10 ** logMs
rng = np.random.default_rng(217)
NB = 2000
Bq = rng.integers(0, N, size=(NB, N))
i_, j_ = np.triu_indices(N, 1)


def slope_z(zv, dv):
    dx = zv[j_] - zv[i_]
    m = dx != 0
    return float(np.median((dv[j_] - dv[i_])[m] / dx[m]))


def flat_slope_sd(gb):
    Dv = gobs0 / gb
    d = delta_arr(z, Dv, gb, "flat")
    dr = delta_arr(z, Dv, gb, "rival")
    bsf = np.array([slope_z(z[b], d[b]) for b in Bq])
    bsr = np.array([slope_z(z[b], dr[b]) for b in Bq])
    return slope_z(z, d), float(np.std(bsf)), slope_z(z, dr), float(np.std(bsr))


def tilt_gbar(t):
    return gbar0 * 10 ** ((t / DLOG) * x)                       # t = the change in log10 baryon mass between z = 0.6 and z = 2.5


tbl = {}
grid = np.round(np.arange(-0.40, 0.0001, 0.025), 3)
for t in grid:
    sf, sdf, sr, sdr = flat_slope_sd(tilt_gbar(float(t)))
    tbl[float(t)] = (sf, sdf, sr, sdr)
P("\n(3) a PURE log-linear tilt t (dex change of the analysis baryon mass, z = 0.6 -> 2.5; negative = lighter at high z, the direction that helps the rival):")
P("     t (dex)   flat slope   sd(flat)   z_flat = |slope|/sd    rival slope   sd(rival)   z(rival vs 0)")
for t in grid:
    sf, sdf, sr, sdr = tbl[float(t)]
    P(f"     {t:+.3f}     {sf:+.4f}     {sdf:.4f}     {abs(sf) / sdf:5.2f}                {sr:+.4f}     {sdr:.4f}     {abs(sr) / sdr:5.2f}")
ts_ = np.array(sorted(tbl))
zs = np.array([abs(tbl[t][0]) / tbl[t][1] if tbl[t][0] > 0 else -abs(tbl[t][0]) / tbl[t][1] for t in ts_])
cross = {}
for target in (2.0, 3.0, 3.6):
    k = np.flatnonzero((zs[:-1] - target) * (zs[1:] - target) < 0)
    if len(k):
        a = k[-1] if len(k) else 0
        cross[target] = float(ts_[a] + (target - zs[a]) * (ts_[a + 1] - ts_[a]) / (zs[a + 1] - zs[a]))
P("     the flat law's tension against its own expectation (0) reaches: " + "; ".join(f"{k} sigma at t = {v:+.3f} dex" for k, v in cross.items()))

# ---- controls -------------------------------------------------------------------------------------------------------------------------------------------------------------
tt_ = np.array(sorted(tbl)); sl_ = np.array([tbl[t][0] for t in tt_])
fac_c = 10 ** ((-0.200 / DLOG) * x)                                                       # a synthetic variant with a KNOWN endpoint tilt of -0.200 dex
end_c = float(np.polyfit(x, np.log10(fac_c), 1)[0]) * DLOG
sf_c = flat_slope_sd(gbar0 * fac_c)[0]
teff_c = float(np.interp(sf_c, sl_[::-1], tt_[::-1]))
ctl = [("CONTROL A1 a synthetic variant with a known endpoint tilt of -0.200 dex is recovered by the regression", f"{end_c:+.6f}", abs(end_c + 0.200) < 1e-9),
       ("CONTROL A2 the pure-tilt table reproduces that variant's flat slope at t = -0.200 (interpolation tolerance 0.005)", f"{teff_c:+.4f}", abs(teff_c + 0.200) < 0.005)]
if MUT:
    d0 = tbl[0.0][0] - J216["nu_mono|canonical|flat"]["slope"]
    ctl.append(("MUTATE the lane's injected 0.2 (z - z_med) slope moves the zero-tilt flat slope by >= +0.19 (measured against CFG216's unmutated value)", f"{d0:+.4f}", d0 >= 0.19))
P("\nCONTROLS")
allok = True
for name, val, ok in ctl:
    P(f"  {'PASS' if ok else 'FAIL'}  {name}: {val}"); allok &= ok
P("\n(1) and (2) the gas variants (all N galaxies, reconstructed M*):")
P("     variant                              half-median    z<1 vs z>2    endpoint-equivalent   flat slope [sd]    z_flat   rival slope [sd]   z(rival vs 0)   pure-tilt t")
P("                                          differential   differential  tilt (z 0.6->2.5)                                                                     that reproduces the flat slope")
res = {}
for name, f in VAR.items():
    fac = np.array([(1 + f(zz, m, mu)) / (1 + mu) for zz, m, mu in zip(z, Mfull, mu0)])
    lf = np.log10(fac)
    half = math.log10(np.median(fac[z > zmed]) / np.median(fac[z <= zmed]))
    lohi = math.log10(np.median(fac[z > 2.0]) / np.median(fac[z < 1.0])) if (z > 2.0).any() and (z < 1.0).any() else float("nan")
    beta = float(np.polyfit(x, lf, 1)[0])
    endpoint = beta * DLOG
    sf, sdf, sr, sdr = flat_slope_sd(gbar0 * fac)
    # the pure tilt reproducing this flat slope
    tt = np.array(sorted(tbl)); sl = np.array([tbl[t][0] for t in tt])
    teff = float(np.interp(sf, sl[::-1], tt[::-1])) if sl.min() <= sf <= sl.max() else float("nan")
    res[name] = dict(half=half, lohi=lohi, endpoint=endpoint, sf=sf, sdf=sdf, sr=sr, sdr=sdr, teff=teff)
    P(f"     {name[:36]:36s}   {half:+.3f}        {lohi:+.3f}       {endpoint:+.3f}                 {sf:+.3f} [{sdf:.3f}]   {abs(sf) / sdf:5.2f}     {sr:+.3f} [{sdr:.3f}]      {abs(sr) / sdr:5.2f}          {teff:+.3f}")
v1 = res[[k for k in res if k.startswith("V1")][0]]
P(f"\n  V1 in numbers: the README's factor 1.20/0.85 is the ratio of the median factors of the two z halves (median z of the halves {np.median(z[z <= zmed]):.2f} and {np.median(z[z > zmed]):.2f}): "
  f"{v1['half']:+.3f} dex between those medians, {v1['lohi']:+.3f} dex between the z < 1 and z > 2 medians; on the chart's axis (a log-linear tilt in log10 (1 + z), the change between z = 0.6 and z = 2.5) "
  f"its regression tilt is {v1['endpoint']:+.3f} dex and the pure tilt that reproduces its flat slope is {v1['teff']:+.3f} dex.")
P(f"  ratio (regression endpoint tilt) / (half-median differential) = {v1['endpoint'] / v1['half']:.2f}; the same ratio for a pure log-linear tilt is "
  f"{(math.log10((1 + np.median(z[z > zmed])) / 2.5) - math.log10((1 + np.median(z[z <= zmed])) / 2.5)) ** -1 * DLOG:.2f} (the z baselines' ratio: {DLOG:.3f} / "
  f"{math.log10((1 + np.median(z[z > zmed])) / (1 + np.median(z[z <= zmed]))):.3f}).")
open(os.path.join(LANE, "cfg217_label_check" + ("_corrected" if CORR else "") + ("_MUTATE" if MUT else "") + ".out"), "w").write("\n".join(out) + "\n")
sys.exit(0 if allok else 1)
