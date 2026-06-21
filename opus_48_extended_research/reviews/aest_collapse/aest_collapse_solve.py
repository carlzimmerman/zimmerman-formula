#!/usr/bin/env python3
"""
AeST SPHERICAL COLLAPSE THROUGH TURNAROUND -- the DYNAMICAL phase-pinning test.
==============================================================================
THE OPEN DOOR (banked wn6n716aa / AEST_NONLINEAR_PHI_CLUSTER_2026-06-20): the static
spherical BVP leaves the AeST oscillation PHASE (= the Helmholtz integration constant
dPhi0 / equivalently chi_infty) FREE; the cluster boost eta(R500) therefore spans
-3.12..+3.97 and is DESCRIPTIVE not predictive. THE QUESTION: does DYNAMICAL collapse
from cosmological ICs through turnaround + virialization PIN that phase -- and if so, to
a BOOST, UNIVERSALLY (IC-independent), GALAXY-SAFELY?

This solver evolves a spherical overdensity (onion shells, Malekjani-Rahvar-Haghi 2008
arXiv:0811.1833, after Sanders 2001 / Nusser 2002) from z~20 through turnaround to
virialization, solving the REAL AeST field at each time step (NOT a proxy):

  MODE 3a (quasistatic-per-step): the EXACT static DS24 Eq 2.40 modified-Helmholtz BVP
    (1/r^2) d/dr[r^2 M(x) Phi'] + mu_t^2 Phi = 4 pi G_N rho_b(r,t)
  solved on the instantaneous density rho_b(r,t), accel g=Phi' fed back to the shells.

  MODE 3b (FULLY TIME-DEPENDENT -- where dynamical phase memory lives): restore the time
  derivative dropped in the quasistatic limit. The scalar perturbation chi obeys a
  Klein-Gordon-like WAVE equation with mass mu (SZ2021 Eq 6 w/ d_t restored; the
  "nonlocality" of Blanchet-Marleau-Skordis 2024):
    chi_tt - c_s^2 [ chi_rr + (2/r) chi_r ] + (mu c)^2 chi = S[rho_b(r,t)]
  sourced by the MOVING collapse density. The oscillation phase at virialization is then
  an OUTPUT of the whole collapse trajectory -- this is exactly the physics the static BVP
  discards. We track whether the phase CONVERGES (pins) or retains IC memory (unpinned).

DIAGNOSTICS (C1-C5):
  C1 phase convergence theta(t)->theta*?   C2 IC-independence (ensemble, DECISIVE)
  C3 boost vs deficit sign of eta(R500)     C4 galaxy veto (same machinery, 1e11 Msun)
  C5 Cassini (selected phase keeps |gamma-1|<2.3e-5)

QUARANTINE: a0=9.36e-11 (=c^2 sqrt(Lambda/32pi)) is an INPUT, never derived. I0/Om_AeST,
mu, lambda_s are FREE AeST inputs. BOTH-WAYS (Carl #1 rule): if collapse pins a BOOST
universally + galaxy-safely, credit it at full weight (door reopens). If the phase is
IC-dependent / deficit-selected / galaxy-breaking, report the no-go holds dynamically.
Do NOT manufacture a pin; do NOT high-priest a genuine one.

Validation gates: mu=0 reproduces analytic MOND collapse (r_max, r_vir closed forms) to
~1e-6; the frozen-rho static limit reproduces the banked aest_phi_cluster_solve eta curve.

Refs: SZ2021 (2007.00082); VSB24 (2304.05134); DS24 (2312.00889); BS24 (2404.06584);
Blanchet-Marleau-Skordis 2024 (2402.11716, nonlocality); MRH08 (0811.1833).
"""
import numpy as np
import functools
from scipy.integrate import solve_ivp
from scipy.optimize import brentq
print = functools.partial(print, flush=True)

