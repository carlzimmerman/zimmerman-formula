#!/usr/bin/env python3
"""
THE NEW QUESTION (distinct from the five prior Koide attacks):
Is Q(SECTOR) a FORCED FUNCTION of the sector's gauge quantum numbers
(color N_c, weak isospin T3, hypercharge Y, the SO(10) 16 embedding) so that the
WHOLE pattern {lepton, up, down, neutrino} is OUTPUT by one rule, with leptons-2/3 a
DERIVED point?

DISCIPLINE (both-ways):
 (1) Any rule whose DEFINITION inputs 2/3 / Koide / r=sqrt2 / c=6 is the 169th re-labeling -> DEAD.
     The rule must map quantum-numbers (defined WITHOUT Koide) -> the c/Q value, and PREDICT all
     four sectors, not fit one.
 (2) A real result = a FORCED predictive rule (flag for re-verify).  A generic fit, or a rule that
     only works for one sector, = NULL.
 (3) Honest prior is WEAK (the c-values look generic).

We test the strongest natural candidate rules:
  - is c (or Q) a function of N_c?                 (color count: lepton 0/1, quark 3)
  - is c a function of electric charge |Q_em|?     (lepton -1, up +2/3, down -1/3, nu 0)
  - is c a function of (T3, Y)?                     (the full EW assignment)
  - is c a function of the SO(10)/SU(5) embedding position?
  - degrees-of-freedom counting (a quark has 3 colors -> 3x states)

A rule must be DEFINED on the quantum numbers ALONE and then output the measured c for ALL sectors.
sympy/mpmath dps>=30.  No 2/3 token in any rule definition.
"""
import numpy as np
import sympy as sp
import mpmath as mp
mp.mp.dps = 40

# ----------------------------------------------------------------------------
# Measured Koide-c per sector (c = 2/(1-Q), Q = sum m / (sum sqrt m)^2).
# Leptons: pole.  Quarks: MSbar at conventional scales (PDG 2024).  Neutrino: free in m1.
# ----------------------------------------------------------------------------
def koide_Q(m):
    m = np.array(m, float); s = np.sqrt(m)
    return m.sum()/s.sum()**2
def c_of(Q): return 2.0/(1.0-Q)

LEP   = [0.51099895000, 105.6583755, 1776.86]          # MeV, pole
UP    = [2.16e-3, 1.27, 162.5]                          # GeV, MSbar mixed-scale (u@2,c@mc,t@mt)
DOWN  = [4.67e-3, 93.4e-3, 4.18]                        # GeV, MSbar (d,s@2GeV; b@mb)
# neutrino: normal ordering, m1 ~ 0..0.05 eV.  Q is a FREE function of m1 -> no single c.
dm21, dm31 = 7.42e-5, 2.51e-3   # eV^2
def nu_Q(m1):
    m2 = np.sqrt(m1**2 + dm21); m3 = np.sqrt(m1**2 + dm31)
    return koide_Q([m1, m2, m3])

Q_lep, Q_up, Q_dn = koide_Q(LEP), koide_Q(UP), koide_Q(DOWN)
print("MEASURED Koide-c per sector  (c = 2/(1-Q)):")
print(f"  charged leptons : Q = {Q_lep:.5f}   c = {c_of(Q_lep):.4f}")
print(f"  up-type quarks  : Q = {Q_up:.5f}   c = {c_of(Q_up):.4f}")
print(f"  down-type quarks: Q = {Q_dn:.5f}   c = {c_of(Q_dn):.4f}")
print(f"  neutrinos (NO)  : Q(m1=0)    = {nu_Q(1e-9):.5f}   c = {c_of(nu_Q(1e-9)):.4f}")
print(f"                    Q(m1=0.01) = {nu_Q(0.01):.5f}   c = {c_of(nu_Q(0.01)):.4f}")
print(f"                    Q(m1=0.05) = {nu_Q(0.05):.5f}   c = {c_of(nu_Q(0.05)):.4f}")
print("  (Koide target: Q=2/3, c=6.  NEUTRINO Q IS A FREE FUNCTION OF m1 -> no fixed sector value.)")

# Gauge quantum numbers per sector (SM, left-handed convention; Y in GUT-free Q=T3+Y normalization)
# sector : (N_c, |Q_em|, T3, Y_L, SU(5) multiplet, SO(10) 16 slot)
QN = {
  'lepton':  dict(Nc=1, Qem=1.0,   T3=-0.5, Y=-0.5),
  'up':      dict(Nc=3, Qem=2/3.,  T3=+0.5, Y=+1/6.),
  'down':    dict(Nc=3, Qem=1/3.,  T3=-0.5, Y=+1/6.),
  'neutrino':dict(Nc=1, Qem=0.0,   T3=+0.5, Y=-0.5),
}
C_meas = {'lepton': c_of(Q_lep), 'up': c_of(Q_up), 'down': c_of(Q_dn)}  # neutrino has no fixed c

print("\n" + "="*78)
print("CANDIDATE RULE TESTS:  c_sector = f(quantum numbers),  f Koide-free, predicts ALL")
print("="*78)

# The honest fact we must beat: leptons c=6, up c=13.2, down c=7.45 (and nu undefined).
cL, cU, cD = C_meas['lepton'], C_meas['up'], C_meas['down']

# --- Rule family A: c = a + b*N_c  (does color count predict c?) ---
# 2 sectors share N_c=3 (up,down) but have DIFFERENT c (13.2 vs 7.45) -> N_c alone CANNOT
# be a function: same input, two outputs.  This is a hard no.
print("\n[A] c = f(N_c) ALONE:")
print(f"    up & down share N_c=3 but c_up={cU:.2f} != c_down={cD:.2f} (ratio {cU/cD:.2f}).")
print(f"    => c is NOT a function of N_c alone (same input, two outputs). FAILS as a function.")

