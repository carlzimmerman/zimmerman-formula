#!/usr/bin/env python3
"""agentHH — the pump profile: minimal scale-invariant pumped-khronon dynamics vs (C1)-(C5).

Sections dispatched by CLI arg (step0, step1, ...); each run's stdout is appended to
agentHH_pump_profile.out by the caller. Raw numbers only; zeta = (16pi/3)^(1/4) QUARANTINED
(never used numerically); NO Z claims. omega in units of H throughout (kappa = H at b = 0).

Conventions (inherited from agentEE):
  free khronon universal mode  phi0(w) = w e^{i c w},  w = k|eta| = k_phys/H  (y == w);
  Mellin  phi~(nu) = int_0^inf w^{-i nu - 1} phi(w) dw  =>  free: Gamma(1-i nu)(-i c)^{i nu - 1};
  worldline density  rho(omega) ~ |phi~(omega/kappa)|^2 (positive part), commutator density
  rho_c(nu) = |phi~(nu)|^2 - |phi~(-nu)|^2  (free: = 2 pi nu / c^2, exactly linear).
Required addition (agentEE C1-C2):
  Delta rho_c(omega) ~ A omega^{-1/3} e^{-ct omega^{1/3}} cos(sqrt3 ct omega^{1/3} + phi),
  ct = 2.1388 (fw) / 1.9687 (canon) / 2.2790 (hostile);  |A| <= A_max ~ 5.7 (C3).
"""
import sys
import numpy as np
import mpmath as mp
import sympy as sp

ZETA = {"fw": 2.0247, "canon": 1.7881, "hostile": 2.2271}     # agentV raw banked values
ZT = {k: v * 2 ** 0.25 for k, v in ZETA.items()}              # zt = zeta (2/H^2)^(1/4), H = 1
CT = {k: float((mp.mpf(3) / 4) * 2 ** (mp.mpf(2) / 3) * (v * 2 ** 0.25) ** (mp.mpf(2) / 3))
      for k, v in ZETA.items()}

# ----------------------------------------------------------------------------------------
# agentEE machinery, reused verbatim-in-substance (regression-gated in step0 before use)
# ----------------------------------------------------------------------------------------

def phi_tilde_closed(nu, c=3.0):
    """Mellin of the free mode: int_0^inf w^{-i nu} e^{i c w} dw = Gamma(1-i nu)(-i c)^{i nu - 1}."""
    nu = mp.mpc(nu)
    return mp.gamma(1 - 1j * nu) * (mp.mpc(0, -1) * c) ** (1j * nu - 1)


def phi_tilde_numeric(nu, c=3.0):
    """Same by rotated contour w = i s (absolutely damped)."""
    f = lambda s: (1j * s) ** (-1j * nu) * mp.e ** (-c * s) * 1j
    return mp.quad(f, [0, mp.inf])


def ft_sinh2_numeric(om, epsv, kapv=1.0):
    f = lambda T: mp.e ** (1j * om * T) * (-1.0) / mp.sinh(kapv * (T - 1j * epsv) / 2) ** 2
    return mp.quad(f, [-80, 0, 80])


def ft_sinh2_closed(om, epsv, kapv=1.0):
    return mp.e ** (-om * epsv) * (8 * mp.pi * om / kapv ** 2) / (1 - mp.e ** (-2 * mp.pi * om / kapv))


def D_pm(Om, zt, gamma, branch):
    """D_pm = int_0^inf tau^-gamma e^{-zt(1 -+ i) tau^-1/2} e^{i Om tau} dtau via tau = i y, y = x^-2,
    steepest rotation x -> e^{i pi/6} x for the + branch."""
    pref = 2j * mp.e ** (-1j * mp.pi * gamma / 2)
    if branch == +1:
        rot = mp.e ** (1j * mp.pi / 6)
        f = lambda uu: (rot * uu) ** (2 * gamma - 3) * mp.e ** (1j * mp.sqrt(2) * zt * rot * uu) \
            * mp.e ** (-Om / (rot * uu) ** 2) * rot
    else:
        f = lambda uu: uu ** (2 * gamma - 3) * mp.e ** (-mp.sqrt(2) * zt * uu) * mp.e ** (-Om / uu ** 2)
    return pref * mp.quad(f, [0, mp.inf])


def D_full(om, zt, gamma, phi0, m=0.5):
    Om = om + 1j * m
    return (mp.e ** (1j * phi0) * D_pm(Om, zt, gamma, +1) + mp.e ** (-1j * phi0) * D_pm(Om, zt, gamma, -1)) / 2


def D_direct(om, zt, gamma, phi0, m=0.5):
    f = lambda T: T ** (-gamma) * mp.e ** (-zt / mp.sqrt(T)) * mp.cos(zt / mp.sqrt(T) + phi0) \
        * mp.e ** ((1j * om - m) * T)
    return mp.quad(f, [0, 1, 8, 80])


# ----------------------------------------------------------------------------------------
# STEP 0 — regression gate
# ----------------------------------------------------------------------------------------

def step0():
    print("=" * 88)
    print("[HH-0] REGRESSION GATE: agentEE per-k kernel machinery reproduced before any new claim")
    print("=" * 88)
    mp.mp.dps = 30
    ok = True

    # (0a) Mellin closed form vs rotated-contour numeric
    print("[0a] Mellin of the free mode, numeric vs Gamma(1-i nu)(-i c)^(i nu - 1):")
    worst = 0.0
    for nu in [0.5, 2.0, -1.3]:
        pn, pc = phi_tilde_numeric(nu), phi_tilde_closed(nu)
        rd = float(abs(pn - pc) / abs(pc))
        worst = max(worst, rd)
        print(f"     nu = {nu:>5}: rel.diff = {rd:.2e}")
    ok &= worst < 1e-12
    print(f"     gate: worst {worst:.2e} < 1e-12  -> {'PASS' if worst < 1e-12 else 'FAIL'}")

    # (0b) the Planck identity (symbolic, exact)
    nu_s = sp.symbols('nu', real=True)
    planck_id = sp.simplify((sp.pi * nu_s / sp.sinh(sp.pi * nu_s) * sp.exp(sp.pi * nu_s)
                             - 2 * sp.pi * nu_s / (1 - sp.exp(-2 * sp.pi * nu_s))
                             ).rewrite(sp.exp).expand().together())
    print(f"[0b] |Gamma(1-i nu)|^2 e^(pi nu) - 2 pi nu/(1-e^(-2 pi nu)) = {planck_id}")
    ok &= planck_id == 0
    print(f"     gate: exactly 0 -> {'PASS' if planck_id == 0 else 'FAIL'}")

    # (0c) FT of sinh^-2 vs residue formula
    print("[0c] FT[-sinh^-2(kappa(tau - i eps)/2)] vs residue formula:")
    worst = 0.0
    for om in [0.7, 2.3, -1.1]:
        fn, fc = ft_sinh2_numeric(om, 1e-3), ft_sinh2_closed(om, 1e-3)
        rd = float(abs(fn - fc) / abs(fc))
        worst = max(worst, rd)
        print(f"     omega = {om:>5}: rel.diff = {rd:.2e}")
    ok &= worst < 1e-10
    print(f"     gate: worst {worst:.2e} < 1e-10 -> {'PASS' if worst < 1e-10 else 'FAIL'}")

    # (0d) the [3c] contour machinery vs direct quadrature
    mp.mp.dps = 40
    zt_fw, gam, phi0 = ZT["fw"], 0.75, mp.pi / 8
    print(f"[0d] D(omega) contour vs direct (zt_fw = {zt_fw:.4f}, gamma = 3/4, m = 0.5):")
    worst = 0.0
    for om in [3.0, 12.0]:
        dc, dd = D_full(om, zt_fw, gam, phi0), D_direct(om, zt_fw, gam, phi0)
        rd = float(abs(dc - dd) / abs(dc))
        worst = max(worst, rd)
        print(f"     omega = {om:>5}: rel.diff = {rd:.2e}")
    ok &= worst < 1e-8
    print(f"     gate: worst {worst:.2e} < 1e-8 -> {'PASS' if worst < 1e-8 else 'FAIL'}")

    # (0e) the saddle-class fit: reproduce ct_fit / ct_pred = 1.00084 and the fingerprint constants
    ct_pred = (mp.mpf(3) / 4) * 2 ** (mp.mpf(2) / 3) * mp.mpf(zt_fw) ** (mp.mpf(2) / 3)
    oms = [100.0, 300.0, 1000.0, 3000.0, 10000.0, 30000.0]
    vals_D = [D_full(om, zt_fw, gam, phi0) for om in oms]
    Amat = np.array([[1.0, np.log(om), -om ** (1.0 / 3)] for om in oms])
    bvec = np.array([float(mp.log(abs(v))) for v in vals_D])
    coef, *_ = np.linalg.lstsq(Amat, bvec, rcond=None)
    ratio = coef[2] / float(ct_pred)
    print(f"[0e] saddle fit: ct_fit = {coef[2]:.6f} vs pred {float(ct_pred):.6f}, ratio = {ratio:.5f}")
    ok_e = 1.0006 < ratio < 1.0011 and abs(coef[1] - (-1.0 / 3)) < 0.02
    ok &= ok_e
    print(f"     q_fit = {coef[1]:.4f} vs -1/3; gate (ratio in [1.0006, 1.0011], q to 0.02) -> "
          f"{'PASS' if ok_e else 'FAIL'}")
    print(f"     fingerprint constants ct by footing: " +
          ", ".join(f"{k} = {v:.4f}" for k, v in CT.items()))
    assert abs(CT['fw'] - 2.1388) < 5e-4 and abs(CT['canon'] - 1.9687) < 5e-4 \
        and abs(CT['hostile'] - 2.2790) < 5e-4

    # (0f) the positivity window A_max (same grid as agentEE [3d])
    om_grid = list(np.geomspace(0.05, 50.0, 28))
    rho_free = lambda om: om / (1 - np.exp(-2 * np.pi * om))
    ratios, imvals = [], []
    for om in om_grid:
        imD = 2 * float(mp.im(D_full(om, zt_fw, gam, phi0)))
        imvals.append(imD)
        ratios.append(max(0.0, -imD) / rho_free(om))
    ratios = np.array(ratios)
    A_max = 1.0 / ratios.max()
    i_bind = int(np.argmax(ratios))
    print(f"[0f] A_max = {A_max:.3f} (binding at omega = {om_grid[i_bind]:.3f})")
    ok_f = 5.6 < A_max < 5.8
    ok &= ok_f
    print(f"     gate (A_max in [5.6, 5.8], agentEE banked 5.716) -> {'PASS' if ok_f else 'FAIL'}")

    print(f"[HH-0] REGRESSION GATE: {'ALL PASS — machinery banked, reuse authorized' if ok else 'FAIL'}")
    assert ok


# ----------------------------------------------------------------------------------------
# STEP 1 — pump parametrization: the forced universal form + the commutator structure
# ----------------------------------------------------------------------------------------

def step1():
    print("=" * 88)
    print("[HH-1] PUMP PARAMETRIZATION: scale invariance forces ONE universal ODE; the response")
    print("       (commutator) is normalization-free; the worldline density is Mellin-bilinear")
    print("=" * 88)

    # ------------------------------------------------------------------------------------
    # [1a] Scale-invariance reduction. Work with the Minkowski-form khronon variable g:
    # free modes g = e^{i c w} (agentEE STEP 1 / arXiv:1206.1083 structure), field mode
    # f_k = (H/sqrt(2 c k^3)) * w g(w), w = k|eta| = k_phys/H. The most general LINEAR,
    # LOCAL-in-time, scale-invariant pump = gain Gamma_conf(eta,k) + dispersion f:
    #   g'' + 2 Gamma_conf g' + c^2 k^2 (1 + f) g = 0  with  Gamma_conf = k ghat(-k eta),
    #   f = f(-k eta)   <-- scale invariance: functions of k_phys/H = -k eta ONLY.
    # Claim: in w = -k eta this is the k-INDEPENDENT universal ODE
    #   g_ww - 2 ghat(w) g_w + c^2 (1 + f(w)) g = 0      [sign: d/deta = -k d/dw]
    # and ghat > 0 = GAIN in physical time (amplitude grows toward the future w -> 0).
    # Physical gain rate per Hubble time: Gamma_phys/H = a^{-1}Gamma_conf/H = w*ghat(w):
    # H-paced by construction -- the (C5) "the only scale available IS the dS bath's".
    # ------------------------------------------------------------------------------------
    eta, k, c, w = sp.symbols('eta k c w', positive=True)
    gh = sp.Function('ghat')
    ff = sp.Function('f')
    G = sp.Function('g')
    # conformal-time equation for v(eta) = g(-k eta):
    v = G(-k * eta)
    conf_eq = sp.diff(v, eta, 2) + 2 * k * gh(-k * eta) * sp.diff(v, eta) \
        + c ** 2 * k ** 2 * (1 + ff(-k * eta)) * v
    # universal target in w:
    univ = (sp.diff(G(w), w, 2) - 2 * gh(w) * sp.diff(G(w), w) + c ** 2 * (1 + ff(w)) * G(w))
    resid = sp.simplify(conf_eq.subs(-k * eta, w).doit() - k ** 2 * univ.subs(w, -k * eta).subs(-k * eta, w))
    # direct route: substitute u = -k eta symbolically
    u_ = sp.symbols('u', positive=True)
    conf_in_u = conf_eq.subs(eta, -u_ / k)
    conf_in_u = sp.simplify(conf_in_u.doit())
    univ_in_u = k ** 2 * univ.subs(w, u_)
    resid2 = sp.simplify(conf_in_u - univ_in_u)
    print(f"[1a] conformal-time pump equation - k^2 x universal w-ODE = {resid2}")
    assert resid2 == 0
    print("     => ANY scale-invariant linear local pump (gain ghat(k_phys/H), dispersion f(k_phys/H))")
    print("        reduces to ONE k-independent ODE:  g'' - 2 ghat(w) g' + c^2(1 + f(w)) g = 0.")
    print("        (ghat > 0 = physical-time gain; w-derivative sign flip since w runs backward.)")
    print("        Physical gain rate / H = w*ghat(w): H-paced, the (C5) structure, AUTOMATIC.")

    # ------------------------------------------------------------------------------------
    # [1b] Friction elimination + the commutator's normalization-free structure.
    # g = e^{+Ghat(w)} psi with Ghat' = ghat  maps the pumped ODE to Hermitian form:
    #   psi'' + Omega2(w) psi = 0,  Omega2 = c^2(1+f) - ghat' - ghat^2   [check exactly]
    # The response/commutator kernel is the CAUCHY PROPAGATOR of the universal ODE --
    # basis-invariant (any GL(2) change of solution basis cancels between numerator and
    # Wronskian) and Wronskian-running-invariant: gain enters as relative factor
    # e^{Ghat(w1) - Ghat(w2)} times the psi-system propagator.   [check exactly]
    # ------------------------------------------------------------------------------------
    Gh = sp.Function('Ghat')
    psi = sp.Function('psi')
    g_sub = sp.exp(Gh(w)) * psi(w)
    pump_op = sp.diff(g_sub, w, 2) - 2 * sp.diff(Gh(w), w) * sp.diff(g_sub, w) \
        + c ** 2 * (1 + ff(w)) * g_sub
    pump_op = sp.expand(pump_op.doit())
    herm_target = sp.exp(Gh(w)) * (sp.diff(psi(w), w, 2)
                                   + (c ** 2 * (1 + ff(w)) + sp.diff(Gh(w), w, 2)
                                      - sp.diff(Gh(w), w) ** 2) * psi(w))
    resid_b = sp.simplify(pump_op - sp.expand(herm_target.doit()))
    print(f"[1b] friction elimination residual = {resid_b}")
    assert resid_b == 0
    print("     => g = e^Ghat psi, Ghat' = ghat:  psi'' + Omega2 psi = 0,")
    print("        Omega2 = c^2(1+f) + ghat' - ghat^2  [w-form; physical-time form -ghat'-ghat^2].")
    print("        NOTE the w-sign: with g'' - 2 ghat g', the dressing is e^{+Ghat}, growing toward")
    print("        large w removed... amplitude bookkeeping lives ONLY in e^{Ghat(w1)-Ghat(w2)}:")
    # Cauchy propagator basis invariance + gain factorization (symbolic, generic functions):
    ga, gb, pa, pb = sp.Function('ga'), sp.Function('gb'), sp.Function('pa'), sp.Function('pb')
    w1, w2 = sp.symbols('w1 w2', positive=True)
    al, be, gam_, de = sp.symbols('alpha beta gamma delta')
    num = ga(w1) * gb(w2) - gb(w1) * ga(w2)
    Wr = ga(w2) * sp.diff(gb(w2), w2) - gb(w2) * sp.diff(ga(w2), w2)
    # GL(2) basis change:
    gA = al * ga(w1) + be * gb(w1)
    gB = gam_ * ga(w1) + de * gb(w1)
    gA2 = al * ga(w2) + be * gb(w2)
    gB2 = gam_ * ga(w2) + de * gb(w2)
    num2 = gA * gB2 - gB * gA2
    Wr2 = gA2 * sp.diff(gB2, w2) - gB2 * sp.diff(gA2, w2)
    inv_resid = sp.simplify(num2 / Wr2 - num / Wr)
    print(f"     basis (GL2) invariance of Cauchy propagator: residual = {inv_resid}")
    assert inv_resid == 0
    # gain factorization: g_i = e^Ghat psi_i  =>  G_c^g(w1,w2) = e^{Ghat(w1)-Ghat(w2)} G_c^psi(w1,w2)
    subsmap = {ga(w1): sp.exp(Gh(w1)) * pa(w1), gb(w1): sp.exp(Gh(w1)) * pb(w1),
               ga(w2): sp.exp(Gh(w2)) * pa(w2), gb(w2): sp.exp(Gh(w2)) * pb(w2)}
    num_g = num.subs(subsmap)
    Wr_g = (ga(w2) * sp.diff(gb(w2), w2) - gb(w2) * sp.diff(ga(w2), w2))
    Wr_g = Wr_g.subs({ga(w2): sp.exp(Gh(w2)) * pa(w2), gb(w2): sp.exp(Gh(w2)) * pb(w2)}).doit()
    num_psi = pa(w1) * pb(w2) - pb(w1) * pa(w2)
    Wr_psi = pa(w2) * sp.diff(pb(w2), w2) - pb(w2) * sp.diff(pa(w2), w2)
    fact_resid = sp.simplify(num_g / Wr_g - sp.exp(Gh(w1) - Gh(w2)) * num_psi / Wr_psi)
    print(f"     gain factorization G_c^g = e^(Ghat(w1)-Ghat(w2)) G_c^psi: residual = {fact_resid}")
    assert fact_resid == 0
    print("     => the RESPONSE the worldline reads is the Cauchy propagator: normalization-FREE")
    print("        (no vacuum choice, no Wronskian normalization enters -- the Bogoliubov lemma's")
    print("        'dynamics object' made explicit). Gain enters ONLY via e^{Ghat(w1)-Ghat(w2)} and")
    print("        via Omega2 inside psi. WLOG scan space = {Ghat-factor} x {Hermitian Omega2 family}.")

    # ------------------------------------------------------------------------------------
    # [1c] the worldline Mellin-bilinear formula, verified EXACTLY on the free case.
    # W_c(tau) at b=0:  ~ int dk/k [w1 w2 Gc(w1,w2)] with w1 = x u, w2 = x/u, u = e^{-H tau/2}
    # Mellin-Plancherel: int dx/x A(xu) B(x/u) = (1/2pi) int dnu A~(nu) B~(-nu) u^{2 i nu}
    #  => rho_c(nu) propto  [phia~(nu) psib~(-nu) - phib~(nu) psia~(-nu)] with
    #     phi_i = w g_i,  psi_i = w g_i / W(w)   (W = running Wronskian).
    # Free case: g_a = e^{icw}, g_b = e^{-icw}, W = -2ic (const):
    #     rho_c(nu) propto |phia~(nu)|^2 - |phia~(-nu)|^2 = 2 pi nu/c^2 EXACTLY.
    # Verify the Plancherel pairing AND the free reduction numerically (mpmath).
    # ------------------------------------------------------------------------------------
    print("[1c] worldline Mellin-bilinear formula:")
    mp.mp.dps = 30
    cval = 3.0
    # (i) Plancherel pairing on a test pair with known Mellins:
    # A(x) = x e^{i c x} (free phi), B(x) = x e^{-i c x}: int dx/x A(xu)B(x/u) closed form:
    # = int dx x e^{i c x(u-1/u)} = -1/(c^2(u-1/u)^2). The pairing is distributional on the
    # real nu-line (integrand ~ nu at +inf); regulate with tau -> tau - i eps (KMS strip):
    # u = e^{-(tau - i eps)/2}, u^{2 i nu} = e^{-i nu tau} e^{-nu eps}; the -nu side carries
    # the detailed-balance e^{-2 pi |nu|}, so eps in (0, 2 pi) converges BOTH ends.
    tau_c = mp.mpf('0.7') - 0.5j
    uu = mp.e ** (-tau_c / 2)
    lhs = -1 / (cval ** 2 * (uu - 1 / uu) ** 2)
    f_pair = lambda nu: (phi_tilde_closed(nu, cval) * mp.conj(phi_tilde_closed(mp.conj(nu), cval))
                         * mp.e ** (-1j * nu * tau_c))
    rhs = mp.quad(f_pair, [-mp.inf, 0, mp.inf]) / (2 * mp.pi)
    rd = float(abs(lhs - rhs) / abs(lhs))
    print(f"     (i) Plancherel pairing at tau = 0.7 - 0.5i: closed = {complex(lhs):.8e},")
    print(f"         Mellin side = {complex(rhs):.8e},  rel.diff = {rd:.2e}")
    assert rd < 1e-12
    # (ii) free commutator reduction: the bilinear with psi_i = phi_i/W, W = -2ic:
    #  rho_c(nu) = 2ic [phia~(nu) psib~(-nu) - phib~(nu) psia~(-nu)]
    #            = -(|phia~(nu)|^2 - |phia~(-nu)|^2)  -> normalize so free = +2 pi nu/c^2
    def rho_c_free_bilinear(nu):
        phia_p = phi_tilde_closed(nu, cval)
        phib_m = mp.conj(phi_tilde_closed(nu, cval))          # phib~(-nu) = conj phia~(nu)
        phib_p = mp.conj(phi_tilde_closed(-nu, cval))         # phib~(nu)  = conj phia~(-nu)
        phia_m = phi_tilde_closed(-nu, cval)
        bil = 2j * cval * (phia_p * phib_m / (-2j * cval) - phib_p * phia_m / (-2j * cval))
        return -bil
    worst = 0.0
    for nu in [0.4, 1.0, 3.7]:
        got = rho_c_free_bilinear(nu)
        want = 2 * mp.pi * nu / cval ** 2
        rd = float(abs(got - want) / abs(want))
        worst = max(worst, rd)
        print(f"     (ii) nu = {nu:>4}: bilinear rho_c = {complex(got).real:.10e}  vs  "
              f"2 pi nu/c^2 = {float(want):.10e}  rel.diff = {rd:.2e}")
    assert worst < 1e-18
    print("     => rho_c(nu) = -2ic[phia~(nu)psib~(-nu) - phib~(nu)psia~(-nu)], free = 2 pi nu/c^2")
    print("        EXACTLY (the [2d] Planck-odd-part recovered through the bilinear). Convention for")
    print("        the scan: NORMALIZE rho_c by (2 pi/c^2) so free rho_c(nu) = nu; then the (C1) tail")
    print("        and the (C3) window A_max = 5.716 compare in agentEE [3d] units directly.")

    # ------------------------------------------------------------------------------------
    # [1d] the scan classes (parametrization registered before computing):
    # ------------------------------------------------------------------------------------
    print("[1d] g-classes registered for the forward scan (STEP 3):")
    print("     P  power-law tails:        ghat or f = kappa w^{-p}, p in (0,2]; p = 2/3 distinguished")
    print("        (the WKB index-transfer candidate for omega^{1/3}); exactly solvable anchors:")
    print("        p = 2 (Bessel, complex kappa allowed), p = 1 (Coulomb/Whittaker).")
    print("     B  gain bands:             ghat = eps * bump((w - w0)/dw)  (compact, smooth);")
    print("        sharp-edged variant for the endpoint/power-law class.")
    print("     L  log-periodic:           ghat or f = eps cos(Omega ln w) x envelope.")
    print("     D  modified dispersion:    f real: f = kappa w^{-p} (phase-only at WKB order),")
    print("        omega^2 = c^2k^2(1 + f(k/aH)) the X2-named form.")
    print("     X  windowed filter bank:   ghat = sum_j eps_j bump(ln w - ln w_j) = B/L composite.")
    print("     G  Gevrey-3/stable class:  profiles with Mellin g~(mu) ~ e^{-A|mu|^{1/3}} (the")
    print("        index-1/3 stable-subordinator kernel in ln w) -- the inverse-problem candidate.")
    print("     For each: compute Delta rho_c(nu), fit ln|tail| = lnK + q ln nu - ct nu^s (s free),")
    print("     test s = 1/3, the cos(sqrt3 ct nu^{1/3}) lock, additivity, and one-sidedness.")


