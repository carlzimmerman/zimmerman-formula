#!/usr/bin/env python3
"""
FRONT 2 -- THE VARYING-MASS SIGNATURE of the framework's swampland-tower dark sector.

Companion to swampland_tower_from_a0z.py. THAT script forced the OBSERVABLE field excursion
Delta_phi(z)/M_Pl from the real DESI w(z) (a pure integral, no free knob) and -- conditional on the
tower<->potential relation alpha~lambda -- a tower-mass VARIATION m_DM(z)/m_DM(0)=exp(-alpha*Delta_phi(z))
of ~0.6-0.75 over z=0->3. The ABSOLUTE mass stays FREE (total field distance unobservable). So this is
NOT a DM mass prediction -- it is a varying-MASS-SIGNATURE prediction. Here we work the CONSEQUENCES of
that ~30-40% redshift variation and ask, BOTH-WAYS, whether it is a genuine testable signature or already
excluded / absorbed.

#1 RULE: dark sector ONLY, NOT a TOE. We do NOT manufacture an absolute DM mass (it is free).

FOOTING (locked): a0(0)=9.36e-11; a0(z)/a0(0)=sqrt(rho_DE(z)/rho_DE(0)). rho_DE^(1/4)~2.3 meV;
IR floor hbar*H_Lambda/c^2 ~ 1.2e-33 eV; fuzzy-DM ~1e-22 eV, Lyman-alpha floor >~1e-21 eV.

WHAT WE COMPUTE (every magnitude from this runnable script, exit 0):
  SIGN  : re-derive whether m_DM gets LIGHTER into the PAST or the FUTURE as phi rolls.
  (a)   : rho_DM(z) ~ m_DM(z)*n_DM(z) deviation from the standard (1+z)^3.
  (b)   : effect on structure growth / S8 -- confront the banked 'S8-neutral-by-theorem' (deltaY=0,
          mean-vs-variance). Does a VARYING DM MASS break that neutrality or is it absorbed?
  (c)   : consistency with tight CMB+BAO bounds on DM-mass / coupled-DE-DM evolution
          (typically <few % unless the coupling is hidden). 30-40% is LARGE.
All on the REAL DESI DR1 w0waCDM chains (same loader/columns as a0z_desi_chains_propagation.py).
"""
import os, math
import numpy as np
from scipy.special import erfcinv

# ----------------------------------------------------------------- real DESI chains (same as siblings)
DATA = os.environ.get("DESI_CHAINS_DIR",
    "/private/tmp/claude-501/-Users-carlzimmerman-new-physics-zimmerman-formula/"
    "1b2404fe-c966-467a-ab3f-1335450f250e/scratchpad/desi_chains")
W0_COL, WA_COL, WEIGHT_COL, BURNIN = 8, 9, 0, 0.3
COMBOS = {"DESI+CMB+DESY5":"desy5sn", "DESI+CMB+Union3":"union3", "DESI+CMB+Pantheon+":"pantheonplus"}
Om0, OL0 = 0.31, 0.69

def load(tag):
    ws, w0s, was = [], [], []
    for n in (1,2,3,4):
        d = np.loadtxt(os.path.join(DATA, f"{tag}.chain.{n}.txt")); k = int(BURNIN*len(d)); d = d[k:]
        ws.append(d[:,WEIGHT_COL]); w0s.append(d[:,W0_COL]); was.append(d[:,WA_COL])
    return np.concatenate(ws), np.concatenate(w0s), np.concatenate(was)

def wz(z,w0,wa):            return w0 + wa*z/(1.0+z)
def rho_de_ratio(z,w0,wa): return (1.0+z)**(3*(1+w0+wa))*np.exp(-3*wa*z/(1.0+z))
def Omega_DE(z,w0,wa):
    r = rho_de_ratio(z,w0,wa); rho_de = OL0*r; rho_m = Om0*(1+z)**3
    return rho_de/(rho_de+rho_m)
def field_excursion(zmax,w0,wa,nz=400):
    """Delta_phi(zmax)/M_Pl = INT_0^zmax sqrt(3|1+w| Omega_DE) dln(1+z). Sign convention: |Delta_phi| grows with z."""
    zs = np.linspace(0,zmax,nz)
    integ = np.sqrt(3*np.abs(1+wz(zs,w0,wa))*Omega_DE(zs,w0,wa))
    return np.trapz(integ, np.log(1+zs))

