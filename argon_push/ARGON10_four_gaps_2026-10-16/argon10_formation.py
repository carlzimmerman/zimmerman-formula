#!/usr/bin/env python3
"""ARGON10 Part F (formation).  Criteria: FROZEN_CRITERIA.md (commit db69ec1a0).
F1 reproduces astra's spinodal growth rates from my own rotating-frame fluctuation operator;
F2 estimates what the spinodal fragments / free quanta imply for the repo's self-interaction window (CFG725).
MUTATE: ARGON10_MUTATE=1 (M3: gyroscopic coupling set to zero)."""
import os, sys, json, math
import numpy as np
from scipy.optimize import brentq, minimize_scalar

MUT = os.environ.get("ARGON10_MUTATE") == "1"
HERE = os.path.dirname(os.path.abspath(__file__))
lines = []
def say(s=""):
    print(s); lines.append(s)

# astra's quoted targets (CURRENT.txt, FOUR_GAP_AUDIT.txt, MEDIATOR_COMPLETION_AND_VALIDITY.tex Table)
ASTRA = {"gamma": {0.1: (0.04369, 0.29), 0.5: (0.07436, 0.34)},
         "table": {1: (0.530967, 0.777373), 10: (4.351594, 0.774215), 100: (48.989310, 0.753423), 1000: (498.929051, 0.750358)}}
ISTAR_100 = 48.989310

def U(c, M):   return M**2*c**2/2 - M*c**3/8 + c**4/4
def Up(c, M):  return M**2*c - 3*M*c**2/8 + c**3
def Upp(c, M): return M**2 - 0.75*M*c + 3*c**2

def coexistence(M):
    """omega*^2 = min_{I,chi} V/I on chi=-x<0 ; returns (I*, omega*^2, x*)."""
    L = 2 - 1.0/M
    R = lambda x: 1 - 2*M*x + 2*math.sqrt(L*U(-x, M))
    r = minimize_scalar(R, bounds=(1e-6, 3*M), method='bounded', options={'xatol': 1e-12})
    x = r.x
    return math.sqrt(U(-x, M)/L), r.fun, x

def background(M, I0):
    L = 2 - 1.0/M; a = 2.0*M
    chi0 = brentq(lambda c: Up(c, M) + a*I0, -5*M, 5*M)
    om2 = 1 + 2*L*I0 + a*chi0
    return L, a, chi0, om2

def growth(M, I0, ks, gyro=True):
    L, a, chi0, om2 = background(M, I0)
    om = math.sqrt(om2)
    Bh = Upp(chi0, M); A = 4*L*I0; h = a*math.sqrt(2*I0)
    best = np.empty(len(ks))
    for n, k in enumerate(ks):
        k2 = k*k
        W = np.zeros((3, 3))
        W[0, 0] = A + k2; W[1, 1] = k2; W[2, 2] = Bh + k2; W[0, 2] = W[2, 0] = h
        Gs = np.zeros((3, 3))
        if gyro:
            Gs[0, 1] = -2*om; Gs[1, 0] = 2*om     # Gm - Gm^T with Gm=[[0,-om],[om,0]]
        Ac = np.block([[np.zeros((3, 3)), np.eye(3)], [-W, -Gs]])
        best[n] = np.linalg.eigvals(Ac).real.max()
    return best, dict(L=L, a=a, chi0=chi0, om2=om2, om=om, Bh=Bh, A=A, h=h)

say(f"ARGON10 Part F   mode={'MUTATE M3 (gyroscopic coupling off)' if MUT else 'scored'}   criteria db69ec1a0")

# ---------- extra (not frozen): coexistence table reproduction ----------
say("\n== extra (not frozen)  coexistence phase I*, omega*^2 vs astra's table ==")
tab_ok = True
for M in (1, 10, 100, 1000):
    Is_, w2, x = coexistence(M)
    aI, aw = ASTRA["table"][M]
    say(f"  M={M:5d}: I* = {Is_:.6f} (astra {aI:.6f}),  omega*^2 = {w2:.6f} (astra {aw:.6f})")
    tab_ok &= (abs(Is_-aI)/aI < 1e-5 and abs(w2-aw) < 1e-5)
say(f"  table reproduction: {'AGREES' if tab_ok else 'DISAGREES'}")

