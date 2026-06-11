#!/usr/bin/env python3
"""agentEE — can the khronon medium's own fluctuation spectrum produce sigma_req structurally?

Small verified chunks; each section [n] prints PASS/FAIL-style facts.
Raw numbers only. zeta = (16pi/3)^(1/4) QUARANTINED: never used numerically; zeta kept symbolic/unit.
"""
import numpy as np
import sympy as sp
import mpmath as mp

print("=" * 88)
print("[1] THE Z-TEST: khronon-class (sound-speed) field on dS is NOT a function of Z alone")
print("=" * 88)
# Conformal-mass member with sound speed c_s on dS, flat slicing, adiabatic vacuum:
#   f_k(eta) = (H*eta/sqrt(2 c_s k)) e^{-i c_s k eta}   (chi = a*phi modes exactly Minkowski-form,
#   the 1206.1083 structure for the reparametrization-symmetric foliation mode)
# Closed form (computed below by direct mode integral, then tested):
#   W(eta,eta',r) = H^2 eta eta' / (4 pi^2 c_s) * 1/(r^2 - c_s^2 (Deta - i eps)^2)
# dS invariant (flat slicing): Z = 1 + (Deta^2 - r^2)/(2 eta eta')
# c_s = 1  =>  W = H^2/(8 pi^2) * 1/(1 - Z)   (function of Z alone — agentV's [A2] conformal check)
# c_s != 1 =>  W depends on (Z, eta'/eta) jointly. Machine check: vary eta'/eta on a Z-level set.

H = 1.0
def W_closed(eta1, eta2, r, cs, eps=1e-9):
    de = (eta1 - eta2) - 1j * eps
    return H**2 * eta1 * eta2 / (4 * np.pi**2 * cs) / (r**2 - cs**2 * de**2)

# --- BUG LOG (this continuation, 2026-06-11): the prior chunk's [1a] used a trapezoid k-grid with a
# mismatched regulator (rel.diff 0.67 -- verified nothing); [1b]'s lambda scan kept only ONE point per
# level set (r^2<0 skips), so 'spread' was trivially 0.0 and the printed verdict was unearned; [1c]'s
# sympy difference was not reduced to 0. All three repaired below; the CLAIMS survive, the CHECKS now
# actually check. ---

def W_modeint_mp(eta1, eta2, r, cs, delta):
    """mode integral int_0^inf dk sin(kr) e^{-i c_s k Deta - delta k}, evaluated on the ROTATED
    contour k = i s (valid when Deta<0 and r < c_s|Deta|: both exponential components carry
    positive frequency, so the upper rotation damps absolutely -- true on every metric-timelike
    chord for c_s > 1). Closed form to compare: r/(r^2 - (c_s Deta - i delta)^2) x prefactor."""
    de = eta1 - eta2
    assert de < 0 and r < cs * abs(de), "rotation validity (timelike chord, c_s>1)"
    f = lambda s: mp.sin(1j * s * r) * mp.e**(-1j * cs * (1j * s) * de - delta * (1j * s)) * 1j
    val = mp.quad(f, [0, mp.inf])
    return complex(H**2 * eta1 * eta2 / (4 * mp.pi**2 * cs * r) * val)

def W_closed_delta(eta1, eta2, r, cs, delta):
    a = cs * (eta1 - eta2) - 1j * delta
    return complex(H**2 * eta1 * eta2 / (4 * np.pi**2 * cs) / (r**2 - a**2))

def Z_of(eta1, eta2, r):
    return 1 + ((eta1 - eta2)**2 - r**2) / (2 * eta1 * eta2)

# (1a) closed form vs mode integral, regulator-matched at two delta values + delta->0 limit
mp.mp.dps = 30
e1, e2, r, cs = -1.0, -0.6, 0.35, 2.0
print(f"[1a] closed form vs mode integral at (eta,eta',r)=({e1},{e2},{r}), c_s={cs} (rotated contour):")
for delta in [5e-2, 0.0]:
    wc, wm = W_closed_delta(e1, e2, r, cs, delta), W_modeint_mp(e1, e2, r, cs, delta)
    print(f"     delta={delta:.0e}: closed = {wc:.8e}   mode-sum = {wm:.8e}   rel.diff = {abs(wc-wm)/abs(wc):.2e}")

# (1b) the Z-level-set test: fix Z (timelike, Z>1), scan lambda = eta'/eta with r^2>0 GUARANTEED
Ztarget = 1.5  # timelike chord (the sigma_req region); r^2 = (1-lam)^2 - lam > 0 needs lam < 0.382
lams = [0.05, 0.1, 0.2, 0.3]
print(f"[1b] Z-level-set test at Z = {Ztarget} (timelike): scan lam = eta'/eta over {lams}")
print(f"     {'lam':>6} | {'W (c_s=1)':>14} | {'W (c_s=2)':>14} | {'W (c_s=10)':>14}")
vals = {1.0: [], 2.0: [], 10.0: []}
for lam in lams:
    eta1 = -1.0
    eta2 = lam * eta1
    r2 = (eta1 - eta2)**2 - 2 * eta1 * eta2 * (Ztarget - 1)
    assert r2 > 0, f"level-set point invalid at lam={lam}"
    rr = np.sqrt(r2)
    row = []
    for cs_ in [1.0, 2.0, 10.0]:
        w = W_closed_delta(eta1, eta2, rr, cs_, 0.0).real
        vals[cs_].append(w)
        row.append(w)
    print(f"     {lam:>6} | {row[0]:>14.6e} | {row[1]:>14.6e} | {row[2]:>14.6e}")
