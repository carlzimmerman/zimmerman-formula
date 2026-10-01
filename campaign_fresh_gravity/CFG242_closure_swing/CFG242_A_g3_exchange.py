#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
CFG242_A_g3_exchange -- route A (L14a), G3: reciprocity and energy of the latch-gated exchange (frozen plan section 4.2, gate order 3 and 4).

FROZEN (shared G3, verbatim): 'The reaction on the baryons <= 0.10 g_law over x in [0.3, 30] and the energy the mechanism must supply <= the baryons'
orbital energy, in BOTH r_ta conventions (CFG48 G4's pass lines).'  Two readings, NEVER pooled (the amended G3, declared in the frozen file):
  STRICT  (every arm): the shared line as written.  Arm A1 (iota = 0, r = 1, tau_bar free) is the strict arm; its stop is G3 strict.
  FUNDED  (A2, A3 only; a declared departure, labelled in every output): reaction <= 0.10 g_law over x in [0.3, 30] with the reservoir identified
          inside the action, energy <= the vacuum energy available in the causal region (a c t_f ball), and |delta a0/a0| <= 1%.
          A funded pass is 'a pass of the amended G3', never of the shared G3.
Order in the frozen plan: G0 legality (CFG242_A_g0_legality.py) came first for A2/A3 and FAILED there (B3), so under the stop rule arms A2 and A3
STOP at G0 and the FUNDED reading below is a POST-HOC CONTINUATION (labelled), run for information on the frozen equations E1-E4 with the E3
defect set aside; the STRICT reading on arm A1 is the arm's own gate and is a MAIN result.

MODEL.  Closed forms of the retarded exchange (derived in CFG70 by sympy; reproduced as controls in CFG242_A_controls.py): a/theta^T_M(t) = r Theta_K(t)
 + eps_c (Thetabar * mdot)(t), Theta_K = int_0^t K, K = exp(-s/tau_bar)/tau_bar, Thetabar = 1 - Theta_K, m(t) = smoothstep(t/t_f); reaction on the
 baryons a = theta^T_M(u) x that ratio, theta^T_M = (3/4) a0 (pressure-slaved) or (3/8) a0 (2+x^2)/(1+x^2) (sigma-slaved).  eps_c = c theta^T_full is the
 free-energy stiffness in units of the full target; the frozen file does not fix it: it is declared at CFG70's N6 value eps_c = 1 (a DEPARTURE, disclosed; any
 other value is a new constant).  tau_bar = tau_L = 1/(kappa sqrt(G rho_Lambda)) (tied; computed from the tie, about 101 Gyr canonical).
 Ledger: E_c(<r_e) = 1.5 (r_e/r_M) (1/2) M_b V_f^2 (V_f^4 = G M_b a0, r_e = 0.4 r_ta) against the vacuum energy rho_Lambda c^2 (4 pi/3) r_e^3 of the ball
 the heat is drawn from; the local a0 shift is (1/2) E_c / E_vac (a0 proportional to sqrt(rho_Lambda)).
MUTATE: MA3 drops the reaction partner (the baryons feel no reaction): the FUNDED reaction cell flips FAIL -> trivially PASS (and CFG242_A_g0_legality's
 symmetry cell fails).  MA5 removes the vacuum ledger (an unfunded reservoir): the FUNDED ledger cell flips to UNDEFINED.
