#!/usr/bin/env python3
"""CFG164 -- a measured gas prior for the KURVS discs from PHIBSS (Tacconi et al. 2013), and the decision-cell verdict marginalised over it.

Frozen criteria: CFG164_FROZEN_CRITERIA.md (9a1d4bc9d), committed before any PHIBSS gas value was examined.
  clean       51 rows: no CO upper limit, not fgas-inconsistent, finite Mmol/M*/z_CO, primary component.
  primary     the 17 rows with z_CO in [1.0, 1.7] and log M* in [9.5, 10.8]; each KURVS disc draws mu_mol uniformly from them.
  variant M   OLS log mu = a + b (log M* - 10.5) on the 38 clean z < 1.7 rows, plus the residual scatter (extrapolated below 10.40).
  variant Z   primary x [(1 + z_i)/(1 + z_CO,j)]^2.5 (a declared exponent).  Coherent per draw: Mmol ln 1.5, M* ln 1.3.
  brackets    alpha_CO ULIRG-like (x 0.8/4.36); HI h in {0, 0.5, 1}: mu = mu_mol (1 + h).  4000 draws per prior, seed 164.
  P1 windows (rival 0.6-1.7, flat 2.1-3.7) for the sample median mu; P2 the decision-cell verdict (CFG160's map) at s = 1.00, 1.42,
  1.62, 1.69, 3.00 x K21; P3 KURVS-15's dust limit (1.90 nominal, 3.79 x2) against its prior; X = the spread across priors.
MUTATE=1: every PHIBSS mu x 4 -> P(lean rival | s = 1) < 0.32.  MUTATE=2: x 0.25 -> P(lean flat | s = 1) < 0.05.  Exit 0 when they behave.
kappa = 1/2 and Omega_c h^2 stay fitted.  Nothing here says the data favour either model, or that the theory is closed.
Run: python3 campaign_fresh_gravity/CFG164_gas_prior.py   (MUTATE=1 or MUTATE=2 for the pinned controls)
"""
import os, sys, io, csv, math, contextlib
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import CFG7_common as C

MODE = os.environ.get("MUTATE", "").strip()
assert MODE in ("", "1", "2")
R = C.Report("CFG164_gas_prior" + (f"_MUTATE{MODE}" if MODE else ""), False)
P, check = R.P, R.check
P(__doc__.split("Run: python3")[0].strip())
MUT = {"": 1.0, "1": 4.0, "2": 0.25}[MODE]

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
KU2, SP, A0, E = g141["KU2"], g141["SP"], g141["A0"], g141["E"]
gbar, gpred, slope, KPC = g141["gbar"], g141["gpred"], g141["slope"], g141["KPC"]
LN10 = math.log(10)
FOOT = "canonical"


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


def obs_terms(objs):
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


TK, TS = obs_terms(KU2), obs_terms(SP)
S_LIST = (1.00, 1.42, 1.62, 1.69, 3.00)
S_NAME = {1.00: "Kretschmer", 1.42: "Dalcanton&Stilp", 1.62: "fixed height", 1.69: "Price n=1", 3.00: "self-grav"}
ANCH = {}
for s in S_LIST:                                                 # the SPARC anchor (measured gas) does not depend on the KURVS gas prior
    for rv in (False, True):
        gb = np.array([gbar(o, 0.67, 0.0, True) for o in SP])
        a = np.array([A0[FOOT] * (E(o["z"]) if rv else 1.0) for o in SP])
        gp = np.array([gpred(g, aa) for g, aa in zip(gb, a)]); sl = np.array([slope(g, aa) for g, aa in zip(gb, a)])
        ANCH[(s, rv)] = pooled(*DS(TS, s, gp, sl))


def kurvs_pred(mus):
    """per-disc g_pred and slope for the flat and rival readings at per-disc gas fractions mus"""
    out = {}
    for rv in (False, True):
        gp, sl = [], []
        for o, mu in zip(KU2, mus):
            g = gbar(o, float(mu), 0.0); aa = A0[FOOT] * (E(o["z"]) if rv else 1.0)
            gp.append(gpred(g, aa)); sl.append(slope(g, aa))
        out[rv] = (np.array(gp), np.array(sl))
    return out


def cell(mus, s, pred=None):
    pred = pred or kurvs_pred(mus)
    res = []
    for rv in (False, True):
        k, ek = pooled(*DS(TK, s, *pred[rv]))
        a, ea = ANCH[(s, rv)]
        res += [k - a, math.hypot(ek, ea)]
    return res


def lean(f, ef, h, eh):
    fw, hw = abs(f) <= 2 * ef, abs(h) <= 2 * eh
    if fw and h < -2 * eh:
        return "lean flat"
    if hw and f > 2 * ef:
        return "lean rival"
    if fw and hw:
        return "both within 2 sigma"
    return "neither"