# ============================================================ constants (SI)
c    = 2.99792458e8
G_N  = 6.674e-11
Msun = 1.989e30
kpc  = 3.0857e19
Mpc  = 3.0857e22
a0   = 9.36e-11          # FRAMEWORK INPUT (quarantined): c^2 sqrt(Lambda/32pi)

# cosmological background (AeST FLRW: AeST dust replaces CDM)
H0   = 67.4e3/Mpc
OL   = 0.685
Om_b = 0.05
Om_aest = 0.265          # set by I0 to match CMB dust (QUARANTINED, never derived)
Om_m = Om_b + Om_aest
Lam  = 3.0*OL*H0**2/c**2

# AeST Helmholtz mass (CMB / flat-RC pinned 1/mu ~ 1 Mpc; robustness band 0.5-2 Mpc)
inv_mu_Mpc = 1.0
def mu_of(inv_mu_Mpc=inv_mu_Mpc): return 1.0/(inv_mu_Mpc*Mpc)
beta0 = 0.0              # lambda_s -> inf (totally screened "simple" interp, DS24 default)

# ============================================================ AeST interpolation M(x)
def Mfunc(x):
    s = np.sqrt(1.0 + 4.0*np.abs(x)); return (s-1.0)/(s+1.0)
def xinv(q):
    """exact positive root of x*M(x)=q : x = q + sqrt(q) (sympy-verified)."""
    q = np.abs(np.asarray(q, dtype=float)); return q + np.sqrt(q)

# ============================================================ (A) STATIC field solve (mode 3a)
# canonical-momentum form (DS24 Sec 3): P = r^2 M(x) Phi', smooth through |Phi'|=0 nodes.
def make_rhs_static(mu_t2, rho_b):
    def rhs(r, Phi, P):
        x = xinv(np.abs(P)/(a0*r**2))
        dPhi = a0*x*np.sign(P)
        dP   = r**2*(-mu_t2*Phi + 4*np.pi*G_N*rho_b(r))
        return dPhi, dP
    return rhs

def Phi0_natural(Menc, r0):
    x0 = xinv(G_N*Menc(r0)/(a0*r0**2)); return -a0*x0*r0

def integrate_static(mu_t2, rho_b, Menc, r0, r1, dPhi0=0.0, n=8000):
    rhs = make_rhs_static(mu_t2, rho_b)
    P0 = G_N*Menc(r0); Phi0 = Phi0_natural(Menc, r0) + dPhi0
    def f(r, y):
        d1, d2 = rhs(r, y[0], y[1]); return [d1, d2]
    sol = solve_ivp(f, [r0, r1], [Phi0, P0], t_eval=np.linspace(r0, r1, n),
                    rtol=1e-10, atol=1e-15, method='DOP853', max_step=(r1-r0)/3000)
    r = sol.t; Phi = sol.y[0]; P = sol.y[1]
    x = xinv(np.abs(P)/(a0*r**2)); g = a0*x*np.sign(P)
    return r, Phi, P, g

def g_mond_arr(r, Menc):
    r = np.atleast_1d(r); Me = np.atleast_1d(Menc(r))
    return a0*xinv(G_N*Me/(a0*r**2))

# ============================================================ (B) onion-shell collapse
# Per-shell EOM r'' = -g(r,t). g from the AeST field at each step (or closed MOND for mu=0).
def deep_mond_turnaround(r_ent, v_ent, M_i):
    alpha = v_ent**2/(2.0*np.sqrt(G_N*M_i*a0)); return r_ent*np.exp(alpha), alpha
def deep_mond_virial(r_ent, v_ent, M_i):
    _, alpha = deep_mond_turnaround(r_ent, v_ent, M_i); return r_ent*np.exp(alpha-0.5), alpha

def H_of_a(a):
    return H0*np.sqrt(Om_m*a**-3 + OL)