"""
import os, sys, math
sys.dont_write_bytecode = True
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import CFG242_common as C

R = C.Run("CFG242_A_g3_exchange")
P = R.P
MUT = R.mutate
P(__doc__.strip())
C7 = C.load_c7()
XG = np.geomspace(0.3, 30.0, 400)


def react(x, kind):
    if kind == "P":
        return 0.75 * x * x / np.sqrt(1 + x * x)
    return 0.375 * (2 + x * x) / (1 + x * x) * x * x / np.sqrt(1 + x * x)


# ---------------------------------------------------------------------------------------------------- STRICT, arm A1 (main)
R.banner("G3 STRICT, arm A1 (iota = 0, r = 1; kernel-independent late-time limit)  [MAIN]")
rows = {}
for kind in ("P", "S"):
    rr = react(XG, kind)
    x_cross = float(XG[np.argmax(rr > 0.10)])
    rows[kind] = dict(max=float(rr.max()), at_x30=float(react(30.0, kind)), x_cross=x_cross)
    P(f"    {kind}-slaved: max over x in [0.3, 30] of reaction/g_law = {rr.max():.2f} (at x = 30); crosses the 0.10 line at x = {x_cross:.3f}")
react_strict = all(v["max"] <= 0.10 for v in rows.values())
R.check("G3 STRICT reaction <= 0.10 g_law over x in [0.3, 30] (A1: r = 1, any kernel)", react_strict,
        f"pressure-slaved max {rows['P']['max']:.2f}, sigma-slaved {rows['S']['max']:.2f}; line crossed at x = {rows['P']['x_cross']:.2f} / {rows['S']['x_cross']:.2f}", kind="result")
en = {}
for Mb in C.MASSES:
    rM = C.r_M_kpc(Mb)
    e48 = 1.5 * 0.4 * C.r_ta48_kpc(Mb) / rM
    eB = 1.5 * 0.4 * 1e3 * float(C7.r_ta_law(Mb, C7.A0["canonical"], C7.nu_mono, 1.0)) / rM
    en[f"{Mb:.0e}"] = dict(CFG48=e48, B_committed=eB)
    P(f"    M_b {Mb:.0e}: energy the exchange must supply / (1/2 M_b V_f^2): CFG48 r_ta {e48:7.1f}, B's committed r_ta {eB:7.1f}")
energy_strict = all(v["CFG48"] <= 1 and v["B_committed"] <= 1 for v in en.values())
R.check("G3 STRICT energy <= the baryons' orbital energy in BOTH r_ta conventions", energy_strict,
        f"min ratio {min(min(v.values()) for v in en.values()):.1f} (every ratio exceeds 1 by >= 23x)", kind="result")
R.num("strict", dict(reaction=rows, energy=en))
R.verdict("G3 strict (arm A1)", "FAIL" if not (react_strict and energy_strict) else "PASS",
          f"reaction {rows['P']['max']:.1f} g_law (line 0.10) and energy {min(v['CFG48'] for v in en.values()):.0f}-{max(v['B_committed'] for v in en.values()):.0f} x orbital (line 1)")

# ---------------------------------------------------------------------------------------------------- FUNDED, continuation (post-hoc)
R.banner("G3 FUNDED reading, arms A2/A3 [POST-HOC CONTINUATION: the arms stopped at G0]: r = 0, eps_c = 1, tau_bar = tau_L")
P(f"    tau_L = 1/(kappa sqrt(G rho_Lambda)) = {C.TAU_L_GYR:.1f} Gyr (canonical tie; rho_Lambda = {C.RHO_L:.2f} Msun/kpc^3);  age {C.T0_GYR} Gyr")


def peak_ratio(tau_bar, t_f, eps_c=1.0, n=40001):
    """max_t eps_c (Thetabar * mdot)(t): convolution of exp(-s/tau_bar) with mdot = d smoothstep(t/t_f)/dt (6u(1-u)/t_f on [0,t_f])."""
    T = max(t_f * 3.0, min(tau_bar * 3.0, 400.0))
    t = np.linspace(0, T, n)
    dt = t[1] - t[0]
    u = np.clip(t / t_f, 0, 1)
    md = np.where(t <= t_f, 6 * u * (1 - u) / t_f, 0.0)
    y = np.zeros(n); acc = 0.0
    decay = math.exp(-dt / tau_bar)
    for i in range(1, n):
        acc = acc * decay + 0.5 * (md[i] + md[i - 1] * decay) * dt
        y[i] = acc
    return eps_c * float(y.max())


fund = {}
for tf in (1.0, 10.0):
    pk = peak_ratio(C.TAU_L_GYR, tf)
    mx = {k: float((pk * react(XG, k)).max()) for k in ("P", "S")}
    eps_max = {k: 0.10 / float(react(XG, k).max() * pk) for k in ("P", "S")}
    fund[f"t_f={tf:g}"] = dict(peak=pk, max_reaction=mx, eps_max=eps_max)
    P(f"    t_f = {tf:4.0f} Gyr: peak of (Thetabar * mdot) = {pk:.4f};  max reaction/g_law over x in [0.3, 30]: P {mx['P']:.2f}, S {mx['S']:.2f};  eps_c needed for the 0.10 line: P {eps_max['P']:.4f}, S {eps_max['S']:.4f}")
reaction_funded_pass = (MUT == "MA3") or all(v["max_reaction"][k] <= 0.10 for v in fund.values() for k in ("P", "S"))
R.check("G3 FUNDED reaction <= 0.10 g_law over x in [0.3, 30] (r = 0, eps_c = 1, tau_bar = tau_L, t_f = 1 and 10 Gyr)" + (" [MA3: reaction partner dropped]" if MUT == "MA3" else ""),
        reaction_funded_pass, f"max reaction {max(v['max_reaction']['P'] for v in fund.values()):.2f} g_law (pressure-slaved); the line needs eps_c <= {min(v['eps_max']['P'] for v in fund.values()):.4f} (an untied coupling)", kind="result")
# tracking arithmetic (reported; G1 is not addressed)
track = 1 - math.exp(-(C.T0_GYR - 1.0) / C.TAU_L_GYR)
P(f"    tracking (REPORTED, G1 not addressed): with tau_bar = tau_L the fluid's heat store reaches {track:.3f} of its target by t = {C.T0_GYR} Gyr for a 1-Gyr formation (the G1 line is 10%)")
R.num("funded", dict(table=fund, tracking_fraction=track, tau_L_Gyr=C.TAU_L_GYR))

R.banner("Vacuum ledger (FUNDED reading, POST-HOC): energy the heat needs against the vacuum energy of the ball it is drawn from")
led = {}
worst_shift = 0.0
for Mb in C.MASSES:
    rM = C.r_M_kpc(Mb); Vf2 = math.sqrt(C.G * Mb * C.A0)
    for lab, rta in (("CFG48", C.r_ta48_kpc(Mb)), ("B_committed", 1e3 * float(C7.r_ta_law(Mb, C7.A0["canonical"], C7.nu_mono, 1.0)))):
        re = 0.4 * rta; xe = re / rM
        Ec = 1.5 * xe * 0.5 * Mb * Vf2
        Evac = C.RHO_L * C.C_KMS ** 2 * (4 * math.pi / 3) * re ** 3
        shift = 0.5 * Ec / Evac
        ctf = C.C_KMS / (1.0 / C.GYR_PER_KPC_KMS) * 1.0           # kpc per Gyr of light travel (t_f = 1 Gyr)
        led[f"{Mb:.0e}/{lab}"] = dict(r_e_kpc=re, Ec_over_Evac=Ec / Evac, a0_shift=shift, light_ball_over_r_e=ctf / re)
        worst_shift = max(worst_shift, shift)
        P(f"    M_b {Mb:.0e} {lab:12s}: r_e = {re:7.1f} kpc   E_c/E_vac(<r_e) = {Ec / Evac:.2e}   local a0 shift = {shift:.2e}   c t_f(1 Gyr)/r_e = {ctf / re:.0f}")
ledger_cell_pass = worst_shift <= 0.01
if MUT == "MA5":
    R.check("G3 FUNDED ledger (reservoir identified, energy within the available vacuum, |delta a0/a0| <= 1%) [MA5: no ledger, an unfunded reservoir]", None is None and False,
            "UNDEFINED: with no ledger there is no reservoir to check", kind="result")
    ledger_cell_pass = False
else:
    R.check("G3 FUNDED ledger (reservoir identified, energy within the available vacuum, |delta a0/a0| <= 1%)", ledger_cell_pass,
            f"worst local a0 shift {worst_shift:.1e} (line 1e-2); every ball can be reached by light within 1 Gyr (c t_f / r_e >= {min(v['light_ball_over_r_e'] for v in led.values()):.0f}); "
            "NOT checked: how a w = -1 vacuum delivers energy locally (needs a non-Lorentz-invariant or dynamical vacuum: door 8's untested premise)", kind="result")
R.num("ledger", led)
R.verdict("G3 funded (arms A2/A3, post-hoc continuation)", "PASS" if (reaction_funded_pass and ledger_cell_pass) else "FAIL",
          f"reaction {'ok (MA3)' if MUT == 'MA3' else 'FAIL'}; ledger {'ok' if ledger_cell_pass else 'UNDEFINED/FAIL'}")

base = R.main_cells()
key_r = "G3 FUNDED reaction <= 0.10 g_law over x in [0.3, 30] (r = 0, eps_c = 1, tau_bar = tau_L, t_f = 1 and 10 Gyr)"
key_l = "G3 FUNDED ledger (reservoir identified, energy within the available vacuum, |delta a0/a0| <= 1%)"
if MUT == "MA3":
    R.finish([base.get(key_r) is False and reaction_funded_pass])
elif MUT == "MA5":
    R.finish([base.get(key_l) is True and not ledger_cell_pass])
else:
    R.finish()
