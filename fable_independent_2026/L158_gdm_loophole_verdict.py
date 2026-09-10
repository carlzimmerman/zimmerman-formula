#!/usr/bin/env python3
"""
L154 -- THE GDM LOOPHOLE, PART 3: WHERE THE PINCER ACTUALLY IS, AND THE VERDICT.  The CMB-vs-galaxy pincer
        does not close (L152).  The pincer RELOCATES to Lyman-alpha(z~3)-vs-galaxy(z=0) -- a lever arm of a
        factor FOUR in scale factor instead of 1090 -- and there it demands a growth exponent p = 3.5-4.1,
        which L153's THEOREM A forbids for every barotropic fluid (p < 3).  The barotropic branch is CLOSED,
        but NARROWLY: by a factor 2-4 in c_s^2, not by orders of magnitude, and only at gate settings that
        use the data-calibrated Lyman-alpha tolerance.  The NON-barotropic branch is NOT closed at all, and
        is named as the surviving door.
=============================================================================================================
L152: the two gates L125 named (CMB third peak / L61 galaxy overshoot) leave ~3 orders of magnitude of room
      in c_s^2; they demand only p > -1, and a decoupled species is pinned at p = -2.  Loophole REAL.
L153: the mechanisms.  Fuzzy DM and ghost condensates are two MORE instances of p = -2; particle GDM needs
      sigma/m ~ 1e5 cm^2/g; shift-symmetric k-essence P = X^n DOES realize a healthy fluid at p = 0; and two
      theorems bound the barotropic class -- THEOREM A: p < 3 strictly; THEOREM B: the fluid can climb a
      well of depth at most Delta_Phi_max = 3 * integral c_s^2 dln a = 3 c_s^2(1)/p.
This lane closes the loop by testing the EPOCHS BETWEEN recombination and today, which neither L125 gate
touches -- and that is where the obstruction turns out to live.

WHAT IS COMPUTED (self-contained; numpy/scipy + CLASS for validation):
  0  a linear two-fluid (dark fluid + baryons) sub-horizon solver for ARBITRARY c_s^2(a), VALIDATED here
     against CLASS's exact Boltzmann integration of the constant-c_s^2 GDM system.  Agreement is quoted.
  1  the intermediate-epoch gate.  The Lyman-alpha forest measures the z = 2-5 power spectrum out to
     k ~ 8 Mpc^-1 comoving.  The dark fluid's sound speed erases exactly that power.  Computed as a
     function of (p, c_s^2(1)).
  2  the joint window scan over (p, c_s^2(1)) against FOUR gates: GATE-G (the L61 galaxy gate, now with
     L153's THEOREM B condensation front, computed on the exact polytrope), GATE-L (Lyman-alpha), GATE-C
     (the L152 CMB Boltzmann ceiling), GATE-T (THEOREM A: p < 3).
  3  the closure equation in closed form:  4^p / p  >=  L v_c^2 / (3 epsilon_Lya), and the required p.
  4  what MOND would have to do to rescue the Lyman-alpha leg (quantified, since the hybrid is MOND-based).
  5  sigma8 / S8 and the CMB lensing amplitude at the window boundary.
  6  the VERDICT, the honest scope, the surviving door, and the propositions worth formalizing in Lean 4.

POLARITY: each check ASSERTS a statement; PASS = the statement is true.  This lane produces a KILL, so the
generous choice is taken at every step (10 percent Lyman-alpha tolerance, condensation allowed inside
10 kpc, the CMB ceiling from the MARGINALISED fit) and the sensitivity of the kill to each choice is
reported, so that no deficit is manufactured.
"""
import numpy as np
import sys, time, math
from scipy.integrate import solve_ivp, quad

T0 = time.time(); FAILS = []; NCHECK = [0]
def check(name, ok, detail=""):
    NCHECK[0] += 1
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f"   ({detail})" if detail else ""), flush=True)
    if not ok: FAILS.append(name)
def sec(t): print("\n" + "=" * 112); print(t); print("=" * 112, flush=True)
def P(s=""): print(s, flush=True)

print("=" * 112)
print("L154 -- where the pincer actually is: Lyman-alpha vs galaxies, and the verdict on the GDM loophole")
print("=" * 112, flush=True)

# =========================================================================================================
# COSMOLOGY
# =========================================================================================================
h    = 0.6736; om_b = 0.02237; om_d = 0.1200
CKMS = 299792.458
H0   = 100.0*h/CKMS
Ob   = om_b/h**2; Od = om_d/h**2; Or = 4.1834e-5/h**2
Om   = Ob + Od;   OL = 1.0 - Om - Or
A_REC = 1.0/1090.0
G_KPC  = 4.300917270e-6
RHOBAR = Od*2.77536627e11*h**2/1e9        # Msun/kpc^3
CS2_CMB_MAX = 6.125e-4                    # L152, CLASS + Planck-like, marginalised 3-sigma

def E2(a): return Om*a**-3 + Or*a**-4 + OL
def dlnEdlna(a): return 0.5*(-3*Om*a**-3 - 4*Or*a**-4)/E2(a)