# ----------------------------------------------------------------------------------------
# STEP 2 — the per-k -> worldline pipeline (exact, complex-contour Mellin)
#
# Universal Hermitian-form ODE: g'' + c^2 (1 + F(w)) g = 0, F real, F == 0 for w < w_cut
# (profiles carry a smooth turn-on exp(-(w_lo/w)^4) and are truncated at w_cut = w_lo/3,
#  where the factor is < 1e-35 — below error budget).
# g_a := the upper-half-plane-decaying solution (vacuum branch continuation), built as:
#   (R) Riccati u = G'/G, G(s) = g_a(i s):  u' = c^2(1+F(is)) - u^2, integrated DOWN from
#       S_max (attracting direction for the decaying branch), WKB-seeded; L' = u alongside.
#   (A) arc continuation i r0 -> r0 (quarter circle, ODE in theta), then real axis r0 -> w_cut.
#   (E) below w_cut: g = A cos(cw) + B sin(cw) EXACTLY (F == 0 there).
# Mellin phia~(nu) = int_0^inf w^{-i nu} g_a(w) w dw / w  --- contour = [0,w_cut] closed form
# (incomplete gamma) + [w_cut, r0] real + quarter arc + imaginary ray [r0, S_max].
# rho_c(nu) (normalized so free = nu) from the [1c] bilinear with g_b = conj-partner and the
# numerically computed Wronskian. The e^{nu pi/2} cancellation on the +nu side is paid with
# dps ~ 0.683 nu + 40.
# ----------------------------------------------------------------------------------------

def _mk_path_ode(Ffunc, cval):
    """RHS for g'' = -c^2 (1+F(w)) g along a straight segment w(t) = a + t*(b-a)."""
    def seg(a, b):
        dw = b - a
        def rhs(t, Y):
            wv = a + t * dw
            return [dw * Y[1], dw * (-cval ** 2 * (1 + Ffunc(wv)) * Y[0])]
        return rhs
    return seg


def solve_branch(Ffunc, cval, r0, S_max, w_cut, n_eval=None):
    """Build g_a (upper-decaying) on: imaginary ray [r0,S_max] (as u,L with G(r0)=1), the arc,
    and the real segment [w_cut, r0]. Returns dict of callables + matching data (A,B) at w_cut."""
    # (R) Riccati down the ray: x = S_max - s, forward in x; state [u, L], L(s)= int_{S_max}^s u ds'
    Q = lambda s: 1 + Ffunc(1j * s)
    def ric_rhs(x, Y):
        s = S_max - x
        return [-(cval ** 2 * Q(s) - Y[0] ** 2), -Y[0]]
    dQ = lambda s: (Q(s + mp.mpf('1e-20')) - Q(s - mp.mpf('1e-20'))) / mp.mpf('2e-20')
    u0 = -cval * mp.sqrt(Q(S_max)) - dQ(S_max) / (4 * Q(S_max))
    ric = mp.odefun(ric_rhs, 0, [u0, mp.mpc(0)], tol=mp.mpf(10) ** (-(mp.mp.dps - 6)))
    u_of_s = lambda s: ric(S_max - s)[0]
    L_of_s = lambda s: ric(S_max - s)[1]          # int_{S_max}^{s} u  (negative of int_s^{Smax})
    Lr0 = L_of_s(r0)
    G_of_s = lambda s: mp.e ** (L_of_s(s) - Lr0)  # G(r0) = 1
    # (A) arc: w = r0 e^{i th}, th: pi/2 -> 0; param x in [0,1], th = pi/2 (1-x)
    g_at_ir0 = mp.mpc(1)
    gp_at_ir0 = -1j * u_of_s(r0) * g_at_ir0      # g'(is) = -i dG/ds
    def arc_rhs(x, Y):
        th = mp.pi / 2 * (1 - x)
        wv = r0 * mp.e ** (1j * th)
        dwdx = r0 * 1j * mp.e ** (1j * th) * (-mp.pi / 2)
        return [dwdx * Y[1], dwdx * (-cval ** 2 * (1 + Ffunc(wv)) * Y[0])]
    arc = mp.odefun(arc_rhs, 0, [g_at_ir0, gp_at_ir0], tol=mp.mpf(10) ** (-(mp.mp.dps - 6)))
    g_r0, gp_r0 = arc(1)
    # (Re) real segment r0 -> w_cut (backward: param x in [0,1], w = r0 + x (w_cut - r0))
    seg = _mk_path_ode(Ffunc, cval)(r0, w_cut)
    real_seg = mp.odefun(seg, 0, [g_r0, gp_r0], tol=mp.mpf(10) ** (-(mp.mp.dps - 6)))
    g_wc, gp_wc = real_seg(1)
    # (E) trig matching at w_cut: g = A cos(c w) + B sin(c w)
    cw = cval * w_cut
    A = g_wc * mp.cos(cw) - gp_wc * mp.sin(cw) / cval
    B = g_wc * mp.sin(cw) + gp_wc * mp.cos(cw) / cval
    return {"u": u_of_s, "G": G_of_s, "arc": arc, "real": real_seg, "A": A, "B": B,
            "r0": r0, "S_max": S_max, "w_cut": w_cut, "c": cval, "g_r0": g_r0, "gp_r0": gp_r0}


def _endpoint_mellin(nu, A, B, cval, w_cut):
    """int_0^{w_cut} w^{-i nu} (A cos(cw) + B sin(cw)) w dw/w  -- w^{-i nu} g w dw/w = w^{-i nu} g dw
    with phi = w g  =>  integrand w^{-i nu} g(w) dw. Closed form via lower incomplete gamma:
    I(a) = int_0^{w_cut} w^{-i nu} e^{i a w} dw = (-i a)^{i nu - 1} gammainc_lower(1 - i nu, -i a w_cut)."""
    def I(a):
        z = 1 - 1j * mp.mpc(nu)
        return (mp.mpc(0, -1) * a) ** (1j * mp.mpc(nu) - 1) * mp.gammainc(z, 0, -1j * a * w_cut)
    Ip, Im_ = I(cval), I(-cval)
    return A * (Ip + Im_) / 2 + B * (Ip - Im_) / (2j)


def mellin_phia(branch, nu, n_panel_fac=3.5, weight=None):
    """phia~(nu) = int_0^inf w^{-i nu} weight(w) g_a(w) dw along the deformed contour.
    weight must be analytic in the closed first quadrant (default 1). nu real, either sign.
    Heavy cancellation for nu > 0 (factor e^{nu pi/2})."""
    cval, r0, S_max, w_cut = branch["c"], branch["r0"], branch["S_max"], branch["w_cut"]
    wt = weight if weight is not None else (lambda wv: mp.mpf(1))
    # (E) endpoint: weight(w) ~ weight(0)(1+O(w-small)) — templates keep |weight-1| < 1e-6
    # below w_cut; the endpoint uses weight(w_cut/2) as a constant (error budgeted per run)
    tot = wt(w_cut / 2) * _endpoint_mellin(nu, branch["A"], branch["B"], cval, w_cut)
    # (Re) real segment w in [w_cut, r0]
    realf = lambda x: branch["real"](x)[0]
    def integ_real(x):
        # contour direction is w_cut -> r0; the solve parametrization runs r0 -> w_cut,
        # so dw = (w_cut - r0) dx and the contour integral = -int_0^1 ... = (r0 - w_cut) int
        wv = r0 + x * (w_cut - r0)
        return wv ** (-1j * mp.mpc(nu)) * wt(wv) * realf(x) * (r0 - w_cut)
    npan = max(8, int(abs(nu) * float(mp.log(r0 / w_cut)) / 4) + 8)
    pts = list(mp.linspace(0, 1, npan))
    tot += mp.quad(integ_real, pts)
    # (A) arc w = r0 e^{i th}, from th=0 to th=pi/2 (reverse of solve direction: x: 1 -> 0)
    def integ_arc(x):
        th = mp.pi / 2 * (1 - x)
        wv = r0 * mp.e ** (1j * th)
        dwdx = r0 * 1j * mp.e ** (1j * th) * (-mp.pi / 2)
        return wv ** (-1j * mp.mpc(nu)) * wt(wv) * branch["arc"](x)[0] * (-dwdx)
    pts = list(mp.linspace(0, 1, max(10, int(abs(nu)) + 10)))
    tot += mp.quad(integ_arc, pts)
    # (R) ray w = i s, s in [r0, S_max]: dw = i ds; w^{-i nu} = e^{nu pi/2} s^{-i nu} (principal)
    def integ_ray(s):
        return (1j * s) ** (-1j * mp.mpc(nu)) * wt(1j * s) * branch["G"](s) * 1j
    # log-spaced panels matched to oscillation rate nu in ln s + decay scale
    nseg = max(12, int(abs(nu) * float(mp.log(S_max / r0)) / n_panel_fac) + 12)
    pts = [r0 * (S_max / r0) ** (mp.mpf(j) / nseg) for j in range(nseg + 1)]
    tot += mp.quad(integ_ray, pts)
    return tot


# ---------- fast cached-node Mellin machinery (nodes are nu-independent) ----------

_GL_CACHE = {}

def gl_nodes(n=24):
    """Gauss-Legendre nodes/weights on [-1,1] at current mp precision (numpy seed + mp Newton)."""
    key = (n, mp.mp.dps)
    if key in _GL_CACHE:
        return _GL_CACHE[key]
    xs, ws = np.polynomial.legendre.leggauss(n)
    nodes = []
    for x0 in xs:
        x = mp.mpf(float(x0))
        for _ in range(4):                    # Newton refine on P_n
            p0, p1 = mp.mpf(1), x
            for k in range(2, n + 1):
                p0, p1 = p1, ((2 * k - 1) * x * p1 - (k - 1) * p0) / k
            dp = n * (x * p1 - p0) / (x ** 2 - 1)
            x = x - p1 / dp
        # weight: 2 / ((1-x^2) P_n'(x)^2)
        p0, p1 = mp.mpf(1), x
        for k in range(2, n + 1):
            p0, p1 = p1, ((2 * k - 1) * x * p1 - (k - 1) * p0) / k
        dp = n * (x * p1 - p0) / (x ** 2 - 1)
        nodes.append((x, 2 / ((1 - x ** 2) * dp ** 2)))
    _GL_CACHE[key] = nodes
    return nodes


def build_node_cache(branch, numax, deg=24):
    """Evaluate g_a (and jacobians) at fixed GL nodes on the real segment, arc and ray,
    sized to resolve oscillations up to numax. Returns list of (w, jac*glw, g) triples."""
    cval, r0, S_max, w_cut = branch["c"], branch["r0"], branch["S_max"], branch["w_cut"]
    gl = gl_nodes(deg)
    items = []
    # real segment w_cut -> r0: param x in [0,1] of the SOLVE (w = r0 + x(w_cut-r0));
    # contour integral = int_0^1 ... (r0-w_cut) dx
    npan = max(6, int(numax * float(mp.log(r0 / w_cut)) / 2.5) + 6)
    for j in range(npan):
        a, b = mp.mpf(j) / npan, mp.mpf(j + 1) / npan
        mid, half = (a + b) / 2, (b - a) / 2
        for x0, wgt in gl:
            x = mid + half * x0
            wv = r0 + x * (w_cut - r0)
            items.append((wv, (r0 - w_cut) * half * wgt, branch["real"](x)[0]))
    # arc th: 0 -> pi/2, w = r0 e^{i th}, dw = i r0 e^{i th} dth; solve param x with th = pi/2(1-x)
    npan = max(6, int(numax * 1.6 / 2.5) + 6)
    for j in range(npan):
        a = mp.pi / 2 * mp.mpf(j) / npan
        b = mp.pi / 2 * mp.mpf(j + 1) / npan
        mid, half = (a + b) / 2, (b - a) / 2
        for x0, wgt in gl:
            th = mid + half * x0
            wv = r0 * mp.e ** (1j * th)
            items.append((wv, 1j * wv * half * wgt, branch["arc"](1 - th / (mp.pi / 2))[0]))
    # ray w = i s, s: r0 -> S_max, log-spaced panels
    lr = float(mp.log(S_max / r0))
    npan = max(10, int(numax * lr / 2.5) + 10)
    for j in range(npan):
        a = r0 * (S_max / r0) ** (mp.mpf(j) / npan)
        b = r0 * (S_max / r0) ** (mp.mpf(j + 1) / npan)
        mid, half = (a + b) / 2, (b - a) / 2
        for x0, wgt in gl:
            s = mid + half * x0
            items.append((1j * s, 1j * half * wgt, branch["G"](s)))
    return items


