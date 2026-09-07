#!/usr/bin/env python3
"""
g04j -- the last scale-selective door: wave dark matter (an ultralight boson, m ~ 1e-24 eV) as the action's dark fluid
======================================================================================================================
After the thermal relic (g04f-g04i: Pauli exclusion has no interior between N_eff and the RAR) and four condensate constructions
(g03w-g03z), one mechanism that keeps a cold-on-cluster-scales fluid OUT of galaxies has never been run: de Broglie exclusion.
An ultralight boson with m ~ 1e-24 eV has a half-mode mass between galaxies and clusters and a de Broglie length of tens of kpc
at galaxy speeds but ~10 kpc at cluster speeds.  Three gates, each of which can fail, plus a control:

  W0 [control]     the partial-wave scattering solver returns unit density for a free plane wave (sum rule) to 1%;
  W1 [selection]   m for which the half-mode mass M_1/2 ~ 5e10 (m/1e-22 eV)^(-4/3) Msun (Hu, Barkana & Gruzinov 2000; Hui et al. 2017,
                   approximate) lies between 1e12 (galaxies form no halo) and 1e14 Msun (clusters do): the window must be non-empty;
  W2 [sea response] steady-state density enhancement of a coherent sea (plane wave, v_inf = 50-200 km/s) in the fixed MOND well of a
                   5e10 Msun disc (log potential, v_f = (G M_b a0)^1/4, truncated at the 0.02 a0 external-field radius), solved exactly
                   by partial waves; the WAVE/CLASSICAL ratio S is the suppression of the well's pull: exclusion needs S < 0.33 inside 10 kpc;
  W3 [pincer]      the captured cosmic share (g04i's cold infall) cannot be packed below the de Broglie length at the local escape speed:
                   the RAR (25% of M_b inside 10 kpc), the BTFR normalisation (25% inside 30 kpc) and KiDS (14% of the cold mass inside
                   100 kpc) each give an UPPER bound on m; cluster formation (M_1/2 < 1e14) gives a LOWER bound; a window must exist;
  W4 [sigma_8]     the FDM transfer function T(k) = cos(x^3)/(1 + x^8), x = 1.61 m_22^(1/18) k/k_Jeq, k_Jeq = 9 m_22^(1/2) Mpc^-1
                   (Hu, Barkana & Gruzinov 2000) grown with g04h's causal-boost law at |K2| in {1e5, 2.5e5, 1e6}: sigma_8 within 20% of 0.81;
  W5 [forest]      the same growth read at z = 3: P(k)/P_LCDM(k) at k = 1, 2, 5 h/Mpc must lie within a factor 1.5 of unity at k = 1-2
                   (the Lyman-alpha forest's 1D flux power is reproduced by LCDM to ~10-20% there; a factor 1.5 is generous).
Both footings.  FAIL marks a requirement the door does not meet.  The classical control uses the same solver at a de Broglie length of
4 kpc (m x v large), so S is a like-for-like ratio; the steady scattering state is a proxy for capture efficiency, labelled as such.

OUTCOME (2026-09-06 run, 3 FAIL of 6): W0 control 0.3%; W1 a selection window exists [3.3e-25, 1.1e-23] eV; W2 FAIL -- the wave sea's
steady-state response to the well is NOT suppressed (S = 0.92-1.03 at lambda_dB = 60-240 kpc): de Broglie exclusion does not weaken the
well's pull; W3 FAIL -- the uncertainty-limited core gives m < 3.4e-25 eV (BTFR, 30 kpc) and m < 2.3e-25 eV (KiDS, 100 kpc) against
m > 3.3e-25 eV for clusters to form: a pincer with no interior (factor 1.4); W4 passes only trivially (|K2| = 1e6, sigma_8 = 0.86-0.91,
because the cutoff sits above the sigma_8 scale); W5 FAIL -- at z = 3 the boost-grown power at k = 1-2 h/Mpc is 0.00-0.45 of LCDM's at
|K2| = 1e6 and 4-90x at 1e5: no |K2| gives the forest its power.  The wave door is closed on the action's own terms.
"""
import numpy as np, math, json, sys, time
from scipy.integrate import solve_ivp
FAILS = []
def check(name, ok, detail=""):
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f"   ({detail})" if detail else ""), flush=True)
    if not ok: FAILS.append(name)
