#!/usr/bin/env python3
r"""mi_dcac_branch_verdict_withdrawn_2026.py -- TRIAGE of the top staleness candidate flagged by
mi_corpus_stale_audit_2026 check E: does mi_dcac_branch_settled_2026.py (Jul 27) still stand?

WHY IT MATTERS. That script settles the wide-binary DC/AC gate branch -- the two branches are
4.9-5.8 sigma apart in the frozen Gaia DR4 error model -- and it states in its own words that this
"decides whether mi_wb_cubic_rise_2026.py and WB_CUBIC_GATE_LAW (Zenodo 10.5281/zenodo.21580093)
stand or are VOID". Its verdict is "THE AC BRANCH ... not an interpretation or a preference".
A PUBLISHED paper's declared standing rests on it, so a defect here is not bookkeeping.

WHAT IS TESTED, and the answer stated up front so nothing is oversold. Three separate defects, in
increasing order of seriousness; the third is the one that withdraws the verdict.

  S1  ITS CENTRAL ALGEBRAIC CLAIM IS FALSE AS STATED. "on a circular orbit u_mu is an EIGENVECTOR of
      Box_u with eigenvalue -Omega^2" is verified there on a TWO-COMPONENT SPATIAL vector; the time
      leg is never formed. Done on the actual 4-velocity, Box_u annihilates u^0 (eigenvalue 0) while
      the spatial legs give -(gamma Omega)^2, so u is NOT an eigenvector. MUTATION CONTROL: this
      script reproduces the false "PASS" by deleting the time leg, proving the defect is exactly the
      omitted component and not a signature or convention quibble. (Independently flagged as
      FINDING 2 of AUDIT_mi_kernel_axis_gate_2026.py, which rated it verdict-neutral for ITS use.)
  S2  ITS S2 THEN PROPAGATES THAT INTO THE AMPLITUDE. Pulling K out of the contraction as
      u^mu K u_mu = K(z)(u.u) = -K(z) requires a genuine eigenvector. The correct block value is
      +gamma^2 v^2 K(z) -- opposite SIGN and suppressed by (v/c)^2. Quantified at wide-binary and
      galactic speeds, both footings.
  S3  NO CONTRADICTION WITH THEOREM B -- the honest half. The u-normalised first MOMENT really is
      +|a|^2 (a magnitude, the DC-side object) and the RESOLVENT eigenvalue really is -(gamma Omega)^2
      (a frequency, the AC-side object). Both are correct: the moment is the spectral weight-average,
      and this script verifies it equals a.a EXACTLY in sympy. So the two readings are different
      objects, not rival claims -- which is precisely why the branch cannot be settled by algebra.
  S4  THE DEFECT THAT WITHDRAWS THE VERDICT. mi_action_eom_vs_rar_2026.py (Jul 30, one day later)
      showed that the action's literal reading is AMPLITUDE-FREE: z sits on K's cut where |K| -> 1,
      against a law that needs mu_fw = 0.618 at a0. Checked here for BOTH kernels, so it does not
      lean on the retired alpha=1. Therefore the "read Box_u off the action" strategy selects the
      one reading under which the framework has NO rotation curves at all (KERNEL_THEORY.md
      Finding C: "gives NO MOND at all", "dead twice over"). A wide-binary prediction cannot be
      settled by the reading that deletes the galaxy phenomenology.
  S5  THE CONSEQUENCE NOBODY PROPAGATED. The gate is a SEPARATE postulate with omega_c provably
      unforced, and the Jul 30 closure never mentions it. A one-pole low-pass passes DC at UNIT gain
      whatever omega_c is, and |a| is constant on a circle -- so the verdict INVERTS and the
      framework's branch is DC, gamma_v ~ 1.05-1.10 (alpha=1) / ~1.02 (alpha=2).
  S6  DOES THAT RESTORE FALSIFIABILITY? Only partly, and this section corrects an earlier draft of
      this script that claimed it did. The frozen document's trap has a SECOND branch -- the
      locally-DRAGGED frame, gamma_v - 1 ~ 1e-6, no gate involved. Withdrawing the gate NARROWS the
      trap from two branches to one ajar door (screening + differential drag), it does not resolve it.
  S7  What actually changes, what does not, and the correction notice owed.

NOTE ON THE AUDIT TOOL. check E paired these two files on shared tokens ['dcac','settled'] alone,
and their headline questions genuinely differ (branch selection vs Im K). The pairing was still
right, for a reason the token overlap could not see. Recorded as calibration, not as a win.

BOTH a0 FOOTINGS throughout. Exit 0 = ran and every internal check held. No hard-coded verdicts.
"""
from __future__ import annotations
import math
import sys