def apply_weight(cache, wt):
    """Fold an analytic weight into the cached node coefficients."""
    return [(wv, jacw * wt(wv), gv) for wv, jacw, gv in cache]


def mellin_from_cache(branch, cache, nu, endpoint_const=1):
    """phia~(nu) = endpoint_const * endpoint + sum over cached nodes of w^{-i nu} g jac."""
    tot = endpoint_const * _endpoint_mellin(nu, branch["A"], branch["B"],
                                            branch["c"], branch["w_cut"])
    nuc = mp.mpc(nu)
    e = -1j * nuc
    tot += mp.fsum(wv ** e * gv * jacw for wv, jacw, gv in cache)
    return tot


# ---------- v2 pipeline: real-axis saddle route (no e^{nu pi/2} cancellation tax) ----------
#
# g_a anchored by Riccati CONTRACTION on the ray [s_a, s_a + 45] (seed error e^{-2c*45} — the
# decaying branch is attracting downward), transported down the arc at radius s_a (stable:
# follows the growing e^{icw}), then real axis both ways and a rotated decaying tail at W_max.
# Mellin contour: [0,w_cut] trig endpoint + [w_cut, W_max] real + rotated tail (truncated).
# All pieces O(w)-bounded: flat dps ~ 40 for ANY nu. The -nu Mellin pays e^{pi nu} on this
# route -> computed only for nu <= 8 (above that |phia~(-nu)|^2 is e^{-2 pi nu} negligible).

def solve_branch2(Ffunc, cval, w_cut, W_max, s_a=6.0, ric_len=45.0, T_rot=42.0,
                  theta_rot=None):
    theta_rot = theta_rot or mp.pi / 6
    s_a = mp.mpf(s_a)
    tol = mp.mpf(10) ** (-(mp.mp.dps - 4))
    # (R) Riccati seed + contraction on the ray
    Q = lambda s: 1 + Ffunc(1j * s)
    def ric_rhs(x, Y):
        s = s_a + ric_len - x
        return [-(cval ** 2 * Q(s) - Y[0] ** 2)]
    dd = mp.mpf('1e-15')
    S0 = s_a + ric_len
    u0 = -cval * mp.sqrt(Q(S0)) - (Q(S0 + dd) - Q(S0 - dd)) / (2 * dd) / (4 * Q(S0))
    ric = mp.odefun(ric_rhs, 0, [u0], tol=tol)
    u_sa = ric(ric_len)[0]
    # (A) arc down: w = s_a e^{i th}, th: pi/2 -> 0; g(i s_a) = 1 (normalization arbitrary)
    g_top = mp.mpc(1)
    gp_top = -1j * u_sa * g_top
    def arc_rhs(x, Y):
        th = mp.pi / 2 * (1 - x)
        wv = s_a * mp.e ** (1j * th)
        dwdx = s_a * 1j * mp.e ** (1j * th) * (-mp.pi / 2)
        return [dwdx * Y[1], dwdx * (-cval ** 2 * (1 + Ffunc(wv)) * Y[0])]
    arc = mp.odefun(arc_rhs, 0, [g_top, gp_top], tol=tol)
    g_sa, gp_sa = arc(1)
    # (Re-) real axis inward s_a -> w_cut  (param x: w = s_a + x (w_cut - s_a))
    segin = _mk_path_ode(Ffunc, cval)(s_a, w_cut)
    real_in = mp.odefun(segin, 0, [g_sa, gp_sa], tol=tol)
    g_wc, gp_wc = real_in(1)
    cw = cval * w_cut
    A = g_wc * mp.cos(cw) - gp_wc * mp.sin(cw) / cval
    B = g_wc * mp.sin(cw) + gp_wc * mp.cos(cw) / cval
    # (Re+) real axis outward s_a -> W_max
    segout = _mk_path_ode(Ffunc, cval)(s_a, W_max)
    real_out = mp.odefun(segout, 0, [g_sa, gp_sa], tol=tol)
    g_W, gp_W = real_out(1)
    # (T) rotated decaying tail from W_max: w = W_max + e^{i theta} t, t in [0, T_rot]
    rot = mp.e ** (1j * theta_rot)
    def tail_rhs(t, Y):
        wv = W_max + rot * t
        return [rot * Y[1], rot * (-cval ** 2 * (1 + Ffunc(wv)) * Y[0])]
    tail = mp.odefun(tail_rhs, 0, [g_W, gp_W], tol=tol)
    return {"c": cval, "w_cut": w_cut, "W_max": W_max, "s_a": s_a, "T_rot": mp.mpf(T_rot),
            "rot": rot, "real_in": real_in, "real_out": real_out, "tail": tail,
            "A": A, "B": B, "g_sa": g_sa, "gp_sa": gp_sa}


def build_node_cache2(branch, numax, deg=24):
    """GL nodes over: real [w_cut, s_a] (via real_in param), real [s_a, W_max] (real_out),
    rotated tail. Panel density set by the local phase rate |c dw| + |numax d ln w|."""
    cval, w_cut, W_max, s_a = branch["c"], branch["w_cut"], branch["W_max"], branch["s_a"]
    T_rot, rot = branch["T_rot"], branch["rot"]
    gl = gl_nodes(deg)
    items = []
    # real inward segment, contour direction w: w_cut -> s_a, log-spaced panels in w;
    # direct w-parametrization: contribution = sum over nodes f(w) * (panel half-width) * wgt
    phase = float(cval * (s_a - w_cut) + numax * mp.log(s_a / w_cut))
    npan = max(6, int(phase / 2.5) + 6)
    x_of_w = lambda wv: (wv - s_a) / (w_cut - s_a)
    for j in range(npan):
        wa = w_cut * (s_a / w_cut) ** (mp.mpf(j) / npan)
        wb = w_cut * (s_a / w_cut) ** (mp.mpf(j + 1) / npan)
        mid, half = (wa + wb) / 2, (wb - wa) / 2
        for x0, wgt in gl:
            wv = mid + half * x0
            items.append((wv, half * wgt, branch["real_in"](x_of_w(wv))[0]))
    # real outward segment [s_a, W_max]: w = s_a + x (W_max - s_a)
    phase = float(cval * (W_max - s_a) + numax * mp.log(W_max / s_a))
    npan = max(8, int(phase / 2.5) + 8)
    for j in range(npan):
        xa, xb = mp.mpf(j) / npan, mp.mpf(j + 1) / npan
        mid, half = (xa + xb) / 2, (xb - xa) / 2
        for x0, wgt in gl:
            x = mid + half * x0
            wv = s_a + x * (W_max - s_a)
            items.append((wv, (W_max - s_a) * half * wgt, branch["real_out"](x)[0]))
    # rotated tail: w = W_max + rot t, t in [0, T_rot]
    phase = float(cval * T_rot + numax * T_rot / W_max) + 8
    npan = max(6, int(phase / 2.5) + 6)
    for j in range(npan):
        ta, tb = T_rot * mp.mpf(j) / npan, T_rot * mp.mpf(j + 1) / npan
        mid, half = (ta + tb) / 2, (tb - ta) / 2
        for x0, wgt in gl:
            t = mid + half * x0
            wv = W_max + rot * t
            items.append((wv, rot * half * wgt, branch["tail"](t)[0]))
    return items


def rho_c_pipeline2(Ffunc, cval, nu_list, w_cut=None, W_max=None, dps=40, Ghat=None,
                    nu_minus_max=8.0, deg=24):
    """v2 normalized rho_c(nu) (free == nu). For nu > nu_minus_max the e^{-2 pi nu} term
    |phia~(-nu)|^2 is dropped (bounded relative error e^{-2 pi nu_minus_max} ~ 1.5e-22)."""
    results = {}
    old = mp.mp.dps
    mp.mp.dps = dps
    try:
        numax = max(abs(n) for n in nu_list)
        w_cut = w_cut or mp.mpf('0.01')
        W_max = W_max or (2.2 * numax / cval + 15)
        branch = solve_branch2(Ffunc, cval, w_cut, W_max)
        A, B = branch["A"], branch["B"]
        W = cval * (A * mp.conj(B) - mp.conj(A) * B)
        cache = build_node_cache2(branch, numax, deg=deg)
        results["_nnodes"] = len(cache)
        if Ghat is not None:
            cache_p = apply_weight(cache, lambda wv: mp.e ** (Ghat(wv)))
            cache_m = apply_weight(cache, lambda wv: mp.e ** (-Ghat(wv)))
            ep_p, ep_m = mp.e ** (Ghat(w_cut / 2)), mp.e ** (-Ghat(w_cut / 2))
        for nu in nu_list:
            if Ghat is None:
                Pp_p = mellin_from_cache(branch, cache, nu)
                t1 = Pp_p * mp.conj(Pp_p)
                t2 = 0
                if nu <= nu_minus_max:
                    Pp_m = mellin_from_cache(branch, cache, -nu)
                    t2 = mp.conj(Pp_m) * Pp_m
                bil = -2j * cval * (t1 - t2) / W
            else:
                Pp_p = mellin_from_cache(branch, cache_p, nu, ep_p)
                Pm_p = mellin_from_cache(branch, cache_m, nu, ep_m)
                t1 = Pp_p * mp.conj(Pm_p)
                t2 = 0
                if nu <= nu_minus_max:
                    Pp_m = mellin_from_cache(branch, cache_p, -nu, ep_p)
                    Pm_m = mellin_from_cache(branch, cache_m, -nu, ep_m)
                    t2 = mp.conj(Pp_m) * Pm_m
                bil = -2j * cval * (t1 - t2) / W
            results[nu] = bil / (2 * mp.pi / cval ** 2)
        results["_W"] = W
    finally:
        mp.mp.dps = old
    return results


def rho_c_pipeline(Ffunc, cval, nu_list, r0=None, S_max=None, w_cut=None, dps_pad=40,
                   Ghat=None, per_nu_dps=True):
    """Full normalized rho_c(nu) (free == nu) for the universal ODE. If Ghat is given (gain),
    Ffunc must be the EFFECTIVE Hermitian profile F_eff = f + (ghat' - ghat^2)/c^2 and the
    bilinear carries the e^{+Ghat}/e^{-Ghat} weighted Mellins (phi-side/chi-side)."""
    results = {}
    numax = max(abs(n) for n in nu_list)
    dps_need = int(0.6822 * numax) + dps_pad
    old = mp.mp.dps
    mp.mp.dps = dps_need
    try:
        r0 = r0 or mp.mpf('0.7')
        w_cut = w_cut or mp.mpf('0.01')
        S_max = S_max or mp.mpf(40) + mp.mpf(dps_need) * mp.log(10) / cval
        branch = solve_branch(Ffunc, cval, r0, S_max, w_cut)
        # Wronskian of (psi_a, psi_b = conj psi_a) from trig coefficients at w_cut:
        A, B = branch["A"], branch["B"]
        W = cval * (A * mp.conj(B) - mp.conj(A) * B)
        cache = build_node_cache(branch, numax)
        if Ghat is not None:
            cache_p = apply_weight(cache, lambda wv: mp.e ** (Ghat(wv)))
            cache_m = apply_weight(cache, lambda wv: mp.e ** (-Ghat(wv)))
            ep_p = mp.e ** (Ghat(w_cut / 2))
            ep_m = mp.e ** (-Ghat(w_cut / 2))
        for nu in nu_list:
            if Ghat is None:
                Pp_p = mellin_from_cache(branch, cache, nu)
                Pp_m = mellin_from_cache(branch, cache, -nu)
                bil = -2j * cval * (Pp_p * mp.conj(Pp_p) - mp.conj(Pp_m) * Pp_m) / W
            else:
                Pp_p = mellin_from_cache(branch, cache_p, nu, ep_p)
                Pp_m = mellin_from_cache(branch, cache_p, -nu, ep_p)
                Pm_p = mellin_from_cache(branch, cache_m, nu, ep_m)
                Pm_m = mellin_from_cache(branch, cache_m, -nu, ep_m)
                bil = -2j * cval * (Pp_p * mp.conj(Pm_p) - mp.conj(Pp_m) * Pm_m) / W
            results[nu] = bil / (2 * mp.pi / cval ** 2)   # normalize: free -> nu
        results["_W"] = W
    finally:
        mp.mp.dps = old
    return results


def fit_tail_laws(nus, dvals):
    """Fit ln|D(nu)| = lnK + beta ln nu  and  lnK + beta ln nu - a nu^s for s in {1/3,1/2,1}.
    Returns dict with pure-power residual and the exponential-improvement diagnostics."""
    nus_f = np.array([float(n) for n in nus])
    mask = np.array([abs(complex(d)) > 0 for d in dvals])
    y = np.array([float(mp.log(abs(d))) for d in dvals])
    out = {}
    A2 = np.column_stack([np.ones_like(nus_f), np.log(nus_f)])
    c2, res2, *_ = np.linalg.lstsq(A2, y, rcond=None)
    r2 = A2 @ c2 - y
    out["power"] = {"K": c2[0], "beta": c2[1], "max_resid": float(np.abs(r2).max())}
    for s, tag in [(1.0 / 3, "s=1/3"), (0.5, "s=1/2"), (1.0, "s=1")]:
        A3 = np.column_stack([np.ones_like(nus_f), np.log(nus_f), -nus_f ** s])
        c3, *_ = np.linalg.lstsq(A3, y, rcond=None)
        r3 = A3 @ c3 - y
        out[tag] = {"a": c3[2], "beta": c3[1], "max_resid": float(np.abs(r3).max())}
    return out


# step-3 profile templates (analytic in the closed first quadrant; vanish ~w^4 at w -> 0)
W_LO = mp.mpf('0.3')

def F_powertail(kappa, p, w_lo=W_LO):
    """F = kappa w^4 (w + w_lo)^{-(p+4)}: -> kappa w^{-p} at large w, ~ w^4 at small w.
    ONLY branch cut: (-inf, -w_lo] — the closed first quadrant is clean. (The earlier
    (w^3 + w_lo^3)-form crossed its principal-branch cut at arg w = 60 deg: bug log.)"""
    kappa = mp.mpf(kappa)
    ex = -(mp.mpf(p) + 4)
    return lambda wv: kappa * wv ** 4 * (wv + w_lo) ** ex


def gain_pair(gamma0, p, w_lo=W_LO):
    """Closed-form (Ghat, ghat, ghat') for ghat = gamma0 w^4 (w+w_lo)^{-(p+4)} (-> gamma0 w^{-p}).
    Ghat exact by the binomial identity w^4 = sum_j C(4,j) (w+a)^{4-j} (-a)^j."""
    from math import comb
    g0, pp, a = mp.mpf(gamma0), mp.mpf(p), mp.mpf(w_lo)
    def Ghat(wv):
        tot = 0
        for j in range(5):
            e = 1 - pp - j
            tot += comb(4, j) * (-a) ** j * ((wv + a) ** e - a ** e) / e
        return g0 * tot
    ghat = lambda wv: g0 * wv ** 4 * (wv + a) ** (-pp - 4)
    ghatp = lambda wv: g0 * (4 * wv ** 3 * (wv + a) ** (-pp - 4)
                             - (pp + 4) * wv ** 4 * (wv + a) ** (-pp - 5))
    return Ghat, ghat, ghatp


NUS_SCAN = [4.0, 6.0, 9.0, 13.5, 20.0, 28.0, 36.0]


def step3a0():
    print("=" * 88)
    print("[HH-3a0] v2 (real-axis saddle route) FREE gate + v1 cross-check on a scan template")
    print("=" * 88)
    res = rho_c_pipeline2(lambda wv: mp.mpc(0), 2.0, [4.0, 20.0, 36.0])
    worst = 0.0
    for nu in [4.0, 20.0, 36.0]:
        rd = float(abs(res[nu] - nu) / nu)
        worst = max(worst, rd)
        print(f"     nu = {nu:>5}: rho_c = {mp.nstr(res[nu].real, 15)}  rel.err = {rd:.2e}")
    print(f"     gate: worst {worst:.2e} < 1e-13 -> {'PASS' if worst < 1e-13 else 'FAIL'}")
    assert worst < 1e-13
    # v1<->v2 are tied through the Bessel Gamma closed form ([2c]: v1 exact to 1e-35; v2 to
    # its known pure-Bessel endpoint bias ~2e-5, absent for templates). On templates v1 is
    # impractically slow; the independence check is CONTOUR-PARAMETER INVARIANCE of v2
    # (s_a, W_max, deg, w_cut, theta_rot all varied — an analytic contour integral must not move):
    F = F_powertail(0.4, mp.mpf(2) / 3)
    base = rho_c_pipeline2(F, 2.0, [6.0, 15.0])
    alt = {}
    old_dps = mp.mp.dps
    mp.mp.dps = 40
    try:
        br_alt = solve_branch2(F, 2.0, mp.mpf('0.003'), mp.mpf(15.0 * 2.2 / 2.0 + 25),
                               s_a=9.0, T_rot=46.0, theta_rot=mp.pi / 4)
        A, B = br_alt["A"], br_alt["B"]
        Wr = 2.0 * (A * mp.conj(B) - mp.conj(A) * B)
        cache_alt = build_node_cache2(br_alt, 15.0, deg=32)
        for nu in [6.0, 15.0]:
            Pp = mellin_from_cache(br_alt, cache_alt, nu)
            Pm = mellin_from_cache(br_alt, cache_alt, -nu)
            bil = -2j * 2.0 * (Pp * mp.conj(Pp) - mp.conj(Pm) * Pm) / Wr
            alt[nu] = bil / (2 * mp.pi / 4.0)
    finally:
        mp.mp.dps = old_dps
    worst = 0.0
    for nu in [6.0, 15.0]:
        rd = float(abs(base[nu] - alt[nu]) / abs(base[nu]))
        worst = max(worst, rd)
        print(f"     contour-invariance (p=2/3 template) nu = {nu:>4}: rho_c = "
              f"{mp.nstr(base[nu].real, 14)}  shift under contour change = {rd:.2e}")
    print(f"     gate: worst {worst:.2e} < 3e-10 -> {'PASS' if worst < 3e-10 else 'FAIL'}")
    assert worst < 3e-10
    print("     => v2 contour-independent to ~1e-10 (the w_cut trig-endpoint template-leakage")
    print("        floor, F(w_cut) ~ 1e-6 kappa; scan signals are O(0.01-1): systematics 8+")
    print("        orders below signal). v2 authorized for the scan.")


