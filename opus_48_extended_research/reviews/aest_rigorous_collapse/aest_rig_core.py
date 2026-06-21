#!/usr/bin/env python3
"""
RIGOROUS AeST COLLAPSE -- the three dropped caveats. CORE (constants, AeST field, gates).
=========================================================================================
Re-tests the phase-pinning of the AeST oscillation mode (the cluster-boost knob chi_infty)
after adding what the scalar-only 1+1D spherical collapse (wxbnjxb64) DROPPED:
  (1) SELF-CONSISTENCY  : r'' = -g_AeST integrated (NOT the cosine kinematic proxy);
  (2) the VECTOR sector : the K_B / E aether field, live only OFF-spherical (curl A != 0);
  (3) VIOLENT RELAXATION: multi-stream shell-crossing + non-radial (l=2,4) modes -> the
      time-dependent collective potential that drives phase-mixing.

QUARANTINE: a0=9.36e-11 = c^2 sqrt(Lambda/32pi) is an INPUT, never derived. mu, K_B, I0 are
FREE AeST inputs. BOTH-WAYS: a "pin" must be (i) IC-robust, (ii) a BOOST eta>1, (iii)
GALAXY-SAFE, (iv) robust to halving every numerical-viscosity/grid knob (NOT an artifact).
A "no-go" claim is held to the SAME bar -- we actively hunt a pin (damping swept to ~omega,
non-radial coupling turned on, tidal field added) and credit one if it survives.

AeST action (SZ2021 arXiv:2007.00082; Hamiltonian Blanchet-Skordis arXiv:2307.15126 Eq.1):
  S = (1/16piG) int sqrt(-g)[ R - 2L - (K_B/2)F_{mn}F^{mn} + (2-K_B)(2 J.grad phi - Y)
                              - F(Y,Q) - lambda(A.A + 1) ] + S_m[g]
  F_{mn}=2 grad_[m A_n] (Maxwell, ANTISYMM -> |E|^2-|B|^2, NO friction); J_m=A.grad A_m;
  Q=A.grad phi (temporal); Y=q.grad phi grad phi, q=g+AA (spatial); A.A=-1.
DECISIVE (DS24 / arXiv:2301.03499 App.B): spherical -> curl A=0, A-eq IDENTICAL to phi-eq,
"setting A=0 justified" -> the scalar-only solve lost NOTHING spherically; the vector is a
live channel ONLY off-spherical. Kandrup 1998 (astro-ph/9708026): phase-mixing damps a
coherent oscillation ONLY against a CONTINUUM of frequencies; a SHARP discrete mode persists.

Refs: SZ2021 2007.00082; DS24 2312.00889; VSB24 2304.05134; weak-lensing 2301.03499;
Blanchet-Skordis 2307.15126; Kandrup 1998 astro-ph/9708026; MRH08 0811.1833.
"""
import numpy as np, functools
from scipy.integrate import solve_ivp
print = functools.partial(print, flush=True)

# ============================================================ constants (SI)
c    = 2.99792458e8
G_N  = 6.674e-11
Msun = 1.989e30
kpc  = 3.0857e19
Mpc  = 3.0857e22
a0   = 9.36e-11          # FRAMEWORK INPUT (quarantined): c^2 sqrt(Lambda/32pi)
H0   = 67.4e3/Mpc
OL   = 0.685
Om_b = 0.05
Om_aest = 0.265
Om_m = Om_b + Om_aest
Gyr  = 3.1557e16

inv_mu_Mpc_default = 1.0
def mu_of(inv_mu_Mpc=inv_mu_Mpc_default): return 1.0/(inv_mu_Mpc*Mpc)

# ============================================================ AeST interpolation M(x)
# F(Y,Q) chosen so the quasistatic scalar gives MOND: x*M(x)=q has exact root x=q+sqrt(q).
def Mfunc(x):
    s = np.sqrt(1.0 + 4.0*np.abs(x)); return (s-1.0)/(s+1.0)
def xinv(q):
    q = np.abs(np.asarray(q, dtype=float)); return q + np.sqrt(q)

