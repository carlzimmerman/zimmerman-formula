#!/usr/bin/env python3
"""CFG161 -- a consistency check of CFG160's P4: the KURVS - KROSS differential under Kretschmer et al.'s pressure support.

Frozen criteria: CFG161_FROZEN_CRITERIA.md (507725b7b). DISCLOSURE: the file was written before, and committed unchanged after, the
orchestrator relayed CFG165's result for this question; the criteria are blind, the outcome is not.
  D           Delta_flat(KURVS) - Delta_flat(KROSS), pooled, mu 0.67, delta 0, canonical, no anchor (CFG140's R3 definition).
  D_flat = 0; D_H = [Delta_flat - Delta_H]_KURVS - [Delta_flat - Delta_H]_KROSS (exact, through the pipeline); CFG140's +0.083 reported.
  rule        lands on flat / lands on the rival / consistent with both / P4 manufactures evolution (2 sigma_D).
  C1 CONTROL  CFG140's committed R3 differentials (P0, P1) reproduce (3-decimal print).  C2 CONTROL  CFG160's decision cell reproduces.
  H1 [HEADLINE; MUTATE must change it] P4 does not manufacture evolution: D within 2 sigma_D of at least one prediction.
MUTATE=1: every KURVS v_last x 10^0.3 (inherited from CFG140's exec'd prefix) -- H1 must FAIL (rc = 1).
kappa = 1/2 and Omega_c h^2 stay fitted.  Nothing here says the data favour either model, or that the theory is closed.
Run: python3 campaign_fresh_gravity/CFG161_kross_differential_p4.py   (MUTATE=1 for the control)
"""
import os, sys, io, re, math, json, contextlib
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import CFG7_common as C

MUTATE = os.environ.get("MUTATE", "0") == "1"
R = C.Report("CFG161_kross_differential_p4", MUTATE)
P, check = R.P, R.check
P(__doc__.split("Run: python3")[0].strip())
if MUTATE:
    P("\n  *** MUTATE=1: every KURVS v_last x 10^0.3 (g_obs x 4) -- H1 must FAIL ***")

F141 = os.path.join(HERE, "CFG141_kurvs_measured_sigma.py")
src = open(F141).read()
g141 = {"__file__": F141, "__name__": "cfg141"}
with contextlib.redirect_stdout(io.StringIO()):                 # MUTATE inherited on purpose: it is this lane's declared MUTATE
    exec(compile(src[:src.index("# ================================================================== C1 / C2")], "CFG141", "exec"), g141)
g140 = g141["g140"]
KU, KU2, KR, SP = g140["KU"], g141["KU2"], g140["KR"], g141["SP"]
A0, E, gbar, gpred, slope, pooled, KPC = g141["A0"], g141["E"], g141["gbar"], g141["gpred"], g141["slope"], g141["pooled"], g141["KPC"]
score, score3 = g141["score"], g141["score3"]


# ------------------------------------------------------------------ P4 functions, copied verbatim from CFG160_kurvs_kretschmer.py
def alpha_k21(x):
    x = min(max(x, 0.0), 4.0)
    return -0.146 * x * x + 1.204 * x + 1.475


def alpha_of(o, mode, re_fac, a_scale):
    if mode == "P2":
        return 2.0 * o["R"] / o["Rd"]
    return a_scale * alpha_k21(o["R"] / (re_fac * 1.68 * o["Rd"]) - 1.0)


def gobs4(o, mode="K21", re_fac=1.0, a_scale=1.0):
    al = alpha_of(o, mode, re_fac, a_scale)
    vc2 = o["V"] ** 2 + al * o["sig"] ** 2
    return vc2 * 1e6 / (o["R"] * KPC), vc2, al


def dlog4(o, mode="K21", re_fac=1.0, a_scale=1.0):
    _, vc2, al = gobs4(o, mode, re_fac, a_scale)
    V = o["V"]
    tv = 2 * V * o["eV"]
    ts = 2 * al * o["sig"] * o["esig"]
    inc = math.radians(o["inc"]) if np.isfinite(o["inc"]) and o["inc"] > 1 else math.radians(60)
    ti = 2 * V ** 2 * o["einc"] / math.tan(inc)
    return math.sqrt(tv ** 2 + ts ** 2 + ti ** 2) / vc2 / math.log(10)


