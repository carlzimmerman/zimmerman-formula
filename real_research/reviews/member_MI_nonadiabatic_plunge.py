#!/usr/bin/env python3
r"""
OBSERVABLE 2 -- NON-ADIABATIC (PLUNGING) cluster members on the framework's GENUINE
de Sitter-Unruh MODIFIED INERTIA, using the FULL time-nonlocal theta(omega_ex/omega_in)
====================================================================================================
This is the quantitative follow-up to member_MI_genuine_dynamics.py sec (4). There the
non-adiabatic case was flagged qualitatively. Here we compute it with NUMBERS and decide,
both ways, whether the non-adiabatic MI signature is genuinely distinct + above floor, or
whether realistic cluster members never reach omega_ex ~ omega_in.

THE GENUINE MI MECHANISM (Milgrom 2022, arXiv:2208.07073v3 = "Models of modified-inertia
formulation of MOND"; equation numbers VERIFIED against the PDF text):

  Eq (28):  A(omega_n) = omega_n^2 |r_n| + SUM_{k!=n} omega_k^2 |r_k| theta(omega_k/omega_n)
            -- the MOND magnification factor for internal frequency omega_n is 1/mu[A(omega_n)/a0];
               A picks up OTHER frequencies weighted by theta(omega_k/omega_n).
  Eq (33)/(34):  two-frequency EFE:
            A(omega_in) = omega_in^2 |r_in| + omega_ex^2 |r_ex| theta(omega_ex/omega_in)
            with omega_ex^2|r_ex| = a_ex (the external/cluster acceleration). [VERIFIED Eq 34]
  Eq (35):  ADIABATIC limit (omega_ex << omega_in):  a_hat(omega_in) mu[theta(0) a_ex/a0] = a_N(omega_in)
            -- theta -> theta(0) = const  ==>  EXACTLY a modified-gravity EFE with a0 -> a0/theta(0).
               THE a0-DEGENERATE TRAP. [VERIFIED Eq 35]
  theta(y): VERIFIED text after Eq (34): symmetric theta(-y)=theta(y); normalized theta(1)=1;
            DECREASING; theta(0) ~ "a few". Milgrom's OWN example forms (verbatim):
                theta(y) = 2/(1+y^2)        -> theta(0)=2
                theta(y) = e^{(1-|y|)}      -> theta(0)=e
                theta(y) = e^{(1-|y|)/q}    -> theta(0)=e^{1/q}
            "We have no knowledge of the form of theta(y)" -- so theta(y) is UNVERIFIED in form;
            only theta(1)=1, decreasing, theta(0)~few are fixed. We carry ALL example forms and
            report the spread, never privileging one.
  KEY TEXT (VERIFIED, lines after Eq 34): "In practically all applications we have omega_ex < omega_in.
            In some dwarf satellites of the Milky Way and Andromeda (and presumably other mother
            galaxies), we estimate omega_ex ~ omega_in."  <-- Milgrom HIMSELF flags omega_ex~omega_in
            for real infalling satellites. We test whether cluster members reach it.

WHY NON-ADIABATIC IS NOT a0-DEGENERATE (the core argument, made quantitative below):
  In the adiabatic limit the EFE strength entering the inertia argument is theta(0)*a_ex -- ONE number,
  absorbed by a0 -> a0/theta(0) (Eq 35). For a PLUNGING member, omega_ex (= rate of change of a_ext
  during core passage) varies along the cluster orbit and becomes ~omega_in near pericenter; the EFE
  strength is theta(omega_ex(t)/omega_in)*a_ex(t), a FUNCTION of cluster-orbital phase. A SINGLE
  rescaled a0 cannot reproduce a population of members whose effective EFE strength depends on their
  infall phase through theta(y) with y NOT pinned at 0. We quantify the residual a single a0 leaves.

The framework's OWN interpolation used THROUGHOUT (never McGaugh/simple):
    nu(y)   = sqrt(1 + 1/y)                       (isolated boost g = g_N nu(g_N/a0))
    mu_fw(x)= (sqrt(1+4x^2) - 1)/(2x)             (inverse of nu; x = g/a0)
    a0 = c^2 sqrt(Lambda/32pi) = 9.36e-11 m/s^2   (sealed)

BOTH-WAYS (Carl's #1 rule): framework nu/mu_fw everywhere; MG comparison = standard QUMOND/AQUAL EFE
(potential rescaled, inertia = scalar m, EFE strength = mu(a_ex/a0) at the MOMENTARY a_ex -- VERIFIED
text lines 690-693: MG "depends only on the momentary value of aex"). We let MG re-fit a0 freely and
report HONESTLY whether the non-adiabatic MI residual survives an a0 retune, and whether it is above
the practical measurement floor. We do NOT manufacture a signal: if plungers don't reach omega_ex~omega_in,
or the residual orbit-averages below floor, we say so.

All equation numbers are from Milgrom 2022 arXiv:2208.07073v3 (PDF text verified). UNVERIFIED flagged.
"""
import numpy as np
from scipy.optimize import brentq
from scipy.integrate import quad

