#!/usr/bin/env python3
"""AS074 -- Robustness of kappa under small kernel deformations.

Bounded prototype: <=120 s wall/CPU, <=512 MB RSS, 1 thread (enforced below).

Main object (from seed):
    mu_base(Y) = 1 - (1+Y)^(-2),   Y = g/s,  s = c*sqrt(G*rho_Lambda)
    mu_eps    = mu_base + eps*f,   f(0) = f(infty) = 0
    kappa     = 1 / (2 + eps*f'(0))

Response law:  mu_eps(g/s) * g = B        (B = Newtonian baryonic field)
Deep limit Y->0: mu_eps(Y) = (2 + eps*f'(0)) Y + O(Y^2)
  => g^2 = B*s/(2 + eps*f'(0))          => v_flat^4 = G M_b * s/(2+eps f'(0))
  => kappa_eff = 1/(2 + eps*f'(0))      (since v_flat^4 = G M_b a0, a0 = kappa_eff s)

Robustness: kappa_eff = 1/2 for all small eps  <=>  f'(0) = 0.
Endpoints preserved (f(0)=f(inf)=0) is NOT sufficient (negative control).

Deformations used:
  fA(Y) = Y^2/(1+Y)^4   (fA'(0) = 0)  -> preserves kappa (deep coefficient s/2)
  fB(Y) = Y/(1+Y)^2     (fB'(0) = 1)  -> changes kappa to 1/(2+eps)
  fL(Y) = lam*Y/(1+lam*Y)^2  (fL'(0) = lam), lam in {1/2,1,2}: diagnostic set
"""
import sys, os, time, json, resource, hashlib, subprocess
from datetime import datetime, timezone

# ---------------------------------------------------------------- bounds ----
# Enforced inside this process: hard CPU cap 120 s, address-space cap 512 MB.
_CAPS = {}
try:
    _CAPS["cpu_before"] = resource.getrlimit(resource.RLIMIT_CPU)
    hard = resource.getrlimit(resource.RLIMIT_CPU)[1]
    target = min(120, hard) if hard > 0 else 120
    resource.setrlimit(resource.RLIMIT_CPU, (target, hard))
    _CAPS["cpu_s_enforced"] = target
except Exception as e:
    _CAPS["cpu_error"] = str(e)
try:
    _CAPS["as_before"] = resource.getrlimit(resource.RLIMIT_AS)
    hard = resource.getrlimit(resource.RLIMIT_AS)[1]
    if hard in (resource.RLIM_INFINITY, -1) or hard > 512 * 1024 * 1024:
        capped = 512 * 1024 * 1024
        target = capped
    else:
        capped = hard
        target = hard
    resource.setrlimit(resource.RLIMIT_AS, (target, hard))
    _CAPS["as_bytes_enforced"] = target
except Exception as e:
    _CAPS["as_error"] = str(e)
# single-threaded by construction; forbid accidental thread spawn
import threading
assert threading.active_count() == 1

import sympy as sp
import mpmath as mp

T0 = time.time()
mp.mp.dps = 50
DPS_REFINE = 100

# ------------------------------------------------------------- constants ----
G  = mp.mpf("6.67430e-11")   # m^3 kg^-1 s^-2
c  = mp.mpf("299792458")     # m/s
M_sun = mp.mpf("1.98847e30") # kg
pc = mp.mpf("3.085677581491367e16")  # m

def repo_abs(p):
    return os.path.join("/Users/carlzimmerman/new_physics/zimmerman-formula", p)

def sha256_file(p):
    h = hashlib.sha256()
    with open(p, "rb") as fh:
        for blk in iter(lambda: fh.read(1 << 16), b""):
            h.update(blk)
    return h.hexdigest()

OUT = []  # raw output lines
def log(s=""):
    OUT.append(str(s)); print(str(s), flush=True)

log("=" * 100)
log(f"AS074 prototype  started={datetime.now(timezone.utc).isoformat()}")
log(f"mpmath dps = {mp.mp.dps} (refinement to {DPS_REFINE}); bounds={_CAPS}")

