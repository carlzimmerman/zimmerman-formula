#!/usr/bin/env python3
# agentL_extended_coherence.py -- THE LAST MECHANISM LOOPHOLE: collective coherence in extended bodies.
# Question: for the dS/Deser-Levin bath (mode wavelength ~ 1/kappa ~ Hubble), all N constituents of a body
# sit in ONE coherence patch and couple in phase to the IR tail. Does the collective response scale as
# N^2 (force) against inertia ~ N, giving effective per-mass enhancement ~ N that climbs the banked
# magnitude walls (agentN4 ~25 dex classical q^2/m; agentI 38-dex-in-beta vacuum correlator;
# agentN3 85-dex-in-eps Cassini wall)?
#
# Sections:
#   [L1] coherence criterion (sympy exact static-pair invariant; mpmath tail-variation scale; decoherence)
#   [L2] the scaling ledger (eps_1 reproduction of agentN3; N_req per wall; per-body table; closure masses)
#   [L3] kill tests: (a) WEP/tracer universality + LLR + MICROSCOPE; (b) solar reflex; (c) decoherence
#   [L4] convention sweep (footings)
#   [L5] verdict numbers
# Raw numbers first, comparisons second. No git. 2026-06-10.

import numpy as np
import mpmath as mp
import sympy as sp

mp.mp.dps = 30
out = []
def P(*a):
    line = " ".join(str(x) for x in a)
    out.append(line)
    print(line)

# ----------------------------------------------------------------------------------------------
# constants (SI unless noted)
c     = 2.99792458e8          # m/s
G     = 6.674e-11             # m^3 kg^-1 s^-2
hbar  = 1.054571817e-34       # J s
kB    = 1.380649e-23          # J/K
eV    = 1.602176634e-19       # J
hbar_eVs = 6.582119569e-16    # eV s
hbarc_eVm = 1.97326980e-7     # eV*m  (hbar*c)
m_p   = 1.67262192e-27        # kg
m_p_eV = 9.38272088e8         # eV
M_red_eV = 2.435e18 * 1e9     # reduced Planck mass in eV
Msun  = 1.989e30              # kg
pc    = 3.0857e16             # m

# repo footings (both run; see [L4])
cH_Lam = 5.418e-10            # m/s^2  hostile/bath normalization (agentE/N3)
a0_fw  = 9.36e-11             # m/s^2  framework canonical a0
a0_mond = 1.2e-10             # m/s^2  regular-MOND default (working-rule baseline)
H_Lam  = cH_Lam / c           # 1/s   = 1.807e-18
H_Lam_eV = hbar_eVs * H_Lam   # eV
H0     = 67.4 * 1e3 / (3.0857e22)   # 1/s (Planck 2018)
beta_C = 3.39e-3              # Cassini-maximal universal coupling (1403.7377 via agentN3 convention)
tau_eff_H = 0.27              # t_dS cap in Hubble units (agentN3 [N3-A3]/Wall 4)

P("="*110)
P("[L0] CONVENTIONS")
P(f"  H_Lambda = {H_Lam:.4e} s^-1 = {H_Lam_eV:.4e} eV ; cH_Lambda = {cH_Lam:.3e} m/s^2 ; a0(fw) = {a0_fw:.3e}")
P(f"  beta_Cassini = {beta_C:.3e} ; tau_eff*H (t_dS cap, N3) = {tau_eff_H}")
P(f"  hierarchy (m_p/M_red)(H/M_red) = {(m_p_eV/M_red_eV)*(H_Lam_eV/M_red_eV):.3e}   (N3 quotes 1.9e-79)")

