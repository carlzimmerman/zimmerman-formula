"""
TRACK B refinement — threshold-aware QED running + Singh comparison framing.

Two issues addressed:
(1) Leading-log run_mass(m_i -> mu) gives a SCALE-FLAT drift because the
    per-flavor logs ln(mu/m_i) enter Q only through their DIFFERENCES, and
    those differences are FIXED (ln(m_j/m_i)) once mu >> all masses. We make
    the threshold structure explicit and confirm the magnitude.
(2) Frame the three competing numbers carefully:
      - measured pole Q  = 0.6666605  (-0.91 sigma below 2/3)
      - computed Q(M_Z)  = pole + (+0.18%)  [QED running, this work + Sumino]
      - Singh post-break = 0.66916 = 2/3 + 0.374%
    Are these the SAME observable? NO. The first two are a pole->MZ COMPUTATION
    from the SAME pole masses (no new info at M_Z). Singh's 0.66916 is a
    STRUCTURAL prediction for the *physical* (pole) Koide, i.e. it predicts the
    pole Q itself is 0.66916, ABOVE the measured 0.66666.
"""
import mpmath as mp
mp.mp.dps = 40

m_e   = mp.mpf('0.51099895000')
m_mu  = mp.mpf('105.6583755')
m_tau = mp.mpf('1776.86')
alpha0  = mp.mpf(1)/mp.mpf('137.035999084')
two_thirds = mp.mpf(2)/3

def Q(ms):
    return sum(ms)/sum(mp.sqrt(m) for m in ms)**2

Qpole = Q([m_e,m_mu,m_tau])

# ---- Why the drift is exactly the per-flavor log structure ----
# m_i(mu) = m_i * (mu/m_i)^(-g),  g = (3/2)(alpha/pi).
# => sqrt(m_i(mu)) = sqrt(m_i) * (mu/m_i)^(-g/2).
# Q(mu) = sum m_i (mu/m_i)^(-g) / [sum sqrt(m_i)(mu/m_i)^(-g/2)]^2
#       = sum m_i^(1+g) mu^(-g) / [ sum m_i^(1/2 + g/2) mu^(-g/2) ]^2
#       = mu^(-g) sum m_i^(1+g) / [ mu^(-g/2) sum m_i^((1+g)/2) ]^2
#       = sum m_i^(1+g) / [ sum m_i^((1+g)/2) ]^2.
# The mu^(-g) factors CANCEL EXACTLY. So Q depends on mu ONLY through g(mu)=
# (3/2)(alpha(mu)/pi). With frozen alpha, Q is mu-INDEPENDENT given g.
# This is the deep reason the drift is "scale-flat": the running is a pure
# POWER rescaling m_i -> m_i^(1+g), and Q under m_i -> m_i^p is
#   Q_p = sum m_i^p / (sum m_i^(p/2))^2,  evaluated at p = 1+g.
g = mp.mpf(3)/2*(alpha0/mp.pi)
def Q_power(p):
    return sum(m**p for m in [m_e,m_mu,m_tau]) / sum(m**(p/2) for m in [m_e,m_mu,m_tau])**2
print("g(alpha0)        =", mp.nstr(g,6))
print("Q at p=1 (pole)  =", mp.nstr(Q_power(1),12))
print("Q at p=1+g (MZ)  =", mp.nstr(Q_power(1+g),12))
print("drift %%          =", mp.nstr((Q_power(1+g)-Q_power(1))/Q_power(1)*100,6))
print()

# Sensitivity dQ/dp at p=1 -> the running is a SMOOTH deformation in p.
h=mp.mpf('1e-12')
dQdp = (Q_power(1+h)-Q_power(1-h))/(2*h)
print("dQ/dp at p=1     =", mp.nstr(dQdp,6))
print("predicted drift = dQ/dp * g =", mp.nstr(dQdp*g,6),
      " (%% =", mp.nstr(dQdp*g/Qpole*100,5),")")
print()

# ---- Singh framing ----
Ksingh = mp.mpf('0.66916')
print("=== Singh 0.66916 framing ===")
print("Singh K           =", mp.nstr(Ksingh,8))
print("Singh - 2/3       =", mp.nstr(Ksingh-two_thirds,6), " (+%% =",
      mp.nstr((Ksingh-two_thirds)/two_thirds*100,5),")")
print("measured pole Q   =", mp.nstr(Qpole,12), " (-%% =",
      mp.nstr((Qpole-two_thirds)/two_thirds*100,5),")")
print("Singh - measured  =", mp.nstr(Ksingh-Qpole,6))
# in sigma units (pole sigma_Q from m_tau 0.12 MeV)
dQ_dmtau = (Q([m_e,m_mu,m_tau+mp.mpf('1e-6')])-Q([m_e,m_mu,m_tau-mp.mpf('1e-6')]))/(2*mp.mpf('1e-6'))
sigmaQ = abs(dQ_dmtau)*mp.mpf('0.12')
print("Singh - measured in sigma_Q :", mp.nstr((Ksingh-Qpole)/sigmaQ,5), "sigma")
print()
print("Is Singh's 0.66916 consistent with pole Q=0.66666?  NO if 0.66916 is")
print("a prediction for the PHYSICAL (pole) Koide: it is", mp.nstr((Ksingh-Qpole)/sigmaQ,4),
      "sigma ABOVE the measured pole value.")
print()
print("BUT if Singh's 0.66916 is meant to be the Koide of the RUNNING (MSbar,")
print("M_Z) masses, compare to our computed Q(M_Z):")
QMZ = Q_power(1+g)
print("  computed Q(M_Z) =", mp.nstr(QMZ,8), " Singh=0.66916  diff=",
      mp.nstr(Ksingh-QMZ,5), "(%% =", mp.nstr((Ksingh-QMZ)/QMZ*100,4),")")
print("  Singh's +0.374% vs running +0.18%: factor", mp.nstr(mp.mpf('0.00374')/mp.mpf('0.0018'),4),
      "-> Singh predicts ~2x the QED running drift.")
