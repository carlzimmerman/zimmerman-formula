#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CFG231_A6_solar_stability -- G5: Q2 (CFG7 H1 recipe: tide = max(|dg/dR|, g/R); isolated Sun at Saturn and the Milky-Way tide at the Sun), the
FC-KH control, the DE12/DE13 gate statement for B3, gamma and c_T statements; controls C7; MUTATE MU2, MU3, MU6, MU7.
Frozen: CFG231_FROZEN_CRITERIA.md sections 2 (G5), 4, 6.
Main run: exit 0 if the reproduction controls pass (verdicts are results).  MUTATE: exit 1 iff the control bites (named headline differs), else 0.
"""
import sys, os, math
import numpy as np
import sympy as sp
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import CFG231_common as C

MUT = os.environ.get("MUTATE") or None
R = C.Report("CFG231_A6_solar_stability", MUT)
C.header(R, "CFG231 A6 -- G5: Q2, stability control, gate statement, gamma and c_T")

GMSUN = 1.32712440018e20              # m^3/s^2
AU = 1.495978707e11
KPC = C.KPC_M
Q2B = 5.2e-27                          # s^-2 (gate 4.01, 2 sigma)
RSAT = 9.54 * AU
PSI_SI = {"K1": lambda g, a: np.sqrt(g ** 2 + a * g) - g, "K2": lambda g, a: np.sqrt(a * g), "K3": lambda g, a: 0.5 * (np.sqrt(g ** 2 + 4 * a * g) - g)}


def tide(gfun, R0, eps=1e-3):
    dg = (gfun(R0 * (1 + eps)) - gfun(R0 * (1 - eps))) / (2 * R0 * eps)
    return max(abs(dg), abs(gfun(R0)) / R0)


# ------------------------------------------------------------------------------------------------------ FC-KH control
R.banner("C-FCKH  the stability-evaluator control: (y q)' for mu = 1 - e^{-y} and for mu = y/(1+y) (q = 1 - mu)")
y = sp.symbols("y", positive=True)
q1 = sp.exp(-y); q2 = 1 / (1 + y)
d1 = sp.simplify(sp.diff(y * q1, y)); d2 = sp.simplify(sp.diff(y * q2, y))
R.P(f"  mu = 1 - e^-y: (y q)' = {d1}  -> negative for y > 1: {bool(d1.subs(y, 2) < 0)};   mu = y/(1+y): (y q)' = {d2} > 0 for all y")
R.check("C-FCKH (y q)' = (1-y) e^{-y} < 0 for y > 1 (exponential kernel) and 1/(1+y)^2 > 0 (y/(1+y)), reproducing CFG172's control before scoring",
        f"{d1}; {d2}", sp.simplify(d1 - (1 - y) * sp.exp(-y)) == 0 and sp.simplify(d2 - 1 / (1 + y) ** 2) == 0)

# ------------------------------------------------------------------------------------------------------ Q2
a_var = {"K1": C.a_V_si("HL"), "K2": C.a_V_si("HL"), "K3": C.a_V_si("HL")}
a0c = C.A0_SI["canonical"]


def Q2_sun(law, a):
    E = lambda RR: PSI_SI[law](GMSUN / RR ** 2, a)
    return dict(E=float(E(RSAT)), tide=tide(E, RSAT), ratio=tide(E, RSAT) / Q2B)


R.banner("C7  Q2 recipe control: the isolated-Sun tail of the P2 law (K1 with a = a0 canonical) at Saturn: E -> a0/2, Q2/bound ~ 6.3e3 (CFG172's tail figure)")
c7 = Q2_sun("K1", a0c)
R.P(f"  E(Saturn) = {c7['E']:.4e} m/s^2 (a0/2 = {a0c / 2:.4e});  tide = {c7['tide']:.3e} s^-2;  tide/bound = {c7['ratio']:.3e}")
R.check("C7 Q2 recipe: the P2 tail at Saturn gives tide/bound = 6.3e3 to 3% (CFG172 [R]; the frozen hand value)", f"{c7['ratio']:.3e}", abs(c7["ratio"] / 6.3e3 - 1) < 0.03)

R.banner("G5 Q2 (a) isolated Sun at Saturn (9.54 AU), a = a_V(H_Lambda) unless stated; the gate is tide/bound <= 1")
q2s = {}
for law in ("K1", "K2", "K3"):
    q2s[law] = Q2_sun(law, a_var[law])
    R.P(f"  {law}: E(Saturn) = {q2s[law]['E']:.3e} m/s^2; tide = {q2s[law]['tide']:.3e} s^-2; tide/bound = {q2s[law]['ratio']:.3e}")
q2s["K1_alt"] = Q2_sun("K1", C.A0_SI["alt"])
R.P(f"  K1 (a = a0 alt): tide/bound = {q2s['K1_alt']['ratio']:.3e}")
gN_sat = GMSUN / RSAT ** 2
R.P(f"  g_N(Saturn) = {gN_sat:.3e} m/s^2; B3's onset gate switches the dark force off where g_N > 3 a_V = {3 * C.a_V_si('HL'):.3e}: dark force ON at Saturn: {gN_sat < 3 * C.a_V_si('HL')}  -> E = 0, tide = 0 (passes only by the unvaried mask)")
q2s["B3"] = dict(E=0.0, tide=0.0, ratio=0.0)
# B1 in the Sun: point mass -> same as K2 (rho_b = 0 at Saturn)
q2s["B1"] = q2s["K2"]
# B4: total-mass reading: g_tot = sqrt(a g_N): the Newtonian force is removed
B4E = lambda RR: math.sqrt(C.a_V_si("HL") * GMSUN / RR ** 2) - GMSUN / RR ** 2
q2s["B4"] = dict(E=B4E(RSAT), tide=tide(B4E, RSAT), ratio=tide(B4E, RSAT) / Q2B)
R.P(f"  B4 (total-mass reading): g_tot/g_N at Saturn = {math.sqrt(C.a_V_si('HL') / gN_sat):.3e}: the Newtonian force is removed (anomalous acceleration = {B4E(RSAT):.3e}); tide/bound = {q2s['B4']['ratio']:.2e}")
R.P("  V0: the anomalous force eps g_N is a 1/R^2 central force = a rescaling of G M_sun: degenerate with the measured GM (no quadrupole beyond the Newtonian tide): Solar-System p* (it is not an a0 law); its gamma/EP consequences are not scored.")
q2s["V0"] = dict(E=GMSUN / RSAT ** 2, tide=float("nan"), ratio=float("nan"))
R.num("Q2_isolated_sun", q2s)

R.banner("G5 Q2 (b) the Milky-Way tide at the Sun (CFG7 H1's standard MW baryon budget [D]; no EFE)")
MD, RD, MBUL, ABUL, MGAS, RGAS = 4.5e10, 2.6, 0.9e10, 0.5, 1.2e10, 5.0
R0 = 8.2 * KPC


def Mexp(Md, Rd, RR):
    x = RR / (Rd * KPC)
    return Md * (1 - (1 + x) * math.exp(-x))


def gN_MW(RR):
    M = Mexp(MD, RD, RR) + Mexp(MGAS, RGAS, RR) + MBUL * (RR / KPC) ** 2 / (RR / KPC + ABUL) ** 2
    return 6.6743e-11 * M * 1.98847e30 / RR ** 2


q2m = {}
for law in ("K1", "K2", "K3"):
    E = lambda RR, law=law: PSI_SI[law](gN_MW(RR), a_var[law])
    t_ = tide(E, R0, eps=1e-2)
    q2m[law] = dict(g_N=gN_MW(R0), E=float(E(R0)), tide=t_, ratio=t_ / Q2B)
    R.P(f"  {law}: g_N,MW(R0) = {gN_MW(R0):.3e}, E = {E(R0):.3e} m/s^2; tide = {t_:.3e} s^-2; tide/bound = {t_ / Q2B:.3e}  (P2 phantom: CFG7 H1 reports margin >= 1e3 i.e. tide/bound <= 1e-3)")
R.num("Q2_MW", q2m)
R.P("  (with this budget the MW baryons' Newtonian field at the Sun is ~1.06e-10 m/s^2, g_N/a ~ 1.2; the MW phantom tide is far below the bound for all three laws)")

# ------------------------------------------------------------------------------------------------------ gate statement
R.banner("G5 (iii) B3's onset gate: DE12/DE13 structural statement (a smooth on/off gate flat at both ends has W'' of both signs), sympy")
u = sp.symbols("u")
W = 3 * u ** 2 - 2 * u ** 3                             # the standard smoothstep: W' = 0 at u = 0 and 1
W2 = sp.diff(W, u, 2)
sign_change = bool(W2.subs(u, sp.Rational(1, 4)) > 0 and W2.subs(u, sp.Rational(3, 4)) < 0)
R.P(f"  W(u) = {W}; W'(0) = {sp.diff(W, u).subs(u, 0)}, W'(1) = {sp.diff(W, u).subs(u, 1)}; W'' = {sp.expand(W2)} (>0 on u < 1/2, <0 on u > 1/2)")
R.P("  a smooth gate flat at both ends therefore has a wrong-sign second variation on half of every transition layer [R: DE12/DE13; CFG172 sec. 0.5]. B3's onset gate is a SHARP mask (an unvaried mask, the V0 obstruction): stable only because nothing varies it; varied as a term it meets this statement. Scored as a statement.")
R.check("gate statement: the smoothstep W has W'(0) = W'(1) = 0 and W'' of both signs (the DE12 structure), sympy", f"W'' = {sp.expand(W2)}", sign_change)

# ------------------------------------------------------------------------------------------------------ statements
R.banner("G5 (iv) c_T = c and gamma (statements)")
R.P("  c_T = c: the class-V action is minimally coupled (no A^mu A^nu R_mu nu, no xi R A^2): the tensor sector is GR's, c_T = 1 [H, statement; P]. Non-minimal couplings are NOT covered.")
R.P("  gamma: the drag force acts on baryons as a potential force and leaves the metric unmodified at this order: gamma - 1 = 0 (Cassini P) [H, statement]; but the SAME statement means the vector force does not deflect light (lensing versus dynamics, diagnostic D2: not scored).")
R.P("  ghost: A3.1-A3.2 show that the attractive drag needs s = -1 (a ghost) for V0, V1 (K1, K2, K3); V2's dark mass is negative (A3.4).")

# ------------------------------------------------------------------------------------------------------ verdict table
R.banner("G5 verdicts per variant (Q2 (a) isolated Sun, Q2 (b) MW tide, stability, gate, statements)")
verd = {}
for law in ("K1", "K2", "K3"):
    verd[law] = dict(Q2_sun=f"FAIL x{q2s[law]['ratio']:.2e}", Q2_MW=("pass" if q2m[law]["ratio"] <= 1 else f"FAIL x{q2m[law]['ratio']:.2e}"), stability="FAIL (ghost sign for attraction; frozen (i) D'>0, D/E>0 hold)", cT="P", gamma="P")
verd["B1"] = dict(Q2_sun=f"FAIL x{q2s['B1']['ratio']:.2e}", Q2_MW=verd["K2"]["Q2_MW"], stability="as K2 (no action: UNDEFINED; the vector reading is a ghost)", cT="P", gamma="P")
verd["B2"] = verd["K2"]
verd["B3"] = dict(Q2_sun="pass by the gate (E = 0 at the Sun)", Q2_MW=f"pass (gate ON at the MW Sun position, tide/bound {q2m['K2']['ratio']:.1e} as B1)", stability="sharp mask: unvaried; a varied gate meets DE12/DE13 (statement)", cT="P", gamma="P")
verd["B4"] = dict(Q2_sun=f"FAIL (Newtonian force removed; x{q2s['B4']['ratio']:.1e})", Q2_MW="n/a", stability="UNDEFINED (no action)", cT="P", gamma="FAIL (g_tot != g_N)")
verd["V0"] = dict(Q2_sun="p* (degenerate with GM)", Q2_MW="p*", stability="FAIL (ghost sign)", cT="P", gamma="p*")
verd["V2"] = dict(Q2_sun="p* (dark mass ~1e-6 of the needed; nothing to test)", Q2_MW="p*", stability="FAIL (ghost sign; negative dark mass)", cT="P", gamma="P")
for k, v in verd.items():
    R.P(f"  {k:3s}: Q2(a) {v['Q2_sun']}; Q2(b) {v['Q2_MW']}; stability {v['stability']}; c_T {v['cT']}; gamma {v['gamma']}")
R.num("G5_table", verd)
# B3 at the MW: is the gate ON at the Sun's location in the MW?
R.P(f"  B3 gate at the MW Sun position: g_N,MW = {gN_MW(R0):.3e} vs 3 a_V = {3 * C.a_V_si('HL'):.3e} -> gate {'ON (E != 0)' if gN_MW(R0) < 3 * C.a_V_si('HL') else 'OFF'}")

# ------------------------------------------------------------------------------------------------------ MUTATE
bites = None
if MUT:
    R.banner(f"MUTATE {MUT}")
    if MUT == "MU2":
        # area-law only: the volume term is absent, a_V -> 0
        Q2_main = q2s["K1"]["ratio"]
        E0 = lambda RR: PSI_SI["K1"](GMSUN / RR ** 2, 0.0)
        Q2_mut = tide(E0, RSAT) / Q2B
        pm = C.G1_cell("K1", "point", 1e10, 0.0, "tie_canonical")
        pm_main = C.G1_cell("K1", "point", 1e10, C.a_V_si("HL"), "tie_canonical")
        R.P(f"  K1 Q2/bound: main {Q2_main:.3e} -> a_V = 0: {Q2_mut:.3e};  G1 point mass (N-tie canonical): main max|R-1| = {pm_main['maxdev']:.3g} (pass {pm_main['pass_strict']}) -> a_V = 0: max|R-1| = {pm['maxdev']:.3g} (pass {pm['pass_strict']})")
        bites = (Q2_main > 1) and (Q2_mut <= 1) and (not pm["pass_strict"])
        R.P(f"  bites = {bites}: the Q2 cell flips F -> P and G1 stays F (R = 0)")
    elif MUT == "MU3":
        # healthy sign: repulsive: g_tot = g_N - E, M_D = -r^2 E/G
        a = C.AKPC(C.a_V_si("HL")); a0t = a
        M = 1e10
        rM = C.r_M_kpc(M, a0t); r = C.XGRID * rM
        prof = C.PointMass(M); gN = C.gN_of(prof, r)
        MD = lambda rr: -rr ** 2 * C.psi_K1(C.gN_of(prof, rr), a) / C.G
        rho = C.ddr(MD, r) / (4 * math.pi * r ** 2)
        gtot = C.G * (prof.Mb(r) + MD(r)) / r ** 2
        Rm = 4 * math.pi * r ** 3 * rho * gtot / (a0t * M)
        R.P(f"  healthy (s = +1) sign: the K1 drag becomes REPULSIVE: R(x) at x = 0.1, 1, 10, 30 = {[round(float(Rm[int(np.argmin(np.abs(C.XGRID - x)))]), 4) for x in (0.1, 1, 10, 30)]}; g_tot < g_N: {bool(np.all(gtot < gN))}")
        stab_main, stab_mut = "ghost (F)", "healthy (P: s D' > 0, s D/E > 0)"
        R.P(f"  stability cell: main {stab_main} -> mutated {stab_mut}  (the frozen prediction said P -> F: WRONG direction, kept: the main run is already a ghost)")
        G1_main = C.G1_cell("K1", "point", 1e10, C.a_V_si("HL"), "shape")["pass_strict"]
        G1_mut = bool(np.all(np.abs(Rm - 1) <= 0.1))
        R.P(f"  G1 point mass N-shape strict: main {G1_main} -> mutated {G1_mut}")
        bites = G1_main and (not G1_mut)
        R.P(f"  bites = {bites} (G1 flips P -> F by sign); the frozen stability-cell expectation (P -> F) is contradicted: the cell moves F -> P")
    elif MUT == "MU6":
        gate_on_Q2 = q2s["B3"]["ratio"]; gate_off_Q2 = q2s["B1"]["ratio"]
        cB3 = C.G1_cell("B3", "point", 1e10, C.a_V_si("HL"), "shape", Hgate_si=6 * C.a_V_si("HL"))
        cB1 = C.G1_cell("B1", "point", 1e10, C.a_V_si("HL"), "shape")
        R.P(f"  gate ON (B3) -> OFF (B1): Q2/bound {gate_on_Q2:.1e} -> {gate_off_Q2:.1e};  G1 R(x = 0.1) point mass {cB3['R_at'][0]:.3g} -> {cB1['R_at'][0]:.3g}")
        bites = (gate_on_Q2 <= 1) and (gate_off_Q2 > 1) and (cB3["R_at"][0] < 0.9) and (cB1["R_at"][0] > 1.1)
        R.P(f"  bites = {bites}")
    elif MUT == "MU7":
        cK1 = C.G1_cell("K1", "point", 1e10, C.a_V_si("HL"), "shape")
        cV2 = C.G1_cell("V2", "point", 1e10, C.a_V_si("HL"), "shape")
        R.P(f"  V1/K1 drag reading: max|R-1| = {cK1['maxdev']:.2e} (pass {cK1['pass_strict']}); V2 gravitating reading: max|R-1| = {cV2['maxdev']:.6f} (R at x = 0.1, 1, 10, 30: {[f'{t:.1e}' for t in cV2['R_at'][:1] + cV2['R_at'][1:2] + cV2['R_at'][3:]]}; pass {cV2['pass_strict']})")
        bites = cK1["pass_strict"] and (not cV2["pass_strict"])
        R.P(f"  bites = {bites}")
    R.num("bites", bool(bites))

if not MUT:
    nf = R.write()
    sys.exit(0 if nf == 0 else 1)
R.write()
sys.exit(1 if bites else 0)