T0 = time.time()
G = 6.674e-11; c = 2.998e8; hbar = 1.0546e-34; eV = 1.602e-19; MSUN = 1.989e30; kpc = 3.0857e19; Mpc = 3.0857e22
h = 0.674; H0 = h*100e3/Mpc; Om, OL, Ob, Od = 0.315, 0.685, 0.049, 0.266; ns = 0.965; sig8_target = 0.81
rho_c = 3*H0**2/(8*math.pi*G); A0 = {"canonical": 9.3619e-11, "alt": 1.1279e-10}; Mb = 5e10*MSUN
print("=" * 118); print("g04j -- wave dark matter (m ~ 1e-24 eV) as the last scale-selective dark-sector door"); print("=" * 118, flush=True)
# ---------------- W1: scale selection ----------------
M_half = lambda m: 5e10*(m/1e-22)**(-4/3)
lam_dB = lambda m, v: 2*math.pi*hbar/(m*eV/c**2*v)
mlo = 1e-22*(5e10/1e14)**0.75; mhi = 1e-22*(5e10/1e12)**0.75
print(f"    W1: M_1/2 = 1e12 Msun at m = {mhi:.2e} eV, 1e14 Msun at m = {mlo:.2e} eV; window [{mlo:.1e}, {mhi:.1e}] eV")
for m in (1e-24, 3e-24, 1e-23):
    print(f"        m = {m:.0e} eV: M_1/2 = {M_half(m):.1e} Msun; lambda_dB = {lam_dB(m, 1e5)/kpc:.0f} kpc at 100 km/s, {lam_dB(m, 4.3e5)/kpc:.0f} kpc at 430 km/s (galaxy escape), {lam_dB(m, 1e6)/kpc:.0f} kpc at 1000 km/s (cluster)")
check("W1 [selection] a mass window exists where galaxies form no halo (M_1/2 > 1e12) and clusters do (M_1/2 < 1e14)", mlo < mhi, f"[{mlo:.1e}, {mhi:.1e}] eV")
# ---------------- the well and the partial-wave solver ----------------
def well(a0):
    vf = (G*Mb*a0)**0.25; r_efe = vf**2/(0.02*a0)
    Phi = lambda r: np.where(r < r_efe, vf**2*np.log(np.maximum(r, 1e-3*kpc)/r_efe), 0.0)
    return vf, r_efe, Phi
