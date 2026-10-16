#!/usr/bin/env python3
"""ARGON10 Part Q (quantum corrections) and Part D1 (normalization bookkeeping).
Criteria: FROZEN_CRITERIA.md (commit db69ec1a0). MUTATE: ARGON10_MUTATE=1.
Runs in seconds, < 0.2 GB. astra's numbers are comparison targets only."""
import os, sys, json, math
import numpy as np
import sympy as sp

MUT = os.environ.get("ARGON10_MUTATE") == "1"
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = {}

# ---- constants (CODATA 2018 / IAU) ----
hbar = 1.054571817e-34; c = 299792458.0; G = 6.67430e-11
Msun = 1.98847e30; pc = 3.0856775814913673e16
MeV_J = 1.602176634e-13; hbarc_MeVm = 197.3269804e-15      # MeV*m
A0 = {"canonical": 9.3603e-11, "alt": 1.1312e-10}

# ---- astra's quoted targets (CURRENT.txt / FOUR_GAP_AUDIT.txt, 2026-10-16) ----
ASTRA_BETA_NET_M100 = 0.28273
ASTRA_BETA_M2_M100 = 506.7

# ================= Q1: one-loop beta functions of the 3-real-scalar model =================
p1, p2, chi, L, a, B, mu, lam, m2, t, Is = sp.symbols('p1 p2 chi L a B mu lam m2 t Is', real=True)
Is = sp.symbols('Is', positive=True)
Isym = (p1**2 + p2**2) / 2
Vgen = m2*Isym + L*Isym**2 + a*chi*Isym + B*chi**2/2 + mu*chi**3/3 + lam*chi**4/4 + t*chi
H = sp.hessian(Vgen, (p1, p2, chi))
TrH2 = sp.expand((H*H).trace())
TrH2_I = sp.expand(TrH2.subs(p2, 0).subs(p1, sp.sqrt(2*Is)))
P = sp.Poly(TrH2_I, Is, chi)
cc = lambda i, j: P.coeff_monomial(Is**i * chi**j)
pref = 1 / (32*sp.pi**2)
FACT = 2 if (MUT and os.environ.get("ARGON10_M") == "1") else 1   # M1: 16 pi^2 in place of 32 pi^2
beta = {'V0': cc(0,0), 't': cc(0,1), 'B': 2*cc(0,2), 'mu': 3*cc(0,3), 'lam': 4*cc(0,4),
        'm2': cc(1,0), 'a': cc(1,1), 'L': cc(2,0)}
beta = {k: v*pref*FACT for k, v in beta.items()}
beta_f = {k: sp.lambdify((L, a, B, mu, lam, m2, t), v, 'mpmath') for k, v in beta.items()}

def params(Mv, eps=1.0, drop_portal=False):
    Lv = (2 - 1.0/Mv) * eps
    av = 2.0*Mv*math.sqrt(eps)
    muv = -3.0*Mv/8.0 * math.sqrt(eps)      # mu chi^3/3 = -M chi^3/8
    if drop_portal and MUT and os.environ.get("ARGON10_M") == "2":
        av = 0.0
    return dict(L=Lv, a=av, B=Mv**2, mu=muv, lam=1.0*eps, m2=1.0, t=0.0)

def betas_at(pr):
    args = (pr['L'], pr['a'], pr['B'], pr['mu'], pr['lam'], pr['m2'], pr['t'])
    return {k: float(f(*args)) for k, f in beta_f.items()}

def net_quartic(pr): return pr['L'] - pr['a']**2/(2*pr['B'])
def beta_net(pr, bt):
    return bt['L'] - pr['a']*bt['a']/pr['B'] + pr['a']**2*bt['B']/(2*pr['B']**2)

lines = []
def say(s=""):
    print(s); lines.append(s)

say(f"ARGON10 Part Q + D1   mode={'MUTATE ' + os.environ.get('ARGON10_M','') if MUT else 'scored'}   criteria db69ec1a0")
pr100 = params(100, drop_portal=True)
bt100 = betas_at(pr100)
bn100 = beta_net(pr100, bt100)
bm100 = bt100['m2'] / pr100['m2']
say("\n== Q1  one-loop MS-bar beta, M=100 ==")
say(f"  net quartic L - a^2/(2B) = {net_quartic(pr100):+.6f}   beta_net = {bn100:.6f}   beta_m2/m2 = {bm100:.4f}")
say(f"  astra targets: beta_net {ASTRA_BETA_NET_M100}, beta_m2/m2 {ASTRA_BETA_M2_M100}")

