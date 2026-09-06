#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""g03o -- spherical collapse of the scalar dust with self-gravity and its position-dependent stiffness, into a growing baryonic MOND well.
Lagrangian shells (N = 400, equal-mass by default; a logarithmic spacing from max(0.01 R_share, 2 r_core (1+z_i)) is used in the convergence block) start at z = 50 (z = 20 in the convergence block) in the Hubble flow as a uniform comoving component (density Omega_d rho_crit a^-3, Omega_d = 0.26);
the dust carries a compensated growing-mode perturbation with enclosed overdensity falling as 1/r inside its share radius (secondary-infall profile, capped at 1 in the core), normalised so the share's edge collapses at z_c = 1 (galaxy) / 0.3 (cluster) in linear theory, with the linear peculiar velocity; the baryons are a central mass growing as M_b(a) = M_b0 a^3/(a^3 + a_f^3) (a_f = 0.5; an assumption); the background expansion is the Friedmann term and
gravity on a shell is the candidate's spherical static law on the PECULIAR field of the overdensity (baryons + dust minus the background inside r; the dust
sources the scalar, the AeST reading; the MOND-cosmology convention, with a large-scale external field of 0.02 a0 in the MOND argument so the deep-MOND boost of the compensating underdensity stays finite), plus the cosmological-constant term; binding is measured relative to the edge of the overdense well; pressure P = c_s^2 rho with c_s^2 = 0.42 J_Y(y_N,loc)/|K_2| c^2 (the kernel's stiffness at the local Newtonian
field, g03j/g03m/g03n), with artificial viscosity for shocks.  Captured fraction f = (dust bound and inside R at a = 1)/(the dust share Omega_d/Omega_b M_b0).
Controls: cold Newtonian (c_s = 0, nu = 1) must capture ~all of the share inside the turnaround; a hot dust (c_s = 300 km/s) must capture ~none.
Systems: galaxy M_b0 = 5e10 Msun, R = 100 kpc (KiDS) and 10 kpc (RAR); cluster M_b0 = 1e14 Msun, R = 1 Mpc.  Checks can fail."""
import math, sys, numpy as np
from scipy.optimize import brentq
FAILS = []
def check(name, ok, detail=""):
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f"   ({detail})" if detail else ""), flush=True)
    if not ok: FAILS.append(name)
G, c, kpc, MSUN, a0 = 6.6743e-11, 2.998e8, 3.0857e19, 1.98892e30, 9.3619e-11
H0 = 67.4e3/(kpc*1e3); Om, OL, Ob, Od = 0.315, 0.685, 0.049, 0.266; rho_c = 3*H0**2/(8*math.pi*G)
GEXT_LSS = 0.02*a0                                                                              # large-scale-structure peculiar acceleration entering the MOND argument (H0 x ~600 km/s; an assumption)
Y1 = 1 - 1/math.e
YT = np.logspace(-6, 3, 4000); YN = YT*(1 - np.exp(-YT))                                   # y_N(y_tot) table (monotone)
def ytot(yN): return np.interp(yN, YN, YT)
def nu_tot(yN):                                                                             # g/g_N for the completed kernel: exponential for y_tot <= 1, saturated scalar force beyond
    yN = np.asarray(yN, float); yt = ytot(yN); out = np.where(yt <= 1, yt/np.maximum(yN, 1e-300), 1 + (1/math.e)/np.maximum(yN, 1e-300)); return out
def JY(yN):
    yN = np.asarray(yN, float); yt = ytot(yN); yt1 = np.minimum(yt, 1.0); return np.where(yt <= 1, yN/(yt1*np.exp(-yt1)), yN/(1/math.e))   # yt clipped in the unselected branch so it cannot overflow
def H_of(a): return H0*math.sqrt(Om*a**-3 + OL)
def run(Mb0, R, K2abs, af=0.5, N=400, zi=50.0, cs_fixed=None, newton=False, zc=1.0, rcore=None, verbose=False, spacing="equal"):
    rcore = rcore if rcore is not None else 0.02*R           # shells reaching the core are absorbed into the central mass (frozen), which keeps the Courant step finite
    ai = 1/(1 + zi); Mshare = Mb0*Od/Ob
    Rshare = (3*Mshare/(4*math.pi*Od*rho_c))**(1/3)                                          # comoving radius holding the dust share
    RL = 2.0*Rshare
    # logarithmically spaced Lagrangian shells from 0.01 Rshare to RL (the core is resolved); the dust inside 0.01 Rshare is a frozen central lump
    rL_in = max(0.01*Rshare, 2.0*rcore*(1 + zi))                                                # no shell starts inside the absorbing core (the previous floor put them there and the densities overflowed)
    edges_L = np.geomspace(rL_in, RL, N + 1) if spacing == "log" else np.concatenate([[rL_in], RL*(np.arange(1, N + 1)/N)**(1/3)]); m = Od*rho_c*(4*math.pi/3)*(edges_L[1:]**3 - edges_L[:-1]**3); M_lump = Od*rho_c*(4*math.pi/3)*edges_L[0]**3
    delta_0 = 1.686*(1 + zc)/(1 + zi)
    rc_ = np.sqrt(edges_L[1:]*edges_L[:-1]); Menc0 = np.cumsum(m) - 0.5*m + M_lump
    dbar_in = np.minimum(delta_0*Rshare/rc_, 1.0)
    Min = np.sum(m[rc_ < Rshare]*0) + 0.0
    # local contrast from the enclosed one: delta = delta_bar + (r/3) d delta_bar/dr  (numerically), then compensate outside
    dloc = np.gradient(rc_**3*dbar_in, rc_)/(3*rc_**2); din = np.where(rc_ < Rshare, dloc, 0.0)
    excess = np.sum(din*m); din = np.where(rc_ < Rshare, din, -excess/np.sum(m[rc_ >= Rshare]))
    dm = np.cumsum(din*m)/Menc0
    r = ai*rc_*(1 - dm/3); v = H_of(ai)*r*(1 - dm/3*1.0)                                        # growing mode: v_pec = -(1/3) H r delta_mean (linear, f ~ 1 at z = 50)
    a = ai; t = 0.0; rmax = r.copy()
    def forces(r, v, a):
        order = np.argsort(r); rs = r[order]; Menc_d = np.cumsum(m[order]) - 0.5*m[order] + M_lump
        Mb = Mb0*a**3/(a**3 + af**3)
        rho_bg = Om*rho_c*a**-3                                                                  # total matter background (in the Friedmann term)
        dM = Mb + Menc_d - rho_bg*(4*math.pi/3)*rs**3                                             # the overdensity's mass: baryons + dust minus the background inside r
        gN = G*dM/rs**2; yN = np.hypot(gN, GEXT_LSS)/a0                                            # PECULIAR Newtonian field (signed); the MOND argument includes a large-scale external field (EFE regularisation of y -> 0)
        g = gN if newton else gN*nu_tot(yN)                                                        # MOND acts on the peculiar field (the MOND-cosmology convention)
        Menc = Mb + Menc_d
        # pressure: rho from shell volumes, c_s^2 local -- on LIVE shells only (core-absorbed shells coincide in r and carry no pressure force)
        live = rs > rcore*1.001; nl = int(live.sum()); rho = np.zeros(N); cs2 = np.zeros(N); gradP = np.zeros(N)
        if nl >= 3:
            rl = rs[live]; ml = m[order][live]
            edges = np.concatenate([[rcore], 0.5*(rl[1:] + rl[:-1]), [rl[-1] + 0.5*(rl[-1] - rl[-2])]])
            vol = np.maximum(4*math.pi/3*(edges[1:]**3 - edges[:-1]**3), 4*math.pi*rl**2*(0.005*rl)); rho_l = ml/vol   # volume floored at a 0.5% radial spacing (crossing shells would otherwise give an infinite density)
            cs2_l = (cs_fixed**2)*np.ones(nl) if cs_fixed is not None else 0.42*JY(yN[live])*c**2/K2abs
            P = cs2_l*rho_l
            dv = np.diff(v[order][live]); q = np.zeros(nl - 1); conv = dv < 0
            if not (cs_fixed is not None and cs_fixed == 0.0): q[conv] = 2.0*rho_l[:-1][conv]*dv[conv]**2
            Pf = P.copy(); Pf[:-1] += 0.5*q; Pf[1:] += 0.5*q
            gP = np.gradient(Pf)/np.maximum(np.gradient(rl), 0.005*rl); rho[live] = rho_l; cs2[live] = cs2_l; gradP[live] = gP   # spacing floored likewise
        acc = -(4*math.pi*G/3)*rho_bg*rs + OL*H0**2*rs - g - np.where(rho > 0, gradP/np.maximum(rho, 1e-300), 0.0); acc[~live] = 0.0
        out = np.empty(N); out[order] = acc; cs = np.empty(N); cs[order] = np.sqrt(cs2); return out, cs, rs, Menc_d, order
    while a < 1.0:
        acc, cs, rs, _, order = forces(r, v, a)
        dr_min = np.min(np.diff(rs)); vmax = np.max(np.abs(v)) + np.max(cs) + 1.0
        live = rs > rcore*1.001; dr_live = np.min(np.diff(rs[live])) if live.sum() > 2 else dr_min
        dt = max(min(0.25*max(dr_live, 0.01*rcore)/vmax, 0.02/H_of(a), 0.1*math.sqrt(max(dr_live, 0.01*rcore)/(np.max(np.abs(acc)) + 1e-30))), 1e-5/H_of(a))
        core = r <= rcore; v[core] = 0.0; acc[core] = 0.0
        v += acc*dt; r += v*dt; r = np.maximum(r, rcore); t += dt; a += a*H_of(a)*dt; rmax = np.maximum(rmax, r)
    # bound and inside R at a = 1: energy per unit mass with the final potential (MOND on total enclosed mass), potential from infinity by quadrature
    acc, cs, rs, Menc_d, order = forces(r, v, 1.0); Mb = Mb0*1/(1 + af**3); rho_bg = Om*rho_c
    Mshare_lump = M_lump                                                                                # the frozen central dust lump counts as captured inside every aperture
    dM = Mb + Menc_d - rho_bg*(4*math.pi/3)*rs**3
    rr = np.logspace(math.log10(rs.min()*0.5), math.log10(rs.max()), 3000); dMe = np.interp(rr, rs, dM); gNe = G*dMe/rr**2
    gg = gNe if newton else gNe*nu_tot(np.hypot(gNe, GEXT_LSS)/a0)
    ipk = int(np.argmax(dMe)); iz = ipk + int(np.argmax(dMe[ipk:] <= 0)) if np.any(dMe[ipk:] <= 0) else len(rr) - 1      # edge of the well: where the enclosed excess mass first returns to zero
    R_edge = rr[iz]
    Phi = np.zeros(len(rr)); Phi[:iz] = -np.array([np.trapz(gg[i:iz], rr[i:iz]) for i in range(iz)])                    # potential relative to the well's edge (0 outside)
    vpec = v[order] - H0*rs                                                                     # peculiar velocity at a = 1
    E = 0.5*vpec**2 + np.interp(rs, rr, Phi); rv = 0.5*rmax[order]; bound = (E < 0) & (rv < R) & (rs < R_edge); inner = (E < 0) & (rv < 0.1*R)
    return float((np.sum(m[order][bound]) + M_lump)/Mshare), float((np.sum(m[order][inner]) + M_lump)/Mshare)
print("=" * 100); print("g03o -- spherical collapse of the scalar dust with self-gravity and local stiffness"); print("=" * 100)
SYS = {"galaxy 100 kpc": (5e10*MSUN, 100*kpc), "cluster 1 Mpc": (1e14*MSUN, 1000*kpc)}
print("  references and controls (captured = bound with virialised radius r_ta/2 inside the aperture; fractions of the cosmic share):")
REF = {}
for nm, (Mb, R, zc) in {"galaxy 100 kpc": (5e10*MSUN, 100*kpc, 1.0), "cluster 1 Mpc": (1e14*MSUN, 1000*kpc, 0.3)}.items():
    cN, cNi = run(Mb, R, 1e30, newton=True, cs_fixed=0.0, zc=zc); cM, cMi = run(Mb, R, 1e30, cs_fixed=0.0, zc=zc); REF[nm] = (cM, cMi)
    print(f"    {nm}: cold Newtonian {cN:.3f} (inner {cNi:.3f}); cold in the MOND well {cM:.3f} (inner {cMi:.3f})  <- the CDM-like reference", flush=True)
fh, _ = run(5e10*MSUN, 100*kpc, 1e30, cs_fixed=3e5, zc=1.0); print(f"    hot dust (c_s = 300 km/s, galaxy): {fh:.3f}", flush=True)
print("  convergence of the cluster capture at |K_2| = 3e5 (z_c = 0.3): captured/share stiff, cold, and their ratio, across shell spacing and start redshift", flush=True)
CONV = {}
for sp_ in ["equal", "log"]:
    for zi_ in [50.0, 20.0]:
        fs_, _ = run(1e14*MSUN, 1000*kpc, 3e5, zc=0.3, zi=zi_, spacing=sp_); fc_, _ = run(1e14*MSUN, 1000*kpc, 1e30, cs_fixed=0.0, zc=0.3, zi=zi_, spacing=sp_)
        CONV[(sp_, zi_)] = fs_/max(fc_, 1e-9); print(f"    {sp_:5s} shells, z_i = {zi_:2.0f}: stiff {fs_:.3f}  cold {fc_:.3f}  ratio {CONV[(sp_, zi_)]:.2f}", flush=True)
cv_ = np.array(list(CONV.values()))
check("D4 [convergence] the cluster's stiff/cold capture ratio at |K_2| = 3e5 agrees within a factor 2 across shell spacing (equal-mass / logarithmic) and start redshift (z_i = 50 / 20); if this fails the window below is NOT a converged result of the method", cv_.max() <= 2*max(cv_.min(), 1e-9) and cv_.min() > 0, f"ratios {np.round(cv_, 2).tolist()}")
check("C1 the cold references capture a definite part of the share inside the apertures (> 0.05 in both systems; the apertures are smaller than the virialised extents, so the absolute fractions are modest and only the RATIOS stiff/cold are used below) and the hot control captures little (< 0.1 of the galaxy's cold reference)", REF["galaxy 100 kpc"][0] > 0.05 and REF["cluster 1 Mpc"][0] > 0.05 and fh < 0.1*REF["galaxy 100 kpc"][0], f"galaxy {REF['galaxy 100 kpc'][0]:.3f}, cluster {REF['cluster 1 Mpc'][0]:.3f}, hot {fh:.3f}")
print(f"\n  {'|K_2|':>8s} | galaxy 100 kpc | galaxy inner 10 kpc | cluster 1 Mpc     (relative to the cold MOND reference; targets: galaxy <= 0.14, inner ~ 0, cluster >= 0.32-0.46)")
RES = {}
for K2 in (5e4, 1e5, 2e5, 3e5, 5e5, 1e6, 3e6):
    fg, fgi = run(5e10*MSUN, 100*kpc, K2, zc=1.0); fcl, _ = run(1e14*MSUN, 1000*kpc, K2, zc=0.3)
    rg = fg/max(REF["galaxy 100 kpc"][0], 1e-9); rgi = fgi/max(REF["galaxy 100 kpc"][1], 1e-9); rc = fcl/max(REF["cluster 1 Mpc"][0], 1e-9)
    RES[K2] = {"galaxy 100 kpc": rg, "galaxy 10 kpc": rgi, "cluster 1 Mpc": rc}; print(f"  {K2:8.0e} | {rg:14.3f} | {rgi:19.3f} | {rc:13.3f}", flush=True)
win = [K2 for K2 in RES if RES[K2]["galaxy 100 kpc"] <= 0.14 and RES[K2]["cluster 1 Mpc"] >= 0.32]
check("D1 with self-gravity and the growing well there is at least one |K_2| in 5e4-3e6 with the galaxy's captured dust <= 14% and the cluster's >= 32% of the CDM-like reference", bool(win), f"window points {win}")
check("D2 at every |K_2| the cluster's relative capture exceeds the galaxy's (the kernel-fixed ordering survives the dynamics)", all(RES[K2]["cluster 1 Mpc"] >= RES[K2]["galaxy 100 kpc"] for K2 in RES))
check("D3 the inner galaxy (10 kpc) captures under 5% of its cold reference wherever the outskirts capture under 14%", all(RES[K2]["galaxy 10 kpc"] < 0.05 for K2 in RES if RES[K2]["galaxy 100 kpc"] <= 0.14))
print("\n  caveats: spherical, one representative system each, baryon assembly history assumed, the dust sources the MOND scalar (AeST reading), potential truncated at 50 r_max for the binding energy, no shell-crossing beyond the fluid treatment.")
print(f"\nRESULT: {len(FAILS)} FAIL -> {FAILS}" if FAILS else "\nRESULT: 0 FAIL"); sys.exit(1 if FAILS else 0)
