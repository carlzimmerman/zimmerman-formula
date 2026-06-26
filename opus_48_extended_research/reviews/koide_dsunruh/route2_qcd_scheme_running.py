#!/usr/bin/env python3
"""
ROUTE 2 -- QCD SCHEME / RUNNING (the strongest sub-angle for the Koide sector-dependence hammer).

QUESTION: Quark Koide-Q is computed from MSbar running masses (light at mu=2 GeV, heavy at
mu=m_q) -- SCHEME + SCALE dependent.  Leptons use clean POLE masses.  Does any PRINCIPLED
(not tuned) scale/scheme make the up- and down-quark Q's converge toward 2/3, OR toward a
clean pattern with the leptons?

The variational verdict (Route 4) claimed: "QCD-running detuning does NOT pull quark Q toward
2/3 (up stays ~0.78-0.85, down ~0.73-0.74 across scales)."  Here we VERIFY OR REFUTE that
carefully, running ALL SIX quark masses CONSISTENTLY to a sequence of principled common scales
(2 GeV, m_c, m_b, M_Z, m_t, 1 TeV, M_GUT=2e16 GeV) using the standard 4-loop QCD
mass-anomalous-dimension + 4-loop alpha_s beta function, with PDG 2024 inputs and error bars
propagated by Monte Carlo.

Everything mpmath dps>=30 where exactness matters; RGE integrated numerically in float (the
RGE itself is not exact -- truncated perturbation series -- so the loop order IS the dominant
"scheme" uncertainty and we report it).

NO 2/3 / Koide / sqrt2 token enters any running definition.  Q is computed from the run masses
and only COMPARED to 2/3 afterward.
"""
import numpy as np
import mpmath as mp
mp.mp.dps = 40

# ============================================================================
# 1. QCD running:  alpha_s(mu) and m(mu), 4-loop MSbar.
# ============================================================================
# beta function coefficients (MSbar), d a/dln(mu^2) = -a^2(b0 + b1 a + b2 a^2 + b3 a^3),
# a = alpha_s/pi.  Standard (Chetyrkin et al.).  nf-dependent.
def beta_coeffs(nf):
    b0 = (11 - 2/3*nf)/4
    b1 = (102 - 38/3*nf)/16
    b2 = (2857/2 - 5033/18*nf + 325/54*nf**2)/64
    b3 = ((149753/6 + 3564*1.2020569) +
          (-1078361/162 - 6508/27*1.2020569)*nf +
          (50065/162 + 6472/81*1.2020569)*nf**2 +
          (1093/729)*nf**3)/256
    return b0, b1, b2, b3

# 4-loop gamma_m (Vermaseren-Larin-Ritbergen), d ln(m)/d ln(mu^2) = -a(g0+g1 a+g2 a^2+g3 a^3)
def gamma_coeffs_clean(nf):
    z3 = 1.2020569031595942854
    g0 = 1.0
    g1 = (202/3 - 20/9*nf)/16
    g2 = (1249 + (-2216/27 - 160/3*z3)*nf - 140/81*nf**2)/64
    g3 = ((4603055/162 + 135680/27*z3 - 8800*1.0369277551)/1  # zeta5 term
          + (-91723/27 - 34192/9*z3 + 18400/9*1.0369277551)*nf
          + (5242/243 + 800/9*z3 - 160/3*1.0369277551)*nf**2
          + (-332/243 + 64/27*z3)*nf**3)/256
    return g0, g1, g2, g3

def beta_rhs(a, nf):
    b0, b1, b2, b3 = beta_coeffs(nf)
    return -a*a*(b0 + b1*a + b2*a*a + b3*a*a*a)   # d a / d ln(mu^2)

def gamma_m_val(a, nf):
    g0, g1, g2, g3 = gamma_coeffs_clean(nf)
    return -a*(g0 + g1*a + g2*a*a + g3*a*a*a)      # d ln m / d ln(mu^2)

# RK4 integrator in t = ln(mu^2)
def rk4_step(f, y, t, h, *args):
    k1 = f(y, t, *args)
    k2 = f(y + 0.5*h*k1, t + 0.5*h, *args)
    k3 = f(y + 0.5*h*k2, t + 0.5*h, *args)
    k4 = f(y + h*k3, t + h, *args)
    return y + h/6*(k1 + 2*k2 + 2*k3 + k4)

# Quark thresholds (MSbar masses, where nf changes).  GeV.
THR = {4: 1.27, 5: 4.18, 6: 172.5}   # mu < mc: nf=3; mc<mu<mb: nf=4; mb<mu<mt: nf=5; >mt: nf=6
def nf_at(mu):
    if mu < THR[4]: return 3
    if mu < THR[5]: return 4
    if mu < THR[6]: return 5
    return 6