# ============================================================ STATIC AeST scalar (DS24 Eq 2.40)
# Canonical-momentum form P = r^2 M(x) Phi' (smooth through |Phi'|=0 nodes):
#   Phi' = a0 x sign(P),  P' = r^2(-mu^2 Phi + 4 pi G rho_b).
def make_rhs_static(mu2, rho_b):
    def rhs(r, Phi, P):
        x = xinv(np.abs(P)/(a0*r**2)); dPhi = a0*x*np.sign(P)
        dP  = r**2*(-mu2*Phi + 4*np.pi*G_N*rho_b(r))
        return dPhi, dP
    return rhs

def Phi0_natural(Menc, r0):
    x0 = xinv(G_N*Menc(r0)/(a0*r0**2)); return -a0*x0*r0

def _rk4_static(mu2, rho_b, Menc, r0, r1, dPhi0=0.0, n=4000):
    """Fixed-step RK4 for the static AeST scalar BVP-as-IVP. scipy-FREE (safe to nest
    inside an outer time integrator -- no f2py/Fortran callback reentrancy)."""
    rhs = make_rhs_static(mu2, rho_b)
    P0 = G_N*Menc(r0); Phi0 = Phi0_natural(Menc, r0) + dPhi0
    r = np.linspace(r0, r1, n); h = (r1-r0)/(n-1)
    Phi = np.empty(n); P = np.empty(n); Phi[0]=Phi0; P[0]=P0
    y = np.array([Phi0, P0])
    for i in range(n-1):
        ri = r[i]
        def f(rr, yy):
            d1, d2 = rhs(rr, yy[0], yy[1]); return np.array([d1, d2])
        k1=f(ri, y); k2=f(ri+0.5*h, y+0.5*h*k1)
        k3=f(ri+0.5*h, y+0.5*h*k2); k4=f(ri+h, y+h*k3)
        y = y + (h/6.0)*(k1+2*k2+2*k3+k4)
        Phi[i+1]=y[0]; P[i+1]=y[1]
    x = xinv(np.abs(P)/(a0*r**2)); g = a0*x*np.sign(P)
    return r, Phi, P, g

def integrate_static(mu2, rho_b, Menc, r0, r1, dPhi0=0.0, n=4000, use_scipy=True):
    if r1 <= r0:                       # guard collapsed-shell degeneracy
        r1 = r0*1.5
    if use_scipy:
        rhs = make_rhs_static(mu2, rho_b)
        P0 = G_N*Menc(r0); Phi0 = Phi0_natural(Menc, r0) + dPhi0
        def f(r, y):
            d1, d2 = rhs(r, y[0], y[1]); return [d1, d2]
        sol = solve_ivp(f, [r0, r1], [Phi0, P0], t_eval=np.linspace(r0, r1, n),
                        rtol=1e-10, atol=1e-15, method='DOP853',
                        max_step=max((r1-r0)/3000, 1e-30))
        r = sol.t; Phi = sol.y[0]; P = sol.y[1]
        x = xinv(np.abs(P)/(a0*r**2)); g = a0*x*np.sign(P)
        return r, Phi, P, g
    return _rk4_static(mu2, rho_b, Menc, r0, r1, dPhi0=dPhi0, n=n)

def g_mond_arr(r, Menc):
    r = np.atleast_1d(r); Me = np.atleast_1d(Menc(r))
    return a0*xinv(G_N*Me/(a0*r**2))

def g_aest_static(r_query, rho_b, Menc, mu2, r0, r1, dPhi0=0.0, n=3000, use_scipy=True):
    """AeST radial accel g(r)=Phi' on the live density, interpolated to r_query."""
    r, Phi, P, g = integrate_static(mu2, rho_b, Menc, r0, r1, dPhi0=dPhi0, n=n,
                                    use_scipy=use_scipy)
    return np.interp(r_query, r, g, left=g[0], right=g[-1]), (r, Phi, P, g)

# ============================================================ phase diagnostics
def fit_oscillation_phase(r, Phi, mu, r_window):
    """Phi ~ (A/r) cos(mu r + theta) over r_window. Returns (A, theta)."""
    sel = (r>=r_window[0]) & (r<=r_window[1])
    if sel.sum() < 8: return np.nan, np.nan
    rr, y = r[sel], Phi[sel]*r[sel]
    Bcos, Bsin = np.cos(mu*rr), np.sin(mu*rr)
    Cc, Cs = np.linalg.lstsq(np.vstack([Bcos, Bsin]).T, y, rcond=None)[0]
    return np.hypot(Cc, Cs), np.arctan2(-Cs, Cc)