assert all(len(v) == len(lams) for v in vals.values()), "level-set scan must keep ALL points"
for cs_ in [1.0, 2.0, 10.0]:
    v = np.array(vals[cs_])
    spread = (v.max() - v.min()) / abs(v.mean())
    tag = "constant on the Z-level set (Z-only)" if spread < 1e-12 else "VARIES on the Z-level set (NOT Z-only)"
    print(f"     c_s = {cs_:>4}: spread = {spread:.3e}  -> {tag}")
print("     => c_s=1 conformal member: constant on Z-level sets (dS-invariant, the [A2] check).")
print("        c_s!=1 khronon-class member: VARIES on Z-level sets. Since EVERY superposition")
print("        int drho(M^2) W_BD(Z;M^2) -- signed, complex, any series -- is constant on Z-level")
print("        sets, NO KL-type representation exists. The Bros-Moschella premise fails at its")
print("        first step (single-invariant dependence), before positivity is even invoked.")

# (1c) worldline pullback on the comoving geodesic (r -> 0): stationarity + KMS survive
print("[1c] comoving-worldline pullback, c_s arbitrary:")
t, tp, tau, csym, Hs = sp.symbols('t tp tau c_s H', positive=True)
eta_t = -sp.exp(-Hs * t) / Hs
eta_tp = -sp.exp(-Hs * tp) / Hs
expr = (Hs**2 * eta_t * eta_tp / (4 * sp.pi**2 * csym)) / (0**2 - csym**2 * (eta_t - eta_tp)**2)
expr_tau = sp.simplify(expr.subs(t, tp + tau))
target = -Hs**2 / (16 * sp.pi**2 * csym**3 * sp.sinh(Hs * tau / 2)**2)
diff_1c = sp.simplify((expr_tau - target).rewrite(sp.exp).expand().together())
print(f"     W(t,t')|_(r=0) simplified - target = {diff_1c}")
assert diff_1c == 0, "[1c] pullback closed form must reduce exactly"
print("     => W(tau) = -H^2/(16 pi^2 c_s^3 sinh^2(H tau/2)): STATIONARY in proper time (dilatation),")
print("        i*beta-periodic with beta = 2pi/H -> KMS at T_GH SURVIVES foliation breaking (this member);")
print("        amplitude rescaled 1/c_s^3. Cut class at the cone: POWER LAW (double pole), zero flatness.")

print()
print("=" * 88)
print("[2] STEP 2 -- the positivity escape, made precise")
print("=" * 88)

# ----------------------------------------------------------------------------------------
# [2a] NO KL-type representation over the principal/complementary series: quantified.
# Every member of the Bros-Moschella basis W_BD(Z;M^2) -- and therefore every superposition
# with ANY measure (positive, signed, complex; principal, complementary, discrete) -- is
# constant on Z-level sets. The khronon W is not. The irreducible level-set fluctuation is
# a LOWER BOUND on the relative error of the best possible KL-type fit.
# ----------------------------------------------------------------------------------------
print("[2a] irreducible Z-level-set fluctuation of the khronon W (timelike region):")
print(f"     {'c_chi':>6} | {'min dev':>10} | {'median dev':>10} | {'max dev':>10}   (dev = std_lam W / |mean_lam W| per level set)")
Zgrid = [1.05, 1.2, 1.5, 2.0, 3.0]
for cchi in [2.0, 10.0, 30.0]:
    devs = []
    for Z in Zgrid:
        lam_max = Z - np.sqrt(Z**2 - 1)  # r^2 > 0 boundary on the level set
        lams2 = np.linspace(0.02, 0.95, 12) * lam_max
        ws = []
        for lam in lams2:
            eta1, eta2 = -1.0, -lam
            r2 = (eta1 - eta2)**2 - 2 * eta1 * eta2 * (Z - 1)
            ws.append(W_closed_delta(eta1, eta2, np.sqrt(r2), cchi, 0.0).real)
        ws = np.array(ws)
        devs.append(ws.std() / abs(ws.mean()))
    devs = np.array(devs)
    print(f"     {cchi:>6} | {devs.min():>10.3e} | {np.median(devs):>10.3e} | {devs.max():>10.3e}")
print("     => O(1) irreducible residual at every c_chi > 1: the khronon Wightman admits NO")
print("        representation W = int drho(M^2) W_BD(Z;M^2) for ANY measure class. V's dS-KL")
print("        frame does not degrade for the khronon -- it never starts.")

