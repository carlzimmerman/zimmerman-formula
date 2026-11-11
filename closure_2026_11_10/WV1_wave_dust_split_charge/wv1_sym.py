#!/usr/bin/env python3
"""WV1 symbolic part (sympy, exact): S0 static reduction, S1b Noether charges, V1's linear dispersion, the V1 psi
equation's 1/|psi|^2 term, KA1 (X14 C5 dispersion), KA2 (QX17 static law), KA6 (LFS1 / COL1 charge), MUTATE M1.

Criteria: FROZEN_CRITERIA.md (committed alone before this script). NR Lagrangian of section 1 there, written in Psi's
mass density rho = m|psi|^2 and phase theta, nu = hbar/m:

  L = -rho nu theta_t - rho nu^2 |grad theta|^2/2 - nu^2 |grad sqrt rho|^2/2 - rho Phi - |grad Phi|^2/(8 pi G)
      - rho_b Phi + P.A - W(K|P|) - gamma F(div P)
  V1: A = grad(Phi + nu theta_t + nu^2 |grad theta|^2/2)        (frame = phase of Psi)
  V2: A = grad(Phi - chi_t + |grad chi|^2/2)                     (separate frame chi; Psi does not see it)

Run:  python3 wv1_sym.py               -> wv1_sym.out, wv1_sym.json   (exit 0 iff every check passes)
      WV1_MUTATE=M1 python3 wv1_sym.py -> wv1_sym_MUTATE_M1.out/.json (exit 0 iff the twin bites)
Adopts nothing. kappa = 1/2 FITTED; not theory closed.
"""
import os, sys, json, time
import sympy as sp
from sympy.calculus.euler import euler_equations

T0 = time.time()
HERE = os.path.dirname(os.path.abspath(__file__))
ARM = os.environ.get("WV1_MUTATE", "").strip()
if ARM not in ("", "M1"):
    sys.exit("WV1_MUTATE must be '' or M1")
STEM = "wv1_sym" if not ARM else f"wv1_sym_MUTATE_{ARM}"
LINES, RES, OK = [], {"arm": ARM or "none", "checks": {}}, True


def P_(s=""):
    LINES.append(s); print(s, flush=True)


def check(name, ok, msg):
    global OK
    RES["checks"][name] = {"ok": bool(ok), "msg": msg}
    OK = OK and bool(ok)
    P_(f"[{'PASS' if ok else 'FAIL'}] {name}: {msg}")


P_("WV1 symbolic part. TEST lane; adopts nothing. kappa = 1/2 FITTED; not theory closed.")
P_(f"arm: {ARM or 'none (main run)'}")
P_("")

t, x, y, z = sp.symbols("t x y z", real=True)
X = (x, y, z)
nu, Gn, a0, gam, mu = sp.symbols("nu G a0 gamma mu", positive=True)
K = 4 * sp.pi * Gn
rho = sp.Function("rho")(t, x, y, z)
th = sp.Function("theta")(t, x, y, z)
chi = sp.Function("chi")(t, x, y, z)
Phi = sp.Function("Phi")(t, x, y, z)
rhob = sp.Function("rho_b")(x, y, z)
P = [sp.Function(f"P{i}")(t, x, y, z) for i in (1, 2, 3)]
w1, w2, c6 = sp.symbols("w1 w2 c6", real=True)
Wf = lambda s: w1 * s + w2 * s ** 2          # stand-in for W(K|P|) as a function of |P|^2 (structure check only; the
                                              # exact W enters KA2 below); its form does not enter the charge identities
Ff = lambda s: s ** 2 / 2 + c6 * s ** 6       # stand-in for the adopted blend F(Pi) (raw part + a Pi^6 term)
Fprime = lambda s: s + 6 * c6 * s ** 5


def grad(f): return [sp.diff(f, c) for c in X]
def div(V): return sum(sp.diff(V[i], X[i]) for i in range(3))
def dot(U, V): return sum(U[i] * V[i] for i in range(3))


divP = div(P)
P2 = dot(P, P)


