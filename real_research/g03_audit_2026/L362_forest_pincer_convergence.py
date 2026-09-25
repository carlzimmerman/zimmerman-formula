#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
L362 -- IS THE FOREST SIDE OF THE KiDS-FOREST PINCER CONVERGED?  Mass and mesh resolution at the decisive threshold.

WHY.  L358 found the KiDS-forest pincer on L342's switch HOLDS on the forest observable, but only through the finer
(25 Mpc/h) box: at the KiDS-accepted x_c = 3 the worst 1D flux-power deviation is 0.160 there and 0.096 in the 50 Mpc/h
box.  A resolution-conditional verdict has to be converged before it is quoted.  Two things were under-resolved in
L346-L358: MASS (96^3 particles on a 128^3 mesh, 0.42 per cell, so the CIC density that defines the switch variable
x = (3/2) Omega_m delta carries discreteness noise) and MESH (0.195-0.39 Mpc/h cells).

METHOD: L347's machinery, generalised to any (box L, mesh NG, particles NP) and otherwise unchanged (L176's PM; the
constraint-derived switch, Lean I26; nu_mono; FGPA flux with pressure filter, redshift-space velocities, thermal
broadening, Becker+2013 tau_eff; same seed).  Runs at x_c = 3 (both footings) and LCDM:
    A  (50, 128, 128)   mass-resolution test of the coarse box (1 particle per cell)
    B  (25, 128, 128)   mass-resolution test of the fine box
    C  (25, 256, 192)   mesh AND mass: 2x finer mesh than L358's fine box, 0.42 particles per cell as there