import numpy as np
import sympy as sp

ok: list[tuple[bool, str]] = []


def check(cond: bool, msg: str) -> bool:
    cond = bool(cond)
    ok.append((cond, msg))
    print(f"  [{'OK' if cond else 'FAIL'}] {msg}")
    return cond


def banner(t: str) -> None:
    print("\n" + "=" * 100)
    print(f"  {t}")
    print("=" * 100)


# ----------------------------------------------------------------- constants and both footings
C = 2.99792458e8
G = 6.67430e-11
AU = 1.495978707e11
KPC = 3.0856775814913673e19
MPC = 3.0856775814913673e22
MSUN = 1.98892e30
H0 = 67.66e3 / MPC
OMEGA_L = 0.6889
Z_FACTOR = math.sqrt(32.0 * math.pi / 3.0)

FOOTINGS = {
    "canon (rho_DE, cH_Lambda)": C * H0 * math.sqrt(OMEGA_L) / Z_FACTOR,
    "alt   (rho_tot, cH_0)": C * H0 / Z_FACTOR,
}


# ----------------------------------------------------------------- the two kernels, K(z) = mu(sqrt z)
def K_alpha1(z: complex) -> complex:
    """K_1(z) = (sqrt(1+4z) - 1) / (2 sqrt z); the framework's own RAR kernel."""
    z = complex(z)
    if z == 0:
        return 0.0 + 0.0j
    return (np.sqrt(1.0 + 4.0 * z) - 1.0) / (2.0 * np.sqrt(z))


def K_alpha2(z: complex) -> complex:
    """K_2(z) = sqrt(z) / sqrt(1+z); factored (NOT sqrt(z/(1+z))) to avoid sympy/numpy branch picking."""
    z = complex(z)
    return np.sqrt(z) / np.sqrt(1.0 + z)


KERNELS = {"alpha=1 (RAR kernel)": K_alpha1, "alpha=2 (ephemeris-safe)": K_alpha2}


def mu_fw(x: float) -> float:
    """The framework's own mu, inverted from g_obs^2 = g_bar^2 + g_bar a0.  mu(1) = (sqrt5-1)/2."""
    return (math.sqrt(1.0 + 4.0 * x * x) - 1.0) / (2.0 * x)


banner("S1  IS u_mu AN EIGENVECTOR OF Box_u ON A CIRCULAR ORBIT?  (exact, all four components)")

tau, R, Om = sp.symbols("tau R Omega", positive=True)
gam = sp.Symbol("gamma", positive=True)

# exact flat-space circular worldline, c = 1, coordinate time t = gamma*tau, phase Omega*t
x4 = sp.Matrix([gam * tau, R * sp.cos(gam * Om * tau), R * sp.sin(gam * Om * tau), 0])
u4 = x4.diff(tau)
a4 = u4.diff(tau)
box_u4 = u4.diff(tau, 2)  # Box_u u^mu = (u.grad)^2 u^mu = d^2 u^mu / dtau^2 on a worldline
eta = sp.diag(-1, 1, 1, 1)

norm = sp.simplify((u4.T * eta * u4)[0, 0])
print(f"  worldline   x^mu(tau) = {sp.simplify(x4.T)}")
print(f"  u.u = {norm}    -> equals -1 exactly under gamma = 1/sqrt(1 - R^2 Omega^2):")
gsub = {gam: 1 / sp.sqrt(1 - R**2 * Om**2)}
check(sp.simplify(norm.subs(gsub) + 1) == 0, "the worldline is correctly normalised, u.u = -1 exactly")

print("\n  Box_u u^mu, component by component:")
ratios = []
for i in range(4):
    comp = sp.simplify(box_u4[i])
    uc = sp.simplify(u4[i])
    r = sp.simplify(comp / uc) if uc != 0 else None
    ratios.append(r)
    print(f"    mu={i}:  Box_u u^mu = {comp}      ratio to u^mu = {r}")

check(sp.simplify(box_u4[0]) == 0 and sp.simplify(u4[0]) != 0,
      "TIME leg: Box_u u^0 = 0 while u^0 = gamma is NONZERO -> eigenvalue 0 on that leg")