def L_psi(rho_, th_):
    return (-rho_ * nu * sp.diff(th_, t) - rho_ * nu ** 2 * dot(grad(th_), grad(th_)) / 2
            - nu ** 2 * dot(grad(sp.sqrt(rho_)), grad(sp.sqrt(rho_))) / 2)


L_grav = -rho * Phi - dot(grad(Phi), grad(Phi)) / (8 * sp.pi * Gn) - rhob * Phi
L_Pcore = -Wf(P2) - gam * Ff(divP)

if ARM == "M1":     # frame decoupled from Psi's phase: A = grad Phi only
    H_V1 = Phi
else:
    H_V1 = Phi + nu * sp.diff(th, t) + nu ** 2 * dot(grad(th), grad(th)) / 2
A_V1 = grad(H_V1)
L_V1 = L_psi(rho, th) + L_grav + dot(P, A_V1) + L_Pcore

P_("=== S1b (V1): Noether current of theta (the frame's shift symmetry) ===")
eqs = euler_equations(L_V1, [rho, th, Phi] + P, [t, x, y, z])
E_rho, E_th, E_Phi = [e.lhs for e in eqs[:3]]
E_P = [e.lhs for e in eqs[3:]]
C = rho + divP
v = [nu * g for g in grad(th)]
cont = nu * (sp.diff(C, t) + div([C * vi for vi in v]))
r1 = sp.simplify(sp.expand(E_th + cont))
r1b = sp.simplify(sp.expand(E_th - cont))
okC = (r1 == 0) or (r1b == 0)
sgn = "-" if r1 == 0 else ("+" if r1b == 0 else "?")
check("S1b_V1_charge", okC,
      f"EL(theta) = {sgn}nu [d_t C + div(C v)] with C = rho + div P, v = nu grad theta: residual "
      f"{'0' if okC else str(sp.simplify(E_th + cont))[:200]}  (the law's phantom density is part of Psi's U(1) charge)")
RES["S1b_V1"] = {"charge": "C = m|psi|^2 + div P", "flux": "C v", "exact": bool(okC)}
cont_plain = nu * (sp.diff(rho, t) + div([rho * vi for vi in v]))
rplain = sp.simplify(sp.expand(E_th + cont_plain))
P_(f"   (for comparison) EL(theta) + nu[d_t rho + div(rho v)] = {'0' if rplain == 0 else 'nonzero'}")

# Bernoulli unchanged by the P sector (P sector does not depend on rho)
L_V1_noP = L_psi(rho, th) + L_grav
E_rho_noP = euler_equations(L_V1_noP, [rho, th, Phi], [t, x, y, z])[0].lhs
rB = sp.simplify(E_rho - E_rho_noP)
check("S1b_V1_bernoulli", rB == 0,
      f"EL(rho) with the P sector minus without: {rB}  (Psi's flow obeys plain Madelung-Euler in the total Phi; "
      "so the frame's proper acceleration is A = -grad Q_qu)")

if ARM == "M1":
    RES["bites"] = not okC
    P_("")
    P_(f"MUTATE M1 (frame decoupled from Psi's phase): S1b_V1_charge {'FAILS -> BITES' if not okC else 'still passes -> DOES NOT BITE'}")
    P_(f"   EL(theta) + nu[d_t rho + div(rho v)] = {rplain}  (the charge is m|psi|^2 alone)")
    RES["runtime_s"] = round(time.time() - T0, 1)
    open(os.path.join(HERE, STEM + ".out"), "w").write("\n".join(LINES) + "\nkappa = 1/2 FITTED; not theory closed. Adopts nothing.\n")
    json.dump(RES, open(os.path.join(HERE, STEM + ".json"), "w"), indent=1, default=str)
    sys.exit(0 if RES["bites"] else 2)

# Poisson
rP = sp.simplify(E_Phi - (sp.diff(Phi, x, 2) + sp.diff(Phi, y, 2) + sp.diff(Phi, z, 2)) / (4 * sp.pi * Gn)
                 + rho + rhob + divP)
