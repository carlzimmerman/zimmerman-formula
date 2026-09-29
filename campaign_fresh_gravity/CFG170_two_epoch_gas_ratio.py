#!/usr/bin/env python3
"""CFG170 -- the two-epoch gas-ratio test: the gas evolution each a0 law needs between KROSS (z ~ 0.85) and KURVS (z ~ 1.5).

Frozen criteria: CFG170_FROZEN_CRITERIA.md (1caae1adb).  This lane analyses data already seen (CFG140, 141, 160, 161, 162, 164).
  mu_be       the root in [0.01, 30] of Delta'(mu) = 0 per sample, law and s (CFG160's P4 functions, s x K21 alpha; SPARC anchor at the same s);
              1-sigma interval from Delta' = +-sigma.  R_law = mu_be(KURVS)/mu_be(KROSS), conservative interval.
  R_obs       in-repo: [(1+z_K)/(1+z_R)]^e x (M*_K/M*_R)^-0.30, e = 0.23 +- 0.52 (2-sigma bracket); literature ABSTRACT-LEVEL:
              [(1+z_K)/(1+z_R)]^2.5 x (M*_K/M*_R)^-0.36 +- 20% (declared allowance).  Medians computed here.
  rule        disfavoured iff the gap between R_law and the nearest bracket edge exceeds R_law's 1-sigma half-interval on that side.
MUTATE=1: R_obs := R_flat(s = 1) (in-repo relative width) -> flat not disfavoured.  MUTATE=2: R_obs := 10 R_flat(s = 1) -> flat disfavoured.
kappa = 1/2 and Omega_c h^2 stay fitted.  Nothing here says the data favour either model, or that the theory is closed.
Run: python3 campaign_fresh_gravity/CFG170_two_epoch_gas_ratio.py   (MUTATE=1 or MUTATE=2 for the pinned controls)
"""
import os, sys, io, math, json, contextlib
import numpy as np
from scipy.optimize import brentq

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import CFG7_common as C

MODE = os.environ.get("MUTATE", "").strip()
assert MODE in ("", "1", "2")
R = C.Report("CFG170_two_epoch_gas_ratio" + (f"_MUTATE{MODE}" if MODE else ""), False)
P, check = R.P, R.check
P(__doc__.split("Run: python3")[0].strip())

F141 = os.path.join(HERE, "CFG141_kurvs_measured_sigma.py")
src = open(F141).read()
g141 = {"__file__": F141, "__name__": "cfg141"}
_saved = os.environ.pop("MUTATE", None)                         # the exec'd pipeline runs unmutated in every mode of this lane
try:
    with contextlib.redirect_stdout(io.StringIO()):
        exec(compile(src[:src.index("# ================================================================== C1 / C2")], "CFG141", "exec"), g141)
finally:
    if _saved is not None:
        os.environ["MUTATE"] = _saved
KU2, SP, KR = g141["KU2"], g141["SP"], g141["g140"]["KR"]
A0, E, gbar, gpred, slope, KPC = g141["A0"], g141["E"], g141["gbar"], g141["gpred"], g141["slope"], g141["KPC"]
LN10, FOOT = math.log(10), "canonical"


def alpha_k21(x):                                                # CFG160's, verbatim
    x = min(max(x, 0.0), 4.0)
    return -0.146 * x * x + 1.204 * x + 1.475


def pooled(d, s):                                                # CFG140's
    w = 1 / s ** 2
    m = float(np.sum(w * d) / np.sum(w)); e = float(1 / math.sqrt(np.sum(w)))
    chi = float(np.sum(w * (d - m) ** 2)); dof = max(len(d) - 1, 1)
    if chi / dof > 1:
        e *= math.sqrt(chi / dof)
    return m, e


def terms(objs):
    V = np.array([o["V"] for o in objs]); eV = np.array([o["eV"] for o in objs]); sg = np.array([o["sig"] for o in objs])
    es = np.array([o["esig"] for o in objs]); Rr = np.array([o["R"] for o in objs]); sm = np.array([o["sm"] for o in objs])
    inc = [math.radians(o["inc"]) if np.isfinite(o["inc"]) and o["inc"] > 1 else math.radians(60) for o in objs]
    ti = np.array([2 * o["V"] ** 2 * o["einc"] / math.tan(i) for o, i in zip(objs, inc)])
    ak = np.array([alpha_k21(o["R"] / (1.68 * o["Rd"]) - 1.0) for o in objs])
    return dict(V=V, eV=eV, sg=sg, es=es, R=Rr, sm=sm, ti=ti, ak=ak)