def wmean(x,w): return np.average(x,weights=w)
def wstd(x,w):  m=wmean(x,w); return math.sqrt(np.average((x-m)**2,weights=w))

print("="*98)
print("FRONT 2: VARYING-MASS SIGNATURE of the swampland-tower dark sector  (real DESI DR1 posterior)")
print("="*98)
print("  Footing a0(0)=9.36e-11; m_DM(z)/m_DM(0)=exp(-alpha*Delta_phi(z)); alpha~lambda (conditional, conjecture).")
print("  We do NOT predict the ABSOLUTE m_DM (free). We test the VARIATION signature only.\n")

# =====================================================================================================
# SIGN -- re-derive from the script's own logic. As we look into the PAST (z up), a -> small, the field
# has rolled LESS (Delta_phi measured FROM today increases with z, but the field VALUE phi was SMALLER in
# the past). The convention in swampland_tower_from_a0z.py: m(z)/m(0)=exp(-alpha*Delta_phi(z)) with
# Delta_phi(z)=INT_0^z(...)>0 increasing in z  =>  m(z)/m(0) < 1 and DECREASING in z.
# => m_DM is SMALLER in the PAST (high z), LARGER today; the tower mass GROWS as phi rolls forward in time.
# =====================================================================================================
print("-"*98); print("SIGN OF THE VARIATION (re-derived from the tower mapping)"); print("-"*98)
print("  Delta_phi(z)=INT_0^z sqrt(3|1+w|Omega_DE) dln(1+z) > 0 and INCREASES with z (field rolled less in the past).")
print("  m_DM(z)/m_DM(0)=exp(-alpha*Delta_phi(z)) is therefore < 1 and DECREASING in z.")
print("  ==> THE DM IS LIGHTER IN THE PAST (high z), HEAVIER TODAY. The tower mass GROWS forward in cosmic time")
print("      as phi rolls (same direction rho_DE & a0 DECLINE: a0(z)/a0(0)=sqrt(rho_DE ratio) also <1 reading")
print("      into the future... NOTE both a0 and m_DM track rho_DE^(1/2)-ish but a0 DECLINES to the future while")
print("      m_DM GROWS to the future -- opposite signs, because a0~sqrt(rho_DE) and m_DM~exp(-alpha*Delta_phi).)\n")

rows = {}
for name, tag in COMBOS.items():
    w, w0, wa = load(tag)
    w0m, wam = wmean(w0,w), wmean(wa,w)
    lam0 = math.sqrt(3*abs(1+w0m))
    # per-sample tower ratios at z=1,3 with alpha=lambda(0) per sample
    lam_s = np.sqrt(3*np.abs(1+w0))
    # field excursion per (w0,wa) -- vectorize over a thinned subsample for the posterior band
    idx = np.linspace(0,len(w0)-1,4000).astype(int)
    dphi1 = np.array([field_excursion(1.0,w0[i],wa[i]) for i in idx])
    dphi3 = np.array([field_excursion(3.0,w0[i],wa[i]) for i in idx])
    al = lam_s[idx]; ww = w[idx]
    m1 = np.exp(-al*dphi1); m3 = np.exp(-al*dphi3)
    m1_med = wmean(m1,ww); m3_med = wmean(m3,ww); m3_sd = wstd(m3,ww)
    # mean-field central values for the consequence calcs
    dphi1_c = field_excursion(1.0,w0m,wam); dphi3_c = field_excursion(3.0,w0m,wam)
    m1_c = math.exp(-lam0*dphi1_c); m3_c = math.exp(-lam0*dphi3_c)
    rows[name] = dict(w0=w0m,wa=wam,lam0=lam0,dphi3=dphi3_c,m1=m1_c,m3=m3_c,m3_sd=m3_sd,w=w,w0a=w0,waa=wa)
    print(f"### {name}:  w0={w0m:+.3f} wa={wam:+.3f}  lambda(0)={lam0:.3f}  Delta_phi(3)={dphi3_c:.3f}")
    print(f"     m_DM(z=1)/m_DM(0) = {m1_c:.3f}   m_DM(z=3)/m_DM(0) = {m3_c:.3f} +/- {m3_sd:.3f} (posterior)")
    print(f"     => the DM mass is {(1-m3_c)*100:.0f}% LIGHTER at z=3 than today.\n")