# ---------- F1 ----------
say("\n== F1  spinodal growth, rotating-frame fluctuations (r,pi,xi), M=100 ==")
M = 100
Istar, w2star, _ = coexistence(M)
ks = np.arange(0.0, 2.0001, 0.005)
f1 = {}
f1_ok = True
for s in (0.1, 0.5, 1.0, 2.0):
    g, par = growth(M, s*Istar, ks, gyro=not MUT)
    i = int(g.argmax())
    f1[s] = dict(gmax=float(g[i]), k=float(ks[i]), om2=par['om2'], chi0=par['chi0'])
    tgt = ASTRA["gamma"].get(s)
    if tgt:
        ok = abs(g[i]-tgt[0]) <= 2e-4 and abs(ks[i]-tgt[1]) <= 0.02
        f1_ok &= ok
        say(f"  s={s:3.1f}: gamma_max = {g[i]:.5f} at k = {ks[i]:.3f}   (astra {tgt[0]:.5f} at {tgt[1]:.2f})  {'ok' if ok else 'MISS'}")
    else:
        ok = g.max() <= 1e-8
        f1_ok &= ok
        say(f"  s={s:3.1f}: max growth over k in [0,2] = {g.max():.2e}  (expect stable)  {'ok' if ok else 'MISS'}   omega^2={par['om2']:.5f}")
say(f"  F1: {'AGREES' if f1_ok else 'DISAGREES'}")
M10 = {}
Is10, _, _ = coexistence(10)
for s in (0.1, 0.5, 1.0, 2.0):
    g, _p = growth(10, s*Is10, ks, gyro=not MUT)
    i = int(g.argmax()); M10[s] = (float(g[i]), float(ks[i]))
say("  info M=10: " + "; ".join(f"s={s}: {v[0]:.5f}@{v[1]:.3f}" for s, v in M10.items()))

if MUT:
    base, _ = growth(M, 0.1*Istar, ks, gyro=True)
    mut, _ = growth(M, 0.1*Istar, ks, gyro=False)
    rel = abs(mut.max()-base.max())/base.max()
    bites = rel > 0.10
    say(f"\nMUTATE M3: s=0.1 gamma_max {base.max():.5f} -> {mut.max():.5f} (change {rel*100:.0f}%); {'bites' if bites else 'DOES NOT BITE'}")
    with open(os.path.join(HERE, "argon10_formation_MUTATE_M3.out"), "w") as fh:
        fh.write("\n".join(lines) + "\n")
    sys.exit(0 if bites else 1)

# ---------- F2 ----------
say("\n== F2  self-interaction consequences (ESTIMATE; CFG725 window) ==")
hbarc = 197.3269804e-15        # MeV m
MeV_kg = 1.78266192e-30
def nat_to_cm2g(S, mh_MeV=1.0):
    """S = (sigma/m) in units of m_h^-3 -> cm^2/g for m_h in MeV."""
    sm = S / mh_MeV**3 * hbarc**2 / MeV_kg      # m^2/kg
    return sm * 10.0                             # 1 m^2/kg = 10 cm^2/g
def cls(x):
    return 'BELOW' if x < 0.105 else ('LOW-EDGE' if x < 0.82 else ('ABOVE-LOW' if x <= 10 else 'EXCLUDED'))
def mh_range(S):
    c1 = nat_to_cm2g(S, 1.0)
    lo = (c1/10.0)**(1/3); hi = (c1/0.105)**(1/3)          # MeV
    return lo, hi

res = {}
Lb = 2 - 1.0/M; ab = 2.0*M; Bb = float(M)**2
say("  gas channel (tree, threshold)  M=100:")
say(f"  {'eps':>7} {'channel':>10} {'|amp|':>10} {'S=(sig/m)m_h^3':>15} {'cm2/g @1MeV':>12} {'class':>10}   m_h range for [0.105,10] cm2/g")
gas = []
for eps in (1.0, 1e-3, 1e-6):
    Le = eps*Lb; a2 = eps*ab**2
    for name, amp, fac in (("same-chg", -4*Le + 2*a2/Bb, 128*math.pi), ("opp-chg", -4*Le + a2/(Bb-4) + a2/Bb, 64*math.pi)):
        S = amp**2/fac
        v = nat_to_cm2g(S); lo, hi = mh_range(S)
        say(f"  {eps:7.0e} {name:>10} {abs(amp):10.3e} {S:15.3e} {v:12.3e} {cls(v):>10}   {lo*1e3:.3g} keV - {hi*1e3:.3g} keV")
        gas.append(dict(eps=eps, ch=name, amp=amp, S=S, cm2g_1MeV=v, cls=cls(v), mh_keV=(lo*1e3, hi*1e3)))
res['gas'] = gas