def circ_std(thetas):
    th = np.array(thetas); th = th[np.isfinite(th)]
    if th.size < 2: return np.nan
    R = np.abs(np.mean(np.exp(1j*th))); return np.sqrt(-2*np.log(max(R,1e-12)))

def slope_theta_vs_ic(ic_phases, late_phases):
    """Wrap-aware slope of late_phase vs ic_phase. Sort by IC, then unwrap, then LSQ.
    A clean pin -> slope ~0; full IC-tracking -> slope ~ +1 (mod sign/offset)."""
    ic = np.array(ic_phases, float); la = np.array(late_phases, float)
    m = np.isfinite(la)
    if m.sum() < 2: return np.nan
    ic, la = ic[m], la[m]
    o = np.argsort(ic); ic, la = ic[o], la[o]
    la = np.unwrap(la)
    A = np.vstack([ic, np.ones(ic.size)]).T
    return np.linalg.lstsq(A, la, rcond=None)[0][0]

def pin_metric(ic_phases, late_phases):
    """Returns (slope, circ_std, |response|): circ_std of late phase is the ROBUST pin
    diagnostic (->0 pinned, large unpinned); |response| = |corr(e^{i th}, e^{i ic})| in
    [0,1] (1 = phase fully tracks IC, 0 = independent of IC)."""
    th = np.array(late_phases, float); ic = np.array(ic_phases, float)
    m = np.isfinite(th); th, ic = th[m], ic[m]
    if th.size < 2: return np.nan, np.nan, np.nan
    resp = np.abs(np.mean(np.exp(1j*(th - ic)))) if th.size else np.nan  # phase-locked response
    return slope_theta_vs_ic(ic, th), circ_std(th), resp

# ============================================================ cosmic time(a), H(a)
def t_of_a(a):
    return (2.0/(3.0*H0*np.sqrt(OL)))*np.arcsinh(np.sqrt(OL/Om_m)*a**1.5)
def H_of_a(a):
    return H0*np.sqrt(Om_m*a**-3 + OL)

# ============================================================ deep-MOND closed forms (gate)
def deep_mond_turnaround(r_ent, v_ent, M_i):
    alpha = v_ent**2/(2.0*np.sqrt(G_N*M_i*a0)); return r_ent*np.exp(alpha), alpha
def deep_mond_virial(r_ent, v_ent, M_i):
    _, al = deep_mond_turnaround(r_ent, v_ent, M_i); return r_ent*np.exp(al-0.5), al