def enhancement(k, Phi, r_efe, v_inf, r_out_fac=1.25, pts_per_wave=32):
    """Angle-averaged |psi|^2/|psi_inf|^2 at sample radii for a unit plane wave of wavenumber k in the potential Phi (SI).
    Numerov outward integration of u_l'' + [k^2 (1 - 2 Phi/v^2) - l(l+1)/r^2] u_l = 0 for all l at once.  Each partial wave is
    started at r_start(l) = max(r0, 0.1 l/k), well inside its classical turning point, with the regular behaviour u ~ r^(l+1) (relative
    values only: the amplitude is fixed at the outer edge, where Phi = 0, by matching to a (kr) j_l + b (kr) y_l).
    E(r) = sum_l (2l+1) u_l^2/(k r)^2, which is exactly 1 for Phi = 0 (the plane-wave sum rule)."""
    from scipy.special import spherical_jn, spherical_yn
    R_out = r_out_fac*r_efe
    r0 = 0.02*kpc; kmax = k*math.sqrt(1 + 2*abs(float(Phi(np.array([r0]))[0]))/v_inf**2)
    dr = min(0.01/k, 2*math.pi/kmax/pts_per_wave, 0.5*kpc); n = int(R_out/dr) + 3          # 0.01/k resolves the centrifugal term at the launch radius 0.1 l/k
    r = r0 + dr*np.arange(n); V = 1 - 2*Phi(r)/v_inf**2
    lmax = int(1.3*k*R_out) + 25; l = np.arange(lmax + 1, dtype=float); li = l.astype(int)
    istart = np.clip(np.searchsorted(r, np.maximum(r0, 0.1*l/k)), 1, n - 3)
    samp = np.unique(np.concatenate([np.geomspace(0.5*kpc, R_out, 160), [10*kpc, 30*kpc, 100*kpc, 200*kpc, 300*kpc]]))
    samp = samp[(samp > r[3]) & (samp < R_out - 3*dr)]; sidx = np.unique(np.searchsorted(r, samp)); samp = r[sidx]     # sample at grid radii exactly
    store = np.zeros((len(samp), lmax + 1)); lstore = np.zeros((len(samp), lmax + 1)); logs = np.zeros(lmax + 1)
    f = lambda i: k**2*V[i] - l*(l + 1)/r[i]**2
    y0 = np.zeros(lmax + 1); y1 = np.zeros(lmax + 1)
    early = istart <= 2                                          # partial waves that start at the grid origin (l = 0, 1, ...)
    y1 = np.where(early, 1e-150, 0.0); y0 = np.where(early, 1e-150*(r[0]/r[1])**(l + 1), 0.0); istart = np.where(early, 0, istart)
    fm, f0 = f(0), f(1); h2 = dr*dr; j = 0
    for i in range(1, n - 1):
        fp = f(i + 1)
        y2 = (2*(1 - 5*h2*f0/12)*y1 - (1 + h2*fm/12)*y0)/(1 + h2*fp/12)
        launch = istart == i + 1
        if launch.any():
            y2 = np.where(launch, 1e-150, y2); y1 = np.where(launch, 1e-150*(r[i]/r[i + 1])**(l + 1), y1)
        scale = np.maximum(np.abs(y2), 1e-300); big = scale > 1e100
        if big.any(): y2 = np.where(big, y2/scale, y2); y1 = np.where(big, y1/scale, y1); logs = logs + np.where(big, np.log(scale), 0.0)
        y0, y1, fm, f0 = y1, y2, f0, fp
        while j < len(sidx) and sidx[j] == i + 1:
            store[j] = y1; lstore[j] = logs; j += 1
    rA, rB = r[n - 2], r[n - 1]; uA, uB = y0, y1
    jA, yA = k*rA*spherical_jn(li, k*rA), k*rA*spherical_yn(li, k*rA)
    jB, yB = k*rB*spherical_jn(li, k*rB), k*rB*spherical_yn(li, k*rB)
    det = jA*yB - jB*yA; a = (uA*yB - uB*yA)/det; b = (jA*uB - jB*uA)/det; amp = np.sqrt(a*a + b*b)
    good = np.isfinite(amp) & (amp > 0); amp = np.where(good, amp, np.inf)
    E = np.array([np.sum((2*l + 1)*(store[q]*np.exp(np.minimum(lstore[q] - logs, 0.0))/amp)**2)/(k*samp[q])**2 for q in range(len(samp))])   # undo the running rescale (stored values are at an earlier scale)
    return samp, E
def mass_inside(samp, E, R):
    sel = samp <= R; rr = np.concatenate([[0.0], samp[sel]]); EE = np.concatenate([[E[0]], E[sel]])
    return float(np.trapz(EE*4*math.pi*rr**2, rr))                                   # in units of rho_bar (m^3)
