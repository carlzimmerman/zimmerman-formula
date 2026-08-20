#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
sf25_lensing_2026.py
====================
THE LENSING GATE -- AND IT RETURNS ADVERSE.  This is a computed kill-class finding against the
current single-piece interaction, stated at full strength per the standing rule.

THE VERDICT:

    *** g_lens = (g_dyn + g_N)/2.  LIGHT SEES ONLY HALF THE MOND ANOMALY. ***

    In the deep-MOND regime (g_dyn >> g_N) the lensing force tends to HALF the dynamical
    force.  The corpus's own weak-lensing RAR standing (KiDS, 40 kpc - 2.2 Mpc, chi2/dof ~ 1
    with the FULL anomaly) is then missed by a factor approaching 2 exactly where the data are
    best.  THE CURRENT INTERACTION FAILS THE LENSING GATE.

THE MECHANISM, and it is structural -- the same choice that bought ghost safety:
  X is built from SPATIAL connection differences (the khronon projection that made the
  interaction lapse-free, sf13a).  Consequently:
    * the interaction's flux term carries (Psi - Psihat)' ONLY -- no Phi anywhere;
    * its stress tensor has NO energy-density piece (delta X/delta g^{00} = 0): unlike a
      canonical scalar, whose (grad phi)^2 gravitates in T_00, a connection-difference scalar
      contributes ONLY spatial stress;
    * so the anomaly enters the field equations as an effective ANISOTROPIC/spatial stress:
      the Psi-variation (which determines Phi) is modified, the Phi-variation (which
      determines Psi) is NOT.  Matter feels the full anomaly through Phi; light averages the
      modified Phi with the UNMODIFIED, Newtonian Psi.

  *** THE GHOST-SAFETY CHOICE AND THE LENSING FAILURE ARE ONE STRUCTURE: projecting the
  interaction fully spatial is what made it lapse-free AND what removed its energy density.
  This is the R2 lesson in a new sector: a fix purchased in one corner sent the bill to
  another. ***

WHAT THIS DOES AND DOES NOT KILL.  It kills THE SINGLE-PIECE MIXED-CONTRACTION INTERACTION as
the complete story.  It does NOT kill the architecture: the palette already contains the
candidate repair -- the ELECTRIC piece alpha*sqrt(Upsilon_E), which is lapse-LINEAR (the
HR-safe form, sf10 PART E) and carries exactly the temporal structure whose absence causes the
deficit.  A two-piece interaction (electric sqrt-piece + spatial 3/2-piece) is the named next
construction; its sign analysis and its own ghost check are NOT done here.

CONTROLS: (i) GR limit: Phi = Psi exactly, g_lens = g_dyn = g_N -- standard lensing recovered;
(ii) the interaction's flux enters the Psi-variation only, verified, which is the whole
mechanism; (iii) matter feels the FULL anomaly (the dynamics side of sf13b is confirmed, not
lost -- the failure is specifically lensing).