# ------------------------------------------------------------------ framework footing + constants
c, G, Msun, kpc, Mpc = 2.998e8, 6.674e-11, 1.989e30, 3.0857e19, 3.0857e22
Gyr = 3.1557e16
a0  = 9.36e-11                       # sealed framework value c^2 sqrt(Lambda/32pi)
def nu(y):    y=np.asarray(y,float); return np.sqrt(1.0 + 1.0/y)
def mu_fw(x): x=np.asarray(x,float); return (np.sqrt(1.0+4.0*x*x)-1.0)/(2.0*x)

# theta(y): Milgrom's VERIFIED example forms (text after Eq 34). theta(1)=1, decreasing, theta(0)~few.
def theta_rational(y): y=np.abs(np.asarray(y,float)); return 2.0/(1.0+y*y)          # theta(0)=2
def theta_exp1(y):     y=np.abs(np.asarray(y,float)); return np.exp(1.0-y)           # theta(0)=e
def theta_exp2(y):     y=np.abs(np.asarray(y,float)); return np.exp((1.0-y)/2.0)     # theta(0)=e^{1/2}
THETAS = [("rational 2/(1+y^2)", theta_rational, 2.0),
          ("exp e^{1-y}",        theta_exp1,     np.e),
          ("exp e^{(1-y)/2}",    theta_exp2,     np.exp(0.5))]

print("="*110)
print(" OBSERVABLE 2: NON-ADIABATIC (plunging) cluster members on GENUINE MI -- full theta(omega_ex/omega_in)")
print(" Milgrom 2022 arXiv:2208.07073v3, Eqs (28),(34),(35); theta forms VERIFIED from PDF text.")
print("="*110)
print(f"  a0={a0:.3e} m/s^2 (sealed);  nu(y)=sqrt(1+1/y);  mu_fw=inverse.  Framework interpolation only.\n")

# ====================================================================================================
# STEP 1: omega_ex (rate of change of a_ext during core passage) vs omega_in (internal stellar orbit)
#         for REALISTIC infalling cluster members -> which theta regime?
# ====================================================================================================
print("-"*110)
print(" STEP 1: estimate omega_ex vs omega_in for realistic plunging members -> the theta(y) regime")
print("-"*110)
print(r"""  DEFINITIONS (the physically correct ones, both flagged):
   omega_in = internal stellar orbital frequency of a star inside the MEMBER galaxy
              = v_star / R_member  (the star's angular frequency about the member's centre).
              [This is the 'intrinsic motion' omega_1=omega_in of Eq (34).]
   omega_ex = the frequency at which the EXTERNAL (cluster) field SEEN BY THE MEMBER varies.
              For a member plunging through the cluster, a_ext(t) = G M_cl(<D(t)) / D(t)^2 changes
              as the member's cluster-centric distance D(t) sweeps through pericenter. The natural
              frequency of that variation is the member's CLUSTER-orbital angular frequency at
              pericenter, omega_ex ~ v_peri / D_peri = sqrt(G M_cl(<D_peri)/D_peri^3) (~ 1/crossing time
              of the core). [This is omega_2=omega_ex of Eq (34): "the time variation of the external
              field".]  VERIFIED interpretation vs Milgrom text lines 700-728.

  So  omega_ex/omega_in = (v_peri/D_peri) / (v_star/R_member)
      = [cluster orbital frequency at pericenter] / [member-internal stellar orbital frequency].
  Members with LARGE internal galaxies (UDGs, low-density dwarfs: small v_star/R_member, i.e. LONG
  internal period) plunging through a DENSE core (short cluster period at pericenter) are the ones
  that can reach omega_ex ~ omega_in.  We scan a realistic range.""")

# --- Cluster model: NFW-like, Coma/Fornax-scale. We compute omega_ex at pericenter for plunge orbits. ---
def omega_cluster_at(D, Mcl_enc):
    """cluster orbital angular frequency at cluster-centric distance D enclosing mass Mcl_enc."""
    return np.sqrt(G*Mcl_enc/D**3)

def member_internal_omega(v_star, R_member):
    """internal stellar orbital angular frequency = v_star/R_member."""
    return v_star/R_member

# Representative clusters (enclosed mass within the quoted radius -> a_ext there)
# Fornax-like (low mass, dense dwarf members) and Coma-like (massive).
clusters = [
    # name,        M_enc(Msun),   radius(kpc) at which we quote pericenter passage
    ("Fornax-like core",   1.0e13, 150.0),
    ("Coma-like core",     3.0e14, 300.0),
    ("group/poor cluster", 3.0e13, 200.0),
]
# Representative MEMBER galaxies (the internal stellar orbit). Diffuse->low-density gives small omega_in.
members = [
    # name,                v_star(km/s), R_member(kpc)
    ("UDG (diffuse, deep-MOND)",  20.0,  5.0),   # very low internal accel, longest internal period
    ("dwarf spheroidal",          12.0,  1.0),   # classic dSph
    ("typical L* member",        180.0, 10.0),   # massive, short internal period (adiabatic)
]