rP2 = sp.simplify(E_Phi + (sp.diff(Phi, x, 2) + sp.diff(Phi, y, 2) + sp.diff(Phi, z, 2)) / (4 * sp.pi * Gn)
                  - rho - rhob - divP)
check("S0_poisson", rP == 0 or rP2 == 0,
      "EL(Phi): lap Phi = 4 pi G (rho_b + m|psi|^2 + div P): residual 0 (Psi's dust IS in the source)")

# P equation: A - dW/dP + gamma grad F'(div P) = 0
okPe = True
for i in range(3):
    e = sp.expand(E_P[i])
    target = sp.expand(A_V1[i] + sp.diff(-Wf(P2), P[i]) + gam * sp.diff(Fprime(divP), X[i]))
    d1 = sp.simplify(e - target); d2 = sp.simplify(e + target)
    okPe = okPe and (d1 == 0 or d2 == 0)
check("S0_P_equation", okPe,
      "EL(P_i) = A_i - dW/dP_i + gamma d_i F'(div P): (A)'s leaf equation E2 at weak field with Pi_+ -> F'(Pi) "
      "(the P sector is (A)'s verbatim)")

P_("")
P_("=== S0 (V1): static galaxy, Psi stationary psi = f(x) e^{-i e t/nu} ===")
e_ = sp.symbols("e", real=True)
f = sp.Function("f")(x, y, z)
Phis = sp.Function("Phi")(x, y, z)
Ps = [sp.Function(f"P{i}")(x, y, z) for i in (1, 2, 3)]
subs_static = {th: -e_ * t / nu, rho: f ** 2, Phi: Phis}
for i in range(3):
    subs_static[P[i]] = Ps[i]
Eth_s = sp.simplify(E_th.subs(subs_static).doit())
check("S0_V1_phase_identity", Eth_s == 0, f"EL(theta) in the stationary state = {Eth_s} (satisfied identically)")
Erho_s = sp.simplify((E_rho.subs(subs_static).doit()) * f)
lapf = sum(sp.diff(f, c, 2) for c in X)
schr = -(nu ** 2 / 2) * lapf + Phis * f - e_ * f
rS = sp.simplify(Erho_s + schr); rS2 = sp.simplify(Erho_s - schr)
check("S0_V1_schrodinger", rS == 0 or rS2 == 0,
      "f * EL(rho) = +-[-(nu^2/2) lap f + Phi f - e f]: the stationary Schrodinger equation in the total Phi")
A_s = [sp.simplify(a.subs(subs_static).doit()) for a in A_V1]
okA = all(sp.simplify(A_s[i] - sp.diff(Phis, X[i])) == 0 for i in range(3))
check("S0_V1_frame_static", okA, "A = grad Phi in the stationary state (frame static, the law's input)")

P_("")
P_("=== S0 / KA2: the law, spherical static, gamma = 0, W = (a0^2/K)[-p/a0 - ln(1 - p/a0)], p = K|P| ===")
r = sp.symbols("r", positive=True)
Phir = sp.Function("Phi")(r)
fr = sp.Function("f")(r)
rbr = sp.Function("rho_b")(r)
g = sp.symbols("g", positive=True)                  # |dPhi/dr| > 0
pK = sp.symbols("p", positive=True)                 # p = K|P|
W = (a0 ** 2 / K) * (-pK / a0 - sp.log(1 - pK / a0))
# radial P equation at gamma = 0: g = dW/d|P| = K W'(p)
eqP = sp.Eq(g, sp.diff(W, pK) * K)
psol = sp.solve(eqP, pK)
psol = [s for s in psol if sp.simplify(s - a0 * g / (a0 + g)) == 0]
check("KA2_constitutive", len(psol) == 1, f"K|P| = a0 x/(1+x), x = g/a0 (QX17 E2 Legendre map): {psol}")
mu_x = (g / a0) / (1 + g / a0)
Pr = (a0 * Phir.diff(r) / (a0 + Phir.diff(r))) / K          # K P_r = (1 - mu) Phi'
lap = lambda F_: sp.diff(r ** 2 * F_, r) / r ** 2
pois_res = sp.simplify(lap(Phir.diff(r)) - 4 * sp.pi * Gn * (rbr + fr ** 2) - K * lap(Pr)
                       - (lap(mu_x.subs(g, Phir.diff(r)) * Phir.diff(r)) - 4 * sp.pi * Gn * (rbr + fr ** 2)))
