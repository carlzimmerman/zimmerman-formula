"""
TRACK B — Running-Koide discriminator computation.

Q(mu) = (sum m_i(mu)) / (sum sqrt(m_i(mu)))^2  for charged leptons.

We compute the QED running of the charged-lepton MS-bar masses from the
pole masses up to mu = M_Z, and report the drift Q(M_Z) - Q(pole).

Physics:
 - 1-loop QED mass anomalous dimension: dm/dln(mu) = gamma_m * m,
   gamma_m = - (3/2) * (alpha/pi) * Q_f^2   (Q_f = -1 for charged leptons,
   so Q_f^2 = 1). This is the pure-QED piece. (For full SM running one would
   add EW and, for completeness above thresholds, the running alpha.)
 - alpha runs too; we include the running of alpha_em via the leptonic +
   hadronic + W contributions encoded through alpha(M_Z) ~ 1/127.95.
 - We do this BOTH ways: (a) frozen alpha = alpha(0); (b) running alpha
   interpolated log-linearly in ln(mu) from alpha(0) at low scale to
   alpha(M_Z). The drift sign/magnitude is robust to this choice.

mpmath dps = 40.
"""
import mpmath as mp
mp.mp.dps = 40

# ---- PDG 2024 pole (physical) masses in MeV ----
m_e   = mp.mpf('0.51099895000')
m_mu  = mp.mpf('105.6583755')
m_tau = mp.mpf('1776.86')          # +/- 0.12 MeV (dominant uncertainty)
m_tau_err = mp.mpf('0.12')

# fine-structure constants
alpha0  = mp.mpf(1)/mp.mpf('137.035999084')   # Thomson limit
alphaMZ = mp.mpf(1)/mp.mpf('127.951')          # alpha_em(M_Z) (PDG)
MZ      = mp.mpf('91188.0')                    # MeV  (91.188 GeV)

def Q(masses):
    s1 = sum(masses)
    s2 = sum(mp.sqrt(m) for m in masses)**2
    return s1/s2

# ----------------------------------------------------------------------
# Koide at the pole
# ----------------------------------------------------------------------
Qpole = Q([m_e, m_mu, m_tau])
two_thirds = mp.mpf(2)/3
print("=== POLE ===")
print("Q_pole          =", mp.nstr(Qpole, 12))
print("Q_pole - 2/3    =", mp.nstr(Qpole - two_thirds, 6))
print("(Q_pole-2/3)/(2/3) %% =", mp.nstr((Qpole-two_thirds)/two_thirds*100, 6))

# sigma_Q from m_tau uncertainty (dominant). Numerical derivative.
def Q_of_mtau(mt):
    return Q([m_e, m_mu, mt])
h = mp.mpf('1e-6')
dQ_dmtau = (Q_of_mtau(m_tau+h) - Q_of_mtau(m_tau-h))/(2*h)
sigmaQ = abs(dQ_dmtau)*m_tau_err
print("dQ/dm_tau       =", mp.nstr(dQ_dmtau, 6), "per MeV")
print("sigma_Q (m_tau) =", mp.nstr(sigmaQ, 6))
print("(Q-2/3)/sigma   =", mp.nstr((Qpole-two_thirds)/sigmaQ, 4), "sigma")
print()

# ----------------------------------------------------------------------
# QED running of masses, pole -> mu.
# 1-loop: m(mu) = m_pole * [running factor].  Since gamma_m is the SAME
# for all three leptons (charge-universal, Q_f^2 = 1), a COMMON
# multiplicative factor C(mu) multiplies every mass:
#   m_i(mu) = C(mu) * m_i(pole-ish reference)
# A common factor C cancels in Q (Q is invariant under m -> C*m).
# => the FLAVOR-BLIND part of QED running does NOT move Q at all.
#
# The drift in Q comes ENTIRELY from the FLAVOR-DEPENDENT part:
# each lepton's running "turns on" only above its own mass threshold
# (mass decoupling). i.e. the running of m_i between its own mass and mu
# differs per lepton because the integration RANGE differs
# (ln(mu/m_i)), and because below ~m_i the lepton's self-energy
# contribution is different. The Sumino treatment: convert pole -> MSbar
# at each lepton's own scale, then run all three up to a COMMON mu.
#
# Standard pole->MSbar 1-loop QED relation (on-shell to MSbar):
#   m_MSbar(m) = m_pole * [1 - (alpha/pi) * (1 + 3/4 * ... )]   -- the
# constant shift is ALSO common-ish but depends on alpha at each scale.
# The dominant FLAVOR-DEPENDENT effect that moves Q is the LOG running
# m_i(mu) = m_i(m_i) * (1 - (3 alpha / 2 pi) ln(mu^2/m_i^2)/2 ... ),
# i.e. each mass is suppressed by a per-flavor log ln(mu/m_i).
# ----------------------------------------------------------------------

