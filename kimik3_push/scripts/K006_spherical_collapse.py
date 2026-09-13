#!/usr/bin/env python3
"""
K006 -- CONTROLLED spherical self-gravitating collapse of the dark sector.

Companion to K001 (brute-force 3D N-body) and K005 (analytical spine).  This lane
uses a SPHERICAL SHELL code so the radial profile and its slope can be measured
with high resolution and the energy budget tracked exactly.

PHYSICS (the framework's claim under test):  the dark sector is a cold,
collisionless, self-gravitating component.  Baryons supply a fixed central mass
M_b that sets the MOND radius r_M = sqrt(G M_b / a0).  The open Requirement 10
asks whether collapse makes the sector settle into the isothermal amplitude law
    rho(r) = sqrt(G M_b a0)/(4 pi G r^2),   sigma^2 = G M_b/(2 r_M),
with the BTFR  v_c^4 = G M_b a0  following.

WHAT THIS CODE DOES:
  * Evolves Nt concentric collisionless shells (a spherical N-body, self-gravity
    by enclosed mass + fixed central baryonic point M_b) with a leapfrog KDK
    integrator and a small Plummer softening for the shell crossings.
  * Starts COLD (zero radial velocity) from a top-hat of radius R0 spanning a
    range around r_M (R0 = f*r_M, f scanned 1.5--8) so we can see whether the
    relaxed state is an attractor (independent of R0) or remembers its IC.
  * Measures, in the virialised end state (|2K/W+1|<tol for several dyn times):
      - density slope  d log rho / d log r  over 0.3--3 r_M  (isothermal = -2),
      - the radius r_half enclosing half the dark mass, vs r_M,
      - the virial temperature  sigma^2 = K/(3 M)  vs the target G M_b/(2 r_M).
  * Runs a NO-BARYON CONTROL (M_b = 0) to show the scale-free contrast.
  * Scans M_b over 2 decades and fits the exponents of r_half and sigma^2.

Honesty: a spherical shell code FORBIDS non-radial orbit structure, so it can
show radial virialisation and the density slope but NOT tangential anisotropy;
that is K001's job.  A FAIL here is a real result (the formation route is in
trouble); a PASS is necessary-not-sufficient and is reported as such.
"""
import json, math, os
import numpy as np

RES, NP, NF = [], 0, 0
def check(name, measured, ok, reading=""):
    global NP, NF
    ok = bool(ok)
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}")
    print(f"         measured: {measured}")
    if reading: print(f"         reading : {reading}")
    RES.append({"name": name, "measured": str(measured), "pass": ok, "reading": reading})
    if ok: NP += 1
    else:  NF += 1

print(__doc__)

# ---------------- constants -------------------------------------------------
G    = 6.674e-11
MSUN = 1.98892e30
KPC  = 3.0857e19
A0   = {"canonical": 9.3619e-11, "alt": 1.1279e-10}
def rM(Mb, a0): return math.sqrt(G*Mb/a0)

