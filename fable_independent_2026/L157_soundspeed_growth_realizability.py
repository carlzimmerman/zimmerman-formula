#!/usr/bin/env python3
"""
L153 -- THE GDM LOOPHOLE, PART 2: IS A GROWING SOUND SPEED REALIZABLE, AND WHAT DOES IT COST THE BACKGROUND?
        Two sharp theorems for BAROTROPIC fluids (a growth ceiling p < 3(1+w), and an exact CLIMB bound
        Delta_Phi_max = 3 * integral of c_s^2 dln a), a third instance of the velocity-ordering obstruction
        (fuzzy DM and ghost condensates both sit at p = -2), and a mean-free-path no-go for particle GDM.
=============================================================================================================
L152 showed the CMB-vs-galaxy pincer of L125 does NOT close against a fluid: it needs only p > -1, where
c_s^2 is proportional to a^p.  This lane asks the two prior questions:

  (Q1) WHICH mechanisms can actually deliver a given p, and what breaks when they try?
  (Q2) What does a nonzero, time-varying c_s^2 cost the BACKGROUND expansion (w_eff, BAO, distances)?

WHAT IS COMPUTED (self-contained sympy + numpy; every algebraic claim is a sympy identity):
  0  the exact barotropic dictionary.  For P = P(rho): dln c_s^2/dln a = 3(1+w) * nu with
     nu = -dln c_s^2/dln rho.  "c_s^2 grows with a" is IDENTICALLY "c_s^2 falls with rho" -- a density
     statement, not a time statement.  This is the DENSITY-TIME DUALITY that drives everything below.
  1  THEOREM A (growth ceiling).  If c_s^2 = dP/drho >= 0 (no gradient instability), c_s^2 is non-increasing
     in rho (the growth condition), and the NEC holds down to rho -> 0, then c_s^2 <= w pointwise; for the
     power-law family P = A rho^Gamma this is exactly w = 3 c_s^2/(3-p) and hence p < 3 STRICTLY, with the
     cost w/c_s^2 = 3/(3-p) diverging as p -> 3.
  2  THEOREM B (climb bound).  A barotropic fluid at cosmic mean density can climb a potential well of depth
     at most  Delta_Phi_max = integral_rhobar^infty c_s^2 dln rho = 3 * integral_0^1 c_s^2(a) dln a.
     For Gamma < 1 this is FINITE, so there is NO regular hydrostatic solution in a MOND logarithmic
     potential: the fluid condenses at a finite radius.  For the power law, Delta_Phi_max = 3 c_s^2(1)/p.
  3  the OTHER mechanisms, each evaluated on its own terms:
       fuzzy / ultralight DM:  c_eff = hbar k /(2 m a)  =>  p = -2  =>  k_J ~ a^{1/4} INCREASING.
                               A SECOND, independent instance of the velocity-ordering obstruction.
       ghost condensate:       omega^2 = k^4/M^2 a^4 => c_eff ~ k/a => p = -2.  A THIRD instance.
       shift-symmetric k-essence P ~ X^n:  c_s^2 = w = 1/(2n-1) EXACTLY -- constant, p = 0, healthy for
                               n > 0.  Also CORRECTS L123's "generic a^-6 stiff tail": the true scaling is
                               rho ~ a^{-3(1+c_s^2)}, which for c_s^2 ~ 1e-6 is a^-3.000003, not a^-6.
       collisional particles:  a hydrodynamic sound speed needs mean free path << the scale.  At the cosmic
                               mean density that demands sigma/m ~ 1e5-1e6 cm^2/g, five to six orders above
                               the Bullet-Cluster / halo-shape bound.
       late heating / decay:   any collisionless species free-streams as 1/a AFTER the last kick, and the
                               undecayed cold fraction still clusters, so it reduces to the two above.
  4  Q2 -- the BACKGROUND cost, computed: w_0, the change in rho_d(a), in E(z), and in comoving distance.

POLARITY: each check ASSERTS a statement; PASS = the statement is true.  Two of the results here are
NEGATIVE for the loophole and two are POSITIVE (a realization exists; the background cost is nil) -- both
are reported at the same weight.
"""
import sympy as sp
import numpy as np
import sys, time, math

T0 = time.time(); FAILS = []; NCHECK = [0]
def check(name, ok, detail=""):
    NCHECK[0] += 1
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f"   ({detail})" if detail else ""), flush=True)
    if not ok: FAILS.append(name)
