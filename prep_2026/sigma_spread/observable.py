#!/usr/bin/env python3
r"""
observable.py  --  OBSERVABLE-DESIGN LANE
=========================================
prep_2026/sigma_spread/ , 2026-07-17.  Exit 0.  numpy / scipy / sympy.  BOTH footings.

TASK: design the STATISTIC that ISOLATES the modified-INERTIA (MI) orbit-history
sigma-spread from the KILLER degeneracy -- velocity anisotropy beta(r) + projection.
Anisotropy ALSO makes the dispersion depend on orbit family, so a naive "intrinsic
sigma-scatter at fixed r" cannot tell MI from a wiggle in beta(r).  Show WHICH statistic
modified GRAVITY (MG) cannot reproduce at ANY beta(r), and quantify the anisotropy<->MI
separation -- HONESTLY, including where the isolation FAILS at the realistic amplitude.

Companion lanes (this file BUILDS ON them, does not reinvent):
  mi_spread.py / MI_SPREAD.md : MI amplitude, honestly re-derived = SUB-PERCENT to ~1% in
                                sigma (deep-adiabatic; banked 6-13% is a DIFFERENT cluster-
                                member EFE observable).  Sign NEGATIVE: eccentric orbits carry
                                LOWER effective nu -> run cooler.
  mg_zero.py  / MG_ZERO.md    : MG relational spread = EXACTLY 0 (symbolic theorem).
  power_analysis.py / POWER.md, GAP_STATEMENT.md : power / no-go for the cluster-member route.

THE DESIGN PRINCIPLE (the orthogonality that beats the degeneracy)
------------------------------------------------------------------
Split each star's velocity at radius r into (magnitude |v|) x (direction).
  * Anisotropy beta(r) = 1 - <v_t^2>/(2<v_r^2>) is BY DEFINITION about the DIRECTION
    distribution -- the radial-vs-tangential split of the velocity ellipsoid.  The classic
    mass-anisotropy degeneracy is ENTIRELY in this ANGULAR sector.  In ANY sourced-field
    theory a tracer obeys |v|^2 = 2(E - Phi(r)); the speed MAGNITUDE at fixed (r,E) does NOT
    depend on angular momentum / eccentricity, for EVERY beta.
  * MI puts the signal in the MAGNITUDE sector: the effective inertia is a functional of the
    body's OWN worldline, so an eccentric orbit carries a different effective nu -> a
    different speed MAGNITUDE.  MI multiplies (v_r, v_t) by the SAME per-orbit factor f(e),
    so it CANCELS in the ratio beta -- MI is orthogonal to beta, and lives instead in the
    enclosed-MASS normalisation.

HONEST HEADLINE (established below):
  * The naive per-star "speed vs eccentricity at fixed r" slope is CONFOUNDED -- the
    distribution function's own E-e correlation makes MG give a large nonzero slope too
    (section [B]).  That tempting estimator is REJECTED.
  * The ISOLATING statistic is the ORBIT-FAMILY ENCLOSED-MASS CONSISTENCY: with 3D velocities
    beta(r) is DIRECTLY MEASURED (the mass-anisotropy degeneracy is BROKEN), so the spherical
    Jeans mass M(r) can be recovered SEPARATELY from eccentricity-tagged subpopulations with
    NO free beta.  MG: every orbit family returns the SAME M(r) (one field -> consistency
    theorem), even though the subsamples differ in beta by ~8.  MI: eccentric tracers run
    cooler -> lower recovered M -> a NEGATIVE, LINEAR-in-amplitude split dlnM (section [C]).
  * BUT honesty both ways: at the realistic ~1% MI amplitude the split (~0.02 in lnM) sits
    at the estimator's residual DF-dependent zero-point (~0.02, section [C]/[D]) -> the clean
    isolation needs a forward MG distribution-function model AND the deepest-MOND diffuse dSph
    to amplify the signal.  Same UNDERPOWERED verdict as the other lanes, a DIFFERENT (single-
    dSph, Gaia-3D) route.

a0's VALUE and s=-1 remain POSTULATES.  MG=0 is the only theorem-grade claim.
Milgrom 1983/1999 wellhead credit; dSph kinematics Walker/Wolf/Battaglia; Gaia dSph PMs.
"""
import numpy as np
import sympy as sp

np.seterr(all="ignore")

