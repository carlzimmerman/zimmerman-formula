#!/usr/bin/env python3
"""
K_AUDIT -- independent audit of the three load-bearing premises of the kappa=1/2 "derivation"
(deepseek PD01/PD08/PD10/PD22, G084). Reproduce-before-contradict: this recomputes each premise's
status from scratch and reports it BOTH ways -- credit what is real, bound what is not.

Verdict in one line: kappa is NOT a free fitted parameter (real advance) but it is NOT derived
from first principles either -- it is structurally two-valued {1/2, 1} via a channel-count
identification, with the selection to 1/2 fixed EMPIRICALLY (cp measured to 0.33%), because the
framework's own k01 theorem proves the last factor is underivable.

Run: python3 opus_48_extended_research/kappa_audit_2026/K_AUDIT_kappa_derivation_three_premises.py
Needs sympy. No data files.
"""
import sympy as sp

print("="*94)
print("K_AUDIT -- the three premises of kappa = 1/(2 cp), n=2  (PD01/PD08/PD10/PD22, G084)")
print("="*94)

# ---------------------------------------------------------------- PREMISE 1: two channels
print("\n[1] CHANNELS = 2  -- linearized GR for ds^2 = -(1+2Phi)dt^2 + (1-2Psi)dx^2  (static, radial)")
x, y, z = sp.symbols('x y z', real=True)
r = sp.sqrt(x**2+y**2+z**2)
F = sp.Function('Phi')(r)          # Phi(r)
G = sp.Function('Psi')(r)          # Psi(r)
eta = sp.diag(-1, 1, 1, 1)
h = sp.diag(-2*F, -2*G, -2*G, -2*G)          # perturbation h_{mu nu}
coords = [sp.Symbol('t', real=True), x, y, z]
def d(f, i):                                  # partial derivative (static: d/dt = 0)
    return 0 if i == 0 else sp.diff(f, coords[i])
lap = lambda f: sp.diff(f, x, 2)+sp.diff(f, y, 2)+sp.diff(f, z, 2)
htr = sum(eta[a, a]*h[a, a] for a in range(4))                 # h = eta^{mu nu} h_{mu nu} = 2Phi-6Psi
# linearized Ricci: R^(1)_{mu nu} = 1/2 ( d_rho d_mu h^rho_nu + d_rho d_nu h^rho_mu - box h_{mu nu} - d_mu d_nu h )
def hmix(rho, nu):                                             # h^rho_nu = eta^{rho a} h_{a nu} (diagonal)
    return eta[rho, rho]*h[rho, nu]
def Ric(mu, nu):
    t1 = sum(d(d(hmix(rho, nu), rho), mu) for rho in range(4))
    t2 = sum(d(d(hmix(rho, mu), rho), nu) for rho in range(4))
    box = -sum(eta[a, a]*0 for a in range(4)) + lap(h[mu, nu])  # static box = spatial Laplacian
    t3 = box
    t4 = d(d(htr, mu), nu)
    return sp.simplify(sp.Rational(1, 2)*(t1+t2-t3-t4))
R = sp.simplify(sum(eta[a, a]*Ric(a, a) for a in range(4)))    # Ricci scalar (diagonal)
G00 = sp.simplify(Ric(0, 0) - sp.Rational(1, 2)*eta[0, 0]*R)
Gkk = sp.simplify(sum(Ric(i, i) for i in range(1, 4)) - sp.Rational(1, 2)*3*R)  # delta^{ij}G_ij
res00 = sp.simplify(G00 - 2*lap(G))
reskk = sp.simplify(Gkk - 2*(lap(F) - lap(G)))
ok1 = (res00 == 0 and reskk == 0)
print(f"    G_00 - 2*lap(Psi)      = {res00}")
print(f"    G_kk - 2*lap(Phi-Psi)  = {reskk}")
print(f"    -> [{'CONFIRMED' if ok1 else 'MISMATCH'}] two independent Poisson channels: 00->Psi, trace->(Phi-Psi).")
print("    CAVEAT (the honest bound): for a perfect fluid / dust the anisotropic-stress eq forces")
print("    Phi = Psi (gamma_PPN = 1), so the two channels are dynamically DEGENERATE. 'Count 2' is")
print("    two PRESENTATIONS before that degeneracy -- a well-motivated IDENTIFICATION, not forced.")

