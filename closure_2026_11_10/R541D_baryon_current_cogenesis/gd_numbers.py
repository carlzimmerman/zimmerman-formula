"""R541D numerical gates GD2, GD3, GD4 (+ GD5 proton line), with KA2-KA5 and MU1-MU3.
Natural units (GeV) unless stated. Run:  python3 gd_numbers.py > gd_numbers.out   (MUTATE rows are inside)
Inputs marked [P] are look-ups (PROVISIONAL); the rest are the record's fit (F1A) or CODATA/AME constants.
"""
import numpy as np
from fractions import Fraction
from scipy.integrate import quad

FOOT = {"canonical": dict(R=5.410, ob=0.02236, od=0.1209, h=0.674),
        "alt":       dict(R=5.412, ob=0.02234, od=0.1209, h=0.674)}
u_GeV = 0.93149410242; mH = 1.00782503207 * u_GeV; mHe = 4.00260325413 * u_GeV
m_p = 0.93827208816; m_e = 0.51099895e-3; m_n = 0.93956542052
Y_p = 0.245                                    # [P] helium mass fraction
rho_c_h2 = 1.05368e-5                          # GeV cm^-3 per h^2 (critical density / h^2)
hbarc_cm = 1.973269804e-14                     # GeV cm
kB_GeV = 8.617333262e-14                       # GeV / K
T0 = 2.7255 * kB_GeV; gs0 = 3.909              # 3.046 neutrino species
gstar_EW = 106.75
T_sph = 131.7; dT_sph = 2.3                    # [P] D'Onofrio, Rummukainen, Tranberg 2014
M_Pl = 1.22089e19; v_EW = 174.0                # GeV; Higgs vev convention v = 174 GeV
dm2_atm = 2.5e-3 * 1e-18                       # [P] eV^2 -> GeV^2 (sum m^2 >= Delta m^2_atm)
Mpc_GeVinv = 3.0856775814913673e22 / 1.973269804e-16   # 1 Mpc in GeV^-1

def P(*a):
    print(*a)

m_bar = (1 - Y_p) * mH + Y_p * mHe / 4
P("== inputs")
P(f"m_bar (mass per baryon, Y_p {Y_p}) = {m_bar:.6f} GeV ; m_p bracket {m_p:.6f} GeV")

# ------------------------------------------------------------------ KA3: n - nbar = g mu T^2/6 (fermion), T = 1
def asym_fd(mu):
    f = lambda k: k * k * (1 / (np.exp(k - mu) + 1) - 1 / (np.exp(k + mu) + 1))
    return quad(f, 0, 60, epsabs=1e-16, epsrel=1e-12)[0] / (2 * np.pi ** 2)
mu_t = 1e-3
ka3 = asym_fd(mu_t) / (mu_t / 6)
P(f"KA3 FD integral / (mu T^2/6) at mu/T = 1e-3 : {ka3:.8f}  ->", "PASS" if abs(ka3 - 1) < 1e-5 else "FAIL")

# ------------------------------------------------------------------ SM chemical equilibrium with a bias on B
# per generation Weyl multiplets: (g, Y, B, L); boson weight 2 (n - nbar = 2 g mu T^2/6)
FERM = [(6, 1/6, 1/3, 0), (3, 2/3, 1/3, 0), (3, -1/3, 1/3, 0), (2, -1/2, 0, 1), (1, -1.0, 0, 0 + 1)]
HIGGS = (2, 1/2, 0, 0)
def equilibrium(muB, BmL, ngen=3):
    """mu_i = B_i muB + lamY Y_i + lamX (B-L)_i ; impose total Y = 0 and total (B-L) = BmL (units T^2/6).
    Returns total B (units T^2/6)."""
    sp_ = [(ngen * g, Y, B, L, 1) for (g, Y, B, L) in FERM] + [(HIGGS[0], HIGGS[1], 0, 0, 2)]
    # linear: charge_c = sum w g c_i (B_i muB + lamY Y_i + lamX X_i)
    def tot(cfun, lamY, lamX):
        return sum(w * g * cfun(Y, B, L) * (B * muB + lamY * Y + lamX * (B - L)) for (g, Y, B, L, w) in sp_)
    cY = lambda Y, B, L: Y; cX = lambda Y, B, L: B - L; cB = lambda Y, B, L: B
    A = np.array([[tot(cY, 1, 0) - tot(cY, 0, 0), tot(cY, 0, 1) - tot(cY, 0, 0)],
                  [tot(cX, 1, 0) - tot(cX, 0, 0), tot(cX, 0, 1) - tot(cX, 0, 0)]])
    b = np.array([0 - tot(cY, 0, 0), BmL - tot(cX, 0, 0)])
    lamY, lamX = np.linalg.solve(A, b)
    return tot(cB, lamY, lamX)
ka2 = equilibrium(0.0, 1.0)
P(f"KA2 B/(B-L), no bias, 3 gen, 1 Higgs: {ka2:.6f}  (Harvey-Turner 28/79 = {28/79:.6f}) ->",
  "PASS" if abs(ka2 - 28 / 79) < 1e-9 else "FAIL")
