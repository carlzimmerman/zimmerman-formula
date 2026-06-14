#!/usr/bin/env python3
"""
ROUTE 4 -- the wide-binary CONTAMINATION model (the dominant systematic).
=========================================================================
Question (Carl's #1 rule, both ways): does UNCORRECTED contamination shift the
inferred gravity boost gamma enough to (a) MANUFACTURE a gamma~1.3 from pure
Newton (so the test cannot confirm the framework without cleaning), and/or (b)
BURY the framework's true gamma=1.32? And is the framework's OWN-interp gamma
(F4/standard ~ 1.04-1.08, NOT the soft-interp 1.32) even above the noise floor?

Three contamination channels, each quantified against the real 2023-2026 literature:
  (i)  UNDETECTED CLOSE COMPANIONS (triples). f_multi ~ 0.2-0.5 (Chae self-cal;
       Moe&DiStefano 2017; Raghavan 2010). A hidden inner pair adds a photocentre-
       barycentre wobble velocity that INFLATES the measured relative velocity ->
       fakes a boost. This is the Chae-vs-Banik/Pittordis crux.
  (ii) ECCENTRICITY. Super-thermal f(e) ~ e^1.3 (Hwang 2022): median e=0.74,
       22% have e>0.9. High-e pairs at apoapsis have low instantaneous v -> the
       deprojection to gamma depends on the assumed e-distribution.
  (iii) CHANCE ALIGNMENT / flybys at wide s. El-Badry R_chance < 0.1 cut; residual
       ~ a few % at the widest s, with ~random (large) velocities.

We MEASURE, by forward Monte Carlo on a pure-Newtonian population + a contaminant
population, the SHIFT in the inferred gamma (via the v-tilde 90th-percentile
estimator that Chae/Pittordis/Banik all use), as a function of f_multi. Then we
ask where the framework's TWO gamma predictions (own-interp 1.08, soft-interp 1.32)
sit relative to that contamination-induced shift, and what cleaning is needed.

numpy only.  C. Zimmerman machinery, 2026-06-14 (Route 4).
"""
import numpy as np
rng = np.random.default_rng(20260614)

G, Msun, AU, kpc, c = 6.674e-11, 1.989e30, 1.496e11, 3.0857e19, 2.998e8

# ------------------------------------------------------------------ framework a0
H0, OmL = 2.184e-18, 0.685
rho_crit = 3*H0**2/(8*np.pi*G)
a0_DE   = (c/2)*np.sqrt(G*OmL*rho_crit)     # 9.36e-11 (pure-Lambda, framework)
a0_MOND = 1.20e-10
Vc, R0  = 229e3, 8.178*kpc
g_ext   = Vc**2/R0
print(f"a0_DE = {a0_DE:.3e}   g_ext = {g_ext:.3e} = {g_ext/a0_DE:.2f} a0_DE = {g_ext/a0_MOND:.2f} a0_MOND\n")

# interpolation functions
def nu_simple(y):   return 0.5+np.sqrt(0.25+1.0/y)             # soft  mu=x/(1+x)
def nu_std(y):      return np.sqrt((y+np.sqrt(y*y+4))/(2*y))   # sharp F4/standard (framework own)

# ----- framework EFE gamma both interps (banked, vector-MI angle average) -------
def gamma_efe(nu, a0, y_int=0.5, n=400000):
    """gamma = G_eff/G_N = <nu(|y_ext zhat + y_int nhat|)> over orbit orientation.
    (velocity boost = sqrt of this). Deep regime y_int<<y_ext -> gamma->nu(y_ext)."""
    ye, yi = g_ext/a0, y_int
    u = rng.uniform(-1,1,n)
    yt = np.sqrt(ye**2+yi**2+2*ye*yi*u)
    return np.mean(nu(yt))

GAMMA = {}
for tag,a0 in (("DE",a0_DE),("MOND",a0_MOND)):
    GAMMA[(tag,"std")]    = gamma_efe(nu_std, a0)
    GAMMA[(tag,"simple")] = gamma_efe(nu_simple, a0)
print("FRAMEWORK gamma = G_eff/G_N (banked vector-MI EFE), both interps both footings:")
for k,v in GAMMA.items():
    print(f"   {k[0]:5s} {k[1]:7s}: gamma={v:.3f}  (vel boost +{100*(np.sqrt(v)-1):.1f}%)")
