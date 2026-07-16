#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
KILL-SWITCH MOCK -- oriented halo-shape lensing EFE test, the m=1 DIPOLE channel.
================================================================================

QUESTION THIS SCRIPT DECIDES (GO / NO-GO / MARGINAL):
With a realistic LOW-Z lens stack (N ~ 1e4..1e5 lenses at z=0.03-0.07, KiDS-like
sources n_eff=6.2/arcmin^2, sigma_e=0.27, per-lens g_ext directions known to
~10-50 deg cones), is the MOND/QUMOND phantom-halo m=1 dipole recoverable at
>~2-3 sigma AFTER marginalizing (i) the attractor's own shear (residual 20-50%
after imperfect subtraction), (ii) the LCDM-like infall/filament m=1 TOWARD the
attractor, and (iii) same-sign IA m=2 -- or is it buried?

PHYSICS SOURCES (verified full texts):
 * Oria et al. 2021 ApJ 923,68 (QUMOND phantom dark matter, Local Volume):
     - QUMOND: rho_PDM = (1/4piG) div[ (nu(|grad PhiN|/a0)-1) grad PhiN ]  (their Eq 6)
     - nu(y) = sqrt(1/4 + 1/y) + 1/2                                       (their Eq 4)
     - isolated point mass: M_PDM(<r) = M*(nu(gN/a0)-1)                    (their Eq 10)
     - computed lensing amplitudes (z_l=0.3, z_s=5):
         NGC5055-like, Mb=5.48e10 Msun, gNe=2.7e-3 a0  ->  kappa_min ~ -1e-3
         extreme,      Mb=5e10 Msun,   gNe=0.02  a0    ->  kappa_min ~ -3e-3
       negative zones PERPENDICULAR to g_ext, near where g_int ~ g_ext.
 * Bilek 2024 A&A 690, A364: far-field phantom is a BICONE along g_ext,
     rho_ph ~ r^-3 (3 z^2/r^2 - 1) beyond r_ef = sqrt(G M a0)/g_e; and an m=1
     asymmetry of the apparent halo along the g_ext axis (their Sec 5.2).
 * KiDS-1000 (Giblin+ 2021): n_eff = 6.2 /arcmin^2, sigma_e ~ 0.27/component.
 * Chae+ 2020/2021: external Newtonian field strengths e_N = gNe/a0 ~ 0.002-0.03
     for SPARC-like field spirals (published amplitudes; directions from 2M++).
 * Direction cones: banked table prep_2026/aligned_firing/direction_cones.csv
     (per-galaxy MC cone68); task-specified stats robust ~10-15 deg, soft
     ~30-50 deg, mix 55/45 used as PRIMARY (pessimistic), banked CSV bootstrap
     as the optimistic variant.

KEY ANALYTIC STEP (exact, no grid Poisson solve needed):
 For a point mass M in a UNIFORM external Newtonian field gNe zhat, both fields
 are divergence-free away from sources, so Oria Eq 6 collapses to the CLOSED FORM
     rho_ph(s,theta) = -(1/4piG) * nu'(y) * [grad y . g]                  (exact)
 with y=|g|/a0,  g = gNe zhat - (GM/s^2) shat,
     grad y . g = [(-4 gi^2 + 4 gNe gi c)(gNe c - gi) - 2 gNe^2 gi (1-c^2)]
                  / (2 |g| a0 s),        gi = GM/s^2,  c = cos(theta).
 Checks built in: (a) isolated limit reproduces Oria Eq 10 exactly;
 (b) far field reproduces the Bilek bicone  -nu'(ye) ye (M/4pi) (3c^2-1)/s^3
     (positive bicone along g_ext, negative torus perpendicular);
 (c) full projected kappa reproduces Oria's computed -1e-3 / -3e-3 amplitudes.
 The m=1 (odd-in-c) structure comes out of the SAME closed form -- nothing is
 injected by hand; the mock can fail.

PRE-REGISTERED VERDICT THRESHOLDS (set before any survey run):
 GO      : survey-overlap-capped median S/N(A_M) >= 3 at N <= 3e4, AND sign of
           the recovered MOND template correct in >= 95% of realizations, AND
           LCDM-universe false-positive rate (|A_M|>2sigma) <= 10%.
 MARGINAL: capped S/N >= 2 at N = 1e5 (or >=3 only at 1e5 / only uncapped).
 NO-GO   : otherwise (dipole buried).

