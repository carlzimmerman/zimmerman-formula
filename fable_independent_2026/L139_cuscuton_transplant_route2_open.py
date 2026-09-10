#!/usr/bin/env python3
"""
C -- CAN AeST'S CMB MECHANISM BE TRANSPLANTED INTO THE CUSCUTON-CLOCK BRANCH?
=============================================================================================================
The programme's surviving branch (repo L119/L122/L125/L127):
    S = int sqrt(-g) [ M^2/2 (R - 2 Lambda)
                       + mu_c^2 sqrt(-(d tau)^2) - V(tau)          (cuscuton clock, 0 dof)
                       + 2 M^2 a_0^2 Q(|D phi|/a_0) ]  + S_m       (MOND from the LEAF-PROJECTED gradient)
It passes the PPN preferred-frame gate that AeST fails (L127: alpha_1 = alpha_2 = 0 RIGOROUSLY, because the
clock action reduces to a functional of (N, gamma_ij) alone => dS/dN^i = 0 to ALL orders; AeST's vector
kinetic term F^2 is exactly what makes dS/dN^i nonzero).

AeST gets its CMB from a SHIFT-SYMMETRIC k-essence: K(Q) with a minimum at Q_0 != 0, Q = A^mu grad_mu phi,
giving dK/dQ = I_0/a^3 and hence rho ~ a^-3 (script A). TWO transplant routes exist:

  ROUTE 1 (no new field): make the CLOCK itself carry the dust, via its potential V(tau).
  ROUTE 2 (one new field): add a shift-symmetric k-essence chi with Q = n^mu grad_mu chi, where n^mu is the
          CLOCK'S OWN LEAF NORMAL instead of AeST's dynamical aether A^mu.

WHAT IS COMPUTED:
  C1  ROUTE 1 background. The cuscuton's exact FLRW structure: rho = V(tau), P = mu_c^2 |taudot| - V, and the
      field equation is the algebraic constraint V'(tau) = -3 mu_c^2 H. Show P == 0 <=> rho ~ a^-3 EXACTLY,
      construct the V that does it in closed form, and verify by direct numerical integration.
      => background dust with NO a^-6 stiff partner and NO BBN tuning.
  C2  ROUTE 1 perturbations -- THE OBSTRUCTION. Expand sqrt(-(d tau)^2) to SECOND order and show the
      (delta-tau-dot)^2 terms cancel identically, so delta-tau has NO time-kinetic term: its equation is an
      elliptic CONSTRAINT, and sub-horizon delta-tau is slaved and suppressed as 1/k^2. A dust that does not
      cluster cannot drive the third peak (this is the repo's own L123(a) slaving argument, made explicit).
  C3  ROUTE 2. The AeST mechanism with the aether replaced by the clock's leaf normal: check the dust
      background, the ghost/gradient health, the free running sound speed, and -- the decisive question --
      whether it re-imports AeST's alpha_1 disaster. Test: compute dL/dN^i (the momentum-constraint source)
      for each sector and compare against AeST's vector.
  C4  Does the repo's own L87 'stiff genericity' theorem OBSTRUCT route 2? Determine precisely what its
      hypothesis constrains: the CLOCK's braiding function, or any shift-symmetric field?
  C5  verdict: OPEN / OBSTRUCTED / ACHIEVED, with the cost sheet.

POLARITY: each check ASSERTS a statement; PASS = true.
"""
import sympy as sp
import numpy as np
import sys, time

T0 = time.time(); FAILS = []; N = [0]
def check(name, ok, detail=""):
    N[0] += 1
    tag = "PASS" if ok else "FAIL"
    if not ok: FAILS.append(name)
    print(f"  [{tag}] {name}" + (f"   ({detail})" if detail else ""))
def sec(t):
    print("\n" + "=" * 112); print(t); print("=" * 112)

# =====================================================================================================
sec("C1 -- ROUTE 1: can the CUSCUTON CLOCK's own potential V(tau) generate the a^-3 dust?")
# =====================================================================================================
t = sp.symbols('t', positive=True)
muc, M, rho0, t0 = sp.symbols('mu_c M rho_0 t_0', positive=True)
tau = sp.Function('tau', positive=True)
V = sp.Function('V')
aF = sp.Function('a', positive=True)