check(all(sp.simplify(ratios[i] + (gam * Om) ** 2) == 0 for i in (1, 2)),
      "SPATIAL legs: Box_u u^i = -(gamma Omega)^2 u^i exactly")
check(sp.simplify(ratios[0] - ratios[1]) != 0,
      "the two eigenvalues DIFFER (0 vs -(gamma Omega)^2), so u_mu is NOT an eigenvector of Box_u")

resid_full = sp.simplify(box_u4 + Om**2 * u4)
check(any(sp.simplify(e) != 0 for e in resid_full),
      "the claim 'Box_u u_mu = -Omega^2 u_mu identically' is FALSE on the actual 4-velocity")

print("\n  MUTATION CONTROL -- reproduce the Jul 27 script's setup verbatim (2-component spatial vector,")
print("  proper time ~ coordinate time) and confirm its check would report PASS:")
t2 = sp.Symbol("t", positive=True)
x2 = sp.Matrix([R * sp.cos(Om * t2), R * sp.sin(Om * t2)])  # exactly mi_dcac_branch_settled S1
u2 = x2.diff(t2)
box_u2 = u2.diff(t2, 2)
resid2 = sp.simplify(box_u2 + Om**2 * u2)
print(f"    spatial-only residual  Box_u u + Omega^2 u = {resid2.T}")
check(all(sp.simplify(e) == 0 for e in resid2),
      "MUTATION: on the spatial block alone the false claim does report PASS -- so the defect is "
      "EXACTLY the omitted time leg, not a signature or convention quibble")


banner("S2  THE AMPLITUDE THAT CLAIM PROPAGATES INTO  (its S2 pulls K out of the contraction)")

print("  Claimed:   u^mu K(Box_u/a0^2) u_mu = K(z) (u.u) = -K(z)                [needs an eigenvector]")
print("  Correct:   u^mu K(Box_u/a0^2) u_mu = (-gamma^2) K(0) + (gamma^2 v^2) K(z)")
print("             and K(0) = mu(0) = 0 for BOTH kernels, so the time leg drops for a DIFFERENT")
print("             reason than claimed -- because K vanishes there, not because u is an eigenvector.\n")

for kname, Kf in KERNELS.items():
    k0 = Kf(0.0)
    check(abs(k0) < 1e-12, f"K(0) = 0 for {kname}  (|K(0)| = {abs(k0):.3e}) -> the time eigenspace drops")

# weights: eta_00 (u^0)^2 = -gamma^2 on the time leg, sum_i (u^i)^2 = gamma^2 v^2 on the spatial legs
w_time = sp.simplify((eta[0, 0] * u4[0] * u4[0]))
w_space = sp.simplify(sum(u4[i] * u4[i] for i in (1, 2, 3)))
print(f"  spectral weights:  time = {w_time}   spatial = {sp.simplify(w_space)}   (v = Omega R, c = 1)")
check(sp.simplify(w_time + w_space - norm) == 0,
      "the two weights sum to u.u, so the spectral decomposition is complete (no leg omitted)")

print("\n  How big is the correction the false step hides?  ratio = |correct| / |claimed| = gamma^2 v^2/c^2")
M_WB, R_WB = 1.5 * MSUN, 10e3 * AU
Om_wb = math.sqrt(G * M_WB / R_WB**3)
v_wb = Om_wb * R_WB
V_GAL = 200e3
systems = {
    f"wide binary 1.5 Msun @ 10 kAU": v_wb,
    f"galaxy disc (v = 200 km/s)": V_GAL,
}
print(f"  {'system':<34}{'v [m/s]':>13}{'gamma^2 v^2/c^2':>20}{'overstatement factor':>24}")
print("  " + "-" * 92)
for sname, v in systems.items():
    beta2 = (v / C) ** 2
    g2 = 1.0 / (1.0 - beta2)
    pref = g2 * beta2
    print(f"  {sname:<34}{v:>13.4e}{pref:>20.4e}{1.0/pref:>24.4e}")
    check(pref < 1e-5, f"the correct prefactor is <<1 for {sname} (claimed |u.u| = 1, actual {pref:.3e})")


banner("S3  IS THERE A CONTRADICTION WITH THEOREM B?  (the honest half -- answer: NO)")