# ----------------------------------------------------------------------------------------------
P("="*110)
P("[L1] THE COHERENCE CRITERION")
P("-"*110)
P("[L1a] sympy: the exact two-worldline dS invariant (static-patch pair, separation d, H=1 units)")
# Embedding R^{1,4}: worldline A = static at r=0 (the comoving geodesic, a=0, kappa=H);
# worldline B = static at r=d. X_A(s) = (sinh s, 0,0,0, cosh s)/H ; X_B(0) = (0, d,0,0, sqrt(1/H^2-d^2)).
H_s, d_s, s_s = sp.symbols('H d s', positive=True)
XA = sp.Matrix([sp.sinh(H_s*s_s)/H_s, 0, 0, 0, sp.cosh(H_s*s_s)/H_s])
XB = sp.Matrix([0, d_s, 0, 0, sp.sqrt(1/H_s**2 - d_s**2)])
eta = sp.diag(-1, 1, 1, 1, 1)
P_AB = sp.simplify(H_s**2 * (XA.T*eta*XB)[0])
P_AA = sp.cosh(H_s*s_s)                      # the self/geodesic invariant (N1 form at a=0)
dP   = sp.simplify(P_AB - P_AA)
dP_expected = (sp.sqrt(1 - H_s**2*d_s**2) - 1)*sp.cosh(H_s*s_s)
P(f"  P_AB(s; d)        = {P_AB}")
P(f"  Delta P = P_AB - P_AA = {sp.simplify(dP)} ; matches (sqrt(1-H^2 d^2)-1) cosh(Hs): "
  f"{sp.simplify(dP - dP_expected) == 0}")
lead = sp.series(sp.sqrt(1-H_s**2*d_s**2) - 1, d_s, 0, 4).removeO()
P(f"  leading pair-shift: Delta P / cosh(Hs) = {lead} + O(d^6)  ->  |Delta P|/P ~ (H d/c)^2 / 2  EXACT-leading")
P("  => the cross-pair memory kernel differs from the CoM self-kernel by a UNIFORM P-shift of relative")
P("     size (Hd/c)^2/2: for the dS bath the spatial coherence scale is the HUBBLE RADIUS, as posited.")

P("")
P("[L1b] mpmath: tail-variation scale |dlnV/dP| (the other half of the criterion |dP * dlnV/dP| << 1)")
def W_tail(Pv, mH):
    nu = mp.sqrt(mp.mpf(9)/4 - mp.mpf(mH)**2)   # complementary for m<3H/2; complex arg handled by sqrt
    hp, hm = mp.mpf(3)/2 + nu, mp.mpf(3)/2 - nu
    pref = mp.gamma(hp)*mp.gamma(hm)/(16*mp.pi**2)
    return pref * mp.hyp2f1(hp, hm, 2, (1+Pv)/2)
def V_tail(Pv, mH, eps=mp.mpf('1e-8')):
    return 2*mp.im(W_tail(Pv + 1j*eps, mH))
P(f"  {'m/H':>5} {'P':>6} {'V(P) [H^2]':>14} {'|dlnV/dP|':>12}")
for mH in (0.3, 1.0, 1.4):
    for Pv in (1.5, 3.0, 10.0):
        V0 = V_tail(mp.mpf(Pv), mH); dV = (V_tail(mp.mpf(Pv)*(1+mp.mpf('1e-6')), mH) - V0)/(Pv*mp.mpf('1e-6'))
        P(f"  {mH:5.2f} {Pv:6.1f} {float(V0):14.4e} {float(abs(dV/V0)):12.4e}")
P("  -> |dlnV/dP| = O(0.1-1) for the light (MOND-signed, m^2<2H^2) corner: criterion is (Hd/c)^2/2 * O(1) << 1.")
P("     MMC endpoint (N1): V = -H^2/4pi CONSTANT in P -> dlnV/dP = 0: coherence EXACT across the whole cone.")