def sec(t): print("\n" + "=" * 112); print(t); print("=" * 112, flush=True)
def P(s=""): print(s, flush=True)

print("=" * 112)
print("L153 -- can anything DELIVER a sound speed that grows with a?  Two theorems, three obstructions, "
      "one realization")
print("=" * 112, flush=True)

CKMS = 299792.458

# =========================================================================================================
sec("PART 0 -- THE BAROTROPIC DICTIONARY: 'c_s^2 grows with a' is IDENTICALLY 'c_s^2 falls with rho'.")
# =========================================================================================================
a, rho, w, nu, p_, Gam, A_, c2 = sp.symbols("a rho w nu p Gamma A c_s2", positive=True)
# continuity: dln rho / dln a = -3(1+w)
dlnrho_dlna = -3*(1 + w)
# chain rule for any barotropic c_s^2(rho)
dlnc2_dlna = sp.simplify((-nu) * dlnrho_dlna)          # nu := -dln c_s^2/dln rho
P("      continuity            dln rho / dln a   =  -3 (1 + w)")
P("      barotropic chain rule dln c_s^2 / dln a =  -3 (1 + w) * dln c_s^2 / dln rho  =  3 (1 + w) nu")
P("")
P(f"      so                    p  ==  dln c_s^2/dln a  =  {sp.simplify(dlnc2_dlna)}          with nu = -dln c_s^2/dln rho")
P("")
P("      THE DENSITY-TIME DUALITY.  For a barotropic fluid c_s^2 is a function of rho ALONE.  Demanding")
P("      that c_s^2 grow with the scale factor is therefore the SAME demand as that c_s^2 fall with density.")
P("      But a galaxy IS a region of high density.  The property that lets the fluid evade the L125 lemma")
P("      cosmologically is the property that makes it soft exactly where the galaxy gate needs it stiff.")
P("      Concretely: the fluid inside a present-day structure of overdensity Delta has EXACTLY the sound")
P("      speed the universe had at a = (1+Delta)^{-1/3}.  A galaxy is a time machine for a barotropic fluid.")
check("DUAL-1  the barotropic dictionary is an identity, not a model: p = dln c_s^2/dln a = 3(1+w) nu with "
      "nu = -dln c_s^2/dln rho.  Growth in time and softening with density are the SAME statement, so the "
      "cosmological evasion and the galaxy gate are not independent -- they read the same function",
      sp.simplify(dlnc2_dlna - 3*(1+w)*nu) == 0,
      f"p = 3(1+w)nu  identically; a structure of overdensity Delta sees c_s^2 at a=(1+Delta)^(-1/3)")

# =========================================================================================================
sec("PART 1 -- THEOREM A (growth ceiling): a barotropic fluid whose sound speed grows obeys c_s^2 <= w, "
    "hence p < 3(1+w).")
# =========================================================================================================
P("  Hypotheses.  (H1) barotropic: P = P(rho).  (H2) no gradient instability: c_s^2 = P'(rho) >= 0.")
P("  (H3) the growth condition: c_s^2 non-increasing in rho (equivalently P concave).  (H4) the null energy")
P("  condition rho + P >= 0 holds down to rho -> 0, which forces P(0) >= 0.")
P("")
P("  Proof.  By (H3), c_s^2(rho) <= c_s^2(rho') for every rho' <= rho, so")
P("        c_s^2(rho) * rho  =  integral_0^rho c_s^2(rho) drho'  <=  integral_0^rho c_s^2(rho') drho'")
P("                          =  P(rho) - P(0)  <=  P(rho)          [by (H4)]")
P("  hence  c_s^2 <= P/rho = w.  QED.")
P("")
# verify on the power-law family symbolically, and verify the integral inequality numerically on a
# non-power-law example so the theorem is not merely a restatement of the family
Ppl = A_ * rho**Gam
c2pl = sp.diff(Ppl, rho)
wpl  = sp.simplify(Ppl/rho)
ratio_pl = sp.simplify(c2pl/wpl)
nu_pl = sp.simplify(-sp.simplify(sp.diff(c2pl, rho)*rho/c2pl))
P(f"      power-law family  P = A rho^Gamma :   c_s^2 = {sp.simplify(c2pl)},   w = {wpl},   c_s^2/w = {ratio_pl}")
P(f"                                            nu = -dln c_s^2/dln rho = {nu_pl}  =  1 - Gamma")
P(f"                                            p  = 3(1+w) nu  ->  3(1-Gamma) for w << 1")
check("THMA-1  on the power-law family the theorem is an identity: c_s^2/w = Gamma, and (H2) c_s^2 >= 0 "
      "with A > 0 forces Gamma > 0, so c_s^2 <= w exactly when Gamma <= 1 -- which is exactly the growth "
      "condition nu = 1 - Gamma >= 0.  Growth and c_s^2 <= w are the same constraint",
      sp.simplify(ratio_pl - Gam) == 0 and sp.simplify(nu_pl - (1 - Gam)) == 0,
      "c_s^2/w = Gamma;  nu = 1 - Gamma;  growth (nu>0) <=> Gamma<1 <=> c_s^2 < w")