print("  Theorem B (mi_dcac_split_settled S1, from u.u = -1 alone):  <Box_u>_u = +|a|^2, a MAGNITUDE.")
print("  The resolvent's surviving eigenvalue:                        -(gamma Omega)^2, a FREQUENCY.")
print("  These are DIFFERENT OBJECTS. The moment is the spectral weight-average; verify that exactly:\n")

moment = sp.simplify((w_time * 0 + w_space * (-(gam * Om) ** 2)) / (w_time + w_space))
a_sq = sp.simplify((a4.T * eta * a4)[0, 0])
print(f"  spectral weight-average of the eigenvalues = {moment}")
print(f"  a.a (proper acceleration squared)          = {a_sq}")
check(sp.simplify(sp.simplify(moment - a_sq).subs(gsub)) == 0,
      "the weight-average of the spectrum equals a.a EXACTLY -> Theorem B and the block form are "
      "CONSISTENT; neither refutes the other")
check(sp.simplify(a_sq.subs(gsub)) != 0 and sp.simplify((a_sq - (gam * Om) ** 2).subs(gsub)) != 0,
      "but the moment (+|a|^2) and the eigenvalue (-(gamma Omega)^2) are NOT the same number, so the "
      "DC/AC choice is a choice of OBJECT, not a theorem -- exactly what mi_offcircular_closure_collapse "
      "recorded as 'the projection IS the residual closure freedom'")

ratio_obj = sp.simplify(sp.sqrt(a_sq) / (gam * Om))
print(f"\n  ratio of the two candidate arguments' scales: sqrt(a.a) / (gamma Omega) = {ratio_obj}")
check(sp.simplify(ratio_obj - gam * Om * R) == 0,
      "that ratio is gamma*v/c -- the SAME v/c factor as Theorem 8's w/x = c/v, so the DC/AC split and "
      "the frequency-vs-magnitude axis mismatch are one and the same fact")


banner("S4  THE DEFECT THAT WITHDRAWS THE VERDICT: the action's reading is amplitude-free")

print("  If K's argument is the FREQUENCY z = -(c Omega/a0)^2, every real system sits far down the")
print("  negative axis, i.e. deep on K's branch cut. Check what |K| does there, for BOTH kernels:\n")
print(f"  {'footing':<26}{'a0 [m/s^2]':>13}  {'system':<22}{'z':>14}{'|K_a1|':>11}{'|K_a2|':>11}")
print("  " + "-" * 100)
mods: list[float] = []
for fname, a0 in FOOTINGS.items():
    for sname, (v, om) in {
        "wide binary 10 kAU": (v_wb, Om_wb),
        "galaxy disc @ 8 kpc": (V_GAL, V_GAL / (8.0 * KPC)),
    }.items():
        z = -((om * C / a0) ** 2)
        m1, m2 = abs(K_alpha1(z)), abs(K_alpha2(z))
        mods += [m1, m2]
        print(f"  {fname:<26}{a0:>13.4e}  {sname:<22}{z:>14.3e}{m1:>11.6f}{m2:>11.6f}")
        check(z < -0.25, f"{sname} sits past the branch point z = -1/4 on the {fname.split()[0]} footing")

check(all(abs(m - 1.0) < 1e-3 for m in mods),
      "|K| = 1 to better than 1e-3 for every system on BOTH kernels and BOTH footings -> the action's "
      "modification carries NO acceleration dependence: it is AMPLITUDE-FREE, not merely small")

print("\n  Against that, the amplitude the framework's LAW requires (its own mu, not McGaugh's nu):")
print(f"  {'x = g_obs/a0':>14}{'mu_fw(x)':>12}   {'|K| on the cut':>16}   {'mismatch':>10}")
print("  " + "-" * 62)
for xv in (10.0, 3.0, 1.0, 0.3, 0.1):
    m = mu_fw(xv)
    print(f"  {xv:>14.2f}{m:>12.6f}   {1.0:>16.6f}   {1.0/m:>10.3f}x")
check(abs(mu_fw(1.0) - (math.sqrt(5.0) - 1.0) / 2.0) < 1e-12,
      f"mu_fw(1) = {mu_fw(1.0):.6f} = (sqrt5-1)/2, the framework's own value at a = a0")
check(mu_fw(0.1) < 0.2 and mu_fw(10.0) > 0.9,
      "mu_fw runs from ~1 (Newtonian) to ->0 (deep), i.e. the law is intrinsically AMPLITUDE-CARRYING, "
      "which an |K| = 1 modification cannot supply at any Omega")