P("")
P("[L1c] where coherence actually breaks -- three scales, per body")
bodies = [  # name, mass [kg], radius [m], N
    ("H atom (HI)",        1.6735e-27, 5.3e-11, None),
    ("Cs atom",            2.207e-25,  3.0e-10, None),
    ("dust grain 1um",     1.26e-14,   1.0e-6,  None),
    ("MICROSCOPE mass",    0.401,      0.04,    None),
    ("Moon",               7.342e22,   1.737e6, None),
    ("Earth",              5.972e24,   6.371e6, None),
    ("Jupiter",            1.898e27,   6.99e7,  None),
    ("Sun (star)",         Msun,       6.96e8,  None),
    ("GMC 1e5 Msun",       1e5*Msun,   50*pc,   None),
    ("GMC 1e7 Msun (max)", 1e7*Msun,   100*pc,  None),
    ("MW baryons",         6.1e10*Msun, 30e3*pc, None),
]
bodies = [(n, m, r, m/m_p) for (n, m, r, _) in bodies]
R_H = c/H_Lam
P(f"  dS-bath coherence length l_c = c/kappa ~ c/H = {R_H:.3e} m = {R_H/pc/1e9:.2f} Gpc")
P(f"  {'body':<20} {'N':>10} {'R [m]':>10} {'(HR/c)^2/2':>12}  spatially coherent (dS bath)?")
for n, m, r, N in bodies:
    dPrel = (H_Lam*r/c)**2/2
    P(f"  {n:<20} {N:10.2e} {r:10.2e} {dPrel:12.2e}  {'YES' if dPrel<1e-2 else 'NO'}")
P("  -> EVERY body through the whole Milky Way is inside ONE dS coherence patch: the loophole's premise holds.")
P("")
P("  massive in-band carriers (knee band, for completeness; N3: anti-MOND-signed for m^2>2H^2):")
for m_eV in (1.3e-29, 5e-28, 5e-26, 1.6e-24):
    lC = hbarc_eVm/m_eV
    P(f"    m = {m_eV:.1e} eV : lambda_C = {lC:.2e} m = {lC/pc:.2e} pc "
      f"-> star coherent: {6.96e8 < lC}; 50-pc cloud coherent: {50*pc < lC}; MW coherent: {30e3*pc < lC}")
P("")
P("  internal/thermal decoherence (solar core T = 1.57e7 K):")
v_th = np.sqrt(3*kB*1.57e7/m_p)
P(f"    proton v_th = {v_th:.3e} m/s ; charge depletion q -> q/gamma: (v/c)^2/2 = {(v_th/c)**2/2:.2e}  (NOT decoherence)")
nu_coll = 9e31 * 1.5e-23 * v_th   # n * sigma_Coulomb * v, order estimate
a_int = v_th * nu_coll
P(f"    collisional proper acceleration a_int ~ v*nu_coll ~ {a_int:.1e} m/s^2 ; x_int = a_int/cH = {a_int/cH_Lam:.1e}")
P(f"    BUT bound-motion displacement <= R: internal coords enter the pair kernel only at (HR/c)^2/2 <= "
  f"{(H_Lam*6.96e8/c)**2/2:.1e} (star)")
P("    -> the monopole Q = beta*M/M_Pl is conserved under internal motion; the kernel cannot resolve sub-patch")
P("       structure; the a-keyed (N^2) cross-terms key to the CoM history. Internal temperature does NOT decohere.")
rng = np.random.default_rng(7)
Nmc = 10**4
vecs = rng.normal(size=(Nmc, 3)); vecs /= np.linalg.norm(vecs, axis=1)[:, None]
P(f"    incoherent control (random-phase MC, N={Nmc}): |sum of N unit vectors| = {np.linalg.norm(vecs.sum(0)):.1f}"
  f" ~ sqrt(N) = {np.sqrt(Nmc):.1f} -> incoherent ensembles give sqrt(N) FLUCTUATION (eps ~ eps_1/sqrt(N): SMALLER)")