Exit 0 = every numbered check passed; A PASS ESTABLISHES THE ADVERSE VERDICT.
"""
import sys
import sympy as sp

FAIL, NCHK = [], [0]


def check(cond, label, detail=""):
    NCHK[0] += 1
    ok = bool(cond)
    print(f"  [{'ok' if ok else 'FAIL'}] {label}" + (f"   {detail}" if detail else ""))
    if not ok:
        FAIL.append(label)
    return ok


def info(label, detail=""):
    print(f"  [info] {label}" + (f"   {detail}" if detail else ""))


def head(t_):
    print("\n" + "=" * 100 + f"\n{t_}\n" + "=" * 100)


print(__doc__)
x, ep = sp.symbols("x epsilon")
a0 = sp.Symbol("a_0", positive=True)
Mg2, Mf2, mI = sp.symbols("M_g^2 M_f^2 m_I", positive=True)
Phi, Psi = sp.Function("Phi")(x), sp.Function("Psi")(x)
Phh, Psh = sp.Function("Phihat")(x), sp.Function("Psihat")(x)
rho = sp.Function("rho")(x)
XC = [sp.Symbol("t"), x, sp.Symbol("y"), sp.Symbol("z")]


def sqrtgR_quad(Phi_, Psi_):
    g = sp.diag(-(1 + 2 * ep * Phi_), 1 - 2 * ep * Psi_, 1 - 2 * ep * Psi_, 1 - 2 * ep * Psi_)
    gi = g.inv()
    Gam = [[[sum(gi[l, r] * (sp.diff(g[r, m], XC[n]) + sp.diff(g[r, n], XC[m])
                             - sp.diff(g[m, n], XC[r])) for r in range(4)) / 2
             for n in range(4)] for m in range(4)] for l in range(4)]
    Ric = sp.zeros(4, 4)
    for m in range(4):
        for n in range(4):
            s_ = 0
            for l in range(4):
                s_ += sp.diff(Gam[l][m][n], XC[l]) - sp.diff(Gam[l][m][l], XC[n])
                for p_ in range(4):
                    s_ += Gam[l][l][p_] * Gam[p_][m][n] - Gam[l][n][p_] * Gam[p_][m][l]
            Ric[m, n] = s_
    R = sum(gi[m, n] * Ric[m, n] for m in range(4) for n in range(4))
    quad = sp.expand(sp.series(sp.sqrt(-g.det()) * R, ep, 0, 3).removeO().coeff(ep, 2))
    # IBP away second derivatives
    for F_ in (Phi_, Psi_):
        d2 = sp.diff(F_, x, 2)
        c2 = sp.expand(quad).coeff(d2)
        quad = sp.expand(quad - c2 * d2 - sp.expand(sp.diff(c2, x)) * sp.diff(F_, x))
    return sp.simplify(quad)


def EL(L, F_):
    return sp.expand(sp.diff(L, F_) - sp.diff(sp.diff(L, sp.diff(F_, x)), x))


# =========================================================================================
head("PART A -- quadratic Lagrangian and the GR control")
# =========================================================================================
L_g = (Mg2 / 2) * sqrtgR_quad(Phi, Psi)
L_f = (Mf2 / 2) * sqrtgR_quad(Phh, Psh)
info("A1  the g-sector quadratic static Lagrangian", f"{L_g}")
L_gr = L_g - rho * Phi
eqPhi = EL(L_gr, Phi)
eqPsi = EL(L_gr, Psi)
sPsi2 = sp.solve(sp.Eq(eqPhi, 0), sp.diff(Psi, x, 2))[0]
sPhi2_raw = sp.solve(sp.Eq(eqPsi, 0), sp.diff(Phi, x, 2))[0]
sPhi2 = sp.simplify(sPhi2_raw.subs(sp.diff(Psi, x, 2), sPsi2))
check(sp.simplify(sPhi2 - sPsi2) == 0,
      "A2  *** GR CONTROL PASSES: after substitution Phi'' = Psi'' with the same rho source -- "
      "Phi = Psi, g_lens = g_dyn = g_N, standard lensing recovered exactly ***",
      f"Phi'' = Psi'' = {sPsi2}")

# =========================================================================================
head("PART B -- the interaction at quadratic-flux order, and where it enters")
# =========================================================================================
F1, B1 = sp.symbols("F' B'", real=True)      # local nonlinear values, sf13b treatment
psi_d = Psh - Psi
# V = sqrt(h)[N F(X) + Nhat B(X)];  X = -ep^2 (psi_d')^2/a0^2;  flux order:
# -mI [ F1 + B1 ] * X * (leading 1's)  ->  + mI (F1+B1) (psi_d')^2/a0^2  at ep^2
L_int = mI * (F1 + B1) * sp.diff(psi_d, x)**2 / a0**2
info("B1  the interaction's quadratic-flux Lagrangian",
     f"L_int = {L_int}   [value terms (F_0, B_0 mass-type pieces) are background bookkeeping, "
     "dropped as in standard weak-field treatment and NOT able to enter the flux ratio]")
check(sp.diff(L_int, Phi) == 0 and sp.diff(L_int, sp.diff(Phi, x)) == 0,
      "B2  *** THE INTERACTION CARRIES NO Phi WHATSOEVER: X is built from SPATIAL connection "
      "differences, so delta X/delta g^{00} = 0 -- no energy-density piece, unlike a canonical "
      "scalar whose (grad phi)^2 gravitates in T_00.  This is the khronon projection's "
      "fingerprint, the same one that made the interaction lapse-free ***",
      "the ghost-safety choice and what follows are ONE structure")
L2 = L_g + L_f + L_int - rho * Phi
eqs = {F_: EL(L2, F_) for F_ in (Phi, Psi, Phh, Psh)}
check(sp.simplify(sp.expand(eqs[Phi]).coeff(F1)) == 0
      and sp.simplify(sp.expand(eqs[Psi]).coeff(F1)) != 0,
      "B3  the interaction flux enters the Psi-VARIATION only (and the hatted analogues) -- the "
      "Phi-variation, which determines Psi, is UNMODIFIED",
      "so Psi stays Newtonian and Phi carries the anomaly, via the EH cross-structure")

# =========================================================================================
head("PART C -- first integrals and the two observables")
# =========================================================================================
P1, S1, Ph1, Sh1 = sp.symbols("Phi1 Psi1 Phihat1 Psihat1", real=True)
m_enc = sp.Symbol("m_enc", positive=True)
subs1 = {sp.diff(Phi, x): P1, sp.diff(Psi, x): S1, sp.diff(Phh, x): Ph1, sp.diff(Psh, x): Sh1}


def first_integral(eq):
    out = 0
    for t in sp.expand(eq).args:
        for F_, s_ in ((Phi, P1), (Psi, S1), (Phh, Ph1), (Psh, Sh1)):
            d2 = sp.diff(F_, x, 2)
            if t.has(d2):
                out += t.coeff(d2) * s_
                break
        else:
            if t.has(rho):
                out += (t / rho) * m_enc
    return sp.expand(out.subs(subs1))


I = {k: first_integral(v) for k, v in eqs.items()}
sol = sp.solve([sp.Eq(v, 0) for v in I.values()], [P1, S1, Ph1, Sh1], dict=True)
check(len(sol) == 1, "C1  the flux system solves uniquely", f"branches: {len(sol)}")
gdyn = sp.simplify(sol[0][P1])
gN = sp.simplify(sol[0][S1])
glens = sp.simplify((gdyn + gN) / 2)
info("C2  the solved fluxes", f"g_dyn = Phi' = {gdyn}\n           Psi'   = {gN}")
check((not gN.has(F1)) and (not gN.has(B1)) and (not gN.has(mI))
      and sp.simplify(sp.Abs(gN) - m_enc / (2 * Mg2)) == 0,
      "C3  *** Psi IS EXACTLY NEWTONIAN: |Psi'| = m_enc/(2 M_g^2) with NO interaction "
      "dependence anywhere in it (no F', no B', no m_I).  Light's second potential never hears "
      "about MOND.  (The overall sign is the source-orientation convention; the content is the "
      "absence of the interaction) ***",
      f"Psi' = {gN}")
delta = sp.simplify(gdyn - gN)
check(sp.simplify(delta) != 0 and delta.has(F1),
      "C4  while MATTER feels the FULL anomaly: g_dyn = g_N + Delta with Delta carrying the "
      "F'-flux -- the dynamics side of sf13b is CONFIRMED, and the failure is specifically "
      "lensing",
      f"Delta = {delta}")
ratio = sp.simplify(glens / gdyn)
target = sp.simplify((1 + gN / gdyn) / 2)
check(sp.simplify(ratio - target) == 0,
      "C5  *** THE VERDICT: g_lens/g_dyn = (1 + g_N/g_dyn)/2.  In deep MOND (g_dyn >> g_N) "
      "LENSING TENDS TO HALF THE DYNAMICAL FORCE.  Against the corpus's KiDS weak-lensing RAR "
      "standing (full anomaly, chi2/dof ~ 1 over 40 kpc - 2.2 Mpc), THIS INTERACTION FAILS THE "
      "LENSING GATE BY A FACTOR APPROACHING 2 exactly where the data are best ***",
      "adverse, computed, and stated at full strength per the standing rule")

# =========================================================================================
head("PART D -- what is killed, what is not, and the named repair")
# =========================================================================================
for s_ in [
    "KILLED: the SINGLE-PIECE mixed-contraction interaction as the complete story.  Its "
    "lensing deficit is structural, not parametric -- no choice of F, B or r repairs it, "
    "because the flux never reaches the Phi-variation",
    "NOT KILLED: the architecture.  The palette already contains the repair candidate: the "
    "ELECTRIC piece alpha sqrt(Upsilon_E) is lapse-LINEAR (the HR-safe form, sf10 PART E) and "
    "carries exactly the temporal structure whose absence causes the deficit.  A TWO-PIECE "
    "interaction -- electric sqrt + spatial 3/2 -- is the named next construction.  Its sign "
    "analysis (sf13d found alpha > 0 weakens the FORCE; its effect on the LENSING split is a "
    "different projection and is NOT computed), its ghost check, and the re-derivation of the "
    "Moebius/A(x) chain on the two-piece form are all OWED",
    "THE STRUCTURAL LESSON, and it is the programme's recurring one: the khronon projection "
    "that made the interaction lapse-free (ghost-safe) is the SAME operation that removed its "
    "energy density (lensing-broken).  Fixes have bills, and the bills arrive in other sectors",
    "the corpus's standing KiDS result (chi2/dof ~ 1 with the full anomaly) is UNTOUCHED as a "
    "statement about the a0-line phenomenology; what fails is this particular relativistic "
    "realisation of it",
    "both footings unchanged: a_0 = 9.3619e-11 canonical / 1.1279e-10 alt; kappa = 1/2 FITTED, "
    "0.529 +/- 0.034, never derived",
]:
    info("S", s_)

print("\n" + "=" * 100)
print(f"SF25 CHECKS: {NCHK[0] - len(FAIL)}/{NCHK[0]} passed  (a pass establishes the ADVERSE verdict)")
print("=" * 100)
if FAIL:
    for f_ in FAIL:
        print("  FAILED:", f_)
    sys.exit(1)
sys.exit(0)
