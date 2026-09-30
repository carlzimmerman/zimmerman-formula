#!/usr/bin/env python3
"""CFG216 POST HOC (referee notes of CFG233, c5adc0f82, relayed by the orchestrator 2026-09-30; written after the frozen numbers were seen; reported only, never a verdict).
Checks the referee's items against the lane's own files and functions (cfg216_rc100.py exec'd read-only through its data block and its primary/expected-slope block):
  (1) the README sentence 'the sign of the flat slope is negative in every variant, and the rival's slope excludes 0 in all of them': the committed sensitivity table is parsed
      and each clause is tested per variant;
  (2) C1 ('a synthetic galaxy placed exactly on each law returns delta = 0') computes log10 of a quantity divided by itself, so it cannot fail (its printed value is exactly 0):
      a NON-VACUOUS replacement is run here: synthetic table rows are placed exactly on each law (both kernels, both footings, five z, five g_bar/a0) by solving for the table's OWN
      observables (V_c, R_e, f_DM), written to a CSV in the RC100 six-field format, read by the lane's actual loader code, and delta is evaluated by the lane's actual delta();
      every on-law row must give |delta| < 1e-9, and (sensitivity) the same rows scored under the OTHER law must not (>= 90 % with |delta| > 1e-3);
  (3) the z-scores of the primary block treat each hypothesis' expected slope as a constant (the full-sample value) over the bootstrap: here the expected slope is recomputed on
      every resample (the same 10,000 index sets), and z = (observed - expected) / sd(observed_k - expected_k) is compared with the lane's z for the four (observed law, true law) cells;
  (4) C2 is flagged load_bearing=False in the lane's code (a reported check, it cannot gate a verdict): read from the source.
MUTATE=1 passes through to the lane's injection (D x 10^(0.2 (z - z_med))): the non-vacuous C1 must then FAIL (the injected drift is caught), the observed flat slope must move to
>= +0.15 (the unmutated value is about -0.03), and outputs are named *_MUTATE.  RC100_INPUT=corrected reads the corrected six-field copy.
Run: python3 campaign_fresh_gravity/CFG216_rc100_within_sample/cfg216_referee_checks.py
"""
import os, sys, io, re, csv, math, tempfile, contextlib
sys.dont_write_bytecode = True
import numpy as np

LANE = os.path.dirname(os.path.abspath(__file__))
path = os.path.join(LANE, "cfg216_rc100.py")
src = open(path).read()
MUT = os.environ.get("MUTATE", "").strip() == "1"
CORR = os.environ.get("RC100_INPUT", "").strip() == "corrected"
SFX = ("_corrected" if CORR else "") + ("_MUTATE" if MUT else "")
out = []


def P(s=""):
    print(s); out.append(s)


P(__doc__.split("Run:")[0].strip())
allok = True


def check(name, val, ok):
    global allok
    allok &= bool(ok)
    P(f"  {'PASS' if ok else 'FAIL'}  {name}: {val}")


# ---------------------------------------------------------------- (1) the README sentence, from the committed outputs
P("\n(1) the sentence 'the sign of the flat slope is negative in every variant, and the rival's slope excludes 0 in all of them'")
outtxt = open(os.path.join(LANE, "cfg216_rc100" + ("_corrected" if CORR else "") + ".out")).read()
variants = {}
for lab, pat in (("(a)", r"\(a\) the RC41 subset \(n = (\d+)\).*"), ("(b)", r"\(b\) the other galaxies \(n = (\d+)\).*"), ("(c)", r"\(c\) g_bar < 3 a0 \(n = (\d+)\).*"), ("(d)", r"\(d\) g_bar from the table's M_bar.*\(n = (\d+)\).*")):
    line = re.search(pat, outtxt).group(0)
    fl = re.search(r"flat: median [^;]*?slope ([+-][\d.]+) \[([+-][\d.]+), ([+-][\d.]+)\]", line)
    ri = re.search(r"rival: median [^;]*?slope ([+-][\d.]+) \[([+-][\d.]+), ([+-][\d.]+)\]", line)
    variants[lab] = dict(n=int(re.search(r"n = (\d+)", line).group(1)), flat=tuple(map(float, fl.groups())), rival=tuple(map(float, ri.groups())))
prim = re.search(r"flat \(nu_mono, canonical\): median [^;]*?slope ([+-][\d.]+) \[([+-][\d.]+), ([+-][\d.]+)\]", outtxt)
for lab, v in variants.items():
    fs, fl_, fh = v["flat"]; rs, rl, rh = v["rival"]
    P(f"    {lab} n = {v['n']:3d}: flat slope {fs:+.3f} [{fl_:+.3f}, {fh:+.3f}] -> {'negative' if fs < 0 else 'NOT negative'}; rival slope {rs:+.3f} [{rl:+.3f}, {rh:+.3f}] -> "
      f"{'excludes 0' if rh < 0 or rl > 0 else 'INCLUDES 0'}")
