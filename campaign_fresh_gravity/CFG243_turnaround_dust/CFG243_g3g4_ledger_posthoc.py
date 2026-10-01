#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CFG243_g3g4_ledger_posthoc -- GATE 5 (G3/G4: energy and ledger), run as a POST-HOC EXTRA: the frozen stop rule halted the lane at COSMIC, so nothing here is part of
the frozen verdict.  Frozen text: CFG243_FROZEN_CRITERIA.md section 2, Gate 5 (L1-L4).

L1 reaction on the baryons: the baryon equation carries no source (CFG131 D4); the closed forms of CFG48 G4 / CFG70 apply only to a MAINTAINED exchange (reported).
L2 literal energy line: E_supplied = M_c c^2 against the baryons' orbital kinetic energy (1/2) M_b V_f^2 (V_f^4 = G a0 M_b), both r_ta conventions (CFG48's and B's committed).
L3 vacuum ledger: f_ta = M_c(<x r_M) / M_Lambda(<r_ta), M_Lambda = rho_Lambda (4 pi/3) r_ta^3 (rho_Lambda from the tie), x <= 30, both r_ta conventions; and CFG131 D4's
   Lagrangian-volume ledger f_Lag = (M_c - 5.366 M_b)/(13.86 M_b).  PASS iff f <= 1 for all x <= 30 in both conventions AND the implied local a0 shift f/2 <= 1e-2.
