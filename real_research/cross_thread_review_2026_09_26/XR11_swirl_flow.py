#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
XR11 (B) -- THE AUTHOR'S IDEA, READING (B): "the halos is like a fluid of dark energy swirling down between the bands".  Does
swirl or flow of the gas (or of the dark fluid) through the edge layer stabilise DE12's gradient instability?

WHY.  DE12 (7f84b3546): the varied MOND-sector gate is a k^0 negative bulk modulus on the layer's gas, so its perturbations
obey omega^2 = c_eff^2 k^2 with c_eff^2 = c_s^2 - c_gate^2 < 0: Gamma = k sqrt(c_gate^2 - c_s^2), UV-dominated.  A flow can
only (a) carry the gas through the layer before it grows, or (b) add a restoring frequency: rotation's epicyclic kappa,
or shear.  Both are k-independent, while Gamma grows with k.  Expected: no help.  This lane verifies it instead of
assuming it, on the gas (DE12's channel) and on reading (A)'s dark channel (XR11_dark_channel_gate.py).

CHECKS
  C1 CONTROL [load-bearing]: XR11_common's transition12 reproduces DE12's committed c_gate_max on all 24 galaxy layers (0e+00).
  X1 [sympy, load-bearing] the local (WKB) dispersion relation of a uniformly rotating compressible fluid with the gate's
     anti-pressure, from the linear equations (-i omega delta + i k.v = 0, -i omega v + 2 Omega x v = -i k c_eff^2 delta):
         omega^4 - omega^2 (c_eff^2 k^2 + 4 Omega^2) + 4 Omega^2 c_eff^2 k^2 cos^2(theta) = 0     (theta: angle of k to Omega).
     For c_eff^2 < 0 the product of its two omega^2 roots, 4 Omega^2 c_eff^2 k^2 cos^2(theta), is negative for every
     theta != 90 deg: a growing mode exists at EVERY rotation rate (and at theta = 0 rotation drops out: omega^2 = c_eff^2 k^2).
     At theta = 90 deg omega^2 = c_eff^2 k^2 + 4 Omega^2, stable only for k < 2 Omega/|c_eff|; with differential rotation
     (shearing sheet, axisymmetric) omega^2 = kappa^2 + c_eff^2 k^2, kappa^2 = 2 Omega (2 Omega - S) -- stable only for
     k < kappa/|c_eff|.
  X2 [numeric, load-bearing] shearing waves in the shearing sheet (U = -S x y^, rotation Omega, the same anti-pressure):
     for every (Omega, S)/(|c_eff| k0) with kappa < |c_eff| k0 -- the regime of every real layer, where Gamma/kappa ~ 1e2-1e4
     (X3) -- namely (0,0), (0,0.1), (0,1), (0,10), (0.1,0.1), (0.3,0.3) (S = Omega is a flat rotation curve), and initial
     wave angles from leading to trailing, every density perturbation grows by more than e^3 within t = 10/(|c_eff| k0):
     none is stabilised.  A compressional wave along the rotation axis (k = k z^) is identical to the unsheared,
     non-rotating one to 1e-10.  The case kappa > |c_eff| k0, (1, 1), is reported: there rotation holds the nearly
     axisymmetric waves, as X1 says -- the long-wave regime no real layer reaches.
  X3 [pre-declared, load-bearing] on every DE12 galaxy layer (z = 0.25, 1, 2.5, 4; M_b = 1e10, 1e11, 1e12; both footings;
     1e6 K gas, 117 km/s): (i) carrying the gas through the layer within 1/Gamma at the longest mode that fits (k = 2 pi/L)
     needs a flow speed above 10 v_f, v_f = (G M_b a0)^(1/4); (ii) rotation at v_phi = v_f -- the fastest swirl a region
     holds -- stabilises no mode that fits: 2 pi/k_rot > L, k_rot = kappa/sqrt(c_gate^2 - c_s^2), kappa = sqrt(2) v_f/r_e.
  X4 (reported) reading (A)'s dark channel (the phi_H door, S = 1; the fluid's stiffness its Jeans sigma): the flow and
     swirl needed, with the dark fluid swirling at v_f (generous) or at FL3's spin (v_rot = sqrt(2) 0.05 v_f), and FL3's
     vortex spacing at the layer -- below it the superfluid is irrotational and has no Coriolis force at all.