def run_alpha(a0, mu0, mu1, nsteps=4000):
    """Run a=alpha_s/pi from mu0 to mu1, crossing thresholds (continuous matching, leading)."""
    t0, t1 = np.log(mu0**2), np.log(mu1**2)
    t = t0; a = a0
    h = (t1 - t0)/nsteps
    for _ in range(nsteps):
        mu = np.exp(0.5*t)
        nf = nf_at(mu)
        a = rk4_step(lambda y, tt, nf: beta_rhs(y, nf), a, t, h, nf)
        t += h
    return a

def run_mass(m0, a0, mu0, mu1, nsteps=4000):
    """Run mass m and a together from mu0 to mu1."""
    t0, t1 = np.log(mu0**2), np.log(mu1**2)
    t = t0; a = a0; lnm = np.log(m0)
    h = (t1 - t0)/nsteps
    for _ in range(nsteps):
        mu = np.exp(0.5*t)
        nf = nf_at(mu)
        # couple: integrate (a, lnm)
        def fa(y, tt, nf): return beta_rhs(y, nf)
        def flnm(a_loc, nf): return gamma_m_val(a_loc, nf)
        # RK4 on the pair
        ka1 = fa(a, t, nf);            km1 = flnm(a, nf)
        ka2 = fa(a+0.5*h*ka1, t, nf);  km2 = flnm(a+0.5*h*ka1, nf)
        ka3 = fa(a+0.5*h*ka2, t, nf);  km3 = flnm(a+0.5*h*ka2, nf)
        ka4 = fa(a+h*ka3, t, nf);      km4 = flnm(a+h*ka3, nf)
        a   = a   + h/6*(ka1+2*ka2+2*ka3+ka4)
        lnm = lnm + h/6*(km1+2*km2+2*km3+km4)
        t += h
    return np.exp(lnm), a

# ============================================================================
# 2. Anchor alpha_s and define the input MSbar masses (PDG 2024).
# ============================================================================
alphas_MZ = 0.1180   # PDG 2024
MZ = 91.1876
a_MZ = alphas_MZ/np.pi

# PDG 2024 MSbar quark masses, each at its conventional scale:
#   m_u(2GeV)=2.16  m_d(2GeV)=4.67  m_s(2GeV)=93.4  (MeV)
#   m_c(m_c)=1.27   m_b(m_b)=4.18   m_t(m_t)=162.5  (GeV)  [m_t(m_t), MSbar]
PDG = {
    'u': (2.16e-3, 2.0, 0.49e-3),     # (mass GeV, scale GeV, 1sigma GeV)
    'd': (4.67e-3, 2.0, 0.48e-3),
    's': (93.4e-3, 2.0, 8.6e-3),
    'c': (1.27,   1.27, 0.02),        # m_c(m_c)
    'b': (4.18,   4.18, 0.03),        # m_b(m_b)
    't': (162.5,  162.5, 0.7),        # m_t(m_t) MSbar (pole 172.5)
}
# charged lepton POLE masses (MeV) -- clean, scheme-independent
LEP = [0.51099895000, 105.6583755, 1776.86]

def koide_Q(masses):
    m = np.array(masses, float)
    s = np.sqrt(m)
    return m.sum()/s.sum()**2

def c_of_Q(Q):       # c = e1^2/e2 = (sum sqrt)^2 ... actually c with Q=(c-2)/c => c = 2/(1-Q)
    return 2.0/(1.0 - Q)

Q_lep = koide_Q(LEP)

# get alpha_s at each conventional input scale by running from MZ
def alphas_at(mu):
    if mu == MZ: return a_MZ
    return run_alpha(a_MZ, MZ, mu)

# To run a mass to scale Q, we need its value & alpha at SOME starting scale.
# Run each quark mass to a target common scale mu_target.
def quark_mass_at(flavor, mu_target):
    m0, mu0, _ = PDG[flavor]
    a0 = alphas_at(mu0)
    m1, _ = run_mass(m0, a0, mu0, mu_target)
    return m1


scales = [('2 GeV', 2.0), ('m_c=1.27', 1.27), ('m_b=4.18', 4.18),
          ('M_Z=91.19', 91.1876), ('m_t=162.5', 162.5),
          ('1 TeV', 1000.0), ('M_GUT=2e16', 2e16)]