# ----------------------------------------------------------------------------------------------
P("="*110)
P("[L2] THE SCALING LEDGER: eps_body = N * eps_1 (coherent), and what N closes each banked wall")
P("-"*110)
# reproduce agentN3 Wall-1 eps_1 (capped, per nucleon)
hier = (m_p_eV/M_red_eV)*(H_Lam_eV/M_red_eV)
eps1_beta1 = hier * tau_eff_H/(4*np.pi)
eps1_cass  = beta_C**2 * eps1_beta1
eps1_q1    = (H_Lam_eV/m_p_eV) * tau_eff_H/(4*np.pi)
P(f"  eps_1(beta=1)      = {eps1_beta1:.3e}   (N3 quotes 4.1e-81)")
P(f"  eps_1(beta_Cassini)= {eps1_cass:.3e}   (N3 quotes 4.7e-86)")
P(f"  eps_1(q=1/nucleon) = {eps1_q1:.3e}   (N3 quotes 2.8e-44)")
P("")
M_H = c**3/(G*H_Lam)
N_H = M_H/m_p
P(f"  Hubble mass M_H = c^3/(G H_Lambda) = {M_H:.3e} kg ; N_H = {N_H:.3e} nucleons")
rho_b = 0.0224 * 1.878e-26
Mb_horizon = rho_b * (4*np.pi/3)*(c/H0)**3
P(f"  horizon baryon budget (Omega_b h^2 = 0.0224, R = c/H0): M_b = {Mb_horizon:.2e} kg ; N_b = {Mb_horizon/m_p:.2e}")
P("")
P("  N_req for eps_body = 1 (the closure ledger):")
for tag, e1 in (("beta = beta_Cassini", eps1_cass), ("beta = 1 (gravitational)", eps1_beta1),
                ("q = 1/nucleon (force 1e37 x gravity, already dead)", eps1_q1)):
    Nr = 1/e1
    P(f"    {tag:<48}: N_req = {Nr:.2e} = {Nr*m_p:.2e} kg = {Nr*m_p/Msun:.2e} Msun = {Nr*m_p/M_H:.2e} M_Hubble")
P("")
P("  the gravitational-charge identity (the classical q^2=Gm^2 route, agentN4's 25-dex wall -- ALREADY coherent):")
eps_cl_sun = G*Msun*H_Lam/c**3
r_g = 2*G*Msun/c**2
P(f"    eps_classical(M) = G M H/c^3 = r_g/(2 R_H): Sun = {eps_cl_sun:.3e} (N4 quotes 1.1e-23; footing diff x1.2)")
P(f"    check r_g/(2R_H) = {r_g/(2*R_H):.3e} ; closure: eps=1 at M = M_H = {M_H:.2e} kg, i.e. x{1/eps_cl_sun:.1e} the Sun")
P("    -> the 25-dex wall is the SUN'S OWN coherent N^2 number (N = 1.19e57 already inside it);")
P("       the only 'body' that closes it is the horizon mass itself.")
P("")
P("  the vacuum-correlator route (agentI 2c-i, '38 dex' -- a gap in beta, not eps; per-nucleon):")
beta_req_I = 4.4e35
eps1_corr = (beta_C/beta_req_I)**2
P(f"    eps_1(beta_C) = (beta_C/beta_req)^2 = {eps1_corr:.2e} -> N_req = {1/eps1_corr:.2e} = {m_p/eps1_corr:.2e} kg"
  f" = {m_p/eps1_corr/Msun:.2e} Msun")