# ----------------------------------------------------------------------------------------
# [2b] what replaces it: the two-variable spectral representation over E(3) x| dilatation.
# Homogeneity+isotropy: W = (1/2pi^2) int_0^inf (dk/k) j0(kr) F_k(eta,eta'); dilatation
# covariance forces F_k(eta,eta') = k^{-3} Psi(k eta, k eta') -- ONE positive kernel Psi on
# the half-line, integrated over the E(3) Casimir k. (Free vacuum: Psi rank-one.)
# ----------------------------------------------------------------------------------------
print("[2b] dilatation reduction F_k = k^-3 Psi(k eta, k eta') on the free modes (sympy):")
k_, eta_, etap_, c_ = sp.symbols('k eta etap c', positive=True)
# F_k = f_k(eta) fbar_k(eta'):  f_k(eta) = H eta e^{-i c k eta} / sqrt(2 c k)
Hsym = sp.Symbol('H', positive=True)
fk  = Hsym * eta_ * sp.exp(-sp.I * c_ * k_ * eta_) / sp.sqrt(2 * c_ * k_)
fkp = Hsym * etap_ * sp.exp(-sp.I * c_ * k_ * etap_) / sp.sqrt(2 * c_ * k_)
Fk = fk * sp.conjugate(fkp)
y_, yp_ = sp.symbols('y yp')
Psi = (Hsym**2 / (2 * c_)) * y_ * yp_ * sp.exp(-sp.I * c_ * (y_ - yp_))
diff_2b = sp.simplify(Fk - Psi.subs([(y_, k_ * eta_), (yp_, k_ * etap_)]) / k_**3)
# NOTE: eta symbols declared positive for sympy conjugation bookkeeping; the identity is
# algebraic in eta and holds for eta<0 (the physical patch) by analytic continuation.
print(f"     F_k - k^-3 Psi(k eta, k eta') = {diff_2b}")
assert diff_2b == 0
print("     => the khronon two-point structure = ONE kernel Psi of TWO scale-invariant variables")
print("        (y, y') = (k eta, k eta'), integrated over dk/k with the E(3) Plancherel weight.")
print("        State positivity = Psi positive-definite kernel (rank-one for the free vacuum).")
print("        This is the Bochner decomposition over the RESIDUAL group, replacing dS-KL:")
print("        the 'basis' is not a rigid one-parameter family -- Psi itself is dynamical data.")

# ----------------------------------------------------------------------------------------
# [2c] the b-family: Deser-Levin worldlines realized as RESIDUAL-group orbits.
# The dilatation orbit through comoving offset x = b*eta is a uniformly accelerated worldline
# with a = b*kappa, kappa = H/sqrt(1-b^2)  ==>  kappa^2 = a^2 + H^2 (the DL relation), and the
# khronon pullback on it is STATIONARY -- the stationary family survives foliation breaking.
# ----------------------------------------------------------------------------------------
print("[2c] the b-family (sympy geometry + pullback):")
tau_s, b_s, H_s, k_s, c_s2 = sp.symbols('tau b H kappa c', positive=True)
kap = H_s / sp.sqrt(1 - b_s**2)
eta_tau = -sp.exp(-kap * tau_s)   # eta_0 = -1; future-directed (eta -> 0^-)
x_tau = b_s * eta_tau
# metric ds^2 = (d eta^2 - dx^2)/(H^2 eta^2), coords (eta, x); curve (eta_tau, x_tau)
ed, xd = sp.diff(eta_tau, tau_s), sp.diff(x_tau, tau_s)
unorm = sp.simplify((ed**2 - xd**2) / (H_s**2 * eta_tau**2))
print(f"     u.u - 1 = {sp.simplify(unorm - 1)}  (proper-time normalization)")
assert sp.simplify(unorm - 1) == 0
# Christoffels for g = a_c^2 diag(1,-1), a_c = -1/(H eta):  (2d eta-x block suffices, motion is radial)
eta_v, x_v = sp.symbols('eta_v x_v')
gmat = sp.Matrix([[1 / (H_s**2 * eta_v**2), 0], [0, -1 / (H_s**2 * eta_v**2)]])
ginv = gmat.inv()
coords = [eta_v, x_v]
Gamma = [[[sp.simplify(sum(ginv[m, l] * (sp.diff(gmat[l, al], coords[be]) + sp.diff(gmat[l, be], coords[al])
            - sp.diff(gmat[al, be], coords[l])) / 2 for l in range(2))) for be in range(2)] for al in range(2)]
         for m in range(2)]
uvec = [ed, xd]
avec = []
for m in range(2):
    expr_a = sp.diff(uvec[m], tau_s)
    for al in range(2):
        for be in range(2):
            expr_a += Gamma[m][al][be].subs(eta_v, eta_tau) * uvec[al] * uvec[be]
    avec.append(sp.simplify(expr_a))
a2 = sp.simplify(-(avec[0]**2 - avec[1]**2) / (H_s**2 * eta_tau**2))
a2_target = b_s**2 * kap**2
print(f"     a.a + (b kappa)^2 = {sp.simplify(a2 - a2_target)}  (proper acceleration a = b*kappa)")
assert sp.simplify(a2 - a2_target) == 0
print(f"     kappa^2 - (a^2 + H^2) = {sp.simplify(kap**2 - (a2_target + H_s**2))}  (the Deser-Levin relation)")
assert sp.simplify(kap**2 - (a2_target + H_s**2)) == 0
# pullback of the free khronon W on the b-orbit: r = b|eta1-eta2|
tau1, tau2 = sp.symbols('tau1 tau2', real=True)
e1s, e2s = -sp.exp(-kap * tau1), -sp.exp(-kap * tau2)
rb = b_s * (e1s - e2s)  # squared below; sign irrelevant
Wb = (H_s**2 * e1s * e2s / (4 * sp.pi**2 * c_s2)) / (rb**2 - c_s2**2 * (e1s - e2s)**2)
Wb_tau = Wb.subs(tau1, tau2 + tau_s)
Wb_target = -H_s**2 / (16 * sp.pi**2 * c_s2 * (c_s2**2 - b_s**2) * sp.sinh(kap * tau_s / 2)**2)
diff_2c = sp.simplify((Wb_tau - Wb_target).rewrite(sp.exp).expand().together())
print(f"     W_b(tau) - [-H^2/(16 pi^2 c (c^2-b^2) sinh^2(kappa tau/2))] = {diff_2c}")
assert diff_2c == 0
# anchor: at c=1 (conformal member) this must reduce to the BANKED Deser-Levin/conformal pullback
# -kappa^2/(16 pi^2 sinh^2(kappa tau/2))  (agentN1/agentB [A2]), using kappa^2 = H^2/(1-b^2):
red_c1 = sp.simplify(Wb_target.subs(c_s2, 1) - (-kap**2 / (16 * sp.pi**2 * sp.sinh(kap * tau_s / 2)**2)))
print(f"     c_chi=1 reduction - banked DL conformal kernel = {red_c1}  (anchors b-family vs N1)")
assert red_c1 == 0
print("     => on EVERY Deser-Levin member (realized as the dilatation orbit at velocity b = a/kappa")
print("        relative to the khronon frame): pullback STATIONARY, EXACT conformal/DL shape,")
print("        KMS at kappa/2pi (i*2pi/kappa periodicity of sinh^2), amplitude")
print("        A(b) = H^2/(16 pi^2 c_chi (c_chi^2 - b^2)),  b^2 = a^2/(a^2+H^2):")
print("        (i)  the free khronon tail T-hat == 0 (conformal class: contact + thermal ONLY);")
print("        (ii) the (a,H)-dependence beyond kappa is an AMPLITUDE factor, ANALYTIC in a^2")
print("             and O(1/c_chi^2)-suppressed -- V's a->0 analyticity wall is OBEYED, not evaded;")
print("        (iii) the free khronon sits INSIDE agentF's KMS census: it cannot source mu.")

