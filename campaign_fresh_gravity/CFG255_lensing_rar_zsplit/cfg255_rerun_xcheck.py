#!/usr/bin/env python3
"""CFG255 independent re-run, part 2: a FRESH re-implementation of the measurement side and of the deep-limit forecast (written by the calculations chat; shares no code with cfg255_zsplit.py).

What it does (offline; reads only the arrays cfg255_zsplit.py reads plus that script's own committed results JSONs):
  X1  the class photo-z thirds (the 1/3 and 2/3 quantiles) equal stage A's recorded quantiles;
  X2  the per-class amplitudes A_data (log10 of the pair-weighted K1 ratio, high-z third / low-z third) and their inverse-variance combination equal stage B's to 1e-9;
  X3  the 50-patch jackknife sigma per class and the combined sigma_A equal stage B / stage A's to 1e-6 relative, with the pair weights held fixed (as the script does) AND re-formed in every leave-one-out (a sensitivity);
  X4  the rival's amplitude from the ANALYTIC deep-limit law (a0 ~ E(z): Delta log g_obs = 0.5 log10[E(z_hi)/E(z_lo)] at fixed g_bar in every K1 bin), at the thirds' median and mean z, lies within 0.004 dex of stage A's A_RIVAL;
  X5  the analytic power (gap / sigma_A)^2 x Hartlap lies in [0.10, 0.25] (stage A: 0.14 canonical / 0.17 alt).
X4 and X5 are PLAUSIBILITY BANDS fixed after the first print of the numbers (0.0187 / 0.0204 against 0.0188; 0.151 against 0.14-0.17); they are not a pre-registered test.
MUTATE=1: the high and low thirds swapped in this implementation (X2 must FAIL; X4 also fails, the swap flips the sign of the forecast).  MUTATE=2: the patch labels permuted (X3 must FAIL; X2 also moves,
the combination weights come from the permuted sigmas).  Outputs go to separate files; the two first MUTATE runs crashed in the final bookkeeping (a KeyError: results were keyed by the long check names) and are kept as *_firstrun.out.
Run: python3 campaign_fresh_gravity/CFG255_lensing_rar_zsplit/cfg255_rerun_xcheck.py      (about 30 s)"""
import os, sys, json, math, time
sys.dont_write_bytecode = True
import numpy as np

T0 = time.time()
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
LR = os.path.join(REPO, "real_research", "data", "lensing_rar")
MUT = os.environ.get("MUTATE", "").strip()
SFX = f"_MUTATE{MUT}" if MUT else ""
LOG, RES = [], {}


def P(s=""):
    print(s, flush=True); LOG.append(str(s))


def X(name, ok, detail):
    RES[name.split()[0]] = bool(ok)                                              # keyed by the short id (X1 ... X5)
    P(f"  [{'PASS' if ok else 'FAIL'}] {name}\n         {detail}")


PL = np.load(os.path.join(LR, "cfg110_perlens.npz")); WG, WW, NN = PL["WG"].astype(float), PL["WW"].astype(float), PL["NN"].astype(float)
LN = np.load(os.path.join(LR, "lr_lenses.npz")); z, typ = LN["z"].astype(float), LN["typ"]
patch = np.load(os.path.join(LR, "lr_esd_jackknife.npz"))["patch"].copy()
if MUT == "2":
    patch = np.random.default_rng(1).permutation(patch)
A_ = json.load(open(os.path.join(HERE, "cfg255_stageA_results.json")))["numbers"]
B_ = json.load(open(os.path.join(HERE, "cfg255_stageB_results.json")))["numbers"]
K1 = slice(8, 15); NP = 50
HART = (NP - 14 - 2) / (NP - 1)
E = lambda x: np.sqrt(0.3 * (1 + x) ** 3 + 0.7)
P("CFG255 independent re-run, part 2: a fresh re-implementation of the measurement side and of the deep-limit forecast"
  + (f"   *** MUTATE={MUT}: " + {"1": "the high and low thirds swapped (X2 must FAIL)", "2": "the patch labels permuted (X3 must FAIL)"}[MUT] + " ***" if MUT else ""))