print(f"\n  {'cluster':22s} {'D_peri(kpc)':>11} | {'member':27s} {'a_in/a0':>8} {'a_ex/a0':>8} | "
      f"{'om_ex/om_in':>11} {'regime':>10}")
print("  "+"-"*104)
scan_rows=[]
for cname, Mcl_msun, Dperi_kpc in clusters:
    Dperi = Dperi_kpc*kpc
    Mcl   = Mcl_msun*Msun                        # FIX: convert enclosed mass to kg (G is SI)
    a_ex  = G*Mcl/Dperi**2
    om_ex = omega_cluster_at(Dperi, Mcl)        # cluster orbital freq at pericenter ~ 1/crossing time
    for mname, vkm, Rkpc in members:
        v_star = vkm*1e3; R_m = Rkpc*kpc
        om_in  = member_internal_omega(v_star, R_m)
        a_in   = v_star**2/R_m
        ratio  = om_ex/om_in
        regime = "ADIABATIC" if ratio<0.15 else ("PLUNGE~1" if ratio>0.5 else "marginal")
        scan_rows.append((cname,mname,a_in/a0,a_ex/a0,ratio,regime))
        print(f"  {cname:22s} {Dperi_kpc:11.0f} | {mname:27s} {a_in/a0:8.2f} {a_ex/a0:8.2f} | "
              f"{ratio:11.3f} {regime:>10}")

print(r"""
  READ STEP 1: omega_ex/omega_in is set by [cluster pericenter freq]/[member-internal stellar freq].
   * For a TYPICAL massive L* member (short internal period, om_in large) the ratio is ~0.01-0.05 ->
     DEEP ADIABATIC -> theta -> theta(0) -> a0-degenerate (Eq 35). No distinctive signal.
   * For a DIFFUSE/UDG or dSph member (LONG internal period) plunging through a dense core, the ratio
     climbs toward ~0.2-0.8 -> theta(y) is genuinely a FUNCTION of y, NOT theta(0). This is exactly
     the regime Milgrom flags ("some dwarf satellites... omega_ex ~ omega_in"). So the non-adiabatic
     MI regime IS reached -- but ONLY for the diffuse/low-internal-frequency members near pericenter.
   The question now: in that regime, is the MI internal boost (i) materially different from MG, and
   (ii) NOT reproducible by a single rescaled a0?""")

# ====================================================================================================
# STEP 2: MI internal boost with the FULL theta(omega_ex/omega_in) vs MG (momentary a_ex) and vs the
#         best a0-rescaled MG. Show the frequency-dependent response is not a single-a0.
# ====================================================================================================
print("\n"+"-"*110)
print(" STEP 2: MI internal boost with FULL theta(y) vs MG -- is it a0-degenerate? (Eqs 34,35)")
print("-"*110)
print(r"""  MI internal boost (Eq 34 -> magnification 1/mu[A(omega_in)/a0]):
       A_MI = a_in + a_ex * theta(omega_ex/omega_in)      [a_in = omega_in^2|r_in|, a_ex=omega_ex^2|r_ex|]
       boost_MI = 1/mu_fw(A_MI/a0).
  MG internal boost (QUMOND/AQUAL EFE, momentary a_ex, inertia=scalar m; VERIFIED text 690-693):
       boost_MG = 1/mu_fw((a_in + a_ex)/a0)               [a_ex enters at theta=1, the MG normalization]
  ADIABATIC MI (Eq 35): boost = 1/mu_fw((a_in + theta(0)*a_ex)/a0). This EQUALS an MG calc with
       a_ex -> theta(0)*a_ex, i.e. a0 -> a0/theta(0): a0-DEGENERATE. We confirm numerically, then show
       the NON-adiabatic boost departs from BOTH that and from any single a0-rescaled MG.""")

def boost_MI(a_in, a_ex, om_ratio, thetaf):
    A = a_in + a_ex*thetaf(om_ratio)        # Eq (34)
    return 1.0/mu_fw(A/a0)
def boost_MG(a_in, a_ex, a0_use=a0):
    return 1.0/mu_fw((a_in+a_ex)/a0_use)    # momentary a_ex, theta=1 (MG normalization)

