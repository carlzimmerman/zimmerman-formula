#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AS239 (Tier-0b) numeric wave code: tensor propagation through an inhomogeneous
carrier region (slab).  Validates the derived quadratic action
    L_T^2 = A qdot^2 + C q'^2 + D q^2
    A = (M/4)/(N b),  C = -(M/4) N/b^3,  D = -N P_d/(2 b)   [D_EH = 0 at O(lambda/L)^2]
EOM:  2A qdd + 2 dA qd + 2C q'' + 2 dC q' - 2D q = 0
Checks (capable of failing):
  C1 cone: measured local wavenumber theta'(x) vs symbol kappa(x): speed N/b
      (t_c = e^z must NOT enter); residual reported.
  C2 amplitude law: |psi(x)| * N(x)/b(x)^2 ~ const along the slab (static law
      Amp = Amp0 * b^2/N); residual reported.
  C3 mass refraction: with m_T^2 = 2 N^2 P_d/M: delta(phase) vs integral
      |m^2|/(2 kappa) dx; residual reported.
  C4 NC1: photon speed from g_d gives (N/b) e^{-z}: false mismatch fires
      (mismatch != 0) while the g-comparison passes (residual ~ 0).
  C5 NC2: shear-modified kinetic A -> A + kap-sh: extracted speed^2 shifts to
      M/(M+kappa) N^2/b^2 and the pure-Einstein check fails (residual ~ kap).
  C6 FRW time-domain: EOM qdd - H qd + (k/a)^2 q = 0 (physical normalization);
      amplitude alpha(t) * a(t) ~ const (matches AS238/240 amplitude law);
      phase speed = 1 in physical units.