check("S0_law", pois_res == 0,
      "Poisson + P equation  <=>  div[mu(|grad Phi|/a0) grad Phi] = 4 pi G (rho_b + m f^2), mu = x/(1+x): residual "
      f"{pois_res} (exact; (A)'s static row at mu_K = 0 with rho_b -> rho_b + m|psi|^2)")

P_("")
P_("=== S1b (V2) and KA6: the separate frame's charge ===")
Hs = sp.symbols("H")
H_V2 = Phi - sp.diff(chi, t) + dot(grad(chi), grad(chi)) / 2
for lab, mu_on in (("V2 (no dust)", False), ("KA6 (with dust term mu^2 H^2/(2K), COL1's reduced form)", True)):
    LV2 = L_psi(rho, th) + L_grav + dot(P, grad(H_V2)) + L_Pcore + (mu ** 2 * H_V2 ** 2 / (2 * K) if mu_on else 0)
    E_chi = euler_equations(LV2, [chi], [t, x, y, z])[0].lhs
    Cf = divP - (mu ** 2 / K * H_V2 if mu_on else 0)
    uf = [-gg for gg in grad(chi)]
    adv = sp.diff(Cf, t) + div([Cf * u for u in uf])
    ra = sp.simplify(sp.expand(E_chi + adv)); rb = sp.simplify(sp.expand(E_chi - adv))
    okv = ra == 0 or rb == 0
    name = "S1b_V2_charge" if not mu_on else "KA6_LFS1_COL1_charge"
    check(name, okv, f"{lab}: EL(chi) = -+[d_t C + div(C u_f)], u_f = -grad chi, C = "
          f"{'div P' if not mu_on else 'div P - mu^2 H/K  (= COL1 N = mu^2 h/K + div P, h = -H)'}: residual 0")
    if not mu_on:
        E_th2 = euler_equations(LV2, [th], [t, x, y, z])[0].lhs
        cps = nu * (sp.diff(rho, t) + div([rho * nu * gg for gg in grad(th)]))
        r_th2 = sp.simplify(sp.expand(E_th2 - cps)) * sp.simplify(sp.expand(E_th2 + cps))
        check("S1b_V2_psi_separate", r_th2 == 0, "V2: Psi's own charge is m|psi|^2 alone, carried with Psi (residual 0)")
RES["S1b_V2"] = {"charge": "div P (no dust)", "carried_by": "the frame's flow u_f", "FRW_value": 0}
P_("   V2 consequence (exact, with LFS1 S1(d)): on FRW P_bar = 0 by isotropy, so the frame's charge per volume element is 0")
P_("   and stays 0 along the frame's regular flow; spherically, div P = 0 with a regular centre forces P_r = 0, so A = 0:")
P_("   the frame never polarizes (the law never appears) and it moves as zero-charge (mimetic) dust.")

P_("")
P_("=== V1: the psi equation (S1e) ===")
x1 = sp.symbols("x1", real=True)
rh1 = sp.Function("rho")(t, x1); th1 = sp.Function("theta")(t, x1); Ph1 = sp.Function("Phi")(t, x1)
S1 = sp.Function("S")(t, x1)
psi = sp.sqrt(rh1) * sp.exp(sp.I * th1)
rho_t = -sp.diff(rh1 * nu * sp.diff(th1, x1), x1) - S1             # V1 continuity: S = D_t(div P) taken from n
th_t = (-nu ** 2 * sp.diff(th1, x1) ** 2 / 2 - Ph1 + nu ** 2 * sp.diff(sp.sqrt(rh1), x1, 2) / (2 * sp.sqrt(rh1))) / nu
psi_t = sp.diff(psi, t).subs({sp.Derivative(rh1, t): rho_t, sp.Derivative(th1, t): th_t})
lhs = sp.I * nu * psi_t - (-(nu ** 2 / 2) * sp.diff(psi, x1, 2) + Ph1 * psi)
extra = -(sp.I * nu / 2) * (S1 / rh1) * psi
rpsi = sp.simplify(sp.expand(sp.simplify((lhs - extra) / psi)))
check("S1e_V1_psi_singular", rpsi == 0,
      "with d_t(m n) + div(m n v) = -S, S = d_t(div P) + div((div P) v): i nu psi_t = H psi - (i nu/2)(S/|psi|^2) psi "
      "exactly -> a term that diverges at |psi| = 0 wherever S != 0 (X14's C5 objection in V1's form)")