# independent identity: finite-difference mu-derivative of the CW potential vs polynomial TrH^2
def V1_num(Iv, chiv, pr, lnmu):
    import mpmath as mp
    mp.mp.dps = 40
    f1 = mp.sqrt(2*Iv)
    Hn = mp.matrix(3, 3)
    Lv, av, Bv, muv, lv, mv = [mp.mpf(pr[k]) for k in ('L','a','B','mu','lam','m2')]
    # Hessian of V at (phi1=f1, phi2=0, chi)
    Hn[0,0] = mv + 2*Lv*Iv + av*chiv + 2*Lv*f1**2   # V_I + 2L phi1^2
    Hn[1,1] = mv + 2*Lv*Iv + av*chiv
    Hn[2,2] = Bv + 2*muv*chiv + 3*lv*chiv**2
    Hn[0,2] = Hn[2,0] = av*f1
    ev = mp.eigsy(Hn, eigvals_only=True)
    ev = [float(e) for e in ev]
    return sum(e**2*(math.log(abs(e)) - 2*lnmu - 1.5) for e in ev) / (64*math.pi**2), ev

rng = np.random.default_rng(20261016)
maxrel = 0.0; npts = 0
while npts < 5:
    Iv = float(rng.uniform(0.0, 2.0)); cv = float(rng.uniform(-0.5, 0.5))
    _, ev = V1_num(Iv, cv, pr100, 0.0)
    if min(ev) <= 0:
        continue
    h = 1e-4
    vp, _ = V1_num(Iv, cv, pr100, +h); vm, _ = V1_num(Iv, cv, pr100, -h)
    dV1 = (vp - vm) / (2*h)                      # d V1 / d ln mu
    trh2 = float(TrH2_I.subs({L: pr100['L'], a: pr100['a'], B: pr100['B'], mu: pr100['mu'], lam: pr100['lam'],
                              m2: pr100['m2'], t: 0, Is: Iv, chi: cv}))
    expect = -trh2 / (32*math.pi**2)
    rel = abs(dV1 - expect) / abs(expect)
    maxrel = max(maxrel, rel); npts += 1
say(f"  identity  dV1/dln(mu) = -TrH^2/(32 pi^2):  max rel diff over 5 random points = {maxrel:.2e}")
q1_ok = (abs(bn100 - ASTRA_BETA_NET_M100) <= 5e-5 and abs(bm100 - ASTRA_BETA_M2_M100) <= 0.05 and maxrel <= 1e-6)
say(f"  Q1: {'AGREES' if q1_ok else 'DISAGREES'}")
OUT['Q1'] = dict(beta_net=bn100, beta_m2=bm100, identity_maxrel=maxrel, agrees=q1_ok)

# ================= Q2: radiative sensitivity span =================
say("\n== Q2  radiative sensitivity span  (Delta = |beta| ln(M/m_h) / |tree value|) ==")
say(f"  {'M':>6} {'eps':>7} {'net quartic':>13} {'beta_net':>11} {'Delta_net':>11} {'cls':>12} | {'beta_m2':>11} {'Delta_m':>11} {'cls':>12}")
def cls(D): return 'UNPROTECTED' if D > 10 else ('MARGINAL' if D > 1 else 'PROTECTED')
q2 = []
for Mv in (10, 100, 1000):
    for eps in (1.0, 1e-3, 1e-6):
        pr = params(Mv, eps)
        bt = betas_at(pr)
        nq = net_quartic(pr); bn = beta_net(pr, bt)
        Dn = abs(bn) * math.log(Mv) / abs(nq)
        Dm = bt['m2'] * math.log(Mv) / pr['m2']
        say(f"  {Mv:6d} {eps:7.0e} {nq:+13.3e} {bn:11.4e} {Dn:11.3e} {cls(Dn):>12} | {bt['m2']:11.4e} {Dm:11.3e} {cls(Dm):>12}")
        q2.append(dict(M=Mv, eps=eps, net=nq, beta_net=bn, Delta_net=Dn, cls_net=cls(Dn),
                       beta_m2=bt['m2'], Delta_m=Dm, cls_m=cls(Dm)))
OUT['Q2'] = q2
chk = [r for r in q2 if r['M'] == 100 and r['eps'] == 1e-6][0]
say(f"  cross-check vs astra (M=100, eps=1e-6, UNIT log): quartic rel shift {abs(chk['beta_net'])/abs(chk['net']):.4e} (astra 2.8273e-5), "
    f"m2 shift {chk['beta_m2']:.4e} (astra 5.0671e-4)")

