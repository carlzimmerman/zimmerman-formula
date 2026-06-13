"""
agentRR Part 9d -- resolve the stability question correctly. Part 9c's 'passive UHP' at lam2=0.2,
wk2=0 is a TACHYON: positive coupling repels the two levels; the lower one's omega^2 goes negative
when lam2 > wk2*wr^2 (DC level crossing). That is a static (k=0) instability, not a dynamical gain
runaway. The fold lives at FINITE k where omega^2>0. So the right stability question is:
  at the OPERATING-POINT fold (finite k, omega^2(k)>0 everywhere = Part 7's bounded branch), are the
  retarded poles in the LHP?
We test stability the clean way: for the spatial fold dispersion (Part 7 in-window point), the
operating-point branch has omega^2(k)>0 for all k (no tachyon, verified). With the khronon's own loss
kappa_chi>0 and a NEGATIVE-residue (active) but POSITIVE-gamma line (QQ Route2: active != anti-damped),
do poles stay LHP?  Sweep coupling sign and magnitude with a baseline kappa_chi and report the regime.

KEY DISTINCTION (QQ Route2, must respect):
  - active = spectral weight SIGN negative (Im chi<0 in band) = breaks passivity. Source of the fold.
  - anti-damped = pole in UHP = runaway.
  These are DIFFERENT. A negative-RESIDUE, positive-gamma Lorentzian is active (Im<0) AND LHP-stable.
We test exactly that object.
"""
import numpy as np

wr,gamma=0.6,0.1

# Object: chi_line(w) = -B * 2*wr*gamma / (wr^2 - w^2 - i gamma w)  (negative residue B>0 = active),
# but to keep poles fixed in LHP the DENOMINATOR keeps +(-i gamma w) retarded form (gamma>0).
# Dressed khronon WITH its own loss kappa: D(w)= w^2 - wk2 + i*kappa*w - chi_line(w).
def poles(wk2,B,wr,gamma,kappa,active=True):
    s = -1.0 if active else +1.0   # active => negative residue
    lam = s*B
    # chi_line = lam/(wr^2 - w^2 - i gamma w)
    # D(w)*(wr^2-w^2-i gamma w)=0:
    # (w^2 - wk2 + i kappa w)(wr^2 - w^2 - i gamma w) - lam = 0
    a4=-1.0
    a3=-1j*(gamma+kappa)
    a2=(wr**2 + kappa*gamma + wk2)
    a1=1j*(kappa*wr**2 + gamma*wk2)
    a0=(-wk2*wr**2 - lam)
    return np.roots([a4,a3,a2,a1,a0])

# sanity: small coupling, both signs, finite wk2 away from level crossing -> LHP
print("=== small coupling B=0.01, kappa=0.05, wk2 swept (away from DC tachyon) ===")
for active in (False,True):
    worst=-1e9
    for wk2 in np.linspace(0.3,1.5,300):  # finite k, above any DC tachyon
        worst=max(worst,max(p.imag for p in poles(wk2,0.01,wr,gamma,0.05,active)))
    print(f"  active={active}: max Im(pole)={worst:+.6f}")

# Now: the ACTIVE negative-residue line at FOLD strength. The fold needed the dispersive Re part
# B ~ y ~ 1.0-1.3 (the sigma4/sigma6). Sweep B up with finite k and a baseline loss kappa; find when
# the active line drives a pole UHP, and whether ANY kappa keeps fold-strength stable.
print("\n=== ACTIVE line, fold-strength B, vs khronon loss kappa (finite k band) ===")
for kappa in [0.05,0.2,0.5,1.0]:
    rows=[]
    for B in [0.05,0.1,0.3,0.6,1.0,1.3]:
        worst=-1e9
        for wk2 in np.linspace(0.2,1.5,300):
            worst=max(worst,max(p.imag for p in poles(wk2,B,wr,gamma,kappa,active=True)))
        rows.append((B,worst))
    desc=" ".join(f"B={b}:Im={w:+.3f}" for b,w in rows)
    print(f"  kappa={kappa}: {desc}")

print("\nINTERPRETATION: if even large khronon loss kappa cannot keep the fold-strength active line in")
print("the LHP, then a SIMPLE (Markovian) saturated/clamped gain does NOT stabilize the fold -- the")
print("clamp bounds amplitude but the linearized retarded pole is UHP => the fold band is convectively")
print("unstable. Delivery then needs a NON-MARKOVIAN/structured gain (KK partner shaped to hold LHP),")
print("which is EXTRA structure beyond plain saturation -- a free model input, not forced by the pump.")
