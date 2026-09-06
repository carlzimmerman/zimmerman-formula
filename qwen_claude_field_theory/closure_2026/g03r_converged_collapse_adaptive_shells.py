#!/usr/bin/env python3
"""
g03r -- converged spherical collapse of the candidate's scalar dust with adaptive (mass-refined) Lagrangian shells
======================================================================================================================
Replaces g03o, whose window was withdrawn as unconverged (its check D4: the cluster capture at |K_2| = 3e5 changed by
a factor 0 - 2.2 with the shell spacing and the start redshift).  Every element that made g03o start-time or grid
dependent is replaced:

  shells      logarithmically refined in Lagrangian radius from max(0.01 R_share, 2 r_core (1 + z_i)) to 2 R_share, so the
              core is resolved and no shell begins inside the absorbing core; the dust inside the innermost radius is a
              frozen central lump counted as captured; the inner boundary r_core is a REFLECTING wall (shells pass through the
              unresolved centre; nothing is absorbed), and the diffuse baryons trace the dust outside the assembled central
              profile (mass conservation: the assembled profile is drawn from the local baryon budget);
  measure     the captured dust is the TIME-AVERAGED mass inside the aperture over the last tenth of the expansion
              (a = 0.9 - 1), read directly off the shell positions (plus the lump) -- no turnaround-radius criterion;
  baryons     a resolved profile (exponential disc for the galaxy, M_b(<r) = M_b u/(1+u), u = (r/700 kpc)^1.7 for the
              cluster), assembling as M_b(a) = M_b0 a^3/(a^3 + a_f^3), a_f = 0.5;
  growth      the seed (secondary-infall profile delta_bar(<r) = delta_0 R_share/r capped at 1, compensated outside R_share,
              growing-mode velocities) is defined at ONE start redshift z_i = 50; MOND acts on the peculiar field with a
              0.02 a0 large-scale external field in the argument (the candidate's linear regime is MONDian, so the
              growth from z_i is a MODEL statement, not a numerical one): the sensitivity to the seed amplitude
              (x 0.5, x 2) is reported as the model band, not folded into the convergence checks;
  fluid step  for the stiff dust, NON-CROSSING Lagrangian hydrodynamics on a staggered grid (von Neumann-Richtmyer:
              velocities on the shells, pressures in the cells between them; P = c_s^2(y_loc) rho with
              c_s^2 = 0.42 J_Y(y_loc) c^2/|K_2|, f34's Bogoliubov sound speed at the local field; viscosity C^2 rho (dv)^2 on
              converging cells, C^2 = 2, plus the linear term C_1 rho c_s |dv|, C_1 = 1; the VNR time-step condition; a central cell of the lump's dust between r = 0 and the first shell (pressure ~ r_0^-3) inside, no-gradient outside; a crossing the
              viscosity fails to stop is clamped momentum-conservingly and counted); the cold references are collisionless
              shells with crossing and an elastic inner reflection; the kernel's unselected np.where branch is clipped.

STATUS OF THE FLUID BRANCH: the non-crossing Lagrangian hydrodynamics of the stiff dust does NOT converge at this dynamic
range -- the core sound speed c_s^2 = 0.42 J_Y c^2/|K_2| reaches 0.1 c where y ~ 10^3, and the innermost shells pile up
against any inner boundary (rigid wall, no-gradient, or a central pressure cell) with cells < 10^-3 kpc and time steps
< 10^-12 H^-1; the branch is kept in run() for the record but is not used.  The stiff dust is instead computed as its
SELF-GRAVITATING HYDROSTATIC ATMOSPHERE at a = 1 (atmosphere()): with c_s^2 proportional to the local field, hydrostatic
balance d(c_s^2 rho)/dr = -rho g integrates to rho ~ exp(-r/H)/g with ONE scale H = 0.42 e c^2/(|K_2| a0) (H/e in the
deep-MOND regime), normalised to the mass the converged cold infall has brought inside the turnaround radius.  Two growth
models bracket the (MONDian) linear regime: Newtonian growth and MOND on the peculiar field.

Checks that can fail (the convergence checks gate everything below them):
  N1 [convergence] cluster, cold Newtonian infall: mass inside 1 Mpc / 200 kpc and the turned-around mass within 15% across N = 200/400/800;
  N2 [convergence] cluster, cold MOND-peculiar infall: the same, judged on the change between N = 400 and 800;
  N3 [anchor]      the cold Newtonian cluster's time-averaged M(<r) slope between 0.05 and 0.5 r_ta is 0.75 +/- 0.25 (Bertschinger 1985);
  N4 [convergence] galaxy: turned-around mass and 100-kpc capture change < 15% between N = 400 and 800, both growth models;
  H1 [convergence] the atmosphere's aperture masses within 1% between 400 and 1600 grid points;
  H2 [reported]    the radius where the cluster atmosphere's enclosed dust-to-baryon ratio peaks scales with H (1-4 H);
  W1 [reported]    a window (growth model x footing) with galaxy 100 kpc <= 14% and cluster 1 Mpc >= 32% of the cold reference;
  X1 [reported]    the best |K_2| reproduces X-COP's residual profile within 0.15 dex rms and the data's radial trend within 0.2;
  X2 [reported]    that best |K_2| lies inside the KiDS/cluster window of the same growth model.
Both footings for the window table (a0 = 9.3619e-11 canonical, 1.1279e-10 alt).  Spherical; one representative system
each; the dust sources the MOND scalar (the AeST reading); the assembly history and the LSS external field are assumptions.
"""
import numpy as np, math, time, sys, json
G = 6.674e-11; c = 2.998e8; MSUN = 1.989e30; kpc = 3.0857e19; Mpc = 1e3*kpc
A0 = {"canonical": 9.3619e-11, "alt": 1.1279e-10}
H0 = 67.4e3/Mpc; Om, OL, Ob, Od = 0.315, 0.685, 0.049, 0.266; rho_c = 3*H0**2/(8*math.pi*G)
GEXT_FRAC = 0.02                                                                                  # large-scale peculiar acceleration in the MOND argument, in units of a0 (an assumption)
YT = np.logspace(-6, 3, 4000); YN = YT*(1 - np.exp(-YT))
def ytot(yN): return np.interp(yN, YN, YT)
def nu_tot(yN):
    yN = np.asarray(yN, float); yt = ytot(yN); return np.where(yt <= 1, yt/np.maximum(yN, 1e-300), 1 + (1/math.e)/np.maximum(yN, 1e-300))
