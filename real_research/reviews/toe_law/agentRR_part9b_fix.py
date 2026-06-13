"""
agentRR Part 9b -- FIX the retarded-pole convention (Part 9's passive ref failed: passive gave UHP,
impossible). The retarded propagator must be analytic in the UPPER half w-plane; passive => poles in
LHP. Pin the convention so a PASSIVE damped oscillator has LHP poles, THEN test the active line.

Retarded oscillator GF (standard): chi_R(w) = 1/(wr^2 - w^2 - i*gamma*w), poles at
    w = -i gamma/2 +/- sqrt(wr^2 - gamma^2/4),  Im(w) = -gamma/2 < 0  => LHP. GOOD (this is the
right retarded sign: -i gamma w with gamma>0). Self-energy from coupling to this line:
    Sigma_R(w) = R * wr^2 * chi_R(w) = R wr^2/(wr^2 - w^2 - i gamma w).
Full retarded D(w) = w^2 - wk^2 - Sigma_R(w). The KHRONON pole = root of D. For the BARE oscillator
(R=0) D=w^2-wk^2 -> poles on real axis (undamped khronon) -- marginal. The damping enters only via
Sigma. So we must add the khronon's OWN intrinsic damping kappa_chi (the cold loss) to have a
baseline-stable propagator: D(w)= w^2 - wk^2 + i*kappa_chi*w - Sigma_R(w) (retarded, kappa_chi>0).
Without it the bare khronon is marginal and ANY Re-shift looks unstable. Pin kappa_chi>0 baseline.
"""
import numpy as np

def poles_full(wk2, R, wr, gamma, kap):
    # D(w) = w^2 - wk2 + i kap w - R wr^2/(wr^2 - w^2 - i gamma w) = 0
    # multiply by (wr^2 - w^2 - i gamma w):
    # (w^2 - wk2 + i kap w)(wr^2 - w^2 - i gamma w) - R wr^2 = 0
    # let P = w^2 - wk2 + i kap w ; Q = -w^2 - i gamma w + wr^2
    # P*Q = (w^2)(-w^2) + ... expand fully as quartic
    # Coeffts (descending w^4..w^0):
    # P = w^2 + i kap w - wk2 ; Q = -w^2 - i gamma w + wr^2
    # P*Q:
    # w^4: (1)(-1) = -1
    # w^3: (1)(-i gamma) + (i kap)(-1) = -i gamma - i kap = -i(gamma+kap)
    # w^2: (1)(wr^2) + (i kap)(-i gamma) + (-wk2)(-1) = wr^2 + kap*gamma + wk2
    # w^1: (i kap)(wr^2) + (-wk2)(-i gamma) = i(kap wr^2 + gamma wk2)
    # w^0: (-wk2)(wr^2) = -wk2 wr^2
    a4=-1.0
    a3=-1j*(gamma+kap)
    a2=(wr**2 + kap*gamma + wk2)
    a1=1j*(kap*wr**2 + gamma*wk2)
    a0=(-wk2*wr**2 - R*wr**2)
    return np.roots([a4,a3,a2,a1,a0])

wr, gamma = 0.6, 0.1
kap = 0.05  # khronon intrinsic loss (baseline stabilizer); will vary

# Step 0: convention check -- bare retarded oscillator chi_R poles must be LHP
w_osc = np.roots([-1.0, -1j*gamma, wr**2])  # -w^2 - i gamma w + wr^2 =0
print("bare retarded oscillator poles (must be LHP):", [f"{w:.4f}" for w in w_osc])

# Step 1: PASSIVE R>0 with baseline kappa -- must stay LHP
print("\n=== PASSIVE R>0 (must be all-LHP) ===")
worst=-1e9
for R in [0.001,0.01,0.1,0.5,1.0]:
    for wk2 in np.linspace(0,1.5,300):
        worst=max(worst,max(p.imag for p in poles_full(wk2,R,wr,gamma,kap)))
print(f"  max Im(pole) passive: {worst:+.6f}  (<=0 => convention now correct)")

# Step 2: ACTIVE R<0 -- threshold vs baseline kappa
print("\n=== ACTIVE R<0 -- UHP threshold vs khronon loss kappa ===")
for kapv in [0.01,0.05,0.1,0.2]:
    # find R_inst
    def maxim(R):
        w=-1e9
        for wk2 in np.linspace(0,1.5,300):
            w=max(w,max(p.imag for p in poles_full(wk2,R,wr,gamma,kapv)))
        return w
    # bracket
    lo,hi=0.0,-2.0
    if maxim(hi)<0:
        print(f"  kappa={kapv}: even R=-2 stays LHP (no instability up to |R|=2)"); continue
    for _ in range(50):
        mid=(lo+hi)/2
        if maxim(mid)>0: hi=mid
        else: lo=mid
    print(f"  kappa={kapv}: R_inst ~ {(lo+hi)/2:.4f}  (|R|>|R_inst| => UHP runaway)")

print("\nfold needs |R|=y~1.0-1.3 (Parts 7,8). Compare to R_inst above to see if a clamp/loss level")
print("exists that keeps the FOLD-strength response stable.")