def main():
    print("="*78)
    print("CHARGED LEPTONS (pole, scheme-free):  Q = %.7f   c=2/(1-Q) = %.5f   (Koide 2/3, c=6)"
          % (Q_lep, c_of_Q(Q_lep)))
    print("="*78)
    print("\nRunning ALL SIX quark masses CONSISTENTLY to each principled common scale.")
    print("(4-loop gamma_m, 4-loop beta, RK4, threshold-matched at m_c,m_b,m_t.)\n")
    print(f"{'scale':<14}{'Q_up':>10}{'c_up':>9}{'Q_down':>10}{'c_down':>9}")
    print("-"*78)
    results = {}
    for label, mu in scales:
        mu_eff = min(mu, 2e16)
        mc = quark_mass_at('c', mu_eff); mu_m = quark_mass_at('u', mu_eff); mt = quark_mass_at('t', mu_eff)
        md = quark_mass_at('d', mu_eff); ms = quark_mass_at('s', mu_eff); mb = quark_mass_at('b', mu_eff)
        Qup = koide_Q([mu_m, mc, mt]); Qdn = koide_Q([md, ms, mb])
        results[label] = dict(Qup=Qup, Qdn=Qdn,
                              masses=dict(u=mu_m, d=md, s=ms, c=mc, b=mb, t=mt))
        print(f"{label:<14}{Qup:>10.5f}{c_of_Q(Qup):>9.3f}{Qdn:>10.5f}{c_of_Q(Qdn):>9.3f}")
    print("\n(Koide target: Q=0.66667, c=6.000.  Lepton Q=%.5f.)" % Q_lep)

    print("\n" + "="*78)
    print("GAP TO 2/3 at each scale  (does it shrink / cross 2/3?)")
    print("="*78)
    print(f"{'scale':<14}{'|Qup-2/3|':>12}{'|Qdn-2/3|':>12}{'Qup>2/3?':>10}{'Qdn>2/3?':>10}")
    for label, mu in scales:
        r = results[label]
        print(f"{label:<14}{abs(r['Qup']-2/3):>12.5f}{abs(r['Qdn']-2/3):>12.5f}"
              f"{str(r['Qup']>2/3):>10}{str(r['Qdn']>2/3):>10}")

    # min over a fine scan: is there ANY scale where Qup or Qdn = 2/3?
    print("\nFine scan 1-1e17 GeV: closest approach of each quark-Q to 2/3:")
    best = {'up': (9,0), 'down': (9,0)}
    for lmu in np.linspace(np.log10(1.5), 17, 60):
        mu = 10**lmu
        mm = {f: quark_mass_at(f, mu) for f in PDG}
        qu = koide_Q([mm['u'],mm['c'],mm['t']]); qd = koide_Q([mm['d'],mm['s'],mm['b']])
        if abs(qu-2/3) < best['up'][0]: best['up'] = (abs(qu-2/3), mu, qu)
        if abs(qd-2/3) < best['down'][0]: best['down'] = (abs(qd-2/3), mu, qd)
    for k,v in best.items():
        print(f"  {k:<6} min|Q-2/3| = {v[0]:.5f} at mu={v[1]:.3g} GeV  (Q={v[2]:.5f})")

    print("\n" + "="*78)
    print("MONTE-CARLO PDG ERROR PROPAGATION (4000 draws) at 2 GeV and M_Z")
    print("="*78)
    rng = np.random.default_rng(20260625)
    N = 4000
    for label, mu in [('2 GeV', 2.0), ('M_Z', 91.1876)]:
        Qups, Qdns = [], []
        for _ in range(N):
            draws = {f: max(rng.normal(PDG[f][0], PDG[f][2]), 1e-6) for f in PDG}
            mm = {}
            for f in PDG:
                a0 = alphas_at(PDG[f][1])
                m1,_ = run_mass(draws[f], a0, PDG[f][1], mu, nsteps=400)
                mm[f] = m1
            Qups.append(koide_Q([mm['u'], mm['c'], mm['t']]))
            Qdns.append(koide_Q([mm['d'], mm['s'], mm['b']]))
        Qups = np.array(Qups); Qdns = np.array(Qdns)
        def report(name, arr):
            med = np.median(arr); lo,hi = np.percentile(arr,[16,84])
            nsig = abs(med-2/3)/((hi-lo)/2)
            print(f"  {name:<6} Q = {med:.5f}  [{lo:.5f},{hi:.5f}]  "
                  f"({nsig:.1f}sig from 2/3; reaches 2/3? {bool(lo<=2/3<=hi)})")
        print(f"-- scale {label} --")
        report('up', Qups); report('down', Qdns)
    print("\nDONE.")

if __name__ == '__main__':
    main()