# ---------------- W0: free-wave control ----------------
vf_c, refe_c, Phi_c = well(A0["canonical"])
k_test = 2*math.pi/(60*kpc); samp0, E0 = enhancement(k_test, lambda r: np.zeros_like(r), refe_c, 1e5)
check("W0 [control] the partial-wave sum returns unit density for a free plane wave at every sample radius (to 1%)", np.all(np.abs(E0 - 1) < 0.01), f"max |E - 1| = {np.max(np.abs(E0 - 1)):.4f} over {len(samp0)} radii, l_max = {int(1.3*k_test*1.25*refe_c) + 25}")
# ---------------- W2: the sea's steady-state response, wave vs classical ----------------
RES = {}
for foot, a0 in A0.items():
    vf, r_efe, Phi = well(a0)
    print(f"    {foot}: v_f = {vf/1e3:.0f} km/s, external-field radius {r_efe/kpc:.0f} kpc", flush=True)
    for v_inf in (5e4, 1e5, 2e5):
        kc = 2*math.pi/(4*kpc); sc, Ec = enhancement(kc, Phi, r_efe, v_inf)
        Mc10, Mc200 = mass_inside(sc, Ec, 10*kpc), mass_inside(sc, Ec, 200*kpc)
        line = f"      v_inf = {v_inf/1e3:.0f} km/s: classical (lambda = 4 kpc) <E>(<10 kpc) = {Mc10/(4/3*math.pi*(10*kpc)**3):.2f}, <E>(<200 kpc) = {Mc200/(4/3*math.pi*(200*kpc)**3):.2f};"
        for m in (1e-24, 3e-24):
            kw = m*eV/c**2*v_inf/hbar; sw, Ew = enhancement(kw, Phi, r_efe, v_inf)
            S10, S200 = mass_inside(sw, Ew, 10*kpc)/Mc10, mass_inside(sw, Ew, 200*kpc)/Mc200
            RES[(foot, v_inf, m)] = dict(S10=S10, S200=S200, lam=lam_dB(m, v_inf)/kpc)
            line += f"  m = {m:.0e} eV (lambda {lam_dB(m, v_inf)/kpc:.0f} kpc): S(<10) = {S10:.2f}, S(<200) = {S200:.2f};"
        print(line, flush=True)
check("W2 [sea response] the wave sea's steady-state density response to the well is suppressed relative to the classical one by at least 3x inside 10 kpc (S < 0.33) at m = 1e-24 eV for every v_inf, both footings", all(v["S10"] < 0.33 for key, v in RES.items() if key[2] == 1e-24), f"S(<10 kpc) = {min(v['S10'] for key, v in RES.items() if key[2] == 1e-24):.2f}-{max(v['S10'] for key, v in RES.items() if key[2] == 1e-24):.2f}: the wave sea responds like the classical one even at lambda_dB = 60-240 kpc; de Broglie exclusion does not reduce the well's pull")
# ---------------- W3: the uncertainty-limited core and the three mass bounds ----------------
# The cosmic share that falls in (g04i's cold infall: M/M_b = 2.7-3.3 inside 10 kpc, 8.7-9.5 inside 30 kpc, 24 inside 100 kpc) cannot be
# packed by a wave below its de Broglie length at the local escape speed: the bound mass inside R is at most the cold mass inside
# lambda_c(R) spread uniformly over lambda_c, i.e. M_wave(<R) = M_cold(<lambda_c) (R/lambda_c)^3 when lambda_c > R.  The RAR/BTFR tolerate
# 25% of M_b inside 10 and 30 kpc; KiDS tolerates 14% of the CDM-like mass inside 100-200 kpc; clusters (1e14 Msun) must still form.
COLD = {"canonical": {10: 2.71, 30: 8.68, 100: 23.92}, "alt": {10: 3.26, 30: 9.54, 100: 24.04}}      # g04i, in units of M_b
def vesc(a0, r):
    vf = (G*Mb*a0)**0.25; r_efe = vf**2/(0.02*a0); return math.sqrt(2*vf**2*math.log(r_efe/r)) if r < r_efe else 1.0
def m_needed(a0, R_kpc, M_cold, tol):
    """largest m for which the wave-limited mass inside R is below tol (in M_b): lambda_c must exceed R (M_cold/tol)^(1/3)."""
    lam_c = R_kpc*kpc*(M_cold/tol)**(1/3); v = vesc(a0, R_kpc*kpc)
    return 2*math.pi*hbar/(lam_c*v)/(eV/c**2)
m_cl = 1e-22*(5e10/1e14)**0.75
BOUNDS = {}
for foot, a0 in A0.items():
    mb = dict(RAR10=m_needed(a0, 10, COLD[foot][10], 0.25), BTFR30=m_needed(a0, 30, COLD[foot][30], 0.25), KiDS100=m_needed(a0, 100, COLD[foot][100], 0.14*COLD[foot][100]))
    BOUNDS[foot] = mb
    print(f"    W3: {foot}: m must be BELOW {mb['RAR10']:.1e} eV (RAR, 10 kpc), {mb['BTFR30']:.1e} eV (BTFR normalisation, 30 kpc), {mb['KiDS100']:.1e} eV (KiDS, 100 kpc) and ABOVE {m_cl:.1e} eV (clusters of 1e14 Msun must form)", flush=True)