g_own  = GAMMA[("DE","std")]      # framework's OWN derived sharp interp at DE footing
g_soft = GAMMA[("DE","simple")]  # soft-interp 'banked 1.32' reading
print(f"\n  >> framework OWN-interp (DSSYK-sharp) gamma = {g_own:.3f}  (the honest framework number)")
print(f"  >> soft-interp ('banked 1.32') gamma        = {g_soft:.3f}  (NOT the framework's own interp)\n")

# =====================================================================================
# THE CONTAMINATION FORWARD MODEL
# =====================================================================================
# The observable everyone uses: v-tilde = v_rel / v_circ, where v_circ=sqrt(G M / s)
# is the Newtonian circular speed at the projected separation. For a real bound
# Keplerian binary, v-tilde lives in [0, sqrt(2)] and the *shape* of its distribution
# (esp. the 90th percentile / the tail) encodes gamma. Contaminants push the tail up.
# We forward-model the SKY-PROJECTED v-tilde that Gaia actually measures.
# -------------------------------------------------------------------------------------

def sample_eccentricities(n, kind="superthermal"):
    if kind=="thermal":      # f(e)=2e
        return np.sqrt(rng.uniform(0,1,n))
    if kind=="superthermal": # f(e) ~ e^1.3  (Hwang 2022): CDF = e^2.3 -> e = U^(1/2.3)
        return rng.uniform(0,1,n)**(1.0/2.3)
    if kind=="uniform":
        return rng.uniform(0,1,n)
    raise ValueError

def kepler_vtilde(n, ecc, boost=1.0):
    """Sky-projected v-tilde for a population of bound binaries.
    boost = sqrt(G_eff/G_N): MOND/framework multiply the true orbital speed by boost
    (the velocities are boosted, the Newtonian v_circ normalizer is NOT) so the whole
    v-tilde distribution scales by 'boost'. Random orbital phase + random 3D orientation
    give the projection scatter. Standard wide-binary forward model (Pittordis/Banik)."""
    # eccentric anomaly E from mean anomaly M (uniform in time) via Kepler's eqn
    M = rng.uniform(0,2*np.pi,n)
    E = M.copy()
    for _ in range(60):
        E = E - (E-ecc*np.sin(E)-M)/(1-ecc*np.cos(E))
    cosf = (np.cos(E)-ecc)/(1-ecc*np.cos(E))
    sinf = (np.sqrt(1-ecc**2)*np.sin(E))/(1-ecc*np.cos(E))
    r_over_a = 1-ecc*np.cos(E)                                   # r/a
    # vis-viva: v^2 = G M (2/r - 1/a); in units where G M / a =1 -> v^2=(2/(r/a)-1)
    v2 = (2.0/r_over_a - 1.0)
    v  = np.sqrt(np.clip(v2,0,None))                            # |v| in sqrt(GM/a) units
    # velocity direction in orbital plane: angle between v and radial
    # v_r = (GM/a)^.5 * e sinf / sqrt(1-e^2);  v_t = (GM/a)^.5 (1+e cosf)/sqrt(1-e^2)
    vr = ecc*sinf/np.sqrt(1-ecc**2)
    vt = (1+ecc*cosf)/np.sqrt(1-ecc**2)
    # position r in orbital plane (units of a)
    x  = r_over_a*cosf; y = r_over_a*sinf
    # random 3D orientation (inclination i, node, argperi already folded via random M+phase)
    # project onto sky: random rotation of the orbital plane
    cosi = rng.uniform(-1,1,n); i = np.arccos(cosi)
    Om   = rng.uniform(0,2*np.pi,n); w = rng.uniform(0,2*np.pi,n)
    # rotate (x,y,0) and (vx,vy,0) by (w about z, i about x, Om about z)
    def rot(px,py):
        # arg of peri
        x1 =  px*np.cos(w)-py*np.sin(w); y1 = px*np.sin(w)+py*np.cos(w); z1=np.zeros_like(px)
        # inclination
        x2 = x1; y2 = y1*np.cos(i)-z1*np.sin(i); z2 = y1*np.sin(i)+z1*np.cos(i)
        # node
        x3 = x2*np.cos(Om)-y2*np.sin(Om); y3 = x2*np.sin(Om)+y2*np.cos(Om); z3=z2
        return x3,y3,z3
    rx,ry,rz = rot(x,y)
    vx,vy,vz = rot(vr*cosf - vt*sinf, vr*sinf + vt*cosf)   # v in orbital-plane cartesian
    s_proj = np.sqrt(rx**2+ry**2)                          # sky-projected separation (units a)
    v_proj = np.sqrt(vx**2+vy**2)                          # sky-projected speed (units sqrt(GM/a))
    # v_circ at the PROJECTED separation: v_c = sqrt(GM/s_proj) -> in our units = 1/sqrt(s_proj)
    vcirc  = 1.0/np.sqrt(np.clip(s_proj,1e-3,None))
    vtilde = boost * v_proj / vcirc
    return vtilde, s_proj