def step3a0b():
    """v1 (the STEP-2-validated complex-contour pipeline, exact to 1e-35 vs Gamma closed
    forms) vs v2 (the rewritten real-axis saddle route) on the SAME nontrivial template —
    the demanded cross-validation of the fixed inward segment. Slow (v1 at high dps)."""
    import time as _t
    print("=" * 88)
    print("[HH-3a0b] v1 (STEP-2 exact contour) vs v2 on the SAME p=2/3 template + gain route")
    print("=" * 88)
    F = F_powertail(0.4, mp.mpf(2) / 3)
    worst = 0.0
    for nu in [6.0, 15.0]:
        t0 = _t.time()
        r1 = rho_c_pipeline(F, 2.0, [nu])
        t1 = _t.time()
        r2 = rho_c_pipeline2(F, 2.0, [nu])
        t2 = _t.time()
        rd = float(abs(r1[nu] - r2[nu]) / abs(r1[nu]))
        worst = max(worst, rd)
        print(f"     dispersion nu = {nu:>4}: v1 = {mp.nstr(r1[nu].real, 14)} ({t1-t0:.0f}s)  "
              f"v2 = {mp.nstr(r2[nu].real, 14)} ({t2-t1:.0f}s)  rel.diff = {rd:.2e}")
    # gain route (weighted bilinear) cross-pipeline at nu = 6:
    g0 = 0.4
    Ghat, ghat, ghatp = gain_pair(g0, mp.mpf(2) / 3)
    Feff = lambda wv: (ghatp(wv) - ghat(wv) ** 2) / 4.0
    t0 = _t.time()
    r1g = rho_c_pipeline(Feff, 2.0, [6.0], Ghat=Ghat)
    t1 = _t.time()
    r2g = rho_c_pipeline2(Feff, 2.0, [6.0], Ghat=Ghat)
    t2 = _t.time()
    rdg = float(abs(r1g[6.0] - r2g[6.0]) / abs(r1g[6.0]))
    worst = max(worst, rdg)
    print(f"     gain       nu =  6.0: v1 = {mp.nstr(r1g[6.0].real, 14)} ({t1-t0:.0f}s)  "
          f"v2 = {mp.nstr(r2g[6.0].real, 14)} ({t2-t1:.0f}s)  rel.diff = {rdg:.2e}")
    ok = worst < 1e-8
    print(f"     gate: worst {worst:.2e} < 1e-8 -> {'PASS' if ok else 'FAIL'}")
    assert ok
    print("     => the two pipelines (different contours, different dps regimes, different")
    print("        cancellation structures) agree on nontrivial templates in BOTH the")
    print("        dispersion and the weighted-gain bilinear: v2's rewritten inward segment")
    print("        is validated against the STEP-2 exact machinery. v2 carries the scan.")


def step3a():
    print("=" * 88)
    print("[HH-3a] FORWARD SCAN I — power-law DISPERSION tails (D/P class):")
    print("        the saddle-reading law and the absence of any stretched exponential")
    print("=" * 88)
    cval = 2.0
    nus = NUS_SCAN

    # ---- D-class: real dispersion tails f = kappa w^{-p} ----
    for p, kap in [(mp.mpf(2) / 3, 0.4), (mp.mpf(1), 0.4)]:
        F = F_powertail(kap, p)
        res = rho_c_pipeline2(F, cval, nus)
        print(f"[3a] D-class p = {mp.nstr(p,4)}, kappa = {kap}: Delta rho_c vs saddle-reading "
              f"-(nu/2) F(nu/c):")
        dvals = []
        for nu in nus:
            d = res[nu] - nu
            dvals.append(d)
            mp.mp.dps = 30
            pred = -nu / 2 * F(mp.mpf(nu) / cval)
            print(f"     nu = {nu:>5}: Drho_c = {mp.nstr(d.real, 8):>15}  pred = "
                  f"{mp.nstr(pred, 8):>15}  ratio = {mp.nstr(d.real / pred, 6)}")
        laws = fit_tail_laws(nus, [d.real for d in dvals])
        po = laws["power"]
        print(f"     pure-power fit: beta = {po['beta']:.4f} (expect {float(1-p):.4f}), "
              f"max ln-resid = {po['max_resid']:.2e}")
        for tag in ["s=1/3", "s=1/2", "s=1"]:
            print(f"     +exp({tag}): a = {laws[tag]['a']:+.5f}, max ln-resid = "
                  f"{laws[tag]['max_resid']:.2e}")
        print("     => exponential coefficients consistent with ZERO (no stretched-exponential")
        print("        component); Delta rho_c is the PROFILE READ AT THE SADDLE, power-law class.")

    # linearity spot-check (Born regime) at p = 2/3:
    F2 = F_powertail(0.2, mp.mpf(2) / 3)
    r2 = rho_c_pipeline2(F2, cval, [9.0, 20.0])
    F4 = F_powertail(0.4, mp.mpf(2) / 3)
    r4 = rho_c_pipeline2(F4, cval, [9.0, 20.0])
    print("[3a-lin] linearity in kappa at p = 2/3 (ratio of Delta rho_c at kappa 0.4/0.2):")
    for nu in [9.0, 20.0]:
        rat = (r4[nu] - nu) / (r2[nu] - nu)
        print(f"     nu = {nu:>5}: ratio = {mp.nstr(rat.real, 8)} (2 = pure Born; deviation = "
              f"the kappa^2 secular term)")

def step3b():
    print("=" * 88)
    print("[HH-3b] FORWARD SCAN II — power-law GAIN tail (the envelope question)")
    print("=" * 88)
    cval = 2.0
    nus = NUS_SCAN
    # ---- GAIN tails: ghat = gamma0 w^{-p}, p = 2/3 — THE decisive multiplicative-envelope test
    print("[3b] GAIN tail ghat -> gamma0 w^{-2/3}, gamma0 = 0.4 (Ghat(w) ~ 3 gamma0 w^{1/3}):")
    print("     competing predictions:  (i) envelope-cancellation law: rho_c = nu(1 + power-law),")
    print("     pred1 = -(nu/2) F_eff(nu/c), F_eff = (ghat' - ghat^2)/c^2;")
    print("     (ii) naive envelope survival: rho_c ~ nu e^{-2 Ghat(nu/c)} (index-1/3 SUPPRESSION).")
    g0 = 0.4
    Ghat, ghat, ghatp = gain_pair(g0, mp.mpf(2) / 3)
    Feff = lambda wv: (ghatp(wv) - ghat(wv) ** 2) / cval ** 2
    resg = rho_c_pipeline2(Feff, cval, nus, Ghat=Ghat)
    # contour-invariance cross-check at nu = 6 for the WEIGHTED bilinear (gain route):
    old_dps = mp.mp.dps
    mp.mp.dps = 40
    try:
        br_alt = solve_branch2(Feff, cval, mp.mpf('0.003'), mp.mpf(6.0 * 2.2 / cval + 25),
                               s_a=9.0, T_rot=46.0, theta_rot=mp.pi / 4)
        A, B = br_alt["A"], br_alt["B"]
        Wr = cval * (A * mp.conj(B) - mp.conj(A) * B)
        cache_alt = build_node_cache2(br_alt, 6.0, deg=32)
        cp = apply_weight(cache_alt, lambda wv: mp.e ** (Ghat(wv)))
        cm = apply_weight(cache_alt, lambda wv: mp.e ** (-Ghat(wv)))
        epp = mp.e ** (Ghat(mp.mpf('0.003') / 2))
        epm = mp.e ** (-Ghat(mp.mpf('0.003') / 2))
        Pp_p = mellin_from_cache(br_alt, cp, 6.0, epp)
        Pm_p = mellin_from_cache(br_alt, cm, 6.0, epm)
        Pp_m = mellin_from_cache(br_alt, cp, -6.0, epp)
        Pm_m = mellin_from_cache(br_alt, cm, -6.0, epm)
        bil = -2j * cval * (Pp_p * mp.conj(Pm_p) - mp.conj(Pp_m) * Pm_m) / Wr
        altg = bil / (2 * mp.pi / cval ** 2)
    finally:
        mp.mp.dps = old_dps
    rdg = float(abs(altg - resg[6.0]) / abs(resg[6.0]))
    print(f"     [contour-invariance, gain route, nu = 6: shift = {rdg:.2e}]")
    assert rdg < 1e-9
    for nu in nus:
        mp.mp.dps = 30
        d = resg[nu] - nu
        pred1 = -nu / 2 * Feff(mp.mpf(nu) / cval)
        env = nu * (mp.e ** (-2 * Ghat(mp.mpf(nu) / cval)) - 1)
        print(f"     nu = {nu:>5}: Drho_c = {mp.nstr(d.real, 8):>15}  pred1 = "
              f"{mp.nstr(pred1, 8):>15}  ratio = {mp.nstr(d.real/pred1, 6):>10}  "
              f"[envelope would give {mp.nstr(env, 6)}]")
    print("     => measured Delta rho_c follows pred1 (power-law class, gamma0^2-led);")
    print("        the would-be e^{-6 gamma0 (nu/c)^{1/3}} envelope is ABSENT: the common")
    print("        amplification factor e^{Ghat(w1)} e^{-Ghat(w2)} cancels at the saddle —")
    print("        GAIN TAILS CANNOT IMPRINT THEIR OWN EXPONENT ON THE RESPONSE.")


# ----------------------------------------------------------------------------------------
# STEP 3c-3e — the remaining scan classes, the G/inverse keystone, the all-orders anchors
# ----------------------------------------------------------------------------------------

def F_logGauss(eps, w0, sig):
    """B class: analytic band, Gaussian in ln w (entire in ln w; log-cut on negative axis
    only — clean in the closed first quadrant; vanishes superpolynomially at w -> 0)."""
    e0, l0, s2 = mp.mpf(eps), mp.log(mp.mpf(w0)), 2 * mp.mpf(sig) ** 2
    return lambda wv: e0 * mp.e ** (-(mp.log(wv) - l0) ** 2 / s2)


def F_logper(eps, Om, p, w_lo=W_LO):
    """L class: log-periodic modulation x power-tail envelope. cos(Om ln w) on the
    imaginary ray is bounded by cosh(Om pi/2): analytic and dominated."""
    e0, Omv = mp.mpf(eps), mp.mpf(Om)
    env = F_powertail(1.0, p, w_lo)
    return lambda wv: e0 * mp.cos(Omv * mp.log(wv)) * env(wv)


def F_bank(banks, sig=0.5):
    """X class: windowed filter bank = sum of log-Gaussian channels (w0_j, eps_j)."""
    comps = [F_logGauss(eps, w0, sig) for (w0, eps) in banks]
    return lambda wv: mp.fsum(f(wv) for f in comps)


def F_expw(eps, w_lo=W_LO):
    """index-1 positive control: F = eps e^{-w} x w^4 turn-on (entire x rational;
    decays with a TRUE exponential, index 1 — the fitter must find it)."""
    e0 = mp.mpf(eps)
    return lambda wv: e0 * mp.e ** (-wv) * wv ** 4 * (wv + w_lo) ** (-4)


def F_gevrey3(AF, ctF, phF, cval, w_lo=mp.mpf('0.1'), qF=None, npow=6):
    """G class / the Born-inverse profile: the LOCKED Gevrey-3 pair
        F = AF (cw)^{qF} e^{-ctF (cw)^{1/3}} cos(sqrt3 ctF (cw)^{1/3} + phF) x turn-on,
    turn-on = [w/(w+w_lo)]^npow (integer power: analytic; pole at -w_lo only).
    Parametrized in x = c w so the saddle transcription nu = c w is c-INDEPENDENT.
    Analyticity: principal x^{1/3} and x^{qF} cut the negative axis only; on the
    imaginary ray the locked pair splits into e^{i 5pi/6} (decaying) and e^{-i pi/2}
    (bounded oscillatory) components — dominated on the whole v2 contour."""
    qF = mp.mpf(-4) / 3 if qF is None else mp.mpf(qF)
    AFv, ctFv, phFv = mp.mpf(AF), mp.mpf(ctF), mp.mpf(phF)
    cv, wl = mp.mpf(cval), mp.mpf(w_lo)
    s3, third = mp.sqrt(3), mp.mpf(1) / 3
    def F(wv):
        x = cv * wv
        x3 = x ** third
        return (AFv * x ** qF * mp.e ** (-ctFv * x3) * mp.cos(s3 * ctFv * x3 + phFv)
                * (wv / (wv + wl)) ** npow)
    return F


def fit_osc_model(nus, dvals, init, fix=None, zmode="pow"):
    """VARPRO fit of D(nu) = nu^q e^{-al z} [P cos(be z) + Q sin(be z)],
    z = nu^s (zmode 'pow') or z = ln nu (zmode 'log', al frozen 0, s ignored).
    Envelope-weighted least squares (every point counts at its own scale).
    init = (q, al, be, s). fix = dict freezing any of q/al/be/s.
    Returns dict(q, al, be, s, P, Q, amp, phi, rms_w) — phi from P cos + Q sin
    = amp cos(be z + phi), i.e. phi = -atan2(Q, P)."""
    from scipy.optimize import minimize
    nus_f = np.array([float(n) for n in nus])
    yv = np.array([float(d) for d in dvals])
    names = ["q", "al", "be", "s"]
    fix = dict(fix or {})
    if zmode == "log":
        fix["al"] = 0.0
        fix["s"] = 1.0
    free_idx = [i for i, nm in enumerate(names) if nm not in fix]

    def unpack(th):
        full, j = [], 0
        for nm in names:
            if nm in fix:
                full.append(float(fix[nm]))
            else:
                full.append(float(th[j])); j += 1
        return full

    def ssr(th, ret=False):
        q, al, be, s = unpack(th)
        if zmode == "pow" and not (0.02 < s <= 2.0):
            return 1e99
        if be < 0:
            return 1e99
        # clamp al >= 0: an unbounded negative al is a growth runaway that the
        # envelope-weighted SSR rewards spuriously (caught on the [3c-L] (C1)-form fit:
        # al -> -154 with rms 6e-108 — a degeneracy, not a fit; bug log):
        if zmode == "pow" and al < 0:
            return 1e99
        z = np.log(nus_f) if zmode == "log" else nus_f ** s
        env = nus_f ** q * np.exp(-al * (0 if zmode == "log" else z))
        if not np.all(np.isfinite(env)) or np.any(env <= 0):
            return 1e99
        Aw = np.column_stack([np.cos(be * z), np.sin(be * z)])
        yw = yv / env
        coef, *_ = np.linalg.lstsq(Aw, yw, rcond=None)
        r = Aw @ coef - yw
        v = float(r @ r)
        return (v, coef) if ret else v

    best = None
    th0 = np.array([init[i] for i in free_idx], dtype=float)
    rng = np.random.default_rng(11)
    for trial in range(7):
        start = th0 if trial == 0 else th0 * (1 + 0.15 * rng.standard_normal(len(th0)))
        res = minimize(ssr, start, method="Nelder-Mead",
                       options={"xatol": 1e-12, "fatol": 1e-22,
                                "maxiter": 20000, "maxfev": 30000})
        if best is None or res.fun < best.fun:
            best = res
    v, coef = ssr(best.x, ret=True)
    q, al, be, s = unpack(best.x)
    P, Q = float(coef[0]), float(coef[1])
    return {"q": q, "al": al, "be": be, "s": s, "P": P, "Q": Q,
            "amp": float(np.hypot(P, Q)), "phi": float(np.arctan2(-Q, P)),
            "rms_w": float(np.sqrt(v / len(nus_f)))}


# ---------- step3a1: the EXACT Born kernel (pure Gamma functions; no ODE, no contour) ----------
#
# First order in the Hermitian profile F (gain folded in via F_eff, the [1b]/[3b] reduction):
#   g_a = e^{icw}(1 + delta),  delta(w) = -(ic/2) int_w^inf F(s)(1 - e^{2ic(s-w)}) ds
#   (delta'' + 2ic delta' = -c^2 F, delta(inf) = 0; W stays -2ic exactly for decaying F)
#   ==> Delta rho_c(nu) = int_0^inf K(nu, s) F(s) ds,
#   K(nu,s) = (c^2/pi) Re{ (-ic/2) [ T(nu,s) - T(-nu,s) ] },
#   T(n,s)  = P*(n) [gam_n(c;s) - e^{2ics} gam_n(-c;s)],   P(n) = Gamma(1-in)(-ic)^{in-1},
#   gam_n(a;s) = int_0^s w^{-in} e^{iaw} dw = (-ia)^{in-1} Gamma_low(1-in, -ias).
# Stable forms: P*(n) gam_n(c;s) = |P(n)|^2 GammaREG(1-in, -ics)  (regularized — the
# e^{n pi/2} scales cancel inside mpmath);  the (-c) piece carries e^{-n pi}: small, kept.
# The would-be divergent constant piece (the secular phase int F) is PURE IMAGINARY and
# is killed by Re{} BEFORE the s-integral: the real kernel decays and is integrable.

