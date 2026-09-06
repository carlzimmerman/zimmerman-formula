#!/usr/bin/env python3
"""
g03s -- the dust growth law from the candidate's perturbation equations
=======================================================================
g03r bracketed the dust's growth between two models: "Newtonian growth" (the MOND scalar frozen) and "MOND-peculiar growth"
(the scalar's static MOND response established instantly everywhere).  Neither is the candidate's own law.  The candidate's
time-dependent scalar equation follows from pieces already verified in this directory:

  * f34 (time-dependent quadratic action about a background field gradient): the MOND branch propagates with
        omega^2 = c_s^2 k^2 (1 + xi^2 k^2),   c_s^2 = 0.42 J_Y c^2 / |K_2|  ==  c_*^2 J_Y,   c_*^2 = 0.42 c^2/|K_2|,
    i.e. the scalar's time-kinetic coefficient relative to its gradient term is 1/c_*^2 and its gradient coefficient is J_Y(Y);
  * the static law (g03c/g03d/f33): div[J_Y grad psi] = 4 pi G rho, with J_Y g_psi = g_N (g03j: the scalar carries the
    exponential kernel g_psi = a0 y_t exp(-y_t) for y_t <= 1 and saturates at a0/e beyond; J_Y = exp(y_t) - 1);
  * the measure sqrt(-g) ~ a^3 on the time-kinetic term (Hubble friction 3H).
Together, on scales >> xi and << the horizon, in the expanding background:

        (1/c_*^2) (psi_tt + 3 H psi_t)  -  div[ J_Y(|grad psi|) grad psi ]  =  - 4 pi G delta rho_pec          (*)

with J_Y a function of the scalar's OWN gradient y_psi = |grad psi|/a0 (the flux function g_N = Phi(g_psi) of the carrier branch, whose slope
dg_N/dg_psi diverges at saturation y_t = 1 -- an unbounded characteristic speed -- continued linearly with slope 100 there; the
solver is implicit so that region responds instantaneously, as it should).  Two facts follow and are checked:
  (i)  on FLRW (Y = 0) J_Y = 0: the scalar has no gradient term at linear order, so it cannot PROPAGATE -- but it is still
       DRIVEN locally by the source with inertia 1/c_*^2: psi_tt + 3H psi_t = -c_*^2 4 pi G delta rho, whose matter-era solution
       gives a scalar force g_psi/g_N = 0.9 (c_* k t)^2 for a mode k, growing until it saturates at the static MOND value
       (a0 g_N)^{1/2}.  With c_* = 390 km/s (|K_2| = 2.5e5) c_* t_0 = 5.5 Mpc, so the linear regime is boosted by O(1) today on
       scales below ~30 Mpc: THE CANDIDATE'S LINEAR GROWTH IS NOT LambdaCDM-LIKE under (*) -- a growth-rate (f sigma_8)
       liability, conditional on the linear source being the static law's (see the caveat);
  (ii) the static MOND response of a region is complete after the saturation time t_sat ~ (L/c_*)(a0/g_N)^{1/4}, i.e. the
       crossing time at the signal speed c_s = c_* Phi'^{1/2} ~ c_* y_N^{1/4}: fast in galaxies, a few Gyr in clusters, longer
       than a Hubble time on >~ 10 Mpc scales -- but the pre-saturation build-up (i) is already an O(1) boost there.
The scalar (*) is solved two ways.  (a) As a field, on a comoving logarithmic grid (implicit Newton on the banded system, edge
fluxes F = r^2 Phi(psi_r), static-relation boundary fluxes F = G delta M(<r)): this is the reference -- its static limit is
checked against the carrier force (S1) and its RESPONSE TIME t_80(r), the time for the force at r to reach 80% of the static
value after a mass is switched on, is measured (S1b).  (b) Coupled to the collapsing shells, as a per-shell relaxation model of
the same equation: the scalar force at each shell relaxes toward the static carrier value as a critically damped oscillator with
rate omega = beta/t_cross(r), t_cross the crossing-time integral of 1/c_s from the centre along the current profile (c_s = c_* Phi'(g_static)^{1/2} the local signal speed), beta calibrated on (a)'s t_80 (S1b reports the
calibration and its spread over y_N).  The field/shell coupling itself is unstable in the linear regime (the scalar has no
restoring force at zero gradient and integrates the shell-sampled source quadratically), which is why (b) is used for the
dynamics; (b) reproduces (a)'s delays by construction and the static law exactly.  The shells are g03r's converged cold
collisionless dust, feeling g = g_N,pec + g_psi; the atmosphere and the X-COP comparison are g03r's.

Checks that can fail:
  S1 [static limit]  a fixed point mass, no expansion, psi from 0: after 40 crossing times the field solver's psi_r matches the
                     g03j carrier force within 3% at y_N = 30 - 0.01 (saturated to deep MOND);
  S1b [calibration]  the relaxation model's t_80(r) = 3/omega matches the field solver's t_80(r) within a factor 1.5 at
                     y_N = 3.7 and 0.07 with ONE beta (fitted at y_N = 0.23);
  S2 [linear regime] cluster seed x 0.001, assembled baryons off: the derived law's growth at r_L = 10 and 14 Mpc is within 8%
                     of LambdaCDM's D(1)/D(a_i) -- EXPECTED TO FAIL by (i): the failure IS the finding (the enhancement is
                     printed with the analytic estimate 0.9 (c_* k t)^2, k = pi/r_L); the instant law's excess is reported;
  S3 [convergence]   the derived-law cluster run's turned-around mass and 1-Mpc capture change < 15% between N = 400 and 800;
  S4 [reported]      the epoch at which the scalar force at 1 Mpc (cluster) and 30 kpc (galaxy) reaches 80% of the static MOND
                     value -- the MOND-activation redshift of each scale;
  S5 [reported]      the dust captured under the derived law relative to the two brackets, both systems;
  S6 [reported]      the window (galaxy 100 kpc <= 14%, cluster 1 Mpc >= 32% of the derived-law cold reference) and the best
                     |K_2| against X-COP with its trend, under the derived law, both footings.
"""
import numpy as np, math, time, sys, json, importlib.util
spec = importlib.util.spec_from_file_location("g03r", "g03r_converged_collapse_adaptive_shells.py"); R = importlib.util.module_from_spec(spec); spec.loader.exec_module(R)
G, c, MSUN, kpc, Mpc, A0, H0, Om, OL, Ob, Od, rho_c = R.G, R.c, R.MSUN, R.kpc, R.Mpc, R.A0, R.H0, R.Om, R.OL, R.Ob, R.Od, R.rho_c
H_of, SYSTEMS, baryon_M, atmosphere, M_at, nu_tot, XCOP_R, XCOP_ETA = R.H_of, R.SYSTEMS, R.baryon_M, R.atmosphere, R.M_at, R.nu_tot, R.XCOP_R, R.XCOP_ETA
FAILS = []
def check(name, ok, detail=""):
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f"   ({detail})" if detail else ""), flush=True)
    if not ok: FAILS.append(name)