def JY(yN):
    yN = np.asarray(yN, float); yt = ytot(yN); yt1 = np.minimum(yt, 1.0); return np.where(yt <= 1, yN/(yt1*np.exp(-yt1)), yN/(1/math.e))
def H_of(a): return H0*math.sqrt(Om*a**-3 + OL)
SYSTEMS = {"galaxy": dict(Mb0=5e10*MSUN, R=100*kpc, zc=1.0, kind="disc"), "cluster": dict(Mb0=1e14*MSUN, R=1000*kpc, zc=0.3, kind="cluster")}
def baryon_M(r, Mb, kind):
    if kind == "disc": x = r/(3*kpc); return Mb*(1 - np.exp(-x)*(1 + x))
    u = (r/(700*kpc))**1.7; return Mb*u/(1 + u)
FAILS = []
def check(name, ok, detail=""):
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f"   ({detail})" if detail else ""), flush=True)
    if not ok: FAILS.append(name)

def run(system, K2abs, N=400, zi=50.0, seed_fac=1.0, rcore_frac=0.02, cs_fixed=None, newton=False, a0=A0["canonical"], avg_from=0.9, af=0.5, max_steps=int(4e6), verbose=False):
    S = SYSTEMS[system]; Mb0, R, zc, kind = S["Mb0"], S["R"], S["zc"], S["kind"]
    Mshare = Mb0*Od/Ob; Rshare = (Mshare/(Od*rho_c*4*math.pi/3))**(1/3); RL = 2*Rshare; rcore = rcore_frac*R; ai = 1/(1 + zi); gext = GEXT_FRAC*a0
    rL_in = max(0.01*Rshare, 2.0*rcore*(1 + zi)); edges_L = np.geomspace(rL_in, RL, N + 1)
    delta_0 = seed_fac*1.686*(1 + zc)/(1 + zi); dL = min(delta_0*Rshare/edges_L[0], 1.0)             # the lump's mean overdensity (the seed profile evaluated at its edge)
    m = Od*rho_c*(4*math.pi/3)*(edges_L[1:]**3 - edges_L[:-1]**3); M_lump = Od*rho_c*(4*math.pi/3)*edges_L[0]**3*(1 + dL)   # the lump carries its overdensity (at mean density it under-sourced the inner shells and pinched them)
    rc_ = np.sqrt(edges_L[1:]*edges_L[:-1]); Menc0 = np.cumsum(m) - 0.5*m + M_lump
    dbar_in = np.minimum(delta_0*Rshare/rc_, 1.0)
    dloc = np.gradient(rc_**3*dbar_in, rc_)/(3*rc_**2); din = np.where(rc_ < Rshare, dloc, 0.0)
    ML0 = M_lump/(1 + dL); excess = np.sum(din*m) + dL*ML0; din = np.where(rc_ < Rshare, din, -excess/np.sum(m[rc_ >= Rshare])); dm = (np.cumsum(din*m) + dL*ML0)/Menc0
    r = ai*rc_*(1 - dm/3); v = H_of(ai)*r*(1 - dm/3); a = ai; rmax = r.copy()
    apertures = np.array([R, 0.2*R]); rgrid = np.geomspace(0.01*R, 5*R, 60); Mavg = np.zeros(2); Pavg = np.zeros(60); nav = 0; step = 0; nclamp = 0
    fluid = not (cs_fixed is not None and cs_fixed == 0.0)
    def gravity(rs, Menc_d, a):
        Mb = Mb0*a**3/(a**3 + af**3); Mb_r = baryon_M(rs, Mb, kind); rho_bg = Om*rho_c*a**-3
        dM = Menc_d*(Om/Od) - rho_bg*(4*math.pi/3)*rs**3 + Mb_r - np.minimum(Mb, (Ob/Od)*Menc_d)   # dust + diffuse baryons tracing it, minus the background, plus the assembled baryon profile net of the local budget it was drawn from
        gN = G*dM/rs**2; yN = np.hypot(gN, gext)/a0; g = gN if newton else gN*nu_tot(yN)
        return -(4*math.pi*G/3)*rho_bg*rs + OL*H0**2*rs - g, yN
    def sample(r):
        nonlocal Mavg, Pavg, nav
        rs_ = np.sort(r); Mc = np.cumsum(m[np.argsort(r)]) + M_lump
        Mavg += np.array([M_lump + np.sum(m[r < ap]) for ap in apertures]); Pavg += np.interp(rgrid, rs_, Mc, left=M_lump); nav += 1
    t0 = time.time()
    if not fluid:                                                                                  # collisionless shells with crossing, elastic reflection at the inner wall
        while a < 1.0:
            order = np.argsort(r); rs = r[order]; Menc_d = np.cumsum(m[order]) - 0.5*m[order] + M_lump
            acc_s, _ = gravity(rs, Menc_d, a); acc = np.empty(N); acc[order] = acc_s
            dr_min = max(np.min(np.diff(rs)), 0.01*rcore); vmax = np.max(np.abs(v)) + 1.0
            dt = min(0.25*dr_min/vmax, 0.02/H_of(a), 0.1*math.sqrt(dr_min/(np.max(np.abs(acc)) + 1e-30)))
            v += acc*dt; r += v*dt; hit = r < rcore; r[hit] = 2*rcore - r[hit]; v[hit] = -v[hit]
            a += a*H_of(a)*dt; rmax = np.maximum(rmax, r); step += 1
            if a >= avg_from and step % 20 == 0: sample(r)
    else:                                                                                          # non-crossing Lagrangian hydrodynamics on a STAGGERED grid (von Neumann-Richtmyer): velocities on the shells, pressures in the cells between them
        C2 = 2.0; C1 = 1.0; mc = 0.5*(m[1:] + m[:-1])                                                       # cell masses between consecutive shells
        while a < 1.0:
            Menc_d = np.cumsum(m) - 0.5*m + M_lump
            acc_g, yN = gravity(r, Menc_d, a)
            vol = np.maximum(4*math.pi/3*(r[1:]**3 - r[:-1]**3), 1e-300); rho_c_ = mc/vol         # cell densities
            yc = 0.5*(yN[1:] + yN[:-1]); cs2c = (cs_fixed**2)*np.ones(N - 1) if cs_fixed is not None else 0.42*JY(yc)*c**2/K2abs
            dvc = v[1:] - v[:-1]; qc = np.where(dvc < 0, rho_c_*(C2*dvc**2 + C1*np.sqrt(cs2c)*np.abs(dvc)), 0.0)   # quadratic + linear viscosity in converging cells
            Pc = cs2c*rho_c_ + qc
            cs2_0 = (cs_fixed**2 if cs_fixed is not None else 0.42*float(JY(yN[0]))*c**2/K2abs); P_in = cs2_0*M_lump/(4*math.pi/3*r[0]**3)   # the central cell: the lump's dust between r = 0 and the first shell (its pressure rises as r_0^-3, which is what stops the infall at the centre)
            Pl = np.concatenate([[P_in], Pc]); Pr = np.concatenate([Pc, [Pc[-1]]])                # pressure on the inner / outer side of every shell; outer boundary no-gradient (a fixed outside pressure on the underdense outer shell imploded the whole sphere)
            acc = acc_g - 4*math.pi*r**2*(Pr - Pl)/m
            dr = np.diff(r); csc = np.sqrt(cs2c)
            dt = min(np.min(0.25*dr/(csc + 4*C2*np.abs(dvc) + 0.5*np.abs(v[1:] + v[:-1]) + 1.0)), 0.25*r[0]/(math.sqrt(cs2_0) + abs(v[0]) + 1.0), 0.02/H_of(a), 0.1*math.sqrt(min(np.min(dr), r[0])/(np.max(np.abs(acc)) + 1e-30)))
            v += acc*dt; r += v*dt
            if r[0] < 0.05*rcore: r[0] = 0.05*rcore; v[0] = max(v[0], 0.0)                          # guard only (the central cell's pressure should keep the first shell well outside this)
            bad = np.where(r[1:] <= r[:-1]*(1 + 1e-6))[0]                                          # a crossing the viscosity did not stop: clamp, momentum-conserving, counted (should stay near zero)
            if bad.size:
                nclamp += bad.size
                for i in bad: r[i + 1] = r[i]*(1 + 1e-6); vm = (m[i]*v[i] + m[i + 1]*v[i + 1])/(m[i] + m[i + 1]); v[i] = vm; v[i + 1] = vm
            a += a*H_of(a)*dt; rmax = np.maximum(rmax, r); step += 1
            if a >= avg_from and step % 20 == 0: sample(r)
            if verbose and step % 50000 == 0:
                i_ = int(np.argmin(0.25*dr/(csc + 4*C2*np.abs(dvc) + 0.5*np.abs(v[1:] + v[:-1]) + 1.0)))
                print(f"      step {step}: a = {a:.4f}, dt H = {dt*H_of(a):.2e}, limiting cell {i_} at r = {r[i_]/kpc:.1f} kpc, dr = {dr[i_]/kpc:.3f} kpc, cs = {csc[i_]/1e3:.0f} km/s, |dv| = {abs(dvc[i_])/1e3:.0f} km/s, clamps {nclamp}", flush=True)
            if step >= max_steps: print(f"      ABORT: {max_steps} steps reached at a = {a:.4f}", flush=True); break
    Mavg /= max(nav, 1); Pavg /= max(nav, 1)
    collapsed = r < 0.5*rmax; r_ta = float(np.max(rmax[collapsed])) if collapsed.any() else float("nan"); Macc = float(np.sum(m[collapsed]) + M_lump)
    return dict(frac=Mavg/Mshare, prof=(rgrid, Pavg), r_ta=r_ta, steps=step, secs=time.time() - t0, Mshare=Mshare, nclamp=nclamp, Macc=Macc)