print("\n  So selecting the AC branch by 'reading Box_u off the action' selects the reading under which")
print("  the framework has no rotation curves at all. That is not a live branch to award a 5-sigma")
print("  prediction to; it is the reading KERNEL_THEORY.md Finding C already recorded as dead twice over,")
print("  and mi_action_eom_vs_rar_2026 (Jul 30) turned into a theorem one day after the Jul 27 verdict.")


banner("S5  THE CONSEQUENCE NOBODY PROPAGATED: a low-pass gate CANNOT suppress a DC argument")

print("""  The suppression Amendment 1 applied to the frozen pre-registration is Re G = 0.005-0.008 from a
  SEPARATE one-pole gate G(omega) = 1/(1 + i omega/omega_c). Two facts the corpus holds but never
  put side by side:
    * mi_omegac_anchor_2026 records that gate as a SEPARATE postulate whose omega_c is PROVABLY
      UNFORCED -- bracketed to only ~3 orders, with no intrinsic framework frequency within 3 decades.
      So it is not derived from K, and cannot inherit K's authority either way.
    * mi_dcac_split_settled_2026 (Jul 30) proved the closure's argument is |a|^2/a0^2 >= 0. It never
      mentions the gate, omega_c, or wide binaries -- checked by grep: zero hits. The theorem was
      never propagated to the prediction it governs.

  Put together, the gate argument inverts, and it does so WITHOUT needing omega_c at all:\n""")

# a one-pole low-pass has UNIT gain at DC, by construction -- no omega_c dependence
for om_c in (1.782e-14, 2.211e-14):
    ReG_dc = (1.0 / (1.0 + 1j * 0.0 / om_c)).real
    check(abs(ReG_dc - 1.0) < 1e-15,
          f"Re G(omega=0) = {ReG_dc:.6f} = 1 EXACTLY for omega_c = {om_c:.3e} rad/s -- a low-pass gate "
          f"passes DC with unit gain, whatever omega_c is")

amag_circ = sp.simplify(sp.sqrt(sp.simplify((a4.T * eta * a4)[0, 0])))
check(sp.simplify(sp.diff(amag_circ, tau)) == 0,
      "on a circular orbit |a| is EXACTLY constant (d|a|/dtau = 0, sympy) -- the Jul 27 script verified "
      "this itself -- so the closure's argument |a|^2/a0^2 is pure DC there")

SUPPRESSION = (0.005, 0.008)
print(f"\n  Amendment 1 applied Re G = {SUPPRESSION[0]}-{SUPPRESSION[1]} to obtain gamma_v = 1.0004-1.0006.")
print(f"  But that suppression belongs to a response whose argument is the FREQUENCY -(c Omega/a0)^2 --")
print(f"  i.e. to the amplitude-free, no-MOND reading of S4. Under the closure the framework actually")
print(f"  uses, the argument is DC, the gate's gain is 1, and the suppression does not apply.")
check(all(0.0 < s < 0.02 for s in SUPPRESSION),
      f"the suppression Amendment 1 applied ({SUPPRESSION[0]}-{SUPPRESSION[1]}) is 2 orders below the DC "
      f"gain of 1.0, so which branch is used moves gamma_v by the FULL boost, not a correction")

GAMMA_V = {
    "alpha=1  ungated (closure/DC)": (1.05, 1.10),
    "alpha=1  gated   (resolvent/AC, Amendment 1 as frozen)": (1.0004, 1.0006),
    "alpha=2  ungated (closure/DC)": (1.02, 1.02),
    "alpha=2  gated   (resolvent/AC, per Amendment (h)(i))": (1.00012, 1.00020),
}
print(f"\n  {'branch':<56}{'gamma_v':>18}")
print("  " + "-" * 76)
for bname, (lo, hi) in GAMMA_V.items():
    print(f"  {bname:<56}{(f'{lo:.5f}' if lo == hi else f'{lo:.4f}-{hi:.4f}'):>18}")
sep1 = (GAMMA_V["alpha=1  ungated (closure/DC)"][0] - 1.0) / (GAMMA_V["alpha=1  gated   (resolvent/AC, Amendment 1 as frozen)"][1] - 1.0)
check(sep1 > 50,
      f"the two branches differ by {sep1:.0f}x in (gamma_v - 1) on alpha=1 -- consistent with the "
      f"4.9-5.8 sigma separation the Jul 27 script itself quoted, so this is verdict-flipping, not cosmetic")