P("inputs: cfg110_perlens.npz (WG, WW, NN), lr_lenses.npz (z, typ), lr_esd_jackknife.npz (patch); compared against the committed cfg255_stageA/B_results.json\n")

res = {}
for c in (0, 1):
    m = typ == c
    q1, q2 = np.quantile(z[m], [1 / 3, 2 / 3])
    hi, lo = m & (z >= q2), m & (z < q1)
    if MUT == "1":
        hi, lo = lo, hi
    nk_fixed = NN[m][:, K1].sum(0)

    def amp(mh, ml, nk):
        eh = WG[mh][:, K1].sum(0) / WW[mh][:, K1].sum(0)
        el = WG[ml][:, K1].sum(0) / WW[ml][:, K1].sum(0)
        return math.log10(np.sum(nk * eh) / np.sum(nk * el))

    a = amp(hi, lo, nk_fixed)
    rf, rl = [], []
    for p in range(NP):
        keep = patch != p
        rf.append(amp(hi & keep, lo & keep, nk_fixed)); rl.append(amp(hi & keep, lo & keep, NN[m & keep][:, K1].sum(0)))
    sd = lambda r: math.sqrt((NP - 1) / NP * float(np.sum((np.array(r) - np.mean(r)) ** 2)))
    res[c] = dict(q1=float(q1), q2=float(q2), a=a, sf=sd(rf), sl=sd(rl), zlo_mean=float(z[lo].mean()), zhi_mean=float(z[hi].mean()),
                  zlo_med=float(np.median(z[lo])), zhi_med=float(np.median(z[hi])), n_lo=int(lo.sum()), n_hi=int(hi.sum()))
    r = res[c]
    P(f"class {c} ({'late' if c == 0 else 'early'}): z cuts {r['q1']:.4f} / {r['q2']:.4f}; N lo {r['n_lo']}, N hi {r['n_hi']}; median z lo {r['zlo_med']:.4f} hi {r['zhi_med']:.4f}; "
      f"mean z lo {r['zlo_mean']:.4f} hi {r['zhi_mean']:.4f}\n         A_data = {a:+.4f} +- {r['sf']:.4f} (weights fixed) / +- {r['sl']:.4f} (weights re-formed per leave-one-out)")

comb = lambda key: (sum(res[c]["a"] / res[c][key] ** 2 for c in (0, 1)) / sum(1 / res[c][key] ** 2 for c in (0, 1)), 1 / math.sqrt(sum(1 / res[c][key] ** 2 for c in (0, 1))))
Af, Sf = comb("sf"); Al, Sl = comb("sl")
P(f"combined: A_data = {Af:+.4f} +- {Sf:.4f} (weights fixed); {Al:+.4f} +- {Sl:.4f} (re-formed)\n")

X("X1 the class photo-z thirds (1/3 and 2/3 quantiles) equal stage A's recorded quantiles to 1e-12" + (" [not affected by MUTATE=1: the swap is after the cuts]" if MUT == "1" else ""),
  all(abs(res[c]["q1"] - A_["quantiles"]["q1"][str(c)]) < 1e-12 and abs(res[c]["q2"] - A_["quantiles"]["q2"][str(c)]) < 1e-12 for c in (0, 1)),
  "; ".join(f"class {c}: {res[c]['q1']:.6f} / {res[c]['q2']:.6f} (recorded {A_['quantiles']['q1'][str(c)]:.6f} / {A_['quantiles']['q2'][str(c)]:.6f})" for c in (0, 1)))