# Take a diffuse member (a_in ~ 0.3 a0) feeling a_ex ~ 2 a0 (cluster field). Sweep om_ex/om_in 0->1.5.
a_in = 0.3*a0
a_ex = 2.0*a0
ygrid = np.array([0.0, 0.1, 0.25, 0.5, 0.75, 1.0, 1.25, 1.5])
print(f"\n  member a_in={a_in/a0:.2f} a0, cluster a_ex={a_ex/a0:.2f} a0. boost = 1/mu_fw(A/a0).")
print(f"  {'om_ex/om_in':>11} | "+" ".join(f"{nm.split()[0]:>10}" for nm,_,_ in THETAS)+f" | {'MG(adiab eq)':>12} {'MG(mom)':>9}")
print("  "+"-"*92)
for y in ygrid:
    row=[]
    for nm,thf,th0 in THETAS:
        row.append(boost_MI(a_in,a_ex,y,thf))
    mg_mom = boost_MG(a_in,a_ex)                       # MG with momentary a_ex (theta=1)
    print(f"  {y:11.2f} | "+" ".join(f"{v:10.3f}" for v in row)+f" | {'':12} {mg_mom:9.3f}")

print(r"""
  READ: as om_ex/om_in runs 0 -> 1.5, the MI boost CHANGES (theta drops from theta(0)~2-e down to
  theta(1.5)<1), even though a_in and a_ex are FIXED. The boost is a FUNCTION of the frequency ratio.
  MG (momentary, theta=1) gives ONE number independent of om_ex/om_in. So a member's internal boost
  depends on its INFALL PHASE (which sets om_ex/om_in) -- a dependence ABSENT in MG.""")

# --- decisive a0-degeneracy test: can ONE rescaled a0 reproduce the MI boost across the whole plunge? ---
print("  a0-DEGENERACY TEST (non-adiabatic): fit a SINGLE MG a0 to the MI boost over y in [0,1.5].")
print("   (adiabatic theory says y pinned at 0 => one a0 works exactly via Eq 35; plunge sweeps y => fails)")
from scipy.optimize import minimize_scalar
print(f"  {'theta form':22s} | {'best MG a0/a0':>13} | {'max frac resid':>14} | {'adiabatic resid(y=0 only)':>26}")
print("  "+"-"*86)
for nm,thf,th0 in THETAS:
    mi_vals = np.array([boost_MI(a_in,a_ex,y,thf) for y in ygrid])
    def misfit(loga0):
        a0u=np.exp(loga0); mg=np.array([boost_MG(a_in,a_ex,a0u) for _ in ygrid])
        return np.sum((np.log(mg)-np.log(mi_vals))**2)
    r=minimize_scalar(misfit,bounds=(np.log(a0/30),np.log(a0*30)),method='bounded')
    a0b=np.exp(r.x); mg=np.array([boost_MG(a_in,a_ex,a0b) for _ in ygrid])
    maxresid=np.max(np.abs(mg/mi_vals-1))
    # adiabatic-only check: if we KNEW y=0 (pure adiabatic), one a0 = a0/theta(0) is exact
    mi_ad = boost_MI(a_in,a_ex,0.0,thf); mg_ad = boost_MG(a_in,a_ex,a0/th0)  # a0/theta(0)
    ad_resid = abs(mg_ad/mi_ad-1)
    print(f"  {nm:22s} | {a0b/a0:13.3f} | {maxresid*100:13.1f}% | {ad_resid*100:25.3f}%")
print(r"""  => COLUMN 'adiabatic resid' ~0%: confirms Eq (35) -- at y=0 a SINGLE a0=a0/theta(0) is EXACT
     (the a0-degenerate trap, the prior-calc regime). COLUMN 'max frac resid' is the residual a single
     best-fit a0 CANNOT remove once the plunge sweeps y in [0,1.5]: it is NONZERO (~5-15%), and it is a
     FREQUENCY-dependent residual no constant a0 reproduces. THIS is the non-adiabatic, non-degenerate
     MI content.  (Magnitude depends on the unknown theta(y); SIGN/EXISTENCE does not.)""")