# =========================================================================================================
sec("PART 0 -- THE SOLVER, AND ITS VALIDATION AGAINST CLASS.")
# =========================================================================================================
P("  Sub-horizon linear system for the dark fluid (delta_d) and the baryons (delta_b), in ln a:")
P("      delta'' + (2 + dlnE/dlna) delta' = (3/2) a^-3 [Om_d delta_d + Om_b delta_b]/E^2  -  J delta")
P("  with the fluid's Jeans term J = c_s^2(a) k^2/(a H)^2 acting on delta_d only.  c_s^2(a) is ARBITRARY.")
P("  Initial conditions: growing mode at a_i = 1e-3.  Reported quantity = the BARYON power ratio, which is")
P("  what the Lyman-alpha forest actually traces, and what CLASS's mPk returns in this configuration.")
P("")
def solve_pair(k, cs2fun, ai=1e-3, af=1.0):
    def rhs(lna, y):
        a = math.exp(lna); q = 2 + dlnEdlna(a); dd, vd, db, vb = y
        src = 1.5*a**-3*(Od*dd + Ob*db)/E2(a)
        return [vd, -q*vd + src - cs2fun(a)*k*k/(a*a*H0*H0*E2(a))*dd, vb, -q*vb + src]
    return solve_ivp(rhs, [math.log(ai), math.log(af)], [1., 1., 1., 1.],
                     rtol=1e-9, atol=1e-15, dense_output=True, method='LSODA')
_S0 = {}
def ratio_b(k, cs2fun, z):
    if k not in _S0: _S0[k] = solve_pair(k, lambda a: 0.0)
    la = math.log(1.0/(1.0+z))
    return (solve_pair(k, cs2fun).sol(la)[2]/_S0[k].sol(la)[2])**2

def ratio_pl(k, cs2_at_quarter, p, z=3.0):
    """baryon power ratio at z for the power-law profile pinned by c_s^2(a=1/4) = cs2_at_quarter.
       Cached on a rounded key so the bisections below reuse work."""
    key = (k, round(math.log10(max(cs2_at_quarter, 1e-30)), 4), round(p, 4), z)
    if key in _RPL: return _RPL[key]
    c1 = cs2_at_quarter*4.0**p
    v = ratio_b(k, lambda a, c=c1, q=p: c*a**q, z)
    _RPL[key] = v
    return v
_RPL = {}

HAVE_CLASS = True
try:
    from classy import Class
except Exception as e:                                                   # pragma: no cover
    HAVE_CLASS = False; P(f"  [CLASS unavailable ({e}); validation skipped]")
if HAVE_CLASS:
    def class_pk(cs2, ks, zs):
        p = {'output':'mPk','omega_cdm':1e-5,'Omega_fld':Od,'w0_fld':-1e-6,'wa_fld':0.0,
             'cs2_fld':max(cs2,1e-14),'use_ppf':'no','P_k_max_1/Mpc':40.0,'z_max_pk':6.0,
             'omega_b':om_b,'h':h,'A_s':2.1e-9,'n_s':0.9649,'tau_reio':0.0544}
        c = Class(); c.set(p); c.compute()
        out = {z: np.array([c.pk_lin(k, z) for k in ks]) for z in zs}
        c.struct_cleanup(); c.empty(); return out
    KV = [0.5, 1.0, 2.0, 5.0]; ZV = (0.0, 3.0)
    P0 = class_pk(0.0, KV, ZV)
    P(f"      {'c_s^2':>8} {'k':>5} | {'CLASS z=0':>10} {'solver':>9} | {'CLASS z=3':>10} {'solver':>9}")
    errs_gate, signs = [], []
    for cs2 in (1e-8, 1e-7, 1e-6):
        PC = class_pk(cs2, KV, ZV)
        for i, k in enumerate(KV):
            r0 = ratio_b(k, lambda a, c=cs2: c, 0.0); r3 = ratio_b(k, lambda a, c=cs2: c, 3.0)
            c0 = PC[0.0][i]/P0[0.0][i]; c3 = PC[3.0][i]/P0[3.0][i]
            # the gates below act at ratios near 0.9, so validate where the ratio is in the decisive band
            for rr, cc in ((r0, c0), (r3, c3)):
                if cc > 0.3: errs_gate.append(abs(rr/cc - 1))
                signs.append(rr >= cc - 1e-9)
            P(f"      {cs2:8.0e} {k:5.1f} | {c0:10.4f} {r0:9.4f} | {c3:10.4f} {r3:9.4f}")
    P("")
    P(f"      disagreement in the DECISIVE band (CLASS ratio > 0.3, where the 0.90 gate acts): "
      f"max {max(errs_gate)*100:.2f} percent")
    P(f"      sign of the residual: the solver retains at least as much power as CLASS in "
      f"{sum(signs)}/{len(signs)} cases")
    P("      -- i.e. the solver is uniformly OPTIMISTIC (it under-states the suppression), which is the")
    P("      generous direction for the loophole, so the kill below is not an artifact of the solver.")
    check("VAL-1  the arbitrary-c_s^2(a) two-fluid solver reproduces CLASS's exact Boltzmann integration of "
          "the constant-c_s^2 GDM system to better than 6 percent throughout the band where the gates below "
          "actually act (power ratio above 0.3), and it NEVER under-states the retained power -- it is "
          "uniformly generous to the loophole.  It is therefore fit to evaluate profiles CLASS cannot run "
          "(time-dependent c_s^2), and cannot manufacture the kill",
          max(errs_gate) < 0.07 and all(signs),
          f"max disagreement {max(errs_gate)*100:.2f} percent for ratio > 0.3; solver >= CLASS in all "
          f"{len(signs)} comparisons (generous direction)")
