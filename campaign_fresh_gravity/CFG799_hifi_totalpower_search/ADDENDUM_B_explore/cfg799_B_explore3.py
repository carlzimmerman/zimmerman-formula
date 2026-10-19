"""CFG799 ADDENDUM B, EXPLORATORY decomposition part 3: is the H-polarisation excess near 541.700 GHz one bump of a ripple?
Sets no class; changes no frozen rule.  Imports the unchanged ../ADDENDUM_B_full90/cfg799.py (sha256 7486117b...a81488).

Run:  python3 -I cfg799_B_explore3.py <data_dir> <out_dir>

Reason.  Part 2 (E7) found the nu_2 excess in H polarisation spread across all IF terciles, three of four sub-bands and all
epoch terciles, so it is not tied to an IF range.  A fixed-RF feature that is broad and polarisation dependent is what an
optical standing wave would give.  A standing wave repeats with a period c/(2L) in RF, so a second look at the same stack
over a wider RF range can show whether the +34..+40 MHz bump is one of a series.

DECLARED LIST (fixed before the first run; everything is reported):
  K1  reproduce B1.
  E9  total-power stack z(delta) for H only and for V only, delta = -60...+60 MHz about nu_t in 1 MHz steps (121 steps; the
      fit windows near the ends can be cut by the sub-band edge, which the frozen code allows).  Report:
        (a) the steps with |z| >= 3 for each polarisation;
        (b) the autocorrelation of z(delta) at lags 1 to 60 MHz and the lag of the largest positive value beyond 5 MHz;
        (c) the periodogram of z(delta) over periods 8 to 60 MHz, the strongest period, and its p-value against 2000
            phase-randomised surrogates of the same z(delta) (same amplitude spectrum, random phases; the statistic is the
            largest periodogram peak over the period range, so the look-elsewhere over periods is included).
      Both polarisations get the same treatment.  One run, no variants.
"""
import importlib.util, json, os, sys
import numpy as np

DATA = os.path.abspath(sys.argv[1]); OUTD = os.path.abspath(sys.argv[2])
HERE = os.path.dirname(os.path.abspath(__file__))
sys.argv = ["cfg799.py", DATA]
spec = importlib.util.spec_from_file_location("cfg799", os.path.join(HERE, "..", "ADDENDUM_B_full90", "cfg799.py"))
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
OUT, R = [], {}


def P(s=""):
    print(s, flush=True); OUT.append(str(s))


man, obs = m.load()
spectra = []
for oid, o in obs.items():
    a = m.anchor(o)
    if a["ok"]:
        spectra += m.build_spectra(oid, o, a["tS"])
sp, drops = m.prep(spectra)
st = m.stack(m.amps(sp, m.NU_2)); st_t = m.stack(m.amps(sp, m.NU_T))
P("CFG799 ADDENDUM B exploratory decomposition, part 3 (sets no class)")
P(f"  K1 nu_t a = {st_t['a'] * 1e3:+.3f} mK, nu_2 a = {st['a'] * 1e3:+.3f} mK  "
  f"{'REPRODUCES B1' if abs(st_t['a'] + 6.577e-3) < 1e-5 and abs(st['a'] - 15.343e-3) < 1e-5 else 'DOES NOT REPRODUCE'}")
assert abs(st_t["a"] + 6.577e-3) < 1e-5 and abs(st["a"] - 15.343e-3) < 1e-5

deltas = np.arange(-60, 60.01, 1.0)
Z = {}
for pol in ("h", "v"):
    spp = [s for s in sp if s["pol"] == pol]
    Z[pol] = np.array([m.stack(m.amps(spp, m.NU_T + d / 1000))["z"] for d in deltas])
R["delta_MHz"] = deltas.tolist(); R["z"] = {k: v.tolist() for k, v in Z.items()}

# (a)
for pol in ("h", "v"):
    z = Z[pol]; big = [(d, v) for d, v in zip(deltas, z) if abs(v) >= 3]
    P(f"\n[{pol.upper()}] mean z {np.nanmean(z):+.2f}, std {np.nanstd(z):.2f}; steps with |z| >= 3: {len(big)}")
    P("   " + ", ".join(f"{d:+.0f}:{v:+.1f}" for d, v in big))


# (b), (c)
def acf(z, maxlag=60):
    z = z - np.nanmean(z); n = len(z); den = np.nansum(z * z)
    return np.array([np.nansum(z[:n - k] * z[k:]) / den for k in range(maxlag + 1)])


def periodogram(z):
    z = np.nan_to_num(z - np.nanmean(z)); n = len(z)
    f = np.fft.rfftfreq(n, d=1.0)[1:]; p = (np.abs(np.fft.rfft(z)) ** 2 / n)[1:]
    return 1.0 / f, p


rng = np.random.default_rng(799)
for pol in ("h", "v"):
    z = Z[pol]; r = acf(z)
    lag = int(np.argmax(r[6:]) + 6)
    P(f"\n[{pol.upper()}] autocorrelation: lag 1 {r[1]:+.2f}, lag 5 {r[5]:+.2f}, lag 10 {r[10]:+.2f}, lag 20 {r[20]:+.2f}, lag 30 {r[30]:+.2f}; "
      f"largest beyond 5 MHz: lag {lag} MHz, r {r[lag]:+.2f}")
    per, pw = periodogram(z); sel = (per >= 8) & (per <= 60)
    k = int(np.argmax(np.where(sel, pw, -1))); obs_peak = pw[k]
    zc = np.nan_to_num(z - np.nanmean(z)); F = np.fft.rfft(zc); amp = np.abs(F)
    peaks = []
    for _ in range(2000):
        ph = rng.uniform(0, 2 * np.pi, len(F)); ph[0] = 0
        if len(zc) % 2 == 0:
            ph[-1] = 0
        zs = np.fft.irfft(amp * np.exp(1j * ph), n=len(zc))
        per_s, pw_s = periodogram(zs); peaks.append(np.max(pw_s[(per_s >= 8) & (per_s <= 60)]))
    pval = float((1 + np.sum(np.array(peaks) >= obs_peak)) / (1 + len(peaks)))
    P(f"[{pol.upper()}] strongest periodogram peak in 8-60 MHz: period {per[k]:.1f} MHz; look-elsewhere-inclusive p vs phase-randomised surrogates {pval:.3f}")
    R[pol] = dict(acf=r.tolist(), best_lag=lag, peak_period=float(per[k]), peak_p=pval)

open(os.path.join(OUTD, "explore3.out"), "w").write("\n".join(OUT) + "\n")
json.dump(R, open(os.path.join(OUTD, "explore3_results.json"), "w"), indent=1, default=str)
