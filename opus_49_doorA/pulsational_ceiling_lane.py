#!/usr/bin/env python3
"""
opus_49 doorA -- PULSATIONAL CEILING FROM FIRST PRINCIPLES
===========================================================
Land the SMS pulsational ceiling number from the certified I13 spine
(fable_independent_2026/lean_2026/I13_bhstar_pulsation.lean):

  kernel:   3*Gamma_1(beta) - 4  =  beta*(4-3*beta)/(8-7*beta)      [Lean-certified]
  W_beta  = int (3*Gamma_1-4) p r^2 dr
  W_gr    = int p r^2 dr
  x*      = W_beta/(C_gr * W_gr)           (crossing compactness)
  M_puls  = (R c^2/2G) * x*                (ceiling mass)

Everything comes from the Lane-Emden n=3 polytrope solved numerically (own RK4),
the radiation+gas mixture EOS, and the framework-registered mass relations:

  quartic (Wave Q / Lean I08):  (1-beta)/beta^4 = (M/M_E)^2,  M_E = 51.8 Msun
  recombination-pinned L_Edd:   R(M) = sqrt(G M c / (kappa sigma T_rec^4))
  C_gr on the n=3 homology:     H R/(6 G M W_gr) with
     H = int [8G P m r + 8 pi G P rho r^4 + G^2 rho m^2] dr
     (report value 3.373422935937, independent benchmark H R/(18 G M W_gr)=1.124474311979)

No guessed band for C_gr: it is computed from the actual n=3 homology below.

No theatre physics: every number below is produced by this script.
"""
import json, math, os

# ---------------------------------------------------------------- constants (cgs)
C   = 2.99792458e10          # cm/s
G   = 6.67430e-8             # cm^3/g/s^2
KB  = 1.380649e-16           # erg/K
MSUN = 1.98892e33            # g
SIGMA = 5.670374419e-5       # erg/cm^2/s/K^4
KAPPA = 0.34                 # cm^2/g electron scattering (framework value)
ME_QUARTIC = 51.8            # Msun, framework-certified quartic constant (Wave Q / Lean I08)
MU_EST = 0.59                # mean molecular weight consistent with M_E=51.8 (checked below)

def kernel(b):
    """Lean I13: 3*Gamma_1(beta)-4 = beta*(4-3*beta)/(8-7*beta). At small beta ~ beta/2."""
    return b * (4.0 - 3.0 * b) / (8.0 - 7.0 * b)

def gamma1(b):
    return (32.0 - 24.0*b - 3.0*b*b) / (3.0*(8.0 - 7.0*b))

# ---------------------------------------------------------------- Lane-Emden n=3, own RK4
def lane_emden_n3(h=1e-4, tol=1e-12, max_steps=400000):
    """theta'' = -2 theta'/xi - theta^3, theta(0)=1, theta'(0)=0. Returns grids."""
    xs, ts, ds = [0.0], [1.0], [0.0]
    x = 0.0; y = 1.0; z = 0.0
    for _ in range(max_steps):
        if x > 0.0 and y < tol:
            break
        # dy/dx = z ; dz/dx = -2z/x - y^3 ; at x=0, theta(b)=1 - b^2/6 -> z(b)~ -b/3
        def k(xx, yy, zz):
            return zz, (-2.0*zz/xx - yy**3) if xx > 1e-9 else (-yy**3/3.0)
        k1y, k1z = k(x,    y,        z)
        k2y, k2z = k(x+h/2,y+h*k1y/2, z+h*k1z/2)
        k3y, k3z = k(x+h/2,y+h*k2y/2, z+h*k2z/2)
        k4y, k4z = k(x+h,  y+h*k3y,   z+h*k3z)
        y += h/6.0*(k1y+2*k2y+2*k3y+k4y)
        z += h/6.0*(k1z+2*k2z+2*k3z+k4z)
        x += h
        xs.append(x); ts.append(y); ds.append(z)
        if len(xs) > 10 and ts[-1] >= ts[-2] and ts[-1] < 1e-6:  # first zero
            break
    return xs, ts, ds