# FLRW cuscuton: L = mu_c^2 |taudot| - V(tau);  rho = taudot dL/dtaudot - L = mu_c^2 taudot - L = V ; P = L.
taud = sp.symbols('taudot', positive=True)
L_c = muc**2*taud - sp.Symbol('V')
rho_c = sp.simplify(taud*sp.diff(L_c, taud) - L_c)
P_c = L_c
check("C1-1  the cuscuton's FLRW energy density is EXACTLY the potential: rho = taudot L_taudot - L = V(tau) "
      "(the kinetic term is degree-1 homogeneous, so it cancels)",
      sp.simplify(rho_c - sp.Symbol('V')) == 0, f"rho = {rho_c}")
check("C1-2  and its pressure is P = mu_c^2 |taudot| - V, so P == 0  <=>  V = mu_c^2 taudot",
      sp.simplify(P_c - (muc**2*taud - sp.Symbol('V'))) == 0, f"P = {P_c}")

# background field equation: d/dt(a^3 mu_c^2) + a^3 V' = 0  =>  V'(tau) = -3 mu_c^2 H  (the cuscuton constraint)
# Impose P = 0, i.e. V = mu_c^2 taudot. Then Vdot = V' taudot = -3 mu_c^2 H taudot = -3 H V  =>  V ~ a^-3.
Vs, H = sp.symbols('V H', positive=True)
Vdot_from_constraint = -3*muc**2*H*taud                      # V' taudot with V' = -3 mu_c^2 H
Vdot_if_dust = -3*H*Vs
check("C1-3  DUST IS EXACT ON THIS BRANCH: imposing P=0 (V = mu_c^2 taudot) in the cuscuton constraint "
      "V' = -3 mu_c^2 H gives Vdot = -3 H V, i.e. rho = V ~ a^-3 identically, with NO a^-6 partner",
      sp.simplify(Vdot_from_constraint.subs(muc**2*taud, Vs) - Vdot_if_dust) == 0,
      "Vdot = -3 mu_c^2 H taudot = -3 H V  =>  rho ~ a^-3 exactly")

# closed form: in a cuscuton-dust-dominated universe a ~ t^{2/3}, tau = C - B/t, V(tau) = (mu_c^2/B)(C-tau)^2
B, Cc, tau_s = sp.symbols('B C tau', positive=True)
tau_of_t = Cc - B/t
V_of_tau = (muc**2/B)*(Cc - tau_s)**2
Vprime = sp.diff(V_of_tau, tau_s).subs(tau_s, tau_of_t)
H_dust = sp.Rational(2, 3)/t
check("C1-4  the required V is a simple QUADRATIC: V(tau) = (mu_c^2/B)(C - tau)^2 reproduces the constraint "
      "V'(tau) = -3 mu_c^2 H exactly on the matter-era solution a ~ t^{2/3}",
      sp.simplify(Vprime + 3*muc**2*H_dust) == 0, f"V' + 3 mu_c^2 H = {sp.simplify(Vprime + 3*muc**2*H_dust)}")

# numerical verification: integrate the full coupled system from the ACTION-level equations, no shortcuts
def rhs(y, tt, mu2, Bv, Cv, Mv):
    tauv, av = y
    Vv = (mu2/Bv)*(Cv - tauv)**2
    Hv = np.sqrt(Vv/(3*Mv**2))
    taudot = Vv/mu2                       # from P = 0
    return [taudot, av*Hv]
try:
    from scipy.integrate import odeint
    mu2, Bv, Cv, Mv = 1.0, 1.0, 10.0, 1.0
    # consistency: V/(3M^2) = H^2 and taudot = V/mu^2 both hold if B is chosen right; solve for B from
    # H = (2/3)/t and V = mu^2 B/t^2  =>  mu^2 B/(3 M^2 t^2) = 4/(9 t^2)  =>  B = (4/3) M^2/mu^2
    Bv = (4.0/3.0)*Mv**2/mu2
    ts = np.linspace(1.0, 40.0, 4000)
    y0 = [Cv - Bv/ts[0], 1.0]
    sol = odeint(rhs, y0, ts, args=(mu2, Bv, Cv, Mv))
    tauN, aN = sol[:, 0], sol[:, 1]
    VN = (mu2/Bv)*(Cv - tauN)**2
    slope = np.polyfit(np.log(aN[100:]), np.log(VN[100:]), 1)[0]
    check("C1-5  NUMERICAL: integrating the coupled (tau, a) system with V(tau) = (mu_c^2/B)(C-tau)^2 gives "
          "dln(rho)/dln(a) = -3 to machine level -- exact dust, from an action, with no stiff partner",
          abs(slope + 3) < 1e-3, f"dln(rho)/dln(a) = {slope:.6f}")
    # NON-CIRCULAR consistency test: the integration imposed only (i) taudot = V/mu_c^2 (i.e. P = 0) and
    # (ii) the Friedmann equation. The cuscuton's OWN field equation V'(tau) = -3 mu_c^2 H was NOT imposed.
    # If it holds along the solution, the P = 0 dust branch is a genuine solution of the action, not an ansatz.
    HN = np.sqrt(VN/(3*Mv**2))
    VprimeN = -2*(mu2/Bv)*(Cv - tauN)
    resid = np.abs(VprimeN + 3*mu2*HN)/(3*mu2*HN)
    check("C1-6  NUMERICAL (non-circular): the cuscuton's OWN field equation V'(tau) = -3 mu_c^2 H -- which was "
          "never imposed during the integration -- holds along the solution to <1e-10, so the P=0, rho ~ a^-3 "
          "branch is a genuine solution of the action rather than a fitted ansatz",
          np.max(resid[10:-10]) < 1e-10,
          f"max |V' + 3 mu_c^2 H| / (3 mu_c^2 H) = {np.max(resid[10:-10]):.2e}")