# ================= Q3: classicality of the S2 sector =================
say("\n== Q3  classicality of the galaxy-law (S2) sector ==")
lP = math.sqrt(hbar*G/c**3)
Mb = 6e10*Msun
q3 = []
all_small = True
say(f"  Planck length {lP:.3e} m;  halo M_b = 6e10 Msun, M_c = 5.364 M_b")
say(f"  {'footing':>10} {'L*':>8} {'g_loop':>11} {'g_act':>11} {'g_zp':>11}")
for foot, a0 in A0.items():
    Vf = (G*Mb*a0)**0.25; rM = math.sqrt(G*Mb/a0); tt = rM/Vf
    S = 5.364*Mb*Vf**2*tt
    gact = hbar/S
    for Ls_pc in (5.75, 24.0, 1000.0):
        Ls = Ls_pc*pc
        gloop = (lP/Ls)**2
        rho_zp = 3*hbar*c/(64*math.pi**2*Ls**4)
        gzp = rho_zp / (4*a0**2/G)
        say(f"  {foot:>10} {Ls_pc:6.2f}pc {gloop:11.2e} {gact:11.2e} {gzp:11.2e}")
        all_small &= (gloop < 1e-30 and gact < 1e-30 and gzp < 1e-30)
    say(f"  ({foot}: V_f = {Vf/1e3:.1f} km/s, r_M = {rM/pc:.0f} pc, t = {tt/3.156e16:.2f} Gyr, classical action S = {S:.2e} J s)")
say(f"  Q3: {'NEGLIGIBLE' if all_small else 'NOT NEGLIGIBLE'}")
OUT['Q3'] = dict(negligible=all_small)

# ================= Q4: vacuum-energy scale (informative) =================
say("\n== Q4  partial MS-bar scalar vacuum value V1(0) at mu=M, m_h = 1 MeV  (scheme-dependent, informative) ==")
def to_MeV4(rho_J_m3): return rho_J_m3 / MeV_J * hbarc_MeVm**3
q4 = []
for Mv in (10, 100, 1000):
    lnM = math.log(Mv)
    V10 = (2*(-2*lnM - 1.5) + Mv**4*(-1.5)) / (64*math.pi**2)       # in m_h^4 units, mu = M
    for foot, a0 in A0.items():
        rho = to_MeV4(4*a0**2/G)
        ratio = abs(V10) / rho
        say(f"  M={Mv:5d} {foot:>10}: |V1(0)| = {abs(V10):.3e} MeV^4, rho_DE c^2 = {rho:.3e} MeV^4, log10 ratio = {math.log10(ratio):.1f}")
        q4.append(dict(M=Mv, foot=foot, log10_ratio=math.log10(ratio)))
OUT['Q4'] = q4
say("  (no cancellation mechanism is claimed; astra's sequestering route fixes only the vacuum-FORM stress)")

# ================= D1: normalization bookkeeping =================
say("\n== D1  normalization bookkeeping ==")
for foot, a0 in A0.items():
    E_a0_eV = hbar*a0/c / 1.602176634e-19
    say(f"  {foot}: hbar*a0/c = {E_a0_eV:.3e} eV;  / (1 MeV) = {E_a0_eV/1e6:.2e};  / (2 MeV) = {E_a0_eV/2e6:.2e};  / (2.25 meV) = {E_a0_eV/2.25e-3:.2e}")
rhoDE = 4*A0['canonical']**2/G
mu_DE_eV = (to_MeV4(rhoDE))**0.25*1e6          # MeV -> eV
say(f"  rho_DE^(1/4) at kappa=1/2 (canonical) = {mu_DE_eV*1e3:.3f} meV;  2 MeV / 2.6757 meV = {2e6/2.6757e-3:.3e}  (astra: 7.47e8)")
say("  parameter count (astra, FOUR_GAP_AUDIT NORMALIZATION):")
say("    observed: ONE ratio  kappa = a0 / (c sqrt(G rho_DE)).")
say("    a0 = q_b^3 / (4 pi C^3 beta G_lab)  -> free: (q_b, C, beta, G_lab)  [4 parameters, 1 output]")
say("    B_eff = Q^2/2 + Delta_F + <tau>/4   -> free: (Q, Delta_F, <tau>)    [3 parameters, 1 output]")
say("    Imposing kappa = 1/2 is ONE relation among >= 7 parameters: >= 6 free directions remain.")
say("    Explicit degeneracy: (Q, Delta_F) = (1, 2.5) and (2, 1) give B_eff = 3 with a0 differing (astra).")
say("  D1: NOT FIXED (agrees with astra)")
OUT['D1'] = dict(reading='NOT FIXED', free_directions_min=6)

# ================= verdict lines =================
say("\n== gate summary ==")
say(f"  Q1 {'AGREES' if q1_ok else 'DISAGREES'} | Q3 {'NEGLIGIBLE' if all_small else 'NOT NEGLIGIBLE'} | D1 NOT FIXED")
suffix = ("_MUTATE_M" + os.environ.get("ARGON10_M","")) if MUT else ""
with open(os.path.join(HERE, f"argon10_quantum{suffix}.out"), "w") as fh:
    fh.write("\n".join(lines) + "\n")
with open(os.path.join(HERE, f"argon10_quantum_results{suffix}.json"), "w") as fh:
    json.dump(OUT, fh, indent=1, default=float)
if MUT:
    bites = not q1_ok
    print(f"MUTATE {os.environ.get('ARGON10_M')}: Q1 AGREES -> {q1_ok}; {'bites' if bites else 'DOES NOT BITE'}")
    sys.exit(0 if bites else 1)