JY_CAP = 100.0
BETA = 1.0                                                                                          # relaxation-rate prefactor omega = BETA c_s/r; calibrated in S1b
from scipy.linalg import solve_banded
# the carrier's flux function: g_N = Phi(g_psi) on the branch y_t <= 1 (g_psi = a0 y e^-y, g_N = a0 y (1 - e^-y)), continued linearly with slope JY_CAP where its slope reaches JY_CAP
_y = np.linspace(0, 1, 200001); _sl = ((1 - np.exp(-_y)) + _y*np.exp(-_y))/np.maximum(np.exp(-_y)*(1 - _y), 1e-300); _imax = int(np.argmax(_sl >= JY_CAP)) if np.any(_sl >= JY_CAP) else len(_y) - 1
_y = _y[:_imax + 1]; S_TAB = _y*np.exp(-_y); G_TAB = _y*(1 - np.exp(-_y)); SL_TAB = np.minimum(_sl[:_imax + 1], JY_CAP); S_MAX, G_MAX = S_TAB[-1], G_TAB[-1]
def Phi(s, a0):
    """g_N as a function of the scalar's own gradient s (signed), in the carrier branch, linear beyond the cap."""
    u = np.abs(s)/a0; g = np.where(u <= S_MAX, np.interp(np.minimum(u, S_MAX), S_TAB, G_TAB), G_MAX + JY_CAP*(u - S_MAX)); return np.sign(s)*a0*g
def dPhi(s, a0):
    u = np.abs(s)/a0; return np.where(u <= S_MAX, np.interp(np.minimum(u, S_MAX), S_TAB, SL_TAB), JY_CAP)
def Phi_inv(gN, a0):
    """the static scalar gradient for a Newtonian field g_N (inverse of Phi)"""
    u = np.abs(gN)/a0; s = np.where(u <= G_MAX, np.interp(np.minimum(u, G_MAX), G_TAB, S_TAB), S_MAX + (u - G_MAX)/JY_CAP); return np.sign(gN)*a0*s
def gpsi_static(gN, a0): return Phi_inv(gN, a0)
def JY_of_gradient(ypsi): return Phi(ypsi, 1.0)/np.maximum(ypsi, 1e-300)