P("    AND the sign is anti-MOND for m^2 > 2H^2 = the whole knee band (agentI 2c-i): no N flips a sign.")
P("")
P("  naive misreadings of the prompt's gaps, corrected:")
P(f"    'N = 1e25 closes 25 dex'  -> 1e25 nucleons = {1e25*m_p*1e3:.1f} g (a ~17-gram lab mass) -- WRONG reading:")
P("       the 25-dex wall is Sun-referenced and already N^2-coherent (above); no kg-scale closure exists.")
P(f"    'N = 1e38 closes 38 dex'  -> 1e38 nucleons = {1e38*m_p:.2e} kg (a ~500-m asteroid) -- WRONG reading:")
P("       agentI's 38 dex is in beta (eps ~ beta^2): the per-nucleon eps gap is 76.6 dex -> N_req = 1.7e76.")
P("")
P("  PER-BODY TABLE (dS-bath/N3 channel, capped, eps = N * eps_1):")
P(f"  {'body':<20} {'N':>10} | {'eps(beta_C)':>12} {'dex short':>9} | {'eps(beta=1)':>12} {'dex short':>9}")
for n, m, r, N in bodies + [("horizon baryons", Mb_horizon, c/H0, Mb_horizon/m_p)]:
    eC, e1 = N*eps1_cass, N*eps1_beta1
    P(f"  {n:<20} {N:10.2e} | {eC:12.2e} {np.log10(1/eC):9.1f} | {e1:12.2e} {np.log10(1/e1):9.1f}")
P("  -> WHICH BODIES GET MOND-STRENGTH: NONE. At the Cassini coupling the largest bound common-acceleration")
P("     unit (a 1e7 Msun cloud) is 21.6 dex short; a star 28.3 dex; the whole horizon baryon budget 6.9 dex.")
P("     At beta=1 the HORIZON ITSELF comes within ~2 dex (the r_g ~ R_H tautology) -- but no sub-horizon body does,")
P("     and beta=1 unscreened is itself Cassini-dead by x{:.0e} in gamma-1.".format((1/beta_C)**2))
P("")
beta_req_star = beta_C*np.sqrt(1/(Msun/m_p*eps1_cass))
P(f"  coupling that WOULD give a star eps=1: beta_req = {beta_req_star:.2e}")
P(f"    -> scalar force 2*beta^2 = {2*beta_req_star**2:.1e} x gravity between all unscreened bodies;")
P(f"    -> over the Cassini gamma-1 budget by x{(beta_req_star/beta_C)**2:.1e} (in eps terms). DEAD on arrival.")

# ----------------------------------------------------------------------------------------------
P("="*110)
P("[L3] THE KILL TESTS (both ways, full weight)")
P("-"*110)
P("[L3a] WEP / tracer universality: eps proportional to M_body is BODY-DEPENDENT inertia")
nu = lambda y: 1/(1-np.exp(-np.sqrt(y)))
P("  predicted gas-vs-star split if the tracer unit differs (atom-unit branch: HI Newtonian, stars MONDian):")
for a0 in (a0_fw, a0_mond):
    row = " ; ".join(f"g_bar={g:.0e}: dlog g_obs = {np.log10(nu(g/a0)):.3f} dex" for g in (1e-12, 1e-11, 1e-10))
    P(f"    a0 = {a0:.2e}: {row}")
P("  observed: ONE RAR for gas-traced (HI/Halpha) and stellar-traced systems; total scatter 0.13 dex,")
P("  intrinsic ~0.057 dex (1609.05917; 2693 pts); dSph stellar-dispersion tracers on the same law (1610.08981).")
P("  -> predicted deep-regime tracer split 0.55-1.0 dex = 4-8x TOTAL scatter, 10-18x intrinsic: KILLED.")
P("")
P("  branch table for the 'body' convention (the decision tree, all branches):")
e_star = 1.0  # calibrated
for tag, Nb in (("HI atom (diffuse, unbound)", 1.0), ("GMC 1e5 Msun (bound-cloud unit)", 1e5*Msun/m_p)):
    P(f"    {tag:<34}: eps/eps_star = {Nb/(Msun/m_p):.1e}")