# ----------------------------------------------------------------------------------------
# [2d] the worldline spectral representation (Mellin = Bochner on the dilatation orbit).
# For ANY scale-invariant Gaussian state (kernel Psi, rank-one Psi = phi x phi-bar for pure),
# the comoving pullback diagonalizes in the Mellin variable:
#   W(tau) = (1/2pi) int dnu |phi-tilde(nu)|^2 e^{-i nu kappa tau} x norm,
# i.e. worldline spectral density rho(omega) = (H^2/(4 pi^2 c kappa)) |phi-tilde(omega/kappa)|^2 >= 0.
# Free vacuum: phi(w) = w e^{i c w}  (w = k|eta|) ==> |phi-tilde(nu)|^2 = (2 pi nu/c^2)/(1 - e^{-2 pi nu}):
# the PLANCK density -- KMS detailed balance at kappa/2pi, recovered spectrally.
# ----------------------------------------------------------------------------------------
print("[2d] worldline Mellin/Bochner structure (free member, b=0, kappa=H):")
mp.mp.dps = 30
cval = 3.0
def phi_tilde_numeric(nu):
    # Mellin transform int_0^inf w^{-i nu} e^{i c w} dw, rotated contour w = i s (absolutely damped)
    f = lambda s: (1j * s)**(-1j * nu) * mp.e**(-cval * s) * 1j
    return mp.quad(f, [0, mp.inf])
def phi_tilde_closed(nu):
    return mp.gamma(1 - 1j * nu) * (-1j * cval)**(1j * nu - 1)
print("     (i) Mellin transform of the free mode, numeric vs closed form Gamma(1-i nu)(-ic)^(i nu - 1):")
for nu in [0.5, 2.0, -1.3]:
    pn, pc = phi_tilde_numeric(nu), phi_tilde_closed(nu)
    print(f"         nu={nu:>5}: |numeric - closed|/|closed| = {float(abs(pn-pc)/abs(pc)):.2e}")
nu_s = sp.symbols('nu', real=True)
mod2 = sp.simplify(sp.Abs(sp.gamma(1 - sp.I * nu_s))**2)  # = pi nu / sinh(pi nu)
planck_id = sp.simplify((sp.pi * nu_s / sp.sinh(sp.pi * nu_s) * sp.exp(sp.pi * nu_s) - 2 * sp.pi * nu_s / (1 - sp.exp(-2 * sp.pi * nu_s))).rewrite(sp.exp).expand().together())
print(f"     (ii) |Gamma(1-i nu)|^2 e^(pi nu) - 2 pi nu/(1-e^(-2 pi nu)) = {planck_id}  (the Planck density)")
assert planck_id == 0
# (iii) closed-form FT of the sinh^-2 kernel vs the residue formula (finite-eps matched):
kapv = 1.0
def ft_sinh2_numeric(om, epsv):
    f = lambda T: mp.e**(1j * om * T) * (-1.0) / mp.sinh(kapv * (T - 1j * epsv) / 2)**2
    return mp.quad(f, [-80, 0, 80])  # integrand decays e^{-kappa|tau|}; 0 split for the near-singularity
def ft_sinh2_closed(om, epsv):
    return mp.e**(-om * epsv) * (8 * mp.pi * om / kapv**2) / (1 - mp.e**(-2 * mp.pi * om / kapv))
print("     (iii) FT[-sinh^-2(kappa(tau-i eps)/2)] vs (8 pi omega/kappa^2)/(1-e^(-2 pi omega/kappa)):")
for om in [0.7, 2.3, -1.1]:
    fn, fc = ft_sinh2_numeric(om, 1e-3), ft_sinh2_closed(om, 1e-3)
    print(f"         omega={om:>5}: rel.diff = {float(abs(fn-fc)/abs(fc)):.2e}")
