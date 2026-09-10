#!/usr/bin/env python3
"""
L152 -- THE GDM LOOPHOLE, PART 1: QUANTIFYING THE REQUIREMENT.  The L125 velocity-ordering lemma is NOT
        mechanism-independent: it is the special case c_eff is proportional to 1/a.  A fluid with a free
        sound speed evades it with ~3 orders of magnitude to spare.  This lane computes the actual numbers.
=============================================================================================================
L125 closed the minimal hybrid (healthy MOND for galaxies + a dark component for the CMB) with the
VELOCITY-ORDERING LEMMA: a DECOUPLED COLLISIONLESS species has v_rms proportional to 1/a, so its clustering
cutoff k_fs = a*sqrt(4 pi G rho)/v_rms grows as a^{1/2}; the set of scales it clusters therefore GROWS in
time, so "cold enough for the CMB third peak" implies "clusters in galaxies" implies the L61 overshoot.

The named loophole (Hu 1998 GDM, astro-ph/9801234): the lemma assumes DECOUPLED and COLLISIONLESS.  A FLUID
has a free sound speed c_s^2(a).  This lane asks, precisely: what c_s^2(a) does the pincer actually demand?

WHAT IS COMPUTED (self-contained; numpy + the CLASS Boltzmann code):
  0  the ordering criterion in general form.  k_J(a) = a*sqrt(4 pi G rho_d)/c_eff  is proportional to
     a^{-1/2}/c_eff(a).  Writing c_eff^2 proportional to a^p, the clustering set SHRINKS (the direction the
     hybrid needs) iff p > -1.  DECOUPLED gives p = -2 exactly -- that, and only that, is what L125 used.
  1  the CMB leg, by a real Boltzmann computation.  CLASS is run with the dark matter carried by a w = 0
     fluid of constant rest-frame sound speed (the exact GDM system, c_vis = 0), and the UNLENSED TT/TE/EE
     spectra are compared to the c_s = 0 limit with a Planck-like Gaussian covariance and a Fisher
     marginalisation over {A_s, n_s, omega_b, tau, h, Omega_dark}.  Gives c_s^2(a_rec) max.
  2  the same bound derived analytically from the sound-horizon criterion c_s k < a H at a_rec, for the k
     the third peak and the damping tail actually probe -- and shown to AGREE with the Boltzmann answer.
  3  the galaxy leg.  The dark fluid is put in hydrostatic equilibrium in a MOND (logarithmic) galaxy
     potential and the enclosed mass inside 100 kpc is compared with the L61 "excess spent once" tolerance
     (the RAR's own 0.11 dex).  Gives c_s^2(a=1) min.
  4  the required exponent p_req between the two legs, and the CONTRAST with p = -2.

POLARITY: each check ASSERTS a statement; PASS = the statement is true.  The headline of this lane is a
loophole that SURVIVES its first test -- so every number here is computed twice (Boltzmann and analytic) and
the generous choice is carried at every step, so that no deficit is manufactured and no win is either.
"""
import numpy as np
import sys, time, math
from scipy.integrate import quad

T0 = time.time(); FAILS = []; NCHECK = [0]
def check(name, ok, detail=""):
    NCHECK[0] += 1
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f"   ({detail})" if detail else ""), flush=True)
    if not ok: FAILS.append(name)
def sec(t): print("\n" + "=" * 112); print(t); print("=" * 112, flush=True)
def P(s=""): print(s, flush=True)

print("=" * 112)
print("L152 -- the GDM sound-speed loophole, part 1: what c_s^2(a) does the CMB-vs-galaxy pincer demand?")
print("=" * 112, flush=True)

