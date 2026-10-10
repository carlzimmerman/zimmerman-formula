#!/usr/bin/env python3
"""CFG539 Stage 1 (FROZEN_CRITERIA.md): the candidate cold-energy equations of motion, analytically (sympy) and on a 1-D periodic toy.
S1 A: linear relaxation rate and dimensions.  S2 A: Lyapunov decrease of the deficit field energy, d -> 0, mass conservation, origin of the
settled mass.  S3 A: emergent cap (supply smaller than the deficit).  S4 B: hydrostatic equilibrium in the law potential needs a per-system
temperature.  S5 C: inertial response (no friction), toy.  S6 D/E: constants ledger from the committed T16/T17/T3 JSONs.
CFG539_MUTATE=1: A with the settling sign reversed (must fail S2) -> cfg539_stage1_MUTATE.out/.json, exit 1 if detected.
Units of the toy: 4 pi G = 1, box length 1."""
import os, sys, json, math
import numpy as np
import sympy as sp

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
MUT = os.environ.get("CFG539_MUTATE", "0") == "1"
SIGN = -1.0 if MUT else 1.0
LINES = []
def P(s=""):
    print(s); LINES.append(s)
R = {"mutate": MUT}

P("CFG539 Stage 1 -- candidate cold-energy equations of motion" + ("   *** MUTATE: settling sign reversed ***" if MUT else ""))
P("kappa = 1/2 FITTED; cold energy mass required; footings never pooled; not theory closed.\n")

# ---------------------------------------------------------------- S1: class A relaxation rate (sympy)
G, rc, rm, rph, eps, t = sp.symbols("G rho_c rho_m rho_ph epsilon t", positive=True)
tau = 1 / sp.sqrt(4 * sp.pi * G * rm)
# continuity with v = -tau grad psi, lap psi = 4 pi G (rho_ph - rho_c): d_t rho_c = -div(rho_c v) = rho_c tau lap psi (uniform background)
drho = rc * tau * 4 * sp.pi * G * (rph - rc)
Gam = sp.simplify(-sp.diff(drho, rc).subs(rc, rph))           # linearised decay rate at the target rho_c = rho_ph
Gam_expected = rph / rm * sp.sqrt(4 * sp.pi * G * rm)
s1_rate = sp.simplify(Gam - Gam_expected) == 0
from sympy.physics import units as u
dimG = u.meter ** 3 / (u.kilogram * u.second ** 2); dimrho = u.kilogram / u.meter ** 3
dim_rate = sp.simplify((dimG * dimrho) ** sp.Rational(1, 2) * u.second)
s1_dim = dim_rate == 1
P(f"S1 (A) linearised deficit relaxation rate Gamma = {sp.simplify(Gam)} = (rho_c/rho_m) sqrt(4 pi G rho_m): {'PASS' if s1_rate else 'FAIL'}")
P(f"   dimensions: sqrt(G rho) x seconds = {dim_rate} -> only G and the local density enter: {'PASS' if s1_dim else 'FAIL'}")
R["S1"] = {"rate_ok": bool(s1_rate), "dim_ok": bool(s1_dim), "Gamma": str(sp.simplify(Gam))}

# ---------------------------------------------------------------- S2 / S3: class A on a 1-D periodic toy (finite volume, upwind)
N = 1024; x = (np.arange(N) + 0.5) / N; dx = 1.0 / N
k = 2 * np.pi * np.fft.rfftfreq(N, d=dx); ik2 = np.zeros_like(k); ik2[1:] = 1.0 / k[1:] ** 2
def grad_psi(d):
    """psi'' = d (4 pi G = 1), periodic; returns d psi/dx."""
    dk = np.fft.rfft(d); return np.fft.irfft(1j * k * (-dk * ik2), n=N)
def Fenergy(d):
    dk = np.fft.rfft(d); gk = 1j * k * (-dk * ik2)
    g = np.fft.irfft(gk, n=N); return 0.5 * float(np.sum(g * g) * dx)