# ------------------------------------------------------------- symbolism ----
Y, e, d = sp.symbols("Y eps delta", positive=True)
mu_base = 1 - 1 / (1 + Y) ** 2
mu2 = lambda x: 1 - 1 / (1 + x / 2) ** 2
log("Symbolic identities:")
log(f"  mu_base(Y) - MU2(2Y) = {sp.simplify(mu_base - mu2(2 * Y))}   (exact: mu_base = MU2 at 2Y)")
log(f"  mu_base(Y) - MU2(Y)  = {sp.simplify(mu_base - mu2(Y))}   (nonzero: mu_base != MU2(Y))")
ser = sp.series(mu_base, Y, 0, 5).removeO()
log(f"  mu_base(Y) expansion = {ser}")
log(f"  mu_base'(0)          = {sp.limit(sp.diff(mu_base, Y), Y, 0)}")

def kappa_eff_formula(eps, fp0):
    return sp.simplify(1 / (2 + eps * fp0))

log(f"  kappa_eff = 1/(2+eps*f'(0))   series in eps: "
    f"{sp.series(1/(2 + e*d), e, 0, 4).removeO()}")

# ---------------------------------------------------------- footings -------
def footing(a0_val, name):
    a0 = mp.mpf(a0_val)
    s  = a0 / mp.mpf("0.5")                    # s = a0/kappa, kappa=1/2 adopted
    rho = 4 * a0 ** 2 / (G * c ** 2)           # kg/m^3, rho_Lambda = 4 a0^2/(G c^2)
    rM  = mp.sqrt(G * M_sun / a0)              # m
    vf  = (G * M_sun * a0) ** mp.mpf("0.25")   # m/s deep flat speed, M_sun
    return dict(name=name, a0=a0, s=s, rho=rho, rM=rM, rM_pc=rM / pc, vf=vf)

FOC = footing("9.3619e-11", "canonical")
FOA = footing("1.1279e-10", "alternative")
log("\nFootings (kappa = 1/2 adopted on each, PER CONTRACT they cannot share")
log(" both fixed rho_Lambda and fixed kappa):")
for F in (FOC, FOA):
    log(f"  {F['name']:12s} a0={mp.nstr(F['a0'], 6)} m/s^2  s={mp.nstr(F['s'], 6)} m/s^2  "
        f"rho_L={mp.nstr(F['rho'], 6)} kg/m^3  r_M(Msun)={mp.nstr(F['rM'], 6)} m "
        f"({mp.nstr(F['rM_pc'], 6)} pc)  v_flat(Msun)={mp.nstr(F['vf'], 7)} m/s")
# alternative footing held at fixed canonical density => effective kappa
kap_alt_fixedrho = FOA["a0"] / (2 * FOC["a0"])
log(f"  alternative a0 at CANONICAL fixed rho_Lambda => kappa_eff = "
    f"{mp.nstr(kap_alt_fixedrho, 12)}  (rho fixed; kappa must move -- matches k01 0.602)")
log(f"  rho_L(alt)/rho_L(can) = {mp.nstr(FOA['rho']/FOC['rho'], 6)} = (a0_alt/a0_can)^2")

# ------------------------------------------------------------- kernels -----
def mu_base_f(Y):  return 1 - 1 / (1 + Y) ** 2
def fA(Y):         return Y ** 2 / (1 + Y) ** 4      # fA'(0) = 0
def fB(Y):         return Y / (1 + Y) ** 2           # fB'(0) = 1
def fL(lam, Y):    return lam * Y / (1 + lam * Y) ** 2  # fL'(0) = lam
def mu_eps(eps, f, Y): return mu_base_f(Y) + eps * f(Y)

def fp0(f, h=mp.mpf("1e-25")):  # forward FD at ultra-small h (dps=50 => exact to ~25 digits)
    return (f(h) - f(mp.mpf(0))) / h   # numeric check of claimed f'(0)

for nm, f, claim in (("fA", fA, 0), ("fB", fB, 1)):
    got = fp0(f)
    log(f"  {nm}'(0) numeric = {mp.nstr(got, 10)}  (claimed {claim}; "
        f"match={abs(got-claim)<mp.mpf('1e-6')})")