# ---------------------------------------------------------------- PREMISE 2: degree-2 (G084)
print("\n[2] DEGREE-2 (G084)  -- is the exponent 2 forced, or does it need eta=1/2?")
C, sig2, gamma, rho, A = sp.symbols('C sigma2 gamma rho A', positive=True)
# max-entropy EL in the log well Phi = C ln r, with energy multiplier beta = 1/sigma^2:
#   rho(r) = A r^{-gamma},  gamma = beta*C = C/sigma^2
gamma_of = C/sig2
print(f"    max-entropy Euler-Lagrange gives  gamma = C/sigma^2 = {gamma_of}")
gamma_at_half = gamma_of.subs(sig2, C/2)
print(f"    at the virial input sigma^2 = C/2 (eta=1/2):  gamma = {sp.simplify(gamma_at_half)}")
print(f"    but gamma=2 requires sigma^2 = C/2 exactly; for sigma^2 = C/3 -> gamma = {sp.simplify(gamma_of.subs(sig2, C/3))}, etc.")
print("    -> [CONDITIONAL] 'degree 2' is NOT free-standing: it follows from eta=1/2 (sigma^2=C/2).")
print("    Using this '2' to derive kappa=1/2 borrows a 1/2 input -> possible circularity. Weakest leg.")

# ---------------------------------------------------------------- PREMISE 3: p'(0)=1
print("\n[3] p'(0) = cp = 1  -- forced, or measured?")
cp, Yv, s = sp.symbols('cp Y s', positive=True)
p = cp*Yv                                       # per-channel engagement, linear coeff cp
mu = 1 - (1 - p)**2                             # two-channel OR
slope = sp.simplify(sp.limit(sp.diff(mu, Yv), Yv, 0))
kappa = sp.simplify(1/slope)                    # kappa = a0/s = 1/mu'(0)
print(f"    two-channel OR: mu = 1-(1-cp*Y)^2 ;  mu'(0) = {slope} ;  kappa = a0/s = 1/mu'(0) = {kappa}")
print("    => kappa = 1/(2 cp).  cp is the k01 ZERO MODE: PD10 states plainly 'p'(0)=1 is NOT")
print("       derivable from the action alone -- the k01 theorem proves no action fixes it.'")
print("    It is MEASURED: SPARC deep slope n = 2.000 -> cp = 1 to 0.33% -> kappa = 1/2 +- 0.17%.")
print(f"    at cp=1: kappa = {sp.simplify(kappa.subs(cp,1))}  (measured, not derived)")

# ---------------------------------------------------------------- VERDICT
print("\n" + "="*94)
print("VERDICT (both ways):")
print("  REAL ADVANCE: kappa is no longer a free continuous fit -- the channel count makes it")
print("  structurally TWO-VALUED {1/2, 1} (premise 1 math confirmed), the 2pi form dies structurally,")
print("  and kappa=1/(2cp) with cp pinned to 0.33% (any deviation = a 2nd acceleration scale, excluded).")
print("  NOT FIRST-PRINCIPLES: (3) cp=1 is MEASURED because the framework's own k01 theorem proves it")
print("  underivable; (1) 'count 2' rests on the OR-identification (GR degenerates Phi=Psi for dust);")
print("  (2) 'degree 2' borrows eta=1/2. Two of three legs are conditional/empirical.")
print("  HONEST STATUS: kappa is structurally quantized to {1/2,1}; the selection to 1/2 is empirical")
print("  (cp measured to 0.33%). Neither 'fitted free parameter' nor 'derived' -- the truth is between,")
print("  and it matches what PD01/PD10 say when read past the commit headlines.")
assert ok1, "premise-1 GR computation did not reproduce -- investigate before trusting the verdict"
print("\nK_AUDIT COMPLETE: premise-1 GR reproduced; premises 2-3 shown conditional/measured.")