P_("")
P_("=== Linear dispersion around a uniform medium (Jeans swindle), 1D, plane waves ===")
k, w, rb0, Ls = sp.symbols("k omega rhobar Lstar", positive=True)
dr, tt, ph, pp = sp.symbols("drho theta Phi P")


def disp(with_P, frame_phase=True, screen=True):
    # quadratic Lagrangian, Fourier amplitudes treated as a real symmetric form after e^{i(kx - wt)}
    # fields u = (drho, theta, Phi, P); kinetic term -drho nu theta_t ; quantum pressure nu^2 (drho_x)^2/(8 rhobar)
    # theta gradient rhobar nu^2 theta_x^2/2 ; -drho Phi ; -Phi_x^2/(8 pi G) ; P (Phi_x + nu theta_tx) - K P^2/2 - gamma (P_x)^2/2
    gm = K * Ls ** 2 / 2 if screen else 0
    I = sp.I
    # build the EL equations directly in Fourier space (d_t -> -i w, d_x -> i k)
    Dt, Dx = -I * w, I * k
    # Lagrangian bilinear: write the action density for complex amplitudes as u^dagger M u (Hermitian)
    # EL equations obtained by hand-free differentiation of the real Lagrangian; we use sympy on symbolic functions instead
    tt_, xx_ = sp.symbols("tt xx", real=True)
    d_ = sp.Function("d")(tt_, xx_); q_ = sp.Function("q")(tt_, xx_); f_ = sp.Function("f")(tt_, xx_); p_ = sp.Function("p")(tt_, xx_)
    L2 = (-d_ * nu * sp.diff(q_, tt_) - rb0 * nu ** 2 * sp.diff(q_, xx_) ** 2 / 2 - nu ** 2 * sp.diff(d_, xx_) ** 2 / (8 * rb0)
          - d_ * f_ - sp.diff(f_, xx_) ** 2 / (8 * sp.pi * Gn))
    if with_P:
        Ain = sp.diff(f_, xx_) + (nu * sp.diff(q_, tt_, xx_) if frame_phase else 0)
        L2 += p_ * Ain - K * p_ ** 2 / 2 - gm * sp.diff(p_, xx_) ** 2 / 2
    fl = [d_, q_, f_] + ([p_] if with_P else [])
    E = [e.lhs for e in euler_equations(L2, fl, [tt_, xx_])]
    amp = sp.symbols("A0:4")
    wave = sp.exp(I * (k * xx_ - w * tt_))
    sub = {fl[i]: amp[i] * wave for i in range(len(fl))}
    M = sp.Matrix([[sp.simplify(sp.diff((E[r_].subs(sub).doit() / wave), amp[c_])) for c_ in range(len(fl))]
                   for r_ in range(len(fl))])
    det = sp.factor(sp.simplify(M.det()))
    W2 = sp.symbols("W2")
    sols = sp.solve(sp.Eq(det.subs(w, sp.sqrt(W2)), 0), W2)
    sols = [s_ for s_ in sols if s_ != 0]
    return det, sols