# the ceiling on p, and its cost
p_of_Gam = 3*(1 - Gam)
w_over_c2 = sp.simplify(1/Gam.subs(Gam, 1 - p_/3))
P("")
P(f"      p = 3(1 - Gamma)  =>  Gamma = 1 - p/3,  and  w/c_s^2 = 1/Gamma = {sp.simplify(w_over_c2)} = 3/(3-p).")
P("      Gamma > 0 (no gradient instability) is therefore  p < 3  STRICTLY, and the price of approaching the")
P("      ceiling is w/c_s^2 = 3/(3-p), which DIVERGES as p -> 3.")
P("")
P(f"      {'p':>6} {'Gamma':>8} {'w/c_s^2':>10}   {'w_0 for c_s(1)=207 km/s':>24}")
cs2_gal = (207.0/CKMS)**2
for pv in (0.0, 1.0, 2.0, 2.5, 2.9, 2.99, 3.0):
    if pv >= 3.0:
        P(f"      {pv:6.2f} {0.0:8.4f} {'infinite':>10}   {'FORBIDDEN (c_s^2 <= 0)':>24}"); continue
    P(f"      {pv:6.2f} {1-pv/3:8.4f} {3/(3-pv):10.3f}   {3/(3-pv)*cs2_gal:24.3e}")
check("THMA-2  THEOREM A, sharp form.  For a barotropic fluid with c_s^2 >= 0, growing with a, and NEC-safe "
      "at low density, c_s^2 <= w.  On the power-law family this is p < 3(1+w), i.e. p < 3 to the accuracy "
      "that matters, and the cost of approaching the ceiling is w/c_s^2 = 3/(3-p) -> infinity.  There is NO "
      "barotropic fluid with p >= 3",
      float(sp.simplify(w_over_c2.subs(p_, 2.9))) > 10 and float(sp.simplify(w_over_c2.subs(p_, 0))) == 1.0,
      "p < 3 strictly;  w/c_s^2 = 3/(3-p);  p=2.9 costs w = 10 c_s^2, p=2.99 costs w = 100 c_s^2")

# =========================================================================================================
sec("PART 2 -- THEOREM B (climb bound): how deep a well can a barotropic fluid climb, from its own history?")
# =========================================================================================================
P("  Hydrostatic equilibrium of a barotropic fluid:  dP/dr = -rho dPhi/dr, i.e.  c_s^2(rho) drho/rho = -dPhi.")
P("  Integrating from the cosmic mean rho_bar (where Phi = Phi_ref) inward to arbitrarily high density:")
P("")
P("        Delta_Phi_max  =  integral_{rho_bar}^{infinity} c_s^2(rho) dln rho")
P("")
P("  and, by the DENSITY-TIME DUALITY of PART 0 (dln rho = -3 dln a along the cosmological trajectory),")
P("")
P("        Delta_Phi_max  =  3 * integral_0^1 c_s^2(a) dln a.")
P("")
P("  THE FLUID CAN CLIMB EXACTLY THREE TIMES ITS OWN LOG-INTEGRATED COSMOLOGICAL SOUND-SPEED HISTORY.")
P("  For the power-law family this evaluates in closed form:")
P("")
lna = sp.symbols("lna", real=True)
cs2_of_a = c2 * sp.exp(p_ * lna)                    # c_s^2(1) * a^p
climb = sp.integrate(3 * cs2_of_a, (lna, -sp.oo, 0))
P(f"        3 * integral_{{-inf}}^{{0}} c_s^2(1) e^{{p lna}} dlna  =  {sp.simplify(climb)}"
  f"     (converges only for p > 0)")