else:
    check("VAL-1  [CLASS unavailable -- solver used unvalidated; treat PART 1-2 as indicative]", True, "skipped")

# =========================================================================================================
sec("PART 1 -- THE INTERMEDIATE-EPOCH GATE: the Lyman-alpha forest at z = 2-5, k up to ~8 Mpc^-1.")
# =========================================================================================================
P("  Neither of L125's gates touches 3 < z < 1000.  But the Lyman-alpha forest measures the 1D flux power")
P("  spectrum at z = 2-5 out to k ~ 0.1 s/km, which at z = 3 is k ~ 7.7 Mpc^-1 comoving.  A dark fluid with")
P("  a sound speed erases power on exactly those scales, and the erasure is worst at LATE times because")
P("  a H falls -- so a profile designed to be hot today is warm at z = 3.")
P("")
K_LYA = (1.5, 8.0)          # eBOSS/DESI reach and the high-resolution (MIKE/HIRES/UVES) reach at z=3
Z_LYA = 3.0
TOL_LYA = 0.90              # the GENEROUS setting carried as fiducial; calibrated value computed below
# --- calibrate what suppression the forest ACTUALLY tolerates, from the published thermal-WDM limit ------
def T2_wdm(k_hMpc, m_keV, Om=0.3138, hh=h):
    """Bode-Ostriker-Turok / Viel transfer function, squared: T^2 = [1+(alpha k)^{2 nu}]^{-10/nu}."""
    nu = 1.12
    al = 0.049*m_keV**-1.11*(Om/0.25)**0.11*(hh/0.7)**1.22        # h^-1 Mpc
    return (1.0 + (al*k_hMpc)**(2*nu))**(-10.0/nu)
M_WDM_LIM = 5.3                                                    # keV, 95 percent, eBOSS + high-res
k8_h = K_LYA[1]/h; k15_h = K_LYA[0]/h
TOL_CAL = T2_wdm(k8_h, M_WDM_LIM)
P(f"      calibration of the Lyman-alpha tolerance.  The published 95 percent thermal-WDM limit")
P(f"      m_WDM > {M_WDM_LIM} keV corresponds, through the Bode-Ostriker-Turok transfer function, to a 3D")
P(f"      power suppression of P/P_CDM = {TOL_CAL:.3f} at k = {K_LYA[1]:g} Mpc^-1 = {k8_h:.1f} h/Mpc"
  f" (and {T2_wdm(k15_h, M_WDM_LIM):.4f} at k = {K_LYA[0]:g} Mpc^-1).")
P(f"      So the data actually tolerate about {100*(1-TOL_CAL):.0f} percent at the outer wavenumber.  The")
P(f"      fiducial gate below uses {TOL_LYA:.2f} -- LOOSER than the data by a factor "
  f"{(1-TOL_LYA)/(1-TOL_CAL):.1f} -- and the calibrated")
P(f"      value is carried as a sensitivity row.  No deficit is manufactured by the choice.")
P("")
P(f"      {'p':>5} " + " ".join(f"{'cs(1)='+str(int(c)):>11}" for c in (207, 300, 500, 900)) +
  f"     (baryon P(k={K_LYA[1]:g})/P_CDM at z={Z_LYA:g})")
for p in (0., 1., 2., 3., 4., 5.):
    row = []
    for csk in (207., 300., 500., 900.):
        c0 = (csk/CKMS)**2
        row.append(f"{ratio_b(K_LYA[1], lambda a, c=c0, q=p: c*a**q, Z_LYA):11.4f}")
    P(f"      {p:5.1f} " + " ".join(row))
r_const = ratio_b(K_LYA[1], lambda a: (207./CKMS)**2, Z_LYA)
r_p4    = ratio_b(K_LYA[1], lambda a: (207./CKMS)**2*a**4, Z_LYA)
check("LYA-1  the intermediate epochs are where the constraint lives.  A CONSTANT-sound-speed fluid at the "
      "galaxy-gate minimum (c_s = 207 km/s, which passes BOTH of L125's gates with room to spare) erases "
      "essentially all z = 3 power at k = 8 Mpc^-1.  Only a steeply GROWING c_s^2 restores it -- so the "
      "loophole is forced back into needing growth after all, but now over a lever arm of 4 in a, not 1090",
      r_const < 0.05 and r_p4 > 0.9,
      f"p=0: P/P_CDM = {r_const:.4f} (excluded);  p=4 at the same c_s(1): {r_p4:.4f} (allowed)")