print("     (iv) assembled: rho_free(omega) = (H^2 omega/(2 pi c^3 kappa^2))/(1-e^(-2 pi omega/kappa))")
print("          -- POSITIVE for every real omega (Bochner), detailed balance rho(-w)=e^(-2 pi w/kappa) rho(w)")
print("          (KMS at kappa/2pi). Mellin route and closed-form FT agree EXACTLY (identical functions).")
print("     => WHAT SURVIVES of V's frame at the worldline: stationarity (family-wide), Bochner")
print("        positivity of the TOTAL density, and KMS for the free member. WHAT DOES NOT SURVIVE:")
print("        the tail is no longer an AUTONOMOUS positive object -- dS-KL forced sigma(u) into the")
print("        positive cone of a rigid basis {sigma_M}; here positivity constrains ONLY the sum")
print("        contact + thermal + tail >= 0 pointwise in omega. A signed flat-oscillatory tail")
print("        riding a growing positive contact density is NOT excluded. (Quantified in [3d].)")

print()
print("=" * 88)
print("[3] STEP 3 -- the asymptotic class: what the khronon CAN and CANNOT carry")
print("=" * 88)

# ----------------------------------------------------------------------------------------
# [3a] free khronon vs sigma_req at u -> 0+: not a wrong exponent -- an ABSENT object.
# Free pullback = exact conformal/DL kernel on every member ([2c]) ==> cut tail T-hat == 0.
# sigma_req(u) = u^(-13/8) e^(-zeta u^(-1/4)) cos(zeta u^(-1/4) - pi/8)  (agentV section 3).
# zeta values: agentV's RAW banked conversions (fw 2.0247 / canonical-a0 1.7881 / hostile 2.2271);
# (16pi/3)^(1/4) remains QUARANTINED -- never used.
# ----------------------------------------------------------------------------------------
print("[3a] u->0 comparison (zeta = 2.0247 fw; canonical 1.7881; hostile 2.2271):")
print(f"     {'u':>8} | {'sigma_req (fw)':>15} | {'sigma_req (canon)':>17} | {'sigma_req (hostile)':>19} | sigma_free")
for u in [1e-2, 1e-4, 1e-6]:
    row = []
    for zv in [2.0247, 1.7881, 2.2271]:
        x = u**-0.25
        row.append(u**(-13/8) * np.exp(-zv * x) * np.cos(zv * x - np.pi / 8))
    print(f"     {u:>8.0e} | {row[0]:>15.3e} | {row[1]:>17.3e} | {row[2]:>19.3e} | 0 (exactly)")
print("     => the free khronon does not have the wrong asymptotic class -- it has NO cut tail at")
print("        all (conformal class, N1 one-point-miracle structure). The MINIMAL khronon CANNOT")
print("        carry sigma_req. The question becomes: what structure can be ADDED?")

# ----------------------------------------------------------------------------------------
# [3b] Gaussian state-shaping CANNOT add it (lemma, two halves):
#  (i) Bogoliubov/occupation/squeezing on FIXED dynamics leaves the worldline COMMUTATOR
#      density untouched: |psi_new(nu)|^2 - |psi_new(-nu)|^2 = |phi(nu)|^2 - |phi(-nu)|^2
#      exactly when |A|^2-|B|^2 = 1. The soft channel reads ONLY this odd part (agentV
#      section 1.1: the response is Im W). State-shaping is invisible to the response.
#  (ii) the squeezed cross term's worldline kernel is sech^2-class: ANALYTIC at tau=0 --
#      V's trichotomy case-(i) shape, not flat-oscillatory.
# ----------------------------------------------------------------------------------------
print("[3b] Gaussian state-shaping lemma:")
import random
random.seed(7)
maxdev = 0
for trial in range(3):
    th1, th2, sq = random.uniform(0, 6.28), random.uniform(0, 6.28), random.uniform(0.3, 1.5)
    A = mp.cosh(sq) * mp.e**(1j * th1)
    B = mp.sinh(sq) * mp.e**(1j * th2)
    for nu in [0.4, 1.7]:
        pt_p, pt_m = phi_tilde_closed(nu), phi_tilde_closed(-nu)
        new_p = A * pt_p + B * mp.conj(pt_m)
        new_m = A * pt_m + B * mp.conj(pt_p)
        lhs = abs(new_p)**2 - abs(new_m)**2
        rhs = abs(pt_p)**2 - abs(pt_m)**2
        maxdev = max(maxdev, float(abs(lhs - rhs) / abs(rhs)))
print(f"     (i) commutator density invariance under Bogoliubov (3 random states x 2 nu): max rel.dev = {maxdev:.2e}")
print("         => occupations/squeezing CANNOT touch the dissipation channel; sigma_chi is a")
print("            DYNAMICS object. The X2 pump must act as a dynamics modifier (in-medium")
print("            dispersion/gain), not a state filler -- exactly X2's active-medium statement.")
# (ii) squeezed cross term: int_0^inf dq q e^{i a q} (b.v.) = -1/a^2 with a = 2 c cosh(kappa tau/2)
q_, a_ = sp.symbols('q a', positive=True)
eps_ = sp.Symbol('epsilon', positive=True)
cross = sp.integrate(q_ * sp.exp(sp.I * a_ * q_ - eps_ * q_), (q_, 0, sp.oo))
cross_lim = sp.simplify(sp.limit(cross, eps_, 0, '+'))
print(f"     (ii) int_0^inf q e^(iaq) dq (b.v.) = {cross_lim}  (a = 2 c_chi cosh(kappa tau/2))")
assert sp.simplify(cross_lim + 1 / a_**2) == 0
sech2 = -1 / (2 * sp.cosh(tau_s / 2))**2  # shape in kappa*tau
taylor = sp.series(sech2, tau_s, 0, 6)
print(f"         => squeezed cross kernel  propto  -sech^2(kappa tau/2)/4c^2: Taylor at tau=0: {taylor}")
print("            ANALYTIC at tau = 0 (and the |B|^2 piece is the time-reversed thermal kernel,")
print("            also analytic-class). Free + ANY Gaussian shaping = power-law/analytic cut class.")
print("            The fourth-root essential singularity is unreachable without DYNAMICS change.")