class Scalar:
    """psi(x, t) on a comoving log grid, cell-centred; edge fluxes F = r^2 Phi(psi_r); implicit (backward-Euler in the velocity, Newton on the
    banded system) so the saturated core (unbounded characteristic speed) is handled as the instantaneous response it is."""
    def __init__(self, xmin, xmax, ncell, K2abs, a0):
        self.xe = np.geomspace(xmin, xmax, ncell + 1); self.x = np.sqrt(self.xe[1:]*self.xe[:-1]); self.n = ncell
        self.psi = np.zeros(ncell); self.psid = np.zeros(ncell); self.cs2 = 0.42*c**2/K2abs; self.a0 = a0; self.newton_max = 0
    def _fluxes(self, psi, a, Fin, Fout):
        r_e = a*self.xe; dx = a*np.diff(self.x); s = np.diff(psi)/dx
        F = np.empty(self.n + 1); F[1:-1] = r_e[1:-1]**2*Phi(s, self.a0); F[0] = Fin; F[-1] = Fout
        return F, s, dx, r_e
    def step(self, a, dt, drho, Fin, Fout, H):
        n = self.n; A = 1/dt**2 + 3*H/dt; psi0 = self.psi.copy(); rhs = self.psid/dt - self.cs2*4*math.pi*G*drho
        psi = psi0.copy()
        for it in range(30):
            F, s, dx, r_e = self._fluxes(psi, a, Fin, Fout); k = 3.0/(r_e[1:]**3 - r_e[:-1]**3)
            res = (psi - psi0)*A - self.cs2*k*np.diff(F) - rhs
            dP = dPhi(s, self.a0); w = r_e[1:-1]**2*dP/dx                                            # dF_e/dpsi_right on interior edges
            diag = A + self.cs2*k*(np.concatenate([w, [0.0]]) + np.concatenate([[0.0], w]))
            upper = -self.cs2*k[:-1]*w; lower = -self.cs2*k[1:]*w
            ab = np.zeros((3, n)); ab[0, 1:] = upper; ab[1] = diag; ab[2, :-1] = lower
            dpsi = solve_banded((1, 1), ab, -res); psi = psi + dpsi
            if np.max(np.abs(dpsi)) <= 1e-7*max(np.max(np.abs(psi)), 1e-30) + 1e-40: break
        self.newton_max = max(self.newton_max, it + 1)
        self.psid = (psi - psi0)/dt; self.psi = psi
    def force_at(self, r, a, Fin):
        """the scalar force psi_r at physical radii r; inside x_min the static relation with the inner flux"""
        F, s, dx, r_e = self._fluxes(self.psi, a, Fin, 0.0); re_ = r_e[1:-1]
        out = np.interp(r, re_, s, left=np.nan, right=s[-1]); inside = np.isnan(out)
        if inside.any(): out[inside] = Phi_inv(Fin/np.maximum(r[inside], 1e-3*r_e[0])**2, self.a0)
        return out