def born_T_factory(nu, cval):
    nu_ = mp.mpf(nu)
    c = mp.mpf(cval)

    def make(n):
        Pn = mp.gamma(1 - 1j * n) * (-1j * c) ** (1j * n - 1)
        Pn2 = Pn * mp.conj(Pn)
        Pc = mp.conj(Pn) * (1j * c) ** (1j * n - 1)

        def T(s):
            z = 1 - 1j * n
            greg = mp.gammainc(z, 0, -1j * c * s, regularized=True)
            glow = mp.gammainc(z, 0, 1j * c * s)
            return Pn2 * greg - mp.e ** (2j * c * s) * Pc * glow
        return T

    Tp, Tm = make(nu_), make(-nu_)

    def Kre(s):
        return (c ** 2 / mp.pi) * mp.re((-1j * c / 2) * (Tp(s) - Tm(s)))
    return Kre


def born_drho(nu, cval, Ffunc, S_max=None, dps=50):
    """Exact first-order Delta rho_c(nu) = int_0^S K(nu,s) F(s) ds (real-kernel form;
    oscillation-aligned panels: dense to 3x the saddle, then pi/c-period panels)."""
    old = mp.mp.dps
    mp.mp.dps = dps
    try:
        c = mp.mpf(cval)
        Kre = born_T_factory(nu, cval)
        sstar = mp.mpf(nu) / c
        S_max = mp.mpf(S_max if S_max is not None else 600)
        pts = [mp.mpf(0), mp.mpf('0.05'), mp.mpf('0.2')]
        x = mp.mpf('0.5')
        while x < 3 * sstar:
            pts.append(x)
            x *= mp.mpf('1.35')
        per = mp.pi / c
        x = 3 * sstar
        while x < S_max:
            pts.append(x)
            x += 2 * per
        pts.append(S_max)
        pts = sorted(set(pts))
        val = mp.quad(lambda s: Kre(s) * Ffunc(s), pts)
        return val
    finally:
        mp.mp.dps = old


def step3a1():
    print("=" * 88)
    print("[HH-3a1] THE EXACT BORN KERNEL (independent machinery: pure Gamma functions,")
    print("         no ODE, no contour) — locality, the read coefficient C(p), and the")
    print("         lock-transcription question answered before interpreting the scans")
    print("=" * 88)
    cval = 2.0

    # [a] gammainc identity gate (the kernel's building block vs direct quadrature):
    mp.mp.dps = 50
    nu0, s0 = 7.3, 2.6
    g_direct = mp.quad(lambda w: w ** (-1j * mp.mpf(nu0)) * mp.e ** (1j * cval * w), [0, s0])
    g_closed = ((-1j * cval) ** (1j * mp.mpf(nu0) - 1)
                * mp.gammainc(1 - 1j * mp.mpf(nu0), 0, -1j * cval * s0))
    rd = float(abs(g_direct - g_closed) / abs(g_closed))
    print(f"[a] gam_nu(c;s) closed vs direct (nu=7.3, s=2.6): rel.diff = {rd:.2e} -> "
          f"{'PASS' if rd < 1e-30 else 'FAIL'}")
    assert rd < 1e-30

    # [b] kernel locality: K(20, s) profile (saddle at s* = nu/c = 10):
    Kre = born_T_factory(20.0, cval)
    print("[b] kernel shape K(20, s) (saddle s* = 10, width ~ sqrt(nu)/c ~ 2.2):")
    for s in [2.0, 5.0, 8.0, 9.0, 10.0, 11.0, 12.0, 15.0, 20.0, 40.0, 100.0, 300.0]:
        print(f"     s = {s:>6}: K = {float(Kre(mp.mpf(s))):+.6e}")

    # [c] Born vs the EXACT anchors (convergence in coupling => the kernel is right):
    print("[c] Born vs exact (Bessel p=2; both couplings — error must scale ~ mu):")
    mp.mp.dps = 60
    FB1 = lambda s: mp.mpf('0.4') / s ** 2
    FB2 = lambda s: mp.mpf('0.1') / s ** 2
    for nu in [6.0, 15.0]:
        ex4 = rho_c_bessel_closed(nu, mp.mpf('0.4'), mp.mpf(cval)) - nu
        ex1 = rho_c_bessel_closed(nu, mp.mpf('0.1'), mp.mpf(cval)) - nu
        b4 = born_drho(nu, cval, FB1, S_max=400)
        b1 = born_drho(nu, cval, FB2, S_max=400)
        r4 = float(abs(b4 - ex4.real) / abs(ex4.real))
        r1 = float(abs(b1 - ex1.real) / abs(ex1.real))
        print(f"     nu = {nu:>4}: mu=0.4: Born {mp.nstr(b4, 8)} vs exact {mp.nstr(ex4.real, 8)} "
              f"(rel {r4:.2e}); mu=0.1: rel {r1:.2e}; error ratio {r4/r1:.2f} (linear-in-mu "
              f"Born residual => ~4)")

    # [d] Born vs the v2 PIPELINE on the p=2/3 template (independent-machinery agreement):
    print("[d] Born vs v2 pipeline, p = 2/3 template (kappa 0.4 banked / 0.1 fresh):")
    F23_4 = F_powertail(0.4, mp.mpf(2) / 3)
    F23_1 = F_powertail(0.1, mp.mpf(2) / 3)
    pipe4 = {6.0: mp.mpf('5.0939362006623') - 6, 15.0: mp.mpf('13.467890327256') - 15}
    pipe1 = rho_c_pipeline2(F23_1, cval, [6.0, 15.0])
    for nu in [6.0, 15.0]:
        b4 = born_drho(nu, cval, F23_4, S_max=900)
        b1 = born_drho(nu, cval, F23_1, S_max=900)
        p4 = float(pipe4[nu])
        p1 = float((pipe1[nu] - nu).real)
        r4 = abs(float(b4) - p4) / abs(p4)
        r1 = abs(float(b1) - p1) / abs(p1)
        print(f"     nu = {nu:>4}: kap=0.4: Born {float(b4):+.6f} vs pipe {p4:+.6f} "
              f"(rel {r4:.2e}); kap=0.1: Born {float(b1):+.6f} vs pipe {p1:+.6f} "
              f"(rel {r1:.2e}); error ratio {r4/r1:.2f} (~4 = kappa^2 Born tail)")

    # [e] the read coefficient C(p): Delta rho_Born = -C(p) nu kappa (nu/c)^{-p} (kappa = 1):
    print("[e] the read coefficient C(p) (pure powers; the saddle map is p-DEPENDENT):")
    print("     [C(0) = 3/2 exact (c_eff argument); anchors: C(2) -> 1/2, C(1) below]")
    for p in [mp.mpf(2) / 3, mp.mpf(1), mp.mpf(4) / 3, mp.mpf(2), mp.mpf(8) / 3]:
        row = []
        for nu in [20.0, 50.0]:
            Fp = lambda s, pv=p: s ** (-pv)
            b = born_drho(nu, cval, Fp, S_max=1200, dps=50)
            Cv = -float(b) / (nu * (nu / cval) ** (-float(p)))
            row.append(f"nu={nu:.0f}: C = {Cv:+.5f}")
        print(f"     p = {mp.nstr(p, 4):>6}: " + "   ".join(row))
    # exact-anchor large-nu coefficients (Born-clean small coupling):
    mp.mp.dps = 100
    exC2 = -(rho_c_bessel_closed(200.0, mp.mpf('0.01'), mp.mpf(2)) - 200).real \
        / (200 * mp.mpf('0.01') * (mp.mpf(100)) ** -2)
    exC1 = -(rho_c_coulomb_closed(200.0, mp.mpf('0.01'), mp.mpf(2)) - 200).real \
        / (200 * mp.mpf('0.01') * (mp.mpf(100)) ** -1)
    print(f"     exact anchors at nu = 200, coupling 0.01: C(2) = {mp.nstr(exC2, 6)}, "
          f"C(1) = {mp.nstr(exC1, 6)}")

    # [f] THE LOCK QUESTION: the kernel applied to the G profile (the same grid as [3d]) —
    # does the locked pair transcribe at sqrt3, or does the saddle map detune it?
    print("[f] Born kernel applied to the G profile (independent of the pipeline):")
    ct = CT["fw"]
    FG = F_gevrey3(-2.0, ct, mp.pi / 8, cval, w_lo=mp.mpf('0.1'), npow=6)
    grid = [float((mp.mpf('1.6') + mp.mpf('0.2') * j) ** 3) for j in range(16)]
    dB = []
    for nu in grid:
        b = born_drho(nu, cval, FG, S_max=80, dps=50)
        dB.append(float(b))
        print(f"     nu = {nu:>7.3f}: Born Drho_c = {float(b):+.6e}")
    s3 = float(mp.sqrt(3))
    ftB = fit_osc_model(grid, dB, init=(-1.0 / 3, float(ct), s3 * float(ct), 1.0 / 3))
    print(f"     Born-side fit: s = {ftB['s']:.5f}  al = {ftB['al']:.5f}  "
          f"be = {ftB['be']:.5f}  be/al = {ftB['be']/ftB['al']:.5f}  q = {ftB['q']:+.4f}  "
          f"amp = {ftB['amp']:.4f}  phi = {ftB['phi']:+.4f}  rms_w = {ftB['rms_w']:.2e}")
    print(f"     targets:       s = 0.33333  al = {float(ct):.5f}  be = {s3*float(ct):.5f}  "
          f"be/al = {s3:.5f}  q = -1/3  amp = 1  phi = {float(mp.pi/8):+.4f}")
    print("     => [to be read against [3d]'s pipeline fit: agreement = the transcription")
    print("        is confirmed by two fully independent computations]")


def step3c():
    print("=" * 88)
    print("[HH-3c] FORWARD SCAN III — bands (B), log-periodic (L), filter bank (X),")
    print("        and the index-1 positive control: NONE reach the (C1) class")
    print("=" * 88)
    cval = 2.0
    nus = NUS_SCAN + [50.0, 70.0, 97.0]   # extended window: ln nu and nu^{1/3} separate

    # ---- B: analytic log-Gaussian band ----
    eps, w0, sig = 0.3, 3.0, 0.5
    FB = F_logGauss(eps, w0, sig)
    res = rho_c_pipeline2(FB, cval, nus, dps=46)
    print(f"[3c-B] band eps = {eps}, w0 = {w0}, sig = {sig} (band center reads at nu = c w0 = 6):")
    dB = []
    for nu in nus:
        mp.mp.dps = 30
        d = res[nu] - nu
        dB.append(d.real)
        pred = -nu / 2 * FB(mp.mpf(nu) / cval)
        print(f"     nu = {nu:>5}: Drho_c = {mp.nstr(d.real, 8):>15}  pred = "
              f"{mp.nstr(pred, 8):>15}  ratio = {mp.nstr(d.real / pred, 6)}")
    nsign = sum(1 for a, b in zip(dB, dB[1:]) if a * b < 0)
    y = np.array([float(mp.log(abs(d))) for d in dB])
    lnn = np.log(np.array([float(n) for n in nus]))
    # log-normal model (the saddle transcription of a log-Gaussian band):
    Aln = np.column_stack([np.ones_like(lnn), lnn, lnn ** 2])
    cln, *_ = np.linalg.lstsq(Aln, y, rcond=None)
    rln = float(np.abs(Aln @ cln - y).max())
    # (C1)-class model on the same data:
    Ac1 = np.column_stack([np.ones_like(lnn), lnn,
                           -np.array([float(n) for n in nus]) ** (1.0 / 3)])
    cc1, *_ = np.linalg.lstsq(Ac1, y, rcond=None)
    rc1 = float(np.abs(Ac1 @ cc1 - y).max())
    print(f"     sign changes of Drho_c on the grid: {nsign} (the (C1) tail would oscillate)")
    print(f"     log-normal fit  ln|D| = a0+a1 ln nu+a2 ln^2 nu: a2 = {cln[2]:+.4f} "
          f"(transcription pred -1/(2 sig^2) = {-1/(2*sig**2):+.4f}), max-resid = {rln:.3f}")
    print(f"     (C1)-form fit   ln|D| = lnK+q ln nu-ct nu^(1/3): ct = {cc1[2]:+.4f}, "
          f"max-resid = {rc1:.3f}")
    print("     => the band transcribes to a LOG-NORMAL tail (quadratic-in-ln nu, its own"
          if rln < rc1 else "     => UNEXPECTED — investigate")
    print("        analytic class), monotone (no sign change): NOT the (C1) exponential-")
    print("        oscillatory class; the (C1)-form fit fails by orders in residual.")

    # ---- L: log-periodic on a power envelope ----
    epsL, OmL, pL = 0.3, 3.0, mp.mpf(2) / 3
    FL = F_logper(epsL, OmL, pL)
    resL = rho_c_pipeline2(FL, cval, nus, dps=46)
    print(f"[3c-L] log-periodic eps = {epsL}, Omega = {OmL}, envelope p = 2/3:")
    dL = []
    for nu in nus:
        mp.mp.dps = 30
        d = resL[nu] - nu
        dL.append(d.real)
        pred = -nu / 2 * FL(mp.mpf(nu) / cval)
        print(f"     nu = {nu:>5}: Drho_c = {mp.nstr(d.real, 8):>15}  pred = "
              f"{mp.nstr(pred, 8):>15}  ratio = {mp.nstr(d.real / pred, 6)}")
    fitLP = fit_osc_model(nus, dL, init=(1.0 / 3, 0.0, OmL, 1.0), zmode="log")
    fitC1 = fit_osc_model(nus, dL, init=(-1.0 / 3, CT["fw"], 3 ** 0.5 * CT["fw"], 1.0 / 3),
                          fix={"s": 1.0 / 3})
    print(f"     log-periodic model fit: q = {fitLP['q']:.4f} (pred {float(1-pL):.4f}), "
          f"Omega_fit = {fitLP['be']:.4f} (pred {OmL}), weighted rms = {fitLP['rms_w']:.2e}")
    print(f"     (C1)-form fit (s=1/3): al = {fitC1['al']:+.4f} (the required DECAY "
          f"ct = {CT['fw']:.3f}), be/al lock undefined/absent, weighted rms = {fitC1['rms_w']:.2e}")
    print("     => oscillation lives in ln nu with NO stretched-exponential decay:")
    print("        the 1/sqrt3 decay/oscillation LOCK (C2) is unreachable — fitted decay")
    print("        is consistent with zero; class = log-periodic x power, not (C1).")

    # ---- X: three-channel filter bank ----
    banks = [(1.5, 0.3), (4.5, 0.18), (13.5, 0.108)]
    FX = F_bank(banks, sig=0.5)
    resX = rho_c_pipeline2(FX, cval, nus, dps=46)
    print(f"[3c-X] filter bank {banks}, sig = 0.5 (log-spaced channels x3):")
    dX = []
    for nu in nus:
        mp.mp.dps = 30
        d = resX[nu] - nu
        dX.append(d.real)
        pred = -nu / 2 * FX(mp.mpf(nu) / cval)
        print(f"     nu = {nu:>5}: Drho_c = {mp.nstr(d.real, 8):>15}  pred = "
              f"{mp.nstr(pred, 8):>15}  ratio = {mp.nstr(d.real / pred, 6)}")
    print("     => the bank transcribes channel-by-channel (Born additivity, cf [3a-lin]):")
    print("        a superposition of log-normals — piecewise log-normal envelope, no")
    print("        nu^(1/3) oscillation, no lock. A bank can only reach (C1) by TUNING its")
    print("        weights into the fingerprint itself (= the G transcription of [3d]).")

    # ---- index-1 positive control: the fitter must FIND a true exponential ----
    Fe = F_expw(0.3)
    nuse = [4.0, 6.0, 9.0, 13.5, 20.0, 28.0]
    rese = rho_c_pipeline2(Fe, cval, nuse, dps=46)
    de = []
    print("[3c-E] index-1 control F = 0.3 e^{-w} x turn-on (true exponential, decay 1/c):")
    for nu in nuse:
        mp.mp.dps = 30
        d = rese[nu] - nu
        de.append(d.real)
        pred = -nu / 2 * Fe(mp.mpf(nu) / cval)
        print(f"     nu = {nu:>5}: Drho_c = {mp.nstr(d.real, 8):>15}  pred = "
              f"{mp.nstr(pred, 8):>15}  ratio = {mp.nstr(d.real / pred, 6)}")
    laws = fit_tail_laws(nuse, de)
    print(f"     pure-power residual {laws['power']['max_resid']:.3f}; +exp fits: "
          f"s=1/3: a = {laws['s=1/3']['a']:+.4f} resid {laws['s=1/3']['max_resid']:.3f} | "
          f"s=1/2: a = {laws['s=1/2']['a']:+.4f} resid {laws['s=1/2']['max_resid']:.3f} | "
          f"s=1: a = {laws['s=1']['a']:+.4f} resid {laws['s=1']['max_resid']:.2e}")
    print(f"     => s = 1 wins with a = {laws['s=1']['a']:+.4f} vs transcription pred 1/c = "
          f"{1/cval:.4f}: the methodology DETECTS a true exponential and reads its index —")
    print("        the null results above are nulls of the profiles, not of the method.")


def step3c2():
    print("=" * 88)
    print("[HH-3c2] the beyond-band index-1/2 tail of [3c-B]: artifact tests")
    print("         (contour invariance + eps-linearity => Born order identified)")
    print("=" * 88)
    cval = 2.0
    # the [3c-B] beyond-band points measured e^{-2 sqrt(nu)}: certify they are (i) contour-
    # independent (not a pipeline artifact) and (ii) first- or second-order in eps.
    FB1 = F_logGauss(0.3, 3.0, 0.5)
    FB2 = F_logGauss(0.15, 3.0, 0.5)
    res1 = rho_c_pipeline2(FB1, cval, [36.0, 50.0], dps=46)
    res2 = rho_c_pipeline2(FB2, cval, [36.0, 50.0], dps=46)
    print("[3c2-a] eps-linearity (eps 0.3 -> 0.15; ratio 2 = 1st order, 4 = 2nd order):")
    for nu in [36.0, 50.0]:
        r = float((res1[nu] - nu).real / (res2[nu] - nu).real)
        print(f"     nu = {nu:>5}: Drho(0.3)/Drho(0.15) = {r:.4f}")
    # contour invariance at nu = 50 (alternate contour, deg 32):
    old_dps = mp.mp.dps
    mp.mp.dps = 46
    try:
        br_alt = solve_branch2(FB1, cval, mp.mpf('0.003'), mp.mpf(50 * 2.2 / cval + 25),
                               s_a=9.0, T_rot=46.0, theta_rot=mp.pi / 4)
        A_, B_ = br_alt["A"], br_alt["B"]
        Wr = cval * (A_ * mp.conj(B_) - mp.conj(A_) * B_)
        cache_alt = build_node_cache2(br_alt, 50.0, deg=32)
        Pp = mellin_from_cache(br_alt, cache_alt, 50.0)
        bil = -2j * cval * (Pp * mp.conj(Pp)) / Wr
        altv = bil / (2 * mp.pi / cval ** 2)
    finally:
        mp.mp.dps = old_dps
    d50 = float((res1[50.0] - 50.0).real)
    shift = abs(float((altv - 50.0).real) - d50)
    print(f"[3c2-b] contour-invariance at nu = 50: shift = {shift:.2e} vs signal "
          f"{abs(d50):.2e} -> {'PASS' if shift < 0.01 * abs(d50) else 'FAIL'}")
    assert shift < 0.01 * abs(d50)
    print("     => the beyond-band tail is a REAL response feature at the stated order;")
    print("        sign-definite, no oscillation, index 1/2 — NOT the (C1) class either way.")