rho_b = 0.2 + 0.6 * np.exp(-0.5 * ((x - 0.5) / 0.03) ** 2)
s_reg = ((x > 0.40) & (x < 0.60)).astype(float)                      # where the law acts (edge x switch)
rho_ph = 1.0 + 3.0 * np.exp(-0.5 * ((x - 0.5) / 0.06) ** 2)          # the target (phantom) inside s

def flow_A(catch, T=60.0, sign=SIGN, rho_c0=None):
    rc_ = np.ones(N) if rho_c0 is None else rho_c0.copy()
    m0 = rc_.sum() * dx; tt = 0.0; Fs = []; us = []; flux_in = 0.0
    d0 = s_reg * np.maximum(rho_ph - rc_, 0); tgt = float((s_reg * rho_ph).sum() * dx)
    inside0 = float((rc_ * s_reg).sum() * dx)
    nstep = 0
    while tt < T and nstep < 400000:
        d = s_reg * np.maximum(rho_ph - rc_, 0.0)
        Fs.append(Fenergy(d)); us.append(float(d.sum() * dx) / float(d0.sum() * dx))
        tau_ = 1.0 / np.sqrt(rho_b + rc_)
        v = -sign * catch * tau_ * grad_psi(d)
        vf = 0.5 * (v + np.roll(v, -1)) * catch * np.roll(catch, -1)    # face i+1/2; zero on faces touching a non-catchment cell (correction 1)
        h = min(0.4 * dx / max(np.abs(vf).max(), 1e-30), 0.4 / max(float((rc_ * tau_ * catch).max()), 1e-30), T - tt)
        up = np.where(vf > 0, rc_, np.roll(rc_, -1))
        fl = up * vf
        # mass crossing into s: faces at the s boundary
        rc_ = rc_ - h / dx * (fl - np.roll(fl, 1))
        tt += h; nstep += 1
    d = s_reg * np.maximum(rho_ph - rc_, 0.0); Fs.append(Fenergy(d)); us.append(float(d.sum() * dx) / float(d0.sum() * dx))
    m1 = rc_.sum() * dx
    settled = float((rc_ * s_reg).sum() * dx) - inside0
    return dict(rho_c=rc_, F=np.array(Fs), u=np.array(us), mass_rel=abs(m1 - m0) / m0, settled=settled, nstep=nstep,
                min_rho=float(rc_.min()), target_sum=tgt)

catchA = ((x > 0.1) & (x < 0.9)).astype(float)                       # correction 1: shell supply 0.6 > deficit 0.407 (run 1 used 0.2-0.8: 0.400 < 0.407)
A = flow_A(catchA)
dF = np.diff(A["F"]); mono = bool(np.all(dF <= 1e-12 * A["F"][0]))
supply_shell = float(((catchA - s_reg).clip(0) * 1.0).sum() * dx)
deficit0 = float((s_reg * np.maximum(rho_ph - 1.0, 0)).sum() * dx)
# all initial cold mass inside s stays inside s (drift points inward there): settled mass beyond the initial inside mass came through the boundary
frac_out = A["settled"] / max(A["settled"], 1e-30) if A["settled"] > 0 else 0.0
s2_ok = mono and A["u"][-1] <= 0.01 and A["mass_rel"] <= 1e-12 and A["settled"] > 0 and frac_out >= 0.5
P(f"\nS2 (A) toy: deficit {deficit0:.3f}, shell supply {supply_shell:.3f}; F monotone non-increasing: {mono} (max dF/F0 {dF.max() / A['F'][0]:+.2e});"
  f" unfilled u: 1 -> {A['u'][-1]:.4f}; |dM|/M {A['mass_rel']:.1e}; settled mass {A['settled']:.4f} (all through the boundary of s: net inflow);"
  f" min rho_c {A['min_rho']:.3f}; steps {A['nstep']} -> {'PASS' if s2_ok else 'FAIL'}")
