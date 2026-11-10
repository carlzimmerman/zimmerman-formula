#!/usr/bin/env python3
"""W4-24 -- the vacuum constant in the two-phase action. Audit lane; no kappa is derived.
Criteria: FROZEN_CRITERIA.md (committed alone, 180b1ff772). Light: sympy + mpmath, single core, seconds.
Run from the repo root:
    python3 why_4_puzzle/W4_24_two_phase_vacuum_constant/w4_24.py > why_4_puzzle/W4_24_two_phase_vacuum_constant/w4_24.out
    W4_24_MUTATE=1 python3 ... > .../w4_24_MUTATE.out
MUTATE runs three arms one at a time (they would partly cancel if combined): MU1 Poisson 4 pi G -> 8 pi G,
MU2 pressure step x 0.9, MU3 constant outside the switch. Exit 1 when all three bite, 2 otherwise.
kappa = 1/2 FITTED. Not theory closed.
"""
import json
import os
import sys

import mpmath as mp
import sympy as sp

mp.mp.dps = 30
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
MUT = os.environ.get("W4_24_MUTATE") == "1"
SUF = "_MUTATE" if MUT else ""
OUT, checks, res = [], [], {}


def P(s=""):
    print(s)
    OUT.append(str(s))


def check(name, detail, ok, store=True):
    if store:
        checks.append({"name": name, "detail": str(detail), "pass": bool(ok)})
    P(f"[{'PASS' if ok else 'FAIL'}] {name}: {detail}")
    return bool(ok)


def within(val, hand, tol=0.01):
    return abs(float(val) - hand) <= tol * abs(hand)


# ---------------- the law in wall units a0^2 / (4 pi G) (SWT1 criteria, I-c and I-d) ----------------
def nu(y):
    return mp.mpf(1) / 2 + mp.sqrt(mp.mpf(1) / 4 + 1 / mp.mpf(y))


def u1(y):
    return nu(y) * mp.mpf(y)


def Wc(u):
    u = mp.mpf(u)
    return u - mp.log1p(u) - u ** 2 / (2 * (1 + u) ** 2)


def uS(S, y):
    """positive root of (1 - S/(1+u)) u = y, i.e. u^2 + (1 - S - y) u - y = 0"""
    b = 1 - S - y
    return (-b + mp.sqrt(b * b + 4 * y)) / 2


def Jred(u):
    return u - mp.log1p(u)


P("W4-24 the vacuum constant in the two-phase action" + ("  [MUTATE: MU1, MU2, MU3 one at a time]" if MUT else ""))
P("kappa = 1/2 FITTED; not theory closed. Audit lane: no kappa is output.\n")

# ---------------- K1: the wall pressure, with and without the constant ----------------
ys = [mp.mpf("1e-4"), mp.mpf("1e-2"), mp.mpf(1) / 3, mp.mpf(1), mp.mpf(3), mp.mpf(100), mp.mpf("1e4")]
rows_a, worst_a = [], mp.mpf(0)
for y in ys:
    q = mp.quad(lambda S: Jred(uS(S, y)), [0, mp.mpf(1) / 2, 1])
    cl = Wc(u1(y))
    rel = abs(q - cl) / cl
    worst_a = max(worst_a, rel)
    rows_a.append({"y": float(y), "quad": float(q), "closed": float(cl), "rel": float(rel)})
    P(f"  y = {float(y):<8g} quadrature {mp.nstr(q, 14):<20} closed W(u1) {mp.nstr(cl, 14):<20} rel {mp.nstr(rel, 3)}")
res["K1a"] = rows_a
check("K1a identity by quadrature", f"integral_0^1 J(u(S,y)) dS = W(u1) at seven y, worst relative {mp.nstr(worst_a, 3)} (line 1e-8)",
      worst_a < mp.mpf("1e-8"))

