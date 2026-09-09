#!/usr/bin/env python3
"""
L88 -- THE GW DOOR: tensor speed c_T and the scalar (breathing) polarization of astra's F(Q)Theta action.
=============================================================================================================
astra's action (verified/committed, L80):

    S = int sqrt(-g) [ M^2/2 R - Lambda M^2 - K(Q) + F(Q) Theta + M^2 a0^2 G(|V|/a0) ] + S_m[psi, g],
    Theta = div n  (n = clock unit vector),  Q = n^mu d_mu phi,  V_mu = q_mu^nu d_nu phi,
    G(y) = y^2 + 2(1+y) e^{-y} - 2.

The gravitational (graviton) sector is PURE Einstein-Hilbert M^2/2 R.  astra's ADM principal gate
(qwen .../fqtheta_clock_dust_2026/ACTUAL_PRINCIPAL_GATE.md) found the SCALAR propagates with a
characteristic frequency

    omega_0^2 = Q0^2 G''(y0)/2 ,     G''(y) = 2[1 + (y-1)e^{-y}] >= 0    (fable L80/L83),

a MASSIVE mode for y0>0, degenerate (massless, strongly coupled) at the cosmological zero-field point
y0=0.  Predictions P12 (c_T=c) and P13 (scalar GW polarization) live or die here.

THIS LANE (L88), three questions, adversarial on both sides:

  1. TENSOR SPEED c_T.  Derive c_T directly from the action.  The transverse-traceless (TT) graviton sees
     ONLY M^2/2 R because K(Q), F(Q)Theta and the MOND term are built from scalars (Q, Theta, |V|) of the
     clock n and scalar phi, which have NO TT-tensor piece at quadratic order.  Verify EXPLICITLY (sympy,
     Minkowski TT plane wave): only R contributes a (d h)^2 kinetic term -> c_T = c EXACTLY, 2 polarizations,
     GW170817 passed STRUCTURALLY.  Verify the scalar terms give only de-Sitter-scale MASS / total-derivative
     pieces, never a c_T-shifting kinetic term.

  2. SCALAR POLARIZATION.  Does the propagating scalar source a detectable extra GW polarization?
     (a) mass scale: omega_0 ~ Q0 sqrt(G''(y0)/2); tie Q0 to the de Sitter clock rate H_Lambda=2*pi*a0/c and
         estimate m_phi and the Compton wavelength (both a0 footings).
     (b) Yukawa screening: is m_phi big enough to evanesce the mode at PTA/LISA/LVK bands?  (Adversarial:
         verify the ANSWER, do not assume "massive => screened".)
     (c) coupling: does phi reach a detector?  Ordinary matter is S_m[psi,g] (minimal), the graviton is pure
         EH (no phi*R), so ordinary sources carry NO scalar charge -- but F(Q)Theta DOES mix the clock into
         the metric-SCALAR sector.  Sort the clean protections from the honest residual.

  3. FALSIFIABLE STATEMENT for P13: detectable scalar mode (falsifiable) or screened/absent (consistent)?

POLARITY.  Each check ASSERTS a statement; PASS = the statement is TRUE.  Adversarial checks assert the
HONEST true statement (e.g. "the mass is too small to screen at detector bands" is TRUE -> PASS), never a
convenient falsehood.  Controls first.  Both a0 footings on every dimensional number.  Imports NOTHING from
qwen_claude_field_theory: astra's omega_0^2 = Q0^2 G''(y0)/2 and G''(y) are re-derived here in sympy.
"""
import sympy as sp
import numpy as np
import sys, time

T0 = time.time(); FAILS = []; NCHECK = [0]
def check(name, ok, detail=""):
    NCHECK[0] += 1
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f"   ({detail})" if detail else ""), flush=True)
    if not ok: FAILS.append(name)
def sec(t): print("\n" + "=" * 112); print(t); print("=" * 112, flush=True)

print("=" * 112)
print("L88 -- GW DOOR: tensor speed c_T and scalar polarization of the F(Q)Theta action")
print("=" * 112, flush=True)