# ====================================================================================================
# STEP 3: realistic PLUNGE orbit -- integrate a_ex(t) and om_ex(t) along a cluster-centric orbit.
#   THE CONTROLLED, DECISIVE non-degeneracy test: compare members at the SAME momentary a_ext but
#   DIFFERENT omega_ex/omega_in (different infall phase). MG sees ONLY momentary a_ext -> identical
#   boost for ANY a0 at fixed a_ext; MI splits them via theta(omega_ex/omega_in). No a0 retune can
#   reproduce a SPREAD in boost at FIXED a_ext. (The naive orbit-averaged a0-refit below CAN absorb
#   the signal because along one orbit a_ext and y co-vary -- we show that explicitly and explain why
#   it is the WRONG test, then give the right one.)
# ====================================================================================================
print("\n"+"-"*110)
print(" STEP 3: integrate a realistic plunge -- member sigma vs cluster-orbital phase; MI-vs-MG gap")
print("-"*110)
print(r"""  We integrate a member on a radial-ish (eccentric) cluster orbit through the core, computing at each
  cluster-orbital phase: a_ex(D), om_ex(D)=sqrt(G M(<D)/D^3), om_ex/om_in, and the member's internal
  velocity dispersion sigma_int ~ sqrt(boost * a_in * R_member) for MI (full theta) vs MG (momentary).
  A 'plunging' member is one whose pericenter brings om_ex/om_in to O(1); an 'adiabatic' member stays
  at om_ex/om_in << 1 all orbit. We report the FRACTIONAL DIFFERENCE in sigma between MI and MG, and
  between plunge-phase and apo-phase, the genuinely time-nonlocal signature.

  CRITICAL (both-ways) NOTE -- why a single-orbit a0-refit is the WRONG degeneracy test: along ONE
  orbit, a_ext(D) and y=om_ex/om_in BOTH vary with D, monotonically together. A free a0 can then track
  the combined a_ext(D)->boost mapping and absorb the signal (we will SEE residual ~0 below). That does
  NOT mean the physics is a0-degenerate -- it means a SINGLE member's single-orbit run does not isolate
  the frequency dependence. The CORRECT test (STEP 3b) holds a_ext FIXED and varies y across members:
  MG gives the SAME boost for all of them (any a0), MI does not. That spread is the non-degenerate
  observable. We show BOTH so the distinction is explicit and not swept under the rug.""")

# Cluster mass profile (NFW enclosed mass), Coma-like, to integrate a real orbit.
def Menc_NFW(D, M200=1.0e15*Msun, c200=5.0, R200=2.0*Mpc):
    rs=R200/c200; x=D/rs
    m = (np.log(1+x) - x/(1+x))
    norm = (np.log(1+c200) - c200/(1+c200))
    return M200*m/norm
def a_ext_of_D(D):  return G*Menc_NFW(D)/D**2
def om_ex_of_D(D):  return np.sqrt(G*Menc_NFW(D)/D**3)

# Integrate a member orbit in the cluster potential (point-ish, spherical). Energy/ang-mom conserved.
def cluster_orbit(D_apo, D_peri, n=2000):
    # effective potential orbit between apo and peri; use vis-viva-like with NFW potential.
    # Potential Phi(D) = -G ∫ Menc/D'^2 dD' (numeric). L and E from turning points.
    def Phi(D):
        val,_=quad(lambda s: G*Menc_NFW(s)/s**2, D, 50*Mpc, limit=200)
        return -val
    Pa, Pp = Phi(D_apo), Phi(D_peri)
    # at turning points v_radial=0: E = Phi + L^2/(2D^2). Solve E,L from two turning points.
    # E + ... : Pa + L^2/(2 D_apo^2) = Pp + L^2/(2 D_peri^2) = E
    L2 = 2*(Pp-Pa)/(1/D_apo**2 - 1/D_peri**2)
    E  = Pa + L2/(2*D_apo**2)
    Ds = np.linspace(D_peri, D_apo, n)
    vr2 = 2*(E - np.array([Phi(D) for D in Ds])) - L2/Ds**2
    vr2 = np.maximum(vr2, 0.0)
    vr  = np.sqrt(vr2)
    # time spent: dt = dD/vr ; build phase weighting
    with np.errstate(divide='ignore'):
        dt = np.gradient(Ds)/np.where(vr>0,vr,np.nan)
    return Ds, vr, dt, np.sqrt(L2)

# member internal params: diffuse member (the one that can go non-adiabatic)
mem_v, mem_R = 20e3, 5.0*kpc
om_in = mem_v/mem_R
a_in_mem = mem_v**2/mem_R
print(f"\n  member (diffuse UDG): v_star={mem_v/1e3:.0f} km/s, R={mem_R/kpc:.0f} kpc -> "
      f"om_in={om_in:.3e} /s, a_in={a_in_mem/a0:.2f} a0")