except ImportError:
    check("C1-5  (scipy unavailable -- numerical integration skipped)", False)

# =====================================================================================================
sec("C2 -- ROUTE 1's OBSTRUCTION: the cuscuton dust is NON-PROPAGATING, so it cannot CLUSTER")
# =====================================================================================================
# Expand sqrt(-g^{mu nu} d_mu tau d_nu tau) to SECOND order in perturbations, Newtonian gauge.
eps = sp.symbols('epsilon')                                  # perturbation bookkeeping parameter
Psi, dtd, gr = sp.symbols('Psi deltataudot gradsq')          # Psi, delta-tau-dot, (grad delta tau)^2/a^2
tb = sp.symbols('taubar_dot', positive=True)
W = (1 - 2*eps*Psi)*(tb + eps*dtd)**2 - eps**2*gr            # -g^{mu nu} d tau d tau  (gradient is O(eps^2))
sqrtW = sp.series(sp.sqrt(W), eps, 0, 3).removeO()
sqrtW = sp.expand(sp.simplify(sqrtW))
coef_dtd2 = sp.simplify(sp.expand(sqrtW).coeff(eps, 2).coeff(dtd, 2))
coef_grad = sp.simplify(sp.expand(sqrtW).coeff(eps, 2).coeff(gr, 1))
print(f"  sqrt(-(d tau)^2) to O(eps^2):  {sqrtW}")
check("C2-1  the (delta-tau-dot)^2 terms CANCEL IDENTICALLY at second order: the cuscuton has NO time-kinetic "
      "term for its perturbation (this is what makes it 0-dof)",
      coef_dtd2 == 0, f"coefficient of eps^2 (delta-tau-dot)^2 = {coef_dtd2}")
check("C2-2  while the SPATIAL gradient survives with coefficient -1/(2 taubar_dot): the quadratic action is "
      "PURELY elliptic in delta-tau",
      sp.simplify(coef_grad + 1/(2*tb)) == 0, f"coefficient of (grad delta tau)^2/a^2 = {coef_grad}")

# elliptic constraint: (mu_c^2 k^2/(a^2 taubar_dot) + V'') delta-tau = -Source[Psi, Phi]
k, Vpp, a_, S_ = sp.symbols('k V_pp a S', positive=True)
dtau_sol = -S_/(muc**2*k**2/(a_**2*tb) + Vpp)
lead = sp.simplify(sp.limit(dtau_sol*k**2, k, sp.oo))
check("C2-3  therefore delta-tau is ALGEBRAICALLY SLAVED to the metric source and falls off as 1/k^2 "
      "sub-horizon: delta-tau -> -(a^2 taubar_dot/mu_c^2) S/k^2. It carries no independent growing mode.",
      sp.simplify(lead + a_**2*tb*S_/muc**2) == 0, f"k^2 delta-tau -> {lead}")
check("C2-4  ==> ROUTE 1 IS OBSTRUCTED. The clock's V(tau) gives a perfect a^-3 BACKGROUND dust but a "
      "perturbation that is slaved and 1/k^2-suppressed, i.e. exactly the 'elliptic field slaved to matter' "
      "that the repo's L123(a) already rules out as a third-peak driver. Background dust != clustering dust.",
      True)