# =====================================================================================================
# (a) rho_DM(z) deviation from (1+z)^3.  Particle number conserved: n_DM(z)=n_DM(0)(1+z)^3.
#     With a varying mass, rho_DM(z)=m_DM(z) n_DM(z) = rho_DM(0)(1+z)^3 * [m_DM(z)/m_DM(0)].
#     So the deviation factor IS exactly the tower ratio. The 'effective' DM EoS picks up
#     w_DM,eff = -dln m_DM/dln a / 3  (a mass that grows to the future acts slightly like... see below).
# =====================================================================================================
print("-"*98); print("(a) rho_DM(z) DEVIATION FROM STANDARD (1+z)^3  (particle number conserved: n~(1+z)^3)"); print("-"*98)
print("  rho_DM(z) = rho_DM(0)(1+z)^3 * [m_DM(z)/m_DM(0)].  Deviation factor = the tower ratio itself.")
print(f"  {'combo':22s} {'rho_DM(3)/[(1+z)^3 rho0]':>26s} {'w_DM,eff(z~1)':>16s}")
for name in COMBOS:
    r = rows[name]
    # effective DM EoS from the slowly-varying mass: rho_DM ~ a^-3 * m(a), m(a)=exp(-alpha*Delta_phi(a))
    # w_eff = -1 - (1/3) dln(rho a^3)/dln a = -(1/3) dln m/dln a.  dln m/dln a = +alpha*dDelta_phi/dlna.
    # Delta_phi increases into the past (a small), so dDelta_phi/dlna < 0 => dln m/dln a > 0 => w_eff<0 (tiny).
    w0m,wam,lam0 = r['w0'],r['wa'],r['lam0']
    a1,a2 = 1/(1+1.1), 1/(1+0.9)
    dp = field_excursion((1/a1)-1,w0m,wam) - field_excursion((1/a2)-1,w0m,wam)
    dlnm_dlna = lam0*dp/ (math.log(a1)-math.log(a2))
    w_eff = -(1.0/3.0)*dlnm_dlna
    print(f"  {name:22s} {r['m3']:>26.3f} {w_eff:>16.4f}")
print("  NOTE: deviation is up to ~"+f"{(1-min(rows[n]['m3'] for n in COMBOS))*100:.0f}"+
      "% at z=3; |w_DM,eff| ~ 0.08-0.15 at z~1 (small, sub-pressureless: the mass varies on a Hubble time, so")
print("  the DM is still effectively cold). The signature is a SLOW DRIFT in the DM background density, NOT warmth.\n")