MUTATE=1 removes the gate's anti-pressure (c_eff^2 = +c_s^2, the gas alone): X1, X2 and X3 must FAIL (rc = 1).

SCOPE.  Local WKB (k >> 1/L), frozen background, DE12's layers and reading (A)'s; the epicyclic frequency of a flat rotation
curve at the layer; no self-gravity (it only adds attraction).  Not a simulation of the instability's outcome.

Run from the repository root:  python3 real_research/cross_thread_review_2026_09_26/XR11_swirl_flow.py
"""
import os, sys, json, math, time
import numpy as np
import sympy as sp
from scipy.integrate import solve_ivp

HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, HERE)
sys.dont_write_bytecode = True                                         # write nothing outside XR11_ files
from XR11_common import (G, A0, MS, KPC, CS, HBAR, EV, c_l, W_M, FOOT, Hz, transition12, cgate_max12, dark_layer,  # noqa: E402
                         layer_stats, jeans_sigma)

MUTATE = os.environ.get("MUTATE", "0") == "1"
SLUG = "XR11_swirl_flow"
T0 = time.time()
P = lambda *a: print(*a, flush=True)
CH, OUT = [], {"lane": "XR11_B", "mutate": MUTATE, "checks": {}, "numbers": {}}
SIGN = +1.0 if MUTATE else -1.0                                        # sign of c_eff^2 in the model problems (X1, X2)


def check(name, measured, ok, reading="", load_bearing=True):
    ok = bool(ok)
    CH.append((name, ok, load_bearing))
    OUT["checks"][name.split()[0]] = {"pass": ok, "measured": str(measured), "load_bearing": load_bearing}
    P(f"  [{'PASS' if ok else 'FAIL'}] {name}")
    P(f"         measured: {measured}")
    if reading: P(f"         reading:  {reading}")
    return ok


def banner(t): P("\n" + "=" * 110); P(t); P("=" * 110)


P(__doc__.split("CHECKS")[0].strip())
if MUTATE: P("\n  *** MUTATE=1: the gate's anti-pressure is removed (c_eff^2 = +c_s^2); X1, X2 and X3 must FAIL ***")

# ============================================================================================ C1
banner("C1  CONTROL: DE12's committed c_gate_max from XR11_common")
R12 = json.load(open(os.path.join(REPO, "real_research", "dark_energy_2026", "DE12_mond_sector_gate_stiffness_results.json")))["numbers"]["budget"]
dev = []
for key, row in R12.items():
    z, Mb, foot = key.split("/")
    cm, _ = cgate_max12(transition12(float(z), float(Mb), foot, 0.25))
    dev.append(abs(cm / row["c_gate_max"] - 1))
check("C1 CONTROL: XR11_common reproduces DE12's c_gate_max on all 24 galaxy layers", f"max rel dev {max(dev):.1e}", max(dev) < 1e-12)

# ============================================================================================ X1 sympy
banner("X1  THE ROTATING, COMPRESSIBLE LAYER WITH THE GATE'S ANTI-PRESSURE (sympy)")
w_, k_, Om_, th = sp.symbols("omega k Omega theta", real=True)
c2 = sp.Symbol("c2", real=True)                                        # c_eff^2 (negative where the gate wins)
kx, kz = k_ * sp.sin(th), k_ * sp.cos(th)
I = sp.I
M = sp.Matrix([[-I * w_, I * kx, 0, I * kz],                           # continuity (delta, vx, vy, vz)
               [I * kx * c2, -I * w_, -2 * Om_, 0],                     # x-momentum, Coriolis -2 Omega vy
               [0, 2 * Om_, -I * w_, 0],                                # y-momentum, Coriolis +2 Omega vx
               [I * kz * c2, 0, 0, -I * w_]])                           # z-momentum
disp = sp.expand(sp.simplify(M.det()))
target = w_ ** 4 - w_ ** 2 * (c2 * k_ ** 2 + 4 * Om_ ** 2) + 4 * Om_ ** 2 * c2 * k_ ** 2 * sp.cos(th) ** 2
ratio = sp.simplify(disp / target)
X_ = sp.Symbol("X")                                                    # omega^2
roots = sp.solve(target.subs(w_ ** 2, X_).subs(w_ ** 4, X_ ** 2), X_)
prod = sp.simplify(roots[0] * roots[1])
# differential rotation: the axisymmetric shearing sheet (delta, vx, vy), shear rate S
S_ = sp.Symbol("S", real=True)
Ms = sp.Matrix([[-I * w_, I * k_, 0], [I * k_ * c2, -I * w_, -2 * Om_], [0, 2 * Om_ - S_, -I * w_]])
disp_s = sp.factor(sp.expand(Ms.det()))
kap2 = 2 * Om_ * (2 * Om_ - S_)
ok_s = sp.simplify(sp.expand(Ms.det()) - (I * w_) * (w_ ** 2 - kap2 - c2 * k_ ** 2)) == 0
P(f"    det M = {disp}")
P(f"    det M / [omega^4 - omega^2 (c2 k^2 + 4 Omega^2) + 4 Omega^2 c2 k^2 cos^2 theta] = {ratio}")
P(f"    product of the two omega^2 roots = {prod};   shearing sheet (axisymmetric): det = {disp_s}; = i omega (omega^2 - kappa^2 - c2 k^2): {ok_s}")
# numeric sweep: for c2 = SIGN, every theta != 90 deg and Omega in [1e-3, 1e3] has a root with omega^2 < 0
unst = []
for Omv in (1e-3, 0.1, 1.0, 10.0, 1e3):
    for thv in np.radians([0, 10, 30, 60, 80, 89]):
        a1, a0 = -(SIGN * 1.0 + 4 * Omv ** 2), 4 * Omv ** 2 * SIGN * math.cos(thv) ** 2
        rts = np.roots([1.0, a1, a0])
        unst.append(bool(np.min(rts.real) < 0))
x1 = sp.simplify(ratio) in (1, -1) and sp.simplify(prod - 4 * Om_ ** 2 * c2 * k_ ** 2 * sp.cos(th) ** 2) == 0 and ok_s and all(unst)
check("X1 [sympy] the rotating layer's dispersion relation is omega^4 - omega^2 (c_eff^2 k^2 + 4 Omega^2) + 4 Omega^2 c_eff^2 k^2 "
      "cos^2 theta = 0; with the gate's anti-pressure (c_eff^2 < 0) a root has omega^2 < 0 for every theta != 90 deg at every "
      "Omega (1e-3 to 1e3 |c_eff| k); the shearing sheet's axisymmetric modes obey omega^2 = kappa^2 + c_eff^2 k^2",
      f"det ratio {ratio}; root product {prod}; shearing sheet {ok_s}; unstable in {sum(unst)}/{len(unst)} (Omega, theta) cases",
      x1, "rotation is a k-independent frequency that never enters modes along its axis: it cannot remove a UV instability")
OUT["numbers"]["X1"] = dict(det=str(disp), root_product=str(prod), unstable_cases=int(sum(unst)), n_cases=len(unst))

# ============================================================================================ X2 shearing waves
banner("X2  SHEARING WAVES WITH ROTATION: does shear or swirl stop the growth? (|c_eff| = k0 = 1 units)")


def shear_wave(Om, S, kx0, ky, kz=0.0, T=10.0):
    """delta, v in the shearing sheet: d delta/dt = -i k.v; dvx/dt = 2 Om vy - i kx c2 delta; dvy/dt = -(2 Om - S) vx - i ky c2 delta;
    dvz/dt = -i kz c2 delta; kx(t) = kx0 + S ky t.  c2 = SIGN (the anti-pressure, or the gas alone under MUTATE)."""
    def rhs(t, y):
        d, vx, vy, vz = y[0] + 1j * y[1], y[2] + 1j * y[3], y[4] + 1j * y[5], y[6] + 1j * y[7]
        kxt = kx0 + S * ky * t
        dd = -1j * (kxt * vx + ky * vy + kz * vz)
        dvx = 2 * Om * vy - 1j * kxt * SIGN * d
        dvy = -(2 * Om - S) * vx - 1j * ky * SIGN * d
        dvz = -1j * kz * SIGN * d
        return [dd.real, dd.imag, dvx.real, dvx.imag, dvy.real, dvy.imag, dvz.real, dvz.imag]
    sol = solve_ivp(rhs, (0, T), [1, 0, 0, 0, 0, 0, 0, 0], rtol=1e-10, atol=1e-12, dense_output=True)
    return abs(sol.y[0, -1] + 1j * sol.y[1, -1])


X2 = {}
CASES = [(0.0, 0.0), (0.0, 0.1), (0.0, 1.0), (0.0, 10.0), (0.1, 0.1), (0.3, 0.3)]   # gated: kappa < |c_eff| k0
LONG = (1.0, 1.0)                                                                       # reported: kappa = 1.41 |c_eff| k0
ANG = (-80, -45, -10, 10, 45, 80)                                     # initial wave angle from the x axis (leading < 0 < trailing)
for Om, S in CASES:
    for a in ANG:
        kx0, ky = math.cos(math.radians(a)) * (1 if a >= 0 else -1), abs(math.sin(math.radians(a)))
        X2[f"Om{Om}/S{S}/ang{a}"] = shear_wave(Om, S, kx0, ky)
XL = {a: shear_wave(LONG[0], LONG[1], math.cos(math.radians(a)) * (1 if a >= 0 else -1), abs(math.sin(math.radians(a)))) for a in ANG}
z_free = shear_wave(0.0, 0.0, 0.0, 0.0, kz=1.0)
z_rot = max(abs(shear_wave(Om, S, 0.0, 0.0, kz=1.0) / z_free - 1) for Om, S in CASES[1:])
gmin = min(X2.values())
P("    |delta(t = 10)| per (Omega, S) over the wave angles " + str(ANG) + ":")
for Om, S in CASES:
    P(f"      Omega {Om:4}, S {S:4}: " + ", ".join(f"{X2[f'Om{Om}/S{S}/ang{a}']:.2e}" for a in ANG))
P(f"    k along the rotation axis: |delta(10)| = {z_free:.4e} unsheared; max relative change with (Omega, S) = {z_rot:.1e}")
P(f"    reported, kappa = 1.41 |c_eff| k0 (Omega = S = 1): " + ", ".join(f"{a}: {XL[a]:.2e}" for a in ANG) +
  "  -- the long-wave regime where X1's axisymmetric modes are held")
x2 = gmin > math.e ** 3 and z_rot < 1e-10
check("X2 [numeric] no shearing wave is stabilised: every perturbation grows by more than e^3 within 10/(|c_eff| k0) for every "
      "(Omega, S) and angle; along the rotation axis the growth is unchanged (1e-10)",
      f"min |delta(10)| = {gmin:.2e} (e^3 = {math.e ** 3:.1f}); axis mode change {z_rot:.1e}", x2,
      "shear turns a wave's k; a trailing wave's |k| grows and so does its rate; a leading wave's rate dips to |c_eff||k_y| and "
      "recovers -- the anti-pressure is local, so there is no scale at which shear or swirl can hold it")
OUT["numbers"]["X2"] = dict(amplitudes=X2, axis_free=z_free, axis_change=z_rot, long_wave_case={str(a): v for a, v in XL.items()})

# ============================================================================================ X3 DE12's layers
banner("X3  DE12's GAS LAYERS: the flow needed to cross before growing, and the swirl's reach (1e6 K gas)")
csg = CS["1e6K"]
X3 = {}
ok3i, ok3ii = [], []
for z in (0.25, 1.0, 2.5, 4.0):
    for Mb in (1e10, 1e11, 1e12):
        for foot in FOOT:
            tr = transition12(z, Mb, foot, W_M)
            m = (tr["t"] > 0) & (tr["t"] < 1)
            cm, re_ = cgate_max12(tr)
            L = float(tr["r"][m].max() - tr["r"][m].min())
            vf = (G * Mb * MS * A0[foot]) ** 0.25
            ce2 = (csg ** 2 - cm ** 2) if not MUTATE else csg ** 2           # c_eff^2
            gam_c = math.sqrt(max(-ce2, 0.0))                                # |c_eff| where unstable
            v_need = 2 * math.pi * gam_c                                      # Gamma(2 pi/L) L
            v_need1 = (L / KPC) * gam_c                                       # Gamma(1/kpc) L
            kap = math.sqrt(2) * vf / re_
            lam_rot = 2 * math.pi * gam_c / kap if gam_c > 0 else 0.0        # modes longer than this are held by the swirl
            X3[f"{z}/{Mb:.0e}/{foot}"] = dict(c_gate=cm, L_kpc=L / KPC, r_e_kpc=re_ / KPC, v_f=vf, v_need_2piL=v_need, v_need_1kpc=v_need1,
                                              efolds_at_vf=v_need / vf, lam_rot_kpc=lam_rot / KPC, kappa_over_H=kap / tr["H"],
                                              Gamma_2piL_over_kappa=(2 * math.pi / L) * gam_c / kap, hubble_flow=tr["H"] * L)
            ok3i.append(v_need > 10 * vf); ok3ii.append(lam_rot > L)
            if foot == "canonical":
                x_ = X3[f"{z}/{Mb:.0e}/{foot}"]
                P(f"    z {z:4.2f} M_b {Mb:.0e}: layer {x_['L_kpc']:6.1f} kpc wide at {x_['r_e_kpc']:6.0f} kpc; c_gate {cm / 1e3:5.0f} km/s; "
                  f"flow to cross in 1/Gamma: {v_need / 1e3:6.0f} km/s (k = 2pi/L), {v_need1 / 1e3:8.0f} km/s (k = 1/kpc) vs v_f {vf / 1e3:4.0f}, "
                  f"Hubble flow across {x_['hubble_flow'] / 1e3:.1f}; e-folds per crossing at v_f {x_['efolds_at_vf']:.0f}; swirl at v_f holds "
                  f"only lambda > {x_['lam_rot_kpc'] / 1e3:.1f} Mpc (Gamma(2pi/L)/kappa = {x_['Gamma_2piL_over_kappa']:.0f})")
check("X3 [pre-declared] on every DE12 galaxy layer: crossing within 1/Gamma needs a flow above 10 v_f, and swirl at v_f "
      "stabilises no mode that fits in the layer",
      f"(i) {sum(ok3i)}/{len(ok3i)}; (ii) {sum(ok3ii)}/{len(ok3ii)}; min v_need/v_f = "
      f"{min(v_['v_need_2piL'] / v_['v_f'] for v_ in X3.values()):.1f}; min lambda_rot/L = "
      f"{min((v_['lam_rot_kpc'] / v_['L_kpc']) for v_ in X3.values()):.1f}", all(ok3i) and all(ok3ii),
      "the gas would have to stream through the layer at thousands of km/s, and the swirl's epicyclic frequency is ~1e3-1e4 "
      "below Gamma at the layer's own scale")
OUT["numbers"]["X3"] = X3

# ============================================================================================ X4 the dark channel
banner("X4  READING (A)'s DARK CHANNEL: flow and swirl of the dark fluid through its own layers (phi_H door, S = 1)")
X4 = {}
for z in (0.25, 2.5, 4.0):
    for Mb in (1e10, 1e11, 1e12):
        for foot in FOOT:
            L_ = dark_layer(z, Mb, foot, n=1.0, S=1.0)
            st = layer_stats(L_)
            sJ = jeans_sigma(z, Mb, st["r_e"])
            c = st["c_max"]
            gam_c = math.sqrt(max(c ** 2 - sJ ** 2, 0.0))
            L = st["r_in"] - st["r_out"] if st["r_in"] > st["r_out"] else st["r_out"] - st["r_in"]
            vf = (G * Mb * MS * A0[foot]) ** 0.25
            out = dict(c_gate_d=c, sigma_J=sJ, L_kpc=L / KPC, r_e_kpc=st["r_e"] / KPC, v_need_2piL=2 * math.pi * gam_c,
                       v_need_cold=2 * math.pi * c)
            for lab, vrot in (("v_f", vf), ("FL3 spin 0.05", math.sqrt(2) * 0.05 * vf)):
                kap = math.sqrt(2) * vrot / st["r_e"]
                out[f"lam_rot_{lab}_kpc"] = (2 * math.pi * gam_c / kap) / KPC if gam_c > 0 else 0.0
                out[f"lam_rot_cold_{lab}_kpc"] = (2 * math.pi * c / kap) / KPC
                mk = 2e-19 * EV / c_l ** 2
                Omg = vrot / st["r_e"]
                out[f"l_vortex_{lab}_kpc"] = (mk * Omg / (math.pi * HBAR)) ** -0.5 / KPC
            X4[f"{z}/{Mb:.0e}/{foot}"] = out
            if foot == "canonical":
                P(f"    z {z:4.2f} M_b {Mb:.0e}: c_gate,d {c / 1e3:4.0f} vs sigma_J {sJ / 1e3:4.0f} km/s; layer {L / KPC:5.0f} kpc; flow to cross "
                  f"in 1/Gamma {out['v_need_2piL'] / 1e3:5.0f} km/s (phase-mixed) / {out['v_need_cold'] / 1e3:5.0f} (cold) vs v_f {vf / 1e3:3.0f}; "
                  f"swirl at v_f holds lambda > {out['lam_rot_cold_v_f_kpc'] / 1e3:.1f} Mpc (cold), at FL3's spin > "
                  f"{out['lam_rot_cold_FL3 spin 0.05_kpc'] / 1e3:.0f} Mpc; vortex spacing at the layer {out['l_vortex_FL3 spin 0.05_kpc']:.2f} kpc")
OUT["numbers"]["X4"] = X4
check("X4 (reported) the dark fluid's own flow or swirl cannot hold its channel either: the needed flow is several times its "
      "v_f, the swirl holds only Mpc-scale modes, and below the vortex spacing the superfluid has no Coriolis force",
      {k_: f"v_need {v_['v_need_cold'] / 1e3:.0f} km/s, swirl lambda > {v_['lam_rot_cold_v_f_kpc'] / 1e3:.1f} Mpc"
       for k_, v_ in X4.items() if k_.endswith("canonical")}, True, load_bearing=False)

nlb = sum(1 for _, ok, lb in CH if lb and not ok)
OUT["n_checks"], OUT["n_fail_load_bearing"], OUT["elapsed_s"] = len(CH), nlb, round(time.time() - T0)
fn = os.path.join(HERE, SLUG + ("_results_MUTATE.json" if MUTATE else "_results.json"))
json.dump(OUT, open(fn, "w"), indent=1, default=str)
P(f"\n  {sum(ok for _, ok, _ in CH)}/{len(CH)} checks pass; load-bearing failures: {nlb}; wrote {os.path.basename(fn)}   "
  f"[{time.time() - T0:.0f}s]")
sys.exit(1 if nlb else 0)