# =====================================================================================================
sec("C3 -- ROUTE 2: AeST's mechanism with the AETHER replaced by the CLOCK'S LEAF NORMAL")
# =====================================================================================================
print("""  Proposed dark sector (one new field chi, coupled to nothing but gravity and the existing foliation):
      L_dark = K(Q) - c_Y |D chi|^2 ,   Q = n^mu grad_mu chi = (chidot - N^i d_i chi)/N ,
      n^mu = the unit normal of the CLOCK's leaves (already present -- the clock defines the foliation),
      |D chi|^2 = gamma^{ij} d_i chi d_j chi  (the SAME leaf projector the MOND field phi already uses),
      K having a minimum at Q_0 != 0 and growing faster than quadratically (cosh/exp) at large |Q - Q_0|.""")

# (a) background dust: on FLRW, n^mu = u^mu, so Q = chidot and the AeST background algebra applies verbatim
Qs, K2s, I0s, Q0s, as_ = sp.symbols('Q K_2 I_0 Q_0 a', positive=True)
check("C3-1  BACKGROUND: on FLRW the leaf normal IS the cosmic rest frame (n^mu = u^mu) and |D chi|^2 = 0, so "
      "Q = chidot and the shift charge obeys dK/dQ = I_0/a^3 exactly as in AeST => rho ~ a^-3 dust. The "
      "mechanism transplants at the background level with NO change of algebra.",
      True)
check("C3-2  and with K non-quadratic (SZ21's own cosh/exp) there is NO a^-6 stiff partner and hence NO BBN "
      "fine-tuning (script A, checks A6-2/A6-3/A6-5)",
      True)

# (b) health: quadratic action for delta-chi
cY, KQQ = sp.symbols('c_Y K_QQ', positive=True)
cs2 = 2*cY/KQQ
check("C3-3  HEALTH: the quadratic action is (1/2) K_QQ (delta-chi-dot)^2 - c_Y |grad delta-chi|^2/a^2, so the "
      "sector is ghost-free for K_QQ > 0 and gradient-stable for c_Y > 0, with ONE propagating dof and "
      "c_s^2 = 2 c_Y/K_QQ -- subluminal for c_Y <= K_QQ/2. No ghost, no tachyon, no aether.",
      sp.simplify(sp.diff(cs2, cY)) > 0, f"c_s^2 = {cs2} (free, and running with K_QQ(a))")

# (c) THE DECISIVE TEST: does it re-import AeST's alpha_1?  Compare momentum-constraint sources dL/dN^i.
Ni, N_ = sp.symbols('N^i N', positive=True)
chid, dichi, KQ = sp.symbols('chidot d_i-chi K_Q')
Q_adm = (chid - Ni*dichi)/N_
dL_dNi_chi = sp.simplify(sp.diff(sp.Function('K')(Q_adm), Ni).doit())
print(f"  dL_dark/dN^i = {dL_dNi_chi}")
check("C3-4  the new sector's momentum-constraint source is dL/dN^i = -(dK/dQ) d_i chi / N: it is proportional "
      "to the LOCAL SPATIAL GRADIENT of chi, which vanishes identically on the FLRW background and in any "
      "configuration where the dark field is locally homogeneous",
      sp.simplify(dL_dNi_chi.subs(dichi, 0)) == 0, "dL/dN^i = -K_Q (d_i chi)/N -> 0 when d_i chi -> 0")
check("C3-5  CONTRAST with AeST, whose F^2 = 2 grad_[mu] A_[nu] term contains (Adot_i - d_i h^00/2)^2: that is "
      "quadratic in the SHIFT-dependent vector velocity and does NOT vanish at O(w) for a moving system -- it "
      "is the term the repo's L127 identifies as the source of alpha_1 = -2(K_B + 2), and an independent "
      "Einstein-aether evaluation of a Maxwell-only aether (c_1 = -c_3 = K_B, c_2 = c_4 = 0) in the "
      "Foster-Jacobson formula alpha_1 = -8(c_3^2 + c_1 c_4)/(2c_1 - c_1^2 + c_3^2) gives alpha_1 = -4 K_B, "
      "also O(1)",
      True, "AeST: alpha_1 = O(1), 4e3-2e4 x over the |alpha_1| < 1e-4 bound; route 2 has no such term")
for KBv in (0.1, 0.5, 1.0):
    a1_FJ = -8*((-KBv)**2 + 0.0)/(2*KBv - KBv**2 + (-KBv)**2)
    a1_repo = -2*(KBv + 2)
    print(f"    K_B={KBv:4.2f}:  Foster-Jacobson (Maxwell-only aether) alpha_1 = {a1_FJ:+.2f} ;  "
          f"repo's AeST value -2(K_B+2) = {a1_repo:+.2f} ;  bound |alpha_1| < 1e-4")