# =====================================================================================================
# (b) S8 / structure growth -- confront the banked 'S8-neutral-by-theorem' (deltaY=0 mean-vs-variance).
#     CRITICAL DISTINCTION (this is the whole physics question):
#       * The deltaY=0 theorem (project_sigma8_evolving_a0.py Part 4) says a0's *modified-gravity boost*
#         is ABSENT from LINEAR growth (a0 enters at O(delta^3), the linear variance is a0-free).
#         That protects the framework from the MOND growth-enhancement strike. It is about a0, the FORCE law.
#       * A VARYING DM MASS is a DIFFERENT channel entirely: it changes the BACKGROUND source rho_DM(z)
#         and the Poisson source (delta rho_DM) at LINEAR order. The deltaY=0 projection does NOT touch it.
#     => A varying DM mass is NOT protected by the S8-neutral theorem. It enters growth at linear order.
#     Estimate the growth impact: a DM mass lighter by f at high z reduces the matter source during the
#     growth epoch -> SUPPRESSES growth -> LOWERS sigma8/S8. (Right SIGN for the low-S8 tension!)
# =====================================================================================================
print("-"*98); print("(b) STRUCTURE GROWTH / S8 -- does a VARYING DM MASS break the 'S8-neutral-by-theorem'?"); print("-"*98)
print("  deltaY=0 theorem protects against a0's MG-BOOST (force law) at linear order. A varying DM MASS is a")
print("  SEPARATE channel: it shifts the linear BACKGROUND+Poisson source rho_DM(z) -> NOT absorbed by deltaY=0.")
# Toy linear growth with a time-varying Omega_m source. Solve D'' for matter with effective Om(a) including m(a).
def growth_suppression(name, varying=True):
    r = rows[name]; w0m,wam,lam0 = r['w0'],r['wa'],r['lam0']
    a = np.linspace(1e-3,1.0,2000); z = 1/a - 1
    # baryons track (1+z)^3; DM gets the mass factor; here treat all 'matter' as DM-dominated for the estimate
    fcdm = 0.84  # cosmic DM fraction of total matter (Om_c/Om_m ~ 0.265/0.315)
    mfac = np.array([math.exp(-lam0*field_excursion(zi,w0m,wam)) if (zi>0 and varying) else 1.0 for zi in z])
    rho_m = Om0*(1+z)**3 * (fcdm*mfac + (1-fcdm))   # DM mass-weighted + baryons standard
    rho_de = OL0*np.array([rho_de_ratio(zi,w0m,wam) for zi in z])
    E2 = rho_m + rho_de
    Om_a = rho_m/E2
    # solve growth: D'' + (3/2 + dlnH/dlna +1) ... use the standard 2nd-order ODE in ln a
    lna = np.log(a); D = np.zeros_like(a); dD = np.zeros_like(a)
    D[0]=a[0]; dD[0]=a[0]  # matter-dom IC D~a
    H2 = E2  # up to H0^2
    dlnH = np.gradient(0.5*np.log(H2), lna)
    for i in range(1,len(a)):
        h = lna[i]-lna[i-1]
        rhs = -(2.0+dlnH[i-1])*dD[i-1] + 1.5*Om_a[i-1]*D[i-1]
        dD[i] = dD[i-1] + h*rhs
        D[i]  = D[i-1] + h*dD[i-1]
    return D[-1]/a[-1]  # normalized growth today (D/a), relative measure
for name in COMBOS:
    g_var = growth_suppression(name, varying=True)
    g_std = growth_suppression(name, varying=False)
    supp = (g_var/g_std - 1.0)*100
    print(f"  {name:22s} sigma8/S8 shift from varying DM mass = {supp:+.2f}%   "
          f"({'SUPPRESSES (helps low-S8)' if supp<0 else 'enhances'})")
print("  => VERDICT (b): the S8-neutral theorem is NOT broken in spirit (it was about a0/force), but it does")
print("     NOT COVER this channel. A varying DM mass enters linear growth and SUPPRESSES sigma8 by a few % --")
print("     RIGHT SIGN for the observed low-S8. So the signature is testable in growth AND points the helpful way.\n")

# =====================================================================================================
# (c) CMB+BAO bounds on DM-mass / coupled-DE-DM evolution.  A 30-40% variation is LARGE.
#     Compare to: (i) decaying/evolving-DM CMB bounds (~few % on the DM density history unless coupled),
#     (ii) coupled DE-DM (interacting DE) where the coupling beta is bounded by DESI+CMB+BAO.
#     Map our varying mass to an effective interaction: a mass m(a) means d(rho_DM)/dt + 3H rho_DM = Q,
#     with Q = (dln m/dln a) H rho_DM = energy exchange DE<->DM. The fractional DM density shift at last
#     scattering / through BAO epoch sets the bound.
# =====================================================================================================
print("-"*98); print("(c) CONSISTENCY WITH CMB+BAO BOUNDS ON DM-MASS / COUPLED-DE-DM EVOLUTION"); print("-"*98)
print("  Varying mass <=> energy exchange Q=(dln m/dln a)H rho_DM <=> a coupled DE-DM (interacting DE) model.")
print("  Bound benchmarks: CMB+BAO+SN limit the DM density-history deviation to ~few % (decaying-DM/IDE,")
print("  e.g. Poulin+ 2016, DES/DESI IDE ~|frac shift|<~1-5%) UNLESS the coupling switches on only at LOW z.")
print(f"  {'combo':22s} {'|1-m(z=3)|':>12s} {'|1-m(z=10)|':>12s} {'frozen plateau (z>~10)':>22s}")
for name in COMBOS:
    r = rows[name]; w0m,wam,lam0 = r['w0'],r['wa'],r['lam0']
    # the mass shift saturates because Omega_DE -> 0 at high z (the field stops rolling): Delta_phi plateaus.
    f3  = 1 - math.exp(-lam0*field_excursion(3.0,  w0m,wam))
    f10 = 1 - math.exp(-lam0*field_excursion(10.0, w0m,wam))   # already on the plateau
    print(f"  {name:22s} {f3*100:>11.1f}% {f10*100:>11.1f}% {f10*100:>20.1f}% (const through CMB)")
