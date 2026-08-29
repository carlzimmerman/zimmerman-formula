"""
mc_frame_theorem.py -- the decisive stage-1 structural question, answered two ways.

Gate-SLIP kills essentially everything through the FRAME slip Phi~' - Psi~'.  The design
question is therefore sharp:

    WHICH disformal partner can make the lensing potential track the MOND-enhanced
    dynamical potential, and does any such partner have a BOOST-INVARIANT vacuum?

(if one did, G2 and G4 would stop being in conflict and the AeST alpha_2 pincer would be
escapable.  every chassis killed this session died in that pincer.)

PART A (symbolic, exact).  Write Phi~' - Psi~' for the general 8-parameter matter frame
    g~_mn = e^{2(M1 phi + M2 chi)}[ g_mn + (M3+M5 phi) A_m A_n + (M4+M6 phi) S_mn
                                         + (M7+M8 phi) d_m phi d_n phi ]
on the Einstein-frame no-slip background (Phi' = Psi', which is what the flux equations
give whenever no operator sources P_Psi), and ask for the conditions under which it
vanishes IDENTICALLY in the carrier background rather than at one acceleration.

PART B (numeric).  For every (MOND core) x (disformal partner) pair, try to zero the
frame slip at TWO accelerations at once with a 2-parameter damped Newton (mc_screen's
_multi_tune), then test the tuned point over the full 29-point Sigma grid, then read off
the vacuum boost-breaking.  Success at one acceleration is cheap; success at all of them
is the theory-level question.
"""
import sys
import numpy as np
import sympy as sp

import mc_gates as G
import mc_reduce_static as RS
import mc_screen as S
from mc_basis import N_OPS, N_PARAM, OP_INDEX, MFRAME

np.seterr(all='ignore')

print("=" * 78)
print("PART A -- symbolic: what makes the frame slip vanish IDENTICALLY?")
print("=" * 78)

m1, m2, m3, m4, m5, m6, m7, m8 = sp.symbols('M1 M2 M3 M4 M5 M6 M7 M8')
Phi1, Psi1, phi1, chi0, chi1 = sp.symbols('Phi1 Psi1 phi1 chi0 chi1')
A00, A01, Az0, Az1 = sp.symbols('A00 A01 Az0 Az1')
S000, S001, Szz0, Szz1 = sp.symbols('S000 S001 Szz0 Szz1')

conf0 = 1 + 2 * m2 * chi0
confp = 2 * (m1 * phi1 + m2 * chi1)
dA0, dAp = m3, m5 * phi1
dS0, dSp = m4, m6 * phi1
dP0, dPp = m7, m8 * phi1

B00_0 = -1 + dA0 * A00**2 + dS0 * S000
B00_p = -2 * Phi1 + dAp * A00**2 + dA0 * 2 * A00 * A01 + dSp * S000 + dS0 * S001
Phit1 = -sp.Rational(1, 2) * (confp * B00_0 + conf0 * B00_p)

Sxx0 = (S000 - Szz0) / 2
Sxxp = (S001 - Szz1) / 2
Bxx_0 = 1 + dS0 * Sxx0
Bxx_p = -2 * Psi1 + dSp * Sxx0 + dS0 * Sxxp
Bzz_0 = 1 + dA0 * Az0**2 + dS0 * Szz0 + dP0 * phi1**2
Bzz_p = (-2 * Psi1 + dAp * Az0**2 + dA0 * 2 * Az0 * Az1 + dSp * Szz0 + dS0 * Szz1
         + dPp * phi1**2)
Bsp_0 = (2 * Bxx_0 + Bzz_0) / 3
Bsp_p = (2 * Bxx_p + Bzz_p) / 3
Psit1 = -sp.Rational(1, 2) * (confp * Bsp_0 + conf0 * Bsp_p)

D = sp.expand(Phit1 - Psit1)

# cross-check against the numeric observables() used by the gates
rng = np.random.default_rng(4)
maxdev = 0.0
for _ in range(200):
    vals = rng.normal(size=13)
    mp = rng.normal(size=8)
    X = np.zeros(RS.N_UNK)
    for k, nm in enumerate(["Phi1", "Psi1", "phi1", "chi0", "chi1", "A00", "A01",
                            "Az0", "Az1", "S000", "S001", "Szz0", "Szz1"]):
        X[G.IX[nm]] = vals[k]
    ob = G.observables(X, mp)
    sub = dict(zip([Phi1, Psi1, phi1, chi0, chi1, A00, A01, Az0, Az1,
                    S000, S001, Szz0, Szz1], vals))
    sub.update(dict(zip([m1, m2, m3, m4, m5, m6, m7, m8], mp)))
    maxdev = max(maxdev, abs(float(D.subs(sub)) - (ob["Phit1"] - ob["Psit1"])))