def run_dyn(system, K2abs, growth="dynamic", N=400, ncell=300, zi=50.0, seed_fac=1.0, rcore_frac=0.02, a0=A0["canonical"], avg_from=0.9, af=0.5, probe=None, max_steps=int(6e6), Mb_scale=1.0, dtH=0.02, diag=None):
    """g03r's converged cold collisionless shells with the dust feeling g_N,pec + the scalar force from (*):
    growth = 'newton' (scalar frozen), 'instant' (static MOND response each step), 'dynamic' (the derived law)."""
    S = SYSTEMS[system]; Mb0, Rap, zc, kind = S["Mb0"], S["R"], S["zc"], S["kind"]
    Mshare = Mb0*Od/Ob; Rshare = (Mshare/(Od*rho_c*4*math.pi/3))**(1/3); RL = 2*Rshare; rcore = rcore_frac*Rap; ai = 1/(1 + zi); gext = R.GEXT_FRAC*a0
    Mb0 = Mb0*Mb_scale                                                                              # the linear-regime test switches the assembled baryons off (Mb_scale ~ 0); the share and the shells are unchanged
    rL_in = max(0.01*Rshare, 2.0*rcore*(1 + zi)); edges_L = np.geomspace(rL_in, RL, N + 1)
    delta_0 = seed_fac*1.686*(1 + zc)/(1 + zi); dL = min(delta_0*Rshare/edges_L[0], 1.0)
    m = Od*rho_c*(4*math.pi/3)*(edges_L[1:]**3 - edges_L[:-1]**3); M_lump = Od*rho_c*(4*math.pi/3)*edges_L[0]**3   # Lagrangian (mean) mass: the seed's contrast is carried by the displacements, including the lump's share of the mean interior contrast below (g03r's lump carried an extra (1 + dL) on top of that -- a double count that over-grew the innermost shells by up to 50%)
    rc_ = np.sqrt(edges_L[1:]*edges_L[:-1]); Menc0 = np.cumsum(m) - 0.5*m + M_lump; dbar_in = np.minimum(delta_0*Rshare/rc_, 1.0)
    dloc = np.gradient(rc_**3*dbar_in, rc_)/(3*rc_**2); din = np.where(rc_ < Rshare, dloc, 0.0)
    ML0 = M_lump; excess = np.sum(din*m) + dL*ML0; din = np.where(rc_ < Rshare, din, -excess/np.sum(m[rc_ >= Rshare])); dm = (np.cumsum(din*m) + dL*ML0)/Menc0
    r = ai*rc_*(1 - dm/3); v = H_of(ai)*r*(1 - dm/3); a = ai; rmax = r.copy(); step = 0
    apertures = np.array([Rap, 0.2*Rap]); Mavg = np.zeros(2); nav = 0
    sc = None; cs2_ = 0.42*c**2/K2abs; gpsi = np.zeros(N); gpsid = np.zeros(N)                       # per-shell scalar force and its rate (the relaxation model)
    probe_log = []
    def dM_of(rq, a, rs, Menc_d):
        """peculiar (overdensity) mass inside physical radii rq, g03r's mass-conserving bookkeeping"""
        Mb = Mb0*a**3/(a**3 + af**3); rho_bg = Om*rho_c*a**-3
        r_lump = rs[0]*edges_L[0]/rc_[0]                                                                   # the lump's edge follows the first shell; the lump is uniform inside it (a point lump made the inner scalar cells a void around a compact mass)
        Md_q = np.where(rq < rs[0], M_lump*np.minimum(1.0, (rq/max(r_lump, 1e-30))**3), np.interp(rq, rs, Menc_d, right=Menc_d[-1]))
        return Md_q*(Om/Od) - rho_bg*(4*math.pi/3)*rq**3 + baryon_M(rq, Mb, kind) - np.minimum(Mb, (Ob/Od)*Md_q)
    t0 = time.time()
    while a < 1.0:
        order = np.argsort(r); rs = r[order]; Menc_d = np.cumsum(m[order]) - 0.5*m[order] + M_lump
        dM = dM_of(rs, a, rs, Menc_d); gN = G*dM/rs**2; rho_bg = Om*rho_c*a**-3; H = H_of(a)
        if growth == "newton": g = gN
        elif growth == "instant": g = gN*nu_tot(np.hypot(gN, gext)/a0)
        else:
            gt = np.hypot(gN, gext); g_static = Phi_inv(gt, a0)*gN/gt; cs_sh = np.sqrt(cs2_*dPhi(Phi_inv(gt, a0), a0))   # target (the static carrier force with the same large-scale external-field regularisation as the instant law: the boost of the total field, applied to the peculiar one) and local signal speed at each (sorted) shell
            tcr = rs[0]/cs_sh[0] + np.concatenate([[0.0], np.cumsum(np.diff(rs)/(0.5*(cs_sh[1:] + cs_sh[:-1])))])   # crossing time from the centre to each shell along the current profile
            om = BETA/tcr
            g = gN + gpsi[order]
        acc_s = -(4*math.pi*G/3)*rho_bg*rs + OL*H0**2*rs - g; acc = np.empty(N); acc[order] = acc_s
        dr_min = max(np.min(np.diff(rs)), 0.01*rcore); vmax = np.max(np.abs(v)) + 1.0
        dt = min(0.25*dr_min/vmax, dtH/H, 0.1*math.sqrt(dr_min/(np.max(np.abs(acc)) + 1e-30)))
        if growth == "dynamic":                                                                              # exact critically-damped update toward the target over dt, then the Hubble damping
            x = gpsi[order] - g_static; xd = gpsid[order]; e = np.exp(-om*dt)
            xn = e*(x + (xd + om*x)*dt); xdn = e*(xd - om*(xd + om*x)*dt)*np.exp(-3*H*dt)
            gpsi[order] = g_static + xn; gpsid[order] = xdn
        v += acc*dt; r += v*dt; hit = r < rcore; r[hit] = 2*rcore - r[hit]; v[hit] = -v[hit]
        a += a*H*dt; rmax = np.maximum(rmax, r); step += 1
        if a >= avg_from and step % 20 == 0: Mavg += np.array([M_lump + np.sum(m[r < ap]) for ap in apertures]); nav += 1
        if probe is not None and step % 200 == 0:
            rp = np.asarray(probe); dMp = dM_of(rp, a, rs, Menc_d); gNp = G*dMp/rp**2
            gp = np.interp(rp, rs, gpsi[order]) if growth == "dynamic" else (gNp*(nu_tot(np.hypot(gNp, gext)/a0) - 1) if growth == "instant" else 0*gNp)
            probe_log.append((a, gNp.copy(), gp.copy(), gpsi_static(gNp, a0)))
        if step >= max_steps: print(f"      ABORT {max_steps} steps at a = {a:.3f}", flush=True); break
    Mavg /= max(nav, 1); collapsed = r < 0.5*rmax; r_ta = float(np.max(rmax[collapsed])) if collapsed.any() else float("nan"); Macc = float(np.sum(m[collapsed]) + M_lump)
    dbar_final = None
    return dict(frac=Mavg/Mshare, r_ta=r_ta, Macc=Macc, Mshare=Mshare, steps=step, secs=time.time() - t0, probe=probe_log, r=r.copy(), rc_=rc_, m=m, M_lump=M_lump, Rshare=Rshare)