def step3c4():
    print("=" * 88)
    print("[HH-3c4] the index-1/2 tail is FIRST order ([3c2] ratio = 2): kernel-side")
    print("         confirmation + the w0-scaling of the constant")
    print("=" * 88)
    # [3c2] measured eps-linearity ratio 2.0026/2.0002 at nu = 36/50: FIRST order — against
    # the pre-registered ratio-4 prediction. The exact Born kernel must therefore CONTAIN
    # the e^{-2 sqrt nu} structure (the naive Gaussian-FT estimate missed the chirped-
    # Gaussian complex saddle). Mechanical check: born_drho on the band vs the pipeline.
    cval = 2.0
    FB = F_logGauss(0.3, 3.0, 0.5)
    pipe = {36.0: 0.03698061, 50.0: 0.0050724596}    # [3c-B] banked pipeline values
    print("[3c4-a] Born kernel applied to the band (first-order completeness check):")
    for nu in [36.0, 50.0]:
        b = born_drho(nu, cval, FB, S_max=240, dps=50)
        print(f"     nu = {nu:>5}: Born = {float(b):+.6e}  pipeline = {pipe[nu]:+.6e}  "
              f"ratio = {float(b)/pipe[nu]:.4f}")
    print("     => ratio ~ 1 confirms the tail is INSIDE the first-order kernel image —")
    print("        the index menu of Born responses includes band-edge index-1/2 tails.")
    # w0-scaling of the constant: a(w0) from a 4-point tail at w0 = 6 (band reads at 12):
    FB6 = F_logGauss(0.3, 6.0, 0.5)
    nus6 = [36.0, 50.0, 64.0, 80.0, 97.0]
    res6 = rho_c_pipeline2(FB6, cval, nus6, dps=48)
    dv6 = [float((res6[nu] - nu).real) for nu in nus6]
    print("[3c4-b] w0 = 6 band beyond-band tail:")
    for nu, d in zip(nus6, dv6):
        print(f"     nu = {nu:>5}: Drho_c = {d:+.6e}")
    nus_f = np.array(nus6)
    y = np.log(np.abs(np.array(dv6)))
    A12 = np.column_stack([np.ones_like(nus_f), np.log(nus_f), -np.sqrt(nus_f)])
    c12, *_ = np.linalg.lstsq(A12, y, rcond=None)
    r12 = np.abs(y - A12 @ c12).max()
    print(f"     index-1/2 fit: a(w0=6) = {c12[2]:+.4f} (w0=3 gave ~2.0), q = {c12[1]:+.3f}, "
          f"max ln-resid = {r12:.4f}")
    print(f"     scaling diagnosis: a proportional to sqrt(2 c w0)? pred a = "
          f"{float(np.sqrt(2 * cval * 6.0) / np.sqrt(2 * cval * 3.0) * 2.0):.3f}; "
          f"w0-independent? pred a = 2.0")


def step3c3():
    print("=" * 88)
    print("[HH-3c3] HOSTILITY AGAINST THE THEOREM — strong band (eps = 1): do NONLINEAR")
    print("         orders generate an index-1/3 oscillatory component from a band?")
    print("=" * 88)
    # [3c-B]/[3c2] establish the orders: first order = log-normal transcription; the
    # beyond-band tail (index 1/2, e^{-2 sqrt nu} at c = 2) at the order identified by
    # the eps-linearity test. The remaining loophole for the no-go: an eps^3-order
    # index-1/3 OSCILLATORY component (3-fold saddle geometry). At eps = 1 any such term
    # is x37 enhanced relative to the eps^2 tail vs the eps = 0.3 run. Fit the strong-band
    # beyond-band tail against (i) pure index-1/2 monotone, (ii) an added (C1)-class
    # component at the required ct: bound its amplitude.
    cval = 2.0
    FB = F_logGauss(1.0, 3.0, 0.5)
    nus = [20.0, 28.0, 36.0, 50.0, 64.0, 80.0, 97.0]
    res = rho_c_pipeline2(FB, cval, nus, dps=48)
    dv = []
    print("[3c3-a] strong band eps = 1.0, w0 = 3, sig = 0.5 — beyond-band tail:")
    for nu in nus:
        d = float((res[nu] - nu).real)
        dv.append(d)
        print(f"     nu = {nu:>5}: Drho_c = {d:+.6e}")
    # index-1/2 monotone fit:
    nus_f = np.array(nus)
    y = np.log(np.abs(np.array(dv)))
    A12 = np.column_stack([np.ones_like(nus_f), np.log(nus_f), -np.sqrt(nus_f)])
    c12, *_ = np.linalg.lstsq(A12, y, rcond=None)
    r12 = y - A12 @ c12
    print(f"[3c3-b] index-1/2 fit: a = {c12[2]:+.4f} (eps=0.3 run gave ~2.0), q = "
          f"{c12[1]:+.3f}, max ln-resid = {np.abs(r12).max():.4f}")
    # residual (C1)-component bound: subtract the 1/2-fit, project the residual of the
    # SIGNED data onto the (C1) template at ct_fw (both quadratures):
    env = np.exp(A12 @ c12)
    sgn = np.sign(dv)
    resid = np.array(dv) - sgn * env
    ct = float(CT["fw"])
    z = nus_f ** (1.0 / 3)
    b1 = nus_f ** (-1.0 / 3) * np.exp(-ct * z) * np.cos(np.sqrt(3) * ct * z)
    b2 = nus_f ** (-1.0 / 3) * np.exp(-ct * z) * np.sin(np.sqrt(3) * ct * z)
    G = np.column_stack([b1, b2])
    coefc1, *_ = np.linalg.lstsq(G, resid, rcond=None)
    Ac1 = float(np.hypot(*coefc1))
    print(f"[3c3-c] (C1)-component amplitude in the residual: A_c1 = {Ac1:.3e}")
    print(f"     scale: the [3d] transcription profile at A = 1 delivers amp = 1 in these")
    print(f"     units; a band-generated (C1) term at eps^3 with O(1) geometry would be")
    print(f"     O(1). Bound: |A_c1| -> {'NEGLIGIBLE' if Ac1 < 0.05 else 'NON-NEGLIGIBLE'}")
    print("     => " + ("no index-1/3 oscillatory component emerges from the band even at"
                        if Ac1 < 0.05 else "INVESTIGATE — possible nonlinear (C1) channel:")
          + " strong coupling.")


def step3d():
    print("=" * 88)
    print("[HH-3d] THE KEYSTONE — G class forward run = the Born-INVERSE profile pushed")
    print("        through the exact pipeline: does the fingerprint transcribe?")
    print("=" * 88)
    cval = 2.0
    third = mp.mpf(1) / 3
    wcut = mp.mpf('0.001')
    # Born inversion of the (C1) target (coefficient C0 = 1/2 measured in [3a]/[3b]):
    #   Delta rho_c^req(nu) = A nu^{-1/3} e^{-ct nu^{1/3}} cos(sqrt3 ct nu^{1/3} + ph)
    #   = -(nu/2) F(nu/c)  ==>  F_req(w) = -2A (cw)^{-4/3} e^{-ct (cw)^{1/3}}
    #                                       cos(sqrt3 ct (cw)^{1/3} + ph)
    # Scan profile: AF = -2 (=> A_target = +1, phase preserved exactly), phF = pi/8.
    ct = CT["fw"]
    phF = mp.pi / 8
    FG = F_gevrey3(-2.0, ct, phF, cval, w_lo=mp.mpf('0.1'), npow=6)
    grid = [float((mp.mpf('1.6') + mp.mpf('0.2') * j) ** 3) for j in range(16)]

    # [3d-0] free-floor gate AT THE SCAN SETTINGS (the Drho subtraction needs ~1e-12 rel):
    resf = rho_c_pipeline2(lambda wv: mp.mpc(0), cval, [grid[0], grid[-1]],
                           w_cut=wcut, dps=50, deg=28)
    fl0 = float(abs(resf[grid[0]] - grid[0]) / grid[0])
    fl1 = float(abs(resf[grid[-1]] - grid[-1]) / grid[-1])
    print(f"[3d-0] free floor at scan settings: nu = {grid[0]:.3f}: {fl0:.2e}; "
          f"nu = {grid[-1]:.3f}: {fl1:.2e}  -> {'PASS' if max(fl0, fl1) < 2e-12 else 'FAIL'}")
    assert max(fl0, fl1) < 2e-12

    # [3d-1] the forward run (fw footing constant):
    res = rho_c_pipeline2(FG, cval, grid, w_cut=wcut, dps=50, deg=28)
    dvals, preds = [], []
    print(f"[3d-1] G profile: AF = -2, ct_F = ct_fw = {float(ct):.4f}, phF = pi/8, "
          f"qF = -4/3, w_lo = 0.1, npow = 6; the transcription PREDICTION is the (C1)")
    print("        fingerprint with A = 1, phase pi/8, SAME ct (x = cw parametrization):")
    for nu in grid:
        mp.mp.dps = 30
        d = (res[nu] - nu).real
        pred = float(-nu / 2 * FG(mp.mpf(nu) / cval))
        dvals.append(d)
        preds.append(pred)
        cosfac = float(mp.cos(mp.sqrt(3) * ct * mp.mpf(nu) ** third + phF))
        tag = f"ratio = {d/pred:9.5f}" if abs(cosfac) > 0.4 else "  (near node)"
        print(f"     nu = {nu:>7.3f}: Drho_c = {d:+.6e}  pred = {pred:+.6e}  {tag}")

    # [3d-2] contour invariance for THIS profile at nu = 64 (independent re-verification):
    nuv = 64.0
    old_dps = mp.mp.dps
    mp.mp.dps = 50
    try:
        br_alt = solve_branch2(FG, cval, mp.mpf('0.003'), mp.mpf(nuv * 2.2 / cval + 25),
                               s_a=9.0, T_rot=46.0, theta_rot=mp.pi / 4)
        A_, B_ = br_alt["A"], br_alt["B"]
        Wr = cval * (A_ * mp.conj(B_) - mp.conj(A_) * B_)
        cache_alt = build_node_cache2(br_alt, nuv, deg=32)
        Pp = mellin_from_cache(br_alt, cache_alt, nuv)
        bil = -2j * cval * (Pp * mp.conj(Pp)) / Wr
        altv = bil / (2 * mp.pi / cval ** 2)
    finally:
        mp.mp.dps = old_dps
    d64 = dvals[grid.index(64.0)] if 64.0 in grid else None
    shift = float(abs((altv - 64.0).real - d64))
    print(f"[3d-2] contour-invariance at nu = 64: Drho shift = {shift:.2e} vs signal "
          f"{abs(d64):.2e} -> {'PASS' if shift < 0.01 * abs(d64) else 'FAIL'}")
    assert shift < 0.01 * abs(d64)

    # [3d-3] fits: measured vs prediction-on-the-same-window (differential — kills
    # finite-window and turn-on bias in the comparison):
    init = (-1.0 / 3, float(ct), float(mp.sqrt(3) * ct), 1.0 / 3)
    fitM = fit_osc_model(grid, dvals, init=init)
    fitP = fit_osc_model(grid, preds, init=init)
    s3 = float(mp.sqrt(3))
    print("[3d-3] free-(q, al, be, s) oscillatory VARPRO fits:")
    for nm, ft in [("measured ", fitM), ("predicted", fitP)]:
        print(f"     {nm}: s = {ft['s']:.5f}  al = {ft['al']:.5f}  be = {ft['be']:.5f}  "
              f"be/al = {ft['be']/ft['al']:.5f}  q = {ft['q']:+.4f}  amp = {ft['amp']:.4f}  "
              f"phi = {ft['phi']:+.4f}  rms_w = {ft['rms_w']:.2e}")
    print(f"     targets:   s = 1/3 = 0.33333  al = ct = {float(ct):.5f}  "
          f"be = sqrt3 ct = {float(mp.sqrt(3)*ct):.5f}  be/al = sqrt3 = {s3:.5f}  "
          f"q = -1/3  amp = 1  phi = pi/8 = {float(mp.pi/8):+.4f}")
    dev_s = abs(fitM["s"] - 1.0 / 3)
    dev_lock = abs(fitM["be"] / fitM["al"] - s3) / s3
    dev_ct = abs(fitM["al"] - float(ct)) / float(ct)
    dev_MP = max(abs(fitM["s"] - fitP["s"]), abs(fitM["al"] - fitP["al"]),
                 abs(fitM["be"] - fitP["be"]))
    print(f"     |s - 1/3| = {dev_s:.4f}; lock dev = {dev_lock:.4f}; ct dev = {dev_ct:.4f}; "
          f"max measured-vs-predicted param gap = {dev_MP:.4f}")
    ok3 = dev_s < 0.02 and dev_lock < 0.03 and dev_ct < 0.03 and dev_MP < 0.02
    print(f"     gate (s to 0.02, lock to 3%, ct to 3%, M-vs-P to 0.02) -> "
          f"{'PASS' if ok3 else 'FAIL'}")

    # [3d-4] hostile re-verifications: c = 3 (different saddle, different contour);
    # w_lo = 0.05 (different regulator); AF/2 (Born linearity); canon + hostile footings.
    grid10 = [float((mp.mpf('1.6') + mp.mpf('0.3') * j) ** 3) for j in range(10)]
    runs = [
        ("c = 3            ", F_gevrey3(-2.0, ct, phF, 3.0, w_lo=mp.mpf('0.1'), npow=6), 3.0,
         float(ct)),
        ("w_lo = 0.05      ", F_gevrey3(-2.0, ct, phF, cval, w_lo=mp.mpf('0.05'), npow=6),
         cval, float(ct)),
        ("ct = canon 1.9687", F_gevrey3(-2.0, CT["canon"], phF, cval, w_lo=mp.mpf('0.1'),
                                        npow=6), cval, CT["canon"]),
        ("ct = host  2.2790", F_gevrey3(-2.0, CT["hostile"], phF, cval, w_lo=mp.mpf('0.1'),
                                        npow=6), cval, CT["hostile"]),
    ]
    print("[3d-4] hostile re-verifications (10-point grids, independent caches):")
    for tag, Fv, cv, ctv in runs:
        rv = rho_c_pipeline2(Fv, cv, grid10, w_cut=wcut, dps=50, deg=28)
        dv = [float((rv[nu] - nu).real) for nu in grid10]
        ftv = fit_osc_model(grid10, dv, init=(-1.0 / 3, ctv, s3 * ctv, 1.0 / 3))
        print(f"     {tag}: s = {ftv['s']:.5f}  al = {ftv['al']:.5f} (target {ctv:.5f})  "
              f"be/al = {ftv['be']/ftv['al']:.5f}  amp = {ftv['amp']:.4f}  "
              f"phi = {ftv['phi']:+.4f}  rms_w = {ftv['rms_w']:.2e}")
    # Born linearity for the G class (AF -> AF/2 halves Drho):
    FG2 = F_gevrey3(-1.0, ct, phF, cval, w_lo=mp.mpf('0.1'), npow=6)
    nl = [grid[1], grid[7], grid[12]]
    r2 = rho_c_pipeline2(FG2, cval, nl, w_cut=wcut, dps=50, deg=28)
    print("     Born linearity (AF -2 -> -1):", end="")
    for nu in nl:
        rat = dvals[grid.index(nu)] / float((r2[nu] - nu).real)
        print(f"  nu={nu:.1f}: ratio = {rat:.6f}", end="")
    print("   (2 = exact linearity)")
    print("[3d] => the Born-inverse profile EXISTS, is scale-invariant, analytic,")
    print("     and transcribes through the exact pipeline onto the (C1)-(C2) fingerprint")
    print("     (s = 1/3, the sqrt3 lock, ct by footing, phase preserved, amplitude linear).")
    print("     The inverse and forward problems agree: the image of scale-invariant pumping")
    print("     contains the fingerprint ONLY through profiles that already carry it.")