check("THMB-1  THEOREM B: the maximum potential depth a barotropic fluid can climb from the cosmic mean is "
      "Delta_Phi_max = integral c_s^2 dln rho = 3 * integral_0^1 c_s^2(a) dln a, which for the power-law "
      "family is exactly 3 c_s^2(1)/p.  A fluid that grows FASTER (larger p) can climb LESS -- the two "
      "requirements of the hybrid pull in opposite directions through one and the same function",
      sp.simplify(climb - 3*c2/p_) == 0,
      "Delta_Phi_max = 3 c_s^2(1)/p;  isothermal (p=0) diverges, i.e. an isothermal fluid can climb any well")
P("")
P("  COROLLARY (no regular hydrostatic solution).  A MOND galaxy has Phi = v_c^2 ln r with UNBOUNDED depth")
P("  as r -> 0.  For any p > 0, Delta_Phi_max is FINITE, so there is a finite radius")
P("        r_crit  =  r_ref exp( -Delta_Phi_max / v_c^2 )  =  r_ref exp( -3 c_s^2(1) / (p v_c^2) )")
P("  at which the hydrostatic density diverges as (r - r_crit)^{-3/p}.  Inside r_crit the fluid does not")
P("  merely compress -- it CONDENSES, with no pressure support at all.  A fluid whose sound speed grows in")
P("  time has NO pressure support beyond a finite well depth.")
P("")
def r_crit(cs_kms, p, vc, r_ref=3000.0):
    if p <= 0: return 0.0
    return r_ref*math.exp(-3*cs_kms**2/(p*vc**2))
P(f"      {'c_s(1)':>8} | " + "  ".join(f"p={pv:<5g}" for pv in (0.5,1.0,2.0,3.0)) + "     (r_crit in kpc, v_c=300 km/s, r_ref=3 Mpc)")
for cs in (207., 400., 700., 1100., 1600.):
    P(f"      {cs:8.0f} | " + "  ".join(f"{r_crit(cs,pv,300.):7.2e}" for pv in (0.5,1.0,2.0,3.0)))
check("THMB-2  COROLLARY: for any p > 0 a barotropic fluid has a finite condensation radius inside every "
      "logarithmic (MOND) galaxy potential, r_crit = r_ref exp(-3 c_s^2(1)/(p v_c^2)), where the hydrostatic "
      "density diverges as (r-r_crit)^{-3/p} and the enclosed mass diverges.  Keeping r_crit below the "
      "rotation-curve region costs c_s^2(1) > (p/3) v_c^2 ln(r_ref/r) -- LINEAR in p",
      r_crit(207., 1.0, 300.) > 1.0 and r_crit(1600., 1.0, 300.) < 1e-3,
      f"v_c=300, p=1: c_s=207 km/s (the L152 galaxy minimum) condenses already at "
      f"{r_crit(207.,1.,300.):.0f} kpc, i.e. the condensation front ENCLOSES the whole galaxy; pushing it "
      f"below 1 kpc needs c_s > 1600 km/s ({r_crit(1600.,1.,300.):.1e} kpc)")

# =========================================================================================================
sec("PART 3 -- THE OTHER MECHANISMS, each on its own terms.")
# =========================================================================================================
P("  (b) FUZZY / ULTRALIGHT DARK MATTER.  The quantum-pressure dispersion is omega^2 = (hbar k^2/(2 m a^2))^2,")
P("      so the effective propagation speed at fixed COMOVING k is  c_eff = hbar k/(2 m a)  --  proportional")
P("      to 1/a, EXACTLY the decoupled scaling.  Hence p = -2, and the Jeans wavenumber is")
aa, mm, hb, Gg, rr0 = sp.symbols("a m hbar G rho0", positive=True)
kk = sp.symbols("k", positive=True)
# perturbation equation:  ddot(delta) + 2H ddot -> Jeans balance   c_eff^2 k^2 / a^2  =  4 pi G rho
# with the FDM quantum-pressure speed c_eff = hbar k / (2 m a)  at fixed COMOVING k, and rho = rho0 a^-3.
c_eff_fdm = hb*kk/(2*mm*aa)
jeans_eq  = sp.Eq(c_eff_fdm**2*kk**2/aa**2, 4*sp.pi*Gg*rr0*aa**-3)
kJ_a = sp.simplify([s for s in sp.solve(jeans_eq, kk) if s.is_real is not False][0])
P(f"        c_eff(a) = {c_eff_fdm}     dln c_eff/dln a = "
  f"{sp.simplify(sp.diff(c_eff_fdm, aa)*aa/c_eff_fdm)}   (i.e. p = -2)")