swt1 = json.load(open(os.path.join(REPO, "fable52_push", "SWT1_switch_theorems", "swt1.json")))
# AMENDMENT A1 (603285f007): rows with y >= 1e-3 keep the frozen line 1e-10 against "closed"; the y = 1e-6 row, whose
# stored double loses digits to cancellation, is graded at 1e-9 against "closed" and at 1e-12 against the stored "quad".
rows_b, k1b = [], True
for r in swt1["KA"]["KA_W1"]["rows"]:
    y = mp.mpf(repr(r["y"]))
    cl = Wc(u1(y))
    rel = abs(cl - mp.mpf(repr(r["closed"]))) / cl
    relq = abs(cl - mp.mpf(repr(r["quad"]))) / cl
    small = y < mp.mpf("1e-3")
    row_ok = (rel < mp.mpf("1e-9") and relq < mp.mpf("1e-12")) if small else (rel < mp.mpf("1e-10"))
    k1b = k1b and row_ok
    rows_b.append({"y": r["y"], "swt1_closed": r["closed"], "swt1_quad": r["quad"], "here": float(cl), "rel_closed": float(rel),
                   "rel_quad": float(relq), "line": "1e-9 closed and 1e-12 quad (A1)" if small else "1e-10 closed", "pass": bool(row_ok)})
    P(f"  swt1.json y = {r['y']:<8g} closed {r['closed']:<24} here {mp.nstr(cl, 16):<22} rel {mp.nstr(rel, 3):<9} "
      f"rel to its quad {mp.nstr(relq, 3):<9} {'(A1 lines)' if small else ''}")
res["K1b"] = rows_b
check("K1b against swt1.json", "closed form equals KA_W1 at its six y: 1e-10 against 'closed' for y >= 1e-3; at y = 1e-6, "
      "1e-9 against 'closed' and 1e-12 against 'quad' (AMENDMENT A1)", k1b)

S_, V_ = sp.Symbol("S"), sp.Symbol("V_in")
Jf = sp.Function("J")
lhs = sp.integrate(Jf(S_) - V_, (S_, 0, 1))
rhs = sp.Integral(Jf(S_), (S_, 0, 1)) - V_
check("K1c the constant is a pressure step", f"integral_0^1 [J - V_in] dS = {lhs}  (= p_wall - V_in)",
      sp.simplify(lhs - rhs) == 0)

# ---------------- K2: Xi, symbolic ----------------
G, c, rho, kap = sp.symbols("G c rho kappa", positive=True)
eta = sp.Symbol("eta", real=True)
lam, mu_, nu_ = sp.symbols("lambda mu nu", positive=True)


def xi_symbolic(cpl=4, wfac=1):
    """V_in / wall unit. cpl: Poisson's coupling cpl*pi*G (4 as frozen). wfac: |w| of the step (1 as frozen)."""
    a0 = kap * c * sp.sqrt(G * rho)
    unit = a0 ** 2 / (cpl * sp.pi * G)
    return sp.simplify(wfac * eta * rho * c ** 2 / unit)


Xi = xi_symbolic()
P(f"\nXi = V_in / (a0^2 / 4 pi G) = {Xi}")
check("K2 Xi symbolic", "with a0 = kappa c sqrt(G rho) and V_in = eta rho c^2, Xi = 4 pi eta / kappa^2",
      sp.simplify(Xi - 4 * sp.pi * eta / kap ** 2) == 0)
a0s = kap * c * sp.sqrt(G * rho)
Xi_scaled = sp.simplify((eta * (mu_ * rho) * (nu_ * c) ** 2) / ((kap * (nu_ * c) * sp.sqrt(lam * G * mu_ * rho)) ** 2
                                                                / (4 * sp.pi * lam * G)))
check("I3 scaling", "Xi unchanged under G -> lambda G, rho -> mu rho, c -> nu c", sp.simplify(Xi_scaled - Xi) == 0)

# ---------------- K3-K5: the bounds ----------------
F_ALLOW = mp.mpf("0.0231")                 # SWT1 T2 filling allowance (I-e)
GATES = [("G-M", mp.mpf(1), 0.4646, 5.20, 34.2), ("G-D", mp.mpf(1) / 100, 6.421e-4, 139.9, 920.0)]


def bounds(cpl=4, wfac=1, eta_on=1):
    """kappa_min per gate and branch. eta_on = 0 moves the constant outside the switch."""
    cxi = sp.simplify(xi_symbolic(cpl, wfac).subs({eta: 1, kap: 1}))        # Xi = cxi * eta / kappa^2
    cx = mp.mpf(str(sp.N(cxi, 30)))
    out = {"cxi": str(cxi)}
    for name, y, _, _, _ in GATES:
        w = Wc(u1(y))
        out[name] = {"y": float(y), "u1": float(u1(y)), "W": float(w),
                     "plus1": float(mp.sqrt(cx * eta_on / w)),
                     "plus1_over_f": float(mp.sqrt(cx * eta_on / F_ALLOW / w)),
                     "minus1": float(mp.sqrt(cx * eta_on / w))}
    return out, cx