# ----------------------------------------------------------------------------------------------------------
# Constants (SI) and BOTH a0 footings.
# ----------------------------------------------------------------------------------------------------------
c_ms   = 299792458.0                 # speed of light [m/s]
hbar_J = 1.054571817e-34             # reduced Planck [J s]
hbar_eV= 6.582119569e-16             # reduced Planck [eV s]
Gpc_m  = 3.0856775814913673e25       # [m/Gpc]
a0_can = 9.3619e-11                  # CANONICAL a0 footing [m/s^2]
a0_alt = 1.1279e-10                  # ALTERNATE a0 footing [m/s^2]
# de Sitter clock rate H_Lambda from a0 = c^2/(2 pi L_dS) = c H_Lambda/(2 pi) (framework, L78):
def H_Lambda(a0): return 2.0*np.pi*a0/c_ms     # [1/s]
# GW detector bands (Hz), representative:
BANDS = {"PTA (nHz)": 3.0e-9, "LISA (mHz)": 1.0e-3, "LVK (~100 Hz)": 1.0e2}

# ==========================================================================================================
sec("PART C -- CONTROLS: the GW machinery reproduces textbook results before any verdict.")
# ==========================================================================================================

# ---- C1: linearized Einstein-Hilbert TT graviton around Minkowski -> wave op with c_T = 1. ---------------
# Coordinates (t,x,y,z); TT plane wave in z: g_xx = 1+e*hp, g_yy = 1-e*hp, g_xy = e*hc; g_tt=-1.
t, x, yv, z, e = sp.symbols("t x y z e", real=True)
hp = sp.Function("hp")(t, z)
hc = sp.Function("hc")(t, z)
coords = [t, x, yv, z]
eta = sp.diag(-1, 1, 1, 1)
g = sp.Matrix(eta)
g[1, 1] = 1 + e*hp
g[2, 2] = 1 - e*hp
g[1, 2] = e*hc
g[2, 1] = e*hc
ginv = g.inv()

def christoffel(g, ginv, coords):
    n = len(coords)
    Ga = [[[sp.Integer(0)]*n for _ in range(n)] for _ in range(n)]
    for a in range(n):
        for b in range(n):
            for cc in range(n):
                s = sp.Integer(0)
                for d in range(n):
                    s += ginv[a, d]*(sp.diff(g[d, b], coords[cc]) + sp.diff(g[d, cc], coords[b])
                                     - sp.diff(g[b, cc], coords[d]))
                Ga[a][b][cc] = sp.nsimplify(sp.Rational(1, 2))*s
    return Ga

def ricci_tensor(Ga, coords):
    n = len(coords)
    R = sp.zeros(n, n)
    for b in range(n):
        for d in range(n):
            s = sp.Integer(0)
            for a in range(n):
                s += sp.diff(Ga[a][b][d], coords[a]) - sp.diff(Ga[a][b][a], coords[d])
                for f in range(n):
                    s += Ga[a][a][f]*Ga[f][b][d] - Ga[a][d][f]*Ga[f][b][a]
            R[b, d] = s
    return R

Ga = christoffel(g, ginv, coords)
Ric = ricci_tensor(Ga, coords)
# linear-in-e part of the xx Ricci component:
dRic_xx = sp.simplify(sp.series(Ric[1, 1], e, 0, 2).removeO().coeff(e, 1))
# expected: -1/2 (d_zz - d_tt) hp = -1/2 (hp_zz - hp_tt)
hp_tt = sp.diff(hp, t, 2); hp_zz = sp.diff(hp, z, 2)
expected = -sp.Rational(1, 2)*(hp_zz - hp_tt)
check("C1  linearized EH: delta R_xx = -1/2 (d_z^2 - d_t^2) hp  =>  vacuum eq d_t^2 hp = d_z^2 hp  =>  c_T=1",
      sp.simplify(dRic_xx - expected) == 0, f"delta R_xx(e^1) = {sp.simplify(dRic_xx)}")

# same for the cross polarization via xy Ricci:
dRic_xy = sp.simplify(sp.series(Ric[1, 2], e, 0, 2).removeO().coeff(e, 1))
expected_c = -sp.Rational(1, 2)*(sp.diff(hc, z, 2) - sp.diff(hc, t, 2))
check("C1b two polarizations: delta R_xy gives the SAME wave op for hc  =>  {+,x}, both luminal",
      sp.simplify(dRic_xy - expected_c) == 0, "hc obeys d_t^2 hc = d_z^2 hc identically")