neg_all = all(v["flat"][0] < 0 for v in variants.values()); excl_all = all(v["rival"][2] < 0 or v["rival"][1] > 0 for v in variants.values())
P(f"    -> 'negative in every variant': {'supported' if neg_all else 'NOT supported'}; 'the rival's slope excludes 0 in all of them': {'supported' if excl_all else 'NOT supported'}")
# ---------------------------------------------------------------- data + functions from the lane
_e = os.environ.pop("MUTATE", None)
if _e is not None and MUT:
    os.environ["MUTATE"] = _e
prefix_end = src.index('R.banner("LEVEL in the two z-halves')
# (2) first: the lane's own loader on a synthetic table placed exactly on each law
ns0 = {"__file__": path, "__name__": "cfg216"}
pre = src[:src.index("# ------------------------------------------------------------------------------------------------ data")]
with contextlib.redirect_stdout(io.StringIO()):
    exec(compile(pre, "cfg216_pre", "exec"), ns0)                       # constants, kernels, gbar_of_gobs (no data yet)
A0F, KER, E, nu1, G2SI, K = (ns0[k] for k in ("A0F", "KER", "E", "nu1", "G2SI", "K"))
tags, recs = [], []
RE_KPC = 5.0
for kname, nu in KER.items():
    for foot in A0F:
        for law in ("flat", "rival"):
            for zz in (0.61, 1.0, 1.53, 2.0, 2.52):
                for y in (0.03, 0.3, 1.0, 3.0, 30.0):
                    a0 = A0F[foot] * (E(zz) if law == "rival" else 1.0)
                    nuv = nu1(nu, y)
                    gobs = y * a0 * nuv                                  # g_bar = y a0, g_obs = g_bar nu(y)
                    fd = 1 - 1 / nuv
                    vc = math.sqrt(gobs * RE_KPC / G2SI)                 # km/s (G2SI converts (km/s)^2 / kpc to m/s^2)
                    tags.append((kname, foot, law)); recs.append(dict(name=f"{kname}|{foot}|{law}|z={zz}|y={y}", z=zz, Re_kpc=RE_KPC, Vc_Re_kms=vc, fDM_within_Re=fd,
                                                                      logMbar_Msun=11.0, sigma0_kms=100.0))
with tempfile.NamedTemporaryFile("w", suffix=".csv", delete=False, newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(recs[0])); w.writeheader(); w.writerows(recs)
    SYN = f.name
src_syn = src.replace('raw = list(csv.DictReader(open(RC100_PATH, newline="")))', 'raw = list(csv.DictReader(open(SYNTH_PATH, newline="")))')
assert src_syn != src, "the loader line changed; refusing"
ns1 = {"__file__": path, "__name__": "cfg216", "SYNTH_PATH": SYN}
with contextlib.redirect_stdout(io.StringIO()):
    exec(compile(src_syn[:src_syn.index('R.banner("CONTROLS")')], "cfg216_syn", "exec"), ns1)
os.unlink(SYN)
rows_syn = ns1["rows"]
assert len(rows_syn) == len(recs), f"the loader dropped synthetic rows ({len(rows_syn)} of {len(recs)})"
dmax, other = 0.0, []
for r, (kname, foot, law) in zip(rows_syn, tags):
    nu = KER[kname]
    d_own = ns1["delta"]([r], law, foot, nu)[0]
    d_oth = ns1["delta"]([r], "rival" if law == "flat" else "flat", foot, nu)[0]
    dmax = max(dmax, abs(d_own)); other.append(abs(d_oth))
frac_off = float(np.mean(np.array(other) > 1e-3))
P(f"\n(2) non-vacuous C1: {len(rows_syn)} synthetic table rows placed exactly on a law through V_c, R_e, f_DM (2 kernels x 2 footings x 2 laws x 5 z x 5 g_bar/a0), read by the lane's loader, scored by the lane's delta()")
if not MUT:
    check("C1' every on-law row returns |delta| < 1e-9", f"max |delta| {dmax:.2e}", dmax < 1e-9)
    check("C1'-sensitivity: scored under the OTHER law, >= 90 % of the rows have |delta| > 1e-3 (the control can discriminate)", f"{100 * frac_off:.0f} %", frac_off >= 0.90)