B, CX = bounds()
res["bounds"] = B
P(f"\nXi = ({B['cxi']}) eta / kappa^2.  kappa_min(y) = sqrt(|Xi kappa^2| / W(u1(y)))")
k3 = True
for name, y, hw, hk, hk5 in GATES:
    b = B[name]
    P(f"  {name}: y = {b['y']:g}, u1 = {b['u1']:.8f}, W = {b['W']:.6g}; kappa_min: eta=+1 {b['plus1']:.4f}, "
      f"eta=+1/f {b['plus1_over_f']:.3f}, eta=-1 {b['minus1']:.4f}")
    k3 = k3 and within(b["W"], hw) and within(b["plus1"], hk)
check("K3 bounds, eta = +1", "W = 0.4646 and 6.421e-4, kappa_min = 5.20 and 139.9 at G-M and G-D, each within 1 % of the hand value", k3)

C_KMS = mp.mpf("299792.458")
sig = [(100, 8.99e6), (300, 9.99e5), (1000, 8.99e4)]
k4, k4rows = True, []
for s, hand in sig:
    r = (C_KMS / s) ** 2
    k4rows.append({"sigma_kms": s, "rho_d_over_rho_DE_min": float(r)})
    k4 = k4 and within(r, hand)
    P(f"  eta = -1: a wall stops only where rho_d / rho_DE >= (c/sigma)^2 = {float(r):.4g} at sigma = {s} km/s")
res["K4"] = k4rows
check("K4 eta = -1, kappa-independent", "stop densities 8.99e6, 9.99e5, 8.99e4 rho_DE at 100, 300, 1000 km/s within 1 %; "
      "the K3 bound applies unchanged for the step not to exceed the law's own wall pressure",
      k4 and all(abs(B[n]["minus1"] - B[n]["plus1"]) < 1e-12 for n, *_ in GATES))

k5 = all(within(B[n]["plus1_over_f"], hk5) for n, _, _, _, hk5 in GATES)
check("K5 eta = +1/f", f"kappa_min rises by 1/sqrt(f) = {float(1 / mp.sqrt(F_ALLOW)):.4f}: 34.2 (G-M) and 920 (G-D) within 1 %",
      k5 and within(1 / mp.sqrt(F_ALLOW), 6.58))

# ---------------- K6: the action as frozen has eta = 0 ----------------
g_, a0_, p_, K_ = sp.symbols("g a0 p K", positive=True)
J_sym = (a0_ ** 2 / (4 * sp.pi * G)) * (g_ / a0_ - sp.log(1 + g_ / a0_))
W_sym = (a0_ ** 2 / K_) * (-p_ / a0_ - sp.log(1 - p_ / a0_))
check("K6 the frozen action has eta = 0", f"J(0) = {J_sym.subs(g_, 0)} (SWT1), W(0) = {W_sym.subs(p_, 0)} (TPA1); "
      "Lambda sits outside the switch in TPA1's frozen Lagrangian (read, criteria line 19)",
      J_sym.subs(g_, 0) == 0 and W_sym.subs(p_, 0) == 0)

# ---------------- identity checks ----------------
src = open(os.path.abspath(__file__)).read()
bad = ["5." + "7888", "0." + "1727", "9." + "36e-11", "9." + "3603e-11", "1." + "13e-10", "1." + "1312e-10",
       "1." + "2e-10", "0." + "417", "0." + "465", "0." + "551"]
hits = [s_ for s_ in bad if s_ in src]
check("I1 forbidden constants", f"hits {hits}", not hits)
kmin_sym = sp.sqrt(sp.Abs(sp.simplify(Xi * kap ** 2)) / sp.Symbol("W", positive=True))
P(f"I2 symbolic: kappa_min = {kmin_sym}; it depends on eta (free unless H1 sets |eta| = 1: TRADE when continuous), on the gate y "
  "through W, and on f in the mean-matched branch. No kappa is output.")
piw = sp.nsimplify(sp.simplify(Xi * kap ** 2 / eta) / sp.pi)
check("I8 pi-weight", f"kappa_min^2 W / |eta| = {sp.simplify(Xi * kap ** 2 / eta)} = ({piw}) pi: one pi over a transcendental W; "
      "a bound, not a value", piw.is_Rational)
P("I4 no law kappa read upstream (the fitted value appears only in the last reported line).  I5 no Friedmann.  "
  "I6 footing rho_DE.  I7 classical, hbar-free.")

# ---------------- final comparison: the data window (rules section 7), downstream of every bound ----------------
W_LO, W_HI = 0.227, 0.607


def verdict_of(bd):
    exceeds = all(bd[n][br] > W_HI for n, *_ in GATES for br in ("plus1", "plus1_over_f", "minus1"))
    if bd["G-M"]["plus1"] <= W_HI:
        return "BOUND REACHES THE WINDOW"
    return "EXCLUDED" if exceeds else "CHECK FAILED"