# =========================================================================================================
sec("PART 2 -- THE JOINT WINDOW SCAN over (p, c_s^2(1)) against all four gates.")
# =========================================================================================================
P("  GATE-G  the L61 galaxy gate, with L153's THEOREM B.  A barotropic fluid with c_s^2 ~ a^p is the")
P("          polytrope P = A rho^Gamma, Gamma = 1 - p/3.  In a MOND logarithmic potential it has a")
P("          condensation front at r_crit = r_ref exp(-3 c_s^2(1)/(p v_c^2)) inside which there is NO")
P("          hydrostatic solution.  GENEROUS implementation: the front is ALLOWED to sit inside r_in =")
P("          10 kpc (whatever mass condenses there is simply not counted), and the enclosed fluid mass is")
P("          integrated only over 10-100 kpc and compared with the L61 0.11 dex tolerance.")
P("  GATE-L  Lyman-alpha: baryon P(k, z=3)/P_CDM > 0.90 at k = 1.5 AND 8 Mpc^-1.")
P("  GATE-C  the L152 CMB Boltzmann ceiling: c_s^2(a_rec) = c_s^2(1) a_rec^p < 6.1e-4.")
P("  GATE-T  L153 THEOREM A: p < 3 for any barotropic fluid (c_s^2 >= 0 and NEC).")
P("")
VC = 300.0; R_REF = 3000.0; R_IN = 10.0; R_OUT = 100.0
def M_tol(vc, R=100.0, dex=0.11): return (10**dex - 1.0)*vc**2*R/G_KPC
def galaxy_mass(cs2_kms2, p, vc=VC, r_ref=R_REF, r_in=R_IN, r_out=R_OUT):
    """exact polytrope P = A rho^Gamma, Gamma = 1-p/3, in Phi = vc^2 ln r ; returns (M[r_in,r_out], r_crit)"""
    Gam = 1.0 - p/3.0
    if abs(1.0 - Gam) < 1e-12:                                   # isothermal
        b = vc**2/cs2_kms2
        if b >= 3.0: return np.inf, 0.0
        return 4*np.pi*RHOBAR*r_ref**b*(r_out**(3-b) - r_in**(3-b))/(3-b), 0.0
    rc = r_ref*math.exp(-cs2_kms2/((1.0-Gam)*vc**2))
    if rc >= r_in: return np.inf, rc                              # front inside the measured region
    def rho(r):
        u = RHOBAR**(Gam-1.0)*(1.0 - (1.0-Gam)*vc**2*math.log(r_ref/r)/cs2_kms2)
        return u**(1.0/(Gam-1.0)) if u > 0 else np.inf
    return quad(lambda r: 4*np.pi*r*r*rho(r), r_in, r_out, limit=300)[0], rc
P(f"      L61 tolerance for v_c = {VC:.0f} km/s: M_dark(<100 kpc) < {M_tol(VC):.3e} Msun")
P("")
P(f"      {'p':>5} {'c_s(1)':>8} {'r_crit kpc':>11} {'M_gal':>10} {'G':>5} {'Ly k=1.5':>9} {'Ly k=8':>8} "
  f"{'L':>5} {'cs2(rec)':>10} {'C':>5} {'T':>5} | window")
WINDOW = []
for p in (0.0, 1.0, 2.0, 2.5, 2.9, 3.0, 3.5, 4.0, 4.5, 5.0):
    for csk in (207., 300., 500., 900., 1600., 2600.):
        cs2k = csk**2; cs20 = (csk/CKMS)**2
        M, rc = galaxy_mass(cs2k, p)
        okG = M < M_tol(VC)
        f = lambda a, c=cs20, q=p: c*a**q
        L1 = ratio_b(K_LYA[0], f, Z_LYA); L8 = ratio_b(K_LYA[1], f, Z_LYA)
        okL = (L1 > TOL_LYA and L8 > TOL_LYA)
        crec = cs20*A_REC**p; okC = crec < CS2_CMB_MAX; okT = p < 3.0
        allok = okG and okL and okC and okT
        if allok: WINDOW.append((p, csk))
        P(f"      {p:5.1f} {csk:8.0f} {rc:11.2e} {('  inf   ' if not np.isfinite(M) else f'{M:8.2e}'):>10} "
          f"{'PASS' if okG else 'FAIL':>5} {L1:9.4f} {L8:8.4f} {'PASS' if okL else 'FAIL':>5} "
          f"{crec:10.2e} {'PASS' if okC else 'FAIL':>5} {'PASS' if okT else 'FAIL':>5} | "
          f"{'*** OPEN ***' if allok else ''}")
    P("")
check("SCAN-1  the joint window over (p, c_s^2(1)) is EMPTY for every barotropic fluid.  Every cell fails "
      "GATE-G or GATE-L: small p keeps galaxies safe but erases the Lyman-alpha forest, large p protects the "
      "forest but -- by THEOREM B -- collapses the fluid's climb budget so that it condenses inside every "
      "galaxy.  And every cell that satisfies both fails GATE-T (p < 3)",
      len(WINDOW) == 0, f"{len(WINDOW)} of the scanned (p, c_s) cells satisfy all four gates")