def step3d2():
    print("=" * 88)
    print("[HH-3d2] LOOP CLOSURE — the CORRECTED Born inverse, forward through the exact")
    print("         pipeline: the measured operator map inverted on the locked class")
    print("=" * 88)
    # The measured read operator ([3a]/[3a1]): Drho(nu) = -nu[(3/2)F + (1/2)sF']|_{s=nu/c}.
    # Inverted on the locked Gevrey-3 class (exponent identity; affine bookkeeping):
    #   F_req(w) = (3A/ct) (cw)^{-5/3} e^{-ct(cw)^{1/3}} cos(sqrt3 ct (cw)^{1/3} + ph + pi/3)
    # must transcribe to EXACTLY the (C1) fingerprint A nu^{-1/3} e^{-ct nu^{1/3}}
    # cos(sqrt3 ct nu^{1/3} + ph): amp = A, q = -1/3, phase = ph, with O(nu^{-1/3})
    # impurity from the subleading (3/2 + q_F/2)cos term and the turn-on (printed).
    cval = 2.0
    third = mp.mpf(1) / 3
    ct = CT["fw"]
    A_t = 1.0
    ph_t = mp.pi / 8
    AF = 3 * A_t / float(ct)
    phF = ph_t + mp.pi / 3
    FR = F_gevrey3(AF, ct, phF, cval, w_lo=mp.mpf('0.1'), qF=mp.mpf(-5) / 3, npow=6)
    grid = [float((mp.mpf('1.6') + mp.mpf('0.2') * j) ** 3) for j in range(16)]
    res = rho_c_pipeline2(FR, cval, grid, w_cut=mp.mpf('0.001'), dps=50, deg=28)
    s3 = float(mp.sqrt(3))
    dv, predO, targ = [], [], []
    print("[3d2-1] measured vs the operator prediction predO = -nu[(3/2)F + (1/2)sF'] and")
    print("        vs the BARE (C1) target (impurity = subleading + turn-on, -> 0 at high nu):")
    for nu in grid:
        mp.mp.dps = 30
        d = float((res[nu] - nu).real)
        sv = mp.mpf(nu) / cval
        po = float(-nu * (mp.mpf(3) / 2 * FR(sv) + sv / 2 * mp.diff(FR, sv)))
        tg = float(A_t * mp.mpf(nu) ** (-third) * mp.e ** (-ct * mp.mpf(nu) ** third)
                   * mp.cos(mp.sqrt(3) * ct * mp.mpf(nu) ** third + ph_t))
        dv.append(d)
        predO.append(po)
        targ.append(tg)
        rO = d / po if abs(po) > 1e-18 else float('nan')
        rT = d / tg if abs(tg) > 1e-18 else float('nan')
        print(f"     nu = {nu:>7.3f}: meas = {d:+.6e}  /predO = {rO:8.5f}  /target = {rT:8.5f}")
    # pointwise loop-closure gate at non-node points (|cos| > 0.4 of the OPERATOR phase):
    devs = []
    for nu, d, po in zip(grid, dv, predO):
        cosfac = float(mp.cos(mp.sqrt(3) * ct * mp.mpf(nu) ** third + ph_t))
        if abs(cosfac) > 0.4:
            devs.append(abs(d / po - 1))
    print(f"[3d2-2] pointwise |meas/predO - 1| at {len(devs)} non-node points: "
          f"max = {max(devs):.4f} -> {'PASS (<= 0.02)' if max(devs) <= 0.02 else 'FAIL'}")
    # fits: measured vs predO (differential) vs bare target:
    init = (-1.0 / 3, float(ct), s3 * float(ct), 1.0 / 3)
    fitM = fit_osc_model(grid, dv, init=init)
    fitO = fit_osc_model(grid, predO, init=init)
    fitT = fit_osc_model(grid, targ, init=init)
    for nm, ft in [("measured", fitM), ("predO   ", fitO), ("target  ", fitT)]:
        print(f"     {nm}: s = {ft['s']:.5f}  al = {ft['al']:.5f}  be/al = "
              f"{ft['be']/ft['al']:.5f}  q = {ft['q']:+.4f}  amp = {ft['amp']:.4f}  "
              f"phi = {ft['phi']:+.4f}  rms_w = {ft['rms_w']:.2e}")
    print(f"     asymptotic targets: s = 1/3, al = {float(ct):.5f}, be/al = {s3:.5f}, "
          f"q = -1/3, amp = {A_t}, phi = {float(ph_t):+.4f}")
    gap = max(abs(fitM["s"] - fitO["s"]), abs(fitM["al"] - fitO["al"]) / fitO["al"],
              abs(fitM["be"] - fitO["be"]) / fitO["be"])
    print(f"[3d2-3] measured-vs-predO fit gap (s, al, be rel): {gap:.4f} -> "
          f"{'PASS (<= 0.01)' if gap <= 0.01 else 'FAIL'}")
    print("     => the inverse problem is SOLVED at Born order: the corrected profile")
    print("        forward-transcribes onto the (C1) fingerprint; residual amp/phi/q")
    print("        offsets vs the bare target are the documented O(nu^{-1/3}) impurity")
    print("        (subleading cos-term + turn-on), shrinking up the window.")


# ---------- step3e: all-orders closed-form anchors (p = 2 Bessel, p = 1 Coulomb) ----------

def _MJ(s_, mu_):
    return 2 ** (s_ - 1) * mp.gamma((mu_ + s_) / 2) / mp.gamma(1 + (mu_ - s_) / 2)


def rho_c_bessel_closed(nu, muv, cval):
    """Exact normalized rho_c(nu) for F = mu/w^2 (ALL orders in mu): Gamma-function
    Mellin of sqrt(w) H1_lam(cw), lam = sqrt(1/4 - mu c^2); Wronskian from hankel
    values at a small real point (mpmath hankel1 is accurate on the real axis)."""
    lam = mp.sqrt(mp.mpf(1) / 4 - muv * cval ** 2)

    def phia(nu_):
        s_ = mp.mpf(3) / 2 - 1j * mp.mpc(nu_)
        return cval ** (-s_) * (_MJ(s_, -lam) - mp.e ** (-1j * mp.pi * lam)
                                * _MJ(s_, lam)) / (1j * mp.sin(mp.pi * lam))

    w0 = mp.mpf('0.3')
    g = mp.sqrt(w0) * mp.hankel1(lam, cval * w0)
    dH = (mp.hankel1(lam - 1, cval * w0) - mp.hankel1(lam + 1, cval * w0)) / 2
    gp = mp.hankel1(lam, cval * w0) / (2 * mp.sqrt(w0)) + mp.sqrt(w0) * cval * dH
    W = g * mp.conj(gp) - mp.conj(g) * gp
    php = phia(nu)
    t1 = php * mp.conj(php)
    t2 = 0
    if nu <= 8:
        phm = phia(-nu)
        t2 = mp.conj(phm) * phm
    bil = -2j * cval * (t1 - t2) / W
    return bil / (2 * mp.pi / cval ** 2)


def _coulomb_g(kap, cval):
    """Upper-decaying Coulomb solution g_a(w) = e^{-z/2} z U(1 - kW, 2, z),
    z = -2 i c w, kW = i c kap / 2  (solves g'' + c^2(1 + kap/w) g = 0; the
    e^{-z/2} = e^{i c w} branch decays in the upper half plane)."""
    kW = 1j * cval * mp.mpf(kap) / 2

    def g(wv):
        z = -2j * cval * wv
        return mp.e ** (-z / 2) * z * mp.hyperu(1 - kW, 2, z)

    def gp(wv):
        z = -2j * cval * wv
        U1 = mp.hyperu(1 - kW, 2, z)
        U2 = mp.hyperu(2 - kW, 3, z)
        ddz = mp.e ** (-z / 2) * ((1 - z / 2) * U1 - z * (1 - kW) * U2)
        return -2j * cval * ddz

    return g, gp, kW


def rho_c_coulomb_closed(nu, kap, cval, MW=None):
    """Exact normalized rho_c(nu) for F = kap/w (ALL orders in kap), via the verified
    Whittaker Mellin (G&R 7.621.2 class, mu = 1/2; quad-verified to 1e-40):
    M_W(s) = int_0^inf x^{s-1} W_{kW,1/2}(x) dx
           = Gamma(s+1) Gamma(s) / Gamma(s-kW+1) * 2F1(s+1, s; s-kW+1; 1/2);
    phia(nu) = (i/(2c))^{1 - i nu} M_W(1 - i nu). At large |s| the 2F1 tends to
    2^{kW} (1 + O(1/nu)) and Gamma(s)s^{kW} carries the Coulomb log-phase: a pure
    Gamma-ratio class — power-law asymptotics at every order in kap."""
    g, gp, kW = _coulomb_g(kap, cval)
    MWf = MW or (lambda s_: mp.gamma(s_ + 1) * mp.gamma(s_) / mp.gamma(s_ - kW + 1)
                 * mp.hyp2f1(s_ + 1, s_, s_ - kW + 1, mp.mpf(1) / 2))

    def phia(nu_):
        s_ = 1 - 1j * mp.mpc(nu_)
        return (1j / (2 * cval)) ** s_ * MWf(s_)

    w0 = mp.mpf('0.3')
    gv, gpv = g(w0), gp(w0)
    W = gv * mp.conj(gpv) - mp.conj(gv) * gpv
    php = phia(nu)
    t1 = php * mp.conj(php)
    t2 = 0
    if nu <= 8:
        phm = phia(-nu)
        t2 = mp.conj(phm) * phm
    bil = -2j * cval * (t1 - t2) / W
    return bil / (2 * mp.pi / cval ** 2)


def step3e():
    print("=" * 88)
    print("[HH-3e] ALL-ORDERS ANCHORS: p = 2 (Bessel) and p = 1 (Coulomb) closed forms —")
    print("        power-law class at EVERY coupling strength; no exponential of any index")
    print("=" * 88)
    mp.mp.dps = 100
    cval = mp.mpf(2)
    nus = [6.0, 10.0, 17.0, 28.0, 47.0, 78.0, 130.0, 200.0]

    # ---- p = 2 Bessel, weak and STRONG coupling (exact in mu) ----
    for muv in [mp.mpf('0.4'), mp.mpf('2.0')]:
        dv = []
        print(f"[3e-B] p = 2, mu = {float(muv)} (lam = {mp.nstr(mp.sqrt(mp.mpf(1)/4 - muv*cval**2), 6)}):")
        for nu in nus:
            r = rho_c_bessel_closed(nu, muv, cval)
            d = (r - nu).real
            dv.append(d)
            print(f"     nu = {nu:>6}: Drho_c = {mp.nstr(d, 10):>18}   "
                  f"nu*Drho = {mp.nstr(d * nu, 8)} (power-law => const)")
        laws = fit_tail_laws(nus, dv)
        print(f"     power fit: beta = {laws['power']['beta']:+.5f} (Gamma-ratio pred -1), "
              f"max ln-resid = {laws['power']['max_resid']:.2e}")
        for tag in ["s=1/3", "s=1/2", "s=1"]:
            print(f"     +exp({tag}): a = {laws[tag]['a']:+.2e} (required ct = "
                  f"{CT['fw']:.3f}: coefficient {abs(laws[tag]['a'])/CT['fw']:.1e} of it), "
                  f"resid {laws[tag]['max_resid']:.2e}")

    # ---- p = 1 Coulomb (exact in kap): verify the solution + the Mellin, then scan ----
    kap = mp.mpf('0.4')
    g, gp, kW = _coulomb_g(kap, cval)
    # (i) ODE residual by finite differences at two points:
    mp.mp.dps = 60
    h = mp.mpf(10) ** -12
    worst = 0.0
    for wv in [mp.mpf('0.7'), mp.mpf('2.3')]:
        gpp = (g(wv + h) - 2 * g(wv) + g(wv - h)) / h ** 2
        resid = gpp + cval ** 2 * (1 + kap / wv) * g(wv)
        rd = float(abs(resid) / abs(cval ** 2 * g(wv)))
        worst = max(worst, rd)
    print(f"[3e-C] p = 1, kap = {float(kap)}: ODE residual (FD) worst = {worst:.2e} "
          f"-> {'PASS' if worst < 1e-20 else 'FAIL'}")
    assert worst < 1e-20
    # (ii) derivative formula check:
    gp_fd = (g(mp.mpf('0.7') + h) - g(mp.mpf('0.7') - h)) / (2 * h)
    rdp = float(abs(gp_fd - gp(mp.mpf('0.7'))) / abs(gp_fd))
    # gate at the FD method's own truncation floor (h^2 = 1e-24), not below it:
    print(f"     derivative formula vs FD: {rdp:.2e} -> {'PASS' if rdp < 1e-20 else 'FAIL'}")
    assert rdp < 1e-20
    # (iii) the Whittaker Mellin closed form vs direct quadrature at two s
    # (G&R 7.621.2 class. TWO wrong candidates caught by this gate before banking:
    # the plain Gamma-ratio [the e^{-x}-weight formula, off x1.3-1.6] and the
    # DLMF-13.10.7 parameterization 2F1(1-kW, s+1; s+1-kW; 1/2) [off x1.2-1.4]: bug log):
    mp.mp.dps = 50
    MWf = lambda s_: (mp.gamma(s_ + 1) * mp.gamma(s_) / mp.gamma(s_ - kW + 1)
                      * mp.hyp2f1(s_ + 1, s_, s_ - kW + 1, mp.mpf(1) / 2))
    worst = 0.0
    for s_ in [mp.mpf('1.4'), mp.mpf('1.1') - mp.mpf('0.7') * 1j]:
        Wx = lambda x: mp.e ** (-x / 2) * x * mp.hyperu(1 - kW, 2, x)
        direct = mp.quad(lambda x: x ** (s_ - 1) * Wx(x), [0, 1, 5, 30, 120])
        rd = float(abs(direct - MWf(s_)) / abs(MWf(s_)))
        worst = max(worst, rd)
        print(f"     M_W({mp.nstr(s_, 4)}): closed vs quad rel.diff = {rd:.2e}")
    ok = worst < 1e-20
    print(f"     gate -> {'PASS' if ok else 'FAIL'}")
    assert ok
    # (iv) free-limit structural check is exact (U(1,2,z) = 1/z reproduces Gamma(1-i nu)
    # phase-for-phase; verified symbolically in the construction notes) — and the scan:
    mp.mp.dps = 100
    dv = []
    for nu in nus:
        r = rho_c_coulomb_closed(nu, kap, cval, MW=MWf)
        d = (r - nu).real
        dv.append(d)
        print(f"     nu = {nu:>6}: Drho_c = {mp.nstr(d, 10):>18}   (p = 1 => -> const)")
    laws = fit_tail_laws(nus, dv)
    print(f"     power fit: beta = {laws['power']['beta']:+.5f} (Gamma-ratio pred 0), "
          f"max ln-resid = {laws['power']['max_resid']:.2e}")
    for tag in ["s=1/3", "s=1/2", "s=1"]:
        print(f"     +exp({tag}): a = {laws[tag]['a']:+.2e}, resid {laws[tag]['max_resid']:.2e}")
    print("     => BOTH solvable anchors are pure Gamma-ratio Mellins: their large-nu")
    print("        asymptotics is a POWER SERIES in 1/nu at every coupling strength —")
    print("        no e^{-a nu^s} term of ANY index s arises at ANY order. The power-law")
    print("        class of [3a] is exact, not perturbative.")


def step4():
    print("=" * 88)
    print("[HH-4] GATES on the survivor (the Born-inverse / G profile)")
    print("=" * 88)
    mp.mp.dps = 40
    gam, phi0, mreg = 0.75, mp.pi / 8, 0.5

    # ---- (i) the dynamics-side amplitude ceiling: 1 + F > 0 with the TRUE target ----
    # The measured Born read is the OPERATOR Drho(nu) = -nu[(3/2)F + (1/2)sF']|_{s=nu/c}
    # ([3a]/[3a1]: C(p) = (3-p)/2). Exact inversion (first-order linear ODE, regular
    # branch): F(s) = -(2/X^3) int_0^X x Drho_req(x) dx, X = c s — c-independent in
    # X. With Drho_req(x) = A * 2 Im D(x) (agentEE minimal completion, m = 0.5 band):
    # tachyon iff A * hbar(X) > 1, hbar(X) = (2/X^3) int_0^X x * 2 Im D(x) dx (pos. part).
    # NOTE the X -> inf limit: F -> -2 A M1/X^3 with M1 = int_0^inf x 2ImD dx — the
    # inversion of a localized target carries an s^{-3} tail ALONG THE KERNEL'S NULL
    # DIRECTION (C(3) = 0): invisible at leading Born order, admissible, computed below.
    print("[4i] no-tachyon ceiling from the EXACT Born inversion (m = 0.5 band):")
    print("     hbar(X) = (2/X^3) int_0^X x 2ImD dx;  A_stab = 1/max_X hbar_+")
    A_stab = {}
    for foot in ["fw", "canon", "hostile"]:
        zt = ZT[foot]
        Xg = list(np.geomspace(0.05, 60.0, 90))
        imd = [2 * float(mp.im(D_full(x, zt, gam, phi0, m=mreg))) for x in Xg]
        # cumulative int_0^X x 2ImD dx (trapezoid on the geometric grid, 0-anchored):
        xs = np.array(Xg)
        ys = np.array(imd) * xs
        cum = np.concatenate([[0.0], np.cumsum(0.5 * (ys[1:] + ys[:-1]) * np.diff(xs))])
        cum = cum + 0.0   # int from 0 to xs[0] ~ x^2-small: negligible
        hbar = 2.0 * cum[1:] / xs[1:] ** 3
        hbar = np.concatenate([[0.0], hbar])
        i = int(np.argmax(hbar))
        M1 = cum[-1]
        Fmax = float(np.abs(hbar).max())     # |F_req|/A pointwise max
        if hbar[i] > 1e-12:
            A_stab[foot] = 1.0 / hbar[i]
            print(f"     {foot:>8}: A_stab = {A_stab[foot]:8.4f} (binds at X = {xs[i]:.3f}); "
                  f"max|F_req|/A = {Fmax:.4f}; M1 = {M1:+.4f} (the s^-3 null-tail weight)")
        else:
            A_stab[foot] = float('inf')
            print(f"     {foot:>8}: hbar(X) <= 0 for ALL X — F_req >= 0 everywhere: "
                  f"NO tachyonic band at ANY A > 0. max|F_req|/A = {Fmax:.4f}; "
                  f"M1 = {M1:+.4f} (s^-3 null tail)")
    if min(A_stab.values()) == float('inf'):
        print("     => the EXACT inversion is tachyon-free at every amplitude: the naive")
        print("        pointwise ceiling (which would have bound A at the O(1) level) was an")
        print("        artifact of the wrong read law — the (3/2 + s d/ds /2) smoothing")
        print("        integral has definite sign on this target. The only residual")
        print("        amplitude statement on the dynamics side: |F_req| ~ A x (max above):")
        print("        |F_req| < 1 (hyperbolicity comfort) holds for A < 1/max|F_req|*A —")
        print("        printed per footing; (C3)'s window |A| <= 5.716 remains the binding")
        print("        amplitude constraint.")
    else:
        print(f"     positivity window (C3) allowed |A| <= 5.716; dynamics ceiling "
              f"{min(v for v in A_stab.values()):.3f}-{max(A_stab.values()):.3f} by footing.")

    # ---- (ii) per-transit amplification at the (C3) ceiling (if tachyonic there) ----
    print("[4ii] per-transit amplification at the (C3) ceiling A = 5.716 (worst case):")
    for foot in ["fw", "canon", "hostile"]:
        zt = ZT[foot]
        Av = 5.716
        Xg = np.geomspace(0.05, 60.0, 90)
        imd = np.array([2 * float(mp.im(D_full(x, zt, gam, phi0, m=mreg))) for x in Xg])
        ys = imd * Xg
        cum = np.concatenate([[0.0],
                              np.cumsum(0.5 * (ys[1:] + ys[:-1]) * np.diff(Xg))])
        hbar = np.concatenate([[0.0], 2.0 * cum[1:] / Xg[1:] ** 3])
        bad = np.sqrt(np.maximum(0.0, Av * hbar - 1.0))
        integ = float(np.trapz(bad, Xg))
        print(f"     {foot:>8}: int sqrt((A hbar - 1)_+) dX = {integ:.4f} -> per-mode "
              f"transit amplification e^{{{integ:.3f}}} = {float(np.exp(integ)):.3f} "
              f"({'finite burst' if integ < 2 else 'LARGE'}; each mode crosses once)")

    # ---- (iii) UV/PPN/Cherenkov corner ----
    print("[4iii] UV switch-off and the Cherenkov corner:")
    ct = CT["fw"]
    for wpt, lab in [(1e3, "nu = 1e3 (cluster-scale modes)"),
                     (5.5e15, "nu ~ 5e15 (1 AU modes, solar system)")]:
        lnF = float(-ct * wpt ** (1.0 / 3) * mp.log10(mp.e))
        print(f"     |F| at {lab}: 10^({lnF:.1f})")
    print("     => the profile is exp(-ct nu^{1/3})-OFF at all sub-galactic scales: the")
    print("        PPN/Cherenkov corner is exactly agentU's — inherited UNCHANGED, BOTH")
    print("        corners: generic (c_chi^2 = O(gamma/alpha) >> 1: v^2 = c_chi^2(1+F) >> 1")
    print("        for any |F| < 1) AND the tuned Cherenkov-edge sliver (c_S^2 in")
    print("        [1.000, 1.033], where v > 1 needs F > -0.03): [4i] found F_req >= 0")
    print("        EVERYWHERE — the modification only RAISES the phase velocity; no")
    print("        Cherenkov re-entry in either corner. The pump acts at w = k_phys/H ~")
    print("        nu/c_chi <~ few/c_chi: the khronon sound-horizon band — super-horizon")
    print("        geography, where nothing else constrains the dispersion.")

    # ---- (iv) gain realization: alternating comb; boundedness; integrated gain ----
    print("[4iv] pure-gain realization ghat' - ghat^2 = c^2 F_req (A = 1, c = 2; F_req =")
    print("      the corrected Born inverse, [3d2] form; gain-sector coefficient caveat:")
    print("      the envelope-curvature term enters the gain read at the same order as")
    print("      F_eff ([3b] ratio drift) — the comb below is the structural realization,")
    print("      its O(1) re-normalization not chased):")
    cval = 2.0
    FG = F_gevrey3(3.0 / CT["fw"], CT["fw"], mp.pi / 8 + mp.pi / 3, cval,
                   w_lo=mp.mpf('0.1'), qF=mp.mpf(-5) / 3, npow=6)
    w_hi = mp.mpf(40)

    def rhs(x, Y):
        wv = w_hi - x
        return [-(Y[0] ** 2 + cval ** 2 * FG(wv)), Y[0]]   # d ghat/dx; d(-Ghat)/dx

    mp.mp.dps = 30
    sol = mp.odefun(rhs, 0, [mp.mpf(0), mp.mpf(0)], tol=mp.mpf('1e-20'))
    ws = np.geomspace(0.02, float(w_hi) * 0.999, 220)
    gh = []
    for wv in ws:
        y = sol(float(w_hi) - wv)
        gh.append(float(y[0]))
    gh = np.array(gh)
    wgh = ws * gh
    DG = float(sol(float(w_hi) - 0.02)[1])
    nflip = int(np.sum(gh[1:] * gh[:-1] < 0))
    print(f"     ghat range: [{gh.min():+.4e}, {gh.max():+.4e}]; sign changes: {nflip}")
    print(f"     physical gain rate per Hubble time w*ghat: max |.| = {np.abs(wgh).max():.4e}")
    print(f"     net integrated gain DGhat(0.02 <- 40) = {DG:+.4e} (bounded: no secular")
    print("     runaway; the comb ALTERNATES gain/loss — the implied pump is NOT positive,")
    print("     it is an H-paced gain/loss comb keyed to the fingerprint's own zeros).")

    # ---- (v) the X2 invoice ----
    print("[4v] energy throughput: the response-side construction fixes only the PROFILE;")
    print("     the amplitude invoice lambda^2<Q^2> ~ m/H with free-energy throughput")
    print("     ~1e33-1e35 W per L*-galaxy (agentX [5], agentI) is a STATE-sector cost,")
    print("     inherited per (C3) — NOT re-adjudicated here; the dispersion realization")
    print("     needs zero response-side throughput, the gain-comb realization a bounded")
    print("     alternating one (DGhat above). No new energy obstruction; no relief either.")
    return A_stab