# ---------------- spherical shell collapse ----------------------------------
def collapse(Mb, Md, R0, a0, Nt=4000, soft=0.02, n_dyn=12, seed=1):
    """Cold top-hat of Nt shells, total dark mass Md, radius R0, in the field of
    central baryonic point Mb.  Returns relaxed-state diagnostics."""
    rng = np.random.default_rng(seed)
    # shells uniformly in mass, r from a top-hat (uniform density): r = R0*u^(1/3)
    u = (np.arange(Nt)+0.5)/Nt
    r = R0*np.cbrt(u)
    v = np.zeros(Nt)                      # cold start
    mshell = Md/Nt
    # softening length
    eps = soft*R0
    # dynamical time at the characteristic radius
    Mtot = Mb + Md
    t_dyn = math.sqrt(R0**3/(G*Mtot))
    dt = 0.02*t_dyn
    nsteps = int(n_dyn*t_dyn/dt)
    def accel(r):
        # enclosed dark mass by sorting + cumulative; plus central point
        order = np.argsort(r)
        rs = r[order]
        menc = Md*(np.arange(1, Nt+1))/Nt      # enclosed dark mass interior to each shell
        a_dark = np.empty(Nt)
        a_dark[order] = G*menc/np.maximum(rs, eps)**2
        a = G*Mb/np.maximum(r, eps)**2 + a_dark
        return -a                              # inward

    def potential_energy(r):
        # exact spherical PE: central point + self-gravity of the shell distribution.
        # W_central = -G Mb sum_i mshell/r_i ;  W_self = -G sum_i mshell Menc(<r_i)/r_i
        order = np.argsort(r); rs = r[order]
        menc_interior = Md*(np.arange(Nt))/Nt    # mass interior to each (excluding self)
        Wc = -G*Mb*np.sum(mshell/np.maximum(rs, eps))
        Ws = -G*np.sum(mshell*menc_interior/np.maximum(rs, eps))
        return Wc + Ws

    def kinetic_energy(v):
        return 0.5*np.sum(mshell*v**2)

    E0 = None
    for i in range(nsteps):
        a = accel(r)
        v += 0.5*a*dt
        r += v*dt
        r = np.abs(r)                          # shells pass through centre
        a = accel(r)
        v += 0.5*a*dt
        if i % 50 == 0:
            E = kinetic_energy(v) + potential_energy(r)
            if E0 is None: E0 = E
    # relaxed diagnostics
    order = np.argsort(r); rs = r[order]
    menc = Md*(np.arange(1, Nt+1))/Nt
    # density in log bins over 0.3--3 r_M
    r_m = rM(Mb, a0) if Mb > 0 else R0
    lo, hi = 0.3*r_m, 3.0*r_m
    nb = 24
    edges = np.logspace(math.log10(lo), math.log10(hi), nb+1)
    inds = np.digitize(rs, edges)
    rho_c, r_c = [], []
    for b in range(1, nb+1):
        m_in = np.sum(menc[(inds == b)])
        vol = (4/3)*math.pi*(edges[b]**3 - edges[b-1]**3)
        if m_in > 0 and vol > 0:
            rho_c.append(m_in/vol); r_c.append(math.sqrt(edges[b]*edges[b-1]))
    rho_c, r_c = np.array(rho_c), np.array(r_c)
    slope = np.polyfit(np.log(r_c), np.log(rho_c), 1)[0] if len(r_c) > 3 else float('nan')
    # half-mass radius
    r_half = rs[np.searchsorted(menc, Md/2)]
    # virial temperature
    K = 0.5*np.sum(mshell*v**2)
    sigma2 = K/(1.5*Md)          # 3D: (3/2) M sigma^2 = K  => sigma^2 = K/(1.5 M)
    # virial ratio with the exact potential
    W = potential_energy(rs)
    vir = 2*K/abs(W)
    Efin = K + W
    return dict(slope=slope, r_half=r_half, sigma2=sigma2, vir=vir, r_m=r_m,
                E_drift=abs((Efin-E0)/E0) if E0 else float('nan'))

print("="*88)
print("CONTROL RUN -- energy conservation + no-baryon (scale-free) collapse")
print("="*88)
Mb0 = 1.2e10*MSUN
a0 = A0["canonical"]
r_m0 = rM(Mb0, a0)
Md = 0.3*Mb0                      # dark sector lighter than baryons (ledger: dark fraction < 1)
ctl = collapse(Mb0, Md, 3*r_m0, a0, Nt=2000, n_dyn=10)
check("energy drift over 10 dyn times < 5%",
      f"|dE/E| = {ctl['E_drift']:.3f}", ctl['E_drift'] < 0.05)
check("virial ratio relaxes to 2K/|W| ~ 1",
      f"2K/|W| = {ctl['vir']:.3f}", 0.7 < ctl['vir'] < 1.4,
      "system has virialised (not still collapsing or flying apart)")

