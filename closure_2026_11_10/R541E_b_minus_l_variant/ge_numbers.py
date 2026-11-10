"""R541E numerical gates GE1-GE5 with KA1-KA4, KA6 and MU1-MU5 (FROZEN_CRITERIA.md).
Natural units, GeV, unless stated. Run:  python3 ge_numbers.py > ge_numbers.out
Inputs marked [P] are PROVISIONAL look-ups; the rest are the record's fit (F1A), CODATA/AME constants, or R541D's.
"""
import numpy as np
from fractions import Fraction
from scipy.integrate import quad

FOOT = {"canonical": dict(R=5.410, ob=0.02236, od=0.1209, h=0.674, a0=9.3603e-11),
        "alt":       dict(R=5.412, ob=0.02234, od=0.1209, h=0.674, a0=1.1312e-10)}
u_GeV = 0.93149410242; mH = 1.00782503207 * u_GeV; mHe = 4.00260325413 * u_GeV
m_p = 0.93827208816; m_n = 0.93956542052
Y_p = 0.245                                    # [P]
rho_c_h2 = 1.05368e-5                          # GeV cm^-3 / h^2
hbarc_cm = 1.973269804e-14                     # GeV cm
hbar_GeVs = 6.582119569e-25                    # GeV s
kB_GeV = 8.617333262e-14
T0 = 2.7255 * kB_GeV; gs0 = 3.909
T_sph = 131.7; dT_sph = 2.3                    # [P]
M_Pl = 1.22089e19; v_EW = 174.0
K_N = 4 * np.pi / M_Pl ** 2                    # K = 4 pi G in GeV^-2
dm2_atm = 2.5e-3 * 1e-18                       # [P] eV^2 -> GeV^2
Mpc_GeVinv = 3.0856775814913673e22 / 1.973269804e-16
H100 = 1e5 / 3.0856775814913673e22 * hbar_GeVs  # 100 km/s/Mpc in GeV
yr_s = 3.15576e7
m_bar = (1 - Y_p) * mH + Y_p * mHe / 4

def P(*a):
    print(*a)

# ---------------------------------------------------------------- SM chemical equilibrium, general
# Weyl multiplets per generation (g, Y, B, L); fermion weight 1, Higgs weight 2 (n - nbar = w g mu T^2 / 6)
FERM = [(6, 1/6, 1/3, 0), (3, 2/3, 1/3, 0), (3, -1/3, 1/3, 0), (2, -1/2, 0, 1), (1, -1.0, 0, 1)]
NUR = (1, 0.0, 0, 1)
HIGGS = (2, 1/2, 0, 0)

def species(nuR):
    sp_ = [(3 * g, Y, B, L, 1) for (g, Y, B, L) in FERM]
    if nuR:
        sp_.append((3 * NUR[0], NUR[1], NUR[2], NUR[3], 1))
    sp_.append((HIGGS[0], HIGGS[1], 0, 0, 2))
    return sp_

CH = {"Y": lambda Y, B, L: Y, "B": lambda Y, B, L: B, "L": lambda Y, B, L: L, "BL": lambda Y, B, L: B - L}

def equilibrium(bias, mu, conserved, nuR=False):
    """mu_i = mu * bias_i + sum_c lam_c c_i ; constraints: each conserved charge c has its given total.
    conserved: dict name -> total (units T^2/6). Returns totals dict (units T^2/6)."""
    sp_ = species(nuR)
    names = list(conserved)
    def tot(cf, lam):
        return sum(w * g * cf(Y, B, L) * (mu * CH[bias](Y, B, L) + sum(lam[k] * CH[names[k]](Y, B, L)
               for k in range(len(names)))) for (g, Y, B, L, w) in sp_)
    n = len(names)
    z = [0.0] * n
    A = np.zeros((n, n)); b = np.zeros(n)
    for i, ci in enumerate(names):
        base = tot(CH[ci], z)
        for j in range(n):
            e = [0.0] * n; e[j] = 1.0
            A[i, j] = tot(CH[ci], e) - base
        b[i] = conserved[ci] - base
    lam = list(np.linalg.solve(A, b))
    return {k: tot(CH[k], lam) for k in ("B", "L", "BL", "Y")}