def ystar(kappa, cx=CX):
    xi = cx / mp.mpf(kappa) ** 2
    us = mp.findroot(lambda u: Wc(u) - xi, xi + mp.log(1 + xi) + mp.mpf(1) / 2)
    return float(xi), float(us ** 2 / (1 + us))


if not MUT:
    P("\nReported, not graded (rho_DE footing; window from the rules, used only here):")
    rep = {}
    for name, *_ in GATES:
        em = W_HI ** 2 * B[name]["W"] / float(CX)
        rep[f"eta_max_{name}"] = em
        P(f"  largest |eta| the gate {name} allows at the top of the window (kappa = {W_HI}): {em:.4g}")
    for k_ in (W_LO, W_HI):
        xi_, ys_ = ystar(k_)
        rep[f"ystar_at_{k_}"] = ys_
        P(f"  kappa = {k_}: Xi = {xi_:.2f}; for eta = +1 the law is off wherever y < y* = {ys_:.1f}")
    KFIT = sp.Rational(1, 2)                                   # the fitted value, comparison only
    xi_, ys_ = ystar(float(KFIT))
    rep["Xi_at_fitted"], rep["ystar_at_fitted"] = xi_, ys_
    P(f"  at the fitted kappa = 1/2: Xi = {xi_:.2f} (16 pi = {float(16 * mp.pi):.2f}), y* = {ys_:.1f}")
    for name, *_ in GATES:
        P(f"  {name}: kappa_min / top of window = {B[name]['plus1'] / W_HI:.1f} (eta = +-1), "
          f"{B[name]['plus1_over_f'] / W_HI:.0f} (eta = +1/f)")
    res["reported"] = rep

# ---------------- verdict / controls ----------------
res["checks"] = checks
byname = {c_["name"]: c_["pass"] for c_ in checks}
if not MUT:
    v = verdict_of(B)
    ok = all(byname.values())
    if ok and v == "EXCLUDED":
        verdict = "SWITCHED VACUUM EXCLUDED; THE FREE CONSTANT STAYS OUTSIDE THE SWITCH; kappa FREE (class CLOSURE)"
        code = 0
    elif ok and v == "BOUND REACHES THE WINDOW":
        verdict, code = v, 0
    else:
        verdict, code = "CHECK FAILED", 1
else:
    P("\nMUTATE arms, one at a time (normal values: " + ", ".join(f"{n} {B[n]['plus1']:.4f}" for n, *_ in GATES) + ")")
    arms = {"MU1 Poisson 4 pi G -> 8 pi G": (dict(cpl=8), float(mp.sqrt(2))),
            "MU2 pressure step x 0.9": (dict(wfac=sp.Rational(9, 10)), float(mp.sqrt(mp.mpf("0.9")))),
            "MU3 constant outside the switch": (dict(eta_on=0), 0.0)}
    bites = {}
    for label, (kw, ratio) in arms.items():
        bm, _ = bounds(**kw)
        moved = all(abs(bm[n]["plus1"] - ratio * B[n]["plus1"]) <= 5e-3 * max(B[n]["plus1"], 1e-30) for n, *_ in GATES)
        k3_fails = not all(within(bm[n]["plus1"], hk) for n, _, _, hk, _ in GATES)
        vm = verdict_of(bm)
        bite = moved and k3_fails and (vm != "EXCLUDED" if "MU3" in label else True)
        bites[label] = {"kappa_min": {n: bm[n]["plus1"] for n, *_ in GATES}, "expected_ratio": ratio, "moved_as_stated": moved,
                        "K3_hand_check_fails": k3_fails, "verdict_rule": vm, "bites": bite}
        P(f"  {label}: kappa_min " + ", ".join(f"{n} {bm[n]['plus1']:.4f}" for n, *_ in GATES)
          + f"; moved by x{ratio:.4f} as stated: {moved}; K3 hand check fails: {k3_fails}; verdict rule gives {vm}; bites: {bite}")
    res["MUTATE"] = bites
    allb = all(b_["bites"] for b_ in bites.values())
    verdict = "CONTROLS BITE (3 of 3)" if allb else "CONTROL DID NOT BITE: lane void"
    code = 1 if allb else 2
P(f"\nVERDICT: {verdict}" + ("" if MUT else ". kappa = 1/2 FITTED; not theory closed."))
res["verdict"] = verdict
with open(os.path.join(HERE, f"w4_24_results{SUF}.json"), "w") as fh:
    json.dump(res, fh, indent=1, default=str)
sys.exit(code)