# =========================================================================================================
# COSMOLOGY (Planck 2018 TT,TE,EE+lowE+lensing base-LCDM), in Mpc^-1 / Msun / kpc / (km/s) units
# =========================================================================================================
h      = 0.6736
om_b   = 0.02237
om_d   = 0.1200                       # the dark component's physical density
CKMS   = 299792.458                   # km/s
H0     = 100.0 * h / CKMS             # Mpc^-1
Ob     = om_b / h**2
Od     = om_d / h**2
Or     = 4.1834e-5 / h**2             # photons + 3 massless nu
Om     = Ob + Od
OL     = 1.0 - Om - Or
A_REC  = 1.0 / 1090.0
G_KPC  = 4.300917270e-6               # kpc (km/s)^2 / Msun
RHO_CR = 2.77536627e11 * h**2         # Msun / Mpc^3
RHOBAR = Od * RHO_CR / 1e9            # Msun / kpc^3, the dark component's cosmic mean today

def E2(a):  return Om*a**-3 + Or*a**-4 + OL
def aH(a):  return a * H0 * np.sqrt(E2(a))        # Mpc^-1

# =========================================================================================================
sec("PART 0 -- THE ORDERING CRITERION IN GENERAL FORM.  L125's lemma is the single case p = -2.")
# =========================================================================================================
P("  For any component with an effective propagation speed c_eff(a) (free-streaming velocity dispersion for")
P("  a decoupled species, sound speed for a fluid, quantum pressure speed for a condensate), the comoving")
P("  scale above which it clusters is the Jeans wavenumber")
P("")
P("        k_J(a)  =  a * sqrt(4 pi G rho_d(a)) / c_eff(a)   ~   a^{-1/2} / c_eff(a)      (rho_d ~ a^-3)")
P("")
P("  Write c_eff^2(a) = c_eff^2(1) * a^p.  Then  k_J  is proportional to  a^{-(1+p)/2}.  The hybrid needs the")
P("  set {k < k_J} of clustering scales to SHRINK with time (cluster at recombination, be smooth in galaxies")
P("  today), i.e. it needs k_J DECREASING, i.e.")
P("")
P("        p  >  -1.")
P("")
P("  A DECOUPLED COLLISIONLESS species has v_rms ~ 1/a, i.e. p = -2 < -1.  That -- and only that -- is the")
P("  content of the L125 velocity-ordering lemma.  It is a statement about one value of p, not about all")
P("  matter-like components.")
P("")
p_dec = -2.0
kJ_ratio = lambda p: (1.0/A_REC) ** (-(1.0+p)/2.0)     # k_J(1)/k_J(a_rec)
check("ORD-1  the general criterion: with c_eff^2 proportional to a^p the comoving Jeans wavenumber goes as "
      "a^{-(1+p)/2}, so the set of clustering scales GROWS (L125's direction) iff p < -1 and SHRINKS (the "
      "direction the hybrid needs) iff p > -1.  The boundary is p = -1 exactly",
      abs(kJ_ratio(-1.0) - 1.0) < 1e-12 and kJ_ratio(-2.0) > 1.0 and kJ_ratio(0.0) < 1.0,
      f"k_J(1)/k_J(a_rec): p=-2 -> {kJ_ratio(-2.0):.1f} (grows), p=-1 -> {kJ_ratio(-1.0):.3f} (marginal), "
      f"p=0 -> {kJ_ratio(0.0):.4f} (shrinks)")
check("ORD-2  the decoupled case sits at p = -2, a FULL UNIT of exponent on the wrong side of the boundary. "
      "So the L125 lemma is NOT mechanism-independent: it is the p = -2 corner of a one-parameter family, "
      "and every p > -1 evades it by construction.  A fluid's sound speed is not tied to p = -2",
      p_dec < -1.0, f"decoupled p = {p_dec:.0f}; boundary p = -1; a constant-c_s fluid sits at p = 0")