def growth_factor(a_i, a_f):
    """LambdaCDM linear growth D(a_f)/D(a_i) (integral form)."""
    def D(a):
        aa = np.linspace(1e-4, a, 20000); E = np.sqrt(Om*aa**-3 + OL); return 2.5*Om*E[-1]*np.trapz(1/(aa*E)**3, aa)
    return D(a_f)/D(a_i)

if __name__ == "__main__":
    print("=" * 110); print("g03s -- the dust growth law from the candidate's perturbation equations"); print("=" * 110, flush=True)
    T0 = time.time(); a0 = A0["canonical"]; K2 = 2.5e5
    print(f"  c_* = (0.42)^1/2 c/|K_2|^1/2 = {math.sqrt(0.42/K2)*c/1e3:.0f} km/s at |K_2| = {K2:.1e}; deep-MOND sound speed c_s = c_* y_N^1/4: {math.sqrt(0.42/K2)*c/1e3*1e-3**0.25:.0f} km/s at y_N = 1e-3, {math.sqrt(0.42/K2)*c/1e3*0.1**0.25:.0f} km/s at 0.1", flush=True)
    # ---- S1 static limit ----
    M = 1e14*MSUN; sc = Scalar(20*kpc, 3*Mpc, 400, K2, a0)
    rq = np.array([50, 200, 800, 1500])*kpc; gst = gpsi_static(G*M/rq**2, a0)
    cs_edge = np.sqrt(sc.cs2*dPhi(gpsi_static(G*M/sc.xe[1:-1]**2, a0), a0)); tcross = float(np.sum(np.diff(sc.x)/cs_edge))
    dt = 0.02*3.156e16; t = 0.0; nst = 0; t80 = np.full(4, np.nan); hist = []
    while t < 40*tcross:
        sc.step(1.0, dt, np.zeros(sc.n), G*M, G*M, 0.5/tcross); t += dt; nst += 1
        ratio = sc.force_at(rq, 1.0, G*M)/gst; hist.append((t, ratio.copy()))
        for j in range(4):
            if np.isnan(t80[j]) and ratio[j] >= 0.8: t80[j] = t
    gps = sc.force_at(rq, 1.0, G*M); dev = np.abs(gps/gst - 1)
    check("S1 [static limit] point mass 1e14 Msun, no expansion, psi from 0, implicit steps of 0.02 Gyr for 40 crossing times: the field solver's psi_r matches the g03j carrier force within 3% at r = 50, 200, 800, 1500 kpc (y_N = 60 - 0.07: saturated to deep MOND)", np.all(dev < 0.03), f"psi_r/g_carrier = {np.round(gps/gst, 4).tolist()}, y_N = {np.round(G*M/rq**2/a0, 3).tolist()}, crossing time {tcross/3.156e16:.1f} Gyr, {nst} steps, Newton iterations <= {sc.newton_max}")
    # S1b: the relaxation model's t_80 = 3/omega, omega = BETA/t_cross(r), t_cross = the crossing-time integral from the centre along the static profile; BETA fitted at r = 800 kpc (y_N = 0.23)
    rr_ = np.geomspace(20*kpc, 3*Mpc, 3000); cs_r = np.sqrt(sc.cs2*dPhi(gpsi_static(G*M/rr_**2, a0), a0)); tcr_r = rr_[0]/cs_r[0] + np.concatenate([[0.0], np.cumsum(np.diff(rr_)/(0.5*(cs_r[1:] + cs_r[:-1])))])
    tcr_q = np.interp(rq, rr_, tcr_r); t80_model_unit = 3.0*tcr_q                                          # BETA = 1 prediction
    BETA_fit = float(t80_model_unit[2]/t80[2]); globals()["BETA"] = BETA_fit
    ratio_t = t80_model_unit/BETA_fit/t80
    print(f"    S1b: field-solver t_80 at r = 50, 200, 800, 1500 kpc = {np.round(t80/3.156e16, 3).tolist()} Gyr; crossing-time model with BETA = {BETA_fit:.2f}: {np.round(t80_model_unit/BETA_fit/3.156e16, 3).tolist()} Gyr; model/field = {np.round(ratio_t, 2).tolist()}", flush=True)
    check("S1b [calibration] with one BETA (fitted at y_N = 0.23) the crossing-time relaxation model's t_80 matches the field solver's within a factor 1.5 at y_N = 3.7 and 0.07 as well", np.all((ratio_t[1:] > 1/1.5) & (ratio_t[1:] < 1.5)), f"BETA = {BETA_fit:.2f}, model/field = {np.round(ratio_t, 2).tolist()}")
    # ---- S2 linear regime ----
    print("  S2: cluster seed x 0.001, growth of the enclosed contrast delta_bar(<r_L) from z_i = 50 to 0 vs LambdaCDM D(1)/D(a_i)", flush=True)
    Dfac = growth_factor(1/51, 1.0); res = {}
    o0 = run_dyn("cluster", K2, growth="newton", N=400, seed_fac=0.0, Mb_scale=1e-6)                                # zero-seed control: numerical drift and the half-shell measurement bias, subtracted below
    def dbar_of(o, rL): sel = o["rc_"] <= rL; return (o["rc_"][sel][-1]/o["r"][sel][-1])**3 - 1
    for gr in ["newton", "instant", "dynamic"]:
        o = run_dyn("cluster", K2, growth=gr, N=400, seed_fac=0.001, Mb_scale=1e-6)
        out = []
        for rL in [3*Mpc, 10*Mpc, 14*Mpc]:
            db0 = min(0.001*1.686*1.3/51*o["Rshare"]/rL, 1.0); out.append((dbar_of(o, rL) - dbar_of(o0, rL))/db0)
        res[gr] = out; print(f"    {gr:8s}: delta_bar(1)/delta_bar(a_i) at r_L = 3, 10, 14 Mpc = {np.round(out, 2).tolist()}  (LambdaCDM {Dfac:.2f}); {o['steps']} steps, {o['secs']:.0f}s", flush=True)
    cst = math.sqrt(0.42/K2)*c*13.8e9*3.156e7; print(f"    analytic (i): g_psi/g_N = 0.9 (c_* k t_0)^2 with c_* t_0 = {cst/Mpc:.1f} Mpc, k = pi/r_L: {[round(0.9*(cst*math.pi/(x*Mpc))**2, 2) for x in (3, 10, 14)]} at r_L = 3, 10, 14 Mpc (before saturation at (a0 g_N)^1/2)", flush=True)
    check("S2 [linear regime] the derived law's linear growth at r_L = 10 and 14 Mpc is within 8% of LambdaCDM's D(1)/D(a_i) (zero-seed drift subtracted) -- expected to FAIL by (i); the newton law must pass the same test (integrator control)", all(abs(x/Dfac - 1) < 0.08 for x in res["dynamic"][1:]) and all(abs(x/Dfac - 1) < 0.08 for x in res["newton"][1:]), f"derived/LCDM = {np.round(np.array(res['dynamic'])/Dfac, 3).tolist()} (3, 10, 14 Mpc), instant/LCDM = {np.round(np.array(res['instant'])/Dfac, 3).tolist()}, newton/LCDM = {np.round(np.array(res['newton'])/Dfac, 3).tolist()}")
    check("S2c [integrator control] the Newtonian law reproduces LambdaCDM's linear growth within 8% at r_L = 3, 10, 14 Mpc", all(abs(x/Dfac - 1) < 0.08 for x in res["newton"]), f"newton/LCDM = {np.round(np.array(res['newton'])/Dfac, 3).tolist()}")
    # ---- S3 convergence + S4 activation + S5 brackets ----
    print("  S3-S5: the derived law on the model cluster (z_c = 0.3) and galaxy (z_c = 1), |K_2| = 2.5e5, canonical", flush=True)
    DYN = {}; PROBE = {"cluster": [1000*kpc, 200*kpc], "galaxy": [30*kpc, 100*kpc]}
    for sysname in ["cluster", "galaxy"]:
        for (N, nc) in [(400, 300), (800, 300)]:
            o = run_dyn(sysname, K2, growth="dynamic", N=N, ncell=nc, probe=PROBE[sysname]); DYN[(sysname, N, nc)] = o
            print(f"    {sysname:8s} derived law N = {N}: captured/share {o['frac'][0]:.4f} / {o['frac'][1]:.4f}, turned around {o['Macc']/o['Mshare']:.3f}, r_ta {o['r_ta']/kpc:.0f} kpc  ({o['steps']} steps, {o['secs']:.0f}s)", flush=True)
    def spread(v): v = np.array(v, float); return float((v.max() - v.min())/max(v.max(), 1e-12))
    s3 = [spread([DYN[("cluster", 400, 300)]["Macc"], DYN[("cluster", 800, 300)]["Macc"]]), spread([DYN[("cluster", 400, 300)]["frac"][0], DYN[("cluster", 800, 300)]["frac"][0]])]
    check("S3 [convergence] derived-law cluster: turned-around mass and 1-Mpc capture change < 15% between N = 400 and 800", max(s3) < 0.15, f"spreads {np.round(s3, 3).tolist()}")
    for sysname in ["cluster", "galaxy"]:
        pl = [p for p in DYN[(sysname, 800, 300)]["probe"] if p[0] >= 0.1 and np.all(p[1] > 0)]; aa = np.array([p[0] for p in pl]); ratio = np.array([p[2]/np.maximum(p[3], 1e-30) for p in pl])
        for j, rp in enumerate(PROBE[sysname]):
            act = aa[ratio[:, j] >= 0.8]; z_act = (1/act[0] - 1) if act.size else float("nan")
            print(f"    S4 {sysname} at {rp/kpc:.0f} kpc: scalar force / static carrier force = {np.interp([0.1, 0.3, 0.5, 0.8, 1.0], aa, ratio[:, j]).round(2).tolist()} at a = 0.1, 0.3, 0.5, 0.8, 1; reaches 80% at z = {z_act:.2f}" + ("" if act.size else " (never)"), flush=True)
    check("S4 [reported] the scalar force reaches 80% of its static MOND value before a = 1 at 30 kpc in the galaxy and at 200 kpc in the cluster", all(np.any(np.array([p[2][j]/max(p[3][j], 1e-30) for p in DYN[(s_, 800, 300)]["probe"] if p[0] >= 0.1 and np.all(p[1] > 0)]) >= 0.8) for s_, j in [("galaxy", 0), ("cluster", 1)]))
    BR = {}
    for sysname in ["cluster", "galaxy"]:
        for gr in ["newton", "instant"]:
            o = run_dyn(sysname, K2, growth=gr, N=800); BR[(sysname, gr)] = o
        d = DYN[(sysname, 800, 300)]
        print(f"    S5 {sysname}: turned-around mass (shares) newton {BR[(sysname, 'newton')]['Macc']/d['Mshare']:.3f} | DERIVED {d['Macc']/d['Mshare']:.3f} | instant {BR[(sysname, 'instant')]['Macc']/d['Mshare']:.3f};  captured inside {SYSTEMS[sysname]['R']/kpc:.0f} kpc: {BR[(sysname, 'newton')]['frac'][0]:.3f} | {d['frac'][0]:.3f} | {BR[(sysname, 'instant')]['frac'][0]:.3f}", flush=True)
    check("S5 [reported] the derived law lies between the two brackets in the turned-around mass for both systems", all(min(BR[(s_, 'newton')]['Macc'], BR[(s_, 'instant')]['Macc']) <= DYN[(s_, 800, 300)]['Macc'] <= max(BR[(s_, 'newton')]['Macc'], BR[(s_, 'instant')]['Macc']) for s_ in ["cluster", "galaxy"]))
    # ---- S6 window and X-COP under the derived law (both footings; the derived-law cold reference at |K_2| = 2.5e5 is used for all rows) ----
    K2S = [5e4, 1e5, 2e5, 3e5, 5e5, 1e6, 3e6]; TABLE = {}; XS = {}
    Mb1 = SYSTEMS["cluster"]["Mb0"]/(1 + 0.5**3); lr = np.log10(XCOP_R/kpc); trend_data = float(np.polyfit(lr, np.log10(XCOP_ETA - 1), 1)[0])
    for foot, a0f in A0.items():
        refc = run_dyn("cluster", K2, growth="dynamic", N=400, a0=a0f); refg = run_dyn("galaxy", K2, growth="dynamic", N=400, a0=a0f)
        print(f"  S6 window table, derived law, {foot} footing: atmosphere mass / derived-law cold capture inside the apertures (cold reference: galaxy {refg['frac'][0]:.3f}/{refg['frac'][1]:.3f}, cluster {refc['frac'][0]:.3f}/{refc['frac'][1]:.3f} of the share; turned around {refg['Macc']/refg['Mshare']:.3f}, {refc['Macc']/refc['Mshare']:.3f})", flush=True)
        print("     |K_2| | galaxy 100 kpc | galaxy 10 kpc | cluster 1 Mpc | cluster 200 kpc | H [kpc]", flush=True)
        rows = []
        for K in K2S:
            ag = atmosphere("galaxy", K, refg["Macc"], refg["r_ta"], a0=a0f); ac = atmosphere("cluster", K, refc["Macc"], refc["r_ta"], a0=a0f)
            row = [M_at(ag, 100*kpc)/max(refg["frac"][0]*refg["Mshare"], 1e-30), M_at(ag, 10*kpc)/max(refg["frac"][1]*refg["Mshare"], 1e-30), M_at(ac, Mpc)/max(refc["frac"][0]*refc["Mshare"], 1e-30), M_at(ac, 0.2*Mpc)/max(refc["frac"][1]*refc["Mshare"], 1e-30)]
            rows.append(row); print(f"     {K:7.0e} |        {row[0]:7.3f} |       {row[1]:7.3f} |       {row[2]:7.3f} |         {row[3]:7.3f} | {ag['H']/kpc:7.0f}", flush=True)
        TABLE[foot] = rows; win = [K for K, row in zip(K2S, rows) if row[0] <= 0.14 and row[2] >= 0.32]; print(f"    window ({foot}): {win if win else 'NONE'}", flush=True)
        if foot == "canonical":
            best = None
            for K in np.geomspace(5e4, 1e6, 14):
                ac = atmosphere("cluster", K, refc["Macc"], refc["r_ta"], a0=a0f); Mb_r = baryon_M(XCOP_R, Mb1, "cluster"); Md_r = np.interp(XCOP_R, ac["r"], ac["Md"]); yb = G*Mb_r/XCOP_R**2/a0f
                eta = (Mb_r + Md_r)*nu_tot(G*(Mb_r + Md_r)/XCOP_R**2/a0f)/(nu_tot(yb)*Mb_r); sup = (eta - 1)/(XCOP_ETA - 1)
                rms = float(np.sqrt(np.mean(np.log10(np.maximum(sup, 1e-6))**2))); trend = float(np.polyfit(lr, np.log10(np.maximum(eta - 1, 1e-6)), 1)[0])
                if best is None or rms < best[1]: best = (K, rms, trend, sup)
            XS[foot] = best; print(f"    X-COP under the derived law: best |K_2| = {best[0]:.2e} (H = {0.42*math.e*c**2/(best[0]*a0f)/kpc:.0f} kpc), rms {best[1]:.2f} dex, trend {best[2]:+.2f} vs data {trend_data:+.2f}; supplied {np.round(best[3], 2).tolist()}", flush=True)
    check("S6 [reported] under the derived law a window exists at both footings (galaxy 100 kpc <= 14%, cluster 1 Mpc >= 32%)", all(any(r[0] <= 0.14 and r[2] >= 0.32 for r in TABLE[f]) for f in A0), json.dumps({f: [K for K, r in zip(K2S, TABLE[f]) if r[0] <= 0.14 and r[2] >= 0.32] for f in A0}))
    check("S6b [reported] under the derived law the best |K_2| for X-COP matches the residual to < 0.15 dex rms with the data's trend within 0.2", XS["canonical"][1] < 0.15 and abs(XS["canonical"][2] - trend_data) < 0.2, f"best {XS['canonical'][0]:.1e}, rms {XS['canonical'][1]:.2f}, trend {XS['canonical'][2]:+.2f} vs {trend_data:+.2f}")
    print(f"\n  caveats: (*) is assembled from f34's coefficients and the static law, not re-derived from the covariant action in the expanding background -- in particular the LINEAR source 4 pi G delta rho is inherited from the static law (where it arises through the clock's spatial gradient tracking the potential, f33); if the candidate's FLRW linear theory couples the scalar only through the metric (as in AeST's published linear analysis) the boost of (i) is absent and the linear growth is LambdaCDM's -- deciding this is the next gate and the candidate's cosmology stands or falls on it; the flux function is the g03j carrier branch continued with slope {JY_CAP:.0f} at saturation; the dynamics uses the per-shell relaxation model calibrated on the field solver (BETA = {BETA:.2f}); the scalar starts unexcited at z_i = 50; the relaxation target carries the 0.02 a0 large-scale external field in its argument exactly as the instant law does (without it the deep-MOND target is unbounded at small g_N); spherical; the AeST reading (the dust sources the scalar); |K_2| = 2.5e5 for the dynamics (the X-COP value), the atmosphere scanned in |K_2|.  total {time.time() - T0:.0f}s")
    print(f"\nRESULT: {len(FAILS)} FAIL" + (f" -> {FAILS}" if FAILS else ""))
    sys.exit(1 if FAILS else 0)