cB = equilibrium(1.0, 0.0)          # B per unit muB, units T^2/6 / GeV ... (T^2/6) * cB * muB
coef = cB * (1 / 6) / (2 * np.pi ** 2 / 45 * gstar_EW)    # n_B/s = coef * muB / T
P(f"bias response (B-L = 0): B = {cB:.5f} * mu_B * T^2/6 ; n_B/s = {coef:.6e} * mu_B/T   (sign of B = sign of mu_B)")
coef1 = 1 * (1 / 6) / (2 * np.pi ** 2 / 45 * gstar_EW)
P(f"   (single unit-B Weyl fermion, Cohen-Kaplan form 45 g/(12 pi^2 g*): {coef1:.6e})")

# Weinberg-operator (dimension five) Delta L = 2 freeze-out, order of magnitude [P]:
# Gamma ~ sum m^2 T^3 / (pi^3 v^4),  H = 1.66 sqrt(g*) T^2 / M_Pl
T_W = 1.66 * np.sqrt(gstar_EW) * np.pi ** 3 * v_EW ** 4 / (M_Pl * dm2_atm)
P(f"Weinberg-operator B-L freeze-out T_W ~ {T_W:.2e} GeV (order of magnitude; heavier nu -> lower)")

def s_today():
    return 2 * np.pi ** 2 / 45 * gs0 * T0 ** 3        # GeV^3