check("W3 [pincer] a mass exists that keeps the wave-limited captured mass inside 30 kpc below 25% of the baryons and inside 100 kpc below 14% of the cold value, while clusters still form (both footings)", all(min(mb["BTFR30"], mb["KiDS100"]) > m_cl for mb in BOUNDS.values()), json.dumps({f: {k: f"{v:.1e}" for k, v in mb.items()} for f, mb in BOUNDS.items()}) + f" vs cluster floor {m_cl:.1e} eV")
# ---------------- cosmology helpers (g04h, copied) ----------------
def Hc(a): return H0*math.sqrt(Om*a**-3 + OL)
def dlnH_dlna(a): return -1.5*Om*a**-3/(Om*a**-3 + OL)
def t_of(a):
    aa = np.linspace(1e-6, a, 4000); return float(np.trapz(1/(aa*np.sqrt(Om*aa**-3 + OL)*H0), aa))
TT_A = np.geomspace(1e-4, 1.0, 3000); TT_T = np.array([t_of(a_) for a_ in TT_A])
def t_a(a): return float(np.interp(a, TT_A, TT_T))
def D_lcdm(a):
    aa = np.linspace(1e-4, a, 20000); E = np.sqrt(Om*aa**-3 + OL); return 2.5*Om*np.sqrt(Om*a**-3 + OL)*np.trapz(1/(aa*E)**3, aa)
om_h2 = Om*h**2; ob_h2 = Ob*h**2; s_eh = 44.5*math.log(9.83/om_h2)/math.sqrt(1 + 10*ob_h2**0.75); aG = 1 - 0.328*math.log(431*om_h2)*Ob/Om + 0.38*math.log(22.3*om_h2)*(Ob/Om)**2
def T_eh(kh):
    Gam = Om*h*(aG + (1 - aG)/(1 + (0.43*kh*h*s_eh)**4)); q = kh/Gam; L = np.log(2*math.e + 1.8*q); C = 14.2 + 731/(1 + 62.5*q); return L/(L + C*q**2)
def Delta2_lcdm(kh, A): return A*kh**(ns + 3)*T_eh(kh)**2
def sigma8_of(kh, D2):
    x = kh*8.0; W = 3*(np.sin(x) - x*np.cos(x))/x**3; return math.sqrt(np.trapz(D2*W**2/kh, kh))
KH = np.geomspace(0.005, 5.0, 300); A_norm = (sig8_target/sigma8_of(KH, Delta2_lcdm(KH, 1.0)))**2
def T_fdm(kh, m):
    m22 = m/1e-22; kJeq = 9.0*math.sqrt(m22); x = 1.61*m22**(1/18)*(kh*h)/kJeq; return np.cos(x**3)/(1 + x**8)
YT = np.logspace(-6, 3, 4000); YN = YT*(1 - np.exp(-YT))
def nu_of(y): yt = np.interp(y, YN, YT); return np.where(yt <= 1, yt/np.maximum(y, 1e-300), 1 + (1/math.e)/np.maximum(y, 1e-300))
def grow(kh, delta_i, K2abs, a0, a_end=1.0, ai=1/51, boost=True):
    kk = kh*h/Mpc; cstar = math.sqrt(0.42/K2abs)*c
    def rhs(lna, y):
        a = math.exp(lna); d, dp = y; B = 0.0
        if boost:
            gN = 4*math.pi*G*Om*rho_c/a**3*abs(d)*a/kk; ycar = gN/a0; nusat = float(nu_of(np.array([ycar]))[0]) - 1
            B = min(0.9*(cstar*kk/a*t_a(a))**2, nusat)
        Oma = Om*a**-3/(Om*a**-3 + OL)
        return [dp, -(2 + dlnH_dlna(a))*dp + 1.5*Oma*(1 + B)*d]
    sol = solve_ivp(rhs, [math.log(ai), math.log(a_end)], [delta_i, delta_i], method='LSODA', rtol=1e-7, atol=1e-30, max_step=0.02)
    return sol.y[0, -1]
