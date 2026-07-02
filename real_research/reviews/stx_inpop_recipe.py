#!/usr/bin/env python3
"""
AGENT A -- s^TX -> INPOP/JPL planetary-ephemeris analysis recipe (computed, both-ways).

FRAMEWORK INPUT (banked, NOT re-derived):
    s^{Tj}(body) = A(body) * gamma^2 * beta_cmb * n_hat_j,   A(body) = a0 / (2 |g_orb(body)|)
    a0 = 9.36e-11 m/s^2 ; beta_cmb = 369.82/299792.458 ; apex l,b = (264.021, 48.253) deg
    Saturn channel: |s^TX| = 8.68e-10  (reviews/stx_target.py, sme_sTX_dipole_perbody.py)

TWO READINGS (footing fork -- run BOTH, per the working rule):
    P (per-body, the ledger's own formula): s^{Tj} scales as 1/g_orb  (prop. to r^2)
    U (universal): a single global s^{Tj} = 8.68e-10 * n_hat (what published SME fits constrain)

PHYSICS (verified from the PDF this session):
    Hees, Bailey, Le Poncin-Lafitte, Bourgoin, Rivoldini, Lamine, Meynadier, Guerlin, Wolf,
    PRD 92, 064049 (2015), arXiv:1508.03478 ("H15"):
      Eq.(3)  two-body EOM: the s^{0j} pieces give (pure gravity, delta_m/M -> ~ -1 for Sun-planet)
              d2r/dt2 |_SME-boost = +/- (2 G M / (c r^3)) [ (s.v) r_vec - (r.v) s_vec ]
      Eq.(7a) <dOmega/dt> = n/(sin i sqrt(1-e^2)) [ eps/e^2 sbar_kP sin w
                            + (e^2-2eps)/e^2 sbar_kQ cos w - (2 n a eps/(e c)) S_k cos w ]
      Eq.(7b) <dw/dt> = -cos i <dOmega/dt> - n [ (e^2-2eps)/(2 e^4) (sbar_PP - sbar_QQ)
                            + (2 n a (e^2-eps)/(c e^3 sqrt(1-e^2))) S_Q ]
              with eps = 1 - sqrt(1-e^2);  S_k = k.s^{Tj}, S_Q = Q.s^{Tj}  (Eq.5, pure gravity)
      Eq.(8)  P,Q,k unit vectors from (i, Omega, w), ecliptic basis
      Table I (INPOP10a supplementary advances, mas/cy):
              Mercury  Odot=1.4+-1.8    wdot=0.4+-0.6
              Venus    Odot=0.2+-1.5    wdot=0.2+-1.5
              EMB      Odot=0.0+-0.9    wdot=-0.2+-0.9
              Mars     Odot=-0.05+-0.13 wdot=-0.04+-0.15
              Jupiter  Odot=-40+-42     wdot=-41+-42
              Saturn   Odot=-0.1+-0.4   wdot=0.15+-0.65
      Table II: S^TX = (-2.9+-8.3)e-9  [the published, HIGHLY CORRELATED marginal;
                Table III shows |corr| up to 0.99 across the 8 SME parameters]
    Fienga et al. 2016 (arXiv:1601.00947, INPOP15a; verified from the PDF this session):
              Mercury wdot_sup = 0.0 +- 1.05 mas/cy (criteria 2); Saturn 0.05 +- 0.20 mas/cy
    Di Ruscio et al. 2020 (A&A 640, A7): 623 Cassini Saturn normal points 2004-2017, metre-level.
    Combined-fit bound sigma(s^TX)=1.3e-9: Hees et al. 2016 review (arXiv:1610.04682, Table 9).

In this realization sbar^{jk}=0 at O(beta) (spatial components enter at O(beta^2)~1e-6 of s^{Tj});
so ONLY the S_k and S_Q terms act.  All spatial-spatial terms dropped, stated explicitly.

Everything below is computed; approximate dataset RMS values are FLAGGED where not verified.
"""
import numpy as np
from scipy.integrate import solve_ivp

np.set_printoptions(precision=4)