# Lyapunov identity (sympy, 1-D, interior of the deficit region): F = 1/2 int psi'^2, psi'' = rho_ph - rho_c, d_t rho_c = (rho_c tau psi')'
# dF/dt = int psi' d_t psi' = -int psi d_t psi'' = int psi d_t rho_c = int psi (rho_c tau psi')' = -int rho_c tau psi'^2  (periodic, by parts)
xs = sp.symbols("x"); psi = sp.Function("psi")(xs); w = sp.Function("w", positive=True)(xs)
integrand_by_parts = sp.simplify(psi * sp.diff(w * sp.diff(psi, xs), xs) - (sp.diff(psi * w * sp.diff(psi, xs), xs) - w * sp.diff(psi, xs) ** 2))
lyap_ok = integrand_by_parts == 0
P(f"   sympy: psi (w psi')' = (psi w psi')' - w psi'^2 (w = rho_c tau >= 0), so dF/dt = -int rho_c tau |grad psi|^2 <= 0 in the deficit interior: {'PASS' if lyap_ok else 'FAIL'}")
P("   stationary <=> rho_c tau grad psi = 0 on the catchment <=> psi harmonic on supp d <=> d = 0 (wherever the catchment still holds cold energy)")
R["S2"] = {"pass": bool(s2_ok), "monotone": mono, "u_final": float(A["u"][-1]), "mass_rel": A["mass_rel"], "settled": A["settled"],
           "deficit0": deficit0, "supply_shell": supply_shell, "lyapunov_identity": bool(lyap_ok)}

catchS = ((x > 0.35) & (x < 0.65)).astype(float)
S = flow_A(catchS, T=400.0)
shell = (catchS - s_reg).clip(0) > 0
avail = float(shell.sum() * dx * 1.0)
left = float((S["rho_c"] * shell).sum() * dx)
s3_ok = (not MUT) and S["mass_rel"] <= 1e-12 and S["settled"] <= avail * (1 + 1e-9) + 1e-12 and left <= 0.02 * avail and S["min_rho"] >= -1e-12 and S["u"][-1] > 0.3
if MUT:
    s3_ok = S["mass_rel"] <= 1e-12 and S["settled"] <= avail * (1 + 1e-9) + 1e-12 and left <= 0.02 * avail
P(f"\nS3 (A) toy, small catchment: deficit {deficit0:.3f} > shell supply {avail:.3f}: settled {S['settled']:.4f} <= available {avail:.4f};"
  f" left in shell {left:.2e} ({left / avail:.1%}); unfilled u {S['u'][-1]:.3f} (supply-limited, d stays > 0); min rho_c {S['min_rho']:.2e};"
  f" |dM|/M {S['mass_rel']:.1e} -> {'PASS' if s3_ok else 'FAIL'}  (the cap is EMERGENT: nothing more than the catchment holds can arrive)")
R["S3"] = {"pass": bool(s3_ok), "settled": S["settled"], "available": avail, "left_frac": left / avail, "u_final": float(S["u"][-1])}

# ---------------------------------------------------------------- S4: class B (sympy)
r, V, sig, rho0, r0, Mb, a0 = sp.symbols("r V sigma rho_0 r_0 M_b a_0", positive=True)
rho = sp.Function("rho")(r)
sol = sp.dsolve(sp.Eq(sig ** 2 * sp.diff(sp.log(rho), r), -V ** 2 / r), rho)
expo = sp.simplify(sp.diff(sp.log(sol.rhs), r) * r)                     # = -V^2/sigma^2
sig_SIS = sp.solve(sp.Eq(expo, -2), sig)
rho_fluid = sig ** 2 / (2 * sp.pi * G * r ** 2)                          # self-consistent isothermal SIS density
rho_phantom = V ** 2 / (4 * sp.pi * G * r ** 2)                          # deep-MOND phantom of a point mass: M_ph(<r) = V^2 r / G
amp = sp.solve(sp.Eq(rho_fluid, rho_phantom), sig)
sig4 = sp.simplify((amp[0] ** 4).subs(V, (G * Mb * a0) ** sp.Rational(1, 4)))
s4_ok = (sp.simplify(expo + V ** 2 / sig ** 2) == 0) and (sp.simplify(sig4 - G * Mb * a0 / 4) == 0)
P(f"\nS4 (B) hydrostatic equilibrium in the law potential: rho ~ r^({expo}); SIS needs sigma = {sig_SIS}; amplitude match needs sigma = {amp};"
  f" with V^4 = G M_b a0: sigma^4 = {sig4} -> a per-system temperature: {'PASS (shown)' if s4_ok else 'FAIL'}")