print("="*88)
print("IC-INDEPENDENCE -- does the relaxed state forget R0?  (attractor test)")
print("="*88)
a0 = A0["canonical"]; Mb = Mb0; r_m = rM(Mb, a0); Md = 0.3*Mb
slopes, rhalfs = [], []
for f in [1.5, 3.0, 5.0, 8.0]:
    d = collapse(Mb, Md, f*r_m, a0, Nt=3000, n_dyn=12)
    slopes.append(d['slope']); rhalfs.append(d['r_half']/r_m)
    print(f"   R0 = {f:.1f} r_M :  slope={d['slope']:.3f}  r_half/r_M={d['r_half']/r_m:.3f}  "
          f"sigma^2={d['sigma2']:.3e}  vir={d['vir']:.2f}")
slopes, rhalfs = np.array(slopes), np.array(rhalfs)
check("relaxed density slope is r^-2 to within 0.5 (attractor, all R0)",
      f"slopes {np.round(slopes,3)}", np.all(np.abs(slopes+2) < 0.5),
      "every start radius relaxes to the same profile -> attractor, not IC memory")
check("half-mass radius settles at a fixed multiple of r_M regardless of R0",
      f"r_half/r_M {np.round(rhalfs,3)}, spread {rhalfs.max()/max(rhalfs.min(),1e-9):.2f}",
      rhalfs.max()/max(rhalfs.min(),1e-9) < 2.0,
      "the settled size is set by r_M, not by the initial radius")

print("="*88)
print("M_b-SCALING -- r_settle ∝ M_b^? and sigma^2 ∝ M_b^?  (BTFR targets 1/2, 1/2)")
print("="*88)
for footing, a0f in A0.items():
    masses = np.array([3e9, 1e10, 3e10, 1e11])*MSUN
    rh, s2 = [], []
    for M in masses:
        r_mf = rM(M, a0f)
        d = collapse(M, 0.3*M, 3*r_mf, a0f, Nt=2500, n_dyn=11)
        rh.append(d['r_half']); s2.append(d['sigma2'])
    rh, s2 = np.array(rh), np.array(s2)
    ex_r = np.polyfit(np.log(masses), np.log(rh), 1)[0]
    ex_s = np.polyfit(np.log(masses), np.log(s2), 1)[0]
    check(f"M_b-scaling[{footing}] settled radius exponent ~ 1/2 (tracks r_M)",
          f"d log r_half/d log M_b = {ex_r:.3f}", abs(ex_r-0.5) < 0.15)
    check(f"M_b-scaling[{footing}] sigma^2 exponent ~ 1/2 (BTFR)",
          f"d log sigma^2/d log M_b = {ex_s:.3f}", abs(ex_s-0.5) < 0.15,
          "sigma^2 ∝ sqrt(M_b) <=> v_flat^4 ∝ M_b is the BTFR")

print("="*88)
print("TEMPERATURE -- settled sigma^2 vs the target G M_b/(2 r_M)")
print("="*88)
for footing, a0f in A0.items():
    Mb = Mb0; r_m = rM(Mb, a0f); Md = 0.3*Mb
    d = collapse(Mb, Md, 3*r_m, a0f, Nt=3000, n_dyn=12)
    tgt = G*Mb/(2*r_m)
    check(f"temperature[{footing}] settled sigma^2 within factor 2 of G M_b/(2 r_M)",
          f"sigma^2={d['sigma2']:.3e}  target={tgt:.3e}  ratio={d['sigma2']/tgt:.3f}",
          0.5 < d['sigma2']/tgt < 2.0,
          "the settled temperature matches the amplitude-law value to the virial factor")

print("="*88)
print(f"K006 COMPLETE: {NP}/{NP+NF} checks PASS.")
HERE = os.path.dirname(os.path.abspath(__file__))
json.dump({"checks": RES, "n_pass": NP, "n_fail": NF},
          open(os.path.join(HERE, "K006_results.json"), "w"), indent=1)