# ----------------------------------------------------------------------
# Constants
# ----------------------------------------------------------------------
GM   = 1.32712440018e20        # m^3/s^2 (Sun)
AU   = 1.495978707e11          # m
c    = 299792458.0             # m/s
a0   = 9.36e-11                # m/s^2  framework a0 (INPUT, quarantined)
beta = 369.82e3 / c            # CMB dipole speed (Planck 2018)
gam2 = 1.0/(1.0-beta**2)
SEC_CY = 3.15576e9             # s per Julian century
RAD2MASCY = (180/np.pi)*3600e3*SEC_CY   # rad/s -> mas/cy
YR = 3.15576e7

# ----------------------------------------------------------------------
# 0. Apex direction: galactic -> equatorial -> ecliptic
# ----------------------------------------------------------------------
# J2000 equatorial->galactic rotation (standard IAU matrix rows)
R_eq2gal = np.array([[-0.0548755604, -0.8734370902, -0.4838350155],
                     [ 0.4941094279, -0.4448296300,  0.7469822445],
                     [-0.8676661490, -0.1980763734,  0.4559837762]])
l, b = np.radians(264.021), np.radians(48.253)     # Planck 2018 dipole apex
n_gal = np.array([np.cos(b)*np.cos(l), np.cos(b)*np.sin(l), np.sin(b)])
n_eq  = R_eq2gal.T @ n_gal
RA  = np.degrees(np.arctan2(n_eq[1], n_eq[0])) % 360
Dec = np.degrees(np.arcsin(n_eq[2]))
print("== 0. APEX DIRECTION ==")
print(f"galactic (l,b)=(264.021,48.253) -> equatorial RA={RA:.3f} deg, Dec={Dec:.3f} deg "
      f"(expect ~167.94,-6.94; ledger used 167.9,-6.9)")
assert abs(RA-167.94) < 0.2 and abs(Dec+6.94) < 0.2
eps_obl = np.radians(23.4392911)
R_eq2ecl = np.array([[1,0,0],
                     [0, np.cos(eps_obl), np.sin(eps_obl)],
                     [0,-np.sin(eps_obl), np.cos(eps_obl)]])
n_ecl = R_eq2ecl @ n_eq
print(f"apex unit vector: equatorial {n_eq}, ecliptic {n_ecl}")

# ----------------------------------------------------------------------
# 1. Planets: J2000 mean elements (Standish, JPL 'approximate positions' table)
#    a[AU], e, i, Omega, varpi, L  [deg]
# ----------------------------------------------------------------------
planets = {
 'Mercury': (0.38709893, 0.20563069, 7.00487,  48.33167,  77.45645, 252.25084),
 'Venus'  : (0.72333199, 0.00677323, 3.39471,  76.68069, 131.53298, 181.97973),
 'EMB'    : (1.00000011, 0.01671022, 0.00005, -11.26064, 102.94719, 100.46435),
 'Mars'   : (1.52366231, 0.09341233, 1.85061,  49.57854, 336.04084, 355.45332),
 'Jupiter': (5.20336301, 0.04839266, 1.30530, 100.55615,  14.75385,  34.40438),
 'Saturn' : (9.53707032, 0.05415060, 2.48446, 113.71504,  92.43194,  49.94432),
}
def g_orb(a_AU):                      # mean orbital acceleration
    return GM/(a_AU*AU)**2
A_led  = lambda a_AU: a0/(2*g_orb(a_AU))       # ledger amplitude a0/2g
sSat   = A_led(planets['Saturn'][0])*gam2*beta  # Saturn-channel magnitude
print("\n== 1. FRAMEWORK s^{Tj} PER BODY ==")
print(f"Saturn-channel magnitude A*gamma^2*beta = {sSat:.4e}; x|n_X|={abs(n_eq[0]):.4f} "
      f"-> |s^TX|={sSat*abs(n_eq[0]):.3e}  (banked 8.68e-10; 1% offset = Saturn a-convention "
      f"9.53707 AU Standish elements vs ledger 9.5826 AU)")