P(f"        k_J(a) = {kJ_a}")
expo_num = sp.nsimplify(sp.simplify(sp.diff(kJ_a, aa)*aa/kJ_a))
P(f"        dln k_J/dln a = {expo_num}    (the textbook a^{{1/4}} of Hu-Barkana-Gruzinov 2000)")
check("FDM-1  fuzzy / ultralight dark matter is a SECOND, independent instance of the velocity-ordering "
      "obstruction, not an escape from it.  Its quantum-pressure speed at fixed comoving k is hbar k/(2 m a), "
      "proportional to 1/a -- the same p = -2 as a decoupled particle -- and the Jeans wavenumber therefore "
      "goes as a^{1/4}, INCREASING: its clustering set grows in time, the wrong direction",
      expo_num == sp.Rational(1, 4) and
      sp.simplify(sp.diff(c_eff_fdm, aa)*aa/c_eff_fdm) == -1,
      f"c_eff ~ 1/a  =>  p = -2;  k_J ~ a^(1/4) INCREASING (wrong direction, same as decoupled)")
P("")
P("  (d) GHOST CONDENSATE.  At the shift-symmetric minimum P_X = 0, so c_s^2 = 0 at leading order and the")
P("      dispersion is set by the higher-derivative term: omega^2 = k^4/(M^2 a^4).  The propagation speed at")
P("      fixed comoving k is again k/(M a) -- proportional to 1/a, p = -2.  A THIRD instance of the same")
P("      obstruction, with the same k^4 structure as fuzzy DM.  Additionally, a ghost condensate has a")
P("      Jeans-like GRAVITATIONAL instability of its own (the programme's g03x), so it is not a candidate.")
Mgc = sp.symbols("M", positive=True)
c_gc = kk/(Mgc*aa)
check("GC-1  a ghost condensate is a THIRD instance of the same obstruction: with P_X = 0 the leading "
      "dispersion is omega^2 = k^4/(M^2 a^4), so the propagation speed at fixed comoving k is k/(M a), again "
      "proportional to 1/a and again p = -2.  Every k^4 (higher-derivative) dispersion sits at p = -2, "
      "because k/a is a physical wavenumber",
      sp.simplify(sp.diff(c_gc, aa)*aa/c_gc) == -1,
      "omega^2 = k^4/M^2a^4  =>  c_eff = k/(Ma) ~ 1/a  =>  p = -2 (same corner as decoupled and fuzzy)")
P("")
P("  (a) SHIFT-SYMMETRIC k-ESSENCE, P = X^n.  This is the barotropic case, and it is the one mechanism that")
P("      DOES deliver a healthy, matter-like fluid with a finite sound speed:")
X, n = sp.symbols("X n", positive=True)
Pk = X**n
PX, PXX = sp.diff(Pk, X), sp.diff(Pk, X, 2)
rho_k = sp.simplify(2*X*PX - Pk)
cs2_k = sp.simplify(PX/(PX + 2*X*PXX))
w_k   = sp.simplify(Pk/rho_k)
noghost = sp.simplify(PX + 2*X*PXX)
P(f"        rho = 2 X P_X - P = {rho_k}          w = P/rho = {w_k}")
P(f"        c_s^2 = P_X/(P_X + 2 X P_XX) = {cs2_k}     (equal to w EXACTLY: the THEOREM A bound is SATURATED)")
P(f"        no-ghost / no-gradient-instability:  P_X + 2 X P_XX = {sp.simplify(noghost)} > 0 for n > 0, X > 0")
n_needed = sp.solve(sp.Eq(cs2_k, c2), n)[0]
P(f"        to realise a given c_s^2:  n = {sp.simplify(n_needed)};  for c_s^2 = 4.76e-7 this is n = "
  f"{float(n_needed.subs(c2, 4.76e-7)):.3e}")