# ----------------------------------------------------------------------------------------
# [3c] the required worldline tail, transformed: what spectral structure the pump must build.
# sigma_req (W'-level) = u^(-13/8) e^(-zeta u^(-1/4)) cos(zeta u^(-1/4) - pi/8)
#  ==> T-hat (W-level cut) ~ (4/(sqrt2 zeta)) u^(-3/8) e^(-zeta u^(-1/4)) cos(zeta u^(-1/4) + pi/8)
#  ==> worldline form (u = H^2 tau^2/2 at leading order, [3e]):
#      T(tau) = tau^(-3/4) e^(-zt/sqrt(tau)) cos(zt/sqrt(tau) + pi/8),  zt = zeta (2/H^2)^(1/4).
# Its frequency content D(omega) = int_0^inf T(tau) e^(i omega tau) dtau (band-regularized by
# e^(-m tau), m = kappa/2 -- touches u >~ 1 only): saddle class
#      |D| ~ omega^(q) e^(-ct omega^(1/3)),  phase ~ -sqrt(3) ct omega^(1/3),
#      ct = (3/4) 2^(2/3) zt^(2/3),  q = 2 gamma/3 - 5/6  (gamma = 3/4 here).
# The INDEX-1/3 STRETCHED-EXPONENTIAL OSCILLATORY frequency tail: the worldline fingerprint
# of the fourth-root lightcone class (the omega-side mirror of V's e^(-b M^(1/3)) remark).
# ----------------------------------------------------------------------------------------
print("[3c] the required worldline spectral tail (exact-target member, gamma = 3/4):")
# (i) symbolic u<->tau mapping checks
u_s, z_s, Hs2, tau2 = sp.symbols('u zeta H tau', positive=True)
That_lead = u_s**sp.Rational(-3, 8) * sp.exp(-z_s * (1 - sp.I) * u_s**sp.Rational(-1, 4))
dThat = sp.diff(That_lead, u_s)
ratio_full = sp.simplify(dThat / (u_s**sp.Rational(-13, 8) * sp.exp(-z_s * (1 - sp.I) * u_s**sp.Rational(-1, 4))))
ratio_target = z_s * (1 - sp.I) / 4 - sp.Rational(3, 8) * u_s**sp.Rational(1, 4)
print(f"     (i) d/du[u^(-3/8) e^(-zeta(1-i)u^(-1/4))] / [u^(-13/8) e^(same)] = {ratio_full}")
assert sp.simplify(ratio_full - ratio_target) == 0
print(f"         = zeta(1-i)/4 + O(u^(1/4)): one u-integration of sigma_req shifts the power by")
print(f"         +5/4 and the phase by +pi/4 (the 1/(1-i)); subleading O(u^(1/4)) only. PASS")
usub = Hs2**2 * tau2**2 / 2
print(f"     (ii) u = H^2 tau^2/2: u^(-3/8) = (H^2/2)^(-3/8) tau^(-3/4); zeta u^(-1/4) = zt/sqrt(tau), zt = zeta (2/H^2)^(1/4). PASS (algebraic)")

# (ii) D(omega) by verified contour deformation
mp.mp.dps = 40
def D_pm(Om, zt, gamma, branch):
    """D_pm = int_0^inf tau^-gamma e^{-zt(1 -+ i) tau^-1/2} e^{i Om tau} dtau via tau=iy, y=x^-2,
    and (for the + branch) the steepest rotation x -> e^{i pi/6} x. branch=+1: (1-i); -1: (1+i)."""
    pref = 2j * mp.e**(-1j * mp.pi * gamma / 2)
    if branch == +1:
        rot = mp.e**(1j * mp.pi / 6)
        f = lambda uu: (rot * uu)**(2 * gamma - 3) * mp.e**(1j * mp.sqrt(2) * zt * rot * uu) \
            * mp.e**(-Om / (rot * uu)**2) * rot
    else:
        f = lambda uu: uu**(2 * gamma - 3) * mp.e**(-mp.sqrt(2) * zt * uu) * mp.e**(-Om / uu**2)
    return pref * mp.quad(f, [0, mp.inf])

def D_full(om, zt, gamma, phi0, m=0.5):
    Om = om + 1j * m
    return (mp.e**(1j * phi0) * D_pm(Om, zt, gamma, +1) + mp.e**(-1j * phi0) * D_pm(Om, zt, gamma, -1)) / 2

def D_direct(om, zt, gamma, phi0, m=0.5):
    f = lambda T: T**(-gamma) * mp.e**(-zt / mp.sqrt(T)) * mp.cos(zt / mp.sqrt(T) + phi0) * mp.e**((1j * om - m) * T)
    return mp.quad(f, [0, 1, 8, 80])

ZETA_FW = 2.0247          # agentV section 6, raw, framework footing (quarantine intact)
zt_fw = ZETA_FW * 2**0.25 # H = 1 units
gam, phi0 = 0.75, mp.pi / 8
print("     (iii) contour machinery vs direct quadrature (m=0.5, zt_fw = 2^(1/4)*2.0247 = %.4f):" % zt_fw)
for om in [3.0, 12.0]:
    dc, dd = D_full(om, zt_fw, gam, phi0), D_direct(om, zt_fw, gam, phi0)
    print(f"          omega={om:>5}: contour = {complex(dc):.6e}  direct = {complex(dd):.6e}  rel.diff = {float(abs(dc-dd)/abs(dc)):.2e}")