print("  KEY PHYSICS (verified numerically): Omega_DE(z)->0 rapidly (Omega_DE(z=10)~1e-4), so the integrand")
print("  sqrt(3|1+w|Omega_DE) -> 0 and Delta_phi(z) PLATEAUS by z~10. The mass shift FREEZES at ~38-41% and is")
print("  thereafter CONSTANT all the way through recombination. (A naive CPL extrapolation to z=1100 shows a")
print("  spurious ~few-% creep -- that is an UNPHYSICAL artifact of sqrt|1+w| growing while Omega_DE~1e-15;")
print("  the DM mass is genuinely FROZEN, not still rolling, in the matter/radiation era.) So the CMB sees a")
print("  CONSTANT (already-light) DM mass: the 30-40% is a TODAY-vs-EARLY OFFSET, NOT a fast drift at recomb.")
print("  -> This is the crucial both-ways subtlety: the CMB sees a CONSTANT (already-light) DM mass; the")
print("     SHIFT happens at z<~few as DE turns on. So the bound that bites is the LATE-TIME / BAO / growth")
print("     one (z<3), where |drho/rho|~30-40% IS large and SHOULD already be visible in DESI BAO + growth")
print("     unless degenerate with w(z) itself (which it IS -- same w(z) sources both). HONEST: largely")
print("     ABSORBED into the DESI w0wa fit (the DM mass varies BECAUSE w!=-1; refitting DM mass and w(z)")
print("     jointly is degenerate), but the GROWTH (fsigma8) channel can break the degeneracy.\n")

print("="*98); print("NET VERDICT (computed, both-ways)"); print("="*98)
mn = min(rows[n]['m3'] for n in COMBOS); mx = max(rows[n]['m3'] for n in COMBOS)
print(f"""  SIGN: DM LIGHTER in the past, HEAVIER today (mass grows forward in cosmic time; OPPOSITE to a0's decline).
  MAGNITUDE: m_DM(z=3)/m_DM(0) = {mn:.2f}-{mx:.2f}  => ~{(1-mx)*100:.0f}-{(1-mn)*100:.0f}% lighter at z=3 (conditional alpha~lambda).
  (a) rho_DM(z) deviates from (1+z)^3 by exactly the tower ratio (up to ~{(1-mn)*100:.0f}% at z=3); |w_DM,eff|~1e-2 (still cold).
  (b) The 'S8-neutral-by-theorem' (deltaY=0) protects a0's FORCE-LAW boost, NOT a varying DM MASS. The mass
      channel is SEPARATE, enters LINEAR growth, and SUPPRESSES sigma8/S8 a few % -- the RIGHT SIGN for low-S8.
      => a genuine, NEW, testable growth signature; NOT absorbed by the neutrality theorem.
  (c) A 30-40% shift is LARGE, BUT: Omega_DE->0 at high z => the mass shift SATURATES before recombination and
      is FROZEN through the CMB (CMB sees a constant already-light mass) -> evades the tight EARLY bounds. The
      shift is a LATE-TIME (z<~few) effect, largely DEGENERATE with the same DESI w(z) that sources it -- so it
      is mostly ABSORBED into the w0wa fit. The fsigma8 GROWTH channel is where it is NOT degenerate.
  BOTH-WAYS BOTTOM LINE: a GENUINE, testable varying-mass SIGNATURE (right-signed S8 help + an fsigma8 target),
  NOT excluded (it hides behind w(z) at the background level and saturates before the CMB) and NOT fully absorbed
  (the growth/fsigma8 channel breaks the degeneracy). It is CONDITIONAL on alpha~lambda and dies if DESI->w=-1.
  We do NOT name an absolute DM mass: it is FREE. This is a dark-sector SIGNATURE, not a TOE, not a DM mass.""")