assert abs(sSat*abs(n_eq[0]) - 8.68e-10) < 0.12e-10
def s_vec(planet, reading):           # ecliptic-frame s^{Tj} 3-vector
    if reading == 'P':                # per-body (ledger formula)
        return A_led(planets[planet][0])*gam2*beta*n_ecl
    return sSat*n_ecl                 # universal at the Saturn-channel value

# ----------------------------------------------------------------------
# 2. Secular rates, H15 Eq.(7)   [only S_k, S_Q terms survive: sbar^{jk}=0 here]
# ----------------------------------------------------------------------
def PQk(i, Om, w):
    P = np.array([ np.cos(Om)*np.cos(w)-np.cos(i)*np.sin(Om)*np.sin(w),
                   np.sin(Om)*np.cos(w)+np.cos(i)*np.cos(Om)*np.sin(w),
                   np.sin(i)*np.sin(w)])
    Q = np.array([-np.cos(Om)*np.sin(w)-np.cos(i)*np.sin(Om)*np.cos(w),
                  -np.sin(Om)*np.sin(w)+np.cos(i)*np.cos(Om)*np.cos(w),
                   np.sin(i)*np.cos(w)])
    k = np.array([ np.sin(i)*np.sin(Om), -np.sin(i)*np.cos(Om), np.cos(i)])
    return P, Q, k

def secular_rates(planet, reading):
    a_AU, e, i, Om, vp, L = planets[planet]
    i, Om, vp = np.radians([i, Om, vp]); w = vp - Om
    a = a_AU*AU; n = np.sqrt(GM/a**3); epse = 1-np.sqrt(1-e**2)
    P, Q, k = PQk(i, Om, w)
    s = s_vec(planet, reading); Sk, SQ = k@s, Q@s
    dOm = n/(np.sin(i)*np.sqrt(1-e**2)) * ( -(2*n*a*epse/(e*c)) * Sk * np.cos(w) )
    dw  = -np.cos(i)*dOm - n*( 2*n*a*(e**2-epse)/(c*e**3*np.sqrt(1-e**2)) * SQ )
    return dOm*RAD2MASCY, dw*RAD2MASCY     # mas/cy

# INPOP10a supplementary advances (H15 Table I), mas/cy
inpop10a = {'Mercury':((1.4,1.8),(0.4,0.6)), 'Venus':((0.2,1.5),(0.2,1.5)),
            'EMB':((0.0,0.9),(-0.2,0.9)),    'Mars':((-0.05,0.13),(-0.04,0.15)),
            'Jupiter':((-40,42),(-41,42)),   'Saturn':((-0.1,0.4),(0.15,0.65))}
# INPOP15a updates (Fienga+16, criteria 2), perihelia only
inpop15a_w = {'Mercury':1.05, 'Saturn':0.20}

print("\n== 2. SECULAR DRIFT RATES (mas/cy) at the framework prediction ==")
print(f"{'planet':8s} {'reading':7s} {'dOmega/dt':>12s} {'dw/dt':>12s} {'sigma_w(10a)':>13s} {'sigma_w(15a)':>13s}")
for rd in ('P','U'):
    for pl in planets:
        dOm, dw = secular_rates(pl, rd)
        s10 = inpop10a[pl][1][1]; s15 = inpop15a_w.get(pl, float('nan'))
        print(f"{pl:8s} {rd:7s} {dOm:12.3e} {dw:12.3e} {s10:13.2f} {s15:13.2f}")

# ----------------------------------------------------------------------
# 3. CROSS-CHECK: direct numerical integration of H15 Eq.(3) boost term vs Eq.(7)
#    (Mercury, s scaled x1e8 for numerics, both EOM signs tested)
# ----------------------------------------------------------------------
def kepler_state(planet, t=0.0):
    a_AU, e, i, Om, vp, L = planets[planet]
    i, Om, vp, L = np.radians([i, Om, vp, L]); w = vp-Om
    a = a_AU*AU; n = np.sqrt(GM/a**3)
    M = (L - vp) + n*t
    E = M
    for _ in range(60): E = E - (E-e*np.sin(E)-M)/(1-e*np.cos(E))
    xp = a*(np.cos(E)-e); yp = a*np.sqrt(1-e**2)*np.sin(E)
    r = np.array([xp,yp,0]); Edot = n/(1-e*np.cos(E))
    v = np.array([-a*np.sin(E)*Edot, a*np.sqrt(1-e**2)*np.cos(E)*Edot, 0])
    P,Q,k = PQk(i,Om,w); Rm = np.column_stack([P,Q,k])
    return Rm@r, Rm@v