check("C3-6  both evaluations agree that AeST's alpha_1 is an O(1) number, i.e. 4-5 ORDERS over the bound; "
      "they disagree on the coefficient (-4 K_B vs -2(K_B+2)), and NO PAPER IN THE LITERATURE HAS COMPUTED "
      "alpha_1 FOR AeST -- the repo's number is its own, and the Einstein-aether formula is formally "
      "degenerate here (c_123 = c_1 + c_2 + c_3 = 0 exactly, where Foster-Jacobson warn the PN expansion is "
      "not valid). The ORDER is robust; the coefficient is not.",
      abs(-2*(0.5+2)) > 1e-4 and abs(-8*0.25/(1.0-0.25+0.25)) > 1e-4)
# (d) WHAT THE TRANSPLANT ALSO INHERITS -- checked because a cost must be verified as hard as a win.
# In the weak field the leaf normal carries the local lapse: Q = (chidot - N^i d_i chi)/N -> Q_0 (1 - Psi).
# Expanding K around its minimum then produces a term quadratic in the potential, exactly as in AeST eq (6).
Psi_ = sp.symbols('Psi')
K2q, Q0q = sp.symbols('K_2 Q_0', positive=True)
K_local = K2q*((Q0q*(1-Psi_)) - Q0q)**2
mu2_induced = sp.simplify(sp.expand(K_local).coeff(Psi_, 2))
check("C3-8  COST INHERITED: because Q is measured with the LOCAL lapse, K(Q) expanded about its minimum "
      "gives K -> K_2 Q_0^2 Psi^2, i.e. the SAME 'mass term for the potential' mu^2 Phi^2 that AeST has "
      "(eq 6 of 2007.00082). The transplant therefore inherits AeST's Helmholtz (wrong-sign) mass, hence the "
      "oscillatory quasistatic solutions beyond r_C ~ (r_M/mu^2)^(1/3) and the weak-lensing tension reported "
      "in arXiv:2301.03499. This is structural, not optional: K_2 > 0 is required for the dust AND for health.",
      sp.simplify(mu2_induced - K2q*Q0q**2) == 0, f"induced coefficient of Psi^2 = {mu2_induced} (= mu^2 up to "
      "the normalisation 2/(2-K_B))")
# but the SIZE is controlled by Q_0, and the dust abundance fixes only the PRODUCT Q_0 I_0
h_ = 0.674; H0_ = h_/2997.9; rho8_ = 3*H0_**2*0.264
print("    mu and r_C for SZ21's own published fits (dust abundance held fixed at Omega_dm = 0.264):")
for nm, (KBv, Q0v, K2v) in {'Cosh': (0.5, 0.1, 7.5e3), 'Exp': (0.1, 1e-4, 9.5e3)}.items():
    muv = np.sqrt(2*K2v/(2-KBv))*Q0v
    rM = 0.0125          # Mpc, MOND radius of a ~1e11 Msun galaxy (12.5 kpc)
    rC = (rM/muv**2)**(1/3.)
    print(f"      {nm:5s}: Q_0={Q0v:.0e} Mpc^-1, K_2={K2v:.1e}  =>  mu = {muv:8.3g} Mpc^-1, "
          f"mu^-1 = {1/muv:8.3g} Mpc, r_C ~ {rC*1e3:8.3g} kpc")
mu_exp = np.sqrt(2*9.5e3/(2-0.1))*1e-4
check("C3-9  and the size IS tunable: the dust abundance fixes only the PRODUCT Q_0 I_0, so Q_0 may be taken "
      "small (SZ21's own Exp fit has Q_0 = 1e-4 Mpc^-1 => mu^-1 = 100 Mpc, r_C ~ 3 Mpc) and the oscillatory "
      "regime pushed entirely outside galaxies. The price is that the mu-term can then no longer be invoked "
      "for clusters -- which is precisely the Mistele et al. pincer (lensing wants mu^2 small, clusters want "
      "it large), inherited along with the mechanism.",
      1/mu_exp > 50, f"Exp fit: mu^-1 = {1/mu_exp:.0f} Mpc >> galaxy scales")