# ================================================================== data and controls
rows = list(csv.DictReader(open(os.path.join(REPO, "data_assembly", "kmos3d_phibss", "phibss13_joined.csv"))))
fl = lambda x: float(x) if x not in ("", None) else float("nan")
clean = [r for r in rows if r["co_upper_limit"] == "0" and r["fgas_inconsistent_in_source"] == "0" and r["comp"] != "se"
         and all(math.isfinite(fl(r[k])) for k in ("mmol_msun", "mstar_msun", "z_co"))]
z_all = [r for r in clean if fl(r["z_co"]) < 1.7]
matched = [r for r in clean if 1.0 <= fl(r["z_co"]) <= 1.7 and 9.5 <= math.log10(fl(r["mstar_msun"])) <= 10.8]
check("C2 CONTROL: the clean count is 51 and the matched count 17 (38 clean rows at z < 1.7)", f"clean {len(clean)}, matched {len(matched)}, z<1.7 {len(z_all)}",
      len(clean) == 51 and len(matched) == 17 and len(z_all) == 38)
dev3 = max(abs(fl(r["mmol_msun"]) / (fl(r["mmol_msun"]) + fl(r["mstar_msun"])) - fl(r["fgas_recomputed"])) for r in clean)
check("C3 CONTROL: fgas_recomputed = Mmol/(Mmol + M*) on the clean rows", f"max |difference| {dev3:.1e}", dev3 < 1e-6)
f1, ef1, h1, eh1 = cell(np.full(10, 0.67), 1.0)
check("C1 CONTROL: with every disc at mu = 0.67 the per-disc pipeline reproduces CFG160's decision cell (4 decimals)",
      f"D'_flat {f1:+.4f} (+0.1441), D'_H {h1:+.4f} (-0.0060)", round(f1, 4) == 0.1441 and round(h1, 4) == -0.0060)

mu_m = np.array([fl(r["mmol_msun"]) / fl(r["mstar_msun"]) for r in matched]) * MUT
z_m = np.array([fl(r["z_co"]) for r in matched])
lmz = np.array([math.log10(fl(r["mstar_msun"])) for r in z_all]); lmu_z = np.log10([fl(r["mmol_msun"]) / fl(r["mstar_msun"]) for r in z_all]) + math.log10(MUT)
b, a = np.polyfit(lmz - 10.5, lmu_z, 1)
resid = float(np.std(lmu_z - (a + b * (lmz - 10.5)), ddof=2))
lmK = np.array([o["lm"] for o in KU2]); zK = np.array([o["z"] for o in KU2])
names = [o["name"] for o in KU2]
i15 = names.index("KURVS-15")
P(f"  variant M fit on 38 rows: log mu = {a:+.3f} {b:+.3f} (log M* - 10.5), residual scatter {resid:.3f} dex; KURVS discs below log M* 10.40: "
  f"{int(np.sum(lmK < 10.40))} of 10 (extrapolated)")

rng = np.random.default_rng(164)
ND = 4000


def draws(kind, h=0.0, aco=1.0):
    out = np.empty((ND, 10))
    for d in range(ND):
        sysf = math.exp(rng.normal(0, math.log(1.5))) / math.exp(rng.normal(0, math.log(1.3)))
        if kind == "M":
            mu = 10 ** (a + b * (lmK - 10.5) + rng.normal(0, resid, 10))
        else:
            j = rng.integers(0, len(mu_m), 10)
            mu = mu_m[j].copy()
            if kind == "Z":
                mu *= ((1 + zK) / (1 + z_m[j])) ** 2.5
        out[d] = mu * sysf * aco * (1 + h)
    return out


PRIORS = {"primary, h 0": ("P", 0.0, 1.0), "primary, h 0.5": ("P", 0.5, 1.0), "primary, h 1": ("P", 1.0, 1.0),
          "variant M, h 0": ("M", 0.0, 1.0), "variant Z, h 0": ("Z", 0.0, 1.0), "alpha_CO ULIRG, h 0": ("P", 0.0, 0.8 / 4.36)}
if MODE:
    PRIORS = {"primary, h 0": PRIORS["primary, h 0"]}