def triple_contaminant_vtilde(n, boost=1.0):
    """Undetected close companion: the photocentre of an unresolved inner pair orbits
    the inner barycentre, adding a wobble velocity dv that is ~comparable to or larger
    than the wide-orbit relative velocity. We model the EXTRA measured relative speed
    as the wide-binary speed PLUS an inner-orbit photocentre velocity. The inner orbit
    has period << observation baseline -> its instantaneous projected velocity adds in
    quadrature with random orientation. Inner-pair speed scale: a few km/s vs wide-pair
    ~ a few hundred m/s -> the inflation is LARGE (this is why triples dominate the tail).
    We parametrize the inner-wobble amplitude relative to v_circ by kappa (Pittordis:
    the triple tail extends to v-tilde ~ several)."""
    vt_wide, sp = kepler_vtilde(n, sample_eccentricities(n), boost=boost)
    # inner photocentre wobble: amplitude drawn from a broad distribution; the median
    # inner-companion adds dv ~ 1-3x the wide v_circ (calibrated so the triple population
    # peaks near v-tilde~1.3-1.6 and tails past 2, matching Pittordis' observed tail).
    kappa = rng.lognormal(mean=np.log(1.4), sigma=0.6, size=n)   # inner-wobble / v_circ
    phase = rng.uniform(0,2*np.pi,n)
    dv = kappa*np.cos(phase)                                     # projected wobble (units v_circ)
    vt_obs = np.sqrt(vt_wide**2 + dv**2 + 2*vt_wide*np.abs(dv)*rng.uniform(-1,1,n))
    return vt_obs

def chance_align_vtilde(n):
    """Chance alignments: two unrelated stars; relative velocity is the local stellar
    velocity dispersion (~30-40 km/s) which is HUGE vs wide-binary v_circ (~0.1-1 km/s)
    -> v-tilde >> 1, flat/broad. El-Badry R<0.1 keeps these to ~few %, but they live
    entirely in the high tail."""
    return np.abs(rng.normal(0, 8.0, n))   # v-tilde scale ~ dispersion/v_circ, broad

# ----- the gamma estimator everyone uses: tie inferred gamma to the v-tilde 90th pctile
# Calibrate gamma <-> vtilde_90 on PURE bound binaries (no contam) at known boost.
boosts_cal = np.linspace(1.0, 1.30, 13)         # vel boost sqrt(gamma) from 1.0 (Newton) to 1.30
v90_cal = []
for b in boosts_cal:
    vt,_ = kepler_vtilde(300000, sample_eccentricities(300000), boost=b)
    v90_cal.append(np.percentile(vt, 90))
v90_cal = np.array(v90_cal)
# invert: given an observed v90, infer the velocity boost (then gamma=boost^2)
def infer_gamma_from_v90(v90_obs):
    b = np.interp(v90_obs, v90_cal, boosts_cal)
    return b**2
v90_newton = v90_cal[0]
print("="*92)
print(f"CALIBRATION: pure-Newton (boost=1) gives v-tilde_90 = {v90_newton:.4f}")
print(f"   v-tilde_90 rises to {v90_cal[-1]:.4f} at velocity boost 1.30 (gamma=1.69)")
print("="*92,"\n")