P("    branch 1 (atom unit):  gas Newtonian vs stars MOND -> 0.55-1.0 dex tracer split vs 0.13 observed: DEAD")
P("    branch 2 (cloud unit): eps_cloud = 1e3-1e7 x eps_star -> eps > 1 = NEGATIVE inertia (dynamical runaway)")
P("                           or, saturated by hand at 1 -> needs a new scale AND falls to branch 3: DEAD")
P("    branch 3 (saturation at some N_sat): can only CAP eps, never raise it -> the L2 magnitude wall stands")
P("                           (no body reaches 1 at allowed coupling) AND the Sun saturates too -> [L3b]: DEAD")
P("")
P("  LLR (Earth vs Moon free fall toward the Sun; Williams-Turyshev-Boggs 2012, arXiv:1203.2150:")
P("  Delta(m_g/m_i) = (-0.8 +/- 1.3)e-13). Stellar calibration eps(N) = N/N_sun * g(x); x_E = x_M (same helio a):")
x_E = 5.93e-3/cH_Lam
g388_lo, g388_hi = 2.45e-15*2e5/2.1e-7, 2.45e-15*1.5e6/2.1e-7   # N3 Wall-2 back-out at x=388
for tag, gfun in (("flat (over-hostile)", lambda x: 1.0),
                  ("N3 (ln x)/x profile", None)):
    if gfun:
        g_E_lo = g_E_hi = gfun(x_E)
    else:
        scale = (388/x_E)*(np.log(x_E)/np.log(388))
        g_E_lo, g_E_hi = g388_lo*scale, g388_hi*scale
    epsE_lo = (5.972e24/Msun)*g_E_lo; epsE_hi = (5.972e24/Msun)*g_E_hi
    dEM_lo, dEM_hi = epsE_lo*(1-7.342e22/5.972e24), epsE_hi*(1-7.342e22/5.972e24)
    P(f"    profile {tag:<22}: Delta(m_g/m_i)_E-M = [{dEM_lo:.1e}, {dEM_hi:.1e}] "
      f"-> x[{dEM_lo/1.3e-13:.1e}, {dEM_hi/1.3e-13:.1e}] over the LLR bound")
P("    -> over the bound by x5-x39 even on the maximally suppressed profile; x2.2e7 flat. KILLED (subordinate kill).")
P("")
eps_micro = (0.401/Msun)  # x g(orbital x), g <= 1
P(f"  MICROSCOPE (2209.15487, eta ~ 1.5e-15): eps(0.4 kg) <= {eps_micro:.1e} at stellar calibration;")
P("    composition split is binding-energy-level (~1e-3) on top -> eta_pred <~ 1e-34: MICROSCOPE IS BLIND.")
P("    (honest both ways: lab/space WEP does NOT bind a mass-proportional coupling at this normalization;")
P("     the kills are astrophysical -- tracers, LLR, and the reflex.)")
P("")
P("[L3b] THE SOLAR REFLEX (Door IVb budget, agentE): the Sun has the LARGEST N in the solar system")
a_sun = 2.1e-7
x_sun = a_sun/cH_Lam
budget = 2.45e-15            # m/s^2, agentE survival line (s < 3.21e-11 -> response < 2.45e-15)
P(f"  Sun: N = {Msun/m_p:.2e} (vs Jupiter {1.898e27/m_p:.2e} = x{Msun/1.898e27:.0f} smaller); the Sun IS the")
P(f"  calibrating body class: eps_sun = eps_star ~ 1 by construction. x_sun = a_sun/cH = {x_sun:.0f}.")
eps_lo, eps_hi = g388_lo, g388_hi
P(f"  retained dressing at x=388: suppressed profile eps_eff = [{eps_lo:.2e}, {eps_hi:.2e}] (= N3 Wall 2);")
P(f"  flat reading eps_eff = 1.")
for tag, ee in (("suppressed lo", eps_lo), ("suppressed hi", eps_hi), ("flat", 1.0)):
    da = ee*a_sun
    P(f"    {tag:<13}: anomalous reflex = {da:.2e} m/s^2 = x{da/budget:.1e} over the agentE budget; "
      f"Mars-residual equivalent ~ {377*ee/3.588e-6:.2e} m vs 1.5 m")