def gstar(nuR):
    return 106.75 + (3 * 2 * 7 / 8 if nuR else 0.0)

def per_s(total, nuR=False):
    """convert a total in units T^2/6 per unit mu (mu/T = 1) to n/s per unit mu/T"""
    return total / 6 / (2 * np.pi ** 2 / 45 * gstar(nuR))

P("== inputs")
P(f"m_bar = {m_bar:.6f} GeV ; K = 4 pi G = {K_N:.4e} GeV^-2 ; 1 Mpc^-1 = {1/Mpc_GeVinv:.4e} GeV ; H100 = {H100:.4e} GeV")

# ---------------------------------------------------------------- KA2
r = equilibrium("B", 0.0, {"Y": 0.0, "BL": 1.0})
P(f"KA2 no bias, B-L = 1: B = {r['B']:.6f} (28/79 = {28/79:.6f}), L = {r['L']:.6f} (-51/79 = {-51/79:.6f}) ->",
  "PASS" if abs(r['B'] - 28/79) < 1e-9 and abs(r['L'] + 51/79) < 1e-9 else "FAIL")

# ---------------------------------------------------------------- GE1 responses (B-L conserved, fixed at 0)
P("\n== GE1 sphaleron response to a bias, B-L conserved (fixed), Y = 0, mu = 1 (units T^2/6)")
resp = {}
for bias in ("B", "BL", "L"):
    for nuR in (False, True):
        rr = equilibrium(bias, 1.0, {"Y": 0.0, "BL": 0.0}, nuR)
        resp[(bias, nuR)] = rr
        P(f"   bias on {bias:2s} (nu_R {'in' if nuR else 'out'}): induced B = {rr['B']:+.6e}, L = {rr['L']:+.6e}, "
          f"B-L = {rr['BL']:+.2e} ; n_B/s per (eps/T) = {per_s(rr['B'], nuR):+.6e}")
# also the made B-L stays at 28/79 under a B-L bias
rr = equilibrium("BL", 3.7, {"Y": 0.0, "BL": 1.0})
P(f"   with B-L = 1 and a B-L bias mu = 3.7: B = {rr['B']:.6f} (unchanged 28/79: {abs(rr['B']-28/79) < 1e-9})")
cB_B = per_s(resp[("B", False)]["B"])
cB_L = per_s(resp[("L", False)]["B"])
cB_BL = per_s(resp[("BL", False)]["B"])
P(f"   MU1 B-L violated in equilibrium (only Y conserved), bias on B-L: "
  f"B = {equilibrium('BL', 1.0, {'Y': 0.0})['B']:+.6e} (nonzero: the gate can fail)")

# ---------------------------------------------------------------- GE3 coefficient: B-L violated, bias on B-L
cBL = {}
for nuR in (False, True):
    rr = equilibrium("BL", 1.0, {"Y": 0.0}, nuR)
    cBL[nuR] = per_s(rr["BL"], nuR)
    P(f"GE3 coefficient (B-L violated in eq., nu_R {'in' if nuR else 'out'}): n_(B-L)/s = {cBL[nuR]:+.6e} * mu/T "
      f"(B {per_s(rr['B'], nuR):+.4e}, sign of n_(B-L) = sign of mu)")

# Weinberg freeze-out (R541D formula), leptogenesis
T_W = 1.66 * np.sqrt(106.75) * np.pi ** 3 * v_EW ** 4 / (M_Pl * dm2_atm)
OPTS = {"(a) Weinberg op (Majorana), T_W": T_W,
        "(b) thermal leptogenesis M1 = 1e9, z_f 10": 1e9 / 10,
        "(b) thermal leptogenesis M1 = 1e10, z_f 10": 1e10 / 10}

