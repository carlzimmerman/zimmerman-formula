#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
L346 -- THE LYMAN-ALPHA FOREST GATE FOR L342's BOUND-REGION SWITCH: does C-H/K + switch keep the z = 2-3 small-scale
power the forest measures?

WHY THIS GATE.  L342 repairs C-H/K's FRW failure (L341) with a switch: MOND acts only where x = 9 R3/(4 K^2) exceeds
x_c ~ 4-7 (KiDS-selected).  L342 checked LINEAR sigma_8, SPARC, the Solar System and KiDS -- not the forest.
THE SWITCH VARIABLE, FROM THE CONSTRAINT (corrected before commit -- the first run of this lane used L342's static-system
form (3/2) Omega_m (1 + delta), whose "1" switches MOND on too early).  With the CMC-stiff foliation K = 3H (L341 F5),
K_ij K^ij = K^2/3 + sigma^2 and the flat Friedmann relation 6 H^2 = 16 pi G rho_bar, the Hamiltonian constraint
R3 + K^2 - K_ij K^ij = 16 pi G rho gives R3 = 16 pi G rho_bar_m delta + sigma^2, hence
        x = (3/2) Omega_m(z) delta + 9 sigma^2/(4 K^2)  >=  (3/2) Omega_m(z) delta     (Lean I26).
(For galaxies delta >> 1 and this equals L342's 4 pi G rho_dyn/H^2; in the forest, delta ~ a few, the difference is
decisive.)  At z = 3, Omega_m = 0.967, so x > 5 wherever delta > 3.45: mildly nonlinear forest structures switch MOND
ON, at peculiar accelerations far below a0.  The forest needs P(k = 1-4 h/Mpc, z = 2-3) within ~10-20% of LCDM (the record's
standing criterion; L319 used the stricter >= 5.3 keV relic line).  This lane measures it.

METHOD (L176's validated cosmological particle-mesh machinery, copied not edited: 50 Mpc/h box, 128^3 mesh, 96^3
particles, Zel'dovich ICs at z = 49 from CLASS, same phases in every run; kernel on the peculiar Newtonian field, a0
constant -- the Llinares/Angus way, as L176/L341)
  * the CMB's cold fluid is present (L295; every carrier on the record is intact at z >= 2), so matter = LCDM's, and
    C-H/K reads the TOTAL field (L345 U0 / Lean I25: a minimally coupled cold fluid is boosted like baryons);
  * the switch: phantom source div[ f(x) (nu - 1) grad phi_N ], f = smooth step at x_c (width 0.1 x_c), with
        x = (3/2) Omega_m(a) delta_mesh        (NEWTONIAN mesh-scale density contrast, 0.39 Mpc/h; shear dropped)
    Dropping sigma^2 >= 0 bounds x from below exactly; the mesh smoothing lowers peak densities (checked: the 0.8 Mpc/h
    bracket gives less excess).  A third bracket adds one phantom iteration to delta (the dynamical density); it is
    reported, not assumed to be a bound (phantom densities can be negative in QUMOND lobes).
  * kernel nu_mono (L340; equal to nu_RAR below y = 2.54, i.e. everywhere in the forest), both footings.