P("  agentE [5]: Sun-only/full signal ratio = 1.000 (Mars), 0.998 (Saturn) -> the kill is 100% Sun-carried:")
P("  de-modifying the planets (their smaller N) changes NOTHING; GM_J absorption is Juno-refuted (20-1000x).")
P("  -> N-scaling makes Door IVb STRICTLY WORSE: the mechanism puts its largest effect on the one body whose")
P("     anomalous response is budgeted at 2.45e-15 m/s^2. Over budget by 5.3-7.9 dex. KILLED.")
P("")
P("[L3c] decoherence: see [L1c] -- internal temperature does NOT break monopole coherence (bounded displacement,")
P("  conserved Q, kernel blind below the patch scale). BOTH WAYS: no kill from decoherence, and NO RESCUE either:")
P("  there is no self-decoherence cap N_sat that could make eps universal across tracers at a useful value --")
P("  a cap only lowers eps, and the magnitude ledger [L2] is already 21.6+ dex short at the largest bound body.")

# ----------------------------------------------------------------------------------------------
P("="*110)
P("[L4] CONVENTION SWEEP (working-rule discipline)")
P("-"*110)
for tag, Hval in (("H_Lambda (canonical)", H_Lam), ("H_0 (rho_total footing)", H0)):
    h_eV = hbar_eVs*Hval
    e1 = beta_C**2*(m_p_eV/M_red_eV)*(h_eV/M_red_eV)*tau_eff_H/(4*np.pi)
    P(f"  {tag:<24}: eps_1(beta_C) = {e1:.2e} ; star eps = {Msun/m_p*e1:.2e} ; "
      f"dex short = {np.log10(1/(Msun/m_p*e1)):.1f}")
P(f"  a0 footing for the tracer split (above): 9.36e-11 vs 1.2e-10 moves dlog g_obs by < 0.06 dex.")
P(f"  s-footing for the reflex: agentE ran BOTH (s=cH kills x251, s=a0 kills x8.5); our eps_eff >= 2.3e-3 sits")
P(f"  x{2.3e-3/3.588e-6:.0f} above even the HOSTILE killed template. No footing moves any verdict.")

# ----------------------------------------------------------------------------------------------
P("="*110)
P("[L5] VERDICT NUMBERS (summary)")
P("-"*110)
P(f"  coherence premise: REAL (eps ~ N exact for bound bodies; dS patch = {R_H/pc/1e9:.1f} Gpc; no thermal break)")
P(f"  residual magnitude gap after full N^2 credit, Cassini coupling: star {np.log10(1/(Msun/m_p*eps1_cass)):.1f} dex;"
  f" 1e7-Msun cloud {np.log10(1/(1e7*Msun/m_p*eps1_cass)):.1f} dex; horizon baryons"
  f" {np.log10(1/(Mb_horizon/m_p*eps1_cass)):.1f} dex")
P(f"  closure body at gravitational coupling: M = M_H = {M_H:.1e} kg (eps = r_g/2R_H -> needs r_g ~ R_H)")
P(f"  coupling to fix a star instead: beta = {beta_req_star:.1e} = force {2*beta_req_star**2:.0e} x gravity: dead")
P(f"  universality: tracer split 0.55-1.0 dex predicted vs 0.13 dex observed; LLR x5-x39 (suppressed) to x2.2e7 (flat)")
P(f"  solar reflex: x2.0e5-8.6e7 over the agentE budget; Sun-only carries 100% of the killed template")
P("  => the N^2 gain and the WEP violation are THE SAME NUMBER: coherence buys exactly what universality forbids.")

with open(__file__.replace('.py', '.out'), 'w') as f:
    f.write("\n".join(out) + "\n")
P("")
P("[done] output mirrored to agentL_extended_coherence.out")