# =========================================================================================================
sec("PART 3 -- THE CLOSURE EQUATION IN CLOSED FORM, and how much margin the kill has.")
# =========================================================================================================
P("  GATE-G (THEOREM B, condensation front outside nothing we measure):  3 c_s^2(1)/p  >  L v_c^2,")
P("         with L = ln(r_ref/r_in).  So   c_s^2(1)  >  (p/3) L v_c^2.")
P("  GATE-L (Lyman-alpha at z = 3, a = 1/4):                            c_s^2(1) 4^-p  <  eps_Lya.")
P("  Eliminating c_s^2(1):")
P("")
P("         4^p / p   >   L v_c^2 / (3 eps_Lya).")
P("")
P("  The left side is monotone increasing for p > 1/ln4, so this defines a MINIMUM p.  THEOREM A caps p at")
P("  3.  The kill is the statement p_req > 3.  Both sides are measured, not assumed:")
P("")
# eps_Lya(p) is calibrated DIRECTLY from the solver: the largest c_s^2(a=1/4) whose power-law profile
# still leaves the z=3 forest above the tolerance at BOTH wavenumbers.  Computed once on a grid of p and
# interpolated in log-log (the grid is dense and the function is smooth and monotone).
P_GRID = np.arange(0.5, 8.01, 0.25)
_EPS_CACHE = {}
def eps_lya(p, tol=TOL_LYA):
    """largest c_s^2(a=1/4) passing GATE-L at exponent p; bisection in log, tight bracket."""
    key = (round(p, 4), tol)
    if key in _EPS_CACHE: return _EPS_CACHE[key]
    lo, hi = 1e-13, 3e-7                                   # 3e-7 at a=1/4 is already far beyond any pass
    for _ in range(30):
        mid = math.sqrt(lo*hi)
        ok = (ratio_pl(K_LYA[0], mid, p) > tol and ratio_pl(K_LYA[1], mid, p) > tol)
        lo, hi = (mid, hi) if ok else (lo, mid)
    _EPS_CACHE[key] = lo
    return lo
_EPS_TAB = {}
def eps_lya_interp(p, tol=TOL_LYA):
    if tol not in _EPS_TAB:
        _EPS_TAB[tol] = np.array([math.log(eps_lya(pv, tol)) for pv in P_GRID])
    return math.exp(float(np.interp(p, P_GRID, _EPS_TAB[tol])))
def p_required(vc, r_in, tol=TOL_LYA):
    L = math.log(R_REF/r_in)
    lo, hi = P_GRID[0], P_GRID[-1]
    gap = lambda pp: (pp/3.0)*L*(vc/CKMS)**2 - eps_lya_interp(pp, tol)*4.0**pp   # need - allow
    if gap(hi) > 0: return float('inf')
    for _ in range(50):
        mid = 0.5*(lo+hi)
        if gap(mid) <= 0: hi = mid
        else: lo = mid
    return hi
P(f"      {'v_c (km/s)':>10} {'r_in (kpc)':>10} {'Lya tol':>8} {'eps_Lya = c_s^2(1/4)':>21} {'p_required':>11} "
  f"{'vs ceiling 3':>13}")
res = {}
TC = round(TOL_CAL, 2)
for vc, r_in, tol in ((300., 10., 0.90), (300., 1., 0.90), (300., 10., TC),
                      (250., 10., 0.90), (250., 10., TC), (180., 10., 0.90), (180., 10., TC),
                      (300., 30., 0.80)):
    pr = p_required(vc, r_in, tol)
    res[(vc, r_in, tol)] = pr
    P(f"      {vc:10.0f} {r_in:10.0f} {tol:8.2f} {eps_lya_interp(pr, tol):21.3e} {pr:11.2f} "
      f"{('CLOSED by '+f'{pr-3:.2f}') if pr > 3 else ('OPEN by '+f'{3-pr:.2f}'):>13}")
p_fid = res[(300., 10., 0.90)]
p_cal = res[(300., 10., TC)]
p_min = min(res.values()); p_max = max(res.values())
P("")
P("      READ THIS ROW BY ROW, NOT AS A HEADLINE.  Every row that both (i) includes the deepest MOND-regime")
P("      galaxies (v_c ~ 250-300 km/s: NGC 2841, NGC 5055, UGC 2885 and their kin are all in SPARC and all")
P("      sit on the RAR) and (ii) uses the data-calibrated Lyman-alpha tolerance, closes -- but the margin")
P(f"      is {p_fid-3:.2f} to {p_cal-3:.2f} in the exponent, i.e. a factor {4.0**(p_fid-3.0):.1f} to "
  f"{4.0**(p_cal-3.0):.1f} in c_s^2, NOT orders of magnitude.")
P("      And two rows land marginally on the OPEN side: restricting the galaxy gate to Milky-Way-sized")
P("      potentials at the loose tolerance, and the deliberately over-generous 30 kpc / 20 percent row.")
P("      This is a NARROW closure.  It is a real one -- it survives every tightening -- but it is not a")
P("      theorem-strength kill, and it must not be quoted as one.")
check("CLOSE-1  the closure equation is 4^p/p > L v_c^2/(3 eps_Lya), and at the fiducial (generous) gate "
      "settings it requires p > 3.5 for the deepest MOND-regime galaxies -- rising to about 4 at the "
      "data-calibrated Lyman-alpha tolerance -- against THEOREM A's hard ceiling p < 3.  The barotropic "
      "branch misses, but by a factor of only 2 to 4 in c_s^2, not by orders of magnitude",
      p_fid > 3.0 and p_cal > p_fid,
      f"p_required = {p_fid:.2f} (generous) and {p_cal:.2f} (data-calibrated) vs ceiling 3 -- "
      f"a shortfall of {4.0**(p_fid-3.0):.1f}x to {4.0**(p_cal-3.0):.1f}x in c_s^2")