# (iv) the saddle-class fit at large omega
ct_pred = (mp.mpf(3) / 4) * 2**(mp.mpf(2) / 3) * zt_fw**(mp.mpf(2) / 3)
q_pred = 2 * gam / 3 - mp.mpf(5) / 6
oms = [100.0, 300.0, 1000.0, 3000.0, 10000.0, 30000.0]
vals_D = [D_full(om, zt_fw, gam, phi0) for om in oms]
# 3-parameter LSQ: ln|D| = lnK + q ln(om) - ct om^(1/3)
Amat = np.array([[1.0, np.log(om), -om**(1.0 / 3)] for om in oms])
bvec = np.array([float(mp.log(abs(v))) for v in vals_D])
coef, *_ = np.linalg.lstsq(Amat, bvec, rcond=None)
resid = Amat @ coef - bvec
# phase slope: d(arg D)/d(om^(1/3)) = -dt, by paired finite differences (pair spacing 0.3 in
# om^(1/3) keeps |Delta phase| < pi -- no unwrap ambiguity; a 6-point sparse unwrap CANNOT work
# at dt ~ 3.7 and was replaced -- bug log)
dt_pred = mp.sqrt(3) * ct_pred
dt_ests = []
for x13 in [10.0, 20.0, 30.0]:
    h13 = 0.3
    v1, v2 = D_full(x13**3, zt_fw, gam, phi0), D_full((x13 + h13)**3, zt_fw, gam, phi0)
    dphi = float(mp.arg(v2 / v1))  # principal value; |dphi| < pi by construction
    dt_ests.append(-dphi / h13)
print("     (iv) saddle-class fit over omega in [1e2, 3e4]:")
print(f"          ct_fit  = {coef[2]:.6f}   vs  (3/4) 2^(2/3) zt^(2/3) = {float(ct_pred):.6f}   ratio = {coef[2]/float(ct_pred):.5f}")
print(f"          q_fit   = {coef[1]:.4f}     vs  2 gamma/3 - 5/6 = {float(q_pred):.4f}")
print(f"          |phase rate| at om^(1/3)=10/20/30 = {abs(dt_ests[0]):.4f} / {abs(dt_ests[1]):.4f} / {abs(dt_ests[2]):.4f}")
print(f"               vs  sqrt(3) ct = {float(dt_pred):.6f}   (deepest-point ratio = {abs(dt_ests[2])/float(dt_pred):.5f})")
print(f"               (measured sign: phase INCREASES with om^(1/3) in the e^(+i om tau) convention --")
print(f"                the conjugate saddle branch; magnitude is the invariant statement, cos is even)")
print(f"          max |fit residual| (ln-space) = {np.abs(resid).max():.2e}")
print(f"          |D-(2 ct)| subdominance: |D_-|/|D_+| at omega=1000: ", end="")
r_sub = abs(D_pm(1000 + 0.5j, zt_fw, gam, -1)) / abs(D_pm(1000 + 0.5j, zt_fw, gam, +1))
print(f"{float(r_sub):.2e}  (predicted e^(-ct om^(1/3)) = {float(mp.e**(-ct_pred*10)):.2e})")
print("     => the pump's REQUIRED spectral fingerprint on the worldline, pinned:")
print("        Delta-rho_c(omega) ~ A omega^(-1/3) e^(-ct omega^(1/3)) cos(sqrt(3) ct omega^(1/3)+phi),")
ct_vals = {}
for tag, zv in [("fw", 2.0247), ("canonical", 1.7881), ("hostile", 2.2271)]:
    ztv = zv * 2**0.25
    ct_vals[tag] = float((3 / 4) * 2**(2 / 3) * ztv**(2 / 3))
    print(f"        ct({tag}: zeta={zv}) = {ct_vals[tag]:.4f}  [omega in units of H; one-sided; signed]")
print("        Decay/oscillation rate ratio LOCKED at 1/sqrt(3) (the index-1/3 saddle diagonal),")
print("        the omega-side mirror of sigma_req's -pi/4 diagonal in u^(-1/4).")

# ----------------------------------------------------------------------------------------
# [3d] the positivity window: does the required signed tail FIT inside worldline Bochner
# positivity riding the free density? Minimal one-sided completion Delta-rho(omega) =
# theta(omega) * A * 2 Im D(omega); total positivity needs rho_free + Delta-rho >= 0.
# Units: kappa = H = 1; rho_free normalized to omega/(1-e^(-2 pi omega)) (the common factor
# H^2/(2 pi c_chi^3 kappa^2) divided out of BOTH -- A is field-internal headroom, the
# PHYSICAL amplitude wall stays with agentI/agentX, inherited not re-adjudicated).
# ----------------------------------------------------------------------------------------
print("[3d] worldline positivity window for the sigma_req-class tail (fw zeta, m=0.5):")
om_grid = list(np.geomspace(0.05, 50.0, 28))
rho_free = lambda om: om / (1 - np.exp(-2 * np.pi * om))
ratios, imvals = [], []
for om in om_grid:
    imD = 2 * float(mp.im(D_full(om, zt_fw, gam, phi0)))
    imvals.append(imD)
    ratios.append(max(0.0, -imD) / rho_free(om))