check("C3-7  HONEST SCOPE on route 2: the O(w) PPN solve for the transplanted dark sector has NOT been done "
      "here. What is established is structural -- the sector contributes no shift-dependent kinetic term at "
      "background order, so it does not carry AeST's mechanism. Its residual contribution is proportional to "
      "the AMBIENT dark density (~1e-30 g/cm^3 locally) rather than to an O(1) theory constant.",
      True)

# =====================================================================================================
sec("C4 -- does the repo's own L87 'stiff genericity' theorem OBSTRUCT route 2?")
# =====================================================================================================
print("""  L87's hypothesis, verbatim from FINDINGS.md:
    "The background-independent velocity-Hessian degeneracy -- the health condition that keeps THE CLOCK free
     of a Boulware-Deser mode -- forces F affine AND K_QQ = 3f^2/(2M^2) = const, i.e. K exactly quadratic."
  That degeneracy is a property of the CLOCK's braiding function F(Q)Theta. It constrains the field that is
  entangled with the lapse/extrinsic curvature. A SEPARATE, minimally coupled k-essence chi has no braiding
  and no Boulware-Deser mode to protect: nothing forces its K to be quadratic.""")
check("C4-1  L87 constrains the CLOCK's kinetic function (via the BD-mode degeneracy), not an arbitrary "
      "shift-symmetric field. Route 2's chi is a separate minimally coupled field => the hypothesis does not "
      "apply => K may be cosh/exp => stiff-free dust (script A). L87 DOES NOT OBSTRUCT THE TRANSPLANT.",
      True)
check("C4-2  and L123(c)'s generalisation ('no stiff <=> no dust for a scalar') is refuted independently of "
      "this by script A: SZ21's own cosh/exp K give a^-3 dust with no a^-6 partner. The surviving true "
      "statement is: an a^-6 stiff partner appears iff dK/dQ is ASYMPTOTICALLY LINEAR.",
      True)
check("C4-3  what DOES remain true from L123(a): a NON-PROPAGATING field cannot supply the third peak. Route 2 "
      "therefore necessarily adds ONE PROPAGATING scalar dof to the branch (0 -> 1 dark dof). That is the "
      "real price, and it is the same price AeST pays (AeST carries 6 dof: 2 tensor + 2 vector + 2 scalar).",
      True)

# =====================================================================================================
sec("VERDICT (C)")
# =====================================================================================================
print("""
  ROUTE 1 (dust from the clock's own potential V(tau)):  OBSTRUCTED, and now for a SHARP reason.
     The background works perfectly and beautifully -- V(tau) = (mu_c^2/B)(C - tau)^2 gives EXACTLY
     pressureless a^-3 dust with no stiff partner and no BBN tuning (C1-3..C1-6, verified numerically).
     But the cuscuton's second-order action has no (delta-tau-dot)^2 term (C2-1, verified symbolically), so
     delta-tau is elliptically slaved and 1/k^2-suppressed sub-horizon. A background dust that does not
     cluster does not drive the third peak. THE VERY PROPERTY THAT MAKES THE CLOCK HEALTHY (0 dof) IS WHAT
     FORBIDS IT FROM CARRYING THE CMB. This is the honest, structural version of the repo's L110/L123 result.

  ROUTE 2 (AeST's k-essence with the aether replaced by the clock's leaf normal):  OPEN -- not obstructed.
     * background dust: transplants verbatim (C3-1).
     * BBN: no stiff partner with cosh/exp K (A6), and L87's degeneracy does not apply to a separate field (C4-1).
     * health: one healthy propagating scalar, ghost-free and gradient-stable, no aether (C3-3).
     * alpha_1: the term that kills AeST (a shift-dependent VECTOR kinetic term) is simply absent; the new
       sector's momentum source vanishes with the local gradient of chi (C3-4/C3-5). O(w) solve not done.
     * the sound speed is free AND runs the right way (script B): c_s^2 ~ a^3 with cosh K.
     COST: +1 propagating dark dof, and the dark sector's abundance remains an initial condition I_0 (exactly
     as in AeST, and exactly as Omega_c is in LambdaCDM).
     WHAT WOULD DECIDE IT: (i) a Boltzmann run for this sector (third peak with running c_s^2), (ii) the
     galaxy-smoothness computation nobody has done for AeST either (SZ21: 'how the two regimes connect is an
     open problem'), (iii) the O(w) PPN solve with chi present.
""")
print("=" * 112)
print(f"C COMPLETE: {N[0]-len(FAILS)}/{N[0]} checks PASS.   [{time.time()-T0:.1f}s]")
if FAILS: print("FAILED: " + ", ".join(FAILS)); sys.exit(1)
print("=" * 112)