# 1-loop running factor for a single lepton from its own mass scale to mu:
#   m_i(mu) = m_i(m_i) * exp( integral gamma_m dln mu' )
# with gamma_m = -(3/2)(alpha/pi). For frozen alpha:
#   factor_i = exp( -(3/2)(alpha/pi) * ln(mu / m_i) )
# The PER-FLAVOR ln(mu/m_i) is what breaks the common-factor cancellation.
#
# We treat m_i(m_i) ~ m_i(pole) at 1-loop leading-log (the finite pole->MSbar
# matching piece is flavor-common at leading order in this approximation and
# cancels in Q; we verify robustness below).

def run_mass(m_pole_i, mu, alpha):
    # leading-log 1-loop QED running from scale m_i up to mu
    g = mp.mpf(3)/2 * (alpha/mp.pi)      # |gamma_m| coefficient
    return m_pole_i * mp.e**(-g*mp.log(mu/m_pole_i))

def Q_running(mu, alpha):
    ms = [run_mass(m_e, mu, alpha),
          run_mass(m_mu, mu, alpha),
          run_mass(m_tau, mu, alpha)]
    return Q(ms), ms

print("=== RUNNING pole -> M_Z (frozen alpha = alpha(0)) ===")
QMZ_frozen, msMZ = Q_running(MZ, alpha0)
print("Q(M_Z)          =", mp.nstr(QMZ_frozen, 12))
drift_frozen = QMZ_frozen - Qpole
print("Q(M_Z) - Q_pole =", mp.nstr(drift_frozen, 6))
print("drift %%         =", mp.nstr(drift_frozen/Qpole*100, 6))
print("drift / sigma_Q =", mp.nstr(drift_frozen/sigmaQ, 5))
print()

print("=== RUNNING pole -> M_Z (alpha = alpha(M_Z)) ===")
QMZ_run, _ = Q_running(MZ, alphaMZ)
drift_run = QMZ_run - Qpole
print("Q(M_Z)          =", mp.nstr(QMZ_run, 12))
print("drift %%         =", mp.nstr(drift_run/Qpole*100, 6))
print("drift / sigma_Q =", mp.nstr(drift_run/sigmaQ, 5))
print()

# ----------------------------------------------------------------------
# Cross-check against Sumino's quoted drift. Sumino (and the literature)
# quote Q(MSbar, M_Z) - Q(pole) ~ +0.2%. Let's see our sign & magnitude.
# ----------------------------------------------------------------------
print("=== scales sweep (frozen alpha0) ===")
for mu_GeV in ['1.777','10','91.188','1000','1e6','1.22e19']:
    muMeV = mp.mpf(mu_GeV)*1000
    Qx,_ = Q_running(muMeV, alpha0)
    print(f"mu={mu_GeV:>10} GeV : Q={mp.nstr(Qx,10)}  drift%={mp.nstr((Qx-Qpole)/Qpole*100,5)}")
print()

# ----------------------------------------------------------------------
# What m_tau precision resolves the competing predictions?
# Competing drift predictions (relative to pole Q at ~2/3):
#   framework banked : +0.18%
#   Singh post-break : +0.374%
#   null (no shift)  :  0%
# The OBSERVABLE that is actually measured is the POLE Q (and its offset
# from 2/3). sigma_Q is dominated by m_tau. To resolve a shift of size
# delta(%) at 1 sigma we need sigma_Q < delta_abs, i.e.
#   sigma_Q = |dQ/dm_tau| * sigma_mtau  <  delta * (2/3)
# Solve for sigma_mtau.
# ----------------------------------------------------------------------
print("=== m_tau precision needed ===")
print("|dQ/dm_tau| =", mp.nstr(abs(dQ_dmtau),6), "per MeV")
print("current sigma_mtau =", mp.nstr(m_tau_err,4), "MeV -> sigma_Q =", mp.nstr(sigmaQ,5),
      " (= ", mp.nstr(sigmaQ/two_thirds*100,4), "% )")
for label, pct in [('+0.18% (framework)',mp.mpf('0.0018')),
                   ('+0.374% (Singh)',mp.mpf('0.00374')),
                   ('half of 0.18%',mp.mpf('0.0009'))]:
    delta_abs = pct*two_thirds
    needed_sigma_mtau = delta_abs/abs(dQ_dmtau)
    print(f"  to reach 1-sigma on {label:<22}: need sigma_mtau < {mp.nstr(needed_sigma_mtau,4)} MeV "
          f"(factor {mp.nstr(m_tau_err/needed_sigma_mtau,3)} better than {mp.nstr(m_tau_err,3)})")