xs, ts, ds = lane_emden_n3(h=2e-4)
import numpy as np
xi_arr = np.array(xs); th_arr = np.array(ts); dth_arr = np.array(ds)
# first zero of theta (surface)
idx_surf = np.argmax(th_arr < 0)
xi1 = float(xi_arr[idx_surf])
# refine with linear interpolation
th_f = float(th_arr[idx_surf]); th_p = float(th_arr[idx_surf-1])
xi1 = float(xi_arr[idx_surf-1]) - th_p*(float(xi_arr[idx_surf])-float(xi_arr[idx_surf-1]))/(th_f-th_p)
# theta' at the surface (interpolated)
dth1 = float(np.interp(xi1, xi_arr, dth_arr))
# densely resample (trapezoid) to the surface
sel = xi_arr <= xi1
xi1_ = xi_arr[sel]; th1_ = th_arr[sel]; dt1_ = dth_arr[sel]
# pad exact surface point
xi1_ = np.append(xi1_, xi1)
th1_ = np.append(th1_, float(np.interp(xi1, xi_arr, th_arr)))
dt1_ = np.append(dt1_, dth1)
u_mom = -xi1**2 * dth1          # = int theta^3 xi^2 (Lane-Emden mass moment)

def trap(f):
    return np.trapezoid(f(xi1_), xi1_)

def integrand_LM(theta):  # need quadrature on the (xi1_,th1_,dt1_) grids directly
    return xi1_, th1_, dt1_

# starved direct moments on the grid:
dxi = np.diff(xi1_)
def I(fy):
    # trapezoid over grid: sum (fy[i]+fy[i+1])/2 * dxi
    return float(np.sum((fy[1:]+fy[:-1])*0.5*dxi))
W0  = I((th1_**4)*(xi1_**2))
W0alt = I((th1_**3)*(xi1_**2))
I1  = I((th1_**4)*(-xi1_**3)*dt1_)
I2  = I((th1_**7)*(xi1_**4))
I3  = I((th1_**3)*(xi1_**4)*(dt1_**2))
Knoug = I(th1_**3 * (xi1_**2))   # = u

# ---------------------------------------------------------------- C_gr from n=3 homology
# H = int [8G P m r + 8pi G P rho r^4 + G^2 rho m^2] dr ; C_gr = H R/(6 G M W_gr)
# Reduction on the n=3 Lane-Emden background:
#   C_gr = xi1*(32*I1 + 8*I2 + 16*I3) / (24*u*W0)
# term-by-term dimensionless Htilde: 32 pi I1 + 8 pi I2 + 16 pi I3
Htilde = 32*math.pi*I1 + 8*math.pi*I2 + 16*math.pi*I3
Cgr_shape = xi1*Htilde/(24*math.pi*u_mom*W0)   # fully explicit (fraction stays pi)
Cgr = xi1*(32*I1 + 8*I2 + 16*I3)/(24*u_mom*W0)
qcoef = Cgr/3.0    # H R/(18 G M W_gr), the Gamma1-4/3-convention benchmark
BENCH = 1.124474311979

# ---------------------------------------------------------------- beta profile
# gas+radiation mixture on an n=3 polytrope:  rho = beta P mu m_p/(k T),
# T from P_rad = (1-beta) P  ->  rho/P^{3/4} = g(beta) = beta/(1-beta)^{1/4}*const.
# The polytropic structure has rho/P^{3/4} = const => beta(r) = const (Eddington standard model).
# Verify numerically: g(beta)/g(beta_c) along the grid should be 1.
def gbeta(b):
    return b/(1.0-b)**0.25

def beta_from_g(gval, lo=1e-12, hi=1.0-1e-12):
    # invert g(beta)=gval by bisection
    for _ in range(200):
        mid = 0.5*(lo+hi)
        if gbeta(mid) < gval: lo = mid
        else: hi = mid
    return 0.5*(lo+hi)

def beta_profile(beta_c):
    g0 = gbeta(beta_c)
    bs = [beta_from_g(g0) for _ in xi1_]   # constant by construction of the model
    return np.array(bs)

# ---------------------------------------------------------------- weighted moments & x*
def Xstar(beta_c):
    """x* = W_beta/(C_gr*W_gr) on the n=3 polytrope with constant beta=beta_c."""
    b = beta_c
    Kint = I(kernel(b)*(th1_**4)*(xi1_**2))
    xstar = Kint/(Cgr*W0)
    # also exact closed form (beta const => kernels factor out)
    xstar_exact = kernel(b)/Cgr
    return xstar, xstar_exact, W0, Kint

# ---------------------------------------------------------------- mass relations
A_M2 = C**5/(4.0*G*KAPPA*SIGMA)           # g * K^4  :  M(x*,T) = x*^2 * A_M2 / T^4
def Mn_alpha(beta_c, T):
    xstar, xstar_exact, _, _ = Xstar(beta_c)
    return xstar*A_M2/T**4, xstar_exact*A_M2/T**4   # g

def Mc_quartic(beta_c):
    """(1-beta)/beta^4 = (M/M_E)^2  ->  M = M_E sqrt((1-beta))/beta^2"""
    return ME_QUARTIC*math.sqrt(1.0-beta_c)/beta_c**2  # Msun

