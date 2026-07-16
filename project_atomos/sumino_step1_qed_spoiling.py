#!/usr/bin/env python3
"""
SUMINO CONSTRUCTION -- STEP 1: quantify the QED spoiling of Koide (the problem the
gauged SU(3)_F family symmetry must CANCEL), and lay out the two forcedness questions.

Koide Q = (Sum m)/(Sum sqrt m)^2 = 2/3 holds for POLE masses. The masses RUN (QED radiative
corrections), and the running is FLAVOR-DEPENDENT (each lepton has its own threshold / its own
ln(m_f) self-energy) -> Q(mu) drifts off 2/3. Sumino's claim: SU(3)_F gauge-boson self-energies
cancel that flavor-dependent QED piece so 2/3 is exact at the family scale. STEP 1 = measure the
drift Sumino must cancel; the a0/Z gravity kernel does NOT enter (number-field obstruction).
"""
import numpy as np
np.seterr(all="ignore")

def koide_Q(ms):
    ms = np.asarray(ms, float)
    return ms.sum() / (np.sqrt(ms).sum()**2)

# --- POLE masses (PDG, MeV): Koide's relation is a POLE-mass statement ---
pole = dict(e=0.51099895, mu=105.6583755, tau=1776.86)
Qp = koide_Q(list(pole.values()))

# --- MS-bar charged-lepton masses run to M_Z (standard running-fermion-mass values,
#     e.g. Xing-Zhang-Zhou 2008/2020; used here to show the flavor-dependent QED drift) ---
msbar_MZ = dict(e=0.486570, mu=102.7181, tau=1746.17)   # MeV, at mu = M_Z
Qz = koide_Q(list(msbar_MZ.values()))

# --- MS-bar at 2 GeV (another common scale) to show scale-dependence of the drift ---
msbar_2GeV = dict(e=0.4955, mu=104.47, tau=1771.0)      # MeV, ~2 GeV (approx)
Q2 = koide_Q(list(msbar_2GeV.values()))

print("="*80)
print("STEP 1 -- how badly does QED running spoil Koide 2/3 ?  (what SU(3)_F must cancel)")
print("="*80)
print(f"  Q(pole masses)     = {Qp:.6f}   (target 2/3 = {2/3:.6f};  off {1e6*(Qp-2/3):+.1f} ppm)")
print(f"  Q(MS-bar, M_Z)     = {Qz:.6f}   (drift from 2/3: {Qz-2/3:+.5f} = {100*(Qz-2/3)/(2/3):+.3f}%)")
print(f"  Q(MS-bar, ~2 GeV)  = {Q2:.6f}   (drift from 2/3: {Q2-2/3:+.5f} = {100*(Q2-2/3)/(2/3):+.3f}%)")
print()
print("  KEY: Q is INVARIANT under a common rescaling m_f -> kappa*m_f (so the FLAVOR-UNIVERSAL")
print("  part of QED running cancels in Q automatically). The drift above is the FLAVOR-DEPENDENT")
print(f"  piece -- ~{abs(Qz-2/3):.1e} in Q, i.e. ~O(alpha/pi x ln(m_tau/m_e)) ~ {(1/137.036/np.pi)*np.log(pole['tau']/pole['e']):.2e}.")
print("  THIS is what Sumino's family gauge bosons must cancel to keep 2/3 exact at the SU(3)_F scale.")
print()

# --- the alpha/pi x ln estimate, per-lepton, to show it is flavor-dependent (does NOT cancel in Q) ---
alpha = 1/137.035999
print("  flavor-dependent QED self-energy weight  (alpha/pi)*ln(mu/m_f)  at mu=M_Z=91188 MeV:")
for f,m in pole.items():
    print(f"    {f:3s}: (alpha/pi)*ln(M_Z/m_{f}) = {(alpha/np.pi)*np.log(91188.0/m):+.4f}   <- differs by flavor => spoils Q")
print()

print("="*80)
print("THE TWO FORCEDNESS QUESTIONS Sumino's model must answer to certify at the gate")
print("="*80)
print("""  Q1 (amplitude): does the SU(3)_F flavon POTENTIAL force the Koide amplitude r=sqrt2
       as an OUTPUT, or is sqrt2 tuned via a free coupling ratio in the potential?
       Known issue: Sumino engineers a specific potential -> sqrt2 is largely INPUT. -> STEP 2.
  Q2 (overdetermination): does the SAME SU(3)_F structure force a SECOND observable (fixing
       the phase delta / a mixing angle / the neutrino sector) with <= 1 free param -- the
       overdetermination Gate C needs -- or does delta stay free (absorbing the masses)?
       The QED-cancellation is ROBUSTNESS of 1 relation, NOT a 2nd independent forced observable.
       -> STEP 3.

  HONEST STANDING (both-ways): Sumino's mechanism is REAL (a genuine way to protect 2/3 under
  running), but the open question is whether it FORCES (r, delta) with zero knobs or HOSTS them
  with a tuned potential + a tuned family-gauge scale (~10^2-10^3 TeV, itself a knob, plus FCNC
  tension). Prior: HOSTS-with-knobs (improves robustness, does not yet close the gate). We test
  Q1 and Q2 next -- and the a0/Z gravity kernel plays NO role here (flavor sector, obstruction).""")
print("EXIT 0")