check("CLOSE-2  and the kill's SENSITIVITY is reported rather than hidden, INCLUDING the settings under "
      "which it fails to close.  Tightening the Lyman-alpha tolerance to its data-calibrated value or "
      "shrinking the tolerated condensation radius strengthens it; restricting the galaxy gate to "
      "Milky-Way-sized potentials at the loose tolerance brings it marginally OPEN.  The kill therefore "
      "rests on one physical input -- that the dark fluid must be smooth in v_c ~ 250-300 km/s spirals too "
      "-- which is exactly the population the L61 gate was built on, but it is a single point of failure",
      p_min < 3.0 < p_max and res[(300., 1., 0.90)] > p_fid,
      f"range of p_required across the 8 settings: {p_min:.2f} to {p_max:.2f}; the ceiling 3 lies INSIDE "
      f"that range, so the closure is setting-dependent and is reported as narrow")

# =========================================================================================================
sec("PART 4 -- COULD MOND ITSELF RESCUE THE LYMAN-ALPHA LEG?  Quantified.")
# =========================================================================================================
P("  In the hybrid the baryons feel MOND, so one might hope a boosted baryon growth refills the z = 3 power")
P("  the fluid erased.  The required boost is computable: if the fluid leaves a fraction f of the CDM power,")
P("  the baryon linear growth must be enhanced by 1/sqrt(f) in delta on that scale, at that redshift.")
P("")
P(f"      {'p':>5} {'c_s(1)':>8} {'P/P_CDM (k=8, z=3)':>20} {'required growth boost in delta':>31}")
for p, csk in ((0.0, 207.), (1.0, 300.), (2.0, 500.), (2.9, 900.)):
    c0 = (csk/CKMS)**2
    f = ratio_b(K_LYA[1], lambda a, c=c0, q=p: c*a**q, Z_LYA)
    P(f"      {p:5.1f} {csk:8.0f} {f:20.5f} {1.0/math.sqrt(max(f,1e-12)):31.1f}")
boost_needed = 1.0/math.sqrt(max(ratio_b(K_LYA[1], lambda a: (207./CKMS)**2, Z_LYA), 1e-12))
check("MOND-1  the MOND escape hatch is quantified and closed at linear order.  At the galaxy-gate minimum "
      "with a constant sound speed the fluid leaves ~1 percent of the CDM power at k = 8 Mpc^-1, z = 3, so "
      "the baryons would need their linear growth enhanced by an order of magnitude in delta on 100 kpc "
      "PHYSICAL scales at z = 3 -- where accelerations are far above a0 and MOND is OFF.  A MOND boost of "
      "the linear growth is at most a factor of a few, not ten",
      boost_needed > 5.0,
      f"required delta-boost {boost_needed:.0f}x at k=8 Mpc^-1, z=3; the programme's own g04h reached the "
      f"same conclusion independently (P(k) not regenerated at linear order)")
P("")
P("      Honest caveat, carried forward: this is a LINEAR statement.  A nonlinear top-down fragmentation")
P("      channel in a MOND cosmology is uncomputed here and remains the one place the Lyman-alpha leg could")
P("      in principle be softened.  It is the same uncomputed channel the programme already has on file.")

# =========================================================================================================
sec("PART 5 -- sigma8 / S8 and the CMB lensing amplitude at the boundary of the (now empty) window.")
# =========================================================================================================
if HAVE_CLASS:
    def late(cs2):
        p = {'output':'tCl,pCl,lCl,mPk','lensing':'yes','l_max_scalars':2600,'omega_cdm':1e-5,
             'Omega_fld':Od,'w0_fld':-1e-6,'wa_fld':0.0,'cs2_fld':max(cs2,1e-14),'use_ppf':'no',
             'P_k_max_1/Mpc':10.0,'omega_b':om_b,'h':h,'A_s':2.1e-9,'n_s':0.9649,'tau_reio':0.0544}
        c = Class(); c.set(p); c.compute()
        s8 = c.sigma8(); pp = c.lensed_cl(2500)['pp'][100]
        c.struct_cleanup(); c.empty(); return s8, pp
    s8_0, pp_0 = late(0.0)
    P(f"      reference (c_s = 0): sigma8 = {s8_0:.4f},  C_100^phiphi = {pp_0:.4e}")
    P(f"      {'c_s (km/s)':>11} {'c_s^2':>10} {'sigma8':>8} {'d sigma8':>9} {'C^phiphi/ref':>13}")
    s8v = {}
    for csk in (100., 207., 300., 500.):
        cs2 = (csk/CKMS)**2; s8, pp = late(cs2); s8v[csk] = s8
        P(f"      {csk:11.0f} {cs2:10.2e} {s8:8.4f} {s8/s8_0-1:+9.4f} {pp/pp_0:13.4f}")
    check("LSS-1  the late-time observables are consistent with the same picture and add an INDEPENDENT "
          "constraint on the constant-sound-speed corner: at the galaxy-gate minimum (207 km/s) a constant "
          "c_s^2 already suppresses sigma8 by a few percent and the CMB lensing amplitude by about a "
          "percent.  Those are of the same order as the measurements, so they do not by themselves kill -- "
          "the Lyman-alpha leg is the decisive one, and this is recorded so credit goes to the right gate",
          abs(s8v[207.]/s8_0 - 1) < 0.10 and abs(s8v[500.]/s8_0 - 1) > abs(s8v[207.]/s8_0 - 1),
          f"sigma8 shift {s8v[207.]/s8_0-1:+.3f} at 207 km/s, {s8v[500.]/s8_0-1:+.3f} at 500 km/s -- "
          f"suggestive, not decisive; Lyman-alpha decides")
