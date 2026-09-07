#!/usr/bin/env python3
"""
g04k -- the load-bearing number, stress-tested in 3D: cold collisionless infall onto a MOND-boosted disc with particles
=========================================================================================================================
Every dark-sector verdict of 2026-09-06 (the relic pincer g04i, the wave pincer g04j, the "no mechanism" sentence) rests on the
spherical shell model g03r: cold infall delivers M/M_b = 2.7-3.3 inside 10 kpc, 8.7-9.5 inside 30 kpc, 24 inside 100 kpc for a
5e10 Msun disc.  A shell model is radial by construction: every particle that reaches r < 10 kpc counts, angular momentum never
stops it, and the baryons are a sphere.  This script repeats the calculation with 3D particles in a flattened disc potential,
with initial random velocities and the cosmological external field, and asks the only question that matters for the pincers:
does the mass inside 10 and 30 kpc stay above the RAR's 25% tolerance, and inside 100 kpc above KiDS's 14% of a CDM-like halo?

Setup (mirrors g03r where it can): a Lagrangian sphere of 8 cosmic shares (M_share = M_b0 Od/Ob) of collisionless dust, uniform
at z_i = 20 with the secondary-infall seed delta(<r) = delta_0 R_share/r (capped at 1, compensated outside R_share; delta_0 =
1.686 (1+z_c)/(1+z_i), z_c = 1 for the galaxy system), Hubble flow plus the linear growing-mode peculiar velocity, plus an
isotropic random velocity sigma_i (0, 20, 60 km/s at z_i).  Baryons: a Miyamoto-Nagai disc (a = 3 kpc, b = 0.3 kpc; a Plummer
sphere in the 'spherical' control) whose mass is the cosmic baryon share of the dust that has fallen inside 50 kpc, capped at
M_b0 = 5e10 Msun (mass conservation, as in g03r).  Forces: analytic disc + dust monopole from sorted radii (softening 0.5 kpc)
+ Lambda's repulsion; MOND as algebraic QUMOND on the internal Newtonian field with the external field g_ext = 0.02 a0 in the
kernel argument (nu_RAR saturated at Delta = 0.6476, THE_ACTION section 3).  KDK leapfrog, adaptive global step, z_i = 20 to z = 0.
Both footings.

  P0 [kernel]      the disc alone gives the deep-MOND flat speed (G M_b a0)^1/4 at 30 kpc to 10% (canonical, no EFE);
  P1 [shell]       the radial 3D run (sigma_i = 0, spherical baryons) reproduces g03r's M(<10 kpc)/M_b within a factor 2 -- the
                   like-for-like anchor that says the two codes agree where they should;
  P2 [control]     the Newtonian run (boost off, sigma_i = 20, disc) delivers a CDM-like inner mass, M(<10 kpc)/M_b in [0.3, 5];
  P3 [THE TEST]    with angular momentum and the flattened disc (sigma_i = 20 and 60 km/s), M(<10 kpc) < 0.25 M_b, both footings;
  P4 [BTFR]        the same inside 30 kpc;
  P5 [KiDS]        M_MOND(<100 kpc) < 0.14 M_Newton(<100 kpc) (the Newtonian run as the CDM-like reference with identical ICs).
PASS on P3-P5 would REOPEN the dark-sector door for plain cold dust; FAIL confirms the shell model's verdict with a stronger tool.

OUTCOME (2026-09-07 run, 3 FAIL of 6, 60k particles, 13.6k steps per run): P0 kernel 168 vs 158 km/s; P1 the radial 3D run reproduces
the shell model (2.65 vs 2.71 inside 10 kpc, 8.89 vs 8.68 inside 30 kpc); P2 the Newtonian control is CDM-like (0.35 M_b inside 10 kpc);
P3 FAIL -- with angular momentum and the flattened disc the dust inside 10 kpc is 2.58 M_b (sigma_i = 20 km/s), 1.52 (60 km/s), 2.64 (alt);
P4 FAIL -- 8.1-9.3 M_b inside 30 kpc; P5 FAIL -- the MOND runs hold 12x the Newtonian control's mass inside 100 kpc (the boost pulls the
cosmic share in).  The shell model's number survives in 3D; the dark-sector no-go stands on a collisionless calculation with angular
momentum, a disc and the external field.
"""
import numpy as np, math, json, sys, time
FAILS = []
def check(name, ok, detail=""):
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f"   ({detail})" if detail else ""), flush=True)
    if not ok: FAILS.append(name)
T0 = time.time()
G = 6.674e-11; c = 2.998e8; MSUN = 1.989e30; kpc = 3.0857e19; Mpc = 3.0857e22; GYR = 3.156e16
h = 0.674; H0 = h*100e3/Mpc; Om, OL, Ob, Od = 0.315, 0.685, 0.049, 0.266; rho_c = 3*H0**2/(8*math.pi*G)
A0 = {"canonical": 9.3619e-11, "alt": 1.1279e-10}; GEXT_FRAC = 0.02
Mb0 = 5e10*MSUN; ZI = 20.0; ZC = 1.0; NPART = 60_000; SOFT = 0.5*kpc; A_MN, B_MN = 3*kpc, 0.3*kpc
print("=" * 118); print("g04k -- cold collisionless infall onto a MOND-boosted disc, 3D particles (the shell model's number, stress-tested)"); print("=" * 118, flush=True)
Hz = lambda a: H0*math.sqrt(Om*a**-3 + OL)
def t_of_a(a):
    aa = np.linspace(1e-6, a, 20000); return float(np.trapz(1/(aa*H0*np.sqrt(Om*aa**-3 + OL)), aa))