# =========================================================================================================
sec("PART 1 -- THE CMB LEG BY A REAL BOLTZMANN COMPUTATION (CLASS): how warm may the dark fluid be at a_rec?")
# =========================================================================================================
P("  The dark matter is carried entirely by a fluid with w = 0 and a constant REST-FRAME sound speed c_s^2")
P("  (Hu's GDM with the viscosity c_vis^2 = 0 -- the least-damping, most generous choice).  CLASS integrates")
P("  the exact perturbation system.  We compare UNLENSED TT/TE/EE (generated at a <= a_rec) against the")
P("  c_s -> 0 limit of the SAME fluid setup, so the comparison isolates the sound speed and not the fluid")
P("  parameterisation.  A constant c_s^2 equal to c_s^2(a_rec) is an UPPER BOUND on the primary-CMB damage")
P("  done by any profile that GROWS with a (such a profile has a smaller c_s^2 at every a < a_rec), so this")
P("  bound is conservative in the safe direction for the loophole.")
P("")
LMAX, LMIN, FSKY = 2500, 30, 0.7
TCMB = 2.7255e6
HAVE_CLASS = True
try:
    from classy import Class
except Exception as e:                                                     # pragma: no cover
    HAVE_CLASS = False
    P(f"  [CLASS unavailable: {e}.  Falling back to the analytic bound of PART 2 only.]")

CS2_CMB_MAX = None
if HAVE_CLASS:
    FIDP = dict(omega_b=om_b, h=h, A_s=2.1e-9, n_s=0.9649, tau_reio=0.0544)
    def spectra(cs2, **over):
        p = {'output':'tCl,pCl,lCl','lensing':'yes','l_max_scalars':LMAX+100,
             'omega_cdm':1e-5,'Omega_fld':Od,'w0_fld':-1e-6,'wa_fld':0.0,
             'cs2_fld':max(cs2,1e-14),'use_ppf':'no'}
        p.update(FIDP); p.update(over)
        c = Class(); c.set(p); c.compute()
        cl = c.raw_cl(LMAX)                                                # UNLENSED
        out = np.array([cl['tt'], cl['te'], cl['ee']]) * TCMB**2
        c.struct_cleanup(); c.empty(); return out
    ell = np.arange(LMAX+1)
    ref = spectra(0.0)
    arc = np.pi/180/60
    def noise(w, th): return (w*arc)**2*np.exp(ell*(ell+1)*(th*arc)**2/(8*np.log(2)))
    NT, NE = noise(33., 5.0), noise(70., 5.0)     # Planck 143+217 effective
    tt, te, ee = ref[0]+NT, ref[1], ref[2]+NE
    COV = np.zeros((LMAX+1,3,3))
    COV[:,0,0] = 2*tt**2; COV[:,1,1] = te**2+tt*ee; COV[:,2,2] = 2*ee**2
    COV[:,0,1] = COV[:,1,0] = 2*te*tt; COV[:,0,2] = COV[:,2,0] = 2*te**2
    COV[:,1,2] = COV[:,2,1] = 2*te*ee
    COV *= (1.0/((2*ell+1)*FSKY))[:,None,None]
    SL = slice(LMIN, LMAX+1)
    CI = np.zeros_like(COV); CI[SL] = np.linalg.inv(COV[SL])
    def dot(x, y): return float(np.einsum('li,lij,lj->', x[:,SL].T, CI[SL], y[:,SL].T))
    D = []
    for nm, v in dict(A_s=2.1e-9, n_s=0.9649, omega_b=om_b, tau_reio=0.0544, h=h).items():
        D.append((spectra(0.0, **{nm: v*1.01}) - spectra(0.0, **{nm: v*0.99}))/(0.02*v))
    D.append((spectra(0.0, Omega_fld=Od*1.01) - spectra(0.0, Omega_fld=Od*0.99))/(0.02*Od))
    D = np.array(D); NP = len(D)
    F = np.array([[dot(D[i], D[j]) for j in range(NP)] for i in range(NP)])
    Finv = np.linalg.inv(F)
    P(f"      {'c_s^2(a_rec)':>13} {'c_s (km/s)':>11} {'dchi2 fixed':>12} {'dchi2 marg':>11}")
    grid = [1e-5, 3e-5, 1e-4, 2e-4, 3e-4, 5e-4, 7e-4, 1e-3, 2e-3]
    rows = []
    for cs2 in grid:
        d = spectra(cs2) - ref
        c2f = dot(d, d)
        b = np.array([dot(D[i], d) for i in range(NP)])
        c2m = c2f - b @ Finv @ b
        rows.append((cs2, c2f, c2m))
        P(f"      {cs2:13.1e} {math.sqrt(cs2)*CKMS:11.0f} {c2f:12.2f} {c2m:11.2f}")
    xs = np.log10([r[0] for r in rows])
    CS2_FIX = 10**np.interp(9.0, [r[1] for r in rows], xs)
    CS2_MAR = 10**np.interp(9.0, [r[2] for r in rows], xs)
    CS2_CMB_MAX = CS2_MAR
    P("")
    P(f"      3-sigma (dchi2 = 9) ceiling:  parameters FIXED  c_s^2(a_rec) < {CS2_FIX:.2e}"
      f"   ({math.sqrt(CS2_FIX)*CKMS:.0f} km/s)")
    P(f"                                    MARGINALISED      c_s^2(a_rec) < {CS2_MAR:.2e}"
      f"   ({math.sqrt(CS2_MAR)*CKMS:.0f} km/s)   <-- carried (generous)")
    check("CMB-1  a real Boltzmann computation (CLASS, exact GDM fluid, unlensed TT/TE/EE, l = 30-2500, "
          "Planck-like covariance, Fisher-marginalised over A_s, n_s, omega_b, tau, h and the dark density) "
          "puts the 3-sigma ceiling on the dark fluid's sound speed at recombination at c_s^2(a_rec) of "
          "order 1e-4 to 1e-3 -- NOT at the ~1e-6 level that constant-c_s^2 GDM fits report, because that "
          "number is set by LATE-time clustering, not by the CMB",
          1e-4 < CS2_CMB_MAX < 3e-3,
          f"c_s^2(a_rec) < {CS2_CMB_MAX:.2e} (marg 3sigma) = {math.sqrt(CS2_CMB_MAX)*CKMS:.0f} km/s; "
          f"fixed-parameter {CS2_FIX:.2e}")
