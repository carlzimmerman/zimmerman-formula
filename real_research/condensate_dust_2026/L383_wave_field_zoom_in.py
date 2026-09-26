#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
L383 -- THE WAVE FIELD INSIDE A DWARF HALO: a zoom-in Schroedinger-Poisson simulation, and the one thing the wave field does
there that cold particles do not -- it heats the stars.

WHY.  L374: of the no-particle candidates, only a linear wave field (fuzzy dark matter) passes through itself.  L382: at every
  boson mass the Lyman-alpha forest allows, the record's particle-mesh box cannot tell that field from the collisionless
  carrier; everything wave-like sits below ~30 pc, inside galaxies.  This lane goes there.  Inside a halo the wave field
  (a) settles into a solitonic core -- the ground state of Schroedinger-Poisson -- surrounded by an envelope of interference
  granules, and (b) its granules, O(1) density fluctuations of size ~ hbar / (m sigma) that live ~ hbar / (m sigma^2), heat
  any star that orbits through them, like a swarm of heavy quasi-particles (Bar-Or, Fouvry & Tremaine 2019: the heating is
  that of classical particles of mass m_eff ~ pi^(3/2) hbar^3 rho / (m^3 sigma^3), so D[v^2] ~ G^2 rho^2 (hbar/m)^3 / sigma^4).
  The heating is what observations bite on: ultra-faint dwarfs would puff up (Dalal & Kravtsov 2022: m >~ 3e-19 eV).  The
  framework adds one thing the literature does not have: its vacuum-gated clearing (mode G, L357/L372) removes the dark mass
  from galaxies once the vacuum takes over, which shortens the heating.
METHOD (code units hbar/m = G = 1; periodic box L = 1; the evolution is exact in Fourier space for the kinetic term).
  A  THE ZOOM-IN.  Ground-state solitons by imaginary-time propagation (masses 40 and 60 in code units: lighter ones are wider
     than their own wave Jeans length in this box and relax to the uniform state).  A halo from 12 merging solitons
     (random positions within 0.25 of the centre, sub-virial random velocities, random phases) on a 128^3 grid, evolved for
     ~12 crossing times (split-step, kick-drift-kick).  The relaxed halo's core against the ground state, its envelope, its
     granules; a figure of a density slice and the profile.
  B  THE HEATING.  A homogeneous wave bath (random phases, Maxwellian with 1D dispersion sigma, mean density rho), evolved
     exactly (free), its fluctuation potential from Poisson; 4000 stars in a harmonic trap (sigma_* = sigma/3, cloud radius
     0.15 spanning several granules); heating D = 2 d<E>/dt fitted while the stars stay slow (trap energy up < 25%).  Three baths: (rho, 24), (2 rho, 24), (2 rho, 36; twice the orbits,
     so the weaker heating stays above the noise); two seeds each.
  C  THE APPLICATION.  A Segue-1-like ultra-faint dwarf (r_h 29 pc, sigma_* 3.7 km/s, dark density 5.7 Msun/pc^3 inside r_h;
     Simon et al. 2011) in a halo with dispersion 5-10 km/s: the measured D, carried to physical units with the Coulomb
     logarithm ln(b_max / b_min) of each system, over the time the dark halo is there -- LCDM: from z = 8 to today; the
     framework: from z = 8 until the vacuum-gated trigger fires in the dwarf's own density (x~ [Omega_L(z)/Omega_L0]^2 >=
     x_v0 = 1000-2000, L357).  The minimum boson mass is the one whose heating stays below the observed sigma_*^2.
PRE-DECLARED (before any run).  H: the framework's late clearing opens the wave field's mass window down to the forest bound:
  with the clearing, the ultra-faint-dwarf floor falls to <= 2e-20 eV.  (The heating scales as m^-3 and the exposure ratio
  is ~10, which suggests it will not: then the clearing lowers the floor by only ~10^(1/3).)
CHECKS
  A1 NUMERICAL TRUST: the halo run conserves mass to 1e-10 and energy to 1%.
  A2 CONTROL: the imaginary-time ground state has Schive et al. 2014's profile (rho_c [1 + 0.091 (r/r_c)^2]^-8; rms log
     residual < 0.05 inside 2.5 r_c), and the M, 1.5M pair obeys the Schroedinger-Poisson scaling r_c ~ 1/M (ratio 2/3
     within 3%).
  A3 THE CORE IS THE GROUND STATE: the relaxed halo's core (time-averaged) has rho_c r_c^4 within 25% of the ground state's
     (the scaling invariant), and its profile is the soliton's inside 2 r_c (rms log residual < 0.12).
  B1 CONTROL: with the bath's potential switched off, the stars' trap energy is conserved to 1e-3 (the integrator).
  B2 THE QUASI-PARTICLE SCALING: doubling rho multiplies the heating by 4 (within 25%).
  B3 (reported) sigma x 1.5 against 1.5^-4 x the Coulomb-log ratio (the log model is rough at ln Lambda ~ 1-2).
  C1 CONTROL: with LCDM's exposure the floor is within a factor 5 of Dalal & Kravtsov's 3e-19 eV (the calibration is sane).
  R1 = H.   W (reported): the floor with and without the clearing, for sigma_DM = 5-10 km/s and x_v0 = 1000-2000.