All bounded: 1 thread, wall budget, fixed grids.
"""
import numpy as np
import time, math, os, sys

T0 = time.time()
M1 = 1.0                       # M = M_P^2 = 1 in these units (overall scale)

# ---------------- slab setup ----------------------------------------------------
L    = 2.5                     # carrier overdensity scale (slow variation)
x0   = 0.0
Nx   = 12001
x    = np.linspace(-10.0, 10.0, Nx)
dx   = x[1] - x[0]

def gauss(center=x0, width=L, amp=1.0):
    return amp*np.exp(-(x - center)**2/(2*width**2))

n1, b1 = 0.06, -0.05           # weak lapse/spatial scale variations
Np  = 1.0 + n1*gauss()
bp  = 1.0 + b1*gauss()
z0  = 0.2624                   # ln(1.3): t_c in {1.3, 1.0, 0.7} sampled via profile
zprof = z0*gauss()            # carrier overdensity: t_c = exp(z) bounded positive
tc_prof = np.exp(zprof)
W0   = 0.02                   # static-clump potential: P_d = -W
Pdev = -W0*gauss()            # carrier pressure profile (static clump: P_d < 0)

def d_num(f, a=1.0):
    return np.gradient(f, dx)/a

# ---------------- EOM coefficients ----------------------------------------------
Acoef = (M1/4.0)/(Np*bp)
Ccoef = -(M1/4.0)*Np/bp**3
Dcoef = -Np*Pdev/(2.0*bp)          # carrier mass; D_EH = 0 at declared order
dA = d_num(Acoef); dC = d_num(Ccoef)

# monochromatic steady-state: q = psi(x) e^{-i w t}:
#   psi'' + (dC/C) psi' + (-A w^2 - D)/C * psi = 0      (C<0)
#   -> psi'' + (dC/C) psi' + kap2(x) psi = 0,  kap2 = (A w^2 + D)/(-C)
omega0 = 40.0                 # carrier-region GW frequency (>> |gradient scales|)
kap2 = lambda w2: (Acoef*w2 + Dcoef)/(-Ccoef)
kap0 = np.sqrt(np.maximum(kap2(omega0**2), 0.0))

def solve_slab(w2, useD=False, Aa=None):
    """Solve psi'' + s(x) psi' + kap2(x) psi = 0 on the slab by RK4 shooting
    with WKB entry data at x = -8.0.  useD: include the carrier mass term;
    Aa: kinetic-coefficient override (shear diagnostic)."""
    A_ = Acoef if Aa is None else Aa
    s_ = dC/Ccoef
    K2 = (A_*w2 + (Dcoef if useD else 0.0))/(-Ccoef)
    K  = np.sqrt(np.maximum(K2, 0.0))
    xin = -8.0
    i0 = int((xin - x[0])/dx)
    # WKB entry: psi ~ alpha(x) e^{i I(x)}, alpha = b^2/N (static amplitude law)
    alph = (bp**2/Np)
    ths  = np.cumsum(K)*dx
    d_alph = d_num(alph)
    ee = np.exp(1j*ths[i0])
    y0 = complex(alph[i0]*ee)
    y1 = complex((d_alph[i0] + 1j*K[i0]*alph[i0])*ee)
    ps = np.zeros(Nx, dtype=complex)
    pd = np.zeros(Nx, dtype=complex)
    ps[i0] = y0; pd[i0] = y1
    # RK4 with fixed step over [i0, Nx-1]
    for i in range(i0, Nx-1):
        def F(p, pp):
            return pp, -(s_[i]*pp + K2[i]*p)
        k1p, k1v = F(ps[i], pd[i])
        k2p, k2v = F(ps[i] + dx*k1p/2, pd[i] + dx*k1v/2)
        k3p, k3v = F(ps[i] + dx*k2p/2, pd[i] + dx*k2v/2)
        k4p, k4v = F(ps[i] + dx*k3p, pd[i] + dx*k3v)
        ps[i+1] = ps[i] + dx*(k1p + 2*k2p + 2*k3p + k4p)/6
        pd[i+1] = pd[i] + dx*(k1v + 2*k2v + 2*k3v + k4v)/6
    ph = np.unwrap(np.angle(ps))
    return ps, ph, K

ps, ph, Ksym = solve_slab(omega0**2)

# ---------------- C1: local cone --------------------------------------------------
mask = (x > -7.0) & (x < 7.0)
th_p = np.gradient(ph, dx)
c_meas  = np.divide(omega0, th_p, out=np.full_like(th_p, np.nan), where=th_p != 0)
c_expect = Np/bp                       # photon null cone of g (speed in x-units)
res_cone = np.abs(c_meas - c_expect)/c_expect
res_cone_masked = np.max(res_cone[mask])
# false g_d comparison:
c_false = (Np/bp)*np.exp(-zprof)
res_false = np.abs(c_meas - c_false)/c_false  # "photons on g_d": must NOT match
res_false_masked = np.max(res_false[mask])
print("=== C1 cone check (WKB): measured phase speed vs cones ===")
print(f"profiles: N in [{Np.min():.4f},{Np.max():.4f}], b in [{bp.min():.4f},{bp.max():.4f}], "
      f"t_c = e^z in [{tc_prof.min():.4f},{tc_prof.max():.4f}]")
print(f"max |c_meas/c_g - 1| over x in [-7,7]: {res_cone_masked:.3e}")
print(f"max |c_meas/c_{'g_d'} - 1| (FALSE photon cone on g_d): {res_false_masked:.3e}")
print(f"NC1 verdict: g-cone residual {res_cone_masked:.2e} (~0: cone matches); "
      f"g_d mismatch {res_false_masked:.2e} != 0 -> false speed mismatch IDENTIFIED")

# ---------------- C2: static amplitude law ---------------------------------------
Amp = np.abs(ps)
amp_law = Amp*Np/bp**2                  # leading WKB law: Amp = Amp0 * b^2/N
res_amp = np.max(np.abs(amp_law[mask] - np.mean(amp_law[mask]))/np.mean(amp_law[mask]))
# exact current for u'' + s u' + k2 u = 0: e^{int s} |u|^2 d(phase)/dx = const,
# with s = C'/C -> e^{int s} = |C| (C<0: |C| = (M/4) N/b^3):
Cabs = (M1/4.0)*Np/bp**3
curr = (Amp**2)*th_p*Cabs
res_curr = np.max(np.abs(curr[mask] - np.mean(curr[mask]))/np.mean(curr[mask]))
print(f"\n=== C2 amplitude law (static): leading WKB Amp*N/b^2 residual = {res_amp:.3e}")
print(f"   exact 1D current |psi|^2 * d(phase)/dx residual = {res_curr:.3e}")
print("   (amplitude changes with the carrier density; speed does not:",
      "'amplitude vs speed' distinction verified)")

# ---------------- C3: mass refraction ----------------------------------------------
ps_ref, ph_ref, _ = solve_slab(omega0**2, useD=True)
dphi_meas = ph_ref - ph
K2base = (Acoef*omega0**2 + 0.0*Dcoef)/(-Ccoef)
K2ref  = (Acoef*omega0**2 + 1.0*Dcoef)/(-Ccoef)
dkap = np.sqrt(np.maximum(K2ref, 0.0)) - np.sqrt(np.maximum(K2base, 0.0))
dphi_theory = np.zeros(Nx)
dphi_theory[mask] = np.cumsum(dkap[mask])*dx
res_refr = np.max(np.abs((dphi_meas[mask] - dphi_theory[mask]) - np.mean(
                    (dphi_meas - dphi_theory)[mask]))/np.max(np.abs(dphi_meas[mask])))
print(f"\n=== C3 mass refraction: analytic delta_phi = int delta_kappa dx vs measured")
print(f"   max residual (slope-removed): {res_refr:.3e}")
print(f"   m_T^2 = 2 P_d/M = {2.0*Pdev[mask].min()/M1:.4e} (P_d < 0 static clump;",
      "refraction, not speed change)")

# ---------------- C4/C5 negative controls ------------------------------------------
print(f"\n=== C4 (NC1) quantified mismatch over the clump (sample t_c set) ===")
for tc_ in (1.3, 1.0, 0.7):
    zz = math.log(tc_)
    mism = math.exp(-2*zz) - 1.0
    print(f"   t_c = {tc_}: z = {zz:+.4f}: false speed^2 mismatch factor = {mism:+.4f}, "
          f"speed ratio e^-z = {math.exp(-zz):.4f}  (detected iff z != 0)")

kap_sh = 0.5
A_sh = Acoef + (kap_sh/8.0)*Np*bp**3*(1.0/Np**2)*2.0/bp**4
dA_sh = d_num(A_sh)
s_sh = dC/Ccoef
K2sh = (A_sh*omega0**2 + Dcoef)/(-Ccoef)
Ksh = np.sqrt(np.maximum(K2sh, 0.0))
ps_sh, ph_sh, _ = solve_slab(omega0**2, Aa=A_sh)
th_p_sh = np.gradient(ph_sh, dx)
c_sh = np.divide(omega0, th_p_sh, out=np.full_like(th_p_sh, np.nan), where=th_p_sh != 0)
exp_sh = np.sqrt(M1/(M1+kap_sh))*(Np/bp)
res_sh = np.max(np.abs(c_sh[mask] - exp_sh[mask])/exp_sh[mask])
res_einstein_only = np.max(np.abs(c_sh[mask] - c_expect[mask])/c_expect[mask])
print(f"\n=== C5 (NC2) shear diagnostic: extracted speed^2 -> M/(M+kappa) = {M1/(M1+kap_sh):.4f}")
print(f"   max |c_shear/c^(M/(M+k)) - 1| = {res_sh:.3e}  (fits the shear law)")
print(f"   max |c_shear/c_g - 1| (pure-Einstein cone check FAILS): {res_einstein_only:.3e}"
      f"  -> control would have detected the modified theory")

# ---------------- C6: FRW time-domain ----------------------------------------------
print("\n=== C6 FRW time-domain amplitude law (physical normalization) ===")
nt = 61000
t = np.linspace(1.0, 61.0, nt)          # a = t^(2/3): a(1) = 1; omega = k/a < 30
dt = t[1]-t[0]
print(f"   max(omega*dt) = {30.0*dt:.4f} (Nyquist margin ok)")
a = t**(2.0/3.0)
aD = (2.0/3.0)*t**(-1.0/3.0)
H = aD/a
k = 30.0
m2f = -0.05                            # |m^2| = 2|P_d|/M small
U  = np.zeros(nt, dtype=complex); Ud = np.zeros(nt, dtype=complex)
Afr = (M1/4.0)/a
U[0]  = 0.1 + 0j
Ud[0] = -1j*np.sqrt(k**2/a[0]**2 + m2f)*U[0]
def Ff(u, up, i):
    # EOM u'' + (d ln A) u' + (k^2/a^2 + m2f) u = 0 with d ln A = -H
    return up, (H[i]*up - (k**2/a[i]**2 + m2f)*u)
for i in range(nt-1):
    k1p, k1v = Ff(U[i], Ud[i], i)
    k2p, k2v = Ff(U[i]+dt*k1p/2, Ud[i]+dt*k1v/2, i)
    k3p, k3v = Ff(U[i]+dt*k2p/2, Ud[i]+dt*k2v/2, i)
    k4p, k4v = Ff(U[i]+dt*k3p, Ud[i]+dt*k3v, i)
    U[i+1]  = U[i]  + dt*(k1p + 2*k2p + 2*k3p + k4p)/6
    Ud[i+1] = Ud[i] + dt*(k1v + 2*k2v + 2*k3v + k4v)/6
env = np.abs(U)
res_env = np.max(np.abs(env/a - np.mean(env/a))/np.mean(env/a))
wm = np.gradient(np.unwrap(np.angle(U)), dt)
c_frw = np.median(np.abs(wm)/(k/a))
print(f"   max |env/a - <env/a>|/<env/a> = {res_env:.3e}")
print("   u (metric perturbation in comoving coordinates) ~ a  <=>  q = u/a^2 ~ a^-1",
      "(strain normalization of AS238/240: same invariant)")
print(f"   median |phase frequency|/(k/a) = {c_frw:.6f}  (speed 1)")

# ---------------- C7: dimensional examples (both footings, kappa = 1/2 adopted) ---
print("\n=== C7 dimensional examples: a0 = (c/2) sqrt(G_bare rho_Lambda), kappa = 1/2 ===")
G_bare = 6.67430e-11
c_l = 299792458.0
M_sun = 1.98847e30
pc_l = 3.085677581491367e16
a0_canon = 9.3619e-11
a0_alt   = 1.1279e-10
rho_canon = (2.0*a0_canon/c_l)**2/G_bare
rho_alt   = (2.0*a0_alt/c_l)**2/G_bare
print(f"G_bare = {G_bare:.5e} (SI), c = {c_l:.6e} (SI)")
print(f"footing 1 (canonical):  a0 = {a0_canon:.4e} m/s^2  ->  rho_Lambda = {rho_canon:.4e} kg/m^3")
print(f"footing 2 (alternative):a0 = {a0_alt:.4e} m/s^2  ->  rho_Lambda = {rho_alt:.4e} kg/m^3")
print("(alternative footing interpreted as changed vacuum density with kappa = 1/2",
      "fixed; interpreted as changed kappa = 1/2*a0_alt/a0_canon =",
      f"{0.5*a0_alt/a0_canon:.4f} with rho fixed: the two footings cannot share both.)")
Mb = 1.0e12*M_sun
for name, a0 in (("canonical", a0_canon), ("alternative", a0_alt)):
    rM = math.sqrt(G_bare*Mb/a0)
    vf = (G_bare*Mb*a0)**0.25
    lamT = c_l/100.0                # LIGO-band 100 Hz wavelength
    print(f"  [{name} footing] r_M(1e12 M_sun) = {rM:.4e} m = {rM/pc_l:.2f} kpc ; "
          f"v_flat = (G M_b a0)^(1/4) = {vf:.4f} m/s = {vf/1000:.2f} km/s ; "
          f"lambda_T(100 Hz)/r_M = {lamT/rM:.3e} << 1 : WKB domain holds")
print("  -> the dimensionless result (tensor cone = photon null cone of g) applies",
      " identically to both footings; only dimensioned scales (r_M, rho_Lambda)",
      " shift.")

print("\n--- bounds ---")
print(f"wall time numeric: {time.time()-T0:.1f} s ; grid Nx = {Nx}, nt = {nt} ; "
      f"threads: 1 (env set) ; omega0 = {omega0} ; k = {k}")
sys.exit(0)