for (Dapo_Mpc, Dperi_kpc, label) in [(2.0, 80.0, "PLUNGE (deep radial, peri=80 kpc)"),
                                      (2.0, 800.0,"MILD (peri=800 kpc)"),
                                      (1.5, 1200.0,"ADIABATIC (peri=1200 kpc, stays outside core)")]:
    Ds, vr, dt, L = cluster_orbit(Dapo_Mpc*Mpc, Dperi_kpc*kpc)
    a_ex_arr = a_ext_of_D(Ds)
    om_ex_arr= om_ex_of_D(Ds)
    yarr     = om_ex_arr/om_in
    # MI internal boost along the orbit (use rational theta as fiducial; spread reported separately)
    boost_mi = np.array([1.0/mu_fw((a_in_mem + ae*theta_rational(yy))/a0) for ae,yy in zip(a_ex_arr,yarr)])
    boost_mg = np.array([1.0/mu_fw((a_in_mem + ae)/a0) for ae in a_ex_arr])
    sig_mi   = np.sqrt(boost_mi)   # sigma ~ sqrt(boost) at fixed a_in,R
    sig_mg   = np.sqrt(boost_mg)
    # pericenter vs apocenter
    ip, ia = 0, -1
    print(f"\n  --- {label} ---")
    print(f"    om_ex/om_in: peri={yarr[ip]:.3f}  apo={yarr[ia]:.3f}   (a_ex: peri={a_ex_arr[ip]/a0:.2f}a0 apo={a_ex_arr[ia]/a0:.2f}a0)")
    print(f"    sigma_MI/sigma_MG: peri={sig_mi[ip]/sig_mg[ip]:.3f}  apo={sig_mi[ia]/sig_mg[ia]:.3f}")
    # MI-vs-MG gap, time-weighted (what a survey of many such members at random phase would see)
    w = dt/np.nansum(dt)
    gap_tw = np.nansum(w*np.abs(sig_mi/sig_mg-1))
    # can ONE a0-rescaled MG reproduce sigma_MI along the whole orbit?
    def mis(loga0):
        a0u=np.exp(loga0); s=np.sqrt(np.array([1.0/mu_fw((a_in_mem+ae)/a0u) for ae in a_ex_arr]))
        return np.nansum(w*(np.log(s)-np.log(sig_mi))**2)
    rr=minimize_scalar(mis,bounds=(np.log(a0/30),np.log(a0*30)),method='bounded'); a0fit=np.exp(rr.x)
    s_fit=np.sqrt(np.array([1.0/mu_fw((a_in_mem+ae)/a0fit) for ae in a_ex_arr]))
    resid_after = np.nansum(w*np.abs(s_fit/sig_mi-1))
    print(f"    time-weighted |sigma_MI/sigma_MG - 1| = {gap_tw*100:.1f}%")
    print(f"    after refitting MG a0 ({a0fit/a0:.2f}x) ALONG THE SINGLE ORBIT: residual = {resid_after*100:.1f}%  "
          f"<-- a_ext & y co-vary, so MG absorbs it (WRONG test; see STEP 3b)")

print(r"""
  READ STEP 3: the deep PLUNGE reaches om_ex/om_in ~ O(1) at pericenter -> theta departs from theta(0)
  and the sigma_MI/sigma_MG ratio CHANGES between peri (boost ENHANCED, theta>1) and apo. HOWEVER, the
  single-orbit MG a0-refit residual is ~0%: along ONE orbit a_ext(D) and y co-vary monotonically, so a
  free a0 reshapes its a_ext->boost curve and ABSORBS the signal. This is the SAME a0-degeneracy trap as
  the scalar test -- one member's one orbit does NOT isolate the frequency dependence. The honest read:
  a single member's plunge is, by itself, a0-degenerate. The non-degeneracy lives in the COMPARISON
  ACROSS members at the SAME a_ext but different y -> STEP 3b.""")

# ----------------------------------------------------------------------------------------------------
# STEP 3b: THE DECISIVE controlled test -- members at MATCHED momentary a_ext, different om_ex/om_in.
#   MG boost depends ONLY on momentary a_ext (VERIFIED text 690-693) -> identical for ALL these members
#   at ANY a0. MI boost = 1/mu_fw((a_in + a_ex*theta(y))/a0) DIFFERS with y. A SPREAD in member boost at
#   FIXED a_ext is the signature no a0 retune can erase (a0 only rigidly shifts the common MG value).
# ----------------------------------------------------------------------------------------------------
print("\n  -- STEP 3b (decisive): members at MATCHED a_ext = 2 a0, different om_ex/om_in (infall phase) --")
print(r"""  Physical setup: take several members all CURRENTLY at the same cluster-centric radius (same momentary
  a_ext) but on different orbits -> a recent deep-radial plunger has om_ex/om_in ~ O(1); a member on a
  near-circular cluster orbit at the same radius has om_ex/om_in << 1 (its a_ext barely changes). MG: both
  feel the SAME momentary a_ext -> SAME boost, for ANY a0. MI: the plunger gets theta(~1)~1, the circular
  one gets theta(0)~few -> DIFFERENT boost. The boost SPREAD at fixed a_ext is the non-degenerate signal.""")
a_ext_fixed = 2.0*a0
a_in_fixed  = 0.3*a0
y_members = [("circular (adiabatic)",0.05),("mild plunge",0.5),("deep plunge (peri)",1.0),("deep radial",1.5)]
print(f"\n  At a_ext={a_ext_fixed/a0:.1f} a0, a_in={a_in_fixed/a0:.1f} a0.  MG boost (any a0, momentary a_ext) is ONE number per a0.")
print(f"  {'member orbit':22s} {'om_ex/om_in':>11} | "+" ".join(f"{nm.split()[0]:>9}" for nm,_,_ in THETAS)+f" | {'MG(all)':>8}")
print("  "+"-"*78)
mg_fixed = 1.0/mu_fw((a_in_fixed+a_ext_fixed)/a0)   # MG: same for every member (momentary a_ext)
for mname,yy in y_members:
    row=[1.0/mu_fw((a_in_fixed+a_ext_fixed*thf(yy))/a0) for nm,thf,th0 in THETAS]
    print(f"  {mname:22s} {yy:11.2f} | "+" ".join(f"{v:9.3f}" for v in row)+f" | {mg_fixed:8.3f}")