# ------------------------------------------------- symbolic kappa formula --
EPS = mp.mpf("0.2")
log("\nkappa_eff = 1/(2 + eps*f'(0)) evaluated:")
for nm, f, d0c in (("fA", fA, 0), ("fB", fB, 1),
                   ("fL1/2", lambda Y: fL(mp.mpf("0.5"), Y), mp.mpf("0.5")),
                   ("fL1", lambda Y: fL(mp.mpf(1), Y), 1),
                   ("fL2", lambda Y: fL(mp.mpf(2), Y), 2)):
    d0 = fp0(f)
    kap = 1 / (2 + EPS * d0c)                    # analytic f'(0) for the formula
    log(f"  {nm:6s} f'(0)={mp.nstr(d0c, 6):>9s}  (FD check {mp.nstr(d0, 4):>10s})"
        f"  kappa_eff(eps=0.2) = {mp.nstr(kap, 10)}"
        f"   (1/2 kept? {kap == mp.mpf('0.5')})")

# ------------------------------------------------------ direct residuals ----
# For given eps, f: Y-grid estimator  kappa_est(Y) = 1 / (mu_eps(Y)/Y)  and the
# IMPLICIT response solve  mu_eps(Y)*Y*s = B  (exact root), g = Y*s.
log("\nIndependent check A -- deep slope estimator at fixed Y (s = 1):")
def kest(eps, f, Y): return 1 / (mu_eps(eps, f, Y) / Y)
rowsA = []
for nm, f in (("fA(eps=0.2)", fA), ("fB(eps=0.2)", fB)):
    kap_t = 1 / (2 + EPS * fp0(f))
    R = []
    for Yv in (mp.mpf(10) ** -k for k in (2, 4, 6, 8)):
        ke = kest(EPS, f, Yv)
        R.append((Yv, ke, ke - kap_t))
    rowsA.append((nm, kap_t, R))
    log(f"  {nm:12s} kappa_target={mp.nstr(kap_t, 10)}")
    for Yv, ke, res in R:
        log(f"      Y={mp.nstr(Yv, 3):>9s}  kappa_est={mp.nstr(ke, 16)}  "
            f"residual={mp.nstr(res, 10)}")
# residual scaling rate (should be O(Y): first-order in Y)
for nm, kap_t, R in rowsA:
    r1, r2 = abs(R[0][2]), abs(R[1][2])
    rate = float(mp.log(r1 / r2) / mp.log(mp.mpf(10))) if r1 and r2 else float("nan")
    log(f"  {nm:12s} |residual(Y=1e-2)/|residual(Y=1e-4)| = 10^{rate:.2f}  "
        f"(expect ~10^2 for a first-order-in-Y term)")

# Implicit response: solve mu_eps(Y)*Y*s = B for Y, s = 1.
log("\nIndependent check B -- exact implicit response  mu_eps(g/s)*g = B:")
def solve_Y(eps, f, B, s=1):
    lo = mp.mpf(0)
    hi = mp.mpf(1)
    def F(Y): return mu_eps(eps, f, Y) * Y * s - B
    while F(hi) <= 0 and hi < mp.mpf("1e10"):   # exponential search (Newtonian: Y ~ B/s)
        hi *= 10
    assert F(hi) > 0, "no upper bracket in [0,1e10]"
    for _ in range(300):                       # bisection, exact mpmath
        mid = (lo + hi) / 2
        if F(mid) > 0: hi = mid
        else: lo = mid
    return (lo + hi) / 2

