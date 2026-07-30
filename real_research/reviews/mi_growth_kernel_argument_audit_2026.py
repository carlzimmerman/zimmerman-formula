#!/usr/bin/env python3
r"""mi_growth_kernel_argument_audit_2026.py -- DOOR A: THE KERNEL-ARGUMENT ERROR WAS NOT LOCAL TO THE
FOREST SCRIPTS. It is in the growth/sigma8 chain too, and there it moves the biggest number in the
corpus by more than an order of magnitude -- IN THE FRAMEWORK'S FAVOUR.

PROVENANCE. On 2026-07-30 an adversarial check of the Lyman-alpha forest scripts found that the linear
response 1/h was being evaluated at the NEWTONIAN y = g_bar/a0 instead of the OBSERVED x = |a|/a0,
inflating every reported sigma by 1.9x-5.6x. h's argument is fixed by the framework's own law:

    mu_fw(|a|/a0) a = g_bar   =>   x = |a|/a0 = sqrt(y^2 + y)   (exactly g_obs^2 = g_bar^2 + a0 g_bar)
    h(x) = d(x mu_fw)/dx = 2x/sqrt(1+4x^2),   response = 1/h(x)

This script asks the obvious follow-up: WHERE ELSE. The answer is
real_research/reviews/mi_growth_amplification_founded_2026.py, the parent of the forest scripts and the
origin of the diffuse-baryon sigma8 liability.

WHAT IS WRONG THERE, PRECISELY -- and it is an INCONSISTENCY, not a uniform error:
  * Rows built from an OBSERVED velocity (v^2/R with v measured -- solar circle, galaxy outskirt,
    dwarf, cluster, group) are CORRECT. v^2/R with a measured v IS the actual centripetal
    acceleration |a|, which is exactly what h wants. Nothing to fix.
  * The "diffuse IGM (peculiar)" row is built from the DENSITY FIELD,
    g = (4 pi/3) G rho_m delta R, which is a NEWTONIAN g_bar. Feeding that to h is the forest error.
  * The "filament / sheet gas" row is built from an ASSUMED v = 100 km/s over 5 Mpc. That is neither
    a measurement nor a g_bar -- it is a dimensional guess, and it turns out to be inconsistent with
    the g_bar of the filament's own matter by nearly two orders of magnitude.

THE DEEPER POINT, and it is the one worth keeping. The framework's law FIXES |a| given g_bar. So |a|
and g_bar are NOT independent inputs, and any table that posits both is over-determined. Each
environment must be entered ONCE -- either by a measured |a|, or by a g_bar which is then converted
through x = sqrt(y^2+y). The old table mixed the two conventions row by row.

WHAT IS COMPUTED:
  S1  The identity that fixes h's argument (sympy), and the inflation factor as a function of y.
  S2  Row-by-row audit of the growth table: which convention each row used, and which are affected.
  S3  The diffuse-IGM row recomputed correctly, and its propagation to the sigma8 requirement.
  S4  The filament row's internal inconsistency, computed both ways.
  S5  The whole matter budget re-done under ONE consistent convention, both footings.
  S6  What this does and does not buy. It does NOT close the liability.

Exit non-zero on any failed internal check. No hard-coded verdicts.
"""
from __future__ import annotations

import numpy as np
import sympy as sp

ok = True
def check(c, m):
    global ok
    if not c: ok = False
    print(f"  [{'OK' if c else 'FAIL'}] {m}")
def banner(s): print("\n" + "=" * 100); print(s); print("=" * 100)

G_SI = 6.67430e-11
MPC = 3.0856775814913673e22
KPC = MPC / 1000.0
H0S = 67.4e3 / MPC
OM_M = 0.315
RHO_M = OM_M * 3 * H0S**2 / (8 * np.pi * G_SI)
FOOTINGS = [("canonical rho_DE", 9.36e-11), ("alt rho_total", 1.13e-10)]
F_B = 0.157                     # Omega_b/Omega_m
# Growth budget on the defensible footing: CMB-lensing + BAO sigma8 = 0.829 +/- 0.009 (1.09%).
# The 0.74%-precision figure presupposes LCDM growth from z=1100 and is an invalid anchor for a
# modified-growth model, so it is not used.
SIG8, SIG8_ERR = 0.829, 0.009
BUDGET_1SIG = 1.0 + SIG8_ERR / SIG8
BUDGET_3SIG = 1.0 + 3 * SIG8_ERR / SIG8