print("""
  => THE DC BRANCH IS THE FRAMEWORK'S BRANCH, and Amendment 1 has it backwards. This does not rest
     on omega_c (unit DC gain is omega_c-independent), on the footing, or on which kernel is used.
     It rests only on: the phenomenology runs on the closure (S4), the closure's argument is |a|^2
     (Theorem B, S3), |a|^2 is constant on a circle (verified above), and a low-pass gate passes DC.""")


banner("S6  DOES THIS RESTORE FALSIFIABILITY?  ONLY PARTLY -- there is a SECOND route to Newton")

print("""  The claim "Newtonian in 2-30 kAU is once again a KILL" does NOT follow from S5 alone, and checking
  it against STANDING.md's own record shows why. The frozen pre-registration carries a FALSIFIABILITY
  TRAP with TWO branches that between them cover both outcomes (STANDING.md:513-521):
    * the GATE branch    -- withdrawn here (S1-S5), gamma_v - 1 ~ 4e-4 to 6e-4
    * the FRAME branch   -- the locally-DRAGGED reading, gamma_v - 1 = 1.018e-6 (canon) / 1.483e-6
                            (alt), verified 4/4 across routes against the 1/(4y^2) asymptote at 50 dps
  The frame branch involves NO gate. So withdrawing the gate removes ONE of two routes to a Newtonian
  prediction, not both.\n""")

GAMMA_M1 = {
    "DC / ungated (this script's conclusion)": (0.05, 0.10),
    "frozen Amendment-3 undragged lower edge": (0.0182, 0.0182),
    "GATE branch (withdrawn here)": (4.0e-4, 6.0e-4),
    "FRAME branch / dragged (NOT touched here)": (1.018e-6, 1.483e-6),
}
print(f"  {'branch':<44}{'gamma_v - 1':>26}")
print("  " + "-" * 72)
for k, (lo, hi) in GAMMA_M1.items():
    print(f"  {k:<44}{(f'{lo:.4e}' if lo == hi else f'{lo:.3e} - {hi:.3e}'):>26}")

frame_hi = GAMMA_M1["FRAME branch / dragged (NOT touched here)"][1]
dc_lo = GAMMA_M1["DC / ungated (this script's conclusion)"][0]
check(frame_hi < dc_lo / 1e3,
      f"the FRAME branch ({frame_hi:.3e}) is >1000x below the DC prediction ({dc_lo:.3e}), so it too "
      f"reads as Newtonian in 2-30 kAU -- it is an INDEPENDENT route to the same observational outcome")
frame_lo = GAMMA_M1["FRAME branch / dragged (NOT touched here)"][0]
edge = GAMMA_M1["frozen Amendment-3 undragged lower edge"][0]
check(abs(edge / frame_lo - 17883.0) / 17883.0 < 0.01,
      f"the CANONICAL dragged reading sits {edge/frame_lo:.0f}x below the frozen undragged lower edge "
      f"{edge}, reproducing STANDING.md's recorded 17883x to better than 1%")
check(edge / frame_hi > 1e4,
      f"and the ALT dragged reading sits {edge/frame_hi:.0f}x below it, so the conclusion is "
      f"footing-independent")

print("""
  WHAT IS AND IS NOT LEFT OF THE FRAME BRANCH. STANDING.md:425 records the net position: "the
  locally-dragged frame has NO SURVIVING LOCAL PRESCRIPTION" -- scalar killed by irrotationality,
  vector by the measured GP-B/LARES magnitude shortfall (>= 2.11e5), uniform-anything by the
  drag-invariance theorem, non-local by the Carina mismatch -- "and screening + differential drag is
  the one door left ajar."

  => SO THE HONEST STATEMENT IS: withdrawing the gate branch NARROWS the trap from two branches to one
     narrow one. It does NOT resolve it. A Newtonian DR4 result could still be claimed through the
     screening + differential-drag residue unless that door is closed too. Falsifiability is
     SUBSTANTIALLY IMPROVED, not restored, and the pre-registration's trap remains Carl's to resolve
     by committing to one branch in the open before the data lands.""")

banner("S7  WHAT CHANGES, WHAT DOES NOT")