def score4(objs, mu, dlt, foot, measured_gas=False, rival=False, mode="K21", re_fac=1.0, a_scale=1.0, per=False):
    D, S = [], []
    for o in objs:
        a = A0[foot] * (E(o["z"]) if rival else 1.0)
        gb = gbar(o, mu, dlt, measured_gas)
        gp = gpred(gb, a)
        go, _, _ = gobs4(o, mode, re_fac, a_scale)
        D.append(math.log10(go / gp)); S.append(math.hypot(dlog4(o, mode, re_fac, a_scale), slope(gb, a) * o["sm"]))
    return (pooled(D, S), np.array(D), np.array(S)) if per else pooled(D, S)


MU, DLT, FOOT = 0.67, 0.0, "canonical"


def pair(fn_ku, fn_kr):
    """returns (D, sigma_D, D_H, own) for flat/rival statistics computed by the two scoring callables"""
    (kf, ekf), (kh, _) = fn_ku(False), fn_ku(True)
    (rf, erf), (rh, _) = fn_kr(False), fn_kr(True)
    D, sD = kf - rf, math.hypot(ekf, erf)
    DH = (kf - kh) - (rf - rh)
    return D, sD, DH, dict(KURVS_flat=kf, KURVS_H=kh, KROSS_flat=rf, KROSS_H=rh, eKURVS=ekf, eKROSS=erf)


def rule(D, sD, DH):
    nf, nh = abs(D) <= 2 * sD, abs(D - DH) <= 2 * sD
    if nf and nh:
        return "consistent with both"
    if nf:
        return "lands on flat"
    if nh:
        return "lands on the rival"
    return "P4 manufactures evolution" if True else ""


# ================================================================== C1 / C2
R.banner("C1 / C2  CONTROLS")
out140 = open(os.path.join(HERE, "CFG140_kurvs_a0z" + ("_MUTATE" if MUTATE else "") + ".out")).read()
m = {k: (float(a), float(b)) for k, a, b in re.findall(r"(P[01]): KROSS Delta_flat [^;]*; KURVS [^;]*; differential ([+-][0-9.]+) \+- ([0-9.]+)", out140)}
c1 = {}
for Pv in ("P0", "P1"):
    (kf, ekf), _, _ = score(KU, MU, DLT, Pv, FOOT)
    (rf, erf), _, _ = score(KR, MU, DLT, Pv, FOOT)
    c1[Pv] = (round(kf - rf, 3), round(math.hypot(ekf, erf), 3))
ok1 = len(m) == 2 and all(c1[k] == m[k] for k in m)
check("C1 CONTROL: CFG140's committed R3 differentials reproduce (3-decimal print)" + ("  [against CFG140's MUTATE output]" if MUTATE else ""),
      f"committed {m}; mine {c1}", ok1)
j160 = json.load(open(os.path.join(HERE, "CFG160_kurvs_kretschmer" + ("_MUTATE" if MUTATE else "") + "_results.json")))["numbers"]["decision_cell"]["P4 primary"]
kf, ekf = score4(KU2, MU, DLT, FOOT); kh, ekh = score4(KU2, MU, DLT, FOOT, rival=True)
af, eaf = score4(SP, MU, DLT, FOOT, measured_gas=True); ah, eah = score4(SP, MU, DLT, FOOT, measured_gas=True, rival=True)
ok2 = abs((kf - af) - j160["df"]) < 5e-4 and abs((kh - ah) - j160["dh"]) < 5e-4
check("C2 CONTROL: the copied P4 functions reproduce CFG160's committed decision cell" + ("  [MUTATE]" if MUTATE else ""),
      f"D'_flat {kf - af:+.4f} (CFG160 {j160['df']:+.4f}); D'_H {kh - ah:+.4f} (CFG160 {j160['dh']:+.4f})", ok2)

# ================================================================== R0 power, then the headline
R.banner("R0  POWER (before the differential is printed)")
D4, sD4, DH4, own4 = pair(lambda rv: score4(KU2, MU, DLT, FOOT, rival=rv), lambda rv: score4(KR, MU, DLT, FOOT, rival=rv))
zk, zr = float(np.median([o["z"] for o in KU])), float(np.median([o["z"] for o in KR]))
approx = 0.5 * math.log10(E(zk) / E(zr))
check("R0 (reported) POWER: sigma_D, the rival's predicted differential D_H and |D_H| / sigma_D under P4",
      f"sigma_D {sD4:.3f}; D_H {DH4:+.3f} (CFG140's deep-regime approximation {approx:+.3f}); |D_H|/sigma_D {abs(DH4) / sD4:.2f}", True, load_bearing=False)