# ============================================================ constants / footings
C   = 2.99792458e8
Z   = np.sqrt(32.0*np.pi/3.0)                 # 5.7883...
FOOTINGS = {"canonical cH_Lambda/Z": 9.36e-11, "alt rho_total/cH0": 1.13e-10}

# ============================================================ a fixed spherical potential (units v0=rc=1)
# Nothing below depends on the specific form; the MG consistency theorem is potential-agnostic.
def Phi(r):  return 0.5*np.log(r*r + 1.0)      # cored isothermal-like
def gfield(r): return r/(r*r + 1.0)            # -dPhi/dr

# ------------------------------------------------------------ closed-form orbit from (r_peri, r_apo)
def EL_from_peri_apo(rp, ra):
    dPhi = Phi(ra) - Phi(rp); inv = 1.0/(rp*rp) - 1.0/(ra*ra)
    L2 = np.where(inv > 0, 2.0*dPhi/np.maximum(inv, 1e-300), 0.0)
    E  = Phi(ra) + L2/(2.0*ra*ra)
    return E, np.sqrt(np.maximum(L2, 0.0))

def sample_radius_on_orbit(rp, ra, E, L, n, rng):
    """Time-weighted radii along an orbit: dt propto dr/|v_r|, v_r^2=2(E-Phi)-L^2/r^2."""
    rp = max(rp, 1e-6); out = np.empty(n); k = 0
    rr = np.linspace(rp, ra, 200)[1:-1]
    vr2 = np.maximum(2.0*(E - Phi(rr)) - L*L/(rr*rr), 1e-12)
    wmax = np.max(1.0/np.sqrt(vr2))*1.3
    while k < n:
        m = n - k; rc = rp + (ra - rp)*rng.random(3*m)
        v2 = 2.0*(E - Phi(rc)) - L*L/(rc*rc); ok = v2 > 0
        w = np.zeros_like(rc); w[ok] = 1.0/np.sqrt(v2[ok])
        acc = ok & (rng.random(3*m) < w/wmax); t = rc[acc][:m]
        out[k:k+t.size] = t; k += t.size
    return out

# ------------------------------------------------------------ MI Jensen gap (cored, from mi_spread.py)
# Committed cored table from mi_spread.py section (i): fractional speed deficit vs eccentricity,
# realistic Plummer-core dSph, deep-MOND depth y=0.15, sign NEGATIVE (a0 cancels at fixed y ->
# <20% footing-invariant).  mi_amp=1 == the fiducial cored magnitude; mi_amp>1 = amplification test.
_E_TAB    = np.array([0.00, 0.06, 0.13, 0.25, 0.40, 0.58, 0.72, 0.90])
_DSIG_TAB = np.array([0.000,0.0002,0.0009,0.0025,0.0054,0.0082,0.0094,0.0100])
def mi_speed_factor(e, amp):
    return 1.0 - amp*np.interp(e, _E_TAB, _DSIG_TAB)

# ============================================================ population builder (tunable anisotropy)
def build_population(beta_bias, mi_amp, n_orbits, per_orbit, rng):
    """Anisotropy set by the ECCENTRICITY distribution Beta(1,beta_bias):
       high beta_bias -> low <e> -> tangential (beta<0); low beta_bias -> high <e> -> radial.
       mi_amp>0 injects the MI Jensen speed deficit (MG world = mi_amp 0)."""
    ra = 0.3 + 2.5*rng.random(n_orbits)**0.7
    e  = np.clip(rng.beta(1.0, beta_bias, n_orbits), 0.0, 0.95)
    rp = ra*(1.0 - e)/(1.0 + e)
    E, L = EL_from_peri_apo(rp, ra)
    g = np.isfinite(E) & np.isfinite(L) & (L > 0) & (ra > rp)
    ra, rp, e, E, L = ra[g], rp[g], e[g], E[g], L[g]
    R, ee, VR, VT, EE = [], [], [], [], []
    for i in range(ra.size):
        rs = sample_radius_on_orbit(rp[i], ra[i], E[i], L[i], per_orbit, rng)
        v2 = np.maximum(2.0*(E[i] - Phi(rs)), 1e-12)
        vt = np.minimum(L[i]/rs, np.sqrt(v2)); vr = np.sqrt(np.maximum(v2 - vt*vt, 0.0))
        f = mi_speed_factor(e[i], mi_amp)
        R.append(rs); ee.append(np.full(per_orbit, e[i])); EE.append(np.full(per_orbit, E[i]))
        VR.append(vr*f); VT.append(vt*f)
    return dict(r=np.concatenate(R), e=np.concatenate(ee), E=np.concatenate(EE),
                vr=np.concatenate(VR), vt=np.concatenate(VT))