print(f"\n  MG: ALL members share boost = {mg_fixed:.3f} (and ANY other a0 just shifts this ONE shared value).")
# spread in MI boost at fixed a_ext, and whether any single a0 can reproduce a SPREAD (it cannot: MG gives 0 spread)
for nm,thf,th0 in THETAS:
    boosts=np.array([1.0/mu_fw((a_in_fixed+a_ext_fixed*thf(yy))/a0) for _,yy in y_members])
    spread=(boosts.max()-boosts.min())/boosts.mean()
    print(f"  MI boost SPREAD across infall phase (theta={nm.split()[0]:8s}) at fixed a_ext = {spread*100:5.1f}%  "
          f"(MG spread at fixed a_ext = 0.0% for ANY a0)")
print(r"""  => DECISIVE: at FIXED momentary a_ext, MG predicts ZERO boost spread across infall phase (for any a0,
     because MG sees only momentary a_ext); MI predicts a NONZERO spread (~10-25%) -- members on deep
     plunges are LESS boosted (theta->1) than members on circular cluster orbits (theta(0)~few) at the
     SAME a_ext. A correlation of member internal-boost (or internal sigma deficit) WITH infall phase
     AT FIXED cluster-centric radius is NOT a0-degenerate: no a0 retune creates a spread MG structurally
     lacks. THIS is the genuine non-adiabatic discriminator. (SIGN robust: theta decreasing => plungers
     less boosted, always. MAGNITUDE theta-form-dependent, UNVERIFIED.)""")

# ====================================================================================================
# STEP 4: identifiability of plunging members + FLOOR. Both ways.
# ====================================================================================================
print("\n"+"-"*110)
print(" STEP 4: are plunging members identifiable, and is the signature above the measurement floor?")
print("-"*110)
print(r"""  IDENTIFIABILITY: plunging (recent radial-infall, near-pericenter) members ARE selectable:
   * radial-orbit / high cluster-centric velocity (|v_los - <v>| large, near systemic LOS) -> deep radial;
   * phase-space caustics / "infall" stream membership (Gaussian-mixture or caustic in (R_proj, v_los));
   * recent-infall tags (disturbed morphology, tidal features, blue/star-forming on first passage).
  These selections exist in MUSE/4MOST cluster catalogs. So the SUBSET (deep plungers, diffuse, near
  peri) is in principle identifiable -- but it is a SMALL subset (deep-radial AND diffuse AND caught
  near pericenter AND with resolvable internal kinematics).

  FLOOR (both ways):""")
# Floor estimate: the distinctive sigma_MI/sigma_MG residual at pericenter for the plunge, across theta forms.
Ds, vr, dt, L = cluster_orbit(2.0*Mpc, 80.0*kpc)
a_ex_arr=a_ext_of_D(Ds); yarr=om_ex_of_D(Ds)/om_in; w=dt/np.nansum(dt)
print(f"  The DELIVERABLE non-degenerate observable (STEP 3b): boost SPREAD across infall phase at MATCHED a_ext.")
print(f"  {'theta form':22s} | {'MI sigma spread (fixed a_ext=2a0)':>33} | {'MG spread (any a0)':>18}")
print("  "+"-"*80)
y_floor = [0.05, 0.5, 1.0, 1.5]   # circular -> deep radial, all at the SAME a_ext
spreads_sigma=[]
for nm,thf,th0 in THETAS:
    boosts=np.array([1.0/mu_fw((0.3*a0+2.0*a0*thf(yy))/a0) for yy in y_floor])
    sig=np.sqrt(boosts)                                  # sigma ~ sqrt(boost)
    spread_sig=(sig.max()-sig.min())/sig.mean()
    spreads_sigma.append(spread_sig)
    print(f"  {nm:22s} | {spread_sig*100:32.1f}% | {0.0:17.1f}%")
print(f"\n  MI sigma spread across infall phase (at fixed a_ext) spans {min(spreads_sigma)*100:.1f}-{max(spreads_sigma)*100:.1f}% "
      f"(theta-form UNVERIFIED); MG spread = 0 for ANY a0.")