def DS(T, s, gp, sl):
    al = s * T["ak"]
    vc2 = T["V"] ** 2 + al * T["sg"] ** 2
    go = vc2 * 1e6 / (T["R"] * KPC)
    dlog = np.sqrt((2 * T["V"] * T["eV"]) ** 2 + (2 * al * T["sg"] * T["es"]) ** 2 + T["ti"] ** 2) / vc2 / LN10
    return np.log10(go / gp), np.hypot(dlog, sl * T["sm"])


TK, TR, TS = terms(KU2), terms(KR), terms(SP)
S_LIST = (0.0, 1.00, 1.42, 1.62, 1.69, 3.00)
S_NAME = {0.0: "none", 1.00: "Kretschmer", 1.42: "Dalcanton&Stilp", 1.62: "fixed height", 1.69: "Price n=1", 3.00: "self-grav"}
_anch = {}


def anchor(s, rv):
    if (s, rv) not in _anch:
        gb = np.array([gbar(o, 0.67, 0.0, True) for o in SP])
        a = np.array([A0[FOOT] * (E(o["z"]) if rv else 1.0) for o in SP])
        gp = np.array([gpred(g, aa) for g, aa in zip(gb, a)]); sl = np.array([slope(g, aa) for g, aa in zip(gb, a)])
        _anch[(s, rv)] = pooled(*DS(TS, s, gp, sl))
    return _anch[(s, rv)]


def delta(objs, T, mu, s, rv):
    gb = np.array([gbar(o, mu, 0.0) for o in objs])
    a = np.array([A0[FOOT] * (E(o["z"]) if rv else 1.0) for o in objs])
    gp = np.array([gpred(g, aa) for g, aa in zip(gb, a)]); sl = np.array([slope(g, aa) for g, aa in zip(gb, a)])
    k, ek = pooled(*DS(T, s, gp, sl))
    an, ea = anchor(s, rv)
    return k - an, math.hypot(ek, ea)


GRID = np.exp(np.linspace(math.log(0.01), math.log(30.0), 36))


def root_mu(objs, T, s, rv, target):
    """mu in [0.01, 30] where Delta' - target * sigma = 0 (Delta' decreases with mu)"""
    fn = lambda mu: (lambda d: d[0] - target * d[1])(delta(objs, T, mu, s, rv))
    vals = [fn(m) for m in GRID]
    for lo, hi, flo, fhi in zip(GRID[:-1], GRID[1:], vals[:-1], vals[1:]):
        if flo == 0:
            return float(lo)
        if flo * fhi < 0:
            return float(brentq(fn, lo, hi, xtol=1e-6, rtol=1e-6))
    return float("nan")


def breakeven(objs, T, s, rv):
    return root_mu(objs, T, s, rv, 0.0), root_mu(objs, T, s, rv, +1.0), root_mu(objs, T, s, rv, -1.0)   # (mu_be, mu_lo, mu_hi)


# ================================================================== controls
R.banner("C1 / C2  CONTROLS")
j162 = json.load(open(os.path.join(HERE, "CFG162_pressure_axis_results.json")))["numbers"]["output2"]
kf1 = root_mu(KU2, TK, 1.0, False, 0.0); kh1 = root_mu(KU2, TK, 1.0, True, 0.0)
check("C1 CONTROL: KURVS's break-evens at s = 1 reproduce CFG162's committed values (1e-3)",
      f"flat {kf1:.4f} (CFG162 {j162['mu_f']:.4f}); rival {kh1:.4f} (CFG162 {j162['mu_h']:.4f})",
      abs(kf1 - j162["mu_f"]) < 1e-3 and abs(kh1 - j162["mu_h"]) < 1e-3)
rf2 = delta(KR, TR, 0.67, 1.0, False)[0]; rh2 = delta(KR, TR, 0.67, 1.0, True)[0]
check("C2 CONTROL: KROSS's anchor-corrected Delta' at mu = 0.67, s = 1 reproduces CFG161's post-hoc row (3 decimals)",
      f"flat {rf2:+.4f} (-0.004), rival {rh2:+.4f} (-0.082)", round(rf2, 3) == -0.004 and round(rh2, 3) == -0.082)