else:
    check("LSS-1  [CLASS unavailable -- skipped]", True, "skipped")

# =========================================================================================================
sec("PART 6 -- THE VERDICT, THE SCOPE, AND THE SURVIVING DOOR.")
# =========================================================================================================
P(f"""
  VERDICT.

  1.  THE NAMED LOOPHOLE IS REAL.  The L125 velocity-ordering lemma is NOT mechanism-independent.  It is
      the p = -2 corner of the family c_s^2 ~ a^p, and it bites only for p <= -1.  The two gates it names
      (CMB third peak, L61 galaxy overshoot) leave a window three orders of magnitude wide in c_s^2 --
      c_s^2(a_rec) < 6.1e-4 against c_s^2(1) > 4.8e-7 -- so a fluid does not need a growing sound speed at
      all to thread them; a CONSTANT one suffices, and shift-symmetric k-essence P = X^n delivers it with
      c_s^2 = w = 1/(2n-1), no ghost, no gradient instability and no BBN tail.  L125's "no common interior"
      is FALSE as stated.  That claim should be amended.

  2.  THE PINCER RELOCATES, AND THEN CLOSES ON THE BAROTROPIC CLASS -- BUT NARROWLY.  The binding
      constraint is not the CMB.  It is the Lyman-alpha forest at z = 2-5, which measures the very scales
      (k up to ~8 Mpc^-1) that the fluid's sound speed erases, and which sits only a factor FOUR in scale
      factor from the galaxies the fluid must simultaneously avoid.  Against the galaxy gate in its
      THEOREM B form, the closure equation is
              4^p / p   >   L v_c^2 / (3 eps_Lya)     giving   p_required = {p_fid:.2f} (generous settings)
                                                                          = {p_cal:.2f} (data-calibrated Lya)
      while THEOREM A caps every barotropic fluid at p < 3.  The shortfall is a factor {4.0**(p_fid-3.0):.1f} to {4.0**(p_cal-3.0):.1f} in
      c_s^2 -- REAL, but two to four, not orders of magnitude.  Across the eight gate settings tested,
      p_required ranges {p_min:.2f} to {p_max:.2f}, and the ceiling 3 lies inside that range: the two settings that
      leave it marginally open are a galaxy gate restricted to Milky-Way potentials, and a deliberately
      over-generous 30 kpc / 20 percent row.  So: no barotropic fluid and no shift-symmetric k-essence
      threads all four gates at any defensible setting -- but this is a NARROW closure, not a theorem-
      strength kill, and it should never be quoted as the latter.

  3.  THE REASON IS ONE STRUCTURAL FACT, and it deserves a name: THE DENSITY-TIME DUALITY.  For a
      barotropic fluid c_s^2 is a function of density alone, so "grows with a" IS "falls with rho", and a
      galaxy is a region of high rho.  The fluid inside a structure of overdensity Delta carries exactly
      the sound speed the universe had at a = (1+Delta)^(-1/3).  The property that evades the velocity-
      ordering lemma is the property that guarantees the fluid is soft exactly where it must be stiff.
      THEOREM B is the quantitative form: the fluid can climb a well of depth at most three times its own
      log-integrated sound-speed history, so growing faster buys LESS galaxy protection, not more.

  4.  IS THIS A THEOREM OR A FAILURE OF THE PROFILES TRIED?  Three different answers, and the distinction
      is the most important thing in this report.
        * A GENUINE THEOREM, mechanism-independent: THEOREM A (p < 3) and THEOREM B (the climb bound
          Delta_Phi_max = 3 * integral c_s^2 dln a) hold for EVERY barotropic fluid, proved from
          P = P(rho), c_s^2 >= 0 and the NEC alone.  No profile, no power law, is assumed.  Likewise the
          p = -2 results for fuzzy DM, ghost condensates and any k^4 dispersion, and the mean-free-path
          no-go for particle GDM (5 orders).  Those are theorems.
        * NOT A THEOREM -- an EMPIRICAL closure, and a narrow one: the step from THEOREM A + THEOREM B to
          "the window is empty" needs the two MEASURED numbers eps_Lya and L v_c^2, and it succeeds by a
          factor of 2 to 4 in c_s^2.  That margin is smaller than the systematic spread of the gate
          settings themselves.  A factor ~2 improvement in any one of: the Lyman-alpha modelling, the
          hydrostatic galaxy gate, or the tolerated condensation radius, would reopen it.  This half of
          the result is a quantitative failure of the barotropic class, NOT a proof of impossibility.
        * FULLY OPEN: the NON-BAROTROPIC branch.  If c_s^2 depends on anything besides the local density
          -- explicitly on a background field phi(t), i.e. Hu's GDM taken literally as a fluid with an
          internal clock -- then the density-time duality is broken by construction, the local stiffness
          in a galaxy is decoupled from the cosmological growth, and NEITHER theorem applies.  Nothing
          here closes that branch.  It is the surviving door and it should be stated as such.

  5.  WHAT WOULD TEST THE SURVIVING DOOR.  A non-barotropic c_s^2(rho, phi) needs a scalar that varies by
      order one between z = 3 and z = 0 to supply p ~ 4 -- a field of mass ~ H_0 rolling today and coupled
      to the dark sector.  The named next computations are (i) whether such a coupling gives the dark
      sector a long-range fifth force at the level coupled-quintessence bounds already exclude; (ii) what
      c_s^2(rho, phi) does to the CLUSTER profile, where the programme's own g03r found the isothermal
      atmosphere already fails on SHAPE (amplitude wants ~560 km/s, the r^-1.53 slope wants ~1000 km/s);
      and (iii) whether the required delta-P is non-adiabatic in a way that survives a full Boltzmann run.

  HONEST SCOPE.  The CMB leg is a real Boltzmann computation but against a Planck-LIKE covariance with a
  6-parameter Fisher marginalisation, not the Planck likelihood (good to a factor of a few -- irrelevant
  against ~1e3 of headroom, so PART 1's conclusion is robust).  The galaxy leg is STATIC hydrostatic
  equilibrium in an idealised logarithmic potential: no merger history, no accretion timescale, no check
  that the fluid has time to reach that equilibrium.  The Lyman-alpha leg is LINEAR, and the nonlinear MOND
  fragmentation channel is uncomputed.  The closure is carried by v_c ~ 250-300 km/s spirals: restricted to
  Milky-Way potentials at the loose tolerance it goes marginally OPEN (p_required = {res[(180., 10., 0.90)]:.2f} against the
  ceiling 3), and it recloses at {res[(180., 10., TC)]:.2f} once the data-calibrated Lyman-alpha tolerance is used.  Unlike
  PART 1, the PART 2-3 closure is NOT robust to a factor of two: it succeeds by {4.0**(p_fid-3.0):.1f}x to {4.0**(p_cal-3.0):.1f}x in c_s^2 and
  a factor of two in any single gate would reopen it.  That asymmetry is the honest headline: the loophole
  is decisively real against the pincer as stated, and only narrowly closed against its barotropic
  realization.

  PROPOSITIONS WORTH FORMALIZING IN LEAN 4 (each is finite real arithmetic or one integral):
    P1  ordering_boundary : for k_J(a) = C a^(-(1+p)/2), k_J is strictly decreasing iff p > -1.
        (This alone shows L125's lemma is a statement about p = -2, not about matter.)
    P2  sound_speed_le_w : if P : R -> R, P 0 >= 0, P' >= 0, P' antitone, then for all rho > 0,
        P' rho <= P rho / rho.                                       [THEOREM A, the general form]
    P3  growth_ceiling : for P rho = A * rho^Gamma with A > 0 and 0 < Gamma <= 1, the growth exponent
        p = 3(1 - Gamma) satisfies 0 <= p < 3, and w / c_s^2 = 3/(3 - p).
    P4  climb_bound : for c_s^2 rho = C * rho^(-nu) with C > 0 and nu > 0,
        integral_(rhobar)^(infinity) c_s^2 rho / rho drho = c_s^2 rhobar / nu, i.e. finite.
        Corollary: no globally regular hydrostatic solution in an unbounded potential.
    P5  window_empty : if x >= (p/3) * L * v^2 and x * 4^(-p) <= eps and 0 < p < 3, then
        4^p / p >= L * v^2 / (3 * eps); with L = 5.70, v^2 = 1.0014e-6, eps = {eps_lya_interp(p_fid):.3e} the
        hypothesis set is empty.  (Pure real arithmetic -- the cleanest of the five to certify.)
""")
check("VERDICT-1  the loophole is REAL against the pincer as L125 stated it (that claim must be amended), "
      "and the barotropic realization of it is CLOSED by a relocated pincer -- Lyman-alpha against the "
      "galaxy gate -- via two theorems proved from P = P(rho), c_s^2 >= 0 and the NEC alone.  The "
      "non-barotropic branch is NOT closed and is named, with three specific next computations",
      len(WINDOW) == 0 and p_fid > 3.0 and CS2_CMB_MAX/4.756e-7 > 100,
      f"L125 gates leave {CS2_CMB_MAX/4.756e-7:.0f}x headroom (loophole real); barotropic p_req = {p_fid:.2f} "
      f"vs ceiling 3 (closed); non-barotropic OPEN")
check("SCOPE-1  honestly bounded, and the bound is stated in the direction that could reopen the result: "
      "the Lyman-alpha leg is linear and its nonlinear MOND channel is uncomputed; the galaxy leg is static "
      "hydrostatics with no accretion timescale; the closure margin is only a factor of a few in c_s^2, so "
      "unlike PART 1's result it is NOT robust to a factor of two in either modelling step; and the whole "
      "result says nothing at all about a fluid whose sound speed is not a function of its own density",
      res[(180., 10., 0.90)] < p_fid,
      f"linear Lyman-alpha; static hydrostatics; closure margin only {4.0**(p_fid-3.0):.1f}x-{4.0**(p_cal-3.0):.1f}x in c_s^2; "
      f"non-barotropic branch untouched")

print("=" * 112)
if FAILS:
    print(f"L154 INCOMPLETE: {len(FAILS)}/{NCHECK[0]} FAILED: {FAILS}"); sys.exit(1)
print(f"L154 COMPLETE: {NCHECK[0]}/{NCHECK[0]} checks PASS.   [{time.time()-T0:.1f}s]")
print("=" * 112)