# ---------------------------------------------------------------- background integrals
def bg(F):
    h = F["h"]; Om = (F["ob"] + F["od"]) / h ** 2; Or = 4.18e-5 / h ** 2; OL = 1 - Om - Or
    H0 = H100 * h
    Hf = lambda a: H0 * np.sqrt(Om / a ** 3 + Or / a ** 4 + OL)
    I3 = quad(lambda a: a ** 3 / (a * Hf(a)), 0, 1, epsrel=1e-10)[0]
    I4 = quad(lambda a: a ** 4 / (a * Hf(a)), 0, 1, epsrel=1e-10)[0]
    t0 = quad(lambda a: 1 / (a * Hf(a)), 0, 1, epsrel=1e-10)[0]
    rho_c = rho_c_h2 * h ** 2 * hbarc_cm ** 3
    return dict(I3=I3, I4=I4, t0=t0, rho_c=rho_c, H0=H0)

# ---------------------------------------------------------------- KA3: coherent two-body production integral
def coherent_rate(M2fun, omega, m1, m2, sym):
    """Gamma/V for a source oscillating at omega making a pair (back-to-back), delta replaced by a narrow Gaussian."""
    def E(p, m):
        return np.sqrt(p * p + m * m)
    # exact two-body: integrate over p with Gaussian delta of width w
    w = 1e-4 * omega
    pmax = omega
    f = lambda p: (4 * np.pi * p * p / (2 * np.pi) ** 3) / (4 * E(p, m1) * E(p, m2)) * 2 * np.pi \
        * np.exp(-0.5 * ((omega - E(p, m1) - E(p, m2)) / w) ** 2) / (np.sqrt(2 * np.pi) * w) * M2fun(p)
    # locate the peak
    from scipy.optimize import brentq
    ps = brentq(lambda p: E(p, m1) + E(p, m2) - omega, 0, pmax)
    val = quad(f, max(0, ps - 40 * w), ps + 40 * w, points=[ps], limit=400)[0]
    return sym * val

m0, om, mf = 1.0, 10.0, 2.0
beta = np.sqrt(1 - 4 * mf ** 2 / om ** 2)
# Dirac, m(t) = m0 cos(om t): producing amplitude m0/2; sum_spins |ubar v|^2 = 4 (p1.p2 - m^2), p1.p2 = E^2 + p^2
M2_dirac = lambda p: (m0 / 2) ** 2 * 4 * ((p * p + mf * mf) + p * p - mf * mf)
num = coherent_rate(M2_dirac, om, mf, mf, 1.0)
ana = m0 ** 2 * om ** 2 * beta ** 3 / (16 * np.pi)       # n_phi Gamma = (om Phi^2/2)(y^2 om beta^3/8pi), y Phi = m0
P(f"\nKA3 coherent Dirac pair rate / [n_phi Gamma(phi->ffbar)] = {num/ana:.8f} ->", "PASS" if abs(num / ana - 1) < 1e-6 else "FAIL")
# Majorana, rotating mass m e^{i om t}: |M|^2 = m^2 s (two contractions), identical pair -> 1/2
mnu_t = 1.0
num_maj = coherent_rate(lambda p: mnu_t ** 2 * om ** 2, om, 0.0, 0.0, 0.5)
P(f"    Majorana rotating mass, massless limit: Gamma/V / [m^2 omega^2/(16 pi)] = {num_maj/(mnu_t**2*om**2/(16*np.pi)):.8f}")

def majorana_rate(m, omega):
    return m * m * omega * omega / (16 * np.pi)