print(f"A0  symbolic D == numeric observables():  max dev {maxdev:.3e}  "
      f"{'OK' if maxdev < 1e-10 else 'MISMATCH'}")
assert maxdev < 1e-10

# on the Einstein-frame no-slip background Phi' = Psi'
Dn = sp.expand(D.subs(Psi1, Phi1))
print("\nA1  frame slip on the Einstein-frame no-slip background (Phi' = Psi'):")
print("    D =", sp.factor(sp.collect(Dn, [phi1, chi1])))

# --- case 1: conformal coupling only (M3..M8 = 0) -----------------------------------
D1 = sp.expand(Dn.subs({m3: 0, m4: 0, m5: 0, m6: 0, m7: 0, m8: 0}))
print("\nA2  CONFORMAL ONLY (M3..M8 = 0):   D =", sp.simplify(D1))
sol1 = sp.solve([sp.Poly(D1, phi1, chi1).coeff_monomial(mono)
                 for mono in sp.Poly(D1, phi1, chi1).monoms()
                 and sp.Poly(D1, phi1, chi1).monoms()], [m1, m2], dict=True)
print("    -> D = 2(M1 phi' + M2 chi'), vanishes identically iff M1 = M2 = 0,"
      " i.e. NO conformal fifth force at all.")
print("    'conformal scalars do not lens' -- reproduced as an identity.")

# --- case 2: add the purely SCALAR disformal partner d_m phi d_n phi ----------------
D2 = sp.expand(Dn.subs({m3: 0, m4: 0, m5: 0, m6: 0, m2: 0}))
p2 = sp.Poly(D2, phi1)
print("\nA3  CONFORMAL + SCALAR-GRADIENT DISFORMAL (M3=M4=M5=M6=M2=0):")
for mono, coef in zip(p2.monoms(), p2.coeffs()):
    print(f"       phi'^{mono[0]} : {sp.simplify(coef)}")
print("    -> the phi'^1 coefficient is 2 M1, independent of M7 and M8: the")
print("       d_m phi d_n phi partner has NO 00-component for a STATIC configuration,")
print("       so it cannot touch Phi~ and cannot cancel the conformal slip.")
print("       Vanishing identically again forces M1 = 0 => no MOND fifth force.")

# --- case 3: vector disformal (Bekenstein) ------------------------------------------
D3 = sp.expand(Dn.subs({m2: 0, m4: 0, m6: 0, m7: 0, m8: 0, Az0: 0, Az1: 0}))
p3 = sp.Poly(D3, phi1)
print("\nA4  CONFORMAL + VECTOR DISFORMAL (A_z = 0 in the static frame):")
for mono, coef in zip(p3.monoms(), p3.coeffs()):
    print(f"       phi'^{mono[0]} : {sp.simplify(coef)}")
lin = sp.simplify(p3.coeff_monomial(phi1))
sol = sp.solve(sp.Eq(lin, 0), m5)
print(f"    -> the phi'^1 coefficient vanishes at  M5 = {sol}")
print(f"       with the unit-timelike normalisation A_0^2 = 1 and M3 = 0 this is"
      f" M5 = {sp.simplify(sol[0].subs({A00: 1, m3: 0}))}  <-- Bekenstein's -4 M1")
print("    -> the cancellation is proportional to A_0^2.  It EXISTS only because the")
print("       vector VEV has a TIMELIKE component, which is precisely a preferred frame.")

# --- case 4: tensor disformal --------------------------------------------------------
D4 = sp.expand(Dn.subs({m2: 0, m3: 0, m5: 0, m7: 0, m8: 0}))
p4 = sp.Poly(D4, phi1)
lin4 = sp.simplify(p4.coeff_monomial(phi1))
print("\nA5  CONFORMAL + SYMMETRIC-TRACELESS DISFORMAL:")
print(f"       phi'^1 coefficient : {lin4}")
sol4 = sp.solve(sp.Eq(lin4, 0), m6)
print(f"    -> vanishes at M6 = {sol4}")
print("       the cancellation is again proportional to the TIME-TIME component S_00")
print("       (S_zz and S_xx enter with the opposite, trace-averaged weight), so it too")
print("       requires a VEV that singles out the time direction.")

