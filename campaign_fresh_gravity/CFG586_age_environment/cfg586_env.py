"""CFG586: is CFG585's old-vs-young early-type excess difference environment (satellite leakage)?
Criteria: FROZEN_CRITERIA.md (8124cb1a4). Executes (unedited, head only, no outputs written): cfg585_age.py (masks + CFG531
estimator), cfg509_counts.py (companion counts and stat()). MUTATE: CFG586_MUTATE=1 assigns OLD 3x its leakage scale.
"""
import os, sys, io, json, math, contextlib
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
LANES = os.path.dirname(HERE)
MUTATE = os.environ.get("CFG586_MUTATE", "0") == "1"
TAG = "_MUTATE" if MUTATE else ""
OUT, CHECKS = [], []


def P(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); OUT.append(s)


def check(c, m):
    CHECKS.append((bool(c), m)); P(f"  [{'PASS' if c else 'FAIL'}] {m}"); return bool(c)


def run_head(path, cut, extra_ns=None):
    src = open(path).read(); assert src.count(cut) >= 1          # head = everything before the FIRST occurrence
    ns = {"__file__": path, "__name__": "head"}; ns.update(extra_ns or {})
    with contextlib.redirect_stdout(io.StringIO()):
        exec(compile(src.split(cut)[0], path, "exec"), ns)
    return ns


for v in ("CFG585_MUTATE", "CFG531_MUTATE"):
    os.environ.pop(v, None)
A = run_head(os.path.join(LANES, "CFG585_age_settling", "cfg585_age.py"), 'P("=" * 100)')
OLD, YOUNG, F30, TYP = A["OLD"], A["YOUNG"], A["F30"], A["TYP"]
esd_loo, comps, all_bands, BANDS, CONS, FOOTS, NPATCH = (A[k] for k in ("esd_loo", "comps", "all_bands", "BANDS", "CONS", "FOOTS", "NPATCH"))
G531 = A["comps"].__globals__                       # CFG531's own namespace (executed head)
MEAS, SHMRS = G531["MEAS"], G531["SHMRS"]
B = run_head(os.path.join(LANES, "CFG509_split_satellite_leakage", "cfg509_counts.py"), "NAMES = [")
stat, wl = B["stat"], B["wl"]

P("=" * 100)
P(f"CFG586  old vs young early types: environment or age?  {'*** MUTATE: OLD leakage x3 ***' if MUTATE else 'PRIMARY'}")
P("=" * 100)
check(abs(B["rw"] - 0.845) < 0.001, f"C1 CFG509 all-lens measured/predicted {B['rw']:.4f} (0.845)")
lam_e = stat(B["typ"] == 1, wl)[0][3]
check(abs(lam_e - 1.0572) < 0.001, f"C2 CFG509 stack-weighted early lambda reproduced: {lam_e:.4f} (1.0572)")

P("\n--- step 1: companion counts (no lensing)")
L = {}
for nm, mk in (("f30all", F30), ("f30early", F30 & (TYP == 1)), ("old", OLD), ("young", YOUNG)):
    full, sd, jk = stat(mk, wl)
    L[nm] = dict(excess=float(full[0]), lam=float(full[3]), lam_sd=float(sd[3]), f_leak=float(full[6]), jk_lam=jk[:, 3])
    P(f"  {nm:9s} N {mk.sum():6d}  companion excess {full[0]:.4f}  lambda {full[3]:.3f} +- {sd[3]:.3f}  f_leak {full[6]:.3f}")
dl = L["old"]["jk_lam"] - L["young"]["jk_lam"]
sdl = math.sqrt((NPATCH - 1) / NPATCH * np.sum((dl - dl.mean()) ** 2))
dlam = L["old"]["lam"] - L["young"]["lam"]
P(f"  lambda_old - lambda_young = {dlam:+.3f} +- {sdl:.3f} (Z {dlam / sdl:+.2f}); ratio {L['old']['lam'] / L['young']['lam']:.3f}")

sc = {"old": L["old"]["lam"] / L["f30all"]["lam"] * (3.0 if MUTATE else 1.0), "young": L["young"]["lam"] / L["f30all"]["lam"]}
P(f"  leakage scale factors (vs f30 average): old {sc['old']:.3f}, young {sc['young']:.3f}")