# ================================================================== R_obs brackets
zK, zR = float(np.median([o["z"] for o in KU2])), float(np.median([o["z"] for o in KR]))
lmK, lmR = float(np.median([o["lm"] for o in KU2])), float(np.median([o["lm"] for o in KR]))
zf = (1 + zK) / (1 + zR)
m_in, m_lit = 10 ** (-0.30 * (lmK - lmR)), 10 ** (-0.36 * (lmK - lmR))
e0, se = 0.23, 0.52
Rin = zf ** e0 * m_in; Rin2 = (zf ** (e0 - 2 * se) * m_in, zf ** (e0 + 2 * se) * m_in)
Rlit = zf ** 2.5 * m_lit; Rlit_b = (0.8 * Rlit, 1.2 * Rlit)
P(f"  medians: KURVS z {zK:.3f}, log M* {lmK:.2f}; KROSS z {zR:.3f}, log M* {lmR:.2f}; (1+z) ratio {zf:.4f}")
P(f"  R_obs in-repo: {Rin:.3f}, 2-sigma bracket [{Rin2[0]:.3f}, {Rin2[1]:.3f}] (mass factor {m_in:.3f});  "
  f"R_obs literature (ABSTRACT-LEVEL): {Rlit:.3f}, +-20% bracket [{Rlit_b[0]:.3f}, {Rlit_b[1]:.3f}] (mass factor {m_lit:.3f})")

# ================================================================== break-evens and R_law
R.banner("BREAK-EVENS mu_be (1-sigma interval) and the required ratio R_law = mu_be(KURVS) / mu_be(KROSS)")
tab = {}
for s in S_LIST:
    for rv, law in ((False, "flat"), (True, "rival")):
        k = breakeven(KU2, TK, s, rv); r = breakeven(KR, TR, s, rv)
        if np.isfinite(k[0]) and np.isfinite(r[0]) and r[0] > 0:
            # a missing +-sigma root lies outside [0.01, 30] (Delta' falls with mu), so that side of R's interval is OPEN:
            # R_lo -> 0 if mu_lo(KURVS) < 0.01 or mu_hi(KROSS) > 30;  R_hi -> inf if mu_hi(KURVS) > 30 or mu_lo(KROSS) < 0.01.
            # (The first run set R to nan whenever any edge root was missing -- an implementation error, kept as *_firstrun.)
            Rc = k[0] / r[0]
            Rlo = k[1] / r[2] if np.isfinite(k[1]) and np.isfinite(r[2]) else 0.0
            Rhi = k[2] / r[1] if np.isfinite(k[2]) and np.isfinite(r[1]) else float("inf")
        else:
            Rc = Rlo = Rhi = float("nan")
        tab[(s, law)] = dict(kurvs=k, kross=r, R=Rc, R_lo=Rlo, R_hi=Rhi)
        P(f"  s {s:4.2f} ({S_NAME[s]:15s}) {law:5s}: KURVS mu_be {k[0]:.3f} [{k[1]:.3f}, {k[2]:.3f}]; KROSS {r[0]:.3f} [{r[1]:.3f}, {r[2]:.3f}];  "
          f"R_{law} = {Rc:.3f} [{Rlo:.3f}, {Rhi:.3f}]")
for sc in (0.6, 1.4):
    for rv, law in ((False, "flat"), (True, "rival")):
        k0 = root_mu(KU2, TK, sc, rv, 0.0); r0 = root_mu(KR, TR, sc, rv, 0.0)
        tab[(sc, law)] = dict(kurvs=(k0,), kross=(r0,), R=k0 / r0 if np.isfinite(k0) and np.isfinite(r0) and r0 > 0 else float("nan"))
        P(f"  calibration scatter s {sc:.1f}: R_{law} = {tab[(sc, law)]['R']:.3f} (KURVS {k0:.3f}, KROSS {r0:.3f})")

# the power row, printed before any comparison (in every mode; the MUTATE brackets keep the in-repo relative width)
lsep = {s: abs(math.log10(tab[(s, "flat")]["R"]) - math.log10(tab[(s, "rival")]["R"]))
        for s in S_LIST if np.isfinite(tab[(s, "flat")]["R"]) and np.isfinite(tab[(s, "rival")]["R"])}