res = {}
for fn, F in FOOT.items():
    P(f"\n================ footing {fn}")
    R = F["R"]; h = F["h"]
    B0 = bg(F)
    nB0 = F["ob"] * rho_c_h2 * hbarc_cm ** 3 / m_bar
    s0 = 2 * np.pi ** 2 / 45 * gs0 * T0 ** 3
    eta = nB0 / s0
    etaBL = 79 / 28 * eta
    P(f"observed n_B/s = {eta:.4e} ; (B-L)/s = (79/28) n_B/s = {etaBL:.4e}")

    # ------------------------------------------------ GE2
    eps_B = -R * m_bar                        # KA6 (R541D)
    eps = -R * m_bar * 28 / 79
    eps_1237 = -R * m_bar * 12 / 37
    eps_L = +R * m_bar * 28 / 51
    P(f"KA6 X = B: eps = {eps_B:.5f} GeV (R541D: -5.0700 / -5.0718) ->",
      "PASS" if abs(eps_B - (-5.0700 if fn == 'canonical' else -5.0718)) < 6e-5 else "FAIL")
    P(f"GE2 main (X = B-L), neutral start: rho_K = -eps n_(B-L) = -eps (79/28) n_B  =>  R = -eps (79/28)/m_bar")
    P(f"   eps = {eps:.5f} GeV (m_p bracket {-R*m_p*28/79:.5f}); eps < 0 for rho_K > 0")
    P(f"   broken-phase ratio 12/37 instead: eps = {eps_1237:.5f} GeV (MU2: moves by {eps_1237/eps:.4f} = (12/37)/(28/79) {(12/37)/(28/79):.4f})")
    P(f"   MU2 R x 2 -> eps = {-2*R*m_bar*28/79:.5f} (x{(-2*R*m_bar*28/79)/eps:.3f})")
    P(f"GE2 variant (X = L): L = -(51/28) B => R = +eps (51/28)/m_bar ; eps_L = {eps_L:+.5f} GeV (positive)")
    # natural normalisation, R541D's list
    om_tot = F["ob"] + F["od"]
    rhoDE = (h ** 2 - om_tot - 4.18e-5) * rho_c_h2 * hbarc_cm ** 3
    E_L = rhoDE ** 0.25
    cands = {}
    for nm, EP in (("M_Pl", M_Pl), ("M_Pl_reduced", M_Pl / np.sqrt(8 * np.pi))):
        for qd in range(1, 7):
            for pn in range(0, qd + 1):
                al = Fraction(pn, qd)
                if al.denominator != qd:
                    continue
                E = EP ** float(al) * E_L ** float(1 - al)
                cands[f"{nm}^{al} * rho_DE^({1-al})/4"] = E
                for k in (0.5, 2.0):
                    cands[f"{k} * {nm}^{al} * rho_DE^({1-al})/4"] = k * E
    cands["hbar a0 / c"] = hbar_GeVs * F["a0"] / 2.99792458e8
    for lab, target in (("main |eps|", abs(eps)), ("12/37 |eps|", abs(eps_1237)), ("variant |eps_L|", abs(eps_L))):
        within = [k for k, v in cands.items() if abs(v / target - 1) <= 0.012]
        best = sorted(cands.items(), key=lambda kv: abs(np.log(kv[1] / target)))[:2]
        P(f"   native list ({len(cands)} energies) vs {lab} = {target:.4f}: within 1.2 %: {within}; nearest "
          + "; ".join(f"{k} = {v:.4g} (ratio {v/target:.3f})" for k, v in best))

    # ------------------------------------------------ GE1
    P("GE1 bias-induced n_B/s at T_sph (B-L conserved):")
    X_B = abs(cB_B * eps_B / T_sph) / eta
    P(f"   KA1 X = B, eps {eps_B:.4f}: n_B/s = {cB_B*eps_B/T_sph:.4e} (R541D -3.7464e-4 canonical) ->",
      "PASS" if fn != "canonical" or abs(cB_B * eps_B / T_sph / -3.7464e-4 - 1) < 1e-4 else "FAIL")
    for Ts in (T_sph - dT_sph, T_sph, T_sph + dT_sph):
        P(f"   main X = B-L, eps {eps:.4f}, T {Ts:.1f}: n_B/s = {cB_BL*eps/Ts:+.3e} -> {abs(cB_BL*eps/Ts)/eta:.2e} of observed")
    GE1_main = abs(cB_BL * eps / T_sph) / eta <= 0.1
    P(f"   GE1 main: {'PASS' if GE1_main else 'FAIL'} (bias absorbed by the B-L Lagrange multiplier; exact zero)")
    nBv = cB_L * eps_L / T_sph
    XL = abs(nBv) / eta
    P(f"   variant X = L, eps_L {eps_L:+.4f}: n_B/s = {nBv:+.4e} -> X = {XL:.3e} ({'baryons' if nBv > 0 else 'antibaryons'}); "
      f"T_sph +- 2.3: {abs(cB_L*eps_L/(T_sph+dT_sph))/eta:.3e} .. {abs(cB_L*eps_L/(T_sph-dT_sph))/eta:.3e} -> GE1 variant FAIL")
    P(f"   (variant: L = B - (B-L), so the L bias is a B bias of the same eps: response ratio {cB_L/cB_B:.6f})")

    # ------------------------------------------------ GE3
    P("GE3 equilibrium B-L the bias drives to while B-L violation is in equilibrium (Q = 1), line 10 % of (B-L)_obs/s:")
    ge3 = {}
    for nuR in (False, True):
        Tmin = abs(cBL[nuR] * eps) / (0.1 * etaBL)
        P(f"   nu_R {'in' if nuR else 'out'}: n_(B-L)^eq/s = {cBL[nuR]*eps:+.4e} GeV / T  (sign {'negative' if cBL[nuR]*eps < 0 else 'positive'}: "
          f"rho_K = -eps n_(B-L) {'< 0' if -eps*cBL[nuR]*eps < 0 else '> 0'}) ; minimum T_f for the line: {Tmin:.3e} GeV")
        ge3[nuR] = Tmin
    for lab, Tf in OPTS.items():
        val = abs(cBL[False] * eps / Tf) / etaBL
        P(f"   {lab}: T_f = {Tf:.3e} GeV -> |n^eq/s| / (B-L)_obs/s = {val:.3e} -> {'passes' if val <= 0.1 else 'FAILS'} the 10 % line")
    val = abs(cBL[False] * eps / (1e9 / 1000)) / etaBL
    P(f"   MU3 T_f 1e8 -> 1e5 GeV: ratio {abs(cBL[False]*eps/1e5)/etaBL / (abs(cBL[False]*eps/1e8)/etaBL):.1f} x")
    P(f"   (c) Dirac-compatible generic sector: passes iff T_f >= {max(ge3.values()):.3e} GeV (free parameter)")

    # ------------------------------------------------ GE4
    P("GE4 vacuum today (Q = 1): omega = 2|eps|")
    om_ = 2 * abs(eps)
    def rho_today(m):
        G = majorana_rate(m, om_)
        return G, G * B0["I3"], om_ * G * B0["I4"]
    for m_eV in (0.05, 0.005):
        G, n0, rho0 = rho_today(m_eV * 1e-9)
        P(f"   m = {m_eV} eV: Gamma/V = {G:.3e} GeV^4 ; n0 = {n0:.3e} GeV^3 = {n0/hbarc_cm**3:.3e} cm^-3 ; "
          f"rho0 = {rho0:.3e} GeV^4 = {rho0/B0['rho_c']:.3e} rho_c")
    G05, n05, r05 = rho_today(0.05e-9)
    G005, _, r005 = rho_today(0.005e-9)
    P(f"   MU4 m/10 -> rho0 x {r005/r05:.4f} ; eps x 2 -> x {majorana_rate(0.05e-9, 2*om_)*2*om_/(G05*om_):.3f}")
    m_max = 0.05e-9 * np.sqrt(0.01 * B0["rho_c"] / r05)
    P(f"   1 % line: m_max = {m_max:.3e} GeV = {m_max*1e9:.3e} eV ; vs 0.05 eV: factor {0.05e-9/m_max:.3e} too large")
    # occupation of the produced shell today: f ~ 2 Gamma/V * 2 pi^2 / (g p^3 H), p = |eps|, g = 1 per helicity
    occ = lambda m: 2 * majorana_rate(m, om_) * 2 * np.pi ** 2 / (abs(eps) ** 3 * B0["H0"])
    P(f"   occupation of the produced shell today: f(0.05 eV) ~ {occ(0.05e-9):.3e} (Pauli-blocked), f(m_max) ~ {occ(m_max):.3e}")
    ncap = abs(eps) ** 3 / (6 * np.pi ** 2); rcap = abs(eps) ** 4 / (8 * np.pi ** 2)
    P(f"   Pauli cap (one helicity, filled to |eps|): n = {ncap/hbarc_cm**3:.3e} cm^-3, rho = {rcap:.3e} GeV^4 = {rcap/B0['rho_c']:.3e} rho_c")
    rhoK0 = R * F["ob"] * rho_c_h2 * hbarc_cm ** 3
    P(f"   drain: the clock gives up 2|eps| per pair; today's rho_K = {rhoK0:.3e} GeV^4 is used up in "
      f"{rhoK0/(om_*G05)*hbar_GeVs/yr_s:.3e} yr at m = 0.05 eV")
    P(f"   => Majorana neutrinos EXCLUDED for this coupling (m_max {m_max*1e9:.1e} eV << 0.05 eV); main case requires Dirac")
    # nucleon operators, dim-7 Delta(B-L) = 2
    tau_p = 3.5e32 * yr_s / hbar_GeVs
    DF, fpi = 1.27, 0.092
    delta_b = np.sqrt(32 * np.pi * fpi ** 2 / (m_p * (1 + DF) ** 2 * tau_p))
    def vac_N(delta):
        G = 2 * delta ** 2 * om_ ** 2 * (1 - m_p ** 2 / om_ ** 2) ** 2 / (8 * np.pi)
        return G, om_ * G * B0["I3"]
    Gd, rd = vac_N(delta_b)
    P(f"   nucleon dim-7 Delta(B-L)=2: delta bound from p -> nu pi+ > 3.5e32 yr [P]: {delta_b:.3e} GeV; vacuum -> pbar e-, nbar nu: "
      f"Gamma/V = {Gd:.3e}, n0 = {Gd*B0['I3']/hbarc_cm**3:.3e} cm^-3, rho0 = {rd/B0['rho_c']:.3e} rho_c ; delta must sit "
      f"{np.sqrt(rd/(0.01*B0['rho_c'])):.3e} x below the bound")
    dnn = 1 / (4.7e8 / hbar_GeVs)
    bnn = np.sqrt(1 - 4 * m_n ** 2 / om_ ** 2)
    Gnn = dnn ** 2 * om_ ** 2 * bnn ** 3 / (16 * np.pi)
    rnn = om_ * Gnn * B0["I3"]
    P(f"   n-nbar: delta_nn <= {dnn:.3e} GeV (tau > 4.7e8 s [P]); vacuum -> nbar nbar (beta {bnn:.3f}): rho0 = {rnn/B0['rho_c']:.3e} rho_c ; "
      f"delta_nn must sit {np.sqrt(rnn/(0.01*B0['rho_c'])):.3e} x below the bound")
    # Delta(B-L) = 4, (nu_R)^4 / Lambda^2: |M|^2 ~ (s/Lambda^2)^2, massless 4-body phase space, 1/4! identical
    om4 = 4 * abs(eps)
    Phi4 = (2 * np.pi) ** (4 - 12) * (np.pi / 2) ** 3 * om4 ** 4 / (6 * 2)
    Phi2chk = (2 * np.pi) ** (4 - 6) * (np.pi / 2) ** 1 / 1
    lam_min = (om4 ** 4 * Phi4 / 24 * om4 * B0["I4"] / (0.01 * B0["rho_c"])) ** 0.25
    P(f"   (phase-space formula check n = 2: {Phi2chk:.6f} vs 1/(8 pi) {1/(8*np.pi):.6f})")
    P(f"   Delta(B-L)=4 remnant (nu_R)^4/Lambda^2, omega = 4|eps|: 1 % line needs Lambda >= {lam_min:.3e} GeV "
      f"({lam_min/M_Pl:.2e} M_Pl) for an O(1) coefficient")

    # ------------------------------------------------ GE5
    P("GE5 back-reaction under action (A), neutral start: Q - 1 = -K eps n_(B-L)/mu_K^2 = I0/(2 mu_K^2 a^3)")
    I0 = 3 * F["od"] / 2997.92458 ** 2                          # Mpc^-2
    def a_of_T(T, gs):
        return (gs0 / gs) ** (1 / 3) * T0 / T
    a = a_of_T(T_sph, 106.75)
    ka4 = I0 / (2 * 8.89e6 ** 2 * a ** 3)
    P(f"   KA4 Q-1 at T_sph, mu_K 8.89e6: {ka4:.4e} (R541D 1.229e24) ->", "PASS" if abs(ka4 / 1.229e24 - 1) < 2e-3 else "FAIL")
    Tf = max(ge3.values())
    epochs = (("lowest passing T_f (GE3)", Tf, 106.75), ("T_sph", T_sph, 106.75))
    for lab, T, gs in epochs:
        a = a_of_T(T, gs)
        sT = 2 * np.pi ** 2 / 45 * gs * T ** 3
        nBL = etaBL * sT
        for mK in (1.0, 198.25, 2.512e4, 8.89e6):
            mu = mK / Mpc_GeVinv
            q1 = -K_N * eps * nBL / mu ** 2
            q1b = I0 / (2 * mK ** 2 * a ** 3)
            P(f"   {lab} T = {T:.3e}: mu_K {mK:.4g}/Mpc: Q-1 = {q1:.3e} (I0 form {q1b:.3e}, ratio {q1/q1b:.4f}); "
              f"bias |eps| Q = {abs(eps)*(1+q1):.3e} GeV vs T {T:.2e}")
        mneed = np.sqrt(I0 / (2 * 0.01 * a ** 3))
        P(f"      Q-1 <= 0.01 needs mu_K >= {mneed:.3e} /Mpc (record max 8.89e6; galaxies <= 7)")
        mu = 8.89e6 / Mpc_GeVinv
        chiT2 = cBL[False] * 6 * (2 * np.pi ** 2 / 45 * 106.75) * 0 + 0  # placeholder (not used)
        # chi: n = chi mu T^2 ; from per_s: n/s = c mu/T -> n = c mu s/T = c mu (2pi^2/45 g) T^2
        chi = cBL[False] * 2 * np.pi ** 2 / 45 * 106.75
        n_eq_bare = chi * eps * T ** 2
        n_eq_back = eps / (1 / (chi * T ** 2) + K_N * eps ** 2 / mu ** 2)
        stiff = K_N * eps ** 2 * nBL ** 2 / (2 * mu ** 2)
        rad = np.pi ** 2 / 30 * gs * T ** 4
        P(f"      mu_K 8.89e6: equilibrium n_(B-L) with the clock's quadratic energy = {n_eq_back:.3e} GeV^3 (bare {n_eq_bare:.3e}; "
          f"needed +{nBL:.3e}); stiff clock energy / radiation after generation = {stiff/rad:.3e}")
        if lab.startswith("lowest"):
            q1_mu10 = I0 / (2 * (8.89e6 / 10) ** 2 * a ** 3) / (I0 / (2 * 8.89e6 ** 2 * a ** 3))
            P(f"      MU5 mu_K/10: Q-1 x {q1_mu10:.1f}")
            res[fn] = dict(eps=eps, epsL=eps_L, XL=XL, Tmin=Tf, Q1=I0 / (2 * 8.89e6 ** 2 * a ** 3), mneed=mneed,
                           m_max=m_max)
    for lab, Tf_ in OPTS.items():
        a = a_of_T(Tf_, 106.75)
        P(f"   at {lab} (T {Tf_:.2e}): Q-1 (mu_K 8.89e6) = {I0/(2*8.89e6**2*a**3):.3e}")
    P("   pressureless dust (Q = 1 at all epochs): bias = eps, energy per unit B-L |eps| << T_f: GE5 passes in that reading")

P("\n== summary (footings not pooled)")
for f, r in res.items():
    P(f"{f}: eps(B-L) = {r['eps']:.4f} GeV ; variant eps_L = {r['epsL']:+.4f} GeV, sphaleron X = {r['XL']:.3e} ; "
      f"GE3 T_f >= {r['Tmin']:.3e} GeV ; GE4 m_max(Majorana) = {r['m_max']*1e9:.2e} eV ; "
      f"GE5 Q-1 at T_f (mu_K 8.89e6) = {r['Q1']:.3e}, needs mu_K >= {r['mneed']:.2e}/Mpc")
