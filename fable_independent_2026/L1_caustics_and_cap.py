#!/usr/bin/env python3
"""
L1 -- the load-bearing number re-run with caustics resolved and the acceleration cap repaired
=============================================================================================
Every dark-sector verdict of 2026-09-06/07 rests on one number: cold collisionless dust falling onto a MOND-boosted 5e10 Msun
disc delivers M/M_b ~ 2.6-3.3 inside 10 kpc, ~10x the ~0.25 M_b the RAR tolerates.  It was computed twice (g03r spherical
shells, g04k 60k 3D particles).  Both share TWO gaps, and both are gaps in MY OWN no-go, so both are tested here as hard as a
win would be tested.

  (a) CAUSTICS.  g04k's dust self-gravity is a MONOPOLE from sorted radii (`dust_monopole`).  A monopole is exact only for a
      sphere; it smooths over shell-crossing, caustic sheets and aspherical collapse -- exactly the structure cold
      collisionless infall develops.  "Caustic-quenched dust" is on the programme's own list of untested survivors.
  (b) THE CAP.  g04k's MOND step is  g = gN_int * (1 + Delta(s)/max(s,1e-30)),  s = |gN_int + g_ext|/a0.  The intended physics
      is that the boost adds at most Delta_max = 0.6476 a0 of acceleration.  Multiplying the INTERNAL field by a multiplier
      evaluated on the TOTAL field loses that cap: the added acceleration is a0 Delta(s)|gN_int|/|gN_tot|, unbounded where the
      internal and external fields cancel -- a real surface at |gN_int| = g_ext = 0.02 a0, tens of kpc up the external-field
      axis, inside the apertures being measured.  This is the lead reviewer's criticism in
      review_reconciliation_2026/PATH_FORWARD.md: "loss of the intended physical acceleration cap and strong cancellation
      sensitivity".  The stronger "literal divergence" claim was withdrawn there and is NOT repeated here.

WHAT THE REPAIR RUN FOUND FIRST (this reshaped the script; it is reported, not hidden).  Swapping in a non-radial force solver
exposes a THIRD defect that neither gap named: the algebraic multiplier itself.  g = nu(|gN|) gN multiplies a vector field by a
scalar function of its own magnitude; curl g = grad(nu) x gN is nonzero as soon as gN stops being radial, so the force does net
work around closed loops.  QUMOND's actual field equation, div[nu grad Phi_N] = div grad Phi, is the CURL-FREE PROJECTION of
that product and has no such term.  With a monopole solver gN is radial and the defect is invisible -- which is why g04k never
saw it.  With the dust's l >= 1 field switched on, the algebraic rule pumps energy and unbinds the whole system inside 1 Gyr
(V5b), at any timestep.  So the number cannot be re-derived by swapping the force solver alone; the MOND step has to be made
conservative too.

THE THREE REPAIRS ACTUALLY RUN
  (a) Force: a softened SPHERICAL-HARMONIC solver to l <= LMAX = 6 on the sorted particles, self excluded,
      Phi = -G sum_lm 4pi/(2l+1) Y_lm(Omega)[rho^-(l+1) S_in,lm + rho^l S_out,lm],  rho = sqrt(r^2+SOFT^2), SOFT = 0.5 kpc
      (g04k's softening).  With that rho the l = 0 term is EXACTLY g04k's monopole, so the two calculations are nested and the
      difference is entirely the l >= 1 force.  Radial derivative analytic; tangential by a central difference in two
      orthogonal tangent directions at fixed rho.  l >= 1 terms carry an angular smoothing matched to SOFT.  A direct O(N^2)
      sum is also implemented and run as an independent cross-check.
  (b) Cap: the bounded QUMOND external-field form g = [gN_tot + a0 Delta(s_tot) ghat_tot] - [g_ext + a0 Delta(s_ext) ghat_ext],
      identical to g04k's with no external field, bounded by 2 Delta_max a0 = 1.295 a0 everywhere including exact cancellation.
  (c) Conservativity: the MOND phantom is added as a radial function of r alone -- a0 B(gbar_N(r)/a0), where B is the ANGLE
      AVERAGE of the radial projection of the chosen algebraic rule applied to the enclosed-mass field.  A radial field is
      curl-free by construction, so the run conserves energy, while the FULL non-radial Newtonian force is kept.  Two versions:
      `cons` (built from the repaired bounded rule) and `consg` (built from g04k's uncapped rule) -- their difference is the
      cap repair, measured inside a scheme that can actually be integrated.

CHECKS THAT CAN FAIL
  V1  the multipole solver reproduces the monopole for a spherically symmetric configuration (binned mean to 1%), residual = its
      own Poisson noise, falling as N^-1/2;
  V2  it reproduces a case the monopole CANNOT: the analytic interior field of a homogeneous oblate spheroid (q = 0.5);
  V3  the repaired multiplier stays below 1.30 a0 through exact internal/external cancellation, where g04k's exceeds 100 a0;
  V3b the repaired rule is identical to g04k's with no external field, and still gives the deep-MOND flat speed;
  V4  monopole + g04k multiplier reproduces g04k's published M(<10 kpc)/M_b = 2.58;
  V5a the algebraic rule has nonzero circulation on a non-radial field, the conservative scheme has none;
  V5b and that is dynamical, not numerical: the algebraic rule + multipole solver unbinds the system at BOTH step floors;
  V6  the conservative surrogate is faithful: monopole + consg reproduces monopole + g04k within 30%, so the answer is not an
      artefact of making the scheme conservative;
  P3 [THE TEST]  with caustics resolved AND the cap repaired, M(<10 kpc) < 0.25 M_b, both dispersions, both a0 footings.
      A PASS REOPENS the dark-sector door for plain cold dust.  Nothing here is tuned to reach it or to avoid it.
  P4  the same inside 30 kpc;  P5  the KiDS aperture at 100 kpc against the Newtonian control.

HONESTY CONTROLS, all reported next to the answer with the direction they push
  * particle noise in gN feeds a steeply falling nu, so a grainy field is boosted LESS than the smooth field it samples ->
    toward a PASS.  Measured by the multipole N-doubling and by the direct O(N^2) N-doubling.
  * a coarse global timestep leaks mass out of the aperture -> toward a PASS.  Measured by re-running at a 3x finer floor.
  * the conservative scheme's phantom is spherical, so it does not feel caustics suppressing nu locally -> toward a FAIL.
    Bounded by comparing against the (uncontrolled) algebraic runs that do.
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
LMAX = 6; NMULTI = 8_000; NDIRECT = 3_000; DTFLOOR = 3e-3          # Gyr
print("=" * 124)
print("L1 -- cold collisionless infall onto a MOND-boosted disc, with CAUSTICS RESOLVED (l <= 6) and the ACCELERATION CAP REPAIRED")
print("=" * 124, flush=True)

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
CFAC = 4*math.pi/(2*LVEC + 1); SOFTK = SOFT/kpc; LL = (LVEC*(LVEC + 1.0))[:, None]
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
    """Softened self-gravity of N equal-mass particles to l <= LMAX.  The l = 0 term equals monopole_acc exactly.

    The l >= 1 terms carry an angular smoothing matched to the radial softening: source and field point are each weighted by
    w_l(rho) = exp(-l(l+1) SOFT^2/(4 rho^2)), so the pair weight is exp(-l(l+1) theta_s^2/2) with theta_s = SOFT/rho -- angular
    structure finer than the softening length is smoothed exactly as the radial softening smooths radial structure.  w_0 = 1,
    so the monopole is untouched, and w_6 = 0.994-0.9995 at 30-100 kpc, so nothing in the measured apertures is affected."""
    r = np.linalg.norm(x, axis=1); rho = np.sqrt(r*r + SOFT*SOFT)/kpc
    n = x/np.maximum(r, 1e-12)[:, None]
    o = np.argsort(rho); rs = rho[o]; ns = n[o]; Ys = real_sph(ns)
    rl = rs[None, :]**LVEC[:, None]; rml = 1.0/(rs[None, :]**(LVEC[:, None] + 1.0))
    w = np.exp(-LL*SOFTK**2/(4.0*rs[None, :]**2)); dwdr = w*LL*SOFTK**2/(2.0*rs[None, :]**3)
    Win = Ys*rl*w; Wout = Ys*rml*w
    Sin = np.cumsum(Win, axis=1) - Win                                   # strictly interior
    Sout = np.cumsum(Wout[:, ::-1], axis=1)[:, ::-1] - Wout              # strictly exterior
    dPhi = -(G*mp/kpc**2)*np.einsum('kn,kn->n', Ys*CFAC[:, None],
                                    w*(-(LVEC[:, None] + 1.0)*rml*Sin + LVEC[:, None]*rl*Sout)/rs[None, :]
                                    + dwdr*(rml*Sin + rl*Sout))
    Ck = CFAC[:, None]*w*(rml*Sin + rl*Sout)
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

# ---------------------------------------------------------------- the MOND step --------------------
def mond_g04k(gN, gext, a0):
    """g04k as written: the INTERNAL field times a multiplier evaluated on the TOTAL field.  Uncapped near cancellation."""
    s = np.linalg.norm(gN + gext[None, :], axis=1)/a0
    return gN*(1 + Delta(s)/np.maximum(s, 1e-30))[:, None]
def mond_repaired(gN, gext, a0):
    """Bounded QUMOND external-field form: boost the total, then subtract the boosted external field."""
    gt = gN + gext[None, :]; nt = np.linalg.norm(gt, axis=1)
    ht = np.where(nt[:, None] > 0, gt/np.maximum(nt, 1e-300)[:, None], 0.0)
    ne = np.linalg.norm(gext); he = gext/ne if ne > 0 else gext*0.0
    return gN + a0*(Delta(nt/a0)[:, None]*ht - Delta(ne/a0)*he[None, :])
MOND = {"g04k": mond_g04k, "repaired": mond_repaired}
BCACHE = {}
def boost_table(a0, gext, rule):
    """B(u) = angle average over sphere directions of the INWARD radial projection of the algebraic boost applied to a radial
    Newtonian field of magnitude u a0.  Used to add the MOND phantom as a curl-free (radial) field."""
    key = (a0, float(gext[2]), rule)
    if key not in BCACHE:
        U = np.geomspace(1e-8, 1e6, 900); mu = np.linspace(-1, 1, 241)
        rh = np.stack([np.sqrt(np.maximum(1 - mu*mu, 0)), np.zeros_like(mu), mu], axis=1)
        B = np.empty_like(U)
        for i, u in enumerate(U):
            gb = -u*a0*rh
            B[i] = -np.trapz(np.einsum('ij,ij->i', MOND[rule](gb, gext, a0) - gb, rh), mu)/(2.0*a0)
        BCACHE[key] = (np.log(U), B)
    return BCACHE[key]
def accel(x, mp, a0, mond, kind, gext, solver, track):
    acc_d, r = SOLVER[solver](x, mp)
    Mdisc = min(Mb0, (Ob/Od)*mp*np.searchsorted(np.sort(r), 50*kpc))
    gN = acc_d + disc_acc(x, Mdisc, kind)
    if mond in ("cons", "consg"):
        o = np.argsort(r); Menc = np.empty(len(r)); Menc[o] = mp*np.arange(0, len(r))
        rs2 = r*r + SOFT*SOFT
        Menc = Menc + Mdisc*r**3/(r*r + A_MN*A_MN)**1.5                  # + the disc's own monopole
        lu, B = boost_table(a0, gext, "repaired" if mond == "cons" else "g04k")
        aph = a0*np.interp(np.log(np.maximum(G*Menc/rs2/a0, 1e-8)), lu, B)
        gN = gN - (aph/np.sqrt(rs2))[:, None]*x
        track[0] = max(track[0], float(np.max(aph))/a0)
    elif mond != "off":
        g = MOND[mond](gN, gext, a0)
        track[0] = max(track[0], float(np.max(np.linalg.norm(g - gN, axis=1)))/a0)
        gN = g
    gN += (OL*H0**2)*x
    return gN, Mdisc, r

# ---------------------------------------------------------------- the integrator (g04k's) ----------
def run(sigma_i, solver="multi", mond="cons", kind="disc", a0=A0["canonical"], seed=1, N=NMULTI,
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
    ctr = np.zeros(3); Rc = 300*kpc                                       # shrinking-sphere centre, to expose any bulk drift
    for _ in range(12):
        s = np.linalg.norm(x - ctr, axis=1) < Rc
        if s.sum() < 20: break
        ctr = x[s].mean(axis=0); Rc *= 0.8
    out = dict(M10=float(S[:, 0].mean()), M30=float(S[:, 1].mean()), M100=float(S[:, 2].mean()), M200=float(S[:, 3].mean()),
               Mdisc=Mdisc/Mb0, steps=nstep, secs=time.time() - t1, maxboost=track[0], N=N,
               drift=float(np.linalg.norm(ctr))/kpc)
    if diag:                                                              # is the final state actually non-radial?
        ad, rr = multipole_acc(x, mp); nn = x/np.maximum(rr, 1e-12)[:, None]
        ar = np.einsum('ij,ij->i', ad, nn); at = np.linalg.norm(ad - ar[:, None]*nn, axis=1)
        sel = (rr < 100*kpc) & (rr > 2*kpc) & (np.abs(ar) > 0)
        out["at_over_ar"] = float(np.median(at[sel]/np.abs(ar[sel]))) if sel.sum() else float('nan')
        inn = x[rr < 30*kpc]
        if len(inn) > 20:
            wq = np.sqrt(np.maximum(np.linalg.eigvalsh(inn.T @ inn/len(inn)), 0))
            out["axes"] = f"{wq[1]/wq[2]:.2f}/{wq[0]/wq[2]:.2f}"
    print(f"    {label:54s}: M/M_b(<10,30,100,200 kpc) = {out['M10']:6.2f}, {out['M30']:6.2f}, {out['M100']:6.1f}, "
          f"{out['M200']:6.1f}   (disc {out['Mdisc']:.2f} M_b0, N={N}, {nstep} steps, drift {out['drift']:.1f} kpc, "
          f"{out['secs']:.0f}s)", flush=True)
    return out

# ================================================================== V1/V2: the force solver =========
print("\n  --- validating the force solver ---", flush=True)
rng = np.random.default_rng(7); dev = {}; noise = {}; VN = (3000, 12000, 48000)
for N in VN:
    u = rng.random(N); rr = 100*kpc*u**(1/3); d = rng.normal(size=(N, 3)); d /= np.linalg.norm(d, axis=1)[:, None]
    xs = rr[:, None]*d; mps = 1e9*MSUN
    am, _ = multipole_acc(xs, mps); a0m, _ = monopole_acc(xs, mps)
    Rr = np.linalg.norm(xs, axis=1); nn = xs/Rr[:, None]
    arm = np.einsum('ij,ij->i', am, nn); ar0 = np.einsum('ij,ij->i', a0m, nn)
    sel = (Rr > 5*kpc) & (np.abs(ar0) > 0)
    dev[N] = abs(float(np.mean(arm[sel])/np.mean(ar0[sel])) - 1); noise[N] = float(np.median(np.abs(arm[sel]/ar0[sel] - 1)))
print(f"    spherical config, SOFT = 0.5 kpc: binned-mean |a_r| deviation from the monopole = "
      + ", ".join(f"N={n}: {dev[n]:.5f}" for n in dev), flush=True)
print(f"    per-particle scatter (the expansion's own Poisson noise) = "
      + ", ".join(f"N={n}: {noise[n]*100:.1f}%" for n in noise) + f"; N^-1/2 would give ratios 2.00, 2.00; measured "
      f"{noise[VN[0]]/noise[VN[1]]:.2f}, {noise[VN[1]]/noise[VN[2]]:.2f}", flush=True)
check("V1 [solver] the multipole solver reproduces the monopole for a spherically symmetric configuration (binned-mean radial "
      "acceleration within 1%, at every N) and its per-particle residual falls as N^-1/2",
      max(dev.values()) < 0.01 and 1.6 < noise[VN[0]]/noise[VN[1]] < 2.5 and 1.6 < noise[VN[1]]/noise[VN[2]] < 2.5,
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
nd = min(Nv, 6000)                                                        # direct is O(N^2) in memory; subsample the same spheroid
e_di = float(np.median(np.linalg.norm(direct_acc(xs[:nd], Mtot/nd)[0] - ex[:nd], axis=1)[sel[:nd]]/nex[:nd][sel[:nd]]))
check("V2 [solver] the multipole solver reproduces a case the monopole CANNOT -- the analytic interior field of a homogeneous "
      "oblate spheroid (q = 0.5) -- to better than 10%, where the monopole is wrong by >30%",
      e_mp < 0.10 and e_mo > 0.30, f"median relative error: multipole {e_mp*100:.1f}%, monopole {e_mo*100:.1f}%, "
      f"direct O(N^2) at the same N {e_di*100:.1f}% (direct is noisier here: its error is particle noise, not truncation)")

# ================================================================== V3: the acceleration cap ========
print("\n  --- validating the repaired multiplier ---", flush=True)
a0c = A0["canonical"]; gx = np.array([0.0, 0.0, GEXT_FRAC*a0c])
off = np.concatenate([-np.geomspace(1e-8, 3.0, 400)[::-1], [0.0], np.geomspace(1e-8, 3.0, 400)])
perp = np.geomspace(1e-8, 1.0, 9)
gN = np.array([[p*GEXT_FRAC*a0c, 0.0, (-1.0 + o)*GEXT_FRAC*a0c] for o in off for p in perp])
ex_g04k = float(np.max(np.linalg.norm(mond_g04k(gN, gx, a0c) - gN, axis=1)))/a0c
ex_rep = float(np.max(np.linalg.norm(mond_repaired(gN, gx, a0c) - gN, axis=1)))/a0c
print(f"    sweep of gN_int through exact cancellation with g_ext = 0.02 a0 ({len(gN)} points, offsets 1e-8..3 of g_ext):"
      f"\n    max added acceleration |g - gN_int|/a0 :  g04k rule {ex_g04k:.3g}   repaired rule {ex_rep:.4f}   "
      f"(intended cap Delta_max = {DMAX}; the repaired bound is 2 Delta_max = {2*DMAX:.4f})", flush=True)
check("V3 [cap] the repaired multiplier's added acceleration stays below 1.30 a0 through exact internal/external cancellation, "
      "while the g04k rule exceeds 100 a0 on the same sweep", ex_rep <= 1.30 and ex_g04k > 100,
      f"repaired {ex_rep:.4f} a0, g04k {ex_g04k:.3g} a0")
xr = np.array([[30*kpc, 0.0, 0.0]]); gnr = -disc_acc(xr, Mb0, "disc")[0, 0]; sr = gnr/a0c
vflat = math.sqrt(gnr*(1 + float(Delta(sr))/sr)*30*kpc); vpred = (G*Mb0*a0c)**0.25
check("V3b [kernel] the repaired rule is IDENTICAL to g04k's with no external field, and the disc alone still gives the "
      "deep-MOND flat speed (G M_b a0)^1/4 at 30 kpc to 10%",
      float(np.max(np.abs(mond_repaired(np.array([[-gnr, 0.0, 0.0]]), np.zeros(3), a0c)
                          - mond_g04k(np.array([[-gnr, 0.0, 0.0]]), np.zeros(3), a0c))))/gnr < 1e-12
      and abs(vflat/vpred - 1) < 0.10, f"{vflat/1e3:.0f} vs {vpred/1e3:.0f} km/s")

# ================================================================== V5a: circulation ================
print("\n  --- is the algebraic MOND step usable once the field stops being radial? ---", flush=True)
def loop_circulation(F, n=4000):
    """closed rectangle in the (R,z) plane, R = 15..25 kpc, z = 3..12 kpc; returns |circulation| / integral|F||dl|."""
    R1, R2, Z1, Z2 = 15*kpc, 25*kpc, 3*kpc, 12*kpc
    segs = [((R1, Z1), (R2, Z1)), ((R2, Z1), (R2, Z2)), ((R2, Z2), (R1, Z2)), ((R1, Z2), (R1, Z1))]
    circ = 0.0; norm = 0.0
    for (p, qq) in segs:
        s = (np.arange(n) + 0.5)/n
        X = p[0] + (qq[0] - p[0])*s; Z = p[1] + (qq[1] - p[1])*s
        pts = np.stack([X, np.zeros_like(X), Z], axis=1)
        dl = np.array([qq[0] - p[0], 0.0, qq[1] - p[1]])/n
        f = F(pts); circ += float(np.sum(f @ dl)); norm += float(np.sum(np.linalg.norm(f, axis=1)))*np.linalg.norm(dl)
    return abs(circ)/norm
gN_of = lambda pts: disc_acc(pts, Mb0, "disc")                            # a genuinely non-radial Newtonian field
c_newt = loop_circulation(gN_of)
c_alg = loop_circulation(lambda pts: mond_g04k(gN_of(pts), gx, a0c))
c_rep = loop_circulation(lambda pts: mond_repaired(gN_of(pts), gx, a0c))
lu_c, B_c = boost_table(a0c, gx, "repaired")
def cons_of(pts):
    rr = np.linalg.norm(pts, axis=1); rs2 = rr*rr + SOFT*SOFT
    Me = Mb0*rr**3/(rr*rr + A_MN*A_MN)**1.5
    aph = a0c*np.interp(np.log(np.maximum(G*Me/rs2/a0c, 1e-8)), lu_c, B_c)
    return gN_of(pts) - (aph/np.sqrt(rs2))[:, None]*pts
c_cons = loop_circulation(cons_of)
print(f"    |circulation|/int|F||dl| around a 10 x 9 kpc loop in the disc's own (non-radial) Newtonian field:"
      f"\n    Newtonian {c_newt:.2e}   g04k algebraic {c_alg:.2e}   repaired algebraic {c_rep:.2e}   conservative scheme "
      f"{c_cons:.2e}", flush=True)
check("V5a [conservativity] the algebraic MOND multiplier does net work around a closed loop once the Newtonian field is "
      "non-radial (>1e-3 of the path integral), while the Newtonian field and the conservative scheme do not (<1e-6)",
      c_newt < 1e-6 and c_cons < 1e-6 and c_alg > 1e-3 and c_rep > 1e-3,
      f"Newton {c_newt:.1e}, conservative {c_cons:.1e}, g04k {c_alg:.1e}, repaired {c_rep:.1e}")

# ================================================================== the runs ========================
print(f"\n  --- V5b: the same defect, dynamically (multipole solver + the algebraic rule, two step floors) ---", flush=True)
R = {}
R["mp_alg_a"] = run(20e3, solver="multi", mond="repaired", label="MULTIPOLE + algebraic repaired cap, floor 3e-3 Gyr")
R["mp_alg_b"] = run(20e3, solver="multi", mond="repaired", dtfloor=DTFLOOR/10, label="MULTIPOLE + algebraic, floor 3e-4 Gyr")
check("V5b [conservativity] with the non-radial solver the algebraic rule unbinds the system (nothing left inside 200 kpc), and "
      "it is not a timestep artefact -- a 10x finer step floor gives the same",
      R["mp_alg_a"]["M200"] < 0.1 and R["mp_alg_b"]["M200"] < 0.1,
      f"M(<200 kpc)/M_b = {R['mp_alg_a']['M200']:.2f} and {R['mp_alg_b']['M200']:.2f}; the monopole runs below keep 30-40")

print(f"\n  --- monopole (g04k's own solver): the anchor, and the cap repair inside a conservative scheme ---", flush=True)
R["mono_g04k"] = run(20e3, solver="mono", mond="g04k", label="MONOPOLE + g04k algebraic cap (the anchor)")
R["mono_consg"] = run(20e3, solver="mono", mond="consg", label="MONOPOLE + conservative, g04k cap")
R["mono_cons"] = run(20e3, solver="mono", mond="cons", label="MONOPOLE + conservative, REPAIRED cap")
R["mono_cons60"] = run(60e3, solver="mono", mond="cons", label="MONOPOLE + conservative, REPAIRED cap, sigma_i=60")
R["mono_newton"] = run(20e3, solver="mono", mond="off", label="MONOPOLE, NEWTON control")
check("V4 [anchor] monopole + g04k multiplier at this N reproduces g04k's published 60k result M(<10 kpc)/M_b = 2.58 within a "
      "factor 1.5", 2.58/1.5 < R["mono_g04k"]["M10"] < 2.58*1.5, f"{R['mono_g04k']['M10']:.2f} vs 2.58")
check("V6 [surrogate] making the scheme conservative does not by itself move the answer: monopole + conservative(g04k cap) "
      "reproduces monopole + g04k algebraic within 30%",
      abs(R["mono_consg"]["M10"]/R["mono_g04k"]["M10"] - 1) < 0.30,
      f"{R['mono_consg']['M10']:.2f} vs {R['mono_g04k']['M10']:.2f}")

print(f"\n  --- MULTIPOLE l <= {LMAX}: caustics resolved, cap repaired, conservative.  THE TEST. ---", flush=True)
R["mp_cons20"] = run(20e3, solver="multi", mond="cons", label="MULTIPOLE + conservative REPAIRED, sigma=20, canonical", diag=True)
R["mp_cons60"] = run(60e3, solver="multi", mond="cons", label="MULTIPOLE + conservative REPAIRED, sigma=60, canonical", diag=True)
R["mp_cons20a"] = run(20e3, solver="multi", mond="cons", a0=A0["alt"], label="MULTIPOLE + conservative REPAIRED, sigma=20, alt")
R["mp_cons60a"] = run(60e3, solver="multi", mond="cons", a0=A0["alt"], label="MULTIPOLE + conservative REPAIRED, sigma=60, alt")
R["mp_consg20"] = run(20e3, solver="multi", mond="consg", label="MULTIPOLE + conservative, g04k cap (cap effect)")
R["mp_newton"] = run(20e3, solver="multi", mond="off", label="MULTIPOLE, NEWTON control")
R["mp_half"] = run(20e3, solver="multi", mond="cons", N=NMULTI//2, label="MULTIPOLE + conservative REPAIRED, half N")

print(f"\n  --- direct O(N^2) cross-check: every scale resolved, but the particle noise biases it toward a PASS ---", flush=True)
R["dir_lo"] = run(20e3, solver="direct", mond="cons", N=NDIRECT//2, label=f"DIRECT + conservative REPAIRED, N={NDIRECT//2}")
R["dir_hi"] = run(20e3, solver="direct", mond="cons", N=NDIRECT, label=f"DIRECT + conservative REPAIRED, N={NDIRECT}")

print(f"\n  --- timestep control (a coarse global step leaks mass OUT of the aperture, i.e. toward a PASS) ---", flush=True)
R["mono_fine"] = run(20e3, solver="mono", mond="cons", dtfloor=DTFLOOR/3, label="MONOPOLE + conservative REPAIRED, floor / 3")

# ================================================================== the verdict =====================
KEY = ("mp_cons20", "mp_cons60", "mp_cons20a", "mp_cons60a")
print("\n  --- the numbers ---", flush=True)
print(f"    {'run':54s}  M(<10)  M(<30)  M(<100)", flush=True)
for k in ("mono_g04k", "mono_consg", "mono_cons", "mono_cons60", "mp_consg20") + KEY + ("mp_newton", "dir_hi"):
    print(f"    {k:54s} {R[k]['M10']:7.2f} {R[k]['M30']:7.2f} {R[k]['M100']:8.1f}", flush=True)
print(f"\n    cap repair alone (monopole, conservative): M(<10) {R['mono_consg']['M10']:.2f} -> {R['mono_cons']['M10']:.2f}  "
      f"({100*(R['mono_cons']['M10']/max(R['mono_consg']['M10'], 1e-9) - 1):+.0f}%)", flush=True)
print(f"    caustics alone (g04k cap, conservative)  : M(<10) {R['mono_consg']['M10']:.2f} -> {R['mp_consg20']['M10']:.2f}  "
      f"({100*(R['mp_consg20']['M10']/max(R['mono_consg']['M10'], 1e-9) - 1):+.0f}%)", flush=True)
print(f"    both repairs                             : M(<10) {R['mono_g04k']['M10']:.2f} (g04k) -> "
      f"{R['mp_cons20']['M10']:.2f}   ({100*(R['mp_cons20']['M10']/max(R['mono_g04k']['M10'], 1e-9) - 1):+.0f}%)", flush=True)
d = R["mp_cons20"]
print(f"    the resolved state IS non-radial: median |a_tangential|/|a_radial| (dust, 2-100 kpc) = "
      f"{d.get('at_over_ar', float('nan')):.3f}; inner-30 kpc axis ratios b/a, c/a = {d.get('axes', 'n/a')}", flush=True)
print(f"    resolution: M(<10) = {R['mp_cons20']['M10']:.2f} at N={NMULTI} vs {R['mp_half']['M10']:.2f} at N={NMULTI//2} "
      f"(multipole); direct O(N^2) {R['dir_lo']['M10']:.2f} at N={NDIRECT//2} -> {R['dir_hi']['M10']:.2f} at N={NDIRECT}. "
      f"Numbers RISING with N are particle noise, not caustics.", flush=True)
print(f"    timestep: M(<10) = {R['mono_cons']['M10']:.2f} at floor {DTFLOOR} Gyr vs {R['mono_fine']['M10']:.2f} at floor "
      f"{DTFLOOR/3:.1e} Gyr (monopole); the coarse step biases DOWN, i.e. toward a PASS.", flush=True)

check("P3 [THE TEST] with caustics resolved (multipole l <= 6), the acceleration cap repaired and the MOND step made "
      "conservative, the dust inside 10 kpc is below 25% of the baryons -- sigma_i = 20 and 60 km/s, both a0 footings",
      all(R[k]["M10"] < 0.25 for k in KEY), json.dumps({k: round(R[k]["M10"], 2) for k in KEY}))
check("P4 [BTFR] the same inside 30 kpc", all(R[k]["M30"] < 0.25 for k in KEY),
      json.dumps({k: round(R[k]["M30"], 2) for k in KEY}))
check("P5 [KiDS] the repaired MOND runs hold less than 14% of the Newtonian control's mass inside 100 kpc",
      all(R[k]["M100"] < 0.14*R["mp_newton"]["M100"] for k in ("mp_cons20", "mp_cons60")),
      f"MOND/Newton inside 100 kpc = {R['mp_cons20']['M100']/max(R['mp_newton']['M100'], 1e-9):.2f}, "
      f"{R['mp_cons60']['M100']/max(R['mp_newton']['M100'], 1e-9):.2f}")
print(f"\n  caveats carried over from g04k and NOT repaired here: algebraic/angle-averaged QUMOND rather than a solved field "
      f"equation; an isolated vacuole of 8 cosmic shares with no tides beyond it; z_i = 20 against the shell model's 50; the "
      f"baryonic disc is an analytic Miyamoto-Nagai pinned at the origin, not live.  New to this script: the expansion "
      f"truncates at l = {LMAX}, so angular structure below ~{180//(LMAX+1)} deg is still smoothed (the direct O(N^2) runs are "
      f"the noise-limited check on that), and the conservative phantom is spherical, so caustics do not locally suppress nu -- "
      f"that omission pushes toward MORE infall, i.e. toward a FAIL, and is the main thing a real QUMOND field solve would "
      f"change.  total {time.time()-T0:.0f}s")
print(f"\nRESULT: {len(FAILS)} FAIL" + (f" -> {FAILS}" if FAILS else ""))
sys.exit(0)