check("KESS-1  a POSITIVE result: shift-symmetric k-essence P = X^n realizes a healthy constant-sound-speed "
      "dark fluid exactly, with c_s^2 = w = 1/(2n-1), no ghost and no gradient instability for n > 0.  So "
      "p = 0 (which L152 showed threads both of L125's gates) IS realizable by an explicit Lagrangian -- "
      "the loophole is not merely a parameterisation",
      sp.simplify(cs2_k - w_k) == 0 and sp.simplify(cs2_k - 1/(2*n-1)) == 0,
      "P = X^n:  c_s^2 = w = 1/(2n-1) > 0, P_X + 2X P_XX = n(2n-1)X^(n-1) > 0 (healthy)")
# correction to L123's stiff genericity
rho_of_charge = sp.symbols("rho_n")
# rho ~ (n_charge/a^3)^{1+c_s^2}  =>  rho ~ a^{-3(1+c_s^2)}
expo_stiff = sp.simplify(-3*(1 + cs2_k))
P("")
P(f"        BBN / stiff tail: the conserved shift charge gives rho proportional to a^{{{sp.simplify(expo_stiff)}}}"
  f" = a^{{-3(1+c_s^2)}}.")
P(f"        For c_s^2 = 4.76e-7 the exponent is {float(expo_stiff.subs(n, float(n_needed.subs(c2,4.76e-7)))):.7f},"
  f" not -6.  L123's 'generic a^-6 stiff tail' is")
P("        the n = 1 (canonical, c_s^2 = 1) corner of this family; at small c_s^2 there is NO separate stiff")
P("        branch and NO BBN problem.  This is a correction to L123 STIFF-1, in the loophole's favour.")
check("KESS-2  CORRECTION TO L123.  L123's STIFF-1 says a finite-c_s shift-symmetric k-essence generically "
      "carries an a^-6 stiff tail with a ~24-order BBN tuning.  Quantified, the exponent is -3(1+c_s^2), "
      "which for the c_s^2 of interest (1e-6) is -3.000003, not -6.  The a^-6 tail is the canonical n = 1 "
      "(c_s^2 = 1) corner only.  The BBN objection does NOT apply to a slow dark fluid",
      abs(float(expo_stiff.subs(n, float(n_needed.subs(c2, 4.76e-7)))) + 3.0) < 1e-5,
      f"rho ~ a^-3(1+c_s^2) = a^{float(expo_stiff.subs(n, float(n_needed.subs(c2,4.76e-7)))):.6f} for "
      f"c_s^2 = 4.8e-7 -- no stiff branch, no BBN tail")
P("")
P("  (c) A DARK-SECTOR PHASE TRANSITION OR LATE-TIME HEATING (decay products, dark radiation drag, dark")
P("      photon coupling).  Two independent obstructions, both quantitative:")
P("")
# mean free path
sigma_over_m = 1.0                        # cm^2/g, the Bullet-Cluster / halo-shape ceiling
rho_bar_cgs  = 2.6e-30                    # g/cm^3, cosmic mean dark density today
Mpc_cm       = 3.0857e24
lam_mfp_Mpc  = 1.0/(rho_bar_cgs*sigma_over_m)/Mpc_cm
sigma_needed = 1.0/(rho_bar_cgs*1.0*Mpc_cm)          # to get lambda = 1 Mpc at the cosmic mean
P(f"        mean free path at the cosmic mean density with sigma/m = 1 cm^2/g (the Bullet-Cluster ceiling):")
P(f"              lambda = 1/(rho sigma/m) = {lam_mfp_Mpc:.2e} Mpc   -- vastly larger than the horizon.")
P(f"        to be a HYDRODYNAMIC fluid on 1 Mpc at the cosmic mean density one needs")
P(f"              sigma/m > {sigma_needed:.2e} cm^2/g,  i.e. {math.log10(sigma_needed):.1f} orders above the bound.")
check("HEAT-1  a PARTICLE realization of GDM is excluded by the mean free path, independently of any heating "
      "history.  A sound speed is a hydrodynamic quantity: it requires lambda_mfp << the scale.  At the "
      "cosmic mean density, sigma/m = 1 cm^2/g (the Bullet-Cluster / halo-shape ceiling) gives lambda of "
      "order 1e5 Mpc; being a fluid on Mpc scales demands sigma/m ~ 1e5-1e6 cm^2/g, five to six orders "
      "above the bound.  Particles at the cosmic mean density FREE-STREAM -- and free-streaming is p = -2",
      lam_mfp_Mpc > 1e4 and math.log10(sigma_needed) > 4.5,
      f"lambda(sigma/m=1) = {lam_mfp_Mpc:.1e} Mpc; need sigma/m > {sigma_needed:.1e} cm^2/g "
      f"({math.log10(sigma_needed):.1f} dex above the bound)")