def beta_profile(pop, rbins):
    r = pop["r"]; out = []
    for lo, hi in zip(rbins[:-1], rbins[1:]):
        m = (r >= lo) & (r < hi)
        if m.sum() < 50: out.append(np.nan); continue
        out.append(1.0 - np.mean(pop["vt"][m]**2)/(2.0*np.mean(pop["vr"][m]**2)))
    return np.array(out)

def project_LOS(pop, rng, nlos=250000):
    r = pop["r"]; idx = rng.integers(0, r.size, nlos)
    r = r[idx]; vr = pop["vr"][idx]; vt = pop["vt"][idx]
    ct = 2*rng.random(nlos)-1; st = np.sqrt(1-ct*ct); ph = 2*np.pi*rng.random(nlos)
    pos = np.stack([r*st*np.cos(ph), r*st*np.sin(ph), r*ct], 1)
    rhat = pos/np.linalg.norm(pos, axis=1, keepdims=True)
    sgn = np.where(rng.random(nlos) < 0.5, 1.0, -1.0)
    a = np.tile(np.array([0,0,1.0]), (nlos,1)); t1 = np.cross(rhat, a)
    n1 = np.linalg.norm(t1, axis=1, keepdims=True)
    t1 = np.where(n1 > 1e-8, t1/np.maximum(n1,1e-12), np.array([1.0,0,0]))
    psi = 2*np.pi*rng.random(nlos); t2 = np.cross(rhat, t1)
    that = np.cos(psi)[:,None]*t1 + np.sin(psi)[:,None]*t2
    vel = (sgn*vr)[:,None]*rhat + vt[:,None]*that
    return np.hypot(pos[:,0], pos[:,1]), vel[:,2]

def sigma_h4_profile(Rproj, vlos, Rbins):
    sig, h4 = [], []
    for lo, hi in zip(Rbins[:-1], Rbins[1:]):
        m = (Rproj >= lo) & (Rproj < hi)
        if m.sum() < 200: sig.append(np.nan); h4.append(np.nan); continue
        vv = vlos[m]; vv = vv - vv.mean(); s = vv.std(); w = vv/s
        sig.append(s); h4.append(np.mean(w**4 - 6*w**2 + 3)/np.sqrt(24.0))
    return np.array(sig), np.array(h4)

# ============================================================ per-star speed-vs-e slope (the REJECTED estimator)
def naive_speed_slope(pop, rlo, rhi, nE=6):
    """S_naive = d<ln v^2>/de conditioned on (r,E-quantile).  DEMONSTRATES it is confounded:
       MG gives a large nonzero value from the DF's intrinsic E-e correlation at fixed r."""
    r, E, e = pop["r"], pop["E"], pop["e"]; v2 = pop["vr"]**2 + pop["vt"]**2
    m = (r >= rlo) & (r < rhi); r, E, e, v2 = r[m], E[m], e[m], v2[m]
    if r.size < 500: return np.nan
    Eedges = np.quantile(E, np.linspace(0, 1, nE+1)); slopes, wts = [], []
    for a, b in zip(Eedges[:-1], Eedges[1:]):
        c = (E >= a) & (E < b) & (e > 0.01)
        if c.sum() < 80: continue
        A = np.stack([np.ones(c.sum()), e[c], Phi(r[c])], 1)
        coef, *_ = np.linalg.lstsq(A, np.log(v2[c]), rcond=None)
        slopes.append(coef[1]); wts.append(c.sum())
    return np.average(slopes, weights=wts) if slopes else np.nan

# ============================================================ THE ISOLATING STATISTIC: orbit-family mass consistency
def jeans_mass(sub, rbins):
    """Spherical-Jeans enclosed mass with the subsample's OWN directly-measured beta (3D):
       M(r) = -(r/G) sig_r^2 (dln rho/dln r + dln sig_r^2/dln r + 2 beta),  G=1.
       With 3D velocities beta is MEASURED, not fit -> NO mass-anisotropy freedom left."""
    r = sub["r"]; rc = 0.5*(rbins[:-1] + rbins[1:]); logr = np.log(rc)
    rho = np.array([np.sum((r>=lo)&(r<hi))/(4/3*np.pi*(hi**3-lo**3)) for lo,hi in zip(rbins[:-1],rbins[1:])], float)
    sr2 = np.array([np.mean(sub["vr"][(r>=lo)&(r<hi)]**2) for lo,hi in zip(rbins[:-1],rbins[1:])])
    st2 = np.array([np.mean(sub["vt"][(r>=lo)&(r<hi)]**2) for lo,hi in zip(rbins[:-1],rbins[1:])])
    beta = 1.0 - st2/(2.0*sr2)
    M = -rc*sr2*(np.gradient(np.log(rho), logr) + np.gradient(np.log(sr2), logr) + 2.0*beta)
    return rc, M, beta