def eom(t, y, s, sign):
    r, v = y[:3], y[3:]; rn = np.linalg.norm(r)
    acc = -GM*r/rn**3 + sign*(2*GM/(c*rn**3))*((s@v)*r-(r@v)*s)
    return np.hstack([v, acc])

def osc_wOm(r, v):
    h = np.cross(r,v); ev = np.cross(v,h)/GM - r/np.linalg.norm(r)
    nv = np.cross([0,0,1], h)
    w = np.arccos(np.clip(nv@ev/np.linalg.norm(nv)/np.linalg.norm(ev),-1,1))
    if ev[2] < 0: w = 2*np.pi - w
    Om = np.arctan2(nv[1], nv[0])
    return w, Om

print("\n== 3. EOM (Eq.3) vs SECULAR FORMULA (Eq.7) CROSS-CHECK, Mercury, s x 1e8 ==")
SCALE = 1e8
sM = s_vec('Mercury','P')*SCALE
r0, v0 = kepler_state('Mercury')
T = 30*YR; ts = np.linspace(0, T, 500)
dOm_th, dw_th = [x*SCALE for x in secular_rates('Mercury','P')]
for sign in (+1,-1):
    sol_p = solve_ivp(eom,(0,T),np.hstack([r0,v0]),t_eval=ts,args=(sM,sign),rtol=3e-12,atol=1e-4,method='DOP853')
    sol_0 = solve_ivp(eom,(0,T),np.hstack([r0,v0]),t_eval=ts,args=(sM*0,1),rtol=3e-12,atol=1e-4,method='DOP853')
    dws, dOms = [], []
    for i_t in range(len(ts)):
        wp,Op = osc_wOm(sol_p.y[:3,i_t], sol_p.y[3:,i_t])
        w0,O0 = osc_wOm(sol_0.y[:3,i_t], sol_0.y[3:,i_t])
        dws.append(wp-w0); dOms.append(Op-O0)
    dw_fit  = np.polyfit(ts, np.unwrap(dws), 1)[0]*RAD2MASCY
    dOm_fit = np.polyfit(ts, np.unwrap(dOms),1)[0]*RAD2MASCY
    print(f" sign={sign:+d}: numeric dw/dt={dw_fit:.4e}, dOm/dt={dOm_fit:.4e}  mas/cy "
          f"| Eq.7: dw/dt={dw_th:.4e}, dOm/dt={dOm_th:.4e}")

# ----------------------------------------------------------------------
# 4. RANGE-SIGNATURE experiment: what the raw ranging actually sees,
#    AFTER absorbing the planet's 6 initial conditions + GM_sun (the honest part)
# ----------------------------------------------------------------------
windows = {  # dataset windows (yr from J2000) + [sigma_NP(m), N] -- RMS/N values FLAGGED approx
 'Mercury': (11.0, 15.0, 1.0, 1000, 'MESSENGER 2011-2015 range NPs (~1 m; FLAG: approx, Park+2017/Verma+2014)'),
 'Mars'   : ( 5.0, 20.0, 1.2, 20000,'MGS/MEX/MRO/Odyssey range (~1.2 m; FLAG: approx, INPOP19a/DE440 docs)'),
 'Saturn' : ( 4.0, 17.7, 6.0, 623,  'Cassini 623 NPs 2004-2017, metre-level (Di Ruscio+2020; 6 m = mid FLAG)'),
 'Jupiter': (16.5, 26.0, 15.0, 45,  'Juno perijove range (~15 m; FLAG: rough, INPOP21a doc)'),
}
def integrate(y0, sv, ts, gm_fac=1.0):
    return solve_ivp(
        lambda t,y: np.hstack([y[3:], -GM*gm_fac*y[:3]/np.linalg.norm(y[:3])**3
                    + (2*GM/(c*np.linalg.norm(y[:3])**3))*((sv@y[3:])*y[:3]-(y[:3]@y[3:])*sv)]),
        (ts[0],ts[-1]), y0, t_eval=ts, rtol=3e-12, atol=1e-4, method='DOP853').y[:3]