det0, s0 = disp(False)
c5 = nu ** 2 * k ** 4 / 4 - 4 * sp.pi * Gn * rb0
okc5 = len(s0) == 1 and sp.simplify(s0[0] - c5) == 0
check("KA1_C5_dispersion", okc5, f"plain Psi: omega^2 = {s0}  (X14 C5: n = 4, coefficient nu^2/4)")
det1, s1 = disp(True)
kJ4 = 16 * sp.pi * Gn * rb0 / nu ** 2
cY = 1 / (1 + Ls ** 2 * k ** 2 / 2)
v1 = (nu ** 2 * k ** 4 / 4) / (1 + cY * k ** 4 / kJ4) - 4 * sp.pi * Gn * rb0
okv1 = len(s1) == 1 and sp.simplify(s1[0] - v1) == 0
check("S1c_V1_dispersion", okv1,
      f"V1: omega^2 = (nu^2 k^4/4)/(1 + cY q^4) - 4 pi G rhobar, q = k/k_J, cY = 1/(1 + Lstar^2 k^2/2): sympy root {s1}")
# QG1's closed form at u = 0 with mu^2 -> k_J^4/k^2
mu2 = kJ4 / k ** 2
qg1 = rb0 * K * ((1 - cY) * k ** 2 - mu2) / (cY * k ** 2 + mu2)
okq = sp.simplify(v1 - qg1) == 0
check("S1c_V1_equals_QG1_form", okq,
      "equals QG1's omega^2 = G k^2 (b - a)/(a b) at zero background acceleration with G = rhobar and the dust stiffness "
      "mu^2/K replaced by Psi's mu_eff^2/K, mu_eff^2 = k_J^4/k^2 (residual 0)")
# off branch (gamma = 0): omega^2 = -4 pi G rhobar/(1 + q^4)
det2, s2 = disp(True, screen=False)
v1off = -4 * sp.pi * Gn * rb0 / (1 + k ** 4 / kJ4)
okoff = len(s2) == 1 and sp.simplify(s2[0] - v1off) == 0
check("S1c_V1_offbranch", okoff,
      f"V1 off branch (no screening): omega^2 = -4 pi G rhobar/(1 + q^4) < 0 at every k: {s2} "
      "(the alpha = 2 P sector cancels the quantum pressure; no Jeans scale, growth rate falls as 1/q^2)")
qq = sp.symbols("q", positive=True)
rate_at_kJ_off = sp.simplify(-v1off.subs(k, sp.root(kJ4, 4)) / (4 * sp.pi * Gn * rb0))
P_(f"   V1 off branch: growth rate^2 / (4 pi G rhobar) at k = k_J = {rate_at_kJ_off} (half); plain Psi: 0")
RES["dispersion"] = {"plain": str(c5), "V1": str(v1), "V1_off": str(v1off), "rate2_at_kJ_over_4piGrho_V1off": str(rate_at_kJ_off)}

# mu_eff from integrating out drho: L(drho) = -drho h - nu^2 k^2 drho^2/(8 rhobar) -> max = 2 rhobar h^2/(nu^2 k^2)
h_ = sp.symbols("h")
Ld = -dr * h_ - nu ** 2 * k ** 2 * dr ** 2 / (8 * rb0)
dstar = sp.solve(sp.diff(Ld, dr), dr)[0]
Lmax = sp.simplify(Ld.subs(dr, dstar))
okmu = sp.simplify(Lmax - (mu2 / K) * h_ ** 2 / 2) == 0
check("S1c_V1_mu_eff", okmu, f"integrating out drho gives {Lmax} = (mu_eff^2/K) h^2/2 with mu_eff^2 = k_J^4/k^2")

RES["runtime_s"] = round(time.time() - T0, 1)
P_("")
P_(f"all checks {'PASS' if OK else 'FAIL'}; runtime {RES['runtime_s']} s")
P_("kappa = 1/2 FITTED; not theory closed. Adopts nothing.")
RES["all_ok"] = OK
open(os.path.join(HERE, STEM + ".out"), "w").write("\n".join(LINES) + "\n")
json.dump(RES, open(os.path.join(HERE, STEM + ".json"), "w"), indent=1, default=str)
sys.exit(0 if OK else 1)