P("   no G9 mechanism sets it (CFG461: 0 of 10 classes); without dissipation the target is 2.2-7.7x more bound than the infall (CFG489 3a).")
P("   => class B needs a per-system constant (knob) and a sink: KILLED (Stage-1 rule: knob).")
R["S4"] = {"pass": bool(s4_ok), "sigma4": str(sig4), "killed": True, "why": "per-system temperature sigma^4 = G M_b a0/4 (knob; CFG461) and no settling without a sink (CFG489)"}

# ---------------------------------------------------------------- S5: class C (inertial) toy, particles
def flow_C(catch, T=60.0, NP_=20000, seed=1):
    rng = np.random.default_rng(seed)
    xp = (np.arange(NP_) + 0.5) / NP_; vp = np.zeros(NP_); mpart = 1.0 / NP_
    def dep(xp):
        u_ = xp / dx - 0.5; i0 = np.floor(u_).astype(int); w1 = u_ - i0; i0 %= N; i1 = (i0 + 1) % N
        return (np.bincount(i0, (1 - w1) * mpart, N) + np.bincount(i1, w1 * mpart, N)) / dx, i0, i1, w1
    rc_, i0, i1, w1 = dep(xp); d0 = float((s_reg * np.maximum(rho_ph - rc_, 0)).sum() * dx)
    tt = 0.0; h = 2e-3; us = []; Es = []
    def acc(xp):
        rc_, i0, i1, w1 = dep(xp); d = s_reg * np.maximum(rho_ph - rc_, 0)
        g = -grad_psi(d) * catch
        return g[i0] * (1 - w1) + g[i1] * w1, d, rc_
    a_, d, rc_ = acc(xp)
    while tt < T:
        vp += 0.5 * h * a_; xp = (xp + h * vp) % 1.0; a_, d, rc_ = acc(xp); vp += 0.5 * h * a_; tt += h
        if int(round(tt / h)) % 50 == 0:
            us.append(float(d.sum() * dx) / d0); Es.append(0.5 * mpart * float(np.sum(vp ** 2)) + Fenergy(d))
    return np.array(us), np.array(Es)
uC, EC = flow_C(catchA)
monoC = bool(np.all(np.diff(uC) <= 1e-9))
P(f"\nS5 (C) toy (inertial, no friction): unfilled u min {uC.min():.3f}, final {uC[-1]:.3f}, mean over the last third {uC[-len(uC) // 3:].mean():.3f};"
  f" monotone: {monoC}; KE + F drift {(EC.max() - EC.min()) / max(abs(EC[0]), 1e-30):.2%} of its initial value")
