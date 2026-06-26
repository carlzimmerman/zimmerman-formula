#!/usr/bin/env python3
"""
ATTACK 5: FDR-controlled brute-force hunt for SM mass relations involving the
framework's geometric symbols {Z=sqrt(32pi/3), kappa=1/2, kernel=sqrt(8pi/3),
pi, small integers, dS-series labels}.

HONEST GOAL: for each claimed "hit" report the LOOK-ELSEWHERE / FDR-corrected
expected number of chance hits. A relation is FRIED only if it survives FDR;
otherwise it is BAKED (coincidence).

Author: Attack-5 agent. Everything sympy/numpy-verified.
"""
import numpy as np
import sympy as sp
from itertools import product, combinations
from fractions import Fraction

np.random.seed(0)

# ----------------------------------------------------------------------
# 0. PDG 2024 masses (MeV) -- central values, with 1-sigma where it matters
# ----------------------------------------------------------------------
# Charged leptons (extremely precise -- these drive Koide)
m_e   = 0.51099895000   # MeV  (PDG, exact-ish)
m_mu  = 105.6583755     # MeV
m_tau = 1776.86         # MeV  (+-0.12)
m_tau_err = 0.12

# Quarks (MS-bar, large uncertainties)
m_u, m_d, m_s = 2.16, 4.67, 93.4          # MeV (2 GeV)
m_c, m_b      = 1270.0, 4180.0            # MeV
m_t           = 172570.0                  # MeV (pole ~172.57 GeV)

# Bosons / EW
m_W, m_Z, m_H = 80377.0, 91187.6, 125250.0  # MeV
m_p, m_n      = 938.27208816, 939.5654205   # MeV proton/neutron
v_EW          = 246220.0                     # MeV (Higgs vev)
alpha_em_inv  = 137.035999084
sin2thetaW    = 0.23122                       # on-shell-ish
G_F           = 1.1663787e-5                  # GeV^-2

# ----------------------------------------------------------------------
# 1. Framework symbol set
# ----------------------------------------------------------------------
pi = np.pi
Z       = np.sqrt(32*pi/3)        # = 5.7888...
kernel  = np.sqrt(8*pi/3)         # = Z/2 = 2.8944...
kappa   = 0.5
sqrtpi  = np.sqrt(pi)

print("="*70)
print("FRAMEWORK CONSTANTS")
print("="*70)
print(f"Z       = sqrt(32pi/3) = {Z:.6f}")
print(f"kernel  = sqrt(8pi/3)  = {kernel:.6f}  (= Z/2)")
print(f"kappa   = 1/2          = {kappa}")
print(f"pi      = {pi:.6f}")

# Koide actual value
Q_koide = (m_e + m_mu + m_tau) / (np.sqrt(m_e)+np.sqrt(m_mu)+np.sqrt(m_tau))**2
print("\n"+"="*70)
print("KOIDE FORMULA (charged leptons)")
print("="*70)
print(f"Q_koide measured = {Q_koide:.8f}")
print(f"2/3              = {2/3:.8f}")
print(f"deviation from 2/3 = {(Q_koide-2/3):+.2e}  ({(Q_koide-2/3)/(2/3)*100:+.4f}%)")

# propagate tau error into Q
def koide(me,mm,mt):
    return (me+mm+mt)/(np.sqrt(me)+np.sqrt(mm)+np.sqrt(mt))**2
dQ = abs(koide(m_e,m_mu,m_tau+m_tau_err)-Q_koide)
print(f"Q_koide 1-sigma (from tau) = +-{dQ:.2e}")
print(f"  -> 2/3 lies {(2/3 - Q_koide)/dQ:+.2f} sigma from measured Q")

print("\nNOTE: 2/3 is a PURE RATIONAL. It needs NO framework symbol. The framework")
print("merely *re-labels* 2/3 as CUBE/GAUGE=8/12 or 'kappa+something'. That is a")
print("RE-DESCRIPTION, not a derivation, UNLESS the framework forces WHY the lepton")
print("mass matrix is democratic+circulant (the actual Koide mechanism question).")

# ----------------------------------------------------------------------
# 2. THE LOOK-ELSEWHERE SET for 2/3
#    How many simple O(1) combinations of the allowed symbols land within the
#    measured tolerance of Q_koide?  Koide is special precisely because the
#    target (2/3) is a tiny-denominator rational. Quantify.
# ----------------------------------------------------------------------
print("\n"+"="*70)
print("FDR TEST A: is hitting Q=2/3 with framework symbols surprising?")
print("="*70)
# Build a symbol pool the framework is 'allowed' to use, per the attack spec.
symbols = {
    'Z': Z, 'kernel': kernel, 'kappa': kappa, 'pi': pi, 'sqrtpi': sqrtpi,
    '1':1.,'2':2.,'3':3.,'4':4.,'5':5.,'6':6.,'7':7.,'8':8.,
    '9':9.,'10':10.,'11':11.,'12':12.,'16':16.,
    # dS-series labels / cube-geometry integers the corpus uses:
    'CUBE':8.,'GAUGE':12.,'BEK':4.,'Ngen':3.,
}
names = list(symbols)
vals  = np.array([symbols[n] for n in names])

# enumerate ratios a/b and products over the pool (single-symbol and pairwise)
combos = []  # (value, label)
for i,n in enumerate(names):
    combos.append((vals[i], n))
for i in range(len(names)):
    for j in range(len(names)):
        if i==j: continue
        a,b = vals[i],vals[j]
        if b!=0:
            combos.append((a/b, f"{names[i]}/{names[j]}"))
        combos.append((a*b, f"{names[i]}*{names[j]}"))
# triple ratios (a/(b*c)) and (a*b/c)
for i,j,k in product(range(len(names)),repeat=3):
    a,b,c = vals[i],vals[j],vals[k]
    if b*c!=0:
        combos.append((a/(b*c), f"{names[i]}/({names[j]}*{names[k]})"))
    if c!=0:
        combos.append((a*b/c, f"{names[i]}*{names[j]}/{names[k]}"))

combo_vals = np.array([c[0] for c in combos])
N_combos = len(combos)
print(f"Look-elsewhere set size (1,2,3-symbol products/ratios) = {N_combos}")

target = 2/3
# measured fractional tolerance: how close does the framework CLAIM to land?
# CUBE/GAUGE=8/12=2/3 is EXACT, so use the experimental tol of Q itself.
tol_frac = dQ/Q_koide   # ~ the precision to which 2/3 is 'special'
print(f"Measured fractional tolerance (1-sigma of Q) = {tol_frac:.2e}")

# count how many combos hit 2/3 to better than (a) exact-rational and (b) tol
hits_exact = [combos[i] for i in range(N_combos) if abs(combo_vals[i]-target)<1e-9]
within = np.abs(combo_vals-target)/target < tol_frac
hits_tol = [combos[i] for i in range(N_combos) if within[i]]
print(f"\nCombos EXACTLY equal to 2/3 (rational identities): {len(hits_exact)}")
for v,l in hits_exact[:12]:
    print(f"   {l} = {v:.6f}")
print(f"... ({len(hits_exact)} total exact-2/3 re-descriptions)")
print(f"\n--> KEY FDR POINT: 2/3 is hit EXACTLY by {len(hits_exact)} distinct symbol")
print(f"    combinations. CUBE/GAUGE=8/12 is just ONE of them. Re-labeling a")
print(f"    small-denom rational is FREE -> the '8/12' identity is BAKED.")