# --- Rule family B: c = f(|Q_em|) ---
# lepton |Q|=1 -> c=6 ; up |Q|=2/3 -> c=13.2 ; down |Q|=1/3 -> c=7.45 ; nu |Q|=0 -> ?
# Try the natural monotone forms and FIT 2 sectors, PREDICT the 3rd (leave-one-out honesty).
print("\n[B] c = f(|Q_em|):  fit a 2-param form on 2 sectors, PREDICT the third (leave-one-out):")
import itertools
qem = {'lepton':1.0, 'up':2/3, 'down':1/3}
forms = {
  'c = A + B*|Q|'      : lambda q,A,B: A + B*q,
  'c = A + B/|Q|'      : lambda q,A,B: A + B/q,
  'c = A*|Q|**B'       : lambda q,A,B: A*q**B,
  'c = A + B*|Q|**2'   : lambda q,A,B: A + B*q**2,
}
secs = ['lepton','up','down']
for fname, f in forms.items():
    worst = 0
    detail = []
    for held in secs:
        fit = [s for s in secs if s != held]
        # solve 2 eqns for A,B
        A,B = sp.symbols('A B', real=True)
        eqs = [sp.Eq(f(qem[s],A,B), C_meas[s]) for s in fit]
        sol = sp.solve(eqs, [A,B], dict=True)
        if not sol:
            detail.append(f"{held}:no-sol"); worst=9; continue
        Av,Bv = float(sol[0][A]), float(sol[0][B])
        pred = f(qem[held],Av,Bv)
        err = abs(pred - C_meas[held])/C_meas[held]
        worst = max(worst, err)
        detail.append(f"hold {held}: pred c={float(pred):.2f} vs {C_meas[held]:.2f} ({err*100:.0f}%)")
    print(f"  {fname:<20} worst LOO err {worst*100:5.0f}%   " + " | ".join(detail))

# --- Rule family C: c = f(T3, Y) two-variable linear ---
print("\n[C] c = A + B*T3 + C*Y  (3 params, 3 charged sectors -> EXACT fit, 0 dof):")
A,Bc,Cc = sp.symbols('A B C', real=True)
eqs = [sp.Eq(A + Bc*QN[s]['T3'] + Cc*QN[s]['Y'], C_meas[s]) for s in secs]
sol = sp.solve(eqs,[A,Bc,Cc],dict=True)[0]
Av,Bv,Cv = [float(sol[k]) for k in (A,Bc,Cc)]
print(f"    Solved A={Av:.3f} B={Bv:.3f} C={Cv:.3f} -> EXACT (3 eq, 3 unk).")
print(f"    This is a GENERIC interpolation (0 dof), NOT a prediction. Test on neutrino:")
for m1 in [1e-9, 0.01, 0.05]:
    pred = Av + Bv*QN['neutrino']['T3'] + Cv*QN['neutrino']['Y']
    cnu  = c_of(nu_Q(m1))
    print(f"      neutrino (m1={m1:g}): rule predicts c={pred:.2f}, measured c={cnu:.2f} "
          f"(off {abs(pred-cnu)/abs(cnu)*100:.0f}%)  [and measured is m1-DEPENDENT -> no fixed target]")

# --- Rule family D: SO(10) 16 universality PREDICTION (the strong test) ---
print("\n[D] SO(10) 16-universality:  all of {nu,e,u,d} sit in ONE 16 spinor.")
print("    If Koide were forced by the 16-embedding, ALL FOUR would share the SAME c (=6).")
print(f"    Reality: c_lep={cL:.2f}, c_up={cU:.2f}, c_down={cD:.2f}, c_nu=FREE in m1.")
print("    => a single-rep universality PREDICTS family-universal Koide -> FALSIFIED by quarks+nu.")

# --- Rule family E: degrees-of-freedom / color-multiplicity weighting ---
# Idea: a quark mass enters weighted by N_c=3 (3 colors).  Does re-weighting sqrt-mass by
# N_c make quark Q -> 2/3?  This is the only DOF-counting that could be Koide-free.
print("\n[E] Color-DOF reweighting of the quark sqrt-mass vector (w_i = N_c=3, uniform):")
def koide_Q_weighted(m, w):
    m=np.array(m,float); w=np.array(w,float); s=np.sqrt(m)
    num = (w*m).sum(); den=(w*s).sum()**2 ;
    return num/den
# uniform weight cancels in the ratio -> identical.  Need a NON-uniform, QN-derived weight.
print(f"    uniform w=3: Q_up unchanged = {koide_Q_weighted(UP,[3,3,3]):.5f} (weight cancels).")
print("    Non-uniform color weighting would need a per-generation color factor (none exists;")
print("    all 3 generations are color triplets identically) -> no Koide-free reweighting helps.")

# ----------------------------------------------------------------------------
# VERDICT LOGIC
# ----------------------------------------------------------------------------
print("\n" + "="*78)
print("SUMMARY")
print("="*78)
print("- N_c alone: NOT a function (up,down share N_c, differ in c).")
print("- |Q_em|, (T3,Y): only EXACT by spending all dof (generic interpolation, 0 predictive dof);")
print("  leave-one-out errors are large; the neutrino has NO fixed c to predict (free in m1).")
print("- SO(10) 16-universality: a real PREDICTION, and it is FALSIFIED (would force all 4 = 2/3).")
print("- color-DOF reweighting: cancels in the ratio; no Koide-free reweighting pulls quarks to 2/3.")
print("=> No rule maps {Nc,Qem,T3,Y,16-embedding} -> c for ALL sectors except by generic fitting.")
print("   The pattern {0.667, 0.849, 0.731, free} is NOT output by one forced gauge-QN rule.")