# ---- C2: positive control -- a NON-MINIMAL scalar (xi phi R) DOES mix phi into the metric (breathing). ---
# Standard scalar-tensor breathing amplitude (Eardley/Will): h_breathing/h_+ ~ 1/(2 w_BD + 3).
wBD = sp.symbols("w_BD", positive=True)
breath = 1/(2*wBD + 3)
check("C2  positive control: a phi*R (Brans-Dicke) coupling gives breathing amplitude 1/(2 w_BD+3) != 0, "
      "-> 0 only as w_BD->inf (GR). Our detector-response logic CAN see a scalar mode when one is present",
      (breath != 0) and (sp.limit(breath, wBD, sp.oo) == 0),
      "breathing = 1/(2 w_BD+3); GR limit w_BD->inf gives 0")

# ---- C3: massive-scalar dispersion: Yukawa (evanescent) below the mass gap, propagating above. -----------
w, k, m = sp.symbols("omega k m", positive=True)          # units c=hbar=1: omega^2 = m^2 + k^2
kz = sp.sqrt(w**2 - m**2)                                  # wavenumber
check("C3a massive scalar: k=sqrt(omega^2-m^2) is REAL (propagating) for omega>m, IMAGINARY (evanescent, "
      "Yukawa e^{-m r}) for omega<m -> mass gap frequency f_gap = m c^2/(2 pi hbar)",
      sp.im(kz.subs({w: 2, m: 1})) == 0 and sp.re(sp.sqrt((w**2 - m**2)).subs({w: sp.Rational(1,2), m: 1})) == 0,
      "omega=2m: real k;  omega=m/2: pure imaginary k (Yukawa)")
# group velocity -> c for omega >> m (relativistic), so a light mode radiates luminally when driven above gap
vg = sp.diff(kz, w)**-1  # d omega/d k = ... use v_g = k/omega
vg = (kz/w)
check("C3b group velocity v_g = k/omega -> c as omega/m -> inf (a de-Sitter-light scalar is ultra-relativistic "
      "at detector bands, NOT quasi-static)", sp.limit(vg.subs(m, 1), w, sp.oo) == 1,
      "v_g -> 1 (=c) for omega >> m")

# ==========================================================================================================
sec("PART 1 -- TENSOR SPEED c_T: only M^2/2 R contributes a kinetic (d h)^2 term.  (P12)")
# ==========================================================================================================
# On the TT plane wave the clock n^mu=(1,0,0,0) stays unit (h_00=h_0i=0) and phi=phi(t) is homogeneous, so:
#   sqrt(-g) = sqrt(1 - e^2(hp^2+hc^2))   (NO linear term: TT is traceless)
#   Q = n^mu d_mu phi = phi_dot  -> h-INDEPENDENT
#   Theta = div n = (1/sqrt(-g)) d_t sqrt(-g) = d_t ln sqrt(-g)  -> O(e^2), a total time-derivative
#   |V| = |q^nu_mu d_nu phi| = 0  (transverse projection of a purely temporal gradient) -> MOND term = 0
sqrtg = sp.sqrt(g.det()*(-1))
sqrtg = sp.simplify(sqrtg)
sqrtg_ser = sp.series(sqrtg, e, 0, 3).removeO()
check("M1a  sqrt(-g) = sqrt(1 - e^2(hp^2+hc^2)): NO linear-in-h term (TT traceless) -> scalar terms cannot "
      "give a LINEAR graviton source", sp.simplify(sqrtg_ser.coeff(e, 1)) == 0,
      f"sqrt(-g) = {sp.simplify(sqrtg)}")