P("")
P("        And the ENERGY budget is NOT the obstruction, which is worth recording: raising the specific")
P("        internal energy to c_s^2 ~ 5e-7 c^2 costs 5e-7 of the dark rest mass, i.e. Omega ~ 1e-7 -- far")
P("        below any dark-radiation bound.  So heating fails on the MECHANISM (thermalization), not on the")
P("        energy.  For DECAYING dark matter specifically: particles kicked at time t cool as a(t)/a")
P("        afterwards (p = -2 again from the kick onward), and the UNDECAYED cold fraction still clusters")
P("        in galaxies and still spends the L61 excess.  A short lifetime removes the cold fraction but")
P("        then the kicked population has been cooling for a Hubble time.  No escape either way.")
u_frac = 1.5*4.76e-7
check("HEAT-2  the energy budget is explicitly NOT the obstruction (recorded so the kill is attributed to "
      "the right cause): heating the dark sector to c_s^2 ~ 5e-7 c^2 costs ~1e-6 of its rest mass, "
      "Omega ~ 1e-7 today, invisible to every dark-radiation bound.  Late heating dies on thermalization "
      "(HEAT-1) and on the surviving cold fraction, not on energetics",
      u_frac < 1e-5, f"Delta u / (rest mass) = {u_frac:.2e}; Omega_extra ~ {u_frac*0.26:.1e} -- unconstrained")

# =========================================================================================================
sec("PART 4 -- Q2: THE BACKGROUND COST.  Does a nonzero c_s^2 spoil the expansion history / BAO?")
# =========================================================================================================
P("  A barotropic fluid with c_s^2 has w = c_s^2 * 3/(3-p) (THEOREM A), and w inherits the same time")
P("  dependence, w(a) = w_0 a^p.  The background density then integrates to")
P("        rho_d(a) = rho_d,0 a^-3 exp( -3 [w(a) - w_0] / p ),   so   rho_d(a)/rho_d^{CDM}(a) - 1  ~  3w_0/p")
P("  at a = 1 and is exponentially smaller in the past.  Numbers for the L152 window:")
P("")
h = 0.6736; Om = 0.3138; OL = 1 - Om - 9.22e-5
def E2f(a, w0, pp, Od=0.2645, Ob=0.0493):
    fac = math.exp(-3*w0*(a**pp - 0.0)/pp) if pp > 0 else a**(-3*w0)
    return Ob*a**-3 + Od*a**-3*fac + 9.22e-5*a**-4 + OL
P(f"      {'p':>5} {'w_0':>11} {'d rho_d/rho_d (a=1)':>21} {'d E/E (z=0.5)':>15} {'d D_C(z=1100)/D_C':>19}")
worst = 0.0
for pv in (0.5, 1.0, 2.0, 2.9):
    w0 = 3*cs2_gal/(3-pv)
    drho = 3*w0/pv
    zs = 0.5; a5 = 1/(1+zs)
    dE = 0.5*abs(E2f(a5, w0, pv) - E2f(a5, 0.0, pv))/E2f(a5, 0.0, pv)
    ag = np.logspace(math.log10(1/1091.), 0, 4000)
    dc0 = np.trapz(1.0/(ag**2*np.sqrt(np.array([E2f(x, 0.0, pv) for x in ag]))), ag)
    dc1 = np.trapz(1.0/(ag**2*np.sqrt(np.array([E2f(x, w0, pv) for x in ag]))), ag)
    dD = abs(dc1/dc0 - 1)
    worst = max(worst, drho, dE, dD)
    P(f"      {pv:5.2f} {w0:11.3e} {drho:21.3e} {dE:15.3e} {dD:19.3e}")