print("""  VERDICT ON mi_dcac_branch_settled_2026.py: SUPERSEDED. Its verdict line -- "THE AC BRANCH.
  This is not an interpretation or a preference" -- must be WITHDRAWN, on three grounds:
    (1) its S1 eigenvector claim is false as stated (S1 above, with the mutation control isolating
        the omitted time leg);
    (2) its S2 amplitude is wrong by a sign and by (v/c)^2 -- a factor 6.7e11 at the wide-binary
        scale it was written to decide (S2);
    (3) decisively, its STRATEGY fails: the action's literal reading is amplitude-free (S4), so it
        cannot be the reading the framework's phenomenology runs on, and a branch selected that way
        cannot carry a wide-binary prediction.

  AND THE VERDICT DOES NOT MERELY LAPSE -- IT INVERTS (S5). The framework's branch is the DC one.
  Its wide-binary prediction is the UNGATED boost: gamma_v ~ 1.05-1.10 (alpha=1) or ~1.02 (alpha=2),
  NOT the 1.0004-1.0006 that Amendment 1 registered. Consequences, stated plainly:
   * TWO PUBLISHED ARTEFACTS CARRY THE DEFECT. WB_CUBIC_GATE_LAW (Zenodo 10.5281/zenodo.21580093)
     asserts "On a circular orbit u_mu is an eigenvector of it" and "The result below no longer rests
     on a choice." The first is false as stated (S1); the second is the overclaim (S3, S4). And the
     FROZEN pre-registration's Amendment 1 cites the Jul 27 script by name as having SETTLED the
     branch "from the committed action".
   * FALSIFIABILITY IS SUBSTANTIALLY IMPROVED, NOT RESTORED (S6 -- and this corrects the first draft
     of this script, which claimed "restored"). Amendment 1's purpose was to stop a Newtonian DR4
     result being scored as a kill, by making 1.000 the framework's own prediction too. Withdrawing
     its basis removes the GATE route to that hedge. But the FRAME (locally-dragged) branch reaches
     the same observational place independently, at gamma_v - 1 = 1.018e-6 / 1.483e-6, with no gate
     involved -- so the frozen document's falsifiability trap is NARROWED from two branches to one,
     not resolved. What is left of the frame branch is a single ajar door, screening + differential
     drag (STANDING.md:425: the dragged frame has "no surviving local prescription"). Closing that
     door is what would make gamma_v ~ 1.02-1.09 a genuine risk taken in advance. Until then, do not
     claim the wide-binary front is falsifiable on the strength of this withdrawal alone.
   * AMENDMENT 6 IS OWED TO THE FROZEN DOCUMENT, and it is Carl's to file, not mine -- as is the
     already-owed Amendment 5 (the s^TX alpha=1-tail collapse). Filing it before DR4 is what keeps
     the inversion from being post-hoc. This is the second frozen-prereg row in two days found to
     rest on a retired or defective reading; the pattern, not just the row, is worth reporting.

  WHAT DOES NOT CHANGE.
   * No MEASUREMENT moves, and the gate law's cubic-rise algebra is not shown wrong here -- what it
     loses is the claim that the branch was fixed by the action rather than chosen.
   * Theorem B stands, unqualified (S3). So does the exact block form. They are compatible.
   * The RAR at 0.108 dex, the a0-line and the flat curves are measurements against a LAW and are
     untouched by which object the ACTION contracts.

  WHAT IS OWED.
   * A correction notice at the head of mi_dcac_branch_settled_2026.py pointing at this script and
     at mi_action_eom_vs_rar_2026.py. Carl's call whether to annotate or retire the file.
   * The DC/AC branch goes back on the open list. It is now visibly the SAME open item as the
     closure-vs-action gap, not an independent question -- which is a reduction in free content
     even though it is a withdrawal.

  CALIBRATION NOTE ON THE AUDIT TOOL. check E flagged this pair on token overlap ['dcac','settled']
  with no access to the physics, and the two files' headline questions really are different. The
  pairing was nonetheless correct. That is the tool working as a POINTER, not as a judge -- worth
  recording, since the same tool listed 256 further orphaned closures whose triage will look like
  this one: mostly false alarms, occasionally a withdrawn verdict.""")

banner("RESULT")
npass = sum(1 for c, _ in ok if c)
print(f"  {npass}/{len(ok)} checks held.")
if npass != len(ok):
    print("\n  FAILED CHECKS:")
    for c, m in ok:
        if not c:
            print(f"    - {m}")
    sys.exit(1)
print("  Exit 0: every internal check held, including the mutation control that isolates the defect.")