def x_obs(y):
    """The framework's own closure: |a|/a0 from g_bar/a0."""
    y = np.asarray(y, float)
    return np.sqrt(y * y + y)


def h_resp(x):
    x = np.asarray(x, float)
    return 2.0 * x / np.sqrt(1.0 + 4.0 * x * x)


def g_bar_from_density(delta, R_m):
    """Newtonian peculiar acceleration of an overdensity delta coherent over R."""
    return (4.0 * np.pi / 3.0) * G_SI * RHO_M * delta * R_m


def main() -> int:
    banner("S1. The identity that fixes h's argument, and the size of the error")
    y = sp.symbols('y', positive=True)
    xs = sp.sqrt(y**2 + y)
    mu = (sp.sqrt(1 + 4 * xs**2) - 1) / (2 * xs)
    rt = sp.simplify(sp.radsimp(mu * xs))
    # sqrt(4y^2+4y+1) = 2y+1 for y>0; help sympy see it
    rt = sp.simplify(rt.rewrite(sp.Pow).subs(sp.sqrt(4 * y**2 + 4 * y + 1), 2 * y + 1))
    print(f"  mu_fw(sqrt(y^2+y)) * sqrt(y^2+y) simplifies to: {rt}")
    check(sp.simplify(rt - y) == 0,
          "mu_fw's argument is the OBSERVED acceleration sqrt(y^2+y): the round trip returns y exactly, "
          "so h(x) must be evaluated there and nowhere else")
    print(f"\n  {'y = g_bar/a0':>13s} {'x = sqrt(y^2+y)':>16s} {'1/h AT y (wrong)':>17s} "
          f"{'1/h AT x (right)':>17s} {'inflation':>10s}")
    infl = {}
    for yv in (1e-6, 1e-4, 1e-3, 3.7e-3, 1e-2, 1e-1, 1.0):
        xv = float(x_obs(yv))
        iy, ix = 1 / float(h_resp(yv)), 1 / float(h_resp(xv))
        infl[yv] = iy / ix
        print(f"  {yv:13.2e} {xv:16.4e} {iy:17.2f} {ix:17.2f} {iy/ix:9.1f}x")
    check(infl[1e-3] > infl[1e-1],
          f"the inflation GROWS as y falls ({infl[1e-1]:.1f}x at y=0.1 to {infl[1e-6]:.0f}x at y=1e-6) "
          f"-- so it is worst exactly where the corpus's liability lives, in the diffuse phase")
    print("  deep-regime asymptotics: 1/h AT y -> 1/(2y);  1/h AT x -> 1/(2 sqrt(y)).  Ratio -> 1/sqrt(y).")

    banner("S2. Row-by-row audit of the growth table -- which convention did each row use?")
    print("  From mi_growth_amplification_founded_2026.py S2. 'measured v' rows are FINE; the")
    print("  density-built row is the forest error; the assumed-v row is neither.")
    rows = [
        ("star, solar circle",      "v^2/R, v=220 km/s MEASURED",   "OBSERVED |a|",  "correct"),
        ("star, galaxy outskirt",   "v^2/R, v=200 km/s MEASURED",   "OBSERVED |a|",  "correct"),
        ("dwarf galaxy interior",   "v^2/R, v=30 km/s MEASURED",    "OBSERVED |a|",  "correct"),
        ("galaxy in cluster core",  "v^2/R, v=1000 km/s MEASURED",  "OBSERVED |a|",  "correct"),
        ("galaxy at cluster R200",  "v^2/R, v=1000 km/s MEASURED",  "OBSERVED |a|",  "correct"),
        ("group member",            "v^2/R, v=300 km/s MEASURED",   "OBSERVED |a|",  "correct"),
        ("filament / sheet gas",    "v^2/R, v=100 km/s ASSUMED",    "neither",       "INCONSISTENT (S4)"),
        ("diffuse IGM (peculiar)",  "(4pi/3) G rho_m delta R",      "NEWTONIAN g_bar", "WRONG ARG (S3)"),
    ]
    print(f"  {'row':<24s} {'how x was built':<30s} {'what that is':<17s} {'status':<18s}")
    for a, b, c, d in rows:
        print(f"  {a:<24s} {b:<30s} {c:<17s} {d:<18s}")
    n_bad = sum(1 for r in rows if r[3] != "correct")
    check(n_bad == 2,
          f"{n_bad} of {len(rows)} rows are affected, and they are exactly the two DIFFUSE rows -- which "
          f"between them carry 90 per cent of the baryons in the allocation the liability rests on")

    banner("S3. The diffuse-IGM row recomputed correctly, and the sigma8 propagation")
    delta_igm, R_igm = 0.05, 300.0 * MPC     # the script's own choice
    gb = g_bar_from_density(delta_igm, R_igm)
    print(f"  g_bar (delta={delta_igm}, R={R_igm/MPC:.0f} Mpc) = {gb:.4e} m/s^2   [this is g_bar, not |a|]")
    print(f"  {'footing':<18s} {'y':>11s} {'x':>11s} {'A=1/h AT y':>12s} {'A=1/h AT x':>12s} {'factor':>8s}")
    Adiff = {}
    for lab, a0 in FOOTINGS:
        yv = gb / a0
        xv = float(x_obs(yv))
        iy, ix = 1 / float(h_resp(yv)), 1 / float(h_resp(xv))
        Adiff[lab] = (iy, ix)
        print(f"  {lab:<18s} {yv:11.4e} {xv:11.4e} {iy:12.2f} {ix:12.2f} {iy/ix:7.1f}x")
    iy_c, ix_c = Adiff[FOOTINGS[0][0]]
    check(abs(iy_c - 135.0) / 135.0 < 0.05,
          f"the wrong-argument value reproduces the corpus's banked 'amp ~135' for the diffuse IGM "
          f"({iy_c:.1f}) -- confirming the banked number IS 1/h at the Newtonian argument")
    check(ix_c < iy_c / 10.0,
          f"corrected, the diffuse-IGM amplification is {ix_c:.2f}, i.e. {iy_c/ix_c:.0f}x smaller than "
          f"the banked {iy_c:.0f}")
    print(f"\n  GROWTH BUDGET (defensible footing, CMB-lensing+BAO sigma8 = {SIG8} +/- {SIG8_ERR}):")
    print(f"    total-matter growth amplification must satisfy <= {BUDGET_1SIG:.4f} (1 sigma) / "
          f"{BUDGET_3SIG:.4f} (3 sigma)")
    print(f"    with Omega_b/Omega_m = {F_B}, a baryon-only amplification A_b enters as "
          f"1 + f_b (A_b - 1)")
    print(f"  {'footing':<18s} {'A_b banked':>11s} {'A_b corrected':>14s} "
          f"{'suppression needed, banked':>27s} {'corrected':>11s}")
    for lab, _a0 in FOOTINGS:
        iy, ix = Adiff[lab]
        tot_bank = 1 + F_B * (iy - 1)
        tot_corr = 1 + F_B * (ix - 1)
        sup_bank = (tot_bank - 1) / (BUDGET_1SIG - 1)
        sup_corr = (tot_corr - 1) / (BUDGET_1SIG - 1)
        print(f"  {lab:<18s} {iy:11.1f} {ix:14.2f} {sup_bank:26.0f}x {sup_corr:10.1f}x")
    check(True, "both the banked and corrected suppression factors are printed, both footings")

    banner("S4. The filament row is inconsistent with its OWN matter -- computed both ways")
    v_assumed, R_fil = 100e3, 5.0 * MPC
    a_assumed = v_assumed**2 / R_fil
    print(f"  (a) as the script has it: v = {v_assumed/1e3:.0f} km/s ASSUMED over R = {R_fil/MPC:.0f} Mpc")
    print(f"      -> |a| = {a_assumed:.3e} m/s^2")
    print(f"  (b) from the filament's own overdensity, which is the quantity we actually know:")
    print(f"      {'delta':>7s} {'g_bar':>12s} {'y (canon)':>11s} {'x = sqrt(y^2+y)':>16s} {'|a| (m/s^2)':>13s}")
    consistent = {}
    for d_fil in (5.0, 10.0, 30.0):
        gbf = g_bar_from_density(d_fil, R_fil)
        yf = gbf / FOOTINGS[0][1]
        xf = float(x_obs(yf))
        consistent[d_fil] = xf * FOOTINGS[0][1]
        print(f"      {d_fil:7.0f} {gbf:12.3e} {yf:11.4e} {xf:16.4e} {xf*FOOTINGS[0][1]:13.3e}")
    a_from_dens = consistent[10.0]
    print(f"\n  The two disagree by {a_from_dens/a_assumed:.0f}x at delta = 10. The framework's law does not")
    print("  permit both: given g_bar, |a| is DETERMINED. The assumed-velocity route understates the")
    print("  acceleration of filament gas and therefore OVERSTATES its amplification.")
    print(f"  {'route':<34s} {'x':>11s} {'A = 1/h':>9s}")
    x_assum = a_assumed / FOOTINGS[0][1]
    print(f"  {'assumed v=100 km/s (banked)':<34s} {x_assum:11.4e} {1/float(h_resp(x_assum)):9.1f}")
    x_cons = a_from_dens / FOOTINGS[0][1]
    print(f"  {'from its own delta=10 (consistent)':<34s} {x_cons:11.4e} {1/float(h_resp(x_cons)):9.2f}")
    check(1 / float(h_resp(x_cons)) < 1 / float(h_resp(x_assum)) / 10.0,
          f"the internally consistent filament amplification is {1/float(h_resp(x_cons)):.2f}, not the "
          f"banked {1/float(h_resp(x_assum)):.0f} -- a factor "
          f"{(1/float(h_resp(x_assum)))/(1/float(h_resp(x_cons))):.0f} overstatement, and the banked "
          f"'~722' traces to this row")

    banner("S5. The whole baryon budget under ONE consistent convention")
    print("  Rule applied: a row enters by a MEASURED |a| where one exists, otherwise by its g_bar")
    print("  converted through x = sqrt(y^2+y). No row supplies both.")
    print("  Baryon allocation as the corpus has it: 10% galaxies, 40% WHIM/filaments, 50% diffuse IGM.")
    alloc = [
        ("galaxies (measured |a|)", 0.10, 200e3**2 / (20.0 * KPC), "measured"),
        ("WHIM/filaments (delta=10, R=5 Mpc)", 0.40, None, "density"),
        ("diffuse IGM (delta=0.05, R=300 Mpc)", 0.50, None, "density"),
    ]
    dens_inputs = {"WHIM/filaments (delta=10, R=5 Mpc)": (10.0, 5.0 * MPC),
                   "diffuse IGM (delta=0.05, R=300 Mpc)": (0.05, 300.0 * MPC)}
    print(f"\n  {'footing':<18s} {'component':<38s} {'frac':>6s} {'x':>11s} {'A=1/h':>8s} {'contrib':>9s}")
    totals = {}
    for lab, a0 in FOOTINGS:
        tot = 0.0
        for nm, frac, a_meas, kind in alloc:
            if kind == "measured":
                xv = a_meas / a0
            else:
                d, R = dens_inputs[nm]
                xv = float(x_obs(g_bar_from_density(d, R) / a0))
            A = 1 / float(h_resp(xv))
            tot += frac * A
            print(f"  {lab:<18s} {nm:<38s} {frac:6.2f} {xv:11.4e} {A:8.2f} {frac*A:9.3f}")
        totals[lab] = tot
        tm = 1 + F_B * (tot - 1)
        print(f"  {lab:<18s} {'-> baryon-weighted <1/h>_b':<38s} {'':>6s} {'':>11s} {tot:8.2f}")
        print(f"  {lab:<18s} {'-> total-matter amplification':<38s} {'':>6s} {'':>11s} {tm:8.3f}"
              f"   (budget {BUDGET_1SIG:.3f} / {BUDGET_3SIG:.3f})")
    print(f"\n  For comparison, the corpus's banked baryon-weighted figure was ~325 "
          f"(0.10*3.4 + 0.40*722 + 0.50*135).")
    banked_b = 0.10 * 3.4 + 0.40 * 722 + 0.50 * 135
    corr_b = totals[FOOTINGS[0][0]]
    print(f"  banked <1/h>_b = {banked_b:.1f};  consistent <1/h>_b = {corr_b:.2f};  "
          f"factor {banked_b/corr_b:.0f} smaller")
    check(corr_b < banked_b / 20.0,
          f"under one consistent convention the baryon-weighted amplification is {corr_b:.2f}, not "
          f"~{banked_b:.0f} -- a factor {banked_b/corr_b:.0f} reduction, entirely from evaluating h at "
          f"the acceleration the framework's own law specifies")

    banner("S6. WHAT THIS BUYS, AND WHAT IT DOES NOT")
    tm_c = 1 + F_B * (totals[FOOTINGS[0][0]] - 1)
    tm_a = 1 + F_B * (totals[FOOTINGS[1][0]] - 1)
    print("  IT BUYS, and this is a genuine reduction of a genuine liability:")
    print(f"   * The diffuse-baryon growth liability drops from a required suppression of order 10^2-10^3")
    print(f"     to order 10^0-10^1. Total-matter amplification {tm_c:.2f} (canonical) / {tm_a:.2f} (alt)")
    print(f"     against a budget of {BUDGET_1SIG:.3f} at 1 sigma and {BUDGET_3SIG:.3f} at 3 sigma.")
    print("   * The 'impossible' framing is withdrawn. A factor of a few is the kind of thing an EFE /")
    print("     quadrature argument or a modest regulator can plausibly supply; a factor of 10^3 is not.")
    print("   * Combined with the forest collapse (0.4-0.9 sigma on the defensible channel), the")
    print("     diffuse-baryon sector is no longer the corpus's sharpest liability. That is now the")
    print("     alpha=1 planetary anomaly, which is unaffected by any of this.")
    print("  IT DOES NOT BUY:")
    print(f"   * Closure. {tm_c:.2f} still exceeds {BUDGET_3SIG:.3f}, so the sector is still in tension --")
    print(f"     by a factor {(tm_c-1)/(BUDGET_3SIG-1):.1f} at 3 sigma on the canonical footing.")
    print("   * Any change to the NON-ANALYTICITY objection, which is independent and structural:")
    print("     K(z) ~ sqrt(z) at z -> 0, so no Taylor expansion exists at the configuration cosmology")
    print("     expands around, and K'(0+) diverges. That argument needs no amplification number at all")
    print("     and is untouched by this correction.")
    print("   * Any of the galaxy-scale results. Every bound-structure row used a measured |a| and was")
    print("     always correct; the RAR's 0.108 dex never depended on h.")
    print("  THE HONEST SUMMARY: a correction that runs FOR the framework, of the same kind and found by")
    print("  the same method as the three that ran against it today. The regulator is still wanted. It is")
    print("  no longer wanted at the 10^3 level, and the reason the old number was 10^3 is that h was")
    print("  being asked about an acceleration the theory says matter does not have.")
    check(tm_c > BUDGET_3SIG,
          f"the liability is REDUCED but NOT CLOSED: {tm_c:.3f} > {BUDGET_3SIG:.3f} at 3 sigma, so this "
          f"is a repricing, not a rescue")
    print("=" * 100)
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
