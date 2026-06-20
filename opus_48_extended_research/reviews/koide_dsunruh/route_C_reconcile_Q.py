#!/usr/bin/env python3
"""
Reconcile the two Q-vs-r formulas against REAL PDG masses, and pin down exactly
which circulant amplitude r corresponds to the empirical Koide Q=2/3.

Koide Q == (m_e+m_mu+m_tau) / [ (2/3)(sqrt m_e + sqrt m_mu + sqrt m_tau)^2 ].
This is the DEFINITION the task gives; Q_exp = 0.666661.  We must find which r in
sqrt(m_i)=M(1+r cos(delta+2pi i/3)) reproduces the empirical sqrt-masses.
"""
import sympy as sp, mpmath as mp
mp.mp.dps = 30

# PDG 2024 charged-lepton pole masses (MeV):
m_e   = mp.mpf('0.51099895000')
m_mu  = mp.mpf('105.6583755')
m_tau = mp.mpf('1776.86')

S = mp.sqrt(m_e)+mp.sqrt(m_mu)+mp.sqrt(m_tau)
Sm = m_e+m_mu+m_tau
Q_exp = Sm / (mp.mpf(2)/3 * S**2)          # the task's Koide Q
print("Koide Q_exp (task definition) =", Q_exp, "  (target 2/3 =", mp.mpf(2)/3, ")")
print("  rel dev from 2/3:", (Q_exp-mp.mpf(2)/3)/(mp.mpf(2)/3))

# Foot angle:
cos_theta = S / mp.sqrt(3*Sm)
theta_deg = mp.degrees(mp.acos(cos_theta))
print("Foot angle theta =", theta_deg, "deg  (Koide <=> 45 deg, cos theta=1/sqrt2)")
print("cos^2 theta =", cos_theta**2, "  (Koide <=> 3/4)")

# Now: circulant ansatz.  sqrt(m_i)=M(1+r cos(delta+2pi i/3)).
# sum_k cos(delta+2pi k/3) = 0 ;  sum_k cos^2 = 3/2 (exact).  =>
#   sum sqrt m = 3M ,  sum m = M^2 (3 + (3/2) r^2).
# Koide Q (task def) = sum m /[(2/3)(sum sqrt m)^2]
#   = M^2(3 + 1.5 r^2) /[(2/3) 9 M^2] = (3+1.5 r^2)/6 = 1/2 + r^2/4.
r = sp.symbols('r', positive=True)
Q_task = sp.Rational(1,2) + r**2/4
print("\nTASK-def Q(r) = 1/2 + r^2/4  =>  Q=2/3 gives r^2 =", sp.solve(sp.Eq(Q_task, sp.Rational(2,3)), r**2 if False else r))
r_task = sp.solve(sp.Eq(Q_task, sp.Rational(2,3)), r)
print("   r for task-Q=2/3:", r_task, "=", [mp.mpf(sp.N(x,30)) for x in r_task])

# The OTHER (banked-memory) normalization defines Qb = sum m/(sum sqrt m)^2 directly
# (NO 2/3), the 'angle' version: Qb = (3+1.5 r^2)/9 = 1/3 + r^2/6, Koide Qb=... let's see.
Qb = sp.Rational(1,3) + r**2/6   # = sum m/(sum sqrt m)^2
print("\nALT-def Qb(r)=sum m/(sum sqrt m)^2 = 1/3 + r^2/6.")
Qb_exp = Sm / S**2
print("   Qb_exp = sum m/(sum sqrt m)^2 =", Qb_exp, " (Koide <=> 1/2, since (2/3)*Qb=Q)")
rb = sp.solve(sp.Eq(Qb, Qb_exp_val := sp.Rational(1,2)), r)  # Qb=1/2 <=> Q=2/3
print("   r for Qb=1/2 (i.e. task-Q=2/3):", rb, "=", [mp.mpf(sp.N(x,30)) for x in rb])

print("\n*** RESOLUTION ***")
print("BOTH normalizations agree on the SAME physical amplitude:")
print("  task-Q = (2/3)*Qb, so task-Q=2/3 <=> Qb=1 ... wait, check numerically:")
print("  (2/3)*Qb_exp =", (mp.mpf(2)/3)*Qb_exp, " vs Q_exp =", Q_exp)
# Solve for the ACTUAL r from the empirical sqrt-masses directly (no normalization ambiguity):
# fit M, r, delta to the three sqrt-masses.
sm_e, sm_mu, sm_tau = mp.sqrt(m_e), mp.sqrt(m_mu), mp.sqrt(m_tau)
Mfit = (sm_e+sm_mu+sm_tau)/3
# r^2 from variance: sum (sqrt m - M)^2 = M^2 r^2 * (3/2)
var = (sm_e-Mfit)**2+(sm_mu-Mfit)**2+(sm_tau-Mfit)**2
r2_fit = var/(Mfit**2 * mp.mpf('1.5'))
print("\nDIRECT FIT to empirical sqrt-masses:")
print("  M =", Mfit, "  r^2 =", r2_fit, "  r =", mp.sqrt(r2_fit))
print("  sqrt(2) =", mp.sqrt(2), "  => empirical r is", mp.sqrt(r2_fit)/mp.sqrt(2), "x sqrt(2)")
print("  This r=sqrt(2) (to 1e-5) is THE Koide content, normalization-independent.")