dA = max(abs(res[c]["a"] - B_["A_class"][str(c)][0]) for c in (0, 1)); dAc = abs(Af - B_["A_data"])
X("X2 per-class A_data and the inverse-variance combination equal stage B's to 1e-9", dA < 1e-9 and dAc < 1e-9,
  f"max |dA| per class {dA:.1e}; combined {Af:+.6f} (recorded {B_['A_data']:+.6f}), difference {dAc:.1e}")
ds = max(abs(res[c]["sf"] / B_["A_class"][str(c)][1] - 1) for c in (0, 1)); dS = abs(Sf / A_["sigma_A"] - 1)
X("X3 the jackknife sigma per class and the combined sigma_A equal the recorded values to 1e-6 relative (weights fixed, as the script does)", ds < 1e-6 and dS < 1e-6,
  f"max relative difference per class {ds:.1e}; combined sigma_A {Sf:.6f} (recorded {A_['sigma_A']:.6f}), {dS:.1e}; sensitivity: re-forming the pair weights per leave-one-out gives {Sl:.6f} ({Sl / Sf - 1:+.1e})")
if MUT:
    P("  (MUTATE: X2 / X3 are expected to FAIL as noted in the header; X4 / X5 use only z and the recorded sigma and are unaffected)")

fc = {lab: {c: 0.5 * math.log10(E(res[c][f"zhi_{k}"]) / E(res[c][f"zlo_{k}"])) for c in (0, 1)} for lab, k in (("median z", "med"), ("mean z", "mean"))}
w = {c: 1 / res[c]["sf"] ** 2 for c in (0, 1)}
cf = {lab: sum(w[c] * fc[lab][c] for c in (0, 1)) / sum(w.values()) for lab in fc}
Arival = A_["amp_models"]["RIVAL_canonical"]; Aflat = A_["amp_models"]["FLAT_canonical"]
P("deep-limit forecast of the rival (a0 ~ E(z)):  Delta log g_obs = 0.5 log10[E(z_hi)/E(z_lo)] at fixed g_bar, the same in every deep-regime bin")
for lab in fc:
    P(f"  {lab}: late {fc[lab][0]:+.4f}, early {fc[lab][1]:+.4f}; combined with the data's inverse-variance weights {cf[lab]:+.4f}")
X("X4 the analytic deep-limit rival amplitude (median-z and mean-z versions) lies within 0.004 dex of stage A's A_RIVAL [band fixed after the first print]",
  all(abs(v - Arival) < 0.004 for v in cf.values()),
  f"median z {cf['median z']:+.4f}, mean z {cf['mean z']:+.4f}; stage A A_RIVAL {Arival:+.4f} (A_FLAT {Aflat:+.4f}, gap {Arival - Aflat:+.4f})")
gap = Arival - Aflat; pw = (gap / A_["sigma_A"]) ** 2 * HART
X("X5 the analytic power (gap / sigma_A)^2 x Hartlap lies in [0.10, 0.25] [band fixed after the first print]", 0.10 <= pw <= 0.25,
  f"({gap:+.4f} / {A_['sigma_A']:.4f})^2 x {HART:.3f} = {pw:.3f}; stage A power {A_['power']['canonical']:.2f} canonical / {A_['power']['alt']:.2f} alt (GLS on the 14 bins, so not identical)")
if MUT:
    expect = {"1": ("X2",), "2": ("X3",)}[MUT]
    bit = all(not RES[k] for k in expect)
    P(f"\n[MUTATE CONTROL] {', '.join(expect)} {'FAILED as designed' if bit else 'did NOT fail: the control does not bite'}")
    ok = bit
else:
    ok = all(RES.values())
P(f"\n{sum(RES.values())}/{len(RES)} checks pass" + (f"; MUTATE={MUT} bites: {ok}" if MUT else f" -> {'ALL PASS' if ok else 'FAILURES'}") + f"   ({time.time() - T0:.0f} s)")
open(os.path.join(HERE, f"cfg255_rerun_xcheck{SFX}.out"), "w").write("\n".join(LOG) + "\n")
sys.exit(0 if ok else 1)