else:
    check("MUTATE: the injected 0.2 (z - z_med) drift makes the non-vacuous C1' FAIL (max |delta| >= 0.15)", f"max |delta| {dmax:.3f}", dmax >= 0.15)
    P(f"      (in the unmutated code the same rows give ~0: the control is only meaningful when it can fail; here it does)")
# ---------------------------------------------------------------- the lane's data block and primary / expected block
with contextlib.redirect_stdout(io.StringIO()):
    ns = {"__file__": path, "__name__": "cfg216"}
    exec(compile(src[:prefix_end], "cfg216", "exec"), ns)
rows, z, delta, ts, boots, K, KER, A0F, E, nu1, gbar_of_gobs, RES, EXP, NBOOT = (ns[k] for k in ("rows", "z", "delta", "ts", "boots", "K", "KER", "A0F", "E", "nu1", "gbar_of_gobs", "RES", "EXP", "NBOOT"))
n = len(rows)
B = boots(n)
i_, j_ = np.triu_indices(n, 1)


def ts_all(dv):
    o = np.empty(NBOOT)
    for k in range(NBOOT):
        xb, yb = z[B[k]], dv[B[k]]
        dx = xb[j_] - xb[i_]
        m = dx != 0
        o[k] = np.median((yb[j_] - yb[i_])[m] / dx[m])
    return o


nu, a0c = K.nu_mono, A0F["canonical"]
obs = {"flat": delta(rows, "flat", "canonical", nu), "rival": delta(rows, "rival", "canonical", nu)}
expd = {}
for truth in ("flat", "rival"):
    dfl, dri = [], []
    for r in rows:
        a0t = a0c * (E(r["z"]) if truth == "rival" else 1.0)
        gt = gbar_of_gobs(r["gobs"], a0t, nu)
        Dt = r["gobs"] / gt
        dfl.append(math.log10(Dt / nu1(nu, gt / a0c))); dri.append(math.log10(Dt / nu1(nu, gt / (a0c * E(r["z"])))))
    expd[truth] = {"flat": np.array(dfl), "rival": np.array(dri)}
P(f"\n(3) z-scores with the expected slope recomputed on every resample (n = {n}, {NBOOT} resamples, the lane's own index sets); nu_mono, canonical")
P("     observed law  true law    observed slope  expected slope   z (lane: constant expected slope)   z (expected recomputed per resample)    sd_obs    sd(obs_k - exp_k)")
zres = {}
for law in ("flat", "rival"):
    ob_k = ts_all(obs[law])
    for truth in ("flat", "rival"):
        ex_k = ts_all(expd[truth][law])
        so, se = ts(z, obs[law]), ts(z, expd[truth][law])
        z_const = (so - se) / np.std(ob_k)
        z_rec = (so - se) / np.std(ob_k - ex_k)
        zres[(law, truth)] = (so, se, z_const, z_rec, float(np.std(ob_k)), float(np.std(ob_k - ex_k)))
        P(f"     delta_{law:5s}    {truth:5s}-true   {so:+.4f}          {se:+.4f}           {z_const:+6.2f}                              {z_rec:+6.2f}                              {np.std(ob_k):.4f}    {np.std(ob_k - ex_k):.4f}")
P("     (a hypothesis' own delta has an expected slope of exactly 0 on every resample, so its two columns agree; the cross cells are the ones the recomputation moves)")
P("     |z| in the four cells, recomputed: " + ", ".join(f"delta_{a} vs {t}-true {abs(v[3]):.2f}" for (a, t), v in zres.items()))
if MUT:
    d_shift = zres[("flat", "flat")][0] - ns["RES"][("nu_mono", "canonical", "flat")]["slope"]
    P(f"      (MUTATE: the observed flat slope in this run is {zres[('flat', 'flat')][0]:+.4f})")
    check("MUTATE: the injected drift moves the observed flat slope to >= +0.15 (the unmutated value is about -0.03)", f"{zres[('flat', 'flat')][0]:+.4f}", zres[("flat", "flat")][0] >= 0.15)
# ---------------------------------------------------------------- (4) C2
P("\n(4) C2 in the lane's code:")
m = re.search(r'check\("C2 .*?load_bearing=(True|False)', src, re.S)
lb = m.group(1) if m else "?"
P(f"     load_bearing={lb} (C2 is printed as '[PASS] (reported)' and cannot gate the lane's verdict); its comparison values come from exec'ing CFG215's code prefix (its RC41 f_DM and g_bar), "
  f"not from an independent re-derivation of CFG215's geometry")
check("C2 is non-load-bearing in the lane's code", f"load_bearing={lb}", lb == "False")
open(os.path.join(LANE, "cfg216_referee_checks" + SFX + ".out"), "w").write("\n".join(out) + "\n")
sys.exit(0 if allok else 1)