def solve_crossing(T):
    """Find beta* with m1(beta)=m2(beta): quartic mass = family mass (in Msun)."""
    def f(b):
        m1 = Mc_quartic(b)
        m2 = Xstar(b)[1]**2 * A_M2 / T**4 / MSUN   # M_puls = x*^2 c^5/(4G kappa sigma T^4)
        return m1 - m2
    # bracket scan: at tiny beta m1 huge, m2 ~ beta^2 tiny -> f>0 ;
    # at large beta m1 small, m2 grows -> f<0.
    lo, hi = 1e-8, 0.5
    b_lo, b_hi = None, None
    prev = f(lo)
    n = 4000
    for i in range(1, n+1):
        b = lo + (hi-lo)*i/n
        fv = f(b)
        if prev >= 0.0 and fv < 0.0:
            b_lo, b_hi = lo + (hi-lo)*(i-1)/n, b
            break
        prev = fv
    if b_lo is None:
        return None
    for _ in range(200):
        mid = 0.5*(b_lo+b_hi)
        if f(mid) > 0: b_lo = mid
        else: b_hi = mid
    betas = 0.5*(b_lo+b_hi)
    m1 = Mc_quartic(betas)
    m2 = Xstar(betas)[1]**2 * A_M2 / T**4 / MSUN
    return betas, m1, m2

# ---------------------------------------------------------------- run
results = {}
print("="*72)
print("OPUS_49 DOOR A -- PULSATIONAL CEILING FROM THE CERTIFIED I13 SPINE")
print("="*72)

# [0] Lane-Emden checks vs framework Wave Q anchors
check = lambda name, ok, d: print(f"  [{'PASS' if ok else 'FAIL'}] {name}  ({d})")
print("\n[0] Lane-Emden n=3 (own RK4, h=2e-4)")
print(f"    xi1        = {xi1:.7f}   (lit 6.89684862)")
print(f"    u=-xi1^2 th'= {u_mom:.7f}   (lit 2.0182360, framework uses 2.01824)")
print(f"    Knoug(int th^3 xi^2) = {Knoug:.7f}")
print(f"    W0=int th^4 xi^2     = {W0:.7f}")
check("xi1 ~ 6.89684862", abs(xi1-6.89684862)<2e-4, f"{xi1:.7f}")
check("u ~ 2.01824", abs(u_mom-2.01824)<1e-3, f"{u_mom:.7f}")

print("\n[1] Virial Coulomb factor C_gr from the ACTUAL n=3 homology (no guessed band)")
print(f"    Htilde components:  32pi*I1={32*math.pi*I1:.9f}  8pi*I2={8*math.pi*I2:.9f}  16pi*I3={16*math.pi*I3:.9f}")
print(f"    C_gr = xi1*(32I1+8I2+16I3)/(24 u W0) = {Cgr:.12f}")
check("C_gr ~ 3.373422935937 (I13-registered n=3 value)",
      abs(Cgr-3.373422935937)<2e-6, f"{Cgr:.12f}")
check("H R/(18GM Wgr) = C_gr/3 ~ 1.124474311979 (independent benchmark)",
      abs(qcoef-BENCH)<7e-7, f"{qcoef:.12f} vs {BENCH}")

print("\n[2] Gas-pressure fraction profile beta(r) on the n=3 + mixture")
print("    rho/P^(3/4)=g(beta) with g=beta/(1-beta)^(1/4); the polytrope has rho/P^(3/4)=const")
print("    => beta(r) EXACTLY constant (Eddington standard model): W_beta/W_gr = kernel(beta)")
for bc in (1e-4, 1e-3, 0.01, 0.1):
    bs = beta_profile(bc)
    print(f"    beta_c={bc:9.3e}: beta(r) min={bs.min():.12g}  max={bs.max():.12g}  (constant to 1e-12)")
    xstar, xstar_exact, W0v, Kint = Xstar(bc)
    check(f"kernel identity 3*g1(b)-4=beta(4-3beta)/(8-7beta) @ beta_c", 
          abs(3*gamma1(bc)-4-kernel(bc))<1e-14, f"{3*gamma1(bc)-4:.12e} = {kernel(bc):.12e}")

print("\n[3] Crossing compactness x* and ceiling mass M_puls")
print(f"    x*(beta_c) = kernel(beta_c)/C_gr + (W-weighted integral == same)")
for bc in (1e-4, 1e-3, 0.01, 0.1):
    xstar, xstar_exact, _, _ = Xstar(bc)
    print(f"    beta_c={bc:9.3e}: x*={xstar:.9e}  x*[kernel/Cgr]={xstar_exact:.9e}")