res = {}
for pname, (kind, h, aco) in PRIORS.items():
    D = draws(kind, h, aco)
    mbar = np.median(D, axis=1)
    win = dict(below=float(np.mean(mbar < 0.6)), rival=float(np.mean((mbar >= 0.6) & (mbar <= 1.7))), between=float(np.mean((mbar > 1.7) & (mbar < 2.1))),
               flat=float(np.mean((mbar >= 2.1) & (mbar <= 3.7))), above=float(np.mean(mbar > 3.7)))
    per = dict(rival=float(np.mean((D >= 0.6) & (D <= 1.7))), flat=float(np.mean((D >= 2.1) & (D <= 3.7))))
    q16, q50, q84 = np.percentile(mbar, [16, 50, 84])
    k15 = D[:, i15]
    p3 = dict(above_1p90=float(np.mean(k15 > 1.90)), above_3p79=float(np.mean(k15 > 3.79)), median=float(np.median(k15)))
    cls, zf, zh = {s: {} for s in S_LIST}, {s: [] for s in S_LIST}, {s: [] for s in S_LIST}
    nd_eval = ND if not MODE else 1000
    for d in range(nd_eval):
        pred = kurvs_pred(D[d])
        for s in S_LIST:
            f, ef, hh, eh = cell(D[d], s, pred)
            c_ = lean(f, ef, hh, eh); cls[s][c_] = cls[s].get(c_, 0) + 1
            zf[s].append(f / ef); zh[s].append(hh / eh)
    probs = {s: {k: v / nd_eval for k, v in cls[s].items()} for s in S_LIST}
    res[pname] = dict(mu_bar_16_50_84=[float(q16), float(q50), float(q84)], windows_median=win, windows_per_disc=per, kurvs15=p3,
                      probs={f"{s:.2f}": probs[s] for s in S_LIST},
                      z_flat={f"{s:.2f}": [float(np.percentile(zf[s], p)) for p in (16, 50, 84)] for s in S_LIST},
                      z_rival={f"{s:.2f}": [float(np.percentile(zh[s], p)) for p in (16, 50, 84)] for s in S_LIST})
    if pname == "primary, h 0":
        wid = math.log10(q84 / q16)
        check("R0 (reported) POWER: the 16-84% width of the sample-median mu under the primary prior against the 0.53-dex break-even separation at s = 1",
              f"median mu {q50:.2f} (16-84%: {q16:.2f}-{q84:.2f}), width {wid:.2f} dex", True, load_bearing=False)
    P(f"\n  [{pname}] sample-median mu: {q50:.2f} (16-84% {q16:.2f}-{q84:.2f}); windows (median mu): below 0.6 {win['below']:.2f}, rival {win['rival']:.2f}, "
      f"between {win['between']:.2f}, flat {win['flat']:.2f}, above 3.7 {win['above']:.2f}; per-disc rival {per['rival']:.2f}, flat {per['flat']:.2f}")
    for s in S_LIST:
        pr = probs[s]
        P(f"      s {s:.2f} ({S_NAME[s]:15s}): " + ", ".join(f"{k} {pr.get(k, 0):.2f}" for k in ("lean flat", "lean rival", "both within 2 sigma", "neither"))
          + f";  D'_flat/sigma {np.percentile(zf[s], 50):+.1f} [{np.percentile(zf[s], 16):+.1f}, {np.percentile(zf[s], 84):+.1f}], "
          f"D'_H/sigma {np.percentile(zh[s], 50):+.1f} [{np.percentile(zh[s], 16):+.1f}, {np.percentile(zh[s], 84):+.1f}]")
    P(f"      KURVS-15: prior median mu {p3['median']:.2f}; P(mu > 1.90) = {p3['above_1p90']:.2f}; P(mu > 3.79) = {p3['above_3p79']:.2f}")
R.num("priors", res)

pr0 = res["primary, h 0"]["probs"]["1.00"]
best = max(pr0, key=pr0.get)
verdict = f"diagnostic: {best} ({pr0[best]:.2f})" if pr0[best] >= 0.68 else f"NON-DIAGNOSTIC (largest class {best} at {pr0[best]:.2f})"
if MODE == "1":
    check("MUTATE=1 [pinned control]: with every PHIBSS mu x 4, P(lean rival | s = 1) < 0.32", f"{pr0.get('lean rival', 0):.2f}", pr0.get("lean rival", 0) < 0.32)
elif MODE == "2":
    check("MUTATE=2 [pinned control]: with every PHIBSS mu x 0.25, P(lean flat | s = 1) < 0.05", f"{pr0.get('lean flat', 0):.2f}", pr0.get("lean flat", 0) < 0.05)
else:
    spread = {k: v["probs"]["1.00"].get("lean rival", 0) for k, v in res.items()}
    meds = {k: v["mu_bar_16_50_84"][1] for k, v in res.items()}
    P(f"\n  X (spread across priors at s = 1): P(lean rival) {min(spread.values()):.2f}-{max(spread.values()):.2f}; median mu {min(meds.values()):.2f}-{max(meds.values()):.2f}")
    R.num("X", dict(p_lean_rival=spread, median_mu=meds))
    check("H1 [HEADLINE, reported] class probabilities at s = 1 under the primary prior, h = 0", verdict, True, load_bearing=False)
R.num("verdict", verdict)
nf = R.write()
raise SystemExit(1 if nf else 0)