CHECKS
  C1 CONTROL: the Newtonian LCDM PM run reproduces CLASS halofit within 35% for 0.3 <= k <= 2 h/Mpc at z = 3 (L176's V1
     criterion; PM resolution) -- only same-phase ratios are read below.
  C2 CONTROL: x_c -> infinity (switch never on) reproduces the LCDM run to 1e-6 (the switch plumbing is exact).
  C3 CONTROL: no switch (x_c = 0, MOND everywhere, L341's branch) overshoots the forest band -- the record's result.
  F1 THE DIAGNOSTIC: the mass fraction with x > x_c and its median |g_N|/a0 at z = 3 (deep MOND where the switch is on).
  F2 THE GATE: P_switch/P_LCDM in the forest band (k = 1-4 h/Mpc) at z = 3 and z = 2, x_c in {4, 5, 7}, both footings.
     Pre-declared: the switch PASSES the forest only if every ratio is within [0.8, 1.2] at x_c = 5 for both footings.
  F3 MONOTONICITY IN SMOOTHING: the 0.8 Mpc/h-smoothed switch gives LESS excess than the mesh-scale switch (finer
     definitions switch on more); the phantom-inclusive bracket is reported alongside.
MUTATE=1 sets x_c -> infinity in the gate runs: F2's excess vanishes and the load-bearing gate verdict must flip (rc=1).

Run from the repository root:  python3 real_research/g03_audit_2026/L346_switch_forest_gate.py
"""
import os, sys, json, math, time
import numpy as np
from multiprocessing import Pool
from scipy.optimize import brentq

HERE = os.path.dirname(os.path.abspath(__file__))
MUTATE = os.environ.get("MUTATE", "0") == "1"
SLUG = "L346_switch_forest_gate"
T0 = time.time()
P = lambda *a: print(*a, flush=True)
CH, OUT = [], {"lane": "L346", "mutate": MUTATE, "checks": {}, "numbers": {}}


def check(name, measured, ok, reading="", load_bearing=True):
    ok = bool(ok)
    CH.append((name, ok, load_bearing))
    OUT["checks"][name] = {"ok": ok, "measured": str(measured), "load_bearing": load_bearing}
    P(f"  [{'PASS' if ok else 'FAIL'}] {name}")
    P(f"         measured: {measured}")
    if reading:
        P(f"         reading:  {reading}")
    return ok


def banner(t):
    P("\n" + "=" * 110); P(t); P("=" * 110)


# ------------------------------------------------------------------------------------------ L176's PM machinery (copied)
h = 0.6736; Om = 0.3138; OL = 1 - Om
L = 50.0; NG = 128; NP = 96; ZI = 49.0
A0_SI = {"canonical": 9.3619e-11, "alt": 1.1279e-10}
UNIT_ACC = 3.086e22 / h * (h * 3.2408e-18) ** 2          # 1 (Mpc/h) H0^2 in m/s^2
A0 = {k: v / UNIT_ACC for k, v in A0_SI.items()}
def Hnorm(a): return np.sqrt(Om * a ** -3 + OL)
def Om_a(a): return Om * a ** -3 / (Om * a ** -3 + OL)
kf = 2 * np.pi / L
kx = np.fft.fftfreq(NG, d=L / NG) * 2 * np.pi
KX, KY, KZ = np.meshgrid(kx, kx, kx, indexing='ij'); K2 = KX ** 2 + KY ** 2 + KZ ** 2; K2[0, 0, 0] = 1.0


def poisson(src):
    f = np.fft.fftn(src); f = -f / K2; f[0, 0, 0] = 0.0
    return np.real(np.fft.ifftn(f))


def grad(f):
    d = L / NG
    return [(np.roll(f, -1, i) - np.roll(f, 1, i)) / (2 * d) for i in range(3)]


def div(v):
    d = L / NG
    return sum((np.roll(v[i], -1, i) - np.roll(v[i], 1, i)) / (2 * d) for i in range(3))


def smooth(f, R):
    return np.real(np.fft.ifftn(np.fft.fftn(f) * np.exp(-0.5 * K2 * R ** 2))) if R > 0 else f


def cic_deposit(x, w):
    rho = np.zeros((NG, NG, NG))
    g = x / (L / NG); i0 = np.floor(g).astype(int); f = g - i0; i0 %= NG; i1 = (i0 + 1) % NG
    for dx in (0, 1):
        wx = f[:, 0] if dx else 1 - f[:, 0]; ix = i1[:, 0] if dx else i0[:, 0]
        for dy in (0, 1):
            wy = f[:, 1] if dy else 1 - f[:, 1]; iy = i1[:, 1] if dy else i0[:, 1]
            for dz in (0, 1):
                wz = f[:, 2] if dz else 1 - f[:, 2]; iz = i1[:, 2] if dz else i0[:, 2]
                np.add.at(rho, (ix, iy, iz), w * wx * wy * wz)
    return rho


def cic_interp(field, x):
    g = x / (L / NG); i0 = np.floor(g).astype(int); f = g - i0; i0 %= NG; i1 = (i0 + 1) % NG
    out = np.zeros(len(x))
    for dx in (0, 1):
        wx = f[:, 0] if dx else 1 - f[:, 0]; ix = i1[:, 0] if dx else i0[:, 0]
        for dy in (0, 1):
            wy = f[:, 1] if dy else 1 - f[:, 1]; iy = i1[:, 1] if dy else i0[:, 1]
            for dz in (0, 1):
                wz = f[:, 2] if dz else 1 - f[:, 2]; iz = i1[:, 2] if dz else i0[:, 2]
                out += field[ix, iy, iz] * wx * wy * wz
    return out


def pk(delta, nb=14):
    f = np.fft.fftn(delta); Pw = np.abs(f) ** 2 * (L ** 3) / NG ** 6
    kk = np.sqrt(K2); kk[0, 0, 0] = 0
    edges = np.geomspace(0.15, 4.0, nb + 1); out = []
    for i in range(nb):
        m = (kk >= edges[i]) & (kk < edges[i + 1]); out.append((np.sqrt(edges[i] * edges[i + 1]), Pw[m].mean() if m.any() else np.nan))
    return np.array(out)


# L340's monotone kernel nu_mono (equal to nu_RAR below y_p = 2.54)
def h_rar(y):
    y = np.asarray(y, float)
    return np.where(y < 1e4, y / np.expm1(np.sqrt(np.minimum(y, 1e4))), 0.0)
def dh_rar(y, e=1e-6):
    return (h_rar(y * (1 + e)) - h_rar(y * (1 - e))) / (2 * y * e)
Y_P = brentq(lambda y: float(dh_rar(y)), 1.0, 5.0); H_P = float(h_rar(Y_P))
LYG = np.linspace(-12, 12, 240001); YG = 10 ** LYG
DH = np.maximum(dh_rar(YG), 0.05 * H_P / (YG + Y_P))
H_MONO = float(h_rar(YG[0])) + np.concatenate([[0.0], np.cumsum(0.5 * (DH[1:] + DH[:-1]) * np.diff(YG))])
def nu_mono(y):
    y = np.maximum(np.asarray(y, float), 1e-12)
    return 1.0 + np.interp(np.log10(y), LYG, H_MONO) / y


from classy import Class
cl = Class(); cl.set({"h": h, "omega_b": 0.02237, "omega_cdm": 0.12, "A_s": 2.1e-9, "n_s": 0.9649, "tau_reio": 0.0544,
                      "N_ur": 3.046, "N_ncdm": 0, "YHe": 0.2454, "output": "mPk", "P_k_max_h/Mpc": 20, "z_max_pk": 60,
                      "non_linear": "halofit"}); cl.compute()
def P_lin(kh, z): return cl.pk_lin(kh * h, z) * h ** 3
def P_nl(kh, z): return cl.pk(kh * h, z) * h ** 3


def make_ics(seed=7):
    rng = np.random.default_rng(seed)
    kk = np.sqrt(K2); kk[0, 0, 0] = kf
    Pk = np.vectorize(lambda q: P_lin(q, ZI))(np.clip(kk, kf, 20.0)); Pk[0, 0, 0] = 0
    white = np.fft.fftn(rng.normal(size=(NG, NG, NG)))
    delta = np.real(np.fft.ifftn(white * np.sqrt(Pk * NG ** 3 / L ** 3)))
    phi = poisson(delta); psi = [-gg for gg in grad(phi)]
    q = (np.arange(NP) + 0.5) * L / NP
    QX, QY, QZ = np.meshgrid(q, q, q, indexing='ij'); Q = np.stack([QX.ravel(), QY.ravel(), QZ.ravel()], 1)
    disp = np.stack([cic_interp(pp, Q) for pp in psi], 1)
    ai = 1 / (1 + ZI); f_growth = (Om * ai ** -3 / (Om * ai ** -3 + OL)) ** 0.55
    return (Q + disp) % L, ai ** 2 * Hnorm(ai) * f_growth * disp


ZOUT = [6.0, 3.0, 2.0]


def run(cfg):
    """cfg = (name, mode, foot, xc, Rs, phantom_in_x): mode 'lcdm' | 'switch'.  xc = 0 -> MOND everywhere."""
    name, mode, foot, xc, Rs, ph_in_x = cfg
    x, p = make_ics()
    npart = len(x); a0 = A0[foot]
    a = 1 / (1 + ZI); dlna = 0.02; zs = list(ZOUT); out = {}; diag = {}

    def accel(x, a, record=False):
        rho = cic_deposit(x, np.full(npart, 1.0)) * NG ** 3 / npart
        delta = rho - 1.0
        src = 1.5 * Om * delta / a
        phiN = poisson(src)
        if mode == "lcdm":
            phi = phiN; fmass = gmed = 0.0
        else:
            gphi = grad(phiN)
            gN = [-gg / a ** 2 for gg in gphi]
            mag = np.sqrt(sum(gg ** 2 for gg in gN)) + 1e-30
            nu = nu_mono(mag / a0)
            xs = 1.5 * Om_a(a) * smooth(delta, Rs)
            if ph_in_x:                                   # one phantom iteration: x from the phantom-inclusive density
                f0 = 1.0 if xc == 0 else 0.5 * (1 + np.tanh((xs - xc) / (0.1 * xc)))
                phiph = poisson(div([f0 * (nu - 1) * gg for gg in gphi]))
                dph = div(grad(phiph)) * a / (1.5 * Om)
                xs = 1.5 * Om_a(a) * smooth(delta + dph, Rs)
            if xc == 0:
                f = np.ones_like(xs)
            elif not np.isfinite(xc):
                f = np.zeros_like(xs)
            else:
                f = 0.5 * (1 + np.tanh((xs - xc) / (0.1 * xc)))
            phi = phiN + poisson(div([f * (nu - 1) * gg for gg in gphi]))
            on = f > 0.5
            fmass = float((rho * on).sum() / rho.sum())
            gmed = float(np.median((mag / a0)[on])) if on.any() else float("nan")
        gr = grad(phi)
        return -np.stack([cic_interp(gg, x) for gg in gr], 1), (fmass, gmed)

    acc, _ = accel(x, a)
    while zs:
        da = a * (np.exp(dlna) - 1); dt = da / (a * Hnorm(a))
        p += 0.5 * dt * acc
        x = (x + dt * p / a ** 2) % L
        a = a + da
        acc, dg = accel(x, a)
        p += 0.5 * dt * acc
        for z in list(zs):
            if 1 / a - 1 <= z + 1e-9:
                rho_t = cic_deposit(x, np.full(npart, 1.0)) * NG ** 3 / npart
                out[str(z)] = pk(rho_t - 1).tolist(); diag[str(z)] = dg; zs.remove(z)
    return name, {"pk": out, "diag": diag}


INF = float("inf")
if __name__ == "__main__":
    P(__doc__)
    xc_gate = INF if MUTATE else 5.0
    if MUTATE:
        P("  MUTATE: the gate runs use x_c = infinity (switch never on)")
    cfgs = [("lcdm", "lcdm", "canonical", 0, 0.0, False),
            ("never_on", "switch", "canonical", INF, 0.0, False),
            ("no_switch", "switch", "canonical", 0, 0.0, False),
            ("sw5_canon", "switch", "canonical", xc_gate, 0.0, False),
            ("sw5_alt", "switch", "alt", xc_gate, 0.0, False),
            ("sw4_canon", "switch", "canonical", (INF if MUTATE else 4.0), 0.0, False),
            ("sw7_canon", "switch", "canonical", (INF if MUTATE else 7.0), 0.0, False),
            ("sw5_smooth08", "switch", "canonical", xc_gate, 0.8, False),
            ("sw5_phantomx", "switch", "canonical", xc_gate, 0.0, True)]
    P(f"  box {L} Mpc/h, mesh {NG}^3, particles {NP}^3, z_i = {ZI}; a0 code units canonical {A0['canonical']:.1f}, alt {A0['alt']:.1f}")
    with Pool(5) as pool:
        res = dict(pool.map(run, cfgs))
    P(f"  runs done in {time.time() - T0:.0f}s")
    OUT["numbers"]["runs"] = res

    ref = {z: np.array(res["lcdm"]["pk"][z]) for z in ("3.0", "2.0")}
    kk = ref["3.0"][:, 0]; forest = (kk >= 1.0) & (kk <= 4.0)
    ratio = lambda name, z: np.array(res[name]["pk"][z])[:, 1] / ref[z][:, 1]

    banner("CONTROLS")
    rh = np.array([pp / P_nl(k_, 3.0) for k_, pp in ref["3.0"]]); m = (kk >= 0.3) & (kk <= 2.0)
    check("C1 the Newtonian LCDM PM run reproduces CLASS halofit within 35% for 0.3 <= k <= 2 h/Mpc at z = 3 (L176's V1)",
          f"P_PM/P_halofit {rh[m].min():.2f}-{rh[m].max():.2f}", np.max(np.abs(rh[m] - 1)) < 0.35)
    dn = max(np.max(np.abs(ratio("never_on", z) - 1)) for z in ("3.0", "2.0"))
    check("C2 x_c -> infinity (switch never on) reproduces the LCDM run exactly (same phases)", f"max |ratio - 1| = {dn:.1e}", dn < 1e-6)
    ns = ratio("no_switch", "3.0")[forest]
    check("C3 no switch (MOND everywhere, L341's branch) overshoots the forest band at z = 3", f"P/P_LCDM {ns.min():.2f}-{ns.max():.2f}",
          ns.min() > 1.2, "the record's result, reproduced in this code")

    banner("F1  WHERE THE SWITCH IS ON, AND HOW DEEP IN MOND")
    for name in ("sw5_canon", "sw5_phantomx", "sw5_smooth08"):
        for z in ("6.0", "3.0", "2.0"):
            fm, gm = res[name]["diag"][z]
            P(f"    {name:13s} z = {z}: mass fraction with x > x_c = {fm:.3f};  median |g_N|/a0 there = {gm:.2e}")
    fm3, gm3 = res["sw5_canon"]["diag"]["3.0"]
    OUT["numbers"]["F1"] = {n: res[n]["diag"] for n in ("sw5_canon", "sw5_phantomx", "sw5_smooth08")}
    check("F1 (informational) at z = 3 the switch is on in a finite fraction of the mesh-scale IGM mass, at deep-MOND accelerations",
          f"mass fraction {fm3:.3f}, median |g_N|/a0 {gm3:.1e}", True, "reported either way", load_bearing=False)

    banner("F2  THE GATE: P_switch / P_LCDM in the forest band (k = 1-4 h/Mpc)")
    gate = {}
    for name in ("sw4_canon", "sw5_canon", "sw7_canon", "sw5_alt", "sw5_smooth08", "sw5_phantomx", "no_switch"):
        for z in ("3.0", "2.0"):
            r = ratio(name, z)[forest]; gate[(name, z)] = (float(r.min()), float(r.max()))
            P(f"    {name:13s} z = {z}: " + " ".join(f"{v:6.2f}" for v in r) + f"   (k = {', '.join(f'{v:.2f}' for v in kk[forest])})")
    OUT["numbers"]["F2"] = {f"{n}_{z}": v for (n, z), v in gate.items()}
    passes = all(0.8 <= gate[(n, z)][0] and gate[(n, z)][1] <= 1.2 for n in ("sw5_canon", "sw5_alt") for z in ("3.0", "2.0"))
    worst = max(max(abs(gate[(n, z)][0] - 1), abs(gate[(n, z)][1] - 1)) for n in ("sw5_canon", "sw5_alt") for z in ("3.0", "2.0"))
    check("F2 THE FOREST GATE FAILS for L342's switch at its KiDS-selected x_c = 5 (both footings, z = 3 and 2): some forest-band "
          "ratio lies outside [0.8, 1.2] even with the minimal (mesh-scale Newtonian) switch variable",
          f"worst |P/P_LCDM - 1| = {worst:.2f}; x_c = 5 canonical z=3 {gate[('sw5_canon', '3.0')][0]:.2f}-{gate[('sw5_canon', '3.0')][1]:.2f}, "
          f"alt z=3 {gate[('sw5_alt', '3.0')][0]:.2f}-{gate[('sw5_alt', '3.0')][1]:.2f}",
          not passes, "pre-declared: the switch passes only if every ratio at x_c = 5 is in [0.8, 1.2]")

    banner("F3  THE BOUND IS ONE-SIDED")
    ex = lambda n: float(np.mean(np.abs(ratio(n, "3.0")[forest] - 1)))
    e_s, e_m, e_p = ex("sw5_smooth08"), ex("sw5_canon"), ex("sw5_phantomx")
    OUT["numbers"]["F3"] = dict(smooth08=e_s, mesh=e_m, phantom_x=e_p)
    check("F3 coarser smoothing of x gives less forest excess (finer, local definitions switch on more); the phantom-"
          "inclusive bracket is reported",
          f"mean |ratio - 1| at z = 3: 0.8 Mpc/h {e_s:.3f} <= mesh {e_m:.3f}; phantom-inclusive {e_p:.3f}",
          e_s <= e_m, "with sigma^2 >= 0 dropped, this is what makes the mesh-scale number a lower bound", load_bearing=False)

    banner("VERDICT")
    P(f"""  L342's switch turns MOND on wherever x = (3/2) Omega_m delta + 9 sigma^2/(4K^2) exceeds x_c.  At z = 3 that is {fm3:.0%} of the
  mesh-scale matter, at median |g_N| = {gm3:.1e} a0 -- deep MOND.  Forest band (k = 1-4 h/Mpc) with x_c = 5:
  canonical z = 3 {gate[('sw5_canon', '3.0')][0]:.2f}-{gate[('sw5_canon', '3.0')][1]:.2f}, z = 2 {gate[('sw5_canon', '2.0')][0]:.2f}-{gate[('sw5_canon', '2.0')][1]:.2f};
  alt z = 3 {gate[('sw5_alt', '3.0')][0]:.2f}-{gate[('sw5_alt', '3.0')][1]:.2f}, z = 2 {gate[('sw5_alt', '2.0')][0]:.2f}-{gate[('sw5_alt', '2.0')][1]:.2f}.
  Pre-declared gate [0.8, 1.2]: {'FAILED' if not passes else 'passed'}.  The mesh-scale Newtonian x without shear is the least-MOND
  definition: the shear term is non-negative and finer smoothing switches on more.  LIMITS: collisionless PM (no gas pressure, no UV background), 50 Mpc/h box,
  single realisation, P(k) of total matter rather than the flux power.""")

    n_fail = sum(1 for _, ok_, lb in CH if lb and not ok_)
    OUT["n_checks"], OUT["n_fail_load_bearing"] = len(CH), n_fail
    outname = f"{SLUG}_results{'_MUTATE' if MUTATE else ''}.json"
    json.dump(OUT, open(os.path.join(HERE, outname), "w"), indent=1, default=str)
    P(f"\n  {sum(1 for _, ok_, _ in CH if ok_)}/{len(CH)} checks pass; load-bearing failures: {n_fail}; wrote {outname}   [{time.time() - T0:.0f}s]")
    sys.exit(0 if n_fail == 0 else 1)