res = {}
for f, F in FOOT.items():
    P(f"\n================ footing {f}")
    R = F["R"]
    # ---------------- GD2
    eps = -R * m_bar
    P(f"GD2 neutral start: rho_K = -eps n_B (f -> 1, (Q+1)/2 with Q-1 ~ 1e-17 today) => R = -eps/m_bar")
    P(f"   eps = {eps:.5f} GeV  (m_p bracket {-R*m_p:.5f} GeV); sign: eps < 0 for rho_K > 0 with n_B > 0")
    P(f"   MU1: R x 2 -> eps = {-2*R*m_bar:.5f} GeV (doubles); eps -> -eps gives rho_K/rho_b = {-R:.3f} (flips)")
    h = F["h"]
    I0 = 3 * F["od"] / 2997.92458 ** 2
    P(f"KA5 I0 = 3 omega_d / (c/100 km/s/Mpc)^2 = {I0:.4e} Mpc^-2 (record MK1: 4.037e-8) ->",
      "PASS" if abs(I0 / 4.037e-8 - 1) < 2e-3 else "FAIL")
    # natural normalisation
    om_tot = F["ob"] + F["od"]
    rhoDE = (h ** 2 - om_tot - 4.18e-5) * rho_c_h2 * hbarc_cm ** 3   # GeV^4 (flat, radiation 4.18e-5 [P])
    E_L = rhoDE ** 0.25
    a0 = 9.3603e-11 if f == "canonical" else 1.1312e-10
    E_a0 = 6.582119569e-25 * a0 / 2.99792458e8      # hbar a0 / c in GeV
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
    cands["hbar a0 / c"] = E_a0
    best = sorted(cands.items(), key=lambda kv: abs(np.log(kv[1] / abs(eps))))[:3]
    within = [k for k, v in cands.items() if abs(v / abs(eps) - 1) <= 0.012]
    P(f"   natural normalisation: {len(cands)} energies from (M_Pl, rho_DE, a0, factors 1/2, 2); within 1.2 % of |eps|: {within}")
    for k, v in best:
        P(f"      nearest: {k} = {v:.4e} GeV  (ratio {v/abs(eps):.3f})")
    P(f"   eps = m_bar would give R = 1 exactly; R = 5.41 needs eps = {R:.3f} m_bar: no native normalisation -> eps is a NEW constant")
    # ---------------- GD3
    nB0 = F["ob"] * rho_c_h2 * hbarc_cm ** 3 / m_bar   # GeV^3
    eta_s = nB0 / s_today()
    P(f"GD3 observed n_B/s = {eta_s:.4e}  (n_B = {nB0/hbarc_cm**3*1e7:.4f}e-7 cm^-3)")
    muB = eps * 1.0                                   # Q = 1 (GD4)
    TD_need = abs(muB) * coef / eta_s
    P(f"   bias mu_B = eps*Q = {muB:.4f} GeV ; equilibrium n_B/s = {coef:.4e} * mu_B/T")
    P(f"   T_D giving the observed |n_B/s|: {TD_need:.3e} GeV  (Weinberg freeze-out ~ {T_W:.1e} GeV: ratio {T_W/TD_need:.1e})")
    for Ts in (T_sph - dT_sph, T_sph, T_sph + dT_sph):
        val = coef * muB / Ts
        P(f"   at sphaleron freeze-out T = {Ts:.1f} GeV: n_B/s = {val:.4e} -> X = |.|/obs = {abs(val)/eta_s:.3e}, sign {'antibaryons' if val < 0 else 'baryons'}")
    X = abs(coef * muB / T_sph) / eta_s
    P(f"   GD3 line X > 10 or wrong sign -> FAIL : X = {X:.3e}, sign wrong -> FAIL")
    P(f"   rescue by a separate B-L source: (B-L)/s needed = {(eta_s - coef*muB/T_sph)/(28/79):.4e} (in s units), tuned to 1 part in {X:.1e}")
    # with leptogenesis-type B-L source plus bias the final B = 28/79 (B-L) + bias term; the bias alone can't be avoided
    P(f"   MU2: eps x 1e-7 -> X = {X*1e-7:.3e} ({'passes' if X*1e-7 < 10 else 'still fails'}) ; T_sph -> 1e9 GeV -> X = {abs(coef*muB/1e9)/eta_s:.3e}")
    # ---------------- GD4
    P(f"GD4 energy per created baryon put into the clock: -eps*Q = {-eps:.4f} GeV (taken from the bath/decay energy); "
      f"vacuum threshold |eps| > m_p + m_e = {m_p+m_e:.5f}: {abs(eps) > m_p + m_e} (exceeded x{abs(eps)/(m_p+m_e):.2f}); "
      f"stable-vacuum ceiling R < {(m_p+m_e)/m_bar:.4f}")
    def a_of_T(T, gs):
        return (gs0 / gs) ** (1 / 3) * T0 / T
    for (lab, T, gs) in (("T_sph", T_sph, 106.75), ("T_D(needed)", TD_need, 106.75), ("BBN 0.1 MeV", 1e-4, 3.909)):
        a = a_of_T(T, gs)
        mu_need = np.sqrt(I0 / (2 * 0.01 * a ** 3))
        P(f"   Q-1 <= 0.01 at {lab} (a = {a:.3e}) needs mu_K >= {mu_need:.3e} Mpc^-1 (1/mu = {Mpc_GeVinv/mu_need*1.973269804e-16:.3e} m)")
        if lab == "T_sph":
            mu_sph = mu_need
            for mK in (198.25, 2.512e4, 8.89e6):
                P(f"      at record mu_K {mK:.4g}/Mpc: Q-1 at T_sph = {I0/(2*mK**2*a**3):.3e}  -> bias mu_B = eps*Q ~ {abs(eps)*(1+I0/(2*mK**2*a**3)):.3e} GeV")
            P(f"      MU3: mu_K / 10 raises Q-1 by {(I0/(2*(mu_need/10)**2*a**3))/(I0/(2*mu_need**2*a**3)):.1f}")
    # KA4: KD1 BBN stiff line, KD1's own formula
    abbn = 1 / (1 + 1e5 / (8.617333262e-5 * 2.7255)); Om_r = 2.47e-5 * (1 + 0.2271 * 3.046) / h ** 2; Om_d = F["od"] / h ** 2
    w0max = 0.067 * Om_r * abbn ** 2 / Om_d
    mu_bbn = np.sqrt(I0 / (4 * w0max))
    P(f"KA4 KD1 BBN stiff line (KD1's formula): mu_K >= {mu_bbn:.4e} Mpc^-1 (KD1: 8.890e6 / 8.889e6) ->",
      "PASS" if abs(mu_bbn / 8.89e6 - 1) < 2e-3 else "FAIL")
    # same stiff line at T_sph with entropy-correct a and g* radiation
    a = a_of_T(T_sph, 106.75)
    rho_d0 = F["od"] * rho_c_h2 * hbarc_cm ** 3
    rho_rad = np.pi ** 2 / 30 * 106.75 * T_sph ** 4
    w0max_s = 0.067 * rho_rad * a ** 6 / rho_d0
    P(f"   stiff/radiation <= 0.067 at T_sph needs mu_K >= {np.sqrt(I0/(4*w0max_s)):.3e} Mpc^-1")
    # ---------------- GD5 proton line
    E_rel = m_p + abs(eps)
    P(f"GD5 proton (eps<0): Delta B = -1 decays release {E_rel:.3f} GeV instead of {m_p:.3f}; dim-6 rate ~ E^5 -> x{(E_rel/m_p)**5:.2e}; "
      f"operator-scale bound from tau_p > 2.4e34 yr [P] moves up x{(E_rel/m_p)**1.25:.2f}. SM alone: no T = 0 B violation beyond exp(-4 pi/alpha_W) ~ {np.exp(-4*np.pi*30):.0e} (alpha_W 1/30)")
    res[f] = dict(eps=eps, X=X, TD=TD_need, eta=eta_s, mu_sph=mu_sph)

P("\n== summary (footings not pooled)")
for f, r in res.items():
    P(f"{f}: eps = {r['eps']:.4f} GeV ; obs n_B/s = {r['eta']:.3e} ; needed T_D = {r['TD']:.3e} GeV ; "
      f"sphaleron overshoot X = {r['X']:.3e} (antibaryons) ; mu_K for Q~1 at T_sph >= {r['mu_sph']:.2e}/Mpc")