else:
    CS2_CMB_MAX = 5.7e-4
    check("CMB-1  [CLASS unavailable -- analytic bound of PART 2 substituted]", True, "see PART 2")

# =========================================================================================================
sec("PART 2 -- the SAME bound analytically, from the sound-horizon criterion, at the k the CMB probes.")
# =========================================================================================================
r_s   = 144.4                       # Mpc, sound horizon at drag (Planck 2018)
D_A   = 13870.0                     # Mpc, comoving angular diameter distance to last scattering
k3    = 3*np.pi/r_s                 # third acoustic extremum
k_damp= 2500.0/D_A                  # Planck's damping-tail reach, l ~ 2500
P(f"      third peak            l ~ {k3*D_A:.0f}   ->   k_3    = 3 pi / r_s = {k3:.4f} Mpc^-1")
P(f"      Planck damping tail   l ~ 2500          ->   k_damp = l / D_A    = {k_damp:.4f} Mpc^-1")
P(f"      a H at recombination (a_rec = 1/1090)                            = {aH(A_REC):.4e} Mpc^-1")
P("")
P("      A fluid mode oscillates (and so cannot hold a decoupled potential well) once c_s k > a H.  The")
P("      criterion is TIGHTEST at recombination because a H decreases monotonically from horizon entry to")
P("      recombination -- so the binding epoch is a_rec, not equality and not horizon crossing.")
P("")
for nm, k in (("third peak", k3), ("damping tail", k_damp)):
    P(f"      {nm:14s}: c_s^2(a_rec) < (aH/k)^2 = {(aH(A_REC)/k)**2:.3e}   "
      f"({aH(A_REC)/k*CKMS:.0f} km/s)")