bw = math.log10(Rin2[1] / Rin2[0])
check("R0 (reported) POWER: |log R_flat - log R_rival| at s = 1 against the log-width of the in-repo 2-sigma bracket",
      f"{lsep.get(1.0, float('nan')):.2f} dex vs {bw:.2f} dex  (other s, reported: "
      + ", ".join(f"s {s:.2f} {v:.2f}" for s, v in lsep.items() if s != 1.0) + ")", True, load_bearing=False)
R.num("power", dict(sep_dex={f"{s:.2f}": v for s, v in lsep.items()}, bracket_width_dex=bw))

if MODE == "1":
    Rin, Rin2 = tab[(1.0, "flat")]["R"], (tab[(1.0, "flat")]["R"] * Rin2[0] / Rin, tab[(1.0, "flat")]["R"] * Rin2[1] / Rin)
    Rlit, Rlit_b = Rin, Rin2
elif MODE == "2":
    base = 10 * tab[(1.0, "flat")]["R"]
    Rin2 = (base * Rin2[0] / Rin, base * Rin2[1] / Rin); Rin = base
    Rlit, Rlit_b = Rin, Rin2


def verdict(t, br):
    """the frozen rule: outside the bracket by more than R's 1-sigma half-interval on that side (= the 1-sigma interval misses the bracket);
    an open side never disfavours"""
    Rc, Rlo, Rhi = t["R"], t.get("R_lo", float("nan")), t.get("R_hi", float("nan"))
    if not np.isfinite(Rc):
        return "no break-even"
    if br[0] <= Rc <= br[1]:
        return "not disfavoured"
    if Rc > br[1]:
        return "disfavoured" if np.isfinite(Rlo) and (Rc - br[1]) > (Rc - Rlo) else "not disfavoured"
    return "disfavoured" if np.isfinite(Rhi) and (br[0] - Rc) > (Rhi - Rc) else "not disfavoured"


R.banner("THE MATRIX (rule: disfavoured iff R_law lies outside the bracket by more than its 1-sigma root-find error)")
mat = {}
for s in S_LIST:
    for law in ("flat", "rival"):
        v_in, v_lit = verdict(tab[(s, law)], Rin2), verdict(tab[(s, law)], Rlit_b)
        mat[f"{s:.2f}|{law}"] = dict(in_repo=v_in, literature=v_lit, R=tab[(s, law)]["R"])
        P(f"  s {s:4.2f} {law:5s}: R = {tab[(s, law)]['R']:.3f}  ->  in-repo [{Rin2[0]:.2f}, {Rin2[1]:.2f}]: {v_in};  literature [{Rlit_b[0]:.2f}, {Rlit_b[1]:.2f}]: {v_lit}")
R.num("table", {f"{k[0]:.2f}|{k[1]}": v for k, v in tab.items()})
R.num("R_obs", dict(in_repo=Rin, in_repo_2sigma=list(Rin2), literature_abstract_level=Rlit, literature_bracket=list(Rlit_b), zK=zK, zR=zR, lmK=lmK, lmR=lmR))
R.num("matrix", mat)

both =[law for law in ("flat", "rival") if mat[f"1.00|{law}"]["in_repo"] == "disfavoured" and mat[f"1.00|{law}"]["literature"] == "disfavoured"]
summary = (f"DIAGNOSTIC: only {both[0]} is disfavoured by both brackets at s = 1" if len(both) == 1 else
           ("NON-DIAGNOSTIC: both laws are disfavoured by both brackets at s = 1" if len(both) == 2 else
            "NON-DIAGNOSTIC: no law is disfavoured by both brackets at s = 1"))
if MODE == "1":
    check("MUTATE=1 [pinned control]: with R_obs set to R_flat(s = 1), flat is not disfavoured (in-repo bracket)", mat["1.00|flat"]["in_repo"],
          mat["1.00|flat"]["in_repo"] == "not disfavoured")
elif MODE == "2":
    check("MUTATE=2 [pinned control]: with R_obs set to 10 R_flat(s = 1), flat is disfavoured (in-repo bracket)", mat["1.00|flat"]["in_repo"],
          mat["1.00|flat"]["in_repo"] == "disfavoured")
else:
    check("H1 [HEADLINE, reported] the declared summary at s = 1", summary, True, load_bearing=False)
R.num("summary", summary)
P(f"\n    SUMMARY (declared): {summary}")
nf = R.write()
raise SystemExit(1 if nf else 0)