def scaled(fac):
    return {s: np.clip(fac * MEAS["f30"][s], 0, 1) for s in SHMRS}


def eps_D(fold, fyoung):
    R = {}
    for cls, mk, fac in (("old", OLD, fold), ("young", YOUNG, fyoung)):
        d, C, Lj = esd_loo(mk)
        for c in CONS:
            for foot in FOOTS:
                f_ = scaled(fac)
                cp = comps(c, foot, mk, fE=f_, fO=f_)
                fb = all_bands(d, C, cp); mM = cp["moster"][0] + cp["moster"][1]
                R[(cls, c, foot)] = (fb, {bd: (Lj[:, ii] - mM[ii][None, :]) @ np.array(fb[bd]["wvec"]) for bd, ii in BANDS.items()})
    Dd = {}
    for c in CONS:
        for foot in FOOTS:
            for bd in ("K-in", "K9"):
                (fo, lo), (fy, ly) = R[("old", c, foot)], R[("young", c, foot)]
                dv = lo[bd] - ly[bd]; vj = (NPATCH - 1) / NPATCH * np.sum((dv - dv.mean()) ** 2)
                vq = fo[bd]["sig"] ** 2 + fy[bd]["sig"] ** 2; s = math.sqrt(max(vj, vq))
                dd = fo[bd]["eps"] - fy[bd]["eps"]
                Dd[(c, foot, bd)] = dict(D=dd, sig=s, Z=dd / s, eps_old=fo[bd]["eps"], eps_young=fy[bd]["eps"])
    return Dd


P("\n--- step 2: lensing re-score")
Draw = eps_D(1.0, 1.0)
if not MUTATE:
    import json as _j
    r585 = _j.load(open(os.path.join(LANES, "CFG585_age_settling", "cfg585_results.json")))["R"]
    dev = max(abs(Draw[(c, f, b)]["D"] - r585[f"D|{c}|{f}|{b}"]["D"]) for c in CONS for f in FOOTS for b in ("K-in", "K9"))
    check(dev < 0.001, f"C3 scale 1 reproduces CFG585's D (max dev {dev:.5f})")
Denv = eps_D(sc["old"], sc["young"])
P("  cell            band   D_raw (Z)            D_env (Z)            eps_old / eps_young (env)")
for c in CONS:
    for foot in FOOTS:
        for bd in ("K9", "K-in"):
            a, e = Draw[(c, foot, bd)], Denv[(c, foot, bd)]
            P(f"  [{c} {foot:9s}] {bd:5s}  {a['D']:+.3f} ({a['Z']:+.2f})      {e['D']:+.3f} ({e['Z']:+.2f})      {e['eps_old']:+.3f} / {e['eps_young']:+.3f}")
cells = [(c, f) for c in CONS for f in FOOTS]
expl = all(abs(Denv[(c, f, "K9")]["Z"]) < 1 and Denv[(c, f, "K9")]["D"] <= 0.5 * Draw[(c, f, "K9")]["D"] for c, f in cells)
surv = all(Denv[(c, f, "K9")]["Z"] >= 2 and Denv[(c, f, "K9")]["D"] >= 0.5 * Draw[(c, f, "K9")]["D"] for c, f in cells)
verdict = "ENVIRONMENT EXPLAINS" if expl else ("AGE SIGNAL SURVIVES" if surv else "PARTIAL")
P(f"\nVERDICT: {verdict}")
if MUTATE:
    ok = all(Denv[(c, f, "K9")]["D"] < Draw[(c, f, "K9")]["D"] for c, f in cells)
    check(ok, "MUTATE: tripling OLD's leakage lowers D(K9) in every cell (direction check)")
P(f"\nchecks: {sum(c for c, _ in CHECKS)}/{len(CHECKS)} pass")
json.dump(dict(verdict=verdict, lambda_={k: {kk: vv for kk, vv in v.items() if kk != "jk_lam"} for k, v in L.items()},
               dlam=dlam, dlam_sd=sdl, scale=sc, D_raw={"|".join(k): v for k, v in Draw.items()}, D_env={"|".join(k): v for k, v in Denv.items()}, checks=CHECKS),
          open(os.path.join(HERE, f"cfg586_results{TAG}.json"), "w"), indent=1, default=float)
open(os.path.join(HERE, f"cfg586_env{TAG}.out"), "w").write("\n".join(OUT) + "\n")