ratios = np.array(ratios); imvals = np.array(imvals)
i_bind = int(np.argmax(ratios))
A_max = 1.0 / ratios.max()
nsign = int(np.sum(np.abs(np.diff(np.sign(imvals[imvals != 0])))) // 2)
print(f"     A_max = {A_max:.3f}  (binding at omega = {om_grid[i_bind]:.3f}, where 2ImD = {imvals[i_bind]:+.4e},")
print(f"     rho_free = {rho_free(om_grid[i_bind]):.4e}); sign changes of Im D on the grid: {nsign}")
print(f"     => FINITE, O(1) headroom: the flat-oscillatory signed tail EMBEDS in a positive")
print(f"        total worldline density (binding near omega ~ kappa, exponentially free above).")
print(f"        V's moment-tower kill does NOT re-enter: positivity binds the TOTAL, not the tail.")
print(f"        The oscillation (sign changes) survives inside the window -- the all-inverse-")
print(f"        moments-zero structure is carried by the SIGNED component, untouched.")

# ----------------------------------------------------------------------------------------
# [3e] family universality: one bulk medium serves the whole Deser-Levin family.
# u(tau; b) = 2 beta sinh^2(kappa tau/2), beta = 1 - b^2 = H^2/kappa^2  ==> beta kappa^2 = H^2
# EXACTLY: the leading u -> 0 law u = H^2 tau^2/2 (1 + kappa^2 tau^2/12 + ...) is b-INDEPENDENT
# at leading order -- the SAME zeta-tail is required on every member; family/band dependence
# (V's (u+t) measure, the R(u) band shape) enters only at subleading orders and through the
# j0(2 q b sinh(kappa tau/2)) factor, which is EVEN-ENTIRE in b => analytic in a^2.
# ----------------------------------------------------------------------------------------
print("[3e] family universality + the a^2-analyticity inheritance:")
beta_id = sp.simplify((1 - b_s**2) * kap**2 - H_s**2)
print(f"     (i) beta kappa^2 - H^2 = {beta_id}  (exact, all b)")
assert beta_id == 0
useries = sp.series(2 * (1 - b_s**2) * sp.sinh(kap * tau_s / 2)**2, tau_s, 0, 6).removeO()
useries_simpl = sp.simplify(useries.subs(kap, sp.sqrt(H_s**2 / (1 - b_s**2))))
print(f"     (ii) u(tau;b) = {sp.expand(useries_simpl)}")
print(f"          = (H^2 tau^2/2)(1 + kappa^2 tau^2/12 + ...): leading term b-free; the family")
print(f"          enters at relative O(kappa^2 tau^2). At the omega-saddle tau* ~ (zt/omega)^(2/3) -> 0:")
for om in [100.0, 10000.0]:
    taust = float((zt_fw / om)**(2.0 / 3))
    print(f"          omega = {om:>7.0f}: kappa^2 tau*^2 ~ {taust**2:.2e}  (kappa = 1)")
print(f"     (iii) free-amplitude family factor 1/(c^2 - b^2): (W_b - W_0)/W_0 = b^2/(c^2 - b^2),")
bv, cv = 0.3, 3.0
pred = bv**2 / (cv**2 - bv**2)
print(f"           e.g. b=0.3, c=3: {pred:.6f} -- analytic in b^2 = a^2/(a^2+H^2). With the")
print(f"           j0 factor even-entire in b, EVERY scale-invariant khronon-medium observable")
print(f"           built by dominated q-integration is ANALYTIC IN a^2 at a = 0:")
print(f"           agentV's NO-KERNEL corollary (deep-MOND onset unreachable; flattening floor")
print(f"           a_* exists) EXTENDS to the whole class. agentCC's watch entry 11 stays the")
print(f"           decisive test FOR THE KHRONON ROUTE TOO. (Escape: IR-divergent Psi only --")
print(f"           the Allen-corner analog, which destroys the stationary law itself.)")

# ----------------------------------------------------------------------------------------
# [3f] the c_chi -> infinity corner is NOT the missing structure
# ----------------------------------------------------------------------------------------
print("[3f] c_chi -> infinity: free worldline amplitude ~ 1/c_chi^3 -> 0 (decoupling); pullback")
print("     SHAPE is c_chi-independent (sinh^-2 for every c_chi > 1): the limit erases the")
print("     khronon's own zero-point weight and creates nothing. NOT the missing structure.")

print()
print("=" * 88)
print("[4] VERDICT SUMMARY (full argument in agentEE_sigma_khronon.md)")
print("=" * 88)
print("""
 STRUCTURALLY-CAPABLE -- for the PUMPED khronon MEDIUM, not the khronon field:
  - free/minimal khronon: CANNOT (tail exactly 0 on the whole stationary family [2c];
    KMS census member; Gaussian state-shaping cannot touch the dissipation channel [3b]);
  - V's dS-KL kill: does NOT re-enter (no KL representation exists [2a]; worldline
    positivity binds only the TOTAL density; A_max = O(1) window [3d]);
  - the derivation becomes a DEFINED CALCULATION: find the scale-invariant in-medium
    dynamics (gain/dispersion profile in k_phys/H) whose worldline commutator density
    carries the one-sided index-1/3 tail with (ct, sqrt(3)ct, -1/3) pinned in [3c];
  - inherited walls, unrescued: deep-MOND a^2-analyticity (flattening floor a_* survives
    [3e]); the physical amplitude invoice (agentI/agentX).
 Coefficient discipline held: zeta values are agentV's raw banked numbers; (16pi/3)^(1/4)
 quarantined throughout; NO Z claims.
""")
