#!/usr/bin/env python3
"""
L1 -- the load-bearing number re-run with caustics resolved and the acceleration cap repaired
=============================================================================================
Every dark-sector verdict of 2026-09-06/07 rests on one number: cold collisionless dust falling onto a MOND-boosted 5e10 Msun
disc delivers M/M_b ~ 2.6-3.3 inside 10 kpc, ~10x the ~0.25 M_b the RAR tolerates.  It was computed twice (g03r spherical shells,
g04k 60k 3D particles).  Both share TWO gaps, and both gaps are gaps in MY OWN no-go, so both are tested here as hard as a win
would be tested:

  (a) CAUSTICS.  g04k's dust self-gravity is a MONOPOLE from sorted radii (`dust_monopole`).  A monopole is exact only for a
      sphere; it smooths over shell-crossing, caustic sheets and any aspherical collapse -- exactly the structure cold
      collisionless infall develops.  "Caustic-quenched dust" is on the programme's own list of untested survivors.
  (b) THE CAP.  g04k's MOND step is  g = gN_int * (1 + Delta(s)/max(s,1e-30)),  s = |gN_int + g_ext|/a0.  The intended physics is
      that the boost adds at most Delta_max = 0.6476 a0 of acceleration.  Multiplying the INTERNAL field by a multiplier
      evaluated on the TOTAL field loses that cap: the added acceleration is a0 Delta(s) |gN_int|/|gN_tot|, which is unbounded
      where the internal and external fields cancel (a real surface, at |gN_int| = g_ext = 0.02 a0, i.e. ~60-100 kpc up the
      external-field axis, inside the apertures being measured).  This is the lead reviewer's criticism in
      review_reconciliation_2026/PATH_FORWARD.md, quoted there as "loss of the intended physical acceleration cap and strong
      cancellation sensitivity" -- the earlier stronger "literal divergence" claim was withdrawn and is NOT repeated here.

REPAIRS.
  (a) Force.  A softened SPHERICAL-HARMONIC (multipole) solver to l <= LMAX = 6 on the sorted particles, self excluded:
      Phi = -G sum_lm 4pi/(2l+1) Y_lm(Omega) [ rho^-(l+1) S_in,lm(rho) + rho^l S_out,lm(rho) ],  rho = sqrt(r^2 + SOFT^2),
      SOFT = 0.5 kpc (the same softening g04k uses).  With that rho the l = 0 term is EXACTLY g04k's monopole, so the two
      calculations are nested and the difference is entirely the l >= 1 (non-radial) force.  Radial force analytic; tangential
      force by a central difference in two orthogonal tangent directions at FIXED rho (the radial sums do not move), eps = 1e-3
      rad.  A direct O(N^2) summation is also implemented and run as a cross-check.
  (b) Multiplier.  The bounded QUMOND external-field form, g_int = [gN_tot + a0 Delta(s_tot) ghat_tot] - [g_ext + a0 Delta(s_ext)
      ghat_ext].  Identical to g04k when g_ext = 0; bounded by |g - gN| <= 2 Delta_max a0 = 1.295 a0 everywhere, including exact
      cancellation, where it correctly returns the finite external-field-subtracted value.

CHECKS THAT CAN FAIL
  V1 [solver]    the multipole solver reproduces the monopole for a spherically symmetric configuration: binned-mean radial
                 acceleration to 1%, and the per-particle residual is the expansion's own Poisson noise (falls as N^-1/2);
  V2 [solver]    it also gets a case the monopole CANNOT: the interior field of a homogeneous oblate spheroid (q = 0.5, analytic)
                 to better than 10%, where the monopole is 38% wrong -- i.e. it really does resolve non-radial structure;
  V3 [cap]       the repaired multiplier's added acceleration stays below 1.30 a0 across a sweep straight through exact
                 internal/external cancellation, while g04k's exceeds 100 a0 on the same sweep;
  V4 [anchor]    monopole + g04k multiplier at this N reproduces g04k's published M(<10 kpc)/M_b = 2.58 within a factor 1.5;
  P3 [THE TEST]  with caustics resolved AND the cap repaired, M(<10 kpc) < 0.25 M_b for both dispersions and both a0 footings.
                 A PASS REOPENS the dark-sector door for plain cold dust.  Nothing here is tuned to reach it or to avoid it.
  P4 [BTFR]      the same inside 30 kpc.

HONESTY CONTROLS (these decide whether a PASS would mean anything).  A direct N-body sum at affordable N has TWO biases that both
push toward a PASS, so neither the direct runs nor a coarse timestep is allowed to carry the verdict:
  * particle noise in gN feeds the algebraic multiplier, and nu is a steeply falling function of |gN|, so a grainy field is
    boosted LESS than the smooth field it samples -> less infall.  Measured here by running direct at two N.
  * a coarse global timestep leaks mass out of the aperture.  Measured here by re-running the monopole at half the step floor.
Both are reported next to the answer, in the direction they push.
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
Mb0 = 5e10*MSUN; ZI = 20.0; ZC = 1.0; SOFT = 0.5*kpc; A_MN, B_MN = 3*kpc, 0.3*kpc
LMAX = 6; NMULTI = 10_000; NDIRECT = 3_000; DTFLOOR = 3e-3          # Gyr; see the timestep control at the end
print("=" * 122)
print("L1 -- cold collisionless infall onto a MOND-boosted disc, with CAUSTICS RESOLVED (l <= 6) and the ACCELERATION CAP REPAIRED")
print("=" * 122, flush=True)

# ---------------------------------------------------------------- cosmology (identical to g04k) ----
Hz = lambda a: H0*math.sqrt(Om*a**-3 + OL)
def t_of_a(a):
    aa = np.linspace(1e-6, a, 20000); return float(np.trapz(1/(aa*H0*np.sqrt(Om*aa**-3 + OL)), aa))
TA = np.geomspace(1e-4, 1.0, 4000); TT = np.array([t_of_a(x) for x in TA]); a_of_t = lambda t: float(np.interp(t, TT, TA))

# ---------------------------------------------------------------- kernel (nu_RAR, saturated) -------
def Delta(s):
    s = np.asarray(s, dtype=float); d = np.where(s > 0, s/np.expm1(np.sqrt(np.maximum(s, 1e-300))), 0.0)
    return np.where(s > 2.540, 0.6476, d)
DMAX = 0.6476

# ---------------------------------------------------------------- initial conditions (g04k's) ------
def make_ics(sigma_i, rng, N):
    ai = 1/(1 + ZI); Mshare = Mb0*Od/Ob; Rshare = (Mshare/(Od*rho_c*ai**-3*4*math.pi/3))**(1/3)
    ML = 8*Mshare; RL = (ML/(Od*rho_c*ai**-3*4*math.pi/3))**(1/3)
    u = rng.random(N); r0 = RL*u**(1/3)
    delta0 = 1.686*(1 + ZC)/(1 + ZI); dbar = np.minimum(delta0*Rshare/np.maximum(r0, 1e-3*kpc), 1.0)
    excess = np.mean(dbar[r0 < Rshare])*(Rshare/RL)**3 if np.any(r0 < Rshare) else 0.0
    dbar = np.where(r0 < Rshare, dbar, -excess/(1 - (Rshare/RL)**3))
    r = r0*(1 + dbar)**(-1/3)
    dirs = rng.normal(size=(N, 3)); dirs /= np.linalg.norm(dirs, axis=1)[:, None]
    x = r[:, None]*dirs
    v = (Hz(ai)*r*(1 - dbar/3))[:, None]*dirs + sigma_i*rng.normal(size=(N, 3))
    return x, v, ML/N

# ---------------------------------------------------------------- baryons (g04k's Miyamoto-Nagai) --
def disc_acc(x, Mdisc, kind):
    X, Y, Z = x[:, 0], x[:, 1], x[:, 2]
    if kind == "spherical":
        r2 = X*X + Y*Y + Z*Z + A_MN**2; f = -G*Mdisc/r2**1.5; return f[:, None]*x
    zb = np.sqrt(Z*Z + B_MN**2); D = X*X + Y*Y + (A_MN + zb)**2; f = -G*Mdisc/D**1.5
    return np.stack([f*X, f*Y, f*Z*(A_MN + zb)/zb], axis=1)

# ---------------------------------------------------------------- force solvers --------------------
def _harm_index(L):
    idx = []
    for l in range(L + 1):
        idx.append((l, 0, 'c'))
        for m in range(1, l + 1): idx.append((l, m, 'c')); idx.append((l, m, 's'))
    return idx
IDX = _harm_index(LMAX); LVEC = np.array([i[0] for i in IDX], dtype=float); NC = len(IDX)
CFAC = 4*math.pi/(2*LVEC + 1)
def real_sph(n):
    """(N,3) unit vectors -> (NC,N) real orthonormal spherical harmonics, stable normalised recurrence."""
    u = n[:, 2]; s = np.sqrt(np.maximum(1.0 - u*u, 1e-30))
    cph = np.where(s > 1e-15, n[:, 0]/s, 1.0); sph = np.where(s > 1e-15, n[:, 1]/s, 0.0)
    N = len(u); P = {(0, 0): np.full(N, math.sqrt(1.0/(4*math.pi)))}
    for m in range(1, LMAX + 1): P[(m, m)] = -math.sqrt((2*m + 1)/(2.0*m))*s*P[(m - 1, m - 1)]
    for m in range(0, LMAX): P[(m + 1, m)] = math.sqrt(2.0*m + 3.0)*u*P[(m, m)]
    for m in range(0, LMAX + 1):
        for l in range(m + 2, LMAX + 1):
            a = math.sqrt((4.0*l*l - 1.0)/(l*l - m*m)); b = math.sqrt(((l - 1.0)**2 - m*m)/(4.0*(l - 1.0)**2 - 1.0))
            P[(l, m)] = a*(u*P[(l - 1, m)] - b*P[(l - 2, m)])
    cm = [np.ones(N)]; sm = [np.zeros(N)]
    for m in range(1, LMAX + 1):
        cm.append(cm[m - 1]*cph - sm[m - 1]*sph); sm.append(sm[m - 1]*cph + cm[m - 1]*sph)
    Y = np.empty((NC, N))
    for k, (l, m, t) in enumerate(IDX):
        Y[k] = P[(l, 0)] if m == 0 else math.sqrt(2.0)*P[(l, m)]*(cm[m] if t == 'c' else sm[m])
    return Y
def multipole_acc(x, mp, eps_ang=1e-3):
    """Softened self-gravity of N equal-mass particles to l <= LMAX.  l = 0 term == monopole_acc exactly."""
    r = np.linalg.norm(x, axis=1); rho = np.sqrt(r*r + SOFT*SOFT)/kpc
    n = x/np.maximum(r, 1e-12)[:, None]
    o = np.argsort(rho); rs = rho[o]; ns = n[o]; Ys = real_sph(ns)
    rl = rs[None, :]**LVEC[:, None]; rml = 1.0/(rs[None, :]**(LVEC[:, None] + 1.0))
    Win = Ys*rl; Wout = Ys*rml
    Sin = np.cumsum(Win, axis=1) - Win                                   # strictly interior
    Sout = np.cumsum(Wout[:, ::-1], axis=1)[:, ::-1] - Wout              # strictly exterior
    dPhi = -(G*mp/kpc**2)*np.einsum('kn,kn->n', Ys*CFAC[:, None],
                                    (-(LVEC[:, None] + 1.0)*rml*Sin + LVEC[:, None]*rl*Sout)/rs[None, :])
    Ck = CFAC[:, None]*(rml*Sin + rl*Sout)
    t1 = np.cross(ns, np.array([0.0, 0.0, 1.0])); bad = np.linalg.norm(t1, axis=1) < 1e-8
    t1[bad] = np.cross(ns[bad], np.array([1.0, 0.0, 0.0])); t1 /= np.linalg.norm(t1, axis=1)[:, None]
    t2 = np.cross(ns, t1); acc_t = np.zeros((len(rs), 3))
    for tv in (t1, t2):
        npv = ns + eps_ang*tv; npv /= np.linalg.norm(npv, axis=1)[:, None]
        nmv = ns - eps_ang*tv; nmv /= np.linalg.norm(nmv, axis=1)[:, None]
        dA = (np.einsum('kn,kn->n', Ck, real_sph(npv)) - np.einsum('kn,kn->n', Ck, real_sph(nmv)))/(2.0*math.atan(eps_ang))
        acc_t += (G*mp/kpc**2)*(dA/rs)[:, None]*tv
    a = np.empty_like(x); a[o] = (-dPhi*(r[o]/kpc)/rs)[:, None]*ns + acc_t
    return a, r
def monopole_acc(x, mp):
    r = np.linalg.norm(x, axis=1); o = np.argsort(r); Menc = np.empty(len(r))
    Menc[o] = mp*np.arange(0, len(r))                                    # strictly interior, matches the l=0 multipole term
    rs = np.sqrt(r*r + SOFT*SOFT); f = -G*Menc/rs**3
    return f[:, None]*x, r
def direct_acc(x, mp):
    n2 = np.einsum('ij,ij->i', x, x)
    r2 = n2[:, None] + n2[None, :] - 2.0*(x @ x.T)
    np.maximum(r2, 0.0, out=r2); r2 += SOFT*SOFT
    inv = 1.0/(r2*np.sqrt(r2)); s = inv.sum(axis=1)
    return G*mp*((inv @ x) - s[:, None]*x), np.sqrt(n2)
SOLVER = {"mono": monopole_acc, "multi": multipole_acc, "direct": direct_acc}

# ---------------------------------------------------------------- the MOND step, two versions ------
def mond_g04k(gN, gext, a0):
    """g04k as written: internal field times a multiplier evaluated on the total field."""
    s = np.linalg.norm(gN + gext[None, :], axis=1)/a0
    return gN*(1 + Delta(s)/np.maximum(s, 1e-30))[:, None]
def mond_repaired(gN, gext, a0):
    """Bounded QUMOND external-field form: boost the total, then subtract the boosted external field."""
    gt = gN + gext[None, :]; nt = np.linalg.norm(gt, axis=1)
    ht = np.where(nt[:, None] > 0, gt/np.maximum(nt, 1e-300)[:, None], 0.0)
    ne = np.linalg.norm(gext); he = gext/ne if ne > 0 else gext*0.0
    return gN + a0*(Delta(nt/a0)[:, None]*ht - Delta(ne/a0)*he[None, :])
MOND = {"g04k": mond_g04k, "repaired": mond_repaired}

def accel(x, mp, a0, mond, kind, gext, solver, track):
    acc_d, r = SOLVER[solver](x, mp)
    Mdisc = min(Mb0, (Ob/Od)*mp*np.searchsorted(np.sort(r), 50*kpc))
    gN = acc_d + disc_acc(x, Mdisc, kind)
    if mond != "off":
        g = MOND[mond](gN, gext, a0)
        track[0] = max(track[0], float(np.max(np.linalg.norm(g - gN, axis=1)))/a0)
        gN = g
    gN += (OL*H0**2)*x
    return gN, Mdisc, r

# ---------------------------------------------------------------- the integrator (g04k's) ----------
def run(sigma_i, solver="multi", mond="repaired", kind="disc", a0=A0["canonical"], seed=1, N=NMULTI,
        dtfloor=DTFLOOR, label="", diag=False):
    rng = np.random.default_rng(seed); x, v, mp = make_ics(sigma_i, rng, N)
    gext = np.array([0.0, 0.0, GEXT_FRAC*a0]); ai = 1/(1 + ZI); t = t_of_a(ai); t_end = t_of_a(1.0)
    track = [0.0]
    acc, Mdisc, r = accel(x, mp, a0, mond, kind, gext, solver, track)
    nstep = 0; t1 = time.time(); samples = []; t_avg_from = t_end - 1.0*GYR
    while t < t_end:
        vmag = np.linalg.norm(v, axis=1) + 1e3; amag = np.linalg.norm(acc, axis=1) + 1e-20
        dt = 0.03*min(float(np.min(np.sqrt((r + SOFT)/amag))), float(np.min((r + SOFT)/vmag)))
        dt = min(dt, 0.05*GYR, t_end - t); dt = max(dt, dtfloor*GYR)
        v += 0.5*dt*acc; x += dt*v; t += dt
        acc, Mdisc, r = accel(x, mp, a0, mond, kind, gext, solver, track); v += 0.5*dt*acc; nstep += 1
        if t >= t_avg_from and (nstep % 5 == 0):
            samples.append([mp*np.sum(r < R)/Mb0 for R in (10*kpc, 30*kpc, 100*kpc, 200*kpc)])
    S = np.array(samples) if samples else np.array([[mp*np.sum(r < R)/Mb0 for R in (10*kpc, 30*kpc, 100*kpc, 200*kpc)]])
    out = dict(M10=float(S[:, 0].mean()), M30=float(S[:, 1].mean()), M100=float(S[:, 2].mean()), M200=float(S[:, 3].mean()),
               Mdisc=Mdisc/Mb0, steps=nstep, secs=time.time() - t1, maxboost=track[0], N=N)
    if diag:                                                             # is the final state actually non-radial?
        ad, rr = multipole_acc(x, mp); nn = x/np.maximum(rr, 1e-12)[:, None]
        ar = np.einsum('ij,ij->i', ad, nn); at = np.linalg.norm(ad - ar[:, None]*nn, axis=1)
        sel = (rr < 100*kpc) & (rr > 2*kpc)
        out["at_over_ar"] = float(np.median(at[sel]/np.abs(ar[sel]))) if sel.sum() else float('nan')
        inn = x[rr < 30*kpc]
        if len(inn) > 20:
            w = np.linalg.eigvalsh(inn.T @ inn/len(inn)); w = np.sqrt(np.maximum(w, 0))
            out["axes"] = f"{w[1]/w[2]:.2f}/{w[0]/w[2]:.2f}"
    print(f"    {label:52s}: M/M_b(<10,30,100,200 kpc) = {out['M10']:6.2f}, {out['M30']:6.2f}, {out['M100']:6.1f}, "
          f"{out['M200']:6.1f}   (disc {out['Mdisc']:.2f} M_b0, N={N}, {nstep} steps, {out['secs']:.0f}s"
          + (f", max boost {out['maxboost']:.2f} a0" if mond != "off" else "") + ")", flush=True)
    return out

# ================================================================== V1/V2: the force solver =========
print("\n  --- validating the force solver ---", flush=True)
rng = np.random.default_rng(7); dev = {}; noise = {}
for N in (3000, 12000, 48000):
    u = rng.random(N); rr = 100*kpc*u**(1/3); d = rng.normal(size=(N, 3)); d /= np.linalg.norm(d, axis=1)[:, None]
    xs = rr[:, None]*d; mps = 1e9*MSUN
    am, _ = multipole_acc(xs, mps); a0m, _ = monopole_acc(xs, mps)
    R = np.linalg.norm(xs, axis=1); nn = xs/R[:, None]
    arm = np.einsum('ij,ij->i', am, nn); ar0 = np.einsum('ij,ij->i', a0m, nn)
    sel = (R > 5*kpc) & (np.abs(ar0) > 0)
    dev[N] = abs(float(np.mean(arm[sel])/np.mean(ar0[sel])) - 1); noise[N] = float(np.median(np.abs(arm[sel]/ar0[sel] - 1)))
print(f"    spherical config, SOFT = 0.5 kpc: binned-mean |a_r| deviation from the monopole = "
      + ", ".join(f"N={n}: {dev[n]:.5f}" for n in dev), flush=True)
print(f"    per-particle scatter (the expansion's own Poisson noise) = "
      + ", ".join(f"N={n}: {noise[n]*100:.1f}%" for n in noise) + f"; N^-1/2 would give ratios 2.00, 2.00; measured "
      f"{noise[3000]/noise[12000]:.2f}, {noise[12000]/noise[48000]:.2f}", flush=True)
check("V1 [solver] the multipole solver reproduces the monopole for a spherically symmetric configuration (binned-mean radial "
      "acceleration within 1%, at every N) and its per-particle residual falls as N^-1/2",
      max(dev.values()) < 0.01 and 1.6 < noise[3000]/noise[12000] < 2.5 and 1.6 < noise[12000]/noise[48000] < 2.5,
      f"max binned deviation {max(dev.values()):.5f}")
Nv = 20000; q = 0.5; Aax = 60*kpc
pts = np.zeros((0, 3))
while len(pts) < Nv:
    p = rng.uniform(-1, 1, size=(4*Nv, 3)); pts = np.concatenate([pts, p[p[:, 0]**2 + p[:, 1]**2 + (p[:, 2]/q)**2 < 1]])
xs = pts[:Nv]*Aax; Mtot = 1e12*MSUN; mps = Mtot/Nv; rho_b = Mtot/(4/3*math.pi*Aax*Aax*q*Aax)
ecc = math.sqrt(1 - q*q)
A1 = (math.sqrt(1 - ecc*ecc)/ecc**3)*math.asin(ecc) - (1 - ecc*ecc)/ecc**2
A3 = 2/ecc**2 - 2*math.sqrt(1 - ecc*ecc)*math.asin(ecc)/ecc**3
ex = -2*math.pi*G*rho_b*np.stack([A1*xs[:, 0], A1*xs[:, 1], A3*xs[:, 2]], axis=1)
sel = np.linalg.norm(xs, axis=1) < 0.6*Aax; nex = np.linalg.norm(ex, axis=1)
e_mp = float(np.median(np.linalg.norm(multipole_acc(xs, mps)[0] - ex, axis=1)[sel]/nex[sel]))
e_mo = float(np.median(np.linalg.norm(monopole_acc(xs, mps)[0] - ex, axis=1)[sel]/nex[sel]))
e_di = float(np.median(np.linalg.norm(direct_acc(xs, mps)[0] - ex, axis=1)[sel]/nex[sel]))
check("V2 [solver] the multipole solver reproduces a case the monopole CANNOT -- the analytic interior field of a homogeneous "
      "oblate spheroid (q = 0.5) -- to better than 10%, where the monopole is wrong by >30%",
      e_mp < 0.10 and e_mo > 0.30, f"median relative error: multipole {e_mp*100:.1f}%, monopole {e_mo*100:.1f}%, "
      f"direct O(N^2) at the same N {e_di*100:.1f}% (direct is noisier here because its error is particle noise, not truncation)")

# ================================================================== V3: the acceleration cap ========
print("\n  --- validating the repaired multiplier ---", flush=True)
a0c = A0["canonical"]; gx = np.array([0.0, 0.0, GEXT_FRAC*a0c])
off = np.concatenate([-np.geomspace(1e-8, 3.0, 400)[::-1], [0.0], np.geomspace(1e-8, 3.0, 400)])   # sweep through cancellation
perp = np.geomspace(1e-8, 1.0, 9)
gN = np.array([[p*GEXT_FRAC*a0c, 0.0, (-1.0 + o)*GEXT_FRAC*a0c] for o in off for p in perp])
ex_g04k = float(np.max(np.linalg.norm(mond_g04k(gN, gx, a0c) - gN, axis=1)))/a0c
ex_rep = float(np.max(np.linalg.norm(mond_repaired(gN, gx, a0c) - gN, axis=1)))/a0c
print(f"    sweep of gN_int through exact cancellation with g_ext = 0.02 a0 ({len(gN)} points, offsets 1e-8..3 of g_ext):", flush=True)
print(f"    max added acceleration |g - gN_int|/a0 :  g04k rule {ex_g04k:.3g}   repaired rule {ex_rep:.4f}   "
      f"(the intended cap is Delta_max = {DMAX}, the repaired bound is 2 Delta_max = {2*DMAX:.4f})", flush=True)
check("V3 [cap] the repaired multiplier's added acceleration stays below 1.30 a0 through exact internal/external cancellation, "
      "while the g04k rule exceeds 100 a0 on the same sweep", ex_rep <= 1.30 and ex_g04k > 100,
      f"repaired {ex_rep:.4f} a0, g04k {ex_g04k:.3g} a0")
xr = np.array([[30*kpc, 0.0, 0.0]]); gnr = -disc_acc(xr, Mb0, "disc")[0, 0]; sr = gnr/a0c
vflat = math.sqrt(gnr*(1 + float(Delta(sr))/sr)*30*kpc); vpred = (G*Mb0*a0c)**0.25
check("V3b [kernel] the repaired rule is IDENTICAL to g04k's with no external field, and the disc alone still gives the "
      "deep-MOND flat speed (G M_b a0)^1/4 at 30 kpc to 10%",
      float(np.max(np.abs(mond_repaired(np.array([[-gnr, 0, 0]]), np.zeros(3), a0c)
                          - mond_g04k(np.array([[-gnr, 0, 0]]), np.zeros(3), a0c)))) < 1e-20*a0c
      and abs(vflat/vpred - 1) < 0.10, f"{vflat/1e3:.0f} vs {vpred/1e3:.0f} km/s")

# ================================================================== the runs ========================
print(f"\n  --- monopole (g04k's own solver) at N = {NMULTI}, for the anchor and the cap-repair effect alone ---", flush=True)
R = {}
R["mono_g04k_20"] = run(20e3, solver="mono", mond="g04k", label="MONOPOLE + g04k cap, sigma_i=20, canonical")
R["mono_rep_20"] = run(20e3, solver="mono", mond="repaired", label="MONOPOLE + REPAIRED cap, sigma_i=20, canonical")
R["mono_rep_60"] = run(60e3, solver="mono", mond="repaired", label="MONOPOLE + REPAIRED cap, sigma_i=60, canonical")
R["mono_rep_20a"] = run(20e3, solver="mono", mond="repaired", a0=A0["alt"], label="MONOPOLE + REPAIRED cap, sigma_i=20, alt")
R["mono_newton"] = run(20e3, solver="mono", mond="off", label="MONOPOLE, NEWTON control, sigma_i=20")
check("V4 [anchor] monopole + g04k multiplier at this N reproduces g04k's published 60k result M(<10 kpc)/M_b = 2.58 within a "
      "factor 1.5", 2.58/1.5 < R["mono_g04k_20"]["M10"] < 2.58*1.5, f"{R['mono_g04k_20']['M10']:.2f} vs 2.58")

print(f"\n  --- MULTIPOLE l <= {LMAX} (caustics/non-radial structure resolved), N = {NMULTI} ---", flush=True)
R["mp_g04k_20"] = run(20e3, solver="multi", mond="g04k", label="MULTIPOLE + g04k cap, sigma_i=20, canonical", diag=True)
R["mp_rep_20"] = run(20e3, solver="multi", mond="repaired", label="MULTIPOLE + REPAIRED cap, sigma_i=20, canonical", diag=True)
R["mp_rep_60"] = run(60e3, solver="multi", mond="repaired", label="MULTIPOLE + REPAIRED cap, sigma_i=60, canonical", diag=True)
R["mp_rep_20a"] = run(20e3, solver="multi", mond="repaired", a0=A0["alt"], label="MULTIPOLE + REPAIRED cap, sigma_i=20, alt")
R["mp_rep_60a"] = run(60e3, solver="multi", mond="repaired", a0=A0["alt"], label="MULTIPOLE + REPAIRED cap, sigma_i=60, alt")
R["mp_newton"] = run(20e3, solver="multi", mond="off", label="MULTIPOLE, NEWTON control, sigma_i=20")
R["mp_rep_20_half"] = run(20e3, solver="multi", mond="repaired", N=NMULTI//2, label="MULTIPOLE + REPAIRED, half N (resolution)")

print(f"\n  --- direct O(N^2) cross-check (resolves EVERY scale, but the particle noise biases it: see below) ---", flush=True)
R["dir_rep_lo"] = run(20e3, solver="direct", mond="repaired", N=NDIRECT//2, label=f"DIRECT + REPAIRED cap, sigma_i=20, N={NDIRECT//2}")
R["dir_rep_hi"] = run(20e3, solver="direct", mond="repaired", N=NDIRECT, label=f"DIRECT + REPAIRED cap, sigma_i=20, N={NDIRECT}")

print(f"\n  --- timestep control (a coarse global step leaks mass OUT of the aperture, i.e. toward a PASS) ---", flush=True)
R["mono_rep_20_fine"] = run(20e3, solver="mono", mond="repaired", dtfloor=DTFLOOR/3, label="MONOPOLE + REPAIRED, step floor / 3")

# ================================================================== the verdict =====================
KEY = ("mp_rep_20", "mp_rep_60", "mp_rep_20a", "mp_rep_60a")
print("\n  --- the numbers ---", flush=True)
print(f"    {'run':52s}  M(<10)  M(<30)  M(<100)", flush=True)
for k in ("mono_g04k_20", "mono_rep_20", "mp_g04k_20") + KEY + ("mp_newton", "dir_rep_hi"):
    print(f"    {k:52s} {R[k]['M10']:7.2f} {R[k]['M30']:7.2f} {R[k]['M100']:8.1f}", flush=True)
print(f"\n    cap repair alone   (monopole, sigma=20, canonical): M(<10) {R['mono_g04k_20']['M10']:.2f} -> "
      f"{R['mono_rep_20']['M10']:.2f}   ({100*(R['mono_rep_20']['M10']/R['mono_g04k_20']['M10'] - 1):+.0f}%); "
      f"max added acceleration {R['mono_g04k_20']['maxboost']:.3g} a0 -> {R['mono_rep_20']['maxboost']:.2f} a0", flush=True)
print(f"    caustics alone     (g04k cap, sigma=20, canonical): M(<10) {R['mono_g04k_20']['M10']:.2f} -> "
      f"{R['mp_g04k_20']['M10']:.2f}   ({100*(R['mp_g04k_20']['M10']/R['mono_g04k_20']['M10'] - 1):+.0f}%)", flush=True)
print(f"    both repairs       (multipole + repaired cap)      : M(<10) {R['mono_g04k_20']['M10']:.2f} -> "
      f"{R['mp_rep_20']['M10']:.2f}   ({100*(R['mp_rep_20']['M10']/R['mono_g04k_20']['M10'] - 1):+.0f}%)", flush=True)
d = R["mp_rep_20"]
print(f"    the resolved state is genuinely non-radial: median |a_tangential|/|a_radial| (dust, 2-100 kpc) = "
      f"{d.get('at_over_ar', float('nan')):.3f}, inner-30 kpc axis ratios b/a, c/a = {d.get('axes', 'n/a')}", flush=True)
print(f"    resolution: M(<10) = {R['mp_rep_20']['M10']:.2f} at N={NMULTI} vs {R['mp_rep_20_half']['M10']:.2f} at N={NMULTI//2} "
      f"(multipole); direct O(N^2) gives {R['dir_rep_lo']['M10']:.2f} at N={NDIRECT//2} and {R['dir_rep_hi']['M10']:.2f} at "
      f"N={NDIRECT} -- if the direct numbers rise with N they are particle noise, not caustics", flush=True)
print(f"    timestep: M(<10) = {R['mono_rep_20']['M10']:.2f} at floor {DTFLOOR} Gyr vs {R['mono_rep_20_fine']['M10']:.2f} at "
      f"floor {DTFLOOR/3:.1e} Gyr (monopole); the coarse step biases the answer DOWN, i.e. toward a PASS", flush=True)

check("P3 [THE TEST] with caustics resolved (multipole l <= 6) AND the acceleration cap repaired, the dust inside 10 kpc is "
      "below 25% of the baryons -- sigma_i = 20 and 60 km/s, both a0 footings",
      all(R[k]["M10"] < 0.25 for k in KEY), json.dumps({k: round(R[k]["M10"], 2) for k in KEY}))
check("P4 [BTFR] the same inside 30 kpc", all(R[k]["M30"] < 0.25 for k in KEY),
      json.dumps({k: round(R[k]["M30"], 2) for k in KEY}))
check("P5 [KiDS] the repaired MOND runs hold less than 14% of the Newtonian control's mass inside 100 kpc",
      all(R[k]["M100"] < 0.14*R["mp_newton"]["M100"] for k in ("mp_rep_20", "mp_rep_60")),
      f"MOND/Newton inside 100 kpc = {R['mp_rep_20']['M100']/R['mp_newton']['M100']:.2f}, "
      f"{R['mp_rep_60']['M100']/R['mp_newton']['M100']:.2f}")
print(f"\n  caveats carried over from g04k and NOT repaired here: algebraic QUMOND rather than a solved field equation; an "
      f"isolated vacuole of 8 cosmic shares with no tides beyond it; z_i = 20 against the shell model's 50; the baryonic disc is "
      f"an analytic Miyamoto-Nagai, not live.  New to this script: the expansion truncates at l = {LMAX}, so structure below "
      f"~180/(l+1) deg in angle is still smoothed -- the direct O(N^2) runs are the (noise-limited) check on that.  "
      f"total {time.time()-T0:.0f}s")
print(f"\nRESULT: {len(FAILS)} FAIL" + (f" -> {FAILS}" if FAILS else ""))
sys.exit(0)