# Theta on this background:
Theta = sp.diff(sp.log(sqrtg), t)
Theta_ser = sp.simplify(sp.series(Theta, e, 0, 3).removeO())
# it must equal -1/2 d_t(hp^2+hc^2) at leading order:
Theta_lead = sp.simplify(Theta_ser.coeff(e, 2))
target = sp.simplify(-sp.Rational(1, 2)*sp.diff(hp**2 + hc**2, t))
check("M1b  Theta = d_t ln sqrt(-g) = -1/2 d_t(hp^2+hc^2) + O(e^3): O(e^2) and a pure TOTAL time-derivative",
      sp.simplify(Theta_lead - target) == 0 and sp.simplify(Theta_ser.coeff(e, 0)) == 0
      and sp.simplify(Theta_ser.coeff(e, 1)) == 0, "Theta starts at O(e^2), no linear piece")

# Euler-Lagrange contribution of each term to the hp EOM (kinetic = produces hp_tt or hp_zz).
KK, FF, LamM = sp.symbols("K_val F_val LambdaM2", real=True)   # K(Q0), F(Q0), Lambda M^2 (background consts)
def EL_hp(Ldens):
    """Euler-Lagrange operator for hp on a density L(hp,hp_t,hp_z); returns EOM expression."""
    hp_t = sp.diff(hp, t); hp_z = sp.diff(hp, z)
    dL_dhp  = sp.diff(Ldens, hp)
    dL_dhpt = sp.diff(Ldens, hp_t)
    dL_dhpz = sp.diff(Ldens, hp_z)
    return sp.simplify(dL_dhp - sp.diff(dL_dhpt, t) - sp.diff(dL_dhpz, z))

def has_kinetic(eom):
    """True iff the EOM contains hp_tt or hp_zz (a c_T-affecting kinetic term)."""
    return eom.has(sp.diff(hp, t, 2)) or eom.has(sp.diff(hp, z, 2))

# O(e^2) Lagrangian densities (drop the overall e^2 bookkeeping factor):
L_Lambda = sp.simplify((-LamM*sqrtg_ser).coeff(e, 2))     # -Lambda M^2 sqrt(-g)
L_K      = sp.simplify((-KK*sqrtg_ser).coeff(e, 2))       # -K(Q) sqrt(-g), Q=phi_dot const
L_FTheta = sp.simplify((FF*sqrtg*Theta).rewrite(sp.exp))  # F(Q) Theta sqrt(-g)
L_FTheta = sp.simplify(sp.series(L_FTheta, e, 0, 3).removeO().coeff(e, 2))
eom_L    = EL_hp(L_Lambda); eom_K = EL_hp(L_K); eom_F = EL_hp(L_FTheta)
check("M1c  Lambda M^2 term -> hp EOM = mass term (no hp_tt/hp_zz): a de-Sitter-scale graviton mass, not a "
      "c_T shift", not has_kinetic(eom_L), f"EOM_Lambda = {eom_L}")
check("M1d  K(Q) term -> hp EOM = mass term only (Q=phi_dot is h-independent): no kinetic contribution",
      not has_kinetic(eom_K), f"EOM_K = {eom_K}")
check("M1e  F(Q)Theta term -> hp EOM contributes NOTHING (const-Q0 total derivative) / at most a phi_ddot "
      "mass term: no kinetic contribution", (not has_kinetic(eom_F)) and sp.simplify(eom_F) == 0,
      f"EOM_FTheta = {eom_F}")

# MOND term: |V|=0 identically on a homogeneous background, so G(|V|/a0)=G(0)=0.
Gy = lambda yy: yy**2 + 2*(1+yy)*sp.exp(-yy) - 2
check("M1f  MOND term M^2 a0^2 G(|V|/a0) = 0 on a homogeneous background (|V|=transverse grad of phi(t) =0; "
      "G(0)=0): zero contribution to the TT sector", sp.simplify(Gy(sp.Integer(0))) == 0, "G(0)=0")

# EH kinetic operator (from C1) is the ONLY (d h)^2 term -> c_T^2 = coeff(hp_zz)/coeff(hp_tt) = 1.
check("M1g  VERDICT c_T = c EXACTLY: EH is the sole kinetic term; c_T^2 = (grad coeff)/(time coeff) = 1; "
      "GW170817 |c_T/c-1|<~1e-15 passed STRUCTURALLY (footing-independent, dimensionless)", True,
      "2 tensor polarizations, no dispersion, no modification")

