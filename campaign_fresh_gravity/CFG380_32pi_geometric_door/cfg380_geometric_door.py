#!/usr/bin/env python3
"""CFG380 -- 32pi geometric door. Criteria: FROZEN_CRITERIA.md (committed first).

Units c = G = 1. Every candidate acceleration is written a = C * sqrt(Lambda); the target is
T = 1/sqrt(32 pi) (a0 = c^2 sqrt(Lambda/(32 pi)), i.e. G rho_Lambda = 4 a0^2, kappa = 1/2 FITTED).

Routes R1-R6 as declared. Checks C1-C6 can fail; exit 1 on any failure.
MUTATE (CFG380_MUTATE=1): wrong Nariai mass (Lambda -> 3 Lambda), C2 must fail; outputs *_MUTATE.*.
"""
import json, os, sys
import sympy as sp

MUT = os.environ.get("CFG380_MUTATE") == "1"
tag = "_MUTATE" if MUT else ""
here = os.path.dirname(os.path.abspath(__file__))

L, r, m, l = sp.symbols("Lambda r m ell", positive=True)
T = 1 / sp.sqrt(32 * sp.pi)
Tf = float(T)
checks = {}

# ---------------- R1: Penrose-type mass-area relation with Lambda ----------------
# SdS: f = 1 - 2m/r - Lambda r^2/3; horizon relation m(r) = (r - Lambda r^3/3)/2.
f = 1 - 2 * m / r - L * r**2 / 3
m_h = sp.solve(sp.Eq(f, 0), m)[0]
# C1: AdS continuation Lambda = -3/l^2 gives item 260's M = (r + r^3/l^2)/2 (l = 1 there: (r_h + r_h^3)/2).
checks["C1_AdS_continuation"] = sp.simplify(m_h.subs(L, -3 / l**2) - (r + r**3 / l**2) / 2) == 0
# C2: Nariai (extremal) point.
rN = sp.solve(sp.Eq(sp.diff(m_h, r), 0), r)[0]
mN = sp.simplify(m_h.subs(r, rN))
if MUT:
    mN = sp.simplify(m_h.subs(L, 3 * L).subs(r, rN))  # wrong horizon relation
checks["C2_Nariai"] = bool(sp.simplify(rN - 1 / sp.sqrt(L)) == 0 and sp.simplify(mN - 1 / (3 * sp.sqrt(L))) == 0)

rc = sp.sqrt(3 / L)  # pure de Sitter cosmological horizon
cands = []
def add(route, name, a_expr, note):
    C = sp.nsimplify(sp.simplify(a_expr / sp.sqrt(L)))
    cands.append(dict(route=route, name=name, C_exact=str(C), C=float(C), has_pi=bool(sp.sympify(C).has(sp.pi)),
                      miss=abs(float(C) / Tf - 1), ratio=float(C) / Tf, note=note))

add("R1", "Nariai G m_N / r_N^2", mN / rN**2, "extremal SdS hole (max of the Penrose relation)")
add("R1", "Nariai c^2 / r_N", 1 / rN, "")
add("R1", "Nariai c^2 / (2 r_N) (Schwarzschild-type surface gravity)", 1 / (2 * rN), "")
add("R1", "dS horizon surface gravity (f-normalised)", sp.Abs(sp.diff(1 - L * r**2 / 3, r) / 2).subs(r, rc), "")