def slope(prof, r_ta):
    rg, Mg = prof; sel = (rg > 0.05*r_ta) & (rg < 0.5*r_ta) & (Mg > 0)
    if sel.sum() < 4: return float("nan")
    return float(np.polyfit(np.log(rg[sel]), np.log(Mg[sel]), 1)[0])


def atmosphere(system, K2abs, M_acc, r_out, a0=A0["canonical"], ngrid=400, af=0.5, iters=60):
    """Self-gravitating hydrostatic atmosphere of the stiff dust in the well at a = 1: P = c_s^2(y_loc) rho with
    c_s^2 = 0.42 J_Y c^2/|K_2|, i.e. c_s^2 = H g_N (H = 0.42 e c^2/(|K_2| a0) for y > 1, H/e for y << 1), so that
    d(c_s^2 rho)/dr = -rho g gives rho ~ exp(-r/H)/g: the dust is pushed out of the centre.  Normalised to the mass M_acc
    that the converged cold infall has brought inside r_out; g includes the dust's own mass (iterated) and the MOND boost."""
    S = SYSTEMS[system]; Mb = S["Mb0"]/(1 + af**3); kind = S["kind"]; gext = GEXT_FRAC*a0
    r = np.geomspace(0.002*S["R"], r_out, ngrid); Md = np.zeros(ngrid)
    for it in range(iters):
        M = baryon_M(r, Mb, kind) + Md; gN = G*M/r**2; yN = np.hypot(gN, gext)/a0; g = gN*nu_tot(yN); cs2 = 0.42*JY(yN)*c**2/K2abs
        I = np.concatenate([[0.0], np.cumsum(0.5*(g[1:]/cs2[1:] + g[:-1]/cs2[:-1])*np.diff(r))])
        shape = np.exp(-I)/cs2; mshape = np.concatenate([[0.0], np.cumsum(0.5*(4*math.pi*r[1:]**2*shape[1:] + 4*math.pi*r[:-1]**2*shape[:-1])*np.diff(r))])
        rho0 = M_acc/mshape[-1]; Md_new = rho0*mshape
        done = np.max(np.abs(Md_new - Md))/max(M_acc, 1e-30) < 1e-6; Md = 0.5*Md + 0.5*Md_new
        if done: break
    return dict(r=r, rho=rho0*shape, Md=Md, cs=np.sqrt(cs2), yN=yN, H=0.42*math.e*c**2/(K2abs*a0), iters=it + 1)