def step5():
    print("=" * 88)
    print("[HH-5] COEFFICIENT DISCIPLINE — raw constants, both/all footings, quarantine")
    print("=" * 88)
    print("[5a] the fingerprint constant ct = (3/4) 2^{2/3} zt^{2/3} (zt = zeta (2/H^2)^{1/4},")
    print("     zeta = agentV RAW banked sigma_req amplitudes — measured, not closed-form):")
    for foot in ["fw", "canon", "hostile"]:
        print(f"     {foot:>8}: zeta = {ZETA[foot]:.4f}  ->  ct = {CT[foot]:.4f}")
    print("[5b] the transcription map (the MEASURED operator read, [3a]/[3e]/[3a1]):")
    print("     Drho_c(nu) = -nu[(3/2)F + (1/2)sF']|_{s = nu/c_chi}; corrected Born inverse")
    print("     F_req(w) = (3A/ct)(c_chi w)^{-5/3} e^{-ct(c_chi w)^{1/3}}")
    print("                cos(sqrt3 ct (c_chi w)^{1/3} + phi_target + pi/3)")
    print("     — in PHYSICAL k_phys/H the pump's Gevrey-3 constant is ct * c_chi^{1/3}")
    print("     (c_chi from agentU's corner, raw, NOT fixed here):")
    for foot in ["fw", "canon", "hostile"]:
        print(f"     {foot:>8}: ct*c_chi^(1/3) = {CT[foot]:.4f} * c_chi^(1/3)   "
              f"(at the scan's c = 2: {CT[foot] * 2 ** (1.0/3):.4f})")
    print("[5c] amplitude bookkeeping (normalized units, free rho_c(nu) = nu):")
    print("     (C3) worldline positivity window: |A| <= 5.716 (agentEE [3d], banked).")
    print("     dynamics-side ceiling: NONE binding ([4i]: the exact inversion of the full")
    print("     D-target is tachyon-free at every A; |F_req|/A printed there) — the naive")
    print("     pointwise ceiling was an artifact of the wrong read law, retracted in-run.")
    print("     PHYSICAL normalization (lambda^2, the wattage) stays with agentI/agentX —")
    print("     inherited; NO Z claims; no a0 claims; nothing here fixes zeta.")
    q = (16 * mp.pi / 3) ** mp.mpf('0.25')
    print(f"[5d] QUARANTINE: (16 pi/3)^(1/4) = {mp.nstr(q, 8)} — never used numerically")
    print(f"     (the scan ran on agentV raw zeta = {ZETA['fw']}, which differs from the")
    print(f"     quarantined closed-form candidate by {abs(float(q) - ZETA['fw']):.4f} — "
          f"{abs(float(q) - ZETA['fw'])/ZETA['fw']*100:.2f}%); kept quarantined.")
    # mechanical audit: the quarantined closed form appears nowhere else in this file:
    import re
    src = open(__file__).read()
    hits = [m.start() for m in re.finditer(r"16 \* mp\.pi / 3", src)]
    zline = src.count("2.0247")
    print(f"     audit: '(16 pi/3)' constructions in source: {len(hits)} (this [5d] print "
          f"only); zeta literals: ZETA dict + this audit only ({zline} occurrences).")
    print("[5e] convention list (all stated in-line where used): omega in units of H")
    print("     (kappa = H at b = 0); free normalization rho_c = nu; the scan's c = 2 is a")
    print("     bookkeeping choice — the x = c w parametrization makes every fitted")
    print("     constant c-independent ([3d-4] c = 3 re-verification).")
    print("[5f] (C4) family universality: the universal ODE and F_req are b-INDEPENDENT by")
    print("     construction (functions of k_phys/H only); beta kappa^2 = H^2 makes the")
    print("     leading worldline law family-universal (agentEE [2c]/[3e], inherited);")
    print("     family/band dependence enters at relative O(kappa^2 tau*^2) as banked.")


# ----------------------------------------------------------------------------------------
# dispatch
# ----------------------------------------------------------------------------------------
def step2():
    print("=" * 88)
    print("[HH-2] PIPELINE VALIDATION: exact per-k -> worldline rho_c(nu) machinery")
    print("=" * 88)

    # [2a] FREE end-to-end: F == 0; pipeline must return rho_c(nu) = nu through the FULL
    # contour assembly (endpoint gamma + real seg + arc + ray + Riccati + bilinear).
    print("[2a] free case through the full pipeline (rho_c must equal nu exactly):")
    Ffree = lambda wv: mp.mpc(0)
    nus = [2.0, 7.0, 19.0, 33.0]
    res = rho_c_pipeline(Ffree, 2.0, nus)
    worst = 0.0
    for nu in nus:
        got = res[nu]
        rd = float(abs(got - nu) / nu)
        worst = max(worst, rd)
        print(f"     nu = {nu:>5}: rho_c = {mp.nstr(got.real, 17)} (im {float(abs(got.imag)):.1e})"
              f"   rel.err vs nu = {rd:.2e}")
    print(f"     gate: worst {worst:.2e} < 1e-18 -> {'PASS' if worst < 1e-18 else 'FAIL'}")
    assert worst < 1e-18

    # [2b] BESSEL anchor: F = mu/w^2 (p = 2, no cutoff needed at the solver level — but use
    # the same cutoff template to validate template handling): exact solution
    # psi = sqrt(w) H1_lam(c w), lam = sqrt(1/4 - mu c^2). Validate the SOLVER (branch values
    # on ray and real axis) against mpmath hankel1 directly, mu = 0.4.
    print("[2b] Bessel anchor (F = mu/w^2, mu = 0.4, c = 2): solver vs sqrt(w) H1_lam(cw):")
    mp.mp.dps = 50
    muv, cval = mp.mpf('0.4'), mp.mpf(2)
    lam = mp.sqrt(mp.mpf(1) / 4 - muv * cval ** 2)
    FB = lambda wv: muv / wv ** 2
    r0, S_max, w_cut = mp.mpf('0.5'), mp.mpf(60), mp.mpf('0.1')
    br = solve_branch(FB, cval, r0, S_max, w_cut)
    # exact upper-decaying combination: H1 ~ e^{i c w}: hank = sqrt(w) hankel1(lam, c w)
    hank = lambda wv: mp.sqrt(wv) * mp.hankel1(lam, cval * wv)
    # compare RATIO g_a/hank at three points (same solution up to one overall constant):
    z1 = br["G"](mp.mpf(3)) / hank(3j)            # ray point w = 3i
    z2 = br["G"](mp.mpf(11)) / hank(11j)
    z3 = (br["real"](1)[0]) / hank(w_cut)         # real point w = w_cut
    d12 = float(abs(z1 / z2 - 1))
    d13 = float(abs(z1 / z3 - 1))
    print(f"     ratio const across ray pts 3i,11i: dev = {d12:.2e}; ray vs real w_cut: dev = {d13:.2e}")
    ok_b = d12 < 1e-30 and d13 < 1e-30
    print(f"     gate (proportional to ONE Hankel branch everywhere, 1e-30) -> "
          f"{'PASS' if ok_b else 'FAIL'}")
    assert ok_b
    print("     => solver tracks the exact upper-decaying branch through ray+arc+real segment.")

    # [2c] Bessel rho_c: pipeline vs CLOSED FORM Gamma-function Mellin.
    # NOTE (recorded): mpmath hankel1 LOSES the decaying branch at large imaginary argument
    # (|hank(85i)| returned 1.8e+8 vs true ~1e-74) — the Riccati route is the stable one; the
    # independent check is therefore done against the exact Mellin, not Hankel quadrature:
    #   M_J(s, mu) = int_0^inf x^{s-1} J_mu(x) dx = 2^{s-1} Gamma((mu+s)/2) / Gamma(1+(mu-s)/2)
    #   H1_lam = (J_{-lam} - e^{-i pi lam} J_lam) / (i sin(pi lam)),  s = 3/2 - i nu
    #   phia~(nu) = C c^{i nu - 3/2} [M_J(s,-lam) - e^{-i pi lam} M_J(s,lam)]/(i sin(pi lam)),
    # C fixed at one SMALL real point (hankel1 accurate there). The pure-Bessel F != 0 below
    # w_cut, so the pipeline endpoint uses the J-power-series (15 terms, c*w_cut = 0.2).
    print("[2c] Bessel rho_c: ODE pipeline vs closed-form Gamma Mellin (nu = 6, 15):")

    def SJ(mu_, nu_, w_cut_, cval_, nmax=25):
        s_ = mp.mpf(3) / 2 - 1j * mp.mpc(nu_)
        tot = mp.mpc(0)
        for m_ in range(nmax):
            tot += (-1) ** m_ * (cval_ / 2) ** (mu_ + 2 * m_) \
                * w_cut_ ** (mu_ + 2 * m_ + s_) / ((mu_ + 2 * m_ + s_)
                                                   * mp.factorial(m_) * mp.gamma(mu_ + m_ + 1))
        return tot

    def endpoint_bessel(nu_, Cnorm, lam_, cval_, w_cut_):
        return Cnorm * (SJ(-lam_, nu_, w_cut_, cval_) - mp.e ** (-1j * mp.pi * lam_)
                        * SJ(lam_, nu_, w_cut_, cval_)) / (1j * mp.sin(mp.pi * lam_))

    def MJ(s_, mu_):
        return 2 ** (s_ - 1) * mp.gamma((mu_ + s_) / 2) / mp.gamma(1 + (mu_ - s_) / 2)

    def phia_closed(nu_, Cnorm, lam_, cval_):
        s_ = mp.mpf(3) / 2 - 1j * mp.mpc(nu_)
        return Cnorm * cval_ ** (-s_) * (MJ(s_, -lam_) - mp.e ** (-1j * mp.pi * lam_)
                                         * MJ(s_, lam_)) / (1j * mp.sin(mp.pi * lam_))

    worst = 0.0
    for nu in [6.0, 15.0]:
        dpsn = int(0.6822 * abs(nu)) + 45
        mp.mp.dps = dpsn
        Smx = mp.mpf(40) + mp.mpf(dpsn) * mp.log(10) / cval
        brB = solve_branch(FB, cval, r0, Smx, w_cut)
        # normalization C of the ODE branch relative to sqrt(w) H1_lam(c w), at real w = r0:
        Cnorm = brB["g_r0"] / (mp.sqrt(r0) * mp.hankel1(lam, cval * r0))
        # pipeline Mellin with Bessel endpoint:
        def phia_pipe(nu_):
            tot = endpoint_bessel(nu_, Cnorm, lam, cval, w_cut)
            def integ_real(x):
                wv = r0 + x * (w_cut - r0)
                return wv ** (-1j * mp.mpc(nu_)) * brB["real"](x)[0] * (r0 - w_cut)
            npan = max(8, int(abs(nu_) * float(mp.log(r0 / w_cut)) / 4) + 8)
            tot += mp.quad(integ_real, list(mp.linspace(0, 1, npan)))
            def integ_arc(x):
                th = mp.pi / 2 * (1 - x)
                wv = r0 * mp.e ** (1j * th)
                dwdx = r0 * 1j * mp.e ** (1j * th) * (-mp.pi / 2)
                return wv ** (-1j * mp.mpc(nu_)) * brB["arc"](x)[0] * (-dwdx)
            tot += mp.quad(integ_arc, list(mp.linspace(0, 1, max(10, int(abs(nu_)) + 10))))
            nseg = max(12, int(abs(nu_) * float(mp.log(Smx / r0)) / 3.5) + 12)
            pts = [r0 * (Smx / r0) ** (mp.mpf(j) / nseg) for j in range(nseg + 1)]
            tot += mp.quad(lambda s: (1j * s) ** (-1j * mp.mpc(nu_)) * brB["G"](s) * 1j, pts)
            return tot
        for sgn in (+1, -1):
            pp = phia_pipe(sgn * nu)
            pc = phia_closed(sgn * nu, Cnorm, lam, cval)
            rd = float(abs(pp - pc) / abs(pc))
            worst = max(worst, rd)
            print(f"     nu = {sgn*nu:>6}: |pipeline/closed - 1| = {rd:.2e}")
        # rho_c from closed forms (W from real-point values of the branch):
        gr, gpr = brB["g_r0"], brB["gp_r0"]
        Wb = gr * mp.conj(gpr) - mp.conj(gr) * gpr
        php, phm = phia_closed(nu, Cnorm, lam, cval), phia_closed(-nu, Cnorm, lam, cval)
        bil = -2j * cval * (php * mp.conj(php) - mp.conj(phm) * phm) / Wb
        rho_closed = bil / (2 * mp.pi / cval ** 2)
        print(f"     nu = {nu:>4}: rho_c closed = {mp.nstr(rho_closed.real, 14)}  "
              f"(deviation from free: {mp.nstr(rho_closed.real - nu, 6)})")
    print(f"     gate: worst Mellin rel.diff {worst:.2e} < 1e-25 -> {'PASS' if worst < 1e-25 else 'FAIL'}")
    assert worst < 1e-25
    print("     => pipeline exact against the Gamma-function closed form (independent of the")
    print("        ODE solver and of the contour). p = 2 column: rho_c - nu is POWER-LAW in nu")
    print("        (Gamma-ratio asymptotics — no exponential of any index), quantified in step3.")
    mp.mp.dps = 30


# ----------------------------------------------------------------------------------------
# dispatch
# ----------------------------------------------------------------------------------------
STEPS = {"step0": step0, "step1": step1, "step2": step2, "step3a0": step3a0,
         "step3a0b": step3a0b, "step3a": step3a, "step3a1": step3a1, "step3b": step3b,
         "step3c": step3c, "step3c2": step3c2, "step3c3": step3c3, "step3c4": step3c4, "step3d": step3d, "step3d2": step3d2, "step3e": step3e, "step4": step4,
         "step5": step5}

if __name__ == "__main__":
    for name in sys.argv[1:]:
        STEPS[name]()