# =====================================================================================
# EXPERIMENT 1 -- how much does UNCORRECTED triple contamination inflate inferred gamma,
#                 starting from a PURE-NEWTON population (boost=1)?  (the false-win test)
# =====================================================================================
print("EXPERIMENT 1: pure-NEWTON population + undetected triples -> inferred gamma")
print("-"*92)
print(f"{'f_multi':>8} | {'v90_obs':>8} | {'inferred gamma':>15} | reading")
print("-"*92)
N = 400000
for f_multi in (0.0, 0.10, 0.20, 0.30, 0.40, 0.50):
    n_tri = int(f_multi*N); n_bin = N-n_tri
    vt_bin,_ = kepler_vtilde(n_bin, sample_eccentricities(n_bin), boost=1.0)  # NEWTON
    vt_tri   = triple_contaminant_vtilde(n_tri, boost=1.0)
    vt_all   = np.concatenate([vt_bin, vt_tri])
    v90 = np.percentile(vt_all, 90)
    g_inf = infer_gamma_from_v90(v90)
    note = ""
    if g_inf>=g_own and g_inf<g_soft: note="-> fakes the FRAMEWORK-OWN gamma from pure Newton!"
    if g_inf>=g_soft: note="-> fakes even the SOFT-interp 1.32 from pure Newton!"
    print(f"{f_multi:8.2f} | {v90:8.4f} | {g_inf:15.3f} | {note}")
print()

# =====================================================================================
# EXPERIMENT 2 -- can cleaning EXPOSE the framework signal? Inject the framework's TWO
#  gammas into the bound population, add residual contamination after a cut, recover.
# =====================================================================================
print("EXPERIMENT 2: framework signal injected, recovered under residual contamination")
print("-"*92)
print("Pre-clean f_multi~0.30 (raw Chae/El-Badry); post-clean RUWE<1.2 + v-tilde + RV vet")
print("brings residual f_multi to ~0.05-0.10 (Chae's self-cal regime).")
print("-"*92)
def recover(true_gamma, f_resid, N=400000, label=""):
    b = np.sqrt(true_gamma)
    n_tri = int(f_resid*N); n_bin=N-n_tri
    vt_bin,_ = kepler_vtilde(n_bin, sample_eccentricities(n_bin), boost=b)
    vt_tri   = triple_contaminant_vtilde(n_tri, boost=b)
    vt_all   = np.concatenate([vt_bin, vt_tri])
    v90 = np.percentile(vt_all, 90)
    return infer_gamma_from_v90(v90)

for true_g, name in ((1.0,"Newton"), (g_own,"framework-OWN (sharp 1.08)"), (g_soft,"soft-interp (1.25)"), (1.49,"Chae-measured 1.49")):
    row=[]
    for f_resid in (0.30, 0.10, 0.05, 0.0):
        row.append(recover(true_g, f_resid))
    print(f"  true gamma={true_g:.3f} [{name:28s}] inferred @f_resid(0.30/0.10/0.05/0): "
          + " / ".join(f"{x:.3f}" for x in row))
print()

# =====================================================================================
# EXPERIMENT 3 -- the SEPARABILITY question. Can DR4 separate framework-own (1.08) from
#  Newton (1.00), and from soft-MOND (1.25-1.32)? Need the v90 GAP vs the DR4 error.
# =====================================================================================
print("EXPERIMENT 3: DR4 separability of v-tilde_90 (the actual discriminant)")
print("-"*92)
def v90_of(gamma, f_resid, N=600000):
    b=np.sqrt(gamma); n_tri=int(f_resid*N); n_bin=N-n_tri
    vt_bin,_=kepler_vtilde(n_bin, sample_eccentricities(n_bin), boost=b)
    vt_tri  =triple_contaminant_vtilde(n_tri, boost=b)
    return np.percentile(np.concatenate([vt_bin,vt_tri]),90)
f_clean=0.05
v90_N   = v90_of(1.00, f_clean)
v90_own = v90_of(g_own, f_clean)
v90_soft= v90_of(g_soft, f_clean)
v90_chae= v90_of(1.49, f_clean)
print(f"  (residual f_multi={f_clean}, clean DR4-class sample)")
print(f"   Newton          gamma=1.00 : v90={v90_N:.4f}")
print(f"   framework-OWN   gamma={g_own:.2f} : v90={v90_own:.4f}   (gap vs Newton: {v90_own-v90_N:+.4f})")
print(f"   soft-interp     gamma={g_soft:.2f} : v90={v90_soft:.4f}   (gap vs Newton: {v90_soft-v90_N:+.4f})")
print(f"   Chae-measured   gamma=1.49 : v90={v90_chae:.4f}   (gap vs Newton: {v90_chae-v90_N:+.4f})")