TA = np.geomspace(1e-4, 1.0, 4000); TT = np.array([t_of_a(x) for x in TA]); a_of_t = lambda t: float(np.interp(t, TT, TA))
# ---- kernel (nu_RAR carried, saturated) ----
def Delta(s):
    s = np.asarray(s, dtype=float); d = np.where(s > 0, s/np.expm1(np.sqrt(np.maximum(s, 1e-300))), 0.0)
    return np.where(s > 2.540, 0.6476, d)
# ---- initial conditions ----
def make_ics(sigma_i, rng):
    ai = 1/(1 + ZI); Mshare = Mb0*Od/Ob; Rshare = (Mshare/(Od*rho_c*ai**-3*4*math.pi/3))**(1/3)      # physical share radius at z_i
    ML = 8*Mshare; RL = (ML/(Od*rho_c*ai**-3*4*math.pi/3))**(1/3)
    # uniform sphere, then the seed: enclosed-mass-preserving radial map r -> r (1 + delta(<r))^(-1/3)
    u = rng.random(NPART); r0 = RL*u**(1/3)
    delta0 = 1.686*(1 + ZC)/(1 + ZI); dbar = np.minimum(delta0*Rshare/np.maximum(r0, 1e-3*kpc), 1.0)
    # compensate outside R_share so the total mass inside RL is unchanged: subtract the excess uniformly from R_share..RL
    excess = np.mean(dbar[r0 < Rshare])*(Rshare/RL)**3 if np.any(r0 < Rshare) else 0.0
    dbar = np.where(r0 < Rshare, dbar, -excess/(1 - (Rshare/RL)**3))
    r = r0*(1 + dbar)**(-1/3)
    dirs = rng.normal(size=(NPART, 3)); dirs /= np.linalg.norm(dirs, axis=1)[:, None]
    x = r[:, None]*dirs
    # Hubble flow + linear growing-mode infall (-1/3 H delta r) + random velocities
    v = (Hz(ai)*r*(1 - dbar/3))[:, None]*dirs + sigma_i*rng.normal(size=(NPART, 3))
    return x, v, ML/NPART, Rshare
# ---- forces ----
def disc_acc(x, Mdisc, kind):
    X, Y, Z = x[:, 0], x[:, 1], x[:, 2]
    if kind == "spherical":
        r2 = X*X + Y*Y + Z*Z + A_MN**2; f = -G*Mdisc/r2**1.5; return f[:, None]*x
    zb = np.sqrt(Z*Z + B_MN**2); D = X*X + Y*Y + (A_MN + zb)**2; f = -G*Mdisc/D**1.5
    return np.stack([f*X, f*Y, f*Z*(A_MN + zb)/zb], axis=1)
def dust_monopole(x, mp):
    r = np.linalg.norm(x, axis=1); order = np.argsort(r); Menc = np.empty(len(r)); Menc[order] = mp*np.arange(1, len(r) + 1)
    rs = np.sqrt(r*r + SOFT*SOFT); f = -G*Menc/rs**3
    return f[:, None]*x, r, Menc, order
def accel(x, mp, a, a0, mond, kind, gext_vec):
    acc_d, r, Menc, order = dust_monopole(x, mp)
    # disc mass = baryon share of the dust inside 50 kpc, capped
    Mdisc = min(Mb0, (Ob/Od)*mp*np.searchsorted(np.sort(r), 50*kpc))
    gN = acc_d + disc_acc(x, Mdisc, kind)
    if mond:
        gtot = gN + gext_vec[None, :]; s = np.linalg.norm(gtot, axis=1)/a0; nu_minus_1 = Delta(s)/np.maximum(s, 1e-30)
        gN = gN*(1 + nu_minus_1)[:, None]
    gN += (OL*H0**2)*x                                                                              # Lambda's repulsion (physical coordinates)
    return gN, Mdisc, r