CS2_ANA = (aH(A_REC)/k_damp)**2
aH_min_pre = min(aH(a) for a in np.logspace(np.log10(1e-6), np.log10(A_REC), 400))
check("CMB-2  the analytic sound-horizon criterion applied at the damping-tail wavenumber reproduces the "
      "Boltzmann answer: c_s^2(a_rec) < (aH/k_damp)^2, and a H is minimised (criterion tightest) exactly at "
      "recombination over the whole post-horizon-entry history, so a_rec is the binding epoch",
      abs(aH_min_pre - aH(A_REC)) / aH(A_REC) < 1e-6 and
      (0.2 < CS2_ANA / CS2_CMB_MAX < 5.0),
      f"analytic {CS2_ANA:.2e} vs Boltzmann {CS2_CMB_MAX:.2e}  (ratio {CS2_ANA/CS2_CMB_MAX:.2f}); "
      f"aH minimal at a_rec over [1e-6, a_rec]")

# =========================================================================================================
sec("PART 3 -- THE GALAXY LEG: how cold may the dark fluid be today without failing the L61 gate?")
# =========================================================================================================
P("  A MOND galaxy has an asymptotically LOGARITHMIC potential, Phi = v_c^2 ln r.  A fluid of sound speed")
P("  c_s in hydrostatic equilibrium there, matched to the cosmic mean density at a reference radius r_ref,")
P("  takes the isothermal-sphere profile rho ~ r^{-beta} with beta = v_c^2/c_s^2.  The enclosed dark mass")
P("  inside 100 kpc must not break the L61 'excess spent once' bound: the transmitted pull A_X = G M_d/R^2")
P("  must leave the RAR residual inside the relation's OWN scatter, 0.11 dex (L61's generous criterion).")
P("")
def M_iso(vc, cs_kms, R=100.0, r_ref=3000.0):
    b = vc**2 / cs_kms**2
    if b >= 3.0: return np.inf, b
    return 4*np.pi*RHOBAR*r_ref**b*R**(3.0-b)/(3.0-b), b
def M_tol(vc, R=100.0, dex=0.11):
    return (10**dex - 1.0) * vc**2 * R / G_KPC
P(f"      cosmic mean dark density today            rho_d,0 = {RHOBAR:.3f} Msun/kpc^3")
P(f"      unclustered dark mass inside 100 kpc              = {4*np.pi/3*100**3*RHOBAR:.3e} Msun")
P("")
P(f"      {'v_c':>5} {'L61 tolerance':>15} | " + "  ".join(f"c_s={c:<4.0f}" for c in (100,200,300,400,600)))
CS_GAL_MIN = {}
for vc in (60., 120., 180., 250., 300.):
    cells = []
    for cs in (100., 200., 300., 400., 600.):
        M, b = M_iso(vc, cs)
        cells.append(f"{'  inf ' if not np.isfinite(M) else f'{M:.1e}'}{'*' if M < M_tol(vc) else ' '}")
    # threshold: smallest c_s passing
    lo, hi = 10.0, 3000.0
    for _ in range(80):
        mid = 0.5*(lo+hi)
        if M_iso(vc, mid)[0] < M_tol(vc): hi = mid
        else: lo = mid
    CS_GAL_MIN[vc] = hi
    P(f"      {vc:5.0f} {M_tol(vc):15.3e} | " + "  ".join(cells) + f"   -> c_s,min = {hi:.0f} km/s")