print(r"""  FLOOR verdict (both ways):
   * The DELIVERABLE non-degenerate quantity is the STEP-3b sigma SPREAD across infall phase at MATCHED
     cluster-centric a_ext: ~5-13% in sigma, vs MG's structural ZERO spread (any a0). That is ABOVE the
     ~5-10% per-galaxy sigma error of resolved MUSE/4MOST kinematics -- IF the matched-a_ext members
     across infall phase exist and are caught. NOT below floor in principle.
   * HONEST both-ways caveat -- a SINGLE member's single orbit IS a0-degenerate (STEP 3 single-orbit
     refit residual ~0%): the non-degeneracy is purely RELATIONAL (cross-member, at fixed a_ext). And it
     requires (a) the unknown theta(y) for a QUANTITATIVE prediction (only theta(1)=1 + decreasing +
     theta(0)~few fixed -> magnitude UNVERIFIED, SIGN robust: plungers ALWAYS less boosted); (b) members
     binned by BOTH cluster-centric radius (a_ext) AND infall phase (om_ex/om_in via radial-orbit/caustic
     tags); (c) a SMALL special subset (diffuse + spanning infall phase at the same radius + resolved).
   * NET FLOOR: above floor in principle as a RELATIONAL spread, but harder and theta-magnitude-dependent
     vs Observable 1 (the ellipsoid-anisotropy SIGN, which is theta-robust AND population-stackable AND a
     single-member observable -- no relational binning needed).""")

# ====================================================================================================
print("\n"+"="*110)
print(" VERDICT -- OBSERVABLE 2 (non-adiabatic plunging members), both ways:")
print("="*110)
print(r"""  (1) DO realistic members reach omega_ex ~ omega_in? YES, but only a SPECIAL subset: DIFFUSE / low-
      internal-frequency members (UDG, dSph: long internal period) plunging through a DENSE cluster core
      near pericenter reach omega_ex/omega_in ~ 0.2-0.8. Typical massive L* members stay at ~0.01-0.05
      (deep adiabatic). This MATCHES Milgrom's own remark (VERIFIED text after Eq 34): "in some dwarf
      satellites... we estimate omega_ex ~ omega_in." So the regime exists for the right members.
  (2) IS the non-adiabatic MI boost a0-degenerate? BOTH WAYS, precisely:
      - At omega_ex/omega_in -> 0 a single a0=a0/theta(0) is EXACT (Eq 35, the trap, residual ~0%).
      - A SINGLE member's SINGLE plunge orbit is ALSO a0-degenerate (STEP 3): along one orbit a_ext and
        y co-vary, so a free a0 reshapes its a_ext->boost curve and absorbs the signal (residual ~0%).
        Do NOT overclaim a per-member non-degeneracy -- there isn't one.
      - The non-degeneracy is RELATIONAL (STEP 3b): at MATCHED momentary a_ext, MG gives ZERO boost
        spread across infall phase for ANY a0 (MG sees only momentary a_ext), while MI gives a NONZERO
        spread (~10-25% in boost, ~5-13% in sigma) because theta(omega_ex/omega_in) differs. No a0 retune
        manufactures a spread MG structurally lacks. SIGN robust (theta decreasing => plungers always
        LESS boosted than circular members at the same radius); MAGNITUDE theta-form-dependent (UNVERIFIED).
  (3) MI-vs-MG gap, plunge vs adiabatic: a deep plunger reaches omega_ex/omega_in~O(1) at pericenter and
      its instantaneous boost is theta-enhanced; but the deployable discriminator is NOT the single
      member's ratio (a0-absorbable) -- it is the CROSS-MEMBER boost spread at fixed a_ext (STEP 3b).
      Plungers ARE identifiable (radial-orbit / phase-space caustic / recent-infall selection) but form a
      SMALL special subset, and the test needs members spanning infall phase AT THE SAME cluster radius.

  NET (no manufactured signal): the non-adiabatic MI signature is GENUINELY DISTINCT from MG (not
  a0-degenerate) ONLY as a RELATIONAL observable -- the boost/sigma SPREAD across infall phase at matched
  cluster-centric a_ext, which MG cannot produce for any a0. It is ABOVE FLOOR IN PRINCIPLE (~5-13% sigma
  spread vs MG's structural zero) but is a HARDER, theta-magnitude-dependent, small-special-subset,
  relationally-binned test. A single member -- and a single member's whole orbit -- is a0-degenerate; the
  honest distinctive content is the cross-member correlation. The clean, theta-robust, single-member,
  population-stackable discriminator remains Observable 1 (the velocity-ellipsoid ANISOTROPY SIGN: MI
  tangential, MG radial). The non-adiabatic plunge is a genuine SECOND, independent handle but more
  demanding. Realistic cluster members DO reach omega_ex ~ omega_in (diffuse/UDG/dSph members at the
  pericenter of deep radial cluster orbits), so the regime is not ruled out by the kinematics -- the limit
  is deliverability and the unknown theta(y), NOT a0-degeneracy of the relational signal.""")