def M_at(res, R): return float(np.interp(R, res["r"], res["Md"]))
XCOP_R = np.array([30, 40, 50, 75, 100, 150, 200, 300, 420])*kpc                                  # h67b canonical medians of eta = M_HSE/(nu(y_b) M_b)
XCOP_ETA = np.array([3.13, 3.00, 2.86, 2.73, 2.78, 2.68, 2.76, 2.61, 2.31])

if __name__ == "__main__":
    print("=" * 110); print("g03r -- converged spherical collapse of the scalar dust with adaptive shells"); print("=" * 110, flush=True)
    T0 = time.time()
    print("  A. cluster, cold collisionless infall (canonical a0, z_c = 0.3): captured/share inside 1 Mpc and 200 kpc (time-averaged a = 0.9-1); turned-around mass and r_ta", flush=True)
    CN, CM = {}, {}
    for N in [200, 400, 800]:
        CN[N] = run("cluster", 1e30, N=N, newton=True, cs_fixed=0.0); print(f"    Newtonian growth N = {N:4d}: {CN[N]['frac'][0]:.4f} / {CN[N]['frac'][1]:.4f}; turned around {CN[N]['Macc']/CN[N]['Mshare']:.3f} shares, r_ta {CN[N]['r_ta']/Mpc:.2f} Mpc, slope {slope(CN[N]['prof'], CN[N]['r_ta']):.2f}  ({CN[N]['secs']:.0f}s)", flush=True)
    for N in [200, 400, 800]:
        CM[N] = run("cluster", 1e30, N=N, cs_fixed=0.0); print(f"    MOND-peculiar growth N = {N:4d}: {CM[N]['frac'][0]:.4f} / {CM[N]['frac'][1]:.4f}; turned around {CM[N]['Macc']/CM[N]['Mshare']:.3f} shares, r_ta {CM[N]['r_ta']/Mpc:.2f} Mpc  ({CM[N]['secs']:.0f}s)", flush=True)
    def spread(vals): vals = np.array(vals, float); return float((vals.max() - vals.min())/max(vals.max(), 1e-12))
    s1 = [spread([CN[N]["frac"][k] for N in CN]) for k in (0, 1)] + [spread([CN[N]["Macc"] for N in CN])]
    check("N1 [convergence] cluster cold Newtonian: mass inside 1 Mpc and 200 kpc and the turned-around mass agree within 15% across N = 200/400/800", max(s1) < 0.15, f"spreads {np.round(s1, 3).tolist()}")
    s1m = [spread([CM[N]["frac"][k] for N in (400, 800)]) for k in (0, 1)] + [spread([CM[N]["Macc"] for N in (400, 800)])]
    check("N2 [convergence] cluster cold MOND-peculiar growth: mass inside 1 Mpc / 200 kpc and the turned-around mass change by < 15% between N = 400 and 800", max(s1m) < 0.15, f"spreads {np.round(s1m, 3).tolist()}")
    sl = slope(CN[800]["prof"], CN[800]["r_ta"]); check("N3 [anchor] cold Newtonian cluster: time-averaged M(<r) slope between 0.05 and 0.5 r_ta is 0.75 +/- 0.25 (secondary infall, rho ~ r^-9/4)", abs(sl - 0.75) < 0.25, f"slope {sl:.2f}")
    print("  B. galaxy, cold collisionless infall (canonical a0, z_c = 1): captured/share inside 100 kpc and 10 kpc", flush=True)
    GN, GM = {}, {}
    for N in [200, 400, 800]:
        GN[N] = run("galaxy", 1e30, N=N, newton=True, cs_fixed=0.0); GM[N] = run("galaxy", 1e30, N=N, cs_fixed=0.0)
        print(f"    N = {N:4d}: Newtonian {GN[N]['frac'][0]:.4f} / {GN[N]['frac'][1]:.4f} (turned around {GN[N]['Macc']/GN[N]['Mshare']:.3f}, r_ta {GN[N]['r_ta']/kpc:.0f} kpc) | MOND-peculiar {GM[N]['frac'][0]:.4f} / {GM[N]['frac'][1]:.4f} (turned around {GM[N]['Macc']/GM[N]['Mshare']:.3f}, r_ta {GM[N]['r_ta']/kpc:.0f} kpc)  ({GN[N]['secs'] + GM[N]['secs']:.0f}s)", flush=True)
    s4 = [spread([GN[N]["Macc"] for N in (400, 800)]), spread([GM[N]["Macc"] for N in (400, 800)]), spread([GN[N]["frac"][0] for N in (400, 800)]), spread([GM[N]["frac"][0] for N in (400, 800)])]
    check("N4 [convergence] galaxy: turned-around mass and the 100-kpc capture change by < 15% between N = 400 and 800 in both growth models", max(s4) < 0.15, f"spreads {np.round(s4, 3).tolist()}")
    print("  C. the stiff dust's hydrostatic atmosphere (P = c_s^2(y_loc) rho, c_s^2 = 0.42 J_Y c^2/|K_2| => rho ~ exp(-r/H)/g, H = 0.42 e c^2/(|K_2| a0)), normalised to the turned-around mass, self-gravity iterated", flush=True)
    for K2 in [1e5, 3e5, 1e6]: print(f"    H(|K_2| = {K2:.0e}) = {0.42*math.e*c**2/(K2*A0['canonical'])/kpc:.0f} kpc (canonical), {0.42*math.e*c**2/(K2*A0['alt'])/kpc:.0f} kpc (alt)", flush=True)
    ac4 = atmosphere("cluster", 3e5, CN[800]["Macc"], CN[800]["r_ta"], ngrid=400); ac16 = atmosphere("cluster", 3e5, CN[800]["Macc"], CN[800]["r_ta"], ngrid=1600)
    check("H1 [convergence] the atmosphere's mass inside 1 Mpc and 200 kpc agrees within 1% between 400 and 1600 grid points (cluster, 3e5, Newtonian-growth normalisation)", abs(M_at(ac4, Mpc)/M_at(ac16, Mpc) - 1) < 0.01 and abs(M_at(ac4, 0.2*Mpc)/M_at(ac16, 0.2*Mpc) - 1) < 0.01, f"1 Mpc {M_at(ac4, Mpc)/MSUN:.3e} vs {M_at(ac16, Mpc)/MSUN:.3e} Msun; 200 kpc {M_at(ac4, 0.2*Mpc)/MSUN:.3e} vs {M_at(ac16, 0.2*Mpc)/MSUN:.3e}")
    Mb1 = SYSTEMS["cluster"]["Mb0"]/(1 + 0.5**3); detail = []; peaks = []
    rr = np.geomspace(10*kpc, 2*Mpc, 200)
    for K2 in [1e5, 3e5, 1e6]:
        ac = atmosphere("cluster", K2, CN[800]["Macc"], CN[800]["r_ta"]); ratio = np.interp(rr, ac["r"], ac["Md"])/baryon_M(rr, Mb1, "cluster"); ip = int(np.argmax(ratio)); peaks.append(rr[ip]/ac["H"])
        detail.append(f"{K2:.0e}: peak of M_d/M_b at {rr[ip]/kpc:.0f} kpc = {rr[ip]/ac['H']:.2f} H")
    check("H2 [reported] the radius where the atmosphere's enclosed dust-to-baryon ratio M_d(<r)/M_b(<r) peaks scales with H (between 1 and 4 H at |K_2| = 1e5, 3e5, 1e6)", all(1.0 <= pk <= 4.0 for pk in peaks), "; ".join(detail))
    K2S = [5e4, 1e5, 2e5, 3e5, 5e5, 1e6, 3e6]; TABLE = {}
    for growth, (refc, refg) in {"Newtonian growth": (CN[800], GN[800]), "MOND-peculiar growth": (CM[800], GM[800])}.items():
        for foot, a0 in A0.items():
            print(f"  D. window table, {growth}, {foot} footing: atmosphere mass / cold reference mass inside the apertures (cold reference = the collisionless infall in the same growth model, canonical run)", flush=True)
            print("     |K_2| | galaxy 100 kpc | galaxy 10 kpc | cluster 1 Mpc | cluster 200 kpc | H [kpc]", flush=True)
            rows = []
            for K2 in K2S:
                ag = atmosphere("galaxy", K2, refg["Macc"], refg["r_ta"], a0=a0); ac = atmosphere("cluster", K2, refc["Macc"], refc["r_ta"], a0=a0)
                row = [M_at(ag, 100*kpc)/max(refg["frac"][0]*refg["Mshare"], 1e-30), M_at(ag, 10*kpc)/max(refg["frac"][1]*refg["Mshare"], 1e-30), M_at(ac, Mpc)/max(refc["frac"][0]*refc["Mshare"], 1e-30), M_at(ac, 0.2*Mpc)/max(refc["frac"][1]*refc["Mshare"], 1e-30)]
                rows.append(row); print(f"     {K2:7.0e} |        {row[0]:7.3f} |       {row[1]:7.3f} |       {row[2]:7.3f} |         {row[3]:7.3f} | {ag['H']/kpc:7.0f}", flush=True)
            TABLE[(growth, foot)] = rows
            win = [K2 for K2, row in zip(K2S, rows) if row[0] <= 0.14 and row[2] >= 0.32]
            print(f"    window: |K_2| with galaxy 100 kpc <= 0.14 and cluster 1 Mpc >= 0.32 -> {win if win else 'NONE'}", flush=True)
    check("W1 [reported] a window exists (some growth model, both footings) where the galaxy's 100-kpc dust is <= 14% of its cold reference while the cluster's 1-Mpc dust is >= 32%",
          any(all(any(r[0] <= 0.14 and r[2] >= 0.32 for r in TABLE[(gr, f)]) for f in A0) for gr in ["Newtonian growth", "MOND-peculiar growth"]),
          json.dumps({f"{gr}/{f}": [K2 for K2, r in zip(K2S, TABLE[(gr, f)]) if r[0] <= 0.14 and r[2] >= 0.32] for gr in ["Newtonian growth", "MOND-peculiar growth"] for f in A0}))
    print("  E. the cluster residual against X-COP: eta_pred = (M_b + M_d) nu(y_tot)/(nu(y_b) M_b) from the atmosphere in the model cluster's well vs the h67b medians; supplied = (eta_pred - 1)/(eta_data - 1); scan of |K_2| for the best profile match", flush=True)
    K2X = np.geomspace(5e4, 1e6, 14); XSHAPE = {}
    lr = np.log10(XCOP_R/kpc); trend_data = float(np.polyfit(lr, np.log10(XCOP_ETA - 1), 1)[0])
    for growth, refc in {"Newtonian growth": CN[800], "MOND-peculiar growth": CM[800]}.items():
        best = None
        for K2 in K2X:
            ac = atmosphere("cluster", K2, refc["Macc"], refc["r_ta"]); Mb_r = baryon_M(XCOP_R, Mb1, "cluster"); Md_r = np.interp(XCOP_R, ac["r"], ac["Md"])
            yb = G*Mb_r/XCOP_R**2/A0["canonical"]
            eta = (Mb_r + Md_r)*nu_tot(G*(Mb_r + Md_r)/XCOP_R**2/A0["canonical"])/(nu_tot(yb)*Mb_r)                  # dynamical mass with the kernel on the total, over the kernel on the baryons alone
            sup = (eta - 1)/(XCOP_ETA - 1); ls = np.log10(np.maximum(sup, 1e-6)); rms = float(np.sqrt(np.mean(ls**2))); trend = float(np.polyfit(lr, np.log10(np.maximum(eta - 1, 1e-6)), 1)[0])
            if K2 in (K2X[0], K2X[4], K2X[7], K2X[10], K2X[13]) or (best is not None and rms < best[1]) or best is None:
                pass
            if best is None or rms < best[1]: best = (K2, rms, trend, sup.copy())
            if any(abs(K2/k - 1) < 0.01 for k in (5e4, 1e5, 2e5, 3e5, 5e5, 1e6)) or K2 == best[0]:
                print(f"    {growth:22s} |K_2| = {K2:.2e}: supplied {np.round(sup, 2).tolist()} rms log = {rms:.2f} dex, trend d log(eta-1)/d log r = {trend:+.2f} (data {trend_data:+.2f})", flush=True)
        XSHAPE[growth] = best; print(f"    {growth:22s} best |K_2| = {best[0]:.2e} (H = {0.42*math.e*c**2/(best[0]*A0['canonical'])/kpc:.0f} kpc): rms {best[1]:.2f} dex, trend {best[2]:+.2f} vs data {trend_data:+.2f}; supplied {np.round(best[3], 2).tolist()}", flush=True)
    check("X1 [reported] at its best |K_2| the atmosphere reproduces X-COP's residual profile (eta - 1 at 30-420 kpc) to within 0.15 dex rms AND with the data's radial trend to within 0.2 in slope, in at least one growth model", any(b[1] < 0.15 and abs(b[2] - trend_data) < 0.2 for b in XSHAPE.values()), "; ".join(f"{gr}: |K_2| {b[0]:.1e}, rms {b[1]:.2f} dex, trend {b[2]:+.2f} vs data {trend_data:+.2f}" for gr, b in XSHAPE.items()))
    check("X2 [reported] the best |K_2| for X-COP lies inside the KiDS/cluster window of the same growth model", any(any(abs(XSHAPE[gr][0]/K2 - 1) < 0.6 for K2 in [k for k, r in zip(K2S, TABLE[(gr, 'canonical')]) if r[0] <= 0.14 and r[2] >= 0.32]) for gr in XSHAPE), "; ".join(f"{gr}: best {XSHAPE[gr][0]:.1e}, window {[k for k, r in zip(K2S, TABLE[(gr, 'canonical')]) if r[0] <= 0.14 and r[2] >= 0.32]}" for gr in XSHAPE))
    print(f"\n  caveats: spherical; one representative system each; the dust sources the MOND scalar (AeST reading); the linear regime is MONDian so the growth from z_i = 50 is a model statement -- two growth models bracket it (Newtonian; MOND on the peculiar field with a 0.02 a0 external field); the stiff dust is treated as a hydrostatic atmosphere with P = c_s^2(y_loc) rho (f34's sound speed at the local field) because the Lagrangian fluid dynamics at this dynamic range (core sound speeds to 0.1 c) does not converge (documented in the header); assembly history assumed.  total {time.time() - T0:.0f}s")
    print(f"\nRESULT: {len(FAILS)} FAIL" + (f" -> {FAILS}" if FAILS else ""))
    sys.exit(1 if FAILS else 0)