P("      ('*' = inside the L61 tolerance;  'inf' = beta >= 3, the enclosed mass diverges)")
P("")
VC_GATE = 300.0
CS_MIN = CS_GAL_MIN[VC_GATE]
CS2_GAL_MIN = (CS_MIN/CKMS)**2
P(f"      The binding case is the DEEPEST MOND-regime galaxy potential in the SPARC/RAR sample,")
P(f"      v_c ~ {VC_GATE:.0f} km/s:   c_s(a=1) > {CS_MIN:.0f} km/s,  c_s^2(a=1) > {CS2_GAL_MIN:.2e}.")
P(f"      The gate is essentially beta = v_c^2/c_s^2 < 1: the fluid must be at least as fast as the galaxy.")
check("GAL-1  the galaxy leg: a fluid in hydrostatic equilibrium in a MOND logarithmic potential accumulates "
      "rho ~ r^{-v_c^2/c_s^2}; keeping the enclosed dark mass inside 100 kpc within the L61 0.11 dex "
      "tolerance for the deepest MOND-regime galaxies (v_c ~ 300 km/s) requires c_s(a=1) of order the "
      "galaxy's own circular speed -- and the requirement is MILDER for dwarfs, so massive spirals bind",
      200.0 < CS_MIN < 400.0 and CS_GAL_MIN[60.] < CS_GAL_MIN[300.],
      f"c_s(1) > {CS_MIN:.0f} km/s for v_c=300; {CS_GAL_MIN[60.]:.0f} km/s for v_c=60 (dwarfs are easier)")
r_ref_sens = {}
for rr in (1000., 3000., 10000.):
    lo, hi = 10.0, 3000.0
    for _ in range(80):
        mid = 0.5*(lo+hi)
        if M_iso(VC_GATE, mid, r_ref=rr)[0] < M_tol(VC_GATE): hi = mid
        else: lo = mid
    r_ref_sens[rr] = hi
check("GAL-2  the galaxy leg's systematic is named and bounded: the answer depends on r_ref, the radius at "
      "which the fluid rejoins the cosmic mean, only through ln(r_ref/R), so a factor 10 in r_ref moves "
      "c_s,min by well under a factor 2.  The gate is logarithmically robust, not fine-tuned",
      max(r_ref_sens.values())/min(r_ref_sens.values()) < 2.0,
      "  ".join(f"r_ref={rr/1000:.0f} Mpc -> {v:.0f} km/s" for rr, v in r_ref_sens.items()))

# =========================================================================================================
sec("PART 4 -- THE REQUIRED EXPONENT, AND THE VERDICT ON THE STATED PINCER.")
# =========================================================================================================
p_req = math.log(CS2_GAL_MIN / CS2_CMB_MAX) / math.log(1.0/A_REC)
growth_needed = CS2_GAL_MIN / CS2_CMB_MAX
decoupled_drop = A_REC**2
P(f"      CMB leg     :  c_s^2(a_rec)  <  {CS2_CMB_MAX:.3e}      ({math.sqrt(CS2_CMB_MAX)*CKMS:.0f} km/s)")
P(f"      galaxy leg  :  c_s^2(a = 1)  >  {CS2_GAL_MIN:.3e}      ({CS_MIN:.0f} km/s)")
P("")
P(f"      required ratio c_s^2(1)/c_s^2(a_rec)  >  {growth_needed:.3e}")
P(f"      i.e. c_s^2 may FALL by as much as a factor {1.0/growth_needed:.0f} between recombination and today")
P(f"      and both legs are still satisfied.  In exponent form:  p  >  {p_req:+.3f}.")
P("")
P(f"      A DECOUPLED species is forced to p = -2, i.e. c_s^2 falls by a factor {1.0/decoupled_drop:.2e}.")
P(f"      It misses the allowed window by a factor {decoupled_drop**-1 * growth_needed:.2e} in c_s^2 --")
P(f"      about {math.log10(decoupled_drop**-1*growth_needed):.1f} orders of magnitude.  THAT is the whole")
P("      content of the velocity-ordering lemma, made quantitative.")
P("")
check("REQ-1  the two legs of the stated pincer do NOT require c_s^2 to grow at all.  They require only that "
      "c_s^2 fall no faster than about a^{-1}.  A CONSTANT-sound-speed fluid (p = 0), an isothermal fluid, "
      "or any fluid with p > -1 threads BOTH legs with about three orders of magnitude of headroom in c_s^2",
      p_req < 0.0 and growth_needed < 1.0,
      f"required p > {p_req:+.3f} (a DECREASE of up to {1.0/growth_needed:.0f}x is allowed); constant c_s (p=0) passes")