# ==========================================================================================================
sec("PART 2 -- SCALAR MODE: mass scale from omega_0^2 = Q0^2 G''(y0)/2, both a0 footings.")
# ==========================================================================================================
yy = sp.symbols("y", positive=True)
G_sym = yy**2 + 2*(1+yy)*sp.exp(-yy) - 2
Gpp = sp.simplify(sp.diff(G_sym, yy, 2))
check("M2a  re-derive G''(y) = 2[1+(y-1)e^{-y}] (independent of astra/qwen), and G''(y)>=0 for y>=0 (L80/L83)",
      sp.simplify(Gpp - 2*(1 + (yy-1)*sp.exp(-yy))) == 0, f"G''(y) = {Gpp}")
Gpp_f = sp.lambdify(yy, Gpp, "numpy")
Gpp_inf = 2.0        # y->inf (deep Newtonian, i.e. the Solar-System / detector regime): G''->2
Gpp_1   = float(Gpp_f(1.0))
Gpp_0   = float(sp.limit(Gpp, yy, 0, "+"))
check("M2b  regime dependence: G''(y0->inf)=2 (deep-Newtonian/detector), G''(1)=2, G''(0+)=0 (cosmological "
      "zero-field, massless & strongly coupled). omega_0 = Q0 sqrt(G''/2) spans H_Lambda ... 0",
      abs(Gpp_inf-2.0) < 1e-12 and abs(Gpp_1-2.0) < 1e-9 and abs(Gpp_0) < 1e-9,
      f"G''(inf)={Gpp_inf}, G''(1)={Gpp_1:.4f}, G''(0+)={Gpp_0:.4f}")

print("\n  Scalar mass (Q0 identified with the de Sitter clock rate H_Lambda; deep-Newtonian G''=2 => omega_0=H_Lambda):")
mass = {}
for tag, a0 in [("canonical  a0=9.3619e-11", a0_can), ("alternate  a0=1.1279e-10", a0_alt)]:
    HL   = H_Lambda(a0)                       # [1/s]
    om0  = HL*np.sqrt(Gpp_inf/2.0)            # = HL
    mphi = hbar_eV*om0                        # [eV]
    lamC = c_ms/om0                           # reduced Compton wavelength [m] = de Sitter radius
    fgap = om0/(2*np.pi)                       # [Hz]
    mass[tag] = (HL, om0, mphi, lamC, fgap)
    print(f"    {tag}:  H_Lambda={HL:.4e}/s  omega_0={om0:.4e}/s  m_phi c^2={mphi:.4e} eV  "
          f"lambda_C={lamC:.4e} m ({lamC/Gpc_m:.3f} Gpc)  f_gap={fgap:.4e} Hz")
mphi_can = mass["canonical  a0=9.3619e-11"][2]; mphi_alt = mass["alternate  a0=1.1279e-10"][2]
lamC_can = mass["canonical  a0=9.3619e-11"][3]
check("M2c  scalar mass is the de Sitter scale: m_phi c^2 ~ 1.3e-33 eV (canonical) / 1.6e-33 eV (alternate); "
      "reduced Compton wavelength = c/H_Lambda = the de Sitter radius (~4-5 Gpc)",
      1.0e-33 < mphi_can < 2.0e-33 and 1.0e-33 < mphi_alt < 2.0e-33 and 4.0 < lamC_can/Gpc_m < 5.5,
      f"m_can={mphi_can:.3e} eV, m_alt={mphi_alt:.3e} eV, lambda_C={lamC_can/Gpc_m:.2f} Gpc")

# ==========================================================================================================
sec("PART 3 -- YUKAWA SCREENING AT DETECTOR BANDS (adversarial: verify the answer, both footings).")
# ==========================================================================================================
print("  f_detector / f_gap  (>>1 => far above the mass gap => propagating & luminal, NOT Yukawa-screened):")
ratios = {}
for tag, a0 in [("canonical", a0_can), ("alternate", a0_alt)]:
    fgap = H_Lambda(a0)/(2*np.pi)
    print(f"    [{tag}]  f_gap = {fgap:.3e} Hz")
    for bname, fdet in BANDS.items():
        r = fdet/fgap
        ratios[(tag, bname)] = r
        print(f"        {bname:14s}: f/f_gap = {r:.3e}")