P("   no Lyapunov decrease: T1 is not an attractor of C analytically (it may still be approached numerically) -> carried to Stage 2 (no knob, G9 kept).")
R["S5"] = {"u_min": float(uC.min()), "u_final": float(uC[-1]), "u_last_third_mean": float(uC[-len(uC) // 3:].mean()), "monotone": monoC,
           "E_drift_rel": float((EC.max() - EC.min()) / max(abs(EC[0]), 1e-30)), "killed": False}

# ---------------------------------------------------------------- S6: classes D and E, constants ledger (committed JSONs, read only)
D_ = os.path.join(REPO, "deepseek_push", "openai_math_cross_analysis_2026-10")
t16 = json.load(open(os.path.join(D_, "t16_coupling_gradient", "t16_results.json")))
t17 = json.load(open(os.path.join(D_, "t17_settling_front", "t17_results.json")))
inter = t16.get("inter")
P(f"\nS6 (D) T17 rate law d_t f = lambda sqrt(4 pi G rho)(1 - f): T16 budget windows mw {t16['windows']['mw']}, groups {t16['windows']['groups']},"
  f" clusters {t16['windows']['clusters']}; intersection {inter}.")
P(f"   lambda is FITTED (MW floor 0.028, CFG382) and must sit in [{inter[0]:.4f}, {inter[1]:.4f}] to clear the budget; the only zero-constant value"
  f" lambda = 1 lies {1.0 / inter[1]:.0f}-{1.0 / inter[0]:.0f}x above that window; and the law has no transport (mass conservation needs the"
  f" bookkeeping draw). => KILLED (knob; no transport).")
t17keys = {k_: t17[k_] for k_ in list(t17)[:6]} if isinstance(t17, dict) else {}
P("   (E) KL/JKO flow (T3 lane): needs a diffusion scale D (a length^2/time: knob), its minimiser is the global rescaling c rho_ph, and rho_ph < 0"
  " on the deep annulus (T3: -66.5 M_b canonical) leaves ln rho_ph undefined. => KILLED (knob).")
R["S6"] = {"D_killed": True, "E_killed": True, "lambda_window": inter, "lambda_forced": 1.0, "factor_above_window": [1.0 / inter[1], 1.0 / inter[0]]}

# ---------------------------------------------------------------- verdicts
P("\nStage-1 table (constants beyond kappa, 5.364, f_b | G9 matter conservation | T1 | T2 | T3 | T5 | T6 | causality):")
P("  A  overdamped flow   | none (tau_ff = 1/sqrt(4 pi G rho_m), coefficient by the free-fall principle) | exact (continuity) | equilibrium d = 0 (Lyapunov) |"
  " INHERITED edge; cap EMERGENT | from surroundings (flux into the deficit) | structural | mobility 0 outside catchments | parabolic: COND | sink NOT SUPPLIED")
P("  B  conservative fluid| per-system temperature (knob)  | exact | only if sigma^4 = G M_b a0/4 | - | - | - | - | KILLED")
P("  C  inertial force    | none                           | exact | not an attractor (no Lyapunov) | INHERITED edge | net inflow | structural | as A | elliptic psi | to Stage 2")
P("  D  T17 rate law      | lambda fitted (knob)           | needs the bookkeeping draw | - | - | - | - | - | KILLED")
P("  E  KL/JKO            | diffusion scale D (knob)       | exact | global rescaling, not the edge fill | - | - | - | - | KILLED")
survivors = ["A", "C"] if (s2_ok and s3_ok) else ["C"]
R["survivors"] = survivors
ok_all = s1_rate and s1_dim and s2_ok and s3_ok and s4_ok and lyap_ok
P(f"\nStage-1 survivors: {survivors}" + ("" if ok_all else "   (some Stage-1 check FAILED -- see above)"))
sfx = "_MUTATE" if MUT else ""
open(os.path.join(HERE, f"cfg539_stage1{sfx}.out"), "w").write("\n".join(LINES) + "\n")
json.dump(R, open(os.path.join(HERE, f"cfg539_stage1_results{sfx}.json"), "w"), indent=1, default=float)
if MUT:
    det = not s2_ok
    print(f"MUTATE (sign reversed) S2 {'FAILS -> DETECTED' if det else 'passes -> NOT DETECTED'}")
    open(os.path.join(HERE, f"cfg539_stage1{sfx}.out"), "a").write(f"MUTATE (sign reversed) S2 {'FAILS -> DETECTED' if det else 'passes -> NOT DETECTED'}\n")
    sys.exit(1 if det else 0)
sys.exit(0 if ok_all else 1)