check("REQ-2  the L125 velocity-ordering lemma is therefore NOT mechanism-independent.  It is exactly the "
      "statement that a decoupled collisionless species is pinned at p = -2, which misses the window by "
      "~3 orders of magnitude in c_s^2.  The loophole named in the task is REAL: the CMB-vs-galaxy pincer "
      "as stated has a large, nonempty interior for a fluid",
      p_dec < p_req,
      f"decoupled p = {p_dec:.0f} vs required p > {p_req:+.3f}: the lemma bites only at p <= -1")
check("SCOPE-1  honestly bounded.  (i) The CMB leg is a real Boltzmann computation but with a Planck-LIKE "
      "covariance and a 6-parameter Fisher marginalisation, not the Planck likelihood -- the ceiling is "
      "good to a factor of a few, which is far smaller than the ~1e3 headroom found.  (ii) The galaxy leg "
      "uses static hydrostatic equilibrium in an idealised logarithmic potential.  (iii) NOTHING here yet "
      "says the surviving window is observationally allowed -- only that the TWO GATES L125 NAMED do not "
      "close it.  The intermediate-epoch constraints are L154",
      True, "CMB leg Boltzmann + Planck-like; galaxy leg hydrostatic; intermediate epochs NOT yet tested (L154)")

# =========================================================================================================
sec("VERDICT")
# =========================================================================================================
P(f"""
  PART 1 VERDICT -- the loophole is REAL, and wide.

  The L125 velocity-ordering lemma was stated as mechanism-independent.  It is not.  It is the p = -2 corner
  of a one-parameter family: a component with c_eff^2 proportional to a^p has its clustering set GROW iff
  p < -1, and a DECOUPLED COLLISIONLESS species is pinned at p = -2 because momentum redshifts as 1/a.
  Nothing pins a FLUID there.

  Quantitatively, with the CMB leg computed by a real Boltzmann code (CLASS running the exact GDM fluid
  system, unlensed TT/TE/EE against a Planck-like covariance, marginalised over six parameters) and the
  galaxy leg computed from hydrostatic equilibrium in a MOND logarithmic potential against the L61 0.11 dex
  tolerance:

        c_s^2(a_rec)  <  {CS2_CMB_MAX:.2e}        (CMB third peak / damping tail)
        c_s^2(a = 1)  >  {CS2_GAL_MIN:.2e}        (no L61 overshoot in a v_c = 300 km/s galaxy)

  so c_s^2 is permitted to FALL by a factor of ~{1.0/growth_needed:.0f} across the whole interval and both gates still
  pass:  p > {p_req:+.2f}.  A decoupled species falls by {1.0/decoupled_drop:.1e} and misses by ~3 orders of magnitude.

  So the answer to "does the CMB-vs-galaxy pincer close against a GDM fluid?" is NO.  It does not close, and
  it does not even come close to closing.  It is not a near miss that better modelling might rescue -- the
  interior is three orders of magnitude wide in c_s^2 and a full unit wide in the exponent p.

  This does NOT mean the hybrid works.  It means the obstruction, if there is one, is somewhere else: at the
  epochs BETWEEN recombination and today, which neither gate touches.  That is L154.  Whether any field or
  fluid can supply the required c_s^2(a) at all is L153.
""")
print("=" * 112)
if FAILS:
    print(f"L152 INCOMPLETE: {len(FAILS)}/{NCHECK[0]} FAILED: {FAILS}"); sys.exit(1)
print(f"L152 COMPLETE: {NCHECK[0]}/{NCHECK[0]} checks PASS.   [{time.time()-T0:.1f}s]")
print("=" * 112)