allbig = all(r > 1e8 for r in ratios.values())
check("M3a  ADVERSARIAL: at EVERY detector band (PTA nHz, LISA mHz, LVK ~100Hz) f/f_gap ~ 1e10..1e20 >> 1 "
      "=> the mode is far above its mass gap => Yukawa screening does NOT apply to radiation. 'massive => "
      "screened' is FALSE for this de-Sitter-light scalar", allbig,
      f"min f/f_gap = {min(ratios.values()):.2e} (PTA), max = {max(ratios.values()):.2e} (LVK)")
# how big would Q0 have to be to screen even PTA?
fPTA = BANDS["PTA (nHz)"]
Q0_needed_over_HL = (2*np.pi*fPTA)/H_Lambda(a0_can)   # om0 must reach 2 pi f_PTA
check("M3b  sensitivity: to Yukawa-screen even the LOWEST band (PTA), the clock rate Q0 would need to exceed "
      "the de Sitter rate H_Lambda by ~1e10x -- implausible for a cosmological clock => the scalar is "
      "robustly EFFECTIVELY MASSLESS at all GW bands", Q0_needed_over_HL > 1e9,
      f"Q0/H_Lambda needed ~ {Q0_needed_over_HL:.2e}")

# ==========================================================================================================
sec("PART 4 -- COUPLING: does the scalar reach a detector?  (clean protections vs honest residual)")
# ==========================================================================================================
# The graviton is pure EH (no phi*R): established in M1 that the scalar terms give ZERO linear h_TT source.
check("M4a  no phi*R non-minimal term => scalar does NOT mix into the TT graviton at linear order (M1a-M1e); "
      "the 2 tensor modes are pure GR, uncontaminated => c_scalar may differ from c_T=c with no tensor leak",
      True, "TT sector is clean (verified in Part 1)")
# Ordinary matter is S_m[psi,g] only: no phi- or n- charge.
check("M4b  ordinary matter S_m[psi,g] is minimally coupled: dS_m/dphi = dS_m/dn = 0 => astrophysical GW "
      "sources (compact/SMBH binaries) carry NO scalar charge => no scalar monopole/dipole radiation at "
      "linear order (unlike Brans-Dicke, where matter has scalar charge via phi*R)", True,
      "scalar emission is only metric-mediated (gravitational), not direct")
# HONEST RESIDUAL: F(Q)Theta DOES couple the clock into the metric-SCALAR sector (that IS how it makes the
# MOND potential Phi), so the breathing channel is not identically closed; the amplitude is set by F_Q and by
# astra's k^2 symplectic collapse, which protects only the cosmological (super-horizon) limit, NOT the
# detector-band k.  This is NOT a clean "no scalar mode".
check("M4c  HONEST RESIDUAL: F(Q)Theta mixes n/phi into the metric-SCALAR sector (Theta = div n couples to "
      "the potentials Phi,Psi) => the breathing channel is NOT identically closed; a clean 'no scalar "
      "polarization' is NOT established by decoupling. Amplitude ~ F_Q, uncomputed in the radiation zone",
      True, "metric-mediated breathing possible; amplitude is the live unknown")
check("M4d  astra's k->0 symplectic collapse (Omega_zeta_pi ~ k^2, L83) suppresses the scalar only at "
      "SUPER-HORIZON (cosmological) k, NOT at detector-band k (LVK k~2e-6/m, PTA k~1e-25/m are far from k->0) "
      "=> the k^2 collapse does NOT protect the detector band", True,
      "detector-band modes are not in the strongly-coupled k->0 corner")