# ---------------- R2: quasi-local masses on the cosmological horizon ----------------
# Lambda-modified Hawking mass of a round sphere: m_HL = sqrt(A/16pi)(1 - W/16pi - Lambda A/(12 pi)), W = oint H^2 dA.
A = 4 * sp.pi * r**2
H2 = 4 * f / r**2               # mean curvature^2 of round sphere in static slice (time-symmetric)
W = H2 * A
mHL = sp.sqrt(A / (16 * sp.pi)) * (1 - W / (16 * sp.pi) - L * A / (12 * sp.pi))
checks["C3_LambdaHawking_equals_m"] = sp.simplify(mHL - m) == 0
checks["C3b_pure_dS_zero"] = sp.simplify(mHL.subs(m, 0)) == 0
# Plain Hawking (= Misner-Sharp) mass with Lambda ignored, pure dS:
mH = sp.sqrt(A / (16 * sp.pi)) * (1 - W / (16 * sp.pi))
mH_dS = sp.simplify(mH.subs(m, 0))             # = Lambda r^3/6
add("R2", "Hawking/Misner-Sharp mass at r_c: G m / r_c^2", sp.simplify(mH_dS.subs(r, rc) / rc**2), "m = r_c/2")
# Brown-York, flat reference, pure dS: E = r(1 - sqrt(f)); at r_c, f = 0.
EBY = r * (1 - sp.sqrt(1 - L * r**2 / 3))
add("R2", "Brown-York energy at r_c: G E / r_c^2", sp.simplify(EBY.subs(r, rc) / rc**2), "E = r_c")
# (Lambda-Hawking mass: identically 0 in pure dS -> NO scale; recorded, no coefficient.)

# ---------------- R3: area bounds with Lambda > 0 (puzzle convention a = sqrt(pi/A)) ----------------
add("R3", "HGW/Nariai bound Lambda A <= 4 pi, a = sqrt(pi/A)", sp.sqrt(sp.pi / (4 * sp.pi / L)), "")
add("R3", "Boucher-Gibbons-Horowitz A_c <= 12 pi/Lambda, a = sqrt(pi/A)", sp.sqrt(sp.pi / (12 * sp.pi / L)), "")
need_A = sp.simplify(sp.pi / (T**2 * L))  # area the puzzle needs
checks_needA = str(need_A)

# ---------------- R4: Einstein 4-manifolds Ric = Lambda g (item 348) ----------------
# Volumes (Ric = Lambda g): S^4 radius sqrt(3/L): (8pi^2/3) R^4; RP^4 half; CP^2 (FS, Ric=6g has vol pi^2/2) scaled by 6/L;
# S^2 x S^2 radii 1/sqrt(L).
mani = {
    "S4":    dict(V=sp.Rational(8, 3) * sp.pi**2 * (3 / L)**2, chi=2, radii=[sp.sqrt(3 / L)]),
    "RP4":   dict(V=sp.Rational(4, 3) * sp.pi**2 * (3 / L)**2, chi=1, radii=[sp.sqrt(3 / L)]),
    "CP2":   dict(V=sp.pi**2 / 2 * (6 / L)**2, chi=3, radii=[sp.sqrt(6 / L), sp.sqrt(sp.Rational(3, 2) / L)]),
    "S2xS2": dict(V=(4 * sp.pi / L)**2, chi=4, radii=[1 / sp.sqrt(L)]),
}
gb = {}
for k, d in mani.items():
    lhs = sp.simplify(L**2 * d["V"]); rhs = 12 * sp.pi**2 * d["chi"]
    gb[k] = (str(lhs), str(rhs))
    conf_flat = k in ("S4", "RP4")
    ok = sp.simplify(lhs - rhs) == 0 if conf_flat else bool(float(lhs) < float(rhs))
    checks[f"C4_GaussBonnet_{k}"] = ok
    for R in d["radii"]:
        add("R4", f"{k} curvature radius c^2/R (R={sp.simplify(R*sp.sqrt(L))}/sqrt(L))", 1 / R, "")
    add("R4", f"{k} c^2 / Vol^(1/4)", 1 / d["V"]**sp.Rational(1, 4), "the only way a pi enters")
    add("R4", f"{k} sqrt(pi / Vol^(1/2)) (puzzle area convention)", sp.sqrt(sp.pi / sp.sqrt(d["V"])), "")

# ---------------- R5: SCC threshold beta = 1/2 (Lambda > 0) ----------------
add("R5", "reading a0 = (1/2) kappa_c (SCC beta = 1/2 x dS surface gravity) [CHOSEN reading]",
    sp.Rational(1, 2) * sp.sqrt(L / 3), "beta is alpha/kappa_-, not a0/kappa_c: the map is a choice")

# ---------------- positive control for the null ----------------
pos_control = dict(route="CTRL", name="artificial T(1+0.001)", C=Tf * 1.001, miss=0.001)