print("\nA6  CONCLUSION OF PART A (structural, exact within this matter-frame family):")
print("    the frame slip is 2(M1 phi' + M2 chi') + [disformal corrections].")
print("    the ONLY disformal structures that produce a phi'-LINEAR correction able to")
print("    cancel it are the ones carrying a TIMELIKE VEV (A_0^2, S_00).  The purely")
print("    spatial partner d_m phi d_n phi cannot.  So within this basis")
print("        G2 (lensing tracks dynamics)  =>  a preferred-frame carrier vacuum")
print("    which is exactly the structure that generated AeST's alpha_2 = 1/lam_s +")
print("    2/(K_B lam_s^2) pole.  G2 and G4 are in structural conflict here.")
print("    SCOPE: this is a statement about THIS 8-parameter matter frame and the static")
print("    plane-symmetric reduction, NOT an all-Lagrangian theorem.")

# ------------------------------------------------------------------------------------
print("\n" + "=" * 78)
print("PART B -- numeric: can any partner zero the frame slip at TWO accelerations?")
print("=" * 78)

# SYSTEMATIC multi-start: a grid over the two free matter-frame parameters, so a failure
# to tune is a statement about the partner and not about a bad random draw.  (A start with
# |M3| or |M4| too large makes g~_00 change sign, sqrt(-g~_00) imaginary and the solve
# fail; the grid covers both signs and three magnitudes so that never decides the answer.)
STARTS = [(sa * a_, sb * b_)
          for sa in (-1.0, 1.0) for a_ in (0.3, 1.0, 4.0)
          for sb in (-1.0, 1.0) for b_ in (0.2, 1.0)]

rows = []
for pname, part in S.DISFORMAL_PARTNERS.items():
    for ci, core in enumerate(S.MOND_CORES[:2]):
        best = None
        ntuned = 0
        for si, (va, vb) in enumerate(STARTS):
            r = np.random.default_rng(1000 * ci + si)
            c = S._mk(core)
            for k, v in part["ops"].items():
                c[OP_INDEX[k]] = v
            c[N_OPS + MFRAME.index("M1_conf_phi")] = -1.0
            free = [N_OPS + MFRAME.index(k) for k in part["mkeys"]]
            if len(free) < 2:
                free = free + [N_OPS + MFRAME.index("M2_conf_chi")]
            c[free[0]] = va
            c[free[1]] = vb
            if not S._multi_tune(c, free[:2], [8.0e-3, 8.0e3]):
                continue
            ntuned += 1
            v, info = G.run_chain(c, rng=r)
            if best is None or (info.get("frame_slip_worst", 9e99) <
                                best[1].get("frame_slip_worst", 9e99)):
                best = (v, info, c.copy())
            if v in ("SURVIVOR",):
                break
        if best is None:
            rows.append((pname, ci, "NO_2POINT_TUNING", None, None, 0))
        else:
            v, info, c = best
            rows.append((pname, ci, v, info.get("frame_slip_worst"),
                         info.get("vacuum_boost_break"), ntuned))

print(f"\n{'partner':12s} {'core':4s} {'verdict':14s} {'worst frame slip':>17s} "
      f"{'vacuum boost-break':>19s} {'n 2pt-tuned':>12s}")
for pname, ci, v, fs, bb, nt in rows:
    fss = "n/a" if fs is None else f"{fs:.3e}"
    bbs = "n/a" if bb is None else f"{bb:.3e}"
    print(f"{pname:12s} {ci:<4d} {v:14s} {fss:>17s} {bbs:>19s} {nt:>12d}")

ok2 = [r for r in rows if r[3] is not None and r[3] < 1e-6]
print(f"\nB1  partners that hold the frame slip to < 1e-6 across the FULL 29-point grid "
      f"after a 2-point tuning: {len(ok2)}")
for r in ok2:
    print(f"      {r[0]} core{r[1]}: verdict={r[2]}  vacuum boost-break={r[4]:.3e}")
if ok2 and all(r[4] is not None and r[4] > 1e-8 for r in ok2):
    print("B2  EVERY one of them has a preferred-frame (boost-breaking) carrier vacuum")
    print("    -> Part A's structural conclusion is confirmed numerically.")
elif not ok2:
    print("B2  none -- the frame slip could not be held to zero across the grid at all.")
else:
    print("B2  at least one boost-INVARIANT vacuum reached zero frame slip: INSPECT IT.")
    for r in ok2:
        if r[4] is not None and r[4] <= 1e-8:
            print("      *** ", r)