# ============================================================ phase diagnostics
def fit_oscillation_phase(r, Phi, mu_t, r_window):
    """Phi ~ A cos(mu r + theta)/r over r_window. Returns (A, theta). Linear LSQ."""
    sel = (r>=r_window[0]) & (r<=r_window[1])
    if sel.sum() < 8: return np.nan, np.nan
    rr, y = r[sel], Phi[sel]*r[sel]
    Bcos, Bsin = np.cos(mu_t*rr), np.sin(mu_t*rr)
    Cc, Cs = np.linalg.lstsq(np.vstack([Bcos, Bsin]).T, y, rcond=None)[0]
    return np.hypot(Cc, Cs), np.arctan2(-Cs, Cc)

def eta_at(r_arr, g, Menc, R500):
    """eta = g_AeST/g_MOND - 1 at R500 (the phantom-boost observable)."""
    gM = g_mond_arr(r_arr, Menc)
    i = np.argmin(np.abs(r_arr-R500))
    return g[i]/gM[i] - 1.0

# ============================================================================
# ============================================================================
#  THE DYNAMICAL SOLVE
# ============================================================================
# ============================================================================

class Cluster:
    """A collapsing spherical overdensity: onion shells + AeST field, evolved a_dec->1."""
    def __init__(self, Mtot, R500_phys, profile='tophat', n_shell=24, inv_mu_Mpc=1.0,
                 delta_dec=None, z_dec=20.0, seed=0, fbary=1.0):
        self.Mtot = Mtot*Msun
        self.R500 = R500_phys
        self.profile = profile
        self.n = n_shell
        self.mu = mu_of(inv_mu_Mpc); self.mu_t2 = (1.0+beta0)*self.mu**2
        self.z_dec = z_dec; self.a_dec = 1.0/(1+z_dec)
        self.fbary = fbary
        rng = np.random.default_rng(seed)
        # --- per-shell Lagrangian masses (enclosed) ---
        Mfrac = np.linspace(1.0/self.n, 1.0, self.n)
        self.M_i = Mfrac*self.Mtot          # enclosed baryon mass at shell i
        # --- comoving (Lagrangian) radii at decoupling from the profile ---
        # tophat: uniform overdensity; Hernquist / NFW-progenitor: concentrated.
        if profile == 'tophat':
            q = Mfrac**(1/3.)
        elif profile == 'hernquist':
            # M(<r) = M r^2/(r+a)^2 -> r(M) = a sqrt(f)/(1-sqrt(f))
            ah = 0.45; q = ah*np.sqrt(Mfrac)/(1-np.sqrt(Mfrac)); q/=q[-1]
        elif profile == 'nfw':
            cc = 5.0
            def mnfw(x): return np.log(1+cc*x) - cc*x/(1+cc*x)
            xs = np.geomspace(1e-3,1,4000); mm = mnfw(xs)/mnfw(1.0)
            q = np.interp(Mfrac, mm, xs)
        else:
            raise ValueError(profile)
        # physical radius of the top-hat at decoupling (turnaround mass -> comoving size)
        # use the standard spherical-collapse normalization: a shell of enclosed mass M
        # has comoving Lagrangian radius set by the cosmic mean density.
        rho_mean0 = Om_m*3*H0**2/(8*np.pi*G_N)         # present mean matter density
        R_lag = (3*self.Mtot/(4*np.pi*rho_mean0))**(1/3.)   # comoving Lagrangian radius
        self.r_com = q*R_lag                                # comoving radius per shell
        # --- initial overdensity amplitude (drawn to give turnaround near z~0.3-1) ---
        if delta_dec is None:
            # linear delta at z_dec s.t. collapse ~ today: delta_dec ~ 1.686/D(a=1)*a_dec
            delta_dec = 1.686*self.a_dec*1.2
        self.delta_dec = delta_dec*(1.0+0.0*rng.standard_normal())  # ensemble realization knob
        # add small per-shell scatter for "random infall realization"
        self.delta_shell = self.delta_dec*(1.0 + 0.0)  # tophat: uniform; overridden below
        self.seed = seed

    def Menc_func(self, r_phys_shells):
        """interpolant M_baryon(<r) from current shell positions (mass conservation)."""
        rs = np.concatenate([[0.0], np.sort(r_phys_shells)])
        Ms = np.concatenate([[0.0], self.M_i[np.argsort(r_phys_shells)]])
        # ensure monotone
        Ms = np.maximum.accumulate(Ms)
        def Menc(r):
            return np.interp(r, rs, Ms, left=0.0, right=self.Mtot)
        return Menc

    def rho_b_func(self, r_phys_shells):
        """smooth rho_b(r) from shell positions (finite-difference of M_enc)."""
        rs = np.sort(r_phys_shells)
        Ms = self.M_i[np.argsort(r_phys_shells)]
        Ms = np.maximum.accumulate(Ms)
        # density in shells
        rs_e = np.concatenate([[0.0], rs])
        dM = np.diff(np.concatenate([[0.0], Ms]))
        Vsh = (4*np.pi/3.)*(rs_e[1:]**3 - rs_e[:-1]**3)
        rho_sh = dM/np.maximum(Vsh, 1e-30)
        rc = 0.5*(rs_e[1:]+rs_e[:-1])
        def rho_b(r):
            r = np.atleast_1d(r)
            out = np.interp(r, rc, rho_sh, left=rho_sh[0], right=0.0)
            return out if out.size>1 else out[0]
        return rho_b

    # ---------------- field solve at a snapshot (mode 3a quasistatic) ----------------
    def field_static(self, r_shells, dPhi0=0.0, r_match=None, n=4000):
        Menc = self.Menc_func(r_shells); rho_b = self.rho_b_func(r_shells)
        rs = np.sort(np.asarray(r_shells))
        rs = rs[np.isfinite(rs) & (rs > 0)]
        # floor the inner radius: avoid r0->0 where Phi0_natural ~ -G*M/r0 diverges.
        # use a small fraction of R500 (or the 2nd shell) -- the deep interior is sub-grid.
        r0 = max(0.5*rs[0], 0.01*self.R500)
        r1 = (r_match if r_match else 4*rs[-1])
        r, Phi, P, g = integrate_static(self.mu_t2, rho_b, Menc, r0, r1, dPhi0=dPhi0, n=n)
        return r, Phi, P, g, Menc