PRE-DECLARED
  * CONTROL C1: the generalised code at (50, 128, 96) reproduces L347's committed x_c = 5 canonical P1D ratio to 1e-3
    (CLASS's k-table is extended to 60 h/Mpc for the finer mesh).
  * THE CONVERGENCE VERDICT: the forest side of the pincer is RESOLUTION-ROBUST iff the worst |P1D ratio - 1| at x_c = 3
    (k_par 0.2-2 h/Mpc, z = 3 and 2, both footings) exceeds 0.10 in the HIGHEST-resolution run C AND in the mass-
    resolution run B; it is NOT robust if either falls to <= 0.10.  (The direction EXPECT_ROBUST = True was set as the
    hypothesis BEFORE a first run of this same script; that run confirmed it and is not committed.)
RESULT.  At x_c = 3 the worst flux-power deviation GROWS with resolution rather than converging away: L358's fine box
0.160 -> 0.157 with 2.4x the particles (B), -> 0.191 with a 2x finer mesh (C); the coarse box rises 0.096 -> 0.104 with
more particles (A).  The forest side of L352's KiDS-forest pincer is resolution-robust at the tested resolutions.
MUTATE=1: the switch never turns on in the x_c = 3 runs; every deviation vanishes and the verdict must flip (rc = 1).

Run from the repository root:  python3 real_research/g03_audit_2026/L362_forest_pincer_convergence.py
"""
import os, sys, json, math, time
import numpy as np
from multiprocessing import Pool
from scipy.optimize import brentq

HERE = os.path.dirname(os.path.abspath(__file__))
MUTATE = os.environ.get("MUTATE", "0") == "1"
SLUG = "L362_forest_pincer_convergence"
T0 = time.time()
P = lambda *a: print(*a, flush=True)
CH, OUT = [], {"lane": "L362", "mutate": MUTATE, "checks": {}, "numbers": {}}


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


h = 0.6736; Om = 0.3138; OL = 1 - Om; ZI = 49.0
A0_SI = {"canonical": 9.3619e-11, "alt": 1.1279e-10}
UNIT_ACC = 3.086e22 / h * (h * 3.2408e-18) ** 2
A0 = {k: v / UNIT_ACC for k, v in A0_SI.items()}
def Hnorm(a): return np.sqrt(Om * a ** -3 + OL)
def Om_a(a): return Om * a ** -3 / (Om * a ** -3 + OL)
ZOUT = [3.0, 2.0]
TAU_EFF = {3.0: 0.751 * (4.0 / 4.5) ** 2.90 - 0.132, 2.0: 0.751 * (3.0 / 4.5) ** 2.90 - 0.132}
BETA, RJ, BTH = 1.6, 0.1, 13.5

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
                      "N_ur": 3.046, "N_ncdm": 0, "YHe": 0.2454, "output": "mPk", "P_k_max_h/Mpc": 60, "z_max_pk": 60,
                      "non_linear": "halofit"}); cl.compute()
def P_lin(kh, z): return cl.pk_lin(kh * h, z) * h ** 3


class Sim:
    """L347's Box + flux + run, with (L, NG, NP) as parameters; the arithmetic is L347's line for line."""

    def __init__(self, L, NG, NP):
        self.L, self.NG, self.NP = L, NG, NP; self.d = L / NG; self.kf = 2 * np.pi / L
        kx = np.fft.fftfreq(NG, d=self.d) * 2 * np.pi
        KX, KY, KZ = np.meshgrid(kx, kx, kx, indexing='ij')
        self.K2 = KX ** 2 + KY ** 2 + KZ ** 2; self.K2[0, 0, 0] = 1.0
        self.kz1 = np.abs(np.fft.fftfreq(NG, d=self.d) * 2 * np.pi)

    def poisson(self, src):
        f = np.fft.fftn(src); f = -f / self.K2; f[0, 0, 0] = 0.0
        return np.real(np.fft.ifftn(f))

    def grad(self, f):
        return [(np.roll(f, -1, i) - np.roll(f, 1, i)) / (2 * self.d) for i in range(3)]

    def div(self, v):
        return sum((np.roll(v[i], -1, i) - np.roll(v[i], 1, i)) / (2 * self.d) for i in range(3))

    def smooth(self, f, R):
        return np.real(np.fft.ifftn(np.fft.fftn(f) * np.exp(-0.5 * self.K2 * R ** 2))) if R > 0 else f

    def _cic(self, x):
        g = x / self.d; i0 = np.floor(g).astype(int); f = g - i0; i0 %= self.NG; i1 = (i0 + 1) % self.NG
        return i0, i1, f

    def deposit(self, x, w):
        NG = self.NG; rho = np.zeros((NG, NG, NG)); i0, i1, f = self._cic(x)
        for dx in (0, 1):
            wx = f[:, 0] if dx else 1 - f[:, 0]; ix = i1[:, 0] if dx else i0[:, 0]
            for dy in (0, 1):
                wy = f[:, 1] if dy else 1 - f[:, 1]; iy = i1[:, 1] if dy else i0[:, 1]
                for dz in (0, 1):
                    wz = f[:, 2] if dz else 1 - f[:, 2]; iz = i1[:, 2] if dz else i0[:, 2]
                    np.add.at(rho, (ix, iy, iz), w * wx * wy * wz)
        return rho

    def interp(self, field, x):
        i0, i1, f = self._cic(x); out = np.zeros(len(x))
        for dx in (0, 1):
            wx = f[:, 0] if dx else 1 - f[:, 0]; ix = i1[:, 0] if dx else i0[:, 0]
            for dy in (0, 1):
                wy = f[:, 1] if dy else 1 - f[:, 1]; iy = i1[:, 1] if dy else i0[:, 1]
                for dz in (0, 1):
                    wz = f[:, 2] if dz else 1 - f[:, 2]; iz = i1[:, 2] if dz else i0[:, 2]
                    out += field[ix, iy, iz] * wx * wy * wz
        return out

    def flux_p1d(self, x, p, a, z):
        NG = self.NG; npart = len(x)
        rho = self.deposit(x, np.full(npart, 1.0)) * NG ** 3 / npart
        mom = self.deposit(x, p[:, 2]) * NG ** 3 / npart
        vz = np.where(rho > 0, mom / np.maximum(rho, 1e-12), 0.0) / a
        dgas = np.maximum(self.smooth(rho, RJ), 1e-6)
        tau_r = dgas ** BETA
        shift = vz / (a * Hnorm(a))
        zpos = (np.arange(NG) * self.d)[None, None, :] + shift
        g = (zpos % self.L) / self.d; j0 = np.floor(g).astype(int); fr = g - j0; j0 %= NG; j1 = (j0 + 1) % NG
        tau_s = np.zeros_like(tau_r)
        I, J = np.meshgrid(np.arange(NG), np.arange(NG), indexing='ij')
        I = np.repeat(I[:, :, None], NG, 2); J = np.repeat(J[:, :, None], NG, 2)
        np.add.at(tau_s, (I, J, j0), tau_r * (1 - fr)); np.add.at(tau_s, (I, J, j1), tau_r * fr)
        sig = (BTH / math.sqrt(2)) / (100.0 * Hnorm(a) * a)
        tau_s = np.real(np.fft.ifft(np.fft.fft(tau_s, axis=2) * np.exp(-0.5 * (self.kz1 * sig) ** 2)[None, None, :], axis=2))
        tau_s = np.maximum(tau_s, 0.0)
        Fbar_t = math.exp(-TAU_EFF[z])
        A = brentq(lambda A_: float(np.mean(np.exp(-A_ * tau_s))) - Fbar_t, 1e-6, 1e3)
        F = np.exp(-A * tau_s); dF = F / F.mean() - 1
        Pk1 = np.mean(np.abs(np.fft.fft(dF, axis=2)) ** 2, axis=(0, 1)) * self.L / NG ** 2
        kpar = np.fft.fftfreq(NG, d=self.d)[:NG // 2] * 2 * np.pi
        return kpar[1:], Pk1[1:NG // 2]


def run(cfg):
    name, L, NG, NP, mode, foot, xc = cfg
    s = Sim(L, NG, NP)
    rng = np.random.default_rng(7)
    kk = np.sqrt(s.K2); kk[0, 0, 0] = s.kf
    Pk = np.vectorize(lambda q: P_lin(q, ZI))(np.clip(kk, s.kf, 60.0)); Pk[0, 0, 0] = 0
    white = np.fft.fftn(rng.normal(size=(NG, NG, NG)))
    delta0 = np.real(np.fft.ifftn(white * np.sqrt(Pk * NG ** 3 / L ** 3)))
    psi = [-gg for gg in s.grad(s.poisson(delta0))]
    q = (np.arange(NP) + 0.5) * L / NP
    QX, QY, QZ = np.meshgrid(q, q, q, indexing='ij'); Q = np.stack([QX.ravel(), QY.ravel(), QZ.ravel()], 1)
    disp = np.stack([s.interp(pp, Q) for pp in psi], 1)
    ai = 1 / (1 + ZI); fg = Om_a(ai) ** 0.55
    x = (Q + disp) % L; p = ai ** 2 * Hnorm(ai) * fg * disp
    npart = len(x); a0 = A0[foot]

    def accel(x, a):
        rho = s.deposit(x, np.full(npart, 1.0)) * NG ** 3 / npart
        delta = rho - 1.0
        phiN = s.poisson(1.5 * Om * delta / a)
        if mode == "lcdm" or (not np.isfinite(xc)):
            phi = phiN
        else:
            gphi = s.grad(phiN)
            mag = np.sqrt(sum((gg / a ** 2) ** 2 for gg in gphi)) + 1e-30
            nu = nu_mono(mag / a0)
            xs = 1.5 * Om_a(a) * delta
            f = np.ones_like(xs) if xc == 0 else 0.5 * (1 + np.tanh((xs - xc) / (0.1 * xc)))
            phi = phiN + s.poisson(s.div([f * (nu - 1) * gg for gg in gphi]))
        return -np.stack([s.interp(gg, x) for gg in s.grad(phi)], 1)

    a = ai; dlna = 0.02; zs = list(ZOUT); out = {}
    acc = accel(x, a)
    while zs:
        da = a * (np.exp(dlna) - 1); dt = da / (a * Hnorm(a))
        p += 0.5 * dt * acc; x = (x + dt * p / a ** 2) % L; a = a + da
        acc = accel(x, a); p += 0.5 * dt * acc
        for z in list(zs):
            if 1 / a - 1 <= z + 1e-9:
                kpar, p1d = s.flux_p1d(x, p, a, z)
                out[str(z)] = {"kpar": kpar.tolist(), "p1d": p1d.tolist()}
                zs.remove(z)
    return name, out


INF = float("inf")
EXPECT_ROBUST = True                                  # the hypothesis, set before the first run (see docstring)
RUNS = {"A": (50.0, 128, 128), "B": (25.0, 128, 128), "C": (25.0, 256, 192)}

if __name__ == "__main__":
    P(__doc__)
    xc3 = INF if MUTATE else 3.0
    cfgs = [("ctrl_lcdm", 50.0, 128, 96, "lcdm", "canonical", 0), ("ctrl_x5", 50.0, 128, 96, "switch", "canonical", 5.0)]
    for tag, (L, NG, NP) in RUNS.items():
        cfgs.append((f"{tag}_lcdm", L, NG, NP, "lcdm", "canonical", 0))
        for foot in ("canonical", "alt"):
            cfgs.append((f"{tag}_x3_{foot}", L, NG, NP, "switch", foot, xc3))
    # heavy C runs first so they overlap the light ones
    cfgs.sort(key=lambda c: -c[2] ** 3)
    with Pool(len(cfgs)) as pool:
        res = dict(pool.map(run, cfgs))
    P(f"  {len(cfgs)} runs done in {time.time() - T0:.0f}s")
    OUT["numbers"]["runs"] = res

    def worst(name, ref):
        w = 0.0
        for z in ("3.0", "2.0"):
            kp = np.array(res[ref][z]["kpar"]); r = np.array(res[name][z]["p1d"]) / np.array(res[ref][z]["p1d"])
            m = (kp >= 0.2) & (kp <= 2.0); w = max(w, float(np.max(np.abs(r[m] - 1))))
        return w

    banner("CONTROL")
    L7 = json.load(open(os.path.join(HERE, "L347_switch_forest_flux_power_results.json")))["numbers"]["runs"]
    d = 0.0
    for z in ("3.0", "2.0"):
        mine = np.array(res["ctrl_x5"][z]["p1d"]) / np.array(res["ctrl_lcdm"][z]["p1d"])
        theirs = np.array(L7["L50_sw5_canon"][z]["p1d"]) / np.array(L7["L50_lcdm"][z]["p1d"])
        d = max(d, float(np.max(np.abs(mine - theirs))))
    check("C1 the generalised code at (50 Mpc/h, 128^3, 96^3) reproduces L347's committed x_c = 5 canonical P1D ratio to 1e-3",
          f"max |difference| = {d:.1e}", d < 1e-3,
          "the refactor is faithful; CLASS's k-table is extended to 60 h/Mpc for the finer mesh, which moves the ICs at ~1e-6")

    banner("F1  THE WORST FLUX-POWER DEVIATION AT x_c = 3 vs RESOLUTION")
    W = {}
    P("    L358 (committed): 50 Mpc/h 128^3 mesh 96^3 particles -> 0.096;  25 Mpc/h 128^3/96^3 -> 0.160")
    for tag, (L, NG, NP) in RUNS.items():
        W[tag] = max(worst(f"{tag}_x3_{f}", f"{tag}_lcdm") for f in ("canonical", "alt"))
        wc = worst(f"{tag}_x3_canonical", f"{tag}_lcdm")
        P(f"    run {tag}: {L:.0f} Mpc/h, mesh {NG}^3 ({L / NG:.3f} Mpc/h cells), particles {NP}^3 ({(NP / NG) ** 3:.2f}/cell): "
          f"worst {W[tag]:.3f} (canonical {wc:.3f})")
    OUT["numbers"]["worst_x3"] = W
    robust = W["B"] > 0.10 and W["C"] > 0.10
    check(f"F1 THE FOREST SIDE OF THE PINCER IS {'RESOLUTION-ROBUST' if EXPECT_ROBUST else 'NOT RESOLUTION-ROBUST'}: at the KiDS-"
          f"accepted x_c = 3 the worst flux-power deviation {'stays above' if EXPECT_ROBUST else 'falls to or below'} 0.10 "
          "with more particles (B) and with a 2x finer mesh (C)",
          f"B {W['B']:.3f}, C {W['C']:.3f} (A, coarse box with more particles: {W['A']:.3f})", robust == EXPECT_ROBUST,
          "pre-declared: robust iff both B and C exceed 0.10")

    banner("VERDICT")
    P(f"""  Worst 1D flux-power deviation at x_c = 3: L358 coarse 0.096, fine 0.160; A (50 Mpc/h, 1 particle/cell) {W['A']:.3f};
  B (25 Mpc/h, 1 particle/cell) {W['B']:.3f}; C (25 Mpc/h, 2x finer mesh) {W['C']:.3f}.  The forest side of L352's pincer is
  {'RESOLUTION-ROBUST' if robust else 'NOT resolution-robust'} at the tested resolutions.
  LIMITS: FGPA (no hydrodynamics), one realisation, 25 Mpc/h volume for the fine runs.""")

    n_fail = sum(1 for _, ok_, lb in CH if lb and not ok_)
    OUT["n_checks"], OUT["n_fail_load_bearing"] = len(CH), n_fail
    outname = f"{SLUG}_results{'_MUTATE' if MUTATE else ''}.json"
    json.dump(OUT, open(os.path.join(HERE, outname), "w"), indent=1, default=str)
    P(f"\n  {sum(1 for _, ok_, _ in CH if ok_)}/{len(CH)} checks pass; load-bearing failures: {n_fail}; wrote {outname}   [{time.time() - T0:.0f}s]")
    sys.exit(0 if n_fail == 0 else 1)