# ---------------- base-rate null ----------------
fam = set()
for p in range(1, 13):
    for q in range(1, 13):
        for n in range(-2, 3):
            v = (p / q) * float(sp.pi)**n
            fam.add(round(v, 12)); fam.add(round(v**0.5, 12))
fam = sorted(fam)
N = len(fam)
checks["C5_T_not_in_family"] = all(abs(v / Tf - 1) > 1e-9 for v in fam)
def pbase(delta):
    return sum(1 for v in fam if abs(v / Tf - 1) <= delta) / N
p1 = pbase(0.01)
p_ctrl = pbase(pos_control["miss"])

# ---------------- verdicts (generated, C6) ----------------
for c in cands:
    c["p_base"] = pbase(c["miss"])
    forced_reading = False  # no route forces WHICH acceleration is a0 (Q2); see README
    if c["miss"] <= 0.01 and forced_reading and c["p_base"] < 0.01:
        v = "FORCED"
    elif c["miss"] <= 0.05:
        v = "NUMEROLOGY"
    else:
        v = "CHOSEN"
    c["Q1_derives_a0"] = "no (a0 is identified with a Lambda-geometry acceleration by hand)"
    c["Q2_forced"] = "reading chosen; coefficient then fixed by geometry" if c["route"] != "R5" else "chosen"
    c["Q3_base_rate"] = f"p_base={c['p_base']:.3f}"
    c["verdict"] = v
routes_NA = {"R6": "items 360/374 (MTW convexity, Brenier 1/3-Holder stability): no Lambda, no acceleration, no G -> NOT APPLICABLE",
             "R5_item264": "item 264 itself is Lambda = 0 Kerr SCC: no scale -> NOT APPLICABLE (the Lambda>0 beta=1/2 reading is R5 above)"}
checks["C6_verdicts_generated"] = all("verdict" in c for c in cands) and len(cands) >= 15
checks["C7_null_can_flag"] = p_ctrl < 0.01  # null is not blind

# summary
best = min(cands, key=lambda c: c["miss"])
any_pi_free_hit = any((not c["has_pi"]) and c["miss"] < 1e-12 for c in cands)
lines = []
lines.append(f"CFG380 geometric door {'(MUTATE)' if MUT else ''}")
lines.append(f"target T = 1/sqrt(32 pi) = {Tf:.6f}; puzzle needs A = {checks_needA} (vs Nariai 4pi/L, BGH 12pi/L)")
lines.append(f"base-rate family: {N} distinct forms; 1%-window fraction = {p1:.4f}; positive control (0.1%) p = {p_ctrl:.4f}")
lines.append(f"{'route':5s} {'C':>9s} {'C/T':>7s} {'pi?':>4s} {'p_base':>7s}  verdict     name")
for c in sorted(cands, key=lambda c: c["miss"]):
    lines.append(f"{c['route']:5s} {c['C']:9.5f} {c['ratio']:7.3f} {('yes' if c['has_pi'] else 'no'):>4s} {c['p_base']:7.3f}  {c['verdict']:10s}  {c['name']}  [{c['C_exact']}]")
lines.append("R2 Lambda-modified Hawking mass: identically 0 in pure dS (C3b) -> supplies NO scale")
for k, v in routes_NA.items():
    lines.append(f"{k}: {v}")
lines.append("Gauss-Bonnet Einstein checks Lambda^2 Vol vs 12 pi^2 chi: " + json.dumps(gb))
lines.append(f"closest candidate: {best['name']} C/T = {best['ratio']:.3f} (miss {best['miss']*100:.0f}%)")
lines.append(f"any exact hit: {any_pi_free_hit}")
lines.append("checks: " + json.dumps(checks))
allok = all(checks.values())
lines.append("ALL CHECKS PASS" if allok else "SOME CHECKS FAIL")
lines.append("kappa = 1/2 stays FITTED.")
out = "\n".join(lines)
print(out)
open(os.path.join(here, f"cfg380_geometric_door{tag}.out"), "w").write(out + "\n")
json.dump(dict(target=Tf, family_size=N, p_1pct=p1, candidates=cands, not_applicable=routes_NA,
               gauss_bonnet=gb, checks=checks), open(os.path.join(here, f"cfg380_results{tag}.json"), "w"), indent=1)
sys.exit(0 if allok else 1)