# ---------------- W4/W5: sigma_8 and the forest ----------------
KGRID = np.geomspace(0.01, 6.0, 44); DLi = D_lcdm(1.0)/D_lcdm(1/51); DLz3 = D_lcdm(0.25)/D_lcdm(1/51)
for m in (3e-25, 1e-24, 3e-24):
    Ti = T_fdm(KGRID, m); khm = KGRID[np.argmin(np.abs(Ti**2 - 0.5))]
    print(f"    W4: m = {m:.0e} eV: half-mode k = {khm:.2f} h/Mpc; T^2 at k = 0.2, 0.5, 1, 2, 5 h/Mpc = {[round(float(np.interp(kk, KGRID, Ti**2)), 3) for kk in (0.2, 0.5, 1, 2, 5)]}", flush=True)
S8 = {}; FOREST = {}
for foot, a0 in A0.items():
    for m in (3e-25, 1e-24, 3e-24):
        Ti = T_fdm(KGRID, m); D2_L = Delta2_lcdm(KGRID, A_norm); Delta_i = np.sqrt(D2_L)*Ti/DLi
        s8_off = sigma8_of(KGRID, D2_L*Ti**2)
        for K2abs in (1e5, 2.5e5, 1e6):
            t1 = time.time()
            R0 = np.array([(grow(kh, di, K2abs, a0)/(di*DLi))**2*Ti[j]**2 for j, (kh, di) in enumerate(zip(KGRID, Delta_i))])
            s8 = sigma8_of(KGRID, D2_L*R0); S8[(foot, m, K2abs)] = s8
            Rz3 = {kk: float((grow(kk, float(np.interp(kk, KGRID, Delta_i)), K2abs, a0, a_end=0.25)/(float(np.interp(kk, KGRID, Delta_i))*DLz3))**2*float(np.interp(kk, KGRID, Ti))**2) for kk in (1.0, 2.0, 5.0)}
            FOREST[(foot, m, K2abs)] = Rz3
            print(f"    {foot}, m = {m:.0e} eV, |K2| = {K2abs:.1e} ({time.time()-t1:.0f}s): sigma_8 = {s8:.3f} (boost off {s8_off:.3f}); z = 3 power ratio at k = 1, 2, 5 h/Mpc = {json.dumps({str(kk): round(v, 3) for kk, v in Rz3.items()})}", flush=True)
check("W4 [sigma_8] some |K2| brings sigma_8 within 20% of 0.81 for m = 3e-25, 1e-24 or 3e-24 eV (canonical footing)", any(abs(v/sig8_target - 1) < 0.2 for key, v in S8.items() if key[0] == "canonical"), json.dumps({f"{key[1]:.0e}/{key[2]:.0e}": round(v, 3) for key, v in S8.items() if key[0] == "canonical"}))
check("W5 [forest] for the same |K2| the z = 3 power at k = 1 and 2 h/Mpc is within a factor 1.5 of LambdaCDM's (canonical footing)", any(abs(v/sig8_target - 1) < 0.2 and all(1/1.5 < FOREST[key][kk] < 1.5 for kk in (1.0, 2.0)) for key, v in S8.items() if key[0] == "canonical"), json.dumps({f"{key[1]:.0e}/{key[2]:.0e}": {str(kk): round(x, 3) for kk, x in FOREST[key].items()} for key in FOREST if key[0] == "canonical"}))
print(f"\n  caveats: the steady scattering state of a coherent sea in a fixed well is a proxy for capture efficiency (a like-for-like wave/classical ratio applied to g04i's cold-infall mass); the FDM transfer function is the Hu-Barkana-Gruzinov fit; the forest gate is a linear-theory proxy at z = 3 with a generous factor 1.5.  total {time.time()-T0:.0f}s")
print(f"\nRESULT: {len(FAILS)} FAIL" + (f" -> {FAILS}" if FAILS else "")); sys.exit(0)