def range_signature(planet, reading):
    """BOTH bodies (planet AND Earth/EMB) carry their s^{Tj}; two absorption levels."""
    t0, t1, sig, N, note = windows[planet]
    ts = np.linspace(t0*YR, t1*YR, 400)
    s_pl = s_vec(planet, reading)*1e6                    # scale x1e6, divide later
    s_E  = s_vec('EMB',  reading)*1e6
    y0p = np.hstack(kepler_state(planet, ts[0]))
    y0e = np.hstack(kepler_state('EMB',  ts[0]))
    z = np.zeros(3)
    rp0, re0 = integrate(y0p, z, ts), integrate(y0e, z, ts)
    rho0 = np.linalg.norm(rp0-re0, axis=0)
    drho = (np.linalg.norm(integrate(y0p,s_pl,ts)-integrate(y0e,s_E,ts), axis=0) - rho0)/1e6
    cols = []                                            # FD partials: 6 planet ICs, 6 EMB ICs, GM
    for body,(y0_,other) in (('pl',(y0p,re0)), ('E',(y0e,rp0))):
        for j in range(6):
            dy = np.zeros(6); step = 1e-7*np.linalg.norm(y0_[:3] if j<3 else y0_[3:]); dy[j]=step
            rj = integrate(y0_+dy, z, ts)
            d  = rj-other if body=='pl' else other-rj
            cols.append((np.linalg.norm(d, axis=0)-rho0)/step)
    cols.append((np.linalg.norm(integrate(y0p,z,ts,1+1e-9)-integrate(y0e,z,ts,1+1e-9),axis=0)-rho0)/1e-9)
    Adm = np.array(cols).T
    nrm = np.linalg.norm(Adm, axis=0); nrm[nrm==0]=1.0; Adm = Adm/nrm
    def fit(M):
        with np.errstate(all='ignore'):        # spurious Accelerate-BLAS matmul warnings on macOS
            r = drho - M@np.linalg.lstsq(M, drho, rcond=None)[0]
        assert np.all(np.isfinite(r)), "non-finite residual: real numerical problem"
        return r
    res_opt = fit(np.hstack([Adm[:,:6],  Adm[:,12:]]))   # planet ICs + GM only (optimistic)
    res_con = fit(Adm)                                    # + Earth ICs too   (conservative)
    return drho, res_opt, res_con, sig, N, note

print("\n== 4. RANGE SIGNATURES (meters), both bodies perturbed, two absorption levels ==")
print(f"{'planet':8s} {'rd':3s} {'raw p2p':>10s} {'RMS opt':>10s} {'RMS con':>10s} {'sig/sqrtN':>10s} "
      f"{'S/N o':>7s} {'S/N c':>7s} {'sigma_A(ded,con)':>16s}")
sn_ded = {'P':{}, 'U':{}}
for rd in ('P','U'):
    for pl in windows:
        drho, ro, rc, sig, N, note = range_signature(pl, rd)
        rms_o, rms_c = np.sqrt(np.mean(ro**2)), np.sqrt(np.mean(rc**2))
        noise = sig/np.sqrt(N)
        sn_o, sn_c = rms_o/noise, rms_c/noise
        sn_ded[rd][pl] = sn_c                             # use CONSERVATIVE for the ledger
        sigA = sSat/sn_c if sn_c>0 else float('inf')
        print(f"{pl:8s} {rd:3s} {np.ptp(drho):10.3e} {rms_o:10.3e} {rms_c:10.3e} {noise:10.3e} "
              f"{sn_o:7.2f} {sn_c:7.2f} {sigA:16.2e}  [{note[:38]}]")