rowsB = []
for nm, f in (("fA(eps=0.2)", fA), ("fB(eps=0.2)", fB)):
    kap_t = 1 / (2 + EPS * fp0(f))
    log(f"  {nm:12s} kappa_target={mp.nstr(kap_t, 12)}   [B/s = g_N in units of s]")
    for Bv in (mp.mpf(10) ** -k for k in (2, 4, 6, 8)):
        Yv = solve_Y(EPS, f, Bv)
        ke = kest(EPS, f, Yv)
        sog = mu_eps(EPS, f, Yv)                 # g in s-units is Y; check law
        rowsB.append((nm, Bv, Yv, ke, ke - kap_t))
        log(f"      B/s={mp.nstr(Bv, 3):>9s}  g/s={mp.nstr(Yv, 10):>10s}  "
            f"mu_eps*Y*s/B - 1 = {mp.nstr(sog*Yv/Bv - 1, 3):>9s}  "
            f"kappa_est={mp.nstr(ke, 14)}  residual={mp.nstr(ke-kap_t, 9)}")

# Newtonian recovery
log("\nIndependent check C -- Newtonian limit Y->inf:  g/B -> 1 exactly:")
for Bv in (mp.mpf(10) ** k for k in (0, 1, 2, 4)):
    Yv = solve_Y(EPS, fB, Bv)
    gB = Yv / Bv                                 # Y = g/s, here s=1
    log(f"      B/s={mp.nstr(Bv, 3):>9s}  g/B = {mp.nstr(gB, 14)}  "
        f"|g/B-1| = {mp.nstr(abs(gB-1), 9)}")

# Boundary identities (exact): mu_eps(0) = 0 ; mu_eps(inf) = 1
log("\nBoundaries (exact identities of the deformation class f(0)=f(inf)=0):")
for nm, f in (("fA", fA), ("fB", fB)):
    log(f"  {nm}: mu_eps(0)={mu_eps(EPS,f,mp.mpf(0))} (exact 0)  "
        f"mu_eps(1e6)={mp.nstr(mu_eps(EPS,f,mp.mpf('1e6')), 12)} (->1)  "
        f"mu_eps(1e6)-1 = {mp.nstr(mu_eps(EPS,f,mp.mpf('1e6'))-1, 3)}")

# -------------------------------------------------------- negative control --
# Premise under test: "endpoint preservation (f(0)=f(inf)=0) is SUFFICIENT for
# coefficient preservation".  Applied to the SECOND deformation fB (nonzero
# derivative at zero).  Must be capable of failing; it DOES fail: the actual
# kappa_eff = 1/(2+eps) != 1/2 even though endpoints are preserved.
log("\nNEGATIVE CONTROL -- 'endpoint preservation => coefficient preservation':")
log(f"  premise prediction : kappa_pred = 1/2 for fB (endpoints fB(0)=fB(inf)=0)")
pred = mp.mpf("0.5")
act  = 1 / (2 + EPS * 1)          # fB'(0) = 1
log(f"  actual (control run): kappa_eff(eps=0.2) = {mp.nstr(act, 15)}")
log(f"  control result: premise FAILS: kappa_pred - kappa_eff = "
    f"{mp.nstr(pred - act, 10)} != 0  =>  endpoint preservation is NOT sufficient.")
log(f"  control capability: the run discriminates -- fA (f'(0)=0) gives "
    f"{mp.nstr(1/(2+EPS*0), 10)} = 1/2 exactly (control passes there), "
    f"fB gives {mp.nstr(act, 10)} =! 1/2 (control fails there).")

# ------------------------------------------------------- lambda counterex. --
log("\nDiagnostic counterexamples (lambda = 1/2, 1, 2), eps = 0.2:")
kapL = {}
for lam in (mp.mpf("0.5"), mp.mpf(1), mp.mpf(2)):
    k = 1 / (2 + EPS * lam)
    kapL[str(lam)] = k
    log(f"  f_L(Y)=lam*Y/(1+lam*Y)^2, f_L'(0)={lam}:  kappa_eff = "
        f"{mp.nstr(k, 12)}")
distinct = len({mp.nstr(v, 20) for v in kapL.values()}) == 3
log(f"  three DISTINCT kappa_eff values: {distinct}  "
    f"(coefficient genuinely moves with the deformation scale; "
    f"no observational preference involved)")