BOTH a0 FOOTINGS run everywhere a0 enters (r_ef ~ sqrt(a0)/g_e, template
amplitude ~ a0 at fixed e_N):  canonical 9.36e-11 (cH_Lambda/Z) and alt 1.13e-10.
(Template calibration against Oria's numbers uses THEIR a0 = 1.2e-10.)

Outputs: dipole_mock_results.json, template cache dipole_templates.npz, stdout
tables. Exit 0 on success (verdict may be NO-GO -- that is a valid outcome).
"""
import numpy as np, json, os, sys, time, zlib
def stable_seed(tag): return zlib.crc32(tag.encode()) % 2**32

T0 = time.time()
HERE = os.path.dirname(os.path.abspath(__file__))
QUICK = os.environ.get("QUICK", "0") == "1"
rng_master = np.random.default_rng(20260716)

# ----------------------------------------------------------------------------
# constants / units (SI)
# ----------------------------------------------------------------------------
G     = 6.674e-11
c_l   = 2.998e8
Msun  = 1.989e30
Mpc   = 3.0857e22
kpc   = 3.0857e19
pc    = 3.0857e16
arcmin= (np.pi/180.0)/60.0
Msun_pc2 = Msun/pc**2          # = 2.089e-3 kg/m^2

H0 = 70.0*1e3/Mpc; Om, OL = 0.3, 0.7

A0_ORIA  = 1.2e-10             # Oria+21 adopted value (their Sec 2.1)
A0_CANON = 9.36e-11            # framework canonical  (cH_Lambda/Z)
A0_ALT   = 1.13e-10            # framework alt footing (rho_total/cH0)

SIG_E = 0.27                   # KiDS-1000 per-component shape noise (Giblin+21)
NEFF  = 6.2                    # KiDS-1000 n_eff / arcmin^2
ZSRC  = 0.7                    # effective single source plane for low-z lenses

# ----------------------------------------------------------------------------
# cosmology
# ----------------------------------------------------------------------------
def Ez(z): return np.sqrt(Om*(1+z)**3 + OL)
_zg = np.linspace(0, 6, 3001)
_dcg = np.concatenate([[0], np.cumsum((c_l/H0)*0.5*(1/Ez(_zg[1:])+1/Ez(_zg[:-1]))*np.diff(_zg))])
def Dc(z):  return np.interp(z, _zg, _dcg)                 # comoving, m
def Da(z):  return Dc(z)/(1+z)                             # angular diameter, m
def Da12(z1, z2): return (Dc(z2)-Dc(z1))/(1+z2)            # flat universe
def Sigma_cr(zl, zs):
    return c_l**2/(4*np.pi*G) * Da(zs)/(Da(zl)*Da12(zl, zs))   # kg/m^2

# ----------------------------------------------------------------------------
# QUMOND closed-form phantom density (point mass + uniform external field)
# ----------------------------------------------------------------------------
def nu_f(y):   return np.sqrt(0.25 + 1.0/y) + 0.5          # Oria Eq 4
def nup_f(y):  return -1.0/(2.0*y**2*np.sqrt(0.25 + 1.0/y))

def rho_ph(s, cth, M, gNe, a0):
    """Exact QUMOND phantom density [kg/m^3]; theta measured from g_ext axis
    (theta=0 points TOWARD the attractor).  s in m."""
    gi   = G*M/s**2
    sth2 = np.clip(1.0 - cth**2, 0.0, 1.0)
    g2   = gNe**2 + gi**2 - 2.0*gNe*gi*cth
    gmag = np.sqrt(np.maximum(g2, (1e-8*a0)**2))           # floor at null point
    y    = gmag/a0
    graddot = ((-4.0*gi**2 + 4.0*gNe*gi*cth)*(gNe*cth - gi)
               - 2.0*gNe**2*gi*sth2) / (2.0*gmag*a0*s)
    return -nup_f(y)/(4.0*np.pi*G)*graddot

def r_ef(M, gNe, a0):
    """EFE radius r_ef = sqrt(G M a0)/g_e with g_e the MOND-level external
    field g_e = nu(e_N) * gNe  (Bilek 2024 convention)."""
    ge = nu_f(gNe/a0)*gNe
    return np.sqrt(G*M*a0)/ge

# ---- validation (a): isolated monopole vs Oria Eq 10 -----------------------
def validate_isolated(a0=A0_ORIA):
    M = 5e10*Msun; gNe = 1e-6*a0                            # essentially isolated
    s = np.geomspace(0.03, 60.0, 4000)*np.sqrt(G*M/a0)      # in r_M units
    cgrid = np.linspace(-1, 1, 401)
    S, C = np.meshgrid(s, cgrid, indexing='ij')
    rho = rho_ph(S, C, M, gNe, a0)
    dM  = 2*np.pi*s**2*np.trapz(rho, cgrid, axis=1)         # dM/ds
    Mph = np.concatenate([[0], np.cumsum(0.5*(dM[1:]+dM[:-1])*np.diff(s))])
    y_end = (G*M/s[-1]**2)/a0
    Mph_analytic = M*(nu_f(y_end)-1.0)
    err = abs(Mph[-1]-Mph_analytic)/Mph_analytic
    return err

# ---- validation (b): far-field bicone coefficient --------------------------
def validate_farfield(a0=A0_ORIA):
    M = 5e10*Msun; gNe = 0.01*a0
    ref = r_ef(M, gNe, a0); s = 40.0*ref
    cth = np.linspace(-0.99, 0.99, 199)
    num = rho_ph(np.full_like(cth, s), cth, M, gNe, a0)
    ye  = gNe/a0
    ana = -nup_f(ye)*ye*(M/(4*np.pi))*(3*cth**2 - 1.0)/s**3
    # compare quadrupole coefficient via projection onto P2
    P2 = 0.5*(3*cth**2-1)
    cn = np.trapz(num*P2, cth)/np.trapz(P2*P2, cth)
    ca = np.trapz(ana*P2, cth)/np.trapz(P2*P2, cth)
    return abs(cn/ca - 1.0)

# ----------------------------------------------------------------------------
# projected surface density + shear templates
# ----------------------------------------------------------------------------
# Template scaling (checked numerically below): at fixed e_N = gNe/a0 and fixed
# inclination, Sigma(u = R/r_ef) is INDEPENDENT of M and proportional to a0.
NGRID = 384 if QUICK else 512
NPAD  = 2*NGRID
HALF  = 6.0            # box half-width in r_ef units
NY    = 200 if QUICK else 280
U_T   = np.geomspace(0.12, 3.5, 26)   # template radial nodes (R/r_ef)
NPHI  = 240

def sigma_map(M, gNe, a0, inc_deg):
    """Projected Sigma(p,q) [kg/m^2] on the sky; p = projected g_ext axis
    (+p TOWARD attractor); inc = angle of g_ext axis out of the sky plane."""
    ref = r_ef(M, gNe, a0)
    x = (np.arange(NGRID)-NGRID/2+0.5)*(2*HALF/NGRID)*ref     # p coords
    p, q = np.meshgrid(x, x, indexing='ij')
    ylos = np.concatenate([-np.geomspace(25.0, 1e-3, NY//2),
                            np.geomspace(1e-3, 25.0, NY//2)])*ref
    ci, si = np.cos(np.radians(inc_deg)), np.sin(np.radians(inc_deg))
    Sig = np.zeros_like(p)
    chunk = 32
    for i0 in range(0, NGRID, chunk):
        pp = p[i0:i0+chunk, :, None]; qq = q[i0:i0+chunk, :, None]
        yy = ylos[None, None, :]
        s  = np.sqrt(pp**2 + qq**2 + yy**2)
        s  = np.maximum(s, 1e-4*ref)
        cth = (pp*ci + yy*si)/s
        rho = rho_ph(s, cth, M, gNe, a0)
        Sig[i0:i0+chunk, :] = np.trapz(rho, ylos, axis=-1)
    return Sig, ref, x

def kappa_to_gamma(Sig):
    """Kaiser-Squires: Sigma map -> complex 'Sigma-shear' map (same units)."""
    n = Sig.shape[0]
    big = np.zeros((NPAD, NPAD)); o = (NPAD-n)//2
    big[o:o+n, o:o+n] = Sig
    k = np.fft.fftfreq(NPAD)
    k1, k2 = np.meshgrid(k, k, indexing='ij')
    k2s = k1**2 + k2**2; k2s[0, 0] = 1.0
    D = ((k1**2 - k2**2) + 2j*k1*k2)/k2s
    g = np.fft.ifft2(D*np.fft.fft2(big))
    return g[o:o+n, o:o+n]

def moments_from_maps(Sig, gmap, ref, x):
    """Azimuthal moments of Sigma (kappa-side) and tangential Sigma-shear at
    radii U_T*r_ef.  a_m = (1/pi) int gamma_t cos(m phi) dphi, phi=0 TOWARD."""
    phi = np.linspace(0, 2*np.pi, NPHI, endpoint=False)
    out = {}
    interp_re = _bilinear(x, np.real(gmap)); interp_im = _bilinear(x, np.imag(gmap))
    interp_S  = _bilinear(x, Sig)
    S0 = np.zeros(len(U_T)); S1 = np.zeros(len(U_T)); S2 = np.zeros(len(U_T))
    K0 = np.zeros(len(U_T)); K1 = np.zeros(len(U_T)); K2 = np.zeros(len(U_T))
    for j, u in enumerate(U_T):
        px = u*ref*np.cos(phi); py = u*ref*np.sin(phi)
        g1 = interp_re(px, py); g2 = interp_im(px, py); Sg = interp_S(px, py)
        gt = -(g1*np.cos(2*phi) + g2*np.sin(2*phi))
        S0[j] = gt.mean()
        S1[j] = 2.0*np.mean(gt*np.cos(phi))
        S2[j] = 2.0*np.mean(gt*np.cos(2*phi))
        K0[j] = Sg.mean()
        K1[j] = 2.0*np.mean(Sg*np.cos(phi))
        K2[j] = 2.0*np.mean(Sg*np.cos(2*phi))
    out.update(S0=S0, S1=S1, S2=S2, K0=K0, K1=K1, K2=K2)
    return out

def _bilinear(x, Z):
    n = len(x); x0, dx = x[0], x[1]-x[0]
    def f(px, py):
        fi = np.clip((px-x0)/dx, 0, n-1.001)
        fj = np.clip((py-x0)/dx, 0, n-1.001)
        i = fi.astype(int); j = fj.astype(int)
        wi = fi-i; wj = fj-j
        return (Z[i, j]*(1-wi)*(1-wj) + Z[i+1, j]*wi*(1-wj)
                + Z[i, j+1]*(1-wi)*wj + Z[i+1, j+1]*wi*wj)
    return f

def validate_fft_pointmass():
    """gamma_t of a compact mass must equal Mbar(<R)/(pi R^2) (Sigma units)."""
    n = NGRID; L = 1.0
    x = (np.arange(n)-n/2+0.5)*(2*L/n)
    p, q = np.meshgrid(x, x, indexing='ij')
    sig0 = 0.02
    Sig = np.exp(-(p**2+q**2)/(2*sig0**2)); Sig /= Sig.sum()*(2*L/n)**2  # unit mass
    g = kappa_to_gamma(Sig)
    R = 0.35
    phi = np.linspace(0, 2*np.pi, 720, endpoint=False)
    f1 = _bilinear(x, np.real(g)); f2 = _bilinear(x, np.imag(g))
    gt = -(f1(R*np.cos(phi), R*np.sin(phi))*np.cos(2*phi)
           + f2(R*np.cos(phi), R*np.sin(phi))*np.sin(2*phi))
    return abs(gt.mean()/(1.0/(np.pi*R**2)) - 1.0)

# ----------------------------------------------------------------------------
# stage 1: validations + Oria amplitude calibration check
# ----------------------------------------------------------------------------
print("="*78)
print("STAGE 1 -- closed-form + machinery validations")
print("="*78)
e_iso = validate_isolated();  print(f"[VAL a] isolated monopole vs Oria Eq10 : rel err = {e_iso:.3e}")
assert e_iso < 0.02, "isolated monopole check failed"
e_far = validate_farfield();  print(f"[VAL b] far-field bicone coefficient   : rel err = {e_far:.3e}")
assert e_far < 0.05, "far-field bicone check failed"
e_fft = validate_fft_pointmass(); print(f"[VAL c] FFT shear vs point-mass law    : rel err = {e_fft:.3e}")
assert e_fft < 0.03, "FFT machinery check failed"

def oria_kappa_check(Mb_msun, eN, zl=0.3, zs=5.0, a0=A0_ORIA, inc=0.0):
    Sig, ref, x = sigma_map(Mb_msun*Msun, eN*a0, a0, inc)
    scr = Sigma_cr(zl, zs)
    kmin = Sig.min()/scr
    return kmin, ref/kpc, scr

k1, ref1, scr_oria = oria_kappa_check(5.48e10, 2.7e-3)
k2, ref2, _        = oria_kappa_check(5.0e10, 0.02)
print(f"[VAL d] Oria NGC5055 config: kappa_min = {k1:+.3e} (paper ~ -1e-3), "
      f"r_ef = {ref1:.0f} kpc (paper feature ~178 kpc), Sigma_cr={scr_oria:.2f} kg/m^2")
print(f"[VAL e] Oria extreme  config: kappa_min = {k2:+.3e} (paper ~ -3e-3)")
assert -3.5e-3 < k1 < -0.35e-3, "Oria NGC5055 kappa amplitude off by >3x"
assert -1.0e-2 < k2 < -1.0e-3,  "Oria extreme kappa amplitude off by >3x"
print(f"[VAL f] ratio extreme/5055 = {k2/k1:.2f} (paper ~3)")

# amplitude-scaling check: Sigma(u) indep of M, prop to a0, at fixed e_N
def scaling_check():
    out = []
    for (M, a0) in [(5e10*Msun, A0_ORIA), (1e10*Msun, A0_ORIA), (5e10*Msun, A0_CANON)]:
        Sig, ref, x = sigma_map(M, 0.008*a0, a0, 0.0)
        g = kappa_to_gamma(Sig)
        mom = moments_from_maps(Sig, g, ref, x)
        out.append(mom['S2']/a0)
    eM  = np.max(np.abs(out[1]/out[0] - 1.0)[4:20])
    eA  = np.max(np.abs(out[2]/out[0] - 1.0)[4:20])
    return eM, eA
eM, eA = scaling_check()
print(f"[VAL g] template M-independence: max rel dev = {eM:.3e}; a0-scaling: {eA:.3e}")
assert eM < 0.05 and eA < 0.05, "template scaling assumption violated"

# ----------------------------------------------------------------------------
# stage 2: template tables S_m(u; e_N, inc)  [Sigma units, per a0_ref]
# ----------------------------------------------------------------------------
print("="*78)
print("STAGE 2 -- QUMOND template tables (this is the injected MOND signal)")
print("="*78)
EN_NODES  = np.array([0.002, 0.004, 0.008, 0.016, 0.032])
INC_NODES = np.array([0.0, 40.0, 65.0, 85.0])
A0_REF    = A0_ORIA
CACHE = os.path.join(HERE, "dipole_templates.npz")
key = f"{NGRID}_{NY}_{len(U_T)}"
if os.path.exists(CACHE) and np.load(CACHE, allow_pickle=True)['key'].item() == key:
    z = np.load(CACHE, allow_pickle=True)
    T_S1, T_S2, T_K1, T_K2, T_S0 = z['S1'], z['S2'], z['K1'], z['K2'], z['S0']
    print("[cache] loaded", CACHE)
else:
    T_S1 = np.zeros((len(EN_NODES), len(INC_NODES), len(U_T)))
    T_S2 = np.zeros_like(T_S1); T_K1 = np.zeros_like(T_S1)
    T_K2 = np.zeros_like(T_S1); T_S0 = np.zeros_like(T_S1)
    for a, eN in enumerate(EN_NODES):
        for b, inc in enumerate(INC_NODES):
            Sig, ref, x = sigma_map(5e10*Msun, eN*A0_REF, A0_REF, inc)
            g = kappa_to_gamma(Sig)
            mom = moments_from_maps(Sig, g, ref, x)
            T_S1[a, b] = mom['S1']; T_S2[a, b] = mom['S2']
            T_K1[a, b] = mom['K1']; T_K2[a, b] = mom['K2']; T_S0[a, b] = mom['S0']
            print(f"  template e_N={eN:.3f} inc={inc:>4.0f}d  "
                  f"S1[u~1]={T_S1[a,b,np.argmin(abs(U_T-1))]:+.3e}  "
                  f"S2[u~1]={T_S2[a,b,np.argmin(abs(U_T-1))]:+.3e}  ({time.time()-T0:.0f}s)")
    np.savez(CACHE, S1=T_S1, S2=T_S2, K1=T_K1, K2=T_K2, S0=T_S0, key=key,
             U=U_T, EN=EN_NODES, INC=INC_NODES)
    print("[cache] saved", CACHE)

# report the template structure at the central node
ia, ib = 2, 0
print("\nQUMOND template at e_N=0.008, axis in sky plane (Sigma units, kg/m^2):")
print("   u=R/r_ef   K1(Sigma dip)  K2(Sigma quad)  S1(gt dip)   S2(gt quad)")
for j in range(0, len(U_T), 3):
    print(f"   {U_T[j]:7.3f}   {T_K1[ia,ib,j]:+.3e}   {T_K2[ia,ib,j]:+.3e}"
          f"   {T_S1[ia,ib,j]:+.3e}   {T_S2[ia,ib,j]:+.3e}")
sgn_note = "AWAY from attractor" if np.trapz(T_K1[ia, ib]*U_T, U_T) < 0 else "TOWARD attractor"
print(f"Projected-Sigma dipole moment integral says apparent excess is {sgn_note}")
print("(Bilek 2024 sec 5.2 full-solver claim: shifted AWAY -- see verdict notes.)")

def interp_template(T, eN, inc, u):
    """T[eN, inc, u] trilinear (log eN, lin inc, log u); vector over lenses/bins."""
    le = np.clip(np.log(eN), np.log(EN_NODES[0]), np.log(EN_NODES[-1]))
    ic = np.clip(inc, INC_NODES[0], INC_NODES[-1])
    lu = np.clip(np.log(u), np.log(U_T[0]), np.log(U_T[-1]))
    ie = np.clip(np.searchsorted(np.log(EN_NODES), le)-1, 0, len(EN_NODES)-2)
    ii = np.clip(np.searchsorted(INC_NODES, ic)-1, 0, len(INC_NODES)-2)
    iu = np.clip(np.searchsorted(np.log(U_T), lu)-1, 0, len(U_T)-2)
    we = (le-np.log(EN_NODES)[ie])/(np.log(EN_NODES)[ie+1]-np.log(EN_NODES)[ie])
    wi = (ic-INC_NODES[ii])/(INC_NODES[ii+1]-INC_NODES[ii])
    wu = (lu-np.log(U_T)[iu])/(np.log(U_T)[iu+1]-np.log(U_T)[iu])
    v = 0.0
    for de, ee in [(0, 1-we), (1, we)]:
        for di, ww in [(0, 1-wi), (1, wi)]:
            for du, uu in [(0, 1-wu), (1, wu)]:
                v = v + ee*ww*uu*T[ie+de, ii+di, iu+du]
    return v

# ----------------------------------------------------------------------------
# stage 3: attractor point-shear moments about the lens center (numeric)
# ----------------------------------------------------------------------------
# A distant point attractor: kappa=0 at the lens => spin-1 flexion F ~ grad(kappa)=0.
# So its shear field contributes m=2 (uniform shear, ~const in R) and m=3, but
# NO m=1 at leading order.  Verify numerically:
def attractor_moments():
    Dd = 1.0                      # attractor distance (units arbitrary)
    K  = 1.0                      # gamma at lens = K/Dd^2
    r  = 0.02*Dd                  # aperture radius scale
    phi = np.linspace(0, 2*np.pi, 4000, endpoint=False)
    zpt = r*np.exp(1j*phi)
    gam = -K/np.conj(zpt-Dd)**2   # point-mass complex shear, mass at +Dd
    gt  = -np.real(gam*np.exp(-2j*phi))
    a1 = 2*np.mean(gt*np.cos(phi)); a2 = 2*np.mean(gt*np.cos(2*phi))
    a3 = 2*np.mean(gt*np.cos(3*phi))
    return a1/(K/Dd**2), a2/(K/Dd**2), a3/(K/Dd**2), (r/Dd)
am1, am2, am3, rr = attractor_moments()
print(f"\n[VAL h] point-attractor gt moments at r/D={rr}: m=1: {am1:+.4f}*gamma_att "
      f"(=0 expected), m=2: {am2:+.4f}*gamma_att, m=3: {am3:+.4f}*gamma_att")
assert abs(am1) < 0.05, "unexpected m=1 from pure external point shear"
# => the attractor m=1 comes only from its EXTENDED halo's Sigma gradient across
# the aperture (isothermal-like: Sigma_att ~ g_e/(2G) at the lens, gradient ~ /D).

# ----------------------------------------------------------------------------
# stage 4: survey mock
# ----------------------------------------------------------------------------
print("="*78)
print("STAGE 4 -- survey-level mock (KiDS-like noise; overlap-capped)")
print("="*78)

U_EDGES = np.geomspace(0.15, 3.0, 13)
U_MID   = np.sqrt(U_EDGES[1:]*U_EDGES[:-1])
NBIN    = len(U_MID)

SURVEY_AREA = {10000: 1350.0, 30000: 4143.0, 100000: 18000.0}   # deg^2 KiDS/DES/LSST
INFALL_SIG0 = 0.4      # Msun/pc^2 dipole at 0.5 Mpc (2-halo/filament-motivated;
                       # Epps&Hudson-17 filament Sigma ~5.5 Msun/pc^2 for LRG pairs,
                       # scaled down for 3e10 Msun field spirals; bracketed 0.1-1.0)
INFALL_SLOPE = -0.5
GT_FROM_K1   = 0.7     # O(1) conversion kappa-dipole -> gt-dipole for smooth profiles
                       # (nuisance templates only; fitted amplitudes absorb it)

# cone stats -- primary per task spec; banked CSV as optimistic variant
cone_csv = os.path.join(HERE, "direction_cones.csv")
if not os.path.exists(cone_csv):
    src = "/Users/carlzimmerman/new_physics/prep_2026/aligned_firing/direction_cones.csv"
    if os.path.exists(src):
        import shutil; shutil.copy(src, cone_csv)
BANKED_R, BANKED_S = None, None
if os.path.exists(cone_csv):
    import csv
    rr_, ss_ = [], []
    with open(cone_csv) as f:
        for row in csv.DictReader(f):
            (rr_ if row['flag'] == 'robust' else ss_).append(float(row['cone68_deg']))
    BANKED_R, BANKED_S = np.array(rr_), np.array(ss_)

def draw_lenses(N, a0, rng, cone_mode="spec"):
    d = {}
    d['M']    = np.clip(10**(rng.normal(np.log10(3e10), 0.30, N)), 1e10, 1e11)*Msun
    zl        = (rng.uniform(0.03**3, 0.07**3, N))**(1/3)          # dV ~ z^2
    d['zl']   = zl
    d['gNe']  = np.clip(10**(rng.normal(np.log10(6e-13), 0.30, N)), 0.002*a0, 0.03*a0)
    d['eN']   = d['gNe']/a0
    d['ge']   = nu_f(d['eN'])*d['gNe']                              # MOND ext field
    d['ref']  = np.sqrt(G*d['M']*a0)/d['ge']
    d['inc']  = np.degrees(np.arcsin(rng.uniform(0, 1, N)))         # axis isotropic
    rob       = rng.uniform(0, 1, N) < 0.55
    if cone_mode == "banked" and BANKED_R is not None:
        cone = np.where(rob, rng.choice(BANKED_R, N), rng.choice(BANKED_S, N))
    elif cone_mode == "perfect":
        cone = np.zeros(N)
    else:
        cone = np.where(rob, rng.uniform(10, 15, N), rng.uniform(30, 50, N))
    d['dphi'] = rng.normal(0, np.radians(cone))                     # PA error
    d['Datt'] = rng.uniform(8, 25, N)*Mpc
    d['eps']  = rng.uniform(0.2, 0.5, N)                            # subtraction residual
    d['geom'] = rng.uniform(0.5, 2.0, N)                            # attractor geometry O(1)
    d['scr']  = Sigma_cr(zl, ZSRC)
    d['Da']   = Da(zl)
    return d

def per_lens_matrices(d, a0, neff=NEFF):
    """signal & nuisance templates and noise, shape (N, NBIN)."""
    N = len(d['M'])
    eN  = np.repeat(d['eN'], NBIN); inc = np.repeat(d['inc'], NBIN)
    u   = np.tile(U_MID, N)
    S1  = interp_template(T_S1, eN, inc, u).reshape(N, NBIN)*(a0/A0_REF)
    S2  = interp_template(T_S2, eN, inc, u).reshape(N, NBIN)*(a0/A0_REF)
    scr = d['scr'][:, None]
    t_M   = S1/scr                                          # MOND gt dipole template
    t_Q   = S2/scr                                          # MOND gt quadrupole
    R     = U_MID[None, :]*d['ref'][:, None]                # physical radius, m
    # infall/filament dipole TOWARD attractor (positive cos(phi) moment):
    t_inf = GT_FROM_K1*(INFALL_SIG0*Msun_pc2)*(R/(0.5*Mpc))**INFALL_SLOPE/scr
    # attractor extended-halo Sigma gradient (isothermal: Sigma ~ g_e/2G at lens):
    t_grd = 0.5*(d['ge'][:, None]/(2*G*scr))*(R/d['Datt'][:, None])
    # IA halo-ellipticity m=2 (LCDM confound; f_h=0.2 on SIS DeltaSigma from BTFR v):
    v2    = np.sqrt(G*d['M']*a0)                            # v_flat^2 (BTFR)
    dsis  = v2[:, None]/(4*G*R)
    t_IA  = 0.2*dsis/scr
    # attractor uniform shear (m=2, const in R):
    g_att = (d['ge']*d['geom']/(np.pi*G*d['scr']))[:, None]*np.ones((1, NBIN))
    # noise per moment bin:
    th_ref = d['ref']/d['Da']/arcmin                        # r_ef in arcmin
    area   = np.pi*(U_EDGES[1:]**2-U_EDGES[:-1]**2)[None, :]*th_ref[:, None]**2
    nsrc   = neff*area
    sig    = np.sqrt(2.0)*SIG_E/np.sqrt(np.maximum(nsrc, 1e-9))
    sig[nsrc < 3.0] = np.inf                                # unusable bins
    return t_M, t_Q, t_inf, t_grd, t_IA, g_att, sig, th_ref

def gls(X, dvec, w):
    XW = X*w[:, None]
    A  = XW.T@X; b = XW.T@dvec
    Ai = np.linalg.inv(A)
    return Ai@b, Ai

def run_config(N, a0, universe, rng, cone_mode="spec", infall_scale=1.0,
               mond_on=None, nreal=40, tscale=1.0, neff=NEFF):
    if mond_on is None: mond_on = (universe == "MOND")
    A_Ms, S_Ns, signs, A_infs, A2s, S2Ns, S_As = [], [], [], [], [], [], []
    fov = None
    for it in range(nreal):
        d = draw_lenses(N, a0, rng, cone_mode)
        t_M, t_Q, t_inf, t_grd, t_IA, g_att, sig, th_ref = per_lens_matrices(d, a0, neff)
        c1 = np.cos(d['dphi'])[:, None]; c2 = np.cos(2*d['dphi'])[:, None]
        # ---- m=1 data ----
        d1 = np.zeros_like(t_M)
        if mond_on: d1 += tscale*t_M*c1
        d1 += infall_scale*t_inf*c1                       # toward (both universes)
        d1 += t_grd*d['eps'][:, None]*c1                  # residual after subtraction
        d1 += rng.normal(0, 1, d1.shape)*np.where(np.isfinite(sig), sig, 0)
        # ---- m=2 data ----
        d2 = np.zeros_like(t_M)
        d2 += (tscale*t_Q*c2 if mond_on else t_IA*c2)     # same-sign confusion pair
        d2 += g_att*d['eps'][:, None]                     # residual uniform shear
        d2 += rng.normal(0, 1, d2.shape)*np.where(np.isfinite(sig), sig, 0)
        # ---- fits ----
        ok = np.isfinite(sig).ravel()
        w  = np.zeros(sig.size); w[ok] = 1.0/sig.ravel()[ok]**2
        X1 = np.stack([t_M.ravel(), t_inf.ravel(), t_grd.ravel()], axis=1)
        a_hat, cov = gls(X1[ok], d1.ravel()[ok], w[ok])
        A_M, sA = a_hat[0], np.sqrt(cov[0, 0])
        X2 = np.stack([t_Q.ravel(), t_IA.ravel(), np.ones(sig.size)], axis=1)
        a2_hat, cov2 = gls(X2[ok], d2.ravel()[ok], w[ok])
        A_Ms.append(A_M); S_Ns.append(A_M/sA); signs.append(A_M > 0)
        A_infs.append(a_hat[1]); A2s.append(a2_hat[0]); S_As.append(sA)
        S2Ns.append(a2_hat[0]/np.sqrt(cov2[0, 0]))
        if fov is None:
            ap_deg2 = np.pi*(3.0*th_ref)**2/3600.0         # aperture per lens, deg^2
            fov = max(1.0, float(np.sum(ap_deg2))/SURVEY_AREA[N])
    A_Ms = np.array(A_Ms); S_Ns = np.array(S_Ns)
    return dict(A_M_med=float(np.median(A_Ms)), A_M_scat=float(np.std(A_Ms)),
                SN_med=float(np.median(S_Ns)), SN_scat=float(np.std(S_Ns)),
                sign_frac=float(np.mean(signs)),
                twosig_frac=float(np.mean(np.array(S_Ns) > 2.0)),
                fp2_frac=float(np.mean(np.abs(S_Ns) > 2.0)),
                A_inf_med=float(np.median(A_infs)),
                A2_med=float(np.median(A2s)), S2N_med=float(np.median(S2Ns)),
                sigA_med=float(np.median(S_As)),
                f_ov=float(fov), SN_med_capped=float(np.median(S_Ns)/np.sqrt(fov)))

# ---- validation (i): source-level noise vs analytic Var(a_m) = 2 sig_e^2/N --
def validate_source_noise(rng=np.random.default_rng(99)):
    Nsrc, ntrial, a1_true = 200, 4000, 5e-2
    ests = np.zeros(ntrial)
    for t in range(ntrial):
        phi = rng.uniform(0, 2*np.pi, Nsrc)
        et  = a1_true*np.cos(phi) + rng.normal(0, SIG_E, Nsrc)
        ests[t] = 2.0*np.mean(et*np.cos(phi))
    bias = ests.mean()/a1_true - 1.0
    vrat = ests.var()/(2*SIG_E**2/Nsrc)
    return bias, vrat
nb, nv = validate_source_noise()
print(f"[VAL i] source-level moment estimator: bias={nb:+.3f}, "
      f"Var/(2 sig_e^2/N)={nv:.3f} (expect ~0, ~1)")
assert abs(nb) < 0.05 and abs(nv-1) < 0.1, "noise model check failed"

# mean dilution factor (report separately)
_d = draw_lenses(20000, A0_CANON, np.random.default_rng(7))
DIL_CONE = float(np.mean(np.cos(_d['dphi'])))
print(f"\nDirection-cone dilution <cos dphi> (spec mix 55/45): {DIL_CONE:.3f}")
_d2 = draw_lenses(20000, A0_CANON, np.random.default_rng(8), cone_mode="banked")
DIL_CONE_B = float(np.mean(np.cos(_d2['dphi'])))
print(f"Direction-cone dilution <cos dphi> (banked CSV)     : {DIL_CONE_B:.3f}")

NREAL = {10000: 120, 30000: 80, 100000: 40}
if QUICK: NREAL = {10000: 20, 30000: 12, 100000: 6}

results = {}
for a0, aname in [(A0_CANON, "canonical_9.36e-11"), (A0_ALT, "alt_1.13e-10")]:
    for N in [10000, 30000, 100000]:
        for uni in ["MOND", "LCDM"]:
            tag = f"{aname}|N={N}|{uni}"
            rng = np.random.default_rng(stable_seed(tag))
            r = run_config(N, a0, uni, rng, nreal=NREAL[N])
            results[tag] = r
            print(f"{tag:48s} A_M={r['A_M_med']:+.3f}+-{r['A_M_scat']:.3f} "
                  f"S/N={r['SN_med']:+.2f} capped={r['SN_med_capped']:+.2f} "
                  f"sign+={r['sign_frac']:.2f} f_ov={r['f_ov']:.2f} "
                  f"m2 S/N={r['S2N_med']:.1f}  ({time.time()-T0:.0f}s)")

# variants at N=3e4 canonical
print("\nVariants (N=3e4, canonical a0, MOND universe):")
variants = {}
ORIA_CAL = min(1.0, abs(-1e-3/k1))   # pessimistic: rescale injection to Oria's
                                     # truncated-cube kappa amplitude
for vtag, kw in [("cones_banked", dict(cone_mode="banked")),
                 ("infall_x0.25", dict(infall_scale=0.25)),
                 ("infall_x2.5",  dict(infall_scale=2.5)),
                 (f"oria_cal_x{ORIA_CAL:.2f}", dict(tscale=ORIA_CAL))]:
    rng = np.random.default_rng(stable_seed(vtag))
    r = run_config(30000, A0_CANON, "MOND", rng, nreal=40, **kw)
    variants[vtag] = r
    print(f"  {vtag:16s} A_M={r['A_M_med']:+.3f} S/N={r['SN_med']:+.2f} "
          f"capped={r['SN_med_capped']:+.2f} sign+={r['sign_frac']:.2f}")
# forward-path variants at N=1e5:
print("Variants (N=1e5, canonical a0):")
for vtag, uni, kw in [
        ("N1e5_LSST_neff27",       "MOND", dict(neff=27.0)),
        ("N1e5_LSST_neff27_LCDM",  "LCDM", dict(neff=27.0)),
        ("N1e5_LSST_neff27_oriacal","MOND", dict(neff=27.0, tscale=ORIA_CAL)),
        ("N1e5_perfect_dirs",      "MOND", dict(cone_mode="perfect"))]:
    rng = np.random.default_rng(stable_seed(vtag))
    r = run_config(100000, A0_CANON, uni, rng, nreal=30, **kw)
    variants[vtag] = r
    print(f"  {vtag:26s} A_M={r['A_M_med']:+.3f} S/N={r['SN_med']:+.2f} "
          f"capped={r['SN_med_capped']:+.2f} sign+={r['sign_frac']:.2f} "
          f"fp2={r['fp2_frac']:.2f}")
# LCDM-side infall bracket (false-positive robustness)
for vtag, kw in [("LCDM_infall_x2.5", dict(infall_scale=2.5))]:
    rng = np.random.default_rng(stable_seed(vtag))
    r = run_config(30000, A0_CANON, "LCDM", rng, nreal=40, **kw)
    variants[vtag] = r
    print(f"  {vtag:16s} A_M={r['A_M_med']:+.3f} S/N={r['SN_med']:+.2f} "
          f"fp(2sig)={r['fp2_frac']:.2f}")

# ----------------------------------------------------------------------------
# stage 5: verdict (pre-registered thresholds)
# ----------------------------------------------------------------------------
print("="*78)
print("STAGE 5 -- verdict")
print("="*78)
def get(a, N, u): return results[f"{a}|N={N}|{u}"]
# sign-separation: can a MOND-away universe be told from an LCDM-toward one?
sep = {}
for aname in ["canonical_9.36e-11", "alt_1.13e-10"]:
    for N in [10000, 30000, 100000]:
        m, l = get(aname, N, "MOND"), get(aname, N, "LCDM")
        s = (m['A_M_med'] - l['A_M_med'])/m['sigA_med']
        sep[f"{aname}|N={N}"] = float(s)
        print(f"sign-separation {aname} N={N}: (A_M^MOND - A_M^LCDM)/sigma = {s:+.2f}")
ver = {}
for aname in ["canonical_9.36e-11", "alt_1.13e-10"]:
    go = (get(aname, 30000, "MOND")['SN_med_capped'] >= 3.0 and
          get(aname, 30000, "MOND")['sign_frac'] >= 0.95 and
          get(aname, 30000, "LCDM")['fp2_frac'] <= 0.10) or \
         (get(aname, 10000, "MOND")['SN_med_capped'] >= 3.0 and
          get(aname, 10000, "MOND")['sign_frac'] >= 0.95 and
          get(aname, 10000, "LCDM")['fp2_frac'] <= 0.10)
    marg = (get(aname, 100000, "MOND")['SN_med_capped'] >= 2.0 or
            get(aname, 100000, "MOND")['SN_med'] >= 3.0 or
            get(aname, 30000, "MOND")['SN_med'] >= 3.0)
    ver[aname] = "GO" if go else ("MARGINAL" if marg else "NO-GO")
    print(f"footing {aname}: {ver[aname]}")

out = dict(results=results, variants=variants, verdict=ver, separation=sep,
           oria_calibration_factor=float(ORIA_CAL),
           dilution_cone_spec=DIL_CONE, dilution_cone_banked=DIL_CONE_B,
           oria_check=dict(k5055=float(k1), kextreme=float(k2),
                           ref5055_kpc=float(ref1)),
           validations=dict(iso=float(e_iso), far=float(e_far), fft=float(e_fft),
                            attractor_m1=float(am1)),
           settings=dict(NEFF=NEFF, SIG_E=SIG_E, ZSRC=ZSRC,
                         infall_sig0_Msunpc2=INFALL_SIG0,
                         survey_areas=SURVEY_AREA, u_edges=list(U_EDGES),
                         quick=QUICK))
with open(os.path.join(HERE, "dipole_mock_results.json"), "w") as f:
    json.dump(out, f, indent=1, default=float)
print(f"\nwrote dipole_mock_results.json   ({time.time()-T0:.0f}s total)")
print("EXIT 0")