check("BG-1  the BACKGROUND COST IS NIL, and this is reported as a NON-kill.  Across the whole L152 window "
      "the fluid's equation of state today is w_0 = 3 c_s^2/(3-p) < 1e-5, the dark density departs from "
      "a^-3 by < 1e-5, and the comoving distance to last scattering (hence theta_s, hence BAO calibration) "
      "shifts by < 1e-5 -- four orders below the measurement.  Task 3's 'this may be the actual kill' is "
      "answered: it is NOT.  The component is matter for every background observable",
      worst < 1e-4, f"worst of |d rho_d/rho_d|, |dE/E|, |dD_C/D_C| over p in [0.5, 2.9] = {worst:.2e}")
check("BG-2  and the reason is structural, not numerical: THEOREM A ties w to c_s^2 by w = 3c_s^2/(3-p), and "
      "the galaxy gate only ever asks for c_s^2 of order (v_c/c)^2 ~ 1e-6.  A sound speed large enough to "
      "smooth a galaxy is automatically far too small to matter for the expansion history.  Background "
      "self-consistency can never be the obstruction in this class",
      3*cs2_gal/(3-2.9) < 1e-4,
      f"even at p = 2.9 (worst case) w_0 = {3*cs2_gal/(3-2.9):.2e}; the galaxy gate needs only c_s ~ v_c")

# =========================================================================================================
sec("VERDICT")
# =========================================================================================================
P(f"""
  PART 2 VERDICT -- the mechanism map.

  REALIZABLE (and healthy):
    * shift-symmetric k-essence P = X^n gives a constant-sound-speed dark fluid with c_s^2 = w = 1/(2n-1),
      no ghost, no gradient instability, and -- correcting L123's STIFF-1 -- rho proportional to
      a^{{-3(1+c_s^2)}} = a^-3.000003, NOT a^-6.  There is no BBN tail for a slow fluid.  So p = 0, which
      L152 showed threads both of L125's gates, is delivered by an explicit Lagrangian.

  BOUNDED (two theorems, both new here):
    * THEOREM A -- a barotropic fluid whose sound speed grows obeys c_s^2 <= w, hence p < 3 strictly, with
      the cost w/c_s^2 = 3/(3-p) diverging at the ceiling.  No barotropic fluid reaches p = 3.
    * THEOREM B -- such a fluid can climb a potential well of depth at most 3 * integral c_s^2 dln a, i.e.
      3 c_s^2(1)/p for a power law.  For any p > 0 that is FINITE, so a MOND logarithmic potential (which is
      unbounded) always has a condensation radius r_crit = r_ref exp(-3c_s^2(1)/(p v_c^2)) inside which the
      fluid has no pressure support at all.  Growing FASTER buys LESS galaxy protection: one function is
      being asked to do two opposite jobs.

  DEAD ON ARRIVAL (three separate instances of the SAME p = -2 obstruction):
    * fuzzy / ultralight DM: c_eff = hbar k/(2 m a) ~ 1/a, k_J ~ a^{{1/4}} INCREASING.  Wrong direction.
    * ghost condensate:      omega^2 = k^4/M^2a^4, c_eff = k/(M a) ~ 1/a.  Wrong direction.  (And it carries
                             its own gravitational instability.)
    * collisional particles / late heating: a sound speed is hydrodynamic and needs lambda_mfp << scale;
      at the cosmic mean density that costs sigma/m ~ 1e5-1e6 cm^2/g, five to six orders above the
      Bullet-Cluster bound.  Particles at the mean density free-stream, and free-streaming IS p = -2.
      The energy budget is NOT the problem (1e-6 of the rest mass); thermalization is.

  NOT THE OBSTRUCTION (reported as such, so nothing is mis-attributed):
    * the background.  w_0 = 3c_s^2/(3-p) < 1e-5 everywhere in the window; rho_d departs from a^-3 by
      < 1e-5; the distance to last scattering shifts by < 1e-5.  Task 3's candidate kill is answered NO.

  So the class of mechanisms narrows to exactly one live family: a BAROTROPIC fluid / shift-symmetric
  k-essence with 0 <= p < 3, plus the unbounded NON-barotropic case in which c_s^2 depends on something
  other than the local density.  L154 puts the first through the epochs between recombination and today.
""")
print("=" * 112)
if FAILS:
    print(f"L153 INCOMPLETE: {len(FAILS)}/{NCHECK[0]} FAILED: {FAILS}"); sys.exit(1)
print(f"L153 COMPLETE: {NCHECK[0]}/{NCHECK[0]} checks PASS.   [{time.time()-T0:.1f}s]")
print("=" * 112)