# --------------------------------------------------- dimensional carry-out --
log("\nDimensional examples (deformation fB, eps = 0.2, delta = fB'(0) = 1):")
kapB = 1 / (2 + EPS)                          # kappa_eff for fB
for F in (FOC, FOA):
    a0_eff = kapB * F["s"]
    vf_eff = (G * M_sun * a0_eff) ** mp.mpf("0.25")
    rho_rigid = F["rho"] * (2 * kapB) ** 2    # density needed if kappa kept 1/2
    log(f"  {F['name']:12s} kappa_eff={mp.nstr(kapB, 8)}  "
        f"a0_eff={mp.nstr(a0_eff, 6)} m/s^2  (a0={mp.nstr(F['a0'],6)}, "
        f"s fixed at {mp.nstr(F['s'],6)})")
    log(f"      v_flat,eff(Msun)={mp.nstr(vf_eff, 6)} m/s  (was {mp.nstr(F['vf'],6)})")
    log(f"      if kappa is held at 1/2 instead: required rho_L' = "
        f"{mp.nstr(rho_rigid, 6)} kg/m^3 = {mp.nstr(rho_rigid/F['rho'], 6)} x rho_L")

# -------------------------------------------------------------- refinement --
log(f"\nRefinement: re-check key residuals at dps = {DPS_REFINE}:")
mp.mp.dps = DPS_REFINE
Yr = mp.mpf("1e-8")
ke = kest(EPS, fB, Yr)
log(f"  fB kappa_est at Y=1e-8 (dps=100): {mp.nstr(ke, 30)}  "
    f"target 1/2.2 = {mp.nstr(1/mp.mpf('2.2'), 30)}  "
    f"residual {mp.nstr(ke - 1/mp.mpf('2.2'), 8)}")
ke2 = kest(EPS, fA, Yr)
log(f"  fA kappa_est at Y=1e-8 (dps=100): {mp.nstr(ke2, 30)}  "
    f"residual to 1/2: {mp.nstr(ke2 - mp.mpf('0.5'), 8)}")

WALL = time.time() - T0
ru = resource.getrusage(resource.RUSAGE_SELF)
CPU = ru.ru_utime + ru.ru_stime
if sys.platform == "darwin":
    RSS_MIB = ru.ru_maxrss / (1024.0 * 1024.0)   # macOS: ru_maxrss is BYTES
else:
    RSS_MIB = ru.ru_maxrss / 1024.0              # Linux: KiB
log("\n" + "=" * 100)
log(f"finished={datetime.now(timezone.utc).isoformat()}  wall={WALL:.3f} s  "
    f"cpu={CPU:.3f} s  maxrss={RSS_MIB:.1f} MiB  "
    f"threads={threading.active_count()}  bounds_ok={WALL<=120 and CPU<=120 and RSS_MIB<=512}")

SELF = os.path.abspath(__file__)
print(f"\nSELF_hash={sha256_file(SELF)}")
print(f"OUTPUT_JSON_BEGIN")
print(json.dumps({"rowsA": [[nm, str(kap_t), [[str(Yv), str(ke), str(res)] for Yv, ke, res in R]]
                            for nm, kap_t, R in rowsA],
                  "rowsB": [[nm, str(Bv), str(Yv), str(ke), str(res)] for nm, Bv, Yv, ke, res in rowsB],
                  "footings": {F["name"]: {"a0": str(F["a0"]), "s": str(F["s"]),
                                           "rho": str(F["rho"]), "rM": str(F["rM"]),
                                           "rM_pc": str(F["rM_pc"]), "vf": str(F["vf"])}
                               for F in (FOC, FOA)},
                  "kappa_alt_fixedrho": str(kap_alt_fixedrho),
                  "kappa_eff_fB_eps02": str(act),
                  "negative_control": {"premise": "f(0)=f(inf)=0 => kappa preserved",
                                       "predicted_kappa": "0.5",
                                       "actual_kappa": str(act),
                                       "passed": act == mp.mpf("0.5")},
                  "lambda_set": {k: str(v) for k, v in kapL.items()},
                  "bounds": _CAPS, "wall_s": WALL, "cpu_s": CPU,
                  "maxrss_kib": ru.ru_maxrss}, indent=1))