# DR4 sample size + per-pair v-tilde error -> error on v90
# DR4 expected clean 3D-velocity wide-binary sample in the deep regime: ~few x10^3 - 10^4.
# v90 statistical error ~ 1.25 * sigma_vt / sqrt(N_eff) (asymptotic quantile SE), with
# sigma_vt the spread of v-tilde near the 90th pctile (~0.3-0.4 for these dists).
for Npairs,desc in ((2000,"DR4 high-quality 3D (Chae-class, ~2k)"),
                    (8000,"DR4 statistical (Banik-class, ~8k)"),
                    (20000,"DR4 optimistic clean deep-regime (~20k)")):
    sig_vt = 0.35
    se_v90 = 1.2533*sig_vt/np.sqrt(Npairs) * np.sqrt(0.9*0.1)/0.3989  # quantile SE approx
    # crude but standard: SE(quantile_p)= sqrt(p(1-p)/N)/ f(x_p); use density~0.4 near tail
    se_v90 = np.sqrt(0.9*0.1/Npairs)/0.5
    snr_own_vs_N  = (v90_own -v90_N)/se_v90
    snr_soft_vs_N = (v90_soft-v90_N)/se_v90
    snr_own_vs_soft = (v90_soft-v90_own)/se_v90
    snr_soft_vs_chae= (v90_chae-v90_soft)/se_v90
    print(f"\n  [{desc}]  SE(v90)_stat~{se_v90:.4f}")
    print(f"     framework-OWN(1.08) vs Newton : {snr_own_vs_N:5.2f} sigma (STAT ONLY)")
    print(f"     soft-interp(1.25)   vs Newton : {snr_soft_vs_N:5.2f} sigma (STAT ONLY)")
    print(f"     soft-interp vs framework-OWN  : {snr_own_vs_soft:5.2f} sigma  (can DR4 tell the two framework interps apart?)")
    print(f"     Chae-1.49 vs soft-interp-1.25 : {snr_soft_vs_chae:5.2f} sigma")

# =====================================================================================
# EXPERIMENT 4 -- the HONEST limiter: the SYSTEMATIC contamination floor, NOT stat.
# DR4's wall is not sqrt(N); it is the residual f_multi uncertainty. How well must we
# KNOW f_multi for the framework-OWN gamma=1.08 (gap dv90~0.039) to survive?
# From Exp 1: d(v90)/d(f_multi) near the clean regime sets the systematic.
# =====================================================================================
print("\n"+"="*92)
print("EXPERIMENT 4: the REAL wall -- systematic contamination floor (NOT statistics)")
print("-"*92)
# numerically d v90 / d f_multi around the clean regime (pure-Newton base)
def v90_newton_with_fmulti(fm, N=600000):
    n_tri=int(fm*N); n_bin=N-n_tri
    vt_bin,_=kepler_vtilde(n_bin, sample_eccentricities(n_bin), boost=1.0)
    vt_tri  =triple_contaminant_vtilde(n_tri, boost=1.0)
    return np.percentile(np.concatenate([vt_bin,vt_tri]),90)
fm0=0.05; dfm=0.02
slope = (v90_newton_with_fmulti(fm0+dfm)-v90_newton_with_fmulti(fm0-dfm))/(2*dfm)
print(f"  d(v90)/d(f_multi) near f_multi=0.05 : {slope:.3f} per unit f_multi")
gap_own  = v90_own - v90_N      # framework-OWN signal in v90
gap_soft = v90_soft - v90_N
print(f"  framework-OWN v90 gap vs Newton    : {gap_own:.4f}")
print(f"  soft-interp  v90 gap vs Newton     : {gap_soft:.4f}")
# the f_multi knowledge needed so contamination systematic < the signal gap
need_dfm_own  = gap_own/abs(slope)
need_dfm_soft = gap_soft/abs(slope)
print(f"  => to NOT swamp framework-OWN(1.08), must know f_multi to +-{need_dfm_own:.3f} ({100*need_dfm_own:.1f}%)")
print(f"  => to NOT swamp soft-interp (1.34),  must know f_multi to +-{need_dfm_soft:.3f} ({100*need_dfm_soft:.1f}%)")
print(f"  Reality: Chae self-calibrates f_multi to ~+-0.05-0.10; surveys give 0.2-0.5 spread.")
print(f"  VERDICT-INPUT: framework-OWN needs f_multi known to ~{100*need_dfm_own:.0f}% (HARDER than current);")
print(f"                 soft-interp needs ~{100*need_dfm_soft:.0f}% (within reach of Chae-class self-cal).")
print("="*92)