MUTATE=1 freezes the bath (granules that never change): the heating vanishes and R1 flips -- the inverted control, showing the
  verdict rests on the granules' time dependence.  (Part A is not rerun under MUTATE.)  FAST=1 is a code test on small grids;
  it writes nothing here.
Run from the repository root:  python3 real_research/condensate_dust_2026/L383_wave_field_zoom_in.py
"""
import os, sys, json, math, time, tempfile
import numpy as np
from multiprocessing import Pool

HERE = os.path.dirname(os.path.abspath(__file__))
MUTATE = os.environ.get("MUTATE", "0") == "1"
FAST = os.environ.get("FAST", "0") == "1"
SLUG = "L383_wave_field_zoom_in" + ("_MUTATE" if MUTATE else "") + ("_FAST" if FAST else "")
OUTDIR = tempfile.gettempdir() if FAST else HERE
T0 = time.time()
P = lambda *a: print(*a, flush=True)
CH, OUT = [], {"lane": "L383", "mutate": MUTATE, "checks": {}, "numbers": {}}
EXPECT_OPENS = True                                                  # H, set before any run

NA = 48 if FAST else 128                                             # Part A grid
NB = 48 if FAST else 128                                             # Part B grid
NSOL, RC_IC_CELLS, R0 = (6, 4.0, 0.25) if FAST else (12, 7.0, 0.25)
N_CROSS = 2.0 if FAST else 12.0
NSTAR = 400 if FAST else 4000
B_ORBITS = 1.5 if FAST else 6.0
# physical constants for Part C
G_PC = 4.3009e-3                                                     # pc (km/s)^2 / Msun
HBARM_1EV = 1.917e-18                                                # hbar/m in pc km/s for m = 1 eV (19.2 kpc km/s at 1e-22 eV)
MYR_PER_PCKMS = 0.9778


def check(name, measured, ok, reading="", load_bearing=True):
    ok = bool(ok); CH.append((name, ok, load_bearing))
    OUT["checks"][name] = {"ok": ok, "measured": str(measured), "load_bearing": load_bearing}
    P(f"  [{'PASS' if ok else 'FAIL'}] {name}"); P(f"         measured: {measured}")
    if reading: P(f"         reading:  {reading}")
    return ok


def banner(t): P("\n" + "=" * 116); P(t); P("=" * 116)


class Box:
    """periodic box of side 1 with an n^3 grid; hbar/m = G = 1."""
    def __init__(self, n):
        self.n, self.dx = n, 1.0 / n
        k = 2 * np.pi * np.fft.fftfreq(n, self.dx); kr = 2 * np.pi * np.fft.rfftfreq(n, self.dx)
        KX, KY, KZ = np.meshgrid(k, k, k, indexing="ij")
        self.K2 = KX ** 2 + KY ** 2 + KZ ** 2
        del KX, KY, KZ
        self.KXr, self.KYr, self.KZr = np.meshgrid(k, k, kr, indexing="ij")
        self.K2r = self.KXr ** 2 + self.KYr ** 2 + self.KZr ** 2; self.K2r[0, 0, 0] = 1.0
        self.x = np.arange(n) * self.dx
        self.dv = self.dx ** 3

    def potential(self, rho):
        rk = np.fft.rfftn(rho); rk[0, 0, 0] = 0.0
        return np.fft.irfftn(-4 * np.pi * rk / self.K2r, s=rho.shape)

    def gravity(self, rho):
        rk = np.fft.rfftn(rho); rk[0, 0, 0] = 0.0
        vk = -4 * np.pi * rk / self.K2r
        return [np.fft.irfftn(-1j * K * vk, s=rho.shape) for K in (self.KXr, self.KYr, self.KZr)]

    def mass(self, psi):
        return float(np.sum(np.abs(psi) ** 2) * self.dv)

    def energy(self, psi):
        pk = np.fft.fftn(psi)
        kin = 0.5 * float(np.sum(self.K2 * np.abs(pk) ** 2)) * self.dv / psi.size
        rho = np.abs(psi) ** 2
        return kin + 0.5 * float(np.sum(self.potential(rho) * rho) * self.dv), kin

    def radial(self, rho, c, nb=60, rmax=0.45):
        nb = min(nb, int(rmax / (0.6 * self.dx)))                    # bins at least 0.6 cells wide
        d = [((self.x - c[i] + 0.5) % 1.0) - 0.5 for i in range(3)]
        r = np.sqrt(d[0][:, None, None] ** 2 + d[1][None, :, None] ** 2 + d[2][None, None, :] ** 2)
        edges = np.linspace(0, rmax, nb + 1); idx = np.digitize(r.ravel(), edges) - 1
        ok = (idx >= 0) & (idx < nb)
        s = np.bincount(idx[ok], weights=rho.ravel()[ok], minlength=nb); c_ = np.bincount(idx[ok], minlength=nb)
        rc = 0.5 * (edges[1:] + edges[:-1])
        prof = np.where(c_ > 0, s / np.maximum(c_, 1), np.nan)
        return rc, prof, r


def half_radius(r, prof):
    """the half-density radius (linear interpolation on the first crossing of rho(0)/2), empty bins skipped."""
    ok = np.isfinite(prof); r, prof = r[ok], prof[ok]
    rc0 = prof[0]
    for i in range(1, len(prof)):
        if prof[i] <= 0.5 * rc0:
            f = (prof[i - 1] - 0.5 * rc0) / (prof[i - 1] - prof[i])
            return float(r[i - 1] + f * (r[i] - r[i - 1]))
    return float("nan")


def fit_core(r, prof, rho_peak, rmax_fac=2.5):
    """least-squares fit of the soliton form (rho_c, r_c) to log rho inside rmax_fac r_c; returns rho_c, r_c, rms log residual."""
    from scipy.optimize import least_squares
    rc0 = half_radius(r, prof)
    ok = np.isfinite(prof) & (prof > 0)
    for _ in range(3):
        m_ = ok & (r < rmax_fac * rc0)
        res = least_squares(lambda q: np.log(soliton_form(r[m_], math.exp(q[0]), math.exp(q[1]))) - np.log(prof[m_]),
                            [math.log(rho_peak), math.log(rc0)])
        rho_c, rc0 = math.exp(res.x[0]), math.exp(res.x[1])
    m_ = ok & (r < rmax_fac * rc0)
    resid = float(np.sqrt(np.mean((np.log(prof[m_]) - np.log(soliton_form(r[m_], rho_c, rc0))) ** 2)))
    return rho_c, rc0, resid


def soliton_form(r, rho_c, r_c):
    return rho_c * (1 + 0.091 * (r / r_c) ** 2) ** -8


def ground_state(box, M, sweeps=(400, 400, 400), seed_w=0.08):
    """imaginary-time propagation to the Schroedinger-Poisson ground state of mass M, centred in the box."""
    c = 0.5
    d = [((box.x - c + 0.5) % 1.0) - 0.5 for _ in range(3)]
    r2 = d[0][:, None, None] ** 2 + d[1][None, :, None] ** 2 + d[2][None, None, :] ** 2
    psi = np.exp(-r2 / (2 * seed_w ** 2)).astype(complex)
    psi *= math.sqrt(M / box.mass(psi))
    for nsw, fac in zip(sweeps, (4.0, 1.0, 0.25)):
        dt = fac * box.dx ** 2
        kin = np.exp(-0.5 * box.K2 * dt)
        for _ in range(nsw):
            V = box.potential(np.abs(psi) ** 2)
            psi *= np.exp(-0.5 * V * dt)
            psi = np.fft.ifftn(kin * np.fft.fftn(psi))
            V = box.potential(np.abs(psi) ** 2)
            psi *= np.exp(-0.5 * V * dt)
            psi *= math.sqrt(M / box.mass(psi))
    return psi


def part_A():
    box = Box(NA)
    # --- A2: ground states at M and 2M
    M1 = 40.0                                                         # the box must exceed the soliton's wave Jeans length
    g1 = ground_state(box, M1); g2 = ground_state(box, 1.5 * M1)
    out = {}
    fits = []
    for g, M in ((g1, M1), (g2, 1.5 * M1)):
        rho = np.abs(g) ** 2
        c = np.unravel_index(np.argmax(rho), rho.shape); c = [c[i] * box.dx for i in range(3)]
        rr, prof, _ = box.radial(rho, c, nb=400, rmax=0.45)
        rho_c, rc, resid = fit_core(rr, prof, float(rho.max()))
        fits.append(dict(M=M, r_c=rc, rho_c=rho_c, inv=rho_c * rc ** 4, Mrc=M * rc, resid=resid))
    out["ground"] = fits
    rr1, prof1, _ = box.radial(np.abs(g1) ** 2, [0.5, 0.5, 0.5], nb=400, rmax=0.45)
    okp = np.isfinite(prof1); rr1, prof1 = rr1[okp], prof1[okp]
    # --- the halo: 16 solitons scaled from the M1 ground state (s_M(r) = lam^-2 s(r / lam), M = M1 / lam)
    K = fits[0]["Mrc"]; rc_ic = RC_IC_CELLS * box.dx; Ms = K / rc_ic; lam = M1 / Ms
    amp = np.sqrt(np.maximum(prof1, 0.0)); rgrid = rr1
    rng = np.random.default_rng(11)
    pos = []
    while len(pos) < NSOL:
        p_ = rng.uniform(-R0, R0, 3)
        if np.linalg.norm(p_) <= R0:
            pos.append(0.5 + p_)
    Mtot = NSOL * Ms
    s_vir = math.sqrt(Mtot / (2 * R0))
    psi = np.zeros((NA,) * 3, complex)
    X = box.x
    for j in range(NSOL):
        d = [((X - pos[j][i] + 0.5) % 1.0) - 0.5 for i in range(3)]
        r = np.sqrt(d[0][:, None, None] ** 2 + d[1][None, :, None] ** 2 + d[2][None, None, :] ** 2)
        s = lam ** -2 * np.interp(r / lam, rgrid, amp, right=0.0)
        v = np.round(rng.normal(0, 0.3 * s_vir, 3) / (2 * np.pi)) * 2 * np.pi        # periodic plane-wave momenta
        ph = v[0] * X[:, None, None] + v[1] * X[None, :, None] + v[2] * X[None, None, :]
        psi += s * np.exp(1j * (ph + rng.uniform(0, 2 * np.pi)))
    psi *= math.sqrt(Mtot / box.mass(psi))
    M0 = box.mass(psi); E0, K0 = box.energy(psi)
    t_cross = R0 / s_vir; t_end = N_CROSS * t_cross
    dt = box.dx ** 2 / 6.0
    kin = np.exp(-0.5j * box.K2 * dt)
    nsteps = int(math.ceil(t_end / dt)); snaps = []
    V = box.potential(np.abs(psi) ** 2); vmax_dt = 0.0
    P(f"    halo: {NSOL} solitons of mass {Ms:.1f} (r_c {rc_ic:.4f} = {RC_IC_CELLS:.0f} cells), total {Mtot:.0f}; virial sigma "
      f"{s_vir:.1f}, crossing time {t_cross:.2e}; {nsteps} steps of {dt:.2e}   [{time.time() - T0:.0f}s]")
    rec_every = max(1, nsteps // 40)
    for it in range(nsteps):
        psi *= np.exp(-0.5j * V * dt)
        psi = np.fft.ifftn(kin * np.fft.fftn(psi))
        V = box.potential(np.abs(psi) ** 2)
        psi *= np.exp(-0.5j * V * dt)
        vmax_dt = max(vmax_dt, float(np.abs(V).max()) * dt)
        if it >= int(0.75 * nsteps) and (it % rec_every == 0 or it == nsteps - 1):
            rho = np.abs(psi) ** 2
            sm = np.fft.irfftn(np.fft.rfftn(rho) * np.exp(-0.5 * box.K2r * (1.5 * box.dx) ** 2), s=rho.shape)
            ci = np.unravel_index(np.argmax(sm), sm.shape); c = [ci[i] * box.dx for i in range(3)]
            rr, prof, _ = box.radial(rho, c, nb=400, rmax=0.45)
            rho_c_, r_c_, _ = fit_core(rr, prof, float(rho[ci]), rmax_fac=2.0)
            snaps.append(dict(c=c, prof=prof, rho_c=rho_c_, r_c=r_c_))
    M1_, (E1, K1) = box.mass(psi), box.energy(psi)
    rho = np.abs(psi) ** 2
    # time-averaged core
    rcs = np.array([s_["r_c"] for s_ in snaps]); rhocs = np.array([s_["rho_c"] for s_ in snaps])
    inv_core = float(np.nanmean(rhocs * rcs ** 4))
    prof_avg = np.nanmean(np.array([s_["prof"] for s_ in snaps]), axis=0); rr = box.radial(rho, snaps[-1]["c"], nb=400, rmax=0.45)[0]
    rc_avg, rhoc_avg = float(np.nanmean(rcs)), float(np.nanmean(rhocs))
    m_ = (rr < 2 * rc_avg) & np.isfinite(prof_avg) & (prof_avg > 0)
    resid = float(np.sqrt(np.mean((np.log(prof_avg[m_]) - np.log(soliton_form(rr[m_], rhoc_avg, rc_avg))) ** 2)))
    sig_h = math.sqrt(2 * K1 / M1_ / 3)
    rq = np.linspace(0, 20 * rc_avg, 4001)
    core_mass = float(np.trapezoid(4 * np.pi * rq ** 2 * soliton_form(rq, rhoc_avg, rc_avg), rq)) if hasattr(np, "trapezoid") else \
        float(np.trapz(4 * np.pi * rq ** 2 * soliton_form(rq, rhoc_avg, rc_avg), rq))
    # granules: density contrast about the radial mean in the envelope, its autocorrelation length along the axes
    c = snaps[-1]["c"]; rrf, proff, rgrid3 = box.radial(rho, c, nb=400, rmax=0.45)
    okf = np.isfinite(proff); mean3 = np.interp(rgrid3, rrf[okf], proff[okf])
    env = (rgrid3 > 2 * rc_avg) & (rgrid3 < 0.2)
    dlt = np.where(env, rho / np.maximum(mean3, 1e-30) - 1, 0.0)
    ac = []
    for sh in range(0, 12):
        prod = dlt * np.roll(dlt, sh, axis=0); ac.append(float(np.sum(prod[env & np.roll(env, sh, axis=0)])))
    ac = np.array(ac) / ac[0]
    lag = next((i for i in range(1, len(ac)) if ac[i] < math.exp(-1)), len(ac)) * box.dx
    out.update(Ms=Ms, Mtot=Mtot, sig_vir=s_vir, t_cross=t_cross, t_end=t_end, steps=nsteps, mass_drift=abs(M1_ / M0 - 1),
               energy_drift=abs(E1 / E0 - 1), E0=E0, E1=E1, vmax_dt=vmax_dt, core_r_c=rc_avg, core_rho_c=rhoc_avg,
               core_inv=inv_core, core_resid=resid, core_mass=core_mass, core_r_c_series=rcs.tolist(), sigma_halo=sig_h,
               lambda_dB=2 * math.pi / sig_h, granule_corr=lag, env_contrast_rms=float(np.sqrt(np.mean(dlt[env] ** 2))),
               r=rr.tolist(), prof=prof_avg.tolist(), slice=np.log10(np.maximum(rho[:, :, int(round(c[2] / box.dx)) % NA], 1e-6)).tolist())
    return out


# ================================================================================================ Part B: the heating
def bath_run(args):
    rho0, sig, seed, frozen, pot_on, orbits = args
    box = Box(NB)
    rng = np.random.default_rng(seed)
    amp = np.sqrt(np.exp(-box.K2 / (2 * sig ** 2)))
    ck = amp * np.exp(2j * np.pi * rng.random(box.K2.shape))
    psi0 = np.fft.ifftn(ck); psi0 *= math.sqrt(rho0 / np.mean(np.abs(psi0) ** 2))
    pk0 = np.fft.fftn(psi0)
    sig_s = sig / 3.0; sx = 0.15; om = sig_s / sx
    pos = 0.5 + rng.normal(0, sx, (NSTAR, 3)); vel = rng.normal(0, sig_s, (NSTAR, 3))
    tau = 1.0 / sig ** 2; T_orb = 2 * np.pi / om
    dt = min(tau / 10.0, T_orb / 400.0); t_end = orbits * T_orb; nst = int(math.ceil(t_end / dt)); dt = t_end / nst

    def acc(p_, t):
        a_ = -om ** 2 * (p_ - 0.5)
        if pot_on:
            psi = np.fft.ifftn(pk0 * (1.0 if frozen else np.exp(-0.5j * box.K2 * t)))
            g = box.gravity(np.abs(psi) ** 2)
            s = (p_ % 1.0) / box.dx; i0 = np.floor(s).astype(np.int64); f = s - i0; i0 %= NB; i1 = (i0 + 1) % NB
            for ax in range(3):
                val = 0.0
                for bx in (0, 1):
                    ix = i1[:, 0] if bx else i0[:, 0]; wx = f[:, 0] if bx else 1 - f[:, 0]
                    for by in (0, 1):
                        iy = i1[:, 1] if by else i0[:, 1]; wy = f[:, 1] if by else 1 - f[:, 1]
                        for bz in (0, 1):
                            iz = i1[:, 2] if bz else i0[:, 2]; wz = f[:, 2] if bz else 1 - f[:, 2]
                            val = val + g[ax][ix, iy, iz] * wx * wy * wz
                a_[:, ax] += val
        return a_
    E = lambda p_, v_: 0.5 * np.sum(v_ ** 2, axis=1) + 0.5 * om ** 2 * np.sum((p_ - 0.5) ** 2, axis=1)
    ts, Es = [0.0], [float(E(pos, vel).mean())]
    a = acc(pos, 0.0); t = 0.0
    rec = max(1, nst // 60)
    for it in range(nst):
        vel += 0.5 * dt * a; pos += dt * vel; t += dt; a = acc(pos, t); vel += 0.5 * dt * a
        if (it + 1) % rec == 0:
            ts.append(t); Es.append(float(E(pos, vel).mean()))
    ts, Es = np.array(ts), np.array(Es)
    # the early, linear heating: from half an orbit until the trap energy first rises by 25% (slow stars stay slow)
    hot = np.where(Es > 1.25 * Es[0])[0]
    t_stop = ts[hot[0]] if len(hot) else ts[-1]
    t_stop = max(t_stop, min(2.0 * T_orb, ts[-1]))
    m_ = (ts >= 0.5 * T_orb) & (ts <= t_stop)
    slope = float(np.polyfit(ts[m_], Es[m_], 1)[0])
    return args, dict(D=2 * slope, E0=Es[0], dE_rel=float(Es[-1] / Es[0] - 1), t_end=t_end, steps=nst, sig_s=sig_s, sx=sx, om=om,
                      lnL=math.log(sx * sig), ts=ts.tolist(), Es=Es.tolist())


# ================================================================================================ Part C: cosmology helpers
OM, OL, H0 = 0.3138, 0.6862, 67.36


def t_of_z(z):                                                      # Gyr, flat LCDM, no radiation
    a = 1.0 / (1 + z)
    return (2.0 / (3 * math.sqrt(OL))) * math.asinh(math.sqrt(OL / OM) * a ** 1.5) * 977.8 / H0


def z_clear(rho_dm, x_v0, p=2):
    """the redshift at which the vacuum-gated trigger fires in a region of fixed physical density rho_dm (Msun/pc^3)."""
    rho_m0 = OM * 2.775e11 * (H0 / 100) ** 2 * 1e-18                  # Msun/pc^3
    def u(z):
        E2 = OM * (1 + z) ** 3 + OL
        delta = rho_dm / (rho_m0 * (1 + z) ** 3) - 1
        return 1.5 * (OM * (1 + z) ** 3 / E2) * delta * (OL / E2 / OL) ** p
    zs = np.linspace(20, 0, 4001)
    for z_ in zs:
        if u(z_) >= x_v0:
            return float(z_)
    return 0.0


def floor_mass(C_sim, lnL_sim, rho, sig_dm, sig_s, r_h, t_gyr):
    """the minimum boson mass (eV) whose granule heating over t stays below the observed sigma_*^2 (1D)."""
    t = t_gyr * 1e3 / MYR_PER_PCKMS                                  # pc/(km/s)
    m = 1e-19
    for _ in range(60):
        hm = HBARM_1EV / m                                            # hbar/m, pc km/s
        lnL = max(math.log(r_h * sig_dm / hm), 1.0)
        C = C_sim * lnL / lnL_sim
        # D t / 3 = sig_s^2  with D = C G^2 rho^2 (hbar/m)^3 / sig^4  ->  (hbar/m)^3 = 3 sig_s^2 sig^4 / (C G^2 rho^2 t)
        hm_max = (3 * sig_s ** 2 * sig_dm ** 4 / (C * G_PC ** 2 * rho ** 2 * t)) ** (1.0 / 3.0)
        m_new = HBARM_1EV / hm_max
        if abs(m_new / m - 1) < 1e-10:
            break
        m = m_new
    return m_new


if __name__ == "__main__":
    P(__doc__.split("CHECKS")[0].strip())
    if MUTATE: P("\n  *** MUTATE=1: the bath is frozen (granules that never change); Part A is not rerun ***")
    if FAST: P("\n  *** FAST=1: code test on small grids; nothing is written here ***")
    RHO_B, SIG_B = (300.0, 12.0) if FAST else (350.0, 24.0)                    # heating stays in the slow-star regime
    KEYS = [(RHO_B, SIG_B, B_ORBITS), (2 * RHO_B, SIG_B, B_ORBITS), (2 * RHO_B, 1.5 * SIG_B, 2 * B_ORBITS)]
    jobs = [(k_[0], k_[1], s_, MUTATE, True, k_[2]) for k_ in KEYS for s_ in (1, 2)] + [(RHO_B, SIG_B, 1, MUTATE, False, B_ORBITS)]
    with Pool(int(os.environ.get("L383_POOL", "4"))) as pool:
        resB = pool.map_async(bath_run, jobs, chunksize=1)
        A = part_A() if not MUTATE else None
        RB = dict(resB.get())
    P(f"  Parts A and B done   [{time.time() - T0:.0f}s]")

    # ------------------------------------------------------------------------------------------ A
    if A is not None:
        banner("A  THE ZOOM-IN: ground states, the merged halo, its core and granules")
        g1, g2 = A["ground"]
        check("A1 NUMERICAL TRUST: the halo run conserves mass to 1e-10 and energy to 1%",
              f"mass drift {A['mass_drift']:.1e}; energy drift {A['energy_drift']:.2e} (E {A['E0']:.1f} -> {A['E1']:.1f}); "
              f"max |V| dt {A['vmax_dt']:.3f}", A["mass_drift"] < 1e-10 and A["energy_drift"] < 0.01)
        check("A2 CONTROL: the imaginary-time ground state has Schive et al. 2014's profile (rms log residual < 0.05 inside 2.5 "
              "r_c) and r_c ~ 1/M (the M, 1.5M ratio 2/3 within 3%)",
              f"M {g1['M']:.0f}: r_c {g1['r_c']:.4f}, residual {g1['resid']:.3f}; M {g2['M']:.0f}: r_c {g2['r_c']:.4f}, residual "
              f"{g2['resid']:.3f}; ratio {g2['r_c'] / g1['r_c']:.4f}; M r_c = {g1['Mrc']:.3f} / {g2['Mrc']:.3f}; rho_c r_c^4 = "
              f"{g1['inv']:.3f} / {g2['inv']:.3f}",
              g1["resid"] < 0.05 and g2["resid"] < 0.05 and abs(g2["r_c"] / g1["r_c"] / (2 / 3) - 1) < 0.03)
        inv_g = 0.5 * (g1["inv"] + g2["inv"])
        check("A3 THE CORE IS THE GROUND STATE: the relaxed halo's core has rho_c r_c^4 within 25% of the ground state's and the "
              "soliton profile inside 2 r_c (rms log residual < 0.12)",
              f"core r_c {A['core_r_c']:.4f} ({A['core_r_c'] * NA:.1f} cells), rho_c {A['core_rho_c']:.3g}; rho_c r_c^4 "
              f"{A['core_inv']:.3f} vs ground state {inv_g:.3f} (ratio {A['core_inv'] / inv_g:.3f}); residual {A['core_resid']:.3f}",
              abs(A["core_inv"] / inv_g - 1) < 0.25 and A["core_resid"] < 0.12)
        P(f"    halo: {NSOL} solitons, total mass {A['Mtot']:.0f}, evolved {A['t_end'] / A['t_cross']:.0f} crossing times; "
          f"sigma_halo {A['sigma_halo']:.1f} -> de Broglie length {A['lambda_dB']:.3f} ({A['lambda_dB'] * NA:.0f} cells); "
          f"granule correlation length {A['granule_corr']:.4f} (1/sigma = {1 / A['sigma_halo']:.4f}); envelope density "
          f"contrast rms {A['env_contrast_rms']:.2f}; soliton mass fraction {A['core_mass'] / A['Mtot']:.2f}")
        OUT["numbers"]["A"] = {k_: v for k_, v in A.items() if k_ != "slice"}
        try:
            import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
            fig, ax = plt.subplots(1, 2, figsize=(12.5, 5.0))
            im = ax[0].imshow(np.array(A["slice"]).T, origin="lower", extent=(0, 1, 0, 1), cmap="magma")
            ax[0].set_title("the wave field inside a halo: log10 density through the core\n(a solitonic core in an envelope of "
                            "interference granules)", fontsize=9)
            fig.colorbar(im, ax=ax[0], fraction=0.046)
            r_, p_ = np.array(A["r"]), np.array(A["prof"])
            ax[1].loglog(r_, p_, "k-", lw=2, label="halo (time-averaged)")
            rr_ = np.geomspace(r_[0], r_[-1], 200)
            ax[1].loglog(rr_, soliton_form(rr_, A["core_rho_c"], A["core_r_c"]), "C3--", label="ground-state soliton (fitted r_c)")
            ax[1].axvline(A["lambda_dB"], color="C0", ls=":", label="de Broglie length")
            ax[1].set_xlabel("r (box units)"); ax[1].set_ylabel("density (code units)"); ax[1].legend(fontsize=8)
            ax[1].set_ylim(max(np.nanmin(p_[p_ > 0]), A["core_rho_c"] * 1e-5), A["core_rho_c"] * 2)
            fig.tight_layout(); fig.savefig(os.path.join(OUTDIR, SLUG + ".png"), dpi=110); P(f"  figure: {SLUG}.png")
        except Exception as e_:
            P(f"  figure skipped: {e_}")

    # ------------------------------------------------------------------------------------------ B
    banner("B  THE HEATING: stars in a trap inside a wave bath (code units)")
    Dm, R1_ = {}, {}
    for key in KEYS:
        ds = [RB[(key[0], key[1], s_, MUTATE, True, key[2])]["D"] for s_ in (1, 2)]
        Dm[key] = float(np.mean(ds)); r0 = RB[(key[0], key[1], 1, MUTATE, True, key[2])]; R1_[key] = r0
        P(f"    rho {key[0]:.0f}, sigma {key[1]:.0f}: D = {ds[0]:.1f} / {ds[1]:.1f} (mean {Dm[key]:.1f}); stars sigma_* {r0['sig_s']:.1f}, "
          f"trap energy {r0['E0']:.1f} -> {100 * r0['dE_rel']:+.1f}% over {key[2]:.0f} orbits; ln Lambda {r0['lnL']:.2f}")
    off = RB[(RHO_B, SIG_B, 1, MUTATE, False, B_ORBITS)]
    check("B1 CONTROL: with the bath's potential switched off the stars' trap energy is conserved to 1e-3 (the integrator)",
          f"relative change {off['dE_rel']:.1e}", abs(off["dE_rel"]) < 1e-3)
    kA, kB, kC = KEYS
    r_rho = Dm[kB] / Dm[kA] if Dm[kA] != 0 else float("nan")
    lnr = R1_[kC]["lnL"] / R1_[kB]["lnL"]
    pred_sig = 1.5 ** -4 * lnr
    r_sig = Dm[kC] / Dm[kB] if Dm[kB] != 0 else float("nan")
    check("B2 THE QUASI-PARTICLE SCALING: doubling rho multiplies the heating by 4 (within 25%) -- the granules act as "
          "quasi-particles whose mass grows with rho", f"rho x2: x{r_rho:.2f} (4)", abs(r_rho / 4 - 1) < 0.25)
    check("B3 (reported) the sigma scaling: sigma x 1.5 against 1.5^-4 x the Coulomb-log ratio (the log model is rough at "
          "ln Lambda ~ 1.3-1.7)", f"x{r_sig:.3f} (predicted {pred_sig:.3f}; ratio {r_sig / pred_sig:.2f})", True, load_bearing=False)
    C_sim = Dm[kA] * kA[1] ** 4 / kA[0] ** 2                                # G = hbar/m = 1
    C_sim2 = Dm[kC] * kC[1] ** 4 / kC[0] ** 2
    lnL_sim, lnL_sim2 = R1_[kA]["lnL"], R1_[kC]["lnL"]
    Cp = 0.5 * (C_sim / lnL_sim + C_sim2 / lnL_sim2)                        # the coefficient per unit Coulomb log
    P(f"    D = C G^2 rho^2 (hbar/m)^3 / sigma^4 with C / ln Lambda = {C_sim / lnL_sim:.2f} (sigma {kA[1]:.0f}), {C_sim2 / lnL_sim2:.2f} "
      f"(sigma {kC[1]:.0f}); mean {Cp:.2f}.  (Quasi-particle estimate: 3 x pi^1.5 / 0.34 ~ {3 * math.pi ** 1.5 / 0.34:.0f}, with its "
      f"factor-of-2 conventions)")

    # ------------------------------------------------------------------------------------------ C
    banner("C  A SEGUE-1-LIKE ULTRA-FAINT DWARF: the boson-mass floor from granule heating, LCDM vs the framework's clearing")
    R_H, SIG_S, RHO_DM = 29.0, 3.7, 5.7
    ZF = 8.0; tf = t_of_z(ZF); t0 = t_of_z(0.0)
    TAB = {}
    for xv in (1000.0, 2000.0):
        zc = z_clear(RHO_DM, xv); TAB[f"z_clear|{xv:.0f}"] = zc
    for sdm in (5.0, 7.0, 10.0):
        row = {}
        row["LCDM"] = floor_mass(Cp, 1.0, RHO_DM, sdm, SIG_S, R_H, t0 - tf) if Cp > 0 else 0.0
        for xv in (1000.0, 2000.0):
            zc = TAB[f"z_clear|{xv:.0f}"]
            row[f"framework|{xv:.0f}"] = floor_mass(Cp, 1.0, RHO_DM, sdm, SIG_S, R_H, max(t_of_z(zc) - tf, 0.0) + 0.1) if Cp > 0 else 0.0
        TAB[f"sigma_dm={sdm:g}"] = row
        P(f"    sigma_DM {sdm:4.1f} km/s: floor LCDM {row['LCDM']:.2e} eV (exposure {t0 - tf:.1f} Gyr); framework {row['framework|1000']:.2e} "
          f"(x_v0 1000, cleared at z = {TAB['z_clear|1000']:.2f}, exposure {t_of_z(TAB['z_clear|1000']) - tf + 0.1:.2f} Gyr) / "
          f"{row['framework|2000']:.2e} (x_v0 2000, z = {TAB['z_clear|2000']:.2f})")
    lc = TAB["sigma_dm=7"]["LCDM"]
    check("C1 CONTROL: with LCDM's exposure the floor is within a factor 5 of Dalal & Kravtsov's 3e-19 eV (sigma_DM 7 km/s)",
          f"{lc:.2e} eV (ratio {lc / 3e-19:.2f})", 3e-19 / 5 <= lc <= 3e-19 * 5 if not MUTATE else lc < 3e-19 / 5,
          reading="under MUTATE the frozen bath does not heat: the floor collapses (the inverted control)" if MUTATE else "")
    fw = max(TAB[f"sigma_dm={s:g}"][f"framework|{x:.0f}"] for s in (5.0, 7.0, 10.0) for x in (1000.0, 2000.0))
    check("R1 = H: with the framework's clearing the ultra-faint-dwarf floor falls to <= 2e-20 eV (the forest bound) for every "
          "sigma_DM 5-10 km/s and x_v0 1000-2000", f"highest framework floor {fw:.2e} eV", (fw <= 2e-20) == EXPECT_OPENS)
    check("W (reported) the floors with and without the clearing", "see above", True, load_bearing=False)
    OUT["numbers"].update(C_per_lnL=Cp, C_sim=C_sim, C_sim2=C_sim2,
                          lnL_sim=[lnL_sim, lnL_sim2], ratios=dict(rho=r_rho, sigma=r_sig, sigma_pred=pred_sig), C=TAB,
                          ufd=dict(r_h=R_H, sigma_s=SIG_S, rho_dm=RHO_DM, z_form=ZF), bath_runs={str(k): {kk: vv for kk, vv in v.items()
                          if kk not in ("ts", "Es")} for k, v in RB.items()})
    OUT["numbers"]["B"] = {f"{k[0]:.0f}|{k[1]:.0f}": v for k, v in Dm.items()}
    banner("VERDICT")
    n_fail = sum(1 for _, ok_, lb in CH if lb and not ok_)
    OUT["n_checks"], OUT["n_fail_load_bearing"] = len(CH), n_fail
    json.dump(OUT, open(os.path.join(OUTDIR, SLUG + "_results.json"), "w"), indent=1,
              default=lambda o: o.tolist() if hasattr(o, "tolist") else str(o))
    P(f"  {sum(1 for _, ok_, _ in CH if ok_)}/{len(CH)} checks pass; load-bearing failures: {n_fail}; wrote {SLUG}_results.json   "
      f"[{time.time() - T0:.0f}s]")
    P(f"rc={0 if n_fail == 0 else 1}")
    sys.exit(0 if n_fail == 0 else 1)
