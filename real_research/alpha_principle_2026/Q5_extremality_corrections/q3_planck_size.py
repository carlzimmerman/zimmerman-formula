#!/usr/bin/env python3
"""Q5 / item 3: how well can the classical relation r = n l_P/(2 sqrt(alpha)) of the minimal magnetic extremal RN
object be trusted?  Estimates (assumptions declared in Q5_PREREGISTRATION.md and printed below).

Real run:     python3 q3_planck_size.py           -> exit 0
MUTATE ctrl:  python3 q3_planck_size.py MUTATE    -> the ONLY trigger is the literal argv 'MUTATE'
              (n = 10^4 quanta and zero log coefficient: the 'all unavoidable effects exceed the bar by > 1e6' check must FAIL, exit 1)
Verdict rule (registered): the four UNAVOIDABLE effects (1/S, |log term|/S, Schwarzian scale relative to 1/r, e B r^2) each
exceed the bar 5e-10 by > 1e6.  Assumption-dependent effects (higher-derivative size, spectrum) are reported, not used.
"""
import sys
import numpy as np
import sympy as sp

MUTATE = (len(sys.argv) > 1 and sys.argv[1] == 'MUTATE')
res = []
def check(name, ok, info=""):
    res.append(bool(ok))
    print(("[PASS] " if ok else "[FAIL] ") + name + (("  " + info) if info else ""))

BAR = 5e-10
n = 1e4 if MUTATE else 1.0
sen_coeff_J0 = 0.0 if MUTATE else 241.0 / 45.0        # -(241/45) ln A_H: printed eq (3.19) of 1204.4061 (-3 - 106/45)
sen_coeff_K1 = 0.0 if MUTATE else (2.0 + 106.0 / 45.0)  # J_3 fixed only: -2 - 106/45 (same paper, text before eq 3.19)
alphas = {'Thomson': 1 / 137.035999177, 'alpha(m_P)': 1 / 104.94}

# ---- Schwarzian coefficient, exact (sympy), G = 1
rp, rm, T = sp.symbols('rp rm T', positive=True)
Q = sp.symbols('Q', positive=True)
Tem = (rp - rm) / (4 * sp.pi * rp**2)
# fixed charge Q^2 = rp*rm  ->  rm = Q^2/rp ; solve T(rp) = T for rp near Q
eps = sp.symbols('eps')
rp_series = Q + sp.Symbol('a1') * T + sp.Symbol('a2') * T**2
eq = sp.series(sp.simplify(((rp_series - Q**2 / rp_series) / (4 * sp.pi * rp_series**2)) - T), T, 0, 3).removeO()
sol = sp.solve([sp.expand(eq).coeff(T, 1), sp.expand(eq).coeff(T, 2)], [sp.Symbol('a1'), sp.Symbol('a2')], dict=True)[0]
S_T = sp.series(sp.pi * rp_series.subs(sol)**2, T, 0, 2).removeO()
Csch = sp.simplify(sp.diff(S_T, T))
print("near-extremal RN at fixed Q (G=1): r_+ = Q + (%s) T + ... ;  S = pi Q^2 + (%s) T + ...  =>  C = dS/dT|_0 = %s" % (sol[sp.Symbol('a1')], Csch, Csch))
check("Q3-c0 Schwarzian coefficient C = dS/dT = 4 pi^2 Q^3 (G=1), from r_+ - r_- = 4 pi T r_+^2", sp.simplify(Csch - 4 * sp.pi**2 * Q**3) == 0)

print("\n=== assumptions: (i) tree-level+one-loop EM-gravity only for Q3-b (SM massless spectrum not added); (ii) Schwarzian universality assumed at Q ~ 6 l_P;")
print("    (iii) constant-B single-electron loop for Q3-e; (iv) d0 = delta l_P^2 with delta bracket as registered. All are ORDER-OF-MAGNITUDE.\n")