R.banner("H1  the P4 differential and the frozen decision rule")
v4 = rule(D4, sD4, DH4)
P(f"  P4: D = {D4:+.3f} +- {sD4:.3f}; flat predicts 0 ({D4 / sD4:+.1f} sigma away), the rival predicts {DH4:+.3f} ({(D4 - DH4) / sD4:+.1f} sigma away): {v4}")
check("H1 [HEADLINE] P4 does not manufacture evolution: D within 2 sigma_D of at least one prediction" + ("  [MUTATE: v x 2]" if MUTATE else ""),
      f"D {D4:+.3f} +- {sD4:.3f}, D_H {DH4:+.3f}: {v4}", v4 != "P4 manufactures evolution")
R.num("P4", dict(D=D4, sigma_D=sD4, D_H=DH4, D_H_approx=approx, verdict=v4, own=own4))

# ================================================================== R1-R3 reported rows
R.banner("R1  the differential under every prescription (mu 0.67, delta 0, canonical, unanchored)")
rows = {}
specs = {
    "P0 (none)": (lambda rv: score(KU2, MU, DLT, "P0", FOOT, rival=rv)[0], lambda rv: score(KR, MU, DLT, "P0", FOOT, rival=rv)[0]),
    "P1 (sigma0 on KURVS)": (lambda rv: score(KU, MU, DLT, "P1", FOOT, rival=rv)[0], lambda rv: score(KR, MU, DLT, "P1", FOOT, rival=rv)[0]),
    "P2 (sigma_out on KURVS)": (lambda rv: score(KU2, MU, DLT, "P1", FOOT, rival=rv)[0], lambda rv: score(KR, MU, DLT, "P1", FOOT, rival=rv)[0]),
    "P3 (fixed height)": (lambda rv: score3(KU2, MU, DLT, FOOT, rival=rv), lambda rv: score3(KR, MU, DLT, FOOT, rival=rv)),
    "P4 (Kretschmer, primary)": (lambda rv: score4(KU2, MU, DLT, FOOT, rival=rv), lambda rv: score4(KR, MU, DLT, FOOT, rival=rv)),
}
for name, (fk, fr) in specs.items():
    D, sD, DH, own = pair(fk, fr)
    rows[name] = dict(D=D, sigma_D=sD, D_H=DH, verdict=rule(D, sD, DH), own=own)
    P(f"  {name:26s}: D {D:+.3f} +- {sD:.3f}; D_H {DH:+.3f}; {rule(D, sD, DH)}")
R.num("R1", rows)

R.banner("R2  the P4 band and the KURVS sigma0 variant")
r2 = {}
for name, kw, ku in (("P4 alpha x 0.6", dict(a_scale=0.6), KU2), ("P4 alpha x 1.4", dict(a_scale=1.4), KU2), ("P4, KURVS sigma0", {}, KU)):
    D, sD, DH, own = pair(lambda rv, kw=kw, ku=ku: score4(ku, MU, DLT, FOOT, rival=rv, **kw), lambda rv, kw=kw: score4(KR, MU, DLT, FOOT, rival=rv, **kw))
    r2[name] = dict(D=D, sigma_D=sD, D_H=DH, verdict=rule(D, sD, DH))
    P(f"  {name:18s}: D {D:+.3f} +- {sD:.3f}; D_H {DH:+.3f}; {rule(D, sD, DH)}")
R.num("R2", r2)

R.banner("R3  the two samples' own pooled Delta under P4 (unanchored)")
P(f"  KURVS: Delta_flat {own4['KURVS_flat']:+.3f} +- {own4['eKURVS']:.3f}, Delta_H {own4['KURVS_H']:+.3f};  "
  f"KROSS (N {len(KR)}): Delta_flat {own4['KROSS_flat']:+.3f} +- {own4['eKROSS']:.3f}, Delta_H {own4['KROSS_H']:+.3f}")

reading = {"consistent with both": "P4 does not manufacture evolution between z ~ 0.85 and 1.5: a weak consistency pass, not a validation of P4; nothing about a0",
           "lands on flat": "the differential lands on flat's prediction at ~1-2 sigma power: reported as that, not an a0 verdict",
           "lands on the rival": "the differential lands on the rival's prediction at ~1-2 sigma power: reported as that, not an a0 verdict",
           "P4 manufactures evolution": "P4 manufactures an evolution neither reading predicts: this counts against P4 (and so against CFG160's lean), not against either law"}[v4]
R.num("reading", reading)
P(f"\n    READING (declared): {reading}")
nf = R.write()
raise SystemExit(1 if nf else 0)