print("  opt = planet ICs+GM absorbed; con = also Earth ICs absorbed PER DATASET (over-generous")
print("  since Earth ICs are shared across datasets in a real global fit -> truth in between).")
print("  S/N idealized: white noise, coherent template, no asteroid/systematic floor.")

# ----------------------------------------------------------------------
# 5. DIY 1-PARAMETER FIT on the PUBLIC supplementary advances (the crude bound NOW)
#    amplitude A normalized to the Saturn-channel |s|=sSat; EMB node EXCLUDED (i=5e-5 deg
#    -> node ill-defined, 1/sin i artifact; flagged both-ways below)
# ----------------------------------------------------------------------
print("\n== 5. CRUDE PUBLIC-DATA BOUND: 1-param LSQ on published wdot/Odot advances ==")
print("   EMB EXCLUDED ENTIRELY: i_EMB=5e-5 deg makes the node ill-defined; the 1/sin(i)")
print("   artifact leaks into BOTH its Odot AND wdot (only varpi=w+Om is finite).")
for rd in ('P','U'):
    dOm_e, dw_e = secular_rates('EMB', rd)
    print(f"   [EMB check, reading {rd}: dOm={dOm_e:+.3f}, dw={dw_e:+.3f}, "
          f"finite varpi-dot={dOm_e+dw_e:+.4f} mas/cy vs measured w-dot sigma 0.9]")
def diy_fit(reading, use15a):
    m, y, w = [], [], []
    for pl in planets:
        if pl == 'EMB':
            continue
        dOm, dw = secular_rates(pl, reading)   # at A = sSat (prediction)
        (Oval,Osig),(wval,wsig) = inpop10a[pl]
        if use15a and pl in inpop15a_w:
            wval, wsig = (0.0 if pl=='Mercury' else 0.05), inpop15a_w[pl]
        m.append(dOm); y.append(Oval); w.append(Osig)
        m.append(dw); y.append(wval); w.append(wsig)
    m, y, w = map(np.array,(m,y,w))
    Ahat = np.sum(m*y/w**2)/np.sum(m**2/w**2)      # in units of the prediction
    sigA = 1/np.sqrt(np.sum(m**2/w**2))
    return Ahat*sSat, sigA*sSat
for rd in ('P','U'):
    for u15 in (False,True):
        Ah, sA = diy_fit(rd,u15)
        lab = 'INPOP15a-updated' if u15 else 'INPOP10a Table I'
        print(f" reading {rd}, {lab:17s}: A_hat = {Ah:+.3e},  sigma_A = {sA:.3e} "
              f"(pred {sSat:.2e} -> pred/sigma = {sSat/sA:.4f})")

# ----------------------------------------------------------------------
# 6. KILL CONDITIONS (both ways, stated as prominently as detection)
# ----------------------------------------------------------------------
print("\n== 6. KILL / DETECTION LEDGER ==")
for rd in ('P','U'):
    tot = np.sqrt(sum(v**2 for v in sn_ded[rd].values()))
    print(f" reading {rd}: combined dedicated-ranging S/N (quadrature over datasets) = {tot:.2f}")
    if tot > 0:
        sig_dedicated = sSat/tot
        print(f"   -> implied dedicated 1-param sigma_A ~ {sig_dedicated:.2e}"
              f"   (95% null bound would be |A| < {2*sig_dedicated:.2e})")
print(f"""
 Reading U detection: dedicated fit returns A = ({sSat:.2e}) +/- sigma with the SIGN of n_X<0
   (i.e. NEGATIVE s^TX, matching the H15 central value -2.9e-9) and direction consistent with
   RA=167.94, Dec=-6.94.
 Reading U kill: dedicated 1-param fit gives |A| < 2 sigma with sigma <= 4.3e-10
   -> 8.68e-10 excluded at >=2 sigma; at sigma ~ 3e-10 a null kills at ~3 sigma.
 Reading P: see the computed S/N above -- if << 1, planetary ranging CANNOT reach the
   per-body realization and this front is NOT in-hand (honest outcome; no manufacture).
""")
print("EXIT 0 -- every number above is computed in this file.")