def run(sigma_i, mond=True, kind="disc", a0=A0["canonical"], seed=1, label=""):
    rng = np.random.default_rng(seed); x, v, mp, Rshare = make_ics(sigma_i, rng)
    gext_vec = np.array([0.0, 0.0, GEXT_FRAC*a0]); ai = 1/(1 + ZI); t = t_of_a(ai); t_end = t_of_a(1.0)
    acc, Mdisc, r = accel(x, mp, ai, a0, mond, kind, gext_vec); nstep = 0; t1 = time.time()
    samples = []; t_avg_from = t_end - 1.0*GYR
    while t < t_end:
        vmag = np.linalg.norm(v, axis=1) + 1e3; amag = np.linalg.norm(acc, axis=1) + 1e-20
        dt = 0.03*min(float(np.min(np.sqrt((r + SOFT)/amag))), float(np.min((r + SOFT)/vmag))); dt = min(dt, 0.05*GYR, t_end - t); dt = max(dt, 1e-3*GYR)
        v += 0.5*dt*acc; x += dt*v; t += dt
        acc, Mdisc, r = accel(x, mp, a_of_t(t), a0, mond, kind, gext_vec); v += 0.5*dt*acc; nstep += 1
        if t >= t_avg_from and (nstep % 5 == 0):
            samples.append([mp*np.sum(r < R)/Mb0 for R in (10*kpc, 30*kpc, 100*kpc, 200*kpc)])
    S = np.array(samples) if samples else np.array([[mp*np.sum(r < R)/Mb0 for R in (10*kpc, 30*kpc, 100*kpc, 200*kpc)]])
    out = dict(M10=float(S[:, 0].mean()), M30=float(S[:, 1].mean()), M100=float(S[:, 2].mean()), M200=float(S[:, 3].mean()), Mdisc=Mdisc/Mb0, steps=nstep, secs=time.time() - t1)
    print(f"    {label:44s}: M/M_b inside 10, 30, 100, 200 kpc = {out['M10']:.2f}, {out['M30']:.2f}, {out['M100']:.1f}, {out['M200']:.1f}  (disc {out['Mdisc']:.2f} M_b0; {nstep} steps, {out['secs']:.0f}s)", flush=True)
    return out
# ---- P0: kernel sanity ----
a0c = A0["canonical"]; xr = np.array([[30*kpc, 0.0, 0.0]]); g = -disc_acc(xr, Mb0, "disc")[0, 0]; s = g/a0c; gtot = g*(1 + float(Delta(s))/s)
vflat = math.sqrt(gtot*30*kpc); vpred = (G*Mb0*a0c)**0.25
check("P0 [kernel] the disc alone gives the deep-MOND flat speed (G M_b a0)^1/4 at 30 kpc to 10% (canonical, no EFE)", abs(vflat/vpred - 1) < 0.10, f"{vflat/1e3:.0f} vs {vpred/1e3:.0f} km/s, s = {s:.3f}")
# ---- runs ----
R = {}
R["shell-like"] = run(0.0, mond=True, kind="spherical", label="MOND, sigma_i = 0, spherical baryons (shell-like)")
R["newton"] = run(20e3, mond=False, kind="disc", label="NEWTON control, sigma_i = 20 km/s, disc")
R["mond20"] = run(20e3, mond=True, kind="disc", label="MOND, sigma_i = 20 km/s, disc (canonical)")
R["mond60"] = run(60e3, mond=True, kind="disc", label="MOND, sigma_i = 60 km/s, disc (canonical)")
R["mond20alt"] = run(20e3, mond=True, kind="disc", a0=A0["alt"], label="MOND, sigma_i = 20 km/s, disc (alt footing)")
check("P1 [shell] the radial 3D run reproduces g03r's cold-infall M(<10 kpc)/M_b = 2.71 within a factor 2", 0.5 < R["shell-like"]["M10"]/2.71 < 2.0, f"3D radial {R['shell-like']['M10']:.2f} vs shell 2.71; inside 30 kpc {R['shell-like']['M30']:.2f} vs 8.68; 100 kpc {R['shell-like']['M100']:.1f} vs 23.9")
check("P2 [control] the Newtonian run delivers a CDM-like inner mass, M(<10 kpc)/M_b in [0.3, 5]", 0.3 < R["newton"]["M10"] < 5.0, f"{R['newton']['M10']:.2f}")
check("P3 [THE TEST] with angular momentum and the flattened disc the mass inside 10 kpc is below 25% of the baryons (sigma_i = 20 and 60 km/s, both footings)", all(R[k]["M10"] < 0.25 for k in ("mond20", "mond60", "mond20alt")), json.dumps({k: round(R[k]["M10"], 2) for k in ("mond20", "mond60", "mond20alt")}))
check("P4 [BTFR] the same inside 30 kpc", all(R[k]["M30"] < 0.25 for k in ("mond20", "mond60", "mond20alt")), json.dumps({k: round(R[k]["M30"], 2) for k in ("mond20", "mond60", "mond20alt")}))
check("P5 [KiDS] the MOND runs hold less than 14% of the Newtonian control's mass inside 100 kpc", all(R[k]["M100"] < 0.14*R["newton"]["M100"] for k in ("mond20", "mond60")), f"MOND/Newton inside 100 kpc = {R['mond20']['M100']/R['newton']['M100']:.2f}, {R['mond60']['M100']/R['newton']['M100']:.2f}")
print(f"\n  caveats: dust self-gravity as a monopole (the dust stays near-spherical; the disc is the flattened part), algebraic QUMOND with the external field in the kernel argument, an isolated vacuole of 8 shares (no tides beyond it), z_i = 20 against the shell model's 50.  total {time.time()-T0:.0f}s")
print(f"\nRESULT: {len(FAILS)} FAIL" + (f" -> {FAILS}" if FAILS else "")); sys.exit(0)