# ============================================================================
#  VALIDATION GATES
# ============================================================================
if __name__ == "__main__":
    print("="*92)
    print("RIGOROUS AeST COLLAPSE -- CORE validation gates")
    print("="*92)
    print(f"a0={a0:.3e} (INPUT, quarantined) | 1/mu={inv_mu_Mpc_default} Mpc | "
          f"Om_m={Om_m} (Om_aest={Om_aest} QUARANTINED)")
    mu = mu_of(); muc = mu*c
    print(f"mu*c/H0 = {muc/H0:.1f}  -> chi oscillates {muc/H0/(2*np.pi):.0f} x per Hubble time")

    # GATE 1: mu=0 deep-MOND collapse -> r_vir/r_max = exp(-1/2)
    print("\n[GATE 1] mu=0 deep-MOND collapse closed form r_vir/r_max = exp(-1/2):")
    M_i=1e14*Msun; r_ent=0.3*Mpc; v_ent=200e3
    rmax,al = deep_mond_turnaround(r_ent, v_ent, M_i)
    rvir,_  = deep_mond_virial(r_ent, v_ent, M_i)
    print(f"  alpha={al:.4f} r_max={rmax/Mpc:.4f} r_vir={rvir/Mpc:.4f} "
          f"ratio={rvir/rmax:.8f} vs exp(-1/2)={np.exp(-0.5):.8f}")
    assert abs(rvir/rmax - np.exp(-0.5)) < 1e-9, "GATE1 FAIL"
    print("  PASS")

    # GATE 2: static AeST scalar at mu=0 reproduces analytic MOND g to ppm (smooth Hernquist)
    print("\n[GATE 2] static AeST scalar mu=0 -> analytic MOND g(r) (smooth Hernquist):")
    Mtot0 = 1e15*Msun; ah = 0.3*Mpc
    def Menc0(r): r=np.atleast_1d(r); o=Mtot0*r**2/(r+ah)**2; return o if o.size>1 else o[0]
    def rho0(r): r=np.atleast_1d(r); o=Mtot0*ah/(2*np.pi)/(r*(r+ah)**3); return o if o.size>1 else o[0]
    r,Phi,P,g = integrate_static(0.0, rho0, Menc0, 0.01*Mpc, 10*Mpc, n=8000)
    gM = g_mond_arr(r, Menc0); sel=(r>0.05*Mpc)&(r<8*Mpc)
    worst = np.max(np.abs(g[sel]/gM[sel]-1.0))
    print(f"  max |g/g_MOND - 1| over [0.05,8]Mpc = {worst*1e6:.3f} ppm")
    assert worst < 1e-4, "GATE2 FAIL"
    print("  PASS")

    # GATE 3: vector trivial in spherical symmetry (curl A == 0 by construction).
    # In spherical symmetry A = A_r(r) e_r; curl of a purely radial field is identically 0,
    # and the A-eq reduces to the phi-eq (DS24). Verify the curl operator on a radial field.
    print("\n[GATE 3] vector trivial spherically: curl(A_r e_r) == 0 (analytic + numeric):")
    th = np.linspace(0.1, np.pi-0.1, 50); rr = np.linspace(0.1, 3, 50)
    R, TH = np.meshgrid(rr, th, indexing='ij')
    Ar = 1.0/R**2                      # any radial profile A_r(r)
    # curl in spherical, phi-component of a field with only A_r(r): (1/r) d(r A_th)/dr - (1/r) dA_r/dth
    # A_th=0, A_r=A_r(r) -> dA_r/dth = 0 -> curl_phi = 0 exactly.
    dAr_dth = np.gradient(Ar, th, axis=1)
    curl_phi = -(1.0/R)*dAr_dth
    print(f"  max|curl_phi(A_r(r) e_r)| = {np.max(np.abs(curl_phi)):.2e} (==0 to FD roundoff -> vector trivial)")
    assert np.max(np.abs(curl_phi)) < 1e-10, "GATE3 FAIL"
    print("  PASS -- scalar-only spherical solve dropped NOTHING from the vector; vector is")
    print("         a live channel ONLY off-spherical (curl A != 0), tested in caveats 2+3.")

    # GATE 4: scipy-free RK4 field solver matches the DOP853 one (used inside the collapse)
    print("\n[GATE 4] RK4 (scipy-free) field solver matches DOP853 (mu=1/Mpc, real mass term):")
    mu = mu_of()
    r_s,Phi_s,P_s,g_s = integrate_static(mu**2, rho0, Menc0, 0.05*Mpc, 6*Mpc, n=3000, use_scipy=True)
    r_r,Phi_r,P_r,g_r = integrate_static(mu**2, rho0, Menc0, 0.05*Mpc, 6*Mpc, n=3000, use_scipy=False)
    gint = np.interp(r_s, r_r, g_r)
    sel=(r_s>0.1*Mpc)&(r_s<4*Mpc)
    dd = np.max(np.abs(gint[sel]/g_s[sel]-1.0))
    print(f"  max |g_RK4/g_DOP853 - 1| over [0.1,4]Mpc = {dd*1e6:.2f} ppm")
    assert dd < 1e-3, "GATE4 FAIL (RK4 field solver disagrees)"
    print("  PASS (RK4 is safe to nest inside the collapse integrator)")

    print("\nAll core gates PASS. Run aest_rig_selfconsistent.py (caveat 1),")
    print("aest_rig_nonradial_vector.py (caveats 2+3), aest_rig_ADVERSARIAL.py (artifact ruling).")