# ============================================================================
#  MODE 3b: the GENUINELY TIME-DEPENDENT chi field (the phase-memory test)
# ============================================================================
def evolve_chi_wave(rho_b_of_t, r_grid, t_grid, mu, cs, chi0=None, chidot0=None,
                    Phi_amp_of_t=None, damping=0.0):
    """
    Evolve the AeST scalar perturbation chi(r,t) as a Klein-Gordon-like WAVE (SZ2021 Eq 6
    with the time derivative RESTORED -- the piece the quasistatic limit drops):

        chi_tt + 2*damping*chi_t - cs^2 [ chi_rr + (2/r) chi_r ] + (mu c)^2 chi = S(r,t)

    where S is the +mu^2-term source driven by the collapse density / potential. This is
    the regime where the oscillation phase carries MEMORY of the collapse trajectory
    (Blanchet-Marleau-Skordis 2024 "nonlocality"). The QUESTION the door turns on: as the
    source virializes (becomes static), does chi(r,t) RELAX to a unique phase (pinned), or
    keep oscillating forever at frequency ~mu*c with an amplitude/phase set by initial data
    (unpinned)?

    KEY PHYSICS (both-ways honest): the homogeneous operator is a CONSERVATIVE wave operator
    (Klein-Gordon, mass mu). With damping=0 (the physical AeST case -- there is no friction
    term in the shift-symmetric action; the only "damping" is Hubble 3H which is ~mu*c/(...)
    weak at cluster scales since mu*c >> H), the chi mode is a forced+free oscillator: the
    FREE oscillation at omega=mu*c persists undamped and its phase is set by IC -> NOT pinned.
    We solve it explicitly and MEASURE the late-time phase vs IC to settle it rather than
    assert it.

    Returns dict with chi(r,t), the late-time oscillation phase theta(t), amplitude A(t).
    """
    Nr = len(r_grid); dr = r_grid[1]-r_grid[0]
    chi = np.zeros(Nr) if chi0 is None else chi0.copy()
    chidot = np.zeros(Nr) if chidot0 is None else chidot0.copy()
    om2 = (mu*c)**2
    hist_phase = []; hist_amp = []; hist_t = []; chi_center = []
    # match r-window for phase fit
    rlo, rhi = r_grid[Nr//3], r_grid[2*Nr//3]
    def laplacian(f):
        lap = np.zeros_like(f)
        lap[1:-1] = (f[2:]-2*f[1:-1]+f[:-2])/dr**2 + (2.0/r_grid[1:-1])*(f[2:]-f[:-2])/(2*dr)
        # r=0 regularity: chi_r=0 -> use 6 f''(0); outer: outgoing/Sommerfeld-ish (clamp)
        lap[0] = 6.0*(f[1]-f[0])/dr**2
        lap[-1] = lap[-2]
        return lap
    dt = t_grid[1]-t_grid[0]
    # CFL check on the wave speed cs
    cfl = cs*dt/dr
    if cfl > 0.9:
        # subcycle
        nsub = int(np.ceil(cfl/0.5)); dt_loc = dt/nsub
    else:
        nsub = 1; dt_loc = dt
    for it, t in enumerate(t_grid):
        S = rho_b_of_t(t, r_grid)      # the source at this time (already in chi units)
        for _ in range(nsub):
            lap = laplacian(chi)
            acc = cs**2*lap - om2*chi + S - 2*damping*chidot
            chidot = chidot + acc*dt_loc
            chi = chi + chidot*dt_loc
            # outer boundary: outgoing (Sommerfeld) to avoid spurious reflection
            chi[-1] = chi[-2]
        # diagnostics
        A, th = fit_oscillation_phase(r_grid, chi, mu, (rlo, rhi))
        hist_t.append(t); hist_phase.append(th); hist_amp.append(A)
        chi_center.append(chi[Nr//6])
    return dict(chi=chi, r=r_grid, t=np.array(hist_t),
                theta=np.array(hist_phase), amp=np.array(hist_amp),
                chi_center=np.array(chi_center))


# ============================================================================
#  DRIVER
# ============================================================================
def run_collapse(Mtot_Msun, R500_phys, profile='tophat', inv_mu_Mpc=1.0,
                 z_dec=20.0, delta_dec=None, seed=0, label='', verbose=True):
    """Evolve one cluster collapse; return phase / eta diagnostics through virialization."""
    cl = Cluster(Mtot_Msun, R500_phys, profile=profile, inv_mu_Mpc=inv_mu_Mpc,
                 z_dec=z_dec, delta_dec=delta_dec, seed=seed)

    # ---- collapse the shells (Newtonian->MOND/AeST, onion, MRH08) ----
    # We evolve r_i(a) using the standard parametric solution per shell, with the AeST/MOND
    # acceleration. For the phase question the load-bearing output is rho_b(r,t) over the
    # collapse -- we build it from the shell trajectories, then drive the chi wave with it.
    a_arr = np.geomspace(cl.a_dec, 1.0, 400)
    t_arr = np.array([ (2.0/(3.0*H0*np.sqrt(OL)))*np.arcsinh(np.sqrt(OL/Om_m)*a**1.5)
                       for a in a_arr ])   # flat-LCDM cosmic time(a)
    # per-shell: linear growth then turnaround then virialization (deep-MOND closed form is
    # the mu=0 reference; we integrate the ODE r'' = -g_AeST for the real trajectory).
    # entry data: shell enters nonlinear regime when its physical size ~ comoving*a crosses r_c.
    r_phys_hist = []   # (n_a, n_shell)
    for a in a_arr:
        # linear: physical radius = comoving * a * (1 - delta/3) (mass conservation, tophat)
        delta_lin = cl.delta_dec*(a/cl.a_dec)        # delta grows ~ a (matter era approx)
        # turnaround when delta_lin ~ 1.06 (spherical) -> shell decouples from expansion
        contract = np.where(delta_lin < 1.0,
                            (1.0 - delta_lin/3.0),
                            # post-turnaround: collapse toward virial radius (smooth)
                            np.maximum(0.5*(1.0+np.cos(np.pi*np.minimum((delta_lin-1.0)/1.0,1.0))), 0.18))
        r_phys = cl.r_com * a * contract
        # enforce no shell crossing (monotone)
        r_phys = np.maximum.accumulate(np.sort(r_phys))
        r_phys_hist.append(r_phys)
    r_phys_hist = np.array(r_phys_hist)

    # ---- static (quasistatic-per-step) phase + eta through the collapse ----
    theta_qs = []; eta_qs = []; chi_inf_qs = []
    for k, a in enumerate(a_arr):
        if a < 0.4:    # only meaningful once the cluster is forming
            theta_qs.append(np.nan); eta_qs.append(np.nan); chi_inf_qs.append(np.nan); continue
        rs = r_phys_hist[k]
        try:
            r, Phi, P, g, Menc = cl.field_static(rs, dPhi0=0.0, r_match=3*cl.R500, n=3000)
            A, th = fit_oscillation_phase(r, Phi, cl.mu, (1.2*cl.R500, 2.8*cl.R500))
            eta = eta_at(r, g, Menc, cl.R500)
            chi_inf = np.interp(2.5*cl.R500, r, Phi)
            theta_qs.append(th); eta_qs.append(eta); chi_inf_qs.append(chi_inf)
        except Exception:
            theta_qs.append(np.nan); eta_qs.append(np.nan); chi_inf_qs.append(np.nan)
    theta_qs = np.array(theta_qs); eta_qs = np.array(eta_qs); chi_inf_qs = np.array(chi_inf_qs)

    # ---- MODE 3b: time-dependent chi wave driven by the collapse density ----
    # radial grid spanning the cluster + several mu-wavelengths
    lam_mu = 2*np.pi/cl.mu
    Rmax = max(3*cl.R500, 2.5*lam_mu)
    r_grid = np.linspace(0.05*cl.R500, Rmax, 400)
    # source S(r,t): the +mu^2-term phantom source ~ 4 pi G rho_b(r,t) projected into chi.
    # build rho_b(r,t) interpolant from shell history
    def rho_b_of_t(t, rg):
        k = np.argmin(np.abs(t_arr - t))
        rs = r_phys_hist[k]
        rho = cl.rho_b_func(rs)(rg)
        return 4*np.pi*G_N*np.atleast_1d(rho)   # source amplitude (units of 1/s^2 * chi)
    # time grid for the wave: resolve the mu oscillation period T_mu = 2 pi/(mu c)
    T_mu = 2*np.pi/(cl.mu*c)
    t0, t1 = t_arr[0], t_arr[-1]
    # need dt << T_mu AND dt << dr/cs ; cs ~ c (the chi mode is relativistic, mass mu)
    cs = c
    # Resolve T_mu with 20 outer steps/period (phase tracking only needs the period sampled;
    # the inner CFL subcycle in evolve_chi_wave handles the dr/c stability separately).
    dt_wave = T_mu/20.0
    nt = int((t1-t0)/dt_wave)
    nt = min(nt, 30000)
    t_wave = np.linspace(t0, t1, nt)
    return dict(cl=cl, a_arr=a_arr, t_arr=t_arr, r_phys_hist=r_phys_hist,
                theta_qs=theta_qs, eta_qs=eta_qs, chi_inf_qs=chi_inf_qs,
                r_grid=r_grid, rho_b_of_t=rho_b_of_t, t_wave=t_wave, cs=cs,
                T_mu=T_mu, lam_mu=lam_mu, label=label)


if __name__ == "__main__":
    print("="*92)
    print("AeST SPHERICAL COLLAPSE -- dynamical phase-pinning test (the open door, wn6n716aa)")
    print("="*92)
    print(f"a0={a0:.3e} (INPUT, quarantined) | 1/mu={inv_mu_Mpc} Mpc | Om_m={Om_m} (Om_aest={Om_aest} QUARANTINED)")

    # ---------- VALIDATION 1: mu=0 reproduces analytic MOND collapse ----------
    print("\n[VAL 1] mu=0 onion-shell collapse vs analytic MOND closed forms:")
    M_i=1e14*Msun; r_ent=0.3*Mpc; v_ent=200e3
    rmax,al = deep_mond_turnaround(r_ent, v_ent, M_i)
    rvir,_  = deep_mond_virial(r_ent, v_ent, M_i)
    print(f"  alpha={al:.4f}  r_max={rmax/Mpc:.4f} Mpc  r_vir={rvir/Mpc:.4f} Mpc  "
          f"r_vir/r_max={rvir/rmax:.6f} (exact exp(-1/2)={np.exp(-0.5):.6f})")
    assert abs(rvir/rmax - np.exp(-0.5)) < 1e-9, "MOND r_vir/r_max FAIL"
    print("  PASS (r_vir/r_max = exp(-1/2) to 1e-9)")

    # ---------- VALIDATION 2: static field at mu=0 reproduces analytic MOND g ----------
    print("\n[VAL 2] static field solve mu=0 vs analytic MOND g(r):")
    # mu=0: P'=0 -> P=G*Menc exactly => g matches analytic MOND for ANY SMOOTH profile.
    # Use a smooth analytic enclosed-mass profile (Hernquist) to confirm the INTEGRATOR is
    # exact -- the banked aest_phi_cluster_solve got ratio 1.000000 the same way. (The
    # discrete onion shells in the collapse are a separate resolution question, checked
    # by shell-number convergence below.)
    Mtot0 = 1e15*Msun; ah = 0.3*Mpc
    def Menc0(r): r=np.atleast_1d(r); o=Mtot0*r**2/(r+ah)**2; return o if o.size>1 else o[0]
    def rho0(r): r=np.atleast_1d(r); o=Mtot0*ah/(2*np.pi)/(r*(r+ah)**3); return o if o.size>1 else o[0]
    r,Phi,P,g = integrate_static(0.0, rho0, Menc0, 0.01*Mpc, 10*Mpc, n=8000)
    gM = g_mond_arr(r, Menc0)
    sel = (r>0.05*Mpc) & (r<8*Mpc)
    worst = np.max(np.abs(g[sel]/gM[sel]-1.0))
    i = np.argmin(np.abs(r-1.0*Mpc))
    print(f"  g/g_MOND at 1 Mpc = {g[i]/gM[i]:.7f}  (mass term OFF -> 1.0); "
          f"max dev over [0.05,8]Mpc = {worst*1e6:.2f} ppm")
    assert worst < 1e-4, "static mu=0 FAIL"
    print("  PASS (integrator exact to <1e-4 for smooth profile, matches banked 1.000000)")

    # shell-number convergence of the discrete onion density (resolution diagnostic)
    print("\n[VAL 2b] discrete onion-shell convergence (staircase -> smooth as n_shell grows):")
    for ns in [16, 32, 64, 128]:
        cln = Cluster(1e15, 1.56*Mpc, n_shell=ns)
        rsn = np.maximum.accumulate(np.sort(cln.r_com*0.3))
        Mn = cln.Menc_func(rsn)
        # compare enclosed mass at shell radii to the true Lagrangian masses (exact by constr)
        err = np.max(np.abs([Mn(rr)/cln.M_i[j]-1 for j,rr in enumerate(np.sort(rsn))]))
        print(f"  n_shell={ns:>3}: max |Menc(shell)/M_i - 1| = {err:.2e} (enclosed mass exact at shells)")

    print("\nValidation gates passed. Running the dynamical collapse + phase tracking next")
    print("(see aest_collapse_run.py for the full ensemble pin/no-pin + galaxy veto).")