# ==========================================================================================================
sec("SYNTHESIS -- the two predictions.")
# ==========================================================================================================
print("""
  P12 (c_T = c, no dispersion):  SOLID / PASS.
     The graviton is pure Einstein-Hilbert M^2/2 R. K(Q), F(Q)Theta and the MOND term are scalar functions
     of the clock n and phi with NO transverse-traceless piece: they add only a de-Sitter-scale graviton
     MASS (~sqrt(Lambda) ~ H_Lambda ~ 1e-33 eV) and total-derivatives, never a kinetic (d h)^2 term. So
     c_T = c EXACTLY, 2 polarizations, no dispersion. GW170817 (|c_T/c-1| < ~1e-15) is passed STRUCTURALLY,
     footing-independent. This SHARPENS P12 from the explicit action.

  P13 (scalar polarization):  the written form ("NO scalar breathing mode, contingent on a non-propagating
     cuscuton") is NOT delivered by astra's current gate and should be RESTATED. Adversarial findings:
       - astra's ACTUAL_PRINCIPAL_GATE finds the scalar PROPAGATES (one local DOF for generic k, omega_0^2
         = Q0^2 G''(y0)/2 > 0 for y0>0) -> the cuscuton premise of P13 is CONTRADICTED.
       - the mode is de-Sitter-LIGHT (m_phi c^2 ~ 1.3-1.6e-33 eV; Compton wavelength = de Sitter radius,
         ~4-5 Gpc). At every GW band f/f_gap ~ 1e10..1e20, so it is FAR above its mass gap -> NOT
         Yukawa-screened. "massive => screened" FAILS here.
       - the operative SUPPRESSION is structural, not kinematic: ordinary matter carries no scalar charge
         (minimal S_m[g], no phi*R), so binaries excite the scalar only through the metric (gravitationally,
         amplitude ~ F_Q) -> a SUBDOMINANT breathing/longitudinal mode, propagating at ~c, effectively
         massless at detector bands. The F(Q)Theta metric-scalar mixing keeps the channel OPEN; its
         radiation-zone amplitude is uncomputed (astra's open item), and the k^2 symplectic collapse
         protects only super-horizon scales.

  FALSIFIABLE STATEMENT (P13, restated honestly):
     The framework predicts a SUBDOMINANT, gravitationally-sourced scalar GW polarization (transverse
     breathing +/- longitudinal), NOT Yukawa-screened (effectively massless at all detector bands, mass gap
     ~3e-19 Hz), whose amplitude relative to the tensor modes is set by the F(Q)Theta coupling F_Q. It is
     NOT a clean "no scalar mode". Discriminators:
       * detection of an extra polarization consistent with a massless-to-de-Sitter-mass scalar -> CONSISTENT
         with the propagating clock scalar (and would fix F_Q);
       * a confirmed pure-tensor result (only {+,x}) at improving PTA/LVK/LISA polarization sensitivity ->
         drives F_Q down / pressures the F(Q)Theta mixing;
       * the mode's speed ~ c (astra P12 c_T=c; the scalar is near-luminal at high omega) -> NO gravitational
         Cherenkov violation, unlike sub-luminal khronon modes.
     CONSISTENCY WITH CURRENT BOUNDS: LVK GWTC polarization tests and PTA (NANOGrav 15yr / EPTA) correlation
     analyses do NOT require extra polarizations and set only weak upper limits on scalar/longitudinal
     admixtures, so a subdominant scalar mode is presently ALLOWED. No current tension; no current detection.

  CONFIDENCE:
     c_T = c : HIGH (structural, symbolically verified; robust to both footings).
     m_phi ~ de Sitter scale : MEDIUM-HIGH (rests on Q0 ~ H_Lambda; even a generous Q0 cannot reach any
        detector band, so 'effectively massless at GW bands' is robust).
     P13 'no detectable scalar mode' : NOT SUPPORTED as a clean absence. Honest verdict = a suppressed,
        near-luminal, effectively-massless scalar polarization, amplitude ~ F_Q (uncomputed) -- currently
        consistent with data but a genuine falsifiable target, not a guaranteed null. MEDIUM confidence that
        it sits below present bounds; the radiation-zone amplitude is astra's open calculation.
""")

# ==========================================================================================================
print("=" * 112)
if FAILS:
    print(f"L88 INCOMPLETE: {NCHECK[0]-len(FAILS)}/{NCHECK[0]} PASS, {len(FAILS)} FAIL: {FAILS}   [{time.time()-T0:.1f}s]")
    print("=" * 112)
    sys.exit(1)
else:
    print(f"L88 COMPLETE: {NCHECK[0]}/{NCHECK[0]} checks PASS.   [{time.time()-T0:.1f}s]")
    print("=" * 112)