eff = {}
for lab, al in alphas.items():
    r = n / (2 * np.sqrt(al))           # l_P
    S = np.pi * n**2 / (4 * al)
    A = 4 * np.pi * r**2
    lnA = np.log(A)
    log_J0 = sen_coeff_J0 * lnA; log_K1 = sen_coeff_K1 * lnA
    C = 4 * np.pi**2 * r**3
    Egap_rel_inv_r = (1 / C) / (1 / r)          # (gap scale) / (1/r)
    Egap_rel_M = (1 / C) / r                    # (gap scale) / M, M = r (G=1)
    eBr2 = n / 2
    mP = 1.220890e19; me = 0.51099895e-3
    eB = eBr2 / r**2                            # in m_P^2
    vp = al / (3 * np.pi) * np.log(eB * (mP / me)**2)
    x = 1 / r**2
    korder = int(np.ceil(np.log(BAR) / np.log(x)))
    print(f"--- {lab}: alpha = 1/{1/al:.3f}, n = {n:g}")
    print(f"  r = {r:.4f} l_P, A_H = {A:.2f} l_P^2, S = pi n^2/(4 alpha) = {S:.4f} ;  1/S = {1/S:.4e}")
    print(f"  Q3-b log term (Sen, EM+gravity only): -(241/45) ln A_H = {-log_J0:.3f} ; (J_3 only: {-log_K1:.3f}) ; |log|/S = {abs(log_J0)/S:.3f} ({abs(log_K1)/S:.3f}); non-universal constant unknown")
    print(f"  Q3-c Schwarzian: C = 4 pi^2 r^3 = {C:.4e} l_P^3 ; gap ~ 1/C = {1/C:.3e} m_P ; (1/C)/(1/r) = {Egap_rel_inv_r:.3e} ; (1/C)/M = {Egap_rel_M:.3e}")
    print(f"  Q3-e e B r^2 = n/2 = {eBr2:g} at the horizon (Dirac); m_e r = {me/mP*r:.3e} (electron effectively massless on the horizon scale);")
    print(f"       vacuum-polarisation (electron loop, constant B) delta = (alpha/3pi) ln(eB/m_e^2) = {vp:.4f}")
    print(f"  Q3-g expansion parameter l_P^2/r^2 = {x:.5f}; orders k with x^k < {BAR:g}: k = {korder}")
    print(f"  non-perturbative e^-S = {np.exp(-S):.3e}")
    eff[lab] = dict(inv_S=1 / S, logS=abs(log_J0) / S, sch=Egap_rel_inv_r, eBr2=eBr2, sch_mass=Egap_rel_M)
    for dl in (1e-4, 1e-3, 1e-2, 1e-1, 1.0):
        print(f"       Q3-d higher-derivative |Delta z| (magnetic, delta={dl:g}) = {0.4*dl*x:.3e}  ({0.4*dl*x/BAR:.2e} x bar)")

# ---- coupling-scale / spectrum (Q3-f)
print("\nQ3-f scale mismatch and spectrum sensitivity")
a_th, a_mp = 137.035999177, 104.94
print(f"  1/alpha(m_P)/1/alpha(Thomson) - 1 = {a_mp/a_th - 1:+.4f}  (lane A, one loop, SM content)")
mP_GeV = 1.220890e19
for M in (1e3, 1e10, 1e17):
    d = 2 / (3 * np.pi) * np.log(mP_GeV / M)
    print(f"  one extra unit-charge Dirac fermion at {M:.0e} GeV shifts 1/alpha(m_P) by -{d:.4f} = {d/a_mp:.4f} relative  ({d/a_mp/BAR:.2e} x bar)")
print("  RECALLED (not scripted): hadronic vacuum polarisation Delta alpha_had^(5)(m_Z) = 0.0276 +- 0.0001 -> ~1e-4 relative uncertainty in alpha(m_Z), hence in any run to m_P.")
dabs = BAR * a_mp
print(f"  bar on 1/alpha(m_P): {dabs:.2e} absolute; a single fermion threshold must then be located to delta ln M = {dabs/(2/(3*np.pi)):.2e}")

# ---- verdict
print("\nVerdict rule (registered): unavoidable effects vs bar (>1e6 x bar each):")
allok = True
for lab in alphas:
    e = eff[lab]
    for k in ('inv_S', 'logS', 'sch', 'eBr2'):
        ratio = e[k] / BAR
        print(f"   {lab:10s} {k:6s} = {e[k]:.3e}  -> {ratio:.2e} x bar")
        allok &= ratio > 1e6
    print(f"   {lab:10s} (unregistered, reported) Schwarzian gap / M = {e['sch_mass']:.3e} -> {e['sch_mass']/BAR:.2e} x bar")
check("Q3-H all four unavoidable effects exceed the bar 5e-10 by > 1e6 at the minimal magnetic object (both alpha scales)", allok)
n_needed = np.sqrt(0.4 * 0.16 * 4 * alphas['Thomson'] / BAR)
print(f"\nprecision vs minimality: magnetic object with |Delta z| < 5e-10 at loop-natural delta = 0.16 needs n >= {n_needed:.3e} quanta;")
print("there r ~ n/(2 sqrt(alpha)) and the geometry depends on alpha and n only through alpha n^2 (lane N4): alpha is not separated from n.")
print("\nSUMMARY: %d/%d checks pass (MUTATE=%s)" % (sum(res), len(res), MUTATE))
sys.exit(0 if all(res) else 1)