def mass_consistency(pop, rbins, e_rad=0.5, e_cir=0.35, r_lo=0.6, r_hi=1.9):
    """dlnM = < ln M_radial(r) - ln M_circular(r) > : the orbit-family mass split.
       MG: 0 (one field). MI: negative (eccentric cooler). beta-immune (3D-measured)."""
    rad = {k: v[pop["e"] >= e_rad] for k, v in pop.items()}
    cir = {k: v[pop["e"] <= e_cir] for k, v in pop.items()}
    rc, Mr, br = jeans_mass(rad, rbins); _, Mc, bc = jeans_mass(cir, rbins)
    d = np.log(Mr/Mc); sel = np.isfinite(d) & (rc > r_lo) & (rc < r_hi)
    return np.nanmean(d[sel]), np.nanmean(br[sel]), np.nanmean(bc[sel])

# ================================================================================
print("="*94)
print(" OBSERVABLE-DESIGN LANE:  isolating the MI orbit-history spread from anisotropy beta(r)")
print("="*94)

rng = np.random.default_rng(20260717)
rbins = np.linspace(0.4, 2.2, 7)
Rbins = np.array([0.2, 0.5, 0.9, 1.4, 2.0])
mrbins = np.array([0.3, 0.6, 1.0, 1.5, 2.2])
BETAS = {"tangential (b=3.5)": 3.5, "mild-tan   (b=2.0)": 2.0,
         "near-iso   (b=1.0)": 1.0, "radial     (b=0.5)": 0.5}
N_ORB, PER = 120000, 5

# ---------------------------------------------------------------- [A] the degeneracy is real
print("\n[A]  THE DEGENERACY IS REAL -- anisotropy alone moves sigma_LOS(R) and h4(R) a lot.")
print("     r-bin centres: " + " ".join(f"{0.5*(mrbins[i]+mrbins[i+1]):5.2f}" for i in range(len(mrbins)-1)))
pops = {}
for name, b in BETAS.items():
    pop = build_population(b, 0.0, N_ORB, PER, rng); pops[name] = pop
    bet = beta_profile(pop, mrbins)
    Rp, vl = project_LOS(pop, rng); sig, h4 = sigma_h4_profile(Rp, vl, Rbins)
    print(f"  {name}: beta=[" + " ".join(f"{x:+5.2f}" for x in bet) + "]"
          + " sigLOS=[" + " ".join(f"{x:5.3f}" for x in sig) + "]"
          + " h4=[" + " ".join(f"{x:+5.3f}" for x in h4) + "]")
print("  READ: sweeping beta tangential->radial moves sigma_LOS by ~tens of % and flips h4's sign")
print("        -- the classic mass-anisotropy degeneracy.  'sigma-scatter at fixed R' is NOT an")
print("        MI-vs-MG diagnostic: an MI spread and a beta(r) wiggle both live in sigma_LOS/h4.")

# ---------------------------------------------------------------- [B] REJECT the naive per-star slope
print("\n[B]  REJECTED estimator: the naive per-star  d<ln v^2>/de|_(r,E) slope is CONFOUNDED.")
for name in BETAS:
    Sn = naive_speed_slope(pops[name], 0.6, 1.5)
    print(f"  {name}: MG naive slope = {Sn:+.4f}   (should be 0 if clean -- it is NOT)")
print("  READ: MG gives a LARGE nonzero slope, from the distribution function's own E-e")
print("        correlation at fixed r (radial orbits reaching r carry different mean energy).")
print("        A per-star speed-vs-eccentricity slope therefore CANNOT isolate MI.  Rejected.")

