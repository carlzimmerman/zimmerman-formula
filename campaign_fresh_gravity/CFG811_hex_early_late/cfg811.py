"""CFG811 -- H-EX galaxy-scale prediction for the KiDS early-late lensing difference at matched M_b.  Criteria: FROZEN_CRITERIA.md (8223947ba).
Run: python3 cfg811.py   (env CFG811_MUTATE=1: uniform placement; CFG811_SMOKE=1: one M_b, no outputs).
Imports the free-mass projection and CFG804 definitions from CFG810.  kappa = 1/2 FITTED; not theory closed.
"""
import json, math, os, sys
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS"):
    os.environ.setdefault(_v, "1")
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__)); LANES = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(LANES, "CFG810_hex_galaxy_lensing")); sys.path.insert(0, os.path.join(LANES, "CFG637_derived_reservoir"))
import cfg810 as C810                                              # noqa: E402
import cfg637_lib as L637                                          # noqa: E402

MUT = os.environ.get("CFG811_MUTATE") == "1"; SMOKE = os.environ.get("CFG811_SMOKE") == "1"
MODE = "uni" if MUT else "iso"; SUP = C810.SUP
RF_PRIMARY = 1.5; LAW = -0.027; OBS, SIG = 0.280, 0.083
RK = np.array([50.0, 70.71, 100.0]); LMB = [10.5] if SMOKE else [10.0, 10.5, 11.0, 11.5]
OUT = []
def P(s=""):
    print(s, flush=True); OUT.append(str(s))

G4 = C810.load_804(); profile, N_of, Gpc, a0, X = (G4[k] for k in ("profile", "N_of", "Gpc", "a0", "X"))
fE = profile(C810.S_EDGE1); RTA = {}
def rta(M_ta):
    k = round(math.log10(M_ta), 3)
    if k not in RTA: RTA[k] = L637.r_ta_single(M_ta, 1.0)[0]          # kpc, z = 0 (T-K as in CFG721)
    return RTA[k]
def ds(lm, N, M_ta, free=True):
    """Delta-Sigma (Msun/pc^2) at RK for log M_b = lm with N (free mass 5.364 (N-1) M_b, placement MODE)."""
    M = 10 ** lm; rM = math.sqrt(Gpc * M / a0); x = RK * 1e3 / rM
    F = np.exp(np.interp(np.log(x), np.log(X), np.log(fE)))
    if free and N > 1 + 1e-12:
        F = F + C810.free_F(x, SUP * (N - 1), rta(M_ta) * 1e3 / rM, MODE)
    return M / rM ** 2 * F
def delta(rf, free=True):
    rows = []
    for lm in LMB:
        NL, lMta = N_of(lm); MtaL = 10 ** lMta
        dl = ds(lm, NL, MtaL, free); de = ds(lm, rf * NL, rf * MtaL, free)
        rows.append(float(np.mean(np.log10(de / dl))))
    return float(np.mean(rows)), rows
pred = lambda rf, free=True: LAW + delta(rf, free)[0]

P(f"CFG811  H-EX early-late at matched M_b (placement {MODE}); log M_b {LMB}" + ("  [SMOKE]" if SMOKE else ""))
RES = dict(lane="CFG811", placement=MODE, obs=OBS, sigma=SIG)
k1 = abs(pred(1.0) - LAW) < 0.005; k2 = abs(delta(RF_PRIMARY, free=False)[0]) < 1e-12
P(f"  K1 r_f = 1: prediction {pred(1.0):+.4f} (law {LAW:+.3f}) -> {'PASS' if k1 else 'FAIL'}")
P(f"  K2 free share 0: delta {delta(RF_PRIMARY, free=False)[0]:+.2e} -> {'PASS' if k2 else 'FAIL'}")
sens = {}
for rf in (1.0, 1.5, 2.0, 3.0):
    d, rows = delta(rf); sens[rf] = dict(delta=d, pred=LAW + d, Z=(OBS - (LAW + d)) / SIG, per_lMb=rows)
    P(f"  r_f {rf:.1f}: delta {d:+.3f} -> prediction {LAW + d:+.3f} (Z {(OBS - LAW - d) / SIG:+.2f}); per log M_b {['%+.3f' % v for v in rows]}")
if not SMOKE:
    lo, hi = 1.0, 60.0
    for _ in range(40):
        mid = math.sqrt(lo * hi)
        if pred(mid) < OBS: lo = mid
        else: hi = mid
    rneed = math.sqrt(lo * hi); P(f"  diagnostic (not scored): r_f giving exactly +0.280 = {rneed:.2f}" if pred(60.0) >= OBS else "  diagnostic: +0.280 not reached for r_f <= 60")
    RES["rf_needed"] = rneed if pred(60.0) >= OBS else None
p = pred(RF_PRIMARY)
cls = "PASS" if abs(p - OBS) < 2 * SIG else ("OVERSHOOT" if p > OBS else "SHORT")
P(f"\n  PRIMARY r_f = {RF_PRIMARY}: prediction {p:+.3f} vs {OBS:+.3f} +- {SIG} (Z {(OBS - p) / SIG:+.2f}) -> {cls}  (placement {MODE}; conditional on declared r_f)")
RES.update(K1=bool(k1), K2=bool(k2), sens=sens, pred=p, cls=cls)
if not SMOKE:
    sfx = "_MUTATE" if MUT else ""
    json.dump(RES, open(os.path.join(HERE, f"cfg811_results{sfx}.json"), "w"), indent=1, default=float)
    open(os.path.join(HERE, f"cfg811{sfx}.out"), "w").write("\n".join(OUT) + "\n")