L4 constants: every constant that entered a verdict of this lane.
MUTATE=6: the vacuum energy of a ball 1e3 times larger than the creation region (a non-local reservoir): L3 must flip FAIL -> PASS.
"""
import os, sys, math, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import CFG243_common as C

R = C.Run("CFG243_g3g4_ledger_posthoc")
P = R.P
MUT = R.mutate
P(__doc__.strip())
P("\n  *** POST-HOC: the frozen stop rule halted the lane at COSMIC; nothing below is part of the frozen verdict ***")
G, A0, c = C.G, C.A0, C.C_KMS
four3 = 4.0 * math.pi / 3.0
RHO_L = C.RHO_L_CAN
P(f"  rho_Lambda from the tie a0 = kappa c sqrt(G rho_Lambda): {RHO_L:.2f} Msun/kpc^3 (CFG242_common: 86.33); a0 = {A0:.1f} (km/s)^2/kpc")

C7 = C.load_c7()
cfg70 = C.cfg70_rta()
HH, OM48, DELTA48 = 0.6736, 0.3153, 11.81
RHOC0_MPC = 2.775e11 * HH ** 2


def rta48(Mb):
    Mcol = Mb * (1.0 + C.OMEGA_C_OVER_B)
    return 1e3 * (3.0 * Mcol / (4.0 * math.pi * OM48 * RHOC0_MPC * DELTA48)) ** (1.0 / 3.0)


def rtaB(Mb):
    return 1e3 * float(C7.r_ta_law(Mb, C7.A0["canonical"], C7.nu_mono, 1.0))


R.banner("controls: r_ta conventions reproduce CFG70's committed values")
ok = True
rows = {}
for Mb in C.MASSES:
    r48, rB = rta48(Mb), rtaB(Mb)
    rows[Mb] = (r48, rB)
    if Mb in cfg70:
        j48, jB = cfg70[Mb]["CFG48"][0], cfg70[Mb]["B_nu_mono"][0]
        ok &= abs(r48 / j48 - 1) < 2e-3 and abs(rB / jB - 1) < 2e-3
        P(f"  M_b = {Mb:.0e}: r_ta(CFG48) {r48:.1f} (CFG70 JSON {j48:.1f}); r_ta(B, nu_mono) {rB:.1f} (CFG70 JSON {jB:.1f})")
    else:
        P(f"  M_b = {Mb:.0e}: r_ta(CFG48) {r48:.1f}; r_ta(B, nu_mono) {rB:.1f} (not in CFG70's table)")
R.check("C1 the two r_ta conventions reproduce CFG70's committed r_ta to 0.2% (1e9, 1e10, 1e12)", ok)

R.banner("L1 (reaction on the baryons)")
xs = np.array([0.3, 1.0, 3.0, 10.0, 30.0])
maint = 0.75 * xs ** 2 / np.sqrt(1 + xs ** 2)
P("  maintained exchange (CFG48 G4 / CFG70 closed form, pressure-slaved), reaction/g_law at x = 0.3, 1, 3, 10, 30: " + " / ".join(f"{m:.3g}" for m in maint) +
  "  (CFG70: 0.065 / 0.53 / 2.1 / 7.5 / 22.5).  These apply only if the exchange is MAINTAINED; the class creates dust once.")
R.check("L1-ctrl the closed form reproduces CFG70's reaction table (0.065, 0.53, 2.1, 7.5, 22.5 to 3%)", np.allclose(maint, [0.0647, 0.530, 2.13, 7.46, 22.49], rtol=0.03), "")
P("  creation-event reaction: the dust is created at the baryon velocity and the baryon equation has no source term (CFG131 D4: non-gravitational reaction = 0); the momentum budget of the creation "
  "is the G0-e integrability row (it fails there), not a reaction on the baryons.")
R.check("L1 the reaction on the baryons from the creation event <= 0.10 g_law at x = 0.3, 1, 3, 10, 30 (0 by construction: no source in the baryon equation)", True,
        "PASS trivially (CFG131 D4); the momentum accounting is G0-e", kind="result")

R.banner("L2 (literal energy line): M_c c^2 against the baryons' orbital kinetic energy")
l2 = {}
for Mb in C.MASSES:
    Vf2 = math.sqrt(G * A0 * Mb)
    Eorb = 0.5 * Mb * Vf2
    rM = C.r_M_kpc(Mb)
    row = {}
    for x in (1.0, 3.0, 10.0, 30.0):
        Mc = Mb * (math.sqrt(1 + x * x) - 1)
        row[f"x={x:g}"] = Mc * c ** 2 / Eorb
    for conv, (rta, re) in (("CFG48", (rows[Mb][0], 0.4 * rows[Mb][0])), ("B", (rows[Mb][1], 0.4 * rows[Mb][1]))):
        xe = re / rM
        Mc = Mb * (math.sqrt(1 + xe * xe) - 1)
        row[f"r_e({conv}) x_e={xe:.0f}"] = Mc * c ** 2 / Eorb
    l2[Mb] = row
    P(f"  M_b = {Mb:.0e} (V_f = {math.sqrt(Vf2):.0f} km/s): M_c c^2/E_orb at x = 1 / 3 / 10 / 30: " + " / ".join(f"{row[f'x={x:g}']:.2e}" for x in (1, 3, 10, 30)) +
      "; at r_e: " + ", ".join(f"{k.split(' ')[0]} {v:.2e}" for k, v in row.items() if k.startswith("r_e")))
R.num("L2", {f"{k:.0e}": v for k, v in l2.items()})
minratio = min(min(v.values()) for v in l2.values())
R.check("L2 the energy the vacuum must supply (rest mass) <= the baryons' orbital kinetic energy, both r_ta conventions", minratio <= 1.0,
        f"smallest ratio over the table {minratio:.2e}; CFG131 D4 quotes ~1e6-1e8 (net of the cosmic share, beyond x = 6.29)", kind="result")

R.banner("L3 (vacuum ledger)")
vol = 1e3 if MUT == "6" else 1.0
if MUT == "6":
    P("  *** MUTATE=6: the vacuum energy of a ball 1e3 times larger than the creation region (a non-local reservoir) ***")
fmax = {"CFG48": [], "B": []}
l3 = {}
for Mb in C.MASSES:
    rM = C.r_M_kpc(Mb)
    for conv, rta in (("CFG48", rows[Mb][0]), ("B", rows[Mb][1])):
        ML = RHO_L * four3 * rta ** 3 * vol
        f30 = Mb * (math.sqrt(1 + 900.0) - 1) / ML
        xta = rta / rM
        fta = Mb * (math.sqrt(1 + xta ** 2) - 1) / ML
        xe = 0.4 * rta / rM
        fe = Mb * (math.sqrt(1 + xe ** 2) - 1) / ML
        fmax[conv].append(f30)
        l3[f"{Mb:.0e}|{conv}"] = dict(r_ta=rta, M_Lambda_over_Mb=ML / Mb, f_x30=f30, f_ta=fta, f_re=fe)
        P(f"  M_b = {Mb:.0e}, r_ta({conv}) = {rta:7.1f} kpc: M_Lambda(<r_ta)/M_b = {ML / Mb:8.2f}; f at x = 30 (M_c = 29.0 M_b) = {f30:7.3f}; f for the dust out to r_ta: {fta:7.2f}; out to r_e: {fe:6.2f}")
R.num("L3", l3)
x_star = math.sqrt((5.366 + 13.86 + 1.0) ** 2 - 1)
f_lag30 = (math.sqrt(1 + 900.0) - 1 - 5.366) / 13.86
P(f"  CFG131 D4 Lagrangian-volume ledger: f_Lag(x = 30) = {f_lag30:.3f} (net of the cosmic share 5.366 M_b against Omega_Lambda/Omega_b = 13.86), crossing 1 at x* = {x_star:.1f}; gross f(30) = {(math.sqrt(1 + 900.0) - 1) / 13.86:.3f}")
worst = max(max(fmax["CFG48"]), max(fmax["B"]), f_lag30 if MUT != "6" else f_lag30 / 1e3)
f_ok = (max(fmax["CFG48"]) <= 1.0 and max(fmax["B"]) <= 1.0 and (f_lag30 / vol) <= 1.0)
a0shift = worst / 2.0
P(f"  worst f over the masses, both conventions and the Lagrangian ledger: {worst:.3f}; implied local a0 shift f/2 = {a0shift:.3f} (line 1e-2: needs f <= 0.02)")
R.check("L3 f <= 1 for every x <= 30 in both r_ta conventions and in CFG131's Lagrangian ledger", f_ok,
        f"CFG48-convention max f(30) = {max(fmax['CFG48']):.2f}; B-convention max {max(fmax['B']):.2f}; Lagrangian {f_lag30 / vol:.2f}", kind="result")
R.check("L3b the implied local a0 shift f/2 <= 1e-2 (f <= 0.02)", worst <= 0.02, f"worst f {worst:.3f}, shift {a0shift:.3f}", kind="result")
P("  CFG242 route A's ledger (heat: at most 1.9e-4 of the ball's vacuum energy, a0 shift <= 9.5e-5) is for the dust's KINETIC energy; this ledger is for its REST MASS, "
  "which the record (CFG131 D4, CFG253 (C)) says is a different and larger number.")

R.banner("L4 (constants that entered a verdict of this lane)")
ent = [("N, the generous normalisation of COSMIC (dust per turned-around mass tuned so that Omega_dust(z=0) = Omega_c)", "enters the COSMIC verdict (in the class's favour: removing it lowers the abundance further)"),
       ("F(u), the form of the amplitude Q = a0/(3 g_loc)", "a declared function shape (allowed), P-declared in AMT-1"),
       ("qj, the pericentre bracket r_peri/r_ta (0.05, 0.1, 0.2)", "a declared bracket (as CFG118), not fitted; the AMT-5 verdict is FAIL at all three"),
       ("creation_scale s (0.25-2) in the AMT-5 scan", "a labelled scan only; it enters no verdict; no s passes"),
       ("hysteresis p in the crossing count (0.01, 0.05, 0.2)", "a numerical regulator; the G0-b median is 19-24 at all three")]
for k, v in ent:
    P(f"   - {k}: {v}")
R.check("L4 no constant beyond kappa and Omega_c h^2 enters a verdict (the strict reading: N enters COSMIC)", False, "N (the generous normalisation) enters the COSMIC verdict", kind="result")

R.banner("G3/G4 verdict")
R.verdict("G3/G4 (post hoc)", "FAIL", f"L1 PASS (0, trivially); L2 FAIL (>= {minratio:.1e} x the orbital energy); L3 {'PASS' if f_ok else 'FAIL'} (f up to {worst:.2f}; a0 shift {a0shift:.2f} against 1e-2); L4 FAIL (strict: N)")

if MUT == "6":
    mc = R.main_cells()
    R.finish([mc.get("L3 f <= 1 for every x <= 30 in both r_ta conventions and in CFG131's Lagrangian ledger") is False, f_ok])
else:
    R.finish()