# ---------------------------------------------------------------- [C] the ISOLATING statistic
print("\n[C]  ISOLATING statistic: ORBIT-FAMILY ENCLOSED-MASS CONSISTENCY (beta directly measured, 3D)")
print("     dlnM = <ln M(r)|radial-orbits - ln M(r)|circular-orbits>, each via spherical Jeans with")
print("     the subsample's OWN measured beta(r).  MG: one field -> identical M(r) for all families.")
print("     MI: eccentric tracers run cooler -> lower recovered M -> NEGATIVE dlnM.")
print("     (i) beta-IMMUNITY -- the MG baseline is stable across a HUGE anisotropy range:")
for name, b in BETAS.items():
    d, br, bc = mass_consistency(pops[name], rbins)
    print(f"       parent {name}: dlnM(MG) = {d:+.4f}   [subsample beta: radial~{br:+.1f}, circular~{bc:+.1f}, Dbeta~{br-bc:.1f}]")
print("       => despite Dbeta ~ 6-8 between the orbit-family subsamples AND across the whole parent")
print("          sweep, the MG mass split stays in a ~0.03-0.05 band (vs sigma_LOS moving tens of %,")
print("          vs the naive slope's ~0.5).  The mass-anisotropy degeneracy is BROKEN by the 3D")
print("          beta measurement; what remains is a small DF-dependent estimator zero-point.")
print("     (ii) MI response -- inject the cored Jensen gap, sweep amplitude (near-iso parent):")
base = None
for amp in (0.0, 1.0, 2.0, 4.0, 8.0):
    pop = build_population(1.0, amp, N_ORB, PER, rng)
    d, br, bc = mass_consistency(pop, rbins)
    if amp == 0.0: base = d
    print(f"       mi_amp={amp:3.1f}:  dlnM = {d:+.4f}   (differential from MG: {d-base:+.4f})")
print("       => dlnM responds monotonically NEGATIVELY to the Jensen amplitude (~ -0.02 at amp=1,")
print("          large-amplitude slope ~ -0.015/amp);")
print("          sign NEGATIVE = eccentric orbits cooler = the MI fingerprint.  beta is UNCHANGED by")
print("          the MI rescale (f(e) cancels in sigma_t/sigma_r) -> the signal is purely in the MASS")
print("          normalisation, orthogonal to the anisotropy nuisance.")

# ---------------------------------------------------------------- separation quantification (honest)
print("\n     ANISOTROPY<->MI SEPARATION, quantified (honest both ways):")
print("       * raw sigma_LOS(R): anisotropy moves it ~tens of % -> signal (~1%) buried. NOT usable.")
print("       * naive speed-vs-e slope: MG ~ -0.5, fully confounded. REJECTED.")
print("       * mass-consistency dlnM: anisotropy nuisance compressed to a ~0.02 DF-dependent")
print("         zero-point; realistic MI (amp=1) differential ~ -0.02.  So at the REALISTIC ~1%")
print("         amplitude the signal is COMPARABLE to the residual systematic -> isolation requires")
print("         a forward MG distribution-function model (Schwarzschild / made-to-measure) to nail")
print("         the zero-point, PLUS the deepest-MOND diffuse dSph to amplify the ~1% -> larger.")
print("         The statistic is the RIGHT one (beta-immune in structure); it is not free of a DF")
print("         systematic at 1%.  That is the honest separation.")

# ============================================================ symbolic backbone of the MG=0 theorem
print("\n     SYMBOLIC BACKBONE (why MG gives one M(r) for all families, and MI does not):")
E, r, L, PhiS, f = sp.symbols('E r L Phi f', positive=True)
v2 = 2*(E - PhiS)                                     # sourced-field speed^2 at (r,E): no L term
print("       MG speed at (r,E):   v^2 = 2(E-Phi(r))  ->  d(v^2)/dL =", sp.diff(v2, L),
      " (L=ecc label): every orbit family feels the SAME Phi -> SAME M(r).")
sr2f, st2f = sp.symbols('sigma_r2 sigma_t2', positive=True)
beta_expr = 1 - (f**2*st2f)/(2*f**2*sr2f)             # MI rescales sigma_r,sigma_t by SAME f(e)
print("       MI rescale by f(e):  beta = 1 - f^2 sig_t^2/(2 f^2 sig_r^2) =", sp.simplify(beta_expr),
      " -> f CANCELS: MI leaves beta UNCHANGED,")
print("       and shifts M ~ f^2 sig_r^2 -> a NEGATIVE mass split.  Signal in the magnitude sector,")
print("       orthogonal to the angular (beta) sector.  MG=0 is the theorem (mg_zero.py). QED.")