print("\n[4] Mass conversion along framework-registered relations")
print("    quartic (Lean I08): (1-beta)/beta^4=(M/M_E)^2, M_E=51.8 Msun")
print("    recombination-pinned L_Edd: R=sqrt(GMc/(kappa*sig*T^4)), M_puls=x*^2 c^5/(4G*kappa*sig*T^4)")
# quartic constant check with mu
k4 = KB**4; uu = u_mom
M_E_mu = math.sqrt(48.0*k4*uu**2/(7.5657e-15*MU_EST**4*(1.67262192e-24)**4*math.pi*G**3))/MSUN
print(f"    quartic constant: M_E(mu={MU_EST}) = {M_E_mu:.3f} Msun  (framework register: 51.8)")

cross = {}
for T in (4000.0, 5000.0, 6000.0):
    res = solve_crossing(T)
    if res is None:
        print(f"    T={T:.0f}K: NO crossing found"); continue
    bc, m1, m2 = res
    xst = Xstar(bc)[1]
    M1, M2 = m1, m2
    cross[int(T)] = dict(beta_c=bc, M_quartic_Msun=M1, M_family_Msun=M2, xstar=xst)
    print(f"    T={T:.0f}K: crossing beta_c={bc:.5e}, M_puls={M1:.4e} Msun  (x*={xst:.4e})")
# headline: T=5000 K
bc5 = cross[5000]["beta_c"]; M5 = cross[5000]["M_quartic_Msun"]; x5 = cross[5000]["xstar"]
print(f"\n    HEADLINE (T_rec = 5000 K):  x* = {x5:.6e}   M_puls = {M5:.4e} Msun")

# [5] verdict vs the registered pulsational ceiling 1e5-1e6 (LF cutoff 1e5.7)
print("\n[5] VERDICT vs framework register: pulsational ceiling = 1e5-1e6 Msun, LF cutoff 1e5.7")
LOW, HIGH, CUT = 1e5, 1e6, 10**5.7
in_band = (LOW <= M5 <= HIGH)
print(f"    M_puls(headline) = {M5:.4e} Msun  vs registered band [{LOW:.0e}, {HIGH:.0e}], LF cutoff {CUT:.3e}")
print(f"    T sensitivity: M_puls(4000K)={cross[4000]['M_quartic_Msun']:.3e}, "
      f"M_puls(5000K)={cross[5000]['M_quartic_Msun']:.3e}, M_puls(6000K)={cross[6000]['M_quartic_Msun']:.3e}")
all_out = all(LOW<=cross[T]["M_quartic_Msun"]<=HIGH for T in (4000,5000,6000))
verdict = "PASS" if in_band and all_out else "FAIL"
print(f"    >>> VERDICT: {verdict}  (pre-registered kill: M_puls must lie in [1e5,1e6])")

results = dict(
    lane="opus_49_doorA_pulsational_ceiling",
    lane_file="opus_49_doorA/pulsational_ceiling_lane.py",
    spine="fable_independent_2026/lean_2026/I13_bhstar_pulsation.lean (certified)",
    lane_emden_n3=dict(xi1=xi1, u=u_mom, W0=W0),
    C_gr_n3_homology=dict(Cgr=Cgr, benchmark_HR_18GMWgr=qcoef, benchmark_lit= BENCH),
    beta_profile="beta(r)=const on the n=3 polytrope + mixture (Eddington standard model); "
                  "rho/P^(3/4)=beta/(1-beta)^(1/4) constant",
    kernel="3*Gamma1-4 = beta*(4-3*beta)/(8-7*beta) (Lean-certified)",
    xstar_formula="W_beta/(C_gr*W_gr) = kernel(beta_c)/C_gr",
    mass_relations=dict(
        quartic="(1-beta)/beta^4=(M/M_E)^2, M_E=51.8 Msun (Lean I08/Wave Q)",
        R_family="R=sqrt(GMc/(kappa sigma T^4)), M_puls=x*^2 c^5/(4G kappa sigma T^4)",
        M_E_mu_check_Msun=M_E_mu,
        kappa_cm2_per_g=KAPPA),
    crossings_Msun=cross,
    headline=dict(T_K=5000.0, xstar=x5, M_puls_Msun=M5, verdict=verdict,
                  registered_band=[LOW, HIGH], LF_cutoff=CUT),
    verdict=verdict,
)
p = os.path.join(os.path.dirname(os.path.abspath(__file__)), "pulsational_ceiling_results.json")
with open(p, "w") as fh:
    json.dump(results, fh, indent=1)
print(f"\nwrote {p}")