say("\n  lump channel (spinodal fragments), M=100; lambda_f = 2 pi / k_s; bracket x[0.5, 2] in lambda_f:")
say(f"  {'s':>4} {'eps':>7} {'lambda_f':>9} {'Q_f':>10} {'R_f':>8} {'S=(sig/m)m_h^3':>15} {'cm2/g @1MeV':>12} {'class':>10} {'bracket cm2/g':>20}   m_h range")
nstar = 2*math.sqrt(w2star)*Istar
lump = []
for s in (0.1, 0.5):
    ks_ = f1[s]['k']; lam = 2*math.pi/ks_
    n0 = 2*math.sqrt(f1[s]['om2'])*s*Istar
    for eps in (1.0, 1e-3, 1e-6):
        def lumpS(lam_):
            Qf = n0*lam_**3/eps
            Rf = (3*Qf/(4*math.pi*nstar/eps))**(1/3)
            return Qf, Rf, 4*math.pi*Rf**2/Qf
        Qf, Rf, S = lumpS(lam)
        v = nat_to_cm2g(S)
        vb = (nat_to_cm2g(lumpS(2*lam)[2]), nat_to_cm2g(lumpS(0.5*lam)[2]))
        lo, hi = mh_range(S)
        say(f"  {s:4.1f} {eps:7.0e} {lam:9.2f} {Qf:10.3e} {Rf:8.2f} {S:15.3e} {v:12.3e} {cls(v):>10} {vb[0]:9.2e}-{vb[1]:.2e}   {lo*1e3:.3g} keV - {hi*1e3:.3g} keV")
        lump.append(dict(s=s, eps=eps, lam=lam, Q=Qf, R=Rf, S=S, cm2g_1MeV=v, cls=cls(v), bracket=vb, mh_keV=(lo*1e3, hi*1e3)))
res['lump'] = lump
say("  note: sigma/m ~ eps for lumps (charge ~ 1/eps at fixed size) but ~ eps^2 for free quanta (amplitude ~ eps).")
say("  ESTIMATE only: linear spinodal scale, hard-sphere cross-section; no nonlinear formation, merging or fragment-size evolution.")

# ---------- F3: POST-HOC (NOT frozen; written after F1/F2/Q2 results were seen) ----------
say("\n== F3  POST-HOC joint map (NOT frozen): quantum-protected eps vs lump self-interaction window ==")
say("  protected: Delta_net <= 1 and Delta_m <= 1 (Q2, both scale as eps);  window: lump sigma/m in [0.105, 10] cm2/g (CFG725 bracket);")
say("  s=0.1 fragments, lambda_f = 2pi/k_s.  m_h is a free scale, so this is a RELATION between eps and m_h, not a constraint on eps alone.")
qj = json.load(open(os.path.join(HERE, "argon10_quantum_results.json")))['Q2']
def q2(Mv, key): return [r for r in qj if r['M'] == Mv and r['eps'] == 1.0][0][key]
f3 = []
say(f"  {'M':>5} {'eps_max':>9} {'k_s':>6} {'lump cm2/g@1MeV, eps=1':>24}  m_h window at eps_max (MeV)")
for Mv in (10, 100, 1000):
    Is_, w2s, _ = coexistence(Mv)
    g_, par_ = growth(Mv, 0.1*Is_, ks)
    ksp = float(ks[int(g_.argmax())]); lam = 2*math.pi/ksp
    n0 = 2*math.sqrt(par_['om2'])*0.1*Is_; nst = 2*math.sqrt(w2s)*Is_
    Qf = n0*lam**3; Rf = (3*Qf/(4*math.pi*nst))**(1/3); S1 = 4*math.pi*Rf**2/Qf
    cg1 = nat_to_cm2g(S1)
    epsmax = min(1/q2(Mv, 'Delta_net'), 1/q2(Mv, 'Delta_m'), 1.0)
    sm = cg1*epsmax
    lo, hi = (sm/10)**(1/3), (sm/0.105)**(1/3)
    say(f"  {Mv:5d} {epsmax:9.2e} {ksp:6.3f} {cg1:24.3e}  {lo:.3g} - {hi:.3g}")
    f3.append(dict(M=Mv, eps_max=epsmax, k_s=ksp, cm2g_eps1=cg1, mh_MeV=(lo, hi)))
res['F3_posthoc'] = f3
say("  reading: at the protection limit the fragments sit in the window only for m_h below the upper value; larger m_h needs larger eps (unprotected).")

with open(os.path.join(HERE, "argon10_formation.out"), "w") as fh:
    fh.write("\n".join(lines) + "\n")
with open(os.path.join(HERE, "argon10_formation_results.json"), "w") as fh:
    json.dump(dict(F1=f1, F1_agrees=f1_ok, table_agrees=tab_ok, F2=res, M10=M10), fh, indent=1, default=float)
say("\n== gate summary ==")
say(f"  F1 {'AGREES' if f1_ok else 'DISAGREES'}  (extra table {'AGREES' if tab_ok else 'DISAGREES'})")