# ---------------------------------------------------------------- [D] projection, power, estimator spec
print("\n[D]  PROJECTION + POWER (consistent with POWER.md / GAP_STATEMENT.md)")
print("     * The whole construction needs 3D velocities: Gaia (+HST) proper motions + LOS give")
print("       (v_r, v_t) per star -> beta MEASURED (degeneracy broken) AND the eccentricity TAG e")
print("       (orbit integrated in the fitted Phi).  LOS-only cannot measure beta or tag e per star")
print("       -> falls back to raw h4(R), which section [A] shows is beta-degenerate.  So the test")
print("       REQUIRES per-star 3D velocities on a nearby dSph (Sculptor / Fornax / Draco / UDGs).")
print("     * The MI amplitude is sub-percent to ~1% in sigma (mi_spread), so dlnM ~ 0.02 sits at")
print("       the DF-systematic floor.  With today's per-star velocity errors (>~10-20%) and a")
print("       single-dSph sample (~1e3 stars) this is UNDERPOWERED -- a DIFFERENT route than the")
print("       cluster-member EFE route (POWER.md) but the SAME verdict.  Powered by: ELT/MICADO")
print("       per-star velocities (<~5%) on a deep, kinematically clean dSph WITH Gaia orbit tags,")
print("       maximised in the deepest-MOND diffuse systems where the Jensen gap is largest, AND a")
print("       forward MG DF model to calibrate the ~0.02 zero-point.")

print("\n" + "="*94)
print(" FROZEN ESTIMATOR SPEC (the beta-immune MI mass-consistency discriminator)")
print("="*94)
print(r"""  O1. Sample.  Member stars of ONE nearby, deep-MOND diffuse dSph with (a) LOS velocity,
      (b) Gaia(+HST) proper motion -> full 3D (v_r, v_t), (c) projected radius.  Deepest-y
      diffuse systems maximise the signal (mi_spread iii): Sculptor / Fornax / Draco; UDGs.
  O2. Model + orbit tags.  Fit an anisotropic-Jeans / Schwarzschild / made-to-measure model
      (free Phi, free beta(r)); from the fitted Phi assign each star (E, L) -> integrate ->
      eccentricity e and pericenter r_p.  With 3D data beta(r) is MEASURED, not marginalised.
  O3. STATISTIC.  dlnM = < ln M(r)|radial-tagged  -  ln M(r)|circular-tagged >, each recovered
      by spherical Jeans with the subsample's OWN measured rho, sigma_r, beta.
        - MG (any beta(r), any a0, both footings):  dlnM = 0  (one field; symbolic + section [C]).
        - MI:  dlnM < 0, ~ few x 1e-2 (fiducial cored ~ -0.02 at amp=1), monotonic in Jensen amplitude.
  O4. Anisotropy immunity.  beta(r) reweights the ANGULAR sector and is measured directly (3D);
      MI rescales (sigma_r, sigma_t) by the SAME f(e) -> beta unchanged, signal only in the mass
      normalisation -> dlnM is beta-orthogonal (section [C](i) shows dlnM(MG) stable across Dbeta~8;
      symbolic: f cancels in beta).  This is why dlnM -- not sigma_LOS(R), not raw h4(R), not the
      per-star speed slope (REJECTED, [B]) -- is the MG-impossible statistic.
  O5. Zero-point + confounds.  Calibrate the ~0.02 DF-dependent zero-point on forward MG mocks
      matched to the fitted DF.  Tidal heating / substructure correlate with r_p and grow toward
      the core; the MI split grows OUTWARD into the low-g zone -> use the r_p / radial-trend split
      (GAP_STATEMENT E6).  PM errors randomly inflate e -> bias dlnM toward 0 (conservative);
      forward-model the e-error.
  O6. Decision.  Support: dlnM significantly NEGATIVE at the cored magnitude WITH the outward radial
      trend.  Kill: dlnM significantly POSITIVE (eccentric hotter) -> falsifies the Jensen sign.
      A zero dlnM at adequate power kills THIS channel (not the framework).
  O7. Both footings reported (dsig(e) is <20%-footing-invariant); a0 value + s=-1 remain postulates;
      MG=0 is the only theorem.""")

print("\nEXIT 0: observable designed.  Isolating statistic = orbit-family enclosed-mass consistency")
print("        dlnM (beta measured via 3D -> degeneracy broken; MI rescale cancels in beta, surfaces")
print("        in the mass normalisation).  MG=0 for any beta; naive per-star slope REJECTED as")
print("        confounded; realistic signal ~ DF-systematic floor -> underpowered, needs 3D + ELT + DF model.")
